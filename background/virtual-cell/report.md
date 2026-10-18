# 虚拟细胞与扰动响应预测 · 方向背景报告

证据 46 篇 · 覆盖度 0.56 · 第 7 轮 · 更新 2026-10-18

## 本次变更

- 新增 [22] PerturbBridge: Direct Phenotypic Supervision for Cellular Perturbation Generation

## 摘要（TL;DR）

- 扰动响应生成模型的方法路线大致可分为潜空间扰动向量、扩散/流匹配生成式去噪、基础模型预训练加下游适配三类，早期 scGen 用变分自编码器在潜空间学习扰动向量奠定范式 [1]。
- scGPT 在超3300万个细胞上预训练生成式 Transformer 并迁移适配下游任务，报告在扰动响应预测等任务上表现优异 [2]。
- Tahoe-x1 将扰动训练的单细胞基础模型扩展到最高30亿参数，报告计算效率比先前细胞状态模型实现高3–30倍并在四个疾病相关基准上达到最先进性能 [3]。
- 扩散与流匹配成为当前扰动生成主流形式但设计分歧明显：OCOO-T 以极简 Transformer 直接作用于连续表达谱达到最先进性能 [4]，而 X-Cell 用扩散语言模型整合多模态先验并构建含2560万扰动单细胞、16种生物学情境的 X-Atlas/Pisces 数据集，报告在 Pearson Δ 等指标上优于现有最先进模型最高达五倍 [5]。
- SCALE 指出对照与处理细胞是非配对群体，用集合式潜传输绕开细胞级匹配，在 CRISPR 数据7项指标上优于竞争方法且预测的细胞因子差异经3名供体 PBMC 实验验证 [6]。
- 有工作证明利用知识图谱的最简 KNN 模型在分布外扰动预测上击败几乎所有方法并在 Replogle 2022 细胞系上达到当前 SOTA，与大规模预训练和复杂生成架构路线形成直接对照 [7]。
- scKITE 的数据缩放分析显示仅用179,067个预训练样本（不足先前强模型0.5%）即在多下游任务超越 Geneformer、scGPT 等，知识增强训练带来平均28.8%相对提升 [8]。
- 预测目标从静态表达谱向轨迹与调控机制延伸：State 用1.67亿细胞训练细胞嵌入并报告大型数据集上效应区分度提升超过30% [9]，PerturbGen 训练于超1亿单细胞转录组预测扰动如何塑造下游状态与轨迹 [10]。
- 评估与泛化仍是薄弱环节，各研究验证范围差异很大（如 D²R² 仅在两个数据集验证且排序依赖推断的 GRN 质量 [11]，scDEFT 仅在 IBD 两药类验证 [12]），当前报告的领先幅度多建立在各自选定基准上、跨研究可比性尚不充分。
- 评测效度批判显示简单基线常反超基础模型：在单/双基因扰动转录组预测上五种基础模型与两种深度学习模型没有任何模型优于简单基线 [13]，而另一研究则主张在良好校准指标下深度学习扰动模型可优于无信息基线，争议核心在于何种指标才算有效证据 [14]。
- 预训练规模研究用2220万细胞预训练400个模型、开展6400次实验，发现性能在远小于现有语料的数据规模即达平台期、无明确数据缩放定律 [15]。
- 世界模型愿景与实证存在张力：Chreode 用一步式细胞世界模型在240万细胞小鼠胚胎图谱、7个数据集上预训练并把 DE20 MSE 从0.2121降至0.1858，但明确只做预测建模、不声称具备规划能力 [16]，而 Cell 的愿景论文主张虚拟细胞世界模型需支持动作条件仿真、反事实推理与长程规划却未报告任何定量结果 [17]。
- 数据资源从单一组学向多模态多尺度扩展：Tahoe-100M 汇集1亿转录组、50个癌细胞系、1100种药物-剂量条件 [18]，基因组规模 Perturb-seq 覆盖>250万人类细胞 [19]，原代细胞工作在4名供体的2200万原代人CD4+T细胞上开展全表达基因扰动 [20]，其规模数字来自不同研究设计、不宜直接比较。
- 图像型虚拟细胞暴露新问题：CellFluxRL 指出图像生成方法可能产生违反物理与生物约束的细胞图像并用强化学习后训练设计三类共七个奖励 [21]，PerturbBridge 批评仅匹配真实图像分布、提出随机数据到数据桥模型在 BBBC021 上 MoA 准确率77.8%（CellProfiler）/74.9%（DINOv2）、较 CellFlux 提升5.7/7.5个百分点 [22]。
- AIVC 综述提出跨尺度表征工程、功能子模块设计与多组件动态调控机制的统一技术框架并列举 GeneCompass、Tahoe-100M 等资源，但指出数据异质性与模型可解释性等挑战尚未解决 [23]。

## 1 背景与定义

虚拟细胞与扰动响应预测的边界，首先由“预测什么”来划定。它不等同于常规单细胞分析流程，也不止于对扰动后表达谱的静态拟合：一类工作把扰动视为对细胞状态的操作，学习从对照群体到处理群体的条件分布转移，SCALE 明确以“对照与处理细胞为非配对群体”为前提，用集合式条件传输绕开细胞级配对 [6]；另一类工作把细胞建成可迭代的状态转移系统，Chreode 以一步式结构化残差转移算子直接生成动作条件下的状态转移 [16]，而 Cell 的愿景论文则主张虚拟细胞应是多模态、多尺度、有状态的动态计算系统，世界模型需支持动作条件仿真、反事实推理与长程规划 [17]。**这三者共享“扰动—状态—响应”的问题骨架，但在是否要求规划能力、是否要求机制可解释上分歧明显**，构成本方向内部的第一条定义性张力。

