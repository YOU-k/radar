# 单细胞与空间组学基础模型与虚拟细胞 · 方向背景报告

证据 101 篇 · 覆盖度 0.65 · 第 13 轮 · 更新 2026-11-22 · 数字核验删句 3

## 本次变更

- 新增 [48] Single-cell dissection of immune-state architecture across diverse human population cohorts

## 摘要（TL;DR）

- scGPT 在超 **3300 万**细胞上做生成式预训练，经迁移学习后在注释、整合、扰动预测、基因网络推断等任务上表现优异[1]；Geneformer 在约 **3000 万**单细胞转录组上预训练，微调后在染色质与网络动力学任务中持续提升准确率[2]。
- CellFM 预训练于 **1 亿**人类细胞，在多种单细胞任务上达到或超过 Geneformer、scGPT、scFoundation、UCE 等基础模型[3]；scPRINT-2 覆盖 **3.5 亿**细胞、**16** 个物种，在表达去噪、细胞嵌入和细胞类型预测上达到 SOTA[4]。
- 一项用 **2220 万**细胞语料预训练 **400** 个模型、开展 **6400** 次实验的研究发现，性能在数据规模远小于当前训练语料时即趋于平台，**未观察到明确的数据缩放定律**[5]。
- 零样本评估在 5 个多样数据集上比较 Geneformer 与 scGPT 的细胞嵌入，结果两种基础模型在 AvgBIO 上多低于 HVG、Harmony、scVI 等更简单的基线[6]。
- 对 scFoundation（**100M** 参数）与 Tahoe-X1（**1.3B** 参数）逐层评估发现，轨迹推断最优层位于 **60%** 深度、比最终层高 **31%**，扰动响应的最优层随 T 细胞激活状态在 **0–96%** 间漂移[7]。
- RegFormer 融合基因调控网络先验与 Mamba 状态空间建模，在 **2500 万**人类细胞上预训练，在细胞注释、GRN 重建、遗传扰动预测和药物响应建模等基准上持续优于 scGPT 和 Geneformer[8]。
- SCimilarity 在 **2340 万**细胞、**412** 项研究（**56** 训练 / **15** 测试数据集）上训练，在查询敏感性与整合性能间取得最佳平衡（**β=0.001**），支持跨器官、系统与条件的可扩展细胞搜索[9]。
- CellWorld 将预测目标从观测基因测量转向潜在细胞表征，采用 JEPA 式预训练，**CellWorld-Small（5.74M）在全部 11 个线性探针和 7 个空间基准上超越所有基线**[10]。
- Tahoe-x1 系列参数规模最高 **30 亿**，在含 Tahoe-100M 扰动图谱的大规模单细胞转录组上预训练，在基因必需性、癌症标志基因、细胞类型分类和留出情境扰动响应预测四项基准上均达 SOTA[11]；而跨模态继续预训练仅用 **70M 参数**模型在 **48,843 个蛋白质组样本**上训练一个 epoch，就在多数原评测基准上匹配或超过 **1B 和 3B** 参数的 RNA-only 模型[12]。
- 系统评估框架（37项分析、153个统计检验）应用于 scGPT 与 Geneformer 后发现，注意力模式具有分层组织，但对扰动预测**无增量价值**：平凡基因级基线 AUROC **0.81–0.88**优于注意力/相关性边的**0.70**[13]。
- 有综述将面向肝脏的 **AI 虚拟细胞（AIVC）** 建模归纳为生成模型、动力学/运输模型和预训练/基础模型三条互补路线，并指出已发表模型仅展示了单个组件，**尚无经过前瞻验证的肝脏模拟器**[14]。
- **scContam** 用 MinHash 基因集指纹加基于损失的成员推断攻击逐细胞审计预训练污染，发现 PBMC 3k 与胰腺胰岛图谱分别有 **80.4%、77.0%** 的细胞指纹 p<0.05，说明零样本分数可能反映预训练暴露而非泛化[15]。
- 在四个 Perturb-seq 数据集上，差分空间 **Train Mean** 基线（0.711/0.557/0.373/0.628）优于 scGPT（0.641/0.554/0.327/0.596）与 scFoundation（0.552/0.459/0.269/0.471），而随机森林加 GO 特征最佳（0.739/0.586/0.480/0.648）[16]。
- VCBench 把四个虚拟细胞框架综合为七个能力维度，结果基线在 **5 维中 4 维**追平或超越所有基础模型，仅 TranscriptFormer 在 RNA 到蛋白预测上超最强基线 **53% Pearson**[17]。

## 1 背景与定义

单细胞与空间组学基础模型的边界，首先由“预训练语料—表征目标—下游任务”三者的耦合方式划定。主流路线把细胞类比为句子、基因类比为词元，用 Transformer 在 scRNA-seq 语料上自监督预训练，再迁移到注释、整合与扰动预测[1][2][18]；空间与病理侧则把图像 patch、基因句子或组织邻域压入共享表征[19][20][21]。**这一方向的共同前提是“表征可迁移”，而非“规则可解释”**：模型被期待从大规模图谱中学到可复用的细胞状态空间，但迁移的成立条件（任务设定、层选择、评估协议）本身尚未稳定[7][6]。因此本方向的边界应同时包含模型、数据资源与评测三类产出，缺一不可。

演化脉络上，可辨识出三条相互交织的线索。其二是**目标重定义**：空间侧从重建被掩码基因转向预测潜在细胞表征（CellWorld）或分层交错建模（NexuST）[10][22]，扰动侧从均值回归转向分布传输（SCALE、STRAND）与状态转移（Chreode）[23][24][25]。其三是**评测独立化**：从早期以整合基准为主[26]，走向扰动专用基准、虚拟细胞挑战赛与污染审计[27][15][28]。

“虚拟细胞”作为该方向的核心概念，其定义在文献中并不统一，大致可分三派。**数据驱动派**主张多尺度多模态大网络直接从数据学习细胞行为，无需显式规则，并以预测、生成、可查询为能力目标[29]；**机理可解释派**主张用自然语言细胞规则映射为可执行 agent-based 模型，强调模块化与可复现[30]；**证据链派**则把虚拟细胞定义为需具备数据、设计、基准与实验验证完整链条才具决策相关性的模型，并提出分子状态、干预、生物背景、正交表型四层经验框架[31]。三派的差别不在技术栈，而在**“什么算预测成功”**：是分布内拟合、分布外泛化，还是前瞻实验验证。这一分歧直接决定了评测设计，也解释了为何同一模型在不同报告中结论相反[16][32]。

扰动响应预测构成该方向最集中的问题域，其数据基础来自 Perturb-seq 系列平台：从早期约 20 万免疫细胞与细胞系的混合池筛选[33]、CROP-seq 的 gRNA 转录本读出[34]，到基因组规模 CRISPRi 筛选覆盖 >250 万人类细胞[35]，再到空间维度的 Perturb-FISH[36]与 Tahoe-100M 的亿级化学扰动图谱[37]。**核心问题可归纳为三点**：对照与处理细胞非配对（SCALE 以集合感知传输回避细胞级匹配[23]）、同一基因不同位点扰动被坍缩为同一表征（STRAND 以调控 DNA 序列为条件[24]）、以及扰动效应强背景依赖而模型多在细胞系或有限供体上训练[38]。这三点共同指向“跨背景泛化”这一尚未解决的枢纽问题。

多模态整合在本方向中承担双重角色：既是独立的方法子问题，也是虚拟细胞“多尺度”主张的技术支撑。RNA+ATAC+蛋白侧，MultiVI 以 VAE 对齐潜空间并模块化扩展至表面蛋白[39]，CLM-X 以多路 Transformer 与统一 token 化支持单模态与配对输入[40]；图像+转录组侧，OmiCLIP 以 CLIP 对比学习对齐 H&E 与基因句子[19]，PAST 联合编码细胞形态与基因表达[20]，mSTAR 进一步纳入病理报告形成三模态[21]。**这些工作的共同约束是配对数据可得性**，OmiCLIP 与 mSTAR 均将跨中心泛化列为待验证局限[19][21]；而 MultiVI 明确依赖相关群体多模态信息的存在[39]。这意味着多模态整合的进展速度受数据资源而非架构创新制约。

机制可解释性研究为上述“表征可迁移”假设提供了最直接的检验，也构成当前方向内部分歧最大的地带。SAE 特征分解显示模型内化了有组织的生物学知识，但转录因子调控靶标特异性响应仅 6.2%[41]；因果电路追踪报告两模型约 53% 生物一致性、65–89% 抑制主导，但 CRISPRi 基因级验证方向准确率仅 56.4%，作者判断模型编码共表达而非因果调控[42]；系统评估进一步发现注意力对扰动预测无增量价值，平凡基因级基线 AUROC 0.81–0.88 优于注意力边的 0.70[13]。与之张力的是，从 scGPT 内部提取的造血算法在伪时间排序与亚型判别上报告了可用性能[43]，GRN 蒸馏方法亦报告显著优于现有方法[44]。**这两类证据并不直接矛盾**：前者衡量内部表示的因果特异性，后者衡量提取算法的任务性能；但它们共同说明“模型内部有生物结构”与“该结构可用于扰动预测”是两个需分别验证的命题。

