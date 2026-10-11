# 资源登记（数据集 / 模型 / 基准）

从 841 处证据引用中挖出资源，并入人工种子与日报新发现，共 584 项；主表 165 项（种子/置顶，或被 ≥2 篇工作使用、或跨方向、或开放且链接核验通过且规模明确），日报新发现 14 项（未核验），其余 405 项单篇提及的列在末尾。开放：yes 公开 / partial 部分 / registration 注册 / controlled 受控 / commercial 商业 / unknown 未确认。核验：ok 内容匹配 / mismatch 页面不是该资源 / blocked 站点拒绝探测 / dead 失效 / n/a 非链接。规模带 * 的取自单篇引用文献。更新 2026-10-11


## P0 优先上手（26）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **UK Biobank** | 数据集 | #衰老 #心血管 #人群队列 | 约 50 万人（40–69 岁入组，2006–10） | [链接](https://www.ukbiobank.ac.uk/) | controlled | 118 | 多组学衰老与CVD方法迁移主数据源，ChinaHEART参照基准 |
| **UK Biobank Pharma Proteomics Project** | 数据集 | #心血管 #人群队列 #衰老 | 约 5.4 万人 · 约 2,900 蛋白 | [链接](https://www.ukbiobank.ac.uk/) | controlled | 13 | UKB蛋白组，ChinaHEART蛋白组CVD风险迁移参照 |
| **China Kadoorie Biobank** | 数据集 | #衰老 #心血管 #人群队列 | 约 51 万成人（10 个地区，2004–08 入组） | [链接](https://www.ckbiobank.org/) | controlled | 10 | 中国人群参照队列，ChinaHEART 迁移时的对照 |
| **Tahoe-100M** | 数据集 | #单细胞 #虚拟细胞 | 1亿转录组，50细胞系，1100药物条件* | [链接](https://huggingface.co/datasets/tahoebio/Tahoe-100M) | yes | 4 | 亿级药物扰动图谱，虚拟扰动预训练与类器官demo核心数据 |
| **UK Biobank Olink Proteomics** | 数据集 | #人群队列 | 54,219人 / 2,923蛋白* | [链接](https://www.ukbiobank.ac.uk/) | unknown | 3 | UKB蛋白组，ChinaHEART蛋白组迁移与pQTL建模直接参照 |
| **Norman 2019 Perturb-seq** | 数据集 | #单细胞 #虚拟细胞 | 91,205单细胞* | GEO | unknown | 2 | 组合扰动基准数据，虚拟扰动响应建模必用基线 |
| **Replogle 2022 Perturb-seq** | 数据集 | #虚拟细胞 | >250万人类细胞* | doi:10.1016/j.cell.2022.05.013 | unknown | 2 | 基因组规模Perturb-seq，扰动预测建模与基准评估核心数据 |
| **Adamson Perturb-seq** | 数据集 | #单细胞 #虚拟细胞 | 68,603单细胞* | GEO | unknown | 1 | 扰动scRNA基准数据，虚拟扰动建模与类器官demo直接可用 |
| **Replogle Perturb-seq** | 数据集 | #单细胞 #虚拟细胞 | K562 162,751与RPE1 162,733细胞* | GEO | unknown | 1 | 虚拟扰动建模标准基准，类器官扰动响应直接对标 |
| **ChinaHEART** | 数据集 | #心血管 #人群队列 | 中国大规模心血管病筛查/早筛队列 |  | controlled | 1 | 目标队列：UKB 等公共队列方法迁移的落点 |
| **scGPT** | 模型 | #类器官 #单细胞 #虚拟细胞 | 预训练于3300万+细胞* | [链接](https://github.com/bowang-lab/scGPT) | yes | 18 | 单细胞基础模型基线，类器官衰老demo与虚拟扰动对标 |
| **Geneformer** | 模型 | #衰老 #单细胞 #虚拟细胞 | 基于基因排序的Transformer* | [链接](https://huggingface.co/ctheodoris/Geneformer) | yes | 13 | 单细胞基础模型基线，类器官衰老demo与虚拟扰动建模直接对标 |
| **scFoundation** | 模型 | #单细胞 #虚拟细胞 | 预训练单细胞基础模型* | [链接](https://github.com/biomap-research/scFoundation) | yes | 7 | 扰动预测基准模型，类器官扰动demo可直接部署对比 |
| **Tahoe-X1** | 模型 | #单细胞 #虚拟细胞 | 1.3B 参数* | [链接](https://huggingface.co/tahoebio) | yes | 3 | 扰动训练单细胞基础模型，虚拟扰动响应建模首选基线 |
| **China-PAR** | 模型 | #心血管 | 推导21320人，验证84961人* | [链接](https://doi.org/10.1161/CIRCULATIONAHA.116.022367) | yes | 3 | 中国人群传统评分基线，ChinaHEART 模型必须对标 |
| **Chreode** | 模型 | #单细胞 #虚拟细胞 | 240万细胞小鼠胚胎图谱预训练* | [链接](https://arxiv.org/abs/2605.28111v1) | unknown | 2 | 细胞世界模型，虚拟扰动响应与类器官时序建模直接参照 |
| **SCALE** | 模型 | #单细胞 #虚拟细胞 | CRISPR/化学/发育/免疫* | [链接](https://arxiv.org/abs/2603.17380v3) | unknown | 1 | 条件传输虚拟扰动模型，类器官扰动响应建模直接可用 |
| **ALADYNOULLI** | 模型 | #人群队列 #心血管 | 68.3万人，348种疾病* |  | unknown | 1 | 生成式疾病轨迹的对标基线（可解释） |
| **Delphi-2M** | 模型 | #人群队列 #心血管 | UKB 约 40 万人训练 + 丹麦 190 万人验证 · 1000+ 病种 |  | unknown | 1 | 生成式疾病轨迹的对标基线 |
| **Pooled Cohort Equations** | 模型 | #心血管 | 标准临床风险方程* |  | yes | 1 | 心血管风险预测的传统评分基线 |
| **Virtual Cell Challenge** | 基准 | #单细胞 #虚拟细胞 | 专用扰动数据集（细节未公开）* | Arc Institute | unknown | 1 | 虚拟扰动响应基准，类器官/细胞虚拟扰动建模直接对标 |
| **LongevityBench** | 基准 | #衰老 | 17任务/5数据域/18个AI系统* | [链接](https://doi.org/10.1016/j.cell.2026.08.026) | unknown | 1 | 衰老 AI 基准（Cell 2026），模型评测对标 |
| **CELLxGENE** | 数据库 | #衰老 #单细胞 | 超7000万细胞* | [链接](https://cellxgene.cziscience.com/) | yes | 1 | 单细胞图谱，训练类器官/单细胞衰老时钟的公开数据 |
| **CELLxGENE Census** | 数据库 | #单细胞 |  | [链接](https://chanzuckerberg.github.io/cellxgene-census/) | yes | 0 | 面向ML的单细胞全库切片，类器官与队列单细胞建模直接可用 |
| **scPerturb** | 数据库 | #虚拟细胞 |  |  | yes | 0 | 单细胞扰动聚合库，虚拟扰动响应建模直接训练数据 |
| **Cell Painting** | 工具 | #衰老 #单细胞 | 多通道荧光图像profiling* | [链接](https://doi.org/10.1038/s41592-024-02528-8) | unknown | 2 | 细胞形态扰动响应，类器官+cell painting扰动建模核心 |

