"""从目标期刊PDF语料学习图像层面的绘图风格。"""

from __future__ import annotations

import argparse
import json
import math
import re
import xml.etree.ElementTree as ET
from io import BytesIO
from collections import Counter
from pathlib import Path
from typing import Any
from urllib.parse import quote

import fitz
import numpy as np
import requests
import yaml
from PIL import Image


ARTICLE_ENDPOINTS = {
    "doi": "https://api.elsevier.com/content/article/doi/{id}",
    "pii": "https://api.elsevier.com/content/article/pii/{id}",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Learn visual figure style from target-journal PDFs.")
    parser.add_argument("--pdf-dir", action="append", default=[], help="Directory containing target-journal PDFs.")
    parser.add_argument("--pdf", action="append", default=[], help="Single target-journal PDF. May be repeated.")
    parser.add_argument("--sciencedirect-manifest", default=None, help="ScienceDirect corpus_manifest.json with DOI or PII records.")
    parser.add_argument("--topic-screening-report", default=None, help="Optional topic_screening_report.json used to keep accepted records only.")
    parser.add_argument("--api-key-file", default=None, help="Private ScienceDirect API key file for XML figure-object retrieval.")
    parser.add_argument("--journal", required=True, help="Target journal name.")
    parser.add_argument("--profile-name", default=None, help="Human-readable visual profile name.")
    parser.add_argument("--source", default="local_pdf_visual_corpus", help="Corpus source label.")
    parser.add_argument("--output", required=True, help="Output directory.")
    parser.add_argument("--max-docs", type=int, default=0, help="Maximum PDFs to process. Zero means all.")
    parser.add_argument("--max-records", type=int, default=0, help="Maximum ScienceDirect records to process. Zero means all.")
    parser.add_argument("--max-figures-per-record", type=int, default=0, help="Maximum ScienceDirect figure objects per record. Zero means all.")
    parser.add_argument("--object-timeout-seconds", type=int, default=30, help="Timeout for each ScienceDirect figure-object download.")
    parser.add_argument("--render-dpi", type=int, default=120, help="DPI for measuring figure crops.")
    parser.add_argument("--save-crops", action="store_true", help="Save low-resolution diagnostic crops for local QA.")
    parser.add_argument("--save-images", action="store_true", help="Save ScienceDirect figure images for local QA.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    pdfs = collect_pdfs(args)
    figures: list[dict[str, Any]] = []
    documents: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    crop_dir = output / "diagnostic_crops"
    if args.save_crops:
        crop_dir.mkdir(exist_ok=True)
    for index, path in enumerate(pdfs[: args.max_docs or None], 1):
        try:
            doc_figures, doc_record = process_pdf(path, index, args.render_dpi, crop_dir if args.save_crops else None)
            if doc_record.get("page_count", 0) >= 4 and doc_record.get("figure_count", 0) > 0:
                figures.extend(doc_figures)
                documents.append(doc_record)
        except Exception as exc:
            failures.append({"path": str(path), "error": str(exc)})
    if args.sciencedirect_manifest:
        if not args.api_key_file:
            raise SystemExit("--api-key-file is required when --sciencedirect-manifest is used.")
        api_key = Path(args.api_key_file).read_text(encoding="utf-8").strip()
        image_dir = output / "sciencedirect_figure_images" if args.save_images else None
        if image_dir is not None:
            image_dir.mkdir(exist_ok=True)
        sd_figures, sd_documents, sd_failures = process_sciencedirect_records(
            args,
            api_key,
            start_index=len(documents) + 1,
            image_dir=image_dir,
        )
        figures.extend(sd_figures)
        documents.extend(sd_documents)
        failures.extend(sd_failures)
    if not documents:
        raise SystemExit("No usable visual figure sources were processed.")
    profile = build_visual_profile(args, documents, figures, failures)
    write_yaml(output / "visual_figure_style.yaml", profile)
    write_json(output / "visual_figure_observations.json", {"figures": figures, "documents": documents, "failures": failures})
    write_digest(output / "visual_figure_style_digest.md", profile)
    if failures:
        write_json(output / "visual_extraction_failures.json", failures)
    print(f"Wrote visual figure style to {output / 'visual_figure_style.yaml'}")
    print(f"Documents processed: {len(documents)}")
    print(f"Figures measured: {len(figures)}")
    if failures:
        print(f"Failures: {len(failures)}")
    return 0


def collect_pdfs(args: argparse.Namespace) -> list[Path]:
    paths: list[Path] = []
    for folder in args.pdf_dir:
        paths.extend(sorted(Path(folder).glob("*.pdf")))
    for item in args.pdf:
        paths.append(Path(item))
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        unique.append(resolved)
    return unique


def process_sciencedirect_records(
    args: argparse.Namespace,
    api_key: str,
    start_index: int,
    image_dir: Path | None,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, str]]]:
    records = selected_sciencedirect_records(Path(args.sciencedirect_manifest), Path(args.topic_screening_report) if args.topic_screening_report else None)
    if args.max_records:
        records = records[: args.max_records]
    figures: list[dict[str, Any]] = []
    documents: list[dict[str, Any]] = []
    failures: list[dict[str, str]] = []
    for offset, record in enumerate(records, start_index):
        try:
            xml = fetch_article_xml(api_key, record)
            doc_figures = process_article_xml_objects(
                xml,
                api_key,
                record,
                offset,
                image_dir,
                args.max_figures_per_record,
                args.object_timeout_seconds,
            )
            if doc_figures:
                figures.extend(doc_figures)
                documents.append(
                    {
                        "path": record.get("doi") or record.get("pii") or record.get("title"),
                        "title": record.get("title"),
                        "doi": record.get("doi"),
                        "source": "sciencedirect_xml_objects",
                        "page_count": None,
                        "figure_count": len(doc_figures),
                    }
                )
        except Exception as exc:
            failures.append({"path": str(record.get("doi") or record.get("title")), "error": str(exc)})
    return figures, documents, failures