演化脉络上，方法重心经历了从潜空间扰动向量到生成式去噪、再到规模化预训练与知识注入的迁移。scGen 用变分自编码器在潜空间加减扰动向量，奠定了跨细胞类型与跨物种响应预测的范式 [1]；此后扩散与流匹配成为主流建模形式，OCOO-T 以极简 Transformer 直接作用于连续表达谱、把预测建模为连续时间去噪 [4]，X-Cell 则以扩散语言模型整合自然语言、蛋白质语言模型与互作网络等多模态先验 [5]。与之并行的是基础模型路线，scGPT 在超3300万细胞上预训练并迁移至下游任务 [2]，Speciesformer 在1.31亿细胞的 SpeciesCorpus 上学习跨物种可迁移细胞状态 [24]。**值得注意的是，这条“越大越复杂”的主线始终伴随反向证据**：知识图谱加最简 KNN 在 Replogle 2022 上达到当前 SOTA [7]，scKITE 仅用179,067个预训练样本即在多下游任务超越 Geneformer、scGPT 等 [8]，说明知识组织方式可能比参数量更关键。

核心问题的第一层是数据统计形态与建模假设的错配。扰动数据普遍存在非配对、类别严重不平衡、扰动特异性方差低等特征，而多数模型默认配对或均衡。SCALE 把非配对当作建模前提而非噪声 [6]，scBalFlow 用两阶段解耦训练显式纠偏弱响应样本 [25]，二者路径不同但都承认**数据组织方式本身是方法设计的一部分**。第二层是预测目标从静态表达谱向轨迹、调控机制与跨模态迁移延伸：PerturbGen 预测扰动如何塑造下游状态与轨迹 [10]，D-SPIN 从跨数千扰动条件推断可解释的生成式调控网络 [26]，RegVelo 联合建模剪接动力学与基因调控互作 [27]，UniPert-G2CP 则尝试遗传到化学的表型迁移 [28]。**目标越靠近机制与轨迹，对数据和验证的要求越高，而当前证据多来自各自选定的基准**。

第三层、也是最尖锐的核心问题，是评测效度本身。细胞级随机划分会因同克隆、同患者细胞共享标签而泄漏答案，暴露度决定泄漏通道、可检索性决定分数膨胀 [29]；而“简单基线反超”在多处被独立报告：五种基础模型与两种深度学习模型没有任何模型优于简单基线 [13]，Train Mean 即优于 scGPT 与 scFoundation [30]，perturbed mean 在 Pearson Δ 上跨所有数据集优于其他方法 [31]，基线在五个评分维度中的四个匹配或超过所有基础模型 [32]。与之直接对立的是指标校准派的结论：MSE、Pearson Δ 等常用指标常校准不良，在良好校准指标下深度学习扰动模型可优于无信息基线 [14]。**争议核心因此不在“模型行不行”，而在“用什么指标、在什么划分下才算有效证据”**；AssayBench 发现零样本通用 LLM 优于生物学专用 LLM [33]、药物盲评估显示单药泛化主要限于同类内 [34]，进一步说明任务定义与泛化目标尚未收敛。

数据资源与产业侧的可核验发布，正在把上述问题从方法层推向基础设施层。Tahoe-100M 以1亿转录组、50个癌细胞系、1100种药物-剂量条件构成十亿级单细胞扰动图谱 [18]，基因组规模 Perturb-seq 覆盖超250万人类细胞 [19]，原代 CD4+T 细胞工作在4名供体、2200万细胞上开展全表达基因扰动 [20]；空间与体内维度则由 SPAC-seq [35] 与 iGOF-Perturb-seq [36] 拓展。与资源建设同步，评测基础设施开始成形：Virtual Cell Challenge 提供评估框架、专用数据集与模型开发平台 [37]，2026 届转向跨多个独立细胞情境的零样本预测 [38]；scArchon 以容器化流程标准化评估九种工具，但仅限非遗传扰动 [39]。**这些资源的规模数字来自不同研究设计，不宜直接比较；其真正价值取决于能否支撑分组验证与跨情境外推，而这恰是当前最薄弱的一环** [29][15]。

最后需要明确本方向的开放边界。闭环智能体目前落在“模型精炼”而非“状态推演”：CellScientist 把执行偏差路由回假设或实现层面形成假设—实现—假设闭环，并留下可审计轨迹，但依赖 LLM 代理、长程工作流仍脆弱 [40]；而世界模型愿景所要求的反事实推理与长程规划，尚无定量结果支撑 [17]。因果解释同样受限：单细胞 CRISPR 综述强调统计关联需附加因果假设，且仅能识别敲低对另一基因的效应而非基因间直接因果 [41]。**因此，本方向的合理定义应包含三层：可复现的扰动响应预测模型、能暴露失效模式的评测基准、以及支撑跨情境外推的数据资源；而“细胞世界模型”目前更接近一个定义性目标而非已兑现的能力**，其与预测型模型之间缺少同一基准下的对照证据 [16][17][40]。

## 2 方法学


### 2.1 扰动响应生成模型

扰动响应生成模型的方法路线大致可分为三类：以变分自编码器为代表的潜空间扰动向量方法、以扩散/流匹配为代表的生成式去噪方法，以及以基础模型预训练加下游适配为代表的规模化路线。早期工作 scGen 用变分自编码器在潜空间学习扰动向量，通过在潜空间中加减扰动向量实现跨细胞类型与跨物种的响应预测，为后续工作奠定了范式 [1]。此后 scGPT 将生成式预训练 Transformer 用于单细胞多组学，在**超3300万个细胞**上预训练并通过迁移学习适配下游任务，报告在扰动响应预测等任务上表现优异 [2]。规模化路线进一步推进：Tahoe-x1 将扰动训练的单细胞基础模型扩展到**最高30亿参数**，预训练数据包括 Tahoe-100M 扰动汇编，报告计算效率比先前细胞状态模型实现高**3–30倍**，并在四个疾病相关基准上达到最先进性能 [3]；Speciesformer 则在包含**1.31亿细胞**的 SpeciesCorpus 上预训练，目标是跨物种生成虚拟细胞状态并区分保守原理与物种/组织特异变异 [24]。

