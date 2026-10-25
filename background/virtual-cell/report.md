# 虚拟细胞与扰动响应预测 · 方向背景报告

证据 49 篇 · 覆盖度 0.56 · 第 8 轮 · 更新 2026-10-25

## 本次变更

- 新增 [21] Genetic Perturbation Prediction Models Fail Out-of-Distribution: A Rigorous Benchmark and Systematic Evaluation
- 新增 [45] Deep dynamical models of single-cell multiomic velocities predict loss-of-function and rescue perturbations in B cells.
- 新增 [44] CauTrigger: deciphering biological system state transitions by hierarchical causal decomposition.

## 摘要（TL;DR）

- 扰动响应生成模型沿三条线索展开：潜空间扰动向量（scGen）、生成式预训练基础模型（scGPT，超3300万单细胞RNA测序图谱）与流匹配/扩散/条件传输重构生成过程 [1][2]。
- 扩散与流匹配成为生成范式更新焦点：OCOO-T 用极简流匹配 Transformer 在 Tahoe100M、Replogle、PBMC 上达最先进性能，X-Cell 构建 X-Atlas/Pisces（2560万扰动单细胞、16种情境）并在 Pearson Δ 上优于现有最先进模型最高达五倍 [3][4]。
- 针对对照与处理细胞为非配对群体，SCALE 提出条件传输模型，在 CRISPR 数据7项指标上优于竞争方法并经三名供体 PBMC 实验验证；D²R² 则以掩码离散扩散做基因级渐进生成，在 Norman19 五项指标最优但仅在两个数据集验证 [5][6]。
- 类别不平衡瓶颈被显式建模：scBalFlow 两阶段解耦训练在 SciPlex3 和 McFarland 等基准显著优于现有 SOTA，scDEFT 在116万细胞 IBD 图谱上状态变化预测达 headroom 的 45%、治疗前应答分层 AUROC 0.70 [7][8]。
- 知识注入与规模叙事形成张力：知识图谱 KNN 在分布外扰动预测上击败几乎所有方法，scKITE 仅用179,067个预训练样本（不足先前强模型0.5%）即超越 Geneformer、scGPT 等并带来平均28.8%相对提升 [9][10]。
- 调控网络与因果结构被显式纳入生成框架：D-SPIN、RegVelo、CauTrigger、DynaVelo 把可解释调控机制作为生成目标而非事后解释，但多数未明确外推验证范围 [11]。
- 跨情境与跨物种泛化被单独提出：State 细胞嵌入训练于1.67亿细胞、效应区分度提升超过30%，Tahoe-x1 扩展至最高30亿参数、计算效率高3–30倍，Speciesformer 在1.31亿细胞 SpeciesCorpus 上预训练 [12][13][14]。
- 图像型虚拟细胞构成并行子问题：CellFluxRL 设计三类共七个奖励做强化学习后训练，PerturbBridge 在 BBBC021 上 MoA 准确率77.8%（CellProfiler）/74.9%（DINOv2），但奖励/监督信号均依赖人工设定且验证范围有限 [15][16]。
- 评测效度批判集中爆发：13个方法在25个数据集、24个指标上系统评测显示常用基准与指标系统性高估真实能力，五种基础模型和两种深度学习模型在单/双基因扰动预测上没有任何模型优于简单线性基线 [17][18]。
- 上述结论存在明确争议：一项在14个数据集、18个指标上的研究发现 MSE 和 Pearson Δ 等常用指标常校准不良，在良好校准指标下深度学习扰动模型可优于无信息基线，争议实质在于什么算有效基线与指标是否对真实信号敏感尚未形成共识 [19]。
- 数据划分方式是效度批判另一主战场：细胞级随机划分导致泄漏、leakcheck 工具在患者队列中显示泄漏足以推翻临床结论，EL-PERTURB 在分层分布外划分下结论为扰动预测模型在真实 OOD 条件下泛化失败 [20][21]。
- 预训练规模效度被重新审视：用2220万细胞预训练400个模型并开展6400次实验的研究发现性能在数据规模远小于现有语料时即达平台期、无明确数据缩放定律，与越大越好的叙事构成直接张力 [22]。
- 从预测走向可干预、可推演存在层次差异：Chreode 作为一步式细胞世界模型在240万细胞小鼠胚胎图谱、7个数据集上预训练，GEARS 上 DE20 MSE 从0.2121降至0.1858（相对提升12.4%），但明确只做预测建模、不声称具备规划能力 [23]。
- 与之相对，Cell 的愿景论文主张虚拟细胞应为多模态、多尺度、有状态的动态计算系统以支持反事实推理与长程规划，但未报告定量结果、属愿景性论述；CellScientist 则构建假设—实现—假设闭环，案例中 PCC 由0.3416提升至0.4368，局限在于精炼依赖 LLM 代理、长程工作流仍脆弱 [24][25]。
- 单细胞扰动图谱规模扩张但覆盖各有取舍：Tahoe-100M 汇集1亿转录组、50个癌细胞系与1100种药物-剂量条件，基因组规模 Perturb-seq 覆盖超过250万人类细胞，原代细胞工作在4名供体的2200万原代人CD4+T细胞上做全表达基因扰动，共同指向体外细胞系体系难以反映组织与体内状态的缺口 [26][27][28]。
- 基准覆盖范围本身被质疑：scArchon 明确仅限非遗传扰动、基因敲除未纳入，AssayBench 基于1920个CRISPR筛选、五类细胞表型发现现有方法远未达经验性能上限，VCBench 显示基线在五个评分维度中的四个匹配或超过所有基础模型且没有基础模型发布完整细胞级训练清单 [29][30][31]。
- 因果层面效度问题从预测准不准延伸到解释是否成立：综述指出这类设计仅能识别一个基因敲低对另一基因的因果效应、无法直接推断两基因间因果效应，早期 Perturb-seq 流形工作则依赖生长表型挖掘强遗传互作、覆盖有限 [32][33]。
- 未来评测方向：Virtual Cell Challenge 2026 把目标设为跨多个独立细胞情境的零样本预测、要求在新 Arc 数据集上预测未见细胞系中的基因敲低响应，能否解决简单基线常胜与指标校准争议仍取决于划分策略与指标选择是否公开可审计 [34]。
- 综述层面，AIVC 统一技术框架主张从跨尺度表征工程、功能子模块设计与多组件动态调控机制三方面分解建模问题，但属综述性质未提供可比较的定量性能结果，且指出数据异质性与模型可解释性等挑战尚未解决、AIVC 仍处早期阶段 [35]。

