# 世界模型与自监督表征学习 · 方向背景报告

证据 65 篇 · 覆盖度 0.46 · 第 3 轮 · 更新 2026-09-27

## 摘要（TL;DR）

- JEPA 把自监督学习的目标从像素重建转向潜空间预测，用上下文片段的潜表征预测目标片段的潜表征，绕开生成式方法对高熵观测的重建 [1]。
- V-JEPA 2 在超 100 万小时互联网视频上预训练动作无关 JEPA，在 SSv2 上达 77.3% top-1、EK100 上 39.7 recall@5、PerceptionTest 上 84.0、TempCompass 上 76.9，并基于少于 62 小时 Droid 机器人视频后训练出 V-JEPA 2-AC 世界模型 [2]。
- LeJEPA 从理论上论证各向同性高斯是嵌入的最优分布，提出 SIGReg 正则与预测损失结合，覆盖 10+ 数据集与 60+ 架构，ViT-H/14 在 ImageNet-1k 冻结骨干线性评估达 79% [3]。
- SiamJEPA 主张学生网络使用孪生编码器并配 EMA 教师，认为孪生结构对 JEPA 目标起正则作用，在有限训练预算下持续优于单编码器 JEPA 变体 [4]。
- 表格领域实证显示，收敛后 JEPA 臂在 147 个真实数据集上仍落后仅值目标臂，分类为 32:70 胜负（按名 29:63）、回归为 8:24，且需 1.42 倍步数与 1.66 倍墙钟达平台 [5]。
- D-JEPA 识别出决策局部预测差距，用有界置换等变算子从已执行结果中学习候选未来间的决策相关关系，在 PushT 上达 87.89% 成功率，RoboTwin 平均提升 15.04 点，真实机器人任务提升 17 点 [6]。
- Flow-JEPA 用条件流匹配以高斯源轨迹生成未来潜状态序列，在四个环境上干净观测成功率由 86% 升至 92%、噪声下由 67% 升至 86% [7]。
- 有工作把三种典型 JEPA 设计提升到点云观测，所有设计均无坍缩，Point-LeWM 与图像基线统计等价，Point-Delta-JEPA 在场景点移动最多（0.3–15%）时表现最强 [8]。
- SANA-WM 是 2.6B 参数开源世界模型，训练用 64 张 H100 共 15 天，蒸馏版在单张 RTX 5090 NVFP4 下 34 秒去噪 60 秒 720p [9]。
- 医疗世界模型综述提出 L1 时序预测到 L4 规划控制的分级，发现多数系统仅达 L1–L2，少数 L3，L4 罕见，并指出动作空间不明确、干预验证薄弱等跨领域缺口 [10]。

## 1 背景与定义

世界模型与自监督表征学习的方向边界，可由"预测什么"与"在哪预测"两个轴划定。生成式掩码重建（MAE、VideoMAE、Audio-MAE）在观测空间或离散 token 空间预测被掩码部分，训练信号可靠、实现简单，但对高冗余模态计算效率低，且训练目标不优先学习高层概念特征 [11]。联合嵌入预测架构（JEPA）把预测目标移到潜空间，用上下文片段的潜表征预测目标片段，绕开对高熵观测的重建 [1]。对比与自蒸馏路线（SimCLR、MoCo、BYOL、DINO）则通过视图间表征对齐学习不变性，其中 DINO 以动量编码器、多裁剪与小 patch 实现无标签自蒸馏 [12]。三条主线共享"用数据自身构造监督"的前提，分歧在于监督信号落在像素、离散 token、潜表征还是视图对齐上。**这一分歧并非纯技术偏好，而是决定了方法在高冗余模态上的效率、在科学数据上的迁移性，以及是否具备动作条件预测与规划能力。**

演化脉络上，掩码建模与自蒸馏在视觉领域先后确立范式，随后向视频、音频、点云、3D、图、表格、基因组、高能物理等模态扩散。MAE 以约 75% 掩码率与非对称编码器-解码器确立图像范式 [13]；VideoMAE 用 90%-95% 管状掩码把这一思路推到视频，并强调数据质量比数量更重要 [14]；点云、音频、NeRF、病理等模态各自针对位置泄漏、信息密度不均、隐式表征难掩码等问题做了适配 [15][16][17][18]。JEPA 路线则从 I-JEPA 的图像块预测出发 [19]，经 V-JEPA 2 的百万小时视频预训练与机器人后训练 [2]、DINO-WM 的冻结特征零样本规划 [20]，延伸到点云、图、表格、基因组、喷注、音频、音视频与扩散语言模型 [21][1][22][23][24][25][26][27]。**JEPA 的扩张速度明显快于掩码建模，但其跨模态、跨任务的普适优势尚未在表格等领域得到稳定验证** [5]。

核心问题之一是防表征坍塌，且不同工作给出的方案相互竞争甚至冲突。LeJEPA 从理论上论证各向同性高斯是嵌入最优分布，用 SIGReg 正则与预测损失结合，避免 stop-gradient、教师学生与调度器等启发式，覆盖 10+ 数据集与 60+ 架构 [3]；SiamJEPA 则主张学生网络使用孪生编码器并配 EMA 教师，认为孪生结构本身起正则作用 [4]；BiJEPA 针对单向预测忽略逆向关系，强制循环一致可预测性并引入范数正则化 [28]；LeVJEPA 把无坍缩目标用于视频编码器，去除目标编码器、预测器、stop-gradient 与掩码重建 [29]。**这些方案在"是否需要教师/EMA/stop-gradient"上并未收敛，说明坍塌的成因与最优约束仍缺乏统一解释。**

核心问题之二是 JEPA 与概率生成模型的关系，同样存在明显分歧。Var-JEPA 主张 JEPA 与变分推断结构等价、标准 JEPA 只是确定性特例，据此推导出用单一 ELBO 建模隐变量的版本 [30]；VJEPA 把 JEPA 推广为概率形式并证明其与预测状态表示和贝叶斯滤波统一，进一步用 BJEPA 的专家乘积分解支持零样本任务迁移与约束满足 [31]。但表格领域的实证给出相反信号：潜项曾坍塌并把编码器带向常数映射，即便采用值头、EMA 差分目标与掩码 token 的配方，收敛后 JEPA 臂在 147 个真实数据集上仍落后仅值目标臂，且需 1.42 倍步数与 1.66 倍墙钟达平台 [5]。**概率化改造在理论上更完备，但尚未证明其能普遍解决潜目标的训练不稳定与收益不确定问题。**

