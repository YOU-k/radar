# 资源登记（数据集 / 模型 / 基准）

从 836 处证据引用中挖出资源，并入人工种子与日报新发现，共 567 项；主表 157 项（种子/置顶，或被 ≥2 篇工作使用、或跨方向、或开放且链接核验通过且规模明确），日报新发现 12 项（未核验），其余 398 项单篇提及的列在末尾。开放：yes 公开 / partial 部分 / registration 注册 / controlled 受控 / commercial 商业 / unknown 未确认。核验：ok 内容匹配 / mismatch 页面不是该资源 / blocked 站点拒绝探测 / dead 失效 / n/a 非链接。规模带 * 的取自单篇引用文献。更新 2026-10-04


## P0 优先上手（26）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **UK Biobank** | 数据集 | #衰老 #心血管 #人群队列 | 约 50 万人（40–69 岁入组，2006–10） | [链接](https://www.ukbiobank.ac.uk/) | controlled | 119 | 多组学衰老与CVD方法迁移主数据源，ChinaHEART参照基准 |
| **UK Biobank Pharma Proteomics Project** | 数据集 | #心血管 #人群队列 #衰老 | 约 5.4 万人 · 约 2,900 蛋白 | [链接](https://www.ukbiobank.ac.uk/) | controlled | 11 | UKB蛋白组，ChinaHEART蛋白组CVD风险迁移参照 |
| **China Kadoorie Biobank** | 数据集 | #衰老 #心血管 #人群队列 | 约 51 万成人（10 个地区，2004–08 入组） | [链接](https://www.ckbiobank.org/) | controlled | 10 | 中国人群参照队列，ChinaHEART 迁移时的对照 |
| **Tahoe-100M** | 数据集 | #单细胞 #虚拟细胞 | 1亿转录组，50细胞系，1100药物条件* | [链接](https://huggingface.co/datasets/tahoebio/Tahoe-100M) | yes | 4 | 亿级药物扰动图谱，虚拟扰动预训练与类器官demo核心数据 |
| **UK Biobank Olink Proteomics** | 数据集 | #人群队列 | 5.4万人，2923蛋白* | [链接](https://www.ukbiobank.ac.uk/) | unknown | 3 | UKB蛋白组，ChinaHEART蛋白组迁移与pQTL建模直接参照 |
| **Norman 2019 Perturb-seq** | 数据集 | #单细胞 #虚拟细胞 | 91,205单细胞* | GEO (Norman et al.) | unknown | 2 | 组合扰动基准数据，虚拟扰动响应建模必用基线 |
| **Replogle 2022 Perturb-seq** | 数据集 | #虚拟细胞 | >250万人类细胞，全基因组* | doi:10.1016/j.cell.2022.05.013 | unknown | 2 | 基因组规模Perturb-seq，扰动预测建模与基准评估核心数据 |
| **Adamson Perturb-seq** | 数据集 | #单细胞 #虚拟细胞 | 68,603单细胞* | GEO (Adamson et al.) | unknown | 1 | 扰动scRNA基准数据，虚拟扰动建模与类器官demo直接可用 |
| **ChinaHEART** | 数据集 | #心血管 #人群队列 | 中国大规模心血管病筛查/早筛队列 |  | controlled | 1 | 目标队列：UKB 等公共队列方法迁移的落点 |
| **Pan-UK Biobank** | 数据集 | #人群队列 | 7,271表型，多祖源* | [链接](https://pan.ukbb.broadinstitute.org/) | yes | 1 | 跨祖源GWAS汇总，ChinaHEART迁移与PRS跨人群校正 |
| **LINCS L1000** | 数据集 | #虚拟细胞 |  | [链接](https://clue.io/) | registration | 0 | 虚拟扰动建模的转录组扰动基线，类器官扰动响应可对标 |
| **scGPT** | 模型 | #类器官 #单细胞 #虚拟细胞 | 预训练超3300万细胞* | [链接](https://github.com/bowang-lab/scGPT) | yes | 18 | 单细胞基础模型基线，类器官衰老demo与虚拟扰动对标 |
| **Geneformer** | 模型 | #衰老 #单细胞 #虚拟细胞 | 约3000万细胞预训练* | [链接](https://huggingface.co/ctheodoris/Geneformer) | yes | 13 | 单细胞基础模型基线，类器官衰老demo与虚拟扰动建模直接对标 |
| **scFoundation** | 模型 | #单细胞 #虚拟细胞 | 预训练单细胞基础模型* | [链接](https://github.com/biomap-research/scFoundation) | yes | 7 | 扰动预测基准模型，类器官扰动demo可直接部署对比 |
| **Tahoe-X1** | 模型 | #单细胞 #虚拟细胞 | 1.3B 参数* | 公开预训练权重、训练代码和评估流程 | unknown | 3 | 扰动训练单细胞基础模型，虚拟扰动响应建模首选基线 |
| **China-PAR** | 模型 | #心血管 | 推导21320人，验证84961人* | [链接](https://doi.org/10.1161/CIRCULATIONAHA.116.022367) | yes | 3 | 中国人群传统评分基线，ChinaHEART 模型必须对标 |
| **Chreode** | 模型 | #单细胞 #虚拟细胞 | 240万细胞小鼠胚胎图谱预训练* |  | unknown | 2 | 细胞世界模型，虚拟扰动响应与类器官时序建模直接参照 |
| **SCALE** | 模型 | #单细胞 #虚拟细胞 | CRISPR/化学/发育/免疫* | arXiv:2603.17380v3 | unknown | 1 | 条件传输虚拟扰动模型，类器官扰动响应建模直接可用 |
| **ALADYNOULLI** | 模型 | #人群队列 #心血管 | 68.3万人、348种疾病* |  | unknown | 1 | 生成式疾病轨迹的对标基线（可解释） |
| **Delphi-2M** | 模型 | #人群队列 #心血管 | UKB 约 40 万人训练 + 丹麦 190 万人验证 · 1000+ 病种 |  | unknown | 1 | 生成式疾病轨迹的对标基线 |
| **Pooled Cohort Equations** | 模型 | #心血管 | 多族裔/祖源人群验证* |  | yes | 1 | 心血管风险预测的传统评分基线 |
| **Virtual Cell Challenge** | 基准 | #单细胞 #虚拟细胞 | 反复举办的开放竞赛* | Arc Institute | unknown | 1 | 虚拟扰动响应基准，类器官/细胞虚拟扰动建模直接对标 |
| **LongevityBench** | 基准 | #衰老 | 17任务/5数据域/18个AI系统* | [链接](https://doi.org/10.1016/j.cell.2026.08.026) | unknown | 1 | 衰老 AI 基准（Cell 2026），模型评测对标 |
| **CELLxGENE** | 数据库 | #衰老 #单细胞 | 超7000万细胞* | [链接](https://cellxgene.cziscience.com/) | yes | 1 | 单细胞图谱，训练类器官/单细胞衰老时钟的公开数据 |
| **scPerturb** | 数据库 | #虚拟细胞 |  |  | yes | 0 | 单细胞扰动聚合，直接用于类器官虚拟扰动响应建模 |
| **Cell Painting** | 工具 | #衰老 #单细胞 | 多通道荧光形态图谱* | [链接](https://doi.org/10.1038/s41592-024-02528-8) | unknown | 2 | 细胞形态扰动响应，类器官+cell painting扰动建模核心 |

