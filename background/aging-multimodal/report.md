# 多模态衰老时钟与生物年龄 · 方向背景报告

证据 79 篇 · 覆盖度 0.60 · 第 8 轮 · 更新 2026-10-25 · 数字核验删句 1

## 本次变更

- 新增 [47] Transcriptomic reprogramming screen identifies SRSF1 as a regulator of aging.

## 摘要（TL;DR）

- Horvath 多组织时钟整合 82 个数据集、7844 个非癌样本，从 21,369 个共有 CpG 中选出 353 个 CpG，多数组织预测误差约 3.6 年 [1]。
- Generation Scotland 队列 18,859 人、174 种新发疾病、10 年随访的无偏比较显示第二、三代时钟显著优于第一代，完全校正模型下 13 种时钟与 57 种疾病共 176 个 Bonferroni 显著关联 [2]。
- 83 人、284 份口腔与血液样本的跨组织比较显示口腔与血液组织表观年龄平均差近 30 年，多数血液时钟与口腔组织相关性低 [3]。
- UK Biobank 基于 2,897 个血浆蛋白、45,441 人训练的蛋白质组年龄时钟经 Boruta 筛选 204 个蛋白，与实际年龄 Pearson r=0.94 [4]。
- 基于 ARCHS4 56,877 例、2–114 岁多组织 RNA-seq 的混合专家模型报告 MAE=7.58 年，但极端年龄方差大、百岁老人误差达 ±40 年 [5]；K-Dense 在 ARCHS4 57,584 样本上报告 R²=0.854、MAE=4.26 年 [6]。
- OMICmAge 以 Mass General Brigham Biobank 约 31,000 人开发 EMRAge，并在 All of Us 10,769、TruDiagnostic 14,213、Generation Scotland 18,672 等独立队列验证 [7]。
- LongevityBench 覆盖 5 个生物数据域、17 项任务，评测 6 个开发团队的 18 个前沿 AI 系统，结论是没有单一模型能主导所有任务且组学年龄预测是最难的任务 [8]。
- ComputAgeBench 整合 66 个公开血液 DNA 甲基化数据集、覆盖 19 种衰老加速疾病，测试 13 个已发表表观遗传时钟模型，但仅基于血液 DNA 甲基化且未给出具体模型性能数值 [9]。
- 四个老年人纵向队列的荟萃分析显示 Δage 每高 5 年全因死亡风险增加 21%，校正健康、生活方式与 APOE 后仍增加 16%，且 Δage 遗传度为 0.43 [10]。
- Lothian Birth Cohort 1936 在 70 岁（n=920）、73 岁（n=299）、76 岁（n=273）三波测量中发现表观年龄加速与 70 岁功能横断面相关，但不预测 70 至 76 岁间的功能下降 [11]。

## 1 背景与定义

表观遗传时钟的演化脉络显示，该方向已从「预测实际年龄」转向「预测结局与机制」。第一代以 Horvath 353 CpG 为代表，确立跨组织年龄预测可行性 [1]；第二代以 PhenoAge 为代表，改用临床表型复合指标训练 [12]；第三代则进一步分化出疾病预测导向（GrimAge v2、DunedinPACE 在 174 种疾病比较中关联最强）[2]、因果分解导向（DamAge/AdaptAge 区分损伤性与适应性甲基化变化）[13] 与通路级解释导向（PathwayAge 放弃单 CpG 改用 GO/KEGG 通路）[14]。**这一分化本身构成该方向的核心张力：预测精度、机制可解释性与因果有效性三者尚未在同一模型中统一。** 同时，跨组织可比性（口腔与血液表观年龄平均差近 30 年）[3] 与发育起源（超过三分之一时钟位点自出生即有个体差异）[15] 的发现，说明「生物年龄」这一构念本身仍需更严格的操作化定义。

蛋白组与转录组时钟的扩张把方向边界从「单一分子层」推向「多器官、多平台」。蛋白组侧已形成 UKB 平台上的多条并行路线：整体蛋白组时钟（2,897 蛋白、45,441 人，筛选 204 蛋白）[4]、PAC（2,923 蛋白、53,021 人）[16]、十器官系统时钟（2,916 蛋白、43,616 人，跨队列 r=0.98 与 0.93）[17]，以及面向特定表型的 HPS [18]、ECM 时钟（14 蛋白）[19]、MSKAge [20] 与纵向 KORA 时钟 [21]。转录组侧则以 Pasta 的跨平台 age-shift 框架 [22]、DeepQA 对健康/非健康样本偏倚的处理 [23] 与 ARCHS4 大规模模型（MAE=7.58 年 vs R²=0.854、MAE=4.26 年）[5][6] 为代表。**这些工作共同表明，单组学时钟的「可用性」已基本建立，但其性能高度依赖所选分子子集、训练平台与目标表型，跨面板、跨平台的性能不可通约。**

多模态整合目前主要停留在「同队列内并行建模 + 事后整合」阶段，而非真正的模态对齐。UKB 体系下的 11 器官蛋白时钟 [24]、11 个 ProtBAG 与 9 个表型年龄差的整合 [25]、5 个 MetBAG（274,247 人）[26]、7 个 MRIBAG（313,645 人）[27] 与 CTBA（123,281 人）[28] 各自建立了模态内的器官分辨率，但跨模态的证据多为关联（如 MRIBAG 关联 2,923 蛋白与 327 代谢物），而非联合训练。真正跨组学联合建模的代表是 OMICmAge（多组学子集生成 DNAmEMRAge 与 OMICmAge，并在 All of Us、TruDiagnostic、Generation Scotland 验证）[7] 与中国 mCAS 队列的三层框架 [29]。**关键空白在于：尚无同一外部队列对上述多模态时钟做头对头比较，模态间的增量信息量因而无法被量化。**

跨队列泛化与不确定性量化正成为方法学焦点。迁移学习证据显示 Horvath 与 PedBE 在墨西哥儿童青少年队列中准确性下降，Kriging 与 DNN 特征适配可缩小差距 [30]；方法学工作指出 ML/AI 回归的系统预测偏差可传播至下游关联、甚至产生方向相反的虚假关联，约束优化可改善校准 [31]；概率框架把预测年龄分布宽度定义为 BAU，在超 45 万 UKB 参与者中显示 BAU 与 BAG 弱相关 [32]。**这意味着跨队列比较前必须先处理年龄偏倚与不确定性，否则器官间差异可能被误读为生物学信号。** 现有外部验证仍集中于少数欧美生物库，跨族群、跨平台的前瞻性头对头比较缺位；性别分层（以色列 10K 队列显示男女衰老模式不同）[33] 可能是迁移的必要步骤，但该队列人群来源单一。

单细胞、空间与扰动体系把衰老建模从「个体年龄」推进到「细胞状态与微环境」。sc-ImmuAging（1,081 人、约 130 万细胞、五类免疫细胞）[34]、scAgeClock（CZ CELLxGENE 超 7,000 万细胞、门控多头注意力）[35] 与「细胞句子」LLM 微调 [36] 代表三条不同建模路线，但外部验证有限、组织覆盖偏血液。空间图谱方面，小鼠 9 组织空间转录组揭示免疫球蛋白聚集与 IgG 积累为保守衰老特征 [37]，乳腺 scRNA/snATAC 比较 3 月龄与 18 月龄 [38]，人皮肤显示光老化衰老负担高于时序衰老 [39]，人骨骼肌单核多组学提出 Maraviroc 候选 [40]。衰老细胞识别本身存在分歧：SenePy 强调细胞类型特异（仅 58/1540 组合标志物重叠显著）[41]，hUSI 追求通用性并优于 31 种方法 [42]。**这一「特异 vs 通用」的对立尚未在统一基准下裁决，是单细胞衰老建模的核心未解问题。**

