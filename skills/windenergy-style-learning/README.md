# windenergy-style-learning

`windenergy-style-learning` 用于从 ScienceDirect full text 或本地 PDF 语料学习目标期刊风格，并把学习结果转成可复用的写作、润色、审稿和绘图约束。

## 主要能力

1. 构建目标期刊写作 profile，包括 section 顺序、长度、move 结构、引用密度、数字报告、comparison language、caption 和表格模式。
2. 构建视觉图风格 profile，包括图像比例、色彩、ink density、图类型分布和视觉一致性规则。
3. 使用 profile 审计手稿，输出 style gap、严重性分级和 revision targets。
4. 为 `windenergy-writing`、`windenergy-polishing` 和 `windenergy-figure` 提供期刊风格约束。

## 内置 Applied Energy Profile

本技能包含一份可长期复用的 Applied Energy 风电预测方向 profile：

```text
references/profiles/applied-energy-wind-forecasting/
├── main-profile/
└── visual-profile/
```

`main-profile` 基于 69 篇 Applied Energy 风电预测论文，覆盖写作结构、语言模板、数字报告、caption、表格和正文引图模式。

`visual-profile` 基于 30 篇论文的 308 张图，覆盖图像比例、配色、ink density、图类型分布和视觉风格规则。

优先读取这些文件：

```text
references/profiles/applied-energy-wind-forecasting/main-profile/learned_style_digest.md
references/profiles/applied-energy-wind-forecasting/main-profile/style_profile.yaml
references/profiles/applied-energy-wind-forecasting/main-profile/figure_style.yaml
references/profiles/applied-energy-wind-forecasting/visual-profile/visual_figure_style_digest.md
references/profiles/applied-energy-wind-forecasting/visual-profile/visual_figure_style.yaml
```

## 使用边界

这份内置 profile 适用于 Applied Energy 风电预测、风电功率预测、区间预测、校准、风险评估和 AI for wind forecasting 论文。

如果目标主题换成建筑能耗、储能调度、PV-only、综合能源系统或其他 Applied Energy 子方向，应重新使用 topic gate 构建新的 profile。

## 常用命令

从 ScienceDirect XML full text 构建主 profile：

```bash
python scripts/build_style_profile.py --text-dir CORPUS/fulltext --journal "Applied Energy" --topic-profile wind_forecasting --require-topic-match --min-template-doc-support 5 --output PROFILE_DIR
```

学习视觉图风格：

```bash
python scripts/learn_visual_figure_style.py --sciencedirect-manifest CORPUS/corpus_manifest.json --topic-screening-report PROFILE_DIR/topic_screening_report.json --api-key-file PRIVATE_KEY_FILE --max-records 30 --max-figures-per-record 14 --journal "Applied Energy" --source sciencedirect_xml_figure_objects --output VISUAL_PROFILE_DIR
```

审计手稿：

```bash
python scripts/audit_manuscript_style.py --manuscript PAPER.pdf --profile PROFILE_DIR/style_profile.yaml --output AUDIT_DIR
```

