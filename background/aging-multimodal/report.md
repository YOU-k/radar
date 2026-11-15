# 多模态衰老时钟与生物年龄 · 方向背景报告

证据 85 篇 · 覆盖度 0.60 · 第 11 轮 · 更新 2026-11-15 · 数字核验删句 1

## 本次变更

- 新增 [35] SARDINE unlocks EWAS summary statistics for large-scale epigenetic biomarker analysis
- 新增 [41] Disease aging clocks in the plasma proteome stratify risk and track preclinical progression
- 新增 [63] Single-cell, multi-region profiling of the macaque brain across the lifespan.
- 新增 [59] Mesoscale molecular architecture of the striatum across cell types and adult aging.

## 摘要（TL;DR）

- 表观遗传时钟中，Horvath 多组织预测器整合 82 个 Illumina 27K/450K 数据集、7844 个非癌样本，从 21,369 个 CpG 中选出 353 个时钟 CpG，在多数组织中预测误差约 3.6 年 [1]。
- 基于 Generation Scotland 队列 18,859 人的系统比较显示，完全校正模型下 13 种时钟与 57 种疾病共 176 个 Bonferroni 显著关联，GrimAge v2 和 DunedinPACE 各 72 个 [2]。
- 跨组织应用存在争议：在 83 人、284 份五类组织样本中，口腔与血液组织的表观年龄平均差近 30 年，多数血液时钟与口腔组织相关性低，Skin and Blood clock 一致性最高 [3]。
- TranslAGE 整合 51 项人类纵向干预研究，统一计算 16 种表观时钟和 94 种额外 DNAm 标志物，发现不同干预与时钟的响应差异显著，并指出文献碎片化、时钟面板不一致导致难以直接比较 [4]。
- UKB 中基于 2,897 个血浆蛋白、45,441 人的蛋白质组年龄时钟经 Boruta 筛选出 204 个蛋白，与实际年龄 Pearson r=0.94，并在 CKB（3,977 人）和 FinnGen（1,990 人）中独立验证 [5]。
- 一项工作在 UKB 43,616 人中构建整体和十个器官系统的时钟，在中国（3,977 人）和美国（800 人）队列中验证，跨队列 r 分别为 0.98 和 0.93 [6]。
- 基于 ARCHS4 的混合专家模型使用 56,877 例人类 RNA-seq、覆盖 2-114 岁多组织，达到 MAE=7.58 年，但残差随年龄增大，百岁老人误差达 ±40 年 [7]。
- StackAge 整合 UKB 30,376 人的 2,923 蛋白与 251 代谢物，与实际年龄 Pearson r≈0.93，对 2 型糖尿病、阿尔茨海默病和慢性肾病的 AUC 超过 0.90，但未整合表观遗传层且以横断面基线为主 [8]。
- 一项纵向多组学研究仅以摘要说明其旨在刻画个体化衰老轨迹，未提供可提取的方法、数据规模与定量结果，表明多模态整合能否稳定追踪同一个体衰老轨迹仍缺少直接证据 [9]。
- LongevityBench 构建了覆盖5个生物数据域的17项任务，评测来自6个开发团队的18个前沿AI系统，结论是没有单一模型主导所有任务，组学年龄预测是最难的任务 [10]。

## 1 背景与定义

表观遗传时钟的成熟并未自动带来“生物年龄”概念的统一。Horvath 353 CpG 预测器把生物年龄操作化为“甲基化谱可预测的实足年龄”，其误差约 3.6 年 [1]；PhenoAge 则把目标换成含临床表型的复合指标，使“年龄”承载死亡与疾病风险信息 [11]；DamAge/AdaptAge 进一步把同一甲基化组拆成损伤性与适应性两个方向 [12]。**这三类定义并不等价：前者衡量分子状态与时间的偏离，后者衡量健康结局风险，第三类衡量变化的因果属性。** 因此本方向所说的“生物年龄”应被理解为**一组可计算、但语义随训练目标而变的估计量**，而非单一生物学实体；跨研究比较年龄差之前，必须先声明其定义与训练标签。

从单组学到多模态的演化，核心驱动力不是模型复杂度，而是底物与结局的扩展。蛋白组时钟在 UKB 中以 2,897 蛋白、45,441 人训练、204 蛋白建模，r=0.94，并在 CKB 与 FinnGen 外部验证 [5]；代谢组 MetBAG 用 274,247 人的 107 种代谢物构建 5 个器官时钟，独立测试 r 仅 0.25–0.42 [13]；MRIBAG 的 7 个器官时钟 MAE 约 5 年 [14]；CT 模型以 8 个影像标志物取得 IPA=29.2、10 年 AUC=0.880 [15]。**不同模态的可预测性差异很大，且这一差异同时反映生物学信号强度与测量噪声，不能读作“某模态更接近真实衰老”。** 多模态整合的现有收益主要体现为结局预测的增量（如 ProtBAG 与表型时钟整合提升系统性疾病与死亡预测 [16]），而非对衰老机制的更强解释。

单细胞与空间组学把“生物年龄”从个体层面下推到细胞类型与组织微环境层面，并暴露出一个定义性难题：**同一组织内不同细胞的老化并不同步**。线虫 128 种神经元类型的预测生物年龄从约 98h 到 177h，近 2 倍差异 [17]；SenePy 显示仅 58/1540 细胞类型组合的衰老标志物重叠显著 [18]；hUSI 则主张存在可跨条件迁移的通用衰老特征并在多种条件下优于 31 种方法 [19]。**细胞类型特异与通用特征两种取向尚未在统一基准下裁决**，这直接决定单细胞衰老时钟应当输出“细胞年龄”还是“细胞状态偏移”。空间层面，小鼠九组织图谱把免疫球蛋白聚集与 IgG 积累定位为衰老的微环境特征 [20]，人皮肤 SenSkin™ 显示光老化衰老负担高于时序衰老 [21]，提示**空间坐标本身应作为时钟的协变量而非事后解释**。

本方向的边界因此可归纳为三条。其一，**输入边界**：以分子组学、影像与功能表型为底物，输出可计算的年龄或年龄差；不含纯临床干预报告，也不含无数据无代码的理论推演。其二，**方法边界**：多模态整合须处理模态对齐、缺失模态与跨队列校正，而非把各模态时钟简单并列；现有工作已指出年龄偏倚校正、器官蛋白特异性与外部验证设计是必须同时报告的前提 [16][14]。其三，**评价边界**：预测精度、结局关联、干预响应性与跨队列校准是四个不同维度，**任一维度的优势都不能替代其余维度**；系统比较显示 14 种表观时钟与 174 种疾病的关联强度差异显著，GrimAge v2 与 DunedinPACE 各 72 个显著关联而第一代时钟有限 [2]，而跨组织应用中口腔与血液表观年龄平均差近 30 年 [3]，说明“时钟准不准”与“时钟测的是什么”必须分开回答。

由此，本方向当前的核心问题不是再训练一个误差更低的时钟，而是**建立可复现的定义—基准—校准链条**。LongevityBench 以 17 项任务、5 个数据域评测 18 个前沿系统，结论是没有单一模型全能、组学年龄预测最难 [10]；ComputAgeBench 以 66 个血液甲基化数据集、19 种疾病测试 13 个模型 [22]；Biolearn 提供标志物整理、协调与评估的统一框架 [23]。**这些基准的共同缺口是：多数只覆盖单一模态、缺少纵向轨迹与干预响应性的统一评测，且未把预测偏差与不确定性纳入评分。** 已有方法学证据表明系统预测偏差可产生方向相反的虚假下游关联 [24]，而生物年龄不确定性 BAU 与年龄差 BAG 仅弱相关 [25]；若基准不惩罚这两类问题，排行榜上的优势可能不可迁移。

