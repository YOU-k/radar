# 多模态衰老时钟与生物年龄 · 方向背景报告

证据 75 篇 · 覆盖度 0.62 · 第 6 轮 · 更新 2026-10-11 · 数字核验删句 1

## 本次变更

- 新增 [19] Intraindividual longitudinal changes of the proteome reveal dynamic markers of biological aging

## 摘要（TL;DR）

- 表观遗传时钟是单组学衰老时钟中最成熟的一支，Horvath 多组织预测器从 21,369 个 CpG 中选出 **353 个时钟 CpG**，在多数组织中预测误差约 **3.6 年** [1]。
- 时钟临床效用需大队列横向比较：Generation Scotland 18,859 人、随访 10 年的无偏比较纳入 14 种时钟与 174 种新发疾病，完全校正模型下 13 种时钟与 57 种疾病共 **176 个 Bonferroni 显著关联**，其中 **GrimAge v2 和 DunedinPACE 各有 72 个**显著关联 [2]。
- 表观时钟的生物学可解释性与可靠性受质疑：TranslAGE 平台评估 18 种 DNAm 标志物发现多数技术重现性好，但**生物学可靠性低至中等**，调整免疫组成后进一步下降，且技术重现性不能预测生物学可靠性 [3]。
- 跨组织可比性是另一争议点：对五种组织中 284 份样本（83 人，9–70 岁）的比较显示，口腔与血液组织的表观年龄估计**平均差近 30 年**，多数血液时钟与口腔组织相关性低，**Skin and Blood clock** 跨组织一致性最好 [4]。
- 蛋白质组时钟依托大规模血浆蛋白平台迅速扩展：UKB 中基于 2,897 个血浆蛋白、45,441 人训练的模型经 Boruta 筛选出 **204 个蛋白**，预测实际年龄 **Pearson r=0.94**，其年龄差与 27 个衰老表型、全因死亡和 26 种年龄相关疾病关联 [5]。
- 转录组时钟在方法上更强调跨平台与跨组织泛化：基于 ARCHS4 的混合专家模型在 56,877 例 2–114 岁样本上达到 **MAE=7.58 年**，肺和脑预测最佳、肝较差，FOSB 重要性 1.00，残差随年龄增大，百岁老人误差达 ±40 年 [6]。
- 多模态衰老时钟正从单一组学向跨器官、跨模态整合推进：基于UKB 44,498人Olink约3,000蛋白的LASSO模型构建了11个器官年龄模型，脑、动脉和整体年龄预测传统年龄r²=0.97，器官年龄差可预测疾病、环境暴露和死亡[7]。
- 跨队列泛化是这些工作的共同薄弱环节：MRIBAG的腹部特征共线性导致泛化较差，脑模型在外部队列存在域偏移[8]；CTBA队列以白人为主（92%）、外部验证有限[9]；ProtBAG训练数据的病理构成会影响泛化与可解释性[10]。
- 单细胞转录组已被用于构建细胞类型特异的免疫衰老时钟：基于1081名18至97岁健康欧洲人外周血单个核细胞的约130万细胞，研究用LASSO、随机森林和PointNet为五类免疫细胞建立**sc-ImmuAging**，内外验证表现优于对照，并揭示COVID-19感染后单核细胞和BCG接种后CD8+T细胞的年龄改变异质性[11]。
- 衰老生物学正从单一模态的专用时钟走向多模态、多任务的基准与基础模型：LongevityBench 以 **17 项任务、5 个生物数据域** 评估 **18 个前沿 AI 系统**（来自 6 个开发团队），结果显示没有单一模型主导所有任务，**组学年龄预测是最难的任务**，而 0.6B–9B 的多任务 Longevity-LLM 可匹配或超过更大的通用系统 [12]。

## 1 背景与定义

多模态衰老时钟的方向边界，首先由“生物年龄”这一构念本身的多层性决定。它既包含以死亡/发病风险为锚的**表型年龄**（如 PhenoAge 用临床表型年龄复合指标替代实际年龄训练 [13]），也包含以分子损伤累积为锚的**因果/机制年龄**（如 DamAge 与 AdaptAge 通过表观全基因组孟德尔随机化分离损伤性与适应性甲基化变化 [14]），还包含以器官功能为锚的**器官特异年龄**（如 11 个器官蛋白组年龄差 ProtBAG [10]、7 个 MRI 器官时钟 MRIBAG [8]）。三者训练目标不同，导致同一“年龄差”在不同研究中的含义不可直接互换。**因此本方向的核心问题不是“哪个时钟更准”，而是“在给定终点（死亡、疾病、功能、干预响应）下，哪种模态与哪种建模目标构成有效且可迁移的测量”**。这也解释了为何 Generation Scotland 的无偏比较中，以死亡/功能衰老为训练目标的第二、三代时钟在 174 种新发疾病上显著优于第一代 [2]，而 LinAge2 以 20 年全因死亡为优化目标时报告 AUC=0.8440 [15]。

演化脉络上，该方向经历了四层扩展。第一层是**单组学时钟的成熟与内部分化**：表观遗传时钟从跨组织 353 CpG 预测器 [1] 分化出表型锚定 [13]、因果拆分 [14]、通路级建模 [16] 与内在能力终点 [17]；蛋白组时钟依托 UKB 大规模平台扩展到 204 蛋白精简面板 [5]、器官特异 [18] 与纵向暴露关联 [19]；转录组时钟则转向跨平台泛化 [20] 与单细胞分辨率 [11]。第二层是**模态与器官的横向整合**：StackAge 整合蛋白与代谢物 [21]，MetBAG 构建 5 个器官代谢时钟 [22]，ProtBAG 与 9 个表型年龄差时钟整合 [10]，OMICmAge 整合甲基化、多组学与电子病历 [23]。第三层是**空间与单细胞图谱对衰老定义的细化**：小鼠九组织空间转录组把衰老定位到免疫球蛋白聚集的微环境 [24]，乳腺与骨骼肌单细胞多组学把衰老拆到细胞类型与 SASP 异质性 [25][26]。第四层是**基准、基础模型与统一评估框架**：LongevityBench 以 17 项任务、5 个数据域评测 18 个 AI 系统 [12]，ComputAgeBench 以 66 个血液甲基化数据集、19 种疾病测试 13 个时钟 [27]，Biolearn 提供跨标志物、跨数据集的统一协调与评估 [28]。

**跨组织与跨队列泛化是本方向最系统性的未解问题，且其失败模式已被具体刻画。** 表观时钟在口腔与血液间平均差近 30 年，多数血液时钟与口腔组织相关性低 [4]；Horvath 与 PedBE 在墨西哥儿童青少年队列中预测准确性下降 [29]；MRIBAG 的腹部特征共线性导致泛化较差、脑模型存在域偏移 [8]；CTBA 队列以白人为主（92%）且外部验证有限 [9]；MetaboAgeMort 主要基于欧洲白人样本 [30]。**这些证据共同指向一个判断：当前多模态时钟的“多模态”多发生在同一队列内的横向拼接，而非跨人群、跨平台、跨组织的可迁移整合。** 与之相对，OMICmAge 在 MGB 开发并在 All of Us、TruDiagnostic、Generation Scotland 等独立队列验证 [23]，GOLD BioAge 轻量版在三个中国队列验证 [31]，属于少数把外部验证作为设计前提的工作。

