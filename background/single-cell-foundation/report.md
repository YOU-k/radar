# 单细胞与空间组学基础模型与虚拟细胞 · 方向背景报告

证据 97 篇 · 覆盖度 0.65 · 第 10 轮 · 更新 2026-10-25 · 数字核验删句 1

## 本次变更

- 新增 [50] Emerging frontiers for AI in single-cell genomics.
- 新增 [89] Genetic Perturbation Prediction Models Fail Out-of-Distribution: A Rigorous Benchmark and Systematic Evaluation
- 新增 [63] Deep dynamical models of single-cell multiomic velocities predict loss-of-function and rescue perturbations in B cells.
- 新增 [69] CauTrigger: deciphering biological system state transitions by hierarchical causal decomposition.

## 摘要（TL;DR）

- scGPT 在超 **3300 万个细胞**上预训练，经迁移学习后在注释、多批次/多组学整合、扰动预测和基因网络推断等任务上表现优异 [1]。
- Geneformer 在约 **3000 万个单细胞转录组**上以自监督方式学习网络层级，微调后在染色质与网络动力学任务中持续提升准确率，并在有限患者数据下识别出心肌病候选治疗靶点 [2]。
- CellFM 预训练于 **1 亿人类细胞**，在多种任务上达到或超过 Geneformer、scGPT、scFoundation、UCE 等模型 [3]。
- RegFormer 改用融合基因调控网络先验的 Mamba 状态空间架构，在 **2500 万人类细胞**上预训练，在细胞注释、GRN 重建、遗传扰动预测和药物响应建模等基准上持续优于 scGPT 和 Geneformer [4]。
- TranscriptFormer 在多达 **1.12 亿细胞、12 个物种、跨越 15.3 亿年进化**的数据上联合建模基因身份与表达水平，分布内与分布外细胞类型分类达 SOTA，可零样本识别疾病状态并跨物种转移注释 [5]。
- GenePT 用 GPT-3.5 基于 NCBI 基因文本描述生成基因嵌入，无需数据策展与预训练，在基因属性与细胞类型分类等任务上达到与 Geneformer 等相当甚至更优的性能 [6]。
- 零样本评估在 5 个数据集（如 Pancreas 16k、PBMC 12k）上比较 Geneformer 和 scGPT 与 HVG、Harmony、scVI，发现两者在 AvgBIO 上多低于这些简单基线，HVG 在所有指标上优于二者 [7]。
- 一项用 **2220 万细胞**语料预训练 **400 个模型**、开展 **6400 次实验**的研究发现，性能在数据规模远小于当前训练语料时即趋于平台，未观察到明确的数据缩放定律 [8]。
- CellWorld 将预测目标改为被掩码细胞的潜在表征，采用 JEPA 式潜在空间预测预训练，在 **4600 万细胞、3 平台 11 器官**上训练 4 个变体（5.74M–94.56M 参数）[9]。
- 因果电路追踪在 Geneformer V2-316M 与 scGPT 的 4 个条件、**96,892 条边、80,191 次前向**上发现两模型约 **53% 生物一致性**、**65–89% 抑制主导**，但 CRISPRi 基因级验证的方向准确率仅 **56.4%** [10]。

## 1 背景与定义

单细胞与空间组学基础模型的边界，首先由“预训练—迁移”范式划定：模型在海量细胞图谱上以自监督方式学习通用表征，再经微调或适配器迁移到注释、整合、扰动预测等下游任务 [1] [2] [11]。这一范式的合法性来自图谱规模的持续扩张——从数千万细胞到亿级人类细胞 [3]，以及跨物种、跨模态语料的引入 [5] [12]。但“基础模型”与“虚拟细胞”并非同义词：前者是可迁移的表征提取器，后者要求对未观测扰动下的细胞状态作出可验证的预测 [13] [14]。**本方向的核心张力正在于此：表征学习的成功并不自动转化为扰动预测的因果能力。**

演化脉络上，三条线索交织推进。其一是**规模与架构的分化**：Transformer 路线之外出现状态空间架构 [4]、扩散后训练 [15] 与潜在空间预测目标 [9]，同时有工作质疑数据缩放的收益是否已饱和 [8]。其二是**模态扩展**：从 RNA-only 走向 RNA+ATAC+蛋白 [16] [17]、病理图像与空间转录组配对 [18] [19] [20]，以及 Cell Painting 形态表型 [21] [22]。其三是**扰动数据与基准的基础设施化**：从 Perturb-seq 的原始范式 [23] [24] 到基因组规模筛选 [25]、空间扰动读出 [26] 与亿级化合物扰动图谱 [27]，再到 Virtual Cell Challenge 这类开放循环基准 [28]。

**“虚拟细胞”的定义边界需要与三类邻近工作区分。** 第一类是图谱检索与整合模型：SCimilarity 提供跨研究细胞相似度查询 [29]，moscot 提供时空最优传输映射 [30]，它们刻画“细胞在哪里”，但不预测“扰动后细胞去哪里”。第二类是纯生成式表达预测：PRnet、PerturbNet、UNAGI 等直接建模扰动后分布 [31] [32] [33]，属于虚拟细胞的建模范畴，但多数缺乏跨条件泛化验证。第三类是机制性 agent-based 模型，用可解释规则而非大数据拟合构建细胞行为 [34]，与数据驱动路线构成方法论对照。**本报告采纳的边界是：须有公开权重或代码、须以扰动响应预测或细胞状态生成为核心任务、须在跨条件设置下评测**；单一数据集流程改良与小规模应用案例不纳入。

核心问题可归纳为四组，且已有证据显示它们尚未被解决。**(1) 规模是否等于能力**：RNA-only 参数缩放与跨模态数据引入的收益对比在同一研究内部出现不利于纯缩放的证据 [35]，而数据缩放定律在单细胞语料上未获明确支持 [8]。**(2) 表征是否编码因果调控**：SAE 与电路追踪一致显示模型内化了有组织的生物学知识，但转录因子靶标特异性仅 **6.2%** [36]，CRISPRi 方向准确率仅 **56.4%** [10]，注意力对扰动预测无增量价值 [37]。**(3) 简单基线是否已被超越**：多个独立评测报告 Train Mean、随机森林加 GO 特征、甚至纯线性流程在扰动预测与分布外任务上追平或超越基础模型 [38] [39] [40]。**(4) 评测是否可信**：预训练污染审计显示高引用基准存在大量重叠证据 [41]，而统一多模型评测中排名随模态、预处理与指标大幅变化 [42]。**这四组问题共同界定了本方向的当前前沿：不是“能否做出更大的模型”，而是“能否给出跨条件可验证、且跑得赢基线的扰动预测”。**

## 2 方法学


### 2.1 单细胞基础模型

单细胞基础模型的主流路线，是用 Transformer 在千万至亿级细胞转录组上做自监督预训练，再把通用表征迁移到注释、整合、扰动预测等下游任务。**scGPT** 在超 **3300 万个细胞**上预训练，经迁移学习后在注释、多批次/多组学整合、扰动预测和基因网络推断等任务上表现优异 [1]；**Geneformer** 在约 **3000 万个单细胞转录组**上以自监督方式学习网络层级，微调后在染色质与网络动力学任务中持续提升准确率，并在有限患者数据下识别出心肌病候选治疗靶点 [2]。两者都把细胞类比为句子、基因类比为词元 [11]。规模继续扩张：**CellFM** 预训练于 **1 亿人类细胞**，在多种任务上达到或超过 Geneformer、scGPT、scFoundation、UCE 等模型 [3]；**scPRINT-2** 覆盖 **3.5 亿细胞、16 个物种**，在表达去噪、细胞嵌入和细胞类型预测上达到 SOTA，并具备表达插补与反事实推理的生成能力 [43]。

架构上的分化体现在对先验知识和序列长度的处理。**RegFormer** 认为 Transformer 存在可扩展性与上下文长度限制，改用融合基因调控网络先验的 Mamba 状态空间架构，在 **2500 万人类细胞**上预训练，在细胞注释、GRN 重建、遗传扰动预测和药物响应建模等基准上持续优于 scGPT 和 Geneformer [4]。**scDifformer** 则在 Transformer 上叠加去噪扩散模块与专门的后训练阶段，三阶段设计在 7 个组织和多项独立研究中提升跨数据集表现，尤其在强批次效应下，并在空间转录组 spot 去卷积上表现优异 [15]。这些工作共同把目标从判别式任务推向虚拟细胞建模。

