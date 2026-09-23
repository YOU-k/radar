# 世界模型与自监督表征学习 · 方向背景报告

证据 65 篇 · 覆盖度 0.34 · 第 3 轮 · 更新 2026-09-23

## 本次变更

- 新增 [60] LaMamba-Diff: Linear-Time High-Fidelity Diffusion Models Based on Local Attention and Mamba
- 新增 [41] Revisiting Self-Supervised Visual Representation Learning
- 新增 [39] SANA-WM: Efficient Minute-Scale World Modeling with Hybrid Linear Diffusion Transformer
- 新增 [42] Scaling and Benchmarking Self-Supervised Visual Representation Learning
- 新增 [15] Contrastive Masked Autoencoders are Stronger Vision Learners
- 新增 [16] Siamese Image Modeling for Self-Supervised Vision Representation Learning
- 新增 [62] RegFormer: a single-cell foundation model powered by gene regulatory hierarchies.
- 新增 [65] JEPA-Anything: Learning Predictive Models across Different Worlds
- 新增 [31] CLAW: Learning Continuous Latent Action World Models via Adversarial Latent Regularization
- 新增 [37] Back to Parsimonious Latents: Learning Task-Centric World Models from Visual Foundations
- 新增 [36] Baba in Wonderland: Online Self-Supervised Dynamics Discovery for Executable World Models
- 新增 [57] MJEPA: A Simple and Scalable Joint-Embedding Predictive Architecture for Audio-Visual Learning
- 新增 [34] GLAM: Training a latent world model over global spatiotemporal memory for active exploration and navigation
- 新增 [7] LeVJEPA: Efficient&Scalable Video Pretraining without the Heuristics
- 新增 [49] A Simple Framework for Contrastive Learning of Visual Representations
- 新增 [50] Momentum Contrast for Unsupervised Visual Representation Learning
- 新增 [13] Masked Autoencoders Are Scalable Vision Learners
- 新增 [52] Emerging Properties in Self-Supervised Vision Transformers
- 新增 [51] Bootstrap Your Own Latent: A New Approach to Self-Supervised Learning
- 新增 [40] Self-Supervised Learning: Generative or Contrastive
- 新增 [53] Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture

## 摘要（TL;DR）

- 预测隐空间与世界模型的核心张力在于是否必须在像素/点云等观测空间重建未来，还是可在学习出的表征空间完成预测，JEPA 系列选择后者但须处理表征坍塌风险。
- LeJEPA 用各向同性高斯分布约束（SIGReg）替代 stop-gradient、教师学生网络等启发式设计，ViT-H/14 在 ImageNet-1k 冻结骨干线性评估达 79%，覆盖 10+ 数据集和 60+ 架构 [1]。
- SiamJEPA 保留 EMA 教师并强化孪生学生编码器结构，在有限训练预算下持续优于单编码器 JEPA 变体，线性探测精度高于需更长训练的 MAE [2]。
- 变分视角引发"JEPA 究竟是什么"的争议：Var-JEPA 论证 JEPA 与变分推断结构等价 [3]，VJEPA/BJEPA 将 JEPA 推广为概率形式并统一预测状态表示与贝叶斯滤波 [4]。
- 表格模态出现直接负面结果：JEPA 臂在 147 个数据集上落后仅值目标臂，分类 32:70 胜负，回归 8:24，且需 1.42 倍步数、1.66 倍墙钟达平台 [5]。
- V-JEPA 2 在超 100 万小时互联网视频上预训练，SSv2 77.3%、EK100 39.7 recall@5、PerceptionTest 84.0、TempCompass 76.9，并基于少于 62 小时 Droid 数据后训练出零样本机器人规划世界模型 [6]。
- LeVJEPA 去除目标编码器、预测器、stop-gradient 与掩码重建，仅用全局-局部不变性损失加 SIGReg，以 5.6–20.8× 更少预训练算力匹配或超 V-JEPA 2 [7]。
- 决策对齐存在直接争议：DINO-WM 假设潜空间距离与任务进度一致并实现零样本规划 [8]，D-JEPA 明确否定该假设并引入决策对齐监督，PushT 达 87.89% 成功率 [9]。
- 3D 与跨模态方向路径分化：3D-JEPA 在 PB_T50_RS 达 88.65% [10]，Point-JEPA 在 ModelNet40 线性 SVM 达 93.7±0.2% [11]，CrossJEPA 借 2D 基础模型在 ModelNet40/ScanObjectNN 达 94.2%/88.3% [12]。
- 掩码建模与自蒸馏路线从对立走向交叉：MAE 确立高掩码率+非对称结构配方，ImageNet-1K 达 87.8% [13]，而病理图像 30 亿张数据上 DINO 优于 MAE [14]，CMAE、SiameseIM、CAE 尝试统一两类目标 [15][16][17]。
- 评估协议不统一是分歧根源：多数工作仅在自有基准或仿真环境验证，真实机器人部署规模有限，跨模态、跨任务的统一对比仍然缺失，防坍塌机制与潜空间几何假设均未在统一协议下直接对比。

## 1 背景与定义

在掩码建模与自蒸馏之外，状态空间模型与线性注意力构成了本方向在架构侧的第三条线索。这条线索的核心动机是：Transformer 的注意力复杂度随序列长度平方增长，而生物多模态数据（长时程影像序列、组学长序列、时序生理信号）往往要求长上下文建模，因此需要线性或近线性复杂度的替代架构。Mamba 系列以选择性状态空间模型（SSM）为核心，通过输入相关的参数化实现内容感知的序列压缩，在语言、音频与基因组序列上展示了与 Transformer 可比或更优的精度-效率权衡 。S4 及其后续工作则从连续时间系统离散化出发，用 HiPPO 初始化与结构化卷积核实现长程记忆，为 SSM 提供了理论根基 。线性注意力一侧，Performer 用随机特征近似 softmax 核，将注意力复杂度降至线性 ；Linformer 从低秩视角证明注意力矩阵可被低秩近似，用投影矩阵压缩键值序列长度 ；RetNet 则提出保留机制，在训练并行、推理循环、长程衰减三者间取得平衡 。这些架构的共同问题是：它们能否在自监督预训练目标下保持表征质量，而不仅仅是在监督任务上替代注意力。目前证据显示，SSM 与线性注意力在长序列自监督（如长视频、长基因组片段）上的系统评测仍然稀缺，多数工作只在语言建模或分类任务上验证，与本方向核心的潜空间预测目标结合的工作更少 。

自监督表征向科学数据的迁移，是本方向另一条快速扩张但结论高度分化的线索。单细胞基因组学的系统基准测试在超 2000 万细胞上训练，评估细胞类型预测、基因表达重建、跨模态预测和数据整合等下游任务，发现 MAE 优于对比学习，与计算机视觉中对比学习常占优的趋势相反，并在零样本细胞类型预测中展现显著能力 [18]。这一"模态反转"与病理图像领域的结论形成对照：病理基础模型的临床基准评测梳理了 CTransPath、Phikon、UNI、Virchow 等模型的训练数据与算法，通过瓦片编码加聚合的两阶段流程评估下游任务，结果显示 DINO 算法优于 MAE，但病理领域 SSL 仍处早期，受限于数据与算力 [19]。两项基准在"掩码重建与自蒸馏谁更优"上给出相反答案，说明算法优劣高度依赖数据模态、标签稀缺程度与下游任务类型，而非存在普适最优目标 [18][19]。基因组方向，JEPA-DNA 将联合嵌入预测架构融入基因组基础模型训练，通过在潜空间监督全局序列嵌入，预测被掩码基因组片段的功能表征，并结合传统生成目标进行持续训练，在 17 项基准上线性探测与零样本性能一致提升，证明潜语义对齐优于纯 token 重建 [20]。高能物理方向，JetParticle-JEPA 基于 Particle Transformer 骨干，直接从连续粒子云预测被掩码粒子的潜表征，无需分词或重建原始输入，在 JetClass 上媲美全监督 SOTA，低标签场景超越监督基线，并在缺失探测器信息下展现鲁棒性 [21]。这些工作的共同模式是：把 JEPA 或掩码目标从自然图像迁移到科学数据时，必须重新定义"掩码单元"与"预测目标空间"，而这一重新定义往往比目标函数本身更决定成败 [20][21]。

医疗世界模型的综述提供了本方向在临床应用上的能力分级视角。该综述覆盖医学影像诊断、EHR 疾病进展建模与机器人手术规划三域，提出 L1 时序预测到 L4 规划控制的能力分级标准，并分析各系统所处层级，发现多数系统仅达 L1–L2，存在动作空间不明确、干预验证薄弱、多模态状态构建不完整等跨领域缺口 [22]。这一分级与本方向在机器人与自动驾驶上的进展形成有趣对照：V-JEPA 2 已在真实机械臂上零样本部署 [6]，D-JEPA 在真实机器人任务上提升 17 点 [9]，而医疗世界模型多数仍停留在 L1–L2，说明"动作空间是否明确、干预是否可验证"是决定世界模型能否进入规划层级的关键条件，而非模型规模或表征质量 [22]。这一判断对生物多模态数据的启示是：若要把世界模型用于干预性任务（如药物扰动预测、手术规划），动作空间定义与反事实验证协议的建设可能比表征学习本身更紧迫。

