# 单细胞与空间组学基础模型与虚拟细胞 · 方向背景报告

证据 93 篇 · 覆盖度 0.65 · 第 9 轮 · 更新 2026-10-18 · 数字核验删句 1

## 本次变更

- 新增 [72] PerturbBridge: Direct Phenotypic Supervision for Cellular Perturbation Generation

## 摘要（TL;DR）

- scGPT 在超 3300 万细胞上预训练，迁移学习后在注释、整合、扰动预测、基因网络推断等任务上表现优异[1]；Geneformer 在约 3000 万单细胞转录组上以自监督方式学习网络动力学，微调后在染色质与网络动力学任务中持续提升准确率，并在有限患者数据下识别出心肌病候选治疗靶点[2]。
- 一项工作用 2220 万细胞语料预训练 400 个模型、开展 6400 次实验，发现性能在数据规模远小于当前语料时即趋于平台，未观察到明确的数据缩放定律[3]。
- 零样本评估中，Geneformer 和 scGPT 的 AvgBIO 多数低于 HVG、Harmony、scVI 等简单基线，HVG 在所有指标上优于二者，scGPT 仅在 PBMC 12k 上部分优于 scVI/Harmony[4]。
- 逐层评估 scFoundation（100M 参数）与 Tahoe-X1（1.3B 参数）发现最优层依赖任务与情境：轨迹推断在 60% 深度达峰、比最终层高 31%，扰动预测的最优层随 T 细胞激活状态在 0–96% 间漂移，静息细胞反而首层最佳[5]。
- CellWorld 将预测目标转向潜在细胞表征，采用 JEPA 式预训练，在 4600 万人细胞、3 平台 11 器官上训练 4 个变体（5.74M–94.56M 参数），其 CellWorld-Small（5.74M）在全部 11 个线性探针和 7 个空间基准上超越所有基线[6]。
- Tahoe-x1（Tx1）将扰动训练的单细胞基础模型推到最高 30 亿参数，在含 Tahoe-100M 扰动图谱的大规模转录组上预训练，在基因必需性、癌症标志基因、细胞类型分类和留出情境扰动响应预测四项基准上均达 SOTA，计算效率较先前细胞状态模型提升 3–30 倍[7]。
- 对已发表的 Tahoe-x1 做跨模态继续预训练，仅用 70M 参数模型在 48,843 个蛋白质组样本（来自 440 项质谱研究）上训练一个 epoch，就在多数原评测基准上匹配或超过 1B 和 3B 参数 RNA-only 模型，作者据此主张精心策划的蛋白质组数据可带来比单纯增大模型规模更大的收益[8]。
- 对 Geneformer V2-316M 与 scGPT whole-human 各层残差流激活训练 TopK SAE，分别生成 82525 与 24527 个特征，其中 99.8% 的特征在 SVD 下不可见，仅 29–59% 能注释到通路，仅 3/48（6.2%）转录因子显示调控靶标特异性[9]。
- 因果电路追踪发现约 53% 生物一致性、65–89% 抑制主导且不随架构与细胞类型变化，跨模型共识 1,142 个域对（10.6 倍富集），但 CRISPRi 基因级验证方向准确率仅 56.4%，提示模型编码的是共表达而非因果调控[10]。
- 在四个 Perturb-seq 数据集上，差分空间指标 Train Mean 基线（0.711/0.557/0.373/0.628）优于 scGPT（0.641/0.554/0.327/0.596）与 scFoundation（0.552/0.459/0.269/0.471），而随机森林加 GO 特征最佳（0.739/0.586/0.480/0.648）[11]。
- 有研究在 14 个数据集、18 个指标上发现 MSE、Pearson Δ 等常用指标常校准不良，降低了对阳性模型性能的敏感性；在良好校准指标下，深度学习扰动模型可优于无信息基线[12]。
- scContam 用 MinHash 基因集指纹加基于损失的成员推断攻击逐细胞审计，在 PBMC 3k 与胰腺胰岛图谱上分别有 80.4%、77.0% 的细胞指纹 p<0.05，而截断后的 AIDA v2 与 Tahoe-100M 为 0%[13]。
- VCBench 把四个虚拟细胞框架综合为七个能力维度，在五个可测维度上，预注册的线性/最近邻基线在 4 维追平或超越所有基础模型，仅 TranscriptFormer 在 RNA 到蛋白预测上超最强基线 53% Pearson[14]。
- 该综述将面向肝脏的 AI 虚拟细胞（AIVC）建模归纳为三条互补路线：生成模型、动力学/运输模型，以及预训练/基础模型，并以扰动响应预测作为跨层评估的切入点[15]。
- 该文指出已发表模型仅展示了图谱整合、轨迹推断、可迁移表示、回顾性响应程序等单个组件，尚无经前瞻验证的肝脏模拟器[15]。

## 1 背景与定义

单细胞与空间组学基础模型的边界，首先由“预训练语料—表征迁移—下游任务”这一范式划定：模型在千万至亿级细胞转录组上自监督预训练，再把表征迁移到注释、整合、扰动预测等任务[1][2]。与之相邻但需区分的是三类对象：一是以蛋白序列/修饰位点为对象的蛋白语言模型，如 PTM-Mamba 在 **79,707** 条修饰序列上训练[16]，其对象与任务均不同于细胞层面模型；二是以病理图像为对象的视觉基础模型及其与空间转录组的跨模态对齐[17][18]；三是以形态图像为读出的 Cell Painting 表征学习[19]。**“虚拟细胞”则是这一范式的目标态而非同义词**：它要求模型预测扰动响应、生成细胞状态并支持多模态整合，其定义在愿景层面被表述为多尺度、多模态的大神经网络模型，具备预测、生成、可查询能力[20]，在评估层面则被要求具备数据、设计、基准与实验验证的完整证据链[21]。

演化脉络上，该方向经历了三次重心转移。第一次是从“图谱即资源”转向“图谱即预训练语料”：细胞图谱被重新定位为细胞普查、3D 图谱、基因型-表型连接、4D 发育图谱与生物学基础模型五种用途[22]，SCimilarity 则以 **2340 万**细胞参考实现跨组织疾病的可扩展细胞搜索[23]。第二次是从“规模扩张”转向“规模收益的怀疑”：**2220 万**细胞、**400** 个模型、**6400** 次实验未观察到明确的数据缩放定律[3]，零样本评估中 HVG 等简单基线在多项指标上优于 Geneformer 与 scGPT[4]，参数无关表示在多个基准上取得 SOTA 或近 SOTA 并超越基础模型的分布外表现[24]。第三次是从“单一转录组”转向“多模态与扰动”：空间转录组基础模型把预测目标从基因重建转向潜在细胞表征[6]，病理—转录组双编码器以 **220 万**配对 patch 对齐图像与基因句子[18]，扰动侧则从 Perturb-seq 的基因组规模筛选[25]走向 Tahoe-100M 的 **超过 1 亿**细胞、**379** 种化合物[26]与 **30 亿**参数的扰动预训练模型[7]。

核心问题可归为四组张力。**其一，规模与收益的张力**：一边是语料持续上推至 **1 亿**[27]、**3.5 亿**[28]、**1.31 亿**[29]细胞，另一边是平台期证据与“精心策划的蛋白质组数据收益大于单纯增大规模”的跨模态结果[8]。**其二，表征与机制的张力**：SAE 特征图谱显示模型内化了有组织的生物学知识，但仅 **6.2%** 转录因子显示调控靶标特异性[9]；因果电路追踪给出约 **53%** 生物一致性与 **56.4%** 的 CRISPRi 方向准确率，指向“编码共表达而非因果调控”[10]；系统评估则发现注意力对扰动预测无增量价值、平凡基因级基线更优[30]。**其三，预测与评测的张力**：Train Mean 基线在四个 Perturb-seq 数据集上优于 scGPT 与 scFoundation[11]，多方法评测亦报告基础模型误差高于加性基线[31]，但指标校准研究指出 MSE、Pearson Δ 常校准不良，良好校准下深度学习模型可优于无信息基线[12]；同时预训练污染审计显示两个高引用基准存在大量预训练重叠证据[13]。**其四，泛化与验证的张力**：虚拟细胞挑战赛提供开放循环基准但本身不含模型结果[32]，路线图工作批评静态图谱、仅转录组读出与分布内基准不足以预测新条件行为[21]，肝脏方向的综述则直言**尚无经前瞻验证的肝脏模拟器**[15]。

由此，该方向的纳入边界应落在“有公开权重、可复现评测、面向扰动或跨模态泛化”的模型与资源上，而排除仅做单一数据集流程改良或无权重无代码的工作。**当前最实质的未决问题是评估口径**：层选择会改变结论（扰动最优层随 T 细胞激活状态在 **0–96%** 间漂移[5]），任务集合与基线各异使跨研究的“SOTA”难以横向比较，VCBench 更发现预注册线性/最近邻基线在五个可测维度中的 **4 维**追平或超越所有基础模型[14]。这意味着“虚拟细胞”的进展判断，正从模型规模与单点精度，转向基准校准、污染审计与实验闭环三者的共同约束[12][13][21]。