最后，类器官、扰动与 cell painting 体系构成本方向与实验衰老生物学的接口，但接口尚未闭合。转录组年龄预测器已驱动 cDNA 过表达筛选并鉴定 SRSF1 产生年轻化转录特征 [26]，ClockBase Agent 以 40 余种时钟评估 43,602 个干预-对照比较 [27]，AURORA 以生成式框架提名并在线虫验证候选干预 [28]；而 Cell Painting 一侧仍以协议、特征提取与批次校正的综述性证据为主，未提供统一衰老基准 [29]。**这意味着“用时钟筛选年轻化扰动”在转录组与线虫中已有闭环实例，在成像表型与人类类器官中仍缺少可比的定量基准**，是本方向定义边界内最明确的方法学空白之一。

## 2 方法学


### 2.1 单组学衰老时钟（表观 / 蛋白 / 转录）

表观遗传时钟是单组学衰老时钟中发展最成熟的一支。Horvath 多组织预测器整合 82 个 Illumina 27K/450K 数据集、7844 个非癌样本，用弹性网络回归从 21,369 个 CpG 中选出 **353 个时钟 CpG**，在多数组织中预测误差约 **3.6 年**，并显示早衰症不符合正常衰老、iPS 重编程可将表观时钟重置为 0 [1]。该工作确立了跨组织 DNAm 年龄预测的基本范式，但其训练数据异质性、仅用两平台共有 CpG 等限制也被作者列出 [1]。后续综述将这类时钟与程序性衰老理论联系起来，指出时钟 CpG 邻近 Hox、polycomb 等发育基因，支持发育程序在生命后期持续并转为有害的假说 [30]。

第二代时钟转向以健康结局而非实际年龄为训练目标。DNAm PhenoAge 用包含临床表型年龄的复合指标替代实际年龄，通过两步流程筛选 CpG，在全因死亡、癌症、健康寿命、身体功能和阿尔茨海默病预测上优于第一代标志物 [11]。但该研究基于全血开发，摘要未给出样本规模与误差指标 [11]。更激进的思路来自因果信息：通过表观全基因组孟德尔随机化识别可能因果影响衰老性状的 CpG，构建追踪损伤性变化的 **DamAge** 与适应性变化的 **AdaptAge**，前者与死亡等不良结局相关，后者与有益适应相关，且两者对短期干预敏感 [12]。这类工作把时钟从"预测年龄"推向"区分损伤与适应"，但因果 CpG 的功能验证有限，且依赖 MR 假设 [12]。

时钟数量的膨胀带来了比较与可靠性问题。一项基于 Generation Scotland 队列 **18,859 人**的系统比较将 14 种时钟与 174 种新发疾病对应，完全校正模型下 13 种时钟与 57 种疾病共 176 个 Bonferroni 显著关联，**GrimAge v2 和 DunedinPACE 各 72 个**，而第一代时钟关联有限 [2]。该研究以欧洲裔为主、为观察性设计，且部分时钟与协变量信息重叠 [2]。LinAge2 的评测给出另一组内部对照：其预测死亡 **AUC=0.8684**，优于 PhenoAge Clinical 的 0.8479 和 ChronAge 的 0.8288；20 年死亡 AUC=0.8440，优于 PhenoAge DNAm 的 0.7859 和 GrimAge2 的 0.8233，但部分对比未达统计显著 [31]。这些数字均来自各自研究内部的对照，不宜跨研究直接比高低。

可靠性研究揭示了准确率之外的另一维度。跨组织应用同样存在争议：在 83 人、284 份五类组织样本中，口腔与血液组织的表观年龄平均差**近 30 年**，多数血液时钟与口腔组织相关性低，**Skin and Blood clock** 一致性最高 [3]。这直接质疑了将血源时钟外推至颊上皮或唾液的做法。

提升可解释性的尝试沿两条路径展开。PathwayAge 放弃孤立 CpG，改用 GO/KEGG 通路级甲基化建模，在多队列和疾病组织中验证，能识别神经退行、免疫失调、代谢病相关通路 [32]。另一项工作分析时钟 CpG 与转录因子结合位点的重叠，发现多数时钟 CpG 并不落在已知 TFBS 上，说明时钟准确性并非主要由 TF 结合动态驱动；其构建的 TFMethyl Clock 使用弱相关非 TFBS CpG，**MdAE=3.77 年**，优于 Horvath1 的 5.95 年、接近 PhenoAge 的 3.79 年，且需移除 88,007 个 CpG 后误差才达随机水平 [33]。此外，将成人时钟位点回溯至生命早期发现，时钟位点发育轨迹高度异质且非线性，**超过三分之一**的位点自出生即存在个体差异，高于非时钟位点，并与遗传背景和产前暴露相关 [34]。

干预响应性是时钟走向临床替代终点的前提。TranslAGE 整合 **51 项**人类纵向干预研究，统一计算 16 种表观时钟和 94 种额外 DNAm 标志物，通过配对比较发现不同干预与时钟的响应差异显著，并指出文献碎片化、时钟面板不一致导致难以直接比较 [4]。在方法学层面，SARDINE 框架仅用 EWAS 汇总统计、时钟权重和参考甲基化协方差即可估计时钟与表型的关联，在 **15,677 人**、38 种表观标志物和 4 种表型上准确复现个体水平估计，并揭示标志物与衰老、疾病、生活方式关联的异质性 [35]。这些工具降低了大规模比较的门槛，但不改变时钟本身生物学可靠性有限的现实 [36]。

蛋白质组时钟以血浆蛋白为底物，规模与验证设计是其突出特点。UKB 中基于 **2,897 个血浆蛋白**、45,441 人的蛋白质组年龄时钟经 Boruta 筛选出 **204 个蛋白**，与实际年龄 Pearson r=0.94，年龄差与 27 个衰老表型、全因死亡和 26 种年龄相关疾病关联，并在 CKB（3,977 人）和 FinnGen（1,990 人）中独立验证 [5]。该研究以 UKB 为主、外部样本较小，且观察性关联不能证明因果 [5]。PAC 则直接以全因死亡为代理，用 LASSO 在 UKB Pharma Proteomics Project 的 **53,021 人**、2,923 个 Olink 蛋白上训练，随访超 10 年，年龄偏差与死亡及多种年龄相关疾病显著关联，但训练仅限 UKB、平台单一 [37]。

器官特异性是蛋白质组时钟的差异化方向。一项工作在 UKB **43,616 人**中构建整体和十个器官系统的时钟，基于 Olink 2,916 蛋白与非线性机器学习，在中国（3,977 人）和美国（800 人）队列中验证，跨队列 r 分别为 **0.98 和 0.93**；加速的器官衰老在临床与遗传风险因素之外预测疾病发生、进展和死亡，其中脑衰老与死亡关联最强，精简蛋白面板仍保持性能 [6]。该研究指出部分器官可用蛋白少、因果机制有限 [6]。类似地，MSKAge 与 MSKAgeMort 在 21,070 名 UKB 参与者中构建，MSKAge 相关 r 女性=0.62、男性=0.56，MSKAgeMort 相关 r 女性=0.93、男性=0.88，其加速指标可预测死亡、肌肉骨骼病和年龄相关病 [38]。ECM 时钟则聚焦细胞外基质，用 **14 个血浆蛋白**建模，发现 ECM 蛋白随龄呈 U 型轨迹、最低点约 40-50 岁，但 Robbins 队列最老仅 66 岁、U 型轨迹较弱 [39]。

