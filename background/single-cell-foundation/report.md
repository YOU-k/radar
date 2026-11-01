# 单细胞与空间组学基础模型与虚拟细胞 · 方向背景报告

证据 100 篇 · 覆盖度 0.65 · 第 11 轮 · 更新 2026-11-01 · 数字核验删句 2

## 本次变更

- 新增 [11] Benchmarking segmentation methods for spatial transcriptomics.
- 新增 [55] ProtCell: a foundation model for single-cell proteomics
- 新增 [78] Advancing morphological profiling with self-supervised learning through comparative insights into representation learning of cellular perturbations.

## 摘要（TL;DR）

- scGPT 在超 3300 万个细胞上预训练，迁移学习后在注释、整合、扰动预测、基因网络推断等任务上表现优异 [1]；Geneformer 在约 3000 万个单细胞转录组上以自监督方式学习网络动力学，微调后在染色质与网络动力学任务中持续提升准确率 [2]。
- CellFM 在 1 亿人类细胞上预训练，在多种单细胞任务上达到或超过 Geneformer、scGPT、scFoundation、UCE 等基础模型 [3]；但一项系统研究用 2220 万细胞语料预训练 400 个模型、开展 6400 次实验后发现性能在数据规模远小于当前训练语料时就趋于平台，未观察到明确的数据缩放定律 [4]。
- 对 Geneformer 和 scGPT 在 5 个多样数据集上的评测显示，二者在 AvgBIO 上多数低于 HVG、Harmony、scVI 等简单基线，HVG 在所有指标上优于二者 [5]。
- 逐层分析发现「默认取最终层嵌入」并不最优：在 scFoundation（100M）与 Tahoe-X1（1.3B）上，轨迹推断的最优层位于 60% 深度、比最终层高 31%，扰动预测的最优层随 T 细胞激活状态在 0–96% 间漂移 [6]。
- TranscriptFormer 在多达 1.12 亿细胞、12 个物种、跨越 15.3 亿年进化的数据上联合建模基因身份与表达水平，在分布内与分布外细胞类型分类上达 SOTA [7]；LucaCell 在 8500 万人类和小鼠单细胞上预训练，实现人、小鼠、狐猴肾脏数据的跨物种跨模态细胞类型迁移 [8]。
- CellWorld 主张重建被掩码的基因身份或表达值会鼓励复现测定特异的技术变异，因而把预测目标改为潜在细胞表征（JEPA 式），其 CellWorld-Small（5.74M）在全部 11 个线性探针和 7 个空间基准上超越所有基线 [9]。
- 对四种亚细胞分辨率平台在三种人肿瘤连续切片上的系统评测发现各平台在灵敏度、特异性、扩散控制、细胞分割、注释、空间聚类及转录本-蛋白对齐上差异显著，结论受限于仅 3 种肿瘤、4 个平台 [10]；细胞分割基准在 5 种空间转录组技术、15 个数据集、12 种人鼠组织上比较，分割质量、转录本回收、细胞组成、形态、表达纯度和空间组织均存在显著差异 [11]。
- 对 Tahoe-x1 做跨模态继续预训练，仅用 70M 参数、在 48,843 个蛋白质组样本上训练一个 epoch，就在多数原评测基准上匹配或超过 1B 和 3B 参数的 RNA-only 模型 [12]；而 Tahoe-x1 将扰动训练的单细胞基础模型扩展到最高 30 亿参数，在四项基准上达 SOTA [13]。
- 因果电路追踪在 Geneformer V2-316M 与 scGPT 上跨 4 条件得到 96,892 条边、80,191 次前向传播，两模型均表现约 53% 生物一致性与 65–89% 抑制主导，但 CRISPRi 基因级验证的方向准确率仅 56.4%，提示模型编码的是共表达而非因果调控 [14]。
- 在扰动后表达预测上，四个 Perturb-seq 数据集的差分空间里 Train Mean 基线（0.711/0.557/0.373/0.628）优于 scGPT（0.641/0.554/0.327/0.596）与 scFoundation（0.552/0.459/0.269/0.471），而随机森林加 GO 特征最佳（0.739/0.586/0.480/0.648）[15]；但有研究提出阳性对照基线与指标校准框架，发现 MSE 和 Pearson Δ 等常用指标常校准不良，在良好校准指标下深度学习扰动模型可优于无信息基线 [16]。
- 已发表肝脏 AIVC 模型仅展示了图谱整合、轨迹推断、可迁移表示、回顾性响应程序等单个组件，尚无前瞻验证的肝脏模拟器 [17]；单细胞与空间图谱只说明细胞状态出现在何处，本身不能预测肝损伤是否进展 [17]。

## 1 背景与定义

单细胞与空间组学基础模型的方向边界，首先由「预训练—迁移」这一范式划定：把细胞类比为句子、基因类比为词元，在大规模单细胞数据上自监督预训练，再将表征迁移到注释、整合、扰动预测等下游任务 [18]。scGPT 在超 3300 万个细胞上预训练 [1]，Geneformer 在约 3000 万个单细胞转录组上学习网络动力学 [2]，构成了这一方向的早期锚点。与之并行的是「虚拟细胞」目标：AI 虚拟细胞（AIVC）愿景主张构建多尺度、多模态大神经网络，从数据直接学习细胞行为而无需显式规则，并提出预测、生成、可查询三类能力 [19]；Human Cell Atlas 相关工作则把细胞图谱的终点指向统一基础模型 [20]。**因此本方向的边界不是「用深度学习分析单细胞数据」，而是以大规模预训练表征为核心资产、以扰动响应预测与细胞状态生成为核心任务、以跨模态与跨情境迁移为核心评价维度的一整套模型—数据—基准体系。**

演化脉络上，这一方向经历了三次重心转移。第一次是从「图谱表征」转向「扰动预测」：早期工作以注释、整合、细胞检索为主（SCimilarity 在 2270 万细胞上做跨组织细胞搜索 [21]，后续扩展到 2340 万细胞、412 项研究 [22]），随后 Perturb-seq 类数据把目标推向「给定扰动预测状态变化」，基因组规模 Perturb-seq 在 K562 与 RPE1 中敲低数千个扰动、覆盖超过 250 万个细胞 [23]，Tahoe-100M 则以超过 1 亿细胞、50 个细胞系、379 种化合物支撑药物扰动建模 [24]。第二次是从「转录组单模态」转向「多模态」：PAST 联合编码病理图像与单细胞转录组 [25]，OmiCLIP 对齐图像与基因句子 [26]，mSTAR 整合切片、报告与基因表达 [27]，MultiVI 与 CLM-X 处理 RNA-ATAC-蛋白的模态缺失与联合表征 [28] [29]。第三次是从「模型规模竞赛」转向「机制审计与可信度」：SAE 特征图谱、因果电路追踪、预训练污染审计与简单基线挑战，构成了近两年最密集的证据增量 [30] [14] [31] [15]。

核心问题可以归纳为四组张力。**其一是规模与收益的张力**：CellFM 在 1 亿人类细胞上预训练并达到或超过多个基础模型 [3]，但用 2220 万细胞预训练 400 个模型、开展 6400 次实验的系统研究发现性能在远小于当前语料时就趋于平台，未观察到明确的数据缩放定律 [4]。**其二是基础模型与简单基线的张力**：零样本评测中 HVG 在全部指标上优于 Geneformer 与 scGPT [5]，扰动后表达预测中 Train Mean 基线优于两个基础模型 [15]，无参数线性流程在多个基准取得 SOTA 或近 SOTA [32]；但指标校准研究指出 MSE、Pearson Δ 等常用指标校准不良，在良好校准指标下深度学习扰动模型可优于无信息基线 [16]。**其三是表征内容与调控逻辑的张力**：SAE 分析显示模型内化了有组织的生物学知识，但仅 6.2% 转录因子显示调控靶标特异性 [30]；因果电路追踪给出约 53% 生物一致性与 65–89% 抑制主导，而 CRISPRi 验证方向准确率仅 56.4% [14]；系统评估则发现基因级基线 AUROC 0.81–0.88 优于注意力边的 0.70 [33]。**其四是分布内成绩与分布外泛化的张力**：可信虚拟细胞路线图明确指出静态图谱、仅转录组读出与分布内基准不足以预测新条件下的细胞行为，评估应转向泛化到未见细胞类型与扰动 [34]；预训练污染审计则显示两个高引用基准存在大量预训练重叠证据，截断后数据集重叠为 0% [31]。

