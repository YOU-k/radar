# 单细胞与空间组学基础模型与虚拟细胞 · 方向背景报告

证据 91 篇 · 覆盖度 0.65 · 第 7 轮 · 更新 2026-10-04 · 数字核验删句 2

## 本次变更

- 新增 [58] NexuST: A Hierarchical Foundation Model for Spatial Transcriptomics
- 新增 [8] LucaCell: a sequence-centric foundation model for cross-species single-cell analysis
- 新增 [29] EpiZoo: a DNA sequence-aware foundation model for cross-species single-cell epigenomics
- 新增 [34] Deep learning perturbation models can outperform baselines on calibrated metrics.

## 摘要（TL;DR）

- 单细胞基础模型的核心思路是把细胞类比为“句子”、基因类比为“词元”，用 Transformer 等架构在大规模单细胞组学数据上自监督预训练，再适配细胞类型注释等下游任务 [1]。
- 早期代表性工作沿两条路径展开：scGPT 在超 3300 万个细胞的单细胞 RNA 测序数据上预训练 [2]，Geneformer 则在约 3000 万个单细胞转录组上预训练 [3]。
- 随后工作沿数据规模与物种范围扩张：CellFM 预训练于 1 亿人类细胞 [4]，scPRINT-2 扩展到 3.5 亿细胞、16 个物种 [5]，TranscriptFormer 在多达 1.12 亿细胞、12 个物种、跨越 15.3 亿年进化的数据上训练 [6]。
- 架构层面出现引入生物学先验或替换注意力机制的路线：RegFormer 融合基因调控网络先验与 Mamba 状态空间建模，在 2500 万人类细胞上学习表达动态与调控层级 [7]；LucaCell 以序列为中心，在 8500 万人类和小鼠单细胞上预训练 [8]。
- 并非所有工作都依赖大规模表达数据预训练：GenePT 用 GPT-3.5 基于 NCBI 基因文本描述生成基因嵌入，无需数据策展与额外预训练，在基因属性与细胞类型分类等下游任务上达到与 Geneformer 等相当甚至更优的性能 [9]。
- 对基础模型实际效用的评估出现明显分歧：一项零样本评估发现 Geneformer 和 scGPT 在 AvgBIO 上多低于 HVG、Harmony、scVI 等更简单的基线 [10]；另一项工作用 2220 万细胞语料预训练 400 个模型并开展 6400 次实验，未观察到明确的数据缩放定律 [11]。
- 表征提取方式本身受到质疑：一项逐层评估发现轨迹最优层在 60% 深度，比最终层高 31%，扰动最优层随 T 细胞激活状态在 0–96% 间变化，直接挑战了当前基准普遍默认使用最终层嵌入的做法 [12]。
- 空间转录组基础模型的预训练目标正在从「重建观测基因」转向「预测潜在细胞表征」：CellWorld 将预测目标改为潜在细胞表征，CellWorld-Small（5.74M）在全部 11 个线性探针和 7 个空间基准上超越所有基线 [13]。
- 扰动响应预测正从静态的对照—处理映射转向对未见扰动、未见细胞背景的泛化建模：Tahoe-x1 将扰动训练的单细胞基础模型扩展到最高 30 亿参数，在四项基准上均达 SOTA，计算效率较先前细胞状态模型提升 3–30 倍 [14]。
- 领域层面的共识与争议集中在评估标准上：可信虚拟细胞路线图批评当前工作偏重模型规模与数据量，主张评估应超越留出重建精度，转向泛化到未见细胞类型与扰动等生物学标准 [15]。

## 1 背景与定义

单细胞与空间组学基础模型与虚拟细胞的边界，可以从三个层次界定。**最窄的一层是"细胞级基础模型"**：把细胞类比为句子、基因类比为词元，用 Transformer 等架构在大规模单细胞组学数据上自监督预训练，再适配下游任务 [1]；这一层的代表性工作包括 scGPT [2] 与 Geneformer [3]，其共同前提是"大规模预训练 + 下游微调"能带来可迁移表征。**中间一层是"多模态与空间基础模型"**：把模态从 RNA 扩展到蛋白、染色质、病理图像与空间转录组，如 MultiVI [16]、OmiCLIP [17]、PAST [18]、mSTAR [19] 与 CellWorld [13]，其核心问题从"表征是否可迁移"转为"跨模态对齐是否保留单细胞分辨率与空间结构"。**最宽的一层是"虚拟细胞"**：以这些模型为核心，做扰动响应预测、细胞状态生成与多模态整合，并配套评测基准 [20][21]。三层的边界并不整齐——扰动预测既可由细胞级模型微调完成 [22]，也可由不依赖预训练的生成模型完成 [23]，因此"是否属于本方向"取决于是否以大规模预训练表征或虚拟细胞框架为方法主体，而非任务本身。

演化脉络上，本方向经历了从"数据平台"到"预训练模型"再到"评测与机制审计"的重心迁移。**数据侧**，Perturb-seq 类工作确立了以单细胞转录组读出 CRISPR 扰动的范式 [24][25]，CROP-seq 使池化筛选具备单细胞读出 [26]，基因组规模 Perturb-seq 把扰动数推到数千量级 [27]，Tahoe-100M 则把化学扰动推到超过 1 亿细胞、50 个细胞系与 379 种化合物 [28]。**模型侧**，scGPT 与 Geneformer 之后出现两条扩张路线：一是数据与物种规模扩张，如 CellFM 的 1 亿人类细胞 [4]、scPRINT-2 的 3.5 亿细胞与 16 物种 [5]、TranscriptFormer 的 1.12 亿细胞与 12 物种 [6]；二是架构与先验替换，如 RegFormer 的 GRN 先验加 Mamba [7]、LucaCell 的序列中心嵌入 [8]、EpiZoo 的表观基因组"细胞句子" [29]。**评测侧**，重心从早期整合工具基准 [30] 转向对基础模型本身的系统审计：预训练污染 [31]、简单基线反超 [32][33]、指标校准 [34]、内部机制是否编码因果调控 [35][36]。这一迁移本身说明，**领域已从"能否训出模型"进入"模型到底学到了什么、评测是否可信"的阶段**。

核心问题可归纳为四组张力。**第一组是规模与收益的张力**：CellFM、scPRINT-2 等继续扩大语料 [4][5]，但一项用 2220 万细胞预训练 400 个模型、开展 6400 次实验的工作发现性能在远小于当前语料时即趋于平台，未观察到明确的数据缩放定律 [11]；跨模态继续预训练也提示精心策划的蛋白质组数据可能比单纯扩大规模收益更大 [37]。**第二组是表征与因果的张力**：SAE 图谱显示模型内化了有组织的生物学知识，但仅 3/48（6.2%）转录因子显示调控靶标特异性响应 [36]；因果电路追踪的 CRISPRi 基因级验证方向准确率仅 56.4%，据此认为模型编码共表达而非因果调控 [35]；独立系统评估也发现注意力边分数对扰动预测无增量价值，基因级基线 AUROC 0.81–0.88 优于注意力/相关性边的 0.70 [38]。**第三组是基准与泛化的张力**：scContam 发现 PBMC 3k 与胰腺胰岛图谱分别有 80.4%、77.0% 的细胞指纹 p<0.05，而截断后的 AIDA v2 与 Tahoe-100M 为 0%，零样本成绩可能反映预训练暴露而非泛化 [31]；VCBench 在五个可测维度上发现基线在四维追平或超越所有基础模型 [39]；但任务依赖性同样明显——蛋白表达预测中基础模型更准，数据整合中 scVI 更佳 [40]。**第四组是预测与验证的张力**：可信虚拟细胞路线图主张评估应超越留出重建精度，转向泛化到未见细胞类型与扰动 [15]；肝脏 AIVC 综述则指出尚无经过前瞻验证的肝脏模拟器 [41]；临床前转化综述提出从计算评估到 CRISPR 与类器官实验验证的闭环，同时指出监管接受、数据隐私与可解释性仍是障碍 [42]。

从方法学看，本方向当前最活跃的增量集中在"如何把预训练表征转化为可用算法"与"如何让评测可信"两端。前者包括从 scGPT 内部提取紧凑造血算法 [43]、从冻结 scFM 蒸馏可泛化基因间特征用于 GRN 推断 [44]、用 SAE 特征干预批次与药物响应 [45]；后者包括 scContam 的逐细胞污染审计 [31]、PertEval-scFM 的分布偏移评测 [46]、PerturBench 对模式崩溃与秩指标的讨论 [47]、scArchon 的容器化统一流程 [48]、BioLLM 的接口标准化 [49]、JUMP-lite 的 92.0 GB 压缩子集 [50] 与 ST 的跨站点质量指标库 [51]。**这些工作的共同指向是：虚拟细胞的可信度不取决于模型规模，而取决于数据来源是否可审计、评测指标是否校准、预测是否经湿实验闭环验证** [15][42]。这也解释了为何"没跑赢基线"的证据在本方向不是边缘结果，而是界定方向边界的关键证据 [32][33][39]。

