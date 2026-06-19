# Renewable Manuscript Quality Principles

Use this shared reference when a renewable skill drafts, audits, polishes, or
orchestrates a manuscript. This file is the core layer. It must stay topic
neutral and journal neutral.

## Core Boundary

Core quality rules may describe scientific reasoning, evidence integrity,
manuscript completeness, visual readability, journal fit, and language control.
Core rules must not contain a specific paper's experiment design, model set,
metric set, result count, reviewer patch, or target-journal numeric threshold.

Load paper-type, topic, journal, and manuscript fragments for specialized
requirements. When specialized rules are needed but no profile is available,
mark the item `UNCHECKED` or `AUTHOR_INPUT_NEEDED`.

## Conflict Priority

Apply rules in this order:

1. User explicit requirement.
2. Journal hard limits.
3. Factual evidence and claim strength.
4. Section purpose.
5. Topic checklist.
6. Style preference.

## Claim Strength Control

Match every major claim to the evidence available.

- `Observation`: a measured pattern is reported.
- `Evidence suggests`: several diagnostics support a cautious interpretation.
- `Consistent with`: results align with an explanation but do not isolate it.
- `Demonstrates`: the design directly tests the stated effect.
- `First`, `proves`, `universal`, and similar absolute terms require a
  completed literature audit plus direct evidence.

Check titles, abstracts, contribution bullets, results summaries, discussions,
and conclusions. If a claim extends beyond the supplied evidence, mark
`Claim risk` and propose a stronger supported rewrite.

## Evidence Chain

Every core claim needs a traceable chain:

- manuscript claim
- source artifact or verified citation
- method, metric, table, figure, dataset note, code path, or result file
- uncertainty, limitation, or boundary condition

When the chain is incomplete, mark the claim `UNCHECKED` or
`AUTHOR_INPUT_NEEDED`. Do not fill gaps with generic domain knowledge.

## Manuscript Completeness

A mature research article must let an expert reviewer assess scope,
reproducibility, and contribution.

- Abstract states the question, approach, core finding, implication, and
  boundary.
- Introduction identifies the field-level problem and explains why the paper's
  evidence can address it.
- Related Work covers the application domain, method family, evaluation
  criteria, and closest alternatives that are relevant to the profile.
- Methodology defines algorithms, assumptions, parameters, and implementation
  details needed to reproduce the work.
- Experimental Setup defines data provenance, sampling, study period, splits,
  inputs, targets, preprocessing, exclusions, and evaluation protocol when
  relevant to the paper type.
- Results separate direct observations from interpretation.
- Discussion explains boundaries, limitations, and practical implications.
- Conclusion does not introduce new evidence.

Empty sections, placeholder text, undefined abbreviations, missing method
settings, and missing data provenance block a ready conclusion.

## Figure Professionalism

Publication figures must be readable, consistent, and claim-linked.

- Use one font policy across the figure set.
- Keep figure text legible at final printed size.
- Use consistent line widths, marker sizes, panel labels, and legend policy.
- Use accessible colors and keep semantic color meanings stable.
- Axis titles must state the metric, unit, and target quantity clearly.
- Captions should state the conclusion first, then define data, metric, sample,
  and panels.
- Quantitative figures need a data map or equivalent provenance record.
- Figure text audits should compare the figure, caption, table, and main text.

Topic fragments may add axis conventions, metric checks, or chart families for
the active research area.

## Journal Fit

Adapt depth, structure, literature coverage, and presentation to the target
journal profile. Journal fragments own hard limits such as article length,
reference scale, abstract length, figure count, and required submission files.

If no journal profile is active, use general scholarly norms and mark
journal-specific readiness checks `UNCHECKED`.

## Language and Tone Quality

### Internal Language Replacement Table

Manuscript prose must not contain internal workflow, tooling, or file
management language. Replace with scholarly equivalents:

| Internal phrase | Scholarly replacement |
|----------------|----------------------|
| source-code setting | parameter configuration |
| source-code-verified | verified against the reproducibility audit |
| diagnostic file | diagnostic output |
| saved key slices | selected representative samples |
| configuration file | configuration settings |
| output folder | (remove; not needed in manuscript) |
| run log | (remove; not needed in manuscript) |
| pipeline stage | processing step |
| checkpoint | model snapshot |
| artifact | output or result |
| revision workspace | (remove from main text, put in appendix) |
| regenerated diagnostic | reproduced diagnostic |
| control file | control comparison |
| the script / the code | the implementation |
| our internal tool | (remove or describe functionality) |
| specific filenames (e.g., preprocess.py, utils.py) | (remove filenames; describe functionality) |
| we saved / we stored | (rephrase as passive or method description) |

Detection: flag as `LANGUAGE_WARNING`. See `narrative-principles.md`
for the detection rule.

File names, workspace paths, script states, and code audit descriptions
belong in a Reproducibility statement or Appendix, never in the main
argument.

### Review-Defensive Tone Quality Check

Before finalizing any section, verify:

- Each paragraph advances the reader's understanding, not the author's
  defense against imagined objections.
- Justifications are concise and placed where they support a decision,
  not scattered preemptively.
- Limitations appear in Discussion, not embedded in Results or Setup.
- Hedging matches evidence strength without stacking qualifiers.
- The prose explains what was done and why, not what reviewers might
  think about it.

Flag as `TONE_WARNING`. See `narrative-principles.md` for the full
detection rule.

### Inter-Chapter Boundary Check

Before finalizing, verify that no section has leaked into another:

- Methodology contains no experimental conditions or result previews.
- Experimental Setup contains no method definitions or result
  interpretations.
- Results contains no mechanism explanations, operational recommendations,
  or literature reconnection.
- Discussion does not re-narrate Results without adding interpretation.
- Conclusion does not compress Results or re-write the Abstract.

Flag as `SECTION_WARNING` when a section exceeds its interpretation
ceiling defined in `section-role-matrix.md`.

## Warning Semantics

- `FAIL`: a checked item violates a blocking rule.
- `UNCHECKED`: the item cannot be checked because evidence, profile, file, or
  tool output is missing.
- `AUTHOR_INPUT_NEEDED`: the author must provide a fact or decision.
- `NARRATIVE_WARNING`: a foreground writing section lacks problem tension,
  take-home message, or synthesis, or an Introduction leaks detailed results
  before the evidence has been presented, while the facts may be correct.
- `SECTION_WARNING`: a section is structurally weak or immature but checkable.
- `LANGUAGE_WARNING`: the section contains internal workflow language
  that must be replaced with scholarly equivalents per the replacement
  table in this file.
- `TONE_WARNING`: the section uses review-defensive phrasing as defined
  in `narrative-principles.md`.

Warnings can block a ready status when they affect title, abstract,
contribution, conclusion, or final submission quality.
