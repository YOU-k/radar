# 世界模型与自监督表征学习 · 方向背景报告

证据 65 篇 · 覆盖度 0.46 · 第 3 轮 · 更新 2026-09-23

## 摘要（TL;DR）

- 世界模型与自监督表征学习的核心趋势，是把「预测未来」从像素/体素重建转向隐空间条件预测，JEPA式非对称架构被视为规避生成式高算力与幻觉风险的关键路径 [1]。
- 3D-JEPA 在 PB_T50_RS 上以150个预训练epoch达到88.65%准确率，用更少轮次取得更高精度，显示采样策略与上下文感知解码器设计是点云JEPA的重要增益来源 [2]。
- 点云世界模型证据对「潜空间预测天然优于重建」的叙事构成反例：Point-LeWM 与图像基线统计等价，Point-Delta-JEPA 仅在场景点移动0.3–15%时最强，距离噪声还会破坏最稀疏场景 [3]。
- 跨模态路线用图像基础模型缓解3D数据稀缺，CrossJEPA 在 ModelNet40 与 ScanObjectNN 线性探测上分别达94.2%与88.3%，但因评测协议不同（线性SVM vs. 线性探测）不能简单读作「跨模态优于纯3D自监督」 [4][5]。
- 视频侧规模化验证以 V-JEPA 2 为关键证据：在超100万小时互联网视频上预训练，Something-Something v2 达77.3%、Epic-Kitchens-100 达39.7 recall@5、PerceptionTest 达84.0、TempCompass 达76.9，并用少于62小时Droid视频后训练出可零样本部署的V-JEPA 2-AC [6]。
- 防坍塌机制出现路线冲突：LeJEPA 用 SIGReg 约束各向同性高斯嵌入，覆盖10+数据集与60+架构、ViT-H/14 在 ImageNet-1k 线性评估达79%；SiamJEPA 则用掩码孪生学生编码器加EMA教师提升可分性，二者评测域不同，尚无法在统一协议下裁决 [7][8]。
- 概率化JEPA成为2026年明显潮流，Var-JEPA 用单一ELBO显式建模隐变量并在真实表格基准上超过T-JEPA，VJEPA/BJEPA 与 BiJEPA 则仅在玩具或小规模数据上验证，证据强度差异很大 [9][10][11]。
- 潜空间规划的最尖锐批评是「决策局部预测差距」：D-JEPA 指出潜距离更近的候选动作可能实际失败，在 PushT 达87.89%、RoboTwin 平均提升15.04点、真实机器人提升17点，但依赖已执行候选结果监督 [12]。
- 负面证据同样存在：一项表格基础模型研究在147个真实表格数据集上发现，收敛后JEPA臂仍落后仅值目标臂，分类差距较小（32:70胜负），回归差距更大（8:24），且需1.42倍步数与1.66倍墙钟才能达到平台 [13]。
- 生成式世界模型并未退出竞争：SANA-WM 以2.6B参数、约21.3万公开视频片段、64张H100训练15天，实现单GPU生成60秒720p、蒸馏版在单张RTX 5090 NVFP4下34秒去噪60秒720p，说明潜空间方法与生成式方法更可能是分工而非替代 [14][1]。

## 1 背景与定义

掩码建模与自蒸馏的谱系在2026年前后出现了一个值得注意的收敛趋势：**JEPA不再只是"另一种自监督方法"，而逐渐成为连接掩码预测、自蒸馏与世界模型的统一框架**。I-JEPA从单个上下文块预测同一图像多个目标块的表征，不依赖手工数据增强，用16张A100在ImageNet训练ViT-Huge/14少于72小时[15]；Bootleg进一步指出仅重建低层数据或依赖最终层非平稳自蒸馏目标的不足，通过预测教师多个隐藏层的潜表征训练模型，在ImageNet-1K、iNaturalist-21、VTAB冻结探针分类上较I-JEPA提升+10%，并在ADE20K、Cityscapes、COCO-Stuff语义分割上显著优于可比基线[16]。这一从单层目标向多层教师目标的演进，与DINO的多裁剪自蒸馏、BYOL的慢速移动平均目标在动机上同源，但JEPA把预测目标从"同一图像的增强视图"扩展到了"同一场景的不同部分或未来状态"，从而与掩码建模和世界模型同时接壤[17][18]。

这一接壤在跨模态与跨领域迁移中表现得尤为明显。Audio-JEPA用ViT骨干预测掩码梅尔频谱块的隐表征而非重建原始音频，在无标签AudioSet上预训练，性能与wav2vec 2.0和data2vec相当，但训练数据不足其五分之一且无需调参[19]；MJEPA用单一统一编码器与单一预测目标做音视频联合嵌入预测，跨模态预测对共享编码器收益关键，冻结ViT-g在AudioSet-20K超最佳冻结基线6.8 mAP，且用少10倍视频数据在视频基准上具竞争力[20]；DLLM-JEPA把JEPA目标引入掩码扩散语言模型，利用扩散噪声调度从单一输入构造两个视图，较LLM-JEPA减少33%训练FLOPs，GSM8K提升+1.8pp[21]。**这些工作共同显示JEPA的跨模态可迁移性，但Audio-JEPA明确未调参、MJEPA强调统一编码器、DLLM-JEPA依赖扩散噪声调度，三者在"什么该被共享、什么该被预测"上并未形成共识**[19][20][21]。

在科学数据上，JEPA的迁移呈现出与视觉领域不同的证据格局。JEPA-DNA将联合嵌入预测架构融入基因组基础模型训练，通过在潜空间监督全局序列嵌入、预测被掩码基因组片段的功能表征，并结合传统生成目标进行持续训练，在17项基准上线性探测与零样本性能一致提升，证明潜语义对齐优于纯token重建[22]。JetParticle-JEPA基于Particle Transformer骨干，直接从连续粒子云预测被掩码粒子的潜表征，无需分词或重建原始输入，在JetClass上媲美全监督SOTA，低标签场景超越监督基线，并在缺失探测器信息下展现鲁棒性[23]。HEP-JEPA则在含1亿喷注的JetClass数据集上预训练，用部分喷注成分预测未见成分的嵌入，在top tagging与轻夸克-胶子喷注区分等下游任务上与高能物理SOTA可比[24]。**这三项工作把JEPA从视觉语义中解放出来，证明"用可见部分预测被掩码部分的潜表征"可以作为科学数据的通用预训练目标；但它们的评测域各自独立——基因组、粒子云、喷注——尚无跨领域统一基准能判断JEPA在科学数据上的收益是否来自同一机制**[22][23][24]。

与此同时，掩码建模与自蒸馏在生物医学与病理领域的对照实验给出了与计算机视觉趋势相反的信号。一项系统基准测试在超2000万细胞上训练多种掩码策略的MAE和对比学习，评估细胞类型预测、基因表达重建、跨模态预测和数据整合等下游任务，发现**MAE优于对比学习，与计算机视觉趋势相反**，并在零样本细胞类型预测中展现显著能力[25]。病理基础模型的临床基准评测梳理了CTransPath、Phikon、UNI、Virchow等模型的训练数据与算法，通过瓦片编码加聚合的两阶段流程评估下游任务，结果显示**DINO算法优于MAE**，但病理领域SSL仍处早期，受限于数据与算力[26]。而构建30亿张图像、42.3万张切片病理数据集的工作同样发现DINO表现更佳[27]。**单细胞基因组偏好MAE、病理图像偏好DINO，这一分歧提示"哪种自监督目标更优"高度依赖数据模态的冗余结构与噪声特性，而非存在普适最优解**[25][26][27]。

从更长的演化脉络看，2019年的两项系统研究已经预埋了后续分歧的种子。Revisiting Self-Supervised Visual Representation Learning通过统一实验揭示CNN设计标准配方不总适用于自监督学习，发现调整架构与训练策略可大幅提升性能并超越此前SOTA[28]；Scaling and Benchmarking Self-Supervised Visual Representation Learning将两种流行方法扩展至1亿图像，在9个数据集任务上建立基准，发现可匹配或超越监督预训练，但**现有方法仍不足以充分利用大规模数据，未学到有效高层语义，且当前自监督方法不够"难"**[29]。这两项工作指出的"方法不够难、未充分利用数据"在VideoMAE的90%-95%极高掩码率[30]与I-JEPA的大尺度目标块采样[15]中得到部分回应，但"高层语义不足"的问题在后续工作中仍以语义分割、物体计数、深度预测等下游任务间接评估，缺乏统一诊断[15]。Self-Supervised Learning: Generative or Contrastive按目标将经验方法归纳为生成式、对比式和生成-对比式三类[31]；以此框架回看，MAE、VideoMAE、Audio-MAE、点云MAE、NeRF-MAE、MPM属于生成式掩码重建[32][30][33][34][35][36]，SimCLR、MoCo、GraphCL属于对比式[37][38][39]，而JEPA系列——I-JEPA、Bootleg、Audio-JEPA、MJEPA、DLLM-JEPA、JEPA-DNA、JetParticle-JEPA、HEP-JEPA——则难以被简单归入任何一类：它们既不做像素重建，也不依赖负样本，而是**在潜空间中预测被掩码部分或未来状态，同时用非对称架构、EMA教师或分布正则避免坍塌**[15][16][19][20][21][22][23][24]。

这一"不可归类"恰恰是当前方向的核心张力所在。**JEPA同时继承了掩码建模的"预测被遮蔽部分"与自蒸馏的"无负样本、无重建"，但它的预测目标既不是像素也不是类别，而是另一段输入或未来状态的潜表征**；这使得它的防坍塌机制、评测协议与失败模式都无法直接沿用掩码建模或对比学习的既有结论[15][18]。LeJEPA试图用各向同性高斯分布与SIGReg约束给出可证明的防坍塌方案，覆盖10+数据集与60+架构，ViT-H/14在ImageNet-1k线性评估达79%[7]；SiamJEPA则通过掩码孪生学生编码器加EMA教师改善优化，在有限训练预算下持续优于单编码器JEPA变体[8]。**两者分别代表"用分布正则替代结构启发式"与"用结构启发式改善优化"两条路线，但评测域不同、基线不同，目前无法在统一协议下裁决**[7][8]。而表格基础模型上的负面结果——JEPA臂在147个真实表格数据集上仍落后仅值目标臂，需1.42倍步数与1.66倍墙钟才能达到平台[13]——进一步提示，**JEPA潜目标的收益高度依赖模态、基线与训练预算，不能默认其普遍占优**[13][9]。

