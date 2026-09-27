# 单细胞与空间组学基础模型与虚拟细胞 · 方向背景报告

证据 87 篇 · 覆盖度 0.65 · 第 6 轮 · 更新 2026-09-27 · 数字核验删句 1

## 摘要（TL;DR）

- 单细胞基础模型把“细胞类比句子、基因类比词元”，通过大规模自监督预训练获得通用表征，再适配注释、整合、扰动预测等下游任务[1]。
- scGPT 在超 3300 万个细胞的 scRNA-seq 数据上训练，迁移学习后在注释、多批次/多组学整合、扰动预测和基因网络推断等任务上表现优异[2]。
- Geneformer 在约 3000 万个单细胞转录组上以自监督方式学习网络动力学，微调后在染色质与网络动力学任务中持续提升准确率，并在有限患者数据下识别出心肌病候选治疗靶点[3]。
- CellFM 把预训练规模推到 1 亿人类细胞，在多种下游任务上达到或超过 Geneformer、scGPT、scFoundation、UCE 等模型，但仅覆盖人类单物种，数据清洗与批次异质性仍影响泛化[4]。
- scPRINT-2 扩展到 3.5 亿细胞、16 个物种，在表达去噪、细胞嵌入和细胞类型预测上达到 SOTA，还具备表达插补与反事实推理的生成能力，并可泛化到未见模态和物种[5]。
- TranscriptFormer 在多达 1.12 亿细胞、12 个物种、跨越 15.3 亿年进化的数据上联合建模基因身份与表达水平，在分布内与分布外细胞类型分类上达 SOTA，可零样本识别疾病状态并跨物种转移注释[6]。
- 零样本评估发现，Geneformer 和 scGPT 在 5 个多样单细胞数据集上的细胞类型聚类和批次校正表现，多数情况下不如 HVG、Harmony、scVI 等更简单的基线[7]。
- 一项针对预训练数据规模与多样性的研究用 2220 万细胞语料预训练 400 个模型并开展 6400 次实验，发现性能在数据规模远小于当前训练语料时即趋于平台，且未观察到明确的数据缩放定律[8]。
- 逐层评估对 scFoundation（100M 参数）和 Tahoe-X1（1.3B 参数）系统比较各层嵌入，发现轨迹任务在 60% 深度达峰、比最终层高 31%，扰动最优层随 T 细胞激活状态在 0–96% 间大幅漂移[9]。
- 在四个 Perturb-seq 数据集上，差分空间的 Train Mean 基线（0.711/0.557/0.373/0.628）优于 scGPT（0.641/0.554/0.327/0.596）与 scFoundation（0.552/0.459/0.269/0.471），而结合 GO 特征的随机森林最佳（0.739/0.586/0.480/0.648）[10]。

## 1 背景与定义

单细胞与空间组学基础模型与虚拟细胞的边界，可以从三个层次界定。**最窄的一层是"带公开权重的单细胞/空间/蛋白/形态基础模型"**：它们以细胞为建模单元、基因或图像 patch 为 token，通过自监督预训练获得可迁移表征，代表性工作包括 scGPT[2]、Geneformer[3]、CellFM[4]、SCimilarity[11] 等。**中间一层是"虚拟细胞"框架**：其目标不是表征本身，而是对扰动响应、细胞状态转移或未见条件下的细胞行为做预测与生成，涵盖 Perturb-seq 响应预测、化学扰动建模、空间-分子联合预测等任务[12][13]。**最外一层是支撑上述两者的数据资源与评测基础设施**：Tahoe-100M 等大规模扰动图谱[14]、Human Cell Atlas 的图谱整合愿景[15]，以及 scIB[16]、PerturBench[17]、VCBench[18] 等基准。三者共同构成方向边界：**只有模型、没有扰动或状态预测任务的，属于表征学习；只有预测、没有可复用权重或基准的，属于应用案例；两者均被排除在本方向之外。**

演化脉络上，该方向经历了从"图谱构建"到"预训练表征"再到"扰动预测与虚拟细胞"的重心迁移。早期 Perturb-seq 与 CROP-seq 把扰动读出从简单表型扩展到全转录组[19][20]，基因组规模 Perturb-seq 进一步把扰动数量推到数千个功能缺失[21]，为监督学习提供了数据基础。随后 scGPT 与 Geneformer 确立"预训练+微调"范式[2][3]，CellFM 把规模推到 1 亿人类细胞[4]，scPRINT-2 与 TranscriptFormer 则扩展到多物种、跨进化尺度[5][6]。与此同时，虚拟细胞从概念走向可执行框架：AIVC 愿景提出预测、生成、可查询三大能力[12]，虚拟细胞挑战赛提供开放循环基准[13]，SCALE、STRAND、Chreode 等生成式传输模型则直接处理对照—处理非配对这一实验现实[22][23][24]。**这条脉络的核心张力在于：预训练规模是否真的转化为扰动预测能力，还是仅仅在分布内基准上制造了 SOTA 假象。**

核心问题可归纳为四组。**第一，表征是否携带调控逻辑。** 稀疏自编码器分析显示模型内化了有组织的生物学知识，但仅 6.2% 转录因子显示调控靶标特异性响应[25]；因果电路追踪发现约 53% 生物一致性、65–89% 抑制主导，但 CRISPRi 验证方向准确率仅 56.4%[26]；注意力边分数对扰动预测无增量价值，平凡基因级基线 AUROC 0.81–0.88 优于注意力边的 0.70[27]。**第二，预训练收益是否稳健。** 零样本评估中 HVG 在所有指标上优于 Geneformer 和 scGPT[7]；参数无关的线性流程在多个基准取得 SOTA 或近 SOTA，并在分布外任务上超越基础模型[28]；扰动预测中 Train Mean 基线优于 scGPT 与 scFoundation，结合 GO 特征的随机森林最佳[10]。**第三，基准是否有效。** scContam 发现 PBMC 3k 与胰腺胰岛图谱分别有 80.4% 和 77.0% 的细胞指纹 p<0.05，提示高引用基准上的零样本成绩可能反映预训练暴露而非真实泛化[29]；Perturb-seq 基准数据集扰动特异性方差偏低，评估价值本身有限[10]。**第四，多模态与空间预测的目标应锚定何处。** CellWorld 主张从基因测量转向潜在细胞表征，以避免复制测定特异技术变异[30]；PAST 与 OmiCLIP 则依赖配对的组织学与 Visium 数据，泛化性尚待验证[31][32]。

从证据分布看，该方向已形成若干相对稳固的共识与若干未决争议。**共识方面**：多模态整合需要显式建模模态缺失与不确定性[33]；空间映射可统一为最优传输问题并在图谱规模上高效求解[34]；扰动响应高度依赖细胞背景，调控因子及所控基因程序随刺激条件大幅变化[35]。**争议方面**：模型内部是否含可用调控逻辑，一方从 scGPT 提取出紧凑造血算法并取得优于探针的伪时间排序[36]，另一方多项证据指向调控逻辑编码极少[25][26]；GRN 推断上，有工作指出重建式预训练未显式捕获调控信号、零样本方法有时不及随机预测[37]，而统一基准在严格零样本下发现 scGPT token 嵌入相似度在 STRING 和 ChIP-seq 上超越经典基线[38]。**这些分歧的根源，部分在于评测口径不统一：模型多在留出基准上报告 SOTA，而可信虚拟细胞路线图要求的是超越分布内的生物学泛化与实验验证[39]。**

面向未来，该方向的边界正在向三个方向扩展。**一是从转录组向多尺度、多模态延伸**：PTM-Mamba 把蛋白修饰纳入序列建模[40]，mSTAR 整合病理切片、报告与基因表达[41]，CellPaint-POSH 把 Cell Painting 与 pooled 光学 CRISPR 筛选结合[42]。**二是从静态图谱向扰动与动力学延伸**：Perturb-FISH 在空间背景下同时解码扰动与转录组[43]，SCALE 与 STRAND 处理非配对对照—处理传输[22][23]，Chreode 用一步式世界模型预测状态转移[24]。**三是从模型规模向评测与可复现基础设施延伸**：BioLLM 以统一 API 集成多个模型[44]，JUMP-lite 把 115 TB 压缩为 92.0 GB 子集[45]，ST 数据集跨六种组织类型建立准确度、精密度、重复性等指标[46]。**这些扩展共同指向一个尚未被充分回答的问题：在何种条件下，基础模型的预训练表征能稳定转化为对未见扰动、未见细胞类型与未见模态的可靠预测——而这正是虚拟细胞从概念走向决策相关工具的关键门槛[39]。**