核心问题之三是潜预测与决策的对齐。D-JEPA 识别出决策局部预测差距——预测隐距离更近的候选动作可能实际失败，用有界置换等变算子学习候选未来间的决策相关关系 [6]；另一项工作给端到端 JEPA 世界模型增加逆动力学与状态对齐目标，逆动力学防止潜坍缩并使潜转移包含动作信息，状态对齐把连续表示锚定到物理状态 [32]；Flow-JEPA 用条件流匹配替代逐点一步转移回归以缓解误差累积与视觉扰动敏感 [7]。几何观测是否适合潜空间规划也被直接检验：三种典型 JEPA 设计提升到点云后均无坍缩，Point-LeWM 与图像基线统计等价，Point-Delta-JEPA 在场景点移动最多时表现最强 [8]。**潜空间预测的效率优势已被反复确认，但其与动作条件、物理状态锚定、几何观测的耦合方式仍在快速演化，尚无公认设计。**

在科学数据迁移上，自监督范式的相对优势与视觉领域并不一致。单细胞基因组上覆盖超 2000 万细胞的系统基准发现 MAE 优于对比学习，与计算机视觉趋势相反，且 SSL 的优势场景有限、主要见于迁移学习 [33]；病理临床评测中 DINO 算法优于 MAE，但各模型在瓦片级与切片级任务上表现不一，领域仍处早期 [34]。RegFormer 把基因调控网络先验与 Mamba 状态空间架构结合，在 2500 万人类细胞上预训练并持续超越 scGPT 与 Geneformer [35]。**这提示在科学数据中，引入领域结构先验可能与单纯扩大自监督目标同样关键，而"哪种自监督目标更优"高度依赖模态与任务层级，不存在跨领域统一的排序。**

架构层面，状态空间模型与线性注意力被引入以缓解长序列的二次复杂度。LaMamba-Diff 用 Local Attentional Mamba 块融合自注意力与 Mamba，动机是 Mamba 将滤波后的全局上下文压缩进隐状态虽实现线性复杂度，却不可避免地带来细粒度局部依赖的信息损失 [36]；在 ImageNet 256×256 与 512×512 上，最大模型较 DiT-XL/2 减少 62% GFLOPs，并在 256×256 上超越 DiT 各规模 [36]。**线性复杂度与细粒度表征之间的取舍仍是开放争议，该工作自身也未充分讨论 Mamba 压缩导致局部细节信息损失的残余影响** [36]。这一取舍直接关系到世界模型在长时序、高分辨率观测上的可扩展性，也是 JEPA 路线与生成式路线共同面对的效率瓶颈。

综合来看，本方向的边界可概括为：以潜空间预测、掩码重建、对比/自蒸馏为三大训练信号来源，以状态空间模型与线性注意力为长序列架构支撑，以科学数据（组学、影像、时序、粒子、地理）为迁移验证场。**当前最突出的空白不在单一方法的性能提升，而在三个交叉处：潜目标训练稳定性的统一理论、潜预测与动作/物理状态的对齐设计、以及跨模态迁移中领域先验与自监督目标的相对权重。** 医疗世界模型综述发现多数系统仅达 L1–L2、L4 罕见，并指出动作空间不明确、干预验证薄弱等跨领域缺口 [10]；Mini-JEPA 的传感器舰队在物理匹配问题上表现良好，但总体问题类型聚合增益有限且路由依赖闭源模型 [37]。这些证据共同指向：**当任务涉及动作条件预测或跨传感器泛化时，当前自监督表征的迁移仍受限于状态构建与验证环节，而非表征学习本身** [10][37]。

## 2 方法学


### 2.1 预测隐空间与世界模型

联合嵌入预测架构（JEPA）把自监督学习的目标从像素重建转向潜空间预测，成为世界模型研究的一条主线。其核心做法是用上下文片段的潜表征预测目标片段的潜表征，从而绕开生成式方法对高熵观测的重建 [1]。这一范式被迅速推广到多种模态：点云上的 **Point-JEPA** 用 sequencer 对点块嵌入排序以选取目标与上下文，在 **ModelNet40** 线性 SVM 分类上达 **93.7±0.2%**，并在四个少样本框架上取得 SOTA [21]；**3D-JEPA** 采用多块采样与上下文感知解码器，在 **PB_T50_RS** 上 150 个预训练 epoch 达 **88.65%** 准确率 [38]；**CrossJEPA** 则用冻结教师从 3D 点云预测 2D 渲染视图嵌入，在 ModelNet40 与 ScanObjectNN 线性探测上分别达 **94.2%** 与 **88.3%** [39]。图数据上，**Graph-JEPA** 从上下文子图潜表征预测被掩码子图潜表征，并用单位双曲线二维坐标作为预测目标 [1]；高能物理中 **HEP-JEPA** 在含 **1 亿**喷注的 JetClass 上预训练，用部分喷注成分预测未见成分嵌入 [40]。

视频与视觉世界模型是证据最密集的方向。**V-JEPA 2** 在超 **100 万小时**互联网视频上预训练动作无关 JEPA，在 SSv2 上达 **77.3%** top-1、EK100 上 **39.7** recall@5、PerceptionTest 上 **84.0**、TempCompass 上 **76.9**，并基于少于 **62 小时** Droid 机器人视频后训练出 V-JEPA 2-AC 世界模型，在 Franka 机械臂上零样本执行图像目标抓取放置 [2]。**DINO-WM** 则直接以 DINOv2 预训练块特征为预测对象，在离线轨迹上训练，于六个环境实现零样本测试时行为求解，无需专家演示、奖励建模或逆模型 [20]。**MC-JEPA** 在共享编码器中联合学习光流与内容特征，在无监督光流基准上与现有方法相当，在图像与视频语义分割等下游任务上与常见自监督方法相当 [41]。

防表征坍塌是 JEPA 训练的核心难题，不同工作给出了相互竞争甚至冲突的方案。**LeJEPA** 从理论上论证各向同性高斯是嵌入的最优分布，提出 **SIGReg** 正则与预测损失结合，避免 stop-gradient、教师学生与调度器等启发式，覆盖 10+ 数据集与 60+ 架构，**ViT-H/14** 在 ImageNet-1k 冻结骨干线性评估达 **79%**，实现约 50 行代码、单超参与线性复杂度 [3]。**SiamJEPA** 则反其道而行，主张学生网络使用孪生编码器并配 EMA 教师，认为孪生结构对 JEPA 目标起正则作用，在有限训练预算下持续优于单编码器 JEPA 变体，线性探测精度高于需更长训练的 MAE [4]。**BiJEPA** 针对标准 JEPA 单向预测忽略逆向关系的问题，强制数据片段间循环一致可预测性，并引入表征向量范数正则化解决对称预测的表征爆炸，在合成周期信号、Lorenz 混沌轨迹与 MNIST 上稳定收敛无坍塌 [28]。**LeVJEPA** 把 LeJEPA 的无坍缩目标首次用于视频编码器，去除目标编码器、预测器、stop-gradient 与掩码重建，仅用全局-局部不变性损失加 SIGReg 并随机丢弃 **95%** patch token，同轮次下以 **5.6–20.8×** 更少预训练算力匹配或超 V-JEPA 2，同 FLOPs 下 ImageNet-1K 超最强视频基线 **7.6** 点 [29]。