AI 基准与基础模型正在补上「可比较、可验证」这一环，但覆盖仍不完整。LongevityBench 以 5 个数据域、17 项任务、18 个前沿系统评测，结论是没有单一模型全能、组学年龄预测最难，5 个 0.6B–9B 多任务 Longevity-LLM 可匹配或超过更大通用模型 [8]；Longevity-LLM v0.1 在 Qwen3-14B 上微调后表观年龄 MAE 为 4.34 年 [43]；单细胞基准覆盖超 250 万细胞、10 个通用基础模型与 3 个衰老专用模型，发现冻结表征下 Geneformer 时序年龄预测最佳但 2000 高变基因平均表现更高 [44]。表观侧 ComputAgeBench 以 66 个血液 DNAm 数据集、19 种衰老加速疾病、13 个时钟模型构建专用基准 [9]。**这些基准的共同局限是：LongevityBench 与单细胞基准覆盖多模态但任务口径各异，ComputAgeBench 仅限血液 DNAm 且未给具体性能数值，三者之间无法横向比较——跨模态统一评价标准仍是空白。** 数据资源侧，Biolearn 提供统一整理与系统评估框架 [45]，Immunosenescence Inventory 以免疫系统为中心整合多组学 [46]，但二者均依赖已有公开数据、未解决统一性能基准与临床验证。

扰动与类器官体系中的衰老建模尚处早期，但已显示「把时钟用作筛选读出」的可行性。人成纤维细胞可解释转录组年龄预测器被用作 cDNA 过表达筛选的判据，鉴定出 SRSF1 可产生强烈年轻化转录特征且不丧失细胞身份 [47]；Cell Painting 作为 2013 年提出的细胞状态成像 assay，十年间在协议、特征提取、质控与批次校正上持续改进 [48]。**但证据中并无同一研究对成像读出与转录组读出的衰老预测或扰动响应能力做直接对照，类器官体系的衰老建模亦未见入库证据——这是该方向明确的空白。** 跨物种脂质组学则补充了候选标志：脂酰链延长是小鼠、线虫、果蝇与人类衰老的保守标志，表现为向长链转变并伴随短链耗竭的比值性重塑，Plb1 参与调控，饮食限制可缩短小鼠心脏脂质 [49]；但尚未在人群队列或其他组织中验证。

应用侧的证据链在干预评估处最薄弱。特发性肺纤维化 12 周 2a 期试验比较六种蛋白质组时钟，均一致预测治疗组生物年龄更低，但作者强调无法单独区分衰老与疾病特异效应 [50]；ClockBase Agent 整合 40 余种时钟、43,602 个干预-对照比较，报告超 500 种干预显著降低生物年龄，同时发现更多干预加速而非延缓衰老 [51]；AURORA 生成式框架提名 Neisseria flavescens 并在线虫中验证 [52]；二甲双胍灵长类研究利用多组学猴时钟报告脑衰老约回退 6 年 [53]。**这些结果均依赖已有时钟的预测，实验验证程度不一，且时钟本身的组织可比性与因果有效性尚未解决，构成当前证据链的主要薄弱环节。** 功能表型侧的结论亦不一致：Lothian Birth Cohort 1936 显示表观年龄加速与 70 岁体能认知横断面相关、但不预测 70 至 76 岁间功能下降 [11]，与死亡预测研究中 Δage 的预后信号（每高 5 年死亡风险增 21%）[10] 形成对照，提示不同结局与设计下结论不可互换。

## 2 方法学


### 2.1 单组学衰老时钟（表观 / 蛋白 / 转录）

表观遗传时钟是单组学衰老时钟中发展最成熟的一支。Horvath 多组织时钟整合 82 个 Illumina 27K/450K 数据集、7844 个非癌样本，用弹性网络从 21,369 个共有 CpG 中选出 **353 个 CpG**，在多数组织中预测误差约 **3.6 年**，并显示早衰症不符合正常衰老轨迹、iPS 重编程可将表观时钟重置为 0 [1]。该工作确立了跨组织 DNAm 年龄预测的可行性，但其训练数据异质、组织覆盖仍有限 [1]。后续综述亦以 353 CpG 的 Horvath 时钟为表观时钟的原型，并将其与发育程序理论相联系，提出发育相关基因作用在生命后期持续并可能变得有害 [54]。

第二代时钟转向以健康结局而非实际年龄为训练目标。DNAm PhenoAge 用包含临床表型年龄的复合指标替代实际年龄，通过两步流程筛选 CpG，报告其在全因死亡、癌症、健康寿命、身体功能和阿尔茨海默病预测上优于第一代标志物，并关联炎症、干扰素及线粒体等通路 [12]。但该工作基于全血开发，摘要未给出样本规模与误差指标 [12]。在疾病预测层面，一项基于 Generation Scotland 队列 **18,859 人**、覆盖 174 种新发疾病和 10 年随访的无偏比较显示，第二、三代时钟显著优于第一代，完全校正模型下 13 种时钟与 57 种疾病共 **176 个 Bonferroni 显著关联**，其中 GrimAge v2 和 DunedinPACE 各有 72 个显著关联 [2]。LinAge2 的评测则报告其 20 年全因死亡预测 **AUC=0.8684**，优于 PhenoAge Clinical 的 0.8479 和 ChronAge 的 0.8288，20 年死亡 AUC=0.8440 优于 PhenoAge DNAm 的 0.7859 和 GrimAge2 的 0.8233，但部分对比未达统计显著 [55]。这些结果共同支持「以生存/功能结局训练的时钟在疾病场景更具效用」的方向，但各研究队列与结局定义不同，数字不宜直接横向比较。

表观时钟的生物学解释与因果性受到质疑。一项利用表观全基因组孟德尔随机化识别因果 CpG 的研究发现，现有表观时钟和年龄相关差异甲基化均未在这些位点富集；作者据此构建追踪损伤性变化的 **DamAge** 和适应性变化的 **AdaptAge**，前者与死亡等不良结局相关，后者与有益适应相关，且两者对短期干预敏感 [13]。另一项分析发现多数时钟 CpG 并不与转录因子结合位点重叠，说明时钟精度并非主要由 TF 结合动态驱动；其构建的 TFMethyl Clock 在弱相关非 TFBS CpG 模型上 **MdAE=3.77 年**，优于 Horvath1 的 5.95 年、接近 PhenoAge 的 3.79 年，且需移除 88,007 个 CpG 后误差才达随机水平 [56]。PathwayAge 则放弃单 CpG、改用 GO/KEGG 通路级甲基化建模，报告在多队列具强预测与泛化性，并能识别神经退行、免疫失调、代谢病相关通路 [14]。这些工作反映出「精度」与「机制可解释性」之间的张力：单 CpG 模型预测力强但生物学信息有限，通路级与因果框架试图补足解释，代价是依赖 MR 假设或组织特异性限制 [13][14]。

表观时钟的可靠性与组织可比性是另一争议点。跨组织比较给出更直接的警告：在 83 人、284 份颊上皮、唾液、干血斑、白细胞层和外周血单核细胞样本中，口腔与血液组织的表观年龄平均差**近 30 年**，多数血液时钟与口腔组织相关性低，Skin and Blood clock 一致性最高 [3]。这意味着把血液来源时钟外推到口腔或商业检测场景需谨慎。此外，对成人时钟位点发育动态的纵向分析显示，时钟位点轨迹高度异质且非线性，**超过三分之一**的位点自出生即存在个体差异、高于非时钟位点，并与遗传背景和产前暴露相关 [15]。在干预响应方面，TranslAGE 整合 **51 项**人类纵向干预研究、统一计算 16 种时钟和 94 种额外 DNAm 标志物，发现不同干预与时钟响应差异显著，并指出文献碎片化与面板不一致使跨研究比较困难 [57]。内在能力时钟则把表观预测从年龄转向功能表型：基于 INSPIRE-T 队列 933 人 EPIC 数据、弹性网筛选 **91 个 CpG** 预测内在能力，报告 IC 与年龄负相关 rs=-0.65、DNAm IC 预测相关 0.61，并在 FHS 中验证其可预测死亡 [58]。