在任务层面，「虚拟细胞」已被拆成若干可分别评测的子问题，而非单一模型能力。扰动响应预测分化出条件生成/传输路线（PRnet [35]、SCALE [36]、STRAND [37]）与基础模型微调路线（药物条件适配器仅调不到 1% 参数 [38]、Tahoe-x1 扩到最高 30 亿参数 [13]），而跨模态继续预训练仅用 70M 参数即在多数原评测基准上匹配或超过 1B/3B 的 RNA-only 模型 [12]，说明**「规模—模态—任务」三者的最优组合远未收敛**。细胞状态生成则分化为表达插补与反事实推理 [39]、扩散后训练 [40]、潜在传输 [36] 与一步式世界模型 [41] 等不同生成机制。多模态整合的核心问题被明确为「用多模态补单模态」：MultiVI 强调校准的不确定性估计与缺失模态差异表达 [28]，CLM-X 强调统一架构下的跨模态翻译 [29]。空间方向则出现预训练目标本身的分歧：多数模型重建被掩码的基因身份或表达值，CellWorld 主张这会复现测定特异的技术变异，改以潜在细胞表征为预测目标 [9]；NexuST 选择基因级与细胞级建模反复交错 [42]；VINTER 把图像、表达与邻域作为单一序列读入生成式视觉语言模型 [43]。

评测与数据基础构成了这一方向的「元问题」，也是当前最活跃的争议场。基准层面，Virtual Cell Challenge 提供开放循环评估框架与专用扰动数据集 [44]；scContam 把预训练污染从隐性假设变成可审计对象 [31]；指标校准工作则反过来质疑负面结论的可靠性 [16]。任务依赖性被多项评测反复确认：七种基础模型与三种经典表示的低监督比较中，仅扰动预测有 6/7 个基础模型超过基线，而重建任务为 0/7 [45]；零样本评估中注释任务基线多数数据集最强，蛋白表达预测则基础模型更准 [46]；细胞类型分类专项评测中 scFoundation 持续最佳而 Geneformer 甚至不如基线 [47]。数据侧的共同瓶颈同样明确：扰动数据集仅覆盖数百分子与少数细胞系 [38]，跨细胞类型与组合扰动泛化仍受限 [48]，组合扰动实验规模本身有限 [49]；空间平台的灵敏度、分割与注释差异显著，跨研究数字不宜直接横向比较 [10] [11]。**由此，本方向的「基础」不仅是模型与数据，还包括一套尚未统一的评估协议：同一模型在不同指标、不同平台、不同污染状态下可以得出相反结论，这正是当前证据格局的基本特征。**

## 2 方法学


### 2.1 单细胞基础模型

单细胞基础模型的主流路线，是用 Transformer 在千万至亿级细胞转录组上做自监督预训练，再把学到的表征迁移到注释、整合、扰动预测等下游任务。**scGPT** 在超 **3300 万个细胞**上预训练，迁移学习后在注释、整合、扰动预测、基因网络推断等任务上表现优异 [1]；**Geneformer** 在约 **3000 万个单细胞转录组**上以自监督方式学习网络动力学，微调后在染色质与网络动力学任务中持续提升准确率，并在有限患者数据下识别出心肌病候选治疗靶点 [2]。综述把这一范式的共同逻辑概括为「细胞类比句子、基因类比词元」，通过大规模自监督学习通用表征再适配下游任务 [18]。不过该综述也指出，早期嵌入模型与基础模型在实验生物学家中应用仍然有限，而大规模图谱的积累使「用 AI 在庞大数据背景下解读新数据集」的需求变得明确 [50]。

预训练规模是否越大越好，出现了明确分歧。CellFM 收集并标准化公共 scRNA-seq 数据，在 **1 亿人类细胞**上预训练，在多种单细胞任务上达到或超过 Geneformer、scGPT、scFoundation、UCE 等基础模型 [3]；scPRINT-2 进一步把预训练扩到 **3.5 亿细胞、16 个物种**，在表达去噪、细胞嵌入和细胞类型预测上达到 SOTA，并具备表达插补与反事实推理的生成能力 [39]。但一项系统研究用 **2220 万细胞**语料预训练 **400 个模型**、开展 **6400 次实验**后发现，性能在数据规模远小于当前训练语料时就趋于平台，**未观察到明确的数据缩放定律**，因而建议平衡模型容量、数据规模与算力 [4]。这意味着「堆数据」的收益并非线性，与上述亿级模型的规模叙事构成张力。

更尖锐的质疑来自零样本评估。对 Geneformer 和 scGPT 在 5 个多样数据集上的评测显示，二者在 AvgBIO 上多数低于 HVG、Harmony、scVI 等简单基线，HVG 在所有指标上优于二者，scGPT 仅在 PBMC 12k 上部分优于 scVI/Harmony [5]。作者强调零样本评估对无法微调的发现型应用至关重要，并指出预训练与评估数据存在部分重叠的问题 [5]。与之呼应，逐层分析发现「默认取最终层嵌入」的做法并不最优：在 scFoundation（100M）与 Tahoe-X1（1.3B）上，轨迹推断的最优层位于 **60% 深度**、比最终层高 **31%**，扰动预测的最优层随 T 细胞激活状态在 **0–96%** 间漂移，静息细胞反而是首层最佳 [6]。该工作自限为两个模型、两类任务，但足以说明表征质量高度依赖任务与细胞情境。

架构层面的改进沿着两条线展开。一条是引入生物学先验：RegFormer 融合基因调控网络与 Mamba 状态空间建模，在 **2500 万人类细胞**上预训练，在细胞注释、GRN 重建、遗传扰动预测和药物响应建模等基准上持续优于 scGPT 和 Geneformer [51]；scDifformer 采用掩码语言模型预训练、扩散驱动后训练与下游微调的三阶段设计，扩散模块在强批次效应下持续提升跨数据集性能，并在 7 个组织与多项独立研究中改善注释与空间转录组 spot 去卷积 [40]。另一条是质疑「必须重训练」本身：GenePT 直接用 GPT-3.5 基于 NCBI 基因文本描述生成基因嵌入，无需数据策展与额外预训练，在基因属性与细胞类型分类等任务上达到与 Geneformer 等相当甚至更优的性能 [52]。这两条线对「预训练投入是否必要」给出了相反方向的回答。

跨物种与跨模态是近期扩张最快的子问题。TranscriptFormer 在多达 **1.12 亿细胞、12 个物种、跨越 15.3 亿年进化**的数据上联合建模基因身份与表达水平，在分布内与分布外细胞类型分类上达 SOTA，可零样本识别疾病状态并跨物种转移注释，发育轨迹与系统发育关系自然涌现 [7]。Speciesformer 在含 **1.31 亿细胞**的 SpeciesCorpus 上预训练，目标是把进化表征学习与虚拟细胞状态生成结合，区分保守生物学原理与物种、组织及细胞环境特异变异，但仅提供摘要信息、缺少定量基准结果 [53]。LucaCell 走「以序列为中心」的路线，用预训练 mRNA 序列嵌入表示基因而非固定基因注释，在 **8500 万人类和小鼠单细胞**上预训练，实现人、小鼠、狐猴肾脏数据的跨物种跨模态细胞类型迁移，并区分 **50 多种细菌**且保留种内结构 [8]。EpiZoo 则把这一思路推进到表观基因组，将百万维单细胞表观基因组谱转换为紧凑「细胞句子」，以克服现有模型依赖基因组坐标、局限于单一物种的问题 [54]。

除转录组外，蛋白与蛋白修饰层面也出现了专门的基础模型。ProtCell 基于 **98 个数据集约 3.8 亿细胞**预训练，在 transformer 编码器中结合蛋白身份嵌入与连续丰度嵌入，通过掩码丰度建模学习细胞级与蛋白级表征，可连接碎片化蛋白组谱实现可迁移注释和批次校正，并扩展有限面板推断未测量的细胞毒性蛋白程序 [55]。PTM-Mamba 面向翻译后修饰，用双向门控 Mamba 块融合 ESM-2 与 PTM 嵌入，以 **79,707 条修饰序列**（源自 **311,350 条** Swiss-Prot PTM 记录）训练，收敛快于 PTM-Transformer 基线并能区分修饰与野生型序列 [56]。这些工作把「单细胞基础模型」的边界从转录组扩展到蛋白组与序列修饰层面，但各自的任务覆盖与验证范围仍相对局部。

在「虚拟细胞」这一目标下，检索与生成两种能力被分别强调。SCimilarity 用深度度量学习学习统一可解释的细胞表征，早期版本在 **2270 万细胞、399 项研究**上训练，实现跨组织细胞类型整合、注释与即时查询，并发现最初在间质性肺病中识别的巨噬细胞亚群也存在于其他纤维化疾病、组织和 3D 水凝胶系统中 [21]；后续版本报告 **2340 万细胞、412 项研究、56 训练/15 测试数据集**，在查询敏感性与整合性能间取得最佳平衡（**β=0.001**），但依赖 Cell Ontology 注释质量，部分细胞类型关系模糊 [22]。生成方向则以 scPRINT-2 的表达插补与反事实推理 [39]、scDifformer 的扩散后训练 [40] 和 TranscriptFormer 的可查询虚拟细胞图谱 [7] 为代表。与之互补的是样本级建模：MrVI 用层次深度生成模型与交叉注意力建模样本协变量效应，无需先验聚类即可识别样本分组，实现高分辨无注释差异表达与丰度分析并控制批次，整合性能优于常用方法，已在 scvi-tools 中提供 [57]。

