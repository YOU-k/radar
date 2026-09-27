# 资源登记（数据集 / 模型 / 基准）

从 780 处证据引用中挖出 515 项命名资源；主表 151 项（被 ≥2 篇工作使用、或跨方向、或开放且链接核验通过且规模明确），其余 364 项单篇提及的列在末尾。核验：ok 可达 / blocked 站点拒绝探测 / dead 失效 / n/a 非链接。更新 2026-09-27


## P0 优先上手（16）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **UK Biobank** | 数据集 | #衰老 #心血管 #人群队列 | 30,376人；2,923蛋白+251代谢物 | [链接](https://www.ukbiobank.ac.uk/) | restricted | 112 | 多组学衰老与CVD方法迁移主数据源，ChinaHEART参照基准 |
| **UK Biobank Pharma Proteomics Project (UKB-PPP)** | 数据集 | #心血管 #人群队列 | 54,219人 / 2,923蛋白 | [链接](https://www.ukbiobank.ac.uk/) | restricted | 10 | UKB蛋白组，ChinaHEART蛋白组CVD风险迁移参照 |
| **Tahoe-100M** | 数据集 | #单细胞 #虚拟细胞 | 1亿转录组，50细胞系，1100药物条件 | 公开释放（Tahoe-100M） | yes | 4 | 亿级药物扰动图谱，虚拟扰动预训练与类器官demo核心数据 |
| **Pan-UK Biobank GWAS summary statistics** | 数据集 | #人群队列 | 7266个性状，多祖源 | [链接](https://pan.ukbb.broadinstitute.org/) | yes | 2 | 跨祖源GWAS汇总，ChinaHEART迁移与PRS跨人群校正 |
| **Replogle 2022 Perturb-seq** | 数据集 | #虚拟细胞 | >250万人类细胞 | [链接](https://doi.org/10.1016/j.cell.2022.05.013) | yes | 2 | 基因组规模Perturb-seq，扰动预测建模与基准评估核心数据 |
| **scGPT** | 模型 | #类器官 #单细胞 #虚拟细胞 | 预训练于3300万+细胞 | [链接](https://doi.org/10.1038/s41592-024-02201-0) | yes | 14 | 单细胞基础模型基线，类器官衰老demo与虚拟扰动对标 |
| **Geneformer** | 模型 | #单细胞 #虚拟细胞 | V2-316M，约316M参数 |  | yes | 10 | 单细胞基础模型基线，类器官衰老demo与虚拟扰动建模直接对标 |
| **scFoundation** | 模型 | #单细胞 #虚拟细胞 | 大规模单细胞预训练模型 | [链接](https://github.com/biomap-research/scFoundation) | yes | 5 | 扰动预测基准模型，类器官扰动demo可直接部署对比 |
| **China-PAR** | 模型 | #心血管 | 推导21320人，验证84961人 | [链接](https://doi.org/10.1161/CIRCULATIONAHA.116.022367) | yes | 4 | 中国CVD风险模型，ChinaHEART迁移必比对照 |
| **Tahoe-X1** | 模型 | #单细胞 | 最高30亿参数 | 公开预训练权重、训练代码和评估流程 | yes | 3 | 扰动训练单细胞基础模型，虚拟扰动响应建模首选基线 |
| **Chreode** | 模型 | #单细胞 #虚拟细胞 | 240万细胞小鼠胚胎图谱预训练 | [链接](https://arxiv.org/abs/2605.28111v1) | yes | 2 | 细胞世界模型，虚拟扰动响应与类器官时序建模直接参照 |
| **SCALE** | 模型 | #单细胞 #虚拟细胞 | CRISPR/化学/发育/免疫 | [链接](https://arxiv.org/abs/2603.17380v3) | yes | 1 | 条件传输虚拟扰动模型，类器官扰动响应建模直接可用 |
| **LongevityBench** | 基准 | #衰老 | 17项任务/5个数据域 | [链接](https://doi.org/10.1016/j.cell.2026.08.026) | yes | 1 | 衰老AI基准，类器官衰老demo与虚拟扰动建模的对标评测 |
| **CZ CELLxGENE Discover** | 数据库 | #衰老 | 超7000万细胞 | [链接](https://cellxgene.cziscience.com/) | yes | 1 | 单细胞图谱，训练类器官/单细胞衰老时钟的公开数据 |
| **Proteome-Phenome Atlas** | 数据库 | #人群队列 | 53,026人，2,920蛋白，406+660疾病 | [链接](https://proteome-phenome-atlas.com) | yes | 1 | 开放蛋白组-疾病图谱，ChinaHEART蛋白组关联查询与验证 |
| **Cell Painting** | 工具 | #衰老 #单细胞 | 图像型profiling数据（十年积累） | [链接](https://doi.org/10.1038/s41592-024-02528-8) | yes | 3 | 细胞形态扰动响应，类器官+cell painting扰动建模核心 |