## 2 方法学


### 2.1 预测隐空间与世界模型

预测隐空间与世界模型的核心主张，是把「预测未来」从像素或体素的重建任务，转化为在抽象表征空间中的条件预测问题。这一转向的动机在自动驾驶场景中被表述得最为直接：生成式世界模型虽然能合成未来观测，却伴随高算力开销与幻觉风险，而JEPA式潜空间预测可以规避这两点，同时通过非对称架构避免表征坍塌 [1]。AD-LiST-JEPA 把这一思路落到多帧LiDAR上，从多帧点云预测未来的时空表征，并以LiDAR占据完成与预测（OCF）作为下游任务；其初步实验显示，JEPA预训练编码器在OCF上性能更优，但作者也承认这仅是概念验证，缺少大规模定量对比与完整基准结果 [1]。与之形成对照的是同期的 **3D-JEPA**，它同样走非生成式路线，但把重点放在采样策略与解码器设计上：通过多块采样生成信息丰富的上下文块与多个目标块，再用上下文感知解码器持续注入上下文信息来预测目标块表征，在 **PB_T50_RS** 上以150个预训练epoch达到 **88.65%** 准确率，用更少预训练轮次取得更高精度 [2]。两者的差异不只是模态（LiDAR序列 vs. 点云物体），更在于对「上下文如何进入预测」的处理：3D-JEPA 让解码器反复读取上下文，AD-LiST-JEPA 则把上下文压缩进时空表征本身，而后者尚未证明这种压缩在规模上成立 [2][1]。

点云模态上的另一条线索关心的是「潜空间规划能否在几何观测下存活」。有工作把三种典型JEPA设计——冻结编码器、分布先验、动作敏感——整体迁移到点云观测，并在 stable-worldmodel 基准上重新设定，使不同方法仅在观测模态上不同 [3]。结果显示所有设计均未出现坍塌，**Point-LeWM** 与图像基线统计等价，而 **Point-Delta-JEPA** 在场景点移动最多（0.3–15%）时表现最强；该工作还提出从当前潜在和目标3D位姿直接构造目标潜在，从而无需目标观测即可规划 [3]。这里值得注意的是一个与「潜空间预测天然优于重建」的流行叙事相冲突的证据：在点云上，潜空间方法并没有系统性超过图像基线，只是在几何扰动加剧时才显出优势，且距离噪声会破坏最稀疏的场景 [3]。更早的 **Point-JEPA** 则从效率与排序入手，引入 sequencer 对点云块嵌入排序，基于索引高效计算并利用邻近性做目标与上下文选择，共享邻近性计算以提升效率；它在 **ModelNet40** 线性SVM分类上达到 **93.7±0.2%**，超过所有其他自监督模型，并在四个少样本框架上均创SOTA，且无需输入空间重建或额外模态 [5]。把这两项工作并置可以看出，点云JEPA的收益来源并不一致：Point-JEPA 的增益主要来自块选择与排序的归纳偏置，而点云世界模型工作强调的是观测模态变化下的鲁棒性，二者尚未在同一预训练预算下被直接比较 [5][3]。

跨模态方向提供了缓解3D数据稀缺的另一条路径。**CrossJEPA** 利用图像基础模型的知识，训练预测器从3D点云推断特定渲染2D视图的嵌入，并采用冻结教师与目标嵌入缓存提升效率，在 **ModelNet40** 与 **ScanObjectNN** 线性探测上分别达到 **94.2%** 与 **88.3%**，均为SOTA [4]。这一结果高于 Point-JEPA 在 ModelNet40 上的 93.7±0.2%，但两者的评测协议并不相同（线性SVM vs. 线性探测），且 CrossJEPA 依赖图像基础模型、未验证真实大规模3D场景，因此不能简单读作「跨模态优于纯3D自监督」 [4][5]。跨模态预测的另一种形态出现在高能物理：**HEP-JEPA** 用基于Transformer的基础模型，在含 **1亿个喷注** 的 JetClass 数据集上预训练，以部分喷注成分预测未见成分的嵌入，在 top tagging 与轻夸克-胶子喷注区分等下游任务上与高能物理SOTA可比 [24]。该工作说明JEPA的「用可见部分预测被掩码部分」范式可以脱离视觉语义，在科学数据上作为通用预训练目标使用，但其局限同样明显：仅用 JetClass 预训练，未覆盖更多对撞机数据 [24]。

视频与图像侧的规模化验证构成了这一方向最重要的经验基础。**V-JEPA 2** 在超过 **100万小时** 互联网视频上预训练动作无关的JEPA架构，对齐大语言模型后在多个视频问答任务上达到SOTA，具体包括 **Something-Something v2 77.3%**、**Epic-Kitchens-100 39.7 recall@5**、**PerceptionTest 84.0**、**TempCompass 76.9**；随后仅用少于 **62小时** Droid机器人视频后训练出 **V-JEPA 2-AC** 世界模型，在Franka机械臂上零样本部署，实现基于图像目标的抓取放置规划 [6]。这一结果常被引为「潜空间世界模型可支撑真实机器人规划」的关键证据，但其机器人规划部分的数据规模与泛化性仍待验证 [6]。与之竞争的是 **LeVJEPA**，它主张去掉目标编码器、预测器、stop-gradient与掩码重建，仅用全局-局部不变性损失加 **SIGReg**，并随机丢弃95%的patch token、支持块因果注意力；在同数据同轮次下以 **5.6–20.8×** 更少预训练算力匹配或超过 V-JEPA 2，同FLOPs下 ImageNet-1K 超过最强视频基线 **7.6点**，运动中心精度接近 DINOv2 的两倍 [40]。这两项工作的冲突点在于「什么才是可扩展性的关键」：V-JEPA 2 依赖大规模数据与动作条件后训练，LeVJEPA 则主张启发式组件本身是算力浪费，用分布正则可以更省地达到同等或更好效果；但 LeVJEPA 未提代码公开，运动中心基准仅保持竞争力，尚不足以判定其全面替代性 [6][40]。

防坍塌机制是JEPA从架构直觉走向可证明方法的关键议题。**LeJEPA** 给出了目前最系统的理论化尝试：它论证各向同性高斯是嵌入的最优分布，并用 **SIGReg** 约束嵌入，与JEPA预测损失结合，从而避免stop-gradient、教师学生与调度器等启发式；实验覆盖 **10+数据集** 与 **60+架构**，**ViT-H/14** 在 ImageNet-1k 冻结骨干线性评估上达到 **79%**，显示单超参、线性复杂度、跨架构稳定，实现约50行代码 [7]。作者同时承认，尽管理论假设与经验验证覆盖面广，但未明确讨论跨全部真实下游任务的预测风险最优性边界 [7]。**SiamJEPA** 从另一角度处理同一问题：它研究JEPA中学生网络使用孪生编码器的作用，采用掩码孪生学生编码器并配EMA教师，可视为 PhiNet 的JEPA形式；实验发现孪生编码器对JEPA目标起正则作用，提升表征可分性并加速早期学习，在有限训练预算下持续优于单编码器JEPA变体，线性探测精度高于需要更长训练的 **MAE** [8]。这与 LeJEPA 的「去启发式」立场形成有趣张力：SiamJEPA 恰恰通过增加一个编码器（一种结构启发式）来改善优化，而 LeJEPA 主张用分布正则替代这类设计 [7][8]。两者的评测域也不同——ImageNet线性探测 vs. 10+数据集60+架构——因此「哪种防坍塌更优」目前无法在统一协议下裁决 [8][7]。

把JEPA重新解释为概率模型，是2026年出现的一股明显潮流，且内部存在方法分歧。**Var-JEPA** 论证JEPA与变分推断在结构上等价，标准JEPA可视为确定性特例，据此推导出用单一 **ELBO** 显式建模隐变量生成结构的 Var-JEPA，并实例化为表格版 **Var-T-JEPA**；在真实表格基准上它超过 **T-JEPA**，与强原始特征基线相当，且ELBO自然防坍缩，无需反坍缩正则 [9]。**VJEPA/BJEPA** 走得更远，把JEPA从确定性回归推广为概率形式，学习未来隐状态的概率预测分布，并证明其与预测状态表示和贝叶斯滤波统一；进一步提出 **BJEPA**，用专家乘积分解预测信念以支持零样本任务迁移与约束满足 [10]。在含高方差干扰的噪声线性系统（Noisy TV玩具实验）中，VJEPA/BJEPA 成功滤除导致生成式基线坍塌的干扰，并可采样构建可信区间，但两者都仅在玩具实验或表格数据上验证，未在大规模高维真实环境评估 [10][9]。**BiJEPA** 则针对对称预测的表征爆炸问题引入表征向量范数正则化，训练前向与后向两个预测器，强制数据片段间循环一致可预测性；在合成周期信号、Lorenz混沌轨迹与MNIST上稳定收敛无坍塌，捕获混沌系统语义结构，并学习到可生成与泛化的时空表征，但同样未扩展至大规模真实数据 [11]。这三项工作共同指向「概率化可带来不确定性量化与防坍塌」的结论，但证据强度差异很大：Var-JEPA 有真实表格基准，VJEPA/BJEPA 与 BiJEPA 基本停留在玩具或小规模数据 [9][10][11]。

