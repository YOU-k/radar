# 多模态衰老时钟与生物年龄 · 方向背景报告

证据 80 篇 · 覆盖度 0.60 · 第 9 轮 · 更新 2026-11-01

## 本次变更

- 新增 [33] Uncovering the transcriptional hallmarks of endothelial cell aging via integrated single-cell analysis.

## 摘要（TL;DR）

- Horvath 多组织时钟整合 82 个 Illumina 27K/450K 数据集、7844 个非癌样本，从 21,369 个共有 CpG 中选出 353 个 CpG，在多数组织中预测误差约 3.6 年 [1]。
- 基于 Generation Scotland 18,859 人的研究无偏比较 14 种时钟与 174 种新发疾病，完全校正模型下 13 种时钟与 57 种疾病共 176 个 Bonferroni 显著关联，GrimAge v2 和 DunedinPACE 各 72 个 [2]。
- TranslAGE 平台评估 18 种 DNAm 标志物，发现多数时钟技术重现性好，但生物学可靠性仅为低至中等，调整免疫组成后进一步下降，且技术重现性不能预测生物学可靠性 [3]。
- 跨组织比较测试五种组织 284 份样本（83 人，9-70 岁），发现口腔与血液组织的表观年龄平均差近 30 年，多数血液时钟与口腔组织相关性低，Skin and Blood clock 一致性最高 [4]。
- UKB 中基于 2,897 个血浆蛋白、45,441 人构建的时钟经 Boruta 筛选出 204 个蛋白，与实际年龄 Pearson r=0.94，年龄差与 27 个衰老表型、全因死亡和 26 种年龄相关疾病关联 [5]。
- 基于 ARCHS4 的混合专家模型在 56,877 样本（2-114 岁）上 MAE=7.58 年，肺和脑预测最佳、肝较差，但百岁老人误差达 ±40 年 [6]。
- 基于 274,247 名 UKB 参与者的 107 种非衍生代谢物构建的 5 个 MetBAG，在独立测试集中与年龄的 Pearson r 仅为 0.25<r<0.42，平均绝对误差约 6 年 [7]。
- 有研究指出常用 ML/AI 连续结局回归存在系统预测偏差，可扭曲甚至逆转下游关联，例如产生“预测脑龄越大认知越好”或“表观年龄越大肾功能越好”的虚假关联 [8]。
- LongevityBench 构建了覆盖 5 个生物数据域的 17 项任务，评测来自 6 个开发团队的 18 个前沿 AI 系统，结论是无单一模型主导所有任务，且组学年龄预测是最难的任务，与模型规模无关 [9]。
- Lothian Birth Cohort 1936 在 70 岁（n=920）、73 岁（n=299）、76 岁（n=273）三波测量中，表观年龄加速与 70 岁步行速度、握力、肺功能、认知的横断面相关成立，但不预测 70 至 76 岁间的功能下降 [10]。

## 1 背景与定义

表观遗传时钟的演化脉络已相对清晰：从 Horvath 以实际年龄为训练目标的第一代跨组织时钟 [1]，到以表型年龄为目标的 PhenoAge [11]，再到以内在能力为终点的 IC clock [12]，训练目标的迁移本身构成了这一支的核心演进逻辑。但**训练目标改变并未同步解决生物学基础问题**：孟德尔随机化分析显示现有时钟位点与年龄相关差异甲基化均未在因果位点富集 [13]，而另一侧的分析又表明时钟精度并非主要由转录因子结合动态驱动 [14]。PathwayAge 以通路级甲基化替代单 CpG 建模，是对"可解释性"这一诉求的直接回应 [15]。**方向边界由此可界定为：衰老时钟研究不止于年龄预测精度，而必须同时回答"预测的是什么"与"为何可预测"两个问题**；仅报告相关系数或 MAE 而不涉及机制或可靠性验证的工作，正在被基准类研究边缘化 [2] [16]。

多模态整合的演化呈现"单组学延长线"特征：蛋白组时钟先在 UKB 大规模人群中确立可预测性 [5] [17]，随后被拆分为器官特异时钟 [18] [19]，再与代谢组、影像组学并置 [7] [20]。**这一路径的核心问题不是"能否整合"，而是"整合的边界由谁定义"**：同为 UKB 平台，器官划分与蛋白数目在不同工作中并不一致 [21] [19]；代谢组时钟的年龄相关性明显低于蛋白组与影像组学 [7]，说明各模态在"年龄可预测性"上的量级差异是整合前必须正视的前提，而非可被融合算法抹平的噪声。跨队列泛化则进一步暴露了策略分歧：迁移学习 [22]、轻量临床模型 [23] 与多组学电子病历模型 [24] 各自成立，但验证队列的人群构成互不重叠，**尚无一项工作在同一外部队列上同时比较这三类策略**。

单细胞与空间组学把衰老时钟推到细胞类型分辨率，同时把"衰老标志物是否通用"这一旧争议重新点燃。sc-ImmuAging 强调细胞类型特异建模与免疫场景验证 [25]，scAgeClock 追求跨组织通用性但组织覆盖仍偏血液 [26]；SenePy 发现仅 58/1540 细胞类型组合的标志物重叠显著 [27]，hUSI 则主张可从 73 项研究学到通用衰老特征 [28]。**两者取向相反却各有验证支撑，说明"特异 vs 通用"并非二选一，而是取决于读出层级与组织范围**。空间图谱一侧，小鼠九组织 [29]、人皮肤 [30]、小鼠乳腺 [31]、人骨骼肌 [32] 与人内皮 [33] 已积累组织特异发现，但**跨物种、跨组织的统一空间衰老坐标尚未建立**，现有图谱多为单一物种或单一组织，人类因果性与泛化仍待验证 [29] [34]。

基准与基础模型的出现，标志着这一方向开始从"各自造钟"转向"共同出题"。LongevityBench 以 17 项任务、5 个数据域评测 18 个前沿系统，得出**无单一模型主导、组学年龄预测最难**的结论 [9]；Longevity-LLM v0.1 以 14B 模型微调在表观年龄预测上报告 MAE 4.34 年 [35]；单细胞基准则显示冻结表征下 Geneformer 在时序年龄预测最佳，但 2000 个高变基因的平均表现更高 [36]。ComputAgeBench 以"区分健康与衰老加速疾病"为核心假设整合 66 个数据集、19 种疾病 [37]。**这些基准的共同贡献是把"衰老时钟好不好"从单研究自评转为可比较的任务集，但其共同局限是任务本身仍以年龄或疾病标签为锚，尚未纳入干预响应或纵向变化速率作为评测维度**。与此同时，预测偏差 [8] 与生物年龄不确定性 [38] 两项方法学工作提示：**多模态整合带来的信息增益，可能被未校正的统计偏差或未报告的不确定性抵消**，而现有各时钟普遍只报告点估计，跨研究可比性因此受限。

扰动与类器官体系是这一方向中证据最稀疏、但定义上最关键的环节。人成纤维细胞转录组年龄预测器驱动的 cDNA 过表达筛选鉴定出 SRSF1，可产生年轻化转录特征而不丧失细胞身份 [39]；Cell Painting 作为成像表型读出已历经十年协议与质控改进 [40]；ClockBase Agent 以 40 余种时钟评估 43,602 个干预-对照比较 [41]；AURORA 把时钟用于生成式干预筛选并以线虫验证 [42]。**这些工作分处转录组、成像、计算筛选与模式生物四条互不衔接的路径，证据中并无同一研究内的直接对照** [39] [40]。类器官衰老建模在已入库证据中尚无专门的方法学或基准工作，**"在类器官体系中建立可复现的衰老读出并与其他模态对齐"仍是明确空白**；同样，跨物种保守标志物（如脂酰链延长 [43]）如何转化为可计算的跨物种衰老时钟，现有证据仅提供机制入口而未提供建模方案。