## P1 值得登记（60）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **All of Us Research Program** | 数据集 | #人群队列 | 39.3万人（含24.5万WGS） | [链接](https://www.researchallofus.org/) | restricted | 10 | 多血统EHR+基因组，PRS与EHR关联复制方法参照 |
| **China Kadoorie Biobank** | 数据集 | #衰老 #心血管 | 约51万人（本研究子集2.5万–4.3万） | [链接](https://www.ckbiobank.org/) | restricted | 8 | 中国人群队列，CVD风险模型跨国验证与迁移参照 |
| **ARIC** | 数据集 | #心血管 #人群队列 | V3 10,638 / V5 3,908 | [链接](https://www2.cscc.unc.edu/aric/) | restricted | 4 | 蛋白组心衰/衰弱队列，ChinaHEART蛋白组参照 |
| **Framingham Heart Study** | 数据集 | #衰老 #心血管 | 10,097人，28,151份ECG | [链接](https://www.framinghamheartstudy.org/) | restricted | 3 | ECG-AF深度学习经典队列，心血管AI模型对标 |
| **MESA** | 数据集 | #心血管 #人群队列 | 6814人，随访12年，735变量 | [链接](https://www.mesa-nhlbi.org/) | restricted | 3 | 多模态CVD队列，心血管基础模型外部验证 |
| **Perturb-seq** | 数据集 | #单细胞 | 约 20 万细胞 |  | unknown | 3 | CRISPR扰动数据，虚拟扰动建模训练与基准 |
| **Atherosclerosis Risk in Communities (ARIC) Study** | 数据集 | #心血管 #人群队列 | 7,213欧裔+1,871非裔，4,657蛋白 | [链接](https://aric.cscc.unc.edu/) | restricted | 2 | 蛋白组预测模型与cis-pQTL参照，可迁移到ChinaHEART蛋白组分析 |
| **Cardiovascular Health Study** | 数据集 | #心血管 | 约5,888人 | [链接](https://chs-nhlbi.org/) | restricted | 2 | 老年CVD队列，ECG-AI心血管结局外部验证 |
| **CHARLS** | 数据集 | #心血管 | 约23,000人 / 9年随访 | [链接](http://charls.pku.edu.cn/) | restricted | 2 | 中国队列，ChinaHEART迁移与AI-ECG外部验证 |
| **Global Biobank Meta-analysis Initiative (GBMI)** | 数据集 | #人群队列 | 23库，220万人，14疾病 | [链接](https://www.globalbiobankmeta.org/) | restricted | 2 | 跨库荟萃资源，跨祖源PRS评估方法参照 |
| **THL Biobank** | 数据集 | #人群队列 | 三国生物库共700,217人 | [链接](https://thl.fi/en/web/thl-biobank) | restricted | 2 | NMR代谢组重复验证队列，ChinaHEART代谢标志物外部参照 |
| **CeNGEN** | 数据集 | #衰老 | 128种神经元类型 | [链接](https://www.cengen.org/) | yes | 1 | 线虫神经元转录组，模式生物虚拟扰动与衰老时钟 |
| **CODE15** | 数据集 | #心血管 | 233647份ECG | [链接](https://doi.org/10.1038/s41591-023-02235-5) | yes | 1 | 大规模ECG公开数据，ECG基础模型预训练验证 |
| **CTRP** | 数据集 | #虚拟细胞 | 大型癌细胞系药物面板 | [链接](https://portals.broadinstitute.org/ctrp) | yes | 1 | 药物基因组学面板，盲响应预测泛化评估 |
| **McFarland** | 数据集 | #虚拟细胞 | 大规模药物扰动数据 | [链接](https://www.ncbi.nlm.nih.gov/geo) | yes | 1 | 药物扰动基准数据，虚拟扰动建模评测 |
| **SciPlex3** | 数据集 | #虚拟细胞 | 大规模药物扰动数据 | [链接](https://www.ncbi.nlm.nih.gov/geo) | yes | 1 | 药物扰动基准数据，虚拟扰动建模评测 |
| **SCORE2** | 模型 | #心血管 | 欧洲10年CVD风险模型 | [链接](https://doi.org/10.1093/eurheartj/ehab309) | yes | 5 | 欧洲CVD风险基线，ChinaHEART模型对标 |
| **GEARS** | 模型 | #单细胞 #虚拟细胞 | 图神经网络模型 |  | unknown | 3 | 扰动预测可迁移基线，虚拟扰动建模对比方法 |
| **TranscriptFormer** | 模型 | #类器官 #单细胞 | 1.12亿细胞、12物种、15.3亿年进化 |  | unknown | 3 | 跨物种虚拟细胞图谱，虚拟扰动与跨物种迁移参照 |
| **CHARGE-AF** | 模型 | #心血管 | 房颤风险预测 | [链接](https://www.chargeconsortium.com/) | yes | 3 | 房颤风险模型，AI-ECG与蛋白组评分比较基线 |
| **PREVENT** | 模型 | #心血管 | 美国AHA 10年CVD风险方程 | [链接](https://doi.org/10.1161/CIRCULATIONAHA.123.067626) | yes | 3 | AHA风险方程，蛋白组评分增量比较基线 |
| **QRISK3** | 模型 | #心血管 | QResearch 1998-2015队列 | [链接](https://qrisk.org/) | yes | 3 | 英国CVD风险模型，蛋白组增量比较基线 |
| **SCimilarity** | 模型 | #单细胞 | 2270 万细胞，399 项研究 |  | unknown | 3 | 细胞表示基础模型，跨队列细胞注释与状态查询可用 |
| **SCORE2-Diabetes** | 模型 | #心血管 | T2D专用CVD风险模型 | [链接](https://doi.org/10.1093/eurheartj/ehad260) | yes | 3 | T2D专用CVD模型，代谢组增量改进对照 |
| **DISCO** | 模型 | #心血管 #虚拟细胞 | HFrEF真实世界队列（规模未明确） | [链接](https://www.immunesinglecell.org) | yes | 2 | ECG嵌入表型匹配，虚拟扰动与治疗效应模拟思路 |
| **UCE (Universal Cell Embeddings)** | 模型 | #类器官 #单细胞 | 3600万细胞预训练 |  | unknown | 2 | 免微调细胞嵌入，类器官衰老demo可作基线表征 |
| **CellPLM** | 模型 | #单细胞 | 预训练模型 |  | unknown | 2 | scEval最佳基础模型之一，类器官单细胞建模候选 |
| **Horvath DNAm Age Clock** | 模型 | #衰老 | 353 CpG |  | unknown | 2 | DNAm年龄基线时钟，类器官衰老demo必比基线 |
| **Longevity-LLM** | 模型 | #衰老 | 0.6B-9B参数，5个模型 | [链接](https://doi.org/10.1016/j.cell.2026.08.026) | yes | 2 | 衰老组学基础模型，可微调做表观年龄与多模态衰老表征 |
| **Reti-CVD** | 模型 | #心血管 | UK Biobank 44,677人验证 |  | unknown | 2 | 视网膜图像CVD评分，多模态风险分层可迁移 |
| **RegFormer** | 模型 | #单细胞 #世界模型 | 2500万人类细胞预训练 |  | unknown | 1 | 融合GRN先验的扰动预测模型，虚拟扰动建模可迁移 |
| **DI-NOv2** | 模型 | #类器官 | ViT骨干自蒸馏模型 | [链接](https://github.com/facebookresearch/dinov2) | yes | 1 | 类器官视频自监督特征+药效预测，可直接用于类器官demo |
| **Framingham Risk Score (FRS)** | 模型 | #心血管 | 10年CVD风险 | [链接](https://www.framinghamheartstudy.org/) | yes | 1 | 传统CVD风险评分，ChinaHEART迁移对照 |
| **GET** | 模型 | #虚拟细胞 | 大规模单细胞预训练 | [链接](https://github.com/GET-Foundation/get_model) | yes | 1 | 代表性虚拟细胞基础模型，扰动建模对标 |
| **I-JEPA** | 模型 | #世界模型 | ViT-Huge/14，16张A100训练<72h | [链接](https://github.com/facebookresearch/ijepa) | yes | 1 | I-JEPA 是自监督表征范式基线，可迁移到类器官图像与组学 |
| **JEPA-DNA** | 模型 | #世界模型 | 多物种基因组基础模型 | [链接](https://github.com/NVIDIA-Digital-Bio/JEPA-DNA) | yes | 1 | JEPA 用于基因组序列，可迁移到虚拟扰动与多组学表征建模 |
| **OmiCLIP** | 模型 | #单细胞 | 基于220万配对patch训练 | [链接](https://doi.org/10.1038/s41592-025-02707-1) | yes | 1 | 图像-转录组对齐模型，类器官多模态衰老建模参照 |
| **scBalFlow** | 模型 | #虚拟细胞 | SciPlex3/McFarland基准 | [链接](https://github.com) | yes | 1 | 流匹配药物扰动预测，类别不平衡场景可迁移 |
| **scDEFT** | 模型 | #虚拟细胞 | 116万细胞 | [链接](https://arxiv.org/abs/2609.10831) | yes | 1 | 药物响应反事实推理框架，虚拟扰动建模可迁移 |
| **scGen** | 模型 | #虚拟细胞 | 未明确（VAE潜空间扰动向量） | [链接](https://doi.org/10.1038/s41592-019-0494-8) | yes | 1 | 潜空间扰动向量预测，虚拟扰动建模经典基线 |
| **scKITE** | 模型 | #虚拟细胞 | 179,067预训练样本 | [链接](https://arxiv.org/abs/2609.14970) | yes | 1 | 知识增强单细胞基础模型，类器官建模候选 |
| **scArchon** | 基准 | #单细胞 #虚拟细胞 | 9种工具，多样本扰动数据 | [链接](https://doi.org/10.1186/s13059-026-04104-z) | yes | 1 | 扰动预测标准化基准，虚拟扰动建模评测直接可用 |
| **VCBench** | 基准 | #类器官 #单细胞 | 5个基础模型、5个可测维度 |  | unknown | 1 | 单细胞基础模型评测基准，选型与对标时参照 |
| **ASSAYBENCH** | 基准 | #虚拟细胞 | 1920个筛选，约13826基因/筛选 | [链接](https://github.com/Genentech/AssayBench) | yes | 1 | CRISPR表型预测基准，评估智能体虚拟细胞能力 |
| **GenoTEX** | 基准 | #Agent | 含专家标注代码与结果 | [链接](https://github.com/Liu-Hy/GenoTEX) | yes | 1 | 基因表达分析智能体基准，LLM科研工作流直接对标 |
| **ProteinGym** | 基准 | #Agent | 217个DMS assay | [链接](https://proteingym.org/) | yes | 1 | 蛋白适应度基准，虚拟扰动与蛋白语言模型对标 |
| **TruthInsightBench** | 基准 | #Agent | 40任务/10领域/40篇研究 | [链接](https://github.com/TruthInsight-stack/TruthInsightBench) | yes | 1 | 科学发现智能体评测，科研智能体工作流可参照 |
| **ARCHS4** | 数据库 | #衰老 | 约5.7万样本，28组织，1-114岁 | [链接](https://maayanlab.cloud/archs4/) | yes | 2 | 跨年龄RNA-seq，转录组衰老时钟训练验证数据 |
| **Human Cell Atlas** | 数据库 | #单细胞 | 全球细胞图谱计划 | HCA门户 | yes | 2 | 细胞图谱资源，类器官衰老demo参照与跨组织整合 |
| **MEDICINE** | 数据库 | #衰老 #人群队列 | UKBB 274,247人/107代谢物 | MEDICINE门户 | yes | 1 | UKB代谢组生物年龄模型，迁移到ChinaHEART做代谢衰老评分 |
| **ChIP-Atlas** | 数据库 | #虚拟细胞 | 大规模TF结合图谱 | [链接](https://chip-atlas.org) | yes | 1 | TF结合先验，虚拟扰动建模调控推断可用 |
| **CollecTRI** | 数据库 | #虚拟细胞 | 多物种TF-靶基因网络 | [链接](https://github.com/saezlab/CollecTRI) | yes | 1 | TF调控网络先验，扰动预测带符号系数学习 |
| **GEO** | 数据库 | #衰老 | 51项人类干预研究 | [链接](https://www.ncbi.nlm.nih.gov/geo/) | yes | 1 | 干预研究DNAm数据，衰老标志物响应性分析 |
| **NHGRI-EBI GWAS Catalog** | 数据库 | #人群队列 | 62.5万关联，>8.5万数据集 | [链接](https://www.ebi.ac.uk/gwas/) | yes | 1 | GWAS汇总统计标准库，ChinaHEART遗传关联查询 |
| **PGS Catalog** | 数据库 | #人群队列 | 未明确 | [链接](https://www.pgscatalog.org/) | yes | 1 | 多基因评分库，ChinaHEART PRS构建与迁移参照 |
| **PhysioNet** | 数据库 | #心血管 | 多数据集门户 | [链接](https://physionet.org/) | yes | 1 | 生理信号门户，ECG基础模型预训练与基准 |
| **Olink** | 工具 | #心血管 #人群队列 | 1,459-2,920蛋白 | [链接](https://www.olink.com/) | yes | 4 | 蛋白组检测平台，ChinaHEART蛋白组方案参照 |
| **SomaScan** | 工具 | #衰老 #心血管 | 4,877 aptamer | [链接](https://somalogic.com/) | restricted | 3 | 血浆蛋白组平台，ChinaHEART蛋白组衰老建模参照 |
| **GRPO** | 工具 | #Agent | 未明确 |  | unknown | 3 | RL优化算法，智能体RLVR训练可直接采用 |
| **Perturb-FISH** | 工具 | #类器官 #单细胞 | MERFISH+gRNA原位解码 |  | unknown | 1 | 空间扰动读取思路，可用于类器官虚拟扰动建模设计 |