评测与批判性结果已足以改变该方向的自我定位。零样本评估中基础模型多低于 HVG、Harmony、scVI 等简单基线[6]；扰动预测上 Train Mean 基线优于 scGPT 与 scFoundation，随机森林加 GO 特征最佳[16]；K562 CRISPRa 双扰动数据上五个基础模型均未超过加性基线[45]；VCBench 在五个可测维度上基线于 4 维追平或超越所有基础模型[17]；无参数线性流程在分布外任务上超越基础模型[46]。与此同时，指标校准被指为分歧来源——在良好校准指标下深度学习扰动模型可优于无信息基线[32]，PerturBench 亦指出模式崩溃与秩指标的必要性[47]。**因此“没跑赢基线”这一证据本身需与评估协议一同解读**，而预训练污染审计进一步表明零样本分数可能反映预训练暴露而非泛化[15]。

综合来看，本方向当前的核心问题不是“能否构建更大的模型”，而是**如何在可比的评估协议下界定基础模型相对简单基线的增量价值，并把这种价值锚定到可实验验证的生物学预测上**。数据资源侧，Tahoe-100M、CARDINAL 与 Human Cell Atlas 的整合路线提供了规模基础[37][48][49]；方法侧，传输模型、序列条件化与分层空间建模提供了新的归纳偏置[23][24][22]；评测侧，虚拟细胞挑战赛、分层 OOD 压力测试与污染审计提供了独立化的基础设施[27][28][15]。**三者的衔接程度，而非任一单点的规模纪录，将决定“虚拟细胞”从概念走向可信模拟器的进度**；肝脏 AIVC 综述所指出的“尚无经过前瞻验证的肝脏模拟器”[14]，正是这一衔接尚未完成的具体表征。

## 2 方法学


### 2.1 单细胞基础模型

单细胞基础模型的主流路线，是把细胞类比为句子、基因类比为词元，用 Transformer 在大规模 scRNA-seq 语料上自监督预训练，再迁移到注释、整合、扰动预测等下游任务。**scGPT** 在超 **3300 万**细胞上做生成式预训练，经迁移学习后在注释、整合、扰动预测、基因网络推断等任务上表现优异[1]；**Geneformer** 在约 **3000 万**单细胞转录组上预训练，以自监督方式把网络层级编码进注意力权重，微调后在染色质与网络动力学任务中持续提升准确率，并在有限患者数据下识别出心肌病候选治疗靶点[2]。综述将这一范式概括为以细胞为句子、基因为词元，通过自监督学习通用表征并适配多种下游任务[18]。

预训练规模被持续推高。**CellFM** 预训练于 **1 亿**人类细胞，在多种单细胞任务上达到或超过 Geneformer、scGPT、scFoundation、UCE 等基础模型[3]；**scPRINT-2** 覆盖 **3.5 亿**细胞、**16** 个物种，在表达去噪、细胞嵌入和细胞类型预测上达到 SOTA，并具备表达插补与反事实推理的生成能力[4]；**TranscriptFormer** 在多达 **1.12 亿**细胞、**12** 个物种、跨越 **15.3 亿年**进化的数据上训练，分布内与分布外细胞类型分类达 SOTA，可零样本识别疾病状态并跨物种转移注释[50]。但规模并非无代价地有效：一项用 **2220 万**细胞语料预训练 **400** 个模型、开展 **6400** 次实验的研究发现，性能在数据规模远小于当前训练语料时即趋于平台，**未观察到明确的数据缩放定律**[5]。

对上述模型的严格评估揭示了明显争议。零样本评估在 5 个多样数据集上比较 Geneformer 与 scGPT 的细胞嵌入，以 HVG、Harmony、scVI 为基线，结果两种基础模型在 AvgBIO 上多低于这些更简单的基线，HVG 在所有指标上优于二者，scGPT 仅在 PBMC 12k 上部分优于 scVI/Harmony[6]。这与预训练论文报告的优越性能形成张力，也说明微调设定与零样本设定下的结论不能互相替代。另一项工作则质疑“默认取最终层嵌入”的惯例：对 scFoundation（**100M** 参数）与 Tahoe-X1（**1.3B** 参数）逐层评估发现，轨迹推断最优层位于 **60%** 深度、比最终层高 **31%**，扰动响应的最优层随 T 细胞激活状态在 **0–96%** 间漂移，静息细胞首层反而最佳[7]。

架构上的分化体现在对先验知识和序列长度的处理。**RegFormer** 融合基因调控网络先验与 Mamba 状态空间建模，以规避 Transformer 的上下文长度与可扩展性限制，在 **2500 万**人类细胞上预训练，在细胞注释、GRN 重建、遗传扰动预测和药物响应建模等基准上持续优于 scGPT 和 Geneformer[8]。**scDifformer** 采用掩码语言模型预训练、扩散驱动后训练与下游微调三阶段设计，扩散模块在强批次效应下持续提升跨数据集性能，细胞类型注释达到 SOTA，并支持空间转录组 spot 去卷积[51]。**GenePT** 则走极简路线，用 GPT-3.5 基于 NCBI 基因文本描述生成基因嵌入，无需数据策展与预训练，在基因属性与细胞类型分类等任务上达到与 Geneformer 等相当甚至更优的性能[52]。

以检索和样本比较为目标的工作把重点从“生成表征”转向“可查询的细胞空间”。**SCimilarity** 用深度度量学习同时优化监督三元组损失与无监督重构损失，在 **2340 万**细胞、**412** 项研究（**56** 训练 / **15** 测试数据集）上训练，在查询敏感性与整合性能间取得最佳平衡（**β=0.001**），支持跨器官、系统与条件的可扩展细胞搜索[9]；其早期版本在 **2270 万**细胞、**399** 项研究语料上训练，验证了最初在间质性肺病中识别的巨噬细胞亚群也存在于其他纤维化疾病、组织和 3D 水凝胶系统中[53]。与之互补，**MrVI** 面向多样本队列的样本级异质性，用层次深度生成模型与交叉注意力建模样本协变量效应，无需先验聚类即可识别样本分组，并实现高分辨无注释差异表达与丰度分析[54]。

跨物种与跨模态是近期扩展的主要方向。**Speciesformer** 将进化表征学习与虚拟细胞状态生成结合，在含 **1.31 亿**细胞的 SpeciesCorpus 上预训练，目标是学习可迁移的细胞状态与状态转变，并区分保守生物学原理与物种、组织及细胞环境特异变异[55]。**LucaCell** 以预训练 mRNA 序列嵌入表示基因而非固定基因注释，将表达离散化为 bin 后用 Transformer 编码，在 **8500 万**人类和小鼠单细胞上预训练，实现人、小鼠和狐猴肾脏数据中的跨物种、跨模态细胞类型迁移，并实现无比对微生物嵌入、区分 **50 多种**细菌且保留种内结构[56]。**EpiZoo** 把百万维跨物种单细胞表观基因组谱转换为紧凑的“细胞句子”，整合 DNA 编码的调控信息与基于可及性的重要性，以克服现有模型依赖基因组坐标、局限于单一物种的问题[57]；**ProtCell** 则把基础模型推进到单细胞蛋白组学，基于 **98** 个数据集约 **3.8 亿**细胞预训练，结合蛋白身份嵌入与连续丰度嵌入做掩码丰度建模，可连接碎片化蛋白组谱实现可迁移注释与批次校正，并扩展有限面板推断未测量的细胞毒性蛋白程序[58]。

值得注意的是，模型能力与实际问题采用之间仍有落差。综述指出早期 scRNA-seq 嵌入模型和基础模型在实验生物学家中应用有限，而随着大规模单细胞图谱积累，利用 AI 在庞大数据背景下解读新数据集的需求变得明确，单细胞表观/多组学检测与 Perturb-seq 也带来新的建模机会[59]。这一判断与零样本评估的负面结果[6]、层选择的任务依赖性[7]以及数据缩放平台的发现[5]共同指向同一问题：单细胞基础模型的收益高度依赖任务设定、评估协议与表征抽取方式，而非仅由预训练细胞数决定。

### 2.2 空间与多模态模型

空间转录组基础模型的一条主线是预测目标的重新定义。早期方法多以重建被掩码的基因身份或表达值为目标，CellWorld 指出这可能促使模型复制测定特异的技术变异、限制表征迁移性，因而将预测目标从观测基因测量转向潜在细胞表征，采用 JEPA 式预训练，在 **4600 万人细胞、3 平台 11 器官**上训练 4 个变体（5.74M–94.56M 参数）；**CellWorld-Small（5.74M）在全部 11 个线性探针和 7 个空间基准上超越所有基线**，仅用 5% 语料的冻结 Large 模型在 7 个空间基准上超越全部微调基线 [10]。与之不同，NexuST 走分层路线，反复交错基因级分子建模与细胞级空间建模，使两个层级在端到端预训练中相互优化，并构建 **HumanST-46M（72 个数据集、11 个器官、三种成像平台、4570 万人类细胞）**，在四个留出数据集约 260 万细胞上于细胞类型注释、区域预测、基因恢复等任务达到 SOTA 或具竞争力 [22]。两者都强调空间迁移更依赖生物来源多样性与优化而非细胞数量 [10]，但预测目标（潜表征 vs 分层交错建模）的取舍尚无直接对比。