JEPA 与概率生成模型的关系存在明显分歧。**Var-JEPA** 主张 JEPA 与变分推断在结构上等价，标准 JEPA 只是确定性特例，据此推导出用单一 ELBO 显式建模隐变量的 Var-JEPA，实例化为表格版 Var-T-JEPA，在真实表格基准上超过 T-JEPA，且无需启发式反坍缩正则即可获得隐空间不确定性量化 [30]。**VJEPA** 同样把 JEPA 从确定性回归推广为概率形式，学习未来隐状态的概率预测分布，并证明其与预测状态表示和贝叶斯滤波统一；进一步提出 **BJEPA** 用专家乘积分解预测信念以支持零样本任务迁移与约束满足，在含高方差干扰的噪声线性系统（Noisy TV 玩具实验）中成功滤除干扰，避免生成式基线的表征坍缩 [31]。但表格领域的实证给出了相反信号：在表格基础模型先验上，潜项曾坍塌并把编码器带向常数映射，即便采用值头读编码器场、EMA 差分目标与掩码 token 的配方，收敛后 JEPA 臂在 **147 个**真实数据集上仍落后仅值目标臂，分类为 32:70 胜负（按名 29:63）、回归为 8:24，且需 **1.42 倍**步数与 **1.66 倍**墙钟达平台 [5]。

面向控制的潜世界模型强调预测要与决策对齐。**D-JEPA** 识别出决策局部预测差距——预测隐距离更近的候选动作可能实际失败，于是用有界置换等变算子从已执行结果中学习候选未来间的决策相关关系，在 **PushT** 上达 **87.89%** 成功率，RoboTwin 平均提升 **15.04** 点，真实机器人任务提升 **17** 点 [6]。另一项工作给端到端 JEPA 世界模型增加逆动力学与状态对齐目标，逆动力学防止潜坍缩并使潜转移包含动作信息，状态对齐把连续表示锚定到物理状态，在 TwoRoom 达 **100%**、PushT 达 **98%**、OGBench-Cube 达 **87%**，消融显示状态对齐一致提升规划成功率 [32]。**Flow-JEPA** 针对 LeWM 确定性自回归预测的误差累积与视觉扰动敏感问题，用条件流匹配以高斯源轨迹生成未来潜状态序列，在四个环境上干净观测成功率由 **86%** 升至 **92%**、噪声下由 **67%** 升至 **86%** [7]。**GLAM** 以 JEPA 式潜预测在地图级 token 上联合预测未来地图表示与机器人中心路点潜变量，在 Habitat/HM3D 的 ObjectNav 子集上成功率与 SPL 均优于复现的 BSC-Nav 基线 [42]。

几何观测是否适合潜空间规划是一个被直接检验的问题。有工作把三种典型 JEPA 设计（冻结编码器、分布先验、动作敏感）提升到点云观测，并重新感知 stable-worldmodel 基准使仅观测模态不同：所有设计均无坍缩，**Point-LeWM** 与图像基线统计等价，**Point-Delta-JEPA** 在场景点移动最多（0.3–15%）时表现最强，还提出从当前潜在和目标 3D 位姿构造目标潜在、无需目标观测即可规划 [8]。**UniJEPA** 则试图统一分裂的目标设定，在共享潜空间联合学习光度预测与时间预测，用单一 next-embedding 预测损失加高斯正则化端到端训练，无需 EMA、stop-gradient 或预训练编码器，在图像、视频与控制基准上匹配或超越任务专用 JEPA，动作条件后训练后支持零样本规划，规划速度比生成式世界模型快数十倍 [43]。

从无动作视频中学习潜动作世界模型是另一条路径。**CLAW** 用对抗潜正则与扩散视频生成端到端联合训练潜动作模型与世界模型，从视觉观察推断动作如何引起环境变化，潜动作具语义性并支持从观察模仿、动作迁移与目标导向规划 [44]。**UWM** 在统一 Transformer 中集成动作扩散与视频扩散过程，各模态由独立扩散时间步控制，通过控制扩散时间步可灵活表示策略、前向动态、逆向动态与视频生成器，预训练策略比模仿学习更泛化鲁棒，并能利用无动作视频进一步提升 [45]。**TC-WM** 把冻结视觉基础模型嵌入当作语义脚手架而非最终状态空间，通过线性投影得到紧凑动态潜空间，用对比学习对齐智能体物理状态子空间并重建嵌入保留视觉结构，在 Robomimic 与 D4RL 上实现更优世界建模与更精确控制 [46]。

早期工作已确立"规划即探索"的思路。**Plan2Explore** 用集成动力学预测下一图像嵌入的分歧作为内在奖励，在潜空间想象 rollout 中反向传播优化探索策略，无任务监督下优于先前自监督探索方法并几乎匹配有奖励 oracle，支持零样本或少样本适应下游任务 [47]。近期工作把可执行性引入世界模型：**Alice** 研究先验错位下仅靠交互证据在线归纳可执行世界模型，把失败候选更新视为结构信号，将保留冲突精炼为假设类并引导探索新颖且欠表示的转移，在替换语义标签的 Baba in Wonderland 上显著提升学习效果 [48]。**Music-JEPA** 把音乐视为动作条件系统，音频为状态、pianoroll 为乐器动作，完全离线用成对音频-pianoroll 数据训练，学到的表示支持节拍跟踪、作曲家识别、调性估计等任务，并可通过规划搜索最佳动作实现钢琴转录 [49]。

生成式世界模型在效率与规模上仍占一席之地。**SANA-WM** 是 **2.6B** 参数开源世界模型，原生支持一分钟 720p 视频生成与精确相机控制，采用混合线性注意力、双分支相机控制、两阶段生成与鲁棒标注流程，训练用 **64 张 H100** 共 **15 天**，单 GPU 生成 60 秒 720p，蒸馏版在单张 RTX 5090 NVFP4 下 **34 秒**去噪 60 秒 720p，动作跟随精度优于开源基线且视觉质量接近工业级模型 [9]。这与 JEPA 路线形成对照：后者以潜空间预测换取效率与任务无关性，但在部分领域（如表格）的实证中尚未稳定超越非潜目标基线 [5]，其跨模态、跨任务的普适优势仍待更广泛验证。

### 2.2 掩码与自蒸馏表征

掩码建模与自蒸馏是自监督表征学习的两条主线，前者以重建或预测被掩码部分为训练信号，后者通过师生网络间的表征对齐避免坍缩。综述性工作将这一领域按目标归纳为生成式、对比式与生成-对比式三类，并指出自监督利用输入数据自身作为监督可惠及多种下游任务 [50]。早期研究已开始系统检验预训练任务与骨干架构的匹配问题，发现CNN设计配方不总适用于自监督学习，调整架构与训练策略可大幅提升性能并超越此前SOTA [51]；同期工作将两种自监督方法扩展至**1亿张图像**，在检测、表面法线估计、视觉导航等任务上匹配或超越监督预训练，但也指出当时方法不够“难”，未充分利用大规模数据、未学到有效高层语义 [52]。

