# 专题调研：虚拟细胞 virtual cell（2026-03-21 ~ 2026-09-17）

# 虚拟细胞（Virtual Cell）近 6 个月研究调研报告

## 摘要（TL;DR）

1. **领域已从"能不能预测"进入"预测有没有用"的清算期**：多篇工作（[1][3][16][20][31][42][53]）集中质疑现有虚拟细胞模型的评估效度，指出高维噪声掩盖信号、基线差距被忽视、未见干预的几何结构坍缩，甚至无神经网络的解析校准即可匹配或超越深度模型 [42]。
2. **蛋白质组与多模态成为新前沿**：Nature 发表基于 3800 万+ 时序蛋白丰度测量的 ProteinTalks 虚拟细胞模型 [9]，标志虚拟细胞从转录组单模态向蛋白动力学扩展；多模态扩散框架 MultiVCDiff 实现形态+转录组联合零样本预测 [35]。
3. **评测基础设施快速成型**：VCBench [2]、AssayBench [27]、scArchon [58]、PerturbHD [3]、SBB 原则 [1] 等在半年内密集出现，覆盖能力维度、实验级表型、可复现平台与科学发现价值。
4. **扰动响应建模方法高度分化**：flow matching（OCOO-T [14][22]）、离散扩散（Lingshu-Cell [23]、D²R² [46]）、最优传输（scPILOT [30]）、响应分解（[44][48]）、因果潜动力学 [47]、RL 后训练 [21] 等路线并行，尚无统一赢家。
5. **世界模型/闭环智能体成为组织性概念**：VCHarness [5]、CellScientist [24]、AblateCell [38]、Chreode [25]、CellOS [36] 把虚拟细胞重新表述为可迭代、可自审的"细胞世界模型"。
6. **衰老与免疫方向出现直接可用的资产**：Insilico 推出 Virtual Aging Cell 网页与多智能体 VAC 生成平台（产业新闻），学术侧 PACE 免疫衰老评分在 434 名老年供体队列中优于 5 种衰老时钟 [34]。
7. **数据可靠性成为瓶颈级问题**：7170 个扰动中 65% 被判为不可靠 [33]；癌细胞系异质性使大规模虚拟筛选保真度从正常细胞 PCC 0.480 降至 0.296 [32]。
8. **产业侧以平台叙事为主**：GenBio AI 的"人类细胞世界模型"、Turbine 2500 万美元 B 轮、Insilico 衰老虚拟细胞等，多为融资/发布类新闻，缺少可核验的技术细节。

---

## 背景与定义

虚拟细胞（virtual cell）在本期文献中已从早期"多尺度生化模拟平台"（E-Cell、CellPACK 等，见综述 [15]）演化为以**大规模单细胞/空间多组学 + 基础模型 + 扰动响应预测**为核心的计算框架：其目标是在统一模型中表示细胞状态、生物学背景与扰动响应，从而在硅预测药物、基因与环境的效应 [18]。与之并行的是"细胞世界模型"（cell world model）这一更严格的形式化提法——要求模型维持细胞状态、支持干预条件下的状态转移、并具备时变结构，而非仅做静态表征或对照-处理映射 [19][25][36]。本期多篇工作（[7][12][19]）强调，虚拟细胞的价值不应仅由预测精度衡量，而应落到机制可解释性、跨情境泛化与科学发现贡献上 [3]。

---

## 关键时间线

**2026 年 3 月**
- CellFluxRL 用强化学习对 CellFlux 图像生成模型做后训练，引入 7 种生物/结构/形态奖励 [21]。
- Lingshu-Cell 提出掩码离散扩散的生成式细胞世界模型，覆盖约 18000 个基因 [23]。

**2026 年 4 月**
- SBB 评估原则（Signal / Bounds / Baselines）提出 [1]。
- PerturbHD 框架主张以科学发现价值评估虚拟细胞 [3]。
- VCHarness 自主 AI 智能体自动构建扰动响应模型 [5]。
- AblateCell"先复现后消融"智能体面向虚拟细胞仓库 [38]。
- AROMA 多模态增强推理用于遗传扰动建模 [39]。
- T-World 虚拟人心肌细胞 I/II 发表，从细胞到器官尺度 [50][60]。
- 零样本泛化基准挑战赛（Virtual Cell Challenge 2026）公布 [10]。

**2026 年 5 月**
- CellScientist 双空间层次化 LLM 编排实现闭环精化 [24]。
- Chreode 一步式细胞世界模型 [25]。
- AssayBench 实验级 LLM/智能体基准 [27]。
- StateXDiff 状态情境化多模态扩散 [40]。
- 可解释虚拟细胞蓝图在 Nature Reviews Genetics 重新审视 [7]。
- scArchon 可复现基准平台发表于 Genome Biology [58]。

**2026 年 6 月**
- VCBench 多维基准发布，评估 5 个基础模型 [2]。
- OCOO-T 极简 flow matching 虚拟细胞模型 [14][22]。
- CellOS 多视图联合嵌入基础模型 [36]。
- 潜表征基因重构基准 [37]。
- CisTransCell 零样本扰动预测框架 [45]。
- 单细胞基础模型零样本表征系统评测（1607 数据集/2180 万细胞）[57]。

**2026 年 7 月**
- UniPert-G2CP 桥接遗传与化学筛选（Cell）[13]。
- 整合式 AI 虚拟细胞识别 CD8⁺ T 细胞潜在效应状态 [11]。
- 下一代虚拟细胞综述提出闭环靶点发现 [12]。
- 统一基准比较 11 方法/6 任务/9 数据集 [16]。
- scDifformer 扩散后训练 Transformer [17]。
- 虚拟细胞世界模型三差距三实验路线图 [19]。
- 无神经网络解析校准 AMM-SimWMag 匹配/超越深度模型 [42]。
- 扰动响应分解框架 [44]。
- 表格基础模型作为扰动预测器 [59]。
- CENO 基因组世界模型 [61]。

