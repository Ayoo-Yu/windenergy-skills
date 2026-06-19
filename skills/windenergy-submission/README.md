# `windenergy-submission` 技能

windenergy-submission 是 windenergy-skills 中的一个 Codex skill。

## 功能

执行投稿前材料打包、合规审查、返修和转投检查。

## 适用场景

- 风电功率预测、风电场运行、可再生能源并网、智能电网或 AI for energy 论文工作。
- 需要可复用、可审查、能直接产出文件或文本的科研流程。
- 需要与本仓库其他 windenergy skills 协同完成论文写作、文献、图件、投稿或回复审稿任务。

## 触发词

```text
submission audit, cover letter, highlights, 预投稿检查, resubmission
```

## Codex 触发描述

```text
Pre-submission packaging, compliance audit, resubmission, and transfer checks for 18 Elsevier energy, power, AI, and pattern-recognition journals used by wind-power and AI-for-energy manuscripts. Generates or audits Highlights, Cover Letter, CRediT author contributions, generative AI declarations, Declaration of Competing Interests, file packaging, word count, reference count, journal scope, double-anonymized review readiness, and target-journal switch requirements. Use when the user asks to prepare a submission, check readiness, adapt a manuscript to another journal, write submission documents, run a pre-submission checklist, or check scope fit.
```

## 文件结构

```text
windenergy-submission/
├── SKILL.md
├── agents/
├── references/
├── scripts/
├── static/
```

## 使用方式

把整个 `windenergy-submission` 文件夹安装到 Codex skills 目录后，开启新的 Codex 会话，直接描述任务即可。

示例：

```text
请使用 $windenergy-submission 帮我处理这篇风电功率预测论文。
```

如果任务依赖共享规则，请同时保留 `skills/_shared/`。