数据资源层面，Biolearn 提供统一整理、协调与评估框架 [44]，Immunosenescence Inventory 汇聚免疫衰老多模态数据并工具化免疫时钟 [45]，二者定位互补但**均依赖既有公开数据、均未建立统一预测性能基准** [44] [45]。这与基准类工作形成对照：后者已给出可比较的任务与数字 [9] [37]，而多组学时钟的定量性能与临床验证仍是证据缺口，综述层面亦仅停留在框架呼吁 [46] [47]。**综合来看，本方向的边界可概括为三层**：底层是模态与数据资源（表观、蛋白、代谢、影像、单细胞/空间、类器官），中层是建模与整合方法（训练目标选择、器官划分、跨队列校正、缺失模态、不确定性量化），顶层是评测与应用（基准任务、干预筛选、临床试验终点）。**当前证据在底层与顶层均已形成可比较的公共产品，中层的方法学共识——尤其是多器官边界标准化、跨策略同队列比较、以及把不确定性纳入常规报告——是最明显的空白**。

## 2 方法学


### 2.1 单组学衰老时钟（表观 / 蛋白 / 转录）

表观遗传时钟是单组学衰老时钟中发展最成熟的一支。Horvath 多组织时钟整合 82 个 Illumina 27K/450K 数据集、7844 个非癌样本，用弹性网络从 21,369 个共有 CpG 中选出 **353 个 CpG**，在多数组织中预测误差约 **3.6 年**，并显示早衰症不符合正常衰老、iPS 重编程可将时钟重置为 0 [1]。该工作确立了跨组织 DNAm 年龄预测的可行性，但其训练数据异质、组织覆盖仍有限 [1]。后续综述亦以 353 CpG 的 Horvath 时钟为参照，讨论其与发育程序（Hox、polycomb 等基因）的关联 [48]。

第二代时钟转向以表型而非实际年龄为训练目标。DNAm PhenoAge 用包含临床表型年龄的复合指标替代实际年龄，通过两步流程筛选 CpG，在全因死亡、癌症、健康寿命、身体功能和阿尔茨海默病预测上优于第一代标志物 [11]。但该模型基于全血开发，摘要未给出样本规模与误差指标 [11]。更晚的 IC clock 则把目标换成内在能力，用 INSPIRE-T 队列 933 人 EPIC 甲基化数据经弹性网筛选 **91 个 CpG**，在 FHS 中验证，DNAm IC 与临床 IC 相关 **0.61**，并可预测死亡 [12]。

时钟数量激增后，横向比较成为独立问题。一项基于 Generation Scotland **18,859 人**的研究无偏比较 14 种时钟与 174 种新发疾病，完全校正模型下 13 种时钟与 57 种疾病共 **176 个** Bonferroni 显著关联，GrimAge v2 和 DunedinPACE 各 **72 个**，而第一代时钟关联有限 [2]。LinAge2 的评测给出另一组内部对照：其 20 年全因死亡预测 AUC=**0.8684**，优于 PhenoAge Clinical 的 0.8479 和 ChronAge 的 0.8288；20 年死亡 AUC=**0.8440**，优于 PhenoAge DNAm 的 0.7859 和 GrimAge2 的 0.8233 [16]。两项研究都支持"以生存/功能为训练目标的时钟优于以实际年龄为目标者"，但比较的时钟集合与结局不同，数字不可直接跨研究对比 [2] [16]。

对时钟生物学基础的追问带来了分歧。一项工作通过表观全基因组孟德尔随机化识别可能因果影响衰老性状的 CpG，指出现有时钟与年龄相关差异甲基化均未在这些位点富集，并据此构建区分损伤的 DamAge 与适应的 AdaptAge [13]。另一项分析则发现多数时钟 CpG 不与转录因子结合位点重叠，说明时钟精度并非主要由 TF 结合动态驱动；但仅用弱相关非 TFBS CpG 建模即可达 MdAE=**3.77 年**，优于 Horvath1 的 5.95 年、接近 PhenoAge 的 3.79 年，且需移除 **88007 个** CpG 后误差才降至随机水平 [14]。PathwayAge 走另一条路，用 GO/KEGG 通路级甲基化替代单 CpG 建模，以提升机制可解释性 [15]。

可靠性与跨组织可比性是表观时钟转化应用的两个薄弱环节。TranslAGE 平台评估 18 种 DNAm 标志物，发现多数时钟技术重现性好，但生物学可靠性仅为低至中等，调整免疫组成后进一步下降，且技术重现性不能预测生物学可靠性 [3]。跨组织比较测试五种组织 284 份样本（83 人，9-70 岁），发现口腔与血液组织的表观年龄平均差近 **30 年**，多数血液时钟与口腔组织相关性低，Skin and Blood clock 一致性最高 [4]。此外，对成人时钟位点的发育追踪显示其轨迹高度异质且非线性，超过三分之一位点自出生即存在个体差异，高于非时钟位点 [49]。在干预响应方面，TranslAGE 整合 **51 项**人类干预研究、统一计算 16 种时钟与 94 种额外 DNAm 标志物，发现不同干预与时钟的响应差异显著 [50]。

蛋白质组时钟以血浆蛋白为底，规模与验证设计是其突出特点。UKB 中基于 **2,897 个**血浆蛋白、**45,441 人**构建的时钟经 Boruta 筛选出 **204 个**蛋白，与实际年龄 Pearson r=**0.94**，年龄差与 27 个衰老表型、全因死亡和 26 种年龄相关疾病关联，并在 CKB（3,977 人）和 FinnGen（1,990 人）中独立验证 [5]。PAC 用 UKB 53,021 人、2923 个 Olink 蛋白以 LASSO 训练，随访超 10 年，年龄偏差与全因死亡及多种年龄相关疾病显著关联 [17]。器官特异时钟进一步细分：UKB 43,616 人建模的整体与十个器官时钟在中国（3,977 人）和美国（800 人）队列中跨队列 r 分别达 **0.98** 和 **0.93**，脑衰老与死亡关联最强 [18]。

蛋白时钟的目标也在分化。HPS 不以年龄而以健康寿命为终点，用 53,018 人、2,920 种蛋白建模，在 43,119 名基线健康者中 **12,427 人（28.8%）** 发生健康寿命终点事件 [51]。ECM 时钟仅用 **14 个**血浆蛋白，报告 ECM 蛋白随龄呈 U 型轨迹、最低点约 40-50 岁，但作者自己指出 Robbins 队列最老仅 66 岁、U 型轨迹较弱 [52]。MSKAge/MSKAgeMort 基于 21,070 名 UKB 参与者的 39 个肌肉骨骼相关蛋白池，MSKAge 相关 r 女性=0.62、男性=0.56，MSKAgeMort 相关 r 女性=0.93、男性=0.88 [53]。纵向数据方面，KORA 队列用 9105 样本、4100 人、25-88 岁的 LC-MS 血浆蛋白组构建时钟，发现个体内血脂异常和肾功能受损与年龄加速增加相关 [54]。

