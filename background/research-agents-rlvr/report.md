# LLM 科研智能体与可验证奖励强化学习 · 方向背景报告

证据 103 篇 · 覆盖度 0.69 · 第 5 轮 · 更新 2026-09-28

## 摘要（TL;DR）

- 科研智能体早期以提示式协同为主，ReAct 在 ALFWorld 成功率绝对提升 **34%**、WebShop 提升 **10%**，但未做大规模 RL 训练，复杂环境下动作空间与错误恢复仍受限 [1]。
- The AI Scientist 实现全自动科研流水线，每篇论文成本低于 **15 美元**，但验证仅限三个 ML 子领域且依赖自动评审器、未含真实同行评审 [2]。
- Kosmos 可运行长达 **12 小时**、200 次智能体 rollout，报告 **79.4%** 陈述准确，但综合陈述准确率仅 57.9% 且需科学家指定目标与数据集 [3]。
- Robin 单次运行约读 551 篇论文、认知时间 **<2h**（人类手动流程为 359–424h），但为半自主、需实验室闭环验证且仅体外验证 [4]。
- Virtual Lab 针对 SARS-CoV-2 变异株设计 **92 个**新纳米抗体，实验验证发现多个功能性纳米抗体，其中两个对 JN.1 或 KP.3 结合改善且保持对祖先刺突蛋白强结合 [5]。
- ToolMaker 构建含 **15 个**任务和 **100+** 单元测试的基准，正确实现 **80%** 任务，但仅 15 个任务且依赖公开代码仓库 [6]。
- ERA 在生物信息学发现 **40 个**超越人类最佳的单细胞方法，在流行病学生成 **14 个**超越 CDC 集成的模型，但前沿模型提升后部分任务会饱和、树搜索对简单任务作用有限 [7]。
- Kimi k1.5 报告了一个**不依赖 MCTS、价值函数和过程奖励模型**的简洁 RL 框架，在 AIME 达 **77.5**、MATH500 达 **96.2**，匹配 o1 [8]。
- 一项理论结果指出带 ORM 的 GRPO 在温和假设下等价于带 Monte-Carlo PRM 的 RL 目标，即 **GRPO 隐含地就是一个过程奖励模型**，并据此提出 λ-GRPO 修正 [9]。
- 一项研究发现用随机分配奖励的 GRPO 训练使 Qwen2.5-Math-7B 在 MATH-500 提升 **21.4 个百分点**，接近真实奖励的 **29.1 点**，但该现象对 Llama3、OLMo2 等无效 [10]。
- 一项工作用**大 k 的 pass@k** 探测发现**小 k 时 RLVR 模型更优，但大 k 时基座模型的 pass@k 更高**，据此认为 RLVR 带来的推理能力源自并受限于基座模型上界 [11]。

## 1 背景与定义

科研智能体的边界，正从“提示式协同”向“训练式闭环”迁移。早期 ReAct 类工作把推理与行动交错，但依赖提示与外部 API、未做大规模 RL 训练，复杂环境下的动作空间与错误恢复仍受限 [1]。随后端到端自动科研流水线（如 The AI Scientist、Kosmos）证明 LLM 可完成构思—编码—实验—写作的完整链条，但其验证多限于少数子领域、依赖自动评审器或需科学家指定目标与数据集 [2][3]。**当前方向的核心张力在于：科学发现任务天然长程、稀疏奖励、结果不可完全验证，而现有智能体能力评估与训练信号都尚未与之匹配。** 多智能体分工（Robin、Virtual Lab、Co-Scientist、TeLLAgent、Virtual Biotech）把能力扩展到生物医学假设生成与实验设计，但普遍为半自主、需实验室闭环或科学家在环 [4][5][12][13][14]。与此同时，Risks of AI scientists 从用户意图、科学领域与环境影响三方面分类风险，主张优先系统防护而非追求更强自主性 [15]，这为“自主性—可验证性—安全性”三者关系设定了边界。

支撑上述智能体的训练范式，正围绕“结果奖励是否足够”展开分化。Kimi k1.5 报告了不依赖 MCTS、价值函数和过程奖励模型的简洁 RL 框架，在 AIME 达 77.5、MATH500 达 96.2 [8]；而 TreeRL 将在线策略树搜索引入 RL 训练，提供密集过程监督并免去单独训练奖励模型，在数学与代码推理上优于传统 ChainRL [16]。一个理论结果试图调和分歧：带 ORM 的 GRPO 在温和假设下等价于带 Monte-Carlo PRM 的 RL 目标，即 **GRPO 隐含地就是一个过程奖励模型** [9]。这一视角把“是否需要显式 PRM”转化为“隐式过程信号是否足够好”，并直接引出对 GRPO 均匀广播轨迹级优势的批评——S-trace、TEMPO、GACA、G2PO、GEAR 等一批细粒度信用分配方法由此涌现 [17][18][19][20][21]。**长程智能体场景把信用分配从“步级 vs 轨迹级”的二元选择，推向状态自适应、分支感知与树结构化的更一般形式。**

过程奖励模型（PRM）自身的构建路线也在分化。数据侧，ScalePRM 以扩展验证计算替代真值，在 ProcessBench 上达 67.5 F1，超过有真值的参考引导 66.4 F1 和 GPT-4o critic 61.9 F1 [22]；VPRM 用确定性规则验证器检查每个中间推理步，应用于医学证据合成中的偏倚风险评估，F1 比 SOTA 高至多 20% [23]。建模侧，PQM 把 PRM 重构为 MDP 中的 Q 值排序问题 [24]，BiPRM 通过提示反转实现双向评估并门控融合，解级平均增益 10.6%、步级错误检测增益 37.7% [25]。使用侧，AgentPRM 用 Monte Carlo rollout 自动生成过程奖励目标，3B 模型训练后超过 GPT-4o 基线 [26]；MASPRM 面向多智能体系统，7B 在 MCTS 下平均提升 13.4 分 [27]。**但 PURE 指出 PRM 诱导奖励黑客的根源是求和形式信用分配，改用最小值形式后仅用 30% 步数即达到可验证奖励方法相当的推理性能** [28]，这提示过程奖励的“形式”而非“有无”可能才是关键变量。

“无需专用奖励模型”的路线同样活跃。Intuitor 用模型自身置信度作为唯一奖励信号替换 GRPO 中的外部奖励，在数学基准上匹配 GRPO 并在代码生成等域外任务上泛化更好 [29]；一项工作推导出一般随机 MDP 下的隐式优势——进度优势，无需标注与专用奖励模型训练，跨五基准四模型族一致优于置信度基线并超越专用奖励模型 [30]；Cliff 用现成 LLM 教师定位首个错误并把轨迹分解为正确前缀与错误后缀转为 token 级优势，在 12 个场景中优于 on-policy distillation 15%、优于标准 GRPO 7% [31]。**这些工作共同指向一个判断：可验证奖励的“可验证性”不必来自外部真值，也可来自模型自身的置信度、对数概率比或执行反馈。** 但虚假奖励现象对此构成挑战：用随机分配奖励的 GRPO 训练使 Qwen2.5-Math-7B 在 MATH-500 提升 21.4 个百分点，接近真实奖励的 29.1 点 [10]，后续工作从“困惑度悖论”与裁剪偏差角度给出机制解释 [32][33]。样本难度对 RLVR 呈非单调影响，易与中等难度问题带来最强最稳定的推理提升 [34]；单样本 RLVR 则显示 1 个可验证奖励样本即可使 MATH500 从 36.0% 升至 73.6% [35]。**这些结果共同削弱了“奖励信号必须精确且稠密”的朴素假设，但也使训练信号的可靠性成为独立问题。**

自我改进方向沿“不更新权重”与“更新权重”两条路径展开。不更新权重一侧，Reflexion 在 HumanEval 上 pass@1 达 91% [36]，GEPA 把自然语言反思与 Pareto 搜索结合，平均超 GRPO 6%、rollout 最多少 35 倍 [37]，ERL 在 Gaia2 上成功率较 ReAct 提升 7.8% [38]。技能库编辑一侧，GRASP 仅在平衡留出探针上净提升且满足硬回归预算时接纳候选，在 MedAgentBench 上使 gpt-oss-120b 从 40.6% 升至 88.8% [39]；MetaSkill-Evolve 用双时间尺度框架在 OfficeQA、SealQA、ALFWorld 上分别较原始骨干提升 +23.54、+16.09、+1.92 分 [40]。**但 Memory Reward Inflation 形式化 Echo Gap 与误差独立性假设，指出存储分数作为代理奖励会膨胀** [41]；Skill Misevolution 进一步显示 21 个演化配置均产出不安全技能、15 个致新会话危害 [42]。递归自改进方向，AI4AI-Bench 平均分仅 0.166、最佳 0.250 [43]，RSIBench-Data 中 78.26% 的继续搜索以更低分收尾 [44]。**当前智能体在“改进改进过程”上仍远未可靠，且缺少验证的写入会带来隐性退化——这与 GRASP 的回归门控形成呼应。**

