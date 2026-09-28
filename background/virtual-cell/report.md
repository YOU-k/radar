# 虚拟细胞与扰动响应预测 · 方向背景报告

证据 44 篇 · 覆盖度 0.56 · 第 4 轮 · 更新 2026-09-28

## 摘要（TL;DR）

- 早期范式以潜空间扰动向量为代表，scGen 用变分自编码器在潜空间中加减扰动向量，实现跨细胞类型与跨物种的响应预测 [1]。
- scGPT 在超过 3300 万个单细胞 RNA 测序图谱上预训练生成式 Transformer，通过迁移学习适配扰动响应预测等下游任务 [2]。
- State 的细胞嵌入训练于 1.67 亿细胞，在大型数据集上效应区分度提升超过 30%，且嵌入可识别训练中未观察扰动的细胞环境 [3]。
- Tahoe-x1 将扰动训练的单细胞基础模型扩展到最高 30 亿参数，计算效率比先前细胞状态模型实现高 3–30 倍 [4]。
- X-Atlas/Pisces 构建了迄今最大的全基因组 CRISPRi Perturb-seq 数据集，含 2560 万扰动单细胞转录组、16 种生物学情境，其 X-Cell 在 Pearson Δ 等关键指标上优于现有最先进模型最高达五倍 [5]。
- scKITE 仅用 179,067 个预训练样本（不足先前强模型 0.5%）即在多下游任务超越 Geneformer、scGPT 等，知识增强训练带来平均 28.8% 相对提升 [6]。
- 一项工作证明利用知识图谱的最简 KNN 模型在分布外扰动预测上击败几乎所有方法，并用强化学习优化推理 LLM 调整邻域，在 Replogle 2022 细胞系上达到当前 SOTA 水平 [7]。
- 争议之一在于模型复杂度与性能是否匹配，OCOO-T 的极简流匹配与知识图谱 KNN 的“简单却有效”同 X-Cell、Tahoe-x1 等大规模多模态基础模型在不同基准上各自报告优势，尚缺乏统一评测 [8][7][5][4]。
- 多项独立工作一致发现简单基线常匹配或超越复杂基础模型，在单/双基因扰动转录组预测中五种基础模型与两种深度学习模型均未优于简单线性基线 [9]。
- 用 2220 万细胞预训练 400 个模型并开展 6400 次实验，性能在数据规模远小于现有语料时即达平台期，无明确数据缩放定律 [10]。
- 2026 年虚拟细胞挑战赛提出跨多个独立细胞情境的零样本预测，参赛者需在 Arc 生成的新数据集上预测未见细胞系中的基因敲低响应 [11]。
- AIVC 仍处于早期阶段，数据异质性与模型可解释性等挑战尚未解决 [12]。

## 1 背景与定义

虚拟细胞与扰动响应预测的边界，可以从"预测什么"与"以什么为单位"两个维度界定。早期工作以潜空间扰动向量为代表，scGen 用变分自编码器在潜空间中加减扰动向量，实现跨细胞类型与跨物种的响应预测，为后续工作奠定基础 [1]。此后路线分化：一类以生成式预训练为核心，scGPT 在超过 **3300 万个**单细胞 RNA 测序图谱上预训练生成式 Transformer，通过迁移学习适配扰动响应预测等下游任务 [2]；另一类强调跨环境泛化，State 用单细胞基因表达数据训练并在预测中显式考虑实验内与跨实验的细胞异质性，其细胞嵌入训练于 **1.67 亿**细胞，在大型数据集上效应区分度提升超过 **30%** [3]。**该方向的核心问题并非单纯拟合对照到扰动的映射，而是预测未见情境、未见扰动与跨数据集条件下的响应，并判断这种预测是否具有生物学效度。**

演化脉络上，数据规模与参数规模的扩张构成一条主线。Tahoe-x1 将扰动训练的单细胞基础模型扩展到最高 **30 亿**参数，预训练数据包括 Tahoe-100M 扰动汇编，计算效率比先前细胞状态模型实现高 **3–30 倍** [4]；X-Atlas/Pisces 构建迄今最大的全基因组 CRISPRi Perturb-seq 数据集，含 **2560 万**扰动单细胞转录组、**16 种**生物学情境，并据此开发扩散语言模型 X-Cell，在 Pearson Δ 等关键指标上优于现有最先进模型最高达 **五倍** [5]；Speciesformer 则在包含 **1.31 亿**细胞的 SpeciesCorpus 上预训练，将进化表征学习与虚拟细胞状态生成结合 [13]。与之并行的是建模范式的更替：扩散与流匹配成为近年的主要选择，OCOO-T 主张极简路线，用普通 Transformer 直接作用于连续基因表达谱，将扰动响应预测建模为连续时间去噪过程 [8]；SCALE 针对对照与处理细胞为非配对群体这一设定，将细胞表示为无序集合、预测处理群体而无需细胞级配对 [14]；D²R² 则把生成粒度下沉到基因层面，用掩码离散扩散以序数 token 逐步重建表达谱 [15]。**从潜向量加减到集合级传输、再到基因级离散生成，方法的分歧本质上是对"扰动响应分布应如何被参数化"的不同回答。**

