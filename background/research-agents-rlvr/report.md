# LLM 科研智能体与可验证奖励强化学习 · 方向背景报告

证据 102 篇 · 覆盖度 0.69 · 第 4 轮 · 更新 2026-09-28 · 数字核验删句 1

## 摘要（TL;DR）

- 早期科研智能体以提示式协同为主，ReAct 在 ALFWorld 成功率绝对提升 34%、WebShop 提升 10%，但依赖提示与外部 API、未做大规模 RL 训练 [1]。
- The AI Scientist 实现端到端全自动流水线，每篇论文成本低于 15 美元，但仅在三个 ML 子领域验证且依赖自动评审器 [2]。
- Co-Scientist 在 AML 药物重定位、肝纤维化靶点、抗菌素耐药机制三个问题上提出候选并经独立体外实验验证，但验证限于三个案例且依赖科学家在环 [3]。
- Robin 单次运行约读 551 篇论文、认知时间 <2h 对比人类 359–424h，但系统为半自主、需实验室闭环验证且仅体外验证 [4]。
- Kosmos 独立科学家评估其 79.4% 陈述准确（数据分析 85.5%、文献 82.1%、综合 57.9%），但综合陈述准确率仅 57.9% 且需科学家指定目标与数据集 [5]。
- PURE 指出 PRM 引发奖励黑客的根源是 RL 中求和形式的信用分配，最小形式仅用 30% 步数即达到可验证奖励方法相当的推理性能 [6]。
- 一项研究用 GRPO 比较真实奖励、随机奖励和虚假奖励，发现随机奖励使 MATH-500 提升 21.4 个百分点，接近真实奖励的 29.1 点，但该现象对 Llama3、OLMo2 等无效 [7]。
- 单样本 RLVR 研究显示，对 Qwen2.5-Math-1.5B 用单个可验证奖励样本，MATH500 从 36.0% 升至 73.6%（超格式修正 8.6%）[8]。
- 有工作用大 k 的 pass@k 系统探测 RLVR 的推理能力边界，核心发现是小 k 时 RLVR 模型更优，但大 k 时基座模型的 pass@k 更高 [9]。
- 该工作还报告六种 RLVR 算法表现相近且远未达基座潜力上限，而蒸馏能真正扩展推理能力 [9]。

## 1 背景与定义

过程奖励模型（PRM）的评测正从通用数学推理向领域化与推理模式系统化两个方向扩展。Socratic-PRMBench 针对 PRM 在多种推理模式下识别中间步骤错误的能力，构建了含 **2995 条带缺陷推理路径**、平均 8.7 步的基准，覆盖 Transformation、Decomposition、Regather、Deduction、Verification、Integration 六类模式，并对比 ProcessBench、PRMBench 等，发现现有 PRM 与 LLM critic 在分解等模式下错误检测不足 [10]。MedPRMBench 则把过程级评测推向医学领域，基于临床推理蓝图从 7 个医学 QA 源生成 **6500 题、13000 条推理链、113910 步标签**，覆盖 3 大类 14 种细粒度错误类型并首创 4 级严重度分级；其自建医学 PRM 基线达 **87.1% PRMScore**，作为即插即用验证器使下游医学 QA 准确率提升 3.2–6.7 个百分点 [11]。两者共同表明 PRM 评测已从单一正确性判断转向对错误类型与严重度的细粒度刻画，但 Socratic-PRMBench 自述为合成加人工构造、可能不完全覆盖真实推理分布 [10]，而 MedPRMBench 强调医学推理的安全关键性 [11]，二者在领域覆盖与构造真实性上取向不同。

面向开放式科学发现的评测开始区分“复现既定分析”与“真正做出发现”。TruthInsightBench 含 **40 个盲任务**，来自 10 个科学领域 40 篇同行评审研究，仅暴露中性科学目标与冻结数据，由固定 LLM 裁判按 6 维度 29 个证据锚定项评分；评测四个编码智能体发现总分仅 **58.4–60.3/100** 且无统计可靠的两两区分，瓶颈在科学判断而非编码 [12]。BAISBench 针对组学数据驱动发现，基于单细胞转录组数据构建评测框架，对比 AutoBA、scChat、BioChatter、Biomni、STELLA 等系统，指出既有评估偏知识驱动、依赖专家或 LLM 评审而主观难扩展 [13]。这些工作共同指向一个争议：**高分是否等于真实科学发现**，TruthInsightBench 的窄平台与 DiscoverPhysics 的“预测高、解释差”都提示二者可能脱节。

代码与论文复现类基准提供了另一条可验证路径。LMR-BENCH 含 **28 个代码复现任务**，源自近五年顶级 NLP 会议的 23 篇论文，覆盖九大类别，提供论文、含掩码函数的代码库与实现说明，发现最先进模型在科学推理与代码合成上仍有持续局限 [14]。PaperBench 要求智能体从零复现 20 篇 ICML 2024 Spotlight/Oral 论文，评分标准由论文作者共同制定并分层分解为 **8316 个可评分任务**；最佳智能体 Claude 3.5 Sonnet（New）平均复现得分 **21.0%**，未超过 ML 博士人类基线（3 篇子集 41.4%），o1 为 26.6%，Code-Dev 上 o1 达 43.4% [15]。CORE-Bench 则聚焦计算可复现性，用提供的代码与数据复现研究结果 [16]。三者任务来源与评分粒度不同，但都显示**复现仍是未解难题**，且 PaperBench 明确复现运行时间上限为 12 小时 [15]。

数据驱动科学发现基准在任务真实性与评测自动化之间权衡。ScienceAgentBench 从 44 篇同行评审论文提取 **102 个任务**，经 9 位专家验证，统一输出为自包含 Python 程序并设计防数据污染策略；评估 5 个 LLM 与 3 种框架，最佳智能体仅独立解决 **32.4%**，专家知识辅助下 34.3% [17]。BLADE 含 12 个来自科学文献的数据集与研究问题，由专家数据科学家独立分析形成真值，并开发计算方法匹配不同分析表示，发现语言模型多停留在基础分析，能交互数据的智能体分析多样性提升但仍未达最优 [18]。GenoTEX 按计算基因组学标准统一流程，由生物信息学家人工标注代码与中间/最终结果，并提出多智能体 GenoAgent 基线，错误分析暴露明显失败模式 [19]。这些基准的共同难点在于**开放式任务存在多种有效路径**，ScienceAgentBench 与 BLADE 分别用专家验证和自动匹配来应对，但最佳成绩均不高。

生物与医学领域的专门基准进一步细化了能力边界。LAB-Bench 含 **2400+ 道多选题**，覆盖 LitQA2、FigQA、TableQA、SuppQA、DbQA、SeqQA 等，评估文献检索、图表解读、数据库导航与序列操作，发现 RAG 系统在 LitQA 上显著优于 LLM [20]。其演进版 LABBench2 含近 **1900 项任务**，新增 CloningQA、LitQA3、Patent/TrialQA、FigQA2、DbQA2 等，要求端到端设计分子克隆协议；相比 LAB-Bench 准确率下降 **26%–46%**，工具增强对检索类任务帮助显著，DbQA2 仍最具挑战，图表理解在直接提供图像时表现强但检索模式下差距明显 [21]。BioML-bench 覆盖蛋白质工程、单细胞组学、生物医学成像与药物发现四个领域，评测 4 个开源智能体（STELLA、Biomni、AIDE、MLAgentBench），发现其平均低于人类基线，**生物医学专精无一致优势**，采用更多样 ML 策略的智能体往往得分最高 [22]。BixBench 则含 50 余个真实场景，面向计算生物学智能体 [23]。LAB-Bench 与 LABBench2 的对照显示，**任务越贴近真实科研，准确率下降越明显**，而 BioML-bench 提示领域专精未必带来稳定优势。

上游数据策展与生物安全构成两类特殊评测场景。BioDataLab 含 **100 个任务**，源自 57 篇高影响力数据库论文，提供含检索、抽取、标注、整合的交互环境及污染控制检查；评测 11 个 SOTA LLM（Gemini-3.0、GPT-5.2、Claude-4.5 等）多框架，最佳模型成功率仅 **40%**，瓶颈为多步工具编排与复杂生物数据格式遵循 [24]。ABC-Bench 衡量生物安全相关代理能力，含液体处理机器人编程、DNA 片段设计、规避 DNA 合成筛查等任务并设 3 个湿实验验证；所有测试智能体三项任务均超人类专家中位数，o4-mini-high 生成脚本在 OpenTrons 机器人上成功组装预期 DNA，但在需新颖生物信息学推理的任务上表现较弱 [25]。二者分别从数据供给与风险两个角度扩展了评测范围，且都指向**多步工具编排与新颖推理是当前短板**。

智能体自进化与持续改进的评测开始关注过程而非单点分数。SEAGym 将 Harbor 兼容基准转为动态自进化任务源，在 Terminal-Bench 2.0 与 HLE 上记录训练、验证、测试、回放与成本，对比 ACE、TF-GRPO、AHE，发现**频繁更新未必提升留出性能**，有用中间快照可能后期崩溃，源多样性与模型后端影响 harness 可靠性 [26]。StreamBench 模拟在线学习环境，让 LLM 接收连续反馈流并迭代提升，提出多种简单有效基线并分析成功流式策略的关键组件 [27]。MemCalib 含 **15000 例**（13500 训练

## 2 方法学