综合以上证据，本方向当前的核心问题可以归纳为三组未解张力。第一组是防坍塌机制与模态收益的关系：LeJEPA 的分布正则 [1]、SiamJEPA 的孪生学生 [2]、BiJEPA 的范数正则 [23]、Var-JEPA 与 VJEPA 的变分目标 [3][4] 各自在特定模态上成立，但表格模态的负面结果 [5] 与 3D、视频、基因组模态的正面结果 [10][7][20] 并存，说明"JEPA 是否普遍优于重建或仅值目标"尚无统一答案，收益高度依赖模态与数据特性。第二组是潜空间几何与决策相关性的关系：D-JEPA 明确否定潜空间距离与任务进度一致的假设 [9]，而 DINO-WM 的成功又表明在特定预训练特征下该假设可近似成立 [8]，Flow-JEPA 用流匹配替代确定性回归以缓解误差累积 [24]，三者对"潜动力学应如何参数化"给出不同答案，且未在统一基准上交叉验证。第三组是评估协议与真实部署的缺口：多数工作仅在自有基准或仿真环境验证，真实机器人部署规模有限 [6][9]，跨模态、跨任务的统一对比仍然缺失，而医疗世界模型的 L1–L2 集中现象 [22] 提示动作空间与干预验证协议的建设可能是比表征学习更前置的瓶颈。对生物多模态数据而言，这意味着直接套用 JEPA 或掩码目标未必带来增益，更可能有效的路径是先明确模态的"掩码单元"与"预测目标空间"、再选择与之匹配的防坍塌机制，并在统一评测协议下与仅值目标、重建目标做对照 [5][18]。

## 2 方法学


### 2.1 预测隐空间与世界模型

预测隐空间与世界模型这一方向的核心张力，在于是否必须在像素或点云等观测空间重建未来，还是可以在一个被学习出来的表征空间里完成预测。JEPA（Joint-Embedding Predictive Architecture）系列工作给出的答案是后者：预测目标不是未来的观测，而是未来观测的嵌入。这一选择带来的直接好处是避免生成式建模对高频细节的过度投入，但代价是必须处理表征坍塌这一结构性风险。围绕这一张力，过去数年间出现了从理论刻画、坍塌防止、模态扩展到决策对齐的多条研究线索，彼此之间存在明显的继承、竞争与未解争议。

在理论层面，LeJEPA 试图为 JEPA 提供一套可证明且可扩展的基础。它指出各向同性高斯是嵌入的最优分布，并用 SIGReg 约束嵌入分布，与 JEPA 预测损失结合，从而避免 stop-gradient、教师学生网络和调度器等启发式设计 [1]。实验覆盖 10+ 数据集和 60+ 架构，ViT-H/14 在 ImageNet-1k 冻结骨干线性评估达 79%，显示单超参、线性复杂度、跨架构稳定，实现约 50 行代码 [1]。这一结果的意义在于把防坍塌从工程技巧提升为分布约束问题，但其局限也很明确：理论假设与经验验证虽广，却未明确讨论跨全部真实下游任务的预测风险最优性边界 [1]。与之形成对照的是 SiamJEPA，它回到学生网络结构本身，采用掩码孪生学生编码器并配 EMA 教师网络，可视为 PhiNet 的 JEPA 形式 [2]。实验发现孪生编码器对 JEPA 目标起正则作用，提升表征可分性并加速早期学习，在有限训练预算下持续优于单编码器 JEPA 变体，线性探测精度高于需更长训练的 MAE [2]。两条路线在防坍塌机制上分歧明显：LeJEPA 主张去掉教师与学生、用分布正则替代，SiamJEPA 则保留 EMA 教师并强化学生侧结构，二者都报告了稳定训练，但评估主要集中在 ImageNet 线性探测，尚未在统一协议下直接对比 [1][2]。

变分视角为 JEPA 与生成式建模之间架起了桥梁，也带来了关于"JEPA 究竟是什么"的争议。Var-JEPA 论证 JEPA 与变分推断在结构上等价，标准 JEPA 可视为确定性特例，并据此推导出用单一 ELBO 显式建模隐变量生成结构的 Var-JEPA，实例化为表格版 Var-T-JEPA [3]。实验显示其在真实表格基准上超过 T-JEPA，且无需启发式反坍缩正则即可获得有意义表征与隐空间不确定性量化 [3]。VJEPA 走得更远，将 JEPA 从确定性回归推广为概率形式，学习未来隐状态的概率预测分布，并证明其与预测状态表示和贝叶斯滤波统一；进一步提出 BJEPA，用专家乘积分解预测信念以支持零样本任务迁移与约束满足 [4]。在含高方差干扰的噪声线性系统（Noisy TV 玩具实验）中，VJEPA/BJEPA 成功滤除高方差干扰，避免生成式基线的表征坍缩，并可采样构建可信区间 [4]。这两项工作共同指向一个判断：JEPA 的确定性形式可能只是更一般的概率世界模型的特例，而概率化带来的不确定性量化是纯确定性 JEPA 难以提供的 [3][4]。但两者的验证范围都相当有限，Var-JEPA 仅实例化表格数据，未验证图像/视频等模态 [3]；VJEPA 仅玩具实验验证，未在大规模高维真实环境评估 [4]。因此"变分化是否在大规模视觉与机器人任务上仍然成立"仍是开放问题。

坍塌问题在具体模态上的表现与对策差异，构成了另一条对比线索。BiJEPA 针对对称预测的表征爆炸问题引入表征向量范数正则化，训练前向与后向两个预测器，强制数据片段间循环一致可预测性 [23]。在合成周期信号、Lorenz 混沌轨迹与 MNIST 上稳定收敛无坍塌，捕获混沌系统语义结构，并学习到可生成与泛化的时空表征 [23]。其局限是仅在合成信号、Lorenz 与 MNIST 上验证，未扩展至大规模真实数据 [23]。与之相对，A JEPA Recipe for Tabular Foundation Models 给出了一个偏负面的结果：研究在表格基础模型先验上能否训练 JEPA 潜目标而不崩溃，提出值头读编码器场、潜目标用 EMA 差分、隐藏单元以掩码 token 进入预测器的配方，并用平台停止协议对比 [5]。收敛后 JEPA 臂在 147 个数据集上仍落后仅值目标臂，分类 32:70 胜负（按名 29:63），回归 8:24，且需 1.42 倍步数、1.66 倍墙钟达平台 [5]。这一结果与 LeJEPA、SiamJEPA 报告的稳定增益形成直接冲突：在表格模态上，潜空间预测目标并未带来收益，反而付出更高计算代价，且收敛后未超越仅值目标臂，每臂仅一次运行 [5]。这提示 JEPA 的收益可能高度依赖模态与数据特性，而非普遍规律。

视频与图像模态的规模化验证主要由 V-JEPA 2 与 LeVJEPA 推进。V-JEPA 2 在超 100 万小时互联网视频上预训练动作无关 JEPA 架构，对齐大语言模型后在多个视频问答任务达 SOTA，SSv2 77.3%、EK100 39.7 recall@5、PerceptionTest 84.0、TempCompass 76.9 [6]。它进一步基于少于 62 小时 Droid 机器人视频后训练出 V-JEPA 2-AC 世界模型，在 Franka 机械臂上零样本部署，实现基于图像目标的抓取放置规划 [6]。其局限是机器人规划仅用 62 小时 Droid 数据，泛化性待验证 [6]。LeVJEPA 则从效率角度挑战这一路线，作为首个用 LeJEPA 无坍缩目标训练的视频编码器，去除目标编码器、预测器、stop-gradient 与掩码重建，仅用全局-局部不变性损失加 SIGReg，并随机丢弃 95% patch token，支持块因果注意力 [7]。同数据同轮次下以 5.6–20.8× 更少预训练算力匹配或超 V-JEPA 2，同 FLOPs 下 ImageNet-1K 超最强视频基线 7.6 点，运动中心精度近 DINOv2 两倍 [7]。其局限是未提代码公开，运动中心基准仅保持竞争力 [7]。两者在"是否需要复杂防坍塌机制"上分歧明显：V-JEPA 2 代表大规模工程化路线，LeVJEPA 则主张极简目标即可在更少算力下达到可比甚至更好结果，但后者尚未在机器人规划等下游任务上与前者直接对比 [6][7]。

3D 与跨模态方向展示了 JEPA 在数据稀缺场景下的适配能力。3D-JEPA 采用多块采样生成信息丰富的上下文块与多个目标块，并用上下文感知解码器持续注入上下文信息以预测目标块表征，在 PB_T50_RS 上 150 预训练 epoch 达 88.65% 准确率，预训练 epoch 更少且精度更高 [10]。其局限是未充分讨论多块采样策略对不同 3D 数据分布的泛化性 [10]。Point-JEPA 引入 sequencer 对点云块嵌入排序，基于索引高效计算并利用邻近性进行目标和上下文选择，共享邻近性计算提升效率，无需输入空间重建或额外模态即可达到 SOTA，ModelNet40 线性 SVM 分类 93.7±0.2%，并在四个少样本学习框架上均创 SOTA [11]。其局限是未明确讨论 sequencer 对复杂点云分布、跨域泛化和预训练成本的限制 [11]。CrossJEPA 则针对 3D 数据稀缺，利用图像基础模型知识，训练预测器从 3D 点云推断特定渲染 2D 视图的嵌入，并采用冻结教师与目标嵌入缓存提升效率，在 ModelNet40 和 ScanObjectNN 线性探测上取得 SOTA，分别达 94.2% 和 88.3% [12]。其局限是依赖图像基础模型，未验证真实大规模 3D 场景 [12]。三者在 3D 表征学习上路径不同：3D-JEPA 与 Point-JEPA 在 3D 内部做自监督，CrossJEPA 借 2D 基础模型跨模态蒸馏，后者的更高数值部分来自外部先验而非纯 3D 自监督，因此直接比较需谨慎 [10][11][12]。

图与高能物理等非视觉模态的 JEPA 应用，进一步检验了架构的通用性。Graph-JEPA 将 JEPA 用于图级表征学习，采用掩码建模，从上下文子图潜表征预测被掩码子图潜表征，并用单位双曲线二维坐标预测目标赋予隐式层次，学习到高语义表达表征，在图分类、回归和区分非同构图任务上表现良好 [25]。其局限是未明确讨论图规模扩展、复杂图结构泛化和预测目标计算成本 [25]。HEP-JEPA 提出基于 Transformer 的高能物理基础模型，采用 JEPA 自监督策略，在含 1 亿喷注的 JetClass 数据集上预训练，用部分喷注成分预测未见成分的嵌入，在 top tagging 和轻夸克-胶子喷注区分等下游任务上与高能物理 SOTA 模型可比 [26]。其局限是仅用 JetClass 预训练，未覆盖更多对撞机数据 [26]。这两项工作说明 JEPA 的"预测嵌入而非重建"原则可以迁移到非欧几里得与非图像数据，但 Graph-JEPA 的双曲线坐标目标与 HEP-JEPA 的部分成分预测都是针对领域结构的定制设计，通用性边界仍不清楚 [25][26]。