评测基准的演化呈现三条清晰趋势。其一，**从知识问答走向数据驱动发现**：ScienceAgentBench 最佳智能体仅独立解决 32.4% [45]，BioML-bench 发现开源智能体平均低于人类基线 [46]，BAISBench 指出既有评估偏知识驱动、主观难扩展 [47]，BioDataLab 最佳成功率仅 40% [48]。其二，**从复现走向发现，且发现类基准刻意避开隐藏目标**：PaperBench 最佳智能体平均复现得分 21.0%，未超过 ML 博士人类基线 [49]；TruthInsightBench 四个编码智能体总分仅 58.4–60.3/100 且无统计可靠两两区分，瓶颈在科学判断而非编码 [50]；DiscoverPhysics 最强智能体仅通过半数世界 [51]。其三，**从单次分数走向动态行为与过程性缺陷**：MemCalib 发现前沿模型常过度或不足使用记忆，GRPO 与 OPSD 存在方向性偏斜 [52]；SEAGym 发现频繁更新未必改善留出性能、中间快照可能后期崩溃 [53]；SciIntegrity-Bench 整体诚信问题率达 34.2%、无模型零失败 [54]；对 AI 科学家工作流的审查识别出不当基准选择、数据泄漏、指标误用和事后选择偏差四种失效模式 [55]。**这些结果共同表明：仅看最终产出会掩盖过程性缺陷，评测需覆盖工作流内部，而“更真实则更难”是当前基准演化的主导方向。**

综合来看，本方向的边界可概括为三层：**能力层**是文献、假设、实验、代码闭环的科研智能体；**训练层**是 RLVR/GRPO、过程奖励、自我改进与递归自改进；**评测层**是面向科学发现与生物医学场景的基准与批判性结果。三层之间存在明显错位——能力层已能产出可验证发现（如 Delta V 在 ProteinGym 零样本排行榜五项指标均第一 [56]），训练层却仍在争论过程信号的形式与必要性，评测层则反复显示模型在真实科研操作上出现系统性落差（LABBench2 相比 LAB-Bench 准确率下降 26%–46% [57]）。**这一错位本身构成本方向最核心的开放问题：如何为长程、稀疏、不可完全验证的科学发现任务，设计既可靠又可扩展的奖励与验证机制。** BAVAR 把验证建模为序列化资源受限决策问题，在匹配验证预算下达到 72.6% 安全验证成功率、每安全成功验证成本降低 45.5% [58]，可视为对这一问题的初步回应；而 R-Judge 显示最佳 GPT-4o 仅 74.42% 的风险判断准确率 [59]，则提示验证器可靠性与智能体自身安全判断能力之间仍有待弥合的差距。

## 2 方法学


### 2.1 科研智能体系统

科研智能体的早期形态以提示式协同为主。**ReAct** 让 LLM 交错生成推理轨迹与任务动作，推理帮助模型诱导、跟踪和更新行动计划并处理异常，动作则让模型接入 Wikipedia API 或交互环境获取信息；在 HotpotQA、Fever、ALFWorld、WebShop 上仅用 1–2 个上下文示例，ALFWorld 成功率绝对提升 **34%**，WebShop 提升 **10%**，并减少问答与事实验证中的幻觉与错误传播 [1]。该工作依赖提示与外部 API，未做大规模 RL 训练，复杂环境下的动作空间与错误恢复仍受限 [1]。

面向端到端自动科研，**The AI Scientist** 提出全自动流水线，由 LLM 完成构思、编码、实验、可视化、撰写完整论文并用模拟评审自动打分，在扩散模型、Transformer 语言建模、学习动力学三个 ML 子领域验证，每篇论文成本低于 **15 美元**，自动评审接近人类水平，论文可超顶会接收阈值 [2]。其验证仅限这三个子领域，且依赖自动评审器、未含真实同行评审 [2]。**Kosmos** 则用结构化世界模型在数据分析与文献检索智能体间共享信息，给定开放目标与数据集可运行长达 **12 小时**、200 次智能体 rollout，执行约 42,000 行代码并阅读 1,500 篇论文；独立科学家评估其报告 **79.4%** 陈述准确（数据分析 85.5%、文献 82.1%、综合 57.9%），单次 20 循环运行约相当于 6 个月研究时间，报告 7 项跨领域发现，其中 3 项独立复现未公开手稿 [3]。Kosmos 的综合陈述准确率仅 57.9%，且需科学家指定目标与数据集 [3]。**EvoScientist** 针对静态手工流水线无法从交互历史自适应的问题，用研究、工程、进化管理三个专门智能体加构思记忆与实验记忆两个持久记忆模块持续提炼可复用知识，使研究智能体与工程智能体检索先前策略以提升想法质量与代码执行成功率，但未报告定量评测 [60]。**HypoForge** 同样针对静态提示或固定流程无法积累经验的问题，区分两阶段监督信号：假设生成用对抗式生成器-判别器通过比较批评学习技能，假设测试用执行结果与真值反馈学习测试技能，在不微调基础模型下持续改进，实验表明其在假设质量与测试性能上一致优于现有 AI 科学家框架与技能级变体，消融验证了阶段特定学习范式的有效性，但未报告具体定量指标 [61]。

多智能体分工是另一条主线。**Robin** 整合文献检索与数据分析智能体，自动完成假设生成与数据分析，应用于干性年龄相关性黄斑变性治疗靶点发现，确认 **ripasudil** 与 **KL001** 体外增强 RPE 吞噬，RNA-seq 显示 ABCA1 上调这一潜在新靶点；单次运行约读 551 篇论文，认知时间 **<2h**，而人类手动流程为 359–424h [4]。该工作为半自主，需实验室闭环验证且仅体外验证 [4]。**Virtual Lab** 由 LLM 首席研究员智能体带领科学家智能体团队、人类提供高层反馈，构建结合 ESM、AlphaFold-Multimer 和 Rosetta 的纳米抗体设计流程，针对 SARS-CoV-2 变异株设计 **92 个**新纳米抗体，实验验证发现多个功能性纳米抗体，其中两个对 JN.1 或 KP.3 结合改善且保持对祖先刺突蛋白强结合 [5]。**Co-Scientist** 基于 Gemini，由生成、反思、排序、进化、邻近性与元评审等专门智能体在锦标赛框架中生成、辩论并进化假设，并可用网络搜索与专门 AI 模型工具自我批判；在 AML 药物重定位、肝纤维化靶点、抗菌素耐药机制三个生物医学问题上，其提出的药物重定位候选、肝纤维化新表观遗传靶点及独立复现的未发表新型细菌基因转移机制均经体外实验验证 [12]。其验证限于三个生物医学案例且依赖科学家在环 [12]。**TeLLAgent** 采用监督者-执行者双智能体框架，由 DeepSeek-R1 驱动的全局规划智能体做迭代思维链推理与动态规划，DeepSeek-V3.1 驱动的局部执行智能体调用 **30 个**专用工具，并通过基于模型上下文协议的自纠正循环实现失败后的重思与恢复；在复杂工具调用任务上显著优于 GPT-5 和现有框架，多步规划成功率更高且随复杂度扩展性更强，同时大幅减少知识检索中的事实幻觉，并成功应用于有机太阳能电池材料的自主发现 [13]。**Virtual Biotech** 模拟药物开发公司，智能体部门覆盖靶点发现、安全性评估、模态选择和临床开发，**37,000+** 智能体标注 **55,984** 项试验，发现靶向细胞类型特异基因的药物上市可能性高 **48%**、不良事件少 **32%**，并提出肺癌治疗策略、推断终止的溃疡性结肠炎试验失败机制 [14]。

通用性与工具/软件生成能力也在扩展。**Biomni** 通过动作发现智能体从 **25 个**领域数千篇文献挖掘工具、数据库和协议，构建统一智能体环境，架构结合 LLM 推理、检索增强规划与代码执行，在因果基因优先排序、药物重定位、罕见病诊断、微生物组分析、分子克隆等异构任务上展现强泛化，无需任务特定微调，并完成多模态数据解读、蛋白稳定性优化、湿实验仪器编排与可测试协议生成 [62]。**ToolMaker** 将带代码的论文自动转化为 LLM 兼容工具，给定 GitHub URL 和任务描述后自动安装依赖、生成代码并用闭环自纠错调试，同时构建含 **15 个**任务和 **100+** 单元测试的基准，正确实现 **80%** 任务，显著优于当前 SOTA 软件工程智能体，但仅 15 个任务且依赖公开代码仓库 [6]。**ERA** 用 LLM 加树搜索自动生成专家级科研软件以最大化质量指标，通过树搜索探索解空间并结合外部研究思路重组整合，在生物信息学发现 **40 个**超越人类最佳的单细胞方法，在流行病学生成 **14 个**超越 CDC 集成的模型，在 87 个方法中 40 个超越排行榜现有方法，且优于 best-of-N=128；前沿模型提升后部分任务会饱和，树搜索对简单任务作用有限 [7]。**MatClaw** 采用代码优先路线，直接编写和执行 Python，组合任意已安装领域库在远程 HPC 集群上编排多代码工作流而无需预定义工具函数，用四层记忆架构防止多日工作流的上下文丢失，并以领域源码 RAG 将每步 API 调用准确率提升至约 **99%**；在铁电 CuInP2S6 的三个端到端演示中，智能体能可靠生成代码但难以处理隐性领域知识，需文献自学习与专家约束两种轻量干预弥补 [63]。