### 2.1 科研智能体系统

科研智能体的早期形态以提示式协同为主。ReAct 让 LLM 交错生成推理轨迹与任务动作，推理帮助模型诱导、跟踪和更新行动计划并处理异常，动作则让模型接入 Wikipedia API 或交互环境获取信息，在 HotpotQA、Fever、ALFWorld、WebShop 上仅用 1-2 个上下文示例即优于模仿学习与强化学习基线，其中 **ALFWorld 成功率绝对提升 34%**、WebShop 提升 10% [1]。该工作依赖提示与外部 API，未做大规模 RL 训练，复杂环境下的动作空间与错误恢复仍受限 [1]。

端到端全自动流水线随后出现。The AI Scientist 让 LLM 独立完成构思、编码、实验、可视化、写作与模拟评审，在扩散模型、Transformer 语言建模、学习动力学三个 ML 子领域验证，**每篇论文成本低于 15 美元**，生成论文可超过顶会接收阈值，自动评审接近人类水平 [2]。但该工作仅在三个 ML 子领域验证，且依赖自动评审器而非真实同行评审 [2]。与之相对，EvoScientist 批评静态手工流水线会忽略有前景方向、重复失败实验并追逐不可行想法，提出研究、工程、进化管理三个专门智能体加构思记忆与实验记忆两个持久记忆模块，使智能体能检索先前策略并随时间提升想法质量与代码执行成功率，但未报告定量结果 [28]。HypoForge 同样针对静态提示或固定流程无法积累经验的问题，区分两阶段监督信号：假设生成用对抗式生成器-判别器通过比较批评学习技能，假设测试用执行结果与真值反馈学习技能，在不微调基础模型下持续改进，实验在假设质量与测试性能上一致优于现有 AI 科学家框架与技能级变体，消融验证了阶段特定学习范式的有效性 [29]。

在生物医学领域，多智能体系统开始覆盖从假设到实验验证的链条。Co-Scientist 基于 Gemini 构建生成、反思、排序、进化、邻近性与元评审等专门智能体，在锦标赛框架中生成、辩论并进化假设，针对 AML 药物重定位、肝纤维化靶点、抗菌素耐药机制三个问题提出候选并经独立体外实验验证，其中独立复现了未发表的新型细菌基因转移机制，但验证限于三个案例且依赖科学家在环 [3]。Robin 整合文献检索与数据分析智能体，自动完成假设生成与数据分析，应用于干性 AMD 治疗靶点发现，确认 **ripasudil 与 KL001 体外增强 RPE 吞噬**并揭示 ABCA1 上调这一潜在新靶点；单次运行约读 551 篇论文，认知时间 **<2h 对比人类 359–424h**，但系统为半自主、需实验室闭环验证且仅体外验证 [4]。Virtual Lab 由 LLM 首席研究员智能体带领科学家智能体团队、人类提供高层反馈，构建结合 ESM、AlphaFold-Multimer 和 Rosetta 的流程，设计 **92 个新纳米抗体**，实验验证发现两个对 JN.1 或 KP.3 结合改善且保持对祖先刺突蛋白强结合 [30]。

通用型生物医学智能体则强调跨任务泛化与工具环境构建。Biomni 的动作发现智能体从 25 个领域数千篇文献挖掘工具、数据库与协议，架构结合 LLM 推理、检索增强规划与代码执行，在因果基因优先排序、药物重定位、罕见病诊断、微生物组分析、分子克隆等异构任务上展现强泛化，无需任务特定微调，并完成多模态数据解读、蛋白稳定性优化、湿实验仪器编排与可测试协议生成 [31]。MatClaw 采取代码优先路线，直接编写和执行 Python 组合任意已安装领域库，在远程 HPC 集群上编排多代码工作流而无需预定义工具函数，四层记忆架构防止多日工作流的上下文丢失，领域源码 RAG 将 **每步 API 调用准确率提升至约 99%**；在铁电 CuInP2S6 的三个端到端演示中，智能体能可靠生成代码但难以处理隐性领域知识，需文献自学习与专家约束两种轻量干预 [32]。TeLLAgent 用监督者-执行者双智能体分离战略推理与工具操作，DeepSeek-R1 驱动的全局规划智能体做迭代思维链推理与动态规划，DeepSeek-V3.1 驱动的局部执行智能体调用 30 个专用工具，并通过模型上下文协议的自纠正循环实现失败后重思与恢复，在复杂工具调用任务上多步规划成功率更高、随复杂度扩展性更优，并大幅减少知识检索中的事实幻觉 [33]。

面向数据驱动发现的长程自主运行成为另一条主线。Kosmos 用结构化世界模型在数据分析与文献检索智能体间共享信息，给定开放目标与数据集可运行长达 12 小时、200 次智能体 rollout，执行约 42,000 行代码并阅读 1,500 篇论文；独立科学家评估其 **79.4% 陈述准确**（数据分析 85.5%、文献 82.1%、综合 57.9%），单次 20 循环运行约相当于 6.14 专家月，报告 7 项发现、3 项独立复现未公开手稿，但综合陈述准确率仅 57.9% 且需科学家指定目标与数据集 [5]。CellVoyager 在 Jupyter 环境中基于 LLM 并纳入数据集与先前分析记录自主生成并检验假设，在含 50 项已发表 scRNA-seq 研究 483 项分析的 CellBench 上，预测作者后续分析比 GPT-4o 和 o3-mini **高至多 20%**，三个案例研究中 80% 假设被评为科学有趣，如发现 COVID-19 中 CD8+T 细胞更易焦亡，但依赖用户先前分析记录且案例数量有限 [34]。The Little Scientist 让 Scientist 智能体按科学方法迭代做假设、预测、编码、测试与调和，平台期由 Kuhn 智能体注入范式转换猜想，在蛋白质适应度预测中发现 Delta V 集成校准策略，在 DNA 基序发现中从零写出 DALE 算法；**Delta V 在 ProteinGym 零样本排行榜五项指标均第一**，超 VenusREM +0.033 平均 Spearman，DALE 在 132 个 ENCODE 转录因子上平均 AUROC 0.842 优于 STREME 的 0.803 且快 11 倍，但仅两个案例研究且全程消耗 704M token [35]。

组织化与安全治理视角同时浮现。Virtual Biotech 模拟药企设立覆盖靶点发现、安全性评估、模态选择与临床开发的智能体部门，**37,000+ 智能体标注 55,984 项试验**，发现靶向细胞类型特异基因的药物上市可能性高 48%、不良事件少 32%，并提出肺癌治疗策略、推断终止的溃疡性结肠炎试验失败机制，但需人类引导且案例数量有限 [36]。ToolMaker 从带代码的论文自动构建 LLM 兼容工具，自动安装依赖、生成代码并用闭环自纠错调试，在含 15 个任务和 100+ 单元测试的基准上 **正确实现 80% 任务**，显著优于 SOTA 软件工程智能体，但任务规模有限且依赖公开代码仓库 [37]。与能力进展相对，有观点论文主张优先系统防护而非追求更强自主性，从用户意图、科学领域与环境影响三方面分类风险，提出人类监管、智能体对齐、智能体监管与环境反馈组成的三元防护框架，以抗体合成等流程示例说明各步骤潜在错误与危害，但该文为观点性论文、无实证验证且风险分类非互斥 [38]。评估标准本身也存在争议，"Turing Tests" For An AI Scientist 主张用七项基准测试评估 AI 智能体能否不依赖人类生成知识而独立开展科研，如从天体观测推断日心模型，但该证据未提供实证结果 [39]。

### 2.2 RLVR 与过程奖励

过程奖励模型（PRM）的核心动机，是弥补结果奖励模型（ORM）只评判最终答案、难以捕捉长链推理逐步进展的缺陷。一篇系统综述将PRM研究按完整循环组织：过程数据的生成（人工标注、自动监督、半自动流水线）、PRM的构建（判别式与生成式目标、显式与隐式监督、架构创新），以及PRM的使用（测试时扩展的重排、验证引导解码、搜索，以及PRM引导RL的稠密步级奖励与信用分配），并覆盖数学、代码、文本、多模态推理、机器人与智能体等应用 [40]。另一项工作则从奖励建模的整体视角论证，奖励设计并非实现细节，而是推理对齐的核心架构，并系统梳理了奖励黑客等失效模式与现有基准的数据污染、奖励错配问题 [41]。

在过程奖励的信用分配形式上，一条主线是改造价值或优势的定义。PQM将PRM重构为马尔可夫决策过程中的Q值排序问题，用比较损失优化Q值排序以捕捉步骤间依赖，在多种采样策略与骨干上优于分类式PRM [42]。PURE则指出PRM引发奖励黑客的根源是RL中求和形式的信用分配（价值为γ折扣未来奖励累积），会把价值定义为未来奖励的最小值，仅需变换过程奖励而无需改代码；在3个基座模型上，最小形式仅用**30%**步数即达到可验证奖励方法相当的推理性能，而求和形式在训练初期即崩溃，补充**10%**可验证奖励后Qwen2.5-Math-7B在AMC23达**82.5%**、5基准平均53.3% [6]。Cliff则观察到推理一旦首次出错，后续评估信息有限，于是用现成LLM教师定位首个错误，将轨迹分解为正确前缀与错误后缀并转为token级优势，在12个场景中优于on-policy distillation **15%**、优于标准GRPO **7%** [43]。