对比学习路线以SimCLR与MoCo为代表。SimCLR通过强数据增强组合、表示与对比损失间的可学习非线性变换、归一化嵌入与温度参数，在ImageNet线性评估达**76.5% top-1**，较此前SOTA相对提升7%，1%标签微调达85.8% top-5 [53]。MoCo则从字典查找视角构建带队列与动量编码器的动态字典，在ImageNet线性协议上具竞争力，并在7个检测/分割任务上可超越监督预训练 [54]。BYOL进一步去掉负样本，用在线网络预测目标网络对同一图像另一增强视图的表征，ResNet-50达**74.3% top-1**、更大ResNet达79.6%，但目标函数存在坍缩解，依赖预测器和慢速移动平均避免坍缩 [55]。DINO将自监督实现为无标签自蒸馏，强调动量编码器、多裁剪与小patch，发现自监督ViT特征包含显式语义分割信息，小ViT k-NN达**78.3% top-1**，ViT-Base线性评估达80.1% [12]。

掩码自编码器路线由MAE确立基本范式：随机掩码输入图像块并重建缺失像素，采用仅编码可见块的非对称编码器与轻量解码器，掩码约**75%**输入，ViT-Huge在ImageNet-1K达87.8%，训练加速3倍以上，迁移性能超过监督预训练 [13]。VideoMAE将这一思路扩展到视频，采用极高比例（**90%-95%**）的视频管状掩码，在仅3k-4k视频上即取得Kinetics-400 87.4%、SSv2 75.4%、UCF101 91.3%、HMDB51 62.6%，且无额外数据，作者据此强调数据质量比数据数量更重要 [14]。Audio-MAE把MAE扩展至音频频谱图，编码器以高掩码率只处理非掩码token，解码器重排并补掩码token重建频谱图，并在解码器引入局部窗口注意力，在六个音频和语音分类任务上取得新SOTA [16]。点云领域则针对位置信息泄漏与信息密度不均，将点云划分为不规则点块并高比例随机掩码，用非对称Transformer自编码器重建，ScanObjectNN达**85.18%**、ModelNet40达94.04%，少样本分类提升1.5%-2.3% [15]。

掩码建模向更多模态与科学数据延伸。HuBERT用离线聚类提供对齐目标，仅在掩码区域预测隐藏单元标签并迭代聚类，从100簇k-means和两轮迭代开始即可匹配或超越wav2vec 2.0，1B模型在dev-other/test-other相对WER降低最高**19%/13%** [56]。MPM面向高能物理无序粒子集合，掩码粒子并预测其由预训练VQ-VAE离散化得到的token身份，学习置换不变函数，可微调用于监督和弱监督喷注分类并迁移到新类别与新数据域 [57]。NeRF-MAE把掩码自编码器用于NeRF辐射与密度网格，将体素网格作为密集输入、用相机轨迹采样规范化场景，在超**180万张**位姿RGB图像上预训练，编码器可有效用于3D迁移学习，但依赖相机轨迹采样，掩码自编码器应用于隐式NeRF表征存在困难 [17]。病理领域构建了含**30亿张**图像、42.3万张切片的病理数据集，用MAE和DINO预训练ViT并在六项临床任务上评估，发现病理数据预训练优于自然图像预训练，且DINO算法表现更佳 [18]。

在掩码与自蒸馏的交叉地带，多类工作试图兼取两者优势。CAE在编码表征空间而非像素空间做预测，采用编码器-回归器-解码器结构，编码器处理可见块、回归器预测掩码块表征、解码器重建掩码块，在分割、检测和分类等下游任务上迁移性能优越，作者认为分离表征学习与预训练任务有益 [58]。CMAE通过新设计统一对比学习与掩码图像建模，在线分支用非对称编码器-解码器重建掩码图像，动量分支用全图做对比学习，并引入像素移位与特征解码器，其表征兼具实例判别性与局部感知性，迁移性能超越MIM对应方法 [59]。SiameseIM基于同一图像另一掩码视图预测增强视图的稠密表征，用孪生网络让在线分支编码第一视图并按相对位置预测第二视图表征，目标分支编码第二视图，从而同时获得语义对齐与空间敏感性，在ImageNet微调与线性探测、COCO、LVIS等下游任务上超越ID与MIM [60]。Bootleg则预测教师多个隐藏层的潜表征，用分层目标迫使模型同时捕获不同抽象层级特征，避免仅重建低层数据或依赖最终层非平稳自蒸馏目标，在ImageNet-1K、iNaturalist-21、VTAB冻结探针分类上较I-JEPA提升**+10%**，并在ADE20K、Cityscapes、COCO-Stuff语义分割上显著优于可比基线 [11]。

联合嵌入预测架构（JEPA）代表另一条自蒸馏式路线。I-JEPA从单个上下文块预测同一图像中多个目标块的表征，不依赖手工数据增强，通过采样大尺度目标块和空间分布充分的上下文块引导语义表征，用**16张A100**在ImageNet训练ViT-Huge/14少于72小时，在线性分类、物体计数和深度预测等下游任务表现强 [19]。Audio-JEPA将JEPA适配到音频，用ViT骨干预测掩码梅尔频谱块的隐表征而非重建原始音频，在无标签AudioSet上随机块掩码预训练，在X-ARES套件上性能与wav2vec 2.0和data2vec相当，但训练数据不足其五分之一且无需调参 [25]。MJEPA用单一统一编码器与单一预测目标做音视频联合嵌入预测，目标同时施加于模态内与跨模态预测，跨模态预测对共享编码器收益关键，冻结ViT-g在AudioSet-20K超最佳冻结基线**6.8 mAP**以上，在ESC-50与FSD50K超全微调模型，且用少10倍视频数据在视频基准上具竞争力 [26]。DLLM-JEPA把JEPA引入掩码扩散语言模型，利用扩散噪声调度从单一输入构造两个视图，无需配对数据且每步单次梯度传播，较LLM-JEPA减少**33%**训练FLOPs，在4任务×2骨干上一致提升，GSM8K提升+1.8pp，并观察到几何漂移增大而功能遗忘更小的分离现象 [27]。

自蒸馏路线在单细胞领域也有对应实践。scRep用潜空间自蒸馏替代观测空间重建，通过对同一细胞不同扰动视图做动量师生对齐，并在细胞和基因两个层面施加自蒸馏目标，在约**280万**细胞上预训练即取得冻结表征基准最优总体表现，扩到3072万细胞仍有效，作者指出观测空间重建与学习稳定生物表征之间存在潜在错配 [61]。图数据方面，GraphCL设计四类图增强引入不同先验，通过最大化不同增强视图间特征一致性学习不变表征，在半监督、无监督、迁移和对抗攻击四设置下，无需调增强幅度或复杂架构即达到与SOTA相似或更好的泛化、迁移与鲁棒性 [62]。

