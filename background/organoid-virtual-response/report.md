# 类器官与模式生物虚拟响应建模 · 方向背景报告

证据 67 篇 · 覆盖度 0.50 · 第 9 轮 · 更新 2026-10-25 · 数字核验删句 1

## 本次变更

- 新增 [51] Emerging frontiers for AI in single-cell genomics.
- 新增 [11] Genetic Perturbation Prediction Models Fail Out-of-Distribution: A Rigorous Benchmark and Systematic Evaluation
- 新增 [38] Deep dynamical models of single-cell multiomic velocities predict loss-of-function and rescue perturbations in B cells.

## 摘要（TL;DR）

- OSCAR 在类器官中以调控网络活性为读出做单细胞 CRISPR 筛选，鉴定出 c-Fos 扰动加速肝细胞分化成熟、Ubr5 缺失起相反作用 [1]。
- Perturb-FISH 将 MERFISH 与 gRNA 原位扩增结合，在 THP1 巨噬细胞 LPS 响应体系中验证敲除效应与 Perturb-seq 一致，并揭示细胞密度和邻居扰动对基因回路的影响 [2]。
- 宫颈方向把单细胞转录组、CRISPR-Cas9 筛选与类器官建模整合，NF1 被鉴定为 HPV 阳性前瘤类器官中恶性转化的首要抑制因子，其缺失将 5~10 年癌变压缩至 3~6 个月 [3]。
- 局部晚期直肠癌类器官活体生物库的共临床试验显示化放疗反应预测准确率 84.43%、灵敏度 78.01%、特异性 91.97% [4]。
- Trellis 用高多重质谱流式在单细胞水平检测 >2500 个 CRC 类器官与 CAF 的 PTM 信号、DNA 损伤、细胞周期与凋亡，发现凋亡罕见且患者特异，CAF 可通过促进 proCSC 向 revCSC 转变保护癌细胞抵抗化疗 [5]。
- DiRL 把分化建模为目标条件序列决策问题，在 iPSC 来源类器官数据上训练智能体导航基因表达潜空间，对随机扰动胜率 69%，但真实生物验证有限 [6]。
- 结直肠癌类器官研究用图像 profiling 分析 31360 张明场图，结合目标检测与深度生成模型预测凋亡强度与真值相关 0.91 [7]。
- 胃癌类器官用 AFM 纳米机械振动检测，pM 级紫杉醇即可检出振动变化、早于形态改变，CNN 分类准确率 97%，但依赖 AFM 设备、通量有限 [8]。
- 一项评估将 TabICL 和 TabPFN 与 PRESAGE、scGPT、scLAMBDA、STACK、Prophet 等专用架构比较，结果显示表格基础模型在伪bulk扰动预测上持续优于专用基线，但作者也指出专用模型在部分任务仍可能更优 [9]。
- 系统综述与荟萃分析显示在 411 对患者-模型配对（267 PDX、144 PDO）中，患者与匹配模型的总体治疗反应一致率为 70%，PDX 与 PDO 之间无显著差异，作者强调需更多前瞻性研究才能给出确定性推荐 [10]。
- EL-PERTURB 采用分层分布外（OOD）划分，在必需基因和全基因组 Perturb-seq 筛选数据上压力测试 6 类架构的 20 个扰动预测模型，结论是现有基准多依赖随机划分而掩盖系统性失效模式，模型在真实 OOD 条件下泛化失败 [11]。

## 1 背景与定义

类器官与模式生物虚拟响应建模的边界，首先由“扰动—读出—预测”三要素共同划定。**只做类器官构建或培养方案优化、没有扰动施加与建模成分的工作不在本方向内**，纯细胞系扰动预测则归入虚拟细胞方向；本方向要求扰动实验（药物、遗传、环境）与单细胞/空间/影像/表型读出同时在场，并至少包含预测或建模环节。综述层面提出的**人工智能虚拟类器官（AIVOs）**把这一边界进一步明确为“在计算空间中实例化的类器官尺度数字孪生”，以虚拟细胞乃至虚拟类器官为最小可执行单元，融合多模态与纵向测量为通用状态表征，并用受生物物理先验约束的虚拟仪器模拟检测 [12]。该框架以**数据层—模型层—交互层**为主线，与物理类器官及临床决策形成闭环耦合，其对照对象包括传统类器官、AIVC 与器官数字孪生 [12]。**这意味着本方向的“虚拟响应”不是单纯的预测模型，而是与湿实验体系互为参照、可被实验检验的计算对象**；综述同时列出类器官对 Matrigel 的依赖、批次差异大、手动操作、终点测量与可扩展性问题作为建模动因 [12]。

从演化脉络看，本方向经历了从“终点药敏”到“单细胞/空间扰动读出”、再到“跨体系表征迁移”的三级跳。早期工作以患者来源类器官（PDO）的药敏与临床反应对应为核心，系统综述纳入 17 项肿瘤学研究，指出 PDO 有潜力预测治疗反应，但需同时满足**分析效度、临床效度和临床效用**，建立率与周转时间仍影响临床落地 [13]。随后，读出维度从批量活力终点扩展到单细胞与空间：**OSCAR** 在 3D 类器官中以调控网络活性为读出做单细胞 CRISPR 筛选 [1]，**Perturb-FISH** 将 MERFISH 与 gRNA 原位扩增结合实现扰动与转录组的空间联合读取 [2]，人胃肿瘤类器官则建立切割、CRISPRi、CRISPRa 与单细胞筛选的全套体系 [14]。第三阶段是把类器官、模式生物与跨物种图谱纳入统一表征：GeneCompass 在 **1.017 亿人/鼠单细胞**上预训练并注入四类先验知识 [15]，SATURN 以蛋白语言模型嵌入绕开一对一同源限制 [16]，LucaCell 进一步放弃固定基因 ID 词表、改用 mRNA 序列嵌入 [17]。**这条脉络的核心变化是：扰动响应的建模单位从“一个类器官一个终点”变为“一个细胞状态一个可迁移表征”**。

模式生物在本方向中的角色，与类器官并不对称。类器官提供人源细胞与组织的可控扰动平台，模式生物则提供在体多器官、剂量/时间响应与表型预测的参照系：跨物种细胞景观整合小鼠、斑马鱼、果蝇等多生命阶段**超 260 万单细胞**并汇入 15 物种公开数据 [18]；小脑研究构建猕猴、狨猴与小鼠小脑皮层单细胞空间转录组图谱，发现区域选择性表达在灵长类主要位于颗粒层、小鼠位于 Purkinje 层 [19]；动脉粥样硬化研究整合人多阶段斑块数据与多时间点小鼠模型，鉴定富集于不稳定病变的 PIM 单核细胞群并衍生 **362 基因血液特征** [20]。**类器官与模式生物因此构成互补的两端：前者长于人源扰动与药敏，后者长于在体时序、多器官与表型终点，而虚拟响应建模的价值恰在于把两端接到同一表征空间** [12][18]。

跨物种迁移到人，是本方向定义中最具张力的一环，其技术分歧集中在“基因身份是否可通约”。第一条路线直接学习控制态到扰动态的映射：CellOT 用神经最优传输从非时间分辨的未配对单细胞数据学习扰动响应，并在**跨物种 LPS 响应**任务上验证 [21]；Speciesformer 则以跨物种生成式虚拟细胞建模为目标，在含 **1.31 亿细胞**的 SpeciesCorpus 上预训练 [22]。第二条路线处理同源映射：CAME 保留同源基因映射，用半监督异构图神经网络支持一对多/多对多同源关系，在 **649 对**跨物种数据集上优于六种基准方法 [23]；SATURN 与 LucaCell 则以蛋白/核酸序列层面表征绕开一对一同源限制 [16][17]。**分歧的实质是：跨物种迁移的可靠性上限，究竟由同源映射质量决定，还是可由序列级表征部分绕过**；CAME 明确受同源映射质量与测序深度不一致影响 [23]，而序列中心路线尚未在扰动响应预测上给出与同源路线可比的系统证据 [17]。

