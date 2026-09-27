# 多模态衰老时钟与生物年龄 · 方向背景报告

证据 71 篇 · 覆盖度 0.62 · 第 4 轮 · 更新 2026-09-27

## 摘要（TL;DR）

- 表观遗传时钟是单组学衰老时钟中最成熟的一支，Horvath 多组织预测器整合 82 个 Illumina 27K/450K 数据集、7844 个非癌样本，选出 353 个时钟 CpG，多数组织预测误差约 3.6 年 [1]。
- 时钟设计已从"以实际年龄为替代"转向以健康结局为目标，DNAm PhenoAge 在全因死亡、癌症、健康寿命、身体功能和阿尔茨海默病预测上优于第一代时钟 [2]。
- 基于 Generation Scotland 队列 18,859 人、随访 10 年、174 种新发疾病的比较显示，完全校正模型下 13 种时钟与 57 种疾病共 176 个 Bonferroni 显著关联，其中 GrimAge v2 和 DunedinPACE 各 72 个 [3]。
- 对时钟生物学基础的追问带来分歧：一项表观全基因组孟德尔随机化研究发现现有表观时钟和年龄相关差异甲基化位点均未在因果位点富集，据此构建的 DamAge 与 AdaptAge 对短期干预敏感 [4]。
- 跨五种组织、284 份样本（83 人，9-70 岁）的比较发现，口腔与血液组织的表观年龄估计平均差近 30 年，多数血液时钟与口腔组织相关性低，Skin and Blood clock 跨组织一致性最好 [5]。
- TranslAGE 平台评估 18 种 DNAm 衰老标志物发现，多数时钟技术重现性好，PCGrimAge 和 SystemsAge 较稳健，但生物学可靠性低至中等，调整免疫组成后进一步下降，且技术重现性不能预测生物学可靠性 [6]。
- 蛋白质组时钟在队列规模和跨人群验证上推进较快，UK Biobank 中基于 2,897 个血浆蛋白、45,441 人的时钟经 Boruta 筛选出 204 个蛋白，与实际年龄 Pearson r=0.94，并在 CKB（3,977 人）和 FinnGen（1,990 人）中独立验证 [7]。
- 跨队列泛化是这一领域最集中的薄弱环节，Horvath 和 PedBE 等常用时钟在墨西哥儿童青少年队列中预测准确性下降，基于 Kriging 和 DNN 特征适配的迁移学习被用于缩小目标数据差距，但样本仅 523 份血样 [8]。
- 方法学层面存在一个被明确指出的争议：常用 ML/AI 连续结局回归模型存在系统预测偏差，并会传播到下游关联估计，可能产生"预测脑龄越大认知越好"或"表观年龄越大肾功能越好"这类虚假甚至方向相反的关联 [9]。
- LongevityBench 覆盖 5 个生物数据域、17 项任务，评测了来自 6 个开发团队的 18 个前沿 AI 系统，结论是没有单一模型主导所有任务，且组学年龄预测是最难的任务，与模型规模无关 [10]。

## 1 背景与定义

多模态衰老时钟的方向边界，可以从“测什么”与“怎么整合”两个维度界定。测什么，已从单一分子层扩展到分子组学（DNA甲基化、转录组、蛋白组、代谢组、单细胞/空间）、影像与功能表型；怎么整合，则涵盖模态对齐、缺失模态处理、跨队列校正与纵向/增量学习。Horvath 多组织预测器以 **353 个时钟 CpG** 在多数组织中实现约 **3.6 年**误差，确立了“以分子特征估计生物学年龄”的范式 [1]；此后 DNAm PhenoAge 把训练目标从实际年龄换成含临床表型的复合指标，转向以健康结局为目标 [2]。**这一转向意味着“生物年龄”不再是实足年龄的替代品，而是对发病与死亡风险的压缩表示**，也决定了后续多模态整合的评价标准必须锚定结局而非年龄拟合。

演化脉络上，单组学时钟先成熟，多模态整合随后成为主线。蛋白组方向，UKB 2,897 个血浆蛋白经 Boruta 筛出 **204 个蛋白**，与实际年龄 **Pearson r=0.94**，并在 CKB、FinnGen 独立验证 [7]；器官特异时钟进一步细分到整体和十个器官，跨队列相关达 **r=0.98 和 0.93**，脑衰老与死亡关联最强 [11]。代谢组方向用 UKBB 274,247 人的 107 种非衍生代谢物构建 5 个 MetBAG，独立测试集 Pearson r 为 0.25<r<0.42 [12]；影像方向基于 313,645 人的 7 个 MRIBAG 在留出测试中 Pearson r 为 0.23–0.77、MAE 约 5 年 [13]。**不同模态的时钟在预测精度与生物学覆盖上各有侧重，但跨模态直接比较仍缺乏统一基准**，这是当前方向最突出的结构性缺口。

核心问题之一，是时钟的生物学解释与因果地位尚未收敛。表观全基因组孟德尔随机化识别出的因果 CpG 并未在现有表观时钟和年龄相关差异甲基化位点中富集，据此构建的 DamAge 追踪损伤性变化、AdaptAge 追踪适应性变化，二者对短期干预敏感 [4]；另一项工作则发现多数时钟 CpG 不与已知 TFBS 重叠，但用弱相关非 TFBS CpG 构建的模型 **MdAE=3.77 年**仍优于 Horvath1 的 5.95 年 [14]。**预测能力未必依赖已知调控机制，这使“时钟位点为何有效”成为悬而未决的问题**。组织与发育维度同样暴露局限：跨五种组织、284 份样本的比较发现口腔与血液的表观年龄估计平均差近 **30 年** [5]；纵向儿童队列显示时钟位点发育轨迹高度异质且非线性，**超过三分之一**的位点自出生即存在个体差异 [15]。

核心问题之二，是可靠性、偏倚与泛化。TranslAGE 评估 18 种 DNAm 标志物发现多数时钟技术重现性好，但**生物学可靠性低至中等**，调整免疫组成后进一步下降，且技术重现性不能预测生物学可靠性 [6]。方法学上，常用 ML/AI 连续结局回归模型存在系统预测偏差，会传播到下游关联估计，可能产生方向相反的虚假关联，作者提出基于约束优化的回归框架但未给出具体数据验证 [9]。跨队列方面，Horvath 和 PedBE 等常用时钟在墨西哥儿童青少年队列中预测准确性下降，迁移学习被用于缩小目标数据差距，但样本仅 523 份血样 [8]；MRIBAG 研究也指出腹部 MRI 特征共线性导致泛化较差、脑模型在外部队列存在域偏移 [13]。**泛化能力与模型复杂度、模态可及性之间存在张力：多组学模型预测力强但依赖数据可得性，轻量模型易推广但生物学分辨率有限**，GOLD BioAge 的 Gompertz 线性模型即属后者，其局限在于依赖常规临床标志物、可能遗漏分子层面机制 [16]。

单细胞、空间与类器官/扰动体系把方向从“预测年龄”推进到“定位衰老细胞与建模年轻化”。sc-ImmuAging 基于 **1081 名健康欧洲人** PBMC 的约 130 万细胞，为五类免疫细胞分别建模，揭示感染与接种后的年龄改变异质性 [17]；scAgeClock 用门控多头注意力网络在 CZ CELLxGENE 大规模数据上训练，精度高于偏最小二乘、弹性网等基线 [18]。空间图谱方面，小鼠九组织空间转录组显示免疫球蛋白表达细胞聚集是衰老保守微环境特征，**IgG** 可诱导巨噬细胞和小胶质细胞促衰老 [19]；人骨骼肌单核 RNA+ATAC 多组学构建衰老细胞图谱并提出 **Maraviroc** 作为肌少症候选 [20]。但如何定义衰老细胞本身存在分歧：SenePy 用 **72 个小鼠和 64 个人类** signature 发现仅 58/1540 细胞类型组合的标志物重叠显著，质疑通用 signature [21]；hUSI 则用 One-Class Logistic Regression 学习通用衰老特征，在多种条件下优于 31 种方法 [22]。**这一冲突部分源于 benchmark 与负样本质量差异，说明该方向尚缺公认的衰老细胞金标准** 。