## 1 背景与定义

虚拟细胞与扰动响应预测的边界，可以从「预测什么」与「以什么为单位」两个维度界定。狭义上，它指给定对照细胞群体与扰动标签（基因敲低/过表达、药物与剂量、环境刺激），预测扰动后细胞的转录组或形态表型分布；广义上，它被主张为多模态、多尺度、有状态的动态计算系统，支持动作条件仿真、反事实推理与长程规划[24]。这一广义定义把「扰动响应模型」与「细胞世界模型」区分开来：前者优化特定任务端点，后者要求建模底层细胞系统本身、使干预在演化状态中传播[24]。**当前有代码可复现的工作绝大多数落在狭义一侧**，Chreode 虽自称细胞世界模型，但明确只做预测建模、不声称具备规划能力[23]；闭环智能体一侧仅有 CellScientist 这类模型精炼框架[25]。因此本方向的现实边界是：**生成式扰动响应预测已有较厚的方法与数据积累，而「可推演、可规划」的世界模型仍主要是架构主张**。

演化脉络上，方法重心经历了三次迁移。第一次是以 scGen 确立的潜空间扰动向量范式，用向量加减实现跨细胞类型与跨物种响应预测[1]；第二次是以 scGPT 为代表的大规模预训练加微调范式，在**超过3300万个单细胞RNA测序图谱**上预训练生成式 Transformer[2]；第三次是生成过程本身被重构，流匹配、扩散、条件传输与离散扩散被用于直接建模对照到扰动的分布转移[3][4][5][6]。与这条主线并行的是知识注入路线：知识图谱 KNN 经强化学习优化邻域后在 Replogle 2022 上达到 SOTA[9]，scKITE 仅用 **179,067个预训练样本（不足先前强模型0.5%）** 即超越 Geneformer、scGPT 等[10]。**这两条路线构成当前最实质的方法论张力：规模扩张与先验质量孰为主因，尚无受控对比**。

核心问题可归为四类。其一是**监督信号的位置**：从潜空间向量[1]、连续时间去噪轨迹[3]，到训练阶段直接施加扰动特异性表型监督[16]，监督越靠近表型层，越依赖对「何为生物学有意义」的人工设定。其二是**数据特性的显式建模**：对照与处理细胞为非配对群体，SCALE 以集合级条件传输绕开细胞级配对[5]；药物扰动类别严重不平衡，scBalFlow 用两阶段解耦训练与高斯增强推断缓解[7]。其三是**外推与因果识别**：跨细胞情境、跨物种、跨数据集的零样本泛化被单独提出为评测目标[34][14]，而因果综述指出这类设计**仅能识别一个基因敲低对另一基因的效应，无法直接推断两基因间因果效应**[32]。其四是**效度**：多项独立评测得出同向结论——常用基准与指标系统性高估真实能力，五种基础模型和两种深度学习模型在单/双基因扰动预测上**没有任何模型优于简单线性基线**[18]，Train Mean 在 Perturb-seq 上优于 scGPT 与 scFoundation[36]，细胞级随机划分会泄漏组内答案[20]。**「预测分数高」与「预测能力真」之间的裂缝，是本方向当前最需要正面处理的定义性问题**。

数据资源的形态决定了上述问题的可检验程度。药物侧以 **Tahoe-100M** 为代表，含 **1亿转录组、50个癌细胞系、1100种药物-剂量条件**，用 Mosaic 平台多重化为平衡细胞村以压低批次效应[26]；基因侧有覆盖 **超过250万人类细胞**的基因组规模 Perturb-seq[27]，以及 **4名供体、2200万原代人CD4+T细胞**的探针式扰动图谱[28]；X-Atlas/Pisces 则以 **2560万扰动单细胞、16种情境**扩展了情境维度[4]。读出维度也在扩展：ProteinTalks 基于 **超过3800万条时序蛋白丰度测量**构建模型并迁移至患者类器官与临床活检[37]，SPAC-seq 把 CRISPR 筛选推到空间分辨层面[38]，iGOF-Perturb-seq 在星形胶质细胞中构建 **约1000个转录因子**的功能获得性图谱[39]。**但训练资源与评测目标存在结构性错位：模型多以癌细胞系为主要训练来源，而原代细胞与在体数据规模相对有限，体外体系难以反映组织与体内状态**。

评测与批判已形成相对独立的一条线索，其价值在于把「虚拟细胞」从宣示性概念拉回可证伪命题。系统评测在 25 个数据集、24 个指标上比较 13 个方法，发现扰动效应幅度强烈影响泛化、源-目标转录组距离越大准确率越低[17]；Systema 把失败归因于「系统性变异」，指出简单 perturbed mean 在 Pearson Δ 上跨所有数据集优于其他方法[40]；EL-PERTURB 用分层分布外划分压力测试 20 个模型，结论是随机划分掩盖了系统性失效模式[21]；药物盲设置下性能显著恶化甚至完全失败，泛化主要限于同类内[41]。争议同样明确：有研究在 14 个数据集、18 个指标上发现 MSE 与 Pearson Δ 等常用指标校准不良，在良好校准指标下深度模型可优于无信息基线[19]。**分歧的实质不是「模型行不行」，而是「什么算有效基线、什么指标对真实信号敏感」尚未形成共识**；在此共识建立之前，跨研究的性能数字不宜相互比较。

据此，本方向尚未被占据的位置有三处。第一，**统一受控对比的缺位**：知识注入路线与规模扩张路线、群体级传输与基因级渐进生成、转录组模型与图像模型，均未在同一划分策略与同一校准指标下系统对比[9][10][5][6]。第二，**世界模型主张的可验证化**：愿景论文给出动作条件仿真与反事实推理的架构原则但未报告定量结果[24]，Chreode 给出定量预测增益但回避规划能力[23]，二者之间缺少「既能推演又能被基准检验」的中间形态。第三，**因果识别条件进入评测协议**：现有基准多评预测精度，少有把划分泄漏、系统性变异与因果假设一并写入协议并公开可审计者[20][32]；Virtual Cell Challenge 2026 已把跨情境零样本设为目标[34]，但其划分与指标是否足以回应上述批评，仍待公开检验。

## 2 方法学


### 2.1 扰动响应生成模型

