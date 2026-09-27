# 资源登记（数据集 / 模型 / 基准）

从 777 处证据引用中挖出资源，并入人工种子与日报新发现，共 536 项；主表 155 项（种子/置顶，或被 ≥2 篇工作使用、或跨方向、或开放且链接核验通过且规模明确），日报新发现 8 项（未核验），其余 373 项单篇提及的列在末尾。开放：yes 公开 / partial 部分 / registration 注册 / controlled 受控 / commercial 商业 / unknown 未确认。核验：ok 内容匹配 / mismatch 页面不是该资源 / blocked 站点拒绝探测 / dead 失效 / n/a 非链接。规模带 * 的取自单篇引用文献。更新 2026-09-27


## P0 优先上手（20）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **UK Biobank** | 数据集 | #衰老 #心血管 #人群队列 | 约 50 万人（40–69 岁入组，2006–10） | [链接](https://www.ukbiobank.ac.uk/) | controlled | 112 | 多组学衰老与CVD方法迁移主数据源，ChinaHEART参照基准 |
| **UK Biobank Pharma Proteomics Project** | 数据集 | #心血管 #人群队列 #衰老 | 约 5.4 万人 · 约 2,900 蛋白 | [链接](https://www.ukbiobank.ac.uk/) | controlled | 12 | UKB蛋白组，ChinaHEART蛋白组CVD风险迁移参照 |
| **China Kadoorie Biobank** | 数据集 | #衰老 #心血管 #人群队列 | 约 51 万成人（10 个地区，2004–08 入组） | [链接](https://www.ckbiobank.org/) | controlled | 8 | 中国人群参照队列，ChinaHEART 迁移时的对照 |
| **Tahoe-100M** | 数据集 | #单细胞 #虚拟细胞 | 1亿转录组，50细胞系，1100药物条件* | [链接](https://huggingface.co/datasets/tahoebio/Tahoe-100M) | yes | 4 | 亿级药物扰动图谱，虚拟扰动预训练与类器官demo核心数据 |
| **Pan-UK Biobank** | 数据集 | #人群队列 | 7266个性状，多祖源* | [链接](https://pan.ukbb.broadinstitute.org/) | yes | 2 | 跨祖源GWAS汇总，ChinaHEART迁移与PRS跨人群校正 |
| **Replogle 2022 Perturb-seq** | 数据集 | #虚拟细胞 | >250万人类细胞* | [链接](https://doi.org/10.1016/j.cell.2022.05.013) | unknown | 2 | 基因组规模Perturb-seq，扰动预测建模与基准评估核心数据 |
| **ChinaHEART** | 数据集 | #心血管 #人群队列 | 中国大规模心血管病筛查/早筛队列 |  | controlled | 1 | 目标队列：UKB 等公共队列方法迁移的落点 |
| **scGPT** | 模型 | #类器官 #单细胞 #虚拟细胞 | 预训练于3300万+细胞* | [链接](https://github.com/bowang-lab/scGPT) | yes | 14 | 单细胞基础模型基线，类器官衰老demo与虚拟扰动对标 |
| **Geneformer** | 模型 | #单细胞 #虚拟细胞 | V2-316M，约316M参数* | [链接](https://huggingface.co/ctheodoris/Geneformer) | yes | 10 | 单细胞基础模型基线，类器官衰老demo与虚拟扰动建模直接对标 |
| **scFoundation** | 模型 | #单细胞 #虚拟细胞 | 大规模单细胞预训练模型* | [链接](https://github.com/biomap-research/scFoundation) | yes | 5 | 扰动预测基准模型，类器官扰动demo可直接部署对比 |
| **China-PAR** | 模型 | #心血管 | 推导21320人，验证84961人* | [链接](https://doi.org/10.1161/CIRCULATIONAHA.116.022367) | yes | 4 | 中国人群传统评分基线，ChinaHEART 模型必须对标 |
| **Tahoe-X1** | 模型 | #单细胞 | 最高30亿参数* | 公开预训练权重、训练代码和评估流程 | unknown | 3 | 扰动训练单细胞基础模型，虚拟扰动响应建模首选基线 |
| **Chreode** | 模型 | #单细胞 #虚拟细胞 | 240万细胞小鼠胚胎图谱预训练* | [链接](https://arxiv.org/abs/2605.28111v1) | unknown | 2 | 细胞世界模型，虚拟扰动响应与类器官时序建模直接参照 |
| **SCALE** | 模型 | #单细胞 #虚拟细胞 | CRISPR/化学/发育/免疫* | [链接](https://arxiv.org/abs/2603.17380v3) | unknown | 1 | 条件传输虚拟扰动模型，类器官扰动响应建模直接可用 |
| **ALADYNOULLI** | 模型 | #人群队列 #心血管 | 68.3万人，348种疾病* |  | unknown | 1 | 生成式疾病轨迹的对标基线（可解释） |
| **Delphi-2M** | 模型 | #人群队列 #心血管 | UKB 约 40 万人训练 + 丹麦 190 万人验证 · 1000+ 病种 |  | unknown | 1 | 生成式疾病轨迹的对标基线 |
| **Pooled Cohort Equations** | 模型 | #心血管 | 多族裔验证* |  | yes | 1 | 心血管风险预测的传统评分基线 |
| **LongevityBench** | 基准 | #衰老 | 17项任务/5个数据域* | [链接](https://doi.org/10.1016/j.cell.2026.08.026) | unknown | 2 | 衰老 AI 基准（Cell 2026），模型评测对标 |
| **CELLxGENE** | 数据库 | #衰老 #单细胞 | 超7000万细胞* | [链接](https://cellxgene.cziscience.com/) | yes | 1 | 单细胞图谱，训练类器官/单细胞衰老时钟的公开数据 |
| **Cell Painting** | 工具 | #衰老 #单细胞 | 图像型profiling数据（十年积累）* | [链接](https://doi.org/10.1038/s41592-024-02528-8) | unknown | 3 | 细胞形态扰动响应，类器官+cell painting扰动建模核心 |