转录组时钟的争议集中在跨平台泛化与极端年龄误差。Pasta 采用"年龄偏移"学习框架，报告优于 MultiTIMER 和 tAge，可区分衰老、静息与干细胞状态，并指出 p53 相关基因贡献显著 [55]。DeepQA 用混合专家与 Hinge-MAE 损失，在 3060 样本、31 数据集上训练，声称在健康与非健康受试者上均优于现有方法 [56]。基于 ARCHS4 的混合专家模型在 56,877 样本（2-114 岁）上 MAE=**7.58 年**，肺和脑预测最佳、肝较差，但百岁老人误差达 **±40 年** [6]。K-Dense 多智能体系统在 57,584 样本、28 组织上报告 R²=**0.854**、MAE=**4.26 年**，并提供校准置信区间以标记过渡期和极端年龄 [57]。同为转录组时钟，MAE 从 7.58 年到 4.26 年的差距反映的是数据集、组织构成与评估方式的不同，而非可直接比较的性能高低 [6] [57]。物种与组织受限的时钟亦有报告：小鼠 LivAge 基于肝脏 RNA-seq，在早衰模型中捕捉年龄加速，并可评估 Snell Dwarf、Ames Dwarf、GHR 缺陷及热量限制等干预 [58]。

跨组学整合已出现在单组学时钟的延长线上。StackAge 整合 UKB 30,376 人的 2,923 蛋白与 251 代谢物，与实际年龄 Pearson r≈**0.93**，对 2 型糖尿病、阿尔茨海默病和慢性肾脏病的 AUC 超过 **0.90**，但作者指出未整合表观遗传层、以横断面基线为主 [59]。代谢组一侧，MetaboAgeMort 用 UKB **239,291 人**血浆代谢组、选 **185 个**死亡相关标志物，以 LASSO Cox 与 Gompertz 回归预测 10 年全因死亡 [60]。非人模型的证据也在积累：犬表观时钟基于 894 只犬的 1640 份甲基化组，可预测死亡率、生命早期表观遗传衰老最快，大体型和雄性犬分子衰老加速，体型相关变化集中于转座子元件 [61]。这些工作共同显示，单组学时钟的分野已不在"能否预测年龄"，而在训练目标（年龄、死亡、健康寿命、器官功能）、组织与平台覆盖、以及可靠性验证是否跟得上预测精度。

### 2.2 多模态整合与跨队列泛化

多模态整合的核心动机，是单一模态的年龄预测虽能高度拟合实际年龄，却未必捕捉到器官特异的衰老信号。UK Biobank 中基于 **2,916 个血浆蛋白**、覆盖 44,498 人的工作为 11 个器官分别训练 LASSO 年龄模型，其中脑、动脉和整体年龄对传统年龄的预测 r² 达 **0.97**，但作者同时指出器官富集蛋白的定义与蛋白平台本身构成局限 [21]。同一队列的另一项分析用 2,448 个血浆蛋白、43,498 人构建 11 个 ProtBAG，并与 9 个多器官表型年龄差时钟整合，报告跨器官特征可提升系统性疾病类别和全因死亡预测，同时强调年龄偏倚校正与器官蛋白特异性是方法学前提 [19]。两项工作共享 UKB 平台却采用不同的蛋白数与器官划分，说明“多器官”的边界尚未标准化。

代谢组与影像组学沿同一框架扩展，但预测精度差异明显。基于 274,247 名 UKB 参与者的 107 种非衍生代谢物构建的 5 个 MetBAG，在独立测试集中与年龄的 Pearson r 仅为 **0.25<r<0.42**，平均绝对误差约 6 年，作者将其归因于代谢组的动态性及饮食、微生物等环境扰动 [7]。相比之下，MULTI Consortium 的 313,645 人数据构建的 7 个 MRIBAG 在留出测试中 r 为 **0.23–0.77**、MAE 约 5 年，并关联 2,923 种血浆蛋白与 327 种代谢物；但腹部 MRI 特征共线性导致泛化较差，脑模型在外部队列存在域偏移 [20]。这些数字来自不同模态与不同测试划分，不能直接比较优劣，只能说明各模态在“年龄可预测性”上的量级差异。

跨队列泛化是更直接的检验场。表观遗传时钟方面，Horvath 与 PedBE 时钟在墨西哥儿童青少年队列（523 份血样）中预测准确性下降，基于 Kriging 与 DNN 特征适配的迁移学习被用于缩小目标数据差距，但样本量与年龄范围有限 [22]。GOLD BioAge 走的是另一条路线：以 Gompertz 风险函数构建轻量线性模型，在 UKB、NHANES 及 CHARLS、CLHLS、RuLAS 三个中国队列中验证其与发病、死亡风险的关联，作者自陈其依赖常规临床标志物、可能遗漏分子层面机制 [23]。OMICmAge 则在 Mass General Brigham 约 31,000 人中开发 EMRAge，并在多组学子集中生成 DNAmEMRAge 与 OMICmAge，随后在 All of Us 10,769 人、TruDiagnostic 14,213 人、Generation Scotland 18,672 人中进行验证 [24]。三者分别代表迁移学习、轻量临床模型与多组学电子病历模型三种泛化策略，验证队列的规模与人群构成各不相同。

中国人群的多模态框架提供了另一种组织方式。mCAS 队列纳入 2,019 名 18–91 岁中国人，整合临床、生理与分子数据，构建核心能力时钟、多模态时钟与器官相关时钟三层结构，并报告血浆蛋白时钟可代理系统生理能力、凝血因子年龄依赖积累驱动多器官衰老与炎症 [62]。该研究的外部验证与跨族群适用性未在摘要中说明，与前述以 UKB 为主体的工作形成人群覆盖上的互补而非互证。以色列 10K 项目则以 1 万名 40–70 岁健康人、每 2 年随访的深度表型设计，揭示男女衰老模式差异及高 BA 与年龄相关疾病患病率的关联，同样受限于单一人群来源 [63]。

方法学层面的争议集中在“预测偏差”与“不确定性”两个概念上。有研究指出常用 ML/AI 连续结局回归存在系统预测偏差，可扭曲甚至逆转下游关联，例如产生“预测脑龄越大认知越好”或“表观年龄越大肾功能越好”的虚假关联，并提出约束优化回归框架改善校准 [8]。另一项工作则从预测年龄分布的均值与宽度推导 BAG 与生物年龄不确定性 BAU，在超过 45 万名 UKB 参与者中报告 BAU 与 BAG 弱相关、并随个体分子间年龄信号不一致而增加 [38]。二者共同提示：多模态整合带来的信息增益，可能被未校正的统计偏差或未被报告的不确定性所抵消，而现有各时钟报告的多为点估计与相关系数，跨研究可比性因此受限。

在应用端，多模态时钟已开始进入干预评估与假设生成。一项特发性肺纤维化 12 周 2a 期试验比较 ProtAge、OrganAgemortality、OrganAgechrono、PAC、ipfP3GPT 与 PAOPAC 六种蛋白质组时钟，均一致预测治疗组生物年龄更低，但作者承认蛋白质组时钟无法单独区分衰老与疾病特异效应，需借助通路分析间接解释 [64]。ClockBase Agent 整合 40 余种衰老时钟、评估 43,602 个干预-对照比较，报告发现超 500 种干预显著降低生物年龄，并指出更多干预加速而非延缓衰老、疾病状态多加速生物年龄，其局限在于依赖已有时钟预测、实验验证有限 [41]。AURORA 生成式多模态框架则把时钟用于干预计算筛选，预测 Neisseria flavescens 为顶级候选，并以线虫实验验证活菌可延长寿命和健康寿命 [42]。这些工作把时钟从“测量工具”推向“筛选工具”，但单一疾病、短期试验与计算预测的性质，决定了其结论仍需独立验证。至于纵向多组学刻画个体化衰老轨迹的方向，现有摘要未提供可提取的方法、规模与结果，暂无法与其他证据对照 [65]。