病理图像与空间转录组的跨模态对齐是另一条主线。PAST 在 **2000 万配对病理图像与单细胞转录组**上联合编码细胞形态与基因表达，学习统一跨模态表征，支持单细胞基因表达预测、虚拟分子染色和多模态生存分析，并在多种癌症任务中超越现有方法 [20]。OmiCLIP 则以 CLIP 对比学习把 H&E 图像与由高表达基因符号拼接成的“基因句子”对齐，基于 **ST-bank 的 220 万组织 patch、1007 样本、32 器官**，配套 Loki 平台提供组织对齐、注释、细胞分解、检索与基因表达预测五项功能，在 5 个模拟、19 个公开和 4 个内部数据集上对比 22 种 SOTA 方法 [19]。mSTAR 进一步把模态扩到三路——病理切片、专家报告与基因表达，用 **26,169 切片-模态对、10,275 患者、32 癌种、1.16 亿 patch** 做两阶段预训练，在 15 类 97 项任务中表现优异，并显示多模态预训练可用更少数据达到竞争性能 [21]。三者的共同前提是配对数据可得，OmiCLIP 明确将依赖配对 WSI 与 Visium 数据、泛化待验证列为主要局限 [19]，mSTAR 亦指出跨中心泛化仍需验证 [21]。

生成式视觉语言模型提供了另一种读取空间组织的方式。VINTER 在 **145 万组织学-文本对**上对齐，将组织学图像、实测基因表达和空间邻域作为单一序列读取，输出每个组织类别的概率；由于基因以文本形式输入，可在固定图像下编辑分子证据，联合三源信息后其组织注释精度优于空间域方法和空间基础模型 [60]。这与 OmiCLIP 的对比学习对齐、PAST 的联合编码在机制上不同：前者把分子证据作为可编辑的输入序列，后两者把模态对齐压进共享表征。

单细胞多模态整合模型处理的是另一类子问题：缺失模态与跨模态推断。MultiVI 用 VAE 分别建模基因表达与染色质可及性，通过惩罚使两模态潜空间对齐，并模块化扩展至表面蛋白，可整合单模态数据集、提供校准的不确定性估计、准确估计缺失模态的差异表达/可及性，并在相关群体存在时实现样本外预测 [39]。CLM-X 则以多路 Transformer 加统一 token 化与分阶段掩码重建，在百万级单模态与多模态数据上预训练，支持 RNA-only、ATAC-only 和配对 RNA-ATAC 输入，在五个下游任务和 10 个数据集上持续超越现有多模态方法与单模态基础模型，RNA-ATAC 跨模态翻译和扰动预测优势明显 [40]。两者都依赖相关群体或配对数据的存在，MultiVI 明确将“依赖相关群体多模态信息”列为局限 [39]。

空间映射与评测层面，moscot 把时序、空间和时空映射统一为 W、GW 或 FGW 型最优传输问题，支持多模态与图谱规模数据，在 **170 万细胞小鼠胚胎**等数据中实现高效对齐，计算时间与内存较既往 OT 工具降数个数量级，并实验验证 NEUROD2 调控 epsilon 细胞形成 [61]。评测工作则揭示平台与方法间的显著差异：四项亚细胞分辨率平台（Stereo-seq v1.3、Visium HD FFPE、CosMx 6K、Xenium 5K）在三种人肿瘤连续切片上统一评测，以 CODEX 蛋白和 scRNA-seq 作真值，各平台在灵敏度、扩散控制、细胞分割等指标上差异显著 [62]；细胞分割基准覆盖 5 种技术、15 个数据集、12 种人鼠组织，比较 11 种图像/转录组/多模态方法，发现分割质量、转录本回收、表达纯度等指标差异显著 [63]。这些差异意味着上述基础模型的性能结论受平台与分割选择影响，跨研究数字不宜直接比较。病理侧亦有临床基准系统比较 CTransPath、Phikon、UNI、Virchow 等公开自监督模型的参数量、算法与训练数据及下游临床任务性能，指出数据与算力是主要瓶颈 [64]；而 Cell Painting 作为 2013 年提出的显微细胞标记检测，经协议优化、特征提取改进与批次校正，已用于解析化合物作用机制与毒性，其未来方向被描述为整合其他高内涵数据类型 [65]。

### 2.3 扰动响应与虚拟细胞

扰动响应预测正从静态的“对照—处理”映射转向对细胞状态分布与动态的建模。早期 Perturb-seq 将单细胞 RNA-seq 与 CRISPR 扰动条形码结合，在混合池中大规模读取转录表型：一项工作分析约 **200,000 个免疫细胞和细胞系**，识别扰动靶点、基因 signature、细胞状态与遗传互作 [33]；另一项以液滴单细胞 RNA-seq 解剖未折叠蛋白反应，经两个全基因组 CRISPRi 筛选鉴定约 **100 个命中基因**，解耦三条 UPR 分支 [66]。CROP-seq 则把 gRNA 盒插入慢病毒 3'LTR 使其成为可检测的 mRNA，实现池化筛选的单细胞转录组读出，并验证编辑效率与 LentiGuide-Puro 高度相似 [34]。这些平台奠定了扰动数据的基础，但其通量与多模态覆盖有限。

在数据规模端，扰动训练的基础模型开始出现。**Tahoe-x1** 系列参数规模最高 **30 亿**，在含 Tahoe-100M 扰动图谱的大规模单细胞转录组上预训练，采用含药物 token 的掩码表达生成目标，在基因必需性、癌症标志基因、细胞类型分类和留出情境扰动响应预测四项基准上均达 SOTA，计算效率较先前细胞状态模型提升 **3–30 倍** [11]。与之形成对照的是跨模态路线：对 Tahoe-x1 做跨模态继续预训练，仅用 **70M 参数**模型在 **48,843 个蛋白质组样本**（来自 **440 项质谱研究**）上训练一个 epoch，就在多数原评测基准上匹配或超过 **1B 和 3B** 参数的 RNA-only 模型，并提升对 held-out 蛋白扰动基准的迁移，作者据此主张精心策划的蛋白质组数据带来的收益可超过单纯扩大规模 [12]。这一结果与“规模驱动”叙事构成直接张力，但两者评测基准与任务并不完全相同，不宜简单比高低。

化学扰动方向，**PRnet** 以 SMILES 与剂量构建扰动嵌入、结合未扰动表达谱生成响应分布，在新化合物、通路和细胞系预测上优于替代方法，实验验证了小细胞肺癌与结直肠癌候选化合物，并构建覆盖 **88 细胞系、52 组织**的扰动图谱、为 **233 种疾病**推荐药物 [67]。**PerturbNet** 则强调预测未见化学与遗传扰动引起的细胞状态分布变化而非仅均值，对标 scGen、CPA、chemCPA、GEARS、Biolord 等方法 [68]。两者都受限于训练扰动空间的覆盖度，对全新化学空间的外推能力有限。

针对“对照与处理细胞非配对”这一实验现实，**SCALE** 将细胞视为无序集合，用共享集合感知编码器与条件 DiT 学习潜在传输，无需细胞级匹配，在 CRISPR 数据七项指标上全面超越竞争方法，其预测的细胞因子差异经三供体 PBMC 实验验证 [23]。**STRAND** 则指出基因级模型会把同一基因不同位点的扰动坍缩为同一表征，改以调控 DNA 序列编码为条件，在 K562、Jurkat、RPE1 上低样本判别分提升达 **33%**，新细胞系迁移 Pearson 提升达 **0.14**，基因组覆盖从约 **1.5%** 扩至约 **95%** [24]。二者分别从“去配对假设”和“位点分辨率”切入，但都依赖编码或传输质量，序列到转录组的非线性映射仍是瓶颈。

时序与动态建模是另一条分线。**Chreode** 以结构化残差转移算子做一步式状态转移预测，将分布演化从推理时移至训练时，在 **240 万细胞**小鼠胚胎图谱上预训练，作为 GEARS 可迁移嵌入将 Norman Perturb-seq 的 DE20 MSE 从 **0.2121** 降至 **0.1858**（相对提升 **12.4%**）[25]。**DynaVelo** 用生成式神经常微分方程从单细胞多组学数据学习基因表达与 TF motif 活性的联合动态，重现野生型小鼠生发中心 B 细胞的体内分叉动态，并揭示 Arid1a 和 Ctcf 杂合缺失下的变化 [69]。**UNAGI** 则以 VAE-GAN 从疾病时间序列单细胞数据解析细胞动力学并做计算机药物筛选 [70]。这些工作共享“把时间纳入模型”的动机，但验证体系分别限于胚胎图谱、B 细胞和特定疾病数据，泛化性尚未统一检验。

