# 虚拟细胞与扰动响应预测 · 方向背景报告

证据 50 篇 · 覆盖度 0.56 · 第 11 轮 · 更新 2026-11-22

## 本次变更

- 新增 [34] Joint single-cell capture of Cas9 edits and transcriptomes reveals on- and off-target effects on gene expression.

## 摘要（TL;DR）

- 扰动响应生成模型最早以潜空间向量算术为范式，scGen 用变分自编码器在潜空间学习扰动向量，通过加减该向量实现跨细胞类型与跨物种的响应预测[1]。
- scGPT 将扰动响应预测作为生成式预训练 Transformer 的下游任务之一，在超3300万个细胞上预训练后经迁移学习适配，报告在扰动响应预测等任务上表现优异[2]。
- Tahoe-x1 的扰动训练单细胞基础模型参数最高达30亿，报告计算效率比先前细胞状态模型实现高3–30倍，并在四个基准上均达最先进性能[3]。
- scKITE 的数据缩放分析显示，加入细胞级文本注释与基因级调控信息比单纯扩大数据量提供额外缩放维度，仅用179,067个预训练样本（不足先前强模型0.5%）即在多下游任务超越 Geneformer、scGPT、scFoundation 等，知识增强训练带来平均28.8%相对提升[4]。
- OCOO-T 用极简流匹配 Transformer 直接作用于连续基因表达谱，将扰动响应预测建模为连续时间去噪过程，在 Tahoe100M、Replogle、PBMC 上达到最先进性能并可扩展至长转录谱[5]。
- X-Cell 配套构建了 X-Atlas/Pisces，含2560万扰动单细胞、16种生物学情境，报告在 Pearson Δ 等指标上优于现有最先进模型最高达五倍并展示零样本预测能力[6]。
- SCALE 提出条件传输模型，将细胞表示为无序集合并预测处理群体而无需细胞级配对，在 CRISPR 数据7项指标上优于竞争方法，其预测的细胞因子差异经3名供体 PBMC 实验验证[7]。
- D²R² 将扰动预测重构为调控引导的基因级渐进生成，在 Norman19 五项指标最优、VCC-H1 具竞争力，消融显示生物先验排序优于随机与不确定性启发式[8]。
- 知识图谱路线发现最简 KNN 模型在分布外扰动预测上击败几乎所有方法，再用强化学习优化的推理 LLM 调整邻域，在 Replogle 2022 细胞系上达到当前 SOTA 水平[9]。
- 一项比较五种基础模型与两种深度学习模型的研究报告没有任何模型优于简单线性基线，所用数据含 1,000 个读出基因、62 个双扰动，并识别出 5,035 个遗传互作（潜在 124,000）[10]。
- 有研究提出阳性对照基线与指标校准框架，在14个数据集、18个指标上发现 MSE 和 Pearson Δ 等常用指标常校准不良，在良好校准指标下深度学习扰动模型可优于无信息基线[11]。
- 用2220万细胞语料预训练400个模型并开展6,400次实验后，性能在数据规模远小于现有语料时即达平台期，未发现类似大语言模型的数据缩放定律[12]。
- 在更宏观的框架层面，有工作提出将虚拟细胞构建为多模态、多尺度、有状态的动态计算系统，但该文属愿景性论文，未报告定量结果，也无实验验证[13]。
- 现有资源多集中于癌细胞系或单一原代细胞类型，蛋白质组时序数据与转录组图谱之间尚缺统一基准，不同研究各自选用的基准与评估协议也使跨工作比较存在争议[14]。

## 1 背景与定义

扰动响应预测的方向边界，首先由“预测什么”与“凭什么预测”两个问题划定。早期工作把扰动响应视为潜空间中的向量平移，scGen 用变分自编码器学习扰动向量并支持跨细胞类型、跨物种的响应预测[1]；这一范式的前提是扰动效应可从观察性表达图谱中被低维编码。后续批判性工作则指出该前提在分布外条件下不成立：仅依赖观察性图谱难以外推到训练分布之外[6]，而单细胞 CRISPR 筛选的统计关联也不能直接读作因果效应，需附加超出标准统计分析的因果假设，且方法仅能识别一个基因敲低对另一基因的效应[15]。因此本方向的边界并非“任何单细胞预测任务”，而是**以干预（遗传、药物、环境）为条件、以细胞状态分布为输出、并须经受分布外与因果效度检验的预测**；常规单细胞分析流程、无代码无权重的方法论文与纯融资新闻均不构成该方向的实质进展。

演化脉络可沿三条线索理解。其一是**生成机制**：从潜空间向量算术，到扩散与流匹配直接作用于连续表达谱（OCOO-T 将扰动响应建模为连续时间去噪过程，整合扰动、剂量与细胞系信息[5]），再到离散扩散与调控引导的基因级渐进生成（D²R² 用掩码离散扩散逐步重建表达谱，调控策略模块由对照细胞 GRN 初始化并经组相对策略优化微调排序[8]），以及面向非配对群体的条件传输（SCALE 将细胞表示为无序集合、无需细胞级配对，使端点监督直接 delta 对齐[7]）。其二是**约束来源**：从纯数据驱动，转向引入基因调控网络与因果结构（D-SPIN 从跨数千扰动条件推断机制可解释且可生成的调控网络模型[16]；RegVelo 联合建模剪接动力学与调控互作[17]；CauTrigger 将 do-calculus 整合进分层深度潜变量模型[18]），再到以强化学习后训练施加生物约束（CellFluxRL 设计三类共七个奖励[19]）。其三是**系统定位**：从单任务预测器，走向有状态的细胞世界模型与闭环智能体（Chreode 以结构化残差转移算子做一步式状态转移预测[20]；CellScientist 把执行偏差路由回假设或实现层面形成闭环[21]；以及将虚拟细胞定义为多模态、多尺度、有状态动态系统并以世界模型为操作框架的愿景性论述[13]）。