## 2 方法学


### 2.1 单细胞基础模型

单细胞基础模型的主流路线，是用 Transformer 在千万至亿级细胞转录组上做自监督预训练，再把表征迁移到注释、整合、扰动预测等下游任务。**scGPT** 在超 **3300 万**细胞上预训练，迁移学习后在注释、整合、扰动预测、基因网络推断等任务上表现优异[1]；**Geneformer** 在约 **3000 万**单细胞转录组上以自监督方式学习网络动力学，微调后在染色质与网络动力学任务中持续提升准确率，并在有限患者数据下识别出心肌病候选治疗靶点[2]。二者都把细胞类比为句子、基因类比为词元[33]。规模继续上推：**CellFM** 预训练于 **1 亿**人类细胞，在多种任务上达到或超过 Geneformer、scGPT、scFoundation、UCE 等模型[27]；**scPRINT-2** 覆盖 **3.5 亿**细胞、**16** 个物种，在表达去噪、细胞嵌入和细胞类型预测上达到 SOTA，并具备表达插补与反事实推理的生成能力[28]。

但“更大即更好”受到直接挑战。一项工作用 **2220 万**细胞语料预训练 **400** 个模型、开展 **6400** 次实验，发现性能在数据规模远小于当前语料时即趋于平台，**未观察到明确的数据缩放定律**[3]。零样本评估则质疑预训练表征的通用性：在 5 个数据集上，Geneformer 和 scGPT 的 AvgBIO 多数低于 HVG、Harmony、scVI 等简单基线，HVG 在所有指标上优于二者，scGPT 仅在 PBMC 12k 上部分优于 scVI/Harmony[4]。这提示预训练规模与下游可靠性之间并非单调关系，也说明零样本设定应成为常规评估项。

表征提取方式同样被重新审视。常规做法默认最终层嵌入最优，但逐层评估 scFoundation（**100M** 参数）与 Tahoe-X1（**1.3B** 参数）发现最优层依赖任务与情境：轨迹推断在 **60%** 深度达峰、比最终层高 **31%**，扰动预测的最优层随 T 细胞激活状态在 **0–96%** 间漂移，静息细胞反而首层最佳[5]。该结论仅基于两个模型、两类任务，外推需谨慎，但它至少表明“取最后一层”的默认约定缺乏依据。

架构层面的分歧在于是否引入生物学先验与替代注意力。**RegFormer** 融合基因调控网络先验与 Mamba 状态空间建模，以规避 Transformer 的上下文长度限制，在细胞注释、GRN 重建、遗传扰动预测和药物响应建模上持续优于 scGPT 和 Geneformer[34]。**scDifformer** 采用掩码语言模型预训练、扩散后训练与下游微调三阶段，扩散模块在强批次效应下持续提升跨数据集性能，细胞注释达到 SOTA，并可恢复 marker 基因、功能通路与跨组织分化轨迹[35]。与之相对，**GenePT** 走极简路线：用 GPT-3.5 基于 NCBI 基因文本描述生成基因嵌入，无需数据策展与预训练，在基因属性与细胞类型分类上达到与 Geneformer 等相当甚至更优的性能[36]。这条路线与大规模表达预训练形成鲜明对照，争议点在于表达数据本身是否被充分利用。

跨物种与跨模态是另一条扩展轴。**TranscriptFormer** 在多达 **1.12 亿**细胞、**12** 个物种、跨越 **15.3 亿**年进化的数据上联合建模基因身份与表达水平，分布内与分布外细胞类型分类达 SOTA，可零样本识别疾病状态并跨物种转移注释，发育轨迹与系统发育关系自然涌现[37]。**Speciesformer** 在含 **1.31 亿**细胞的 SpeciesCorpus 上预训练，目标是把进化表征学习与虚拟细胞状态生成结合，区分保守原理与物种/组织/细胞环境特异变异，但证据仅给出摘要级信息，缺少定量基准[29]。**LucaCell** 以预训练 mRNA 序列嵌入表示基因而非固定注释，将表达离散化为 bin 后用 Transformer 编码，在 **8500 万**人类和小鼠单细胞上预训练，实现人、小鼠、狐猴肾脏数据的跨物种跨模态细胞类型迁移，并实现无比对微生物嵌入、区分 **50 多**种细菌且保留种内结构[38]。**EpiZoo** 则把 DNA 序列感知引入跨物种单细胞表观基因组学，将百万维表观基因组谱转换为紧凑“细胞句子”，以克服现有模型依赖基因组坐标、局限于单一物种的问题[39]。

面向“虚拟细胞”的生成式建模与检索式建模构成两种互补范式。**SCimilarity** 用深度度量学习学习统一可解释的细胞表征：一项工作报告 **2340 万**细胞、**412** 项研究、**56** 训练/ **15** 测试数据集，在查询敏感性与整合性能间取得最佳平衡（β=**0.001**）[23]；另一版本在 **2270 万**细胞、**399** 项研究上训练，验证了跨组织查询能力，发现最初在间质性肺病中识别的巨噬细胞亚群也存在于其他纤维化疾病、组织和 3D 水凝胶系统[40]。其局限在于依赖 Cell Ontology 注释质量，部分细胞类型关系模糊[23]。样本级异质性方面，**MrVI** 以层次深度生成模型和交叉注意力建模样本协变量效应，无需先验聚类即可识别样本分组，实现高分辨无注释差异表达与丰度分析并控制批次[41]。值得注意的是，上述模型多以 scRNA-seq 为主，而 **PTM-Mamba** 代表另一类基础模型：它用双向门控 Mamba 融合 ESM-2 与 PTM 嵌入，在 **79,707** 条修饰序列（源自 **311,350** 条 Swiss-Prot PTM 记录）上训练，收敛快于 PTM-Transformer 基线并能区分修饰与野生型序列[16]——它与细胞层面基础模型在对象和任务上均不同，不宜直接比较性能高低。

综合来看，该领域的核心张力有三：其一，预训练规模的红利在数据规模远未触顶时即出现平台，且缺乏清晰缩放定律[3]，与持续扩大语料的路线（1 亿[27]、3.5 亿[28]、1.31 亿[29]）并存；其二，零样本条件下简单基线可胜过基础模型[4]，而多数工作报告的是微调后性能，两类结论不可直接对照；其三，评估口径不统一——层选择[5]、任务集合与基准基线各异，使跨工作报告的“SOTA”难以横向比较。综述亦指出当前模型仍需改进性能与生物学实用性[33]。

### 2.2 空间与多模态模型

在空间与多模态基础模型的发展中，一个核心分歧在于预训练目标应重建什么。早期思路以掩码基因身份或表达值为目标，但 CellWorld 指出这可能促使模型复制测定特异的技术变异，限制表征迁移性，因而将预测目标转向潜在细胞表征，采用 JEPA 式预训练，在 **4600 万人细胞、3 平台 11 器官**上训练 4 个变体（5.74M–94.56M 参数），其 **CellWorld-Small（5.74M）** 在全部 11 个线性探针和 7 个空间基准上超越所有基线，且仅用 5% 语料的冻结 Large 模型在 7 个空间基准上超越全部微调基线 [6]。与之相对，NexuST 走分层路线，反复交错基因级分子建模与细胞级空间建模，构建 **HumanST-46M**（72 个数据集、11 个器官、三种成像平台、4570 万人类细胞），在四个留出数据集约 260 万细胞上于细胞类型注释、区域预测、基因恢复等任务达到 SOTA 或具竞争力 [42]。两者都强调空间迁移更依赖生物来源多样性与优化而非单纯细胞数量 [6]，但预训练目标的选择（潜在表征 vs 分层交错建模）仍是未决问题。

病理图像与空间转录组的跨模态对齐是另一条主线。PAST 在 **2000 万配对病理图像与单细胞转录组**上训练泛癌单细胞基础模型，联合编码细胞形态与基因表达，支持单细胞基因表达预测、虚拟分子染色和多模态生存分析，并在多种癌症任务中超越现有方法 [43]。OmiCLIP 则用 CLIP 对比学习把 H&E 图像与转录组"句子"对齐，基于 **ST-bank 的 220 万配对 patch（1007 样本、32 器官）**，配套 Loki 平台提供组织对齐、注释、细胞分解、检索与基因表达预测五项功能，在 5 个模拟、19 个公开和 4 个内部数据集上对比 22 种 SOTA 方法 [18]。mSTAR 进一步引入第三种模态，整合病理切片、专家报告与基因表达，用 **26,169 切片-模态对、10,275 患者、32 癌种、1.16 亿 patch** 做两阶段预训练，在 15 类 97 项任务中表现优异，并显示多模态预训练可用更少数据达到竞争性能 [44]。这些工作共同面对的限制是配对数据依赖：OmiCLIP 依赖配对 WSI 与 Visium 数据且泛化待验证 [18]，mSTAR 依赖报告与基因表达配对、跨中心泛化仍需验证 [44]。

