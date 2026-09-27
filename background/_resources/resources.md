# 资源登记（数据集 / 模型 / 基准）

从 778 处证据引用中挖出 505 项命名资源；主表 135 项（被 ≥2 篇工作使用、或跨方向、或开放且链接核验通过且规模明确），其余 370 项单篇提及的列在末尾。核验：ok 可达 / blocked 站点拒绝探测 / dead 失效 / n/a 非链接。更新 2026-09-27


## P0 优先上手（16）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **UK Biobank** | 数据集 | #衰老 #心血管 #人群队列 | 30,376人；2,923蛋白+251代谢物 | [链接](https://www.ukbiobank.ac.uk/) | restricted | 113 | 多组学衰老与CVD方法迁移主数据源，ChinaHEART参照基准 |
| **UKB-PPP** | 数据集 | #心血管 #人群队列 | 54,219人 / 2,923蛋白 | [链接](https://www.ukbiobank.ac.uk/) | restricted | 11 | UKB蛋白组，ChinaHEART蛋白组CVD风险迁移参照 |
| **Tahoe-100M** | 数据集 | #单细胞 #虚拟细胞 | 1亿转录组，50细胞系，1100药物条件 | [链接](https://huggingface.co/datasets/tahoebio/Tahoe-100M) | yes | 4 | 亿级药物扰动图谱，虚拟扰动预训练与类器官demo核心数据 |
| **Replogle 2022 Perturb-seq** | 数据集 | #虚拟细胞 | >250万人类细胞 | doi:10.1016/j.cell.2022.05.013 | yes | 2 | 基因组规模Perturb-seq，扰动预测建模与基准评估核心数据 |
| **Pan-UK Biobank GWAS summary statistics** | 数据集 | #人群队列 | 7,271表型，多祖源 | [链接](https://pan.ukbb.broadinstitute.org/) | yes | 1 | 跨祖源GWAS汇总，ChinaHEART迁移与PRS跨人群校正 |
| **scGPT** | 模型 | #类器官 #单细胞 #虚拟细胞 | 预训练3300万+细胞 | [链接](https://doi.org/10.1038/s41592-024-02201-0) | yes | 17 | 单细胞基础模型基线，类器官衰老demo与虚拟扰动对标 |
| **Geneformer** | 模型 | #单细胞 #虚拟细胞 | V2-316M，约316M参数 | [链接](https://huggingface.co/ctheodoris/Geneformer) | yes | 12 | 单细胞基础模型基线，类器官衰老demo与虚拟扰动建模直接对标 |
| **scFoundation** | 模型 | #单细胞 #虚拟细胞 | 5000万细胞/1亿参数 | [链接](https://github.com/biomap-research/scFoundation) | yes | 8 | 扰动预测基准模型，类器官扰动demo可直接部署对比 |
| **China-PAR** | 模型 | #心血管 | 推导21320人，验证84961人 |  | unknown | 4 | 中国CVD风险模型，ChinaHEART迁移必比对照 |
| **Tahoe-X1** | 模型 | #单细胞 | 未明确（基础模型） | 公开预训练权重、训练代码与评估流程 | yes | 3 | 扰动训练单细胞基础模型，虚拟扰动响应建模首选基线 |
| **Chreode** | 模型 | #单细胞 #虚拟细胞 | 240万细胞小鼠胚胎图谱预训练 | [链接](https://doi.org/10.48550/arxiv.2605.28111) | unknown | 2 | 细胞世界模型，虚拟扰动响应与类器官时序建模直接参照 |
| **SCALE** | 模型 | #单细胞 #虚拟细胞 | CRISPR/化学/发育/免疫扰动 |  | unknown | 1 | 条件传输虚拟扰动模型，类器官扰动响应建模直接可用 |
| **LongevityBench** | 基准 | #衰老 | 17项任务/5个数据域 | [链接](https://doi.org/10.1016/j.cell.2026.08.026) | yes | 1 | 衰老AI基准，类器官衰老demo与虚拟扰动建模的对标评测 |
| **CZ CELLxGENE Discover** | 数据库 | #衰老 | 超7000万细胞 | [链接](https://cellxgene.cziscience.com) | yes | 1 | 单细胞图谱，训练类器官/单细胞衰老时钟的公开数据 |
| **Proteome-Phenome Atlas** | 数据库 | #人群队列 | 53,026人，2,920蛋白，406+660疾病 | [链接](https://proteome-phenome-atlas.com) | yes | 1 | 开放蛋白组-疾病图谱，ChinaHEART蛋白组关联查询与验证 |
| **Cell Painting** | 工具 | #衰老 #单细胞 | 十年积累的公开图像profiling数据 | [链接](https://jump-cellpainting.broadinstitute.org/) | yes | 3 | 细胞形态扰动响应，类器官+cell painting扰动建模核心 |