**可靠性、偏倚与可解释性构成第二类核心问题，且三者相互纠缠。** TranslAGE 评估 18 种 DNAm 标志物发现多数技术重现性好但生物学可靠性低至中等，调整免疫组成后进一步下降，且技术重现性不能预测生物学可靠性 [3]；常用 ML/AI 连续结局回归模型存在系统预测偏差，可传播至下游关联并产生方向相反的虚假关联 [32]；概率框架进一步显示生物年龄不确定性（BAU）与 BAG 弱相关，并随个体分子间年龄信号不一致而增加 [33]。**这意味着“年龄差”作为暴露变量进入下游流行病学或干预分析时，其测量误差结构尚未被常规建模。** 可解释性方面，多数时钟 CpG 不与已知转录因子结合位点重叠，弱相关非 TFBS CpG 建模的 TFMethyl Clock 达到 MdAE=3.77 年、优于 Horvath1 的 5.95 年 [34]，说明**预测精度与机制解释可以脱钩**；PathwayAge 转向通路级建模 [16]、SenePy 与 hUSI 在“细胞类型特异”与“通用衰老 signature”之间取向相反 [35][36]，都是对这一脱钩的不同回应。

**干预响应性与因果验证是第三类核心问题，也是时钟从“描述性生物标志物”走向“替代终点”的门槛。** TranslAGE 整合 51 项人类纵向干预研究、统一计算 16 种表观时钟，发现不同干预与时钟响应差异显著，但文献碎片化与时钟面板不一致导致难以直接比较 [37]；rentosertib 2a 期试验中六种蛋白组时钟一致提示治疗组生物年龄更低，但需借助通路分析间接区分抗衰老与抗纤维化效应，且样本来自单一疾病与短期试验 [38]；ClockBase Agent 再分析 43,602 个干预-对照比较，发现更多干预加速而非延缓衰老、疾病状态多加速生物年龄，但依赖已有时钟预测且实验验证有限 [39]。**目前只有少数工作把时钟预测推进到湿实验验证**，如 AURORA 通过降低年龄差的干预计算筛选并在线虫中验证 Neisseria flavescens 活菌延长寿命与健康寿命 [40]，以及二甲双胍灵长类研究中脑衰老约回退 6 年并伴随脑结构与认知改善 [41]。异时心脏移植显示移植心脏生物年龄快速同化受体年龄而非保留供体年龄 [42]，则从另一侧提示**组织生物年龄受系统环境驱动，可能限制“器官时钟”作为局部干预终点的解释力**。

**基准与基础模型正在重塑方向的组织方式，但尚未收敛。** LongevityBench 显示没有单一模型主导全部任务、组学年龄预测是最难任务，而 0.6B–9B 的多任务 Longevity-LLM 可匹配或超过更大通用系统 [12]；Longevity-LLM v0.1 在 DNA 甲基化、蛋白组、临床标志物与 RNA 表达上微调，强化微调后表观年龄预测 MAE 为 4.34 年 [43]；单细胞基准覆盖超过 250 万单细胞转录组，发现冻结预训练表征下 Geneformer 在时序年龄预测与年龄伪时间一致性上最佳，但 2000 个高变基因平均表现更高 [44]。**这些结果共同表明：通用基础模型在衰老任务上并不自动占优，任务专用的小模型与特征选择仍具竞争力；而不同基准在模态覆盖、终点定义与评测设计上尚未统一** [12][27]。资源层面，Biolearn 以跨标志物、跨数据集评估为重心 [28]，Immunosenescence Inventory 以免疫领域多组学整合与免疫时钟计算为重心 [45]，二者均依赖已有公开数据、未提供统一预测性能基准，反映**数据资源建设与评测标准建设仍是两条尚未合流的线**。

综合来看，本方向的边界可概括为：**以多模态分子、影像与功能表型为输入，以生物学年龄与衰老速率为输出，以跨组织/跨队列泛化、干预响应性与因果可解释性为验证标准，并以基准与基础模型为组织形态。** 其核心张力在于三对取舍：预测精度与机制解释的脱钩 [34][16]、细胞类型特异性与通用泛化的对立 [35][36]、以及队列内多模态拼接与跨人群可迁移整合的差距 [8][23]。这些张力尚未有公认解法，也构成本方向后续工作的主要着力点。

## 2 方法学


### 2.1 单组学衰老时钟（表观 / 蛋白 / 转录）

表观遗传时钟是单组学衰老时钟中发展最成熟的一支。Horvath 多组织预测器整合 82 个 Illumina 27K/450K 数据集、7844 个非癌样本，用弹性网络回归从 21,369 个 CpG 中选出 **353 个时钟 CpG**，在多数组织中预测误差约 **3.6 年**，并显示早衰症不符合正常衰老、iPS 重编程将表观时钟重置为 0 [1]。后续工作转向以表型而非实际年龄为训练目标：DNAm PhenoAge 用两步法纳入临床表型年龄复合指标，在全因死亡、癌症、健康寿命、身体功能和阿尔茨海默病预测上优于第一代时钟 [13]。因果取向的工作则通过表观全基因组孟德尔随机化筛选因果 CpG，构建追踪损伤性变化的 DamAge 与适应性变化的 AdaptAge，前者与死亡等不良结局相关，后者与有益适应相关，且两者对短期干预敏感 [14]。

时钟的临床效用需要在大队列中横向比较。一项基于 Generation Scotland 18,859 人、随访 10 年的无偏比较纳入 14 种时钟与 174 种新发疾病，完全校正模型下 13 种时钟与 57 种疾病共 **176 个 Bonferroni 显著关联**，其中 **GrimAge v2 和 DunedinPACE 各有 72 个**显著关联，第二、三代时钟显著优于第一代 [2]。LinAge2 报告 20 年全因死亡预测 **AUC=0.8440**，优于 PhenoAge DNAm 的 0.7859 和 GrimAge2 的 0.8233 [15]。这些比较提示，以死亡或功能衰老为训练目标的时钟在疾病场景中更具价值，但不同队列、人群与随访设计下的数值不宜直接横向比高低。

表观时钟的生物学可解释性与可靠性受到质疑。对已建立时钟中预测性 CpG 的分析显示，多数时钟 CpG 并不与已知转录因子结合位点重叠，说明时钟准确性并非主要由 TF 结合动态驱动；用弱相关非 TFBS CpG 建模的 TFMethyl Clock 达到 **MdAE=3.77 年**，优于 Horvath1 的 5.95 年，接近 PhenoAge 的 3.79 年 [34]。PathwayAge 转而整合 GO/KEGG 通路级甲基化而非孤立 CpG，在多队列和疾病组织中预测年龄并识别神经退行、免疫失调、代谢病相关通路 [16]。可靠性方面，TranslAGE 平台评估 18 种 DNAm 标志物发现多数技术重现性好，但**生物学可靠性低至中等**，调整免疫组成后进一步下降，且技术重现性不能预测生物学可靠性 [3]。