AI 基准与基础模型正在成为方向的新边界。**LongevityBench** 覆盖 5 个生物数据域、17 项任务，评测 18 个前沿 AI 系统，结论是没有单一模型主导所有任务，且**组学年龄预测是最难的任务**，与模型规模无关；同一工作微调的 5 个 0.6B–9B 参数多任务 Longevity-LLM 可匹配或超过更大的通用前沿系统 [10]。Longevity-LLM v0.1 以 Qwen3-14B 在多组学上微调，强化微调后表观年龄预测 **MAE 为 4.34 年**，超过 Horvath 多组织时钟 [23]。评测标准方面，**ComputAgeBench** 以“可靠时钟应能区分健康个体与衰老加速疾病个体”为核心假设，整合 66 个公开血液 DNA 甲基化数据集、覆盖 19 种疾病，测试 13 个已发表时钟模型 [24]；Biolearn 则提供统一的开源整理与评估框架，揭示标志物跨人群和数据集的表现、稳健性与泛化性 [25]。**中等规模、面向衰老数据的专用模型可能比通用大模型更有效，但现有基准在模态覆盖、验证队列和性能报告上差异较大，跨研究直接比较仍不可行** [24][26]。

## 2 方法学


### 2.1 单组学衰老时钟（表观 / 蛋白 / 转录）

表观遗传时钟是单组学衰老时钟中发展最成熟的一支。Horvath 多组织预测器整合 82 个 Illumina 27K/450K 数据集、**7844 个非癌样本**，用弹性网络回归从 21,369 个共有 CpG 中选出 **353 个时钟 CpG**，在多数组织中预测误差约 **3.6 年**，并显示早衰症不符合正常衰老、iPS 重编程将表观时钟重置为 0 [1]。此后时钟设计从"以实际年龄为替代"转向以健康结局为目标：DNAm PhenoAge 用包含临床表型年龄的复合指标替代实际年龄，经两步流程筛选 CpG，在全因死亡、癌症、健康寿命、身体功能和阿尔茨海默病预测上优于第一代时钟 [2]。

时钟的"代际"差异在大规模无偏比较中得到量化。基于 Generation Scotland 队列 18,859 人、随访 10 年、174 种新发疾病的比较显示，第二代和第三代时钟显著优于第一代，后者在疾病场景中应用有限；完全校正模型下 13 种时钟与 57 种疾病共 **176 个 Bonferroni 显著关联**，其中 **GrimAge v2 和 DunedinPACE 各 72 个** [3]。LinAge2 的评测给出同研究内部的对照：其预测死亡 **AUC=0.8684**，优于 PhenoAge Clinical 的 0.8479 和 ChronAge 的 0.8288；20 年死亡 **AUC=0.8440**，优于 PhenoAge DNAm 的 0.7859 和 GrimAge2 的 0.8233 [27]。这些结果支持"以生存和功能衰老训练的时钟优于以实际年龄训练的时钟"这一判断，但部分对比未达统计显著 [27]。

对时钟生物学基础的追问带来了分歧。一项研究通过表观全基因组孟德尔随机化识别可能因果影响衰老性状的 CpG，发现现有表观时钟和年龄相关差异甲基化位点均未在这些位点富集；据此构建的 DamAge 追踪损伤性甲基化变化、与死亡等不良结局相关，AdaptAge 追踪适应性变化、与有益适应相关，两者对短期干预敏感 [4]。另一项工作则分析预测性 CpG 与转录因子结合位点的重叠，发现多数时钟 CpG 并不与已知 TFBS 重叠，说明时钟准确性并非主要由 TF 结合动态驱动；但用弱相关非 TFBS CpG 构建的模型 **MdAE=3.77 年**，优于 Horvath1 的 5.95 年、接近 PhenoAge 的 3.79 年，且需移除 88,007 个 CpG 后误差才达随机水平 [14]。这提示时钟位点的功能解释仍不明确，但预测能力未必依赖已知调控机制。

组织与发育维度进一步暴露了时钟的局限。跨五种组织、284 份样本（83 人，9-70 岁）的比较发现，口腔与血液组织的表观年龄估计平均差近 **30 年**，多数血液时钟与口腔组织相关性低，**Skin and Blood clock** 跨组织一致性最好 [5]。将成人时钟分解到单个 CpG 的纵向儿童队列分析显示，时钟位点发育轨迹高度异质且非线性，**超过三分之一**的位点自出生即存在个体差异、高于非时钟位点，且出生变异与遗传背景和产前暴露相关 [15]。PathwayAge 则放弃单 CpG、改用 GO/KEGG 通路级甲基化建模，在多队列和疾病组织中验证，识别出神经退行、免疫失调和代谢病相关通路 [28]。

可靠性问题对上述所有预测构成约束。TranslAGE 平台评估 18 种 DNAm 衰老标志物发现，多数时钟技术重现性好，PCGrimAge 和 SystemsAge 较稳健，但**生物学可靠性低至中等**，调整免疫组成后进一步下降，且技术重现性不能预测生物学可靠性 [6]。在干预响应方面，整合 51 项人类纵向干预研究、统一计算 16 种时钟和 94 种额外 DNAm 标志物的分析显示，不同干预与时钟的响应差异显著，并建立了可跨研究比较的响应性框架 [29]。此外，基于血液 DNA 甲基化的内在能力时钟用 INSPIRE-T 队列 933 人数据经弹性网回归筛选 **91 个 CpG** 预测内在能力，在 FHS 中验证，与年龄负相关 **rs=-0.65**、预测相关 0.61，并可预测死亡 [30]。

蛋白质组时钟在队列规模和跨人群验证上推进较快。UK Biobank 中基于 2,897 个血浆蛋白、45,441 人的时钟经 Boruta 筛选出 **204 个蛋白**，与实际年龄 **Pearson r=0.94**，其年龄差与 27 个衰老表型、全因死亡和 26 种年龄相关疾病关联，并在 CKB（3,977 人）和 FinnGen（1,990 人）中独立验证 [7]。PAC 时钟基于 UKB 53,021 名 39-70 岁参与者、2,923 个 Olink 蛋白，用 LASSO 训练并以随访超 10 年验证，其年龄偏差与全因死亡和多种年龄相关疾病显著关联 [31]。器官特异时钟进一步细分：利用 UKB 43,616 人及 CKB、NHS 外部队列、Olink 2,916 蛋白构建的整体和十个器官时钟，跨队列相关达 **r=0.98 和 0.93**，加速的器官衰老可预测疾病发生、进展和死亡，其中脑衰老与死亡关联最强，且精简蛋白面板可保持性能 [11]。

