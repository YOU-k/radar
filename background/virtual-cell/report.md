# 虚拟细胞与扰动响应预测 · 方向背景报告

证据 45 篇 · 覆盖度 0.56 · 第 5 轮 · 更新 2026-10-04

## 本次变更

- 新增 [10] Deep learning perturbation models can outperform baselines on calibrated metrics.

## 摘要（TL;DR）

- 早期范式以 scGen 的潜空间扰动向量为代表，用变分自编码器实现跨细胞类型与跨物种响应预测 [1]。
- scGPT 在超过 3300 万个单细胞 RNA 测序图谱上预训练生成式 Transformer，适配扰动响应预测等下游任务 [2]。
- State 的细胞嵌入训练于 1.67 亿细胞，在大型数据集上效应区分度提升超过 30%，并引入 Cell-Eval 评估框架 [3]。
- Tahoe-x1 将扰动训练的单细胞基础模型扩展到最高 30 亿参数，实现比先前细胞状态模型高 3–30 倍的计算效率 [4]。
- X-Atlas/Pisces 构建含 2560 万扰动单细胞、16 种生物学情境的最大全基因组 CRISPRi Perturb-seq 数据集，配套 X-Cell 在 Pearson Δ 等指标上优于现有最先进模型最高达五倍 [5]。
- scKITE 仅用 179,067 个样本（不足先前强模型 0.5%）即在多下游任务超越 Geneformer、scGPT 等，知识增强训练带来平均 28.8% 相对提升 [6]。
- 有工作证明利用知识图谱的最简 KNN 模型在未见基因敲除的转录组效应预测上击败几乎所有方法，在 Replogle 2022 细胞系上达到当前 SOTA 水平 [7]。
- Chreode 提出一步式细胞世界模型，在 GEARS 上把 DE20 MSE 从 0.2121 降至 0.1858（相对提升 12.4%），但明确不声称具备规划或推演能力 [8]。
- 一项对比五种基础模型与两种深度学习模型的研究发现，没有任何模型优于简单线性基线，并识别出 5,035 个遗传互作（潜在 124,000）[9]。
- 指标校准研究在 14 个数据集、18 个指标上发现 MSE 和 Pearson Δ 等常用指标常校准不良，在良好校准指标下深度学习扰动模型可优于无信息基线 [10]。
- 用 2220 万细胞预训练 400 个模型、开展 6400 次实验后发现性能在远小于现有语料的数据规模即达平台期，无明确数据缩放定律 [11]。

## 1 背景与定义

虚拟细胞与扰动响应预测的方向边界，首先由“预测什么”与“在什么条件下预测”共同划定。早期范式以潜空间扰动向量为代表，scGen 用变分自编码器在潜空间中加减扰动向量，实现跨细胞类型与跨物种的响应预测 [1]；此后生成式预训练路线兴起，scGPT 在超过 3300 万个单细胞 RNA 测序图谱上预训练生成式 Transformer，通过迁移学习适配扰动响应预测等下游任务 [2]。与之相对，State 强调预测扰动效应时须考虑实验内与跨实验的细胞异质性，其细胞嵌入训练于 1.67 亿细胞，并引入 Cell-Eval 评估框架 [3]。**该方向的核心问题并非“能否生成扰动后的表达谱”，而是“预测是否在未见细胞情境、未见扰动与跨数据集条件下仍然成立”**，这一判断由多项基准工作共同支撑 [12][13]。

演化脉络上，数据规模与模型容量的扩张是一条主线，但知识注入与调控先验构成并行的第二条路线，二者形成张力。Tahoe-x1 将扰动训练的单细胞基础模型扩展到最高 30 亿参数，预训练数据包括 Tahoe-100M 扰动汇编 [4]；X-Atlas/Pisces 构建迄今最大的全基因组 CRISPRi Perturb-seq 数据集，含 2560 万扰动单细胞、16 种生物学情境，配套的 X-Cell 扩散语言模型整合自然语言、蛋白质语言模型与互作网络等多模态先验 [5]；Speciesformer 进一步把生成式虚拟细胞扩展到跨物种设定，在含 1.31 亿细胞的 SpeciesCorpus 上预训练 [14]。与之相对，scKITE 的数据缩放分析显示，纳入细胞级文本注释与基因级调控信息比单纯扩大数据规模提供额外缩放维度，仅用 179,067 个样本（不足先前强模型 0.5%）即在多下游任务超越 Geneformer、scGPT 等 [6]；TFActProfiler 整合 TF–mRNA 先验与大规模 RNA-seq 图谱，无需额外训练即可预测 TF 扰动转录组响应 [15]；D-SPIN 从跨数千扰动条件的单细胞 mRNA-seq 推断机制可解释且可生成的基因调控网络模型 [16]。**“扩大数据”与“注入知识”两条路线尚未在统一评测下分出优劣，但预训练规模的作用已受到质疑**：用 2220 万细胞预训练 400 个模型、开展 6400 次实验后发现，性能在远小于现有语料的数据规模即达平台期，无明确数据缩放定律 [11]。

架构层面，扩散与流匹配成为扰动生成的主流选择，但设计取向存在分歧，且最简方法在分布外预测上仍具竞争力。OCOO-T 主张极简路线，用普通 Transformer 直接作用于连续基因表达谱，将扰动响应预测建模为连续时间去噪过程 [17]；SCALE 针对对照与处理细胞为非配对群体这一设定，用条件传输模型将细胞表示为无序集合、预测处理群体而无需细胞级配对 [18]；D²R² 把预测重构为调控引导的基因级渐进生成，用掩码离散扩散以序数 token 逐步重建表达谱 [19]；scBalFlow 关注药物扰动数据的类别严重不平衡问题，采用两阶段解耦训练 [20]。与此同时，有工作证明利用知识图谱的最简 KNN 模型在未见基因敲除的转录组效应预测上击败几乎所有方法，并用强化学习优化推理 LLM 调整邻域，在 Replogle 2022 细胞系上达到当前 SOTA 水平 [7]。**这一结果提示，知识图谱作为先验与 RL 精炼 LLM 的组合，可能比单纯增加架构复杂度更有效，但其性能依赖知识图谱质量** [7]。