跨组织可比性是表观时钟应用中的另一争议点。对五种组织中 284 份样本（83 人，9–70 岁）的比较显示，口腔与血液组织的表观年龄估计**平均差近 30 年**，多数血液时钟与口腔组织相关性低，**Skin and Blood clock** 跨组织一致性最好 [4]。发育起源研究将成人时钟分解到单个 CpG，发现时钟位点发育轨迹高度异质且非线性，**超过三分之一**位点自出生即存在个体差异，高于非时钟位点，且出生变异与遗传背景和产前暴露相关 [46]。综述性工作则把表观时钟与程序性衰老理论联系，指出时钟 CpG 附近富集 Hox、polycomb 等发育基因，提出发育程序在生命后期持续并转为有害 [47]。

干预响应性是表观时钟作为替代终点的前提。TranslAGE 数据库整合 51 项人类纵向干预研究，统一计算 16 种表观时钟和 94 种额外 DNAm 标志物，通过配对比较发现不同干预与时钟响应差异显著，并指出文献碎片化、时钟面板不一致导致难以直接比较 [37]。内在能力时钟则提供了另一类终点：基于 INSPIRE-T 队列 933 人 EPIC 甲基化数据，用弹性网回归筛选 **91 个 CpG** 预测内在能力，IC 与年龄负相关 **rs=-0.65**，DNAm IC 预测相关 0.61，并在 FHS 中验证其可预测死亡、关联临床与免疫和生活方式因素 [17]。

蛋白质组时钟依托大规模血浆蛋白平台迅速扩展。UKB 中基于 2,897 个血浆蛋白、45,441 人训练的模型经 Boruta 筛选出 **204 个蛋白**，预测实际年龄 **Pearson r=0.94**，其年龄差与 27 个衰老表型、全因死亡和 26 种年龄相关疾病关联，并在 CKB（3,977 人）和 FinnGen（1,990 人）中独立验证 [5]。PAC 使用 UKB Pharma Proteomics Project 的 53,021 名 39–70 岁参与者和 2,923 个 Olink 蛋白，以 LASSO 预测全因死亡，随访超 10 年，发现 PAC 年龄偏差与死亡及多种年龄相关疾病显著关联 [48]。器官特异时钟进一步细分：基于 UKB 43,616 人及 CKB、NHS 外部队列，用 Olink 2,916 蛋白构建整体和十个器官时钟，跨队列 **r=0.98 和 0.93**，脑衰老与死亡关联最强，精简蛋白面板可保持性能 [18]。

蛋白质组时钟也被用于更具体的表型与暴露维度。HPS 基于 UKB 53,018 人和 2,920 个蛋白构建健康寿命评分，随访 13.5 年，43,119 名基线健康者中 **12,427 人（28.8%）**发生健康寿命终点事件 [49]。ECM 时钟仅用 **14 个血浆蛋白**，发现 ECM 蛋白随龄呈 U 型轨迹、最低点约 40–50 岁，可预测年龄并区分健康与疾病，但最老仅 66 岁的队列使 U 型轨迹较弱 [50]。肌肉骨骼时钟 MSKAge 与 MSKAgeMort 在 21,070 名 UKB 参与者中开发，MSKAgeMort 与实际年龄相关 **r 女性=0.93、r 男性=0.88**，其加速指标可预测死亡、肌肉骨骼病和年龄相关病 [51]。KORA 队列的纵向血浆 LC-MS 蛋白质组（9105 样本、4100 人、25–88 岁）则显示蛋白质组年龄加速与生活方式和临床风险因素相关，心血管代谢暴露共享蛋白质组特征，而吸烟和体力活动具独特特征 [19]。

转录组时钟在方法上更强调跨平台与跨组织泛化。Pasta 采用“age-shift”学习框架，在 bulk、单细胞 RNA-Seq 和微阵列等多平台数据上预测相对年龄，优于 MultiTIMER 和 tAge，可区分衰老、静息和干细胞状态，并显示 p53 相关基因贡献显著 [20]。基于 ARCHS4 的混合专家模型在 56,877 例 2–114 岁样本上达到 **MAE=7.58 年**，肺和脑预测最佳、肝较差，FOSB 重要性 1.00，残差随年龄增大，百岁老人误差达 ±40 年 [6]。K-Dense 多智能体系统在同一 ARCHS4 数据（57,584 样本、28 组织、1,039 队列、1–114 岁）上报告 **R²=0.854、MAE=4.26 年**，并提供校准置信区间以标记过渡期和极端年龄预测 [52]。DeepQA 用混合专家与 Hinge-MAE 损失，在 3060 样本、31 数据集上于健康和非健康受试者中均优于现有方法 [53]。小鼠肝脏时钟 LivAge 则把转录组时钟用于干预评估，在早衰综合征中显示转录组年龄增加，并可评估 Snell Dwarf、Ames Dwarf、GHR 缺陷及热量限制等干预 [54]。

跨组学整合开始出现，但单组学时钟仍是主体。StackAge 整合 UKB 30,376 人的 2,923 个蛋白与 251 个代谢物，年龄预测 **Pearson r≈0.93**，对 2 型糖尿病、阿尔茨海默病和慢性肾脏病的 **AUC 超过 0.90**，中位随访 11.7 年，但未整合表观遗传层且以横断面基线为主 [21]。代谢组时钟 MetaboAgeMort 用 UKB 239,291 人血浆代谢组、以 10 年全因死亡为替代指标，选出 **185 个**死亡相关代谢标志物，训练 167,506、测试 71,785 人，提升死亡预测并关联疾病、可调因素和遗传位点，但主要基于欧洲白人样本 [30]。这些工作共同表明，单组学时钟在预测精度、组织特异性和可解释性上各有取舍，跨平台泛化、生物学可靠性与干预响应性仍是尚未解决的核心问题。

### 2.2 多模态整合与跨队列泛化

多模态衰老时钟的构建正从单一组学向跨器官、跨模态整合推进。基于UKB 44,498人Olink约3,000蛋白的LASSO模型构建了11个器官年龄模型，脑、动脉和整体年龄预测传统年龄r²=0.97，器官年龄差可预测疾病、环境暴露和死亡[7]；同一队列43,498人、2,448血浆蛋白构建的11个ProtBAG进一步与9个表型年龄差时钟整合，发现跨器官特征可提升系统性疾病类别和全因死亡预测[10]。代谢组方向则以UKBB 274,247人的107种非衍生代谢物构建5个MetBAG，独立测试集Pearson r为0.25<r<0.42，关联525个疾病终点[22]。影像模态中，MULTI Consortium 313,645人的7个MRIBAG在留出测试中Pearson r 0.23–0.77、MAE约5年，并关联2,923种蛋白和327种代谢物[8]；腹部CT模型在123,281名成人中IPA为29.2，优于人口学模型的21.7（p<0.001）[9]。

跨队列泛化是这些工作的共同薄弱环节。MRIBAG的腹部特征共线性导致泛化较差，脑模型在外部队列存在域偏移[8]；CTBA队列以白人为主（92%）、外部验证有限[9]；ProtBAG训练数据的病理构成会影响泛化与可解释性[10]。表观遗传时钟方面，Horvath和PedBE等常用时钟在墨西哥儿童青少年队列中预测准确性下降，基于Kriging和DNN特征适配的迁移学习可缩小目标数据差距，但样本仅523份血样[29]。OMICmAge在MGB约31,264人开发，并在All of Us 10,769、TruDiagnostic 14,213、Generation Scotland 18,672等独立队列验证[23]；GOLD BioAge的轻量版本在CHARLS、CLHLS、RuLAS三个中国队列验证有效[31]。中国人群的mCAS队列纳入2,019名18–91岁个体，构建核心能力时钟、多模态时钟和器官相关时钟三层框架，但外部验证和跨族群适用性未说明[55]。