面向特定结局的蛋白评分与时钟并行发展。健康寿命蛋白组评分 HPS 基于 UKB 53,018 人、2,920 种蛋白构建，随访 13.5 年，在 43,119 名基线健康者中 **12,427 人（28.8%）**发生健康寿命终点事件，较低 HPS 与更高死亡风险和慢性阻塞性肺病等年龄相关状况相关 [32]。ECM 时钟仅用 **14 个血浆蛋白**，发现 ECM 蛋白随龄呈 U 型轨迹、最低点约 40-50 岁，可预测年龄并区分健康与疾病，但最老仅 66 岁的队列中 U 型轨迹较弱 [33]。肌肉骨骼时钟 MSKAge 与 MSKAgeMort 基于 UKB 21,070 人构建，MSKAge 相关 **r 女性=0.62、r 男性=0.56**，MSKAgeMort 相关 **r 女性=0.93、r 男性=0.88**，其加速指标可预测死亡、肌肉骨骼病和年龄相关病 [34]。

转录组时钟在方法上更强调跨平台泛化和不确定性刻画。Pasta 采用"年龄偏移"学习框架，可跨组织、bulk 与单细胞 RNA-Seq、微阵列及物种预测相对年龄，优于 MultiTIMER 和 tAge，能区分衰老、静息和干细胞状态，并揭示 p53 相关基因贡献 [35]。基于 ARCHS4 56,877 例、2-114 岁多组织数据的混合专家模型实现 **MAE=7.58 年**，肺和脑预测最佳、肝较差，FOSB 重要性 1.00、C4B_2 为 0.95、PAX8-AS1 为 0.85、MT-RNR2 为 0.64、GFAP 为 0.53，但极端年龄预测方差大、百岁老人误差达 **±40 年** [36]。DeepQA 用混合专家与 Hinge-MAE 损失，在 MCATS 数据库 3,060 样本、31 数据集上训练，在健康和非健康受试者上均显著优于现有方法 [37]。K-Dense 多智能体系统在 ARCHS4 57,584 样本、28 组织、1,039 队列、1-114 岁数据上实现 **R2=0.854、MAE=4.26 年**，并提供校准置信区间、标记过渡期和极端年龄预测，发现 CDKN2A/p16、AMPD3、MIR29B2CHG、SEPTIN3 等阶段标志物及 85 个重叠窗口中基因重要性的波状变化 [38]。小鼠肝脏转录组时钟 LivAge 则把应用场景扩展到干预评估，在早衰综合征中显示转录组年龄增加，并可评估 Snell Dwarf、Ames Dwarf、GHR 缺陷及热量限制等干预 [39]。

跨组学整合的尝试也已出现，但边界清晰。StackAge 整合 UKB 30,376 人的 2,923 种蛋白与 251 种代谢物，年龄预测 **Pearson r≈0.93**，对 12 种慢性病提升风险预测，2 型糖尿病、阿尔茨海默病和慢性肾脏病 **AUC 超过 0.90**，中位随访 11.7 年，但未整合表观遗传层且以横断面基线为主 [40]。代谢组时钟 MetaboAgeMort 基于 UKB 239,291 人、年龄中位 58.3 岁，选出 **185 个**全因死亡相关代谢标志物，用 LASSO Cox 与 Gompertz 回归建模，提升 10 年死亡预测并关联疾病、可调因素和遗传位点，但以全因死亡为替代指标、样本主要来自欧洲白人 [41]。这些工作共同表明，单组学时钟在预测精度上已具规模，但组织特异性、可靠性、因果解释和跨人群泛化仍是尚未收敛的问题。

### 2.2 多模态整合与跨队列泛化

多模态整合的核心动机，是单一模态时钟在器官特异性和预测范围上的局限。基于UKB 44,498人、2,916个血浆蛋白的LASSO模型构建了**11个器官年龄模型**，脑、动脉和整体年龄预测传统年龄的r²=0.97，并可在17年随访内预测心衰、慢阻肺等疾病发生[42]。同一队列的另一项工作用43,498人的2,448个血浆蛋白构建11个ProtBAG，强调年龄偏倚校正与器官蛋白特异性，并报告整合多器官特征可提升系统性疾病和全因死亡预测[43]。代谢组方向则用UKBB 274,247人的107种非衍生代谢物构建5个MetBAG，独立测试集Pearson r为0.25<r<0.42，关联525个疾病终点[12]。影像模态上，基于313,645人的7个MRIBAG在留出测试中Pearson r为0.23–0.77、MAE约5年，并关联2,923个血浆蛋白和327个代谢物[13]；CT方向的CTBA模型在123,281名成人中IPA为29.2，优于人口学模型的21.7（p<0.001）[44]。这些工作共同显示，不同模态的时钟在预测精度和生物学覆盖上各有侧重，但跨模态的直接比较仍缺乏统一基准。

跨队列泛化是这一领域最集中的薄弱环节。表观遗传时钟方面，Horvath和PedBE等常用时钟在墨西哥儿童青少年队列中预测准确性下降，基于Kriging和DNN特征适配的迁移学习被用于缩小目标数据差距，但样本仅523份血样[8]。MRIBAG研究也指出腹部MRI特征共线性导致泛化较差、脑模型在外部队列存在域偏移[13]。OMICmAge则展示了另一种路径：以MGB约31,264人开发EMRAge，在多组学子集中训练DNAmEMRAge和OMICmAge，并在All of Us 10,769、TruDiagnostic 14,213、Generation Scotland 18,672等独立队列验证，报告与慢病和死亡风险强相关[45]。GOLD BioAge采用更轻量的Gompertz风险函数线性模型，在NHANES、UKB及CHARLS、CLHLS、RuLAS三个中国队列中验证有效，但其局限在于依赖常规临床标志物、可能遗漏分子层面机制[16]。这些证据表明，泛化能力与模型复杂度、模态可及性之间存在张力：多组学模型预测力强但依赖数据可得性，轻量模型易推广但生物学分辨率有限。

人群与设计差异进一步影响结论的可比性。以色列10K项目对1万名40–70岁健康人每2年随访，构建多生理系统BA评分，揭示男女衰老模式差异，但队列主要来自以色列，性别与人群外推性需验证[46]。中国mCAS队列纳入2,019名18–91岁个体，建立核心能力时钟、多模态时钟和器官相关时钟三层框架，发现血浆蛋白时钟可代理系统生理能力、凝血因子年龄依赖积累驱动多器官衰老和炎症，但外部验证和跨族群适用性未说明[47]。值得注意的是，不同队列、人群和研究设计得到的数字不宜直接比高低，例如MRIBAG的r=0.23–0.77与MetBAG的r=0.25–0.42来自不同模态、不同样本和分析流程，只能在同一研究内部比较对照。

方法学层面存在一个被明确指出的争议：常用ML/AI连续结局回归模型存在系统预测偏差，并会传播到下游关联估计，可能产生“预测脑龄越大认知越好”或“表观年龄越大肾功能越好”这类虚假甚至方向相反的关联，而真实生物年龄在训练中不可观测使问题更复杂；作者提出基于约束优化的回归框架以改善校准和下游推断，但摘要未给出具体数据验证[9]。这一警告对前述所有时钟的下游关联解读都构成约束。与此相关，ClockBase Agent用自主AI代理整合40余种衰老时钟、评估43,602个干预-对照比较，发现超500种干预显著降低生物年龄，同时报告更多干预加速而非延缓衰老、疾病状态多加速生物年龄，但其依赖已有时钟预测、实验验证有限[48]。这说明多模态整合的价值不仅在于提升预测精度，也在于暴露时钟本身的偏差结构。

在应用端，多模态时钟开始进入临床试验场景。一项针对特发性肺纤维化的12周2a期试验中，六种蛋白质组时钟（ProtAge、OrganAgemortality、OrganAgechrono、PAC、ipfP3GPT、PAOPAC）对血清蛋白质组作出一致预测，均提示治疗组生物年龄更低，通路分析显示衰老和代谢过程出现潜在抗衰老转变并伴抗纤维化活性；但蛋白质组时钟无法单独区分衰老与疾病特异效应，样本来自单一疾病和短期试验[49]。综合来看，多模态整合与跨队列泛化的进展体现在器官覆盖扩展、多组学关联和独立队列验证上，而主要争议集中在年龄偏倚与系统预测偏差的校正、器官特异性定义、以及不同人群和平台间的域偏移；这些问题的解决程度，直接决定多模态衰老时钟能否从关联研究走向可解释、可推广的临床终点。