扩散与流匹配成为当前扰动生成的主流建模形式，但具体设计分歧明显。OCOO-T 主张极简架构，用普通 Transformer 直接作用于连续基因表达谱，将扰动响应预测建模为连续时间去噪过程，通过自适应层归一化和上下文 token 整合扰动、剂量与细胞系信息，在 Tahoe100M、Replogle、PBMC 上达到最先进性能 [4]。X-Cell 则走多模态先验路线，用扩散语言模型通过交叉注意力整合自然语言、蛋白质语言模型、互作网络等先验，配套构建了含**2560万扰动单细胞、16种生物学情境**的 X-Atlas/Pisces 数据集，报告在 Pearson Δ 等指标上优于现有最先进模型**最高达五倍**并展示零样本预测能力 [5]。D²R² 提出另一维度的重构：把预测拆成调控引导的基因级渐进生成，用掩码离散扩散以序数 token 逐步重建表达谱，并由对照细胞 GRN 初始化、经组相对策略优化微调生成排序，在 Norman19 五项指标最优、H1 具竞争力，消融显示生物先验排序优于随机与不确定性启发式 [11]。这些工作对"是否值得引入复杂先验与辅助结构"存在张力：OCOO-T 明确以降低架构复杂度为动机 [4]，而 X-Cell 与 D²R² 均把外部生物学知识作为核心组件 [5][11]。

针对扰动数据本身的统计缺陷，近期工作转向训练目标与数据组织方式的改造。SCALE 指出对照与处理细胞是**非配对群体**，因而将细胞表示为无序集合、用条件 DiT 骨干学习潜传输，使端点监督直接 delta 对齐而无需细胞级匹配，在 CRISPR 数据**7项指标**上优于竞争方法，其预测的细胞因子差异经**3名供体** PBMC 实验验证 [6]。scBalFlow 针对药物扰动数据的严重类别不平衡导致偏向弱响应样本的问题，采用两阶段解耦训练：第一阶段预测响应强度并用高斯增强推断缓解不平衡，第二阶段跳过弱响应条件、用 Flow Matching 合成高响应样本，在 SciPlex3 和 McFarland 等基准上显著优于现有 SOTA [25]。两者都承认非配对或失衡是建模前提而非噪声，但 SCALE 通过集合式传输绕开配对，scBalFlow 则通过显式重加权响应强度来纠偏 [6][25]。

一个值得注意的争议是模型复杂度与性能是否匹配。有工作证明，利用知识图谱的最简 KNN 模型在分布外扰动预测上击败几乎所有方法，并用强化学习优化推理 LLM 调整邻域，在 Replogle 2022 细胞系上达到当前 SOTA 水平，RL 训练还提升了 LLM 在差异表达预测上的表现 [7]。这与大规模预训练和复杂生成架构的路线形成直接对照，提示知识先验的组织方式可能比参数量更关键。类似地，scKITE 的数据缩放分析显示，引入细胞级文本注释与基因级调控信息提供了额外的缩放维度，仅用**179,067个预训练样本（不足先前强模型0.5%）**即在多下游任务超越 Geneformer、scGPT 等，知识增强训练带来平均**28.8%**相对提升 [8]。

在预测目标上，工作从静态表达谱向轨迹与调控机制延伸。State 强调跨实验的细胞异质性，用单细胞基因表达数据训练预测细胞集合的扰动效应，细胞嵌入训练于**1.67亿细胞**，报告大型数据集上效应区分度提升**超过30%**，并引入 Cell-Eval 评估框架 [9]。PerturbGen 训练于**超1亿单细胞转录组**，预测源状态遗传扰动如何塑造下游状态与轨迹，在免疫挑战、造血与皮肤发育三套数据中预测 IL1B 敲除减弱后续细胞因子-干扰素程序，与 IL-1β 刺激逆转一致 [10]。D-SPIN 从跨数千扰动条件的单细胞 mRNA-seq 推断机制可解释的生成式调控网络，解释扰动如何改变细胞状态比例，并模拟未观测剂量组合下的免疫细胞群结构变化 [26]；RegVelo 联合建模剪接动力学与基因调控互作，结合计算机扰动、CRISPR-Cas9 敲除和 Perturb-seq 验证，确立 tfec 为早期驱动因子、elf1 为色素细胞命运调控因子 [27]。TFActProfiler 则从资源侧切入，整合 ChIP、motif 与 curated 先验及大规模 RNA-seq 学习带符号定量 TF–mRNA 系数，在多细胞类型 TF 敲低基准上优于现有 TF 活性推断方法，且无需额外训练即可预测 TF 扰动转录组响应 [42]。