在单细胞多模态整合层面，MultiVI 用深度生成模型（VAE）分别建模基因表达与染色质可及性，通过惩罚对齐两模态潜空间并模块化扩展至表面蛋白，可整合单模态数据集、提供校准的不确定性估计、估计缺失模态的差异表达并支持样本外预测，但依赖相关群体存在多模态信息 [45]。CLM-X 则用多路 Transformer 与统一 token 化、分阶段掩码重建预训练，在百万级单模态与多模态数据上支持 RNA-only、ATAC-only 和配对 RNA-ATAC 输入，在 10 个数据集、五个下游任务上持续超越现有多模态方法与单模态基础模型，尤其在 RNA-ATAC 跨模态翻译和扰动预测上优势明显 [46]。二者的差异在于生成式概率建模与 Transformer 基础模型路线的取舍，前者强调不确定性量化与插补，后者强调跨模态翻译与规模扩展。

空间映射与对齐方面，moscot 把生物映射任务统一为 W、GW 或 FGW 型最优传输问题，支持多模态与图谱规模数据，在 **170 万细胞小鼠胚胎**等数据上实现高效对齐，计算时间与内存较既往 OT 工具降数个数量级，并实验验证 NEUROD2 调控 epsilon 细胞形成 [47]。VINTER 则从生成式视觉语言角度切入，在 **145 万组织学-文本对**上对齐，把组织学图像、实测基因表达和空间邻域作为单一序列读取，输出每个组织类别的概率，并可在固定图像下编辑分子证据，联合三源信息后组织注释精度优于空间域方法和空间基础模型 [48]。这两类方法分别代表"对齐即传输"与"对齐即生成"的不同技术路线。

支撑上述模型的评测与数据基础仍不均衡。病理侧已有临床基准系统比较 CTransPath、Phikon、UNI、Virchow 等公开自监督模型的参数量、算法与训练数据，指出数字病理数据缺乏与 WSI 算力需求是主要瓶颈 [17]；空间转录组侧则有对 Stereo-seq v1.3、Visium HD FFPE、CosMx 6K、Xenium 5K 四个亚细胞平台在三种人肿瘤连续切片上的统一评测，以 CODEX 蛋白和 scRNA-seq 为真值，发现各平台在灵敏度、扩散控制、细胞分割等关键指标上差异显著，但仅覆盖 3 种肿瘤、4 个平台，结论外推受限 [49]。应用层面，SEA-AD 整合多组学与空间基因组学构建阿尔茨海默病图谱，对 **84 名供体**颞中回开展 snRNA-seq、snATAC-seq、snMultiome 与 MERFISH，识别 **139 种分子细胞类型**，发现早期炎症小胶质、反应性星形胶质、SST+ 神经元丢失与 OPC 再髓鞘，晚期兴奋性神经元及 Pvalb+、Vip+ 亚型丢失，但队列以老年供体为主、横断面设计难以确定因果时序 [50]。更早的 Cell Painting 综述则提示图像型 profiling 自 2013 年以来经协议优化、特征提取与批次校正改进，已用于解析化合物作用机制与毒性，未来需整合其他高内涵数据类型 [19]。总体看，多模态与空间模型的能力提升高度依赖配对数据规模与平台特性，而跨平台、跨中心的泛化验证仍是共同短板。

### 2.3 扰动响应与虚拟细胞

虚拟细胞的核心任务之一是预测细胞对扰动的响应，而单细胞扰动数据本身的稀缺与高维使这一任务长期受限于实验通量。**Perturb-seq** 将单细胞RNA-seq与CRISPR扰动结合，在混合池中检测复杂转录表型，早期工作分析了约**200,000个**免疫细胞和细胞系，识别出扰动靶点、基因signature、细胞状态与遗传互作[51]；同一时期另一项工作用单基因与组合CRISPR扰动解剖未折叠蛋白反应，经两个全基因组CRISPRi筛选鉴定约**100个**命中基因，解耦三条UPR分支[52]。**CROP-seq** 则把gRNA盒插入慢病毒3'LTR使其成为可检测的mRNA，实现池化筛选的单细胞转录组读出，验证显示编辑效率与LentiGuide-Puro高度相似、多数细胞可分配单一gRNA[53]。这些技术奠定了扰动响应建模的数据基础，但覆盖的扰动与细胞类型仍有限。

在数据规模扩张的方向上，**Tahoe-x1（Tx1）** 将扰动训练的单细胞基础模型推到最高**30亿参数**，在含Tahoe-100M扰动图谱的大规模转录组上预训练，采用含药物token的掩码表达生成目标，在基因必需性、癌症标志基因、细胞类型分类和留出情境扰动响应预测四项基准上均达SOTA，计算效率较先前细胞状态模型提升**3–30倍**[7]。与之形成对照的是跨模态路线：对已发表的Tahoe-x1做跨模态继续预训练，仅用**70M参数**模型在**48,843个**蛋白质组样本（来自**440项**质谱研究）上训练一个epoch，就在多数原评测基准上匹配或超过1B和3B参数RNA-only模型，并提升对held-out蛋白扰动基准的迁移，作者据此主张精心策划的蛋白质组数据可带来比单纯增大模型规模更大的收益[8]。这与参数缩放主导的叙事构成直接张力，但两者评测基准与任务并不完全重合，不宜简单比高低。

面向新扰动的泛化是另一条主线。**PRnet** 以SMILES与剂量构建扰动嵌入、结合未扰动表达谱生成响应分布，在新化合物、通路和细胞系预测上优于替代方法，实验验证了小细胞肺癌与结直肠癌候选化合物，并构建覆盖**88个细胞系、52个组织**的扰动图谱、为**233种疾病**推荐药物[54]。**PerturbNet** 同样针对未见化学与遗传扰动，强调预测细胞状态分布变化而非仅均值，并以scGen、CPA、chemCPA、GEARS、Biolord为对照[55]。**UNAGI** 则从疾病时间序列单细胞数据出发，用VAE-GAN解析细胞动力学并整合CMAP药物数据库做虚拟药物筛选，对照Seurat、SCANPY、scVI、scGPT、GEARS等方法[56]。三者都指向"未见扰动"这一共同难点，但PRnet依赖训练化合物库覆盖度、对全新化学空间外推有限，PerturbNet指出跨细胞类型与组合扰动泛化仍受限。

利用预训练基础模型做轻量适配是提高样本效率的一条路径。有工作引入**药物条件适配器**，仅微调不到**1%**参数以保留预训练生物表征，在所有泛化设置下达SOTA，尤其在新细胞系少样本与零样本泛化上显著优于基线；其限制在于扰动数据集仅覆盖数百分子、少数细胞系[57]。**AROMA** 走多模态增强推理路线，整合文本证据、图拓扑与蛋白序列特征建模扰动-靶依赖，构建**PerturbReason数据集（>498k样本）**与两个知识图谱，在多细胞系超越现有方法，并在未见细胞系零样本与知识稀疏长尾场景下保持稳健，但依赖知识图谱与检索质量[58]。

对扰动表征粒度的反思催生了序列条件模型。**STRAND** 指出基因级模型会把同一基因不同位点（不同转录起始位点与调控元件）的扰动坍缩为同一表征，因而以调控DNA序列编码为条件参数化对照到扰动状态的条件传输；在K562、Jurkat、RPE1上评估，低样本判别分提升达**33%**，未见基因基准取得最佳平均排名，新细胞系迁移Pearson提升达**0.14**，基因组覆盖从约**1.5%**扩至约**95%**[59]。**SCALE** 针对对照与处理细胞非配对这一实验现实，将细胞视为无序集合，用共享集合感知编码器与条件DiT学习潜在传输，无需细胞级匹配，在CRISPR数据七项指标上全面超越竞争方法，并预测出经三供体PBMC实验验证的细胞因子响应差异[60]。**Chreode** 则把分布演化从推理时移到训练时，用结构化残差转移算子做一步式状态转移预测，在**240万细胞**小鼠胚胎图谱（**7个数据集**）上预训练，作为GEARS可迁移嵌入将Norman Perturb-seq的DE20 MSE从**0.2121**降至**0.1858**（相对提升**12.4%**）[61]。这些工作共享"分布级、非配对"的问题意识，但分别在序列条件、集合传输与一步动力学上给出不同答案。

评测与可信度问题正被单独提出。**Virtual Cell Challenge** 作为Arc Institute的循环开放基准竞赛，提供评估框架、专用数据集与竞赛平台以加速模型开发，但本身不含具体模型结果[32]。有路线图工作主张虚拟细胞模型只有在数据、模型设计、基准与实验验证之间的证据链被显式化后才具决策相关性，提出四层经验框架（分子状态、干预、生物背景、正交表型），并批评静态图谱、仅转录组读出与分布内基准不足以预测新条件下的细胞行为，评估应转向泛化到未见细胞类型与扰动等生物学标准[21]。这与多数以留出集精度为主要卖点的建模工作报告形成方法论上的争议。