### 2.3 单细胞与空间衰老图谱

单细胞转录组衰老时钟已从泛化模型走向细胞类型特异建模。sc-ImmuAging 基于 **1081 名健康欧洲人** PBMC 的约 130 万细胞，用 LASSO、随机森林和 PointNet 为五类免疫细胞分别建模，内外验证优于对照，并揭示 COVID-19 感染后单核细胞和 BCG 接种后 CD8+T 细胞的年龄改变异质性 [17]。scAgeClock 则用门控多头注意力网络，在 CZ CELLxGENE 超 7000 万细胞上训练，精度高于偏最小二乘、弹性网等基线 [18]。另一条路线把单细胞转录组表示为基因名序列的「细胞句子」微调大语言模型，在数百万细胞上训练，实现单细胞分辨率年龄预测，并提名可降低转录年龄的候选靶点 [50]。三者差异在于建模单元与先验：细胞类型特异时钟强调免疫细胞异质性，通用注意力模型强调跨组织覆盖，LLM 路线则依赖预训练语言先验，其跨物种泛化与干预靶点尚需实验确认 [50]。

空间与多组学图谱把衰老时钟从「预测年龄」推进到「定位衰老细胞」。小鼠九组织空间转录组显示，衰老敏感位点与组织结构熵升高共定位，免疫球蛋白表达细胞聚集是其微环境特征，**IgG** 在雄性和雌性小鼠衰老组织及人组织中积累，并可诱导巨噬细胞和小胶质细胞促衰老，靶向降低 IgG 缓解多组织衰老 [19]。人骨骼肌单核 RNA+ATAC 多组学构建了首个衰老细胞图谱，解析 SASP 异质性与动态，并提出 **Maraviroc** 作为肌少症衰老治疗候选 [20]。人皮肤单细胞与空间转录组构建 SenSkin™ 基因集，发现光老化衰老细胞负担高于时序衰老，衰老黑素细胞黑色素合成升高、衰老网状真皮成纤维细胞胶原和弹性纤维合成下降 [51]。小鼠乳腺 scRNA-seq 与 snATAC-seq 比较 3 月龄与 18 月龄，显示上皮、免疫和成纤维细胞组成改变及癌症/衰老相关表观转录特征 [52]。

如何定义与识别衰老细胞本身存在方法学分歧。SenePy 用 **72 个小鼠和 64 个人类**加权单细胞转录组 signature 构建评分平台，发现仅 58/1540 细胞类型组合的标志物重叠显著，通用 signature 会被细胞异质性掩盖，已知标志物高度组织细胞特异 [21]。hUSI 则从 73 项公开 RNA-seq 研究用 One-Class Logistic Regression 学习通用衰老特征，在 bulk 和单细胞多种条件下优于 31 种方法，并用于 COVID-19 肺和黑色素瘤组织 [22]。两者取向相反：前者强调细胞类型特异、质疑通用标志物，后者主张可迁移的通用指数，这一冲突部分源于 benchmark 与负样本质量差异 [22]。综述亦指出，缺乏特异性标志物、衰老细胞稀少且异质动态，是多组学识别与空间定位的核心障碍 [53]。

在神经系统中，单细胞时钟被用于区分易感与耐受的神经元类型。对线虫 **128 种**神经元类型应用 BitAge 与 Stochastic Clock，预测年龄从约 **98h 到 177h**，近 2 倍差异，两时钟相关 Pearson 0.65（P=5.5×10−17）；较老神经元更易早期退化，翻译是驱动因素，丁香酸和 vanoxerine 可防止神经退化 [54]。该结果主要基于线虫，人类相关性需进一步验证 [54]。脑衰老综述则从细胞类型中心视角总结年龄相关变化与细胞互作，并评述单细胞组学如何无偏评估年轻化干预，但受样本、批次和因果推断限制 [55]。

### 2.4 衰老生物学基准与基础模型

衰老生物学正从单一模态的专用时钟走向跨模态基准与基础模型。**LongevityBench** 覆盖 5 个生物数据域、17 项任务，评测了来自 6 个开发团队的 18 个前沿 AI 系统，结论是没有单一模型主导所有任务，且**组学年龄预测是最难的任务**，与模型规模无关 [10]。同一工作微调了 5 个 0.6B–9B 参数的多任务 Longevity-LLM，其表现可匹配或超过更大的通用前沿系统 [10]。与之呼应，Longevity-LLM v0.1 以 Qwen3-14B 在 DNA 甲基化、蛋白质组、临床生物标志物和 RNA 表达上微调，强化微调后表观年龄预测 **MAE 为 4.34 年**，超过 Horvath 多组织时钟，蛋白质组谱生成也显著优于所比较的前沿 LLM [23]。这两项工作共同指向一个判断：中等规模、面向衰老数据的专用模型可能比通用大模型更有效，但前者仍属初期阶段性报告、未说明数据规模与公开情况 [23]，后者的任务与模型覆盖也可能仍有限 [10]。

在评测标准方面，**ComputAgeBench** 提出以“可靠时钟应能区分健康个体与衰老加速疾病个体”为核心假设的标准化框架，整合 66 个公开血液 DNA 甲基化数据集、覆盖 19 种疾病，测试 13 个已发表表观遗传时钟模型，并另建 46 个数据集用于训练新时钟 [24]。其局限在于仅基于血液 DNA 甲基化、未覆盖其他模态，且未提供具体模型性能数值 [24]。方法学综述则把 AI 生物年龄预测拆解为生物标志物选择、特征工程、模型开发、偏倚校正和性能评估等环节，强调异步衰老与多模态融合，并指出数据异质性、泛化性有限、可解释性不足和临床转化障碍是当前挑战 [26]。另有综述认为 AI 的集成学习与深度学习推动了衰老时钟在准确性、可解释性和泛化性上的进展，但该文全文不可得，具体数据、验证队列和定量性能无法提取 [56]。

多模态整合被反复视为方向，但落地路径与证据强度不一。有综述指出表观时钟被认为预测生物年龄和健康表型最准确，并提出将生物年龄预测器与“人类数字孪生”结合，用实时多模态数据流和连续监测模拟干预与风险，其限制是数据整合、隐私、互操作性和纵向建模 [57]。另一篇覆盖 2016–2024 年 125 篇同行评审研究的叙述性综述总结了 CNN、RNN、GAN、LLM 和扩散模型在衰老时钟、合成数据生成、药物发现和多模态健康评估中的应用，但作为综述缺乏定量荟萃分析 [58]。在干预评估这一子问题上，有观点类论文主张评估应正确、有用、全面、可解释，并考虑因果、跨学科、标准、纵向数据和已知衰老生物学，建议采用 LLM 结合知识图谱与检索增强生成并开展基准测试，但未提供具体实验验证或定量结果 [59]。总体来看，基准与基础模型两条线索正在汇合，但各研究在模态覆盖、验证队列和性能报告上的差异，使得跨研究的直接比较仍不可行 [24][26]。

### 2.5 类器官、扰动与 Cell Painting 衰老建模