任务边界正从静态“对照—处理”映射向轨迹、药物与跨模态扩展，而细胞世界模型的核心分歧在于是否显式建模状态随时间的演化。PerturbGen 训练于超 1 亿单细胞转录组，预测沿细胞轨迹的扰动响应 [21]；scDEFT 将药物视为细胞表征的条件算子，在 116 万细胞 IBD 图谱上状态变化预测达 headroom 的 45%，治疗前应答分层 AUROC 0.70 [22]；UniPert-G2CP 以两阶段框架统一多模态分子扰动表征，实现遗传到化学的表型迁移学习 [23]；CellFluxRL 面向图像型虚拟细胞生成，用强化学习后训练 CellFlux，设计三类共七个奖励 [24]。Chreode 提出一步式细胞世界模型，通过结构化残差转移算子预测动作条件下的细胞状态转移，把分布演化从推理时移到训练时 [8]；与之相对，Cell 的愿景论文主张虚拟细胞应是多模态、多尺度、有状态的动态计算系统，提出虚拟细胞世界模型（VCWM）框架，强调动作条件仿真、反事实推理与长程规划 [25]。**两者的差异在于：前者给出可验证的预测性能但明确不声称具备规划或推演能力，后者给出架构与评估原则却无实验验证与定量结果** [8][25]。

闭环智能体方向关注预测失败后的定向修正，但目前更多停留在框架倡议与工具链层面。CellScientist 将高层假设空间与低层可执行实现空间耦合，把执行偏差路由回假设或实现层面的定向更新，形成假设—实现—假设闭环，在形态学与转录组基准及单细胞扰动评估中，其案例的 PCC 由 0.3416 提升至 0.4368，并产生可审计的精炼轨迹，但该精炼依赖 LLM 代理，长程工作流仍脆弱 [26]。**这与 Chreode 仅做预测建模、不涉及规划形成对照，也提示世界模型的“闭环”能力尚缺统一的定量验证** [8][26]。

数据资源层面，单细胞扰动图谱正沿规模与覆盖两个维度扩张，并向原代、体内与空间体系推进。Tahoe-100M 以 1 亿转录组、50 个癌细胞系、1100 种药物-剂量条件构建十亿级药物扰动图谱，借助 Mosaic 平台将遗传上不同的细胞模型多重化为平衡的“细胞村”以降低批次效应 [27]；基因组规模 Perturb-seq 用 CRISPRi 靶向全部表达基因、覆盖超过 250 万人类细胞 [28]。向原代与体内体系的推进带来新的资源类型：针对 2200 万原代人 CD4+T 细胞、4 名供体的全表达基因扰动，探针式 perturb-seq 平台同时测量静息与刺激后转录组效应 [29]；iGOF-Perturb-seq 在小鼠星形胶质细胞中构建约 1000 个转录因子的功能获得性图谱 [30]；SPAC-seq 与 TARDIS 将基因扰动与空间表型和通路关联 [31]。ProteinTalks 基于超过 3800 万条时序蛋白丰度测量，学习可迁移的动态潜表示 [32]。**上述资源在体系、扰动类型与读出层上互补，但覆盖范围与转化验证程度差异明显，尚无统一评测口径可直接横向比较** [27][29][30]。

评测效度的争议构成该方向当前最尖锐的核心问题：常用基准是否高估了模型能力，以及“深度模型是否优于简单基线”。多项工作指出，现有评估设置过度简化或不一致，未反映真实生物系统的复杂性，导致常用设置下性能被高估、严格条件下性能显著下降 [12]；Systema 量化了十个数据集中的系统性变异，指出当前方法难以泛化到系统性变异之外 [33]；单细胞基准中细胞级随机划分会把同克隆或同患者、共享标签的“亲属”细胞放进训练集，暴露度决定泄漏通道，可检索性决定分数膨胀，在患者队列中泄漏足以推翻临床结论 [34]。在“是否优于简单基线”上，证据呈现明显冲突：一项对比五种基础模型与两种深度学习模型的研究发现，没有任何模型优于简单线性基线 [9]；在扰动后 RNA-seq 预测中，最简单的 Train Mean 即优于 scGPT 和 scFoundation [35]；VCBench 评估五种基础模型后同样发现，基线在五个评分维度中的四个匹配或超过所有基础模型 [36]。不过，这一结论受到指标校准研究的直接挑战：该研究在 14 个数据集、18 个指标上发现，MSE 和 Pearson Δ 等常用指标常校准不良，降低了对阳性模型性能的敏感性；在良好校准指标下，深度学习扰动模型可优于无信息基线 [10]。**“深度模型不如基线”的判断可能部分源于指标选择而非模型本身，评测效度的关键已从“分数高低”转向划分方式、指标校准与任务可测试性的系统审视** [10][33]。

任务边界与泛化类型的分歧进一步限定了方向的可宣称范围。药物盲评估显示，模型通常能做癌症盲预测，但药物盲性能显著下降甚至完全失败，单药癌症药物盲响应预测主要限于同类内泛化 [37]；跨任务基准评测 13 个模型发现，扰动效应幅度强烈影响泛化与双扰动预测，细胞类型迁移中源-目标转录组距离越大准确率越低 [38]；scArchon 标准化评估九种工具，但明确仅限非遗传扰动，基因敲除作为独立问题未纳入 [39]；ASSAYBENCH 基于 1920 个 CRISPR 筛选、五类表型，发现现有方法远未达经验性能上限，且零样本通用 LLM 优于生物学专用 LLM 和可训练基线 [40]；因果层面，单细胞 CRISPR 筛选的因果效应估计需附加因果假设，且仅能识别一个基因敲低对另一基因的效应，而非基因间直接因果效应 [41]。**这些结果共同表明，虚拟细胞的“预测能力”必须按扰动模态、泛化类型与因果层级分别声明，笼统的“预测扰动响应”已不足以刻画模型边界** [37][41]。