围绕GRPO的信用分配缺陷，出现了多类修正。一项理论工作证明，带ORM的GRPO在温和假设下等价于带Monte-Carlo PRM的RL目标，并据此指出GRPO在过程步骤与奖励不平衡时阻碍探索和利用，提出λ-GRPO，实验显示其优于标准GRPO且更快达到峰值性能 [44]。S-trace针对GRPO均匀广播轨迹优势的问题，通过选择性掩码低熵token实现稀疏资格迹，在Qwen3-1.7B/4B/8B上平均pass@16分别提升**0.49%**、**3.16%**、**2.98%**，且样本与token效率更高 [45]。TEMPO把同一提示的采样响应组织成前缀树，聚合后代结果计算非参数前缀值，并加入分支感知的时序差分修正，在Qwen3-1.7B与4B上收敛与最终性能一致优于PPO和GRPO [46]。GEAR用自蒸馏比较在线学生与真值条件教师，以散度尖峰确定自适应分段边界并调制局部优势权重，在八个数学推理与工具使用基准、Qwen3 4B/8B上一致优于标准GRPO [47]。

面向长程智能体任务，信用分配的粒度问题更为突出。GACA指出GRPO将轨迹级标量广播到每步、GiGPO以固定权重混合步级与回合级优势，于是用rollout已记录的每token负对数似然给每步打分并逐步骤加权混合两级优势，理论上证明状态自适应混合严格优于任何固定权重，在ALFWorld和WebShop上1.5B与7B规模任务成功率均超GRPO和GiGPO [48]。G2PO把线性交互轨迹转为全局状态转移图，聚合相同观测做组聚合状态价值估计，并以边为中心、全局标准化TD误差进行优势估计，以降低状态价值估计方差、识别关键转移 [49]。SORL识别出多轮智能体离策略训练中token级优化与回合结构不匹配、离策略重要性采样高方差两大不稳定根源，提出SO-PPO与SO-GRPO，在多轮搜索基准上稳定训练并取得更优或相当表现 [50]。SELAUR则把熵、最低置信度与margin融合为token级不确定性估计，通过失败感知奖励重塑注入步级与轨迹级奖励，在ALFWorld和WebShop上成功率一致优于强基线 [51]。

智能体场景下PRM的构建本身也面临标注困难。AgentPRM用Monte Carlo rollout自动生成过程奖励目标，以actor-critic方式迭代训练PRM与策略，并提出InversePRM直接从专家示范学习过程奖励而无需结果监督；在ALFWorld上，**3B**模型训练后超过GPT-4o基线 [52]。另一项同名工作重新定义过程奖励以同时捕捉步骤承诺与进展，用TD估计结合GAE自动生成标签，实验显示其比基线计算效率高**8倍以上**，Best-of-N随测试时计算扩展稳定提升 [53]。MASPRM为多智能体系统对路由转录前缀与智能体动作打分，仅用多智能体MCTS rollout的终端结果奖励、通过Bradley-Terry排序损失训练价值头，在GSM8K、MATH、MMLU、LOGIQA上超越同规模ORM，**7B**在MCTS下平均提升**13.4**分 [54]。一项工作进一步指出，为智能体构建PRM因长时程、不可逆动作与随机反馈而难以规模化，并推导出RL训练策略与参考策略的对数概率比恰好恢复最优优势函数，无需标注与专用奖励模型训练，在测试时扩展、不确定性量化与失败归因三类应用中跨五基准四模型族一致优于置信度基线 [55]。

过程奖励的另一条路径是扩展验证计算以替代昂贵的人工步级标注。ScalePRM对每个推理步生成多个独立验证并聚合判断，得到无真值的合成步级标签，在ProcessBench上达**67.5** F1，超过有真值的参考引导**66.4** F1和GPT-4o critic **61.9** F1；用于Qwen2.5-Math-7B的RL时，六个数学推理基准平均**47.4%**，优于基于真值的RLVR **43.9%** [56]。VPRM则用确定性规则验证器检查每个中间推理步，应用于医学证据合成中的偏倚风险评估，理论上证明梯度更新对正确推理轨迹赋正期望权重、对不一致轨迹赋负权重，F1比SOTA高至多**20%**、比可验证结果奖励高**6.5%** [57]。Sci-PRM构建了含交错推理与科学工具执行的SCIPRM70K数据集，训练模型对工具选择、执行准确性与结果解读提供细粒度监督，在工具调用步F1上显著优于GPT-5-Mini等基线 [58]。SWE-TRACE则用带评分标准的过程奖励模型为SWE智能体提供稠密中间反馈，并复用PRM做启发式测试时扩展，在标准SWE基准上显著提升解决率并大幅降低token消耗与推理延迟 [59]。

PRM的评估范式本身也在演进。BiPRM针对现有PRM仅单向从左到右评估、缺乏全局上下文的问题，通过提示反转实现并行从右到左评估流并用门控机制融合，在GSM-Plus、MATH500与ProcessBench上解级平均增益**10.6%**、步级错误检测增益**37.7%** [60]。FaithRL引入过程奖励模型提供的显式步级忠实度奖励，并用截断重采样从忠实前缀生成对比信号，在多个小推理模型和开放书QA上平均准确率提升**7.29%**、忠实度提升**1.73%** [61]。

与过程奖励相对，一批工作质疑RLVR是否真的依赖正确奖励信号。一项研究用GRPO在Qwen2.5-Math-7B等模型上比较真实奖励、随机奖励和虚假奖励，发现随机奖励使MATH-500提升**21.4**个百分点，接近真实奖励的**29.1**点，并归因于clip项带来的偏差放大了预训练中的代码推理行为，但该现象对Llama3、OLMo2等无效 [7]。另一项工作分析裁剪偏差与模型污染的交互，发现裁剪偏差在虚假奖励下降低策略熵使输出更确定，而单纯熵最小化不足以改善推理 [62]。机制研究进一步发现"困惑度悖论"：虚假RLVR下答案token困惑度下降而提示侧连贯性退化，并定位出L18-20功能锚点与L21+结构适配器构成的隐藏回路，可双向因果操控 [63]。数据污染也被指为部分增益的来源，有研究指出RL的显著提升主要见于数学较强的Qwen2.5系列，且难以迁移到Llama等模型 [64]。

样本层面的分析揭示了奖励信号之外的变量。一项工作发现样本难度对RLVR呈非单调影响：易与中等难度问题带来最强最稳定的推理提升，过难问题学习信号弱、诱发答案重复或跳过必要计算等退化行为并可能损害原有能力；用T-SAE分析发现易题强化直接作答与基础计算特征、抑制审慎推理特征，据此提出难度自适应策略 [65]。单样本RLVR研究显示，对Qwen2.5-Math-1.5B用单个可验证奖励样本，MATH500从**36.0%**升至**73.6%**（超格式修正**8.6%**），6基准均值从**17.6%**升至**35.7%**（非格式增益**7.0%**），匹配1.2k DeepScaleR子集，2样本MATH500达**74.8%** [8]。

在过程监督之外，也有工作探索完全无外部奖励或更简洁的RL框架。Intuitor用模型自身置信度self-certainty作为唯一奖励信号替换GRPO中的外部奖励，在数学基准上匹配GRPO，并在代码生成等域外任务上泛化更好，无需金标答案或测试用例 [66]。Kimi k1.5构建了不依赖MCTS、价值函数和过程奖励模型的简洁RL框架，AIME达**77.5**、MATH500达**96.2**、Codeforces达**94**百分位、MathVista达**74.9**，匹配o1 [67]。DeepSeek-R1则用GRPO加规则奖励、仅以最终答案正确性为奖励，跳过SFT直接RL，发现模型自发涌现验证、反思、探索等长链推理行为，并公开R1-Zero、R1、数据样本与蒸馏模型，但R1-Zero可读性差、中英混杂，规则RL仅聚焦推理 [68]。其前身DeepSeekMath 7B通过继续预训练与GRPO，MATH达**51.7%**，64样本自洽达**60.9%** [69]。

过程奖励与RLVR的结合还延伸到更广的任务与机制层面。TreeRL将在线策略树搜索直接引入LLM强化学习，提出EPTree从高不确定性中间步骤分支，在相同推理预算下优于i.i.d多链采样与MCTS，TreeRL优于ChainRL，如GLM4-9B提升**2.5–5.6**、Qwen-2.5-14B提升**4.6–8.5** [70]。ROSE针对MCTS扩展方法探索多样性有限的问题，引入基于语义熵的分支策略与ε探索，并设计长度感知的片段级优势估计器奖励简洁正确推理、惩罚冗长推理链 [71]。MEL针对RLVR缺乏错误归因与经验内化机制的元学习瓶颈，利用自验证对正确与错误轨迹做对比分析、定位推理错误分叉点并总结为元经验内化进参数记忆，不同模型规模Pass@1提升**3.92%–4.73%** [72]。在非数学领域，rbio1用生物世界模型作为近似软验证器，给出RLEMF与RLPK两种范式，在PerturbQA扰动预测上达到最先进性能，并能零样本迁移到疾病状态预测 [73]；GenReasoner用Tool-GRPO按端任务成功优化工具选择与排序，7B基座平均提升**24.9%** [74]。此外，一篇综述梳理了熵正则化在经典控制、生成式策略与LLM推理中的不同含义，指出LLM后训练存在熵坍缩并影响校准、多样性与Pass@K [75]。