跨物种与跨模态是另一条扩展轴。**TranscriptFormer** 在多达 **1.12 亿细胞、12 个物种、跨越 15.3 亿年进化**的数据上联合建模基因身份与表达水平，分布内与分布外细胞类型分类达 SOTA，可零样本识别疾病状态并跨物种转移注释，发育轨迹与系统发育关系自然涌现 [5]。**Speciesformer** 在含 **1.31 亿细胞**的 SpeciesCorpus 上预训练，目标是把进化表征学习与虚拟细胞状态生成结合，区分保守生物学原理与物种、组织及细胞环境特异变异，但摘要未给出定量基准结果 [44]。**LucaCell** 不以固定基因注释而以预训练 mRNA 序列嵌入表示基因，将表达离散化为 bin 后用 Transformer 编码，在 **8500 万人类和小鼠单细胞**上预训练，实现人、小鼠、狐猴肾脏数据的跨物种跨模态细胞类型迁移，并做到无比对微生物嵌入、区分 **50 多种细菌**且保留种内结构 [12]。**EpiZoo** 把这一思路延伸到表观组，将百万维单细胞表观基因组谱转换为紧凑的“细胞句子”，以摆脱对基因组坐标的依赖和单一物种局限 [45]。

检索式路线追求的是统一可比的细胞相似度。**SCimilarity** 用深度度量学习同时优化监督三元组损失和无监督重构损失，早期版本在 **2270 万细胞、399 项研究**上训练，验证了跨组织查询能力——最初在间质性肺病中识别的巨噬细胞亚群也存在于其他纤维化疾病、组织和 3D 水凝胶系统中 [46]；后续版本报告 **2340 万细胞、412 项研究、56 训练/15 测试数据集**，在查询敏感性与整合性能间取得最佳平衡（**β=0.001**），但依赖 Cell Ontology 注释质量，部分细胞类型关系模糊 [29]。与之相对，**GenePT** 质疑大规模表达预训练的必要性：它用 GPT-3.5 基于 NCBI 基因文本描述生成基因嵌入，再经表达加权或基因名句子嵌入得到单细胞嵌入，无需数据策展与预训练，在基因属性与细胞类型分类等任务上达到与 Geneformer 等相当甚至更优的性能 [6]。

对上述模型的严格评估揭示了明显争议。零样本评估在 5 个数据集（如 Pancreas 16k、PBMC 12k）上比较 Geneformer 和 scGPT 与 HVG、Harmony、scVI，发现两者在 AvgBIO 上多低于这些简单基线，HVG 在所有指标上优于二者，scGPT 仅在 PBMC 12k 上部分优于 scVI/Harmony [7]。关于“堆数据”是否有效，一项用 **2220 万细胞**语料预训练 **400 个模型**、开展 **6400 次实验**的研究发现，性能在数据规模远小于当前训练语料时即趋于平台，未观察到明确的数据缩放定律，建议平衡模型容量、数据规模与算力 [8]。表征提取方式同样被质疑：对 scFoundation（**100M 参数**）和 Tahoe-X1（**1.3B 参数**）的逐层评估显示，轨迹推断最优层在 **60% 深度**、比最终层高 **31%**，扰动预测最优层随 T 细胞激活状态在 **0–96%** 间漂移，静息细胞首层反而最佳，而常规做法默认取最终层 [47]。

除细胞表征外，样本级异质性与蛋白序列也被纳入基础模型视野。**MrVI** 用层次深度生成模型和交叉注意力建模样本协变量效应，无需先验聚类即可识别样本分组，实现高分辨无注释差异表达与丰度分析并控制批次，整合性能领先，已在 scvi-tools 中提供 [48]。**PTM-Mamba** 用双向门控 Mamba 块融合 ESM-2 与翻译后修饰嵌入，以 **79,707 条修饰序列**（源自 **311,350 条 Swiss-Prot PTM 记录**）训练，收敛快于 PTM-Transformer 基线，能区分修饰与野生型序列 [49]。

综述层面的判断则提醒落地差距：早期 scRNA-seq 嵌入模型和基础模型在实验生物学家中应用有限，但随着大规模单细胞图谱积累，利用 AI 在庞大数据背景下解读新数据集的需求明确，单细胞表观/多组学检测和 Perturb-seq 带来新的建模机会 [50]；当前 scFMs 仍有限制，需改进性能与生物学实用性 [11]。

### 2.2 空间与多模态模型

空间转录组基础模型的预训练目标正在从“重建观测基因”转向“预测潜在表征”。CellWorld 指出，既有模型主要重建被掩码的基因身份或表达值，可能鼓励复制测定特异的技术变异、限制表征迁移性，因此将预测目标改为被掩码细胞的潜在表征，采用 JEPA 式潜在空间预测预训练，在 **4600 万细胞、3 平台 11 器官**上训练 4 个变体（5.74M–94.56M 参数）[9]。其结果显示 **CellWorld-Small（5.74M）在全部 11 个线性探针和 7 个空间基准上超越所有基线**，且仅用 5% 语料的冻结 Large 模型在 7 个空间基准上超越全部微调基线；作者强调空间迁移依赖生物来源多样性与充分优化，而非细胞数量[9]。与之不同，NexuST 走分层路线，反复交错基因级分子建模与细胞级空间建模，使两个层级在端到端预训练中相互优化，并构建 **HumanST-46M（72 个数据集、11 个器官、三种成像平台、4570 万人类细胞）**，在四个留出数据集约 260 万细胞上于细胞类型注释、区域预测、基因恢复等任务达到 SOTA 或具竞争力[51]。两者都强调大规模空间语料，但前者以潜在表征为预测目标、后者以层级交错建模为架构核心，尚未见直接对比。

病理图像与空间转录组的跨模态对齐形成了另一条主线。PAST 在 **2000 万配对病理图像与单细胞转录组**上训练泛癌单细胞基础模型，联合编码细胞形态与基因表达，学习统一跨模态表征，支持单细胞基因表达预测、虚拟分子染色和多模态生存分析，并在多种癌症下游任务中超越现有方法[18]。OmiCLIP 则以 CLIP 对比学习对齐 H&E 图像与由高表达基因符号拼接成的“基因句子”，基于 **ST-bank 的 220 万组织 patch（1007 样本、32 器官）**，配套 Loki 平台提供组织对齐、注释、细胞分解、检索与基因表达预测五项功能，在 5 个模拟、19 个公开和 4 个内部数据集上对比 22 种 SOTA 方法[19]。mSTAR 进一步把模态扩展到三种：病理切片、专家报告与基因表达，用 **26,169 切片-模态对、10,275 患者、32 癌种、1.16 亿 patch** 做两阶段预训练（先切片级对比学习训练聚合器，再把全切片上下文注入 patch 特征提取器），在 15 类 97 项任务中表现优异，并显示多模态预训练可用更少数据达到竞争性能[20]。三者都依赖配对数据，OmiCLIP 明确其泛化受限于配对 WSI 与 Visium 数据[19]，mSTAR 亦指出跨中心泛化仍需验证[20]。

生成式视觉语言模型提供了另一种空间组织注释路径。VINTER 在 **145 万组织学-文本对**上对齐，将组织学图像、实测基因表达和空间邻域作为单一序列读取，输出每个组织类别的概率；由于基因以文本形式输入，可在固定图像下编辑分子证据，联合三源信息后其组织注释精度优于空间域方法和空间基础模型[52]。这与 PAST、OmiCLIP 的对比学习式对齐不同：VINTER 强调生成式读取与分子证据的可编辑性，而后者强调跨模态表征的判别与检索能力。

多模态单细胞整合模型处理的是同一细胞的多组学测量，与空间模型互补。MultiVI 用深度生成模型（VAE 分别建模基因表达与染色质可及性，通过惩罚对齐潜空间，并模块化扩展至表面蛋白）整合多模态与单模态数据，提供校准的不确定性估计，能准确估计缺失模态的差异表达/可及性，并在相关群体存在时实现样本外预测，已集成于 scvi-tools[16]。CLM-X 则基于多路 Transformer 与统一 token 化、分阶段掩码重建预训练，在百万级单模态与多模态数据上支持 RNA-only、ATAC-only 和配对 RNA-ATAC 输入，在 **10 个数据集**的五个下游任务上持续超越现有多模态方法与单模态基础模型，尤其在 RNA-ATAC 跨模态翻译和扰动预测上优势明显[17]。两者都面对缺失模态问题，但 MultiVI 以概率生成模型给出不确定性，CLM-X 以 Transformer 基础模型追求跨模态翻译与扰动预测，评测口径不同，不宜直接比较数值。