潜空间世界模型用于规划时，最尖锐的批评来自「决策局部预测差距」。**D-JEPA** 明确指出：预测隐距离更近的候选动作可能实际失败，即潜空间中的接近性并不等于决策上的可取性；为此它用有界置换等变算子从已执行结果中学习候选未来间的决策相关关系，并将决策结构写入JEPA兼容的未来表征 [12]。实验上，D-JEPA 在 **PushT** 达到 **87.89%** 成功率，**RoboTwin** 平均提升 **15.04点**，真实机器人任务提升 **17点**，但依赖已执行候选结果监督，并需预训练预测几何 [12]。与之互补的是 **Flow-JEPA**，它针对 LeWM 确定性自回归预测的误差累积与视觉扰动敏感问题，用条件流匹配以高斯源轨迹生成未来潜状态序列，替代逐点一步转移回归，同时保持无重建JEPA框架；在四个环境上干净观测成功率从 **86%→92%**，噪声下从 **67%→86%** [41]。这两项工作从不同侧面修正同一个缺陷：D-JEPA 修正「潜距离不等于决策质量」，Flow-JEPA 修正「单步确定性转移在噪声下脆弱」；但 Flow-JEPA 尚处工作进展中，未报告更大规模或更长时域泛化，D-JEPA 的监督依赖也限制了其数据效率 [12][41]。

面向机器人规划的一批工作则更强调物理接地与状态对齐。有研究提出端到端JEPA世界模型，在潜在预测基础上增加逆动力学和状态对齐目标：逆动力学防止潜在坍缩并使潜在转移包含动作信息，状态对齐将连续表示锚定到物理状态；在四个基准任务上 **TwoRoom 达100%**、**PushT 达98%**、**OGBench-Cube 达87%**，消融显示状态对齐一致提升规划成功率，但 **Reacher** 任务仅与基线相当，过渡子空间维度分析有限 [42]。**TC-WM** 则把冻结视觉基础模型嵌入当作语义脚手架而非最终状态空间，通过线性投影得到紧凑动态潜空间，用对比学习对齐智能体物理状态子空间，并重建嵌入保留视觉结构；理论上可辨识任务中心潜因子，在 **Robomimic** 与 **D4RL** 上实现更优世界建模与更精确控制，但依赖预训练视觉基础模型且全文未公开 [43]。**GLAM** 把潜世界模型扩展到导航：基于全局时空记忆的目标条件模型以JEPA式潜预测在地图级token上联合预测未来地图表示与机器人中心路点潜变量，用预训练路点编解码器监督解码，在 Habitat/HM3D 的 ObjectNav 子集上成功率与SPL均优于复现的 **BSC-Nav** 基线，但其局限在于仅预测专家数据中的未来观测与计划，而非任意动作反事实 [44]。这三项工作对「什么该被对齐」给出了三种不同答案——物理状态、任务中心潜因子、地图与路点——目前没有统一评测能判断哪种对齐更通用 [42][43][44]。

动作条件与无动作标签学习是另一条并行线索。**UWM** 在统一Transformer中集成动作扩散与视频扩散过程，各模态由独立扩散时间步控制，通过控制扩散时间步可灵活表示策略、前向动态、逆向动态与视频生成器；实验表明其预训练策略比模仿学习更泛化鲁棒，并能利用无动作视频数据进一步提升性能，但未明确给出定量指标与真实世界任务规模细节 [45]。**CLAW** 则从无动作标签视频中端到端自监督学习连续潜动作世界模型，用对抗潜正则与扩散视频生成同时训练潜动作模型和世界模型，从视觉观察推断动作如何引起环境变化；结果显示潜动作具语义性，可支持从观察模仿、动作迁移与目标导向规划，并超越现有方法，但全文未公开，缺乏定量指标与规模细节 [46]。**Music-JEPA** 把这一范式推到音乐领域：将音乐视为动作条件系统，音频为状态、pianoroll为乐器动作，给定当前音频状态和动作预测未来音频状态，完全离线使用成对音频-pianoroll数据训练；学到的表示支持节拍跟踪、作曲家识别、调性估计等下游任务，并可通过规划搜索最佳动作实现钢琴转录，但仅限钢琴领域且离线训练无环境交互 [47]。这三项工作共同说明「动作条件潜预测」不限于机器人，但其证据成熟度差异显著：UWM 有大规模多任务数据但缺定量，CLAW 缺全文，Music-JEPA 有明确下游任务但域窄 [45][46][47]。

并非所有证据都支持JEPA潜目标优于值目标。一项针对表格基础模型的研究直接检验了「能否在表格先验上训练JEPA潜目标而不崩溃」，提出值头读编码器场、潜目标用EMA差分、隐藏单元以掩码token进入预测器的配方，并用平台停止协议对比；结果是收敛后JEPA臂在 **147个真实表格数据集** 上仍落后仅值目标臂，分类差距较小（32:70胜负，按名29:63），回归差距更大（8:24），且需 **1.42倍步数** 与 **1.66倍墙钟** 才能达到平台 [13]。作者也承认收敛后未超越仅值目标臂，且每臂仅一次运行 [13]。这一负面结果与 Var-JEPA 在表格数据上「优于T-JEPA」的结论并不直接矛盾，因为两者比较的基线不同（仅值目标臂 vs. T-JEPA），但合起来提示：JEPA潜目标在表格模态上的收益高度依赖基线选择与训练预算，不能默认其普遍占优 [13][9]。

更早的探索类工作为「潜空间世界模型 + 规划」提供了原型。**Plan2Explore** 通过规划主动寻找预期未来新颖性进行自监督探索，用集成动力学预测下一图像嵌入的分歧作为内在奖励，在潜空间想象 rollout 中反向传播优化探索策略，学习全局世界模型；无任务监督下优于先前自监督探索方法，几乎匹配有奖励oracle，并支持零样本或少样本适应下游任务，但依赖集成动力学分歧，未广泛验证真实机器人 [48]。这一2020年的结果与2026年的 D-JEPA、Flow-JEPA 在问题设定上高度呼应：都在潜空间中做 rollout 并优化动作序列，区别在于 Plan2Explore 的驱动力是探索新颖性，而后者分别关注决策对齐与噪声鲁棒性 [48][12][41]。**Baba in Wonderland** 则处理更极端的先验错位情形：其闭环系统 **Alice** 把失败候选更新视为结构信号，将保留冲突精炼为假设类，并引导探索新颖且欠表示的转移；在替换语义标签的 Baba Is You 变体上显著提升可执行世界模型学习，消融证明类精炼与类感知探索均有贡献，但仅单一游戏环境验证且未提代码公开 [49]。这提示「世界模型的可执行性」在规则可被改写时不能仅靠离线拟合，需要在线假设精炼，而这类方法与主流JEPA的离线预训练范式尚未融合 [49]。

统一化与多任务共享是近期另一条组织线索。**UniJEPA** 在共享潜空间联合学习光度预测（图像级变换）与时间预测（视频级动态），用单一 next-embedding 预测损失加高斯正则化端到端训练，无需EMA、stop-gradient或预训练编码器，并证明可防坍塌；在图像、视频与控制基准上匹配或超越任务专用JEPA（如 **I-JEPA、IWM、V-JEPA 2、DINO-World**），动作条件后训练后支持零样本规划，规划速度比生成式世界模型快 **数十倍** 且精度相当，但动作条件后训练依赖离线轨迹，未验证真实机器人部署 [50]。**DINO-WM** 则代表另一条「借用预训练特征」的路线：利用 **DINOv2** 预训练的块特征预测未来块特征，在不重建视觉世界的情况下建模视觉动态，在离线轨迹上训练并通过动作序列优化实现目标达成，将目标特征作为预测目标支持任务无关规划；在 **六个环境** 上实现零样本行为求解，无需专家演示、奖励建模或逆模型，超越先前SOTA，但依赖预训练DINOv2特征，未验证其他特征或真实机器人 [51]。UniJEPA 与 DINO-WM 的对比颇具意味：前者主张从零端到端训练统一目标，后者主张冻结强特征只学动力学；UniJEPA 报告规划速度优势，DINO-WM 报告零样本行为求解，但两者都未在真实机器人上验证，因此「统一目标 vs. 冻结特征」的取舍仍缺决定性证据 [50][51]。

最后，非视觉模态与生成式对照提醒我们潜空间预测的边界。**MC-JEPA** 用共享编码器联合学习光流和内容特征，结合光流估计目标与自监督学习目标，使内容特征融入运动信息；在无监督光流基准上与现有方法相当，并在图像和视频语义分割等下游任务上与常见SSL方法相当，但未明确讨论共享编码器中运动与内容目标冲突、光流标注依赖或复杂场景泛化限制 [52]。**Graph-JEPA** 把JEPA用于图级表征，采用掩码建模从上下文子图潜表征预测被掩码子图潜表征，并用单位双曲线二维坐标预测目标赋予隐式层次；实验发现其能学习高语义表达表征，在图分类、回归及区分非同构图等下游任务中表现良好，但未明确讨论图规模扩展、复杂图结构泛化和预测目标计算成本 [53]。与此同时，生成式世界模型并未退出竞争：**SANA-WM** 作为 **2.6B** 参数开源世界模型，原生支持一分钟720p视频生成与精确相机控制，采用混合线性注意力、双分支相机控制、两阶段生成与鲁棒标注流程，在约 **21.3万** 公开视频片段（含度量尺度位姿监督）上训练，用 **64张H100训练15天**，单GPU可生成60秒720p，蒸馏版在单张 **RTX 5090 NVFP4** 下 **34秒** 去噪60秒720p；其动作跟随精度优于开源基线，视觉质量接近工业级模型且效率显著提升，但训练仍需64张H100，计算成本较高 [14]。SANA-WM 的存在说明「避免生成式高算力」这一JEPA动机在2026年仍未被完全兑现：潜空间方法在规划速度上有优势，但生成式方法在分钟级高分辨率可控生成上仍保持能力，两者更可能是分工而非替代 [1]。

### 2.2 掩码与自蒸馏表征

掩码建模与自蒸馏构成了自监督表征学习中两条彼此纠缠的技术路线：前者通过重建或预测被遮蔽的部分迫使模型学习结构信息，后者通过让模型预测自身或教师的表征来避免像素级重建的短视性。二者在视觉、语音、音频、点云、图、三维场景乃至语言与生物序列上被反复验证，也在方法细节上不断发生分歧——掩码比例该多高、预测目标该在像素空间还是潜空间、是否需要负样本、教师信号该来自哪一层。以下按方法谱系与子问题展开。