**2026 年 8 月**
- ProteinTalks 时序扰动蛋白质组虚拟细胞模型（Nature）[9]。
- 虚拟细胞挑战赛零样本泛化基准（Cell）[10]。
- 干预几何压缩（IGC）诊断分析 [31]。
- 癌细胞系异质性瓶颈分析 [32]。
- 扰动可靠性分类（65% 不可靠）[33]。
- 免疫衰老自审 AI 发现框架（PACE/CellQ）[34]。
- MultiVCDiff 多模态扩散 [35]。
- 人引导因果知识注入 [28]。
- D²R² 离散扩散+调控强化 [46]。
- DeMixPert 高斯混合分解 [48]。
- CFM-GP 条件流匹配 [43]。
- 单细胞扰动预测模型系统比较（Science Advances，25 数据集/13 方法）[53]。
- 自回归 Transformer 单细胞生成 [63]。

**2026 年 9 月**
- 大规模并行合成基因图谱 Chronos 首个公开数据集（约 6 万顺式调控元件 × 约 50 细胞系）[51]。
- PHAROS 将扰动模型转为靶向药物组合筛选 [52]。
- 单细胞扰动预测模型系统比较（Science Advances）[53]。
- 肝病虚拟细胞建模路径综述 [8]。

**产业新闻时间线（据提供新闻）**
- 2 月 24 日：Turbine 完成 2500 万美元 B 轮，扩展虚拟生物学平台与免疫学。
- 6 月 1 日：国际团队发布"虚拟酵母"路线图；"虚拟细胞"将原始数据转为预测模型的报道。
- 6 月 9 日：虚拟细胞走向多尺度预测复杂生物学。
- 8 月 13 日：Insilico Medicine 将生物学年龄引入虚拟细胞研究，推出 Virtual Aging Cell 网页并预览多智能体 VAC 生成平台；同期"科学家竞逐虚拟细胞"报道。
- 8 月 18 日：GenBio AI 构建首个"人类细胞世界模型"。
- 8 月 26 日：Nobel 得主 David Baker 与 GenBio AI 合作瞄准虚拟细胞。
- 8 月 27 日：Jacksonville 学生构建癌症护理 AI 工具。
- 9 月 8 日 / 9 月 12 日：AI 模型预测乳腺癌最佳药物；AI 虚拟细胞用蛋白动力学预测个体化乳腺癌治疗。
- 9 月 16 日：UAE 展示可模拟药物响应的 AI 细胞模型。

---

## 使用的技术

### 1. 生成式建模：扩散 / 流匹配 / 离散扩散

- **OCOO-T** [14][22]：极简 flow matching 模型，直接预测单细胞对遗传、化学、细胞因子扰动的转录响应，刻意去除辅助细胞状态编码器、层次 VAE 与基因互作先验以提升可扩展性。
- **Lingshu-Cell** [23]：掩码离散扩散，在适配单细胞稀疏非序列特性的离散 token 空间学习转录组状态分布，覆盖约 18000 个基因，支持扰动条件模拟。
- **scDifformer** [17]：上下文感知 Transformer + 去噪扩散模块，三阶段（掩码语言模型预训练、扩散后训练、下游微调），在 7 个组织上基准测试，针对稀疏噪声数据去噪与跨研究泛化。
- **D²R²** [46]：掩码离散扩散 + 调控策略模块，将扰动预测重构为调控引导的逐基因渐进生成，显式建模基因响应生成顺序。
- **MultiVCDiff** [35]：统一多模态生成扩散，从化学或遗传扰动同时预测细胞形态图像与转录组谱；在 1118 个化学 + 130 个遗传扰动语料上训练，严格零样本下优于单模态基线。
- **StateXDiff** [40]：细胞状态情境化多模态扩散，先学解耦多模态细胞状态表征，面向 OOD 药物响应预测。
- **CellFluxRL** [21]：用 RL 对 CellFlux 图像生成模型后训练，7 种奖励覆盖生物功能、结构有效性、形态正确性；所有奖励指标均优于 CellFlux，测试时扩展进一步提升。

### 2. 扰动响应分解与迁移

- **UniPert-G2CP** [13]：两阶段深度学习框架，统一多模态分子扰动（因）表示并实现遗传→化学扰动表型（果）迁移学习，在大规模遗传与化学筛选数据上验证。
- **扰动响应分解框架** [44]：将转录响应显式拆为全局、扰动特异、细胞系特异、扰动×细胞系交互四成分，在 4 个多细胞系 CRISPRi Perturb-seq 筛选上应用；结论是泛化依赖成分识别而非模型复杂度。
- **DeMixPert** [48]：高斯混合分解为基础状态依赖系统响应、扰动特异响应、随机群体变异三部分，针对 OOD 预测中共享模式掩盖弱扰动特异信号的问题。
- **scPILOT** [30]：深度生成模型 + 最优传输，判别器辅助训练学习生成式隐表示并分离扰动效应，将已观察扰动响应迁移到未见生物情境（细胞类型、患者、物种）。
- **CFM-GP** [43]：条件流匹配，学习对照→扰动状态的连续向量场并显式以细胞类型为条件，在 5 个单细胞扰动数据集上验证跨细胞类型预测。
- **GeneGeoFlow** [41]：控制锚定残差流匹配，条件化于生物网络导出的基因几何，但仅把网络几何作为条件信号而非同时构建表示与介导交互，面向未见遗传扰动与药物组合。

### 3. 基础模型与表征学习

