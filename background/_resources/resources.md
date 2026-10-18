# 资源登记（数据集 / 模型 / 基准）

从 798 处证据引用中挖出资源，并入人工种子与日报新发现，共 555 项；主表 155 项（种子/置顶，或被 ≥2 篇工作使用、或跨方向、或开放且链接核验通过且规模明确），日报新发现 16 项（未核验），其余 384 项单篇提及的列在末尾。开放：yes 公开 / partial 部分 / registration 注册 / controlled 受控 / commercial 商业 / unknown 未确认。核验：ok 内容匹配 / mismatch 页面不是该资源 / blocked 站点拒绝探测 / dead 失效 / n/a 非链接。规模带 * 的取自单篇引用文献。更新 2026-10-18


## P0 优先上手（25）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **UK Biobank** | 数据集 | #衰老 #心血管 #人群队列 | 约 50 万人（40–69 岁入组，2006–10） | [链接](https://www.ukbiobank.ac.uk/) | controlled | 121 | 多组学衰老与CVD方法迁移主数据源，ChinaHEART参照基准 |
| **UK Biobank Pharma Proteomics Project** | 数据集 | #心血管 #人群队列 #衰老 | 约 5.4 万人 · 约 2,900 蛋白 | [链接](https://www.ukbiobank.ac.uk/) | controlled | 11 | UKB蛋白组，ChinaHEART蛋白组CVD风险迁移参照 |
| **China Kadoorie Biobank** | 数据集 | #衰老 #心血管 #人群队列 | 约 51 万成人（10 个地区，2004–08 入组） | [链接](https://www.ckbiobank.org/) | controlled | 9 | 中国人群参照队列，ChinaHEART 迁移时的对照 |
| **Tahoe-100M** | 数据集 | #单细胞 #虚拟细胞 | 1亿+细胞/50细胞系/379化合物* | [链接](https://huggingface.co/datasets/tahoebio/Tahoe-100M) | yes | 5 | 亿级药物扰动图谱，虚拟扰动预训练与类器官demo核心数据 |
| **Norman 2019 Perturb-seq** | 数据集 | #单细胞 #虚拟细胞 | Perturb-seq扰动数据集* |  | unknown | 3 | 组合扰动基准数据，虚拟扰动响应建模必用基线 |
| **UK Biobank Olink Plasma Proteomics (Pharma Proteomics Project)** | 数据集 | #人群队列 | 约5.4万人/2923蛋白* | UK Biobank Showcase | unknown | 3 | pQTL与蛋白关联参照，ChinaHEART蛋白组迁移必对标 |
| **KORA cohort** | 数据集 | #衰老 #心血管 | 9105样本/4100人* | [链接](https://www.helmholtz-munich.de/en/kora) | unknown | 2 | 纵向蛋白组衰老时钟参照，直接对标ChinaHEART蛋白组迁移 |
| **Replogle 2022 Perturb-seq** | 数据集 | #虚拟细胞 | >250万人类细胞* | [链接](https://doi.org/10.1016/j.cell.2022.05.013) | unknown | 2 | 基因组规模Perturb-seq，扰动预测建模与基准评估核心数据 |
| **Adamson Perturb-seq** | 数据集 | #单细胞 #虚拟细胞 | 68,603单细胞* |  | unknown | 1 | 扰动scRNA基准数据，虚拟扰动建模与类器官demo直接可用 |
| **Replogle Perturb-seq** | 数据集 | #单细胞 #虚拟细胞 | K562 162,751/RPE1 162,733细胞* |  | unknown | 1 | 虚拟扰动建模标准基准，类器官扰动响应直接对标 |
| **ChinaHEART** | 数据集 | #心血管 #人群队列 | 中国大规模心血管病筛查/早筛队列 |  | controlled | 1 | 目标队列：UKB 等公共队列方法迁移的落点 |
| **scGPT** | 模型 | #类器官 #单细胞 #虚拟细胞 | 基础模型（参数量未明确）* | [链接](https://github.com/bowang-lab/scGPT) | yes | 18 | 单细胞基础模型基线，类器官衰老demo与虚拟扰动对标 |
| **Geneformer** | 模型 | #衰老 #单细胞 #虚拟细胞 | 基础模型（参数量未明确）* | [链接](https://huggingface.co/ctheodoris/Geneformer) | yes | 13 | 单细胞基础模型基线，类器官衰老demo与虚拟扰动建模直接对标 |
| **scFoundation** | 模型 | #单细胞 #虚拟细胞 | 基础模型（参数量未明确）* | [链接](https://github.com/biomap-research/scFoundation) | yes | 7 | 扰动预测基准模型，类器官扰动demo可直接部署对比 |
| **China-PAR** | 模型 | #心血管 | 推导21320人/验证8.5万人* | [链接](https://doi.org/10.1161/CIRCULATIONAHA.116.022367) | yes | 4 | 中国人群传统评分基线，ChinaHEART 模型必须对标 |
| **Tahoe-X1** | 模型 | #单细胞 #虚拟细胞 | 最高30亿参数* | 预训练检查点/训练代码/评估流程 | unknown | 3 | 扰动训练单细胞基础模型，虚拟扰动响应建模首选基线 |
| **Chreode** | 模型 | #单细胞 #虚拟细胞 | 240万细胞小鼠胚胎图谱预训练* |  | unknown | 2 | 细胞世界模型，虚拟扰动响应与类器官时序建模直接参照 |
| **SCALE** | 模型 | #单细胞 #虚拟细胞 | PBMC三供体等* | [链接](https://arxiv.org/abs/2603.17380v3) | unknown | 1 | 条件传输虚拟扰动模型，类器官扰动响应建模直接可用 |
| **ALADYNOULLI** | 模型 | #人群队列 #心血管 | 68.3万人，348种疾病* |  | unknown | 1 | 生成式疾病轨迹的对标基线（可解释） |
| **Delphi-2M** | 模型 | #人群队列 #心血管 | UKB 约 40 万人训练 + 丹麦 190 万人验证 · 1000+ 病种 |  | unknown | 1 | 生成式疾病轨迹的对标基线 |
| **Pooled Cohort Equations** | 模型 | #心血管 |  |  | yes | 0 | 心血管风险预测的传统评分基线 |
| **Virtual Cell Challenge** | 基准 | #单细胞 #虚拟细胞 | 专用扰动数据集* | [链接](https://doi.org/10.1016/j.cell.2025.06.008) | unknown | 1 | 虚拟扰动响应基准，类器官/细胞虚拟扰动建模直接对标 |
| **LongevityBench** | 基准 | #衰老 | 17项任务/5个数据域* | [链接](https://doi.org/10.1016/j.cell.2026.08.026) | unknown | 1 | 衰老 AI 基准（Cell 2026），模型评测对标 |
| **CELLxGENE** | 数据库 | #衰老 #单细胞 | 公共单细胞数据集合* | [链接](https://cellxgene.cziscience.com/) | yes | 2 | 单细胞图谱，训练类器官/单细胞衰老时钟的公开数据 |
| **Cell Painting** | 工具 | #衰老 #单细胞 | 多批次图像profiling数据* |  | unknown | 2 | 细胞形态扰动响应，类器官+cell painting扰动建模核心 |