## 2 方法学


### 2.1 单细胞基础模型

单细胞基础模型的核心思路，是把语言模型里“词组成句子”的类比搬到细胞上：**细胞类比句子、基因类比词元**，通过大规模自监督预训练获得通用表征，再适配注释、整合、扰动预测等下游任务[1]。早期代表性工作沿两条路径展开。**scGPT** 用生成式预训练 Transformer 在超 **3300 万个细胞**的单细胞 RNA 测序数据上训练，迁移学习后在注释、多批次/多组学整合、扰动预测和基因网络推断等任务上表现优异[2]；**Geneformer** 则在约 **3000 万个**单细胞转录组上以自监督方式学习网络动力学，把网络层级编码进注意力权重，微调后在染色质与网络动力学任务中持续提升准确率，并在有限患者数据下识别出心肌病候选治疗靶点[3]。两者都把“预训练+微调”确立为主流范式，但 Geneformer 的作者也指出，这类模型依赖大规模转录组数据，在数据有限场景仍受限[3]。

随后的工作沿数据规模、架构与任务目标分化。**CellFM** 把预训练规模推到 **1 亿人类细胞**，系统收集并标准化公共 scRNA-seq 数据，在多种下游任务上达到或超过 Geneformer、scGPT、scFoundation、UCE 等模型，验证了单物种超大规模预训练的潜力，但其局限在于仅覆盖人类单物种，数据清洗与批次异质性仍影响泛化[4]。**scPRINT-2** 进一步扩展到 **3.5 亿细胞、16 个物种**，通过改进预训练任务、tokenization 和损失函数并采用细胞级架构，在表达去噪、细胞嵌入和细胞类型预测上达到 SOTA，还具备表达插补与反事实推理的生成能力，并可泛化到未见模态和物种[5]。**TranscriptFormer** 则强调跨物种与进化尺度，在多达 **1.12 亿细胞、12 个物种、跨越 15.3 亿年进化**的数据上联合建模基因身份与表达水平，在分布内与分布外细胞类型分类上达 SOTA，可零样本识别疾病状态并跨物种转移注释，发育轨迹与系统发育关系自然涌现[6]。**Speciesformer** 同样走跨物种生成路线，在包含 **1.31 亿细胞**的 SpeciesCorpus 上预训练，目标是学习可迁移的细胞状态与状态转变，并区分保守生物学原理与物种、组织及细胞环境特异变异，但该工作仅提供摘要信息，缺少代码、权重、数据公开情况和定量基准结果[47]。

架构层面的另一条主线是引入生物学先验与新的序列建模机制。**RegFormer** 把基因调控网络（GRN）先验与 Mamba 状态空间架构结合，用值嵌入和 token 嵌入的双重嵌入编码每个基因，在 **2500 万人类细胞**上做 GRN 引导的生成式预训练，在细胞注释、GRN 重建、遗传扰动预测和药物响应建模等基准上持续优于 scGPT 和 Geneformer；其动机正是针对 Transformer 在长基因序列上的可扩展性与上下文长度限制，以及序列模型难以捕捉长程依赖和层级结构的问题[48]。**scDifformer** 面向虚拟细胞建模，采用掩码语言模型预训练、扩散驱动后训练和下游微调的三阶段设计，在 7 个组织和多项独立研究中提升跨数据集表现，扩散模块在强批次效应下持续带来增益，细胞类型注释达到 SOTA，并可恢复关键 marker 基因、功能通路和跨组织分化轨迹，以及完成空间转录组 spot 去卷积[49]。与之相关的还有样本级异质性建模：**MrVI** 用层次深度生成模型和交叉注意力建模样本协变量效应，无需先验聚类即可识别样本分组，实现高分辨无注释差异表达与丰度分析并控制批次，整合性能领先，已在 scvi-tools 中提供[50]。

并非所有工作都依赖大规模表达数据预训练。**GenePT** 提出一条更简单的替代路线：用 GPT-3.5 基于 NCBI 基因文本描述生成基因嵌入，再通过表达加权平均或按表达排序的基因名句子嵌入生成单细胞嵌入，无需数据策展与额外预训练，在基因属性与细胞类型分类等下游任务上达到与 Geneformer、scGPT 相当甚至更优的性能；其局限是依赖文献文本质量，且未充分利用表达数据本身[51]。在细胞图谱检索方向，**SCimilarity** 用深度度量学习同时优化监督三元组损失和无监督重构损失，学习低维表征使相似细胞靠近。较早的预印本版本在 **2270 万细胞、399 项研究**上训练，验证了跨组织查询能力，发现最初在间质性肺病中识别的巨噬细胞亚群也存在于其他纤维化疾病、组织和 3D 水凝胶系统中[52]；后续正式发表版本报告了 **2340 万细胞、412 项研究、56 训练/15 测试数据集**的规模，在查询敏感性和整合性能间取得最佳平衡（**β=0.001**），支持跨器官、系统、条件的可扩展细胞搜索，但依赖 Cell Ontology 注释质量，部分细胞类型关系模糊[11]。

对上述模型的严格评估揭示了明显争议。**零样本评估**发现，Geneformer 和 scGPT 在 5 个多样单细胞数据集（如 Pancreas 16k、PBMC 12k）上的细胞类型聚类和批次校正表现，多数情况下不如 HVG、Harmony、scVI 等更简单的基线；HVG 在所有指标上优于二者，scGPT 仅在 PBMC 12k 上部分优于 scVI/Harmony[7]。这一结果与前述模型在微调后表现优异的报告形成张力，提示预训练收益高度依赖是否允许微调以及评估设定。另一项针对预训练数据规模与多样性的研究，用 **2220 万细胞**语料预训练 **400 个模型**并开展 **6400 次实验**，覆盖零样本与微调任务，发现性能在数据规模远小于当前训练语料时即趋于平台，且**未观察到明确的数据缩放定律**，因而建议平衡模型容量、数据规模与算力，而非单纯扩大语料[8]。这与 CellFM、scPRINT-2 等以“更大数据带来更强性能”为卖点的工作构成直接对照。

表征提取方式本身也受到质疑。一项逐层评估对 **scFoundation（100M 参数）**和 **Tahoe-X1（1.3B 参数）**在轨迹推断与扰动响应预测上系统比较各层嵌入，发现最优层依赖任务与细胞情境：轨迹任务在 **60% 深度**达峰，比最终层高 **31%**；扰动最优层随 T 细胞激活状态在 **0–96%** 间大幅漂移，静息细胞反而首层最佳[9]。这直接挑战了当前基准“普遍提取最终层嵌入”的默认做法，也说明模型内部表征的可用性不能仅由最终层代表。该研究自身也承认仅评估两个模型、两类任务，未涵盖更多模型与生物场景[9]。

除细胞层面的基础模型外，相关证据还延伸到蛋白与修饰层面。**PTM-Mamba** 是 PTM 感知的蛋白语言模型，基于双向 Mamba 块并以门控机制融合 ESM-2 与 PTM 嵌入，用 **79,707 条**修饰序列（源自 **311,350 条** Swiss-Prot PTM 记录）训练，相比 PTM-Transformer 收敛更快，能区分并相关表示修饰与未修饰序列，但依赖 ESM-2 嵌入，PTM 类型与序列长度覆盖有限[40]。这一方向与单细胞基础模型共享序列建模与预训练思路，但研究对象从细胞转向蛋白修饰，提示“基础模型+虚拟细胞”生态正在向多模态、多尺度扩展。

### 2.2 空间与多模态模型

空间与多模态基础模型的核心张力在于：预测目标应锚定在观测到的分子测量上，还是转向更抽象的细胞表征。现有空间转录组基础模型多重建被掩码的基因身份或表达值，这可能促使模型复制测定特异的技术变异，限制表征迁移性；**CellWorld** 因此把预测目标从观测基因测量改为潜在细胞表征，用空间 Transformer 建模细胞交互，以可见上下文加部分表达提示预测被掩码细胞的潜在表征，预训练 4 个变体（5.74M–94.56M 参数），其中 **CellWorld-Small（5.74M）在全部 11 个线性探针和 7 个空间基准上超越所有基线**，仅用 5% 语料的冻结 Large 模型在 7 个空间基准上超越全部微调基线 [30]。该工作还指出，空间迁移更依赖生物来源多样性与充分优化，而非细胞数量，且细胞级目标歧义需部分表达提示 [30]。