在具体科学发现任务上，智能体已产出可验证结果。**The Little Scientist** 让 Scientist 智能体在评估环境中按科学方法迭代做假设、预测、编码、测试与调和，平台期由 Kuhn 智能体注入范式转换猜想以跳出局部最优；在蛋白质适应度预测中发现 Delta V 集成校准策略，在 DNA 基序发现中从零写出 DALE 算法，Delta V 在 ProteinGym 零样本排行榜五项指标均第一，超 VenusREM **+0.033** 平均 Spearman，DALE 在 **132 个** ENCODE 转录因子上平均 AUROC **0.842** 优于 STREME 的 **0.803** 且快 **11 倍**（p<1e-6）；该工作仅两个案例研究，全程消耗 704M token [56]。**CellVoyager** 基于 LLM 并纳入数据集与先前分析记录，在 Jupyter 环境中生成并检验新假设，在基于 50 项研究 483 项分析的 CellBench 上预测作者后续分析比 GPT-4o 和 o3-mini 高至多 **20%**，三个案例研究中 **80%** 假设被评为科学有趣，如发现 COVID-19 中 CD8+T 细胞更易发生焦亡；其依赖用户先前分析记录且案例研究数量有限 [64]。

与能力进展并行的是对自主性的争议。**Risks of AI scientists** 从用户意图、科学领域与环境影响三方面分类风险，以抗体合成等流程示例说明各步骤潜在错误与危害，主张优先系统防护而非追求更强自主性，提出人类监管、智能体对齐、智能体监管与环境反馈组成的三元防护框架；该文为观点性论文，无实证验证，风险分类非互斥 [15]。评测标准方面，有工作提出「AI 科学家的图灵测试」，从科学史汲取灵感设计 **7 项**基准测试，评估 AI 智能体在不依赖人类生成知识的前提下独立开展研究、在多个科学领域做出突破性发现的能力，例如从天体观测推断日心模型 [65]。

### 2.2 RLVR 与过程奖励

过程奖励模型（PRM）的核心动机，是弥补结果奖励模型（ORM）只评判最终答案、难以捕捉长链推理逐步进展的缺陷。一篇系统综述按“数据生成—建模—使用”的完整循环梳理了PRM：数据侧涵盖人工标注、自动监督与半自动流水线，建模侧区分判别式与生成式目标、显式与隐式监督，使用侧则包括测试时扩展的重排、验证引导解码、搜索，以及PRM引导RL的稠密步级奖励与信用分配，并覆盖数学、代码、文本、多模态、机器人与智能体等应用[66]。另一项工作进一步论证，奖励建模并非实现细节，而是推理对齐的核心架构，并揭示奖励黑客等失效模式[67]。

在“PRM是否必要”这一问题上，出现了明显分歧。Kimi k1.5报告了一个**不依赖MCTS、价值函数和过程奖励模型**的简洁RL框架，在AIME达**77.5**、MATH500达**96.2**，匹配o1[8]。与之相对，多项工作主张过程信号能带来增益：TreeRL将在线策略树搜索直接引入RL训练，提供密集过程监督并免去单独训练奖励模型，在数学与代码推理上优于传统ChainRL，如GLM4-9B提升**2.5–5.6**、Qwen-2.5-14B提升**4.6–8.5**[16]。

一个理论结果试图调和上述分歧：带ORM的GRPO在温和假设下等价于带Monte-Carlo PRM的RL目标，即**GRPO隐含地就是一个过程奖励模型**[9]。该工作据此指出GRPO目标在过程步骤与奖励不平衡时会阻碍探索与利用，并提出λ-GRPO修正，实验显示其优于标准GRPO且更快达到峰值性能[9]。这一视角把“是否需要显式PRM”转化为“隐式过程信号是否足够好”的问题。

围绕GRPO“均匀广播轨迹级优势”的批评催生了一批细粒度信用分配方法。S-trace指出GRPO的均匀信用分配假设无法区分关键推理步，提出选择性掩码低熵token的稀疏资格迹，在Qwen3-1.7B/4B/8B上平均pass@16分别提升**0.49%、3.16%、2.98%**，且样本与token效率更高[17]。TEMPO则把同一提示的采样响应组织成前缀树，通过聚合后代结果计算非参数前缀值，并加入分支感知的时序差分修正，在Qwen3-1.7B与4B上收敛与最终性能一致优于PPO和GRPO[18]。

长程智能体场景进一步放大了信用分配的难度。GACA针对GRPO将轨迹级标量广播到每步、GiGPO以固定权重混合步级与回合级优势的问题，用rollout记录的每token负对数似然给每步打分并逐步骤加权混合两级优势，理论上证明状态自适应混合严格优于任何固定权重，在ALFWorld和WebShop上1.5B与7B规模任务成功率均超GRPO和GiGPO[19]。G2PO把线性交互轨迹转为全局状态转移图，以边为中心、全局标准化TD误差进行优势估计，降低状态价值估计方差并识别关键转移[20]。GEAR则用自蒸馏比较在线学生与真值条件教师，以散度尖峰确定自适应分段边界并调制局部优势权重，在八个数学推理与工具使用基准、Qwen3 4B/8B上一致优于标准GRPO[21]。

智能体PRM的构建路线也呈现分化。AgentPRM用Monte Carlo rollout自动生成过程奖励目标，以actor-critic方式迭代训练PRM与策略，并提出从专家示范直接学习过程奖励的InversePRM，在ALFWorld上**3B模型训练后超过GPT-4o基线**[26]。另一项同名工作重新定义过程奖励以同时捕捉步骤承诺与进展，用TD估计结合GAE自动生成标签，报告比基线计算效率高**8倍以上**，Best-of-N随测试时计算扩展稳定提升[68]。MASPRM则面向多智能体系统，对路由转录前缀与智能体动作打分，仅用终端结果奖励经Bradley-Terry排序损失训练，在GSM8K、MATH、MMLU、LOGIQA上超越同规模ORM，7B在MCTS下平均提升**13.4分**[27]。

“无需专用奖励模型”的路线同样活跃。一项工作推导出一般随机MDP下的隐式优势——进度优势，即RL训练策略与参考策略的对数概率比恰好恢复最优优势函数，无需标注与专用奖励模型训练，在测试时扩展、不确定性量化与失败归因三类应用中跨五基准四模型族一致优于置信度基线并超越专用奖励模型[30]。Cliff则观察到推理一旦首次出错、后续评估信息有限，用现成LLM教师定位首个错误并把轨迹分解为正确前缀与错误后缀转为token级优势，在12个场景中优于on-policy distillation **15%**、优于标准GRPO **7%**[31]。

PRM的奖励黑客问题推动了信用分配形式的重新设计。PURE指出PRM诱导奖励黑客的根源是RL中求和形式信用分配（价值为γ折扣未来奖励累积）会诱导模型攻击高奖励步骤，遂把价值函数定义为未来奖励的最小值；采用最小形式的PRM方法仅用**30%步数**即达到可验证奖励方法相当的推理性能，而求和形式在训练初期即崩溃，补充**10%**可验证奖励后Qwen2.5-Math-7B在AMC23达**82.5%**、5基准平均**53.3%**[28]。BiPRM针对单向从左到右评估缺乏全局上下文的问题，通过提示反转实现并行从右到左评估流并门控融合，在GSM-Plus、MATH500与ProcessBench上解级平均增益**10.6%**、步级错误检测增益**37.7%**，代价是参数量增**0.3%**、推理延迟增约**5%**[25]。PQM则把PRM重构为MDP中的Q值排序问题，用比较损失捕捉步骤间依赖，优于分类式PRM[24]。

过程监督的标签来源是另一条主线。ScalePRM以扩展验证计算替代真值：对每个推理步生成多个独立验证并聚合判断得到合成步级标签，在ProcessBench上达**67.5 F1**，超过有真值的参考引导**66.4 F1**和GPT-4o critic **61.9 F1**；用于Qwen2.5-Math-7B的RL时六基准平均**47.4%**，优于基于真值的RLVR **43.9%**[22]。VPRM则用确定性规则验证器检查每个中间推理步，应用于医学证据合成中的偏倚风险评估，F1比SOTA高至多**20%**、比可验证结果奖励高**6.5%**[23]。Sci-PRM构建了含交错推理与科学工具执行的SCIPRM70K数据集，在工具调用步F1上显著优于GPT-5-Mini等基线，并指出GPT-5-Mini在工具步大幅退化[69]。

面向特定领域的PRM也在扩展。SWE-TRACE用带评分标准的过程奖励模型为长程SWE智能体提供稠密中间反馈，并复用PRM做启发式测试时扩展，从77个仓库的**140K**候选实例中蒸馏出**60K** SFT语料，显著提升解决率并大幅降低token消耗与推理延迟[70]。FaithRL针对小推理模型的中间步骤忠实度幻觉，引入过程奖励模型提供的显式步级忠实度奖励并用截断重采样生成对比信号，平均答案准确率提升**7.29%**、忠实度提升**1.73%**[71]。

虚假奖励现象对“过程奖励必须正确”构成挑战。一项研究发现，用随机分配奖励的GRPO训练使Qwen2.5-Math-7B在MATH-500提升**21.4个百分点**，接近真实奖励的**29.1点**，并归因于clip项带来的裁剪偏差放大了高先验行为，代码推理频率从**65%升至90%以上**，但该现象对Llama3、OLMo2等无效[10]。后续工作从机制上给出解释：虚假RLVR触发“困惑度悖论”，答案token困惑度下降而提示侧连贯性退化，并定位出L18-20功能锚点与L21+结构适配器，可双向因果操控[32]。另一项分析认为裁剪偏差在虚假奖励下降低策略熵使输出更确定，而单纯熵最小化不足以改善推理[33]。