多组学与临床数据的整合被用于提升预测稳健性。OMICmAge整合DNA甲基化与多组学及电子病历，与慢病和死亡强相关[23]；以色列10K项目对1万名40–70岁健康人每2年随访，构建多生理系统BA评分，揭示男女衰老模式差异，高BA与年龄相关疾病患病率升高相关[56]。概率框架则从预测年龄分布的均值和宽度推导BAG与生物年龄不确定性（BAU），在超45万名UKB参与者中显示BAU与BAG弱相关，并随个体分子间年龄信号不一致而增加[33]。方法学上，常用ML/AI连续结局回归模型存在系统预测偏差并可传播至下游关联，甚至产生“预测脑龄越大认知越好”等虚假关联，约束优化回归框架可改善校准和下游推断[32]。

多模态时钟也开始进入干预评估与发现流程。在rentosertib治疗特发性肺纤维化的12周2a期试验中，六种蛋白质组时钟（ProtAge、OrganAgemortality、OrganAgechrono、PAC、ipfP3GPT、PAOPAC）均一致预测治疗组生物年龄更低，但需借助通路分析间接区分抗衰老与抗纤维化效应，且样本来自单一疾病和短期试验[38]。ClockBase Agent整合40余种衰老时钟再分析人鼠甲基化与RNA-seq数百万样本、43,602个干预-对照比较，发现超500种干预显著降低生物年龄，并指出更多干预加速而非延缓衰老、疾病状态多加速生物年龄，但依赖已有时钟预测且实验验证有限[39]。生成式多模态框架AURORA则通过降低年龄差的干预计算筛选预测Neisseria flavescens为顶级候选，分离两株菌并在线虫中验证活菌可延长寿命和健康寿命[40]。

### 2.3 单细胞与空间衰老图谱

单细胞转录组已被用于构建细胞类型特异的免疫衰老时钟。基于1081名18至97岁健康欧洲人外周血单个核细胞的约130万细胞，研究用LASSO、随机森林和PointNet为五类免疫细胞建立**sc-ImmuAging**，内外验证表现优于对照，并揭示COVID-19感染后单核细胞和BCG接种后CD8+T细胞的年龄改变异质性[11]。在更大规模公共数据上，**scAgeClock**利用CZ CELLxGENE中超过40种人体组织、400种细胞类型的单细胞转录组，采用门控多头注意力神经网络，预测精度高于偏最小二乘、弹性网等基线[57]；另一项工作把单细胞转录组表示为基因名序列的“细胞句子”，微调预训练大语言模型，在数百万细胞上训练后实现单细胞分辨率年龄预测，并提名可降低转录年龄的候选靶点[58]。三者都指向单细胞分辨率的生物年龄估计，但数据来源、建模策略与验证范围不同，且均以公共或健康人群数据为主，外部验证有限。

空间维度上，小鼠九组织的空间转录组显示，衰老敏感位点与组织结构熵升高共定位，免疫球蛋白表达细胞聚集是其微环境特征，**IgG**在雌雄小鼠及人组织中随衰老积累，并可诱导巨噬细胞和小胶质细胞促衰老，靶向降低IgG可缓解小鼠多组织衰老[24]。人皮肤的单细胞与空间转录组研究构建了**SenSkin™**皮肤特异衰老基因集，发现光老化的衰老细胞负担高于时序衰老，衰老细胞倾向聚集，衰老黑素细胞黑色素合成升高、衰老网状真皮成纤维细胞胶原和弹性纤维合成下降[59]。小鼠乳腺的多组学图谱则显示上皮、免疫和成纤维细胞组成的年龄相关改变，并伴随代谢、促炎和癌症相关基因的表观与转录变化[25]。这些工作共同把衰老从“细胞类型比例变化”推进到“空间微环境与细胞互作”，但组织、物种和验证策略差异明显。

细胞衰老的识别方法本身存在分歧。**hUSI**则从73项公开RNA-seq研究学习通用衰老特征，在bulk和单细胞多种条件下优于31种方法，并可用于COVID-19肺和黑色素瘤组织[36]。二者取向相反：一个强调细胞类型特异性，一个强调通用性，反映出“通用衰老signature受细胞异质性掩盖”与“通用评分更易泛化”之间的争议[35][36]。综述亦指出，缺乏特异性标志物、衰老细胞稀少且异质动态，是计算多组学识别衰老细胞的主要障碍[60]。

在特定组织与干预筛选上，人骨骼肌单核RNA-seq与ATAC-seq联合分析构建了首个衰老人肌衰老细胞图谱，解析SASP异质性与动态，并提出**Maraviroc**作为肌少症衰老治疗候选[26]。线虫研究中，BitAge与Stochastic Clock预测128种神经元类型的生物年龄约98h至177h，近2倍差异，两时钟相关Pearson 0.65（P=5.5×10−17），并验证丁香酸和vanoxerine可防止神经退化[61]。脑衰老综述则从细胞类型中心视角总结年龄相关变化、细胞互作及年轻化干预，但指出单细胞技术仍受样本、批次和因果推断限制[62]。这些结果说明单细胞与空间图谱已能提名干预靶点，但跨物种、跨组织的因果验证仍是共同瓶颈。

### 2.4 衰老生物学基准与基础模型

衰老生物学正从单一模态的专用时钟走向多模态、多任务的基准与基础模型。LongevityBench 以 **17 项任务、5 个生物数据域** 评估 **18 个前沿 AI 系统**（来自 6 个开发团队），结果显示没有单一模型主导所有任务，**组学年龄预测是最难的任务**，而 0.6B–9B 的多任务 Longevity-LLM 可匹配或超过更大的通用系统 [12]。与之呼应，Longevity-LLM v0.1 将 Qwen3-14B 在 DNA 甲基化、蛋白质组、临床生物标志物和 RNA 表达上微调，强化微调后表观年龄预测 **MAE 为 4.34 年**，超过 Horvath 多组织时钟，蛋白质组谱生成也显著优于所比较的前沿 LLM [43]。单细胞层面，一项基准评估了 10 个通用单细胞基础模型、3 个衰老专用模型及传统方法，覆盖 5 个生物学问题、**超过 250 万单细胞转录组**，发现冻结预训练表征下 Geneformer 在时序年龄预测和年龄伪时间一致性上最佳，但 2000 个高变基因平均表现更高，多个模型在三种疾病背景中捕捉到正向分子年龄偏移 [44]。

