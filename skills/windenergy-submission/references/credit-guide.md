# CRediT Author Contributions Guide

Use this guide for target journals that require or encourage CRediT statements.
Check `journal-profiles.md` first.

## Requirements

- CRediT author contributions statement is **mandatory**
- Corresponding author is responsible for acknowledging co-author contributions
- Uses the standard CRediT role taxonomy
- Placed after Acknowledgements, before References

## Standard CRediT roles

The complete CRediT taxonomy with energy research context:

| Role | Description | Energy research examples |
|------|-------------|------------------------|
| **Conceptualization** | Ideas; formulation of research goals and aims | Identifying the research gap; defining the energy-system decision problem |
| **Data curation** | Management activities for research data | Cleaning measurement data; organizing simulation or market datasets |
| **Formal analysis** | Statistical, mathematical, computational | Running evaluations; computing profile-relevant metrics; performing sensitivity analysis |
| **Funding acquisition** | Financial support for the project | Securing grants; obtaining industry or institutional support |
| **Investigation** | Conducting research and experiments | Running experiments; performing simulations; validating against field or benchmark data |
| **Methodology** | Development or design of methodology | Designing the model, controller, optimization, or analysis workflow |
| **Project administration** | Management and coordination | Coordinating data access, experiments, and research timeline |
| **Resources** | Provision of study materials, equipment | Providing data access, computational resources, equipment, or site access |
| **Software** | Programming, software development | Implementing the model, solver, dashboard, or preprocessing pipeline |
| **Supervision** | Oversight and leadership | Supervising graduate students; guiding research direction |
| **Validation** | Verification of results | Independent verification of results; validation protocol setup |
| **Visualization** | Data presentation, figures | Creating profile-relevant plots, diagrams, maps, or heatmaps |
| **Writing - original draft** | Initial writing | Drafting the manuscript sections |
| **Writing - review and editing** | Critical review, commentary | Revising for clarity; polishing English; addressing reviewer comments |

Not all roles apply to every manuscript. Some authors may contribute through multiple roles.

## Format

Many journals do not set a strict format, but a common structure is:

**Author-first format (recommended):**

```text
Author contributions

Author A: Conceptualization, Methodology, Software, Writing - original draft.
Author B: Data curation, Formal analysis, Validation.
Author C: Supervision, Funding acquisition, Writing - review & editing.
Author D: Resources, Investigation.
Author E: Visualization, Writing - review & editing.
```

**Role-first format (alternative):**

```text
Author contributions

Conceptualization: Author A, Author C.
Data curation: Author B.
Formal analysis: Author B.
Funding acquisition: Author C.
Investigation: Author D.
Methodology: Author A.
Software: Author A.
Supervision: Author C.
Validation: Author B.
Visualization: Author E.
Writing - original draft: Author A.
Writing - review & editing: Author C, Author E.
```

Both formats are acceptable. Choose the one that best represents the team's contributions.

## Writing process

### Step 1. Collect author information

Ask the user for:
- Full names and order of all authors
- Each author's main contributions (in Chinese or English)

### Step 2. Map to CRediT roles

For each author, map their described contributions to standard CRediT roles. Common mapping for Chinese authors:

| Chinese description | CRediT role(s) |
|-------------------|----------------|
| 提出了研究思路 | Conceptualization |
| 处理了数据 | Data curation |
| 做了实验/分析 | Formal analysis, Investigation |
| 写了代码 | Software |
| 设计了方法 | Methodology |
| 提供了数据/资源 | Resources |
| 画了图 | Visualization |
| 写了初稿 | Writing - original draft |
| 修改了论文 | Writing - review & editing |
| 获得了经费 | Funding acquisition |
| 指导了研究 | Supervision |
| 验证了结果 | Validation |

### Step 3. Draft the statement

Use the author-first format by default. Ensure every author appears at least once.

### Step 4. Verify

- [ ] All authors listed
- [ ] Each author has at least one role
- [ ] Only standard CRediT terms used
- [ ] No fabricated contributions
- [ ] Corresponding author identified

## Common issues for Chinese-author teams

### Issue 1: "Everyone did everything"

In some Chinese research groups, contributions are described as equal across all authors. The CRediT statement should still differentiate roles honestly.

### Issue 2: "The supervisor only supervised"

Supervisors often also contribute Conceptualization, Funding acquisition, and Writing - review & editing. Ask the user rather than assuming.

### Issue 3: Author name romanization

Ensure author names in the CRediT statement match the romanization used on the title page. If authors use different name formats (e.g., given-name-first vs. family-name-first), pick one convention and use it consistently.

## QA checklist

- [ ] All manuscript authors included
- [ ] Each author has at least one CRediT role
- [ ] Only standard CRediT taxonomy terms used
- [ ] Names match title page formatting
- [ ] Statement placed after Acknowledgements, before References
- [ ] Corresponding author's roles explicitly stated
