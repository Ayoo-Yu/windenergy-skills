from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "windenergy-orchestrator" / "scripts"))

from audit_writing_quality import audit_writing_quality  # noqa: E402


class WritingQualityAuditTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="writing_quality_test_"))
        (self.tmp / "drafts").mkdir()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def write_tex(self, body: str) -> None:
        (self.tmp / "drafts" / "paper_polished.tex").write_text(
            "\\documentclass{article}\n"
            "\\title{Adaptive Conformal Calibration for Wind Interval Forecasting}\n"
            "\\author{Author names to be added}\n"
            "\\begin{document}\n"
            "\\maketitle\n"
            + body
            + "\n\\end{document}\n",
            encoding="utf-8",
        )

    def test_flags_draft_residue_terminology_and_discussion_gap(self) -> None:
        self.write_tex(
            r"""
\begin{abstract}
We evaluate 88704 runs, 24 horizons, 11 levels, 4 sites, 7 methods, 0.456913
winner rate, -0.376799 score difference, and 0.798295 ramping rate.
\end{abstract}
\section{Introduction}
Wind interval forecasting has an unresolved calibration question. We develop a
benchmark to diagnose when adaptive conformal calibration helps.
\section{Related Work}
\subsection{Wind forecasting}
One research line studies probabilistic forecasting \citep{a,b,c}. This
literature establishes calibration and sharpness as core criteria, but the
operating boundary remains unclear.
\subsection{Conformal prediction}
Another research line studies conformal prediction. These studies compare
assumptions and mechanisms across exchangeable and time-series settings.
\subsection{Evaluation}
Evaluation work studies interval score and coverage diagnostics. The unresolved
gap is a multi-axis benchmark.
\section{Methodology}
ACI, AgACI, EnbPI, NEX, and SPCI are used. FACI is treated as an implementation
label in this draft because the citation mapping remains author dependent.
\section{Experimental Setup}
The setup lists zones and methods.
\section{Results}
\subsection{Rolling diagnostics}
High alpha overcoverage appears in high alpha settings. High alpha overcoverage
is repeated again. High alpha overcoverage is repeated again. Figure evidence
supports a bounded claim.
\begin{figure}\caption{Result}\end{figure}
\section{Discussion}
The result is consistent with the idea that residual structure matters. The
same bounded claim remains visible. To be completed by the authors.
\section{Conclusion}
Adaptive conformal calibration has conditional value for wind interval
forecasting.
"""
        )

        report = audit_writing_quality(self.tmp)
        statuses = {item["check"]: item["status"] for item in report["items"]}

        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(statuses["draft_residue_cleanup"], "FAIL")
        self.assertEqual(statuses["abstract_number_density"], "NARRATIVE_WARNING")
        self.assertEqual(statuses["alpha_coverage_terminology"], "LANGUAGE_WARNING")
        self.assertEqual(statuses["discussion_depth"], "NARRATIVE_WARNING")

    def test_flags_method_without_citation_and_undefined_process_label(self) -> None:
        self.write_tex(
            r"""
\begin{abstract}
This paper studies adaptive calibration and states a bounded take-home message.
\end{abstract}
\section{Introduction}
Wind interval forecasting has an unresolved calibration question. However, the
method choice remains difficult.
\section{Related Work}
\subsection{Wind forecasting}
One research line studies probabilistic forecasting \citep{a,b,c}. This
literature establishes calibration and sharpness as core criteria, but the
operating boundary remains unclear.
\subsection{Conformal prediction}
Another research line studies conformal prediction and adaptive calibration.
\subsection{Evaluation}
Evaluation work studies interval score and coverage diagnostics.
\section{Methodology}
FACI uses an adaptive update rule. Phase 3 condition summaries are used for
the final comparison.
\section{Experimental Setup}
The setup lists data source, sampling interval, time span, features, target,
missing values, exclusions, and train validation test split.
\section{Results}
\subsection{Main comparison}
The central result shows a conditional pattern while preserving boundary
language. Figure evidence reports the comparison.
\begin{figure}\caption{Result}\end{figure}
\section{Discussion}
The finding matters operationally because method choice depends on the decision
context and reconnects to prior work \citep{a}.
\section{Conclusion}
Adaptive conformal calibration has conditional value for wind interval
forecasting.
"""
        )

        report = audit_writing_quality(self.tmp)
        statuses = {item["check"]: item["status"] for item in report["items"]}

        self.assertEqual(statuses["method_citation_binding"], "SECTION_WARNING")
        self.assertEqual(statuses["undefined_process_terms"], "SECTION_WARNING")


if __name__ == "__main__":
    unittest.main()