类器官药敏与患者结局对应，是本方向临床落点的核心问题，其争议不在“是否相关”而在“相关性的强度与适用边界”。荟萃分析在 411 对患者-模型配对（267 PDX、144 PDO）中给出患者与匹配模型的**总体治疗反应一致率 70%**，PDX 与 PDO 之间无显著差异，作者认为两者在转化研究中互补并强调需更多前瞻性研究 [10]；单癌种研究则常报告更高指标，如局部晚期直肠癌类器官化放疗反应预测**准确率 84.43%** [4]，转移性结直肠癌 PDO 对伊立替康为基础治疗的活检病灶反应**预测准确率超过 80%** [24]。**这些数字因人群、终点与验证设计不同不宜直接比高低**；更值得关注的是预测性能对模型来源的依赖：卵巢癌 191 个类器官的多模态 AI 模型显示**原发肿瘤来源预测准确性最高、转移灶次之、腹水来源较低** [25]，胶质母细胞瘤 GBO-DST 则报告**比 MGMT 启动子甲基化状态更准确预测 TMZ 个体反应** [26]。心脏方向作为优先领域，成熟方案使 **TNNI3** 比例达 **18%**（约 **20 周**胎儿心脏水平）并用于复杂疾病建模与药物测试 [27]，但成年心脏特性仍未完全实现，**心血管类器官的药敏-临床对应证据强度明显弱于肿瘤类器官**。

数据资源与评测构成了本方向的“基础设施层”，也暴露出当前最尖锐的方法学争议。资源侧已出现多类规模化语料：Nicheformer 的 SpatialCorpus-110M 涵盖**超 1.1 亿细胞、5383 万空间细胞、73 组织** [28]，BrainBeacon 基于 **1.33 亿空间分辨细胞**、四物种五平台 [29]，UCE 构建含 **3600 万细胞、1000+ 细胞类型、8 物种**的图谱 [30]，类器官空间转录组方面则有 Stereo-seq 系统基准数据 [31]。评测侧的结论却趋于保守：统一基准测试 **Nicheformer、CellPLM、scGPT-spatial、GenePT、scELMo、Novae** 六个模型后发现无模型全面占优，排名随模态、预处理、token 化、生物先验、域偏移与指标选择而变 [32]；VCBench 在五个可测维度上评测 **Geneformer、scGPT、UCE、TranscriptFormer、Arc State** 及线性/KNN 基线，发现基线在其中 **4 个**维度匹配或超越所有基础模型 [33]；EL-PERTURB 采用分层分布外划分压力测试 **6 类架构的 20 个**扰动预测模型，结论是随机划分掩盖了系统性失效模式 [11]。**三者共同指向的判断是：本方向尚不存在可跨任务复用的“最优模型”，评测结论高度依赖划分策略与指标设计**；而通用表格基础模型在伪 bulk 扰动预测上持续优于专用基线的结果 [9]，进一步说明“通用优于专用”同样不是普适结论。

综合上述，本方向的核心问题可归纳为三层。**第一层是表征层**：如何在基因身份不可通约、测序深度不一致、物种与平台异质的条件下，建立可迁移的细胞状态表征 [16][23][17]。**第二层是因果层**：如何从观察性、非时间分辨、含混杂的扰动数据中识别扰动效应，CINEMA-OT 的独立性与线性假设、CellOT 的未配对数据假设都是这一层的明确边界 [34][21]。**第三层是转化层**：类器官药敏与患者结局的对应强度如何在不同癌种、取材部位与终点定义下被稳定估计，以及心血管等非肿瘤类器官能否建立可比的验证链条 [10][25][27]。**三层之间的耦合尚不充分——表征层的跨物种模型很少在类器官药敏-临床对应任务上被直接检验，转化层的前瞻性队列也很少报告其所用表征与评测划分**，这正是本方向从“各自成立”走向“可比较、可复现”的关键缺口 [32][11]。

## 2 方法学


### 2.1 类器官与器官芯片扰动建模

类器官扰动建模的第一条主线是把 CRISPR 筛选搬进 3D 类器官，并以单细胞或空间读出替代传统的批量活力终点。**OSCAR** 在类器官中以调控网络活性为读出做单细胞 CRISPR 筛选，针对转录因子低表达、噪声与 dropout 难以准确估计的问题，鉴定出 **c-Fos** 扰动加速肝细胞分化成熟、**Ubr5** 缺失起相反作用，并按调控效应排序 [1]。与之互补，**Perturb-FISH** 将 MERFISH 与 gRNA 原位扩增结合，在 THP1 巨噬细胞 LPS 响应体系中验证敲除效应与 Perturb-seq 一致，并揭示细胞密度和邻居扰动对基因回路的影响，进一步在肿瘤异种移植 3D 组织中展示适用性 [2]。两者差异在于读出维度：前者读调控网络，后者读空间转录组与原位扰动身份；共同局限是低丰度转录本估计与 gRNA 原位扩增的技术约束 [1][2]。

在筛选通量与筛选模态上，人胃肿瘤类器官已建立切割、CRISPRi、CRISPRa 与单细胞筛选的全套体系，在 TP53/APC 双敲类器官中筛选顺铂基因-药物互作，发现 DNA 修复通路转录组趋同、蛋白岩藻糖化与顺铂敏感性关联及 **TAF6L** 在 DNA 损伤恢复期增殖中的作用 [14]。宫颈方向则把单细胞转录组、CRISPR-Cas9 筛选与类器官建模整合，**NF1** 被鉴定为 HPV 阳性前瘤类器官中恶性转化的首要抑制因子，其缺失将 **5~10 年**癌变压缩至 **3~6 个月**，NF1 恢复诱导凋亡，AI 设计的 NF1 模拟肽可降低肿瘤负荷 [3]。两项工作都强调类器官相较 2D 细胞系的生理相关性，但前者基于单一工程化模型、后者全文未获取，结论的普适性尚待验证 [14][3]。

药敏预测的临床验证是另一条主线。局部晚期直肠癌类器官活体生物库来自接受新辅助化放疗的 III 期临床试验患者，共临床试验显示类器官重现肿瘤病理生理与遗传变化，化放疗反应预测**准确率 84.43%、灵敏度 78.01%、特异性 91.97%** [4]。头颈鳞癌方面，**TransferNet-PDO** 基于 Hover-Net 架构与 ResNet50 骨干的单细胞 CNN 分类器结合 H&E 与全外显子测序，可区分肿瘤与正常类器官、保留含低频亚克隆的克隆结构，并对顺铂、西妥昔单抗、仑伐替尼、放疗及放化疗显示临床相关敏感性 [35]。后者同时指出 HNSCC 类器官模型仍不成熟：正常上皮或基质细胞过度生长、肿瘤异质性与克隆性难以跨传代保持、新鲜手术标本获取受限 [35]；这与直肠癌队列的较高预测指标并不构成直接可比，因为两者人群、终点与验证设计不同 [4]。

微环境与细胞类型分辨的扰动读出，弥补了批量药敏只给单一终点的不足。**Trellis** 用高多重质谱流式在单细胞水平检测 **>2500 个** CRC 类器官与 CAF 的 PTM 信号、DNA 损伤、细胞周期与凋亡，发现靶向细胞周期阻断和 DNA 损伤效应常见，而凋亡罕见且患者特异，CAF 可通过促进 proCSC 向 revCSC 转变保护癌细胞抵抗化疗 [5]；其预印本版本方法与 Cell 论文一致，但未提供具体数据规模与定量结果 [36]。另一条路径把急性切片培养与 microwell scRNA-seq 结合，在 **7 例** GBM 标本的 **500 μm** 切片上于 **24 小时**内完成多药扰动，去卷积出细胞类型特异药物反应并保留肿瘤微环境与异质性 [37]。两者都强调微环境细胞对药效的调节，但一为类器官-基质共培养、一为原组织切片，短期培养能否反映长期治疗反应仍是共同疑问 [5][37]。

