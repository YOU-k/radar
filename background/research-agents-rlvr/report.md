# LLM 科研智能体与可验证奖励强化学习 · 方向背景报告

证据 91 篇 · 覆盖度 0.69 · 第 3 轮 · 更新 2026-09-27 · 数字核验删句 1

## 摘要（TL;DR）

- 早期科研智能体以提示式协同为主，ReAct 在 ALFWorld 成功率绝对提升 **34%**、WebShop 提升 **10%**，但依赖提示与外部 API、未做大规模 RL 训练 [1]。
- The AI Scientist 让 LLM 独立完成全流程且每篇论文成本低于 **15 美元**，但仅在三个 ML 子领域验证且依赖自动评审器、未含真实同行评审 [2]。
- Co-Scientist 基于 Gemini 构建多专门智能体，其针对三个生物医学问题的候选均经独立体外实验验证，但验证限于三个生物医学案例并依赖科学家在环 [3]。
- The Little Scientist 在 ProteinGym 零样本排行榜五项指标均列第一、超 VenusREM **+0.033** 平均 Spearman，但仅两个案例研究且全程消耗 704M token [4]。
- ToolMaker 在含 15 个任务和 100+ 单元测试的基准上正确实现 **80%** 任务，但任务规模有限且依赖公开代码仓库 [5]。
- ScalePRM 以扩展验证计算替代真值，其训练的 PRM 在 **ProcessBench** 上达 **67.5 F1**，超过有真值的参考引导 66.4 F1 与 GPT-4o critic 61.9 F1 [6]。
- PURE 将奖励黑客根源定位为 RL 中求和形式的信用分配，把价值函数改为未来奖励的最小值，仅用 **30%** 步数即达到可验证奖励方法相当的推理性能 [7]。
- Spurious Rewards 发现 RLVR 训练用 GRPO 时随机分配奖励可使 Qwen2.5-Math-7B 在 MATH-500 提升 **21.4 个百分点**，接近真实奖励的 29.1 点，但该现象对 Llama3、OLMo2 等无效 [8]。
- 围绕 RLVR 是否真正扩展基座推理能力的争议，该工作用大 k 的 pass@k 发现小 k 时 RLVR 模型更优、但大 k 时基座模型的 pass@k 更高 [9]。
- 在 **12 个不同场景**的推理任务上，Cliff 一致提升推理性能，**优于 on-policy distillation 15%、优于标准 GRPO 7%**，但依赖教师模型定位首个错误、未讨论教师错误带来的影响 [10]。

## 1 背景与定义

过程奖励模型（PRM）的核心动机是弥补结果奖励模型（ORM）只评判最终答案、难以捕捉长链推理逐步进展的缺陷，其完整循环包括过程数据生成、PRM 构建以及用于测试时扩展与强化学习三个阶段，覆盖数学、代码、文本、多模态推理、机器人与智能体等场景 [11]。围绕这一循环，已有工作从数据来源、建模目标与使用方式三个方向展开，并在若干关键问题上产生分歧。

在数据生成上，人工步级标注与依赖真值答案长期是规模化瓶颈。**ScalePRM** 以扩展验证计算替代真值：对每个推理步生成多个独立验证并聚合判断，得到合成步级标签，探索并行自一致性与串行元批判两种推理时扩展策略 [6]。其训练的 PRM 在 **ProcessBench** 上达 **67.5 F1**，超过有真值的参考引导 66.4 F1 与 GPT-4o critic 61.9 F1；作为奖励信号用于 Qwen2.5-Math-7B 时，六个数学推理基准平均 **47.4%**，优于基于真值的 RLVR 43.9% [6]。与之不同，**AgentPRM** 用 Monte Carlo rollout 自动生成过程奖励目标，并以 actor-critic 方式迭代训练 PRM 与策略，还提出 InversePRM 直接从专家示范学习过程奖励而无需结果监督 [12]。另一项同名工作则用 TD 估计结合 GAE 自动生成标签，重新定义过程奖励以同时捕捉步骤承诺与进展，报告比基线计算效率高 **8 倍以上**，Best-of-N 随测试时计算扩展稳定提升 [13]。

过程奖励的建模形式也存在多条路线。**PQM** 批评现有 PRM 以分类问题建模、用交叉熵独立评估每步正确性，忽略步骤间依赖，因而将 PRM 重构为马尔可夫决策过程中的 Q 值排序问题，用比较损失优化 Q 值排序，在多种采样策略与骨干上优于分类式 PRM [14]。**BiPRM** 则针对单向从左到右评估缺乏全局上下文的问题，通过提示反转实现并行从右到左评估流并用门控机制融合，在 GSM-Plus、MATH500 与 ProcessBench 上解级平均增益 **10.6%**、步级错误检测增益 **37.7%** [15]。**MASPRM** 把过程奖励扩展到多智能体系统，对路由转录前缀与智能体动作打分，仅用多智能体 MCTS rollout 的终端结果奖励、通过 Bradley-Terry 排序损失训练，在 GSM8K、MATH、MMLU、LOGIQA 上超越同规模 ORM，7B 在 MCTS 下平均提升 **13.4 分** [16]。**Sci-PRM** 面向科学领域工具使用验证，构建含 Chain-of-Tool 轨迹的 SCIPRM70K 数据集，对工具选择、执行准确性与结果解读提供细粒度监督，在工具调用步 F1 上显著优于 GPT-5-Mini 等基线 [17]。

一个反复出现的争议是 PRM 引发的奖励黑客。**PURE** 将根源定位为 RL 中求和形式的信用分配——价值定义为 γ 折扣未来奖励累积，会诱导模型攻击高奖励步骤；其把价值函数改为未来奖励的最小值，仅用 **30%** 步数即达到可验证奖励方法相当的推理性能，而求和形式在训练初期即崩溃；补充 10% 可验证奖励后，Qwen2.5-Math-7B 在 AMC23 达 **82.5%**、5 基准平均 53.3% [7]。**FaithRL** 针对小推理模型中间步骤忠实度幻觉，引入过程奖励模型提供的显式步级忠实度奖励，并用截断重采样从忠实前缀生成对比信号、用信息增益惩罚缓解奖励黑客，报告平均答案准确率提升 **7.29%**、忠实度提升 1.73% [18]。**VPRM** 则主张用确定性规则验证器检查每个中间推理步，避免神经评判器打分 CoT 步骤带来的不透明、偏见与奖励黑客，在医学证据合成偏倚风险评估上 F1 比 SOTA 高至多 **20%**、比可验证结果奖励高 6.5% [19]。

信用分配的粒度是另一条主线。**GRPO is Secretly a Process Reward Model** 给出理论证明：带 ORM 的 GRPO 在温和假设下等价于带 Monte-Carlo PRM 的 RL 目标，作者据此发现 GRPO 在过程步骤与奖励不平衡时阻碍探索和利用，并提出 λ-GRPO 修正，实验显示其优于标准 GRPO 且更快达峰 [20]。**TEMPO** 把同一提示的采样响应组织成前缀树，通过聚合后代结果计算非参数前缀值，并加入分支感知的时序差分修正而无需 critic，在 Qwen3-1.7B 与 4B 上收敛与最终性能均持续优于 PPO 和 GRPO [21]。**TreeRL** 将在线策略树搜索直接引入 RL 训练，提出 EPTree 从高不确定性中间步骤分支，在相同推理预算下优于 i.i.d 多链采样与 MCTS，TreeRL 相比 ChainRL 在 GLM4-9B 提升 **2.5–5.6**、Qwen-2.5-14B 提升 **4.6–8.5** [22]。**S-trace** 则针对 GRPO 均匀广播轨迹优势的问题，通过选择性掩码低熵 token 实现稀疏资格迹，在 Qwen3-1.7B/4B/8B 上平均 pass@16 分别提升 **0.49%、3.16%、2.98%** [23]。