综合来看，生成式掩码重建因训练目标可靠而稳定，但对高冗余模态计算效率低、训练目标不优先学习高层概念特征；预测式方法语义性强，却常因依赖非平稳自蒸馏目标而训练不稳定 [11]。上述工作从统一对比与掩码 [59]、孪生稠密预测 [60]、多层隐藏层自蒸馏 [11] 以及潜空间自蒸馏 [61] 等方向尝试调和这一矛盾，但各自仍受限于教师设计依赖、双分支计算成本或离散化误差等未充分讨论的问题。

### 2.3 新架构：状态空间与线性注意力

在扩散模型追求长序列建模效率的背景下，**LaMamba-Diff** 提出用 Local Attentional Mamba 块融合自注意力与 Mamba，试图在保持线性复杂度的同时兼顾全局上下文与局部细节 [36]。其动机在于：自注意力虽能通过全对交互精确捕捉全局与局部上下文，但二次复杂度对长序列输入构成显著计算挑战；而 Mamba 通过将滤波后的全局上下文压缩进隐状态实现线性复杂度，这种压缩却不可避免地带来细粒度局部依赖的信息损失 [36]。

在 ImageNet 256×256 与 512×512 图像生成任务上，该方法采用 U-Net 架构，最大模型较 **DiT-XL/2** 减少 **62% GFLOPs**，参数量相当或更少，并在 256×256 上超越 DiT 各规模 [36]。不过，该工作未充分讨论 Mamba 压缩导致局部细节信息损失的残余影响，这一局限也提示线性注意力与状态空间模型在细粒度表征上的取舍仍有争议 [36]。

## 3 数据与基准

（本节暂无入库证据）

## 4 向科学数据的迁移

在科学数据迁移中，JEPA 类方法被用于替代或补充生成式目标。**JetParticle-JEPA（JP-JEPA）** 基于 Particle Transformer 骨干，直接从连续粒子云预测被掩码粒子的潜表征，无需分词或重建原始输入，在 JetClass 全量数据上媲美全监督 SOTA，低标签场景优于监督基线，并显著优于现有 SSL 方法 [24]。**JEPA-DNA** 则将 JEPA 与生成目标结合做持续训练，在 17 项基因组基准上线性探测与零样本性能一致提升，监督线性探测达新 SOTA [23]。T-JEPA 面向表格数据，用同一特征子集的潜表征预测另一子集，规避了表格数据难以构造增强的问题，在分类与回归任务上部分方法可超越或匹配 GBDT [22]。三者共同点是都在潜空间做预测而非重建原始输入，差异在于 JP-JEPA 与 JEPA-DNA 依赖领域专用骨干（Particle Transformer、已有 GFM），T-JEPA 则强调无增强与训练稳定性（需正则化 token）[24][23][22]。

迁移到科学数据时，自监督范式的相对优势与视觉领域并不一致。在单细胞基因组上，系统基准测试覆盖超 2000 万细胞，发现 **MAE 优于对比学习**，与计算机视觉趋势相反，并在零样本细胞类型预测中表现突出，但 SSL 的优势场景有限，主要见于迁移学习 [33]。RegFormer 走的是另一条路线：将基因调控网络先验与 Mamba 状态空间架构结合，在 2500 万人类细胞上预训练，在细胞注释、GRN 重建、遗传扰动预测与药物响应建模等基准上持续超越 scGPT 与 Geneformer [35]。这提示在科学数据中，**引入领域结构先验**（调控层级、物理匹配）可能与单纯扩大自监督目标同样关键，而 JEPA-DNA 也把潜语义对齐置于纯 token 重建之上 [23][35]。

地理空间与临床两个方向则暴露了迁移的边界。Mini-JEPA 用五个 22M 参数传感器专用模型组成舰队，各模型最佳预测变量即其传感器所观测变量，联合模型对土壤湿度等 ΔR² 达 0.031，路由命中率 d=1.10, p=0.031，但总体问题类型聚合增益有限，且路由 LLM 依赖闭源模型 [37]。医疗世界模型综述提出 L1 时序预测到 L4 规划控制的分级，发现多数系统仅达 L1–L2，少数 L3，L4 罕见，并指出动作空间不明确、干预验证薄弱等跨领域缺口 [10]。与单细胞和喷注任务相比，这两项工作表明：当任务涉及动作条件预测或跨传感器泛化时，当前自监督表征的迁移仍受限于状态构建与验证环节，而非表征学习本身 [10][37]。

## 5 评测、可复现性与争议

在病理自监督基础模型的临床评测中，**CTransPath、Phikon、UNI、Virchow、Prov-GigaPath** 等公开模型被纳入统一基准，评测采用瓦片编码加聚合的两阶段流程，覆盖瓦片级与切片级下游任务 [34]。结果显示 **DINO 算法优于 MAE**，但各模型在瓦片级与切片级任务上表现不一，且病理领域自监督学习仍处早期，受限于数据与算力缺乏、数字病理采用率低以及 WSI 分辨率极高等因素 [34]。

世界模型测试时自适应方面，**Sandwich-Residuals** 冻结预训练世界模型，仅学习预测器前后的轻量残差修正，残差用模型自监督预测误差在线优化，无需奖励、标签或源域数据 [63]。在 AdaJEPA 基准 21 种条件下，其成功率达冻结模型的 1.3 倍，保留最强 AdaJEPA 变体 95% 性能，少调 97–99% 参数；复合偏移下达 1.9 倍，并在 DINO-WM 三维操作上得到验证 [63]。不过复合偏移下其仅与内部块自适应相当，未超越最强变体，项目页公开 [63]。

## 6 空白与趋势

综合现有证据，本方向在「潜空间预测是否足以支撑可迁移世界模型」这一根本问题上，已从早期的架构可行性验证，转入对训练稳定性、概率化建模与决策对齐的系统性检验，但**跨模态、跨任务的普适优势仍缺乏统一评测**。以下列出若干趋势与尚未被充分占据的空白。

1. **JEPA 的概率化与生成式融合正在形成新分支，但两条路线的等价性主张尚未在统一基准上对质。** Var-JEPA 论证 JEPA 与变分推断结构等价、标准 JEPA 只是确定性特例，并实例化出无需启发式反坍缩正则的 Var-T-JEPA [30]；VJEPA 同样把 JEPA 推广为概率形式并证明其与预测状态表示、贝叶斯滤波统一，BJEPA 用专家乘积支持零样本迁移 [31]；Flow-JEPA 则用条件流匹配替代逐点一步转移回归，在四个环境上把噪声下成功率由 67% 升至 86% [7]。**但三者各自的环境、指标与基线不同，尚无工作在同一设定下比较"变分 JEPA / 流匹配 JEPA / 确定性 JEPA"的优劣**，也无人检验概率化带来的不确定性估计是否真能改善下游规划而非仅改善预测指标。

