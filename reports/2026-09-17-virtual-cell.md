# 专题调研：虚拟细胞 virtual cell（2026-03-21 ~ 2026-09-17）

# 虚拟细胞（Virtual Cell）近 6 个月研究调研报告

> 说明：本报告严格基于所提供的 77 篇文献抽取结果撰写。产业新闻部分因输入为空，按写作要求标注"本期无足够信息"。所有定量结果均保留原文数字，未引入抽取结果之外的引用。

---

## 摘要（TL;DR）

1. **虚拟细胞正从"表征模型"转向"世界模型/生成模拟"**：CellOS（多视图联合嵌入世界模型）、Lingshu-Cell（掩码离散扩散）、Chreode（一步式时序动力学）、U-Pert（非平衡生成动力学）等一批工作明确以"细胞世界模型"为目标，强调干预条件下的状态转移而非静态表征。
2. **扰动响应预测进入"大基准 + 严格反思"阶段**：至少 10 项基准/评估工作集中出现（Empirical Comparison、VCBench、AssayBench、scArchon、STGBench、SBB 原则、PerturbHD、scContam、SVC-Probe、SCMBench），核心结论是**现有基准高估了模型能力**。
3. **最刺眼的负面证据**：29 个数据集 7170 个扰动中 **65% 不可靠、11% 共享、24% 特异**；PBMC 3k 与 CELLxGENE 人胰岛图谱存在 **80.4% 预训练重叠证据**；逐细胞 macro-F1 仅 **0.2–0.3**；无神经网络的解析校准方法可**匹配或超越**深度模型。
4. **多模态整合成为主战场**：HoloCell（表观+转录+蛋白三模态）、CellxPert（scRNA/ATAC/CITE/MERFISH/IMC）、MultiVCDiff（形态+转录组）、StateXDiff（多模态扩散）等，直接对应"缺失模态处理"与"跨模态对齐"需求。
5. **蛋白质组虚拟细胞出现里程碑**：Nature 的 ProteinTalks 基于 **3800 万条时序蛋白丰度测量**，是本期唯一大规模时序蛋白组资源，与衰老/蛋白组方向高度相关。
6. **Agent 化科研工作流密集落地**：VCHarness（自主 AI 智能体+基础模型）、CellScientist（双空间分层编排）、AblateCell（复现-消融智能体）、VCR-Agent（多智能体验证式推理）构成一条清晰的"自动化建模"线索。
7. **评测揭示"癌细胞系异质性"是规模化筛选的首要瓶颈**：UniPert-G2CP 扩展到 162 细胞系/32039 化合物/12328 基因后，正常与原代细胞系 PCC **0.480** vs 癌细胞系 **0.296**（p=3.93e-11）。
8. **产业侧本期无足够信息**：输入未提供任何公司、合作或授权新闻，无法评估转化动态。

---

## 背景与定义

虚拟细胞（virtual cell）指以计算模型模拟细胞结构、状态与功能，并预测细胞对遗传、化学、细胞因子等扰动响应的一类方法体系。本期文献显示该概念已从早期 E-Cell、CellPACK 等机制性平台，演进为以**单细胞/空间多组学数据 + 基础模型 + 生成式建模**为主流技术栈的预测性框架。多篇工作（What Makes a Virtual Cell a World Model?、The next-generation virtual cell、Virtual cell: Current perspectives）尝试给出更严格的形式化定义：虚拟细胞世界模型（VCWM）被刻画为具有生物与观测上下文、干预条件转移和时变结构的"维持性细胞状态"，并明确指出三个反复出现的缺口——**表征不等于动力学、预测不等于干预、多模态不等于多尺度世界建模**。同时，Virtual cell/virtual cell like 一文指出该术语在 HIV 研究中尚未标准化，但多尺度、多模态计算模拟的核心概念已深入前沿。

---

## 关键时间线

### 2026 年 3 月
- **03-23** CellFluxRL：用强化学习对图像型虚拟细胞生成模型做后训练，设计生物功能、结构有效性、形态正确性三类共 7 个奖励，在所有奖励指标上持续优于 CellFlux。
- **03-26** Lingshu-Cell：掩码离散扩散生成模型，覆盖约 18000 个基因，直接在离散 token 空间建模单细胞转录组。
- **03-28** Virtual cell/virtual cell like（HIV/AIDS 治疗综述）。
- 另有 Evaluating the Utilities of Foundation Models in Single-Cell Data Analysis（十个基础模型/八任务）。

