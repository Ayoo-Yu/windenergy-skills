# Journal Fragment: Applied Energy

## Activation Condition

Load only when the target journal is Applied Energy or the user asks for an
Applied Energy style full research article.

## Scope

Use for Applied Energy article framing, energy-system relevance, article depth,
reference scale, and submission readiness.

## Allowed Content

Energy-system value, methodological rigor, practical implications, full-article
depth, balanced literature coverage, and submission sections expected by the
journal profile.

## Forbidden Content

Topic-specific methods, benchmark-specific numbers, or unsupported claims about
journal acceptance.

## Output Influence

Foreground the energy application and practical value while keeping the method
and evidence rigorous.

## Audit Influence

For full research articles, use the journal profile to check main-body depth,
reference scale, abstract length, declaration sections, and figure-table
adequacy. Exact thresholds belong here or in the journal profile, not in core.

## Bundled Wind Forecasting Style Profile

When the target journal is Applied Energy and the topic is wind-power
forecasting, probabilistic wind forecasting, prediction intervals, calibration,
or grid-risk forecasting, load the bundled style-learning profile from the
sibling skill:

```text
../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/main-profile/learned_style_digest.md
../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/main-profile/style_profile.yaml
../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/main-profile/figure_style.yaml
../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/visual-profile/visual_figure_style_digest.md
../windenergy-style-learning/references/profiles/applied-energy-wind-forecasting/visual-profile/visual_figure_style.yaml
```

Use the main profile for section architecture, move-level language templates,
numeric reporting, comparison language, caption syntax, table patterns, and
in-text figure references. Use the visual profile for figure aspect ratio,
palette, ink density, and topic mix.

Treat this profile as an Applied Energy wind-forecasting constraint layer above
generic `common-18` guidance. Keep the user's supplied claims, numbers,
datasets, baselines, and citations unchanged unless corrected evidence is
provided.

## Examples

"Applied Energy framing should connect the technical contribution to energy
system operation, planning, or efficiency."

## Anti Examples

"Every renewable manuscript follows Applied Energy length and reference
targets."