def selected_sciencedirect_records(manifest_path: Path, topic_report_path: Path | None) -> list[dict[str, Any]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    records = manifest.get("records", [])
    if topic_report_path is None:
        return [record for record in records if record.get("doi") or record.get("pii")]
    report = json.loads(topic_report_path.read_text(encoding="utf-8"))
    selected: list[dict[str, Any]] = []
    for item in report:
        if not item.get("accepted"):
            continue
        match = re.match(r"(\d+)_", Path(item.get("path", "")).name)
        if not match:
            continue
        index = int(match.group(1)) - 1
        if 0 <= index < len(records):
            record = records[index]
            if record.get("doi") or record.get("pii"):
                selected.append(record)
    return selected


def fetch_article_xml(api_key: str, record: dict[str, Any]) -> bytes:
    identifiers = []
    if record.get("pii"):
        identifiers.append(("pii", str(record["pii"])))
    if record.get("doi"):
        identifiers.append(("doi", str(record["doi"])))
    headers = {"X-ELS-APIKey": api_key, "Accept": "text/xml"}
    errors = []
    for kind, value in identifiers:
        url = ARTICLE_ENDPOINTS[kind].format(id=quote(value, safe=""))
        response = requests.get(url, headers=headers, params={"httpAccept": "text/xml"}, timeout=90)
        if response.ok and response.content:
            return response.content
        errors.append(f"{kind}:{response.status_code}")
    raise RuntimeError("article_xml_unavailable:" + ",".join(errors))


def process_article_xml_objects(
    xml: bytes,
    api_key: str,
    record: dict[str, Any],
    doc_index: int,
    image_dir: Path | None,
    max_figures: int = 0,
    object_timeout_seconds: int = 30,
) -> list[dict[str, Any]]:
    root = ET.fromstring(xml)
    objects = xml_object_map(root)
    figures: list[dict[str, Any]] = []
    figure_number = 0
    for figure in root.iter():
        if local_name(figure.tag) not in {"figure", "fig"}:
            continue
        if max_figures and figure_number >= max_figures:
            break
        label = first_descendant_text(figure, "label") or f"Fig. {figure_number + 1}"
        caption = first_descendant_text(figure, "caption")
        locator = figure_locator(figure)
        if not locator or locator not in objects:
            continue
        obj = objects[locator]
        if not is_usable_figure_object(obj):
            continue
        try:
            image_bytes = download_object_bytes(api_key, obj["url"], object_timeout_seconds)
            metrics = measure_image_bytes(image_bytes)
        except Exception:
            continue
        if not metrics:
            continue
        figure_number += 1
        caption_text = normalize_space(caption)
        figure_record = {
            "document": record.get("doi") or record.get("title"),
            "document_index": doc_index,
            "page": None,
            "label": normalize_space(label),
            "caption_words": len(word_tokens(caption_text)),
            "caption_topic": classify_caption_topic(caption_text),
            "panel_cue": bool(re.search(r"\b(panel|panels|subplot|subplots)\b|(?:\b[A-D]\b[,;]\s*){1,3}\b[A-D]\b", caption_text, re.I)),
            "object_ref": locator,
            "object_width": obj.get("width"),
            "object_height": obj.get("height"),
            **metrics,
        }
        if image_dir is not None:
            suffix = ".jpg" if "jpeg" in str(obj.get("mimetype", "")).lower() else ".png"
            image_path = image_dir / f"{doc_index:03d}_{safe_label(normalize_space(label))}_{safe_label(locator)}{suffix}"
            image_path.write_bytes(image_bytes)
            figure_record["saved_image"] = str(image_path)
        figures.append(figure_record)
    return figures


def xml_object_map(root: ET.Element) -> dict[str, dict[str, Any]]:
    objects: dict[str, dict[str, Any]] = {}
    for element in root.iter():
        if local_name(element.tag) != "object":
            continue
        ref = element.attrib.get("ref")
        url = normalize_space("".join(element.itertext()))
        if not ref or not url:
            continue
        candidate = {
            "ref": ref,
            "category": element.attrib.get("category"),
            "type": element.attrib.get("type"),
            "mimetype": element.attrib.get("mimetype"),
            "width": int(element.attrib.get("width", "0") or 0),
            "height": int(element.attrib.get("height", "0") or 0),
            "size": int(element.attrib.get("size", "0") or 0),
            "url": url,
        }
        current = objects.get(ref)
        if current is None or xml_object_rank(candidate) < xml_object_rank(current):
            objects[ref] = candidate
    return objects


def xml_object_rank(obj: dict[str, Any]) -> tuple[int, int, int, int]:
    category = str(obj.get("category", "")).lower()
    mimetype = str(obj.get("mimetype", "")).lower()
    url = str(obj.get("url", "")).lower()
    width = int(obj.get("width") or 0)
    height = int(obj.get("height") or 0)
    area = width * height
    if category in {"thumbnail", "thumb"}:
        category_rank = 9
    elif category == "standard":
        category_rank = 0
    elif "lrg" in category or "_lrg" in url or "large" in category:
        category_rank = 2
    else:
        category_rank = 1
    image_rank = 0 if "image" in mimetype else 1
    usable_rank = 0 if width >= 240 and height >= 100 else 1
    target_area = 720 * 480
    return (category_rank, image_rank + usable_rank, abs(area - target_area), int(obj.get("size") or 0))


def is_usable_figure_object(obj: dict[str, Any]) -> bool:
    if str(obj.get("category", "")).lower() in {"thumbnail", "thumb"}:
        return False
    if not str(obj.get("ref", "")).lower().startswith("gr"):
        return False
    if "image" not in str(obj.get("mimetype", "")).lower():
        return False
    return int(obj.get("width") or 0) >= 240 and int(obj.get("height") or 0) >= 100


def figure_locator(figure: ET.Element) -> str:
    for element in figure.iter():
        if local_name(element.tag) == "link":
            locator = element.attrib.get("locator")
            if locator:
                return locator
    return ""


def first_descendant_text(element: ET.Element, target_name: str) -> str:
    for child in element.iter():
        if local_name(child.tag) == target_name:
            return normalize_space(" ".join(child.itertext()))
    return ""


def download_object_bytes(api_key: str, url: str, timeout_seconds: int = 30) -> bytes:
    response = requests.get(url, headers={"X-ELS-APIKey": api_key, "Accept": "image/*"}, timeout=timeout_seconds)
    if not response.ok or not response.content:
        raise RuntimeError(f"object_download_failed:{response.status_code}")
    return response.content


def process_pdf(path: Path, doc_index: int, dpi: int, crop_dir: Path | None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    doc = fitz.open(path)
    figures: list[dict[str, Any]] = []
    for page_index in range(len(doc)):
        page = doc[page_index]
        captions = find_caption_blocks(page)
        for fig_index, caption in enumerate(captions, 1):
            crop_rect = infer_figure_rect(page, caption)
            if crop_rect is None or crop_rect.get_area() <= 0:
                continue
            metrics = measure_crop(page, crop_rect, dpi)
            if not metrics:
                continue
            caption_text = normalize_space(caption["text"])
            figure_record = {
                "document": str(path),
                "document_index": doc_index,
                "page": page_index + 1,
                "label": caption["label"],
                "caption_words": len(word_tokens(caption_text)),
                "caption_topic": classify_caption_topic(caption_text),
                "panel_cue": bool(re.search(r"\b(panel|panels|subplot|subplots|Fig\.\s*\d+[A-Za-z]?\([A-Za-z]\))\b|(?:\b[A-D]\b[,;]\s*){1,3}\b[A-D]\b", caption_text, re.I)),
                "crop_rect": [round(crop_rect.x0, 2), round(crop_rect.y0, 2), round(crop_rect.x1, 2), round(crop_rect.y1, 2)],
                **metrics,
            }
            if crop_dir is not None:
                crop_path = crop_dir / f"{doc_index:03d}_p{page_index + 1:03d}_{safe_label(caption['label'])}.png"
                pix = page.get_pixmap(matrix=fitz.Matrix(72 / 72, 72 / 72), clip=crop_rect, alpha=False)
                pix.save(crop_path)
                figure_record["diagnostic_crop"] = str(crop_path)
            figures.append(figure_record)
    record = {
        "path": str(path),
        "page_count": len(doc),
        "figure_count": len(figures),
    }
    doc.close()
    return figures, record


def find_caption_blocks(page: fitz.Page) -> list[dict[str, Any]]:
    blocks = page.get_text("blocks")
    captions: list[dict[str, Any]] = []
    for block in blocks:
        x0, y0, x1, y1, text = block[:5]
        clean = normalize_space(text)
        match = re.match(
            r"^(?P<label>(?:Fig\.?|Figure)\s*\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?)\s*(?:[:.]\s+|-\s+)(?P<body>.+)",
            clean,
            re.I,
        )
        if not match:
            continue
        if len(word_tokens(clean)) < 5:
            continue
        captions.append(
            {
                "label": normalize_figure_label(match.group("label")),
                "text": clean,
                "bbox": fitz.Rect(x0, y0, x1, y1),
            }
        )
    captions.sort(key=lambda item: (item["bbox"].y0, item["bbox"].x0))
    return captions


def infer_figure_rect(page: fitz.Page, caption: dict[str, Any]) -> fitz.Rect | None:
    cap = caption["bbox"]
    page_rect = page.rect
    band_top = max(page_rect.y0 + 18, cap.y0 - page_rect.height * 0.58)
    band_bottom = max(band_top + 24, cap.y0 - 4)
    band = fitz.Rect(page_rect.x0 + 18, band_top, page_rect.x1 - 18, band_bottom)
    rects: list[fitz.Rect] = []
    for item in page.get_drawings():
        rect = item.get("rect")
        if not rect:
            continue
        rect = fitz.Rect(rect)
        if rect.get_area() < 2:
            continue
        if rect.intersects(band):
            rects.append(rect & band)
    try:
        for info in page.get_image_info(xrefs=True):
            rect = fitz.Rect(info["bbox"])
            if rect.get_area() > 20 and rect.intersects(band):
                rects.append(rect & band)
    except Exception:
        pass
    for block in page.get_text("blocks"):
        x0, y0, x1, y1, text = block[:5]
        rect = fitz.Rect(x0, y0, x1, y1)
        if rect.y1 >= cap.y0 or rect.y0 < band_top or not rect.intersects(band):
            continue
        clean = normalize_space(text)
        if re.match(r"^(?:Fig\.?|Figure|Table)\s*\d+", clean, re.I):
            continue
        if len(word_tokens(clean)) <= 12 or rect.height <= 28:
            rects.append(rect & band)
    if rects:
        union = rects[0]
        for rect in rects[1:]:
            union |= rect
        pad = 6
        crop = fitz.Rect(
            max(page_rect.x0, union.x0 - pad),
            max(page_rect.y0, union.y0 - pad),
            min(page_rect.x1, union.x1 + pad),
            min(page_rect.y1, union.y1 + pad),
        )
        if crop.height >= 35 and crop.width >= 80:
            return crop
    fallback_height = min(page_rect.height * 0.42, 260)
    return fitz.Rect(page_rect.x0 + 24, max(page_rect.y0 + 24, cap.y0 - fallback_height), page_rect.x1 - 24, cap.y0 - 4)


def measure_crop(page: fitz.Page, rect: fitz.Rect, dpi: int) -> dict[str, Any]:
    scale = dpi / 72
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), clip=rect, alpha=False)
    if pix.width < 20 or pix.height < 20:
        return {}
    arr = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, pix.n))
    if pix.n > 3:
        arr = arr[:, :, :3]
    rgb = arr.astype(np.int16)
    maxc = rgb.max(axis=2)
    minc = rgb.min(axis=2)
    mean = rgb.mean(axis=2)
    saturation = maxc - minc
    white = (rgb[:, :, 0] > 245) & (rgb[:, :, 1] > 245) & (rgb[:, :, 2] > 245)
    dark = mean < 75
    light_gray = (mean > 170) & (mean < 245) & (saturation < 12)
    color = (saturation > 35) & (maxc < 245)
    nonwhite = ~white
    edge_density = simple_edge_density(mean)
    palette = dominant_palette(rgb, nonwhite)
    page_rect = page.rect
    return {
        "crop_width_pt": round(rect.width, 2),
        "crop_height_pt": round(rect.height, 2),
        "crop_width_fraction": round(rect.width / page_rect.width, 3) if page_rect.width else None,
        "crop_height_fraction": round(rect.height / page_rect.height, 3) if page_rect.height else None,
        "aspect_ratio": round(rect.width / rect.height, 3) if rect.height else None,
        "white_fraction": round(float(white.mean()), 4),
        "ink_density": round(float(nonwhite.mean()), 4),
        "dark_fraction": round(float(dark.mean()), 4),
        "light_gray_fraction": round(float(light_gray.mean()), 4),
        "color_fraction": round(float(color.mean()), 4),
        "edge_density": round(edge_density, 4),
        "dominant_colors": palette,
    }