核心问题可归纳为四组张力。**第一，规模与知识之争**：一端以参数与语料扩张取胜，另一端主张知识监督提供额外缩放维度——scKITE 仅用 179,067 个预训练样本（不足先前强模型 0.5%）即在多下游任务超越 Geneformer、scGPT 等，知识增强训练带来平均 28.8% 相对提升[4]；而用 2220 万细胞预训练 400 个模型、开展 6,400 次实验的研究发现性能在数据规模远小于现有语料时即达平台期，未发现清晰的数据缩放定律[12]。**第二，复杂架构与简单基线的之争**：知识图谱路线发现最简 KNN 模型在分布外扰动预测上击败几乎所有方法，再用强化学习优化的推理 LLM 调整邻域达到当前 SOTA[9]；多项独立评测报告深度学习模型未跑赢简单基线，如五种基础模型与两种深度学习模型均未优于线性基线[10]，Perturb-seq 基准上 Train Mean 即优于 scGPT 与 scFoundation[22]，Systema 在十个数据集上发现简单 perturbed mean 跨所有数据集优于其他方法[23]。**第三，评测效度之争**：细胞级随机划分会泄漏组内答案，同克隆或同患者细胞共享标签，患者队列中泄漏足以推翻临床结论[24]；常用 MSE 与 Pearson Δ 等指标常校准不良，在良好校准指标下深度学习模型可优于无信息基线[11]；VCBench 报告基线在五个评分维度中的四个匹配或超过所有基础模型，且无基础模型发布完整细胞级训练清单[25]。**第四，任务定义之争**：scArchon 明确仅限非遗传扰动、基因敲除作为独立问题未纳入[26]，AssayBench 则把表型筛选重构为基因排序任务并发现零样本通用 LLM 优于生物学专用 LLM[27]，说明“扰动预测”并非单一任务，模型排名随任务形式与指标而变[28]。

数据资源构成该方向的物质基础，也决定了评估上限。Tahoe-100M 以 Mosaic 平台把遗传上不同的细胞模型多重化为平衡的“细胞村”，含 1 亿转录组、50 个癌细胞系、1100 种药物-剂量条件[29]；基因组规模 Perturb-seq 覆盖超过 250 万人类细胞[30]；原代 CD4+T 细胞工作在 4 名供体、2200 万细胞上测量静息与刺激后效应[31]；X-Atlas/Pisces 含 2560 万扰动单细胞、16 种生物学情境[6]；ProteinTalks 基于超过 3800 万条时序蛋白丰度测量[14]。读出维度亦从转录组扩展到空间与体内：SPAC-seq 将 CRISPR 筛选与空间表型关联[32]，iGOF-Perturb-seq 在星形胶质细胞中构建约 1000 个转录因子的功能图谱[33]。**这些资源在细胞来源、扰动方式与读出层面差异显著，跨资源比较缺乏统一基准**；Superb-seq 同时捕获编辑结果与转录组、检出 5761 个编辑细胞及 36 个脱靶位点，提示生成模型的评估上限受制于扰动标签与脱靶效应的测量精度[34]。

评测基准与效度批判已从“排行榜”演化为独立研究方向。Virtual Cell Challenge 提供评估框架、专用数据集与竞赛平台，作为反复举办的开放基准[35]，其 2026 届进一步推进到跨独立细胞情境的零样本设定，在含未见细胞系的 Arc 新数据集上预测基因敲低响应[36]。与此同时，批判性证据指向基准设置本身：EL-PERTURB 采用分层分布外划分，在必需基因与全基因组 Perturb-seq 数据上压力测试 6 类架构的 20 个模型，结论是现有基准多依赖随机划分而掩盖系统性失效模式[37]；Systema 把高分归因于“系统性变异”而非扰动特异性效应[23]；跨任务大规模比较显示扰动效应幅度强烈影响泛化与双扰动预测，细胞类型迁移中源-目标转录组距离越大准确率越低，且实验系统多限于细胞系[38]；药物响应方向则显示单药模型通常可做癌症盲预测，但药物盲性能显著下降甚至失败，泛化主要限于同类内[39]。**因此本方向当前的核心问题不是“能否拟合扰动数据”，而是“在何种划分、何种指标、何种干预信息质量下，预测才具备可迁移的生物学效度”**；这一问题的答案尚不统一，构成该子领域最主要的方法论争议。

## 2 方法学


### 2.1 扰动响应生成模型

扰动响应生成模型最早以潜空间向量算术为范式：scGen 用变分自编码器在潜空间学习扰动向量，通过加减该向量实现跨细胞类型与跨物种的响应预测[1]。这一思路奠定了"对照—扰动"映射的基本框架，但后续工作普遍指出，仅依赖观察性表达图谱难以外推到训练分布之外[6]。与之相对，**scGPT** 将扰动响应预测作为生成式预训练 Transformer 的下游任务之一，在**超3300万个细胞**上预训练后经迁移学习适配，报告在扰动响应预测等任务上表现优异[2]。基础模型路线由此分化：一端是继续扩大预训练规模，另一端则质疑单纯扩数据的收益。

规模扩张的代表是 **Tahoe-x1**，其扰动训练的单细胞基础模型参数最高达**30亿**，预训练语料包括 Tahoe-100M，报告计算效率比先前细胞状态模型实现高**3–30倍**，并在基因必需性、癌症标志基因、细胞类型分类与留出环境扰动响应预测四个基准上均达最先进性能[3]。跨物种方向则有 **Speciesformer**，在含**1.31亿细胞**的 SpeciesCorpus 上预训练，目标是学习可迁移的细胞状态与状态转变，并区分保守原理与物种/组织特异变异[40]。但知识增强路线给出了相反的证据：scKITE 的数据缩放分析显示，加入细胞级文本注释与基因级调控信息比单纯扩大数据量提供额外缩放维度，仅用**179,067个预训练样本（不足先前强模型0.5%）**即在多下游任务超越 Geneformer、scGPT、scFoundation 等，知识增强训练带来平均**28.8%**相对提升[4]。这与大规模预训练路线的取舍构成直接张力：前者以参数与数据量取胜，后者主张知识监督可替代数据规模。