基准化也发生在表观时钟这一最成熟的方向。ComputAgeBench 以“可靠时钟应能区分健康个体与衰老加速疾病个体”为核心假设，整合 **66 个公开血液 DNA 甲基化数据集、覆盖 19 种疾病**，测试 13 个已发表表观时钟模型，并另建 46 个数据集用于训练新时钟 [27]。综述层面，临床衰老时钟被认为正从表观遗传向多组学、多模态整合演进，AI、集成学习与深度学习推动其在准确性、可解释性和泛化性上的进展 [63]；生物年龄预测器则被讨论与“人类数字孪生”结合，其中表观时钟被认为预测生物年龄和健康表型最准确，但落地受数据整合、隐私、互操作性和纵向建模限制 [64]。方法学综述进一步把 AI 生物年龄预测拆解为生物标志物选择、特征工程、模型开发、偏倚校正和性能评估，并指出数据异质性、泛化性有限、可解释性不足与临床转化障碍是当前挑战 [65]。

对生成式与深度学习应用的综述梳理了 2016–2024 年间 **125 篇同行评审研究**，总结 CNN、RNN、GAN、LLM 和扩散模型在衰老时钟、合成数据生成、药物发现和多模态健康评估中的使用，并强调多模态、多任务研究系统的兴起 [66]。与之相对，针对 AI 干预评估的验证要求提出评估应正确、有用、全面、可解释，并考虑因果、跨学科、标准、纵向数据和已知衰老生物学，建议采用 LLM 结合知识图谱与检索增强生成并开展基准测试，而非依赖朴素的 LLM 查询或传统生物医学数据库比较 [67]。这些工作共同显示：领域已从“造更多专用时钟”转向“如何统一评测、跨模态推理并约束验证标准”，但组学年龄预测仍是最难环节，且不同基准在模态覆盖与评测设计上尚未收敛 [12][27]。

### 2.5 类器官、扰动与 Cell Painting 衰老建模

Cell Painting 自 **2013 年**提出，是一种基于显微成像的细胞标记 assay，目标在于捕获细胞状态并优化图像型 profiling；其核心思路是借助定量图像分析，从图像中提取丰富信息以识别生物样本间的相似性或差异，而非像传统高内涵筛选那样只测量少量特征 [68]。该综述指出，Cell Painting 能够捕获细胞对多种扰动的响应，十年来其协议、特征提取、质控和批次校正持续改进，并已应用于机制研究、毒性评估及多组学整合等场景 [68]。

在方法学层面，该工作将 Cell Painting 与传统高内涵筛选相对照，强调前者以图像型 profiling 替代少量特征测量 [68]。作为综述，其局限在于未提供统一定量基准，结论依赖公开数据集与计算实验技术的进展；未来方向包括计算与实验技术的推进、新公开数据集的构建，以及与其他高内涵数据的整合 [68]。

## 3 数据与资源

面向多模态衰老时钟与生物年龄研究，现有资源可分为通用评估框架与领域专用数据库两类。**Biolearn** 作为开源库，针对跨人群验证缺乏标准化方法、标志物设计分散及数据集结构不一致等障碍，提供统一的整理、协调与系统评估框架，覆盖多公开数据集与多种衰老生物标志物，并输出标准化格式及性能、稳健性、泛化性评估，其开源地址为 https://Bio-Learn.github.io [28]。该工作强调可复现的跨数据集比较，但依赖已有公开数据，临床验证仍待推进 [28]。

与之互补，**Immunosenescence Inventory** 聚焦免疫衰老，整合单细胞转录组、bulk转录组、表观组及 TCR/BCR 等多物种数据，提供知识 curation、多模态数据集与工具，支持免疫细胞识别和**免疫时钟**计算，用于评估生物年龄、预测年龄相关疾病及干预影响 [45]。其基准参照 ImmPort、InnateDB、Aging Atlas 等既有数据库，但未提供统一预测性能基准，单细胞免疫衰老覆盖仍有限 [45]。两者差异在于：前者以跨标志物、跨数据集的通用评估与协调为重心，后者以免疫领域多组学整合与专用时钟工具为重心；二者均受限于对已有公开数据的依赖 [28][45]。

## 4 应用与结果

在血液与多组织样本中，DNA甲基化年龄差（Δage）与死亡风险的关联得到多项队列证据支持。四个老年人纵向队列的荟萃分析显示，**Δage每高5年全因死亡风险增加21%，校正健康、生活方式与APOE后仍增加16%**，且Δage遗传度为0.43 [69]。随后扩展至13个队列、13,089人（2,734例死亡）的荟萃分析比较了Horvath 353 CpG与Hannum 71 CpG时钟，表观年龄与实足年龄相关系数为0.65–0.89，年龄加速与全因死亡风险增加相关，且纳入血液细胞组成信息可提升预测 [70]。同一353 CpG时钟在多组织数据中显示表观年龄加速存在种族与性别差异，并与冠心病及相关风险因素相关 [71]。在特定暴露与疾病场景中，HIV感染者在血液和脑组织均表现出显著增加的表观年龄加速 [72]；而Lothian Birth Cohort 1936（70岁n=920、73岁n=299、76岁n=273）中，表观年龄加速与70岁时的步行速度、握力、肺功能和认知能力横断面相关，但不预测70至76岁间的功能下降 [73]，提示时钟与功能指标的关联方向可能随暴露类型和随访设计而异。

系统层面的证据整合进一步刻画了EAA关联的广度与异质性。一项系统综述与荟萃分析检索299篇文献，提取**1050个EAA-因素关联、覆盖53种甲基化时钟**，对选定配对进行随机效应荟萃分析，发现若干EAA与生理、认知、社会和环境因素存在显著汇总关联，并建立四级分类与TEAPEE交互数据库 [74]。该工作同时指出研究异质性大、部分关联证据有限、因果方向不明确，这与单队列研究中横断面关联显著而纵向预测有限的模式相互呼应 [73]。

在干预与器官层面，多组学衰老时钟被用于评估灵长类干预和移植场景。40个月二甲双胍干预雄性食蟹猴的研究整合多组织转录组、DNA甲基化、血浆蛋白组与代谢组构建猴衰老时钟，发现二甲双胍显著延缓衰老指标，**脑衰老约回退6年**，保护脑结构并增强认知，部分由Nrf2激活介导 [41]。异时心脏移植的多组学分析则显示，移植心脏的DNA甲基化和基因表达生物年龄快速同化受体年龄而非保留供体年龄，且该效应仅限移植物、不影响受体全身生物年龄 [42]。此外，一项仅提供标题与抽取字段的干细胞衰老时钟研究提出生物学年龄偏差与急性髓系白血病临床结局相关，但未给出具体数值与验证细节 [75]。

## 5 评测、可复现性与争议

（本节暂无入库证据）

## 6 空白与趋势

**趋势一：从“造更多专用时钟”转向统一评测与基准化，但基准之间尚未收敛。** LongevityBench 以 17 项任务、5 个生物数据域评测 18 个前沿 AI 系统，结论是**没有单一模型全能、组学年龄预测最难**，而 0.6B–9B 的多任务 Longevity-LLM 可匹配或超过更大通用模型 [12]。表观方向已有 ComputAgeBench 整合 66 个公开血液 DNA 甲基化数据集、覆盖 19 种疾病、测试 13 个已发表时钟 [27]；单细胞方向则有覆盖 5 个生物学问题、超过 250 万单细胞转录组的基准，发现冻结预训练表征下 Geneformer 在时序年龄预测上最佳，但 2000 个高变基因平均表现更高 [44]。**空白在于：这些基准在模态覆盖、任务定义与评测设计上互不兼容，尚无跨模态统一的衰老评测协议**，也缺少把“预测精度—生物学可靠性—干预响应性”放在同一框架下打分的基准 [28][3]。