基于显微成像的细胞状态刻画方法中，Cell Painting 自 2013 年提出，旨在通过细胞标记 assay 捕获细胞状态，并优化与标准化图像型 profiling [60]。其核心思路是**利用图像中的丰富信息识别生物样本间的相似性或差异**，而非像传统高内涵筛选那样仅测量少量特征 [60]。该综述指出，Cell Painting 能够捕获细胞对多种扰动的响应，并已应用于机制研究、毒性评估及多组学整合等场景 [60]。

在方法演进上，该综述总结了过去十年间协议、特征提取、质控和批次效应校正的持续改进，以及针对不同扰动的适配 [60]。不过，作为一篇综述，它**未提供统一定量基准**，其结论依赖公开数据集与计算实验技术的进展 [60]。未来方向包括计算与实验技术的进一步发展、新公开数据集的构建，以及与其他高内涵数据的整合 [60]。

## 3 数据与资源

面向跨人群、跨数据集的衰老标志物验证，**Biolearn** 提供了统一的开源整理与评估框架，针对标准化方法缺失、标志物设计分散、数据集结构不一致等障碍，对多种衰老生物标志物进行协调与系统评估，并揭示其在不同人群和数据集间的表现、稳健性与泛化性，输出可复现的评估流程 [25]。该框架依赖已有公开数据，临床验证仍待推进 [25]。与之互补，**Immunosenescence Inventory** 面向免疫衰老，整合单细胞转录组、bulk 转录组、表观组及 TCR/BCR 等多物种数据，提供知识 curation、多模态数据集与工具，支持免疫细胞识别和免疫时钟计算，用于评估生物年龄、预测年龄相关疾病及干预影响 [61]。

两者定位不同：Biolearn 侧重标志物的统一整理与系统评估，Immunosenescence Inventory 侧重免疫衰老多组学数据的整合与免疫时钟工具 [25][61]。二者均依赖已有公开数据，且都指出验证层面的局限——前者临床验证待推进，后者未提供统一预测性能基准、单细胞免疫衰老覆盖仍有限 [25][61]。

## 4 应用与结果

在死亡与疾病结局预测方面，DNA甲基化年龄差（Δage）被用于晚年风险分层。四个老年人纵向队列的荟萃分析显示，**Δage每高5年全因死亡风险增加21%，校正健康、生活方式与APOE后仍增加16%**，且Δage遗传度为0.43 [62]。随后一项扩展至13个队列、13,089人（2,734例死亡）的荟萃分析比较了Horvath 353 CpG与Hannum 71 CpG时钟，发现表观年龄与实足年龄相关系数为0.65–0.89，年龄加速与全因死亡风险增加相关，且纳入血液细胞组成信息可提升预测 [63]。同一353 CpG时钟在多组织数据中显示表观年龄加速存在种族与性别差异，并与冠心病及相关风险因素相关 [64]。在感染场景中，基于11个甲基化数据集的比较显示HIV感染与血液和脑组织中显著增加的表观年龄加速相关 [65]。

在体能、认知与多因素关联方面，Lothian Birth Cohort 1936（70岁n=920、73岁n=299、76岁n=273）发现表观年龄加速与70岁时的步行速度、握力、肺功能和认知能力横断面相关，但**不预测70至76岁间的功能下降** [66]。一项系统综述与荟萃分析检索299篇文献，提取1050个EAA-因素关联、涵盖53种甲基化时钟，随机效应荟萃分析发现若干EAA与生理、认知、社会和环境因素存在显著汇总关联，并建立四级分类与TEAPEE数据库 [67]。上述证据的局限在于：队列多限于老年人或特定人群，血液细胞组成影响估计，且关联的因果方向不明确 [62][63][67]。

在干预与器官/疾病层面的应用上，一项40个月研究以雄性食蟹猴为对象，利用多组织转录组、DNA甲基化、血浆蛋白与代谢组构建猴衰老时钟，发现二甲双胍显著延缓衰老指标，**脑衰老约回退6年**，保护脑结构并增强认知，部分由Nrf2激活介导 [68]。异时心脏移植的多组学分析（小鼠与患者）显示，移植心脏的DNA甲基化和基因表达生物年龄快速同化受体年龄，且**该效应仅限移植物，不影响受体全身生物年龄** [69]。此外，一项干细胞衰老时钟研究提出生物学年龄偏差与急性髓系白血病临床结局相关，但具体定量结果与验证细节未在提供文本中给出 [70]。这些工作提示衰老时钟的应用正从死亡预测扩展到干预评估与器官/疾病场景，但灵长类样本仅限雄性、移植研究全文未公开、干细胞时钟缺乏定量验证，均限制了结论的推广 [68][69][70]。

## 5 评测、可复现性与争议

（本节暂无入库证据）

## 6 空白与趋势

多模态衰老时钟的整合目前仍以“同一队列内多模态并行建模、分别关联结局”为主，真正的模态对齐与缺失模态补全尚未成为主流。UKB 44,498人、2,916个血浆蛋白的11器官模型与43,498人、2,448个蛋白的11个ProtBAG，均是在蛋白组内部做器官拆分，而非跨组学融合[42][43]；MetBAG用274,247人的107种代谢物构建5个器官时钟，MRIBAG用313,645人的7个器官影像时钟，CTBA用123,281人的CT标志物，三者各自独立、互不校验[12][13][44]。StackAge虽整合蛋白与代谢物，但明确未纳入表观遗传层且以横断面基线为主[40]。**跨模态的直接比较与统一基准仍缺乏**，不同模态报告的r值来自不同样本与分析流程，只能在同一研究内部比较。

趋势一：**从“预测年龄”转向“预测结局并区分损伤与适应”**。DamAge/AdaptAge把因果信息引入表观时钟，将损伤性与适应性甲基化变化解耦，两者对短期干预敏感[4]；LinAge2以20年死亡预测为目标，AUC=0.8440，优于PhenoAge DNAm的0.7859和GrimAge2的0.8233[27]；Generation Scotland 18,859人、174种疾病的比较显示GrimAge v2和DunedinPACE各72个显著关联[3]。**但“以结局训练”是否等于“更接近真实生物年龄”仍未被独立验证**，因为真实生物年龄在训练中不可观测[9]。

趋势二：**器官/细胞类型分辨率持续细化，但器官特异性定义不统一**。蛋白组方向有11器官ProtBAG、10器官时钟、脑-动脉-整体年龄三条并行路线，各自定义器官富集蛋白的方式不同[43][11][42]；单细胞方向sc-ImmuAging为五类免疫细胞分别建模，scAgeClock用门控多头注意力跨组织预测[17][18]。**“器官年龄”目前是建模约定而非生物学实体**，同一器官在不同研究中的蛋白面板、训练目标和年龄差定义均不可通约。

趋势三：**基准与基础模型开始成形，但覆盖与公开度不足**。LongevityBench覆盖5个数据域、17项任务、18个前沿AI系统，结论是没有单一模型主导、组学年龄预测最难[10]；Longevity-LLM v0.1以Qwen3-14B微调，表观年龄MAE为4.34年[23]；ComputAgeBench整合66个血液DNA甲基化数据集、19种疾病、13个时钟模型[24]；Biolearn提供统一整理与评估框架[25]。**空白在于：尚无覆盖多模态（甲基化+蛋白+代谢+影像+单细胞）的公开基准**，ComputAgeBench仅限血液DNA甲基化，LongevityBench的任务与模型覆盖也可能仍有限[24][10]。