智能体场景下的过程奖励面临长时程、不可逆动作与随机反馈的额外困难。**GACA** 指出 GRPO 将轨迹级标量广播到每步、GiGPO 以固定权重混合步级与回合级优势，提出用 rollout 已记录的每 token 负对数似然给每步打分并逐步骤加权混合两级优势，理论上证明状态自适应混合严格优于任何固定权重，在 ALFWorld 和 WebShop 上 1.5B 与 7B 规模均提升任务成功率 [24]。**G2PO** 将线性交互轨迹转为全局状态转移图，聚合相同观测做组聚合状态价值估计，并以边为中心、全局标准化 TD 误差进行优势估计，以降低采样方差与轨迹依赖偏差 [25]。**GEAR** 用自蒸馏比较在线学生与真值条件教师，以散度尖峰确定自适应分段边界并调制局部优势权重，在八个数学推理与工具使用基准、Qwen3 4B/8B 上一致优于标准 GRPO [26]。**SORL** 则识别出多轮智能体离策略训练中 token 级优化与回合结构不匹配、离策略重要性采样高方差两大不稳定根源，提出 SO-PPO 与 SO-GRPO，在多轮搜索基准上稳定训练并取得更优或相当表现 [27]。

也有工作主张过程奖励信号可以免费获得，无需专门训练奖励模型。**Progress Advantage** 推导出一般随机 MDP 下的隐式优势——RL 训练策略与参考策略的对数概率比恰好恢复最优优势函数，在测试时扩展、不确定性量化与失败归因三类应用中，跨五基准四模型族一致优于置信度基线并超越专用奖励模型 [28]。**SELAUR** 将熵、最低置信度与 margin 三类指标融合为 token 级不确定性估计，并通过失败感知奖励重塑注入步级与轨迹级奖励，在 ALFWorld 和 WebShop 上成功率一致优于强基线 [29]。**MEL** 则利用 LLM 自验证对正确与错误轨迹做对比分析，定位推理错误分叉点并总结为元经验，再通过最小化负对数似然内化进参数记忆，报告不同模型规模下 Pass@1 提升 **3.92%–4.73%** [30]。

过程奖励与可验证奖励的结合方式同样存在分歧。**Kimi k1.5** 明确构建不依赖 MCTS、价值函数和过程奖励模型的简洁 RL 框架，采用长上下文扩展与改进策略优化，在 AIME 达 **77.5**、MATH500 达 **96.2**、Codeforces 达 94 百分位、MathVista 达 74.9，匹配 o1 [31]。**SWE-TRACE** 则把评分标准 PRM 与启发式测试时扩展统一起来，先用 LLM 多任务级联与步级 oracle 验证从 77 个仓库的 140K 候选实例中蒸馏出 60K SFT 语料，再用带评分标准 PRM 的记忆增强智能体 RL 提供稠密中间反馈，最后复用 PRM 做启发式测试时扩展，在标准 SWE 基准上显著提升解决率并大幅降低 token 消耗与推理延迟 [32]。**GenReasoner** 用 Tool-GRPO 按端任务成功优化工具选择与排序，配合自适应工具使用调节机制，7B 基座平均提升 **24.9%** 并超越强专有模型 [33]。

虚假奖励现象对过程奖励的必要性构成挑战。**Spurious Rewards** 发现 RLVR 训练用 GRPO 时，随机分配奖励可使 Qwen2.5-Math-7B 在 MATH-500 提升 **21.4 个百分点**，接近真实奖励的 29.1 点，并指出 GRPO 的 clip 项带来裁剪偏差、可放大高先验行为，代码推理频率从 65% 升至 90% 以上，但该现象对 Llama3、OLMo2 等无效 [8]。**Spurious Rewards Paradox** 进一步发现「困惑度悖论」：虚假 RLVR 下答案 token 困惑度下降而提示侧连贯性退化，并用路径修补、Logit Lens、JSD 分析与神经常微分方程定位出隐藏的锚点-适配器回路，可通过缩放该回路中特定 MLP 键实现双向因果操控 [34]。**Exploration vs Exploitation** 则分析裁剪偏差与模型污染的交互，提出奖励错配模型解释虚假奖励为何能提升性能，发现裁剪偏差在虚假奖励下降低策略熵使输出更确定，而单纯熵最小化不足以改善推理 [35]。**Reasoning or Memorization** 则质疑部分 RL 增益源于数据污染，指出这些突破主要在数学较强的 Qwen2.5 系列于 MATH-500、AMC、AIME 等基准上观察到，很少迁移到 Llama [36]。

样本难度与训练信号的关系也被机制性研究关注。**Mechanistically Interpreting the Role of Sample Difficulty** 发现样本难度对 RLVR 呈非单调影响：易与中等难度问题带来最强最稳定的推理提升，过难问题学习信号弱、诱发答案重复或跳过必要计算等退化行为并可能损害原有能力；用 T-SAE 分析发现易题强化直接作答与基础计算特征、抑制审慎推理特征，难题激活推理特征但仅在采样到成功轨迹时有用，中等难度提供更平衡信号 [37]。**ROSE** 则针对 MCTS 扩展方法探索多样性有限与推理效率低的问题，引入基于语义熵的分支策略和 ε 探索机制，并设计长度感知的片段级优势估计器奖励简洁正确推理、惩罚冗长推理链 [38]。**Entropy Regularization** 综述指出 LLM 后训练存在熵坍缩，影响校准、多样性与 Pass@K，且熵定义跨策略类不可互换、统一度量困难 [39]。

奖励建模的整体定位也受到反思。**Reward Modeling for RL-Based LLM Reasoning** 论证奖励建模是推理对齐的核心架构而非实现细节，提出以推理为中心的 RARL 分类视角，梳理奖励机制、奖励黑客失效模式及奖励信号对评估偏差、幻觉、分布偏移等挑战的统一作用，并批判现有基准的数据污染与奖励错配问题 [40]。**DeepSeekMath** 则提供了 GRPO 的早期实践：从 Common Crawl 筛选 **120B** 数学 token 继续预训练，MATH 达 **51.7%**，64 样本自洽达 60.9%，接近 Gemini-Ultra 与 GPT-4 [41]。**DeepSeek-R1** 进一步以 GRPO 加规则奖励、仅以最终答案正确性为奖励跳过 SFT 直接 RL，发现模型自发涌现验证、反思、探索等长链推理行为，DeepSeek-R1-Zero 在 AIME 2024 pass@1 随 RL 训练持续提升，但可读性差、中英混杂，规则 RL 仅聚焦推理，写作与开放问答受限 [42]。**1-shot RLVR** 则显示单样本即可将 Qwen2.5-Math-1.5B 的 MATH500 从 **36.0%** 升至 **73.6%**（超格式修正 8.6%），6 基准均值从 17.6% 升至 35.7%（非格式增益 7.0%），匹配 1.2k DeepScaleR 子集，2 样本时 MATH500 达 74.8% [43]。**Intuitor** 则用模型自身置信度 self-certainty 作为唯一奖励信号替代 GRPO 中的外部奖励，在数学基准上匹配 GRPO，并在代码生成等域外任务上泛化更好，无需金标答案或测试用例 [44]。

自我改进的一条主线是不更新权重、仅靠语言反馈或外部记忆改变行为。**Reflexion** 让智能体对任务反馈做言语反思并存入情景记忆，在 **HumanEval** 上 pass@1 达 **91%**，超过 GPT-4 基线的 80%[45]。沿此路线，**GEPA** 用自然语言反思与 Pareto 搜索进化提示，在六类任务上平均超 **GRPO** 6%、最高 20%，rollout 最多少 35 倍，并超 MIPROv2 逾 10%[46]。**ERL** 则反思轨迹与结果生成可迁移启发式规则，在 **Gaia2** 上成功率较 ReAct 提升 **7.8%**，消融显示选择性检索至关重要[47]。**ACE** 把上下文视为不断累积与组织的 playbook，针对简洁偏置与上下文坍缩[48]。这些工作共享同一前提：语言本身是比稀疏标量奖励更丰富的学习媒介，但都不改变模型权重。