## P1 值得登记（46）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **All of Us Research Program** | 数据集 | #人群队列 | 目标 100 万人（美国，多族裔） | [链接](https://www.researchallofus.org/) | controlled | 10 | 多血统EHR+基因组，PRS与EHR关联复制方法参照 |
| **ARIC** | 数据集 | #心血管 #人群队列 | 约 1.6 万人（1987–89 入组） | [链接](https://www2.cscc.unc.edu/aric/) | controlled | 6 | 蛋白组心衰/衰弱队列，ChinaHEART蛋白组参照 |
| **Cardiovascular Health Study** | 数据集 | #心血管 #衰老 | 5,888 人（65 岁以上） | [链接](https://chs-nhlbi.org/) | controlled | 4 | 老年CVD队列，ECG-AI心血管结局外部验证 |
| **Framingham Heart Study** | 数据集 | #衰老 #心血管 | 10,097人，28,151份ECG* | [链接](https://www.framinghamheartstudy.org/) | controlled | 3 | ECG-AF深度学习经典队列，心血管AI模型对标 |
| **MESA** | 数据集 | #心血管 #人群队列 | 6,814 人（45–84 岁，四个族裔） | [链接](https://www.mesa-nhlbi.org/) | controlled | 3 | 多模态CVD队列，心血管基础模型外部验证 |
| **CHARLS** | 数据集 | #心血管 #人群队列 #衰老 | 约23,000人 / 9年随访* | [链接](https://charls.pku.edu.cn/) | registration | 2 | 中国队列，ChinaHEART迁移与AI-ECG外部验证 |
| **Global Biobank Meta-analysis Initiative (GBMI)** | 数据集 | #人群队列 | 23库，220万人，14疾病* | [链接](https://www.globalbiobankmeta.org/) | unknown | 2 | 跨库荟萃资源，跨祖源PRS评估方法参照 |
| **THL Biobank** | 数据集 | #人群队列 | 三国生物库共700,217人* | [链接](https://thl.fi/en/web/thl-biobank) | unknown | 2 | NMR代谢组重复验证队列，ChinaHEART代谢标志物外部参照 |
| **CODE-15%** | 数据集 | #心血管 | 约 34.6 万份心电 / 23.4 万患者 | [链接](https://zenodo.org/records/4916206) | yes | 1 | 大规模ECG公开数据，ECG基础模型预训练验证 |
| **SCORE2** | 模型 | #心血管 | 欧洲10年CVD风险模型* | [链接](https://doi.org/10.1093/eurheartj/ehab309) | unknown | 5 | 欧洲CVD风险基线，ChinaHEART模型对标 |
| **DINOv2** | 模型 | #类器官 #世界模型 | ViT-Base线性评估80.1%* | [链接](https://github.com/facebookresearch/dinov2) | yes | 3 | 类器官视频自监督特征+药效预测，可直接用于类器官demo |
| **GEARS** | 模型 | #单细胞 #虚拟细胞 | 图神经网络模型* |  | unknown | 3 | 扰动预测可迁移基线，虚拟扰动建模对比方法 |
| **TranscriptFormer** | 模型 | #类器官 #单细胞 | 1.12亿细胞、12物种、15.3亿年进化* |  | unknown | 3 | 跨物种虚拟细胞图谱，虚拟扰动与跨物种迁移参照 |
| **CHARGE-AF** | 模型 | #心血管 | 房颤风险预测* | [链接](https://www.chargeconsortium.com/) | unknown | 3 | 房颤风险模型，AI-ECG与蛋白组评分比较基线 |
| **Horvath clock** | 模型 | #衰老 | 353 CpG |  | yes | 3 | DNAm年龄基线时钟，类器官衰老demo必比基线 |
| **PREVENT** | 模型 | #心血管 | 美国AHA 10年CVD风险方程* | [链接](https://doi.org/10.1161/CIRCULATIONAHA.123.067626) | unknown | 3 | AHA风险方程，蛋白组评分增量比较基线 |
| **QRISK3** | 模型 | #心血管 | QResearch 1998-2015队列* | [链接](https://qrisk.org/) | unknown | 3 | 英国CVD风险模型，蛋白组增量比较基线 |
| **SCimilarity** | 模型 | #单细胞 | 2270 万细胞，399 项研究* |  | unknown | 3 | 细胞表示基础模型，跨队列细胞注释与状态查询可用 |
| **SCORE2-Diabetes** | 模型 | #心血管 | T2D专用CVD风险模型* | [链接](https://doi.org/10.1093/eurheartj/ehad260) | unknown | 3 | T2D专用CVD模型，代谢组增量改进对照 |
| **DISCO (ECG HFrEF study)** | 模型 | #心血管 #虚拟细胞 | HFrEF真实世界队列（规模未明确）* | [链接](https://www.immunesinglecell.org) | unknown | 2 | ECG嵌入表型匹配，虚拟扰动与治疗效应模拟思路 |
| **UCE** | 模型 | #类器官 #单细胞 | 3600万细胞预训练* | [链接](https://github.com/snap-stanford/UCE) | yes | 2 | 免微调细胞嵌入，类器官衰老demo可作基线表征 |
| **CellPLM** | 模型 | #单细胞 | 预训练模型* |  | unknown | 2 | scEval最佳基础模型之一，类器官单细胞建模候选 |
| **Longevity-LLM** | 模型 | #衰老 | 0.6B-9B参数，5个模型* | [链接](https://doi.org/10.1016/j.cell.2026.08.026) | unknown | 2 | 衰老组学基础模型，可微调做表观年龄与多模态衰老表征 |
| **Reti-CVD** | 模型 | #心血管 | UK Biobank 44,677人验证* |  | unknown | 2 | 视网膜图像CVD评分，多模态风险分层可迁移 |
| **RegFormer** | 模型 | #单细胞 #世界模型 | 2500万人类细胞预训练* |  | unknown | 1 | 融合GRN先验的扰动预测模型，虚拟扰动建模可迁移 |
| **DNAm PhenoAge** | 模型 | #衰老 | 基于CpG的表观遗传时钟* |  | yes | 1 | 甲基化时钟基线 |
| **GET** | 模型 | #虚拟细胞 | 大规模单细胞预训练* | [链接](https://github.com/GET-Foundation/get_model) | yes | 1 | 代表性虚拟细胞基础模型，扰动建模对标 |
| **I-JEPA** | 模型 | #世界模型 | ViT-Huge/14，16张A100训练<72h* | [链接](https://github.com/facebookresearch/ijepa) | yes | 1 | I-JEPA 是自监督表征范式基线，可迁移到类器官图像与组学 |
| **JEPA-DNA** | 模型 | #世界模型 | 多物种基因组基础模型* | [链接](https://github.com/NVIDIA-Digital-Bio/JEPA-DNA) | yes | 1 | JEPA 用于基因组序列，可迁移到虚拟扰动与多组学表征建模 |
| **GrimAge** | 模型 | #衰老 |  |  | unknown | 0 | 死亡率导向的甲基化时钟基线 |
| **PhenoAge** | 模型 | #衰老 |  |  | yes | 0 | 血检生物年龄基线，NHANES 可复现 |
| **scArchon** | 基准 | #单细胞 #虚拟细胞 | 9种工具，多样本扰动数据* | [链接](https://doi.org/10.1186/s13059-026-04104-z) | unknown | 1 | 扰动预测标准化基准，虚拟扰动建模评测直接可用 |
| **VCBench** | 基准 | #类器官 #单细胞 | 5个基础模型、5个可测维度* |  | unknown | 1 | 单细胞基础模型评测基准，选型与对标时参照 |
| **ASSAYBENCH** | 基准 | #虚拟细胞 | 1920个筛选，约13826基因/筛选* | [链接](https://github.com/Genentech/AssayBench) | yes | 1 | CRISPR表型预测基准，评估智能体虚拟细胞能力 |
| **GenoTEX** | 基准 | #Agent | 含专家标注代码与结果* | [链接](https://github.com/Liu-Hy/GenoTEX) | yes | 1 | 基因表达分析智能体基准，LLM科研工作流直接对标 |
| **TruthInsightBench** | 基准 | #Agent | 40任务/10领域/40篇研究* | [链接](https://github.com/TruthInsight-stack/TruthInsightBench) | yes | 1 | 科学发现智能体评测，科研智能体工作流可参照 |
| **ARCHS4** | 数据库 | #衰老 | 约5.7万样本，28组织，1-114岁* | [链接](https://maayanlab.cloud/archs4/) | yes | 2 | 跨年龄RNA-seq，转录组衰老时钟训练验证数据 |
| **Human Cell Atlas** | 数据库 | #单细胞 | 全球细胞图谱计划* | [链接](https://data.humancellatlas.org/) | yes | 2 | 细胞图谱资源，类器官衰老demo参照与跨组织整合 |
| **MEDICINE** | 数据库 | #衰老 #人群队列 | UKBB 274,247人/107代谢物* | MEDICINE门户 | unknown | 1 | UKB代谢组生物年龄模型，迁移到ChinaHEART做代谢衰老评分 |
| **CollecTRI** | 数据库 | #虚拟细胞 | 多物种TF-靶基因网络* | [链接](https://github.com/saezlab/CollecTRI) | yes | 1 | TF调控网络先验，扰动预测带符号系数学习 |
| **Gene Expression Omnibus** | 数据库 | #衰老 | 51项人类干预研究* | [链接](https://www.ncbi.nlm.nih.gov/geo/) | yes | 1 | 干预研究DNAm数据，衰老标志物响应性分析 |
| **NHGRI-EBI GWAS Catalog** | 数据库 | #人群队列 | 62.5万关联，>8.5万数据集* | [链接](https://www.ebi.ac.uk/gwas/) | yes | 1 | GWAS汇总统计标准库，ChinaHEART遗传关联查询 |
| **Olink** | 工具 | #心血管 #人群队列 | 2,920蛋白 panel* | [链接](https://www.olink.com/) | commercial | 6 | 蛋白组检测平台，ChinaHEART蛋白组方案参照 |
| **SomaScan** | 工具 | #衰老 #心血管 #人群队列 | 4,877 aptamer* | [链接](https://somalogic.com/) | commercial | 4 | 血浆蛋白组平台，ChinaHEART蛋白组衰老建模参照 |
| **Perturb-seq** | 工具 | #单细胞 #虚拟细胞 | 约 20 万细胞* |  | unknown | 3 | CRISPR扰动数据，虚拟扰动建模训练与基准 |
| **Perturb-FISH** | 工具 | #类器官 #单细胞 | MERFISH+gRNA原位解码* |  | unknown | 1 | 空间扰动读取思路，可用于类器官虚拟扰动建模设计 |