面向未来，评测正转向更严苛的泛化设定，而 AIVC 作为整合性范式仍处早期。Virtual Cell Challenge 2026 要求跨多个独立细胞情境的零样本预测，在含未见细胞系的 Arc 新数据集上预测基因敲低响应 [13]；更早的 Arc Institute 虚拟细胞挑战赛作为反复举办的开放基准竞赛，提供评估框架、专用数据集与模型开发平台，但其摘要未报告具体实验数据或定量结果 [42]。人工智能虚拟细胞（AIVC）被提出作为整合多组学数据、贯通微观分子机制与宏观组织行为的研究新范式，其统一技术框架从跨尺度表征工程、功能子模块设计与多组件动态调控机制三方面展开，并系统梳理了现有模型与数据集资源 [43]。**但该综述本身未提供可供比较的定量结果，且作者强调数据异质性与模型可解释性等挑战尚未解决，AIVC 仍处早期阶段** [43]。综合来看，该方向的边界已从“能否生成扰动后表达谱”收缩为“在何种划分、何种指标、何种泛化类型下预测成立”，而世界模型与闭环智能体的框架倡议尚未与这一评测效度审视充分对接 [25][26]。

## 2 方法学


### 2.1 扰动响应生成模型

单细胞扰动响应预测的早期范式以潜空间扰动向量为代表：**scGen** 用变分自编码器在潜空间中加减扰动向量，实现跨细胞类型与跨物种的响应预测，为后续工作奠定基础 [1]。此后生成式预训练路线兴起，**scGPT** 在超过 **3300 万个**单细胞 RNA 测序图谱上预训练生成式 Transformer，通过迁移学习适配细胞类型注释、多批次与多组学整合、扰动响应预测、基因网络推断等下游任务 [2]。与之相对，**State** 强调预测扰动效应时须考虑实验内与跨实验的细胞异质性，其细胞嵌入训练于 **1.67 亿**细胞，在大型数据集上效应区分度提升超过 **30%**，并引入 Cell-Eval 评估框架 [3]。

数据规模与模型容量的扩张成为一条主线。**Tahoe-x1** 将扰动训练的单细胞基础模型扩展到最高 **30 亿**参数，预训练数据包括 Tahoe-100M 扰动汇编，通过架构与训练策略优化实现比先前细胞状态模型高 **3–30 倍**的计算效率，在基因必需性、癌症标志基因、细胞类型分类和留出环境扰动响应预测四个基准上均达最先进性能 [4]。**X-Atlas/Pisces** 则构建了迄今最大的全基因组 CRISPRi Perturb-seq 数据集，含 **2560 万**扰动单细胞、**16 种**生物学情境，配套的 **X-Cell** 扩散语言模型通过交叉注意力整合自然语言、蛋白质语言模型与互作网络等多模态先验，在 Pearson Δ 等指标上优于现有最先进模型最高达 **五倍**，并展示零样本预测能力 [5]。**Speciesformer** 进一步把生成式虚拟细胞扩展到跨物种设定，在含 **1.31 亿**细胞的 SpeciesCorpus 上预训练，学习可迁移的细胞状态与状态转变，并区分保守生物学原理与物种、组织及细胞环境特异变异 [14]。

在架构层面，扩散与流匹配成为扰动生成的主流选择，但设计取向存在分歧。**OCOO-T** 主张极简路线，用普通 Transformer 直接作用于连续基因表达谱，将扰动响应预测建模为连续时间去噪过程，通过自适应层归一化和上下文 token 整合扰动、剂量与细胞系信息，在 Tahoe100M、Replogle、PBMC 上达到最先进性能并可扩展至长转录谱，但其作者也指出基于扩散/流匹配的方法学习对照到扰动分布仍具挑战 [17]。**SCALE** 针对对照与处理细胞为非配对群体这一设定，用条件传输模型将细胞表示为无序集合、预测处理群体而无需细胞级配对，共享集合感知编码器与条件 DiT 骨干使端点监督直接 delta 对齐，在 CRISPR 数据 **7 项**指标上优于竞争方法，其预测的细胞因子差异经 **3 名**供体 PBMC 实验验证 [18]。**D²R²** 则把预测重构为调控引导的基因级渐进生成，用掩码离散扩散以序数 token 逐步重建表达谱，调控策略模块由对照细胞 GRN 初始化并经组相对策略优化微调排序，在 Norman19 **五项**指标最优、H1 具竞争力，消融显示生物先验排序优于随机与不确定性启发式，但仅在两个数据集验证且排序依赖推断的 GRN 质量 [19]。**scBalFlow** 关注药物扰动数据的类别严重不平衡问题，采用两阶段解耦训练，第一阶段预测响应强度并用高斯增强推断缓解不平衡，第二阶段跳过弱响应条件并用 Flow Matching 合成高响应样本，在 SciPlex3 和 McFarland 等基准上显著优于现有 SOTA，尤其能捕捉复杂分布偏移并保持单细胞分布一致性 [20]。