蛋白质组时钟的结局定义也在分化。HPS 不以年龄而以健康寿命为靶，基于 UKB Pharma Proteomics Project 的 **53,018 人**、2,920 个蛋白构建，随访 13.5 年，基线健康的 43,119 人中 12,427 人（**28.8%**）发生健康寿命终点事件，较低 HPS 与更高死亡风险和慢性阻塞性肺病等年龄相关疾病相关 [40]。该研究以欧洲裔为主、健康寿命定义尚无共识 [40]。疾病特异的思路则构建针对 **31 种**年龄相关疾病的蛋白复合评分，在 44,526 名 UKB 参与者中，疾病年龄差可将同龄人 10 年发病率区分达 **20 倍**，每增加 1 年差距使 2 型糖尿病风险升高 24%、慢性肾病 21% [41]。纵向数据方面，KORA 队列基于最多三个时间点的 LC-MS 血浆蛋白质组（9,105 样本、4,100 人、25-88 岁）构建时钟，发现心血管代谢暴露共享蛋白质组特征，而吸烟和体力活动具独特特征，个体内血脂异常和肾功能受损与年龄加速增加相关 [42]。

转录组时钟长期受平台依赖和组织特异性困扰。Pasta 以"年龄偏移"学习框架构建跨组织、跨数据类型的时钟，覆盖 bulk 与单细胞 RNA-Seq 及芯片数据，在比较中优于 **MultiTIMER 和 tAge**，能区分衰老、静息和干细胞状态，可分层肿瘤分级和生存，p53 相关基因贡献显著 [43]。该研究指出转录组噪声与批次效应仍限制跨平台泛化 [43]。DeepQA 则针对"仅在健康样本上训练、却在健康与非健康样本上推断"的固有偏倚，用混合专家与 Hinge-MAE 损失在 MCATS 数据库 3,060 样本、31 数据集上训练，报告在健康和非健康受试者上均显著优于现有方法 [44]；但非健康样本的生物年龄缺乏金标准 [44]。

大规模数据推动了转录组时钟精度的数量级变化。基于 ARCHS4 的混合专家模型使用 **56,877 例**人类 RNA-seq、覆盖 2-114 岁多组织，达到 **MAE=7.58 年**，肺和脑预测最佳、肝较差，FOSB 重要性 1.00、C4B_2 为 0.95、PAX8-AS1 为 0.85、MT-RNR2 为 0.64、GFAP 为 0.53，但残差随年龄增大，百岁老人误差达 ±40 年 [7]。K-Dense 多智能体系统在 ARCHS4 的 57,584 样本、28 组织、1,039 队列、1-114 岁数据上报告 **R²=0.854、MAE=4.26 年**，并提供校准置信区间以标记过渡期和极端年龄预测，识别 CDKN2A/p16、AMPD3、MIR29B2CHG、SEPTIN3 等阶段标志物 [45]。两项工作同样使用 ARCHS4 但样本数与误差不同，其差异来自模型与数据切分，不宜直接视为同一基准上的优劣。物种与组织扩展方面，小鼠肝脏时钟 LivAge 在早衰综合征中显示转录组年龄增加，并可评估 Snell Dwarf、Ames Dwarf、GHR 缺陷及热量限制等干预，但仅基于肝脏组织 [46]。

跨组学与跨物种的证据进一步界定时钟的边界。StackAge 整合 UKB **30,376 人**的 2,923 蛋白与 251 代谢物，与实际年龄 Pearson r≈0.93，对 2 型糖尿病、阿尔茨海默病和慢性肾病的 AUC 超过 0.90，但未整合表观遗传层且以横断面基线为主 [8]。代谢组时钟 MetaboAgeMort 在 UKB **239,291 人**中先选 185 个死亡相关代谢标志物，再用 LASSO Cox 与 Gompertz 回归建模，提升 10 年死亡预测并关联疾病、可调因素和遗传位点，但以全因死亡为替代指标、样本主要为欧洲白人 [47]。在犬中，基于 894 只犬的 1,640 份甲基化组构建的时钟可预测死亡率，生命早期表观遗传衰老最快，大体型和雄性犬寿命更短且分子衰老加速，体型相关变化集中于转座子元件、性别相关变化集中于 X 染色体 [48]。这些结果共同表明，单组学时钟的预测力已在多个分子层得到验证，但其生物学可靠性、跨组织外推与干预响应性仍是尚未解决的核心争议 [36][3][4]。

### 2.2 多模态整合与跨队列泛化

多模态整合的起点是把不同分子层与影像、临床表型分别训练成器官特异时钟，再在同一框架下比较。UK Biobank 血浆蛋白质组研究用 **2,916 种蛋白**、44,498 人训练出 11 个器官年龄模型，其中脑、动脉和整体年龄对传统年龄的预测 r²=0.97 [49]；同一队列的另一项工作用 2,448 种蛋白、43,498 人构建 11 个 ProtBAG，强调年龄偏倚校正与器官蛋白特异性，并报告整合多器官特征可提升系统性疾病和全因死亡预测 [16]。代谢组层面，274,247 人的 107 种非衍生代谢物被用于构建 5 个 MetBAG，独立测试集 Pearson r 为 0.25<r<0.42，关联 525 个疾病终点 [13]；MRI 层面则构建 7 个 MRIBAG，留出测试 Pearson r 0.23–0.77、MAE 约 5 年，并关联 2,923 种蛋白与 327 种代谢物 [14]。这些数字来自不同组学与不同研究设计，不能横向比高低，只能说明各模态内部预测精度差异较大。

跨队列泛化是这些工作共同的薄弱环节，且失败模式因模态而异。MRIBAG 的作者明确指出腹部 MRI 特征共线性导致泛化较差、脑模型在外部队列存在域偏移 [14]；表观遗传时钟方面，Horvath 与 PedBE 在 523 份墨西哥儿童青少年血样中预测准确性下降，迁移学习被用来缩小目标队列的差距 [50]。相对地，GOLD BioAge 以 Gompertz 风险函数构建轻量线性模型，并在 CHARLS、CLHLS、RuLAS 三个中国队列中验证有效 [51]；OMICmAge 则在 MGB 约 31,264 人开发后，于 All of Us 10,769、TruDiagnostic 14,213、Generation Scotland 18,672 等独立队列验证 [52]。可见泛化证据的强度取决于是否真正做了外部验证，而非模型复杂度。

多模态融合的收益在若干研究中被具体量化，但融合层次不同。ProtBAG 与 9 个表型年龄差时钟整合后提升了系统性疾病类别和全因死亡预测 [16]；CT 模型以 8 个心脏代谢影像标志物取得 IPA=29.2，优于人口学模型的 21.7（p<0.001），10 年 AUC=0.880 [15]；中国 mCAS 队列（2,019 名 18–91 岁）建立核心能力时钟、多模态时钟与器官时钟三层框架，并报告血浆蛋白时钟可代理系统生理能力、凝血因子年龄依赖积累驱动多器官衰老和炎症 [53]。10K 项目则从另一角度提示融合的必要性：男女衰老模式存在差异，较高 BA 评分与年龄相关疾病负担增加相关 [54]。

方法学争议集中在“预测偏差”与“不确定性”两个被长期忽视的维度。有研究指出常用 ML/AI 连续结局回归存在系统预测偏差并传播到下游关联，甚至产生“预测脑龄越大认知越好”“表观年龄越大肾功能越好”这类方向相反的虚假关联，约束优化可改善校准与下游推断 [24]；另一项工作用概率框架从预测年龄分布的均值与宽度导出 BAG 与生物年龄不确定性 BAU，在超过 45 万名 UK Biobank 参与者中发现 BAU 与 BAG 仅弱相关、并随个体分子间年龄信号不一致而增加 [25]。这与前述各时钟普遍只报告年龄差的做法形成张力：若偏差与不确定性未被建模，跨队列比较和下游关联都可能被扭曲。