## P1 值得登记（62）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **All of Us Research Program** | 数据集 | #人群队列 | 39.4万人（含24.5万WGS） | [链接](https://allofus.nih.gov/) | restricted | 11 | 多血统EHR+基因组，PRS与EHR关联复制方法参照 |
| **China Kadoorie Biobank** | 数据集 | #衰老 #心血管 #人群队列 | 约51万人（本组文献用2.5万–4.3万） | [链接](https://www.ckbiobank.org/) | restricted | 8 | 中国人群队列，CVD风险模型跨国验证与迁移参照 |
| **UK Biobank Exome Sequencing** | 数据集 | #人群队列 | 454,787人/12.3M变异 | [链接](https://www.ukbiobank.ac.uk/) | restricted | 4 | UKB外显子数据，ChinaHEART遗传-多组学整合方法迁移参照。 |
| **ARIC** | 数据集 | #心血管 #人群队列 | V3 10,638人；V5 3,908人 | [链接](https://aric.cscc.unc.edu/) | restricted | 3 | 蛋白组心衰/衰弱队列，ChinaHEART蛋白组参照 |
| **MESA** | 数据集 | #心血管 #人群队列 | 6814人，随访12年 | [链接](https://www.mesa-nhlbi.org/) | restricted | 3 | 多模态CVD队列，心血管基础模型外部验证 |
| **Framingham Heart Study** | 数据集 | #衰老 #心血管 | 10,097人，28,151份ECG | [链接](https://www.framinghamheartstudy.org/) | restricted | 2 | ECG-AF深度学习经典队列，心血管AI模型对标 |
| **CHARLS** | 数据集 | #心血管 | 约23,000人 / 9年随访 | [链接](http://charls.pku.edu.cn/) | restricted | 2 | 中国队列，ChinaHEART迁移与AI-ECG外部验证 |
| **Global Biobank Meta-analysis Initiative (GBMI)** | 数据集 | #人群队列 | 23库，220万人，14终点 | 汇总统计可申请 | restricted | 2 | 跨库荟萃资源，跨祖源PRS评估方法参照 |
| **THL Biobank** | 数据集 | #人群队列 | 参与三国生物库共700,217人 | [链接](https://thl.fi/en/web/thl-biobank) | restricted | 2 | NMR代谢组重复验证队列，ChinaHEART代谢标志物外部参照 |
| **SpeciesCorpus** | 数据集 | #类器官 #单细胞 #虚拟细胞 | 1.31亿细胞 |  | unknown | 1 | 跨物种单细胞语料，可预训练虚拟细胞模型支撑类器官与扰动。 |
| **CeNGEN** | 数据集 | #衰老 | 128种神经元类型 | [链接](https://www.cengen.org/) | yes | 1 | 线虫神经元转录组，模式生物虚拟扰动与衰老时钟 |
| **CTRP** | 数据集 | #虚拟细胞 | 大型单药药物基因组面板 | [链接](https://portals.broadinstitute.org/ctrp) | yes | 1 | 药物基因组学面板，盲响应预测泛化评估 |
| **JUMP-MOA** | 数据集 | #单细胞 | 参考板/多MoA | [链接](https://jump-cellpainting.broadinstitute.org/) | yes | 1 | Cell Painting参考数据，类器官图像+ML扰动检索评估。 |
| **MIMIC-IV-ECG** | 数据集 | #心血管 | 约80万份ECG | [链接](https://physionet.org/content/mimic-iv-ecg/) | yes | 1 | 80万ECG公开数据，可预训练ECG基础模型用于心血管队列。 |
| **SEA-AD** | 数据集 | #单细胞 | 340万核/84供体 | [链接](https://sea-ad.org/) | yes | 1 | 多模态脑图谱，可迁移到类器官多模态衰老整合方法。 |
| **Tabula Sapiens** | 数据集 | #单细胞 | 564,253细胞，多供体 | [链接](https://tabula-sapiens-portal.ds.czbiohub.org) | yes | 1 | 多供体单细胞图谱，可作类器官与虚拟细胞表征基准。 |
| **SCORE2** | 模型 | #心血管 | 45队列67.8万人建模 | [链接](https://www.escardio.org/Education/Practice-Tools/CVD-prevention-toolbox/SCORE-Risk-Charts) | yes | 6 | 欧洲CVD风险基线，ChinaHEART模型对标 |
| **GEARS** | 模型 | #单细胞 #虚拟细胞 | 图神经网络扰动模型 | [链接](https://github.com/snap-stanford/GEARS) | yes | 3 | 扰动预测可迁移基线，虚拟扰动建模对比方法 |
| **TranscriptFormer** | 模型 | #类器官 #单细胞 | 1.12亿细胞、12物种 | [链接](https://github.com/czi-ai/transcriptformer) | yes | 3 | 跨物种虚拟细胞图谱，虚拟扰动与跨物种迁移参照 |
| **CHARGE-AF** | 模型 | #心血管 | 房颤风险预测评分 | [链接](https://www.chargeaf.org/) | yes | 3 | 房颤风险模型，AI-ECG与蛋白组评分比较基线 |
| **PREVENT** | 模型 | #心血管 | 美国人群CVD风险方程 | [链接](https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.123.067626) | yes | 3 | AHA风险方程，蛋白组评分增量比较基线 |
| **QRISK3** | 模型 | #心血管 | QResearch 1998-2015开放队列 | [链接](https://qrisk.org/three/) | yes | 3 | 英国CVD风险模型，蛋白组增量比较基线 |
| **SCimilarity** | 模型 | #单细胞 | 2270 万细胞、399 项研究 | [链接](https://github.com/Genentech/SCimilarity) | yes | 3 | 细胞表示基础模型，跨队列细胞注释与状态查询可用 |
| **DISCO** | 模型 | #心血管 #虚拟细胞 | 大规模整合RNA-seq图谱 | [链接](https://www.immunesinglecell.org/disco) | yes | 2 | ECG嵌入表型匹配，虚拟扰动与治疗效应模拟思路 |
| **UCE (Universal Cell Embeddings)** | 模型 | #类器官 #单细胞 | 3600万细胞预训练 | [链接](https://github.com/snap-stanford/UCE) | yes | 2 | 免微调细胞嵌入，类器官衰老demo可作基线表征 |
| **CellPLM** | 模型 | #单细胞 | 细胞语言模型基础模型 | [链接](https://github.com/OmicsML/CellPLM) | yes | 2 | scEval最佳基础模型之一，类器官单细胞建模候选 |
| **ECG-AI** | 模型 | #心血管 | UKB 48300配对ECG-CMR |  | unknown | 2 | UKB ECG-CMR配对模型，可作ChinaHEART心血管多模态风险预测参照。 |
| **Horvath DNAm Age Clock** | 模型 | #衰老 | 353 CpG，7844样本 |  | unknown | 2 | DNAm年龄基线时钟，类器官衰老demo必比基线 |
| **Longevity-LLM** | 模型 | #衰老 | 0.6B-9B参数，5个模型 | [链接](https://doi.org/10.1016/j.cell.2026.08.026) | yes | 2 | 衰老组学基础模型，可微调做表观年龄与多模态衰老表征 |
| **Reti-CVD** | 模型 | #心血管 | UK Biobank 44,677人验证 |  | unknown | 2 | 视网膜图像CVD评分，多模态风险分层可迁移 |
| **Speciesformer** | 模型 | #类器官 #单细胞 #虚拟细胞 | 在1.31亿细胞上预训练 |  | unknown | 1 | 跨物种虚拟细胞基础模型，直接对标虚拟扰动响应建模基线。 |
| **RegFormer** | 模型 | #单细胞 #世界模型 | 2500 万人类细胞预训练 |  | unknown | 1 | 融合GRN先验的扰动预测模型，虚拟扰动建模可迁移 |
| **CPA** | 模型 | #单细胞 | 组合扰动自编码器 | [链接](https://github.com/theislab/cpa) | yes | 1 | 组合扰动自编码器，虚拟扰动预测必对标基线。 |
| **GenoAgent** | 模型 | #Agent | 未明确 | [链接](https://github.com/Liu-Hy/GenoTEX) | yes | 1 | 多智能体基因分析框架，可作科研智能体工作流基线。 |
| **GET** | 模型 | #虚拟细胞 | 单细胞转录组基础模型 | [链接](https://github.com/GET-Foundation/get_model) | yes | 1 | 代表性虚拟细胞基础模型，扰动建模对标 |
| **I-JEPA** | 模型 | #世界模型 | ViT-Huge/14，ImageNet预训练 | [链接](https://github.com/facebookresearch/ijepa) | yes | 1 | I-JEPA 是自监督表征范式基线，可迁移到类器官图像与组学 |
| **Mondrian Cross-Conformal Prediction (MCCP)** | 模型 | #心血管 | 算法框架 | [链接](https://doi.org/10.1371/journal.pcbi.1014670) | yes | 1 | 跨祖源PRS不确定性框架，可迁移到ChinaHEART风险预测。 |
| **OmiCLIP** | 模型 | #单细胞 | 基于220万配对patch训练 | [链接](https://doi.org/10.1038/s41592-025-02707-1) | yes | 1 | 图像-转录组对齐模型，类器官多模态衰老建模参照 |
| **scGen** | 模型 | #虚拟细胞 | VAE潜空间扰动向量 | [链接](https://doi.org/10.1038/s41592-019-0494-8) | yes | 1 | 潜空间扰动向量预测，虚拟扰动建模经典基线 |
| **scMulan** | 模型 | #单细胞 | 多任务生成式基础模型 | [链接](https://github.com/SuperBianC/scMulan) | yes | 1 | 生成式单细胞基础模型，低监督扰动预测对标基线。 |
| **scVI** | 模型 | #单细胞 | 变分自编码器 | [链接](https://github.com/scverse/scvi-tools) | yes | 1 | 单细胞嵌入经典基线，类器官与虚拟细胞建模对照。 |
| **scArchon** | 基准 | #单细胞 #虚拟细胞 | 9种工具，多样本数据集 | [链接](https://doi.org/10.1186/s13059-026-04104-z) | yes | 1 | 扰动预测标准化基准，虚拟扰动建模评测直接可用 |
| **VCBench** | 基准 | #类器官 #单细胞 | 5个基础模型+线性/KNN基线，7维度 |  | unknown | 1 | 单细胞基础模型评测基准，选型与对标时参照 |
| **ASSAYBENCH** | 基准 | #虚拟细胞 | 1920个筛选，约13826基因/筛选 | [链接](https://github.com/Genentech/AssayBench) | yes | 1 | CRISPR表型预测基准，评估智能体虚拟细胞能力 |
| **GenoTEX** | 基准 | #Agent | 含专家标注代码与结果 | [链接](https://github.com/Liu-Hy/GenoTEX) | yes | 1 | 基因表达分析智能体基准，LLM科研工作流直接对标 |
| **ProteinGym** | 基准 | #Agent | 217个DMS assay | [链接](https://proteingym.org) | yes | 1 | 蛋白适应度基准，虚拟扰动与蛋白语言模型对标 |
| **TruthInsightBench** | 基准 | #Agent | 40个盲任务/10领域/40篇论文 | [链接](https://github.com/TruthInsight-stack/TruthInsightBench) | yes | 1 | 科学发现智能体评测，科研智能体工作流可参照 |
| **MEDICINE portal** | 数据库 | #衰老 #人群队列 | 5个器官MetBAG模型 | MEDICINE门户 | yes | 2 | 多器官代谢组衰老时钟可迁移到类器官衰老demo与ChinaHEART衰老建模。 |
| **ARCHS4** | 数据库 | #衰老 | 约5.7万样本，28组织，1-114岁 | [链接](https://maayanlab.cloud/archs4/) | yes | 2 | 跨年龄RNA-seq，转录组衰老时钟训练验证数据 |
| **Human Cell Atlas** | 数据库 | #单细胞 | 全球细胞图谱计划 | Human Cell Atlas门户 | yes | 2 | 细胞图谱资源，类器官衰老demo参照与跨组织整合 |
| **ChIP-Atlas** | 数据库 | #虚拟细胞 | 大规模TF结合图谱 | [链接](https://chip-atlas.org) | yes | 1 | TF结合先验，虚拟扰动建模调控推断可用 |
| **CMAP (Connectivity Map)** | 数据库 | #单细胞 | 百万级表达谱 | [链接](https://clue.io/) | yes | 1 | 药物扰动转录组库，虚拟扰动响应建模与药物匹配核心资源。 |
| **CollecTRI** | 数据库 | #虚拟细胞 | 多物种TF-靶基因网络 | [链接](https://github.com/saezlab/CollecTRI) | yes | 1 | TF调控网络先验，扰动预测带符号系数学习 |
| **NHGRI-EBI GWAS Catalog** | 数据库 | #人群队列 | 625,113关联、>85K数据集 | [链接](https://www.ebi.ac.uk/gwas/) | yes | 1 | GWAS汇总统计标准库，ChinaHEART遗传关联查询 |
| **PGS Catalog** | 数据库 | #人群队列 | 未明确 | [链接](https://www.pgscatalog.org/) | yes | 1 | 多基因评分库，ChinaHEART PRS构建与迁移参照 |
| **PhysioNet** | 数据库 | #心血管 | 公开生理信号数据库 | [链接](https://physionet.org/) | yes | 1 | 生理信号门户，ECG基础模型预训练与基准 |
| **Perturb-seq** | 工具 | #单细胞 #虚拟细胞 | pooled CRISPR筛选 |  | unknown | 4 | CRISPR扰动数据，虚拟扰动建模训练与基准 |
| **SomaScan** | 工具 | #衰老 #心血管 | 4,877个aptamer | [链接](https://somalogic.com/) | restricted | 3 | 血浆蛋白组平台，ChinaHEART蛋白组衰老建模参照 |
| **Olink Proteomics** | 工具 | #心血管 | 1,459-2,920蛋白panel | [链接](https://www.olink.com/) | no | 3 | 血浆蛋白组平台，ChinaHEART蛋白组风险预测选型参考。 |
| **Olink** | 工具 | #心血管 #人群队列 | 2,920蛋白 | [链接](https://www.olink.com/) | no | 2 | 蛋白组检测平台，ChinaHEART蛋白组方案参照 |
| **Trellis** | 工具 | #类器官 | >2500个CRC PDO与CAF |  | unknown | 2 | 类器官药物响应分析方法，可直接用于类器官扰动响应建模。 |
| **Perturb-FISH** | 工具 | #类器官 #单细胞 | THP1/hIPSC/异种移植3D组织 |  | unknown | 1 | 空间扰动读取思路，可用于类器官虚拟扰动建模设计 |