### 2026 年 4 月
- **04-07** T-World 虚拟人心肌细胞（Circulation Research），数据驱动微分方程描述性别特异性兴奋-收缩耦联。
- **04-13** Towards Autonomous Mechanistic Reasoning in Virtual Cells：发布 VC-TRACES 数据集，提出 VCR-Agent 多智能体框架。
- **04-14** VCHarness：自主 AI 智能体 + 生物基础模型，自动探索架构与训练流程。
- **04-16** Intermediate Layers Encode Optimal Biological Representations：轨迹最优层较末层 +31%。
- **04-21** AblateCell：面向虚拟细胞仓库的"先复现再消融"智能体。
- **04-22** AROMA（多模态增强推理，构建两个知识图谱）；Signal, Bounds, and Baselines（SBB 评测原则）。
- **04-25** Are Current AI Virtual Cell Models Useful for Scientific Discovery?：提出 PerturbHD 命中发现评估框架。
- **04-28** scPert（多模态 LLM 知识融合 Transformer）；From genes to germ layers（原肠胚虚拟孪生）。
- **04-30** Benchmarking virtual cell models for in-the-wild perturbation response；CellxPert（多组学基础模型 + MCMC 引导，154 类细胞注释标签空间）。

### 2026 年 5 月
- **05-02** SCMBench：23 种方法的多组学整合基准。
- **05-08** CellScientist：双空间分层编排，闭环修正虚拟细胞模型。
- **05-11** AssayBench：assay 级别 LLM/智能体虚拟细胞基准。
- **05-12** scArchon：基于 Snakemake 的可复现基准平台，6 个 scRNA-seq 数据集。
- **05-15** StateXDiff：细胞状态上下文化多模态扩散。
- **05-21** MultiVCDiff：1118 化学 + 130 遗传扰动、4 数据集，零样本下优于单模态基线。
- **05-27** Virtual cell: Current perspectives and future prospects（综述）；Chreode：一步式细胞世界模型。
- **05-28** Computational blueprints for cell fate programming（综述）。

### 2026 年 6 月
- **06-07/06-11** HoloCell：首个面向表观/转录/蛋白三模态的生成式基础模型。
- **06-08/06-11** OCOO-T：极简 flow matching 虚拟细胞模型（arXiv 与 europepmc 双版本）。
- **06-09** Evaluating the role of pretraining dataset size and diversity：2220 万细胞、400 模型、6400 实验，性能随数据规模趋于平台。
- **06-15/06-18** Benchmarking gene expression reconstruction from single-cell latent representations；VCBench（七维度中五维可评测）。
- **06-16/06-22** ImmuneNavi：AI 虚拟细胞免疫恢复模型，配对 PBMC 单细胞转录组，用于中药成分筛选。
- **06-18/06-23** CellOS：多视图联合嵌入世界模型，三阶段训练策略。
- **06-26** SVC-Probe：空间基础模型嵌入扰动泛化评估，98.6% 三方一致性。
- **06-30/07-04** U-Pert：非平衡生成动力学，从非配对单细胞快照学习扰动动力学。

### 2026 年 7 月
- **07-01** scDifformer（NAR）：扩散后训练 Transformer，跨 7 个组织基准；STGBench：空间 DNA-RNA 测序级模拟器。
- **07-06** Score Distributions, Not Cells：逐细胞 macro-F1 仅 0.2–0.3。
- **07-08** Universal cell embedding（UCE，Nature）；Counterfactual Diffusion Modeling（SPAD-CFR，空间点云反事实扩散）。
- **07-12** OCellus：基于 Qwen3.5-9B 的 90 亿参数语言模型，22 项生物任务，EvenClock 空间编码。
- **07-16** scYeast：首个酵母单细胞转录组基础模型。
- **07-17** A Neural-Network-Free Calibration：AMM-SimWMag 匹配或超越 scGen 等深度模型。
- **07-21** What Makes a Virtual Cell a World Model?；Auditing pretraining contamination（scContam）。
- **07-22** An Empirical Comparison of Virtual Cell Models：11 种方法/5 模型家族/6 类任务/9 个数据集。
- **07-24** The next-generation virtual cell（Life Sciences 综述）。
- **07-25** Integrative AI-Enabled Virtual Cell Modeling（CD8⁺ T 细胞潜在效应状态）；UniPert-G2CP（Cell）。
- **07-30** The organ-on-a-chip-AI virtual cell loop（Science Bulletin）。