药物与化学扰动方向强调条件化与跨模态迁移。scDEFT 把药物视为细胞表征的条件算子，用特征级线性调制生成药物条件化潜变量，冻结后由两个独立头按转录邻域聚合预测状态变化与应答状态，在**116万细胞** IBD 图谱（3队列2类药物、51供体）上状态变化预测达 headroom 的**45%**，治疗前应答分层 AUROC **0.70**，而标准预测器仅达随机水平 [12]。UniPert-G2CP 用两阶段框架统一多模态分子扰动表征，实现遗传到化学的表型迁移学习，在大规模遗传与化学筛选数据上验证并揭示药物响应异质性与耐药机制 [28]。图像型虚拟细胞则暴露了另一类问题：CellFluxRL 指出图像生成方法可能产生违反物理与生物约束的细胞图像，因而用强化学习后训练，设计生物功能、结构有效性与形态正确性三类共**七个奖励**，在所有奖励上优于基线 CellFlux [21]；PerturbBridge 进一步批评仅匹配真实图像分布、未显式优化扰动特异性生物响应，提出随机数据到数据桥模型在训练中直接施加表型监督，在 BBBC021 上 MoA 准确率**77.8%（CellProfiler）/74.9%（DINOv2）**，较 CellFlux 提升**5.7/7.5个百分点**，JUMP Hit@10 为**12.15%**，AllenCell Hit@1 为**69.29%** [22]。

评估与泛化仍是未解决的薄弱环节。多个工作把"外推能力"作为核心卖点：X-Cell 强调现有方法依赖观察性图谱而非干预数据、难以外推 [5]，State 强调跨细胞环境泛化 [9]，OCOO-T 则承认基于扩散/流匹配的方法学习对照到扰动分布仍具挑战 [4]。但各研究的验证范围差异很大：D²R² 仅在两个数据集验证且排序策略依赖推断的 GRN 质量 [11]，scDEFT 仅在 IBD 两药类验证、归因结果为待实验验证的假设 [12]，CellFluxRL 仅验证于 CellFlux 一种生成框架且奖励为加权线性组合、权重依赖人工 [21]。这些限制说明，当前报告的领先幅度多建立在各自选定的基准与指标上，跨研究、跨数据分布的可比性尚不充分。

### 2.2 细胞世界模型与闭环智能体

在预测细胞状态转移的建模路径上，Chreode 把分布演化从推理阶段前移到训练阶段，用**一步式细胞世界模型**配合结构化残差转移算子，直接生成动作条件下的细胞状态转移，从而避免逐数据集求解多步 ODE 或 Schrödinger 桥问题[16]。该工作在 **240万细胞小鼠胚胎图谱、7个数据集**上预训练，并在 GEARS 扰动预测上把 DE20 MSE 从 **0.2121 降至 0.1858**（相对提升 12.4%），在 Weinreb 与 Veres 上 Sinkhorn 距离优于匹配的从头训练模型[16]。不过作者明确只做预测建模，不声称具备规划或推演能力[16]。与之相对，Cell 的愿景论文主张虚拟细胞应是多模态、多尺度、有状态的动态计算系统，世界模型作为操作框架需支持动作条件仿真、反事实推理与长程规划，并强调建模底层细胞系统本身、让干预在演化状态中传播，而非只优化特定任务端点[17]。两者构成明显张力：前者以单步预测精度为落点并主动放弃规划主张，后者以规划与反事实能力为定义性目标却未报告任何定量结果，属无实验验证的架构与评估原则提案[16][17]。

闭环方向的证据落在模型精炼而非状态推演上。CellScientist 针对预测失败难以归因的“精炼路由”问题，把高层假设空间与低层可执行实现空间耦合，将执行偏差路由回假设或实现层面的定向更新，形成假设—实现—假设闭环[40]。在形态学与转录组基准及单细胞扰动评估中，案例里 PCC 由 **0.3416 提升至 0.4368**，最终可执行模型在固定划分与评估协议下优于参考基线，并留下可审计的精炼轨迹[40]。其局限在于精炼依赖 LLM 代理、长程工作流仍脆弱[40]。三篇工作因此分处不同子问题：单步扰动预测、虚拟细胞世界模型的架构愿景、以及模型自身的迭代修正；目前尚无用同一基准同时检验“世界模型式推演”与“预测型模型”的对照证据，愿景与实证之间的差距仍是该方向的开放争议[16][17][40]。

## 3 数据与资源

虚拟细胞与扰动响应预测所依赖的数据资源，正从单一组学向多模态、多尺度扩展。在转录组层面，**Tahoe-100M** 汇集了 **1亿转录组**、**50个癌细胞系**、**1100种药物-剂量条件**，借助 Mosaic 平台将遗传上不同的细胞模型多重化为平衡的"细胞村"，实现低批次效应的并行单细胞扰动分析，并系统量化增殖、细胞毒性、谱系特异性脆弱性与细胞周期变化 [18]。与之互补，基因组规模 Perturb-seq 以 CRISPRi 靶向全部表达基因、覆盖 **>250万人类细胞**，用转录表型预测功能未知基因并识别非整倍体的遗传驱动因素与后果 [19]；而针对原代细胞的工作则在 **4名供体** 的 **2200万原代人CD4+T细胞** 上开展全表达基因扰动，开发探针式 perturb-seq 平台，测量静息与刺激后的转录组效应 [20]。这三项工作在细胞体系（癌细胞系、原代T细胞）、扰动方式（药物、CRISPRi）与读出维度上各不相同，其规模数字来自不同研究设计，不宜直接比较。

在空间与体内维度，证据显示扰动筛选正走出体外细胞系。**SPAC-seq** 作为高通量空间 CRISPR 筛选平台，配合 TARDIS 统计分析工具，将基因扰动与空间表型和通路关联，揭示 Icam1 缺失经免疫抑制促转移、Cd44 调控空间表型以及转录因子-趋化因子受体轴 [35]。**iGOF-Perturb-seq** 则采用体内功能获得性扰动测序，在小鼠星形胶质细胞中构建 **约1000个转录因子** 的功能图谱，识别共功能模块并注释未表征 TF，并在神经炎症模型中鉴定 Ferd3l 为治疗候选 [36]。两者分别代表空间分辨与体内细胞类型特异两条路线，但前者未明确说明平台通量与适用组织范围的限制，后者限于小鼠模型与星形胶质细胞，向人类转化仍需验证 [35][36]。