扰动响应生成模型的方法谱系大致沿三条线索展开：以 scGen 为代表的潜空间扰动向量方法、以 scGPT 为代表的生成式预训练基础模型，以及近年围绕流匹配、扩散与条件传输重构生成过程的一批工作。scGen 用变分自编码器在潜空间中学习扰动向量，通过向量的加减实现跨细胞类型与跨物种的响应预测[1]；scGPT 则在**超过3300万个单细胞RNA测序图谱**上预训练生成式 Transformer，经迁移学习适配细胞类型注释、多批次/多组学整合与扰动响应预测等下游任务[2]。两者分别确立了「潜空间算术」与「大规模预训练+微调」两种范式，但前者全文未提供、后者以观察性图谱为主，对干预数据的利用有限。

生成范式的更新集中在扩散与流匹配。OCOO-T 用极简流匹配 Transformer 直接作用于连续基因表达谱，把扰动响应预测建模为连续时间去噪过程，通过自适应层归一化和上下文 token 整合扰动、剂量与细胞系信息，在 Tahoe100M、Replogle、PBMC 上达到最先进性能并可扩展至长转录谱[3]。X-Cell 则构建了 **X-Atlas/Pisces：2560万扰动单细胞、16种情境**的全基因组 CRISPRi Perturb-seq 数据集，用扩散语言模型经交叉注意力整合自然语言、蛋白质语言模型与互作网络等多模态先验，在 Pearson Δ 等指标上优于现有最先进模型最高达五倍并展示零样本预测能力[4]。二者都指出同一争议点：依赖观察性表达图谱的方法难以外推，而扩散/流匹配方法学习对照到扰动分布本身仍具挑战[3][4]。

针对「对照与处理细胞为非配对群体」这一数据特性，SCALE 提出条件传输模型，将细胞表示为无序集合并直接预测处理群体而无需细胞级配对，共享集合感知编码器与条件 DiT 骨干使端点监督直接 delta 对齐；在 CRISPR 数据 **7项指标**上优于竞争方法，其预测的细胞因子差异经三名供体 PBMC 实验验证[5]。与之不同，D²R² 把预测重构为调控引导的基因级渐进生成，用掩码离散扩散以序数 token 逐步重建表达谱，并由对照细胞 GRN 初始化、经组相对策略优化微调排序，在 Norman19 五项指标最优、H1 具竞争力，消融显示生物先验排序优于随机与不确定性启发式[6]。两者分别从群体层面与基因层面处理生成顺序问题，但 D²R² 仅在两个数据集验证且排序依赖推断的 GRN 质量[6]。

类别不平衡是药物扰动预测的另一瓶颈。scBalFlow 采用两阶段解耦训练：第一阶段预测扰动响应强度并用高斯增强推断缓解不平衡，第二阶段跳过弱响应条件、用 Flow Matching 合成高响应样本，在 SciPlex3 和 McFarland 等基准上显著优于现有 SOTA，尤其能捕捉复杂分布偏移并保持单细胞分布一致性[7]。scDEFT 则把药物视为细胞表征的条件算子，用特征级线性调制生成药物条件化潜变量，冻结后由两个独立头按转录邻域聚合预测状态变化与应答状态；在 **116万细胞**的 IBD 图谱上，状态变化预测达 headroom 的 45%，治疗前应答分层 AUROC 0.70，而标准预测器仅达随机水平[8]。两项工作都强调不平衡/弱响应样本带来的偏置，但验证范围分别限于药物筛选基准与 IBD 两药类[7][8]。

知识注入成为提升外推能力的另一条路径。知识图谱 KNN 这一最简模型在分布外扰动预测上击败几乎所有方法，经强化学习优化的推理 LLM 调整邻域后在 Replogle 2022 细胞系上达到 SOTA[9]。TFActProfiler 整合 ChIP、motif 与 curated 先验及大规模 RNA-seq 图谱，学习带符号定量的 TF–mRNA 调控系数，在多细胞类型 TF 敲低基准上优于现有 TF 活性推断方法，且无需额外训练即可预测 TF 扰动转录组响应[42]。scKITE 的数据缩放分析显示，细胞文本注释与基因调控信息提供了比单纯扩大数据量更有效的缩放维度，仅用 **179,067个预训练样本（不足先前强模型0.5%）** 即在多下游任务超越 Geneformer、scGPT 等，知识增强训练带来平均 **28.8%** 相对提升[10]。这些结果与大规模预训练路线形成张力：数据规模并非唯一决定因素，先验质量与注入方式同样关键。

调控网络与因果结构被显式纳入生成框架。D-SPIN 从跨数千扰动条件的单细胞 mRNA-seq 推断维度可扩展、机制可解释且可生成的基因调控网络模型，识别细胞命运关键调控因子、解析药物组合的加性基因程序招募，并模拟未观测剂量组合下的免疫细胞群结构变化[11]。RegVelo 联合建模剪接动力学与基因调控互作，在斑马鱼神经嵴发育数据上结合计算机扰动、CRISPR-Cas9 敲除与 Perturb-seq 验证，确立 tfec 为早期驱动因子、elf1 为色素细胞命运调控因子[43]。CauTrigger 将 do-calculus 整合进分层深度潜变量模型，分离因果与虚假潜因子并递归重建调控层级，在合成和真实多层调控数据集上优于现有方法[44]。DynaVelo 则以生成式神经常微分方程学习基因表达与 TF motif 活性的联合动态，对向量场做计算机扰动，重现野生型小鼠生发中心 B 细胞的体内分叉动态并揭示 Arid1a 和 Ctcf 杂合缺失下的变化[45]。这一组工作共同把「可解释的调控机制」作为生成模型的目标而非事后解释，但多数未明确外推验证范围[11]。

跨情境与跨物种的泛化被单独提出。State 在预测扰动效应时考虑实验内与跨实验的细胞异质性，细胞嵌入训练于 **1.67亿细胞**，在大型数据集上效应区分度提升超过30%，差异表达基因识别准确率显著优于基线，且细胞嵌入可识别训练中未观察扰动的细胞环境[12]。Tahoe-x1 将扰动训练的单细胞基础模型扩展到最高 **30亿参数**，预训练于包括 Tahoe-100M 的大规模转录组，计算效率比先前细胞状态模型实现高3–30倍，在基因必需性、癌症标志基因、细胞类型分类和留出环境扰动响应预测四个基准上均达最先进性能[13]。Speciesformer 在包含 **1.31亿细胞**的 SpeciesCorpus 上预训练，将进化表征学习与虚拟细胞状态生成结合，旨在区分保守生物学原理与物种、组织及细胞环境特异变异[14]。PerturbGen 训练于超1亿单细胞转录组，把预测对象从静态响应扩展到沿细胞轨迹的响应，在免疫挑战、造血与皮肤发育三套数据中预测 IL1B 敲除减弱后续细胞因子-干扰素程序，与 IL-1β 刺激逆转一致[46]。UniPert-G2CP 则用两阶段框架统一多模态分子扰动表征，实现遗传到化学筛选的表型迁移学习，在大规模遗传与化学筛选数据上验证并揭示耐药机制[47]。