### 2026 年 8 月
- **08-01** 西湖秋季 AI 蛋白质组学与虚拟细胞研讨会综述；多模态肿瘤边界聚类识别（Golden Eyes 3.0）。
- **08-03** CellPrism 可视分析系统；Scaling an Autoregressive Transformer for Single-Cell Generation。
- **08-07** GeneGeoFlow：控制锚定残差流匹配，以基因几何为条件。
- **08-09** Human-Guided Causal Knowledge Injection for Virtual Cells。
- **08-10/08-15** Cancer Cell Line Heterogeneity：162 细胞系/32039 化合物/12328 基因，正常细胞 PCC 0.480 vs 癌细胞 0.296。
- **08-11/08-12** Reliable single-cell perturbations：29 数据集/7170 扰动，65% 不可靠。
- **08-26** Artificial intelligence virtual bone organoids（AIVBOs）。
- **08-29** scPILOT：深度生成模型 + 最优传输，跨生物情境扰动响应预测。

### 2026 年 9 月
- **09-01** TFActProfiler：260 万 TF-mRNA 相互作用资源。
- **09-08/09-10** PHAROS：将预训练扰动模型转为靶向药物组合搜索引擎。
- **09-09** An operational perturbation proteomics-based virtual cell model（Nature，ProteinTalks）；A systematic comparison of single-cell perturbation response prediction models（Science Advances，13 方法/25 数据集/24 指标）。
- **09-14** scKITE：知识增强单细胞基础模型。
- **09-17** Toward AI Virtual Cells for Hepatology（综述）。

---

## 使用的技术

### 1. 生成式建模（扩散 / 流匹配 / 非平衡动力学）

- **Lingshu-Cell**：掩码离散扩散模型，直接在离散 token 空间建模单细胞转录组状态分布，覆盖约 18000 个基因，无需先验即可捕捉全转录组表达依赖，支持扰动条件下的模拟。
- **OCOO-T**：极简 flow matching 模型，预测单细胞对遗传、化学和细胞因子扰动的转录响应；刻意避免辅助细胞状态编码器、层次 VAE、专用 Transformer 编解码模块或基因互作先验，以提升可扩展性与泛化性。
- **GeneGeoFlow**：控制锚定残差流匹配，以生物网络导出的基因几何为条件，区分稳定关联与干预特异的响应方向和幅度，用于未见遗传扰动和药物组合预测。
- **StateXDiff**：细胞状态上下文化多模态扩散，先学习解耦的多模态细胞状态表征再建模条件分布，缓解仅依赖 RNA、条件分布漂移和低信噪比导致的伪相关。
- **MultiVCDiff**：统一多模态生成扩散框架，从化学或遗传扰动同时预测高保真细胞形态图像和转录组谱，无需扰动后实测数据；在 1118 个化学 + 130 个遗传扰动、4 个数据集上训练，严格零样本设置下优于最先进单模态基线。
- **U-Pert**：非平衡生成框架，从非配对单细胞快照学习条件与情境依赖的扰动动力学，联合建模转录组状态转移与细胞数量变化，刻画增殖、凋亡、选择导致的非质量守恒响应。
- **scDifformer**：上下文感知 Transformer + 去噪扩散模块，三阶段（掩码语言模型预训练、扩散驱动后训练、下游微调），跨 7 个组织基准测试。
- **CellFluxRL**：用强化学习对图像型生成虚拟细胞模型后训练，7 个奖励（生物功能、结构有效性、形态正确性三类），所有奖励指标优于 CellFlux，测试时扩展进一步提升。

### 2. 世界模型与动力学建模

- **CellOS**：多视图基础模型，从配对的表达与感知视图学习细胞表征；三阶段训练（因果细胞句子语言建模、保函数稠密到专家混合扩展、潜在空间对齐），目标是学习可表征、查询和预测细胞状态的世界模型。
- **Chreode**：一步式细胞世界模型，结构化残差转移算子预测动作条件下的细胞状态转变，将分布演化从推理时转移到训练时，实现单次前向生成；受 Waddington 景观启发，分解为下坡景观流、切向旋转动态和随机扩散。
- **What Makes a Virtual Cell a World Model?**：提出 VCWM 结构化评估框架，形式化为具有生物与观测上下文、干预条件转移和时变结构的维持性细胞状态，给出三个动机实验与路线图。

