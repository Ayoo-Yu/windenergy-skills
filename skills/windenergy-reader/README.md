# `windenergy-reader` 技能

windenergy-reader 是 windenergy-skills 中的一个 Codex skill。

## 功能

构建含中英对照、图表定位和来源锚点的风电能源论文 Markdown reader。

## 适用场景

- 风电功率预测、风电场运行、可再生能源并网、智能电网或 AI for energy 论文工作。
- 需要可复用、可审查、能直接产出文件或文本的科研流程。
- 需要与本仓库其他 windenergy skills 协同完成论文写作、文献、图件、投稿或回复审稿任务。

## 触发词

```text
paper reader, 中英对照, full paper markdown, figure-aware reading
```

## Codex 触发描述

```text
Build full-paper Chinese-English side-by-side, figure/table-aware, and source-grounded Markdown readers for journal or conference papers in renewable energy, wind power, smart grids, energy forecasting, and AI-for-energy. Use when the user asks to translate or read a paper, make 中英文对照, 原文对照, 全文翻译解读, extract figures/tables into the right positions, preserve figure/table placement near relevant prose, or keep exact source anchors. Do not degrade into a summary-only output unless the user explicitly asks for a summary.
```

## 文件结构

```text
windenergy-reader/
├── SKILL.md
├── agents/
├── references/
```

## 使用方式

把整个 `windenergy-reader` 文件夹安装到 Codex skills 目录后，开启新的 Codex 会话，直接描述任务即可。

示例：

```text
请使用 $windenergy-reader 帮我处理这篇风电功率预测论文。
```

如果任务依赖共享规则，请同时保留 `skills/_shared/`。