图像型虚拟细胞构成并行的生成子问题，其评价逻辑与转录组模型不同。CellFluxRL 针对图像生成违反物理与生物约束的问题，设计生物功能、结构有效性与形态正确性三类共七个奖励，用强化学习后训练 CellFlux，在所有奖励上持续优于基线，测试时扩展进一步提升性能[15]。PerturbBridge 则指出仅匹配真实图像分布不足以优化扰动特异性生物响应，提出随机数据到数据桥模型，在训练中对预测图像直接施加扰动特异性表型监督；在 BBBC021 上 MoA 准确率 **77.8%（CellProfiler）/74.9%（DINOv2）**，较 CellFlux 提升5.7/7.5个百分点，JUMP Hit@10 12.15%、中位秩74，AllenCell Hit@1 69.29%[16]。两项工作都把「生物学有意义的生成」作为目标，但奖励/监督信号的设计均依赖人工设定，且分别只验证于单一生成框架或三个显微基准[15][16]。

综观上述证据，扰动响应生成模型的差异主要体现在三处：其一是监督信号的位置，从潜空间向量[1]、去噪轨迹[3]到训练阶段的直接表型监督[16]；其二是对数据特性的假设，非配对群体[5]与类别不平衡[7]被显式建模，而多数基础模型仍以观察性图谱为主[2]；其三是先验与规模的角色之争，知识图谱 KNN 与知识增强预训练显示小数据可胜过大模型[9][10]，而 Tahoe-x1 与 X-Cell 则分别以30亿参数和2560万扰动细胞推进规模边界[13][4]。这些路线尚未在同一基准上系统对比，跨研究数字不可直接比较，外推能力与机制可解释性能否兼得仍是开放问题。

### 2.2 细胞世界模型与闭环智能体

在虚拟细胞如何从“预测”走向“可干预、可推演”的问题上，三篇证据给出了不同层次的方案。Chreode 定位为**一步式细胞世界模型**，用结构化残差转移算子预测动作条件下的细胞状态转移，把分布演化从推理时移到训练时以实现单次生成，并在 **240万细胞小鼠胚胎图谱、7个数据集**上预训练；在 GEARS 上其 DE20 MSE 从 **0.2121 降至 0.1858**（相对提升 12.4%），在 Weinreb 与 Veres 上 Sinkhorn 距离优于匹配的从头训练模型 [23]。但该工作明确只做预测建模，不声称具备规划或推演能力 [23]。与之相对，Cell 的愿景论文主张虚拟细胞应是多模态、多尺度、有状态的动态计算系统，以世界模型为操作框架支持动作条件仿真、反事实推理与长程规划，核心论点是应建模底层细胞系统本身、让干预在演化状态中传播，而非只优化特定任务端点 [24]。二者构成明显张力：一方给出可验证的定量预测增益但回避规划能力，另一方给出规划与反事实的架构主张却**未报告定量结果**、属愿景性论述 [23][24]。

在闭环层面，CellScientist 处理的是预测失败后的归因与修订问题：预测偏差通过可执行实现被观察到，但相关修订可能落在建模假设、表示设计、实现或任务约束等不同层级，缺乏结构化反馈传播时容易出现“修了代码却没改假设”。该框架将高层假设空间与低层可执行实现空间耦合，把执行偏差路由回假设或实现层面，形成假设—实现—假设闭环；案例中 **PCC 由 0.3416 提升至 0.4368**，最终可执行模型在固定划分与评估协议下优于参考基线，并产生可审计的精炼轨迹 [25]。其局限在于精炼依赖 LLM 代理、长程工作流仍脆弱 [25]。三篇工作分别覆盖单步动态预测、世界模型架构愿景与模型迭代精炼三个子问题，尚未在同一基准上直接比较，因此其性能数字不宜跨研究比对高低。

## 3 数据与资源

单细胞扰动图谱的规模在近年迅速扩张，但不同工作在覆盖范围与扰动类型上各有取舍。**Tahoe-100M** 汇集了 **1亿转录组**、**50个癌细胞系**与 **1100种药物-剂量条件**，借助 Mosaic 平台把遗传背景不同的细胞模型多重化为平衡的"细胞村"，以降低批次效应，并系统量化增殖、细胞毒性、谱系特异性脆弱性与细胞周期变化 [26]。与之互补的是基因层面的扰动：基因组规模 Perturb-seq 用 CRISPRi 靶向全部表达基因、覆盖 **超过250万人类细胞**，据此发现核糖体生物发生、转录与线粒体呼吸的新调控因子 [27]；针对原代细胞的工作则在 **4名供体**的 **2200万原代人CD4+T细胞**上做全表达基因扰动，采用探针式 perturb-seq 平台测量静息与刺激后的转录组效应，发现活跃调控因子及其所控程序随刺激条件剧变 [28]。上述三项研究分别以药物、细胞系基因敲低和原代免疫细胞为对象，队列与设计不可直接比较，但共同指向一个缺口：体外细胞系体系难以反映组织与体内状态。

在体与空间维度上，**iGOF-Perturb-seq** 转向功能获得性扰动，在小鼠星形胶质细胞中构建 **约1000个转录因子**的功能图谱，识别共功能模块并注释未表征转录因子，并在神经炎症模型中鉴定 Ferd3l 为治疗候选 [39]；**SPAC-seq** 与配套的 TARDIS 工具则把 CRISPR 筛选推到空间分辨层面，将基因扰动与空间表型、通路关联，揭示 Icam1 缺失经免疫抑制促转移等现象 [38]。这两项工作拓展了扰动读出的维度，但前者限于小鼠与单一细胞类型、后者未明确说明通量与适用组织范围的限制，向人类与更广组织的转化仍需验证。