空间映射与评测基础设施构成上述模型的支撑层。moscot 将时序、空间和时空映射统一为 W、GW、FGW 型最优传输问题，支持多模态与图谱规模数据，在 **170 万细胞小鼠胚胎**等数据中实现高效对齐，计算时间与内存较既往 OT 工具降数个数量级，并实验验证 NEUROD2 调控 epsilon 细胞形成[30]。在数据与评测侧，一项系统基准对结肠腺癌、肝细胞癌和卵巢癌连续切片，用 CODEX 蛋白与 scRNA-seq 作真值，统一比较 Stereo-seq v1.3、Visium HD FFPE、CosMx 6K、Xenium 5K 四个亚细胞平台，发现各平台在灵敏度、扩散控制、细胞分割等关键指标上差异显著，但仅覆盖 3 种肿瘤、4 个平台，结论外推受限[53]。病理基础模型的临床基准则系统比较 CTransPath、Phikon、UNI、Virchow 等公开自监督模型的参数量、算法与训练数据，评估下游临床任务性能，并指出数字病理数据缺乏与 WSI 算力需求是主要瓶颈[54]。这些工作提示，空间与多模态模型的性能声明高度依赖平台特性与评测设计。

更广的背景来自图谱与成像传统。Cell Painting 综述则回顾了 2013 年提出的显微细胞标记检测十年进展，协议优化、特征提取与批次校正的改进使其能捕获细胞对扰动的响应并用于解析化合物作用机制与毒性，未来方向是整合其他高内涵数据类型[21]。这两项工作本身不是基础模型，但分别提供了空间多模态图谱的组织范式与图像型 profiling 的表型基础。

### 2.3 扰动响应与虚拟细胞

扰动响应预测是虚拟细胞的核心任务，其技术路线大致沿三条线索展开：数据与基准的规模化、建模范式的分化、以及可信度与验证标准的反思。

**数据与基准的规模化**是这一方向的基础设施。Perturb-seq 最早将单细胞 RNA-seq 与 CRISPR 扰动结合，在混合池中分析约 **200,000 个免疫细胞和细胞系**，识别扰动靶点、基因 signature、细胞状态与遗传互作 [23]；同期工作用液滴单细胞 RNA-seq 加扰动条形码解剖未折叠蛋白反应，两个全基因组 CRISPRi 筛选鉴定约 **100 个命中基因**，解耦三条 UPR 分支 [55]。CROP-seq 通过将 gRNA 盒插入慢病毒 3'LTR 使其成为可检测的 mRNA，实现池化筛选的单细胞转录组读出，并验证编辑效率与 LentiGuide-Puro 高度相似 [24]。规模进一步扩展到原代细胞：一项工作扰动 4 名供体的 **2200 万原代人 CD4+ T 细胞**，在静息与刺激态测量转录组效应，发现调控因子及所控基因程序随刺激条件大幅变化 [56]。在评测侧，Arc Institute 发起 **Virtual Cell Challenge**，以循环开放的基准竞赛提供评估框架与专用数据集 [28]。

建模范式上出现了明显分化。一类工作以**生成模型直接预测扰动后的表达分布**：PRnet 用 SMILES 与剂量构建扰动嵌入，在新化合物、通路和细胞系预测上优于替代方法，并构建覆盖 **88 细胞系、52 组织**的扰动图谱为 **233 种疾病**推荐药物 [31]；PerturbNet 强调预测细胞状态分布变化而非仅均值，与 scGen、CPA、chemCPA、GEARS、Biolord 等对比 [32]；UNAGI 用 VAE-GAN 从疾病时间序列单细胞数据解析细胞动力学并做计算机药物筛选 [33]。

另一类工作转向**基础模型与适配器微调**。有研究在预训练单细胞基础模型上引入药物条件适配器，仅训练 **不到 1% 参数**，在所有泛化设置下达 SOTA，尤其在新细胞系少样本与零样本泛化上显著优于基线，但指出扰动数据集仅覆盖数百分子、少数细胞系 [57]。**Tahoe-x1** 将扰动训练的基础模型推到最高 **30 亿参数**，在 Tahoe-100M 等图谱上预训练，四项癌症相关基准均达 SOTA，计算效率较先前细胞状态模型提升 **3–30 倍** [58]。值得注意的是，跨模态工作对"堆参数"提出挑战：对 Tahoe-x1 的 **70M 参数**模型在 **48,843 个蛋白质组样本**（来自 **440 项质谱研究**）上做一个 epoch 的跨模态继续预训练，在多数基准上匹配或超过 **1B 和 3B** 的 RNA-only 模型，并提升对 held-out 蛋白扰动基准的迁移，而 RNA-only 缩放无同等收益 [35]。

第三类工作关注**扰动表征的粒度与结构**。STRAND 指出基因级模型会把同一基因不同位点（不同转录起始位点与调控元件）的扰动坍缩为同一表征，遂以调控 DNA 序列编码为条件参数化条件传输，在 K562、Jurkat、RPE1 上低样本判别分提升达 **33%**，新细胞系迁移 Pearson 提升达 **0.14**，基因组覆盖从约 **1.5%** 扩至约 **95%** [59]。SCALE 针对对照与处理细胞非配对的问题，将细胞视为无序集合、用集合感知编码器加条件 DiT 学习潜在传输，无需细胞级匹配，在 CRISPR 七项指标上全面超越竞争方法，其预测的细胞因子差异经三供体 PBMC 实验验证 [60]。AROMA 则整合文本证据、图拓扑与蛋白序列建模扰动-靶依赖，构建 **PerturbReason 数据集（>498k 样本）**，在未见细胞系零样本与知识稀疏长尾场景下保持稳健 [61]。

**时序与世界模型**是较新的子问题。Chreode 提出一步式细胞世界模型，用结构化残差转移算子把分布演化从推理时移到训练时，在 **240 万细胞**小鼠胚胎图谱上预训练，作为 GEARS 可迁移嵌入将 Norman Perturb-seq 的 **DE20 MSE 从 0.2121 降至 0.1858（相对提升 12.4%）** [62]。DynaVelo 用生成式神经常微分方程从单细胞多组学数据学习基因表达与 TF motif 活性的联合动态，重现野生型小鼠生发中心 B 细胞的体内分叉动态，并揭示 Arid1a 和 Ctcf 杂合缺失下的变化 [63]。与上述数据驱动路线不同，还有工作主张用自然语言"细胞规则"直接映射为数学方程构建可解释 agent-based 模型，案例覆盖肿瘤生长、侵袭、免疫治疗与脑发育 [34]。

在愿景与反思层面，AIVC 路线图提出构建多尺度、多模态的大神经网络模型，强调预测、生成、可查询三大能力，并对比 2012 年首个全细胞模型（**482 基因**）[13]。与之形成张力的是"可信虚拟细胞"路线图，批评当前工作偏重模型规模与数据量，指出静态图谱、仅转录组读出与分布内基准不足以预测新条件下的细胞行为，主张评估转向泛化到未见细胞类型与扰动，并建立数据—设计—基准—实验验证的完整证据链 [14]。这一批评与前述模型各自报告的零样本/未见基因泛化结果构成对话：后者多以自身基准上的提升为证据，而前者要求的是跨条件的生物学泛化。临床前转化综述同样强调从计算评估到 CRISPR 与类器官实验验证的闭环，并指出监管接受、数据隐私与可解释性仍是障碍 [64]。

综合来看，该领域的争议集中在三点：其一是**规模与模态之争**，RNA-only 参数缩放与跨模态数据引入何者收益更大，已有同一研究内部的对照显示后者在特定设置下更优 [35]；其二是**表征粒度之争**，基因级扰动表征是否因忽略位点信息而损失预测力 [59]；其三是**评估标准之争**，分布内留出精度与跨细胞类型、跨扰动的生物学泛化之间的落差尚未被统一基准消解 [14] [28]。

### 2.4 机制可解释性与表征分析