单细胞扰动效应的因果与动态建模，为类器官筛选提供了统计与生成式工具。**CINEMA-OT** 用独立成分分析与加权最优传输分离混杂与处理相关变异、进行因果细胞配对，在模拟和真实数据中优于现有方法，并用于气道类器官病毒感染/烟雾及 PBMC 细胞因子组合刺激分析，其局限是依赖独立性与线性假设 [34]。**DiRL** 把分化建模为目标条件序列决策问题，在 iPSC 来源类器官数据上训练智能体导航基因表达潜空间，对随机扰动**胜率 69%**，恢复 Wnt 与 Hedgehog 通路顺序调控因子，价值函数重现伪时间排序，但真实生物验证有限 [6]。**DynaVelo** 则以生成式神经常微分方程从单细胞多组学学习表达与 TF motif 活性联合动态，重现野生型小鼠生发中心 B 细胞体内分叉动态，并揭示 Arid1a 与 Ctcf 杂合缺失下的动态变化 [38]。三者的共同取向是"计算机扰动"替代部分湿实验，但验证深度不一，DiRL 与 DynaVelo 的生物学确证仍有限 [6][38]。

图像与形态表型正在成为扰动读出的低成本替代。结直肠癌类器官研究用图像 profiling 分析 **31360 张**明场图，识别囊性与实性两亚型，囊性活性更高，结合目标检测与深度生成模型预测凋亡强度与真值相关 **0.91**，并用 scRNA-seq 验证细胞异质性 [7]。**SCOPE** 整合 AI 图像活力分析与生长追踪数学建模，提出 **GV 评分**与 **CCTR** 两指标，把药物反应分为细胞毒、细胞静止加细胞毒、延迟细胞毒、细胞静止四类 [39]。PDO 延时显微视频方面，SAM 分割与 DI-NOv2 结合注意力 MIL 预测 ATP 活力，优于非时间分辨方法 [40]。这些工作共享"以形态/延时影像推断功能"的思路，但泛化性与临床验证普遍不足 [7][40]。

几何、力学与电生理等物理读出扩展了扰动响应的维度。心脏类器官库用微图案化生成 **230 个**类器官、**7 种**几何设计，采集收缩运动与钙瞬变 **10 项**变量，结合流形学习与集成学习识别形状决定生理属性并降低异质性，局限是仅分化第 **20 天**、未验证长期功能 [41]。胃癌类器官则用 AFM 纳米机械振动检测，**pM 级**紫杉醇即可检出振动变化、早于形态改变，CNN 分类准确率 **97%**，但依赖 AFM 设备、通量有限 [8]。**LWD-Miniscope** 改造长工作距离微型荧光显微镜与 heart-on-a-chip 整合，在芯片上以 **228 lp/mm@60 帧/秒**的分辨率成像人心脏类器官钙瞬变，以替代劳动密集、低通量的 MEA 与膜片钳 [42]。三者分别代表形态几何、力学振动与光学电生理三条物理读出路线，通量与设备依赖是共同瓶颈 [41][8][42]。

高通量与动态组合扰动平台解决的是"如何稳定地施加扰动"。自动化微流控系统兼容 Matrigel，对数百个培养物提供组合与动态药物处理并实时分析，支持长期培养、程序化刺激与实时监测，降低试剂与人工消耗，但系统复杂性与通量仍受凝胶和微流控限制 [43]。微流控单细胞来源肿瘤类器官（STO）阵列用亲水涂层微孔随机捕获单细胞、藻酸-壳聚糖膜包裹原位培养数千 STO，识别耐药亚群及差异表达基因，候选药经 STO 阵列再验证有效，通量与标准化仍受限 [44]。两者都指向"单细胞来源 + 阵列化"以提高异质性分辨，但前者重动态组合给药、后者重克隆溯源 [43][44]。

空间转录组与多重化策略为类器官扰动提供群体尺度与区域尺度的读出基础。**Stereo-seq** 被系统用于脑、心肌、心瓣膜、肾、肺、软骨、造血等多类干细胞来源类器官，优化芯片包被与通透、评估 UMI/基因捕获，并指出 RNA 捕获效率低于参考组织、造血与悬浮肾类器官存在转录扩散导致单细胞注释困难 [45][31]。皮层脑类器官方面，比较了类器官生成时混合细胞系的 mosaic 策略与单细胞建库前混合的下游策略，并开发 **SCanSNP** 去卷积进行基因型识别，在 **50/100/300 天**时间点上重建神经发育轨迹并关联遗传变异与轨迹表型，局限是成本与工作量大、批次间变异 [46]。神经类器官的形态发生素多重单细胞筛选进一步显示，形态发生素的时序、浓度与组合显著决定区域组成，且细胞系与神经诱导方法影响响应 [47]。这些工作共同把"扰动"从单基因敲除扩展到微环境梯度与遗传背景多重化 [46][47]。

疾病建模与药物发现的应用侧，出现了以类器官表型为起点的深度学习筛选。Leigh 综合征研究基于脑类器官 scRNA-seq 建立细胞类型特异药物重定位算法，并在 ΔSHY 酵母中筛选 **2250 种** FDA 药物，两条路线独立收敛于唑类化合物，**sertaconazole** 与 **talarozole** 促进神经定向并挽救中脑类器官异常生长率与乳酸释放 [48]。心脏成熟方面，短暂激活 AMPK 与 ERR 的定向成熟方案使 **TNNI3** 比例达 **18%**（约 **20 周**胎儿心脏水平），DM-hCOs 可建模复杂疾病并用于药物测试，但成年心脏特性仍未完全实现 [27]。多组学嵌入方面，**135 个** CRC/PDAC PDO 的 WES、RNA-seq 与药敏数据被用于训练模型预测药物 AUC，并在嵌入空间识别 KRAS 抑制剂敏感或耐药富集的分子邻域 [49]。这些应用显示类器官正从"药敏测试"走向"扰动响应预测"，但临床转化价值均需系统验证 [48][49]。

最后，视网膜类器官的发育结局预测提示异质性本身可以被建模为可预测变量。研究采集 **988 个**类器官、**117249 张**明场延时图像，结合专家注释训练深度学习模型，在 RPE 与晶状体组织可见出现前很早期准确预测其发生与大小及整体形态相似性，并明确组织结局决定时间窗，局限是监督学习需大量高质量标注数据集 [50]。这与前述图像表型工作形成呼应：类器官的形态异质性既是噪声来源，也是可被学习、可用于扰动归因的信号 [7][50]。综述层面则指出，早期 scRNA-seq 嵌入模型与基础模型在实验生物学家中应用有限，但随着大规模单细胞图谱积累，利用 AI 在庞大数据背景下解读新数据集的需求已明确，单细胞表观/多组学检测与 Perturb-seq 带来新的建模机会 [51]。

### 2.2 模式生物扰动响应模型

在细胞扰动响应预测方向，通用表格基础模型与领域专用模型的相对优势仍存争议。一项评估将 **TabICL** 和 **TabPFN** 与 PRESAGE、scGPT、scLAMBDA、STACK、Prophet 等专用架构在四个互补设置中比较，覆盖五个 Perturb-seq 数据集、CD4+ T 全基因组 CRISPR 与斑马鱼图谱；结果显示表格基础模型在细胞水平跨类型预测持平或更优，在**伪bulk扰动预测**上持续优于专用基线，在胚胎组成预测中具竞争力，但作者也指出专用模型在部分任务仍可能更优 [9]。这一结论的边界在于评估尚未覆盖所有生物尺度，提示“通用优于专用”并非普适判断 [9]。

在模式生物与跨物种框架方面，两项工作侧重不同子问题。动脉粥样硬化研究整合人晚期稳定与不稳定斑块单细胞数据及多时间点小鼠模型，鉴定富集于不稳定病变的 **PIM 单核细胞群**，并从其转录组衍生 **362 基因血液特征**，再用可解释深度学习筛选 20 基因 panel 区分不稳定与稳定病例 [20]；但该证据 AUC 数值不完整、临床验证规模未明，预测性能尚难与其他工作直接比较 [20]。小脑研究则构建猕猴、狨猴与小鼠小脑皮层单细胞空间转录组图谱，发现灵长类特异 Purkinje 细胞和分子层中间神经元亚型及 **GRID2** 表达差异，区域选择性表达在灵长类主要位于颗粒层、小鼠位于 Purkinje 层，且基因表达梯度与清醒 fMRI 功能连接梯度匹配 [19]。前者面向疾病事件预测建模，后者提供跨物种空间图谱与功能组织参照，二者在“虚拟响应”上的可比性有限，且均缺乏全文层面的功能验证细节 [20][19]。