## P2 了解即可（75）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **ImageNet-1k** | 数据集 | #世界模型 | 约128万训练图像，1000类 | [链接](https://www.image-net.org/) | yes | 8 | 作为自监督视觉预训练与线性评估的主要基准数据集。 |
| **FinnGen** | 数据集 | #衰老 #人群队列 | 176,899芬兰人，2,444表型 | [链接](https://www.finngen.fi/) | restricted | 4 | 芬兰隔离人群疾病遗传资源，用于GWAS与精细定位发现低频变异关联。 |
| **Mass General Brigham Biobank** | 数据集 | #心血管 #人群队列 | 约5.3万例（670例颈动脉狭窄+52,636对照） | [链接](https://www.massgeneralbrigham.org/research/biobank) | restricted | 4 | 用于评估CAD、PAD、IS和cIMT多基因风险评分与颈动脉狭窄的关联。 |
| **ModelNet40** | 数据集 | #世界模型 | 40类、12311个模型 | [链接](https://modelnet.cs.princeton.edu/) | yes | 4 | 用于点云自监督方法的线性分类与少样本分类评估。 |
| **MATH** | 数据集 | #Agent | 约12500题 | [链接](https://github.com/hendrycks/math) | yes | 3 | 用于评测MASPRM在数学推理任务中的表现。 |
| **BioBank Japan (BBJ)** | 数据集 | #心血管 #人群队列 | 日本9,826例AF/140,446对照 | [链接](https://biobankjp.org/) | restricted | 2 | 作为国家生物样本库WGS项目案例，用于比较设计、技术与发现经验。 |
| **GSM8K** | 数据集 | #Agent #世界模型 | 小学数学应用题基准 | [链接](https://github.com/openai/grade-school-math) | yes | 2 | 用于评估DLLM-JEPA在数学推理任务上的性能提升。 |
| **MIMIC-IV** | 数据集 | #心血管 #人群队列 | 重症监护EHR（多任务基准） | [链接](https://physionet.org/content/mimiciv/) | restricted | 2 | 作为MiGHT-EHR多任务图Transformer的评测数据集之一。 |
| **Penn Medicine BioBank** | 数据集 | #心血管 #人群队列 | 参与PRS评估人群 | [链接](https://www.pennmedicine.org/for-patients-and-visitors/penn-medicine-divisions/penngen) | restricted | 2 | 用于构建整合基因组和蛋白组的冠脉微血管疾病风险预测框架。 |
| **AMC23** | 数据集 | #Agent | 40题 | [链接](https://huggingface.co/datasets/AI-MO/aimo-validation-amc) | yes | 2 | 用于评测PURE方法在数学竞赛题上的推理性能。 |
| **CHS** | 数据集 | #心血管 | 3,189人 |  | restricted | 2 | 作为外部验证队列用于心衰/衰弱蛋白组学及CARDIAC-FM验证。 |
| **COCO** | 数据集 | #世界模型 | 约33万图像，80类 | [链接](https://cocodataset.org/) | yes | 2 | 用于评估自监督预训练模型在检测与分割下游任务上的迁移能力。 |
| **ELSA-Brasil** | 数据集 | #心血管 | 巴西成人队列（规模未明确） | [链接](https://www.elsa.org.br/) | restricted | 2 | 作为外部前瞻队列验证单导联AI-ECG心衰风险分层。 |
| **ESTHER** | 数据集 | #心血管 | 5,578-8,308人 |  | unknown | 2 | 德国队列，用于代谢组学心血管风险预测的外部验证。 |
| **Genecorpus-30M** | 数据集 | #单细胞 | 约3000万细胞 |  | unknown | 2 | 作为scFM预训练语料，用于审计基准污染及Geneformer预训练。 |
| **JetClass** | 数据集 | #世界模型 | 1亿个喷注 | 项目网站公开 | yes | 2 | 用于预训练HEP-JEPA高能物理基础模型并评估top tagging等下游任务。 |
| **ScanObjectNN** | 数据集 | #世界模型 | 15类、约15000样本 | [链接](https://hkust-vgd.github.io/scanobjectnn/) | yes | 2 | 用于评估点云掩码自编码器在真实扫描物体分类上的下游性能。 |
| **AudioSet** | 数据集 | #世界模型 | 无标签音频片段 | [链接](https://research.google.com/audioset/) | yes | 1 | 用于Audio-JEPA的无标签预训练，学习掩码梅尔频谱块的隐表征。 |
| **FEVER** | 数据集 | #Agent | 约18万条声明 | [链接](https://fever.ai/) | yes | 1 | 用于评测ReAct在事实核查任务中的表现。 |
| **GTEx** | 数据集 | #衰老 | 581样本 | [链接](https://gtexportal.org/) | yes | 1 | 用于分析TFMethyl Clock靶基因表达。 |
| **HotpotQA** | 数据集 | #Agent | 约11万问答对 | [链接](https://hotpotqa.github.io/) | yes | 1 | 用于评测ReAct在知识密集型多跳问答中的推理与行动协同能力。 |
| **Libri-light** | 数据集 | #世界模型 | 60000小时 | [链接](https://github.com/facebookresearch/libri-light) | yes | 1 | 用于大规模无标注语音预训练及多规模微调评估HuBERT。 |
| **Librispeech** | 数据集 | #世界模型 | 960小时 | [链接](https://www.openslr.org/12) | yes | 1 | 用于微调和评估HuBERT语音表征在语音识别任务上的性能。 |
| **LVIS** | 数据集 | #世界模型 | 约16万图像，1200+类 | [链接](https://www.lvisdataset.org/) | yes | 1 | 用于评估SiameseIM在长尾实例分割任务上的迁移性能。 |
| **MATH500** | 数据集 | #Agent | 500题 | [链接](https://github.com/openai/prm800k) | yes | 1 | 用于评测BiPRM在解级数学推理上的表现。 |
| **MNIST** | 数据集 | #世界模型 | 7万张28x28图像 | [链接](http://yann.lecun.com/exdb/mnist/) | yes | 1 | 用于BiJEPA验证双向JEPA在图像数据上的稳定收敛与表征学习。 |
| **MODIS** | 数据集 | #世界模型 | 全球覆盖卫星影像 | [链接](https://modis.gsfc.nasa.gov/) | yes | 1 | 作为Mini-JEPA舰队中热红外传感器模型的训练与预测数据源。 |
| **PRM800K** | 数据集 | #Agent | 80万步级标签 | [链接](https://github.com/openai/prm800k) | yes | 1 | 用于训练过程奖励模型PURE。 |
| **SaMi-Trop** | 数据集 | #心血管 | 1631人 | [链接](https://doi.org/10.1371/journal.pntd.0006847) | yes | 1 | 作为ECG死亡风险模型的国际外部验证队列。 |
| **Qwen3-4B** | 模型 | #Agent | 4B参数 | [链接](https://huggingface.co/Qwen/Qwen3-4B) | yes | 3 | 用于RLVR信用分配与GEAR优势重加权实验的基础模型。 |
| **Qwen2.5-Math-7B** | 模型 | #Agent | 70亿参数 | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-7B) | yes | 2 | 作为PURE与ScalePRM的基座模型进行推理强化学习。 |
| **Qwen3-1.7B** | 模型 | #Agent | 1.7B参数 | [链接](https://huggingface.co/Qwen/Qwen3-1.7B) | yes | 2 | 用于评估TEMPO与P2T信用分配方法的基座模型。 |
| **Qwen3-8B** | 模型 | #Agent | 8B参数 |  | yes | 2 | 用于RLVR信用分配与GEAR优势重加权实验的基础模型。 |
| **ADVANCE** | 模型 | #心血管 | T2D CVD风险模型 | [链接](https://doi.org/10.1016/S0140-6736(07)61014-9) | yes | 1 | 作为中国T2DM患者CVD风险预测的对比模型。 |
| **data2vec** | 模型 | #世界模型 | 通用自监督模型 | [链接](https://github.com/facebookresearch/fairseq/tree/main/examples/data2vec) | yes | 1 | 作为Audio-JEPA的对比基线，比较音频表征学习性能。 |
| **DINO** | 模型 | #世界模型 | ViT-Base线性评估80.1% | [链接](https://github.com/facebookresearch/dino) | yes | 1 | 无标签自蒸馏自监督方法，赋予ViT显式语义分割特性。 |
| **Flow-JEPA** | 模型 | #世界模型 | 四个环境 | [链接](https://arxiv.org/abs/2608.29029) | yes | 1 | 用条件流匹配生成未来潜状态序列的JEPA世界模型。 |
| **GenePT** | 模型 | #单细胞 | GPT-3.5嵌入，无需预训练 | [链接](https://doi.org/10.1101/2023.10.16.562533) | yes | 1 | 用GPT-3.5基于NCBI基因文本描述生成基因与单细胞嵌入的基础模型。 |
| **Graph-JEPA** | 模型 | #世界模型 | 图级表征 | [链接](https://github.com/geriskenderi/graph-jepa) | yes | 1 | 用于图级表征学习的联合嵌入预测架构模型，支持图分类与回归。 |
| **GraphCL** | 模型 | #世界模型 | 未明确 | [链接](https://arxiv.org/abs/2010.13902) | yes | 1 | 图对比学习框架，用于无监督图表征学习。 |
| **HuBERT** | 模型 | #世界模型 | 最大1B参数 | [链接](https://github.com/facebookresearch/fairseq/tree/main/examples/hubert) | yes | 1 | 提出并发布的语音自监督预训练模型，用于掩码隐藏单元预测学习语音表征。 |
| **Intuitor** | 模型 | #Agent | 基于GRPO的无监督RL方法 | [链接](https://github.com/sunblaze-ucb/Intuitor) | yes | 1 | 用模型自身置信度作为唯一奖励信号的无监督强化学习方法。 |
| **LaMamba-Diff** | 模型 | #世界模型 | ImageNet 256/512，线性复杂度 | [链接](https://github.com/) | yes | 1 | 融合局部注意力与Mamba的线性时间高保真扩散生成模型。 |
| **MAE** | 模型 | #世界模型 | ViT-Huge，ImageNet-1K达87.8% | [链接](https://github.com/facebookresearch/mae) | yes | 1 | 掩码自编码器，通过重建缺失图像块实现可扩展视觉自监督预训练。 |
| **MoCo** | 模型 | #世界模型 | ResNet-50骨干，ImageNet预训练 | [链接](https://github.com/facebookresearch/moco) | yes | 1 | 提出动量对比学习框架，构建动态字典进行无监督视觉表征学习。 |
| **Plan2Explore** | 模型 | #世界模型 | 未明确 | [链接](https://arxiv.org/abs/2005.05960) | yes | 1 | 通过规划主动探索的自监督世界模型智能体。 |
| **Point-Delta-JEPA** | 模型 | #世界模型 | 未明确 | [链接](https://arxiv.org/abs/2608.29434) | yes | 1 | 在几何移动最多时表现最强的点云JEPA世界模型。 |
| **Point-JEPA** | 模型 | #世界模型 | 点云块嵌入 | [链接](https://github.com/Ayumu-J-S/Point-JEPA) | yes | 1 | 面向点云的联合嵌入预测架构模型，用于自监督点云表征学习。 |
| **Point-LeWM** | 模型 | #世界模型 | 未明确 | [链接](https://arxiv.org/abs/2608.29434) | yes | 1 | 点云观测下的JEPA世界模型设计，与图像基线统计等价。 |
| **SAM (Segment Anything Model)** | 模型 | #类器官 | 十亿级掩码预训练 | [链接](https://github.com/facebookresearch/segment-anything) | yes | 1 | 用于PDO延时显微视频中类器官的分割。 |
| **SANA-WM** | 模型 | #世界模型 | 2.6B参数 | [链接](https://doi.org/10.48550/arXiv.2605.15178) | yes | 1 | 开源世界模型，支持一分钟720p视频生成与精确相机控制。 |
| **wav2vec 2.0** | 模型 | #世界模型 | 预训练语音模型 | [链接](https://github.com/facebookresearch/fairseq/tree/main/examples/wav2vec) | yes | 1 | 作为Audio-JEPA的对比基线，比较音频表征学习性能。 |
| **ALFWorld** | 基准 | #Agent | 6类任务、数千回合 | [链接](https://alfworld.github.io/) | yes | 4 | 用于评估MetaSkill-Evolve智能体技能自进化框架的基准之一。 |
| **MMLU** | 基准 | #Agent #世界模型 | 57学科多选题基准 | [链接](https://github.com/hendrycks/test) | yes | 2 | 用于评估DLLM-JEPA在多学科知识任务上的性能。 |
| **ProcessBench** | 基准 | #Agent | 3400条推理路径 | [链接](https://huggingface.co/datasets/Qwen/ProcessBench) | yes | 2 | 用于评测BiPRM与ScalePRM的步级错误检测能力。 |
| **scIB** | 基准 | #单细胞 | 13任务，最多100万细胞 |  | unknown | 2 | 单细胞数据整合基准，用于评估批次去除与生物变异保留。 |
| **WebShop** | 基准 | #Agent | 约120万商品 | [链接](https://webshop-pnlp.github.io/) | yes | 2 | 用于评估SELAUR智能体在网页购物任务上的成功率。 |
| **AI4AI-Bench** | 基准 | #Agent | 10仓库×29配置×6系统×10任务 | [链接](https://arxiv.org/abs/2608.20318) | yes | 1 | 评测LLM智能体改写训练算法的递归自我改进基准，含公开任务套件与评估器。 |
| **BIRD** | 基准 | #Agent | 大规模跨域text-to-SQL基准 | [链接](https://bird-bench.github.io/) | yes | 1 | 用于评估记忆型自改进智能体的执行准确率与奖励膨胀问题。 |
| **GSM-HARD** | 基准 | #Agent | 未明确 | [链接](https://github.com/openai/grade-school-math) | yes | 1 | 用于评估分布外数学推理泛化能力。 |
| **MedMCQA** | 基准 | #Agent | 未明确 | [链接](https://medmcqa.github.io/) | yes | 1 | 用于评估分布外医学推理泛化能力。 |
| **MedQA** | 基准 | #Agent | 未明确 | [链接](https://github.com/jind11/MedQA) | yes | 1 | 用于评估医学推理能力的分布内基准。 |
| **NKIBench** | 基准 | #Agent | 来自真实LLM工作负载的Trainium内核 | [链接](https://github.com/zhang677/AccelOpt) | yes | 1 | 用于评测LLM智能体自主优化AWS Trainium内核的性能。 |
| **PASCAL VOC** | 基准 | #世界模型 | 约1.1万图像，20类 | [链接](http://host.robots.ox.ac.uk/pascal/VOC/) | yes | 1 | 用于评估MoCo无监督预训练在检测与分割任务上的迁移性能。 |
| **PushT** | 基准 | #世界模型 | 推T形块操作任务 | [链接](https://github.com/huggingface/gym-pusht) | yes | 1 | 用于评估D-JEPA在机器人操作任务上的动作选择成功率。 |
| **R-Judge** | 基准 | #Agent | 569条交互记录，27类风险场景 | [链接](https://github.com/Lordog/R-Judge) | yes | 1 | 用于评测LLM智能体在交互环境中的安全风险意识。 |
| **RoboTwin** | 基准 | #世界模型 | 双臂机器人操作基准 | [链接](https://robotwin-platform.github.io/) | yes | 1 | 用于评估D-JEPA在机器人操作任务上的决策对齐性能。 |
| **SKILLMISEVO-BENCH** | 基准 | #Agent | 冻结基准，含恶意/良性/延续任务 | [链接](https://github.com/henrymao2004/misevolve) | yes | 1 | 冻结基准，用于评估技能误演化导致的不安全行为。 |
| **SKILLMISEVO-GYM** | 基准 | #Agent | 25种配置，各525任务、25回合 | [链接](https://github.com/henrymao2004/misevolve) | yes | 1 | 生命周期感知测试台，用于研究自改进智能体的技能误演化。 |
| **Socratic-PRMBench** | 基准 | #Agent | 2995条缺陷路径 | [链接](https://github.com/Xiang-Li-oss/Socratic-PRMBench) | yes | 1 | 用于系统评测PRM在六种推理模式下的过程错误检测能力。 |
| **StreamBench** | 基准 | #Agent | 在线学习环境，多任务序列 | [链接](https://github.com/stream-bench/stream-bench) | yes | 1 | 评估LLM智能体在连续反馈流中持续改进能力的基准。 |
| **Allen Brain Atlas** | 数据库 | #单细胞 | 全脑空间转录组图谱 | [链接](https://portal.brain-map.org/) | yes | 1 | 用于参数化细胞行为规则语法，构建脑发育相关的虚拟细胞模型。 |
| **EMBL-EBI ArrayExpress** | 数据库 | #衰老 | 51项人类干预研究 | [链接](https://www.ebi.ac.uk/biostudies/arrayexpress) | yes | 1 | 提供表观遗传衰老生物标志物响应性分析所用的公开DNAm数据。 |
| **GeneATLAS** | 数据库 | #人群队列 | 452,264人，778性状，9,113,133变异 | [链接](http://geneatlas.roslin.ed.ac.uk) | yes | 1 | UK Biobank遗传关联图谱数据库，供统一查询GWAS结果。 |
| **CellProfiler** | 工具 | #单细胞 | 图像分析软件 |  | yes | 2 | 提取传统手工图像特征并与深度学习特征比较。 |