## P1 值得登记（71）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **All of Us Research Program** | 数据集 | #心血管 #人群队列 | 目标 100 万人（美国，多族裔） | [链接](https://www.researchallofus.org/) | controlled | 13 | 多血统EHR+基因组，PRS与EHR关联复制方法参照 |
| **ARIC** | 数据集 | #心血管 #人群队列 | 约 1.6 万人（1987–89 入组） | [链接](https://www2.cscc.unc.edu/aric/) | controlled | 6 | 蛋白组心衰/衰弱队列，ChinaHEART蛋白组参照 |
| **Framingham Heart Study** | 数据集 | #衰老 #心血管 | 10,097人/28,151份ECG* | [链接](https://www.framinghamheartstudy.org/) | controlled | 3 | ECG-AF深度学习经典队列，心血管AI模型对标 |
| **MESA** | 数据集 | #心血管 #人群队列 | 6,814 人（45–84 岁，四个族裔） | [链接](https://www.mesa-nhlbi.org/) | controlled | 3 | 多模态CVD队列，心血管基础模型外部验证 |
| **UK Biobank Exome Sequencing** | 数据集 | #人群队列 | 454,787人 / 12.3M变异* | [链接](https://www.ukbiobank.ac.uk/) | unknown | 3 | UKB外显子数据，ChinaHEART遗传-多组学整合方法迁移参照。 |
| **CHARGE-AF Consortium** | 数据集 | #心血管 | 推导18,556例；验证7,672例（5队列）* | [链接](https://www.chargeconsortium.com/) | unknown | 2 | 房颤风险评分基准，ChinaHEART心血管预测可参照 |
| **CHARLS** | 数据集 | #心血管 #人群队列 #衰老 | 8,080名≥45岁人群* | [链接](https://charls.pku.edu.cn/) | registration | 2 | 中国队列，ChinaHEART迁移与AI-ECG外部验证 |
| **Global Biobank Meta-analysis Initiative (GBMI)** | 数据集 | #人群队列 | 23库，220万人，14疾病* | [链接](https://www.globalbiobankmeta.org/) | unknown | 2 | 跨库荟萃资源，跨祖源PRS评估方法参照 |
| **THL Biobank** | 数据集 | #人群队列 | 三国生物库之一* | [链接](https://thl.fi/en/web/thl-biobank) | unknown | 2 | NMR代谢组重复验证队列，ChinaHEART代谢标志物外部参照 |
| **SpeciesCorpus** | 数据集 | #类器官 #单细胞 #虚拟细胞 | 1.31 亿细胞* |  | unknown | 1 | 跨物种单细胞语料，可预训练虚拟细胞模型支撑类器官与扰动。 |
| **CODE-15%** | 数据集 | #心血管 | 约 34.6 万份心电 / 23.4 万患者 | [链接](https://zenodo.org/records/4916206) | yes | 1 | 大规模ECG公开数据，ECG基础模型预训练验证 |
| **MIMIC-IV-ECG** | 数据集 | #心血管 | 公开ECG数据库* | [链接](https://physionet.org/content/mimic-iv-ecg/) | yes | 1 | 80万ECG公开数据，可预训练ECG基础模型用于心血管队列。 |
| **NHANES** | 数据集 | #衰老 #人群队列 | 每两年约 1 万人（美国代表性样本） | [链接](https://www.cdc.gov/nchs/nhanes/) | yes | 1 | 外部验证衰老时钟对死亡风险捕捉，可作ChinaHEART迁移参照 |
| **Tabula Sapiens** | 数据集 | #单细胞 | 564,253 细胞，多供体* | [链接](https://tabula-sapiens-portal.ds.czbiohub.org) | unknown | 1 | 多供体单细胞图谱，可作类器官与虚拟细胞表征基准。 |
| **Cell Painting Gallery** | 数据集 | #类器官 |  | [链接](https://github.com/broadinstitute/cellpainting-gallery) | yes | 0 | 细胞成像形态数据，类器官cell painting+ML可用 |
| **GTEx** | 数据集 | #衰老 | 约 950 名供体 · 54 个组织（v8） | [链接](https://gtexportal.org/) | partial | 0 | 多组织eQTL参考，人群多组学遗传整合基线 |
| **LINCS L1000** | 数据集 | #虚拟细胞 |  | [链接](https://clue.io/) | registration | 0 | 扰动转录组数据，虚拟扰动建模训练与对标 |
| **Pan-UK Biobank** | 数据集 | #人群队列 |  | [链接](https://pan.ukbb.broadinstitute.org/) | yes | 0 | 多祖源GWAS汇总，ChinaHEART遗传整合与跨队列校正参照 |
| **PTB-XL** | 数据集 | #心血管 | 21,799 份心电 / 18,869 人 | [链接](https://physionet.org/content/ptb-xl/) | yes | 0 | 公开心电标注数据，ChinaHEART心血管AI建模可迁移 |
| **SCORE2** | 模型 | #心血管 | 欧洲10年CVD风险模型* | [链接](https://doi.org/10.1093/eurheartj/ehab309) | unknown | 6 | 欧洲CVD风险基线，ChinaHEART模型对标 |
| **TranscriptFormer** | 模型 | #类器官 #单细胞 #虚拟细胞 | 1.12亿细胞、12物种* |  | unknown | 3 | 跨物种虚拟细胞图谱，虚拟扰动与跨物种迁移参照 |
| **DINOv2** | 模型 | #类器官 #世界模型 | ViT-S/B，ImageNet预训练* | [链接](https://github.com/facebookresearch/dinov2) | yes | 3 | 类器官视频自监督特征+药效预测，可直接用于类器官demo |
| **GEARS** | 模型 | #单细胞 #虚拟细胞 | 未明确* | github.com/snap-stanford/GEARS | unknown | 3 | 扰动预测可迁移基线，虚拟扰动建模对比方法 |
| **CHARGE-AF** | 模型 | #心血管 | 房颤风险预测方程* | [链接](https://www.chargeaf.org/) | unknown | 3 | 房颤风险模型，AI-ECG与蛋白组评分比较基线 |
| **PREVENT** | 模型 | #心血管 | 美国AHA 10年CVD风险方程* | [链接](https://doi.org/10.1161/CIRCULATIONAHA.123.067626) | unknown | 3 | AHA风险方程，蛋白组评分增量比较基线 |
| **QRISK3** | 模型 | #心血管 | QResearch 1998-2015开放队列* | [链接](https://qrisk.org/) | unknown | 3 | 英国CVD风险模型，蛋白组增量比较基线 |
| **SCimilarity** | 模型 | #单细胞 | 2270 万细胞、399 项研究* | [链接](https://doi.org/10.1038/s41586-024-08411-y) | unknown | 3 | 细胞表示基础模型，跨队列细胞注释与状态查询可用 |
| **CPA** | 模型 | #单细胞 #虚拟细胞 | 未明确* | github.com/theislab/cpa | unknown | 2 | 组合扰动自编码器，虚拟扰动预测必对标基线。 |
| **LucaCell** | 模型 | #类器官 #单细胞 | 8500万人鼠单细胞预训练* |  | unknown | 2 | 跨物种单细胞基础模型，类器官注释与虚拟扰动可用 |
| **UCE** | 模型 | #类器官 #单细胞 | 3600万细胞预训练* | [链接](https://github.com/snap-stanford/UCE) | yes | 2 | 免微调细胞嵌入，类器官衰老demo可作基线表征 |
| **Biomni** | 模型 | #Agent | 25领域数千文献挖掘* |  | unknown | 2 | 通用生物医学智能体，科研工作流与基因优先排序可试 |
| **CellPLM** | 模型 | #单细胞 | 细胞语言模型* |  | unknown | 2 | scEval最佳基础模型之一，类器官单细胞建模候选 |
| **Horvath DNA methylation age clock** | 模型 | #衰老 | 353 CpG* |  | unknown | 2 | 表观遗传衰老基线，类器官衰老demo与队列甲基化建模参照 |
| **Longevity-LLM** | 模型 | #衰老 | 0.6B–9B参数，5个微调模型* | 公开模型 | unknown | 2 | 衰老组学基础模型，可微调做表观年龄与多模态衰老表征 |
| **Reti-CVD** | 模型 | #心血管 | UK Biobank 44,677人验证* |  | unknown | 2 | 视网膜图像CVD评分，多模态风险分层可迁移 |
| **SCORE2-Diabetes** | 模型 | #心血管 | 欧洲T2D 10年CVD风险模型* | [链接](https://doi.org/10.1186/s12933-025-02581-3) | unknown | 2 | T2D专用CVD模型，代谢组增量改进对照 |
| **Speciesformer** | 模型 | #类器官 #单细胞 #虚拟细胞 | 在 1.31 亿细胞上预训练* |  | unknown | 1 | 跨物种虚拟细胞基础模型，直接对标虚拟扰动响应建模基线。 |
| **RegFormer** | 模型 | #单细胞 #世界模型 | 2500万人类细胞预训练* |  | unknown | 1 | 融合GRN先验的扰动预测模型，虚拟扰动建模可迁移 |
| **DNAm PhenoAge** | 模型 | #衰老 | 基于CpG的表观遗传时钟* | [链接](https://doi.org/10.18632/aging.101414) | yes | 1 | 甲基化时钟基线 |
| **Horvath clock** | 模型 | #衰老 | 353 CpG | [链接](https://horvath.genetics.ucla.edu/html/dnamage/) | yes | 1 | DNAm年龄基线时钟，类器官衰老demo必比基线 |
| **I-JEPA** | 模型 | #世界模型 | ViT-Huge/14，ImageNet预训练* | [链接](https://github.com/facebookresearch/ijepa) | yes | 1 | I-JEPA 是自监督表征范式基线，可迁移到类器官图像与组学 |
| **JEPA-DNA** | 模型 | #世界模型 | 多物种基因组基础模型* | [链接](https://github.com/NVIDIA-Digital-Bio/JEPA-DNA) | yes | 1 | JEPA 用于基因组序列，可迁移到虚拟扰动与多组学表征建模 |
| **DunedinPACE** | 模型 | #衰老 |  | [链接](https://github.com/danbelsky/DunedinPACE) | yes | 0 | 衰老速度时钟，类器官与队列衰老评估可用基线 |
| **Enformer** | 模型 |  |  |  | yes | 0 | 序列到表达模型，虚拟扰动与调控建模基线 |
| **GrimAge** | 模型 | #衰老 |  |  | unknown | 0 | 死亡率导向的甲基化时钟基线 |
| **Nucleotide Transformer** | 模型 |  |  | [链接](https://github.com/instadeepai/nucleotide-transformer) | yes | 0 | 跨物种基因组基础模型，类器官跨物种迁移可用 |
| **PhenoAge** | 模型 | #衰老 |  |  | yes | 0 | 血检生物年龄基线，NHANES 可复现 |
| **VCBench** | 基准 | #类器官 #单细胞 #虚拟细胞 | 5个基础模型+4框架7维度* | 污染报告模式与共同标签集协议 | unknown | 1 | 单细胞基础模型评测基准，选型与对标时参照 |
| **scArchon** | 基准 | #单细胞 #虚拟细胞 | 9种工具、多样本数据集* | [链接](https://doi.org/10.1186/s13059-026-04104-z) | unknown | 1 | 扰动预测标准化基准，虚拟扰动建模评测直接可用 |
| **ASSAYBENCH** | 基准 | #虚拟细胞 | 1920个筛选，5类表型* | [链接](https://github.com/Genentech/AssayBench) | yes | 1 | CRISPR表型预测基准，评估智能体虚拟细胞能力 |
| **GenoTEX** | 基准 | #Agent | 含专家标注代码与结果* | [链接](https://github.com/Liu-Hy/GenoTEX) | yes | 1 | 基因表达分析智能体基准，LLM科研工作流直接对标 |
| **TruthInsightBench** | 基准 | #Agent | 40个盲任务，源自10领域40篇研究* | [链接](https://github.com/TruthInsight-stack/TruthInsightBench) | yes | 1 | 科学发现智能体评测，科研智能体工作流可参照 |
| **ARCHS4** | 数据库 | #衰老 | 约5.7万样本，28组织，1-114岁* | [链接](https://maayanlab.cloud/archs4/) | yes | 2 | 跨年龄RNA-seq，转录组衰老时钟训练验证数据 |
| **Human Cell Atlas** | 数据库 | #单细胞 | 全球细胞图谱计划* | [链接](https://data.humancellatlas.org/) | yes | 2 | 细胞图谱资源，类器官衰老demo参照与跨组织整合 |
| **CollecTRI** | 数据库 | #虚拟细胞 | 多物种TF-靶基因网络* | [链接](https://github.com/saezlab/CollecTRI) | yes | 1 | TF调控网络先验，扰动预测带符号系数学习 |
| **Gene Expression Omnibus** | 数据库 | #衰老 | 51项人类干预研究* | [链接](https://www.ncbi.nlm.nih.gov/geo/) | yes | 1 | 取公开DNAm数据评估表观遗传时钟对干预响应 |
| **NHGRI-EBI GWAS Catalog** | 数据库 | #人群队列 | 625,113关联，>85K数据集* | [链接](https://www.ebi.ac.uk/gwas/) | yes | 1 | GWAS汇总统计标准库，ChinaHEART遗传关联查询 |
| **Aging Atlas** | 数据库 | #衰老 |  | [链接](https://ngdc.cncb.ac.cn/aging/) | yes | 0 | 衰老多组学聚合，类器官衰老demo注释与特征来源 |
| **ClockBase** | 数据库 | #衰老 |  |  | unknown | 0 | 甲基化时钟基准平台，衰老建模评估直接对标 |
| **DepMap** | 数据库 | #虚拟细胞 |  | [链接](https://depmap.org/portal/) | yes | 0 | 癌细胞系依赖药敏，虚拟细胞扰动建模参照 |
| **EWAS Atlas** | 数据库 | #衰老 |  | [链接](https://ngdc.cncb.ac.cn/ewas/atlas) | yes | 0 | 甲基化关联库，衰老表观建模与EWAS迁移参照 |
| **HuBMAP** | 数据库 | #单细胞 |  | [链接](https://portal.hubmapconsortium.org/) | yes | 0 | 人体单细胞空间图谱，类器官与空转建模参照 |
| **recount3** | 数据库 |  |  | [链接](https://rna.recount.bio/) | yes | 0 | 统一重处理RNA-seq，跨队列表达整合可直接用 |
| **Single Cell Portal** | 数据库 | #单细胞 |  | [链接](https://singlecell.broadinstitute.org/) | yes | 0 | Broad单细胞数据集，类器官demo数据来源 |
| **Olink** | 工具 | #心血管 #人群队列 | 约3,000-5,000蛋白* | [链接](https://www.olink.com/) | commercial | 7 | 蛋白组检测平台，ChinaHEART蛋白组方案参照 |
| **SomaScan** | 工具 | #心血管 #人群队列 | 4877个aptamer* | [链接](https://somalogic.com/) | commercial | 3 | 血浆蛋白组平台，ChinaHEART蛋白组衰老建模参照 |
| **NMR Metabolomics Platform** | 工具 | #心血管 #人群队列 | 250个代谢标志物* | [链接](https://www.nightingalehealth.com/) | unknown | 2 | NMR代谢组平台，ChinaHEART代谢物风险预测可对标 |
| **Perturb-seq** | 工具 | #单细胞 #虚拟细胞 | 约 20 万细胞* |  | unknown | 2 | CRISPR扰动数据，虚拟扰动建模训练与基准 |
| **scvi-tools** | 工具 | #单细胞 | 多模态与单模态整合* | [链接](https://github.com/scverse/scvi-tools) | yes | 2 | 单细胞嵌入经典基线，类器官与虚拟细胞建模对照。 |
| **Trellis** | 工具 | #类器官 | >2500个CRC PDO与CAF* |  | unknown | 2 | 类器官药物响应分析方法，可直接用于类器官扰动响应建模。 |
| **Perturb-FISH** | 工具 | #类器官 #单细胞 | THP1巨噬细胞等，MERFISH+gRNA* | [链接](https://doi.org/10.1016/j.cell.2025.02.012) | unknown | 1 | 空间扰动读取思路，可用于类器官虚拟扰动建模设计 |

## P2 了解即可（68）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **ImageNet-1k** | 数据集 | #世界模型 | 约128万训练图像、1000类* | [链接](https://www.image-net.org/) | unknown | 8 | 用于线性评估或冻结探针评估自监督图像/视频表征。 |
| **FinnGen** | 数据集 | #衰老 #人群队列 | 224,737人 / 1,932终点* | [链接](https://www.finngen.fi/) | unknown | 6 | 用于分析编码变异对疾病的单等位与双等位效应及隐性关联扫描。 |
| **Cardiovascular Health Study** | 数据集 | #心血管 #衰老 | 5,888 人（65 岁以上） | [链接](https://chs-nhlbi.org/) | controlled | 4 | 作为外部验证队列，评估ECG-AI估计左房结构与功能及预测心血管结局的能力。 |
| **ModelNet40** | 数据集 | #世界模型 | 40类三维模型* | [链接](https://modelnet.cs.princeton.edu/) | unknown | 4 | 用于点云自监督方法的线性分类与少样本分类评估。 |
| **Mass General Brigham Biobank** | 数据集 | #心血管 #人群队列 | 约5.3万（670例狭窄/52,636对照）* | [链接](https://www.massgeneralbrigham.org/en/research/brigham-biobank) | unknown | 3 | 作为三个生物库之一用于ALADYNOULLI贝叶斯框架的EHR与遗传发现。 |
| **MATH** | 数据集 | #Agent | 1.25万题* | [链接](https://github.com/hendrycks/math) | yes | 3 | 评估数学推理能力，DeepSeekMath达51.7%。 |
| **BioBank Japan** | 数据集 | #心血管 #人群队列 | 第一期约 20 万患者（47 种疾病） | [链接](https://biobankjp.org/) | controlled | 2 | 用于日本房颤GWAS发现及与欧洲队列跨祖先荟萃分析，构建跨祖先PRS。 |
| **GSM8K** | 数据集 | #Agent #世界模型 | 约8500道小学数学题* | [链接](https://github.com/openai/grade-school-math) | yes | 2 | 用于评测MASPRM在多智能体推理任务上的表现。 |
| **MIMIC-IV** | 数据集 | #心血管 #人群队列 | 大规模ICU患者数据库* | [链接](https://physionet.org/content/mimiciv/) | controlled | 2 | 用于ECG-FM预训练与基准评测的重症监护ECG数据来源之一。 |
| **23andMe** | 数据集 | #人群队列 | 大规模消费者队列* | [链接](https://www.23andme.com/) | unknown | 2 | 作为疾病不可知队列之一用于跨表型PheWAS药物靶点验证。 |
| **AMC23** | 数据集 | #Agent | 40题* | [链接](https://huggingface.co/datasets/AI-MO/aimo-validation-amc) | unknown | 2 | 用于评测PURE方法在数学竞赛题上的推理性能。 |
| **ELSA-Brasil** | 数据集 | #心血管 | 13,454人* | [链接](https://www.elsa.org.br/) | unknown | 2 | 用于评估噪声单导联ECG AI模型对新发心衰风险的社区人群分层能力。 |
| **ESTHER cohort** | 数据集 | #心血管 | 5578人（含1039例T2D）* |  | unknown | 2 | 代谢组CVD外部验证队列，受限，仅作迁移参照。 |
| **Genecorpus-30M** | 数据集 | #单细胞 | 约3000万细胞* | 论文/公开语料库（Geneformer预训练语料） | unknown | 2 | Geneformer的预训练语料，用于自监督学习网络动力学。 |
| **JetClass** | 数据集 | #世界模型 | 1亿个喷注* | 项目网站公开 | unknown | 2 | 用于预训练HEP-JEPA高能物理基础模型并评估top tagging等下游任务。 |
| **Penn Medicine BioBank** | 数据集 | #人群队列 | 约4万人* | [链接](https://www.med.upenn.edu/pmbb/) | unknown | 2 | 用于冠心病PRS一致性评估及PAD PRS验证。 |
| **ScanObjectNN** | 数据集 | #世界模型 | 15类真实扫描物体* | [链接](https://hkust-vgd.github.io/scanobjectnn/) | unknown | 2 | 用于评估点云掩码自编码器预训练模型的下游分类性能。 |
| **TCGA** | 数据集 | #类器官 | 泛癌种临床队列* | [链接](https://portal.gdc.cancer.gov/) | partial | 2 | 癌症基因组图谱，用于整合类器官RNA-seq数据及预测临床药物反应。 |
| **ADVANCE** | 数据集 | #心血管 | 约1.1万人* |  | unknown | 1 | T2D心肾并发症试验数据，用于跨祖源PRS预测验证。 |
| **COCO-Stuff** | 数据集 | #世界模型 | 约16.4万图像、172类* | [链接](https://github.com/nightrome/cocostuff) | yes | 1 | 自监督分割数据，与生物应用弱相关 |
| **GSM-Plus** | 数据集 | #Agent | 约1万题* | [链接](https://huggingface.co/datasets/qintongli/GSM-Plus) | yes | 1 | 数学推理评测集，与生物应用弱相关。 |
| **Libri-light** | 数据集 | #世界模型 | 60000小时* | [链接](https://github.com/facebookresearch/libri-light) | yes | 1 | 用于HuBERT在多规模无标注语音数据下的自监督预训练与微调评估。 |
| **PRM800K** | 数据集 | #Agent | 80万步级标签* | [链接](https://github.com/openai/prm800k) | yes | 1 | 用于训练过程奖励模型以支持PURE的最小形式信用分配。 |
| **Qwen3-4B** | 模型 | #Agent | 4B参数* |  | unknown | 3 | 作为TEMPO与PPO/GRPO对比实验的基座模型。 |
| **Qwen3-1.7B** | 模型 | #Agent | 1.7B参数* |  | unknown | 2 | 作为S-trace选择性资格迹方法的实验基座模型之一。 |
| **Qwen3-8B** | 模型 | #Agent | 8B参数* |  | unknown | 2 | 作为S-trace与GEAR方法的实验基座模型之一。 |
| **AlphaFold** | 模型 | #心血管 | 未明确* | [链接](https://github.com/google-deepmind/alphafold) | yes | 1 | 用于预测ANGPTL4、FN1等关键因果蛋白的结构，辅助功能变异解释。 |
| **BYOL** | 模型 | #世界模型 | ResNet-50，ImageNet线性评估74.3%* | [链接](https://github.com/deepmind/deepmind-research/tree/master/byol) | yes | 1 | 无负样本自监督，表征学习思路储备 |
| **data2vec** | 模型 | #世界模型 | 通用自监督表征模型* | [链接](https://github.com/facebookresearch/fairseq/tree/main/examples/data2vec) | yes | 1 | 作为Audio-JEPA的对比基线。 |
| **ESM-2** | 模型 | #Agent | 未明确* | [链接](https://github.com/facebookresearch/esm) | yes | 1 | Virtual Lab纳米抗体设计流程中用于蛋白质序列建模。 |
| **MAE** | 模型 | #世界模型 | ViT-Huge，ImageNet-1K 87.8%* | [链接](https://github.com/facebookresearch/mae) | yes | 1 | 掩码自编码器视觉自监督预训练模型，可扩展至大ViT。 |
| **MemCalib-RL** | 模型 | #Agent | 基于MemCalib基准训练* | [链接](https://github.com/Quark-Medical/memcalib) | yes | 1 | 记忆校准RL方法，LLM agent储备弱相关 |
| **MoCo** | 模型 | #世界模型 | ResNet-50骨干，ImageNet预训练* | [链接](https://github.com/facebookresearch/moco) | yes | 1 | 提出带队列与动量编码器的对比学习框架，提供预训练视觉表征。 |
| **Qwen2.5-7B** | 模型 | #Agent | 70亿参数* | [链接](https://huggingface.co/Qwen/Qwen2.5-7B) | yes | 1 | 通用LLM基座，科研智能体微调可选。 |
| **Qwen2.5-Math-1.5B** | 模型 | #Agent | 15亿参数* | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-1.5B) | yes | 1 | 小规模数学推理基座，仅作对比实验。 |
| **Qwen2.5-Math-7B** | 模型 | #Agent | 70亿参数* | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-7B) | yes | 1 | 作为PURE方法验证的数学推理基座模型。 |
| **SimCLR** | 模型 | #世界模型 | ResNet-50，ImageNet线性评估76.5%* | [链接](https://github.com/google-research/simclr) | yes | 1 | 对比学习经典框架，自监督表征思路可借鉴 |
| **wav2vec 2.0** | 模型 | #世界模型 | 预训练语音表征模型* | [链接](https://github.com/facebookresearch/fairseq/tree/main/examples/wav2vec) | yes | 1 | 作为Audio-JEPA的对比基线。 |
| **DNABERT-2** | 模型 |  |  | [链接](https://github.com/MAGICS-LAB/DNABERT_2) | yes | 0 | DNA语言模型，序列建模备用 |
| **ALFWorld** | 基准 | #Agent | 多任务文本环境交互轨迹* | [链接](https://alfworld.github.io/) | unknown | 4 | 作为SELAUR智能体强化学习框架的评测环境之一，衡量任务成功率。 |
| **MMLU** | 基准 | #Agent #世界模型 | 1.4万题、57学科* | [链接](https://github.com/hendrycks/test) | unknown | 2 | 用于评测MASPRM在多学科知识推理上的表现。 |
| **COCO** | 基准 | #世界模型 | 约33万图像，80类* | [链接](https://cocodataset.org/) | unknown | 2 | 用于评估自监督预训练在目标检测与分割上的迁移能力。 |
| **ESCALATE Trial** | 基准 | #心血管 | 1,000名45-65岁* | [链接](https://doi.org/10.1016/j.ahj.2023.06.009) | unknown | 2 | PRS+CAC临床实施研究，ChinaHEART迁移可借鉴设计 |
| **ProcessBench** | 基准 | #Agent | 3400条推理路径* | [链接](https://huggingface.co/datasets/Qwen/ProcessBench) | yes | 2 | 用于评测PRM的步级错误检测能力。 |
| **scIB** | 基准 | #单细胞 | 13个整合任务，最多23批次、100万细胞* | [链接](https://doi.org/10.1038/s41592-021-01336-8) | unknown | 2 | 单细胞数据整合工具的标准基准，含14项批次去除与生物变异保留指标。 |
| **WebShop** | 基准 | #Agent | 118万商品、1.2万指令* | [链接](https://webshop-pnlp.github.io/) | unknown | 2 | 作为SELAUR智能体强化学习框架的评测环境之一，衡量任务成功率。 |
| **HumanEval** | 基准 | #Agent | 164个编程问题* | [链接](https://github.com/openai/human-eval) | yes | 1 | 用于评估Reflexion智能体的编码能力，pass@1达91%。 |
| **MemCalib** | 基准 | #Agent | 15000例（13500训练+1500测试）* | [链接](https://github.com/Quark-Medical/memcalib) | yes | 1 | 智能体记忆评测，方法储备了解即可 |
| **NKIBench** | 基准 | #Agent | 来自真实LLM工作负载的Trainium内核，复杂度不一* | [链接](https://github.com/zhang677/AccelOpt) | yes | 1 | 用于评测AccelOpt在AWS Trainium上自主优化AI加速器内核的性能。 |
| **PaperBench** | 基准 | #Agent | 20篇论文，8,316个可评分任务* | [链接](https://github.com/openai/preparedness) | yes | 1 | 评测AI智能体从零复现前沿AI研究的能力。 |
| **PushT** | 基准 | #世界模型 | 推T形块操作任务* | [链接](https://github.com/real-stanford/diffusion_policy) | yes | 1 | 用于评估D-JEPA在机器人操作任务上的动作选择成功率。 |
| **R-Judge** | 基准 | #Agent | 569条交互记录，27类风险场景* | [链接](https://github.com/Lordog/R-Judge) | yes | 1 | 用于评测LLM智能体在交互环境中的安全风险识别能力。 |
| **SKILLMISEVO-BENCH** | 基准 | #Agent | 未明确* | [链接](https://github.com/henrymao2004/misevolve) | yes | 1 | 冻结基准，用于评估技能误演化与SAFEEVOLVE修复效果。 |
| **SKILLMISEVO-GYM** | 基准 | #Agent | 25种配置，各525任务、25回合* | [链接](https://github.com/henrymao2004/misevolve) | yes | 1 | 生命周期感知测试台，用于研究自改进智能体的技能误演化。 |
| **Socratic-PRMBench** | 基准 | #Agent | 2995条缺陷路径* | [链接](https://github.com/Xiang-Li-oss/Socratic-PRMBench) | yes | 1 | 用于系统评测PRM在六种推理模式下的过程错误检测能力。 |
| **VTAB** | 基准 | #世界模型 | 19个视觉任务* | [链接](https://github.com/google-research/task_adaptation) | yes | 1 | 视觉迁移基准，世界模型储备边缘参考 |
| **ENCODE** | 数据库 | #Agent | 132个转录因子* | [链接](https://www.encodeproject.org/) | yes | 1 | 转录因子结合数据，仅用于基序发现评测。 |
| **ArrayExpress** | 数据库 |  |  | [链接](https://www.ebi.ac.uk/biostudies/arrayexpress) | yes | 0 | EBI多组学归档，通用数据源 |
| **CellAge** | 数据库 | #衰老 |  | [链接](https://genomics.senescence.info/cells/) | yes | 0 | 细胞衰老基因集，注释参考 |
| **dbGaP** | 数据库 | #人群队列 |  | [链接](https://www.ncbi.nlm.nih.gov/gap/) | controlled | 0 | 受控访问基因型库，获取门槛高，备用 |
| **EGA** | 数据库 | #人群队列 |  | [链接](https://ega-archive.org/) | controlled | 0 | 受控访问组学档案，备用数据源 |
| **GenAge** | 数据库 | #衰老 |  | [链接](https://genomics.senescence.info/genes/) | yes | 0 | 衰老基因curated集，注释参考 |
| **Human Protein Atlas** | 数据库 |  |  | [链接](https://www.proteinatlas.org/) | yes | 0 | 蛋白表达图谱，注释参考 |
| **MassIVE** | 数据库 |  |  | [链接](https://massive.ucsd.edu/) | yes | 0 | 质谱仓库，蛋白组备用 |
| **Open Genes** | 数据库 | #衰老 |  | [链接](https://open-genes.com/) | yes | 0 | 衰老基因库，注释参考 |
| **Open Targets** | 数据库 |  |  | [链接](https://platform.opentargets.org/) | yes | 0 | 靶点疾病证据聚合，注释参考 |
| **PRIDE** | 数据库 |  |  | [链接](https://www.ebi.ac.uk/pride/) | yes | 0 | 质谱原始数据，蛋白组备用 |
| **SRA** | 数据库 |  |  | [链接](https://www.ncbi.nlm.nih.gov/sra) | yes | 0 | 原始测序归档，通用数据源 |

## 日报新发现（14，未核验）

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

## 单篇提及（405，未进主表）

- 数据集：AASK (African American Study of Kidney Disease and Hypertension)、ADE20K、AIDA v2、AIDHS/SDS、ALSPAC、Age, Gene/Environment Susceptibility (AGES) Study、AudioSet、AudioSet-20K、C3PO、CHOP、CTRP、CeNGEN、Cityscapes、Copenhagen General Population Study、DFTJ、Droid、EPIC-Norfolk、ESC-50、EST-Health-30、EWOC、Estonian Biobank、FEVER、FINRISK、FSD50K、Fenland、Framingham Offspring Study、GIANT Consortium、GSE67752、Geisinger ECG Dataset、Generation Scotland、HEEDB、HM3D v0.2、HotpotQA、HumanST-46M、I-SPY2、INSPIRE-T cohort、ImageNet ILSVRC-2012、Integrated Mega-scale Atlas、Israel 10K、JUMP-MOA、JUMP-lite、Jiangsu Provincial Center for Disease Control and Prevention (JBPCD) Cohort、KORA、Librispeech、Lorenz attractor、Lothian Birth Cohort 1936、MATH500、MGB (Mass General Brigham) ECG Cohort、MGB Biobank、MIMIC、MIMIC-III、MNIST、MODIS、McFarland、Mexico City Prospective Study (MCPS)、Mount Sinai、NLST、NPBBD-Korea、Norman et al. K562 CRISPRa、Nurses' Health Study (NHS)、PRECISE、Pan-UK Biobank GWAS、Perturb-seq genome-scale screen、PerturbReason、Robomimic、Rotterdam Study、SCIPRM70K、SEA-AD、SHIP-START、SHIP-TREND、ST-bank、SaMi-Trop、SciPlex3、Sentinel-1、Sentinel-2、SpatialCorpus-110M、Taiwan Biobank (TWB)、Taiwan Precision Medicine Initiative (TPMI)、TruDiagnostic、UCLA Biobank
- 模型：AB-PRS、AI-HF、AIDE、AIRE (AI-ECG Risk Estimation)、AROMA、ASCVD-IRT、ATM、AURORA、AdaptAge、AlphaEarth、AlphaFold-Multimer、Audio-MAE、BEHRT、BitAge、Bootleg、BrainBeacon、CAME、CARDIAC-FM、CHARGE-AF score、CLM-X、CLOOME、CMAE、CODRP、CTBA、CTransPath、Cell-o1、CellFM、CellFlux、CellFluxRL、CellOT、CellPaintSSL、CellWorld、China-AIHeart、Co-Scientist、CrossJEPA、D-SPIN、D2R2、DINO-WM、DISCO (ECG HFrEF study)、DNAmEMRAge、DamAge、DeepSeek-R1、DeepSeek-R1-Zero、DeepSeekMath 7B、DiRL、ECG-AI、ECG-FM、ECG-LFM、ECM aging clock、EHR-MPC、EHRAgent、EMRAge、ERA、Echo2HF、EpiZoo、EvoScientist、Foresight、Foresight-England、GLAM、GLAM NAV、GOLD BioAge、GPS_Mult (multi-ancestry CAD polygenic score)、GRASP、GeneCompass、GenePT、Graph-JEPA、HEP-JEPA、Hannum DNA methylation age clock、Healthspan Proteomic Score (HPS)、HuBERT、Intuitor、JEPA-Anything、Kimi k1.5、Kosmos、LPAI、LaMamba-Diff、LeJEPA、LeVJEPA、LifeLong Digital Twin、LinAge2
- 基准：ABC-Bench、AI4AI-Bench、AdaJEPA、BIRD、BLADE、Baba in Wonderland、BioDataLab、BioKGBench、BioML-bench、BiomniBench-DA、Cell-Eval、CellBench、CellPuzzles、ComputAgeBench、D4RL、DiscoverPhysics、GSM-HARD、Gaia2、HLE、Hofmarcher et al. bioactivity benchmark、LAB-Bench、LABBench2、LMR-BENCH、LOGIQA、LVIS、LiveCodeBench、MLAgentBench、MMLU-Medical、MedMCQA、MedPRMBench、MedQA、Moshkov et al. Cell Painting benchmark、OfficeQA、PARADIGM-HF、PASCAL VOC、PertEval-scFM、PerturBench、PerturbQA、ProteinGym、RSIBench-Data、RoboTwin、SEAGym、SWE Bench Verified、SciIntegrity-Bench、ScienceAgentBench、SealQA、SoundnessBench、StreamBench、Systema、Terminal-Bench 2.0、ToolMaker Benchmark、Virtual Cell Challenge 2026、X-ARES、scEval
- 数据库：Allen Brain Atlas、CMAP、CPRD、CPRD Aurum、Cell Landscape、ChIP-Atlas、DISCO (single-cell database)、Danish National Patient Register、Danish National Patient Registry、ELAN、EMBL-EBI ArrayExpress/BioStudies、GeneATLAS、Immunosenescence Inventory、MCATS、MEDICINE portal、PGS Catalog、PhysioNet、Proteome-Phenome Atlas、QResearch database、STP、TEAPEE
- 工具：AccelOpt、AusCVDRisk、AutoPrognosis、BASIL、BOLT-LMM、BioLLM、Biolearn、CHARLS Web-based CVD Risk Calculator、CINEMA-OT、CROP-seq、CellOracle、CellPaint-POSH、CellProfiler、CellScientist、ClockBase Agent、DeGAs、FaithRL、GATK、GEPA、Habitat、Hail、Harmony、ICD-8 to ICD-10 unidirectional mapping、LWD-Miniscope、LivAge、Loki、Longevity Claw、Mortara VERITAS Algorithm、Nahual、OSCAR、PHESANT、PheMIME、PheWeb、Phecodes、REGENIE、Rosetta、SAFEEVOLVE、SAIGE-GENE、SCOPE (Systematic Classification of Organoids for Phenotypic Evaluation)、SCanSNP、SPAC-seq、SPA_GRM、SenePy、SpatialQM、TARDIS、TFActProfiler、TeLLAgent、The AI Scientist、TotalSegmentator、TranslAGE、TreeRL、copairs、leakcheck、moscot、scContam、ukbnmr