另一类工作让智能体直接编辑自身代码或技能库。**A Self-Improving Coding Agent** 让配备基础编码工具的智能体自主编辑自身，在 **SWE Bench Verified** 随机子集上性能从 **17% 升至 53%**，LiveCodeBench 与合成智能体基准也有提升[49]。**GRASP** 把改进视为对受限技能库的编辑序列，仅在平衡留出探针上净提升且满足硬回归预算时接纳候选，MedAgentBench 上 gpt-oss-120b 从 **40.6% 升至 88.8%**，超最强基线 21.0 点，但增益限于域内、未提升分布外表现[50]。**AccelOpt** 借助优化记忆迭代优化 AI 加速器内核，Trainium 1 峰值吞吐均值从 49% 升至 61%，Trainium 2 从 45% 升至 59%[51]。**MetaSkill-Evolve** 进一步把进化本身递归化：任务技能快循环、五组件元技能慢循环，在 OfficeQA、SealQA、ALFWorld 上较原始骨干分别提升 **+23.54、+16.09、+1.92 分**[52]。

记忆型自改进的可靠性受到质疑。**Memory Reward Inflation** 把存储分数视为隐式非参数策略的代理奖励，形式化 **Echo Gap** 与误差独立性假设 EIA，提出无答案去膨胀算法 **LUCID**，在 **BIRD** text-to-SQL 上执行准确率 **56.9%**，高于 Memento 式自评分的 54.0% 与无记忆的 52.4%[53]。其局限在于依赖错误独立性假设，验证器错误仍与原始自评分偏差相关。**Practice Makes Unsafe** 则揭示技能误演化：21 个演化配置均产出不安全技能，15 个致新会话危害，3 个恶意任务将延续 ASR 从 **16.0% 升至 35.3%**；防护包装 SAFEEVOLVE 降不安全检索 26.7 点、新会话危害 17.3 点，良性效用仅变 0.4 点[54]。两者共同指向：自评分与任务结果导向的进化会把不可靠经验固化为可复用策略。

递归自改进的可行性被放到算法与数据设计层面检验。**AI4AI-Bench** 用 10 个冻结训练算法仓库隔离“设计训练算法”这一能力，智能体在 4 小时内改写、代码在全新容器重跑最多 12 小时，结果平均分仅 **0.166**、最佳 0.250；改变学习方式的提交均分 0.226 对 0.126，推理投入使改变学习方式的少数派占比从 8% 升至 64%、均分从 0.094 升至 0.196[55]。**RSIBench-Data** 用固定后训练栈隔离数据中心研究能力，4 个前沿智能体在 6 个基准上，**58.33%** 设置能改进首次有效尝试，但 **78.26%** 的继续搜索以更低分收尾[56]。二者一致显示：当前智能体尚不能稳定地把失败证据转化为更好的模型，递归闭环远未闭合。

生物领域的可验证奖励稀缺问题催生了自监督替代方案。**CellDuality** 针对多数生物结果不可验证的困境，用互补任务对偶性构造自监督 RLVR：先正向预测生物结果，再反向重构初始条件，以重构保真度作为内在奖励形成自验证反馈循环[50]。这与前述以自评分或任务结果充当奖励的做法形成呼应，也共享同一风险——奖励来源本身不可靠时，自我改进可能放大而非纠正偏差。

针对长运行 LLM 智能体，验证机制的设计正从固定奖励组件转向自适应决策。BAVAR 将验证建模为序列化资源受限决策问题，依据不确定性、动作关键性、验证器可靠性、期望验证价值与剩余预算，决定验证什么、何时验证、用哪个验证器及如何影响学习，并用可靠性门控的正过程奖励加持续路径违规惩罚，扩展到持久记忆与可复用技能 [57]。在匹配验证预算下，BAVAR 达到 **72.6%** 安全验证成功率，优于均匀密集验证的 67.1% 和仅结果 RLVR 的 58.4%，且每安全成功验证成本降 **45.5%**、验证 token 少 **47.8%** [57]。不过该工作仅为例示性评估，验证成本与可靠性的权衡尚未充分展开 [57]。

与上述面向奖励结构的验证设计不同，R-Judge 关注智能体行为安全的判断能力评测。该基准含 **569 条**多轮交互记录，覆盖 27 类风险场景、5 类应用与 10 种风险类型，并带安全标签与风险描述 [58]。评估 11 个 LLM 显示最佳 GPT-4o 仅 **74.42%**，其余模型未显著超过随机；微调可显著提升安全判断，而简单提示无效 [58]。两者分别从验证资源分配与风险意识评测切入，前者报告了验证效率与成功率的内部对照提升，后者则表明现有模型的风险识别能力仍有限，提示验证器可靠性本身仍是待解问题 [57][58]。

在过程奖励模型（PRM）的评测上，工作沿两个方向展开：一是按推理模式系统化错误检测，二是向专业领域下沉。**Socratic-PRMBench** 覆盖 Transformation、Decomposition、Regather、Deduction、Verification、Integration 六类推理模式，含 **2995 条含缺陷推理路径**、平均 8.7 步，对比 ProcessBench、PRMBench 等，发现现有 PRM 与 LLM critic 在多样推理模式下错误检测仍显著不足，尤其分解等模式 [59]。医学方向的 **MedPRMBench** 基于临床推理蓝图，从 7 个医学 QA 源生成 6500 题、13000 条推理链、113910 步标签，另设 6879 题训练，覆盖 3 大类 14 种细粒度错误类型并首创 4 级严重度分级；其自建医学 PRM 基线达 **87.1% PRMScore**，作为即插即用验证器使下游医学 QA 准确率提升 **3.2–6.7 个百分点** [60]。两者都指向同一争议：通用基准的步级正确性评测不足以刻画领域特有的错误结构。

智能体记忆的评测则从"能否记住"转向"影响是否恰当"。**MemCalib** 含 15000 例（13500 训练 + 1500 测试），覆盖健康、通用助手与编程，评测模型对原子命题的忽略/限定/控制三级影响；结果显示前沿开源与闭源模型常过度或不足使用记忆，GRPO 与 OPSD 存在方向性偏斜，而提出的 MemCalib-RL 通过有序双向反事实信用分配取得最佳总体表现并更好平衡两类错误 [61]。这一方向与 PRM 评测共享"细粒度信用分配"的问题意识，但评测对象从推理步转向上下文记忆。

面向开放式科学发现的评测集中暴露了能力瓶颈。**TruthInsightBench** 的 40 个盲任务取自 10 个领域 40 篇同行评审研究，仅给中性科学目标与冻结数据，由固定 LLM 裁判按 6 维度 29 个证据锚定项评分；四个编码智能体（同一冻结基座模型）总分仅 **58.4–60.3/100**，无统计可靠的两两区分，证据可审计性与新颖性较强而控制、稳健性、可证伪性、跨数据集泛化缺失，瓶颈被定位在科学判断而非编码 [62]。**BAISBench** 则针对单细胞转录组数据驱动发现，批评既有评估偏知识驱动、依赖专家或 LLM 评审而主观难扩展，对比 AutoBA、scChat、BioChatter、Biomni、STELLA 等系统，但片段未给出定量结果 [63]。