在扰动预测之外，虚拟细胞的构建路线存在明显分歧。一派主张多尺度多模态大神经网络直接从数据学习细胞行为，提出预测、生成、可查询三大能力，并以 2012 年首个全细胞模型（**482 基因**）为对照 [29]；另一派强调可解释性，提出用自然语言“细胞规则”一一映射为数学方程、构建 agent-based 模型，案例覆盖肿瘤生长、侵袭、免疫治疗与脑发育 [30]。**AROMA** 走多模态增强推理路线，整合文本证据、图拓扑与蛋白序列，构建 **PerturbReason 数据集（>498k 样本）**，在未见细胞系零样本与知识稀疏长尾场景下保持稳健，但依赖知识图谱与检索质量 [71]。**PRnet** 式的生成模型与语法式机理模型之间，核心争议在于可解释性与预测广度的取舍。

评测与可信度正成为独立议题。**Virtual Cell Challenge** 以开放循环基准竞赛形式提供评估框架与专用数据集，推动扰动响应预测的可比评测 [27]。有观点批评当前工作偏重模型规模与数据量，主张虚拟细胞模型需明确数据、设计、基准与实验验证的证据链，提出分子状态、干预、生物背景、正交表型四层经验框架，并指出静态图谱、仅转录组读出与分布内基准不足以预测新条件下的行为 [31]。临床前转化综述则强调以 CRISPR 和类器官实验形成闭环验证，同时指出监管接受、数据隐私与可解释性仍是障碍 [72]。这些框架性工作本身不提供模型结果，但为上述方法间的比较设定了标准。

数据侧的边界也在被推进。一项全基因组 perturb-seq 在 **4 名供体、2200 万原代人 CD4+ T 细胞**的静息与刺激态测量转录组效应，发现调控因子及其所控基因程序随刺激条件大幅变化，并提名极化与衰老表型调控因子、关联自身免疫病风险 [38]。这类原代细胞、多供体、条件依赖的数据提示：扰动效应具有强背景依赖性，而现有虚拟细胞模型多在细胞系或有限供体上训练，跨背景泛化仍是未解问题。

### 2.4 机制可解释性与表征分析

机制可解释性研究目前主要沿两条技术路线展开：稀疏自编码器（SAE）特征分解与注意力/电路层面的因果干预。在特征分解方面，对Geneformer V2-316M与scGPT全人模型各层残差流激活训练TopK SAE，分别得到**82525与24527个特征**，其中**99.8%的特征SVD不可见**，仅29–59%能注释到通路；转录因子调控特异性响应仅**3/48（6.2%）**，多组织对照下为10.4%[41]。在三个scFM（scGPT、scFoundation、Geneformer）隐藏表示上训练SAE则显示特征涵盖多样生物与技术信号，且不同训练协议与架构的编码方式不同；抑制批次特征可改善整合并保留生物信号，激活药物特征能使对照细胞浓度依赖地向药物扰动状态转变[73]。这两项工作都表明SAE特征具有功能相关性，但对“特征是否编码调控逻辑”给出了不同侧重的答案：前者强调调控逻辑编码极少，后者强调特征可干预、与模型行为功能相关。

因果电路层面的证据进一步区分了“有结构的生物信息”与“可用于扰动的机制”。系统评估框架（37项分析、153个统计检验、四种细胞类型、两种扰动模态）应用于scGPT与Geneformer后发现，注意力模式具有分层组织——早期层对应蛋白-蛋白相互作用、晚期层对应转录调控——但对扰动预测**无增量价值**：平凡基因级基线AUROC **0.81–0.88**优于注意力/相关性边的**0.70**，消融调控头无退化，CSSI可将GRN恢复提升至多**1.85×**[13]。因果电路追踪（96,892条边、80,191次前向）则显示两模型约**53%生物一致性**、**65–89%抑制主导**且不随架构与细胞类型变化，跨模型共识**1,142个域对（10.6倍富集）**，但CRISPRi基因级验证方向准确率仅**56.4%**，作者据此判断模型编码的是共表达而非因果调控[42]。对Geneformer的穷举电路追踪（L5层全部4065个SAE特征）得到**1,393,850条显著下游边**，较选择性采样扩**27倍**，并发现重尾枢纽结构（1.8%特征占大量连接，40%顶级枢纽无注释）、随交互阶数单调加深的冗余（三阶冗余比0.59 vs 配对0.74，零协同），以及层位置决定分化方向性（L17特征100%推向成熟，L0/L11为0.00–0.58）[74]。这些结果共同指向一个争议点：电路与注意力确实承载分层生物结构，但其对扰动预测的边际贡献有限，且基因级验证准确率接近随机水平。

与上述“编码共表达而非因果”的判断形成张力的是，从scGPT内部提取紧凑造血算法的尝试报告了可用的下游性能：在Tabula Sapiens **564,253细胞**上，伪时间深度排序**|ρ|=0.439**优于次优**0.331**，CD4/CD8 AUROC **0.867**、单核/巨噬**0.951**，且比MLP探针快**34.5倍**、参数少约**1000倍**[43]。在GRN推断方向，有工作指出重建式预训练未显式捕获调控信号、现有零样本方法有时不及随机预测，因而提出GRN泛化基准并用虚拟值扰动与梯度轨迹从冻结scFM蒸馏基因间特征，报告显著优于现有方法[44]；CauTrigger则将do-calculus整合进分层深度潜变量模型，分离因果与虚假潜因子、递归重建调控层级，在合成与真实多层调控数据集上优于现有方法[75]。需要指出，造血算法提取仅在造血系统验证、泛化性有限[43]，GRN与CauTrigger的证据以“优于现有方法”的定性表述为主[44][75]，与SAE/电路研究“调控逻辑编码极少”的结论并不直接可比——前者衡量的是提取算法的任务性能，后者衡量的是模型内部表示的因果特异性，二者构成当前机制可解释性领域的主要分歧。

### 2.5 形态与图像表型基础模型

图像表型基础模型的核心问题正从“能否提取有用特征”转向“特征空间是否保留任务相关的生物关系”。Cell Painting 与 pooled 光学 CRISPR 筛选结合的自监督平台 CellPaint-POSH 在 **163,090 个单细胞**上学习形态表征，其自监督机器学习特征在基因功能预测上优于专家形态特征，并能在无通路报告基因的条件下按已知功能聚类基因、揭示基因关联网络[76]。但特征空间的优劣依赖具体任务：在 U2OS JUMP-MOA 参考板的 **90 个化合物**上零样本评估时，CellPaintSSL、OpenPhenom、uniDINO 的活性阳性数分别为 **85/90、81/90、82/90**，数量相近，而 CellPaintSSL 的活性检索 mAP 显著高于另两者（p<0.0001），MOA 注释仅部分恢复且因模型而异[77]。这表明预训练特征的总体质量并不保证目标生物学关系的恢复，特征空间需在下游检索前做任务感知的资格评估。

在训练范式上，自监督预训练与生成式建模两条路线都在试图把生物响应显式纳入表征学习。系统评估对比式（DINO）、掩码生成式（MAE、iTPN）与混合式（DINOv2）模型的工作，在 JUMP-CP 全部未标注化学扰动数据（**119,876 化合物、约 177 万图像、7 个实验室**）上预训练，于 JUMP-Target2 留出集上最佳 SSL 模型在化合物重复检索上优于 CellProfiler[78]；综述则给出 CLOOME 零样本 MoA top-10 准确率 **61.3%** 对 CellProfiler **24.5%** 的对照，同时提醒时序与 3D 数据方法、质控标准及特征解释仍不成熟，且部分场景手工特征仍具竞争力[79]。生成方向上的 PerturbBridge 主张虚拟细胞模型不应只匹配真实图像分布，而应在训练中对预测的扰动图像直接施加扰动特异性表型监督，在 BBBC021 上 MoA 准确率 CellProfiler 达 **77.8%**（较 CellFlux 高 5.7 点）、DINOv2 达 **74.9%**（高 7.5 点）[80]。与检索评估工作强调“特征空间须先验证”相比，生成式工作更关注生物监督信号进入流程的位置，二者构成方法取向上的差异而非直接冲突；共同点是都承认形态表型的生物学可解释性仍受模型与任务依赖的限制。

## 3 数据与资源

在扰动筛选数据方面，**Perturb-seq** 已从区域尺度推进到基因组规模：一项工作报告了靶向所有表达基因的 CRISPRi 筛选，覆盖 **>2.5 million human cells**，在 K562 与 RPE1 两个细胞系中测定数千个功能缺失扰动，并据此研究 RNA 剪接、分化、染色体不稳定等多维表型 [35]。同一技术路线的另一项工作则把高维单细胞表型组织为细胞状态"流形"，将每个扰动与遗传互作投射到流形特定位置，用于调控通路的无偏排序和遗传互作的系统分类 [81]。两者的差异在于前者追求扰动规模与表型广度，后者侧重以流形框架解释遗传互作机制；前者亦自述仅限两个细胞系、CRISPRi 为敲低而非敲除、表型限于转录组 [35]。

空间维度上，**Perturb-FISH** 将 MERFISH 与 gRNA 原位扩增结合，在空间背景下同时解码扰动与转录组，并在 LPS 刺激巨噬细胞中与匹配的 Perturb-seq 数据比较，验证敲除效应的一致性，进而分析细胞密度与邻居扰动的影响，还结合钙成像用于 ASD 风险基因的 CRISPRi 筛选及肿瘤异种移植 3D 组织验证 [36]。非扰动型空间图谱方面，小鼠全脑 MERFISH 对约 **800万细胞** 成像 >1100 基因并整合 scRNA-seq，生成包含 >5000 转录簇、约 300 主要细胞类型的图谱并注册到 CCF [82]；其局限在于仅限小鼠脑且基因面板有限、需整合 scRNA-seq [82]。

