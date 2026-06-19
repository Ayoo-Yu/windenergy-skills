#!/usr/bin/env python3
"""Run manuscript, figure, and mechanism quality audits for orchestrator workspaces."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


MAIN_BODY_START_TITLE = "Introduction"
MAIN_BODY_END_TITLE = "Conclusion"

STATUS_ORDER = {
    "PASS": 0,
    "SECTION_WARNING": 1,
    "NARRATIVE_WARNING": 2,
    "LANGUAGE_WARNING": 2,
    "TONE_WARNING": 2,
    "UNCHECKED": 3,
    "AUTHOR_INPUT_NEEDED": 4,
    "FAIL": 5,
}

DEFAULT_JOURNAL_DECLARATIONS = [
    "data_availability",
    "competing_interests",
    "credit_author_statement",
]

DECLARATION_PATTERNS = {
    "data_availability": [
        r"\\section\*?\{(?:Code and )?Data Availability\}",
        r"\\section\*?\{Data and Code Availability\}",
    ],
    "competing_interests": [
        r"\\section\*?\{Declaration of Competing Interests?\}",
        r"\\section\*?\{Conflict[s]? of Interest\}",
        r"\\section\*?\{Declaration of Interest Statement\}",
    ],
    "credit_author_statement": [
        r"\\section\*?\{CRediT Author Statement\}",
        r"\\section\*?\{Author Contributions?\}",
        r"\bCRediT\b",
    ],
}

COLORBLIND_SAFE_PALETTE_TOKENS = [
    "okabe",
    "ito",
    "colorblind",
    "cividis",
    "viridis",
    "plasma",
    "tol",
    "tableau",
]

GENERIC_SETUP_REQUIREMENTS = [
    ("data_source", [r"data source", r"dataset", r"data were", r"data come from", r"measurement"]),
    ("sampling_interval", [r"sampling interval", r"sampled", r"resolution", r"\b\d+\s*(min|minute|hour)"]),
    ("time_span", [r"time span", r"time period", r"from\s+\d{4}", r"\d{4}\s*to\s*\d{4}", r"period"]),
    ("evaluation_split", [r"train", r"test", r"split", r"validation", r"chronological"]),
    ("input_features", [r"input feature", r"feature set", r"covariate", r"predictor input"]),
    ("target_variable", [r"target variable", r"target", r"output variable", r"response variable"]),
    ("missing_values", [r"missing value", r"missing data", r"imputation", r"removed missing"]),
    ("exclusions", [r"exclusion", r"excluded", r"filter", r"preprocess", r"pre-processing"]),
]

GENERIC_METHOD_REQUIREMENTS = [
    ("algorithm_or_workflow", [r"algorithm", r"workflow", r"procedure", r"pipeline", r"formulation", r"model"]),
    ("assumptions", [r"assumption", r"assume", r"condition", r"constraint"]),
    ("parameters_or_settings", [r"parameter", r"setting", r"configuration", r"hyperparameter"]),
    ("implementation_detail", [r"implementation", r"software", r"code", r"solver", r"training"]),
]

CORE_EVIDENCE_GAPS = [
    r"additional diagnostic",
    r"additional experiment",
    r"future study",
    r"future work",
]

WORKFLOW_REQUIRED_CONCEPTS = [
    "research object",
    "comparison unit",
    "alternatives",
    "diagnostic layer",
    "boundary analysis",
]

FIGURE_PORTFOLIO_ROLES = [
    "workflow",
    "data or task overview",
    "method comparison",
    "condition boundary",
    "mechanism evidence",
    "robustness",
    "deployment guidance",
]

INTERNAL_ARTIFACT_PATTERNS = [
    r"local experiment tree",
    r"source[-_ ]code evidence register",
    r"source_code_evidence_register\.md",
    r"claim_evidence_map\.md",
    r"mechanism_diagnostics\.md",
    r"figure_data_map\.json",
    r"figure data map\.json",
]

LANGUAGE_WARNING_PATTERNS = [
    r"source[- ]code[- ]verified",
    r"source[- ]code setting",
    r"diagnostic file",
    r"saved key slices",
    r"configuration file",
    r"output folder",
    r"run log",
    r"pipeline stage",
    r"revision workspace",
    r"regenerated diagnostic",
    r"control file",
    r"\b[A-Za-z0-9_./-]+\.(py|json|csv|md|pth|pkl)\b",
]

TONE_WARNING_PATTERNS = [
    r"to (avoid|prevent|address) (potential )?(reviewer )?concerns?",
    r"common reviewer question",
    r"reviewers? may (argue|ask|question)",
    r"one might argue",
    r"it is worth noting that this design avoids",
    r"we do not claim that",
    r"to preempt",
]

TITLE_STRONG_PATTERNS = [
    r"mechanism diagnosis",
    r"mechanism diagnostic",
    r"mechanistic diagnosis",
    r"mechanistic explanation",
]

EVIDENCE_BOUNDARY_WEAKNESS_PATTERNS = [
    r"partial",
    r"aggregate proxy",
    r"proxy",
    r"not fully saved",
    r"not completely saved",
    r"unavailable",
    r"not available",
    r"future work",
]

ADVICE_PATTERNS = [r"deploy", r"operational", r"selection", r"choose", r"recommend"]
GRANULARITY_PATTERNS = [r"per[- ]method", r"method[- ]level", r"individual", r"per[- ]case", r"case[- ]level"]

INTRODUCTION_SPOILER_PATTERNS = {
    "results-heavy wording": [
        r"\bwe\s+find\s+that\b",
        r"\bwe\s+found\s+that\b",
        r"\bresults?\s+(show|shows|indicate|indicates|demonstrate|demonstrates)\b",
        r"\bthe\s+evidence\s+(show|shows|indicate|indicates)\b",
        r"\bthis\s+implies\s+that\b",
    ],
    "final method ranking": [
        r"\bbest[- ]performing\b",
        r"\bworst[- ]performing\b",
        r"\boutperform(?:s|ed|ing)?\b",
        r"\bdominates?\b",
        r"\bwins?\b",
        r"\bis\s+preferable\b",
        r"\bis\s+favou?red\b",
    ],
    "detailed numerical outcome": [
        r"\b\d+(?:\.\d+)?\s*%\s+(improvement|reduction|increase|decrease|gain|loss)\b",
        r"\b(improves|reduces|increases|decreases|lowers|raises)\b.{0,60}\b\d+(?:\.\d+)?\s*%\b",
        r"\b\d+(?:\.\d+)?\s+(points|percentage points)\b",
    ],
    "operational recommendation": [
        r"\bwe\s+recommend\b",
        r"\bpractitioners\s+should\b",
        r"\bshould\s+be\s+(selected|chosen|deployed|used)\b",
        r"\boperational\s+recommendation\b",
    ],
    "operating-boundary conclusion": [
        r"\bworks\s+best\s+when\b",
        r"\bhelps\s+when\b",
        r"\bfails\s+when\b",
        r"\bis\s+preferable\s+under\b",
        r"\bis\s+favou?red\s+under\b",
    ],
}

RELATED_WORK_MAP_PATTERNS = [
    r"research line",
    r"strand",
    r"body of work",
    r"literature",
    r"studies",
    r"prior work",
    r"foundational",
    r"recent",
    r"competitor",
]

RELATED_WORK_SYNTHESIS_PATTERNS = [
    r"assumption",
    r"mechanism",
    r"paradigm",
    r"method family",
    r"evaluation",
    r"benchmark",
    r"data setting",
    r"operational context",
    r"failure mode",
]

RELATED_WORK_GAP_PATTERNS = [
    r"gap",
    r"unresolved",
    r"remain",
    r"limitation",
    r"open question",
    r"unclear",
    r"less clear",
    r"under[- ]studied",
]

RELATED_WORK_CURRENT_PAPER_PATTERNS = [
    r"\bthis paper\b",
    r"\bour (method|study|paper|benchmark|framework|experiment|evaluation)\b",
    r"\bwe (use|compare|evaluate|develop|propose|test|show|find|report)\b",
]

RELATED_WORK_PROTOCOL_PATTERNS = [
    r"\btraining\b",
    r"\btrain(?:ing)?[- ]validation[- ]test\b",
    r"\btest split\b",
    r"\bmultiple seeds?\b",
    r"\bexperimental protocol\b",
    r"\bimplementation setting\b",
    r"\bwe use\b",
    r"\bwe evaluate\b",
]

RELATED_WORK_RESULT_PATTERNS = [
    r"\bwe find that\b",
    r"\bwe show that\b",
    r"\bthis paper shows\b",
    r"\bresults? (show|shows|indicate|indicates|demonstrate|demonstrates)\b",
    r"\boutperform(?:s|ed|ing)?\b.{0,80}\bthis paper\b",
    r"\b\d+(?:\.\d+)?\s*%\s+(improvement|reduction|increase|decrease|gain|loss)\b",
]

TOPIC_REQUIREMENTS = {
    "wind-power-forecasting": {
        "setup": [
            ("forecast_time_scale", [r"lead time", r"time scale", r"forecast horizon", r"forecast period"]),
            ("operating_filter", [r"operating", r"abnormal", r"curtail", r"filter", r"exclusion"]),
        ]
    },
    "probabilistic-forecasting": {
        "method": [
            ("uncertainty_target", [r"uncertainty", r"quantile", r"interval", r"distribution", r"risk"]),
            ("reliability_or_sharpness", [r"reliability", r"sharpness", r"calibration", r"scoring rule"]),
        ]
    },
    "conformal-calibration": {
        "method": [
            ("score_definition", [r"score definition", r"nonconformity", r"calibration score", r"interval score"]),
            ("calibration_protocol", [r"calibration", r"exchangeability", r"online", r"adaptive"]),
            ("update_or_window", [r"update", r"window", r"memory", r"step size", r"learning rate"]),
            ("delayed_label_or_timing", [r"delayed label", r"label delay", r"available after", r"forecast origin", r"online timing"]),
        ],
        "evidence": [
            ("interval_score_decomposition", [r"interval score decomposition", r"width contribution", r"lower miss", r"upper miss"]),
            ("matched_width_comparison", [r"width[- ]matched", r"matched width"]),
            ("matched_reliability_comparison", [r"coverage[- ]matched", r"matched reliability", r"same empirical reliability"]),
        ],
    },
}

JOURNAL_THRESHOLDS = {
    "applied-energy": {
        "main_body_min_words": 5000,
        "main_body_target_words": 7000,
        "reference_min": 40,
        "min_figures": 10,
        "min_display_items": 12,
        "display_item_range": "12 to 18 display items",
        "required_declarations": DEFAULT_JOURNAL_DECLARATIONS,
    }
}

PROFILE_CONTRACT_FIELDS = [
    "paper_type",
    "topics",
    "journal",
    "paper_type_confidence",
    "topic_confidence",
    "journal_confidence",
    "profile_source",
    "loaded_fragments",
    "disabled_fragments",
    "quality_thresholds",
    "routing_notes",
]

FALLBACK_PROFILE_PATTERNS = [
    r"local paper workflow",
    r"paper workflow equivalents",
    r"fallback",
    r"not exposed",
    r"absent in this session",
]


@dataclass
class AuditItem:
    check: str
    status: str
    detail: str


def worst_status(statuses: list[str]) -> str:
    if not statuses:
        return "PASS"
    return max(statuses, key=lambda value: STATUS_ORDER.get(value, 3))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_latex_with_inputs(path: Path, seen: set[Path] | None = None) -> str:
    seen = seen or set()
    path = path.resolve()
    if path in seen:
        return ""
    seen.add(path)
    text = read_text(path)
    if not text:
        return text

    def replace_input(match: re.Match[str]) -> str:
        raw = match.group("path").strip()
        candidates = [path.parent / raw]
        if not Path(raw).suffix:
            candidates.append(path.parent / f"{raw}.tex")
        for candidate in candidates:
            candidate = candidate.resolve()
            if candidate.exists():
                return read_latex_with_inputs(candidate, seen)
        return match.group(0)

    return re.sub(r"\\(?:input|include)\{(?P<path>[^{}]+)\}", replace_input, text)


def slugify(value: Any) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def normalize_profile(data: dict[str, Any]) -> dict[str, Any]:
    nested = data.get("profile")
    if isinstance(nested, dict):
        for key in ["paper_type", "topics", "journal", "manuscript_fragment"]:
            if key not in data and key in nested:
                data[key] = nested[key]
        if "confidence" in nested and "topic_confidence" not in data:
            confidence = str(nested.get("confidence", "")).lower()
            confidence_value = {"high": 0.95, "medium": 0.80, "low": 0.60}.get(confidence, 0.0)
            topics = nested.get("topics", [])
            if isinstance(topics, str):
                topics = [topics]
            data["topic_confidence"] = {slugify(topic): confidence_value for topic in topics}
            data.setdefault("journal_confidence", confidence_value if nested.get("journal") else 0.0)
            data.setdefault("paper_type_confidence", confidence_value if nested.get("paper_type") else 0.0)
    return data


def profile_contract_issues(profile: dict[str, Any]) -> list[str]:
    issues = []
    missing = [field for field in PROFILE_CONTRACT_FIELDS if field not in profile]
    if missing:
        issues.append("missing profile contract fields: " + ", ".join(missing))
    mapping = profile.get("workflow_skill_mapping", {})
    mapping_text = json.dumps(mapping, ensure_ascii=False).lower() if isinstance(mapping, dict) else str(mapping).lower()
    if any(re.search(pattern, mapping_text, re.I) for pattern in FALLBACK_PROFILE_PATTERNS):
        issues.append("workflow profile records fallback or local workflow equivalents instead of renewable skills")
    return issues


def load_profile(workspace: Path, profile_rel: str | None = None) -> dict[str, Any]:
    candidates = []
    if profile_rel:
        candidates.append(workspace / profile_rel)
    candidates.append(workspace / "workflow_profile.json")
    for path in candidates:
        if path.exists():
            try:
                data = json.loads(read_text(path))
            except json.JSONDecodeError:
                return {"profile_status": "FAIL", "profile_path": str(path), "routing_notes": ["invalid JSON"]}
            if isinstance(data, dict):
                data = normalize_profile(data)
                data.setdefault("profile_status", "PASS")
                data.setdefault("profile_path", str(path))
                return data
    return {
        "profile_status": "UNCHECKED",
        "paper_type": "generic",
        "topics": [],
        "journal": "",
        "topic_confidence": {},
        "loaded_fragments": [],
        "disabled_fragments": [],
        "quality_thresholds": {},
        "routing_notes": ["workflow_profile.json missing"],
    }


def profile_topics(profile: dict[str, Any], minimum_confidence: float = 0.85) -> set[str]:
    topics = profile.get("topics", [])
    if isinstance(topics, str):
        topics = [topics]
    confidence = profile.get("topic_confidence", {})
    selected = set()
    for topic in topics:
        slug = slugify(topic)
        if not slug.strip():
            continue
        value = 1.0
        if isinstance(confidence, dict) and slug in {slugify(key) for key in confidence}:
            for key, raw_value in confidence.items():
                if slugify(key) == slug:
                    try:
                        value = float(raw_value)
                    except (TypeError, ValueError):
                        value = 0.0
                    break
        if value >= minimum_confidence:
            selected.add(slug)
    return selected


def profile_journal(profile: dict[str, Any]) -> str:
    return slugify(profile.get("journal", "") or "")


def profile_threshold(profile: dict[str, Any], key: str) -> Any:
    thresholds = profile.get("quality_thresholds", {})
    if isinstance(thresholds, dict) and key in thresholds:
        return thresholds[key]
    journal = profile_journal(profile)
    return JOURNAL_THRESHOLDS.get(journal, {}).get(key)


def profile_required_declarations(profile: dict[str, Any]) -> list[str]:
    configured = profile_threshold(profile, "required_declarations")
    if isinstance(configured, list):
        return [str(item) for item in configured if str(item).strip()]
    if profile.get("profile_status") == "PASS" and profile_journal(profile):
        return list(DEFAULT_JOURNAL_DECLARATIONS)
    return []


def declaration_integrity_items(tex: str, profile: dict[str, Any]) -> list[AuditItem]:
    required = profile_required_declarations(profile)
    if not required:
        return [AuditItem("declaration_integrity", "PASS", "No target-journal declaration checklist is active.")]

    missing = []
    for name in required:
        patterns = DECLARATION_PATTERNS.get(name, [])
        if patterns and not has_any(tex, patterns):
            missing.append(name)
    if missing:
        return [
            AuditItem(
                "declaration_integrity",
                "AUTHOR_INPUT_NEEDED",
                "Target profile requires declaration sections that are missing from the manuscript: " + ", ".join(missing),
            )
        ]
    return [AuditItem("declaration_integrity", "PASS", "Target-profile declaration sections are present.")]


def profile_setup_requirements(profile: dict[str, Any]) -> list[tuple[str, list[str]]]:
    requirements = list(GENERIC_SETUP_REQUIREMENTS)
    for topic in profile_topics(profile):
        requirements.extend(TOPIC_REQUIREMENTS.get(topic, {}).get("setup", []))
    return requirements


def profile_method_requirements(profile: dict[str, Any]) -> list[tuple[str, list[str]]]:
    requirements = list(GENERIC_METHOD_REQUIREMENTS)
    for topic in profile_topics(profile):
        requirements.extend(TOPIC_REQUIREMENTS.get(topic, {}).get("method", []))
    return requirements


def profile_evidence_requirements(profile: dict[str, Any]) -> list[tuple[str, list[str]]]:
    requirements: list[tuple[str, list[str]]] = []
    for topic in profile_topics(profile):
        requirements.extend(TOPIC_REQUIREMENTS.get(topic, {}).get("evidence", []))
    custom = profile.get("evidence_requirements", [])
    if isinstance(custom, list):
        for item in custom:
            if isinstance(item, dict) and item.get("name") and item.get("patterns"):
                patterns = item["patterns"] if isinstance(item["patterns"], list) else [str(item["patterns"])]
                requirements.append((str(item["name"]), [str(pattern) for pattern in patterns]))
    return requirements


def profile_figure_thresholds(profile: dict[str, Any]) -> tuple[int | None, int | None, str]:
    min_figures = profile_threshold(profile, "min_figures")
    min_display = profile_threshold(profile, "min_display_items")
    display_range = str(profile_threshold(profile, "display_item_range") or "profile target")
    try:
        min_figures_value = int(min_figures) if min_figures is not None else None
    except (TypeError, ValueError):
        min_figures_value = None
    try:
        min_display_value = int(min_display) if min_display is not None else None
    except (TypeError, ValueError):
        min_display_value = None
    return min_figures_value, min_display_value, display_range


def strip_environment(text: str, names: list[str]) -> str:
    for name in names:
        text = re.sub(rf"\\begin\{{{name}\}}.*?\\end\{{{name}\}}", " ", text, flags=re.S)
    return text


def strip_latex_to_words(text: str) -> str:
    text = re.sub(r"(?<!\\)%.*", " ", text)
    text = strip_environment(
        text,
        [
            "table",
            "table*",
            "figure",
            "figure*",
            "equation",
            "equation*",
            "align",
            "align*",
            "tabular",
        ],
    )
    text = re.sub(r"\$.*?\$", " ", text, flags=re.S)
    text = re.sub(r"\\(?:section|subsection|subsubsection)\*?\{([^{}]*)\}", r" \1 ", text)
    text = re.sub(r"\\(?:cite|ref|label|includegraphics|bibliography|bibliographystyle)(?:\[[^\]]*\])?\{[^{}]*\}", " ", text)
    text = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", " ", text)
    text = re.sub(r"[{}_^&]", " ", text)
    return text


def extract_title(tex: str) -> str:
    match = re.search(r"\\title\{(?P<title>[^{}]*)\}", tex, re.S)
    return strip_latex_to_words(match.group("title")) if match else ""


def main_text_without_reproducibility_or_appendix(tex: str) -> str:
    cut_points = []
    for pattern in [
        r"\\appendix\b",
        r"\\section\*?\{Reproducibility Statement\}",
        r"\\section\*?\{Code and Data Availability\}",
    ]:
        match = re.search(pattern, tex, re.I)
        if match:
            cut_points.append(match.start())
    return tex[: min(cut_points)] if cut_points else tex


def count_latex_environment(tex: str, name: str) -> int:
    return len(re.findall(rf"\\begin\{{{name}\*?\}}", tex))


def count_bib_entries(workspace: Path) -> tuple[int, str]:
    for rel in ["final/refs.bib", "literature/refs.bib", "refs.bib"]:
        path = workspace / rel
        if path.exists():
            text = read_text(path)
            return len(re.findall(r"@\w+\s*\{", text)), rel
    return 0, ""


def count_words(text: str) -> int:
    return len(re.findall(r"[A-Za-z][A-Za-z0-9']*", strip_latex_to_words(text)))


def extract_main_body(tex: str) -> tuple[str, list[str]]:
    """Return text from Introduction through Conclusion, excluding front/back matter."""
    section_pattern = re.compile(r"\\section\*?\{(?P<title>[^{}]*)\}")
    sections = list(section_pattern.finditer(tex))
    missing: list[str] = []
    start_index = next(
        (idx for idx, match in enumerate(sections) if match.group("title").strip().lower() == MAIN_BODY_START_TITLE.lower()),
        None,
    )
    end_index = next(
        (idx for idx, match in enumerate(sections) if match.group("title").strip().lower() == MAIN_BODY_END_TITLE.lower()),
        None,
    )
    if start_index is None:
        missing.append(MAIN_BODY_START_TITLE)
    if end_index is None:
        missing.append(MAIN_BODY_END_TITLE)
    if start_index is None or end_index is None or end_index < start_index:
        return "", missing
    start = sections[start_index].start()
    end = sections[end_index + 1].start() if end_index + 1 < len(sections) else len(tex)
    return tex[start:end], missing


def extract_blocks(tex: str) -> list[dict[str, Any]]:
    pattern = re.compile(r"\\(?P<level>section|subsection|subsubsection)\*?\{(?P<title>[^{}]*)\}")
    matches = list(pattern.finditer(tex))
    blocks: list[dict[str, Any]] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(tex)
        blocks.append(
            {
                "level": match.group("level"),
                "title": match.group("title").strip(),
                "body": tex[start:end],
            }
        )
    return blocks


def find_block(blocks: list[dict[str, Any]], title: str) -> str:
    wanted = title.lower()
    for index, block in enumerate(blocks):
        if block["title"].lower() == wanted:
            parts = [str(block["body"])]
            if block.get("level") == "section":
                for child in blocks[index + 1 :]:
                    if child.get("level") == "section":
                        break
                    parts.append(str(child.get("body", "")))
            return "\n".join(parts)
    return ""


def has_any(text: str, patterns: list[str]) -> bool:
    return any(re.search(pattern, text, re.I) for pattern in patterns)


def extract_abstract(tex: str) -> str:
    match = re.search(r"\\begin\{abstract\}(?P<body>.*?)\\end\{abstract\}", tex, re.S | re.I)
    return match.group("body") if match else ""


def narrative_warning_items(tex: str, blocks: list[dict[str, Any]]) -> list[AuditItem]:
    items: list[AuditItem] = []
    abstract = extract_abstract(tex)
    intro = find_block(blocks, "Introduction")
    conclusion = find_block(blocks, "Conclusion")
    title = extract_title(tex)
    foreground = {
        "title": title,
        "abstract": abstract,
        "introduction": intro,
        "conclusion": conclusion,
    }
    tension_patterns = [r"however", r"yet", r"challenge", r"gap", r"unresolved", r"unclear", r"unknown", r"limited"]
    takeaway_patterns = [r"therefore", r"overall", r"take-home", r"implies", r"suggests", r"provides", r"shows", r"indicates", r"principle", r"boundary", r"guidance"]
    warnings = []
    for name, text in foreground.items():
        if not text.strip():
            continue
        words = count_words(text)
        if name in {"abstract", "introduction"} and words > 40 and not has_any(text, tension_patterns):
            warnings.append(f"{name} lacks visible problem tension")
        if name in {"abstract", "conclusion"} and words > 40 and not has_any(text, takeaway_patterns):
            warnings.append(f"{name} lacks a clear take-home message")
    if warnings:
        items.append(AuditItem("foreground_narrative", "NARRATIVE_WARNING", "; ".join(warnings)))
    else:
        items.append(AuditItem("foreground_narrative", "PASS", "Foreground sections have narrative tension or take-home synthesis where present."))
    return items


def introduction_spoiler_items(blocks: list[dict[str, Any]]) -> list[AuditItem]:
    intro = find_block(blocks, "Introduction")
    if not intro.strip():
        return [AuditItem("introduction_spoiler_control", "UNCHECKED", "Introduction section was not found.")]

    hits: list[str] = []
    for category, patterns in INTRODUCTION_SPOILER_PATTERNS.items():
        if has_any(intro, patterns):
            hits.append(category)

    if hits:
        return [
            AuditItem(
                "introduction_spoiler_control",
                "NARRATIVE_WARNING",
                "Introduction appears to report material reserved for Results or Discussion: " + ", ".join(hits) + ".",
            )
        ]
    return [
        AuditItem(
            "introduction_spoiler_control",
            "PASS",
            "Introduction previews the question, evidence design, and contribution types without detailed result leakage.",
        )
    ]


def related_work_synthesis_items(blocks: list[dict[str, Any]]) -> list[AuditItem]:
    related = find_block(blocks, "Related Work")
    if not related.strip():
        return [AuditItem("related_work_synthesis_control", "UNCHECKED", "Related Work section was not found.")]

    prose = strip_environment(related, ["table", "table*", "figure", "figure*", "tabular"])
    words = count_words(prose)
    citations = len(re.findall(r"\\cite", related))
    current_paper_hits = sum(len(re.findall(pattern, prose, re.I)) for pattern in RELATED_WORK_CURRENT_PAPER_PATTERNS)
    issues: list[str] = []

    if words < 120:
        issues.append(f"section is too short for literature synthesis ({words} words)")
    if citations < 3:
        issues.append(f"few representative citations ({citations} citation commands)")
    if not has_any(prose, RELATED_WORK_MAP_PATTERNS):
        issues.append("no visible literature map or research-line organization")
    if not has_any(prose, RELATED_WORK_SYNTHESIS_PATTERNS):
        issues.append("limited comparison of assumptions, mechanisms, evaluation, or context")
    if not has_any(prose, RELATED_WORK_GAP_PATTERNS):
        issues.append("no explicit unresolved gap")
    if current_paper_hits > 3:
        issues.append("current-paper transitions are overused")
    if has_any(prose, RELATED_WORK_PROTOCOL_PATTERNS):
        issues.append("methodology or protocol detail appears before Methodology")
    if has_any(prose, RELATED_WORK_RESULT_PATTERNS):
        issues.append("result or ranking language appears before Results")

    if issues:
        return [
            AuditItem(
                "related_work_synthesis_control",
                "SECTION_WARNING",
                "; ".join(issues),
            )
        ]
    return [
        AuditItem(
            "related_work_synthesis_control",
            "PASS",
            "Related Work maps literature lines, representative citations, synthesis dimensions, and unresolved gaps.",
        )
    ]


def language_and_tone_items(tex: str) -> list[AuditItem]:
    main_text = main_text_without_reproducibility_or_appendix(tex)
    items: list[AuditItem] = []

    language_hits = [pattern for pattern in LANGUAGE_WARNING_PATTERNS if re.search(pattern, main_text, re.I)]
    if language_hits:
        items.append(
            AuditItem(
                "internal_workflow_language_warning",
                "LANGUAGE_WARNING",
                "Main text contains internal workflow or file-management language: " + ", ".join(language_hits[:8]),
            )
        )
    else:
        items.append(AuditItem("internal_workflow_language_warning", "PASS", "No internal workflow language warning detected."))

    tone_hits = [pattern for pattern in TONE_WARNING_PATTERNS if re.search(pattern, main_text, re.I)]
    if tone_hits:
        items.append(
            AuditItem(
                "review_defensive_tone_warning",
                "TONE_WARNING",
                "Main text contains review-defensive phrasing: " + ", ".join(tone_hits[:8]),
            )
        )
    else:
        items.append(AuditItem("review_defensive_tone_warning", "PASS", "No review-defensive tone warning detected."))

    return items


def audit_manuscript(workspace: Path, tex_path: Path, profile: dict[str, Any]) -> dict[str, Any]:
    tex = read_latex_with_inputs(tex_path)
    blocks = extract_blocks(tex)
    items: list[AuditItem] = []
    if profile.get("profile_status") != "PASS":
        items.append(AuditItem("workflow_profile", "UNCHECKED", "workflow_profile.json is missing or invalid; profile-specific checks are disabled."))
    else:
        items.append(AuditItem("workflow_profile", "PASS", f"Profile loaded from {profile.get('profile_path', 'workflow_profile.json')}." ))

    contract_issues = profile_contract_issues(profile)
    if contract_issues:
        items.append(AuditItem("workflow_profile_contract", "FAIL", "; ".join(contract_issues)))
    else:
        items.append(AuditItem("workflow_profile_contract", "PASS", "Workflow profile satisfies the windenergy-orchestrator contract and does not record fallback execution."))

    word_count = count_words(tex)
    main_body, missing_main_body_sections = extract_main_body(tex)
    main_body_word_count = count_words(main_body)
    min_main_body_words = profile_threshold(profile, "main_body_min_words")
    target_main_body_words = profile_threshold(profile, "main_body_target_words") or min_main_body_words
    if min_main_body_words is not None and main_body_word_count < int(min_main_body_words):
        detail = (
            f"{main_body_word_count} main-body words found from Introduction through Conclusion; "
            f"active profile target is {min_main_body_words} to {target_main_body_words} main-body words, "
            "excluding abstract, declarations, captions, tables, figures, references, and appendices."
        )
        if missing_main_body_sections:
            detail += " Missing section marker(s): " + ", ".join(missing_main_body_sections) + "."
        items.append(
            AuditItem(
                "main_body_word_count",
                "FAIL",
                detail,
            )
        )
    elif min_main_body_words is None:
        items.append(
            AuditItem(
                "main_body_word_count",
                "UNCHECKED",
                f"{main_body_word_count} main-body words found; no active profile word-count target.",
            )
        )
    else:
        items.append(
            AuditItem(
                "main_body_word_count",
                "PASS",
                f"{main_body_word_count} main-body words found from Introduction through Conclusion.",
            )
        )

    figure_count = count_latex_environment(tex, "figure")
    table_count = count_latex_environment(tex, "table")
    display_count = figure_count + table_count
    min_figures, min_display_items, display_range = profile_figure_thresholds(profile)
    if min_figures is not None and figure_count < min_figures:
        items.append(
            AuditItem(
                "figure_count",
                "UNCHECKED",
                f"{figure_count} figures found; active profile expects at least {min_figures} figures or a written justification.",
            )
        )
    elif min_figures is None:
        items.append(AuditItem("figure_count", "UNCHECKED", f"{figure_count} figures found; no active profile figure-count target."))
    else:
        items.append(AuditItem("figure_count", "PASS", f"{figure_count} figures found."))

    if min_display_items is not None and display_count < min_display_items:
        items.append(
            AuditItem(
                "display_item_coverage",
                "UNCHECKED",
                f"{display_count} display items found; expected range is {display_range}.",
            )
        )
    elif min_display_items is None:
        items.append(AuditItem("display_item_coverage", "UNCHECKED", f"{display_count} display items found; no active profile display-item target."))
    else:
        items.append(AuditItem("display_item_coverage", "PASS", f"{display_count} display items found."))

    reference_count, reference_source = count_bib_entries(workspace)
    reference_min = profile_threshold(profile, "reference_min")
    if reference_min is not None and reference_count < int(reference_min):
        source = reference_source or "no refs.bib found"
        items.append(
            AuditItem(
                "reference_pool_size",
                "UNCHECKED",
                f"{reference_count} BibTeX entries found in {source}; active profile expects at least {reference_min} verified references or a written justification.",
            )
        )
    elif reference_min is None:
        items.append(AuditItem("reference_pool_size", "UNCHECKED", f"{reference_count} BibTeX entries found; no active profile reference-scale target."))
    else:
        items.append(AuditItem("reference_pool_size", "PASS", f"{reference_count} BibTeX entries found in {reference_source}."))

    items.extend(declaration_integrity_items(tex, profile))

    ignored_titles = {
        "author contribution",
        "author contributions",
        "credit author statement",
        "data availability",
        "declaration of competing interest",
        "declaration of competing interests",
        "acknowledgements",
    }
    short_blocks = []
    for block in blocks:
        title = block["title"]
        if title.lower() in ignored_titles:
            continue
        body_without_tables = strip_environment(str(block["body"]), ["table", "table*", "figure", "figure*", "tabular"])
        words = count_words(body_without_tables)
        if block["level"] in {"subsection", "subsubsection"} and words < 40:
            short_blocks.append({"title": title, "words_without_tables_figures": words})
    if short_blocks:
        detail = "; ".join(f"{item['title']} has {item['words_without_tables_figures']} words" for item in short_blocks[:8])
        items.append(AuditItem("empty_or_table_only_sections", "FAIL", detail))
    else:
        items.append(AuditItem("empty_or_table_only_sections", "PASS", "No empty or table-only subsection detected."))

    operational = find_block(blocks, "Operational Selection Guidance")
    if operational:
        op_words = count_words(strip_environment(operational, ["table", "table*", "tabular", "figure", "figure*"]))
        if op_words < 80:
            items.append(AuditItem("operational_guidance_text", "FAIL", f"Operational Selection Guidance has only {op_words} prose words outside tables."))
        else:
            items.append(AuditItem("operational_guidance_text", "PASS", f"Operational guidance has {op_words} prose words."))

    setup = find_block(blocks, "Experimental Setup")
    missing_setup = [name for name, patterns in profile_setup_requirements(profile) if not has_any(setup, patterns)]
    if missing_setup:
        items.append(AuditItem("experimental_setup_fields", "FAIL", "Missing: " + ", ".join(missing_setup)))
    else:
        items.append(AuditItem("experimental_setup_fields", "PASS", "Required setup fields are present."))

    methodology = find_block(blocks, "Methodology")
    missing_method = [name for name, patterns in profile_method_requirements(profile) if not has_any(methodology, patterns)]
    if missing_method:
        items.append(AuditItem("methodology_fields", "FAIL", "Missing: " + ", ".join(missing_method)))
    else:
        items.append(AuditItem("methodology_fields", "PASS", "Required methodology fields are present."))

    items.extend(related_work_synthesis_items(blocks))

    future_text = " ".join(
        str(block["body"])
        for block in blocks
        if block["title"].lower() in {"discussion", "conclusion", "evidence boundaries"}
    )
    future_matches = [pattern for pattern in CORE_EVIDENCE_GAPS if re.search(r"future work.*" + pattern, future_text, re.I | re.S)]
    if future_matches:
        items.append(AuditItem("future_work_core_evidence_gap", "FAIL", "Future work contains current-evidence gaps: " + ", ".join(future_matches)))
    else:
        items.append(AuditItem("future_work_core_evidence_gap", "PASS", "No current-evidence gap is moved to future work."))

    title = extract_title(tex)
    evidence_boundary = find_block(blocks, "Evidence Boundaries")
    title_is_strong = has_any(title, TITLE_STRONG_PATTERNS)
    boundary_is_weak = has_any(evidence_boundary, EVIDENCE_BOUNDARY_WEAKNESS_PATTERNS)
    evidence_requirements = profile_evidence_requirements(profile)
    title_missing_controls = [name for name, patterns in evidence_requirements if not has_any(tex, patterns)]
    if title_is_strong and (boundary_is_weak or title_missing_controls):
        detail = "Strong mechanism title exceeds visible evidence boundary."
        if title_missing_controls:
            detail += " Missing main-text controls: " + ", ".join(title_missing_controls) + "."
        items.append(AuditItem("title_strength_evidence_boundary", "FAIL", detail))
    else:
        items.append(AuditItem("title_strength_evidence_boundary", "PASS", "Title strength is compatible with visible evidence boundaries."))

    results_and_discussion = " ".join(
        str(block["body"])
        for block in blocks
        if block["title"].lower() in {"results", "discussion", "operational selection guidance", "conclusion"}
    )
    gives_advice = has_any(results_and_discussion, ADVICE_PATTERNS)
    has_granular_reporting = has_any(results_and_discussion, GRANULARITY_PATTERNS)
    if gives_advice and not has_granular_reporting:
        items.append(
            AuditItem(
                "result_granularity",
                "UNCHECKED",
                "Operational or selection advice is present but profile-compatible granular evidence is not visible.",
            )
        )
    else:
        items.append(AuditItem("result_granularity", "PASS", "Result granularity is compatible with the advice level."))

    main_text = main_text_without_reproducibility_or_appendix(tex)
    artifact_hits = [pattern for pattern in INTERNAL_ARTIFACT_PATTERNS if re.search(pattern, main_text, re.I)]
    if artifact_hits:
        items.append(AuditItem("internal_artifact_language", "FAIL", "Main text contains internal workflow artifact language: " + ", ".join(artifact_hits)))
    else:
        items.append(AuditItem("internal_artifact_language", "PASS", "No internal workflow artifact language detected in main text."))

    items.extend(narrative_warning_items(tex, blocks))
    items.extend(introduction_spoiler_items(blocks))
    items.extend(language_and_tone_items(tex))

    status = worst_status([item.status for item in items])
    return {
        "status": status,
        "word_count": word_count,
        "main_body_word_count": main_body_word_count,
        "items": [item.__dict__ for item in items],
    }


def audit_profile_evidence(workspace: Path, tex_path: Path, profile: dict[str, Any]) -> dict[str, Any]:
    tex = read_latex_with_inputs(tex_path)
    diagnostics = read_text(workspace / "diagnostics" / "mechanism_diagnostics.md")
    combined = tex + "\n" + diagnostics
    items: list[AuditItem] = []
    evidence_requirements = profile_evidence_requirements(profile)
    if not evidence_requirements:
        items.append(AuditItem("profile_evidence_controls", "PASS", "No topic-specific evidence-control checklist is active."))
        return {"status": "PASS", "items": [item.__dict__ for item in items]}

    strong_patterns = [
        r"primarily\s+(associated with|from|driven by)",
        r"mainly\s+(associated with|from|driven by)",
        r"proves",
        r"demonstrates the mechanism",
        r"mechanism is",
    ]
    strong_claim = has_any(tex, strong_patterns)
    missing = [name for name, patterns in evidence_requirements if not has_any(combined, patterns)]
    missing_in_manuscript = [name for name, patterns in evidence_requirements if not has_any(tex, patterns)]
    if strong_claim and missing:
        items.append(
            AuditItem(
                "profile_claim_support",
                "FAIL",
                "Strong evidence wording needs active profile controls: " + ", ".join(missing),
            )
        )
    elif strong_claim and missing_in_manuscript:
        items.append(
            AuditItem(
                "profile_claim_support",
                "FAIL",
                "Profile controls exist only outside the manuscript or are not visible in main text: " + ", ".join(missing_in_manuscript),
            )
        )
    elif missing:
        items.append(
            AuditItem(
                "profile_claim_support",
                "UNCHECKED",
                "Only cautious wording is allowed until these active profile controls exist: " + ", ".join(missing),
            )
        )
    else:
        items.append(AuditItem("profile_claim_support", "PASS", "Active profile evidence controls are present."))

    status = worst_status([item.status for item in items])
    return {"status": status, "items": [item.__dict__ for item in items]}


def flatten_values(value: Any) -> list[dict[str, Any]]:
    if isinstance(value, dict):
        if "plotted_value" in value or "expected_value" in value or "table_value" in value:
            return [value]
        values: list[dict[str, Any]] = []
        for child in value.values():
            values.extend(flatten_values(child))
        return values
    if isinstance(value, list):
        values = []
        for child in value:
            values.extend(flatten_values(child))
        return values
    return []


def metadata_bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "y", "1", "pass"}:
            return True
        if lowered in {"false", "no", "n", "0", "fail"}:
            return False
    return None


def is_colorblind_safe(entry: dict[str, Any], style: dict[str, Any]) -> bool | None:
    for value in [entry.get("colorblind_safe"), style.get("colorblind_safe")]:
        parsed = metadata_bool(value)
        if parsed is not None:
            return parsed
    palette = str(style.get("palette_id", entry.get("palette_id", ""))).lower()
    if palette:
        return any(token in palette for token in COLORBLIND_SAFE_PALETTE_TOKENS)
    return None


def figure_visual_contract_items(entries: list[Any]) -> list[AuditItem]:
    failures: list[str] = []
    unchecked: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        figure_name = str(entry.get("figure", "unknown"))
        style = entry.get("style", {})
        if not isinstance(style, dict):
            style = {}

        has_dual_axis = bool(entry.get("dual_axis") or entry.get("secondary_y_axis") or entry.get("uses_secondary_axis"))
        if has_dual_axis and not (entry.get("dual_axis_justification") or entry.get("same_unit_dual_axis") is True):
            failures.append(f"{figure_name}: dual-axis design lacks justification or same-unit metadata")

        chart_type = str(entry.get("chart_type", entry.get("type", ""))).lower()
        visual_encoding = str(entry.get("visual_encoding", "")).lower()
        colorblind_state = is_colorblind_safe(entry, style)
        if colorblind_state is False:
            failures.append(f"{figure_name}: metadata marks palette as not colorblind-safe")
        elif colorblind_state is None and any(token in chart_type + " " + visual_encoding for token in ["heatmap", "diverging", "red-blue", "red blue"]):
            unchecked.append(f"{figure_name}: colorblind-safe palette metadata is missing")

        uncertainty_required = metadata_bool(entry.get("uncertainty_required")) is True
        uncertainty_visible = bool(entry.get("uncertainty_shown") or entry.get("confidence_interval_shown"))
        if uncertainty_required and not uncertainty_visible:
            value_uncertainty = any(bool(value.get("uncertainty_shown") or value.get("confidence_interval_shown")) for value in flatten_values(entry))
            if not value_uncertainty:
                unchecked.append(f"{figure_name}: uncertainty is required but not marked visible")

        unexplained = entry.get("unexplained_labels") or entry.get("undefined_labels") or []
        if isinstance(unexplained, str):
            unexplained = [unexplained]
        if unexplained:
            unchecked.append(f"{figure_name}: unexplained labels " + ", ".join(str(item) for item in unexplained[:6]))

        reference_lines = entry.get("reference_lines", [])
        if isinstance(reference_lines, list):
            missing_reference_source = []
            for item in reference_lines:
                if isinstance(item, dict) and item.get("source") and (item.get("meaning") or item.get("definition")):
                    continue
                missing_reference_source.append(str(item.get("label", "reference line")) if isinstance(item, dict) else str(item))
            if missing_reference_source:
                unchecked.append(f"{figure_name}: reference line source or meaning missing")

        if metadata_bool(entry.get("selection_basis_required")) is True and not entry.get("selection_basis"):
            unchecked.append(f"{figure_name}: displayed subset lacks selection-basis metadata")

        low_support_visual_issue = False
        for value in flatten_values(entry):
            try:
                sample_share = float(value.get("sample_share"))
            except (TypeError, ValueError):
                continue
            if sample_share < 0.01 and not (value.get("visual_warning") or entry.get("visual_warning")):
                low_support_visual_issue = True
        if low_support_visual_issue:
            unchecked.append(f"{figure_name}: low-support subgroup lacks visual warning metadata")

    if failures:
        return [AuditItem("figure_visual_contract", "FAIL", "; ".join(failures[:8]))]
    if unchecked:
        return [AuditItem("figure_visual_contract", "UNCHECKED", "; ".join(unchecked[:8]))]
    return [AuditItem("figure_visual_contract", "PASS", "Figure visual metadata has no configured dual-axis, palette, uncertainty, label, reference-line, subset-selection, or low-support warnings.")]


def audit_figure_consistency(workspace: Path, tex_path: Path, profile: dict[str, Any]) -> dict[str, Any]:
    tex = read_latex_with_inputs(tex_path)
    include_paths = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^{}]+)\}", tex)
    quantitative = [path for path in include_paths if "grid" not in path.lower() and "workflow" not in path.lower()]
    workflow = [path for path in include_paths if "grid" in path.lower() or "workflow" in path.lower()]
    map_path = workspace / "figures" / "figure_data_map.json"
    items: list[AuditItem] = []

    if (quantitative or workflow) and not map_path.exists():
        items.append(AuditItem("figure_data_map", "UNCHECKED", "`figures/figure_data_map.json` is missing for manuscript figures."))
        return {"status": "UNCHECKED", "items": [item.__dict__ for item in items], "figures": include_paths}

    if not map_path.exists():
        items.append(AuditItem("figure_data_map", "PASS", "No quantitative manuscript figures detected."))
        return {"status": "PASS", "items": [item.__dict__ for item in items], "figures": include_paths}

    try:
        data = json.loads(read_text(map_path))
    except json.JSONDecodeError as exc:
        items.append(AuditItem("figure_data_map", "FAIL", f"Invalid JSON: {exc}"))
        return {"status": "FAIL", "items": [item.__dict__ for item in items], "figures": include_paths}

    if isinstance(data, dict):
        entries = data.get("figures", [])
    elif isinstance(data, list):
        entries = data
    else:
        entries = []
    if not isinstance(entries, list):
        entries = []

    mapped_names = {str(entry.get("figure", "")) for entry in entries if isinstance(entry, dict)}
    missing_maps = [path for path in include_paths if Path(path).name not in mapped_names and path not in mapped_names]
    if missing_maps:
        items.append(AuditItem("mapped_figures", "UNCHECKED", "Missing map entries: " + ", ".join(missing_maps)))
    else:
        items.append(AuditItem("mapped_figures", "PASS", "All included figures have map entries."))

    items.extend(figure_visual_contract_items(entries))

    value_failures = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        tolerance = float(entry.get("tolerance", data.get("tolerance", 0.02) if isinstance(data, dict) else 0.02))
        for value in flatten_values(entry.get("values", entry)):
            if "plotted_value" not in value:
                continue
            expected = value.get("expected_value", value.get("table_value"))
            if expected is None:
                value_failures.append(f"{entry.get('figure', 'unknown')}: missing expected value for {value.get('label', 'value')}")
                continue
            try:
                plotted = float(value["plotted_value"])
                expected_float = float(expected)
            except (TypeError, ValueError):
                value_failures.append(f"{entry.get('figure', 'unknown')}: nonnumeric value for {value.get('label', 'value')}")
                continue
            if abs(plotted - expected_float) > tolerance:
                value_failures.append(
                    f"{entry.get('figure', 'unknown')} {value.get('label', 'value')} plotted={plotted} expected={expected_float}"
                )
    if value_failures:
        items.append(AuditItem("plotted_value_consistency", "FAIL", "; ".join(value_failures[:8])))
    else:
        items.append(AuditItem("plotted_value_consistency", "PASS", "Mapped plotted values match expected values."))

    figure_count = count_latex_environment(tex, "figure")
    table_count = count_latex_environment(tex, "table")
    display_count = figure_count + table_count
    min_figures, min_display_items, display_range = profile_figure_thresholds(profile)
    if min_figures is not None and figure_count < min_figures:
        items.append(
            AuditItem(
                "display_item_figure_count",
                "UNCHECKED",
                f"{figure_count} figures found; active profile expects at least {min_figures}.",
            )
        )
    elif min_figures is None:
        items.append(AuditItem("display_item_figure_count", "UNCHECKED", f"{figure_count} figures found; no active profile figure-count target."))
    else:
        items.append(AuditItem("display_item_figure_count", "PASS", f"{figure_count} figures found."))
    if min_display_items is not None and display_count < min_display_items:
        items.append(
            AuditItem(
                "display_item_total_count",
                "UNCHECKED",
                f"{display_count} display items found; expected range is {display_range}.",
            )
        )
    elif min_display_items is None:
        items.append(AuditItem("display_item_total_count", "UNCHECKED", f"{display_count} display items found; no active profile display-item target."))
    else:
        items.append(AuditItem("display_item_total_count", "PASS", f"{display_count} display items found."))

    style_failures = []
    style_unchecked = []
    line_widths = []
    palette_ids = set()
    legend_policies = set()
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        figure_name = str(entry.get("figure", "unknown"))
        style = entry.get("style") or (data.get("style") if isinstance(data, dict) else None)
        if not isinstance(style, dict):
            style_unchecked.append(figure_name)
            continue
        font = str(style.get("font_family", "")).lower()
        if font and not any(token in font for token in ["times", "serif", "stix", "libertinus", "cambria"]):
            style_failures.append(f"{figure_name}: nonserif font {style.get('font_family')}")
        min_font = style.get("min_font_pt")
        try:
            if min_font is None or float(min_font) < 8:
                style_failures.append(f"{figure_name}: min font below 8 pt")
        except (TypeError, ValueError):
            style_failures.append(f"{figure_name}: invalid min_font_pt")
        if "line_width_pt" in style:
            try:
                line_widths.append(float(style["line_width_pt"]))
            except (TypeError, ValueError):
                style_failures.append(f"{figure_name}: invalid line_width_pt")
        if style.get("palette_id"):
            palette_ids.add(str(style["palette_id"]))
        if style.get("legend_policy"):
            legend_policies.add(str(style["legend_policy"]))
    if style_unchecked:
        items.append(AuditItem("figure_style_metadata", "UNCHECKED", "Missing style metadata for: " + ", ".join(style_unchecked[:8])))
    elif style_failures:
        items.append(AuditItem("figure_style_metadata", "FAIL", "; ".join(style_failures[:8])))
    else:
        items.append(AuditItem("figure_style_metadata", "PASS", "Figure style metadata satisfies font and minimum-size rules."))
    if len(line_widths) > 1 and (max(line_widths) - min(line_widths)) > 0.5:
        items.append(AuditItem("figure_style_consistency", "FAIL", "Line widths vary by more than 0.5 pt across mapped figures."))
    elif len(palette_ids) > 2 or len(legend_policies) > 3:
        items.append(AuditItem("figure_style_consistency", "FAIL", "Palette or legend policy varies too much across the figure set."))
    else:
        items.append(AuditItem("figure_style_consistency", "PASS", "Line width, palette, and legend metadata are consistent enough for audit."))

    roles = {str(entry.get("role", entry.get("portfolio_role", ""))).lower() for entry in entries if isinstance(entry, dict)}
    profile_roles = profile_threshold(profile, "figure_portfolio_roles") or FIGURE_PORTFOLIO_ROLES
    if not isinstance(profile_roles, list):
        profile_roles = FIGURE_PORTFOLIO_ROLES
    missing_roles = [str(role).lower() for role in profile_roles if str(role).lower() not in roles]
    if missing_roles:
        items.append(AuditItem("figure_portfolio_roles", "UNCHECKED", "Missing figure portfolio roles: " + ", ".join(missing_roles)))
    else:
        items.append(AuditItem("figure_portfolio_roles", "PASS", "Figure portfolio covers the expected evidence roles."))

    axis_issues = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        axis = entry.get("x_axis", {})
        if not isinstance(axis, dict):
            continue
        quantity = str(axis.get("quantity", "")).lower()
        label = str(axis.get("label", "")).lower()
        needs_dual_label = bool(axis.get("requires_dual_label")) or bool(axis.get("profile_axis_check"))
        has_dual_label = bool(axis.get("target_label") or axis.get("dual_label") or axis.get("secondary_label"))
        if needs_dual_label and not has_dual_label:
            axis_issues.append(str(entry.get("figure", "unknown")))
    if axis_issues:
        items.append(AuditItem("axis_interpretation", "UNCHECKED", "Profile-specific axis metadata is incomplete: " + ", ".join(axis_issues[:8])))
    else:
        items.append(AuditItem("axis_interpretation", "PASS", "Axis metadata does not create an avoidable alpha-to-coverage conversion burden."))

    low_support_issues = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        for value in flatten_values(entry.get("values", entry)):
            sample_share = value.get("sample_share")
            sample_count = value.get("sample_count")
            try:
                low_share = sample_share is not None and float(sample_share) < 0.01
            except (TypeError, ValueError):
                low_share = False
            try:
                low_count = sample_count is not None and int(sample_count) < 30
            except (TypeError, ValueError):
                low_count = False
            if low_share or low_count:
                stable = bool(
                    value.get("uncertainty_shown")
                    or value.get("sensitivity_reported")
                    or value.get("visual_warning")
                    or entry.get("sensitivity_reported")
                    or entry.get("visual_warning")
                )
                if not stable:
                    low_support_issues.append(f"{entry.get('figure', 'unknown')}: {value.get('label', 'low-support condition')}")
    if low_support_issues:
        items.append(AuditItem("low_support_condition", "UNCHECKED", "Low-support conditions need uncertainty or sensitivity evidence: " + "; ".join(low_support_issues[:8])))
    else:
        items.append(AuditItem("low_support_condition", "PASS", "No unsupported low-sample condition detected in figure map."))

    workflow_entries = [entry for entry in entries if isinstance(entry, dict) and str(entry.get("type", "")).lower() == "workflow"]
    if workflow and not workflow_entries:
        items.append(AuditItem("workflow_figure_structure", "UNCHECKED", "Workflow figure needs a workflow map entry."))
    for entry in workflow_entries:
        layers = [str(item).lower() for item in entry.get("layers", [])]
        concepts = [str(item).lower() for item in entry.get("concepts", [])]
        required_layers = profile_threshold(profile, "workflow_layers") or []
        if not isinstance(required_layers, list):
            required_layers = []
        missing_layers = [str(layer).lower() for layer in required_layers if str(layer).lower() not in layers]
        missing_concepts = [concept for concept in WORKFLOW_REQUIRED_CONCEPTS if concept not in concepts]
        contains_code = bool(entry.get("contains_code_filenames"))
        too_dense = int(entry.get("text_items", 0) or 0) > 25
        if missing_layers or missing_concepts or contains_code or too_dense:
            detail = []
            if missing_layers:
                detail.append("missing layers: " + ", ".join(missing_layers))
            if missing_concepts:
                detail.append("missing concepts: " + ", ".join(missing_concepts))
            if contains_code:
                detail.append("contains code filenames")
            if too_dense:
                detail.append("too many text items")
            items.append(AuditItem("workflow_figure_structure", "FAIL", "; ".join(detail)))
        else:
            items.append(AuditItem("workflow_figure_structure", "PASS", "Workflow figure contains required layers and scientific concepts."))

    status = worst_status([item.status for item in items])
    return {"status": status, "items": [item.__dict__ for item in items], "figures": include_paths}


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_markdown(path: Path, title: str, report: dict[str, Any]) -> None:
    lines = [f"# {title}", "", f"Overall status: {report['status']}", ""]
    if "word_count" in report:
        lines.append(f"Total manuscript word count: {report['word_count']}")
        lines.append("")
    if "main_body_word_count" in report:
        lines.append(f"Main body word count: {report['main_body_word_count']}")
        lines.append("")
    lines.extend(["| Check | Status | Detail |", "|---|---|---|"])
    for item in report.get("items", []):
        lines.append(f"| {item['check']} | {item['status']} | {item['detail']} |")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_all_audits(workspace: Path, tex_rel: str = "final/paper.tex", profile_rel: str | None = None) -> dict[str, Any]:
    profile = load_profile(workspace, profile_rel)
    tex_path = workspace / tex_rel
    if not tex_path.exists():
        tex_path = workspace / "drafts" / "paper_polished.tex"
    if not tex_path.exists():
        tex_path = workspace / "drafts" / "paper.tex"

    manuscript = audit_manuscript(workspace, tex_path, profile)
    profile_evidence = audit_profile_evidence(workspace, tex_path, profile)
    figure = audit_figure_consistency(workspace, tex_path, profile)

    write_json(workspace / "audits" / "manuscript_quality_audit.json", manuscript)
    write_markdown(workspace / "audits" / "manuscript_quality_audit.md", "Manuscript Quality Audit", manuscript)
    write_json(workspace / "diagnostics" / "profile_evidence_strength_audit.json", profile_evidence)
    write_markdown(workspace / "diagnostics" / "profile_evidence_strength_audit.md", "Profile Evidence Strength Audit", profile_evidence)
    write_json(workspace / "diagnostics" / "mechanism_evidence_strength_audit.json", profile_evidence)
    write_markdown(workspace / "diagnostics" / "mechanism_evidence_strength_audit.md", "Mechanism Evidence Strength Audit", profile_evidence)
    write_json(workspace / "audits" / "figure_consistency_audit.json", figure)
    write_markdown(workspace / "audits" / "figure_consistency_audit.md", "Figure Consistency Audit", figure)

    maturity_items = [
        AuditItem("manuscript_quality", manuscript["status"], "See `audits/manuscript_quality_audit.md`."),
        AuditItem("profile_evidence_strength", profile_evidence["status"], "See `diagnostics/profile_evidence_strength_audit.md`."),
        AuditItem("figure_consistency", figure["status"], "See `audits/figure_consistency_audit.md`."),
    ]
    maturity = {
        "status": worst_status([item.status for item in maturity_items]),
        "items": [item.__dict__ for item in maturity_items],
    }
    write_markdown(workspace / "audits" / "scientific_maturity_audit.md", "Scientific Maturity Audit", maturity)
    write_json(workspace / "audits" / "scientific_maturity_audit.json", maturity)
    return {
        "manuscript": manuscript,
        "mechanism": profile_evidence,
        "profile_evidence": profile_evidence,
        "figure": figure,
        "scientific_maturity": maturity,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace")
    parser.add_argument("--tex", default="final/paper.tex", help="Manuscript path relative to workspace")
    parser.add_argument("--profile", help="Profile path relative to workspace. Defaults to workflow_profile.json")
    parser.add_argument("--strict", action="store_true", help="Return nonzero unless all audits PASS")
    args = parser.parse_args()

    report = run_all_audits(Path(args.workspace).resolve(), args.tex, args.profile)
    status = report["scientific_maturity"]["status"]
    print(json.dumps({"status": status, **report}, indent=2, ensure_ascii=False))
    if args.strict and status != "PASS":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