面向预测建模，资源形态从转录组扩展到蛋白质组与标准化基准。**ProteinTalks** 基于 **超过3800万条时序蛋白丰度测量**（系统扰动的乳腺癌细胞系）构建虚拟细胞模型，学习可迁移的动态潜表示，在药物疗效与协同预测、耐药蛋白发现、患者分层及类器官候选药物排序上普遍优于所选基准，并可迁移至患者类器官与临床活检 [37]。与之并行，Arc Institute 发起的 **Virtual Cell Challenge** 以反复举办的开放基准竞赛形式，提供评估框架与专用数据集，试图为扰动响应预测建立统一的比较场所 [48]；该文摘要未报告具体实验数据或定量结果，因此其实际区分度尚待赛事结果检验。值得注意的是，现有模型多以癌细胞系为主要训练来源 [37][26]，而原代细胞与在体数据规模相对有限 [28][39]，训练资源与评测目标之间的这种错位，是当前虚拟细胞预测需要正视的争议点。

## 4 评测与效度批判

评测效度批判的核心矛盾在 2025–2026 年集中爆发：多篇独立工作用不同数据集和指标得出同一方向性结论——**常用基准与指标系统性高估了扰动响应预测模型的真实能力**。一项系统评测在 25 个数据集、24 个指标上比较 13 个代表性方法，发现扰动效应幅度强烈影响泛化与双扰动预测，细胞类型迁移中源-目标转录组距离越大准确率越低 [17]；另一标准化模块化基准则指出常用设置下性能被高估、严格条件下性能显著下降，且不同指标导致模型排名差异显著 [49]。更直接的证据来自与简单基线的对照：五种基础模型和两种深度学习模型在单/双基因扰动转录组预测上**没有任何模型优于简单线性基线** [18]；在 Perturb-seq 数据上，最简单的 Train Mean 即优于 scGPT 与 scFoundation，带 GO 特征的随机森林在四个数据集上的 Pearson Delta 分别为 **0.739/0.586/0.480/0.648**，高于 scGPT 的 0.641/0.554/0.327/0.596 [36]。Systema 框架进一步把这一现象归因于「系统性变异」：当前方法难以泛化到扰动与对照细胞间由选择偏倚或混杂因素造成的一致转录差异之外，简单 perturbed mean 在 Pearson Δ 上跨所有数据集优于其他方法，双基因扰动中 matching mean 显著更优 [40]。

对上述「深度学习不如基线」的结论存在明确争议。一项提出阳性对照基线与指标校准框架的研究在 14 个数据集、18 个指标上发现，**MSE 和 Pearson Δ 等常用指标常校准不良**，降低了对阳性模型性能的敏感性；在良好校准指标下，深度学习扰动模型可优于无信息基线 [19]。这与 Systema 关于「常见指标易受偏倚影响导致高估」的诊断部分一致（都指向指标问题），但结论方向相反：前者认为换用校准指标后深度模型可胜出，后者认为即便强调扰动特异性效应，简单基线仍常占优。争议的实质在于「什么算有效基线」与「指标是否对真实信号敏感」尚未形成共识。

数据划分方式是效度批判的另一主战场。细胞级随机划分会把同克隆、同患者细胞连同其标签一起放入训练集，模型可靠「记忆亲属」而非学习可迁移规则；该研究提出用暴露度与可检索性在训练前估计泄漏，并给出 leakcheck 工具，在患者队列中泄漏足以推翻临床结论 [20]。EL-PERTURB 采用分层分布外划分，在必需基因与全基因组 Perturb-seq 数据上压力测试 6 类架构的 20 个模型，结论是**现有基准多依赖随机划分而掩盖系统性失效模式，扰动预测模型在真实 OOD 条件下泛化失败** [21]。药物响应领域有平行发现：模型通常能做癌症盲预测，但**药物盲性能显著下降、部分模型完全失败**，单药药物盲泛化主要限于同类内 [41]。这些结果共同说明，随机划分下的高分不能外推为对未见扰动或未见情境的预测能力。

基准的覆盖范围本身也被质疑。scArchon 提供容器化可复现流程并标准化评估九种工具，但明确**仅限非遗传扰动，基因敲除作为独立问题未纳入** [29]；AssayBench 基于 **1920 个 CRISPR 筛选、五类细胞表型**构建表型筛选预测基准，发现现有方法远未达经验性能上限，且零样本通用 LLM 优于生物学专用 LLM 和可训练基线 [30]；VCBench 把四个虚拟细胞框架综合为七个能力维度，结果显示**基线在五个评分维度中的四个匹配或超过所有基础模型**，TranscriptFormer 虽在跨模态 RNA 到蛋白预测上 Pearson 提升 **53%** 但时间排序性能崩溃，且没有基础模型发布完整细胞级训练清单、数据污染对用户不可检测 [31]。三者指向同一缺口：单任务、单模态基准无法刻画「虚拟细胞」宣称的多维能力，而可测试性在多尺度整合与端到端 in silico 实验上结构性地不成立。

预训练规模的效度同样被重新审视。用 **2220 万细胞**预训练 **400 个模型**并开展 **6400 次实验**的研究发现，性能在数据规模远小于现有语料时即达平台期，**无明确数据缩放定律**，提示应平衡模型容量、数据规模与算力而非盲目扩大 [22]。这与基础模型「越大越好」的叙事构成直接张力，也解释了为何在受控基准上大模型未必胜过简单基线。

在因果层面，效度问题从「预测准不准」延伸到「解释是否成立」。综述指出，把统计关联解读为因果效应需要超出标准统计分析的额外假设，基于共表达相关性的传统方法难有因果解释，且这类设计**仅能识别一个基因敲低对另一基因的因果效应，无法直接推断两基因间因果效应** [32]。早期 Perturb-seq 流形工作则展示了另一种效度来源：将高维单细胞表型映射为细胞状态流形，实现通路无偏排序与遗传互作的原则性分类，但其局限是依赖生长表型挖掘强遗传互作、覆盖有限 [33]。二者共同提示，扰动预测的「真值」本身依赖实验设计与假设，评测必须把因果识别条件纳入考量。

面向未来，Virtual Cell Challenge 2026 把评测目标明确设为跨多个独立细胞情境的零样本预测，要求在新 Arc 数据集上预测未见细胞系中的基因敲低响应，以检验最优模型能否缩小临床前实验预测与人类生物学之间的差距 [34]。这与前述 OOD、泄漏与指标校准批评方向一致，但能否解决「简单基线常胜」与「指标校准争议」两个未决问题，仍取决于其划分策略与指标选择是否公开可审计。