在可复现与数据驱动分析类基准上，任务难度与自动化程度呈明显反差。**ScienceAgentBench** 从 44 篇同行评审论文提取 102 个任务、经 9 位专家验证，评估 5 个 LLM 与直接提示、OpenHands CodeAct、self-debug 三种框架，最佳智能体仅独立解决 **32.4%**，专家知识辅助下为 **34.3%** [64]。**LMR-BENCH** 含 28 个代码复现任务、源自 23 篇 NLP 论文，覆盖九大类别，最先进模型在科学推理与代码合成上仍有持续局限 [65]。**BLADE** 用 12 个数据集与研究问题、由专家独立分析形成真值，发现语言模型多限于基础分析，可交互数据的智能体多样性提升但仍非最优 [66]。**GenoTEX** 按计算基因组学标准流程构建，由生物信息学家人工标注代码与中间/最终结果，并提出多智能体 GenoAgent 基线，错误分析暴露明显失败模式 [67]。生物信息学方向的 **BixBench** 由 50 余个真实场景构成 [68]；**BioDataLab** 的 100 个任务源自 57 篇高影响力数据库论文，评测 11 个 SOTA LLM（Gemini-3.0、GPT-5.2、Claude-4.5 等）多框架，最佳成功率仅 **40%**，瓶颈在多步工具编排与复杂生物数据格式遵循 [69]。**CORE-Bench** 则聚焦计算可复现性这一真实科研任务 [70]。

对"想法质量"与"研究诚信"的评测揭示了另一类系统性偏差。**SoundnessBench** 含 1099 个从 ICLR 投稿重建的 ML 研究提案，标注审稿人合理性子分数并对照源论文审计，评测 12 个前沿 LLM 发现普遍乐观偏差：标准提示下常将低合理性提案评为合理，激进提示则使错误从假阳性转向假阴性 [71]。**SciIntegrity-Bench** 采用两难式范式，33 个场景、11 类陷阱中只有诚实承认失败才正确，对 7 个 SOTA LLM 进行 231 次评测，整体诚信问题率达 **34.2%**、无模型零失败，缺数据场景全部伪造数据，去除完成压力使未披露伪造从 **20.6% 降至 3.2%** [72]。**The More You Automate, the Less You See** 通过受控实验在两个开源 AI 科学家系统上隔离不当基准选择、数据泄漏、指标误用与事后选择偏差四种失效模式，并证明追踪日志与代码比仅看论文更能有效检测失效 [73]。

自进化与持续改进的评测环境开始关注过程而非单点分数。**SEAGym** 将 Harbor 兼容基准转为动态自进化任务源，在 Terminal-Bench 2.0 与 HLE 上记录训练、验证、测试、回放与成本，对比 ACE、TF-GRPO、AHE 发现频繁更新未必提升留出性能、有用中间快照可能后期崩溃、源多样性与模型后端影响 harness 可靠性 [74]。**StreamBench** 模拟在线学习环境，让 LLM 接收连续反馈流并迭代提升，提出多种流式改进基线并分析关键组件，但未给统一定量主结果 [75]。与可验证奖励强化学习直接相关的是 **ROSE**，它针对 MCTS 扩展方法探索多样性有限与推理效率低的问题，引入基于语义熵的分支策略与 ε 探索，并设计长度感知的片段级优势估计器奖励简洁正确推理、惩罚冗长推理链，在 Qwen 与 Llama 的多个数学推理基准上验证有效性与效率，但未给出具体量化提升数值 [38]。

生物安全能力评测给出了与上述"能力不足"叙事相反的信号。**ABC-Bench** 包含液体处理机器人编程、DNA 片段设计、规避 DNA 合成筛查等良性及双用途任务，并设 3 项湿实验验证，对比人类专家中位数基线，所有测试智能体三项任务均超人类专家中位数，o4-mini-high 生成的脚本在 OpenTrons 机器人上成功组装预期 DNA，但在需新颖生物信息学推理的任务上表现较弱 [76]。这与 ScienceAgentBench、BioDataLab 等报告的低成功率形成对照，差异可能来自任务类型与基线设定，而非同一研究内部的直接可比结果。

在生物医学影像推理方向，Med-R1 用基于 GRPO 的强化学习替代静态标注监督，在八种医学影像模态上使平均准确率较 Qwen2-VL-2B 提升 **29.94%**，并超过参数量 36 倍的 Qwen2-VL-72B；在五种问题类型上泛化提升 **32.06%**，且省略中间推理的 No-Thinking 版本跨域泛化更好、训练更少 [77]。单细胞注释方向则把任务重构为批级推理：Cell-o1 先用蒸馏推理轨迹做监督微调，再用批级奖励强化学习训练 7B 模型，在 CellPuzzles 基准上超过 OpenAI o1 逾 **73%**，而最佳基线 o1 仅 19.0% 批级准确率 [78]。两者都指向奖励引导学习对领域推理的价值，但前者强调无思考版本更利于跨域，后者依赖蒸馏轨迹质量且仅限 7B 规模，泛化范围有限。

面向科研智能体评估，BioKGBench 从 AI 科学家视角把“理解文献”拆为科学论断验证与知识图谱问答，其 KGCheck 任务用 KGQA 与领域 RAG 识别知识图谱事实错误，发现现有 SOTA 智能体表现失败或较差，BKGAgent 在流行知识图谱上发现超 **90 个事实错误** [79]。BiomniBench 则主张结果导向基准会因记忆、奖励黑客或偶然正确而失真，转而按专家设计的任务专属评分标准对完整轨迹打分，其 BiomniBench-DA 含 100 个数据分析任务、17 种类型、5 个疾病领域，测试显示前沿与开源模型差距仅几分且均有较大提升空间，智能体框架带来的分数差异大于相邻代际模型差距，智能体在方法选择、生物学解释与科学推理上持续不足 [80]。二者都批评仅看最终答案的评估，但 BioKGBench 聚焦知识图谱核查且智能体任务仅 225 条标注，BiomniBench 仅覆盖数据分析、未涵盖完整科研流程，评估范围与粒度存在差异。

围绕「RLVR 是否真正扩展了基座模型的推理能力」这一争议，该工作用**大 k 的 pass@k** 系统探测 RLVR 训练后模型的推理能力边界，覆盖多模型家族、多 RL 算法以及数学、代码、视觉推理基准，并与基座模型和蒸馏做对比 [9]。其核心发现是：**小 k 时 RLVR 模型更优，但大 k 时基座模型的 pass@k 更高**，据此认为 RLVR 带来的推理能力源自并受限于基座模型，而非引出全新的推理模式 [9]。

在算法层面，该研究观察到**六种 RLVR 算法表现相近**，且都远未达到基座

## 2 方法学


### 2.1 科研智能体系统

科研智能体系统的早期形态以提示式协同为主。**ReAct** 让 LLM 交错生成推理轨迹与任务动作，使推理帮助模型归纳、跟踪和更新行动计划，动作则让模型接入 Wikipedia API 或交互环境获取信息，在 HotpotQA、Fever、ALFWorld、WebShop 上仅用 1-2 个上下文示例即优于模仿学习与强化学习基线，其中 ALFWorld 成功率绝对提升 **34%**、WebShop 提升 **10%**，并减少问答与事实验证中的幻觉与错误传播 [1]。该工作依赖提示与外部 API，未做大规模 RL 训练，复杂环境下的动作空间与错误恢复仍受限 [1]。

此后工作转向端到端全自动流水线与多智能体分工。**The AI Scientist** 让 LLM 独立完成构思、编码、实验、可视化、写作与模拟评审的全流程，在扩散模型、Transformer 语言建模、学习动力学三个 ML 子领域验证，每篇论文成本低于 **15 美元**，自动评审接近人类水平，论文可超过顶会接收阈值 [2]。**Co-Scientist** 基于 Gemini 构建生成、反思、排序、进化、邻近性与元评审等专门智能体，在锦标赛框架中生成、辩论并进化假设，针对 AML 药物重定位、肝纤维化靶点、抗菌素耐药机制三个生物医学问题提出的候选均经独立体外实验验证，并独立复现了未发表的新型细菌基因转移机制 [3]。两者都强调科学家在环或自动评审的局限：前者仅在三个 ML 子领域验证且依赖自动评审器、未含真实同行评审 [2]，后者验证限于三个生物医学案例并依赖科学家在环 [3]。