- **CellOS** [36]：多视图基础模型，从配对表达与感知视图学习细胞表征，三阶段训练整合因果细胞句子语言建模、保函数稠密到专家混合扩展、潜在空间对齐。
- **CellxPert** [49]：多组学基础模型，统一编码转录组、染色质可及性、表面蛋白，并将 MERFISH 与成像质谱流式作为 2D/3D 空间视觉层纳入；开箱支持 154 类细胞类型注释（迄今最大标签空间）、LoRA 微调、in-silico 扰动全基因组转录响应预测。
- **scYeast** [55]：首个酵母单细胞转录组基础模型，非对称并行架构将转录调控信息注入 Transformer 注意力，零样本任务表现良好。
- **表格基础模型** [59]：TabICL、TabPFN 等通用预训练表格模型在四种设定（细胞级跨类型、5 细胞系 Perturb-seq 伪批量、原代 CD4⁺ T 细胞全基因组 CRISPR、胚胎级）下与 PRESAGE、scGPT、scLAMBDA、STACK、Prophet 等专用架构竞争。
- **CENO** [61]：基因组世界模型，长上下文核苷酸分辨率状态、反事实突变打分、同源序列条件生成，统一序列理解与设计。

### 4. 世界模型与智能体闭环

- **VCHarness** [5]：AI 编码智能体 + 多模态生物基础模型，在庞大架构/训练流程空间中迭代生成、评估、精炼扰动响应模型，替代专家数月手动设计。
- **CellScientist** [24]：双空间层次框架，耦合高层假设空间与低层可执行实现空间，支持跨层反馈传播与针对性修订。
- **AblateCell** [38]：先自动配置环境、解决依赖与数据问题、重跑官方评估端到端复现基线，再执行闭环消融检验组件贡献。
- **Chreode** [25]：结构化残差转移算子实现动作条件一步状态转移，将分布演化从推理时移至训练时，保留 Waddington 式分解（下坡景观流、切向旋转动态、随机扩散）。
- **PHAROS** [52]：将预训练扰动模型转为靶向药物组合搜索引擎，先预测单药群体影响再串联模拟组合并打分搜索，无需重训练；在两个组合扰动数据集中恢复精确或机制匹配双药响应。

### 5. 机制/多尺度与领域专用模型

- **ProteinTalks** [9]：从系统扰动乳腺癌细胞系生成 3800 万+ 时序蛋白丰度测量，新预训练框架从时序蛋白轨迹学习可迁移动态隐表征，建模蛋白对扰动的条件性响应，用于治疗响应预测与在硅药物发现。
- **T-World 虚拟人心肌细胞** [50][60]：数据驱动微分方程描述性别特异兴奋-收缩耦联、机械收缩、β 肾上腺素能信号；可复现所有主要细胞心律失常机制，并嵌入临床影像双心室电生理与机电模型做器官级模拟与药物安全评估。
- **整合式 AI 虚拟细胞框架** [11]：将 scRNA-seq 与配对 TCR-seq 整合进 C2S 规模基础模型，把每个 T 细胞编码为含转录、信号、克隆特征的功能身份，识别出 ICI 治疗中临床相关但传统分析检测不到的 CD8⁺ T 细胞潜在效应状态。
- **PACE / CellQ 自审框架** [34]：表型验证器 PACE 将免疫衰老分解为 10 个方向性评分模块，在 4 个 PBMC 队列筛选跨队列稳定性，并在 434 名老年供体独立队列中优于 5 种衰老时钟；虚拟细胞验证器 CellQ 用多模态 LLM 将单细胞转录组压缩为 8 个离散 token。

---

## 数据

- **时序蛋白质组**：3800 万+ 时序蛋白丰度测量，来自系统扰动的乳腺癌细胞系 [9]。
- **单细胞多组学**：scRNA/ATAC/CITE-seq/MERFISH/IMC 统一表示，154 类细胞类型标签空间 [49]；scRNA-seq + 配对 TCR-seq [11]。
- **大规模扰动筛选**：162 细胞系 × 32039 化合物 × 12328 基因输出 [32]；1118 化学 + 130 遗传扰动、4 数据集 [35]；4 个多细胞系 CRISPRi Perturb-seq 筛选 [44]；两个组合扰动数据集 [52]。
- **基准数据集集合**：11 方法/6 任务/9 数据集 [16]；25 数据集/13 方法 [53]；6 个 scRNA-seq 数据集 [58]；29 数据集/7170 扰动 [33]；1607 数据集/2180 万细胞 [57]。
- **合成基因图谱**：Chronos 平台首个公开数据集，Penta-47x27K 与 Tria-47x28K 两模块，约 6 万个紧凑顺式调控元件在约 50 个细胞系中测量，细胞系由 Tahoe Tx 提供 [51]。
- **临床/队列数据**：4 个 PBMC 队列 + 434 名老年供体独立队列 [34]。
- **挑战赛数据**：Arc 生成、包含未见细胞系的新数据集，用于基因敲低响应零样本预测 [10]。
- **图像/形态数据**：CellFlux 图像生成模型及其 RL 后训练 [21]；细胞形态图像 + 转录组三模态语料 [35]。
- **其他**：酵母单细胞转录组 [55]；约 18000 基因的单细胞转录组 [23]；SciPlex3 24 小时基准 [62]。

---

## 应用场景

### 药物发现与靶点识别
- PerturbHD 主张以 AI 辅助 hit 发现的实际贡献评估模型 [3]；PHAROS 直接输出靶向药物组合 [52]；UniPert-G2CP 桥接遗传与化学筛选 [13]；ProteinTalks 面向在硅药物发现与治疗响应预测 [9]；MultiVCDiff 面向零样本虚拟药物筛选 [35]；CellPrism 提供扰动空间可视化分析 [26]。

### 免疫学与免疫衰老
- 整合式 AI 虚拟细胞识别 CD8⁺ T 细胞潜在效应状态，用于 ICI 治疗响应 [11]；PACE/CellQ 自审框架面向免疫衰老药物发现，PACE 在 434 名老年供体队列中优于 5 种衰老时钟 [34]。

