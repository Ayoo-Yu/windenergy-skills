"""风格学习脚本的共享函数。"""

from __future__ import annotations

import json
import math
import re
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import fitz
import yaml


SECTION_ALIASES = {
    "highlights": ["highlights"],
    "article_info": ["article info"],
    "abstract": ["abstract"],
    "keywords": ["keywords", "key words"],
    "nomenclature": ["nomenclature"],
    "introduction": ["introduction", "background"],
    "related_work": ["related work", "literature review"],
    "methods": [
        "method",
        "methods",
        "methodology",
        "materials and methods",
        "model",
        "proposed method",
    ],
    "case_study": ["case study", "study area", "data", "dataset"],
    "results": ["results", "experimental results", "experiments"],
    "discussion": ["discussion"],
    "results_discussion": ["results and discussion", "results & discussion"],
    "conclusion": [
        "conclusion",
        "conclusions",
        "conclusion and future work",
        "conclusions and future work",
        "conclusions and future works",
        "conclusion and future research",
        "conclusion and future scope",
        "conclusion and prospect",
        "conclusions and future directions",
        "conclusions and future recommendations",
        "concluding remarks",
    ],
    "appendix": ["appendix", "appendices"],
    "acknowledgements": ["acknowledgements", "acknowledgments"],
    "funding": ["funding", "funding statement"],
    "data_availability": ["data availability", "data availability statement", "data and code availability"],
    "declaration": [
        "declaration of competing interest",
        "declaration of interests",
        "conflict of interest",
        "credit authorship contribution statement",
    ],
    "references": ["references"],
}

SECTION_ORDER = [
    "highlights",
    "article_info",
    "abstract",
    "keywords",
    "nomenclature",
    "introduction",
    "related_work",
    "methods",
    "case_study",
    "results",
    "discussion",
    "results_discussion",
    "conclusion",
    "appendix",
    "acknowledgements",
    "funding",
    "data_availability",
    "declaration",
    "references",
]

HEDGE_TERMS = {
    "may",
    "might",
    "could",
    "suggest",
    "indicate",
    "likely",
    "potential",
    "approximately",
}

CONTRAST_TERMS = {
    "however",
    "although",
    "whereas",
    "while",
    "nevertheless",
    "in contrast",
}

CAUSAL_TERMS = {
    "therefore",
    "thus",
    "because",
    "thereby",
    "consequently",
    "as a result",
}

LIMITATION_TERMS = {
    "limitation",
    "limited",
    "uncertain",
    "uncertainty",
    "future work",
    "scope",
    "constraint",
}

ABSTRACT_MOVE_PATTERNS = {
    "context": re.compile(r"\b(challenge|important|critical|operation|grid|renewable|wind)\b", re.I),
    "gap": re.compile(r"\b(however|cannot|limited|challenge|gap|uncertain|rarely)\b", re.I),
    "method": re.compile(r"\b(we propose|we develop|we formulate|we present|this paper|method|model)\b", re.I),
    "result": re.compile(r"\b(attain|achieve|reduce|increase|improve|outperform|%|\d+\.\d+)\b", re.I),
    "implication": re.compile(r"\b(indicating|suggesting|demonstrating|enable|operational|grid|practical)\b", re.I),
}

MOVE_PATTERNS = {
    "context": re.compile(r"\b(energy|power|renewable|grid|system|operation|decarbon|transition|demand)\b", re.I),
    "gap": re.compile(r"\b(however|despite|although|challenge|limited|lack|remain|difficult|uncertain)\b", re.I),
    "method": re.compile(r"\b(propose|develop|present|introduce|formulate|framework|model|method|approach)\b", re.I),
    "result": re.compile(r"\b(result|show|demonstrate|achieve|reduce|increase|improve|outperform|performance|%)\b", re.I),
    "implication": re.compile(r"\b(indicate|suggest|enable|provide|support|practical|operational|decision|planning)\b", re.I),
    "limitation": re.compile(r"\b(limitation|future work|further|uncertainty|constraint|scope)\b", re.I),
}

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "with",
}

RESEARCH_VERBS = {
    "achieve",
    "address",
    "analyze",
    "assess",
    "compare",
    "demonstrate",
    "develop",
    "evaluate",
    "formulate",
    "improve",
    "indicate",
    "introduce",
    "investigate",
    "optimize",
    "outperform",
    "present",
    "propose",
    "provide",
    "reduce",
    "reveal",
    "show",
    "validate",
}

DEGREE_TERMS = {
    "significantly",
    "substantially",
    "considerably",
    "slightly",
    "marginally",
    "moderately",
    "notably",
    "consistently",
    "effectively",
}

BOILERPLATE_PHRASES = {
    "contents lists available",
    "journal homepage",
    "published by elsevier",
    "open access article",
    "cc by license",
    "sciencedirect",
    "doi.org",
    "applied energy",
    "energy and buildings",
    "received in revised form",
    "available online",
    "e-mail address",
    "email address",
    "corresponding author",
    "declaration of competing interest",
    "credit author statement",
    "data availability",
    "supplementary data",
    "supplementary material",
    "supplementary fig",
    "supplementary table",
    "acknowledgements",
    "funding this research",
    "funded by",
    "writing review editing",
    "writing original draft",
    "funding acquisition",
    "formal analysis",
    "data curation",
    "conceptualization",
    "if there are other authors",
    "declaration of generative ai",
    "appendix a",
    "references",
}

TOPIC_PROFILES = {
    "wind_forecasting": {
        "required_groups": ["wind", "forecast_core"],
        "min_score": 6,
        "include": {
            "wind": [
                "wind power",
                "wind energy",
                "wind farm",
                "wind farms",
                "wind turbine",
                "wind turbines",
                "wind speed",
                "wind generation",
                "offshore wind",
                "wind scenario",
            ],
            "forecast_core": [
                "forecast",
                "forecasting",
                "prediction",
                "predictive",
                "prediction interval",
                "scenario generation",
            ],
            "horizon": ["short-term", "ultra-short-term", "day-ahead", "ahead"],
            "uncertainty": [
                "probabilistic",
                "uncertainty",
                "quantile",
                "interval",
                "scenario",
            ],
        },
        "exclude": [
            "urban building",
            "ubem",
            "building energy modelling",
            "building energy modeling",
            "building stock",
            "hot water",
            "thermal load",
            "district heating",
            "hvac",
            "heat pump",
            "heating cooling",
            "solar irradiance",
            "photovoltaic performance",
            "electrolyzer",
            "hydrogen storage",
            "levelized cost",
            "lcoe",
            "energy community",
            "renewable energy community",
            "public transit",
            "electric vehicle charging",
            "microgrid scheduling",
            "peer-to-peer",
        ],
    },
    "renewable_forecasting": {
        "required_groups": ["renewable", "forecasting"],
        "min_score": 5,
        "include": {
            "renewable": [
                "wind power",
                "wind energy",
                "solar power",
                "photovoltaic",
                "renewable energy",
                "renewable generation",
                "net load",
                "power system",
            ],
            "forecasting": [
                "forecast",
                "forecasting",
                "prediction",
                "predictive",
                "probabilistic",
                "prediction interval",
                "uncertainty",
                "scenario generation",
            ],
            "horizon": ["short-term", "ultra-short-term", "day-ahead", "ahead"],
        },
        "exclude": [
            "urban building",
            "ubem",
            "building energy modelling",
            "building energy modeling",
            "hot water",
            "district heating",
            "hvac",
            "electrolyzer",
            "public transit",
        ],
    },
}

COMPARISON_VERBS = {
    "achieve",
    "compare",
    "decrease",
    "improve",
    "increase",
    "outperform",
    "reduce",
    "surpass",
}


@dataclass
class PdfDocument:
    path: Path
    text: str
    page_count: int
    metadata: dict[str, Any]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")


def read_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def extract_pdf(path: Path) -> PdfDocument:
    doc = fitz.open(path)
    pages = []
    for page in doc:
        pages.append(page.get_text("text"))
    metadata = {k: v for k, v in doc.metadata.items() if v}
    text = normalize_text("\n".join(pages))
    return PdfDocument(path=path, text=text, page_count=len(doc), metadata=metadata)