### 3. 基础模型与表征学习

- **UCE（Universal Cell Embedding）**：自监督跨物种、跨组织大规模细胞数据训练，构建统一生物潜空间，捕捉重要生物变异并抵抗实验噪声，新细胞无需标注即可嵌入（Nature）。
- **HoloCell**：首个面向表观基因组、转录组和蛋白质组三大单细胞组学模态的生成式基础模型，联合表示学习与生成建模，稳健应对模态缺失异质性。
- **CellxPert**：可扩展多模态基础模型，在共同表示空间统一单细胞和空间多组学，联合编码转录组、染色质可及性和表面蛋白，纳入 MERFISH 和成像质谱空间层；支持 154 类细胞注释、LoRA 微调、全基因组转录组扰动响应预测。
- **scYeast**：首个酵母单细胞转录组基础模型，非对称并行架构将转录调控信息注入 Transformer 注意力机制。
- **scKITE**：知识增强单细胞基础模型，通过轻量辅助解码器将细胞级文本注释与基因级调控监督融入共享 Transformer 编码器，预训练后丢弃解码器。
- **OCellus**：基于 Qwen3.5-9B 的 90 亿参数语言模型，22 项生物任务微调；EvenClock 将二维空间坐标编码为 18 个钟面扇区文本，统一支持单细胞、空间与扰动生物学及自然语言推理。
- **Intermediate Layers Encode Optimal Biological Representations**：系统评估 scFoundation 和 Tahoe-X1 各层表征，轨迹在 60% 深度达峰（较末层 +31%），扰动最优层随 T 细胞激活状态偏移 0–96%，静息细胞中首层优于所有深层。
- **Scaling an Autoregressive Transformer for Single-Cell Generation**：因果 Transformer + 学习型量化 VAE 分词器，交叉熵损失训练，评估生成分布生物保真度并刻画预训练损失缩放行为。

### 4. 多模态整合与缺失模态处理

- **HoloCell**（见上）、**CellxPert**（见上）、**StateXDiff**（见上）、**MultiVCDiff**（见上）。
- **SCMBench**：23 种方法在单细胞多组学整合中的基准，评估整合准确性、生物标志物检测、轨迹推断和批次效应校正，揭示基础模型相较专用模型的效能与局限。
- **STGBench**：测序级空间 DNA-RNA 模拟器，在用户定义二维组织网格上生成配对 DNA-seq BAM 与匹配基因表达矩阵，支持多组学与虚拟细胞导向的多模态基准测试。

### 5. Agent / LLM 驱动的自动化建模

- **VCHarness**：将 AI 编码智能体与多模态生物基础模型结合，自动探索架构与训练流程，构建遗传和化学扰动到转录响应的预测模型，以极少人工干预自动生成、评估和优化模型。
- **CellScientist**：双空间分层编排框架，耦合高层假设空间与低层可执行实现空间，使预测偏差能在建模假设、表征设计、实现或任务约束等层级间传播反馈，支持闭环修正。
- **AblateCell**：面向虚拟细胞仓库的"先复现再消融"智能体，自动配置环境、解决依赖与数据问题、重跑官方评估以端到端复现报告基线，随后闭环消融检验组件重要性。
- **VCR-Agent**：多智能体框架，将生物推理表示为可系统验证和证伪的机制动作图，结合有生物依据的知识检索与验证器过滤，发布 VC-TRACES 数据集。
- **AROMA**：增强推理多模态架构，整合文本证据、图拓扑信息和蛋白序列特征建模扰动-靶点依赖关系，两阶段优化，构建两个知识图谱和扰动推理数据集。
- **Human-Guided Causal Knowledge Injection**：基因相似度感知的因果图可视化 + 混合优化算法，引入人工引导修正因果图。

### 6. 扰动响应预测（非生成式 / 迁移学习）