在病理图像与空间转录组的跨模态对齐上，**PAST** 联合编码细胞形态与基因表达，在 2000 万配对病理图像与单细胞转录组上训练，学习统一跨模态表征，支持单细胞基因表达预测、虚拟分子染色和多模态生存分析，并在多种癌症和下游任务中持续超越现有方法 [31]。**OmiCLIP** 则用双编码器与 CLIP 对比学习，把转录组数据转为“基因句子”，基于 ST-bank 的 220 万组织 patch（1007 样本、32 器官）对齐图像与基因表示，配套 Loki 平台提供组织对齐、注释、细胞分解、检索与基因表达预测五项功能，在对比 22 种 SOTA 方法时表现一致准确稳健 [32]。两者都依赖配对的组织学与 Visium 数据，泛化性尚待验证 [arxiv:2507.06418, doi:10.1038/s41592-025-02707-1]。全切片尺度上，**mSTAR** 同时纳入病理切片、专家报告和基因表达三种模态，采用两阶段预训练（先切片级对比学习训练聚合器，再把全切片上下文注入 patch 特征提取器），在 15 类 97 项任务中表现优异，并显示多模态预训练可用更少数据达到竞争性能 [41]。与之相对，病理自监督基础模型的临床基准评测系统比较了 CTransPath、Phikon、UNI、Virchow 等模型的参数量、算法与训练数据，指出数字病理数据缺乏与 WSI 算力需求是主要瓶颈 [53]。

单细胞多模态整合走的是另一条技术路线。**MultiVI** 用深度生成模型（VAE 分别建模基因表达与染色质可及性，通过惩罚对齐潜空间，并模块化扩展至表面蛋白）整合多模态与单模态数据，提供校准的不确定性估计，能准确估计缺失模态的差异表达/可及性，并在相关群体存在时实现样本外预测 [33]。**CLM-X** 则基于多路 Transformer 与统一 token 化、分阶段掩码重建预训练，在百万级单模态与多模态数据上支持 RNA-only、ATAC-only 和配对 RNA-ATAC 输入，在五个下游任务和 10 个数据集上持续超越现有多模态方法与单模态基础模型，RNA-ATAC 跨模态翻译和扰动预测优势明显 [54]。在时空映射任务上，**moscot** 把生物映射统一为 W、GW 或 FGW 型最优传输问题，支持多模态与图谱规模数据，在 170 万细胞小鼠胚胎等数据中实现高效对齐，计算时间与内存较既往 OT 工具降数个数量级，并实验验证 NEUROD2 调控 epsilon 细胞形成 [34]。

多模态图谱与平台评测为上述模型提供了数据与真值基础。阿尔茨海默病整合多模态细胞图谱对 84 名供体颞中回开展定量神经病理、snRNA-seq、snATAC-seq、snMultiome 与 MERFISH，识别出 139 种分子细胞类型，并发现疾病分两阶段：早期为炎症小胶质、反应性星形胶质、SST+ 抑制性神经元丢失与 OPC 再髓鞘，晚期病理指数增长并丢失兴奋性神经元及 Pvalb+、Vip+ 亚型；该队列以老年供体为主、为横断面设计，难以确定因果时序 [55]。平台层面，一项系统评测采集结肠腺癌、肝细胞癌和卵巢癌连续切片，用 CODEX 蛋白和 scRNA-seq 作真值，统一比较 Stereo-seq v1.3、Visium HD FFPE、CosMx 6K、Xenium 5K 四个亚细胞分辨率平台，发现各平台在灵敏度、扩散控制、细胞分割、注释、空间聚类及转录本-蛋白对齐上差异显著，但结论受限于仅 3 种肿瘤、4 个平台 [56]。更早的 **Cell Painting** 综述则记录了 2013 年提出的显微细胞标记检测经协议优化、特征提取与批次校正改进后，可捕获细胞对扰动的响应并用于解析化合物作用机制与毒性，其进一步发展需计算与实验技术进步及多组学整合 [57]。

### 2.3 扰动响应与虚拟细胞

扰动响应预测正从静态的对照—处理映射，转向以基础模型和生成式传输为核心建模范式。早期工作确立了数据基础：**Perturb-seq** 将单细胞RNA-seq与CRISPR扰动结合，在约20万个免疫细胞和细胞系中识别扰动靶点、基因signature、细胞状态与遗传互作 [19]；同期另一项Perturb-seq工作以单基因与组合扰动解剖未折叠蛋白反应，经两个全基因组CRISPRi筛选鉴定约100个命中基因，解耦三条UPR分支 [58]；**CROP-seq** 则把gRNA盒插入慢病毒3'LTR使其成为可检测的mRNA，实现池化筛选的单细胞转录组读出，并验证gRNA插入不影响病毒功能、编辑效率与LentiGuide-Puro高度相似 [20]。这些平台共同把扰动响应的读出从简单表型扩展到全转录组。

在化学扰动方向，**PRnet** 以SMILES与剂量构建扰动嵌入，结合未扰动表达谱生成响应分布，在新化合物、通路和细胞系预测上优于替代方法，并实验验证小细胞肺癌与结直肠癌候选化合物，构建覆盖88细胞系、52组织的扰动图谱，为233种疾病推荐药物 [59]。**PerturbNet** 同样面向未见化学与遗传扰动，强调预测细胞状态分布变化而非仅均值，其对比基线包括scGen、CPA、chemCPA、GEARS、Biolord [60]。两者都受制于扰动空间巨大、跨细胞类型与组合扰动泛化受限这一共同瓶颈。

基础模型路线试图用预训练规模缓解数据稀缺。**Tahoe-x1（Tx1）** 系列参数规模最高30亿，在含Tahoe-100M扰动图谱的大规模单细胞转录组上预训练，采用含药物token的掩码表达生成目标，在基因必需性、癌症标志基因、细胞类型分类和留出情境扰动响应预测四项基准上均达SOTA，计算效率较先前细胞状态模型提升3–30倍 [61]。另一项工作则对Tahoe-x1做药物条件适配器微调，仅训练不到1%参数，在所有泛化设置下达SOTA，尤其在新细胞系少样本与零样本泛化上显著优于基线，但其扰动数据仅覆盖数百分子、少数细胞系 [62]。值得注意的是，**跨模态继续预训练**对参数缩放提出了反例：在来自440项质谱研究的48,843个蛋白质组样本上训练70M参数Tahoe-x1仅一个epoch，就在多数原评测基准上匹配或超过1B和3B参数RNA-only模型，并提升对held-out蛋白扰动基准的迁移，而RNA-only缩放无同等收益 [63]。

生成式传输模型进一步处理对照与处理细胞非配对这一实验现实。**SCALE** 将细胞视为无序集合，用共享集合感知编码器与条件DiT学习潜在传输，无需细胞级匹配，在CRISPR七项指标上全面超越竞争方法并保持基因靶表征分离，其预测的细胞因子差异经三供体PBMC实验验证 [22]。**STRAND** 则针对基因级模型把同一基因不同位点扰动坍缩为同一表征的问题，以扰动位点调控DNA序列编码为条件参数化条件传输，在K562、Jurkat、RPE1上低样本判别分提升达33%，未见基因基准最佳平均排名，新细胞系迁移Pearson提升达0.14，基因组覆盖从约1.5%扩至约95% [23]。**Chreode** 走一步式世界模型路线，用结构化残差转移算子预测动作条件下的状态转移，将分布演化从推理时移至训练时，在240万细胞小鼠胚胎图谱上预训练，作为GEARS可迁移嵌入将Norman Perturb-seq的DE20 MSE从0.2121降至0.1858（相对提升12.4%）[24]。三者对监督信号的假设不同：SCALE明确指出现有分布级学习对扰动特异性监督弱、细胞级配对假设实验不成立 [22]，而STRAND与Chreode则分别以序列条件和时间动力学补充监督来源。

多模态与可解释推理是另一条并行线索。**AROMA** 整合文本证据、图拓扑与蛋白序列特征建模扰动—靶依赖，构建两个知识图谱与PerturbReason数据集（>498k样本），在多细胞系超越现有方法，未见细胞系零样本与知识稀疏长尾场景下保持稳健，但依赖知识图谱与检索质量 [64]。**UNAGI** 基于VAE-GAN从疾病时间序列单细胞数据解析细胞动力学并做计算机药物筛选，整合疾病特异基因调控信息与CMAP药物数据库，对比Seurat、SCANPY、scVI、scGPT、GEARS等 [65]。**细胞行为假设语法**则把自然语言细胞规则一一映射为数学方程以构建可解释agent-based模型，案例覆盖肿瘤生长、侵袭、免疫治疗与脑发育，但依赖标注细胞状态与规则质量 [66]。