## 5 产业动态

（本节暂无入库证据）

## 6 空白与趋势

**趋势一：评测效度批判从“单点质疑”走向“系统性框架”，但批判者之间尚未就“何为有效基线”达成共识。** 一方面，Systema 把深度模型失效归因于系统性变异，并报告简单 perturbed mean 在 Pearson Δ 上跨所有数据集优于其他方法[40]；另一方面，阳性对照基线与指标校准框架在 14 个数据集、18 个指标上发现 MSE 与 Pearson Δ 常校准不良，而在良好校准指标下深度模型可优于无信息基线[19]。**两条结论方向相反，却共享“常用指标不可靠”的诊断**，说明该领域缺少的是被共同接受的基线集合与指标校准协议，而非更多单点胜负结论。EL-PERTURB 的分层 OOD 压力测试与 leakcheck 的泄漏估计工具分别从划分与泄漏两侧提供了可操作抓手[21][20]，但尚无工作把划分策略、指标校准与基线选择整合为单一可审计流程。

**趋势二：世界模型叙事与可验证预测能力之间出现明显断层，闭环智能体是唯一给出定量迭代增益的中间层。** 愿景论文主张虚拟细胞应支持动作条件仿真、反事实推理与长程规划，但未报告定量结果[24]；Chreode 虽自称一步式细胞世界模型并在 GEARS 上把 DE20 MSE 从 0.2121 降至 0.1858，却明确只做预测建模、不声称具备规划能力[23]。**“世界模型”一词目前被同时用于指代单步状态转移与长程规划两种能力，缺乏区分性定义**。CellScientist 的假设—实现闭环把 PCC 由 0.3416 提升至 0.4368 并产出可审计轨迹[25]，但其精炼依赖 LLM 代理、长程工作流仍脆弱，且未与 Chreode 类单步模型在同一协议下比较。**没人做的方向**：把“是否具备规划/反事实能力”写成可执行测试（而非架构声明），并让闭环智能体在统一基准上同时报告预测精度与迭代成本。

**趋势三：知识先验与小数据路线对“规模至上”构成实质挑战，但先验质量本身缺少评测。** 知识图谱 KNN 经 RL 优化邻域后在 Replogle 2022 上达 SOTA[9]，scKITE 仅用 179,067 个预训练样本（不足先前强模型 0.5%）即超越 Geneformer、scGPT 等并带来平均 28.8% 相对提升[10]，而 2220 万细胞、400 个模型、6400 次实验的研究发现性能在数据规模远小于现有语料时即达平台、无清晰数据缩放定律[22]。**三方证据共同指向“先验注入方式比数据量更关键”，但没有任何工作系统评测先验本身的质量与错误传播**：D²R² 的排序依赖推断的 GRN 质量[6]，TFActProfiler 虽提供可靠性度量[42]，却未被纳入端到端生成模型的误差分析。**空白**：先验错误如何在后端生成中被放大或吸收，目前无定量刻画。

**趋势四：扰动数据资源在模态与情境上快速扩张，但训练资源与评测目标之间存在结构性错位。** 药物侧有 Tahoe-100M 的 1 亿转录组、50 个癌细胞系、1100 种药物-剂量条件[26]，基因侧有超 250 万细胞的全基因组 Perturb-seq[27]与 2200 万原代 CD4+T 细胞图谱[28]，蛋白侧有超 3800 万条时序蛋白丰度测量[37]，空间侧有 SPAC-seq[38]，在体侧有约 1000 个转录因子的 iGOF-Perturb-seq[39]。然而 Virtual Cell Challenge 2026 明确要求跨独立细胞情境的零样本预测、在新 Arc 数据集上预测未见细胞系中的基因敲低响应[34]，而现有模型多以癌细胞系为主要训练来源[37][26]。**原代细胞与在体数据规模相对有限，却正是评测想要外推的目标域**。**没人做的方向**：构建“训练域—评测域”显式错位的资源分层协议，量化域距离与性能衰减的关系；跨物种侧 Speciesformer 的 1.31 亿细胞 SpeciesCorpus 提供了可用的表征基础[14]，但尚未与上述情境错位问题对接。

**趋势五：生成范式的竞争已从“用哪种生成器”转向“监督信号放在哪里”，但跨范式统一比较仍缺位。** 监督位置从潜空间向量[1]、连续时间去噪[3]、训练阶段直接表型监督[16]，到调控引导的基因级渐进生成[6]与条件传输的端点对齐[5]，各自在自有基准上报告优势。**但这些工作分别验证于 CRISPR 七项指标、Norman19/H1、BBBC021 等不同数据集与指标，跨研究数字不可直接比较**，且 AssayBench 显示零样本通用 LLM 优于生物学专用 LLM 和可训练基线[30]，VCBench 显示基线在五个评分维度中的四个匹配或超过所有基础模型[31]。**空白**：尚无一个基准同时容纳流匹配、离散扩散、条件传输与 RL 后训练四类生成器，并在校准指标与 OOD 划分下给出统一排名；scArchon 虽提供容器化可复现流程，却明确仅限非遗传扰动[29]。

**趋势六：因果识别条件被逐步写入模型设计，但“预测真值”本身的假设依赖尚未进入评测协议。** CauTrigger 把 do-calculus 整合进分层潜变量模型以分离因果与虚假潜因子[44]，D-SPIN 从跨数千扰动条件推断可解释、可生成的调控网络[11]，RegVelo 联合建模剪接动力学与调控互作并经 CRISPR 验证[43]。但综述明确指出，这类设计仅能识别一个基因敲低对另一基因的因果效应，无法直接推断两基因间因果效应，因果解读需超出标准统计分析的额外假设[32]。**这意味着基准里的“真值”本身是设计依赖的**，而现有评测框架尚未把因果识别假设列为报告项。**没人做的方向**：在基准提交中强制披露因果假设与可识别边界，并把“在何种假设下该预测成立”作为与精度并列的评分维度。

## 7 未归类新证据

这篇综述提出 **AI 虚拟细胞（AIVC）** 的统一技术框架，主张通过整合多组学数据，从跨尺度表征工程、功能子模块设计与多组件动态调控机制三方面分解建模问题，以突破传统实验与生化分析在时空分辨率和处理能力上的限制 [35]。作者将 AIVC 定位为生命科学从观测分析转向可预测与创新的新范式，并系统梳理了现有模型与数据集资源（如 **GeneCompass、Tahoe-100M**）[35]。