## P1 值得登记（68）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **All of Us Research Program** | 数据集 | #心血管 #人群队列 | 目标 100 万人（美国，多族裔） | [链接](https://www.researchallofus.org/) | controlled | 13 | 多血统EHR+基因组，PRS与EHR关联复制方法参照 |
| **ARIC** | 数据集 | #心血管 #人群队列 | 约 1.6 万人（1987–89 入组） | [链接](https://aric.cscc.unc.edu/) | controlled | 5 | 蛋白组心衰/衰弱队列，ChinaHEART蛋白组参照 |
| **Framingham Heart Study** | 数据集 | #衰老 #心血管 | 10,097人/28,151份ECG* | [链接](https://www.framinghamheartstudy.org/) | controlled | 3 | ECG-AF深度学习经典队列，心血管AI模型对标 |
| **MESA** | 数据集 | #心血管 #人群队列 | 6,814 人（45–84 岁，四个族裔） | [链接](https://www.mesa-nhlbi.org/) | controlled | 3 | 多模态CVD队列，心血管基础模型外部验证 |
| **UK Biobank Exome Sequencing Dataset** | 数据集 | #人群队列 | 约45.5万人/1230万变异* | UK Biobank Showcase | unknown | 3 | 罕见变异负荷分析参照，人群多组学遗传整合 |
| **CHARLS** | 数据集 | #心血管 #人群队列 #衰老 | 8,080名≥45岁参与者* | [链接](https://charls.pku.edu.cn/) | registration | 2 | 中国队列，ChinaHEART迁移与AI-ECG外部验证 |
| **Global Biobank Meta-analysis Initiative (GBMI)** | 数据集 | #人群队列 | 23库，220万人，14终点* | [链接](https://www.globalbiobankmeta.org/) | unknown | 2 | 跨库荟萃资源，跨祖源PRS评估方法参照 |
| **Pan-UK Biobank** | 数据集 | #人群队列 | 7,266性状，多祖源* | [链接](https://pan.ukbb.broadinstitute.org/) | yes | 2 | 多祖源GWAS汇总，ChinaHEART遗传整合与跨队列校正参照 |
| **SpeciesCorpus** | 数据集 | #类器官 #单细胞 #虚拟细胞 | 1.31亿细胞* |  | unknown | 1 | 跨物种单细胞语料，可预训练虚拟细胞模型支撑类器官与扰动。 |
| **BBBC021** | 数据集 | #单细胞 #虚拟细胞 | 63,781训练/5,120测试图像* | BBBC | unknown | 1 | 扰动图像基准，虚拟扰动建模评测参照 |
| **JUMP** | 数据集 | #单细胞 #虚拟细胞 | 多通道细胞图像* | JUMP Consortium | unknown | 1 | 细胞形态扰动基准，类器官成像扰动评测 |
| **CODE-15%** | 数据集 | #心血管 | 约 34.6 万份心电 / 23.4 万患者 | [链接](https://zenodo.org/records/4916206) | yes | 1 | 大规模ECG公开数据，ECG基础模型预训练验证 |
| **NHANES** | 数据集 | #衰老 #人群队列 | 每两年约 1 万人（美国代表性样本） | [链接](https://www.cdc.gov/nchs/nhanes/) | yes | 1 | 外部验证衰老时钟对死亡风险捕捉，可作ChinaHEART迁移参照 |
| **Tabula Sapiens** | 数据集 | #单细胞 | 564,253细胞* |  | unknown | 1 | 多供体单细胞图谱，可作类器官与虚拟细胞表征基准。 |
| **Cell Painting Gallery** | 数据集 | #类器官 |  | [链接](https://github.com/broadinstitute/cellpainting-gallery) | yes | 0 | 细胞形态成像，类器官cell painting扰动建模 |
| **GTEx** | 数据集 | #衰老 | 约 950 名供体 · 54 个组织（v8） | [链接](https://gtexportal.org/) | partial | 0 | 多组织eQTL参照，人群多组学遗传整合 |
| **LINCS L1000** | 数据集 | #虚拟细胞 |  | [链接](https://clue.io/) | registration | 0 | 扰动转录组，虚拟扰动响应建模训练数据 |
| **PTB-XL** | 数据集 | #心血管 | 21,799 份心电 / 18,869 人 | [链接](https://physionet.org/content/ptb-xl/) | yes | 0 | 公开心电数据，ChinaHEART AI-ECG风险模型预训练 |
| **SCORE2** | 模型 | #心血管 | 45队列67.8万人建模；外部113万人* | [链接](https://www.escardio.org/Education/Practice-Tools/CVD-prevention-toolbox/SCORE-Risk-Charts) | unknown | 5 | 欧洲CVD风险基线，ChinaHEART模型对标 |
| **TranscriptFormer** | 模型 | #类器官 #单细胞 #虚拟细胞 | 单细胞基础模型（参数量未明）* |  | unknown | 3 | 跨物种虚拟细胞图谱，虚拟扰动与跨物种迁移参照 |
| **DINOv2** | 模型 | #类器官 #世界模型 | ViT-S/B，ImageNet线性80.1%* | [链接](https://github.com/facebookresearch/dinov2) | yes | 3 | 类器官视频自监督特征+药效预测，可直接用于类器官demo |
| **GEARS** | 模型 | #单细胞 #虚拟细胞 | 图神经网络扰动模型* |  | unknown | 3 | 扰动预测可迁移基线，虚拟扰动建模对比方法 |
| **QRISK3** | 模型 | #心血管 | QResearch 1998-2015开放队列* | [链接](https://qrisk.org) | unknown | 3 | 英国CVD风险模型，蛋白组增量比较基线 |
| **SCimilarity** | 模型 | #单细胞 | 2340万细胞/412研究* | [链接](https://doi.org/10.1038/s41586-024-08411-y) | unknown | 3 | 细胞表示基础模型，跨队列细胞注释与状态查询可用 |
| **LucaCell** | 模型 | #类器官 #单细胞 | 8500万人/鼠细胞预训练* |  | unknown | 2 | 跨物种单细胞基础模型，类器官注释与虚拟扰动可用 |
| **UCE** | 模型 | #类器官 #单细胞 | 3600万细胞，8物种* | [链接](https://github.com/snap-stanford/UCE) | yes | 2 | 免微调细胞嵌入，类器官衰老demo可作基线表征 |
| **Biomni** | 模型 | #Agent | 25领域工具库* |  | unknown | 2 | 通用生物医学智能体，科研工作流与基因优先排序可试 |
| **CellPLM** | 模型 | #单细胞 | 单细胞基础模型* |  | unknown | 2 | scEval最佳基础模型之一，类器官单细胞建模候选 |
| **CHARGE-AF** | 模型 | #心血管 | 房颤10年风险简易评分* | [链接](https://www.chargeaf.org) | unknown | 2 | 房颤风险模型，AI-ECG与蛋白组评分比较基线 |
| **CHARGE-AF Risk Score** | 模型 | #心血管 | 多变量预测方程* | [链接](https://www.chargeconsortium.com/) | unknown | 2 | 房颤风险基线，ChinaHEART心血管预测对照 |
| **Horvath epigenetic clock (353 CpG)** | 模型 | #衰老 | 353个CpG* |  | unknown | 2 | 表观年龄基线，类器官衰老demo与队列甲基化对照 |
| **Longevity-LLM** | 模型 | #衰老 | 0.6B–9B参数，5个模型* | 论文公开模型（doi:10.1016/j.cell.2026.08.026） | unknown | 2 | 衰老组学基础模型，可微调做表观年龄与多模态衰老表征 |
| **PREVENT** | 模型 | #心血管 | AHA多队列推导方程* | [链接](https://www.ahajournals.org/doi/10.1161/CIRCULATIONAHA.123.067626) | unknown | 2 | AHA风险方程，蛋白组评分增量比较基线 |
| **Reti-CVD** | 模型 | #心血管 | 深度学习CVD风险评分模型* |  | unknown | 2 | 视网膜图像CVD评分，多模态风险分层可迁移 |
| **SCORE2-Diabetes** | 模型 | #心血管 | 2型糖尿病10年MACE风险模型* | [链接](https://www.escardio.org/Education/Practice-Tools/CVD-prevention-toolbox/SCORE-Risk-Charts) | unknown | 2 | T2D专用CVD模型，代谢组增量改进对照 |
| **Speciesformer** | 模型 | #类器官 #单细胞 #虚拟细胞 | 1.31亿细胞预训练* |  | unknown | 1 | 跨物种虚拟细胞基础模型，直接对标虚拟扰动响应建模基线。 |
| **PerturbBridge** | 模型 | #单细胞 #虚拟细胞 | BBBC021约6.9万图像* |  | unknown | 1 | 扰动图像生成思路，可迁移到类器官扰动响应建模 |
| **RegFormer** | 模型 | #单细胞 #世界模型 | 2500万人类细胞预训练* |  | unknown | 1 | 融合GRN先验的扰动预测模型，虚拟扰动建模可迁移 |
| **DNAm PhenoAge** | 模型 | #衰老 | CpG表观遗传时钟* |  | yes | 1 | 甲基化时钟基线 |
| **Horvath clock** | 模型 | #衰老 | 353 CpG |  | yes | 1 | DNAm年龄基线时钟，类器官衰老demo必比基线 |
| **I-JEPA** | 模型 | #世界模型 | ViT-Huge/14，16×A100<72h* | [链接](https://github.com/facebookresearch/ijepa) | yes | 1 | I-JEPA 是自监督表征范式基线，可迁移到类器官图像与组学 |
| **scGen** | 模型 | #虚拟细胞 | 未明确（VAE模型）* | [链接](https://github.com/theislab/scgen) | yes | 1 | 潜空间扰动向量预测，虚拟扰动建模经典基线 |
| **DunedinPACE** | 模型 | #衰老 |  | [链接](https://github.com/danbelsky/DunedinPACE) | yes | 0 | 衰老速度时钟，类器官与队列衰老速率评估 |
| **GrimAge** | 模型 | #衰老 |  |  | unknown | 0 | 死亡率导向的甲基化时钟基线 |
| **PhenoAge** | 模型 | #衰老 |  |  | yes | 0 | 血检生物年龄基线，NHANES 可复现 |
| **VCBench** | 基准 | #类器官 #单细胞 #虚拟细胞 | 5个基础模型×7能力维度×4框架* | 污染报告模式与共同标签集协议 | unknown | 1 | 单细胞基础模型评测基准，选型与对标时参照 |
| **scArchon** | 基准 | #单细胞 #虚拟细胞 | 9种工具、多样本扰动数据* | 容器化流程（GitHub） | unknown | 1 | 扰动预测标准化基准，虚拟扰动建模评测直接可用 |
| **AssayBench** | 基准 | #虚拟细胞 | 1920个筛选/约13826基因* | [链接](https://github.com/Genentech/AssayBench) | yes | 1 | CRISPR表型预测基准，评估智能体虚拟细胞能力 |
| **GenoTEX** | 基准 | #Agent | 含专家标注代码与结果的分析基准* | [链接](https://github.com/Liu-Hy/GenoTEX) | yes | 1 | 基因表达分析智能体基准，LLM科研工作流直接对标 |
| **TruthInsightBench** | 基准 | #Agent | 40个盲任务/10领域* | [链接](https://github.com/TruthInsight-stack/TruthInsightBench) | yes | 1 | 科学发现智能体评测，科研智能体工作流可参照 |
| **ARCHS4** | 数据库 | #衰老 | 约5.7万样本，28组织，1,039队列* | [链接](https://maayanlab.cloud/archs4/) | yes | 2 | 跨年龄RNA-seq，转录组衰老时钟训练验证数据 |
| **Human Cell Atlas** | 数据库 | #单细胞 | 多组织细胞图谱* | [链接](https://data.humancellatlas.org/) | yes | 2 | 细胞图谱资源，类器官衰老demo参照与跨组织整合 |
| **CollecTRI** | 数据库 | #虚拟细胞 | 文献整合调控网络* | [链接](https://github.com/saezlab/CollecTRI) | yes | 1 | TF调控网络先验，扰动预测带符号系数学习 |
| **Gene Expression Omnibus** | 数据库 | #衰老 | 51项人类干预研究* | [链接](https://www.ncbi.nlm.nih.gov/geo/) | yes | 1 | 取公开DNAm数据评估表观遗传时钟对干预响应 |
| **NHGRI-EBI GWAS Catalog** | 数据库 | #人群队列 | 625,113关联，>85K数据集* | [链接](https://www.ebi.ac.uk/gwas/) | yes | 1 | GWAS汇总统计标准库，ChinaHEART遗传关联查询 |
| **CELLxGENE Census** | 数据库 | #单细胞 |  | [链接](https://chanzuckerberg.github.io/cellxgene-census/) | yes | 0 | 单细胞ML切片，类器官与虚拟扰动表征训练 |
| **ClockBase** | 数据库 | #衰老 |  |  | unknown | 0 | 甲基化时钟基准平台，选型与评测参照 |
| **DepMap** | 数据库 | #虚拟细胞 |  | [链接](https://depmap.org/portal/) | yes | 0 | 细胞系依赖与药敏，虚拟细胞扰动基线 |
| **HuBMAP** | 数据库 | #单细胞 |  | [链接](https://portal.hubmapconsortium.org/) | yes | 0 | 人体单细胞空转图谱，类器官衰老demo参照 |
| **scPerturb** | 数据库 | #虚拟细胞 |  |  | yes | 0 | 单细胞扰动聚合，虚拟扰动建模核心数据 |
| **Olink** | 工具 | #心血管 #人群队列 | 2920蛋白/44779人* | [链接](https://www.ukbiobank.ac.uk) | commercial | 6 | 蛋白组检测平台，ChinaHEART蛋白组方案参照 |
| **Olink Proteomics panels** | 工具 | #衰老 | 2,448-2,923蛋白* | [链接](https://olink.com) | unknown | 3 | 血浆蛋白组时钟建模，可迁移到ChinaHEART蛋白组衰老指标 |
| **MEDICINE portal** | 工具 | #衰老 #人群队列 | 5个器官特异性MetBAG模型* | MEDICINE门户 | unknown | 2 | 多器官代谢组衰老时钟可迁移到类器官衰老demo与ChinaHEART衰老建模。 |
| **Perturb-seq** | 工具 | #单细胞 #虚拟细胞 | 约20万细胞* |  | unknown | 2 | CRISPR扰动数据，虚拟扰动建模训练与基准 |
| **scvi-tools** | 工具 | #单细胞 | 多模态深度生成模型* | [链接](https://github.com/scverse/scvi-tools) | yes | 2 | 单细胞嵌入经典基线，类器官与虚拟细胞建模对照。 |
| **SomaScan** | 工具 | #心血管 #人群队列 | 4,877个aptamer/蛋白* | [链接](https://somalogic.com/) | commercial | 2 | 血浆蛋白组平台，ChinaHEART蛋白组衰老建模参照 |
| **Trellis** | 工具 | #类器官 | >2500个CRC PDO与CAF* |  | unknown | 2 | 类器官药物响应分析方法，可直接用于类器官扰动响应建模。 |
| **Perturb-FISH** | 工具 | #类器官 #单细胞 | MERFISH+gRNA原位* | [链接](https://doi.org/10.1016/j.cell.2025.02.012) | unknown | 1 | 空间扰动读取思路，可用于类器官虚拟扰动建模设计 |