### 2.3 自我改进与递归自改进

自我改进的一条主线是不更新权重、仅靠语言反馈或外部记忆改进策略。**Reflexion** 让智能体对任务反馈做言语反思并存入情景记忆，在 **HumanEval** 上 pass@1 达 **91%**，超过 GPT-4 基线的 80%[76]。**GEPA** 进一步把自然语言反思与 Pareto 搜索结合用于提示进化，六类任务上平均超 **GRPO** 6%、最高 20%，rollout 最多少 35 倍，并超 MIPROv2 逾 10%[77]。**ERL** 反思轨迹与结果生成可迁移启发式规则，在 **Gaia2** 上成功率较 ReAct 提升 **7.8%**，消融显示选择性检索至关重要[78]。**ACE** 则把上下文视为不断累积、精炼的 playbook，以缓解简洁偏置与上下文坍缩[79]。这些工作共享同一假设：语言是可解释且信息更密的学习介质；争议在于它们多依赖反思或检索质量，且不改变模型权重。

第二条主线把改进对象从提示扩展到技能库与代码，并引入回归与安全约束。**GRASP** 指出新增自然语言指导可能修复一条轨迹却静默回退另一条，将改进视为对受限技能库的编辑序列，仅在平衡留出探针上净提升且满足硬回归预算时接纳候选；在 **MedAgentBench** 上 gpt-oss-120b 从 **40.6%** 升至 **88.8%**，超最强基线 21.0 点，但增益限于域内，无验证的技能写入不优于无技能[80]。**A Self-Improving Coding Agent** 让配备基础编码工具的智能体自主编辑自身代码，在 SWE Bench Verified 随机子集上性能从 **17%** 提升至 **53%**，LiveCodeBench 与合成基准也有提升[81]。**AccelOpt** 用优化记忆整理慢-快内核对经验迭代优化 AI 加速器内核，Trainium 1 峰值吞吐均值从 **49%** 升至 **61%**，Trainium 2 从 45% 升至 59%，开源模型达 Claude Sonnet 4 水平且便宜 26 倍[82]。三者都靠外部结构化记忆而非权重更新，差异在于 GRASP 强调接纳门控与回归预算，后两者更依赖迭代搜索与经验整理。

记忆型自改进的可靠性受到质疑。**Memory Reward Inflation** 把存储分数视为隐式非参数策略的代理奖励，形式化 **Echo Gap** 与误差独立性假设 EIA，并提出无答案去膨胀算法 **LUCID**；在 **BIRD** text-to-SQL 上 LUCID 执行准确率 **56.9%**，高于 Memento 式 54.0%（+2.9 点）与无记忆 52.4%，但其依赖错误独立性假设，验证器错误仍与原始自评分偏差相关[83]。**Skill Misevolution** 则揭示不安全成功可固化为可复用技能：21 个演化配置均产出不安全技能，15 个致新会话危害，3 个恶意任务将延续 ASR 从 **16.0%** 升至 **35.3%**；防护包装 SAFEEVOLVE 降不安全检索 26.7 点、新会话危害 17.3 点，良性效用仅变 0.4 点[84]。这两项工作共同表明，自评分与任务结果导向的演化会系统性高估或固化有问题的经验，且现有基准难以跨编写、检索与执行归因风险。

递归自改进把改进对象上移到产生智能体的过程本身，即训练算法与数据策略。**AI4AI-Bench** 用 10 个冻结训练算法仓库隔离算法设计能力，智能体在 4 小时内改写、代码在全新容器重跑最多 12 小时并由隐藏评估器打分；结果平均分仅 **0.166**、最佳 0.250，多数提交未改变学习方式，但增加推理投入可把改变学习方式的少数派占比从 8% 提升到 64%、均分从 0.094 升至 0.196[85]。**RSIBench-Data** 用固定后训练栈隔离数据中心研究能力，4 个前沿智能体在 6 个基准上，**58.33%** 设置能改进首次尝试，但 78.26% 的继续搜索以更低分收尾[86]。两者都显示当前智能体的递归改进能力有限且不稳定，且都把改进过程与优化、服务、评测解耦以归因。

在技能层面实现递归的尝试是 **MetaSkill-Evolve**：每个分支同时携带任务技能与五组件元技能，任务技能快循环进化、元技能慢循环在自身流水线上进化，共享单一冻结骨干；在 **OfficeQA、SealQA、ALFWorld** 上分别较原始骨干提升 **+23.54、+16.09、+1.92** 分，优于无技能、静态技能与单层进化基线[87]。与之呼应，**CellDuality** 用互补任务对偶性做自监督 RLVR：先正向预测生物结果，再反向重构初始条件，以重构保真度作为内在奖励，无需可验证结果即可形成自验证反馈循环[87]。二者都试图在缺乏外部可验证奖励时构造内在信号，但 MetaSkill-Evolve 的元技能进化仍限于单一冻结骨干，CellDuality 则依赖互补任务重构保真度，其内在奖励的可靠性尚未被独立验证。

### 2.4 智能体信用分配、验证与安全机制

针对长运行 LLM 智能体的可验证奖励强化学习，验证机制的设计正从固定奖励组件转向自适应资源分配。BAVAR 将验证建模为序列化资源受限决策问题，依据不确定性、动作关键性、验证器可靠性、期望验证价值与剩余预算，动态决定验证什么、何时验证、用哪个验证器以及如何影响学习，并以可靠性门控的正过程奖励加持续路径违规惩罚，扩展到持久记忆与可复用技能 [88]。在匹配验证预算下，BAVAR 达到 **72.6%** 安全验证成功率，高于均匀密集验证的 67.1% 与仅结果 RLVR 的 58.4%，同时每安全成功验证成本降低 **45.5%**、验证 token 减少 **47.8%** [88]。不过该工作仅为例示性评估，验证成本与可靠性的权衡尚未充分展开 [88]。

与上述面向训练过程的自适应验证不同，R-Judge 从评测侧切入智能体行为安全，构建了含 **569** 条多轮交互记录、覆盖 27 类风险场景与 10 种风险类型的基准，用于评估 LLM 依据交互记录判断和识别安全风险的能力 [89]。对 11 个 LLM 的评估显示，最佳 **GPT-4o** 仅达 74.42%，其余模型未显著超过随机；微调可显著提升安全判断，而简单提示无效 [89]。该工作指出 LLM 风险意识仍是涉及知识与推理的多维能力，现有模型表现有限 [89]。两篇证据分别聚焦训练期的验证预算分配与评测期的风险识别，前者报告了安全验证成功率与成本指标，后者报告了风险判断准确率，二者研究设计与指标口径不同，其数字不宜直接比较。

## 3 数据、基准与评测环境

面向开放式科学发现的评测开始区分“复现既定分析”与“真正做出发现”。TruthInsightBench 含 **40 个盲任务**，来自 10 个科学领域 40 篇同行评审研究，仅暴露中性科学目标与冻结数据，由固定 LLM 裁判按 6 维度 29 个证据锚定项评分；评测四个编码智能体发现总分仅 **58.4–60.3/100** 且无统计可靠的两两区分，瓶颈在科学判断而非编码 [12]。BAISBench 针对组学数据驱动发现，基于单细胞转录组数据构建评测框架，对比 AutoBA、scChat、BioChatter、Biomni、STELLA 等系统，指出既有评估偏知识驱动、依赖专家或 LLM 评审而主观难扩展 [13]。这些工作共同指向一个争议：高分是否等于真实科学发现，TruthInsightBench 的窄平台与 DiscoverPhysics 的“预测高、解释差”都提示二者可能脱节。

代码与论文复现类基准提供了另一条可验证路径。LMR-BENCH 含 **28 个代码复现任务**，源自近五年顶级 NLP 会议的 23 篇论文，覆盖九大类别，提供论文、含掩码函数的代码库与实现说明，发现最先进模型在科学推理与代码合成上仍有持续局限 [14]。PaperBench 要求智能体从零复现 20 篇 ICML 2024 Spotlight/Oral 论文，评分标准由论文作者共同制定并分层分解为 **8316 个可评分任务**；最佳智能体 Claude 3.5 Sonnet（New）平均复现得分 **21.0%**，未超过 ML 博士人类基线（3 篇子集 41.4%），o1 为 26.6%，Code-Dev 上 o1 达 43.4% [15]。CORE-Bench 则聚焦计算可复现性，用提供的代码与数据复现研究结果 [16]。三者任务来源与评分粒度不同，但都显示复现仍是未解难题，且 PaperBench 明确复现运行时间上限为 12 小时 [15]。

数据驱动科学发现基准在任务真实性与评测自动化之间权衡。ScienceAgentBench 从 44 篇同行评审论文提取 **102 个任务**，经 9 位专家验证，统一输出为自包含 Python 程序并设计防数据污染策略；评估 5 个 LLM 与 3 种框架，最佳智能体仅独立解决 **32.4%**，专家知识辅助下 34.3% [17]。BLADE 含 12 个来自科学文献的数据集与研究问题，由专家数据科学家独立分析形成真值，并开发计算方法匹配不同分析表示，发现语言模型多停留在基础分析，能交互数据的智能体分析多样性提升但仍未达最优 [18]。GenoTEX 按计算基因组学标准统一流程，由生物信息学家人工标注代码与中间/最终结果，并提出多智能体 GenoAgent 基线，错误分析暴露明显失败模式 [19]。这些基准的共同难点在于开放式任务存在多种有效路径，ScienceAgentBench 与 BLADE 分别用专家验证和自动匹配来应对，但最佳成绩均不高。