### 2.3 单细胞与空间衰老图谱

单细胞转录组已被用于构建细胞类型特异的衰老时钟。**sc-ImmuAging** 基于 **1081** 名 **18 至 97** 岁健康欧洲人 PBMC 的约 **130 万**细胞，用 LASSO、随机森林和 PointNet 为五类免疫细胞分别建模，内外验证表现优于对照，并揭示 COVID-19 感染后单核细胞与 BCG 接种后 CD8+T 细胞的年龄改变异质性 [25]。与之不同，**scAgeClock** 采用门控多头注意力神经网络，利用 CZ CELLxGENE 中超过 **40** 种人体组织、**400** 种细胞类型的大规模单细胞转录组训练，精度高于偏最小二乘、弹性网等基线 [26]；另有工作把单细胞转录组表示为基因名序列的「细胞句子」微调预训练大语言模型，在数百万细胞上训练实现单细胞分辨率年龄预测，并提名调控后降低转录年龄的候选靶点 [66]。这些时钟的差异主要在建模策略与数据覆盖：前者强调细胞类型特异与免疫场景验证，后两者追求跨组织通用性，但 scAgeClock 的组织覆盖仍偏血液、外部验证有限 [26]。

空间维度上，小鼠九组织的空间转录组显示衰老敏感斑点与组织结构熵升高共定位，免疫球蛋白表达细胞聚集是其微环境特征，**IgG** 在雄性与雌性小鼠的衰老组织及人组织中积累，靶向降低 IgG 可缓解小鼠多组织衰老 [29]。人皮肤的单细胞与空间转录组研究构建了 **SenSkin™** 皮肤特异衰老基因集，发现光老化的衰老细胞负担高于时序衰老，衰老黑素细胞黑色素合成升高、衰老网状真皮成纤维细胞胶原和弹性纤维合成下降 [30]。小鼠乳腺的 scRNA-seq 与 snATAC-seq 整合图谱则显示年老上皮细胞在代谢、促炎和癌症相关基因上发生表观与转录改变， stromal 细胞下调成纤维标志物、上调衰老与癌症相关成纤维标志物 [31]。人骨骼肌的单核 RNA+ATAC 多组学构建了首个衰老人肌衰老细胞图谱，解析 SASP 异质性与动态，并提出 Maraviroc 作为肌少症候选干预 [32]；人内皮细胞图谱 **HAECA** 整合 **12** 种人体组织、超 **37.5 万**个内皮细胞，发现静脉内皮血管生成基因表达下降及细胞外基质和机械转导相关基因广泛改变 [33]。

细胞衰老的识别方法本身存在分歧。**SenePy** 用 **72** 个小鼠和 **64** 个人类加权单细胞转录组 signature 构建评分平台，发现其比体外来源 signature 更能重现体内衰老，Cdkn2a 等随龄增加（FDR p=0.01），但仅 **58/1540** 细胞类型组合的标志物重叠显著，说明衰老标志物高度组织细胞特异 [27]。**hUSI** 则从 **73** 项公开 RNA-seq 研究学习通用衰老特征，在 bulk 和单细胞多种条件下优于 **31** 种方法 [28]。两者取向相反——一个强调细胞类型特异、一个强调通用性——恰好对应综述所指出的缺乏特异标志物、衰老细胞稀少且异质动态的核心困难 [67]。

将衰老时钟推到单细胞类型分辨率后，同一组织内不同细胞类型的生物年龄可以显著分离。在线虫 **128** 种神经元类型中，BitAge 与 Stochastic Clock 预测年龄从约 **98h** 到 **177h**，近 **2** 倍差异，两时钟相关 Pearson **0.65**（P=5.5×10−17）；较老神经元更易早期退化，翻译是驱动因素，丁香酸和 vanoxerine 被验证可防止神经退化 [34]。脑衰老的单细胞组学综述则从细胞类型中心视角总结年龄相关变化与细胞互作，并评述如何无偏评估年轻化干预 [68]。需要注意，上述图谱与时钟多基于小鼠或特定人群、特定组织，人类因果性与跨物种泛化仍需验证 [29][34]。

### 2.4 衰老生物学基准与基础模型

衰老生物学正从单一模态的专用时钟走向标准化基准与基础模型。**LongevityBench** 构建了覆盖 5 个生物数据域的 17 项任务，评测来自 6 个开发团队的 18 个前沿 AI 系统，结论是**无单一模型主导所有任务**，且**组学年龄预测是最难的任务**，与模型规模无关；微调的 0.6B–9B 多任务 Longevity-LLM 可匹配或超过更大的前沿系统 [9]。与之呼应，Longevity-LLM v0.1 将 Qwen3-14B 在 DNA 甲基化、蛋白质组、临床生物标志物和 RNA 表达上微调，强化微调后表观年龄预测 **MAE 为 4.34 年**，超过 Horvath 多组织时钟，蛋白质组谱生成显著优于所有前沿 LLM [35]。单细胞层面则建立了覆盖 5 个生物学问题、**超过 250 万单细胞转录组**的基准，评估 10 个通用单细胞基础模型、3 个衰老专用模型及传统方法；冻结预训练表征时 Geneformer 在时序年龄预测和年龄伪时间一致性上最佳，但 **2000 个高变基因的平均表现更高**，多个模型在三种疾病背景中捕捉到正向分子年龄偏移 [36]。这些结果共同显示：专用小模型与通用大模型各有胜场，基准任务本身（尤其组学年龄预测）仍是瓶颈。

表观时钟的标准化评测提供了另一条线索。**ComputAgeBench** 以“可靠时钟应能区分健康个体与衰老加速疾病个体”为核心假设，整合 **66 个公开血液 DNA 甲基化数据集、覆盖 19 种疾病**，测试 13 个已发表表观遗传时钟模型，并另建 46 个数据集用于训练新时钟 [37]。其局限在于仅基于血液 DNA 甲基化、未覆盖其他模态，全文也未给出具体模型性能数值 [37]。综述层面，表观时钟被认为在预测生物年龄和健康表型上最准确，多组学与多模态整合则被视为提升准确性、可解释性和泛化性的方向 [69][70]。但后者全文不可得，具体数据、验证队列和定量性能无法提取 [70]；前者也指出数字孪生落地受数据整合、隐私、互操作性和纵向建模挑战限制 [69]。

方法学综述与验证要求类工作则更多停留在框架层面。系统综述覆盖生物标志物选择、特征工程、模型开发、偏倚校正和性能评估，强调异步衰老与多模态融合，指出的挑战包括数据异质性、泛化性有限、可解释性不足和临床转化障碍 [46]。另一篇综述梳理 2016–2024 年间 **125 篇同行评审研究**，总结 CNN、RNN、GAN、LLM 和扩散模型在衰老时钟、合成数据生成、药物发现和多模态健康评估中的应用，但属叙述性综述、缺乏定量荟萃分析 [47]。针对干预评估，有观点文章主张 AI 评估应正确、有用、全面、可解释，并考虑因果、跨学科、标准、纵向数据和已知衰老生物学，建议 LLM 结合知识图谱与检索增强生成并开展基准测试，但未提供具体实验验证或定量结果 [71]。总体而言，基准与基础模型已给出可比较的任务与数字，而多组学时钟的定量性能与临床验证仍是证据缺口。