数据规模与生物学语境的重要性在两项大规模扰动研究中凸显。一项工作对4名供体、2200万原代人CD4+ T细胞扰动所有表达基因，在静息与刺激态测量转录组效应，发现调控因子及所控基因程序随刺激条件大幅变化，并提名极化与衰老表型调控因子、关联自身免疫病风险，其局限在于仅4名供体、原代T细胞与体外刺激条件 [35]。这提示扰动响应高度依赖细胞背景，与前述模型在未见细胞系上的泛化诉求形成张力。

领域层面的共识与争议集中在评估标准。**AI虚拟细胞（AIVC）** 愿景主张多尺度多模态大神经网络从数据直接学习细胞行为，提出预测、生成、可查询三大能力，并指出多尺度建模、海量互作组件与非线性动力学挑战 [12]。**虚拟细胞挑战赛**作为开放循环基准，提供评估框架与专用数据集以加速模型开发 [13]。但可信虚拟细胞路线图批评当前工作偏重模型规模与数据量，指出静态图谱、仅转录组读出与分布内基准不足以预测新条件下的细胞行为，主张评估应转向泛化到未见细胞类型与扰动，并建立分子状态、干预、生物背景、正交表型四层经验框架 [39]。临床前转化综述同样强调从计算评估到CRISPR和类器官实验验证的闭环，并指出监管接受、数据隐私与模型可解释性仍是障碍 [67]。这些框架性主张与前述模型各自报告的SOTA结果之间存在评价口径差异：模型多在留出基准上取胜，而路线图要求的是超越分布内的生物学泛化与实验验证。

### 2.4 机制可解释性与表征分析

机制可解释性研究目前主要沿两条路径展开：一是用稀疏自编码器（SAE）分解模型激活，二是直接检验注意力与电路结构。对Geneformer V2-316M（18层，d=1152）与scGPT全人模型（12层，d=512）各层残差流训练TopK SAE，分别生成**82525与24527个特征**，其中**99.8%的特征SVD不可见**，29–59%可注释到通路；但仅3/48（6.2%）转录因子显示调控靶标特异性，多组织对照下为10.4%[25]。在三个模型（scGPT、scFoundation、Geneformer）隐藏表示上训练的SAE则揭示出多样生物与技术信号，且不同训练协议与架构的编码方式不同；这些特征可干预——抑制批次特征改善整合并保留生物信号，激活药物特征使对照细胞浓度依赖地向药物扰动状态转变[68]。

对注意力与电路的系统检验给出了更悲观的结论。一个包含37项分析、153个统计检验的框架应用于scGPT与Geneformer后发现，注意力模式虽编码分层生物结构（早期层蛋白互作、晚期层转录调控），但对扰动预测无增量价值：**平凡基因级基线AUROC 0.81–0.88，优于注意力/相关性边的0.70**，成对边分数零增量，消融调控头无退化，而CSSI可将GRN恢复提升至多1.85×[27]。因果电路追踪（消融SAE特征测下游响应，96,892条边、80,191次前向）显示两模型约53%生物一致性、**65–89%抑制主导**，且不随架构与细胞类型变化，跨模型共识1,142域对（10.6倍富集）；但CRISPRi基因级验证方向准确率仅56.4%，提示编码的是共表达而非因果调控[26]。对Geneformer的穷举电路追踪（L5层全部4065个SAE特征）得到1,393,850条显著下游边，较选择性采样扩27倍，三阶冗余比0.59对配对0.74且零协同，并发现重尾枢纽分布（1.8%特征占大量连接，40%顶级枢纽无注释）与层位置决定分化方向性（L17特征100%推向成熟，L0/L11为0.00–0.58）[69]。

争议与分歧集中在「模型内部是否含可用调控逻辑」。一方面，从scGPT中提取出紧凑造血算法，伪时间深度排序|ρ|=0.439优于次优0.331，CD4/CD8 AUROC 0.867、单核/巨噬0.951，比MLP探针快34.5倍、参数少约1000倍，被视为首个经机制可解释性提取的可用算法[36]；另一方面，多项证据指向调控逻辑编码极少[25][26]。针对GRN推断，有工作指出重建式预训练未显式捕获调控信号，现有零样本方法有时不及随机预测，并提出GRN泛化基准与虚拟值扰动、梯度轨迹蒸馏，从冻结scFM中提取可泛化基因间特征[37]。

### 2.5 形态与图像表型基础模型

图像表型基础模型的核心问题之一，是如何把高维显微图像转成能保留生物学关系的表征。一项工作开发了 **CellPaint-POSH** 平台，将 Cell Painting 与 pooled 光学 CRISPR 筛选、自监督深度学习结合，在 **163,090 个单细胞**、Cell Painting 图像加 4 色 ISS 数据上实现无偏的基因功能推断；其自监督机器学习特征预测性能高于经典图像分析与专家形态特征，形态表型可按已知功能聚类基因，并在无通路报告基因时揭示基因关联网络 [42]。该平台需改造 Cell Painting 以兼容 ISS（如将线粒体染色替换为 RNA 探针 Mitoprobe、加入 RNase 抑制剂并提前逆转录），依赖成像与测序流程优化 [42]。

特征空间本身是否可靠，则是另一条独立的方法学线索。有研究在 U2OS JUMP-MOA 参考板的 **90 个化合物**上，以零样本方式对比 CellPaintSSL、OpenPhenom、uniDINO 三种预训练模型，用 copairs 的 mAP 框架评估活性、区分度与 MOA 恢复：活性阳性分别为 CellPaintSSL **85/90**、OpenPhenom **81/90**、uniDINO **82/90**，三者数量相近，但 CellPaintSSL 的活性检索质量显著高于另两者（p<0.0001），MOA 注释恢复仅部分实现且因模型而异 [70]。该研究仅基于单一 U2OS 参考板，MOA 恢复不完整且模型间不一致，说明前提性质量并不保证目标生物学关系的恢复 [70]。与之呼应，一篇综述指出深度学习表征常优于手工特征，如 CLOOME 零样本 MoA top-10 准确率 **61.3%** 对比 CellProfiler **24.5%**，但部分场景手工特征仍具竞争力，且时序与 3D 数据方法、质控标准及特征解释仍不成熟 [71]。

## 3 数据与资源

单细胞扰动图谱的构建正从单一细胞系、有限扰动规模走向基因组规模与多模态整合。**基因组规模Perturb-seq** 在K562与RPE1细胞系中以多重CRISPRi加scRNA-seq测定数千个功能缺失扰动，覆盖超过250万人类细胞，用于绘制基因型-表型图谱并研究RNA剪接、分化、染色体不稳定等复杂表型，其局限在于仅两个细胞系、CRISPRi为敲低而非敲除、表型限于转录组 [21]。与之互补，基于高维单细胞表型构建的细胞状态流形框架将每个扰动与遗传互作投射到流形特定位置，实现调控通路无偏排序与遗传互作的系统分类，但依赖强遗传互作筛选，未覆盖全基因组互作 [72]。在空间维度上，**Perturb-FISH** 将MERFISH与gRNA原位扩增结合，在LPS刺激巨噬细胞中与匹配的Perturb-seq比较验证敲除效应一致性，并揭示细胞密度与邻居扰动的影响，还结合钙成像用于ASD风险基因CRISPRi筛选并在肿瘤异种移植3D组织中验证，其限制是gRNA仅20bp、无法如mRNA般平铺而需原位扩增 [43]。

大规模资源方面，**Tahoe-100M** 覆盖超过1亿细胞、50个人类细胞系与379种化合物，采用3D球状体混合细胞系、24小时三剂量处理及组合条形码池化测序，覆盖约56,000个细胞系-药物-剂量组合，报告了Dabrafenib在非BRAF依赖细胞系中的意外敏感性以及CDK抑制剂引起G1或G2/M阻滞，其对照是受批次效应与实验变异限制的传统扰动研究，但摘要未提供模型训练与验证细节 [14]。在组织尺度上，全小鼠脑MERFISH图谱对约800万细胞成像超过1100个基因并整合scRNA-seq，鉴定出超过5000个转录簇与约300个主要细胞类型，注册到小鼠脑共坐标框架以量化各脑区细胞组成并识别空间模块，局限在于仅限小鼠脑且基因面板有限、需整合scRNA-seq [73]。面向基础模型，Human Cell Atlas相关工作提出细胞图谱作为细胞普查、3D图谱、基因型-表型连接、4D发育图谱及生物学基础模型五种用途，指向从数据收集向图谱整合与统一基础模型的演进 [15]。

