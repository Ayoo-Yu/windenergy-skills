# `windenergy-response` 技能

windenergy-response 是 windenergy-skills 中的一个 Codex skill。

## 功能

起草、审查和修改风电能源论文逐点回复审稿人信件。

## 适用场景

- 风电功率预测、风电场运行、可再生能源并网、智能电网或 AI for energy 论文工作。
- 需要可复用、可审查、能直接产出文件或文本的科研流程。
- 需要与本仓库其他 windenergy skills 协同完成论文写作、文献、图件、投稿或回复审稿任务。

## 触发词

```text
response letter, reviewer comments, rebuttal, 审稿意见回复
```

## Codex 触发描述

```text
Draft, audit, or revise point-by-point reviewer response letters for the 18 target energy, power-system, AI, and pattern-recognition journals used by wind-power and AI-for-energy manuscripts, including Renewable Energy, Applied Energy, Energy, Energy Conversion and Management, Energy Reports, Energy and AI, IJEPES, EPSR, SETA, SEGAN, Applied Soft Computing, Information Sciences, Neurocomputing, Knowledge-Based Systems, Pattern Recognition, Engineering Applications of Artificial Intelligence, Expert Systems with Applications, and Computers and Electrical Engineering. Use when the user provides reviewer comments, editor decision letters, revision notes, response drafts, rebuttal letters, response to reviewers, peer-review reports, council-review requests, multi-expert reviewer analysis, revision direction summaries, major revision, minor revision, rejection resubmission, 审稿意见回复, 逐点回复, 审稿意见评价, 多专家分析, 修改方向总结, 大修, 小修, 拒稿转投, 修回信, or 如何回复 reviewer.
```

## 文件结构

```text
windenergy-response/
├── SKILL.md
├── agents/
├── examples/
├── references/
├── reviewer_patterns/
```

## 使用方式

把整个 `windenergy-response` 文件夹安装到 Codex skills 目录后，开启新的 Codex 会话，直接描述任务即可。

示例：

```text
请使用 $windenergy-response 帮我处理这篇风电功率预测论文。
```

如果任务依赖共享规则，请同时保留 `skills/_shared/`。