## P2 了解即可（57）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **ImageNet-1K** | 数据集 | #世界模型 | 约128万训练图像，1000类 | [链接](https://www.image-net.org/) | yes | 8 | 作为自监督预训练与线性评估的主基准数据集。 |
| **ModelNet40** | 数据集 | #世界模型 | 40类三维模型 | [链接](https://modelnet.cs.princeton.edu/) | yes | 4 | 用于点云自监督方法的线性分类与少样本分类评估。 |
| **Mass General Brigham Biobank** | 数据集 | #心血管 #人群队列 | 约5.3万例（670例颈动脉狭窄） | [链接](https://www.massgeneralbrigham.org/en/research/innovation/biobank) | restricted | 3 | 用于评估CAD、PAD、IS、cIMT多基因风险评分与颈动脉狭窄的关联与判别能力。 |
| **FinnGen** | 数据集 | #人群队列 | 176,899芬兰人，2,444表型 | [链接](https://www.finngen.fi/) | yes | 3 | 用于编码变异单等位与双等位效应对疾病表型的系统分析。 |
| **MATH** | 数据集 | #Agent | 1.25万题 | [链接](https://github.com/hendrycks/math) | yes | 3 | 评估数学推理性能，DeepSeekMath达51.7%。 |
| **BioBank Japan (BBJ)** | 数据集 | #心血管 #人群队列 | 9,826例AF/140,446对照 | [链接](https://biobankjp.org/) | restricted | 2 | 作为国家生物样本库WGS项目案例，用于比较设计、技术与发现经验。 |
| **GSM8K** | 数据集 | #Agent #世界模型 | 小学数学应用题基准 | [链接](https://github.com/openai/grade-school-math) | yes | 2 | 用于评估DLLM-JEPA在数学推理任务上的提升。 |
| **MIMIC-IV** | 数据集 | #心血管 #人群队列 | 单中心ICU EHR | [链接](https://physionet.org/content/mimiciv/) | restricted | 2 | 作为MiGHT-EHR多任务评测的EHR数据集之一。 |
| **Penn Medicine BioBank** | 数据集 | #心血管 #人群队列 | 57,170人，4,007例PET | [链接](https://www.pennmedicine.org/for-patients-and-visitors/penn-medicine-locations/penn-medicine-biobank) | restricted | 2 | 用于构建整合基因组和蛋白组的冠脉微血管疾病风险预测框架。 |
| **AMC23** | 数据集 | #Agent | 40题 | [链接](https://huggingface.co/datasets/AI-MO/aimo-validation-amc) | yes | 2 | 作为分布外基准评估TEMPO的数学推理泛化。 |
| **CHS** | 数据集 | #心血管 | 3,189人 |  | restricted | 2 | 用于心衰/衰弱蛋白组学外部复制及CARDIAC-FM外部验证。 |
| **COCO** | 数据集 | #世界模型 | 约33万图像，80类 | [链接](https://cocodataset.org/) | yes | 2 | 用于评估自监督表征在检测与分割任务上的迁移能力。 |
| **ELSA-Brasil** | 数据集 | #心血管 | 13,454人 | [链接](https://www.elsa.org.br/) | restricted | 2 | 用于外部验证AI-ECG预测新发心衰风险的多国队列之一。 |
| **ESTHER cohort** | 数据集 | #心血管 | 5,578-8,308人 |  | restricted | 2 | 代谢组CVD外部验证队列，受限，仅作迁移参照。 |
| **Genecorpus-30M** | 数据集 | #单细胞 | 约3000万细胞 |  | unknown | 2 | 作为单细胞基础模型预训练语料，用于污染审计与Geneformer预训练。 |
| **JetClass** | 数据集 | #世界模型 | 1亿个喷注 | 项目网站公开 | yes | 2 | 用于预训练HEP-JEPA高能物理基础模型并评估top tagging等下游任务。 |
| **ScanObjectNN** | 数据集 | #世界模型 | 15类真实扫描物体 | [链接](https://hkust-vgd.github.io/scanobjectnn/) | yes | 2 | 用于评估点云掩码自编码器在真实扫描物体分类上的下游性能。 |
| **FEVER** | 数据集 | #Agent | 约18万条声明 | [链接](https://fever.ai/) | yes | 1 | 用于评测ReAct在事实核查任务上的表现。 |
| **GSM-Plus** | 数据集 | #Agent | 约1万题 | [链接](https://huggingface.co/datasets/qintongli/GSM-Plus) | yes | 1 | 数学推理评测集，与生物应用弱相关。 |
| **GTEx** | 数据集 | #衰老 | 581全血样本 | [链接](https://gtexportal.org/) | yes | 1 | 提供全血RNA-seq数据，用于分析TFMethyl Clock靶基因表达。 |
| **HotpotQA** | 数据集 | #Agent | 约11万问答对 | [链接](https://hotpotqa.github.io/) | yes | 1 | 用于评测ReAct在知识密集型多跳问答上的推理与行动协同能力。 |
| **Libri-light** | 数据集 | #世界模型 | 60000小时 | [链接](https://github.com/facebookresearch/libri-light) | yes | 1 | 用于大规模无标注语音预训练及多规模微调评估HuBERT。 |
| **Librispeech** | 数据集 | #世界模型 | 960小时 | [链接](https://www.openslr.org/12) | yes | 1 | 用于微调和评估HuBERT语音表征在下游语音识别任务上的性能。 |
| **LVIS** | 数据集 | #世界模型 | 约12万图像，1200+类 | [链接](https://www.lvisdataset.org/) | yes | 1 | 用于评估SiameseIM在长尾实例分割上的迁移性能。 |
| **MATH500** | 数据集 | #Agent | 500题 | [链接](https://github.com/hendrycks/math) | yes | 1 | 用于评测BiPRM在解级数学推理上的表现。 |
| **PRM800K** | 数据集 | #Agent | 80万步级标签 | [链接](https://github.com/openai/prm800k) | yes | 1 | 用于训练过程奖励模型以支持PURE的最小形式信用分配。 |
| **Qwen3-4B** | 模型 | #Agent | 4B参数 | Hugging Face (Qwen/Qwen3-4B) | yes | 3 | 作为S-trace与GEAR方法的实验基座模型，评测数学推理与工具使用任务。 |
| **Qwen2.5-Math-7B** | 模型 | #Agent | 70亿参数 | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-7B) | yes | 2 | 作为PURE与ScalePRM的基座模型进行数学推理强化学习实验。 |
| **Qwen3-1.7B** | 模型 | #Agent | 1.7B参数 | Hugging Face (Qwen/Qwen3-1.7B) | yes | 2 | 作为S-trace选择性资格迹方法的实验基座模型之一，评测推理任务pass@16。 |
| **Qwen3-8B** | 模型 | #Agent | 8B参数 | Hugging Face (Qwen/Qwen3-8B) | yes | 2 | 作为S-trace与GEAR方法的实验基座模型，评测数学推理与工具使用任务。 |
| **DINO** | 模型 | #世界模型 | ViT-Base线性评估80.1% | [链接](https://github.com/facebookresearch/dino) | yes | 1 | 自蒸馏自监督ViT模型，展现语义分割涌现特性。 |
| **GenePT** | 模型 | #单细胞 | GPT-3.5嵌入，无需预训练 | [链接](https://doi.org/10.1101/2023.10.16.562533) | yes | 1 | 用GPT-3.5基于NCBI基因文本描述生成基因与单细胞嵌入的基础模型。 |
| **HuBERT** | 模型 | #世界模型 | 最大10亿参数 | [链接](https://github.com/facebookresearch/fairseq/tree/main/examples/hubert) | yes | 1 | 提出并发布的语音自监督预训练模型，通过掩码预测隐藏单元学习语音表征。 |
| **LaMamba-Diff** | 模型 | #世界模型 | 线性复杂度扩散模型 | [链接](https://github.com/) | yes | 1 | 基于局部注意力与Mamba的高效高保真扩散生成模型。 |
| **MAE** | 模型 | #世界模型 | ViT-Huge，ImageNet-1K 87.8% | [链接](https://github.com/facebookresearch/mae) | yes | 1 | 掩码自编码器预训练模型，用于可扩展视觉自监督学习。 |
| **MoCo** | 模型 | #世界模型 | ResNet-50骨干，ImageNet预训练 | [链接](https://github.com/facebookresearch/moco) | yes | 1 | 提出动量对比学习框架，提供可复用的无监督预训练模型。 |
| **Qwen2.5-7B** | 模型 | #Agent | 70亿参数 | [链接](https://huggingface.co/Qwen/Qwen2.5-7B) | yes | 1 | 通用LLM基座，科研智能体微调可选。 |
| **Qwen2.5-Math-1.5B** | 模型 | #Agent | 15亿参数 | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-1.5B) | yes | 1 | 小规模数学推理基座，仅作对比实验。 |
| **SAM (Segment Anything Model)** | 模型 | #类器官 | 十亿级掩码预训练 | [链接](https://github.com/facebookresearch/segment-anything) | yes | 1 | 用于PDO延时显微视频中类器官的分割。 |
| **SANA-WM** | 模型 | #世界模型 | 2.6B参数 | [链接](https://doi.org/10.48550/arXiv.2605.15178) | yes | 1 | 开源世界模型，支持一分钟720p视频生成与精确相机控制。 |
| **ALFWorld** | 基准 | #Agent | 6类任务、数千回合 | [链接](https://alfworld.github.io/) | yes | 4 | 作为SELAUR智能体强化学习框架的评测环境之一，衡量任务成功率。 |
| **MMLU** | 基准 | #Agent #世界模型 | 1.4万题、57学科 | [链接](https://github.com/hendrycks/test) | yes | 2 | 用于评估DLLM-JEPA在多学科知识任务上的表现。 |
| **ProcessBench** | 基准 | #Agent | 3400条推理路径 | [链接](https://huggingface.co/datasets/Qwen/ProcessBench) | yes | 2 | 用于评测BiPRM与ScalePRM的步级错误检测能力。 |
| **scIB** | 基准 | #单细胞 | 13任务，最多100万细胞 |  | unknown | 2 | 单细胞数据整合基准，用于评测整合工具及审计预训练污染。 |
| **WebShop** | 基准 | #Agent | 118万商品、1.2万指令 | [链接](https://webshop-pnlp.github.io/) | yes | 2 | 作为SELAUR智能体强化学习框架的评测环境之一，衡量任务成功率。 |
| **AI4AI-Bench** | 基准 | #Agent | 10仓库×29配置×6系统×10任务 | [链接](https://arxiv.org/abs/2608.20318) | yes | 1 | 评测LLM智能体在递归自我改进中算法设计能力的隔离基准，含公开任务套件与评估器。 |
| **LOGIQA** | 基准 | #Agent | 约1万题 | [链接](https://github.com/csitfun/LogiQA2.0) | yes | 1 | 逻辑推理基准，与科研智能体弱相关。 |
| **NKIBench** | 基准 | #Agent | 来自真实LLM工作负载的Trainium内核，复杂度不一 | [链接](https://github.com/zhang677/AccelOpt) | yes | 1 | 用于评测LLM智能体自主优化AWS Trainium AI加速器内核的性能。 |
| **PASCAL VOC** | 基准 | #世界模型 | 20类，约1.1万图像 | [链接](http://host.robots.ox.ac.uk/pascal/VOC/) | yes | 1 | 用于评估MoCo无监督预训练的迁移检测性能。 |
| **R-Judge** | 基准 | #Agent | 569条交互记录，27类风险场景 | [链接](https://github.com/Lordog/R-Judge) | yes | 1 | 用于评测LLM智能体在交互环境中的安全风险意识。 |
| **SKILLMISEVO-BENCH** | 基准 | #Agent | 未明确 | [链接](https://github.com/henrymao2004/misevolve) | yes | 1 | 冻结基准，用于评估自改进智能体的技能安全性。 |
| **SKILLMISEVO-GYM** | 基准 | #Agent | 25种配置，各525任务、25回合 | [链接](https://github.com/henrymao2004/misevolve) | yes | 1 | 生命周期感知测试台，用于检测技能误演化。 |
| **Socratic-PRMBench** | 基准 | #Agent | 2995条缺陷推理路径 | [链接](https://github.com/Xiang-Li-oss/Socratic-PRMBench) | yes | 1 | 用于系统评测PRM在六种推理模式下的过程错误检测能力。 |
| **Allen Brain Atlas** | 数据库 | #单细胞 | 全脑空间图谱 | [链接](https://portal.brain-map.org/) | yes | 1 | 提供脑空间转录组数据，用于参数化可解释细胞行为语法模型。 |
| **ENCODE** | 数据库 | #Agent | 132个转录因子 | [链接](https://www.encodeproject.org) | yes | 1 | 转录因子结合数据，仅用于基序发现评测。 |
| **GeneATLAS** | 数据库 | #人群队列 | 452,264人，778性状，9,113,133变异 | [链接](http://geneatlas.roslin.ed.ac.uk) | yes | 1 | 提供UK Biobank大规模遗传关联图谱的统一查询。 |
| **CellProfiler** | 工具 | #单细胞 | 开源图像分析管线 | [链接](https://cellprofiler.org/) | yes | 2 | 作为经典手工特征提取工具与深度学习特征比较。 |