**掩码自编码器的核心设计**在视觉领域由MAE确立：随机掩码输入图像块并重建缺失像素，编码器仅处理可见块，配合轻量解码器，掩码比例约**75%**，ViT-Huge在ImageNet-1K达**87.8%**准确率，训练加速3倍以上，迁移性能超过监督预训练[32]。这一非对称编解码结构随后被广泛移植。VideoMAE把图像MAE扩展到视频，采用**90%-95%**的极高比例视频管状掩码，使重建任务更具挑战性，在仅3k-4k视频的小数据集上无额外数据即取得Kinetics-400 **87.4%**、SSv2 **75.4%**、UCF101 **91.3%**、HMDB51 **62.6%**，并强调数据质量比数据数量更重要[30]。Audio-MAE则把同一思路简单扩展到音频频谱图，编码器以高掩码率只处理非掩码token，解码器重排并补掩码token重建频谱图，并在解码器引入局部窗口注意力，在六个音频与语音分类任务上取得新SOTA，超过使用外部监督预训练的模型[33]。点云领域的对应工作针对位置信息泄漏和信息密度不均问题，将点云划分为不规则点块并高比例随机掩码，用非对称标准Transformer和移位掩码token从可见点块重建被掩码点块，在ScanObjectNN达**85.18%**、ModelNet40达**94.04%**，少样本分类提升**1.5%-2.3%**[34]。这些结果共同表明，掩码重建的收益高度依赖掩码比例与数据模态的冗余结构，但各工作对计算成本与泛化边界的讨论普遍不足[30][34]。

**掩码预测的目标空间**很快成为分歧点。CAE主张在编码表征空间而非像素空间做预测，采用编码器-回归器-解码器结构：编码器处理可见块，回归器预测掩码块表征，解码器重建掩码块，在分割、检测和分类等下游任务上迁移性能优越，并认为分离表征学习与预训练任务有益[54]。这与MAE在像素空间重建的路线形成对照，前者强调语义抽象，后者强调实现简洁与可扩展性[32]。SiameseIM进一步把预测目标推向另一视图的稠密表征：基于同一图像的另一掩码视图预测增强视图的表征，在线分支编码第一视图并按相对位置预测第二视图表征，目标分支编码第二视图，从而同时获得语义对齐与空间敏感性，在ImageNet微调与线性探测、COCO、LVIS等下游任务上超越实例判别（ID）与掩码图像建模（MIM）方法[55]。CMAE则试图统一对比学习与掩码图像建模：在线分支用非对称编码器-解码器重建掩码图像，动量分支用全图进行对比学习，并引入像素移位与特征解码器，使表征兼具实例判别性与局部感知性，迁移性能优于MIM对应方法[56]。这三项工作从不同方向回应了同一争议：纯像素重建是否足以产生高层语义，抑或必须引入潜空间或视图间的预测目标。

**自蒸馏路线**以BYOL和DINO为代表，绕开了负样本与重建。BYOL使用在线网络和目标网络，在线网络从一幅图像的一种增强视图预测目标网络对同一图像另一增强视图的表征，目标网络用在线参数的慢速移动平均更新，在ImageNet线性评估下ResNet-50达**74.3%**、更大ResNet达**79.6%**，迁移与半监督基准持平或优于当时最先进方法；其局限在于目标函数存在坍缩解，依赖预测器和慢速移动平均避免坍缩[18]。DINO把自监督实现为无标签自蒸馏，强调动量编码器、多裁剪训练和小patch的重要性，发现自监督ViT特征包含显式语义分割信息且是优秀k-NN分类器，小ViT达**78.3%**，ViT-Base线性评估达**80.1%**[17]。与之对照，SimCLR走的是对比路线：通过组合数据增强、表示与对比损失间可学习非线性变换、归一化嵌入与温度参数，最大化同一样本不同增强视图的一致性，ImageNet线性评估达**76.5%** top-1，较此前SOTA相对提升**7%**，1%标签微调达**85.8%** top-5，12个数据集中10个不逊于强监督基线，但需大batch与长训练，算力开销大[37]。MoCo则从字典查找视角构建带队列与动量编码器的动态字典，队列使字典大且一致，动量编码器保证特征一致性，在ImageNet线性协议上具竞争力，并在PASCAL VOC、COCO等7个检测/分割任务上可超越监督预训练，部分大幅领先[38]。BYOL与SimCLR/MoCo之间的核心争议在于负样本是否必要：BYOL声称无需负样本即可达到可比性能，但其坍缩风险与对移动平均的依赖也被明确标注[18]。

**联合嵌入预测架构（JEPA）**把自蒸馏与掩码预测合并为一条更简洁的路线。I-JEPA从单个上下文块预测同一图像中多个目标块的表征，通过采样大尺度目标块和空间分布充分的上下文块引导语义表征，不依赖手工数据增强，用**16张A100**在ImageNet训练ViT-Huge/14少于**72小时**，在线性分类、物体计数和深度预测等下游任务表现强[15]。Bootleg则指出仅重建低层数据或依赖最终层非平稳自蒸馏目标的不足，通过预测教师多个隐藏层的潜表征训练模型，用分层目标迫使模型同时捕获不同抽象层级特征，在ImageNet-1K、iNaturalist-21、VTAB冻结探针分类上较I-JEPA提升**+10%**，并在ADE20K、Cityscapes、COCO-Stuff语义分割上显著优于可比基线[16]。这两项工作的时间跨度显示了JEPA内部从单层目标向多层教师目标的演进，但Bootleg未明确讨论多层教师目标带来的训练成本与教师设计依赖[16]。

**JEPA向非视觉模态的迁移**在音频与语言上出现了分化。Audio-JEPA用ViT骨干预测掩码梅尔频谱块的隐表征而非重建原始音频，在无标签AudioSet上随机块掩码预训练，在X-ARES套件上评估语音、音乐和环境声任务，性能与wav2vec 2.0和data2vec相当，但训练数据不足其五分之一且无需调参；其局限在于仅将原模型直接迁移到音频，未做超参调优[19]。MJEPA则用单一统一编码器与单一预测目标做音视频联合嵌入预测，目标同时施加于模态内与跨模态预测，跨模态预测对共享编码器收益关键，冻结ViT-g在AudioSet-20K超最佳冻结基线**6.8 mAP**以上，在ESC-50与FSD50K超全微调模型，且用少**10倍**视频数据在视频基准上具竞争力；其局限是跨模态预测缺失时共享编码器退化[20]。DLLM-JEPA把JEPA目标引入掩码扩散语言模型，利用扩散噪声调度从单一输入构造两个视图，无需配对数据，每步单次梯度传播，较LLM-JEPA减少**33%**训练FLOPs，在4任务×2骨干上一致提升，GSM8K提升**+1.8pp**，并观察到几何漂移增大而功能遗忘更小的分离现象；增益在稳定设置下较温和，主要验证于有限任务与骨干[21]。这三项工作共同显示JEPA的跨模态可迁移性，但Audio-JEPA与MJEPA在是否调参、是否共享编码器上采取了相反策略，前者明确未调参，后者强调统一编码器[19][20]。

**语音与高能物理**提供了掩码预测在非图像连续信号上的早期证据。HuBERT用离线聚类提供对齐目标，先对连续语音特征做k-means聚类，再仅在掩码区域预测隐藏单元标签并迭代聚类，从**100簇**k-means和两轮迭代开始，在Librispeech与Libri-light多规模微调下可匹配或超越wav2vec 2.0，**1B**参数模型在dev-other/test-other相对WER降低最高**19%/13%**；其局限是依赖离线聚类步骤的一致性，未明确讨论聚类质量与计算开销[57]。MPM把掩码粒子建模用于高能物理无序输入集合，掩码粒子并预测其由预训练VQ-VAE离散化得到的token身份，学习置换不变函数，并研究离散化、置换不变性和顺序影响，模型可微调用于监督和弱监督喷注分类，并能用小规模微调数据迁移到新类别和新数据域；其局限是依赖预训练VQ-VAE离散token，未明确讨论离散化误差和跨任务泛化上限[36]。二者都把连续输入离散化为token再掩码预测，与HuBERT的离线聚类和MPM的VQ-VAE在离散化机制上不同，但都面临离散化质量对最终表征的约束[57][36]。

**三维与图结构**上的掩码与对比方法则面对各自的结构性难题。NeRF-MAE用掩码自编码器对NeRF辐射与密度网格进行自监督预训练，将NeRF体素网格作为密集输入，利用相机轨迹采样规范化场景，随机掩码patch并用3D Swin Transformer重建，在超**180万**张位姿RGB图像上预训练，编码器可有效用于3D迁移学习；其局限是依赖相机轨迹采样，掩码自编码器应用于隐式NeRF表征存在困难[35]。GraphCL设计四类图增强引入不同先验，通过最大化不同增强视图间特征一致性学习不变表征，在半监督、无监督、迁移和对抗攻击四设置下，无需调增强幅度或复杂架构即达到与SOTA相似或更好的泛化、迁移与鲁棒性；其局限是增强类型与幅度需选择，参数化增强仅初步实验[39]。NeRF-MAE把掩码重建推向隐式三维表征，GraphCL则坚持对比路线，二者在是否依赖重建目标上形成对照，但都受限于各自的结构假设——相机轨迹与图增强设计[35][39]。

**自蒸馏在生物序列与病理图像**上的应用显示了潜空间对齐相对于观测空间重建的优势。scRep用潜空间自蒸馏替代观测空间重建来学习单细胞表征，通过对同一细胞不同扰动视图做动量师生对齐，并在细胞和基因两个层面施加自蒸馏目标，在约**280万**细胞上预训练即取得冻结表征基准最优总体表现，扩到**3072万**细胞仍有效；其局限是仅评估冻结表征，未做任务微调[58]。病理基础模型工作构建了含**30亿**张图像、**42.3万**张切片的病理数据集，采用MAE和DINO两种自监督算法预训练视觉Transformer，并在乳腺癌检测、炎症性肠病检测、雌激素受体预测、EGFR突变预测和免疫治疗响应预测等六项临床任务上评估，结果显示病理数据预训练优于自然图像预训练，且DINO算法表现更佳；其局限是仅对比MAE与DINO，未覆盖更多SSL算法[27]。这两项工作共同指向一个经验性结论：在数据规模极大且观测空间噪声高的领域，潜空间自蒸馏或动量教师路线往往优于像素/表达重建，但病理工作的对比范围有限，尚不能推广为普遍规律[27]。