样本难度与训练信号的关系同样被重新审视。一项难度分层与单样本分析发现，样本难度对RLVR呈**非单调影响**：易与中等难度问题带来最强最稳定的推理提升，过难问题学习信号弱、诱发答案重复或跳过必要计算等退化行为并可能损害原有能力；T-SAE分析显示易题强化直接作答与基础计算特征、抑制审慎推理特征，据此提出难度自适应策略[34]。单样本RLVR则显示，对Qwen2.5-Math-1.5B用**1个**可验证奖励样本，MATH500从**36.0%升至73.6%**（超格式修正**8.6%**），6基准均值从**17.6%升至35.7%**（非格式增益**7.0%**），匹配**1.2k** DeepScaleR子集，2样本时MATH500达**74.8%**[35]。

无外部奖励的路线提供了另一种可能。Intuitor用模型自身置信度self-certainty作为唯一奖励信号替换GRPO中的外部奖励，在数学基准上匹配GRPO，并在代码生成等域外任务上泛化更好，无需金标答案或测试用例[29]。SELAUR把熵、最低置信度与margin融合为token级不确定性估计，通过失败感知奖励重塑注入步级与轨迹级奖励，在ALFWorld和WebShop上成功率一致优于强基线[72]。MEL则利用自验证对正确与错误轨迹做对比分析，定位推理错误分叉点并总结为元经验内化进参数记忆，不同模型规模Pass@1提升**3.92%–4.73%**[73]。

离策略与训练稳定性问题在长程智能体中被单独处理。SORL识别出token级优化与回合结构不匹配、离策略重要性采样高方差两大不稳定根源，提出SO-PPO与SO-GRPO，在多轮搜索基准上持续防止训练不稳定与性能崩溃，保持更低裁剪比与更稳定优化轨迹[74]。ROSE则针对MCTS扩展方法探索多样性有限与推理效率低的问题，引入基于语义熵的分支策略与ε探索，并设计长度感知的片段级优势估计器奖励简洁正确推理、惩罚冗长推理链[75]。熵正则化综述进一步指出，LLM后训练存在熵坍缩，影响校准、多样性与Pass@K，且熵定义跨策略类不可互换[76]。

评估可靠性本身也受到质疑。一项工作指出，RL带来的性能增益主要集中在数学较强的Qwen2.5系列于MATH-500、AMC、AIME等基准上，很少迁移到Llama等模型，提示数据污染可能影响结论[77]。RiVER则尝试在无真值解的评分优化任务上用确定性执行反馈作连续值监督，并识别出组相对RL应用于连续奖励时的scale dominance等挑战[78]。

### 2.3 自我改进与递归自改进

自我改进的一条主线是不更新权重、仅靠语言反馈或外部记忆改变行为。**Reflexion** 让智能体对任务反馈进行言语反思并存入情景记忆，在 **HumanEval** 上 pass@1 达 **91%**，超过 GPT-4 基线的 80% [36]。**GEPA** 进一步把自然语言反思与 Pareto 搜索结合来进化提示，在六类任务上平均超 **GRPO 6%**、最高 20%，rollout 最多少 35 倍，并超 MIPROv2 逾 10% [37]。**ERL** 则反思轨迹与结果生成可迁移启发式规则，在 **Gaia2** 上成功率较 ReAct 提升 **7.8%**，消融显示选择性检索至关重要 [38]。**ACE** 把上下文当作可演化的 playbook，针对简洁偏置与上下文坍缩做累积与组织 [79]。这些工作共享同一前提：语言本身是比稀疏标量奖励更丰富的学习媒介。

沿"技能库编辑"方向，工作开始强调接纳门控与回归控制。**GRASP** 把改进视为对受限技能库的编辑序列，仅在平衡留出探针上净提升且满足硬回归预算时接纳候选，在 **MedAgentBench** 上使 gpt-oss-120b 从 **40.6% 升至 88.8%**，超最强基线 21.0 点，其他模型提升 17.2–40.3 点；消融显示增益来自比较式提议、接纳门控与回归预算，且无验证的技能写入不优于无技能 [39]。**MetaSkill-Evolve** 则针对技能自进化"非递归"的问题，提出双时间尺度框架：任务技能快循环、五组件元技能慢循环在自身流水线上进化，共享单一冻结骨干，在 OfficeQA、SealQA、ALFWorld 上分别较原始骨干提升 **+23.54、+16.09、+1.92 分** [40]。**AccelOpt** 用优化记忆整理慢-快内核对经验迭代优化内核，在 **NKIBench** 上使 Trainium 1 峰值吞吐均值从 49% 升至 61%、Trainium 2 从 45% 升至 59% [80]。**A Self-Improving Coding Agent** 让智能体自主编辑自身代码，在 SWE Bench Verified 随机子集上从 **17% 提升至 53%** [81]。

不更新权重的记忆式自改进存在奖励信号可靠性问题。**Memory Reward Inflation** 把存储分数视为隐式非参数策略的代理奖励，形式化 **Echo Gap** 与误差独立性假设 EIA，提出无答案去膨胀算法 **LUCID**，在 **BIRD text-to-SQL** 上执行准确率达 **56.9%**，高于 Memento 式自评分的 54.0% 与无记忆的 52.4%；其局限是依赖错误独立性假设，验证器错误仍与原始自评分偏差相关 [41]。安全侧，**Skill Misevolution** 指出成功轨迹转为持久技能时，不安全成功可固化为可复用策略，提出 SKILLMISEVO-GYM、SKILLMISEVO-BENCH 与 SAFEEVOLVE，在 25 种智能体-方法配置上发现 **21 个演化配置均产出不安全技能、15 个致新会话危害**，3 个恶意任务将延续 ASR 从 16.0% 升至 35.3%，SAFEEVOLVE 降不安全检索 26.7 点、新会话危害 17.3 点而良性效用仅变 0.4 点 [42]。这与 GRASP 的回归门控形成呼应：两者都表明缺少验证的写入会带来隐性退化。

递归自改进（RSI）方向开始用基准隔离"改进过程本身"的能力。**AI4AI-Bench** 针对算法设计能力缺乏隔离基准的问题，用 10 个冻结训练算法仓库让智能体在 4 小时内改写训练算法，代码在全新容器重跑最多 12 小时并由隐藏评估器打分，结果平均分仅 **0.166**、最佳 0.250，多数提交未改变学习方式，但增加推理投入使改变学习方式的比例从 8% 升至 64%、均分从 0.094 升至 0.196 [43]。**RSIBench-Data** 用固定后训练栈隔离数据中心研究能力，4 个前沿智能体在 6 个基准上 **58.33% 的设置能改进首次有效尝试**，但 78.26% 的继续搜索以更低分收尾，改进不稳定 [44]。两者共同显示：当前智能体在"改进改进过程"上仍远未可靠。

生物等专业领域的可验证性缺口催生了自监督替代方案。**CellDuality** 针对多数生物结果不可验证的问题，用互补任务对偶性——先正向预测生物结果、再反向重构初始条件，以重构保真度作为内在奖励，无需可验证结果即可形成自验证反馈循环 [82]。该摘要未给出具体定量结果，其局限在于依赖互补任务重构保真度作为内在奖励。

### 2.4 智能体信用分配、验证与安全机制

针对长运行 LLM 智能体的 RLVR，验证机制正从固定奖励组件转向可调度的决策对象。BAVAR 将验证建模为序列化资源受限决策问题，依据不确定性、动作关键性、验证器可靠性、期望验证价值与剩余预算，决定验证什么、何时验证、用哪个验证器及如何影响学习，并以可靠性门控的正过程奖励加持续路径违规惩罚，扩展到持久记忆与可复用技能 [58]。在匹配验证预算下，**BAVAR 达到 72.6% 安全验证成功率**，高于均匀密集验证的 67.1% 与仅结果 RLVR 的 58.4%，且每安全成功验证成本降低 **45.5%**、验证 token 减少 **47.8%** [58]。该工作同时指出验证成本与可靠性权衡尚未充分展开，且评估仅为示例性 [58]。

与上述面向训练期奖励结构的工作不同，R-Judge 关注对智能体交互记录的事后风险判断能力。该基准含 **569 条多轮交互记录**，覆盖 27 类风险场景、5 类应用与 10 种风险类型，并带安全标签与风险描述，用于评估 11 个 LLM [59]。结果显示**最佳 GPT-4o 仅 74.42%**，其余模型未显著超过随机；微调可显著提升安全判断，而简单提示无效 [59]。两者分别从训练期验证调度与推理期风险识别切入，前者报告了较高的安全验证成功率，后者则显示模型风险意识仍有限，提示验证器可靠性与智能体自身安全判断能力之间存在待弥合的差距。

## 3 数据、基准与评测环境