更宏观的愿景与验证闭环也被反复讨论。**AI虚拟细胞（AIVC）** 被设想为多尺度、多模态的大神经网络模型，具备预测、生成、可查询三大能力，主张从数据直接学习细胞行为而无需显式规则，并指出多尺度建模、海量互作组件与非线性动力学仍是挑战[20]。临床前转化综述强调整合单细胞转录组与蛋白质组等多模态组学、结合深度生成模型与图神经网络，并采用从计算评估到CRISPR和类器官实验验证的闭环流程，同时指出监管接受、数据隐私与可解释性仍是障碍[62]。另一条路线追求可解释性：以自然语言"细胞规则"直接映射为数学方程构建agent-based模型，案例覆盖肿瘤生长、侵袭、免疫治疗响应与脑发育，依赖标注细胞状态与规则质量[63]。在数据侧，全基因组扰动已扩展到原代细胞：对**4名供体、2200万**原代人CD4+ T细胞在静息与刺激态做扰动测序，发现调控因子及所控基因程序随刺激条件大幅变化，并提名极化与衰老表型调控因子、关联自身免疫病风险，其限制是供体数少、体外刺激条件[64]。这些工作共同表明，虚拟细胞的价值判断正从"预测精度"扩展到可解释、可验证与上下文特异性，而不同路线在规模、模态与机制透明度之间的取舍尚未收敛。

### 2.4 机制可解释性与表征分析

机制可解释性研究目前主要沿两条技术路线展开：稀疏自编码器（SAE）特征分解与注意力/电路分析。在 SAE 路线上，对 **Geneformer V2-316M** 与 **scGPT whole-human** 各层残差流激活训练 TopK SAE，分别生成 **82525** 与 **24527** 个特征，其中 **99.8%** 的特征在 SVD 下不可见，仅 **29–59%** 能注释到通路；模型内化了有组织的生物学知识，但调控逻辑编码极少，仅 **3/48（6.2%）** 转录因子显示调控靶标特异性，多组织对照下为 **10.4%** [9]。在三个模型（scGPT、scFoundation、Geneformer）隐藏表示上训练的 SAE 则揭示出多样且复杂的生物与技术信号，且不同训练协议与架构的模型编码方式不同；这些特征具有功能可干预性——抑制批次特征可改善整合并保留生物信号，激活药物特征可使对照细胞呈浓度依赖地向药物扰动状态转变 [65]。两条结果并不矛盾：SAE 能提取可解释、可操控的特征，但特征注释覆盖率与调控特异性都有限。

因果层面的证据进一步区分了「编码结构」与「编码因果」。因果电路追踪对两模型消融 SAE 特征并测量下游响应（**96,892** 条边、**80,191** 次前向），发现约 **53%** 生物一致性、**65–89%** 抑制主导且不随架构与细胞类型变化，跨模型共识 **1,142** 个域对（**10.6 倍**富集），但 CRISPRi 基因级验证方向准确率仅 **56.4%**，提示模型编码的是共表达而非因果调控 [10]。系统评估框架（37 项分析、153 个统计检验、四种细胞类型、两种扰动模态）同样发现注意力虽具分层结构——早期层富集蛋白互作、晚期层富集转录调控——但对扰动预测无增量价值：平凡基因级基线 AUROC **0.81–0.88** 优于注意力/相关性边的 **0.70**，成对边分数零增量，消融调控头无退化，而 CSSI 可将 GRN 恢复提升至多 **1.85×** [30]。对 Geneformer 的穷举电路追踪则补充了结构细节：L5 层全部 **4065** 个活跃 SAE 特征产生 **1,393,850** 条显著下游边（较选择性采样扩 **27 倍**），呈重尾枢纽分布（**1.8%** 特征占大量连接，**40%** 顶级枢纽无注释），三阶冗余比 **0.59** 低于配对 **0.74** 且零协同，层位置决定分化方向性（L17 特征 **100%** 推向成熟，L0/L11 为 **0.00–0.58**）[66]。这些工作共同指向一个争议点：电路与注意力中的生物结构是否等价于可用于预测的机制信息，现有证据偏否定。

在「可解释性反哺算法」的方向上，有研究从 scGPT 内部提取出紧凑的造血流形算法，在 Tabula Sapiens **564,253** 细胞上验证并在多供体免疫面板做冻结头零样本迁移，伪时间深度排序 **|ρ|=0.439** 优于次优 **0.331**，CD4/CD8 AUROC **0.867**、单核/巨噬 **0.951**，且比 MLP 探针快 **34.5 倍**、参数少约 **1000 倍**，但作者承认主要在造血系统验证、其他生物学过程泛化性有限 [67]。与之呼应，针对 scFM 在 GRN 推断上表现不佳（重建式预训练未显式捕获调控信号、现有零样本方法有时不及随机预测）的问题，有工作提出 GRN 泛化基准并用虚拟值扰动与梯度轨迹从冻结 scFM 蒸馏可泛化基因间特征，报告显著优于现有方法 [68]。两类结果与前述「调控逻辑编码极少」的结论形成张力：从模型内部确实能提取有竞争力的专用算法，但这种提取依赖任务特定的读出设计，尚不能证明模型本身具备通用因果调控表征。

### 2.5 形态与图像表型基础模型

图像表型基础模型的表征能力已在多项评测中被直接比较。在U2OS JUMP-MOA参考板的零样本检索评测中，**CellPaintSSL**、OpenPhenom与uniDINO的活性阳性数分别为**85/90**、81/90与82/90，数量相近，但CellPaintSSL的活性检索mAP显著高于另两者（p<0.0001），而MOA注释的恢复仅部分实现且因模型而异[69]。这一结果说明，特征空间的前提性质量并不保证目标生物学关系的恢复，也提示不同模型间的差异更多体现在检索质量而非简单分类计数上。综述层面的证据同样支持深度学习表征的优势，同时指出部分场景手工特征仍具竞争力，并列出CLOOME零样本MoA top-10准确率**61.3%**对比CellProfiler 24.5%[70]；该综述还强调时序与3D模态、质控标准及特征解释仍不成熟[70]。

在方法路径上，自监督学习被用于从形态图像中无偏推断基因功能。**CellPaint-POSH**将Cell Painting与pooled光学CRISPR筛选结合，改造线粒体染色为RNA探针Mitoprobe以兼容原位测序，在**163,090个单细胞**的Cell Painting图像与4色ISS数据上训练自监督模型，其机器学习特征预测性能高于专家形态特征，形态表型可按已知功能聚类基因并在无通路报告基因条件下揭示基因关联网络[71]。与之不同，PerturbBridge把表型监督放入生成流程的训练阶段，以随机数据到数据桥模型联合优化桥回归与可微生物响应损失，在BBBC021上MoA准确率CellProfiler达**77.8%**（较CellFlux+5.7点）、DINOv2达74.9%（+7.5点），并在JUMP上取得Hit@10 12.15%、中位秩74，在AllenCell上Hit@1 69.29%[72]。两类工作分别从表征学习与生成建模切入，前者强调无偏形态表征对基因功能聚类的价值，后者强调扰动特异性生物响应需在训练中被显式监督，二者并不构成直接冲突，但共同指向同一问题：形态特征空间是否保留任务相关的生物学关系，需在下游检索或生成指标上逐项验证[69][72]。

## 3 数据与资源

单细胞扰动图谱的规模正从千级扰动扩展到百万级细胞。**基因组规模Perturb-seq** 在K562与RPE1两个细胞系中以CRISPRi靶向所有表达基因、覆盖**超过250万个**人类细胞，报告了RNA剪接、分化、染色体不稳定等多维表型，并发现线粒体基因组应激的特异调控；其局限在于仅两个细胞系、CRISPRi为敲低而非敲除、表型限于转录组 [25]。在分析方法上，有工作以CRISPR介导的pooled Perturb-seq高维单细胞表型构建细胞状态“流形”，将每个扰动与遗传互作投射到流形特定位置，实现调控通路无偏排序与遗传互作的系统分类，但依赖强遗传互作筛选、未覆盖全基因组互作 [73]。空间维度上，**Perturb-FISH** 将MERFISH与gRNA原位扩增结合，在LPS刺激巨噬细胞中与匹配的Perturb-seq比较验证敲除效应一致性，并揭示细胞密度与邻居扰动的影响，进一步结合钙成像用于ASD风险基因CRISPRi筛选并在肿瘤异种移植3D组织中验证；其技术限制是gRNA仅20 bp、无法如mRNA般平铺，需原位扩增 [74]。药物扰动方面，**Tahoe-100M** 覆盖**超过1亿**细胞、50个细胞系与379种化合物（3剂量、24 h），覆盖约56,000个细胞系-药物-剂量组合，发现Dabrafenib在非BRAF依赖细胞系中的意外敏感性及CDK抑制剂引起G1或G2/M阻滞，但摘要未提供模型训练与验证细节 [26]。