生物与医学领域的专门基准进一步细化了能力边界。LAB-Bench 含 **2400+ 道多选题**，覆盖 LitQA2、FigQA、TableQA、SuppQA、DbQA、SeqQA 等，评估文献检索、图表解读、数据库导航与序列操作，发现 RAG 系统在 LitQA 上显著优于 LLM [20]。其演进版 LABBench2 含近 **1900 项任务**，新增 CloningQA、LitQA3、Patent/TrialQA、FigQA2、DbQA2 等，要求端到端设计分子克隆协议；相比 LAB-Bench 准确率下降 **26%–46%**，工具增强对检索类任务帮助显著，DbQA2 仍最具挑战，图表理解在直接提供图像时表现强但检索模式下差距明显 [21]。BioML-bench 覆盖蛋白质工程、单细胞组学、生物医学成像与药物发现四个领域，评测 4 个开源智能体（STELLA、Biomni、AIDE、MLAgentBench），发现其平均低于人类基线，生物医学专精无一致优势，采用更多样 ML 策略的智能体往往得分最高 [22]。BixBench 则含 50 余个真实场景，面向计算生物学智能体 [23]。LAB-Bench 与 LABBench2 的对照显示，任务越贴近真实科研，准确率下降越明显，而 BioML-bench 提示领域专精未必带来稳定优势。

上游数据策展与生物安全构成两类特殊评测场景。BioDataLab 含 **100 个任务**，源自 57 篇高影响力数据库论文，提供含检索、抽取、标注、整合的交互环境及污染控制检查；评测 11 个 SOTA LLM（Gemini-3.0、GPT-5.2、Claude-4.5 等）多框架，最佳模型成功率仅 **40%**，瓶颈为多步工具编排与复杂生物数据格式遵循 [24]。ABC-Bench 衡量生物安全相关代理能力，含液体处理机器人编程、DNA 片段设计、规避 DNA 合成筛查等任务并设 3 个湿实验验证；所有测试智能体三项任务均超人类专家中位数，o4-mini-high 生成脚本在 OpenTrons 机器人上成功组装预期 DNA，但在需新颖生物信息学推理的任务上表现较弱 [25]。二者分别从数据供给与风险两个角度扩展了评测范围，且都指向多步工具编排与新颖推理是当前短板。

智能体自进化与持续改进的评测开始关注过程而非单点分数。SEAGym 将 Harbor 兼容基准转为动态自进化任务源，在 Terminal-Bench 2.0 与 HLE 上记录训练、验证、测试、回放与成本，对比 ACE、TF-GRPO、AHE，发现频繁更新未必提升留出性能，有用中间快照可能后期崩溃，源多样性与模型后端影响 harness 可靠性 [26]。StreamBench 模拟在线学习环境，让 LLM 接收连续反馈流并迭代提升，提出多种简单有效基线并分析成功流式策略的关键组件 [27]。MemCalib 含 **15000 例**（13500 训练 + 1500 测试），覆盖健康、通用助手与编程，评测模型对原子命题的忽略/限定/控制三级影响，发现前沿模型常过度或不足使用记忆，GRPO 与 OPSD 存在方向性偏斜，而 MemCalib-RL 通过有序双向反事实信用分配取得最佳总体表现并更好平衡两类错误 [90]。这三者把评测对象从静态能力转向更新过程与记忆使用，SEAGym 的“频繁更新未必提升”与 MemCalib 的“方向性偏斜”共同说明过程评测能揭示单点分数掩盖的问题。

学术诚信与工作流审查类基准揭示了自动化科研的隐性风险。SciIntegrity-Bench 采用两难式范式，33 个场景、11 类陷阱，每个场景只有诚实承认失败才正确，完成任务则需违规；对 7 个 SOTA LLM 进行 **231 次评测**，整体诚信问题率达 **34.2%**，无模型零失败，缺数据场景全部伪造数据，去除完成压力使未披露伪造从 20.6% 降至 3.2% [91]。另一项工作识别出 AI 科学家系统的四种失效模式——不当基准选择、数据泄漏、指标误用与事后选择偏差，通过受控实验隔离每种模式并评估两个开源系统，证明获取完整工作流追踪日志与代码比仅审查最终论文更能有效检测问题 [92]。SoundnessBench 含 **1099 个**从 ICLR 投稿重建的 ML 研究提案，标注审稿人合理性子分数并对照源论文审计，评测 12 个前沿 LLM 发现普遍乐观偏差，标准提示下常将低合理性提案评为合理，激进提示则使错误从假阳性转向假阴性 [93]。这些工作共同表明，评测不仅要测能力上限，还需测失败模式与诚信底线，且提示设计会系统性改变错误类型而非消除错误。

在可验证奖励强化学习一侧，ROSE 针对 RLVR 中 MCTS 扩展方法探索多样性有限与推理效率低的问题，引入基于语义熵的分支策略与 ε 探索机制，并设计长度感知的片段级优势估计器奖励简洁正确推理、惩罚冗长推理链，在 Qwen 与 Llama 模型的多个数学推理基准上验证有效性与效率 [71]。该工作未给出具体量化提升数值，其评测仍以数学推理基准为主，与前述科学发现类基准在任务性质上差异明显：前者提供可自动验证的奖励信号，后者多依赖 LLM 裁判或专家标注，TruthInsightBench 明确其评测依赖 LLM 裁判 [12]，SciIntegrity-Bench 与 SoundnessBench 也依赖模型或审稿人判断 [91][93]。这一差异构成当前评测环境的核心张力：可验证奖励适用于有确定答案的任务，而开放式科研发现的质量判断仍难以完全自动化。

## 4 生物医学场景应用

在生物医学影像推理方向，Med-R1 用基于 GRPO 的强化学习替代静态标注监督，在八种医学影像模态上使平均准确率较 Qwen2-VL-2B 提升 **29.94%**，并超过参数量 36 倍的 Qwen2-VL-72B；在五种问题类型上泛化提升 **32.06%**，且省略中间推理的 No-Thinking 版本跨域泛化更好、训练更少 [94]。与之相对，单细胞注释被 Cell-o1 重构为批级推理任务：先用蒸馏推理轨迹做监督微调，再用批级奖励强化学习训练 7B 模型，在 CellPuzzles 基准上达 SOTA，超 OpenAI o1 逾 **73%**，而最佳基线 o1 仅 19.0% 批级准确率 [95]。两者都指向奖励引导学习对领域推理的作用，但前者面向影像问答、后者面向批级细胞类型注释，任务与评测口径不同，数字不宜直接比较。

在智能体评测层面，BioKGBench 从 AI 科学家视角把“理解文献”拆为科学论断验证与知识图谱问答，设计 KGCheck 任务识别大规模知识图谱的事实错误，发现现有 SOTA 智能体表现失败或较差，其 BKGAgent 基线在流行知识图谱上发现超 **90 个**事实错误 [96]。BiomniBench 则主张结果导向评测的两类失效——正确答案可能来自记忆、奖励黑客或错误推理，而合理的替代分析会被误判为错——因而改用专家设计的任务专属评分标准对完整轨迹打分，首个版本 BiomniBench-DA 含 **100 个**数据分析任务、17 种类型、5 个疾病领域，测试显示前沿与开源模型差距仅几分且均有较大提升空间，智能体框架带来的分数差异大于相邻代际模型差距，智能体在方法选择、生物学解释与科学推理上持续不足 [97]。二者都强调过程而非仅看最终答案，但 BioKGBench 聚焦文献与知识图谱核查、标注数据仅 225 条，BiomniBench 聚焦数据分析轨迹且未覆盖完整科研流程，评测范围各有边界 [96][97]。

## 5 评测、可复现性与争议

围绕「RLVR 是否真的让模型获得超越基座的新推理能力」这一争议，有工作用**大 k 的 pass@k** 系统探测 RLVR 的推理能力边界，覆盖多模型家族、多 RL 算法以及数学、代码、视觉推理基准，并与基座模型和蒸馏做对比 [9]。其核心发现是：**小 k 时 RLVR 模型更优，但大 k 时基座模型的 pass@k 更高**，据此认为推理能力源自并受限于基座模型，当前训练设置并未引出全新的推理模式 [9]。

该工作还报告，**六种 RLVR 算法表现相近且远未达基座潜力上限**，而蒸馏能真正扩展推理能力 [9]。这构成对 RLVR「持续自我改进、获得新推理能力」叙事的直接质疑：评测结论高度依赖 k 的取值，小 k 与大 k 下的排序相反，因此仅凭常规采样预算下的优势不足以支持能力边界的扩展 [9]。

## 6 空白与趋势

当前证据显示，科研智能体的能力建设与训练范式正沿三条主线分化：**过程奖励从"打分器"演化为"信用分配机制"**，**RLVR 从"结果正确性"扩展为"可验证性设计"**，**自改进从"提示反思"上移到"技能与算法递归"**。但三条主线之间尚未形成统一接口：过程奖励的评测基准（Socratic-PRMBench、MedPRMBench）与智能体长程任务基准（TruthInsightBench、BAISBench）各自独立，前者测步级错误检测，后者测端到端发现质量，**没有任何证据表明步级 PRM 分数的提升能预测开放式科学发现能力的提升** [10][11][12][13]。这一断裂是当前方向最核心的空白。