## 单篇提及（364，未进主表）

- 数据集：23andMe、23andMe BMI GWAS、ADE20K、ADVANCE Trial、AIDA v2、Age, Gene/Environment Susceptibility-Reykjavik Study (AGES)、Asian Indian Diabetes Heart Study / Sikh Diabetes Study (AIDHS/SDS)、AudioSet-20K、CHARGE-AF Consortium、CHOP、COCO-Stuff、CODE (Brazilian ECG Dataset, 2.3M ECGs)、ChinaHEART、Cityscapes、Copenhagen General Population Study、DFTJ、Danish National Patient Registry、Droid、ELAN、EPIC-Norfolk、ESC-50、Estonian Biobank、FINRISK、FSD50K、Fenland、Framingham Offspring Study、GDSC、GIANT Consortium BMI GWAS、GSE67752、GSM-Plus、Geisinger ECG Cohort、Generation Scotland、HEEDB、HM3D v0.2、I-SPY2、INSPIRE-T、ImageNet ILSVRC-2012、Integrated Mega-scale Atlas、Israel 10K Project、JUMP-MOA、JUMP-lite、Jiangsu Behavioral and Physical Chronic Disease Cohort (JBPCD)、KORA、Lorenz attractor、Lothian Birth Cohort 1936、MERFISH whole mouse brain atlas、MGB (Mass General Brigham) ECG Cohort、MGB Biobank、MIMIC、MIMIC-III、MIMIC-IV-ECG、Mexico City Prospective Study (MCPS)、NHANES、NLST、NPBBD-Korea、Norman K562 CRISPRa、Norman Perturb-seq、Norman19、Nurses' Health Study、Olink Proteomics Panel (UK Biobank)、PRECISE、Perturb-seq genome-scale screen、PerturbReason、Robomimic、Rotterdam Study、SCIPRM70K、SEA-AD、SHIP-START、SHIP-TREND、ST-bank、Sentinel-1、Sentinel-2、SpatialCorpus-110M、Tabula Sapiens、Taiwan Precision Medicine Initiative (TPMI)、Tox21、TruDiagnostic、UCLA Biobank、UHN-ECG、UK Biobank ECG Interval Reference Dataset
- 模型：AI-HF、AIRE、ALADYNOULLI、AROMA、ASCVD-IRT、ASCVD-PCE、ATM (Age-dependent Topic Model)、AdaptAge、AlphaEarth、AlphaFold3、Audio-MAE、BEHRT、BYOL、Bootleg、BrainBeacon、CAME、CARDIAC-FM、CLM-X、CMAE、CPA、CTBA、CTransPath、Cell-o1、CellFM、CellFlux、CellFluxRL、CellOT、CellWorld、China-AIHeart、Co-Scientist、CrossJEPA、D-SPIN、D2R2、DINO-WM、DINOv2、DNAm PhenoAge、DNAmEMRAge、DamAge、DeepSeek-R1、DeepSeek-R1-Zero、DeepSeekMath 7B、Delphi-2M、Delta V、DiRL、ECG-AI、ECG-FM、ECG-LFM、ECG2CAD、EHR-MPC、EMRAge、Echo2HF、Extracellular Matrix Aging Clock、Foresight、Foresight-England、GLAM、GLAM NAV、GOLD BioAge、GPS Mult、GRASP、GenReasoner、GeneCompass、GenoAgent、HEP-JEPA、Hannum DNAm Age Clock、Healthspan Proteomic Score (HPS)、Horvath clock、JEPA-Anything、Kimi k1.5、LeJEPA、LeVJEPA、LinAge2、Longitudinal Proteomic Aging Index (LPAI)、LucaCell、MC-JEPA、MILTON、ML-CVD-C、MSGene、MSKAge、Med-BERT、Med-R1
- 基准：ABC-Bench、AdaJEPA、BLADE、Baba in Wonderland、BioDataLab、BioKGBench、BiomniBench-DA、CellPuzzles、ComputAgeBench、D4RL、DiscoverPhysics、Gaia2、HLE、HumanEval、LMR-BENCH、LOGIQA、LiveCodeBench、Longevity Bench、MMLU-Medical、MedPRMBench、MemCalib、OfficeQA、PARADIGM-HF、PertEval-scFM、PerturBench、RSIBench-Data、SEAGym、SWE Bench Verified、SciIntegrity-Bench、ScienceAgentBench、SealQA、SoundnessBench、Terminal-Bench 2.0、ToolMaker Benchmark、VTAB、Virtual Cell Challenge、Virtual Cell Challenge 2026、X-ARES、scEval
- 数据库：CMAP、CPRD、CPRD Aurum、Cell Landscape、ENCODE、Immunosenescence Inventory、MEDICINE portal、STP、TCGA、TEAPEE
- 工具：AusCVDRisk、AutoPrognosis、BASIL、BAVAR、BOLT-LMM、BioLLM、Biolearn、CINEMA-OT、CODRP、CROP-seq、CellDuality、CellPaint-POSH、CellScientist、ClockBase Agent、DALE、DeGAs、FaithRL、GATK、GEPA、Habitat、Hail、Harmony、ICD-8 to ICD-10 Mapping、K-Dense、LUCID、LWD-Miniscope、LivAge、Loki、Longevity Claw、MatClaw、Mortara VERITAS Algorithm、Mosaic、Nahual、OSCAR、Olink Explore 3072、Olink Proteomics、P2T、PHESANT、PRS-CS、PheMIME、PheWeb、Phecodes、REGENIE、SAFEEVOLVE、SAIGE-GENE、SCOPE (Systematic Classification of Organoids for Phenotypic Evaluation)、SCanSNP、SO-GRPO、SO-PPO、SORL、SPAC-seq、SenePy、SomaLogic、SpatialQM、TARDIS、TEMPO、TFActProfiler、The AI Scientist、Tool-GRPO、TotalSegmentator、TranslAGE、TreeRL、Trellis、UKB-MDRMF、associationSubgraphs、copairs、leakcheck、moscot、scContam、ukbnmr