### 2.3 跨物种迁移

跨物种迁移的第一条技术路线是把控制态与扰动态之间的映射直接学出来。CellOT 用神经最优传输，从非时间分辨的未配对单细胞数据中学习控制态到扰动态的映射，在黑色素瘤药物响应、狼疮与胶质瘤患者活检、**跨物种 LPS 响应**及造血命运演化任务上优于线性潜空间位移类方法 [21]。其限制在于依赖未配对数据假设，且需捕获训练队列的异质性才能泛化到新患者 [21]。与之不同，Speciesformer 把目标定为跨物种**生成式虚拟细胞建模**，在含 **1.31 亿细胞**的 SpeciesCorpus 上预训练，学习可迁移的细胞状态与状态转变，并明确要区分保守生物学原理与物种、组织及细胞环境特异变异 [22]。两者都指向跨物种扰动/状态预测，但前者以最优传输映射为核心、在具体扰动任务上验证，后者以大规模预训练加生成为核心，摘要层面尚未给出下游任务数字 [21][22]。

第二条路线解决的是"基因身份不可通约"这一前置障碍。SATURN 用蛋白语言模型嵌入编码基因生物学性质，与 RNA 表达耦合，引入宏基因把功能相关基因映射到联合低维空间，在人、小鼠、狐猴等跨物种图谱上实现远缘物种注释迁移，数据规模为哺乳动物 **335,000 细胞、9 组织**，另含蛙与斑马鱼胚胎 [16]。LucaCell 走得更彻底，放弃固定基因 ID 词表，改用预训练 mRNA 序列嵌入表示基因、表达离散分箱后以 Transformer 编码，在 **8500 万人/鼠单细胞**上预训练，实现无手动映射的跨物种注释，并扩展到染色质、50+ 原核与 5 株流感病毒载量预测 [17]。CAME 则保留同源基因映射，用半监督异构图神经网络把参考与查询物种的表达矩阵及同源映射编码为异质细胞-基因图，支持一对多/多对多同源关系并提取基因模块，在 **649 对**跨物种数据集上优于六种基准方法 [23]。三者的分歧点在于是否依赖同源基因：CAME 明确受同源映射质量与测序深度不一致影响 [23]，SATURN 与 LucaCell 则以蛋白/核酸序列层面的表征绕开一对一同源限制 [16][17]。

第三条路线是通用表征与基础模型，其跨物种能力多以整合规模与注释迁移来度量。UCE 完全自监督训练于人及多物种细胞图谱，构建含 **3600 万细胞、1000+ 细胞类型、8 物种**的 Integrated Mega-scale Atlas，新细胞无需再训练或微调即可映射 [30]。GeneCompass 在 scCompass-126M 的 **1.017 亿人/鼠单细胞**上预训练并注入启动子、GRN、基因家族、共表达四类先验，微调后在细胞注释、扰动预测、剂量响应与 GRN 推断上达到或接近 SOTA，但主要限于人和鼠 [15]。Nicheformer 把空间背景纳入表征，在 **超 1.1 亿细胞、5383 万空间细胞、73 组织**的人鼠数据上预训练，在空间依赖任务上系统性优于 Geneformer、scGPT、UCE、CellPLM 等，并能把空间背景迁移至解离 scRNA-seq 数据 [28]。BrainBeacon 专注脑空间转录组，基于 **1.33 亿空间分辨细胞**、人/猕猴/狨猴/小鼠四物种五平台，实现跨物种脑细胞类型与解剖区域对齐 [29]。这些工作报告的规模数字来自不同语料与统计口径，不宜直接横向比高低；可比较的是同一研究内部的对照，如 Nicheformer 相对所列基础模型的优势 [28]。此外，Nicheformer 摘要亦指出独立基准结果未完全复现，这构成对基础模型跨任务优越性的争议点 [28]。

第四条路线以图谱构建和特定细胞类型为载体，检验"保守与分歧"的具体内容。跨物种细胞景观整合小鼠、斑马鱼、果蝇等多生命阶段 **超 260 万单细胞**并汇入 15 物种公开数据，发现结构炎症与线粒体功能障碍为衰老常见标志，激活线粒体代谢可缓解小鼠衰老表型 [18]。小胶质细胞图谱整合 **>20 万**人鼠细胞与空间数据，识别稳态、干扰素响应、吞噬/激活等保守亚型，并发现高表达 APOE、TREM2、GPNMB 的保守 LAM 状态 [52]。在模型侧，mouse-Geneformer 基于 **1089 个数据集、过滤前 1.19 亿细胞**构建 mouse-Genecorpus-20M，评估细胞类型分类与 in silico 扰动并探索跨物种应用，但其仅用健康野生型小鼠数据，跨物种效用尚需进一步验证 [53]。这些证据共同表明，跨物种迁移的落点正从"能否对齐"转向"哪些状态真正保守"，而保守性结论目前仍高度依赖所选的物种组合与细胞类型 [18][52]。

### 2.4 虚拟组织与数字孪生建模

类器官平台受批次差异、纵向读数稀疏和规模化障碍限制，这构成了虚拟建模的出发点。综述提出**人工智能虚拟类器官（AIVOs）**，亦称硅基类器官，即在计算空间中实例化的类器官尺度数字孪生，以虚拟细胞乃至虚拟类器官作为最小可执行单元；其融合多模态与纵向测量为通用状态表征，并用受生物物理先验约束的虚拟仪器模拟检测 [12]。在方法上，该框架以**数据层—模型层—交互层**为主线，综合多模态组学、高内涵成像与空间 profiling 等文献，并与物理类器官及临床决策形成闭环耦合 [12]。

该综述将虚拟干细胞、功能细胞和肿瘤细胞定位为可复用基元，用于连接单细胞表征与类器官乃至患者尺度模拟，其对照对象包括传统类器官、AIVC 与器官数字孪生 [12]。所列举的限制包括类器官对 Matrigel 的依赖、批次差异大、手动操作、终点测量以及伦理成本与可扩展性问题 [12]。证据为综述性综合，未提供同一研究内部的定量对照，故不同平台间的性能高低无法据此判断。

## 3 数据资源与基准

在类器官虚拟响应建模的基准构建上，该研究采用**单细胞图谱基准评估脑类器官**的方法，构建了覆盖人海马发育过程的**连续发育人海马单细胞图谱**，并以此作为基准评估家族性阿尔茨海默病（fAD）脑类器官 [54]。其核心思路是用连续发育海马图谱校准 fAD 类器官中神经发育相关扰动，从而应对 iPSC 来源脑类器官在区域身份、成熟状态和细胞组成上的异质性 [54]。

该工作强调，fAD 突变对早期海马发育过程的影响需要在统一发育参照下解读 [54]。这一结论也提示，类器官响应建模的基准需与发育参照对齐，而非仅依赖单一终点的类器官读数 [54]。

## 4 与临床响应的对应

在临床响应预测这一目标下，患者来源类器官（PDO）的证据已从回顾性相关性走向前瞻性对照，但不同癌种、不同研究设计给出的验证强度差异明显。系统综述层面，一项纳入17项肿瘤学研究的分析指出PDO有潜力预测治疗反应，但需同时满足**分析效度、临床效度和临床效用**，且建立率与周转时间仍影响临床落地[13]。更严格的比较来自一项系统综述与荟萃分析：在411对患者-模型配对（267 PDX、144 PDO）中，患者与匹配模型的**总体治疗反应一致率为70%**，PDX与PDO之间无显著差异，敏感性、特异性及预测值相当；PDO应答者无进展生存延长，而PDX的这一关联仅在低偏倚风险配对中成立，作者因此认为两者在转化研究中互补，并强调需更多前瞻性研究才能给出确定性推荐[10]。