知识注入与调控先验构成另一条并行路线，且与纯数据缩放路线形成张力。**scKITE** 的数据缩放分析显示，纳入细胞级文本注释与基因级调控信息比单纯扩大数据规模提供额外缩放维度，其通过轻量辅助解码器将细胞注释与基因调控监督融入共享转录组 Transformer 编码器（解码器仅预训练使用），仅用 **179,067** 个样本（不足先前强模型 **0.5%**）即在多下游任务超越 Geneformer、scGPT 等，知识增强训练带来平均 **28.8%** 相对提升 [6]。**TFActProfiler** 整合 ChIP 基、motif 基与人工整理的 TF–mRNA 先验及大规模 RNA-seq 图谱，通过聚类正则化回归学习带符号定量的调控系数，兼顾覆盖度与精度并提供可靠性度量，在多细胞类型 TF 敲低基准上优于现有 TF 活性推断方法，且无需额外训练即可预测 TF 扰动转录组响应 [15]。**D-SPIN** 从跨数千扰动条件的单细胞 mRNA-seq 推断机制可解释且可生成的基因调控网络模型，通过重构调控相互作用解释扰动如何改变细胞状态比例，在 Perturb-seq 和药物响应数据上识别细胞命运关键调控因子、解析药物组合的加性基因程序招募，并模拟未观测剂量组合下的免疫细胞群结构变化 [16]。**RegVelo** 则联合建模剪接动力学与基因调控互作，在多种生物系统中预测终态、基因互作和扰动模拟，结合计算机扰动、CRISPR-Cas9 敲除与单细胞 Perturb-seq 验证，确立 tfec 为早期驱动因子、elf1 为色素细胞命运调控因子 [44]。

值得注意的是，最简方法在分布外扰动预测上仍具竞争力，这与复杂生成模型的扩张形成对照。有工作证明利用知识图谱的最简 KNN 模型在未见基因敲除的转录组效应预测上击败几乎所有方法，并用强化学习优化推理 LLM 调整邻域，在 Replogle 2022 细胞系上达到当前 SOTA 水平，RL 训练还提升 LLM 在差异表达预测上的表现 [7]。这一结果提示，知识图谱作为先验与 RL 精炼 LLM 的组合，可能比单纯增加架构复杂度更有效，但其性能依赖知识图谱质量 [7]。

任务边界也在向轨迹、药物与跨模态扩展。**PerturbGen** 训练于超 **1 亿**单细胞转录组，预测沿细胞轨迹的扰动响应，即源状态遗传扰动如何塑造下游状态、改变基因程序与轨迹，在免疫挑战、造血与皮肤发育三套数据中预测 IL1B 敲除减弱后续细胞因子-干扰素程序，与 IL-1β 刺激逆转一致 [21]。**scDEFT** 将药物视为细胞表征的条件算子，用特征级线性调制生成药物条件化潜变量并冻结，由两个独立头按转录邻域聚合预测状态变化与应答状态，反向阶段排序潜维度并映射到基因，在 **116 万**细胞 IBD 图谱（**3** 队列 **2** 类药物、**51** 供体）上状态变化预测达 headroom 的 **45%**，治疗前应答分层 AUROC **0.70**，而标准预测器仅达随机水平 [22]。**UniPert-G2CP** 则以两阶段框架统一多模态分子扰动表征，实现遗传到化学的表型迁移学习，在大规模遗传与化学筛选数据上实现更高效准确鲁棒的扰动因果空间模拟，并揭示药物响应异质性与耐药机制 [23]。**CellFluxRL** 面向图像型虚拟细胞生成，用强化学习后训练 CellFlux，设计生物功能、结构有效性与形态正确性三类共 **七个**奖励，通过采样-优化交替提升高奖励样本似然，在所有奖励上优于基线且测试时扩展进一步增益，但其奖励为加权线性组合、权重依赖人工设计，且仅验证于 CellFlux 一种生成框架 [24]。

### 2.2 细胞世界模型与闭环智能体

细胞世界模型的核心分歧在于：是直接拟合静态的“对照—处理”映射，还是显式建模状态随时间的演化。Chreode 提出**一步式细胞世界模型**，通过结构化残差转移算子预测动作条件下的细胞状态转移，把分布演化从推理时移到训练时，从而在单次生成中保留 Waddington 式分解；它在 240 万细胞小鼠胚胎图谱、7 个数据集上预训练，在 GEARS 上把 DE20 MSE 从 0.2121 降至 0.1858（相对提升 12.4%），并在 Weinreb 与 Veres 上使 Sinkhorn 距离优于匹配的从头训练模型 [8]。与之相对，Cell 的愿景论文主张虚拟细胞应是多模态、多尺度、有状态的动态计算系统，提出**虚拟细胞世界模型（VCWM）**框架，强调动作条件仿真、反事实推理与长程规划，认为应建模底层细胞系统本身、让干预在演化状态中传播，而非只优化特定任务端点 [25]。两者的差异在于：前者给出可验证的预测性能但明确不声称具备规划或推演能力 [8]，后者给出架构与评估原则却无实验验证与定量结果 [25]。

闭环智能体方向则关注预测失败后的定向修正。CellScientist 针对“精炼路由”问题——预测偏差通过可执行实现被观察到，但相关修正可能落在建模假设、表示设计、实现或任务约束等不同层级——将高层假设空间与低层可执行实现空间耦合，把执行偏差路由回假设或实现层面的定向更新，形成假设—实现—假设闭环 [26]。在形态学与转录组基准及单细胞扰动评估中，其案例的 PCC 由 0.3416 提升至 0.4368，最终可执行模型在固定划分与评估协议下优于参考基线，并产生可审计的精炼轨迹；但该精炼依赖 LLM 代理，长程工作流仍脆弱 [26]。这与 Chreode 仅做预测建模、不涉及规划形成对照，也提示世界模型的“闭环”能力目前更多停留在框架倡议与工具链层面，尚缺统一的定量验证。

## 3 数据与资源

数据资源层面，单细胞扰动图谱正沿规模与覆盖两个维度扩张。Tahoe-100M 以 **1亿转录组、50个癌细胞系、1100种药物-剂量条件** 构建十亿级药物扰动图谱，借助 Mosaic 平台将遗传上不同的细胞模型多重化为平衡的"细胞村"以降低批次效应，并系统量化增殖、细胞毒性、谱系特异性脆弱性与细胞周期变化 [27]。基因扰动方面，基因组规模 Perturb-seq 用 CRISPRi 靶向全部表达基因、覆盖 **超过250万人类细胞**，据此发现核糖体生物发生新调控因子 CCDC86、ZNF236、SPATA5L1 等 [28]。二者均基于癌细胞系，前者明确限于 50 个癌细胞系、未覆盖原代或体内 [27]，后者亦未覆盖体内与激活扰动 [28]。