2. **防坍塌方案高度碎片化且相互冲突，缺少统一的失效条件刻画。** LeJEPA 主张各向同性高斯最优、用 SIGReg 去掉 stop-gradient 与教师学生等启发式 [3]；SiamJEPA 反其道主张孪生编码器加 EMA 教师起正则作用 [4]；BiJEPA 用循环一致性与范数正则解决对称预测的表征爆炸 [28]；UniJEPA 则声称无需 EMA、stop-gradient 或预训练编码器即可防坍塌 [43]。与此同时，表格领域的实证显示潜项曾坍塌并把编码器带向常数映射，即便采用值头、EMA 差分目标与掩码 token 的配方，JEPA 臂在 147 个数据集上仍落后仅值目标臂，且需 1.42 倍步数与 1.66 倍墙钟 [5]。**这些方案在何种数据冗余度、何种模态下失效，目前没有统一判据**，表格上的负面结果是否可外推到组学、时序等结构化科学数据，也无人系统检验。

3. **决策对齐与物理锚定成为控制侧 JEPA 的共识方向，但"预测准"与"决策对"的分离现象缺乏机制性解释。** D-JEPA 明确指出预测隐距离更近的候选动作可能实际失败，用有界置换等变算子学习候选未来间的决策相关关系 [6]；另一项工作用逆动力学加状态对齐把连续表示锚定到物理状态，消融显示状态对齐一致提升规划成功率 [32]；点云实验则发现 Point-LeWM 与图像基线统计等价、Point-Delta-JEPA 在几何移动最多时最强 [8]。**这些工作各自提出修补目标，但没有人给出"何时潜预测指标与任务成功率解耦"的可检验条件**，也缺少跨观测模态（图像、点云、状态向量）的对照实验来定位解耦来源。

4. **科学数据迁移呈现"领域结构先验可能比自监督目标本身更关键"的信号，但这一假设尚未被直接检验。** 单细胞基准覆盖超 2000 万细胞，发现 MAE 优于对比学习、与计算机视觉趋势相反，且 SSL 优势主要见于迁移学习 [33]；RegFormer 把基因调控网络先验与 Mamba 结合，在 2500 万人类细胞上预训练并持续超越 scGPT 与 Geneformer [35]；JEPA-DNA 把潜语义对齐置于纯 token 重建之上，在 17 项基因组基准上一致提升 [23]；JP-JEPA 用 Particle Transformer 骨干在低标签场景优于监督基线 [24]。**但没有工作做"同一自监督目标 + 有无领域结构先验"的受控消融**，因此无法判断增益来自潜空间预测范式还是来自先验注入。

5. **世界模型的能力分级与测试时自适应已被提出，但"规划级"能力的评测仍集中在少数仿真环境。** 医疗世界模型综述提出 L1 时序预测到 L4 规划控制的分级，发现多数系统仅达 L1–L2、L4 罕见，并指出动作空间不明确、干预验证薄弱、多模态状态构建不完整等跨领域缺口 [10]；Sandwich-Residuals 在冻结世界模型上仅学轻量残差，在 AdaJEPA 21 种条件下成功率达冻结模型 1.3 倍、少调 97–99% 参数，但复合偏移下仅与内部块自适应相当、未超越最强变体 [63]。**L1–L4 分级目前只是描述性框架，没有配套的可复现评测协议**，也无人把该分级用于生物医学多模态数据（影像 + 组学 + 时序）的状态构建。

6. **跨域统一 JEPA 的尝试已出现，但其"统一是否以牺牲领域特异性为代价"仅由作者自陈，缺少第三方复现。** JEPA-Anything 用正交预测因子分解把潜在目标拆为互补因子，覆盖视觉、生物、临床、控制、分子、物理场、天气七个领域，报告在 10 个动力学任务上全部相对 JEPA 基线提升，Interventional Pong 单干预预测误差下降 34.8% [64]。**该工作自认跨域统一可能牺牲领域特异性，但尚无独立评测验证其在不同领域是否一致优于领域专用方案**，也未与 RegFormer、JEPA-DNA 等科学领域专用模型做同台比较。

7. **长序列架构与潜预测的结合仍是空白。** 现有证据中，状态空间与线性注意力的讨论集中在生成式扩散（LaMamba-Diff 用 Local Attentional Mamba 块融合自注意力与 Mamba，最大模型较 DiT-XL/2 减少 62% GFLOPs）[36]，或作为科学模型的骨干（RegFormer 的 Mamba 架构）[35]。**但把 Mamba / 线性注意力直接用作 JEPA 世界模型的时序预测骨干、并检验其在线性复杂度下是否仍能避免潜坍塌与误差累积，目前没有入库证据**；Flow-JEPA 用流匹配缓解误差累积 [7]，却未涉及架构层面的长序列效率。

## 7 未归类新证据

在跨域世界模型方向，JEPA-Anything 提出以**正交预测因子分解（OPF）**扩展联合嵌入预测架构，将潜在目标分解为互补因子、经专用通路学习后在共享预测设计中重组，从而用同一学习原则覆盖不同系统 [64]。其评测覆盖视觉、生物、临床、控制、分子、物理场、天气七个领域的数据，并以匹配的 JEPA 基线作为对照 [64]。

在该研究内部，作者报告在**10 个动力学任务**上全部相对 JEPA 基线提升，其中 Interventional Pong 的单干预预测误差下降 **34.8%**，四系统 100 步分子误差最低，轨道标度指数拟合斜率为 -1.4991 [64]。作者同时指出，跨域统一框架在部分领域可能牺牲领域特异性，这一取舍是该证据自身承认的局限 [64]。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 预测隐空间 / 世界模型（JEPA、Dreamer、DINO-WM 等） | 朝阳 | 雷达样本中该节 n=29、近两年占比 0.79，说明近两年集中爆发；[2] V-JEPA 2 把自监督视频模型推到理解+预测+规划，[20] DINO-WM 在预训练视觉特征上做零样本规划，[45] Unified World Models 耦合视频与动作扩散——方法路线多、目标从表征转向规划/控制，尚未收敛。 |
| 掩码与自蒸馏表征（MAE、DINO、MoCo、SimCLR） | 成熟 | [13] MAE 与 [12] DINO 已是范式级工作，[53] SimCLR、[54] MoCo 奠定对比学习基线；该节 n=25 但近两年占比仅 0.2、中位引用 520，说明核心思想已沉淀为通用组件，新工作多为增量或迁移。 |
| 新架构：状态空间模型 / 线性注意力 | 证据不足 | 雷达样本中该节仅 n=1，[36] LaMamba-Diff 是唯一证据，无法据此判断阶段；但 Mamba/线性注意力在长序列建模上的潜力与该方向关键词一致，属于雷达覆盖不足而非领域空白。 |
| 数据与基准 | 证据不足 | 该节 n=0，雷达未挂到证据；但 [33] 对单细胞基因组自监督的有效使用做了系统 delineation，[34] 对病理自监督基础模型做临床基准，说明评测类工作实际存在，只是被归到其他节。 |
| 向科学数据的迁移（组学、单细胞、粒子等） | 朝阳 | [33] 系统评估自监督在单细胞基因组中的有效使用，[35] RegFormer 用基因调控层级做单细胞基础模型，[23] JEPA-DNA 把联合嵌入预测架构接地到基因组基础模型，[24] JetParticle-JEPA 把 JEPA 迁到粒子数据；该节 n=7、近两年占比 0.71，说明迁移刚起步、方法未定。 |
| 评测、可复现性与争议 | 萌芽 | [34] 对公共病理自监督基础模型做临床基准，[63] Sandwich-Residuals 讨论世界模型的参数高效测试时适配；该节 n=2、近两年占比 1.0，说明批判性评测刚出现，尚未形成标准。 |