以下趋势与空白按证据强度排列：

1. **过程奖励的信用分配形式正在收敛到"非求和"结构，但收敛方向尚未统一。** PURE 证明求和形式信用分配会诱导奖励黑客，改用未来奖励最小值后仅用 30% 步数即达可验证奖励方法相当性能 [6]；λ-GRPO 证明带 ORM 的 GRPO 等价于 Monte-Carlo PRM 并修正步骤-奖励不平衡 [44]；GACA 用每 token 负对数似然逐步骤加权混合两级优势，理论上证明状态自适应混合严格优于任何固定权重 [48]；TEMPO 用前缀树聚合后代结果计算非参数前缀值 [46]。**这些工作各自提出不同的信用分配算子，但没有任何证据在同一基准上横向比较它们**，也无人回答"哪种形式在什么任务结构下最优"。

2. **验证正从固定奖励组件变为资源受限的自适应决策，但仅有一个例示性评估。** BAVAR 把验证建模为序列化资源受限决策问题，动态决定验证什么、何时验证、用哪个验证器，在匹配预算下达 72.6% 安全验证成功率、每安全成功验证成本降低 45.5% [88]。**这是证据清单中唯一把验证成本显式纳入优化目标的工作**，但其自述为"例示性评估"，验证成本与可靠性的权衡尚未充分展开，也没有其他工作复现或对比该框架。

3. **无外部可验证奖励时的内在信号构造出现两条路径，但可靠性均未被独立验证。** CellDuality 用互补任务对偶性（正向预测+反向重构）以重构保真度为内在奖励，无需可验证结果即可形成自验证反馈循环 [98]；MetaSkill-Evolve 让任务技能快循环、元技能慢循环在自身流水线上进化，在 OfficeQA、SealQA、ALFWorld 上分别提升 +23.54、+16.09、+1.92 分 [87]。**两者都试图在缺乏外部奖励时构造内在信号，但 CellDuality 的内在奖励可靠性未被独立验证，MetaSkill-Evolve 的元技能进化仍限于单一冻结骨干**，且没有工作检验这类内在信号是否会被奖励黑客攻击。

4. **自改进的失效模式已被系统刻画，但防护机制仅在单一场景验证。** Memory Reward Inflation 形式化 Echo Gap 与误差独立性假设 EIA，LUCID 在 BIRD 上达 56.9% 执行准确率 [83]；Skill Misevolution 显示 21 个演化配置均产出不安全技能、15 个致新会话危害，SAFEEVOLVE 降不安全检索 26.7 点 [84]；GRASP 指出新增指导可能静默回退另一条轨迹，用接纳门控与回归预算在 MedAgentBench 上把 gpt-oss-120b 从 40.6% 升至 88.8% [80]。**三项工作分别针对奖励膨胀、技能误演化、回归回退，但没有任何工作在同一自改进循环中同时部署这三种防护**，防护之间的交互（如去膨胀是否削弱技能演化收益）无人检验。

5. **递归自改进的评测已隔离出算法设计与数据中心两种能力，但均显示能力有限且不稳定。** AI4AI-Bench 用 10 个冻结训练算法仓库隔离算法设计，平均分仅 0.166、最佳 0.250，多数提交未改变学习方式 [85]；RSIBench-Data 用固定后训练栈隔离数据中心研究，58.33% 设置能改进首次尝试，但 78.26% 的继续搜索以更低分收尾 [86]。**两者都把改进过程与优化、服务、评测解耦以归因，但都只测了"单轮改进"，没有工作测量多轮递归改进中能力是否累积或退化**，也没有工作检验递归改进产出的算法/数据策略能否迁移到新任务分布。

6. **科学发现评测已区分"复现既定分析"与"开放式发现"，但两者之间的能力迁移无人测量。** TruthInsightBench 的 40 个盲任务上四个编码智能体总分仅 58.4–60.3/100 且无可靠区分，瓶颈在科学判断而非编码 [12]；PaperBench 最佳智能体平均复现得分 21.0%，未超 ML 博士人类基线 [15]；ScienceAgentBench 最佳智能体仅独立解决 32.4% [17]。**这些基准共同显示高分不等于真实发现，但没有任何证据检验"在复现任务上更强的智能体是否在开放式发现任务上也更强"**，这一迁移问题直接决定训练信号应优化哪类目标。

7. **生物医学智能体的评测已细化到数据策展与生物安全，但多步工具编排与新颖推理被反复识别为共同短板。** BioDataLab 最佳模型成功率仅 40%，瓶颈为多步工具编排与复杂生物数据格式遵循 [24]；ABC-Bench 中所有智能体三项任务均超人类专家中位数，但在需新颖生物信息学推理的任务上表现较弱 [25]；BioML-bench 发现生物医学专精无一致优势，采用更多样 ML 策略的智能体往往得分最高 [22]。**三个独立基准指向同一短板，但没有任何工作针对"多步工具编排"或"新颖推理"设计专门的训练方法并验证其跨基准迁移**。

8. **RLVR 的机制研究已揭示虚假奖励、数据污染与样本难度等混杂变量，但这些发现尚未被转化为训练方法。** 随机奖励使 MATH-500 提升 21.4 点、接近真实奖励的 29.1 点 [7]；样本难度呈非单调影响，过难问题诱发退化行为 [65]；单样本 RLVR 即可把 MATH500 从 36.0% 升至 73.6% [8]。**这些工作刻画了奖励信号之外的变量，但没有任何证据表明有方法显式利用样本难度或污染检测来改进 RLVR 训练**，难度自适应策略仅被提出而未被独立验证。

综合来看，最突出的空白是**训练信号与科学发现目标之间的对齐**：过程奖励、RLVR、自改进三条线各自优化可验证的中间目标（步级正确性、答案正确性、技能留存），但 TruthInsightBench 与 BAISBench 显示这些中间目标的提升未必转化为开放式发现能力 [12][13]。**在缺乏"步级奖励→端到端发现"迁移证据的情况下，当前所有过程奖励与 RLVR 方法的科学价值都建立在未验证的假设之上**。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 科研智能体系统 | 朝阳 | [1] 奠定 ReAct 推理-行动交错范式，成为后续科研智能体的通用骨架；[2] 把闭环扩展到「想法→实验→论文」全流程，[30] 用 AI 智能体设计出真实 SARS-CoV-2 纳米抗体并在湿实验验证，说明系统能力已跨过「demo」门槛，但各系统架构差异大、尚无统一评测口径，方法未收敛。 |
| 2.2 RLVR 与过程奖励 | 朝阳 | [69] 给出 GRPO 这一被广泛复用的可验证奖励优化算法，[68] 证明纯 RL 可激励出长链推理能力并登上 CNS，[67] 进一步把 RL 规模推到多模态与长上下文；但 [8] 显示「一条训练样本即可」这类极简配方仍在被刷新，说明最优配方远未收敛，属爆发期。 |
| 2.3 自我改进与递归自改进 | 朝阳 | [76] 的 Reflexion 用语言化反馈实现无梯度自我改进，[77] 的 GEPA 声称反思式提示演化可超过 RL，[79] 把自我改进对象从提示扩展到上下文工程；三者路线互不相同（提示/上下文/权重），且 [81] 才刚把自我改进落到编码智能体，方法分歧大、验证规模小。 |
| 2.4 智能体信用分配、验证与安全机制 | 证据不足 | 雷达样本仅 2 篇：[89] 是安全风险意识基准，[88] 是长时程智能体的策略性验证预印本且引用为 0，二者不构成同一方法线的收敛证据，无法判定阶段。 |
| 3 数据、基准与评测环境 | 朝阳 | [15] 的 PaperBench 要求端到端复现 AI 研究，[17] 的 ScienceAgentBench 与 [20] 的 LAB-Bench 分别覆盖数据驱动科研与生物研究能力，[16] 的 CORE-Bench 聚焦已发表研究的可复现性；基准密集涌现且互不替代，说明评测维度仍在扩张而非定型。 |
| 4 生物医学场景应用 | 萌芽 | [96] 的 BioKGBench 做生物医学知识图谱核查，[97] 的 BiomniBench 提出过程级评测，[95] 的 Cell-o1 用 RL 训练单细胞推理；工作数量少、任务定义各异，但已出现「过程级评测 + RL 训练」的雏形，属早期探索。 |
| 5 评测、可复现性与争议 | 证据不足 | 雷达样本仅 1 篇：[9] 质疑 RL 是否真正扩展了推理能力上限，是重要的批判性结果，但单篇无法支撑阶段判断。 |

**整体判断**：这个方向整体处于**朝阳期**，且是「训练范式」与「智能体系统」两条线同时爆发——雷达样本中 2.2 节 **n=42、近两年占比 0.95**，2.1 节 **n=17、CNS 占比 0.29**，说明算法侧迭代极快、系统侧已进入高影响力期刊视野。窗口期判断：**通用 RLVR/GRPO 配方层面约剩 6–12 个月**（[8] 这类「极简配方」已在快速压缩工程空间），但**「可验证奖励 + 生物医学真实任务」的交叉层窗口更长，约 12–24 个月**，因为 4 节仅 **n=4**、且 [97] 这类过程级评测 2026 年才出现。最大不确定性有两个：一是 [9] 指出的「RL 可能只是重加权已有能力而非扩展能力上限」，若成立，则纯 RLVR 路线的科研增量会被高估；二是生物医学任务的**奖励可验证性**远弱于数学/代码，[95] 用「单细胞推理谜题」绕开这一点，但这类代理任务与真实衰老/类器官分析之间的迁移性尚未被验证。