在生成机制上，扩散与流匹配成为主流。**OCOO-T** 用极简流匹配 Transformer 直接作用于连续基因表达谱，将扰动响应预测建模为连续时间去噪过程，通过自适应层归一化和上下文 token 整合扰动、剂量与细胞系信息，在 Tahoe100M、Replogle、PBMC 上达到最先进性能并可扩展至长转录谱[5]。**State** 则强调细胞异质性，其细胞嵌入训练于**1.67亿细胞**，报告在大型数据集上效应区分度提升**超过30%**，差异表达基因识别准确率显著优于基线，且嵌入可识别训练中未观察扰动的细胞环境[41]。**X-Cell** 配套构建了 X-Atlas/Pisces，含**2560万扰动单细胞、16种生物学情境**，用扩散语言模型经交叉注意力整合自然语言、蛋白质语言模型与互作网络等多模态先验，报告在 Pearson Δ 等指标上优于现有最先进模型**最高达五倍**并展示零样本预测能力[6]。这些工作报告的提升幅度建立在各自基准与对照之上，不宜跨研究直接比较高低。

针对"对照与处理细胞为非配对群体"这一数据特性，**SCALE** 提出条件传输模型，将细胞表示为无序集合并预测处理群体而无需细胞级配对，共享集合感知编码器与条件 DiT 骨干使端点监督直接 delta 对齐；在 CRISPR 数据**7项指标**上优于竞争方法并保持基因靶表示分离，其预测的细胞因子差异经**3名供体** PBMC 实验验证[7]。**scBalFlow** 则聚焦药物扰动数据的类别严重不平衡，采用两阶段解耦训练：第一阶段预测响应强度并用高斯增强推断缓解不平衡，第二阶段跳过弱响应条件、用 Flow Matching 合成高响应样本，在 SciPlex3 与 McFarland 等基准上显著优于现有 SOTA，尤其在不平衡数据集上[42]。两者都承认端到端映射的偏差来源，但归因不同——前者归因于配对缺失，后者归因于类别不平衡。

另一条路线把生成顺序本身作为建模对象。**D²R²** 将扰动预测重构为调控引导的基因级渐进生成，用掩码离散扩散以序数 token 逐步重建表达谱，调控策略模块由对照细胞 GRN 初始化并经组相对策略优化微调排序；在 Norman19 **五项指标**最优、VCC-H1 具竞争力，消融显示生物先验排序优于随机与不确定性启发式[8]。与之呼应，知识图谱路线发现最简 KNN 模型在分布外扰动预测上击败几乎所有方法，再用强化学习优化的推理 LLM 调整邻域，在 Replogle 2022 细胞系上达到当前 SOTA 水平[9]。这两项结果共同对"复杂生成架构必要"提出质疑：简单先验加排序/检索即可获得强竞争力，而 OCOO-T 亦自承基于扩散/流匹配的方法学习对照到扰动分布仍具挑战[5]。

调控网络与因果结构被引入生成过程以提升可解释性。**D-SPIN** 从跨数千扰动条件的单细胞 mRNA-seq 推断机制可解释且可生成的基因调控网络模型，通过重构调控相互作用解释扰动如何改变细胞状态比例，识别细胞命运关键调控因子、解析药物组合的加性基因程序招募，并模拟未观测剂量组合下的免疫细胞群结构变化[16]。**RegVelo** 联合建模剪接动力学与基因调控互作，在斑马鱼神经嵴发育数据上结合计算机扰动、CRISPR-Cas9 敲除与单细胞 Perturb-seq 验证，确立 tfec 为早期驱动因子、elf1 为色素细胞命运调控因子[17]。**DynaVelo** 以生成式神经常微分方程学习基因表达与 TF motif 活性的联合动态，重现野生型小鼠生发中心 B 细胞体内分叉动态，揭示 Arid1a 和 Ctcf 杂合缺失下的动态变化，并预测突变体中受破坏的 TF-基因边[43]。**CauTrigger** 则将 do-calculus 整合进分层深度潜变量模型，分离因果与虚假潜因子、递归重建调控层级，在合成与真实多层调控数据集上优于现有方法[18]。这些工作共享"生成须受调控结构约束"的立场，但约束来源不同：D-SPIN 与 RegVelo 依赖数据推断的网络，CauTrigger 依赖因果分解假设。

时间维度上的扰动预测由 **PerturbGen** 推进，其生成式基础模型训练于**超1亿单细胞转录组**，预测源状态遗传扰动如何塑造下游状态、改变基因程序与轨迹；在免疫挑战、造血与皮肤发育三套数据中，预测 IL1B 敲除减弱后续细胞因子-干扰素程序，与 IL-1β 刺激逆转一致[44]。药物方向上，**scDEFT** 将药物视为细胞表征的条件算子，用特征级线性调制生成药物条件化潜变量并由两个独立头聚合预测，在**116万细胞** IBD 图谱（3队列2类药物、51供体）上状态变化预测达 headroom 的**45%**，治疗前应答分层 AUROC **0.70**，而标准预测器仅达随机水平[45]。**UniPert-G2CP** 则以两阶段框架统一多模态分子扰动表征，实现遗传到化学的表型迁移学习，在大规模遗传与化学筛选数据上验证并揭示耐药机制[46]。**TFActProfiler** 走的是资源+框架路线，整合 ChIP、motif 与 curated 先验及大规模 RNA-seq 学习带符号定量 TF-mRNA 系数，在多细胞类型 TF 敲低基准上优于现有 TF 活性推断方法，且无需额外训练即可预测 TF 扰动转录组响应[47]。

图像型虚拟细胞暴露了另一类问题：生成结果可能违反基本物理与生物约束。**CellFluxRL** 用强化学习后训练 CellFlux，设计生物功能、结构有效性与形态正确性三类共**七个奖励**，通过采样—优化交替提升高奖励样本似然，在所有奖励上持续优于基线，测试时扩展进一步提升性能[19]。**PerturbBridge** 则指出仅匹配真实图像分布不足以优化扰动特异性生物响应，提出随机数据到数据桥模型，在训练中对预测扰动图像直接施加表型监督；在 BBBC021 上 MoA 准确率**77.8%（CellProfiler）/74.9%（DINOv2）**，较 CellFlux 提升**5.7/7.5个百分点**，JUMP Hit@10 **12.15%**、中位秩**74**，AllenCell Hit@1 **69.29%**[48]。两者都把生物约束放在训练后或训练中的监督环节，而非架构本身。