面向药物响应与群体变异的大规模资源亦在形成。**Tahoe-100M** 覆盖 **100 million** 以上细胞、50 个细胞系与 379 种化合物（3 剂量、24 小时），覆盖约 56,000 个细胞系-药物-剂量组合，报告了 Dabrafenib 在非 BRAF 依赖细胞系中的意外敏感性及 CDK 抑制剂引起 G1 或 G2/M 阻滞 [37]；该摘要未提供模型训练与验证细节 [37]。CARDINAL 项目则构建覆盖成年生命历程的群体规模外周血单细胞图谱，纳入两个英国队列 **6003 名个体** 的近 1000 万免疫细胞，目标是解析衰老、环境暴露、感染史与疾病对免疫变异和疾病易感性的共同影响 [48]。在资源整合层面，有综述提出细胞图谱正从数据收集走向图谱整合，并将作为细胞普查、3D 图谱、基因型-表型连接、4D 发育图谱及生物学基础模型五种用途，最终指向统一基础模型 [49]。需注意上述资源在物种、细胞类型与扰动类型上各不相同，其规模数字不宜跨研究直接比较。

## 4 应用与结果

现有肝脏单细胞与空间图谱已能在高分辨率下刻画健康与病变肝脏，包括肝小叶肝细胞分区、纤维化巨噬细胞—星状细胞生态位、胆管细胞反应、免疫重塑及肝细胞癌生态系统，但这些图谱本身只能显示细胞状态出现的位置，并不能预测肝损伤是否进展，也无法预测肝脏对未经测试的药物、毒物或遗传扰动的响应。为此，有综述将面向肝脏的 **AI 虚拟细胞（AIVC）** 建模归纳为生成模型、动力学/运输模型和预训练/基础模型三条互补路线，并以扰动响应预测作为跨层评估的切入点 [14]。

该综述进一步把现有证据分为直接肝脏验证、含肝脏基准、通用单细胞证据和概念应用四类，并指出已发表模型仅展示了图谱整合、轨迹推断、可迁移表示、回顾性响应程序等单个组件，**尚无经过前瞻验证的肝脏模拟器** [14]。这一判断也构成对评估设计的要求：验证需覆盖供体、病因、分期和平台等维度，而非停留在回顾性拟合 [14]。

## 5 评测、可复现性与争议

评测工作首先暴露的是基准本身的可信度问题。**scContam** 用 MinHash 基因集指纹加基于损失的成员推断攻击（MIA-scFM）逐细胞审计预训练污染，在四个 scIB 基准和三个 scFM 上发现 PBMC 3k 与胰腺胰岛图谱分别有 **80.4%、77.0%** 的细胞指纹 p<0.05，而截断后的 AIDA v2 与 Tahoe-100M 为 **0%**；MIA AUROC 随模型容量数据比从 0.494 升至 0.690 再到 0.881 [15]。这说明零样本分数可能反映预训练暴露而非泛化，且生产级模型对实例记忆有抵抗，分布污染仍需单独检测 [15]。另一类问题是划分方式：EL-PERTURB 指出多数基准依赖随机划分，掩盖了系统性失效模式，在必需基因与全基因组 Perturb-seq 上对 6 类架构 20 个模型做分层 OOD 压力测试后，扰动预测模型在真实 OOD 条件下泛化失败 [28]。

在扰动预测这一子问题上，结论冲突最明显。一边是多项评测报告基础模型不敌简单基线：在四个 Perturb-seq 数据集上，差分空间 **Train Mean** 基线（0.711/0.557/0.373/0.628）优于 scGPT（0.641/0.554/0.327/0.596）与 scFoundation（0.552/0.459/0.269/0.471），而随机森林加 GO 特征最佳（0.739/0.586/0.480/0.648）[16]；K562 CRISPRa 双扰动数据上五个基础模型和两个深度学习模型均未超过加性基线，遗传互作预测不优于 no change 基线 [45]；PertEval-scFM 发现零样本 scFM 嵌入未持续优于基线，尤其在分布偏移下 [83]。另一边，指标校准被指为分歧来源：在 14 个数据集、18 个指标上，MSE 和 Pearson Δ 等常用指标常校准不良，降低了对阳性模型性能的敏感性，而在良好校准指标下深度学习扰动模型可优于无信息基线 [32]。PerturBench 则从另一角度补充：广泛使用模型存在模式崩溃，秩指标可补充 RMSE，且无单一架构明显占优、简单架构具竞争力并随数据规模扩展良好 [47]。27 种方法、29 个数据集、6 类指标的综合评测同样对基础模型的真实效力存疑，并强调细胞上下文嵌入对泛化性的必要 [84]。

零样本与低监督评测进一步显示性能高度任务依赖。四模型零样本比较中，细胞类型注释多数数据集由传统基线最强，蛋白表达预测基础模型更准（SCimilarity 误差最低、Transcriptformer 相关性最高），数据整合基础模型中等而 scVI 更佳 [85]。七模型低监督比较给出更细的计数：CellPLM 在聚类、注释、批次校正领先，scMulan 扰动预测领先，PCA 重建领先；7 个基础模型中仅 1 个聚类、3 个批次校正、4 个注释、0 个重建、6 个扰动预测超过最强经典基线，且跨模型基因关系一致性未超过维度匹配随机投影零假设 [86]。VCBench 把四个虚拟细胞框架综合为七个能力维度，在五个可测维度上预注册线性/最近邻基线，结果基线在 **5 维中 4 维**追平或超越所有基础模型，仅 TranscriptFormer 在 RNA 到蛋白预测上超最强基线 **53% Pearson**，而多尺度整合与 in silico 实验两维度结构上无法端到端测试 [17]。统一框架评测六个单细胞/空间模型也得出无模型全面领先，排名随模态、预处理、token 化、生物先验、域偏移和指标变化 [87]。

细胞类型分类上的模型排名同样不一致。生物学驱动的评测引入 AIDA v2 独立数据集与细胞本体指标，发现零样本嵌入确实捕捉生物学信息，但预训练模型在部分场景未超越 HVG、Seurat、Harmony、scVI 等简单基线 [88]。更激进的结论来自无参数流程：依赖精细归一化与线性方法的简单可解释流程在多个常用基准取得 SOTA 或近 SOTA，并在新细胞类型与未见物种的分布外任务上超越基础模型 [46]。

可解释性方面出现了明确的否定性证据。两层评估框架在两种架构、四种细胞类型、两种扰动模态下做 **153 项统计检验**并配合因果消融，发现注意力边分数对扰动靶标预测相对基因级特征无增量价值，单变量基因级基线反而更优，TRRUST 头因果消融也无行为效应 [89]。GRN 重建的统一基准则给出较正面但分化的结果：严格零样本下 scGPT token 嵌入相似度在 STRING 和 ChIP-seq 参考上超越经典基线，动态转移探测中 scFoundation 整体最强 [90]。两者并不直接矛盾——前者检验的是注意力边分数对扰动靶标的预测增量，后者检验的是 token 嵌入对参考网络的恢复——但共同提示“注意力即调控”的解读需要按信号来源拆开审视 [89][90]。

评测方法学本身正在成为独立议题。无监督框架基于“忠实表征应在模拟技术与采样变异的扰动下保持邻域结构”，测试 5 个 scFM、PCA 基线与 39 个数据集，发现标准基准判定近乎等价的模型在丢弃 **5%** 计数时局部邻域保持差异近 **2 倍**，且该不稳定性具尺度依赖性并被视觉连贯的嵌入掩盖 [91]。这与下游任务评测形成方法论对照：后者只能测嵌入是否恢复注释的细胞类型、批次或轨迹，无法判断结构是否可复现 [91]。

可复现性基础设施被多方视为瓶颈而非附属品。BioLLM 指出架构框架与编码标准异质、预处理不一致、接口异构和评估指标非标准化三大挑战，以统一 API、决策树预处理和 BioTask 执行器支持零样本推理与微调 [92]。scArchon 基于 Snakemake 容器化运行 trVAE、scGen、CPA、CellOT、SCREEN 等 **9 种工具**，统一 MSE、Wasserstein 及生物指标并聚合评分排名，解决环境不兼容并支持用户自有数据，但仅限非遗传扰动 [93]。数据规模也是可复现性的现实约束：JUMP 单独占 **115 TB**，JUMP-lite 以 **92.0 GB** 子集约缩小 **1,250 倍**，中度压缩基本保留信号，标准化表型活性与一致性指标揭示方法间显著性能差异 [94]。