**趋势二：多模态整合从“拼接”走向器官分辨与不确定性量化，但跨队列泛化仍是共同短板。** 蛋白组已能构建 11 个器官年龄模型并整合 9 个表型年龄差时钟，发现跨器官特征可提升系统性疾病类别和全因死亡预测 [7][10]；代谢组以 107 种非衍生代谢物构建 5 个 MetBAG [22]；影像侧 7 个 MRIBAG 关联 2,923 种蛋白和 327 种代谢物 [8]。概率框架进一步从预测年龄分布推导生物年龄不确定性（BAU），在超 45 万名 UKB 参与者中显示 BAU 与 BAG 弱相关 [33]。**但 MRIBAG 腹部特征共线性导致泛化较差、脑模型存在域偏移 [8]，CTBA 队列以白人为主（92%）[9]，ProtBAG 训练数据的病理构成会影响泛化 [10]。没人做的方向是：把缺失模态、模态对齐与跨队列校正作为一等公民纳入时钟训练目标，而非事后校正。**

**趋势三：单细胞与空间图谱把衰老推进到“微环境与互作”，但细胞衰老识别本身仍有通用 vs 特异的路线分歧。** sc-ImmuAging 基于 1081 名健康成人约 130 万 PBMC 建立五类免疫细胞时钟，揭示感染与接种后的年龄改变异质性 [11]；scAgeClock 覆盖 40 余种组织、400 种细胞类型 [57]；另有工作把单细胞转录组当作“细胞句子”微调预训练大语言模型 [58]。空间侧，小鼠九组织图谱显示 IgG 积累是保守衰老特征且可诱导促衰老 [24]，人皮肤 SenSkin™ 显示光老化衰老细胞负担高于时序衰老 [59]。**SenePy 强调细胞类型特异 signature 更能重现体内衰老 [35]，hUSI 则强调通用特征更易泛化 [36]，二者取向相反；综述亦指出缺乏特异性标志物、衰老细胞稀少且异质是主要障碍 [60]。空白在于：尚无跨物种、跨组织的因果验证闭环，单细胞时钟的外部验证普遍有限。**

**趋势四：干预评估开始进入时钟框架，但“抗衰老 vs 抗疾病”的效应分离尚未解决。** rentosertib 2a 期试验中六种蛋白质组时钟一致提示治疗组生物年龄更低，但需借助通路分析间接区分抗衰老与抗纤维化效应，且样本来自单一疾病和短期试验 [38]。ClockBase Agent 整合 40 余种时钟、43,602 个干预-对照比较，发现超 500 种干预显著降低生物年龄，同时指出更多干预加速而非延缓衰老、疾病状态多加速生物年龄，但依赖已有时钟预测且实验验证有限 [39]。AURORA 通过降低年龄差的干预计算筛选并在线虫中验证活菌延长寿命 [40]。**没人做的方向是：把干预响应性作为时钟的独立验证维度，建立能区分“疾病修饰”与“衰老速率修饰”的终点体系**；现有证据也提示表观时钟对短期干预敏感但不同干预响应差异显著、面板不一致导致难以直接比较 [14][37]。

**趋势五：基础模型与语言模型进入衰老生物学，但验证标准与可解释性要求尚未配套。** Longevity-LLM v0.1 将 Qwen3-14B 在 DNA 甲基化、蛋白质组、临床生物标志物和 RNA 表达上微调，强化微调后表观年龄预测 MAE 为 4.34 年，超过 Horvath 多组织时钟 [43]。生成式与深度学习综述梳理 2016–2024 年间 125 篇同行评审研究，强调多模态、多任务研究系统的兴起 [66]。与之相对，针对 AI 干预评估的验证要求提出评估应正确、有用、全面、可解释，并考虑因果、跨学科、标准、纵向数据和已知衰老生物学，建议采用 LLM 结合知识图谱与检索增强生成并开展基准测试 [67]。**空白在于：领域尚无面向衰老基础模型的“可信性”规范**——常用 ML/AI 连续结局回归存在系统预测偏差并可传播至下游、甚至产生方向相反的虚假关联，约束优化回归框架虽可改善校准，但尚未被纳入基础模型训练与评测流程 [32]。

**趋势六：类器官、扰动与 Cell Painting 体系在衰老建模中仍近乎空白。** Cell Painting 自 2013 年提出，以图像型 profiling 捕获细胞状态，十年来协议、特征提取、质控与批次校正持续改进，并已用于机制研究、毒性评估及多组学整合 [68]。但该综述未提供统一定量基准，结论依赖公开数据集与计算实验技术进展 [68]。**在本次证据清单中，没有一项工作把 Cell Painting 或类器官体系直接用于衰老时钟训练、年轻化建模或扰动响应预测**；单细胞与空间图谱虽已能提名干预靶点（如 Maraviroc [26]、丁香酸与 vanoxerine [61]），但跨物种、跨组织的因果验证仍是共同瓶颈。**把形态学扰动图谱与分子组学时钟对齐、在类器官中建立可干预的衰老速率读出，是当前最明确的方向性空白。**

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 单组学衰老时钟（表观/蛋白/转录） | 成熟 | 表观时钟已有 Horvath 2013 [1] 与 PhenoAge [13] 这类被反复验证、系数公开的基准，属于方法收敛后的增量迭代；蛋白组时钟 [5] 与因果增强表观年龄 [14] 说明新工作主要在换模态/换目标，而非重构范式。 |
| 2.2 多模态整合与跨队列泛化 | 朝阳 | 雷达样本中该节 **n=15、近两年占比 0.92、CNS 占比 0.53**，且方法明显未收敛：血浆蛋白组连接脑-免疫衰老 [7]、MRI 多器官时钟 [8] 代表不同模态路线并存；表型组性别特异动态 [56] 与 AI agent 挖掘干预 [39] 说明整合层与决策层都还在开题阶段。 |
| 2.3 单细胞与空间衰老图谱 | 朝阳 | 空间转录组揭示免疫球蛋白相关衰老 [24]、单细胞免疫衰老时钟揭示个体异质性 [11] 表明“细胞类型分辨的衰老建模”刚起步；乳腺单细胞衰老图谱 [25] 与细胞类型特异衰老景观 [35] 说明图谱在快速积累但尚未形成统一坐标/统一时钟。 |
| 2.4 衰老生物学基准与基础模型 | 萌芽 | 已有 ComputAgeBench 表观时钟基准 [27] 与 AI 干预评估验证要求 [67]，但雷达样本中该节 **n=9、median_citations=0、CNS 占比 0.11**，且多为观点/框架类 [66]、[64]，尚缺被广泛采用的基准与基础模型。 |
| 2.5 类器官、扰动与 Cell Painting 衰老建模 | 证据不足 | 雷达样本中该节仅 **n=1**，只有 Cell Painting 十年综述 [68]，缺少第二篇可引证据来支撑阶段判断；不能据此推断领域空白或成熟。 |
| 3 数据与资源 | 证据不足 | 雷达样本中该节仅 **n=2**：统一衰老生物标志物 curation/evaluation 框架 [28] 与免疫衰老多组学数据库 [45]，数量不足以判断阶段。 |
| 4 应用与结果 | 成熟 | 表观年龄预测死亡率的 meta 分析 [69]、种族/性别/冠心病表观时钟分析 [71]、HIV 加速衰老 [72] 等属于早期大规模关联验证，方法与应用范式已稳定，新意主要在增量应用。 |
| 5 评测、可复现性与争议 | 证据不足 | 雷达样本中该节 **n=0**，无可引用证据；这本身提示评测/可复现性在雷达证据库中未被单独挂载，不能据此判断领域无争议。 |

