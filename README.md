# windenergy-skills

`windenergy-skills` 是一套面向风电、可再生能源、智能电网和 AI for energy 科研工作流的 Codex skills。它围绕论文写作、文献检索、引用核验、投稿图件、数据声明、审稿回复、预投稿审查和完整论文编排组织。

## 安装

`windenergy-skills` 使用与 Codex skills 兼容的目录结构。每个 `skills/windenergy-*` 目录都是一个可安装单元，`skills/_shared/` 存放共享规则和验证脚本。

### Codex 推荐安装方式

把仓库链接交给 Codex，并让它安装完整技能目录：

```text
https://github.com/Ayoo-Yu/windenergy-skills.git
```

推荐提示词：

```text
请从这个仓库安装 Codex skills：
https://github.com/Ayoo-Yu/windenergy-skills.git

请把 skills/ 下的完整技能文件夹安装到我的 Codex skills 目录中，包括 skills/_shared。
不要只复制 SKILL.md。
```

如果只安装单个技能，请明确说明技能名：

```text
只安装这个仓库里的 windenergy-writing：
https://github.com/Ayoo-Yu/windenergy-skills.git

如果该技能需要共享文件，也请一并安装 skills/_shared。
```

关键规则：保留完整目录结构。许多技能依赖 `references/`、`static/`、`manifest.yaml`、脚本、资产或 `skills/_shared/`。

### 手动安装

Linux 或 macOS：

```bash
git clone https://github.com/Ayoo-Yu/windenergy-skills.git
cd windenergy-skills
scripts/update-codex-skills.sh
```

Windows PowerShell：

```powershell
git clone https://github.com/Ayoo-Yu/windenergy-skills.git
cd windenergy-skills
.\scripts\update-codex-skills.ps1
```

安装后开启新的 Codex 会话，然后自然描述任务，例如：

```text
帮我把这篇风电功率预测论文做成中英文对照 Markdown reader。
```

```text
根据这些实验结果起草一篇风电预测论文的 introduction 和 results。
```

```text
帮我检查这篇风电 AI 论文的投稿材料和引用完整性。
```

## 目录结构

```text
skills/
├── _shared/
└── windenergy-<topic>/
    ├── README.md
    ├── SKILL.md
    ├── manifest.yaml
    ├── references/
    ├── scripts/
    └── static/
```

## 技能索引

| 技能 | 状态 | 用途 | 触发词 |
|---|---|---|---|
| [`windenergy-academic-search`](skills/windenergy-academic-search/README.md) | Beta | 检索、筛选和导出风电、可再生能源预测、智能电网和 AI for energy 论文候选文献。 | wind paper search, 查文献, DOI, literature search, AI for energy |
| [`windenergy-citation`](skills/windenergy-citation/README.md) | Beta | 补充、核验、筛选和导出风电 AI 论文引用，并做最终引用完整性审查。 | citation audit, DOI-backed citation, 参考文献, claim support |
| [`windenergy-data`](skills/windenergy-data/README.md) | Beta | 准备数据可用性声明、数据仓储方案、数据集引用和 FAIR 元数据检查。 | data availability, 数据可用性, FAIR, repository, dataset citation |
| [`windenergy-figure`](skills/windenergy-figure/README.md) | Beta | 创建、审查或润色风电与 AI for energy 投稿级科研图件。 | wind figure, publication figure, 投稿级图片, power curve, forecast plot |
| [`windenergy-orchestrator`](skills/windenergy-orchestrator/README.md) | Beta | 编排从实验材料到投稿包的风电能源论文全流程工作台。 | full paper workflow, manuscript workbench, wind paper pipeline, 投稿包 |
| [`windenergy-paper2ppt`](skills/windenergy-paper2ppt/README.md) | Beta | 把风电、可再生能源或 AI for energy 科研论文转换为中文 PPTX 汇报。 | paper to PPT, journal club, 论文汇报, 中文 slides |
| [`windenergy-polishing`](skills/windenergy-polishing/README.md) | Stable | 润色、缩短、重构、翻译或生成带修订痕迹的风电能源学术文本。 | polish, shorten, tracked changes, 学术润色, manuscript edit |
| [`windenergy-reader`](skills/windenergy-reader/README.md) | Beta | 构建含中英对照、图表定位和来源锚点的风电能源论文 Markdown reader。 | paper reader, 中英对照, full paper markdown, figure-aware reading |
| [`windenergy-response`](skills/windenergy-response/README.md) | Beta | 起草、审查和修改风电能源论文逐点回复审稿人信件。 | response letter, reviewer comments, rebuttal, 审稿意见回复 |
| [`windenergy-reviewer`](skills/windenergy-reviewer/README.md) | Draft | 从能源期刊审稿人视角模拟投稿前评审，输出三份 reviewer reports 和作者行动清单。 | pre-submission review, reviewer report, 投稿前评审, 审稿人视角 |
| [`windenergy-style-learning`](skills/windenergy-style-learning/README.md) | Beta | 学习 Applied Energy 等目标期刊风格，生成可复用写作、caption、图表和视觉风格 profile。 | style learning, Applied Energy profile, 期刊风格学习, figure style |
| [`windenergy-submission`](skills/windenergy-submission/README.md) | Beta | 执行投稿前材料打包、合规审查、返修和转投检查。 | submission audit, cover letter, highlights, 预投稿检查, resubmission |
| [`windenergy-writing`](skills/windenergy-writing/README.md) | Stable | 根据 claims、结果、图表、笔记或中文草稿起草风电能源论文各章节。 | write introduction, manuscript draft, 摘要, 引言, 讨论, paper writing |