向原代与体内体系的推进带来新的资源类型。针对 **2200万原代人CD4+T细胞、4名供体** 的全表达基因扰动，探针式 perturb-seq 平台同时测量静息与刺激后转录组效应，发现活跃调控因子及其所控程序随刺激条件剧变，并将扰动特征关联自身免疫病风险 [29]；其局限在于仅 4 名供体，供体间异质性可能限制泛化 [29]。体内方向，iGOF-Perturb-seq 在小鼠星形胶质细胞中构建 **约1000个转录因子** 的功能获得性图谱，鉴定 Ferd3l 为治疗候选，其过表达可缓解小鼠阿尔茨海默病症状，但仅限小鼠模型与星形胶质细胞、向人类转化需验证 [30]。空间维度上，SPAC-seq 与 TARDIS 将基因扰动与空间表型和通路关联，揭示 Icam1 缺失经免疫抑制促转移、Cd44 调控空间表型及转录因子-趋化因子受体轴，其平台通量与适用组织范围的限制未明确说明 [31]。

面向预测建模的资源与评测框架同步出现。ProteinTalks 基于 **超过3800万条时序蛋白丰度测量** 的扰动乳腺癌细胞系数据，学习可迁移的动态潜表示，在药物疗效与协同预测、耐药蛋白发现、患者分层及类器官候选药物排序上普遍优于所选基准，并可迁移至患者类器官与临床活检，但主要基于乳腺癌细胞系、需更多体系验证 [32]。与之配套，Arc Institute 建立的虚拟细胞挑战赛作为反复举办的开放基准竞赛，提供评估框架、专用数据集与模型开发平台，以推动扰动响应预测这一目标；其摘要未报告具体实验数据或定量结果 [42]。上述资源在体系（癌细胞系、原代T细胞、小鼠星形胶质细胞、空间组织）、扰动类型（药物、CRISPRi、功能获得）与读出层（转录组、蛋白质组、空间表型）上互补，但覆盖范围与转化验证程度差异明显，尚无统一评测口径可直接横向比较。

## 4 评测与效度批判

虚拟细胞评测的首要争议在于：常用基准是否高估了模型能力。多项工作指出，现有评估设置过度简化或不一致，未反映真实生物系统的复杂性，导致常用设置下性能被高估、严格条件下性能显著下降 [12]。**Systema** 进一步量化了十个数据集（三种技术、五种细胞系）中的系统性变异，指出当前方法难以泛化到系统性变异之外，而常见指标易受这类偏倚影响从而高估性能 [33]。与之呼应，单细胞基准中细胞级随机划分会把同克隆或同患者、共享标签的“亲属”细胞放进训练集，模型可靠记忆而非学习可迁移规则得分；暴露度决定泄漏通道，可检索性决定分数膨胀，在患者队列中泄漏足以推翻临床结论 [34]。

在“深度学习模型是否优于简单基线”这一核心问题上，证据呈现明显冲突。一项对比五种基础模型与两种深度学习模型的研究发现，**没有任何模型优于简单线性基线**，并识别出 5,035 个遗传互作（潜在 124,000）[9]。在扰动后 RNA-seq 预测中，最简单的 Train Mean 即优于 scGPT 和 scFoundation，带 GO 特征的随机森林大幅领先（RF+GO 的 Pearson Delta 为 0.739/0.586/0.480/0.648，而 scGPT 为 0.641/0.554/0.327/0.596）[35]。VCBench 评估五种基础模型后同样发现，**基线在五个评分维度中的四个匹配或超过所有基础模型**，TranscriptFormer 仅在跨模态 RNA 到蛋白预测上超过最强基线，但时间排序性能崩溃 [36]。Systema 也报告简单 perturbed mean 在 Pearson Δ 上跨所有数据集优于其他方法，双基因扰动中 matching mean 显著更优 [33]。

不过，这一结论受到指标校准研究的直接挑战。该研究在 14 个数据集、18 个指标上发现，**MSE 和 Pearson Δ 等常用指标常校准不良**，降低了对阳性模型性能的敏感性；在良好校准指标下，深度学习扰动模型可优于无信息基线 [10]。这提示“深度模型不如基线”的判断可能部分源于指标选择而非模型本身，与前述基准结论形成方法论层面的争议。

评测的另一个分歧在于任务边界与泛化类型。药物盲评估显示，模型通常能做癌症盲预测，但**药物盲性能显著下降甚至完全失败**，单药癌症药物盲响应预测主要限于同类内泛化 [37]。跨任务基准评测 13 个模型发现，扰动效应幅度强烈影响泛化与双扰动预测，细胞类型迁移中源-目标转录组距离越大准确率越低 [38]。scArchon 标准化评估九种工具，但明确仅限非遗传扰动，基因敲除作为独立问题未纳入 [39]。ASSAYBENCH 基于 1920 个 CRISPR 筛选、五类表型，发现现有方法远未达经验性能上限，且零样本通用 LLM 优于生物学专用 LLM 和可训练基线 [40]。因果层面，单细胞 CRISPR 筛选的因果效应估计需附加因果假设，且仅能识别一个基因敲低对另一基因的效应，而非基因间直接因果效应 [41]。