## 2 方法学


### 2.1 单细胞基础模型

单细胞基础模型的核心思路，是把细胞类比为“句子”、基因类比为“词元”，用 Transformer 等架构在大规模单细胞组学数据上自监督预训练，再适配细胞类型注释等下游任务 [1]。早期代表性工作沿两条路径展开：**scGPT** 基于生成式预训练 Transformer，在超 **3300 万个细胞**的单细胞 RNA 测序数据上预训练，经迁移学习后在注释、整合、扰动预测、基因网络推断等任务表现优异 [2]；**Geneformer** 则在约 **3000 万个单细胞转录组**上预训练，以自监督方式学习网络动力学并将网络层级编码进注意力权重，微调后在染色质与网络动力学任务中持续提升准确率，并在有限患者数据下识别出心肌病候选治疗靶点 [3]。两者都强调“大规模预训练 + 下游微调”的范式，但前者侧重生成式多组学任务，后者侧重网络生物学中数据有限的场景。

随后工作沿数据规模与物种范围两个方向扩张。**CellFM** 预训练于 **1 亿人类细胞**，在多种单细胞任务上取得竞争或更优性能，验证了单物种超大规模预训练的潜力，但其局限是仅覆盖人类，数据清洗与批次异质性仍影响泛化 [4]。**scPRINT-2** 进一步扩展到 **3.5 亿细胞、16 个物种**，通过改进预训练任务、tokenization 和损失函数并采用细胞级架构，在表达去噪、细胞嵌入和细胞类型预测上达到 SOTA，并具备表达插补与反事实推理的生成能力 [5]。跨物种方向还有 **TranscriptFormer**，在多达 **1.12 亿细胞、12 个物种、跨越 15.3 亿年进化**的数据上训练，联合建模基因身份与表达水平，在分布内和分布外细胞类型分类上达 SOTA，可零样本识别疾病状态并跨物种转移注释 [6]；**Speciesformer** 则在包含 **1.31 亿细胞**的 SpeciesCorpus 上预训练，目标是学习可迁移的细胞状态与状态转变，并区分保守原理与物种、组织及细胞环境特异变异，但该工作仅提供摘要信息，缺少定量基准结果 [52]。

架构层面的另一条线索是引入生物学先验或替换注意力机制。**RegFormer** 融合基因调控网络先验与 Mamba 状态空间建模，针对 scRNA-seq 高维稀疏和无序特性，通过 GRN 引导的生成式预训练在 **2500 万人类细胞**上学习表达动态与调控层级，在细胞注释、GRN 重建、遗传扰动预测和药物响应建模等基准上持续优于 scGPT 和 Geneformer [7]。**scDifformer** 采用掩码语言模型预训练、扩散驱动后训练和下游微调三阶段设计，在 7 个组织和多项独立研究中提升跨数据集表现，尤其在强批次效应下，并在细胞类型注释、marker 基因与通路恢复、跨组织分化轨迹及空间转录组 spot 去卷积方面表现优异 [53]。**LucaCell** 则以序列为中心，用预训练 mRNA 序列嵌入表示基因而非固定基因注释，将表达离散化为 bin 后用 Transformer 编码器建模，在 **8500 万人类和小鼠单细胞**上预训练，可在人、小鼠和狐猴肾脏数据中实现跨物种、跨模态细胞类型迁移，并实现无比对微生物嵌入，区分 50 多种细菌且保留种内结构 [8]。**EpiZoo** 把这一思路延伸到表观基因组，将百万维单细胞表观基因组谱转换为紧凑的“细胞句子”，整合 DNA 编码的调控信息、序列无关的表观基因组背景以及基于可及性的重要性，以克服现有模型依赖基因组坐标、局限于单一物种的问题 [29]。

并非所有工作都依赖大规模表达数据预训练。**GenePT** 用 GPT-3.5 基于 NCBI 基因文本描述生成基因嵌入，再通过表达加权平均或按表达排序的基因名句子嵌入生成单细胞嵌入，无需数据策展与额外预训练，在基因属性与细胞类型分类等下游任务上达到与 Geneformer 等相当甚至更优的性能，其局限是依赖文献文本质量、未充分利用表达数据本身 [9]。这构成与“越大越好”路线的一种对照：预训练语料并非唯一决定性能的因素。

面向检索与样本级分析，**SCimilarity** 用深度度量学习学习统一可解释的细胞表示，同时优化监督三元组损失和无监督重构损失，使相似细胞靠近。较早版本在 **22.7M 细胞、399 项研究**上训练，实现跨组织细胞类型整合、注释与即时查询，并发现最初在间质性肺病中识别的巨噬细胞亚群也存在于其他纤维化疾病、组织和 3D 水凝胶系统中 [54]；后续版本报告在 **2340 万细胞、412 项研究、56 训练/15 测试数据集**上，在查询敏感性和整合性能间取得最佳平衡（β=0.001），支持跨器官、系统、条件的可扩展细胞搜索，但依赖 Cell Ontology 注释质量，部分细胞类型关系模糊 [55]。**MrVI** 则从另一角度切入，用层次深度生成模型和交叉注意力建模样本协变量效应，无需先验聚类即可识别样本分组，实现高分辨无注释差异表达与丰度分析并控制批次，整合性能领先，已在 scvi-tools 中提供 [56]。

对基础模型实际效用的评估出现了明显分歧。一项零样本评估在 5 个多样单细胞数据集（如 Pancreas 16k、PBMC 12k 等）上比较 Geneformer 和 scGPT 与 HVG、Harmony、scVI 基线，发现两种基础模型在 AvgBIO 上多低于这些更简单的基线，HVG 在所有指标上优于二者，scGPT 仅在 PBMC 12k 部分优于 scVI/Harmony；作者据此强调零样本评估的重要性，并指出预训练与评估数据存在部分重叠 [10]。另一项工作用 **2220 万细胞**语料预训练 **400 个模型**并开展 **6400 次实验**，覆盖零样本与微调任务，发现性能在数据规模远小于当前训练语料时即趋于平台，未观察到明确的数据缩放定律，建议平衡模型容量、数据规模与算力 [11]。这与 CellFM、scPRINT-2 等继续扩大语料的路线形成张力：规模扩张是否持续带来收益，尚无一致结论。

表征提取方式本身也受到质疑。一项逐层评估对 scFoundation（100M 参数）和 Tahoe-X1（1.3B 参数）在轨迹推断与扰动响应预测上系统提取各层嵌入，发现最优层依赖任务与细胞情境：轨迹最优层在 **60% 深度**，比最终层高 **31%**；扰动最优层随 T 细胞激活状态在 **0–96%** 间变化；静息细胞首层反而最佳 [12]。这直接挑战了当前基准普遍默认使用最终层嵌入的做法，也提示模型规模与表征质量之间并非简单对应。该评估仅覆盖两个模型、两类任务，未涵盖更多模型与生物场景 [12]。

除细胞层面的基础模型外，相关证据还涉及更细粒度的分子建模。**PTM-Mamba** 是 PTM 感知的蛋白语言模型，基于双向 Mamba 块并以门控机制融合 ESM-2 与 PTM 嵌入，用 **79,707 条修饰序列**（源自 311,350 条 Swiss-Prot PTM 记录）训练，相比 PTM-Transformer 收敛更快，能区分并相关表示修饰与未修饰序列，其局限是依赖 ESM-2 嵌入、PTM 类型与序列长度覆盖有限 [57]。这类工作与细胞级基础模型在建模对象上不同，但同属为下游生物学任务提供可迁移表征的尝试。

### 2.2 空间与多模态模型

空间转录组基础模型的预训练目标正在从「重建观测基因」转向「预测潜在细胞表征」。CellWorld 指出，既有模型主要重建被掩码的基因身份或表达值，可能鼓励复现测定特异的技术变异、限制表征迁移性，因此将预测目标改为潜在细胞表征，用空间 Transformer 建模细胞交互，以可见上下文加部分表达提示预测被掩码细胞 [13]。该工作在 4600 万人细胞、3 平台 11 器官上预训练 4 个变体（5.74M–94.56M 参数），**CellWorld-Small（5.74M）在全部 11 个线性探针和 7 个空间基准上超越所有基线**；仅用 5% 语料的冻结 Large 模型在 7 个空间基准上超越全部微调基线 [13]。其局限在于空间迁移依赖生物来源多样性与充分优化而非细胞数量，细胞级目标歧义需部分表达提示 [13]。NexuST 走的是另一条分层路线：反复交错基因级分子建模与细胞级空间建模，使两个层级在端到端预训练中相互优化，并构建了含 72 个数据集、11 个器官、三种成像平台、4570 万人类细胞的 HumanST-46M，在四个留出数据集约 260 万细胞上于细胞类型注释、区域预测、基因恢复等任务达到 SOTA 或具竞争力 [58]。