### 2.5 类器官、扰动与 Cell Painting 衰老建模

在细胞衰老建模的扰动筛选路径上，一项研究构建了**人成纤维细胞的可解释转录组年龄预测器**，并以此作为读出开展cDNA过表达筛选，寻找能把衰老转录组重编程为年轻状态的因子；筛选鉴定出RNA加工与剪接因子**SRSF1**，其诱导可产生强烈的年轻化转录特征且不丧失细胞身份，体外实验显示可恢复年轻表型[id:10.1038/s43587-026-01234-8]。该工作以预测器预测的年龄作为筛选基准，但仅限体外成纤维细胞模型，样本规模与体内验证均未提及[id:10.1038/s43587-026-01234-8]。

成像一侧，Cell Painting作为2013年提出的显微细胞标记assay，旨在捕获细胞状态并优化图像型profiling，十年来协议、特征提取、质控和批次校正持续改进，已用于机制、毒性及多组学整合等应用[id:10.1038/s41592-024-02528-8]。不过该文为综述，未提供统一定量基准，其结论依赖公开数据集与计算实验技术进展[id:10.1038/s41592-024-02528-8]；与上述转录组筛选相比，两者分处成像表型与转录组读出，证据中并无同一研究内的直接对照。

### 2.6 跨物种与跨组织衰老标志（脂质组等）

跨物种、多组织的脂质组学比较显示，**脂酰链延长**是小鼠、线虫、果蝇和人类衰老的保守标志；在人类心脏病进展中也观察到类似的脂质延长，而饮食限制可缩短小鼠心脏脂质 [43]。该研究将衰老的脂质变化描述为一种比值性重塑，即向长链脂质转变并伴随短链脂质耗竭，而非单一脂质种类的孤立变化 [43]。

在机制层面，该工作鉴定了脂质重塑因子 **Plb1** 参与调控上述脂质重塑过程 [43]。这一结果把跨物种保守的脂质延长表型与具体的调控因子联系起来，为脂质组作为跨物种、跨组织衰老标志提供了可检验的分子入口 [43]。

## 3 数据与资源

在数据资源层面，现有工作主要沿两条路径推进：一是面向衰老标志物统一整理与评估的通用框架，二是聚焦免疫衰老的多组学数据库。**Biolearn** 作为开源库，针对跨人群验证缺乏标准化方法、标志物设计分散、数据集结构不一致等问题，提供统一的整理、协调与系统评估框架，并据此对多种衰老生物标志物进行综合评估，覆盖多公开数据集，输出可复现的评估流程 [44]。其可用性以开源形式提供（https://Bio-Learn.github.io），但依赖已有公开数据，临床验证仍待推进 [44]。

另一类资源面向特定子问题——免疫衰老。**Immunosenescence Inventory** 整合单细胞转录组、bulk 转录组、表观组及 TCR/BCR 等多物种数据，提供知识 curation、多模态数据集与工具，工具涵盖免疫细胞识别与**免疫时钟**计算，用于评估生物年龄、预测年龄相关疾病及干预影响，并以 ImmPort、InnateDB、Aging Atlas 等既有数据库为参照 [45]。该库开放获取，但整合依赖已有数据，未提供统一预测性能基准，单细胞层面的免疫衰老覆盖仍有限 [45]。两项工作定位不同：前者强调跨数据集、跨人群的标志物评估与泛化性比较，后者强调免疫相关多模态数据的汇聚与免疫时钟工具化；二者均受限于对既有公开数据的依赖，且尚未建立统一的预测性能基准，这一空白也是当前数据资源建设的共同争议点 [44][45]。

## 4 应用与结果

在血液与多组织样本上，DNA甲基化时钟对死亡与疾病的预测已积累较多证据。四个老年纵向队列的荟萃分析显示，**Δage每高5年全因死亡风险增加21%，校正健康、生活方式与APOE后仍增加16%**，且Δage遗传度为0.43 [72]。随后扩展至**13个队列13,089人、2,734例死亡**的荟萃分析比较了Horvath 353 CpG与Hannum 71 CpG时钟，表观年龄与实足年龄相关系数为0.65–0.89，年龄加速与全因死亡风险升高相关，并报告血液细胞组成信息可提升预测 [73]。同一353 CpG时钟用于种族/民族、性别与冠心病分析时，发现表观年龄加速存在种族和性别差异，并与冠心病及相关风险因素相关，但该工作以横断面为主、组织来源异质 [74]。HIV感染研究同样使用353 CpG时钟，在11个甲基化数据集的血液与脑组织中均观察到感染者表观年龄加速显著增加，局限为样本量有限与横断面设计 [75]。

时钟与功能表型的关系则出现不一致。Lothian Birth Cohort 1936在70岁（n=920）、73岁（n=299）、76岁（n=273）三波测量中，表观年龄加速与70岁步行速度、握力、肺功能、认知的横断面相关成立，**但不预测70至76岁间的功能下降** [10]。这一"相关而不预测变化"的结果，与死亡预测类研究强调的纵向预后价值形成对照，提示时钟捕捉的可能是当前状态而非变化速率。系统层面，一项系统综述纳入**299篇文献、1050个EAA-因素关联、53种甲基化时钟**，对选定配对做随机效应荟萃分析，报告若干EAA与生理、认知、社会和环境因素存在显著汇总关联，并建立四级分类与TEAPEE数据库；其局限是研究异质性大、部分关联证据有限、因果方向不明确 [76]。

干预与器官层面的应用开始出现，但证据成熟度差异明显。40个月二甲双胍干预雄性食蟹猴的研究整合多组织转录组、DNA甲基化、血浆蛋白与代谢组构建猴衰老时钟，报告**脑衰老约回退6年**、脑结构保护与认知增强，部分由Nrf2激活介导，局限为仅雄性食蟹猴、人类转化待验证 [77]。异时心脏移植的多组学分析（小鼠与患者）报告移植心脏的DNA甲基化与基因表达生物年龄快速同化受体年龄，且**仅限移植物、不影响受体全身生物年龄**，但全文未公开、样本规模与组学细节未在摘要说明 [78]。急性髓系白血病方面，仅有标题级信息提出干细胞衰老时钟连接生物学年龄偏差与临床结局，无摘要与具体数值，无法评估其验证强度 [79]。总体看，死亡预测证据相对充分，功能下降预测与临床预后应用仍受设计（多为横断面、老年或单一人群队列）与数据公开度限制。

## 5 评测、可复现性与争议

（本节暂无入库证据）

## 6 空白与趋势

在单组学时钟已高度成熟的背景下，**多模态整合的真正瓶颈不在"能否拼接模态"，而在模态间年龄信号的可比性与对齐方式**。现有工作多以"同一队列、同一平台、分别建模再整合"为路径：UKB 蛋白组 11 器官时钟与 9 个多器官表型年龄差的整合报告跨器官特征可提升系统性疾病与死亡预测，但作者把年龄偏倚校正与器官蛋白特异性列为前提 [19]；StackAge 整合蛋白与代谢物后 r≈0.93，却自陈未纳入表观遗传层、以横断面基线为主 [59]。**证据清单中没有一项工作给出跨模态年龄差的统一标定方案**——MetBAG 的 r 仅 0.25–0.42 [7]，MRIBAG 的 r 为 0.23–0.77 [20]，蛋白时钟可达 0.94 [5]，这些量级差异被各研究归因于模态本身，但**缺乏同一批样本上的头对头标定**，使"多模态增益"难以与"模态可预测性差异"分离。