不过该文属综述性质，汇总现有模型与数据集而未自行分析样本，因此未提供可比较的定量性能结果 [35]。作者同时指出，**数据异质性与模型可解释性**等挑战尚未解决，AIVC 仍处早期阶段 [35]。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 扰动响应生成模型（flow matching / 扩散 / 最优传输 / 因果潜动力学） | 朝阳 | 方法谱系从 scGen 的潜空间加性扰动 [1] 演进到 State 的跨上下文状态迁移 [12] 与 X-Cell 的因果扰动预测规模化 [4]，说明范式仍在快速换代而非收敛；scGPT [2] 提供通用表征底座但被后续工作当作基线而非终点。雷达样本中该节 n=22、近两年占比 0.89，属证据最密集的一节，但 median_citations=0 说明大量新工作尚未经时间检验，符合「爆发但未收敛」。 |
| 细胞世界模型与闭环智能体 | 萌芽 | 仅 3 篇且全部为 2026 年：Chreode 提出一步式时序动力学与扰动预测的世界模型 [23]，CellScientist 做双空间分层编排的闭环精化 [25]，另有虚拟细胞世界模型的立场性论述 [24]。概念已被提出但无独立复现、无跨数据集验证，属典型少量探索性工作。 |
| 扰动数据资源（Perturb-seq 图谱、Tahoe、Virtual Cell Challenge） | 朝阳 | 基因组尺度 Perturb-seq 图谱 [27] 奠定数据基础，Virtual Cell Challenge 以「图灵测试」形式把评测标准化 [48]，并已向空间分辨功能基因组学扩展 [38]。数据侧已从「造数据」转向「定标准」，但标准刚立、参赛方法未定，属朝阳。 |
| 评测基准与效度批判 | 朝阳（且已出现明确的负面结论） | 关键证据是「深度学习扰动预测尚不能超越简单基线」[18] 与细胞基础模型扰动后 RNA-seq 预测的系统评测 [36]，二者共同构成对上一节生成模型的效度挑战；Systema 进一步把评测从「拟合表达」推进到「超越表达的遗传扰动响应」[40]。批判性工作密集出现且被高引，说明该节正在定义领域的问题框架，是当前话语权最高的位置。 |
| 产业动态 | 证据不足 | 雷达样本中该节 n=0，无可核验技术细节的发布可引，无法判断阶段。 |

**整体判断**：这个方向整体处于**朝阳期的中段偏后**——生成模型侧方法快速换代（雷达样本中 2.1 节 n=22、近两年占比 **0.89**），数据与评测侧刚完成标准化（Virtual Cell Challenge [48]），而**最硬的结论是负面的**：现有深度模型尚未跑赢简单基线 [18]。这意味着「再提一个更强的扰动预测网络」的边际收益正在快速下降，而「说清楚什么条件下模型真的有效」的收益在上升。窗口期估计 **12–18 个月**：世界模型/闭环智能体 [23][25] 目前只有概念性工作，谁先给出可复现的闭环验证谁就占位；一旦大厂把 Virtual Cell Challenge 类基准刷成排行榜游戏，独立组的切入空间会被压缩。最大不确定性有两点：一是**评测效度**——若「不跑赢基线」的结论在更多数据上被确认，整个生成模型子领域的叙事需要重写；二是**数据覆盖**——现有 Perturb-seq 图谱 [27] 以细胞系为主，类器官/原代体系上的扰动响应是否可迁移完全未知，而这恰好是博后合作项目的优势区。

**接下来怎么做**：

1. **把「效度批判」做成自己的方法学标签，而不是回避它。** 切入点：以 [18] 的基线协议为骨架，在**类器官多组学数据**上重做一次分层评测（按扰动类型、细胞类型未见程度、供体差异分层），并加入 [40] 的「超越表达」指标。产出：一个可复用的分层评测框架 + 一篇「基础模型在类器官扰动上何时失效」的实证论文。为什么现在：负面结论刚出、尚未有人在非细胞系体系上验证，先做先定义标准。

2. **用公共数据做「跨上下文迁移」的 demo，直接对准 State / X-Cell 的软肋。** 切入点：拿 [12] 与 [4] 的跨上下文设定，在公开 Perturb-seq [27] 上训练、在类器官/原代数据上零样本测试，量化「上下文外推」的真实衰减。产出：一个迁移性诊断报告 + 一个轻量适配器（不需要重训基础模型）。为什么现在：这两篇都是 2026 年新工作、引用个位数，复现与压力测试的空白期最短。

3. **把闭环智能体作为差异化切口，但绑定在「实验可执行」上。** 切入点：借鉴 [25] 的编排思路与 [23] 的一步式动力学，做一个**小闭环**：模型提假设 → 选下一批扰动 → 用类器官实验或公共数据回填 → 迭代。产出：闭环协议 + 一个可复现的主动学习基线。为什么现在：该节仅 3 篇、全部 2026 年，属萌芽期，**先发即定义**；且闭环天然需要湿实验合作，正是博后合作项目的结构优势。

4. **以 Virtual Cell Challenge 为公共 demo 的锚点，做「参赛+批判」双身份。** 切入点：用 [48] 的官方任务与数据做公开可复现的 baseline，同时发布误差分解分析。产出：开源 repo + 技术报告，成本低、可见度高。为什么现在：基准刚立、社区尚无公认强基线，此时提交的 baseline 容易被引用为参照。

5. **暂不投入「再训一个单细胞基础模型」。** 依据：scGPT [2] 已是高引底座，而 [36] 显示基础模型在扰动后预测上优势有限；在算力与数据都不占优的情况下，**适配与评测**的性价比显著高于预训练。把省下的精力投到第 1、2 条。

## 参考文献