稀疏自编码器（SAE）已成为拆解单细胞基础模型内部表征的主流工具，但不同工作对“模型里到底编码了什么”给出了并不一致的答案。在 Geneformer V2-316M 与 scGPT whole-human 的全部层上训练 TopK SAE，分别得到 **82525 与 24527 个特征**，其中 **99.8% 的特征在 SVD 下不可见**，29–59% 可注释到通路；然而仅 **3/48（6.2%）的转录因子**表现出调控靶标特异性，多组织对照下为 10.4%[36]。在三个模型（scGPT、scFoundation、Geneformer）上训练的 SAE 则揭示出多样且复杂的生物与技术信号，且这些信号在预训练模型中即已出现，不同训练协议与架构的模型编码方式不同；更重要的是这些特征可被干预——抑制批次特征改善整合并保留生物信号，激活药物特征使对照细胞呈浓度依赖地向药物扰动状态转变[65]。两条路线因此形成对照：前者强调模型内化了有组织的生物学知识但几乎不含因果调控逻辑，后者强调特征与模型行为功能相关且可控。

因果层面的证据进一步收紧了这一判断。因果电路追踪通过消融 SAE 特征并测量下游响应，在 Geneformer V2-316M 与 scGPT 的 4 个条件、**96,892 条边、80,191 次前向**上发现两模型约 **53% 生物一致性**、**65–89% 抑制主导**，且不随架构与细胞类型变化，跨模型共识达 **1,142 个域对（10.6 倍富集）**；但 CRISPRi 基因级验证的方向准确率仅 **56.4%**，作者据此认为模型编码的是共表达而非因果调控[10]。对 Geneformer 的穷举电路追踪则指出以往选择性采样（每层 30 个特征）的偏差：L5 层全部 **4065 个活跃 SAE 特征**产出 **1,393,850 条显著下游边**，较选择性采样扩大 **27 倍**；三阶冗余比 0.59 低于配对交互的 0.74 且呈零协同，并发现重尾枢纽结构（1.8% 特征占据大量连接，40% 顶级枢纽无注释）以及层位置决定分化方向性（L17 特征 100% 推向成熟，L0/L11 为 0.00–0.58）[66]。系统评估框架则从预测效用角度提出质疑：在 37 项分析、153 个统计检验、四种细胞类型与两种扰动模态下，注意力模式虽呈分层组织（早期层蛋白互作、晚期层转录调控），但对扰动预测无增量价值，**基因级基线 AUROC 0.81–0.88 优于注意力/相关性边的 0.70**，消融调控头无退化，而 CSSI 可将 GRN 恢复提升至多 **1.85×**[37]。

与上述“表征丰富但因果稀薄”的图景相反，也有工作主张可从模型内部提取可用的机制性算法。从 scGPT 中提取的紧凑造血算法在 Tabula Sapiens 的 **564,253 个细胞**上验证，伪时间深度排序 **|ρ|=0.439** 优于次优的 0.331，CD4/CD8 AUROC 为 **0.867**、单核/巨噬为 0.951，且比 MLP 探针快 **34.5 倍**、参数少约 **1000 倍**，但作者承认主要在造血系统验证、其他生物学过程泛化有限[67]。在 GRN 推断方向，有研究认为 scFM 表现不佳源于重建式预训练未显式捕获调控信号，遂提出 GRN 泛化基准并用虚拟值扰动与梯度轨迹从冻结 scFM 蒸馏基因间特征，报告显著优于现有方法[68]；CauTrigger 则把 do-calculus 整合进分层深度潜变量模型以分离因果与虚假潜因子，在合成与真实多层调控数据集上优于现有方法[69]。两类主张与前述 CRISPRi 56.4% 方向准确率、注意力无增量价值的结论存在张力：分歧部分源于评价目标不同——提取可执行算法或提升 GRN 基准分数，并不等同于模型内部编码了因果调控逻辑。

### 2.5 形态与图像表型基础模型

图像表型基础模型的核心问题正从“能否提取表征”转向“表征是否保留任务相关的生物学关系”。在特征空间评估上，一项工作用U2OS JUMP-MOA参考板的**90个化合物**做零样本检索，发现CellPaintSSL、OpenPhenom、uniDINO的活性阳性数分别为**85/90、81/90、82/90**，数量相近，但CellPaintSSL的活性检索mAP显著高于另两者（p<0.0001），且MOA注释恢复只是部分实现并因模型而异[70]。这说明前提性的特征质量并不保证目标生物学关系的恢复，也提示单一参考板上的结论需谨慎外推[70]。综述层面则给出更宏观的判断：深度学习表征常优于手工特征，如CLOOME零样本MoA top-10准确率**61.3%**对比CellProfiler **24.5%**，但部分场景手工特征仍具竞争力，时序与3D模态、质控标准和特征解释仍不成熟[71]。

在数据规模与监督方式上，不同工作走向两条路径。CellPaint-POSH把Cell Painting与pooled光学CRISPR筛选、自监督深度学习结合，改造线粒体染色为RNA探针Mitoprobe并调整逆转录流程以兼容原位测序，在**163,090个单细胞**上实现无偏基因功能推断，其自监督机器学习特征预测性能高于专家形态特征，形态表型可按已知功能聚类基因并在无通路报告基因时揭示基因关联网络[22]。与之相对，PerturbBridge针对虚拟细胞模型仅匹配真实图像分布、未显式优化扰动特异性生物响应的问题，提出随机数据到数据桥模型，在训练中对预测的扰动图像直接施加扰动特异性表型监督，联合优化桥回归与可微生物响应损失[72]；在BBBC021上MoA准确率CellProfiler **77.8%**（较CellFlux+5.7点）、DINOv2 **74.9%**（+7.5点），JUMP Hit@10 **12.15%**、中位秩**74**，AllenCell Hit@1 **69.29%**[72]。两者的差异在于监督信号进入流程的位置：前者以自监督表征支撑下游推断，后者把表型监督直接嵌入生成训练[22][72]。

## 3 数据与资源

在扰动筛选数据方面，**基因组规模Perturb-seq** 在K562与RPE1两个细胞系中以CRISPRi敲低所有表达基因、覆盖**超过250万个**人类细胞，报告了RNA剪接、分化、染色体不稳定等多维表型，并发现线粒体基因组应激的特异调控，其局限在于仅两个细胞系、敲低而非敲除、表型限于转录组 [25]。同一Perturb-seq范式的另一项工作则从高维单细胞表型构建细胞状态流形，将每个扰动与遗传互作投射到流形特定位置，实现调控通路无偏排序与遗传互作的系统分类，但依赖强互作筛选、未覆盖全基因组互作 [73]。空间维度上，**Perturb-FISH** 将MERFISH与gRNA原位扩增结合，在LPS刺激巨噬细胞中与匹配的Perturb-seq比较验证敲除效应一致性，并揭示细胞密度与邻居扰动的影响，进一步结合钙成像用于ASD风险基因CRISPRi筛选并在肿瘤异种移植3D组织中验证；其技术限制是gRNA仅20bp、无法如mRNA般平铺而需原位扩增 [26]。药物扰动方面，**Tahoe-100M** 覆盖**超过1亿**细胞、50个细胞系与379种化合物（3剂量、24小时），覆盖约56,000个细胞系-药物-剂量组合，发现Dabrafenib在非BRAF依赖细胞系中的意外敏感性及CDK抑制剂引起G1或G2/M阻滞，但摘要未提供模型训练与验证细节 [27]。

图谱类资源为上述扰动数据提供参照框架。全小鼠脑MERFISH图谱对约**800万**细胞成像超过1100个基因并整合scRNA-seq，鉴定超过5000个转录簇与约300个主要细胞类型，注册到小鼠脑共坐标框架以量化各脑区细胞组成并识别空间模块，局限为仅小鼠脑且基因面板有限、需整合scRNA-seq [74]。Human Cell Atlas相关综述则提出细胞图谱作为细胞普查、3D图谱、基因型-表型连接、4D发育图谱及生物学基础模型五种用途，指向从数据收集走向图谱整合与统一基础模型 [75]。值得注意的是，扰动数据在规模与模态上差异明显：Perturb-seq类工作以百万级细胞换取全基因组扰动覆盖但限于少数细胞系与转录组读出，Tahoe-100M以亿级细胞换取化合物与细胞系多样性但缺乏全文验证细节，空间筛选则以牺牲通量与gRNA平铺能力换取原位空间与功能读出——三者尚无可直接比较的统一基准。

## 4 应用与结果

面向肝脏的 AI 虚拟细胞（AIVC）建模被归纳为三条互补路线：**生成模型、动力学/运输模型与预训练/基础模型**，并以扰动响应预测作为跨层评估任务 [76]。现有证据按强度分为直接肝脏验证、含肝脏基准、通用单细胞证据与概念应用四类，但已发表模型仅展示了图谱整合、轨迹推断、可迁移表示、回顾性响应程序等单个组件，**尚不构成经前瞻验证的肝脏模拟器** [76]。