面向未来，评测正转向更严苛的泛化设定。**Virtual Cell Challenge 2026** 要求跨多个独立细胞情境的零样本预测，在含未见细胞系的 Arc 新数据集上预测基因敲低响应 [13]。与此同时，预训练规模的作用也受到质疑：用 2220 万细胞预训练 400 个模型、开展 6400 次实验后发现，性能在远小于现有语料的数据规模即达平台期，**无明确数据缩放定律** [11]。更早的 Perturb-seq 流形工作则展示了从高维单细胞表型构建细胞状态流形、实现通路无偏排序与遗传互作分类的路径，但其依赖生长表型挖掘强互作，覆盖有限 [45]。综合来看，评测效度的关键已从“分数高低”转向划分方式、指标校准与任务可测试性的系统审视。

## 5 产业动态

（本节暂无入库证据）

## 6 空白与趋势

**趋势一：评测效度正在从“分数高低”转向对划分方式、指标校准与任务可测试性的系统审视，但尚无统一口径。** 细胞级随机划分会泄漏同克隆或同患者共享标签的答案，暴露度决定泄漏通道、可检索性决定分数膨胀，患者队列中泄漏足以推翻临床结论 [34]；Systema 量化十个数据集的系统性变异，指出常见指标易受这类偏倚影响而高估性能 [33]；指标校准研究进一步发现 MSE 与 Pearson Δ 常校准不良，在良好校准指标下深度模型可优于无信息基线 [10]。**这三类证据指向同一空白：目前没有同时控制泄漏、校准与任务可测试性的统一评测协议**，scArchon 虽提供容器化可复现流程，却明确仅限非遗传扰动 [39]。

**趋势二：生成架构从“拟合对照—处理映射”向显式状态演化与调控引导生成分化，但两条路线尚未在同一协议下对撞。** Chreode 用结构化残差转移算子做一步式状态转移、保留 Waddington 式分解 [8]，Cell 的 VCWM 愿景则主张动作条件仿真、反事实推理与长程规划，应建模底层细胞系统本身而非只优化任务端点 [25]；D²R² 把预测重构为调控引导的基因级渐进生成，消融显示生物先验排序优于随机与不确定性启发式 [19]。**空白在于：VCWM 框架给出架构与评估原则却无实验验证与定量结果 [25]，而 Chreode 明确不声称具备规划或推演能力 [8]，二者之间缺少可验证的中间形态。**

**趋势三：知识注入与调控先验被证明可替代部分数据规模，但先验质量本身成为新的瓶颈。** scKITE 仅用 179,067 个样本（不足先前强模型 0.5%）即在多下游任务超越 Geneformer、scGPT 等，知识增强训练带来平均 28.8% 相对提升 [6]；TFActProfiler 无需额外训练即可预测 TF 扰动转录组响应并提供可靠性度量 [15]；D-SPIN 从跨数千扰动条件推断可解释、可生成的基因调控网络模型 [16]。**但 D²R² 的排序依赖推断的 GRN 质量 [19]，知识图谱 KNN 路线的性能亦依赖知识图谱质量 [7]，先验可靠性如何量化并传导到预测置信度，尚无系统研究。**

**趋势四：扰动数据资源沿体系、扰动类型与读出层三维扩张，但覆盖范围与转化验证程度差异明显，缺乏统一口径。** Tahoe-100M 覆盖 1 亿转录组、50 个癌细胞系、1100 种药物-剂量条件 [27]，基因组规模 Perturb-seq 覆盖超过 250 万人类细胞 [28]，二者均基于癌细胞系；原代方向有 2200 万原代人 CD4+T 细胞、4 名供体的探针式 perturb-seq [29]，体内方向有约 1000 个转录因子的小鼠星形胶质细胞功能获得图谱 [30]，空间方向有 SPAC-seq 与 TARDIS [31]，蛋白层有超过 3800 万条时序蛋白丰度测量 [32]。**空白在于：这些资源在体系、扰动模态与读出层上互补，却无统一评测口径可直接横向比较，且多数未覆盖体内与激活扰动。**

**趋势五：闭环智能体开始处理“预测失败如何归因与修正”，但仍停留在工具链层面，缺统一定量验证。** CellScientist 将高层假设空间与低层可执行实现空间耦合，把执行偏差路由回假设或实现层面的定向更新，案例 PCC 由 0.3416 提升至 0.4368，并产生可审计的精炼轨迹，但精炼依赖 LLM 代理、长程工作流仍脆弱 [26]。**这与 Chreode 仅做预测建模、不涉及规划形成对照 [8]，也提示世界模型的“闭环”能力目前更多停留在框架倡议与工具链层面，尚缺统一的定量验证。**

**趋势六：任务边界向轨迹、药物、跨物种与跨模态扩展，但泛化类型的分层证据显示“能预测什么”比“预测多准”更关键。** PerturbGen 预测沿细胞轨迹的扰动响应 [21]，scDEFT 将药物视为细胞表征的条件算子并在 116 万细胞 IBD 图谱上实现治疗前应答分层 AUROC 0.70 [22]，UniPert-G2CP 实现遗传到化学的表型迁移学习 [23]，Speciesformer 在 1.31 亿细胞上学习跨物种可迁移细胞状态 [14]。**但药物盲评估显示单药癌症药物盲响应预测主要限于同类内泛化 [37]，跨任务基准显示扰动效应幅度强烈影响泛化与双扰动预测、源-目标转录组距离越大准确率越低 [38]，ASSAYBENCH 则发现零样本通用 LLM 优于生物学专用 LLM 和可训练基线 [40]。空白在于：尚无工作系统刻画“何种泛化类型在何种数据条件下可被当前模型可靠支撑”的边界图谱。**

**趋势七：预训练规模的作用受到直接质疑，但“规模—知识—架构”三者的权衡尚无定论。** 用 2220 万细胞预训练 400 个模型、开展 6400 次实验后发现性能在远小于现有语料的数据规模即达平台期，无明确数据缩放定律 [11]；scKITE 则显示知识增强提供额外缩放维度 [6]。**空白在于：尚无研究在同一受控条件下同时变动数据规模、知识注入强度与架构容量，以判定三者的边际收益与交互效应。**