def measure_image_bytes(image_bytes: bytes) -> dict[str, Any]:
    with Image.open(BytesIO(image_bytes)) as image:
        rgb_image = image.convert("RGB")
        arr = np.asarray(rgb_image, dtype=np.uint8)
    if arr.shape[0] < 20 or arr.shape[1] < 20:
        return {}
    metrics = measure_rgb_array(arr)
    metrics.update(
        {
            "image_width_px": int(arr.shape[1]),
            "image_height_px": int(arr.shape[0]),
            "aspect_ratio": round(arr.shape[1] / arr.shape[0], 3) if arr.shape[0] else None,
        }
    )
    return metrics


def measure_rgb_array(arr: np.ndarray) -> dict[str, Any]:
    rgb = arr.astype(np.int16)
    maxc = rgb.max(axis=2)
    minc = rgb.min(axis=2)
    mean = rgb.mean(axis=2)
    saturation = maxc - minc
    white = (rgb[:, :, 0] > 245) & (rgb[:, :, 1] > 245) & (rgb[:, :, 2] > 245)
    dark = mean < 75
    light_gray = (mean > 170) & (mean < 245) & (saturation < 12)
    color = (saturation > 35) & (maxc < 245)
    nonwhite = ~white
    return {
        "white_fraction": round(float(white.mean()), 4),
        "ink_density": round(float(nonwhite.mean()), 4),
        "dark_fraction": round(float(dark.mean()), 4),
        "light_gray_fraction": round(float(light_gray.mean()), 4),
        "color_fraction": round(float(color.mean()), 4),
        "edge_density": round(simple_edge_density(mean), 4),
        "dominant_colors": dominant_palette(rgb, nonwhite),
    }