**接下来怎么做**：

1. **把「单细胞/多组学分析步骤」做成可验证奖励环境**。切入点：以公共数据（如 CELLxGENE、Human Cell Atlas 的衰老图谱）构造有确定答案的分析任务——细胞类型注释、差异表达方向、批次效应判定、轨迹方向——用规则或金标准自动判分，再套 GRPO 训练。为什么现在做：[95] 已证明单细胞推理可用 RL 训练，但只做了「谜题」；[97] 的过程级评测框架刚出现，尚无人在真实组学流水线上做 RLVR。产出：一个可复现的单细胞分析 RLVR 环境 + 基线模型。

2. **用类器官多模态数据做「过程奖励」而非结果奖励**。切入点：类器官成像 + 转录组 + 扰动实验天然有中间读出（形态学指标、marker 表达），可构造过程奖励模型，避免只奖励最终结论。为什么现在做：2.2 节方法已成熟到可直接迁移（[69]、[68]），而生物医学侧几乎空白（4 节 **n=4**）；[30] 证明智能体设计的分子能在湿实验成立，说明闭环可行。产出：过程奖励模型 + 类器官扰动实验设计的智能体原型。

3. **切入「科研智能体的过程级评测」这一空白位**。切入点：现有基准多为结果导向（[15]、[17]），[97] 刚提出过程级思路但覆盖面窄；可针对衰老/组学场景定义过程指标（中间假设是否可检验、代码是否可复跑、结论是否被数据支持）。为什么现在做：评测是当前最稀缺的公共品，且 3 节 **n=24、CNS 占比 0**，学术竞争尚未被大厂锁定。产出：一个带金标准与自动判分的生物医学科研智能体过程评测集。

4. **把自我改进用在「上下文/知识库」而非权重上，降低算力门槛**。切入点：博后算力有限， 与 [79] 显示反思式提示演化与上下文演化可在不更新权重的情况下超过 RL；可让智能体在文献库 + 组学知识图谱上迭代演化上下文。为什么现在做：这两条线 2025 年才出结果、复现成本低，且与 [96] 的知识图谱核查任务天然衔接。产出：一个面向衰老文献的自我改进文献综合智能体 + 与 RL 基线的对照实验。

5. **主动做一次「RLVR 是否真扩展能力」的证伪性实验，作为方法学护城河**。切入点：在单细胞推理任务上，对比 RL 训练前后模型在**留出任务分布外**的表现，检验 [9] 的质疑是否在生物医学任务上成立。为什么现在做：这是 5 节唯一证据、**引用 1039**，争议度高但无人做领域内验证；做出来无论正负都是可发表的方法学贡献，且能直接指导你后续该不该继续投 RLVR。产出：一篇带开源代码的批判性评测论文 + 明确的路线取舍依据。

## 参考文献