### 复杂疾病与器官尺度
- 肝病虚拟细胞建模三条路线（生成表征、动力学转运、基础模型迁移）[8]；T-World 从人心肌细胞到双心室器官级模拟，用于药物安全评估 [50][60]；下一代虚拟细胞综述指向复杂疾病闭环靶点发现 [12]。

### 表型筛选与实验级预测
- AssayBench 面向 LLM/智能体的实验级虚拟细胞基准，结合异质文本输入与多样表型输出 [27]；CellFluxRL 面向虚拟细胞图像生成与药物发现 [21]。

### 调控设计与合成生物学
- CENO 面向进化序列解读与可编程调控元件设计 [61]；Chronos 合成基因图谱服务虚拟细胞建模社区 [51]；scYeast 面向酵母细胞建模 [55]。

### 临床导航与手术
- "Golden Eyes 3.0" 集成图卷积虚拟细胞模型与近红外光谱，用于肿瘤边界识别导航 [54]。

### 器官芯片闭环
- 器官芯片 + AI 虚拟细胞闭环概念框架，指向下一代生物医学 [29]。

---

## 评测与可靠性反思

本期最突出的主题是**对虚拟细胞评测体系的系统性批判**：

- **信号被噪声掩盖**：SBB 原则指出高维基因表达空间噪声掩盖真实性能差异，主张引入诊断性元指标并推广基于差异表达基因的加权/过滤 [1]。
- **基准碎片化**：VCBench 将四个独立框架综合为七个能力维度，评估 5 个基础模型后发现多尺度整合与计算机实验无法作为端到端任务测试，其余 5 维可评估，且现有基准掩盖模型相对简单基线的优势 [2]。
- **基线差距**：统一基准汇集 5 类模型家族 11 种方法、6 任务家族、9 数据集，固定数据划分/预处理/指标后，发现因训练与评估高度异质，真实能力仍不清晰 [16]。
- **无神经网络即可匹配深度模型**：AMM-SimWMag 将 scGen 优势分解为按类型响应幅度与按基因响应方向两个无泄漏解析成分，加逐基因仿射矩匹配，在 4 数据集、3 生物学体系、2 种 LOCO 轴上以数据集分层 Stouffer 符号秩检验评估 9 项指标，匹配或超越深度模型，且仅用 CPU [42]。
- **未见干预的几何坍缩**：干预几何压缩（IGC）分析发现未见干预的全局与局部几何减弱、干预间方差下降并出现谱坍缩，失败并非主要源于响应空间容量，而是缺失几何集中于少数从已知干预学到的残差响应方向 [31]。
- **数据可靠性**：7170 个扰动中仅 24% 特异性、11% 共享型、65% 不可靠；将质量标签应用于已发表基准后发现模型比较结果依赖扰动质量，使用可靠扰动训练可改善性能与评估 [33]。
- **细胞系异质性瓶颈**：扩展到 162 细胞系/32039 化合物/12328 基因后，正常与原代细胞系预测保真度显著高于癌细胞系（平均 PCC 0.480 vs 0.296，p=3.93e-11）[32]。
- **性能依赖效应大小**：25 数据集/13 方法/24 指标的大规模比较发现性能强烈依赖扰动效应大小 [53]。
- **真实场景评估缺失**：标准化模块化基准框架在未见细胞背景、未见扰动、跨数据集场景下评估，指出现有模型在真实生物学系统中是否有意义仍不清晰 [20]。
- **表征选择被低估**：潜表征基因重构基准指出表征选择常被视为实现细节而非主要建模决策，但忠实重构对生物学解释至关重要 [37]。
- **基础模型表征效用有条件**：1607 数据集/2180 万细胞/20 方法/6 任务的零样本评测显示单细胞基础模型表征效用高度依赖上下文 [57]。
- **世界模型三差距**：表征≠动态、预测≠干预、多模态≠多尺度世界建模 [19]。
- **科学发现价值导向**：PerturbHD 主张从科学发现价值而非预测精度评价模型 [3]。

---

## 产业动态

- **Turbine**：完成 2500 万美元 B 轮融资，用于虚拟生物学平台与免疫学扩展（2 月 24 日新闻）。
- **GenBio AI**：构建首个"人类细胞世界模型"（8 月 18 日）；Nobel 得主 David Baker 加入瞄准虚拟细胞（8 月 26 日）。
- **Insilico Medicine**：将生物学年龄引入虚拟细胞研究，推出 Virtual Aging Cell 网页并预览多智能体驱动的 VAC 生成平台（8 月 13/14 日新闻）。
- **UAE**：展示可模拟药物响应的 AI 细胞模型（9 月 16 日）。
- **乳腺癌个体化治疗**：AI 虚拟细胞用蛋白动力学预测个体化乳腺癌治疗（9 月 12 日）；AI 模型预测哪种乳腺癌药物最有效（9 月 8 日）。
- **虚拟酵母路线图**：国际团队发布（6 月 1 日）。
- **多尺度趋势报道**：虚拟细胞走向多尺度预测复杂生物学（6 月 9 日）；"虚拟细胞"将原始数据转为预测模型（6 月 1 日）；科学家竞逐虚拟细胞（8 月 13 日）。
- **其他**：Jacksonville 学生构建癌症护理 AI 工具（8 月 27 日）；Agentic AI、虚拟细胞、LNP 疫苗佐剂、工程化器官与并购综述（3 月 26 日）。

> 注：以上均为新闻标题级信息，缺少可核验的技术细节、数据规模与同行评议，建议仅作方向性参考。

---

## 趋势结论与空白

