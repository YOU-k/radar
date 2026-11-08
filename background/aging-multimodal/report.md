# 多模态衰老时钟与生物年龄 · 方向背景报告

证据 81 篇 · 覆盖度 0.60 · 第 10 轮 · 更新 2026-11-08 · 数字核验删句 1

## 本次变更

- 新增 [https://huggingface.co/datasets/transhumanist-already-exists/pansci-mouse-aging-snrna] [dataset] transhumanist-already-exists/pansci-mouse-aging-snrna

## 摘要（TL;DR）

- Horvath 多组织预测器整合 **82 个 Illumina 数据集、7844 个非癌样本、51 种组织/细胞类型**，用弹性网络从 21,369 个共有 CpG 中选出 **353 个 CpG**，测试误差约 **3.6 年** [1]。
- 一项基于 Generation Scotland **18,859 人**、174 种新发疾病、10 年随访的无偏比较显示，第二代和第三代时钟显著优于第一代，完全校正模型下 13 种时钟与 57 种疾病共 **176 个 Bonferroni 显著关联**，其中 **GrimAge v2 和 DunedinPACE 各 72 个** [2]。
- 在 83 人、284 份五类组织样本中，口腔与血液组织的表观年龄平均差近 **30 年**，多数血液时钟与口腔组织相关性低，**Skin and Blood clock** 一致性最高 [3]。
- UK Biobank 中基于 **2,897 个血浆蛋白、45,441 人**的时钟经 Boruta 筛出 **204 个蛋白**，与实际年龄 **Pearson r=0.94**，其年龄差与 27 个衰老表型、全因死亡和 26 种年龄相关疾病关联 [4]。
- 基于 ARCHS4 **56,877 例、2-114 岁**多组织的混合专家模型报告 **MAE=7.58 年**，肺和脑预测最佳、肝较差，并指出残差随年龄增大、百岁老人误差达 **±40 年** [5]。
- UK Biobank 274,247 人、107 种非衍生代谢物构建的 5 个 MetBAG，独立测试集 Pearson r 仅 **0.25<r<0.42**，平均绝对误差约 6 年，关联 525 个疾病终点 [6]；而 MULTI Consortium 313,645 人的 7 个 MRIBAG 在留出测试中 r 为 **0.23–0.77**、MAE 约 5 年 [7]。
- **LongevityBench** 覆盖 5 个生物数据域、17 项任务，评测来自 6 个开发团队的 18 个前沿 AI 系统，结论是**没有单一模型主导所有任务**，且**组学年龄预测是最难的任务**，与模型规模无关 [8]。
- **Longevity-LLM v0.1** 将 Qwen3-14B 在 DNA 甲基化、蛋白质组、临床生物标志物和 RNA 表达数据上经监督与强化学习微调，强化微调后表观年龄预测 **MAE 为 4.34 年**，超过 Horvath 多组织时钟 [9]。
- **SenePy** 利用 **72** 个小鼠和 **64** 个人类加权单细胞转录组 signature 构建评分平台，发现仅 **58/1540** 细胞类型组合的标志物重叠显著，说明衰老标志物高度组织细胞特异 [10]。
- 40个月二甲双胍干预雄性食蟹猴的研究构建了多组织转录组、DNA甲基化、血浆蛋白与代谢组的猴衰老时钟，**二甲双胍显著延缓衰老指标，脑衰老约回退6年** [11]。

## 1 背景与定义

表观遗传时钟的演化脉络已由第一代「以实际年龄为训练目标」、第二代「以表型/死亡为训练目标」推进到第三代「以因果与机制为目标」，但**三代时钟之间缺乏统一的验证口径**：同一研究内的对照显示 GrimAge v2 与 DunedinPACE 在 174 种疾病上关联最强 [2]，而 LinAge2 在 20 年死亡预测上报告 AUC=0.8684 并优于 PhenoAge 与 GrimAge2 [12]，两项研究的队列、结局集与对照设置不同，其数字不可横向比高低。更根本的边界在于，**时钟位点的生物学含义尚未收敛**：一条证据把 353 个 CpG 邻近 Hox/polycomb 发育基因、据此连接程序性衰老理论 [13]，另一条直接分析则发现多数时钟 CpG 不与转录因子结合位点重叠，且仅用弱相关非 TFBS CpG 的模型 MdAE=3.77 年优于 Horvath1 的 5.95 年 [14]。这意味着「时钟精度」与「时钟机制解释」在当前证据下是两条尚未对齐的线索，方向边界应把「预测精度」与「因果/调控解释」分开评估，而非以单一误差指标统摄。

从单组学到多模态，核心问题已从「能否预测年龄」转为「**预测增益是否来自模态本身，还是来自样本量与平台**」。蛋白组方向在 UKB 同一平台上出现多个规模不同的器官时钟：2,916 蛋白/44,498 人报告脑、动脉与整体年龄对传统年龄 r² 达 0.97 [15]，2,448 蛋白/43,498 人的 ProtBAG 则把年龄偏倚校正、器官蛋白特异性、样本量与训练病理列为方法学要点 [16]；两文共享平台但蛋白数与样本量不同，预测增益不能直接比较。代谢组与影像组的精度落差更明显：274,247 人、107 种代谢物的 5 个 MetBAG 独立测试 r 仅 0.25<r<0.42 [6]，而 313,645 人的 7 个 MRIBAG 留出测试 r 为 0.23–0.77、MAE 约 5 年，且明确指出腹部 MRI 特征共线性导致泛化较差、脑模型存在域偏移 [7]。**因此「多模态优于单模态」目前只是各研究内部的主张，跨模态、跨队列的可比证据仍缺位**；跨组学整合的 StackAge 报告 r≈0.93 但未纳入表观遗传层、以横断面为主 [17]，恰说明模态覆盖与纵向设计是当前整合工作的共同短板。

单细胞与空间组学把衰老从组织均值推进到细胞类型与空间位置，随之而来的是**「通用衰老特征」与「细胞类型特异特征」的取向冲突**。SenePy 发现仅 58/1540 细胞类型组合的标志物重叠显著，主张衰老标志物高度组织细胞特异 [10]；hUSI 则从 73 项研究学习通用特征并在 bulk 与单细胞多种条件下优于 31 种方法 [18]。单细胞时钟同样分叉：sc-ImmuAging 为五类免疫细胞分别建模、基于 1081 人约 130 万细胞 [19]，scAgeClock 走跨组织门控多头注意力路线 [20]，二者训练数据与验证范围差异明显，**孰优尚缺同一队列内的直接比较**。空间维度的证据已把「衰老细胞在哪、与谁互作」变成可测量问题——小鼠九组织空间转录组定位免疫球蛋白聚集与 IgG 积累 [21]，人皮肤 SenSkin™ 显示光老化衰老负担高于时序衰老 [22]，人骨骼肌单核 RNA+ATAC 解析 SASP 异质性 [23]——但组织与物种各异，结论不能直接互推。

基准与基础模型的出现，标志着该方向开始从「堆叠预测器」转向「**可比较的评测问题**」。LongevityBench 覆盖 5 个数据域、17 项任务、18 个前沿系统，结论是**没有单一模型主导所有任务，组学年龄预测是最难的任务且与模型规模无关**，微调的 0.6B–9B 多任务 Longevity-LLM 可匹配或超过更大系统 [8]。表观遗传方向有 ComputAgeBench 以「区分健康与衰老加速疾病个体」为核心假设、整合 66 个血液 DNAm 数据集与 19 种疾病、测试 13 个已发表时钟 [24]；单细胞层面有覆盖 5 个生物学问题、超 250 万单细胞转录组的表征基准，发现冻结预训练表征时 Geneformer 在时序年龄预测上最佳，但 2000 个高变基因的平均表现更高 [25]。**这些基准的覆盖面并不一致**：ComputAgeBench 仅限血液 DNAm、单细胞基准仅限转录组，而 LongevityBench 虽跨 5 域仍发现组学年龄预测最难 [8]——这与综述中「表观时钟最准确」的判断 [26] 分别来自跨任务评测与叙述性综述，二者不可直接对照，恰说明**该领域尚缺统一、跨模态的验证口径**。基础模型的最直接主张来自 Longevity-LLM v0.1：Qwen3-14B 经微调后表观年龄预测 MAE 为 4.34 年、超过 Horvath 多组织时钟 [9]，但该报告未说明数据规模与公开情况，「替代专用时钟」仍是待验证主张而非定论。

数据资源与扰动体系构成该方向的另一条边界。Biolearn 以统一整理、协调与评估框架回应跨人群验证缺乏标准化方法的问题，输出标准化格式并比较性能、稳健性与泛化性，但依赖已有公开数据、临床验证待推进 [27]；Immunosenescence Inventory 整合单细胞、bulk、表观组与 TCR/BCR 多物种数据并提供免疫时钟工具，但未提供统一预测性能基准、单细胞层面覆盖仍有限 [28]。**两者在「可比较的标准化评估」上均存在未解问题**。扰动侧，Cell Painting 自 2013 年提出以来在协议、特征提取、质控与批次校正上持续改进并用于机制、毒性与多组学整合，但该综述未提供统一定量基准 [29]；转录组扰动筛选则鉴定出 SRSF1 可产生强烈年轻化转录特征且不丧失细胞身份，但仅为人成纤维细胞体外模型、样本规模与体内验证未提及 [30]。**成像表型与转录组扰动两条路线方法学与验证层级不同，尚无同一研究内的对照数据**，这正是类器官/扰动体系里衰老建模尚未打通的关键缺口。

## 2 方法学


### 2.1 单组学衰老时钟（表观 / 蛋白 / 转录）

表观遗传时钟是单组学衰老时钟中发展最成熟的一支。Horvath 多组织预测器整合 **82 个 Illumina 数据集、7844 个非癌样本、51 种组织/细胞类型**，用弹性网络从 21,369 个共有 CpG 中选出 **353 个 CpG**，测试误差约 **3.6 年**，并显示早衰症不符合正常衰老、iPS 重编程可将时钟重置为 0 [1]。该工作奠定了「以实际年龄为训练目标」的第一代时钟范式，其局限也随之后续：仅用两平台共有 CpG、训练数据异质、组织覆盖有限 [1]。围绕时钟位点的生物学解释，有综述指出 Horvath 时钟的 353 个 CpG 邻近 Hox、polycomb 等发育基因，并据此把表观时钟与程序性衰老理论联系起来 [13]；但另一项直接分析发现，多数时钟 CpG 并不与转录因子结合位点重叠，说明时钟精度并非主要由 TF 结合动态驱动，且一个仅用弱相关非 TFBS CpG 的模型 **MdAE=3.77 年**，优于 Horvath1 的 5.95 年、接近 PhenoAge 的 3.79 年 [14]。这两条证据对「时钟 CpG 的调控含义」给出了不同侧重，前者强调发育程序关联，后者强调多数位点缺乏已知调控注释。

第二代时钟转向以表型而非实际年龄为训练目标。DNAm PhenoAge 用包含临床表型年龄的复合指标替代实际年龄，通过两步流程筛选 CpG，报告其在全因死亡、癌症、健康寿命、身体功能和阿尔茨海默病预测上优于既往指标 [31]；但该研究基于全血开发，摘要未给出样本规模与误差指标 [31]。更进一步的因果化尝试用表观全基因组孟德尔随机化识别可能因果影响衰老性状的 CpG，构建分别追踪损伤性与适应性甲基化变化的 **DamAge** 与 **AdaptAge**，发现前者与死亡等不良结局相关、后者与有益适应相关，且两者对短期干预敏感 [32]；其限制在于因果 CpG 的功能验证有限、依赖 MR 假设 [32]。另有工作把时钟从单 CpG 提升到通路层面，构建 **PathwayAge**，整合 GO/KEGG 通路级甲基化并在多队列与疾病组织中验证，声称可揭示疾病特异性衰老通路 [33]；该研究主要基于 DNA 甲基化，通路解释仍受组织特异性和队列差异限制 [33]。

不同代际时钟的临床效用存在明确争议，且比较结论依赖同一研究内的对照。一项基于 Generation Scotland **18,859 人**、174 种新发疾病、10 年随访的无偏比较显示，第二代和第三代时钟显著优于第一代，完全校正模型下 13 种时钟与 57 种疾病共 **176 个 Bonferroni 显著关联**，其中 **GrimAge v2 和 DunedinPACE 各 72 个** [2]；该研究以欧洲裔为主、为观察性设计，且部分时钟与协变量信息重叠 [2]。LinAge2 的基准评测则报告其 20 年全因死亡预测 **AUC=0.8684**，优于 PhenoAge Clinical 的 0.8479 和 ChronAge 的 0.8288，20 年死亡 **AUC=0.8440**，优于 PhenoAge DNAm 的 0.7859 和 GrimAge2 的 0.8233 [12]；但作者承认未满足理想时钟全部标准、部分对比未达统计显著 [12]。这两项研究的队列、结局集与对照设置不同，其数字不宜直接横向比高低。

时钟的可靠性与响应性构成另一类争议。在干预响应方面，一项整合 **51 项**人类纵向干预研究、统一计算 16 种时钟与 94 种额外 DNAm 标志物的分析发现，不同干预与时钟的响应差异显著 [34]；其限制是文献碎片化、时钟面板不一致导致难以直接比较 [34]。此外，跨组织可比性也是一处硬约束：在 83 人、284 份五类组织样本中，口腔与血液组织的表观年龄平均差近 **30 年**，多数血液时钟与口腔组织相关性低，**Skin and Blood clock** 一致性最高 [3]。生命早期溯源方面，对第一至第三代时钟位点的纵向分析显示其发育轨迹高度异质且非线性，超过三分之一位点自出生即存在个体差异，高于非时钟位点，并与遗传背景和产前暴露相关 [35]。

蛋白质组时钟以血浆蛋白为底，规模与验证设计差异明显。UK Biobank 中基于 **2,897 个血浆蛋白、45,441 人**的时钟经 Boruta 筛出 **204 个蛋白**，与实际年龄 **Pearson r=0.94**，其年龄差与 27 个衰老表型、全因死亡和 26 种年龄相关疾病关联，并在 CKB（3,977 人）和 FinnGen（1,990 人）中独立验证 [4]；局限是主要发现基于 UKB、外部样本较小、观察性关联不能证明因果 [4]。另一项 PAC 时钟用 UKB **53,021 人、2,923 个 Olink 蛋白**、LASSO 建模，以全因死亡为代理，随访超 10 年，报告年龄偏差与死亡及多种年龄相关疾病显著关联 [36]；其训练仅限 UKB、平台单一、外部验证有限 [36]。器官特异方向在 UKB **43,616 人**、Olink 2,916 蛋白上构建整体与十个器官时钟，并在中国（3,977 人）和美国（800 人）队列验证，报告跨队列 **r=0.98 和 0.93**，脑衰老与死亡关联最强 [37]；部分器官可用蛋白少、因果机制有限 [37]。

蛋白组时钟的分化还体现在目标表型与蛋白子集上。健康寿命方向用 UKB **53,018 人、2,920 个蛋白**构建 HPS，在 43,119 名基线健康者中 **12,427 人（28.8%）**发生健康寿命终点事件，并报告 HPS 与多种生物学年龄指标相关 [38]；其人群以欧洲裔为主、健康寿命定义尚无共识、外部验证有限 [38]。ECM 方向仅用 **14 个血浆蛋白**构建时钟，发现 ECM 蛋白随龄呈 U 型轨迹、最低点约 **40-50 岁**，并称可区分健康与疾病 [39]；但所用 Robbins 队列最老仅 66 岁、U 型轨迹较弱 [39]。肌肉骨骼方向在 UKB **21,070 人**中构建 MSKAge 与 MSKAgeMort，报告 MSKAge 相关 **r 女性=0.62、男性=0.56**，MSKAgeMort 相关 **r 女性=0.93、男性=0.88**，其加速指标可预测死亡与肌肉骨骼病 [40]。纵向设计方面，KORA 队列用最多三个时间点、**9105 样本、4100 人、25-88 岁**的 LC-MS 血浆蛋白组构建时钟，发现年龄加速与生活方式和临床风险因素相关，心血管代谢暴露共享蛋白组特征而吸烟和体力活动具独特特征 [41]。这些工作目标表型（死亡、健康寿命、器官、ECM、肌肉骨骼）与蛋白面板各不相同，其相关数值不宜跨研究直接比较。

转录组时钟的争议集中在跨平台泛化与极端年龄误差。Pasta 采用「age-shift」学习框架，声称在 bulk 与单细胞 RNA-Seq、微阵列及跨物种上预测相对年龄，优于 MultiTIMER 和 tAge，可区分衰老/静息/干细胞状态并分层肿瘤分级与生存，p53 相关基因贡献显著 [42]；其限制是转录组噪声与批次效应、跨平台泛化仍受限 [42]。基于 ARCHS4 **56,877 例、2-114 岁**多组织的混合专家模型报告 **MAE=7.58 年**，肺和脑预测最佳、肝较差，并指出残差随年龄增大、百岁老人误差达 **±40 年** [5]。K-Dense 多智能体系统在 ARCHS4 **57,584 样本、28 组织、1,039 队列、1-114 岁**上报告 **R²=0.854、MAE=4.26 年**，并提供校准置信区间以标记过渡期和极端年龄预测 [43]。DeepQA 则针对「仅在健康样本训练、却在健康与非健康样本上推断」的偏倚，用混合专家与 Hinge-MAE 损失在 3,060 样本、31 数据集上训练，声称在健康和非健康受试者上均显著优于现有方法 [44]；其非健康样本的生物年龄缺乏金标准 [44]。上述转录组研究报告的误差指标来自不同数据集与组织构成，不能直接互比优劣。

跨组学与跨物种的证据提示单组学时钟的边界。StackAge 整合 UKB **30,376 人**的 2,923 蛋白与 251 代谢物，报告与实际年龄 **Pearson r≈0.93**，并称对 12 种慢性病风险预测增强、2 型糖尿病/阿尔茨海默病/慢性肾病 **AUC 超过 0.90** [17]；该工作未整合表观遗传层、以横断面基线为主 [17]。代谢组方向 MetaboAgeMort 用 UKB **239,291 人**、以 10 年全因死亡为替代指标，选出 **185 个**死亡相关代谢标志物，报告可提升 10 年死亡预测并关联疾病、可调因素与遗传位点 [45]；其以全因死亡为替代、样本主要为欧洲白人、外推性受限 [45]。非人模型方面，LivAge 基于小鼠肝脏 RNA-seq 构建转录组时钟，在早衰综合征中显示转录组年龄增加，并可评估 Snell Dwarf、Ames Dwarf、GHR 缺陷及热量限制等干预 [46]；其仅基于肝脏、验证范围有限 [46]。犬表观时钟用 **894 只犬的 1640 份甲基化组**构建，报告可预测死亡率、生命早期表观遗传衰老最快，大体型和雄性犬寿命更短且分子衰老加速，体型相关甲基化变化集中于转座子元件、性别相关变化集中于 X 染色体 [47]。这些跨组学与跨物种结果说明，单组学时钟的预测力与可解释性高度依赖训练表型、组织来源与验证队列，尚无某一组学或某一代时钟在所有结局上一致占优。

### 2.2 多模态整合与跨队列泛化

多模态整合的起点是同一平台上的器官分层。UK Biobank 中基于 **2,916 种血浆蛋白**、44,498 人的工作训练出 11 个器官年龄模型，其中脑、动脉和整体年龄对传统年龄的预测 r² 达 **0.97**，器官年龄差同时关联生活方式、用药与随访 17 年内的疾病发生 [15]。同一队列稍小规模（43,498 人、2,448 种蛋白）的 11 个 ProtBAG 研究进一步把蛋白时钟与 9 个表型年龄差时钟整合，报告跨器官特征可提升系统性疾病类别和全因死亡预测，并把年龄偏倚校正、器官蛋白特异性、样本量与训练病理构成列为方法学要点 [16]。两文共享 UKB 蛋白平台，但蛋白数与样本量不同，其预测增益不能直接比较。

代谢组与影像组把器官框架推向其他模态，代价是精度差异明显。UK Biobank 274,247 人、107 种非衍生代谢物构建的 5 个 MetBAG，独立测试集 Pearson r 仅 **0.25<r<0.42**，平均绝对误差约 6 年，关联 525 个疾病终点 [6]；而 MULTI Consortium 313,645 人的 7 个 MRIBAG 在留出测试中 r 为 **0.23–0.77**、MAE 约 5 年，并关联 2,923 种蛋白与 327 种代谢物 [7]。后者明确指出腹部 MRI 特征共线性导致泛化较差、脑模型在外部队列存在域偏移，这与蛋白时钟报告的高 r² 形成方法学上的张力：不同模态、不同队列的数字不宜横向比高低，只能各自内部对照。

跨队列泛化在表观遗传时钟上被最直接地检验。针对 Horvath 与 PedBE 时钟在墨西哥儿童青少年 523 份血样中预测准确性下降的问题，迁移学习框架被用于适配 EPIC 850K 阵列与目标队列 [48]。临床指标路线则走轻量化：GOLD BioAge 以 Gompertz 风险函数构建线性模型，在 NHANES、UK Biobank 及 CHARLS、CLHLS、RuLAS 三个中国队列中验证其与发病、死亡风险的关联 [49]；OMICmAge 在 Mass General Brigham 约 31,000 人中开发 EMRAge，并在多组学子集生成 DNAmEMRAge 与 OMICmAge，随后在 All of Us 10,769 人、TruDiagnostic 14,213 人、Generation Scotland 18,672 人验证 [50]。这些工作共同显示外部验证队列规模从数百到近两万不等，泛化结论的强度随之不同。

中国人群与多模态框架提供了另一类证据。mCAS 队列纳入 **2,019 名 18–91 岁中国人**，整合临床、生理与分子数据，构建核心能力时钟、多模态时钟与器官相关时钟三层框架，并报告血浆蛋白时钟可代理系统生理能力、凝血因子年龄依赖积累驱动多器官衰老与炎症 [51]。以色列 10K 项目则以 1 万名 40–70 岁健康人、每 2 年随访的深度表型数据训练多系统生物年龄评分，强调男女衰老模式差异 [52]。两者都主张多模态优于单模态，但前者样本仅两千余人且未说明外部验证，后者人群局限于以色列，跨族群适用性均待检验。

影像与临床试验场景把时钟从关联推向应用与干扰识别。腹部 CT 的 CTBA 模型在 123,281 名成人中取得 IPA **29.2**，优于人口学模型的 21.7（p<0.001），但队列 92% 为白人、属回顾性设计 [53]。在 rentosertib 治疗特发性肺纤维化的 12 周 2a 期试验中，六种蛋白质组时钟（ProtAge、OrganAgemortality、OrganAgechrono、PAC、ipfP3GPT、PAOPAC）一致预测治疗组生物年龄更低，但作者承认蛋白时钟无法单独区分衰老与疾病特异效应，需借助通路分析 [54]。ClockBase Agent 则以 AI 代理整合 40 余种时钟、评估 43,602 个干预-对照比较，报告超 500 种干预显著降低生物年龄，同时指出更多干预加速而非延缓衰老、疾病状态多加速生物年龄，其局限是依赖已有时钟预测、实验验证有限 [55]。

方法学争议集中在偏差与不确定性两处。有研究指出常用 ML/AI 连续结局回归存在系统预测偏差并可传播至下游关联，甚至产生“预测脑龄越大认知越好”“表观年龄越大肾功能越好”这类方向相反的虚假关联，约束优化回归可改善校准与下游推断，但摘要未给出具体数据验证 [56]。概率框架则从预测年龄分布的均值与宽度导出 BAG 与生物年龄不确定性 BAU，在超 45 万名 UK Biobank 参与者中显示 BAU 与 BAG 弱相关、随个体分子间年龄信号不一致而增加 [57]。另有 AURORA 生成式多模态框架以降低年龄差为筛选目标预测出口腔共生菌 *Neisseria flavescens*，并在线虫中验证活菌延长寿命与健康寿命 [58]；而一项纵向多组学刻画个体化衰老轨迹的研究摘要未报告可提取的定量发现，暂无法纳入比较 [59]。

### 2.3 单细胞与空间衰老图谱

单细胞转录组与空间转录组正在把衰老研究从组织层面的平均信号推进到细胞类型与空间位置的分辨率。在免疫系统，**sc-ImmuAging** 基于 **1081** 名 **18 至 97** 岁健康欧洲人 PBMC 的约 **130 万**细胞，用 LASSO、随机森林和 PointNet 为五类免疫细胞分别建模，内部与外部验证均优于对照，并能揭示 COVID-19 感染后单核细胞与 BCG 接种后 CD8+T 细胞的年龄改变异质性 [19]。与之不同，**scAgeClock** 走的是跨组织路线，用门控多头注意力神经网络在 CZ CELLxGENE 大规模单细胞数据上训练，精度高于偏最小二乘、弹性网等基线 [20]；另有工作把单细胞转录组转成基因名序列的「细胞句子」微调预训练大语言模型，在数百万细胞上训练并报告单细胞分辨率的最先进年龄预测精度 [60]。三者都指向单细胞水平的生物年龄预测，但建模对象从特定细胞类型扩展到跨组织通用模型，训练数据与验证范围差异明显，孰优尚缺同一队列内的直接比较。

空间维度上，小鼠九组织的空间转录组显示衰老敏感斑点与组织结构熵升高共定位，免疫球蛋白表达细胞聚集是其微环境特征，**IgG** 在雌雄小鼠及人组织中积累，靶向降低 IgG 可缓解小鼠多组织衰老 [21]。人皮肤的单细胞与空间转录组研究构建了 **SenSkin™** 皮肤特异衰老基因集，发现光老化的衰老细胞负担高于时序衰老，衰老黑素细胞黑色素合成升高、衰老网状真皮成纤维细胞胶原与弹性纤维合成下降 [22]。人骨骼肌的单核 RNA+ATAC 多组学则构建了首个衰老人肌衰老细胞图谱，解析 SASP 异质性与动态，并提出 Maraviroc 作为肌少症衰老治疗候选 [23]。这些工作共同把「衰老细胞在哪、与谁互作」变成可测量的问题，但组织与物种各异，结论不能直接互推。

细胞衰老的识别本身存在方法学争议。**SenePy** 利用 **72** 个小鼠和 **64** 个人类加权单细胞转录组 signature 构建评分平台，发现其比体外来源 signature 更能重现体内衰老，且仅 **58/1540** 细胞类型组合的标志物重叠显著，说明衰老标志物高度组织细胞特异 [10]。**hUSI** 则从 **73** 项公开 RNA-seq 研究学习通用衰老特征，基准测试中在 bulk 和单细胞多种条件下优于 **31** 种方法 [18]。一个强调细胞类型特异、一个强调通用可迁移，二者取向相反；综述亦指出缺乏特异性标志物、衰老细胞稀少且异质动态是共同瓶颈 [61]。

图谱资源的覆盖范围快速扩张。小鼠乳腺的 scRNA-seq 与 snATAC-seq 比较 **3** 月龄与 **18** 月龄，显示上皮 AV/HS 减少、肌上皮增加，免疫髓系/浆细胞/记忆 T 增加、naive T 减少，成纤维细胞增加，并伴随衰老与癌症相关的表观与转录特征 [62]。**HAECA** 整合 **12** 种人体组织、超过 **37.5 万**个内皮细胞，发现静脉内皮血管生成基因表达下降及细胞外基质和机械转导相关基因广泛改变 [63]。小鼠跨器官单核图谱覆盖 **13** 个器官、**5** 个年龄段、雌雄两性，共 **93** 只小鼠 **20,317,820** 个细胞核，默认核心集含 **32** 只野生型小鼠、**11** 个器官 [https://huggingface.co/datasets/transhumanist-already-exists/pansci-mouse-aging-snrna]。这些资源多为描述性图谱，摘要层面尚未报告跨器官的统一衰老轴。

把时钟用于特定细胞类型已出现干预线索。线虫 **128** 种神经元类型的 BitAge 与 Stochastic Clock 预测年龄约 **98h 至 177h**，近 **2** 倍差异，两时钟相关 Pearson **0.65**、**P=5.5×10−17**，较老神经元更易早期退化，翻译是驱动因素，丁香酸和 vanoxerine 被验证可防止神经退化 [64]。脑衰老综述则从细胞类型中心视角总结年龄相关变化与细胞互作，并评述单细胞组学如何无偏评估年轻化干预 [65]。这类工作把「哪些细胞老得更快」与可干预靶点连接起来，但主要基于线虫，人类相关性仍需验证。

### 2.4 衰老生物学基准与基础模型

衰老生物学正从单一模态的专用时钟走向标准化基准与基础模型。**LongevityBench** 覆盖 5 个生物数据域、17 项任务，评测来自 6 个开发团队的 18 个前沿 AI 系统，结论是**没有单一模型主导所有任务**，且**组学年龄预测是最难的任务**，与模型规模无关；微调的 5 个多任务 Longevity-LLM（0.6B–9B）可匹配或超过更大的前沿系统 [8]。表观遗传方向已有 **ComputAgeBench**，以"可靠时钟应能区分健康个体与衰老加速疾病个体"为核心假设，整合 66 个公开血液 DNA 甲基化数据集、覆盖 19 种疾病，测试 13 个已发表时钟，并另建 46 个数据集用于训练新时钟 [24]。单细胞层面则建立了覆盖 5 个生物学问题、超过 250 万单细胞转录组的表征基准，评估 10 个通用单细胞基础模型、3 个衰老专用模型及传统方法，发现冻结预训练表征时 Geneformer 在时序年龄预测和年龄伪时间一致性上最佳，但 **2000 个高变基因的平均表现更高**，多个模型在三种疾病背景中捕捉到正向分子年龄偏移 [25]。这些基准的共同取向是把"能否解释异构衰老数据"变成可比较的评测问题，而非继续堆叠单模态预测器。

基础模型路线的最直接主张来自 **Longevity-LLM v0.1**：将 Qwen3-14B 在 DNA 甲基化、蛋白质组、临床生物标志物和 RNA 表达数据上经监督与强化学习微调，在 Longevity Bench 任务中排名较高，强化微调后表观年龄预测 **MAE 为 4.34 年**，超过 Horvath 多组织时钟，蛋白质组谱生成显著优于所有前沿 LLM；作者据此提出单一中等规模 LLM 可匹配或替代跨模态专用衰老时钟 [9]。这与 LongevityBench 中"小型专用模型可匹敌更大通用系统"的观察方向一致 [8]，但两处证据均属阶段性报告，前者未说明数据规模与公开情况 [9]，后者亦未列出具体局限 [8]，因此"替代专用时钟"仍是待验证的主张而非定论。综述层面的判断相对温和：深度学习与生成式 AI（CNN、RNN、GAN、LLM、扩散模型）已用于衰老时钟、合成数据生成、药物发现和多模态健康评估，但该文为叙述性综述，缺乏定量荟萃分析 [66]；多组学与多模态整合被认为在准确性、可解释性和泛化性上取得进展，然而全文不可得，具体性能与验证队列无法提取 [67]。

方法学上的争议集中在验证标准与模态覆盖。系统综述指出 AI 生物年龄预测的挑战是数据异质性、泛化性有限、可解释性不足与临床转化障碍，并强调异步衰老和多模态融合 [68]；面向干预评估的观点文章进一步要求评估做到正确、有用、全面、可解释，并考虑因果、跨学科、标准、纵向数据和已知衰老生物学，建议以 LLM 结合知识图谱与检索增强生成并开展基准测试，但未提供实验验证或定量结果 [69]。生物年龄预测器与人类数字孪生的整合框架认为表观时钟在预测生物年龄和健康表型上最准确，同时指出落地受数据整合、隐私、互操作性和纵向建模限制 [26]。值得注意的是，现有基准的覆盖面并不一致：ComputAgeBench 仅基于血液 DNA 甲基化、未覆盖其他模态 [24]，单细胞基准局限于转录组 [25]，而 LongevityBench 虽跨 5 个数据域仍发现组学年龄预测最难 [8]——"表观时钟最准确"的印象 [26] 与"组学年龄预测最难"的基准结果 [8] 分别来自综述判断与跨任务评测，二者不可直接对照，恰说明该领域尚缺统一、跨模态的验证口径。

### 2.5 类器官、扰动与 Cell Painting 衰老建模

在细胞衰老建模方向，Cell Painting 提供了一种基于显微成像、以图像型 profiling 捕获细胞状态与扰动响应的标准化路径。该方法自 **2013 年**提出，通过优化和标准化图像型 profiling，利用图像中的丰富信息识别生物样本间的相似性或差异，而非像传统高内涵筛选那样只测量少量特征 [29]。十年间其协议、特征提取、质控和批次校正持续改进，并已用于机制、毒性及多组学整合等场景；但该工作为综述，未提供统一定量基准，依赖公开数据集和计算实验技术进展 [29]。

与成像表型路线不同，另一项工作从转录组层面切入衰老重编程：构建人成纤维细胞的**可解释转录组年龄预测器**，并开展 cDNA 过表达筛选，寻找能将衰老转录组重编程为年轻状态的因子，最终鉴定出 RNA 加工与剪接因子 **SRSF1**，其诱导可产生强烈的年轻化转录特征且不丧失细胞身份，体外实验显示可恢复年轻表型 [30]。该证据的局限在于仅为人成纤维细胞体外模型，样本规模与体内验证未提及 [30]。两篇证据分属成像表型综述与转录组扰动筛选，方法学与验证层级不同，未提供可直接比较的同一研究内对照数据。

### 2.6 跨物种与跨组织衰老标志（脂质组等）

跨物种、多组织脂质组学比较显示，**脂酰链延长**是小鼠、线虫、果蝇和人类衰老的保守标志；在人类心脏病进展中也观察到类似的脂质延长，而饮食限制可缩短小鼠心脏脂质 [70]。衰老并非单一脂质分子的增减，而是表现为向长链脂质转变并伴随短链脂质耗竭的**比值性重塑** [70]。

在机制层面，该研究鉴定了脂质重塑因子 **Plb1** 参与调控上述脂质重塑过程 [70]。这一跨物种证据将脂质组变化与衰老及寿命调控联系起来，并提示饮食限制对小鼠心脏脂质的影响可作为同一研究内部的对照观察 [70]。

## 3 数据与资源

在数据资源层面，两项工作分别面向衰老标志物的统一评估与免疫衰老的多组学整合。**Biolearn** 作为开源库，针对跨人群验证缺乏标准化方法、标志物设计分散、数据集结构不一致等问题，提供整理、协调与系统评估的统一框架，并基于多公开数据集与多种衰老生物标志物开展评估，输出标准化格式并比较性能、稳健性与泛化性，其开源地址为 https://Bio-Learn.github.io [27]。该框架依赖已有公开数据，临床验证仍待推进 [27]。

**Immunosenescence Inventory** 则聚焦免疫衰老，整合单细胞转录组、bulk 转录组、表观组及 TCR/BCR 等多物种数据，提供知识 curation、多模态数据集与工具，工具涵盖免疫细胞识别与免疫时钟计算，用于评估生物年龄、预测年龄相关疾病和干预影响 [28]。该数据库以 ImmPort、InnateDB、Aging Atlas 等既有数据库为参照，开放获取，但整合依赖已有数据，未提供统一预测性能基准，单细胞层面的免疫衰老覆盖仍有限 [28]。两者差异在于：前者以统一评估框架为核心、强调跨数据集可比性，后者以多组学资源聚合与免疫时钟工具为核心；前者明确指出临床验证待推进，后者则指出缺乏统一预测性能基准，二者在“可比较的标准化评估”上均存在未解问题 [27][28]。

## 4 应用与结果

在血液与多组织样本上，DNA甲基化时钟对死亡与疾病的预测能力已得到多队列验证。四个老年人纵向队列的荟萃分析显示，**Δage每高5年全因死亡风险增加21%，校正健康、生活方式与APOE后仍增加16%**，且Δage遗传度为0.43 [71]。扩展至13个队列、13,089人（2,734例死亡）后，表观年龄与实足年龄相关系数为0.65–0.89，年龄加速与全因死亡风险升高相关，且纳入血细胞组成信息可提升预测 [72]。同一353 CpG时钟还被用于人群差异分析，发现表观年龄加速存在种族/民族与性别差异，并与冠心病及相关风险因素相关 [73]；在HIV感染者中，血液和脑组织均观察到显著的表观年龄加速 [74]。这些结果共同支持甲基化年龄差作为跨队列的死亡与疾病风险标志物，但各研究人群与设计不同，风险增幅不宜直接横向比较。

时钟与功能表型的关联则呈现方向性差异。Lothian Birth Cohort 1936在70、73、76岁三波测量中发现，表观年龄加速与70岁时的步行速度、握力、肺功能和认知能力横断面相关，**但不预测70至76岁间的功能下降** [75]。系统综述与荟萃分析整合299篇文献、1050个EAA-因素关联和53种时钟，对选定配对做随机效应合并，确认若干EAA与生理、认知、社会和环境因素存在显著汇总关联，并建立四级分类与TEAPEE数据库 [76]。前者提示时钟与功能水平相关而非与功能变化相关，后者提示关联证据广泛但研究异质性大、因果方向不明确，二者并不矛盾，但共同说明关联强度依赖表型与时钟的选择。

在干预与临床转化方向，多组学时钟开始用于评估干预效果和预后。40个月二甲双胍干预雄性食蟹猴的研究构建了多组织转录组、DNA甲基化、血浆蛋白与代谢组的猴衰老时钟，**二甲双胍显著延缓衰老指标，脑衰老约回退6年**，并保护脑结构、增强认知，部分由Nrf2激活介导 [11]。异时心脏移植的多组学分析则显示，移植心脏的生物年龄快速同化受体年龄而非保留供体年龄，且该效应仅限移植物、不影响受体全身生物年龄 [77]。此外，有研究提出干细胞衰老时钟连接生物学年龄偏差与急性髓系白血病临床结局，但所提供文本未给出具体定量结果与验证细节 [78]。这些工作把时钟从风险预测推进到干预监测与器官/疾病层面，但灵长类干预仅限雄性食蟹猴、移植研究全文未公开，向人类应用的转化仍需进一步验证。

## 5 评测、可复现性与争议

（本节暂无入库证据）

## 6 空白与趋势

当前方向最明显的结构性空白，是**「多模态」在证据层面仍主要是「多组学并列」而非「多模态对齐」**。已写正文中真正跨模态整合的工作屈指可数：StackAge 只整合蛋白与代谢物两层 [17]，ProtBAG 把蛋白时钟与表型年龄差时钟并列整合 [16]，mCAS 把临床、生理与分子数据拼成三层框架 [51]，而 MRIBAG 与 MetBAG 各自独立、彼此未做联合建模 [7][6]。**尚无工作报告在同一队列内对表观、蛋白、代谢、影像、单细胞五类模态做显式对齐、缺失模态补全与跨模态一致性约束**；现有基准也各自为政——ComputAgeBench 仅覆盖血液 DNA 甲基化 [24]，单细胞基准仅覆盖转录组 [25]，LongevityBench 虽跨 5 个数据域却仍发现组学年龄预测最难 [8]。这是最值得投入的方向之一。

第二个空白是**缺失模态与异构采样条件下的时钟推断**。真实队列中蛋白、代谢、影像极少同时齐全，但已写正文所列工作几乎都要求完整模态输入；唯一接近该问题的是概率框架从预测年龄分布导出生物年龄不确定性 BAU，并显示 BAU 随个体分子间年龄信号不一致而升高 [57]，以及迁移学习用于适配目标队列的甲基化阵列 [48]。**尚无工作报告在模态随机缺失下训练多模态时钟并给出校准的不确定性区间**，而这恰是临床落地的前置条件。

第三个趋势是**从「预测年龄」转向「区分损伤与适应、区分衰老与疾病」**。DamAge/AdaptAge 把甲基化变化拆成损伤性与适应性两支 [32]，PathwayAge 把时钟提升到通路层面以获取疾病特异性解释 [33]，rentosertib 试验则明确承认蛋白时钟无法单独区分抗衰老与抗纤维化效应、需借助通路分析 [54]。**「时钟能否归因」而非「时钟能否预测」正在成为新的评价轴**，但现有工作均未给出可跨研究复用的归因评测协议。

第四个空白是**纵向/增量学习几乎缺席**。已写正文中带纵向设计的仅 KORA 三个时间点 [41]、Lothian 三波测量 [75]、10K 每 2 年随访 [52] 与生命早期时钟位点轨迹分析 [35]，且后者已提示时钟位点发育轨迹高度非线性、超三分之一自出生即有个体差异。**尚无工作报告以增量学习方式让时钟随个体重复测量更新、并检验更新后的时钟是否改善结局预测**；Lothian 的结果——表观年龄加速与功能水平横断面相关但不预测 70 至 76 岁间功能下降 [75]——正是这一空白的直接证据。

第五个趋势是**基准与基础模型的「专用 vs 通用」之争尚未收敛**。LongevityBench 报告没有单一模型主导所有任务、小型专用 Longevity-LLM 可匹敌更大通用系统 [8]，Longevity-LLM v0.1 则主张单一中等规模 LLM 可匹配或替代跨模态专用时钟、强化微调后表观年龄 MAE 为 4.34 年 [9]；但前者未列具体局限，后者未说明数据规模与公开情况，**「替代专用时钟」仍是待验证主张**。同时，系统预测偏差可产生方向相反的虚假下游关联 [56]，说明基准设计必须把校准与下游推断纳入评测，而现有三个基准均未系统覆盖这一点 [24][25][8]。

第六个空白在**类器官/扰动体系与 cell painting 的衰老建模**。Cell Painting 自 2013 年提出、十年间协议与批次校正持续改进，但相关证据为综述、未提供统一定量基准 [29]；转录组扰动筛选已鉴定 SRSF1 可产生年轻化转录特征 [30]，但仅为人成纤维细胞体外模型、样本规模与体内验证未提及。**尚无工作把 cell painting 图像表型与分子组学时钟在同一扰动体系中联合建模、并以时钟读数作为扰动效应的定量读出**；ClockBase Agent 虽评估 43,602 个干预-对照比较，却依赖已有时钟预测、实验验证有限 [55]。此外，跨物种证据（犬表观时钟 [47]、小鼠 LivAge [46]、线虫神经元时钟 [64]）与跨物种脂质延长保守标志 [70] 提示**跨物种时钟的标定与可比性**是另一条几乎无人系统处理的空白。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 单组学衰老时钟（表观/蛋白/转录） | **成熟** | 表观时钟的方法内核已高度收敛：Horvath 2013 多组织甲基化时钟 [1] 与 PhenoAge [31] 奠定了「甲基化年龄 + 死亡率/疾病终点校准」的范式，后续工作多为换模态、换队列的增量验证（如蛋白组时钟 [4]）。因果富集时钟 [32] 属于少数方法层面的再推进，说明单组学时钟本身已进入「增量为主」阶段。雷达样本中该节 n=28、median citations 9，高被引集中在 2013–2018 的老锚点，也符合成熟期特征。 |
| 2.2 多模态整合与跨队列泛化 | **朝阳** | 近两年集中爆发且方法未收敛：血浆蛋白组连接脑—免疫衰老与 healthspan [15]、MRI 多器官时钟 [7]、表型组性别特异动态 [52] 各自用不同模态、不同对齐策略，尚无统一评测口径；AI agent 从分子库筛干预 [55] 代表另一条「多模态+扰动」路线。雷达样本该节 n=16、recent_share **0.92**、CNS share **0.56**，是典型朝阳信号（注意：这是雷达样本统计，非领域发文量）。 |
| 2.3 单细胞与空间衰老图谱 | **朝阳** | 图谱类工作密集出现且各有侧重：空间转录组揭示免疫球蛋白相关衰老 [21]、细胞类型特异衰老景观 [10]、单细胞免疫衰老时钟揭示个体异质性 [19]、健康乳腺单细胞衰老图谱 [62]。四篇分别解决「空间定位」「细胞类型分辨率」「个体异质性时钟」「组织特异图谱」，说明问题被拆成多个未收敛的子问题，方法仍在快速分化。 |
| 2.4 衰老生物学基准与基础模型 | **萌芽** | 已有基准尝试但规模小、引用低：ComputAgeBench 表观时钟基准 [24]、AI 干预评估的验证要求 [69]，加上数字孪生视角 [26] 与生成式 AI 综述 [66]。这些是「提出评测框架/呼吁规范」的探索性工作，尚无被广泛采用的统一 benchmark 或衰老基础模型；雷达样本该节 n=9、median citations **0**，符合萌芽期。 |
| 2.5 类器官、扰动与 Cell Painting 衰老建模 | **证据不足** | 仅 2 篇且均非「类器官衰老建模」本身：Cell Painting 十年综述 [29] 是成像表型方法学总览，转录组重编程筛选鉴定 SRSF1 [30] 是扰动筛选。二者说明「扰动+高内涵表型」工具链存在，但没有证据表明类器官衰老建模已形成细分方向，故不判阶段。 |
| 2.6 跨物种与跨组织衰老标志（脂质组等） | **证据不足** | 仅 1 篇：长链脂质标记衰老并约束寿命 [70]。单篇不足以判断阶段。 |
| 3 数据与资源 | **萌芽** | 统一的老化生物标志物 curation/评估框架 [27] 与免疫衰老多组学数据库 [28] 是资源层基础设施的早期搭建，尚未成为社区默认标准；雷达样本该节 n=2、recent_share 1.0，量小但方向明确。 |
| 4 应用与结果 | **成熟** | 甲基化年龄预测全因死亡 [71]、meta 分析预测死亡时间 [72]、种族/性别与冠心病关联 [73]、HIV 加速衰老 [74] 构成一套已被反复复现的「时钟→临床终点」应用范式，属增量应用而非方法突破。 |
| 5 评测、可复现性与争议 | **证据不足** | 雷达样本该节 n=0，无证据可引。 |

**整体判断**：这个方向整体处于**「单组学时钟成熟、多模态与单细胞图谱朝阳、基准/基础模型萌芽」的三层叠加态**，不是单一阶段。真正的窗口期在**多模态整合的方法层**（模态对齐、缺失模态、跨队列校正）与**单细胞/空间衰老时钟**，雷达样本中这两节 recent_share 分别为 **0.92** 和 **0.75**、CNS share **0.56** 和 **0.57**，说明近两年新工作密集但方法尚未收敛——这正是方法学博后可切入的缝隙，估计窗口 **12–24 个月**，之后会像表观时钟一样被标准化 benchmark 收编。最大不确定性有三：一是**评测口径未定**（ComputAgeBench [24] 与 curation 框架 [27] 尚未成为共识，谁先做出被采纳的 benchmark 谁定义赛道）；二是**跨队列泛化的真实增益存疑**，多模态时钟多数仍在小队列内部验证，外部泛化证据薄弱；三是**类器官/扰动体系几乎空白**（2.5 节仅 2 篇且非直接证据），意味着这块要么是蓝海要么是坑，取决于是否有可用的扰动-表型配对数据。

**接下来怎么做**：

1. **做「缺失模态下的多模态衰老时钟」方法学**：用公共多组学队列（甲基化+转录+蛋白+临床表型）构造模态随机缺失场景，提出对齐+插补+不确定性估计的统一框架，产出可复现 benchmark 与开源代码。现在做是因为多模态工作各自为战、无人系统处理缺失模态（[15]、[7] 均为完整模态内部验证），而评测框架刚起步 [27]，先发可占口径。**这是与他「多模态建模」技能最直接匹配的切入点。**

2. **把单细胞衰老时钟做成「跨组织可迁移」版本**：以现有单细胞免疫衰老时钟 [19] 与细胞类型特异衰老景观 [10] 为基线，用迁移学习/域适应做跨组织、跨队列校准，产出可迁移的细胞类型级衰老评分。现在做是因为图谱数据刚放出、方法仍停留在单队列（[62] 亦为单组织），迁移问题未被解决。

3. **用公共数据先做「类器官+多组学衰老建模」的 demo，低成本探路**：以 Cell Painting 成像表型方法学 [29] 与扰动筛选范式 [30] 为模板，在公开扰动-表型数据上构建「年轻化/衰老」表型评分并做多组学锚定，验证类器官体系能否支撑衰老时钟。现在做是因为该节证据不足（仅 2 篇），先做 demo 可用极低成本判断是蓝海还是坑，且直接对接他的类器官+多组学合作项目。

4. **抢做衰老 AI 基准的一个子赛道而非全赛道**：不做通用 LongevityBench，只做「多模态衰老时钟的跨队列泛化评测」子基准，复用 curation 框架 [27] 的评估思路与 ComputAgeBench [24] 的表观时钟评测设计，产出数据集+leaderboard。现在做是因为基准层处于萌芽（median citations **0**），单点切入成本低、被引用潜力高。

5. **把因果/扰动视角嵌入时钟，做「可干预的衰老评分」**：借鉴因果富集时钟 [32] 的解耦思路与 AI agent 筛干预 [55]，构建对扰动敏感、能区分「损伤 vs 适应」的评分，产出可对接类器官扰动实验的读出指标。现在做是因为现有临床终点型时钟（[71]、[72]）只预测不指导干预，而干预读出正是类器官合作项目的刚需。

## 参考文献

1. DNA methylation age of human tissues and cell types. Genome Biology 2013. https://doi.org/10.1186/gb-2013-14-10-r115
2. An unbiased comparison of 14 epigenetic clocks in relation to 174 incident disease outcomes.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66106-y
3. Cross-tissue comparison of epigenetic aging clocks in humans.. Aging cell 2025. https://doi.org/10.1111/acel.14451
4. Proteomic aging clock predicts mortality and risk of common age-related diseases in diverse populations. Nature Medicine 2023. https://doi.org/10.1038/s41591-024-03164-7
5. Transcriptomic age prediction using mixture-of-experts models reveals tissue-specific aging signatures in large-scale human RNA-sequencing data. medRxiv 2025. https://doi.org/10.1101/2025.06.28.25330474
6. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
7. MRI-based multi-organ clocks for healthy aging and disease assessment.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03999-8
8. An open benchmark and language models for AI in aging biology.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.026
9. The End of Aging Clocks: Training Foundation Models to Reason in Aging and Longevity. bioRxiv 2026. https://doi.org/10.64898/2026.03.28.714980
10. Unveiling the cell-type-specific landscape of cellular senescence through single-cell transcriptomics using SenePy.. Nature communications 2025. https://doi.org/10.1038/s41467-025-57047-7
11. Metformin decelerates aging clock in male monkeys.. Cell 2024. https://doi.org/10.1016/j.cell.2024.08.021
12. LinAge2: providing actionable insights and benchmarking with epigenetic clocks.. npj aging 2025. https://doi.org/10.1038/s41514-025-00221-4
13. Epigenetic clocks and programmatic aging.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102546
14. Enhancing the performance and interpretability of epigenetic clocks.. Nucleic acids research 2026. https://doi.org/10.1093/nar/gkag661
15. Plasma proteomics links brain and immune system aging with healthspan and longevity.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03798-1
16. Refining the generation, interpretation and application of multi-organ, multi-omics biological aging clocks.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00928-9
17. StackAge: an ensemble-based clock for precise quantification of biological age using multi-omics data.. Briefings in bioinformatics 2026. https://doi.org/10.1093/bib/bbag271
18. A transcriptome-based human universal senescence index (hUSI) robustly predicts cellular senescence under various conditions.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00886-2
19. Single-cell immune aging clocks reveal inter-individual heterogeneity during infection and vaccination.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00819-z
20. scAgeClock: a single-cell transcriptome-based human aging clock model using gated multi-head attention neural networks.. npj aging 2026. https://doi.org/10.1038/s41514-026-00379-5
21. Spatial transcriptomic landscape unveils immunoglobin-associated senescence as a hallmark of aging.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.019
22. Mapping epidermal and dermal cellular senescence in human skin aging.. Aging cell 2024. https://doi.org/10.1111/acel.14358
23. Multiomics and cellular senescence profiling of aging human skeletal muscle uncovers Maraviroc as a senotherapeutic approach for sarcopenia.. Nature communications 2025. https://doi.org/10.1038/s41467-025-61403-y
24. ComputAgeBench: Epigenetic Aging Clocks Benchmark. bioRxiv 2025. https://doi.org/10.1145/3711896.3737382
25. Benchmarking single-cell foundation models for aging biology.  . https://doi.org/10.64898/2026.09.21.753191
26. From ageing clocks to human digital twins in personalising healthcare through biological age analysis.. NPJ digital medicine 2025. https://doi.org/10.1038/s41746-025-01911-9
27. A unified framework for systematic curation and evaluation of aging biomarkers.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00987-y
28. Immunosenescence Inventory-a multi-omics database for immune aging research.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1102
29. Cell Painting: a decade of discovery and innovation in cellular imaging.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02528-8
30. Transcriptomic reprogramming screen identifies SRSF1 as a regulator of aging.. Nature aging . https://doi.org/10.1038/s43587-026-01234-8
31. An epigenetic biomarker of aging for lifespan and healthspan. bioRxiv 2018. https://doi.org/10.18632/aging.101414
32. Causality-Enriched Epigenetic Age Uncouples Damage and Adaptation. bioRxiv 2023. https://doi.org/10.1038/s43587-023-00557-0
33. Decoding disease-specific ageing mechanisms through pathway-level epigenetic clock: insights from multi-cohort validation.. EBioMedicine 2025. https://doi.org/10.1016/j.ebiom.2025.105829
34. Responsiveness of epigenetic aging biomarkers to longevity interventions in humans.. Nature medicine 2026. https://doi.org/10.1038/s41591-026-04562-9
35. Characterising developmental dynamics of adult epigenetic clock sites.. EBioMedicine 2024. https://doi.org/10.1016/j.ebiom.2024.105425
36. Proteomic aging clock (PAC) predicts age‐related outcomes in middle‐aged and older adults. Aging Cell 2024. https://doi.org/10.1111/acel.14195
37. Organ-specific proteomic aging clocks predict disease and longevity across diverse populations.. Nature aging 2025. https://doi.org/10.1038/s43587-025-01016-8
38. A proteomic signature of healthspan.. Proceedings of the National Academy of Sciences of the United States of America 2025. https://doi.org/10.1073/pnas.2414086122
39. An Extracellular Matrix Aging Clock Based on Circulating Matrisome Proteins Predicts Biological Aging and Disease.. Aging cell 2026. https://doi.org/10.1111/acel.70474
40. Construction and Validation of Plasma Protein-Based Musculoskeletal Biological Age and Genetic and Environmental Risk Profiles.. Aging cell 2026. https://doi.org/10.1111/acel.70636
41. Intraindividual longitudinal changes of the proteome reveal dynamic markers of biological aging.  . https://doi.org/10.64898/2026.10.01.755909
42. Pasta, a Versatile Transcriptomic Clock, Maps the Chemical and Genetic Determinants of Aging and Rejuvenation. bioRxiv 2025. https://doi.org/10.1002/advs.76740
43. Guided multi-agent AI invents highly accurate, uncertainty-aware transcriptomic aging clocks. bioRxiv 2025. https://doi.org/10.1101/2025.09.08.674588
44. DeepQA: A Unified Transcriptome-Based Aging Clock Using Deep Neural Networks.. Aging cell 2025. https://doi.org/10.1111/acel.14471
45. A Novel Metabolomic Aging Clock Predicting Health Outcomes and Its Genetic and Modifiable Factors. Advancement of science 2024. https://doi.org/10.1002/advs.202406670
46. LivAge: An Online Aging Clock for Murine Transcriptomic Age Estimation.. Aging cell 2026. https://doi.org/10.1111/acel.70677
47. Epigenetic aging and transposon dysregulation reflect size-related lifespan compression in dogs.. Science (New York, N.Y.) . https://doi.org/10.1126/science.aeb2986
48. BRIDGING THE GAP: ENHANCING THE GENERALIZABILITY OF EPIGENETIC CLOCKS THROUGH TRANSFER LEARNING.. The annals of applied statistics 2026. https://doi.org/10.1214/26-aoas2136
49. Gompertz Law-Based Biological Age (GOLD BioAge): A Simple and Practical Measurement of Biological Ageing to Capture Morbidity and Mortality Risks.. Advanced science (Weinheim, Baden-Wurttemberg, Germany) 2025. https://doi.org/10.1002/advs.202501765
50. OMICmAge quantifies biological age by integrating multi-omics with electronic medical records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01073-7
51. Multimodal clocks of human aging.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.025
52. Phenome-wide associations of human aging uncover sex-specific dynamics.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00734-9
53. Biological age model using explainable automated CT-based cardiometabolic biomarkers for phenotypic prediction of longevity.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56741-w
54. Integration of proteomic aging clocks in a phase 2a clinical trial supports simultaneous geroprotective assessment.. Nature Biotechnology 2026. https://doi.org/10.1038/s41587-026-03286-y
55. Autonomous AI Agents Discover Aging Interventions from Millions of Molecular Profiles. bioRxiv 2025. https://doi.org/10.1101/2023.02.28.530532
56. Trustworthy ML/AI for Aging Clocks: Preventing Systematic Prediction Bias in Biological Age Estimation. bioRxiv 2026. https://doi.org/10.64898/2026.05.27.728155
57. Uncertainty redefines biological age.  . https://doi.org/10.64898/2026.09.26.26364091
58. Multi-modality profiling identifies Neisseria flavescens as a central geroprotective oral commensal in humans.. Nature aging . https://doi.org/10.1038/s43587-026-01220-0
59. Longitudinal multiomics reveals personalized aging trajectories.. Nature aging . https://doi.org/10.1038/s43587-026-01248-2
60. Universal Single-Cell Transcriptomic Aging Clock powered by LLMs reveals targets to slow cellular aging. Innovation in aging 2025. https://doi.org/10.1093/geroni/igaf122.4305
61. Advancing biological understanding of cellular senescence with computational multiomics.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02314-y
62. Comprehensive single-cell aging atlas of healthy mammary tissues reveals shared epigenomic and transcriptomic signatures of aging and cancer.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00751-8
63. Uncovering the transcriptional hallmarks of endothelial cell aging via integrated single-cell analysis.. Nature aging . https://doi.org/10.1038/s43587-026-01247-3
64. Aging clocks delineate neuron types vulnerable or resilient to neurodegeneration and identify neuroprotective interventions.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01067-5
65. Brain aging and rejuvenation at single-cell resolution.. Neuron 2025. https://doi.org/10.1016/j.neuron.2024.12.007
66. Deep learning and generative artificial intelligence in aging research and healthy longevity medicine.. Aging 2025. https://doi.org/10.18632/aging.206190
67. The Evolving Landscape of Clinical Aging Clocks: From Epigenetic to Multi-Omics Integration.. Aging cell 2026. https://doi.org/10.1111/acel.70579
68. Artificial intelligence approaches in biological age prediction: current status and challenges.. British journal of biomedical science 2026. https://doi.org/10.3389/bjbs.2026.16141
69. Validation Requirements for AI-based Intervention-Evaluation in Aging and Longevity Research and Practice. Ageing Research Reviews 2024. https://doi.org/10.1016/j.arr.2024.102617
70. Longer lipids mark aging and constrain lifespan.. Nature aging . https://doi.org/10.1038/s43587-026-01223-x
71. DNA methylation age of blood predicts all-cause mortality in later life. Genome Biology 2015. https://doi.org/10.1186/s13059-015-0584-6
72. DNA methylation-based measures of biological age: meta-analysis predicting time to death. Aging 2016. https://doi.org/10.18632/aging.101020
73. An epigenetic clock analysis of race/ethnicity, sex, and coronary heart disease. Genome Biology 2016. https://doi.org/10.1186/s13059-016-1030-0
74. HIV-1 Infection Accelerates Age According to the Epigenetic Clock. Journal of Infectious Diseases 2015. https://doi.org/10.1093/infdis/jiv277
75. The epigenetic clock is correlated with physical and cognitive fitness in the Lothian Birth Cohort 1936. International Journal of Epidemiology 2015. https://doi.org/10.1093/ije/dyu277
76. Breaking new ground on human health and well-being with epigenetic clocks: A systematic review and meta-analysis of epigenetic age acceleration associations.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102552
77. Transplanted hearts assimilate the recipient’s biological age. bioRxiv 2026. https://doi.org/10.64898/2026.09.15.751836
78. A stem cell aging clock links biological age deviation to clinical outcome in acute myeloid leukemia. bioRxiv 2026. https://doi.org/10.64898/2026.02.12.703707
79. A blood-based epigenetic clock for intrinsic capacity predicts mortality and is associated with clinical, immunological and lifestyle factors.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00883-5
80. Biological Versus Technical Reliability of Epigenetic Clocks and Implications for Disease Prognosis and Intervention Response.. Aging cell 2026. https://doi.org/10.1111/acel.70635
81. [dataset] transhumanist-already-exists/pansci-mouse-aging-snrna.  . https://huggingface.co/datasets/transhumanist-already-exists/pansci-mouse-aging-snrna