def simple_edge_density(mean: np.ndarray) -> float:
    if mean.shape[0] < 3 or mean.shape[1] < 3:
        return 0.0
    dx = np.abs(np.diff(mean, axis=1))
    dy = np.abs(np.diff(mean, axis=0))
    return float(((dx > 35).mean() + (dy > 35).mean()) / 2)


def dominant_palette(rgb: np.ndarray, mask: np.ndarray, limit: int = 8) -> list[dict[str, Any]]:
    if mask.sum() == 0:
        return []
    sample = rgb[mask]
    if len(sample) > 50000:
        step = max(1, len(sample) // 50000)
        sample = sample[::step]
    maxc = sample.max(axis=1)
    minc = sample.min(axis=1)
    sat = maxc - minc
    keep = (maxc < 245) & ~((sat < 12) & (maxc > 160))
    sample = sample[keep]
    if len(sample) == 0:
        return []
    quant = (sample // 32) * 32
    counts = Counter(map(tuple, quant.tolist()))
    total = sum(counts.values())
    rows = []
    for color, count in counts.most_common(limit):
        r, g, b = [int(min(255, c + 16)) for c in color]
        rows.append({"hex": f"#{r:02X}{g:02X}{b:02X}", "share": round(count / total, 4)})
    return rows


def build_visual_profile(args: argparse.Namespace, documents: list[dict[str, Any]], figures: list[dict[str, Any]], failures: list[dict[str, str]]) -> dict[str, Any]:
    profile_strength = "normal" if len(documents) >= 30 else "caution" if len(documents) >= 10 else "pilot"
    caption_topics = Counter(item.get("caption_topic", "unknown") for item in figures)
    panel_count = sum(1 for item in figures if item.get("panel_cue"))
    color_counter: Counter[str] = Counter()
    for item in figures:
        for color in item.get("dominant_colors", [])[:4]:
            color_counter[color["hex"]] += 1
    caption_metric_name = "caption_fragment_words" if "sciencedirect" in args.source.lower() else "caption_words"
    metrics = {
        "figures_per_article": distribution([doc.get("figure_count") for doc in documents]),
        caption_metric_name: distribution([item.get("caption_words") for item in figures]),
        "image_width_px": distribution([item.get("image_width_px") for item in figures]),
        "image_height_px": distribution([item.get("image_height_px") for item in figures]),
        "crop_width_fraction": distribution([item.get("crop_width_fraction") for item in figures]),
        "crop_height_fraction": distribution([item.get("crop_height_fraction") for item in figures]),
        "aspect_ratio": distribution([item.get("aspect_ratio") for item in figures]),
        "ink_density": distribution([item.get("ink_density") for item in figures]),
        "dark_fraction": distribution([item.get("dark_fraction") for item in figures]),
        "light_gray_fraction": distribution([item.get("light_gray_fraction") for item in figures]),
        "color_fraction": distribution([item.get("color_fraction") for item in figures]),
        "edge_density": distribution([item.get("edge_density") for item in figures]),
    }
    return {
        "schema_version": "visual-figure-style-1.0",
        "profile_name": args.profile_name or f"{args.journal} visual figure style",
        "journal": args.journal,
        "source": args.source,
        "profile_strength": profile_strength,
        "corpus": {
            "document_count": len(documents),
            "figure_count": len(figures),
            "failure_count": len(failures),
            "documents": documents,
        },
        "visual_metrics": metrics,
        "figure_topics": counter_records(caption_topics, 12),
        "panel_cue_share": round(panel_count / len(figures), 3) if figures else None,
        "dominant_palette": [{"hex": color, "doc_or_figure_count": count} for color, count in color_counter.most_common(12)],
        "measurement_notes": measurement_notes(args.source),
        "style_rules": style_rules(metrics, panel_count, len(figures), args.source),
    }


def measurement_notes(source: str) -> list[str]:
    notes: list[str] = []
    if "sciencedirect" in source.lower():
        notes.append("ScienceDirect figure-object captions can be short title fragments; use the full-text caption profile for authoritative caption length and syntax.")
        notes.append("Panel cues derived from XML caption text can undercount visual multi-panel layouts.")
    return notes


def style_rules(metrics: dict[str, dict[str, Any]], panel_count: int, figure_count: int, source: str) -> dict[str, list[str]]:
    rules = {
        "layout": [],
        "color": [],
        "axes_and_grid": [],
        "caption_handoff": [],
    }
    aspect = metrics.get("aspect_ratio", {})
    width = metrics.get("crop_width_fraction", {})
    color = metrics.get("color_fraction", {})
    gray = metrics.get("light_gray_fraction", {})
    caption = metrics.get("caption_words", {})
    if width.get("median") is not None:
        rules["layout"].append(f"Target figure visual width around {width['p25']:.2f} to {width['p75']:.2f} of page width.")
    if aspect.get("median") is not None:
        rules["layout"].append(f"Use aspect ratios around {aspect['p25']:.2f} to {aspect['p75']:.2f} for comparable figures.")
    if figure_count and panel_count / figure_count >= 0.25:
        rules["layout"].append("Use named panels when one display compares mechanisms, diagnostics, or external checks.")
    if color.get("median") is not None:
        if color["median"] < 0.08:
            rules["color"].append("Keep most plotted ink dark or neutral, with restrained accent colors for method families.")
        else:
            rules["color"].append("Use color deliberately for method families, regimes, or uncertainty bands.")
    if gray.get("median") is not None and gray["median"] > 0.05:
        rules["axes_and_grid"].append("Light gray gridlines or reference guides are common enough to use when they improve quantitative reading.")
    rules["axes_and_grid"].append("Keep axis labels explicit with metric and unit whenever the display reports operating quantities.")
    if "sciencedirect" in source.lower():
        rules["caption_handoff"].append("Use this visual profile for image-level layout, palette, and topic mix; use the full-text caption profile for caption length and sentence syntax.")
    elif caption.get("p25") is not None and caption.get("p75") is not None:
        rules["caption_handoff"].append(f"Pair the visual with captions around {caption['p25']:.0f} to {caption['p75']:.0f} words when complexity is comparable.")
    return rules


def write_digest(path: Path, profile: dict[str, Any]) -> None:
    metrics = profile.get("visual_metrics", {})
    lines = [
        f"# Visual Figure Style Digest: {profile['journal']}",
        "",
        f"Profile strength: `{profile['profile_strength']}`",
        f"Documents processed: {profile['corpus']['document_count']}",
        f"Figures measured: {profile['corpus']['figure_count']}",
        "",
        "## Visual Metrics",
        "",
        markdown_table(
            [
                [name, dist.get("median"), dist.get("p25"), dist.get("p75")]
                for name, dist in metrics.items()
            ],
            ["Metric", "Median", "P25", "P75"],
        ),
        "",
        "## Figure Topics",
        "",
        record_line(profile.get("figure_topics", [])),
        "",
        "## Panel And Palette Signals",
        "",
        f"- Panel cue share: {profile.get('panel_cue_share')}",
        f"- Dominant palette signals: {record_palette(profile.get('dominant_palette', []))}",
        "",
        "## Measurement Notes",
        "",
        record_notes(profile.get("measurement_notes", [])),
        "",
        "## Downstream Figure Rules",
        "",
    ]
    for group, rules in profile.get("style_rules", {}).items():
        lines.append(f"### {group.replace('_', ' ').title()}")
        lines.append("")
        for rule in rules:
            lines.append(f"- {rule}")
        lines.append("")
    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def classify_caption_topic(text: str) -> str:
    lower = text.lower()
    if re.search(r"\b(comparison|compare|versus|vs\.?|benchmark|baseline)\b", lower):
        return "comparison"
    if re.search(r"\b(performance|error|rmse|mae|mape|accuracy|score|risk|coverage)\b", lower):
        return "performance_or_metric"
    if re.search(r"\b(distribution|density|histogram|box|uncertainty|interval)\b", lower):
        return "distribution_or_uncertainty"
    if re.search(r"\b(framework|architecture|flow|workflow|scheme|structure)\b", lower):
        return "framework_or_process"
    if re.search(r"\b(map|spatial|region|farm|site|zone)\b", lower):
        return "spatial_or_case"
    if re.search(r"\b(sensitivity|threshold|ablation|scenario)\b", lower):
        return "sensitivity_or_ablation"
    if re.search(r"\b(time|hour|daily|season|horizon|series)\b", lower):
        return "temporal_pattern"
    return "descriptive"


def distribution(values: list[Any]) -> dict[str, float | None]:
    cleaned = sorted(float(value) for value in values if isinstance(value, (int, float)) and not math.isnan(float(value)))
    if not cleaned:
        return {"median": None, "p25": None, "p75": None, "min": None, "max": None}
    return {
        "median": round(percentile(cleaned, 50), 4),
        "p25": round(percentile(cleaned, 25), 4),
        "p75": round(percentile(cleaned, 75), 4),
        "min": round(cleaned[0], 4),
        "max": round(cleaned[-1], 4),
    }


def percentile(values: list[float], q: float) -> float:
    if not values:
        return float("nan")
    if len(values) == 1:
        return values[0]
    pos = (len(values) - 1) * q / 100
    lower = math.floor(pos)
    upper = math.ceil(pos)
    if lower == upper:
        return values[int(pos)]
    return values[lower] * (upper - pos) + values[upper] * (pos - lower)


def markdown_table(rows: list[list[Any]], headers: list[str]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join("" if value is None else str(value) for value in row) + " |")
    return "\n".join(out)


def counter_records(counter: Counter[str], limit: int) -> list[dict[str, Any]]:
    return [{"pattern": key, "count": count} for key, count in counter.most_common(limit)]


def record_line(records: list[dict[str, Any]]) -> str:
    if not records:
        return "Unchecked"
    return "; ".join(f"{item['pattern']} ({item['count']})" for item in records)


def record_palette(records: list[dict[str, Any]]) -> str:
    if not records:
        return "Unchecked"
    return "; ".join(f"{item['hex']} ({item['doc_or_figure_count']})" for item in records[:10])


def record_notes(notes: list[str]) -> str:
    if not notes:
        return "None"
    return "\n".join(f"- {note}" for note in notes)


def normalize_figure_label(label: str) -> str:
    match = re.search(r"(?:Fig\.?|Figure)\s*(\d+[A-Za-z]?)", label, re.I)
    return f"Fig. {match.group(1)}" if match else label.strip()


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def word_tokens(text: str) -> list[str]:
    return re.findall(r"<[a-z_]+>|[A-Za-z][A-Za-z0-9\-]*|\d+(?:\.\d+)?%?", text)


def safe_label(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", value.strip())[:80]


def local_name(tag: str) -> str:
    return tag.split("}")[-1].split(":")[-1]


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