运动与内容特征的联合学习是 JEPA 早期的重要探索。MC-JEPA 用联合嵌入预测架构在共享编码器中联合学习光流和内容特征，结合光流估计目标与自监督学习目标，使内容特征融入运动信息 [27]。实验发现该方法在无监督光流基准上达到与现有方法相当的性能，并在图像和视频语义分割等下游任务上与常见自监督方法相当 [27]。其局限是未明确讨论共享编码器中运动与内容目标冲突、光流标注依赖或复杂场景泛化限制 [27]。这一工作与后续 V-JEPA 2、LeVJEPA 的关系值得注意：MC-JEPA 强调运动信息对内容表征的增益，而 LeVJEPA 报告运动中心精度近 DINOv2 两倍 [27][7]，两者都指向运动信号在视频表征中的价值，但 MC-JEPA 依赖光流监督目标，LeVJEPA 则完全不含此类显式运动目标，说明运动信息的注入方式存在多条路径。

世界模型用于规划与决策时，潜空间预测的"决策相关性"成为焦点。DINO-WM 利用 DINOv2 预训练的块特征预测未来块特征，在不重建视觉世界的情况下建模视觉动态，在离线轨迹上训练，通过动作序列优化实现目标达成，将目标特征作为预测目标支持任务无关规划 [8]。实验在六个环境上实现零样本行为求解，无需专家演示或奖励建模，超越先前 SOTA [8]。其局限是依赖预训练 DINOv2 特征，未验证其他特征或真实机器人 [8]。D-JEPA 则识别出决策局部预测差距：预测隐距离更近的候选动作可能实际失败 [9]。它用有界置换等变算子从已执行结果中学习候选未来间的决策相关关系，并将决策结构写入 JEPA 兼容的未来表征，在隐控制、操作、真实机器人和自动驾驶上提升动作选择，PushT 达 87.89% 成功率，RoboTwin 平均提升 15.04 点，真实机器人任务提升 17 点 [9]。其局限是依赖已执行候选结果监督，需预训练预测几何 [9]。DINO-WM 与 D-JEPA 的差异在于前者假设潜空间距离与任务进度一致，后者明确否定这一假设并引入决策对齐监督，二者在"潜空间几何是否天然适合规划"上构成直接争议 [8][9]。

在机器人规划的具体实现上，多项工作围绕潜空间预测的稳定性与物理接地展开。Toward Physically Grounded JEPA World Models 提出端到端 JEPA 世界模型，在潜在预测基础上增加逆动力学和状态对齐目标，逆动力学防止潜在坍缩并使潜在转移包含动作信息，状态对齐将连续表示锚定到物理状态 [28]。在四个基准任务上，TwoRoom 达 100%、PushT 达 98%、OGBench-Cube 达 87%，消融显示状态对齐一致提升规划成功率 [28]。其局限是 Reacher 任务仅与基线相当，过渡子空间维度分析有限 [28]。Does Latent Planning Survive Point Clouds? 将三种典型 JEPA 设计（冻结编码器、分布先验、动作敏感）提升到点云观测，重新感知 stable-worldmodel 基准使仅观测模态不同 [29]。所有设计均无坍缩，Point-LeWM 与图像基线统计等价，Point-Delta-JEPA 在几何移动最多时表现最强，还提出从当前潜在和目标 3D 位姿构造目标潜在，无需目标观测即可规划 [29]。其局限是距离噪声会破坏最稀疏场景，仅仿真验证 [29]。Flow-JEPA 则针对 LeWM 确定性自回归预测的误差累积和对视觉扰动敏感问题，用条件流匹配以高斯源轨迹生成未来潜状态序列，替代逐点一步转移回归，保持无重建 JEPA 框架 [24]。在四个环境上干净观测成功率 86%→92%，噪声下 67%→86% [24]。其局限是工作进展中，未报告更大规模或更长时域泛化 [24]。这三项工作共同处理潜动力学鲁棒性，但路径不同：物理接地靠额外监督目标，点云工作靠观测模态适配，Flow-JEPA 靠生成式流匹配替代确定性回归，三者在噪声与几何移动场景下的相对优势尚未在统一基准上交叉验证 [28][29][24]。

动作条件与无动作视频的学习是另一条并行线索。Unified World Models 在统一 Transformer 中集成动作扩散与视频扩散过程，各模态由独立扩散时间步控制，通过控制扩散时间步可灵活表示策略、前向动态、逆向动态与视频生成器 [30]。实验表明其预训练策略比模仿学习更泛化鲁棒，并能利用无动作视频数据进一步提升性能 [30]。其局限是未明确给出定量指标与真实世界任务规模细节 [30]。CLAW 从无动作视频中端到端自监督学习连续潜动作世界模型，用对抗潜正则与扩散视频生成同时训练潜动作模型和世界模型，从视觉观察推断动作如何引起环境变化，潜动作具语义性，可支持从观察模仿、动作迁移与目标导向规划，并超越现有方法 [31]。其局限是全文未公开，缺乏定量指标与规模细节 [31]。UniJEPA 则在共享潜空间联合学习光度预测（图像级变换）与时间预测（视频级动态），用单一 next-embedding 预测损失加高斯正则化端到端训练，无需 EMA、stop-gradient 或预训练编码器，并证明可防坍塌 [32]。在图像、视频与控制基准上匹配或超越任务专用 JEPA，动作条件后训练后支持零样本规划，规划速度比生成式世界模型快数十倍 [32]。其局限是动作条件后训练依赖离线轨迹，未验证真实机器人部署 [32]。这三项工作在"如何获得动作条件能力"上分歧明显：UWM 用扩散时间步统一多模态，CLAW 用对抗正则从无动作视频推断潜动作，UniJEPA 用单一预测损失统一光度与时间目标，三者的防坍塌与动作推断机制互不相同，且都缺乏大规模真实机器人验证 [30][31][32]。

自动驾驶与导航场景提供了时空世界模型的专门检验。AD-LiST-JEPA 提出面向自动驾驶的自监督 JEPA 世界模型，从多帧 LiDAR 预测未来时空表征，通过 JEPA 在潜空间学习世界模型，避免生成式方法的高算力与幻觉问题，并规避表征坍塌 [33]。以 LiDAR 占据完成与预测（OCF）为下游任务，初步实验表明预训练编码器带来更好 OCF 性能 [33]。其局限是仅概念验证实验，未给出大规模定量对比与完整基准结果 [33]。GLAM 提出基于全局时空记忆的目标条件潜世界模型，并构建 GLAM NAV 导航系统，模型以 JEPA 式潜预测在地图级 token 上联合预测未来地图表示与机器人中心路点潜变量，用预训练路点编解码器监督解码 [34]。在 Habitat/HM3D 的 ObjectNav 子集上，成功率与 SPL 均优于复现的 BSC-Nav 基线 [34]。其局限是仅预测专家数据中的未来观测与计划，非任意动作反事实 [34]。两者都强调潜空间预测对生成式方法的替代，但 AD-LiST-JEPA 面向占据预测、GLAM 面向导航规划，任务与评估协议不同，且前者仅概念验证，后者限于专家轨迹，均未触及任意动作反事实预测这一世界模型的核心能力 [33][34]。

探索与在线学习场景揭示了世界模型在先验错位下的脆弱性。Plan2Explore 通过规划主动寻找预期未来新颖性进行自监督探索，用集成动力学预测下一图像嵌入的分歧作为内在奖励，在潜空间想象 rollout 中反向传播优化探索策略，学习全局世界模型 [35]。无任务监督下优于先前自监督探索方法，几乎匹配有奖励 oracle，并支持零样本或少样本适应下游任务 [35]。其局限是依赖集成动力学分歧，未广泛验证真实机器人 [35]。Baba in Wonderland 研究先验错位下仅靠交互证据在线归纳可执行世界模型，Alice 把失败候选更新视为结构信号，将保留冲突精炼为假设类，并引导探索新颖且欠表示的转移 [36]。在替换语义标签的 Baba in Wonderland 上显著提升学习效果，消融证明类精炼与类感知探索均有效 [36]。其局限是仅单一游戏环境验证，未提代码公开 [36]。Plan2Explore 假设集成分歧能可靠指示新颖性，Baba in Wonderland 则显示当先验本身错位时，需要把失败转化为结构信号并精炼假设类，二者对"探索信号来源"的理解不同，且都未在真实机器人上验证 [35][36]。

任务中心潜空间与生成式世界模型的效率对比，构成收束性的一组证据。Back to Parsimonious Latents 提出 TC-WM，把冻结视觉基础模型嵌入当作语义脚手架而非最终状态空间，通过线性投影得到紧凑动态潜空间，用对比学习对齐智能体物理状态子空间，并重建嵌入保留视觉结构 [37]。理论上可辨识任务中心潜因子，在 Robomimic 与 D4RL 上实现更优世界建模与更精确控制 [37]。其局限是依赖预训练视觉基础模型，全文未公开 [37]。Music-JEPA 将音乐视为动作条件系统，音频为状态、pianoroll 为乐器动作，给定当前音频状态和动作预测未来音频状态，完全离线使用成对音频-pianoroll 数据训练，学到的表示支持节拍跟踪、作曲家识别、调性估计等下游任务，并可通过规划搜索最佳动作实现钢琴转录 [38]。其局限是仅钢琴领域，离线训练无环境交互 [38]。SANA-WM 则代表生成式世界模型的规模化路线，2.6B 参数开源世界模型原生支持一分钟 720p 视频生成与精确相机控制，采用混合线性注意力、双分支相机控制、两阶段生成与鲁棒标注流程，动作跟随精度优于开源基线，视觉质量接近工业级模型且效率显著提升 [39]。其训练需 64 张 H100 训练 15 天，单 GPU 生成 60 秒 720p，蒸馏版单张 RTX 5090 NVFP4 下 34 秒去噪 60 秒 720p，训练仍需 64 张 H100，计算成本较高 [39]。UniJEPA 报告规划速度比生成式世界模型快数十倍且精度相当 [32]，与 SANA-WM 的高训练成本形成对照，但两者任务不同（规划 vs 视频生成），效率对比需限定在规划场景 [32][39]。TC-WM 与 Music-JEPA 则分别从任务中心潜因子和动作条件音频预测两个方向，说明紧凑潜空间在特定领域可以替代通用生成式建模，但都依赖领域特定的监督结构或数据配对 [37][38]。