综合来看，这一领域的争议集中在三点：预训练规模是否带来可预期的收益（亿级模型的性能主张 [3] 与「无清晰缩放定律」的系统结论 [4] 并存）；基础模型相对简单基线是否真有优势（零样本评测给出否定性证据 [5]，而任务特定微调与架构改进报告持续领先 [51]）；以及「取最终层」等默认实践是否成立（逐层分析显示最优层随任务与细胞状态大幅漂移 [6]）。跨物种、跨模态与蛋白组方向的扩张 [7] [8] [55] 正在把评价标准从单一物种的注释准确率，推向可迁移性与生成能力，但多数新模型仍缺少公开的定量基准与权重，可比性有待建立。

### 2.2 空间与多模态模型

空间与多模态模型的第一条主线是把组织学图像与空间转录组配对，学习跨模态表征。**PAST** 在**2000万**配对病理图像与单细胞转录组上训练，联合编码细胞形态与基因表达，支持单细胞基因表达预测、虚拟分子染色和多模态生存分析，在多种癌症任务中超越现有方法 [25]。**OmiCLIP** 走的是双编码器对比学习路线，把转录组数据转成“基因句子”，基于 **ST-bank** 的 **220万** 组织 patch（**1007** 样本、**32** 器官）对齐图像与基因表示，配套 Loki 平台覆盖组织对齐、注释、细胞分解、检索与基因预测五类功能，并在对比 **22** 种 SOTA 方法时表现一致 [26]。**mSTAR** 则把模态扩展到三路——病理切片、专家报告与基因表达，用 **26,169** 切片-模态对、**10,275** 患者、**32** 癌种、**1.16亿** patch 做两阶段预训练，在 **15** 类 **97** 项任务中表现优异，并显示多模态预训练可用更少数据达到竞争性能 [27]。三者都依赖配对数据，OmiCLIP 明确把“依赖配对 WSI 与 Visium 数据、泛化待验证”列为局限 [26]，mSTAR 同样指出跨中心泛化仍需验证 [27]。

空间转录组基础模型的预训练目标本身出现了分歧。多数模型重建被掩码的基因身份或表达值，**CellWorld** 则主张这会鼓励复现测定特异的技术变异、限制表征迁移性，因而把预测目标改为潜在细胞表征（JEPA 式），用空间 Transformer 建模细胞交互 [9]。其预训练规模为 **4600万** 细胞、**3** 平台 **11** 器官、**4** 个模型变体（**5.74M–94.56M** 参数）；**CellWorld-Small（5.74M）** 在全部 **11** 个线性探针和 **7** 个空间基准上超越所有基线，仅用 **5%** 语料的冻结 Large 在 **7** 个空间基准上超越全部微调基线 [9]。该工作报告的迁移驱动因素也值得注意：空间迁移依赖生物来源多样性与充分优化，而非细胞数量 [9]。**NexuST** 提供另一种组织方式，反复交错基因级分子建模与细胞级空间建模，使两个层级在端到端预训练中相互优化，并构建 **HumanST-46M**（**72** 数据集、**11** 器官、三种成像平台、**4570万** 人类细胞），在四个留出数据集约 **260万** 细胞上于细胞类型注释、区域预测、基因恢复等任务达到 SOTA 或具竞争力 [42]。**VINTER** 则把组织学图像、实测基因表达和空间邻域作为单一序列读入生成式视觉语言模型，在 **145万** 组织学-文本对上对齐，因基因以文本形式输入而可在固定图像下编辑分子证据，联合三源信息后组织注释精度优于空间域方法和空间基础模型 [43]。

多模态单细胞整合模型处理的是另一类子问题：模态缺失与联合表征。**MultiVI** 用深度生成模型分别建模基因表达与染色质可及性，通过惩罚使两模态潜空间对齐，并模块化扩展至表面蛋白；其卖点是提供校准的不确定性估计、准确估计缺失模态的差异表达/可及性，以及在相关群体存在时实现样本外预测，局限是依赖相关群体的多模态信息 [28]。**CLM-X** 用多路 Transformer 与统一 token 化设计、分阶段掩码重建预训练，在百万级单模态与多模态数据上预训练，支持 RNA-only、ATAC-only 和配对 RNA-ATAC 输入，在 **5** 个下游任务和 **10** 个数据集上持续超越现有多模态方法与单模态基础模型，RNA-ATAC 跨模态翻译和扰动预测优势明显 [29]。两者都指向“用多模态补单模态”，但 MultiVI 强调概率模型的不确定性校准 [28]，CLM-X 强调统一架构下的跨模态翻译 [29]。

空间映射与对齐方面，**moscot** 把时序、空间、时空映射统一为 W、GW、FGW 型最优传输问题，支持多模态与图谱规模数据，在 **170万** 细胞小鼠胚胎等数据上实现高效对齐，计算时间与内存较既往 OT 工具降数个数量级，并实验验证 NEUROD2 调控 epsilon 细胞形成；其局限是依赖 OT 假设与先验知识、复杂映射仍需调参 [58]。

评测与数据基础方面的证据提示，上述模型的比较不能脱离平台与流程差异。对四种亚细胞分辨率平台（Stereo-seq v1.3、Visium HD FFPE、CosMx 6K、Xenium 5K）在三种人肿瘤连续切片上的系统评测，以 CODEX 蛋白和 scRNA-seq 作真值，发现各平台在灵敏度、特异性、扩散控制、细胞分割、注释、空间聚类及转录本-蛋白对齐上差异显著，结论受限于仅 **3** 种肿瘤、**4** 个平台 [10]。细胞分割本身也被系统基准：**11** 种图像、转录组与多模态方法在 **5** 种空间转录组技术、**15** 个数据集、**12** 种人鼠组织上比较，分割质量、转录本回收、细胞组成、形态、表达纯度和空间组织均存在显著差异 [11]。病理基础模型的临床基准则系统比较了 CTransPath、Phikon、UNI、Virchow 等模型的参数量、算法与训练数据，并指出数字病理数据缺乏与 WSI 算力需求是主要瓶颈 [59]。更早的图像侧基础是 **Cell Painting**：2013 年提出的显微细胞标记检测，经协议优化、特征提取改进与批次校正增强，可捕获细胞对扰动的响应并用于解析化合物作用机制与毒性，其进一步发展被认为需要计算与实验技术进步及多组学整合 [60]。这些评测共同说明，跨研究的性能数字不宜直接横向比高低，模型间的差异需放在同一平台、同一分割与同一真值设定下解读 [10][11]。

### 2.3 扰动响应与虚拟细胞

虚拟细胞的核心任务之一是预测细胞在遗传、化学或发育信号扰动下的状态变化。早期实验技术为这一方向奠定了数据基础：**Perturb-seq** 将单细胞RNA-seq与CRISPR扰动结合，在约**20万**个免疫细胞和细胞系中识别扰动靶点、基因signature与遗传互作[61]；同一技术被用于未折叠蛋白反应解剖，通过两个全基因组CRISPRi筛选鉴定约**100**个命中基因，解耦三条UPR分支[49]；**CROP-seq** 则把gRNA盒插入慢病毒3'LTR，使池化筛选可直接读出单细胞转录组[62]。这些工作确立了“扰动—转录组”配对测量的范式，但通量与覆盖仍有限。较新的平台将规模推向全基因组与原代细胞：一项研究扰动4名供体的**2200万**原代人CD4+ T细胞，发现调控因子及基因程序随静息/刺激条件大幅变化[63]。

在建模层面，一条主线是把扰动预测形式化为条件生成或条件传输问题。**PRnet** 以SMILES与剂量构建扰动嵌入，预测新化学扰动的转录响应，并构建覆盖**88**个细胞系、**52**个组织的扰动图谱[35]；**PerturbNet** 强调预测未见化学与遗传扰动引起的细胞状态分布变化而非仅均值，基准对比scGen、CPA、chemCPA、GEARS、Biolord[48]。**SCALE** 针对对照与处理细胞非配对的实际测量方式，用集合感知编码器与条件DiT学习潜在传输，在CRISPR数据七项指标上超越竞争方法，其预测的细胞因子差异经三供体PBMC实验验证[36]。**STRAND** 则指出基因级模型会把同一基因不同位点的扰动坍缩为同一表征，改以调控DNA序列为条件，在K562、Jurkat、RPE1上低样本判别分提升达**33%**，新细胞系迁移Pearson提升达**0.14**，基因组覆盖从约**1.5%**扩至约**95%**[37]。

基础模型路线侧重利用大规模预训练表征。一项工作引入药物条件适配器，仅微调**不到1%**参数，在新细胞系少样本与零样本泛化上显著优于基线[38]；**Tahoe-x1** 将扰动训练的单细胞基础模型扩展到最高**30亿**参数，在基因必需性、癌症标志基因、细胞类型分类与留出情境扰动响应预测四项基准上达SOTA，计算效率较先前细胞状态模型提升**3–30倍**[13]。值得注意的是，规模并非唯一路径：对Tahoe-x1做跨模态继续预训练，仅用**70M**参数、在**48,843**个蛋白质组样本上训练一个epoch，就在多数原评测基准上匹配或超过**1B**和**3B**参数的RNA-only模型，并提升对held-out蛋白扰动的迁移[12]。这与“更大即更好”的缩放叙事形成直接对照。