**早期系统研究**为上述方法提供了基准与警示。Revisiting Self-Supervised Visual Representation Learning对多种自监督视觉表征学习方法进行大规模系统研究，通过统一实验揭示CNN设计标准配方不总适用于自监督学习，发现调整架构与训练策略可大幅提升性能并超越此前SOTA[28]。Scaling and Benchmarking Self-Supervised Visual Representation Learning将两种流行自监督方法扩展至**1亿**图像，在9个数据集任务上建立基准，发现可匹配或超越监督预训练，但现有方法仍不足以充分利用大规模数据，未学到有效高层语义，且当前自监督方法不够“难”[29]。这两项2019年的工作与后续MAE、DINO、I-JEPA等形成时间上的呼应：前者指出的“方法不够难、未充分利用数据”在VideoMAE的极高掩码率与I-JEPA的大尺度目标块采样中得到部分回应[30][15]，但Scaling and Benchmarking所指出的高层语义不足问题，在后续工作中仍以语义分割、物体计数、深度预测等下游任务间接评估，缺乏统一诊断[15]。

**综述框架**为上述分歧提供了分类坐标。Self-Supervised Learning: Generative or Contrastive系统回顾计算机视觉、自然语言处理和图学习中的经验方法，按目标归纳为生成式、对比式和生成-对比式（对抗）三类，并收集相关理论分析，指出自监督学习利用输入数据自身作为监督可惠及多种下游任务，同时讨论开放问题与未来方向；作为综述，它未提出统一新方法，覆盖范围受当时文献限制[31]。以此框架回看，MAE、VideoMAE、Audio-MAE、点云MAE、NeRF-MAE、MPM属于生成式掩码重建[32][30][33][34][35][36]；SimCLR、MoCo、GraphCL属于对比式[37][38][39]；BYOL、DINO、scRep属于自蒸馏/生成-对比的交叉地带[18][17][58]；CAE、SiameseIM、CMAE、I-JEPA、Bootleg、Audio-JEPA、MJEPA、DLLM-JEPA则处于掩码预测与潜空间预测的混合区间[54][55][56][15][16][19][20][21]。这一分类也暴露了争议：HuBERT与MPM的离散token预测既可视为生成式掩码预测，也可视为潜空间对齐[57][36]；病理工作中DINO优于MAE的结果[27]与MAE在自然图像上的强势[32]并不矛盾，但提示算法优劣高度依赖数据域与评估协议。总体而言，掩码与自蒸馏的边界正在被JEPA类工作持续模糊，而各方法在掩码比例、目标空间、教师层数、是否共享编码器等设计上的差异，仍是决定其成败的关键变量，也是当前证据尚不足以统一裁决的开放地带。

### 2.3 新架构：状态空间与线性注意力

在扩散模型从 U-Net 向 Transformer 主干迁移的过程中，**DiT-XL/2** 这类纯注意力架构虽然具备良好的可扩展性，但其全局自注意力的二次复杂度在**ImageNet 256×256 与 512×512** 等高分辨率生成任务上带来了沉重的计算负担。LaMamba-Diff 正是在这一子问题上提出的新架构方案：它设计了一种 **Local Attentional Mamba 块**，将自注意力与 Mamba 两种机制组合进 U-Net 式的编解码结构中，试图在保持线性复杂度的同时兼顾全局上下文建模与局部细节刻画 [59]。其核心主张是，单一地用状态空间模型替换注意力会牺牲局部保真度，而单一地保留注意力又无法摆脱算力瓶颈，因此混合化是必要的折中路径 [59]。从结果看，该工作报告其最大模型相较 **DiT-XL/2 减少了 62% 的 GFLOPs**，参数量相当或更少，并在 256×256 上超越了 DiT 的各规模版本，代码已在 GitHub 开源 [59]。这一数字意味着线性注意力/状态空间路线在图像生成这一具体场景中，已经不只是理论上的效率优势，而是能够在同等或更小参数预算下转化为实际的质量收益。

不过，这一证据也暴露出该方向内部尚未解决的争议与张力。LaMamba-Diff 的局限被明确标注为**未充分讨论 Mamba 压缩导致局部细节信息损失的残余影响** [59]，这恰恰触及状态空间模型与线性注意力共同面对的核心质疑：线性复杂度往往以牺牲对长程依赖中精细结构的精确建模为代价，而扩散生成对纹理、边缘等局部细节高度敏感。换言之，该工作用混合架构缓解而非消除了这一矛盾——它把自注意力保留在需要局部精度的位置，把 Mamba 用于承担全局与长程建模，但 Mamba 分支本身的信息压缩损失究竟在多大程度上被补偿、在哪些尺度上仍会显现，证据中并未给出结论 [59]。因此，在「世界模型与自监督表征学习」的语境下，这条证据的价值在于提供了一个可检验的架构假设：状态空间与注意力的混合而非替代，可能是兼顾效率与表征保真度的现实路线，但其代价与适用边界仍需更细粒度的消融与诊断来确认 [59]。

## 3 数据与基准

（本节暂无入库证据）

## 4 向科学数据的迁移

将世界模型与自监督表征学习迁移到科学数据，首先遇到的差异是数据形态：自然图像是规则网格，而科学数据往往是连续粒子云、基因组序列或表格样本。JetParticle-JEPA（JP-JEPA）直接面向高能物理的连续粒子云，基于Particle Transformer骨干，预测被掩码粒子的潜表征，而不做分词或重建原始输入 [23]。在JetClass上，它媲美全监督SOTA，低标签场景超越监督基线，并显著优于现有SSL方法，且在缺失探测器信息时展现鲁棒性 [23]。但该工作仅基于模拟数据，未报告真实探测器数据上的表现 [23]，这提示科学迁移中的仿真到现实鸿沟尚未被证据覆盖。与之呼应，JEPA-DNA把联合嵌入预测架构引入基因组基础模型的持续训练，在潜空间监督全局序列嵌入、预测被掩码基因组片段的功能表征，并保留传统生成目标 [22]。它在17项基因组基准上线性探测与零样本性能一致提升，监督线性探测达到新SOTA，超过DNABERT-2、NTv3、HyenaDNA及MLM/NTP基线 [22]。两者的共同主张是潜语义对齐优于纯token重建，但JEPA-DNA仅作为持续预训练阶段、依赖已有GFM，且未明确跨物种泛化边界 [22]，这与JP-JEPA从零训练、但受限于模拟数据的路径形成互补而非互证。

在更接近决策与干预的科学场景中，能力层级成为组织证据的另一条线索。医疗世界模型综述覆盖医学影像诊断、EHR疾病进展建模与机器人手术规划，提出从L1时序预测、L2动作条件预测、L3反事实到L4规划控制的分级标准 [60]。其核心发现是多数系统仅达L1–L2，少数达L3，L4罕见，并指出动作空间不明确、干预验证薄弱、多模态状态构建不完整等跨领域缺口 [60]。这一判断与单细胞基因组的基准结论存在张力：后者在超2000万细胞上系统比较MAE与对比学习，发现MAE优于对比学习，与计算机视觉中对比学习占优的趋势相反，并在零样本细胞类型预测中表现突出 [25]。但同一工作也承认SSL优势场景有限，主要见于迁移学习 [25]，说明“自监督普遍更优”在科学数据上并不成立，收益高度依赖下游任务与标签可得性。RegFormer则从另一侧推进：它把基因调控网络先验与Mamba状态空间架构结合，在2500万人类细胞上生成式预训练，学习基因表达动态与调控层级，并在细胞注释、GRN重建、遗传扰动预测与药物响应建模上持续超越scGPT与Geneformer [61]。不过它未明确讨论跨物种与跨组织泛化能力 [61]，因此其“先验注入优于纯规模扩展”的结论仍限于人类细胞范围。

当科学数据来自多传感器观测时，迁移策略转向模块化与路由。Mini-JEPA舰队由五个22M参数的传感器专用小型JEPA组成，共享ViT骨干与JEPA训练配方，每个模型重建与其传感器物理匹配的环境变量，再由路由LLM选择合适传感器 [62]。各模型最佳预测变量即其传感器所观测变量，R²达0.97（高程/温度）与0.81（降水）；联合模型对土壤湿度等变量的ΔR²达0.031；路由命中率完美，d=1.10, p=0.031 [62]。它在物理匹配问题上媲美Google AlphaEarth，联合检索在单传感器问题上显著优于AlphaEarth [62]，但总体问题类型聚合增益有限，且路由LLM依赖闭源模型 [62]。表格数据则提供了无增强的第三条路径：T-JEPA从同一表格样本一个特征子集的潜表征预测另一子集的潜表征，实现潜空间掩码重建，无需数据增强 [63]。它在分类与回归任务上显著提升，部分方法持续超越或匹配GBDT，但需引入正则化token以稳定训练，且未在大规模表格上验证 [63]。综合来看，科学数据迁移的争议集中在三点：潜空间预测是否普遍优于重建或对比学习 [25][22]；领域先验与规模扩展谁更关键 [61]；以及从L1–L2预测走向L3–L4干预规划时，动作空间与验证缺口如何补齐 [60]。

## 5 评测、可复现性与争议

在自监督表征学习的评测实践中，病理基础模型的临床基准测试揭示了一个核心张力：算法选择与任务层级共同决定模型排名，而非存在单一最优解。该研究系统梳理了**CTransPath、Phikon、UNI、Virchow、Prov-GigaPath**等公开自监督病理基础模型的训练数据与算法，采用瓦片编码加聚合的两阶段流程评估下游临床任务，发现**DINO算法优于MAE**[26]。这一结论与自然图像领域早期自监督评测中MAE在细粒度任务上常具竞争力的图景形成对照，暗示领域数据特性可能重塑算法偏好。然而，该基准同时指出各模型在瓦片级与切片级任务上表现不一，说明评测结论高度依赖任务粒度与聚合策略[26]。更根本的争议在于可复现性基础：数字病理采用率低、数据与算力缺乏，且全切片图像分辨率极高，这些约束使得大规模公平复现难以实现，公开基准的结论可能受限于参与评测的模型集合与机构数据分布[26]。换言之，该工作既提供了迄今较系统的临床评测框架，也暴露了病理SSL仍处早期、评测生态尚未成熟的现实。