## 4 应用与结果

单细胞与空间图谱已能以高分辨率刻画健康与病变肝脏，涵盖肝小叶肝细胞分区、纤维化巨噬细胞-星状细胞生态位、胆管细胞反应、免疫重塑及肝细胞癌生态系统，但这些图谱本身只能显示细胞状态出现的位置，无法预测肝损伤是否会进展，也无法预测肝脏对未经测试的药物、毒物或遗传扰动的响应 [74]。针对这一缺口，该综述将面向肝脏的 **AI 虚拟细胞（AIVC）** 建模路线归纳为三类互补方向：生成模型、动力学/运输模型，以及预训练/基础模型，并以扰动响应预测作为跨层评估任务 [74]。

在证据分层上，现有工作被梳理为直接肝脏验证、含肝脏基准、通用单细胞证据和概念应用四类 [74]。其核心结论是：已发表模型仅展示了单个组件（图谱整合、轨迹推断、可迁移表示、回顾性响应程序），**尚无经过前瞻验证的肝脏模拟器** [74]。因此该综述提出，评估需覆盖供体、病因、分期和平台等维度，以检验模型在不同条件下的可迁移性 [74]。

## 5 评测、可复现性与争议

单细胞基础模型的评测正从单一任务排行榜转向对**泛化性**与**基准有效性**的审计。scContam 对四个 scIB 基准和三个 scFM 做逐细胞预训练污染审计，发现 PBMC 3k 与胰腺胰岛图谱分别有 **80.4%** 和 **77.0%** 的细胞指纹 p<0.05，而截断后的 AIDA v2 与 Tahoe-100M 为 0%；MIA AUROC 随模型容量数据比从 0.494 升至 0.690 再到 0.881 [29]。这意味着高引用基准上的零样本成绩可能反映预训练暴露而非真实泛化，且生产级 scFM 抗实例记忆、分布污染需单独检测 [29]。

在扰动响应预测这一虚拟细胞核心任务上，多项独立评测一致对基础模型提出质疑。在四个 Perturb-seq 数据集上，差分空间的 Train Mean 基线（0.711/0.557/0.373/0.628）优于 scGPT（0.641/0.554/0.327/0.596）与 scFoundation（0.552/0.459/0.269/0.471），而结合 GO 特征的随机森林最佳（0.739/0.586/0.480/0.648）[10]。另一项在 K562 CRISPRa、224 个扰动、19,264 个基因上的评测中，scGPT、scFoundation、GEARS、CPA 的误差均高于加性基线，遗传互作预测不优于 no change 基线 [75]。PertEval-scFM 同样发现零样本 scFM 嵌入未持续优于基线，尤其在分布偏移下 [76]。这些结论与 PerturBench 的观察相呼应：广泛使用模型存在模式崩溃，秩指标可补充 RMSE，且无单一架构明显占优、简单架构随数据规模扩展良好 [17]。不过 scArchon 指出，现有 Perturb-seq 基准数据集扰动特异性方差偏低，评估价值本身有限 [10]，而 scArchon 以容器化流程统一 MSE、Wasserstein 及生物指标并聚合排名，支持用户自有数据 [77]。

跨任务、跨模态的统一评测进一步显示性能高度依赖上下文。一项统一框架评测 Nicheformer、CellPLM、scGPT-spatial、GenePT、scELMo、Novae 六个模型，覆盖 scRNA-seq、空间转录组与 Perturb-seq，结论是**无模型全面领先**：表达训练的细胞级 Transformer 擅长细胞身份，空间/图模型保留组织结构，语言嵌入在部分扰动指标有竞争力，排名随模态、预处理、token 化、生物先验、域偏移和指标变化 [78]。零样本评测 scGPT、SCimilarity、UCE、Transcriptformer 四项任务时，细胞类型注释中基线在多数数据集最强，蛋白表达预测中基础模型更准（SCimilarity 误差最低、Transcriptformer 相关性最高），数据整合中基础模型中等而 scVI 更佳 [79]。VCBench 将四个虚拟细胞框架综合为七个能力维度，在五个可测维度上用预注册线性/最近邻基线评测 Geneformer、scGPT、UCE、TranscriptFormer、Arc State，发现**基线在 5 维中 4 维追平或超越所有基础模型**，仅 TranscriptFormer 在 RNA 到蛋白预测上超最强基线 53% Pearson；多尺度整合与 in silico 实验两维度结构上无法端到端测试 [18]。

低监督条件下的结论同样呈任务依赖性。七种基础模型与三种经典表示对比中，CellPLM 在聚类、注释、批次校正领先，scMulan 在扰动预测领先，PCA 在表达重建领先；7 个基础模型中仅 1 个聚类超过最强经典基线，3 个批次校正、4 个注释、0 个重建、6 个扰动预测超过基线，且跨模型基因关系一致性未超过维度匹配随机投影零假设 [80]。细胞类型分类的系统评测则给出更分化的结果：scFoundation 持续最佳，Geneformer 表现差甚至不如基线 [81]；而生物学驱动的零样本评测承认嵌入确实捕捉生物学信息，但预训练模型在部分场景未超越 HVG、Seurat、Harmony、scVI 等简单基线 [82]。参数无关的线性流程在多个基准取得 SOTA 或近 SOTA，并在新细胞类型与未见物种的分布外任务上超越基础模型 [28]。

评测方法本身也在被重新设计。一项无监督框架基于表征应在模拟技术与采样扰动下保持邻域结构的原则，测试 5 个 scFM、PCA 基线与 39 个数据集，发现标准基准判定近乎等价的模型在丢弃 5% 计数时局部邻域保持差异近 2 倍，且该不稳定性具尺度依赖性并被视觉连贯的嵌入掩盖 [83]。可解释性方面，两层评估框架在两种架构、四种细胞类型、两种扰动模态下做 153 项统计检验与因果消融，发现**注意力边分数相对基因级特征无增量价值**，单变量基线优于注意力和相关边，TRRUST 头因果消融无行为效应 [84]。与之相对，GRN 重建统一基准在严格零样本下发现 scGPT token 嵌入相似度在 STRING 和 ChIP-seq 上超越经典基线，scFoundation 动态转移表现最强 [38]——两者对注意力/嵌入是否携带调控信号给出了不同侧重。

可复现性基础设施被视为缓解碎片化的路径。BioLLM 以统一 API、决策树预处理和 BioTask 执行器集成 scBERT、Geneformer、scFoundation、scGPT 等，针对预处理不一致、接口异构、指标非标准化三大挑战 [44]。JUMP-lite 把 115 TB 的 JUMP Cell Painting 压缩为 **92.0 GB** 子集（约缩小 1,250 倍），配合开源框架 Nahual 对 CellProfiler、MorphEM、OpenPhenom、SubCell、DINOv2 做基准，发现中度压缩基本保留信号 [45]。空间组学侧，ST 数据集跨六种组织类型、三站点在 Xenium 与 CosMx 上建立准确度、精密度、重复性、灵敏度与特异性指标，SpatialQM 开源、STP 门户可实时评估约 3300 万细胞数据 [46]。

基准设计缺陷构成另一类争议。对小分子活性基准的审计发现许多 assay 直接关联细胞健康或毒性，逻辑回归细胞计数 AUC 达 **0.70±0.22**，接近 CLOOME 的 0.71±0.19，细胞计数加 MW 与 logP 达 0.74±0.21；但在 24 个蛋白靶标基准中 Cell Painting 确实优于细胞计数 [85]。这提示部分基准的高分可由平凡信号解释，需过滤此类 assay 并纳入细胞计数基线。扰动预测的泛化性评测也强调，方法选择需谨慎，细胞上下文嵌入对提升跨未见场景的泛化性必要 [86]。综合来看，现有证据的冲突集中在：基础模型在部分任务（蛋白预测、GRN 零样本、动态转移）确有优势，但在扰动预测、注释、整合与重建上频繁不敌简单基线；而污染审计、无监督稳定性评测与基准缺陷审计共同表明，此前报告的领先幅度可能被预训练暴露、任务选择与平凡信号高估。

## 6 空白与趋势