组织学与空间转录组的跨模态对齐方面，OmiCLIP 用双编码器将 H&E 图像与转录组对齐，把转录组数据转为「基因句子」，基于 ST-bank 的 **220 万组织 patch、1007 样本、32 器官**训练，配套 Loki 平台提供组织对齐、注释、细胞分解、检索与基因表达预测五项功能，在 5 个模拟、19 个公开、4 个内部数据集上对比 22 种 SOTA 方法 [17]。PAST 则定位为泛癌单细胞基础模型，在 **2000 万配对病理图像与单细胞转录组**上联合编码细胞形态与基因表达，学习统一跨模态表征，支持单细胞基因表达预测、虚拟分子染色和多模态生存分析，其出发点是既有方法多限于 bulk 或粗区域整合、难捕捉单细胞变异 [18]。mSTAR 进一步把模态扩展到三种——病理切片、专家报告与基因表达，用两阶段预训练（先切片级对比学习训练聚合器，再将全切片上下文注入 patch 特征提取器），基于 26,169 切片-模态对、10,275 患者、32 癌种、1.16 亿 patch，在 15 类 97 项任务中表现优异，并显示多模态预训练可用更少数据达到竞争性能 [19]。三者共同点是依赖配对数据（OmiCLIP 依赖配对 WSI 与 Visium，mSTAR 依赖报告与基因表达配对），跨中心泛化均待验证 [17][19]。

多模态单细胞整合模型侧重缺失模态推断与联合表征。MultiVI 用深度生成模型分别建模基因表达与染色质可及性，通过惩罚使两模态潜空间对齐，并模块化扩展至表面蛋白，可整合单模态数据集，提供校准的不确定性估计，准确估计缺失模态的差异表达/可及性，在相关群体存在时实现样本外预测，已开源并集成于 scvi-tools [16]。CLM-X 采用多路 Transformer 架构与统一 token 化设计、分阶段掩码重建预训练，在百万级单模态与多模态数据上预训练，支持 RNA-only、ATAC-only 和配对 RNA-ATAC 输入，在五个下游任务和 10 个数据集上持续超越现有多模态方法与单模态基础模型，**RNA-ATAC 跨模态翻译和扰动预测优势明显** [59]。moscot 则从最优传输角度切入，将时序、空间、时空映射统一为 W、GW 或 FGW 型 OT 问题并支持多模态与图谱规模数据，在 170 万细胞小鼠胚胎等数据中实现高效对齐，计算时间与内存较既往 OT 工具降数个数量级，并实验验证 NEUROD2 调控 epsilon 细胞形成 [60]。

数据与评测层面，若干工作提供了资源与基准参照。平台评测方面，一项工作用三种人肿瘤连续切片、CODEX 蛋白与 scRNA-seq 作真值，统一比较 Stereo-seq v1.3、Visium HD FFPE、CosMx 6K、Xenium 5K 四个亚细胞分辨率平台，发现各平台在灵敏度、扩散控制、细胞分割等关键指标上差异显著，但结论受限于仅 3 种肿瘤、4 个平台 [61]。病理基础模型临床基准则系统比较 CTransPath、Phikon、UNI、Virchow 等模型的参数量、算法与训练数据，评估下游临床任务性能，指出数字病理数据缺乏与 WSI 计算资源需求高是主要瓶颈 [62]。此外，Cell Painting 作为 2013 年提出的显微细胞标记检测，经协议优化、特征提取改进与批次校正增强，可捕获细胞对扰动的响应，已用于解析化合物作用机制与毒性，未来方向是整合其他高内涵数据类型 [63]。

### 2.3 扰动响应与虚拟细胞

扰动响应预测正从静态的对照—处理映射，转向对未见扰动、未见细胞背景的泛化建模。早期工作确立了以单细胞转录组读出CRISPR扰动的技术范式：Perturb-seq将单细胞RNA-seq与CRISPR混合筛选结合，在约**20万**免疫细胞和细胞系中识别扰动靶点、基因signature、细胞状态与遗传互作[24]；同一方法被用于解剖未折叠蛋白反应，通过两个全基因组CRISPRi筛选鉴定约**100**个命中基因，解耦三条UPR分支并揭示转位子与IRE1α的反馈环[25]。CROP-seq则把gRNA盒插入慢病毒3'LTR使其成为可检测的mRNA，实现池化筛选的单细胞转录组读出，并验证gRNA插入不影响病毒功能、编辑效率与LentiGuide-Puro高度相似[26]。这些平台构成了后续虚拟细胞模型的主要训练数据来源。

在化学扰动方向，PRnet以SMILES与剂量构建扰动嵌入，结合未扰动表达谱生成响应分布，在新化合物、通路和细胞系预测上优于替代方法，并实验验证了小细胞肺癌与结直肠癌候选化合物，构建覆盖**88**细胞系、**52**组织的扰动图谱，为**233**种疾病推荐药物[23]。PerturbNet则强调预测未见化学与遗传扰动下的细胞状态分布而非仅均值，以scGen、CPA、chemCPA、GEARS、Biolord为对照[64]。两者都受限于训练化合物库的覆盖度，对全新化学空间的外推能力有限[23][64]。

利用预训练基础模型做扰动预测成为另一条路径。有工作引入药物条件适配器，仅微调**不到1%**参数以保留预训练生物表征，在所有泛化设置下达SOTA，尤其在新细胞系少样本与零样本泛化上显著优于基线，但其扰动数据集仅覆盖数百分子、少数细胞系[22]。Tahoe-x1将扰动训练的单细胞基础模型扩展到最高**30亿**参数，在含Tahoe-100M扰动图谱的大规模数据上预训练，采用含药物token的掩码表达生成目标，在基因必需性、癌症标志基因、细胞类型分类和留出情境扰动响应预测四项基准上均达SOTA，计算效率较先前细胞状态模型提升**3–30倍**[14]。值得注意的是，一项跨模态研究对Tahoe-x1做继续预训练，在来自**440**项质谱研究的**48,843**个蛋白质组样本上训练**70M**参数模型一个epoch，结果在多数原评测基准上匹配或超过1B和3B参数的RNA-only模型，并提升对held-out蛋白扰动基准的迁移，提示精心策划的蛋白质组数据可能比单纯扩大规模收益更大[37]。

针对基因级模型把同一基因不同位点扰动坍缩为同一表征的问题，STRAND以扰动位点调控DNA序列编码为条件，参数化从对照到扰动状态的条件传输，在K562、Jurkat、RPE1上低样本判别分提升达**33%**，未见基因基准取得最佳平均排名，新细胞系迁移Pearson提升达**0.14**，基因组覆盖从约**1.5%**扩至约**95%**[65]。SCALE则针对对照与处理细胞非配对的问题，将细胞视为无序集合，用集合感知编码器与条件DiT学习潜在传输，无需细胞级匹配，在CRISPR七项指标上全面超越竞争方法并保持基因靶表征分离，其预测的细胞因子差异经三供体PBMC实验验证[66]。AROMA整合文本证据、图拓扑与蛋白序列特征建模扰动—靶依赖，构建**>498k**样本的PerturbReason数据集与两个知识图谱，在多细胞系超越现有方法，未见细胞系零样本与知识稀疏长尾场景下保持稳健，但依赖知识图谱与检索质量[67]。

时序与动力学建模是另一子问题。Chreode提出一步式细胞世界模型，通过结构化残差转移算子预测动作条件下的状态转移，将分布演化从推理时移至训练时，在**240万**细胞小鼠胚胎图谱上预训练；作为GEARS可迁移嵌入，将Norman Perturb-seq的DE20 MSE从**0.2121**降至**0.1858**（相对提升**12.4%**），作为微调初始化在造血和胰岛分化上改善Sinkhorn距离[68]。UNAGI基于VAE-GAN从疾病时间序列单细胞数据解析细胞动力学并进行计算机药物筛选，整合疾病特异基因调控信息与CMAP药物数据库，以Seurat、SCANPY、scVI、scGPT、GEARS等为对照，但其虚拟扰动仍需实验验证[69]。

数据规模与生物学背景的扩展也在推进。一项全基因组扰动测序研究扰动原代人CD4+ T细胞所有表达基因，覆盖**4**名供体、**2200万**细胞，在静息与刺激态测量转录组效应，发现调控因子及其所控基因程序随刺激条件大幅变化，并提名极化与衰老表型调控因子、关联自身免疫病风险，但受限于仅4名供体与体外刺激条件[70]。在可解释建模方向，有工作提出细胞行为假设语法，将自然语言细胞规则一一映射为数学方程以构建agent-based模型，案例涵盖肿瘤生长、侵袭、免疫治疗响应与脑发育，依赖标注细胞状态与规则质量[71]。