## P1 值得登记（66）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **All of Us Research Program** | 数据集 | #心血管 #人群队列 | 目标 100 万人（美国，多族裔） | [链接](https://www.researchallofus.org/) | controlled | 11 | 多血统EHR+基因组，PRS与EHR关联复制方法参照 |
| **ARIC** | 数据集 | #心血管 #人群队列 | 约 1.6 万人（1987–89 入组） | [链接](https://aric.cscc.unc.edu/) | controlled | 6 | 蛋白组心衰/衰弱队列，ChinaHEART蛋白组参照 |
| **Framingham Heart Study** | 数据集 | #衰老 #心血管 | 10,097人/28,151份ECG* | [链接](https://www.framinghamheartstudy.org/) | controlled | 3 | ECG-AF深度学习经典队列，心血管AI模型对标 |
| **MESA** | 数据集 | #心血管 #人群队列 | 6,814 人（45–84 岁，四个族裔） | [链接](https://www.mesa-nhlbi.org/) | controlled | 3 | 多模态CVD队列，心血管基础模型外部验证 |
| **UK Biobank Exome Sequencing** | 数据集 | #人群队列 | 45.5万人，1230万变异* | [链接](https://www.ukbiobank.ac.uk/) | unknown | 3 | UKB外显子数据，ChinaHEART遗传-多组学整合方法迁移参照。 |
| **CHARGE-AF Consortium** | 数据集 | #心血管 | 推导18,556例、验证7,672例（5队列）* | [链接](https://www.chargeconsortium.com/) | unknown | 2 | 房颤风险评分基准，ChinaHEART心血管预测可参照 |
| **CHARLS** | 数据集 | #心血管 #人群队列 #衰老 | 8,080名≥45岁* | [链接](https://charls.pku.edu.cn/) | registration | 2 | 中国队列，ChinaHEART迁移与AI-ECG外部验证 |
| **Global Biobank Meta-analysis Initiative (GBMI)** | 数据集 | #人群队列 | 23库，220万人，14疾病* | [链接](https://www.globalbiobankmeta.org/) | unknown | 2 | 跨库荟萃资源，跨祖源PRS评估方法参照 |
| **THL Biobank** | 数据集 | #人群队列 | 参与三国生物库70万人* | [链接](https://thl.fi/en/web/thl-biobank) | unknown | 2 | NMR代谢组重复验证队列，ChinaHEART代谢标志物外部参照 |
| **SpeciesCorpus** | 数据集 | #类器官 #单细胞 #虚拟细胞 | 1.31亿细胞* |  | unknown | 1 | 跨物种单细胞语料，可预训练虚拟细胞模型支撑类器官与扰动。 |
| **CODE-15%** | 数据集 | #心血管 | 约 34.6 万份心电 / 23.4 万患者 | [链接](https://zenodo.org/records/4916206) | yes | 1 | 大规模ECG公开数据，ECG基础模型预训练验证 |
| **MIMIC-IV-ECG** | 数据集 | #心血管 | 大规模ICU ECG* | [链接](https://physionet.org/content/mimic-iv-ecg/) | yes | 1 | 80万ECG公开数据，可预训练ECG基础模型用于心血管队列。 |
| **NHANES** | 数据集 | #衰老 #人群队列 | 每两年约 1 万人（美国代表性样本） | [链接](https://www.cdc.gov/nchs/nhanes/) | yes | 1 | 外部验证衰老时钟对死亡风险捕捉，可作ChinaHEART迁移参照 |
| **Tabula Sapiens** | 数据集 | #单细胞 | 564,253 细胞* |  | unknown | 1 | 多供体单细胞图谱，可作类器官与虚拟细胞表征基准。 |
| **Cell Painting Gallery** | 数据集 | #类器官 |  | [链接](https://github.com/broadinstitute/cellpainting-gallery) | yes | 0 | cell painting 形态学数据，类器官成像+ML 衰老建模可用 |
| **GTEx** | 数据集 | #衰老 | 约 950 名供体 · 54 个组织（v8） | [链接](https://gtexportal.org/) | partial | 0 | 多组织eQTL参考，人群多组学遗传整合可迁移 |
| **PTB-XL** | 数据集 | #心血管 | 21,799 份心电 / 18,869 人 | [链接](https://physionet.org/content/ptb-xl/) | yes | 0 | 公开心电标注数据，ChinaHEART心血管AI建模可迁移 |
| **SCORE2** | 模型 | #心血管 | 45队列67.8万人建模，25队列113万人验证* | [链接](https://doi.org/10.1093/eurheartj/ehab309) | unknown | 6 | 欧洲CVD风险基线，ChinaHEART模型对标 |
| **PREVENT** | 模型 | #心血管 | 美国人群10年/30年CVD风险* | [链接](https://doi.org/10.1161/CIRCULATIONAHA.123.067626) | unknown | 5 | AHA风险方程，蛋白组评分增量比较基线 |
| **TranscriptFormer** | 模型 | #类器官 #单细胞 #虚拟细胞 | 1.12亿细胞、12物种* |  | unknown | 3 | 跨物种虚拟细胞图谱，虚拟扰动与跨物种迁移参照 |
| **DINOv2** | 模型 | #类器官 #世界模型 | ViT-S/B，小ViT 78.3% k-NN* | [链接](https://github.com/facebookresearch/dinov2) | yes | 3 | 类器官视频自监督特征+药效预测，可直接用于类器官demo |
| **GEARS** | 模型 | #单细胞 #虚拟细胞 |  | github.com/snap-stanford/GEARS | unknown | 3 | 扰动预测可迁移基线，虚拟扰动建模对比方法 |
| **CHARGE-AF** | 模型 | #心血管 | 房颤5年风险预测方程* | [链接](https://www.chargeaf.org/) | unknown | 3 | 房颤风险模型，AI-ECG与蛋白组评分比较基线 |
| **Horvath clock** | 模型 | #衰老 | 353 CpG |  | yes | 3 | DNAm年龄基线时钟，类器官衰老demo必比基线 |
| **QRISK3** | 模型 | #心血管 | 英国人群10年CVD风险算法* | [链接](https://qrisk.org/) | unknown | 3 | 英国CVD风险模型，蛋白组增量比较基线 |
| **SCimilarity** | 模型 | #单细胞 | 2270 万细胞、399 项研究* | [链接](https://doi.org/10.1101/2023.07.18.549537) | unknown | 3 | 细胞表示基础模型，跨队列细胞注释与状态查询可用 |
| **CPA** | 模型 | #单细胞 #虚拟细胞 |  | github.com/facebookresearch/CPA | unknown | 2 | 组合扰动自编码器，虚拟扰动预测必对标基线。 |
| **LucaCell** | 模型 | #类器官 #单细胞 | 8500万人/鼠单细胞预训练* |  | unknown | 2 | 跨物种单细胞基础模型，类器官注释与虚拟扰动可用 |
| **UCE** | 模型 | #类器官 #单细胞 | 3600万细胞预训练* | [链接](https://github.com/snap-stanford/UCE) | yes | 2 | 免微调细胞嵌入，类器官衰老demo可作基线表征 |
| **Biomni** | 模型 | #Agent | 覆盖25个领域工具/数据库/协议* |  | unknown | 2 | 通用生物医学智能体，科研工作流与基因优先排序可试 |
| **CellPLM** | 模型 | #单细胞 | 单细胞基础模型* |  | unknown | 2 | scEval最佳基础模型之一，类器官单细胞建模候选 |
| **Longevity-LLM** | 模型 | #衰老 | 0.6B-9B参数，5个模型* | 公开模型（论文公开） | unknown | 2 | 衰老组学基础模型，可微调做表观年龄与多模态衰老表征 |
| **Reti-CVD** | 模型 | #心血管 | UK Biobank 44,677人验证* |  | unknown | 2 | 视网膜图像CVD评分，多模态风险分层可迁移 |
| **SCORE2-Diabetes** | 模型 | #心血管 | 2型糖尿病专用10年CVD风险模型* | [链接](https://doi.org/10.1186/s12933-025-02581-3) | unknown | 2 | T2D专用CVD模型，代谢组增量改进对照 |
| **Speciesformer** | 模型 | #类器官 #单细胞 #虚拟细胞 | SpeciesCorpus 1.31亿细胞* |  | unknown | 1 | 跨物种虚拟细胞基础模型，直接对标虚拟扰动响应建模基线。 |
| **RegFormer** | 模型 | #单细胞 #世界模型 | 2500 万人类细胞预训练* | [链接](https://doi.org/10.1038/s41467-026-72198-x) | unknown | 1 | 融合GRN先验的扰动预测模型，虚拟扰动建模可迁移 |
| **DNAm PhenoAge** | 模型 | #衰老 | 多CpG表观遗传时钟* |  | yes | 1 | 甲基化时钟基线 |
| **I-JEPA** | 模型 | #世界模型 | ViT-Huge/14* | [链接](https://github.com/facebookresearch/ijepa) | yes | 1 | I-JEPA 是自监督表征范式基线，可迁移到类器官图像与组学 |
| **DunedinPACE** | 模型 | #衰老 |  | [链接](https://github.com/danbelsky/DunedinPACE) | yes | 0 | 衰老速度时钟，类器官衰老demo与时钟对标可用 |
| **Enformer** | 模型 |  |  |  | yes | 0 | 序列到表达预测，多组学整合与变异效应建模可迁移 |
| **GrimAge** | 模型 | #衰老 |  |  | unknown | 0 | 死亡率导向的甲基化时钟基线 |
| **Nucleotide Transformer** | 模型 |  |  | [链接](https://github.com/instadeepai/nucleotide-transformer) | yes | 0 | 跨物种基因组基础模型，模式生物迁移与表征储备 |
| **PhenoAge** | 模型 | #衰老 |  |  | yes | 0 | 血检生物年龄基线，NHANES 可复现 |
| **VCBench** | 基准 | #类器官 #单细胞 #虚拟细胞 | 5个基础模型+线性/KNN基线，7维度* | 污染报告模式与共同标签集协议 | unknown | 1 | 单细胞基础模型评测基准，选型与对标时参照 |
| **scArchon** | 基准 | #单细胞 #虚拟细胞 | 9种工具、多样本扰动数据* | [链接](https://doi.org/10.1186/s13059-026-04104-z) | unknown | 1 | 扰动预测标准化基准，虚拟扰动建模评测直接可用 |
| **ASSAYBENCH** | 基准 | #虚拟细胞 | 1920个筛选，5类表型，每筛选约13826基因* | [链接](https://github.com/Genentech/AssayBench) | yes | 1 | CRISPR表型预测基准，评估智能体虚拟细胞能力 |
| **TruthInsightBench** | 基准 | #Agent | 40个盲任务/10领域/40篇研究* | [链接](https://github.com/TruthInsight-stack/TruthInsightBench) | yes | 1 | 科学发现智能体评测，科研智能体工作流可参照 |
| **MEDICINE portal** | 数据库 | #衰老 #人群队列 | UKBB 274,247人模型* | MEDICINE门户 | unknown | 2 | 多器官代谢组衰老时钟可迁移到类器官衰老demo与ChinaHEART衰老建模。 |
| **ARCHS4** | 数据库 | #衰老 | 约5.7万样本，多组织，1-114岁* | [链接](https://maayanlab.cloud/archs4/) | yes | 2 | 跨年龄RNA-seq，转录组衰老时钟训练验证数据 |
| **Human Cell Atlas** | 数据库 | #单细胞 | 全球细胞图谱计划* | [链接](https://data.humancellatlas.org/) | yes | 2 | 细胞图谱资源，类器官衰老demo参照与跨组织整合 |
| **CollecTRI** | 数据库 | #虚拟细胞 | 文献整合调控网络* | [链接](https://github.com/saezlab/CollecTRI) | yes | 1 | TF调控网络先验，扰动预测带符号系数学习 |
| **Gene Expression Omnibus** | 数据库 | #衰老 | 51项人类干预研究* | [链接](https://www.ncbi.nlm.nih.gov/geo/) | yes | 1 | 取公开DNAm数据评估表观遗传时钟对干预响应 |
| **NHGRI-EBI GWAS Catalog** | 数据库 | #人群队列 | 625,113关联、>85K数据集* | [链接](https://www.ebi.ac.uk/gwas/) | yes | 1 | GWAS汇总统计标准库，ChinaHEART遗传关联查询 |
| **CELLxGENE Census** | 数据库 | #单细胞 |  | [链接](https://chanzuckerberg.github.io/cellxgene-census/) | yes | 0 | 面向ML的单细胞全库，类器官与虚拟细胞训练可用 |
| **ClockBase** | 数据库 | #衰老 |  |  | unknown | 0 | 甲基化时钟基准平台，衰老建模评估可参照 |
| **DepMap** | 数据库 | #虚拟细胞 |  | [链接](https://depmap.org/portal/) | yes | 0 | 细胞系依赖图谱，虚拟细胞扰动建模的参照与特征来源 |
| **HuBMAP** | 数据库 | #单细胞 |  | [链接](https://portal.hubmapconsortium.org/) | yes | 0 | 人体单细胞空间图谱，类器官衰老多模态参照 |
| **Olink** | 工具 | #衰老 #心血管 #人群队列 | 1459-2920种蛋白panel* | [链接](https://www.olink.com/) | commercial | 12 | 蛋白组检测平台，ChinaHEART蛋白组方案参照 |
| **SomaScan** | 工具 | #心血管 #人群队列 | 4,877蛋白* | [链接](https://somalogic.com/) | commercial | 3 | 血浆蛋白组平台，ChinaHEART蛋白组衰老建模参照 |
| **PRS-CS** | 工具 | #心血管 #人群队列 | 贝叶斯PRS方法* | [链接](https://github.com/getian107/PRScs) | yes | 2 | PRS基线方法，ChinaHEART心血管风险建模需对标 |
| **NMR metabolomics platform (Nightingale)** | 工具 | #心血管 | 249种代谢物* | [链接](https://www.nightingalehealth.com/) | unknown | 2 | NMR代谢组平台，ChinaHEART代谢物风险预测可对标 |
| **Olink Proteomics Platform** | 工具 | #心血管 | 多面板（数百至数千蛋白）* | [链接](https://www.olink.com/) | unknown | 2 | 血浆蛋白组平台，器官衰老时钟与风险预测可迁移 |
| **Perturb-seq** | 工具 | #单细胞 #虚拟细胞 | 约 20 万细胞* | [链接](https://doi.org/10.1016/j.cell.2016.11.038) | unknown | 2 | CRISPR扰动数据，虚拟扰动建模训练与基准 |
| **scvi-tools** | 工具 | #单细胞 | 多模态与单模态数据整合* | [链接](https://github.com/scverse/scvi-tools) | yes | 2 | 单细胞嵌入经典基线，类器官与虚拟细胞建模对照。 |
| **Trellis** | 工具 | #类器官 | >2500个CRC PDO与CAF* | [链接](https://doi.org/10.1016/j.cell.2023.11.005) | unknown | 2 | 类器官药物响应分析方法，可直接用于类器官扰动响应建模。 |
| **Perturb-FISH** | 工具 | #类器官 #单细胞 | THP1/hIPSC/异种移植3D组织* | [链接](https://doi.org/10.1016/j.cell.2025.02.012) | unknown | 1 | 空间扰动读取思路，可用于类器官虚拟扰动建模设计 |

## P2 了解即可（65）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **ImageNet-1K** | 数据集 | #世界模型 | 约128万训练图像，1000类* | [链接](https://www.image-net.org/) | unknown | 8 | 作为自监督视觉预训练与线性评估的主基准数据集。 |
| **FinnGen** | 数据集 | #衰老 #人群队列 | 17.7万芬兰人，2,444表型* | [链接](https://www.finngen.fi/) | unknown | 6 | 整合芬兰生物库与全国健康登记，用于疾病GWAS与精细定位。 |
| **Cardiovascular Health Study** | 数据集 | #心血管 #衰老 | 5,888 人（65 岁以上） | [链接](https://chs-nhlbi.org/) | controlled | 4 | 作为外部队列验证ECG-AI模型估计左房结构与功能及预测心血管结局。 |
| **ModelNet40** | 数据集 | #世界模型 | 40类3D CAD模型* | [链接](https://modelnet.cs.princeton.edu/) | unknown | 4 | 用于点云自监督方法的线性分类和少样本学习评估。 |
| **Mass General Brigham Biobank** | 数据集 | #心血管 #人群队列 | 约5.3万例（670例颈动脉狭窄）* | [链接](https://www.massgeneralbrigham.org/en/research/innovation/biobank) | unknown | 3 | 作为三个生物库之一用于ALADYNOULLI贝叶斯框架的EHR与遗传发现。 |
| **MATH** | 数据集 | #Agent | 1.25万道竞赛数学题* | [链接](https://github.com/hendrycks/math) | yes | 3 | 用于评估数学推理能力，DeepSeekMath与TEMPO均在此基准上报告结果。 |
| **BioBank Japan** | 数据集 | #心血管 #人群队列 | 第一期约 20 万患者（47 种疾病） | [链接](https://biobankjp.org/) | controlled | 2 | 用于日本房颤GWAS发现及跨祖先荟萃分析，构建房颤多基因风险评分。 |
| **GSM8K** | 数据集 | #Agent #世界模型 | 小学数学应用题基准* | [链接](https://github.com/openai/grade-school-math) | yes | 2 | 用于评估DLLM-JEPA在数学推理任务上的性能提升。 |
| **MIMIC-IV** | 数据集 | #心血管 #人群队列 | 大规模ICU患者数据库* | [链接](https://physionet.org/content/mimiciv/) | controlled | 2 | 作为MiGHT-EHR多任务图Transformer的预训练与评测数据集。 |
| **23andMe** | 数据集 | #人群队列 | 大规模消费者队列* | [链接](https://www.23andme.com/) | unknown | 2 | 作为疾病不可知队列之一用于PheWAS药物靶点验证。 |
| **AMC23** | 数据集 | #Agent | 2023年AMC竞赛题* | [链接](https://huggingface.co/datasets/AI-MO/aimo-validation-amc) | unknown | 2 | 作为分布外数学推理基准，评估TEMPO的泛化性能。 |
| **COCO** | 数据集 | #世界模型 | 约33万图像，80类* | [链接](https://cocodataset.org/) | unknown | 2 | 用于评估自监督预训练在目标检测与分割上的迁移效果。 |
| **ELSA-Brasil** | 数据集 | #心血管 | 13,454人* | [链接](https://www.elsa.org.br/) | unknown | 2 | 用于评估噪声自适应AI-ECG模型对新发心衰风险的社区人群分层能力。 |
| **ESTHER cohort** | 数据集 | #心血管 | 5578人（含1039例2型糖尿病）* |  | unknown | 2 | 代谢组CVD外部验证队列，受限，仅作迁移参照。 |
| **Genecorpus-30M** | 数据集 | #单细胞 | 约3000万细胞* |  | unknown | 2 | Geneformer的预训练语料，用于审计污染及网络生物学预测预训练。 |
| **JetClass** | 数据集 | #世界模型 | 1亿个喷注* | 项目网站公开 | unknown | 2 | 用于预训练HEP-JEPA高能物理基础模型并评估top tagging等下游任务。 |
| **ScanObjectNN** | 数据集 | #世界模型 | 真实扫描3D物体分类基准* | [链接](https://hkust-vgd.github.io/scanobjectnn/) | unknown | 2 | 用于评估点云掩码自编码器在真实扫描物体分类上的下游泛化。 |
| **TCGA** | 数据集 | #类器官 | 大规模肿瘤队列* | [链接](https://portal.gdc.cancer.gov/) | partial | 2 | 癌症基因组图谱，用于整合类器官RNA-seq及临床药物反应预测验证。 |
| **ADVANCE** | 数据集 | #心血管 | 约1.1万例T2D患者* |  | unknown | 1 | 用于验证MCCP跨祖源多基因风险评分在T2D心肾并发症中的预测可靠性。 |
| **GSM-Plus** | 数据集 | #Agent | 约1万题* | [链接](https://huggingface.co/datasets/qintongli/GSM-Plus) | yes | 1 | 数学推理评测集，与生物应用弱相关。 |
| **Libri-light** | 数据集 | #世界模型 | 60000小时* | [链接](https://github.com/facebookresearch/libri-light) | yes | 1 | 用于大规模无标注语音预训练及多规模微调评估HuBERT。 |
| **PRM800K** | 数据集 | #Agent | 80万步级标签* | [链接](https://github.com/openai/prm800k) | yes | 1 | 用于训练过程奖励模型PRM。 |
| **Qwen3-4B** | 模型 | #Agent | 40亿参数* | Hugging Face: Qwen/Qwen3-4B | unknown | 3 | 用于验证S-trace与GEAR在推理及工具使用任务上的性能。 |
| **Qwen2.5-Math-7B** | 模型 | #Agent | 70亿参数* | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-7B) | yes | 2 | 作为PURE与ScalePRM的基座模型进行推理强化实验。 |
| **Qwen3-1.7B** | 模型 | #Agent | 1.7B参数* | Hugging Face: Qwen/Qwen3-1.7B | unknown | 2 | 用于验证选择性资格迹S-trace在推理任务上的pass@16提升。 |
| **Qwen3-8B** | 模型 | #Agent | 8B参数* |  | unknown | 2 | 用于验证S-trace与GEAR在推理及工具使用任务上的性能。 |
| **AlphaFold** | 模型 | #心血管 | 未明确* | [链接](https://github.com/google-deepmind/alphafold) | yes | 1 | 用于预测ANGPTL4、FN1等关键蛋白变异的结构，辅助功能解释。 |
| **ESM-2** | 模型 | #Agent |  | [链接](https://github.com/facebookresearch/esm) | yes | 1 | Virtual Lab纳米抗体设计流程中用于蛋白质序列建模。 |
| **Graph-JEPA** | 模型 | #世界模型 | 图分类/回归任务* | [链接](https://github.com/geriskenderi/graph-jepa) | yes | 1 | 面向图级表征学习的联合嵌入预测架构模型，用于图分类和回归。 |
| **MAE** | 模型 | #世界模型 | ViT-Huge，约6.3亿参数* | [链接](https://github.com/facebookresearch/mae) | yes | 1 | 掩码自编码器，随机掩码图像块并重建像素的可扩展视觉自监督模型。 |
| **MoCo** | 模型 | #世界模型 | ResNet-50骨干* | [链接](https://github.com/facebookresearch/moco) | yes | 1 | 基于队列与动量编码器的对比学习无监督视觉表征模型。 |
| **Point-JEPA** | 模型 | #世界模型 | ModelNet40 93.7%* | [链接](https://github.com/Ayumu-J-S/Point-JEPA) | yes | 1 | 面向点云的自监督联合嵌入预测架构模型，用于分类和少样本学习。 |
| **Qwen2.5-7B** | 模型 | #Agent | 70亿参数* | [链接](https://huggingface.co/Qwen/Qwen2.5-7B) | yes | 1 | 通用LLM基座，科研智能体微调可选。 |
| **Qwen2.5-Math-1.5B** | 模型 | #Agent | 15亿参数* | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-1.5B) | yes | 1 | 小规模数学推理基座，仅作对比实验。 |
| **SAM (Segment Anything Model)** | 模型 | #类器官 | 通用图像分割大模型* | [链接](https://github.com/facebookresearch/segment-anything) | yes | 1 | 用于PDO延时显微视频中类器官的自动分割。 |
| **DNABERT-2** | 模型 |  |  | [链接](https://github.com/MAGICS-LAB/DNABERT_2) | yes | 0 |  |
| **ALFWorld** | 基准 | #Agent | 6类任务、3500+场景* | [链接](https://alfworld.github.io/) | unknown | 4 | 用于评估MetaSkill-Evolve智能体技能自进化能力的基准之一。 |
| **MMLU** | 基准 | #Agent #世界模型 | 57学科、1.4万题* | [链接](https://github.com/hendrycks/test) | unknown | 2 | 用于评估DLLM-JEPA在多任务语言理解上的性能。 |
| **ProcessBench** | 基准 | #Agent | 3400+条推理步骤* | [链接](https://huggingface.co/datasets/Qwen/ProcessBench) | yes | 2 | 用于评测BiPRM与ScalePRM的步级错误检测能力。 |
| **scIB** | 基准 | #单细胞 | 13任务，最多23批次/100万细胞* |  | unknown | 2 | 单细胞数据整合工具的标准基准，用于评估批次去除与生物变异保留。 |
| **WebShop** | 基准 | #Agent | 118万商品、1.2万指令* | [链接](https://webshop-pnlp.github.io/) | unknown | 2 | 用于评测SELAUR智能体在网页购物任务中的成功率。 |
| **BioML-bench** | 基准 | #Agent | 4个领域任务* | [链接](https://github.com/science-machine/biomlbench) | yes | 1 | 评测AI智能体在蛋白质工程、单细胞组学、成像和药物发现端到端ML任务上的表现。 |
| **HumanEval** | 基准 | #Agent | 164个编程问题* | [链接](https://github.com/openai/human-eval) | yes | 1 | 用于评估Reflexion框架的编码能力，pass@1达91%。 |
| **LOGIQA** | 基准 | #Agent | 约7000题* | [链接](https://huggingface.co/datasets/lucasmccabe/logiqa) | yes | 1 | 逻辑推理基准，与科研智能体弱相关。 |
| **NKIBench** | 基准 | #Agent | 来自真实LLM工作负载的Trainium内核* | [链接](https://github.com/zhang677/AccelOpt) | yes | 1 | 用于评测LLM智能体自主优化AWS Trainium内核的性能。 |
| **PaperBench** | 基准 | #Agent | 20篇论文，8,316个可评分任务* | [链接](https://github.com/openai/preparedness) | yes | 1 | 评测AI智能体从零复现前沿AI研究的能力。 |
| **R-Judge** | 基准 | #Agent | 569条交互记录，27类风险场景* | [链接](https://github.com/Lordog/R-Judge) | yes | 1 | 用于评测LLM智能体在交互环境中的安全风险意识与识别能力。 |
| **Socratic-PRMBench** | 基准 | #Agent | 2995条缺陷推理路径* | [链接](https://github.com/Xiang-Li-oss/Socratic-PRMBench) | yes | 1 | 用于系统评测PRM在六种推理模式下的过程错误检测能力。 |
| **Danish National Patient Registry** | 数据库 | #人群队列 | 1965年至今全国登记* | Danish National Patient Registry | unknown | 2 | 提供丹麦高粒度纵向医疗编码数据用于ICD映射构建。 |
| **ArrayExpress** | 数据库 | #衰老 | 51项人类干预研究* | [链接](https://www.ebi.ac.uk/biostudies/arrayexpress) | yes | 1 | 提供公开DNAm数据用于跨研究表观遗传时钟响应性分析。 |
| **ENCODE** | 数据库 | #Agent | 132个转录因子数据集* | [链接](https://www.encodeproject.org/) | yes | 1 | 转录因子结合数据，仅用于基序发现评测。 |
| **Aging Atlas** | 数据库 | #衰老 |  | [链接](https://ngdc.cncb.ac.cn/aging/) | yes | 0 |  |
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

## 日报新发现（12，未核验）

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

## 单篇提及（398，未进主表）

- 数据集：AASK、ADE20K、AIDA v2、ALSPAC、Age, Gene/Environment Susceptibility (AGES) Study、Asian Indian Diabetes Heart Study / Sikh Diabetes Study (AIDHS/SDS)、AudioSet、AudioSet-20K、CHOP、COCO-Stuff、CPRD、CTRP、CeNGEN、Cityscapes、Common Crawl、Copenhagen General Population Study、DFTJ、Droid、EPIC-Norfolk、ESC-50、EST-Health-30、Estonian Biobank、FEVER、FINRISK、FSD50K、Fenland、Framingham Offspring Study (FOS)、GIANT Consortium、GSE67752、Geisinger ECG Dataset、Generation Scotland、HEEDB、HM3D v0.2、HotpotQA、HumanST-46M、INSPIRE-T、ImageNet ILSVRC-2012、Integrated Mega-scale Atlas、Israeli 10K、JUMP-MOA、JUMP-lite、Jiangsu Provincial Center for Disease Control and Prevention (JBPCD) Cohort、KORA、LVIS、Librispeech、Lorenz、Lothian Birth Cohort 1936、MATH500、MGB Biobank、MIMIC、MIMIC-III、MNIST、MODIS、McFarland、Mexico City Prospective Study (MCPS)、Mount Sinai、NLST、NMR Metabolomics、NPBBD-Korea、Norman et al. K562 CRISPRa、Nurses' Health Study (NHS)、PRECISE、Penn Medicine BioBank (PMBB)、Perturb-seq genome-scale screen、PerturbReason、Replogle Perturb-seq、Replogle Perturb-seq K562、Replogle Perturb-seq RPE1、Robomimic、Rotterdam Study、SCIPRM70K、SEA-AD、SHIP-START、SHIP-TREND、ST-bank、SaMi-Trop、SciPlex3、Sentinel-1、Sentinel-2、SpatialCorpus-110M
- 模型：AB-PRS、AI-HF、AIDE、AIRE、AROMA、ASCVD-IRT、ATM、AURORA、AdaptAge、AlphaEarth、AlphaFold-Multimer、Audio-MAE、BEHRT、BYOL、Bootleg、BrainBeacon、CAME、CARDIAC-FM、CLM-X、CLOOME、CMAE、CODRP、CTBA、CTransPath、Cell-o1、CellFM、CellFlux、CellFluxRL、CellOT、CellPaintSSL、CellWorld、China-AIHeart、CrossJEPA、D-SPIN、D2R2、DINO-WM、DISCO (ECG HFrEF study)、DNAmEMRAge、DamAge、DeepSeek-R1、DeepSeekMath 7B、DiRL、ECG-AI、ECG-AI AF model、ECG-FM、ECG-LFM、ECG2CAD、ECG2Stroke、ECM aging clock、EHR-MPC、EHRAgent、EMRAge、ERA、Echo2HF、EpiZoo、EvoScientist、Foresight、Foresight-England、Framingham Risk Score (FRS)、GLAM、GOLD BioAge、GPS_Mult、GRASP、GeneCompass、GenePT、HEP-JEPA、HPS、Hannum DNAm Age Clock、HuBERT、Intuitor、JEPA-Anything、JEPA-DNA、Kimi k1.5、LaMamba-Diff、LeJEPA、LeVJEPA、LinAge2、Longitudinal Proteomic Aging Index (LPAI)、MC-JEPA、MILTON
- 基准：ABC-Bench、AI4AI-Bench、AdaJEPA、BIRD、BLADE、Baba in Wonderland、BioDataLab、BioKGBench、BiomniBench-DA、Cell-Eval、CellBench、CellPuzzles、ComputAgeBench、D4RL、DiscoverPhysics、GSM-HARD、Gaia2、GenoTEX、HLE、Hofmarcher et al. bioactivity benchmark、LAB-Bench、LABBench2、LMR-BENCH、LiveCodeBench、MLAgentBench、MMLU-Medical、MedMCQA、MedPRMBench、MedQA、MemCalib、Moshkov et al. Cell Painting benchmark、OfficeQA、PASCAL VOC、PertEval-scFM、PerturBench、PerturbQA、ProteinGym、PushT、RSIBench-Data、RoboTwin、SEAGym、SKILLMISEVO-BENCH、SKILLMISEVO-GYM、SWE Bench Verified、SciIntegrity-Bench、ScienceAgentBench、SealQA、SoundnessBench、StreamBench、Systema、Terminal-Bench 2.0、ToolMaker Benchmark、VTAB、Virtual Cell Challenge 2026、X-ARES、scEval
- 数据库：Allen Brain Atlas、CMAP、CPRD Aurum、Cell Landscape、ChIP-Atlas、DISCO (single-cell database)、ELAN、GeneATLAS、Immunosenescence Inventory、MCATS、PGS Catalog、PhysioNet、Plasma Proteome-Phenome Atlas、QResearch、STP、TEAPEE
- 工具：AccelOpt、AnnoPred、AusCVDRisk、AutoPrognosis、BASIL、BOLT-LMM、BioLLM、Biolearn、CINEMA-OT、CROP-seq、CellOracle、CellPaint-POSH、CellProfiler、CellScientist、Cliff、ClockBase Agent、DeGAs、FaithRL、GEPA、Habitat、Harmony、ICD-8 to ICD-10 unidirectional mapping、K-Dense、LDpred、LWD-Miniscope、LivAge、Loki、Longevity Claw、Mortara VERITAS Algorithm、Mosaic、Nahual、OSCAR、P+T (Pruning and Thresholding)、PHESANT、PheMIME、PheWeb、Phecodes、Rosetta、SAFEEVOLVE、SCOPE (Systematic Classification of Organoids for Phenotypic Evaluation)、SCanSNP、SPAC-seq、SPA_GRM、STREME、SenePy、SpatialQM、TARDIS、TFActProfiler、TeLLAgent、The AI Scientist、TotalSegmentator、TranslAGE、associationSubgraphs、copairs、leakcheck、moscot、scContam、ukbnmr