- **UniPert-G2CP**：两阶段深度学习框架，统一多模态分子扰动表示，实现遗传到化学扰动的表型迁移学习，桥接遗传与化学筛选（Cell）。
- **scPILOT**：查询条件化框架，判别器辅助训练学习生成式隐表示，借助潜在最优传输将已观测扰动响应迁移到新生物情境（细胞类型、患者、物种）。
- **scPert**：基于 Transformer 的多模态框架，融合大语言模型嵌入预测单细胞遗传扰动效应。
- **PHAROS**：将预训练单细胞扰动模型转化为靶向药物组合搜索引擎，逐个预测药物作用下细胞群变化再串联模拟组合，无需重新训练；在两个独立组合扰动数据集中恢复精确或机制匹配的双药响应。
- **AMM-SimWMag**：无神经网络解析校准方法，将 scGen 优势分解为每类型响应幅度和每基因响应方向两个无泄漏解析部分，加入每基因仿射矩匹配；在 4 数据集、3 类生物学、2 种 LOCO 轴、九指标评估下匹配或超越深度模型。
- **TFActProfiler**：整合 ChIP、motif 和人工注释等异质先验与大规模 bulk 及单细胞 RNA-seq 图谱，学习带符号定量 TF-mRNA 调控系数，构建 2,606,176 个带符号 TF-mRNA 相互作用资源，TF 敲低基准中优于常用 regulon 资源。

### 7. 空间与形态学建模

- **SPAD-CFR**：将组织视为包含细胞分子谱和物理坐标的空间点云，采用 Pearl 三步反事实工作流进行空间靶向重编程。
- **SVC-Probe**：结合亚细胞嵌入图谱稳定性、Mondrian 邻域图和基础模型扰动探针，评估荧光显微图像空间基础模型嵌入在药物处理下的稳定性、邻域重连与质心预测；应用于含 462 个抗体标签的 CM4AI MDA-MB-468 化学扰动图谱与 SubCell 1536 维嵌入，98.6% 三方一致性。
- **CellPrism**：可视分析系统，帮助研究者交互式分析基因扰动预测结果，应对扰动空间组合爆炸与细胞特异性响应复杂问题。

### 8. 机制性 / 微分方程 / 多范式智能体

- **T-World 虚拟人心肌细胞**：数据驱动微分方程描述性别特异性兴奋-收缩耦联、机械收缩、β 肾上腺素信号及其细胞靶点效应。
- **From genes to germ layers**：以智能体驱动的多范式方法构建原肠胚虚拟孪生。
- **AIVBOs**：以虚拟细胞为基本单元，融合多模态组学数据与生物物理约束，构建 AI 虚拟骨器官oid，目前仍处早期构想阶段。

---

## 数据

### 大规模扰动资源
- **ProteinTalks / 时序扰动蛋白质组**：超过 **3800 万条**时序蛋白丰度测量，来自系统扰动的乳腺癌细胞系，是本期唯一的超大规模时序蛋白组资源（Nature）。
- **UniPert-G2CP 扩展平台**：**162 个细胞系、32039 个化合物、12328 个基因**输出。
- **MultiVCDiff trimodal 语料**：**1118 个化学扰动 + 130 个遗传扰动**，4 个数据集。
- **TFActProfiler**：**2,606,176 个**带符号 TF-mRNA 相互作用。
- **Reliable single-cell perturbations**：**29 个数据集、7170 个扰动**。
- **Evaluating pretraining dataset size**：**2220 万细胞**语料、**400 个模型**、**6400 次实验**。
- **A systematic comparison**：**13 种方法、25 个数据集、24 个指标**。
- **Empirical Comparison of Virtual Cell Models**：**11 种方法、5 个模型家族、6 类任务、9 个公开数据集**。

### 多模态 / 空间数据
- **HoloCell**：单细胞表观、转录、蛋白三模态。
- **CellxPert**：scRNA / ATAC / CITE / MERFISH / IMC。
- **STGBench**：配对 DNA-seq BAM 与表达矩阵，二维组织网格。
- **SVC-Probe**：CM4AI MDA-MB-468 化学扰动图谱（462 抗体标签）+ SubCell 1536 维嵌入。
- **Integrative AI Virtual Cell（CD8⁺ T）**：单细胞 RNA 测序 + 配对 TCR 测序。
- **ImmuneNavi**：配对 PBMC 单细胞转录组。
- **Lingshu-Cell**：约 18000 基因的单细胞转录组。
- **scDifformer**：大规模多模态单细胞数据，7 个组织。
- **OCellus**：22 项生物任务。
- **scYeast**：大规模酵母单细胞转录组。
- **UCE**：跨物种多组织单细胞数据。
- **SCMBench**：23 种方法、多组学数据。
- **scArchon**：6 个代表性 scRNA-seq 数据集。
- **VCBench**：五个基础模型、多数据集。
- **CellxPert**：154 细胞类型标签空间。

