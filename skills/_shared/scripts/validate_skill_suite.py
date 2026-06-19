#!/usr/bin/env python3
"""Validate the renewable skill suite structure."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
JOURNAL_SLUGS = {
    "common-18",
    "renewable-energy",
    "applied-energy",
    "energy",
    "energy-conversion-management",
    "energy-reports",
    "energy-and-ai",
    "segan",
    "seta",
    "ijepes",
    "electric-power-systems-research",
    "computers-electrical-engineering",
    "engineering-applications-ai",
    "expert-systems-applications",
    "knowledge-based-systems",
    "information-sciences",
    "neurocomputing",
    "pattern-recognition",
    "applied-soft-computing",
}
FORBIDDEN = {
    "em_dash": "\u2014",
    "en_dash": "\u2013",
    "right_arrow": "\u2192",
    "replacement_char": "\ufffd",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def validate_skill_frontmatter(errors: list[str]) -> None:
    for skill in sorted(ROOT.glob("windenergy-*/SKILL.md")):
        text = read_text(skill)
        match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if not match:
            errors.append(f"{skill}: missing YAML frontmatter")
            continue
        data = yaml.safe_load(match.group(1)) or {}
        if set(data) != {"name", "description"}:
            errors.append(f"{skill}: frontmatter must contain only name and description")
        if data.get("name") != skill.parent.name:
            errors.append(f"{skill}: name does not match folder")
        if not data.get("description"):
            errors.append(f"{skill}: empty description")


def validate_manifest_paths(errors: list[str]) -> None:
    for manifest in sorted(ROOT.glob("windenergy-*/manifest.yaml")):
        data = yaml.safe_load(read_text(manifest)) or {}
        paths: list[str] = []
        paths.extend(data.get("always_load") or [])
        for axis in (data.get("axes") or {}).values():
            paths.extend((axis.get("values") or {}).values())
        for item in (data.get("references") or {}).get("on_demand", []) or []:
            if isinstance(item, dict) and item.get("path"):
                paths.append(item["path"])
        for rel in paths:
            target = (manifest.parent / rel).resolve()
            if not target.exists():
                errors.append(f"{manifest}: missing referenced path {rel}")


def validate_submission_revision_protocol(errors: list[str]) -> None:
    required = [
        ROOT / "windenergy-submission" / "references" / "revision-protocol.md",
        ROOT / "windenergy-submission" / "references" / "manuscript-compression-protocol.md",
        ROOT / "windenergy-submission" / "references" / "final-manuscript-audit.md",
        ROOT / "windenergy-submission" / "scripts" / "apply_submission_revisions.py",
        ROOT / "windenergy-submission" / "scripts" / "scan_docx_blocks.py",
        ROOT / "_shared" / "core" / "output-run-folders.md",
        ROOT / "_shared" / "scripts" / "create_run_folder.py",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"missing submission revision support file {path}")
    skill = read_text(ROOT / "windenergy-submission" / "SKILL.md")
    for phrase in [
        "Applied tracked revisions",
        "Applied tracked manuscript compression",
        "apply_submission_revisions.py",
        "manuscript-compression-protocol.md",
        "revision-protocol.md",
        "final-manuscript-audit.md",
        "../windenergy-polishing/SKILL.md",
        "output-run-folders.md",
    ]:
        if phrase not in skill:
            errors.append(f"windenergy-submission/SKILL.md missing {phrase}")


def validate_agents_metadata(errors: list[str]) -> None:
    for skill in sorted(ROOT.glob("windenergy-*")):
        agent = skill / "agents" / "openai.yaml"
        if not agent.exists():
            errors.append(f"{skill}: missing agents/openai.yaml")
            continue
        data = yaml.safe_load(read_text(agent)) or {}
        interface = data.get("interface") or {}
        for key in ["display_name", "short_description", "default_prompt"]:
            if not interface.get(key):
                errors.append(f"{agent}: missing interface.{key}")

    submission_agent = ROOT / "windenergy-submission" / "agents" / "openai.yaml"
    if submission_agent.exists():
        prompt = ((yaml.safe_load(read_text(submission_agent)) or {}).get("interface") or {}).get("default_prompt", "")
        for phrase in ["$windenergy-submission", "$windenergy-polishing", "tracked revisions"]:
            if phrase not in prompt:
                errors.append(f"{submission_agent}: default prompt missing {phrase}")


def validate_output_run_folder_protocol(errors: list[str]) -> None:
    protocol = ROOT / "_shared" / "core" / "output-run-folders.md"
    if not protocol.exists():
        errors.append("missing shared output-run-folders.md")
        return
    for skill in sorted(ROOT.glob("windenergy-*/SKILL.md")):
        text = read_text(skill)
        if "output-run-folders.md" not in text:
            errors.append(f"{skill}: missing output-run-folders.md reference")


def validate_journal_slugs(errors: list[str]) -> None:
    profile = ROOT / "windenergy-submission" / "references" / "journal-profiles.md"
    text = read_text(profile) if profile.exists() else ""
    for slug in JOURNAL_SLUGS:
        if f"`{slug}`" not in text and f"Slug: `{slug}`" not in text:
            errors.append(f"journal profile missing slug {slug}")
    for manifest in [
        ROOT / "windenergy-writing" / "manifest.yaml",
        ROOT / "windenergy-polishing" / "manifest.yaml",
    ]:
        data = yaml.safe_load(read_text(manifest)) or {}
        values = ((data.get("axes") or {}).get("journal") or {}).get("values") or {}
        missing = JOURNAL_SLUGS - set(values)
        if missing:
            errors.append(f"{manifest}: journal axis missing {sorted(missing)}")


def validate_forbidden_chars(errors: list[str]) -> None:
    extensions = {".md", ".py", ".yaml", ".yml", ".toml", ".json"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or "__pycache__" in path.parts:
            continue
        if path.suffix.lower() not in extensions:
            continue
        rel = path.relative_to(ROOT)
        if not str(rel).startswith(("windenergy-", "_shared")):
            continue
        text = read_text(path)
        for name, char in FORBIDDEN.items():
            if char in text:
                errors.append(f"{rel}: contains forbidden {name}")
        contrast_pattern = "\u4e0d" + "\u662f" + r".*" + "\u800c" + "\u662f"
        if re.search(contrast_pattern, text):
            errors.append(f"{rel}: contains forbidden Chinese contrast pattern")


def validate_polishing_requirements(errors: list[str]) -> None:
    skill = read_text(ROOT / "windenergy-polishing" / "SKILL.md")
    style = read_text(ROOT / "windenergy-polishing" / "references" / "style-guardrails.md")
    script = read_text(ROOT / "windenergy-polishing" / "scripts" / "polish_docx.py")
    for phrase in [
        "Rewrite avoidable parenthetical sentence structures",
        "preserving the information inside the parentheses",
        "#0000FF",
        "numbered citation marker",
        "--color-crossrefs",
        "Tool Failure Recovery",
        "Do not create ad hoc scripts",
    ]:
        if phrase not in skill:
            errors.append(f"windenergy-polishing/SKILL.md missing {phrase}")
    for phrase in [
        "Rewrite avoidable parenthetical sentence structures",
        "preserving the information inside the parentheses",
        "#0000FF",
        "numbered citations",
    ]:
        if phrase not in style:
            errors.append(f"windenergy-polishing style guardrails missing {phrase}")
    for phrase in [
        "color_crossrefs",
        "CROSSREF_RE",
        "CITATION_RE",
        "\\u2013",
        "BLUE",
        "IGNORABLE_BETWEEN_RUN_TAGS",
        "themeColor",
    ]:
        if phrase not in script:
            errors.append(f"polish_docx.py missing {phrase}")
    for phrase in ["MATH_NS", "_unsafe_paragraph_reasons", "unsupported_content"]:
        if phrase not in script:
            errors.append(f"polish_docx.py missing complex OOXML guard {phrase}")
    for phrase in ["package_risk_summary", "requires_package_preserving_save", "word/document.xml"]:
        if phrase not in script:
            errors.append(f"polish_docx.py missing package-preserving guard {phrase}")
    for phrase in ["MathType", "Preserving formulas and variables"]:
        if phrase not in skill:
            errors.append(f"windenergy-polishing/SKILL.md missing complex OOXML guard {phrase}")
    if "package-preserving save behavior" not in skill:
        errors.append("windenergy-polishing/SKILL.md missing package-preserving save behavior")


def validate_citation_audit_requirements(errors: list[str]) -> None:
    script = read_text(ROOT / "windenergy-citation" / "scripts" / "windenergy_citation.py")
    citation_skill = read_text(ROOT / "windenergy-citation" / "SKILL.md")
    submission_skill = read_text(ROOT / "windenergy-submission" / "SKILL.md")
    checklist = read_text(ROOT / "windenergy-submission" / "references" / "submission-checklist.md")
    final_audit = read_text(ROOT / "windenergy-submission" / "references" / "final-manuscript-audit.md")
    test_file = ROOT / "_shared" / "tests" / "test_word_and_citation_safety.py"

    for phrase in [
        "--audit",
        "--bib",
        "--markdown",
        "strict_ready",
        "FAIL",
        "UNCHECKED",
        "search_openalex",
        "audit_references",
    ]:
        if phrase not in script:
            errors.append(f"windenergy_citation.py missing citation audit phrase {phrase}")
    for name, text in [
        ("windenergy-citation/SKILL.md", citation_skill),
        ("windenergy-submission/SKILL.md", submission_skill),
        ("submission-checklist.md", checklist),
        ("final-manuscript-audit.md", final_audit),
    ]:
        for phrase in ["audit.json", "FAIL", "UNCHECKED"]:
            if phrase not in text:
                errors.append(f"{name} missing strict citation audit phrase {phrase}")
    if not test_file.exists():
        errors.append("missing word and citation safety tests")
    else:
        test_text = read_text(test_file)
        for phrase in ["fake-mathtype.bin", "strict_ready", "UNCHECKED", "word/embeddings"]:
            if phrase not in test_text:
                errors.append(f"test_word_and_citation_safety.py missing {phrase}")


def validate_academic_search_boundaries(errors: list[str]) -> None:
    academic_skill = read_text(ROOT / "windenergy-academic-search" / "SKILL.md")
    citation_skill = read_text(ROOT / "windenergy-citation" / "SKILL.md")
    requirements_path = ROOT / "windenergy-academic-search" / "mcp-server" / "requirements.txt"

    if not requirements_path.exists():
        errors.append("windenergy-academic-search missing mcp-server/requirements.txt")
    else:
        requirements = read_text(requirements_path).lower()
        if not re.search(r"^mcp(?:[<>=~!]=?|$)", requirements, re.M):
            errors.append("windenergy-academic-search mcp-server/requirements.txt missing mcp")

    for phrase in [
        "candidate sources",
        "windenergy-citation",
        "MCP server is not available",
        "Do not imply that MCP-backed sources were queried",
    ]:
        if phrase not in academic_skill:
            errors.append(f"windenergy-academic-search/SKILL.md missing boundary phrase {phrase}")

    for phrase in [
        "final reference-list audits",
        "in-text citation to",
        "windenergy-academic-search",
    ]:
        if phrase not in citation_skill:
            errors.append(f"windenergy-citation/SKILL.md missing boundary phrase {phrase}")


def validate_response_council_requirements(errors: list[str]) -> None:
    response_skill = read_text(ROOT / "windenergy-response" / "SKILL.md")
    intake = read_text(ROOT / "windenergy-response" / "references" / "intake-and-routing.md")
    council_path = ROOT / "windenergy-response" / "references" / "revision-council.md"
    memory_path = ROOT / "windenergy-response" / "reviewer_patterns" / "_cumulative.md"
    agent_path = ROOT / "windenergy-response" / "agents" / "openai.yaml"
    example_path = ROOT / "windenergy-response" / "examples" / "council-review.md"
    archived_council_path = ROOT / "paper-revision-council" / "SKILL.md"
    active_council_path = Path.home() / ".claude" / "skills" / "paper-revision-council"

    if not council_path.exists():
        errors.append("windenergy-response missing references/revision-council.md")
        return
    if not memory_path.exists():
        errors.append("windenergy-response missing reviewer_patterns/_cumulative.md")
        return
    if not example_path.exists():
        errors.append("windenergy-response missing examples/council-review.md")
        return
    if active_council_path.exists():
        errors.append(
            f"{active_council_path}: archived paper-revision-council must not be installed as an active skill; "
            "use windenergy-response council-review"
        )

    council = read_text(council_path)
    memory = read_text(memory_path)
    agent = read_text(agent_path)
    example = read_text(example_path)
    for name, text in [
        ("windenergy-response/SKILL.md", response_skill),
        ("intake-and-routing.md", intake),
        ("revision-council.md", council),
        ("agents/openai.yaml", agent),
        ("examples/council-review.md", example),
    ]:
        if "council-review" not in text:
            errors.append(f"{name} missing council-review")

    for phrase in [
        "Energy Domain Expert",
        "AI and Computer Science Expert",
        "Math and Physics Expert",
        "Consensus",
        "revision_council_plan.md",
        "response_draft.md",
        "reviewer_pattern_update.md",
        "windenergy-polishing",
        "Do not run `paper_revision_helpers.py`",
        "Do not run `paper_revision_helpers.py` or `apply_minimal_revisions.py`",
    ]:
        if phrase not in council and phrase not in response_skill:
            errors.append(f"revision council workflow missing {phrase}")

    if "paper_revision_helpers.py" in response_skill and "Do not run legacy" not in response_skill:
        errors.append("windenergy-response/SKILL.md references legacy helper without prohibition")
    if "apply_minimal_revisions.py" in response_skill and "Do not run legacy" not in response_skill:
        errors.append("windenergy-response/SKILL.md references legacy apply script without prohibition")
    if "Cumulative Reviewer Pattern Memory" not in memory:
        errors.append("reviewer_patterns/_cumulative.md missing memory heading")
    for phrase in [
        "comment inventory",
        "three expert summaries",
        "consensus table",
        "priority plan",
        "author decision items",
        "English response draft",
    ]:
        if phrase not in example:
            errors.append(f"examples/council-review.md missing {phrase}")
    if archived_council_path.exists():
        archived_council = read_text(archived_council_path)
        for phrase in ["ARCHIVE ONLY", "windenergy-response", "council-review"]:
            if phrase not in archived_council:
                errors.append(f"paper-revision-council/SKILL.md missing archive phrase {phrase}")


def validate_orchestrator_requirements(errors: list[str]) -> None:
    base = ROOT / "windenergy-orchestrator"
    required = [
        base / "SKILL.md",
        base / "agents" / "openai.yaml",
        base / "references" / "workflow.md",
        base / "references" / "workspace-contract.md",
        base / "references" / "gates.md",
        base / "references" / "benchmark-mechanism-paper.md",
        base / "scripts" / "init_workspace.py",
        base / "scripts" / "validate_workspace.py",
        base / "scripts" / "validate_stage_outputs.py",
        base / "scripts" / "collect_outputs.py",
        base / "scripts" / "audit_manuscript_quality.py",
        base / "scripts" / "update_workspace_state.py",
        base / "scripts" / "audit_writing_quality.py",
    ]
    for path in required:
        if not path.exists():
            errors.append(f"windenergy-orchestrator missing {path.relative_to(base)}")
            return

    skill = read_text(base / "SKILL.md")
    workflow = read_text(base / "references" / "workflow.md")
    contract = read_text(base / "references" / "workspace-contract.md")
    gates = read_text(base / "references" / "gates.md")
    benchmark = read_text(base / "references" / "benchmark-mechanism-paper.md")
    scripts = "\n".join(read_text(path) for path in required if path.suffix == ".py")

    for phrase in [
        "full-paper",
        "benchmark-run",
        "output-run-folders.md",
        "project_state.json",
        "decision_log.md",
        "task_queue.md",
        "update_workspace_state.py",
        "audit_writing_quality.py",
    ]:
        if phrase not in skill:
            errors.append(f"windenergy-orchestrator/SKILL.md missing {phrase}")

    for phrase in [
        "windenergy-writing",
        "windenergy-academic-search",
        "windenergy-citation",
        "windenergy-figure",
        "windenergy-submission",
        "windenergy-polishing",
    ]:
        if phrase not in workflow and phrase not in skill:
            errors.append(f"windenergy-orchestrator workflow missing {phrase}")

    for phrase in [
        "citation_audit.json",
        "polishing_audit.md",
        "source_code_evidence_register.md",
        "paper_polished.tex",
        "submission_audit.md",
        "manuscript_quality_audit.json",
        "figure_consistency_audit.json",
        "mechanism_evidence_strength_audit.json",
        "Citation audit is mandatory",
        "Polishing audit is mandatory",
        "Source evidence register is mandatory",
        "Submission audit is mandatory",
        "PASS",
        "FAIL",
        "UNCHECKED",
        "workbench state",
        "project_state.json",
        "artifact_index.json",
        "automation_recipes.md",
        "writing_quality_audit",
    ]:
        if phrase not in gates and phrase not in contract:
            errors.append(f"windenergy-orchestrator gates missing {phrase}")

    for phrase in [
        "mechanism_diagnostics.md",
        "claim_evidence_map.md",
        "3528",
        "Applied Energy",
        "CPTC",
        "AcMCP",
    ]:
        if phrase not in benchmark:
            errors.append(f"benchmark-mechanism-paper.md missing {phrase}")

    if "paper-orchestra" not in workflow or "runtime" not in workflow or "substitute" not in workflow:
        errors.append("windenergy-orchestrator must state paper-orchestra is not a runtime quality gate")

    for phrase in ["orchestrator_status.json", "final_manifest.json", "sha256", "UTF-8"]:
        if phrase not in scripts and phrase not in contract:
            errors.append(f"windenergy-orchestrator scripts missing {phrase}")
    for phrase in [
        "project_state.json",
        "decision_log.md",
        "task_queue.md",
        "artifact_index.json",
        "automation_recipes.md",
        "--init-missing",
        "workbench_state",
        "queued_tasks",
        "next_action",
        "writing_quality",
        "writing_revision_plan.md",
        "method_citation_binding",
        "undefined_process_terms",
        "declaration_integrity",
        "figure_visual_contract",
    ]:
        if phrase not in scripts and phrase not in contract and phrase not in workflow:
            errors.append(f"windenergy-orchestrator workbench protocol missing {phrase}")
    for phrase in [
        "source_evidence",
        "polishing",
        "workflow_profile.json",
        "profile_evidence_strength",
        "paper_polished.tex",
        "polishing_audit.md",
        "manuscript_quality",
        "figure_consistency",
        "mechanism_evidence_strength",
        "main_body_word_count",
        "figure_data_map.json",
        "profile_threshold",
        "profile_figure_thresholds",
        "narrative_warning",
        "reference_pool_size",
        "figure_portfolio_roles",
        "figure_visual_contract",
        "internal_artifact_language",
        "declaration_integrity",
    ]:
        if phrase not in scripts:
            errors.append(f"windenergy-orchestrator scripts missing stage phrase {phrase}")


def validate_quality_principles(errors: list[str]) -> None:
    shared_path = ROOT / "_shared" / "core" / "quality-principles.md"
    narrative_path = ROOT / "_shared" / "core" / "narrative-principles.md"
    section_role_path = ROOT / "_shared" / "core" / "section-role-matrix.md"
    fragment_contract_path = ROOT / "_shared" / "core" / "fragment-contract.md"
    if not shared_path.exists():
        errors.append("missing shared quality-principles.md")
        return
    for path in [narrative_path, section_role_path, fragment_contract_path, ROOT / "_shared" / "migration_map.md"]:
        if not path.exists():
            errors.append(f"missing shared layered refactor file {path.relative_to(ROOT)}")
    shared = read_text(shared_path)
    for phrase in [
        "Claim Strength Control",
        "Evidence Chain",
        "Figure Professionalism",
        "Manuscript Completeness",
        "Journal Fit",
        "Core Boundary",
        "Conflict Priority",
        "Warning Semantics",
    ]:
        if phrase not in shared:
            errors.append(f"quality-principles.md missing {phrase}")
    hard_core_terms = [
        "Kupiec",
        "Christoffersen",
        "conformal calibration",
        "interval score",
        "Applied Energy full-length",
        "40 verified references",
        "3528",
        "QRLSTM",
        "GBR",
    ]
    core_text = "\n".join(
        read_text(path)
        for path in [
            shared_path,
            narrative_path,
            section_role_path,
            fragment_contract_path,
            ROOT / "_shared" / "core" / "reader-workflow.md",
            ROOT / "_shared" / "core" / "paper-type-taxonomy.md",
        ]
        if path.exists()
    )
    for term in hard_core_terms:
        if term.lower() in core_text.lower():
            errors.append(f"core layer contains hard-deny specialized term {term}")
    section_role = read_text(section_role_path) if section_role_path.exists() else ""
    for phrase in [
        "Related Work",
        "literature map and gap validation",
        "Common Role Collisions",
    ]:
        if phrase not in section_role:
            errors.append(f"section-role-matrix.md missing {phrase}")
    narrative = read_text(narrative_path) if narrative_path.exists() else ""
    narrative_lower = narrative.lower()
    for phrase in [
        "standard narrative pass",
        "high-impact narrative pass",
        "section-specific narrative control",
        "Introduction Spoiler Control",
        "Related Work",
        "SECTION_WARNING",
        "take-home message",
        "cannot increase claim strength",
        "NARRATIVE_WARNING",
    ]:
        if phrase.lower() not in narrative_lower:
            errors.append(f"narrative-principles.md missing {phrase}")
    fragment_contract = read_text(fragment_contract_path) if fragment_contract_path.exists() else ""
    for phrase in [
        "Activation Condition",
        "Allowed Content",
        "Anti Examples",
        "topic_confidence < 0.70",
        "Topic fragments must not contain single-manuscript",
    ]:
        if phrase not in fragment_contract:
            errors.append(f"fragment-contract.md missing {phrase}")

    required_fragments = [
        "_shared/fragments/paper_type/mechanism-paper.md",
        "_shared/fragments/paper_type/method-paper.md",
        "_shared/fragments/paper_type/benchmark-paper.md",
        "_shared/fragments/paper_type/deployment-paper.md",
        "_shared/fragments/paper_type/case-study.md",
        "_shared/fragments/paper_type/review.md",
        "_shared/fragments/paper_type/resource-assessment.md",
        "_shared/fragments/paper_type/control-paper.md",
        "_shared/fragments/paper_type/optimization-paper.md",
        "_shared/fragments/topic/wind-power-forecasting.md",
        "_shared/fragments/topic/probabilistic-forecasting.md",
        "_shared/fragments/topic/conformal-calibration.md",
        "_shared/fragments/topic/wake-modeling.md",
        "_shared/fragments/topic/offshore-wind-siting.md",
        "_shared/fragments/topic/storage-optimization.md",
        "_shared/fragments/topic/power-market.md",
        "_shared/fragments/topic/cfd-surrogate.md",
        "_shared/fragments/topic/scada-anomaly-detection.md",
        "_shared/fragments/journal/applied-energy.md",
        "_shared/fragments/journal/energy.md",
        "_shared/fragments/journal/renewable-energy.md",
        "_shared/fragments/journal/nature-energy.md",
        "_shared/fragments/journal/joule.md",
        "_shared/fragments/journal/ieee-tste.md",
        "_shared/fragments/manuscript/wind-conformal-benchmark.md",
    ]
    required_headings = [
        "## Activation Condition",
        "## Scope",
        "## Allowed Content",
        "## Forbidden Content",
        "## Output Influence",
        "## Audit Influence",
        "## Examples",
        "## Anti Examples",
    ]
    for rel in required_fragments:
        path = ROOT / rel
        if not path.exists():
            errors.append(f"missing fragment {rel}")
            continue
        text = read_text(path)
        for heading in required_headings:
            if heading not in text:
                errors.append(f"{rel} missing fragment heading {heading}")
    topic_dir = ROOT / "_shared" / "fragments" / "topic"
    pollution_terms = ["3528", "4 wind farms", "four wind farms", "4 predictors", "four predictors", "24 horizons", "QRLSTM", "GBR"]
    for path in topic_dir.glob("*.md"):
        text = read_text(path)
        main_part = re.split(r"## Anti Examples", text, maxsplit=1)[0]
        for term in pollution_terms:
            if term.lower() in main_part.lower():
                errors.append(f"{path.relative_to(ROOT)} contains manuscript-specific term outside anti examples: {term}")

    required_skill_refs = [
        "windenergy-writing",
        "windenergy-figure",
        "windenergy-orchestrator",
        "windenergy-submission",
        "windenergy-polishing",
        "windenergy-academic-search",
        "windenergy-citation",
    ]
    for skill_name in required_skill_refs:
        skill_text = read_text(ROOT / skill_name / "SKILL.md")
        if "quality-principles.md" not in skill_text:
            errors.append(f"{skill_name}/SKILL.md missing quality-principles.md reference")
    for skill_name in ["windenergy-writing", "windenergy-polishing", "windenergy-orchestrator", "windenergy-submission"]:
        skill_text = read_text(ROOT / skill_name / "SKILL.md")
        if "narrative-principles.md" not in skill_text:
            errors.append(f"{skill_name}/SKILL.md missing narrative-principles.md reference")
    for skill_name in ["windenergy-writing", "windenergy-polishing", "windenergy-orchestrator", "windenergy-figure"]:
        skill_text = read_text(ROOT / skill_name / "SKILL.md")
        if "fragment-contract.md" not in skill_text:
            errors.append(f"{skill_name}/SKILL.md missing fragment-contract.md reference")

    writing = read_text(ROOT / "windenergy-writing" / "SKILL.md").lower()
    for phrase in [
        "claim strength control",
        "manuscript completeness checklist",
        "workflow_profile.json",
        "topic confidence",
        "high-impact narrative control",
        "section-specific",
        "related-work synthesis control",
        "section-role-matrix.md",
        "take-home message",
        "per-claim presentation check",
        "narrative_warning",
    ]:
        if phrase not in writing:
            errors.append(f"windenergy-writing/SKILL.md missing quality phrase {phrase}")

    introduction = read_text(ROOT / "windenergy-writing" / "references" / "introduction.md").lower()
    for phrase in [
        "introduction spoiler control",
        "contribution preview",
        "research-task language",
        "detailed empirical outcomes",
        "final method rankings",
        "operational recommendations",
    ]:
        if phrase not in introduction:
            errors.append(f"windenergy-writing/references/introduction.md missing phrase {phrase}")

    related_work = read_text(ROOT / "windenergy-writing" / "references" / "related-work.md").lower()
    for phrase in [
        "literature role types",
        "gap type taxonomy",
        "coverage matrix",
        "synthesis density rule",
        "related work boundary control",
        "topic bucket",
    ]:
        if phrase not in related_work:
            errors.append(f"windenergy-writing/references/related-work.md missing phrase {phrase}")

    figure = read_text(ROOT / "windenergy-figure" / "SKILL.md")
    for phrase in [
        "Times New Roman",
        "8 pt",
        "figure_text_audit.md",
        "figure_data_map.json",
        "active profile",
        "figure portfolio",
        "low-support",
        "visual-contract metadata",
        "dual-axis justification",
        "colorblind-safe palette",
    ]:
        if phrase not in figure:
            errors.append(f"windenergy-figure/SKILL.md missing figure quality phrase {phrase}")

    orchestrator_text = "\n".join(
        read_text(path)
        for path in [
            ROOT / "windenergy-orchestrator" / "SKILL.md",
            ROOT / "windenergy-orchestrator" / "references" / "workflow.md",
            ROOT / "windenergy-orchestrator" / "references" / "gates.md",
            ROOT / "windenergy-orchestrator" / "references" / "workspace-contract.md",
            ROOT / "windenergy-orchestrator" / "scripts" / "audit_manuscript_quality.py",
            ROOT / "windenergy-orchestrator" / "scripts" / "validate_stage_outputs.py",
            ROOT / "windenergy-orchestrator" / "scripts" / "collect_outputs.py",
        ]
    )
    orchestrator_text_lower = orchestrator_text.lower()
    for phrase in [
        "general scientific maturity gate",
        "scientific_maturity_audit.md",
        "manuscript_quality_audit.json",
        "figure_consistency_audit.json",
        "workflow_profile.json",
        "profile_evidence_strength",
        "mechanism_evidence_strength_audit",
        "claim strength",
        "figure professionalism",
        "profile-required display-item coverage",
        "figure portfolio",
        "NARRATIVE_WARNING",
        "related_work_synthesis_control",
        "SECTION_WARNING",
    ]:
        if phrase.lower() not in orchestrator_text_lower:
            errors.append(f"windenergy-orchestrator missing quality gate phrase {phrase}")

    submission_text = "\n".join(
        read_text(path)
        for path in [
            ROOT / "windenergy-submission" / "SKILL.md",
            ROOT / "windenergy-submission" / "references" / "final-manuscript-audit.md",
            ROOT / "windenergy-submission" / "references" / "submission-checklist.md",
        ]
    )
    for phrase in [
        "content maturity audit",
        "claim-evidence mismatch",
        "empty sections",
        "manuscript_quality_audit.json",
        "figure_consistency_audit.json",
        "profile_evidence_strength_audit.json",
        "workflow_profile.json",
        "narrative_warning",
        "profile",
        "internal workflow artifact",
    ]:
        if phrase not in submission_text.lower():
            errors.append(f"windenergy-submission missing content maturity phrase {phrase}")

    polishing_text = "\n".join(
        read_text(path)
        for path in [
            ROOT / "windenergy-polishing" / "SKILL.md",
            ROOT / "windenergy-polishing" / "references" / "style-guardrails.md",
        ]
    ).lower()
    for phrase in [
        "claim risk pass",
        "evidence-calibrated language",
        "narrative preservation pass",
        "NARRATIVE_WARNING".lower(),
        "preserve numbers",
        "table-only sections",
        "visual-language pass",
        "internal workflow artifact language",
        "profile-required display target",
    ]:
        if phrase not in polishing_text:
            errors.append(f"windenergy-polishing missing claim risk phrase {phrase}")

    academic = read_text(ROOT / "windenergy-academic-search" / "SKILL.md").lower()
    for phrase in [
        "literature coverage audit",
        "journal fit",
        "final citation errors",
        "active profile",
        "topic-bucket coverage",
        "related_work_literature_map",
        "coverage status",
        "known limitation",
        "connection to manuscript gap",
    ]:
        if phrase not in academic:
            errors.append(f"windenergy-academic-search/SKILL.md missing coverage phrase {phrase}")

    citation = read_text(ROOT / "windenergy-citation" / "SKILL.md").lower()
    for phrase in ["evidence chain", "broad literature coverage"]:
        if phrase not in citation:
            errors.append(f"windenergy-citation/SKILL.md missing evidence phrase {phrase}")

    example_path = ROOT / "windenergy-orchestrator" / "examples" / "reviewer-comment-to-skill-gap.md"
    if not example_path.exists():
        errors.append("windenergy-orchestrator missing examples/reviewer-comment-to-skill-gap.md")
    else:
        example = read_text(example_path).lower()
        for phrase in [
            "claim strength control",
            "figure professionalism",
            "display-item coverage",
            "figure portfolio",
            "method reproducibility",
            "evidence chain",
            "result granularity",
            "low-support condition",
            "journal fit",
            "reproducibility wording",
            "manuscript completeness",
        ]:
            if phrase not in example:
                errors.append(f"reviewer-comment-to-skill-gap.md missing {phrase}")


def validate_tool_failure_recovery(errors: list[str]) -> None:
    shared = read_text(ROOT / "_shared" / "core" / "output-run-folders.md")
    revision = read_text(ROOT / "windenergy-submission" / "references" / "revision-protocol.md")
    for path_name, text in [
        ("output-run-folders.md", shared),
        ("revision-protocol.md", revision),
    ]:
        for phrase in ["Tool Failure Recovery", "file_path", "content", "polish_docx.py"]:
            if phrase not in text:
                errors.append(f"{path_name} missing tool failure recovery phrase {phrase}")


def validate_complex_ooxml_guard(errors: list[str]) -> None:
    revision = read_text(ROOT / "windenergy-submission" / "references" / "revision-protocol.md")
    for phrase in ["MathType", "complex OOXML", "Do not rebuild such paragraphs"]:
        if phrase not in revision:
            errors.append(f"revision-protocol.md missing complex OOXML guard {phrase}")


def validate_final_manuscript_audit(errors: list[str]) -> None:
    final_audit = read_text(ROOT / "windenergy-submission" / "references" / "final-manuscript-audit.md")
    submission_skill = read_text(ROOT / "windenergy-submission" / "SKILL.md")
    citation_skill = read_text(ROOT / "windenergy-citation" / "SKILL.md")
    polishing_skill = read_text(ROOT / "windenergy-polishing" / "SKILL.md")
    for phrase in ["Abbreviation Audit", "Citation Audit", "windenergy-citation", "windenergy-polishing"]:
        if phrase not in final_audit:
            errors.append(f"final-manuscript-audit.md missing {phrase}")
    if "abbreviations" not in submission_skill or "citation" not in submission_skill:
        errors.append("windenergy-submission/SKILL.md missing final manuscript audit routing")
    if "Final Citation Audit" not in citation_skill:
        errors.append("windenergy-citation/SKILL.md missing Final Citation Audit")
    if "Audit abbreviations" not in polishing_skill:
        errors.append("windenergy-polishing/SKILL.md missing abbreviation audit")


def validate_migration_upgrade(errors: list[str]) -> None:
    migration = ROOT.parent / "migration-notes.md"
    requirements = ROOT.parent / "requirements-dev.txt"
    if not migration.exists():
        errors.append("missing migration-notes.md")
    else:
        text = read_text(migration)
        for phrase in [
            "20ca94313e18463e1eabf4616f958de94372c434",
            "5d2ba1dee1c087be6de8f4a8aad4b27f04974be9",
            "windenergy-reviewer",
            "nature-skills",
        ]:
            if phrase not in text:
                errors.append(f"migration-notes.md missing {phrase}")

    if not requirements.exists():
        errors.append("missing requirements-dev.txt")
    else:
        text = read_text(requirements).lower()
        for package in ["pyyaml", "matplotlib", "numpy"]:
            if package not in text:
                errors.append(f"requirements-dev.txt missing {package}")

    router_skills = [
        "windenergy-academic-search",
        "windenergy-citation",
        "windenergy-data",
        "windenergy-figure",
        "windenergy-paper2ppt",
        "windenergy-reader",
        "windenergy-response",
        "windenergy-reviewer",
    ]
    for skill_name in router_skills:
        base = ROOT / skill_name
        for rel in ["manifest.yaml", "static/core"]:
            if not (base / rel).exists():
                errors.append(f"{skill_name} missing router path {rel}")
        skill_text = read_text(base / "SKILL.md")
        if "Router Protocol" not in skill_text:
            errors.append(f"{skill_name}/SKILL.md missing Router Protocol")


def validate_evals_and_atlas(errors: list[str]) -> None:
    eval_skills = [
        "windenergy-academic-search",
        "windenergy-figure",
        "windenergy-reader",
        "windenergy-response",
        "windenergy-reviewer",
    ]
    for skill_name in eval_skills:
        path = ROOT / skill_name / "evals" / "evals.json"
        if not path.exists():
            errors.append(f"{skill_name} missing evals/evals.json")
            continue
        text = read_text(path)
        for phrase in ["skill_name", "evals", "expected_output"]:
            if phrase not in text:
                errors.append(f"{path.relative_to(ROOT)} missing {phrase}")

    reviewer = ROOT / "windenergy-reviewer"
    for rel in [
        "static/core/source-basis.md",
        "static/core/workflow.md",
        "static/core/output-contract.md",
        "static/fragments/reviewer_lens/energy-significance.md",
        "static/fragments/reviewer_lens/method-reproducibility.md",
        "static/fragments/reviewer_lens/ai-statistics.md",
        "references/review-rubric.md",
    ]:
        if not (reviewer / rel).exists():
            errors.append(f"windenergy-reviewer missing {rel}")

    figure = ROOT / "windenergy-figure"
    for rel in [
        "assets/figures4papers/windenergy_atlas/generate_windenergy_atlas.py",
        "assets/figures4papers/windenergy_atlas/atlas_qa.md",
        "references/atlas-index.md",
    ]:
        if not (figure / rel).exists():
            errors.append(f"windenergy-figure missing {rel}")

    slugs = [
        "atlas-01-wind-rose",
        "atlas-02-power-curve",
        "atlas-03-forecast-timeseries",
        "atlas-04-error-distribution",
        "atlas-05-interval-reliability",
        "atlas-06-model-comparison-ci",
        "atlas-07-ablation-heatmap",
        "atlas-08-wake-layout",
        "atlas-09-storage-market",
        "atlas-10-mechanism-flow",
    ]
    for slug in slugs:
        for suffix in ["png", "svg", "pdf"]:
            path = figure / "assets" / "chart-atlas" / f"{slug}.{suffix}"
            if not path.exists():
                errors.append(f"windenergy-figure missing chart-atlas/{slug}.{suffix}")
    if not (figure / "assets" / "gallery" / "atlas-01-wind-rose.png").exists():
        errors.append("windenergy-figure missing gallery/atlas-01-wind-rose.png")


def main() -> int:
    errors: list[str] = []
    validate_skill_frontmatter(errors)
    validate_manifest_paths(errors)
    validate_submission_revision_protocol(errors)
    validate_agents_metadata(errors)
    validate_output_run_folder_protocol(errors)
    validate_journal_slugs(errors)
    validate_forbidden_chars(errors)
    validate_polishing_requirements(errors)
    validate_citation_audit_requirements(errors)
    validate_academic_search_boundaries(errors)
    validate_response_council_requirements(errors)
    validate_orchestrator_requirements(errors)
    validate_quality_principles(errors)
    validate_final_manuscript_audit(errors)
    validate_migration_upgrade(errors)
    validate_evals_and_atlas(errors)
    validate_tool_failure_recovery(errors)
    validate_complex_ooxml_guard(errors)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