调控网络与先验知识被多篇工作用作提升外推能力的抓手，但对"需要多复杂模型"存在明显张力。D-SPIN 从跨数千扰动条件的单细胞 mRNA-seq 数据推断机制可解释且可生成的基因调控网络模型，通过重构调控相互作用解释扰动如何改变细胞状态比例 [16]；TFActProfiler 整合先验与大规模 RNA-seq 图谱，学习带符号定量的 TF–mRNA 调控系数，无需额外训练即可预测 TF 扰动转录组响应 [17]。与之形成对照的是，一项工作证明利用知识图谱的最简 KNN 模型在分布外扰动预测上击败几乎所有方法，并用强化学习优化推理 LLM 调整邻域，在 Replogle 2022 细胞系上达到当前 SOTA 水平 [7]；scKITE 则从数据缩放角度给出另一条证据：仅用 **179,067** 个预训练样本（不足先前强模型 **0.5%**）即在多下游任务超越 Geneformer、scGPT 等，知识增强训练带来平均 **28.8%** 相对提升 [6]。**先验质量与模型容量孰为瓶颈，目前尚无统一定论，二者在不同基准上各自报告优势。**

"细胞世界模型"的提法把方向边界进一步推向外推与规划。Chreode 采用一步式细胞世界模型，通过结构化残差转移算子预测动作条件下的状态转移，把分布演化从推理时移至训练时，在 240 万细胞小鼠胚胎图谱、7 个数据集上预训练，但作者明确仅做预测建模，不声称具备规划或推演能力 [18]。与之相对，VCWM 框架主张虚拟细胞应是多模态、多尺度、有状态的动态计算系统，支持动作条件仿真、反事实推理与长程规划，使干预在演化状态中传播，而非仅优化特定任务端点；该文属愿景性论文，未报告定量结果与实验验证 [19]。**两者的张力在于：前者以可验证的预测精度推进，后者以能力边界更宽的架构为目标，但后者尚无实证支撑。** 闭环精炼则针对预测失败后的归因问题，CellScientist 将高层假设空间与低层可执行实现空间耦合，把执行偏差路由回相应层级，案例中 **PCC 由 0.3416 提升至 0.4368**，但其精炼依赖 LLM 代理，长程工作流仍脆弱 [20]。

数据资源与评测效度构成该方向的两条约束线。Tahoe-100M 通过 Mosaic 平台将遗传上不同的细胞模型多重化为平衡的"细胞村"，构建了包含 **1 亿转录组**、50 个癌细胞系、1100 种药物-剂量条件的图谱 [21]；基因组规模 Perturb-seq 以 CRISPRi 靶向全部表达基因、覆盖 **超过 250 万人类细胞** [22]；ProteinTalks 基于超过 **3800 万条时序蛋白丰度测量** 学习可迁移的动态潜表示 [23]。这些资源在规模指标上口径不一，不宜直接横向比较。评测方面，多项独立工作一致发现简单基线常匹配或超越复杂基础模型：五种基础模型与两种深度学习模型均未优于简单线性基线 [9]；Systema 框架下 perturbed mean 在 Pearson Δ 上跨所有数据集优于其他方法 [24]；VCBench 评估的五种基础模型中，基线在五个评分维度中的四个匹配或超过所有基础模型 [25]。**这些结果跨不同数据集与指标反复出现，指向同一判断：在评测设置未充分控制系统性变异、数据泄漏与任务结构差异之前，虚拟细胞模型的性能声明应被视为高度情境依赖，而非可迁移的生物学能力。**

## 2 方法学


### 2.1 扰动响应生成模型

单细胞扰动响应预测的早期范式以潜空间扰动向量为代表：**scGen** 用变分自编码器在潜空间中加减扰动向量，实现跨细胞类型与跨物种的响应预测，为后续工作奠定基础 [1]。此后生成式预训练路线兴起，**scGPT** 在超过 **3300 万个**单细胞 RNA 测序图谱上预训练生成式 Transformer，通过迁移学习适配细胞类型注释、多批次与多组学整合、扰动响应预测、基因网络推断等下游任务 [2]。与之相对，**State** 强调跨细胞环境的泛化，用单细胞基因表达数据训练并在预测中显式考虑实验内与跨实验的细胞异质性，其细胞嵌入训练于 **1.67 亿**细胞，在大型数据集上效应区分度提升超过 **30%**，差异表达基因识别准确率显著优于基线，且嵌入可识别训练中未观察扰动的细胞环境 [3]。

数据规模与参数规模的扩张成为一条主线。**Tahoe-x1** 将扰动训练的单细胞基础模型扩展到最高 **30 亿**参数，预训练数据包括 Tahoe-100M 扰动汇编，通过架构优化与训练策略改进，计算效率比先前细胞状态模型实现高 **3–30 倍**，在基因必需性、癌症标志基因、细胞类型分类和留出环境扰动响应预测四个基准上均达最先进性能 [4]。**X-Atlas/Pisces** 则构建了迄今最大的全基因组 CRISPRi Perturb-seq 数据集，含 **2560 万**扰动单细胞转录组、**16 种**生物学情境，并据此开发扩散语言模型 **X-Cell**，通过交叉注意力整合自然语言、蛋白质语言模型与互作网络等多模态先验，在 Pearson Δ 等关键指标上优于现有最先进模型最高达 **五倍**，并展示零样本预测能力 [5]。跨物种方向亦有尝试，**Speciesformer** 在包含 **1.31 亿**细胞的 SpeciesCorpus 上预训练，将进化表征学习与虚拟细胞状态生成结合，旨在区分保守生物学原理与物种、组织及细胞环境特异变异 [13]。