面向预测建模，资源建设开始与模型架构协同设计。**ProteinTalks** 基于 **3800万+条时序蛋白丰度测量** 的扰动乳腺癌细胞系数据，通过大规模动态蛋白质组资源与架构的协同学习可迁移的动态潜表示，在药物疗效与协同预测、耐药蛋白发现、患者分层及类器官候选药物排序上普遍优于所选基准，并可迁移至患者类器官与临床活检 [43]。与之配套的评估基础设施亦在形成：Arc Institute 建立的 **虚拟细胞挑战赛** 提供评估框架、专用数据集与模型开发平台，作为反复举办的开放基准竞赛，推动预测细胞扰动响应这一目标 [37]。值得注意的是，上述模型与基准多基于特定细胞体系（如乳腺癌细胞系）或尚未报告定量结果，其泛化能力与可比性仍是待解问题 [43][37]。

## 4 评测与效度批判

评测效度批判的第一条主线是数据划分与泄漏。单细胞数据具有分组结构，同克隆、同患者或同批次的细胞共享标签，细胞级随机划分会把测试细胞的“亲属”连同标签放进训练集，模型可以靠记忆亲属而非学习可迁移规则取得高分；**暴露度决定泄漏通道，可检索性决定分数膨胀**，在患者队列中泄漏足以推翻临床结论 [29]。分组验证能消除泄漏，但会留下远更少的独立样本 [29]。与此相关，VCBench 指出**没有基础模型发布完整细胞级训练清单**，数据污染对用户不可检测 [32]。

第二条主线是“简单基线反超”。在单/双基因扰动转录组预测上，五种基础模型与两种深度学习模型**没有任何模型优于简单基线**，研究识别出 **5,035 个遗传互作**（潜在 124,000）[13]。在 Perturb-seq 扰动后表达预测中，最简单的 Train Mean 即优于 scGPT 与 scFoundation，带 GO 特征的随机森林大幅领先（如 Replogle K562 上 RF+GO 的 Pearson Delta 为 **0.480**，Train Mean 为 0.373，scGPT 为 0.327）[30]；该文同时指出当前 Perturb-Seq 基准数据**扰动特异性方差低**，不适合评估此类模型 [30]。Systema 在十个数据集、三种技术、五种细胞系上发现，**perturbed mean 在 Pearson Δ 上跨所有数据集优于其他方法**，双基因扰动中 matching mean 显著更优，常见指标高估性能 [doi:10.1038/s41587-026-03307-w 之外的 doi:10.1038/s41587-025-02777-8]。VCBench 评估五种基础模型，**基线在五个评分维度中的四个匹配或超过所有基础模型**，TranscriptFormer 跨模态 RNA 到蛋白预测 Pearson 提升 **53%**，但时间排序性能崩溃 [32]。

第三条主线是评估设置本身失真。标准化模块化基准发现，常用设置下性能被高估，严格条件下性能显著下降，简单线性模型仅捕捉全局转录趋势、无法恢复细粒度扰动特异效应，且不同指标导致模型排名差异显著 [44]。scArchon 以容器化可复现流程标准化评估九种工具，但**仅限非遗传扰动**，基因敲除作为独立问题未纳入 [39]。大规模系统比较覆盖 25 个数据集、13 个方法，发现扰动效应幅度强烈影响泛化与双扰动预测，细胞类型迁移中源-目标转录组距离越大准确率越低 [45]。药物盲评估则显示模型通常能做癌症盲预测，但**药物盲性能显著下降、部分模型完全失败**，单药药物盲泛化主要限于同类内 [34]。

第四条主线是任务与指标定义的分歧。AssayBench 基于 **1920 个 CRISPR 筛选**、五类表型构建基准，发现零样本通用 LLM 优于生物学专用 LLM 和可训练基线，现有方法远未达经验性能上限 [33]。与之相对，有研究提出阳性对照基线与指标校准框架，在 **14 个数据集、18 个指标**上发现 MSE、Pearson Δ 等常用指标常校准不良、降低对阳性模型性能的敏感性，在良好校准指标下深度学习扰动模型可优于无信息基线 [14]。这构成与前述“基线反超”结论的直接张力：一方归因于模型能力不足，另一方归因于指标校准缺陷，争议核心在于何种指标才算有效证据。

最后是泛化目标与因果解释的边界。Virtual Cell Challenge 2026 转向跨多个独立细胞情境的零样本预测，在新 Arc 数据集上预测未见细胞系中的基因敲低响应，目标是检验最优模型能否缩小临床前预测与人类生物学之间的差距 [38]。预训练规模研究用 **2220 万细胞**预训练 400 个模型、开展 **6400 次实验**，发现性能在远小于现有语料的数据规模即达平台期，**无明确数据缩放定律** [15]。因果层面，单细胞 CRISPR 综述强调统计关联需附加因果假设才能解释为因果效应，且仅能识别一个基因敲低对另一基因的效应，无法直接推断两基因间因果效应 [41]；而基于 Perturb-seq 表型流形的工作则主张流形可实现通路无偏排序与遗传互作的原则性分类，但其依赖生长表型挖掘强互作、覆盖有限 [46]。

## 5 产业动态

（本节暂无入库证据）

## 6 空白与趋势

综合上述证据，本方向的空白与趋势可归纳为以下六条。

