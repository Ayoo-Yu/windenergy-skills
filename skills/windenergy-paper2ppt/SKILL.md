---
name: windenergy-paper2ppt
description: >-
  Build a complete Chinese PPTX presentation from a scientific paper in
  renewable energy, wind power, energy forecasting, smart grids, or AI-for-energy
  research. Use when the user asks to make slides, PPT, PPTX, journal-club
  slides, group-meeting slides, thesis-seminar slides, or academic presentation
  materials from an energy paper. The expected output is a real .pptx deck, not
  only an outline.
---

# Renewable Paper to PPT

Transform a paper or paper-derived notes into a Chinese, figure-integrated PPTX
for academic sharing.

Before writing generated files, load `../_shared/core/output-run-folders.md`
and create a run folder for this invocation. Put the `.pptx`, extracted media,
slide outline, QA report, and intermediate files in that run folder.

## Scope

Use this skill for:

- wind power forecasting and resource assessment
- solar energy prediction and optimization
- renewable integration and grid stability
- AI/ML applications in energy systems
- turbine performance and condition monitoring
- wake modelling and wind-farm layout optimization
- storage, hybrid systems, smart grids, and demand response
- reviews and perspectives on renewable energy topics

## Core Principle

Use the paper's scientific argument as the presentation spine:

1. Why does the problem matter?
2. What gap or bottleneck does the paper address?
3. What did the authors do?
4. What is the key evidence?
5. Why should we trust the result?
6. What is reusable or broadly meaningful?
7. Where are the boundaries and open questions?

## Workflow

1. Extract title, authors, venue, year, DOI, problem, gap, method, data, figures,
   results, limitations, and implications.
2. Classify the paper: forecasting, method, resource assessment, condition
   monitoring, wake/layout, integration, benchmark, or review.
3. Select only figures/tables that carry evidence.
4. Build a 12-16 slide Chinese deck by default.
5. Use python-pptx or the available presentation tooling to create the actual
   `.pptx`.
6. Reopen or inspect the deck and fix overflow, missing media, or unreadable
   figures.
7. Provide a short QA report with remaining risks and the run folder path.

## Default Slide Plan

1. 标题页
2. 研究背景
3. 技术瓶颈
4. 核心问题与贡献
5. 方法框架
6. 数据与实验设计
7. 关键证据 1
8. 关键证据 2
9. 关键证据 3
10. 稳健性或消融验证
11. 创新点与可复用价值
12. 局限性与开放问题
13. 总结与讨论

## Design Rules

- Default language is simplified Chinese; preserve model names, datasets,
  metrics, equations, and technical abbreviations in English where appropriate.
- Use conclusion-style slide titles.
- Keep slide text short and figure-led.
- Do not invent results, methods, numbers, citations, or figure details.
- Keep source labels for figure slides.