数据侧的配套进展同样影响生成模型的可信度。**Superb-seq** 整合 Cas9 编辑检测、T7 原位转录与单细胞 RNA 测序，在**3个细胞系3.5万个细胞**上同时捕获编辑结果与转录组；在**1万个 K562细胞**中用**7条 gRNA** 靶向4个染色质重塑基因，检出**5761个编辑细胞**、全部在靶位点及**36个脱靶位点**，较 Perturb-seq 更准确估计下游表达扰动效应[34]。这提示生成模型的评估上限受制于扰动标签与脱靶效应的测量精度，而现有工作报告的性能差异部分可能源于训练与评测数据的干预信息质量不同。

### 2.2 细胞世界模型与闭环智能体

在细胞世界模型的建模路线上，Chreode 将自身定位为**一步式细胞世界模型**，通过结构化残差转移算子预测动作条件下的细胞状态转移，把分布演化从推理时移至训练时以实现单次生成，并保留 Waddington 式分解 [20]。其在 **240万细胞小鼠胚胎图谱、7个数据集**上预训练，在 GEARS 扰动预测上使 **DE20 MSE 从 0.2121 降至 0.1858（相对提升12.4%）**，并在 Weinreb 与 Veres 上 Sinkhorn 距离优于匹配的从头训练模型 [20]。与之相对，CellScientist 关注的是预测失败后的修正问题：它把高层假设空间与低层可执行实现空间耦合，将执行偏差路由回假设或实现层面，形成假设-实现-假设闭环，在形态学与转录组基准及单细胞扰动评估中，案例里 **PCC 由 0.3416 提升至 0.4368**，最终可执行模型在固定协议下优于参考基线 [21]。两者都涉及扰动响应，但前者明确仅做预测建模、不声称具备规划或推演能力 [20]，后者则依赖 LLM 代理且长程工作流仍脆弱 [21]。

在更宏观的框架层面，有工作提出将虚拟细胞构建为多模态、多尺度、有状态的动态计算系统，并以世界模型作为操作框架，支持动作条件仿真、反事实推理与长程规划，给出架构、数据框架、训练策略与评估原则 [13]。其核心主张是虚拟细胞世界模型应建模底层细胞系统本身，使干预在演化状态中传播，而非仅优化特定任务端点，并据此与面向特定任务的预测型基础模型形成对照 [13]。但该文属愿景性论文，**未报告定量结果**，也无实验验证 [13]；因此它与上述两项有具体基准数字的工作之间，尚不能就性能高低作比较，差异主要体现在**是否提供可执行、可评估的闭环机制**这一层面。

## 3 数据与资源

近年的扰动图谱在规模与覆盖维度上快速扩展，但不同工作在细胞体系、扰动类型和读出层面差异明显。**Tahoe-100M** 借助 Mosaic 平台将遗传上不同的细胞模型多重化为平衡的“细胞村”，构建了包含 **1亿转录组**、50个癌细胞系、1100种药物-剂量条件的单细胞扰动图谱，并系统量化增殖、细胞毒性、谱系特异性脆弱性与细胞周期变化 [29]。与之互补，基因组规模 Perturb-seq 用 CRISPRi 靶向全部表达基因、覆盖 **超过250万人类细胞**，以转录表型预测功能未知基因并发现核糖体生物发生等新调控因子 [30]；而针对原代免疫细胞的工作则在 **4名供体、2200万原代人CD4+T细胞** 上开发探针式 perturb-seq，测量静息与刺激后的转录组效应，发现活跃调控因子及其所控程序随刺激条件剧变 [31]。三者分别代表了药物扰动、基因敲低扰动与原代细胞扰动三类资源，其细胞来源（癌细胞系 vs 原代细胞）和扰动方式不可直接比较。

在读出维度上，空间与体内信息成为新的扩展方向。**iGOF-Perturb-seq** 作为体内功能获得性扰动测序平台，在小鼠星形胶质细胞中构建了 **约1000个转录因子** 的功能图谱，识别共功能模块并注释未表征 TF，并在神经炎症模型中鉴定 Ferd3l 为治疗候选 [33]；SPAC-seq 则将 CRISPR 筛选与空间组学结合，配套 TARDIS 分析工具，把基因扰动与空间表型和通路关联，揭示 Icam1 缺失促转移等空间表型 [32]。这两项工作把扰动响应从转录组丰度推进到组织空间与体内情境，但前者限于小鼠与单一细胞类型、后者未明确说明通量与适用组织范围的限制，向人类与更广组织的转化仍需验证。

面向预测建模，资源建设开始与模型训练直接耦合。**ProteinTalks** 基于 **超过3800万条时序蛋白丰度测量** 的扰动乳腺癌细胞系数据，学习可迁移的动态潜表示，在药物疗效与协同预测、耐药蛋白发现、患者分层及类器官候选药物排序上普遍优于所选基准，并可迁移至患者类器官与临床活检 [14]。与之配套的评估基础设施也在形成：Arc Institute 建立的 **Virtual Cell Challenge** 提供评估框架、专用数据集与竞赛平台，作为反复举办的开放基准推动扰动响应预测 [35]。值得注意的是，现有资源多集中于癌细胞系或单一原代细胞类型，蛋白质组时序数据与转录组图谱之间尚缺统一基准，不同研究各自选用的基准与评估协议也使跨工作比较存在争议。

## 4 评测与效度批判

评测效度批判的核心争议在于：模型在标准基准上的高分究竟反映生物学泛化能力，还是评估设置本身的产物。多项独立工作从数据划分、指标校准和基线选择三个层面给出了否定性证据。**细胞级随机划分**会把同克隆、同患者或同批次的"亲属细胞"放入训练集，模型可通过记忆亲属标签而非学习可迁移规则获得高分；该研究提出以暴露度与可检索性在训练前估计泄漏，并指出在患者队列中泄漏足以推翻临床结论 [24]。与之呼应，**EL-PERTURB** 采用分层分布外划分，在必需基因与全基因组 Perturb-seq 数据上压力测试 6 类架构的 20 个模型，结论是现有基准多依赖随机划分而掩盖系统性失效模式，模型在真实 OOD 条件下泛化失败 [37]。