1. **“世界模型”愿景与单步预测实证之间存在结构性缺口，尚无用同一基准同时检验两者的对照研究。** 一方面，Cell 的愿景论文把虚拟细胞定义为多模态、多尺度、有状态的动态系统，要求支持动作条件仿真、反事实推理与长程规划，并明确主张应建模底层细胞系统本身而非只优化任务端点，但该文未报告任何定量结果 [17]。另一方面，Chreode 虽自称细胞世界模型，却明确只做预测建模、不声称具备规划或推演能力 [16]；CellScientist 的闭环落在模型自身的假设—实现迭代修正上，而非细胞状态的推演 [40]。**三者分处单步扰动预测、架构愿景与模型精炼三个子问题，彼此不可互证**，这是该方向最核心的开放争议。

2. **评测效度批判已积累足够证据，但批判结论尚未转化为被广泛采纳的评估协议。** 细胞级随机划分会因同克隆、同患者细胞共享标签而泄漏答案，暴露度决定泄漏通道、可检索性决定分数膨胀，患者队列中泄漏足以推翻临床结论 [29]；VCBench 指出没有基础模型发布完整细胞级训练清单，数据污染对用户不可检测 [32]；AssayBench 发现零样本通用 LLM 优于生物学专用 LLM 与可训练基线 [33]；标准化模块化基准发现常用设置高估性能、不同指标导致排名差异显著 [44]。**这些批判各自成立，但缺少一个同时纳入分组划分、污染审计与多指标校准的统一评测**；scArchon 虽提供容器化可复现流程，却仅限非遗传扰动，基因敲除作为独立问题未纳入 [39]。

3. **“简单基线反超”与“指标校准缺陷”两种解释形成直接张力，争议未决。** 一方报告五种基础模型与两种深度学习模型没有任何模型优于简单基线，并识别出 5,035 个遗传互作 [13]；Train Mean 即优于 scGPT 与 scFoundation，且当前 Perturb-Seq 基准数据扰动特异性方差低、不适合评估此类模型 [30]；Systema 在十个数据集上发现 perturbed mean 在 Pearson Δ 上跨所有数据集优于其他方法 [31]。另一方则在 14 个数据集、18 个指标上发现 MSE、Pearson Δ 等常用指标常校准不良，在良好校准指标下深度学习扰动模型可优于无信息基线 [14]。**两方对同一现象给出能力不足与指标缺陷两种归因，目前没有工作在同一数据上同时执行两套评估以裁决分歧**，这是方法学上最值得填补的空白。

4. **知识先验的组织方式可能比参数规模更关键，但这一线索尚未被系统化。** 利用知识图谱的最简 KNN 模型在分布外扰动预测上击败几乎所有方法，经 RL 优化邻域后在 Replogle 2022 细胞系上达到当前 SOTA [7]；scKITE 仅用 179,067 个预训练样本（不足先前强模型 0.5%）即在多下游任务超越 Geneformer、scGPT 等，知识增强训练带来平均 28.8% 相对提升 [8]；预训练规模研究用 2220 万细胞预训练 400 个模型、开展 6400 次实验，发现性能在远小于现有语料的数据规模即达平台期、无明确数据缩放定律 [15]。**三条证据指向同一方向，但尚无工作把“知识先验强度”作为可控变量与“数据/参数规模”做正交比较**，因而无法判断何时该加知识、何时该加规模。

5. **扰动数据资源在细胞体系、扰动模态与读出维度上高度异质，跨资源整合与可比性仍是空白。** Tahoe-100M 覆盖 1 亿转录组、50 个癌细胞系、1100 种药物-剂量条件 [18]；基因组规模 Perturb-seq 覆盖 >250 万人类细胞 [19]；原代 CD4+T 细胞工作在 4 名供体的 2200 万细胞上开展 [20]；X-Atlas/Pisces 含 2560 万扰动单细胞、16 种生物学情境 [5]；空间与体内维度则有 SPAC-seq [35] 与 iGOF-Perturb-seq 的约 1000 个转录因子图谱 [36]；蛋白层面有 3800 万+条时序蛋白丰度测量支撑的 ProteinTalks [43]。**这些资源的规模数字来自不同研究设计、不宜直接比较，而目前缺少跨资源统一本体与统一扰动编码的工作**，使“多资源联合训练”难以被严格评估。

6. **泛化目标正从同分布外推转向跨细胞情境零样本，但因果解释的边界尚未与预测能力对齐。** Virtual Cell Challenge 2026 已转向跨多个独立细胞情境的零样本预测，要求在新 Arc 数据集上预测未见细胞系中的基因敲低响应 [38]；药物盲评估显示模型通常能做癌症盲预测，但药物盲性能显著下降、部分模型完全失败，单药药物盲泛化主要限于同类内 [34]；系统比较亦发现细胞类型迁移中源-目标转录组距离越大准确率越低 [45]。与此同时，单细胞 CRISPR 综述强调统计关联需附加因果假设才能解释为因果效应，且仅能识别一个基因敲低对另一基因的效应 [41]。**预测精度提升与因果可解释性之间缺少桥接工作**：现有模型多在报告预测指标，而因果主张仍停留在附加假设层面，二者未被同一框架同时检验。

## 7 未归类新证据

人工智能虚拟细胞（AIVC）被提出作为整合多组学数据、理解跨尺度动态生物事件的新研究范式，其基本设想是细胞通过微观分子机制与宏观组织构型之间的相互作用协调生命活动，而传统实验与生化分析受时空分辨率与处理能力限制，难以刻画这类动态跨尺度过程 [23]。该综述给出的统一技术框架从**跨尺度表征工程**、功能子模块设计与多组件动态调控机制三个方面进行分解，并系统梳理了现有模型与数据集资源，文中列举的资源包括 **GeneCompass、Tahoe-100M** 等 [23]。