该综述同时指出，肝脏单细胞与空间图谱虽能刻画小叶区带化肝细胞、纤维化巨噬细胞—星状细胞生态位、胆管细胞反应、免疫重塑与肝细胞癌生态系统等状态的空间分布，但其本身无法预测肝损伤是否进展，也无法预测肝脏对未经测试的药物、毒物或遗传扰动的响应 [76]。因此作者提出评估应覆盖**供体、病因、分期与平台**等维度，而缺乏前瞻性验证被列为主要局限 [76]。

## 5 评测、可复现性与争议

评测工作的第一条主线是基准污染与数据泄漏。**scContam** 用 MinHash 基因集指纹加基于损失的成员推断攻击（MIA-scFM）逐细胞审计预训练暴露，在 PBMC 3k 与胰腺胰岛图谱上分别有 **80.4%**、**77.0%** 的细胞指纹 p<0.05，而截断后的 AIDA v2 与 Tahoe-100M 为 **0%**；MIA AUROC 随模型容量数据比从 **0.494** 升到 **0.690** 再到 **0.881** [41]。这说明零样本分数可能反映记忆而非泛化，但作者也指出生产级模型抗实例记忆，分布污染仍需单独检测 [41]。

第二条主线是「基础模型是否打得过简单基线」，结论高度依赖任务与指标。在扰动后表达预测上，四个 Perturb-seq 数据集的差分空间里 Train Mean 基线（0.711/0.557/0.373/0.628）优于 scGPT（0.641/0.554/0.327/0.596）与 scFoundation（0.552/0.459/0.269/0.471），而随机森林加 GO 特征最佳（0.739/0.586/0.480/0.648）[38]；另一项 K562 CRISPRa 双扰动评测中，五个基础模型与两个深度学习模型均未超过加性基线，遗传互作预测不优于 no change 基线 [77]。零样本嵌入同样不稳健：PertEval-scFM 显示 scFM 嵌入未持续优于基线，尤其在分布偏移下 [78]；四模型零样本评测中注释任务基线多数数据集最强，蛋白表达预测基础模型更准（SCimilarity 误差最低、Transcriptformer 相关性最高），整合任务 scVI 更佳 [79]。

低监督条件下这一图景更细碎。七种基础模型对三种经典表示的比较中，**CellPLM** 在聚类、注释与批次校正领先，scMulan 在扰动预测领先，PCA 在表达重建领先；7 个基础模型中仅 1 个聚类、3 个批次校正、4 个注释、0 个重建、6 个扰动预测超过最强经典基线，且跨模型基因关系一致性未超过维度匹配随机投影零假设 [80]。细胞类型分类上，scFoundation 持续最佳，Geneformer 表现差甚至不如基线 [81]；十模型八任务的 scEval 评测则认为 scGPT、Geneformer、CellPLM 综合最佳，但没有模型在所有任务上优于专用方法 [82]。生物学驱动的六模型评测补充说零样本嵌入确实捕捉生物学信息，但部分场景未超越 HVG、Seurat、Harmony、scVI 等简单基线 [83]。

「无参数也能赢」是争议的另一端。一条仅依赖精细归一化与线性方法的流程在多个常用基准取得 SOTA 或近 SOTA，并在新细胞类型与新物种的分布外任务上超越 TranscriptFormer 等基础模型 [39]。类似地，小分子活性基准中逻辑回归细胞计数达 AUC **0.70±0.22**，接近 CLOOME 的 **0.71±0.19**，细胞计数加 MW 与 logP 达 **0.74±0.21**；作者指出许多 assay 直接关联细胞健康或毒性，但在 24 个蛋白靶标基准中 Cell Painting 确实优于细胞计数 [84]。这些结果把「基准本身是否有效」推到了前台。

多模型统一评测进一步显示排名不稳定。六模型跨 scRNA-seq、空间转录组与 Perturb-seq 的协调基准中无模型全面领先：表达训练的细胞级 Transformer 擅长细胞身份，空间/图模型保留组织结构，语言嵌入在部分扰动指标有竞争力，排名随模态、预处理、token 化、生物先验、域偏移与指标而变化 [42]。VCBench 把四个虚拟细胞框架综合为七个能力维度，在五个可测维度上预注册线性/最近邻基线，结果基线在 **5 维中 4 维**追平或超越所有基础模型，仅 TranscriptFormer 在 RNA 到蛋白预测上以 **53% Pearson** 超过最强基线；多尺度整合与 in silico 实验两维结构上无法端到端测试 [40]。

可解释性方面出现了明确的反面证据。两层评估框架在两种架构、四种细胞类型、两种扰动模态下做 **153 项**统计检验并加因果消融，发现注意力边分数对扰动靶标预测相对基因级特征无增量价值，单变量基线反而更优，TRRUST 头因果消融无行为效应 [85]。GRN 重建的统一基准则给出部分正面信号：严格零样本下 scGPT token 嵌入相似度在 STRING 和 ChIP-seq 参考上超越经典基线，动态转移探测中 scFoundation 整体最强 [86]。两者并不直接冲突——前者测的是扰动靶标预测的增量信息，后者测的是参考网络恢复——但共同说明「注意力即调控」的默认解读需要分任务验证。

扰动预测的评测协议本身正被重写。PerturBench 指出广泛使用模型存在模式崩溃，秩指标可补充 RMSE，且无单一架构明显占优、简单架构随数据规模扩展良好 [87]；27 种方法、29 个数据集、6 类指标的综述强调跨未见细胞背景与扰动场景的泛化仍存疑，细胞上下文嵌入对泛化必要 [88]。**EL-PERTURB** 用分层 OOD 划分在必需基因与全基因组 Perturb-seq 上压力测试 6 类架构 20 个模型，结论是现有基准多依赖随机划分而掩盖系统性失效，模型在真实 OOD 下泛化失败 [89]。与之相对，指标校准框架在 14 个数据集、18 个指标上发现 MSE、Pearson Δ 等常用指标校准不良、降低对阳性模型的敏感性，在良好校准指标下深度学习扰动模型可优于无信息基线 [90]——这与前述「不如基线」的结论构成直接张力，分歧点在于指标是否校准、划分是否 OOD。

可复现性基础设施被反复提为瓶颈。BioLLM 用统一 API、决策树预处理与 BioTask 执行器解决预处理不一致、接口异构与指标非标准化三大问题，支持零样本推理与微调 [91]；scArchon 基于 Snakemake 容器化运行 9 种扰动工具并聚合评分排名，解决环境不兼容并支持用户自有数据，但仅限非遗传扰动 [92]。图像侧，JUMP 单数据集占 **115 TB**，JUMP-lite 以 **92.0 GB** 子集约缩小 **1,250 倍**，中度有损压缩基本保留信号，标准化表型活性与一致性指标揭示方法间显著差异 [93]。空间转录组则通过多站点统一 SOP、开源 SpatialQM 与 STP 门户，在 Xenium 与 CosMx 上跨三站点六组织建立准确度、精密度、重复性、灵敏度与特异性指标，STP 可实时评估约 **3300 万**细胞数据 [94]。

还有一类被忽视的评测维度：表征对技术噪声的稳定性。基于扰动不变性的无监督框架在 5 个 scFM、PCA 基线与 39 个数据集上发现，标准基准判定近乎等价的模型在丢弃 **5%** 计数时局部邻域保持差异近 **2 倍**，且该不稳定性具尺度依赖性并被视觉连贯的嵌入掩盖；重采样聚类稳定性与生物保守指标的 Spearman ρ=**0.78** [95]。这与整合基准的经典结论形成对照：68 种方法/预处理组合、85 批次、13 个图谱级任务、超 **120 万**细胞的评测认定 Scanorama 与 scVI 在复杂任务表现好、有注释时 scGen 与 scANVI 最优、Harmony 与 LIGER 适合 scATAC，但部分任务 ground truth 依赖预处理注释可能引入偏差 [96]。总的争议可归为三点：基准污染使零样本分数含义不明 [41]，简单基线在多数任务追平或超越基础模型 [40][39]，而指标校准与 OOD 划分的选择足以翻转「谁更好」的结论 [90][89]。

## 6 空白与趋势