1. **评测口径正在从「留出基准上的 SOTA」转向「分布外泛化与基准有效性审计」，但两者尚未对齐。** 一方面，多项独立评测一致发现基础模型在扰动响应预测上未跑赢简单基线：Train Mean 在四个 Perturb-seq 数据集上优于 scGPT 与 scFoundation，结合 GO 特征的随机森林最佳[10]；在 K562 CRISPRa、224 个扰动上 scGPT、scFoundation、GEARS、CPA 误差均高于加性基线[75]；VCBench 在五个可测维度上发现基线在 4 维追平或超越所有基础模型[18]。另一方面，模型侧仍以留出基准取胜为主要卖点。**这一评价口径差异是当前方向最核心的空白：缺少同时报告分布内成绩、分布外泛化与基线对照的统一协议。** 可信虚拟细胞路线图已明确提出评估应转向泛化到未见细胞类型与扰动[39]，但尚无被广泛采纳的落地标准。

2. **预训练污染审计揭示高引用基准的零样本成绩可能被高估，但污染检测尚未进入常规评测流程。** scContam 发现 PBMC 3k 与胰腺胰岛图谱分别有 **80.4%** 和 **77.0%** 的细胞指纹 p<0.05，而截断后的 AIDA v2 与 Tahoe-100M 为 0%，MIA AUROC 随模型容量数据比从 0.494 升至 0.690 再到 0.881[29]。**这意味着当前大量零样本结论的生物学解释力存疑，而污染审计与基准截断尚未成为领域惯例。** 与之呼应，一项针对预训练数据规模的研究用 2220 万细胞预训练 400 个模型、开展 6400 次实验，**未观察到明确的数据缩放定律**[8]，直接挑战了「更大语料必然更强」的默认假设。

3. **机制可解释性证据正在系统性地质疑「模型内部含可用调控逻辑」，但提取可用算法的尝试同时存在。** 多项独立工作指向同一结论：注意力边分数相对基因级特征无增量价值，平凡基因级基线 AUROC 0.81–0.88 优于注意力/相关性边的 0.70[27]；因果电路追踪显示 CRISPRi 基因级验证方向准确率仅 56.4%，提示编码的是共表达而非因果调控[26]；SAE 图谱显示仅 6.2% 转录因子显示调控靶标特异性响应[25]。**但反向证据同样存在：从 scGPT 中提取的紧凑造血算法在 88 折供体留出基准中取得最强伪时间排序，且比标准探针快 34.5 倍、参数少约 1000 倍[36]。** 这一分歧尚未被调和，**「模型内部知识能否被可靠提取为可执行算法」是明确的未决问题**。

4. **扰动预测正从静态对照—处理映射转向生成式传输与世界模型，但监督信号来源仍是开放设计空间。** SCALE 用集合感知编码器与条件 DiT 学习潜在传输，无需细胞级匹配，CRISPR 七项指标超越竞争方法[22]；STRAND 以扰动位点 DNA 序列为条件，基因组覆盖从约 1.5% 扩至约 95%[23]；Chreode 用一步式结构化残差转移算子，将 Norman Perturb-seq 的 DE20 MSE 从 0.2121 降至 0.1858[24]。**三者的关键差异在于监督信号假设：SCALE 明确指出现有分布级学习对扰动特异性监督弱、细胞级配对假设实验不成立[22]，而 STRAND 与 Chreode 分别以序列条件和时间动力学补充监督。** 尚无工作系统比较这些监督来源在跨细胞类型、跨扰动模态下的相对贡献。

5. **多模态整合的瓶颈正从「能否对齐」转向「对齐后能否泛化到未见条件」，且评测显示无模型全面领先。** PAST 在 2000 万配对病理图像与单细胞转录组上训练，支持虚拟分子染色与多模态生存分析[31]；OmiCLIP 基于 220 万组织 patch 对齐图像与基因句子，在对比 22 种 SOTA 方法时表现稳健[32]；mSTAR 在 97 项临床任务中显示多模态预训练可用更少数据达到竞争性能[41]。**但统一评测框架覆盖 scRNA-seq、空间转录组与 Perturb-seq 后结论是「无模型全面领先」：表达训练的细胞级 Transformer 擅长细胞身份，空间/图模型保留组织结构，语言嵌入在部分扰动指标有竞争力，排名随模态、预处理、token 化、生物先验、域偏移和指标变化[78]。** 跨模态泛化到未见平台、未见组织与未见物种，仍是未被系统检验的方向。

6. **空间与形态基础模型的核心张力在于预测目标锚定观测测量还是抽象表征，且特征空间可靠性本身受到质疑。** CellWorld 把预测目标从基因测量改为潜在细胞表征，CellWorld-Small（5.74M）在全部 11 个线性探针和 7 个空间基准上超越所有基线[30]。**但形态侧的证据显示前提性质量并不保证目标生物学关系恢复：在 U2OS JUMP-MOA 参考板 90 个化合物上，三种预训练模型活性阳性数量相近（85/81/82），但 MOA 注释恢复仅部分实现且因模型而异[70]。** 同时，小分子活性基准审计发现许多 assay 直接关联细胞健康或毒性，逻辑回归细胞计数 AUC 达 0.70±0.22，接近 CLOOME 的 0.71±0.19[85]。**「形态/图像基础模型学到的表征是否对应可解释的生物学机制」与「基准本身是否在测量预期目标」是两个尚未被同时解决的问题。**

7. **可复现性与评测基础设施正在被系统性建设，但覆盖范围与采纳度仍有限。** BioLLM 以统一 API、决策树预处理和 BioTask 执行器集成 scBERT、Geneformer、scFoundation、scGPT 等，针对预处理不一致、接口异构、指标非标准化三大挑战[44]；JUMP-lite 把 115 TB 的 JUMP Cell Painting 压缩为 92.0 GB 子集（约缩小 1,250 倍），发现中度压缩基本保留信号[45]；空间组学侧 ST 数据集跨六种组织类型、三站点在 Xenium 与 CosMx 上建立五项指标，SpatialQM 开源、STP 门户可实时评估约 3300 万细胞数据[46]。**这些基础设施尚未与前述污染审计、分布外泛化评测、机制可解释性检验形成统一流水线，是明确的工程空白。**

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 单细胞基础模型 | 成熟（方法收敛、增量为主） | scGPT [2] 与 Geneformer [3] 已确立"大规模预训练 + 迁移"范式并被广泛复用，后续工作多为架构/数据规模增量；同时 GenePT [51] 用 GPT 文本嵌入在多项任务上逼近专用模型，说明纯预训练架构的边际收益在收窄。 |
| 2.2 空间与多模态模型 | 朝阳（近两年爆发、方法未收敛） | 多模态整合仍有多条并行路线：MultiVI [33] 走深度生成式整合，moscot [34] 走时空最优传输映射，二者目标与假设不同、尚未统一；AD 多模态图谱 [55] 证明大规模多模态数据已可产出 CNS 级结果，但方法层面仍在竞争。 |
| 2.3 扰动响应与虚拟细胞 | 朝阳（近两年爆发、方法未收敛） | 数据侧已规模化：genome-scale Perturb-seq [21] 与 Perturb-seq 原始框架 [19] 提供了从千级到全基因组的扰动标签；愿景侧 Cell 的 virtual cell 路线图 [12] 明确了任务定义，但方法尚未收敛（见 5 节的反证）。 |
| 2.4 机制可解释性与表征分析 | 萌芽（少量探索性工作） | 稀疏自编码器被用于拆解单细胞基础模型特征 [68]，但同期的系统评测 [27] 显示可解释性收益有限、调控信息提取不足，属于刚起步且结论尚不稳定的探索。 |
| 2.5 形态与图像表型基础模型 | 萌芽（少量探索性工作） | Cell Painting 综述 [57] 总结了十年积累但指出基础模型化仍在早期；pooled Cell Painting CRISPR 筛选平台 [42] 与检索式特征空间评测 [70] 显示该方向刚开始建立"扰动—形态"闭环与评测口径。 |
| 3 数据与资源 | 成熟（资源已确立、增量为主） | Human Cell Atlas 从细胞普查走向统一基础模型的路线 [15] 与全小鼠脑空间图谱 [73] 表明图谱类资源已形成稳定产出模式；遗传互作流形 [72] 与全基因组扰动图谱 [21] 说明扰动数据资源也已进入规模化复用阶段。 |
| 4 应用与结果 | 证据不足 | 雷达样本中仅 1 篇（肝病虚拟细胞展望 [74]），不足以判断阶段。 |
| 5 评测、可复现性与争议 | 朝阳（近两年爆发、结论未收敛） | 系统性评测密集出现：深度学习扰动效应预测未跑赢基线 [75]、PerturBench [17]、基础模型单细胞实用性评估 [87] 三篇给出不同任务下的负面/中性结论；而 atlas 整合基准 [16] 是更早的成熟基准，说明评测范式在向扰动/基础模型迁移但尚未定型。 |

