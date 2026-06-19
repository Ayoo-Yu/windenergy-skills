# `windenergy-polishing` 技能

windenergy-polishing 是 windenergy-skills 中的一个 Codex skill。

## 功能

润色、缩短、重构、翻译或生成带修订痕迹的风电能源学术文本。

## 适用场景

- 风电功率预测、风电场运行、可再生能源并网、智能电网或 AI for energy 论文工作。
- 需要可复用、可审查、能直接产出文件或文本的科研流程。
- 需要与本仓库其他 windenergy skills 协同完成论文写作、文献、图件、投稿或回复审稿任务。

## 触发词

```text
polish, shorten, tracked changes, 学术润色, manuscript edit
```

## Codex 触发描述

```text
Polish, shorten, restructure, translate, or produce tracked changes for academic prose in wind power, renewable energy, smart grids, energy forecasting, and AI-for-energy manuscripts targeting 18 Elsevier energy, power systems, AI, and pattern-recognition journals. Use when the user asks to improve manuscript paragraphs, abstracts, introductions, results, discussion, conclusions, titles, methods, response text, Chinese drafts, journal-specific style, transfer polishing, or Word .docx tracked edits.
```

## 文件结构

```text
windenergy-polishing/
├── SKILL.md
├── agents/
├── manifest.yaml
├── references/
├── scripts/
├── static/
```

## 使用方式

把整个 `windenergy-polishing` 文件夹安装到 Codex skills 目录后，开启新的 Codex 会话，直接描述任务即可。

示例：

```text
请使用 $windenergy-polishing 帮我处理这篇风电功率预测论文。
```

如果任务依赖共享规则，请同时保留 `skills/_shared/`。