## P2 了解即可（62）

| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |
|---|---|---|---|---|---|---|---|
| **ImageNet-1K** | 数据集 | #世界模型 | 约128万训练图像/1000类* | [链接](https://www.image-net.org/) | unknown | 10 | 用于线性/冻结探针评估自监督表征质量及预训练。 |
| **ModelNet40** | 数据集 | #世界模型 | 40类3D CAD模型* | [链接](https://modelnet.cs.princeton.edu/) | unknown | 4 | 用于CrossJEPA的3D表征线性探测评估。 |
| **Cardiovascular Health Study** | 数据集 | #心血管 #衰老 | 5,888 人（65 岁以上） | [链接](https://chs-nhlbi.org/) | controlled | 3 | 作为外部验证队列用于心衰/衰弱蛋白组复制及CARDIAC-FM验证。 |
| **BioBank Japan** | 数据集 | #心血管 #人群队列 | 第一期约 20 万患者（47 种疾病） | [链接](https://biobankjp.org/) | controlled | 2 | 作为国家生物样本库WGS项目案例，用于比较设计与转化经验。 |
| **Mass General Brigham Biobank** | 数据集 | #心血管 #人群队列 | 约5.3万人（670例狭窄）* | [链接](https://www.massgeneralbrigham.org/) | unknown | 2 | 作为三个生物库之一用于ALADYNOULLI纵向EHR与遗传发现框架。 |
| **MIMIC-IV** | 数据集 | #心血管 #人群队列 | 大型ICU患者数据库* | [链接](https://physionet.org/content/mimiciv/) | controlled | 2 | 用于MiGHT-EHR四任务评测并与MIMIC-III联合验证。 |
| **ELSA-Brasil** | 数据集 | #心血管 | 13,454人* | [链接](https://www.elsa-brasil.org.br) | unknown | 2 | 作为前瞻队列用于验证单导联AI-ECG模型对新发心衰风险的关联。 |
| **ESTHER cohort** | 数据集 | #心血管 | 5578人（T2D亚组1039人）；249代谢物* |  | unknown | 2 | 代谢组CVD外部验证队列，受限，仅作迁移参照。 |
| **JetClass** | 数据集 | #世界模型 | 1亿个喷注* | 项目网站公开 | unknown | 2 | 用于预训练HEP-JEPA高能物理基础模型并评估top tagging等下游任务。 |
| **ScanObjectNN** | 数据集 | #世界模型 | 约1.5万点云/15类* | [链接](https://hkust-vgd.github.io/scanobjectnn/) | unknown | 2 | 用于CrossJEPA的3D点云分类线性探测评估。 |
| **AllenCell** | 数据集 | #单细胞 #虚拟细胞 | 公开细胞图像库* | Allen Institute | unknown | 1 | 评测PerturbBridge扰动图像生成与检索。 |
| **ADVANCE** | 数据集 | #心血管 | 全球T2D试验人群（万级）* |  | unknown | 1 | 用于验证跨祖源PRS心肾并发症预测的MCCP方法。 |
| **GSM-Plus** | 数据集 | #Agent | 约1万题* | [链接](https://huggingface.co/datasets/qintongli/GSM-Plus) | yes | 1 | 数学推理评测集，与生物应用弱相关。 |
| **Libri-light** | 数据集 | #世界模型 | 60000小时* | [链接](https://github.com/facebookresearch/libri-light) | yes | 1 | 用于HuBERT多规模自监督预训练与微调评测。 |
| **PRM800K** | 数据集 | #Agent | 80万步级标签* | [链接](https://github.com/openai/prm800k) | yes | 1 | 用于训练过程奖励模型（PRM），为PURE提供过程监督数据。 |
| **TCGA** | 数据集 |  |  | [链接](https://portal.gdc.cancer.gov/) | partial | 0 |  |
| **Qwen2.5-Math-7B** | 模型 | #Agent | 7B参数* | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-7B) | yes | 2 | 作为PURE与ScalePRM的基座模型，验证最小形式信用分配与合成过程监督的RL效果。 |
| **Qwen3** | 模型 | #Agent | 1.7B/4B/8B参数* |  | unknown | 2 | 作为基座模型用于验证信用分配与优势重加权方法的推理性能。 |
| **AlphaFold** | 模型 | #心血管 | 蛋白复合物结构* | [链接](https://github.com/google-deepmind/alphafold) | yes | 1 | 预测关键蛋白变异的结构以解释功能机制。 |
| **ESM-2** | 模型 | #Agent | 未明确* | [链接](https://github.com/facebookresearch/esm) | yes | 1 | Virtual Lab纳米抗体设计流程中的蛋白质序列建模组件。 |
| **Graph-JEPA** | 模型 | #世界模型 | 图级JEPA编码器* | [链接](https://github.com/geriskenderi/graph-jepa) | yes | 1 | 图级联合嵌入预测架构自监督表征模型。 |
| **HuBERT** | 模型 | #世界模型 | 最大10亿参数* | [链接](https://github.com/facebookresearch/fairseq/tree/main/examples/hubert) | yes | 1 | 掩码隐藏单元预测的语音自监督预训练模型。 |
| **MAE** | 模型 | #世界模型 | ViT-Huge，ImageNet-1K 87.8%* | [链接](https://github.com/facebookresearch/mae) | yes | 1 | 掩码自编码器预训练模型，用于可扩展视觉自监督学习。 |
| **MoCo** | 模型 | #世界模型 | ResNet-50骨干，ImageNet预训练* | [链接](https://github.com/facebookresearch/moco) | yes | 1 | 动量对比学习框架，提供可复用预训练视觉编码器。 |
| **Point-JEPA** | 模型 | #世界模型 | 点云ViT编码器* | [链接](https://github.com/Ayumu-J-S/Point-JEPA) | yes | 1 | 点云联合嵌入预测架构自监督预训练模型。 |
| **Qwen2.5-Math-1.5B** | 模型 | #Agent | 1.5B参数* | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-1.5B) | yes | 1 | 小规模数学推理基座，仅作对比实验。 |
| **SAM (Segment Anything Model)** | 模型 | #类器官 | 十亿级掩码预训练基础模型* | [链接](https://github.com/facebookresearch/segment-anything) | yes | 1 | 用于类器官延时显微视频中类器官的自动分割。 |
| **DNABERT-2** | 模型 |  |  | [链接](https://github.com/MAGICS-LAB/DNABERT_2) | yes | 0 |  |
| **Enformer** | 模型 |  |  |  | yes | 0 |  |
| **Nucleotide Transformer** | 模型 |  |  | [链接](https://github.com/instadeepai/nucleotide-transformer) | yes | 0 |  |
| **ALFWorld** | 基准 | #Agent | 文本家务任务交互基准* | [链接](https://alfworld.github.io/) | unknown | 4 | 作为ReAct与AgentPRM的交互决策/智能体任务环境，评测多步动作决策。 |
| **COCO** | 基准 | #世界模型 | 约33万图像/80类* | [链接](https://cocodataset.org/) | unknown | 2 | 作为下游检测与分割迁移评测基准。 |
| **MATH** | 基准 | #Agent | 数学推理基准* |  | unknown | 2 | 分布内数学推理评测基准，用于比较TEMPO与PPO/GRPO及DeepSeekMath性能。 |
| **ProcessBench** | 基准 | #Agent | 3400余条推理路径* | [链接](https://huggingface.co/datasets/Qwen/ProcessBench) | yes | 2 | 用于评测PRM的步级错误检测能力，BiPRM与ScalePRM均在此报告F1。 |
| **PushT** | 基准 | #世界模型 | 推T形块操作任务（规模未列）* | [链接](https://github.com/huggingface/gym-pusht) | yes | 2 | 用于评估D-JEPA在机器人操作动作选择上的成功率（达87.89%）。 |
| **WebShop** | 基准 | #Agent | 118万商品、1.2万指令* | [链接](https://webshop-pnlp.github.io/) | unknown | 2 | 作为ReAct的交互式网购决策任务，评测多步导航与选择。 |
| **HumanEval** | 基准 | #Agent | 164道编程题* | [链接](https://github.com/openai/human-eval) | yes | 1 | Reflexion在编码任务上评估pass@1的基准。 |
| **MemCalib** | 基准 | #Agent | 15000例（13500训练+1500测试）* | [链接](https://github.com/Quark-Medical/memcalib) | yes | 1 | 智能体记忆评测，方法储备了解即可 |
| **NKIBench** | 基准 | #Agent | 真实LLM工作负载内核，复杂度不一* | [链接](https://github.com/zhang677/AccelOpt) | yes | 1 | 用于评测LLM智能体自主优化AWS Trainium内核的性能。 |
| **OGBench** | 基准 | #世界模型 | 多任务离线目标基准* | [链接](https://github.com/seohongpark/ogbench) | yes | 1 | 提供Cube等目标条件机器人规划评测任务。 |
| **PaperBench** | 基准 | #Agent | 20篇论文/8,316个可评分任务* | [链接](https://github.com/openai/preparedness) | yes | 1 | 评测AI智能体从零复现前沿AI研究的能力。 |
| **R-Judge** | 基准 | #Agent | 569条交互记录/27类风险场景* | [链接](https://github.com/Lordog/R-Judge) | yes | 1 | 用于评测LLM智能体在交互环境中的安全风险识别能力。 |
| **SKILLMISEVO-BENCH** | 基准 | #Agent | 冻结基准，含三类任务* | [链接](https://github.com/henrymao2004/misevolve) | yes | 1 | 冻结基准，用于衡量技能误演化导致的不安全检索与新会话危害。 |
| **SKILLMISEVO-GYM** | 基准 | #Agent | 25种配置×525任务×25回合* | [链接](https://github.com/henrymao2004/misevolve) | yes | 1 | 生命周期感知测试台，用于研究自改进智能体的技能误演化。 |
| **Socratic-PRMBench** | 基准 | #Agent | 2995条路径、平均8.7步* | [链接](https://github.com/Xiang-Li-oss/Socratic-PRMBench) | yes | 1 | 系统评测PRM在六种推理模式下的过程错误检测能力。 |
| **FinnGen** | 数据库 | #衰老 #人群队列 | R5约22.5万人/1932终点* | [链接](https://www.finngen.fi/) | unknown | 6 | 用于慢性疼痛GWAS荟萃分析及EHR预测模型跨队列验证。 |
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

## 日报新发现（16，未核验）

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

## 单篇提及（384，未进主表）

- 数据集：AASK (African American Study of Kidney Disease and Hypertension)、ADE20K、AGES-Reykjavik Study、AIDA v2、AIDHS/SDS (Asian Indian Diabetes Heart Study / Sikh Diabetes Study)、ARIC cohort、AudioSet、AudioSet-20K、C3PO、CHARGE-AF Consortium、COCO-Stuff、CTRP、CeNGEN、Cityscapes、Code15 / 2.3M ECG Brazilian dataset、Copenhagen General Population Study、DFTJ、DROID、EPIC-Norfolk、ESC-50、EST-Health-30、EWOC、Estonian Biobank、FEVER、FSD50K、Fenland、Finnish THL Biobank、GEO GSE67752、GSM8K、Geisinger ECG dataset、Genecorpus-30M、Generation Scotland、HEEDB、HM3D v0.2、HotpotQA、HumanST-46M、INSPIRE-T cohort、Integrated Mega-scale Atlas、JBPCD (Jiangsu Behavioral Risk Factor and Non-communicable Chronic Disease Cohort)、JUMP-MOA、JUMP-lite、Kailuan Cohort、LibriSpeech、Lothian Birth Cohort 1936、MATH500、MIMIC、MIMIC-III、MIMIC-IV-ECG、MODIS、McFarland、Mexico City Prospective Study (MCPS)、Mount Sinai、NLST (National Lung Screening Trial)、NPBBD-Korea、Norman K562 CRISPRa dataset、Nurses' Health Study (NHS)、PRECISE、Perturb-seq genome-scale screen、PerturbReason、Rotterdam Study、SCIPRM70K、SHIP-START、SHIP-TREND、ST-bank、SaMi-Trop、SciPlex3、SenSkin、Sentinel-1、Sentinel-2、SpatialCorpus-110M、THL Biobank、Taiwan Biobank (TWB)、Taiwan Precision Medicine Initiative (TPMI)、UHN-ECG、UK Biobank ECG interval reference dataset、UK Biobank Exome Sequencing Consortium (UKB-ESC) data、UK Biobank NMR Metabolomics Dataset、UK Biobank Polygenic Risk Score Release、UK Biobank Whole-Genome Sequencing、US Veterans Affairs EHR
- 模型：AB-PRS、AI-HF、AIDE、AIRE (AI-ECG Risk Estimation)、AROMA、ASCVD-IRT、ATM (Age-dependent Topic Model)、AURORA、AdaptAge、AlphaEarth、AlphaFold-Multimer、Audio-MAE、BEHRT、BYOL、BiPRM、BrainBeacon、CAME、CARDIAC-FM、CHARGE-AF score、CLM-X、CLOOME、CMAE、CPA、CTBA、CTransPath、Cell-o1、CellFM、CellFlux、CellOT、CellPaintSSL、CellWorld、China-AIHeart、D-SPIN、D2R2、DINO-WM、DISCO (ECG HFrEF study)、DNAmEMRAge、DamAge、DeepSeek-R1、DeepSeek-R1-Zero、DeepSeekMath、DiRL、ECG-AI (LA structure/function)、ECG-FM、ECG-LFM、ECG2CAD、ECG2Stroke、ECM aging clock、EHR-MPC、EHRAgent、EMRAge、ERA、Echo2HF、EpiZoo、Foresight、Foresight-England、GOLD BioAge、GPS_Mult (multi-ancestry CAD polygenic risk score)、GRASP、GeneCompass、GenePT、GenoAgent、GraphCL、Hannum epigenetic clock、Healthspan Proteomic Score (HPS)、JEPA-Anything、JEPA-DNA、Kimi k1.5、Kosmos、LPAI、LaMamba-Diff、LifeLong Digital Twin、LinAge2、MASPRM、MILTON、ML-CVD-C、MSGene、MSKAge / MSKAgeMort、MVX、Med-BERT
- 基准：ABC-Bench、AI4AI-Bench、AMC23、AdaJEPA、BAISBench、BIRD、BLADE、BioDataLab、BioKGBench、BioML-bench、BiomniBench-DA、CellBench、CellPuzzles、ComputAgeBench、D4RL、DiscoverPhysics、ESCALATE CAD PRS-triaged CACS pathway、GSM-HARD、Gaia2、HLE、Hofmarcher benchmark、LAB-Bench、LABBench2、LMR-BENCH、LVIS、LiveCodeBench、MLAgentBench、MMLU、MMLU-Medical、MedMCQA、MedPRMBench、MedQA、Moshkov benchmark、OfficeQA、PASCAL VOC、PertEval-scFM、PerturBench、PerturbQA、ProteinGym、RSIBench-Data、RoboTwin、Robomimic、SEAGym、SWE Bench Verified、SciIntegrity-Bench、ScienceAgentBench、SealQA、SoundnessBench、StreamBench、Systema、Terminal-Bench 2.0、ToolMaker Benchmark、VTAB、Virtual Cell Challenge 2026、X-ARES、scEval、scIB
- 数据库：Allen Brain Atlas、CMAP、CPRD (Clinical Practice Research Datalink)、CPRD Aurum、Cell Landscape、ChIP-Atlas、DISCO (single-cell database)、Danish National Patient Registry、ELAN、EMBL-EBI ArrayExpress/BioStudies、GeneATLAS、Immunosenescence Inventory、MCATS、MGB Biobank、PhysioNet、Proteome-Phenome Atlas、QResearch database、SEA-AD、STP、TEAPEE、TruDiagnostic
- 工具：AgentPRM、AusCVDRisk、AutoPrognosis、BASIL、BOLT-LMM、BioLLM、Biolearn、CHARLS web-based CVD risk calculator、CINEMA-OT、CROP-seq、Cell-Eval、CellOracle、CellPaint-POSH、CellProfiler、CellScientist、ClockBase Agent、DeGAs、FaithRL、GEPA、Habitat、Harmony、ICD-8 to ICD-10 Mapping Table、Intuitor、K-Dense、LWD-Miniscope、LivAge、Loki、Longevity Claw、Mortara VERITAS Algorithm、Mosaic、NMR Metabolomics Platform、Nahual、OSCAR、PHESANT、PRS-PheWAS atlas web application、PURE、PheMIME、PheWeb、Phecodes、ROSE、Rosetta、SAFEEVOLVE、SCOPE、SCanSNP、SPAC-seq、SPA_GRM、ScalePRM、SenePy、SpatialQM、TARDIS、TFActProfiler、The AI Scientist、TotalSegmentator、TranslAGE、TreeRL、UKB-MDRMF、Virtual Lab、copairs、leakcheck、moscot、scContam、ukbnmr