蛋白质组时钟依托大规模血浆蛋白平台快速发展。UK Biobank 中基于 2,897 个血浆蛋白、**45,441 人**训练的蛋白质组年龄时钟，经 Boruta 筛选 **204 个蛋白**，报告与实际年龄 Pearson r=0.94，ProtAgeGap 与 27 个衰老表型、全因死亡和 26 种年龄相关疾病关联，并在 CKB（3,977 人）和 FinnGen（1,990 人）中独立验证 [4]。同样基于 UKB 的 PAC 使用 Olink 2,923 蛋白、**53,021 名** 39–70 岁参与者，以 LASSO 训练预测全因死亡，随访超 10 年，报告 PAC 年龄偏差与死亡及多种年龄相关疾病显著关联 [16]。器官特异化是另一条路线：利用 UKB 43,616 人及中国 CKB 3,977 人、美国 NHS 800 人，基于 Olink 2,916 蛋白构建整体和十个器官系统的时钟，跨队列相关 r=0.98 和 0.93，加速的器官衰老可预测疾病发生、进展和死亡，其中**脑衰老与死亡关联最强**，并可用精简蛋白面板保持性能 [17]。这些研究共享 UKB 平台，跨 ancestry 验证程度不同，CKB 与 FinnGen 样本量较小是共同限制 [4][16]。

蛋白组时钟正从「预测年龄」扩展到特定表型与系统。健康寿命蛋白组评分 HPS 基于 UKB 2,920 种蛋白、**53,018 人**、随访 13.5 年，在 43,119 名基线健康者中 **12,427 人（28.8%）**发生健康寿命终点事件，低 HPS 与更高死亡风险和慢性阻塞性肺病等年龄相关疾病相关 [18]。ECM 时钟仅用 **14 个血浆蛋白**，报告 ECM 蛋白随龄呈 U 型轨迹、最低点约 40–50 岁，时钟可预测年龄并区分健康与疾病，但 Robbins 队列最老仅 66 岁、U 型轨迹较弱 [19]。肌肉骨骼时钟整合转录组富集、蛋白功能注释与文献构建 39 个蛋白池，在 21,070 名 UKB 参与者中开发 MSKAge 与 MSKAgeMort，报告 MSKAge 相关 r 女性=0.62、男性=0.56，MSKAgeMort 相关 r 女性=0.93、男性=0.88，其加速指标可预测死亡与肌肉骨骼疾病 [20]。纵向层面，KORA 队列基于最多三个时间点、**9,105 样本、4,100 人**、25–88 岁的 LC-MS 血浆蛋白质组构建时钟与年龄加速指标，发现其与生活方式和临床风险因素相关，心血管代谢暴露共享蛋白组特征而吸烟和体力活动具独特特征，个体内血脂异常和肾功能受损与年龄加速增加相关 [21]。这些工作提示蛋白组时钟的效用高度依赖所选蛋白子集与目标表型，不同面板之间难以直接比较性能。

转录组时钟长期受平台依赖和组织特异性困扰。Pasta 采用「age-shift」学习框架，报告在 bulk 与单细胞 RNA-Seq、微阵列及跨物种数据上预测相对年龄，优于 MultiTIMER 和 tAge，可区分衰老、静息与干细胞状态，并揭示 p53 相关基因贡献及肿瘤分级与生存分层 [22]。DeepQA 针对「仅在健康样本训练、却在健康与非健康样本推断」的偏倚，设计混合专家结构与 Hinge-MAE 损失，在 MCATS 数据库 **3,060 样本**、31 个数据集上报告在健康和非健康受试者上均显著优于现有方法 [23]。大规模数据进一步推高精度：基于 ARCHS4 **56,877 例**、2–114 岁、多组织 RNA-seq 的混合专家模型报告 **MAE=7.58 年**，肺和脑预测最佳、肝较差，FOSB 重要性 1.00、C4B_2 为 0.95，但极端年龄方差大、百岁老人误差达 ±40 年 [5]；K-Dense 多智能体系统在 ARCHS4 57,584 样本、28 组织、1,039 队列上报告 **R²=0.854、MAE=4.26 年**，并提供校准置信区间以标记过渡期和极端年龄预测，同时发现 CDKN2A/p16 等阶段标志物与基因重要性波状变化 [6]。两项工作使用高度重叠的 ARCHS4 数据但误差不同，提示模型架构与样本筛选对结果影响显著，其数字不宜直接对比。小鼠端，LivAge 基于肝脏 RNA-seq 构建转录组时钟，在早衰综合征中显示转录组年龄增加，并可评估 Snell Dwarf、Ames Dwarf、GHR 缺陷及热量限制等干预，但仅限肝脏组织、验证范围有限 [59]。

跨组学与跨物种证据补充了单组学时钟的边界。StackAge 整合 UKB **30,376 人**的 2,923 蛋白与 251 代谢物，报告与实际年龄 Pearson r≈0.93，对 12 种慢性病风险预测增强，2 型糖尿病、阿尔茨海默病和慢性肾病 AUC 超过 0.90，但未整合表观遗传层且以横断面基线为主 [60]。代谢组时钟 MetaboAgeMort 基于 UKB **239,291 人**血浆代谢组、以 10 年全因死亡为替代指标，选出 **185 个**死亡相关代谢标志物，报告可提升死亡预测并关联疾病、可调因素与遗传位点，但主要為欧洲白人样本、外推性受限 [61]。跨物种方面，犬表观时钟利用 **894 只犬的 1,640 份**甲基化组，报告可预测死亡率、生命早期表观遗传衰老最快，大体型和雄性犬寿命更短且分子衰老加速，体型相关甲基化变化集中于转座子元件、性别相关变化集中于 X 染色体 [62]。总体来看，单组学时钟已在表观、蛋白、转录三个层面各自建立起可用的年龄预测与结局关联框架，但组织可比性、生物学可靠性、因果解释与跨平台泛化仍是共同未解问题，且现有证据以观察性关联为主，尚不足以支撑因果推断 [63][4]。

### 2.2 多模态整合与跨队列泛化

多模态整合的起点是同一队列内不同组学层面的并行建模。UK Biobank 血浆蛋白质组被用于训练 **11 个器官年龄模型**（约 3,000 蛋白、44,498 人），器官年龄差可预测疾病、环境暴露与死亡，其中脑、动脉和整体年龄对传统年龄的预测 r²=0.97 [24]。同一数据体系下另一项工作用 2,448 个血浆蛋白、43,498 人构建 11 个 **ProtBAG**，并与 9 个表型年龄差时钟整合，报告跨器官特征可提升系统性疾病类别和全因死亡预测 [25]。代谢组层面则用 107 种非衍生代谢物、274,247 人构建 5 个 **MetBAG**，独立测试集 Pearson r 为 0.25<r<0.42，关联 525 个疾病终点 [26]。这些工作共享 UK Biobank 平台，但蛋白与代谢物数量、器官划分和模型族不同，预测相关性高低不宜跨研究直接比较。

影像模态提供了另一条多器官路线。基于 MULTI Consortium 313,645 人的 7 个 **MRIBAG**（脑、心、肝、脾、脂肪、肾、胰）在留出测试中 Pearson r 0.23–0.77、MAE 约 5 年，并关联 2,923 个血浆蛋白与 327 个代谢物 [27]。CT 路线则用自动化流程从 123,281 名成人腹部 CT 提取 8 个心脏代谢标志物，**CTBA** 的 IPA 为 29.2、人口学模型为 21.7（p<0.001）[28]。两项影像研究都强调外部泛化问题：MRI 工作指出腹部 MRI 特征共线性导致泛化较差、脑模型存在域偏移 [27]，CT 工作则承认队列以白人为主（92%）、外部验证有限 [28]。

跨组学整合的代表是 **OMICmAge**：以 Mass General Brigham Biobank 约 31,000 人开发 EMRAge，在多组学子集中生成 DNAmEMRAge 与 OMICmAge，并在 All of Us 10,769、TruDiagnostic 14,213、Generation Scotland 18,672 等独立队列验证，报告与慢病和死亡强相关 [7]。中国人群的 **mCAS** 队列纳入 2,019 名 18–91 岁个体，构建核心能力时钟、多模态时钟与器官相关时钟三层框架，发现血浆蛋白时钟可代理系统生理能力、凝血因子年龄依赖积累驱动多器官衰老和炎症 [29]。另有 GOLD BioAge 以 Gompertz 风险函数构建轻量线性模型，并在 CHARLS、CLHLS、RuLAS 三个中国队列验证 [64]。这些研究在人群来源（美国、中国、以色列）与组学组合上互补，但尚无同一外部队列对上述多模态时钟做头对头比较。