趋势四：**扰动与类器官体系的衰老建模仍处于早期，与时钟的对接尚未建立**。Cell Painting综述总结了协议、特征提取、质控与批次校正的十年改进，并指出未来方向包括新公开数据集与高内涵数据整合，但**未提供统一定量基准**[60]。ClockBase Agent整合40余种时钟、评估43,602个干预-对照比较，报告超500种干预显著降低生物年龄，但依赖已有时钟预测、实验验证有限[48]。**没人做的方向是：把Cell Painting或类器官扰动表型直接作为时钟的训练标签或验证模态**，现有扰动评估仍以转录组/甲基化时钟为读出，成像表型与分子时钟之间缺少映射。

趋势五：**跨队列泛化从“验证”走向“迁移”，但方法学证据薄弱**。Horvath和PedBE在墨西哥儿童青少年队列中准确性下降，Kriging与DNN特征适配被用于迁移学习，但样本仅523份血样[8]；MRIBAG指出腹部MRI共线性导致泛化差、脑模型存在域偏移[13]；OMICmAge在All of Us 10,769、TruDiagnostic 14,213、Generation Scotland 18,672等独立队列验证[45]；GOLD BioAge在NHANES、UKB及三个中国队列验证，但依赖常规临床标志物[16]。**空白在于：缺少对缺失模态、平台差异和人群差异的系统性校正框架**，现有迁移多为单队列适配，未形成可复用的域泛化方法。

趋势六：**系统预测偏差被识别为领域级风险，但校正方案尚未落地**。约束优化回归框架被提出以改善校准和下游推断，可避免“预测脑龄越大认知越好”这类方向相反的虚假关联，但摘要未给出具体数据验证[9]。TranslAGE评估18种DNAm标志物发现多数时钟技术重现性好，但**生物学可靠性低至中等**，调整免疫组成后进一步下降，且技术重现性不能预测生物学可靠性[6]。**没人做的方向是：把偏差校正与可靠性评估嵌入时钟开发的标准流程**，目前二者仍是事后分析。

趋势七：**衰老细胞识别与时钟建模出现方法学冲突，通用标志物与细胞类型特异标志物尚未调和**。SenePy用72个小鼠和64个人类signature发现仅58/1540细胞类型组合的标志物重叠显著，通用signature会被细胞异质性掩盖[21]；hUSI用One-Class Logistic Regression学习通用衰老特征，在bulk和单细胞多种条件下优于31种方法[22]。**这一冲突部分源于benchmark与负样本质量差异**[22]，而综述亦指出缺乏特异性标志物、衰老细胞稀少且异质动态是多组学识别与空间定位的核心障碍[53]。

趋势八：**空间与单细胞图谱把衰老定位到微环境，但跨物种、跨组织的外推仍受限**。小鼠九组织空间转录组显示IgG积累是保守特征并可诱导促衰老[19]；人骨骼肌单核RNA+ATAC构建衰老细胞图谱并提出Maraviroc候选[20]；人皮肤SenSkin™发现光老化衰老细胞负担高于时序衰老[51]；线虫128种神经元类型的BitAge预测年龄从约98h到177h，但人类相关性需验证[54]。**空白在于：空间衰老图谱与分子时钟尚未双向校准**，即图谱衍生的空间特征未用于改进时钟，时钟预测的年龄差也未在空间上定位到具体细胞邻域。

趋势九：**干预评估进入临床试验场景，但衰老终点与疾病终点的区分仍是难题**。rentosertib治疗特发性肺纤维化的12周2a期试验中，六种蛋白质组时钟一致提示治疗组生物年龄更低，但**无法单独区分衰老与疾病特异效应**，样本来自单一疾病和短期试验[49]。整合51项人类纵向干预研究、统一计算16种时钟和94种额外DNAm标志物的分析建立了可跨研究比较的响应性框架[29]。**没人做的方向是：设计能同时捕捉抗衰老与抗疾病效应的复合终点**，现有试验仍以疾病终点为主、衰老时钟为辅助读出。

趋势十：**多模态数据资源与图谱在积累，但模态间的时间对齐与纵向增量学习尚未解决**。Immunosenescence Inventory整合单细胞转录组、bulk转录组、表观组及TCR/BCR数据，支持免疫时钟计算，但未提供统一预测性能基准、单细胞免疫衰老覆盖仍有限[61]。综述提出将生物年龄预测器与“人类数字孪生”结合，用实时多模态数据流和连续监测模拟干预与风险，但受限于数据整合、隐私、互操作性和纵向建模[57]。**空白在于：纵向多模态时钟的增量学习框架缺失**，现有工作多为横断面训练+独立队列验证，OMICmAge、GOLD BioAge等均未报告纵向更新策略[45][16]。

综合来看，**多模态衰老时钟的空白集中在三处**：一是跨模态统一基准与缺失模态校正框架的缺位，使不同模态的预测精度无法直接比较；二是系统预测偏差与生物学可靠性的评估尚未嵌入开发流程，下游关联的方向性存疑；三是扰动/类器官/成像表型与分子时钟之间缺少映射，使干预筛选与机制解释仍依赖单一分子读出。趋势则指向专用基础模型、器官/细胞类型分辨率细化、以及衰老终点进入临床试验，但三者的成熟度差异显著，短期内难以形成闭环。

## 7 未归类新证据

表观遗传时钟与程序性衰老理论的整合，为理解甲基化时钟的生物学基础提供了新框架。该综述指出，时钟CpG位点附近存在指定发育的基因，包括Hox（同源盒）和polycomb类基因，这提示时钟与发育机制存在关联；同时，表观时钟从胚胎发育到老年持续运行，支持发育程序驱动衰老的观点，其中**Horvath多组织甲基化时钟**基于**353个CpG**，可跨组织预测年龄[71]。

作者进一步提出，发育相关基因的作用在生命后期持续并可能变得有害，这或许是衰老的重要机制[71]。不过，该证据为综述性文章，缺乏原始实验验证，部分观点仍属推测[71]。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 单组学衰老时钟（表观/蛋白/转录） | 成熟 | 表观时钟已有 2013 年 [1] 与 2018 年 [2] 两代经典系数公开、被大规模引用，方法框架（甲基化→年龄回归）已收敛；近年增量转向蛋白组 [7] 与因果增强表观年龄 [4]，属于同一范式的模态扩展而非方法重构。雷达样本中该节 n=25、近两年占比 0.72，但中位引用仅 10，提示新工作多为增量验证。 |
| 2.2 多模态整合与跨队列泛化 | 朝阳 | 该节雷达样本年份跨度仅 2024–2026、近两年占比 0.92、CNS 占比 0.54，说明近两年集中爆发；[42] 用血浆蛋白组连接脑—免疫衰老与健康寿命，[13] 用 MRI 构建多器官时钟，两者模态、器官、建模口径均不同，说明整合范式尚未收敛；[46] 做表型组全关联并揭示性别特异动态，进一步说明跨队列/跨表型校正仍是开放问题。 |
| 2.3 单细胞与空间衰老图谱 | 朝阳 | [19] 用空间转录组揭示免疫球蛋白相关衰老，[21] 用单细胞刻画细胞类型特异的衰老景观，两者都在建图谱而非收敛到统一时钟；[17] 提出单细胞免疫衰老时钟并强调个体异质性，[52] 建健康乳腺单细胞衰老图谱，说明“图谱 + 时钟”两条线并行、方法未定。雷达样本该节 n=12、CNS 占比 0.58、中位引用 28，属高关注但未定型。 |
| 2.4 衰老生物学基准与基础模型 | 萌芽 | 该节雷达样本 n=8、中位引用仅 2，说明工作少且新；[24] 提出 ComputAgeBench 表观时钟基准，[59] 讨论 AI 干预评估的验证要求，两者都是“定标准/定规则”的早期基础设施，而非已收敛的建模范式；[58] 与 [57] 仍以综述/数字孪生框架为主，缺少统一基准与基础模型权重。 |
| 2.5 类器官、扰动与 Cell Painting 衰老建模 | 证据不足 | 雷达样本仅 1 篇 [60]，且是 Cell Painting 方法综述而非衰老建模本身，无法判断该细分方向阶段。 |
| 3 数据与资源 | 萌芽 | 雷达样本仅 2 篇：[25] 提出衰老生物标志物系统化 curation 与评估统一框架，[61] 建免疫衰老多组学数据库，两者都是资源/框架型早期工作，尚未形成被广泛复用的标准资源生态。 |
| 4 应用与结果 | 成熟 | [62] 与 [63] 已把甲基化年龄用于死亡预测与 meta 分析，[64] 与 [65] 把时钟应用到种族/性别/冠心病与 HIV 加速衰老，属经典应用范式；雷达样本该节近两年占比仅 0.22、中位引用 524，说明新工作少、以引用旧范式为主。 |
| 5 评测、可复现性与争议 | 证据不足 | 雷达样本 n=0，无证据可判断。 |

