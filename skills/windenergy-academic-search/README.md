# `windenergy-academic-search` 技能

windenergy-academic-search 是 windenergy-skills 中的一个 Codex skill。

## 功能

检索、筛选和导出风电、可再生能源预测、智能电网和 AI for energy 论文候选文献。

## 适用场景

- 风电功率预测、风电场运行、可再生能源并网、智能电网或 AI for energy 论文工作。
- 需要可复用、可审查、能直接产出文件或文本的科研流程。
- 需要与本仓库其他 windenergy skills 协同完成论文写作、文献、图件、投稿或回复审稿任务。

## 触发词

```text
wind paper search, 查文献, DOI, literature search, AI for energy
```

## Codex 触发描述

```text
Search, discover, screen, deduplicate, and export candidate references for renewable energy, wind power, energy forecasting, and AI-for-energy papers. Uses free academic metadata sources including CrossRef, OpenAlex, Semantic Scholar, and arXiv, plus DOI/arXiv lookup and citation formatting for candidate sources. Use when the user asks to find papers, build literature searches, retrieve candidate metadata, export RIS/BibTeX-style records, or locate sources that may support a claim. For final reference-list audits, in-text citation checks, DOI metadata mismatch checks, or reference cleanup, use `windenergy-citation`.
```

## 文件结构

```text
windenergy-academic-search/
├── SKILL.md
├── agents/
├── config/
├── mcp-server/
├── references/
```

## 使用方式

把整个 `windenergy-academic-search` 文件夹安装到 Codex skills 目录后，开启新的 Codex 会话，直接描述任务即可。

示例：

```text
请使用 $windenergy-academic-search 帮我处理这篇风电功率预测论文。
```

如果任务依赖共享规则，请同时保留 `skills/_shared/`。