前瞻性验证集中在胃肠道肿瘤。在转移性结直肠癌中，PDO测试对伊立替康为基础治疗的活检病灶反应**预测准确率超过80%**，且未误分类不应治疗的患者[24]。结直肠癌肝转移方面，一项前瞻性观察研究以30例患者建立39个类器官，将体外药敏与指南推荐治疗的客观反应一致性作为主要终点，涵盖化疗与靶向药物，但样本量与随访时间有限[55]。胃癌研究从73例组织建成57个类器官（**成功率78%**），类器官保留原发肿瘤组织学特征，高增殖类器官富集REG4、KLF4、ERBB3、HRAS、NOTCH1、MYC，并借助PDOX模型与患者实际治疗反应进行验证[56]。更早的转移性胃肠癌工作则构建了来自I/II期临床试验患者的活体类器官生物库，将类器官药敏与患者实际临床试验反应对比，发现类器官分子谱与原肿瘤高度相似，可补充现有方法定义治疗反应，但样本来自重度预处理患者且未明确前瞻性验证[57]。

妇科肿瘤方面的证据在“能否重现临床反应”上较为一致，但对预测标志物的比较结果存在张力。卵巢癌中，23例患者的36个全基因组特征PDO保留了原肿瘤基因组特征，并重现患者对新辅助卡铂/紫杉醇的临床反应，**88%患者对至少一种药物高响应**，患者间与患者内异质性可部分由遗传变异解释[58]。另一项研究建立21例初治晚期上皮性卵巢癌类器官，其组织病理、分子特征与突变谱与亲本肿瘤一致，但作者明确指出其药敏检测指导个体化治疗的临床应用仍待确定[59]。规模更大的一项工作构建191个卵巢癌类器官（来自123例患者），结合随访与多模态组学AI模型，发现**原发肿瘤来源类器官预测准确性最高，转移灶次之，腹水来源较低**[25]。高级别浆液性卵巢癌的纵向平台则聚焦长期培养后药敏稳定性，作者承认该稳定性仍需进一步验证[60]。

中枢神经系统肿瘤的证据突出“优于传统分子标志物”这一比较。胶质母细胞瘤研究从55例患者建立59份GBO，GBO-DST与无进展生存强相关，且**比MGMT启动子甲基化状态更准确预测TMZ个体反应**；同时筛选4种FDA批准抗癌药，发现第三代EGFR抑制剂lazertinib可抑制GBO生长与存活并在体内移植模型验证，但作者强调仍需在结构良好的临床队列中广泛验证[26]。脑肿瘤IPTO系统将患者肿瘤外植体培养于iPSC来源脑类器官中，覆盖成人、儿童与转移性肿瘤，多组学证明其保留原肿瘤细胞异质性与分子特征，并在前瞻性队列中预测患者特异药物响应及耐药机制[61]。

其他癌种与建模方法提供了补充但强度不一的证据。胰腺癌30例PDO经WGS、RNA-seq与组织学表征，测试76种药物，发现临床未利用的敏感性，并验证PRMT5抑制剂EZP015556对MTAP阴性及部分阳性肿瘤有效，作者指出体外药敏与临床相关性需进一步验证[62]。乳腺癌研究以40个类器官结合I-SPY2临床试验数据构建仅用类器官可检测生物标志物的预测模型，并对26个类器官行386化合物10剂量筛选，耐药模型筛出的方案在亚型匹配患者中显示生存获益，但样本量有限[63]。骨肉瘤23份样本的PDO可预测新辅助化疗反应与长期生存，但作者列出肉瘤3D培养启动困难、化疗后残留肿瘤增殖能力低、缺乏验证的功能性指标等限制[64]。方法学上，肺癌CODRP整合AUC、类器官生长率与癌症分期，在PFS预后分析中优于传统AUC方法，但样本规模未明确[65]；PharmaFormer以自定义Transformer加迁移学习、用类器官药敏数据微调后在TCGA队列预测临床反应，显著优于SVR、MLP、RF、KNN和Ridge，但受限于类器官药物基因组数据有限[66]。

综合来看，争议不在“类器官能否相关于临床”，而在相关性的强度与适用边界：荟萃分析显示PDO与PDX总体一致率相当、均为70%[10]，而单癌种研究常报告更高的预测准确率（如结直肠癌>80%[24]），二者因研究设计与对照不同不宜直接比高低。同样，GBO优于MGMT[26]与卵巢癌类器官预测力随取材部位下降[25]提示预测性能高度依赖模型来源与终点定义；而多项研究一致将前瞻性、大样本验证列为尚未完成的前提[13][10][26]。

## 5 评测、可复现性与争议

评测方法本身正在成为争议焦点。统一框架对 **Nicheformer、CellPLM、scGPT-spatial、GenePT、scELMo、Novae** 六个单细胞/空间基础模型的基准测试显示，无模型全面占优，排名随模态、预处理、token化、生物先验、域偏移和指标选择而变，模型对域偏移脆弱且可解释性有限 [32]。VCBench 则把四个虚拟细胞框架整合为七个能力维度，在五个可测维度上评测 **Geneformer、scGPT、UCE、TranscriptFormer、Arc State** 及预注册线性/KNN 基线，发现基线在其中 **4 个**维度匹配或超越所有基础模型，仅 TranscriptFormer 在跨模态 RNA-蛋白预测上 Pearson 提升 **53%**；同时多尺度整合与 in silico 实验无法端到端测试，跨模态结果存在污染警告 [33]。两项工作都指向同一问题：评测结论高度依赖维度与指标设计，单一任务基准会掩盖模型相对简单基线的真实位置。

泛化失败与划分策略的争议在扰动预测上更直接。EL-PERTURB 采用分层分布外（OOD）划分，在必需基因和全基因组 Perturb-seq 筛选数据上压力测试 **6 类架构的 20 个**扰动预测模型，结论是现有基准多依赖随机划分而掩盖系统性失效模式，模型在真实 OOD 条件下泛化失败 [11]。这与前述基准中「排名随域偏移变化」的观察相互呼应，但冲突在于：统一框架与 VCBench 仍以多维度综合排名呈现模型能力，而 EL-PERTURB 主张随机划分下的成绩不能代表分布外泛化，评测应显式区分划分策略。可复现性因此不仅取决于是否公开基准，还取决于划分、预处理与指标是否被固定并报告。

## 6 空白与趋势

在梳理上述证据后，该方向当前最明显的结构性空白是：**类器官扰动数据与跨物种迁移模型基本在两条平行线上发展，缺少把"类器官作为人源响应代理"与"模式生物作为可扰动、可成像、可遗传操作的体内参照"统一到同一预测框架下的工作**。跨物种基础模型一侧已有 GeneCompass、SATURN、LucaCell、UCE、Nicheformer、BrainBeacon 等覆盖人、鼠、灵长类、斑马鱼、蛙的整合与注释迁移 [15][16][17][30][28][29]，类器官一侧已有 OSCAR、Perturb-FISH、胃类器官全模态 CRISPR 筛选等扰动读出体系 [1][2][14]，但**鲜有工作把模式生物的体内扰动响应作为类器官虚拟响应的先验或校准集**。CellOT 的跨物种 LPS 任务与 Speciesformer 的生成式虚拟细胞目标最接近这一接口 [21][22]，但前者是映射学习而非类器官场景，后者摘要层面未给出下游任务数字，二者都未真正落到"类器官—模式生物—人"的三级迁移链上。

第二个空白在于**类器官药敏的临床对应研究与其虚拟建模之间缺少共享的评测协议**。药敏侧已积累直肠癌 84.43% 准确率、卵巢癌 88% 患者可找到有效药、GBO 优于 MGMT 等单癌种结论 [4][58][26]，荟萃分析给出 PDO 与 PDX 总体一致率 70% 的横截面参照 [10]；建模侧则有 PharmaFormer 用类器官药敏微调后在 TCGA 预测、以及 135 个 PDO 多组学嵌入预测 AUC [66][49]。**但两侧的终点定义、划分方式与患者队列互不统一，导致"模型预测性能"与"类器官临床预测力"无法在同一标尺上比较**。系统综述早已指出 PDO 落地需同时满足分析效度、临床效度与临床效用 [13]，而现有虚拟响应工作几乎没有按这三层分别报告指标。