**整体判断**：这个方向整体处于**朝阳期**，但内部严重分化——**掩码/自蒸馏/对比学习已成熟**（[13]、[12]），**预测隐空间与世界模型正在爆发**（[2]、[20]），**向科学数据迁移刚起步**（[33]、[23]）。窗口期估计还有 **12–24 个月**：JEPA/世界模型的通用架构仍在快速迭代，但一旦收敛成类似 MAE/DINO 的稳定组件，迁移红利会迅速消失。最大不确定性是**评测与可复现性**——雷达样本中该节仅 n=2（[34]、[63]），说明科学数据上的自监督表征缺乏统一基准，很容易做出「看起来好但不可复现」的结果；另一个不确定性是**状态空间/线性注意力在生物多模态上的适配**，雷达样本中该节仅 n=1（[36]），证据严重不足。

**接下来怎么做**：

1. **把 JEPA 式隐空间预测接到类器官多组学时序上**。切入点：用类器官发育/衰老时间序列的多组学（转录组+表观组+影像），把不同模态当作不同 view，做联合嵌入预测而非重构；产出是一个可迁移到公共单细胞数据的衰老轨迹表征。为什么现在做：[23] JEPA-DNA 刚证明 JEPA 可接地到基因组基础模型，[33] 又指出单细胞自监督的有效使用尚缺系统结论，两者之间的空白正好是类器官时序。支撑：[23]、[33]。

2. **用公共数据做世界模型式的扰动预测 demo**。切入点：拿公共 Perturb-seq / 药物扰动数据，训练一个在隐空间预测「扰动后状态」的世界模型，而不是直接预测表达值；产出是可零样本规划（选扰动组合）的 demo。为什么现在做：[20] DINO-WM 已证明在预训练特征上做零样本规划可行，[45] 进一步耦合视频与动作扩散，这套思路迁到扰动数据上尚无人做。支撑：[20]、[45]。

3. **优先做评测，而不是再刷一个基础模型**。切入点：对现有单细胞/病理自监督基础模型做衰老相关下游任务的系统基准，覆盖批次效应、可复现性、跨模态迁移；产出是一篇批判性评测 + 开源 benchmark。为什么现在做：[34] 已在病理上做了临床基准，[33] 在单细胞上做了 delineation，但衰老 + 多模态交叉处仍是空白，且雷达样本中评测节仅 n=2，先发优势明显。支撑：[34]、[33]。

4. **把状态空间/线性注意力作为长序列单细胞建模的工程切入点**。切入点：用 Mamba/线性注意力替换 Transformer 做长时序单细胞轨迹或长读长多组学建模，重点验证显存与长程依赖；产出是一个效率对比 + 可开源实现。为什么现在做：雷达样本中该节仅 n=1（[36]），说明在生物数据上几乎没人系统试过，而单细胞轨迹天然是长序列，工程红利大。支撑：[36]。

5. **用测试时适配（test-time adaptation）处理类器官批次漂移**。切入点：在已预训练的世界模型/表征上做参数高效测试时适配，应对不同批次、不同供体的类器官数据；产出是一个即插即用的适配模块 + 跨批次泛化结果。为什么现在做：[63] Sandwich-Residuals 刚提出世界模型的参数高效测试时适配，[34] 又显示基础模型跨临床场景泛化是痛点，两者结合在类器官上直接可用。支撑：[63]、[34]。

## 参考文献