1. **评测正在成为独立研究领域，但"科学发现价值"评估仍缺可操作标准**：PerturbHD [3] 提出方向，但尚无跨团队采纳的发现级基准；AssayBench [27] 是早期尝试，覆盖的实验终点仍有限。
2. **蛋白质组虚拟细胞刚起步，多模态蛋白-转录-形态联合建模几乎空白**：ProteinTalks [9] 是单点突破，未见蛋白组与空间转录组、甲基化、代谢组的统一虚拟细胞框架。
3. **衰老方向的虚拟细胞学术工作稀缺**：仅 [34] 直接涉及免疫衰老，且以评分/验证器形式出现；Insilico 的 Virtual Aging Cell 为产业侧动作。**多模态健康衰老模型所需的跨队列校正、缺失模态处理、增量学习在虚拟细胞文献中几乎未被系统研究**——这是合作项目最直接的空白。
4. **扰动可靠性 [33] 与细胞系异质性 [32] 已被识别为瓶颈，但尚无"数据质量感知"的建模方法**：现有方法仍默认训练标签为真值。
5. **未见干预的几何坍缩 [31] 缺少针对性架构解决方案**：诊断已明确，修复方法未见。
6. **类器官 + 组学 + 虚拟细胞的闭环在学术文献中缺位**：仅 [29] 提出器官芯片-AI 虚拟细胞闭环概念，无实证工作。
7. **持续/增量学习在虚拟细胞中几乎无人做**：新数据进来后如何持续矫正统一模型 vs 每模态独立训练再整合，本期文献未提供方法学答案。
8. **世界模型形式化 [19][25][36] 与评测实践脱节**：概念框架已提出，但三差距对应的三个实验尚无团队报告结果。
9. **跨物种泛化仅在 VCBench [2] 作为能力维度被提及**，scYeast [55] 是单物种案例，跨物种虚拟细胞迁移方法缺失。
10. **LLM/智能体在虚拟细胞中的角色集中在"编排与复现"（[5][24][38]），而非科学假设生成**：self-improving / RSI / RLVR 在虚拟细胞语境下尚无实质进展。
11. **临床转化证据薄弱**：除 T-World [60] 与 [11] 外，多数工作止于基准指标，缺少前瞻性临床或湿实验验证。
12. **数据发布侧出现积极信号**：Chronos [51] 首个公开数据集与 Virtual Cell Challenge 2026 [10] 的未见细胞系设定，可能推动社区从"刷榜"转向真实泛化。

## 参考文献

