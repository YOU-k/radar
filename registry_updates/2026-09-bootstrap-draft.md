# Registry 大盘点初稿（LLM 起草，人工删改后合并进 registry/）

# 长期知识库 Registry 草案

> 收录标准：经得起时间检验的基础设施（数据库/模型/研究者），非新闻。宁缺勿滥。
> 说明：URL 尽量给到项目主页或稳定入口；若某条你无法确认当前可访问性，建议入库前手动核验一次。

---

## databases.md

- [GEO (Gene Expression Omnibus)](https://www.ncbi.nlm.nih.gov/geo/) — NCBI 旗舰表达谱仓库，覆盖 bulk/单细胞/空转原始与处理数据，免费开放。
- [ArrayExpress / BioStudies](https://www.ebi.ac.uk/biostudies/) — EBI 侧的表达与多组学归档，与 GEO 互补，支持程序化批量下载。
- [Single Cell Portal (Broad)](https://singlecell.broadinstitute.org/) — Broad 托管的单细胞数据集集合，含大量 PBMC/免疫图谱，网页+API 访问。
- [Human Cell Atlas (HCA) Data Portal](https://data.humancellatlas.org/) — 国际人类细胞图谱计划的数据入口，跨组织跨模态，标准化元数据。
- [CELLxGENE (CZI)](https://cellxgene.cziscience.com/) — 单细胞数据标准化浏览与下载平台，schema 统一，适合直接喂模型。
- [Tabula Sapiens](https://tabula-sapiens-portal.ds.czbiohub.org/) — 多器官人类单细胞参考图谱，~50 万细胞，含年龄/组织元数据。
- [Human Protein Atlas](https://www.proteinatlas.org/) — 蛋白/转录本空间分布与单细胞图谱，含组织、细胞、病理多模态。
- [GTEx Portal](https://gtexportal.org/) — 多组织基因型-表达（eQTL）参考队列，衰老/组织特异研究常用基线。
- [UK Biobank](https://www.ukbiobank.ac.uk/) — 50 万人级多模态队列（基因、蛋白组、影像、甲基化子集），需申请访问。
- [dbGaP](https://www.ncbi.nlm.nih.gov/gap/) — NIH 受控访问的基因型-表型数据库，含大量衰老与队列研究。
- [EGA (European Genome-phenome Archive)](https://ega-archive.org/) — 欧洲受控访问的人类组学数据档案，甲基化/基因组/单细胞均有。
- [GEO + ARCHS4](https://maayanlab.cloud/archs4/) — 对 GEO 大规模重处理的统一表达矩阵，适合预训练/迁移。
- [CELLxGENE Census](https://chanzuckerberg.github.io/cellxgene-census/) — 对 CELLxGENE 全库的可查询切片，专为 ML 训练设计。
- [10x Genomics Datasets](https://www.10xgenomics.com/datasets) — 官方单细胞/空转/多组学示例数据，格式规范，适合 pipeline 验证。
- [Spatial Omics / SODB](https://github.com/STOmics/SODB) — 空间组学数据库集合，整合多平台空转数据。
- [STOmicsDB](https://db.cngb.org/stomics/) — 国家基因库空间转录组数据库，含注释与可视化。
- [Aging Atlas](https://ngdc.cncb.ac.cn/aging/index) — 衰老相关多组学整合数据库（转录、甲基化、单细胞等），中文团队维护。
- [GenAge / Human Ageing Genomic Resources](https://genomics.senescence.info/) — 衰老基因、干预、长寿模型的核心人工整理库。
- [ClockBase (Altos Labs)](https://www.clockbase.org/) — 多组织多物种甲基化 aging clock 基准数据与评估平台。
- [Methylation Array / GEO 甲基化子集](https://www.ncbi.nlm.nih.gov/geo/) — Illumina 450K/EPIC 数据主要来源，配合 GEOmetadb 可批量检索。
- [PRIDE / ProteomeXchange](https://www.ebi.ac.uk/pride/) — 蛋白组原始质谱数据主仓库，含大量衰老/血浆蛋白组。
- [MassIVE / ProteomeXchange](https://massive.ucsd.edu/) — 美国侧质谱数据仓库，与 PRIDE 互通。
- [Perturb-seq / scPerturb](https://scperturb.org/) — 单细胞扰动实验数据整合，含 CRISPR 筛选与药物扰动。
- [LINCS L1000 / CLUE](https://clue.io/) — 大规模药物/基因扰动转录组签名库，药物重定位与扰动建模核心资源。
- [Cell Painting Gallery (Broad)](https://registry.opendata.aws/cellpainting-gallery/) — 细胞成像形态学数据集，配合 ML 做表型筛选。

---

## models.md

- [scGPT](https://github.com/bowang-lab/scGPT) — 单细胞 foundation model，Transformer 架构，支持注释/扰动/整合，MIT 许可。
- [Geneformer](https://huggingface.co/ctheodoris/Geneformer) — 基于 GeneRank 的细胞基础模型，适合迁移到下游任务，需申请/开放权重。
- [scFoundation](https://github.com/biomap-research/scFoundation) — 1 亿参数级单细胞基础模型，支持表达重建与药物响应预测。
- [UCE (Universal Cell Embedding)](https://github.com/snap-stanford/UCE) — 跨物种零样本细胞嵌入，无需微调即可用，权重开放。
- [scVI / scArches](https://docs.scvi-tools.org/) — 概率单细胞整合与参考映射框架，跨队列校正与增量学习常用。
- [Harmony](https://github.com/immunogenomics/harmony) — 快速批次整合方法，PBMC 场景事实标准之一，R/Python 均有。
- [BBKNN](https://github.com/Teichlab/bbknn) — 基于图邻接的批次校正，轻量、可组合。
- [SAMap](https://github.com/atarashansky/SAMap) — 跨物种单细胞图谱映射，适合衰老跨物种比较。
- [ESM-2 / ESMFold](https://github.com/facebookresearch/esm) — 蛋白语言模型与结构预测，权重开放，可微调。
- [AlphaFold2 / ColabFold](https://github.com/sokrypton/ColabFold) — 蛋白结构预测事实标准，ColabFold 便于快速部署。
- [ESM-IF / ESM-3](https://github.com/evolutionaryscale/esm) — 新一代蛋白语言模型，含结构/功能条件生成。
- [ProtGPT2](https://huggingface.co/nferruz/ProtGPT2) — 蛋白序列生成语言模型，适合从头设计探索。
- [DNABERT-2](https://github.com/MAGICS-LAB/DNABERT_2) — 多物种 DNA 语言模型，基因组序列表征。
- [Nucleotide Transformer](https://github.com/instadeepai/nucleotide-transformer) — 跨物种基因组基础模型，含多尺度权重。
- [Enformer](https://github.com/google-deepmind/enformer) — 从序列预测基因表达/染色质状态，调控建模基线。
- [scBasset](https://github.com/calico/scBasset) — 单细胞 ATAC 序列模型，调控元件解析。
- [Aging clocks: Horvath / Hannum / PhenoAge / GrimAge](https://github.com/EpigeneticClock) — 甲基化 aging clock 经典实现，多语言重实现广泛。
- [Altos ClockBase 上的 clock 集合](https://www.clockbase.org/) — 多组织 clock 基准与可复现实现，适合做方法对比。
- [DeepMAge / MethylNet](https://github.com/ChristinaGao/MethylNet) — 甲基化深度学习方法，可迁移到多模态衰老建模。
- [MOFA+](https://biofam.github.io/MOFA2/) — 多组学因子分析，缺失模态与跨队列整合常用，R/Python。
- [MultiVI / totalVI](https://docs.scvi-tools.org/) — 多模态单细胞整合（RNA+ATAC / RNA+蛋白），处理缺失模态。
- [MILO / MIRA](https://github.com/calico/milo) — 单细胞差异丰度与调控建模，衰老队列分析常用。
- [CellBender](https://github.com/broadinstitute/CellBender) — 单细胞背景去除，提升下游建模质量。
- [Squidpy](https://squidpy.readthedocs.io/) — 空间组学分析与图建模工具，空转 pipeline 核心。
- [Tangram](https://github.com/broadinstitute/Tangram) — 单细胞到空间映射，空转注释与整合常用。
- [JEPA / I-JEPA 参考实现](https://github.com/facebookresearch/ijepa) — 自监督表征新范式，可迁移到组学表征学习。

---

## people.md

- Fabian Theis（Helmholtz Munich）— 单细胞方法学、scVI/scArches、多模态整合。
- Aviv Regev（Genentech / Broad）— 单细胞图谱、Human Cell Atlas、扰动建模。
- Sarah Teichmann（Cambridge / Sanger）— 免疫单细胞、HCA、跨组织图谱。
- Dana Pe'er（MSKCC）— 单细胞计算、肿瘤异质性与扰动响应。
- Nir Yosef（UC Berkeley）— 单细胞建模、Perturb-seq 分析、免疫组学。
- Alex Wolf（CZI）— Scanpy/AnnData 生态、单细胞基础设施。
- Lior Pachter（Caltech）— 转录组定量、单细胞统计方法。
- Cole Trapnell（UW）— 单细胞轨迹、Monocle、扰动实验。
- Steve Horvath（Altos Labs）— 甲基化 aging clock 奠基人。
- Morgan Levine（Altos Labs / Yale）— PhenoAge、衰老表观遗传建模。
- Vadim Gladyshev（Harvard）— 衰老组学、跨物种比较。
- Tony Wyss-Coray（Stanford）— 血浆蛋白组与衰老、脑衰老。
- Anne Brunet（Stanford）— 衰老表观遗传与单细胞。
- Manolis Kellis（MIT）— 基因组调控、衰老与表观遗传。
- Emma Lundberg（KTH / Stanford）— 空间蛋白组、Cell Painting、Human Protein Atlas。
- Anne Carpenter（Broad）— Cell Painting、形态学 profiling、影像 ML。
- Bo Wang（Toronto）— scGPT、单细胞基础模型。
- Christina Theodoris（Gladstone / UCSF）— Geneformer、网络医学。
- Anshul Kundaje（Stanford）— 序列到功能模型、Enformer 相关。
- Sergey Ovchinnikov（MIT）— 蛋白语言模型与结构预测方法。

---

需要的话，我可以再补一份 `methods.md`（多模态对齐、缺失模态、持续学习的方法学清单），或把每条的许可/访问限制标注得更细。