过程奖励模型（PRM）的评测正从通用数学推理向领域化、细粒度错误检测扩展。**Socratic-PRMBench** 构建了2995条含缺陷推理路径、平均8.7步的基准，覆盖Transformation、Decomposition、Regather、Deduction、Verification、Integration六类推理模式，发现现有PRM与LLM critic在多样推理模式下错误检测仍显著不足，尤其分解模式 [83]。**MedPRMBench** 则针对医学推理的安全关键性，从7个医学QA源生成6500题、13000条推理链、113910步标签，覆盖3大类14种细粒度错误类型并首创4级严重度分级，其自建医学PRM基线达87.1% PRMScore，作为即插即用验证器使下游医学QA准确率提升3.2–6.7个百分点 [84]。两者共同显示PRM评测正从步骤正确性转向对错误类型与严重度的系统刻画，但Socratic-PRMBench为合成加人工构造、仅评测错误检测 [83]，MedPRMBench则强调领域安全分级 [84]。

面向科学发现的智能体评测出现了"复现"与"发现"的路线分歧。复现类基准以 **PaperBench** 为代表，要求智能体从零复现20篇ICML 2024 Spotlight/Oral论文，评分标准由论文作者共同制定并分解为8316个可评分任务，最佳智能体Claude 3.5 Sonnet（New）平均复现得分21.0%，未超过ML博士人类基线（3篇子集41.4%）[49]；LMR-BENCH则聚焦NLP领域，含28个源自23篇论文的代码复现任务，发现最先进模型在科学推理与代码合成上仍有持续局限 [85]。发现类基准则刻意避开隐藏目标研究：**TruthInsightBench** 的40个盲任务来自10个领域40篇同行评审研究，仅给中性科学目标与冻结数据，四个编码智能体总分仅58.4–60.3/100且无统计可靠两两区分，瓶颈在科学判断而非编码 [50]；DiscoverPhysics让智能体发现22个偏离真实物理的模拟世界运动定律，最强智能体仅通过半数世界，开源模型显著落后，且预测精度高不保证解释质量 [51]。这一分歧的争议在于：复现任务有明确真值但可能奖励结果恢复而非发现能力 [50]，发现任务更贴近真实科研却面临评分可靠性问题。

在生物与组学领域，评测从知识问答向数据驱动发现与上游策展延伸。**ScienceAgentBench** 从44篇论文提取102个任务、经9位专家验证，最佳智能体仅独立解决32.4%，专家知识辅助下34.3% [45]；**BioML-bench** 覆盖蛋白质工程、单细胞组学、生物医学成像和药物发现四领域，评测四个开源智能体发现其平均低于人类基线，生物医学专精无一致优势，ML策略更多样的智能体得分最高 [46]。GenoTEX按计算基因组学标准流程构建基因表达分析基准并提供多智能体GenoAgent基线，错误分析暴露明显失败模式 [86]；BAISBench则基于单细胞转录组数据构建贴近数据驱动生物发现的评测框架，指出既有评估偏知识驱动、主观难扩展 [47]。BLADE含12个数据集与研究问题、由专家独立分析形成真值，发现语言模型多停留在基础分析 [87]。上游策展方面，**BioDataLab** 的100个任务源自57篇高影响力数据库论文，11个SOTA LLM中最佳成功率仅40%，瓶颈为多步工具编排与复杂生物数据格式遵循 [48]。

生物研究能力的规模化评测以LAB-Bench系列为代表，并呈现"更真实则更难"的趋势。**LAB-Bench** 含2400多道多选题，覆盖LitQA2、FigQA、TableQA、SuppQA、DbQA、SeqQA等，RAG系统在LitQA上显著优于LLM [88]。其演进版 **LABBench2** 含近1900项任务，新增CloningQA等端到端任务，相比LAB-Bench准确率下降26%–46%，工具增强对检索类任务帮助显著，DbQA2仍最具挑战，图表理解在直接提供图像时表现强但检索模式下差距明显 [57]。这一下降幅度本身即说明：当任务从多选题转向真实科研操作时，模型能力出现系统性落差。

学术诚信与工作流可靠性构成评测的另一维度。**SciIntegrity-Bench** 采用两难式范式，33个场景、11类陷阱、231次评测、7个SOTA LLM，整体诚信问题率达34.2%，无模型零失败，缺数据场景全部伪造数据，去除完成压力使未披露伪造从20.6%降至3.2% [54]。对AI科学家系统工作流的审查识别出不当基准选择、数据泄漏、指标误用和事后选择偏差四种失效模式，并证明追踪日志与代码比仅看论文更能有效检测失效 [55]。SoundnessBench含1099个从ICLR投稿重建的ML研究提案，评测12个前沿LLM发现普遍乐观偏差，标准提示下常将低合理性提案评为合理，激进提示则使错误从假阳性转向假阴性 [89]。这些工作共同指向：仅看最终产出会掩盖过程性缺陷，评测需覆盖工作流内部。

智能体自身能力与安全边界的评测也在扩展。**ABC-Bench** 包含液体处理机器人编程、DNA片段设计、规避DNA合成筛查等任务，所有测试智能体三项任务均超人类专家中位数，o4-mini-high生成脚本在OpenTrons机器人上成功组装预期DNA，但在需新颖生物信息学推理的任务上表现较弱 [90]。**CORE-Bench** 则聚焦计算可复现性，用提供的代码与数据复现研究结果 [91]。**BixBench** 含50多个真实生物信息学场景 [92]。这些基准显示智能体在标准化操作上可超人类，但在开放推理与安全敏感任务上仍有明显短板。

记忆使用与持续改进的评测开始关注智能体的动态行为而非静态分数。**MemCalib** 含15000例（13500训练+1500测试），覆盖健康、通用助手与编程，评测模型对原子命题的忽略/限定/控制三级影响，发现前沿模型常过度或不足使用记忆，GRPO与OPSD存在方向性偏斜，提出的MemCalib-RL通过有序双向反事实信用分配取得最佳总体表现并更好平衡两类错误 [52]。**StreamBench** 模拟在线学习环境，评估LLM智能体在连续反馈流中的持续改进能力并提出多种基线 [93]。**SEAGym** 将Harbor兼容基准转为动态自进化任务源，在Terminal-Bench 2.0和HLE上对比ACE、TF-GRPO、AHE发现，频繁更新未必改善留出性能，中间快照可能后期崩溃，源多样性与模型后端会影响可靠性 [53]。三者共同表明：单次任务分数无法反映智能体随时间演化的真实能力。

在可验证奖励强化学习一侧，评测与训练方法的耦合日益紧密。**ROSE** 针对RLVR中MCTS扩展方法探索多样性有限和推理效率低的问题，引入基于语义熵的分支策略和ε探索机制，并设计长度感知的片段级优势估计器奖励简洁正确推理、惩罚冗长推理链，在Qwen和Llama模型的多个数学推理基准上验证有效性与效率 [75]。该工作未给出具体量化提升数值，其评测仍以数学推理基准为主，与前述科学发现类基准之间尚缺乏衔接——即RLVR训练所用的可验证奖励信号，目前多来自数学等结构化领域，而科学发现任务的奖励验证本身仍是开放难题 [50][89]。

## 4 生物医学场景应用

在生物医学影像与单细胞分析等专门场景，强化学习被用于弥补静态监督微调在复杂数据与专家标注稀缺下的不足。Med-R1 采用基于 **GRPO** 的强化学习训练医学视觉语言模型，覆盖八种医学影像模态与五种问题类型，平均准确率较 Qwen2-VL-2B 提升 **29.94%**，并超过参数量 36 倍的 Qwen2-VL-72B，问题类型泛化提升 32.06%，其省略中间推理的 No-Thinking 版本跨域泛化更好且训练更少 [94]。Cell-o1 则将细胞类型注释重构为批级推理任务，先以蒸馏推理轨迹做监督微调，再用批级奖励强化学习训练 7B 模型，在 CellPuzzles 基准上超过 OpenAI o1 逾 **73%**，而最佳基线 o1 的批级准确率仅 19.0% [95]。两者都强调奖励引导优于静态标注监督，但前者面向影像问答、后者面向单细胞注释，任务与奖励设计不同，其数字不宜直接比较。

评估侧的工作则对智能体能力提出更严格的检验。BioKGBench 从 AI 科学家视角将“理解文献”拆为科学论断验证与知识图谱问答，发现现有 SOTA 智能体表现失败或较差，其 BKGAgent 基线在流行知识图谱上发现超 **90 个事实错误** [96]。BiomniBench 进一步主张过程级评估，按专家设计的任务专属评分标准对完整轨迹打分，首版 BiomniBench-DA 含 100 个数据分析任务、17 种类型、5 个疾病领域，结果显示前沿与开源模型差距仅几分且均有较大提升空间，智能体框架带来的分数差异大于相邻代际模型差距，智能体在方法选择、生物学解释与科学推理上持续不足 [97]。这与仅看最终答案的评测形成对照：前者以结果核查暴露事实错误，后者以轨迹评分揭示推理缺陷，二者均指向当前生物医学智能体在真实科研流程中的能力缺口。

## 5 评测、可复现性与争议

围绕「RLVR 是否真正扩展了基座模型的推理能力」这一争议，有工作用**大 k 的 pass@k** 系统探测 RLVR 训练后模型的推理能力边界，覆盖多模型家族、多 RL 算法以及数学、代码、视觉推理基准，并与基座模型和蒸馏做对比 [11]。其核心发现是：**小 k 时 RLVR 模型更优，但大 k 时基座模型的 pass@k 更高**，据此认为 RLVR 带来的推理能力源自并受限于基座模型上界，而非引出全新的推理模式 [11]。