在生成建模范式上，扩散与流匹配成为近年的主要选择，但具体设计分歧明显。**OCOO-T** 主张极简路线，用普通 Transformer 直接作用于连续基因表达谱，将扰动响应预测建模为连续时间去噪过程，通过自适应层归一化和上下文 token 整合扰动、剂量与细胞系信息，在 Tahoe100M、Replogle、PBMC 上达到最先进性能并可扩展至长转录谱；作者同时指出基于扩散/流匹配的方法学习对照到扰动分布仍具挑战 [8]。**SCALE** 针对对照与处理细胞为非配对群体这一设定，将细胞表示为无序集合、预测处理群体而无需细胞级配对，共享集合感知编码器与条件 DiT 骨干学习潜传输使端点监督直接 delta 对齐，在 CRISPR 数据 **7 项**指标上优于竞争方法并保持基因靶表示分离，其预测的细胞因子差异经 **3 名**供体 PBMC 实验验证 [14]。**scBalFlow** 则聚焦药物扰动数据的类别严重不平衡问题，采用两阶段解耦训练：第一阶段预测扰动响应强度并用高斯增强推断缓解不平衡，第二阶段跳过弱响应条件并用 Flow Matching 合成高响应样本，在 SciPlex3 和 McFarland 等大规模基准上显著优于现有 SOTA，尤其能捕捉复杂分布偏移并保持单细胞分布一致性 [26]。

另一类工作把生成粒度下沉到基因层面或引入离散扩散。**D²R²** 将扰动预测重构为调控引导的基因级渐进生成，用掩码离散扩散以序数 token 逐步重建表达谱，调控策略模块由对照细胞 GRN 初始化并经组相对策略优化微调排序，在 Norman19 **五项**指标最优、H1 具竞争力，消融显示生物先验排序优于随机与不确定性启发式，且优先调控基因与扰动特异 TF [15]。**PerturbGen** 把预测对象从静态响应扩展到动态轨迹，作为训练于超 **1 亿**单细胞转录组的生成式基础模型，预测源状态遗传扰动如何塑造下游状态、改变基因程序与轨迹，在免疫挑战、造血与皮肤发育三套数据中预测 IL1B 敲除减弱后续细胞因子-干扰素程序，与 IL-1β 刺激逆转一致 [27]。**RegVelo** 则从动力学角度切入，联合建模剪接动力学与基因调控互作，在多种生物系统中预测终态、基因互作和扰动模拟，并结合计算机扰动、CRISPR-Cas9 敲除与单细胞 Perturb-seq 验证，确立 tfec 为早期驱动因子、elf1 为色素细胞命运调控因子 [28]。

调控网络与先验知识被多篇工作用作提升外推能力的抓手，但对"需要多复杂模型"存在明显张力。**D-SPIN** 从跨数千扰动条件的单细胞 mRNA-seq 数据推断机制可解释且可生成的基因调控网络模型，通过重构调控相互作用解释扰动如何改变细胞状态比例，在 Perturb-seq 和药物响应数据上识别细胞命运关键调控因子、解析药物组合的加性基因程序招募，并模拟未观测剂量组合下的免疫细胞群结构变化 [16]。**TFActProfiler** 整合 ChIP 类、motif 类与人工整理先验及大规模 RNA-seq 图谱，学习带符号定量的 TF–mRNA 调控系数，在多细胞类型 TF 敲低基准上优于现有 TF 活性推断方法，且无需额外训练即可预测 TF 扰动转录组响应 [17]。与之形成对照的是，一项工作证明利用知识图谱的最简 KNN 模型在分布外扰动预测上击败几乎所有方法，并用强化学习优化推理 LLM 调整邻域，在 Replogle 2022 细胞系上达到当前 SOTA 水平，RL 训练还提升 LLM 在差异表达预测上的表现 [7]。**scKITE** 则从数据缩放角度给出另一条证据：细胞文本注释与基因调控信息提供额外缩放维度，通过轻量辅助解码器注入监督（解码器仅预训练使用），仅用 **179,067** 个预训练样本（不足先前强模型 **0.5%**）即在多下游任务超越 Geneformer、scGPT 等，知识增强训练带来平均 **28.8%** 相对提升 [6]。

面向药物与临床情境的建模进一步引入条件化与因果解释。**scDEFT** 将药物视为细胞表征的条件算子，用特征级线性调制生成药物条件化潜变量并在冻结后由两个独立头按转录邻域聚合，预测状态变化与应答状态，反向阶段排序潜维度并映射到基因；在 **116 万**细胞 IBD 图谱（**3** 队列、**2** 类药物、**51** 供体）上，状态变化预测达 headroom 的 **45%**，治疗前应答分层 AUROC **0.70**，而标准预测器仅达随机水平，作者注明归因结果为待实验验证的假设 [29]。**UniPert-G2CP** 以两阶段框架统一多模态分子扰动表征并实现遗传到化学的表型迁移学习，在大规模遗传与化学筛选数据上验证，联合分析揭示药物响应异质性并为药物作用与耐药机制提供见解 [30]。此外，**CellFluxRL** 针对图像型虚拟细胞生成违反物理与生物约束的问题，用强化学习后训练 CellFlux，设计生物功能、结构有效性与形态正确性三类共 **七个**奖励，通过采样-优化交替提升高奖励样本似然，在所有奖励上优于基线且测试时扩展进一步增益，但作者指出奖励为加权线性组合、权重依赖人工设计且仅验证于 CellFlux 一种框架 [31]。

综合来看，该方向的争议集中在三点：其一，模型复杂度与性能是否匹配——一端是 OCOO-T 的极简流匹配与知识图谱 KNN 的"简单却有效"，另一端是 X-Cell、Tahoe-x1 等大规模多模态基础模型，二者在不同基准上各自报告优势，尚缺乏统一评测 [8][7][5][4]；其二，监督信号的选择——SCALE 强调端点监督直接 delta 对齐、无需辅助 delta 目标，而 D²R² 依赖推断的 GRN 质量进行排序，scKITE 则依赖注释与 GRN 推断质量，先验质量成为共同瓶颈 [14][15][6]；其三，外推与验证边界——多项工作报告零样本或跨情境能力，但验证范围多限于特定数据集或细胞系，scDEFT 明确将归因结果标为待实验验证的假设，D-SPIN 亦未提外推验证范围 [5][29][16]。