### 知识资源与数据集发布
- **VC-TRACES**（VCR-Agent 发布）。
- **AROMA**：两个知识图谱 + 扰动推理数据集。
- **TFActProfiler**：TF 调控图谱资源。
- **PerturbHD**：命中发现评估框架（非数据集，但定义了评估数据需求）。

---

## 应用场景

### 1. 药物发现与虚拟筛选
- **VCHarness**：扰动响应建模、药物发现。
- **ProteinTalks**：在硅药物发现、治疗响应预测。
- **PHAROS**：靶向药物组合筛选，恢复精确或机制匹配双药响应。
- **MultiVCDiff**：从头虚拟筛选，零样本预测形态与转录组。
- **CellPrism**：药物发现中虚拟细胞的可视探索。
- **OCOO-T**：药物发现 / 基因调控网络。
- **AssayBench**：体外表型筛选、in silico 表型筛选标准评测。

### 2. 免疫与免疫治疗
- **Integrative AI Virtual Cell（CD8⁺ T）**：识别此前未被认识的 CD8⁺ T 细胞动态潜在效应状态，与免疫检查点抑制剂治疗响应相关，常规分析无法检测。
- **ImmuneNavi**：配对 PBMC 数据中对中药成分排序，将异质 PBMC 队列映射到统一健康免疫坐标系。
- **A systematic comparison**：包含两个原代免疫细胞药物响应资源。

### 3. 复杂疾病与器官特异性虚拟细胞
- **肝病虚拟细胞**（Toward AI Virtual Cells for Hepatology）：生成模型表征、动力学与运输模型、预训练/基础模型三条路线；指出单细胞与空间图谱无法预测肝损伤进展或对未测试药物、毒物、遗传扰动的响应。
- **HIV/AIDS**（Virtual cell/virtual cell like）：多尺度、多模态计算模型模拟 HIV 感染、免疫应答和治疗干预。
- **T-World 虚拟人心肌细胞**：心律失常机制与治疗。
- **AIVBOs**：骨器官oid 标准化与筛选。
- **原肠胚虚拟孪生**：人类原肠胚多尺度生物学重建。
- **肿瘤边界识别**（Golden Eyes 3.0）：图卷积虚拟细胞模型 + 近红外光谱 + 门控注意力多模态融合。

### 4. 细胞命运编程与干预设计
- **U-Pert**：细胞命运设计、最优干预的逆设计。
- **Computational blueprints for cell fate programming**：细胞注释、网络推断、轨迹分析、转录因子与小分子优先级排序，整合为迭代设计-测试-学习流程。
- **SPAD-CFR**：组织微环境空间靶向重编程。

### 5. 闭环实验与器官芯片
- **The organ-on-a-chip-AI virtual cell loop**：提出器官芯片与 AI 虚拟细胞构成的闭环路径（摘要缺失，具体方法与结果无法确认）。
- **The next-generation virtual cell**：从时空转录组建模到复杂疾病闭环靶点发现，弥合体外靶点筛选与体内疗效间的转化鸿沟。

### 6. 中药与天然产物筛选
- **ImmuneNavi**：中药处理-对照谱转化为固定成分扰动库，患者与成分状态在匹配的基因、通路和转录层面表征。

---

## 评测与可靠性反思

本期最显著的特征是**评测与批判性工作的大量涌现**，且结论普遍偏负面。