空间组学与图像基准提供了另一条标准化路径。ST 数据集覆盖六种组织类型、跨三站点、在 Xenium 与 CosMx 上 centralized sectioning 分析，建立跨站点准确度、精密度、重复性、灵敏度与特异性指标，SpatialQM 开源、STP 门户实时评估约 **3300 万细胞**数据 [95]。小分子活性基准则暴露了任务效度问题：Hofmarcher 与 Moshkov 数据集中许多 assay 直接关联细胞健康或毒性，逻辑回归细胞计数 AUC **0.70±0.22** 接近 CLOOME 的 **0.71±0.19**，细胞计数加 MW 与 logP 达 **0.74±0.21**，但在 24 个蛋白靶标基准中 Cell Painting 确实优于细胞计数 [96]。早期整合基准仍是方法选择的参照：68 种方法与预处理组合、85 个批次、13 个图谱级任务、超 **120 万细胞**、16 种工具与 14 项指标，发现 Scanorama 和 scVI 在复杂任务表现好，有注释时 scGen 和 scANVI 最优，Harmony 和 LIGER 适合 scATAC [26]。

综合这些证据，争议的核心不在“基础模型是否有用”，而在评测能否支撑比较：污染审计、OOD 划分、指标校准、无监督稳定性与统一接口分别攻击了现有结论的不同环节，而同一模型在不同评测中的排名反转（如 Geneformer 在 [97] 中不如基线、在 [98] 中综合最佳）说明任务集合与基线选择本身就在决定结论 [97][98]。

## 6 空白与趋势

机制可解释性之外，**评测本身正在成为独立的研究对象，且结论普遍不利于“更大即更好”的叙事**。scContam 的审计显示，两个高引用基准存在大量预训练重叠证据，而截断后数据集无重叠，MIA AUROC 随模型容量数据比单调上升[15]；这意味着零样本分数可能部分来自记忆而非泛化。与此同时，参数无关的简单流程在多个常用基准上取得 SOTA 或近 SOTA，并在新细胞类型与未见物种的分布外任务上超越基础模型[46]；系统评估亦发现注意力对扰动预测无增量价值，平凡基因级基线 AUROC 0.81–0.88 优于注意力/相关性边的 0.70[13]。**这些结果共同把“预训练规模”从解释变量降格为待控制变量**，而当前多数模型报告并未区分记忆、插值与真实外推。

扰动预测的分歧则集中在指标与划分两个层面。一方面，Train Mean 基线在四个 Perturb-seq 数据集上优于 scGPT 与 scFoundation，随机森林加 GO 特征最佳[16]；K562 CRISPRa 双扰动上五个基础模型均未超过加性基线[45]。另一方面，有工作指出 MSE、Pearson Δ 等常用指标校准不良，在良好校准指标下深度学习扰动模型可优于无信息基线[32]；PerturBench 补充模式崩溃问题并主张秩指标[47]。**指标选择本身足以翻转结论**，这使得跨论文的“SOTA”声明难以直接比较，也解释了为何 STRAND[24]、SCALE[23] 等方法报告的大幅提升与基线评测的否定结论可以并存——前者在特定划分与指标下度量，后者在另一组协议下度量。

从上述证据看，该方向存在若干明确的空白与趋势：

1. **缺少同时控制预训练污染、划分方式与指标校准的统一评测**。scContam 只审计污染[15]，EL-PERTURB 只做分层 OOD 压力测试[28]，指标校准工作只针对指标[32]，三者尚未合并为单一协议。依据是各工作分别报告了污染、OOD 失效与指标不敏感，但没有一项研究同时施加三重控制后重排现有模型。

2. **位点分辨率与序列条件的扰动建模仍属少数**。STRAND 指出基因级模型将同一基因不同位点扰动坍缩为同一表征，并以调控 DNA 序列为条件把基因组覆盖从约 1.5% 扩至约 95%[24]；但现有主流扰动基准仍以基因级标签组织，位点级数据与评测几乎空白。

3. **非配对设定与分布传输正在替代细胞级匹配**。SCALE 将细胞视为无序集合、无需细胞级匹配，在 CRISPR 七项指标上超越竞争方法并经实验验证[23]；这与传统 Perturb-seq 分析默认配对或伪配对的做法形成方法分歧，但两类设定尚无同一基准下的对照。

4. **跨背景泛化缺乏原代、多供体数据支撑**。全基因组 perturb-seq 在 4 名供体、2200 万原代 CD4+ T 细胞上显示调控程序随刺激条件大幅变化[38]，而现有虚拟细胞模型多在细胞系或有限供体上训练；可信虚拟细胞路线图亦指出静态图谱与分布内基准不足以预测新条件[31]。

5. **机制可解释性与任务性能之间缺少桥接**。SAE 研究显示转录因子调控靶标特异性响应仅 6.2%[41]，电路追踪给出 CRISPRi 方向准确率 56.4%[42]，但从 scGPT 提取的造血算法却报告 |ρ|=0.439 的伪时间排序与 0.867 的 CD4/CD8 AUROC[43]。**“内部表示不含因果调控”与“可提取高性能算法”并不矛盾，但尚无工作说明何种任务性能可以从何种表示结构中可靠提取**，这是可解释性研究向实用转化的关键缺口。

6. **空间与形态基础模型的评测受平台与分割选择支配**。四平台统一评测显示灵敏度、扩散控制、细胞分割差异显著[62]，分割基准跨 5 种技术、15 个数据集亦报告指标差异显著[63]；Cell Painting 侧零样本评估中三个模型活性阳性数相近（85/90、81/90、82/90）但检索 mAP 差异显著[77]。**这意味着跨研究的性能数字不宜直接比较，而目前缺少把平台/分割不确定性传播到模型排名的评测设计**。

7. **虚拟细胞的验证仍以回顾性拟合为主**。肝脏 AIVC 综述明确指出尚无经过前瞻验证的肝脏模拟器[14]，Virtual Cell Challenge 虽提供开放循环基准[27]，但前瞻性、跨供体/病因/分期的验证体系尚未建立；可信虚拟细胞框架提出的四层经验证据链[31]目前缺少可操作的执行标准。

8. **多模态整合的收益与配对数据依赖尚未解耦**。PAST 依赖 2000 万配对病理图像与单细胞转录组[20]，OmiCLIP 明确将依赖配对 WSI 与 Visium 数据列为主要局限[19]，mSTAR 指出跨中心泛化待验证[21]；而跨模态继续预训练以 70M 参数在 48,843 个蛋白质组样本上匹配或超过 1B/3B RNA-only 模型[12]，提示**数据策展质量可能比模态数量更关键，但这一假设尚未在统一基准下检验**。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 单细胞基础模型 | 成熟（方法收敛、增量为主） | scGPT [1] 与 Geneformer [2] 已确立"大规模预训练 + 迁移"范式并被广泛复用；但 GenePT [52] 用简单基因文本嵌入即达到可比效果，说明架构红利在收窄；评测侧 [98] 系统评估显示基础模型在下游任务上相对简单基线优势有限。方法已收敛、增量工作为主。 |
| 2.2 空间与多模态模型 | 朝阳（近两年爆发、方法未收敛） | MultiVI [39] 与 moscot [61] 分别代表多模态生成整合与时空映射两条尚未统一的路线；AD 多模态图谱 [99] 显示大规模多模态整合已有 CNS 级落地，但 Cell Painting 综述 [65] 指出形态模态的表示与评测仍开放。方法未收敛。 |
| 2.3 扰动响应与虚拟细胞 | 朝阳（近两年爆发、CNS 频出、方法未收敛） | 早期 Perturb-seq [33] 与单细胞 CRISPR 筛选 [34] 奠定数据基础；2024 年虚拟细胞路线图 [29] 提出框架但未给收敛方法；同时 [45] 明确报告深度扰动预测**未跑赢简单基线**，说明核心问题仍开放。 |
| 2.4 机制可解释性与表征分析 | 萌芽（少量探索性工作） | 稀疏自编码器揭示单细胞基础模型可解释特征 [73] 与系统性可解释性评测 [13] 均显示"有组织生物知识但调控信息有限"，属早期探索；scGPT 流形发现 [43] 提供表征提取方法但样本极少。证据仅 2 篇以上但均为 2026 年预印本、零引用，判为萌芽。 |
| 2.5 形态与图像表型基础模型 | 萌芽（少量探索性工作） | pooled Cell Painting CRISPR 平台 [76] 与图像 profiling 挑战综述 [79] 显示该方向刚起步、评测标准未定；检索式特征空间评估 [77] 指出不同特征空间差异显著。证据少且新。 |
| 3 数据与资源 | 成熟（方法收敛、增量为主） | 全基因组 Perturb-seq 图谱 [35] 与遗传互作流形 [81] 已建立规模化数据生产范式；Human Cell Atlas 向统一基础模型演进 [49] 表明资源侧进入整合与标准化阶段，增量为主。 |
| 5 评测、可复现性与争议 | 朝阳（近两年爆发、方法未收敛） | atlas 级整合基准 [26] 确立评测范式；PerturBench [47] 与"深度扰动预测未超基线" [45] 形成对虚拟细胞核心主张的批判性证据，评测口径仍在快速演化、未收敛。 |

