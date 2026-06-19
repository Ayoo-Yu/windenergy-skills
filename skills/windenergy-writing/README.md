# `windenergy-writing` 技能

windenergy-writing 是 windenergy-skills 中的一个 Codex skill。

## 功能

根据 claims、结果、图表、笔记或中文草稿起草风电能源论文各章节。

## 适用场景

- 风电功率预测、风电场运行、可再生能源并网、智能电网或 AI for energy 论文工作。
- 需要可复用、可审查、能直接产出文件或文本的科研流程。
- 需要与本仓库其他 windenergy skills 协同完成论文写作、文献、图件、投稿或回复审稿任务。

## 触发词

```text
write introduction, manuscript draft, 摘要, 引言, 讨论, paper writing
```

## Codex 触发描述

```text
Draft, restructure, or plan manuscript sections from author-provided claims, results, figures, notes, or Chinese drafts for wind power, renewable energy, smart grids, energy forecasting, and AI-for-energy papers targeting 18 Elsevier energy, power systems, AI, and pattern-recognition journals. Use when the user wants to write or rebuild an abstract, introduction, related work, method, experiments, discussion, conclusion, title, highlights, keywords, cover-letter draft, or full manuscript argument with journal-aware constraints.
```

## 文件结构

```text
windenergy-writing/
├── SKILL.md
├── agents/
├── manifest.yaml
├── references/
├── static/
```

## 使用方式

把整个 `windenergy-writing` 文件夹安装到 Codex skills 目录后，开启新的 Codex 会话，直接描述任务即可。

示例：

```text
请使用 $windenergy-writing 帮我处理这篇风电功率预测论文。
```

如果任务依赖共享规则，请同时保留 `skills/_shared/`。