### 基准与评估框架
- **An Empirical Comparison of Virtual Cell Models**：统一数据划分与预处理下比较 11 种方法（GEARS、CPA、chemCPA、scGen、Geneformer、scGPT、scFoundation、UCE、State 等）、5 个模型家族、6 类任务、9 个公开数据集，揭示基线差距，指出哪些能力真实可靠。
- **VCBench**：将四个独立虚拟细胞框架综合为七个能力维度（扰动响应预测、跨物种通用性、基因调控网络推断、模态整合、时序动态、多尺度整合、in silico 实验），评估五个基础模型；**多尺度整合和 in silico 实验在当前架构与数据下尚无法端到端测试**。
- **AssayBench**：assay 级别基准，评估 LLM 和智能体在未见生物背景下预测细胞扰动表型效应的能力，弥补现有基准偏重分子读出、与真实药物发现表型终点脱节的问题。
- **scArchon**：基于 Snakemake 的可复现模块化基准平台，在 6 个 scRNA-seq 数据集上比较 scGen、CPA、trVAE、scPRAM、scVIDR、scDisInFact、SCREEN、scPreGAN、CellOT 等与基线方法。
- **Benchmarking virtual cell models for in-the-wild perturbation response**：在未见细胞背景、未见扰动和跨数据集等真实挑战场景下评估多种模型。
- **Signal, Bounds, and Baselines（SBB）**：Signal 引入诊断元指标并推广基于差异表达基因的加权或过滤；Bounds 提供扰动级指标校准；Baselines 强调合理基线。
- **PerturbHD**：面向 AI 驱动命中发现的评估框架，主张建立直接衡量模型预测对具体科学发现成果价值的新基准。
- **SCMBench**：23 种方法的多组学整合基准，指出当前评估空白并提供整合工具使用指南。
- **STGBench**：解决空间 CNV、SNV 和突变负荷代理分析缺乏已知真值数据的问题。
- **SVC-Probe**：98.6% 三方一致性。
- **A systematic comparison**（Science Advances）：13 种方法、25 个数据集、24 个指标，覆盖多种扰动模态和物种，评估未见单基因扰动泛化、组合交互预测和跨细胞类型迁移三类任务，**发现性能强烈依赖扰动效应大小**。

### 批判性结果与"没跑赢基线"的证据
1. **数据可靠性危机**：29 个数据集的 7170 个扰动中，**65% 不可靠、11% 共享、24% 特异**；将质量标签应用于已发表基准后发现**模型比较结果依赖于扰动质量**，使用可靠扰动训练可改善性能。
2. **预训练污染**：scContam 逐细胞审计框架（MinHash 基因集指纹 + MIA-scFM 成员推断攻击）应用于四个 scIB 基准和三个 scFM，发现 **PBMC 3k 与 CELLxGENE 人胰岛图谱存在 80.4% 预训练重叠证据**，提示零样本性能可能反映预训练暴露而非真实泛化。
3. **逐细胞指标失效**：单细胞扰动数据类别高度重叠，逐细胞准确率实际衡量的是重叠而非模型质量，线性分类器、MLP 和 Transformer 的 **macro-F1 均停滞在 0.2–0.3**；应改为在扰动群体层面聚合分类器概率向量评分。
4. **无神经网络方法追平深度模型**：AMM-SimWMag 在 4 数据集、3 类生物学、2 种 LOCO 轴、九指标评估下**匹配或超越** scGen 等深度单细胞扰动响应模型。
5. **预训练规模收益递减**：2220 万细胞、400 模型、6400 实验显示，当前方法在远小于现有语料的数据规模上性能即趋于平台，**不同于大语言模型**。
6. **癌细胞系异质性瓶颈**：UniPert-G2CP 扩展到 162 细胞系/32039 化合物/12328 基因后，正常和原代细胞系预测保真度显著高于癌细胞系，平均 **PCC 0.480 vs 0.296**（Mann-Whitney p=3.93e-11）。
7. **表征层选择被忽视**：最优层依赖任务和上下文，轨迹在 60% 深度达峰（较末层 +31%），扰动最优层随 T 细胞激活状态偏移 0–96%，静息细胞中首层优于所有深层——表示选择通常被当作实现细节而非核心建模决策。
8. **概念缺口**：VCWM 框架指出表征不等于动力学、预测不等于干预、多模态不等于多尺度世界建模；肝病综述指出单细胞与空间图谱本身无法预测肝损伤进展或对未测试扰动的响应。

---

## 产业动态

**本期无足够信息。** 输入未提供任何公司、合作、授权或融资新闻，无法评估虚拟细胞领域的转化与商业化动态。文献中仅有的产业化线索包括：
- **The organ-on-a-chip-AI virtual cell loop**（Science Bulletin）提出器官芯片与 AI 虚拟细胞的闭环路径，但摘要缺失，无法确认具体合作方或落地情况。
- **AIVBOs**（Journal of Orthopaedic Translation）提出 AI 虚拟骨器官oid 概念，明确"目前仍处早期构想阶段"。
- **CellPrism** 面向药物发现场景的可视分析系统，属工具层而非产业合作。

---

## 趋势结论与空白

