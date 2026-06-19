# `windenergy-citation` 技能

windenergy-citation 是 windenergy-skills 中的一个 Codex skill。

## 功能

补充、核验、筛选和导出风电 AI 论文引用，并做最终引用完整性审查。

## 适用场景

- 风电功率预测、风电场运行、可再生能源并网、智能电网或 AI for energy 论文工作。
- 需要可复用、可审查、能直接产出文件或文本的科研流程。
- 需要与本仓库其他 windenergy skills 协同完成论文写作、文献、图件、投稿或回复审稿任务。

## 触发词

```text
citation audit, DOI-backed citation, 参考文献, claim support
```

## Codex 触发描述

```text
Add, verify, screen, and export citations for renewable energy, wind power, energy forecasting, smart-grid, and AI-for-energy manuscripts. Use when the user asks for supporting literature, DOI checks, reference-list cleanup, EndNote/RIS/BibTeX export, or claim-by-claim citation suggestions for the 18 target Elsevier energy, power, AI, and pattern-recognition journals, IEEE energy journals, final manuscript citation audits, or similar venues.
```

## 文件结构

```text
windenergy-citation/
├── SKILL.md
├── agents/
├── references/
├── scripts/
```

## 使用方式

把整个 `windenergy-citation` 文件夹安装到 Codex skills 目录后，开启新的 Codex 会话，直接描述任务即可。

示例：

```text
请使用 $windenergy-citation 帮我处理这篇风电功率预测论文。
```

如果任务依赖共享规则，请同时保留 `skills/_shared/`。