领域层面的共识与争议集中在评估标准上。AIVC愿景主张从数据直接学习细胞行为、无需显式规则，提出预测、生成、可查询三大能力，并指出多尺度建模、海量互作组件与非线性动力学仍是挑战[20]。虚拟细胞挑战赛作为开放循环基准，提供评估框架与专用数据集以加速模型开发[21]。可信虚拟细胞路线图则批评当前工作偏重模型规模与数据量，主张评估应超越留出重建精度，转向泛化到未见细胞类型与扰动等生物学标准，并明确数据、设计、基准与实验验证的证据链[15]。临床前转化综述进一步提出从计算评估到CRISPR与类器官实验验证的闭环流程，同时指出监管接受、数据隐私与可解释性仍是障碍[42]。这些框架性主张与前述具体模型在“规模优先还是验证优先”上的分歧，构成了当前虚拟细胞研究的核心张力。

### 2.4 机制可解释性与表征分析

对单细胞基础模型内部机制的系统解析，主要沿两条技术路线展开。其一是以**稀疏自编码器（SAE）**分解稠密激活：在 Geneformer V2-316M 与 scGPT 全人模型各层残差流上训练 TopK SAE，分别生成 **82525 与 24527 个特征**，其中 99.8% 在 SVD 中不可见，29–59% 可注释到通路 [36]；在 scGPT、scFoundation、Geneformer 三个模型隐藏表示上训练的 SAE 同样揭示出多样且复杂的生物与技术信号，且不同训练协议和架构的模型编码方式不同 [45]。其二是因果电路追踪：消融 SAE 特征并测量下游响应，在 Geneformer V2-316M 与 scGPT 上共得到 96,892 条边、80,191 次前向，两模型均表现约 **53% 生物一致性与 65–89% 抑制主导**，且不随架构与细胞类型变化，跨模型共识 1,142 域对（10.6 倍富集）[35]；对 Geneformer 第 5 层全部 4065 个 SAE 特征做穷举追踪则得到 1,393,850 条显著下游边，较选择性采样扩 27 倍，并观察到重尾枢纽分布与随交互阶数单调加深的冗余（三阶冗余比 0.59 对配对 0.74，零协同）[72]。

这些表征是否承载因果调控逻辑，是当前最集中的争议点。SAE 图谱显示模型内化了有组织的生物学知识，但仅 **3/48（6.2%）转录因子**显示调控靶标特异性响应，多组织对照为 10.4% [36]；因果电路追踪的 CRISPRi 基因级验证方向准确率仅 56.4%，据此认为模型编码的是共表达而非因果调控 [35]。独立的系统评估框架（37 项分析、153 个统计检验、四种细胞类型、两种扰动模态）给出方向一致的结论：注意力模式虽编码分层生物结构（早期层蛋白互作、晚期层转录调控），但对扰动预测无增量价值，**基因级基线 AUROC 0.81–0.88 优于注意力/相关性边的 0.70**，成对边分数零增量，消融调控头无退化 [38]。不过该框架也指出注意力—相关性关系依赖背景，且 CSSI 可将 GRN 恢复提升至多 1.85 倍 [38]，说明结构信息并非完全无用。

在提取可用算法方面，已有工作尝试把内部几何转化为独立算子。从 scGPT 中提取的紧凑造血算法在 Tabula Sapiens 564,253 细胞上伪时间深度排序 **|ρ|=0.439**，优于次优的 0.331，CD4/CD8 AUROC 0.867、单核/巨噬 0.951，且比 MLP 探针快 34.5 倍、参数少约 1000 倍 [43]；但该验证主要限于造血系统，其他生物学过程的泛化性有限 [43]。针对 GRN 推断，有研究指出重建式预训练目标未显式捕获潜在调控信号，现有零样本方法有时不及随机预测，遂提出 GRN 泛化基准并用虚拟值扰动与梯度轨迹从冻结 scFM 蒸馏可泛化基因间特征，报告显著优于现有方法 [44]。SAE 特征还被证明可干预：抑制批次特征改善整合并保留生物信号，激活药物特征使对照细胞呈浓度依赖地向药物扰动状态转变 [45]。

### 2.5 形态与图像表型基础模型

图像表型基础模型的核心问题之一，是如何把高维显微图像转成能保留生物学关系的表征。CellPaint-POSH 把 Cell Painting 与 pooled 光学 CRISPR 筛选、自监督深度学习结合，在 **163,090 个单细胞**上学习形态表征，结果显示自监督机器学习特征在预测性能上高于专家形态特征，形态表型可按已知功能聚类基因，并在无通路报告基因的情况下揭示基因关联网络 [73]。但该平台需改造 Cell Painting 以兼容原位测序（如将线粒体染色改为 RNA 探针 Mitoprobe、加入 RNase 抑制剂并提前逆转录），依赖成像与测序流程优化 [73]。与之相对，一项综述给出的对比是 **CLOOME 零样本 MoA top-10 准确率 61.3%**，高于 CellProfiler 的 24.5%，但同时指出部分场景手工特征仍具竞争力，且时序与 3D 数据方法、质控标准及特征解释仍不成熟 [74]。

特征空间本身是否可靠，是另一条独立的方法学线索。有工作在 U2OS JUMP-MOA 参考板的 **90 个化合物**上，以零样本方式对比 CellPaintSSL、OpenPhenom、uniDINO 三种预训练模型，发现活性阳性数量相近（CellPaintSSL 85/90、OpenPhenom 81/90、uniDINO 82/90），但 CellPaintSSL 的活性 mAP 显著高于另两者（p<0.0001），而 MOA 注释恢复只是部分且因模型而异 [75]。这说明模型在前提性质量指标上接近，并不保证目标生物学关系能被同等恢复；该研究也受限于单一 U2OS 参考板，MOA 恢复不完整且模型间不一致 [75]。

## 3 数据与资源

单细胞与空间组学的基础模型依赖大规模、标准化的扰动与图谱数据。在扰动数据方面，**Perturb-seq** 类工作提供了基因型-表型映射的核心资源：一项研究以多重CRISPRi在K562与RPE1细胞系中对超过**250万**人类细胞进行基因组规模筛选，覆盖数千个敲低扰动，并据此研究RNA剪接、分化、染色体不稳定等表型 [27]；另一项工作则基于CRISPR介导的pooled Perturb-seq，从高维单细胞表型构建细胞状态流形，用于遗传互作的无偏排序与分类 [76]。空间维度上，Perturb-FISH将MERFISH与gRNA原位扩增结合，在LPS刺激的巨噬细胞中与匹配的Perturb-seq比较验证敲除效应，并进一步结合钙成像用于ASD风险基因筛选及肿瘤异种移植3D组织验证 [77]。药物扰动方面，**Tahoe-100M** 覆盖超过**1亿**细胞、50个细胞系与379种化合物，采用3D球状体混合细胞系、24小时三剂量处理，覆盖约56,000个细胞系-药物-剂量组合，并报告了Dabrafenib在非BRAF依赖细胞系中的意外敏感性及CDK抑制剂引起的G1或G2/M阻滞 [28]。

图谱类资源为虚拟细胞提供参考坐标系。全小鼠脑MERFISH图谱对约**800万**细胞成像超过1100个基因，整合scRNA-seq后鉴定出超过5000个转录簇与约300个主要细胞类型，并注册到小鼠脑共坐标框架以量化各脑区细胞组成、识别空间模块 [78]。Human Cell Atlas相关工作则从数据收集转向图谱整合，提出细胞图谱作为细胞普查、3D图谱、基因型-表型连接、4D发育图谱及生物学基础模型五种用途 [79]。需注意，上述扰动数据多局限于少数细胞系或特定刺激条件（如CRISPRi为敲低而非敲除、表型限于转录组 [27]），空间图谱则受限于基因面板与物种 [78]，不同队列的规模数字不宜直接横向比较。

## 4 应用与结果

单细胞与空间图谱已能在高分辨率下刻画健康与病变肝脏，包括肝小叶肝细胞分区、纤维化巨噬细胞-星状细胞生态位、胆管细胞反应、免疫重塑及肝细胞癌生态系统，但这些图谱本身并不能预测肝损伤是否会进展，也无法预测肝脏对未经测试的药物、毒物或遗传扰动的响应 [41]。该综述将面向肝脏的 **AI 虚拟细胞（AIVC）** 建模路线归纳为三类互补方向——生成模型、动力学/运输模型与预训练/基础模型，并以扰动响应预测作为跨层评估 [41]。

在证据分层上，现有工作被梳理为直接肝脏验证、含肝脏基准、通用单细胞证据与概念应用四类 [41]。其核心结论是：已发表模型仅展示了图谱整合、轨迹推断、可迁移表示、回顾性响应程序等单个组件，**尚无经过前瞻验证的肝脏模拟器** [41]。因此该综述提出，评估需覆盖供体、病因、分期与平台等维度，以检验模型在不同条件下的稳健性 [41]。