1. **"世界模型"叙事已成型但缺乏统一评测**：CellOS、Chreode、Lingshu-Cell、U-Pert、VCWM 框架共同指向干预条件下的状态转移建模，但 VCWM 明确指出"多模态不等于多尺度世界建模"，且 VCBench 显示多尺度整合与 in silico 实验**当前无法端到端测试**——这是一个明确的方法学空白。
2. **数据可靠性审计应成为标准前置步骤**：65% 扰动不可靠、80.4% 预训练重叠、macro-F1 0.2–0.3 三项证据叠加，意味着**任何新模型报告的性能数字都需要先过数据质量与污染审计**。目前只有 scContam、Reliable single-cell perturbations 等少数工作在做这件事，尚未形成社区标准流程。
3. **无神经网络基线被系统性低估**：AMM-SimWMag 匹配或超越深度模型，提示大量深度扰动预测工作的增益可能来自校准而非表征学习。**缺少将解析基线纳入标准对比的系统性实践**。
4. **时序蛋白质组虚拟细胞仅有一个孤例**：ProteinTalks 的 3800 万条时序蛋白丰度测量是本期唯一大规模时序蛋白组资源，且未见后续工作在其上做迁移、跨模态对齐或衰老建模。**蛋白组 × 虚拟细胞 × 时序动力学**是明显空白。
5. **多模态缺失处理刚起步**：HoloCell 明确以"稳健应对模态缺失异质性"为目标，但仅覆盖表观/转录/蛋白三模态；CellxPert 覆盖 scRNA/ATAC/CITE/MERFISH/IMC 但未强调缺失模态。**跨队列校正、增量学习/持续学习在虚拟细胞语境下几乎未见专门工作**。
6. **衰老方向在 77 篇文献中几乎缺席**：未出现以 aging clock、衰老细胞、衰老队列为核心的虚拟细胞工作。考虑到虚拟细胞与单细胞/多模态/扰动建模的高度重叠，**衰老虚拟细胞（aging virtual cell）是一个未被占据的方向**。
7. **Agent 化科研工作流密集但缺乏互操作标准**：VCHarness、CellScientist、AblateCell、VCR-Agent 各自定义任务与验证器，**没有共享的智能体-模型接口或复现协议**；AblateCell 的"先复现再消融"是目前最接近可验证工件的方案。
8. **空间虚拟细胞与组织尺度建模脱节**：SPAD-CFR、SVC-Probe、STGBench 处理空间维度，但 VCBench 指出多尺度整合无法端到端测试；**从单细胞到组织微环境的多尺度世界模型尚无可行架构**。
9. **临床转化评估框架缺失**：PerturbHD 提出应衡量模型预测对具体科学发现成果的价值，但本期未见任何工作报告"虚拟细胞预测 → 实验验证 → 临床命中"的完整闭环数据。
10. **癌细胞系异质性作为首要瓶颈尚未被系统性解决**：PCC 0.480 vs 0.296 的差距明确指向细胞系异质性，但未见针对该瓶颈的专门方法学工作（如细胞系特异校正、原代细胞迁移学习）。

---

## 参考文献

[1] Harnessing AI to Build Virtual Cells, europepmc, 2026-04-14, https://doi.org/10.64898/2026.04.11.717183
[2] The 2025 Westlake Autumn Symposium for AI Proteomics and Virtual Cell., Genomics, proteomics & bioinformatics, 2026-08-01, https://doi.org/10.1093/gpbjnl/qzag022
[3] Toward AI Virtual Cells for Hepatology: Representation, Generation, Dynamics, and Intervention in Single-Cell Models., Clinical and molecular hepatology, 2026-09-17, https://doi.org/10.3350/cmh.2026.0820
[4] An operational perturbation proteomics-based virtual cell model., Nature, 2026-09-09, https://doi.org/10.1038/s41586-026-11001-9
[5] Integrative AI-Enabled Virtual Cell Modeling Reveals a Clinically Relevant Latent Effector State of Human CD8⁺ T Cells Undetectable by Conventional Analyses, europepmc, 2026-07-25, https://doi.org/10.64898/2026.07.22.739582
[6] An Empirical Comparison of Virtual Cell Models: Perturbation Prediction, Representation, and the Baseline Gap, europepmc, 2026-07-22, https://doi.org/10.21203/rs.3.rs-10434123/v