第三个趋势是**评测本身正在从"模型排名"转向"划分与分布外压力测试"，但这一转向尚未传导到类器官扰动领域**。统一基准显示六个单细胞/空间基础模型无全面占优、排名随预处理与域偏移变化 [32]，VCBench 发现线性/KNN 基线在 4 个维度匹配或超越所有基础模型 [33]，EL-PERTURB 进一步指出随机划分掩盖系统性失效、模型在真实 OOD 下泛化失败 [11]。**类器官扰动建模目前仍普遍采用单一批次或单一癌种的内部验证**，如几何心脏类器官仅分化第 20 天、未验证长期功能 [41]，卵巢癌纵向药敏稳定性"仍需进一步验证" [60]，胃癌纳米机械检测依赖 AFM、通量有限 [8]。**把 OOD 划分、批次留出与跨中心验证引入类器官虚拟响应，是明确的方法学缺口**。

第四个趋势是**读出维度从"终点活力"向"空间、形态、力学、电生理"扩散，但多模态读出与扰动归因之间尚未形成可复用的表征层**。空间侧 Stereo-seq 类器官基准指出 RNA 捕获效率低于参考组织、悬浮类器官存在转录扩散导致注释困难 [45][31]；形态侧图像 profiling 与延时视频已能预测凋亡与 ATP 活力 [7][40]；物理侧心脏类器官几何库、AFM 振动、LWD-Miniscope 钙成像各自成立 [41][8][42]。**这些读出各自有预测成分，却缺少一个把空间、形态、力学、电生理对齐到同一扰动身份与同一时间轴的共享表征**；AIVO 框架提出以虚拟细胞为最小可执行单元、用受生物物理先验约束的虚拟仪器模拟检测 [12]，但仍是综述层面的构想，尚无实证工作验证该表征层能否支撑跨读出迁移。

第五个趋势是**扰动模态从单基因敲除扩展到形态发生素梯度、遗传背景多重化与组合给药，但相应的建模方法仍以单扰动、单时间点为主**。神经类器官多重单细胞筛选显示形态发生素时序、浓度与组合显著决定区域组成，且细胞系与诱导方法影响响应 [47]；皮层脑类器官多重化在 50/100/300 天重建轨迹并关联遗传变异 [46]；微流控平台已支持动态组合给药 [43]。**组合扰动下的响应预测在类器官场景中几乎空白**，现有 CINEMA-OT、DiRL、DynaVelo 分别处理因果配对、分化导航与动态推断 [34][6][38]，但均未在类器官组合扰动数据上系统验证，且 DiRL 与 DynaVelo 的生物学确证有限。

第六个值得指出的空白是**心脏/血管类器官的虚拟响应建模显著落后于肿瘤类器官**。肿瘤侧已有 PDO 药敏、CRISPR 筛选、图像与多组学嵌入的完整链条 [4][14][7][49]，心脏侧则集中在成熟方案与物理读出：AMPK/ERR 定向成熟使 TNNI3 达 18%、约 20 周胎儿水平但成年特性未完全实现 [27]，几何库识别形状决定生理属性但仅第 20 天 [41]，LWD-Miniscope 提供高通量钙成像替代 MEA [42]。**这些工作提供了扰动读出与表型终点，却尚未出现以心脏类器官为对象、以患者结局或跨物种心脏响应为目标的预测模型**，与肿瘤侧形成明显不对称。

最后，**数据资源层面存在"图谱多、扰动基准少"的失衡**。跨物种图谱侧有 260 万细胞景观、20 万小胶质细胞图谱、335,000 细胞 SATURN 语料、1.31 亿 SpeciesCorpus、8500 万 LucaCell 语料 [18][52][16][22][17]，类器官侧有 Stereo-seq 空间基准与多重化资源 [31][46]，但**面向"类器官扰动响应预测"的公开基准——固定扰动、固定读出、固定划分、含跨物种与临床终点——尚未出现**。EL-PERTURB 与 VCBench 的教训表明，缺少统一划分与 OOD 设计的基准会系统性高估模型能力 [11][33]，这一风险在类器官领域尚未被正面处理。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 类器官与器官芯片扰动建模 | 朝阳 | 已有患者来源类器官预测放化疗响应的临床验证级工作（[4]，630 引），说明读出与结局对应已跑通；同时 2025 年出现 CRISPR 筛选 + 空间转录组同步读出（[2]），把扰动从「药物浓度」推进到「基因型 × 空间位置」，方法明显未收敛；微流控组合药筛平台（[43]）仍以实验通量为主，建模成分弱，说明「筛选数据 → 预测模型」这一段仍是缺口。雷达样本中该节 n=30、近两年占比 0.54，属证据最厚的一节。 |
| 2.2 模式生物扰动响应模型 | 萌芽 | 仅 3 篇且中位引用 1，跨物种小脑皮层单细胞空间图谱（[19]）是图谱资源而非响应预测模型；表格基础模型跨体系做扰动预测的尝试（[9]）引用仅 1，属单点探索；斑马鱼/线虫/果蝇的剂量-时间响应预测基本没有成型工作。证据量不足以支撑「朝阳」判断。 |
| 2.3 跨物种迁移 | 朝阳 | 神经最优传输做单细胞扰动响应预测（[21]，364 引）提供了可复用的方法骨架；通用细胞嵌入（[30]）与 Nicheformer（[28]）把跨体系表征做成基础模型，但两者都不是为「扰动响应迁移」专门设计的，方法路线仍在竞争；跨物种细胞图谱（[18]）提供了同源映射的底座。雷达样本中该节 CNS 占比仅 0.08、中位引用 72，说明是方法社区驱动而非顶刊驱动，正处方法未定型的窗口。 |
| 2.4 虚拟组织与数字孪生建模 | 证据不足 | 仅 1 篇（[12]，AI Virtual Organoids，16 引），是概念性提出，缺少第二篇独立证据支撑阶段判断。 |
| 3 数据资源与基准 | 证据不足 | 仅 1 篇（[54]），且为发育海马图谱对基础模型的基准，与本方向的扰动-响应评测只是部分相关。 |
| 4 与临床响应的对应 | 成熟 | 2018 年即有大样本患者来源类器官复现转移性胃肠癌治疗响应（[57]，1852 引），2019 年结直肠癌化疗响应预测（[24]，694 引）与胰腺癌个体化药筛（[62]）形成重复验证；2021 年已出现把 PDO 作为预测性生物标志物的系统评价（[13]）。多癌种、多中心重复验证 + 综述化，是方法收敛、增量为主的典型特征。注意：该节以肿瘤类器官为主，**心脏/血管类器官与患者结局的对应在雷达样本中几乎缺席**。 |
| 5 评测、可复现性与争议 | 萌芽 | 三篇全部为 2026 年、引用 ≤1：单细胞/空间基础模型的统一基准（[32]）、VCBench 多维基准（[33]）、以及明确指出遗传扰动预测模型分布外失效的严格基准（[11]）。最后一篇是对整个「扰动预测」子领域的负面结论，说明评测刚起步且已出现实质性争议，属典型萌芽期信号。 |

**整体判断**：这个方向不是单一阶段，而是**三段拼在一起**——「类器官药敏 ↔ 临床结局」已经**成熟**（多癌种重复验证、已有系统评价），「类器官扰动 + 空间/单细胞读出建模」处于**朝阳**（2025 年才出现 CRISPR×空间同步读出，方法未收敛），而「模式生物响应模型」「虚拟组织」「评测基准」都还在**萌芽**，其中评测节已经出现「扰动预测模型分布外失效」的负面基准（[11]），这是最值得注意的信号：**建模侧的方法供给快于可信评测的供给**。窗口期判断：类器官扰动建模的「方法未定型」窗口大约还有 **1–2 年**（雷达样本中该节近两年占比 0.54、2026 年证据 22 条，说明正在快速填充）；跨物种迁移的方法窗口类似但更依赖基础模型迭代节奏。**最大的不确定性有三个**：(1) 评测缺口——如果分布外泛化被反复证伪，纯预测型工作的审稿门槛会快速抬高；(2) 数据瓶颈——类器官扰动 + 空间 + 影像的多模态配对数据在雷达样本中几乎没有以数据资源形式出现（第 3 节仅 1 篇），模型能力受限于数据而非算法；(3) **心脏/血管类器官这一优先子方向在证据中近乎空白**，既是机会也是风险（无对照基准、无社区共识读出）。另外提醒：雷达样本 n=67、CNS 占比 0.24 只描述这份样本，不能推出领域整体发文趋势。