## 5 评测、可复现性与争议

单细胞基础模型的评测正从单一任务排行榜转向对评测本身的方法学审计。**scContam** 对四个 scIB 基准和三个 scFM 做逐细胞预训练污染审计，发现 PBMC 3k 与胰腺胰岛图谱分别有 **80.4%**、**77.0%** 的细胞指纹 p<0.05，而截断后的 AIDA v2 与 Tahoe-100M 为 **0%**；MIA AUROC 随模型容量数据比从 **0.494** 升至 **0.690** 再到 **0.881**，说明零样本成绩可能反映预训练暴露而非泛化，且生产级 scFM 抗实例记忆、分布污染需单独检测 [31]。这直接动摇了以公开仓库数据构建的基准的解释力。

与此并行的是「简单基线反超」的证据群。在扰动后表达预测上，差分空间 **Train Mean** 基线（0.711/0.557/0.373/0.628）优于 **scGPT**（0.641/0.554/0.327/0.596）与 **scFoundation**（0.552/0.459/0.269/0.471），而结合 GO 特征的随机森林最佳（0.739/0.586/0.480/0.648）[32]。另一项工作在 K562 CRISPRa 双扰动数据上比较 scGPT、scFoundation、GEARS、CPA 与线性基线，所有模型误差高于加性基线，遗传互作预测不优于 no change 基线 [33]。**PertEval-scFM** 同样报告零样本 scFM 嵌入未持续优于基线，尤其在分布偏移下 [46]。**VCBench** 把四个虚拟细胞框架综合为七个能力维度，在五个可测维度上预注册线性与最近邻基线，结果基线在四维追平或超越所有基础模型，仅 **TranscriptFormer** 在 RNA 到蛋白预测上以 **53% Pearson** 超过最强基线 [39]。

不过「基础模型无用」并非定论，任务依赖性是最一致的结论。零样本评估 scGPT、SCimilarity、UCE、Transcriptformer 时，细胞类型注释中基线在多数数据集最强，蛋白表达预测中基础模型更准（SCimilarity 误差最低、Transcriptformer 相关性最高），数据整合中基础模型表现中等而 scVI 更佳 [40]。低监督条件下，CellPLM 在聚类、注释与批次校正领先，scMulan 在扰动预测领先，PCA 在表达重建领先；七个基础模型中仅 1 个聚类、3 个批次校正、4 个注释、0 个重建、6 个扰动预测超过最强经典基线 [80]。生物学驱动的评测则发现零样本嵌入确实捕捉生物学信息，但预训练模型在部分场景未超越 HVG、Seurat、Harmony、scVI 等简单基线 [81]。

跨模态统一评测进一步显示没有全能模型。对 Nicheformer、CellPLM、scGPT-spatial、GenePT、scELMo、Novae 的统一基准覆盖 scRNA-seq、空间转录组与 Perturb-seq，发现表达训练的细胞级 Transformer 擅长细胞身份，空间/图模型保留组织结构，语言嵌入在部分扰动指标有竞争力，排名随模态、预处理、token 化、生物先验、域偏移和指标变化 [82]。细胞类型分类上，scFoundation 持续最佳，Geneformer 表现差甚至不如基线 [83]。GRN 重建方面，零样本下 scGPT token 嵌入相似度在 STRING 和 ChIP-seq 上超越经典基线，scFoundation 动态转移表现最强 [84]；但另一项两层可解释性框架在两种架构、四种细胞类型、两种扰动模态下做 153 项统计检验与因果消融，发现注意力边分数相对基因级特征无增量价值，单变量基线更优，TRRUST 头因果消融无行为效应 [85]。

评测指标本身也被证明是争议来源。有研究提出阳性对照基线与指标校准框架，在 14 个数据集、18 个指标上发现 MSE、Pearson Δ 等常用指标校准不良，降低了对阳性模型性能的敏感性，而在良好校准指标下深度学习扰动模型可优于无信息基线 [34]。这与前述「深度模型不如基线」的结论形成直接张力：差异可能部分来自指标选择而非模型能力。**PerturBench** 也指出广泛使用模型存在模式崩溃，秩指标可补充 RMSE，且无单一架构明显占优、简单架构随数据规模扩展良好 [47]。**scArchon** 则以 Snakemake 容器化流程统一 MSE、Wasserstein 及生物指标并聚合排名，解决环境不兼容问题 [48]。

可复现性基础设施是另一条主线。**BioLLM** 通过决策树预处理接口、BioTask 执行器和统一模型加载器，针对预处理不一致、接口异构和评估指标非标准化三大挑战提升可比性 [49]。**JUMP-lite** 把 115 TB 的 JUMP Cell Painting 压缩为 **92.0 GB** 子集（约缩小 **1,250 倍**），配合开源框架 Nahual 对 CellProfiler、MorphEM、OpenPhenom、SubCell、DINOv2 做基准测试，发现中度压缩基本保留信号 [50]。空间组学侧，**ST** 数据集覆盖六种组织类型、跨三站点在 Xenium 与 CosMx 上比较，建立跨站点准确度、精密度、重复性、灵敏度与特异性指标，SpatialQM 开源、STP 门户公开，并构建约 **3300 万**细胞的社区质量指标库 [51]。

无监督评估提供了不依赖标注的替代路径。有框架基于「忠实表征应在模拟技术与采样变异扰动下保持邻域结构」这一原则，对 5 个 scFM、PCA 基线和 39 个数据集测试，发现标准基准判定近乎等价的模型在丢弃 **5%** 计数时局部邻域保持差异近 **2 倍**，且该不稳定性具尺度依赖性并被视觉连贯的嵌入掩盖；重采样聚类稳定性与生物保守指标的 Spearman ρ=**0.78** [86]。这提示下游任务基准可能无法区分可复现结构与单次噪声抽样产物。

数据集层面的评估价值也受到质疑。有研究发现常用小分子活性基准中许多 assay 直接关联细胞健康或毒性，逻辑回归细胞计数 AUC **0.70±0.22** 接近 CLOOME 的 **0.71±0.19**，细胞计数加 MW 与 logP 达 **0.74±0.21**；但在 24 个蛋白靶标基准中 Cell Painting 确实优于细胞计数 [87]。扰动基准方面，有工作指出 Perturb-Seq 数据集扰动特异性方差低、评估价值有限 [32]，另一项 27 种方法、29 个数据集、6 类指标的评测强调细胞上下文嵌入对提升泛化性的必要性 [88]。整合基准的早期工作则提示部分任务真实数据 ground truth 依赖预处理注释，可能引入偏差 [30]。

## 6 空白与趋势

面向虚拟细胞的扰动响应预测，正从「拟合已知扰动」转向「外推到未见扰动与未见细胞背景」，但现有证据显示这条外推路径远未闭合。STRAND 指出基因级模型会把同一基因不同位点的扰动坍缩为同一表征，转而以扰动位点调控 DNA 序列为条件，在 K562、Jurkat、RPE1 上把低样本判别分提升达 **33%**、新细胞系迁移提升达 **0.14**，并把基因组覆盖从约 **1.5%** 扩至约 **95%** [65]；SCALE 则针对对照与处理细胞非配对这一根本困难，用集合感知编码器与条件 DiT 学习潜在传输，在 CRISPR 七项指标上超越竞争方法，其预测的细胞因子差异经三供体 PBMC 实验验证 [66]。**但这类方法仍主要在同一扰动模态、同一读出层（转录组）内验证，跨模态、跨物种的外推尚无系统证据。**

评测侧的证据则对「规模即能力」构成持续压力。scContam 发现 PBMC 3k 与胰腺胰岛图谱分别有 **80.4%**、**77.0%** 的细胞指纹 p<0.05，而截断后的 AIDA v2 与 Tahoe-100M 为 **0%**，MIA AUROC 随模型容量数据比从 **0.494** 升至 **0.881** [31]；**这意味着部分零样本成绩可能反映预训练暴露而非泛化，公开仓库构建的基准解释力被直接动摇。** 与之呼应，差分空间 Train Mean 基线在四个 Perturb-seq 数据集上优于 scGPT 与 scFoundation，结合 GO 特征的随机森林最佳 [32]；K562 CRISPRa 双扰动上所有模型误差高于加性基线，遗传互作预测不优于 no change 基线 [33]；VCBench 在五个可测维度上预注册线性与最近邻基线，基线在四维追平或超越所有基础模型，仅 TranscriptFormer 在 RNA 到蛋白预测上以 **53% Pearson** 超过最强基线 [39]。**不过「基础模型无用」并非定论：任务依赖性是最一致的结论**——细胞类型注释中基线多数最强，蛋白表达预测中基础模型更准，数据整合中 scVI 更佳 [40]；低监督下七个基础模型中仅 1 个聚类、3 个批次校正、4 个注释、0 个重建、6 个扰动预测超过最强经典基线 [80]。指标本身也被证明是争议来源：MSE、Pearson Δ 等常用指标校准不良，而在良好校准指标下深度学习扰动模型可优于无信息基线 [34]。

