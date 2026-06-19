# `windenergy-orchestrator` 技能

windenergy-orchestrator 是 windenergy-skills 中的一个 Codex skill。

## 功能

编排从实验材料到投稿包的风电能源论文全流程工作台。

## 适用场景

- 风电功率预测、风电场运行、可再生能源并网、智能电网或 AI for energy 论文工作。
- 需要可复用、可审查、能直接产出文件或文本的科研流程。
- 需要与本仓库其他 windenergy skills 协同完成论文写作、文献、图件、投稿或回复审稿任务。

## 触发词

```text
full paper workflow, manuscript workbench, wind paper pipeline, 投稿包
```

## Codex 触发描述

```text
End-to-end renewable-energy manuscript orchestration for Applied Energy and related journals. Use when the user wants to write a full paper from an experiment folder, run a repeatable benchmark writing workflow, coordinate windenergy-writing, windenergy-academic-search, windenergy-figure, windenergy-citation, windenergy-submission, and windenergy-polishing, or produce a complete LaTeX manuscript package with evidence, citation, and submission audits.
```

## 文件结构

```text
windenergy-orchestrator/
├── SKILL.md
├── agents/
├── examples/
├── references/
├── scripts/
```

## 使用方式

把整个 `windenergy-orchestrator` 文件夹安装到 Codex skills 目录后，开启新的 Codex 会话，直接描述任务即可。

示例：

```text
请使用 $windenergy-orchestrator 帮我处理这篇风电功率预测论文。
```

如果任务依赖共享规则，请同时保留 `skills/_shared/`。