**接下来怎么做**：

1. **把「跨物种扰动响应迁移」做成方法学主攻，而不是做又一个细胞嵌入。** 切入点：用跨物种细胞图谱（[18]）做同源锚定，把神经最优传输的扰动响应建模框架（[21]）从「同体系内」扩展到「小鼠/斑马鱼 → 人」，以 Nicheformer 类空间基础模型（[28]）作为表征底座。为什么现在做：现有基础模型都不是为扰动响应迁移设计的，方法位还空着；且这类工作可直接复用你已有的单细胞 + 多模态建模能力，迁移成本最低。产出：一个跨物种扰动响应预测器 + 分布外泛化评测。

2. **主动把「评测」当成一作级产出，而不是附属实验。** 切入点：针对类器官扰动预测构造分布外基准（留出供体、留出药物机制、留出物种），直接对标并回应 [11] 的失效结论，方法上借用 [32] 与 [33] 的基准设计范式。为什么现在做：评测节三篇全是 2026 年、引用 ≤1，**标准尚未被任何团队占住**；而负面结论已经出现，谁先给出可信评测谁就定义了这个子领域的审稿语言。这对生信博后是性价比最高的切入点——不需要新数据，只需要公共数据 + 严谨设计。

3. **用公共数据做「类器官药敏 → 患者结局」的建模增量，避开纯湿实验赛道。** 切入点：以 [57] 与 [24] 的 PDO-临床配对范式为问题定义，用 [13] 的系统评价作为标签与效应量来源，做「药敏读出 → 结局」的预测建模与不确定性量化。为什么现在做：这一节已成熟，意味着**问题定义和对照都现成**，适合作为你公共数据 demo 的落地场景，能快速产出一个可展示的端到端 pipeline；但要注意成熟也意味着增量空间有限，应定位为「验证 + 方法迁移」而非「新发现」。

4. **把心脏/血管类器官作为差异化下注点，但先做数据可行性验证再投入。** 切入点：雷达样本中该优先子方向几乎无证据（2.1 与第 4 节的 top 证据全是肿瘤类器官），先用公共类器官多组学数据做一次小规模可行性 demo（药敏 + 单细胞读出 → 响应预测），确认数据量与读出异质性是否支撑建模。为什么现在做：空白意味着没有竞争也没有基准，**先做可行性验证的成本远低于直接押注**；若数据可行，这是最容易形成「首个基准 + 首个模型」的位置。若不可行，退回第 1、2 条。

5. **与你的合作项目对接的具体接口：把「CRISPR × 空间同步读出」当作多模态建模的锚定任务。** 切入点：以 [2] 的同步 CRISPR 筛选 + 空间转录组为任务模板，用 [43] 的组合药筛平台数据作为扰动维度扩展，建模目标是「扰动 → 空间组织响应」的预测。为什么现在做：这是 2025 年才出现的新读出模态，**多模态融合方法几乎空白**，正好落在你「单细胞 + 多模态建模」的能力正中心；且它天然衔接合作项目的类器官 + 多组学数据，不需要另起数据采集。

## 参考文献