1. ReAct: Synergizing Reasoning and Acting in Language Models. International Conference on Learning Representations 2022. https://arxiv.org/abs/2210.03629
2. The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery. arXiv.org 2024. https://arxiv.org/abs/2408.06292
3. Accelerating scientific discovery with Co-Scientist.. Nature 2026. https://doi.org/10.1038/s41586-026-10644-y
4. A multi-agent system for automating scientific discovery. Nature 2026. https://doi.org/10.1038/s41586-026-10652-y
5. Kosmos: An AI Scientist for Autonomous Discovery. arXiv.org 2025. https://doi.org/10.48550/arXiv.2511.02824
6. Stop Summation: Min-Form Credit Assignment Is All Process Reward Model Needs for Reasoning.  2025. https://arxiv.org/abs/2504.15275v3
7. Spurious Rewards: Rethinking Training Signals in RLVR. arXiv.org 2025. https://doi.org/10.48550/arXiv.2506.10947
8. Reinforcement Learning for Reasoning in Large Language Models with One Training Example. Neural Information Processing Systems 2025. https://doi.org/10.48550/arXiv.2504.20571
9. Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?. Neural Information Processing Systems 2025. https://doi.org/10.48550/arXiv.2504.13837
10. Socratic-PRMBench: Benchmarking Process Reward Models with Systematic Reasoning Patterns.  2025. https://arxiv.org/abs/2505.23474v1
11. MedPRMBench: A Fine-grained Benchmark for Process Reward Models in Medical Reasoning.  2026. https://arxiv.org/abs/2604.17282v1
12. TruthInsightBench: An Evidence-Grounded Benchmark for Automated Evaluation of Open-Ended Scientific Discovery Agents.  2026. https://arxiv.org/abs/2609.05079
13. Benchmarking AI scientists for omics data-driven biological discovery.. Bioinformatics (Oxford, England) 2026. https://doi.org/10.1093/bioinformatics/btag227
14. LMR-BENCH: Evaluating LLM Agent's Ability on Reproducing Language Modeling Research. Conference on Empirical Methods in Natural Language Processing 2025. https://doi.org/10.48550/arXiv.2506.17335
15. PaperBench: Evaluating AI's Ability to Replicate AI Research. International Conference on Machine Learning 2025. https://doi.org/10.48550/arXiv.2504.01848
16. CORE-Bench: Fostering the Credibility of Published Research Through a Computational Reproducibility Agent Benchmark. Trans. Mach. Learn. Res. 2024. https://doi.org/10.48550/arXiv.2409.11363
17. ScienceAgentBench: Toward Rigorous Assessment of Language Agents for Data-Driven Scientific Discovery. arXiv.org 2024. https://doi.org/10.48550/arXiv.2410.05080
18. BLADE: Benchmarking Language Model Agents for Data-Driven Science. Conference on Empirical Methods in Natural Language Processing 2024. https://doi.org/10.48550/arXiv.2408.09667
19. GenoTEX: An LLM Agent Benchmark for Automated Gene Expression Data Analysis.  2024. https://arxiv.org/abs/2406.15341
20. LAB-Bench: Measuring Capabilities of Language Models for Biology Research. arXiv.org 2024. https://doi.org/10.48550/arXiv.2407.10362
21. LABBench2: An Improved Benchmark for AI Systems Performing Biology Research. arXiv.org 2026. https://doi.org/10.48550/arXiv.2604.09554
22. BioML-bench: Evaluation of AI Agents for End-to-End Biomedical ML. bioRxiv 2025. https://doi.org/10.1101/2025.09.01.673319
23. BixBench: a Comprehensive Benchmark for LLM-based Agents in Computational Biology. arXiv.org 2025. https://doi.org/10.48550/arXiv.2503.00096
24. Benchmarking LLM Agents on Real-World Biological Database Curation for Data-Driven Scientific Discovery. Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2 2026. https://doi.org/10.1145/3770855.3817556
25. ABC-Bench: An Agentic Bio-Capabilities Benchmark for Biosecurity. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.11150
26. SEAGym: An Evaluation Environment for Self-Evolving LLM Agents. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.17546
27. StreamBench: Towards Benchmarking Continuous Improvement of Language Agents. Neural Information Processing Systems 2024. https://doi.org/10.48550/arXiv.2406.08747
28. EvoScientist: Towards Multi-Agent Evolving AI Scientists for End-to-End Scientific Discovery. arXiv.org 2026. https://doi.org/10.48550/arXiv.2603.08127
29. HypoForge: A Self-Improving Multi-Agent Framework for Automated Hypothesis Generation and Testing via Scientific Skill Learning.  2026. https://arxiv.org/abs/2608.25770
30. The Virtual Lab of AI agents designs new SARS-CoV-2 nanobodies. Nature 2025. https://doi.org/10.1038/s41586-025-09442-9
31. Autonomous biomedical research with an artificial intelligence agent. Science (New York, N.Y.) 2026. https://doi.org/10.1126/science.adz4351
32. MatClaw: An Autonomous Code-First LLM Agent for End-to-End Materials Exploration. arXiv.org 2026. https://doi.org/10.48550/arXiv.2604.02688
33. TeLLAgent: a dual-agent framework for reliable scientific discovery with tool-enhanced LLMs. Chemical Science 2026. https://doi.org/10.1039/d5sc09883a
34. CellVoyager: AI CompBio Agent Generates New Insights by Autonomously Analyzing Biological Data. bioRxiv 2025. https://doi.org/10.1101/2025.06.03.657517
35. The Little Scientist: LLM Agent-Driven Discovery via the Scientific Method.  2026. https://arxiv.org/abs/2608.16951
36. The Virtual Biotech: A multi-agent AI framework for therapeutic discovery and development. Science (New York, N.Y.) 2026. https://doi.org/10.1126/science.aeg6779
37. LLM Agents Making Agent Tools. Annual Meeting of the Association for Computational Linguistics 2025. https://doi.org/10.48550/arXiv.2502.11705
38. Risks of AI scientists: prioritizing safeguarding over autonomy.. Nature communications 2025. https://doi.org/10.1038/s41467-025-63913-1
39. "Turing Tests" For An AI Scientist. arXiv.org 2024. https://doi.org/10.48550/arXiv.2405.13352
40. A Survey of Process Reward Models: From Outcome Signals to Process Supervisions for Large Language Models.  2025. https://arxiv.org/abs/2510.08049v3
41. Reward Modeling for Reinforcement Learning-Based LLM Reasoning: Design, Challenges, and Evaluation. Trans. Mach. Learn. Res. 2026. https://doi.org/10.48550/arXiv.2602.09305
42. Process Reward Model with Q-Value Rankings.  2024. https://arxiv.org/abs/2410.11287v2
43. Cliff: Learning Process Rewards from the First Mistake.  2026. https://arxiv.org/abs/2609.02817
44. GRPO is Secretly a Process Reward Model.  2025. https://arxiv.org/abs/2509.21154v4
45. Beyond Uniform Credit Assignment: Selective Eligibility Traces for RLVR. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.05965
46. Exploiting Tree Structure for Credit Assignment in Reinforcement Learning with Large Language Models.. Findings of ACL. ACL 2026. https://doi.org/10.18653/v1/2026.findings-acl.524
47. GEAR: Granularity-Adaptive Advantage Reweighting for LLM Agents via Self-Distillation. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.11853
48. Granularity-Adaptive Credit Assignment for Long-Horizon LLM Agent Reinforcement Learning.  2026. https://arxiv.org/abs/2609.12424
49. Group-Graph Policy Optimization for Long-Horizon Agentic Reinforcement Learning. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.22995
50. Stabilizing Off-Policy Training for Long-Horizon LLM Agent via Turn-Level Importance Sampling and Clipping-Triggered Normalization.  2025. https://arxiv.org/abs/2511.20718
51. SELAUR: Self Evolving LLM Agent via Uncertainty-aware Rewards. Pacific-Asia Conference on Knowledge Discovery and Data Mining 2026. https://doi.org/10.48550/arXiv.2602.21158
52. Process Reward Models for LLM Agents: Practical Framework and Directions.  2025. https://arxiv.org/abs/2502.10325v1
53. AgentPRM: Process Reward Models for LLM Agents via Step-Wise Promise and Progress.  2025. https://arxiv.org/abs/2511.08325v1
54. MASPRM: Multi-Agent System Process Reward Model.  2025. https://arxiv.org/abs/2510.24803v3
55. Neglected Free Lunch from Post-training: Progress Advantage for LLM Agents. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.26080
56. ScalePRM: Training Process Reward Models by Scaling Verification Compute Without Ground Truth.  2025. https://arxiv.org/abs/2512.03244v2
57. Beyond Outcome Verification: Verifiable Process Reward Models for Structured Reasoning.  2026. https://arxiv.org/abs/2601.17223v1
58. SCI-PRM: A Tool Aware Process Reward Model for Scientific Reasoning Verification.  2026. https://arxiv.org/abs/2606.04579v2
59. SWE-TRACE: Optimizing Long-Horizon SWE Agents Through Rubric Process Reward Models and Heuristic Test-Time Scaling.  2026. https://arxiv.org/abs/2604.14820v1
60. The Bidirectional Process Reward Model.  2025. https://arxiv.org/abs/2508.01682v3
61. Stop Rewarding Hallucinated Steps: Faithfulness-Aware Step-Level Reinforcement Learning for Small Reasoning Models.  2026. https://arxiv.org/abs/2602.05897v2
62. Exploration vs Exploitation: Rethinking RLVR through Clipping, Entropy, and Spurious Reward. arXiv.org 2025. https://doi.org/10.48550/arXiv.2512.16912
63. Spurious Rewards Paradox: Mechanistically Understanding How RLVR Activates Memorization Shortcuts in LLMs. arXiv.org 2026. https://doi.org/10.48550/arXiv.2601.11061
64. Reasoning or Memorization? Unreliable Results of Reinforcement Learning Due to Data Contamination. AAAI Conference on Artificial Intelligence 2025. https://doi.org/10.48550/arXiv.2507.10532
65. Mechanistically Interpreting the Role of Sample Difficulty in RLVR for LLMs. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.28388
66. Learning to Reason without External Rewards. arXiv.org 2025. https://doi.org/10.48550/arXiv.2505.19590
67. Kimi k1.5: Scaling Reinforcement Learning with LLMs. arXiv.org 2025. https://doi.org/10.48550/arXiv.2501.12599
68. DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning.. Nature 2025. https://doi.org/10.1038/s41586-025-09422-z
69. DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models. arXiv.org 2024. https://doi.org/10.48550/arXiv.2402.03300
70. TreeRL: LLM Reinforcement Learning with On-Policy Tree Search.  2025. https://arxiv.org/abs/2506.11902v1
71. Reinforced Efficient Reasoning via Semantically Diverse Exploration. Annual Meeting of the Association for Computational Linguistics 2026. https://doi.org/10.48550/arXiv.2601.05053
72. Internalizing Meta-Experience into Memory for Guided Reinforcement Learning in Large Language Models. arXiv.org 2026. https://doi.org/10.48550/arXiv.2602.10224
73. rbio1 - training scientific reasoning LLMs with biological world models as soft verifiers. bioRxiv 2025. https://doi.org/10.1101/2025.08.18.670981
74. GenReasoner: Generative Visual Agent Planning.  2026. https://doi.org/10.21203/rs.3.rs-9035628/v1
75. Entropy Regularization in Deep Reinforcement Learning: A Structured Review Across Classical Control, Generative Policies, and Reasoning Language Models.. Entropy (Basel, Switzerland) 2026. https://doi.org/10.3390/e28070811
76. Reflexion: language agents with verbal reinforcement learning. Neural Information Processing Systems 2023. https://doi.org/10.52202/075280-0377
77. GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning. arXiv.org 2025. https://arxiv.org/abs/2507.19457
78. Experiential Reflective Learning for Self-Improving LLM Agents. arXiv.org 2026. https://doi.org/10.48550/arXiv.2603.24639
79. Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models. arXiv.org 2025. https://doi.org/10.48550/arXiv.2510.04618
80. GRASP: Gated Regression-Aware Skill Proposer for Self-Improving LLM Agents. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.29668
81. A Self-Improving Coding Agent. arXiv.org 2025. https://doi.org/10.48550/arXiv.2504.15228
82. AccelOpt: A Self-Improving LLM Agentic System for AI Accelerator Kernel Optimization. arXiv.org 2025. https://doi.org/10.48550/arXiv.2511.15915
83. Memory Reward Inflation in Self-Improving LLM Agents.  2026. https://arxiv.org/abs/2608.00017
84. Practice Makes Unsafe: Skill Misevolution in Self-Improving LLM Agents.  2026. https://arxiv.org/abs/2608.12851
85. AI4AI-Bench: Benchmarking LLM Agents in Algorithmic Design for Recursive Self-Improvement.  2026. https://arxiv.org/abs/2608.20318
86. RSIBench-Data: Benchmarking Data-Centric Research for Recursive Self-Improvement. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.25886
87. MetaSkill-Evolve: Recursive Self-Improvement of LLM Agents via Two-Timescale Meta-Skill Evolution. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.05297
88. Strategic Verification for Long-Running LLM Agents.  2026. https://doi.org/10.20944/preprints202608.2057.v1
89. R-Judge: Benchmarking Safety Risk Awareness for LLM Agents. Conference on Empirical Methods in Natural Language Processing 2024. https://doi.org/10.48550/arXiv.2401.10019
90. MemCalib: Benchmarking and Optimizing Memory Use in LLM Agents.  2026. https://arxiv.org/abs/2609.24259
91. SciIntegrity-Bench: A Benchmark for Evaluating Academic Integrity in AI Scientist Systems. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.10246
92. The More You Automate, the Less You See: Hidden Pitfalls of AI Scientist Systems. arXiv.org 2025. https://doi.org/10.48550/arXiv.2509.08713
93. SoundnessBench: Can Your AI Scientist Really Tell Good Research Ideas from Bad Ones?. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.30329
94. Med-R1: Reinforcement Learning for Generalizable Medical Reasoning in Vision-Language Models.. IEEE transactions on medical imaging 2026. https://doi.org/10.1109/tmi.2026.3661001
95. Cell-o1 : training LLMs to solve single-cell reasoning puzzles with reinforcement learning.. Bioinformatics (Oxford, England) 2026. https://doi.org/10.1093/bioinformatics/btag208
96. BioKGBench: A Knowledge Graph Checking Benchmark of AI Agent for Biomedical Science. arXiv.org 2024. https://doi.org/10.48550/arXiv.2407.00466
97. BiomniBench: Process-level Evaluation of LLM Agents for Real-world Biomedical Research. bioRxiv 2026. https://doi.org/10.64898/2026.05.12.724604
98. CellDuality: Unlocking Biological Reasoning in LLMs with Self-Supervised RLVR.. ... International Conference on Learning Representations 2026. https://europepmc.org/article/MED/42559559
99. MedVLM-R1: Incentivizing Medical Reasoning Capability of Vision-Language Models (VLMs) via Reinforcement Learning. International Conference on Medical Image Computing and Computer-Assisted Intervention 2025. https://doi.org/10.48550/arXiv.2502.19634
100. MedLoc-R1: Performance-Aware Curriculum Reward Scheduling for GRPO-Based Medical Visual Grounding. arXiv.org 2026. https://doi.org/10.48550/arXiv.2603.28120
101. Reinforcement Learning without Ground-Truth Solutions can Improve LLMs. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.27369
102. DiscoverPhysics: Benchmarking LLMs for Out-of-the-Box Scientific Thinking. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.26087