空间图谱与图谱整合构成另一类资源基础。全小鼠脑MERFISH成像**约800万**细胞、>1100基因并整合scRNA-seq，生成包含>5000转录簇、约300主要细胞类型的图谱，注册到小鼠脑共坐标框架以量化各脑区细胞组成并识别空间模块；其局限为仅小鼠脑、基因面板有限需整合scRNA-seq [75]。在资源定位上，有综述提出细胞图谱正从数据收集走向图谱整合与基础模型，列举其作为细胞普查、3D图谱、基因型-表型连接、4D发育图谱及生物学基础模型五种用途 [22]。需注意上述资源在物种（人细胞系 vs 小鼠脑）、扰动类型（CRISPRi敲低、化合物处理）与读出（转录组、空间转录组、钙成像）上差异显著，各自的细胞数与扰动数不可直接比较高低。

## 4 应用与结果

单细胞与空间图谱已能以高分辨率刻画肝脏的健康与疾病状态，涵盖小叶肝细胞分区、纤维化巨噬细胞—星状细胞生态位、胆管细胞反应、免疫重塑及肝细胞癌生态系统；但这些图谱本身只能显示细胞状态出现在何处，并不能预测肝损伤是否会进展，也无法预测肝脏对未经测试的药物、毒物或遗传扰动的响应。该综述据此将面向肝脏的 **AI 虚拟细胞（AIVC）** 建模归纳为三条互补路线：生成模型、动力学/运输模型，以及预训练/基础模型，并以扰动响应预测作为跨层评估的切入点 [15]。

在证据层面，该文将现有工作分为直接肝脏验证、含肝脏基准、通用单细胞证据与概念应用四类，指出已发表模型仅展示了图谱整合、轨迹推断、可迁移表示、回顾性响应程序等单个组件，**尚无经前瞻验证的肝脏模拟器** [15]。这一判断也界定了后续评估的要求：验证需覆盖供体、病因、分期与平台等维度，而非停留在回顾性拟合 [15]。

## 5 评测、可复现性与争议

评测单细胞基础模型时，最直接的争议是基准本身是否被预训练数据污染。**scContam** 用 MinHash 基因集指纹加基于损失的成员推断攻击（MIA-scFM）逐细胞审计，在 **PBMC 3k** 与胰腺胰岛图谱上分别有 **80.4%**、**77.0%** 的细胞指纹 p<0.05，而截断后的 AIDA v2 与 Tahoe-100M 为 **0%**；MIA AUROC 随模型容量数据比从 **0.494** 升至 **0.690**、**0.881** [13]。这说明零样本高分可能反映预训练暴露而非泛化，但作者也指出生产级模型抗实例记忆，分布污染需单独检测 [13]。

在扰动预测这一被寄予厚望的任务上，多项独立基准得出相近的负面结论。在四个 Perturb-seq 数据集上，差分空间指标 **Train Mean** 基线（0.711/0.557/0.373/0.628）优于 **scGPT**（0.641/0.554/0.327/0.596）与 **scFoundation**（0.552/0.459/0.269/0.471），而随机森林加 GO 特征最佳（0.739/0.586/0.480/0.648）[11]。另一项在 K562 CRISPRa、224 个扰动、19,264 个基因上的评测中，scGPT、scFoundation、GEARS、CPA 的误差均高于加性基线，遗传互作预测不优于 no change 基线 [31]。PertEval-scFM 同样报告零样本 scFM 嵌入未持续优于基线，尤其在分布偏移下 [76]；覆盖 27 种方法、29 个数据集的评测也认为基础模型表现仍存疑，并强调细胞上下文嵌入的必要性 [77]。

不过，这一负面图景受到指标校准问题的挑战。有研究在 **14 个数据集、18 个指标**上发现 MSE、Pearson Δ 等常用指标常校准不良，降低了对阳性模型性能的敏感性；在良好校准指标下，深度学习扰动模型可优于无信息基线 [12]。这与前述「不如简单基线」的结论构成直接张力：分歧部分源于评测指标而非模型本身，提示基准设计需引入阳性对照。

细胞类型注释与整合任务上的结论同样分裂。零样本评测中，scGPT、SCimilarity、UCE、Transcriptformer 在注释任务上多数数据集由传统基线最强，蛋白表达预测则基础模型更准（SCimilarity 误差最低、Transcriptformer 相关性最高），整合任务表现中等、scVI 更佳 [78]。低监督条件下，7 个基础模型中仅 1 个聚类超过最强经典基线，3 个批次校正、4 个注释、0 个重建、6 个扰动预测超过基线，CellPLM 在聚类/注释/批次校正领先、scMulan 在扰动预测领先、PCA 在重建领先 [79]。这些差异说明排名高度依赖任务、数据集与监督设置，不宜跨研究直接比较高低。

空间与多模态方向的统一评测显示「无模型全面领先」。对 Nicheformer、CellPLM、scGPT-spatial、GenePT、scELMo、Novae 六个模型的统一框架评估发现，表达训练的细胞级 Transformer 擅长细胞身份，空间/图模型保留组织结构，语言嵌入在部分扰动指标有竞争力，排名随模态、预处理、token 化、生物先验、域偏移和指标变化 [80]。VCBench 把四个虚拟细胞框架综合为七个能力维度，在五个可测维度上，预注册的线性/最近邻基线在 **4 维**追平或超越所有基础模型，仅 **TranscriptFormer** 在 RNA 到蛋白预测上超最强基线 **53% Pearson**；多尺度整合与 in silico 实验两维度结构上无法端到端测试 [14]。

可解释性方面出现了明确的否定证据。在两种架构、四种细胞类型、两种扰动模态下进行 **153 项**统计检验并做因果消融，发现注意力边分数对扰动靶标预测相对基因级特征无增量价值，单变量基线反而更优，TRRUST 头因果消融无行为效应 [81]。与之部分呼应的是 GRN 重建基准：严格零样本下 scGPT token 嵌入相似度在 STRING 和 ChIP-seq 上超越经典基线，scFoundation 动态转移表现最强 [82]——即嵌入层面的信号可能存在，但注意力作为调控代理的解释需谨慎。

可复现性基础设施被普遍视为瓶颈，也是较一致的建设方向。BioLLM 针对预处理不一致、接口异构、评估指标非标准化三大挑战提供统一 API 与决策树预处理 [83]；scArchon 基于 Snakemake 容器化运行 9 种扰动工具并聚合评分排名 [84]；PerturBench 揭示广泛使用模型的模式崩溃，指出秩指标可补充 RMSE、无单一架构明显占优 [85]。图像侧，JUMP 原始数据达 **115 TB**，JUMP-lite 以 **92.0 GB** 子集约缩小 **1,250 倍**，中度压缩基本保留信号 [86]。

无监督评估提供了不依赖下游标签的另一条路径。基于扰动不变性的框架在 5 个 scFM、PCA 基线与 39 个数据集上发现，丢弃 **5%** 计数时近等价模型的局部邻域保持差异近 **2 倍**，且该不稳定性具尺度依赖性并被视觉连贯的嵌入掩盖 [87]。这与「标准基准判定近乎等价」的观察一起，指向现有任务型评测的分辨力不足。

空间转录组与更广的方法学基准则把可重复性落到跨站点指标上。ST 数据集覆盖六种组织类型、跨三站点，在 Xenium 与 CosMx 上评估重复性、灵敏度、动态范围、信噪比、错误发现率与细胞类型注释一致性，SpatialQM 开源、STP 门户公开，社区质量指标库约 **3300 万**细胞 [88]。更早的图谱级整合基准在 13 个任务、最多 23 批次、超 **120 万**细胞上比较 16 种工具、14 项指标，发现 Scanorama 和 scVI 在复杂任务表现好、有注释时 scGen 和 scANVI 最优、Harmony 和 LIGER 适合 scATAC [89]。小分子活性基准则提醒基线选择本身会改变结论：逻辑回归细胞计数 AUC **0.70±0.22** 接近 CLOOME 的 **0.71±0.19**，细胞计数加 MW 与 logP 达 **0.74±0.21**，但在 24 个蛋白靶标基准中 Cell Painting 确实优于细胞计数 [90]。

## 6 空白与趋势