机制可解释性方向在 2026 年集中爆发，但结论高度收敛于一个否定性判断。SAE 图谱显示模型内化了有组织的生物学知识，却仅 **3/48（6.2%）转录因子**显示调控靶标特异性响应 [36]；因果电路追踪的 CRISPRi 基因级验证方向准确率仅 **56.4%**，据此认为模型编码的是共表达而非因果调控 [35]；独立系统评估框架（37 项分析、153 个统计检验）发现基因级基线 AUROC **0.81–0.88** 优于注意力/相关性边的 **0.70**，消融调控头无退化 [38]。**三条独立技术路线（SAE 特征图谱、因果电路追踪、注意力—基线对照）指向同一结论：当前单细胞基础模型主要编码共表达结构，而非因果调控逻辑。** 但结构信息并非完全无用：CSSI 可将 GRN 恢复提升至多 **1.85 倍** [38]，SAE 特征可干预——抑制批次特征改善整合，激活药物特征使对照细胞呈浓度依赖地向药物扰动状态转变 [45]。从 scGPT 提取的紧凑造血算法在 Tabula Sapiens 564,253 细胞上伪时间深度排序 **|ρ|=0.439**，优于次优的 **0.331**，且比 MLP 探针快 **34.5 倍**、参数少约 **1000 倍** [43]，说明内部几何中确实存在可提取的可用算子，但验证限于造血系统。

空间与多模态方向正在经历预训练目标的重新定义。CellWorld 将预测目标从重建观测基因转向预测潜在细胞表征，用空间 Transformer 建模细胞交互，**CellWorld-Small（5.74M）在全部 11 个线性探针和 7 个空间基准上超越所有基线**，仅用 5% 语料的冻结 Large 模型在 7 个空间基准上超越全部微调基线 [13]；NexuST 则反复交错基因级与细胞级建模，构建含 72 个数据集、4570 万人类细胞的 HumanST-46M [58]。跨模态对齐方面，OmiCLIP 基于 **220 万组织 patch、1007 样本、32 器官**训练，配套 Loki 平台在 5 个模拟、19 个公开、4 个内部数据集上对比 22 种 SOTA 方法 [17]；PAST 在 **2000 万配对病理图像与单细胞转录组**上联合编码形态与表达 [18]；mSTAR 把模态扩展到切片、报告与基因表达三种，在 15 类 97 项任务中表现优异并显示多模态预训练可用更少数据达到竞争性能 [19]。**三者的共同约束是依赖配对数据，跨中心泛化均待验证** [17][19]。多模态单细胞整合侧，CLM-X 在五个下游任务和 10 个数据集上持续超越现有多模态方法与单模态基础模型，**RNA-ATAC 跨模态翻译和扰动预测优势明显** [59]；moscot 把时序、空间、时空映射统一为 W、GW 或 FGW 型 OT 问题，在 170 万细胞小鼠胚胎等数据中实现高效对齐，计算时间与内存较既往 OT 工具降数个数量级 [60]。

综合以上证据，可归纳出以下趋势与空白：

1. **扰动预测的评测正在从「排行榜」转向「审计」**：scContam 揭示两个高引用基准存在大量预训练重叠证据 [31]，PerturBench 指出广泛使用模型存在模式崩溃、秩指标可补充 RMSE [47]，scArchon 以容器化流程统一 MSE、Wasserstein 及生物指标并聚合排名 [48]。**但尚无工作把污染审计、指标校准与模型排名整合为单一可复现的评测协议**——现有审计工具与排名框架各自独立，未形成闭环。

2. **「简单基线反超」的证据群已足够密集，但缺乏对反超条件的系统刻画**：Train Mean 优于 scGPT/scFoundation [32]、加性基线优于所有模型 [33]、VCBench 基线四维追平或超越 [39]、低监督下仅少数基础模型超过经典基线 [80]。**没人做的方向是：把「何时基础模型会输给基线」形式化为可预测的条件函数**（如扰动特异性方差、分布偏移程度、标注量），而非逐数据集报告胜负。

3. **机制可解释性三条路线收敛于「共表达而非因果调控」，但干预性利用才刚起步**：SAE 特征可干预以改善整合或诱导药物状态转变 [45]，从 scGPT 提取的造血算法可独立运行 [43]，GRN 泛化基准与冻结 scFM 蒸馏可超越现有方法 [44]。**空白在于：尚无工作把「模型编码共表达而非因果」这一否定性结论转化为正向的干预工具**——即用 SAE 特征或电路追踪结果直接指导扰动实验设计或 GRN 推断的因果校正。

4. **空间基础模型的预训练目标正在从重建转向潜在表征预测，但跨模态、跨平台泛化仍无系统证据**：CellWorld 以潜在细胞表征为目标并在小模型上超越基线 [13]，NexuST 交错两级建模 [58]，OmiCLIP/PAST/mSTAR 依赖配对数据 [17][18][19]。**没人做的方向是：在无配对数据的条件下，用空间上下文与形态先验联合推断转录组状态**——现有跨模态方法均以配对训练为前提。

5. **扰动数据资源在规模与生物学背景上快速扩张，但前瞻验证几乎空白**：Tahoe-100M 覆盖超 **1 亿**细胞、50 细胞系、379 化合物 [28]，全基因组 CD4+ T 细胞扰动覆盖 **4** 名供体、**2200 万**细胞 [70]，Perturb-FISH 把扰动与空间背景结合 [77]。**但肝脏 AIVC 综述明确指出，已发表模型仅展示单个组件，尚无经过前瞻验证的肝脏模拟器** [41]；可信虚拟细胞路线图同样主张评估应转向泛化到未见细胞类型与扰动 [15]。**空白在于：从计算预测到 CRISPR/类器官实验验证的闭环流程尚未在任一器官系统中被完整执行** [42]。

6. **表征提取方式本身被证明是未充分探索的变量**：逐层评估发现轨迹最优层在 **60% 深度**、扰动最优层随 T 细胞激活状态在 **0–96%** 间漂移、静息细胞首层最佳 [12]；无监督评估发现标准基准判定近乎等价的模型在丢弃 **5%** 计数时局部邻域保持差异近 **2 倍** [86]。**没人做的方向是：把「层选择」与「表征稳定性」纳入模型训练目标**——现有工作均默认使用最终层嵌入，而最优层依赖任务与细胞情境这一事实尚未被任何预训练目标显式建模。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 单细胞基础模型 | 成熟（方法收敛、增量为主） | scGPT [2] 与 Geneformer [3] 已确立"大规模预训练 + 迁移"范式并被广泛复用，后续工作多为架构/数据规模微调；同时 [9] 用 GPT 文本嵌入做基因/细胞表征即接近或超过复杂模型，说明表征红利已被摊薄；[55] 转向"可扩展检索"这类工程化能力，属增量改良。 |
| 2.2 空间与多模态模型 | 朝阳（近两年爆发、方法未收敛） | MultiVI [16] 与 moscot [60] 分别代表深度生成整合与时空映射两条尚未统一的路线；[89] 展示多模态图谱在疾病中的整合价值，但模态对齐、空间分辨率与批次仍是开放问题；[63] 说明 Cell Painting 影像模态刚进入整合视野，方法远未收敛。 |
| 2.3 扰动响应与虚拟细胞 | 朝阳（近两年爆发、方法未收敛） | Perturb-seq 系列 [24]、[25]、[26] 奠定数据基础，但预测方法仍在混战；[20] 提出"AI 虚拟细胞"路线图，属愿景性框架而非收敛方法；[33] 直接指出深度学习扰动预测尚未跑赢简单基线，说明核心问题未解。 |
| 2.4 机制可解释性与表征分析 | 萌芽（少量探索性工作） | 稀疏自编码器揭示单细胞基础模型可解释特征 [45] 与 [36] 均报告"有组织生物知识但调控信息有限"，结论互相印证但样本极少；[38] 系统评测可解释性并给出负面/有限结论，属早期批判性探索，尚无统一评测协议。 |
| 2.5 形态与图像表型基础模型 | 萌芽（少量探索性工作） | 池化 Cell Painting CRISPR 筛选平台 [73] 与检索式特征空间评测 [75] 分别代表数据生成与评测两端，但均为单点工作；[74] 综述指出影像 profiling 仍面临挑战，说明该方向尚未形成方法共识。 |
| 3 数据与资源 | 朝阳（近两年爆发、方法未收敛） | 全基因组 Perturb-seq 图谱 [27] 与遗传互作流形 [76] 提供大规模扰动资源；[79] 提出从细胞普查走向统一基础模型，说明资源正被重新组织为训练底座，但数据标准与模态覆盖仍在快速演化。 |
| 4 应用与结果 | 证据不足 | 仅 [41] 一篇，属愿景性讨论，无法据此判断阶段。 |
| 5 评测、可复现性与争议 | 朝阳（近两年爆发、方法未收敛） | 图谱整合基准 [30] 与 PerturBench [47] 建立评测框架；[33] 给出"未跑赢基线"的强负面证据，[90] 系统评估基础模型实用性，说明评测本身正成为独立且高争议的活跃方向。 |