**趋势一：评测正在从“分布内留出精度”转向“污染审计 + 简单基线 + 跨条件泛化”三重压力测试，且结论普遍不利于基础模型。** scContam 在 PBMC 3k 与胰腺胰岛图谱上分别有 **80.4%**、**77.0%** 的细胞指纹 p<0.05，而截断后的 AIDA v2 与 Tahoe-100M 为 **0%**，MIA AUROC 随模型容量数据比从 **0.494** 升到 **0.881** [41]；四个 Perturb-seq 数据集上 Train Mean 基线在差分空间优于 scGPT 与 scFoundation，随机森林加 GO 特征最佳 [38]；K562 CRISPRa 双扰动评测中五个基础模型均未超过加性基线 [77]；VCBench 中预注册线性/最近邻基线在 **5 维中 4 维**追平或超越所有基础模型 [40]。**尚未见到把污染审计、基线对照与分布外泛化纳入同一预注册流程的基准**——现有工作各测一角，无法回答“扣掉记忆效应后还剩多少泛化”。

**趋势二：机制可解释性从“注意力可视化”转向“SAE 特征 + 因果消融”，但多条独立证据指向模型编码共表达而非因果调控。** 因果电路追踪在 **96,892 条边、80,191 次前向**上发现两模型约 **53% 生物一致性**、**65–89% 抑制主导**，而 CRISPRi 基因级验证方向准确率仅 **56.4%** [10]；TopK SAE 图谱显示仅 **3/48（6.2%）转录因子**具调控靶标特异性 [36]；系统评估中基因级基线 AUROC **0.81–0.88** 优于注意力/相关性边的 **0.70**，消融调控头无退化 [37]。**空白在于：尚无工作把 SAE 特征干预（如激活药物特征使对照细胞向扰动状态转变 [65]）与 CRISPRi 湿实验验证做成闭环**，即“找到特征—操纵特征—验证表型”的完整证据链仍缺失。

**趋势三：扰动表征的粒度从基因级下沉到位点/序列级，并开始与集合级、非配对传输建模合流。** STRAND 指出基因级模型将同基因不同位点扰动坍缩为同一表征，以调控 DNA 序列为条件，低样本判别分提升达 **33%**、新细胞系迁移提升达 **0.14**、基因组覆盖从约 **1.5%** 扩至约 **95%** [59]；SCALE 用集合感知编码器加条件 DiT 处理非配对对照-处理细胞，CRISPR 七项指标超越竞争方法并经三供体 PBMC 实验验证 [60]。**没人做的是把位点级序列条件与集合级非配对传输结合**：前者解决“扰动身份太粗”，后者解决“细胞对不上”，二者目前分属不同论文、未见联合建模或统一评测。

**趋势四：空间与病理多模态基础模型的预训练目标从“重建观测基因”转向“预测潜在表征”，但配对数据依赖成为共同瓶颈。** CellWorld 以 JEPA 式潜在空间预测替代基因重建，**CellWorld-Small（5.74M）在全部 11 个线性探针和 7 个空间基准上超越所有基线** [9]；NexuST 走基因级与细胞级交错的分层路线，构建 **HumanST-46M** [51]；PAST 基于 **2000 万配对病理图像与单细胞转录组** [18]，OmiCLIP 基于 **220 万组织 patch** 并明确泛化受限于配对 WSI 与 Visium 数据 [19]，mSTAR 亦指出跨中心泛化仍需验证 [20]。**空白是“无配对的跨模态预训练”与“跨平台/跨中心的外部验证”**——现有模型几乎都在配对语料内报告提升，尚无工作系统量化配对数据规模下降到何种程度时性能崩塌。

**趋势五：虚拟细胞的“可信度”要求开始从愿景转为可操作标准，但实验验证闭环仍是少数派。** “可信虚拟细胞”路线图主张评估转向泛化到未见细胞类型与扰动，并建立数据—设计—基准—实验验证的完整证据链 [14]；AIVC 路线图提出预测、生成、可查询三大能力 [13]；肝脏 AIVC 综述明确指出已发表模型仅展示单个组件，**尚不构成经前瞻验证的肝脏模拟器**，缺乏前瞻性验证是主要局限 [76]。**目前只有 SCALE [60]、Perturb-FISH [26]、Chreode [62] 等少数工作带湿实验或独立数据验证**，且验证规模小、限于单一系统；**没有人建立“预测—实验—反馈再训练”的公开循环数据集**，这正是 Virtual Cell Challenge 试图填补但尚未产出跨条件泛化证据的环节 [28]。

**趋势六：规模扩张的收益出现明确反例，跨模态数据与架构效率开始替代单纯堆参数。** 用 **2220 万细胞**语料预训练 **400 个模型**、开展 **6400 次实验**的研究未观察到明确数据缩放定律，性能在远小于当前语料时即趋于平台 [8]；对 Tahoe-x1 的 **70M 参数**模型在 **48,843 个蛋白质组样本**上做一个 epoch 跨模态继续预训练，在多数基准上匹配或超过 **1B 和 3B** 的 RNA-only 模型 [35]；逐层评估显示轨迹最优层在 **60% 深度**、扰动最优层随 T 细胞激活状态在 **0–96%** 间漂移 [47]。**没人做的是“按任务与细胞状态自适应选择表征层/模态配比”的元学习框架**——现有工作只报告“最优层因任务而异”这一现象，未将其转化为可部署的推理时策略。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 单细胞基础模型 | 成熟（方法收敛、增量为主，但评测争议未决） | scGPT [1] 与 Geneformer 系 [2] 已确立「大规模预训练 + 迁移」范式并被广泛复用；同时 GenePT [6] 用简单基因文本嵌入即达到可比效果，说明架构创新边际收益下降、进入增量与批判期 |
| 2.2 空间与多模态模型 | 朝阳（近两年爆发、方法未收敛） | MultiVI [16] 与 moscot [30] 分别代表多模态生成整合与时空映射两条并行路线，尚未统一；AD 多模态图谱 [97] 显示大规模多模态整合已进入疾病应用，但方法层面仍多路线竞争 |
| 2.3 扰动响应与虚拟细胞 | 朝阳（概念爆发、CNS 高频，但预测性能未过关） | Perturb-seq 原始框架 [23] 与 multiplexed CRISPR 筛选 [55] 奠定数据基础；虚拟细胞路线图 [13] 提出议程但未收敛；而 [77] 明确「深度学习扰动预测尚未跑赢基线」，说明处于高热度 + 未解决阶段 |
| 2.4 机制可解释性与表征分析 | 萌芽（少量探索性工作，全部为 2026 预印本） | 稀疏自编码器揭示单细胞基础模型可解释特征 [65] 与系统性可解释性评测 [37] 均为新近预印本、引用极低，尚无共识方法；[36] 进一步指出模型编码的生物知识「组织化但调控信息有限」，属早期批判性探索 |
| 2.5 形态与图像表型基础模型 | 萌芽（证据少、以平台与评测为主） | pooled Cell Painting CRISPR 平台 [22] 与图像表型 profiling 综述 [71] 表明该方向刚建立数据与评测框架，尚无公开权重的基础模型主导；检索样本仅 4 篇，属早期 |
| 3 数据与资源 | 成熟（图谱与扰动数据资源已规模化、被广泛复用） | genome-scale Perturb-seq 图谱 [25] 与 genetic interaction manifold [73] 已构成标准扰动资源；Human Cell Atlas 向统一基础模型演进 [75] 说明资源层已进入整合复用阶段 |
| 5 评测、可复现性与争议 | 朝阳（近两年集中爆发、结论尚未定型） | atlas-level 整合基准 [96] 确立评测范式；PerturBench [87] 与「未跑赢基线」[77]、基础模型效用评估 [82] 共同显示评测正快速扩张且不断推翻既有结论，属方法未收敛的活跃期 |

**整体判断**：这个方向整体处于**「朝阳后期 + 局部成熟」的混合阶段**——单细胞基础模型（2.1）与数据资源（3）已方法收敛、进入增量与复用；扰动预测/虚拟细胞（2.3）与评测（5）热度最高但**核心性能问题未解决**（[77] 明确未跑赢基线），可解释性（2.4）与形态模型（2.5）仍是萌芽。雷达样本中近两年占比 **74%**、CNS 占比 **31%**，但 2.4/2.5 节 n 很小（8/4 篇）且多为 2026 预印本，只能说明证据挂载集中，不能推出领域整体规模。**窗口期估计 12–24 个月**：评测与可解释性方向尚可抢占先发，但一旦「跑赢基线」的强结果出现，纯预测类工作将迅速贬值。**最大不确定性**是扰动响应预测能否在跨细胞类型/跨扰动泛化上真正超越简单基线——若长期不能，虚拟细胞的叙事会从「预测」退化为「表征 + 检索」。