多模态与可解释性构成另一条分支。**AROMA** 整合文本证据、图拓扑与蛋白序列建模扰动-靶依赖，构建**PerturbReason**数据集（**>498k**样本），在未见细胞系零样本与知识稀疏长尾场景下保持稳健[64]。**DynaVelo** 用生成式神经常微分方程从单细胞多组学数据学习基因表达与TF motif活性的联合动态，重现野生型小鼠生发中心B细胞的体内分叉动态，并揭示Arid1a和Ctcf杂合缺失下的变化[65]。**Chreode** 提出一步式细胞世界模型，以结构化残差转移算子预测动作条件下的状态转移，作为GEARS可迁移嵌入将Norman Perturb-seq的DE20 MSE从**0.2121**降至**0.1858**（相对提升**12.4%**）[41]。**UNAGI** 则用VAE-GAN从疾病时间序列单细胞数据解析细胞动力学并做计算机药物筛选[66]。

与数据驱动模型并行的是对建模范式的反思。**AI虚拟细胞（AIVC）** 愿景主张构建多尺度、多模态大神经网络，从数据直接学习细胞行为而无需显式规则，并提出预测、生成、可查询三大能力[19]。与之相对，细胞行为假设语法路线坚持可解释性，将自然语言细胞规则一一映射为数学方程与agent-based模型，案例覆盖肿瘤生长、侵袭、免疫治疗与脑发育[67]。这两种立场——端到端学习 vs. 显式机制——构成虚拟细胞领域的核心张力。

评估与可信度问题正被单独提出。**Virtual Cell Challenge** 作为开放循环基准竞赛，提供评估框架与专用扰动数据集以加速模型开发[44]。一篇路线图文章批评当前工作偏重模型规模与数据量，主张虚拟细胞模型只有在数据、设计、基准与实验验证的证据链明确时才具决策相关性，并提出分子状态、干预、生物背景、正交表型四层经验框架，认为静态图谱、仅转录组读出与分布内基准不足以预测新条件下的行为[34]。另一篇综述强调从计算评估到CRISPR与类器官实验验证的闭环流程，同时指出监管接受、数据隐私与可解释性仍是障碍[68]。

综合来看，该子问题的分歧集中在三处：其一是表征粒度，基因级扰动建模被指丢失位点信息，序列条件化可部分弥补但依赖序列编码质量[37]；其二是规模与模态的取舍，跨模态数据在70M参数上即可匹敌1B/3B RNA-only模型[12]，而扰动训练的大模型仍在癌症任务上刷新SOTA[13]；其三是评估标准，现有基准多为分布内留出重建，可信虚拟细胞路线图主张转向泛化到未见细胞类型与扰动的生物学标准[34]。数据侧的共同瓶颈也被多方指出：扰动数据集仅覆盖数百分子与少数细胞系[38]，跨细胞类型与组合扰动泛化仍受限[48]，而组合扰动实验规模本身有限[49]。

### 2.4 机制可解释性与表征分析

稀疏自编码器（SAE）已成为拆解单细胞基础模型内部表征的主流工具，但不同工作对“模型里到底编码了什么”给出的答案并不一致。对Geneformer V2-316M与scGPT全人模型各层残差流激活训练TopK SAE，分别得到**82525与24527个特征**，其中**99.8%的特征SVD不可见**，仅29–59%能注释到通路；在转录因子层面，仅**3/48（6.2%）**显示调控靶标特异性，多组织对照下为10.4%[30]。在三个模型（scGPT、scFoundation、Geneformer）隐藏表示上训练的SAE则揭示出多样且复杂的生物与技术信号，且不同训练协议与架构的模型编码方式不同；这些特征具有功能可干预性——抑制批次特征可改善整合并保留生物信号，激活药物特征能使对照细胞呈浓度依赖地向药物扰动状态转变[69]。可见SAE能稳定提取有组织的生物知识，但“知识”与“调控逻辑”之间存在明显缺口。

因果层面的证据进一步收窄了这一缺口。因果电路追踪通过消融SAE特征并测量下游响应，在Geneformer V2-316M与scGPT上跨4条件得到**96,892条边**、80,191次前向传播，两模型均表现约53%生物一致性与**65–89%抑制主导**，且不随架构与细胞类型变化；跨模型共识达1,142个域对（10.6倍富集），但CRISPRi基因级验证的方向准确率仅**56.4%**，提示模型编码的是共表达而非因果调控[14]。对Geneformer的穷举电路追踪（L5层全部4065个SAE特征）得到**1,393,850条显著下游边**，较选择性采样扩27倍，并发现重尾枢纽结构（1.8%特征占大量连接，40%顶级枢纽无注释）、随交互阶数单调加深的冗余（三阶冗余比0.59 vs 配对0.74，零协同），以及层位置决定分化方向性（L17特征100%推向成熟，L0/L11为0.00–0.58）[70]。系统评估框架则从另一角度提出质疑：注意力虽编码分层生物结构（早期层蛋白互作、晚期层转录调控），但对扰动预测无增量价值，**基因级基线AUROC 0.81–0.88优于注意力/相关性边的0.70**，消融调控头无退化，而CSSI可将GRN恢复提升至多1.85×[33]。这些结果共同指向一个争议点：电路结构真实存在且可测量，但其因果/调控效用被基因级统计基线大幅抵消。

在“能否把内部结构转化为可用算法”这一子问题上，工作走向了提取与蒸馏两条路径。三阶段提取方法从scGPT中导出紧凑造血算法，在Tabula Sapiens 564,253细胞上伪时间深度排序**|ρ|=0.439**优于次优0.331，CD4/CD8 AUROC 0.867、单核/巨噬0.951，且比MLP探针快34.5倍、参数少约1000倍[71]。与之相对，GRN推断工作观察到scFM表现不佳，归因于重建式预训练未显式捕获调控信号，遂提出GRN泛化基准并用虚拟值扰动与梯度轨迹从冻结scFM蒸馏可泛化基因间特征，显著优于现有方法[72]。CauTrigger则把do-calculus整合进分层深度潜变量模型，分离因果与虚假潜因子、递归重建调控层级，在合成与真实多层调控数据集上优于现有方法[73]。三者分别代表“从模型内部提取”“从模型蒸馏”“在潜变量模型中显式建模因果”三种取向，其共同前提仍是：当前scFM的表征更接近统计共表达，调控逻辑需要额外的因果结构才能被可靠读出[30][14]。

### 2.5 形态与图像表型基础模型

图像表型基础模型的核心问题正从“能否学到表征”转向“表征在具体生物学任务上是否可靠”。Cell Painting 与 pooled 光学 CRISPR 筛选结合的自监督平台 CellPaint-POSH 在 **163,090 个单细胞**上显示，自监督机器学习特征在基因功能预测上优于经典图像分析与专家形态特征，且形态表型可按已知功能聚类基因、在无通路报告基因时揭示基因关联网络[74]。但特征空间的质量并不自动等于任务相关性：在 U2OS JUMP-MOA 参考板的 **90 个化合物**上零样本评估三种预训练模型，活性阳性数相近（CellPaintSSL **85/90**、OpenPhenom 81/90、uniDINO 82/90），而 CellPaintSSL 的活性检索 mAP 显著高于另两者（p<0.0001），MOA 注释仅部分恢复且因模型而异[75]。综述层面亦给出类似张力：CLOOME 零样本 MoA top-10 准确率 **61.3%** 对比 CellProfiler 24.5%，但部分场景手工特征仍具竞争力，时序与 3D 模态、质控标准和特征解释尚不成熟[76]。

在生成式虚拟细胞方向，监督信号放置位置成为方法差异的焦点。PerturbBridge 指出仅匹配真实图像分布不足以显式优化扰动特异性生物响应，因而在训练中对预测扰动图像直接施加表型监督，将可微生物响应损失与桥回归联合优化、生物梯度经特征提取器回传[77]。其在 BBBC021（**63,781 张训练 + 5,120 张测试**）上 MoA 准确率 CellProfiler 特征达 **77.8%**（较 CellFlux 基线 +5.7 点）、DINOv2 特征 74.9%（+7.5 点），JUMP 上 Hit@10 为 12.15%、中位秩 74，AllenCell 上 Hit@1 为 69.29%[77]。与之互补的是表征预训练规模的证据：在 JUMP-CP 全部未标注化学扰动数据（**119,876 化合物、约 177 万图像、7 个实验室**）上预训练对比式 DINO、掩码生成式 MAE/iTPN 与混合式 DINOv2，最佳 SSL 模型在 JUMP-Target2 留出集的化合物重复检索上优于 CellProfiler[78]。需注意上述检索与生成指标分别来自不同数据集与评估协议，不宜跨研究直接比较高低；共同的方法学争议在于，预训练表征的通用优势能否稳定转化为特定生物学关系（如 MOA）的恢复，仍取决于任务感知的评估与监督设计[75][78]。

## 3 数据与资源