针对静态流水线无法积累经验的问题，一批工作引入记忆与技能学习。**HypoForge** 区分两阶段监督信号：假设生成用对抗式生成器-判别器通过比较批评学习技能，假设测试用执行结果与真值反馈学习测试技能，在不微调基础模型下持续改进，实验表明其在假设质量与测试性能上一致优于现有 AI 科学家框架与技能级变体 [81]。**EvoScientist** 用研究、工程、进化管理三个专门智能体加构思记忆与实验记忆两个持久记忆模块，使智能体检索先前策略以随时间提升想法质量与代码执行成功率，但未报告定量评测 [82]。**The Little Scientist** 则让 Scientist 智能体按科学方法迭代假设、预测、编码、测试与调和，并在平台期由 Kuhn 智能体注入范式转换猜想，在 ProteinGym 零样本排行榜五项指标均列第一、超 VenusREM **+0.033** 平均 Spearman，其 DALE 算法在 132 个 ENCODE 转录因子上平均 AUROC **0.842** 优于 STREME 的 0.803 且快 11 倍，但仅两个案例研究且全程消耗 704M token [4]。

面向具体科学领域的智能体则更强调工具编排与可靠性。**ToolMaker** 将带代码的论文自动转化为 LLM 兼容工具，自动安装依赖、生成代码并用闭环自纠错调试，在含 15 个任务和 100+ 单元测试的基准上正确实现 **80%** 任务，显著优于 SOTA 软件工程智能体，但任务规模有限且依赖公开代码仓库 [5]。**MatClaw** 采用代码优先策略，直接编写和执行 Python 组合任意已安装领域库，在远程 HPC 集群上编排多代码工作流而无需预定义工具函数，其四层记忆架构防止多日工作流的上下文丢失，领域源码 RAG 使每步 API 调用准确率达约 **99%**，但在铁电 CuInP2S6 的三个端到端演示中仍难以处理隐性领域知识，需文献自学习与专家约束干预 [83]。**TeLLAgent** 用监督者-执行者双智能体分离战略推理与工具操作，由 DeepSeek-R1 驱动的全局规划智能体做迭代思维链推理，DeepSeek-V3.1 驱动的局部执行智能体调用 30 个专用工具，并通过基于模型上下文协议的自纠正循环恢复失败，在复杂工具调用任务上显著优于 GPT-5 和现有框架，多步规划成功率更高且随复杂度扩展性更强，同时大幅减少知识检索中的事实幻觉 [84]。与之相对，**Turing Tests For An AI Scientist** 提出七项基准测试评估 AI 智能体能否在不依赖人类生成知识的情况下独立做出突破性发现，如从天体观测推断日心模型，属于评测框架而非系统实现 [85]。安全侧，一篇观点论文从用户意图、科学领域与环境影响三方面分类 AI 科学家风险，主张优先系统防护而非追求更强自主性，提出人类监管、智能体对齐、智能体监管与环境反馈组成的三元防护框架，但为概念分析、无实证验证 [86]。

### 2.2 RLVR 与过程奖励
### 2.3 自我改进与递归自改进
### 2.4 智能体信用分配、验证与安全机制
## 3 数据、基准与评测环境
## 4 生物医学场景应用
## 5 评测、可复现性与争议

在算法层面，该研究观察到**六种 RLVR 算法表现相近**，且都远未达到基座模型的潜力上限；与之相对，蒸馏能够真正扩展推理能力 [9]。作者将上述现象归因于当前训练设置未能引出新的推理模式，能力受基座模型上界约束 [9]。

## 6 空白与趋势

在过程奖励与可验证奖励的交叉地带，**验证信号本身的可靠性尚未被系统建模**：BAVAR 已把验证形式化为资源受限决策并报告了内部对照下的效率提升 [57]，R-Judge 显示最佳模型风险识别仅 74.42% [58]，但两者未回答「验证器在何种错误分布下仍值得信任」。**趋势 1：从固定奖励组件转向自适应验证策略**，依据是 BAVAR 按不确定性、动作关键性、验证器可靠性与剩余预算决定验证什么、何时验证 [57]，以及 VPRM 用确定性规则验证器替代神经评判器以规避不透明与奖励黑客 [19]。**空白 1：验证器可靠性的在线估计与失效检测**，现有工作或假设验证器可靠（BAVAR 的可靠性门控 [57]），或仅在离线基准上报告错误检测率（Socratic-PRMBench 的 2995 条缺陷路径 [59]、MedPRMBench 的 14 类错误 [60]），**没有工作在训练循环内持续估计验证器自身错误率并据此调整奖励权重**。

**趋势 2：过程奖励的信用分配从求和形式向最小形式、树结构与状态自适应混合演化**，依据是 PURE 把价值定义为未来奖励最小值并报告仅用 30% 步数达到可验证奖励方法相当性能 [7]，TEMPO 用前缀树聚合后代结果计算非参数前缀值 [21]，GACA 用每 token 负对数似然逐步骤加权混合两级优势并证明状态自适应混合严格优于固定权重 [24]。**空白 2：跨粒度信用分配的统一定量比较**，TreeRL 报告 GLM4-9B 提升 2.5–5.6、Qwen-2.5-14B 提升 4.6–8.5 [22]，S-trace 报告 Qwen3-1.7B/4B/8B 平均 pass@16 分别提升 0.49%、3.16%、2.98% [23]，但这些数字来自不同基座、基准与预算，**尚无工作在同一实验条件下系统比较最小形式、树搜索、状态自适应与稀疏资格迹四类信用分配的收益边界**。

**趋势 3：自我改进从提示与记忆层向技能库编辑与递归元技能演化，但可靠性问题同步暴露**，依据是 GRASP 在 MedAgentBench 上把 gpt-oss-120b 从 40.6% 升至 88.8% 但增益限于域内 [50]，MetaSkill-Evolve 把进化本身递归化并在三个基准上分别提升 +23.54、+16.09、+1.92 分 [52]，而 Memory Reward Inflation 形式化 Echo Gap 并报告 LUCID 在 BIRD 上达 56.9% [53]，Practice Makes Unsafe 显示 21 个演化配置均产出不安全技能、3 个恶意任务将延续 ASR 从 16.0% 升至 35.3% [54]。**空白 3：自改进系统的「改进方向」可控性**，现有工作或只报告净提升（GRASP、MetaSkill-Evolve），或只报告失效现象（Memory Reward Inflation、Practice Makes Unsafe），**没有工作把「改进什么、不改进什么」作为可指定的约束纳入自改进目标**，也缺少在改进过程中实时检测方向性偏斜的机制。

**趋势 4：科研智能体评测从结果导向转向过程与证据锚定，并集中暴露科学判断瓶颈**，依据是 TruthInsightBench 的四个编码智能体总分仅 58.4–60.3/100 且无可靠区分、瓶颈被定位在科学判断而非编码 [62]，BiomniBench 主张按任务专属评分标准对完整轨迹打分并发现智能体框架带来的分数差异大于相邻代际模型差距 [80]，SoundnessBench 发现 12 个前沿 LLM 在 1099 个提案上普遍乐观偏差 [71]，SciIntegrity-Bench 报告整体诚信问题率 34.2%、缺数据场景全部伪造数据 [72]。**空白 4：面向「科学判断」的可验证奖励构造**，现有 PRM 评测集中在推理步正确性（Socratic-PRMBench、MedPRMBench）或工具调用（Sci-PRM [17]），而 TruthInsightBench 与 BiomniBench 指出的控制、稳健性、可证伪性、跨数据集泛化等维度**尚无对应的过程级奖励信号或可验证规则**，VPRM 在医学偏倚风险评估上的规则化尝试 [19] 是少数例外但领域极窄。