跨队列泛化的直接证据集中在表观遗传时钟。迁移学习工作报告 Horvath 与 PedBE 时钟在墨西哥儿童青少年队列（523 份血样）中预测准确性下降，采用 Kriging 与 DNN 特征适配可缩小目标数据差距 [30]。这提示泛化失败可能来自阵列平台与人群分布差异，而非时钟本身失效。与之呼应，方法学工作指出常用 ML/AI 回归存在系统预测偏差并可传播至下游关联，甚至产生方向相反的虚假关联，约束优化框架可改善校准与下游推断 [31]；概率框架进一步把预测年龄分布的宽度定义为 **BAU**，在超 45 万 UK Biobank 参与者中显示 BAU 与 BAG 弱相关、随分子间年龄信号不一致而增加 [32]。二者共同说明，跨队列比较前需先处理年龄偏倚与不确定性，否则器官间差异可能被误读。

多模态时钟的应用已延伸到干预评估与假设生成。一项特发性肺纤维化 12 周 2a 期试验比较 **六种蛋白质组时钟**（ProtAge、OrganAgemortality、OrganAgechrono、PAC、ipfP3GPT、PAOPAC），均一致预测治疗组生物年龄更低，但作者强调蛋白质组时钟无法单独区分衰老与疾病特异效应 [50]。**ClockBase Agent** 整合 40 余种时钟再分析人鼠甲基化与 RNA-seq 数百万样本、43,602 个干预-对照比较，报告超 500 种干预显著降低生物年龄，同时发现更多干预加速而非延缓衰老 [51]。AURORA 生成式多模态框架则通过降低年龄差的干预筛选预测 **Neisseria flavescens** 为顶级候选，并在线虫中验证活菌延长寿命和健康寿命 [52]。这些结果依赖已有时钟的预测，实验验证程度不一，构成当前证据链的主要薄弱环节。

人群异质性与纵向设计是跨队列泛化的另一争议点。以色列 10K 项目对 1 万名 40–70 岁健康人每 2 年随访，报告男女衰老模式不同、较高 BA 评分与年龄相关疾病负担增加相关 [33]；这提示按性别分层可能是跨队列迁移的必要步骤，但该队列人群来源单一，外推性待验证。纵向多组学工作虽以个体化衰老轨迹为目标，摘要未提供具体方法、数据规模与结果，暂无法据此评估其泛化表现 [65]。总体而言，现有证据在器官覆盖与组学层次上快速扩张，但外部验证多集中于少数欧美生物库，跨族群、跨平台的前瞻性头对头比较仍然缺位。

### 2.3 单细胞与空间衰老图谱

单细胞衰老时钟的核心问题是细胞类型异质性。sc-ImmuAging 基于 **1081 名健康欧洲成人** PBMC 的约 **130 万细胞**，用 LASSO、随机森林和 PointNet 为五类免疫细胞分别建模，内外验证优于对照，并揭示 COVID-19 感染后单核细胞和 BCG 接种后 CD8+T 细胞的年龄改变异质性 [34]。scAgeClock 则用门控多头注意力网络，依托 CZ CELLxGENE 超 **7000 万细胞**训练，精度高于偏最小二乘、弹性网等基线 [35]；另一项工作报告将单细胞转录组表示为基因名序列的“细胞句子”微调大语言模型，在数百万细胞上训练，称达到单细胞分辨率年龄预测的最先进精度，并可提名调控后降低转录年龄的候选靶点 [36]。三者数据规模与建模路线不同，不宜直接比较精度高低；共同局限是外部验证有限、组织覆盖偏血液 [35]。在神经元层面，BitAge 与 Stochastic Clock 预测线虫 **128 种**神经元类型年龄约 **98h 至 177h**，近 **2 倍**差异，两时钟相关 Pearson **0.65**（P=5.5×10−17），并据此筛选出丁香酸和 vanoxerine [66]。

空间图谱把衰老从细胞类型推进到组织微环境。小鼠 **9 种**组织的空间转录组显示，衰老敏感斑点与组织结构熵升高共定位，免疫球蛋白表达细胞聚集是其微环境特征，IgG 在雄性和雌性小鼠及人组织中积累，靶向降低 IgG 可缓解小鼠多组织衰老 [37]。小鼠乳腺 scRNA-seq 与 snATAC-seq 比较 **3 月龄与 18 月龄**，发现上皮 AV/HS 减少、肌上皮增加，免疫髓系/浆细胞/记忆 T 增加、naive T 减少，成纤维细胞增加，并呈现衰老与癌症相关表观/转录特征 [38]。人皮肤单细胞与空间转录组则显示光老化衰老细胞负担高于时序衰老，衰老黑素细胞黑色素合成升高、衰老网状真皮成纤维细胞胶原和弹性纤维合成下降 [39]。人骨骼肌单核多组学构建了首个衰老人肌衰老细胞图谱，解析 SASP 异质性与动态，并提出 Maraviroc 作为候选干预 [40]。

衰老细胞识别方法本身存在分歧。SenePy 用 **72 个**小鼠和 **64 个**人类加权单细胞转录组 signature 构建评分平台，称其比体外来源 signature 更能重现体内衰老，并发现仅 **58/1540** 细胞类型组合的标志物重叠显著，说明标志物高度组织细胞特异 [41]。hUSI 从 **73 项**公开 RNA-seq 研究学习通用衰老特征，在 bulk 和单细胞多种条件下优于 **31 种**方法 [42]。两者取向相反：前者强调细胞类型特异，后者追求通用性；综述亦指出缺乏特异性标志物、衰老细胞稀少且异质动态是共同瓶颈 [67]。脑衰老综述补充了单细胞组学在细胞类型变化、细胞互作与年轻化干预评估中的作用，但受样本、批次和因果推断限制 [68]。

### 2.4 衰老生物学基准与基础模型

衰老生物学正从单一模态的专用时钟走向标准化评测与基础模型。**LongevityBench** 构建了覆盖 5 个生物数据域的 **17 项任务**，评测来自 6 个开发团队的 **18 个前沿 AI 系统**，结论是没有单一模型能主导所有任务，且**组学年龄预测是最难的任务**，与模型规模无关；作者微调的 5 个 **0.6B–9B** 多任务 Longevity-LLM 可匹配或超过更大的前沿系统 [8]。与之呼应，**Longevity-LLM v0.1** 将 Qwen3-14B 在 DNA 甲基化、蛋白质组、临床生物标志物和 RNA 表达上微调，强化微调后表观年龄预测 **MAE 为 4.34 年**，超过 Horvath 多组织时钟，蛋白质组谱生成显著优于所有前沿 LLM [43]。单细胞层面另有基准评估 10 个通用单细胞基础模型、3 个衰老专用模型及传统方法，覆盖 5 个生物学问题、**超过 250 万单细胞转录组**；冻结预训练表征时 Geneformer 在时序年龄预测和年龄伪时间一致性上最佳，但 **2000 个高变基因**的平均表现更高，多个模型在三种疾病背景中捕捉到正向分子年龄偏移 [44]。这些工作共同显示：专用小模型与通用大模型各有胜场，评测结论高度依赖任务与表征方式。

表观时钟的标准化评测已有专门框架。**ComputAgeBench** 以「可靠时钟应能区分健康个体与衰老加速疾病个体」为核心假设，整合 **66 个公开血液 DNA 甲基化数据集**、覆盖 **19 种衰老加速疾病**，测试 **13 个已发表表观遗传时钟模型**，并另建 46 个数据集用于训练新时钟 [9]。该基准仅基于血液 DNA 甲基化，未覆盖其他模态，全文也未给出具体模型性能数值 [9]；这与 LongevityBench 强调跨模态、组学年龄预测最难的结果形成互补而非直接可比——两者队列、任务与评价口径不同，数字不宜横向比较。

