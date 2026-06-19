# `windenergy-figure` 技能

windenergy-figure 是 windenergy-skills 中的一个 Codex skill。

## 功能

创建、审查或润色风电与 AI for energy 投稿级科研图件。

## 适用场景

- 风电功率预测、风电场运行、可再生能源并网、智能电网或 AI for energy 论文工作。
- 需要可复用、可审查、能直接产出文件或文本的科研流程。
- 需要与本仓库其他 windenergy skills 协同完成论文写作、文献、图件、投稿或回复审稿任务。

## 触发词

```text
wind figure, publication figure, 投稿级图片, power curve, forecast plot
```

## Codex 触发描述

```text
Create, audit, or polish publication-grade figures for renewable energy, wind power, energy forecasting, and AI-for-energy manuscripts in Python or R. Use when the user asks for wind roses, power curves, forecast-vs-actual plots, residual/error distributions, ablation heatmaps, wake/layout diagrams, model comparison charts, graphical abstracts, artwork resolution checks, or Elsevier target-journal figure checks. If the user has not chosen Python or R, ask "Python or R?" before writing plotting code.
```

## 文件结构

```text
windenergy-figure/
├── .gitignore
├── SKILL.md
├── agents/
├── references/
```

## 使用方式

把整个 `windenergy-figure` 文件夹安装到 Codex skills 目录后，开启新的 Codex 会话，直接描述任务即可。

示例：

```text
请使用 $windenergy-figure 帮我处理这篇风电功率预测论文。
```

如果任务依赖共享规则，请同时保留 `skills/_shared/`。