**整体判断**：这个方向整体处于**朝阳期偏早期**，但内部高度不均：单组学时钟与应用结果已**成熟**，多模态整合与单细胞/空间图谱是**朝阳**，基准/基础模型是**萌芽**，类器官+扰动+Cell Painting 在雷达样本中几乎**证据不足**。窗口期我判断还有 **2–3 年**：多模态整合目前 **CNS 占比 0.53、近两年占比 0.92**，说明高影响力工作密集但方法未收敛，谁先定义跨队列/缺失模态/纵向增量的统一评测，谁就占住下一阶段入口。最大不确定性是**评测与可复现性缺位**（第 5 节雷达样本 **n=0**），以及类器官/扰动体系能否产出可被公共数据验证的衰老读出——如果这两点不解决，多模态时钟可能停留在“每个队列一个模型”的碎片化状态。

**接下来怎么做**：
1. **切入多模态缺失模态对齐，用公共大队列做 demo**：以血浆蛋白组 [7] 与 MRI 多器官时钟 [8] 为两个模态锚点，构建“甲基化+蛋白+影像”缺失模态下的生物年龄估计与跨队列校正；现在做是因为该节 **近两年占比 0.92、CNS 占比 0.53**，方法未收敛且审稿人正在找统一框架。
2. **把单细胞/空间衰老图谱转成可迁移的细胞类型分辨时钟**：用单细胞免疫衰老时钟 [11] 与空间免疫球蛋白相关衰老 [24] 作为读出定义，做跨组织/跨平台泛化；现在做是因为图谱刚积累到可训练规模，但尚无统一坐标，先做者定义标签体系。
3. **做衰老 AI 基准与评测层，而不是再训一个时钟**：以 ComputAgeBench [27] 和 AI 干预评估验证要求 [67] 为起点，补上缺失模态、跨队列、纵向增量三类评测；现在做是因为第 5 节雷达样本 **n=0**，评测空白意味着方法学论文的引用窗口打开。
4. **把类器官+多组学合作项目包装成扰动衰老建模**：用 Cell Painting 综述 [68] 定义影像读出，结合统一衰老标志物 curation 框架 [28] 做扰动-年轻化响应的建模与公共数据对齐；现在做是因为该细分在雷达样本中仅 **n=1**，竞争少，且能直接利用博后的类器官合作资源。
5. **用公共数据资源做跨队列泛化验证，避免小样本时钟**：以免疫衰老多组学数据库 [45] 和表型组性别特异动态 [56] 为外部验证集，检验多模态时钟的队列偏移与性别特异校准；现在做是因为多模态整合工作虽多，但跨队列泛化仍是审稿人最常攻击的弱点。

## 参考文献