纵向与增量学习是另一处明显空白。已写正文中唯一涉及纵向设计的是 KORA 队列的蛋白组时钟（9105 样本、4100 人）[54] 与以色列 10K 的两年随访表型组 [63]，二者均未报告增量学习或个体轨迹更新的建模方法；Lothian 队列的"相关而不预测变化"结果 [10] 恰恰说明**横断面训练的时钟未必携带速率信息**。清单中没有任何研究比较"单时点时钟"与"纵向增量时钟"在同一队列的预测增益，也没有工作处理随访间隔不等、模态缺失随时间变化的现实情形。**这是从"生物年龄估计"走向"衰老速率监测"必须补上的一环，目前无直接证据。**

缺失模态与跨队列校正虽有零星尝试，但方法学深度不足。表观时钟一侧有 Kriging 与 DNN 特征适配的迁移学习用于儿童队列 [22]，蛋白时钟一侧有中国与美国外部队列的跨队列 r 报告 [18]，OMICmAge 则在多组学子集与三个外部队列中验证 [24]。但这些工作**均未系统评测"某模态缺失时时钟如何降级运行"**，也未报告缺失比例与性能衰减的对应关系；跨队列校正多停留在外部验证层面，而非显式的域适应或批次不变表征学习。清单中唯一直接讨论统计可靠性的是预测偏差约束优化 [8] 与 BAU 不确定性量化 [38]，**二者均针对单模态时钟开发，尚未扩展到多模态融合场景**。

基准与基础模型的进展反而凸显了组学年龄预测这一薄弱点。LongevityBench 覆盖 5 个数据域 17 项任务、评测 18 个系统，结论是**无单一模型主导、组学年龄预测最难且与模型规模无关** [9]；单细胞基准在超过 250 万细胞上发现冻结表征时 Geneformer 最佳，但**2000 个高变基因的平均表现更高** [36]；Longevity-LLM 的 MAE 4.34 年虽超过 Horvath 多组织时钟 [35]，但对比基准仍是第一代时钟而非当前最强的生存训练型时钟。**这意味着"基础模型优于专用时钟"的结论尚缺公平对照**，而 ComputAgeBench 仅覆盖血液 DNA 甲基化、未给具体性能数值 [37]，Biolearn 提供统一评估框架但依赖既有公开数据、临床验证待推进 [44]。**跨模态、跨任务、含缺失模态的统一基准仍是空缺。**

类器官与扰动体系中的衰老建模则处于更早期。人成纤维细胞可解释转录组年龄预测器驱动的 cDNA 过表达筛选鉴定出 SRSF1，可产生年轻化转录特征且不丧失细胞身份，但**仅限体外成纤维细胞、样本规模与体内验证未提及** [39]；Cell Painting 作为成像表型读出已用于机制与多组学整合，但该文为综述、无统一定量基准 [40]。**清单中没有一项工作把 Cell Painting 或类器官体系与多模态衰老时钟直接耦合**，也没有在扰动筛选中同时使用成像、转录组与甲基化多读出并比较其年轻化判定一致性。ClockBase Agent 虽评估 43,602 个干预-对照比较 [41]，但其依赖已有时钟预测、实验验证有限，**扰动体系内的"时钟读出—机制验证"闭环尚未建立**。

综合来看，本方向的趋势可归纳为三条：**训练目标从实际年龄转向死亡/健康寿命/器官功能**（PhenoAge、HPS、GOLD BioAge、LinAge2 等 [11][51][23][16]）；**分辨率从整体人下沉到器官、细胞类型乃至单细胞**（多器官蛋白时钟、sc-ImmuAging、scAgeClock、BitAge [18][25][26][34]）；**评价从单研究自报转向公开基准与基础模型**（LongevityBench、ComputAgeBench、Biolearn [9][37][44]）。与之对应的空白同样清晰：**跨模态年龄差的统一标定、纵向增量时钟、缺失模态下的降级运行、含缺失模态的跨任务基准、以及类器官/扰动体系内的多读出闭环**，在现有证据中均无直接工作填补。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 单组学衰老时钟（表观/蛋白/转录） | 成熟 | 表观时钟已有 Horvath 2013 与 PhenoAge 2018 两代奠基工作，方法收敛、系数公开，后续多为增量验证与队列应用 [1][11]；蛋白组时钟 [5] 与因果富集表观年龄 [13] 属于同一范式内的扩展，而非方法重构。雷达样本中该节 n=28、median_citations=9，说明大量工作已进入常规应用层。 |
| 2.2 多模态整合与跨队列泛化 | 朝阳 | 该节证据全部落在 2024–2026（recent_share=0.92），CNS 占比 0.56，说明近两年集中爆发但尚未收敛：血浆蛋白组连接脑-免疫-健康寿命 [21]、MRI 多器官时钟 [20]、表型组性别特异动态 [63] 各自用不同模态与对齐策略，尚无统一的多模态融合与缺失模态处理标准。 |
| 2.3 单细胞与空间衰老图谱 | 朝阳 | 空间转录组揭示免疫球蛋白相关衰老 [29] 与单细胞免疫衰老时钟刻画个体异质性 [25] 均为 2024–2025 新工作，方法（细胞类型特异时钟 vs 空间图谱）尚未统一；乳腺单细胞衰老图谱 [31] 与细胞类型特异衰老景观 [27] 进一步显示图谱类工作仍在快速扩张、以资源产出为主。 |
| 2.4 衰老生物学基准与基础模型 | 萌芽 | 仅有零散基准与规范讨论：ComputAgeBench 提出表观时钟基准 [37]，AI 干预评估的验证要求 [71] 属方法学倡议；该节 median_citations=0、CNS 占比 0.11，尚无被广泛采用的衰老基础模型或统一 LongevityBench 类基准，属早期探索。 |
| 2.5 类器官、扰动与 Cell Painting 衰老建模 | 证据不足 | 雷达仅收录 2 篇：Cell Painting 十年综述 [40] 与转录组重编程筛选识别 SRSF1 [39]，前者是成像方法综述、后者是扰动筛选，均非「类器官衰老时钟建模」的直接证据，不足以判定阶段。 |
| 2.6 跨物种与跨组织衰老标志（脂质组等） | 证据不足 | 仅 1 篇脂质标志工作 [43]，无法构成阶段判断。 |
| 3 数据与资源 | 萌芽 | 出现衰老标志物统一 curation/评估框架 [44] 与免疫衰老多组学数据库 [45]，均为 2025 年单点资源建设，尚未形成社区标准或被广泛复用。 |
| 4 应用与结果 | 成熟 | 表观年龄预测全因死亡 [72]、meta 分析预测死亡时间 [73]、种族/性别/冠心病关联 [74] 构成已确立的临床关联证据链，属成熟应用层；该节 recent_share 仅 0.22，新工作稀少。 |
| 5 评测、可复现性与争议 | 证据不足 | 雷达该节 n=0，无证据可引。 |