**接下来怎么做**：

1. **把评测当作切入点，而非附属**：用 Tahoe-100M / Perturb-seq 公共数据 + 你自己的类器官扰动数据，构建**跨细胞类型泛化的扰动预测基准**，重点复现并扩展 [77] 与 PerturBench [87] 的「基线未被打败」结论。现在做是因为评测结论尚未定型、CNS 接受度高（[77] 已被引 143），且能直接产出可复用 benchmark 与代码。

2. **做「衰老 × 扰动」的交叉子问题**：衰老细胞状态是扰动预测的天然难点（状态漂移大、跨供体异质），用公共衰老图谱 + 类器官多组学做**扰动响应在衰老背景下的泛化评估**，引用 [13] 的虚拟细胞议程作为框架。现在做是因为该交叉点尚无系统性工作，且与你博后的衰老主线直接契合。

3. **押注可解释性/表征分析（2.4）作为低成本高回报方向**：用稀疏自编码器复现并扩展 [65] 与 [37]，在 scGPT/Geneformer 权重上做**特征级生物学验证**（如调控元件、细胞类型流形），结合 [67] 的流形提取方法。现在做是因为该节全部为 2026 预印本、**引用近零**，先发优势明显，且不需要新数据、只需公开权重。

4. **多模态整合走「方法对比 + 类器官验证」而非新架构**：用 MultiVI [16] 与 moscot [30] 作为基线，在你的类器官 RNA+蛋白+空间数据上做**整合方法头对头评测**，产出可复现流程。现在做是因为 2.2 方法未收敛、多路线并存，对比研究有明确发表空间，且直接服务合作项目。

5. **避开纯「再训一个基础模型」的红海**：2.1 已成熟（scGPT [1]、Geneformer [2] 主导），GenePT [6] 证明简单方法可比，新预训练模型边际收益低。建议把算力投向**下游任务适配 + 评测 + 可解释性**，用公共数据 demo 快速出结果，再迁移到类器官多组学。

## 参考文献

1. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. Nature Methods 2024. https://doi.org/10.1038/s41592-024-02201-0
2. Transfer learning enables predictions in network biology. Nature 2023. https://doi.org/10.1038/s41586-023-06139-9
3. CellFM: a large-scale foundation model pre-trained on transcriptomics of 100 million human cells.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59926-5
4. RegFormer: a single-cell foundation model powered by gene regulatory hierarchies.. Nature communications 2026. https://doi.org/10.1038/s41467-026-72198-x
5. A Cross-Species Generative Cell Atlas Across 1.5 Billion Years of Evolution: The TranscriptFormer Single-cell Model. bioRxiv 2025. https://doi.org/10.1101/2025.04.25.650731
6. GenePT: A Simple But Effective Foundation Model for Genes and Cells Built From ChatGPT. bioRxiv 2023. https://doi.org/10.1101/2023.10.16.562533
7. Zero-shot evaluation reveals limitations of single-cell foundation models.. Genome biology 2025. https://doi.org/10.1186/s13059-025-03574-x
8. Evaluating the role of pretraining dataset size and diversity on single-cell foundation model performance.. Nature methods 2026. https://doi.org/10.1038/s41592-026-03120-y
9. CellWorld: From Gene-Level Reconstruction to Latent Cell Prediction in Spatial Transcriptomics Foundation Models.  2026. https://arxiv.org/abs/2608.06659v1
10. Causal Circuit Tracing Reveals Distinct Computational Architectures in Single-Cell Foundation Models: Inhibitory Dominance, Biological Coherence, and Cross-Model Convergence.  2026. https://arxiv.org/abs/2603.01752v2
11. Single-cell foundation models: bringing artificial intelligence into cell biology.. Experimental & molecular medicine 2025. https://doi.org/10.1038/s12276-025-01547-5
12. LucaCell: a sequence-centric foundation model for cross-species single-cell analysis.  . https://doi.org/10.21203/rs.3.rs-11151765/v1
13. How to build the virtual cell with artificial intelligence: Priorities and opportunities.. Cell 2024. https://doi.org/10.1016/j.cell.2024.11.015
14. Toward trustworthy virtual cells: a roadmap for perturbation-resolved, context-aware, and experimentally validated cell models. Frontiers in Cell and Developmental Biology 2026. https://doi.org/10.3389/fcell.2026.1900624
15. scDifformer: diffusion-based post-training for virtual cell modeling across large-scale single-cell data. Nucleic Acids Research 2026. https://doi.org/10.1093/nar/gkag706
16. MultiVI: deep generative model for the integration of multimodal data. Nature Methods 2023. https://doi.org/10.1038/s41592-023-01909-9
17. CLM-X: A multimodal single-cell foundation model with flexible multi-way Transformer for unified scRNA-seq and scATAC-seq analysis. bioRxiv 2026. https://doi.org/10.64898/2026.02.17.704943
18. PAST: A multimodal single-cell foundation model for histopathology and spatial transcriptomics in cancer. arXiv.org 2025. https://arxiv.org/abs/2507.06418v1
19. A visual-omics foundation model to bridge histopathology with spatial transcriptomics.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02707-1
20. A multimodal knowledge-enhanced whole-slide pathology foundation model.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66220-x
21. Cell Painting: a decade of discovery and innovation in cellular imaging.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02528-8
22. A pooled Cell Painting CRISPR screening platform enables de novo inference of gene function by self-supervised deep learning.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66778-6
23. Perturb-seq: Dissecting molecular circuits with scalable single cell RNA profiling of pooled genetic screens. Cell 2016. https://doi.org/10.1016/j.cell.2016.11.038
24. Pooled CRISPR screening with single-cell transcriptome read-out. Nature Methods 2017. https://doi.org/10.1038/nmeth.4177
25. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. bioRxiv 2021. https://doi.org/10.1016/j.cell.2022.05.013
26. Simultaneous CRISPR screening and spatial transcriptomics reveal intracellular, intercellular, and functional transcriptional circuits.. Cell 2025. https://doi.org/10.1016/j.cell.2025.02.012
27. Abstract 491: A 100 million cell single cell atlas enabling mechanistic and genotype-specific drug response discovery.. Cancer Research 2026. https://doi.org/10.1158/1538-7445.am2026-491
28. Virtual Cell Challenge: Toward a Turing test for the virtual cell.. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.008
29. A cell atlas foundation model for scalable search of similar human cells.. Nature 2024. https://doi.org/10.1038/s41586-024-08411-y
30. Mapping cells through time and space with moscot.. Nature 2025. https://doi.org/10.1038/s41586-024-08453-2
31. Predicting transcriptional responses to novel chemical perturbations using deep generative model for drug discovery.. Nature communications 2024. https://doi.org/10.1038/s41467-024-53457-1
32. PerturbNet predicts single-cell responses to unseen chemical and genetic perturbations.. Molecular systems biology 2025. https://doi.org/10.1038/s44320-025-00131-3
33. A deep generative model for deciphering cellular dynamics and in silico drug discovery in complex diseases.. Nature biomedical engineering 2025. https://doi.org/10.1038/s41551-025-01423-7
34. Human interpretable grammar encodes multicellular systems biology models to democratize virtual cell laboratories.. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.048
35. Single-cell foundation models benefit from cross-modal training: adding proteomics data beats parameter scaling. bioRxiv 2026. https://doi.org/10.64898/2026.08.14.744845
36. Sparse autoencoders reveal organized biological knowledge but minimal regulatory logic in single-cell foundation models: a comparative atlas of Geneformer and scGPT.  2026. https://arxiv.org/abs/2603.02952v1
37. Systematic Evaluation of Single-Cell Foundation Model Interpretability Reveals Attention Captures Co-Expression Rather Than Unique Regulatory Signal.  2026. https://arxiv.org/abs/2602.17532v1
38. Benchmarking foundation cell models for post-perturbation RNA-seq prediction.. BMC genomics 2025. https://doi.org/10.1186/s12864-025-11600-2
39. Parameter-free representations outperform single-cell foundation models on downstream benchmarks.  2026. https://arxiv.org/abs/2602.16696v1
40. VCBench: A Multi-Dimensional Benchmark for Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.06.18.733146
41. Auditing pretraining contamination in single-cell foundation model benchmarks.  2026. https://arxiv.org/abs/2607.20572v1
42. Harmonised benchmarking of foundation models for single-cell and spatial transcriptomics reveals context-dependent generalisation.  2026. https://arxiv.org/abs/2607.17227
43. scPRINT-2: Towards the next-generation of cell foundation models and benchmarks.  2025. https://doi.org/10.64898/2025.12.11.693702
44. Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling.  . https://doi.org/10.64898/2026.09.22.752128
45. EpiZoo: a DNA sequence-aware foundation model for cross-species single-cell epigenomics.  . https://doi.org/10.64898/2026.09.24.754017
46. Scalable querying of human cell atlases via a foundational model reveals commonalities across fibrosis-associated macrophages. bioRxiv 2023. https://doi.org/10.1101/2023.07.18.549537
47. Intermediate Layers Encode Optimal Biological Representations in Single-Cell Foundation Models.  2026. https://arxiv.org/abs/2604.14838v1
48. Deep generative modeling of sample-level heterogeneity in single-cell genomics.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02808-x
49. PTM-Mamba: a PTM-aware protein language model with bidirectional gated Mamba blocks.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02656-9
50. Emerging frontiers for AI in single-cell genomics.. Molecular cell . https://doi.org/10.1016/j.molcel.2026.09.014
51. NexuST: A Hierarchical Foundation Model for Spatial Transcriptomics.  . https://doi.org/10.64898/2026.09.22.753590
52. VINTER: a generative vision-language model for annotating and interrogating spatial tissues.  . https://doi.org/10.64898/2026.10.01.752251
53. Systematic benchmarking of high-throughput subcellular spatial transcriptomics platforms across human tumors.. Nature communications 2025. https://doi.org/10.1038/s41467-025-64292-3
54. A clinical benchmark of public self-supervised pathology foundation models.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58796-1
55. A multiplexed single-cell CRISPR screening platform enables systematic dissection of the unfolded protein response. Cell 2016. https://doi.org/10.1016/j.cell.2016.11.048
56. Genome-scale perturb-seq in primary human CD4+ T cells maps context-specific regulators of T cell programs and human immune traits.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.002
57. Efficient Fine-Tuning of Single-Cell Foundation Models Enables Zero-Shot Molecular Perturbation Prediction.  2024. https://arxiv.org/abs/2412.13478v2
58. Tahoe-x1: Scaling Perturbation-Trained Single-Cell Foundation Models to 3 Billion Parameters. bioRxiv 2025. https://doi.org/10.1101/2025.10.23.683759
59. STRAND: Sequence-Conditioned Transport for Single-Cell Perturbations.  2026. https://arxiv.org/abs/2602.10156v1
60. SCALE:Scalable Conditional Atlas-Level Endpoint transport for virtual cell perturbation prediction.  2026. https://arxiv.org/abs/2603.17380v3
61. AROMA: Augmented Reasoning Over a Multimodal Architecture for Virtual Cell Genetic Perturbation Modeling.  2026. https://arxiv.org/abs/2604.20263v1
62. Chreode: A Cell World Model for One-Step Temporal Dynamics and Perturbation Prediction. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.28111
63. Deep dynamical models of single-cell multiomic velocities predict loss-of-function and rescue perturbations in B cells.. Nature biotechnology . https://doi.org/10.1038/s41587-026-03348-1
64. AI-driven virtual cell models in preclinical research: technical pathways, validation mechanisms, and clinical translation potential.. NPJ digital medicine 2025. https://doi.org/10.1038/s41746-025-02198-6
65. Sparse Autoencoders Reveal Interpretable Features in Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.1101/2025.10.22.681631
66. Exhaustive Circuit Mapping of a Single-Cell Foundation Model Reveals Massive Redundancy, Heavy-Tailed Hub Architecture, and Layer-Dependent Differentiation Control.  2026. https://arxiv.org/abs/2603.11940v1
67. Discovery of a Hematopoietic Manifold in scGPT Yields a Method for Extracting Performant Algorithms from Biological Foundation Model Internals.  2026. https://arxiv.org/abs/2603.10261v1
68. Towards Universal Gene Regulatory Network Inference: Unlocking Generalizable Regulatory Knowledge in Single-cell Foundation Models.  2026. https://arxiv.org/abs/2605.08128v1
69. CauTrigger: deciphering biological system state transitions by hierarchical causal decomposition.. Nature methods . https://doi.org/10.1038/s41592-026-03274-9
70. Retrieval-Based Evaluation of Cell Painting Feature Spaces Reveals Differences in the Preservation of Biologically Meaningful Phenotypic Similarity.. International journal of molecular sciences 2026. https://doi.org/10.3390/ijms27135727
71. Progress and new challenges in image-based profiling.. Molecular systems biology 2026. https://doi.org/10.1038/s44320-026-00197-7
72. PerturbBridge: Direct Phenotypic Supervision for Cellular Perturbation Generation.  . https://arxiv.org/abs/2610.17066
73. Exploring genetic interaction manifolds constructed from rich single-cell phenotypes. Science 2019. https://doi.org/10.1126/science.aax4438
74. A molecularly defined and spatially resolved cell atlas of the whole mouse brain. bioRxiv 2023. https://doi.org/10.1101/2023.03.06.531348
75. The Human Cell Atlas from a cell census to a unified foundation model.. Nature 2024. https://doi.org/10.1038/s41586-024-08338-4
76. Toward AI Virtual Cells for Hepatology: Representation, Generation, Dynamics, and Intervention in Single-Cell Models.. Clinical and Molecular Hepatology 2026. https://doi.org/10.3350/cmh.2026.0820
77. Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02772-6
78. PertEval-scFM: Benchmarking Single-Cell Foundation Models for Perturbation Effect Prediction. bioRxiv 2025. https://doi.org/10.1101/2024.10.02.616248
79. Benchmarking single-cell foundation models in a zero-shot setting. bioRxiv 2026. https://doi.org/10.64898/2026.08.03.739553
80. Task-dependent Performance of Single-cell Foundation Models under Low Supervision. bioRxiv 2026. https://doi.org/10.64898/2026.04.01.714123
81. A Systematic Evaluation of Single-Cell Foundation Models on Cell-Type Classification Task. Web Search and Data Mining 2025. https://doi.org/10.1145/3701551.3708811
82. Evaluating the Utilities of Foundation Models in Single‐Cell Data Analysis. bioRxiv 2024. https://doi.org/10.1101/2023.09.08.555192
83. Biology-driven insights into the power of single-cell foundation models. Genome Biology 2025. https://doi.org/10.1186/s13059-025-03781-6
84. Counting cells can accurately predict small-molecule bioactivity benchmarks.. Nature communications 2026. https://doi.org/10.1038/s41467-026-68725-5
85. Systematic evaluation of single-cell foundation model interpretability: attention-derived edge scores add no incremental value over gene-level features for perturbation-target prediction. BMC Genomics 2026. https://doi.org/10.1186/s12864-026-12965-8
86. Benchmarking Static Gene Regulatory Network Reconstruction and Dynamic Transition Probing in Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.05.17.725083
87. PerturBench: Benchmarking Machine Learning Models for Cellular Perturbation Analysis. Neural Information Processing Systems 2024. https://doi.org/10.48550/arXiv.2408.10609
88. Benchmarking algorithms for generalizable single-cell perturbation response prediction.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02980-0
89. Genetic Perturbation Prediction Models Fail Out-of-Distribution: A Rigorous Benchmark and Systematic Evaluation.  . https://doi.org/10.64898/2026.10.16.759604
90. Deep learning perturbation models can outperform baselines on calibrated metrics.. Nature biotechnology . https://doi.org/10.1038/s41587-026-03307-w
91. BioLLM: A standardized framework for integrating and benchmarking single-cell foundation models. bioRxiv 2024. https://doi.org/10.1016/j.patter.2025.101326
92. scArchon: a scalable benchmarking framework for assessing single-cell perturbation models.. Genome biology 2026. https://doi.org/10.1186/s13059-026-04104-z
93. JUMP-lite: Compact, reproducible benchmarking of cell representations.  2026. https://arxiv.org/abs/2608.07632
94. Standardized metrics for assessment and reproducibility of imaging-based spatial transcriptomics datasets.. Nature biotechnology 2025. https://doi.org/10.1038/s41587-025-02811-9
95. Robustness to nuisance perturbations enables unsupervised evaluation of single-cell foundation models. bioRxiv 2026. https://doi.org/10.64898/2026.08.22.746357
96. Benchmarking atlas-level data integration in single-cell genomics. Nature Methods 2020. https://doi.org/10.1038/s41592-021-01336-8
97. Integrated multimodal cell atlas of Alzheimer's disease.. Nature neuroscience 2024. https://doi.org/10.1038/s41593-024-01774-5