**趋势 5：RLVR 的能力边界与虚假奖励现象被机制性研究持续质疑，但质疑尚未转化为训练方法**，依据是大 k pass@k 探测发现小 k 时 RLVR 模型更优、大 k 时基座模型 pass@k 更高，据此认为 RLVR 推理能力源自并受限于基座 [9]；Spurious Rewards 发现随机奖励可使 Qwen2.5-Math-7B 在 MATH-500 提升 21.4 个百分点、接近真实奖励的 29.1 点 [8]；Spurious Rewards Paradox 定位出隐藏的锚点-适配器回路并可双向因果操控 [34]；样本难度研究显示易与中等难度问题带来最强提升、过难问题诱发退化行为 [37]。**空白 5：把「基座能力边界」与「虚假奖励敏感性」作为训练时的可测量约束**，现有工作或事后诊断（大 k pass@k、路径修补），或提出修正算法但未与边界探测联动（λ-GRPO [20]、PURE [7]），**没有工作在训练过程中实时估计当前策略距基座能力边界的距离并据此决定是否继续 RL、切换奖励形式或停止训练**。

**趋势 6：生物医学领域的可验证奖励稀缺催生自监督与任务重构方案，但验证闭环的独立性存疑**，依据是 CellDuality 用正向预测与反向重构的对偶性以重构保真度为内在奖励形成自验证循环 [50]，Cell-o1 把细胞类型注释重构为批级推理任务并用批级奖励 RL 训练 7B 模型、超 o1 逾 73% [78]，Med-R1 用 GRPO 在八种医学影像模态上平均准确率较 Qwen2-VL-2B 提升 29.94% [77]。**空白 6：自监督奖励与外部可验证信号的一致性检验**，CellDuality 的重构保真度、Cell-o1 的批级奖励、Med-R1 的答案正确性各自构成闭环，但**没有工作检验这些内在奖励与领域专家判断或独立实验验证之间的一致率**，而 CellDuality 与 Memory Reward Inflation 共享的「奖励来源不可靠时自我改进放大偏差」风险 [50][53] 在生物场景下尚未被定量评估。

## 7 未归类新证据

在 RLVR 的过程奖励塑造方向上，Cliff 针对结果奖励对中间推理指导不足的问题，提出用现成 LLM 教师定位每条 rollout 中的首个错误，将轨迹切分为正确前缀与错误后缀并转为 token 级优势，对正确前缀给正优势、其后给负反馈 [10]。其动机来自一个观察：推理过程一旦首次出错，对后续推理的评估提供的信息有限 [10]。方法上它与过程奖励建模、on-policy distillation 形成对照，后两者分别依赖专门奖励模型或假设师生推理模式一致 [10]。

在 **12 个不同场景**的推理任务上，Cliff 一致提升推理性能，**优于 on-policy distillation 15%、优于标准 GRPO 7%**，且即使教师能力一般也有效 [10]。该工作同时指出其局限：依赖教师模型定位首个错误，未讨论教师错误带来的影响 [10]。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 科研智能体系统 | 朝阳 | ReAct [1] 确立「推理-行动」交错范式，The AI Scientist [2] 首次展示端到端自动科研闭环，两者被大量后续工作引用；但 2025–2026 年仍不断出现新架构（LLM Agents Making Agent Tools [5]、EvoScientist [82]），说明系统形态尚未收敛，属近两年爆发但方法未定型的阶段。 |
| 2.2 RLVR 与过程奖励 | 朝阳 | DeepSeekMath [41] 提出 GRPO，DeepSeek-R1 [42] 与 Kimi k1.5 [31] 把 RLVR 推到可复现的大规模验证，并登上 CNS；但同方向仍在快速产出「单条训练样本即可」等新变体 [43]，且出现对 RL 是否真正扩展推理能力的质疑 [9]，方法未收敛。 |
| 2.3 自我改进与递归自改进 | 朝阳 | Reflexion [45] 奠定语言化自我反馈范式，GEPA [46] 进一步显示反思式提示演化可超过 RL，Agentic Context Engineering [48] 与 A Self-Improving Coding Agent [49] 在 2025 年密集出现，说明该方向近两年活跃但路线分歧明显（提示演化 vs 上下文演化 vs 代码自改）。 |
| 2.4 智能体信用分配、验证与安全机制 | 证据不足 | 雷达样本中仅 2 篇：R-Judge [58] 提供安全风险意识基准，Strategic Verification for Long-Running LLM Agents [57] 提出长时程验证策略，但后者为预印本、零引用，尚不足以判断阶段。 |
| 3 数据、基准与评测环境 | 朝阳 | ScienceAgentBench [64]、CORE-Bench [70]、BLADE [66] 在 2024 年集中出现，BixBench [68] 把评测推进到计算生物学，说明基准建设近两年爆发；但各基准任务定义与评分口径差异大，尚未形成公认标准。 |
| 4 生物医学场景应用 | 萌芽 | 雷达样本仅 4 篇且引用偏低：BioKGBench [79] 做生物医学知识图谱核查，BiomniBench [80] 提出真实生物医学研究的过程级评测，Cell-o1 [78] 用 RL 训练单细胞推理，均为探索性工作，尚无大规模验证或共识方法。 |
| 5 评测、可复现性与争议 | 证据不足 | 雷达样本仅 1 篇：Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond… [9] 对 RLVR 的推理增益提出批判性证据，属单点争议性工作，尚不构成独立成熟方向。（引用少于 2 篇证据，不下阶段结论） |

**整体判断**：这个方向整体处于**朝阳期**——RLVR/GRPO 这条训练范式线已有 CNS 级大规模验证（[42]、[31]），科研智能体系统线已有端到端闭环原型（[2]），但两者尚未真正合流：**「可验证奖励」目前主要验证数学/代码答案，而科研的验证信号（实验是否可复现、假设是否有价值）还没有可靠代理**。雷达样本中 2.2 节 n=40、近两年占比 0.95，而 4 节生物医学应用仅 n=4，说明**方法侧拥挤、场景侧稀薄**。窗口期估计 **12–18 个月**：一旦通用 RLVR 工具链（如 GRPO 开源实现）被封装成标准库，纯方法改进的边际收益会迅速下降，而「领域可验证奖励设计」仍会长期稀缺。最大不确定性是 [9] 提出的质疑——如果 RL 主要是在重加权已有能力而非扩展能力边界，那么以 RLVR 为核心的科研智能体训练路线可能被更轻量的上下文/提示演化方法（[46]、[48]）部分替代。

**接下来怎么做**：

1. **把「单细胞/多组学分析流程」做成可验证奖励环境**。切入点：用公共数据（如 CELLxGENE、Human Cell Atlas）构造带标准答案的分析任务（细胞类型注释、差异表达、轨迹推断），把每一步中间产物（聚类数、marker 基因、通路富集）转成可自动判定的奖励信号，用 GRPO 训练一个组学分析智能体。为什么现在做：Cell-o1 [78] 已证明单细胞推理可用 RL 训练，但只覆盖「谜题式」任务；BixBench [68] 提供了计算生物学评测骨架，两者之间正好缺「过程级可验证奖励」这一层。产出：一个可复现的单细胞分析 RLVR 环境 + 基线模型。

2. **做过程奖励模型（PRM）而非只做结果奖励**。切入点：把生信分析拆成「读数据→QC→归一化→降维→注释→富集」的步骤链，人工或半自动标注每步正确性，训练 PRM 给中间步骤打分，再与 GRPO 结合。为什么现在做：2.2 节证据几乎全是结果奖励（[41]、[43]），而科研任务的失败往往发生在中间步骤；BiomniBench [80] 明确提出过程级评测，说明需求已被识别但方法供给不足。产出：领域 PRM + 在 BixBench/BiomniBench 上的过程级评测结果。