## 7 未归类新证据

人工智能虚拟细胞（AIVC）被提出作为整合多组学数据、贯通微观分子机制与宏观组织行为的研究新范式，其统一技术框架从跨尺度表征工程、功能子模块设计与多组件动态调控机制三方面展开，并系统梳理了现有模型与数据集资源，如 **GeneCompass**、**Tahoe-100M** 等 [43]。该综述指出，传统实验与生化分析受限于时空分辨率与处理能力，难以刻画动态跨尺度生物事件，而 AIVC 有望推动生命科学从观测分析转向可预测与创新的范式 [43]。

不过，该证据本身为综述性工作，汇总现有模型与数据集而未自行分析样本，因此未提供可供比较的定量结果 [43]。作者同时强调，**数据异质性与模型可解释性**等挑战尚未解决，AIVC 仍处早期阶段 [43]。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 扰动响应生成模型 | 朝阳 | 方法谱系从 scGen 的潜空间加性迁移（[1]）一路扩到 scGPT 的多组学基础模型（[2]），再到 2026 年 State（[3]）与 X-Cell（[5]）强调跨细胞情境的因果/规模化预测，说明近两年仍在出新框架、未收敛到单一范式。 |
| 2.2 细胞世界模型与闭环智能体 | 萌芽 | 雷达样本中仅 3 篇且全部落在 2026 年：Chreode 提出一步式时序动力学与扰动预测的细胞世界模型（[8]），CellScientist 做双空间分层编排的闭环精化（[26]），加上 Cell 的虚拟细胞世界模型观点文（[25]），概念先行、可复现系统极少。 |
| 3 数据与资源 | 朝阳 | 从 genome-scale Perturb-seq 图谱（[28]）到 Virtual Cell Challenge 把评测做成"图灵测试"（[42]），再到空间分辨 CRISPR 筛选测序（[31]）与体内 TF 功能图谱（[30]），数据规模与模态仍在快速扩张。 |
| 4 评测与效度批判 | 朝阳 | 早期遗传互作流形（[45]）提供评测思路，2025 年"深度学习扰动预测尚未跑赢简单基线"（[9]）与基础细胞模型基准（[35]）直接质疑现有方法，2026 年 Systema 把评测推进到超越表达谱的层面（[33]），批判性工作密集且尚未形成统一协议。 |
| 5 产业动态 | 证据不足 | 雷达样本中该节 **n=0**，无可核验技术细节的发布可引；不能据此推断产业冷热。 |

**整体判断**：这个方向整体处于**朝阳期偏早**——生成模型与数据资源两侧都在近两年爆发（雷达样本中 2.1 节 n=19、3 节 n=7，recent_share 分别 **0.89 / 0.86**），但方法未收敛，且评测侧已出现"**没跑赢简单基线**"的硬证据（[9]、[35]），说明**性能红利尚未兑现**。世界模型/闭环智能体（2.2 节 n=3，全为 2026 年）更像概念占位，**窗口期估计 12–24 个月**：一旦 Virtual Cell Challenge 类基准（[42]）收敛出公认评测协议，纯"再训一个更大基础模型"的边际价值会迅速下降。**最大不确定性**是效度——现有评测多基于表达谱相似度，而 Systema 指出需超越表达层面（[33]）；若扰动响应预测在严格基准下持续不敌简单基线，整个子领域的资金与注意力可能转向数据与实验侧。

**接下来怎么做**：
1. **把"评测批判"做成你的第一张牌**：用 Systema 的超越表达谱评测思路（[33]）叠加"未跑赢基线"的结论（[9]），在公共 Perturb-seq 图谱（[28]）上系统复现 State/X-Cell 类方法（[3]、[5]）。现在做是因为基准尚未统一，**谁先给出可信的失效边界谁就定义问题**；产出可为一篇 benchmark + 开源评测套件。
2. **切入"跨情境泛化"而非再刷同分布精度**：State 与 X-Cell 都把卖点放在 diverse cellular contexts（[3]、[5]），但你的衰老 + 多模态背景正好能提供**分布外情境**（衰老细胞、类器官）。用公共数据做 demo、用合作类器官做验证，产出"扰动响应在衰老背景下的泛化衰减曲线"。
3. **把世界模型当假设检验工具，而不是当卖点**：Chreode 的一步式时序动力学（[8]）与 CellScientist 的闭环精化（[26]）都还缺独立验证，你可以用闭环智能体做**主动实验选择**（选哪些扰动最能把模型打崩），产出"主动学习 vs 随机采样"的增益证据。现在做是因为闭环工作刚出现、无人做严格对照。
4. **绑定数据资源侧的新模态**：空间分辨 CRISPR 筛选（[31]）与体内 TF 功能图谱（[30]）提供了表达谱之外的表型读出，正好补上评测效度的短板。用这些数据训练/评测你的多模态模型，产出"空间表型能否提升扰动响应预测效度"的实证。
5. **以 Virtual Cell Challenge 为锚定赛道**：把方法提交到该基准（[42]）并公开失败分析，比自建小基准更有说服力；同时用 scGen→scGPT 的方法演进线（[1]、[2]）说明你站在哪一代之上。现在做是因为基准刚立、**排行榜尚未固化**，早期提交的可见度最高。

## 参考文献