**整体判断**：这个方向整体处于**「单组学时钟已成熟、多模态整合正朝阳」的叠加态**。表观/蛋白时钟的方法与系数已收敛（[1][11][5]），继续做单模态时钟属增量；真正的窗口在**多模态整合与跨队列泛化**——雷达样本中该节 **recent_share=0.92、CNS 占比 0.56**，但方法未收敛（蛋白组、MRI 多器官、表型组各走各路），**窗口期估计 12–24 个月**，之后会快速进入基准化与增量阶段。最大不确定性是**评测与可复现性基础设施缺位**：评测节 n=0，基准类工作仅 ComputAgeBench [37] 等零星尝试，意味着「谁定义多模态衰老时钟的评测标准」尚未定局——这既是风险（易被后来基准否定）也是机会（可抢占标准位）。其次是**缺失模态与跨队列校正**没有公认方案，直接决定模型能否泛化到公开队列。

**接下来怎么做**：

1. **以「缺失模态 + 跨队列校正」为方法主线，做多模态融合时钟**。切入点：用公开多组学队列（表观+转录+蛋白+临床表型）构造模态缺失场景，方法上做模态对齐与缺失鲁棒训练，产出可复用的融合框架 + 跨队列泛化 benchmark。为什么现在做：该节近两年爆发但方法未收敛 [21][20]，且表型组性别特异动态提示队列异质性必须显式建模 [63]。

2. **把单细胞/空间衰老图谱作为「细胞类型特异时钟」的监督来源，而非再产出一张图谱**。切入点：复用公开单细胞衰老图谱 [31][27]，提取细胞类型特异的衰老特征，训练可在 bulk 多组学上迁移的时钟。为什么现在做：单细胞免疫衰老时钟已证明个体异质性可建模 [25]，空间图谱提供了组织区位信息 [29]，但「单细胞→bulk 迁移」尚少人做，正好发挥他的单细胞+多模态建模优势。

3. **抢占评测标准位：做一个多模态衰老时钟的开放 benchmark**。切入点：整合现有公开系数与数据资源 [44][45]，定义缺失模态、跨队列、纵向增量三类评测任务，对标并扩展 ComputAgeBench [37]。为什么现在做：评测节雷达 n=0、基准工作 citation 极低（median_citations=0），标准真空期正是低成本高影响力的切入时点，且与他的算法背景高度匹配。

4. **与合作项目结合：在类器官+多组学体系里做扰动-衰老建模的 pilot**。切入点：用类器官多组学 + 扰动筛选数据（参照 SRSF1 重编程筛选 [39]），把 Cell Painting 形态学读出 [40] 与转录组衰老评分对齐，验证「扰动→衰老速率变化」可否被时钟量化。为什么现在做：该细分在雷达中仅 2 篇、**证据不足**，属明显空白；但需注意这是高风险探索，建议作为合作项目的附加模块而非主线，先出小规模 demo 再决定投入。

5. **用公共数据先做 demo 验证可行性，再决定是否加注**。切入点：选 1–2 个公开多组学队列，复现蛋白组时钟 [5] 与 MRI 多器官时钟 [20] 的基线，量化跨队列性能衰减幅度。为什么现在做：这是判断「多模态整合窗口是否值得全力投入」的最低成本实验，也能为建议 1、3 提供前期数据；若衰减过大，说明评测/校正方向（建议 3）优先级应高于新模型。

## 参考文献