单细胞扰动图谱的规模化是虚拟细胞建模的数据基础。**基因组规模Perturb-seq** 在K562与RPE1两个细胞系中以CRISPRi敲低数千个扰动、覆盖超过250万个细胞，报告了RNA剪接、分化、染色体不稳定等多维表型，并发现线粒体基因组应激的特异调控；其局限在于仅两个细胞系、CRISPRi为敲低而非敲除、表型限于转录组 [23]。与之互补，基于高维单细胞表型构建细胞状态流形的工作将每个扰动与遗传互作投射到流形特定位置，实现调控通路无偏排序与遗传互作系统分类，但依赖强互作筛选、未覆盖全基因组互作 [79]。在空间维度，**Perturb-FISH** 将MERFISH与gRNA原位扩增结合，在LPS刺激巨噬细胞中与匹配的Perturb-seq比较验证敲除效应一致性，并揭示细胞密度与邻居扰动的影响；该方法受限于gRNA仅20 bp、需原位扩增 [80]。药物响应方向，**Tahoe-100M** 覆盖超过1亿细胞、50个细胞系与379种化合物，采用3D球状体混合细胞系、24小时三剂量处理，覆盖约56,000个细胞系-药物-剂量组合，发现Dabrafenib在非BRAF依赖细胞系中的意外敏感性及CDK抑制剂引起G1或G2/M阻滞，但摘要未提供模型训练与验证细节 [24]。

空间图谱方面，全小鼠脑MERFISH成像约800万细胞、超过1100个基因并整合scRNA-seq，鉴定超过5000个转录簇与约300个主要细胞类型，注册到小鼠脑共坐标框架以量化各脑区细胞组成并识别空间模块；其局限为仅限小鼠脑、基因面板有限 [81]。在资源整合层面，Human Cell Atlas相关工作提出细胞图谱作为细胞普查、3D图谱、基因型-表型连接、4D发育图谱及生物学基础模型五种用途，指向从数据收集走向图谱整合与统一基础模型 [20]。上述资源在扰动类型（敲低、敲除、化合物）、读出模态（转录组、空间、钙活动）与物种覆盖上差异明显，尚无跨队列可直接比较的统一基准。

## 4 应用与结果

面向肝脏的 AI 虚拟细胞（AIVC）建模目前被归纳为三条互补路线：生成模型、动力学/运输模型，以及预训练/基础模型，并以扰动响应预测作为跨层评估的落点[17]。现有证据按验证强度分为四类——直接肝脏验证、含肝脏基准、通用单细胞证据与概念应用；但已发表模型仅展示了图谱整合、轨迹推断、可迁移表示、回顾性响应程序等单个组件，**尚无前瞻验证的肝脏模拟器**[17]。

这一现状的根源在于图谱类证据的固有边界：单细胞与空间图谱能高分辨率描述健康与疾病肝脏，包括小叶区带化、纤维化巨噬细胞—星状细胞生态位、胆管细胞反应、免疫重塑与肝细胞癌生态系统，但**只说明细胞状态出现在何处，本身不能预测肝损伤是否进展**，也无法预测对未测试药物、毒物或遗传扰动的响应[17]。因此该综述主张评估需覆盖供体、病因、分期与平台等维度[17]。

## 5 评测、可复现性与争议

评测工作的第一条主线是**预训练污染与基准泄漏**。scContam 用 MinHash 基因集指纹加基于损失的成员推断攻击（MIA-scFM）逐细胞审计，在 PBMC 3k 与胰腺胰岛图谱上分别有 **80.4%、77.0%** 的细胞指纹 p<0.05，而截断后的 AIDA v2 与 Tahoe-100M 为 **0%**；MIA AUROC 随模型容量数据比从 0.494 升到 0.690 再到 0.881 [31]。这说明高引用整合基准上的零样本成绩可能反映预训练暴露而非泛化，但作者也指出生产级 scFM 抗实例记忆，分布污染需单独检测 [31]。

第二条主线是**简单基线对基础模型的挑战**。在扰动后表达预测上，四个 Perturb-seq 数据集的差分空间里 Train Mean 基线（0.711/0.557/0.373/0.628）优于 scGPT（0.641/0.554/0.327/0.596）与 scFoundation（0.552/0.459/0.269/0.471），而随机森林加 GO 特征最佳（0.739/0.586/0.480/0.648）[15]。另一项工作比较五个基础模型和两个深度学习模型与刻意简单的基线，结论是**无一超过基线**，遗传互作预测也不优于 no change 基线 [82]。PertEval-scFM 同样报告零样本 scFM 嵌入未持续优于基线，尤其在分布偏移下 [83]。在非扰动任务上，无参数线性流程在多个基准取得 SOTA 或近 SOTA，并在新细胞类型与新物种的分布外任务上超越基础模型 [32]。

但这一结论本身存在争议。有研究提出阳性对照基线与指标校准框架，在 14 个数据集和 18 个指标上发现 **MSE 和 Pearson Δ 等常用指标常校准不良**，降低了对阳性模型性能的敏感性；在良好校准指标下，深度学习扰动模型可优于无信息基线 [16]。这提示「基础模型不如基线」的部分证据可能受指标选择影响，与前述负面结论形成直接张力。

**任务依赖性**是多数评测的共同发现。七种基础模型与三种经典表示的低监督比较中，CellPLM 在聚类、注释、批次校正领先，scMulan 在扰动预测领先，PCA 在重建领先；7 个基础模型中仅 1 个聚类超过最强经典基线，批次校正 3 个、注释 4 个、重建 0 个、扰动预测 6 个超过基线 [45]。零样本评估 scGPT、SCimilarity、UCE、Transcriptformer 时，注释任务基线多数数据集最强，蛋白表达预测基础模型更准（SCimilarity 误差最低、Transcriptformer 相关性最高），整合任务基础模型中等而 scVI 更佳 [46]。细胞类型分类的专项评测则给出更分化的结果：scFoundation 持续最佳，Geneformer 表现差甚至不如基线 [47]。

统一框架的跨模态评测进一步显示**排名不稳定**。对 Nicheformer、CellPLM、scGPT-spatial、GenePT、scELMo、Novae 六个模型的统一基准中，无模型全面领先；表达训练的细胞级 Transformer 擅长细胞身份，空间/图模型保留组织结构，语言嵌入在部分扰动指标有竞争力，排名随模态、预处理、token 化、生物先验、域偏移和指标变化 [84]。VCBench 把四个虚拟细胞框架综合为七个能力维度，在五个可测维度上，**预注册的线性/最近邻基线在 4 维追平或超越所有基础模型**，仅 TranscriptFormer 在 RNA 到蛋白预测上超最强基线 53% Pearson [85]；多尺度整合与 in silico 实验两维度结构上无法端到端测试 [85]。

**可复现性与评测基础设施**是另一条独立线索。整合基准方面，68 种方法与预处理组合在 85 个批次、13 个图谱级任务上评测，Scanorama 和 scVI 在复杂任务表现好，有注释时 scGen 和 scANVI 最优，Harmony 和 LIGER 适合 scATAC [86]。扰动预测方面，PerturBench 揭示广泛使用模型存在**模式崩溃**，秩指标可补充 RMSE，无单一架构明显占优 [87]；scArchon 以 Snakemake 容器化运行 9 种工具并聚合评分排名 [88]；BioLLM 用统一 API 与决策树预处理解决预处理不一致、接口异构和指标非标准化三大挑战 [89]。图像侧，JUMP 原始数据 115 TB，JUMP-lite 压缩为 **92.0 GB**、约缩小 1,250 倍，中度压缩基本保留信号 [90]。空间转录组侧，ST 数据集跨三站点六组织类型比较 Xenium 与 CosMx，STP 门户可实时评估约 **3300 万细胞**数据 [91]。

**无监督与分布外评估**代表方法学上的转向。一项框架基于「忠实表征应在模拟技术与采样变异扰动下保持邻域结构」，测试 5 个 scFM、PCA 基线与 39 个数据集，发现标准基准判定近乎等价的模型在丢弃 **5%** 计数时局部邻域保持差异近 2 倍，且该不稳定性被视觉连贯的嵌入掩盖 [92]。EL-PERTURB 采用分层 OOD 划分，在必需基因与全基因组 Perturb-seq 数据上压力测试 6 类架构的 20 个模型，结论是现有基准多依赖随机划分而掩盖系统性失效模式，模型在真实 OOD 条件下泛化失败 [93]。这与前述「校准后深度学习可胜基线」的结论并不矛盾但取向相反：前者说指标不敏感，后者说划分不严格，共同指向评测设计本身决定结论。

**可解释性与生物学信号**的争议集中在注意力机制。统一 GRN 基准区分 token 嵌入、隐状态与注意力分数三种信号来源，零样本下 scGPT token 嵌入相似度在 STRING 和 ChIP-seq 上超越经典基线，scFoundation 动态转移表现最强 [94]。但另一项两层评估框架在 2 种架构、4 种细胞类型、2 种扰动模态下做 **153 项统计检验**加因果消融，发现注意力边分数相对基因级特征无增量价值，单变量基线反而更优，TRRUST 头因果消融无行为效应 [95]。两者结论的差异在于前者测参考网络恢复、后者测扰动靶标预测，说明「注意力是否可解释」高度依赖所测任务。