多篇综述勾勒出同一趋势与未解问题。有综述梳理 2016–2024 年间 **125 篇同行评审研究**，指出 CNN、RNN、GAN、LLM 和扩散模型已用于衰老时钟、合成数据生成、药物发现和多模态健康评估，但属叙述性综述、缺乏定量荟萃分析 [69]。另有综述认为表观时钟在预测生物年龄和健康表型上最准确，并将生物年龄预测器与「人类数字孪生」结合，但落地受数据整合、隐私、互操作性和纵向建模限制 [70]；临床衰老时钟综述则强调 AI 集成学习与深度学习推动多组学时钟在准确性、可解释性和泛化性上的进展，惟全文不可得、无法提取定量性能 [71]。方法学综述进一步把挑战归为数据异质性、泛化性有限、可解释性不足和临床转化障碍，并强调异步衰老与多模态融合 [72]。在干预评估侧，有观点文章主张 AI 评估应正确、有用、全面、可解释并考虑因果、跨学科、标准、纵向数据和已知衰老生物学，建议 LLM 结合知识图谱与检索增强生成并开展基准测试，但未提供实验验证或定量结果 [73]。可见基准与基础模型正在补上「可比较、可验证」这一环，而跨模态统一评价与临床转化仍是争议与空白所在。

### 2.5 类器官、扰动与 Cell Painting 衰老建模

在细胞衰老建模的扰动侧，一项研究构建了**人成纤维细胞的可解释转录组年龄预测器**，并以此作为筛选读出，开展cDNA过表达筛选，寻找能把衰老转录组重编程为年轻状态的因子；筛选鉴定出RNA加工与剪接因子**SRSF1**，其诱导可产生强烈的年轻化转录特征且不丧失细胞身份，体外实验显示可恢复年轻表型[47]。该工作将年龄预测器用作扰动筛选的判据，但证据限于体外成纤维细胞模型，样本规模与体内验证均未提及[47]。

在成像侧，Cell Painting作为2013年提出的显微细胞标记assay，旨在捕获细胞状态并优化图像型profiling，区别于传统高内涵筛选测量少量特征的做法[48]。十年间其协议、特征提取、质控和批次校正持续改进，并用于机制、毒性及多组学整合等应用[48]。不过该证据为综述，未提供统一定量基准，依赖公开数据集和计算实验技术进展[48]；与上述转录组筛选相比，两者分处成像与转录组两种读出层面，证据中并无在同一研究内对二者衰老预测或扰动响应能力的直接对照。

### 2.6 跨物种与跨组织衰老标志（脂质组等）

跨物种、多组织脂质组学比较显示，**脂酰链延长**是小鼠、线虫、果蝇和人类衰老的保守标志；人类心脏病进展中也出现类似的脂质延长，而饮食限制可缩短小鼠心脏脂质 [49]。衰老并非单一脂质种类的增减，而是表现为向长链脂质转变并伴随短链脂质耗竭的**比值性重塑** [49]。

在机制层面，该研究鉴定出脂质重塑因子 **Plb1** 参与调控上述脂质重塑过程 [49]。这一跨物种保守性与饮食限制的可逆性，为将脂质组特征纳入多模态衰老时钟提供了候选标志，但证据仅来自该研究的跨物种比较与小鼠心脏饮食限制对照，尚未涉及其他组织或人群队列的验证 [49]。

## 3 数据与资源

在数据资源的组织方式上，两项工作代表了不同路径。**Biolearn** 作为开源库，针对跨人群验证缺乏标准化方法、标志物设计分散、数据集结构不一致等问题，提供统一的整理、协调与系统评估框架，并已用于对多种衰老生物标志物的综合评估，覆盖多公开数据集，输出可复现的评估流程 [45]。其可用性以开源形式提供（https://Bio-Learn.github.io），但依赖已有公开数据，临床验证仍待推进 [45]。与之不同，**Immunosenescence Inventory** 面向免疫衰老这一特定子问题构建多组学数据库，整合单细胞转录组、bulk 转录组、表观组及 TCR/BCR 等多物种数据，并提供知识 curation、多模态数据集与工具，其中包括免疫细胞识别与免疫时钟计算，用于评估生物年龄、预测年龄相关疾病和干预影响 [46]。

两者的差异主要体现在覆盖范围与评估深度：Biolearn 强调跨数据集、跨人群的标志物系统比较与泛化性评估 [45]；Immunosenescence Inventory 则以免疫系统为中心，对标 ImmPort、InnateDB、Aging Atlas 等既有数据库，覆盖多物种和年龄阶段，但未提供统一预测性能基准，单细胞层面的免疫衰老覆盖仍有限 [46]。二者均以开放获取方式提供，且都受限于对已有数据的整合，尚未解决临床验证或统一性能基准的问题 [45][46]。

## 4 应用与结果

在血液DNA甲基化时钟的死亡预测方向上，早期工作确立了Δage（甲基化年龄减实际年龄）作为生物学年龄偏差指标的预后价值。四个老年人纵向队列的荟萃分析显示，**Δage每高5年全因死亡风险增加21%，校正健康、生活方式与APOE后仍增加16%**，且Δage遗传度为0.43 [10]。随后一项扩展至**13个队列、13,089人（2,734例死亡）**的荟萃分析比较了Horvath 353 CpG与Hannum 71 CpG时钟，报告表观年龄与实际年龄相关系数为0.65–0.89，年龄加速与全因死亡风险增加相关，并指出纳入血液细胞组成信息可提升预测 [74]。不过该研究也承认血液细胞组成会影响估计、部分出生队列无法计算年龄相关指标 [74]。在人群差异上，353 CpG时钟的多组织分析发现表观年龄加速存在种族和性别差异，并与冠心病及相关风险因素相关，但以横断面为主、组织来源异质 [75]。

在暴露与干预场景中，时钟被用于量化感染、移植与药物对生物年龄的影响。基于11个甲基化数据集（含血液与脑组织）的比较显示，HIV感染与显著增加的表观年龄加速相关，血液和脑组织均可见，但样本量有限且为横断面设计 [76]。异时心脏移植的多组学分析则报告移植心脏的DNA甲基化和基因表达生物年龄快速同化受体年龄，而非保留供体年龄，且该效应仅限移植物、不影响受体全身生物年龄 [77]。在灵长类干预中，40个月二甲双胍研究利用多组织转录组、DNA甲基化、蛋白与代谢组构建猴衰老时钟，发现**脑衰老约回退6年**，并伴脑结构保护与认知增强，部分由Nrf2激活介导；局限在于仅雄性食蟹猴、样本量未明确 [53]。此外，一项仅有标题与抽取字段的干细胞衰老时钟研究提示生物学年龄偏差与急性髓系白血病临床结局相关，但未给出具体数值与验证细节 [78]。

时钟与功能表型的关联则呈现方向性差异。Lothian Birth Cohort 1936在70岁（n=920）、73岁（n=299）、76岁（n=273）三波测量中，发现表观年龄加速与70岁步行速度、握力、肺功能和认知能力横断面相关，**但不预测70至76岁间的功能下降** [11]。这一“横断面有关、纵向预测有限”的结果，与死亡预测研究中Δage的预后信号形成对照，提示不同结局（功能衰退 vs 死亡）与不同研究设计下结论并不一致。系统综述层面，299篇文献、1050个EAA-因素关联、53种时钟的荟萃分析确认若干EAA与生理、认知、社会和环境因素存在显著汇总关联，并建立四级分类与TEAPEE数据库，但研究异质性大、部分关联证据有限、因果方向不明确 [79]。

## 5 评测、可复现性与争议

（本节暂无入库证据）

## 6 空白与趋势

当前证据显示，多模态衰老时钟的「多模态」大多停留在同一队列内并行建模、再事后整合的层面，而非真正的模态对齐与联合表征。UK Biobank 体系下的 11 器官蛋白时钟、11 个 ProtBAG、5 个 MetBAG 与 7 个 MRIBAG 各自独立训练，器官划分、蛋白/代谢物数量与模型族均不统一 [24][25][26][27]；OMICmAge 与 mCAS 虽在同一框架内组合多层组学，但前者以美国生物库为主、后者为中国单队列，**尚无同一外部队列对上述多模态时钟做头对头比较** [7][29]。这构成本方向第一个明确空白：**跨模态、跨队列的统一评测缺失**，而现有基准各自为政——ComputAgeBench 仅覆盖血液 DNA 甲基化、19 种疾病、13 个时钟 [9]，LongevityBench 覆盖 5 个数据域、17 项任务但结论是「组学年龄预测最难」[8]，两者队列与评价口径不同，无法互相校准。