1. Graph-level Representation Learning with Joint-Embedding Predictive Architectures. Trans. Mach. Learn. Res. 2023. https://doi.org/10.48550/arXiv.2309.16014
2. V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning. arXiv.org 2025. https://doi.org/10.48550/arXiv.2506.09985
3. LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics. arXiv.org 2025. https://doi.org/10.48550/arXiv.2511.08544
4. SiamJEPA: On the Role of Siamese Student Encoders in JEPA. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.04044
5. A JEPA Recipe for Tabular Foundation Models.  2026. https://arxiv.org/abs/2609.25541
6. D-JEPA: A Decision-Aligned Latent World Model.  2026. https://arxiv.org/abs/2609.24749
7. Flow-JEPA: Flow Matching for Robust Latent Dynamics in JEPA World Models.  2026. https://arxiv.org/abs/2608.29029
8. Does Latent Planning Survive Point Clouds? Action-Conditioned JEPA World Models for Geometric Observations.  2026. https://arxiv.org/abs/2608.29434
9. SANA-WM: Efficient Minute-Scale World Modeling with Hybrid Linear Diffusion Transformer. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.15178
10. Beyond Generative AI: World Models for Clinical Prediction, Counterfactuals, and Planning.  2025. https://arxiv.org/abs/2511.16333v1
11. Self-Distillation of Hidden Layers for Self-Supervised Representation Learning. arXiv.org 2026. https://doi.org/10.48550/arXiv.2603.15553
12. Emerging Properties in Self-Supervised Vision Transformers. IEEE International Conference on Computer Vision 2021. https://doi.org/10.1109/ICCV48922.2021.00951
13. Masked Autoencoders Are Scalable Vision Learners. Computer Vision and Pattern Recognition 2021. https://doi.org/10.1109/CVPR52688.2022.01553
14. VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training. Neural Information Processing Systems 2022. https://doi.org/10.48550/arXiv.2203.12602
15. Masked Autoencoders for Point Cloud Self-supervised Learning. European Conference on Computer Vision 2022. https://doi.org/10.48550/arXiv.2203.06604
16. Masked Autoencoders that Listen. Neural Information Processing Systems 2022. https://doi.org/10.48550/arXiv.2207.06405
17. NeRF-MAE: Masked AutoEncoders for Self-Supervised 3D Representation Learning for Neural Radiance Fields. European Conference on Computer Vision 2024. https://doi.org/10.48550/arXiv.2404.01300
18. Computational Pathology at Health System Scale - Self-Supervised Foundation Models from Three Billion Images. arXiv.org 2023. https://doi.org/10.48550/arXiv.2310.07033
19. Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture. Computer Vision and Pattern Recognition 2023. https://doi.org/10.1109/CVPR52729.2023.01499
20. DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning. International Conference on Machine Learning 2024. https://doi.org/10.48550/arXiv.2411.04983
21. Point-JEPA: A Joint Embedding Predictive Architecture for Self-Supervised Learning on Point Cloud. IEEE Workshop/Winter Conference on Applications of Computer Vision 2024. https://doi.org/10.1109/WACV61041.2025.00714
22. T-JEPA: Augmentation-Free Self-Supervised Learning for Tabular Data.  2024. https://arxiv.org/abs/2410.05016v3
23. JEPA-DNA: Grounding Genomic Foundation Models through Joint-Embedding Predictive Architectures.  2026. https://arxiv.org/abs/2602.17162v3
24. JetParticle-JEPA: An Efficient Self-Supervised Representation Learning method for Jet Tagging in High-Energy Physics. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.14813
25. Audio-JEPA: Joint-Embedding Predictive Architecture for Audio Representation Learning.  2025. https://arxiv.org/abs/2507.02915v1
26. MJEPA: A Simple and Scalable Joint-Embedding Predictive Architecture for Audio-Visual Learning. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.25225
27. DLLM-JEPA: Joint Embedding Predictive Architectures for Masked Diffusion Language Models.  2026. https://arxiv.org/abs/2606.00091v1
28. BiJEPA: Bi-directional Joint Embedding Predictive Architecture for Symmetric Representation Learning.  2026. https://arxiv.org/abs/2603.00049v1
29. LeVJEPA: Efficient&Scalable Video Pretraining without the Heuristics.  2026. https://arxiv.org/abs/2608.27395
30. Var-JEPA: A Variational Formulation of the Joint-Embedding Predictive Architecture - Bridging Predictive and Generative Self-Supervised Learning.  2026. https://arxiv.org/abs/2603.20111v2
31. VJEPA: Variational Joint Embedding Predictive Architectures as Probabilistic World Models.  2026. https://arxiv.org/abs/2601.14354v1
32. Toward Physically Grounded JEPA World Models for Goal-Conditioned Robotic Planning.  2026. https://arxiv.org/abs/2609.03565
33. Delineating the Effective Use of Self-Supervised Learning in Single-Cell Genomics. bioRxiv 2024. https://doi.org/10.1038/s42256-024-00934-3
34. A clinical benchmark of public self-supervised pathology foundation models.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58796-1
35. RegFormer: a single-cell foundation model powered by gene regulatory hierarchies.. Nature communications 2026. https://doi.org/10.1038/s41467-026-72198-x
36. LaMamba-Diff: Linear-Time High-Fidelity Diffusion Models Based on Local Attention and Mamba. arXiv.org 2024. https://doi.org/10.48550/arXiv.2408.02615
37. Mini-JEPA Foundation Model Fleet Enables Agentic Hydrologic Intelligence.  2026. https://arxiv.org/abs/2605.14120v1
38. 3D-JEPA: A Joint Embedding Predictive Architecture for 3D Self-Supervised Representation Learning. arXiv.org 2024. https://doi.org/10.48550/arXiv.2409.15803
39. CrossJEPA: Cross-Modal Joint-Embedding Predictive Architecture for Efficient 3D Representation Learning from 2D Images. arXiv.org 2025. https://doi.org/10.48550/arXiv.2511.18424
40. HEP-JEPA: A foundation model for collider physics using joint embedding predictive architecture. arXiv.org 2025. https://doi.org/10.48550/arXiv.2502.03933
41. MC-JEPA: A Joint-Embedding Predictive Architecture for Self-Supervised Learning of Motion and Content Features. arXiv.org 2023. https://doi.org/10.48550/arXiv.2307.12698
42. GLAM: Training a latent world model over global spatiotemporal memory for active exploration and navigation.  2026. https://arxiv.org/abs/2609.14561
43. UniJEPA: A Unified Joint-Embedding Predictive Architecture for Task-Agnostic Visual World Modeling.  2026. https://arxiv.org/abs/2608.07409v1
44. CLAW: Learning Continuous Latent Action World Models via Adversarial Latent Regularization. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.04130
45. Unified World Models: Coupling Video and Action Diffusion for Pretraining on Large Robotic Datasets. Robotics 2025. https://doi.org/10.48550/arXiv.2504.02792
46. Back to Parsimonious Latents: Learning Task-Centric World Models from Visual Foundations. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.25620
47. Planning to Explore via Self-Supervised World Models. International Conference on Machine Learning 2020. https://arxiv.org/abs/2005.05960
48. Baba in Wonderland: Online Self-Supervised Dynamics Discovery for Executable World Models. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.16725
49. Music-JEPA: Learning a World Model of Sound from Action. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.22000
50. Self-Supervised Learning: Generative or Contrastive. IEEE Transactions on Knowledge and Data Engineering 2020. https://doi.org/10.1109/TKDE.2021.3090866
51. Revisiting Self-Supervised Visual Representation Learning. Computer Vision and Pattern Recognition 2019. https://doi.org/10.1109/CVPR.2019.00202
52. Scaling and Benchmarking Self-Supervised Visual Representation Learning. IEEE International Conference on Computer Vision 2019. https://doi.org/10.1109/ICCV.2019.00649
53. A Simple Framework for Contrastive Learning of Visual Representations. International Conference on Machine Learning 2020. https://arxiv.org/abs/2002.05709
54. Momentum Contrast for Unsupervised Visual Representation Learning. Computer Vision and Pattern Recognition 2019. https://doi.org/10.1109/cvpr42600.2020.00975
55. Bootstrap Your Own Latent: A New Approach to Self-Supervised Learning. Neural Information Processing Systems 2020. https://arxiv.org/abs/2006.07733
56. HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units. IEEE/ACM Transactions on Audio Speech and Language Processing 2021. https://doi.org/10.1109/taslp.2021.3122291
57. Masked particle modeling on sets: towards self-supervised high energy physics foundation models. Machine Learning: Science and Technology 2024. https://doi.org/10.1088/2632-2153/ad64a8
58. Context Autoencoder for Self-supervised Representation Learning. International Journal of Computer Vision 2022. https://doi.org/10.1007/s11263-023-01852-4
59. Contrastive Masked Autoencoders are Stronger Vision Learners. IEEE Transactions on Pattern Analysis and Machine Intelligence 2022. https://doi.org/10.1109/TPAMI.2023.3336525
60. Siamese Image Modeling for Self-Supervised Vision Representation Learning. Computer Vision and Pattern Recognition 2022. https://doi.org/10.1109/CVPR52729.2023.00212
61. scRep: A Latent-Space Self-Distilled Foundation Model for Single-Cell Representation Learning. bioRxiv 2026. https://doi.org/10.64898/2026.08.31.747784
62. Graph Contrastive Learning with Augmentations. Neural Information Processing Systems 2020. https://arxiv.org/abs/2010.13902
63. Sandwich-Residuals: Parameter-Efficient Test-time Adaptation of World Models.  2026. https://arxiv.org/abs/2609.21740
64. JEPA-Anything: Learning Predictive Models across Different Worlds.  2026. https://arxiv.org/abs/2609.20800
65. Self-Supervised JEPA-based World Models for LiDAR Occupancy Completion and Forecasting.  2026. https://arxiv.org/abs/2602.12540v1
