# Writing workflow

Run these eight steps for any drafting or restructuring task. Steps 1-3 are planning, 4-6 are drafting, 7-8 are checking.

## 1. Build a one-sentence argument

> In [system/problem], we show [advance] using [approach], supported by [evidence], with [boundary].

Force every section to serve this sentence. If the sentence cannot be written, the paper does not yet have an argument: surface that to the user.

## 2. Choose section architecture

Pick the section structure from the relevant `section/*.md` fragment and, if needed, deeper patterns from `references/article-architecture.md`.

## 3. Map each paragraph to one job

Each paragraph must do exactly one job from: context, gap, approach, result, comparison, mechanism, implication, limitation.

If a paragraph carries two jobs, split it before drafting.

## 4. Draft from evidence outward

Keep claims near the data that support them. Do not stack claims at the top of a section then leave evidence at the bottom.

## 5. Calibrate verbs to evidence strength

`show` / `demonstrate` need strong direct evidence. `suggest` / `indicate` are for trend-level or indirect evidence. `may` / `could` are for plausible but unverified mechanisms.

## 6. Remove unsupported novelty and universal claims

Sweep for `first`, `unique`, `unprecedented`, `comprehensive`, `complete`, `always`, `never`. Replace with bounded claims or delete.

## 7. Run a paragraph-flow check

- One paragraph, one message.
- The first sentence is the topic / claim.
- Each subsequent sentence has an explicit relation to the previous one (cause, comparison, restriction, example).

For full reverse-outlining, open `references/paragraph-flow.md`.

## 8. Return prose plus notes

Output the draft together with explicit notes on assumptions, missing inputs, and where evidence is needed. See `output-format.md`.

## Target-Journal Formatting Rules

When drafting for a named journal, load
`../../../windenergy-submission/references/journal-profiles.md` and apply the
matching slug. Use the rules below as a conservative Elsevier-style default.

### Section numbering

Use numbered sections when the target journal expects numbered sections:
- Top level: 1, 2, 3, ...
- Subsections: 1.1, 1.2, ...
- Sub-subsections: 1.1.1, 1.1.2, ...
- Cross-references use numbers: "as discussed in Section 3.2" (not "as discussed above")
- Abstract is NOT included in section numbering
- Subsection headings appear on separate lines

### Math formulae

- Submit equations as **editable text**, not as images
- Simple formulae inline with normal text where possible
- Use the **solidus (/)** instead of a horizontal line for small fractions (e.g., X/Y)
- Present **variables in italics**
- Powers of e written as **exp(...)** not e^
- **Display equations** numbered consecutively in the order they appear
- Example:

```text
The power coefficient is defined as:

    C_p = P / (0.5 * rho * A * v^3)       (1)

where P is the extracted power (W), rho is the air density (kg/m^3),
A is the rotor swept area (m^2), and v is the wind speed (m/s).
```

### Theory/Calculation section (optional)

Some Elsevier journals allow an optional Theory and Calculation section:
- Theory: extends the background from Introduction
- Calculation: practical development from theoretical basis
- Place after Introduction, before Methods (if used)