**整体判断**：该方向整体处于**朝阳期**，但内部已明显分层——单细胞基础模型（2.1）进入**成熟期**，表征红利被 GPT 嵌入类简单方法追平 [9]，新工作以增量为主；真正的窗口在**扰动响应/虚拟细胞（2.3）**、**空间多模态（2.2）**与**评测（5）**，这三块近两年爆发、方法未收敛，且已有强负面证据 [33] 暴露核心缺口。窗口期估计还有 **1–2 年**：一旦扰动预测出现稳定跑赢基线的统一框架，或评测协议收敛，先发优势会迅速消失。最大不确定性是**扰动预测是否本质可学**——若 [33] 的负面结论被更多数据证实，整个"虚拟细胞"叙事需要从"预测"退回到"表征 + 检索 + 实验设计"，这会重定义投入方向。

**接下来怎么做**：

1. **用类器官多组学数据做扰动响应的"跨模态泛化"评测**：切入点是把合作项目里的类器官 Perturb-seq/药物扰动数据，按 [47] 的 PerturBench 协议切分，测试 RNA→蛋白/影像的跨模态预测是否比 RNA-only 基线更好；产出是一套可复现的负面/正面证据。现在做是因为 [33] 刚证明纯 RNA 扰动预测未跑赢基线，跨模态是否救场尚无定论，属于空白且高价值。

2. **把衰老作为扰动轴，构建"衰老虚拟细胞"评测子集**：切入点是用公共衰老图谱 + Tahoe/CZI 类资源 [27]、[79]，定义衰老相关基因/通路的扰动响应预测任务，复用 [90] 的评测框架；产出是领域首个衰老特化的扰动基准。现在做是因为衰老 + 扰动交叉几乎无人占位，且能直接对接他的博后课题。

3. **做空间多模态整合的"模态缺失鲁棒性"方法**：切入点是在 MultiVI [16] 与 moscot [60] 基础上，针对类器官空间数据常见的模态缺失/低分辨率问题设计鲁棒整合模块；产出是可开源权重与代码的整合工具。现在做是因为 2.2 方法未收敛，且 [89] 证明多模态图谱在疾病中有真实需求。

4. **切入机制可解释性，做基础模型的"调控信息"审计**：切入点是用稀疏自编码器 [45]、[36] 的思路，系统审计 scGPT/Geneformer 表征中是否编码真实调控关系，并与 [38] 的评测对齐；产出是一份可复现的可解释性审计报告 + 工具。现在做是因为 2.4 仅 7 篇、全为 2026 年新工作，属萌芽期，先入者易定义标准。

5. **用公共数据做低成本 demo，绑定合作项目验证**：切入点是用 CZI/HCA 公共数据 [79] 快速跑通上述 1–2 条 pipeline，产出预印本 + 开源代码，再用类器官多组学数据做外部验证。现在做是因为评测与虚拟细胞方向窗口期仅 1–2 年，先用公共数据占位、再用独家类器官数据建立壁垒，是风险最低的切入路径。

## 参考文献