## P2 了解即可（89）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **ImageNet-1k** | 数据集 | #世界模型 | 约128万训练图像，1000类* | [链接](https://www.image-net.org/) | unknown | 8 | 作为自监督视觉预训练与线性评估的主要基准数据集。 |
| **FinnGen** | 数据集 | #衰老 #人群队列 | 176,899芬兰人，2,444表型* | [链接](https://www.finngen.fi/) | unknown | 4 | 芬兰隔离人群疾病遗传资源，用于GWAS与精细定位发现低频变异关联。 |
| **Mass General Brigham Biobank** | 数据集 | #心血管 #人群队列 | 约5.3万例（670例颈动脉狭窄+52,636对照）* | [链接](https://www.massgeneralbrigham.org/research/biobank) | unknown | 4 | 用于评估CAD、PAD、IS和cIMT多基因风险评分与颈动脉狭窄的关联。 |
| **ModelNet40** | 数据集 | #世界模型 | 40类、12311个模型* | [链接](https://modelnet.cs.princeton.edu/) | unknown | 4 | 用于点云自监督方法的线性分类与少样本分类评估。 |
| **Norman 2019 Perturb-seq** | 数据集 | #单细胞 #虚拟细胞 | Perturb-seq扰动数据集* |  | unknown | 3 | 用于评估扰动响应预测的DE20 MSE基准数据集。 |
| **MATH** | 数据集 | #Agent | 约12500题* | [链接](https://github.com/hendrycks/math) | yes | 3 | 用于评测MASPRM在数学推理任务中的表现。 |
| **BioBank Japan** | 数据集 | #心血管 #人群队列 | 第一期约 20 万患者（47 种疾病） | [链接](https://biobankjp.org/) | controlled | 2 | 作为国家生物样本库WGS项目案例，用于比较设计、技术与发现经验。 |
| **GSM8K** | 数据集 | #Agent #世界模型 | 小学数学应用题基准* | [链接](https://github.com/openai/grade-school-math) | yes | 2 | 用于评估DLLM-JEPA在数学推理任务上的性能提升。 |
| **MIMIC-IV** | 数据集 | #心血管 #人群队列 | 重症监护EHR（多任务基准）* | [链接](https://physionet.org/content/mimiciv/) | controlled | 2 | 作为MiGHT-EHR多任务图Transformer的评测数据集之一。 |
| **Penn Medicine BioBank** | 数据集 | #心血管 #人群队列 | 参与PRS评估人群* | [链接](https://www.pennmedicine.org/for-patients-and-visitors/penn-medicine-divisions/penngen) | unknown | 2 | 用于构建整合基因组和蛋白组的冠脉微血管疾病风险预测框架。 |
| **ADVANCE** | 数据集 | #心血管 | T2D CVD风险模型* |  | unknown | 2 | 用于验证MCCP在T2D心肾并发症跨祖源预测中的可靠性。 |
| **AMC23** | 数据集 | #Agent | 40题* | [链接](https://huggingface.co/datasets/AI-MO/aimo-validation-amc) | unknown | 2 | 用于评测PURE方法在数学竞赛题上的推理性能。 |
| **COCO** | 数据集 | #世界模型 | 约33万图像，80类* | [链接](https://cocodataset.org/) | unknown | 2 | 用于评估自监督预训练模型在检测与分割下游任务上的迁移能力。 |
| **ELSA-Brasil** | 数据集 | #心血管 | 巴西成人队列（规模未明确）* | [链接](https://www.elsa.org.br/) | unknown | 2 | 作为外部前瞻队列验证单导联AI-ECG心衰风险分层。 |
| **ESTHER** | 数据集 | #心血管 | 5,578-8,308人* |  | unknown | 2 | 德国队列，用于代谢组学心血管风险预测的外部验证。 |
| **Genecorpus-30M** | 数据集 | #单细胞 | 约3000万细胞* |  | unknown | 2 | 作为scFM预训练语料，用于审计基准污染及Geneformer预训练。 |
| **JetClass** | 数据集 | #世界模型 | 1亿个喷注* | 项目网站公开 | unknown | 2 | 用于预训练HEP-JEPA高能物理基础模型并评估top tagging等下游任务。 |
| **ScanObjectNN** | 数据集 | #世界模型 | 15类、约15000样本* | [链接](https://hkust-vgd.github.io/scanobjectnn/) | unknown | 2 | 用于评估点云掩码自编码器在真实扫描物体分类上的下游性能。 |
| **GSM-Plus** | 数据集 | #Agent | 约1万题* | [链接](https://huggingface.co/datasets/qintongli/GSM-Plus) | yes | 1 | 用于评测BiPRM在解级数学推理上的表现。 |
| **GTEx** | 数据集 | #衰老 | 约 950 名供体 · 54 个组织（v8） | [链接](https://gtexportal.org/) | partial | 1 | 用于分析TFMethyl Clock靶基因表达。 |
| **Libri-light** | 数据集 | #世界模型 | 60000小时* | [链接](https://github.com/facebookresearch/libri-light) | yes | 1 | 用于大规模无标注语音预训练及多规模微调评估HuBERT。 |
| **NHANES** | 数据集 | #衰老 #人群队列 | 每两年约 1 万人（美国代表性样本） | [链接](https://www.cdc.gov/nchs/nhanes/) | yes | 1 | 作为外部验证队列验证GOLD BioAge对死亡风险的预测能力。 |
| **PRM800K** | 数据集 | #Agent | 80万步级标签* | [链接](https://github.com/openai/prm800k) | yes | 1 | 用于训练过程奖励模型PURE。 |
| **Tabula Sapiens** | 数据集 | #单细胞 | 564,253细胞，多供体* |  | unknown | 1 | 用于从scGPT中提取造血伪时间排序算法并做供体留出基准评估。 |
| **TCGA** | 数据集 | #类器官 | 泛癌队列，数万样本* | [链接](https://portal.gdc.cancer.gov/) | partial | 1 | 与乳腺癌类器官RNA-seq整合，用于构建类器官定制预测模型。 |
| **Cell Painting Gallery** | 数据集 | #类器官 |  | [链接](https://github.com/broadinstitute/cellpainting-gallery) | yes | 0 |  |
| **LINCS L1000** | 数据集 | #虚拟细胞 |  | [链接](https://clue.io/) | registration | 0 |  |
| **PTB-XL** | 数据集 | #心血管 | 21,799 份心电 / 18,869 人 | [链接](https://physionet.org/content/ptb-xl/) | yes | 0 |  |
| **Qwen3-4B** | 模型 | #Agent | 4B参数* | [链接](https://huggingface.co/Qwen/Qwen3-4B) | yes | 3 | 用于RLVR信用分配与GEAR优势重加权实验的基础模型。 |
| **Qwen2.5-Math-7B** | 模型 | #Agent | 70亿参数* | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-7B) | yes | 2 | 作为PURE与ScalePRM的基座模型进行推理强化学习。 |
| **Qwen3-1.7B** | 模型 | #Agent | 1.7B参数* | [链接](https://huggingface.co/Qwen/Qwen3-1.7B) | yes | 2 | 用于评估TEMPO与P2T信用分配方法的基座模型。 |
| **Qwen3-8B** | 模型 | #Agent | 8B参数* |  | unknown | 2 | 用于RLVR信用分配与GEAR优势重加权实验的基础模型。 |
| **AlphaFold** | 模型 | #心血管 | 未明确* | [链接](https://github.com/google-deepmind/alphafold) | yes | 1 | 用于预测候选因果蛋白的三维结构以辅助功能解释。 |
| **data2vec** | 模型 | #世界模型 | 通用自监督模型* | [链接](https://github.com/facebookresearch/fairseq/tree/main/examples/data2vec) | yes | 1 | 作为Audio-JEPA的对比基线，比较音频表征学习性能。 |
| **DeepSeekMath 7B** | 模型 | #Agent | 7B参数，120B数学token预训练* | [链接](https://huggingface.co/deepseek-ai/deepseek-math-7b-base) | yes | 1 | 通过继续预训练与GRPO提升开放模型数学推理能力。 |
| **Graph-JEPA** | 模型 | #世界模型 | 图级表征* | [链接](https://github.com/geriskenderi/graph-jepa) | yes | 1 | 用于图级表征学习的联合嵌入预测架构模型，支持图分类与回归。 |
| **HuBERT** | 模型 | #世界模型 | 最大1B参数* | [链接](https://github.com/facebookresearch/fairseq/tree/main/examples/hubert) | yes | 1 | 提出并发布的语音自监督预训练模型，用于掩码隐藏单元预测学习语音表征。 |
| **Intuitor** | 模型 | #Agent | 基于GRPO的无监督RL方法* | [链接](https://github.com/sunblaze-ucb/Intuitor) | yes | 1 | 用模型自身置信度作为唯一奖励信号的无监督强化学习方法。 |
| **MAE** | 模型 | #世界模型 | ViT-Huge，ImageNet-1K达87.8%* | [链接](https://github.com/facebookresearch/mae) | yes | 1 | 掩码自编码器，通过重建缺失图像块实现可扩展视觉自监督预训练。 |
| **MoCo** | 模型 | #世界模型 | ResNet-50骨干，ImageNet预训练* | [链接](https://github.com/facebookresearch/moco) | yes | 1 | 提出动量对比学习框架，构建动态字典进行无监督视觉表征学习。 |
| **Point-JEPA** | 模型 | #世界模型 | 点云块嵌入* | [链接](https://github.com/Ayumu-J-S/Point-JEPA) | yes | 1 | 面向点云的联合嵌入预测架构模型，用于自监督点云表征学习。 |
| **Qwen2-VL-2B** | 模型 | #Agent | 2B参数* | [链接](https://huggingface.co/Qwen/Qwen2-VL-2B-Instruct) | yes | 1 | 作为Med-R1的基座模型与对比基线。 |
| **Qwen2-VL-72B** | 模型 | #Agent | 72B参数* | [链接](https://huggingface.co/Qwen/Qwen2-VL-72B-Instruct) | yes | 1 | 作为Med-R1对比的更大规模基线模型。 |
| **Qwen2.5-7B** | 模型 | #Agent | 70亿参数* | [链接](https://huggingface.co/Qwen/Qwen2.5-7B) | yes | 1 | 作为PURE方法的基础模型之一进行强化微调。 |
| **Qwen2.5-Math-1.5B** | 模型 | #Agent | 15亿参数* | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-1.5B) | yes | 1 | 作为PURE方法的小规模基座模型进行实验。 |
| **SAM (Segment Anything Model)** | 模型 | #类器官 | 十亿级掩码预训练* | [链接](https://github.com/facebookresearch/segment-anything) | yes | 1 | 用于PDO延时显微视频中类器官的分割。 |
| **wav2vec 2.0** | 模型 | #世界模型 | 预训练语音模型* | [链接](https://github.com/facebookresearch/fairseq/tree/main/examples/wav2vec) | yes | 1 | 作为Audio-JEPA的对比基线，比较音频表征学习性能。 |
| **DNABERT-2** | 模型 |  |  | [链接](https://github.com/MAGICS-LAB/DNABERT_2) | yes | 0 |  |
| **DunedinPACE** | 模型 | #衰老 |  | [链接](https://github.com/danbelsky/DunedinPACE) | yes | 0 |  |
| **Enformer** | 模型 |  |  |  | yes | 0 |  |
| **ESM-2** | 模型 |  |  | [链接](https://github.com/facebookresearch/esm) | yes | 0 |  |
| **Nucleotide Transformer** | 模型 |  |  | [链接](https://github.com/instadeepai/nucleotide-transformer) | yes | 0 |  |
| **ALFWorld** | 基准 | #Agent | 6类任务、数千回合* | [链接](https://alfworld.github.io/) | unknown | 4 | 用于评估MetaSkill-Evolve智能体技能自进化框架的基准之一。 |
| **MMLU** | 基准 | #Agent #世界模型 | 57学科多选题基准* | [链接](https://github.com/hendrycks/test) | unknown | 2 | 用于评估DLLM-JEPA在多学科知识任务上的性能。 |
| **ProcessBench** | 基准 | #Agent | 3400条推理路径* | [链接](https://huggingface.co/datasets/Qwen/ProcessBench) | yes | 2 | 用于评测BiPRM与ScalePRM的步级错误检测能力。 |
| **scIB** | 基准 | #单细胞 | 13任务，最多100万细胞* |  | unknown | 2 | 单细胞数据整合基准，用于评估批次去除与生物变异保留。 |
| **WebShop** | 基准 | #Agent | 约120万商品* | [链接](https://webshop-pnlp.github.io/) | unknown | 2 | 用于评估SELAUR智能体在网页购物任务上的成功率。 |
| **MedQA** | 基准 | #Agent | 未明确* | [链接](https://github.com/jind11/MedQA) | yes | 1 | 用于评估医学推理能力的分布内基准。 |
| **MMLU-Medical** | 基准 | #Agent | 未明确* | [链接](https://huggingface.co/datasets/cais/mmlu) | yes | 1 | 用于评估分布外医学推理泛化能力。 |
| **NKIBench** | 基准 | #Agent | 来自真实LLM工作负载的Trainium内核* | [链接](https://github.com/zhang677/AccelOpt) | yes | 1 | 用于评测LLM智能体自主优化AWS Trainium内核的性能。 |
| **PushT** | 基准 | #世界模型 | 推T形块操作任务* | [链接](https://github.com/huggingface/gym-pusht) | yes | 1 | 用于评估D-JEPA在机器人操作任务上的动作选择成功率。 |
| **R-Judge** | 基准 | #Agent | 569条交互记录，27类风险场景* | [链接](https://github.com/Lordog/R-Judge) | yes | 1 | 用于评测LLM智能体在交互环境中的安全风险意识。 |
| **SKILLMISEVO-BENCH** | 基准 | #Agent | 冻结基准，含恶意/良性/延续任务* | [链接](https://github.com/henrymao2004/misevolve) | yes | 1 | 冻结基准，用于评估技能误演化导致的不安全行为。 |
| **SKILLMISEVO-GYM** | 基准 | #Agent | 25种配置，各525任务、25回合* | [链接](https://github.com/henrymao2004/misevolve) | yes | 1 | 生命周期感知测试台，用于研究自改进智能体的技能误演化。 |
| **Socratic-PRMBench** | 基准 | #Agent | 2995条缺陷路径* | [链接](https://github.com/Xiang-Li-oss/Socratic-PRMBench) | yes | 1 | 用于系统评测PRM在六种推理模式下的过程错误检测能力。 |
| **StreamBench** | 基准 | #Agent | 在线学习环境，多任务序列* | [链接](https://github.com/stream-bench/stream-bench) | yes | 1 | 评估LLM智能体在连续反馈流中持续改进能力的基准。 |
| **ArrayExpress** | 数据库 | #衰老 | 51项人类干预研究* | [链接](https://www.ebi.ac.uk/biostudies/arrayexpress) | yes | 1 | 提供表观遗传衰老生物标志物响应性分析所用的公开DNAm数据。 |
| **ENCODE** | 数据库 | #Agent | 132个转录因子* | [链接](https://www.encodeproject.org/) | yes | 1 | 用于DNA基序发现评测，DALE在132个转录因子上评估。 |
| **Aging Atlas** | 数据库 | #衰老 |  | [链接](https://ngdc.cncb.ac.cn/aging/) | yes | 0 |  |
| **CellAge** | 数据库 | #衰老 |  | [链接](https://genomics.senescence.info/cells/) | yes | 0 |  |
| **CELLxGENE Census** | 数据库 | #单细胞 |  | [链接](https://chanzuckerberg.github.io/cellxgene-census/) | yes | 0 |  |
| **ClockBase** | 数据库 | #衰老 |  |  | unknown | 0 |  |
| **dbGaP** | 数据库 | #人群队列 |  | [链接](https://www.ncbi.nlm.nih.gov/gap/) | controlled | 0 |  |
| **DepMap** | 数据库 | #虚拟细胞 |  | [链接](https://depmap.org/portal/) | yes | 0 |  |
| **EGA** | 数据库 | #人群队列 |  | [链接](https://ega-archive.org/) | controlled | 0 |  |
| **EWAS Atlas** | 数据库 | #衰老 |  | [链接](https://ngdc.cncb.ac.cn/ewas/atlas) | yes | 0 |  |
| **GenAge** | 数据库 | #衰老 |  | [链接](https://genomics.senescence.info/genes/) | yes | 0 |  |
| **HuBMAP** | 数据库 | #单细胞 |  | [链接](https://portal.hubmapconsortium.org/) | yes | 0 |  |
| **Human Protein Atlas** | 数据库 |  |  | [链接](https://www.proteinatlas.org/) | yes | 0 |  |
| **MassIVE** | 数据库 |  |  | [链接](https://massive.ucsd.edu/) | yes | 0 |  |
| **Open Genes** | 数据库 | #衰老 |  | [链接](https://open-genes.com/) | yes | 0 |  |
| **Open Targets** | 数据库 |  |  | [链接](https://platform.opentargets.org/) | yes | 0 |  |
| **PRIDE** | 数据库 |  |  | [链接](https://www.ebi.ac.uk/pride/) | yes | 0 |  |
| **recount3** | 数据库 |  |  | [链接](https://rna.recount.bio/) | yes | 0 |  |
| **scPerturb** | 数据库 | #虚拟细胞 |  |  | yes | 0 |  |
| **Single Cell Portal** | 数据库 | #单细胞 |  | [链接](https://singlecell.broadinstitute.org/) | yes | 0 |  |
| **SRA** | 数据库 |  |  | [链接](https://www.ncbi.nlm.nih.gov/sra) | yes | 0 |  |
| **CellProfiler** | 工具 | #单细胞 | 图像分析软件* |  | unknown | 2 | 提取传统手工图像特征并与深度学习特征比较。 |
| **scvi-tools** | 工具 | #单细胞 | 多模态与单模态数据集* | [链接](https://github.com/scverse/scvi-tools) | yes | 2 | 深度生成模型，用于多模态数据整合、插补与缺失模态差异表达估计。 |

## 日报新发现（8，未核验）

- Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling（模型，2026-09-26）https://doi.org/10.64898/2026.09.22.752128
- A single-cell RNA-seq catalog of ground truth gene coregulation（数据集，2026-09-22）https://doi.org/10.64898/2026.09.18.752692
- A lifespan-scale single-cell atlas defines an early-childhood immunometabolic transition linked to age-referenced immune states（数据集，2026-09-19）https://doi.org/10.64898/2026.09.11.750312
- spaGFM is a scalable graph foundation model for spatial transcriptomics analyses（模型，2026-09-19）https://doi.org/10.21203/rs.3.rs-11012643/v1
- A massively parallel synthetic gene atlas for learning compact cis-regulatory grammar across cellular contexts（数据集，2026-09-16）https://doi.org/10.64898/2026.09.13.751267
- LucaCell: a sequence-centric foundation model for cross-species single-cell analysis（模型，2026-09-16）https://doi.org/10.64898/2026.09.08.750024
- Single-cell splice isoform usage reveals distinct axes of cellular identity and senescence（数据集，2026-09-16）https://doi.org/10.64898/2026.09.11.748700
- A breast tissue-specific epigenetic clock provides accurate chronological age predictions and reveals de-correlation of age and DNA methylation in tumor-adjacen（模型，2026-09-15）https://doi.org/10.1080/15592294.2026.2714582

## 单篇提及（373，未进主表）

- 数据集：23andMe、23andMe BMI GWAS、ADE20K、AIDA v2、Age, Gene/Environment Susceptibility-Reykjavik Study (AGES)、Asian Indian Diabetes Heart Study / Sikh Diabetes Study (AIDHS/SDS)、AudioSet、AudioSet-20K、CHARGE-AF Consortium、CHOP、COCO-Stuff、CODE (Brazilian ECG Dataset, 2.3M ECGs)、CTRP、CeNGEN、Cityscapes、Copenhagen General Population Study、DFTJ、Danish National Patient Registry、Droid、ELAN、EPIC-Norfolk、ESC-50、Estonian Biobank、FEVER、FINRISK、FSD50K、Fenland、Framingham Offspring Study、GDSC、GIANT Consortium BMI GWAS、GSE67752、Geisinger ECG Cohort、Generation Scotland、HEEDB、HM3D v0.2、HotpotQA、I-SPY2、INSPIRE-T、ImageNet ILSVRC-2012、Integrated Mega-scale Atlas、Israel 10K Project、JUMP-MOA、JUMP-lite、Jiangsu Behavioral and Physical Chronic Disease Cohort (JBPCD)、KORA、LVIS、Librispeech、Lorenz attractor、Lothian Birth Cohort 1936、MATH500、MERFISH whole mouse brain atlas、MGB (Mass General Brigham) ECG Cohort、MGB Biobank、MIMIC、MIMIC-III、MIMIC-IV-ECG、MNIST、MODIS、McFarland、Mexico City Prospective Study (MCPS)、NLST、NPBBD-Korea、Nurses' Health Study、PRECISE、Perturb-seq genome-scale screen、PerturbReason、Robomimic、Rotterdam Study、SCIPRM70K、SEA-AD、SHIP-START、SHIP-TREND、ST-bank、SaMi-Trop、SciPlex3、Sentinel-1、Sentinel-2、SpatialCorpus-110M、Taiwan Precision Medicine Initiative (TPMI)、Tox21
- 模型：AI-HF、AIRE、AROMA、ASCVD-IRT、ATM (Age-dependent Topic Model)、AdaptAge、AlphaEarth、Audio-MAE、BEHRT、BYOL、Bootleg、BrainBeacon、CAME、CARDIAC-FM、CLM-X、CMAE、CPA、CTBA、CTransPath、Cell-o1、CellFM、CellFlux、CellFluxRL、CellOT、CellWorld、China-AIHeart、Co-Scientist、CrossJEPA、D-SPIN、D2R2、DINO-WM、DNAmEMRAge、DamAge、DeepSeek-R1、DeepSeek-R1-Zero、Delta V、DiRL、ECG-AI、ECG-FM、ECG-LFM、ECG2CAD、EHR-MPC、EMRAge、Echo2HF、Extracellular Matrix Aging Clock、Flow-JEPA、Foresight、Foresight-England、Framingham Risk Score (FRS)、GLAM、GLAM NAV、GOLD BioAge、GPS Mult、GRASP、GenReasoner、GeneCompass、GenePT、GenoAgent、GraphCL、HEP-JEPA、Hannum DNAm Age Clock、Healthspan Proteomic Score (HPS)、JEPA-Anything、Kimi k1.5、LaMamba-Diff、LeJEPA、LeVJEPA、LinAge2、Longitudinal Proteomic Aging Index (LPAI)、LucaCell、MC-JEPA、MILTON、ML-CVD-C、MSGene、MSKAge、Med-BERT、Med-R1、MetBAG、MetaboHealth、Metabolic Vulnerability Index (MVX)
- 基准：ABC-Bench、AI4AI-Bench、AdaJEPA、BIRD、BLADE、Baba in Wonderland、BioDataLab、BioKGBench、BiomniBench-DA、CellPuzzles、ComputAgeBench、D4RL、DiscoverPhysics、GSM-HARD、Gaia2、HLE、HumanEval、LMR-BENCH、LOGIQA、LiveCodeBench、MedMCQA、MedPRMBench、MemCalib、OfficeQA、PARADIGM-HF、PASCAL VOC、PertEval-scFM、PerturBench、ProteinGym、RSIBench-Data、RoboTwin、SEAGym、SWE Bench Verified、SciIntegrity-Bench、ScienceAgentBench、SealQA、SoundnessBench、Terminal-Bench 2.0、ToolMaker Benchmark、VTAB、Virtual Cell Challenge、Virtual Cell Challenge 2026、X-ARES、scEval
- 数据库：Allen Brain Atlas、CMAP、CPRD、CPRD Aurum、Cell Landscape、ChIP-Atlas、GeneATLAS、Immunosenescence Inventory、MEDICINE portal、PGS Catalog、PhysioNet、Proteome-Phenome Atlas、STP、TEAPEE
- 工具：AusCVDRisk、AutoPrognosis、BASIL、BAVAR、BOLT-LMM、BioLLM、Biolearn、CINEMA-OT、CODRP、CROP-seq、CellDuality、CellPaint-POSH、CellScientist、ClockBase Agent、DALE、DeGAs、FaithRL、GATK、GEPA、Habitat、Hail、Harmony、ICD-8 to ICD-10 Mapping、K-Dense、LUCID、LWD-Miniscope、LivAge、Loki、Longevity Claw、MatClaw、Mortara VERITAS Algorithm、Mosaic、Nahual、OSCAR、P2T、PHESANT、PRS-CS、PheMIME、PheWeb、Phecodes、REGENIE、SAFEEVOLVE、SAIGE-GENE、SCOPE (Systematic Classification of Organoids for Phenotypic Evaluation)、SCanSNP、SO-GRPO、SO-PPO、SORL、SPAC-seq、SenePy、SpatialQM、TARDIS、TEMPO、TFActProfiler、The AI Scientist、Tool-GRPO、TotalSegmentator、TranslAGE、TreeRL、Trellis、UKB-MDRMF、associationSubgraphs、copairs、leakcheck、moscot、scContam、ukbnmr