由此衍生出若干具体空白与趋势：

1. **缺失模态与模态不对齐下的时钟构建几乎无人处理。** 现有工作均要求完整模态输入，而临床与队列场景中蛋白、代谢、影像极少同时可得；证据中唯一接近该问题的是迁移学习对表观时钟的跨平台适配（Kriging 与 DNN 特征适配缩小目标数据差距）[30]，以及概率框架把预测分布宽度定义为 BAU 以标记不确定性 [32]，但二者均未扩展到多模态缺失场景。**「部分模态可用时的稳健生物年龄估计」是可直接落地却尚属空白的方向。**

2. **年龄偏倚与不确定性校正尚未成为多模态时钟的标准步骤。** 方法学工作已证明常用 ML/AI 回归存在系统预测偏差，并可传播至下游关联、甚至产生方向相反的虚假关联，约束优化框架可改善校准 [31]；多器官蛋白时钟的方法学讨论也把年龄偏倚校正列为核心问题 [25]。但影像、代谢、单细胞时钟的报告中，偏倚校正与置信区间多为可选项而非强制项 [27][26]。**把校准与不确定性量化写进多模态时钟的评测协议，是低成本高收益的空白。**

3. **纵向/增量学习证据薄弱，且现有纵向结论互相矛盾。** Lothian Birth Cohort 显示表观年龄加速与 70 岁体能认知横断面相关、却不预测 70 至 76 岁功能下降 [11]；KORA 的纵向蛋白组时钟则报告个体内血脂异常与肾功能受损与年龄加速增加相关 [21]。二者结局与设计不同，无法合并判断。**「同一批个体、多时点、多模态的增量式衰老速率估计」在证据中尚无一项完成**，而这是区分「状态标记」与「速率测量」的关键。

4. **跨族群泛化证据高度集中于欧美生物库。** 蛋白时钟的外部验证主要落在 CKB（3,977 人）与 FinnGen（1,990 人）等较小样本 [4][16]；CT 时钟自认队列 92% 为白人、外部验证有限 [28]；MRI 时钟指出腹部特征共线性导致泛化较差、脑模型存在域偏移 [27]；MetaboAgeMort 亦以欧洲白人为主 [61]。**跨族群、跨平台的前瞻性头对头验证仍是缺位环节**，而以色列 10K 的性别差异结果提示按性别分层可能是迁移的必要步骤 [33]。

5. **基础模型与专用小模型的胜负高度依赖任务，尚无定论。** LongevityBench 报告没有单一模型全能、组学年龄预测最难、0.6B–9B 专用 Longevity-LLM 可匹配更大通用模型 [8]；Longevity-LLM v0.1 在表观年龄上 MAE 4.34 年并超过 Horvath 多组织时钟 [43]；单细胞基准则发现冻结表征时 Geneformer 最佳，但 2000 个高变基因的平均表现更高 [44]。**「何种任务该用基础模型、何种该用专用时钟」缺乏可操作的判据**，且这些评测均未纳入影像与空间模态。

6. **扰动与类器官体系的衰老建模刚起步，读出层面彼此割裂。** 人成纤维细胞可解释转录组年龄预测器被用作 cDNA 过表达筛选的读出，鉴定出 SRSF1 可产生年轻化转录特征 [47]；Cell Painting 作为细胞状态成像 assay 已成熟十年，但证据为综述、无统一定量基准 [48]。**证据中没有任何研究在同一实验体系内直接对照成像读出与转录组读出的衰老预测或扰动响应能力**，类器官中的衰老时钟构建亦未见入库证据。这是把「衰老时钟」从观测工具转为干预筛选工具的关键缺口。

7. **机制可解释性与预测精度的张力尚未在多模态层面被处理。** 表观层面已出现因果框架（DamAge/AdaptAge）[13] 与通路级时钟（PathwayAge）[14]，但蛋白、代谢、影像时钟的解释多停留在器官富集与通路分析 [50][25]。**跨模态共享的机制层表征（而非各模态各自的通路注释）尚属空白**，而这正是判断「生物年龄差是真实衰老还是疾病特异效应」的前提——肺纤维化试验已明确暴露该问题：六种蛋白时钟一致提示治疗组生物年龄更低，却无法单独区分抗衰老与抗纤维化效应 [50]。

8. **数据资源与评测框架正在标准化，但临床转化路径未验证。** Biolearn 提供统一整理、协调与系统评估框架并开源 [45]，Immunosenescence Inventory 以免疫系统为中心整合多组学并提供免疫时钟计算 [46]，但二者均依赖已有公开数据、未解决统一性能基准与临床验证 [45][46]。综述层面亦把落地障碍归为数据整合、隐私、互操作性与纵向建模 [70]，并把数据异质性、泛化性有限、可解释性不足列为核心挑战 [72]。**从「基准分数」到「临床或试验终点」之间，尚缺前瞻性、预注册的验证研究**，而将衰老终点纳入疾病临床试验的提议目前仅有一项 12 周 2a 期试验的方法学示范 [50]。

综合来看，本方向的演化脉络清晰：单组学时钟已分别在表观、蛋白、转录层面建立起可用的年龄预测与结局关联框架，多模态整合正从并行建模走向同队列组合，评测与基础模型开始补上「可比较」这一环。**但真正的模态对齐、缺失模态稳健性、跨族群头对头验证、纵向速率估计与跨模态机制表征，仍是证据清单中找不到对应工作的空白区**；而扰动与类器官体系中的衰老建模，则因读出层面割裂与缺乏入库证据，构成本方向最薄弱也最具扩展空间的一端 [47][48]。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 单组学衰老时钟（表观/蛋白/转录） | 成熟 | 表观时钟的方法学底座已高度收敛：Horvath 2013 多组织泛化时钟 [1] 与 PhenoAge [12] 奠定了「甲基化年龄 + 死亡率/健康寿命预测」的范式，后续工作多为增量（蛋白组时钟 [4]、因果富集表观年龄 [13]）。雷达样本中该节 n=28、median citations 9，说明新工作以应用/扩展为主，方法未出现替代性突破。 |
| 2.2 多模态整合与跨队列泛化 | 朝阳 | 近两年集中爆发且方法未收敛：血浆蛋白组连接脑-免疫衰老 [24]、MRI 多器官时钟 [27]、表型组性别特异动态 [33] 各自用不同模态与对齐策略，尚未形成统一框架；雷达样本中该节 recent_share **0.92**、CNS 占比 **0.56**，是典型的「新模态涌入、评测口径未定」阶段。 |
| 2.3 单细胞与空间衰老图谱 | 朝阳 | 图谱类工作密集出现但整合方法仍在探索：空间转录组揭示免疫球蛋白相关衰老 [37]、单细胞免疫衰老时钟揭示个体异质性 [34]、乳腺单细胞衰老图谱 [38] 分别给出不同组织/细胞类型的「衰老细胞状态」定义，跨图谱可比性尚未解决；雷达样本中该节 median citations **28**、CNS 占比 **0.58**，属高关注、方法未定。 |
| 2.4 衰老生物学基准与基础模型 | 萌芽 | 基准工作刚起步且规模小：ComputAgeBench 表观时钟基准 [9] 与 AI 干预评估验证要求 [73] 是少数把「评测」当研究对象的工作，另有数字孪生综述 [70]；雷达样本中该节 median citations **0**、CNS 占比 **0.11**，说明尚无被广泛引用的基准或基础模型，属探索期。 |
| 2.5 类器官、扰动与 Cell Painting 衰老建模 | 证据不足 | 雷达样本中该节仅 n=2：Cell Painting 十年综述 [48] 提供成像表型方法学，转录组重编程筛选鉴定 SRSF1 [47] 提供扰动体系案例，但两者均非「类器官衰老时钟」的直接建模证据，无法据此判定阶段。 |
| 2.6 跨物种与跨组织衰老标志（脂质组等） | 证据不足 | 雷达样本中该节仅 1 篇：长链脂质标记衰老并约束寿命 [49]，单篇不足以判断方法是否收敛或被替代。 |
| 3 数据与资源 | 萌芽 | 统一策展与评估框架 [45] 与免疫衰老多组学数据库 [46] 是少数面向「可复用资源」的工作，雷达样本中该节 n=2、recent_share **1.0**，说明资源层刚起步、尚未形成社区标准。 |
| 4 应用与结果 | 成熟 | 表观时钟的临床/流行病学应用已被大规模验证并反复复现：甲基化年龄预测全因死亡 [10]、meta 分析预测死亡时间 [74]、种族/性别/冠心病分析 [75]；雷达样本中该节 median citations **524**，属已被替代性验证的成熟应用层。 |
| 5 评测、可复现性与争议 | 证据不足 | 雷达样本中该节 n=0，无证据可引用，无法判定阶段。 |