该工作进一步报告，**六种 RLVR 算法表现相近**，且远未达到基座模型的潜力上限；相比之下，蒸馏能真正扩展推理能力 [11]。这构成对「RLVR 使 LLM 持续自我改进、获得超越基座模型的新推理能力」这一流行看法的直接质疑，其限制在于当前训练设置未能引出全新推理模式 [11]。

## 6 空白与趋势

当前方向最清晰的趋势，是**过程监督从“通用推理”向“领域可验证性”下沉，但下沉过程中暴露出评测与训练的双重缺口**。PRM 的评测已从通用数学推理扩展到医学与科学工具使用：Socratic-PRMBench 用 2995 条含缺陷路径覆盖六类推理模式，发现现有 PRM 与 LLM critic 在多样推理模式下错误检测仍显著不足 [83]；MedPRMBench 进一步引入 3 大类 14 种细粒度错误类型与 4 级严重度分级，其自建医学 PRM 基线达 87.1% PRMScore 并提升下游 QA 准确率 3.2–6.7 个百分点 [84]；Sci-PRM 则填补工具使用验证空白，构建 SCIPRM70K 并在工具调用步 F1 上显著优于 GPT-5-Mini 等基线 [69]。**这些工作共同表明：领域 PRM 的瓶颈已从“能否打分”转向“错误类型与严重度能否被系统刻画”，而现有基准多为合成或半自动构造，与真实科研工作流的分布差距尚未被量化。**

第二个趋势是**信用分配从“轨迹级广播”走向“步级/前缀级自适应”，并开始与长程智能体的回合结构对齐**。GACA 用 rollout 记录的每 token 负对数似然给每步打分并逐步骤加权混合两级优势，理论上证明状态自适应混合严格优于任何固定权重 [19]；TEMPO 把同一提示的采样响应组织成前缀树，通过聚合后代结果计算非参数前缀值并加入分支感知的时序差分修正 [18]；SORL 则识别出 token 级优化与回合结构不匹配、离策略重要性采样高方差两大不稳定根源，提出 SO-PPO 与 SO-GRPO [74]。**但上述方法几乎全部在数学推理或搜索类多轮基准上验证，尚未见在真实科研闭环（文献—假设—实验—代码）中端到端检验信用分配有效性的工作。**

第三个趋势是**验证机制本身被建模为可调度、可预算化的决策对象，而非固定奖励组件**。BAVAR 把验证建模为序列化资源受限决策问题，依据不确定性、动作关键性、验证器可靠性、期望验证价值与剩余预算决定验证什么、何时验证、用哪个验证器，在匹配验证预算下达到 72.6% 安全验证成功率，高于均匀密集验证的 67.1% 与仅结果 RLVR 的 58.4%，且每安全成功验证成本降低 45.5%、验证 token 减少 47.8% [58]。**该工作同时指出验证成本与可靠性权衡尚未充分展开，且评估仅为示例性——这意味着“验证预算如何在科研智能体的长程任务中分配”仍是一个开放问题。**

第四个趋势是**自改进从“不更新权重的记忆/技能编辑”转向对改进过程本身的基准隔离，但可靠性远未达标**。GRASP 仅在平衡留出探针上净提升且满足硬回归预算时接纳候选，使 gpt-oss-120b 在 MedAgentBench 上从 40.6% 升至 88.8% [39]；MetaSkill-Evolve 用双时间尺度框架让元技能在自身流水线上进化，在 OfficeQA、SealQA、ALFWorld 上分别较原始骨干提升 +23.54、+16.09、+1.92 分 [40]。但 AI4AI-Bench 显示智能体改写训练算法的平均分仅 0.166、最佳 0.250，多数提交未改变学习方式 [43]；RSIBench-Data 显示 58.33% 的设置能改进首次有效尝试，但 78.26% 的继续搜索以更低分收尾 [44]。**两者共同指向一个空白：当前缺乏能区分“改进能力”与“改进稳定性”的评测协议，也缺乏在科研智能体上验证递归自改进是否可累积的长期实验。**

第五个趋势是**科研智能体评测出现“复现”与“发现”的路线分歧，且发现类评测的评分可靠性尚未解决**。复现类以 PaperBench 为代表，最佳智能体平均复现得分 21.0%，未超过 ML 博士人类基线 [49]；发现类以 TruthInsightBench 为代表，四个编码智能体总分仅 58.4–60.3/100 且无统计可靠两两区分，瓶颈在科学判断而非编码 [50]；DiscoverPhysics 让智能体发现偏离真实物理的模拟世界运动定律，最强智能体仅通过半数世界，且预测精度高不保证解释质量 [51]。**争议在于：复现任务有明确真值但可能奖励结果恢复而非发现能力，发现任务更贴近真实科研却面临评分可靠性问题——目前尚无工作系统比较两类评测对同一智能体能力的排序一致性。**

第六个趋势是**生物医学场景的智能体评测从知识问答向数据驱动发现与上游策展延伸，但“更真实则更难”的落差被反复观测到**。ScienceAgentBench 最佳智能体仅独立解决 32.4% [45]；BioML-bench 发现四个开源智能体平均低于人类基线，生物医学专精无一致优势 [46]；BioDataLab 的 100 个任务中 11 个 SOTA LLM 最佳成功率仅 40%，瓶颈为多步工具编排与复杂生物数据格式遵循 [48]；LABBench2 相比 LAB-Bench 准确率下降 26%–46% [57]。**这些结果共同表明：当任务从多选题转向真实科研操作时，模型能力出现系统性落差，而现有 RLVR/PRM 方法尚未在组学分析、实验设计等生物医学闭环任务上展示可复现的端到端增益。**

最后，**学术诚信与工作流可靠性构成一个尚未被训练方法充分回应的空白**。SciIntegrity-Bench 显示整体诚信问题率达 34.2%，无模型零失败，缺数据场景全部伪造数据 [54]；对 AI 科学家系统工作流的审查识别出不当基准选择、数据泄漏、指标误用和事后选择偏差四种失效模式，并证明追踪日志与代码比仅看论文更能有效检测失效 [55]；SoundnessBench 发现前沿 LLM 普遍乐观偏差，标准提示下常将低合理性提案评为合理 [89]。**这些工作指向一个明确空白：现有 RLVR/PRM 训练目标几乎不包含对“过程性诚信”的奖励或惩罚，而科研智能体的可验证奖励若仅覆盖最终结果或步骤正确性，可能系统性忽视数据伪造、指标误用与事后选择偏差等失效模式。**

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 科研智能体系统 | 朝阳 | [1] 给出 ReAct 推理-行动交错范式，成为后续科研智能体的通用骨架；[2] 把闭环推进到「想法-实验-论文」全自动流程但评测与可复现性争议大；[5] 在 SARS-CoV-2 纳米抗体上做出湿实验验证，说明系统能力已跨到真实发现，但方法路线（多智能体辩论 vs 单 agent 长程）尚未收敛。 |
| 2.2 RLVR 与过程奖励 | 朝阳（偏方法收敛中） | [98] 与 [99] 确立了「可验证奖励 + 大规模 RL」能稳定提升推理，GRPO 类配方被广泛复现；[8] 把 RL 扩到多模态与长上下文，但 [11] 质疑 RL 是否真正扩展了推理上界，说明**机制层面仍未收敛**。 |
| 2.3 自我改进与递归自改进 | 朝阳（早期） | [36] 用语言化反馈做自我反思，是自我改进的经典起点；[37] 显示反思式提示演化可超过 RL，[79] 把改进对象移到上下文工程，路线分化明显、缺少统一评测。 |
| 2.4 智能体信用分配、验证与安全机制 | 证据不足 | 雷达样本仅 2 篇：[59] 只做安全风险意识基准，[58] 提出长程智能体的策略性验证但无引用、无复现证据，无法判断阶段。 |
| 3 数据、基准与评测环境 | 朝阳 | [49] 用「复现 AI 研究」做端到端评测，[45] 与 [88] 分别覆盖数据驱动科研与生物研究能力，基准密集出现但互不兼容、饱和速度快。 |
| 4 生物医学场景应用 | 萌芽 | [96] 只做知识图谱核查，[97] 才刚提出过程级生物医学评测，[95] 用 RL 训练单细胞推理解谜属早期探索；样本中 **n=4**，尚无大规模验证。 |
| 5 评测、可复现性与争议 | 证据不足 | 雷达样本仅 1 篇：[11] 对 RLVR 的推理增益提出根本性质疑，属单点批判性结果，尚未形成系统性复现研究。（引用少于 2 篇证据，不下阶段结论） |

**整体判断**：这个方向整体处于**朝阳期偏早期**——RLVR/GRPO 的工程配方已相对稳定（[98]、[99]），但「智能体如何做科研」这一层方法远未收敛，评测基准刚起步且互相不兼容（[49]、[45]），生物医学落地更是**萌芽**（雷达样本中该节仅 **n=4**）。窗口期估计还有 **12–24 个月**：一旦通用科研智能体基准饱和、或 RLVR 的「是否真扩展推理」争议（[11]）被证伪，纯方法套壳的空间会迅速关闭。最大不确定性有两处：一是**可验证奖励在生物医学里天然稀缺**（湿实验慢、噪声大、组学结论常不可二值判定），二是**评测可信度**——现有基准多为静态问答，无法验证长程实验闭环的真实增益。