1. Single-cell foundation models: bringing artificial intelligence into cell biology.. Experimental & molecular medicine 2025. https://doi.org/10.1038/s12276-025-01547-5
2. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. Nature Methods 2024. https://doi.org/10.1038/s41592-024-02201-0
3. Transfer learning enables predictions in network biology. Nature 2023. https://doi.org/10.1038/s41586-023-06139-9
4. CellFM: a large-scale foundation model pre-trained on transcriptomics of 100 million human cells.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59926-5
5. scPRINT-2: Towards the next-generation of cell foundation models and benchmarks.  2025. https://doi.org/10.64898/2025.12.11.693702
6. A Cross-Species Generative Cell Atlas Across 1.5 Billion Years of Evolution: The TranscriptFormer Single-cell Model. bioRxiv 2025. https://doi.org/10.1101/2025.04.25.650731
7. RegFormer: a single-cell foundation model powered by gene regulatory hierarchies.. Nature communications 2026. https://doi.org/10.1038/s41467-026-72198-x
8. LucaCell: a sequence-centric foundation model for cross-species single-cell analysis.  . https://doi.org/10.21203/rs.3.rs-11151765/v1
9. GenePT: A Simple But Effective Foundation Model for Genes and Cells Built From ChatGPT. bioRxiv 2023. https://doi.org/10.1101/2023.10.16.562533
10. Zero-shot evaluation reveals limitations of single-cell foundation models.. Genome biology 2025. https://doi.org/10.1186/s13059-025-03574-x
11. Evaluating the role of pretraining dataset size and diversity on single-cell foundation model performance.. Nature methods 2026. https://doi.org/10.1038/s41592-026-03120-y
12. Intermediate Layers Encode Optimal Biological Representations in Single-Cell Foundation Models.  2026. https://arxiv.org/abs/2604.14838v1
13. CellWorld: From Gene-Level Reconstruction to Latent Cell Prediction in Spatial Transcriptomics Foundation Models.  2026. https://arxiv.org/abs/2608.06659v1
14. Tahoe-x1: Scaling Perturbation-Trained Single-Cell Foundation Models to 3 Billion Parameters. bioRxiv 2025. https://doi.org/10.1101/2025.10.23.683759
15. Toward trustworthy virtual cells: a roadmap for perturbation-resolved, context-aware, and experimentally validated cell models. Frontiers in Cell and Developmental Biology 2026. https://doi.org/10.3389/fcell.2026.1900624
16. MultiVI: deep generative model for the integration of multimodal data. Nature Methods 2023. https://doi.org/10.1038/s41592-023-01909-9
17. A visual-omics foundation model to bridge histopathology with spatial transcriptomics.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02707-1
18. PAST: A multimodal single-cell foundation model for histopathology and spatial transcriptomics in cancer. arXiv.org 2025. https://arxiv.org/abs/2507.06418v1
19. A multimodal knowledge-enhanced whole-slide pathology foundation model.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66220-x
20. How to build the virtual cell with artificial intelligence: Priorities and opportunities.. Cell 2024. https://doi.org/10.1016/j.cell.2024.11.015
21. Virtual Cell Challenge: Toward a Turing test for the virtual cell.. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.008
22. Efficient Fine-Tuning of Single-Cell Foundation Models Enables Zero-Shot Molecular Perturbation Prediction.  2024. https://arxiv.org/abs/2412.13478v2
23. Predicting transcriptional responses to novel chemical perturbations using deep generative model for drug discovery.. Nature communications 2024. https://doi.org/10.1038/s41467-024-53457-1
24. Perturb-seq: Dissecting molecular circuits with scalable single cell RNA profiling of pooled genetic screens. Cell 2016. https://doi.org/10.1016/j.cell.2016.11.038
25. A multiplexed single-cell CRISPR screening platform enables systematic dissection of the unfolded protein response. Cell 2016. https://doi.org/10.1016/j.cell.2016.11.048
26. Pooled CRISPR screening with single-cell transcriptome read-out. Nature Methods 2017. https://doi.org/10.1038/nmeth.4177
27. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. bioRxiv 2021. https://doi.org/10.1016/j.cell.2022.05.013
28. Abstract 491: A 100 million cell single cell atlas enabling mechanistic and genotype-specific drug response discovery.. Cancer Research 2026. https://doi.org/10.1158/1538-7445.am2026-491
29. EpiZoo: a DNA sequence-aware foundation model for cross-species single-cell epigenomics.  . https://doi.org/10.64898/2026.09.24.754017
30. Benchmarking atlas-level data integration in single-cell genomics. Nature Methods 2020. https://doi.org/10.1038/s41592-021-01336-8
31. Auditing pretraining contamination in single-cell foundation model benchmarks.  2026. https://arxiv.org/abs/2607.20572v1
32. Benchmarking foundation cell models for post-perturbation RNA-seq prediction.. BMC genomics 2025. https://doi.org/10.1186/s12864-025-11600-2
33. Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02772-6
34. Deep learning perturbation models can outperform baselines on calibrated metrics.. Nature biotechnology . https://doi.org/10.1038/s41587-026-03307-w
35. Causal Circuit Tracing Reveals Distinct Computational Architectures in Single-Cell Foundation Models: Inhibitory Dominance, Biological Coherence, and Cross-Model Convergence.  2026. https://arxiv.org/abs/2603.01752v2
36. Sparse autoencoders reveal organized biological knowledge but minimal regulatory logic in single-cell foundation models: a comparative atlas of Geneformer and scGPT.  2026. https://arxiv.org/abs/2603.02952v1
37. Single-cell foundation models benefit from cross-modal training: adding proteomics data beats parameter scaling. bioRxiv 2026. https://doi.org/10.64898/2026.08.14.744845
38. Systematic Evaluation of Single-Cell Foundation Model Interpretability Reveals Attention Captures Co-Expression Rather Than Unique Regulatory Signal.  2026. https://arxiv.org/abs/2602.17532v1
39. VCBench: A Multi-Dimensional Benchmark for Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.06.18.733146
40. Benchmarking single-cell foundation models in a zero-shot setting. bioRxiv 2026. https://doi.org/10.64898/2026.08.03.739553
41. Toward AI Virtual Cells for Hepatology: Representation, Generation, Dynamics, and Intervention in Single-Cell Models.. Clinical and Molecular Hepatology 2026. https://doi.org/10.3350/cmh.2026.0820
42. AI-driven virtual cell models in preclinical research: technical pathways, validation mechanisms, and clinical translation potential.. NPJ digital medicine 2025. https://doi.org/10.1038/s41746-025-02198-6
43. Discovery of a Hematopoietic Manifold in scGPT Yields a Method for Extracting Performant Algorithms from Biological Foundation Model Internals.  2026. https://arxiv.org/abs/2603.10261v1
44. Towards Universal Gene Regulatory Network Inference: Unlocking Generalizable Regulatory Knowledge in Single-cell Foundation Models.  2026. https://arxiv.org/abs/2605.08128v1
45. Sparse Autoencoders Reveal Interpretable Features in Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.1101/2025.10.22.681631
46. PertEval-scFM: Benchmarking Single-Cell Foundation Models for Perturbation Effect Prediction. bioRxiv 2025. https://doi.org/10.1101/2024.10.02.616248
47. PerturBench: Benchmarking Machine Learning Models for Cellular Perturbation Analysis. Neural Information Processing Systems 2024. https://doi.org/10.48550/arXiv.2408.10609
48. scArchon: a scalable benchmarking framework for assessing single-cell perturbation models.. Genome biology 2026. https://doi.org/10.1186/s13059-026-04104-z
49. BioLLM: A standardized framework for integrating and benchmarking single-cell foundation models. bioRxiv 2024. https://doi.org/10.1016/j.patter.2025.101326
50. JUMP-lite: Compact, reproducible benchmarking of cell representations.  2026. https://arxiv.org/abs/2608.07632
51. Standardized metrics for assessment and reproducibility of imaging-based spatial transcriptomics datasets.. Nature biotechnology 2025. https://doi.org/10.1038/s41587-025-02811-9
52. Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling.  . https://doi.org/10.64898/2026.09.22.752128
53. scDifformer: diffusion-based post-training for virtual cell modeling across large-scale single-cell data. Nucleic Acids Research 2026. https://doi.org/10.1093/nar/gkag706
54. Scalable querying of human cell atlases via a foundational model reveals commonalities across fibrosis-associated macrophages. bioRxiv 2023. https://doi.org/10.1101/2023.07.18.549537
55. A cell atlas foundation model for scalable search of similar human cells.. Nature 2024. https://doi.org/10.1038/s41586-024-08411-y
56. Deep generative modeling of sample-level heterogeneity in single-cell genomics.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02808-x
57. PTM-Mamba: a PTM-aware protein language model with bidirectional gated Mamba blocks.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02656-9
58. NexuST: A Hierarchical Foundation Model for Spatial Transcriptomics.  . https://doi.org/10.64898/2026.09.22.753590
59. CLM-X: A multimodal single-cell foundation model with flexible multi-way Transformer for unified scRNA-seq and scATAC-seq analysis. bioRxiv 2026. https://doi.org/10.64898/2026.02.17.704943
60. Mapping cells through time and space with moscot.. Nature 2025. https://doi.org/10.1038/s41586-024-08453-2
61. Systematic benchmarking of high-throughput subcellular spatial transcriptomics platforms across human tumors.. Nature communications 2025. https://doi.org/10.1038/s41467-025-64292-3
62. A clinical benchmark of public self-supervised pathology foundation models.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58796-1
63. Cell Painting: a decade of discovery and innovation in cellular imaging.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02528-8
64. PerturbNet predicts single-cell responses to unseen chemical and genetic perturbations.. Molecular systems biology 2025. https://doi.org/10.1038/s44320-025-00131-3
65. STRAND: Sequence-Conditioned Transport for Single-Cell Perturbations.  2026. https://arxiv.org/abs/2602.10156v1
66. SCALE:Scalable Conditional Atlas-Level Endpoint transport for virtual cell perturbation prediction.  2026. https://arxiv.org/abs/2603.17380v3
67. AROMA: Augmented Reasoning Over a Multimodal Architecture for Virtual Cell Genetic Perturbation Modeling.  2026. https://arxiv.org/abs/2604.20263v1
68. Chreode: A Cell World Model for One-Step Temporal Dynamics and Perturbation Prediction. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.28111
69. A deep generative model for deciphering cellular dynamics and in silico drug discovery in complex diseases.. Nature biomedical engineering 2025. https://doi.org/10.1038/s41551-025-01423-7
70. Genome-scale perturb-seq in primary human CD4+ T cells maps context-specific regulators of T cell programs and human immune traits.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.002
71. Human interpretable grammar encodes multicellular systems biology models to democratize virtual cell laboratories.. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.048
72. Exhaustive Circuit Mapping of a Single-Cell Foundation Model Reveals Massive Redundancy, Heavy-Tailed Hub Architecture, and Layer-Dependent Differentiation Control.  2026. https://arxiv.org/abs/2603.11940v1
73. A pooled Cell Painting CRISPR screening platform enables de novo inference of gene function by self-supervised deep learning.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66778-6
74. Progress and new challenges in image-based profiling.. Molecular systems biology 2026. https://doi.org/10.1038/s44320-026-00197-7
75. Retrieval-Based Evaluation of Cell Painting Feature Spaces Reveals Differences in the Preservation of Biologically Meaningful Phenotypic Similarity.. International journal of molecular sciences 2026. https://doi.org/10.3390/ijms27135727
76. Exploring genetic interaction manifolds constructed from rich single-cell phenotypes. Science 2019. https://doi.org/10.1126/science.aax4438
77. Simultaneous CRISPR screening and spatial transcriptomics reveal intracellular, intercellular, and functional transcriptional circuits.. Cell 2025. https://doi.org/10.1016/j.cell.2025.02.012
78. A molecularly defined and spatially resolved cell atlas of the whole mouse brain. bioRxiv 2023. https://doi.org/10.1101/2023.03.06.531348
79. The Human Cell Atlas from a cell census to a unified foundation model.. Nature 2024. https://doi.org/10.1038/s41586-024-08338-4
80. Task-dependent Performance of Single-cell Foundation Models under Low Supervision. bioRxiv 2026. https://doi.org/10.64898/2026.04.01.714123
81. Biology-driven insights into the power of single-cell foundation models. Genome Biology 2025. https://doi.org/10.1186/s13059-025-03781-6
82. Harmonised benchmarking of foundation models for single-cell and spatial transcriptomics reveals context-dependent generalisation.  2026. https://arxiv.org/abs/2607.17227
83. A Systematic Evaluation of Single-Cell Foundation Models on Cell-Type Classification Task. Web Search and Data Mining 2025. https://doi.org/10.1145/3701551.3708811
84. Benchmarking Static Gene Regulatory Network Reconstruction and Dynamic Transition Probing in Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.05.17.725083
85. Systematic evaluation of single-cell foundation model interpretability: attention-derived edge scores add no incremental value over gene-level features for perturbation-target prediction. BMC Genomics 2026. https://doi.org/10.1186/s12864-026-12965-8
86. Robustness to nuisance perturbations enables unsupervised evaluation of single-cell foundation models. bioRxiv 2026. https://doi.org/10.64898/2026.08.22.746357
87. Counting cells can accurately predict small-molecule bioactivity benchmarks.. Nature communications 2026. https://doi.org/10.1038/s41467-026-68725-5
88. Benchmarking algorithms for generalizable single-cell perturbation response prediction.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02980-0
89. Integrated multimodal cell atlas of Alzheimer's disease.. Nature neuroscience 2024. https://doi.org/10.1038/s41593-024-01774-5
90. Evaluating the Utilities of Foundation Models in Single‐Cell Data Analysis. bioRxiv 2024. https://doi.org/10.1101/2023.09.08.555192
91. Parameter-free representations outperform single-cell foundation models on downstream benchmarks.  2026. https://arxiv.org/abs/2602.16696v1