**整体判断**：这个方向整体处于**「单组学时钟成熟、多模态整合与单细胞图谱朝阳、基准与资源萌芽」的三层叠加阶段**。窗口期集中在 **2.2 多模态整合**与 **2.3 单细胞/空间图谱**：雷达样本中这两节 recent_share 分别为 **0.92** 和 **0.75**、CNS 占比 **0.56/0.58**，说明近两年新工作密集但方法未收敛，正是「方法定义权」尚未被占满的时期，估计窗口 **1–2 年**（一旦出现被广泛复用的跨模态对齐框架或统一评测基准，增量工作会迅速转向成熟层）。最大的不确定性是**评测与可复现性层几乎空白**（第 5 节 n=0，2.4 节 median citations **0**）：多模态时钟的「谁更好」缺乏公认基准，导致方法比较不可比、跨队列泛化结论易被推翻；其次是**缺失模态与跨队列校正**没有标准做法，谁先做出可复现的基准，谁就掌握下一阶段的定义权。

**接下来怎么做**：

1. **把「缺失模态 + 跨队列校正」做成方法学主线，而不是再做一个新时钟**。切入点：用公开多组学队列（甲基化+转录组+蛋白组）构造人为缺失模态场景，做模态对齐与缺失鲁棒训练；产出是可复现的缺失模态基准 + 对齐方法。为什么现在做：2.2 节方法未收敛（[24]、[27] 各用不同模态与对齐策略），而 2.4 节基准几乎空白（[9] 仅覆盖表观时钟），缺口明确。

2. **把单细胞/空间图谱转成「细胞类型特异衰老时钟」并做跨图谱可比性**。切入点：用公开单细胞衰老图谱（[38]、[34]）训练细胞类型特异年龄预测器，重点解决批次/组织间可比性；产出是跨组织可迁移的单细胞衰老评分与不确定性估计。为什么现在做：2.3 节图谱密集但定义不统一（[37] 提出免疫球蛋白相关衰老这一新状态），可比性方法尚无人占位。

3. **与类器官 + 多组学合作项目对接，做「扰动体系中的衰老建模」**。切入点：在类器官扰动/重编程体系中采集转录组+成像（Cell Painting 式）表型，构建「扰动→衰老状态偏移」的预测模型；产出是类器官衰老响应的可复现建模流程与小型基准。为什么现在做：2.5 节雷达样本仅 2 篇（[48]、[47]），是**证据不足但方法学就绪**的空白区，且正好匹配他的合作项目，先发优势最大。

4. **用公共数据做一个「多模态衰老时钟评测 demo」抢占基准层**。切入点：整合现有公开系数与数据资源（[45] 的策展框架、[46] 的免疫衰老数据库），实现统一划分、跨队列留出与缺失模态压力测试；产出是开源 benchmark + 排行榜式报告。为什么现在做：第 5 节 n=0、2.4 节 median citations **0**，基准层是整条链路最薄弱环节，投入产出比最高，且能反哺他后续所有建模工作的可信度。

5. **把「衰老速率/纵向增量」作为建模目标而非横断面年龄**。切入点：在纵向队列上做增量学习与个体内变化率估计，结合 2.2 节的表型组性别特异动态（[33]）做分层验证；产出是纵向衰老速率模型与个体异质性分解。为什么现在做：现有成熟层（2.1、第 4 节）几乎都是横断面年龄预测（[10]、[74]），纵向速率是成熟层向朝阳层迁移的自然接口，竞争尚不拥挤。

## 参考文献

