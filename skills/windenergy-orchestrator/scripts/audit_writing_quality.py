#!/usr/bin/env python3
"""Audit manuscript-level writing quality for windenergy-orchestrator workspaces."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BLOCKING_STATUSES = {"FAIL", "UNCHECKED", "NARRATIVE_WARNING", "SECTION_WARNING", "LANGUAGE_WARNING", "TONE_WARNING"}

METHOD_CITATION_TERMS = [
    "ACI",
    "AgACI",
    "FACI",
    "EnbPI",
    "NEX",
    "SPCI",
    "CQR",
    "SplitCF",
    "LCF",
]

SELF_DEFINED_METHOD_PATTERNS = [
    r"\bintroduced in this (?:paper|study|work)\b",
    r"\bwe (?:define|introduce|propose|develop)\b",
    r"\bcustom implementation\b",
    r"\bin-house implementation\b",
    r"\bimplementation label\b",
]


@dataclass
class WritingItem:
    check: str
    status: str
    detail: str
    recommendation: str


def worst_status(statuses: list[str]) -> str:
    order = {
        "PASS": 0,
        "UNCHECKED": 1,
        "NARRATIVE_WARNING": 2,
        "SECTION_WARNING": 3,
        "LANGUAGE_WARNING": 3,
        "TONE_WARNING": 3,
        "FAIL": 4,
    }
    return max(statuses or ["UNCHECKED"], key=lambda status: order.get(status, 4))


def read_latex_with_inputs(path: Path, seen: set[Path] | None = None) -> str:
    seen = seen or set()
    path = path.resolve()
    if path in seen or not path.exists():
        return ""
    seen.add(path)
    text = path.read_text(encoding="utf-8", errors="replace")

    def repl(match: re.Match[str]) -> str:
        rel = match.group(1)
        candidate = (path.parent / rel).resolve()
        if candidate.suffix == "":
            candidate = candidate.with_suffix(".tex")
        return read_latex_with_inputs(candidate, seen)

    return re.sub(r"\\(?:input|include)\{([^}]+)\}", repl, text)


def strip_latex(text: str) -> str:
    text = re.sub(r"(?<!\\)%.*", " ", text)
    text = text.replace(r"\%", "%")
    text = re.sub(r"\\begin\{(?:figure|figure\*|table|table\*|tabular|equation|align|adjustbox)\}.*?\\end\{(?:figure|figure\*|table|table\*|tabular|equation|align|adjustbox)\}", " ", text, flags=re.S)
    text = re.sub(r"\\cite[a-zA-Z*]*(?:\[[^\]]*\])*\{[^}]*\}", " ", text)
    text = re.sub(r"\\ref\{[^}]*\}", " reference ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{([^{}]*)\})?", lambda match: " " + (match.group(1) or "") + " ", text)
    text = re.sub(r"[{}_$^&~]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z0-9'-]*", strip_latex(text))


def sentence_count(text: str) -> int:
    prose = strip_latex(text)
    return len([item for item in re.split(r"[.!?]+\s+", prose) if item.strip()])


def extract_environment(tex: str, name: str) -> str:
    match = re.search(rf"\\begin\{{{re.escape(name)}\}}(.*?)\\end\{{{re.escape(name)}\}}", tex, re.S)
    return match.group(1).strip() if match else ""


def extract_sections(tex: str) -> dict[str, str]:
    matches = list(re.finditer(r"\\section\*?\{([^}]+)\}", tex))
    sections: dict[str, str] = {}
    for index, match in enumerate(matches):
        title = strip_latex(match.group(1)).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(tex)
        sections[title] = tex[start:end].strip()
    return sections


def extract_subsections(section_text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"\\subsection\*?\{([^}]+)\}", section_text))
    if not matches:
        return [("", section_text)]
    result: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        title = strip_latex(match.group(1)).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(section_text)
        result.append((title, section_text[start:end].strip()))
    return result


def split_paragraphs(section_text: str) -> list[str]:
    section_text = re.sub(r"\\begin\{(?:figure|figure\*|table|table\*)\}.*?\\end\{(?:figure|figure\*|table|table\*)\}", "\n\n", section_text, flags=re.S)
    return [para.strip() for para in re.split(r"\n\s*\n", section_text) if len(words(para)) >= 20]


def split_sentences(text: str) -> list[str]:
    prose = strip_latex(text)
    return [item.strip() for item in re.split(r"(?<=[.!?])\s+", prose) if item.strip()]


def has(patterns: list[str], text: str) -> bool:
    return any(re.search(pattern, text, re.I) for pattern in patterns)


def central_argument_item(tex: str, sections: dict[str, str]) -> WritingItem:
    title_match = re.search(r"\\title\{([^}]+)\}", tex, re.S)
    title = strip_latex(title_match.group(1)) if title_match else ""
    abstract = extract_environment(tex, "abstract")
    intro = sections.get("Introduction", "")
    discussion = sections.get("Discussion", "")
    conclusion = sections.get("Conclusion", "")

    central_terms = [term for term in ["wind", "interval", "conformal", "adaptive", "calibration"] if term in (title + abstract).lower()]
    missing_locations = []
    for name, content in [("abstract", abstract), ("introduction", intro), ("discussion", discussion), ("conclusion", conclusion)]:
        lower = strip_latex(content).lower()
        if central_terms and sum(1 for term in central_terms if term in lower) < max(2, min(3, len(central_terms))):
            missing_locations.append(name)

    boundary_patterns = [r"\bconditional\b", r"\bboundar", r"\bdepends?\b", r"\bwhen\b", r"\blimit", r"\bselection\b"]
    if not has(boundary_patterns, abstract + discussion + conclusion):
        missing_locations.append("take-home boundary")

    if missing_locations:
        return WritingItem(
            "central_argument_alignment",
            "NARRATIVE_WARNING",
            "Central argument terms or boundary message are weak in: " + ", ".join(missing_locations),
            "Revise title, abstract, introduction, discussion, and conclusion around one explicit reader takeaway.",
        )
    return WritingItem(
        "central_argument_alignment",
        "PASS",
        "Core terms and bounded take-home message are visible across foreground sections.",
        "No central argument rewrite required.",
    )


def draft_residue_item(tex: str) -> WritingItem:
    prose = strip_latex(tex)
    patterns = [
        r"Author names to be added",
        r"Affiliations to be added",
        r"Corresponding author email to be added",
        r"\bin this draft\b",
        r"\bauthor dependent\b",
        r"temporary target in this workspace",
        r"hard checks remain pending",
        r"To be completed by the authors",
        r"requires author confirmation",
        r"The current draft uses result summaries",
        r"\breviewer reorganized\b",
        r"\btarget journal is confirmed\b",
        r"\bjournal[- ]specific formatting and submission checks\b",
        r"\bsubmission checks should be applied\b",
    ]
    hits = [pattern for pattern in patterns if re.search(pattern, prose, re.I)]
    if hits:
        return WritingItem(
            "draft_residue_cleanup",
            "FAIL",
            "Submission-facing manuscript still contains draft residue or author-input placeholders: " + ", ".join(hits),
            "Delete workflow-facing phrases or replace them with completed author, journal, data, declaration, and method statements.",
        )
    return WritingItem(
        "draft_residue_cleanup",
        "PASS",
        "No configured draft residue or author-input placeholders detected.",
        "No draft-residue cleanup required.",
    )


def abstract_density_item(tex: str) -> WritingItem:
    abstract = extract_environment(tex, "abstract")
    if not abstract.strip():
        return WritingItem(
            "abstract_number_density",
            "UNCHECKED",
            "Abstract section was not found.",
            "Add an abstract before final writing review.",
        )
    prose = strip_latex(abstract)
    numeric_tokens = re.findall(r"[-+]?(?:\d+(?:,\d{3})*(?:\.\d+)?|\.\d+)\s*%?", prose)
    precise_decimals = [token for token in numeric_tokens if re.search(r"\.\d{3,}", token)]
    if len(numeric_tokens) > 8 or len(precise_decimals) > 2:
        return WritingItem(
            "abstract_number_density",
            "NARRATIVE_WARNING",
            f"Abstract contains {len(numeric_tokens)} numeric tokens and {len(precise_decimals)} high-precision decimals.",
            "Keep only the 3 to 4 numbers that anchor the central finding and move detailed values to Results.",
        )
    return WritingItem(
        "abstract_number_density",
        "PASS",
        "Abstract numeric density is within the configured readability threshold.",
        "No abstract compression required.",
    )


def section_role_item(sections: dict[str, str]) -> WritingItem:
    issues: list[str] = []
    intro = sections.get("Introduction", "")
    setup = sections.get("Experimental Setup", "")
    results = sections.get("Results", "")
    conclusion = sections.get("Conclusion", "")

    if has([r"\bwe find\b", r"\badaptive better rate\b", r"\bmean\s+\\?d?IS\b", r"\b\d+\.\d{3,}\b"], intro):
        issues.append("Introduction contains result or ranking language")
    if has([r"\bwe find\b", r"\bresults show\b", r"\bfavors\b", r"\bwins?\b"], setup):
        issues.append("Experimental Setup previews results")
    result_interpretive_hits = len(re.findall(r"\btherefore\b|\bthis implies\b|\bpractitioners should\b|\boperationally means\b", strip_latex(results), re.I))
    if result_interpretive_hits > 3:
        issues.append("Results contains too many discussion-level interpretation markers")
    if re.search(r"\\cite", conclusion):
        issues.append("Conclusion introduces citations")

    if issues:
        return WritingItem(
            "section_role_integrity",
            "SECTION_WARNING",
            "; ".join(issues),
            "Move result language out of Introduction and Setup, keep Results observational, and reserve broader meaning for Discussion.",
        )
    return WritingItem(
        "section_role_integrity",
        "PASS",
        "Major sections stay within their expected roles.",
        "No section role rewrite required.",
    )


def method_definition_item(sections: dict[str, str]) -> WritingItem:
    method = sections.get("Methodology", "")
    prose = strip_latex(method)
    issues: list[str] = []
    method_names = ["ACI", "AgACI", "EnbPI", "NEX", "SPCI"]
    present = [name for name in method_names if re.search(rf"\b{re.escape(name)}\b", prose)]
    if present:
        update_rule_hits = len(re.findall(r"\bupdate rule\b|\beffective miscoverage\b|\bnonconformity score\b|\bresidual quantile\b|\bcalibration score\b|\\eta|\\gamma|\\lambda|\\begin\{algorithm\}|\bpseudocode\b", method, re.I))
        if update_rule_hits < 3:
            issues.append("adaptive and extension methods are named without enough update-rule, score, or pseudocode detail")
    if re.search(r"\brolling\b", prose, re.I) and not re.search(r"\b168\b.*\b(sample|window)|\bwindow\b.*\b168\b", prose, re.I):
        issues.append("rolling window size is mentioned without a clear operational definition")
    if re.search(r"\bramping\b", prose, re.I) and not re.search(r"\bramp(?:ing)?\b.*\bthreshold\b|\bthreshold\b.*\bramp(?:ing)?\b|\bpower change\b.*\bramp", prose, re.I):
        issues.append("ramping appears without threshold or operational definition")
    if issues:
        return WritingItem(
            "method_definition_depth",
            "SECTION_WARNING",
            "; ".join(issues),
            "Add a benchmark algorithm box and symmetric method-definition table with update rules, signals, parameters, and operating definitions.",
        )
    return WritingItem(
        "method_definition_depth",
        "PASS",
        "Methodology has enough visible workflow, update-rule, or diagnostic definition detail for the configured review.",
        "No method-definition expansion required.",
    )


def method_citation_item(tex: str) -> WritingItem:
    body = re.sub(r"\\begin\{(?:figure|figure\*|table|table\*)\}.*?\\end\{(?:figure|figure\*|table|table\*)\}", " ", tex, flags=re.S)
    body = re.sub(r"\\(?:section|subsection|subsubsection)\*?\{[^{}]*\}", "\n\n", body)
    paragraphs = [para for para in re.split(r"\n\s*\n", body) if len(words(para)) >= 8]
    missing: list[str] = []
    for method in METHOD_CITATION_TERMS:
        method_pattern = rf"\b{re.escape(method)}\b"
        first_para = next((para for para in paragraphs if re.search(method_pattern, strip_latex(para), re.I)), "")
        if not first_para:
            continue
        has_citation = bool(re.search(r"\\cite[a-zA-Z*]*(?:\[[^\]]*\])*\{[^}]+\}", first_para))
        explicitly_defined = has(SELF_DEFINED_METHOD_PATTERNS, first_para)
        if not has_citation and not explicitly_defined:
            missing.append(method)
    if missing:
        return WritingItem(
            "method_citation_binding",
            "SECTION_WARNING",
            "Named methods lack a citation or explicit self-defined implementation note at first substantive mention: " + ", ".join(missing),
            "Attach a source citation to each external named method at first substantive mention, or state that the method is newly defined in this work.",
        )
    return WritingItem(
        "method_citation_binding",
        "PASS",
        "Configured named methods have citation or self-defined status near first substantive mention.",
        "No method-citation binding rewrite required.",
    )


def undefined_process_terms_item(tex: str) -> WritingItem:
    prose = strip_latex(tex)
    labels = sorted(set(re.findall(r"\b(?:Phase|Stage|Step)\s+\d+[A-Za-z]?\b", prose)))
    undefined: list[str] = []
    for label in labels:
        escaped = re.escape(label)
        definition_patterns = [
            rf"\b{escaped}\b\s+(?:is|denotes|refers to|captures|contains|corresponds to)\b",
            rf"\bwe define\s+{escaped}\b",
            rf"\bdefined as\s+{escaped}\b",
        ]
        if not has(definition_patterns, prose):
            undefined.append(label)
    if undefined:
        return WritingItem(
            "undefined_process_terms",
            "SECTION_WARNING",
            "Process or stage labels appear without a reader-facing definition: " + ", ".join(undefined),
            "Define each process label before use or replace it with a descriptive experimental condition.",
        )
    return WritingItem(
        "undefined_process_terms",
        "PASS",
        "No undefined numbered process labels detected.",
        "No process-term rewrite required.",
    )


def terminology_item(tex: str) -> WritingItem:
    prose = strip_latex(tex)
    high_alpha_count = len(re.findall(r"\bhigh alpha\b", prose, re.I))
    high_alpha_overcoverage = len(re.findall(r"\bhigh alpha overcoverage\b", prose, re.I))
    if high_alpha_count > 4 or high_alpha_overcoverage > 2:
        return WritingItem(
            "alpha_coverage_terminology",
            "LANGUAGE_WARNING",
            f"`high alpha` appears {high_alpha_count} times and `high alpha overcoverage` appears {high_alpha_overcoverage} times.",
            "Use reader-facing target-coverage language, such as low target coverage or narrow-interval setting, and define alpha only where needed for equations.",
        )
    return WritingItem(
        "alpha_coverage_terminology",
        "PASS",
        "Alpha and target-coverage terminology stay within the configured repetition threshold.",
        "No terminology rewrite required.",
    )


def repeated_qualification_item(tex: str) -> WritingItem:
    prose = strip_latex(tex)
    tracked = {
        "causal mechanism disclaimer": r"current diagnostics do not isolate",
        "residual structure hedge": r"consistent with the idea that residual structure matters",
        "weak mechanism compatibility hedge": r"compatible with the idea that",
        "bounded claim phrase": r"\bbounded (?:claim|interpretation|extension claim|robustness claim)\b",
        "scoped claim phrase": r"\bscoped (?:interpretation|robustness statement|extension statement|claim)\b",
    }
    overused = []
    for label, pattern in tracked.items():
        count = len(re.findall(pattern, prose, re.I))
        threshold = 1 if label == "weak mechanism compatibility hedge" else 3
        if count >= threshold:
            overused.append(f"{label}: {count}")
    if overused:
        return WritingItem(
            "repeated_qualification",
            "NARRATIVE_WARNING",
            "Overused cautious or disclaimer phrasing detected: " + "; ".join(overused),
            "State the boundary once in the relevant section, then vary phrasing and return to positive contribution language.",
        )
    return WritingItem(
        "repeated_qualification",
        "PASS",
        "Repeated cautious phrasing stays within the configured threshold.",
        "No qualification rewrite required.",
    )


def paragraph_function_item(sections: dict[str, str]) -> WritingItem:
    issues: list[str] = []
    for section_name in ["Introduction", "Related Work", "Methodology", "Experimental Setup", "Results", "Discussion", "Conclusion"]:
        paras = split_paragraphs(sections.get(section_name, ""))
        if not paras:
            issues.append(f"{section_name} has no substantial prose paragraphs")
            continue
        long_paras = [len(words(para)) for para in paras if len(words(para)) > 230]
        if long_paras:
            issues.append(f"{section_name} has overlong paragraphs")

    intro_paras = split_paragraphs(sections.get("Introduction", ""))
    if intro_paras and not has([r"\bhowever\b", r"\byet\b", r"\bunresolved\b", r"\bdifficulty\b", r"\bchallenge\b"], intro_paras[0] + " " + (intro_paras[1] if len(intro_paras) > 1 else "")):
        issues.append("Introduction opening lacks visible tension")

    if issues:
        return WritingItem(
            "paragraph_function_flow",
            "SECTION_WARNING",
            "; ".join(issues[:8]),
            "Assign each paragraph one job: tension, gap, design, evidence, interpretation, boundary, or transition.",
        )
    return WritingItem(
        "paragraph_function_flow",
        "PASS",
        "Sections contain substantial prose with manageable paragraph flow.",
        "No paragraph-function rewrite required.",
    )


def related_work_gap_item(sections: dict[str, str]) -> WritingItem:
    related = sections.get("Related Work", "")
    prose = strip_latex(related)
    issues: list[str] = []
    if len(words(related)) < 700:
        issues.append("Related Work is short for a full manuscript")
    if len(re.findall(r"\\subsection", related)) < 3:
        issues.append("Related Work lacks at least three literature lines")
    if not has([r"\bstrand\b", r"\bresearch line\b", r"\bliterature line\b", r"\bstudies establish\b", r"\bthis literature\b"], prose):
        issues.append("Related Work does not visibly group literature lines")
    if not has([r"\bunresolved\b", r"\bremains? unclear\b", r"\brarely\b", r"\bless clear\b", r"\bgap\b"], prose):
        issues.append("Related Work does not validate a clear gap")

    if issues:
        return WritingItem(
            "related_work_gap_strength",
            "SECTION_WARNING",
            "; ".join(issues),
            "Rewrite Related Work as a literature map with established knowledge, unresolved gap, and manuscript novelty boundary.",
        )
    return WritingItem(
        "related_work_gap_strength",
        "PASS",
        "Related Work has literature lines and an explicit unresolved gap.",
        "No Related Work gap rewrite required.",
    )


def results_storyline_item(sections: dict[str, str]) -> WritingItem:
    results = sections.get("Results", "")
    subsections = [(title, body) for title, body in extract_subsections(results) if len(words(body)) >= 60]
    issues: list[str] = []
    if len(subsections) < 3:
        issues.append("Results lacks enough substantive result blocks")
    for title, body in subsections:
        paras = split_paragraphs(body)
        first = paras[0] if paras else body[:800]
        if not has([r"\bcentral\b", r"\bshows?\b", r"\bindicates?\b", r"\breports?\b", r"\bpattern\b"], first):
            issues.append(f"{title or 'unnamed result block'} lacks a finding lead")
        if "\\ref{" not in body and "\\includegraphics" not in body and "\\begin{table" not in body:
            issues.append(f"{title or 'unnamed result block'} lacks a visible display item")
        if not has([r"\bwhile\b", r"\bhowever\b", r"\bboundary\b", r"\blimit", r"\bcautious\b", r"\bconditional\b"], body):
            issues.append(f"{title or 'unnamed result block'} lacks boundary language")

    if issues:
        return WritingItem(
            "results_storyline",
            "SECTION_WARNING",
            "; ".join(issues[:10]),
            "Rewrite each Results subsection as finding, evidence, diagnostic comparison, boundary, and transition.",
        )
    return WritingItem(
        "results_storyline",
        "PASS",
        "Results blocks contain finding leads, display-item support, and boundary language.",
        "No Results storyline rewrite required.",
    )


def discussion_depth_item(sections: dict[str, str]) -> WritingItem:
    discussion = sections.get("Discussion", "")
    results = sections.get("Results", "")
    prose = strip_latex(discussion)
    issues: list[str] = []
    if len(words(discussion)) < 500:
        issues.append("Discussion is too short for interpretation and boundary synthesis")
    if not has([r"\bmeans\b", r"\bmatters\b", r"\boperational\b", r"\bpractical\b", r"\bselection logic\b", r"\bfor applied use\b"], prose):
        issues.append("Discussion lacks field meaning or operational interpretation")
    if not has([r"\blimitation", r"\bbound", r"\bremains\b", r"\brequire", r"\bwould\b"], prose):
        issues.append("Discussion lacks visible evidence boundary")
    if "\\cite" not in discussion:
        issues.append("Discussion does not reconnect findings to specific literature")
    numeric_tokens = len(re.findall(r"\b\d+(?:\.\d+)?\b", prose))
    if numeric_tokens > 35:
        issues.append("Discussion repeats many numeric results")
    result_sentences = [set(words(sentence.lower())) for sentence in split_sentences(results) if len(words(sentence)) >= 8]
    repeated_sentences = 0
    for sentence in split_sentences(discussion):
        tokens = set(words(sentence.lower()))
        if len(tokens) < 8 or not result_sentences:
            continue
        overlap = max((len(tokens & other) / max(1, len(tokens | other)) for other in result_sentences), default=0.0)
        if overlap >= 0.55:
            repeated_sentences += 1
    if repeated_sentences >= 2:
        issues.append("Discussion repeats Results sentences with limited synthesis")

    if issues:
        return WritingItem(
            "discussion_depth",
            "NARRATIVE_WARNING",
            "; ".join(issues),
            "Revise Discussion to explain field meaning, rival interpretations, boundaries, and decision implications without rerunning Results.",
        )
    return WritingItem(
        "discussion_depth",
        "PASS",
        "Discussion provides interpretation, boundary, and applied meaning.",
        "No Discussion depth rewrite required.",
    )


def table_language_item(tex: str) -> WritingItem:
    issues: list[str] = []
    tables = "\n".join(re.findall(r"\\begin\{table\*?\}.*?\\end\{table\*?\}", tex, re.I | re.S))
    if re.search(r"\b(Supported observation|Unsupported|Evidence status)\b", tables, re.I) and not re.search(
        r"\b(statistical support|p[- ]?value|confidence interval|CI|bootstrap|not applicable|N/A|not tested)\b",
        tables,
        re.I,
    ):
        issues.append("evidence-status table lacks a statistical-support column or explicit not-applicable rationale")
    if re.search(r"\bstored verdict\b|\bstored benchmark\b|\bstored diagnostic\b", tex, re.I):
        issues.append("table or prose contains workflow-derived stored-verdict language")
    if re.search(r"Claim area\s*&\s*Main quantitative support\s*&\s*Boundary", tex, re.I):
        issues.append("claim summary table uses broad Boundary column without separating evidence status, limitation, and statistical support")
    if re.search(r"88,704", tex) and not re.search(r"4\s*\\times\s*24\s*\\times\s*11\s*\\times\s*4\s*\\times\s*7\s*\\times\s*3|4×24×11×4×7×3|4 x 24 x 11 x 4 x 7 x 3", tex):
        issues.append("88,704 run count appears without a visible calculation formula")
    if issues:
        return WritingItem(
            "table_claim_language",
            "SECTION_WARNING",
            "; ".join(issues),
            "Revise tables so claims, evidence strength, limitations, and statistical support use standard scholarly labels and traceable run-count logic.",
        )
    return WritingItem(
        "table_claim_language",
        "PASS",
        "Configured table-language and run-count checks passed.",
        "No table-language rewrite required.",
    )


def audit_writing_quality(workspace: Path, tex_rel: str | None = None) -> dict[str, Any]:
    workspace = workspace.resolve()
    candidates = []
    if tex_rel:
        candidates.append(workspace / tex_rel)
    candidates.extend([
        workspace / "drafts" / "paper_polished.tex",
        workspace / "drafts" / "paper.tex",
        workspace / "final" / "paper.tex",
    ])
    tex_path = next((path for path in candidates if path.exists()), candidates[0])
    tex = read_latex_with_inputs(tex_path)
    sections = extract_sections(tex)

    items = [
        draft_residue_item(tex),
        abstract_density_item(tex),
        central_argument_item(tex, sections),
        section_role_item(sections),
        method_definition_item(sections),
        method_citation_item(tex),
        undefined_process_terms_item(tex),
        terminology_item(tex),
        repeated_qualification_item(tex),
        paragraph_function_item(sections),
        related_work_gap_item(sections),
        results_storyline_item(sections),
        discussion_depth_item(sections),
        table_language_item(tex),
    ]
    status = worst_status([item.status for item in items])
    report = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "workspace": str(workspace),
        "tex_path": str(tex_path),
        "status": status,
        "items": [item.__dict__ for item in items],
    }
    return report


def write_outputs(workspace: Path, report: dict[str, Any]) -> None:
    audits = workspace / "audits"
    audits.mkdir(parents=True, exist_ok=True)
    (audits / "writing_quality_audit.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# Writing Quality Audit",
        "",
        f"Overall status: {report['status']}",
        "",
        "| Check | Status | Detail | Recommendation |",
        "|---|---|---|---|",
    ]
    for item in report["items"]:
        lines.append(f"| {item['check']} | {item['status']} | {item['detail']} | {item['recommendation']} |")
    (audits / "writing_quality_audit.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    plan_lines = ["# Writing Revision Plan", ""]
    blocking = [item for item in report["items"] if item["status"] in BLOCKING_STATUSES]
    if not blocking:
        plan_lines.append("No blocking writing revisions are required by the writing quality audit.")
    else:
        for index, item in enumerate(blocking, start=1):
            plan_lines.extend([
                f"## R{index}: {item['check']}",
                "",
                f"Status: {item['status']}",
                "",
                f"Issue: {item['detail']}",
                "",
                f"Revision target: {item['recommendation']}",
                "",
            ])
    (audits / "writing_revision_plan.md").write_text("\n".join(plan_lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace")
    parser.add_argument("--tex", help="Optional manuscript path relative to workspace")
    parser.add_argument("--strict", action="store_true", help="Return nonzero unless the writing audit PASSes")
    args = parser.parse_args()

    workspace = Path(args.workspace).resolve()
    report = audit_writing_quality(workspace, args.tex)
    write_outputs(workspace, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.strict and report["status"] != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