### 2.2 细胞世界模型与闭环智能体

细胞世界模型的核心分歧在于：是建模底层细胞系统本身，还是拟合特定任务的预测端点。Chreode 采用**一步式细胞世界模型**，通过结构化残差转移算子预测动作条件下的状态转移，把分布演化从推理时移至训练时，在 240 万细胞小鼠胚胎图谱、7 个数据集上预训练，GEARS 上 DE20 MSE 从 0.2121 降至 0.1858（相对提升 12.4%），Weinreb 与 Veres 上 Sinkhorn 距离优于匹配的从头训练模型，但作者明确仅做预测建模，不声称具备规划或推演能力 [18]。与之相对，VCWM 框架主张虚拟细胞应是多模态、多尺度、有状态的动态计算系统，支持动作条件仿真、反事实推理与长程规划，使干预在演化状态中传播，而非仅优化特定任务端点；该文属愿景性论文，未报告定量结果与实验验证 [19]。两者的张力在于：前者以可验证的预测精度推进，后者以能力边界更宽的架构为目标，但后者尚无实证支撑。

闭环精炼则针对预测失败后的归因问题。CellScientist 指出，预测偏差通过可执行实现被观察到，但相关修正可能落在建模假设、表征设计、实现或任务约束等不同层级，缺乏结构化反馈传播时，迭代可能只修代码而未修正导致偏差的假设；该框架将高层假设空间与低层可执行实现空间耦合，把执行偏差路由回相应层级，形成假设-实现-假设闭环，案例中 **PCC 由 0.3416 提升至 0.4368**，最终可执行模型在固定划分与评估协议下优于参考基线，并产生可审计的精炼轨迹，但其精炼依赖 LLM 代理，长程工作流仍脆弱 [20]。这一路线与 Chreode 的差异在于：Chreode 把能力限定在单步预测，CellScientist 则试图让模型在被证伪后定向修订，二者分别对应"预测得多准"与"错了能否改"两个子问题，目前尚无同一基准上的直接对照。

## 3 数据与资源

数据资源层面，单细胞扰动图谱的规模与覆盖范围正在快速扩张。**Tahoe-100M** 通过 Mosaic 平台将遗传上不同的细胞模型多重化为平衡的“细胞村”，构建了包含 **1亿转录组**、50个癌细胞系、1100种药物-剂量条件的图谱，并系统量化增殖、细胞毒性、谱系特异性脆弱性与细胞周期变化，通路特征可分类作用机制并揭示脱靶活性 [21]。与之互补的是基因组规模 Perturb-seq，以 CRISPRi 靶向全部表达基因、覆盖 **超过250万人类细胞**，据此发现核糖体生物发生新调控因子 CCDC86、ZNF236、SPATA5L1 等 [22]。在蛋白质层面，**ProteinTalks** 基于超过 **3800万条时序蛋白丰度测量** 的扰动乳腺癌细胞系数据，学习可迁移的动态潜表示，用于药物疗效与协同预测、耐药蛋白发现、患者分层及类器官候选药物排序 [23]。这些资源分别以转录组、基因组扰动和时序蛋白质组为核心，覆盖的细胞体系与扰动类型差异明显，尚不能相互替代。

在扰动体系的多样性上，不同工作向原代细胞、体内组织和空间维度延伸。探针式 perturb-seq 平台对 **2200万原代人CD4+T细胞**（4名供体）进行全表达基因扰动，测量静息与刺激后的转录组效应，发现活跃调控因子及所控程序随刺激条件剧变，并将扰动特征关联自身免疫病风险 [32]。iGOF-Perturb-seq 则采用体内功能获得性策略，在小鼠星形胶质细胞中构建 **约1000个转录因子** 的功能图谱，识别共功能模块并注释未表征TF，在神经炎症模型中鉴定 Ferd3l 为治疗候选 [33]。SPAC-seq 与 TARDIS 进一步把扰动与空间表型、通路关联，揭示 Icam1 缺失经免疫抑制促转移、Cd44 调控空间表型以及转录因子-趋化因子受体轴 [34]。这些体系在物种、细胞类型与读出维度上各不相同，其结论的适用范围也相应受限。

评估与基准建设方面，Arc Institute 建立的 **虚拟细胞挑战赛** 以预测细胞扰动响应为目标，提供评估框架、专用数据集和模型开发平台，作为反复举办的开放基准竞赛 [35]。该工作摘要未报告具体实验数据或定量结果，因此其与上述资源在性能上的可比性尚无法从现有证据判断。值得注意的是，各资源在规模指标上口径不一——转录组数、细胞数、蛋白测量数与扰动条件数分别来自不同研究设计，不宜直接横向比较；而 ProteinTalks 报告在药物疗效与协同预测等任务上“普遍优于所选基准” [23]，其对比仅在该研究自选的基准与评估协议下成立。

## 4 评测与效度批判

评测效度批判的核心争议在于：标准基准上的高分是否反映真实生物学泛化能力。多项独立工作一致发现，**简单基线常匹配或超越复杂基础模型**。在单/双基因扰动转录组预测中，五种基础模型与两种深度学习模型均未优于简单线性基线 [9]；在扰动后RNA-seq预测中，最简单Train Mean即优于scGPT和scFoundation，带GO特征的随机森林大幅领先 [36]；Systema框架下，perturbed mean在Pearson Δ上跨所有数据集优于其他方法，双基因扰动中matching mean显著更优 [24]；VCBench评估的五种基础模型中，基线在五个评分维度中的四个匹配或超过所有基础模型 [25]。这些结果跨不同数据集与指标反复出现，指向同一结论：当前评测可能系统性高估了模型能力。