综合来看，预测隐空间与世界模型这一方向尚未收敛。防坍塌机制上，LeJEPA 的分布正则、SiamJEPA 的孪生学生、BiJEPA 的范数正则、Var-JEPA 与 VJEPA 的变分目标各自成立，但表格模态的负面结果 [5] 与 3D、视频模态的正面结果 [10][7] 并存，说明收益高度依赖模态与数据特性。决策对齐上，D-JEPA 明确否定潜空间距离与任务进度一致的假设 [9]，而 DINO-WM 的成功又表明在特定特征下该假设可近似成立 [8]。概率化与生成式路线上，VJEPA/BJEPA 与 Var-JEPA 主张概率形式更一般 [4][3]，Flow-JEPA 用流匹配替代确定性回归 [24]，而 SANA-WM 显示生成式世界模型在视频质量与相机控制上仍有独立价值 [39]。这些分歧的根源在于评估协议不统一：多数工作仅在自有基准或仿真环境验证，真实机器人部署规模有限，跨模态、跨任务的统一对比仍然缺失。

### 2.2 掩码与自蒸馏表征

掩码建模与自蒸馏这两条路线在近年的自监督表征学习中逐渐从对立走向交叉。早期综述将自监督学习按目标归纳为生成式、对比式和生成-对比式（对抗）三类，并指出自监督利用输入数据自身作为监督即可惠及多种下游任务 [40]。这一分类框架为后续讨论提供了坐标：掩码自编码器属于生成式路线，对比学习与自蒸馏属于另一侧，而近年的工作不断尝试把两侧的目标统一起来。

掩码自编码器在视觉领域的规模化验证始于 MAE。它随机掩码输入图像块并重建缺失像素，采用仅编码可见块的非对称编码器和轻量解码器，掩码比例约 75%，ViT-Huge 在 ImageNet-1K 达到 87.8% 准确率，训练加速 3 倍以上，迁移性能超过监督预训练 [13]。这一结果确立了"高掩码率 + 非对称结构"作为掩码图像建模的基本配方。但该工作未明确讨论局限，其有效性依赖高比例掩码与大规模模型训练 [13]。与之形成对照的是更早的系统性复现研究，它通过统一实验揭示 CNN 设计标准配方不总适用于自监督学习，调整架构与训练策略即可大幅提升性能并超越此前 SOTA [41]；另一项工作把两种自监督方法扩展到 1 亿张图像，在 9 个数据集任务上建立基准，发现可匹配或超越监督预训练，但现有方法仍不足以充分利用大规模数据，未学到有效高层语义 [42]。这两项早期研究共同提示：数据规模与任务难度的匹配，而非单纯的方法堆叠，才是自监督收益的关键变量。

视频域的 VideoMAE 把这一配方推向时序维度。它采用极高比例（90%-95%）的视频管状掩码使重建任务更具挑战性，用 vanilla ViT 在无标签视频上预训练，仅用约 3k-4k 视频即在 Kinetics-400 达 87.4%、Something-Something V2 达 75.4%、UCF101 达 91.3%、HMDB51 达 62.6%，且无额外数据 [43]。该工作明确提出数据质量比数据数量更重要，但其高掩码率依赖视频时序冗余，域偏移仍是问题 [43]。音频域的 Audio-MAE 则把图像 MAE 简单扩展至音频频谱图：编码器以高掩码率只处理非掩码 token，解码器重排并补掩码 token 重建频谱图，并在解码器引入局部窗口注意力，在六个音频和语音分类任务上取得新 SOTA，超过使用外部监督预训练的模型 [44]。不过它需在目标数据集上以较低掩码率微调编码器 [44]。从视频到音频，掩码重建的跨模态迁移显示出较强的通用性，但各模态对掩码率与微调策略的敏感度并不一致。

三维与结构化数据上的掩码建模面临额外挑战。点云掩码自编码器针对位置信息泄漏和信息密度不均问题，将点云划分为不规则点块并高比例随机掩码，用非对称标准 Transformer 自编码器和移位掩码 token 从可见点块重建被掩码点块，在 ScanObjectNN 达 85.18%、ModelNet40 达 94.04%，少样本分类提升 1.5%-2.3% [45]。该工作未明确讨论高比例掩码、点云密度不均和位置泄漏处理的计算成本或泛化边界 [45]。NeRF-MAE 则把掩码自编码器用于隐式 NeRF 表征，将 NeRF 体素网格作为密集输入，利用相机轨迹采样规范化场景，随机掩码 patch 并用 3D Swin Transformer 重建，在超 180 万张位姿 RGB 图像上预训练，编码器可有效用于 3D 迁移学习 [46]。但它依赖相机轨迹采样，掩码自编码器应用于隐式 NeRF 表征存在困难 [46]。高能物理领域的 MPM 进一步把掩码思想推广到无序集合：掩码粒子并预测其由预训练 VQ-VAE 离散化得到的 token 身份，学习置换不变函数，并研究离散化、置换不变性和顺序影响，模型可微调用于监督和弱监督喷注分类，并能用小规模微调数据迁移到新类别和新数据域 [47]。其局限在于依赖预训练 VQ-VAE 离散 token，未明确讨论离散化误差和跨任务泛化上限 [47]。这些工作共同表明，掩码建模的"重建目标"从像素扩展到体素、点块和离散 token 后，如何定义掩码单元与目标空间成为方法设计的核心分歧。

语音领域的 HuBERT 提供了另一种思路：不直接重建连续特征，而是用离线聚类提供对齐目标，先对连续语音特征做 k-means 聚类，再仅在掩码区域预测隐藏单元标签，并迭代聚类 [48]。实验发现从 100 簇 k-means 和两轮迭代开始，在 Librispeech 与 Libri-light 多规模微调下可匹配或超越 wav2vec 2.0，1B 参数模型在 dev-other/test-other 相对 WER 降低最高 19%/13% [48]。该工作依赖离线聚类步骤的一致性，未明确讨论聚类质量与计算开销等局限 [48]。HuBERT 与 Audio-MAE 构成音频自监督的两条对照路线：前者预测离散隐藏单元，后者重建频谱图，二者都在各自基准上取得领先，但目标空间的差异使它们对掩码率与微调方式的依赖明显不同。

对比学习一侧的发展为后续融合埋下伏笔。SimCLR 通过组合数据增强、表示与对比损失间可学习非线性变换、归一化嵌入与温度参数，最大化同一样本不同增强视图的一致性，ImageNet 线性评估达 76.5% top-1，较此前 SOTA 相对提升 7%，1% 标签微调达 85.8% top-5，12 个数据集中 10 个不逊于强监督基线 [49]。但其需大 batch 与长训练，算力开销大 [49]。MoCo 从字典查找视角构建带队列与动量编码器的动态字典，队列使字典大且一致，动量编码器保证特征一致性，在 ImageNet 线性协议上具竞争力，且在 PASCAL VOC、COCO 等 7 个检测/分割任务上可超越监督预训练，部分大幅领先 [50]。该工作全文未公开，未提代码与权重 [50]。BYOL 则完全去掉负样本，用在线网络从一幅图像的一种增强视图预测目标网络对同一图像另一增强视图的表征，目标网络用在线参数的慢速移动平均更新，ResNet-50 达 74.3% top-1、更大 ResNet 达 79.6% top-1，并在迁移和半监督基准上持平或优于当时最先进方法 [51]。其目标函数存在坍缩解，依赖预测器和慢速移动平均避免坍缩 [51]。SimCLR、MoCo 与 BYOL 的差异集中在负样本是否必要、字典如何维护以及坍缩如何避免，这三条路线后来都被吸收进掩码与自蒸馏的融合设计中。

DINO 把自蒸馏推向视觉 Transformer，将自监督实现为无标签自蒸馏，强调动量编码器、多裁剪训练和小 patch 的重要性，发现自监督 ViT 特征包含显式语义分割信息且是优秀 k-NN 分类器，小 ViT 达 78.3%，ViT-Base 线性评估达 80.1% [52]。该工作未明确讨论局限，依赖动量编码器、多裁剪和小 patch 等设计 [52]。DINO 的意义在于证明自蒸馏可以在没有负样本和重建目标的情况下产生具有语义结构的表征，这与掩码建模的局部感知形成互补。在病理图像这一极端规模场景中，研究者构建了含 30 亿张图像、42.3 万张切片的病理数据集，采用 MAE 和 DINO 两种自监督算法预训练视觉 Transformer，并在乳腺癌检测、炎症性肠病检测、雌激素受体预测、EGFR 突变预测和免疫治疗响应预测等六项临床任务上评估，结果显示病理数据预训练优于自然图像预训练，且 DINO 算法表现更佳 [14]。该工作仅对比 MAE 与 DINO，未覆盖更多 SSL 算法 [14]。这一结果对"掩码重建是否总是优于自蒸馏"提出了直接反例：在特定数据分布与任务上，自蒸馏路线的表现可以更好。