1. scGen predicts single-cell perturbation responses. Nature Methods 2019. https://doi.org/10.1038/s41592-019-0494-8
2. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. Nature Methods 2024. https://doi.org/10.1038/s41592-024-02201-0
3. OCOO-T : A Simple and Scalable Virtual Cell Model for Transcriptional Perturbation Response Prediction.  2026. https://arxiv.org/abs/2606.12838v2
4. X-Cell: Scaling Causal Perturbation Prediction Across Diverse Cellular Contexts via Diffusion Language Models.  2026. https://doi.org/10.64898/2026.03.18.712807
5. SCALE:Scalable Conditional Atlas-Level Endpoint transport for virtual cell perturbation prediction.  2026. https://arxiv.org/abs/2603.17380v3
6. $D^{2}R^{2}$: Discrete Diffusion with Regulation Reinforcement for Single-Cell Perturbation Prediction.  2026. https://arxiv.org/abs/2608.15288v1
7. scBalFlow: A Staged Flow Matching Framework for Imbalanced Single-Cell Drug Perturbation Prediction.. Bioinformatics (Oxford, England) 2026. https://doi.org/10.1093/bioinformatics/btag682
8. scDEFT: A deep learning framework for drug-effect prediction and counterfactual reasoning.  2026. https://arxiv.org/abs/2609.10831
9. Knowledge Graphs and Reasoning LLMs for Finding Simple Yet Effective Transcriptomic Perturbation Predictors.  2026. https://arxiv.org/abs/2606.08816v1
10. Towards a knowledge-enhanced single-cell foundation model.  2026. https://arxiv.org/abs/2609.14970
11. D-SPIN constructs regulatory network models from scRNA-seq that reveal organizing principles of perturbation response.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.028
12. Predicting cellular responses to perturbation across diverse contexts with State. Cell 2026. https://doi.org/10.1016/j.cell.2026.07.052
13. Tahoe-x1: Scaling Perturbation-Trained Single-Cell Foundation Models to 3 Billion Parameters. bioRxiv 2025. https://doi.org/10.1101/2025.10.23.683759
14. Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling.  . https://doi.org/10.64898/2026.09.22.752128
15. CellFluxRL: Biologically-Constrained Virtual Cell Modeling via Reinforcement Learning.  2026. https://arxiv.org/abs/2603.21743v4
16. PerturbBridge: Direct Phenotypic Supervision for Cellular Perturbation Generation.  . https://arxiv.org/abs/2610.17066
17. A systematic comparison of single-cell perturbation response prediction models.. Science advances 2026. https://doi.org/10.1126/sciadv.aed3414
18. Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines. Nature methods 2025. https://doi.org/10.1038/s41592-025-02772-6
19. Deep learning perturbation models can outperform baselines on calibrated metrics.. Nature biotechnology . https://doi.org/10.1038/s41587-026-03307-w
20. Cell-level random splits leak group-owned answers in single-cell benchmarks. bioRxiv 2026. https://doi.org/10.64898/2026.09.09.750484
21. Genetic Perturbation Prediction Models Fail Out-of-Distribution: A Rigorous Benchmark and Systematic Evaluation.  . https://doi.org/10.64898/2026.10.16.759604
22. Evaluating the role of pretraining dataset size and diversity on single-cell foundation model performance.. Nature methods 2026. https://doi.org/10.1038/s41592-026-03120-y
23. Chreode: A Cell World Model for One-Step Temporal Dynamics and Perturbation Prediction.  2026. https://arxiv.org/abs/2605.28111v1
24. A world model of the virtual cell.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.042
25. CellScientist: Dual-Space Hierarchical Orchestration for Closed-Loop Refinement of Virtual Cell Models.  2026. https://arxiv.org/abs/2605.07335v1
26. Tahoe-100M: Mapping drug-induced molecular phenotypes at single-cell resolution.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.035
27. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. bioRxiv 2021. https://doi.org/10.1016/j.cell.2022.05.013
28. Genome-scale perturb-seq in primary human CD4&lt;sup&gt;+&lt;/sup&gt; T cells maps context-specific regulators of T cell programs and human immune traits.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.002
29. scArchon: a scalable benchmarking framework for assessing single-cell perturbation models.. Genome biology 2026. https://doi.org/10.1186/s13059-026-04104-z
30. AssayBench: An Assay-Level Virtual Cell Benchmark for LLMs and Agents.  2026. https://arxiv.org/abs/2605.10876v1
31. VCBench: A Multi-Dimensional Benchmark for Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.06.18.733146
32. Causal effect estimation from trans-regulatory single-cell CRISPR screens.. Cell genomics 2026. https://doi.org/10.1016/j.xgen.2026.101251
33. Exploring genetic interaction manifolds constructed from rich single-cell phenotypes. Science 2019. https://doi.org/10.1126/science.aax4438
34. Virtual Cell Challenge 2026: Benchmarking zero-shot generalization across cellular contexts.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.004
35. Artificial intelligence-enabled multi-scale virtual cell: perspective, challenges, and opportunities.. Briefings in bioinformatics 2026. https://doi.org/10.1093/bib/bbag104
36. Benchmarking foundation cell models for post-perturbation RNA-seq prediction. BMC genomics 2025. https://doi.org/10.1186/s12864-025-11600-2
37. An operational perturbation proteomics-based virtual cell model.. Nature 2026. https://doi.org/10.1038/s41586-026-11001-9
38. Uncovering spatially resolved functional genomics with CRISPR screen sequencing.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.049
39. Mapping transcription factor functions in astrocytes using in vivo gain-of-function Perturb-seq.. Science (New York, N.Y.) 2026. https://doi.org/10.1126/science.adw2156
40. Systema: a framework for evaluating genetic perturbation response prediction beyond systematic variation. Nature biotechnology 2026. https://doi.org/10.1038/s41587-025-02777-8
41. Monotherapy cancer drug-blind response prediction is limited to intraclass generalization.. PLoS computational biology 2026. https://doi.org/10.1371/journal.pcbi.1013232
42. A transcription factor regulatory atlas for activity inference and perturbation prediction. Nucleic Acids Research 2026. https://doi.org/10.1093/nar/gkag897
43. RegVelo: Gene-regulatory-informed dynamics of single cells.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.022
44. CauTrigger: deciphering biological system state transitions by hierarchical causal decomposition.. Nature methods . https://doi.org/10.1038/s41592-026-03274-9
45. Deep dynamical models of single-cell multiomic velocities predict loss-of-function and rescue perturbations in B cells.. Nature biotechnology . https://doi.org/10.1038/s41587-026-03348-1
46. Predicting how perturbations reshape cellular trajectories with PerturbGen.  2026. https://doi.org/10.64898/2026.03.04.709254
47. UniPert-G2CP bridges genetic and chemical screens from molecular representation to phenotype modeling.. Cell 2026. https://doi.org/10.1016/j.cell.2026.06.005
48. Virtual Cell Challenge: Toward a Turing test for the virtual cell. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.008
49. Benchmarking virtual cell models for in-the-wild perturbation response.  2026. https://arxiv.org/abs/2604.27646v1