生物学驱动的评测则试图回答基础模型是否捕捉到超越统计拟合的信息。六模型在基因级与细胞级任务上对比 HVG、Seurat、Harmony、scVI 等基线，并引入 AIDA v2 独立数据集与细胞本体指标 scGraph-OntoRWR、LCAD，结论是零样本嵌入确实捕捉生物学信息，但预训练模型在部分场景未超越简单基线，需按任务选择模型 [96]。与之呼应，扰动响应预测的 27 种方法、29 个数据集、6 类指标评测强调细胞上下文嵌入对提升泛化性的必要性，同时指出基础模型表现仍存疑 [97]。

最后，基准本身的有效性也受到质疑。小分子活性基准中许多 assay 与细胞健康或毒性直接相关，逻辑回归细胞计数达 **AUC 0.70±0.22**，接近 CLOOME 的 0.71±0.19，细胞计数加 MW 与 logP 达 0.74±0.21；但在 24 个蛋白靶标基准中 Cell Painting 确实优于细胞计数 [98]。这与扰动领域「简单基线追平复杂模型」的模式一致，但作者的建议是过滤此类 assay 并纳入细胞计数基线，而非否定复杂模型本身。

## 6 空白与趋势

在「空白与趋势」层面，这一方向正从「造更大的模型」转向「弄清模型到底学到了什么、以及在哪里失效」，以下六条趋势与空白值得单独标出。

1. **机制可解释性已形成独立子领域，但「可解释」与「可预测」之间尚未打通。** SAE 拆解显示模型内化了有组织的生物知识，却几乎不含因果调控逻辑（仅 **6.2%** 转录因子显示靶标特异性）[30]；因果电路追踪给出约 53% 生物一致性、**65–89% 抑制主导**，但 CRISPRi 方向准确率仅 **56.4%** [14]；系统评估更直接指出注意力对扰动预测无增量价值、基因级基线 AUROC **0.81–0.88** 优于注意力边 **0.70** [33]。**空白在于：尚无工作把电路/特征层面的结构证据转化为在留出扰动上稳定增益的预测器**，现有「提取算法」[71] 与「蒸馏特征」[72] 只是两条初步路径，缺少统一评测。

2. **评测正在从「分布内留出」转向「污染审计 + 校准指标 + 分布外泛化」，但三者尚未合并成一套协议。** scContam 发现两个高引用基准存在大量预训练重叠证据，截断后重叠为 **0%**，且 MIA AUROC 随容量数据比升至 **0.881** [31]；指标校准研究指出 MSE、Pearson Δ 常校准不良，在良好校准指标下深度学习扰动模型可优于无信息基线 [16]；可信虚拟细胞路线图则主张转向泛化到未见细胞类型与扰动 [34]。**没人做的是：把污染审计、指标校准与分布外划分三者叠加到同一基准上重跑主流模型**——这正是当前「基础模型不如基线」与「基础模型持续 SOTA」两类结论无法收敛的方法学根源 [15][82]。

3. **规模叙事正在被「模态与监督信号的位置」取代，但替代方案缺少统一比较。** 一方面系统实验在 **2220 万细胞、400 个模型、6400 次实验**下未观察到明确数据缩放定律 [4]；另一方面跨模态继续预训练仅用 **70M** 参数、**48,843** 个蛋白质组样本一个 epoch 即匹配或超过 **1B/3B** RNA-only 模型 [12]。**空白在于：尚无跨任务、跨模态的「参数—数据—模态」三维缩放研究**，现有结论各自局限于单一模型族与单一基准。

4. **扰动建模的粒度正从基因级下沉到位点级与序列级，但组合扰动与跨细胞系泛化仍是硬缺口。** STRAND 指出基因级模型会把同基因不同位点坍缩为同一表征，改以调控 DNA 序列为条件后基因组覆盖从约 **1.5%** 扩至约 **95%** [37]；SCALE 以集合感知传输绕开细胞级配对 [36]。但证据侧同时承认扰动数据集仅覆盖数百分子与少数细胞系 [38]、组合扰动实验规模本身有限 [49]。**没人做的是：系统评测「位点级/序列级条件」在组合扰动与未见细胞系上的增益是否可叠加**，而非仅在单扰动基准上报告提升。

5. **空间与影像基础模型的预训练目标出现路线分歧，且评测受平台与分割差异严重污染。** CellWorld 主张放弃基因重建、改预测潜在细胞表征，其 **5.74M** 小模型在全部 **11** 个线性探针与 **7** 个空间基准上超越所有基线 [9]；NexuST 则坚持基因级与细胞级交错建模 [42]。与此同时，四平台系统评测显示灵敏度、分割、注释差异显著 [10]，**11** 种分割方法在 **15** 个数据集上差异同样显著 [11]。**空白在于：缺少在统一分割与统一真值下重跑这些空间基础模型的交叉基准**，现有跨研究数字不宜横向比较。

6. **「虚拟细胞」的可信度与实验闭环被反复呼吁，但前瞻验证几乎空白。** Virtual Cell Challenge 提供开放循环基准 [44]，路线图要求数据、设计、基准与实验验证形成证据链 [34]，肝脏 AIVC 综述更直接指出**尚无前瞻验证的肝脏模拟器**，图谱只能说明细胞状态出现在何处、不能预测扰动响应 [17]。**最明显的空白是：目前几乎没有工作报告「模型预测—湿实验验证—失败案例公开」的完整闭环**，SCALE 的细胞因子验证 [36] 与 Perturb-FISH 的空间扰动读出 [80] 只是零散样例，尚不构成可复用的验证范式。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 单细胞基础模型 | 成熟（方法收敛、增量为主） | scGPT [1] 与 Geneformer/网络迁移学习 [2] 已确立"大规模预训练+微调"范式并被广泛复用；但 GenePT [52] 用简单基因文本嵌入即取得有竞争力效果，说明架构创新边际收益下降、进入增量改良期；同时评测证据 [99] 显示基础模型在下游任务上优势有限，进一步支持"方法已收敛、争议转向评测"的判断。 |
| 2.2 空间与多模态模型 | 朝阳（近两年爆发、方法未收敛） | 多模态整合 [28] 与时空映射 [58] 代表两类不同技术路线并存，尚未统一；阿尔茨海默病整合图谱 [100] 与 Cell Painting 综述 [60] 显示数据规模与模态仍在快速扩张，方法层面无收敛共识。 |
| 2.3 扰动响应与虚拟细胞 | 朝阳（近两年爆发、CNS 频出、方法未收敛） | 早期 Perturb-seq 平台 [61]、[62] 奠定数据基础，近两年"AI 虚拟细胞"路线图 [19] 将其提升为领域议程；但 [82] 明确报告深度学习扰动预测**尚未跑赢简单基线**，说明目标明确而方法远未收敛，属典型高热度+高不确定的朝阳期。 |
| 2.4 机制可解释性与表征分析 | 萌芽（少量探索性工作） | 稀疏自编码器解析单细胞基础模型特征 [69] 与系统性可解释性评测 [33] 均为 2026 年新出、引用近零的探索性工作；[30] 进一步指出模型内部"有组织生物知识但调控逻辑有限"，问题刚被提出、尚无方法共识。 |
| 2.5 形态与图像表型基础模型 | 萌芽（少量探索性工作） | 池化 Cell Painting CRISPR 筛选平台 [74] 与图像 profiling 挑战综述 [76] 表明数据与评测框架刚起步；检索式评测 [75] 显示特征空间差异尚未厘清，方法仍在早期探索。 |
| 3 数据与资源 | 成熟（方法收敛、增量为主） | 全基因组 Perturb-seq 图谱 [23] 与遗传互作流形 [79] 已建立规模化扰动数据生产范式；Human Cell Atlas 从细胞普查走向统一基础模型 [20] 标志资源建设进入"整合与复用"阶段，增量为主。 |
| 4 应用与结果 | 证据不足 | 雷达样本中仅 1 篇（[17]，肝病 AI 虚拟细胞展望，2026、引用 0），不足以判断阶段。 |
| 5 评测、可复现性与争议 | 朝阳（近两年爆发、方法未收敛） | 图谱整合基准 [86] 确立评测范式；近两年 PerturBench [87] 与"未跑赢基线"的批判性结果 [82] 集中爆发，说明评测本身成为独立且快速演进的研究方向，标准尚未定型。 |

**整体判断**：这个方向整体处于**朝阳期偏后段**——单细胞基础模型（2.1）与数据资源（3）已进入成熟/增量阶段，而**扰动响应与虚拟细胞（2.3）、空间多模态（2.2）、评测（5）仍在爆发且方法未收敛**，雷达样本中 2025–2026 年证据占 **74%**、CNS 占 **32%**，但同一批证据里出现了"**深度学习扰动预测尚未跑赢简单基线**"[82] 这样的强反证。窗口期判断：**纯"再训一个更大的单细胞基础模型"的窗口基本关闭**（2.1 已收敛、GenePT 类简单基线即可竞争 [52]）；**真正开放的窗口约 1–2 年**，集中在"扰动预测的可信评测 + 多模态/形态表型 + 可解释性"三块。最大不确定性是：**虚拟细胞的核心承诺（扰动响应可预测）目前缺乏超越基线的证据**，若 1–2 年内仍无大规模验证，领域可能从"朝阳"快速转入"期望回落"，届时纯生成式路线会被评测驱动的务实路线替代。

