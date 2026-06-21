"""从PDF语料构建目标期刊风格档案。"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from style_learning_lib import (
    build_profile,
    extract_pdf,
    extract_text_document,
    markdown_table,
    split_sections,
    topic_screen_document,
    write_json,
    write_yaml,
    word_tokens,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a target-journal style profile from local PDFs or full-text files.")
    parser.add_argument("--pdf-dir", action="append", default=[], help="Directory containing corpus PDFs.")
    parser.add_argument("--pdf", action="append", default=[], help="Single PDF path. May be repeated.")
    parser.add_argument("--text-dir", action="append", default=[], help="Directory containing full-text .txt files.")
    parser.add_argument("--text", action="append", default=[], help="Single full-text .txt path. May be repeated.")
    parser.add_argument("--journal", required=True, help="Target journal name.")
    parser.add_argument("--profile-name", default=None, help="Human-readable profile name.")
    parser.add_argument("--source", default="local_pdf_corpus", help="Corpus source label.")
    parser.add_argument("--corpus-manifest", default=None, help="Optional corpus_manifest.json path.")
    parser.add_argument("--output", required=True, help="Output profile directory.")
    parser.add_argument("--min-pages", type=int, default=4, help="Minimum PDF pages required for profile inclusion.")
    parser.add_argument("--min-words", type=int, default=1500, help="Minimum extracted words required for profile inclusion.")
    parser.add_argument("--min-abstract-words", type=int, default=80, help="Minimum extracted abstract words.")
    parser.add_argument("--min-introduction-words", type=int, default=250, help="Minimum extracted introduction words.")
    parser.add_argument(
        "--require-sections",
        default="abstract,introduction",
        help="Comma-separated required section keys. Use empty string to disable.",
    )
    parser.add_argument("--max-docs", type=int, default=0, help="Maximum accepted PDFs to include. Zero means all.")
    parser.add_argument(
        "--topic-profile",
        default="none",
        choices=["none", "wind_forecasting", "renewable_forecasting"],
        help="Optional topic gate applied after PDF extraction.",
    )
    parser.add_argument("--require-topic-match", action="store_true", help="Exclude PDFs that fail the topic gate.")
    parser.add_argument("--min-topic-score", type=int, default=None, help="Override the topic profile score threshold.")
    parser.add_argument("--include-keyword", action="append", default=[], help="Extra topic include keyword. May be repeated.")
    parser.add_argument("--exclude-keyword", action="append", default=[], help="Extra topic exclude keyword. May be repeated.")
    parser.add_argument("--min-template-doc-support", type=int, default=5, help="Minimum documents supporting a learned language template.")
    return parser.parse_args()


def collect_sources(args: argparse.Namespace) -> list[Path]:
    paths: list[Path] = []
    for folder in args.pdf_dir:
        root = Path(folder)
        paths.extend(sorted(root.glob("*.pdf")))
    for item in args.pdf:
        paths.append(Path(item))
    for folder in args.text_dir:
        root = Path(folder)
        paths.extend(sorted(root.glob("*.txt")))
    for item in args.text:
        paths.append(Path(item))
    unique = []
    seen = set()
    seen_keys = set()
    for path in paths:
        resolved = path.resolve()
        key = dedupe_key(resolved)
        if resolved in seen or key in seen_keys:
            continue
        seen.add(resolved)
        seen_keys.add(key)
        unique.append(resolved)
    return unique


def dedupe_key(path: Path) -> str:
    # ScienceDirect下载名通常带有三位序号，去掉序号后用题名slug去重。
    return re.sub(r"^\d+_", "", path.stem).casefold()


def main() -> int:
    args = parse_args()
    output = Path(args.output)
    sources = collect_sources(args)
    if not sources:
        raise SystemExit("No corpus files were found. Provide --pdf-dir, --pdf, --text-dir, or --text.")

    docs = []
    failures = []
    excluded = []
    topic_screens = []
    required_sections = [item.strip() for item in args.require_sections.split(",") if item.strip()]
    for source_path in sources:
        try:
            doc = extract_source(source_path)
            reason = exclusion_reason(
                doc,
                args.min_pages,
                args.min_words,
                required_sections,
                args.min_abstract_words,
                args.min_introduction_words,
            )
            if reason:
                excluded.append(
                    {
                        "path": str(source_path),
                        "reason": reason,
                        "page_count": doc.page_count,
                        "word_count": len(word_tokens(doc.text)),
                        "sections_detected": list(split_sections(doc.text).keys()),
                    }
                )
                continue
            topic_screen = topic_screen_document(
                doc,
                args.topic_profile,
                min_score=args.min_topic_score,
                include_keywords=args.include_keyword,
                exclude_keywords=args.exclude_keyword,
            )
            topic_screens.append({"path": str(source_path), **topic_screen})
            if args.require_topic_match and not topic_screen.get("accepted"):
                excluded.append(
                    {
                        "path": str(source_path),
                        "reason": topic_screen.get("reason", "topic_mismatch"),
                        "page_count": doc.page_count,
                        "word_count": len(word_tokens(doc.text)),
                        "sections_detected": list(split_sections(doc.text).keys()),
                        "topic_screen": topic_screen,
                    }
                )
                continue
            docs.append(doc)
            if args.max_docs and len(docs) >= args.max_docs:
                break
        except Exception as exc:
            failures.append({"path": str(source_path), "error": str(exc)})

    if not docs:
        write_json(output / "extraction_failures.json", failures)
        raise SystemExit("No corpus files could be extracted. See extraction_failures.json.")

    profile_name = args.profile_name or f"{args.journal} style profile"
    profile = build_profile(
        docs=docs,
        journal=args.journal,
        profile_name=profile_name,
        source=args.source,
        corpus_manifest=args.corpus_manifest,
        selection_criteria={
            "min_pages": args.min_pages,
            "min_words": args.min_words,
            "min_abstract_words": args.min_abstract_words,
            "min_introduction_words": args.min_introduction_words,
            "required_sections": required_sections,
            "max_docs": args.max_docs or None,
            "topic_profile": args.topic_profile,
            "require_topic_match": args.require_topic_match,
            "min_topic_score": args.min_topic_score,
            "include_keywords": args.include_keyword,
            "exclude_keywords": args.exclude_keyword,
            "min_template_doc_support": args.min_template_doc_support,
            "excluded_count": len(excluded),
            "failed_count": len(failures),
        },
        min_template_doc_support=args.min_template_doc_support,
    )
    output.mkdir(parents=True, exist_ok=True)
    write_yaml(output / "style_profile.yaml", profile)
    write_yaml(output / "figure_style.yaml", profile.get("figures", {}))
    write_json(output / "source_document_metrics.json", profile["corpus"]["documents"])
    if failures:
        write_json(output / "extraction_failures.json", failures)
    if excluded:
        write_json(output / "excluded_documents.json", excluded)
    if topic_screens:
        write_json(output / "topic_screening_report.json", topic_screens)

    write_section_moves(output / "section_moves.md", profile)
    write_report(output / "style_learning_report.md", profile, failures, excluded)
    write_digest(output / "learned_style_digest.md", profile)
    print(f"Wrote profile to {output / 'style_profile.yaml'}")
    print(f"Profile strength: {profile['profile_strength']}")
    print(f"Documents extracted: {len(docs)}")
    if failures:
        print(f"Extraction failures: {len(failures)}")
    if excluded:
        print(f"Excluded PDFs: {len(excluded)}")
    return 0


def extract_source(path: Path):
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf(path)
    if suffix in {".txt", ".text"}:
        return extract_text_document(path)
    raise ValueError(f"Unsupported corpus file type: {path}")


def exclusion_reason(
    doc,
    min_pages: int,
    min_words: int,
    required_sections: list[str],
    min_abstract_words: int,
    min_introduction_words: int,
) -> str | None:
    word_count = len(word_tokens(doc.text))
    if doc.page_count < min_pages:
        return f"page_count_below_{min_pages}"
    if word_count < min_words:
        return f"word_count_below_{min_words}"
    sections = split_sections(doc.text)
    missing = [section for section in required_sections if section not in sections]
    if missing:
        return "missing_sections:" + ",".join(missing)
    abstract_words = len(word_tokens(sections.get("abstract", "")))
    if "abstract" in required_sections and abstract_words < min_abstract_words:
        return f"abstract_words_below_{min_abstract_words}"
    introduction_words = len(word_tokens(sections.get("introduction", "")))
    if "introduction" in required_sections and introduction_words < min_introduction_words:
        return f"introduction_words_below_{min_introduction_words}"
    return None


def write_section_moves(path: Path, profile: dict) -> None:
    abstract_moves = profile.get("abstract", {}).get("move_presence", {})
    rows = [
        [move, values.get("count"), values.get("share")]
        for move, values in abstract_moves.items()
    ]
    content = [
        f"# Section Moves: {profile['journal']}",
        "",
        f"Profile strength: `{profile['profile_strength']}`",
        "",
        "## Common Section Order",
        "",
        ", ".join(profile.get("sections", {}).get("common_order", [])) or "Unchecked",
        "",
        "## Abstract Move Presence",
        "",
        markdown_table(rows, ["Move", "Count", "Share"]),
        "",
        "## Recommended Introduction Moves",
        "",
    ]
    for item in profile.get("introduction", {}).get("recommended_moves", []):
        content.append(f"- {item}")
    content.extend(["", "## Recommended Results and Discussion Moves", ""])
    for item in profile.get("results_discussion", {}).get("recommended_moves", []):
        content.append(f"- {item}")
    path.write_text("\n".join(content).strip() + "\n", encoding="utf-8")


def write_report(path: Path, profile: dict, failures: list[dict], excluded: list[dict]) -> None:
    sections = profile.get("sections", {}).get("presence", {})
    rows = [
        [section, values.get("count"), values.get("share")]
        for section, values in sorted(sections.items())
    ]
    content = [
        f"# Style Learning Report: {profile['journal']}",
        "",
        f"Profile name: {profile['profile_name']}",
        f"Profile strength: `{profile['profile_strength']}`",
        f"Article count: {profile['corpus']['article_count']}",
        f"PDF count: {profile['corpus']['pdf_count']}",
        f"Excluded count: {profile['corpus'].get('selection_criteria', {}).get('excluded_count', 0)}",
        "",
        "## Section Coverage",
        "",
        markdown_table(rows, ["Section", "Count", "Share"]),
        "",
        "## Downstream Constraints",
        "",
    ]
    for group, items in profile.get("constraints", {}).items():
        content.append(f"### {group.title()}")
        content.append("")
        for item in items:
            content.append(f"- {item}")
        content.append("")
    if failures:
        content.extend(["## Extraction Failures", ""])
        for item in failures:
            content.append(f"- `{item['path']}`: {item['error']}")
    if excluded:
        content.extend(["", "## Excluded PDFs", ""])
        for item in excluded:
            content.append(
                f"- `{item['path']}`: {item['reason']}; pages={item['page_count']}; words={item['word_count']}"
            )
    path.write_text("\n".join(content).strip() + "\n", encoding="utf-8")


def write_digest(path: Path, profile: dict) -> None:
    sections = profile.get("sections", {})
    section_metrics = sections.get("metrics", {})
    presence = sections.get("presence", {})
    figures = profile.get("figures", {})
    abstract = profile.get("abstract", {})
    introduction = profile.get("introduction", {})
    results_discussion = profile.get("results_discussion", {})
    corpus = profile.get("corpus", {})
    language = profile.get("language_patterns", {})

    lines = [
        f"# Learned Style Digest: {profile['journal']}",
        "",
        f"Profile strength: `{profile['profile_strength']}`",
        f"Article count: {corpus.get('article_count')}",
        f"PDF count: {corpus.get('pdf_count')}",
        f"Corpus years: {range_cell(corpus.get('years', {}))}",
        "",
        "## Architecture",
        "",
        "Common detected order:",
        "",
        ", ".join(sections.get("common_order", [])) or "Unchecked",
        "",
        markdown_table(
            [
                [name, values.get("count"), values.get("share")]
                for name, values in sorted(presence.items())
            ],
            ["Section", "Count", "Share"],
        ),
        "",
        "## Front Matter",
        "",
        "Highlights appear in most sampled papers and are concise claim bullets. Keywords appear in every sampled paper.",
        "",
        markdown_table(
            metric_rows(
                section_metrics,
                ["highlights", "keywords"],
                ["word_count", "sentence_count", "median_sentence_words"],
            ),
            ["Section", "Metric", "Median", "P25", "P75"],
        ),
        "",
        "## Abstract",
        "",
        "The abstract is compact and usually follows context, gap, method, quantified result, and operational implication.",
        "",
        markdown_table(
            single_group_rows(
                abstract.get("metrics", {}),
                ["word_count", "sentence_count", "median_sentence_words", "numeric_tokens_per_1000_words"],
            ),
            ["Metric", "Median", "P25", "P75"],
        ),
        "",
        markdown_table(
            [
                [move, values.get("count"), values.get("share")]
                for move, values in abstract.get("move_presence", {}).items()
            ],
            ["Move", "Count", "Share"],
        ),
        "",
        "### Abstract Expression Templates",
        "",
    ]
    lines.extend(section_language_block(language, "abstract", include_flow=False))
    lines.extend(
        [
            "",
        "## Introduction",
        "",
        "The introduction establishes the energy-system setting before narrowing to the method gap and contribution.",
        "",
        markdown_table(
            single_group_rows(
                introduction.get("metrics", {}),
                [
                    "word_count",
                    "paragraph_count",
                    "median_sentence_words",
                    "citation_markers_per_1000_words",
                    "numeric_tokens_per_1000_words",
                    "contrast_terms_per_1000_words",
                ],
            ),
            ["Metric", "Median", "P25", "P75"],
        ),
        "",
        "Recommended moves:",
        "",
        ]
    )
    for item in introduction.get("recommended_moves", []):
        lines.append(f"- {item}")
    lines.extend(["", "### Introduction Narrative Arc", ""])
    lines.extend(introduction_arc_block(language))
    lines.extend(["", "### Introduction Expression Templates", ""])
    lines.extend(section_language_block(language, "introduction", include_flow=True))

    lines.extend(
        [
            "",
            "## Methods And Case Study",
            "",
            "Methods sections are present in most sampled papers. Case-study sections appear when the paper needs a concrete system, geography, dataset, or operational setup.",
            "",
            markdown_table(
                metric_rows(
                    section_metrics,
                    ["methods", "case_study", "nomenclature"],
                    ["word_count", "paragraph_count", "median_sentence_words", "citation_markers_per_1000_words"],
                ),
                ["Section", "Metric", "Median", "P25", "P75"],
            ),
            "",
            "### Methods Expression Templates",
            "",
        ]
    )
    lines.extend(section_language_block(language, "methods", include_flow=True))
    lines.extend(["", "### Case Study Expression Templates", ""])
    lines.extend(section_language_block(language, "case_study", include_flow=True))
    lines.extend(
        [
            "",
            "## Results And Discussion",
            "",
            "Result prose should start from a claim, then give metric, unit, comparison, uncertainty or support, and operational interpretation.",
            "",
            markdown_table(
                single_group_rows(
                    results_discussion.get("metrics", {}),
                    [
                        "word_count",
                        "paragraph_count",
                        "median_sentence_words",
                        "figure_refs_per_1000_words",
                        "citation_markers_per_1000_words",
                        "limitation_terms_per_1000_words",
                    ],
                ),
                ["Metric", "Median", "P25", "P75"],
            ),
            "",
            "Recommended moves:",
            "",
        ]
    )
    for item in results_discussion.get("recommended_moves", []):
        lines.append(f"- {item}")
    lines.extend(["", "### Results Expression Templates", ""])
    lines.extend(section_language_block(language, "results", include_flow=True))
    lines.extend(["", "### Discussion Expression Templates", ""])
    lines.extend(section_language_block(language, "discussion", include_flow=True))
    lines.extend(["", "### Results And Discussion Combined Templates", ""])
    lines.extend(section_language_block(language, "results_discussion", include_flow=True))
    lines.extend(["", "### Numeric Reporting Templates", ""])
    lines.extend(numeric_reporting_block(language))
    lines.extend(["", "### Comparison Language Templates", ""])
    lines.extend(comparison_language_block(language))

    lines.extend(
        [
            "",
            "## Conclusion",
            "",
            "Conclusions are common and should restate the evidence-bound contribution, operational implication, and boundary conditions.",
            "",
            markdown_table(
                metric_rows(
                    section_metrics,
                    ["conclusion"],
                    ["word_count", "paragraph_count", "median_sentence_words", "limitation_terms_per_1000_words"],
                ),
                ["Section", "Metric", "Median", "P25", "P75"],
            ),
            "",
            "### Conclusion Expression Templates",
            "",
        ]
    )
    lines.extend(section_language_block(language, "conclusion", include_flow=True))
    lines.extend(["", "### Conclusion Closing Patterns", ""])
    lines.extend(conclusion_closing_block(language))
    lines.extend(
        [
            "",
            "## Figures And Tables",
            "",
            "Figures and tables are expected to support the evidence chain. Captions should name the metric, unit, sample, and main interpretation.",
            "",
            markdown_table(
                [
                    ["figures_per_article", dist_stat(figures.get("figures_per_article", {}), "median"), dist_stat(figures.get("figures_per_article", {}), "p25"), dist_stat(figures.get("figures_per_article", {}), "p75")],
                    ["tables_per_article", dist_stat(figures.get("tables_per_article", {}), "median"), dist_stat(figures.get("tables_per_article", {}), "p25"), dist_stat(figures.get("tables_per_article", {}), "p75")],
                    ["figure_caption_words", dist_stat(figures.get("figure_caption_metrics", {}).get("word_count", {}), "median"), dist_stat(figures.get("figure_caption_metrics", {}).get("word_count", {}), "p25"), dist_stat(figures.get("figure_caption_metrics", {}).get("word_count", {}), "p75")],
                    ["table_caption_words", dist_stat(figures.get("table_caption_metrics", {}).get("word_count", {}), "median"), dist_stat(figures.get("table_caption_metrics", {}).get("word_count", {}), "p25"), dist_stat(figures.get("table_caption_metrics", {}).get("word_count", {}), "p75")],
                ],
                ["Metric", "Median", "P25", "P75"],
            ),
            "",
            "### Figure And Caption Expression",
            "",
        ]
    )
    lines.extend(figure_table_expression_block(language))
    lines.extend(
        [
            "",
            "## Downstream Use",
            "",
        ]
    )
    for group, items in profile.get("constraints", {}).items():
        lines.append(f"### {group.title()}")
        lines.append("")
        for item in items:
            lines.append(f"- {item}")
        lines.append("")

    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def section_language_block(language: dict, section: str, include_flow: bool = True) -> list[str]:
    data = language.get("by_section", {}).get(section, {})
    if not data:
        return ["No stable section-level language patterns were extracted."]
    lines = [
        f"- Sentence starters: {record_inline(data.get('sentence_starters', []), limit=6)}",
        f"- Verb preferences: {record_inline(data.get('verb_preferences', []), limit=8)}",
        f"- Hedging and degree terms: {record_inline(data.get('hedging_and_degree_terms', []), limit=8)}",
        f"- Frequent bigrams: {record_inline(data.get('bigrams', []), limit=8)}",
        f"- Frequent trigrams: {record_inline(data.get('trigrams', []), limit=8)}",
    ]
    move_templates = data.get("move_sentence_templates", {})
    if move_templates:
        lines.append("- Move-level normalized templates:")
        for move in ["context", "gap", "method", "result", "implication", "limitation"]:
            records = move_templates.get(move, [])
            if records:
                lines.append(f"  - {move}: {record_inline(records, limit=3)}")
    move_starters = data.get("move_starters", {})
    if move_starters:
        lines.append("- Move-level starters:")
        for move in ["context", "gap", "method", "result", "implication", "limitation"]:
            records = move_starters.get(move, [])
            if records:
                lines.append(f"  - {move}: {record_inline(records, limit=3)}")
    if include_flow:
        flow = language.get("paragraph_flow_templates", {}).get(section, [])
        if flow:
            lines.append(f"- Paragraph flow templates: {record_inline(flow, limit=5)}")
    return lines


def introduction_arc_block(language: dict) -> list[str]:
    arc = language.get("introduction_arc_patterns", {})
    if not arc:
        return ["No stable introduction arc patterns were extracted."]
    lines = [
        f"- Arc sequences: {record_inline(arc.get('arc_sequences', []), limit=5)}",
        f"- Transition starters: {record_inline(arc.get('transition_starters', []), limit=6)}",
    ]
    position_moves = arc.get("paragraph_position_moves", {})
    position_starters = arc.get("paragraph_position_starters", {})
    for slot in sorted(position_moves.keys())[:6]:
        moves = record_inline(position_moves.get(slot, []), limit=3)
        starters = record_inline(position_starters.get(slot, []), limit=3)
        lines.append(f"- {slot}: moves {moves}; starters {starters}")
    return lines


def numeric_reporting_block(language: dict) -> list[str]:
    numeric = language.get("numeric_reporting", {})
    if not numeric:
        return ["No stable numeric reporting patterns were extracted."]
    lines = [
        f"- Format types: {record_inline(numeric.get('format_types', []), limit=8)}",
        f"- Short normalized templates: {record_inline(numeric.get('short_templates', []), limit=8)}",
        f"- Unit co-occurrence: {record_inline(numeric.get('units', []), limit=10)}",
        f"- Uncertainty expressions: {record_inline(numeric.get('uncertainty_expressions', []), limit=8)}",
    ]
    by_section = numeric.get("by_section", {})
    if by_section:
        lines.append("- Numeric pattern by section:")
        for section in ["abstract", "introduction", "methods", "case_study", "results", "discussion", "results_discussion", "conclusion"]:
            records = by_section.get(section, [])
            if records:
                lines.append(f"  - {section}: {record_inline(records, limit=4)}")
    unit_templates = numeric.get("unit_context_templates", {})
    if unit_templates:
        lines.append("- Unit context templates:")
        for unit, records in sorted(unit_templates.items())[:8]:
            lines.append(f"  - {unit}: {record_inline(records, limit=2)}")
    return lines


def comparison_language_block(language: dict) -> list[str]:
    comparison = language.get("comparison_language", {})
    if not comparison:
        return ["No stable comparison language patterns were extracted."]
    return [
        f"- Comparison templates: {record_inline(comparison.get('templates', []), limit=8)}",
        f"- Comparison verbs: {record_inline(comparison.get('verbs', []), limit=8)}",
    ]


def conclusion_closing_block(language: dict) -> list[str]:
    closing = language.get("conclusion_closing_patterns", {})
    if not closing:
        return ["No stable conclusion closing patterns were extracted."]
    return [
        f"- Opening starters: {record_inline(closing.get('opening_starters', []), limit=6)}",
        f"- Closing starters: {record_inline(closing.get('closing_starters', []), limit=6)}",
        f"- Closing moves: {record_inline(closing.get('closing_moves', []), limit=6)}",
    ]


def figure_table_expression_block(language: dict) -> list[str]:
    fig = language.get("figure_caption_patterns", {})
    table = language.get("table_caption_patterns", {})
    headers = language.get("table_header_patterns", {})
    refs = language.get("figure_reference_patterns", {})
    lines = [
        f"- Figure caption opening types: {record_inline(fig.get('opening_types', []), limit=8)}",
        f"- Figure caption starters: {record_inline(fig.get('opening_starters', []), limit=8)}",
        f"- Figure caption syntax: {record_inline(fig.get('syntax_patterns', []), limit=8)}",
        f"- Table caption opening types: {record_inline(table.get('opening_types', []), limit=8)}",
        f"- Table caption starters: {record_inline(table.get('opening_starters', []), limit=8)}",
        f"- Table header shapes: {record_inline(headers.get('header_shapes', []), limit=8)}",
        f"- Table header terms: {record_inline(headers.get('header_terms', []), limit=12)}",
        f"- Figure reference templates: {record_inline(refs.get('sentence_templates', []), limit=8)}",
    ]
    topic_to_starters = fig.get("topic_to_starters", {})
    if topic_to_starters:
        lines.append("- Figure topic to caption starter:")
        for topic in sorted(topic_to_starters.keys())[:8]:
            lines.append(f"  - {topic}: {record_inline(topic_to_starters.get(topic, []), limit=3)}")
    return lines


def record_inline(records: list[dict] | None, limit: int = 5) -> str:
    if not records:
        return "Unchecked"
    items = []
    for record in records[:limit]:
        pattern = record.get("pattern", "")
        count = record.get("count")
        doc_support = record.get("doc_support")
        if doc_support is not None and count is not None:
            items.append(f"{pattern} (docs={doc_support}, n={count})")
        elif count is None:
            items.append(str(pattern))
        else:
            items.append(f"{pattern} ({count})")
    return "; ".join(items) if items else "Unchecked"


def metric_rows(section_metrics: dict, section_names: list[str], metric_names: list[str]) -> list[list]:
    rows = []
    for section in section_names:
        metrics = section_metrics.get(section, {})
        for metric in metric_names:
            if metric in metrics:
                rows.append([section, metric, dist_stat(metrics[metric], "median"), dist_stat(metrics[metric], "p25"), dist_stat(metrics[metric], "p75")])
    return rows


def single_group_rows(metrics: dict, metric_names: list[str]) -> list[list]:
    rows = []
    for metric in metric_names:
        if metric in metrics:
            rows.append([metric, dist_stat(metrics[metric], "median"), dist_stat(metrics[metric], "p25"), dist_stat(metrics[metric], "p75")])
    return rows


def dist_stat(dist: dict, key: str):
    value = dist.get(key) if isinstance(dist, dict) else None
    return "" if value is None else value


def range_cell(value: dict) -> str:
    if not isinstance(value, dict):
        return "Unchecked"
    low = value.get("min")
    high = value.get("max")
    if low is None and high is None:
        return "Unchecked"
    if low == high:
        return str(low)
    return f"{low} to {high}"


if __name__ == "__main__":
    raise SystemExit(main())
