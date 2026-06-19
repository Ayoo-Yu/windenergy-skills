# `windenergy-data` 技能

windenergy-data 是 windenergy-skills 中的一个 Codex skill。

## 功能

准备数据可用性声明、数据仓储方案、数据集引用和 FAIR 元数据检查。

## 适用场景

- 风电功率预测、风电场运行、可再生能源并网、智能电网或 AI for energy 论文工作。
- 需要可复用、可审查、能直接产出文件或文本的科研流程。
- 需要与本仓库其他 windenergy skills 协同完成论文写作、文献、图件、投稿或回复审稿任务。

## 触发词

```text
data availability, 数据可用性, FAIR, repository, dataset citation
```

## Codex 触发描述

```text
Prepare, audit, or revise Data Availability statements, data repository plans, dataset citations, software/code availability notes, and FAIR metadata checks for the 18 target Elsevier energy, power, AI, and pattern-recognition journals used by wind-power, renewable-energy integration, and AI-for-energy submissions. Use when the user asks about SCADA data sharing, NWP/reanalysis datasets, repository choice, restricted operator data, dataset DOI citation, code release, or data availability wording.
```

## 文件结构

```text
windenergy-data/
├── SKILL.md
├── agents/
├── references/
```

## 使用方式

把整个 `windenergy-data` 文件夹安装到 Codex skills 目录后，开启新的 Codex 会话，直接描述任务即可。

示例：

```text
请使用 $windenergy-data 帮我处理这篇风电功率预测论文。
```

如果任务依赖共享规则，请同时保留 `skills/_shared/`。