在方法定位上，这是一篇汇总现有模型与数据集、未自行分析样本的综述，其贡献在于提出 AIVC 的统一定义与技术框架，而非提供新的预测结果 [23]。作者同时指出该方向仍处早期阶段，**数据异质性与模型可解释性**等挑战尚未解决，但认为其有望推动生命科学从观测分析转向可预测与创新的范式 [23]。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 扰动响应生成模型（flow matching / 扩散 / 因果潜动力学） | 朝阳 | [1] 用 VAE 潜空间做扰动响应迁移，是这一路线的早期范式；[2] 把单细胞基础模型推到多组学预训练，成为后续扰动预测的通用底座；[9] 与 [5] 在 2026 年同时提出跨细胞情境的因果扰动预测与规模化扩展，说明方法仍在快速换代、尚未收敛。 |
| 细胞世界模型与闭环智能体 | 萌芽 | [16] 提出一步式时序动力学与扰动预测的 cell world model；[17] 以 perspective 形式提出「虚拟细胞的世界模型」框架；[40] 做闭环精炼的智能体编排。三者均为 2026 年新出、引用近零，属概念先行、缺大规模验证。 |
| 扰动数据资源（Perturb-seq 图谱、Tahoe、Virtual Cell Challenge） | 朝阳 | [19] 建立基因组尺度 Perturb-seq 基因型-表型图谱，成为训练数据基座；[37] 以 Virtual Cell Challenge 形式给出「虚拟细胞图灵测试」的公共评测与数据接口；[35] 把 CRISPR 筛选推进到空间分辨功能基因组学，数据维度仍在扩张。 |
| 评测基准与效度批判 | 朝阳（且已出现强负面结论） | [13] 直接证明深度学习扰动预测**尚未跑赢简单基线**；[30] 系统基准显示基础细胞模型在后扰动 RNA-seq 预测上表现有限；[31] 的 Systema 把评测从「拟合表达」推进到「超越表达的效用」，说明评测口径本身在重构。 |
| 产业动态 | 证据不足 | 雷达样本中该节 **n=0**，无可核验技术细节的发布可引，无法判断阶段。 |

**整体判断**：这个方向整体处于**朝阳期偏早段**——生成模型路线近两年密集换代（[9]、[5]），数据与评测基础设施同步成型（[37]、[31]），但**方法未收敛**且已被证明「打不过简单基线」（[13]）。窗口期估计 **12–24 个月**：一旦 Virtual Cell Challenge 类公共基准把胜负标准固定下来，纯模型刷分空间会迅速收窄。最大不确定性是**效度**——现有指标是否真的对应「未见扰动/未见细胞类型」的泛化，还是只奖励了表达谱拟合；其次是数据侧的情境覆盖（[19] 类图谱多为单一细胞系/条件），跨情境外推缺乏 ground truth。

**接下来怎么做**：

1. **把「跨情境泛化」做成可证伪的评测贡献，而不是再提一个生成模型**。用 Virtual Cell Challenge 的公共划分（[37]）+ Perturb-seq 图谱（[19]）构造「留出细胞类型 / 留出扰动组合」的严格 split，复现 [13] 的基线对比并扩展到多组学输入。现在做：负面结论刚出、社区尚无统一反驳口径，先占住评测话语权成本最低。产出：基准代码 + 一篇批判性方法学论文。

2. **用类器官多组学做「真实分布外」验证集，这是你合作项目的独特筹码**。公共 Perturb-seq 多为细胞系，类器官的扰动响应在结构与状态分布上更接近体内；把 [35] 的空间分辨 CRISPR 思路与你的类器官多组学配对，构造小规模但高价值的 OOD 测试集。现在做：数据资源侧仍在扩张（[37]），谁先提供「非细胞系」评测集谁定义下一轮问题。

3. **在因果潜动力学 + 最优传输这条线上做轻量增量，而不是从头训基础模型**。以 [2] 的预训练权重为底座，接 [9] 的跨情境因果预测设定，重点改「扰动表征如何解耦」而非规模。现在做：方法未收敛（[5] 刚提出 scaling 版本），改进空间明确且算力门槛可控。产出：可复现的模块 + 在自建 OOD 集上的增益。

4. **把闭环智能体当作「实验设计器」而非「预测器」来切入**。参考 [40] 的闭环精炼与 [16] 的一步时序动力学，做一个「选下一个扰动」的主动学习策略，在类器官数据上做小规模闭环 demo（预测→选扰动→湿实验→回填）。现在做：该节仅 3 篇、全部 2026 年新出（[17]），属萌芽期，早期进入者定义任务形式。产出：公共数据 demo + 闭环协议。

5. **避开纯刷分，转向「效用评测」**。采用 [31] 的 Systema 框架，把下游任务（如药物响应排序、靶点优先级）作为评测终点，而非表达谱相关性；结合 [30] 的基准结论设定「必须超过简单基线」的准入线。现在做：评测口径正在重构（[31] 引用已起），早进入可与基准作者形成对话。产出：一套效用导向的评测脚本 + 对现有模型的批判性复评。

## 参考文献