正是在这一背景下，统一掩码与对比/自蒸馏的尝试集中出现。CMAE 通过新设计统一对比学习与掩码图像建模，在线分支用非对称编码器-解码器重建掩码图像，动量分支用全图进行对比学习，并引入像素移位与特征解码器，发现其表征兼具实例判别性与局部感知性，迁移性能超越 MIM 对应方法 [15]。该工作未明确讨论计算开销与超参数敏感性 [15]。SiameseIM 则基于同一图像另一掩码视图预测增强视图的稠密表征，使用孪生网络，在线分支编码第一视图并按相对位置预测第二视图表征，目标分支编码第二视图，发现其可同时获得语义对齐与空间敏感性，在 ImageNet 微调与线性探测、COCO、LVIS 等下游任务上超越 ID 与 MIM [16]。该工作未明确讨论双分支训练的计算成本 [16]。CAE 走的是另一条统一路径：在编码表征空间做预测而非像素空间，采用编码器-回归器-解码器结构，编码器处理可见块，回归器预测掩码块表征，解码器重建掩码块，在分割、检测和分类等下游任务上迁移性能优越，且分离表征学习与预训练任务有益 [17]。但其需两阶段任务（表征预测+块重建），结构较复杂 [17]。CMAE、SiameseIM 与 CAE 分别从对比分支、孪生预测和表征空间回归三个角度回应同一问题：掩码重建学到的局部特征如何与实例级判别性共存。三者的共同结论是统一目标可以带来迁移增益，但对计算开销与结构复杂度的代价都未给出充分讨论。

联合嵌入预测架构（JEPA）把预测目标从像素或 token 空间彻底移到潜表征空间。I-JEPA 不依赖手工数据增强，从单个上下文块预测同一图像中多个目标块的表征，通过采样大尺度目标块和空间分布充分的上下文块引导语义表征，结合 Vision Transformer 后高度可扩展，用 16 张 A100 在 ImageNet 训练 ViT-Huge/14 少于 72 小时，在线性分类、物体计数和深度预测等下游任务表现强 [53]。该工作未明确讨论局限，依赖目标块尺度与上下文块信息量等掩码策略 [53]。I-JEPA 与 MAE 的关键差异在于预测目标空间：前者预测潜表征，后者重建像素，这直接影响了表征的抽象层级与训练效率。Bootleg 进一步把自蒸馏与多层潜表征预测结合，通过预测教师多个隐藏层的潜表征训练模型，用分层目标迫使模型同时捕获不同抽象层级特征，避免仅重建低层数据或依赖最终层非平稳自蒸馏目标，在 ImageNet-1K、iNaturalist-21、VTAB 冻结探针分类上较 I-JEPA 提升 +10%，并在 ADE20K、Cityscapes、COCO-Stuff 语义分割上显著优于可比基线 [54]。该工作未明确讨论多层教师目标带来的训练成本、教师设计依赖和跨模态扩展限制 [54]。Bootleg 与 I-JEPA 的对比说明，教师信号的层级选择本身就是一个独立的设计维度，而不仅仅是目标空间的附属选择。

JEPA 范式向语言、音频与音视频的扩展显示出该框架的可迁移性，也暴露出不同模态下的边界。DLLM-JEPA 将 JEPA 目标引入掩码扩散语言模型，利用扩散噪声调度从单一输入构造两个视图，无需配对数据，每步单次梯度传播，较 LLM-JEPA 减少 33% 训练 FLOPs，在 4 任务×2 骨干上一致提升，GSM8K 提升 +1.8pp，并观察到几何漂移增大而功能遗忘更小的分离现象 [55]。其增益在稳定设置下较温和，主要验证于有限任务与骨干 [55]。Audio-JEPA 将 JEPA 范式适配到音频，用 ViT 骨干预测掩码梅尔频谱块的隐表征而非重建原始音频，在无标签 AudioSet 上随机块掩码预训练，在 X-ARES 套件上评估语音、音乐和环境声任务，性能与 wav2vec 2.0 和 data2vec 相当，但训练数据不足其五分之一且无需调参 [56]。该工作仅将原模型直接迁移到音频，未做超参调优 [56]。MJEPA 则用单一统一编码器与单一预测目标做音视频联合嵌入预测学习，目标同时施加于模态内与跨模态预测，跨模态预测对共享编码器收益关键，冻结 ViT-g 在 AudioSet-20K 超最佳冻结基线 6.8 mAP 以上，在 ESC-50 与 FSD50K 超全微调模型，且用少 10 倍视频数据在视频基准上具竞争力 [57]。该工作未提代码公开，跨模态预测缺失时共享编码器退化 [57]。DLLM-JEPA、Audio-JEPA 与 MJEPA 共同显示 JEPA 在文本、音频和音视频上的适应性，但三者的增益幅度差异明显：语言域提升温和，音频域以极少数据追平专用方法，音视频域则在冻结评估上大幅领先，这种差异提示 JEPA 的收益高度依赖模态冗余结构与跨模态监督信号的存在。

自蒸馏路线在单细胞等科学数据上同样展现出替代重建的潜力。scRep 用潜空间自蒸馏替代观测空间重建来学习单细胞表征，通过对同一细胞不同扰动视图做动量师生对齐，并在细胞和基因两个层面施加自蒸馏目标，在约 280 万细胞上预训练即取得冻结表征基准最优总体表现，扩到 3072 万细胞仍有效 [58]。该工作未在文中明确说明局限，仅评估冻结表征，未做任务微调 [58]。scRep 与病理图像中 DINO 优于 MAE 的结果 [14] 相互呼应，共同构成对"掩码重建在科学数据上普遍占优"这一假设的质疑。图领域的 GraphCL 则从增强视角提供另一条线索：设计四类图增强引入不同先验，通过最大化不同增强视图间特征一致性学习不变表征，在半监督、无监督、迁移和对抗攻击四设置下，无需调增强幅度或复杂架构即达到与 SOTA 相似或更好的泛化、迁移与鲁棒性 [59]。其增强类型与幅度需选择，参数化增强仅初步实验 [59]。GraphCL 与 SimCLR、MoCo 共享对比学习的基本逻辑，但图增强的设计空间与图像增强差异显著，说明"增强不变性"这一自蒸馏/对比路线的核心假设在不同数据结构上的实现成本并不相同。

把上述证据放在一起，可以看到几条清晰的张力线。其一是目标空间的争议：MAE、VideoMAE、Audio-MAE、点云 MAE、NeRF-MAE 与 MPM 都在观测或离散 token 空间重建 [13][43][44][45][46][47]，而 CAE、I-JEPA、Bootleg、Audio-JEPA、DLLM-JEPA、MJEPA 与 scRep 则把目标移到潜表征空间 [17][53][54][56][55][57][58]。HuBERT 介于两者之间，预测的是离线聚类得到的离散隐藏单元而非原始波形 [48]。这一分布本身说明，重建目标的选择并非简单的技术偏好，而是与模态冗余度、数据规模和下游任务类型紧密耦合。

其二是负样本与坍缩避免机制的争议。SimCLR 与 MoCo 依赖负样本或队列维护字典 [49][50]，BYOL 与 DINO 则证明无负样本的自蒸馏可以避免坍缩并取得有竞争力的结果 [51][52]。CMAE 把动量分支的对比学习与在线分支的掩码重建并置 [15]，SiameseIM 用孪生网络预测另一视图的稠密表征 [16]，二者都在尝试用掩码结构替代或补充负样本所提供的判别性信号。这些工作的共同点是承认单一目标不足以同时获得局部感知与实例判别性，但对如何组合目标、组合带来的计算代价，均未给出充分讨论 [15][16]。

其三是数据规模与数据质量的权衡。VideoMAE 明确主张数据质量比数据数量更重要 [43]，而扩展到 1 亿图像的早期研究则发现现有方法不足以充分利用大规模数据 [42]。Audio-JEPA 用不足 wav2vec 2.0 五分之一的训练数据达到相当性能 [56]，MJEPA 用少 10 倍视频数据在视频基准上具竞争力 [57]，scRep 在 280 万细胞上即取得冻结表征基准最优 [58]。这些结果从不同侧面支持"目标设计可以部分替代数据规模"的判断，但病理图像工作显示 30 亿张图像的规模本身带来了超越自然图像预训练的收益 [14]，说明规模与目标设计并非互相替代，而是在不同数据域中各自发挥主导作用。

其四是评估协议的差异对结论的影响。I-JEPA、Bootleg、Audio-JEPA、MJEPA 与 scRep 都强调冻结表征或线性探针评估 [53][54][56][57][58]，而 MAE、VideoMAE、Audio-MAE 与点云 MAE 的报告以微调或线性评估为主 [13][43][44][45]。Bootleg 报告的 +10% 提升是在冻结探针分类上相对 I-JEPA 测得 [54]，MJEPA 的 6.8 mAP 优势也是在冻结 ViT-g 设置下 [57]，这些数字与微调协议下的增益不可直接比较。评估协议的不统一使得跨工作的"谁更好"难以直接判定，也解释了为何同一路线在不同报告中会呈现相反的优劣排序。

综合来看，掩码与自蒸馏表征的演进呈现出从单一目标到混合目标、从观测空间到潜空间、从图像到多模态与科学数据的扩散趋势。生成式与对比式的早期分类 [40] 在今天的证据中已难以清晰维持：CMAE、SiameseIM、CAE、Bootleg 都同时带有生成与判别成分 [15][16][17][54]，DLLM-JEPA 把扩散噪声调度与 JEPA 目标结合 [55]，MJEPA 把模态内与跨模态预测统一在单一编码器下 [57]。与此同时，各工作对自身局限的讨论普遍不足：MAE、DINO、I-JEPA、CMAE、SiameseIM、Bootleg、scRep 等均未明确讨论计算开销、超参数敏感性或扩展边界 [13][52][53][15][16][54][58]，这使得跨工作的公平比较更加困难。未来这一方向的关键问题可能不在于再提出一种新的掩码比例或教师层级，而在于建立能够同时衡量局部感知、语义判别性与训练效率的统一评估框架，并明确不同目标空间在不同模态与数据规模下的适用边界。