应用侧的证据显示多模态时钟已进入干预评估与假设生成。一项特发性肺纤维化 12 周 2a 期试验比较 ProtAge、OrganAgemortality、OrganAgechrono、PAC、ipfP3GPT、PAOPAC 六种蛋白质组时钟，均一致预测治疗组生物年龄更低，但作者承认蛋白质组时钟无法单独区分衰老与疾病特异效应，需借助通路分析 [55]。ClockBase Agent 整合 40 余种衰老时钟、评估 43,602 个干预-对照比较，报告超 500 种干预显著降低生物年龄，并指出更多干预加速而非延缓衰老、疾病状态多加速生物年龄 [27]；AURORA 生成式多模态框架则通过降低年龄差的干预筛选预测 Neisseria flavescens 为顶级候选，并在线虫中验证活菌延长寿命和健康寿命 [28]。这些结果依赖已有时钟的预测，实验验证仍有限。

纵向与个体化维度是目前证据最薄弱的一环。上述多数时钟基于横断面年龄差，而一项纵向多组学研究仅以摘要说明其旨在刻画个体化衰老轨迹，未提供可提取的方法、数据规模与定量结果 [9]。这意味着“多模态整合”在横断面上已有蛋白、代谢、影像、临床多条证据链，但能否稳定追踪同一个体的衰老轨迹、并在跨队列迁移中保持校准，仍缺少直接证据；年龄偏倚校正、器官特异性定义与外部验证设计，是后续工作必须同时报告的三项前提 [16][14]。

### 2.3 单细胞与空间衰老图谱

单细胞转录组已被用于构建细胞类型特异的衰老时钟。sc-ImmuAging 基于 **1081 名 18 至 97 岁健康欧洲人** PBMC 的约 **130 万细胞**，用 LASSO、随机森林和 PointNet 为五类免疫细胞分别建模，内部与外部验证优于对照，并能揭示 COVID-19 感染后单核细胞和 BCG 接种后 CD8+T 细胞的年龄改变异质性 [56]。scAgeClock 则用门控多头注意力神经网络，在 CZ CELLxGENE 大规模单细胞转录组上训练，精度高于偏最小二乘、弹性网等基线，可在单细胞水平预测转录组年龄 [57]。另一项工作把单细胞转录组表示为基因名序列的“细胞句子”，微调预训练大语言模型，在数百万细胞上训练后实现单细胞分辨率年龄预测，并提名调控后降低预测转录年龄的候选靶点 [58]。这些时钟的差异主要在建模策略与数据来源，而非同一队列内的直接比较。

空间维度上，小鼠九组织的空间转录组显示衰老敏感斑点与组织结构熵升高共定位，免疫球蛋白表达细胞聚集是其微环境特征，**IgG** 在雄性和雌性小鼠的衰老组织中积累并在人组织观察到类似现象，靶向降低 IgG 可缓解小鼠多组织衰老 [20]。人皮肤的单细胞与空间转录组研究构建了 **SenSkin™** 皮肤特异衰老基因集，发现光老化的衰老细胞负担高于时序衰老，衰老黑素细胞黑色素合成升高、衰老网状真皮成纤维细胞胶原和弹性纤维合成下降 [21]。纹状体的 Slide-tags 单核空间转录组分析 **19 例死后供体、110 万细胞**，揭示纹状体一致分为六个区，每区由分子上不同的棘状投射神经元群体界定并具空间协调的神经元-星形胶质细胞互作网络，并借配套小鼠图谱推断衰老相关变化 [59]。

