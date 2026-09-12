# 数据库 / 数据集索引（按模态）

> 长期资产，人工维护。weekly digest 会提增补建议，确认后加进来。
> 格式：名字 — 一句话 — 数据类型/规模。

## 转录组 / bulk

- GEO — 最大公共组学仓库 — bulk + 部分单细胞，n=数百万样本
- SRA — 原始测序 reads — 所有物种
- ARCHS4 — GEO RNA-seq 统一重处理矩阵 — 人/鼠，可直接下载 count matrix
- recount3 — 统一重处理 RNA-seq — 人/鼠，含 GTEx/TCGA

## 单细胞

- CELLxGENE — 最大单细胞标准化浏览器 + h5ad 下载 — 人/鼠，n=1 亿+ 细胞
- Human Cell Atlas — 人体全细胞图谱计划 — 多器官
- Tabula Sapiens — 人多器官单细胞参考 — 24 组织 50 万细胞
- scRNA-seq 衰老专属：见 Aging Atlas

## 空间转录组

- HuBMAP — 人体单细胞+空间图谱 — Visium/Slide-seq/MERFISH 等
- SpatialDB / STOmicsDB — 空转数据聚合
- 10x 官方公开数据集 — 质控好，适合 demo

## 蛋白质组

- PRIDE / ProteomeXchange — 质谱原始数据
- Human Protein Atlas (HPA) — 组织/单细胞/亚细胞蛋白表达图谱
- UKB-PPP — UK Biobank Olink 3000 蛋白 — n=5.4 万，衰老蛋白组首选
- SomaScan 队列 — ARIC/CHS 等老队列有 SomaLogic 数据

## 甲基化 / 表观

- EWAS Atlas / EWAS Data Hub — 甲基化关联结果 + 数据
- GEO 450K/EPIC 数据 — 搜 "aging" 大量血样甲基化阵列，时钟训练原料
- ENCODE — ChIP/ATAC/DNase 调控组学

## 衰老专属

- Aging Atlas — 衰老相关基因/多组学聚合
- Open Genes — 衰老基因数据库 + 实验证据分级
- CellAge / GenAge — 细胞衰老/基因衰老 curated 集
- NHANES — 体检+死亡率随访，PhenoAge 类时钟校准标准集
- UK Biobank — 50 万人，组学+影像+结局，需申请
- CKB（中国嘉道理）/ CHARLS（中国老年追踪）— 中国人群，时钟本土化用

## 药物 / 扰动

- LINCS L1000 — 药扰转录组，n=百万级 profile
- DepMap — 癌细胞系 CRISPR 依赖 + 药敏
- Open Targets — 靶点-疾病证据聚合
- Perturb-seq 数据集（scPerturb 聚合）— 单细胞扰动响应

## 多模态整合专用

- TCGA — 肿瘤多模态标杆（RNA+甲基化+CNV+病理+结局）
- 10x Multiome 公共集 — RNA+ATAC 同细胞