### 2.3 新架构：状态空间与线性注意力

在扩散模型的高保真图像生成任务中，Transformer 架构长期占据主导地位，但其自注意力机制的二次复杂度构成了显著的计算瓶颈。LaMamba-Diff 针对这一子问题提出了一种混合架构方案，其核心是 Local Attentional Mamba 块，将自注意力与 Mamba 状态空间模型相结合，并嵌入 U-Net 架构中以同时捕捉全局上下文与局部细节 [60]。该工作的关键设计动机在于：纯 Mamba 结构虽能实现线性时间建模，却可能在压缩过程中损失局部细节信息，而局部注意力的引入正是为了弥补这一潜在缺陷 [60]。从效率指标看，LaMamba-Diff 的最大模型相较 DiT-XL/2 减少了 62% 的 GFLOPs，参数量相当或更少，同时在 ImageNet 256×256 上的性能超越了 DiT 的各规模变体 [60]。这一结果说明，在图像生成这一子问题上，状态空间模型与注意力的混合设计能够在计算效率与生成质量之间取得优于纯 Transformer 的折中。

然而，该证据也暴露了当前方法的一个未决争议点。作者在 limitations 中明确指出，尚未充分讨论 Mamba 压缩导致局部细节信息损失的残余影响 [60]。这意味着，尽管 Local Attentional Mamba 块在架构层面引入了局部注意力作为补偿，但 Mamba 分支本身的信息压缩是否会在某些生成场景下造成不可逆的细节退化，仍缺乏系统性的消融或可视化分析。从时间线看，该工作发表于 2024 年，代表了状态空间模型向扩散生成领域渗透的一次尝试，其代码已在 GitHub 开源，为后续复现与改进提供了基础 [60]。与纯线性注意力或纯 Mamba 方案相比，LaMamba-Diff 的混合路线在 ImageNet 256×256 与 512×512 两个分辨率上均报告了结果，但证据中仅给出了 256×256 上超越 DiT 各规模的结论，512×512 的具体对比数据未被展开 [60]。因此，在评估状态空间架构是否真正替代自注意力时，该工作提供的证据更倾向于支持“混合互补”而非“线性替代”的立场，而 Mamba 压缩带来的细节损失残余影响，仍是该方向需要进一步厘清的关键问题 [60]。

## 3 数据与基准

（本节暂无入库证据）

## 4 向科学数据的迁移

自监督表征学习向科学数据的迁移，首先遇到的困难是数据形态与自然图像的根本差异：粒子云、基因组序列、表格记录与单细胞表达谱都不具备规整的网格结构，掩码与重建的直觉需要重新设计。高能物理领域的工作给出了一个直接回应。[21] 提出 JetParticle-JEPA（JP-JEPA），以 Particle Transformer 为骨干，直接从连续粒子云预测被掩码粒子的潜表征，而不做分词，也不重建原始输入。这一选择与视觉 JEPA 的思路一致：把预测目标放在潜空间而非输入空间，避免把建模容量浪费在不可预测的低层细节上。在 JetClass 上，该方法在全量数据下媲美全监督 SOTA，在低标签场景下超越监督基线，并显著优于现有 SSL 方法，同时在缺失探测器信息时展现鲁棒性 [21]。但作者明确承认，结果仅基于模拟数据，未报告真实探测器数据上的表现 [21]。这一限制并非细枝末节：喷注标记的模拟—现实差距正是该领域长期痛点，潜空间预测能否吸收探测器效应，目前没有证据支持。

同样的 JEPA 逻辑被迁移到基因组序列。[20] 的 JEPA-DNA 把联合嵌入预测架构嵌入基因组基础模型的持续训练流程，在潜空间监督全局序列嵌入，预测被掩码基因组片段的功能表征，并与传统生成目标联合优化。在 17 项基因组基准上，线性探测与零样本性能一致提升，监督线性探测达到新 SOTA，超过 DNABERT-2、NTv3、HyenaDNA 及 MLM/NTP 基线 [20]。作者据此主张潜语义对齐优于纯 token 重建 [20]。值得注意的是其定位：JEPA-DNA 只是持续预训练阶段，必须依赖已有 GFM，且未明确跨物种泛化边界 [20]。这与 JP-JEPA 从零训练的姿态形成对照，也提示 JEPA 在科学数据中的角色可能更多是"对齐器"而非"从零学习器"。表格数据方向提供了另一条证据。[61] 的 T-JEPA 完全放弃数据增强，改为从同一样本一个特征子集的潜表征预测另一子集的潜表征，实现潜空间掩码重建；分类与回归任务显著提升，部分方法持续超越或匹配 GBDT，并引入正则化 token 以稳定结构化数据训练 [61]。三篇工作共享"潜空间预测优于输入重建"的假设，但验证强度差异明显：JP-JEPA 有明确的低标签优势，JEPA-DNA 有 17 项基准的一致提升，T-JEPA 则仍受限于未在大规模表格上验证 [21][20][61]。

然而，这一假设在单细胞基因组学中遭到部分反驳。[18] 在超过 2000 万细胞上系统基准测试了多种掩码策略的 MAE 与对比学习，评估细胞类型预测、基因表达重建、跨模态预测与数据整合四类下游任务，结论是 MAE 优于对比学习，与计算机视觉中对比学习占优的趋势相反，并在零样本细胞类型预测中表现突出 [18]。该研究同时给出一个更克制的判断：SSL 的优势场景有限，主要见于迁移学习 [18]。这与 JEPA-DNA 宣称的"一致提升"存在张力：前者强调 SSL 收益的条件性，后者强调跨 17 项基准的普遍性，两者的分歧可能源于任务选择与预训练起点不同，而非单纯的方法优劣。与此同时，[62] 的 RegFormer 走了一条不同路线：把基因调控网络先验与 Mamba 状态空间架构结合，在 2500 万人类细胞上做生成式预训练，学习基因表达动态与调控层级，在细胞注释、GRN 重建、遗传扰动预测与药物响应建模等基准上持续超越 scGPT 与 Geneformer [62]。它未明确讨论跨物种与跨组织泛化能力 [62]。RegFormer 与上述自监督工作构成方法论对照：前者把领域结构（调控层级）显式注入架构，后者依赖掩码预测目标隐式获取结构，二者在单细胞任务上的相对优势尚无直接比较证据。

把视野拉到系统层面，两篇工作揭示了迁移到科学数据的另一类瓶颈：能力层级与部署形态。[22] 综述医疗世界模型，覆盖医学影像诊断、EHR 疾病进展建模与机器人手术规划三域，提出 L1 时序预测到 L4 规划控制的能力分级，并逐级评估现有系统，发现多数系统仅达 L1–L2，少数达到 L3，L4 罕见，同时指出动作空间不明确、干预验证薄弱、多模态状态构建不完整等跨领域缺口 [22]。作为综述，它未提出新模型，也缺乏统一量化评测 [22]，但其分级框架对前述工作有定位价值：JP-JEPA 与 JEPA-DNA 基本停留在 L1 表征与预测层面，距离反事实与规划尚有距离。[63] 的 Mini-JEPA 则展示了另一种工程路径：由五个 22M 参数传感器专用 Mini-JEPA 组成模型舰队，共享 ViT 骨干与 JEPA 训练配方，每个模型重建与其传感器物理匹配的环境变量，再由路由 LLM 选择合适传感器。各模型最佳预测变量即其传感器所观测变量，R² 达 0.97（高程/温度）、0.81（降水）；联合模型对土壤湿度等变量的 ΔR² 达 0.031；路由命中率完美，d=1.10, p=0.031；在物理匹配问题上媲美 Google AlphaEarth，联合检索在单传感器问题上显著优于 AlphaEarth [63]。其局限同样明确：总体问题类型聚合增益有限，且路由 LLM 依赖闭源模型 [63]。Mini-JEPA 的"专用小模型 + 路由"策略与 RegFormer、JEPA-DNA 的"单一基础模型 + 持续预训练"策略形成鲜明对比，前者以物理匹配换取可解释性与效率，后者以规模与先验换取跨任务泛化，两种路线在科学数据上的取舍尚无定论。综合来看，这七项证据共同勾勒出一条从潜空间预测目标、领域结构注入到能力分级与部署架构的迁移链条，但真实数据验证、跨域泛化边界与统一评测的缺失，仍是该方向最突出的未解问题 [21][20][22]。

## 5 评测、可复现性与争议

在计算病理学这一高风险临床场景中，自监督基础模型的评测正暴露出“算法优劣”与“落地可用”之间的张力。doi:10.1038/s41467-025-58796-1 对公开自监督病理基础模型进行了临床基准评测，系统梳理了 CTransPath、Phikon、UNI、Virchow、Prov-GigaPath 等模型的训练数据与算法，并采用“瓦片编码加聚合”的两阶段流程评估下游任务 [19]。其核心发现是 DINO 算法优于 MAE，这为掩码重建与自蒸馏两类自监督范式在病理领域的相对有效性提供了直接比较 [19]。但该工作同时强调，各模型在瓦片级与切片级任务上表现并不一致，说明单一任务或单一层级的排名无法外推为普遍结论 [19]。更关键的争议在于可复现性与领域成熟度：论文指出数字病理采用率低、数据与算力缺乏，且全切片图像分辨率极高，这些约束使基准评测本身难以覆盖真实临床的多样性，病理领域的自监督学习仍处于早期阶段 [19]。换言之，DINO 优于 MAE 的结论成立，但其可迁移边界受制于数据、算力与任务层级，评测的“临床”标签与实际的临床覆盖之间仍存在落差。