**接下来怎么做**：

1. **做"扰动预测的可信评测 + 失败归因"，而不是再训一个预测模型。** 切入点：用公开 Perturb-seq / Tahoe 类数据 + PerturBench [87] 框架，系统复现现有方法并与简单基线对比 [82]，产出"何时基础模型才真正有用"的判定准则与开源评测套件。为什么现在做：领域刚被批判性结果震动、标准未定，**评测类工作引用窗口最好**；且与你公共数据 demo 的合作项目直接契合。

2. **把衰老作为扰动维度切入虚拟细胞，做"衰老背景下的扰动响应预测"。** 切入点：在公共衰老/扰动图谱上构造"年龄×扰动"条件预测任务，检验现有虚拟细胞框架 [19] 在衰老背景下的泛化，产出领域首个衰老扰动基准。为什么现在做：2.3 方法未收敛、衰老维度几乎无人系统评测，你的衰老+单细胞背景是**差异化壁垒**，且能直接对接类器官多组学合作。

3. **用类器官多组学做"形态+转录组"多模态整合的小规模验证。** 切入点：类器官 Cell Painting/成像 + scRNA-seq 配对数据，复用 MultiVI [28] 与时空映射 [58] 思路，验证形态表型能否作为扰动的低成本读出 [74]。为什么现在做：2.5 处于萌芽、图像 profiling 挑战刚被系统提出 [76]，**小规模配对数据就能出有辨识度的结果**，且正是你合作项目的现成数据形态。

4. **做基础模型的可解释性表征分析，作为低成本高杠杆的"副线"。** 切入点：对 scGPT [1] 等公开权重做稀疏自编码器特征分解 [69]，并复现系统性可解释性评测 [33]，回答"模型学到了调控逻辑还是仅统计关联"[30]。为什么现在做：2.4 全部为 2026 年新工作、**引用近零、竞争极少**，用现成权重即可启动，适合作为主线风险的对冲。

5. **避免正面重训通用单细胞基础模型；若要做模型，只做"评测驱动的小而专"模型。** 切入点：以 2.3/2.5 的具体任务（如形态扰动生成 [77]）为目标训练专用模型，并以第 1 条的评测套件自证优于基线。为什么现在做：2.1 已成熟、通用模型增量收益低 [52]，而**专用模型+严格评测**是当前证据支持下唯一能站住脚的建模路径。

## 参考文献

1. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. Nature Methods 2024. https://doi.org/10.1038/s41592-024-02201-0
2. Transfer learning enables predictions in network biology. Nature 2023. https://doi.org/10.1038/s41586-023-06139-9
3. CellFM: a large-scale foundation model pre-trained on transcriptomics of 100 million human cells.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59926-5
4. Evaluating the role of pretraining dataset size and diversity on single-cell foundation model performance.. Nature methods 2026. https://doi.org/10.1038/s41592-026-03120-y
5. Zero-shot evaluation reveals limitations of single-cell foundation models.. Genome biology 2025. https://doi.org/10.1186/s13059-025-03574-x
6. Intermediate Layers Encode Optimal Biological Representations in Single-Cell Foundation Models.  2026. https://arxiv.org/abs/2604.14838v1
7. A Cross-Species Generative Cell Atlas Across 1.5 Billion Years of Evolution: The TranscriptFormer Single-cell Model. bioRxiv 2025. https://doi.org/10.1101/2025.04.25.650731
8. LucaCell: a sequence-centric foundation model for cross-species single-cell analysis.  . https://doi.org/10.21203/rs.3.rs-11151765/v1
9. CellWorld: From Gene-Level Reconstruction to Latent Cell Prediction in Spatial Transcriptomics Foundation Models.  2026. https://arxiv.org/abs/2608.06659v1
10. Systematic benchmarking of high-throughput subcellular spatial transcriptomics platforms across human tumors.. Nature communications 2025. https://doi.org/10.1038/s41467-025-64292-3
11. Benchmarking segmentation methods for spatial transcriptomics.. Nature methods . https://doi.org/10.1038/s41592-026-03272-x
12. Single-cell foundation models benefit from cross-modal training: adding proteomics data beats parameter scaling. bioRxiv 2026. https://doi.org/10.64898/2026.08.14.744845
13. Tahoe-x1: Scaling Perturbation-Trained Single-Cell Foundation Models to 3 Billion Parameters. bioRxiv 2025. https://doi.org/10.1101/2025.10.23.683759
14. Causal Circuit Tracing Reveals Distinct Computational Architectures in Single-Cell Foundation Models: Inhibitory Dominance, Biological Coherence, and Cross-Model Convergence.  2026. https://arxiv.org/abs/2603.01752v2
15. Benchmarking foundation cell models for post-perturbation RNA-seq prediction.. BMC genomics 2025. https://doi.org/10.1186/s12864-025-11600-2
16. Deep learning perturbation models can outperform baselines on calibrated metrics.. Nature biotechnology . https://doi.org/10.1038/s41587-026-03307-w
17. Toward AI Virtual Cells for Hepatology: Representation, Generation, Dynamics, and Intervention in Single-Cell Models.. Clinical and Molecular Hepatology 2026. https://doi.org/10.3350/cmh.2026.0820
18. Single-cell foundation models: bringing artificial intelligence into cell biology.. Experimental & molecular medicine 2025. https://doi.org/10.1038/s12276-025-01547-5
19. How to build the virtual cell with artificial intelligence: Priorities and opportunities.. Cell 2024. https://doi.org/10.1016/j.cell.2024.11.015
20. The Human Cell Atlas from a cell census to a unified foundation model.. Nature 2024. https://doi.org/10.1038/s41586-024-08338-4
21. Scalable querying of human cell atlases via a foundational model reveals commonalities across fibrosis-associated macrophages. bioRxiv 2023. https://doi.org/10.1101/2023.07.18.549537
22. A cell atlas foundation model for scalable search of similar human cells.. Nature 2024. https://doi.org/10.1038/s41586-024-08411-y
23. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. bioRxiv 2021. https://doi.org/10.1016/j.cell.2022.05.013
24. Abstract 491: A 100 million cell single cell atlas enabling mechanistic and genotype-specific drug response discovery.. Cancer Research 2026. https://doi.org/10.1158/1538-7445.am2026-491
25. PAST: A multimodal single-cell foundation model for histopathology and spatial transcriptomics in cancer. arXiv.org 2025. https://arxiv.org/abs/2507.06418v1
26. A visual-omics foundation model to bridge histopathology with spatial transcriptomics.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02707-1
27. A multimodal knowledge-enhanced whole-slide pathology foundation model.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66220-x
28. MultiVI: deep generative model for the integration of multimodal data. Nature Methods 2023. https://doi.org/10.1038/s41592-023-01909-9
29. CLM-X: A multimodal single-cell foundation model with flexible multi-way Transformer for unified scRNA-seq and scATAC-seq analysis. bioRxiv 2026. https://doi.org/10.64898/2026.02.17.704943
30. Sparse autoencoders reveal organized biological knowledge but minimal regulatory logic in single-cell foundation models: a comparative atlas of Geneformer and scGPT.  2026. https://arxiv.org/abs/2603.02952v1
31. Auditing pretraining contamination in single-cell foundation model benchmarks.  2026. https://arxiv.org/abs/2607.20572v1
32. Parameter-free representations outperform single-cell foundation models on downstream benchmarks.  2026. https://arxiv.org/abs/2602.16696v1
33. Systematic Evaluation of Single-Cell Foundation Model Interpretability Reveals Attention Captures Co-Expression Rather Than Unique Regulatory Signal.  2026. https://arxiv.org/abs/2602.17532v1
34. Toward trustworthy virtual cells: a roadmap for perturbation-resolved, context-aware, and experimentally validated cell models. Frontiers in Cell and Developmental Biology 2026. https://doi.org/10.3389/fcell.2026.1900624
35. Predicting transcriptional responses to novel chemical perturbations using deep generative model for drug discovery.. Nature communications 2024. https://doi.org/10.1038/s41467-024-53457-1
36. SCALE:Scalable Conditional Atlas-Level Endpoint transport for virtual cell perturbation prediction.  2026. https://arxiv.org/abs/2603.17380v3
37. STRAND: Sequence-Conditioned Transport for Single-Cell Perturbations.  2026. https://arxiv.org/abs/2602.10156v1
38. Efficient Fine-Tuning of Single-Cell Foundation Models Enables Zero-Shot Molecular Perturbation Prediction.  2024. https://arxiv.org/abs/2412.13478v2
39. scPRINT-2: Towards the next-generation of cell foundation models and benchmarks.  2025. https://doi.org/10.64898/2025.12.11.693702
40. scDifformer: diffusion-based post-training for virtual cell modeling across large-scale single-cell data. Nucleic Acids Research 2026. https://doi.org/10.1093/nar/gkag706
41. Chreode: A Cell World Model for One-Step Temporal Dynamics and Perturbation Prediction. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.28111
42. NexuST: A Hierarchical Foundation Model for Spatial Transcriptomics.  . https://doi.org/10.64898/2026.09.22.753590
43. VINTER: a generative vision-language model for annotating and interrogating spatial tissues.  . https://doi.org/10.64898/2026.10.01.752251
44. Virtual Cell Challenge: Toward a Turing test for the virtual cell.. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.008
45. Task-dependent Performance of Single-cell Foundation Models under Low Supervision. bioRxiv 2026. https://doi.org/10.64898/2026.04.01.714123
46. Benchmarking single-cell foundation models in a zero-shot setting. bioRxiv 2026. https://doi.org/10.64898/2026.08.03.739553
47. A Systematic Evaluation of Single-Cell Foundation Models on Cell-Type Classification Task. Web Search and Data Mining 2025. https://doi.org/10.1145/3701551.3708811
48. PerturbNet predicts single-cell responses to unseen chemical and genetic perturbations.. Molecular systems biology 2025. https://doi.org/10.1038/s44320-025-00131-3
49. A multiplexed single-cell CRISPR screening platform enables systematic dissection of the unfolded protein response. Cell 2016. https://doi.org/10.1016/j.cell.2016.11.048
50. Emerging frontiers for AI in single-cell genomics.. Molecular cell . https://doi.org/10.1016/j.molcel.2026.09.014
51. RegFormer: a single-cell foundation model powered by gene regulatory hierarchies.. Nature communications 2026. https://doi.org/10.1038/s41467-026-72198-x
52. GenePT: A Simple But Effective Foundation Model for Genes and Cells Built From ChatGPT. bioRxiv 2023. https://doi.org/10.1101/2023.10.16.562533
53. Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling.  . https://doi.org/10.64898/2026.09.22.752128
54. EpiZoo: a DNA sequence-aware foundation model for cross-species single-cell epigenomics.  . https://doi.org/10.64898/2026.09.24.754017
55. ProtCell: a foundation model for single-cell proteomics.  . https://doi.org/10.64898/2026.10.22.760932
56. PTM-Mamba: a PTM-aware protein language model with bidirectional gated Mamba blocks.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02656-9
57. Deep generative modeling of sample-level heterogeneity in single-cell genomics.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02808-x
58. Mapping cells through time and space with moscot.. Nature 2025. https://doi.org/10.1038/s41586-024-08453-2
59. A clinical benchmark of public self-supervised pathology foundation models.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58796-1
60. Cell Painting: a decade of discovery and innovation in cellular imaging.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02528-8
61. Perturb-seq: Dissecting molecular circuits with scalable single cell RNA profiling of pooled genetic screens. Cell 2016. https://doi.org/10.1016/j.cell.2016.11.038
62. Pooled CRISPR screening with single-cell transcriptome read-out. Nature Methods 2017. https://doi.org/10.1038/nmeth.4177
63. Genome-scale perturb-seq in primary human CD4+ T cells maps context-specific regulators of T cell programs and human immune traits.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.002
64. AROMA: Augmented Reasoning Over a Multimodal Architecture for Virtual Cell Genetic Perturbation Modeling.  2026. https://arxiv.org/abs/2604.20263v1
65. Deep dynamical models of single-cell multiomic velocities predict loss-of-function and rescue perturbations in B cells.. Nature biotechnology . https://doi.org/10.1038/s41587-026-03348-1
66. A deep generative model for deciphering cellular dynamics and in silico drug discovery in complex diseases.. Nature biomedical engineering 2025. https://doi.org/10.1038/s41551-025-01423-7
67. Human interpretable grammar encodes multicellular systems biology models to democratize virtual cell laboratories.. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.048
68. AI-driven virtual cell models in preclinical research: technical pathways, validation mechanisms, and clinical translation potential.. NPJ digital medicine 2025. https://doi.org/10.1038/s41746-025-02198-6
69. Sparse Autoencoders Reveal Interpretable Features in Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.1101/2025.10.22.681631
70. Exhaustive Circuit Mapping of a Single-Cell Foundation Model Reveals Massive Redundancy, Heavy-Tailed Hub Architecture, and Layer-Dependent Differentiation Control.  2026. https://arxiv.org/abs/2603.11940v1
71. Discovery of a Hematopoietic Manifold in scGPT Yields a Method for Extracting Performant Algorithms from Biological Foundation Model Internals.  2026. https://arxiv.org/abs/2603.10261v1
72. Towards Universal Gene Regulatory Network Inference: Unlocking Generalizable Regulatory Knowledge in Single-cell Foundation Models.  2026. https://arxiv.org/abs/2605.08128v1
73. CauTrigger: deciphering biological system state transitions by hierarchical causal decomposition.. Nature methods . https://doi.org/10.1038/s41592-026-03274-9
74. A pooled Cell Painting CRISPR screening platform enables de novo inference of gene function by self-supervised deep learning.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66778-6
75. Retrieval-Based Evaluation of Cell Painting Feature Spaces Reveals Differences in the Preservation of Biologically Meaningful Phenotypic Similarity.. International journal of molecular sciences 2026. https://doi.org/10.3390/ijms27135727
76. Progress and new challenges in image-based profiling.. Molecular systems biology 2026. https://doi.org/10.1038/s44320-026-00197-7
77. PerturbBridge: Direct Phenotypic Supervision for Cellular Perturbation Generation.  . https://arxiv.org/abs/2610.17066
78. Advancing morphological profiling with self-supervised learning through comparative insights into representation learning of cellular perturbations.. Nature methods . https://doi.org/10.1038/s41592-026-03270-z
79. Exploring genetic interaction manifolds constructed from rich single-cell phenotypes. Science 2019. https://doi.org/10.1126/science.aax4438
80. Simultaneous CRISPR screening and spatial transcriptomics reveal intracellular, intercellular, and functional transcriptional circuits.. Cell 2025. https://doi.org/10.1016/j.cell.2025.02.012
81. A molecularly defined and spatially resolved cell atlas of the whole mouse brain. bioRxiv 2023. https://doi.org/10.1101/2023.03.06.531348
82. Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02772-6
83. PertEval-scFM: Benchmarking Single-Cell Foundation Models for Perturbation Effect Prediction. bioRxiv 2025. https://doi.org/10.1101/2024.10.02.616248
84. Harmonised benchmarking of foundation models for single-cell and spatial transcriptomics reveals context-dependent generalisation.  2026. https://arxiv.org/abs/2607.17227
85. VCBench: A Multi-Dimensional Benchmark for Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.06.18.733146
86. Benchmarking atlas-level data integration in single-cell genomics. Nature Methods 2020. https://doi.org/10.1038/s41592-021-01336-8
87. PerturBench: Benchmarking Machine Learning Models for Cellular Perturbation Analysis. Neural Information Processing Systems 2024. https://doi.org/10.48550/arXiv.2408.10609
88. scArchon: a scalable benchmarking framework for assessing single-cell perturbation models.. Genome biology 2026. https://doi.org/10.1186/s13059-026-04104-z
89. BioLLM: A standardized framework for integrating and benchmarking single-cell foundation models. bioRxiv 2024. https://doi.org/10.1016/j.patter.2025.101326
90. JUMP-lite: Compact, reproducible benchmarking of cell representations.  2026. https://arxiv.org/abs/2608.07632
91. Standardized metrics for assessment and reproducibility of imaging-based spatial transcriptomics datasets.. Nature biotechnology 2025. https://doi.org/10.1038/s41587-025-02811-9
92. Robustness to nuisance perturbations enables unsupervised evaluation of single-cell foundation models. bioRxiv 2026. https://doi.org/10.64898/2026.08.22.746357
93. Genetic Perturbation Prediction Models Fail Out-of-Distribution: A Rigorous Benchmark and Systematic Evaluation.  . https://doi.org/10.64898/2026.10.16.759604
94. Benchmarking Static Gene Regulatory Network Reconstruction and Dynamic Transition Probing in Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.05.17.725083
95. Systematic evaluation of single-cell foundation model interpretability: attention-derived edge scores add no incremental value over gene-level features for perturbation-target prediction. BMC Genomics 2026. https://doi.org/10.1186/s12864-026-12965-8
96. Biology-driven insights into the power of single-cell foundation models. Genome Biology 2025. https://doi.org/10.1186/s13059-025-03781-6
97. Benchmarking algorithms for generalizable single-cell perturbation response prediction.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02980-0
98. Counting cells can accurately predict small-molecule bioactivity benchmarks.. Nature communications 2026. https://doi.org/10.1038/s41467-026-68725-5
99. Evaluating the Utilities of Foundation Models in Single‐Cell Data Analysis. bioRxiv 2024. https://doi.org/10.1101/2023.09.08.555192
100. Integrated multimodal cell atlas of Alzheimer's disease.. Nature neuroscience 2024. https://doi.org/10.1038/s41593-024-01774-5