多组织图谱方面，小鼠乳腺的 scRNA-seq 与 snATAC-seq 比较 3 月龄与 18 月龄，发现上皮 AV/HS 减少、肌上皮增加，免疫髓系/浆细胞/记忆 T 增加、naive T 减少，成纤维细胞增加，并呈现衰老与癌症相关的表观与转录特征 [60]。人骨骼肌的单核 RNA+ATAC 多组学构建了首个衰老人肌衰老细胞图谱，解析 SASP 异质性与动态，并提出 Maraviroc 作为肌少症衰老治疗候选 [61]。内皮方面，HAECA 整合 **12 种人体组织、超 37.5 万个内皮细胞**，发现静脉内皮血管生成基因表达下降及细胞外基质和机械转导相关基因广泛改变 [62]。小鼠跨器官资源覆盖 **13 个器官、5 个年龄段、雌雄两性**，共 **93 只小鼠的 20,317,820 个细胞核**，默认核心集含 32 只野生型小鼠、11 个器官 [https://huggingface.co/datasets/transhumanist-already-exists/pansci-mouse-aging-snrna]。灵长类脑图谱覆盖 **11 个脑区、55 只 0.5–21 岁恒河猴、530 万细胞**，识别衰老耗竭的脆弱神经元群体及仅在单细胞分辨率可见的胶质细胞组成变化，其特征与阿尔茨海默病重叠 [63]。

细胞衰老的识别方法本身存在明显分歧。SenePy 用 **72 个小鼠和 64 个人类**加权单细胞转录组 signature 构建评分平台，发现其比体外来源 signature 更能重现体内衰老，Cdkn2a 等随龄增加（FDR p=0.01），但仅 **58/1540** 细胞类型组合的标志物重叠显著，说明标志物高度组织细胞特异 [18]。hUSI 从 **73 项**公开 RNA-seq 研究学习通用衰老特征，在 bulk 和单细胞多种条件下优于 **31 种**方法，并可用于 COVID-19 肺组织和黑色素瘤组织 [19]。两者取向相反：前者强调细胞类型特异，后者强调通用性，这一冲突尚未在统一基准下解决。综述亦指出，缺乏特异性标志物、衰老细胞稀少且异质动态，是细胞与组织层面理解衰老的主要障碍 [64]。

将衰老时钟推到细胞类型分辨率，可揭示同一组织内不同细胞的老化差异。在线虫中，BitAge 与 Stochastic Clock 预测 **128 种**神经元类型的生物年龄从约 **98h 到 177h**，近 2 倍差异，两时钟相关 Pearson **0.65**、P=5.5×10⁻¹⁷；较老神经元更易早期退化，翻译是驱动因素，丁香酸和 vanoxerine 可防止神经退化 [17]。脑衰老综述则从细胞类型中心视角总结年龄相关变化与细胞互作，并评述单细胞组学如何无偏评估年轻化干预 [65]。这些结果共同表明，生物年龄在细胞类型层面并不同步，但线虫结论向人类的外推仍需验证。

### 2.4 衰老生物学基准与基础模型

衰老生物学正从单一模态的“时钟”走向标准化基准与基础模型并存的评测体系。**LongevityBench** 构建了覆盖5个生物数据域的17项任务，评测来自6个开发团队的18个前沿AI系统，结论是**没有单一模型主导所有任务，组学年龄预测是最难的任务**；而微调的5个0.6B–9B参数多任务Longevity-LLM可匹配或超过更大的前沿系统[10]。与之呼应，Longevity-LLM v0.1将Qwen3-14B在DNA甲基化、蛋白质组、临床生物标志物和RNA表达上微调，强化微调后**表观年龄预测MAE为4.34年**，超过Horvath多组织时钟，蛋白质组谱生成显著优于所有前沿LLM[66]。单细胞层面则另有基准：评估10个通用单细胞基础模型、3个衰老专用模型及传统方法，覆盖5个生物学问题、超过250万单细胞转录组，冻结预训练表征时Geneformer在时序年龄预测和年龄伪时间一致性上最佳，但**2000个高变基因的平均表现更高**，多个模型在三种疾病背景中捕捉到正向分子年龄偏移[67]。表观时钟方向，ComputAgeBench以“可靠时钟应能区分健康个体与衰老加速疾病个体”为核心假设，整合**66个公开血液DNA甲基化数据集、覆盖19种疾病**，测试13个已发表模型，并另建46个数据集用于训练新时钟[22]。

方法学综述层面，多项工作把多组学与多模态融合视为主要演进方向，但证据性质多为叙述性。一篇综述梳理2016–2024年间125篇同行评审研究，总结CNN、RNN、GAN、LLM和扩散模型在衰老时钟、合成数据生成、药物发现和多模态健康评估中的应用，并自述缺乏定量荟萃分析[68]。另一篇认为AI、集成学习和深度学习推动临床衰老时钟在准确性、可解释性和泛化性方面进展，但全文不可得，具体数据、验证队列和定量性能无法提取[69]。系统综述则覆盖生物标志物选择、特征工程、模型开发、偏倚校正和性能评估，强调异步衰老与多模态融合，同时指出数据异质性、泛化性有限、可解释性不足和临床转化障碍[70]。生物年龄预测器与人类数字孪生的整合框架认为表观时钟预测生物年龄和健康表型最准确，数字孪生可动态模拟干预与风险，但落地受数据整合、隐私、互操作性和纵向建模挑战限制[71]。

争议与空白集中在“专用时钟”与“通用基础模型”的取舍及验证标准。Longevity-LLM的结果表明单一中等规模LLM可匹配或替代跨模态专用衰老时钟[66]，而LongevityBench强调组学年龄预测最难、无模型全能[10]，单细胞基准又显示简单的高变基因基线在平均表现上不逊于基础模型[67]，三者对基础模型相对优势的判断并不一致。验证层面，有观点文章主张AI评估干预应正确、有用、全面、可解释，并考虑因果、跨学科、标准、纵向数据和已知衰老生物学，建议LLM结合知识图谱与检索增强生成并开展基准测试，但未提供具体实验验证或定量结果[72]；ComputAgeBench则仅基于血液DNA甲基化、未覆盖其他模态，且未提供具体模型性能数值[22]。

### 2.5 类器官、扰动与 Cell Painting 衰老建模

在细胞衰老建模的扰动筛选一侧，转录组年龄预测器已被用于指导重编程因子的发现：研究在人成纤维细胞中构建可解释的转录组年龄预测器，并据此开展 cDNA 过表达筛选，鉴定出 RNA 加工与剪接因子 **SRSF1**，其诱导可产生强烈的年轻化转录特征且不丧失细胞身份，体外实验显示可恢复年轻表型 [26]。该工作以预测器输出的年龄作为筛选基准，属于单一细胞类型的体外模型，样本规模与体内验证均未提及 [26]。

在成像表型一侧，Cell Painting 作为 2013 年提出的显微细胞标记 assay，旨在捕获细胞状态并优化图像型 profiling，十年来其协议、特征提取、质控与批次校正持续改进，已用于机制、毒性和多组学整合等场景 [29]。两篇证据分属转录组扰动筛选与图像型 profiling 两条技术路线，前者提供了可解释年龄预测器驱动的因子发现实例，后者为综述、未提供统一定量基准，二者尚未在同一研究内被直接比较，成像表型能否支撑类似的衰老重编程筛选仍无证据 [29][26]。

### 2.6 跨物种与跨组织衰老标志（脂质组等）

跨物种、多组织脂质组学比较显示，**脂酰链延长**是小鼠、线虫、果蝇和人类衰老的保守标志；人类心脏病进展中也出现类似的脂质延长，而饮食限制可缩短小鼠心脏脂质 [73]。衰老在脂质组层面并非单一脂质升降，而是表现为向长链脂质转变并伴随短链脂质耗竭的**比值性重塑** [73]。

在机制层面，该研究鉴定出脂质重塑因子 **Plb1** 参与调控上述脂质重塑过程 [73]。上述证据覆盖小鼠、线虫、果蝇与人类多组织，并以饮食限制小鼠心脏脂质作为对照，提示脂酰链长度变化可作为跨物种、跨组织的衰老相关标志 [73]。

## 3 数据与资源

在数据资源层面，现有工作主要沿两条路径推进：一是面向衰老标志物统一整理与评估的通用框架，二是聚焦免疫衰老的多组学专门数据库。**Biolearn** 作为开源库，针对跨人群验证缺乏标准化方法、标志物设计分散、数据集结构不一致等问题，提供整理、协调与系统评估的统一框架，并基于多公开数据集与多种衰老生物标志物开展评估，输出可复现的标准化格式与性能、稳健性、泛化性比较 [23]。其局限在于依赖已有公开数据，临床验证仍待推进 [23]。与之互补，**Immunosenescence Inventory** 面向免疫衰老，整合单细胞转录组、bulk转录组、表观组及 TCR/BCR 等多物种数据，提供知识 curation、多模态数据集与工具，支持免疫细胞识别和**免疫时钟**计算，用于评估生物年龄、预测年龄相关疾病及干预影响 [74]。

两者的差异体现在覆盖范围与评估取向上：Biolearn 以跨数据集、跨人群的标志物系统比较为核心，强调可复现的评估流程 [23]；Immunosenescence Inventory 则以免疫系统为切口，将多模态数据与免疫时钟工具整合于开放获取数据库，并对标 ImmPort、InnateDB、Aging Atlas 等既有数据库 [74]。需要指出的是，后者未提供统一预测性能基准，单细胞免疫衰老覆盖仍有限 [74]，因此其工具输出与 Biolearn 框架下的标志物评估结果之间尚缺乏可直接对照的基准，二者在“数据整合”与“性能验证”上的分工仍是当前资源建设的争议与空白所在。

## 4 应用与结果

在死亡预测这一子问题上，证据链从单一年龄差指标扩展到多队列荟萃。四个老年人纵向队列的分析显示，**Δage每高5年全因死亡风险增加21%，校正健康、生活方式与APOE后仍增加16%**，且Δage遗传度为0.43 [75]。随后扩展到**13个队列13,089人、2,734例死亡**，比较Horvath 353 CpG与Hannum 71 CpG时钟，表观年龄与实足年龄相关系数0.65–0.89，年龄加速与全因死亡风险升高相关，且纳入血液细胞组成信息可提升预测 [76]。两项工作结论方向一致，但后者强调细胞组成是混杂与改进来源，前者未展开此点。

在人群差异与暴露因素上，研究把时钟用作比较工具而非单纯预测器。整合血液、唾液、淋巴细胞和脑组织的353 CpG时钟分析发现表观年龄加速存在种族/民族与性别差异，并与冠心病及相关风险因素相关，但以横断面为主、组织来源异质 [77]。HIV感染方面，11个甲基化数据集的血液与脑组织比较显示感染者表观年龄加速显著增加，样本量与横断面设计限制因果解读 [78]。Lothian Birth Cohort 1936（70岁n=920、73岁n=299、76岁n=273）则给出方向不同的结果：**表观年龄加速与70岁步行速度、握力、肺功能、认知横断面相关，但不预测70至76岁间的功能下降** [79]，提示横断面关联未必延伸为纵向变化预测。系统综述层面，299篇文献、1050个EAA-因素关联、53种时钟的随机效应荟萃分析确认若干EAA与生理、认知、社会和环境因素存在显著汇总关联，并建立四级分类与TEAPEE数据库，但研究异质性大、因果方向不明 [80]。

干预与可塑性证据集中在器官与灵长类层面。异时心脏移植的多组学分析（小鼠与患者）显示**移植心脏的生物年龄快速同化受体年龄**，且该效应仅限移植物、不影响受体全身生物年龄，全文尚未公开、样本规模未说明 [81]。40个月二甲双胍干预雄性食蟹猴的研究构建了多组织转录组、DNA甲基化、血浆蛋白与代谢组的猴衰老时钟，**脑衰老约回退6年**，并观察到脑结构保护与认知增强，部分由Nrf2激活介导，但仅限雄性食蟹猴、人类转化待验证 [82]。临床结局方向仅有一项提出干细胞衰老时钟连接生物学年龄偏差与急性髓系白血病临床结局，具体定量结果与验证细节未在提供文本中给出 [83]。

## 5 评测、可复现性与争议

（本节暂无入库证据）

## 6 空白与趋势

多模态整合的现状是“各模态分别建时钟、再在同一框架下比较”，而非真正的联合表征学习。蛋白、代谢、影像、临床表型各自已有器官特异时钟，但融合多发生在评分层：ProtBAG 与 9 个表型年龄差时钟整合后提升系统性疾病和全因死亡预测 [16]，CT 模型以 8 个影像标志物取得 IPA=29.2 优于人口学模型 21.7 [15]，mCAS 队列建立核心能力、多模态与器官三层框架 [53]。**尚无证据表明存在端到端跨模态对齐的衰老表征模型**；缺失模态下的时钟推断、模态间年龄信号冲突的处理，均未见专门方法。年龄偏倚校正、器官特异性定义与外部验证设计被明确列为后续工作必须同时报告的三项前提 [16][14]。

纵向与个体化维度是证据最薄弱的一环。多数时钟基于横断面年龄差，纵向多组学工作仅以摘要说明其刻画个体化衰老轨迹，未提供可提取的方法、规模与定量结果 [9]。Lothian 队列的结果直接提示横断面关联未必延伸为纵向预测：表观年龄加速与 70 岁体能认知横断面相关，却不预测 70 至 76 岁间的功能下降 [79]。**“同一个体的衰老速率能否被稳定追踪、并在跨队列迁移中保持校准”仍缺直接证据**；增量学习、纵向校准、个体内变异分解在衰老时钟语境下基本空白。

可靠性研究正在从“预测精度”转向“偏差与不确定性”，但尚未进入常规报告。有研究指出常用 ML/AI 连续结局回归存在系统预测偏差并传播到下游关联，可产生方向相反的虚假关联，约束优化可改善校准 [24]；概率框架从预测年龄分布导出 BAG 与生物年龄不确定性 BAU，在超过 45 万 UKB 参与者中发现 BAU 与 BAG 仅弱相关 [25]。跨组织外推同样受质疑：83 人、284 份五类组织样本中口腔与血液表观年龄平均差近 30 年 [3]。**偏差建模与不确定性量化尚未成为时钟发表的标配**，这使跨队列比较和干预效应解读都可能被扭曲。

基准与基础模型的判断彼此不一致，构成当前最尖锐的争议。LongevityBench 覆盖 5 个数据域 17 项任务、评测 18 个前沿系统，结论是没有单一模型全能、组学年龄预测最难 [10]；Longevity-LLM v0.1 则报告强化微调后表观年龄预测 MAE=4.34 年、超过 Horvath 多组织时钟 [66]；单细胞基准又显示冻结预训练表征时 Geneformer 在时序年龄预测最佳，但 2000 个高变基因的平均表现更高 [67]。ComputAgeBench 以“区分健康与衰老加速疾病”为核心假设，整合 66 个血液 DNA 甲基化数据集、19 种疾病、测试 13 个模型，但仅覆盖血液甲基化、未给具体性能数值 [22]。**专用时钟与通用基础模型谁更优，目前取决于基准选择而非稳健结论**；跨模态统一基准、以及把干预响应性纳入基准的设计仍属空白。

细胞与空间分辨率的衰老建模已能揭示同一组织内的不同步老化，但识别方法本身存在取向冲突。SenePy 用 72 个小鼠和 64 个人类 signature 构建评分，发现仅 58/1540 细胞类型组合的标志物重叠显著，强调高度细胞类型特异 [18]；hUSI 从 73 项研究学习通用特征、优于 31 种方法 [19]。线虫中 BitAge 与 Stochastic Clock 预测 128 种神经元类型生物年龄从约 98h 到 177h、近 2 倍差异 [17]。**“通用衰老特征”与“细胞类型特异特征”的冲突尚未在统一基准下解决**，而人类细胞类型分辨率的衰老时钟仍主要限于免疫与乳腺等少数组织 [56][60]。

扰动与类器官体系中的衰老建模是最接近“因果验证”的方向，但证据零散。转录组年龄预测器已驱动 cDNA 过表达筛选，鉴定出 SRSF1 可产生强烈年轻化转录特征且不丧失细胞身份 [26]；Cell Painting 作为图像型 profiling 的协议与质控持续改进，已用于机制与多组学整合 [29]；ClockBase Agent 整合 40 余种时钟、评估 43,602 个干预-对照比较，报告超 500 种干预显著降低生物年龄 [27]；AURORA 生成式框架预测 Neisseria flavescens 并在线虫验证延长寿命 [28]。**成像表型能否支撑类似的重编程筛选、类器官时钟能否作为干预替代终点，均无直接证据** [29][26]；现有扰动筛选多以预测器输出为基准，缺少与真实衰老表型的独立对照。

数据资源与评估框架正在成形，但“整合”与“验证”仍分工而非合一。Biolearn 提供标志物整理、协调与系统评估的统一框架，输出可复现的性能、稳健性与泛化性比较，局限是依赖已有公开数据、临床验证待推进 [23]；Immunosenescence Inventory 整合单细胞、bulk、表观组及 TCR/BCR 多物种数据并支持免疫时钟计算，但未提供统一预测性能基准、单细胞免疫衰老覆盖有限 [74]。**两类资源之间尚缺乏可直接对照的基准**，跨资源、跨模态的标志物可比性仍是空白。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 单组学衰老时钟（表观/蛋白/转录） | 成熟（表观）/ 朝阳（蛋白、转录） | 表观时钟方法已高度收敛：Horvath 2013 多组织甲基化年龄 [1] 与 PhenoAge [11] 奠定了系数公开、跨队列复现的范式，后续多为增量（如因果富集表观年龄 [12]）。蛋白组时钟 [5] 近两年才出现大规模死亡率/疾病预测验证，方法仍在快速迭代，属朝阳。 |
| 2.2 多模态整合与跨队列泛化 | 朝阳 | 雷达样本中该节 **n=16、近两年占比 0.92、CNS 占比 0.56**，但方法未收敛：血浆蛋白组连接脑-免疫衰老 [49] 与 MRI 多器官时钟 [14] 代表两条不同的整合路线（分子 vs 影像），表型组性别特异动态 [54] 又提出跨队列校正问题，尚无统一对齐/缺失模态框架。 |
| 2.3 单细胞与空间衰老图谱 | 朝阳 | 空间转录组揭示免疫球蛋白相关衰老 [20] 与单细胞免疫衰老时钟揭示个体异质性 [56] 均为近两年高影响工作，但前者是图谱描述、后者是时钟建模，细胞类型特异衰老景观 [18] 与乳腺单细胞图谱 [60] 说明数据在快速积累而建模口径（衰老细胞定义、跨组织可比性）尚未统一。 |
| 2.4 衰老生物学基准与基础模型 | 萌芽 | 仅 **n=9、median citations=0**，且以观点/综述为主：AI 干预评估的验证要求 [72] 与数字孪生综述 [71] 属框架讨论；唯一实质基准 ComputAgeBench [22] 刚出现（9 次引用），说明基准化才起步、尚无领域公认 benchmark 与基础模型。 |
| 2.5 类器官、扰动与 Cell Painting 衰老建模 | 证据不足 | 雷达样本仅 **n=2**：Cell Painting 十年综述 [29] 是成像方法学总结而非衰老建模，转录组重编程筛选 SRSF1 [26] 是扰动筛选但未做衰老时钟建模；两篇均不能支撑「类器官衰老建模」已成方向，故判证据不足（可能是证据挂到别节）。 |
| 2.6 跨物种与跨组织衰老标志（脂质组等） | 证据不足 | 雷达样本仅 **n=1**：长链脂质标记衰老并约束寿命 [73]，单篇无法判断阶段。 |
| 3 数据与资源 | 萌芽 | **n=2**：衰老生物标志统一 curation/评估框架 [23] 与免疫衰老多组学数据库 [74] 说明资源层刚出现标准化尝试，但规模与复用度尚低。 |
| 4 应用与结果 | 成熟 | 甲基化年龄预测全因死亡 [75]、预测寿命的 meta 分析 [76]、种族/性别/冠心病分析 [77] 构成大量高引用应用验证，属方法已定后的增量应用；但该节 **近两年占比仅 0.22**，说明新意主要在别处。 |
| 5 评测、可复现性与争议 | 证据不足 | 雷达样本 **n=0**，无证据可判。 |

**整体判断**：这个方向整体处于**朝阳期偏早段**——单组学表观时钟已成熟（[1]、[11]），但**多模态整合（2.2）与单细胞/空间（2.3）近两年才爆发且方法未收敛**（雷达样本中 2.2 近两年占比 **0.92**、CNS 占比 **0.56**；2.3 CNS 占比 **0.62**），而**基准与基础模型（2.4）仍是萌芽**（median citations **0**，仅 ComputAgeBench [22]）。窗口期估计 **1–2 年**：多模态对齐/缺失模态/跨队列校正尚无公认方案，谁先给出可复现框架谁占位。最大不确定性是**评测口径缺失**——没有统一 benchmark 与衰老细胞/生物年龄金标准（[72]、[23] 只是呼吁与初步框架），导致方法间不可比、易被后续基准工作替代。

**接下来怎么做**：
1. **做「多模态缺失模态 + 跨队列校正」的通用框架，用公共数据 demo**：以甲基化+蛋白组+影像公共队列为骨架，方法上做模态对齐与缺失模态插补、跨队列批次校正，产出可复现 pipeline 与开源系数。现在做是因为 2.2 方法未收敛且 CNS 密集（[49]、[14]），但都各做各的模态，缺统一对齐层；同时可对接你的公共数据 demo 合作。
2. **把单细胞/空间衰老图谱转成「细胞类型特异时钟」并做跨组织可比性**：用公开单细胞/空间衰老图谱训练细胞类型分辨的衰老评分，重点解决衰老细胞定义与跨组织校准。现在做是因为图谱数据已足（[20]、[18]）但时钟建模仅个别工作（[56]），方法空白明显。
3. **抢先做衰老时钟的基准层（benchmark + 评测协议）**：整合公开系数与数据，定义跨队列泛化、缺失模态、纵向增量三类评测任务，产出 benchmark 与 leaderboard。现在做是因为 2.4 仅 ComputAgeBench [22] 一篇且引用极低，验证要求讨论已出现（[72]），先发者定义口径；这与你多模态建模能力直接匹配。
4. **把类器官+多组学合作项目做成「扰动体系中的衰老建模」**：在类器官扰动/重编程筛选中嵌入转录组或影像衰老评分，做年轻化/衰老加速的定量建模。现在做是因为该细分在雷达样本中**证据不足（n=2）**，Cell Painting 方法学已成熟（[29]）、扰动筛选有先例（[26]），但无人把它接成衰老时钟——正是你合作项目的差异化切口，风险是需自建标注。
5. **用统一 curation 框架做数据资源侧贡献，作为上述工作的底座**：按 [23] 的评估框架与 [74] 的多组学资源，整理可复现的衰老时钟数据/系数库。现在做是因为资源层仅 **n=2** 且刚起步，成本低、复用高，能为 1–3 条提供数据与评测支撑。

## 参考文献

1. DNA methylation age of human tissues and cell types. Genome Biology 2013. https://doi.org/10.1186/gb-2013-14-10-r115
2. An unbiased comparison of 14 epigenetic clocks in relation to 174 incident disease outcomes.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66106-y
3. Cross-tissue comparison of epigenetic aging clocks in humans.. Aging cell 2025. https://doi.org/10.1111/acel.14451
4. Responsiveness of epigenetic aging biomarkers to longevity interventions in humans.. Nature medicine 2026. https://doi.org/10.1038/s41591-026-04562-9
5. Proteomic aging clock predicts mortality and risk of common age-related diseases in diverse populations. Nature Medicine 2023. https://doi.org/10.1038/s41591-024-03164-7
6. Organ-specific proteomic aging clocks predict disease and longevity across diverse populations.. Nature aging 2025. https://doi.org/10.1038/s43587-025-01016-8
7. Transcriptomic age prediction using mixture-of-experts models reveals tissue-specific aging signatures in large-scale human RNA-sequencing data. medRxiv 2025. https://doi.org/10.1101/2025.06.28.25330474
8. StackAge: an ensemble-based clock for precise quantification of biological age using multi-omics data.. Briefings in bioinformatics 2026. https://doi.org/10.1093/bib/bbag271
9. Longitudinal multiomics reveals personalized aging trajectories.. Nature aging . https://doi.org/10.1038/s43587-026-01248-2
10. An open benchmark and language models for AI in aging biology.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.026
11. An epigenetic biomarker of aging for lifespan and healthspan. bioRxiv 2018. https://doi.org/10.18632/aging.101414
12. Causality-Enriched Epigenetic Age Uncouples Damage and Adaptation. bioRxiv 2023. https://doi.org/10.1038/s43587-023-00557-0
13. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
14. MRI-based multi-organ clocks for healthy aging and disease assessment.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03999-8
15. Biological age model using explainable automated CT-based cardiometabolic biomarkers for phenotypic prediction of longevity.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56741-w
16. Refining the generation, interpretation and application of multi-organ, multi-omics biological aging clocks.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00928-9
17. Aging clocks delineate neuron types vulnerable or resilient to neurodegeneration and identify neuroprotective interventions.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01067-5
18. Unveiling the cell-type-specific landscape of cellular senescence through single-cell transcriptomics using SenePy.. Nature communications 2025. https://doi.org/10.1038/s41467-025-57047-7
19. A transcriptome-based human universal senescence index (hUSI) robustly predicts cellular senescence under various conditions.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00886-2
20. Spatial transcriptomic landscape unveils immunoglobin-associated senescence as a hallmark of aging.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.019
21. Mapping epidermal and dermal cellular senescence in human skin aging.. Aging cell 2024. https://doi.org/10.1111/acel.14358
22. ComputAgeBench: Epigenetic Aging Clocks Benchmark. bioRxiv 2025. https://doi.org/10.1145/3711896.3737382
23. A unified framework for systematic curation and evaluation of aging biomarkers.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00987-y
24. Trustworthy ML/AI for Aging Clocks: Preventing Systematic Prediction Bias in Biological Age Estimation. bioRxiv 2026. https://doi.org/10.64898/2026.05.27.728155
25. Uncertainty redefines biological age.  . https://doi.org/10.64898/2026.09.26.26364091
26. Transcriptomic reprogramming screen identifies SRSF1 as a regulator of aging.. Nature aging . https://doi.org/10.1038/s43587-026-01234-8
27. Autonomous AI Agents Discover Aging Interventions from Millions of Molecular Profiles. bioRxiv 2025. https://doi.org/10.1101/2023.02.28.530532
28. Multi-modality profiling identifies Neisseria flavescens as a central geroprotective oral commensal in humans.. Nature aging . https://doi.org/10.1038/s43587-026-01220-0
29. Cell Painting: a decade of discovery and innovation in cellular imaging.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02528-8
30. Epigenetic clocks and programmatic aging.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102546
31. LinAge2: providing actionable insights and benchmarking with epigenetic clocks.. npj aging 2025. https://doi.org/10.1038/s41514-025-00221-4
32. Decoding disease-specific ageing mechanisms through pathway-level epigenetic clock: insights from multi-cohort validation.. EBioMedicine 2025. https://doi.org/10.1016/j.ebiom.2025.105829
33. Enhancing the performance and interpretability of epigenetic clocks.. Nucleic acids research 2026. https://doi.org/10.1093/nar/gkag661
34. Characterising developmental dynamics of adult epigenetic clock sites.. EBioMedicine 2024. https://doi.org/10.1016/j.ebiom.2024.105425
35. SARDINE unlocks EWAS summary statistics for large-scale epigenetic biomarker analysis.  . https://doi.org/10.64898/2026.11.05.763758
36. Biological Versus Technical Reliability of Epigenetic Clocks and Implications for Disease Prognosis and Intervention Response.. Aging cell 2026. https://doi.org/10.1111/acel.70635
37. Proteomic aging clock (PAC) predicts age‐related outcomes in middle‐aged and older adults. Aging Cell 2024. https://doi.org/10.1111/acel.14195
38. Construction and Validation of Plasma Protein-Based Musculoskeletal Biological Age and Genetic and Environmental Risk Profiles.. Aging cell 2026. https://doi.org/10.1111/acel.70636
39. An Extracellular Matrix Aging Clock Based on Circulating Matrisome Proteins Predicts Biological Aging and Disease.. Aging cell 2026. https://doi.org/10.1111/acel.70474
40. A proteomic signature of healthspan.. Proceedings of the National Academy of Sciences of the United States of America 2025. https://doi.org/10.1073/pnas.2414086122
41. Disease aging clocks in the plasma proteome stratify risk and track preclinical progression.  . https://doi.org/10.21203/rs.3.rs-10675323/v1
42. Intraindividual longitudinal changes of the proteome reveal dynamic markers of biological aging.  . https://doi.org/10.64898/2026.10.01.755909
43. Pasta, a Versatile Transcriptomic Clock, Maps the Chemical and Genetic Determinants of Aging and Rejuvenation. bioRxiv 2025. https://doi.org/10.1002/advs.76740
44. DeepQA: A Unified Transcriptome-Based Aging Clock Using Deep Neural Networks.. Aging cell 2025. https://doi.org/10.1111/acel.14471
45. Guided multi-agent AI invents highly accurate, uncertainty-aware transcriptomic aging clocks. bioRxiv 2025. https://doi.org/10.1101/2025.09.08.674588
46. LivAge: An Online Aging Clock for Murine Transcriptomic Age Estimation.. Aging cell 2026. https://doi.org/10.1111/acel.70677
47. A Novel Metabolomic Aging Clock Predicting Health Outcomes and Its Genetic and Modifiable Factors. Advancement of science 2024. https://doi.org/10.1002/advs.202406670
48. Epigenetic aging and transposon dysregulation reflect size-related lifespan compression in dogs.. Science (New York, N.Y.) . https://doi.org/10.1126/science.aeb2986
49. Plasma proteomics links brain and immune system aging with healthspan and longevity.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03798-1
50. BRIDGING THE GAP: ENHANCING THE GENERALIZABILITY OF EPIGENETIC CLOCKS THROUGH TRANSFER LEARNING.. The annals of applied statistics 2026. https://doi.org/10.1214/26-aoas2136
51. Gompertz Law-Based Biological Age (GOLD BioAge): A Simple and Practical Measurement of Biological Ageing to Capture Morbidity and Mortality Risks.. Advanced science (Weinheim, Baden-Wurttemberg, Germany) 2025. https://doi.org/10.1002/advs.202501765
52. OMICmAge quantifies biological age by integrating multi-omics with electronic medical records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01073-7
53. Multimodal clocks of human aging.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.025
54. Phenome-wide associations of human aging uncover sex-specific dynamics.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00734-9
55. Integration of proteomic aging clocks in a phase 2a clinical trial supports simultaneous geroprotective assessment.. Nature Biotechnology 2026. https://doi.org/10.1038/s41587-026-03286-y
56. Single-cell immune aging clocks reveal inter-individual heterogeneity during infection and vaccination.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00819-z
57. scAgeClock: a single-cell transcriptome-based human aging clock model using gated multi-head attention neural networks.. npj aging 2026. https://doi.org/10.1038/s41514-026-00379-5
58. Universal Single-Cell Transcriptomic Aging Clock powered by LLMs reveals targets to slow cellular aging. Innovation in aging 2025. https://doi.org/10.1093/geroni/igaf122.4305
59. Mesoscale molecular architecture of the striatum across cell types and adult aging.. Cell . https://doi.org/10.1016/j.cell.2026.10.029
60. Comprehensive single-cell aging atlas of healthy mammary tissues reveals shared epigenomic and transcriptomic signatures of aging and cancer.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00751-8
61. Multiomics and cellular senescence profiling of aging human skeletal muscle uncovers Maraviroc as a senotherapeutic approach for sarcopenia.. Nature communications 2025. https://doi.org/10.1038/s41467-025-61403-y
62. Uncovering the transcriptional hallmarks of endothelial cell aging via integrated single-cell analysis.. Nature aging . https://doi.org/10.1038/s43587-026-01247-3
63. Single-cell, multi-region profiling of the macaque brain across the lifespan.. Cell . https://doi.org/10.1016/j.cell.2026.09.014
64. Advancing biological understanding of cellular senescence with computational multiomics.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02314-y
65. Brain aging and rejuvenation at single-cell resolution.. Neuron 2025. https://doi.org/10.1016/j.neuron.2024.12.007
66. The End of Aging Clocks: Training Foundation Models to Reason in Aging and Longevity. bioRxiv 2026. https://doi.org/10.64898/2026.03.28.714980
67. Benchmarking single-cell foundation models for aging biology.  . https://doi.org/10.64898/2026.09.21.753191
68. Deep learning and generative artificial intelligence in aging research and healthy longevity medicine.. Aging 2025. https://doi.org/10.18632/aging.206190
69. The Evolving Landscape of Clinical Aging Clocks: From Epigenetic to Multi-Omics Integration.. Aging cell 2026. https://doi.org/10.1111/acel.70579
70. Artificial intelligence approaches in biological age prediction: current status and challenges.. British journal of biomedical science 2026. https://doi.org/10.3389/bjbs.2026.16141
71. From ageing clocks to human digital twins in personalising healthcare through biological age analysis.. NPJ digital medicine 2025. https://doi.org/10.1038/s41746-025-01911-9
72. Validation Requirements for AI-based Intervention-Evaluation in Aging and Longevity Research and Practice. Ageing Research Reviews 2024. https://doi.org/10.1016/j.arr.2024.102617
73. Longer lipids mark aging and constrain lifespan.. Nature aging . https://doi.org/10.1038/s43587-026-01223-x
74. Immunosenescence Inventory-a multi-omics database for immune aging research.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1102
75. DNA methylation age of blood predicts all-cause mortality in later life. Genome Biology 2015. https://doi.org/10.1186/s13059-015-0584-6
76. DNA methylation-based measures of biological age: meta-analysis predicting time to death. Aging 2016. https://doi.org/10.18632/aging.101020
77. An epigenetic clock analysis of race/ethnicity, sex, and coronary heart disease. Genome Biology 2016. https://doi.org/10.1186/s13059-016-1030-0
78. HIV-1 Infection Accelerates Age According to the Epigenetic Clock. Journal of Infectious Diseases 2015. https://doi.org/10.1093/infdis/jiv277
79. The epigenetic clock is correlated with physical and cognitive fitness in the Lothian Birth Cohort 1936. International Journal of Epidemiology 2015. https://doi.org/10.1093/ije/dyu277
80. Breaking new ground on human health and well-being with epigenetic clocks: A systematic review and meta-analysis of epigenetic age acceleration associations.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102552
81. Transplanted hearts assimilate the recipient’s biological age. bioRxiv 2026. https://doi.org/10.64898/2026.09.15.751836
82. Metformin decelerates aging clock in male monkeys.. Cell 2024. https://doi.org/10.1016/j.cell.2024.08.021
83. A stem cell aging clock links biological age deviation to clinical outcome in acute myeloid leukemia. bioRxiv 2026. https://doi.org/10.64898/2026.02.12.703707
84. A blood-based epigenetic clock for intrinsic capacity predicts mortality and is associated with clinical, immunological and lifestyle factors.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00883-5
85. [dataset] transhumanist-already-exists/pansci-mouse-aging-snrna.  . https://huggingface.co/datasets/transhumanist-already-exists/pansci-mouse-aging-snrna