1. DNA methylation age of human tissues and cell types. Genome Biology 2013. https://doi.org/10.1186/gb-2013-14-10-r115
2. An unbiased comparison of 14 epigenetic clocks in relation to 174 incident disease outcomes.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66106-y
3. Biological Versus Technical Reliability of Epigenetic Clocks and Implications for Disease Prognosis and Intervention Response.. Aging cell 2026. https://doi.org/10.1111/acel.70635
4. Cross-tissue comparison of epigenetic aging clocks in humans.. Aging cell 2025. https://doi.org/10.1111/acel.14451
5. Proteomic aging clock predicts mortality and risk of common age-related diseases in diverse populations. Nature Medicine 2023. https://doi.org/10.1038/s41591-024-03164-7
6. Transcriptomic age prediction using mixture-of-experts models reveals tissue-specific aging signatures in large-scale human RNA-sequencing data. medRxiv 2025. https://doi.org/10.1101/2025.06.28.25330474
7. Plasma proteomics links brain and immune system aging with healthspan and longevity.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03798-1
8. MRI-based multi-organ clocks for healthy aging and disease assessment.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03999-8
9. Biological age model using explainable automated CT-based cardiometabolic biomarkers for phenotypic prediction of longevity.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56741-w
10. Refining the generation, interpretation and application of multi-organ, multi-omics biological aging clocks.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00928-9
11. Single-cell immune aging clocks reveal inter-individual heterogeneity during infection and vaccination.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00819-z
12. An open benchmark and language models for AI in aging biology.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.026
13. An epigenetic biomarker of aging for lifespan and healthspan. bioRxiv 2018. https://doi.org/10.18632/aging.101414
14. Causality-Enriched Epigenetic Age Uncouples Damage and Adaptation. bioRxiv 2023. https://doi.org/10.1038/s43587-023-00557-0
15. LinAge2: providing actionable insights and benchmarking with epigenetic clocks.. npj aging 2025. https://doi.org/10.1038/s41514-025-00221-4
16. Decoding disease-specific ageing mechanisms through pathway-level epigenetic clock: insights from multi-cohort validation.. EBioMedicine 2025. https://doi.org/10.1016/j.ebiom.2025.105829
17. A blood-based epigenetic clock for intrinsic capacity predicts mortality and is associated with clinical, immunological and lifestyle factors.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00883-5
18. Organ-specific proteomic aging clocks predict disease and longevity across diverse populations.. Nature aging 2025. https://doi.org/10.1038/s43587-025-01016-8
19. Intraindividual longitudinal changes of the proteome reveal dynamic markers of biological aging.  . https://doi.org/10.64898/2026.10.01.755909
20. Pasta, a Versatile Transcriptomic Clock, Maps the Chemical and Genetic Determinants of Aging and Rejuvenation. bioRxiv 2025. https://doi.org/10.1002/advs.76740
21. StackAge: an ensemble-based clock for precise quantification of biological age using multi-omics data.. Briefings in bioinformatics 2026. https://doi.org/10.1093/bib/bbag271
22. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
23. OMICmAge quantifies biological age by integrating multi-omics with electronic medical records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01073-7
24. Spatial transcriptomic landscape unveils immunoglobin-associated senescence as a hallmark of aging.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.019
25. Comprehensive single-cell aging atlas of healthy mammary tissues reveals shared epigenomic and transcriptomic signatures of aging and cancer.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00751-8
26. Multiomics and cellular senescence profiling of aging human skeletal muscle uncovers Maraviroc as a senotherapeutic approach for sarcopenia.. Nature communications 2025. https://doi.org/10.1038/s41467-025-61403-y
27. ComputAgeBench: Epigenetic Aging Clocks Benchmark. bioRxiv 2025. https://doi.org/10.1145/3711896.3737382
28. A unified framework for systematic curation and evaluation of aging biomarkers.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00987-y
29. BRIDGING THE GAP: ENHANCING THE GENERALIZABILITY OF EPIGENETIC CLOCKS THROUGH TRANSFER LEARNING.. The annals of applied statistics 2026. https://doi.org/10.1214/26-aoas2136
30. A Novel Metabolomic Aging Clock Predicting Health Outcomes and Its Genetic and Modifiable Factors. Advancement of science 2024. https://doi.org/10.1002/advs.202406670
31. Gompertz Law-Based Biological Age (GOLD BioAge): A Simple and Practical Measurement of Biological Ageing to Capture Morbidity and Mortality Risks.. Advanced science (Weinheim, Baden-Wurttemberg, Germany) 2025. https://doi.org/10.1002/advs.202501765
32. Trustworthy ML/AI for Aging Clocks: Preventing Systematic Prediction Bias in Biological Age Estimation. bioRxiv 2026. https://doi.org/10.64898/2026.05.27.728155
33. Uncertainty redefines biological age.  . https://doi.org/10.64898/2026.09.26.26364091
34. Enhancing the performance and interpretability of epigenetic clocks.. Nucleic acids research 2026. https://doi.org/10.1093/nar/gkag661
35. Unveiling the cell-type-specific landscape of cellular senescence through single-cell transcriptomics using SenePy.. Nature communications 2025. https://doi.org/10.1038/s41467-025-57047-7
36. A transcriptome-based human universal senescence index (hUSI) robustly predicts cellular senescence under various conditions.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00886-2
37. Responsiveness of epigenetic aging biomarkers to longevity interventions in humans.. Nature medicine 2026. https://doi.org/10.1038/s41591-026-04562-9
38. Integration of proteomic aging clocks in a phase 2a clinical trial supports simultaneous geroprotective assessment.. Nature Biotechnology 2026. https://doi.org/10.1038/s41587-026-03286-y
39. Autonomous AI Agents Discover Aging Interventions from Millions of Molecular Profiles. bioRxiv 2025. https://doi.org/10.1101/2023.02.28.530532
40. Multi-modality profiling identifies Neisseria flavescens as a central geroprotective oral commensal in humans.. Nature aging . https://doi.org/10.1038/s43587-026-01220-0
41. Metformin decelerates aging clock in male monkeys.. Cell 2024. https://doi.org/10.1016/j.cell.2024.08.021
42. Transplanted hearts assimilate the recipient’s biological age. bioRxiv 2026. https://doi.org/10.64898/2026.09.15.751836
43. The End of Aging Clocks: Training Foundation Models to Reason in Aging and Longevity. bioRxiv 2026. https://doi.org/10.64898/2026.03.28.714980
44. Benchmarking single-cell foundation models for aging biology.  . https://doi.org/10.64898/2026.09.21.753191
45. Immunosenescence Inventory-a multi-omics database for immune aging research.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1102
46. Characterising developmental dynamics of adult epigenetic clock sites.. EBioMedicine 2024. https://doi.org/10.1016/j.ebiom.2024.105425
47. Epigenetic clocks and programmatic aging.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102546
48. Proteomic aging clock (PAC) predicts age‐related outcomes in middle‐aged and older adults. Aging Cell 2024. https://doi.org/10.1111/acel.14195
49. A proteomic signature of healthspan.. Proceedings of the National Academy of Sciences of the United States of America 2025. https://doi.org/10.1073/pnas.2414086122
50. An Extracellular Matrix Aging Clock Based on Circulating Matrisome Proteins Predicts Biological Aging and Disease.. Aging cell 2026. https://doi.org/10.1111/acel.70474
51. Construction and Validation of Plasma Protein-Based Musculoskeletal Biological Age and Genetic and Environmental Risk Profiles.. Aging cell 2026. https://doi.org/10.1111/acel.70636
52. Guided multi-agent AI invents highly accurate, uncertainty-aware transcriptomic aging clocks. bioRxiv 2025. https://doi.org/10.1101/2025.09.08.674588
53. DeepQA: A Unified Transcriptome-Based Aging Clock Using Deep Neural Networks.. Aging cell 2025. https://doi.org/10.1111/acel.14471
54. LivAge: An Online Aging Clock for Murine Transcriptomic Age Estimation.. Aging cell 2026. https://doi.org/10.1111/acel.70677
55. Multimodal clocks of human aging.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.025
56. Phenome-wide associations of human aging uncover sex-specific dynamics.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00734-9
57. scAgeClock: a single-cell transcriptome-based human aging clock model using gated multi-head attention neural networks.. npj aging 2026. https://doi.org/10.1038/s41514-026-00379-5
58. Universal Single-Cell Transcriptomic Aging Clock powered by LLMs reveals targets to slow cellular aging. Innovation in aging 2025. https://doi.org/10.1093/geroni/igaf122.4305
59. Mapping epidermal and dermal cellular senescence in human skin aging.. Aging cell 2024. https://doi.org/10.1111/acel.14358
60. Advancing biological understanding of cellular senescence with computational multiomics.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02314-y
61. Aging clocks delineate neuron types vulnerable or resilient to neurodegeneration and identify neuroprotective interventions.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01067-5
62. Brain aging and rejuvenation at single-cell resolution.. Neuron 2025. https://doi.org/10.1016/j.neuron.2024.12.007
63. The Evolving Landscape of Clinical Aging Clocks: From Epigenetic to Multi-Omics Integration.. Aging cell 2026. https://doi.org/10.1111/acel.70579
64. From ageing clocks to human digital twins in personalising healthcare through biological age analysis.. NPJ digital medicine 2025. https://doi.org/10.1038/s41746-025-01911-9
65. Artificial intelligence approaches in biological age prediction: current status and challenges.. British journal of biomedical science 2026. https://doi.org/10.3389/bjbs.2026.16141
66. Deep learning and generative artificial intelligence in aging research and healthy longevity medicine.. Aging 2025. https://doi.org/10.18632/aging.206190
67. Validation Requirements for AI-based Intervention-Evaluation in Aging and Longevity Research and Practice. Ageing Research Reviews 2024. https://doi.org/10.1016/j.arr.2024.102617
68. Cell Painting: a decade of discovery and innovation in cellular imaging.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02528-8
69. DNA methylation age of blood predicts all-cause mortality in later life. Genome Biology 2015. https://doi.org/10.1186/s13059-015-0584-6
70. DNA methylation-based measures of biological age: meta-analysis predicting time to death. Aging 2016. https://doi.org/10.18632/aging.101020
71. An epigenetic clock analysis of race/ethnicity, sex, and coronary heart disease. Genome Biology 2016. https://doi.org/10.1186/s13059-016-1030-0
72. HIV-1 Infection Accelerates Age According to the Epigenetic Clock. Journal of Infectious Diseases 2015. https://doi.org/10.1093/infdis/jiv277
73. The epigenetic clock is correlated with physical and cognitive fitness in the Lothian Birth Cohort 1936. International Journal of Epidemiology 2015. https://doi.org/10.1093/ije/dyu277
74. Breaking new ground on human health and well-being with epigenetic clocks: A systematic review and meta-analysis of epigenetic age acceleration associations.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102552
75. A stem cell aging clock links biological age deviation to clinical outcome in acute myeloid leukemia. bioRxiv 2026. https://doi.org/10.64898/2026.02.12.703707
