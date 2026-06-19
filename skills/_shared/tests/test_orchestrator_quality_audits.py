from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "windenergy-orchestrator" / "scripts"))

from audit_manuscript_quality import run_all_audits  # noqa: E402
from validate_stage_outputs import validate_stages  # noqa: E402


class OrchestratorQualityAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="renewable_quality_test_"))
        for rel in ["final", "drafts", "audits", "diagnostics", "figures", "literature"]:
            (self.tmp / rel).mkdir(parents=True, exist_ok=True)

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def write_tex(self, body: str) -> None:
        (self.tmp / "final" / "paper.tex").write_text(
            "\\documentclass{article}\n"
            "\\begin{document}\n"
            + body
            + "\n\\bibliographystyle{unsrt}\n\\bibliography{refs}\n\\end{document}\n",
            encoding="utf-8",
        )

    def write_profile(
        self,
        *,
        topics: list[str] | None = None,
        topic_confidence: dict[str, float] | None = None,
        journal: str = "",
        thresholds: dict | None = None,
    ) -> None:
        profile = {
            "paper_type": "research",
            "topics": topics or [],
            "journal": journal,
            "paper_type_confidence": 0.8,
            "topic_confidence": topic_confidence or {},
            "journal_confidence": 0.9 if journal else 0.0,
            "profile_source": "unit test",
            "routing_notes": [],
            "loaded_fragments": [],
            "disabled_fragments": [],
            "quality_thresholds": thresholds or {},
        }
        (self.tmp / "workflow_profile.json").write_text(json.dumps(profile, indent=2), encoding="utf-8")

    def generic_body(self) -> str:
        return r"""
\begin{abstract}
This paper studies an energy system planning problem where existing practice
does not clearly connect model outputs to operational decisions. We evaluate a
data-driven workflow, report bounded evidence, and derive a practical selection
rule. The take-home message is that method value should be judged by the
decision it improves.
\end{abstract}
\section{Introduction}
Energy system studies often report technical performance without explaining
which operational uncertainty or decision gap is being addressed. However, a
complete manuscript must connect evidence to the system decision and then state
the boundary of that evidence.
\section{Methodology}
The workflow describes the algorithm, assumptions, parameters, configuration,
software implementation, and model procedure used in the evaluation.
\section{Experimental Setup}
The data source, sampling interval, time period, train validation test split,
input feature set, target variable, missing value handling, preprocessing
filters, and exclusions are reported.
\section{Results}
The results are reported cautiously.
\section{Discussion}
The operational recommendation is supported at the same granularity as the
reported results.
\section{Conclusion}
Overall, the study provides a bounded decision rule and states the remaining
evidence limits.
"""

    def test_generic_profile_does_not_trigger_specific_topic_requirements(self) -> None:
        self.write_profile()
        self.write_tex(self.generic_body())
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["experimental_setup_fields"]["status"], "PASS")
        self.assertEqual(manuscript_items["methodology_fields"]["status"], "PASS")
        joined = json.dumps(report, ensure_ascii=False)
        for forbidden in ["NWP", "Kupiec", "Christoffersen", "interval_score_decomposition"]:
            self.assertNotIn(forbidden, joined)

    def test_conformal_profile_triggers_topic_controls(self) -> None:
        self.write_profile(
            topics=["conformal-calibration"],
            topic_confidence={"conformal-calibration": 0.95},
        )
        self.write_tex(
            r"""
\section{Introduction}
However, this paper studies a calibration problem and states a mechanism claim.
\section{Methodology}
The algorithm, assumptions, parameters, implementation, and calibration
procedure are described.
\section{Experimental Setup}
The data source, sampling interval, time period, train validation test split,
input feature set, target variable, missing value handling, preprocessing
filters, and exclusions are reported.
\section{Results}
The mechanism is fully explained by the reported behavior.
\section{Conclusion}
Overall, the study provides a bounded decision rule.
"""
        )
        report = run_all_audits(self.tmp)
        self.assertEqual(report["profile_evidence"]["status"], "FAIL")

    def test_low_confidence_topic_does_not_load_heavy_topic_checks(self) -> None:
        self.write_profile(
            topics=["conformal-calibration"],
            topic_confidence={"conformal-calibration": 0.60},
        )
        self.write_tex(self.generic_body())
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["methodology_fields"], "PASS")
        self.assertEqual(report["profile_evidence"]["status"], "PASS")

    def test_applied_energy_profile_triggers_reference_target(self) -> None:
        self.write_profile(journal="applied-energy", thresholds={"reference_min": 40})
        self.write_tex(self.generic_body())
        (self.tmp / "literature" / "refs.bib").write_text(
            "\n".join(f"@article{{ref{i}, title={{Reference {i}}}}}" for i in range(19)),
            encoding="utf-8",
        )
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["reference_pool_size"], "UNCHECKED")

    def test_applied_energy_defaults_apply_when_thresholds_missing(self) -> None:
        self.write_profile(journal="Applied Energy")
        self.write_tex(self.generic_body())
        (self.tmp / "literature" / "refs.bib").write_text(
            "\n".join(f"@article{{ref{i}, title={{Reference {i}}}}}" for i in range(17)),
            encoding="utf-8",
        )
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["main_body_word_count"], "FAIL")
        self.assertEqual(manuscript_items["reference_pool_size"], "UNCHECKED")
        self.assertEqual(manuscript_items["figure_count"], "UNCHECKED")

    def test_target_journal_missing_declarations_needs_author_input(self) -> None:
        self.write_profile(journal="Applied Energy")
        self.write_tex(self.generic_body())
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["declaration_integrity"], "AUTHOR_INPUT_NEEDED")

    def test_fallback_workflow_profile_is_blocking_failure(self) -> None:
        fallback_profile = {
            "profile": {
                "paper_type": ["mechanism paper"],
                "topics": ["conformal calibration"],
                "journal": "Applied Energy",
                "confidence": "high",
            },
            "workflow_skill_mapping": {
                "requested_renewable_orchestrator": "local paper workflow orchestrator",
            },
        }
        (self.tmp / "workflow_profile.json").write_text(json.dumps(fallback_profile, indent=2), encoding="utf-8")
        self.write_tex(self.generic_body())
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["workflow_profile_contract"], "FAIL")
        self.assertEqual(manuscript_items["main_body_word_count"], "FAIL")

    def test_ready_manifest_conflicting_with_missing_stages_fails_validation(self) -> None:
        self.write_profile()
        (self.tmp / "final").mkdir(exist_ok=True)
        (self.tmp / "final" / "paper.tex").write_text("\\documentclass{article}\n", encoding="utf-8")
        (self.tmp / "final" / "paper.pdf").write_bytes(b"%PDF-1.4\n")
        (self.tmp / "final_manifest.json").write_text(
            json.dumps({"status": "ready", "ready": True}, indent=2),
            encoding="utf-8",
        )
        report = validate_stages(self.tmp)
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(any(stage["stage"] == "final_manifest_consistency" for stage in report["stages"]))

    def test_abstract_without_take_home_message_gets_narrative_warning(self) -> None:
        self.write_profile()
        self.write_tex(
            r"""
\begin{abstract}
This paper presents a study of renewable energy data. The manuscript describes
the method, the experiment, the results, and the tables. Several numerical
outputs are listed in the evaluation. The text remains factual and complete but
does not tell the reader what larger message should be remembered.
\end{abstract}
\section{Introduction}
However, the study addresses an operational gap.
\section{Methodology}
The workflow describes the algorithm, assumptions, parameters, implementation,
and model procedure.
\section{Experimental Setup}
The data source, sampling interval, time period, train validation test split,
input feature set, target variable, missing value handling, preprocessing
filters, and exclusions are reported.
\section{Results}
The results are reported cautiously.
\section{Conclusion}
The conclusion is concise.
"""
        )
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["foreground_narrative"], "NARRATIVE_WARNING")

    def test_introduction_question_and_design_preview_passes_spoiler_control(self) -> None:
        self.write_profile()
        self.write_tex(
            r"""
\begin{abstract}
This paper studies an energy decision problem where method choice remains
unclear. We develop a bounded evaluation workflow and synthesize its evidence
into a decision principle. Overall, the take-home message is that claims should
follow the decision context.
\end{abstract}
\section{Introduction}
However, existing studies leave unresolved how technical performance should be
connected to operational value. This paper asks whether a diagnostic comparison
can expose the conditions under which alternative methods should be evaluated.
We develop a diagnostic framework, examine candidate moderators, and translate
the resulting evidence into a selection framework.
\section{Methodology}
The workflow describes the algorithm, assumptions, parameters, implementation,
and model procedure.
\section{Experimental Setup}
The data source, sampling interval, time period, train validation test split,
input feature set, target variable, missing value handling, preprocessing
filters, and exclusions are reported.
\section{Results}
The results are reported cautiously.
\section{Conclusion}
Overall, the study provides a bounded decision rule.
"""
        )
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["introduction_spoiler_control"], "PASS")

    def test_introduction_result_leakage_gets_narrative_warning(self) -> None:
        self.write_profile()
        self.write_tex(
            r"""
\section{Introduction}
However, existing studies leave unresolved how technical performance should be
connected to operational value. We find that Method A outperforms Method B by
12% and should be selected under high-demand operation.
\section{Methodology}
The workflow describes the algorithm, assumptions, parameters, implementation,
and model procedure.
\section{Experimental Setup}
The data source, sampling interval, time period, train validation test split,
input feature set, target variable, missing value handling, preprocessing
filters, and exclusions are reported.
\section{Results}
The results are reported cautiously.
\section{Conclusion}
Overall, the study provides a bounded decision rule.
"""
        )
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["introduction_spoiler_control"], "NARRATIVE_WARNING")

    def test_results_and_discussion_result_language_does_not_trigger_intro_spoiler(self) -> None:
        self.write_profile()
        self.write_tex(
            r"""
\section{Introduction}
However, existing studies leave unresolved how technical performance should be
connected to operational value. We develop a diagnostic framework, examine
candidate moderators, and translate the resulting evidence into a selection
framework.
\section{Methodology}
The workflow describes the algorithm, assumptions, parameters, implementation,
and model procedure.
\section{Experimental Setup}
The data source, sampling interval, time period, train validation test split,
input feature set, target variable, missing value handling, preprocessing
filters, and exclusions are reported.
\section{Results}
We find that Method A outperforms Method B by 12%.
\section{Discussion}
This implies that practitioners should evaluate the method under the reported
decision context.
\section{Conclusion}
Overall, the study provides a bounded decision rule.
"""
        )
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["introduction_spoiler_control"], "PASS")

    def test_related_work_background_and_design_note_gets_section_warning(self) -> None:
        self.write_profile()
        self.write_tex(
            r"""
\section{Introduction}
However, existing studies leave unresolved how technical performance should be
connected to operational value.
\section{Related Work}
Renewable energy systems are important for clean power. Many papers study
models, optimization, and data-driven tools. This paper uses a new workflow and
we evaluate the method with a train validation test split. This paper compares
several baselines and reports a practical design.
\section{Methodology}
The workflow describes the algorithm, assumptions, parameters, implementation,
and model procedure.
\section{Experimental Setup}
The data source, sampling interval, time period, train validation test split,
input feature set, target variable, missing value handling, preprocessing
filters, and exclusions are reported.
\section{Results}
The results are reported cautiously.
\section{Conclusion}
Overall, the study provides a bounded decision rule.
"""
        )
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["related_work_synthesis_control"], "SECTION_WARNING")

    def test_related_work_literature_map_and_gap_synthesis_passes(self) -> None:
        self.write_profile()
        self.write_tex(
            r"""
\section{Introduction}
However, existing studies leave unresolved how technical performance should be
connected to operational value.
\section{Related Work}
Three literature strands define the problem context. The first body of work
studies application-domain decision support and establishes why operational
context changes the value of technical metrics \cite{a,b}. These studies share
the assumption that model outputs are useful only when evaluation criteria match
the decision setting, but the mechanism connecting accuracy and action remains
less clear.

A second research line develops method-family tools for energy-system analysis
\cite{c,d}. This literature compares assumptions, mechanisms, and data settings
across model classes, and it shows that the same method family can behave
differently across operating contexts. The unresolved gap is an evaluation
question: prior work rarely separates method behavior from the decision
boundary that makes the behavior useful.

Benchmark and evaluation studies provide the third strand \cite{e,f}. They
define common metrics and representative competitors, yet their common paradigm
usually summarizes aggregate performance before testing which assumption or
failure mode explains the observed ranking. Together, the literature motivates
a manuscript that validates the gap through structured evidence rather than a
new implementation alone.
\section{Methodology}
The workflow describes the algorithm, assumptions, parameters, implementation,
and model procedure.
\section{Experimental Setup}
The data source, sampling interval, time period, train validation test split,
input feature set, target variable, missing value handling, preprocessing
filters, and exclusions are reported.
\section{Results}
The results are reported cautiously.
\section{Conclusion}
Overall, the study provides a bounded decision rule.
"""
        )
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["related_work_synthesis_control"], "PASS")

    def test_related_work_current_paper_overuse_gets_section_warning(self) -> None:
        self.write_profile()
        self.write_tex(
            r"""
\section{Introduction}
However, existing studies leave unresolved how technical performance should be
connected to operational value.
\section{Related Work}
Prior work studies energy-system decision support \cite{a,b,c}. This paper
uses a different pipeline. This paper compares a broader set of alternatives.
Our benchmark evaluates the methods under a common protocol. We use this
literature to design the experiment, and we evaluate the final method family in
the next sections.
\section{Methodology}
The workflow describes the algorithm, assumptions, parameters, implementation,
and model procedure.
\section{Experimental Setup}
The data source, sampling interval, time period, train validation test split,
input feature set, target variable, missing value handling, preprocessing
filters, and exclusions are reported.
\section{Results}
The results are reported cautiously.
\section{Conclusion}
Overall, the study provides a bounded decision rule.
"""
        )
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["related_work_synthesis_control"], "SECTION_WARNING")

    def test_related_work_result_language_gets_section_warning(self) -> None:
        self.write_profile()
        self.write_tex(
            r"""
\section{Introduction}
However, existing studies leave unresolved how technical performance should be
connected to operational value.
\section{Related Work}
A research line on model evaluation compares assumptions and evaluation
criteria across several studies \cite{a,b,c}. The literature establishes a
common paradigm and leaves an unresolved gap about how decisions change method
value. We find that Method A improves performance by 18% and outperforms the
alternatives in this paper.
\section{Methodology}
The workflow describes the algorithm, assumptions, parameters, implementation,
and model procedure.
\section{Experimental Setup}
The data source, sampling interval, time period, train validation test split,
input feature set, target variable, missing value handling, preprocessing
filters, and exclusions are reported.
\section{Results}
The results are reported cautiously.
\section{Conclusion}
Overall, the study provides a bounded decision rule.
"""
        )
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["related_work_synthesis_control"], "SECTION_WARNING")

    def test_related_work_literature_map_contract_has_required_fields(self) -> None:
        text = (ROOT / "windenergy-academic-search" / "SKILL.md").read_text(encoding="utf-8")
        for phrase in [
            "related_work_literature_map",
            "topic bucket",
            "search queries used",
            "representative papers",
            "seminal papers",
            "recent direct competitors",
            "known limitation",
            "connection to manuscript gap",
            "coverage status",
        ]:
            self.assertIn(phrase, text)

    def test_storage_optimization_smoke_does_not_import_forecasting_terms(self) -> None:
        self.write_profile(
            topics=["storage-optimization"],
            topic_confidence={"storage-optimization": 0.95},
        )
        self.write_tex(self.generic_body())
        report = run_all_audits(self.tmp)
        joined = json.dumps(report, ensure_ascii=False)
        for forbidden in ["wind forecasting", "NWP", "curtailment", "interval score", "forecast horizon"]:
            self.assertNotIn(forbidden, joined)

    def test_internal_workflow_language_gets_language_warning(self) -> None:
        self.write_profile()
        self.write_tex(
            r"""
\section{Introduction}
However, the study addresses an operational gap.
\section{Methodology}
The workflow describes the algorithm, assumptions, parameters, implementation,
and model procedure.
\section{Experimental Setup}
The data source, sampling interval, time period, train validation test split,
input feature set, target variable, missing value handling, preprocessing
filters, and exclusions are reported.
\section{Results}
The diagnostic file records the observed comparison.
\section{Conclusion}
Overall, the study provides a bounded decision rule.
"""
        )
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["internal_workflow_language_warning"], "LANGUAGE_WARNING")

    def test_review_defensive_tone_gets_tone_warning(self) -> None:
        self.write_profile()
        self.write_tex(
            r"""
\section{Introduction}
However, the study addresses an operational gap.
\section{Methodology}
The workflow describes the algorithm, assumptions, parameters, implementation,
and model procedure.
\section{Experimental Setup}
To prevent reviewer concerns about leakage, the data source, sampling interval,
time period, train validation test split, input feature set, target variable,
missing value handling, preprocessing filters, and exclusions are reported.
\section{Results}
The results are reported cautiously.
\section{Conclusion}
Overall, the study provides a bounded decision rule.
"""
        )
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["review_defensive_tone_warning"], "TONE_WARNING")

    def test_missing_figure_data_map_is_unchecked(self) -> None:
        self.write_profile()
        self.write_tex(
            self.generic_body()
            + r"""
\begin{figure}
\includegraphics{../figures/quantitative_result.png}
\caption{Quantitative result}
\end{figure}
"""
        )
        report = run_all_audits(self.tmp)
        self.assertEqual(report["figure"]["status"], "UNCHECKED")

    def test_conflicting_plotted_value_fails_figure_audit(self) -> None:
        self.write_profile()
        self.write_tex(
            self.generic_body()
            + r"""
\begin{figure}
\includegraphics{../figures/result.png}
\caption{Result}
\end{figure}
"""
        )
        (self.tmp / "figures" / "figure_data_map.json").write_text(
            json.dumps(
                {
                    "figures": [
                        {
                            "figure": "result.png",
                            "source": "table.csv",
                            "tolerance": 0.01,
                            "values": [{"label": "reported value", "plotted_value": 0.62, "table_value": 0.31}],
                        }
                    ]
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        report = run_all_audits(self.tmp)
        self.assertEqual(report["figure"]["status"], "FAIL")

    def test_figure_visual_contract_flags_dual_axis_and_palette(self) -> None:
        self.write_profile()
        self.write_tex(
            self.generic_body()
            + r"""
\begin{figure}
\includegraphics{../figures/result.png}
\caption{Result}
\end{figure}
"""
        )
        (self.tmp / "figures" / "figure_data_map.json").write_text(
            json.dumps(
                {
                    "figures": [
                        {
                            "figure": "result.png",
                            "source": "table.csv",
                            "dual_axis": True,
                            "style": {
                                "font_family": "Times New Roman",
                                "min_font_pt": 8,
                                "line_width_pt": 1.0,
                                "palette_id": "red-blue",
                                "colorblind_safe": False,
                            },
                            "values": [{"label": "reported value", "plotted_value": 0.62, "table_value": 0.62}],
                        }
                    ]
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        report = run_all_audits(self.tmp)
        figure_items = {item["check"]: item["status"] for item in report["figure"]["items"]}
        self.assertEqual(figure_items["figure_visual_contract"], "FAIL")

    def test_input_sections_are_expanded_before_audit(self) -> None:
        self.write_profile()
        (self.tmp / "sections").mkdir(exist_ok=True)
        (self.tmp / "sections" / "body.tex").write_text(
            r"""
\section{Introduction}
However, this study asks an operational question. We find that Method A
outperforms Method B by 12%.
\section{Methodology}
The workflow describes the algorithm, assumptions, parameters, implementation,
and model procedure.
\section{Experimental Setup}
The data source, sampling interval, time period, train validation test split,
input feature set, target variable, missing value handling, preprocessing
filters, and exclusions are reported.
\section{Results}
The results are reported cautiously.
\section{Conclusion}
Overall, the study provides a bounded decision rule.
""",
            encoding="utf-8",
        )
        (self.tmp / "final" / "paper.tex").write_text(
            "\\documentclass{article}\n\\begin{document}\n\\input{../sections/body.tex}\n\\end{document}\n",
            encoding="utf-8",
        )
        report = run_all_audits(self.tmp)
        manuscript_items = {item["check"]: item["status"] for item in report["manuscript"]["items"]}
        self.assertEqual(manuscript_items["introduction_spoiler_control"], "NARRATIVE_WARNING")

    def test_figure_data_map_list_shape_is_supported(self) -> None:
        self.write_profile()
        self.write_tex(
            self.generic_body()
            + r"""
\begin{figure}
\includegraphics{../figures/result.png}
\caption{Result}
\end{figure}
"""
        )
        (self.tmp / "figures" / "figure_data_map.json").write_text(
            json.dumps(
                [
                    {
                        "figure": "result.png",
                        "source": "table.csv",
                        "tolerance": 0.01,
                        "values": [{"label": "reported value", "plotted_value": 0.62, "table_value": 0.31}],
                    }
                ],
                indent=2,
            ),
            encoding="utf-8",
        )
        report = run_all_audits(self.tmp)
        self.assertEqual(report["figure"]["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