机制可解释性之外，评测与可信度正成为独立的研究对象，且负面证据集中在三类。其一是**基准污染**：scContam 在 PBMC 3k 与胰腺胰岛图谱上分别有 **80.4%**、**77.0%** 的细胞指纹 p<0.05，而截断后的 AIDA v2 与 Tahoe-100M 为 **0%**，MIA AUROC 随模型容量数据比从 **0.494** 升至 **0.690**、**0.881** [13]，说明零样本高分可能反映预训练暴露而非泛化。其二是**简单基线反超**：四个 Perturb-seq 数据集上 Train Mean 基线（0.711/0.557/0.373/0.628）优于 scGPT（0.641/0.554/0.327/0.596）与 scFoundation（0.552/0.459/0.269/0.471），随机森林加 GO 特征最佳 [11]；K562 CRISPRa 评测中 scGPT、scFoundation、GEARS、CPA 误差均高于加性基线，遗传互作预测不优于 no change 基线 [31]；VCBench 在五个可测维度上，预注册的线性/最近邻基线在 **4 维**追平或超越所有基础模型，仅 TranscriptFormer 在 RNA 到蛋白预测上超最强基线 **53% Pearson** [14]。其三是**指标校准**：14 个数据集、18 个指标上 MSE、Pearson Δ 等常校准不良，降低了对阳性模型性能的敏感性，在良好校准指标下深度学习扰动模型可优于无信息基线 [12]。**这三类证据并不指向同一结论**——污染审计质疑的是评测有效性，基线反超质疑的是模型增益，指标校准则质疑负面结论本身，三者需分别处理而非合并为"基础模型无用"。

综合上述证据，该方向的趋势与空白可归纳为以下六条。

1. **从"重建表达"转向"预测潜在状态"，但目标函数选择尚无共识。** CellWorld 将预测目标从基因测量转向潜在细胞表征，其 Small（5.74M）变体在全部 11 个线性探针和 7 个空间基准上超越所有基线 [6]；NexuST 则坚持分层交错建模基因级与细胞级，在四个留出数据集约 260 万细胞上达 SOTA 或具竞争力 [42]。**没人做过的是在同一数据与评测下直接对比这两类预训练目标的迁移收益**，现有工作各自选边、基准不重叠。

2. **扰动表征粒度从"基因级"下沉到"位点/序列级"，但覆盖仍限于少数细胞系。** STRAND 指出基因级模型会把同一位点不同调控元件的扰动坍缩为同一表征，以调控 DNA 序列为条件后基因组覆盖从约 **1.5%** 扩至约 **95%**，新细胞系迁移 Pearson 提升达 **0.14** [59]；AROMA 以文本、图拓扑与蛋白序列增强推理，构建 **>498k** 样本的 PerturbReason 数据集 [58]。**空白在于位点级扰动数据本身稀缺**，STRAND 仅在 K562、Jurkat、RPE1 三个细胞系评估，位点级 Perturb-seq 图谱尚未出现。

3. **分布级、非配对的传输建模成为扰动预测的新默认设定。** SCALE 将细胞视为无序集合、用条件 DiT 学习潜在传输，无需细胞级匹配，在 CRISPR 七项指标上超越竞争方法并预测出经三供体 PBMC 实验验证的细胞因子响应差异 [60]；Chreode 把分布演化移到训练时，将 Norman Perturb-seq 的 DE20 MSE 从 **0.2121** 降至 **0.1858** [61]。**尚未有人系统比较传输模型与生成模型（PRnet、PerturbNet、UNAGI）在同一非配对基准上的表现**，两类方法目前各用各的对照集。

4. **机制可解释性给出的是"有结构、无因果"的一致结论，但反哺算法的路径刚起步。** SAE 路线显示仅 **3/48（6.2%）** 转录因子具调控靶标特异性 [9]；因果电路追踪的 CRISPRi 验证方向准确率仅 **56.4%** [10]；系统评估中平凡基因级基线 AUROC **0.81–0.88** 优于注意力边 **0.70** [30]。与此同时，从 scGPT 提取的造血流形算法伪时间深度排序 **|ρ|=0.439** 优于次优 **0.331**、比 MLP 探针快 **34.5 倍** [67]，GRN 蒸馏工作也报告显著超越现有方法 [68]。**关键空白是：这些提取出的专用算法能否在造血系统之外复现**，现有验证均限于单一生物学过程。

5. **虚拟细胞的评估正从"留出集精度"转向"泛化到未见条件 + 实验闭环"，但前瞻验证几乎空白。** 路线图工作主张评估应转向泛化到未见细胞类型与扰动，并批评静态图谱与仅转录组读出不足 [21]；Virtual Cell Challenge 提供开放循环基准但本身不含模型结果 [32]；肝脏 AIVC 综述明确指出**尚无经前瞻验证的肝脏模拟器**，已发表模型仅展示单个组件 [15]。**这是最明确的空白：从回顾性拟合到前瞻性湿实验验证的闭环，目前只有零散个案（SCALE 的三供体 PBMC、PRnet 的候选化合物）而非系统流程。**

6. **多模态与空间的瓶颈已从"模型能力"转移到"配对数据与跨平台泛化"。** PAST 依赖 **2000 万**配对病理图像与单细胞转录组 [43]，OmiCLIP 依赖 **220 万**配对 patch 且泛化待验证 [18]，mSTAR 依赖报告与基因表达配对、跨中心泛化仍需验证 [44]；四个亚细胞空间平台在三种肿瘤上的统一评测显示灵敏度、扩散控制、细胞分割差异显著，但仅覆盖 3 种肿瘤、4 个平台 [49]。**没人做过的是跨平台、跨中心的配对数据稀缺条件下的多模态基础模型迁移评估**，现有工作均在单平台配对数据上报告 SOTA。

此外有两条值得单列但证据尚薄的线索。其一是**参数效率对参数规模的挑战**：跨模态继续预训练的 **70M** 参数模型在 **48,843** 个蛋白质组样本上训练一个 epoch，就在多数原评测基准上匹配或超过 1B 和 3B 参数 RNA-only 模型 [8]，但两者评测基准与任务并不完全重合，**该结论需在统一基准上复核**。其二是**图像表型基础模型的任务相关性验证**：U2OS JUMP-MOA 零样本检索中 CellPaintSSL、OpenPhenom、uniDINO 的活性阳性数为 **85/90**、81/90、82/90 相近，但 CellPaintSSL 的活性检索 mAP 显著更高（p<0.0001），MOA 注释恢复仅部分实现 [69]；细胞计数基线在小分子活性基准上接近甚至超过复杂模型 [90]。**这两条线索共同指向一个尚未被系统回答的问题：在形态与图像模态上，复杂表征相对简单计数/线性基线的增量究竟来自何处。**

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 单细胞基础模型（scGPT/Geneformer 类） | 朝阳（方法未收敛，已进入批判期） | scGPT 建立了多组学预训练范式并获大量引用 [1]，Geneformer 证明迁移学习可用于网络生物学 [2]；但 GenePT 用简单文本嵌入即达到可比效果 [36]，且系统性评测显示基础模型在下游任务上未必优于简单基线 [91]，说明**架构红利尚未被证实**，方法仍在快速迭代。 |
| 空间与多模态整合模型 | 朝阳（工具层收敛中，生物学应用爆发） | MultiVI 提供了多模态深度生成整合的通用框架 [45]，moscot 把时空映射统一为可扩展的最优传输问题 [47]；同时 AD 多模态图谱 [50] 表明整合方法已被大规模生物学项目直接消费。工具在收敛，但**跨模态对齐的评价标准仍缺**。 |
| 扰动响应预测与虚拟细胞 | 朝阳（概念热、验证弱，争议最大） | Perturb-seq 系列奠定了扰动测序的数据基础 [51]、[53]，虚拟细胞的路线图已被明确提出 [20]；但 2025 年的基准工作直接给出**深度学习扰动预测尚不能超越简单基线**的结论 [31]，PerturBench 进一步显示模型间差异不稳定 [85]。这是典型的「问题定义已成立、解法未成立」。 |
| 机制可解释性与表征分析 | 萌芽（几乎全为 2026 年预印本） | 稀疏自编码器在单细胞基础模型中提取出可解释特征 [65]，但同一路线发现其调控知识组织有限 [9]；系统评测显示不同基础模型的可解释性差异大且缺乏统一协议 [30]。**证据全为预印本、无同行评议共识**，属早期探索。 |
| 形态与图像表型基础模型 | 萌芽（样本极少，方法刚起步） | 池化 Cell Painting CRISPR 平台实现了基因功能的从头推断 [71]，图像 profiling 的进展与挑战被系统梳理 [70]；但检索式评测显示不同 Cell Painting 特征空间差异显著 [69]，说明**表征尚未标准化**。 |
| 数据与资源（图谱、扰动库） | 成熟（资源型工作，增量为主） | 全基因组 Perturb-seq 图谱 [25] 与遗传互作流形 [73] 已确立数据规模范式；Human Cell Atlas 从细胞普查走向统一基础模型的路线已被明确 [22]。新工作多为**规模扩展与覆盖补全**，而非方法突破。 |
| 评测、可复现性与争议 | 朝阳（近两年集中爆发，正成为独立子领域） | atlas 级整合基准确立了标准化评测范式 [89]；随后出现针对扰动预测的否定性结论 [31] 与 PerturBench 统一评测框架 [85]，以及基础模型效用评估 [91]。**批判性结果正在重塑领域议程**，但评测标准本身尚未收敛。 |

