# 资源登记（数据集 / 模型 / 基准）

从 780 处证据引用中挖出 515 项命名资源；主表 151 项（被 ≥2 篇工作使用、或跨方向、或开放且链接核验通过且规模明确），其余 364 项单篇提及的列在末尾。核验：ok 可达 / blocked 站点拒绝探测 / dead 失效 / n/a 非链接。更新 2026-09-27


## 数据集（50）

| 名称 | 模态 | 规模 | 获取 | 开放 | 核验 | 方向 | 证据 | 用途 |
|---|---|---|---|---|---|---|---|---|
| **UK Biobank** | 多模态人群队列（影像/蛋白/基因） | 30,376人；2,923蛋白+251代谢物 | [链接](https://www.ukbiobank.ac.uk/) | restricted | blocked | 3 | 112 | 用于代谢评分、CNV负担、遗传关联、蛋白组性别差异、蛋白组衰老、生理衰老指数、稀疏回归及慢性疼痛GWAS等分析。 |
| **UK Biobank Pharma Proteomics Project (UKB-PPP)** | 血浆蛋白组学 | 54,219人 / 2,923蛋白 | [链接](https://www.ukbiobank.ac.uk/) | restricted | blocked | 2 | 10 | 用于构建血浆蛋白组-疾病-性状关联图谱及解析2型糖尿病多基因风险的蛋白标志物。 |
| **China Kadoorie Biobank** | 流行病学队列、ECG、电子健康记录 | 约51万人（本研究子集2.5万–4.3万） | [链接](https://www.ckbiobank.org/) | restricted | blocked | 2 | 8 | 用于中国成人ECG异常流行率、心血管风险预测模型验证与跨国风险方程比较。 |
| **ARIC** | 人群队列/血浆蛋白组 | V3 10,638 / V5 3,908 | [链接](https://www2.cscc.unc.edu/aric/) | restricted | ok | 2 | 4 | 用于血浆蛋白组与心衰、衰弱及高血压发病关联分析。 |
| **FinnGen** | 人群队列基因组/表型 | 176,899芬兰人，2,444表型 | [链接](https://www.finngen.fi/) | restricted | ok | 2 | 4 | 芬兰隔离人群疾病遗传资源，用于GWAS与精细定位发现低频变异关联。 |
| **Mass General Brigham Biobank** | 生物样本库、电子健康记录、基因型 | 约5.3万例（670例颈动脉狭窄+52,636对照） | [链接](https://www.massgeneralbrigham.org/research/biobank) | restricted | dead | 2 | 4 | 用于评估CAD、PAD、IS和cIMT多基因风险评分与颈动脉狭窄的关联。 |
| **Tahoe-100M** | 单细胞转录组+药物扰动 | 1亿转录组，50细胞系，1100药物条件 | 公开释放（Tahoe-100M） | yes | n/a | 2 | 4 | 大规模单细胞药物扰动图谱，用于预训练与机制/基因型特异药物响应发现。 |
| **Framingham Heart Study** | 前瞻队列、心血管危险因素 | 10,097人，28,151份ECG | [链接](https://www.framinghamheartstudy.org/) | restricted | ok | 2 | 3 | 社区队列用于优化和测试ECG-AF深度学习模型。 |
| **MESA** | 队列/影像/ECG/生物标志物 | 6814人，随访12年，735变量 | [链接](https://www.mesa-nhlbi.org/) | restricted | ok | 2 | 3 | 作为外部验证队列用于CARDIAC-FM心血管风险预测验证。 |
| **Atherosclerosis Risk in Communities (ARIC) Study** | 前瞻队列、心血管流行病学 | 7,213欧裔+1,871非裔，4,657蛋白 | [链接](https://aric.cscc.unc.edu/) | restricted | ok | 2 | 2 | 用于cis-pQTL定位与蛋白组预测模型构建，比较欧裔与非裔人群。 |
| **BioBank Japan (BBJ)** | 人群队列/基因组 | 日本9,826例AF/140,446对照 | [链接](https://biobankjp.org/) | restricted | ok | 2 | 2 | 作为国家生物样本库WGS项目案例，用于比较设计、技术与发现经验。 |
| **GSM8K** | 小学数学推理 | 小学数学应用题基准 | [链接](https://github.com/openai/grade-school-math) | yes | ok | 2 | 2 | 用于评估DLLM-JEPA在数学推理任务上的性能提升。 |
| **MIMIC-IV** | 重症监护EHR/波形 | 重症监护EHR（多任务基准） | [链接](https://physionet.org/content/mimiciv/) | restricted | ok | 2 | 2 | 作为MiGHT-EHR多任务图Transformer的评测数据集之一。 |
| **Penn Medicine BioBank** | 生物样本库（基因/EHR） | 参与PRS评估人群 | [链接](https://www.pennmedicine.org/for-patients-and-visitors/penn-medicine-divisions/penngen) | restricted | dead | 2 | 2 | 用于构建整合基因组和蛋白组的冠脉微血管疾病风险预测框架。 |
| **All of Us Research Program** | EHR、问卷、基因组、生物样本 | 39.3万人（含24.5万WGS） | [链接](https://www.researchallofus.org/) | restricted | ok | 1 | 10 | 用于多血统PRS评估及PME与HPO两种EHR来源的关联复制比较。 |
| **ImageNet-1k** | 自然图像 | 约128万训练图像，1000类 | [链接](https://www.image-net.org/) | yes | ok | 1 | 8 | 作为自监督视觉预训练与线性评估的主要基准数据集。 |
| **ModelNet40** | 3D点云 | 40类、12311个模型 | [链接](https://modelnet.cs.princeton.edu/) | yes | ok | 1 | 4 | 用于点云自监督方法的线性分类与少样本分类评估。 |
| **MATH** | 数学竞赛推理 | 约12500题 | [链接](https://github.com/hendrycks/math) | yes | ok | 1 | 3 | 用于评测MASPRM在数学推理任务中的表现。 |
| **Perturb-seq** | scRNA-seq + CRISPR 扰动 | 约 20 万细胞 |  | unknown | n/a | 1 | 3 | 将单细胞 RNA-seq 与 CRISPR 扰动结合，用于大规模检测转录表型与遗传互作。 |
| **AMC23** | 数学竞赛推理 | 40题 | [链接](https://huggingface.co/datasets/AI-MO/aimo-validation-amc) | yes | dead | 1 | 2 | 用于评测PURE方法在数学竞赛题上的推理性能。 |
| **Cardiovascular Health Study** | 老年前瞻队列、心血管数据 | 约5,888人 | [链接](https://chs-nhlbi.org/) | restricted | ok | 1 | 2 | 外部队列用于验证ECG-AI估计左房结构与功能及预测心血管结局。 |
| **CHARLS** | 人群队列/临床 | 约23,000人 / 9年随访 | [链接](http://charls.pku.edu.cn/) | restricted | ok | 1 | 2 | 作为外部验证队列用于China-AIHeart Transformer模型验证。 |
| **CHS** | 人群队列/蛋白组学 | 3,189人 |  | restricted | n/a | 1 | 2 | 作为外部验证队列用于心衰/衰弱蛋白组学及CARDIAC-FM验证。 |
| **COCO** | 图像检测/分割/字幕 | 约33万图像，80类 | [链接](https://cocodataset.org/) | yes | ok | 1 | 2 | 用于评估自监督预训练模型在检测与分割下游任务上的迁移能力。 |
| **ELSA-Brasil** | 前瞻队列/ECG | 巴西成人队列（规模未明确） | [链接](https://www.elsa.org.br/) | restricted | dead | 1 | 2 | 作为外部前瞻队列验证单导联AI-ECG心衰风险分层。 |
| **ESTHER** | 人群队列、代谢组 | 5,578-8,308人 |  | unknown | n/a | 1 | 2 | 德国队列，用于代谢组学心血管风险预测的外部验证。 |
| **Genecorpus-30M** | 单细胞转录组 | 约3000万细胞 |  | unknown | n/a | 1 | 2 | 作为scFM预训练语料，用于审计基准污染及Geneformer预训练。 |
| **Global Biobank Meta-analysis Initiative (GBMI)** | GWAS荟萃汇总统计 | 23库，220万人，14疾病 | [链接](https://www.globalbiobankmeta.org/) | restricted | ok | 1 | 2 | 跨生物样本库荟萃分析资源，用于跨祖源PRS评估与遗传发现。 |
| **JetClass** | 高能物理喷注粒子云 | 1亿个喷注 | 项目网站公开 | yes | n/a | 1 | 2 | 用于预训练HEP-JEPA高能物理基础模型并评估top tagging等下游任务。 |
| **Pan-UK Biobank GWAS summary statistics** | GWAS汇总统计 | 7266个性状，多祖源 | [链接](https://pan.ukbb.broadinstitute.org/) | yes | ok | 1 | 2 | 提供跨祖源GWAS与荟萃分析汇总统计，用于遗传结构解析。 |
| **Replogle 2022 Perturb-seq** | CRISPRi单细胞转录组 | >250万人类细胞 | [链接](https://doi.org/10.1016/j.cell.2022.05.013) | yes | ok | 1 | 2 | 基因组规模Perturb-seq图谱，用于扰动预测建模与基准评估。 |
| **ScanObjectNN** | 三维点云 | 15类、约15000样本 | [链接](https://hkust-vgd.github.io/scanobjectnn/) | yes | ok | 1 | 2 | 用于评估点云掩码自编码器在真实扫描物体分类上的下游性能。 |
| **THL Biobank** | NMR代谢组与临床随访 | 三国生物库共700,217人 | [链接](https://thl.fi/en/web/thl-biobank) | restricted | dead | 1 | 2 | 用于重复验证UKB血浆NMR代谢标志物与疾病的关联。 |
| **AudioSet** | 音频（10s片段，32kHz） | 无标签音频片段 | [链接](https://research.google.com/audioset/) | yes | ok | 1 | 1 | 用于Audio-JEPA的无标签预训练，学习掩码梅尔频谱块的隐表征。 |
| **CeNGEN** | 线虫神经元RNA-seq | 128种神经元类型 | [链接](https://www.cengen.org/) | yes | ok | 1 | 1 | 提供线虫晚期L4神经元转录组数据，用于BitAge和Stochastic Clock预测神经元生物年龄。 |
| **CODE15** | 12导联ECG | 233647份ECG | [链接](https://doi.org/10.1038/s41591-023-02235-5) | yes | ok | 1 | 1 | 作为ECG死亡风险模型的外部验证队列。 |
| **CTRP** | 药物基因组学 | 大型癌细胞系药物面板 | [链接](https://portals.broadinstitute.org/ctrp) | yes | ok | 1 | 1 | 用于评估单药癌症药物盲响应预测泛化能力。 |
| **FEVER** | 事实验证 | 约18万条声明 | [链接](https://fever.ai/) | yes | ok | 1 | 1 | 用于评测ReAct在事实核查任务中的表现。 |
| **GTEx** | 全血RNA-seq | 581样本 | [链接](https://gtexportal.org/) | yes | ok | 1 | 1 | 用于分析TFMethyl Clock靶基因表达。 |
| **HotpotQA** | 多跳问答 | 约11万问答对 | [链接](https://hotpotqa.github.io/) | yes | ok | 1 | 1 | 用于评测ReAct在知识密集型多跳问答中的推理与行动协同能力。 |
| **Libri-light** | 语音音频 | 60000小时 | [链接](https://github.com/facebookresearch/libri-light) | yes | ok | 1 | 1 | 用于大规模无标注语音预训练及多规模微调评估HuBERT。 |
| **Librispeech** | 语音音频 | 960小时 | [链接](https://www.openslr.org/12) | yes | ok | 1 | 1 | 用于微调和评估HuBERT语音表征在语音识别任务上的性能。 |
| **LVIS** | 图像实例分割 | 约16万图像，1200+类 | [链接](https://www.lvisdataset.org/) | yes | ok | 1 | 1 | 用于评估SiameseIM在长尾实例分割任务上的迁移性能。 |
| **MATH500** | 数学推理 | 500题 | [链接](https://github.com/openai/prm800k) | yes | ok | 1 | 1 | 用于评测BiPRM在解级数学推理上的表现。 |
| **McFarland** | 单细胞药物扰动 | 大规模药物扰动数据 | [链接](https://www.ncbi.nlm.nih.gov/geo) | yes | ok | 1 | 1 | 作为药物扰动预测基准数据集。 |
| **MNIST** | 手写数字图像 | 7万张28x28图像 | [链接](http://yann.lecun.com/exdb/mnist/) | yes | ok | 1 | 1 | 用于BiJEPA验证双向JEPA在图像数据上的稳定收敛与表征学习。 |
| **MODIS** | 热红外遥感影像 | 全球覆盖卫星影像 | [链接](https://modis.gsfc.nasa.gov/) | yes | ok | 1 | 1 | 作为Mini-JEPA舰队中热红外传感器模型的训练与预测数据源。 |
| **PRM800K** | 数学推理步级标注 | 80万步级标签 | [链接](https://github.com/openai/prm800k) | yes | ok | 1 | 1 | 用于训练过程奖励模型PURE。 |
| **SaMi-Trop** | 12导联ECG | 1631人 | [链接](https://doi.org/10.1371/journal.pntd.0006847) | yes | ok | 1 | 1 | 作为ECG死亡风险模型的国际外部验证队列。 |
| **SciPlex3** | 单细胞药物扰动 | 大规模药物扰动数据 | [链接](https://www.ncbi.nlm.nih.gov/geo) | yes | ok | 1 | 1 | 作为药物扰动预测基准数据集。 |

## 模型（55）

| 名称 | 模态 | 规模 | 获取 | 开放 | 核验 | 方向 | 证据 | 用途 |
|---|---|---|---|---|---|---|---|---|
| **scGPT** | scRNA-seq 基础模型 | 预训练于3300万+细胞 | [链接](https://doi.org/10.1038/s41592-024-02201-0) | yes | ok | 3 | 14 | 生成式预训练Transformer单细胞基础模型，用于细胞与基因表征及下游任务迁移。 |
| **Geneformer** | scRNA-seq 基础模型 | V2-316M，约316M参数 |  | yes | n/a | 2 | 10 | 作为被评估/被解释的单细胞基础模型，用于注意力可解释性、SAE图谱与电路映射研究。 |
| **scFoundation** | 单细胞基础模型 | 大规模单细胞预训练模型 | [链接](https://github.com/biomap-research/scFoundation) | yes | ok | 2 | 5 | 被基准测试用于扰动后RNA-seq预测的Transformer基础模型。 |
| **GEARS** | 单细胞转录组扰动 | 图神经网络模型 |  | unknown | n/a | 2 | 3 | 作为可迁移嵌入基线，被Chreode改进Norman Perturb-seq预测。 |
| **TranscriptFormer** | 单细胞转录组基础模型 | 1.12亿细胞、12物种、15.3亿年进化 |  | unknown | n/a | 2 | 3 | 生成式跨物种单细胞基础模型，充当可查询虚拟细胞图谱，跨模态RNA到蛋白预测领先。 |
| **Chreode** | 细胞时序动态/扰动 | 240万细胞小鼠胚胎图谱预训练 | [链接](https://arxiv.org/abs/2605.28111v1) | yes | ok | 2 | 2 | 一步式细胞世界模型，预测动作条件下的细胞状态转移。 |
| **DISCO** | AI-ECG嵌入表型匹配 | HFrEF真实世界队列（规模未明确） | [链接](https://www.immunesinglecell.org) | yes | ok | 2 | 2 | 将ECG分解为嵌入进行高维表型匹配，模拟RCT治疗效应。 |
| **UCE (Universal Cell Embeddings)** | 单细胞转录组 | 3600万细胞预训练 |  | unknown | n/a | 2 | 2 | 自监督细胞嵌入基础模型，可将新细胞无需微调映射到统一潜空间。 |
| **RegFormer** | scRNA-seq 基础模型 | 2500万人类细胞预训练 |  | unknown | n/a | 2 | 1 | 融合基因调控网络先验与 Mamba 架构，用于细胞注释、GRN 重建与扰动预测。 |
| **SCALE** | 扰动单细胞转录组 | CRISPR/化学/发育/免疫 | [链接](https://arxiv.org/abs/2603.17380v3) | yes | ok | 2 | 1 | 条件传输模型，用于虚拟细胞扰动预测与群体结构恢复。 |
| **SCORE2** | 临床风险评分 | 欧洲10年CVD风险模型 | [链接](https://doi.org/10.1093/eurheartj/ehab309) | yes | blocked | 1 | 5 | 欧洲人群10年心血管疾病风险预测算法，被代谢组研究用作基线模型。 |
| **China-PAR** | 临床风险因素 | 推导21320人，验证84961人 | [链接](https://doi.org/10.1161/CIRCULATIONAHA.116.022367) | yes | blocked | 1 | 4 | 用于验证东亚CAD多基因风险评分及作为中国CVD风险预测对照模型。 |
| **CHARGE-AF** | 临床风险因素 | 房颤风险预测 | [链接](https://www.chargeconsortium.com/) | yes | ok | 1 | 3 | 房颤风险预测临床模型，被用于与AI-ECG和蛋白组评分比较。 |
| **PREVENT** | 临床风险评分 | 美国AHA 10年CVD风险方程 | [链接](https://doi.org/10.1161/CIRCULATIONAHA.123.067626) | yes | blocked | 1 | 3 | 作为基线临床CVD风险评分与蛋白组学评分比较。 |
| **QRISK3** | 临床风险因素 | QResearch 1998-2015队列 | [链接](https://qrisk.org/) | yes | ok | 1 | 3 | 英国人群10年心血管疾病风险预测算法，被用于外部验证和蛋白组增量比较。 |
| **Qwen3-4B** | 文本大语言模型 | 4B参数 | [链接](https://huggingface.co/Qwen/Qwen3-4B) | yes | dead | 1 | 3 | 用于RLVR信用分配与GEAR优势重加权实验的基础模型。 |
| **SCimilarity** | scRNA-seq 细胞表示基础模型 | 2270 万细胞，399 项研究 |  | unknown | n/a | 1 | 3 | 度量学习基础模型，用于细胞类型注释与跨数千万 profile 的细胞状态查询。 |
| **SCORE2-Diabetes** | 临床风险因素 | T2D专用CVD风险模型 | [链接](https://doi.org/10.1093/eurheartj/ehad260) | yes | blocked | 1 | 3 | 2型糖尿病患者心血管风险预测模型，被代谢组研究用于增量改进。 |
| **Tahoe-X1** | 单细胞转录组 | 最高30亿参数 | 公开预训练权重、训练代码和评估流程 | yes | n/a | 1 | 3 | 扰动训练的单细胞基础模型，在多项癌症任务达SOTA，并被跨模态继续预训练。 |
| **CellPLM** | scRNA-seq 基础模型 | 预训练模型 |  | unknown | n/a | 1 | 2 | 在 scEval 基准中被评估，表现最佳的基础模型之一。 |
| **Horvath DNAm Age Clock** | DNA甲基化 | 353 CpG |  | unknown | n/a | 1 | 2 | 跨组织DNA甲基化年龄预测器，用于评估生物年龄。 |
| **Longevity-LLM** | DNA甲基化/蛋白组/临床/RNA | 0.6B-9B参数，5个模型 | [链接](https://doi.org/10.1016/j.cell.2026.08.026) | yes | ok | 1 | 2 | 在多种衰老组学数据上微调的基础模型，用于Longevity Bench推理与表观年龄预测。 |
| **Qwen2.5-Math-7B** | 数学推理语言模型 | 70亿参数 | [链接](https://huggingface.co/Qwen/Qwen2.5-Math-7B) | yes | dead | 1 | 2 | 作为PURE与ScalePRM的基座模型进行推理强化学习。 |
| **Qwen3-1.7B** | 文本大语言模型 | 1.7B参数 | [链接](https://huggingface.co/Qwen/Qwen3-1.7B) | yes | dead | 1 | 2 | 用于评估TEMPO与P2T信用分配方法的基座模型。 |
| **Qwen3-8B** | 文本大语言模型 | 8B参数 |  | yes | n/a | 1 | 2 | 用于RLVR信用分配与GEAR优势重加权实验的基础模型。 |
| **Reti-CVD** | 视网膜眼底图像 | UK Biobank 44,677人验证 |  | unknown | n/a | 1 | 2 | 基于视网膜图像的深度学习心血管疾病生物标志物评分，用于卒中、心梗、房颤、心衰风险分层及他汀疗效评估。 |
| **ADVANCE** | 临床风险因素 | T2D CVD风险模型 | [链接](https://doi.org/10.1016/S0140-6736(07)61014-9) | yes | ok | 1 | 1 | 作为中国T2DM患者CVD风险预测的对比模型。 |
| **data2vec** | 多模态自监督表征 | 通用自监督模型 | [链接](https://github.com/facebookresearch/fairseq/tree/main/examples/data2vec) | yes | ok | 1 | 1 | 作为Audio-JEPA的对比基线，比较音频表征学习性能。 |
| **DI-NOv2** | 图像自监督特征模型 | ViT骨干自蒸馏模型 | [链接](https://github.com/facebookresearch/dinov2) | yes | ok | 1 | 1 | 提取PDO视频帧特征，配合注意力机制预测ATP活力与药效。 |
| **DINO** | 视觉表征（图像） | ViT-Base线性评估80.1% | [链接](https://github.com/facebookresearch/dino) | yes | ok | 1 | 1 | 无标签自蒸馏自监督方法，赋予ViT显式语义分割特性。 |
| **Flow-JEPA** | 像素级环境轨迹 | 四个环境 | [链接](https://arxiv.org/abs/2608.29029) | yes | ok | 1 | 1 | 用条件流匹配生成未来潜状态序列的JEPA世界模型。 |
| **Framingham Risk Score (FRS)** | 临床风险评分 | 10年CVD风险 | [链接](https://www.framinghamheartstudy.org/) | yes | ok | 1 | 1 | 作为传统临床CVD风险评分与蛋白组学评分比较。 |
| **GenePT** | 基因/细胞嵌入 | GPT-3.5嵌入，无需预训练 | [链接](https://doi.org/10.1101/2023.10.16.562533) | yes | ok | 1 | 1 | 用GPT-3.5基于NCBI基因文本描述生成基因与单细胞嵌入的基础模型。 |
| **GET** | 基因表达Transformer | 大规模单细胞预训练 | [链接](https://github.com/GET-Foundation/get_model) | yes | ok | 1 | 1 | 作为代表性虚拟细胞基础模型被综述比较。 |
| **Graph-JEPA** | 图数据 | 图级表征 | [链接](https://github.com/geriskenderi/graph-jepa) | yes | ok | 1 | 1 | 用于图级表征学习的联合嵌入预测架构模型，支持图分类与回归。 |
| **GraphCL** | 图数据 | 未明确 | [链接](https://arxiv.org/abs/2010.13902) | yes | ok | 1 | 1 | 图对比学习框架，用于无监督图表征学习。 |
| **HuBERT** | 语音表征 | 最大1B参数 | [链接](https://github.com/facebookresearch/fairseq/tree/main/examples/hubert) | yes | ok | 1 | 1 | 提出并发布的语音自监督预训练模型，用于掩码隐藏单元预测学习语音表征。 |
| **I-JEPA** | 视觉表征（图像） | ViT-Huge/14，16张A100训练<72h | [链接](https://github.com/facebookresearch/ijepa) | yes | ok | 1 | 1 | 联合嵌入预测架构，从上下文块预测目标块表征，无需手工数据增强。 |
| **Intuitor** | 数学推理与代码生成 | 基于GRPO的无监督RL方法 | [链接](https://github.com/sunblaze-ucb/Intuitor) | yes | ok | 1 | 1 | 用模型自身置信度作为唯一奖励信号的无监督强化学习方法。 |
| **JEPA-DNA** | 基因组DNA序列 | 多物种基因组基础模型 | [链接](https://github.com/NVIDIA-Digital-Bio/JEPA-DNA) | yes | ok | 1 | 1 | 将JEPA融入基因组基础模型，在17项基因组基准上提升线性探测与零样本性能。 |
| **LaMamba-Diff** | 图像生成（扩散） | ImageNet 256/512，线性复杂度 | [链接](https://github.com/) | yes | ok | 1 | 1 | 融合局部注意力与Mamba的线性时间高保真扩散生成模型。 |
| **MAE** | 视觉表征（图像） | ViT-Huge，ImageNet-1K达87.8% | [链接](https://github.com/facebookresearch/mae) | yes | ok | 1 | 1 | 掩码自编码器，通过重建缺失图像块实现可扩展视觉自监督预训练。 |
| **MoCo** | 视觉表征（图像） | ResNet-50骨干，ImageNet预训练 | [链接](https://github.com/facebookresearch/moco) | yes | ok | 1 | 1 | 提出动量对比学习框架，构建动态字典进行无监督视觉表征学习。 |
| **OmiCLIP** | 组织病理图像+空间转录组 | 基于220万配对patch训练 | [链接](https://doi.org/10.1038/s41592-025-02707-1) | yes | ok | 1 | 1 | 转录组-图像双编码器基础模型，用CLIP对比学习对齐图像与基因句子表示。 |
| **Plan2Explore** | 高维图像控制 | 未明确 | [链接](https://arxiv.org/abs/2005.05960) | yes | ok | 1 | 1 | 通过规划主动探索的自监督世界模型智能体。 |
| **Point-Delta-JEPA** | 点云观测 | 未明确 | [链接](https://arxiv.org/abs/2608.29434) | yes | ok | 1 | 1 | 在几何移动最多时表现最强的点云JEPA世界模型。 |
| **Point-JEPA** | 三维点云 | 点云块嵌入 | [链接](https://github.com/Ayumu-J-S/Point-JEPA) | yes | ok | 1 | 1 | 面向点云的联合嵌入预测架构模型，用于自监督点云表征学习。 |
| **Point-LeWM** | 点云观测 | 未明确 | [链接](https://arxiv.org/abs/2608.29434) | yes | ok | 1 | 1 | 点云观测下的JEPA世界模型设计，与图像基线统计等价。 |
| **SAM (Segment Anything Model)** | 图像分割基础模型 | 十亿级掩码预训练 | [链接](https://github.com/facebookresearch/segment-anything) | yes | ok | 1 | 1 | 用于PDO延时显微视频中类器官的分割。 |
| **SANA-WM** | 视频生成/世界模型 | 2.6B参数 | [链接](https://doi.org/10.48550/arXiv.2605.15178) | yes | ok | 1 | 1 | 开源世界模型，支持一分钟720p视频生成与精确相机控制。 |
| **scBalFlow** | 药物扰动预测 | SciPlex3/McFarland基准 | [链接](https://github.com) | yes | ok | 1 | 1 | 两阶段流匹配框架解决药物扰动类别不平衡。 |
| **scDEFT** | 单细胞药物响应 | 116万细胞 | [链接](https://arxiv.org/abs/2609.10831) | yes | ok | 1 | 1 | 深度学习框架，用于药物效应预测与反事实推理。 |
| **scGen** | 单细胞转录组 | 未明确（VAE潜空间扰动向量） | [链接](https://doi.org/10.1038/s41592-019-0494-8) | yes | ok | 1 | 1 | 用变分自编码器在潜空间学习扰动向量，预测单细胞扰动响应。 |
| **scKITE** | 单细胞转录组 | 179,067预训练样本 | [链接](https://arxiv.org/abs/2609.14970) | yes | ok | 1 | 1 | 知识增强单细胞基础模型，融合细胞注释与基因调控监督。 |
| **wav2vec 2.0** | 音频自监督表征 | 预训练语音模型 | [链接](https://github.com/facebookresearch/fairseq/tree/main/examples/wav2vec) | yes | ok | 1 | 1 | 作为Audio-JEPA的对比基线，比较音频表征学习性能。 |

## 基准（26）

| 名称 | 模态 | 规模 | 获取 | 开放 | 核验 | 方向 | 证据 | 用途 |
|---|---|---|---|---|---|---|---|---|
| **MMLU** | 多学科知识问答 | 57学科多选题基准 | [链接](https://github.com/hendrycks/test) | yes | ok | 2 | 2 | 用于评估DLLM-JEPA在多学科知识任务上的性能。 |
| **scArchon** | 单细胞扰动scRNA-seq | 9种工具，多样本扰动数据 | [链接](https://doi.org/10.1186/s13059-026-04104-z) | yes | ok | 2 | 1 | 标准化数据集与指标，容器化运行并排名单细胞扰动预测模型。 |
| **VCBench** | 单细胞基础模型多维评测 | 5个基础模型、5个可测维度 |  | unknown | n/a | 2 | 1 | 将四个虚拟细胞框架综合为七个能力维度的多维基准，评测单细胞基础模型。 |
| **ALFWorld** | 文本交互式具身任务 | 6类任务、数千回合 | [链接](https://alfworld.github.io/) | yes | ok | 1 | 4 | 用于评估MetaSkill-Evolve智能体技能自进化框架的基准之一。 |
| **ProcessBench** | 推理过程错误检测 | 3400条推理路径 | [链接](https://huggingface.co/datasets/Qwen/ProcessBench) | yes | dead | 1 | 2 | 用于评测BiPRM与ScalePRM的步级错误检测能力。 |
| **scIB** | scRNA/scATAC整合 | 13任务，最多100万细胞 |  | unknown | n/a | 1 | 2 | 单细胞数据整合基准，用于评估批次去除与生物变异保留。 |
| **WebShop** | 网页购物交互轨迹 | 约120万商品 | [链接](https://webshop-pnlp.github.io/) | yes | ok | 1 | 2 | 用于评估SELAUR智能体在网页购物任务上的成功率。 |
| **AI4AI-Bench** | 算法设计任务 | 10仓库×29配置×6系统×10任务 | [链接](https://arxiv.org/abs/2608.20318) | yes | ok | 1 | 1 | 评测LLM智能体改写训练算法的递归自我改进基准，含公开任务套件与评估器。 |
| **ASSAYBENCH** | CRISPR筛选表型 | 1920个筛选，约13826基因/筛选 | [链接](https://github.com/Genentech/AssayBench) | yes | ok | 1 | 1 | 基于公开CRISPR筛选的表型预测基准，用于评估LLM与智能体的虚拟细胞能力。 |
| **BIRD** | text-to-SQL 数据 | 大规模跨域text-to-SQL基准 | [链接](https://bird-bench.github.io/) | yes | ok | 1 | 1 | 用于评估记忆型自改进智能体的执行准确率与奖励膨胀问题。 |
| **GenoTEX** | 基因表达数据与代码 | 含专家标注代码与结果 | [链接](https://github.com/Liu-Hy/GenoTEX) | yes | ok | 1 | 1 | 评估LLM智能体自动化基因表达数据分析流程的基准。 |
| **GSM-HARD** | 数学应用题 | 未明确 | [链接](https://github.com/openai/grade-school-math) | yes | ok | 1 | 1 | 用于评估分布外数学推理泛化能力。 |
| **LongevityBench** | 多域衰老生物学数据 | 17项任务/5个数据域 | [链接](https://doi.org/10.1016/j.cell.2026.08.026) | yes | ok | 1 | 1 | 用于评估AI系统理解衰老生物学异构数据能力的公开基准。 |
| **MedMCQA** | 医学多选题问答 | 未明确 | [链接](https://medmcqa.github.io/) | yes | ok | 1 | 1 | 用于评估分布外医学推理泛化能力。 |
| **MedQA** | 医学问答 | 未明确 | [链接](https://github.com/jind11/MedQA) | yes | ok | 1 | 1 | 用于评估医学推理能力的分布内基准。 |
| **NKIBench** | AI加速器内核代码 | 来自真实LLM工作负载的Trainium内核 | [链接](https://github.com/zhang677/AccelOpt) | yes | ok | 1 | 1 | 用于评测LLM智能体自主优化AWS Trainium内核的性能。 |
| **PASCAL VOC** | 图像检测/分割 | 约1.1万图像，20类 | [链接](http://host.robots.ox.ac.uk/pascal/VOC/) | yes | ok | 1 | 1 | 用于评估MoCo无监督预训练在检测与分割任务上的迁移性能。 |
| **ProteinGym** | 蛋白质适应度数据 | 217个DMS assay | [链接](https://proteingym.org/) | yes | ok | 1 | 1 | 用于评估蛋白质适应度零样本预测，Delta V在此取得领先。 |
| **PushT** | 机器人操作轨迹 | 推T形块操作任务 | [链接](https://github.com/huggingface/gym-pusht) | yes | ok | 1 | 1 | 用于评估D-JEPA在机器人操作任务上的动作选择成功率。 |
| **R-Judge** | 多轮智能体交互文本 | 569条交互记录，27类风险场景 | [链接](https://github.com/Lordog/R-Judge) | yes | ok | 1 | 1 | 用于评测LLM智能体在交互环境中的安全风险意识。 |
| **RoboTwin** | 机器人操作轨迹 | 双臂机器人操作基准 | [链接](https://robotwin-platform.github.io/) | yes | ok | 1 | 1 | 用于评估D-JEPA在机器人操作任务上的决策对齐性能。 |
| **SKILLMISEVO-BENCH** | 智能体技能安全评测 | 冻结基准，含恶意/良性/延续任务 | [链接](https://github.com/henrymao2004/misevolve) | yes | ok | 1 | 1 | 冻结基准，用于评估技能误演化导致的不安全行为。 |
| **SKILLMISEVO-GYM** | 智能体技能演化任务 | 25种配置，各525任务、25回合 | [链接](https://github.com/henrymao2004/misevolve) | yes | ok | 1 | 1 | 生命周期感知测试台，用于研究自改进智能体的技能误演化。 |
| **Socratic-PRMBench** | 推理过程错误检测 | 2995条缺陷路径 | [链接](https://github.com/Xiang-Li-oss/Socratic-PRMBench) | yes | ok | 1 | 1 | 用于系统评测PRM在六种推理模式下的过程错误检测能力。 |
| **StreamBench** | 文本反馈流 | 在线学习环境，多任务序列 | [链接](https://github.com/stream-bench/stream-bench) | yes | ok | 1 | 1 | 评估LLM智能体在连续反馈流中持续改进能力的基准。 |
| **TruthInsightBench** | 开放式科学发现盲任务 | 40任务/10领域/40篇研究 | [链接](https://github.com/TruthInsight-stack/TruthInsightBench) | yes | ok | 1 | 1 | 证据锚定的开放式科学发现智能体自动评测基准，含29个评分项。 |

## 数据库（14）

| 名称 | 模态 | 规模 | 获取 | 开放 | 核验 | 方向 | 证据 | 用途 |
|---|---|---|---|---|---|---|---|---|
| **MEDICINE** | 代谢组生物年龄模型与结果 | UKBB 274,247人/107代谢物 | MEDICINE门户 | yes | n/a | 2 | 1 | 公开多器官代谢组生物年龄MetBAG的预训练模型与分析结果。 |
| **ARCHS4** | 人类RNA-seq转录组 | 约5.7万样本，28组织，1-114岁 | [链接](https://maayanlab.cloud/archs4/) | yes | ok | 1 | 2 | 作为大规模人类RNA-seq数据源，用于训练和验证转录组衰老时钟。 |
| **Human Cell Atlas** | 多组学细胞图谱 | 全球细胞图谱计划 | HCA门户 | yes | n/a | 1 | 2 | 细胞图谱数据资源，支撑统一基础模型与细胞搜索。 |
| **Allen Brain Atlas** | 空间转录组/脑图谱 | 全脑空间转录组图谱 | [链接](https://portal.brain-map.org/) | yes | ok | 1 | 1 | 用于参数化细胞行为规则语法，构建脑发育相关的虚拟细胞模型。 |
| **ChIP-Atlas** | ChIP-seq/转录因子结合 | 大规模TF结合图谱 | [链接](https://chip-atlas.org) | yes | ok | 1 | 1 | 作为TF-mRNA调控先验用于TF活性推断与扰动预测。 |
| **CollecTRI** | 转录因子调控网络 | 多物种TF-靶基因网络 | [链接](https://github.com/saezlab/CollecTRI) | yes | ok | 1 | 1 | 提供TF调控先验用于学习带符号调控系数。 |
| **CZ CELLxGENE Discover** | 单细胞转录组 | 超7000万细胞 | [链接](https://cellxgene.cziscience.com/) | yes | ok | 1 | 1 | 用于训练scAgeClock单细胞转录组人类衰老时钟模型。 |
| **EMBL-EBI ArrayExpress** | DNA甲基化等组学数据 | 51项人类干预研究 | [链接](https://www.ebi.ac.uk/biostudies/arrayexpress) | yes | ok | 1 | 1 | 提供表观遗传衰老生物标志物响应性分析所用的公开DNAm数据。 |
| **GeneATLAS** | GWAS汇总统计 | 452,264人，778性状，9,113,133变异 | [链接](http://geneatlas.roslin.ed.ac.uk) | yes | ok | 1 | 1 | UK Biobank遗传关联图谱数据库，供统一查询GWAS结果。 |
| **GEO** | DNA甲基化等组学数据 | 51项人类干预研究 | [链接](https://www.ncbi.nlm.nih.gov/geo/) | yes | ok | 1 | 1 | 提供表观遗传衰老生物标志物响应性分析所用的公开DNAm数据。 |
| **NHGRI-EBI GWAS Catalog** | GWAS关联与汇总统计 | 62.5万关联，>8.5万数据集 | [链接](https://www.ebi.ac.uk/gwas/) | yes | ok | 1 | 1 | 标准化收集人类GWAS关联与汇总统计的公开数据库。 |
| **PGS Catalog** | 多基因评分 | 未明确 | [链接](https://www.pgscatalog.org/) | yes | ok | 1 | 1 | 与GWAS Catalog互链的多基因评分数据库。 |
| **PhysioNet** | 生理信号/心电图 | 多数据集门户 | [链接](https://physionet.org/) | yes | ok | 1 | 1 | 提供ECG等生理信号数据，用于ECG-FM预训练与基准。 |
| **Proteome-Phenome Atlas** | 血浆蛋白组-疾病关联 | 53,026人，2,920蛋白，406+660疾病 | [链接](https://proteome-phenome-atlas.com) | yes | ok | 1 | 1 | 开放获取的血浆蛋白组-疾病-性状关联图谱查询门户。 |

## 工具（6）

| 名称 | 模态 | 规模 | 获取 | 开放 | 核验 | 方向 | 证据 | 用途 |
|---|---|---|---|---|---|---|---|---|
| **Olink** | 血浆蛋白组检测平台 | 1,459-2,920蛋白 | [链接](https://www.olink.com/) | yes | ok | 2 | 4 | 高通量蛋白组学检测平台，用于心血管疾病蛋白标志物研究。 |
| **Cell Painting** | 高内涵细胞成像 | 图像型profiling数据（十年积累） | [链接](https://doi.org/10.1038/s41592-024-02528-8) | yes | ok | 2 | 3 | 2013年提出的显微细胞标记检测协议，用于捕获细胞对扰动的形态响应。 |
| **SomaScan** | 血浆蛋白组检测平台 | 4,877 aptamer | [链接](https://somalogic.com/) | restricted | ok | 2 | 3 | 用于高通量血浆蛋白定量以发现心衰、衰弱及高血压相关蛋白。 |
| **Perturb-FISH** | 空间转录组+CRISPR | MERFISH+gRNA原位解码 |  | unknown | n/a | 2 | 1 | 结合MERFISH与gRNA原位扩增，实现扰动与转录组的空间联合读取。 |
| **GRPO** | 强化学习优化算法 | 未明确 |  | unknown | n/a | 1 | 3 | Group Relative Policy Optimization，用于LLM推理与智能体RL训练。 |
| **CellProfiler** | 显微图像特征提取 | 图像分析软件 |  | yes | n/a | 1 | 2 | 提取传统手工图像特征并与深度学习特征比较。 |

## 单篇提及（364，未进主表）

- 数据集：23andMe、23andMe BMI GWAS、ADE20K、ADVANCE Trial、AIDA v2、Age, Gene/Environment Susceptibility-Reykjavik Study (AGES)、Asian Indian Diabetes Heart Study / Sikh Diabetes Study (AIDHS/SDS)、AudioSet-20K、CHARGE-AF Consortium、CHOP、COCO-Stuff、CODE (Brazilian ECG Dataset, 2.3M ECGs)、ChinaHEART、Cityscapes、Copenhagen General Population Study、DFTJ、Danish National Patient Registry、Droid、ELAN、EPIC-Norfolk、ESC-50、Estonian Biobank、FINRISK、FSD50K、Fenland、Framingham Offspring Study、GDSC、GIANT Consortium BMI GWAS、GSE67752、GSM-Plus、Geisinger ECG Cohort、Generation Scotland、HEEDB、HM3D v0.2、I-SPY2、INSPIRE-T、ImageNet ILSVRC-2012、Integrated Mega-scale Atlas、Israel 10K Project、JUMP-MOA、JUMP-lite、Jiangsu Behavioral and Physical Chronic Disease Cohort (JBPCD)、KORA、Lorenz attractor、Lothian Birth Cohort 1936、MERFISH whole mouse brain atlas、MGB (Mass General Brigham) ECG Cohort、MGB Biobank、MIMIC、MIMIC-III、MIMIC-IV-ECG、Mexico City Prospective Study (MCPS)、NHANES、NLST、NPBBD-Korea、Norman K562 CRISPRa、Norman Perturb-seq、Norman19、Nurses' Health Study、Olink Proteomics Panel (UK Biobank)、PRECISE、Perturb-seq genome-scale screen、PerturbReason、Robomimic、Rotterdam Study、SCIPRM70K、SEA-AD、SHIP-START、SHIP-TREND、ST-bank、Sentinel-1、Sentinel-2、SpatialCorpus-110M、Tabula Sapiens、Taiwan Precision Medicine Initiative (TPMI)、Tox21、TruDiagnostic、UCLA Biobank、UHN-ECG、UK Biobank ECG Interval Reference Dataset
- 模型：AI-HF、AIRE、ALADYNOULLI、AROMA、ASCVD-IRT、ASCVD-PCE、ATM (Age-dependent Topic Model)、AdaptAge、AlphaEarth、AlphaFold3、Audio-MAE、BEHRT、BYOL、Bootleg、BrainBeacon、CAME、CARDIAC-FM、CLM-X、CMAE、CPA、CTBA、CTransPath、Cell-o1、CellFM、CellFlux、CellFluxRL、CellOT、CellWorld、China-AIHeart、Co-Scientist、CrossJEPA、D-SPIN、D2R2、DINO-WM、DINOv2、DNAm PhenoAge、DNAmEMRAge、DamAge、DeepSeek-R1、DeepSeek-R1-Zero、DeepSeekMath 7B、Delphi-2M、Delta V、DiRL、ECG-AI、ECG-FM、ECG-LFM、ECG2CAD、EHR-MPC、EMRAge、Echo2HF、Extracellular Matrix Aging Clock、Foresight、Foresight-England、GLAM、GLAM NAV、GOLD BioAge、GPS Mult、GRASP、GenReasoner、GeneCompass、GenoAgent、HEP-JEPA、Hannum DNAm Age Clock、Healthspan Proteomic Score (HPS)、Horvath clock、JEPA-Anything、Kimi k1.5、LeJEPA、LeVJEPA、LinAge2、Longitudinal Proteomic Aging Index (LPAI)、LucaCell、MC-JEPA、MILTON、ML-CVD-C、MSGene、MSKAge、Med-BERT、Med-R1
- 基准：ABC-Bench、AdaJEPA、BLADE、Baba in Wonderland、BioDataLab、BioKGBench、BiomniBench-DA、CellPuzzles、ComputAgeBench、D4RL、DiscoverPhysics、Gaia2、HLE、HumanEval、LMR-BENCH、LOGIQA、LiveCodeBench、Longevity Bench、MMLU-Medical、MedPRMBench、MemCalib、OfficeQA、PARADIGM-HF、PertEval-scFM、PerturBench、RSIBench-Data、SEAGym、SWE Bench Verified、SciIntegrity-Bench、ScienceAgentBench、SealQA、SoundnessBench、Terminal-Bench 2.0、ToolMaker Benchmark、VTAB、Virtual Cell Challenge、Virtual Cell Challenge 2026、X-ARES、scEval
- 数据库：CMAP、CPRD、CPRD Aurum、Cell Landscape、ENCODE、Immunosenescence Inventory、MEDICINE portal、STP、TCGA、TEAPEE
- 工具：AusCVDRisk、AutoPrognosis、BASIL、BAVAR、BOLT-LMM、BioLLM、Biolearn、CINEMA-OT、CODRP、CROP-seq、CellDuality、CellPaint-POSH、CellScientist、ClockBase Agent、DALE、DeGAs、FaithRL、GATK、GEPA、Habitat、Hail、Harmony、ICD-8 to ICD-10 Mapping、K-Dense、LUCID、LWD-Miniscope、LivAge、Loki、Longevity Claw、MatClaw、Mortara VERITAS Algorithm、Mosaic、Nahual、OSCAR、Olink Explore 3072、Olink Proteomics、P2T、PHESANT、PRS-CS、PheMIME、PheWeb、Phecodes、REGENIE、SAFEEVOLVE、SAIGE-GENE、SCOPE (Systematic Classification of Organoids for Phenotypic Evaluation)、SCanSNP、SO-GRPO、SO-PPO、SORL、SPAC-seq、SenePy、SomaLogic、SpatialQM、TARDIS、TEMPO、TFActProfiler、The AI Scientist、Tool-GRPO、TotalSegmentator、TranslAGE、TreeRL、Trellis、UKB-MDRMF、associationSubgraphs、copairs、leakcheck、moscot、scContam、ukbnmr