1. scGen predicts single-cell perturbation responses. Nature Methods 2019. https://doi.org/10.1038/s41592-019-0494-8
2. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. Nature Methods 2024. https://doi.org/10.1038/s41592-024-02201-0
3. Tahoe-x1: Scaling Perturbation-Trained Single-Cell Foundation Models to 3 Billion Parameters. bioRxiv 2025. https://doi.org/10.1101/2025.10.23.683759
4. OCOO-T : A Simple and Scalable Virtual Cell Model for Transcriptional Perturbation Response Prediction.  2026. https://arxiv.org/abs/2606.12838v2
5. X-Cell: Scaling Causal Perturbation Prediction Across Diverse Cellular Contexts via Diffusion Language Models.  2026. https://doi.org/10.64898/2026.03.18.712807
6. SCALE:Scalable Conditional Atlas-Level Endpoint transport for virtual cell perturbation prediction.  2026. https://arxiv.org/abs/2603.17380v3
7. Knowledge Graphs and Reasoning LLMs for Finding Simple Yet Effective Transcriptomic Perturbation Predictors.  2026. https://arxiv.org/abs/2606.08816v1
8. Towards a knowledge-enhanced single-cell foundation model.  2026. https://arxiv.org/abs/2609.14970
9. Predicting cellular responses to perturbation across diverse contexts with State. Cell 2026. https://doi.org/10.1016/j.cell.2026.07.052
10. Predicting how perturbations reshape cellular trajectories with PerturbGen.  2026. https://doi.org/10.64898/2026.03.04.709254
11. $D^{2}R^{2}$: Discrete Diffusion with Regulation Reinforcement for Single-Cell Perturbation Prediction.  2026. https://arxiv.org/abs/2608.15288v1
12. scDEFT: A deep learning framework for drug-effect prediction and counterfactual reasoning.  2026. https://arxiv.org/abs/2609.10831
13. Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines. Nature methods 2025. https://doi.org/10.1038/s41592-025-02772-6
14. Deep learning perturbation models can outperform baselines on calibrated metrics.. Nature biotechnology . https://doi.org/10.1038/s41587-026-03307-w
15. Evaluating the role of pretraining dataset size and diversity on single-cell foundation model performance.. Nature methods 2026. https://doi.org/10.1038/s41592-026-03120-y
16. Chreode: A Cell World Model for One-Step Temporal Dynamics and Perturbation Prediction.  2026. https://arxiv.org/abs/2605.28111v1
17. A world model of the virtual cell.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.042
18. Tahoe-100M: Mapping drug-induced molecular phenotypes at single-cell resolution.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.035
19. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. bioRxiv 2021. https://doi.org/10.1016/j.cell.2022.05.013
20. Genome-scale perturb-seq in primary human CD4&lt;sup&gt;+&lt;/sup&gt; T cells maps context-specific regulators of T cell programs and human immune traits.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.002
21. CellFluxRL: Biologically-Constrained Virtual Cell Modeling via Reinforcement Learning.  2026. https://arxiv.org/abs/2603.21743v4
22. PerturbBridge: Direct Phenotypic Supervision for Cellular Perturbation Generation.  . https://arxiv.org/abs/2610.17066
23. Artificial intelligence-enabled multi-scale virtual cell: perspective, challenges, and opportunities.. Briefings in bioinformatics 2026. https://doi.org/10.1093/bib/bbag104
24. Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling.  . https://doi.org/10.64898/2026.09.22.752128
25. scBalFlow: A Staged Flow Matching Framework for Imbalanced Single-Cell Drug Perturbation Prediction.. Bioinformatics (Oxford, England) 2026. https://doi.org/10.1093/bioinformatics/btag682
26. D-SPIN constructs regulatory network models from scRNA-seq that reveal organizing principles of perturbation response.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.028
27. RegVelo: Gene-regulatory-informed dynamics of single cells.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.022
28. UniPert-G2CP bridges genetic and chemical screens from molecular representation to phenotype modeling.. Cell 2026. https://doi.org/10.1016/j.cell.2026.06.005
29. Cell-level random splits leak group-owned answers in single-cell benchmarks. bioRxiv 2026. https://doi.org/10.64898/2026.09.09.750484
30. Benchmarking foundation cell models for post-perturbation RNA-seq prediction. BMC genomics 2025. https://doi.org/10.1186/s12864-025-11600-2
31. Systema: a framework for evaluating genetic perturbation response prediction beyond systematic variation. Nature biotechnology 2026. https://doi.org/10.1038/s41587-025-02777-8
32. VCBench: A Multi-Dimensional Benchmark for Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.06.18.733146
33. AssayBench: An Assay-Level Virtual Cell Benchmark for LLMs and Agents.  2026. https://arxiv.org/abs/2605.10876v1
34. Monotherapy cancer drug-blind response prediction is limited to intraclass generalization.. PLoS computational biology 2026. https://doi.org/10.1371/journal.pcbi.1013232
35. Uncovering spatially resolved functional genomics with CRISPR screen sequencing.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.049
36. Mapping transcription factor functions in astrocytes using in vivo gain-of-function Perturb-seq.. Science (New York, N.Y.) 2026. https://doi.org/10.1126/science.adw2156
37. Virtual Cell Challenge: Toward a Turing test for the virtual cell. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.008
38. Virtual Cell Challenge 2026: Benchmarking zero-shot generalization across cellular contexts.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.004
39. scArchon: a scalable benchmarking framework for assessing single-cell perturbation models.. Genome biology 2026. https://doi.org/10.1186/s13059-026-04104-z
40. CellScientist: Dual-Space Hierarchical Orchestration for Closed-Loop Refinement of Virtual Cell Models.  2026. https://arxiv.org/abs/2605.07335v1
41. Causal effect estimation from trans-regulatory single-cell CRISPR screens.. Cell genomics 2026. https://doi.org/10.1016/j.xgen.2026.101251
42. A transcription factor regulatory atlas for activity inference and perturbation prediction. Nucleic Acids Research 2026. https://doi.org/10.1093/nar/gkag897
43. An operational perturbation proteomics-based virtual cell model.. Nature 2026. https://doi.org/10.1038/s41586-026-11001-9
44. Benchmarking virtual cell models for in-the-wild perturbation response.  2026. https://arxiv.org/abs/2604.27646v1
45. A systematic comparison of single-cell perturbation response prediction models.. Science advances 2026. https://doi.org/10.1126/sciadv.aed3414
46. Exploring genetic interaction manifolds constructed from rich single-cell phenotypes. Science 2019. https://doi.org/10.1126/science.aax4438
