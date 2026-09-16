# 代表模型索引（按任务）

> 长期资产，人工维护。格式：名字 — 一句话 — 部署难度（⭐易/⭐⭐中/⭐⭐⭐难）+ 备注。

## 单细胞 foundation model

- scGPT — Transformer 单细胞预训练，支持扰动预测 — ⭐⭐，官方 repo 有 checkpoint
- Geneformer — BERT 式基因 token 预训练 — ⭐⭐，HF 上有权重
- scFoundation — 1 亿细胞预训练，大模型 — ⭐⭐⭐，显存要求高
- UCE (Universal Cell Embedding) — 跨物种细胞 embedding — ⭐⭐
- scVI / scANVI — 经典 VAE 整合/注释基线 — ⭐，scvi-tools 一条命令
- scArches — 参考映射 + 增量整合 — ⭐⭐，跨队列校正常用

## 单细胞工具 / 批次整合

- Harmony — 快速批次整合，PBMC 场景事实标准 — ⭐，R/Python
- BBKNN — 图邻接批次校正 — ⭐，轻量可组合
- SAMap — 跨物种单细胞图谱映射 — ⭐⭐，适合衰老跨物种比较
- CellBender — 单细胞背景去除 — ⭐⭐，提升下游建模质量
- MILO — 差异丰度分析 — ⭐⭐，衰老队列组成变化常用

## 蛋白

- ESM-2 / ESM-3 — Meta 蛋白语言模型 — ⭐⭐，HF 可拉
- AlphaFold2/3 — 结构预测 — ⭐⭐⭐（2 可本地，3 走 server）
- ColabFold — AF2 快速部署版 — ⭐⭐
- ProtGPT2 — 蛋白序列生成 — ⭐⭐，从头设计探索

## 基因组 / 调控序列

- Enformer — 序列→表达/染色质状态 — ⭐⭐，调控建模基线
- Nucleotide Transformer — 跨物种基因组基础模型 — ⭐⭐，多尺度权重开放
- DNABERT-2 — 多物种 DNA 语言模型 — ⭐⭐
- scBasset — 单细胞 ATAC 序列模型 — ⭐⭐，调控元件解析

## Aging clock

- PhenoAge (Levine 2018) — 9 项血检线性模型 — ⭐，本仓库 age_prediction_business/mvp 有实现
- Horvath pan-tissue clock — 甲基化 353 CpG — ⭐⭐，R 包
- GrimAge / DunedinPACE — 死亡率/衰老速度时钟 — ⭐⭐
- 蛋白组时钟：ProtAge (UKB-PPP 系) — ⭐⭐，需 Olink 数据
- ClockBase clock 集合 (Altos) — 多组织 clock 基准 + 可复现实现 — ⭐⭐，方法对比用
- DeepMAge / MethylNet — 甲基化深度学习时钟 — ⭐⭐，可迁移到多模态衰老建模

## Cell painting / 影像

- imAgeScore — Cell Painting + ML 测成纤维细胞衰老（bioRxiv 2026）— 免疫版是空白机会
- DeepProfiler / pycytominer — 形态学 profile 标准工具链 — ⭐⭐

## 空间组学

- Squidpy — 空间组学分析与图建模 — ⭐，空转 pipeline 核心
- Tangram — 单细胞→空间映射 — ⭐⭐，空转注释常用

## 多模态整合

- MOFA+ — 多组因子分析基线 — ⭐
- MultiVI (scvi-tools) — RNA+ATAC VAE 整合 — ⭐⭐
- totalVI — RNA+蛋白 (CITE-seq) — ⭐⭐
- OT/最优传输类（如 scOT 方法）— 跨模态映射新趋势 — ⭐⭐

## 通用 ML / 自监督

- I-JEPA — 自监督表征新范式参考实现 — ⭐⭐，可迁移到组学表征学习

## 持续学习 / 增量（新数据进来矫正模型用）

- EWC / replay buffer 经典方法 — 概念即可，工程上通常直接重训+正则
- LoRA 微调 — 大模型增量适配首选 — ⭐，peft 库