1. DNA methylation age of human tissues and cell types. Genome Biology 2013. https://doi.org/10.1186/gb-2013-14-10-r115
2. An unbiased comparison of 14 epigenetic clocks in relation to 174 incident disease outcomes.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66106-y
3. Cross-tissue comparison of epigenetic aging clocks in humans.. Aging cell 2025. https://doi.org/10.1111/acel.14451
4. Proteomic aging clock predicts mortality and risk of common age-related diseases in diverse populations. Nature Medicine 2023. https://doi.org/10.1038/s41591-024-03164-7
5. Transcriptomic age prediction using mixture-of-experts models reveals tissue-specific aging signatures in large-scale human RNA-sequencing data. medRxiv 2025. https://doi.org/10.1101/2025.06.28.25330474
6. Guided multi-agent AI invents highly accurate, uncertainty-aware transcriptomic aging clocks. bioRxiv 2025. https://doi.org/10.1101/2025.09.08.674588
7. OMICmAge quantifies biological age by integrating multi-omics with electronic medical records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01073-7
8. An open benchmark and language models for AI in aging biology.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.026
9. ComputAgeBench: Epigenetic Aging Clocks Benchmark. bioRxiv 2025. https://doi.org/10.1145/3711896.3737382
10. DNA methylation age of blood predicts all-cause mortality in later life. Genome Biology 2015. https://doi.org/10.1186/s13059-015-0584-6
11. The epigenetic clock is correlated with physical and cognitive fitness in the Lothian Birth Cohort 1936. International Journal of Epidemiology 2015. https://doi.org/10.1093/ije/dyu277
12. An epigenetic biomarker of aging for lifespan and healthspan. bioRxiv 2018. https://doi.org/10.18632/aging.101414
13. Causality-Enriched Epigenetic Age Uncouples Damage and Adaptation. bioRxiv 2023. https://doi.org/10.1038/s43587-023-00557-0
14. Decoding disease-specific ageing mechanisms through pathway-level epigenetic clock: insights from multi-cohort validation.. EBioMedicine 2025. https://doi.org/10.1016/j.ebiom.2025.105829
15. Characterising developmental dynamics of adult epigenetic clock sites.. EBioMedicine 2024. https://doi.org/10.1016/j.ebiom.2024.105425
16. Proteomic aging clock (PAC) predicts age‐related outcomes in middle‐aged and older adults. Aging Cell 2024. https://doi.org/10.1111/acel.14195
17. Organ-specific proteomic aging clocks predict disease and longevity across diverse populations.. Nature aging 2025. https://doi.org/10.1038/s43587-025-01016-8
18. A proteomic signature of healthspan.. Proceedings of the National Academy of Sciences of the United States of America 2025. https://doi.org/10.1073/pnas.2414086122
19. An Extracellular Matrix Aging Clock Based on Circulating Matrisome Proteins Predicts Biological Aging and Disease.. Aging cell 2026. https://doi.org/10.1111/acel.70474
20. Construction and Validation of Plasma Protein-Based Musculoskeletal Biological Age and Genetic and Environmental Risk Profiles.. Aging cell 2026. https://doi.org/10.1111/acel.70636
21. Intraindividual longitudinal changes of the proteome reveal dynamic markers of biological aging.  . https://doi.org/10.64898/2026.10.01.755909
22. Pasta, a Versatile Transcriptomic Clock, Maps the Chemical and Genetic Determinants of Aging and Rejuvenation. bioRxiv 2025. https://doi.org/10.1002/advs.76740
23. DeepQA: A Unified Transcriptome-Based Aging Clock Using Deep Neural Networks.. Aging cell 2025. https://doi.org/10.1111/acel.14471
24. Plasma proteomics links brain and immune system aging with healthspan and longevity.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03798-1
25. Refining the generation, interpretation and application of multi-organ, multi-omics biological aging clocks.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00928-9
26. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
27. MRI-based multi-organ clocks for healthy aging and disease assessment.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03999-8
28. Biological age model using explainable automated CT-based cardiometabolic biomarkers for phenotypic prediction of longevity.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56741-w
29. Multimodal clocks of human aging.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.025
30. BRIDGING THE GAP: ENHANCING THE GENERALIZABILITY OF EPIGENETIC CLOCKS THROUGH TRANSFER LEARNING.. The annals of applied statistics 2026. https://doi.org/10.1214/26-aoas2136
31. Trustworthy ML/AI for Aging Clocks: Preventing Systematic Prediction Bias in Biological Age Estimation. bioRxiv 2026. https://doi.org/10.64898/2026.05.27.728155
32. Uncertainty redefines biological age.  . https://doi.org/10.64898/2026.09.26.26364091
33. Phenome-wide associations of human aging uncover sex-specific dynamics.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00734-9
34. Single-cell immune aging clocks reveal inter-individual heterogeneity during infection and vaccination.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00819-z
35. scAgeClock: a single-cell transcriptome-based human aging clock model using gated multi-head attention neural networks.. npj aging 2026. https://doi.org/10.1038/s41514-026-00379-5
36. Universal Single-Cell Transcriptomic Aging Clock powered by LLMs reveals targets to slow cellular aging. Innovation in aging 2025. https://doi.org/10.1093/geroni/igaf122.4305
37. Spatial transcriptomic landscape unveils immunoglobin-associated senescence as a hallmark of aging.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.019
38. Comprehensive single-cell aging atlas of healthy mammary tissues reveals shared epigenomic and transcriptomic signatures of aging and cancer.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00751-8
39. Mapping epidermal and dermal cellular senescence in human skin aging.. Aging cell 2024. https://doi.org/10.1111/acel.14358
40. Multiomics and cellular senescence profiling of aging human skeletal muscle uncovers Maraviroc as a senotherapeutic approach for sarcopenia.. Nature communications 2025. https://doi.org/10.1038/s41467-025-61403-y
41. Unveiling the cell-type-specific landscape of cellular senescence through single-cell transcriptomics using SenePy.. Nature communications 2025. https://doi.org/10.1038/s41467-025-57047-7
42. A transcriptome-based human universal senescence index (hUSI) robustly predicts cellular senescence under various conditions.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00886-2
43. The End of Aging Clocks: Training Foundation Models to Reason in Aging and Longevity. bioRxiv 2026. https://doi.org/10.64898/2026.03.28.714980
44. Benchmarking single-cell foundation models for aging biology.  . https://doi.org/10.64898/2026.09.21.753191
45. A unified framework for systematic curation and evaluation of aging biomarkers.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00987-y
46. Immunosenescence Inventory-a multi-omics database for immune aging research.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1102
47. Transcriptomic reprogramming screen identifies SRSF1 as a regulator of aging.. Nature aging . https://doi.org/10.1038/s43587-026-01234-8
48. Cell Painting: a decade of discovery and innovation in cellular imaging.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02528-8
49. Longer lipids mark aging and constrain lifespan.. Nature aging . https://doi.org/10.1038/s43587-026-01223-x
50. Integration of proteomic aging clocks in a phase 2a clinical trial supports simultaneous geroprotective assessment.. Nature Biotechnology 2026. https://doi.org/10.1038/s41587-026-03286-y
51. Autonomous AI Agents Discover Aging Interventions from Millions of Molecular Profiles. bioRxiv 2025. https://doi.org/10.1101/2023.02.28.530532
52. Multi-modality profiling identifies Neisseria flavescens as a central geroprotective oral commensal in humans.. Nature aging . https://doi.org/10.1038/s43587-026-01220-0
53. Metformin decelerates aging clock in male monkeys.. Cell 2024. https://doi.org/10.1016/j.cell.2024.08.021
54. Epigenetic clocks and programmatic aging.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102546
55. LinAge2: providing actionable insights and benchmarking with epigenetic clocks.. npj aging 2025. https://doi.org/10.1038/s41514-025-00221-4
56. Enhancing the performance and interpretability of epigenetic clocks.. Nucleic acids research 2026. https://doi.org/10.1093/nar/gkag661
57. Responsiveness of epigenetic aging biomarkers to longevity interventions in humans.. Nature medicine 2026. https://doi.org/10.1038/s41591-026-04562-9
58. A blood-based epigenetic clock for intrinsic capacity predicts mortality and is associated with clinical, immunological and lifestyle factors.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00883-5
59. LivAge: An Online Aging Clock for Murine Transcriptomic Age Estimation.. Aging cell 2026. https://doi.org/10.1111/acel.70677
60. StackAge: an ensemble-based clock for precise quantification of biological age using multi-omics data.. Briefings in bioinformatics 2026. https://doi.org/10.1093/bib/bbag271
61. A Novel Metabolomic Aging Clock Predicting Health Outcomes and Its Genetic and Modifiable Factors. Advancement of science 2024. https://doi.org/10.1002/advs.202406670
62. Epigenetic aging and transposon dysregulation reflect size-related lifespan compression in dogs.. Science (New York, N.Y.) . https://doi.org/10.1126/science.aeb2986
63. Biological Versus Technical Reliability of Epigenetic Clocks and Implications for Disease Prognosis and Intervention Response.. Aging cell 2026. https://doi.org/10.1111/acel.70635
64. Gompertz Law-Based Biological Age (GOLD BioAge): A Simple and Practical Measurement of Biological Ageing to Capture Morbidity and Mortality Risks.. Advanced science (Weinheim, Baden-Wurttemberg, Germany) 2025. https://doi.org/10.1002/advs.202501765
65. Longitudinal multiomics reveals personalized aging trajectories.. Nature aging . https://doi.org/10.1038/s43587-026-01248-2
66. Aging clocks delineate neuron types vulnerable or resilient to neurodegeneration and identify neuroprotective interventions.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01067-5
67. Advancing biological understanding of cellular senescence with computational multiomics.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02314-y
68. Brain aging and rejuvenation at single-cell resolution.. Neuron 2025. https://doi.org/10.1016/j.neuron.2024.12.007
69. Deep learning and generative artificial intelligence in aging research and healthy longevity medicine.. Aging 2025. https://doi.org/10.18632/aging.206190
70. From ageing clocks to human digital twins in personalising healthcare through biological age analysis.. NPJ digital medicine 2025. https://doi.org/10.1038/s41746-025-01911-9
71. The Evolving Landscape of Clinical Aging Clocks: From Epigenetic to Multi-Omics Integration.. Aging cell 2026. https://doi.org/10.1111/acel.70579
72. Artificial intelligence approaches in biological age prediction: current status and challenges.. British journal of biomedical science 2026. https://doi.org/10.3389/bjbs.2026.16141
73. Validation Requirements for AI-based Intervention-Evaluation in Aging and Longevity Research and Practice. Ageing Research Reviews 2024. https://doi.org/10.1016/j.arr.2024.102617
74. DNA methylation-based measures of biological age: meta-analysis predicting time to death. Aging 2016. https://doi.org/10.18632/aging.101020
75. An epigenetic clock analysis of race/ethnicity, sex, and coronary heart disease. Genome Biology 2016. https://doi.org/10.1186/s13059-016-1030-0
76. HIV-1 Infection Accelerates Age According to the Epigenetic Clock. Journal of Infectious Diseases 2015. https://doi.org/10.1093/infdis/jiv277
77. Transplanted hearts assimilate the recipient’s biological age. bioRxiv 2026. https://doi.org/10.64898/2026.09.15.751836
78. A stem cell aging clock links biological age deviation to clinical outcome in acute myeloid leukemia. bioRxiv 2026. https://doi.org/10.64898/2026.02.12.703707
79. Breaking new ground on human health and well-being with epigenetic clocks: A systematic review and meta-analysis of epigenetic age acceleration associations.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102552