评测设置本身的缺陷被认为是高估的来源之一。现有评估设置过度简化或不一致，未反映真实生物系统的复杂性，常用设置下性能被高估，严格条件下性能显著下降，且不同指标导致模型排名差异显著 [37]。**系统性变异**——扰动与对照细胞间由选择偏差或混杂因素造成的一致转录差异——被量化于十个数据集、三种技术、五种细胞系，常见指标对此类偏差敏感并导致性能高估，当前方法难以泛化超越系统性变异 [24]。数据泄漏是另一条通道：单细胞数据中同克隆、同患者或同批次细胞共享标签，细胞级随机划分会把测试细胞的"亲属"放入训练集，模型可靠记忆而非学习可迁移规则；暴露度决定泄漏通道，可检索性决定分数膨胀，患者队列中泄漏足以推翻临床结论 [38]。此外，现有Perturb-Seq基准数据集扰动特异性方差低，本身不适合评估此类模型 [36]。

泛化边界在不同任务上表现出结构性差异。药物盲设置下，模型通常能做癌症盲预测，但药物盲性能显著下降甚至完全失败，单药癌症药物盲响应预测主要限于同类内泛化 [39]。跨细胞类型迁移中，源-目标转录组距离越大准确率越低；扰动效应幅度强烈影响泛化与双扰动预测 [40]。预训练规模的作用同样受限：用2220万细胞预训练400个模型并开展6400次实验，性能在数据规模远小于现有语料时即达平台期，**无明确数据缩放定律**，提示应平衡模型容量、数据规模与算力而非盲目扩大 [10]。这些发现共同表明，泛化失败并非单一模型缺陷，而是与任务结构、数据构成和评测设计交织。

针对上述问题，社区从基准框架与因果效度两个方向回应。标准化模块化基准框架在未见细胞情境、未见扰动和跨数据集泛化等场景下评估多种模型，发现模型性能高度依赖情境，严格条件下鲁棒性有限 [37]；scArchon基于Snakemake构建可复现、模块化平台，标准化评估九种工具并提供容器化流程，但仅限非遗传扰动，基因敲除未纳入 [41]；ASSAYBENCH基于1920个公开CRISPR筛选、五类细胞表型，将筛选预测建模为基因排序任务并引入调整nDCG指标，发现零样本通用LLM优于生物学专用LLM和可训练基线，现有方法远未达经验性能上限 [42]。因果层面，单细胞CRISPR筛选的因果效应估计需附加因果假设，且仅能识别一个基因敲低对另一基因的效应，无法直接推断两基因间因果效应 [43]。更早的Perturb-seq表型流形工作则通过高维单细胞表型实现通路无偏排序与遗传互作分类，但其依赖生长表型挖掘的强互作，覆盖有限 [44]。

面向未来，评测设计正转向更严苛的泛化设定。2026年虚拟细胞挑战赛提出跨多个独立细胞情境的零样本预测，参赛者需在Arc生成的新数据集上预测未见细胞系中的基因敲低响应，目标是检验最优模型能否缩小临床前实验预测与人类生物学之间的差距 [11]。与此同时，VCBench指出多尺度整合和计算机模拟实验作为端到端任务结构上不可测试，且无基础模型发布完整细胞级训练清单，数据污染对用户不可检测 [25]。综合来看，当前证据支持一个审慎判断：在评测设置未充分控制系统性变异、数据泄漏与任务结构差异之前，虚拟细胞模型的性能声明应被视为高度情境依赖，而非可迁移的生物学能力。

## 5 产业动态

（本节暂无入库证据）

## 6 空白与趋势

综合上述证据，该方向的演化脉络可概括为三条并行的主线：**从潜空间扰动向量到大规模生成式基础模型**、**从静态端点预测到动态轨迹与世界模型**、**从单一数据集评测到跨情境泛化基准**。早期 scGen 以潜空间加减扰动向量奠定范式 [1]，随后 scGPT 以 3300 万细胞预训练把路线推向基础模型 [2]，而 Tahoe-x1、X-Cell、Speciesformer 等把参数、数据与模态进一步扩张 [4][5][13]。与之并行，Chreode 与 VCWM 分别以一步式状态转移和"建模细胞系统本身"的框架，把目标从任务端点推向可迭代的细胞世界模型 [18][19]。第三条主线则由 Systema、scArchon、ASSAYBENCH、虚拟细胞挑战赛等基准工作构成，把评测从"能否拟合"推向"能否泛化" [24][41][42][11]。

**核心问题可归结为三组张力**：其一，**模型复杂度与性能的匹配关系尚未确立**——OCOO-T 的极简流匹配与知识图谱 KNN 的"简单却有效"分别在不同基准上报告优势，而 X-Cell、Tahoe-x1 等大规模多模态模型亦各自报告最先进性能，二者缺乏统一评测 [8][7][5][4]。其二，**监督信号的来源与质量成为共同瓶颈**——SCALE 强调端点监督直接 delta 对齐、无需辅助目标，D²R² 依赖推断的 GRN 质量进行排序，scKITE 依赖注释与 GRN 推断质量，先验质量直接决定外推上限 [14][15][6]。其三，**评测效度受到系统性挑战**——多项独立工作一致发现简单基线常匹配或超越复杂基础模型，系统性变异、数据泄漏与任务结构差异被识别为高估来源 [9][36][24][25][38]。