**整体判断**：这个方向整体处于**朝阳期偏早期**——单组学时钟（2.1）和应用（4）已成熟，但真正的方法前沿在**多模态整合（2.2）与单细胞/空间图谱（2.3）**，两者雷达样本近两年占比分别 **0.92** 和 **0.75**、CNS 占比 **0.54** 和 **0.58**，说明近两年集中爆发且顶刊频出，但模态、器官、队列、建模口径均未收敛。**基准与基础模型（2.4）尚在萌芽**，雷达样本中位引用仅 **2**，是明显的空白区。窗口期估计还有 **1–2 年**：多模态整合的“拼模态”红利正在被快速消耗，一旦出现跨队列统一基准（如 ComputAgeBench 类工作扩展到多模态）或基础模型权重公开，后来者只能做增量。**最大不确定性**是评测与可复现性（第 5 节雷达样本 n=0）：没有统一基准，多模态时钟的“泛化”声明无法被独立验证，可能导致一批高影响工作无法沉淀为可复用方法。

**接下来怎么做**：

1. **用公共多模态数据做“缺失模态”鲁棒性基准**：切入点是用 [42]（血浆蛋白组）与 [13]（MRI 多器官时钟）的公开系数/数据，构造模态缺失场景，系统评测现有整合方法。为什么现在做：2.2 节雷达样本近两年占比 **0.92** 但方法未收敛，缺失模态是公认痛点却无基准；产出可直接对接 [24] 的基准思路，形成多模态版 benchmark。与博后合作项目结合：公共数据 demo 即可起步，无需新采数据。

2. **把单细胞/空间衰老图谱转成“细胞类型特异时钟”并做跨组织泛化**：切入点是用 [17]（单细胞免疫衰老时钟）与 [52]（乳腺单细胞衰老图谱）的公开数据，训练细胞类型条件化的时钟，测试跨组织迁移。为什么现在做：2.3 节 CNS 占比 **0.58**、中位引用 **28**，图谱多但时钟少，跨组织泛化几乎空白；产出是可复用的细胞类型特异时钟系数。与博后合作项目结合：单细胞 + 多模态建模正是其算法强项。

3. **在类器官扰动体系中建立衰老/年轻化建模的评测协议**：切入点是用 [60]（Cell Painting）的成像范式，结合类器官 + 多组学扰动数据，定义“年轻化评分”的建模与验证标准。为什么现在做：2.5 节雷达样本仅 **1 篇**且非衰老建模本身，属证据不足的空白区；[59] 已指出 AI 干预评估缺验证要求，先做协议即占位。与博后合作项目结合：直接对接其类器官 + 多组学合作项目。

4. **参与/扩展衰老生物标志物统一 curation 框架，做多模态版**：切入点是用 [25] 的统一 curation 与评估框架，把多模态时钟纳入同一评测口径，并接入 [61] 的免疫衰老多组学数据库做案例。为什么现在做：第 5 节雷达样本 **n=0**，评测与可复现性是最大不确定性；谁先定义多模态评测口径，谁就掌握后续比较基准。产出是开源评测工具 + 论文。

5. **用纵向/增量学习做“衰老速率”而非“年龄”的建模**：切入点是用 [46]（表型组全关联、性别特异动态）与 [7]（蛋白组时钟预测死亡与疾病风险）的纵向设计，把静态年龄预测转为速率估计。为什么现在做：2.1 节已成熟、增量为主，但“速率”建模在雷达样本中仍零散；2.2 节跨队列泛化需求正好需要速率型目标。产出是可跨队列迁移的衰老速率模型。与博后合作项目结合：公共纵向队列 + 多模态 demo 即可验证。

## 参考文献