**整体判断**：这个方向整体处于**朝阳期偏后段**——单细胞基础模型（2.1）与数据资源（3）已进入**成熟、增量为主**的阶段，而**扰动响应/虚拟细胞（2.3）、空间多模态（2.2）、评测与争议（5）** 仍在爆发且方法未收敛。雷达样本中 **近两年占比 0.74、CNS 占比 0.30**，但**中位引用在 2.3 仅 21、2.4 为 0、2.5 为 6**，说明热度集中在少数旗舰工作，长尾尚未沉淀。**窗口期估计还有 12–24 个月**：一旦扰动预测的评测口径（如 PerturBench 类）稳定下来、且出现能稳定跑赢简单基线的模型，2.3 会迅速从朝阳转入成熟。**最大不确定性**是"预训练是否真的带来可迁移增益"——[75] 与 [87] 的负面结论若被更多任务复现，整个虚拟细胞叙事的技术前提会被削弱；反之若在特定任务（如跨细胞类型扰动外推）上稳定胜出，则会快速固化。另一个不确定性是**多模态对齐的生物学正确性**：MultiVI [33] 与 moscot [34] 的整合结果缺乏统一验证标准。

**接下来怎么做**

1. **用类器官多组学做"扰动外推"的严格评测，而不是再训一个基础模型。** 切入点：拿公共 Perturb-seq 资源 [21] 预训练/微调，在你的类器官多组学数据上做**跨细胞类型、跨时间点的扰动响应外推**，对照简单基线（均值/线性/表达加性）。为什么现在做：[75] 与 [17] 已指出"没跑赢基线"是普遍现象，但缺**类器官/衰老背景**下的证据；你能用合作项目补上这块，产出高影响力负面或正面结论。产出：一个可复现的评测协议 + 公开 demo。

2. **把衰老作为扰动维度切入虚拟细胞。** 切入点：在 Tahoe/CZI 类图谱 [15] 上做**衰老相关基因/通路的扰动响应预测**，用你的衰老单细胞数据做外部验证。为什么现在做：2.3 的方法未收敛 [12]，而衰老这一扰动轴在现有基准中几乎缺席，属于低竞争高相关。产出：衰老扰动响应预测模型 + 外部验证结果。

3. **做多模态整合的"生物学正确性"评测，而非再提一个整合方法。** 切入点：用你的 RNA + 蛋白 + 空间数据，对比 MultiVI [33] 与 moscot [34] 在**已知生物学 ground truth**（如标记基因空间定位、谱系关系）上的表现。为什么现在做：2.2 方法并行未收敛，评测缺口明显；且能直接复用你的合作项目数据。产出：多模态整合的生物学评测基准。

4. **用稀疏自编码器做基础模型表征的机制分析，绑定衰老表型。** 切入点：对 scGPT [2] / Geneformer [3] 的嵌入做 SAE 拆解 [68]，检验提取的特征是否对应衰老相关通路，并用 [27] 的评测框架做对照。为什么现在做：2.4 处于萌芽、结论未定，早期进入容易占位；且与你多模态建模能力匹配。产出：可解释性分析 + 衰老特征提取方法。

5. **把 Cell Painting 形态表型纳入你的多模态栈，做形态—转录组扰动对齐。** 切入点：用 pooled Cell Painting CRISPR 平台 [42] 的公开数据，检验形态特征能否预测转录组扰动响应，并与 [70] 的检索式评测口径对齐。为什么现在做：2.5 萌芽、雷达样本仅 3 篇，竞争少；且形态数据可与你的类器官成像直接结合。产出：形态—转录组扰动对齐的 demo + 评测。

## 参考文献