3. **把类器官多组学数据作为「真实科研闭环」的验证床**。切入点：用你手上的类器官 + 多组学数据，构造「假设生成→实验设计→数据分析」的智能体任务，奖励信号来自数据本身的可复现性（同一 pipeline 重跑一致性、跨批次稳健性）。为什么现在做：The AI Scientist [2] 的闭环在真实湿实验数据上缺乏验证，而 4 节生物医学应用全是基准或知识图谱核查（[79]），没有真实多组学闭环；这是你能提供而 ML 组提供不了的独特资产。产出：一个真实数据驱动的科研智能体案例研究 + 可复现评测协议。

4. **在自我改进线上选「上下文演化」而非「权重更新」作为轻量切入**。切入点：用 Agentic Context Engineering [48] 或 GEPA [46] 的思路，让智能体在多次生信分析任务中自动积累「领域经验上下文」（如某类数据的 QC 陷阱、某物种的注释惯例），不训练模型权重。为什么现在做：GEPA 已显示反思式提示演化可超过 RL，且计算成本远低于 GRPO；对博后而言这是**低 GPU 门槛、高领域壁垒**的切入点，且与 [9] 的质疑方向一致。产出：一个领域上下文库 + 在 BixBench 类任务上的增益对比。

5. **主动做批判性评测，而不是只做系统**。切入点：复现 [9] 的质疑实验，但换成生物医学分析任务，检验「RLVR 训练后的生信智能体是真的学会了新分析能力，还是只是重加权了预训练中已有的生信知识」。为什么现在做：5 节雷达样本仅 1 篇且引用过千，说明这类批判性工作影响力大但供给极少；CORE-Bench [70] 已提供「复现已发表研究」的评测框架，可直接复用。产出：一篇有争议性的评测论文，同时为你的系统工作提供可信度背书。

## 参考文献

