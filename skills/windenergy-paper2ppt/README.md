# `windenergy-paper2ppt` 技能

windenergy-paper2ppt 是 windenergy-skills 中的一个 Codex skill。

## 功能

把风电、可再生能源或 AI for energy 科研论文转换为中文 PPTX 汇报。

## 适用场景

- 风电功率预测、风电场运行、可再生能源并网、智能电网或 AI for energy 论文工作。
- 需要可复用、可审查、能直接产出文件或文本的科研流程。
- 需要与本仓库其他 windenergy skills 协同完成论文写作、文献、图件、投稿或回复审稿任务。

## 触发词

```text
paper to PPT, journal club, 论文汇报, 中文 slides
```

## Codex 触发描述

```text
Build a complete Chinese PPTX presentation from a scientific paper in renewable energy, wind power, energy forecasting, smart grids, or AI-for-energy research. Use when the user asks to make slides, PPT, PPTX, journal-club slides, group-meeting slides, thesis-seminar slides, or academic presentation materials from an energy paper. The expected output is a real .pptx deck, not only an outline.
```

## 文件结构

```text
windenergy-paper2ppt/
├── SKILL.md
├── agents/
```

## 使用方式

把整个 `windenergy-paper2ppt` 文件夹安装到 Codex skills 目录后，开启新的 Codex 会话，直接描述任务即可。

示例：

```text
请使用 $windenergy-paper2ppt 帮我处理这篇风电功率预测论文。
```

如果任务依赖共享规则，请同时保留 `skills/_shared/`。