与上述静态基准评测形成方法论对照的是面向世界模型测试时自适应的Sandwich-Residuals，它将可复现性与评测争议推向另一个维度：当环境发生偏移时，冻结模型是否足够，以及参数高效的自适应能否在不访问源域数据的前提下缩小性能差距。该方法冻结预训练世界模型，仅学习预测器前后的轻量残差修正，残差用模型自监督预测误差在线优化，无需奖励、标签或源域数据[64]。在**AdaJEPA基准21种条件**下，其成功率达冻结模型的**1.3倍**，同时少调**97–99%参数**，复合偏移下提升至**1.9倍**，并在**DINO-WM三维操作**上得到验证[64]。但争议恰在其边界：复合偏移下该方法仅与内部块自适应相当，未超越最强AdaJEPA变体，说明轻量残差在极端分布偏移下存在性能天花板[64]。这与病理基准中DINO优于MAE的结论并不直接冲突，但共同指向一个未决问题：评测所衡量的究竟是表征质量本身，还是特定自适应策略与任务分布的耦合优势。两篇证据在时间上相隔一年、领域迥异，却都表明当前自监督世界模型与表征学习的评测仍高度情境化，可复现性受数据、算力与基准覆盖范围的多重制约。

## 6 空白与趋势

**趋势一：JEPA 正从「确定性单步预测」走向「概率化与流匹配」，但证据强度严重不均。** Var-JEPA 论证 JEPA 与变分推断结构等价，用单一 ELBO 显式建模隐变量生成结构，在真实表格基准上超过 T-JEPA 且无需反坍缩正则 [9]；VJEPA/BJEPA 把 JEPA 推广为概率形式并证明其与预测状态表示、贝叶斯滤波统一，用专家乘积分解预测信念支持零样本迁移 [10]；BiJEPA 用范数正则化解决对称预测的表征爆炸，在 Lorenz 混沌轨迹上稳定收敛 [11]；Flow-JEPA 用条件流匹配替代逐点一步转移回归，噪声下成功率从 67% 提升到 86% [41]。**但这条线上只有 Var-JEPA 有真实表格基准，VJEPA/BJEPA 与 BiJEPA 基本停留在玩具或小规模数据，Flow-JEPA 尚处工作进展中且未报告长时域泛化 [9][10][11][41]。** 没人做的方向是：在统一的高维真实环境（而非玩具系统或表格）上，把概率化 JEPA 的不确定性估计质量与规划成功率、样本效率放在同一协议下比较。

**趋势二：防坍塌机制出现「去启发式」与「加结构」的路线对撞，且缺乏统一裁决协议。** LeJEPA 主张各向同性高斯是嵌入最优分布，用 SIGReg 约束嵌入，去掉 stop-gradient、教师学生与调度器，覆盖 10+ 数据集与 60+ 架构，ViT-H/14 在 ImageNet-1k 线性评估达 79% [7]；UniJEPA 同样声称无需 EMA、stop-gradient 或预训练编码器，用单一 next-embedding 损失加高斯正则即可防坍塌 [50]。与之相反，SiamJEPA 发现孪生编码器对 JEPA 目标起正则作用，提升表征可分性并加速早期学习，在有限预算下持续优于单编码器变体 [8]；LeJEPA 与 SiamJEPA 的评测域完全不同（ImageNet 线性探测 vs. 10+ 数据集 60+ 架构），**「哪种防坍塌更优」目前无法在统一协议下裁决 [7][8]。** 空白在于：缺少一个跨架构、跨模态、固定预训练预算的防坍塌基准，把「分布正则」「孪生编码器」「EMA 教师」「stop-gradient」作为可消融变量而非各自论文的默认配置。

**趋势三：潜空间世界模型的规划缺陷被精确定位，但修正方案各自引入新的监督依赖。** D-JEPA 指出「决策局部预测差距」——预测隐距离更近的候选动作可能实际失败，用有界置换等变算子从已执行结果中学习决策相关关系，PushT 达 87.89%、RoboTwin 平均提升 15.04 点 [12]；Flow-JEPA 针对确定性自回归的误差累积与视觉扰动敏感，用流匹配生成未来潜状态序列 [41]；物理接地路线则增加逆动力学与状态对齐目标，TwoRoom 达 100%、PushT 达 98%、OGBench-Cube 达 87%，但 Reacher 仅与基线相当 [42]。**这些工作共同承认「潜空间接近性 ≠ 决策可取性」，但 D-JEPA 依赖已执行候选结果监督，Flow-JEPA 未报告更大规模泛化，物理接地路线依赖预训练视觉基础模型且部分全文未公开 [12][41][42][43]。** 没人做的是：在无已执行结果、无预训练编码器的条件下，仅靠离线轨迹同时解决决策对齐与噪声鲁棒性。

**趋势四：JEPA 向科学数据（组学、病理、高能物理、表格）迁移已出现系统性证据，但结论高度依赖基线与模态。** 正面证据包括：JEPA-DNA 在 17 项基因组基准上线性探测与零样本一致提升，证明潜语义对齐优于纯 token 重建 [22]；HEP-JEPA 在 1 亿喷注上预训练，下游与高能物理 SOTA 可比 [24]；JetParticle-JEPA 在 JetClass 上媲美全监督 SOTA，低标签场景超越监督基线 [23]；病理基准显示 DINO 优于 MAE，但病理领域 SSL 仍处早期 [26]；单细胞基因组基准发现 MAE 优于对比学习，与计算机视觉趋势相反 [25]。**负面证据同样明确：一项表格基础模型研究在 147 个真实数据集上发现，收敛后 JEPA 臂仍落后仅值目标臂（分类 32:70 胜负，回归 8:24），且需 1.42 倍步数与 1.66 倍墙钟 [13]。** 这与 Var-JEPA 在表格上「优于 T-JEPA」并不矛盾，因为基线不同（仅值目标臂 vs. T-JEPA），但合起来提示 **JEPA 潜目标在表格模态上的收益高度依赖基线选择与训练预算，不能默认其普遍占优 [13][9]。** 空白在于：科学数据上缺少像病理基准 [26] 那样统一瓦片编码加聚合流程的 JEPA 专项评测，组学、高能物理、表格各自为战，无法判断「潜空间预测在科学数据上何时优于重建或值目标」。

**趋势五：统一化与多任务共享成为组织线索，但「统一目标 vs. 冻结强特征」的取舍仍缺决定性证据。** UniJEPA 在共享潜空间联合学习光度预测与时间预测，用单一 next-embedding 损失加高斯正则端到端训练，在图像、视频与控制基准上匹配或超越任务专用 JEPA，规划速度比生成式世界模型快数十倍 [50]；DINO-WM 则冻结 DINOv2 块特征只学动力学，在六个环境上零样本行为求解，无需专家演示、奖励建模或逆模型 [51]。**两者都未在真实机器人上验证，因此「统一目标 vs. 冻结特征」的取舍仍缺决定性证据 [50][51]。** 与此同时，生成式世界模型并未退出竞争：SANA-WM 作为 2.6B 参数开源世界模型，原生支持一分钟 720p 视频生成与精确相机控制，单 GPU 可生成 60 秒 720p，蒸馏版在单张 RTX 5090 NVFP4 下 34 秒去噪 60 秒 720p，但训练仍需 64 张 H100 训练 15 天 [14]。**这说明「避免生成式高算力」这一 JEPA 动机在 2026 年仍未被完全兑现：潜空间方法在规划速度上有优势，生成式方法在分钟级高分辨率可控生成上仍保持能力，两者更可能是分工而非替代 [14][1]。** 没人做的是：在同一任务上同时评测潜空间规划与生成式规划的成功率、算力、幻觉率与长时域稳定性，给出「何时该用哪种」的判据。

**趋势六：动作条件与无动作标签学习向非机器人域扩散，但证据成熟度差异显著。** UWM 在统一 Transformer 中集成动作扩散与视频扩散，通过控制扩散时间步灵活表示策略、前向动态、逆向动态与视频生成器，预训练策略比模仿学习更泛化鲁棒，并能利用无动作视频数据 [45]；CLAW 从无动作标签视频端到端学习连续潜动作世界模型，用对抗潜正则与扩散视频生成同时训练，潜动作可支持观察模仿、动作迁移与目标导向规划 [46]；Music-JEPA 把音乐视为动作条件系统，音频为状态、pianoroll 为乐器动作，支持节拍跟踪、作曲家识别、调性估计与钢琴转录 。**但 UWM 未明确给出定量指标与真实世界任务规模细节，CLAW 全文未公开、缺乏定量指标，Music-JEPA 仅限钢琴领域且离线训练无环境交互 [45][46]。** 空白在于：无动作标签学习目前缺少一个跨域（机器人、音乐、医疗时序）的统一评测，来判断「从观察推断动作」在何种数据条件下可靠。

**趋势七：掩码建模与自蒸馏的模态迁移已高度成熟，但「预测目标该在哪个空间」的分歧仍未收敛。** MAE 在像素空间重建，ViT-Huge 在 ImageNet-1K 达 87.8% [32]；CAE 主张在编码表征空间预测，认为分离表征学习与预训练任务有益 [54]；SiameseIM 基于另一掩码视图预测增强视图的稠密表征，同时获得语义对齐与空间敏感性 [55]；CMAE 统一对比学习与掩码图像建模，使表征兼具实例判别性与局部感知性 [56]。**这些工作从不同方向回应同一争议：纯像素重建是否足以产生高层语义，抑或必须引入潜空间或视图间预测目标；但各工作对计算成本与泛化边界的讨论普遍不足，且缺少统一诊断来判定「高层语义不足」是否被真正解决 [32][54][55][56]。** 早期系统研究已警示现有方法「不够难、未充分利用大规模数据、未学到有效高层语义」[29]，后续 VideoMAE 的极高掩码率与 I-JEPA 的大尺度目标块采样部分回应了「不够难」[30][15]，但高层语义不足仍以语义分割、物体计数、深度预测等下游任务间接评估，缺乏统一诊断 [15]。