## 技能概览

### `windenergy-academic-search`

检索、筛选和导出风电、可再生能源预测、智能电网和 AI for energy 论文候选文献。

详见 [`skills/windenergy-academic-search/README.md`](skills/windenergy-academic-search/README.md)。

### `windenergy-citation`

补充、核验、筛选和导出风电 AI 论文引用，并做最终引用完整性审查。

详见 [`skills/windenergy-citation/README.md`](skills/windenergy-citation/README.md)。

### `windenergy-data`

准备数据可用性声明、数据仓储方案、数据集引用和 FAIR 元数据检查。

详见 [`skills/windenergy-data/README.md`](skills/windenergy-data/README.md)。

### `windenergy-figure`

创建、审查或润色风电与 AI for energy 投稿级科研图件。

详见 [`skills/windenergy-figure/README.md`](skills/windenergy-figure/README.md)。

### `windenergy-orchestrator`

编排从实验材料到投稿包的风电能源论文全流程工作台。

详见 [`skills/windenergy-orchestrator/README.md`](skills/windenergy-orchestrator/README.md)。

### `windenergy-paper2ppt`

把风电、可再生能源或 AI for energy 科研论文转换为中文 PPTX 汇报。

详见 [`skills/windenergy-paper2ppt/README.md`](skills/windenergy-paper2ppt/README.md)。

### `windenergy-polishing`

润色、缩短、重构、翻译或生成带修订痕迹的风电能源学术文本。

详见 [`skills/windenergy-polishing/README.md`](skills/windenergy-polishing/README.md)。

### `windenergy-reader`

构建含中英对照、图表定位和来源锚点的风电能源论文 Markdown reader。

详见 [`skills/windenergy-reader/README.md`](skills/windenergy-reader/README.md)。

### `windenergy-response`

起草、审查和修改风电能源论文逐点回复审稿人信件。

详见 [`skills/windenergy-response/README.md`](skills/windenergy-response/README.md)。

### `windenergy-reviewer`

从能源期刊审稿人视角模拟投稿前评审，输出三份 reviewer reports、交叉综合意见和作者行动清单。

详见 [`skills/windenergy-reviewer/README.md`](skills/windenergy-reviewer/README.md)。

### `windenergy-style-learning`

学习 Applied Energy 等目标期刊风格，生成可复用写作、caption、图表和视觉风格 profile。

详见 [`skills/windenergy-style-learning/README.md`](skills/windenergy-style-learning/README.md)。

### `windenergy-submission`

执行投稿前材料打包、合规审查、返修和转投检查。

详见 [`skills/windenergy-submission/README.md`](skills/windenergy-submission/README.md)。

### `windenergy-writing`

根据 claims、结果、图表、笔记或中文草稿起草风电能源论文各章节。

详见 [`skills/windenergy-writing/README.md`](skills/windenergy-writing/README.md)。

## 共享设计原则

1. 证据优先：不要编造数据、机制、指标、样本量、引用或投稿要求。
2. 来源可追踪：论文写作、引用、图件和回复审稿都要能追溯到用户提供材料、正式文献或明确的本地来源。
3. 输出可直接使用：优先生成 `.tex`、`.docx`、`.pptx`、`.svg`、`.bib`、Markdown 报告或可粘贴文本。
4. 保留目录结构：安装时复制完整 skill 文件夹和 `skills/_shared/`。
5. 面向风电能源场景：默认覆盖风电功率预测、预测区间、并网调度、储能、SCADA、NWP、智能电网和 AI for energy 论文。

## 新增技能

向本仓库添加技能时，请按以下流程：

### 1. 创建目录

```text
skills/windenergy-<topic>/
```

### 2. 最低文件要求

| 文件 | 是否必需 | 用途 |
|---|---|---|
| `SKILL.md` | 必需 | frontmatter 与触发后的执行规则 |
| `README.md` | 必需 | 面向人的中文说明文档 |
| `references/*.md` | 复杂技能推荐 | 模块化规则文件 |
| `scripts/*` | 按需 | 可重复执行的确定性脚本 |
| `manifest.yaml` | 按需 | router-style skill 的入口配置 |

### 3. `SKILL.md` frontmatter 模板

```yaml
---
name: windenergy-<topic>
description: >-
  用一句话说明这个技能做什么、什么时候触发、主要输出格式和核心使用场景。
---
```

### 4. 更新技能索引

在上方技能索引表格中添加一行：

```markdown
| [`windenergy-<topic>`](skills/windenergy-<topic>/README.md) | Draft | 一句话用途 | 触发词 |
```

### 5. 状态标签

| 标签 | 含义 |
|---|---|
| `Draft` | 规则已定义，仍需更多真实案例验证 |
| `Beta` | 已在示例或局部真实任务上测试，仍可能存在边界问题 |
| `Stable` | 已在真实学术内容上验证，规则相对稳定 |

## License

Apache-2.0