在遗传扰动预测这一子问题上，最尖锐的冲突是深度学习模型与简单基线的对比。一项比较五种基础模型与两种深度学习模型的研究报告**没有任何模型优于简单线性基线**，所用数据含 1,000 个读出基因、62 个双扰动，并识别出 5,035 个遗传互作（潜在 124,000）[10]。在 Perturb-seq 基准上，最简单的 Train Mean 即优于 scGPT 与 scFoundation，带 GO 特征的随机森林进一步领先（如 Replogle K562 上 RF+GO 的 Pearson Delta 为 **0.480**，Train Mean 为 0.373，scGPT 为 0.327），作者并指出当前 Perturb-Seq 基准数据扰动特异性方差低、不适合评估此类模型 [22]。**Systema** 框架把原因归结为"系统性变异"——扰动组与对照组之间由选择偏差或混杂因素造成的一致转录差异；在十个数据集（三种技术、五种细胞系）上，简单 perturbed mean 在 Pearson Δ 上跨所有数据集优于其他方法，双基因扰动中 matching mean 显著更优，而 CPA、GEARS、scGPT 均难以泛化到系统性变异之外 [23]。

对这一"深度模型不如基线"的共识，存在明确的方法学反驳。有研究提出阳性对照基线与指标校准框架，在 **14 个数据集、18 个指标**上发现 MSE 和 Pearson Δ 等常用指标常校准不良，降低了对阳性模型性能的敏感性；在良好校准指标下，深度学习扰动模型可优于无信息基线 [11]。这意味着前述负面结论至少部分可归因于指标而非模型本身，构成该子领域尚未解决的核心争议。**VCBench** 从能力维度切入，将四个虚拟细胞框架综合为七个维度，评估 Geneformer、scGPT、UCE、TranscriptFormer、Arc State 与线性/最近邻基线，发现基线在五个评分维度中的四个匹配或超过所有基础模型；TranscriptFormer 跨模态 RNA 到蛋白预测 Pearson 提升 **53%**，但时间排序性能崩溃；多尺度整合与计算机模拟实验被判定为端到端结构上不可测试，且无基础模型发布完整细胞级训练清单，数据污染对用户不可检测 [25]。

预训练规模这一常被默认的效度来源也受到质疑。用 **2220 万细胞**语料预训练 400 个模型并开展 6,400 次实验后，性能在数据规模远小于现有语料时即达平台期，未发现类似大语言模型的数据缩放定律，提示应平衡模型容量、数据与算力而非盲目扩大 [12]。在药物响应方向，单药癌症 DRP 模型通常能做癌症盲预测，但**药物盲**性能显著下降、部分模型完全失败，药物盲泛化主要限于同类内 [39]。跨任务的大规模比较则显示，扰动效应幅度强烈影响泛化与双扰动预测，细胞类型迁移中源-目标转录组距离越大准确率越低，且实验系统多限于细胞系，原代与体内适用性有限 [38]。

评测对象与任务定义的差异进一步分裂了证据图景。**scArchon** 基于 Snakemake 构建可复现模块化平台，在六个 scRNA-seq 数据集上标准化评估九种工具（trVAE、scDisInFact、scVIDR、scPRAM、scGen、SCREEN、CPA、scPreGAN、CellOT），提供 MSE、Wasserstein 距离等指标与聚合排名，但明确仅限非遗传扰动，基因敲除作为独立问题未纳入 [26]。**AssayBench** 则把表型筛选预测重构为基因排序任务，基于 **1,920 个 CRISPR 筛选**、五类表型、每筛选约 13,826 个基因，引入调整 nDCG 以跨异质实验比较，发现零样本通用 LLM 优于生物学专用 LLM 和可训练基线，现有方法远未达经验性能上限 [27]。二者说明"扰动预测"并非单一任务，模型排名随任务形式与指标而变。

在因果效度层面，单细胞 CRISPR 筛选的统计关联不能直接读作因果效应：需附加超出标准统计分析的因果假设，且方法仅能识别一个基因敲低对另一基因的效应，无法直接推断两基因间的因果效应 [15]。更早的 Perturb-seq 流形工作则展示了另一条路径——将高维单细胞表型映射为细胞状态流形以实现通路无偏排序与遗传互作分类，但其依赖生长表型挖掘强互作、覆盖有限 [49]。面向真实场景的标准化模块化基准进一步报告：常用设置下性能被高估，严格条件下显著下降，简单线性模型仅捕捉全局转录趋势、无法恢复细粒度扰动特异效应，且不同指标导致模型排名差异显著 [28]。**Virtual Cell Challenge 2026** 把这一效度关切推进到跨独立细胞情境的零样本设定，在含未见细胞系的 Arc 新数据集上预测基因敲低响应，目标是检验最优模型能否缩小临床前实验预测与人类生物学之间的差距 [36]。

## 5 产业动态

（本节暂无入库证据）

## 6 空白与趋势

综合上述证据，本方向的空白与趋势可归纳为以下六条，每条附支撑依据。

1. **评测效度批判已形成共识，但"如何修"尚无共识，指标校准本身成为新的争议前线。** 细胞级随机划分泄漏组内答案、患者队列中泄漏足以推翻临床结论[24]；分层分布外划分下 6 类架构 20 个模型泛化失败[37]；Systema 报告简单 perturbed mean 在十个数据集上跨全部数据集优于其他方法[23]；Train Mean 优于 scGPT 与 scFoundation[22]；VCBench 发现基线在五个评分维度中的四个匹配或超过所有基础模型，且无基础模型发布完整细胞级训练清单、数据污染对用户不可检测[25]。但阳性对照基线与指标校准框架在 14 个数据集、18 个指标上发现 MSE 与 Pearson Δ 常校准不良，良好校准指标下深度学习模型可优于无信息基线[11]。**空白在于：尚无工作把"泄漏估计—划分协议—指标校准—基线选择"整合为单一可复现的评测流水线**，leakcheck[24]、scArchon[26]、Systema[23] 各自只覆盖其中一环。