1. DNA methylation age of human tissues and cell types. Genome Biology 2013. https://doi.org/10.1186/gb-2013-14-10-r115
2. An unbiased comparison of 14 epigenetic clocks in relation to 174 incident disease outcomes.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66106-y
3. Biological Versus Technical Reliability of Epigenetic Clocks and Implications for Disease Prognosis and Intervention Response.. Aging cell 2026. https://doi.org/10.1111/acel.70635
4. Cross-tissue comparison of epigenetic aging clocks in humans.. Aging cell 2025. https://doi.org/10.1111/acel.14451
5. Proteomic aging clock predicts mortality and risk of common age-related diseases in diverse populations. Nature Medicine 2023. https://doi.org/10.1038/s41591-024-03164-7
6. Transcriptomic age prediction using mixture-of-experts models reveals tissue-specific aging signatures in large-scale human RNA-sequencing data. medRxiv 2025. https://doi.org/10.1101/2025.06.28.25330474
7. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
8. Trustworthy ML/AI for Aging Clocks: Preventing Systematic Prediction Bias in Biological Age Estimation. bioRxiv 2026. https://doi.org/10.64898/2026.05.27.728155
9. An open benchmark and language models for AI in aging biology.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.026
10. The epigenetic clock is correlated with physical and cognitive fitness in the Lothian Birth Cohort 1936. International Journal of Epidemiology 2015. https://doi.org/10.1093/ije/dyu277
11. An epigenetic biomarker of aging for lifespan and healthspan. bioRxiv 2018. https://doi.org/10.18632/aging.101414
12. A blood-based epigenetic clock for intrinsic capacity predicts mortality and is associated with clinical, immunological and lifestyle factors.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00883-5
13. Causality-Enriched Epigenetic Age Uncouples Damage and Adaptation. bioRxiv 2023. https://doi.org/10.1038/s43587-023-00557-0
14. Enhancing the performance and interpretability of epigenetic clocks.. Nucleic acids research 2026. https://doi.org/10.1093/nar/gkag661
15. Decoding disease-specific ageing mechanisms through pathway-level epigenetic clock: insights from multi-cohort validation.. EBioMedicine 2025. https://doi.org/10.1016/j.ebiom.2025.105829
16. LinAge2: providing actionable insights and benchmarking with epigenetic clocks.. npj aging 2025. https://doi.org/10.1038/s41514-025-00221-4
17. Proteomic aging clock (PAC) predicts age‐related outcomes in middle‐aged and older adults. Aging Cell 2024. https://doi.org/10.1111/acel.14195
18. Organ-specific proteomic aging clocks predict disease and longevity across diverse populations.. Nature aging 2025. https://doi.org/10.1038/s43587-025-01016-8
19. Refining the generation, interpretation and application of multi-organ, multi-omics biological aging clocks.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00928-9
20. MRI-based multi-organ clocks for healthy aging and disease assessment.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03999-8
21. Plasma proteomics links brain and immune system aging with healthspan and longevity.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03798-1
22. BRIDGING THE GAP: ENHANCING THE GENERALIZABILITY OF EPIGENETIC CLOCKS THROUGH TRANSFER LEARNING.. The annals of applied statistics 2026. https://doi.org/10.1214/26-aoas2136
23. Gompertz Law-Based Biological Age (GOLD BioAge): A Simple and Practical Measurement of Biological Ageing to Capture Morbidity and Mortality Risks.. Advanced science (Weinheim, Baden-Wurttemberg, Germany) 2025. https://doi.org/10.1002/advs.202501765
24. OMICmAge quantifies biological age by integrating multi-omics with electronic medical records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01073-7
25. Single-cell immune aging clocks reveal inter-individual heterogeneity during infection and vaccination.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00819-z
26. scAgeClock: a single-cell transcriptome-based human aging clock model using gated multi-head attention neural networks.. npj aging 2026. https://doi.org/10.1038/s41514-026-00379-5
27. Unveiling the cell-type-specific landscape of cellular senescence through single-cell transcriptomics using SenePy.. Nature communications 2025. https://doi.org/10.1038/s41467-025-57047-7
28. A transcriptome-based human universal senescence index (hUSI) robustly predicts cellular senescence under various conditions.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00886-2
29. Spatial transcriptomic landscape unveils immunoglobin-associated senescence as a hallmark of aging.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.019
30. Mapping epidermal and dermal cellular senescence in human skin aging.. Aging cell 2024. https://doi.org/10.1111/acel.14358
31. Comprehensive single-cell aging atlas of healthy mammary tissues reveals shared epigenomic and transcriptomic signatures of aging and cancer.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00751-8
32. Multiomics and cellular senescence profiling of aging human skeletal muscle uncovers Maraviroc as a senotherapeutic approach for sarcopenia.. Nature communications 2025. https://doi.org/10.1038/s41467-025-61403-y
33. Uncovering the transcriptional hallmarks of endothelial cell aging via integrated single-cell analysis.. Nature aging . https://doi.org/10.1038/s43587-026-01247-3
34. Aging clocks delineate neuron types vulnerable or resilient to neurodegeneration and identify neuroprotective interventions.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01067-5
35. The End of Aging Clocks: Training Foundation Models to Reason in Aging and Longevity. bioRxiv 2026. https://doi.org/10.64898/2026.03.28.714980
36. Benchmarking single-cell foundation models for aging biology.  . https://doi.org/10.64898/2026.09.21.753191
37. ComputAgeBench: Epigenetic Aging Clocks Benchmark. bioRxiv 2025. https://doi.org/10.1145/3711896.3737382
38. Uncertainty redefines biological age.  . https://doi.org/10.64898/2026.09.26.26364091
39. Transcriptomic reprogramming screen identifies SRSF1 as a regulator of aging.. Nature aging . https://doi.org/10.1038/s43587-026-01234-8
40. Cell Painting: a decade of discovery and innovation in cellular imaging.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02528-8
41. Autonomous AI Agents Discover Aging Interventions from Millions of Molecular Profiles. bioRxiv 2025. https://doi.org/10.1101/2023.02.28.530532
42. Multi-modality profiling identifies Neisseria flavescens as a central geroprotective oral commensal in humans.. Nature aging . https://doi.org/10.1038/s43587-026-01220-0
43. Longer lipids mark aging and constrain lifespan.. Nature aging . https://doi.org/10.1038/s43587-026-01223-x
44. A unified framework for systematic curation and evaluation of aging biomarkers.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00987-y
45. Immunosenescence Inventory-a multi-omics database for immune aging research.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1102
46. Artificial intelligence approaches in biological age prediction: current status and challenges.. British journal of biomedical science 2026. https://doi.org/10.3389/bjbs.2026.16141
47. Deep learning and generative artificial intelligence in aging research and healthy longevity medicine.. Aging 2025. https://doi.org/10.18632/aging.206190
48. Epigenetic clocks and programmatic aging.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102546
49. Characterising developmental dynamics of adult epigenetic clock sites.. EBioMedicine 2024. https://doi.org/10.1016/j.ebiom.2024.105425
50. Responsiveness of epigenetic aging biomarkers to longevity interventions in humans.. Nature medicine 2026. https://doi.org/10.1038/s41591-026-04562-9
51. A proteomic signature of healthspan.. Proceedings of the National Academy of Sciences of the United States of America 2025. https://doi.org/10.1073/pnas.2414086122
52. An Extracellular Matrix Aging Clock Based on Circulating Matrisome Proteins Predicts Biological Aging and Disease.. Aging cell 2026. https://doi.org/10.1111/acel.70474
53. Construction and Validation of Plasma Protein-Based Musculoskeletal Biological Age and Genetic and Environmental Risk Profiles.. Aging cell 2026. https://doi.org/10.1111/acel.70636
54. Intraindividual longitudinal changes of the proteome reveal dynamic markers of biological aging.  . https://doi.org/10.64898/2026.10.01.755909
55. Pasta, a Versatile Transcriptomic Clock, Maps the Chemical and Genetic Determinants of Aging and Rejuvenation. bioRxiv 2025. https://doi.org/10.1002/advs.76740
56. DeepQA: A Unified Transcriptome-Based Aging Clock Using Deep Neural Networks.. Aging cell 2025. https://doi.org/10.1111/acel.14471
57. Guided multi-agent AI invents highly accurate, uncertainty-aware transcriptomic aging clocks. bioRxiv 2025. https://doi.org/10.1101/2025.09.08.674588
58. LivAge: An Online Aging Clock for Murine Transcriptomic Age Estimation.. Aging cell 2026. https://doi.org/10.1111/acel.70677
59. StackAge: an ensemble-based clock for precise quantification of biological age using multi-omics data.. Briefings in bioinformatics 2026. https://doi.org/10.1093/bib/bbag271
60. A Novel Metabolomic Aging Clock Predicting Health Outcomes and Its Genetic and Modifiable Factors. Advancement of science 2024. https://doi.org/10.1002/advs.202406670
61. Epigenetic aging and transposon dysregulation reflect size-related lifespan compression in dogs.. Science (New York, N.Y.) . https://doi.org/10.1126/science.aeb2986
62. Multimodal clocks of human aging.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.025
63. Phenome-wide associations of human aging uncover sex-specific dynamics.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00734-9
64. Integration of proteomic aging clocks in a phase 2a clinical trial supports simultaneous geroprotective assessment.. Nature Biotechnology 2026. https://doi.org/10.1038/s41587-026-03286-y
65. Longitudinal multiomics reveals personalized aging trajectories.. Nature aging . https://doi.org/10.1038/s43587-026-01248-2
66. Universal Single-Cell Transcriptomic Aging Clock powered by LLMs reveals targets to slow cellular aging. Innovation in aging 2025. https://doi.org/10.1093/geroni/igaf122.4305
67. Advancing biological understanding of cellular senescence with computational multiomics.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02314-y
68. Brain aging and rejuvenation at single-cell resolution.. Neuron 2025. https://doi.org/10.1016/j.neuron.2024.12.007
69. From ageing clocks to human digital twins in personalising healthcare through biological age analysis.. NPJ digital medicine 2025. https://doi.org/10.1038/s41746-025-01911-9
70. The Evolving Landscape of Clinical Aging Clocks: From Epigenetic to Multi-Omics Integration.. Aging cell 2026. https://doi.org/10.1111/acel.70579
71. Validation Requirements for AI-based Intervention-Evaluation in Aging and Longevity Research and Practice. Ageing Research Reviews 2024. https://doi.org/10.1016/j.arr.2024.102617
72. DNA methylation age of blood predicts all-cause mortality in later life. Genome Biology 2015. https://doi.org/10.1186/s13059-015-0584-6
73. DNA methylation-based measures of biological age: meta-analysis predicting time to death. Aging 2016. https://doi.org/10.18632/aging.101020
74. An epigenetic clock analysis of race/ethnicity, sex, and coronary heart disease. Genome Biology 2016. https://doi.org/10.1186/s13059-016-1030-0
75. HIV-1 Infection Accelerates Age According to the Epigenetic Clock. Journal of Infectious Diseases 2015. https://doi.org/10.1093/infdis/jiv277
76. Breaking new ground on human health and well-being with epigenetic clocks: A systematic review and meta-analysis of epigenetic age acceleration associations.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102552
77. Metformin decelerates aging clock in male monkeys.. Cell 2024. https://doi.org/10.1016/j.cell.2024.08.021
78. Transplanted hearts assimilate the recipient’s biological age. bioRxiv 2026. https://doi.org/10.64898/2026.09.15.751836
79. A stem cell aging clock links biological age deviation to clinical outcome in acute myeloid leukemia. bioRxiv 2026. https://doi.org/10.64898/2026.02.12.703707
80. Biological age model using explainable automated CT-based cardiometabolic biomarkers for phenotypic prediction of longevity.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56741-w