1. scGen predicts single-cell perturbation responses. Nature Methods 2019. https://doi.org/10.1038/s41592-019-0494-8
2. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. Nature Methods 2024. https://doi.org/10.1038/s41592-024-02201-0
3. Predicting cellular responses to perturbation across diverse contexts with State. Cell 2026. https://doi.org/10.1016/j.cell.2026.07.052
4. Tahoe-x1: Scaling Perturbation-Trained Single-Cell Foundation Models to 3 Billion Parameters. bioRxiv 2025. https://doi.org/10.1101/2025.10.23.683759
5. X-Cell: Scaling Causal Perturbation Prediction Across Diverse Cellular Contexts via Diffusion Language Models.  2026. https://doi.org/10.64898/2026.03.18.712807
6. Towards a knowledge-enhanced single-cell foundation model.  2026. https://arxiv.org/abs/2609.14970
7. Knowledge Graphs and Reasoning LLMs for Finding Simple Yet Effective Transcriptomic Perturbation Predictors.  2026. https://arxiv.org/abs/2606.08816v1
8. Chreode: A Cell World Model for One-Step Temporal Dynamics and Perturbation Prediction.  2026. https://arxiv.org/abs/2605.28111v1
9. Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines. Nature methods 2025. https://doi.org/10.1038/s41592-025-02772-6
10. Deep learning perturbation models can outperform baselines on calibrated metrics.. Nature biotechnology . https://doi.org/10.1038/s41587-026-03307-w
11. Evaluating the role of pretraining dataset size and diversity on single-cell foundation model performance.. Nature methods 2026. https://doi.org/10.1038/s41592-026-03120-y
12. Benchmarking virtual cell models for in-the-wild perturbation response.  2026. https://arxiv.org/abs/2604.27646v1
13. Virtual Cell Challenge 2026: Benchmarking zero-shot generalization across cellular contexts.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.004
14. Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling.  . https://doi.org/10.64898/2026.09.22.752128
15. A transcription factor regulatory atlas for activity inference and perturbation prediction. Nucleic Acids Research 2026. https://doi.org/10.1093/nar/gkag897
16. D-SPIN constructs regulatory network models from scRNA-seq that reveal organizing principles of perturbation response.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.028
17. OCOO-T : A Simple and Scalable Virtual Cell Model for Transcriptional Perturbation Response Prediction.  2026. https://arxiv.org/abs/2606.12838v2
18. SCALE:Scalable Conditional Atlas-Level Endpoint transport for virtual cell perturbation prediction.  2026. https://arxiv.org/abs/2603.17380v3
19. $D^{2}R^{2}$: Discrete Diffusion with Regulation Reinforcement for Single-Cell Perturbation Prediction.  2026. https://arxiv.org/abs/2608.15288v1
20. scBalFlow: A Staged Flow Matching Framework for Imbalanced Single-Cell Drug Perturbation Prediction.. Bioinformatics (Oxford, England) 2026. https://doi.org/10.1093/bioinformatics/btag682
21. Predicting how perturbations reshape cellular trajectories with PerturbGen.  2026. https://doi.org/10.64898/2026.03.04.709254
22. scDEFT: A deep learning framework for drug-effect prediction and counterfactual reasoning.  2026. https://arxiv.org/abs/2609.10831
23. UniPert-G2CP bridges genetic and chemical screens from molecular representation to phenotype modeling.. Cell 2026. https://doi.org/10.1016/j.cell.2026.06.005
24. CellFluxRL: Biologically-Constrained Virtual Cell Modeling via Reinforcement Learning.  2026. https://arxiv.org/abs/2603.21743v4
25. A world model of the virtual cell.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.042
26. CellScientist: Dual-Space Hierarchical Orchestration for Closed-Loop Refinement of Virtual Cell Models.  2026. https://arxiv.org/abs/2605.07335v1
27. Tahoe-100M: Mapping drug-induced molecular phenotypes at single-cell resolution.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.035
28. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. bioRxiv 2021. https://doi.org/10.1016/j.cell.2022.05.013
29. Genome-scale perturb-seq in primary human CD4&lt;sup&gt;+&lt;/sup&gt; T cells maps context-specific regulators of T cell programs and human immune traits.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.002
30. Mapping transcription factor functions in astrocytes using in vivo gain-of-function Perturb-seq.. Science (New York, N.Y.) 2026. https://doi.org/10.1126/science.adw2156
31. Uncovering spatially resolved functional genomics with CRISPR screen sequencing.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.049
32. An operational perturbation proteomics-based virtual cell model.. Nature 2026. https://doi.org/10.1038/s41586-026-11001-9
33. Systema: a framework for evaluating genetic perturbation response prediction beyond systematic variation. Nature biotechnology 2026. https://doi.org/10.1038/s41587-025-02777-8
34. Cell-level random splits leak group-owned answers in single-cell benchmarks. bioRxiv 2026. https://doi.org/10.64898/2026.09.09.750484
35. Benchmarking foundation cell models for post-perturbation RNA-seq prediction. BMC genomics 2025. https://doi.org/10.1186/s12864-025-11600-2
36. VCBench: A Multi-Dimensional Benchmark for Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.06.18.733146
37. Monotherapy cancer drug-blind response prediction is limited to intraclass generalization.. PLoS computational biology 2026. https://doi.org/10.1371/journal.pcbi.1013232
38. A systematic comparison of single-cell perturbation response prediction models.. Science advances 2026. https://doi.org/10.1126/sciadv.aed3414
39. scArchon: a scalable benchmarking framework for assessing single-cell perturbation models.. Genome biology 2026. https://doi.org/10.1186/s13059-026-04104-z
40. AssayBench: An Assay-Level Virtual Cell Benchmark for LLMs and Agents.  2026. https://arxiv.org/abs/2605.10876v1
41. Causal effect estimation from trans-regulatory single-cell CRISPR screens.. Cell genomics 2026. https://doi.org/10.1016/j.xgen.2026.101251
42. Virtual Cell Challenge: Toward a Turing test for the virtual cell. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.008
43. Artificial intelligence-enabled multi-scale virtual cell: perspective, challenges, and opportunities.. Briefings in bioinformatics 2026. https://doi.org/10.1093/bib/bbag104
44. RegVelo: Gene-regulatory-informed dynamics of single cells.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.022
45. Exploring genetic interaction manifolds constructed from rich single-cell phenotypes. Science 2019. https://doi.org/10.1126/science.aax4438