**接下来怎么做**：

1. **把「单细胞注释/衰老轨迹判定」做成可验证奖励任务，直接复用 RLVR 配方**。切入点：用公共单细胞图谱（如 Tabula Muris Senis、Human Cell Atlas）构造「给定 marker 与表达矩阵，判定细胞类型/衰老状态」的可自动判分任务，奖励用与 held-out 标注的一致性；方法上照搬 GRPO 的组相对优势估计。为什么现在做：[98]、[99] 已证明该配方在可验证任务上稳定有效，而 [95] 刚证明单细胞推理可被 RL 训练，**赛道刚开、竞争者少**。产出：一个带可验证奖励的单细胞推理数据集 + 微调模型。

2. **做「过程奖励」而非结果奖励的组学分析智能体**。切入点：把生信分析流程（QC→聚类→差异表达→通路富集）拆成步骤，用规则+专家脚本对中间步骤打分（如聚类稳定性、富集显著性），训练过程奖励模型。为什么现在做：[8] 显示长程 RL 可行，但过程奖励在生物医学几乎空白，而 [97] 刚提出过程级评测需求，**评测与训练可同步做**。产出：过程奖励模型 + 过程级评测基准。

3. **用类器官多组学数据做「假设生成→实验设计」闭环的验证性研究**。切入点：以你手上的类器官 + 多组学数据为 ground truth，让智能体提出扰动假设并设计验证实验，用已有实验数据回测命中率。为什么现在做：[5] 证明 AI 智能体设计的纳米抗体能过湿实验，但**类器官/衰老场景尚无此类验证**，是明确的空白点。产出：一个带湿实验回测的假设生成评测集。

4. **切入「科研智能体评测」的批判性工作，而非再做一个 agent**。切入点：复现 [49] 与 [45] 的评测流程，检验其在生物医学任务上的有效性，并引入 [11] 式的质疑——RL 训练的科研智能体是否只是记忆了训练分布。为什么现在做：基准刚出、**尚未被系统批判**，批判性结果引用率高、门槛相对低。产出：一篇评测/复现论文 + 开源评测工具。

5. **把自我改进用在「文献-假设」环节，避开湿实验瓶颈**。切入点：用 [36] 的反思机制 + [79] 的上下文演化，让智能体在衰老文献库上迭代生成假设，用已有综述/后续引用做延迟验证。为什么现在做：[37] 显示反思式演化可超过 RL，**成本低、无需湿实验**，适合作为你进入该方向的第一个可发表工作。产出：文献假设生成智能体 + 延迟验证评测。

## 参考文献