1. In-organoid single-cell CRISPR screening reveals determinants of hepatocyte differentiation and maturation.. Genome biology 2023. https://doi.org/10.1186/s13059-023-03084-8
2. Simultaneous CRISPR screening and spatial transcriptomics reveal intracellular, intercellular, and functional transcriptional circuits.. Cell 2025. https://doi.org/10.1016/j.cell.2025.02.012
3. Single-Cell Analysis Guides Organoid CRISPR Screening to Reveal NF1 as a Gatekeeper of Cervical Squamous Malignant Transformation.. Cancer Research 2026. https://doi.org/10.1158/0008-5472.CAN-25-5315
4. Patient-Derived Organoids Predict Chemoradiation Responses of Locally Advanced Rectal Cancer.. Cell Stem Cell 2019. https://doi.org/10.1016/j.stem.2019.10.010
5. Trellis tree-based analysis reveals stromal regulation of patient-derived organoid drug responses.. Cell 2023. https://doi.org/10.1016/j.cell.2023.11.005
6. Reinforcement learning enables single-cell foundation models to learn cellular differentiation. bioRxiv 2025. https://doi.org/10.64898/2025.12.09.693267
7. Image-based profiling and deep learning reveal morphological heterogeneity of colorectal cancer organoids. Comput. Biol. Medicine 2024. https://doi.org/10.1016/j.compbiomed.2024.108322
8. Deciphering Anti‐Cancer Drug Efficacy Through Nanomechanical Vibrations in Living Gastric Cancer Organoids. Advancement of science 2026. https://doi.org/10.1002/advs.76878
9. Tabular Foundation Models Are Competitive Cellular Perturbation Predictors Across Biological Scales. bioRxiv 2026. https://doi.org/10.64898/2026.06.28.735106
10. Comparative analysis of patient-derived organoids and patient-derived xenografts as avatar models for predicting response to anti-cancer therapy.. Cancer Treatment Reviews 2026. https://doi.org/10.1016/j.ctrv.2026.103190
11. Genetic Perturbation Prediction Models Fail Out-of-Distribution: A Rigorous Benchmark and Systematic Evaluation.  . https://doi.org/10.64898/2026.10.16.759604
12. Artificial Intelligence Virtual Organoids (AIVOs).. Bioactive materials 2025. https://doi.org/10.1016/j.bioactmat.2025.12.030
13. Patient-derived organoids as a predictive biomarker for treatment response in cancer patients. npj Precision Oncology 2021. https://doi.org/10.1038/s41698-021-00168-1
14. Large-scale CRISPR screening in primary human 3D gastric organoids enables comprehensive dissection of gene-drug interactions.. Nature communications 2025. https://doi.org/10.1038/s41467-025-62818-3
15. GeneCompass: deciphering universal gene regulatory mechanisms with a knowledge-informed cross-species foundation model.. Cell research 2024. https://doi.org/10.1038/s41422-024-01034-y
16. Toward universal cell embeddings: integrating single-cell RNA-seq datasets across species with SATURN. Nature Methods 2024. https://doi.org/10.1038/s41592-024-02191-z
17. LucaCell: a sequence-centric foundation model for cross-species single-cell analysis. bioRxiv 2026. https://doi.org/10.64898/2026.09.08.750024
18. Construction of a cross-species cell landscape at single-cell level. Nucleic Acids Research 2022. https://doi.org/10.1093/nar/gkac633
19. Cross-species single-cell spatial transcriptomic atlases of the cerebellar cortex. Science 2024. https://doi.org/10.1126/science.ado3927
20. Abstract 4372183: Cross-species single-cell reconstruction of atherosclerosis reveals predictive monocytes for acute coronary events. Circulation 2025. https://doi.org/10.1161/circ.152.suppl_3.4372183
21. Learning single-cell perturbation responses using neural optimal transport. bioRxiv 2021. https://doi.org/10.1038/s41592-023-01969-x
22. Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling.  . https://doi.org/10.64898/2026.09.22.752128
23. Cross-species cell-type assignment from single-cell RNA-seq data by a heterogeneous graph neural network. bioRxiv 2021. https://doi.org/10.1101/gr.276868.122
24. Patient-derived organoids can predict response to chemotherapy in metastatic colorectal cancer patients. Science Translational Medicine 2019. https://doi.org/10.1126/scitranslmed.aay2574
25. Patient-derived ovarian cancer organoids as platforms for predicting platinum resistance and screening tumor stem cell inhibitors.. Drug resistance updates 2026. https://doi.org/10.1016/j.drup.2026.101411
26. Patient-derived organoids predict personalized drug response and reveal alternative therapeutic options in glioblastoma. Cell Reports Medicine 2026. https://doi.org/10.1016/j.xcrm.2026.102850
27. Maturation of human cardiac organoids enables complex disease modeling and drug discovery.. Nature cardiovascular research 2025. https://doi.org/10.1038/s44161-025-00669-3
28. Nicheformer: a foundation model for single-cell and spatial omics. bioRxiv 2024. https://doi.org/10.1038/s41592-025-02814-z
29. BrainBeacon: A Cross-Species Foundation Model for Single-cell Resolved Brain Spatial Transcriptomics. bioRxiv 2025. https://doi.org/10.1101/2025.07.08.663729
30. Universal Cell Embeddings: A Foundation Model for Cell Biology. bioRxiv 2026. https://doi.org/10.1101/2023.11.28.568918
31. Application of spatial transcriptomics across organoids for a high-resolution, spatial whole-transcriptome benchmarking dataset. iScience 2026. https://doi.org/10.1016/j.isci.2026.115827
32. Harmonised benchmarking of foundation models for single-cell and spatial transcriptomics reveals context-dependent generalisation.  2026. https://arxiv.org/abs/2607.17227
33. VCBench: A Multi-Dimensional Benchmark for Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.06.18.733146
34. Causal identification of single-cell experimental perturbation effects with CINEMA-OT.. Nature methods 2023. https://doi.org/10.1038/s41592-023-02040-5
35. Integrating artificial intelligence-driven digital pathology and genomics to establish patient-derived organoids as new approach methodologies for drug response in head and neck cancer.. Oral oncology 2025. https://doi.org/10.1016/j.oraloncology.2025.107742
36. Trellis Single-Cell Screening Reveals Stromal Regulation of Patient-Derived Organoid Drug Responses. bioRxiv 2023. https://doi.org/10.1101/2022.10.19.512668
37. Deconvolution of cell type-specific drug responses in human tumor tissue with single-cell RNA-seq. Genome Medicine 2020. https://doi.org/10.1186/s13073-021-00894-y
38. Deep dynamical models of single-cell multiomic velocities predict loss-of-function and rescue perturbations in B cells.. Nature biotechnology . https://doi.org/10.1038/s41587-026-03348-1
39. Systematic modeling of phenotypic drug response profiles in patient-derived organoids. bioRxiv 2026. https://doi.org/10.64898/2026.07.29.741618
40. Spatio-Temporal Analysis of Patient-Derived Organoid Videos Using Deep Learning for the Prediction of Drug Efficacy. 2023 IEEE/CVF International Conference on Computer Vision Workshops (ICCVW) 2023. https://doi.org/10.1109/ICCVW60793.2023.00425
41. Design optimization of geometrically confined cardiac organoids enabled by machine learning techniques.. Cell reports methods 2024. https://doi.org/10.1016/j.crmeth.2024.100798
42. Heart‐on‐a‐Miniscope: A Miniaturized Solution for Electrophysiological Drug Screening in Cardiac Organoids. Small 2024. https://doi.org/10.1002/smll.202409571
43. Automated microfluidic platform for dynamic and combinatorial drug screening of tumor organoids. Nature Communications 2020. https://doi.org/10.1038/s41467-020-19058-4
44. Single-Cell-Derived Tumor Organoid (STO) arrays on a microfluidic chip for personalized drug screening to address heterogeneity-induced drug resistance in colorectal cancer. Microsystems & Nanoengineering 2025. https://doi.org/10.1038/s41378-025-01068-1
45. Application of spatial transcriptomics across organoids: a high-resolution spatial whole-transcriptome benchmarking dataset. bioRxiv 2026. https://doi.org/10.1101/2025.05.04.651803
46. Multiplexing cortical brain organoids for the longitudinal dissection of developmental traits at single-cell resolution.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02555-5
47. Decoding morphogen patterning of human neural organoids with a multiplexed single-cell transcriptomic screen. bioRxiv 2024. https://doi.org/10.1101/2024.02.08.579413
48. Accelerating Leigh syndrome drug discovery through deep learning screening in brain organoids.. Nature communications 2026. https://doi.org/10.1038/s41467-026-71391-2
49. Abstract 494: Multi-omics patient-derived organoid embeddings predict targeted therapy response and KRAS inhibitor sensitivity.. Cancer Research 2026. https://doi.org/10.1158/1538-7445.am2026-494
50. A deep learning-based computational pipeline predicts developmental outcome in retinal organoids.. PLoS biology 2026. https://doi.org/10.1371/journal.pbio.3003597
51. Emerging frontiers for AI in single-cell genomics.. Molecular cell . https://doi.org/10.1016/j.molcel.2026.09.014
52. Single-Cell Atlas of Microglia Reveals Conserved and Divergent Cell Populations in Mouse and Human Brain 2255696. Journal of Immunology 2026. https://doi.org/10.1093/jimmun/vkag141.278
53. Mouse-Geneformer: A deep learning model for mouse single-cell transcriptome and its cross-species utility. bioRxiv 2024. https://doi.org/10.1371/journal.pgen.1011420
54. A lifespan single-cell atlas of the human developing hippocampus benchmarks familial Alzheimer's disease brain organoids..  . https://doi.org/10.64898/2026.09.18.752796
55. Prospective comparison of patient-derived organoid drug screening with standard guideline recommendations for colorectal cancer liver metastasis.. Journal of Clinical Oncology 2026. https://doi.org/10.1200/jco.2026.44.16_suppl.e15609
56. Personalized drug screening using patient-derived organoid and its clinical relevance in gastric cancer.. Cell reports. Medicine 2024. https://doi.org/10.1016/j.xcrm.2024.101627
57. Patient-derived organoids model treatment response of metastatic gastrointestinal cancers. Science 2018. https://doi.org/10.1126/science.aao2774
58. Patient-Derived Ovarian Cancer Organoids Mimic Clinical Response and Exhibit Heterogeneous Inter- and Intrapatient Drug Responses.. Cell Reports 2019. https://doi.org/10.1101/2019.12.12.19014712
59. Patient-derived organoids predict responses to chemotherapy and PARP inhibitors in advanced ovarian cancer. Journal of Translational Medicine 2026. https://doi.org/10.1186/s12967-025-07112-y
60. Longitudinal prediction of drug response in high-grade serous ovarian cancer organoid cultures aligning with clinical responses. bioRxiv 2024. https://doi.org/10.1016/j.jare.2025.08.009
61. Individualized patient tumor organoids faithfully preserve human brain tumor ecosystems and predict patient response to therapy.. Cell stem cell 2025. https://doi.org/10.1016/j.stem.2025.01.002
62. Pancreatic cancer organoids recapitulate disease and allow personalized drug screening. Proceedings of the National Academy of Sciences of the United States of America 2019. https://doi.org/10.1073/pnas.1911273116
63. Biomarker-guided responses in patient-derived organoids predict effective therapies in breast cancer. Cell Reports Medicine 2026. https://doi.org/10.1016/j.xcrm.2026.102973
64. Personalized prediction of chemotherapy efficacy in osteosarcoma through patient-derived organoids: correlation with survival and tumor proliferation potential. Journal of experimental & clinical cancer research : CR 2025. https://doi.org/10.1186/s13046-025-03541-1
65. Abstract 2503: Lung cancer organoid-based diagnostic response prediction (CODRP) for predicting anticancer drug response and progression-free survival. Cancer Research 2026. https://doi.org/10.1158/1538-7445.am2026-2503
66. PharmaFormer predicts clinical drug responses through transfer learning guided by patient derived organoid. npj Precision Oncology 2025. https://doi.org/10.1038/s41698-025-01082-6
67. AI-driven framework modeling perturbation in brain organoids reveals candidate genes for autism. bioRxiv 2026. https://doi.org/10.64898/2026.08.22.746387
