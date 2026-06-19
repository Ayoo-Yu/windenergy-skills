# Renewable Narrative Principles

Use this reference for foreground writing: title, abstract, introduction,
highlights, contribution paragraph, discussion lead-ins, and conclusion.

## Core Rule

Narrative quality can improve structure, emphasis, sequencing, and reader
memory. It cannot increase claim strength beyond the evidence chain.

High-impact language must come from a real field tension, unresolved problem,
counterintuitive finding, mechanism explanation, operating boundary, design
principle, or practical decision rule. If the evidence is ordinary, improve the
clarity and stakes without inventing a larger contribution.

## Standard Narrative Pass

Use this for methods, experimental setup, limitations, supplementary material,
response letters, and detailed audit text.

- State the section purpose early.
- Keep technical definitions clear and reproducible.
- Preserve qualifiers, uncertainties, and scope boundaries.
- Prefer direct transitions over rhetorical framing.
- Do not hide missing evidence behind polished prose.

## High-Impact Narrative Pass

Use section-specific narrative control for foreground sections unless the user
asks for a purely technical note.

1. Identify the field-level tension, missing explanation, wrong intuition, or
   operational dilemma.
2. Match the section purpose: abstracts compress the full argument,
   introductions create the need to read, discussions explain meaning, and
   conclusions distill the final judgment.
3. Let experiment scale support the central point. Do not open with run counts
   or implementation details unless scale is the contribution.
4. Compress technical details and numeric results in abstracts. Keep only the
   numbers that anchor the main judgment.
5. End abstracts and conclusions with a take-home message: method selection,
   operating boundary, mechanism correction, design rule, or field-level update.
6. Keep conservative wording when evidence is bounded, while preserving the
   manuscript's importance.

## Section-Specific Narrative Control

- **Title, abstract, and highlights**: reveal the central finding when evidence
  is available. Compress technical detail and keep only the numbers that anchor
  the main judgment.
- **Introduction**: identify the field tension, unresolved question, difficulty,
  evidence design, and contribution types. Use research-task language before
  evidence is presented.
- **Related Work**: build a literature map rather than a background tutorial.
  Group studies by research line, compare assumptions, mechanisms, data
  settings, and evaluation criteria, then identify the unresolved gap the
  manuscript addresses. Use synthesis language before paper-by-paper listing.
  Avoid reporting the manuscript's results or turning the section into a
  method-design justification.
- **Discussion**: interpret results, explain boundaries, compare alternatives,
  and connect evidence to scientific or operational meaning.
- **Conclusion**: synthesize the final judgment, boundary, and take-home
  message without introducing new evidence.

## Introduction Spoiler Control

Introduction may preview what the paper will diagnose, compare, explain, or
translate into guidance. It should avoid detailed empirical outcomes, numerical
effects, final method rankings, operating-boundary conclusions, or operational
recommendations that belong to Results or Discussion.

Use contribution-preview language in Introduction:

```text
We develop a diagnostic framework for ...
We examine whether ... changes the value of ...
We translate the resulting evidence into a selection framework.
```

Reserve result language for Results and Discussion:

```text
We find that ...
The evidence shows that ...
This implies that ...
```

## Narrative Diagnostics

Mark `NARRATIVE_WARNING` when a foreground section has any of these problems:

- starts with generic background and no tension
- reports experiment scale before the question is clear
- buries the core finding inside a list of numbers
- has contribution bullets that only name tasks completed
- ends without a memorable take-home message
- downgrades importance so far that the reader cannot tell why the paper
  matters
- uses Introduction to report detailed results, final rankings, numerical
  effects, or recommendations that should appear after evidence is presented

Mark `Claim risk` when the wording raises the claim strength rather than the
presentation quality.

Mark `SECTION_WARNING` when Related Work becomes a citation dump, repeats the
Introduction's motivation without literature synthesis, teaches generic
definitions without comparing studies, overuses current-paper transitions, omits
recent direct competitors when they are needed, or justifies the current
experimental protocol before Methodology.

Mark `TONE_WARNING` when the section uses review-defensive phrasing as
defined in the Review-Defensive Tone section below.

Mark `LANGUAGE_WARNING` when the section contains internal workflow
language as defined in the Internal Workflow Language section below.

## Interpretation Strength Ladder

Each section has a maximum interpretation strength. The ladder runs from
lowest to highest:

1. **Specify**: state conditions, parameters, facts. No reasoning about causes.
   (Used by: Experimental Setup)
2. **Observe**: report measured patterns. One sentence of immediate
   interpretation per finding is allowed. No mechanism explanation.
   (Used by: Results)
3. **Compare**: relate findings to prior work or alternatives. No causal claims.
   (Used by: Related Work)
4. **Interpret**: explain why a pattern occurs, propose mechanism, identify
   boundary. Must stay within evidence scope. Must address rival explanations.
   (Used by: Discussion)
5. **Synthesize**: combine established interpretations into a final judgment.
   No new depth beyond what Discussion already established.
   (Used by: Conclusion, Abstract)

When a section's prose moves above its ceiling on this ladder, it is doing
another section's job. Detect and flag this as `SECTION_WARNING`.

The ceiling for each section is defined in `section-role-matrix.md`.

## Review-Defensive Tone

Academic writing should explain findings and their meaning, not preempt
imagined reviewer objections. Review-defensive tone appears when the author
is writing to block criticism rather than to communicate understanding.

### Detection Markers

Flag `TONE_WARNING` when prose contains:

- Preemptive justifications that interrupt the argument flow
  ("To ensure fairness, we emphasize that ...")
- Self-audit phrases in the main text
  ("It is worth noting that this design avoids the common pitfall of ...")
- Evidence buried behind defensive framing
  ("Although one might argue X, our results clearly show Y")
- Hedging stacks that pad rather than qualify
  ("It may somewhat suggest a potential tendency toward ...")
- Checklist-driven paragraphs that serve the author's anxiety rather than
  the reader's understanding
- Sentences that explain what the paper does NOT do instead of what it DOES
  ("We do not claim that this method is universally applicable")
- Phrases that name reviewer concerns explicitly
  ("To prevent concerns about data leakage", "to address the common
  reviewer question")
- Justification-by-mentioning-what-was-avoided
  ("The setup is intentionally stricter than a normal performance table to
  prevent three common review concerns")

### Replacement Principle

Replace defensive framing with confident, bounded statements:

- Instead of "To address potential concerns about fairness, we use k-fold
  cross-validation", write "We use k-fold cross-validation to estimate
  generalization."
- Instead of "Although this study does not prove causation, the pattern is
  consistent with...", write "The pattern is consistent with [mechanism],
  though causal isolation would require [stated condition]."
- Instead of "The setup is intentionally stricter than a normal performance
  table to prevent reviewer concerns", write "The benchmark uses
  chronological splits without shuffling to prevent temporal leakage."

### Scope

This rule applies to all sections. It is especially common in Discussion
and Experimental Setup. It must stay topic-neutral -- specific reviewer
objections belong in paper-type or topic fragments, not here.

## Internal Workflow Language

Manuscript prose must not contain language that reveals the author's
internal workflow, tooling, or file management. When such language appears,
replace it using the table in `quality-principles.md` under
"Internal Language Replacement".

Detection: scan for terms like "source-code setting", "source-code-verified",
"diagnostic file", "saved key slices", "configuration file", "output folder",
"run log", "pipeline stage", "checkpoint", "artifact", "revision workspace",
"regenerated", "control file", or any filename pattern
(e.g., `preprocess.py`, `model_v2_final.pth`).

Flag as `LANGUAGE_WARNING` and apply the replacement table.