**趋势八：生物多模态数据的自监督迁移已出现明确信号，但「哪种范式最适合」尚无定论。** scRep 用潜空间自蒸馏替代观测空间重建，在约 280 万细胞上预训练取得冻结表征基准最优总体表现，扩到 3072 万细胞仍有效 [58]；病理基础模型在 30 亿张图像上对比 MAE 与 DINO，发现 DINO 更佳 [27]；单细胞基因组基准发现 MAE 优于对比学习，与计算机视觉趋势相反 [25]；JEPA-DNA 证明潜语义对齐优于纯 token 重建 [22]。**这些结果合起来指向一个经验性结论：在数据规模极大且观测空间噪声高的领域，潜空间自蒸馏或动量教师路线往往优于像素/表达重建；但病理工作仅对比 MAE 与 DINO，单细胞基准仅覆盖有限方法，尚不能推广为普遍规律 [27][25]。** 没人做的是：在生物多模态数据（组学 + 影像 + 时序）上，把 JEPA、掩码建模、对比学习、自蒸馏放在同一预训练预算与同一冻结评测协议下系统比较，并检验跨模态预测（如从影像预测组学潜表征）是否带来额外收益。

## 7 未归类新证据

跨域世界模型长期面临一个张力：共享结构能带来数据效率，但领域异质性又要求表征保留各自的动力学特异性。JEPA-Anything 以**正交预测因子分解**回应这一张力，其做法是把潜在目标拆解为互补且正交的因子，让每个因子经由专用通路学习，再在共享的预测设计中重新组合 [65]。这一设计的关键在于，域无关性并非通过抹平领域差异实现，而是通过把差异分配到彼此正交的子空间中，使共享预测器仍能对各领域的动力学作出区分。证据覆盖视觉、生物、临床、控制、分子、物理场与天气七个领域，并在 10 个动力学任务上与匹配的 JEPA 基线对比，报告称**全部任务均有提升** [65]。其中 Interventional Pong 的单干预预测误差下降 **34.8%**，四系统 100 步分子预测取得最低误差，轨道标度指数拟合斜率为 **-1.4991** [65]。这些结果跨越了从干预式控制到长程分子滚动、再到标度律拟合的不同子问题，说明该框架的收益并不局限于单一任务类型。

值得注意的是，证据同时给出了湿实验与轨道标度律两类验证，这使该工作的方法论主张超出了纯基准比较的范围：标度指数拟合斜率接近 -1.5，意味着模型在轨道动力学上复现了某种可被独立物理规律检验的行为，而非仅仅拟合了训练分布 [65]。但证据也明确提示了一项内在争议：跨域统一框架在部分领域可能牺牲领域特异性 [65]。这与前述"全面超越基线"的结论构成一种张力——整体任务层面的提升，未必等价于每个领域内部都优于领域专用方案，因为基线是匹配的 JEPA 基线而非各领域的最优专用模型。换言之，正交分解在多大程度上真正隔离了领域因子、又在多大程度上以共享容量换取了跨域泛化，证据本身并未给出消融层面的回答。就目前材料看，该工作更稳妥的定位是：它证明了域无关的预测式自监督框架在多个异质动力学任务上可行且有效，代码与模型公开也为后续检验其领域特异性代价提供了条件 [65]。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据（引用数字与 [id]） |
|---|---|---|
| 2.1 预测隐空间与世界模型（JEPA / Dreamer / DINO-WM） | **朝阳** | **n=29**、**recent_share=0.79**、year_span 2020–2026；V-JEPA 2 单篇 **725 引用** [6]，DINO-WM **368** [51]，Unified World Models **229** [45]；但 **cns_share=0.0**、median_citations=0，说明方法未收敛、顶刊尚未接管 |
| 2.2 掩码与自蒸馏表征（MAE / DINO / MoCo / SimCLR） | **成熟** | **n=25** 但 **recent_share=0.20**，year_span 2019–2026，median_citations **520**；SimCLR **26276** [37]、MoCo **15753** [38]、MAE **12863** [32]、DINO **10289** [17]——经典已固化，新工作占比低，属增量为主 |
| 2.3 新架构：状态空间与线性注意力（Mamba / 线性注意力） | **萌芽** | **n=1**、recent_share=0.0、仅 2024 一篇 [59]，**7 引用**；证据库覆盖极弱，属少量探索性工作 |
| 3 数据与基准 | **萌芽（空档）** | **n=0**，无任何证据条目——这是本方向最大的结构性缺口 |
| 4 向科学数据的迁移（单细胞 / 基因组 / 病理） | **朝阳** | **n=7**、**recent_share=0.71**、year_span 2024–2026、**cns_share=0.14**；Delineating SSL in Single-Cell Genomics **39 引用** [25]、RegFormer [61]、JEPA-DNA [22]、JetParticle-JEPA [23] |
| 5 评测、可复现性与争议 | **朝阳（早期）** | **n=2**、**recent_share=1.0**、**cns_share=0.5**、median_citations **39**；病理 SSL 临床基准 **78 引用** [26]、Test-time 世界模型适配 [64] |

**整体判断**

这个方向整体处于**「核心范式已爆发、科学迁移刚起步、评测与基准几乎空白」的错位窗口期**。证据库 **n=65**、**recent_share=0.55**、**2026 年 28 条**，说明热度仍在爬升而非见顶；但结构极度不均：2.1 预测隐空间/世界模型占 **29/65** 且 **79% 是近两年**，2.2 经典自监督已 **成熟**（近两年仅 20%），2.3 新架构只有 **1 条**，而 **3 数据与基准为 0 条**——意味着「方法供给过剩、评测与科学落地供给严重不足」。**CNS 占比整体仅 0.03**，但 4/5 两个迁移与评测板块 **cns_share 分别 0.14 / 0.5**，说明顶刊入口恰恰在「把方法搬到科学数据 + 做严格基准」这一侧，而不是再造一个 JEPA 变体。窗口期判断：**纯方法侧（2.1）大约还有 6–12 个月的高影响窗口**，之后会像 2.2 一样迅速成熟化；**科学迁移 + 评测侧（4/5）窗口更长（12–24 个月）**，因为目前只有 7 + 2 条证据、且 **median_citations 为 0**，几乎无人占位。最大不确定性有三点：一是 **2.1 的 median_citations=0**，说明大量新工作尚未被验证，方法可能快速被下一代架构（SSM/线性注意力，目前仅 1 条证据）替代；二是 **3 数据与基准完全空白**，意味着「什么算好表征」在生物多模态上尚无共识，任何结论都可能被后续基准推翻；三是 **test-time compute / 世界模型适配** 才刚出现单条证据 [64]，若这条线成为主流，静态表征学习的价值会被重估。

**接下来怎么做**

1. **把 JEPA 的「隐空间预测」直接搬到单细胞多组学，做跨模态掩码预测而非重构。** 切入点：用公共 CITE-seq / 10x Multiome（RNA+ATAC）或类器官时序多组学，把一种模态当 context、另一种当 target，在隐空间做预测（而非 MAE 式的原始计数重构），损失用 latent prediction + VICReg 式正则。为什么现在做：JEPA 侧方法已成熟可复用 [6]，而科学迁移侧只有 **7 条**证据、**median_citations=0**，JEPA-DNA [22] 刚出现说明这条路刚被打开、尚未被占满。产出：一个跨模态隐空间预测的表征模型 + 在衰老标签（如细胞衰老评分、供体年龄回归）上的线性探针评测。

2. **抢占「数据与基准」这块 0 证据的空地，做单细胞 SSL 的严格基准。** 切入点：复现 MAE / DINO / 对比学习 / JEPA 四类范式在统一单细胞数据上的表现，控制预训练数据规模、批次效应、下游任务（细胞类型注释、扰动预测、衰老轨迹）。为什么现在做：**3 数据与基准 n=0**，而 5 评测板块 **cns_share=0.5**、病理基准已拿到 **78 引用** [26]，证明「严格基准」在生物医学里是顶刊级贡献；单细胞侧只有一篇方法学批判 [25]（**39 引用**），远未饱和。产出：开源基准 + 负面结果报告，这类工作引用寿命长、且直接支撑你自己的方法选择。

3. **用类器官时序数据做「世界模型」式潜空间动力学建模，切入衰老轨迹预测。** 切入点：把类器官/细胞重编程的时序多组学当作可动作条件化的轨迹，用 DINO-WM 式「在预训练特征上建世界模型」[51] 或 Dreamer 式规划 [48]，预测干预（如部分重编程因子、senolytics）后的状态。为什么现在做：2.1 板块 **79% 近两年**、方法组件现成，但**没有任何一条证据把它用在衰老/类器官时序上**；同时 test-time 适配 [64] 刚出现，说明「世界模型 + 测试时计算」是下一个接口。产出：可做干预规划的潜空间动力学模型 + 湿实验可验证的预测假设。

4. **把状态空间模型 / 线性注意力作为长序列组学的骨干，而不是追 JEPA 变体。** 切入点：单细胞发育轨迹、染色质长程调控、多组学拼接后的超长 token 序列，用 Mamba/线性注意力替换 Transformer 注意力，对比显存-精度曲线。为什么现在做：2.3 只有 **1 条**证据 [59]、**7 引用**，是典型的**萌芽期低竞争高上限**；而 2.2 已成熟、2.1 将成熟，架构侧是唯一还没被填的坑。产出：长序列组学骨干 + 与 Transformer 的等算力对比，属于「方法本身有新意」的迁移，符合纳入标准。

5. **把「评测与可复现性」做成你的差异化标签，绑定公共数据 demo。** 切入点：对已发表的单细胞基础模型（含 RegFormer [61]）做独立复现 + 数据泄漏审计 + 跨数据集泛化测试，模仿病理基准的做法 [26]。为什么现在做：5 板块 **recent_share=1.0**、**cns_share=0.5**，说明这类工作刚被顶刊认可且供给极少；同时 4 板块 **cns_share=0.14** 表明科学迁移类工作正在进入高影响通道。产出：可复现性报告 + 公开评测套件，成本低、周期短，且能立刻反哺你前 4 条的方法选择。

## 参考文献