基于上述证据，可识别以下趋势与空白：

1. **趋势：从"预测端点"转向"建模状态转移与世界模型"。** Chreode 以结构化残差转移算子实现一步式状态转移预测，把分布演化从推理时移至训练时 [18]；VCWM 框架进一步主张虚拟细胞应支持动作条件仿真、反事实推理与长程规划，使干预在演化状态中传播而非仅优化特定任务端点 [19]。**空白在于：尚无工作在同一基准上直接对照"单步预测精度"与"多步推演能力"**，Chreode 明确仅做预测建模、不声称具备规划能力，VCWM 则未报告定量结果与实验验证 [18][19]。

2. **趋势：闭环智能体开始处理"预测失败后的归因与修订"。** CellScientist 将高层假设空间与低层可执行实现空间耦合，把执行偏差路由回相应层级，案例中 PCC 由 0.3416 提升至 0.4368，并产生可审计的精炼轨迹 [20]。**空白在于：闭环精炼与单步预测模型之间缺乏直接对照**，且该框架依赖 LLM 代理、长程工作流仍脆弱 [20]。

3. **趋势：扰动数据资源向原代细胞、体内组织与空间维度延伸。** 探针式 perturb-seq 覆盖 2200 万原代人 CD4+T 细胞并测量静息与刺激后效应 [32]；iGOF-Perturb-seq 在体内星形胶质细胞中构建约 1000 个转录因子图谱 [33]；SPAC-seq 把扰动与空间表型关联 [34]。**空白在于：这些体系在物种、细胞类型与读出维度上各不相同，其结论的适用范围受限，且尚无跨体系的可比性评估**。

4. **趋势：评测从单一数据集走向跨情境零样本泛化。** 2026 年虚拟细胞挑战赛要求参赛者在 Arc 新数据集上预测未见细胞系中的基因敲低响应 [11]；ASSAYBENCH 基于 1920 个公开 CRISPR 筛选、五类细胞表型，发现零样本通用 LLM 优于生物学专用 LLM 和可训练基线 [42]。**空白在于：VCBench 指出多尺度整合和计算机模拟实验作为端到端任务结构上不可测试，且无基础模型发布完整细胞级训练清单，数据污染对用户不可检测** [25]。

5. **空白：因果效度与可解释性尚未与预测性能打通。** 单细胞 CRISPR 筛选的因果效应估计需附加因果假设，且仅能识别一个基因敲低对另一基因的效应，无法直接推断两基因间因果效应 [43]；scDEFT 明确将归因结果标为待实验验证的假设 [29]；D-SPIN 亦未提外推验证范围 [16]。**目前尚无工作把因果假设检验与扰动响应预测的泛化评估统一在同一框架内。**

6. **空白：预训练规模的作用边界缺乏系统刻画。** 一项研究用 2220 万细胞预训练 400 个模型并开展 6400 次实验，发现性能在数据规模远小于现有语料时即达平台期，**无明确数据缩放定律** [10]；scKITE 则显示知识增强训练带来平均 28.8% 相对提升，仅用 179,067 个预训练样本即超越 Geneformer、scGPT 等 [6]。**两条证据指向同一空白：数据规模、知识注入与模型容量之间的权衡关系尚未被系统建模，盲目扩大语料的收益边界不明。**

7. **空白：药物盲与跨类泛化的结构性失败尚未被有效回应。** 单药癌症药物盲响应预测主要限于同类内泛化，药物盲性能显著下降甚至完全失败 [39]；跨细胞类型迁移中源-目标转录组距离越大准确率越低，扰动效应幅度强烈影响泛化与双扰动预测 [40]。**目前尚无工作提出可跨药物类别或跨细胞类型稳定外推的架构或训练策略。**

## 7 未归类新证据

人工智能虚拟细胞（AIVC）被提出作为整合多组学数据、贯通微观分子机制与宏观组织行为的研究新范式，其核心思路是通过跨尺度表征工程、功能子模块设计与多组件动态调控机制三方面构建统一技术框架 [12]。该综述系统梳理了现有模型与数据集资源，列举了 **GeneCompass**、**Tahoe-100M** 等代表性资源，并指出传统实验与生化分析受限于时空分辨率与处理能力，难以刻画动态跨尺度生物事件 [12]。

作者同时指出，AIVC 仍处于早期阶段，**数据异质性**与**模型可解释性**等挑战尚未解决 [12]。该证据为综述性工作，汇总现有模型与数据集而未自行分析样本，因此未提供可供比较的实验对照或定量性能指标 [12]。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 扰动响应生成模型 | 朝阳 | 方法谱系从 [1]（scGen，潜空间加性扰动向量）一路演化到 [2]（scGPT，多组学基础模型），再到 [3]（State，跨上下文扰动响应）与 [5]（X-Cell，因果扰动预测的规模化），说明**建模范式仍在快速换代、尚未收敛**；同时新工作（State、X-Cell）引用数极低（9、7），表明这是**近两年刚爆发、尚无定论**的赛道，而非增量成熟期。 |
| 2.2 细胞世界模型与闭环智能体 | 萌芽 | 雷达样本中仅 3 篇且全部落在 2026 年：[18]（Chreode，一步式时序动力学与扰动预测的细胞世界模型）与 [19]（虚拟细胞的世界模型）提出框架性概念，[20]（CellScientist，双空间分层编排的闭环精化）尝试闭环智能体，但**彼此方法不共享、无统一评测、无大规模验证**，属于少量探索性工作。 |
| 3 数据与资源 | 朝阳 | 从 [22]（全基因组 Perturb-seq 图谱，749 引用）到 [35]（Virtual Cell Challenge，把虚拟细胞变成 Turing test 式竞赛），数据规模与评测基础设施在**近两年集中落地**；[34]（空间分辨功能基因组学 + CRISPR 筛选测序）与 [33]（体内 gain-of-function 映射转录因子功能）进一步把扰动数据推向**空间与体内维度**，说明资源仍在扩张而非饱和。 |
| 4 评测与效度批判 | 朝阳 | [9]（深度学习基因扰动效应预测**尚未跑赢简单基线**，179 引用）与 [36]（基础细胞模型在后扰动 RNA-seq 预测上的基准测试）构成对当前模型的直接证伪性证据；[24]（Systema，超越表达谱的遗传扰动响应评测框架）与 [44]（从单细胞表型构建遗传互作流形）则提供更严格的评测与效度工具。**批判与基准同步爆发**，是该方向从"能跑"走向"可信"的关键期。 |
| 5 产业动态 | 证据不足 | 雷达样本中该节 **n=0**，无任何可核验技术细节的产业发布证据，无法判断阶段。 |