2. **"复杂生成架构是否必要"被反复质疑，简单先验+检索/排序路线缺少与生成模型在同等严格协议下的正面对照。** 知识图谱最简 KNN 加 RL 优化邻域在 Replogle 2022 上达 SOTA[9]；AssayBench 上零样本通用 LLM 优于生物学专用 LLM 和可训练基线[27]；OCOO-T 自承基于扩散/流匹配的方法学习对照到扰动分布仍具挑战[5]。**空白在于：这些"简单方法强"的证据分散在各自设定的基准上，尚无在同一 OOD 划分、同一校准指标下对 KNN/线性基线、流匹配、离散扩散、传输模型做统一横评的工作**；现有横评或限于非遗传扰动[26]，或未纳入最新生成模型。

3. **世界模型/闭环智能体的愿景与可执行机制之间存在明显断层。** 世界模型框架主张建模底层细胞系统本身、使干预在演化状态中传播，但属愿景性论文、未报告定量结果[13]；Chreode 明确仅做预测建模、不声称具备规划或推演能力[20]；CellScientist 依赖 LLM 代理且长程工作流仍脆弱[21]。**空白在于：尚无工作把"动作条件仿真—反事实推理—长程规划"的完整闭环在统一基准上跑通并给出可审计轨迹**，现有闭环仅到"假设-实现"层面的定向更新[21]。

4. **扰动数据的读出维度正在从转录组丰度向蛋白质组、空间与体内扩展，但跨模态、跨体系的统一基准缺失。** ProteinTalks 基于超过 3800 万条时序蛋白丰度测量并可迁移至患者类器官与临床活检[14]；SPAC-seq 把扰动与空间表型关联[32]；iGOF-Perturb-seq 在体内构建约 1000 个 TF 图谱[33]；Tahoe-100M 覆盖 1 亿转录组、50 细胞系、1100 药物-剂量条件[29]。**空白在于：蛋白质组时序数据与转录组图谱之间尚无统一基准，且这些资源在细胞来源（癌细胞系 vs 原代细胞）与扰动方式上不可直接比较**，跨资源迁移的可比性未被系统检验。

5. **因果效度的形式化程度不足，生成模型普遍借用调控网络作为约束，但约束来源的可靠性未被评估。** 单细胞 CRISPR 筛选的统计关联需附加超出标准统计分析的因果假设，且仅能识别敲低对另一基因的效应而非基因间直接因果效应[15]；D-SPIN 与 RegVelo 依赖数据推断的网络[16][17]，CauTrigger 依赖因果分解假设[18]。**空白在于：尚无工作量化"所引调控先验的错误率如何传播到扰动响应预测误差"**，即先验质量与生成质量之间的敏感性分析缺失。

6. **预训练规模收益见顶与知识增强路线并存，二者的取舍缺少可预测的判据。** 2220 万细胞预训练 400 个模型、6400 次实验显示性能在数据规模远小于现有语料时即达平台期，无清晰数据缩放定律[12]；scKITE 仅用 179,067 样本（不足先前强模型 0.5%）即在多下游任务超越 Geneformer、scGPT 等，知识增强带来平均 28.8% 相对提升[4]。**空白在于：尚无工作给出"何时该加数据、何时该加知识"的定量判据**，两条路线的证据各自成立但未在同一任务族上做因子化对照。

## 7 未归类新证据

人工智能虚拟细胞（AIVC）被提出作为整合多组学数据、贯通微观分子机制与宏观组织行为的研究新范式，其目标是突破传统实验与生化分析在时空分辨率和处理能力上的限制 [50]。该综述给出了AIVC的统一技术框架，将其分解为**跨尺度表征工程、功能子模块设计与多组件动态调控机制**三个方面，并系统梳理了现有模型与数据集资源，如**GeneCompass、Tahoe-100M**等 [50]。

在方法层面，该工作属于综述性整合而非自行分析样本，其贡献在于定义与框架梳理，而非产生新的基准测试结果 [50]。作者同时指出，**数据异质性与模型可解释性**等挑战尚未解决，AIVC仍处于早期阶段 [50]。这一判断提示，当前AIVC的证据基础主要来自对既有模型与数据集的归纳，跨尺度耦合与动态调控机制能否在统一框架下得到验证，仍有待后续研究补充。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 扰动响应生成模型（flow matching / 扩散 / 最优传输 / 因果潜动力学） | 朝阳 | 方法线从 scGen 的隐空间位移 [1] 演进到 State 的跨上下文状态迁移 [41] 与 X-Cell 的因果扰动预测规模化 [6]，说明范式仍在快速换代而非收敛；同时 scGPT [2] 这类基础模型被大量当作 backbone 复用，表明"基础模型 + 扰动头"已成主流骨架但具体生成机制未定。雷达样本中该节 n=23、近两年占比 **0.89**，属证据最密集的一节。 |
| 细胞世界模型与闭环智能体 | 萌芽 | 仅 3 篇且全部为 2026 年：Chreode 提出一步式时序动力学与扰动预测的世界模型 [20]，CellScientist 做双空间分层编排的闭环精化 [21]，加上 Cell 的观点文章 [13]。概念刚被提出、无横向对比、无统一评测，属典型早期探索；雷达样本中该节 n=3，样本量本身也提示证据稀薄。 |
| 扰动数据资源与大规模图谱 | 成熟（资源层）/ 朝阳（空间化扩展） | 基因组规模 Perturb-seq 图谱 [30] 已把"数据有没有"变成"怎么用"的问题，Virtual Cell Challenge 把数据转成标准化竞赛与 Turing test 式评测 [35]，说明数据层进入基础设施化阶段；但空间分辨功能基因组 [32] 与体内增益功能筛选 [33] 显示资源正从"细胞系 + 体外"向"空间 + 体内"扩张，仍有新维度可占。 |
| 评测基准与效度批判 | 朝阳（且是当前最有话语权的一节） | 关键负结果：深度学习扰动预测尚不能超越简单基线 [10]，基础细胞模型在后扰动 RNA-seq 预测上的基准同样不乐观 [22]；Systema 进一步把评测从"拟合精度"推进到"超越观测的泛化" [23]。三代工作（否定 → 细化 → 框架化）在 **2 年内**连续出现，说明评测口径正在被重写、尚未定型。 |
| 产业动态（可核验技术细节） | 证据不足 | 雷达样本中该节 n=0，无任何可核验的产业发布证据，无法判断阶段。 |