1. Self-Supervised JEPA-based World Models for LiDAR Occupancy Completion and Forecasting.  2026. https://arxiv.org/abs/2602.12540v1
2. 3D-JEPA: A Joint Embedding Predictive Architecture for 3D Self-Supervised Representation Learning. arXiv.org 2024. https://doi.org/10.48550/arXiv.2409.15803
3. Does Latent Planning Survive Point Clouds? Action-Conditioned JEPA World Models for Geometric Observations.  2026. https://arxiv.org/abs/2608.29434
4. CrossJEPA: Cross-Modal Joint-Embedding Predictive Architecture for Efficient 3D Representation Learning from 2D Images. arXiv.org 2025. https://doi.org/10.48550/arXiv.2511.18424
5. Point-JEPA: A Joint Embedding Predictive Architecture for Self-Supervised Learning on Point Cloud. IEEE Workshop/Winter Conference on Applications of Computer Vision 2024. https://doi.org/10.1109/WACV61041.2025.00714
6. V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning. arXiv.org 2025. https://doi.org/10.48550/arXiv.2506.09985
7. LeJEPA: Provable and Scalable Self-Supervised Learning Without the Heuristics. arXiv.org 2025. https://doi.org/10.48550/arXiv.2511.08544
8. SiamJEPA: On the Role of Siamese Student Encoders in JEPA. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.04044
9. Var-JEPA: A Variational Formulation of the Joint-Embedding Predictive Architecture - Bridging Predictive and Generative Self-Supervised Learning.  2026. https://arxiv.org/abs/2603.20111v2
10. VJEPA: Variational Joint Embedding Predictive Architectures as Probabilistic World Models.  2026. https://arxiv.org/abs/2601.14354v1
11. BiJEPA: Bi-directional Joint Embedding Predictive Architecture for Symmetric Representation Learning.  2026. https://arxiv.org/abs/2603.00049v1
12. D-JEPA: A Decision-Aligned Latent World Model.  2026. https://arxiv.org/abs/2609.24749
13. A JEPA Recipe for Tabular Foundation Models.  2026. https://arxiv.org/abs/2609.25541
14. SANA-WM: Efficient Minute-Scale World Modeling with Hybrid Linear Diffusion Transformer. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.15178
15. Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture. Computer Vision and Pattern Recognition 2023. https://doi.org/10.1109/CVPR52729.2023.01499
16. Self-Distillation of Hidden Layers for Self-Supervised Representation Learning. arXiv.org 2026. https://doi.org/10.48550/arXiv.2603.15553
17. Emerging Properties in Self-Supervised Vision Transformers. IEEE International Conference on Computer Vision 2021. https://doi.org/10.1109/ICCV48922.2021.00951
18. Bootstrap Your Own Latent: A New Approach to Self-Supervised Learning. Neural Information Processing Systems 2020. https://arxiv.org/abs/2006.07733
19. Audio-JEPA: Joint-Embedding Predictive Architecture for Audio Representation Learning.  2025. https://arxiv.org/abs/2507.02915v1
20. MJEPA: A Simple and Scalable Joint-Embedding Predictive Architecture for Audio-Visual Learning. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.25225
21. DLLM-JEPA: Joint Embedding Predictive Architectures for Masked Diffusion Language Models.  2026. https://arxiv.org/abs/2606.00091v1
22. JEPA-DNA: Grounding Genomic Foundation Models through Joint-Embedding Predictive Architectures.  2026. https://arxiv.org/abs/2602.17162v3
23. JetParticle-JEPA: An Efficient Self-Supervised Representation Learning method for Jet Tagging in High-Energy Physics. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.14813
24. HEP-JEPA: A foundation model for collider physics using joint embedding predictive architecture. arXiv.org 2025. https://doi.org/10.48550/arXiv.2502.03933
25. Delineating the Effective Use of Self-Supervised Learning in Single-Cell Genomics. bioRxiv 2024. https://doi.org/10.1038/s42256-024-00934-3
26. A clinical benchmark of public self-supervised pathology foundation models.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58796-1
27. Computational Pathology at Health System Scale - Self-Supervised Foundation Models from Three Billion Images. arXiv.org 2023. https://doi.org/10.48550/arXiv.2310.07033
28. Revisiting Self-Supervised Visual Representation Learning. Computer Vision and Pattern Recognition 2019. https://doi.org/10.1109/CVPR.2019.00202
29. Scaling and Benchmarking Self-Supervised Visual Representation Learning. IEEE International Conference on Computer Vision 2019. https://doi.org/10.1109/ICCV.2019.00649
30. VideoMAE: Masked Autoencoders are Data-Efficient Learners for Self-Supervised Video Pre-Training. Neural Information Processing Systems 2022. https://doi.org/10.48550/arXiv.2203.12602
31. Self-Supervised Learning: Generative or Contrastive. IEEE Transactions on Knowledge and Data Engineering 2020. https://doi.org/10.1109/TKDE.2021.3090866
32. Masked Autoencoders Are Scalable Vision Learners. Computer Vision and Pattern Recognition 2021. https://doi.org/10.1109/CVPR52688.2022.01553
33. Masked Autoencoders that Listen. Neural Information Processing Systems 2022. https://doi.org/10.48550/arXiv.2207.06405
34. Masked Autoencoders for Point Cloud Self-supervised Learning. European Conference on Computer Vision 2022. https://doi.org/10.48550/arXiv.2203.06604
35. NeRF-MAE: Masked AutoEncoders for Self-Supervised 3D Representation Learning for Neural Radiance Fields. European Conference on Computer Vision 2024. https://doi.org/10.48550/arXiv.2404.01300
36. Masked particle modeling on sets: towards self-supervised high energy physics foundation models. Machine Learning: Science and Technology 2024. https://doi.org/10.1088/2632-2153/ad64a8
37. A Simple Framework for Contrastive Learning of Visual Representations. International Conference on Machine Learning 2020. https://arxiv.org/abs/2002.05709
38. Momentum Contrast for Unsupervised Visual Representation Learning. Computer Vision and Pattern Recognition 2019. https://doi.org/10.1109/cvpr42600.2020.00975
39. Graph Contrastive Learning with Augmentations. Neural Information Processing Systems 2020. https://arxiv.org/abs/2010.13902
40. LeVJEPA: Efficient&Scalable Video Pretraining without the Heuristics.  2026. https://arxiv.org/abs/2608.27395
41. Flow-JEPA: Flow Matching for Robust Latent Dynamics in JEPA World Models.  2026. https://arxiv.org/abs/2608.29029
42. Toward Physically Grounded JEPA World Models for Goal-Conditioned Robotic Planning.  2026. https://arxiv.org/abs/2609.03565
43. Back to Parsimonious Latents: Learning Task-Centric World Models from Visual Foundations. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.25620
44. GLAM: Training a latent world model over global spatiotemporal memory for active exploration and navigation.  2026. https://arxiv.org/abs/2609.14561
45. Unified World Models: Coupling Video and Action Diffusion for Pretraining on Large Robotic Datasets. Robotics 2025. https://doi.org/10.48550/arXiv.2504.02792
46. CLAW: Learning Continuous Latent Action World Models via Adversarial Latent Regularization. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.04130
47. Music-JEPA: Learning a World Model of Sound from Action. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.22000
48. Planning to Explore via Self-Supervised World Models. International Conference on Machine Learning 2020. https://arxiv.org/abs/2005.05960
49. Baba in Wonderland: Online Self-Supervised Dynamics Discovery for Executable World Models. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.16725
50. UniJEPA: A Unified Joint-Embedding Predictive Architecture for Task-Agnostic Visual World Modeling.  2026. https://arxiv.org/abs/2608.07409v1
51. DINO-WM: World Models on Pre-trained Visual Features enable Zero-shot Planning. International Conference on Machine Learning 2024. https://doi.org/10.48550/arXiv.2411.04983
52. MC-JEPA: A Joint-Embedding Predictive Architecture for Self-Supervised Learning of Motion and Content Features. arXiv.org 2023. https://doi.org/10.48550/arXiv.2307.12698
53. Graph-level Representation Learning with Joint-Embedding Predictive Architectures. Trans. Mach. Learn. Res. 2023. https://doi.org/10.48550/arXiv.2309.16014
54. Context Autoencoder for Self-supervised Representation Learning. International Journal of Computer Vision 2022. https://doi.org/10.1007/s11263-023-01852-4
55. Siamese Image Modeling for Self-Supervised Vision Representation Learning. Computer Vision and Pattern Recognition 2022. https://doi.org/10.1109/CVPR52729.2023.00212
56. Contrastive Masked Autoencoders are Stronger Vision Learners. IEEE Transactions on Pattern Analysis and Machine Intelligence 2022. https://doi.org/10.1109/TPAMI.2023.3336525
57. HuBERT: Self-Supervised Speech Representation Learning by Masked Prediction of Hidden Units. IEEE/ACM Transactions on Audio Speech and Language Processing 2021. https://doi.org/10.1109/taslp.2021.3122291
58. scRep: A Latent-Space Self-Distilled Foundation Model for Single-Cell Representation Learning. bioRxiv 2026. https://doi.org/10.64898/2026.08.31.747784
59. LaMamba-Diff: Linear-Time High-Fidelity Diffusion Models Based on Local Attention and Mamba. arXiv.org 2024. https://doi.org/10.48550/arXiv.2408.02615
60. Beyond Generative AI: World Models for Clinical Prediction, Counterfactuals, and Planning.  2025. https://arxiv.org/abs/2511.16333v1
61. RegFormer: a single-cell foundation model powered by gene regulatory hierarchies.. Nature communications 2026. https://doi.org/10.1038/s41467-026-72198-x
62. Mini-JEPA Foundation Model Fleet Enables Agentic Hydrologic Intelligence.  2026. https://arxiv.org/abs/2605.14120v1
63. T-JEPA: Augmentation-Free Self-Supervised Learning for Tabular Data.  2024. https://arxiv.org/abs/2410.05016v3
64. Sandwich-Residuals: Parameter-Efficient Test-time Adaptation of World Models.  2026. https://arxiv.org/abs/2609.21740
65. JEPA-Anything: Learning Predictive Models across Different Worlds.  2026. https://arxiv.org/abs/2609.20800