**整体判断**：这个方向整体处于**朝阳期**，且是"模型爆发 + 批判同步爆发"的双高态势——雷达样本中近两年占比 **0.91**、CNS 占比 **0.43**，但 2.1 节新方法引用数普遍为个位数（State 9、X-Cell 7），说明**方法远未收敛**。窗口期估计还有 **12–24 个月**：一旦 Virtual Cell Challenge 类基准（[35]）跑出稳定领先且能复现的赢家，赛道会迅速从"拼新架构"转向"拼数据与评测"，届时纯方法论文的边际收益会骤降。**最大的不确定性**是效度问题：[9] 已明确显示深度学习扰动预测**尚未跑赢简单基线**，如果这一结论在更大规模、更多上下文下持续成立，那么当前大量生成式扰动模型的科学价值会被重估——**"预测得准"与"预测得有用"之间的鸿沟，是这个方向最可能翻车的地方**。

**接下来怎么做**：

1. **用类器官 + 多组学做"跨上下文泛化"的扰动预测，而不是再刷一个细胞系基准**。切入点：以类器官扰动数据（CRISPR / 药物）为测试床，方法上采用 [3]（State）或 [5]（X-Cell）的跨上下文设定，产出"在未见细胞上下文下扰动响应预测"的评测结果。为什么现在做：现有模型几乎都在细胞系上验证，类器官是**上下文迁移的天然压力测试**，而 [9] 已证明简单基线在标准基准上就能打平深度模型，**换一个更难、更贴近生理的上下文，正是差异化窗口**。

2. **把"没跑赢基线"当成研究起点，做效度批判 + 可复现基准**。切入点：复现 [9] 的结论，在 [35]（Virtual Cell Challenge）的数据划分上系统比较基础模型 vs. 简单基线，并引入 [24]（Systema）的超越表达谱评测维度。产出：一份可复现的基准报告 + 代码。为什么现在做：批判性证据刚出现（2025–2026），**领域还没有公认的"正确评测协议"**，此时进入门槛低、影响力大，且与你博后的生信算法背景高度匹配。

3. **切入"细胞世界模型"的时序动力学，做一步式 / 少步式预测**。切入点：参考 [18]（Chreode，一步式时序动力学与扰动预测）的思路，用公共 Perturb-seq 时序数据（如 [22] 的图谱）训练 flow matching 或扩散式动力学模型，产出"扰动后轨迹预测"而非单点预测。为什么现在做：2.2 节仅 3 篇、全在 2026 年，**框架刚提出、无统一实现**，是典型的"早进入者定义问题"阶段；且时序预测比单点预测更接近"细胞世界模型"的本意。

4. **把空间维度接进来，做空间分辨的扰动响应预测**。切入点：利用 [34]（空间分辨功能基因组学 + CRISPR 筛选测序）与 [33]（体内 gain-of-function 转录因子映射）这类数据，把空间邻域信息作为扰动响应的条件变量，方法上可嫁接 [2]（scGPT）的多组学编码器。为什么现在做：空间扰动数据刚出现（2026），**几乎没有人做过空间条件下的扰动响应预测**，而你的多模态建模背景正好是入场券。

5. **用公共数据做闭环智能体的最小 demo，验证"预测—实验—再预测"循环**。切入点：以 [20]（CellScientist，闭环精化）为架构参考，在 [35]（Virtual Cell Challenge）的公开数据上搭建一个"预测 → 选扰动 → 用留出数据模拟实验 → 更新模型"的闭环 demo，产出可运行代码与循环增益曲线。为什么现在做：闭环智能体在雷达样本中仅 1 篇且无代码，**"有框架无实现"是最大的空白**；同时这类 demo 可以直接对接你的类器官合作项目，把公共数据验证过的循环迁移到真实湿实验。

## 参考文献