**整体判断**：这个方向整体处于**朝阳期的中前段**——生成模型范式未收敛（隐空间位移 → 状态迁移 → 因果规模化，两三年一换），而评测侧已经用**负结果**把"刷 benchmark"的路堵了一半 [10][22]。真正的空白在**世界模型 / 闭环智能体**（雷达样本中仅 3 篇、全为 2026 年）[20][21] 和**空间 / 体内扰动资源** [32][33]。窗口期估计 **12–18 个月**：世界模型概念刚落地、尚无公认评测，谁先给出"可复现的闭环 + 诚实的效度分析"谁就定义赛道；一旦 Virtual Cell Challenge 类基准把世界模型纳入正式赛道 [35]，入场成本会迅速抬高。**最大不确定性**是效度：现有最强负结果说明多数模型学到的可能只是"平均扰动效应 + 上下文偏置"，若世界模型的增益同样来自数据泄漏或简单基线可复现的成分，整条线会被一次性证伪；其次是数据维度错配——公开 Perturb-seq 以细胞系为主 [30]，而类器官 / 空间数据的扰动标签稀少，跨域迁移是否成立尚无证据。

**接下来怎么做**

1. **把"效度批判"做成自己的方法学名片，而不是绕开它。** 切入点：在 Systema 的"超越观测泛化"框架 [23] 上，复现并扩展负结果 [10][22]，加入**简单基线族**（均值位移、线性加性、kNN 上下文匹配）与**分布外划分**（未见细胞类型 / 未见扰动组合）。产出：一个开源评测包 + 一篇"哪些增益是真的"的分析。为什么现在：评测口径正在重写、尚无定论，此时进入成本最低、引用窗口最大；且这类工作对算力要求低，适合博后独立起步。

2. **用类器官 + 多组学做"跨上下文迁移"的稀缺验证集。** 切入点：以公开 Perturb-seq 图谱 [30] 为训练源，把合作项目的类器官多组学扰动数据作为**外部验证域**，检验 State 式跨上下文状态迁移 [41] 与 X-Cell 的因果规模化设定 [6] 是否在体外 2D → 类器官 3D 的域偏移下仍成立。产出：首个"细胞系 → 类器官"扰动迁移的效度报告，正负结果都有价值。为什么现在：所有生成模型都在宣称 cross-context，但验证几乎全在细胞系内部；类器官数据是你独有的护城河，且能直接反哺合作项目。

3. **在世界模型上抢一个"最小可复现闭环"，别做通用框架。** 切入点：以 Chreode 的一步式时序动力学 [20] 为基线，把 CellScientist 的闭环精化思想 [21] 缩到一个**窄任务**（如"给定扰动 → 预测 24h/72h 状态 → 用主动实验选择下一轮扰动"），在公共数据上做 demo、在类器官上做小规模真实验证。产出：闭环 agent 的开源实现 + 主动学习相对随机选点的增益曲线。为什么现在：该节雷达样本仅 3 篇、全为 2026 年，概念期入场；且闭环的瓶颈是"实验预算下的决策"，正好匹配你的湿实验合作资源，而不是拼模型规模。

4. **把空间维度作为差异化切口，而不是追细胞系规模。** 切入点：结合空间分辨 CRISPR 筛选 [32] 与体内增益功能筛选 [33]，构建"空间上下文作为扰动响应条件变量"的建模任务，检验现有生成模型 [41] 在加入邻域 / 组织位姿信息后是否改善。产出：空间扰动响应的数据集整理 + 条件化建模基线。为什么现在：数据资源层在细胞系维度已基础设施化 [30]，增量空间小；空间与体内是刚打开的新维度，且与类器官（自带空间结构）天然契合。

5. **对接 Virtual Cell Challenge 的评测口径，把工作挂在公共赛道上。** 切入点：按 [35] 的任务定义与划分提交方法，同时公开你的效度分析代码，形成"参赛 + 批判"双身份。产出：榜单成绩 + 方法论文 + 可复用评测脚本。为什么现在：基准刚建立、赛道尚未饱和，早期提交的方法更容易成为后续对照基线；同时这是把前面 1–4 条串成一条叙事的最低成本粘合剂。

## 参考文献

