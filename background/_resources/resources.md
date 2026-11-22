# 资源登记（数据集 / 模型 / 基准）

从 714 处证据引用中挖出资源，并入人工种子与日报新发现，共 542 项；主表 153 项（种子/置顶，或被 ≥2 篇工作使用、或跨方向、或开放且链接核验通过且规模明确），日报新发现 22 项（未核验），其余 367 项单篇提及的列在末尾。开放：yes 公开 / partial 部分 / registration 注册 / controlled 受控 / commercial 商业 / unknown 未确认。核验：ok 内容匹配 / mismatch 页面不是该资源 / blocked 站点拒绝探测 / dead 失效 / n/a 非链接。规模带 * 的取自单篇引用文献。更新 2026-11-22


## P0 优先上手（25）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **UK Biobank** | 数据集 | #衰老 #人群队列 | 约 50 万人（40–69 岁入组，2006–10） | [链接](https://www.ukbiobank.ac.uk/) | controlled | 97 | 多组学衰老与CVD方法迁移主数据源，ChinaHEART参照基准 |
| **UK Biobank Pharma Proteomics Project** | 数据集 | #衰老 #人群队列 | 约 5.4 万人 · 约 2,900 蛋白 | [链接](https://www.ukbiobank.ac.uk/) | controlled | 6 | UKB蛋白组，ChinaHEART蛋白组CVD风险迁移参照 |
| **Tahoe-100M** | 数据集 | #单细胞 #虚拟细胞 | 1亿+细胞/50细胞系/379化合物* | [链接](https://huggingface.co/datasets/tahoebio/Tahoe-100M) | yes | 4 | 亿级药物扰动图谱，虚拟扰动预训练与类器官demo核心数据 |
| **China Kadoorie Biobank** | 数据集 | #衰老 #人群队列 | 约 51 万成人（10 个地区，2004–08 入组） | [链接](https://www.ckbiobank.org/) | controlled | 3 | 中国人群参照队列，ChinaHEART 迁移时的对照 |
| **Norman 2019 Perturb-seq** | 数据集 | #单细胞 #虚拟细胞 | Perturb-seq扰动数据集* |  | unknown | 3 | 组合扰动基准数据，虚拟扰动响应建模必用基线 |
| **UK Biobank Olink Plasma Proteomics** | 数据集 | #人群队列 | 约5.4万人/2923蛋白* | [链接](https://www.ukbiobank.ac.uk/) | unknown | 3 | pQTL与蛋白关联参照，ChinaHEART蛋白组迁移必对标 |
| **Replogle 2022 Perturb-seq** | 数据集 | #虚拟细胞 | >250万人类细胞* | doi:10.1016/j.cell.2022.05.013 | unknown | 2 | 基因组规模Perturb-seq，扰动预测建模与基准评估核心数据 |
| **ChinaHEART** | 数据集 | #人群队列 | 中国大规模心血管病筛查/早筛队列 |  | controlled | 0 | 目标队列：UKB 等公共队列方法迁移的落点 |
| **scGPT** | 模型 | #类器官 #单细胞 #虚拟细胞 | 单细胞基础模型（预训练）* | [链接](https://github.com/bowang-lab/scGPT) | yes | 18 | 单细胞基础模型基线，类器官衰老demo与虚拟扰动对标 |
| **Geneformer** | 模型 | #衰老 #单细胞 #虚拟细胞 | 单细胞基础模型（预训练）* | [链接](https://huggingface.co/ctheodoris/Geneformer) | yes | 13 | 单细胞基础模型基线，类器官衰老demo与虚拟扰动建模直接对标 |
| **scFoundation** | 模型 | #单细胞 #虚拟细胞 | 单细胞基础模型（预训练）* | [链接](https://github.com/biomap-research/scFoundation) | yes | 7 | 扰动预测基准模型，类器官扰动demo可直接部署对比 |
| **Tahoe-X1** | 模型 | #单细胞 #虚拟细胞 | 1.3B 参数* | HuggingFace (tahoebio/Tahoe-X1) | unknown | 3 | 扰动训练单细胞基础模型，虚拟扰动响应建模首选基线 |
| **Chreode** | 模型 | #单细胞 #虚拟细胞 | 240万细胞小鼠胚胎图谱预训练* |  | unknown | 2 | 细胞世界模型，虚拟扰动响应与类器官时序建模直接参照 |
| **SCALE** | 模型 | #单细胞 #虚拟细胞 | CRISPR/化学/发育/免疫扰动* | arXiv:2603.17380v3 | unknown | 1 | 条件传输虚拟扰动模型，类器官扰动响应建模直接可用 |
| **ALADYNOULLI** | 模型 | #人群队列 | 68.3万人/348种疾病* |  | unknown | 1 | 生成式疾病轨迹的对标基线（可解释） |
| **Delphi-2M** | 模型 | #人群队列 | UKB 约 40 万人训练 + 丹麦 190 万人验证 · 1000+ 病种 |  | unknown | 1 | 生成式疾病轨迹的对标基线 |
| **China-PAR** | 模型 |  |  | [链接](https://doi.org/10.1161/CIRCULATIONAHA.116.022367) | yes | 0 | 中国人群传统评分基线，ChinaHEART 模型必须对标 |
| **DunedinPACE** | 模型 | #衰老 |  | [链接](https://github.com/danbelsky/DunedinPACE) | yes | 0 | 甲基化衰老速度时钟，类器官衰老 demo 与队列衰老建模必对标基线 |
| **Horvath clock** | 模型 | #衰老 | 353 CpG |  | yes | 0 | 多组织甲基化年龄时钟，衰老建模标准基线，可直接部署 |
| **Pooled Cohort Equations** | 模型 |  |  |  | yes | 0 | 心血管风险预测的传统评分基线 |
| **LongevityBench** | 基准 | #衰老 | 17项任务/5个数据域* | [链接](https://doi.org/10.1016/j.cell.2026.08.026) | unknown | 2 | 衰老 AI 基准（Cell 2026），模型评测对标 |
| **Virtual Cell Challenge** | 基准 | #单细胞 #虚拟细胞 | 专用扰动数据集（细节未公开）* | [链接](https://doi.org/10.1016/j.cell.2025.06.008) | unknown | 1 | 虚拟扰动响应基准，类器官/细胞虚拟扰动建模直接对标 |
| **CELLxGENE** | 数据库 | #衰老 #单细胞 | 超7000万细胞* | [链接](https://cellxgene.cziscience.com/) | yes | 1 | 单细胞图谱，训练类器官/单细胞衰老时钟的公开数据 |
| **scPerturb** | 数据库 | #虚拟细胞 |  |  | yes | 0 | 单细胞扰动聚合库，虚拟扰动响应建模直接可用的训练数据 |
| **Cell Painting** | 工具 | #衰老 #单细胞 | 多批次高内涵图像* |  | unknown | 2 | 细胞形态扰动响应，类器官+cell painting扰动建模核心 |

## P1 值得登记（61）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **All of Us Research Program** | 数据集 | #人群队列 | 目标 100 万人（美国，多族裔） | [链接](https://www.researchallofus.org/) | controlled | 15 | 多血统EHR+基因组，PRS与EHR关联复制方法参照 |
| **UK Biobank Exome Sequencing Dataset** | 数据集 | #人群队列 | 约45.5万人/1230万变异* | [链接](https://www.ukbiobank.ac.uk/) | unknown | 3 | 罕见变异负荷分析参照，人群多组学遗传整合 |
| **ARIC** | 数据集 | #人群队列 | 约 1.6 万人（1987–89 入组） | [链接](https://aric.cscc.unc.edu) | controlled | 2 | 蛋白组心衰/衰弱队列，ChinaHEART蛋白组参照 |
| **Global Biobank Meta-analysis Initiative (GBMI)** | 数据集 | #人群队列 | 23库，220万人，14终点* | [链接](https://www.globalbiobankmeta.org/) | unknown | 2 | 跨库荟萃资源，跨祖源PRS评估方法参照 |
| **NMR Metabolomics** | 数据集 | #人群队列 | 250个代谢标志物* |  | unknown | 2 | NMR 代谢组标志物可作 ChinaHEART 迁移的器官衰老时钟参照 |
| **SpeciesCorpus** | 数据集 | #类器官 #单细胞 #虚拟细胞 | 1.31亿细胞* |  | unknown | 1 | 跨物种单细胞语料，可预训练虚拟细胞模型支撑类器官与扰动。 |
| **BBBC021** | 数据集 | #单细胞 #虚拟细胞 | 63,781训练+5,120测试图像* | BBBC021 | unknown | 1 | 扰动图像基准，虚拟扰动建模评测参照 |
| **JUMP** | 数据集 | #单细胞 #虚拟细胞 | 大规模化合物扰动图像* | JUMP | unknown | 1 | 细胞形态扰动基准，类器官成像扰动评测 |
| **Framingham Heart Study** | 数据集 | #衰老 | 社区队列（规模未明确）* | [链接](https://www.framinghamheartstudy.org/) | controlled | 1 | ECG-AF深度学习经典队列，心血管AI模型对标 |
| **LINCS L1000** | 数据集 | #衰老 #虚拟细胞 | 大规模化学/遗传扰动* | [链接](https://clue.io/) | registration | 1 | 扰动转录组，虚拟扰动响应建模训练数据 |
| **MESA** | 数据集 | #人群队列 | 6,814 人（45–84 岁，四个族裔） | [链接](https://www.mesa-nhlbi.org/) | controlled | 1 | 多模态CVD队列，心血管基础模型外部验证 |
| **NHANES** | 数据集 | #衰老 #人群队列 | 每两年约 1 万人（美国代表性样本） | [链接](https://www.cdc.gov/nchs/nhanes/) | yes | 1 | 外部验证衰老时钟对死亡风险捕捉，可作ChinaHEART迁移参照 |
| **Pan-UK Biobank** | 数据集 | #人群队列 | 7,271表型，多祖源* | [链接](https://pan.ukbb.broadinstitute.org/) | yes | 1 | 多祖源 GWAS 汇总，ChinaHEART 遗传整合与跨队列校正参照 |
| **pansci-mouse-aging-snrna** | 数据集 | #衰老 | 2031万细胞核/93小鼠* | [链接](https://huggingface.co/datasets/transhumanist-already-exists/pansci-mouse-aging-snrna) | yes | 1 | 跨器官小鼠衰老单核图谱，可作衰老模型与虚拟扰动参照 |
| **Tabula Sapiens** | 数据集 | #单细胞 | 564,253 细胞* | CZ CELLxGENE / Tabula Sapiens 门户 | unknown | 1 | 多供体单细胞图谱，可作类器官与虚拟细胞表征基准。 |
| **Cell Painting Gallery** | 数据集 | #类器官 |  | [链接](https://github.com/broadinstitute/cellpainting-gallery) | yes | 0 | 细胞成像形态学数据，cell painting+ML 与类器官表型建模参照 |
| **CHARLS** | 数据集 | #人群队列 #衰老 |  | [链接](https://charls.pku.edu.cn/) | registration | 0 | 中国中老年队列，可作 ChinaHEART 迁移的中国人群参照与外部验证 |
| **GTEx** | 数据集 | #衰老 | 约 950 名供体 · 54 个组织（v8） | [链接](https://gtexportal.org/) | partial | 0 | 多组织 eQTL 参考，人群多组学遗传整合与跨队列校正用 |
| **TranscriptFormer** | 模型 | #类器官 #单细胞 #虚拟细胞 | 单细胞基础模型（预训练）* |  | unknown | 3 | 跨物种虚拟细胞图谱，虚拟扰动与跨物种迁移参照 |
| **DINOv2** | 模型 | #类器官 #世界模型 | 未明确（视觉基础模型）* | [链接](https://github.com/facebookresearch/dinov2) | yes | 3 | 类器官视频自监督特征+药效预测，可直接用于类器官demo |
| **GEARS** | 模型 | #单细胞 #虚拟细胞 | 扰动预测模型（基线）* | github.com/snap-stanford/GEARS | unknown | 3 | 扰动预测可迁移基线，虚拟扰动建模对比方法 |
| **SCimilarity** | 模型 | #单细胞 | 2340万细胞，412项研究* | [链接](https://doi.org/10.1038/s41586-024-08411-y) | unknown | 3 | 细胞表示基础模型，跨队列细胞注释与状态查询可用 |
| **ESM-2** | 模型 | #Agent #单细胞 | 蛋白语言模型* | [链接](https://github.com/facebookresearch/esm) | yes | 2 | 蛋白语言模型，可微调用于多组学蛋白模态表征与虚拟扰动 |
| **LucaCell** | 模型 | #类器官 #单细胞 | 8500万人类和小鼠细胞预训练* |  | unknown | 2 | 跨物种单细胞基础模型，类器官注释与虚拟扰动可用 |
| **UCE** | 模型 | #类器官 #单细胞 | 单细胞基础模型（预训练）* | [链接](https://github.com/snap-stanford/UCE) | yes | 2 | 免微调细胞嵌入，类器官衰老demo可作基线表征 |
| **BEHRT** | 模型 | #人群队列 | 百万级患者预训练* |  | unknown | 2 | EHR序列预训练基线，ChinaHEART结构化数据迁移参照 |
| **CellPLM** | 模型 | #单细胞 | 单细胞基础模型（预训练）* |  | unknown | 2 | scEval最佳基础模型之一，类器官单细胞建模候选 |
| **Horvath epigenetic clock (353 CpG)** | 模型 | #衰老 | 353个CpG* |  | unknown | 2 | 经典甲基化年龄基线，类器官与队列衰老评估对标 |
| **Longevity-LLM** | 模型 | #衰老 | 0.6B–9B参数，5个模型* | [链接](https://doi.org/10.1016/j.cell.2026.08.026) | unknown | 2 | 衰老组学基础模型，可微调做表观年龄与多模态衰老表征 |
| **DynaVelo** | 模型 | #类器官 #单细胞 #虚拟细胞 | 小鼠生发中心B细胞* |  | unknown | 1 | 多组学速度+扰动预测，可借鉴到虚拟扰动建模与类器官动态 |
| **Speciesformer** | 模型 | #类器官 #单细胞 #虚拟细胞 | 在1.31亿细胞上预训练* |  | unknown | 1 | 跨物种虚拟细胞基础模型，直接对标虚拟扰动响应建模基线。 |
| **CauTrigger** | 模型 | #单细胞 #虚拟细胞 | 合成与真实多层调控数据集* |  | unknown | 1 | 跨层扰动预测思路，可用于虚拟扰动与类器官状态转变 |
| **PerturbBridge** | 模型 | #单细胞 #虚拟细胞 | BBBC021 6.9万张图像* |  | unknown | 1 | 扰动图像生成思路，可迁移到类器官扰动响应建模 |
| **RegFormer** | 模型 | #单细胞 #世界模型 | 2500万人类细胞预训练* |  | unknown | 1 | 融合GRN先验的扰动预测模型，虚拟扰动建模可迁移 |
| **DNAm PhenoAge** | 模型 | #衰老 | CpG位点评分模型* |  | yes | 1 | 甲基化时钟基线 |
| **I-JEPA** | 模型 | #世界模型 | ViT-Huge/14* | [链接](https://github.com/facebookresearch/ijepa) | yes | 1 | I-JEPA 是自监督表征范式基线，可迁移到类器官图像与组学 |
| **SAM (Segment Anything Model)** | 模型 | #类器官 | 通用图像分割基础模型* | [链接](https://github.com/facebookresearch/segment-anything) | yes | 1 | 类器官延时显微视频自动分割，做类器官衰老 demo 的现成基线 |
| **GrimAge** | 模型 | #衰老 |  |  | unknown | 0 | 死亡率导向的甲基化时钟基线 |
| **PhenoAge** | 模型 | #衰老 |  |  | yes | 0 | 血检生物年龄基线，NHANES 可复现 |
| **EL-PERTURB** | 基准 | #类器官 #单细胞 #虚拟细胞 | 20个模型/6类架构* |  | unknown | 1 | 扰动预测OOD基准，虚拟扰动建模选型与评测参照 |
| **VCBench** | 基准 | #类器官 #单细胞 #虚拟细胞 | 7个能力维度，5种基础模型* | 污染报告模式与共同标签集协议 | unknown | 1 | 单细胞基础模型评测基准，选型与对标时参照 |
| **scArchon** | 基准 | #单细胞 #虚拟细胞 | 9种工具、标准化数据集与指标* | 容器化流程（GitHub） | unknown | 1 | 扰动预测标准化基准，虚拟扰动建模评测直接可用 |
| **ASSAYBENCH** | 基准 | #虚拟细胞 | 1920筛选/约1.38万基因* | [链接](https://github.com/Genentech/AssayBench) | yes | 1 | CRISPR表型预测基准，评估智能体虚拟细胞能力 |
| **GenoTEX** | 基准 | #Agent | 含专家标注代码与结果的分析任务集* | [链接](https://github.com/Liu-Hy/GenoTEX) | yes | 1 | 基因表达分析智能体基准，LLM科研工作流直接对标 |
| **TruthInsightBench** | 基准 | #Agent | 40个盲任务/10领域* | [链接](https://github.com/TruthInsight-stack/TruthInsightBench) | yes | 1 | 科学发现智能体评测，科研智能体工作流可参照 |
| **ARCHS4** | 数据库 | #衰老 | 约5.7万样本，28组织，1,039队列* | [链接](https://maayanlab.cloud/archs4/) | yes | 2 | 跨年龄RNA-seq，转录组衰老时钟训练验证数据 |
| **Human Cell Atlas** | 数据库 | #单细胞 | 多组织细胞图谱* | [链接](https://data.humancellatlas.org/) | yes | 2 | 细胞图谱资源，类器官衰老demo参照与跨组织整合 |
| **CollecTRI** | 数据库 | #虚拟细胞 | 多物种TF-target先验* | [链接](https://github.com/saezlab/CollecTRI) | yes | 1 | TF调控网络先验，扰动预测带符号系数学习 |
| **Gene Expression Omnibus** | 数据库 | #衰老 | 51项人类干预研究* | [链接](https://www.ncbi.nlm.nih.gov/geo/) | yes | 1 | 取公开DNAm数据评估表观遗传时钟对干预响应 |
| **NHGRI-EBI GWAS Catalog** | 数据库 | #人群队列 | 62.5万关联/8.5万数据集* | [链接](https://www.ebi.ac.uk/gwas) | yes | 1 | GWAS汇总统计标准库，ChinaHEART遗传关联查询 |
| **CELLxGENE Census** | 数据库 | #单细胞 |  | [链接](https://chanzuckerberg.github.io/cellxgene-census/) | yes | 0 | 面向 ML 的单细胞全库切片，虚拟扰动与表征预训练数据源 |
| **ClockBase** | 数据库 | #衰老 |  |  | unknown | 0 | 甲基化时钟基准平台，选时钟与评估类器官衰老模型时参照 |
| **DepMap** | 数据库 | #虚拟细胞 |  | [链接](https://depmap.org/portal/) | yes | 0 | 癌细胞系扰动依赖数据，虚拟扰动建模的迁移起点 |
| **HuBMAP** | 数据库 | #单细胞 |  | [链接](https://portal.hubmapconsortium.org/) | yes | 0 | 人体单细胞+空间图谱，类器官多模态对齐与空转参照 |
| **Olink** | 工具 | #人群队列 | 约5,416种蛋白* | [链接](https://olink.com/) | commercial | 3 | 蛋白组检测平台，ChinaHEART蛋白组方案参照 |
| **scvi-tools** | 工具 | #单细胞 | 变分自编码器框架* | [链接](https://github.com/scverse/scvi-tools) | yes | 3 | 单细胞嵌入经典基线，类器官与虚拟细胞建模对照。 |
| **MEDICINE portal** | 工具 | #衰老 #人群队列 | 5个器官特异性MetBAG模型* | MEDICINE门户 | unknown | 2 | 器官特异性代谢组衰老时钟，可作类器官/队列衰老建模参照 |
| **Biomni** | 工具 | #Agent | 25领域数千文献工具* |  | unknown | 2 | 通用生物医学智能体，科研工作流与基因优先排序可试 |
| **Perturb-seq** | 工具 | #单细胞 #虚拟细胞 | 约20万细胞* |  | unknown | 2 | CRISPR扰动数据，虚拟扰动建模训练与基准 |
| **Trellis** | 工具 | #类器官 | >2500个CRC PDO与CAF* |  | unknown | 2 | 类器官药物响应分析方法，可直接用于类器官扰动响应建模。 |
| **Perturb-FISH** | 工具 | #类器官 #单细胞 | THP1/hIPSC/异种移植体系* | [链接](https://doi.org/10.1016/j.cell.2025.02.012) | unknown | 1 | 空间扰动读取思路，可用于类器官虚拟扰动建模设计 |

## P2 了解即可（67）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **ImageNet-1K** | 数据集 | #世界模型 | 1000类约128万图* | [链接](https://www.image-net.org) | unknown | 10 | 用于线性/冻结探针评估自监督表征质量及预训练。 |
| **FinnGen** | 数据集 | #衰老 #人群队列 | 17.7万人，2,444疾病表型* | [链接](https://www.finngen.fi/) | unknown | 6 | 用于慢性疼痛GWAS荟萃分析及跨国家EHR预测模型迁移验证。 |
| **ModelNet40** | 数据集 | #世界模型 | 40 类 3D 模型* | [链接](https://modelnet.cs.princeton.edu/) | unknown | 4 | 用于点云自监督方法的线性分类与少样本分类评测。 |
| **MATH** | 数据集 | #Agent | 约1.25万题* | [链接](https://github.com/hendrycks/math) | yes | 3 | 用于评测数学推理准确率（DeepSeekMath与TEMPO）。 |
| **GSM8K** | 数据集 | #Agent #世界模型 | 约8.5千题* | [链接](https://github.com/openai/grade-school-math) | yes | 2 | 用于评估DLLM-JEPA在掩码扩散语言模型上的数学推理提升。 |
| **AMC23** | 数据集 | #Agent | AMC 2023题集* | [链接](https://huggingface.co/datasets/AI-MO/aimo-validation-amc) | unknown | 2 | PURE 用于评测 Qwen2.5-Math-7B 的推理性能。 |
| **CPRD Aurum** | 数据集 | #人群队列 | 英国全科诊疗数百万患者* | [链接](https://www.cprd.com/（申请访问）) | unknown | 2 | 用于阿尔茨海默病和帕金森病基于EHR的Transformer嵌入与亚型聚类。 |
| **GeneCorpus-30M** | 数据集 | #单细胞 | 约3000万单细胞* |  | unknown | 2 | 作为单细胞基础模型（如Geneformer）的预训练语料，并被用于污染审计。 |
| **JetClass** | 数据集 | #世界模型 | 未明确（喷注数据集）* | 项目网站公开 | unknown | 2 | 用于预训练HEP-JEPA高能物理基础模型并评估top tagging等下游任务。 |
| **ScanObjectNN** | 数据集 | #世界模型 | 约1.5万扫描物体* | [链接](https://hkust-vgd.github.io/scanobjectnn/) | unknown | 2 | 用于CrossJEPA的3D表征线性探测评估。 |
| **AllenCell** | 数据集 | #单细胞 #虚拟细胞 | 公开细胞图像库* | AllenCell | unknown | 1 | 用于评测PerturbBridge扰动图像生成的公开细胞显微图像数据集。 |
| **GSM-Plus** | 数据集 | #Agent | 约1万题* | [链接](https://huggingface.co/datasets/qintongli/GSM-Plus) | yes | 1 | 数学推理评测集，与生物应用弱相关。 |
| **Libri-light** | 数据集 | #世界模型 | 60000小时* | [链接](https://github.com/facebookresearch/libri-light) | yes | 1 | 用于HuBERT大规模无标注语音预训练及多规模微调评测。 |
| **MIMIC-IV** | 数据集 | #人群队列 | 约30万患者* | [链接](https://physionet.org/content/mimiciv/) | controlled | 1 | 用于评估MiGHT-EHR在四项临床任务上的性能。 |
| **PRM800K** | 数据集 | #Agent | 约80万步级标签* | [链接](https://github.com/openai/prm800k) | yes | 1 | PURE 用于训练过程奖励模型并研究最小形式信用分配。 |
| **ADVANCE** | 数据集 |  |  |  | unknown | 0 |  |
| **BioBank Japan** | 数据集 | #人群队列 | 第一期约 20 万患者（47 种疾病） | [链接](https://biobankjp.org/) | controlled | 0 |  |
| **Cardiovascular Health Study** | 数据集 | #衰老 | 5,888 人（65 岁以上） | [链接](https://chs-nhlbi.org/) | controlled | 0 | 老年心血管队列，衰老表型参照，受控访问 |
| **CODE-15%** | 数据集 |  | 约 34.6 万份心电 / 23.4 万患者 | [链接](https://zenodo.org/records/4916206) | yes | 0 |  |
| **PTB-XL** | 数据集 |  | 21,799 份心电 / 18,869 人 | [链接](https://physionet.org/content/ptb-xl/) | yes | 0 |  |
| **TCGA** | 数据集 |  |  | [链接](https://portal.gdc.cancer.gov/) | partial | 0 |  |
| **Qwen3-4B** | 模型 | #Agent | 4B参数* | Hugging Face (Qwen/Qwen3-4B) | unknown | 3 | 用于验证TEMPO在分布内与分布外推理基准上的收敛与性能。 |
| **DINO-WM** | 模型 | #世界模型 | 六个环境* |  | unknown | 2 | 作为冻结预训练世界模型，用于验证Sandwich-Residuals在三维操作任务上的测试时自适应。 |
| **Qwen2.5-Math-7B** | 模型 | #Agent | 7B 参数* | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-7B) | yes | 2 | 作为基座模型用于 PRM 引导强化学习与 RLVR 对比实验。 |
| **Qwen3-1.7B** | 模型 | #Agent | 1.7B参数* | Hugging Face (Qwen/Qwen3-1.7B) | unknown | 2 | 用于验证TEMPO信用分配方法在推理基准上的性能。 |
| **Qwen3-8B** | 模型 | #Agent | 8B参数* | Hugging Face (Qwen/Qwen3-8B) | unknown | 2 | 作为RLVR信用分配与GEAR优势重加权实验的基础模型。 |
| **Graph-JEPA** | 模型 | #世界模型 | 未明确* | [链接](https://github.com/geriskenderi/graph-jepa) | yes | 1 | 该文献提出的图级联合嵌入预测架构表征学习模型，代码公开。 |
| **MAE** | 模型 | #世界模型 | ViT-Huge约6.3亿参数* | [链接](https://github.com/facebookresearch/mae) | yes | 1 | 掩码自编码器预训练模型，ImageNet-1K达87.8%。 |
| **MoCo** | 模型 | #世界模型 | ResNet-50骨干* | [链接](https://github.com/facebookresearch/moco) | yes | 1 | 基于队列与动量编码器的对比学习预训练模型。 |
| **Point-JEPA** | 模型 | #世界模型 | 未明确* | [链接](https://github.com/Ayumu-J-S/Point-JEPA) | yes | 1 | 该文献提出的点云联合嵌入预测架构自监督模型，代码公开。 |
| **Qwen2.5-Math-1.5B** | 模型 | #Agent | 1.5B 参数* | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-1.5B) | yes | 1 | 作为小规模基座模型验证 PURE 最小形式信用分配效果。 |
| **AlphaFold** | 模型 |  |  | [链接](https://github.com/google-deepmind/alphafold) | yes | 0 |  |
| **DNABERT-2** | 模型 |  |  | [链接](https://github.com/MAGICS-LAB/DNABERT_2) | yes | 0 |  |
| **Enformer** | 模型 |  |  |  | yes | 0 |  |
| **Nucleotide Transformer** | 模型 |  |  | [链接](https://github.com/instadeepai/nucleotide-transformer) | yes | 0 |  |
| **ALFWorld** | 基准 | #Agent | 约3500+任务实例* | [链接](https://alfworld.github.io/) | unknown | 4 | ReAct 与 AgentPRM 用于交互式决策/智能体过程奖励训练与评测。 |
| **MMLU** | 基准 | #Agent #世界模型 | 约1.4万题，57学科* | [链接](https://github.com/hendrycks/test) | unknown | 2 | 用于评估DLLM-JEPA的多任务知识与推理性能。 |
| **COCO** | 基准 | #世界模型 | 80类约33万图* | [链接](https://cocodataset.org) | unknown | 2 | 作为下游检测与分割任务评估自监督表征迁移能力。 |
| **ProcessBench** | 基准 | #Agent | 约3400条推理路径* | [链接](https://huggingface.co/datasets/Qwen/ProcessBench) | yes | 2 | 用于步级过程错误检测评测 PRM 性能。 |
| **scIB** | 基准 | #单细胞 | 13个整合任务，最多100万细胞* | [链接](https://doi.org/10.1038/s41592-021-01336-8) | unknown | 2 | 用于评测单细胞数据整合工具及审计基础模型基准的预训练污染。 |
| **WebShop** | 基准 | #Agent | 约1.18万条指令* | [链接](https://webshop-pnlp.github.io/) | unknown | 2 | 用于评测不确定性感知奖励下LLM智能体的任务成功率。 |
| **HumanEval** | 基准 | #Agent | 164道编程题* | [链接](https://github.com/openai/human-eval) | yes | 1 | Reflexion在编码任务上评估pass@1的基准。 |
| **MemCalib** | 基准 | #Agent | 15000例（13500训练+1500测试）* | [链接](https://github.com/Quark-Medical/memcalib) | yes | 1 | 智能体记忆评测，方法储备了解即可 |
| **NKIBench** | 基准 | #Agent | 来自真实LLM工作负载的Trainium内核* | [链接](https://github.com/zhang677/AccelOpt) | yes | 1 | 用于评测LLM智能体自主优化AWS Trainium内核的效果。 |
| **PaperBench** | 基准 | #Agent | 20篇论文，8,316个可评分任务* | [链接](https://github.com/openai/preparedness) | yes | 1 | 评测AI智能体从零复现前沿AI研究的能力。 |
| **R-Judge** | 基准 | #Agent | 569条交互，27类风险场景* | [链接](https://github.com/Lordog/R-Judge) | yes | 1 | 用于评测LLM智能体在交互环境中的安全风险意识。 |
| **SKILLMISEVO-BENCH** | 基准 | #Agent | 冻结基准，覆盖多类任务* | [链接](https://github.com/henrymao2004/misevolve) | yes | 1 | 冻结基准，用于衡量技能演化后的不安全检索与新会话危害。 |
| **SKILLMISEVO-GYM** | 基准 | #Agent | 25种配置×525任务×25回合* | [链接](https://github.com/henrymao2004/misevolve) | yes | 1 | 生命周期感知测试台，用于研究自改进智能体的技能误演化。 |
| **Socratic-PRMBench** | 基准 | #Agent | 2995条路径，平均8.7步* | [链接](https://github.com/Xiang-Li-oss/Socratic-PRMBench) | yes | 1 | 系统评测 PRM 在六种推理模式下的过程错误检测能力。 |
| **ENCODE** | 数据库 | #Agent | 132个转录因子* | [链接](https://www.encodeproject.org/) | yes | 1 | 转录因子结合数据，仅用于基序发现评测。 |
| **Aging Atlas** | 数据库 | #衰老 |  | [链接](https://ngdc.cncb.ac.cn/aging/) | yes | 0 |  |
| **ArrayExpress** | 数据库 |  |  | [链接](https://www.ebi.ac.uk/biostudies/arrayexpress) | yes | 0 |  |
| **CellAge** | 数据库 | #衰老 |  | [链接](https://genomics.senescence.info/cells/) | yes | 0 |  |
| **dbGaP** | 数据库 | #人群队列 |  | [链接](https://www.ncbi.nlm.nih.gov/gap/) | controlled | 0 |  |
| **EGA** | 数据库 | #人群队列 |  | [链接](https://ega-archive.org/) | controlled | 0 |  |
| **EWAS Atlas** | 数据库 | #衰老 |  | [链接](https://ngdc.cncb.ac.cn/ewas/atlas) | yes | 0 |  |
| **GenAge** | 数据库 | #衰老 |  | [链接](https://genomics.senescence.info/genes/) | yes | 0 |  |
| **Human Protein Atlas** | 数据库 |  |  | [链接](https://www.proteinatlas.org/) | yes | 0 |  |
| **MassIVE** | 数据库 |  |  | [链接](https://massive.ucsd.edu/) | yes | 0 |  |
| **Open Genes** | 数据库 | #衰老 |  | [链接](https://open-genes.com/) | yes | 0 |  |
| **Open Targets** | 数据库 |  |  | [链接](https://platform.opentargets.org/) | yes | 0 |  |
| **PRIDE** | 数据库 |  |  | [链接](https://www.ebi.ac.uk/pride/) | yes | 0 |  |
| **recount3** | 数据库 |  |  | [链接](https://rna.recount.bio/) | yes | 0 |  |
| **Single Cell Portal** | 数据库 | #单细胞 |  | [链接](https://singlecell.broadinstitute.org/) | yes | 0 |  |
| **SRA** | 数据库 |  |  | [链接](https://www.ncbi.nlm.nih.gov/sra) | yes | 0 |  |
| **fastGxE** | 工具 | #人群队列 | 生物样本库规模* | [链接](https://doi.org/10.1038/s41588-026-02806-5) | unknown | 2 | 基因环境交互工具，人群队列可选分析 |
| **SomaScan** | 工具 | #人群队列 |  |  | commercial | 0 |  |

## 日报新发现（22，未核验）

- LACA: a cross-species single-cell resource for exploring longevity and aging-associated cellular and molecular programs.（数据集，2026-11-21）https://doi.org/10.1093/nar/gkag1129
- [dataset] transhumanist-already-exists/pansci-mouse-aging-snrna（数据集，2026-11-08）https://huggingface.co/datasets/transhumanist-already-exists/pansci-mouse-aging-snrna
- Multi-omics in the All Of Us Research Program expands mapping genetic mechanisms in health and disease（数据集，2026-11-04）https://doi.org/10.64898/2026.10.29.26366507
- A haplotype reference panel constructed from 490,319 UK Biobank genomes improves genotype imputation for global populations.（数据集，2026-11-01）https://doi.org/10.1038/s41588-026-02819-0
- ProtCell: a foundation model for single-cell proteomics（模型，2026-10-28）https://doi.org/10.64898/2026.10.22.760932
- CauTrigger: deciphering biological system state transitions by hierarchical causal decomposition.（模型，2026-10-25）https://doi.org/10.1038/s41592-026-03274-9
- An open vision-language model for diverse medical applications.（模型，2026-10-17）https://doi.org/10.1038/s41591-026-04626-w
- scRNA-seq（数据集，2026-10-11）
- VINTER: a generative vision-language model for annotating and interrogating spatial tissues（模型，2026-10-09）https://doi.org/10.64898/2026.10.01.752251
- Urban Genomics in a Rapidly Urbanizing Megacity Reveals Layered Cardiometabolic Genetic Architecture（数据集，2026-10-06）https://doi.org/10.21203/rs.3.rs-10933833/v1
- A pre-train and fine-tune framework for adaptive boosting of pre-trained polygenic risk scores.（模型，2026-10-02）https://doi.org/10.1038/s41467-026-77128-5
- EpiZoo: a DNA sequence-aware foundation model for cross-species single-cell epigenomics（模型，2026-10-02）https://doi.org/10.64898/2026.09.24.754017
- SingPro 2.0: a proteomics-centric knowledge base for single-cell multimodal profiling.（数据集，2026-10-02）https://doi.org/10.1093/nar/gkag933
- NexuST: A Hierarchical Foundation Model for Spatial Transcriptomics（模型，2026-09-29）https://doi.org/10.64898/2026.09.22.753590
- Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling（模型，2026-09-26）https://doi.org/10.64898/2026.09.22.752128
- A single-cell RNA-seq catalog of ground truth gene coregulation（数据集，2026-09-22）https://doi.org/10.64898/2026.09.18.752692
- A lifespan-scale single-cell atlas defines an early-childhood immunometabolic transition linked to age-referenced immune states（数据集，2026-09-19）https://doi.org/10.64898/2026.09.11.750312
- spaGFM is a scalable graph foundation model for spatial transcriptomics analyses（模型，2026-09-19）https://doi.org/10.21203/rs.3.rs-11012643/v1
- A massively parallel synthetic gene atlas for learning compact cis-regulatory grammar across cellular contexts（数据集，2026-09-16）https://doi.org/10.64898/2026.09.13.751267
- LucaCell: a sequence-centric foundation model for cross-species single-cell analysis（模型，2026-09-16）https://doi.org/10.64898/2026.09.08.750024
- Single-cell splice isoform usage reveals distinct axes of cellular identity and senescence（数据集，2026-09-16）https://doi.org/10.64898/2026.09.11.748700
- A breast tissue-specific epigenetic clock provides accurate chronological age predictions and reveals de-correlation of age and DNA methylation in tumor-adjacen（模型，2026-09-15）https://doi.org/10.1080/15592294.2026.2714582

## 单篇提及（367，未进主表）

- 数据集：23andMe、AASK (African American Study of Kidney Disease and Hypertension)、ADE20K、AIDA v2、ALSPAC、Adamson、Adamson Perturb-seq、AudioSet、AudioSet-20K、CARDINAL、COCO-Stuff、CTRP、CeNGEN、Cityscapes、DFTJ、Droid、EPIC-Norfolk、ESC-50、EST-Health-30、Estonian Biobank、FEVER、FSD50K、Fenland、Finnish THL Biobank、GEO GSE67752、GIANT Consortium、Generation Scotland、HAECA、HM3D v0.2、HotpotQA、HumanST-46M、INSPIRE-T cohort、ImageOmicsNet-300M、Integrated Mega-scale Atlas、JUMP-CP、JUMP-MOA、JUMP-Target2、JUMP-lite、KORA cohort、LOGIQA、Librispeech、Lorenz attractor trajectories、Lothian Birth Cohort 1936 (LBC1936)、MATH500、MGB Biobank、MIMIC、MIMIC-III、MNIST、MODIS、Mass General Brigham Biobank、McFarland、Mexico City Prospective Study (MCPS)、Mount Sinai、Norman、Norman K562 CRISPRa dataset、Nurses' Health Study (NHS)、PURE、Perturb-seq genome-scale screen、PerturbReason、Replogle、Replogle Perturb-seq、SCIPRM70K、ST-bank、SciPlex3、Sentinel-1、Sentinel-2、SpatialCorpus-110M、THL Biobank、Taiwan Biobank (TWB)、Taiwan Precision Medicine Initiative (TPMI)、UK Biobank Exome Sequencing (49,960 WES)、UK Biobank Exome Sequencing Consortium (UKB-ESC) data、UK Biobank NMR Metabolomics、UK Biobank Polygenic Risk Score Release、UK Biobank Whole-Genome Sequencing、US Veterans Affairs EHR、VCC-H1、WikiText、X-Atlas/Pisces、iNaturalist-21
- 模型：3D-JEPA、AB-PRS、AROMA、ATM (Age-dependent Topic Model)、AURORA、AdaptAge、AlphaEarth、AlphaFold-Multimer、AlphaGenome、Audio-MAE、BYOL、BitAge、Borzoi、BrainBeacon、CAME、CLM-X、CLOOME、CMAE、CPA、CTBA、CTransPath、Cell-o1、CellFM、CellFlux、CellFluxRL、CellOT、CellPaintSSL、CellWorld、ClinicalAge、D-SPIN、D2R2、DamAge、DeepSeek-R1、DeepSeekMath、DiRL、ECM aging clock、EHR-MPC、EHRAgent、EpiZoo、Flow-JEPA、Foresight、Foresight-England、GOLD BioAge、GPN-Star、GRASP、GenEHR、GenVinci、GeneCompass、GenePT、GraphCL、HAPNEST、HELICS、HPS (Healthspan Proteomic Score)、Hannum epigenetic clock、Horvath multi-tissue clock、HuBERT、JEPA-Anything、JEPA-DNA、KASM、Kimi k1.5、Kosmos、LPAI、LaMamba-Diff、LifeLong Digital Twin、LinAge2、MC-JEPA、MEGASCORE、MILTON、MSGene、MSKAge / MSKAgeMort、MVX、Med-BERT、MetBAG、MetaboHealth、MiGHT-EHR、Mouse-Geneformer、MrVI、NOAH、NeRF-MAE、NexuST
- 基准：ABC-Bench、AI4AI-Bench、AdaJEPA、BAISBench、BIRD、BLADE、BioDataLab、BioKGBench、BioML-bench、BiomniBench-DA、Cell-Eval、CellBench、CellPuzzles、ComputAgeBench、D4RL、DiscoverPhysics、GSM-HARD、Gaia2、HLE、Hofmarcher benchmark、LAB-Bench、LABBench2、LMR-BENCH、LVIS、MLAgentBench、MMLU-Medical、MedMCQA、MedPRMBench、MedQA、Moshkov benchmark、OfficeQA、PASCAL VOC、PertEval-scFM、PerturBench、PerturbQA、ProteinGym、PushT、RSIBench-Data、RoboTwin、Robomimic、SEAGym、SciIntegrity-Bench、ScienceAgentBench、SealQA、SoundnessBench、StreamBench、Systema、Terminal-Bench 2.0、ToolMaker Benchmark、VTAB、Virtual Cell Challenge 2026、X-ARES、scEval
- 数据库：Allen Brain Atlas、CMAP、Cell Landscape、ChIP-Atlas、DISCO (single-cell database)、Danish National Patient Registry (DNPR)、EMBL-EBI ArrayExpress/BioStudies、GeneATLAS、Immunosenescence Inventory、LACA、MCATS、PGS Catalog、Proteome-Phenome Atlas、SEA-AD、STP、TEAPEE
- 工具：AIDE、AccelOpt、AgentPRM、BASIL、BOLT-LMM、BioLLM、Biolearn、CINEMA-OT、CROP-seq、CellOracle、CellPaint-POSH、CellProfiler、CellScientist、ClockBase Agent、DeGAs、ERA、FaithRL、GATK、GEPA、Habitat、Hail、Harmony、ICD-8 to ICD-10 Mapping Table、Intuitor、K-Dense、LWD-Miniscope、LivAge、Loki、Longevity Claw、MetabHub、Mosaic、Nahual、OSCAR、PHESANT、PRS-PheWAS atlas web application、PheMIME、PheWeb、Phecodes、REGENIE、ROSE、Rosetta、SAFEEVOLVE、SAIGE-GENE、SARDINE、SCOPE (Systematic Classification of Organoids for Phenotypic Evaluation)、SCanSNP、SIQReg、SPAC-seq、SPA_GRM、STELLA、SenePy、SpatialQM、Superb-seq、TARDIS、TFActProfiler、TeLLAgent、The AI Scientist、TranslAGE、TreeRL、UKB-MDRMF、Virtual Lab、copairs、leakcheck、moscot、scContam、ukbnmr