**整体判断**：这个方向整体处于**朝阳期偏后段**——单细胞基础模型（2.1）与数据资源（3）已进入**成熟/增量**阶段，架构红利收窄；真正的窗口在**扰动响应与虚拟细胞（2.3）、空间多模态（2.2）、以及评测与可解释性（2.4/2.5/5）**，这些子方向方法未收敛、且刚出现"没跑赢基线"的硬证据 [45]，意味着**问题定义与评测**比再训一个大模型更有价值。窗口期估计**12–24 个月**：一旦虚拟细胞评测标准（PerturBench 类 [47]）与 Tahoe 级数据成为公共默认，纯方法增量会被迅速商品化。最大不确定性是**扰动预测的可泛化性是否真实存在**——若"未超基线"结论在更多数据上复现，整个虚拟细胞叙事需要从"预测"转向"表征 + 检索 + 机制解释"。

**接下来怎么做**：

1. **做"衰老 × 扰动"的评测与基准，而不是再训基础模型**。用公共 Perturb-seq / Tahoe 级数据 + 你自己的衰老队列，构建按"基因/通路/细胞状态"分层的泛化评测，复现并扩展 [45] 与 [47] 的负结果。现在做是因为评测口径尚未固化、且批判性结果刚被 CNS 子刊接受，**低成本高可见度**；产出是可复现 benchmark + 一篇"什么条件下扰动预测有效"的方法学论文。

2. **把类器官多组学做成"多模态整合"的验证场景**。用 MultiVI [39] 与 moscot [61] 作为基线，在你的类器官 RNA + 蛋白 + 空间数据上做跨模态对齐与时空映射，重点回答"整合是否保留衰老相关状态"。现在做是因为 2.2 方法未收敛、CNS 级多模态图谱 [99] 已证明场景价值，而类器官数据是稀缺的**纵向 + 干预**资源。

3. **切入可解释性：用稀疏自编码器分析你手上的基础模型表征**。直接复用 [73] 与 [13] 的 SAE 流程，在 scGPT/Geneformer 表征上检验"衰老轴"是否是可分离的线性特征，并对照 [43] 的流形提取方法。现在做是因为 2.4 仅 **8 篇、零引用**，属萌芽，**先发优势明显**，且与你多模态建模技能高度匹配。

4. **用 Cell Painting / 形态数据补上"非转录组"模态**。以 [76] 的 pooled Cell Painting CRISPR 平台为模板，在类器官或细胞系上做形态 + 转录组配对，检验形态特征能否作为扰动响应的低成本代理。现在做是因为 2.5 仅 **5 篇**、评测标准未定 [79]，且形态数据成本远低于 Perturb-seq，适合公共数据 demo 快速起量。

5. **把衰老作为"分布外泛化"的天然测试床**。用 Human Cell Atlas 类资源 [49] 与衰老图谱做跨年龄迁移，检验基础模型在**年龄偏移**下的表征稳定性——这是当前评测 [98] 未覆盖的维度。现在做是因为 2.1 已成熟、增量空间小，但"衰老 OOD"这一角度尚无人系统做，能把你的领域优势转成方法学贡献。

## 参考文献

1. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. Nature Methods 2024. https://doi.org/10.1038/s41592-024-02201-0
2. Transfer learning enables predictions in network biology. Nature 2023. https://doi.org/10.1038/s41586-023-06139-9
3. CellFM: a large-scale foundation model pre-trained on transcriptomics of 100 million human cells.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59926-5
4. scPRINT-2: Towards the next-generation of cell foundation models and benchmarks.  2025. https://doi.org/10.64898/2025.12.11.693702
5. Evaluating the role of pretraining dataset size and diversity on single-cell foundation model performance.. Nature methods 2026. https://doi.org/10.1038/s41592-026-03120-y
6. Zero-shot evaluation reveals limitations of single-cell foundation models.. Genome biology 2025. https://doi.org/10.1186/s13059-025-03574-x
7. Intermediate Layers Encode Optimal Biological Representations in Single-Cell Foundation Models.  2026. https://arxiv.org/abs/2604.14838v1
8. RegFormer: a single-cell foundation model powered by gene regulatory hierarchies.. Nature communications 2026. https://doi.org/10.1038/s41467-026-72198-x
9. A cell atlas foundation model for scalable search of similar human cells.. Nature 2024. https://doi.org/10.1038/s41586-024-08411-y
10. CellWorld: From Gene-Level Reconstruction to Latent Cell Prediction in Spatial Transcriptomics Foundation Models.  2026. https://arxiv.org/abs/2608.06659v1
11. Tahoe-x1: Scaling Perturbation-Trained Single-Cell Foundation Models to 3 Billion Parameters. bioRxiv 2025. https://doi.org/10.1101/2025.10.23.683759
12. Single-cell foundation models benefit from cross-modal training: adding proteomics data beats parameter scaling. bioRxiv 2026. https://doi.org/10.64898/2026.08.14.744845
13. Systematic Evaluation of Single-Cell Foundation Model Interpretability Reveals Attention Captures Co-Expression Rather Than Unique Regulatory Signal.  2026. https://arxiv.org/abs/2602.17532v1
14. Toward AI Virtual Cells for Hepatology: Representation, Generation, Dynamics, and Intervention in Single-Cell Models.. Clinical and Molecular Hepatology 2026. https://doi.org/10.3350/cmh.2026.0820
15. Auditing pretraining contamination in single-cell foundation model benchmarks.  2026. https://arxiv.org/abs/2607.20572v1
16. Benchmarking foundation cell models for post-perturbation RNA-seq prediction.. BMC genomics 2025. https://doi.org/10.1186/s12864-025-11600-2
17. VCBench: A Multi-Dimensional Benchmark for Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.06.18.733146
18. Single-cell foundation models: bringing artificial intelligence into cell biology.. Experimental & molecular medicine 2025. https://doi.org/10.1038/s12276-025-01547-5
19. A visual-omics foundation model to bridge histopathology with spatial transcriptomics.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02707-1
20. PAST: A multimodal single-cell foundation model for histopathology and spatial transcriptomics in cancer. arXiv.org 2025. https://arxiv.org/abs/2507.06418v1
21. A multimodal knowledge-enhanced whole-slide pathology foundation model.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66220-x
22. NexuST: A Hierarchical Foundation Model for Spatial Transcriptomics.  . https://doi.org/10.64898/2026.09.22.753590
23. SCALE:Scalable Conditional Atlas-Level Endpoint transport for virtual cell perturbation prediction.  2026. https://arxiv.org/abs/2603.17380v3
24. STRAND: Sequence-Conditioned Transport for Single-Cell Perturbations.  2026. https://arxiv.org/abs/2602.10156v1
25. Chreode: A Cell World Model for One-Step Temporal Dynamics and Perturbation Prediction. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.28111
26. Benchmarking atlas-level data integration in single-cell genomics. Nature Methods 2020. https://doi.org/10.1038/s41592-021-01336-8
27. Virtual Cell Challenge: Toward a Turing test for the virtual cell.. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.008
28. Genetic Perturbation Prediction Models Fail Out-of-Distribution: A Rigorous Benchmark and Systematic Evaluation.  . https://doi.org/10.64898/2026.10.16.759604
29. How to build the virtual cell with artificial intelligence: Priorities and opportunities.. Cell 2024. https://doi.org/10.1016/j.cell.2024.11.015
30. Human interpretable grammar encodes multicellular systems biology models to democratize virtual cell laboratories.. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.048
31. Toward trustworthy virtual cells: a roadmap for perturbation-resolved, context-aware, and experimentally validated cell models. Frontiers in Cell and Developmental Biology 2026. https://doi.org/10.3389/fcell.2026.1900624
32. Deep learning perturbation models can outperform baselines on calibrated metrics.. Nature biotechnology . https://doi.org/10.1038/s41587-026-03307-w
33. Perturb-seq: Dissecting molecular circuits with scalable single cell RNA profiling of pooled genetic screens. Cell 2016. https://doi.org/10.1016/j.cell.2016.11.038
34. Pooled CRISPR screening with single-cell transcriptome read-out. Nature Methods 2017. https://doi.org/10.1038/nmeth.4177
35. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. bioRxiv 2021. https://doi.org/10.1016/j.cell.2022.05.013
36. Simultaneous CRISPR screening and spatial transcriptomics reveal intracellular, intercellular, and functional transcriptional circuits.. Cell 2025. https://doi.org/10.1016/j.cell.2025.02.012
37. Abstract 491: A 100 million cell single cell atlas enabling mechanistic and genotype-specific drug response discovery.. Cancer Research 2026. https://doi.org/10.1158/1538-7445.am2026-491
38. Genome-scale perturb-seq in primary human CD4+ T cells maps context-specific regulators of T cell programs and human immune traits.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.002
39. MultiVI: deep generative model for the integration of multimodal data. Nature Methods 2023. https://doi.org/10.1038/s41592-023-01909-9
40. CLM-X: A multimodal single-cell foundation model with flexible multi-way Transformer for unified scRNA-seq and scATAC-seq analysis. bioRxiv 2026. https://doi.org/10.64898/2026.02.17.704943
41. Sparse autoencoders reveal organized biological knowledge but minimal regulatory logic in single-cell foundation models: a comparative atlas of Geneformer and scGPT.  2026. https://arxiv.org/abs/2603.02952v1
42. Causal Circuit Tracing Reveals Distinct Computational Architectures in Single-Cell Foundation Models: Inhibitory Dominance, Biological Coherence, and Cross-Model Convergence.  2026. https://arxiv.org/abs/2603.01752v2
43. Discovery of a Hematopoietic Manifold in scGPT Yields a Method for Extracting Performant Algorithms from Biological Foundation Model Internals.  2026. https://arxiv.org/abs/2603.10261v1
44. Towards Universal Gene Regulatory Network Inference: Unlocking Generalizable Regulatory Knowledge in Single-cell Foundation Models.  2026. https://arxiv.org/abs/2605.08128v1
45. Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02772-6
46. Parameter-free representations outperform single-cell foundation models on downstream benchmarks.  2026. https://arxiv.org/abs/2602.16696v1
47. PerturBench: Benchmarking Machine Learning Models for Cellular Perturbation Analysis. Neural Information Processing Systems 2024. https://doi.org/10.48550/arXiv.2408.10609
48. Single-cell dissection of immune-state architecture across diverse human population cohorts.  . https://doi.org/10.64898/2026.11.17.26366584
49. The Human Cell Atlas from a cell census to a unified foundation model.. Nature 2024. https://doi.org/10.1038/s41586-024-08338-4
50. A Cross-Species Generative Cell Atlas Across 1.5 Billion Years of Evolution: The TranscriptFormer Single-cell Model. bioRxiv 2025. https://doi.org/10.1101/2025.04.25.650731
51. scDifformer: diffusion-based post-training for virtual cell modeling across large-scale single-cell data. Nucleic Acids Research 2026. https://doi.org/10.1093/nar/gkag706
52. GenePT: A Simple But Effective Foundation Model for Genes and Cells Built From ChatGPT. bioRxiv 2023. https://doi.org/10.1101/2023.10.16.562533
53. Scalable querying of human cell atlases via a foundational model reveals commonalities across fibrosis-associated macrophages. bioRxiv 2023. https://doi.org/10.1101/2023.07.18.549537
54. Deep generative modeling of sample-level heterogeneity in single-cell genomics.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02808-x
55. Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling.  . https://doi.org/10.64898/2026.09.22.752128
56. LucaCell: a sequence-centric foundation model for cross-species single-cell analysis.  . https://doi.org/10.21203/rs.3.rs-11151765/v1
57. EpiZoo: a DNA sequence-aware foundation model for cross-species single-cell epigenomics.  . https://doi.org/10.64898/2026.09.24.754017
58. ProtCell: a foundation model for single-cell proteomics.  . https://doi.org/10.64898/2026.10.22.760932
59. Emerging frontiers for AI in single-cell genomics.. Molecular cell . https://doi.org/10.1016/j.molcel.2026.09.014
60. VINTER: a generative vision-language model for annotating and interrogating spatial tissues.  . https://doi.org/10.64898/2026.10.01.752251
61. Mapping cells through time and space with moscot.. Nature 2025. https://doi.org/10.1038/s41586-024-08453-2
62. Systematic benchmarking of high-throughput subcellular spatial transcriptomics platforms across human tumors.. Nature communications 2025. https://doi.org/10.1038/s41467-025-64292-3
63. Benchmarking segmentation methods for spatial transcriptomics.. Nature methods . https://doi.org/10.1038/s41592-026-03272-x
64. A clinical benchmark of public self-supervised pathology foundation models.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58796-1
65. Cell Painting: a decade of discovery and innovation in cellular imaging.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02528-8
66. A multiplexed single-cell CRISPR screening platform enables systematic dissection of the unfolded protein response. Cell 2016. https://doi.org/10.1016/j.cell.2016.11.048
67. Predicting transcriptional responses to novel chemical perturbations using deep generative model for drug discovery.. Nature communications 2024. https://doi.org/10.1038/s41467-024-53457-1
68. PerturbNet predicts single-cell responses to unseen chemical and genetic perturbations.. Molecular systems biology 2025. https://doi.org/10.1038/s44320-025-00131-3
69. Deep dynamical models of single-cell multiomic velocities predict loss-of-function and rescue perturbations in B cells.. Nature biotechnology . https://doi.org/10.1038/s41587-026-03348-1
70. A deep generative model for deciphering cellular dynamics and in silico drug discovery in complex diseases.. Nature biomedical engineering 2025. https://doi.org/10.1038/s41551-025-01423-7
71. AROMA: Augmented Reasoning Over a Multimodal Architecture for Virtual Cell Genetic Perturbation Modeling.  2026. https://arxiv.org/abs/2604.20263v1
72. AI-driven virtual cell models in preclinical research: technical pathways, validation mechanisms, and clinical translation potential.. NPJ digital medicine 2025. https://doi.org/10.1038/s41746-025-02198-6
73. Sparse Autoencoders Reveal Interpretable Features in Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.1101/2025.10.22.681631
74. Exhaustive Circuit Mapping of a Single-Cell Foundation Model Reveals Massive Redundancy, Heavy-Tailed Hub Architecture, and Layer-Dependent Differentiation Control.  2026. https://arxiv.org/abs/2603.11940v1
75. CauTrigger: deciphering biological system state transitions by hierarchical causal decomposition.. Nature methods . https://doi.org/10.1038/s41592-026-03274-9
76. A pooled Cell Painting CRISPR screening platform enables de novo inference of gene function by self-supervised deep learning.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66778-6
77. Retrieval-Based Evaluation of Cell Painting Feature Spaces Reveals Differences in the Preservation of Biologically Meaningful Phenotypic Similarity.. International journal of molecular sciences 2026. https://doi.org/10.3390/ijms27135727
78. Advancing morphological profiling with self-supervised learning through comparative insights into representation learning of cellular perturbations.. Nature methods . https://doi.org/10.1038/s41592-026-03270-z
79. Progress and new challenges in image-based profiling.. Molecular systems biology 2026. https://doi.org/10.1038/s44320-026-00197-7
80. PerturbBridge: Direct Phenotypic Supervision for Cellular Perturbation Generation.  . https://arxiv.org/abs/2610.17066
81. Exploring genetic interaction manifolds constructed from rich single-cell phenotypes. Science 2019. https://doi.org/10.1126/science.aax4438
82. A molecularly defined and spatially resolved cell atlas of the whole mouse brain. bioRxiv 2023. https://doi.org/10.1101/2023.03.06.531348
83. PertEval-scFM: Benchmarking Single-Cell Foundation Models for Perturbation Effect Prediction. bioRxiv 2025. https://doi.org/10.1101/2024.10.02.616248
84. Benchmarking algorithms for generalizable single-cell perturbation response prediction.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02980-0
85. Benchmarking single-cell foundation models in a zero-shot setting. bioRxiv 2026. https://doi.org/10.64898/2026.08.03.739553
86. Task-dependent Performance of Single-cell Foundation Models under Low Supervision. bioRxiv 2026. https://doi.org/10.64898/2026.04.01.714123
87. Harmonised benchmarking of foundation models for single-cell and spatial transcriptomics reveals context-dependent generalisation.  2026. https://arxiv.org/abs/2607.17227
88. Biology-driven insights into the power of single-cell foundation models. Genome Biology 2025. https://doi.org/10.1186/s13059-025-03781-6
89. Systematic evaluation of single-cell foundation model interpretability: attention-derived edge scores add no incremental value over gene-level features for perturbation-target prediction. BMC Genomics 2026. https://doi.org/10.1186/s12864-026-12965-8
90. Benchmarking Static Gene Regulatory Network Reconstruction and Dynamic Transition Probing in Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.05.17.725083
91. Robustness to nuisance perturbations enables unsupervised evaluation of single-cell foundation models. bioRxiv 2026. https://doi.org/10.64898/2026.08.22.746357
92. BioLLM: A standardized framework for integrating and benchmarking single-cell foundation models. bioRxiv 2024. https://doi.org/10.1016/j.patter.2025.101326
93. scArchon: a scalable benchmarking framework for assessing single-cell perturbation models.. Genome biology 2026. https://doi.org/10.1186/s13059-026-04104-z
94. JUMP-lite: Compact, reproducible benchmarking of cell representations.  2026. https://arxiv.org/abs/2608.07632
95. Standardized metrics for assessment and reproducibility of imaging-based spatial transcriptomics datasets.. Nature biotechnology 2025. https://doi.org/10.1038/s41587-025-02811-9
96. Counting cells can accurately predict small-molecule bioactivity benchmarks.. Nature communications 2026. https://doi.org/10.1038/s41467-026-68725-5
97. A Systematic Evaluation of Single-Cell Foundation Models on Cell-Type Classification Task. Web Search and Data Mining 2025. https://doi.org/10.1145/3701551.3708811
98. Evaluating the Utilities of Foundation Models in Single‐Cell Data Analysis. bioRxiv 2024. https://doi.org/10.1101/2023.09.08.555192
99. Integrated multimodal cell atlas of Alzheimer's disease.. Nature neuroscience 2024. https://doi.org/10.1038/s41593-024-01774-5
100. Efficient Fine-Tuning of Single-Cell Foundation Models Enables Zero-Shot Molecular Perturbation Prediction.  2024. https://arxiv.org/abs/2412.13478v2
101. PTM-Mamba: a PTM-aware protein language model with bidirectional gated Mamba blocks.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02656-9