1. scGen predicts single-cell perturbation responses. Nature Methods 2019. https://doi.org/10.1038/s41592-019-0494-8
2. scGPT: toward building a foundation model for single-cell multi-omics using generative AI. Nature Methods 2024. https://doi.org/10.1038/s41592-024-02201-0
3. Tahoe-x1: Scaling Perturbation-Trained Single-Cell Foundation Models to 3 Billion Parameters. bioRxiv 2025. https://doi.org/10.1101/2025.10.23.683759
4. Towards a knowledge-enhanced single-cell foundation model.  2026. https://arxiv.org/abs/2609.14970
5. OCOO-T : A Simple and Scalable Virtual Cell Model for Transcriptional Perturbation Response Prediction.  2026. https://arxiv.org/abs/2606.12838v2
6. X-Cell: Scaling Causal Perturbation Prediction Across Diverse Cellular Contexts via Diffusion Language Models.  2026. https://doi.org/10.64898/2026.03.18.712807
7. SCALE:Scalable Conditional Atlas-Level Endpoint transport for virtual cell perturbation prediction.  2026. https://arxiv.org/abs/2603.17380v3
8. $D^{2}R^{2}$: Discrete Diffusion with Regulation Reinforcement for Single-Cell Perturbation Prediction.  2026. https://arxiv.org/abs/2608.15288v1
9. Knowledge Graphs and Reasoning LLMs for Finding Simple Yet Effective Transcriptomic Perturbation Predictors.  2026. https://arxiv.org/abs/2606.08816v1
10. Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines. Nature methods 2025. https://doi.org/10.1038/s41592-025-02772-6
11. Deep learning perturbation models can outperform baselines on calibrated metrics.. Nature biotechnology . https://doi.org/10.1038/s41587-026-03307-w
12. Evaluating the role of pretraining dataset size and diversity on single-cell foundation model performance.. Nature methods 2026. https://doi.org/10.1038/s41592-026-03120-y
13. A world model of the virtual cell.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.042
14. An operational perturbation proteomics-based virtual cell model.. Nature 2026. https://doi.org/10.1038/s41586-026-11001-9
15. Causal effect estimation from trans-regulatory single-cell CRISPR screens.. Cell genomics 2026. https://doi.org/10.1016/j.xgen.2026.101251
16. D-SPIN constructs regulatory network models from scRNA-seq that reveal organizing principles of perturbation response.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.028
17. RegVelo: Gene-regulatory-informed dynamics of single cells.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.022
18. CauTrigger: deciphering biological system state transitions by hierarchical causal decomposition.. Nature methods . https://doi.org/10.1038/s41592-026-03274-9
19. CellFluxRL: Biologically-Constrained Virtual Cell Modeling via Reinforcement Learning.  2026. https://arxiv.org/abs/2603.21743v4
20. Chreode: A Cell World Model for One-Step Temporal Dynamics and Perturbation Prediction.  2026. https://arxiv.org/abs/2605.28111v1
21. CellScientist: Dual-Space Hierarchical Orchestration for Closed-Loop Refinement of Virtual Cell Models.  2026. https://arxiv.org/abs/2605.07335v1
22. Benchmarking foundation cell models for post-perturbation RNA-seq prediction. BMC genomics 2025. https://doi.org/10.1186/s12864-025-11600-2
23. Systema: a framework for evaluating genetic perturbation response prediction beyond systematic variation. Nature biotechnology 2026. https://doi.org/10.1038/s41587-025-02777-8
24. Cell-level random splits leak group-owned answers in single-cell benchmarks. bioRxiv 2026. https://doi.org/10.64898/2026.09.09.750484
25. VCBench: A Multi-Dimensional Benchmark for Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.06.18.733146
26. scArchon: a scalable benchmarking framework for assessing single-cell perturbation models.. Genome biology 2026. https://doi.org/10.1186/s13059-026-04104-z
27. AssayBench: An Assay-Level Virtual Cell Benchmark for LLMs and Agents.  2026. https://arxiv.org/abs/2605.10876v1
28. Benchmarking virtual cell models for in-the-wild perturbation response.  2026. https://arxiv.org/abs/2604.27646v1
29. Tahoe-100M: Mapping drug-induced molecular phenotypes at single-cell resolution.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.035
30. Mapping information-rich genotype-phenotype landscapes with genome-scale Perturb-seq. bioRxiv 2021. https://doi.org/10.1016/j.cell.2022.05.013
31. Genome-scale perturb-seq in primary human CD4&lt;sup&gt;+&lt;/sup&gt; T cells maps context-specific regulators of T cell programs and human immune traits.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.002
32. Uncovering spatially resolved functional genomics with CRISPR screen sequencing.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.049
33. Mapping transcription factor functions in astrocytes using in vivo gain-of-function Perturb-seq.. Science (New York, N.Y.) 2026. https://doi.org/10.1126/science.adw2156
34. Joint single-cell capture of Cas9 edits and transcriptomes reveals on- and off-target effects on gene expression.. Nature methods . https://doi.org/10.1038/s41592-026-03319-z
35. Virtual Cell Challenge: Toward a Turing test for the virtual cell. Cell 2025. https://doi.org/10.1016/j.cell.2025.06.008
36. Virtual Cell Challenge 2026: Benchmarking zero-shot generalization across cellular contexts.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.004
37. Genetic Perturbation Prediction Models Fail Out-of-Distribution: A Rigorous Benchmark and Systematic Evaluation.  . https://doi.org/10.64898/2026.10.16.759604
38. A systematic comparison of single-cell perturbation response prediction models.. Science advances 2026. https://doi.org/10.1126/sciadv.aed3414
39. Monotherapy cancer drug-blind response prediction is limited to intraclass generalization.. PLoS computational biology 2026. https://doi.org/10.1371/journal.pcbi.1013232
40. Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling.  . https://doi.org/10.64898/2026.09.22.752128
41. Predicting cellular responses to perturbation across diverse contexts with State. Cell 2026. https://doi.org/10.1016/j.cell.2026.07.052
42. scBalFlow: A Staged Flow Matching Framework for Imbalanced Single-Cell Drug Perturbation Prediction.. Bioinformatics (Oxford, England) 2026. https://doi.org/10.1093/bioinformatics/btag682
43. Deep dynamical models of single-cell multiomic velocities predict loss-of-function and rescue perturbations in B cells.. Nature biotechnology . https://doi.org/10.1038/s41587-026-03348-1
44. Predicting how perturbations reshape cellular trajectories with PerturbGen.  2026. https://doi.org/10.64898/2026.03.04.709254
45. scDEFT: A deep learning framework for drug-effect prediction and counterfactual reasoning.  2026. https://arxiv.org/abs/2609.10831
46. UniPert-G2CP bridges genetic and chemical screens from molecular representation to phenotype modeling.. Cell 2026. https://doi.org/10.1016/j.cell.2026.06.005
47. A transcription factor regulatory atlas for activity inference and perturbation prediction. Nucleic Acids Research 2026. https://doi.org/10.1093/nar/gkag897
48. PerturbBridge: Direct Phenotypic Supervision for Cellular Perturbation Generation.  . https://arxiv.org/abs/2610.17066
49. Exploring genetic interaction manifolds constructed from rich single-cell phenotypes. Science 2019. https://doi.org/10.1126/science.aax4438
50. Artificial intelligence-enabled multi-scale virtual cell: perspective, challenges, and opportunities.. Briefings in bioinformatics 2026. https://doi.org/10.1093/bib/bbag104