与上述静态基准评测形成对照，arxiv:2609.21740 把评测焦点转向世界模型在测试时的自适应能力，并试图用参数效率回应“重训练不可行”的现实约束。其提出的 Sandwich-Residuals 冻结预训练世界模型，仅学习预测器前后的轻量残差修正，残差用模型自监督预测误差在线优化，无需奖励、标签或源域数据 [64]。在 AdaJEPA 基准的 21 种条件下，该方法成功率达到冻结模型的 1.3 倍，同时少调 97–99% 参数；在复合偏移下达到 1.9 倍，并在 DINO-WM 三维操作上得到验证 [64]。这一结果与病理基准的结论构成有意义的对照：前者表明自监督表征的评测高度依赖下游任务与数据条件，后者则显示在不改动预训练表征的前提下，仅靠测试时残差即可显著改善世界模型的鲁棒性 [19][64]。但该工作也坦承局限：复合偏移下其表现仅与内部块自适应相当，并未超越最强 AdaJEPA 变体 [64]。因此，两篇证据共同指向一个争议点——评测中的“领先”往往是条件性的：病理基准中 DINO 的优势受限于瓦片与切片任务的不一致及领域早期状态，而世界模型自适应中 1.3 倍与 1.9 倍的提升也伴随“未超越最强变体”的边界 [19][64]。可复现性方面，后者提供项目页公开，前者则受制于数据与算力缺乏，二者在开放程度与评测可重复性上的差异，进一步说明该方向亟需统一、可审计的评测协议 [19][64]。

## 6 空白与趋势

在掩码建模与自蒸馏的融合之外，JEPA 路线把预测目标彻底移出观测空间，这一选择在 2024—2026 年间迅速扩散到几乎所有可被"掩码"的数据模态，但扩散过程中暴露出一个被反复触及却未被系统回答的问题：潜空间预测的收益究竟来自目标空间的选择，还是来自防坍塌机制的设计。表格模态给出了最直接的负面证据：在 147 个数据集上，收敛后的 JEPA 臂仍落后仅值目标臂，分类 32:70、回归 8:24，且需 1.42 倍步数与 1.66 倍墙钟达平台 [5]。这与 LeJEPA 在 ImageNet-1k 线性评估达 79%、SiamJEPA 在有限预算下持续优于单编码器 JEPA 的正面结果 [1][2] 形成直接张力。一个合理的解释是：表格数据的特征子集之间缺乏视觉数据中那种空间局部性与语义层次，潜空间预测所依赖的"可预测结构"本身较弱，因此目标空间的选择收益被计算代价抵消。但这一解释尚未被任何工作直接检验，也没有跨模态的统一协议来分离"目标空间"与"防坍塌机制"两个变量。

概率化与生成式建模的回归是另一条正在成形的趋势。Var-JEPA 论证 JEPA 与变分推断结构等价、标准 JEPA 是确定性特例 [3]，VJEPA 进一步给出与预测状态表示和贝叶斯滤波的统一，并用 BJEPA 的专家乘积分解支持零样本任务迁移与约束满足 [4]。Flow-JEPA 则用条件流匹配生成未来潜状态序列替代逐点一步回归，在噪声观测下成功率从 67% 提升到 86% [24]。三条工作从变分、贝叶斯滤波、流匹配三个角度指向同一判断：确定性一步预测在噪声与长时域下不足，概率化或轨迹级生成是必要的补充。但三者的验证都停留在玩具系统、表格或小规模仿真，VJEPA 仅玩具实验 [4]，Var-JEPA 仅表格实例化 [3]，Flow-JEPA 未报告更大规模或更长时域泛化 [24]。概率化 JEPA 能否在 V-JEPA 2 级别的视频规模与真实机器人上保持优势，目前没有任何证据。

决策对齐正在从"潜空间距离近似任务进度"的默认假设转向显式建模。D-JEPA 识别出决策局部预测差距——预测隐距离更近的候选动作可能实际失败——并用有界置换等变算子从已执行结果中学习候选未来间的决策相关关系，PushT 达 87.89%，RoboTwin 平均提升 15.04 点，真实机器人提升 17 点 [9]。这与 DINO-WM 依赖 DINOv2 特征、假设潜空间距离可用于目标达成规划的成功形成对照 [8]。Toward Physically Grounded JEPA 用逆动力学与状态对齐把连续表示锚定到物理状态，TwoRoom 达 100%、PushT 达 98% [28]；Does Latent Planning Survive Point Clouds? 则显示在点云观测下三种典型 JEPA 设计均无坍缩，Point-Delta-JEPA 在几何移动最多时最强 [29]。这些工作共同表明，潜空间几何是否天然适合规划取决于观测模态、动作空间与任务结构，而非 JEPA 的固有属性，但没有任何工作在统一基准上交叉验证这些对齐机制的相对贡献。

真实机器人部署与跨模态统一评估是当前最明显的空白。V-JEPA 2 的机器人规划仅用少于 62 小时 Droid 数据，泛化性待验证 [6]；UniJEPA 的动作条件后训练依赖离线轨迹，未验证真实机器人部署 [32]；AD-LiST-JEPA 仅概念验证，未给出大规模定量对比 [33]；GLAM 仅预测专家数据中的未来观测与计划，非任意动作反事实 [34]；Plan2Explore 与 Baba in Wonderland 都未在真实机器人上验证 [35][36]。与此同时，SANA-WM 以 2.6B 参数、64 张 H100 训练 15 天的成本展示生成式世界模型在视频质量与相机控制上的独立价值 [39]，而 UniJEPA 报告规划速度比生成式世界模型快数十倍 [32]，两者任务不同却常被并置比较，效率对比缺乏限定条件。跨模态、跨任务的统一评测协议，以及真实机器人上任意动作反事实预测的验证，是这一方向从概念验证走向可信世界模型的关键缺口。

综合上述证据，可以归纳出五条趋势与对应的空白。第一，防坍塌机制从启发式走向分布约束与理论刻画，LeJEPA 用 SIGReg 约束各向同性高斯嵌入、去掉 stop-gradient 与教师学生 [1]，SiamJEPA 保留 EMA 教师并强化孪生学生结构 [2]，BiJEPA 用范数正则处理对称预测的表征爆炸 [23]，但表格模态的负面结果 [5] 说明这些机制并非普遍有效，空白在于跨模态统一协议下分离"目标空间"与"防坍塌机制"的对照实验。第二，JEPA 从确定性回归走向概率化与轨迹级生成，Var-JEPA、VJEPA/BJEPA、Flow-JEPA 分别用变分、贝叶斯滤波与流匹配给出概率形式 [3][4][24]，空白在于这些形式尚未在 V-JEPA 2 级别的视频规模与真实机器人上验证。第三，决策对齐从隐式假设走向显式建模，D-JEPA 否定潜空间距离与任务进度一致 [9]，物理接地与点云适配工作分别用额外监督目标与观测模态适配提升规划 [28][29]，空白在于这些对齐机制缺乏统一基准上的交叉验证。第四，动作条件能力从有动作数据扩展到无动作视频，UWM 用扩散时间步统一多模态 [30]，CLAW 用对抗潜正则从无动作视频推断潜动作 [31]，UniJEPA 用单一预测损失统一光度与时间目标 [32]，空白在于三者都缺乏大规模真实机器人验证，且防坍塌与动作推断机制互不相同、无法直接比较。第五，生成式世界模型与潜空间世界模型在效率与质量上形成分工，SANA-WM 展示生成式路线在视频质量与相机控制上的独立价值但训练成本高 [39]，UniJEPA 与 TC-WM 则说明紧凑潜空间在规划与特定领域可替代通用生成式建模 [32][37]，空白在于两者效率对比需限定任务场景，且缺乏同一任务上质量-效率-泛化性的三维权衡分析。

## 7 未归类新证据

在跨域世界模型与自监督预测学习这一方向上，最新的一项工作提出了一个颇具野心的统一框架。JEPA-Anything 的核心主张是：不同领域——包括视觉、生物、临床、控制、分子、物理场与天气——的动力学预测任务，可以共享同一套域无关的预测架构，而不必为每个领域单独设计归纳偏置 [65]。其方法上的关键设计是「正交预测因子分解」：将潜在目标表征拆解为若干互补且正交的因子，每个因子由专用通路学习，再在一个共享的预测设计中重新组合 [65]。这一思路与经典 JEPA 路线形成对照——后者通常在单一模态或单一领域内学习预测性表征，而 JEPA-Anything 试图把「预测什么」与「在哪个世界预测」解耦，让因子结构承担跨域迁移的职责。值得注意的是，该工作并非只做架构层面的思辨，而是在七个领域、十个动力学任务上与匹配的 JEPA 基线做了系统对比，并报告了全部任务上的提升 [65]。这种「全胜」式的报告本身值得审慎看待：它一方面说明正交因子分解在多种动力学形态下具有可迁移性，另一方面也提示基线可能未针对每个领域做充分调优，因而提升幅度在不同任务间的可比性仍需进一步检验。

具体到量化证据，该工作在若干子问题上给出了较有区分度的结果。在干预式动力学任务 Interventional Pong 上，单干预预测误差降低了 34.8% [65]，这一数字直接指向模型对干预后状态演化的建模能力，而非仅仅拟合观测分布。在分子系统上，四系统 100 步预测误差达到最低 [65]，说明正交因子分解在长时程误差累积场景下仍具优势。更具理论意味的是轨道标度律的验证：拟合得到的标度指数斜率为 -1.4991 [65]，这一接近 -1.5 的数值被该工作用作框架捕捉真实物理标度行为的证据，并声称获得了湿实验与轨道标度律的双重验证 [65]。然而，这里存在一个需要指出的张力：一个域无关的统一框架在获得跨域通用性的同时，作者自己也承认「在部分领域可能牺牲领域特异性」[65]。这意味着，全面超越基线的结论与领域特异性受损的风险是并存的——前者是任务平均意义上的收益，后者则可能在特定领域的精细结构上表现为损失，而现有证据并未给出逐领域的消融来厘清这一权衡。此外，该工作强调代码与模型公开 [65]，为后续复现与在更多领域上检验其通用性提供了条件，但其跨域主张目前仍主要建立在十个动力学任务之上，尚不足以断言该框架对所有「世界」都成立。