1. scGen predicts single-cell perturbation responses. Nature Methods 2019. https://doi.org/10.1038/s41592-019-0494-8
2. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. Nature Methods 2024. https://doi.org/10.1038/s41592-024-02201-0
3. Predicting cellular responses to perturbation across diverse contexts with State. Cell 2026. https://doi.org/10.1016/j.cell.2026.07.052
4. Tahoe-x1: Scaling Perturbation-Trained Single-Cell Foundation Models to 3 Billion Parameters. bioRxiv 2025. https://doi.org/10.1101/2025.10.23.683759
5. X-Cell: Scaling Causal Perturbation Prediction Across Diverse Cellular Contexts via Diffusion Language Models.  2026. https://doi.org/10.64898/2026.03.18.712807
6. Towards a knowledge-enhanced single-cell foundation model.  2026. https://arxiv.org/abs/2609.14970
7. Knowledge Graphs and Reasoning LLMs for Finding Simple Yet Effective Transcriptomic Perturbation Predictors.  2026. https://arxiv.org/abs/2606.08816v1
8. OCOO-T : A Simple and Scalable Virtual Cell Model for Transcriptional Perturbation Response Prediction.  2026. https://arxiv.org/abs/2606.12838v2
9. Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines. Nature methods 2025. https://doi.org/10.1038/s41592-025-02772-6
10. Evaluating the role of pretraining dataset size and diversity on single-cell foundation model performance.. Nature methods 2026. https://doi.org/10.1038/s41592-026-03120-y
11. Virtual Cell Challenge 2026: Benchmarking zero-shot generalization across cellular contexts.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.004
12. Artificial intelligence-enabled multi-scale virtual cell: perspective, challenges, and opportunities.. Briefings in bioinformatics 2026. https://doi.org/10.1093/bib/bbag104
13. Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling.  . https://doi.org/10.64898/2026.09.22.752128
14. SCALE:Scalable Conditional Atlas-Level Endpoint transport for virtual cell perturbation prediction.  2026. https://arxiv.org/abs/2603.17380v3
15. $D^{2}R^{2}$: Discrete Diffusion with Regulation Reinforcement for Single-Cell Perturbation Prediction.  2026. https://arxiv.org/abs/2608.15288v1
16. D-SPIN constructs regulatory network models from scRNA-seq that reveal organizing principles of perturbation response.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.028
17. A transcription factor regulatory atlas for activity inference and perturbation prediction. Nucleic Acids Research 2026. https://doi.org/10.1093/nar/gkag897
18. Chreode: A Cell World Model for One-Step Temporal Dynamics and Perturbation Prediction.  2026. https://arxiv.org/abs/2605.28111v1
19. A world model of the virtual cell.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.042
20. CellScientist: Dual-Space Hierarchical Orchestration for Closed-Loop Refinement of Virtual Cell Models.  2026. https://arxiv.org/abs/2605.07335v1
21. Tahoe-100M: Mapping drug-induced molecular phenotypes at single-cell resolution.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.035
22. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. bioRxiv 2021. https://doi.org/10.1016/j.cell.2022.05.013
23. An operational perturbation proteomics-based virtual cell model.. Nature 2026. https://doi.org/10.1038/s41586-026-11001-9
24. Systema: a framework for evaluating genetic perturbation response prediction beyond systematic variation. Nature biotechnology 2026. https://doi.org/10.1038/s41587-025-02777-8
25. VCBench: A Multi-Dimensional Benchmark for Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.06.18.733146
26. scBalFlow: A Staged Flow Matching Framework for Imbalanced Single-Cell Drug Perturbation Prediction.. Bioinformatics (Oxford, England) 2026. https://doi.org/10.1093/bioinformatics/btag682
27. Predicting how perturbations reshape cellular trajectories with PerturbGen.  2026. https://doi.org/10.64898/2026.03.04.709254
28. RegVelo: Gene-regulatory-informed dynamics of single cells.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.022
29. scDEFT: A deep learning framework for drug-effect prediction and counterfactual reasoning.  2026. https://arxiv.org/abs/2609.10831
30. UniPert-G2CP bridges genetic and chemical screens from molecular representation to phenotype modeling.. Cell 2026. https://doi.org/10.1016/j.cell.2026.06.005
31. CellFluxRL: Biologically-Constrained Virtual Cell Modeling via Reinforcement Learning.  2026. https://arxiv.org/abs/2603.21743v4
32. Genome-scale perturb-seq in primary human CD4&lt;sup&gt;+&lt;/sup&gt; T cells maps context-specific regulators of T cell programs and human immune traits.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.002
33. Mapping transcription factor functions in astrocytes using in vivo gain-of-function Perturb-seq.. Science (New York, N.Y.) 2026. https://doi.org/10.1126/science.adw2156
34. Uncovering spatially resolved functional genomics with CRISPR screen sequencing.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.049
35. Virtual Cell Challenge: Toward a Turing test for the virtual cell. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.008
36. Benchmarking foundation cell models for post-perturbation RNA-seq prediction. BMC genomics 2025. https://doi.org/10.1186/s12864-025-11600-2
37. Benchmarking virtual cell models for in-the-wild perturbation response.  2026. https://arxiv.org/abs/2604.27646v1
38. Cell-level random splits leak group-owned answers in single-cell benchmarks. bioRxiv 2026. https://doi.org/10.64898/2026.09.09.750484
39. Monotherapy cancer drug-blind response prediction is limited to intraclass generalization.. PLoS computational biology 2026. https://doi.org/10.1371/journal.pcbi.1013232
40. A systematic comparison of single-cell perturbation response prediction models.. Science advances 2026. https://doi.org/10.1126/sciadv.aed3414
41. scArchon: a scalable benchmarking framework for assessing single-cell perturbation models.. Genome biology 2026. https://doi.org/10.1186/s13059-026-04104-z
42. AssayBench: An Assay-Level Virtual Cell Benchmark for LLMs and Agents.  2026. https://arxiv.org/abs/2605.10876v1
43. Causal effect estimation from trans-regulatory single-cell CRISPR screens.. Cell genomics 2026. https://doi.org/10.1016/j.xgen.2026.101251
44. Exploring genetic interaction manifolds constructed from rich single-cell phenotypes. Science 2019. https://doi.org/10.1126/science.aax4438