## 单篇提及（370，未进主表）

- 数据集：23andMe BMI GWAS、AASK (African American Study of Kidney Disease and Hypertension)、ADE20K、ADVANCE trial、AIDA v2、AIDHS/SDS、ARIC Study、Arc Virtual Cell Dataset、Atherosclerosis Risk in Communities (ARIC) Study、AudioSet、AudioSet-20K、CHARGE-AF Consortium、CKMCC、COCO-Stuff、CODE (Brazilian ECG Dataset)、CODE15、CPRD、ChinaHEART cohort、Cityscapes、Copenhagen General Population Study、DFTJ cohort、Danish National Patient Registry、Droid、EPIC-Norfolk、ESC-50、EST-Health-30、Estonian Biobank、FSD50K、Fenland、Framingham Offspring Study、GDSC、GIANT Consortium BMI GWAS、GSE67752、Geisinger ECG Dataset、Generation Scotland、HM3D v0.2、INSPIRE-T、ImageNet ILSVRC-2012、Integrated Mega-scale Atlas、Israel 10K、JUMP-lite、Jiangsu Province Cohort (JBPCD)、Lorenz、Lothian Birth Cohort 1936、MERFISH whole mouse brain atlas、MGB Biobank、MIMIC、MIMIC-III、MNIST、MODIS、McFarland、Mexico City Prospective Study (MCPS)、NHANES、NLST、NPBBD-Korea、Norman K562 CRISPRa、Norman Perturb-seq、Norman19、Nurses' Health Study、Olink Proteomics Panel (UK Biobank)、PRECISE、Perturb-seq genome-scale screen、PerturbReason、Robomimic、SCIPRM70K、SHIP-START、SHIP-TREND、ST-bank、SaMi-Trop、SciPlex3、Sentinel-1、Sentinel-2、SpatialCorpus-110M、Taiwan Biobank (TWB)、Taiwan Precision Medicine Initiative (TPMI)、Tox21、UCLA Biobank、UHN-ECG、UK Biobank ECG Interval Reference Dataset、UK Biobank Exome Sequencing Consortium (UKB-ESC)
- 模型：AI-HF、AIRE、ALADYNOULLI、AROMA、ASCVD-IRT、ATM (Age-dependent Topic Model)、AdaptAge、AlphaEarth、AlphaFold3、Audio-MAE、BEHRT、BYOL、BitAge、Bootleg、BrainBeacon、CAME、CARDIAC-FM、CLM-X、CMAE、CODRP、CTBA、CTransPath、Cell-o1、CellFM、CellFlux、CellFluxRL、CellOT、CellWorld、China-AIHeart、CrossJEPA、D-SPIN、D2R2、DI-NOv2、DINO-WM、DINOv2、DNAm PhenoAge、DNAmEMRAge、DamAge、DeepQA、DeepSeek-R1、DeepSeekMath 7B、Delphi-2M、DiRL、ECG-AF、ECG-FM、ECG-LFM、ECG2CAD、EHR-MPC、EHRAgent、EMRAge、Echo2HF、EvoScientist、Foresight、Foresight-England、Framingham Risk Score、GLAM、GLAM NAV、GOLD BioAge、GPS Mult、GRASP、GeneCompass、Graph-JEPA、HEP-JEPA、HPS (Healthspan Proteomic Score)、Hannum DNAm Age Clock、Horvath clock、Intuitor、JCVI-syn3A、JEPA-Anything、JEPA-DNA、Kimi k1.5、LeJEPA、LeVJEPA、LinAge2、Longitudinal Proteomic Aging Index (LPAI)、LucaCell、MILTON、ML-CVD-C、MSGene、MSKAge
- 基准：ABC-Bench、AdaJEPA、BIRD、BLADE、Baba in Wonderland、BioDataLab、BioKGBench、BiomniBench-DA、CHARGE score、CellPuzzles、ComputAgeBench、D4RL、DiscoverPhysics、ESCALATE trial、GSM-HARD、Gaia2、HLE、HumanEval、LMR-BENCH、LiveCodeBench、MMLU-Medical、MedMCQA、MedPRMBench、MedQA、MemCalib、OfficeQA、PertEval-scFM、PerturBench、PushT、RSIBench-Data、RoboTwin、SEAGym、SWE Bench Verified、SciIntegrity-Bench、ScienceAgentBench、SealQA、SoundnessBench、StreamBench、Terminal-Bench 2.0、ToolMaker Benchmark、VTAB、Virtual Cell Challenge、Virtual Cell Challenge 2026、X-ARES、scEval
- 数据库：CPRD Aurum、Cell Landscape、ELAN、Immunosenescence Inventory、QResearch、STP、TCGA、TEAPEE
- 工具：AusCVDRisk、AutoPrognosis、BASIL、BOLT-LMM、BioLLM、Biolearn、CINEMA-OT、CROP-seq、CellML、CellOracle、CellPaint-POSH、CellScientist、ClockBase Agent、Co-Scientist、DeGAs、E-Cell、FaithRL、GATK、GEPA、Habitat、Hail、Harmony、ICD-8 to ICD-10 Mapping、K-Dense、LWD-Miniscope、LivAge、Loki、Longevity Claw、Mortara VERITAS algorithm、Mosaic、Nahual、OSCAR、Olink Explore 3072、PHESANT、PRS-CS、PheMIME、PheWeb、Phecodes、REGENIE、SAFEEVOLVE、SAIGE-GENE、SCOPE (Systematic Classification of Organoids for Phenotypic Evaluation)、SCanSNP、SPAC-seq、SPA_GRM、STREME、SenePy、SomaLogic、SpatialQM、TARDIS、TFActProfiler、The AI Scientist、TotalSegmentator、TranslAGE、VCell、associationSubgraphs、copairs、iGOF-Perturb-seq、leakcheck、moscot、ukbnmr