def extract_text_document(path: Path) -> PdfDocument:
    text = normalize_text(path.read_text(encoding="utf-8", errors="replace"))
    page_count = max(1, math.ceil(len(word_tokens(text)) / 750))
    metadata = {"source_format": path.suffix.lstrip(".").lower() or "text", "title": path.stem}
    return PdfDocument(path=path, text=text, page_count=page_count, metadata=metadata)


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"(?<=\w)-\n(?=\w)", "", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def safe_label(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    text = text.replace("\u2014", "-").replace("\u2013", "-")
    return text


def sentence_split(text: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return []
    protected = protect_sentence_abbreviations(cleaned)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", protected)
    return [restore_sentence_abbreviations(p.strip()) for p in parts if len(p.strip()) > 2]


def protect_sentence_abbreviations(text: str) -> str:
    placeholder = "<DOT>"
    # 保护学术缩写，避免 Fig. 1 和 et al. 被误切成半句。
    abbreviations = ["Fig.", "Figs.", "Eq.", "Eqs.", "Ref.", "Refs.", "No.", "Nos.", "e.g.", "i.e.", "et al."]
    protected = text
    for abbreviation in abbreviations:
        protected = re.sub(
            re.escape(abbreviation),
            lambda match: match.group(0).replace(".", placeholder),
            protected,
            flags=re.I,
        )
    return protected


def restore_sentence_abbreviations(text: str) -> str:
    return text.replace("<DOT>", ".")


def word_tokens(text: str) -> list[str]:
    return re.findall(r"<[a-z_]+>|[A-Za-z][A-Za-z0-9\-]*|\d+(?:\.\d+)?%?", text)


def paragraph_split(text: str) -> list[str]:
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    if len(blocks) >= 3:
        return blocks
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    paragraphs: list[str] = []
    current: list[str] = []
    for line in lines:
        if looks_like_heading(line):
            if current:
                paragraphs.append(" ".join(current))
                current = []
            paragraphs.append(line)
        else:
            current.append(line)
            if line.endswith((".", "?", "!")) and len(" ".join(current)) > 180:
                paragraphs.append(" ".join(current))
                current = []
    if current:
        paragraphs.append(" ".join(current))
    return paragraphs


def looks_like_heading(line: str) -> bool:
    stripped = line.strip()
    if len(stripped) > 90:
        return False
    if re.match(r"^\d+(?:\s*\.\s*\d+)*\s*\.?\s+[A-Z][A-Za-z0-9 ,:/&\-]+$", stripped):
        return True
    lowered = normalize_heading_text(stripped)
    return any(lowered == alias for aliases in SECTION_ALIASES.values() for alias in aliases)


def split_sections(text: str) -> dict[str, str]:
    lines = text.splitlines()
    hits: list[tuple[int, str]] = []
    for idx, line in enumerate(lines):
        heading = canonical_heading(line)
        if heading:
            hits.append((idx, heading))
    sections: dict[str, str] = {}
    for pos, (start, name) in enumerate(hits):
        end = hits[pos + 1][0] if pos + 1 < len(hits) else len(lines)
        content = "\n".join(lines[start + 1 : end]).strip()
        if not content:
            continue
        if name not in sections:
            sections[name] = content
            continue
        if len(word_tokens(content)) >= 20:
            sections[name] = "\n\n".join([sections[name], content]).strip()
    if "abstract" not in sections:
        match = re.search(r"\bAbstract\b(.+?)(?:\bKeywords\b|\b1\s+Introduction\b)", text, re.I | re.S)
        if match:
            sections["abstract"] = match.group(1).strip()
    return sections


def canonical_heading(line: str) -> str | None:
    stripped = re.sub(r"^\s*\d+(?:\s*\.\s*\d+)*\s*\.?\s*", "", line.strip())
    stripped = normalize_heading_text(stripped)
    if not stripped or len(stripped) > 80:
        return None
    if re.match(r"^appendix(?:\s+[a-z0-9]+)?(?:\.|\s|$)", stripped):
        return "appendix"
    for key, aliases in SECTION_ALIASES.items():
        if stripped in aliases:
            return key
    return None


def normalize_heading_text(value: str) -> str:
    value = value.strip().strip(":").lower()
    if re.fullmatch(r"(?:[a-z]\s+){2,}[a-z]", value):
        value = value.replace(" ", "")
    return re.sub(r"\s+", " ", value)


def topic_screen_document(
    doc: PdfDocument,
    profile_name: str | None,
    min_score: int | None = None,
    include_keywords: list[str] | None = None,
    exclude_keywords: list[str] | None = None,
) -> dict[str, Any]:
    if not profile_name or profile_name == "none":
        return {"accepted": True, "profile": "none", "score": None, "reason": "topic_screen_disabled"}
    profile = TOPIC_PROFILES.get(profile_name)
    if not profile:
        raise ValueError(f"Unknown topic profile: {profile_name}")
    title = str(doc.metadata.get("title") or doc.path.stem)
    excluded_type = excluded_article_type(title)
    if excluded_type:
        return {
            "accepted": False,
            "profile": profile_name,
            "score": None,
            "threshold": min_score if min_score is not None else int(profile.get("min_score", 0)),
            "include_hits": {},
            "exclude_hits": [excluded_type],
            "required_missing": [],
            "reason": f"document_type_excluded:{excluded_type}",
        }
    sections = split_sections(doc.text)
    screened_text = "\n".join(
        [
            title,
            sections.get("abstract", ""),
            sections.get("keywords", ""),
            "\n".join(sentence_split(sections.get("introduction", ""))[:10]),
        ]
    ).lower()
    include = {name: list(values) for name, values in profile.get("include", {}).items()}
    if include_keywords:
        include.setdefault("custom", []).extend(include_keywords)
    exclude = list(profile.get("exclude", []))
    if exclude_keywords:
        exclude.extend(exclude_keywords)

    group_hits: dict[str, list[str]] = {}
    score = 0
    for group, terms in include.items():
        hits = sorted({term for term in terms if term.lower() in screened_text})
        group_hits[group] = hits
        score += len(hits) * (3 if group in profile.get("required_groups", []) else 1)
    exclude_hits = sorted({term for term in exclude if term.lower() in screened_text})
    score -= len(exclude_hits) * 4
    required_missing = [
        group
        for group in profile.get("required_groups", [])
        if not group_hits.get(group)
    ]
    threshold = min_score if min_score is not None else int(profile.get("min_score", 0))
    accepted = not required_missing and not exclude_hits and score >= threshold
    reason = "accepted" if accepted else "topic_mismatch"
    if required_missing:
        reason += ":missing_" + ",".join(required_missing)
    if exclude_hits:
        reason += ":excluded_" + ",".join(exclude_hits[:5])
    if score < threshold:
        reason += f":score_below_{threshold}"
    return {
        "accepted": accepted,
        "profile": profile_name,
        "score": score,
        "threshold": threshold,
        "required_missing": required_missing,
        "include_hits": group_hits,
        "exclude_hits": exclude_hits,
        "reason": reason,
    }


def excluded_article_type(title: str) -> str:
    lower = title.lower()
    if re.search(r"\b(a|an|systematic|critical|comprehensive|deep|state-of-the-art)?\s*review\b", lower):
        return "review"
    if re.search(r"\breview\s+(of|and|on)\b", lower):
        return "review"
    if re.search(r"\bsurvey\b", lower):
        return "survey"
    if re.search(r"\bbibliometric\b|\bperspective\b", lower):
        return "non_research_article"
    return ""


def basic_metrics(text: str) -> dict[str, Any]:
    words = word_tokens(text)
    sentences = sentence_split(text)
    paragraphs = paragraph_split(text)
    sent_lengths = [len(word_tokens(s)) for s in sentences if word_tokens(s)]
    lower = text.lower()
    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
        "median_sentence_words": safe_median(sent_lengths),
        "p75_sentence_words": percentile(sent_lengths, 75),
        "numeric_tokens_per_1000_words": rate_per_1000(count_numeric(words), len(words)),
        "citation_markers_per_1000_words": rate_per_1000(count_citations(text), len(words)),
        "figure_refs_per_1000_words": rate_per_1000(len(re.findall(r"\b(?:Fig\.|Figure)\s*\d+", text)), len(words)),
        "table_refs_per_1000_words": rate_per_1000(len(re.findall(r"\bTable\s*\d+", text)), len(words)),
        "hedge_terms_per_1000_words": rate_per_1000(term_count(lower, HEDGE_TERMS), len(words)),
        "contrast_terms_per_1000_words": rate_per_1000(term_count(lower, CONTRAST_TERMS), len(words)),
        "causal_terms_per_1000_words": rate_per_1000(term_count(lower, CAUSAL_TERMS), len(words)),
        "limitation_terms_per_1000_words": rate_per_1000(term_count(lower, LIMITATION_TERMS), len(words)),
    }


def count_numeric(words: Iterable[str]) -> int:
    return sum(1 for word in words if re.search(r"\d", word))


def count_citations(text: str) -> int:
    numbered = len(re.findall(r"\[(?:\d+[,\-\s]*)+\]", text))
    author_year = len(re.findall(r"\b[A-Z][A-Za-z\-]+ et al\.,? \d{4}\b", text))
    return numbered + author_year


def term_count(lower_text: str, terms: Iterable[str]) -> int:
    count = 0
    for term in terms:
        count += len(re.findall(r"\b" + re.escape(term.lower()) + r"\b", lower_text))
    return count


def rate_per_1000(count: int, denominator_words: int) -> float | None:
    if denominator_words <= 0:
        return None
    return round(count * 1000 / denominator_words, 2)


def safe_median(values: list[float | int]) -> float | None:
    if not values:
        return None
    return round(float(statistics.median(values)), 2)


def percentile(values: list[float | int], pct: int) -> float | None:
    if not values:
        return None
    ordered = sorted(float(v) for v in values)
    if len(ordered) == 1:
        return round(ordered[0], 2)
    rank = (len(ordered) - 1) * pct / 100
    low = math.floor(rank)
    high = math.ceil(rank)
    if low == high:
        return round(ordered[int(rank)], 2)
    value = ordered[low] + (ordered[high] - ordered[low]) * (rank - low)
    return round(value, 2)


def distribution(values: list[float | int | None]) -> dict[str, float | None]:
    numeric = [float(v) for v in values if isinstance(v, (int, float))]
    if not numeric:
        return {"median": None, "p25": None, "p75": None, "min": None, "max": None}
    return {
        "median": safe_median(numeric),
        "p25": percentile(numeric, 25),
        "p75": percentile(numeric, 75),
        "min": round(min(numeric), 2),
        "max": round(max(numeric), 2),
    }


def aggregate_metric_dicts(metric_dicts: list[dict[str, Any]]) -> dict[str, dict[str, float | None]]:
    keys = sorted({key for metrics in metric_dicts for key in metrics})
    return {key: distribution([metrics.get(key) for metrics in metric_dicts]) for key in keys}


def is_substantive_caption_metric(metrics: dict[str, Any]) -> bool:
    return float(metrics.get("word_count") or 0) >= 40


def extract_captions(text: str, label: str) -> list[str]:
    if label.lower().startswith("fig"):
        return extract_figure_captions(text)
    source_text = text
    pattern = re.compile(
        rf"^\s*(?:{label}|{label}\.)\s*\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?\s*[\.:]?[^\S\r\n]+(.+?)(?=\n\s*(?:Fig\.?|Figure|Table)\s*\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?|\n\s*(?:References|Appendix|Acknowledg|Declaration|Funding|Data availability)\b|\n\s*\d+(?:\.\d+)*\.?\s+[A-Z]|\n\s*\d+(?:\.\d+)*\.?\s*\n\s*[A-Z]|\Z)",
        re.I | re.S | re.M,
    )
    captions = []
    for match in pattern.finditer(source_text):
        caption = re.sub(r"\s+", " ", match.group(1)).strip()
        if 20 <= len(caption) <= 4000:
            captions.append(caption)
    return captions


def caption_source_text(text: str) -> str:
    marker = "Figure And Table Captions"
    if marker not in text:
        return text
    source = text.split(marker, 1)[1]
    match = re.search(r"\n\s*References\s*(?:\n|$)", source, re.I)
    if match:
        source = source[: match.start()]
    return source


def extract_figure_captions(text: str) -> list[str]:
    source_text = caption_source_text(text)
    pattern = re.compile(
        r"^\s*(?P<label>(?:Fig\.?|Figure)\s*\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?)\s*(?:[\.:]\s+|-\s+)(?P<caption>.+?)(?=\n\s*(?:Fig\.?|Figure|Table)\s*\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?|\n\s*(?:References|Appendix|Acknowledg|Declaration|Funding|Data availability)\b|\n\s*\d+(?:\.\d+)*\.?\s+[A-Z]|\n\s*\d+(?:\.\d+)*\.?\s*\n\s*[A-Z]|\Z)",
        re.I | re.S | re.M,
    )
    captions: list[str] = []
    for match in pattern.finditer(source_text):
        label = normalize_figure_label(match.group("label"))
        caption = re.sub(r"\s+", " ", match.group("caption")).strip()
        if not caption or len(caption) > 4000:
            continue
        expanded = expand_figure_caption(text, label, caption)
        if 10 <= len(expanded) <= 5000:
            captions.append(expanded)
    return captions


def normalize_figure_label(label: str) -> str:
    match = re.search(r"(?:Fig\.?|Figure)\s*(\d+[A-Za-z]?)(?:\s*\(([A-Za-z0-9]+)\))?", label, re.I)
    if not match:
        return label.strip()
    number = match.group(1)
    panel = f"({match.group(2)})" if match.group(2) else ""
    return f"Fig. {number}{panel}"


def figure_label_number(label: str) -> str:
    match = re.search(r"\d+[A-Za-z]?", label)
    return match.group(0) if match else ""


def expand_figure_caption(text: str, label: str, caption: str) -> str:
    caption = re.sub(r"\s+", " ", caption).strip()
    if len(word_tokens(caption)) >= 50:
        return caption
    combined = caption
    for sentence in figure_reference_context_sentences(text, label):
        if sentence.lower() in combined.lower():
            continue
        candidate = f"{combined} {sentence}".strip()
        if len(word_tokens(candidate)) > 180:
            continue
        combined = candidate
        if len(word_tokens(combined)) >= 55 and len(sentence_split(combined)) >= 2:
            break
    return combined


def figure_reference_context_sentences(text: str, label: str, max_sentences: int = 4) -> list[str]:
    number = figure_label_number(label)
    if not number:
        return []
    body_text = text.split("Figure And Table Captions", 1)[0]
    ref_pattern = re.compile(
        rf"\b(?:Fig\.?|Figure)\s*{re.escape(number)}(?![A-Za-z0-9])(?:\s*\([A-Za-z0-9]+\))?",
        re.I,
    )
    candidates: list[str] = []
    for line in body_text.splitlines():
        if re.match(r"^\s*(?:Fig\.?|Figure|Table)\s*\d+", line, re.I):
            continue
        if not ref_pattern.search(line):
            continue
        for sentence in sentence_split(line):
            if not ref_pattern.search(sentence):
                continue
            tokens = word_tokens(sentence)
            if len(tokens) < 8 or len(tokens) > 90:
                continue
            if sentence and sentence[0].islower():
                continue
            if is_boilerplate_line(sentence):
                continue
            candidates.append(re.sub(r"\s+", " ", sentence).strip())
    candidates = sorted(dict.fromkeys(candidates), key=figure_context_score, reverse=True)
    return candidates[:max_sentences]


def figure_context_score(sentence: str) -> int:
    lower = sentence.lower()
    score = 0
    if re.search(r"\b(show|indicate|illustrate|demonstrate|reveal|compare|present|depict|summarize|summarise)\w*\b", lower):
        score += 3
    if re.search(r"\b(performance|forecast|prediction|error|accuracy|uncertainty|distribution|comparison)\b", lower):
        score += 2
    if re.search(r"\d", sentence):
        score += 1
    return score


def extract_table_header_candidates(text: str, window_lines: int = 10) -> list[str]:
    lines = [line.strip() for line in text.splitlines()]
    candidates: list[str] = []
    for idx, line in enumerate(lines):
        if not re.match(r"^Table\s+\d+", line, re.I):
            continue
        for follow in lines[idx + 1 : idx + 1 + window_lines]:
            cleaned = re.sub(r"\s+", " ", follow).strip()
            if not cleaned or len(cleaned) < 8 or len(cleaned) > 160:
                continue
            if re.match(r"^(Fig\.?|Figure|Table|References|\d+\.?\s+[A-Z])\b", cleaned, re.I):
                break
            token_count = len(word_tokens(cleaned))
            has_header_signal = bool(re.search(r"\b(unit|value|mean|std|error|mae|rmse|mape|r2|scenario|case|model|method|dataset|parameter)\b", cleaned, re.I))
            has_compact_columns = bool(re.search(r"\s{2,}|[/()]", follow))
            if token_count >= 3 and (has_header_signal or has_compact_columns):
                candidates.append(cleaned)
    return candidates[:200]


def abstract_moves(text: str) -> dict[str, bool]:
    sentences = sentence_split(text)
    move_hits = {name: False for name in ABSTRACT_MOVE_PATTERNS}
    for sentence in sentences:
        for name, pattern in ABSTRACT_MOVE_PATTERNS.items():
            if pattern.search(sentence):
                move_hits[name] = True
    return move_hits


def document_metrics(doc: PdfDocument) -> dict[str, Any]:
    sections = split_sections(doc.text)
    section_metrics = {name: basic_metrics(body) for name, body in sections.items()}
    figure_captions = extract_captions(doc.text, "Fig(?:ure)?")
    table_captions = extract_captions(doc.text, "Table")
    abstract = sections.get("abstract", "")
    return {
        "path": str(doc.path),
        "page_count": doc.page_count,
        "word_count": len(word_tokens(doc.text)),
        "sections_detected": list(sections.keys()),
        "section_metrics": section_metrics,
        "abstract_moves": abstract_moves(abstract),
        "figure_caption_metrics": [basic_metrics(caption) for caption in figure_captions],
        "table_caption_metrics": [basic_metrics(caption) for caption in table_captions],
        "figure_caption_count": len(figure_captions),
        "table_caption_count": len(table_captions),
    }


def build_profile(
    docs: list[PdfDocument],
    journal: str,
    profile_name: str,
    source: str,
    corpus_manifest: str | None = None,
    selection_criteria: dict[str, Any] | None = None,
    min_template_doc_support: int = 5,
) -> dict[str, Any]:
    doc_metrics = [document_metrics(doc) for doc in docs]
    section_texts: dict[str, list[str]] = defaultdict(list)
    figure_captions_raw: list[str] = []
    table_captions_raw: list[str] = []
    table_header_lines_raw: list[str] = []
    document_sections_by_doc: list[dict[str, str]] = []
    figure_captions_by_doc: list[list[str]] = []
    table_captions_by_doc: list[list[str]] = []
    table_header_lines_by_doc: list[list[str]] = []
    for doc in docs:
        sections = split_sections(doc.text)
        document_sections_by_doc.append(sections)
        for name, body in sections.items():
            section_texts[name].append(body)
        doc_figure_captions = extract_captions(doc.text, "Fig(?:ure)?")
        doc_table_captions = extract_captions(doc.text, "Table")
        doc_table_headers = extract_table_header_candidates(doc.text)
        figure_captions_raw.extend(doc_figure_captions)
        table_captions_raw.extend(doc_table_captions)
        table_header_lines_raw.extend(doc_table_headers)
        figure_captions_by_doc.append(doc_figure_captions)
        table_captions_by_doc.append(doc_table_captions)
        table_header_lines_by_doc.append(doc_table_headers)
    article_count = len(doc_metrics)
    section_presence = Counter()
    section_orders = []
    section_metric_buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for metrics in doc_metrics:
        detected = metrics["sections_detected"]
        section_orders.append([name for name in SECTION_ORDER if name in detected])
        for section in detected:
            section_presence[section] += 1
        for section, values in metrics["section_metrics"].items():
            section_metric_buckets[section].append(values)

    abstract_metrics = [
        metrics["section_metrics"]["abstract"]
        for metrics in doc_metrics
        if "abstract" in metrics["section_metrics"]
    ]
    introduction_metrics = [
        metrics["section_metrics"]["introduction"]
        for metrics in doc_metrics
        if "introduction" in metrics["section_metrics"]
    ]
    rd_metrics = []
    for metrics in doc_metrics:
        for key in ("results", "discussion", "results_discussion"):
            if key in metrics["section_metrics"]:
                rd_metrics.append(metrics["section_metrics"][key])

    figure_caption_metrics = [
        caption
        for metrics in doc_metrics
        for caption in metrics["figure_caption_metrics"]
    ]
    substantive_figure_caption_metrics = [
        metrics
        for metrics in figure_caption_metrics
        if is_substantive_caption_metric(metrics)
    ]
    table_caption_metrics = [
        caption
        for metrics in doc_metrics
        for caption in metrics["table_caption_metrics"]
    ]

    move_counts = {
        move: sum(1 for metrics in doc_metrics if metrics["abstract_moves"].get(move))
        for move in ABSTRACT_MOVE_PATTERNS
    }
    years = infer_years(docs)
    profile_strength = strength_from_count(article_count)
    section_metric_summary = {
        section: aggregate_metric_dicts(values)
        for section, values in section_metric_buckets.items()
    }
    return {
        "schema_version": "1.3",
        "profile_name": profile_name,
        "journal": journal,
        "created_utc": utc_now(),
        "profile_strength": profile_strength,
        "corpus": {
            "source": source,
            "article_count": article_count,
            "pdf_count": len(docs),
            "years": years,
            "manifest": corpus_manifest,
            "selection_criteria": selection_criteria or {},
            "language_pattern_settings": {
                "min_template_doc_support": min_template_doc_support,
            },
            "documents": [
                {
                    "path": str(doc.path),
                    "page_count": doc.page_count,
                    "title": safe_label(doc.metadata.get("title")),
                    "word_count": len(word_tokens(doc.text)),
                }
                for doc in docs
            ],
        },
        "sections": {
            "common_order": most_common_order(section_orders),
            "presence": {
                section: {
                    "count": count,
                    "share": round(count / article_count, 3) if article_count else 0,
                }
                for section, count in section_presence.items()
            },
            "metrics": section_metric_summary,
        },
        "abstract": {
            "metrics": aggregate_metric_dicts(abstract_metrics),
            "move_presence": {
                move: {
                    "count": count,
                    "share": round(count / article_count, 3) if article_count else 0,
                }
                for move, count in move_counts.items()
            },
            "synthetic_template": "Context. Gap. Method. Quantified result. Operational implication.",
        },
        "introduction": {
            "metrics": aggregate_metric_dicts(introduction_metrics),
            "recommended_moves": [
                "energy-system context",
                "field practice or methodological gap",
                "why the gap matters operationally",
                "proposed contribution",
                "evidence design preview",
            ],
        },
        "results_discussion": {
            "metrics": aggregate_metric_dicts(rd_metrics),
            "recommended_moves": [
                "claim-first result sentence",
                "quantified comparison with metric and unit",
                "uncertainty or support statement",
                "operational interpretation",
                "boundary or limitation when needed",
            ],
        },
        "figures": {
            "figures_per_article": distribution([m["figure_caption_count"] for m in doc_metrics]),
            "tables_per_article": distribution([m["table_caption_count"] for m in doc_metrics]),
            "figure_caption_metrics": aggregate_metric_dicts(substantive_figure_caption_metrics or figure_caption_metrics),
            "figure_caption_all_metrics": aggregate_metric_dicts(figure_caption_metrics),
            "table_caption_metrics": aggregate_metric_dicts(table_caption_metrics),
            "panel_label_policy": "Use stable panel labels when a figure contains multiple claims or diagnostics.",
        },
        "language_patterns": build_language_patterns(
            section_texts,
            figure_captions_by_doc,
            table_captions_by_doc,
            table_header_lines_by_doc,
            document_sections_by_doc,
            min_doc_support=min_template_doc_support,
        ),
        "constraints": build_constraints(
            journal,
            profile_strength,
            abstract_metrics,
            substantive_figure_caption_metrics or figure_caption_metrics,
            section_metric_summary,
            selection_criteria or {},
        ),
    }


def build_language_patterns(
    section_texts: dict[str, list[str]],
    figure_captions_by_doc: list[list[str]],
    table_captions_by_doc: list[list[str]],
    table_header_lines_by_doc: list[list[str]],
    document_sections_by_doc: list[dict[str, str]] | None = None,
    min_doc_support: int = 5,
) -> dict[str, Any]:
    focus_sections = [
        "abstract",
        "introduction",
        "methods",
        "case_study",
        "results",
        "discussion",
        "results_discussion",
        "conclusion",
    ]
    by_section = {}
    for section in focus_sections:
        texts = section_texts.get(section, [])
        if not texts:
            continue
        by_section[section] = {
            "sentence_starters": top_sentence_starters(texts, min_doc_support=min_doc_support),
            "move_starters": move_starters(texts, min_doc_support=min_doc_support),
            "move_sentence_templates": move_sentence_templates(texts, min_doc_support=min_doc_support),
            "bigrams": top_ngrams(texts, 2),
            "trigrams": top_ngrams(texts, 3),
            "verb_preferences": top_verbs(texts),
            "hedging_and_degree_terms": top_terms(texts, HEDGE_TERMS | DEGREE_TERMS),
        }
    return {
        "settings": {"min_template_doc_support": min_doc_support},
        "by_section": by_section,
        "numeric_reporting": numeric_reporting_patterns(section_texts, min_doc_support=min_doc_support),
        "comparison_language": comparison_language_patterns(section_texts, min_doc_support=min_doc_support),
        "figure_caption_patterns": caption_patterns(figure_captions_by_doc, min_doc_support=min_doc_support),
        "table_caption_patterns": caption_patterns(table_captions_by_doc, min_doc_support=min_doc_support),
        "table_header_patterns": table_header_patterns(table_header_lines_by_doc, min_doc_support=min_doc_support),
        "figure_reference_patterns": figure_reference_patterns(
            section_texts,
            min_doc_support=min_doc_support,
            document_sections_by_doc=document_sections_by_doc,
        ),
        "paragraph_flow_templates": paragraph_flow_templates(section_texts),
        "introduction_arc_patterns": introduction_arc_patterns(section_texts.get("introduction", [])),
        "conclusion_closing_patterns": conclusion_closing_patterns(
            section_texts.get("conclusion", []),
            min_doc_support=min_doc_support,
        ),
    }


def top_sentence_starters(texts: list[str], limit: int = 12, min_doc_support: int = 5) -> list[dict[str, Any]]:
    doc_patterns = []
    for text in texts:
        patterns = [reusable_sentence_starter(sentence) for sentence in style_sentences_from_text(text)]
        doc_patterns.append([pattern for pattern in patterns if pattern])
    return document_supported_records(doc_patterns, limit, min_doc_support)


def move_starters(texts: list[str], limit: int = 6, min_doc_support: int = 5) -> dict[str, list[dict[str, Any]]]:
    doc_buckets: dict[str, list[list[str]]] = {name: [] for name in MOVE_PATTERNS}
    for text in texts:
        per_doc: dict[str, list[str]] = {name: [] for name in MOVE_PATTERNS}
        for sentence in style_sentences_from_text(text):
            move = dominant_move(sentence)
            if move not in per_doc:
                continue
            starter = reusable_sentence_starter(sentence, move)
            if starter:
                per_doc[move].append(starter)
        for move, values in per_doc.items():
            doc_buckets[move].append(values)
    return {
        name: document_supported_records(values, limit, min_doc_support)
        for name, values in doc_buckets.items()
        if document_supported_records(values, limit, min_doc_support)
    }


def move_sentence_templates(texts: list[str], limit: int = 5, min_doc_support: int = 5) -> dict[str, list[dict[str, Any]]]:
    doc_buckets: dict[str, list[list[str]]] = {name: [] for name in MOVE_PATTERNS}
    for text in texts:
        per_doc: dict[str, list[str]] = {name: [] for name in MOVE_PATTERNS}
        for sentence in style_sentences_from_text(text):
            move = dominant_move(sentence)
            if move not in per_doc:
                continue
            template = structural_sentence_template(sentence, move)
            if template:
                per_doc[move].append(template)
        for move, values in per_doc.items():
            doc_buckets[move].append(values)
    return {
        name: document_supported_records(values, limit, min_doc_support)
        for name, values in doc_buckets.items()
        if document_supported_records(values, limit, min_doc_support)
    }


def top_ngrams(texts: list[str], n: int, limit: int = 20) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    for text in all_sentences(texts):
        tokens = [
            token.lower()
            for token in word_tokens(text)
            if token.isalpha() and len(token) > 2 and token.lower() not in STOPWORDS
        ]
        for idx in range(0, max(len(tokens) - n + 1, 0)):
            gram = tokens[idx : idx + n]
            if any(token in STOPWORDS for token in gram):
                continue
            if len(set(gram)) == 1:
                continue
            if any(token in {"writing", "editing", "draft"} for token in gram):
                continue
            counter[" ".join(gram)] += 1
    return counter_records(counter, limit)


def top_verbs(texts: list[str], limit: int = 20) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    for sentence in all_sentences(texts):
        for token in word_tokens(sentence):
            base = verb_base(token.lower())
            if base in RESEARCH_VERBS:
                counter[base] += 1
    return counter_records(counter, limit)


def top_terms(texts: list[str], terms: set[str], limit: int = 20) -> list[dict[str, Any]]:
    counter: Counter[str] = Counter()
    combined = "\n".join(all_sentences(texts)).lower()
    for term in terms:
        count = len(re.findall(r"\b" + re.escape(term.lower()) + r"\b", combined))
        if count:
            counter[term] = count
    return counter_records(counter, limit)


def numeric_reporting_patterns(section_texts: dict[str, list[str]], min_doc_support: int = 5) -> dict[str, Any]:
    patterns: Counter[str] = Counter()
    template_docs: list[list[str]] = []
    by_section: dict[str, Counter[str]] = defaultdict(Counter)
    units: Counter[str] = Counter()
    unit_doc_templates: dict[str, list[list[str]]] = defaultdict(list)
    uncertainty: Counter[str] = Counter()
    focus = ["abstract", "results", "discussion", "results_discussion"]
    for section in focus:
        for text in section_texts.get(section, []):
            doc_templates: list[str] = []
            doc_unit_templates: dict[str, list[str]] = defaultdict(list)
            for sentence in style_sentences_from_text(text):
                if not re.search(r"\d", sentence):
                    continue
                pattern = classify_numeric_sentence(sentence)
                patterns[pattern] += 1
                by_section[section][pattern] += 1
                template = structural_numeric_template(sentence)
                if template:
                    doc_templates.append(template)
                unit_matches = re.findall(
                    r"\b\d+(?:\.\d+)?\s*(MW|GW|kW|kWh|MWh|GWh|%|h|s|min|kg|ton|USD|EUR)(?=\b|[^A-Za-z])",
                    sentence,
                    re.I,
                )
                for unit in unit_matches:
                    units[unit] += 1
                    unit_template = unit_context_template(sentence, unit) or template
                    if unit_template:
                        doc_unit_templates[unit].append(unit_template)
                for phrase in uncertainty_phrases(sentence):
                    uncertainty[phrase] += 1
            template_docs.append(doc_templates)
            for unit, values in doc_unit_templates.items():
                unit_doc_templates[unit].append(values)
    return {
        "format_types": counter_records(patterns, 20),
        "short_templates": document_supported_records(template_docs, 20, min_doc_support),
        "units": counter_records(units, 20),
        "unit_context_templates": {
            unit: document_supported_records(values, 5, min_doc_support)
            for unit, values in unit_doc_templates.items()
        },
        "uncertainty_expressions": counter_records(uncertainty, 20),
        "by_section": {section: counter_records(counter, 10) for section, counter in by_section.items()},
    }


def unit_context_template(sentence: str, unit: str) -> str:
    lower = normalize_template_tokens(sentence).lower()
    lower = normalize_metric_terms(lower)
    unit_lower = unit.lower()
    if unit_lower == "%":
        if re.search(r"\b(improv\w*|reduc\w*|decreas\w*|increas\w*)\s+by\s+<percent>", lower):
            return "<quantity_or_metric> changes by <percent>"
        if re.search(r"\b(error|<metric>|accuracy|coverage|share|ratio)\b", lower):
            return "<metric_or_share> is reported as <percent>"
        return "<percentage_value> is reported for <metric_or_case>"
    if unit_lower in {"h", "hour", "hours"}:
        if re.search(r"\b(horizon|lead time|ahead|look-ahead|forecasting step)\b", lower):
            return "<forecast_horizon> is reported as <num> h"
        if re.search(r"\b(interval|resolution|sampling|time step)\b", lower):
            return "<time_resolution> is reported as <num> h"
        return "<time_context> is reported as <num> h"
    if unit_lower in {"mw", "gw", "kw"}:
        return "<power_value> is reported in <power_unit>"
    if unit_lower in {"kwh", "mwh", "gwh"}:
        return "<energy_value> is reported in <energy_unit>"
    return ""


def comparison_language_patterns(section_texts: dict[str, list[str]], min_doc_support: int = 5) -> dict[str, Any]:
    doc_templates: list[list[str]] = []
    verbs: Counter[str] = Counter()
    for section in ["results", "discussion", "results_discussion", "abstract"]:
        for text in section_texts.get(section, []):
            per_doc = []
            for sentence in style_sentences_from_text(text):
                template = comparison_template(sentence)
                if not template:
                    continue
                per_doc.append(template)
                for verb in COMPARISON_VERBS:
                    if re.search(r"\b" + re.escape(verb) + r"\w*\b", sentence, re.I):
                        verbs[verb] += 1
            doc_templates.append(per_doc)
    return {
        "templates": document_supported_records(doc_templates, 20, min_doc_support),
        "verbs": counter_records(verbs, 20),
    }


def caption_patterns(captions_by_doc: list[list[str]], min_doc_support: int = 5) -> dict[str, Any]:
    starter_docs: list[list[str]] = []
    raw_starter_docs: list[list[str]] = []
    structures: Counter[str] = Counter()
    syntax: Counter[str] = Counter()
    topic_docs: dict[str, list[list[str]]] = defaultdict(list)
    for captions in captions_by_doc:
        doc_starters = []
        doc_raw_starters = []
        per_topic: dict[str, list[str]] = defaultdict(list)
        for caption in captions:
            sentences = sentence_split(caption)
            if not sentences:
                continue
            starter = caption_opening_template(sentences[0]) or sentence_starter(sentences[0], max_tokens=8)
            raw_starter = sentence_starter(sentences[0], max_tokens=8)
            opening_type = classify_caption(sentences[0])
            if starter:
                doc_starters.append(starter)
                per_topic[opening_type].append(starter)
            if raw_starter:
                doc_raw_starters.append(raw_starter)
            structures[opening_type] += 1
            syntax[caption_syntax_pattern(sentences)] += 1
        starter_docs.append(doc_starters)
        raw_starter_docs.append(doc_raw_starters)
        for topic, starters in per_topic.items():
            topic_docs[topic].append(starters)
    return {
        "opening_starters": document_supported_records(starter_docs, 20, min_doc_support),
        "raw_opening_starters": document_supported_records(raw_starter_docs, 20, min_doc_support),
        "opening_types": counter_records(structures, 20),
        "syntax_patterns": counter_records(syntax, 20),
        "topic_to_starters": {
            topic: document_supported_records(patterns, 8, min_doc_support)
            for topic, patterns in topic_docs.items()
        },
    }


def figure_reference_patterns(
    section_texts: dict[str, list[str]],
    min_doc_support: int = 5,
    document_sections_by_doc: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    doc_templates: list[list[str]] = []
    reference_sections = [
        "introduction",
        "related_work",
        "methods",
        "case_study",
        "results",
        "discussion",
        "results_discussion",
        "conclusion",
    ]
    if document_sections_by_doc is not None:
        for sections in document_sections_by_doc:
            templates = []
            for section in reference_sections:
                text = sections.get(section, "")
                if not text:
                    continue
                for snippet in figure_reference_snippets(text):
                    template = classify_figure_reference(snippet)
                    if template:
                        templates.append(template)
            doc_templates.append(templates)
        return {"sentence_templates": document_supported_records(doc_templates, 20, min_doc_support)}
    for section in reference_sections:
        for text in section_texts.get(section, []):
            templates = []
            for snippet in figure_reference_snippets(text):
                template = classify_figure_reference(snippet)
                if template:
                    templates.append(template)
            doc_templates.append(templates)
    return {"sentence_templates": document_supported_records(doc_templates, 20, min_doc_support)}


def figure_reference_snippets(text: str) -> list[str]:
    snippets: list[str] = []
    ref_pattern = re.compile(r"\b(Fig\.|Figure)\s*\d+[A-Za-z]?(?:\([A-Za-z0-9]+\))?", re.I)
    for line in text.splitlines():
        if re.match(r"^\s*(Fig\.?|Figure)\s*\d+", line, re.I):
            continue
        if not ref_pattern.search(line):
            continue
        candidates = sentence_split(line)
        if not candidates:
            candidates = [line]
        for candidate in candidates:
            if ref_pattern.search(candidate):
                if len(word_tokens(candidate)) > 90:
                    for match in ref_pattern.finditer(candidate):
                        template = normalize_figure_reference(candidate[max(0, match.start() - 120) : match.end() + 160])
                        if template:
                            snippets.append(template)
                else:
                    snippet = re.sub(r"\s+", " ", candidate).strip()
                    if snippet:
                        snippets.append(snippet)
    return snippets


def paragraph_flow_templates(section_texts: dict[str, list[str]]) -> dict[str, Any]:
    out = {}
    for section in ["introduction", "methods", "results", "discussion", "results_discussion", "conclusion"]:
        flows: Counter[str] = Counter()
        for text in section_texts.get(section, []):
            for paragraph in paragraph_split(text):
                sentences = style_sentences_from_text(paragraph)
                if len(sentences) < 2:
                    continue
                labels = [dominant_move(sentence) for sentence in sentences[:4]]
                flows[" > ".join(labels)] += 1
        if flows:
            out[section] = counter_records(flows, 10)
    return out


def introduction_arc_patterns(texts: list[str]) -> dict[str, Any]:
    paragraph_position_starters: dict[str, Counter[str]] = defaultdict(Counter)
    paragraph_position_moves: dict[str, Counter[str]] = defaultdict(Counter)
    arc_counter: Counter[str] = Counter()
    transition_counter: Counter[str] = Counter()
    for text in texts:
        arc_labels = []
        style_pos = 0
        for idx, paragraph in enumerate(paragraph_split(text)[:7]):
            sentences = style_sentences_from_text(paragraph)
            if not sentences:
                continue
            first = sentences[0]
            label = dominant_move(first)
            arc_labels.append(label)
            slot = f"paragraph_{style_pos + 1}"
            starter = sentence_starter(first, max_tokens=10)
            if starter:
                paragraph_position_starters[slot][starter] += 1
                if style_pos > 0:
                    transition_counter[starter] += 1
            paragraph_position_moves[slot][label] += 1
            style_pos += 1
        if arc_labels:
            arc_counter[" > ".join(arc_labels[:7])] += 1
    return {
        "paragraph_position_starters": {
            slot: counter_records(counter, 5)
            for slot, counter in paragraph_position_starters.items()
        },
        "paragraph_position_moves": {
            slot: counter_records(counter, 5)
            for slot, counter in paragraph_position_moves.items()
        },
        "arc_sequences": counter_records(arc_counter, 10),
        "transition_starters": counter_records(transition_counter, 15),
    }


def conclusion_closing_patterns(texts: list[str], min_doc_support: int = 5) -> dict[str, Any]:
    opening_docs: list[list[str]] = []
    closing_docs: list[list[str]] = []
    closing_moves: Counter[str] = Counter()
    for text in texts:
        doc_openings = []
        doc_closings = []
        paragraphs = [paragraph for paragraph in paragraph_split(text) if style_sentences_from_text(paragraph)]
        if paragraphs:
            first_sentences = style_sentences_from_text(paragraphs[0])
            last_sentences = style_sentences_from_text(paragraphs[-1])
            if first_sentences:
                opening = reusable_sentence_starter(first_sentences[0])
                if opening:
                    doc_openings.append(opening)
            if last_sentences:
                closing_sentence = last_sentences[-1]
                closing = reusable_sentence_starter(closing_sentence)
                if closing:
                    doc_closings.append(closing)
                closing_moves[dominant_move(closing_sentence)] += 1
        opening_docs.append(doc_openings)
        closing_docs.append(doc_closings)
    return {
        "opening_starters": document_supported_records(opening_docs, 12, min_doc_support),
        "closing_starters": document_supported_records(closing_docs, 12, min_doc_support),
        "closing_moves": counter_records(closing_moves, 8),
    }


def all_sentences(texts: list[str]) -> list[str]:
    sentences: list[str] = []
    for text in texts:
        sentences.extend(style_sentences_from_text(text))
    return sentences


def style_sentences_from_text(text: str) -> list[str]:
    return [sentence for sentence in sentence_split(text) if is_style_sentence(sentence)]


def is_style_sentence(sentence: str) -> bool:
    tokens = word_tokens(sentence)
    if len(tokens) < 6 or len(tokens) > 90:
        return False
    lower = sentence.lower()
    if is_boilerplate_line(sentence):
        return False
    if re.search(r"writing\W+review\W+editing|writing\W+original\W+draft", lower):
        return False
    if re.search(r"ai-assisted technologies|all changes by the ai", lower):
        return False
    if re.search(r"https?://|www\.|\bcom\b", lower):
        return False
    if re.match(r"^applied energy\s+\d+", lower):
        return False
    if re.search(r"\b(appl\.?\s+energy|renewable sustainable energy reviews|energy buildings|energy build\.?|ieee trans|sustainable cities and society|energy conversion and management)\b", lower) and re.search(r"\b\d{2,}\b", lower):
        return False
    if re.search(r"\brefs?\b", lower):
        return False
    if len(re.findall(r"\b20\d{2}\b", sentence)) >= 2 and re.search(r"\b[A-Z][A-Za-z\-]+,\s+[A-Z]\.", sentence):
        return False
    if re.match(r"^[A-Z][A-Za-z\-]+,\s+[A-Z]\.", sentence) and re.search(r"\b\d{3,}\b", sentence):
        return False
    return True


def is_boilerplate_line(text: str) -> bool:
    lower = text.lower()
    if any(phrase in lower for phrase in BOILERPLATE_PHRASES):
        return True
    if re.search(r"\bfunding\W+(this research|was|statement|acquisition)|\backnowledg(e)?ments?\b", lower):
        return True
    if re.search(r"https?://|www\.|\bcom\b", lower):
        return True
    return False


def sentence_starter(sentence: str, max_tokens: int = 10) -> str:
    tokens = []
    for token in word_tokens(sentence):
        clean = token.lower()
        if re.search(r"\d", clean):
            clean = "<num>"
        tokens.append(clean)
        if len(tokens) >= max_tokens:
            break
    if len(tokens) < 3:
        return ""
    return " ".join(tokens)


def reusable_sentence_starter(sentence: str, move: str | None = None) -> str:
    label = move or dominant_move(sentence)
    template = structural_sentence_template(sentence, label)
    if template:
        return template
    lower = normalize_template_tokens(sentence).lower()
    if label == "context" and re.search(r"\bin recent years\b", lower):
        return "in recent years, <field_context> has <trend_or_change>"
    if label == "context" and re.search(r"\bwind (power|speed|energy)\b", lower) and re.search(r"\bforecast|predict", lower):
        return "wind <target_variable> forecasting is important for <power_system_operation>"
    if label == "context" and re.search(r"\bthe increasing\b", lower) and re.search(r"\brenewable|wind|power\b", lower):
        return "the increasing <renewable_energy_context> creates <operational_need>"
    if re.search(r"\bto address\b", lower):
        return "to address <gap>, <method_or_framework> is proposed"
    return sentence_starter(sentence)


def structural_sentence_template(sentence: str, move: str) -> str:
    lower = normalize_template_tokens(sentence).lower()
    lower = normalize_metric_terms(lower)
    comparison = comparison_template(lower)
    if comparison and move in {"result", "implication"}:
        return comparison
    numeric = structural_numeric_template(lower)
    if numeric and move == "result":
        return numeric
    if move == "result":
        if re.search(r"<fig>\s+(shows|presents|illustrates|depicts|reports|compares|summarizes|summarises)", lower):
            return "<fig> <shows_or_compares> <result_or_setup>"
        if re.search(r"\bresults?\s+(show|shows|indicate|indicates|suggest|suggests|demonstrate|demonstrates|reveal|reveals)\b", lower):
            return "the results <show_or_indicate> <main_finding>"
        if re.search(r"\bthe proposed (model|method|framework|approach)\b", lower) and re.search(r"\b(outperform|improv|reduc|achiev|show|demonstrat)\w*\b", lower):
            return "the proposed <method> <improves_or_reports> <performance_metric>"
        if re.search(r"\bforecasting performance\b", lower) and re.search(r"\b(show|improv|evaluat|compar)\w*\b", lower):
            return "<forecasting_performance> is <reported_or_compared> across <methods_or_cases>"
        if re.search(r"\b(show|indicate|demonstrate|reveal|confirm)\w*\b", lower):
            return "<result_evidence> shows <finding_or_pattern>"
        if re.search(r"\bperformance\b", lower) and "<metric>" in lower:
            return "<method_performance> is evaluated using <metric>"
    if move == "gap":
        if re.search(r"\bhowever\b", lower):
            return "however, <gap_statement>"
        if re.search(r"\bdespite\b", lower):
            return "despite <prior_work_or_condition>, <gap_statement>"
        if re.search(r"\balthough\b", lower):
            return "although <prior_work_or_condition>, <gap_statement>"
        if re.search(r"\bremain\w*\b", lower):
            return "<challenge_or_uncertainty> remains <gap_state>"
        if re.search(r"\blimited|lack|challenge|uncertain\b", lower):
            return "<existing_work_or_system> is limited by <gap_or_uncertainty>"
    if move == "method":
        if re.search(r"\bwe\s+(propose|develop|present|introduce|formulate)\b", lower):
            verb = re.search(r"\bwe\s+(propose|develop|present|introduce|formulate)\b", lower).group(1)
            return f"we {verb} <method_or_framework> for <forecasting_task>"
        if re.search(r"\bthis (paper|study)\s+(proposes|develops|presents|introduces|formulates)\b", lower):
            return "this study <method_verb> <method_or_framework> for <forecasting_task>"
        if re.search(r"\bin this (paper|study)\b", lower):
            return "in this study, <method_or_experiment> is <described_or_evaluated>"
        if re.search(r"\bmodel|framework|approach|method\b", lower):
            return "<method_or_framework> is used to <forecast_or_evaluate> <target_variable>"
    if move == "context":
        if re.search(r"\bwind (power|energy|speed|farm|generation)\b", lower) and re.search(r"\bforecast|predict", lower):
            return "wind <target_variable> forecasting is important for <power_system_operation>"
        if re.search(r"\brenewable energy|power system|grid\b", lower):
            return "<renewable_energy_context> creates <operational_need_or_challenge>"
    if move == "implication":
        if re.search(r"\bwhich\s+(indicates|suggests|demonstrates|shows)\b", lower):
            return "<finding>, which <indicates_or_suggests> <interpretation>"
        if re.search(r"\b(indicating|suggesting|demonstrating|showing)\s+that\b", lower):
            return "<finding>, <indicating_or_suggesting> that <interpretation>"
        if re.search(r"\bthis\s+(indicates|suggests|demonstrates|shows)\b", lower):
            return "this <indicates_or_suggests> <operational_interpretation>"
        if re.search(r"\bresults?\s+(indicate|suggest|show|demonstrate)\b", lower):
            return "the results <indicate_or_suggest> <operational_implication>"
        if re.search(r"\benable|support|provide\b", lower):
            return "<finding_or_method> can <enable_or_support> <operational_decision>"
    if move == "limitation":
        if re.search(r"\bfuture work|further\b", lower):
            return "future work should <extend_or_validate> <method_or_application>"
        if re.search(r"\blimitation|uncertainty|constraint\b", lower):
            return "<limitation_or_uncertainty> should be considered when <applying_the_method>"
    return ""


def structural_numeric_template(sentence: str) -> str:
    lower = normalize_template_tokens(sentence).lower()
    lower = normalize_metric_terms(lower)
    if re.search(r"\b(improv\w*|reduc\w*|decreas\w*|increas\w*)\s+by\s+<percent>", lower):
        verb = re.search(r"\b(improv\w*|reduc\w*|decreas\w*|increas\w*)\s+by\s+<percent>", lower).group(1)
        return f"<quantity_or_metric> {verb} by <percent>"
    if re.search(r"\bfrom\s+<num>\s+(?:\w+\s+){0,3}to\s+<num>", lower):
        return "<quantity_or_metric> changes from <num> to <num>"
    if re.search(r"\b<metric>\s*(=|of|is|was|reaches|reached)\s*<num>", lower):
        return "<metric> = <num>"
    if re.search(r"\bachiev\w*\s+<num>", lower):
        return "<method_or_system> achieves <num> on <metric_or_target>"
    if re.search(r"\b(mean|average)\s+.*<num>.*(std|standard deviation|confidence interval|ci)", lower):
        return "<metric> is reported with <uncertainty_measure>"
    if re.search(r"\bp\s*[<=>]\s*<num>", lower):
        return "p < <num>"
    if re.search(r"\bconfidence interval|prediction interval|uncertainty interval\b", lower):
        return "<interval_type> is reported for <forecast_or_metric>"
    return ""


def comparison_template(sentence: str) -> str:
    lower = normalize_template_tokens(sentence).lower()
    lower = normalize_metric_terms(lower)
    if re.search(r"\boutperform\w*\b", lower):
        if re.search(r"\bby\s+<percent>", lower):
            return "<method> outperforms <baseline> by <percent> in terms of <metric>"
        return "<method> outperforms <baseline> in terms of <metric>"
    if re.search(r"\b(reduc\w*|decreas\w*)\b", lower) and re.search(r"\bcompared with|compared to|relative to\b", lower):
        if re.search(r"\bby\s+<percent>", lower):
            return "<method> reduces <metric> by <percent> compared with <baseline>"
        return "<method> reduces <metric> compared with <baseline>"
    if re.search(r"\b(improv\w*|increas\w*)\b", lower) and re.search(r"\bcompared with|compared to|relative to\b", lower):
        if re.search(r"\bby\s+<percent>", lower):
            return "<method> improves <metric> by <percent> compared with <baseline>"
        return "<method> improves <metric> compared with <baseline>"
    if re.search(r"\bachiev\w*\b", lower) and "<metric>" in lower:
        return "<method> achieves <metric> of <num>"
    if re.search(r"\bcompared with|compared to|relative to\b", lower):
        return "<method_or_result> is compared with <baseline>"
    return ""


def normalize_metric_terms(text: str) -> str:
    return re.sub(
        r"\b(rmse|mae|mape|nrmse|r2|r\^2|crps|pinaw|picp|accuracy|precision|recall|f1|error|cost|reliability)\b",
        "<metric>",
        text,
        flags=re.I,
    )


def normalized_sentence_template(sentence: str, max_tokens: int = 14) -> str:
    text = normalize_template_tokens(sentence)
    tokens = word_tokens(text)
    if len(tokens) < 5:
        return ""
    return " ".join(tokens[:max_tokens]).lower()


def normalized_numeric_template(sentence: str, max_tokens: int = 18) -> str:
    text = normalize_template_tokens(sentence)
    tokens = word_tokens(text)
    if len(tokens) < 4:
        return ""
    return " ".join(tokens[:max_tokens]).lower()


def normalize_template_tokens(sentence: str) -> str:
    text = re.sub(r"\[(?:\d+[,\-\s]*)+\]", "<cit>", sentence)
    text = re.sub(r"\b(?:Fig\.?|Figure)\s*\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?", "<fig>", text, flags=re.I)
    text = re.sub(r"\bTable\s*\d+[A-Za-z]?(?:\s*\([A-Za-z0-9]+\))?", "<table>", text, flags=re.I)
    text = re.sub(r"\b\d+(?:\.\d+)?\s*%", "<percent>", text)
    text = re.sub(r"\b\d+(?:\.\d+)?\s*(MW|GW|kW|kWh|MWh|GWh|h|s|min|kg|ton|USD|EUR)\b", r"<num> \1", text)
    text = re.sub(r"\b\d+(?:\.\d+)?\b", "<num>", text)
    return text


def classify_numeric_sentence(sentence: str) -> str:
    lower = sentence.lower()
    if re.search(r"\bfrom\s+\d", lower) and re.search(r"\bto\s+\d", lower):
        return "from_to_change"
    if "%" in sentence and re.search(r"\b(improv|reduc|increas|decreas|higher|lower|saving|error)\w*", lower):
        return "percent_change_or_comparison"
    if re.search(r"\b(rmse|mae|mape|r2|r\^2|accuracy|precision|recall|f1|crps|pinaw|picp)\b", lower):
        return "metric_value"
    if re.search(r"\b(ci|confidence interval|p\s*[<=>])\b", lower):
        return "statistical_uncertainty"
    if re.search(r"\d+(?:\.\d+)?\s*(mw|gw|kw|kwh|mwh|gwh)\b", lower):
        return "energy_unit_value"
    if re.search(r"\b(fig\.|figure|table)\s*\d+", lower):
        return "display_reference_with_number"
    return "numeric_context"


def uncertainty_phrases(sentence: str) -> list[str]:
    lower = sentence.lower()
    phrases = []
    checks = [
        ("confidence_interval", r"\b(?:confidence interval|ci)\b"),
        ("p_value", r"\bp\s*[<=>]\s*\d"),
        ("standard_deviation", r"\b(?:standard deviation|std\.?|sd)\b"),
        ("error_bar", r"\berror bars?\b"),
        ("interquartile_range", r"\b(?:interquartile range|iqr)\b"),
        ("uncertainty_interval", r"\buncertainty interval\b"),
        ("prediction_interval", r"\bprediction interval\b"),
    ]
    for label, pattern in checks:
        if re.search(pattern, lower):
            phrases.append(label)
    return phrases


def classify_caption(sentence: str) -> str:
    lower = sentence.lower()
    if lower.startswith(("comparison", "comparisons")):
        return "comparison_caption"
    if lower.startswith(("effect", "effects", "impact", "impacts")):
        return "effect_or_impact_caption"
    if lower.startswith(("performance", "prediction", "forecast")):
        return "performance_or_prediction_caption"
    if lower.startswith(("distribution", "probability", "uncertainty")):
        return "distribution_or_uncertainty_caption"
    if lower.startswith(("schematic", "framework", "workflow", "structure")):
        return "framework_caption"
    if re.search(r"\b(spatial|temporal|seasonal|daily|hourly)\b", lower):
        return "time_or_space_caption"
    return "descriptive_caption"


def caption_opening_template(sentence: str) -> str:
    lower = normalize_template_tokens(sentence).lower()
    lower = normalize_metric_terms(lower)
    if re.match(r"^(comparison|comparisons)\s+of\b", lower):
        return "comparison of <methods_or_results>"
    if re.match(r"^(performance|prediction|forecasting|forecast)\b", lower):
        return "<forecast_or_performance> of <method_or_target>"
    if re.search(r"\bwind (power|speed|energy|farm)\b", lower) and re.search(r"\bforecast|predict", lower):
        return "wind <target_variable> forecasting <result_or_setup>"
    if re.search(r"\bproposed (model|method|framework|approach)\b", lower):
        return "<proposed_method> <figure_content>"
    if re.search(r"\b(framework|structure|architecture|workflow|flowchart|schematic)\b", lower):
        return "<method_framework_or_architecture>"
    if re.search(r"\b(distribution|probability|interval|uncertainty)\b", lower):
        return "<distribution_or_uncertainty> of <target_variable>"
    if re.search(r"\b(error|<metric>|accuracy|performance)\b", lower):
        return "<performance_metric_or_error> under <case_or_method>"
    if re.search(r"\b(spatial|temporal|seasonal|daily|hourly)\b", lower):
        return "<temporal_or_spatial_pattern> of <target_variable>"
    if re.search(r"\b(data|dataset|sample|case study|study area)\b", lower):
        return "<data_or_case_study> description"
    return ""


def caption_syntax_pattern(sentences: list[str]) -> str:
    labels = []
    for idx, sentence in enumerate(sentences[:3]):
        lower = sentence.lower()
        if idx == 0:
            labels.append(classify_caption(sentence))
        elif re.search(r"\b(show|indicate|suggest|demonstrate|reveal|confirm)\w*\b", lower):
            labels.append("interpretation")
        elif re.search(r"\d", sentence):
            labels.append("quantified_detail")
        elif re.search(r"\b(a|b|c|d)\)", lower):
            labels.append("panel_definition")
        else:
            labels.append("scope_or_condition")
    if len(labels) == 1:
        return "single_sentence:" + labels[0]
    return " > ".join(labels)


def table_header_patterns(header_lines_by_doc: list[list[str]], min_doc_support: int = 5) -> dict[str, Any]:
    starter_docs: list[list[str]] = []
    term_counter: Counter[str] = Counter()
    shape_counter: Counter[str] = Counter()
    for header_lines in header_lines_by_doc:
        doc_starters = []
        for line in header_lines:
            if is_boilerplate_line(line):
                continue
            starter = sentence_starter(line, max_tokens=8)
            if starter:
                doc_starters.append(starter)
            for token in word_tokens(line):
                lower = token.lower()
                if lower in STOPWORDS or len(lower) <= 2 or re.search(r"\d", lower):
                    continue
                term_counter[lower] += 1
            shape_counter[classify_table_header(line)] += 1
        starter_docs.append(doc_starters)
    return {
        "line_starters": document_supported_records(starter_docs, 20, min_doc_support),
        "header_terms": counter_records(term_counter, 30),
        "header_shapes": counter_records(shape_counter, 10),
    }


def classify_table_header(line: str) -> str:
    lower = line.lower()
    has_metric = bool(re.search(r"\b(mae|rmse|mape|r2|error|accuracy|cost|power|energy|emission)\b", lower))
    has_unit = bool(re.search(r"\((?:mw|gw|kw|kwh|mwh|gwh|%|h|min|s|kg|usd|eur)\)|\b(?:mw|gw|kw|kwh|mwh|gwh|%)\b", lower))
    has_scenario = bool(re.search(r"\b(case|scenario|dataset|site|season|period|model|method)\b", lower))
    if has_metric and has_unit:
        return "metric_with_unit"
    if has_metric and has_scenario:
        return "scenario_metric_matrix"
    if has_scenario:
        return "scenario_or_model_columns"
    if has_unit:
        return "unit_columns"
    return "descriptive_columns"


def classify_figure_reference(sentence: str) -> str:
    lower = normalize_template_tokens(sentence).lower()
    if re.search(r"\bas can be (seen|observed)\s+(from|in)\s+<fig>", lower):
        verb = re.search(r"\bas can be (seen|observed)\s+(from|in)\s+<fig>", lower).group(1)
        return f"as can be {verb} in <fig>"
    if re.search(r"\bit can be (seen|observed)\s+(from|in)\s+<fig>", lower):
        verb = re.search(r"\bit can be (seen|observed)\s+(from|in)\s+<fig>", lower).group(1)
        return f"it can be {verb} from <fig>"
    if re.search(r"\bas (shown|illustrated|presented|depicted|reported) in\s+<fig>", lower):
        verb = re.search(r"\bas (shown|illustrated|presented|depicted|reported) in\s+<fig>", lower).group(1)
        return f"as {verb} in <fig>"
    if re.search(r"\b(shown|illustrated|presented|depicted|reported) in\s+<fig>", lower):
        verb = re.search(r"\b(shown|illustrated|presented|depicted|reported) in\s+<fig>", lower).group(1)
        return f"{verb} in <fig>"
    if re.search(r"<fig>\s+(shows|presents|illustrates|depicts|reports|compares|summarizes|summarises)", lower):
        verb = re.search(r"<fig>\s+(shows|presents|illustrates|depicts|reports|compares|summarizes|summarises)", lower).group(1)
        return f"<fig> {verb} <result_or_setup>"
    if re.search(r"\bsee\s+<fig>", lower):
        return "see <fig>"
    if re.search(r"\baccording to\s+<fig>", lower):
        return "according to <fig>"
    if re.search(r"\(<fig>\)", lower):
        return "(<fig>) parenthetical support"
    if "<fig>" in lower:
        return "<fig> referenced inside explanatory sentence"
    return ""


def normalize_figure_reference(sentence: str) -> str:
    lower = sentence.lower()
    lower = re.sub(r"\b(fig\.|figure)\s*\d+[a-z]?(?:\s*\([a-z0-9]+\))?", "<fig>", lower)
    lower = re.sub(r"\b\d+(?:\.\d+)?\b", "<num>", lower)
    tokens = word_tokens(lower)
    try:
        center = tokens.index("<fig>")
    except ValueError:
        center = 0
    start = max(0, center - 6)
    end = min(len(tokens), center + 10)
    return " ".join(tokens[start:end])


def dominant_move(sentence: str) -> str:
    lower = normalize_metric_terms(normalize_template_tokens(sentence).lower())
    if comparison_template(lower) or (
        re.search(r"\b(result|show|demonstrate|achieve|reduce|increase|improve|outperform|performance|reveal)\w*\b", lower)
        and re.search(r"<metric>|<percent>|<num>|<fig>|\bcompared\b|\bbaseline\b", lower)
    ):
        return "result"
    if MOVE_PATTERNS["implication"].search(sentence) and re.search(
        r"\b(indicate|suggest|enable|provide|support|practical|operational|decision|planning)\w*\b",
        lower,
    ):
        return "implication"
    for move in ["gap", "method", "context", "limitation"]:
        if MOVE_PATTERNS[move].search(sentence):
            return move
    if re.search(r"\[(?:\d+[,\-\s]*)+\]|\bet al\.", sentence):
        return "literature"
    if re.search(r"\d", sentence):
        return "quantitative"
    return "statement"


def verb_base(token: str) -> str:
    for suffix in ["ing", "ed", "es", "s"]:
        if token.endswith(suffix) and len(token) > len(suffix) + 3:
            candidate = token[: -len(suffix)]
            if candidate in RESEARCH_VERBS:
                return candidate
    return token


def counter_records(counter: Counter[str], limit: int) -> list[dict[str, Any]]:
    return [{"pattern": key, "count": count} for key, count in counter.most_common(limit)]


def document_supported_records(doc_patterns: list[list[str]], limit: int, min_doc_support: int) -> list[dict[str, Any]]:
    occurrences: Counter[str] = Counter()
    support: Counter[str] = Counter()
    for patterns in doc_patterns:
        clean = [pattern for pattern in patterns if pattern]
        occurrences.update(clean)
        for pattern in set(clean):
            support[pattern] += 1
    rows = [
        {
            "pattern": pattern,
            "count": occurrences[pattern],
            "doc_support": doc_count,
        }
        for pattern, doc_count in support.items()
        if doc_count >= min_doc_support
    ]
    rows.sort(key=lambda item: (item["doc_support"], item["count"], item["pattern"]), reverse=True)
    return rows[:limit]


def infer_years(docs: list[PdfDocument]) -> dict[str, int | None]:
    years = []
    for doc in docs:
        candidates = " ".join(str(v) for v in doc.metadata.values())
        years.extend(int(y) for y in re.findall(r"\b(20\d{2}|19\d{2})\b", candidates))
    if not years:
        return {"min": None, "max": None}
    return {"min": min(years), "max": max(years)}


def strength_from_count(count: int) -> str:
    if count >= 30:
        return "normal"
    if count >= 10:
        return "caution"
    return "pilot"


def most_common_order(orders: list[list[str]]) -> list[str]:
    if not orders:
        return []
    counts = Counter(tuple(order) for order in orders)
    return list(counts.most_common(1)[0][0])


def build_constraints(
    journal: str,
    profile_strength: str,
    abstract_metrics: list[dict[str, Any]],
    figure_caption_metrics: list[dict[str, Any]],
    section_metrics: dict[str, Any],
    selection_criteria: dict[str, Any],
) -> dict[str, list[str]]:
    constraints = {
        "writing": [
            "Use the learned section order when it is compatible with the target journal instructions.",
            "Make the energy-system value explicit before presenting algorithmic novelty.",
            "Tie each major claim to a metric, unit, comparison baseline, or figure reference.",
        ],
        "polishing": [
            "Preserve all supplied numbers, method names, datasets, and citations.",
            "Replace audit-style wording with claim-first scientific prose when the evidence supports it.",
            "Keep uncertainty and limitations visible when claims depend on subgroup or regime support.",
        ],
        "figures": [
            "Make captions self-contained with metric, unit, sample definition, and main interpretation.",
            "Keep panel order aligned with the claim sequence in the Results section.",
            "Use consistent colors for method families across the manuscript.",
        ],
        "guardrails": [
            "In Results and Discussion, reserve wind-forecasting importance statements for context. Start result claims with evidence-first templates such as <result_evidence> shows <finding_or_pattern>.",
            "When unit templates are sparse, use fallback unit framing: kW, MW, and GW for power; kWh, MWh, and GWh for energy; h for forecast horizon or temporal resolution.",
        ],
    }
    abstract_words = distribution([m.get("word_count") for m in abstract_metrics])
    if abstract_words["p25"] is not None and abstract_words["p75"] is not None:
        constraints["writing"].append(
            f"Target abstract length near {abstract_words['p25']:.0f} to {abstract_words['p75']:.0f} words for this profile."
        )
    caption_words = distribution([m.get("word_count") for m in figure_caption_metrics])
    if caption_words["p25"] is not None and caption_words["p75"] is not None:
        constraints["figures"].append(
            f"Target figure caption length near {caption_words['p25']:.0f} to {caption_words['p75']:.0f} words when figure complexity is comparable."
        )
    conclusion_words = section_metrics.get("conclusion", {}).get("word_count", {})
    conclusion_median = conclusion_words.get("median") if isinstance(conclusion_words, dict) else None
    if (
        journal.casefold() == "applied energy"
        and selection_criteria.get("topic_profile") == "wind_forecasting"
    ):
        constraints["writing"].append(
            "For full Applied Energy wind-forecasting manuscripts, draft the Conclusion around 500 to 700 words unless the evidence scope is narrow."
        )
    if isinstance(conclusion_median, (int, float)) and conclusion_median < 450:
        constraints["guardrails"].append(
            "Treat the learned Conclusion word-count distribution as extraction-sensitive when drafting full papers; do not compress a complete Conclusion only to match this corpus median."
        )
    methods_sentence_words = section_metrics.get("methods", {}).get("median_sentence_words", {})
    methods_sentence_p75 = methods_sentence_words.get("p75") if isinstance(methods_sentence_words, dict) else None
    if isinstance(methods_sentence_p75, (int, float)) and methods_sentence_p75 > 45:
        constraints["guardrails"].append(
            "Treat Methods median sentence P75 above 45 words as sentence-splitter noise; keep drafted long Methods sentences below about 35 words."
        )
    if profile_strength == "pilot":
        constraints["writing"].append("Label style conclusions as PILOT_PROFILE until at least 10 target-journal PDFs are available.")
    return constraints


def markdown_table(rows: list[list[Any]], headers: list[str]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join("" if value is None else str(value) for value in row) + " |")
    return "\n".join(out)


def metric_value(profile: dict[str, Any], section: str, metric: str, stat: str) -> float | None:
    value = (
        profile.get("sections", {})
        .get("metrics", {})
        .get(section, {})
        .get(metric, {})
        .get(stat)
    )
    return float(value) if isinstance(value, (int, float)) else None


def compare_to_distribution(value: float | int | None, dist: dict[str, Any]) -> str:
    if value is None:
        return "missing"
    p25 = dist.get("p25")
    p75 = dist.get("p75")
    if not isinstance(p25, (int, float)) or not isinstance(p75, (int, float)):
        return "unchecked"
    if value < p25:
        return "below"
    if value > p75:
        return "above"
    return "within"
