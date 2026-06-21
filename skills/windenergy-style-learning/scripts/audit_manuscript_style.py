"""根据目标期刊风格档案审计手稿。"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any

from style_learning_lib import (
    basic_metrics,
    compare_to_distribution,
    count_citations,
    document_metrics,
    extract_pdf,
    markdown_table,
    read_yaml,
    split_sections,
    write_json,
    word_tokens,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit a manuscript against a learned style profile.")
    parser.add_argument("--manuscript", required=True, help="Manuscript PDF path.")
    parser.add_argument("--profile", required=True, help="style_profile.yaml path.")
    parser.add_argument("--output", required=True, help="Audit output directory.")
    parser.add_argument("--label", default=None, help="Optional manuscript label.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manuscript = Path(args.manuscript).resolve()
    output = Path(args.output)
    profile_path = Path(args.profile).resolve()
    profile = read_yaml(profile_path)
    doc = extract_pdf(manuscript)
    metrics = document_metrics(doc)
    sections = split_sections(doc.text)
    issues = build_issues(profile, metrics, sections)
    audit = {
        "manuscript": str(manuscript),
        "label": args.label or manuscript.stem,
        "profile": str(profile_path),
        "journal": profile.get("journal"),
        "profile_strength": profile.get("profile_strength"),
        "manuscript_metrics": metrics,
        "issues": issues,
    }
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / "manuscript_style_audit.json", audit)
    write_markdown(output / "manuscript_style_audit.md", audit, profile)
    write_revision_targets(output / "revision_targets.md", issues)
    print(f"Wrote audit to {output / 'manuscript_style_audit.md'}")
    print(f"Issues: {len(issues)}")
    for severity in ["BLOCKER", "MAJOR", "MINOR", "INFO"]:
        count = sum(1 for issue in issues if issue["severity"] == severity)
        if count:
            print(f"{severity}: {count}")
    return 0


def build_issues(profile: dict[str, Any], metrics: dict[str, Any], sections: dict[str, str]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    profile_strength = profile.get("profile_strength")
    if profile_strength == "pilot":
        issues.append(
            issue(
                "INFO",
                "PROFILE_PILOT",
                "Profile is based on fewer than 10 PDFs.",
                "Treat ranges as exploratory and expand the target-journal corpus before enforcing hard rules.",
                "windenergy-style-learning",
            )
        )

    required = ["abstract", "introduction", "conclusion"]
    for section in required:
        if section not in sections:
            issues.append(
                issue(
                    "BLOCKER",
                    f"MISSING_{section.upper()}",
                    f"Required section `{section}` was not detected.",
                    "Restore or rename the section so downstream polishing can verify structure.",
                    "windenergy-writing",
                )
            )

    section_profile = profile.get("sections", {}).get("metrics", {})
    section_presence = profile.get("sections", {}).get("presence", {})
    for section, manuscript_metrics in metrics.get("section_metrics", {}).items():
        if section in {"references", "keywords", "article_info", "highlights"}:
            continue
        support_count = section_presence.get(section, {}).get("count", 0)
        if support_count < 10:
            continue
        target_metrics = section_profile.get(section, {})
        for metric_name in ["word_count", "median_sentence_words", "citation_markers_per_1000_words"]:
            if section == "abstract" and metric_name == "word_count":
                continue
            if metric_name not in target_metrics:
                continue
            status = compare_to_distribution(manuscript_metrics.get(metric_name), target_metrics[metric_name])
            if status in {"above", "below"}:
                severity = "MAJOR" if metric_name == "word_count" and section in {"abstract", "introduction"} else "MINOR"
                issues.append(
                    issue(
                        severity,
                        f"{section.upper()}_{metric_name.upper()}_{status.upper()}",
                        f"`{section}` {metric_name} is {status} the target interquartile range.",
                        metric_recommendation(section, metric_name, status),
                        downstream_for_section(section, metric_name),
                        evidence={
                            "manuscript_value": manuscript_metrics.get(metric_name),
                            "target": target_metrics[metric_name],
                        },
                    )
                )

    abstract_text = sections.get("abstract", "")
    if abstract_text:
        abstract_metrics = basic_metrics(abstract_text)
        abstract_target = profile.get("abstract", {}).get("metrics", {}).get("word_count", {})
        status = compare_to_distribution(abstract_metrics.get("word_count"), abstract_target)
        if status in {"above", "below"}:
            issues.append(
                issue(
                    "MAJOR",
                    f"ABSTRACT_LENGTH_{status.upper()}",
                    f"Abstract word count is {status} the learned profile range.",
                    "Revise the abstract around context, gap, method, quantified result, and operational implication.",
                    "windenergy-polishing",
                    evidence={
                        "manuscript_value": abstract_metrics.get("word_count"),
                        "target": abstract_target,
                    },
                )
            )

    issues.extend(results_citation_issues(profile, metrics, sections))
    issues.extend(figure_caption_length_issues(profile, metrics))
    issues.extend(conclusion_guardrail_issues(profile, metrics, sections))

    figure_count = metrics.get("figure_caption_count", 0)
    target_figures = profile.get("figures", {}).get("figures_per_article", {})
    figure_status = compare_to_distribution(figure_count, target_figures)
    if figure_status in {"above", "below"}:
        issues.append(
            issue(
                "MAJOR",
                f"FIGURE_COUNT_{figure_status.upper()}",
                f"Detected figure-caption count is {figure_status} the target profile range.",
                "Check whether each central claim has a display item and whether low-value figures can be merged.",
                "windenergy-figure",
                evidence={"manuscript_value": figure_count, "target": target_figures},
            )
        )

    if metrics.get("table_caption_count", 0) > max(8, figure_count * 2):
        issues.append(
            issue(
                "MAJOR",
                "TABLE_LOAD_HIGH",
                "Detected table count is high relative to figure count.",
                "Move exhaustive diagnostics to supplementary material or consolidate tables around review-critical comparisons.",
                "windenergy-figure",
                evidence={
                    "figure_caption_count": figure_count,
                    "table_caption_count": metrics.get("table_caption_count", 0),
                },
            )
        )

    return issues


def results_citation_issues(profile: dict[str, Any], metrics: dict[str, Any], sections: dict[str, str]) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    text = "\n\n".join(
        sections.get(section, "")
        for section in ["results", "discussion", "results_discussion"]
        if sections.get(section)
    )
    if not text:
        return issues
    citations = count_citations(text)
    baseline_hits = comparison_baseline_hits(text)
    if citations == 0 and baseline_hits:
        section_metrics = metrics.get("section_metrics", {})
        citation_density = 0
        for section in ["results_discussion", "results", "discussion"]:
            if section in section_metrics:
                citation_density = section_metrics[section].get("citation_markers_per_1000_words", 0)
                break
        target = citation_density_target(profile)
        issues.append(
            issue(
                "MAJOR",
                "RESULTS_DISCUSSION_CITATION_DENSITY_ZERO",
                "Results and Discussion contains comparison baselines but no citation markers.",
                "Add 2 to 4 source-backed citations for the compared calibration or baseline methods, using only references supplied by the author.",
                "windenergy-citation",
                evidence={
                    "manuscript_value": citation_density,
                    "baseline_hits": baseline_hits,
                    "target": target,
                },
            )
        )
    return issues


def comparison_baseline_hits(text: str) -> list[str]:
    patterns = {
        "ACI": r"\bACI\b",
        "AgACI": r"\bAgACI\b",
        "EnbPI-RH": r"\bEnbPI-?RH\b",
        "Static": r"\bStatic\b",
        "Width-only": r"\bWidth-only\b",
        "QRLSTM": r"\bQRLSTM\b",
        "GBR": r"\bGBR\b",
        "MLP": r"\bMLP\b",
        "Ridge": r"\bRidge\b",
    }
    hits = [name for name, pattern in patterns.items() if re.search(pattern, text, re.I)]
    return sorted(set(hits))


def citation_density_target(profile: dict[str, Any]) -> dict[str, Any]:
    metrics = profile.get("sections", {}).get("metrics", {})
    for section in ["results_discussion", "results", "discussion"]:
        target = metrics.get(section, {}).get("citation_markers_per_1000_words")
        if target:
            return target
    return {}


def figure_caption_length_issues(profile: dict[str, Any], metrics: dict[str, Any]) -> list[dict[str, Any]]:
    caption_metrics = metrics.get("figure_caption_metrics", [])
    target = profile.get("figures", {}).get("figure_caption_metrics", {}).get("word_count", {})
    p25 = target.get("p25") if isinstance(target, dict) else None
    if not isinstance(p25, (int, float)) or not caption_metrics:
        return []
    word_counts = [item.get("word_count") for item in caption_metrics if isinstance(item.get("word_count"), (int, float))]
    below = [count for count in word_counts if count < p25]
    if len(below) >= max(3, int(len(word_counts) * 0.3)):
        return [
            issue(
                "MINOR",
                "FIGURE_CAPTION_LENGTH_BELOW",
                "Several figure captions are shorter than the target profile range.",
                "Expand short captions with metric, unit, sample definition, and one interpretation sentence.",
                "windenergy-figure",
                evidence={
                    "below_count": len(below),
                    "caption_count": len(word_counts),
                    "caption_word_counts": word_counts,
                    "target": target,
                },
            )
        ]
    return []


def conclusion_guardrail_issues(profile: dict[str, Any], metrics: dict[str, Any], sections: dict[str, str]) -> list[dict[str, Any]]:
    if "conclusion" not in sections:
        return []
    journal = str(profile.get("journal", "")).casefold()
    selection = profile.get("corpus", {}).get("selection_criteria", {})
    if journal != "applied energy" or selection.get("topic_profile") != "wind_forecasting":
        return []
    conclusion_metrics = metrics.get("section_metrics", {}).get("conclusion", {})
    word_count = conclusion_metrics.get("word_count")
    if isinstance(word_count, (int, float)) and word_count < 500:
        return [
            issue(
                "MINOR",
                "CONCLUSION_GUARDRAIL_BELOW",
                "Conclusion is below the v13 full-manuscript Applied Energy wind-forecasting guardrail.",
                "Expand the Conclusion toward 500 to 700 words by adding evidence-bound implications, limitations, and transfer conditions.",
                "windenergy-polishing",
                evidence={
                    "manuscript_value": word_count,
                    "target": {"p25": 500, "p75": 700, "source": "v13_guardrail"},
                },
            )
        ]
    return []


def issue(
    severity: str,
    issue_id: str,
    finding: str,
    recommendation: str,
    downstream_skill: str,
    evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "id": issue_id,
        "severity": severity,
        "finding": finding,
        "recommendation": recommendation,
        "downstream_skill": downstream_skill,
        "evidence": evidence or {},
    }


def metric_recommendation(section: str, metric_name: str, status: str) -> str:
    if metric_name == "word_count":
        return f"Adjust `{section}` length toward the target profile range while preserving supplied evidence."
    if metric_name == "median_sentence_words":
        return f"Revise `{section}` sentence rhythm and split or combine sentences as needed."
    if metric_name == "citation_markers_per_1000_words":
        return f"Check `{section}` citation placement and add sources only when the author supplies valid references."
    return f"Review `{section}` {metric_name}."


def downstream_for_section(section: str, metric_name: str) -> str:
    if "figure" in metric_name or section in {"results", "discussion", "results_discussion"}:
        return "windenergy-figure"
    if section in {"abstract", "introduction", "conclusion"}:
        return "windenergy-polishing"
    return "windenergy-writing"


def write_markdown(path: Path, audit: dict[str, Any], profile: dict[str, Any]) -> None:
    issues = audit["issues"]
    summary_rows = []
    for severity in ["BLOCKER", "MAJOR", "MINOR", "INFO"]:
        summary_rows.append([severity, sum(1 for item in issues if item["severity"] == severity)])
    section_rows = [
        [section, values.get("word_count"), values.get("paragraph_count"), values.get("citation_markers_per_1000_words")]
        for section, values in audit["manuscript_metrics"].get("section_metrics", {}).items()
    ]
    lines = [
        f"# Manuscript Style Audit: {audit['label']}",
        "",
        f"Target journal: {audit['journal']}",
        f"Profile strength: `{audit['profile_strength']}`",
        f"Profile file: `{audit['profile']}`",
        "",
        "## Summary",
        "",
        markdown_table(summary_rows, ["Severity", "Count"]),
        "",
        "## Profile Learning Snapshot",
        "",
        markdown_table(profile_snapshot_rows(profile), ["Area", "Learned Target"]),
        "",
        "Profile coverage:",
        "",
        markdown_table(profile_coverage_rows(profile), ["Section", "Count", "Share"]),
        "",
        "## Profile Language Snapshot",
        "",
        markdown_table(profile_language_rows(profile), ["Area", "Learned Pattern"]),
        "",
        "## Manuscript Section Metrics",
        "",
        markdown_table(section_rows, ["Section", "Words", "Paragraphs", "Citations per 1000 words"]),
        "",
        "## Ranked Issues",
        "",
    ]
    if not issues:
        lines.append("No style gaps were detected by the deterministic checks.")
    for item in issues:
        lines.extend(
            [
                f"### {item['severity']} {item['id']}",
                "",
                item["finding"],
                "",
                f"Recommendation: {item['recommendation']}",
                "",
                f"Downstream skill: `{item['downstream_skill']}`",
                "",
            ]
        )
    lines.extend(["## Downstream Constraints", ""])
    for group, values in profile.get("constraints", {}).items():
        lines.append(f"### {group.title()}")
        lines.append("")
        for value in values:
            lines.append(f"- {value}")
        lines.append("")
    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def profile_snapshot_rows(profile: dict[str, Any]) -> list[list[str]]:
    abstract_metrics = profile.get("abstract", {}).get("metrics", {})
    intro_metrics = profile.get("introduction", {}).get("metrics", {})
    rd_metrics = profile.get("results_discussion", {}).get("metrics", {})
    section_metrics = profile.get("sections", {}).get("metrics", {})
    figures = profile.get("figures", {})
    return [
        ["Abstract length", dist_range(abstract_metrics.get("word_count", {}))],
        ["Abstract sentence count", dist_range(abstract_metrics.get("sentence_count", {}))],
        ["Introduction length", dist_range(intro_metrics.get("word_count", {}))],
        ["Introduction citation density", dist_range(intro_metrics.get("citation_markers_per_1000_words", {}))],
        ["Methods length", dist_range(section_metrics.get("methods", {}).get("word_count", {}))],
        ["Results and discussion length", dist_range(rd_metrics.get("word_count", {}))],
        ["Conclusion length", dist_range(section_metrics.get("conclusion", {}).get("word_count", {}))],
        ["Figures per article", dist_range(figures.get("figures_per_article", {}))],
        ["Figure caption words", dist_range(figures.get("figure_caption_metrics", {}).get("word_count", {}))],
        ["Table caption words", dist_range(figures.get("table_caption_metrics", {}).get("word_count", {}))],
    ]


def profile_coverage_rows(profile: dict[str, Any]) -> list[list[Any]]:
    presence = profile.get("sections", {}).get("presence", {})
    preferred = [
        "highlights",
        "keywords",
        "abstract",
        "introduction",
        "methods",
        "case_study",
        "results",
        "discussion",
        "results_discussion",
        "conclusion",
        "references",
    ]
    rows = []
    for section in preferred:
        values = presence.get(section)
        if values:
            rows.append([section, values.get("count"), values.get("share")])
    return rows


def profile_language_rows(profile: dict[str, Any]) -> list[list[str]]:
    language = profile.get("language_patterns", {})
    by_section = language.get("by_section", {})
    rows: list[list[str]] = []
    for section in [
        "abstract",
        "introduction",
        "methods",
        "case_study",
        "results",
        "discussion",
        "results_discussion",
        "conclusion",
    ]:
        data = by_section.get(section, {})
        if not data:
            continue
        rows.append([f"{section} starters", record_inline(data.get("sentence_starters", []), 3)])
        rows.append([f"{section} verbs", record_inline(data.get("verb_preferences", []), 5)])
        rows.append([f"{section} move templates", move_template_inline(data.get("move_sentence_templates", {}), 3)])
    numeric = language.get("numeric_reporting", {})
    if numeric:
        rows.append(["numeric format types", record_inline(numeric.get("format_types", []), 5)])
        rows.append(["numeric units", record_inline(numeric.get("units", []), 8)])
        rows.append(["uncertainty expressions", record_inline(numeric.get("uncertainty_expressions", []), 5)])
        rows.append(["numeric templates", record_inline(numeric.get("short_templates", []), 5)])
    comparison = language.get("comparison_language", {})
    if comparison:
        rows.append(["comparison templates", record_inline(comparison.get("templates", []), 5)])
        rows.append(["comparison verbs", record_inline(comparison.get("verbs", []), 8)])
    intro_arc = language.get("introduction_arc_patterns", {})
    if intro_arc:
        rows.append(["introduction arc", record_inline(intro_arc.get("arc_sequences", []), 3)])
        rows.append(["introduction transitions", record_inline(intro_arc.get("transition_starters", []), 3)])
    closing = language.get("conclusion_closing_patterns", {})
    if closing:
        rows.append(["conclusion closing starters", record_inline(closing.get("closing_starters", []), 4)])
        rows.append(["conclusion closing moves", record_inline(closing.get("closing_moves", []), 4)])
    figures = language.get("figure_caption_patterns", {})
    if figures:
        rows.append(["figure caption syntax", record_inline(figures.get("syntax_patterns", []), 5)])
        rows.append(["figure caption openings", record_inline(figures.get("opening_types", []), 5)])
    table_headers = language.get("table_header_patterns", {})
    if table_headers:
        rows.append(["table header shapes", record_inline(table_headers.get("header_shapes", []), 5)])
        rows.append(["table header terms", record_inline(table_headers.get("header_terms", []), 8)])
    return rows or [["language patterns", "Unchecked"]]


def move_template_inline(move_templates: dict[str, list[dict[str, Any]]], limit: int) -> str:
    if not move_templates:
        return "Unchecked"
    chunks = []
    for move in ["context", "gap", "method", "result", "implication", "limitation"]:
        records = move_templates.get(move, [])
        if records:
            chunks.append(f"{move}: {records[0].get('pattern')}")
        if len(chunks) >= limit:
            break
    return "; ".join(chunks) if chunks else "Unchecked"


def record_inline(records: list[dict[str, Any]] | None, limit: int) -> str:
    if not records:
        return "Unchecked"
    parts = []
    for record in records[:limit]:
        pattern = record.get("pattern", "")
        count = record.get("count")
        doc_support = record.get("doc_support")
        if doc_support is not None and count is not None:
            parts.append(f"{pattern} (docs={doc_support}, n={count})")
        elif count is None:
            parts.append(str(pattern))
        else:
            parts.append(f"{pattern} ({count})")
    return "; ".join(parts) if parts else "Unchecked"


def dist_range(dist: dict[str, Any]) -> str:
    if not isinstance(dist, dict):
        return "Unchecked"
    p25 = dist.get("p25")
    p75 = dist.get("p75")
    median = dist.get("median")
    if p25 is None or p75 is None:
        return "Unchecked"
    return f"{p25} to {p75}, median {median}"


def write_revision_targets(path: Path, issues: list[dict[str, Any]]) -> None:
    lines = ["# Revision Targets", ""]
    if not issues:
        lines.append("No deterministic style targets were generated.")
    for item in issues:
        if item["severity"] == "INFO":
            continue
        lines.extend(
            [
                f"- [{item['severity']}] {item['id']}: {item['recommendation']} Use `{item['downstream_skill']}`.",
            ]
        )
    path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