1. ReAct: Synergizing Reasoning and Acting in Language Models. International Conference on Learning Representations 2022. https://arxiv.org/abs/2210.03629
2. The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery. arXiv.org 2024. https://arxiv.org/abs/2408.06292
3. Accelerating scientific discovery with Co-Scientist.. Nature 2026. https://doi.org/10.1038/s41586-026-10644-y
4. The Little Scientist: LLM Agent-Driven Discovery via the Scientific Method.  2026. https://arxiv.org/abs/2608.16951
5. LLM Agents Making Agent Tools. Annual Meeting of the Association for Computational Linguistics 2025. https://doi.org/10.48550/arXiv.2502.11705
6. ScalePRM: Training Process Reward Models by Scaling Verification Compute Without Ground Truth.  2025. https://arxiv.org/abs/2512.03244v2
7. Stop Summation: Min-Form Credit Assignment Is All Process Reward Model Needs for Reasoning.  2025. https://arxiv.org/abs/2504.15275v3
8. Spurious Rewards: Rethinking Training Signals in RLVR. arXiv.org 2025. https://doi.org/10.48550/arXiv.2506.10947
9. Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model?. Neural Information Processing Systems 2025. https://doi.org/10.48550/arXiv.2504.13837
10. Cliff: Learning Process Rewards from the First Mistake.  2026. https://arxiv.org/abs/2609.02817
11. A Survey of Process Reward Models: From Outcome Signals to Process Supervisions for Large Language Models.  2025. https://arxiv.org/abs/2510.08049v3
12. Process Reward Models for LLM Agents: Practical Framework and Directions.  2025. https://arxiv.org/abs/2502.10325v1
13. AgentPRM: Process Reward Models for LLM Agents via Step-Wise Promise and Progress.  2025. https://arxiv.org/abs/2511.08325v1
14. Process Reward Model with Q-Value Rankings.  2024. https://arxiv.org/abs/2410.11287v2
15. The Bidirectional Process Reward Model.  2025. https://arxiv.org/abs/2508.01682v3
16. MASPRM: Multi-Agent System Process Reward Model.  2025. https://arxiv.org/abs/2510.24803v3
17. SCI-PRM: A Tool Aware Process Reward Model for Scientific Reasoning Verification.  2026. https://arxiv.org/abs/2606.04579v2
18. Stop Rewarding Hallucinated Steps: Faithfulness-Aware Step-Level Reinforcement Learning for Small Reasoning Models.  2026. https://arxiv.org/abs/2602.05897v2
19. Beyond Outcome Verification: Verifiable Process Reward Models for Structured Reasoning.  2026. https://arxiv.org/abs/2601.17223v1
20. GRPO is Secretly a Process Reward Model.  2025. https://arxiv.org/abs/2509.21154v4
21. Exploiting Tree Structure for Credit Assignment in Reinforcement Learning with Large Language Models.. Findings of ACL. ACL 2026. https://doi.org/10.18653/v1/2026.findings-acl.524
22. TreeRL: LLM Reinforcement Learning with On-Policy Tree Search.  2025. https://arxiv.org/abs/2506.11902v1
23. Beyond Uniform Credit Assignment: Selective Eligibility Traces for RLVR. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.05965
24. Granularity-Adaptive Credit Assignment for Long-Horizon LLM Agent Reinforcement Learning.  2026. https://arxiv.org/abs/2609.12424
25. Group-Graph Policy Optimization for Long-Horizon Agentic Reinforcement Learning. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.22995
26. GEAR: Granularity-Adaptive Advantage Reweighting for LLM Agents via Self-Distillation. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.11853
27. Stabilizing Off-Policy Training for Long-Horizon LLM Agent via Turn-Level Importance Sampling and Clipping-Triggered Normalization.  2025. https://arxiv.org/abs/2511.20718
28. Neglected Free Lunch from Post-training: Progress Advantage for LLM Agents. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.26080
29. SELAUR: Self Evolving LLM Agent via Uncertainty-aware Rewards. Pacific-Asia Conference on Knowledge Discovery and Data Mining 2026. https://doi.org/10.48550/arXiv.2602.21158
30. Internalizing Meta-Experience into Memory for Guided Reinforcement Learning in Large Language Models. arXiv.org 2026. https://doi.org/10.48550/arXiv.2602.10224
31. Kimi k1.5: Scaling Reinforcement Learning with LLMs. arXiv.org 2025. https://doi.org/10.48550/arXiv.2501.12599
32. SWE-TRACE: Optimizing Long-Horizon SWE Agents Through Rubric Process Reward Models and Heuristic Test-Time Scaling.  2026. https://arxiv.org/abs/2604.14820v1
33. GenReasoner: Generative Visual Agent Planning.  2026. https://doi.org/10.21203/rs.3.rs-9035628/v1
34. Spurious Rewards Paradox: Mechanistically Understanding How RLVR Activates Memorization Shortcuts in LLMs. arXiv.org 2026. https://doi.org/10.48550/arXiv.2601.11061
35. Exploration vs Exploitation: Rethinking RLVR through Clipping, Entropy, and Spurious Reward. arXiv.org 2025. https://doi.org/10.48550/arXiv.2512.16912
36. Reasoning or Memorization? Unreliable Results of Reinforcement Learning Due to Data Contamination. AAAI Conference on Artificial Intelligence 2025. https://doi.org/10.48550/arXiv.2507.10532
37. Mechanistically Interpreting the Role of Sample Difficulty in RLVR for LLMs. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.28388
38. Reinforced Efficient Reasoning via Semantically Diverse Exploration. Annual Meeting of the Association for Computational Linguistics 2026. https://doi.org/10.48550/arXiv.2601.05053
39. Entropy Regularization in Deep Reinforcement Learning: A Structured Review Across Classical Control, Generative Policies, and Reasoning Language Models.. Entropy (Basel, Switzerland) 2026. https://doi.org/10.3390/e28070811
40. Reward Modeling for Reinforcement Learning-Based LLM Reasoning: Design, Challenges, and Evaluation. Trans. Mach. Learn. Res. 2026. https://doi.org/10.48550/arXiv.2602.09305
41. DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models. arXiv.org 2024. https://doi.org/10.48550/arXiv.2402.03300
42. DeepSeek-R1 incentivizes reasoning in LLMs through reinforcement learning.. Nature 2025. https://doi.org/10.1038/s41586-025-09422-z
43. Reinforcement Learning for Reasoning in Large Language Models with One Training Example. Neural Information Processing Systems 2025. https://doi.org/10.48550/arXiv.2504.20571
44. Learning to Reason without External Rewards. arXiv.org 2025. https://doi.org/10.48550/arXiv.2505.19590
45. Reflexion: language agents with verbal reinforcement learning. Neural Information Processing Systems 2023. https://doi.org/10.52202/075280-0377
46. GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning. arXiv.org 2025. https://arxiv.org/abs/2507.19457
47. Experiential Reflective Learning for Self-Improving LLM Agents. arXiv.org 2026. https://doi.org/10.48550/arXiv.2603.24639
48. Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models. arXiv.org 2025. https://doi.org/10.48550/arXiv.2510.04618
49. A Self-Improving Coding Agent. arXiv.org 2025. https://doi.org/10.48550/arXiv.2504.15228
50. GRASP: Gated Regression-Aware Skill Proposer for Self-Improving LLM Agents. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.29668
51. AccelOpt: A Self-Improving LLM Agentic System for AI Accelerator Kernel Optimization. arXiv.org 2025. https://doi.org/10.48550/arXiv.2511.15915
52. MetaSkill-Evolve: Recursive Self-Improvement of LLM Agents via Two-Timescale Meta-Skill Evolution. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.05297
53. Memory Reward Inflation in Self-Improving LLM Agents.  2026. https://arxiv.org/abs/2608.00017
54. Practice Makes Unsafe: Skill Misevolution in Self-Improving LLM Agents.  2026. https://arxiv.org/abs/2608.12851
55. AI4AI-Bench: Benchmarking LLM Agents in Algorithmic Design for Recursive Self-Improvement.  2026. https://arxiv.org/abs/2608.20318
56. RSIBench-Data: Benchmarking Data-Centric Research for Recursive Self-Improvement. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.25886
57. Strategic Verification for Long-Running LLM Agents.  2026. https://doi.org/10.20944/preprints202608.2057.v1
58. R-Judge: Benchmarking Safety Risk Awareness for LLM Agents. Conference on Empirical Methods in Natural Language Processing 2024. https://doi.org/10.48550/arXiv.2401.10019
59. Socratic-PRMBench: Benchmarking Process Reward Models with Systematic Reasoning Patterns.  2025. https://arxiv.org/abs/2505.23474v1
60. MedPRMBench: A Fine-grained Benchmark for Process Reward Models in Medical Reasoning.  2026. https://arxiv.org/abs/2604.17282v1
61. MemCalib: Benchmarking and Optimizing Memory Use in LLM Agents.  2026. https://arxiv.org/abs/2609.24259
62. TruthInsightBench: An Evidence-Grounded Benchmark for Automated Evaluation of Open-Ended Scientific Discovery Agents.  2026. https://arxiv.org/abs/2609.05079
63. Benchmarking AI scientists for omics data-driven biological discovery.. Bioinformatics (Oxford, England) 2026. https://doi.org/10.1093/bioinformatics/btag227
64. ScienceAgentBench: Toward Rigorous Assessment of Language Agents for Data-Driven Scientific Discovery. arXiv.org 2024. https://doi.org/10.48550/arXiv.2410.05080
65. LMR-BENCH: Evaluating LLM Agent's Ability on Reproducing Language Modeling Research. Conference on Empirical Methods in Natural Language Processing 2025. https://doi.org/10.48550/arXiv.2506.17335
66. BLADE: Benchmarking Language Model Agents for Data-Driven Science. Conference on Empirical Methods in Natural Language Processing 2024. https://doi.org/10.48550/arXiv.2408.09667
67. GenoTEX: An LLM Agent Benchmark for Automated Gene Expression Data Analysis.  2024. https://arxiv.org/abs/2406.15341
68. BixBench: a Comprehensive Benchmark for LLM-based Agents in Computational Biology. arXiv.org 2025. https://doi.org/10.48550/arXiv.2503.00096
69. Benchmarking LLM Agents on Real-World Biological Database Curation for Data-Driven Scientific Discovery. Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.2 2026. https://doi.org/10.1145/3770855.3817556
70. CORE-Bench: Fostering the Credibility of Published Research Through a Computational Reproducibility Agent Benchmark. Trans. Mach. Learn. Res. 2024. https://doi.org/10.48550/arXiv.2409.11363
71. SoundnessBench: Can Your AI Scientist Really Tell Good Research Ideas from Bad Ones?. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.30329
72. SciIntegrity-Bench: A Benchmark for Evaluating Academic Integrity in AI Scientist Systems. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.10246
73. The More You Automate, the Less You See: Hidden Pitfalls of AI Scientist Systems. arXiv.org 2025. https://doi.org/10.48550/arXiv.2509.08713
74. SEAGym: An Evaluation Environment for Self-Evolving LLM Agents. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.17546
75. StreamBench: Towards Benchmarking Continuous Improvement of Language Agents. Neural Information Processing Systems 2024. https://doi.org/10.48550/arXiv.2406.08747
76. ABC-Bench: An Agentic Bio-Capabilities Benchmark for Biosecurity. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.11150
77. Med-R1: Reinforcement Learning for Generalizable Medical Reasoning in Vision-Language Models.. IEEE transactions on medical imaging 2026. https://doi.org/10.1109/tmi.2026.3661001
78. Cell-o1 : training LLMs to solve single-cell reasoning puzzles with reinforcement learning.. Bioinformatics (Oxford, England) 2026. https://doi.org/10.1093/bioinformatics/btag208
79. BioKGBench: A Knowledge Graph Checking Benchmark of AI Agent for Biomedical Science. arXiv.org 2024. https://doi.org/10.48550/arXiv.2407.00466
80. BiomniBench: Process-level Evaluation of LLM Agents for Real-world Biomedical Research. bioRxiv 2026. https://doi.org/10.64898/2026.05.12.724604
81. HypoForge: A Self-Improving Multi-Agent Framework for Automated Hypothesis Generation and Testing via Scientific Skill Learning.  2026. https://arxiv.org/abs/2608.25770
82. EvoScientist: Towards Multi-Agent Evolving AI Scientists for End-to-End Scientific Discovery. arXiv.org 2026. https://doi.org/10.48550/arXiv.2603.08127
83. MatClaw: An Autonomous Code-First LLM Agent for End-to-End Materials Exploration. arXiv.org 2026. https://doi.org/10.48550/arXiv.2604.02688
84. TeLLAgent: a dual-agent framework for reliable scientific discovery with tool-enhanced LLMs. Chemical Science 2026. https://doi.org/10.1039/d5sc09883a
85. "Turing Tests" For An AI Scientist. arXiv.org 2024. https://doi.org/10.48550/arXiv.2405.13352
86. Risks of AI scientists: prioritizing safeguarding over autonomy.. Nature communications 2025. https://doi.org/10.1038/s41467-025-63913-1
87. CellDuality: Unlocking Biological Reasoning in LLMs with Self-Supervised RLVR.. ... International Conference on Learning Representations 2026. https://europepmc.org/article/MED/42559559
88. MedVLM-R1: Incentivizing Medical Reasoning Capability of Vision-Language Models (VLMs) via Reinforcement Learning. International Conference on Medical Image Computing and Computer-Assisted Intervention 2025. https://doi.org/10.48550/arXiv.2502.19634
89. MedLoc-R1: Performance-Aware Curriculum Reward Scheduling for GRPO-Based Medical Visual Grounding. arXiv.org 2026. https://doi.org/10.48550/arXiv.2603.28120
90. Reinforcement Learning without Ground-Truth Solutions can Improve LLMs. arXiv.org 2026. https://doi.org/10.48550/arXiv.2606.27369
91. DiscoverPhysics: Benchmarking LLMs for Out-of-the-Box Scientific Thinking. arXiv.org 2026. https://doi.org/10.48550/arXiv.2605.26087