1. Single-cell foundation models: bringing artificial intelligence into cell biology.. Experimental & molecular medicine 2025. https://doi.org/10.1038/s12276-025-01547-5
2. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. Nature Methods 2024. https://doi.org/10.1038/s41592-024-02201-0
3. Transfer learning enables predictions in network biology. Nature 2023. https://doi.org/10.1038/s41586-023-06139-9
4. CellFM: a large-scale foundation model pre-trained on transcriptomics of 100 million human cells.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59926-5
5. scPRINT-2: Towards the next-generation of cell foundation models and benchmarks.  2025. https://doi.org/10.64898/2025.12.11.693702
6. A Cross-Species Generative Cell Atlas Across 1.5 Billion Years of Evolution: The TranscriptFormer Single-cell Model. bioRxiv 2025. https://doi.org/10.1101/2025.04.25.650731
7. Zero-shot evaluation reveals limitations of single-cell foundation models.. Genome biology 2025. https://doi.org/10.1186/s13059-025-03574-x
8. Evaluating the role of pretraining dataset size and diversity on single-cell foundation model performance.. Nature methods 2026. https://doi.org/10.1038/s41592-026-03120-y
9. Intermediate Layers Encode Optimal Biological Representations in Single-Cell Foundation Models.  2026. https://arxiv.org/abs/2604.14838v1
10. Benchmarking foundation cell models for post-perturbation RNA-seq prediction.. BMC genomics 2025. https://doi.org/10.1186/s12864-025-11600-2
11. A cell atlas foundation model for scalable search of similar human cells.. Nature 2024. https://doi.org/10.1038/s41586-024-08411-y
12. How to build the virtual cell with artificial intelligence: Priorities and opportunities.. Cell 2024. https://doi.org/10.1016/j.cell.2024.11.015
13. Virtual Cell Challenge: Toward a Turing test for the virtual cell.. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.008
14. Abstract 491: A 100 million cell single cell atlas enabling mechanistic and genotype-specific drug response discovery.. Cancer Research 2026. https://doi.org/10.1158/1538-7445.am2026-491
15. The Human Cell Atlas from a cell census to a unified foundation model.. Nature 2024. https://doi.org/10.1038/s41586-024-08338-4
16. Benchmarking atlas-level data integration in single-cell genomics. Nature Methods 2020. https://doi.org/10.1038/s41592-021-01336-8
17. PerturBench: Benchmarking Machine Learning Models for Cellular Perturbation Analysis. Neural Information Processing Systems 2024. https://doi.org/10.48550/arXiv.2408.10609
18. VCBench: A Multi-Dimensional Benchmark for Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.06.18.733146
19. Perturb-seq: Dissecting molecular circuits with scalable single cell RNA profiling of pooled genetic screens. Cell 2016. https://doi.org/10.1016/j.cell.2016.11.038
20. Pooled CRISPR screening with single-cell transcriptome read-out. Nature Methods 2017. https://doi.org/10.1038/nmeth.4177
21. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. bioRxiv 2021. https://doi.org/10.1016/j.cell.2022.05.013
22. SCALE:Scalable Conditional Atlas-Level Endpoint transport for virtual cell perturbation prediction.  2026. https://arxiv.org/abs/2603.17380v3
23. STRAND: Sequence-Conditioned Transport for Single-Cell Perturbations.  2026. https://arxiv.org/abs/2602.10156v1
24. Chreode: A Cell World Model for One-Step Temporal Dynamics and Perturbation Prediction. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.28111
25. Sparse autoencoders reveal organized biological knowledge but minimal regulatory logic in single-cell foundation models: a comparative atlas of Geneformer and scGPT.  2026. https://arxiv.org/abs/2603.02952v1
26. Causal Circuit Tracing Reveals Distinct Computational Architectures in Single-Cell Foundation Models: Inhibitory Dominance, Biological Coherence, and Cross-Model Convergence.  2026. https://arxiv.org/abs/2603.01752v2
27. Systematic Evaluation of Single-Cell Foundation Model Interpretability Reveals Attention Captures Co-Expression Rather Than Unique Regulatory Signal.  2026. https://arxiv.org/abs/2602.17532v1
28. Parameter-free representations outperform single-cell foundation models on downstream benchmarks.  2026. https://arxiv.org/abs/2602.16696v1
29. Auditing pretraining contamination in single-cell foundation model benchmarks.  2026. https://arxiv.org/abs/2607.20572v1
30. CellWorld: From Gene-Level Reconstruction to Latent Cell Prediction in Spatial Transcriptomics Foundation Models.  2026. https://arxiv.org/abs/2608.06659v1
31. PAST: A multimodal single-cell foundation model for histopathology and spatial transcriptomics in cancer. arXiv.org 2025. https://arxiv.org/abs/2507.06418v1
32. A visual-omics foundation model to bridge histopathology with spatial transcriptomics.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02707-1
33. MultiVI: deep generative model for the integration of multimodal data. Nature Methods 2023. https://doi.org/10.1038/s41592-023-01909-9
34. Mapping cells through time and space with moscot.. Nature 2025. https://doi.org/10.1038/s41586-024-08453-2
35. Genome-scale perturb-seq in primary human CD4+ T cells maps context-specific regulators of T cell programs and human immune traits.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.002
36. Discovery of a Hematopoietic Manifold in scGPT Yields a Method for Extracting Performant Algorithms from Biological Foundation Model Internals.  2026. https://arxiv.org/abs/2603.10261v1
37. Towards Universal Gene Regulatory Network Inference: Unlocking Generalizable Regulatory Knowledge in Single-cell Foundation Models.  2026. https://arxiv.org/abs/2605.08128v1
38. Benchmarking Static Gene Regulatory Network Reconstruction and Dynamic Transition Probing in Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.05.17.725083
39. Toward trustworthy virtual cells: a roadmap for perturbation-resolved, context-aware, and experimentally validated cell models. Frontiers in Cell and Developmental Biology 2026. https://doi.org/10.3389/fcell.2026.1900624
40. PTM-Mamba: a PTM-aware protein language model with bidirectional gated Mamba blocks.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02656-9
41. A multimodal knowledge-enhanced whole-slide pathology foundation model.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66220-x
42. A pooled Cell Painting CRISPR screening platform enables de novo inference of gene function by self-supervised deep learning.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66778-6
43. Simultaneous CRISPR screening and spatial transcriptomics reveal intracellular, intercellular, and functional transcriptional circuits.. Cell 2025. https://doi.org/10.1016/j.cell.2025.02.012
44. BioLLM: A standardized framework for integrating and benchmarking single-cell foundation models. bioRxiv 2024. https://doi.org/10.1016/j.patter.2025.101326
45. JUMP-lite: Compact, reproducible benchmarking of cell representations.  2026. https://arxiv.org/abs/2608.07632
46. Standardized metrics for assessment and reproducibility of imaging-based spatial transcriptomics datasets.. Nature biotechnology 2025. https://doi.org/10.1038/s41587-025-02811-9
47. Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling.  . https://doi.org/10.64898/2026.09.22.752128
48. RegFormer: a single-cell foundation model powered by gene regulatory hierarchies.. Nature communications 2026. https://doi.org/10.1038/s41467-026-72198-x
49. scDifformer: diffusion-based post-training for virtual cell modeling across large-scale single-cell data. Nucleic Acids Research 2026. https://doi.org/10.1093/nar/gkag706
50. Deep generative modeling of sample-level heterogeneity in single-cell genomics.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02808-x
51. GenePT: A Simple But Effective Foundation Model for Genes and Cells Built From ChatGPT. bioRxiv 2023. https://doi.org/10.1101/2023.10.16.562533
52. Scalable querying of human cell atlases via a foundational model reveals commonalities across fibrosis-associated macrophages. bioRxiv 2023. https://doi.org/10.1101/2023.07.18.549537
53. A clinical benchmark of public self-supervised pathology foundation models.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58796-1
54. CLM-X: A multimodal single-cell foundation model with flexible multi-way Transformer for unified scRNA-seq and scATAC-seq analysis. bioRxiv 2026. https://doi.org/10.64898/2026.02.17.704943
55. Integrated multimodal cell atlas of Alzheimer's disease.. Nature neuroscience 2024. https://doi.org/10.1038/s41593-024-01774-5
56. Systematic benchmarking of high-throughput subcellular spatial transcriptomics platforms across human tumors.. Nature communications 2025. https://doi.org/10.1038/s41467-025-64292-3
57. Cell Painting: a decade of discovery and innovation in cellular imaging.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02528-8
58. A multiplexed single-cell CRISPR screening platform enables systematic dissection of the unfolded protein response. Cell 2016. https://doi.org/10.1016/j.cell.2016.11.048
59. Predicting transcriptional responses to novel chemical perturbations using deep generative model for drug discovery.. Nature communications 2024. https://doi.org/10.1038/s41467-024-53457-1
60. PerturbNet predicts single-cell responses to unseen chemical and genetic perturbations.. Molecular systems biology 2025. https://doi.org/10.1038/s44320-025-00131-3
61. Tahoe-x1: Scaling Perturbation-Trained Single-Cell Foundation Models to 3 Billion Parameters. bioRxiv 2025. https://doi.org/10.1101/2025.10.23.683759
62. Efficient Fine-Tuning of Single-Cell Foundation Models Enables Zero-Shot Molecular Perturbation Prediction.  2024. https://arxiv.org/abs/2412.13478v2
63. Single-cell foundation models benefit from cross-modal training: adding proteomics data beats parameter scaling. bioRxiv 2026. https://doi.org/10.64898/2026.08.14.744845
64. AROMA: Augmented Reasoning Over a Multimodal Architecture for Virtual Cell Genetic Perturbation Modeling.  2026. https://arxiv.org/abs/2604.20263v1
65. A deep generative model for deciphering cellular dynamics and in silico drug discovery in complex diseases.. Nature biomedical engineering 2025. https://doi.org/10.1038/s41551-025-01423-7
66. Human interpretable grammar encodes multicellular systems biology models to democratize virtual cell laboratories.. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.048
67. AI-driven virtual cell models in preclinical research: technical pathways, validation mechanisms, and clinical translation potential.. NPJ digital medicine 2025. https://doi.org/10.1038/s41746-025-02198-6
68. Sparse Autoencoders Reveal Interpretable Features in Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.1101/2025.10.22.681631
69. Exhaustive Circuit Mapping of a Single-Cell Foundation Model Reveals Massive Redundancy, Heavy-Tailed Hub Architecture, and Layer-Dependent Differentiation Control.  2026. https://arxiv.org/abs/2603.11940v1
70. Retrieval-Based Evaluation of Cell Painting Feature Spaces Reveals Differences in the Preservation of Biologically Meaningful Phenotypic Similarity.. International journal of molecular sciences 2026. https://doi.org/10.3390/ijms27135727
71. Progress and new challenges in image-based profiling.. Molecular systems biology 2026. https://doi.org/10.1038/s44320-026-00197-7
72. Exploring genetic interaction manifolds constructed from rich single-cell phenotypes. Science 2019. https://doi.org/10.1126/science.aax4438
73. A molecularly defined and spatially resolved cell atlas of the whole mouse brain. bioRxiv 2023. https://doi.org/10.1101/2023.03.06.531348
74. Toward AI Virtual Cells for Hepatology: Representation, Generation, Dynamics, and Intervention in Single-Cell Models.. Clinical and Molecular Hepatology 2026. https://doi.org/10.3350/cmh.2026.0820
75. Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02772-6
76. PertEval-scFM: Benchmarking Single-Cell Foundation Models for Perturbation Effect Prediction. bioRxiv 2025. https://doi.org/10.1101/2024.10.02.616248
77. scArchon: a scalable benchmarking framework for assessing single-cell perturbation models.. Genome biology 2026. https://doi.org/10.1186/s13059-026-04104-z
78. Harmonised benchmarking of foundation models for single-cell and spatial transcriptomics reveals context-dependent generalisation.  2026. https://arxiv.org/abs/2607.17227
79. Benchmarking single-cell foundation models in a zero-shot setting. bioRxiv 2026. https://doi.org/10.64898/2026.08.03.739553
80. Task-dependent Performance of Single-cell Foundation Models under Low Supervision. bioRxiv 2026. https://doi.org/10.64898/2026.04.01.714123
81. A Systematic Evaluation of Single-Cell Foundation Models on Cell-Type Classification Task. Web Search and Data Mining 2025. https://doi.org/10.1145/3701551.3708811
82. Biology-driven insights into the power of single-cell foundation models. Genome Biology 2025. https://doi.org/10.1186/s13059-025-03781-6
83. Robustness to nuisance perturbations enables unsupervised evaluation of single-cell foundation models. bioRxiv 2026. https://doi.org/10.64898/2026.08.22.746357
84. Systematic evaluation of single-cell foundation model interpretability: attention-derived edge scores add no incremental value over gene-level features for perturbation-target prediction. BMC Genomics 2026. https://doi.org/10.1186/s12864-026-12965-8
85. Counting cells can accurately predict small-molecule bioactivity benchmarks.. Nature communications 2026. https://doi.org/10.1038/s41467-026-68725-5
86. Benchmarking algorithms for generalizable single-cell perturbation response prediction.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02980-0
87. Evaluating the Utilities of Foundation Models in Single‐Cell Data Analysis. bioRxiv 2024. https://doi.org/10.1101/2023.09.08.555192