**整体判断**：这个方向整体处于**朝阳期的中后段，且已提前进入"清算阶段"**。雷达样本中 2025–2026 年证据占 **74%**，CNS 占 **29%**，说明热度和资源投入仍在高位；但真正的方法收敛尚未发生——单细胞基础模型的架构红利被 GenePT 类简单基线挑战 [36]，扰动预测被基准工作判定为**未跑赢基线** [31]。窗口期判断：**纯"再训一个更大的基础模型"的窗口基本关闭（约 6–12 个月）**；而"**用严格基准证明某类归纳偏置有效**"和"**多模态/形态表型的可解释表征**"的窗口还有 **1.5–2.5 年**。最大不确定性是：**虚拟细胞的核心任务（扰动响应预测）是否本质上受限于数据覆盖而非模型容量**——若是，则当前大部分生成式路线会被证伪，领域重心将转向数据设计与评测 [85]、[20]。

**接下来怎么做**

1. **把"衰老"做成扰动预测的评测切口，而不是再训一个模型。** 用公共 Perturb-seq / Tahoe 类数据 + 衰老相关基因集，构造**跨年龄、跨细胞类型的分布外扰动基准**，产出可复现的 benchmark 与失败模式分析。现在做是因为领域刚承认"没跑赢基线" [31]，但**尚无针对衰老/状态漂移的专门基准**，而 PerturBench 提供了可复用的评测骨架 [85]。这与你衰老 + 单细胞的背景直接对齐，且不依赖新数据。

2. **在多模态整合上做"评价"而非"新模型"，优先空间 + 影像。** 用 MultiVI [45] 与 moscot [47] 作为基线，系统检验跨模态对齐在**批次、分辨率、模态缺失**下的稳健性，产出评测协议 + 轻量修正方法。现在做是因为工具已收敛到可复现基线，但 Cell Painting 特征空间差异显著 [69]，**评价缺口明确**。

3. **把类器官多组学项目包装成"虚拟细胞"的验证场景。** 用你的类器官 + 多组学数据做**扰动响应预测的前瞻性验证**（预测 → 实验验证 → 报告失败），这是当前最稀缺的证据类型。现在做是因为虚拟细胞路线图明确呼吁此类闭环验证 [20]，而现有工作几乎全是回顾性评测 [91]。**这类"预测 + 证伪"的工作审稿价值高于又一个模型。**

4. **切入机制可解释性，但以"可证伪的调控假设"为产出。** 用稀疏自编码器 [65] 在公开权重模型上提取特征，再用你的衰老数据检验这些特征是否对应**已知调控程序**；正面回应"调控知识组织有限"的负面结果 [9]。现在做是因为该子领域**全是 2026 年预印本、无共识**，先发优势明显，且算力门槛低（推理为主）。

5. **用公共数据做低成本 demo，锁定"数据资源 + 评测"的复合定位。** 基于 Human Cell Atlas 的统一模型路线 [22] 与全基因组扰动图谱 [25]，构建**衰老视角的子集重加权/采样策略**并量化其对下游预测的影响。现在做是因为资源型工作已成熟、增量空间在**"如何选数据"而非"如何堆数据"**，且能快速产出可分享的 demo 建立合作信誉。

## 参考文献

1. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. Nature Methods 2024. https://doi.org/10.1038/s41592-024-02201-0
2. Transfer learning enables predictions in network biology. Nature 2023. https://doi.org/10.1038/s41586-023-06139-9
3. Evaluating the role of pretraining dataset size and diversity on single-cell foundation model performance.. Nature methods 2026. https://doi.org/10.1038/s41592-026-03120-y
4. Zero-shot evaluation reveals limitations of single-cell foundation models.. Genome biology 2025. https://doi.org/10.1186/s13059-025-03574-x
5. Intermediate Layers Encode Optimal Biological Representations in Single-Cell Foundation Models.  2026. https://arxiv.org/abs/2604.14838v1
6. CellWorld: From Gene-Level Reconstruction to Latent Cell Prediction in Spatial Transcriptomics Foundation Models.  2026. https://arxiv.org/abs/2608.06659v1
7. Tahoe-x1: Scaling Perturbation-Trained Single-Cell Foundation Models to 3 Billion Parameters. bioRxiv 2025. https://doi.org/10.1101/2025.10.23.683759
8. Single-cell foundation models benefit from cross-modal training: adding proteomics data beats parameter scaling. bioRxiv 2026. https://doi.org/10.64898/2026.08.14.744845
9. Sparse autoencoders reveal organized biological knowledge but minimal regulatory logic in single-cell foundation models: a comparative atlas of Geneformer and scGPT.  2026. https://arxiv.org/abs/2603.02952v1
10. Causal Circuit Tracing Reveals Distinct Computational Architectures in Single-Cell Foundation Models: Inhibitory Dominance, Biological Coherence, and Cross-Model Convergence.  2026. https://arxiv.org/abs/2603.01752v2
11. Benchmarking foundation cell models for post-perturbation RNA-seq prediction.. BMC genomics 2025. https://doi.org/10.1186/s12864-025-11600-2
12. Deep learning perturbation models can outperform baselines on calibrated metrics.. Nature biotechnology . https://doi.org/10.1038/s41587-026-03307-w
13. Auditing pretraining contamination in single-cell foundation model benchmarks.  2026. https://arxiv.org/abs/2607.20572v1
14. VCBench: A Multi-Dimensional Benchmark for Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.06.18.733146
15. Toward AI Virtual Cells for Hepatology: Representation, Generation, Dynamics, and Intervention in Single-Cell Models.. Clinical and Molecular Hepatology 2026. https://doi.org/10.3350/cmh.2026.0820
16. PTM-Mamba: a PTM-aware protein language model with bidirectional gated Mamba blocks.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02656-9
17. A clinical benchmark of public self-supervised pathology foundation models.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58796-1
18. A visual-omics foundation model to bridge histopathology with spatial transcriptomics.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02707-1
19. Cell Painting: a decade of discovery and innovation in cellular imaging.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02528-8
20. How to build the virtual cell with artificial intelligence: Priorities and opportunities.. Cell 2024. https://doi.org/10.1016/j.cell.2024.11.015
21. Toward trustworthy virtual cells: a roadmap for perturbation-resolved, context-aware, and experimentally validated cell models. Frontiers in Cell and Developmental Biology 2026. https://doi.org/10.3389/fcell.2026.1900624
22. The Human Cell Atlas from a cell census to a unified foundation model.. Nature 2024. https://doi.org/10.1038/s41586-024-08338-4
23. A cell atlas foundation model for scalable search of similar human cells.. Nature 2024. https://doi.org/10.1038/s41586-024-08411-y
24. Parameter-free representations outperform single-cell foundation models on downstream benchmarks.  2026. https://arxiv.org/abs/2602.16696v1
25. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. bioRxiv 2021. https://doi.org/10.1016/j.cell.2022.05.013
26. Abstract 491: A 100 million cell single cell atlas enabling mechanistic and genotype-specific drug response discovery.. Cancer Research 2026. https://doi.org/10.1158/1538-7445.am2026-491
27. CellFM: a large-scale foundation model pre-trained on transcriptomics of 100 million human cells.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59926-5
28. scPRINT-2: Towards the next-generation of cell foundation models and benchmarks.  2025. https://doi.org/10.64898/2025.12.11.693702
29. Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling.  . https://doi.org/10.64898/2026.09.22.752128
30. Systematic Evaluation of Single-Cell Foundation Model Interpretability Reveals Attention Captures Co-Expression Rather Than Unique Regulatory Signal.  2026. https://arxiv.org/abs/2602.17532v1
31. Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02772-6
32. Virtual Cell Challenge: Toward a Turing test for the virtual cell.. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.008
33. Single-cell foundation models: bringing artificial intelligence into cell biology.. Experimental & molecular medicine 2025. https://doi.org/10.1038/s12276-025-01547-5
34. RegFormer: a single-cell foundation model powered by gene regulatory hierarchies.. Nature communications 2026. https://doi.org/10.1038/s41467-026-72198-x
35. scDifformer: diffusion-based post-training for virtual cell modeling across large-scale single-cell data. Nucleic Acids Research 2026. https://doi.org/10.1093/nar/gkag706
36. GenePT: A Simple But Effective Foundation Model for Genes and Cells Built From ChatGPT. bioRxiv 2023. https://doi.org/10.1101/2023.10.16.562533
37. A Cross-Species Generative Cell Atlas Across 1.5 Billion Years of Evolution: The TranscriptFormer Single-cell Model. bioRxiv 2025. https://doi.org/10.1101/2025.04.25.650731
38. LucaCell: a sequence-centric foundation model for cross-species single-cell analysis.  . https://doi.org/10.21203/rs.3.rs-11151765/v1
39. EpiZoo: a DNA sequence-aware foundation model for cross-species single-cell epigenomics.  . https://doi.org/10.64898/2026.09.24.754017
40. Scalable querying of human cell atlases via a foundational model reveals commonalities across fibrosis-associated macrophages. bioRxiv 2023. https://doi.org/10.1101/2023.07.18.549537
41. Deep generative modeling of sample-level heterogeneity in single-cell genomics.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02808-x
42. NexuST: A Hierarchical Foundation Model for Spatial Transcriptomics.  . https://doi.org/10.64898/2026.09.22.753590
43. PAST: A multimodal single-cell foundation model for histopathology and spatial transcriptomics in cancer. arXiv.org 2025. https://arxiv.org/abs/2507.06418v1
44. A multimodal knowledge-enhanced whole-slide pathology foundation model.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66220-x
45. MultiVI: deep generative model for the integration of multimodal data. Nature Methods 2023. https://doi.org/10.1038/s41592-023-01909-9
46. CLM-X: A multimodal single-cell foundation model with flexible multi-way Transformer for unified scRNA-seq and scATAC-seq analysis. bioRxiv 2026. https://doi.org/10.64898/2026.02.17.704943
47. Mapping cells through time and space with moscot.. Nature 2025. https://doi.org/10.1038/s41586-024-08453-2
48. VINTER: a generative vision-language model for annotating and interrogating spatial tissues.  . https://doi.org/10.64898/2026.10.01.752251
49. Systematic benchmarking of high-throughput subcellular spatial transcriptomics platforms across human tumors.. Nature communications 2025. https://doi.org/10.1038/s41467-025-64292-3
50. Integrated multimodal cell atlas of Alzheimer's disease.. Nature neuroscience 2024. https://doi.org/10.1038/s41593-024-01774-5
51. Perturb-seq: Dissecting molecular circuits with scalable single cell RNA profiling of pooled genetic screens. Cell 2016. https://doi.org/10.1016/j.cell.2016.11.038
52. A multiplexed single-cell CRISPR screening platform enables systematic dissection of the unfolded protein response. Cell 2016. https://doi.org/10.1016/j.cell.2016.11.048
53. Pooled CRISPR screening with single-cell transcriptome read-out. Nature Methods 2017. https://doi.org/10.1038/nmeth.4177
54. Predicting transcriptional responses to novel chemical perturbations using deep generative model for drug discovery.. Nature communications 2024. https://doi.org/10.1038/s41467-024-53457-1
55. PerturbNet predicts single-cell responses to unseen chemical and genetic perturbations.. Molecular systems biology 2025. https://doi.org/10.1038/s44320-025-00131-3
56. A deep generative model for deciphering cellular dynamics and in silico drug discovery in complex diseases.. Nature biomedical engineering 2025. https://doi.org/10.1038/s41551-025-01423-7
57. Efficient Fine-Tuning of Single-Cell Foundation Models Enables Zero-Shot Molecular Perturbation Prediction.  2024. https://arxiv.org/abs/2412.13478v2
58. AROMA: Augmented Reasoning Over a Multimodal Architecture for Virtual Cell Genetic Perturbation Modeling.  2026. https://arxiv.org/abs/2604.20263v1
59. STRAND: Sequence-Conditioned Transport for Single-Cell Perturbations.  2026. https://arxiv.org/abs/2602.10156v1
60. SCALE:Scalable Conditional Atlas-Level Endpoint transport for virtual cell perturbation prediction.  2026. https://arxiv.org/abs/2603.17380v3
61. Chreode: A Cell World Model for One-Step Temporal Dynamics and Perturbation Prediction. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.28111
62. AI-driven virtual cell models in preclinical research: technical pathways, validation mechanisms, and clinical translation potential.. NPJ digital medicine 2025. https://doi.org/10.1038/s41746-025-02198-6
63. Human interpretable grammar encodes multicellular systems biology models to democratize virtual cell laboratories.. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.048
64. Genome-scale perturb-seq in primary human CD4+ T cells maps context-specific regulators of T cell programs and human immune traits.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.002
65. Sparse Autoencoders Reveal Interpretable Features in Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.1101/2025.10.22.681631
66. Exhaustive Circuit Mapping of a Single-Cell Foundation Model Reveals Massive Redundancy, Heavy-Tailed Hub Architecture, and Layer-Dependent Differentiation Control.  2026. https://arxiv.org/abs/2603.11940v1
67. Discovery of a Hematopoietic Manifold in scGPT Yields a Method for Extracting Performant Algorithms from Biological Foundation Model Internals.  2026. https://arxiv.org/abs/2603.10261v1
68. Towards Universal Gene Regulatory Network Inference: Unlocking Generalizable Regulatory Knowledge in Single-cell Foundation Models.  2026. https://arxiv.org/abs/2605.08128v1
69. Retrieval-Based Evaluation of Cell Painting Feature Spaces Reveals Differences in the Preservation of Biologically Meaningful Phenotypic Similarity.. International journal of molecular sciences 2026. https://doi.org/10.3390/ijms27135727
70. Progress and new challenges in image-based profiling.. Molecular systems biology 2026. https://doi.org/10.1038/s44320-026-00197-7
71. A pooled Cell Painting CRISPR screening platform enables de novo inference of gene function by self-supervised deep learning.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66778-6
72. PerturbBridge: Direct Phenotypic Supervision for Cellular Perturbation Generation.  . https://arxiv.org/abs/2610.17066
73. Exploring genetic interaction manifolds constructed from rich single-cell phenotypes. Science 2019. https://doi.org/10.1126/science.aax4438
74. Simultaneous CRISPR screening and spatial transcriptomics reveal intracellular, intercellular, and functional transcriptional circuits.. Cell 2025. https://doi.org/10.1016/j.cell.2025.02.012
75. A molecularly defined and spatially resolved cell atlas of the whole mouse brain. bioRxiv 2023. https://doi.org/10.1101/2023.03.06.531348
76. PertEval-scFM: Benchmarking Single-Cell Foundation Models for Perturbation Effect Prediction. bioRxiv 2025. https://doi.org/10.1101/2024.10.02.616248
77. Benchmarking algorithms for generalizable single-cell perturbation response prediction.. Nature methods 2025. https://doi.org/10.1038/s41592-025-02980-0
78. Benchmarking single-cell foundation models in a zero-shot setting. bioRxiv 2026. https://doi.org/10.64898/2026.08.03.739553
79. Task-dependent Performance of Single-cell Foundation Models under Low Supervision. bioRxiv 2026. https://doi.org/10.64898/2026.04.01.714123
80. Harmonised benchmarking of foundation models for single-cell and spatial transcriptomics reveals context-dependent generalisation.  2026. https://arxiv.org/abs/2607.17227
81. Systematic evaluation of single-cell foundation model interpretability: attention-derived edge scores add no incremental value over gene-level features for perturbation-target prediction. BMC Genomics 2026. https://doi.org/10.1186/s12864-026-12965-8
82. Benchmarking Static Gene Regulatory Network Reconstruction and Dynamic Transition Probing in Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.05.17.725083
83. BioLLM: A standardized framework for integrating and benchmarking single-cell foundation models. bioRxiv 2024. https://doi.org/10.1016/j.patter.2025.101326
84. scArchon: a scalable benchmarking framework for assessing single-cell perturbation models.. Genome biology 2026. https://doi.org/10.1186/s13059-026-04104-z
85. PerturBench: Benchmarking Machine Learning Models for Cellular Perturbation Analysis. Neural Information Processing Systems 2024. https://doi.org/10.48550/arXiv.2408.10609
86. JUMP-lite: Compact, reproducible benchmarking of cell representations.  2026. https://arxiv.org/abs/2608.07632
87. Robustness to nuisance perturbations enables unsupervised evaluation of single-cell foundation models. bioRxiv 2026. https://doi.org/10.64898/2026.08.22.746357
88. Standardized metrics for assessment and reproducibility of imaging-based spatial transcriptomics datasets.. Nature biotechnology 2025. https://doi.org/10.1038/s41587-025-02811-9
89. Benchmarking atlas-level data integration in single-cell genomics. Nature Methods 2020. https://doi.org/10.1038/s41592-021-01336-8
90. Counting cells can accurately predict small-molecule bioactivity benchmarks.. Nature communications 2026. https://doi.org/10.1038/s41467-026-68725-5
91. Evaluating the Utilities of Foundation Models in Single‐Cell Data Analysis. bioRxiv 2024. https://doi.org/10.1101/2023.09.08.555192
92. A Systematic Evaluation of Single-Cell Foundation Models on Cell-Type Classification Task. Web Search and Data Mining 2025. https://doi.org/10.1145/3701551.3708811
93. Biology-driven insights into the power of single-cell foundation models. Genome Biology 2025. https://doi.org/10.1186/s13059-025-03781-6
