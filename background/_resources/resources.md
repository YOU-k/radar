# 资源登记（数据集 / 模型 / 基准）

从 495 处证据引用中挖出 348 项命名资源；主表 96 项（被 ≥2 篇工作使用、或跨方向、或开放且链接核验通过且规模明确），其余 252 项单篇提及的列在末尾。核验：ok 可达 / blocked 站点拒绝探测 / dead 失效 / n/a 非链接。更新 2026-09-23


## 数据集（41）

| 名称 | 模态 | 规模 | 获取 | 开放 | 核验 | 方向 | 证据 | 用途 |
|---|---|---|---|---|---|---|---|---|
| **UK Biobank** | 多模态人群队列（影像/蛋白/基因） | 30,376人，2,923蛋白+251代谢物 | [链接](https://www.ukbiobank.ac.uk/) | restricted | blocked | 2 | 71 | 作为核心人群队列用于血浆蛋白组关联、代谢组风险评分、多基因风险蛋白组分析、WGS资源构建及疾病自然史生成模型训练。 |
| **FinnGen** | 血浆蛋白质组/遗传 | 176,899芬兰人；2,444疾病表型 | [链接](https://www.finngen.fi/) | restricted | ok | 2 | 4 | 芬兰隔离人群遗传资源，用于GWAS和精细定位发现低频变异关联。 |
| **GSM8K** | 小学数学应用题 | 8.5K道小学数学题 | [链接](https://huggingface.co/datasets/openai/gsm8k) | yes | ok | 2 | 2 | 用于评测MASPRM在多智能体推理中的表现。 |
| **All of Us Research Program** | EHR/生物标志物/基因组 | 245,388全基因组序列；393,590参与者 | [链接](https://www.researchallofus.org/) | restricted | ok | 1 | 11 | 用于生物标志物轨迹预测功能衰退、冠心病PRS一致性评估及PAD多基因评分验证。 |
| **ImageNet-1K** | 自然图像分类 | 约128万训练图像，1000类 | [链接](https://www.image-net.org/) | yes | ok | 1 | 8 | 用于线性评估、冻结探针分类及视频预训练模型评估。 |
| **UK Biobank Pharma Proteomics Project (UKB-PPP)** | 血浆蛋白质组 | 53,026人，2,920种蛋白 | [链接](https://www.ukbiobank.ac.uk/) | restricted | blocked | 1 | 5 | 用于构建血浆蛋白组-疾病-性状关联图谱及解析2型糖尿病多基因风险的蛋白标志物。 |
| **ModelNet40** | 3D点云/CAD模型 | 12,311模型，40类 | [链接](https://modelnet.cs.princeton.edu/) | yes | ok | 1 | 4 | 用于评估点云自监督方法（Point-JEPA、Point-MAE）的分类与少样本学习性能。 |
| **MATH** | 数学竞赛题 | 1.25万题 | [链接](https://huggingface.co/datasets/hendrycks/competition_math) | yes | ok | 1 | 3 | 评估数学推理能力，DeepSeekMath达51.7%。 |
| **UKB Exome Sequencing** | 全外显子测序 | 454,787人，12.3M变异 | [链接](https://www.ukbiobank.ac.uk/) | restricted | blocked | 1 | 3 | 用于罕见变异关联分析，揭示编码变异对复杂疾病的贡献。 |
| **23andMe** | GWAS汇总统计 | 最多697,815人（含多队列） | [链接](https://www.23andme.com/) | restricted | ok | 1 | 2 | 作为疾病不可知大队列之一，用于PheWAS药物靶点验证。 |
| **AMC23** | 数学竞赛题 | 40题 | [链接](https://huggingface.co/datasets/AI-MO/aimo-validation-amc) | yes | ok | 1 | 2 | 用于评测PURE在数学推理上的准确率。 |
| **China Kadoorie Biobank** | 血浆蛋白组/Olink | 3,977人 | [链接](https://www.ckbiobank.org) | restricted | blocked | 1 | 2 | 用于独立验证蛋白质组年龄时钟的跨人群队列。 |
| **COCO** | 图像检测/分割/字幕 | 约33万图像，80类 | [链接](https://cocodataset.org/) | yes | ok | 1 | 2 | 用于评估自监督表征在检测与分割任务上的迁移能力。 |
| **GeneCorpus-30M** | 单细胞转录组 | 约3000万细胞 | 论文/门户（Genecorpus-30M） | yes | n/a | 1 | 2 | 用于预训练Geneformer等单细胞基础模型的大规模单细胞转录组语料。 |
| **Global Biobank Meta-analysis Initiative (GBMI)** | GWAS汇总统计 | 23个生物样本库；220万人；14疾病终点 | [链接](https://www.globalbiobankmeta.org/) | restricted | ok | 1 | 2 | 用于跨祖源PRS方法评估及跨人群疾病遗传发现的荟萃分析。 |
| **JetClass** | 高能物理喷注粒子云 | 大规模喷注模拟数据集 | 项目网站公开 | yes | n/a | 1 | 2 | 用于预训练HEP-JEPA高能物理基础模型并评估top tagging等下游任务。 |
| **Mass General Brigham (MGBB)** | 多中心ICU/EHR队列 | 8家医院ICU脓毒症队列 |  | restricted | n/a | 1 | 2 | 用于脓毒症治疗推理时控制（EHR-MPC）评估及PAD多基因评分验证。 |
| **Perturb-seq** | CRISPR扰动单细胞转录组 | 4个数据集，约48.5万细胞 | GEO（文中引用数据集） | yes | n/a | 1 | 2 | CRISPR介导的pooled扰动单细胞RNA测序数据，用于构建遗传互作流形及基准测试基础模型扰动预测能力。 |
| **ScanObjectNN** | 三维点云 | 15类、约2902个样本 | [链接](https://hkust-vgd.github.io/scanobjectnn/) | yes | ok | 1 | 2 | 用于评估点云掩码自编码器在真实扫描物体分类任务上的下游泛化能力。 |
| **THL Biobank** | NMR代谢组与临床随访 | 参与三国生物库共700,217人 | [链接](https://thl.fi/en/web/thl-biobank) | restricted | dead | 1 | 2 | 用于训练和验证12种高DALY疾病的代谢组风险评分。 |
| **ADE20K** | 场景图像分割 | 2万余张图像 | [链接](https://groups.csail.mit.edu/vision/datasets/ADE20K/) | yes | ok | 1 | 1 | 用于Bootleg语义分割评估。 |
| **CeNGEN** | 线虫神经元RNA-seq | 128种神经元类型 | [链接](https://www.cengen.org/) | yes | ok | 1 | 1 | 提供晚期L4线虫神经元转录组数据，用于BitAge和Stochastic Clock预测神经元生物年龄。 |
| **COCO-Stuff** | 图像语义分割 | 含stuff类别标注 | [链接](https://github.com/nightrome/cocostuff) | yes | ok | 1 | 1 | 用于Bootleg语义分割评估。 |
| **FEVER** | 事实验证文本 | 约18万条声明 | [链接](https://fever.ai/) | yes | ok | 1 | 1 | 用于评测ReAct在事实核查任务中的推理与证据检索。 |
| **GSM-Plus** | 数学应用题 | 约1万题 | [链接](https://huggingface.co/datasets/qintongli/GSM-Plus) | yes | ok | 1 | 1 | 用于评测BiPRM在解级数学推理上的表现。 |
| **GTEx** | 多组织RNA-seq与基因型 | 全血581样本 | [链接](https://gtexportal.org/) | yes | ok | 1 | 1 | 用于分析TFMethyl Clock靶基因在血液中的表达。 |
| **HM3D v0.2** | 3D室内场景 | Habitat ObjectNav场景 | [链接](https://aihabitat.org/datasets/hm3d/) | yes | ok | 1 | 1 | 用于GLAM NAV在Habitat中ObjectNav子集的训练与评估。 |
| **HotpotQA** | 多跳问答文本 | 约11万问答对 | [链接](https://hotpotqa.github.io/) | yes | ok | 1 | 1 | 用于评测ReAct在知识密集型多跳问答中的推理与检索能力。 |
| **ImageNet ILSVRC-2012** | 自然图像 | 1000类约128万图像 | [链接](https://www.image-net.org/challenges/LSVRC/2012/) | yes | ok | 1 | 1 | 用于SimCLR线性评估与半监督微调评估。 |
| **iNaturalist-21** | 自然图像 | 21类物种图像 | [链接](https://github.com/visipedia/inat_comp) | yes | ok | 1 | 1 | 用于Bootleg冻结探针分类评估。 |
| **Libri-light** | 语音音频 | 60000小时 | [链接](https://github.com/facebookresearch/libri-light) | yes | ok | 1 | 1 | 用于大规模无标注语音自监督预训练及多规模微调评估HuBERT。 |
| **Librispeech** | 语音音频 | 960小时 | [链接](https://www.openslr.org/12) | yes | ok | 1 | 1 | 用于微调和评估HuBERT语音表征在下游语音识别任务上的性能。 |
| **LVIS** | 大规模实例分割 | 约12万图像，1200+类 | [链接](https://www.lvisdataset.org/) | yes | ok | 1 | 1 | 用于评估SiameseIM表征的实例分割迁移性能。 |
| **MATH500** | 数学竞赛题 | 500题 | [链接](https://huggingface.co/datasets/HuggingFaceH4/MATH-500) | yes | ok | 1 | 1 | 用于评测BiPRM在解级数学推理上的表现。 |
| **MNIST** | 手写数字图像 | 7万张图像 | [链接](http://yann.lecun.com/exdb/mnist/) | yes | ok | 1 | 1 | 用于BiJEPA的双向表征学习实验。 |
| **MODIS** | 热红外遥感影像 | 全球覆盖 | [链接](https://modis.gsfc.nasa.gov/) | yes | ok | 1 | 1 | 作为Mini-JEPA舰队中热红外传感器模型的训练数据。 |
| **Pan-UK Biobank GWAS** | GWAS汇总统计 | 7,271表型；多祖源 | [链接](https://pan.ukbb.broadinstitute.org/) | yes | ok | 1 | 1 | 提供跨群体GWAS与荟萃分析汇总统计，用于遗传结构解析与祖源富集效应发现。 |
| **Perturb-seq genome-scale screen** | CRISPRi扰动scRNA-seq | K562与RPE1，数千个敲低扰动 | [链接](https://doi.org/10.1016/j.cell.2022.05.013) | yes | ok | 1 | 1 | 首个基因组规模Perturb-seq筛选，用于研究基因功能与调控网络。 |
| **PRM800K** | 数学推理步级标注 | 80万步级标签 | [链接](https://github.com/openai/prm800k) | yes | ok | 1 | 1 | 用于训练过程奖励模型PURE的步级监督数据。 |
| **Sentinel-1** | SAR遥感影像 | 全球覆盖 | [链接](https://dataspace.copernicus.eu/) | yes | ok | 1 | 1 | 作为Mini-JEPA舰队中SAR传感器模型的训练数据。 |
| **Sentinel-2** | 多光谱光学遥感影像 | 全球覆盖 | [链接](https://dataspace.copernicus.eu/) | yes | ok | 1 | 1 | 作为Mini-JEPA舰队中光学传感器模型的训练数据。 |

## 模型（24）

| 名称 | 模态 | 规模 | 获取 | 开放 | 核验 | 方向 | 证据 | 用途 |
|---|---|---|---|---|---|---|---|---|
| **scGPT** | 单细胞转录组基础模型 | 3300万+细胞预训练 | [链接](https://doi.org/10.1038/s41592-024-02201-0) | yes | ok | 1 | 8 | 生成式预训练Transformer单细胞基础模型，用于细胞类型注释、扰动预测等下游任务，并被用作扰动后RNA-seq预测基准的对比模型。 |
| **Geneformer** | 单细胞转录组基础模型 | 约3000万细胞预训练 | [链接](https://doi.org/10.1038/s41586-023-06139-9) | yes | ok | 1 | 6 | 作为被评估/被解释的单细胞基础模型，用于注意力可解释性、SAE 图谱与电路追踪研究。 |
| **Qwen3-4B** | 文本大语言模型 | 40亿参数 | Hugging Face (Qwen/Qwen3-4B) | yes | n/a | 1 | 3 | 作为S-trace与GEAR方法的实验基座模型，评测数学推理与工具使用任务。 |
| **scFoundation** | 单细胞转录组基础模型 | 大规模单细胞预训练模型 | [链接](https://doi.org/10.1186/s12864-025-11600-2) | yes | ok | 1 | 3 | Transformer单细胞基础模型，在扰动后RNA-seq预测基准中与scGPT一同被评估。 |
| **DINO-WM** | 离线行为轨迹/图像 | 三维操作任务 |  | unknown | n/a | 1 | 2 | 作为冻结的预训练世界模型，用于验证Sandwich-Residuals在三维操作任务上的测试时自适应效果。 |
| **Horvath DNAm age clock (353 CpG)** | DNA甲基化 | 353 CpG，误差约3.6年 |  | unknown | n/a | 1 | 2 | 跨组织DNA甲基化年龄预测器，用于评估表观年龄加速。 |
| **Longevity-LLM** | DNA甲基化/蛋白组/临床/RNA | 0.6B-9B参数/5个模型 | [链接](https://doi.org/10.1016/j.cell.2026.08.026) | yes | ok | 1 | 2 | 在Longevity Bench任务中排名较高，表观年龄预测MAE达4.34年。 |
| **Qwen2.5-Math-7B** | 数学推理语言模型 | 70亿参数 | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-7B) | yes | ok | 1 | 2 | 作为PURE与ScalePRM的基座模型，用于数学推理RL训练。 |
| **Qwen3-1.7B** | 文本大语言模型 | 1.7B参数 | Hugging Face (Qwen/Qwen3-1.7B) | yes | n/a | 1 | 2 | 作为S-trace选择性资格迹方法的实验基座模型之一，评测推理任务pass@16。 |
| **Qwen3-8B** | 文本大语言模型 | 8B参数 | Hugging Face (Qwen/Qwen3-8B) | yes | n/a | 1 | 2 | 作为S-trace与GEAR方法的实验基座模型，评测数学推理与工具使用任务。 |
| **BYOL** | 自然图像 | ResNet-50/更大ResNet | [链接](https://github.com/deepmind/deepmind-research/tree/master/byol) | yes | ok | 1 | 1 | 不依赖负样本的自监督图像表征学习方法，用于ImageNet线性评估与迁移。 |
| **DINO** | 自蒸馏视觉Transformer | ViT-Base线性评估80.1% | [链接](https://github.com/facebookresearch/dino) | yes | ok | 1 | 1 | 无标签自蒸馏自监督方法，赋予ViT语义分割特性。 |
| **HuBERT** | 语音表征 | 最大1B参数 | [链接](https://github.com/facebookresearch/fairseq/tree/main/examples/hubert) | yes | ok | 1 | 1 | 提出并发布的语音自监督预训练模型，通过掩码预测隐藏单元学习语音表征。 |
| **I-JEPA** | 联合嵌入预测表征 | ViT-Huge/14，16×A100训练<72h | [链接](https://github.com/facebookresearch/ijepa) | yes | ok | 1 | 1 | 不依赖数据增强的图像联合嵌入预测自监督模型。 |
| **LaMamba-Diff** | 扩散生成模型 | ImageNet 256/512，线性复杂度 | [链接](https://github.com/) | yes | ok | 1 | 1 | 融合局部注意力与Mamba的高效高保真扩散生成模型。 |
| **MAE** | 掩码图像自编码表征 | ViT-Huge，ImageNet-1K达87.8% | [链接](https://github.com/facebookresearch/mae) | yes | ok | 1 | 1 | 掩码自编码器，用于可扩展视觉自监督预训练。 |
| **MoCo** | 视觉对比学习表征 | ResNet-50骨干，ImageNet预训练 | [链接](https://github.com/facebookresearch/moco) | yes | ok | 1 | 1 | 提出队列与动量编码器构建动态字典的对比学习模型。 |
| **OmiCLIP** | 组织病理图像+空间转录组 | 基于220万配对patch训练 | [链接](https://doi.org/10.1038/s41592-025-02707-1) | yes | ok | 1 | 1 | 转录组-图像双编码器基础模型，通过CLIP对比学习对齐图像与基因句子表示。 |
| **PRnet** | 化学扰动转录响应 | 约1亿bulk观测、175,549化合物；数千万单细胞、188化合物 | [链接](https://doi.org/10.1038/s41467-024-53457-1) | yes | ok | 1 | 1 | 扰动条件深度生成模型，以化合物SMILES和未扰动转录谱预测新化学扰动的bulk与单细胞转录响应。 |
| **Qwen2.5-7B** | 语言模型 | 70亿参数 | [链接](https://huggingface.co/Qwen/Qwen2.5-7B) | yes | ok | 1 | 1 | 作为PURE方法验证的基座模型之一。 |
| **Qwen2.5-Math-1.5B** | 数学推理语言模型 | 15亿参数 | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-1.5B) | yes | ok | 1 | 1 | 作为PURE方法验证的轻量基座模型。 |
| **SANA-WM** | 视频生成/世界模型 | 2.6B参数 | [链接](https://doi.org/10.48550/arXiv.2605.15178) | yes | ok | 1 | 1 | 开源世界模型，支持一分钟720p视频生成与相机控制。 |
| **SCimilarity** | 单细胞转录组 | 2340万细胞，412项研究 | [链接](https://doi.org/10.1038/s41586-024-08411-y) | yes | ok | 1 | 1 | 深度度量学习基础模型，实现跨组织疾病的相似细胞可扩展搜索。 |
| **SimCLR** | 自然图像 | ResNet-50对比学习框架 | [链接](https://github.com/google-research/simclr) | yes | ok | 1 | 1 | 无需专用架构或记忆库的对比学习框架，用于图像自监督表征学习。 |

## 基准（18）

| 名称 | 模态 | 规模 | 获取 | 开放 | 核验 | 方向 | 证据 | 用途 |
|---|---|---|---|---|---|---|---|---|
| **MMLU** | 多学科知识问答 | 1.4万题、57学科 | [链接](https://huggingface.co/datasets/cais/mmlu) | yes | ok | 2 | 2 | 用于评测MASPRM在多学科推理任务中的表现。 |
| **ALFWorld** | 文本交互式具身任务 | 6类任务、数千回合 | [链接](https://alfworld.github.io/) | yes | ok | 1 | 4 | 作为SELAUR智能体强化学习框架的评测环境之一，衡量任务成功率。 |
| **ProcessBench** | 推理步级错误检测 | 3400条推理路径 | [链接](https://huggingface.co/datasets/Qwen/ProcessBench) | yes | ok | 1 | 2 | 用于评测BiPRM与ScalePRM的步级错误检测能力。 |
| **scIB** | scRNA/scATAC整合 | 13个整合任务，最多23批次、100万细胞 | [链接](https://doi.org/10.1038/s41592-021-01336-8) | yes | ok | 1 | 2 | 单细胞数据整合工具的标准基准，用于评估批次去除与生物变异保留。 |
| **WebShop** | 网页购物交互任务 | 118万商品、1.2万指令 | [链接](https://webshop-pnlp.github.io/) | yes | ok | 1 | 2 | 作为SELAUR智能体强化学习框架的评测环境之一，衡量任务成功率。 |
| **AI4AI-Bench** | 算法设计智能体任务 | 10仓库×29配置×6系统×10任务 | [链接](https://arxiv.org/abs/2608.20318) | yes | ok | 1 | 1 | 评测LLM智能体在递归自我改进中算法设计能力的隔离基准。 |
| **GenoTEX** | 基因表达数据分析 | 含专家标注代码与结果 | [链接](https://github.com/Liu-Hy/GenoTEX) | yes | ok | 1 | 1 | 评估LLM智能体自动化基因表达分析流程的基准。 |
| **LOGIQA** | 逻辑推理问答 | 约1万题 | [链接](https://huggingface.co/datasets/lucasmccabe/logiqa) | yes | ok | 1 | 1 | 用于评测MASPRM在逻辑推理任务中的表现。 |
| **LongevityBench** | 多组学衰老数据 | 17项任务/5个数据域 | [链接](https://doi.org/10.1016/j.cell.2026.08.026) | yes | ok | 1 | 1 | 用于评估AI系统理解衰老生物学异构数据能力的公开基准。 |
| **NKIBench** | AI加速器内核代码 | 来自真实LLM工作负载的Trainium内核，复杂度不一 | [链接](https://github.com/zhang677/AccelOpt) | yes | ok | 1 | 1 | 用于评测LLM智能体自主优化AWS Trainium AI加速器内核的性能。 |
| **PASCAL VOC** | 图像检测与分割 | 约1.1万图像，20类 | [链接](http://host.robots.ox.ac.uk/pascal/VOC/) | yes | ok | 1 | 1 | 用于评估无监督预训练表征的检测/分割迁移性能。 |
| **R-Judge** | 多轮智能体交互文本 | 569条交互记录，27类风险场景 | [链接](https://github.com/Lordog/R-Judge) | yes | ok | 1 | 1 | 用于评测LLM智能体在交互环境中的安全风险意识。 |
| **SKILLMISEVO-BENCH** | 智能体技能安全基准 | 未明确 | [链接](https://github.com/henrymao2004/misevolve) | yes | ok | 1 | 1 | 冻结基准，用于评估技能误演化与安全修复。 |
| **SKILLMISEVO-GYM** | 智能体技能演化测试台 | 25种配置，各525任务、25回合 | [链接](https://github.com/henrymao2004/misevolve) | yes | ok | 1 | 1 | 生命周期感知测试台，用于研究技能误演化。 |
| **Socratic-PRMBench** | 推理过程错误检测 | 2995条缺陷路径、平均8.7步 | [链接](https://github.com/Xiang-Li-oss/Socratic-PRMBench) | yes | ok | 1 | 1 | 用于系统评测PRM在六种推理模式下的过程错误检测能力。 |
| **TruthInsightBench** | 开放式科学发现任务与评分 | 40个盲任务/10领域/40篇研究 | [链接](https://github.com/TruthInsight-stack/TruthInsightBench) | yes | ok | 1 | 1 | 评测开放式科学发现智能体，含6维度29个证据锚定评分项。 |
| **Virtual Cell Challenge** | 扰动响应单细胞数据 | 专用扰动数据集（规模未明） | [链接](https://doi.org/10.1016/j.cell.2025.06.008) | yes | ok | 1 | 1 | 虚拟细胞挑战赛，提供评估框架与数据集以预测扰动响应。 |
| **VTAB** | 视觉任务集合 | 19个视觉任务 | [链接](https://github.com/google-research/task_adaptation) | yes | ok | 1 | 1 | 用于Bootleg冻结探针分类评估。 |

## 数据库（10）

| 名称 | 模态 | 规模 | 获取 | 开放 | 核验 | 方向 | 证据 | 用途 |
|---|---|---|---|---|---|---|---|---|
| **ARCHS4** | 人类RNA-seq转录组 | 约5.7万样本，28组织，1-114岁 | [链接](https://maayanlab.cloud/archs4/) | yes | ok | 1 | 2 | 用于训练和验证转录组年龄预测模型及不确定性感知衰老时钟。 |
| **Human Cell Atlas** | 多模态单细胞图谱 | 全球细胞图谱计划 | [链接](https://doi.org/10.1038/s41586-024-08338-4) | yes | ok | 1 | 2 | 细胞图谱计划，作为细胞普查、3D图谱与基础模型的数据基础。 |
| **Allen Brain Atlas** | 空间转录组/脑图谱 | 全脑多区域空间转录组图谱 | [链接](https://portal.brain-map.org/) | yes | ok | 1 | 1 | 提供脑发育空间转录组数据，用于参数化可解释细胞行为语法构建的agent-based虚拟细胞模型。 |
| **CZ CELLxGENE Discover** | 单细胞转录组 | 超7000万细胞 | [链接](https://cellxgene.cziscience.com) | yes | ok | 1 | 1 | 用于训练scAgeClock单细胞转录组人类衰老时钟模型。 |
| **EMBL-EBI ArrayExpress** | DNA甲基化等组学数据 | 51项人类干预研究 | [链接](https://www.ebi.ac.uk/biostudies/arrayexpress) | yes | ok | 1 | 1 | 提供表观遗传衰老生物标志物响应性分析所用的公开DNAm数据。 |
| **GeneATLAS** | GWAS汇总统计 | 778性状/911万变异 | [链接](http://geneatlas.roslin.ed.ac.uk) | yes | ok | 1 | 1 | UK Biobank遗传关联图谱的统一查询数据库。 |
| **GEO** | DNA甲基化等组学数据 | 51项人类干预研究 | [链接](https://www.ncbi.nlm.nih.gov/geo/) | yes | ok | 1 | 1 | 提供表观遗传衰老生物标志物响应性分析所用的公开DNAm数据。 |
| **NHGRI-EBI GWAS Catalog** | GWAS关联与汇总统计 | 625,113关联、>85K数据集 | [链接](https://www.ebi.ac.uk/gwas/) | yes | ok | 1 | 1 | 标准化收集人类GWAS关联和汇总统计，支持可复用研究。 |
| **PGS Catalog** | 多基因评分 | 未明确 | [链接](https://www.pgscatalog.org/) | yes | ok | 1 | 1 | 与GWAS Catalog互链，提供多基因评分资源。 |
| **Proteome-Phenome Atlas** | 血浆蛋白组-疾病关联 | 53,026人，2,920蛋白，406+660疾病 | [链接](https://proteome-phenome-atlas.com) | yes | ok | 1 | 1 | 开放获取的血浆蛋白组-疾病-性状关联图谱门户，支持蛋白-疾病关联查询。 |

## 工具（3）

| 名称 | 模态 | 规模 | 获取 | 开放 | 核验 | 方向 | 证据 | 用途 |
|---|---|---|---|---|---|---|---|---|
| **Cell Painting** | 高内涵细胞成像 | 十年积累的公开图像profiling数据集 | [链接](https://doi.org/10.1038/s41592-024-02528-8) | yes | ok | 2 | 2 | 基于多荧光标记的细胞形态学profiling检测，用于解析化合物作用机制、毒性及基因功能推断。 |
| **MEDICINE portal** | MRI器官衰老时钟模型与结果 | 274247人 / 107代谢物 | MEDICINE门户 | yes | n/a | 2 | 2 | 公开多器官代谢组生物年龄模型、预训练模型及相关结果。 |
| **CellProfiler** | 显微图像特征提取 | 开源图像分析软件 | cellprofiler.org | yes | n/a | 1 | 2 | 作为经典手工图像特征提取基线，与深度学习特征在 MoA 预测等任务中比较。 |

## 单篇提及（252，未进主表）

- 数据集：ARIC、Atherosclerosis Risk in Communities (ARIC) Study、AudioSet、AudioSet-20K、Biobank Japan、CHOP、Cityscapes、DFTJ、Danish National Patient Registry、Droid、EPIC-Norfolk、ESC-50、Estonian Biobank、FINRISK、FSD50K、Fenland、Framingham Heart Study (FHS)、Framingham Offspring Study (FOS)、GIANT、GSE67752、Generation Scotland、INSPIRE-T cohort、Israel 10K Project、JUMP Cell Painting Consortium data、Jackson Heart Study (AASK)、Lorenz attractor、Lothian Birth Cohort 1936、MESA、MGB Biobank、MIMIC、MIMIC-III、MIMIC-IV、Mass General Brigham Biobank、Mexico City Prospective Study (MCPS)、NHANES、NPBBD-Korea、Norman K562 CRISPRa dataset、Nurses' Health Study (NHS)、PRECISE、Penn Medicine BioBank (PMBB)、PerturbReason、Robomimic、SCIPRM70K、SEA-AD、ST-bank、Tabula Sapiens、Taiwan Biobank (TWB)、Taiwan Precision Medicine Initiative (TPMI)、Tox21、TruDiagnostic、UCLA Biobank、UK Biobank Exome Sequencing Consortium (UKB-ESC)、UK Biobank Whole-Genome Sequencing、UKB NMR Metabolomics、US Veterans Affairs EHR、Wikitext、mCAS
- 模型：3D-JEPA、ALADYNOULLI、AROMA、ATM、AdaptAge、AlphaEarth、Audio-MAE、BEHRT、BitAge、Bootleg、CAE (Context Autoencoder)、CMAE、CPA、CTBA (CT-based Biological Age)、CTransPath、Cell-o1、CellFM、CellWorld、Co-Scientist、CrossJEPA、DINOv2、DNAm PhenoAge、DNAmEMRAge、DamAge、DeepSeek-R1、DeepSeek-R1-Zero、DeepSeekMath 7B、Delphi-2M、EMRAge、EvoScientist、Flow-JEPA、Foresight、Foresight-England、GEARS、GLAM、GLAM NAV、GOLD BioAge、GRASP、GenoAgent、Graph-JEPA、GraphCL、HEP-JEPA、HPS (Healthspan Proteomic Score)、Hannum DNAm age clock、Horvath clock、Horvath multi-tissue clock、Intuitor、JEPA-Anything、JEPA-DNA、JetParticle-JEPA (JP-JEPA)、Kimi k1.5、LeJEPA、LeVJEPA、LinAge2、Longitudinal Proteomic Aging Index (LPAI)、MILTON、MSGene、MSKAge / MSKAgeMort、MatClaw、Med-BERT、MetBAG、MetaboHealth、Metabolic Vulnerability Index (MVX)、Music-JEPA、NOAH、NeRF-MAE、OMICmAge、PAST、PRS-PAD、PULSE、Pasta、PathwayAge、PedBE clock、PerturbNet、Phikon、Physiological Aging Index (PAI)、Plan2Explore、Point-Delta-JEPA、Point-JEPA、Point-LeWM
- 基准：ABC-Bench、AdaJEPA、BIRD、BLADE、Baba in Wonderland、BioDataLab、BioKGBench、BiomniBench-DA、CellPuzzles、ComputAgeBench、D4RL、DiscoverPhysics、GSM-HARD、Gaia2、HLE、HumanEval、LMR-BENCH、LiveCodeBench、Longevity Bench、MMLU-Medical、MedMCQA、MedPRMBench、MedQA、MemCalib、OfficeQA、ProteinGym、PushT、RSIBench-Data、RoboTwin、SEAGym、SWE Bench Verified、SciIntegrity-Bench、ScienceAgentBench、SealQA、SoundnessBench、StreamBench、Terminal-Bench 2.0、ToolMaker Benchmark、X-ARES
- 数据库：CMAP、CPRD Aurum、ENCODE、Immunosenescence Inventory、MEDICINE、TEAPEE
- 工具：BASIL、BOLT-LMM、Biolearn、CellPaint-POSH、ClockBase Agent、DeGAs、FaithRL、GATK、GEPA、Habitat、Hail、Harmony、ICD-8 to ICD-10 Mapping、K-Dense、LivAge、Loki、Longevity Claw、Olink、PHESANT、Perturb-FISH、PheMIME、PheWeb、Phecodes、REGENIE、SAFEEVOLVE、SAIGE-GENE、STREME、SenePy、SomaLogic、SomaScan、The AI Scientist、TranslAGE、UKB-MDRMF、copairs、moscot、scContam、ukbnmr