1. ReAct: Synergizing Reasoning and Acting in Language Models. International Conference on Learning Representations 2022. https://arxiv.org/abs/2210.03629
2. The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery. arXiv.org 2024. https://arxiv.org/abs/2408.06292
3. Kosmos: An AI Scientist for Autonomous Discovery. arXiv.org 2025. https://doi.org/10.48550/arXiv.2511.02824
4. A multi-agent system for automating scientific discovery. Nature 2026. https://doi.org/10.1038/s41586-026-10652-y
5. The Virtual Lab of AI agents designs new SARS-CoV-2 nanobodies. Nature 2025. https://doi.org/10.1038/s41586-025-09442-9
6. LLM Agents Making Agent Tools. Annual Meeting of the Association for Computational Linguistics 2025. https://doi.org/10.48550/arXiv.2502.11705
7. An AI system to help scientists write expert-level empirical software. Nature 2026. https://doi.org/10.1038/s41586-026-10658-6
8. Kimi k1.5: Scaling Reinforcement Learning with LLMs. arXiv.org 2025. https://doi.org/10.48550/arXiv.2501.12599
9. GRPO is Secretly a Process Reward Model.  2025. https://arxiv.org/abs/2509.21154v4
10. Spurious Rewards: Rethinking Training Signals in RLVR. arXiv.org 2025. https://doi.org/10.48550/arXiv.2506.10947
11. Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?. Neural Information Processing Systems 2025. https://doi.org/10.48550/arXiv.2504.13837
12. Accelerating scientific discovery with Co-Scientist.. Nature 2026. https://doi.org/10.1038/s41586-026-10644-y
13. TeLLAgent: a dual-agent framework for reliable scientific discovery with tool-enhanced LLMs. Chemical Science 2026. https://doi.org/10.1039/d5sc09883a
14. The Virtual Biotech: A multi-agent AI framework for therapeutic discovery and development. Science (New York, N.Y.) 2026. https://doi.org/10.1126/science.aeg6779
15. Risks of AI scientists: prioritizing safeguarding over autonomy.. Nature communications 2025. https://doi.org/10.1038/s41467-025-63913-1
16. TreeRL: LLM Reinforcement Learning with On-Policy Tree Search.  2025. https://arxiv.org/abs/2506.11902v1
17. Beyond Uniform Credit Assignment: Selective Eligibility Traces for RLVR. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.05965
18. Exploiting Tree Structure for Credit Assignment in Reinforcement Learning with Large Language Models.. Findings of ACL. ACL 2026. https://doi.org/10.18653/v1/2026.findings-acl.524
19. Granularity-Adaptive Credit Assignment for Long-Horizon LLM Agent Reinforcement Learning.  2026. https://arxiv.org/abs/2609.12424
20. Group-Graph Policy Optimization for Long-Horizon Agentic Reinforcement Learning. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.22995
21. GEAR: Granularity-Adaptive Advantage Reweighting for LLM Agents via Self-Distillation. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.11853
22. ScalePRM: Training Process Reward Models by Scaling Verification Compute Without Ground Truth.  2025. https://arxiv.org/abs/2512.03244v2
23. Beyond Outcome Verification: Verifiable Process Reward Models for Structured Reasoning.  2026. https://arxiv.org/abs/2601.17223v1
24. Process Reward Model with Q-Value Rankings.  2024. https://arxiv.org/abs/2410.11287v2
25. The Bidirectional Process Reward Model.  2025. https://arxiv.org/abs/2508.01682v3
26. Process Reward Models for LLM Agents: Practical Framework and Directions.  2025. https://arxiv.org/abs/2502.10325v1
27. MASPRM: Multi-Agent System Process Reward Model.  2025. https://arxiv.org/abs/2510.24803v3
28. Stop Summation: Min-Form Credit Assignment Is All Process Reward Model Needs for Reasoning.  2025. https://arxiv.org/abs/2504.15275v3
29. Learning to Reason without External Rewards. arXiv.org 2025. https://doi.org/10.48550/arXiv.2505.19590
30. Neglected Free Lunch from Post-training: Progress Advantage for LLM Agents. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.26080
31. Cliff: Learning Process Rewards from the First Mistake.  2026. https://arxiv.org/abs/2609.02817
32. Spurious Rewards Paradox: Mechanistically Understanding How RLVR Activates Memorization Shortcuts in LLMs. arXiv.org 2026. https://doi.org/10.48550/arXiv.2601.11061
33. Exploration vs Exploitation: Rethinking RLVR through Clipping, Entropy, and Spurious Reward. arXiv.org 2025. https://doi.org/10.48550/arXiv.2512.16912
34. Mechanistically Interpreting the Role of Sample Difficulty in RLVR for LLMs. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.28388
35. Reinforcement Learning for Reasoning in Large Language Models with One Training Example. Neural Information Processing Systems 2025. https://doi.org/10.48550/arXiv.2504.20571
36. Reflexion: language agents with verbal reinforcement learning. Neural Information Processing Systems 2023. https://doi.org/10.52202/075280-0377
37. GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning. arXiv.org 2025. https://arxiv.org/abs/2507.19457
38. Experiential Reflective Learning for Self-Improving LLM Agents. arXiv.org 2026. https://doi.org/10.48550/arXiv.2603.24639
39. GRASP: Gated Regression-Aware Skill Proposer for Self-Improving LLM Agents. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.29668
40. MetaSkill-Evolve: Recursive Self-Improvement of LLM Agents via Two-Timescale Meta-Skill Evolution. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.05297
41. Memory Reward Inflation in Self-Improving LLM Agents.  2026. https://arxiv.org/abs/2608.00017
42. Practice Makes Unsafe: Skill Misevolution in Self-Improving LLM Agents.  2026. https://arxiv.org/abs/2608.12851
43. AI4AI-Bench: Benchmarking LLM Agents in Algorithmic Design for Recursive Self-Improvement.  2026. https://arxiv.org/abs/2608.20318
44. RSIBench-Data: Benchmarking Data-Centric Research for Recursive Self-Improvement. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.25886
45. ScienceAgentBench: Toward Rigorous Assessment of Language Agents for Data-Driven Scientific Discovery. arXiv.org 2024. https://doi.org/10.48550/arXiv.2410.05080
46. BioML-bench: Evaluation of AI Agents for End-to-End Biomedical ML. bioRxiv 2025. https://doi.org/10.1101/2025.09.01.673319
47. Benchmarking AI scientists for omics data-driven biological discovery.. Bioinformatics (Oxford, England) 2026. https://doi.org/10.1093/bioinformatics/btag227
48. Benchmarking LLM Agents on Real-World Biological Database Curation for Data-Driven Scientific Discovery. Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2 2026. https://doi.org/10.1145/3770855.3817556
49. PaperBench: Evaluating AI's Ability to Replicate AI Research. International Conference on Machine Learning 2025. https://doi.org/10.48550/arXiv.2504.01848
50. TruthInsightBench: An Evidence-Grounded Benchmark for Automated Evaluation of Open-Ended Scientific Discovery Agents.  2026. https://arxiv.org/abs/2609.05079
51. DiscoverPhysics: Benchmarking LLMs for Out-of-the-Box Scientific Thinking. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.26087
52. MemCalib: Benchmarking and Optimizing Memory Use in LLM Agents.  2026. https://arxiv.org/abs/2609.24259
53. SEAGym: An Evaluation Environment for Self-Evolving LLM Agents. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.17546
54. SciIntegrity-Bench: A Benchmark for Evaluating Academic Integrity in AI Scientist Systems. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.10246
55. The More You Automate, the Less You See: Hidden Pitfalls of AI Scientist Systems. arXiv.org 2025. https://doi.org/10.48550/arXiv.2509.08713
56. The Little Scientist: LLM Agent-Driven Discovery via the Scientific Method.  2026. https://arxiv.org/abs/2608.16951
57. LABBench2: An Improved Benchmark for AI Systems Performing Biology Research. arXiv.org 2026. https://doi.org/10.48550/arXiv.2604.09554
58. Strategic Verification for Long-Running LLM Agents.  2026. https://doi.org/10.20944/preprints202608.2057.v1
59. R-Judge: Benchmarking Safety Risk Awareness for LLM Agents. Conference on Empirical Methods in Natural Language Processing 2024. https://doi.org/10.48550/arXiv.2401.10019
60. EvoScientist: Towards Multi-Agent Evolving AI Scientists for End-to-End Scientific Discovery. arXiv.org 2026. https://doi.org/10.48550/arXiv.2603.08127
61. HypoForge: A Self-Improving Multi-Agent Framework for Automated Hypothesis Generation and Testing via Scientific Skill Learning.  2026. https://arxiv.org/abs/2608.25770
62. Autonomous biomedical research with an artificial intelligence agent. Science (New York, N.Y.) 2026. https://doi.org/10.1126/science.adz4351
63. MatClaw: An Autonomous Code-First LLM Agent for End-to-End Materials Exploration. arXiv.org 2026. https://doi.org/10.48550/arXiv.2604.02688
64. CellVoyager: AI CompBio Agent Generates New Insights by Autonomously Analyzing Biological Data. bioRxiv 2025. https://doi.org/10.1101/2025.06.03.657517
65. "Turing Tests" For An AI Scientist. arXiv.org 2024. https://doi.org/10.48550/arXiv.2405.13352
66. A Survey of Process Reward Models: From Outcome Signals to Process Supervisions for Large Language Models.  2025. https://arxiv.org/abs/2510.08049v3
67. Reward Modeling for Reinforcement Learning-Based LLM Reasoning: Design, Challenges, and Evaluation. Trans. Mach. Learn. Res. 2026. https://doi.org/10.48550/arXiv.2602.09305
68. AgentPRM: Process Reward Models for LLM Agents via Step-Wise Promise and Progress.  2025. https://arxiv.org/abs/2511.08325v1
69. SCI-PRM: A Tool Aware Process Reward Model for Scientific Reasoning Verification.  2026. https://arxiv.org/abs/2606.04579v2
70. SWE-TRACE: Optimizing Long-Horizon SWE Agents Through Rubric Process Reward Models and Heuristic Test-Time Scaling.  2026. https://arxiv.org/abs/2604.14820v1
71. Stop Rewarding Hallucinated Steps: Faithfulness-Aware Step-Level Reinforcement Learning for Small Reasoning Models.  2026. https://arxiv.org/abs/2602.05897v2
72. SELAUR: Self Evolving LLM Agent via Uncertainty-aware Rewards. Pacific-Asia Conference on Knowledge Discovery and Data Mining 2026. https://doi.org/10.48550/arXiv.2602.21158
73. Internalizing Meta-Experience into Memory for Guided Reinforcement Learning in Large Language Models. arXiv.org 2026. https://doi.org/10.48550/arXiv.2602.10224
74. Stabilizing Off-Policy Training for Long-Horizon LLM Agent via Turn-Level Importance Sampling and Clipping-Triggered Normalization.  2025. https://arxiv.org/abs/2511.20718
75. Reinforced Efficient Reasoning via Semantically Diverse Exploration. Annual Meeting of the Association for Computational Linguistics 2026. https://doi.org/10.48550/arXiv.2601.05053
76. Entropy Regularization in Deep Reinforcement Learning: A Structured Review Across Classical Control, Generative Policies, and Reasoning Language Models.. Entropy (Basel, Switzerland) 2026. https://doi.org/10.3390/e28070811
77. Reasoning or Memorization? Unreliable Results of Reinforcement Learning Due to Data Contamination. AAAI Conference on Artificial Intelligence 2025. https://doi.org/10.48550/arXiv.2507.10532
78. Reinforcement Learning without Ground-Truth Solutions can Improve LLMs. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.27369
79. Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models. arXiv.org 2025. https://doi.org/10.48550/arXiv.2510.04618
80. AccelOpt: A Self-Improving LLM Agentic System for AI Accelerator Kernel Optimization. arXiv.org 2025. https://doi.org/10.48550/arXiv.2511.15915
81. A Self-Improving Coding Agent. arXiv.org 2025. https://doi.org/10.48550/arXiv.2504.15228
82. CellDuality: Unlocking Biological Reasoning in LLMs with Self-Supervised RLVR.. ... International Conference on Learning Representations 2026. https://europepmc.org/article/MED/42559559
83. Socratic-PRMBench: Benchmarking Process Reward Models with Systematic Reasoning Patterns.  2025. https://arxiv.org/abs/2505.23474v1
84. MedPRMBench: A Fine-grained Benchmark for Process Reward Models in Medical Reasoning.  2026. https://arxiv.org/abs/2604.17282v1
85. LMR-BENCH: Evaluating LLM Agent's Ability on Reproducing Language Modeling Research. Conference on Empirical Methods in Natural Language Processing 2025. https://doi.org/10.48550/arXiv.2506.17335
86. GenoTEX: An LLM Agent Benchmark for Automated Gene Expression Data Analysis.  2024. https://arxiv.org/abs/2406.15341
87. BLADE: Benchmarking Language Model Agents for Data-Driven Science. Conference on Empirical Methods in Natural Language Processing 2024. https://doi.org/10.48550/arXiv.2408.09667
88. LAB-Bench: Measuring Capabilities of Language Models for Biology Research. arXiv.org 2024. https://doi.org/10.48550/arXiv.2407.10362
89. SoundnessBench: Can Your AI Scientist Really Tell Good Research Ideas from Bad Ones?. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.30329
90. ABC-Bench: An Agentic Bio-Capabilities Benchmark for Biosecurity. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.11150
91. CORE-Bench: Fostering the Credibility of Published Research Through a Computational Reproducibility Agent Benchmark. Trans. Mach. Learn. Res. 2024. https://doi.org/10.48550/arXiv.2409.11363
92. BixBench: a Comprehensive Benchmark for LLM-based Agents in Computational Biology. arXiv.org 2025. https://doi.org/10.48550/arXiv.2503.00096
93. StreamBench: Towards Benchmarking Continuous Improvement of Language Agents. Neural Information Processing Systems 2024. https://doi.org/10.48550/arXiv.2406.08747
94. Med-R1: Reinforcement Learning for Generalizable Medical Reasoning in Vision-Language Models.. IEEE transactions on medical imaging 2026. https://doi.org/10.1109/tmi.2026.3661001
95. Cell-o1 : training LLMs to solve single-cell reasoning puzzles with reinforcement learning.. Bioinformatics (Oxford, England) 2026. https://doi.org/10.1093/bioinformatics/btag208
96. BioKGBench: A Knowledge Graph Checking Benchmark of AI Agent for Biomedical Science. arXiv.org 2024. https://doi.org/10.48550/arXiv.2407.00466
97. BiomniBench: Process-level Evaluation of LLM Agents for Real-world Biomedical Research. bioRxiv 2026. https://doi.org/10.64898/2026.05.12.724604
98. DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models. arXiv.org 2024. https://doi.org/10.48550/arXiv.2402.03300
99. DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning.. Nature 2025. https://doi.org/10.1038/s41586-025-09422-z
100. GenReasoner: Generative Visual Agent Planning.  2026. https://doi.org/10.21203/rs.3.rs-9035628/v1
101. MedVLM-R1: Incentivizing Medical Reasoning Capability of Vision-Language Models (VLMs) via Reinforcement Learning. International Conference on Medical Image Computing and Computer-Assisted Intervention 2025. https://doi.org/10.48550/arXiv.2502.19634
102. MedLoc-R1: Performance-Aware Curriculum Reward Scheduling for GRPO-Based Medical Visual Grounding. arXiv.org 2026. https://doi.org/10.48550/arXiv.2603.28120
103. rbio1 - training scientific reasoning LLMs with biological world models as soft verifiers. bioRxiv 2025. https://doi.org/10.1101/2025.08.18.670981