[1] Signal, Bounds, and Baselines: Principles for Evaluating Virtual Cell Perturbation Models *europepmc*, 2026-04-22, https://doi.org/10.64898/2026.04.20.719650
[2] VCBench: A Multi-Dimensional Benchmark for Single-Cell Foundation Models *europepmc*, 2026-06-23, https://doi.org/10.64898/2026.06.18.733146
[3] Are Current AI Virtual Cell Models Useful for Scientific Discovery? *europepmc*, 2026-04-25, https://doi.org/10.64898/2026.04.23.719015
[4] A Multi-modal LLM-Knowledge Fusion Framework for Predicting Single-cell Genetic Perturbation Effects *europepmc*, 2026-04-28, https://doi.org/10.64898/2026.04.24.720560
[5] Harnessing AI to Build Virtual Cells *europepmc*, 2026-04-14, https://doi.org/10.64898/2026.04.11.717183
[6] The 2025 Westlake Autumn Symposium for AI Proteomics and Virtual Cell. *Genomics, proteomics & bioinformatics*, 2026-08-01, https://doi.org/10.1093/gpbjnl/qzag022
[7] Revisiting the blueprint for an interpretable virtual cell. *Nature reviews. Genetics*, 2026-05-01, https://doi.org/10.1038/s41576-026-00940-8
[8] Toward AI Virtual Cells for Hepatology: Representation, Generation, Dynamics, and Intervention in Single-Cell Models. *Clinical and molecular hepatology*, 2026-09-17, https://doi.org/10.3350/cmh.2026.0820
[9] An operational perturbation proteomics-based virtual cell model. *Nature*, 2026-09-09, https://doi.org/10.1038/s41586-026-11001-9
[10] Virtual Cell Challenge 2026: Benchmarking zero-shot generalization across cellular contexts. *Cell*, 2026-08-26, https://doi.org/10.1016/j.cell.2026.08.004
[11] Integrative AI-Enabled Virtual Cell Modeling Reveals a Clinically Relevant Latent Effector State of Human CD8⁺ T Cells Undetectable by Conventional Analyses *europepmc*, 2026-07-25, https://doi.org/10.64898/2026.07.22.739582
[12] The next-generation virtual cell: From spatiotemporal transcriptomic modeling to closed-loop target discovery in complex diseases. *Life sciences*, 2026-07-24, https://doi.org/10.1016/j.lfs.2026.124600
[13] UniPert-G2CP bridges genetic and chemical screens from molecular representation to phenotype modeling. *Cell*, 2026-07-25, https://doi.org/10.1016/j.cell.2026.06.005
[14] OCOO-T : A SIMPLE AND SCALABLE VIRTUAL CELL MODEL FOR TRANSCRIPTIONAL PERTURBATION RESPONSE PREDICTION *europepmc*, 2026-06-11, https://doi.org/10.64898/2026.06.08.731000
[15] Virtual cell: Current perspectives and future prospects. *The Journal of international medical research*, 2026-05-27, https://doi.org/10.1177/03000605261425080
[16] An Empirical Comparison of Virtual Cell Models: Perturbation Prediction, Representation, and the Baseline Gap *europepmc*, 2026-07-22, https://doi.org/10.21203/rs.3.rs-10434123/v1
[17] scDifformer: diffusion-based post-training for virtual cell modeling across large-scale single-cell data. *Nucleic acids research*, 2026-07-01, https://doi.org/10.1093/nar/gkag706
[18] Virtual cell construction for artificial intelligence-driven drug discovery. *British journal of pharmacology*, 2026-07-10, https://doi.org/10.1111/bph.70585
[19] What Makes a Virtual Cell a World Model? Three Gaps, Three Experiments, and a Roadmap *europepmc*, 2026-07-21, https://doi.org/10.21203/rs.3.rs-10404367/v1
[20] Benchmarking virtual cell models for in-the-wild perturbation response *arxiv*, 2026-04-30, https://arxiv.org/abs/2604.27646v1
[21] CellFluxRL: Biologically-Constrained Virtual Cell Modeling via Reinforcement Learning *arxiv*, 2026-03-23, https://arxiv.org/abs/2603.21743v4
[22] OCOO-T : A Simple and Scalable Virtual Cell Model for Transcriptional Perturbation Response Prediction *arxiv*, 2026-06-11, https://arxiv.org/abs/2606.12838v2
[23] Lingshu-Cell: A generative cellular world model for transcriptome modeling toward virtual cells *arxiv*, 2026-03-26, https://arxiv.org/abs/2603.25240v1
[24] CellScientist: Dual-Space Hierarchical Orchestration for Closed-Loop Refinement of Virtual Cell Models *arxiv*, 2026-05-08, https://arxiv.org/abs/2605.07335v1
[25] Chreode: A Cell World Model for One-Step Temporal Dynamics and Perturbation Prediction *arxiv*, 2026-05-27, https://arxiv.org/abs/2605.28111v1
[26] CellPrism: A Visual Analytics System for Exploring AI-Driven Virtual Cells in Drug Discovery *arxiv*, 2026-08-03, https://arxiv.org/abs/2608.01669v2
[27] AssayBench: An Assay-Level Virtual Cell Benchmark for LLMs and Agents *arxiv*, 2026-05-11, https://arxiv.org/abs/2605.10876v1
[28] Human-Guided Causal Knowledge Injection for Virtual Cells *arxiv*, 2026-08-09, https://arxiv.org/abs/2608.08430v1
[29] The organ-on-a-chip-AI virtual cell loop: a path toward next‑generation biomedicine. *Science bulletin*, 2026-07-30, https://doi.org/10.1016/j.scib.2026.07.080
[30] Predicting Single-Cell Perturbation Responses Across Biological Contexts With a Deep Generative Model Integrating Optimal Transport. *Advanced science (Weinheim, Baden-Wurttemberg, Germany)*, 2026-08-29, https://doi.org/10.1002/advs.77461
[31] Virtual-cell models compress unseen intervention geometry through a target-specific generalization bottleneck *europepmc*, 2026-08-24, https://doi.org/10.64898/2026.08.21.746243
[32] Cancer Cell Line Heterogeneity Imposes a Primary Bottleneck for Virtual Perturbation Screening at Scale *europepmc*, 2026-08-15, https://doi.org/10.64898/2026.08.10.743942
[33] Reliable single-cell perturbations explain and improve model performance *europepmc*, 2026-08-12, https://doi.org/10.64898/2026.08.11.744177
[34] Virtual-cell verification enables self-auditing AI discovery for immune rejuvenation *europepmc*, 2026-08-11, https://doi.org/10.64898/2026.08.04.742916
[35] A generative framework for predicting cellular morphological and transcriptomic perturbation responses. *Cell reports methods*, 2026-05-21, https://doi.org/10.1016/j.crmeth.2026.101459
[36] CellOS: Learning a World Model of Cellular State through Joint Embedding Prediction *europepmc*, 2026-06-23, https://doi.org/10.64898/2026.06.18.733163
[37] Benchmarking gene expression reconstruction from single-cell latent representations *europepmc*, 2026-06-18, https://doi.org/10.64898/2026.06.15.731445
[38] AblateCell: A Reproduce-then-Ablate Agent for Virtual Cell Repositories *arxiv*, 2026-04-21, https://arxiv.org/abs/2604.19606v2
[39] AROMA: Augmented Reasoning Over a Multimodal Architecture for Virtual Cell Genetic Perturbation Modeling *arxiv*, 2026-04-22, https://arxiv.org/abs/2604.20263v1
[40] StateXDiff: Cell State-Contextualized Multimodal Diffusion for Single-Cell Perturbation Prediction *arxiv*, 2026-05-15, https://arxiv.org/abs/2605.16104v1
[41] Control-Anchored Residual Flow Matching Conditioned on Gene Geometry for Virtual Cell Perturbation Modeling *arxiv*, 2026-08-07, https://arxiv.org/abs/2608.06824v1
[42] A Neural-Network-Free Calibration Matches or Beats Deep Single-Cell Perturbation Response Models Across Four Datasets. *Genes*, 2026-07-17, https://doi.org/10.3390/genes17070816
[43] CFM-GP: unified conditional flow matching to learn gene perturbation across cell types. *NAR genomics and bioinformatics*, 2026-08-10, https://doi.org/10.1093/nargab/lqag087
[44] Perturbation response decomposition enables biologically aligned generalization to unseen perturbations and cellular contexts *europepmc*, 2026-07-27, https://doi.org/10.64898/2026.07.24.740459
[45] CisTransCell: Single-Cell Perturbation Prediction via Gene Function, Regulatory Control, and Cellular Context *arxiv*, 2026-06-10, https://arxiv.org/abs/2606.13713v1
[46] $D^{2}R^{2}$: Discrete Diffusion with Regulation Reinforcement for Single-Cell Perturbation Prediction *arxiv*, 2026-08-15, https://arxiv.org/abs/2608.15288v1
[47] Learning Latent Dynamical Causal Processes for Single-Cell Perturbation Prediction *arxiv*, 2026-05-25, https://arxiv.org/abs/2605.25581v1
[48] DeMixPert: Decomposed Response Modeling with Gaussian Mixtures for OOD Single-Cell Perturbation Prediction *arxiv*, 2026-08-24, https://arxiv.org/abs/2608.23114v1
[49] CellxPert: Inference-Time MCMC Steering of a Multi-Omics Single-Cell Foundation Model for In-Silico Perturbation *arxiv*, 2026-04-30, https://arxiv.org/abs/2605.00930v1
[50] T-World Virtual Human Cardiomyocyte. I. Development, Validation, and Cell Arrhythmogenesis. *Circulation research*, 2026-04-07, https://doi.org/10.1161/circresaha.125.328073
[51] A massively parallel synthetic gene atlas for learning compact cis-regulatory grammar across cellular contexts *europepmc*, 2026-09-14, https://doi.org/10.64898/2026.09.13.751267
[52] PHAROS: turning single-cell perturbation models into target-directed drug-combination screens *europepmc*, 2026-09-10, https://doi.org/10.64898/2026.09.08.749477
[53] A systematic comparison of single-cell perturbation response prediction models. *Science advances*, 2026-09-09, https://doi.org/10.1126/sciadv.aed3414
[54] [Multi-modal tumor boundary clustering recognition based on artificial intelligence virtual cells and near-infrared surgical field]. *Sheng wu yi xue gong cheng xue za zhi = Journal of biomedical engineering = Shengwu yixue gongchengxue zazhi*, 2026-08-01, https://doi.org/10.7507/1001-5515.202512069
[55] scYeast: a biological-knowledge-guided foundation model on yeast single-cell transcriptomics. *Synthetic and systems biotechnology*, 2026-07-16, https://doi.org/10.1016/j.synbio.2026.05.014
[56] Decoding Single-Cell Omics of Perturbation Responses Using DeSCOPE *europepmc*, 2026-04-15, https://doi.org/10.64898/2026.04.13.718147
[57] Context-dependent utility and robustness of pretrained single-cell foundation model representations across analytical tasks *europepmc*, 2026-06-23, https://doi.org/10.64898/2026.06.18.733285
[58] scArchon: a scalable benchmarking framework for assessing single-cell perturbation models. *Genome biology*, 2026-05-12, https://doi.org/10.1186/s13059-026-04104-z
[59] Tabular Foundation Models Are Competitive Cellular Perturbation Predictors Across Biological Scales *europepmc*, 2026-07-01, https://doi.org/10.64898/2026.06.28.735106
[60] T-World Virtual Human Cardiomyocyte. II. Organ-Scale Simulations and Applications. *Circulation research*, 2026-04-08, https://doi.org/10.1161/circresaha.125.328123
[61] CENO: A Genome-Scale World Model for Evolutionary Sequence Interpretation and Programmable Regulatory Design *europepmc*, 2026-07-30, https://doi.org/10.64898/2026.07.28.741284
[62] Modeling Cell-Cycle-Aware Single-Cell Drug Perturbation Responses *arxiv*, 2026-06-29, https://arxiv.org/abs/2606.30695v2
[63] Scaling an Autoregressive Transformer for Single-Cell Generation *arxiv*, 2026-08-03, https://arxiv.org/abs/2608.02961v2
[64] SAVE: A Generalizable Framework for Multi-Condition Single-Cell Generation with Gene Block Attention *arxiv*, 2026-04-18, https://arxiv.org/abs/2604.16776v1
[65] PerturbCellRL: Verifier-Guided Reinforcement Learning for Single-Cell Perturbation Prediction *arxiv*, 2026-06-26, https://arxiv.org/abs/2606.27752v1
[66] Evaluating the role of pretraining dataset size and diversity on single-cell foundation model performance. *Nature methods*, 2026-06-09, https://doi.org/10.1038/s41592-026-03120-y
[67] Counterfactual Diffusion Modeling Enables Spatially Targeted Reprogramming of Tissue Microenvironments. *Biology*, 2026-07-08, https://doi.org/10.3390/biology15141097
[68] Universal cell embedding provides a foundation model for cell biology. *Nature*, 2026-07-08, https://doi.org/10.1038/s41586-026-10689-z
[69] Generative atlasing in universal gene expression space defines cell types and microenvironment spectra during disease progression *europepmc*, 2026-09-04, https://doi.org/10.21203/rs.3.rs-10838361/v1
[70] PertAdapt: unlocking single-cell foundation models for genetic perturbation prediction via condition-sensitive adaptation. *Bioinformatics (Oxford, England)*, 2026-07-01, https://doi.org/10.1093/bioinformatics/btag307
[71] Cellfm-datasets: A Unified Data Infrastructure for Single-Cell and Spatial Transcriptomics Foundation Model Pretraining *europepmc*, 2026-06-14, https://doi.org/10.64898/2026.06.11.731508
[72] Finetuning masking challenges narrow-task evaluation of cell foundation models *europepmc*, 2026-06-06, https://doi.org/10.64898/2026.06.04.730272
[73] Evaluating the learnability of single-cell large language models on multiple tasks. *BMC genomics*, 2026-06-05, https://doi.org/10.1186/s12864-026-12975-6
[74] Evaluating the Utilities of Foundation Models in Single-Cell Data Analysis. *Advanced science (Weinheim, Baden-Wurttemberg, Germany)*, 2026-03-23, https://doi.org/10.1002/advs.202514490
[75] Enhancing cross-context generalization in drug perturbation prediction with a multimodal conditional diffusion framework. *Bioinformatics (Oxford, England)*, 2026-07-01, https://doi.org/10.1093/bioinformatics/btag482
[76] PopPert: Population-level Joint-Distribution Modeling for Single-Cell Perturbation Prediction *arxiv*, 2026-09-01, https://arxiv.org/abs/2609.01357v1
[77] Directional coherence and effect magnitude in single-cell CRISPR perturbation responses *arxiv*, 2026-04-17, https://arxiv.org/abs/2604.16642v4
[78] A vision foundation model for single-cell biology via spatial gene cartography *arxiv*, 2026-07-15, https://arxiv.org/abs/2607.14163v1
[79] RAGCell: Retrieval-Augmented Generation as Supervision for Versatile Single-cell Analysis *arxiv*, 2026-09-12, https://arxiv.org/abs/2609.14147v1
[80] Prototype Guided Post-pretraining for Single-Cell Representation Learning *arxiv*, 2026-05-08, https://arxiv.org/abs/2605.07938v1
[81] What Makes a Representation Good for Single-Cell Perturbation Prediction? *arxiv*, 2026-05-19, https://arxiv.org/abs/2605.19343v1
[82] SCMBench: benchmarking domain-specific and foundation models for single-cell multi-omics data integration. *Nature communications*, 2026-05-02, https://doi.org/10.1038/s41467-026-72570-x
[83] A transcription factor regulatory atlas for activity inference and perturbation prediction. *Nucleic acids research*, 2026-09-01, https://doi.org/10.1093/nar/gkag897
[84] Artificial intelligence virtual bone organoids (AIVBOs). *Journal of orthopaedic translation*, 2026-08-26, https://doi.org/10.1016/j.jot.2026.101196
[85] CAPTAIN: a multimodal foundation model pretrained on co-assayed single-cell RNA and protein. *Nature communications*, 2026-05-07, https://doi.org/10.1038/s41467-026-72882-y
[86] RegFormer: a single-cell foundation model powered by gene regulatory hierarchies. *Nature communications*, 2026-05-05, https://doi.org/10.1038/s41467-026-72198-x
[87] Sparse autoencoders reveal interpretable cell-type programs in single-cell foundation model representations. *Journal of biomedical informatics*, 2026-05-19, https://doi.org/10.1016/j.jbi.2026.105056
[88] A mechanism-annotated benchmark reveals limited fidelity to drug-response signatures in single-cell perturbation models *europepmc*, 2026-08-24, https://doi.org/10.64898/2026.08.19.745729
[89] Predictive single cell foundation model for gene regulation and aging with privacy-preserving tabular learning *europepmc*, 2026-07-09, https://doi.org/10.21203/rs.3.rs-10274933/v1
[90] Tissueformer: extending single-cell foundation models to predict population-level phenotypes. *BMC bioinformatics*, 2026-06-04, https://doi.org/10.1186/s12859-026-06490-4
[91] scBalFlow: A Staged Flow Matching Framework for Imbalanced Single-Cell Drug Perturbation Prediction. *Bioinformatics (Oxford, England)*, 2026-09-15, https://doi.org/10.1093/bioinformatics/btag682
[92] Learning stochastic dynamics and cell-fate landscapes from single-cell snapshots via optimal transport. *Science advances*, 2026-09-09, https://doi.org/10.1126/sciadv.aeb4205
[93] MultiFlow: coupled flow matching for predicting single-cell multiomic perturbation responses in unseen cellular contexts *europepmc*, 2026-08-25, https://doi.org/10.64898/2026.08.20.746112
[94] SLIM: A small linear model with STRING embeddings for single-cell genetic perturbation prediction *europepmc*, 2026-08-07, https://doi.org/10.64898/2026.08.07.743481
[95] Towards Principled Evaluation of Single-Cell Perturbation Prediction Models *europepmc*, 2026-07-27, https://doi.org/10.64898/2026.07.23.740433
[96] CAPRA predicts single-cell transcriptional responses to genetic perturbations with response anchoring and residual correction *europepmc*, 2026-07-21, https://doi.org/10.21203/rs.3.rs-10231666/v1
[97] What topological and geometric structure do biological foundation models learn? Evidence from 141 hypotheses. *PloS one*, 2026-07-17, https://doi.org/10.1371/journal.pone.0344826
[98] Deep Generative Model of Macrophage Immune Response for Hepato-intestinal Tumor Therapy Optimization. *Cyborg and bionic systems (Washington, D.C.)*, 2026-06-16, https://doi.org/10.34133/cbsystems.0559
[99] D-SPIN constructs regulatory network models from scRNA-seq that reveal organizing principles of perturbation response. *Cell*, 2026-05-12, https://doi.org/10.1016/j.cell.2026.04.028
[100] Predictive single cell foundation model for gene regulation and aging with privacy-preserving tabular learning *arxiv*, 2026-07-06, https://arxiv.org/abs/2607.19400v1
[101] Towards a knowledge-enhanced single-cell foundation model *arxiv*, 2026-09-14, https://arxiv.org/abs/2609.14970v1
[102] Intermediate Layers Encode Optimal Biological Representations in Single-Cell Foundation Models *arxiv*, 2026-04-16, https://arxiv.org/abs/2604.14838v1
[103] Score Distributions, Not Cells: Evaluating Single-Cell Perturbations Under Class Overlap *arxiv*, 2026-07-06, https://arxiv.org/abs/2607.04595v1
[104] GC-MoE: Genomics-Guided Cell-Type-Specific Mixture of Experts for Histology-Based Single-Cell Spatial Transcriptomics *arxiv*, 2026-06-01, https://arxiv.org/abs/2606.02424v1
[105] Single-Cell Cross-Modal Transfer by Adversarial Fine-Tuning of Foundation Models *arxiv*, 2026-06-04, https://arxiv.org/abs/2606.07676v1
[106] VeloTree: Inferring single-cell trajectories from RNA velocity fields with varifold distances *arxiv*, 2026-04-01, https://arxiv.org/abs/2604.02380v1
[107] PACE: Geometry-Aware Bridge Transport for Single-Cell Trajectory Inference *arxiv*, 2026-05-18, https://arxiv.org/abs/2605.18587v2
[108] Prior-Guided Multi-Omic Transformers for Single-Cell Gene Regulatory Network Inference *arxiv*, 2026-05-30, https://arxiv.org/abs/2606.00685v1
