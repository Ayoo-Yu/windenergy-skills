# Method Writing Guide for Renewable Energy Papers

## Goal

Write the Method section clearly: answer design questions, draw a pipeline sketch, then write step by step.

## Pre-Writing Questions

Before writing Method, answer:

1. What modules exist in the method?
2. For each module: workflow, why needed, why it works.

## Method Writing Steps

1. Draw the pipeline figure sketch.
2. Map subsections from the sketch.
3. For each subsection, plan: motivation, module design, technical advantages.
4. Write module design first, then add motivation and advantages.

## Three Elements of a Pipeline Module

### 1) Module Design
- Describe data/network/representation details.
- Describe forward process: input -> steps -> output.

### 2) Motivation
- Why this module is needed (problem-driven).

### 3) Technical Advantages
- Why this module beats alternatives. Tie to measurable behavior.

## Generic Energy Method Architecture

```
\section{Proposed Method}
\subsection{Problem Formulation}
  % Define task, inputs, outputs, decisions, and notation
\subsection{[Module 1: e.g., Input or Scenario Encoding]}
  % Motivation, design, advantage
\subsection{[Module 2: e.g., System, Process, or Temporal Modeling]}
  % Motivation, design, advantage
\subsection{[Module 3: e.g., Spatial, Network, or Constraint Modeling]}
  % Motivation, design, advantage
\subsection{[Module 4: e.g., Output, Decision, or Uncertainty Head]}
  % Motivation, design, advantage
\subsection{Loss Function and Training}
\subsection{Implementation Details}
```

## Problem Formulation Template

```
Given historical observations {y_{t-T+1}, ..., y_t},
exogenous forecasts {x_{t+1}, ..., x_{t+H}}, and optional
auxiliary features {z_{t-T+1}, ..., z_t}, the goal is to predict
target values {y_hat_{t+1}, ..., y_hat_{t+H}} over horizon H.
```

Load topic fragments for asset-specific, system-specific, market-specific, or
control-specific formulations.

## Module Design Writing Template

```
To address [challenge], we propose [module]. Given [input],
we first [step 1] to obtain [intermediate]. Then we [step 2]
to capture [capability]. This produces [output]. Formally,
[equation] where [definitions].
```

## Loss Function Patterns

- **Deterministic**: MSE, MAE, Huber loss
- **Probabilistic**: Pinball/quantile loss, CRPS, negative log-likelihood
- **Multi-task**: L = L_forecast + lambda * L_auxiliary

## Implementation Details Checklist

| Item | Typical content |
|------|----------------|
| Framework | PyTorch / TensorFlow |
| Optimizer | Adam, AdamW |
| Learning rate | 1e-3 to 1e-4 with scheduler |
| Batch size | 32-256 |
| Training epochs | 100-500 with early stopping |
| Hardware | GPU model, training time |
| Data split | train/val/test ratios |
| Scaling or normalization | min-max, z-score, per-unit, or profile-defined scaling |
| Prediction, planning, or control horizon | profile-defined time or scenario range |
| Input or context window | profile-defined lookback or state context |

## Quality Checklist

1. Can a reader reconstruct the method from description alone?
2. Is motivation for each module stated before its design?
3. Are all symbols defined at first use?
4. Are equations numbered and consistent?
5. Is there a clear mapping between method claims and experiments?

## Benchmark and Comparison Study Method Template

Use this template when the paper evaluates, compares, or benchmarks
multiple methods rather than proposing a single new method.

### When to Use This vs Standard Method Template

- Use the **standard method template** (above) when the paper proposes
  one primary method with modules.
- Use this **benchmark template** when the paper evaluates multiple
  methods, conducts a fair comparison, or defines a benchmark protocol.
- If the paper does both (proposes a method AND benchmarks it against
  others), use the standard template for the proposed method and the
  symmetric description for all comparators.

### Section Structure for Benchmark Papers

```text
\section{Methodology}
\subsection{Problem Formulation}
  % Define the task the benchmark studies
\subsection{Evaluation Protocol}
  % Define how methods are compared: data splits, metrics, statistical tests,
  % reproducibility conditions. Include a protocol overview diagram.
\subsection{[Method Family A]}
  % Symmetric description for each method in this family
\subsection{[Method Family B]}
  % Same symmetric description for each method in this family
\subsection{Evaluation and Diagnostic Metrics}
  % Organize in tiers: primary quality, reliability or feasibility diagnostics,
  % paired comparison
\subsection{Implementation Configuration}
  % Hyperparameter table, not inline prose
```

### Protocol Overview

When the method section describes a comparison protocol rather than a
single proposed method, provide a high-level flow BEFORE detailed notation.
Use an algorithm box or flow diagram:

```text
shared input, method signal, method application,
final output, feasibility or validity check, evaluation
```

This gives readers the full picture before they encounter individual
formulas and method details.

### Symmetric Method Description Template

For comparison and benchmark papers, describe each method using the
same subsection structure. Do not give one method a detailed subsection
and others a one-line mention.

For each method, include:

| Element | Content |
|---------|---------|
| Name and source | Full name, citation, variant used |
| Core idea | One-sentence summary of the method's principle |
| Input representation | What features or data it consumes |
| Signal or state source | Where the method's decision signal comes from |
| Update or fixed rule | How the method produces its output |
| Final output construction | How the method output is built |
| Feasibility or validity rule | How physical, operational, or statistical bounds are enforced |
| Key parameters | Parameters relevant to fair comparison |

Apply this template to ALL methods, including the proposed method if
there is one. The proposed method does not get a longer description
by default -- it gets the same template plus a "Design motivation"
paragraph explaining why it was designed differently.

### Tiered Metrics Organization

Organize evaluation metrics into clear tiers so readers understand
what question each metric answers:

| Tier | Question | Example metrics |
|------|----------|----------------|
| Primary quality | How good is the output overall? | Error metric, accuracy metric, score function |
| Reliability or feasibility diagnostics | Does the output satisfy active reliability or constraint requirements? | Reliability diagram, constraint violation rate, feasibility rate |
| Paired comparison | Is one method significantly better? | Paired bootstrap, sign test, effect size |

### Anti-Checklist Guidance

When writing a comparison method section, avoid:

- Opening with a checklist of what will be covered. Start with the method
  problem and protocol structure instead.
- Listing implementation details as a checklist without explaining
  the design rationale for each choice.
- Describing only the proposed method in detail while treating
  baselines as black boxes.
- Omitting the version, configuration, or adaptation applied to
  each baseline.
- Stating "we use the default settings" without specifying what
  those defaults are.
- Presenting the method as a sequence of implementation steps
  ("we first load the data, then we normalize, then we train")
  instead of a principled design.
- Mixing mechanism explanation into method description. Method defines;
  Results reports; Discussion interprets.

### Inter-Chapter Boundary

Method section should only contain method definitions. It should NOT
contain:

- Experimental design defense or justification (Experimental Setup's job)
- Result previews or mechanism explanations (Results/Discussion's job)
- Data characteristics or task selection logic (Experimental Setup's job)
- Literature survey paragraphs (Related Work's job)

If a hyperparameter range, scenario range, or design grid needs justification,
state the design intent briefly. Do not write a paragraph defending the choice.