1. DNA methylation age of human tissues and cell types. Genome Biology 2013. https://doi.org/10.1186/gb-2013-14-10-r115
2. An epigenetic biomarker of aging for lifespan and healthspan. bioRxiv 2018. https://doi.org/10.18632/aging.101414
3. An unbiased comparison of 14 epigenetic clocks in relation to 174 incident disease outcomes.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66106-y
4. Causality-Enriched Epigenetic Age Uncouples Damage and Adaptation. bioRxiv 2023. https://doi.org/10.1038/s43587-023-00557-0
5. Cross-tissue comparison of epigenetic aging clocks in humans.. Aging cell 2025. https://doi.org/10.1111/acel.14451
6. Biological Versus Technical Reliability of Epigenetic Clocks and Implications for Disease Prognosis and Intervention Response.. Aging cell 2026. https://doi.org/10.1111/acel.70635
7. Proteomic aging clock predicts mortality and risk of common age-related diseases in diverse populations. Nature Medicine 2023. https://doi.org/10.1038/s41591-024-03164-7
8. BRIDGING THE GAP: ENHANCING THE GENERALIZABILITY OF EPIGENETIC CLOCKS THROUGH TRANSFER LEARNING.. The annals of applied statistics 2026. https://doi.org/10.1214/26-aoas2136
9. Trustworthy ML/AI for Aging Clocks: Preventing Systematic Prediction Bias in Biological Age Estimation. bioRxiv 2026. https://doi.org/10.64898/2026.05.27.728155
10. An open benchmark and language models for AI in aging biology.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.026
11. Organ-specific proteomic aging clocks predict disease and longevity across diverse populations.. Nature aging 2025. https://doi.org/10.1038/s43587-025-01016-8
12. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
13. MRI-based multi-organ clocks for healthy aging and disease assessment.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03999-8
14. Enhancing the performance and interpretability of epigenetic clocks.. Nucleic acids research 2026. https://doi.org/10.1093/nar/gkag661
15. Characterising developmental dynamics of adult epigenetic clock sites.. EBioMedicine 2024. https://doi.org/10.1016/j.ebiom.2024.105425
16. Gompertz Law-Based Biological Age (GOLD BioAge): A Simple and Practical Measurement of Biological Ageing to Capture Morbidity and Mortality Risks.. Advanced science (Weinheim, Baden-Wurttemberg, Germany) 2025. https://doi.org/10.1002/advs.202501765
17. Single-cell immune aging clocks reveal inter-individual heterogeneity during infection and vaccination.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00819-z
18. scAgeClock: a single-cell transcriptome-based human aging clock model using gated multi-head attention neural networks.. npj aging 2026. https://doi.org/10.1038/s41514-026-00379-5
19. Spatial transcriptomic landscape unveils immunoglobin-associated senescence as a hallmark of aging.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.019
20. Multiomics and cellular senescence profiling of aging human skeletal muscle uncovers Maraviroc as a senotherapeutic approach for sarcopenia.. Nature communications 2025. https://doi.org/10.1038/s41467-025-61403-y
21. Unveiling the cell-type-specific landscape of cellular senescence through single-cell transcriptomics using SenePy.. Nature communications 2025. https://doi.org/10.1038/s41467-025-57047-7
22. A transcriptome-based human universal senescence index (hUSI) robustly predicts cellular senescence under various conditions.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00886-2
23. The End of Aging Clocks: Training Foundation Models to Reason in Aging and Longevity. bioRxiv 2026. https://doi.org/10.64898/2026.03.28.714980
24. ComputAgeBench: Epigenetic Aging Clocks Benchmark. bioRxiv 2025. https://doi.org/10.1145/3711896.3737382
25. A unified framework for systematic curation and evaluation of aging biomarkers.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00987-y
26. Artificial intelligence approaches in biological age prediction: current status and challenges.. British journal of biomedical science 2026. https://doi.org/10.3389/bjbs.2026.16141
27. LinAge2: providing actionable insights and benchmarking with epigenetic clocks.. npj aging 2025. https://doi.org/10.1038/s41514-025-00221-4
28. Decoding disease-specific ageing mechanisms through pathway-level epigenetic clock: insights from multi-cohort validation.. EBioMedicine 2025. https://doi.org/10.1016/j.ebiom.2025.105829
29. Responsiveness of epigenetic aging biomarkers to longevity interventions in humans.. Nature medicine 2026. https://doi.org/10.1038/s41591-026-04562-9
30. A blood-based epigenetic clock for intrinsic capacity predicts mortality and is associated with clinical, immunological and lifestyle factors.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00883-5
31. Proteomic aging clock (PAC) predicts age‐related outcomes in middle‐aged and older adults. Aging Cell 2024. https://doi.org/10.1111/acel.14195
32. A proteomic signature of healthspan.. Proceedings of the National Academy of Sciences of the United States of America 2025. https://doi.org/10.1073/pnas.2414086122
33. An Extracellular Matrix Aging Clock Based on Circulating Matrisome Proteins Predicts Biological Aging and Disease.. Aging cell 2026. https://doi.org/10.1111/acel.70474
34. Construction and Validation of Plasma Protein-Based Musculoskeletal Biological Age and Genetic and Environmental Risk Profiles.. Aging cell 2026. https://doi.org/10.1111/acel.70636
35. Pasta, a Versatile Transcriptomic Clock, Maps the Chemical and Genetic Determinants of Aging and Rejuvenation. bioRxiv 2025. https://doi.org/10.1002/advs.76740
36. Transcriptomic age prediction using mixture-of-experts models reveals tissue-specific aging signatures in large-scale human RNA-sequencing data. medRxiv 2025. https://doi.org/10.1101/2025.06.28.25330474
37. DeepQA: A Unified Transcriptome-Based Aging Clock Using Deep Neural Networks.. Aging cell 2025. https://doi.org/10.1111/acel.14471
38. Guided multi-agent AI invents highly accurate, uncertainty-aware transcriptomic aging clocks. bioRxiv 2025. https://doi.org/10.1101/2025.09.08.674588
39. LivAge: An Online Aging Clock for Murine Transcriptomic Age Estimation.. Aging cell 2026. https://doi.org/10.1111/acel.70677
40. StackAge: an ensemble-based clock for precise quantification of biological age using multi-omics data.. Briefings in bioinformatics 2026. https://doi.org/10.1093/bib/bbag271
41. A Novel Metabolomic Aging Clock Predicting Health Outcomes and Its Genetic and Modifiable Factors. Advancement of science 2024. https://doi.org/10.1002/advs.202406670
42. Plasma proteomics links brain and immune system aging with healthspan and longevity.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03798-1
43. Refining the generation, interpretation and application of multi-organ, multi-omics biological aging clocks.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00928-9
44. Biological age model using explainable automated CT-based cardiometabolic biomarkers for phenotypic prediction of longevity.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56741-w
45. OMICmAge quantifies biological age by integrating multi-omics with electronic medical records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01073-7
46. Phenome-wide associations of human aging uncover sex-specific dynamics.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00734-9
47. Multimodal clocks of human aging.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.025
48. Autonomous AI Agents Discover Aging Interventions from Millions of Molecular Profiles. bioRxiv 2025. https://doi.org/10.1101/2023.02.28.530532
49. Integration of proteomic aging clocks in a phase 2a clinical trial supports simultaneous geroprotective assessment.. Nature Biotechnology 2026. https://doi.org/10.1038/s41587-026-03286-y
50. Universal Single-Cell Transcriptomic Aging Clock powered by LLMs reveals targets to slow cellular aging. Innovation in aging 2025. https://doi.org/10.1093/geroni/igaf122.4305
51. Mapping epidermal and dermal cellular senescence in human skin aging.. Aging cell 2024. https://doi.org/10.1111/acel.14358
52. Comprehensive single-cell aging atlas of healthy mammary tissues reveals shared epigenomic and transcriptomic signatures of aging and cancer.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00751-8
53. Advancing biological understanding of cellular senescence with computational multiomics.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02314-y
54. Aging clocks delineate neuron types vulnerable or resilient to neurodegeneration and identify neuroprotective interventions.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01067-5
55. Brain aging and rejuvenation at single-cell resolution.. Neuron 2025. https://doi.org/10.1016/j.neuron.2024.12.007
56. The Evolving Landscape of Clinical Aging Clocks: From Epigenetic to Multi-Omics Integration.. Aging cell 2026. https://doi.org/10.1111/acel.70579
57. From ageing clocks to human digital twins in personalising healthcare through biological age analysis.. NPJ digital medicine 2025. https://doi.org/10.1038/s41746-025-01911-9
58. Deep learning and generative artificial intelligence in aging research and healthy longevity medicine.. Aging 2025. https://doi.org/10.18632/aging.206190
59. Validation Requirements for AI-based Intervention-Evaluation in Aging and Longevity Research and Practice. Ageing Research Reviews 2024. https://doi.org/10.1016/j.arr.2024.102617
60. Cell Painting: a decade of discovery and innovation in cellular imaging.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02528-8
61. Immunosenescence Inventory-a multi-omics database for immune aging research.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1102
62. DNA methylation age of blood predicts all-cause mortality in later life. Genome Biology 2015. https://doi.org/10.1186/s13059-015-0584-6
63. DNA methylation-based measures of biological age: meta-analysis predicting time to death. Aging 2016. https://doi.org/10.18632/aging.101020
64. An epigenetic clock analysis of race/ethnicity, sex, and coronary heart disease. Genome Biology 2016. https://doi.org/10.1186/s13059-016-1030-0
65. HIV-1 Infection Accelerates Age According to the Epigenetic Clock. Journal of Infectious Diseases 2015. https://doi.org/10.1093/infdis/jiv277
66. The epigenetic clock is correlated with physical and cognitive fitness in the Lothian Birth Cohort 1936. International Journal of Epidemiology 2015. https://doi.org/10.1093/ije/dyu277
67. Breaking new ground on human health and well-being with epigenetic clocks: A systematic review and meta-analysis of epigenetic age acceleration associations.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102552
68. Metformin decelerates aging clock in male monkeys.. Cell 2024. https://doi.org/10.1016/j.cell.2024.08.021
69. Transplanted hearts assimilate the recipient’s biological age. bioRxiv 2026. https://doi.org/10.64898/2026.09.15.751836
70. A stem cell aging clock links biological age deviation to clinical outcome in acute myeloid leukemia. bioRxiv 2026. https://doi.org/10.64898/2026.02.12.703707
71. Epigenetic clocks and programmatic aging.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102546