## 参考文献

1. LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics. arXiv.org 2025. https://doi.org/10.48550/arXiv.2511.08544
2. SiamJEPA: On the Role of Siamese Student Encoders in JEPA. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.04044
3. Var-JEPA: A Variational Formulation of the Joint-Embedding Predictive Architecture - Bridging Predictive and Generative Self-Supervised Learning.  2026. https://arxiv.org/abs/2603.20111v2
4. VJEPA: Variational Joint Embedding Predictive Architectures as Probabilistic World Models.  2026. https://arxiv.org/abs/2601.14354v1
5. A JEPA Recipe for Tabular Foundation Models.  2026. https://arxiv.org/abs/2609.25541
6. V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning. arXiv.org 2025. https://doi.org/10.48550/arXiv.2506.09985
7. LeVJEPA: Efficient&Scalable Video Pretraining without the Heuristics.  2026. https://arxiv.org/abs/2608.27395
8. DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning. International Conference on Machine Learning 2024. https://doi.org/10.48550/arXiv.2411.04983
9. D-JEPA: A Decision-Aligned Latent World Model.  2026. https://arxiv.org/abs/2609.24749
10. 3D-JEPA: A Joint Embedding Predictive Architecture for 3D Self-Supervised Representation Learning. arXiv.org 2024. https://doi.org/10.48550/arXiv.2409.15803
11. Point-JEPA: A Joint Embedding Predictive Architecture for Self-Supervised Learning on Point Cloud. IEEE Workshop/Winter Conference on Applications of Computer Vision 2024. https://doi.org/10.1109/WACV61041.2025.00714
12. CrossJEPA: Cross-Modal Joint-Embedding Predictive Architecture for Efficient 3D Representation Learning from 2D Images. arXiv.org 2025. https://doi.org/10.48550/arXiv.2511.18424
13. Masked Autoencoders Are Scalable Vision Learners. Computer Vision and Pattern Recognition 2021. https://doi.org/10.1109/CVPR52688.2022.01553
14. Computational Pathology at Health System Scale - Self-Supervised Foundation Models from Three Billion Images. arXiv.org 2023. https://doi.org/10.48550/arXiv.2310.07033
15. Contrastive Masked Autoencoders are Stronger Vision Learners. IEEE Transactions on Pattern Analysis and Machine Intelligence 2022. https://doi.org/10.1109/TPAMI.2023.3336525
16. Siamese Image Modeling for Self-Supervised Vision Representation Learning. Computer Vision and Pattern Recognition 2022. https://doi.org/10.1109/CVPR52729.2023.00212
17. Context Autoencoder for Self-supervised Representation Learning. International Journal of Computer Vision 2022. https://doi.org/10.1007/s11263-023-01852-4
18. Delineating the Effective Use of Self-Supervised Learning in Single-Cell Genomics. bioRxiv 2024. https://doi.org/10.1038/s42256-024-00934-3
19. A clinical benchmark of public self-supervised pathology foundation models.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58796-1
20. JEPA-DNA: Grounding Genomic Foundation Models through Joint-Embedding Predictive Architectures.  2026. https://arxiv.org/abs/2602.17162v3
21. JetParticle-JEPA: An Efficient Self-Supervised Representation Learning method for Jet Tagging in High-Energy Physics. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.14813
22. Beyond Generative AI: World Models for Clinical Prediction, Counterfactuals, and Planning.  2025. https://arxiv.org/abs/2511.16333v1
23. BiJEPA: Bi-directional Joint Embedding Predictive Architecture for Symmetric Representation Learning.  2026. https://arxiv.org/abs/2603.00049v1
24. Flow-JEPA: Flow Matching for Robust Latent Dynamics in JEPA World Models.  2026. https://arxiv.org/abs/2608.29029
25. Graph-level Representation Learning with Joint-Embedding Predictive Architectures. Trans. Mach. Learn. Res. 2023. https://doi.org/10.48550/arXiv.2309.16014
26. HEP-JEPA: A foundation model for collider physics using joint embedding predictive architecture. arXiv.org 2025. https://doi.org/10.48550/arXiv.2502.03933
27. MC-JEPA: A Joint-Embedding Predictive Architecture for Self-Supervised Learning of Motion and Content Features. arXiv.org 2023. https://doi.org/10.48550/arXiv.2307.12698
28. Toward Physically Grounded JEPA World Models for Goal-Conditioned Robotic Planning.  2026. https://arxiv.org/abs/2609.03565
29. Does Latent Planning Survive Point Clouds? Action-Conditioned JEPA World Models for Geometric Observations.  2026. https://arxiv.org/abs/2608.29434
30. Unified World Models: Coupling Video and Action Diffusion for Pretraining on Large Robotic Datasets. Robotics 2025. https://doi.org/10.48550/arXiv.2504.02792
31. CLAW: Learning Continuous Latent Action World Models via Adversarial Latent Regularization. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.04130
32. UniJEPA: A Unified Joint-Embedding Predictive Architecture for Task-Agnostic Visual World Modeling.  2026. https://arxiv.org/abs/2608.07409v1
33. Self-Supervised JEPA-based World Models for LiDAR Occupancy Completion and Forecasting.  2026. https://arxiv.org/abs/2602.12540v1
34. GLAM: Training a latent world model over global spatiotemporal memory for active exploration and navigation.  2026. https://arxiv.org/abs/2609.14561
35. Planning to Explore via Self-Supervised World Models. International Conference on Machine Learning 2020. https://arxiv.org/abs/2005.05960
36. Baba in Wonderland: Online Self-Supervised Dynamics Discovery for Executable World Models. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.16725
37. Back to Parsimonious Latents: Learning Task-Centric World Models from Visual Foundations. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.25620
38. Music-JEPA: Learning a World Model of Sound from Action. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.22000
39. SANA-WM: Efficient Minute-Scale World Modeling with Hybrid Linear Diffusion Transformer. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.15178
40. Self-Supervised Learning: Generative or Contrastive. IEEE Transactions on Knowledge and Data Engineering 2020. https://doi.org/10.1109/TKDE.2021.3090866
41. Revisiting Self-Supervised Visual Representation Learning. Computer Vision and Pattern Recognition 2019. https://doi.org/10.1109/CVPR.2019.00202
42. Scaling and Benchmarking Self-Supervised Visual Representation Learning. IEEE International Conference on Computer Vision 2019. https://doi.org/10.1109/ICCV.2019.00649
43. VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training. Neural Information Processing Systems 2022. https://doi.org/10.48550/arXiv.2203.12602
44. Masked Autoencoders that Listen. Neural Information Processing Systems 2022. https://doi.org/10.48550/arXiv.2207.06405
45. Masked Autoencoders for Point Cloud Self-supervised Learning. European Conference on Computer Vision 2022. https://doi.org/10.48550/arXiv.2203.06604
46. NeRF-MAE: Masked AutoEncoders for Self-Supervised 3D Representation Learning for Neural Radiance Fields. European Conference on Computer Vision 2024. https://doi.org/10.48550/arXiv.2404.01300
47. Masked particle modeling on sets: towards self-supervised high energy physics foundation models. Machine Learning: Science and Technology 2024. https://doi.org/10.1088/2632-2153/ad64a8
48. HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units. IEEE/ACM Transactions on Audio Speech and Language Processing 2021. https://doi.org/10.1109/taslp.2021.3122291
49. A Simple Framework for Contrastive Learning of Visual Representations. International Conference on Machine Learning 2020. https://arxiv.org/abs/2002.05709
50. Momentum Contrast for Unsupervised Visual Representation Learning. Computer Vision and Pattern Recognition 2019. https://doi.org/10.1109/cvpr42600.2020.00975
51. Bootstrap Your Own Latent: A New Approach to Self-Supervised Learning. Neural Information Processing Systems 2020. https://arxiv.org/abs/2006.07733
52. Emerging Properties in Self-Supervised Vision Transformers. IEEE International Conference on Computer Vision 2021. https://doi.org/10.1109/ICCV48922.2021.00951
53. Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture. Computer Vision and Pattern Recognition 2023. https://doi.org/10.1109/CVPR52729.2023.01499
54. Self-Distillation of Hidden Layers for Self-Supervised Representation Learning. arXiv.org 2026. https://doi.org/10.48550/arXiv.2603.15553
55. DLLM-JEPA: Joint Embedding Predictive Architectures for Masked Diffusion Language Models.  2026. https://arxiv.org/abs/2606.00091v1
56. Audio-JEPA: Joint-Embedding Predictive Architecture for Audio Representation Learning.  2025. https://arxiv.org/abs/2507.02915v1
57. MJEPA: A Simple and Scalable Joint-Embedding Predictive Architecture for Audio-Visual Learning. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.25225
58. scRep: A Latent-Space Self-Distilled Foundation Model for Single-Cell Representation Learning. bioRxiv 2026. https://doi.org/10.64898/2026.08.31.747784
59. Graph Contrastive Learning with Augmentations. Neural Information Processing Systems 2020. https://arxiv.org/abs/2010.13902
60. LaMamba-Diff: Linear-Time High-Fidelity Diffusion Models Based on Local Attention and Mamba. arXiv.org 2024. https://doi.org/10.48550/arXiv.2408.02615
61. T-JEPA: Augmentation-Free Self-Supervised Learning for Tabular Data.  2024. https://arxiv.org/abs/2410.05016v3
62. RegFormer: a single-cell foundation model powered by gene regulatory hierarchies.. Nature communications 2026. https://doi.org/10.1038/s41467-026-72198-x
63. Mini-JEPA Foundation Model Fleet Enables Agentic Hydrologic Intelligence.  2026. https://arxiv.org/abs/2605.14120v1
64. Sandwich-Residuals: Parameter-Efficient Test-time Adaptation of World Models.  2026. https://arxiv.org/abs/2609.21740
65. JEPA-Anything: Learning Predictive Models across Different Worlds.  2026. https://arxiv.org/abs/2609.20800
