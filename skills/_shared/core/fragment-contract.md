# Fragment Contract

Fragments add specialization after core rules are loaded. They must remain
small, scoped, and profile-driven.

## Required Headings

Every fragment must include these headings:

- Activation Condition
- Scope
- Allowed Content
- Forbidden Content
- Output Influence
- Audit Influence
- Examples
- Anti Examples

## Routing Confidence

Use these thresholds for topic loading:

- `topic_confidence < 0.70`: load only core and paper-type fragments.
- `0.70 <= topic_confidence < 0.85`: load a lightweight topic fragment or only
  the general part of the topic fragment.
- `topic_confidence >= 0.85`: load the full topic fragment.

If low confidence affects writing direction or audit readiness, mark
`AUTHOR_INPUT_NEEDED` or a routing warning.

## Fragment Boundaries

Paper-type fragments define argument shape and evidence form. Topic fragments
define stable domain concepts, methods, metrics, and common failure modes.
Journal fragments define venue limits and presentation expectations. Manuscript
fragments define one paper's evidence, reviewer history, benchmark artifacts,
and author-specific decisions.

Topic fragments must not contain single-manuscript experiment counts, model
lists, table numbers, reviewer patches, workspace files, or manuscript-specific
conclusions.
