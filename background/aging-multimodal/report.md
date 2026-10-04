# 多模态衰老时钟与生物年龄 · 方向背景报告

证据 74 篇 · 覆盖度 0.62 · 第 5 轮 · 更新 2026-10-04

## 本次变更

- 新增 [26] Benchmarking single-cell foundation models for aging biology
- 新增 [31] Uncertainty redefines biological age
- 新增 [51] Multi-modality profiling identifies Neisseria flavescens as a central geroprotective oral commensal in humans.

## 摘要（TL;DR）

- 第一代表观遗传时钟以实际年龄为训练目标，Horvath 用 353 个 CpG 构建多组织预测器，测试误差约 3.6 年 [1]。
- 第二代时钟转向复合终点，DNAm PhenoAge 在全因死亡、癌症、健康寿命等预测上显著优于第一代标志物 [2]。
- Generation Scotland 队列 18,859 人中，13 种时钟与 57 种疾病共产生 176 个 Bonferroni 显著关联，GrimAge v2 和 DunedinPACE 各有 72 个 [3]。
- 跨五种组织、284 份样本比较发现，口腔与血液组织的表观年龄平均差近 30 年，Skin and Blood clock 跨组织一致性最好 [4]。
- UK Biobank 中 45,441 人、2,897 个血浆蛋白训练的模型筛选出 204 个蛋白，与实际年龄 Pearson r=0.94 [5]。
- 器官特异化路线在 UKB 43,616 人及中国 3,977 人、美国 800 人队列中，跨队列 r 分别达 0.98 和 0.93 [6]。
- 转录组时钟在 ARCHS4 的 56,877 例人类 RNA-seq 上，混合专家模型达到 MAE=7.58 年，百岁老人误差达 ±40 年 [7]。
- K-Dense 多智能体系统在 ARCHS4 的 57,584 样本上达到 R²=0.854、MAE=4.26 年，并提供校准置信区间 [8]。
- StackAge 整合 UKB 30,376 人的 2,923 个蛋白与 251 个代谢物，2 型糖尿病、阿尔茨海默病和慢性肾脏病 AUC 超过 0.90 [9]。
- LongevityBench 评测 18 个前沿 AI 系统后结论是没有单一模型主导所有任务，且组学年龄预测被识别为最难的任务 [10]。

## 1 背景与定义

多模态衰老时钟的方向边界，首先由“以何种模态、在何种组织、以何为训练目标”三个维度划定。第一代表观时钟以实际年龄为监督信号，Horvath 的 353 CpG 预测器把衰老时钟从单队列工具变成跨组织可迁移的通用模型 [1]；第二代时钟转向以死亡、疾病、功能衰退等结局为代理，DNAm PhenoAge 用临床表型年龄替代实际年龄 [2]，LinAge2 的评测进一步显示以生存为目标训练的时钟在死亡预测上优于以实际年龄为目标的时钟 [11]。**这一演化脉络意味着“生物年龄”并非单一构念，而是随训练目标变化的一组可操作定义**：预测年龄、预测死亡、预测器官功能衰退，各自对应不同的标志物集合与验证标准。Generation Scotland 对 14 种时钟与 174 种疾病的系统比较，以及 DamAge/AdaptAge 对损伤性与适应性甲基化变化的拆分，从不同角度印证了同一时钟分数可能混合了异质甚至方向相反的生物学过程 [3][12]。

模态扩展是过去十年的主线。蛋白质组时钟在队列规模上推进最快，UKB 45,441 人、2,897 蛋白训练的模型经 Boruta 筛选出 204 个蛋白，并在 CKB 与 FinnGen 中独立验证 [5]；器官特异化路线在 UKB 43,616 人及中国、美国队列中构建整体与十个器官时钟，跨队列 r 达 0.98 和 0.93 [6]。代谢组方向以 274,247 人的 107 种非衍生代谢物构建 5 个 MetBAG，独立测试集 Pearson r 为 0.25<r<0.42 [13]。影像侧，七个 MRIBAG 在留出测试中 r 为 0.23–0.77、MAE 约 5 年 [14]，CT 模型则以 123,281 名成人的 8 个心脏代谢标志物取得 IPA=29.2 [15]。**这些工作的共同特征是：模态越接近临床可及数据，队列规模越大，但单模态时钟对衰老机制的解释力并未同步提升**——蛋白质组与代谢组时钟多依赖 LASSO 类线性模型，其预测性能与所捕获的生物学通路之间的对应关系仍不明确。

多模态整合的核心问题由此从“拼接”转向“对齐与缺失”。StackAge 整合 UKB 30,376 人的 2,923 个蛋白与 251 个代谢物，对 12 种慢性病风险预测增强，2 型糖尿病、阿尔茨海默病和慢性肾脏病 AUC 超过 0.90 [9]；ProtBAG 工作则强调年龄偏倚校正与器官蛋白特异性，并报告整合多器官特征可提升系统性疾病和全因死亡预测 [16]。**但现有整合多停留在同一队列内不同组学层的特征级拼接，跨模态的生物学对齐（如某器官的蛋白年龄与影像年龄是否指向同一衰老过程）尚未成为标准做法**。跨队列泛化是更普遍的薄弱环节：Horvath 和 PedBE 等常用时钟在墨西哥儿童青少年队列预测准确性下降 [17]，OMICmAge 虽在多个独立队列验证，作者仍指出跨队列泛化与临床效用需进一步验证 [18]，mCAS 完全建立在中国人群之上且外部验证未说明 [19]。

单细胞与空间模态把生物年龄的分辨率推到细胞类型层级，同时暴露出新的定义问题。sc-ImmuAging 基于 1081 名健康欧洲人 PBMC 的约 130 万细胞，为五类免疫细胞分别建模，并揭示感染与接种后的年龄改变异质性 [20]；scAgeClock 用门控多头注意力网络在 CZ CELLxGENE 超 7000 万细胞上训练 [21]。空间转录组则显示免疫球蛋白表达细胞聚集是衰老的保守微环境特征，IgG 可诱导促衰老表型 [22]。**细胞类型特异的时钟与通用衰老标志物之间存在张力**：SenePy 发现已知标志物高度细胞类型特异，仅 58/1540 细胞类型组合的标志物重叠显著 [23]，而 hUSI 用 One-Class Logistic Regression 学习通用衰老特征并在多种条件下优于 31 种方法 [24]。这一分歧直接关系到多模态整合的前提：若不存在跨细胞类型的通用衰老轴，则模态间对齐需要以细胞类型为条件，而非在整体水平求平均。

基准与基础模型的兴起，把上述分歧转化为可评测的问题。LongevityBench 覆盖 17 项任务、5 个生物数据域，评测 18 个前沿 AI 系统，结论是没有单一模型主导所有任务，组学年龄预测被识别为最难的任务 [10]；Longevity-LLM v0.1 在 DNA 甲基化、蛋白质组、临床生物标志物和 RNA 表达上微调，强化微调后表观年龄预测 MAE 为 4.34 年 [25]。单细胞基准评估 10 个通用基础模型、3 个衰老专用模型及传统方法，覆盖超过 250 万单细胞转录组，发现冻结预训练表征时 Geneformer 在时序年龄预测上最佳，但 2000 个高变基因平均表现更高 [26]。ComputAgeBench 则以“可靠时钟应能区分健康个体与衰老加速疾病个体”为核心假设，整合 66 个血液 DNA 甲基化数据集、19 种疾病、13 个已发表时钟 [27]。**这些基准的共同发现是：专用小模型与通用大模型、基础模型表征与简单基线之间尚无定论，而评测本身的模态覆盖与任务设计仍在快速变动**。Biolearn 作为统一整理与评估框架，以及 Immunosenescence Inventory 作为免疫衰老多组学数据库，分别从评估标准化与数据汇聚两端支撑这一方向，但均依赖既有公开数据、缺乏统一预测性能基准 [28][29]。

方法学可靠性问题贯穿所有模态。有研究指出常用 ML/AI 连续结局回归模型存在系统预测偏差，可扭曲甚至逆转下游关联 [30]；概率框架从预测年龄分布推导生物年龄不确定性，在超过 45 万名 UKB 参与者中发现 BAU 与 BAG 弱相关 [31]。表观时钟的可靠性评估显示，多数 DNAm 标志物技术重现性好但生物学可靠性仅为低至中等，调整免疫组成后进一步下降 [32]；组织来源影响同样显著，口腔与血液组织的表观年龄平均差近 30 年 [4]。**这些证据共同指向一个尚未被多模态整合充分吸收的约束：时钟输出的稳健性与模态间可比性，是比预测精度更前置的问题**。在干预与临床转化侧，ClockBase Agent 评估 43,602 个干预-对照比较并报告更多干预加速而非延缓衰老 [33]，rentosertib 2a 期试验中六种蛋白质组时钟一致预测治疗组生物年龄更低但无法单独区分衰老与疾病特异效应 [34]，异时心脏移植显示移植物生物年龄快速同化受体年龄 [35]——**这些结果提示生物年龄具有系统环境驱动的可塑性，同时也意味着单次测量的时钟分数难以作为干预终点的充分证据**。

## 2 方法学


### 2.1 单组学衰老时钟（表观 / 蛋白 / 转录）

以实际年龄为训练目标的第一代表观遗传时钟奠定了单组学衰老时钟的方法学基础。Horvath 整合 82 个 Illumina 27K/450K 数据集、7844 个非癌样本，覆盖 51 种组织与细胞类型，用弹性网络回归从 21,369 个共有 CpG 中选出 **353 个 CpG** 构建多组织预测器，测试误差约 **3.6 年**，并显示早衰症样本偏离正常衰老轨迹、iPS 重编程可将表观时钟重置为 0 [1]。该工作同时暴露了单组学时钟的固有约束：仅使用两平台共有位点、训练数据异质、癌症组织被排除、组织覆盖仍有限 [1]。后续综述亦将 Horvath 时钟的 353 CpG 与发育程序假说联系起来，指出时钟位点邻近 Hox、polycomb 等发育基因，且甲基化时钟从胚胎发育到老年持续运行 [36]。

第二代时钟的关键转向是不再以实际年龄为唯一替代终点。DNAm PhenoAge 用包含临床表型年龄的复合指标替代实际年龄，通过两步流程筛选 CpG，在全因死亡、癌症、健康寿命、身体功能、阿尔茨海默病等预测上显著优于第一代标志物，并关联炎症、干扰素及线粒体等通路 [2]。但该工作基于全血开发，摘要未给出样本规模、验证队列和误差指标，机制解释仍有限 [2]。与之呼应，LinAge2 的评测显示，以生存和功能衰老为目标训练的时钟优于以实际年龄为目标训练的时钟：LinAge2 预测死亡的 **AUC=0.8684**，高于 PhenoAge Clinical 的 0.8479 和 ChronAge 的 0.8288；20 年死亡预测 **AUC=0.8440**，高于 PhenoAge DNAm 的 0.7859 和 GrimAge2 的 0.8233 [11]。

大规模无偏比较为代际差异提供了更系统的证据。在 Generation Scotland 队列 18,859 人中，14 种表观遗传时钟与 174 种新发疾病及 10 年全因死亡被统一评估，完全校正模型下 13 种时钟与 57 种疾病共产生 **176 个 Bonferroni 显著关联**，其中 GrimAge v2 和 DunedinPACE 各有 72 个显著关联，而第一代时钟在疾病场景中应用有限 [3]。该研究同时指出其局限：以欧洲裔为主、观察性设计、部分时钟与协变量信息重叠 [3]。另一项工作则从因果维度切入，通过表观全基因组孟德尔随机化识别可能因果影响衰老性状的 CpG，发现现有表观时钟和年龄相关差异甲基化均未富集于这些位点，并据此构建追踪损伤性甲基化变化的 **DamAge** 与适应性变化的 **AdaptAge**；DamAge 与死亡等不良结局相关，AdaptAge 与有益适应相关，两者对短期干预敏感 [12]。

表观时钟的生物学解释与可靠性受到持续质疑。对已建立时钟中预测性 CpG 的分析显示，多数时钟 CpG 不与转录因子结合位点重叠，说明时钟准确性并非主要由 TF 结合动态驱动；但用弱相关非 TFBS CpG 结合噪声稳定特征工程构建的 TFMethyl Clock 仍达到 **MdAE=3.77 年**，优于 Horvath1 的 5.95 年，接近 PhenoAge 的 3.79 年，且移除 88,007 个 CpG 后误差才达随机水平 [37]。可靠性评估则给出更谨慎的结论：在 TranslAGE 平台评估的 18 种 DNAm 标志物中，多数时钟技术重现性好，PCGrimAge 和 SystemsAge 较稳健，但生物学可靠性仅为低至中等，调整免疫组成后进一步下降，且技术重现性不能预测生物学可靠性 [32]。此外，时钟位点在生命早期的行为高度异质且非线性，超过三分之一位点自出生即存在个体差异，高于非时钟位点，并与遗传背景和产前暴露相关 [38]。

组织来源对表观年龄估计的影响构成另一争议点。跨五种组织、284 份样本（83 人，9–70 岁）的比较发现，口腔与血液组织的表观年龄平均差近 **30 年**，多数血液时钟与口腔组织相关性低，**Skin and Blood clock** 跨组织一致性最好 [4]。该研究样本量、组织类型和年龄范围均有限 [4]。为提升机制可解释性，PathwayAge 放弃孤立 CpG 而整合 GO 和 KEGG 通路级甲基化信息，在多队列和疾病组织中验证，能预测年龄并识别神经退行、免疫失调、代谢病相关通路 [39]；其局限在于仍主要基于 DNA 甲基化，通路级解释受组织特异性和队列差异限制 [39]。面向干预应用，TranslAGE 整合 51 项人类纵向干预研究，统一计算 16 种表观时钟和 94 种额外 DNAm 标志物，通过配对比较发现不同干预与时钟响应差异显著，但文献碎片化和时钟面板不一致使跨研究直接比较困难 [40]。

蛋白质组时钟在队列规模和跨人群验证上推进较快。UK Biobank 中 45,441 人、2,897 个血浆蛋白训练的模型经 Boruta 筛选出 **204 个蛋白**，与实际年龄的 Pearson r=0.94，蛋白质组年龄差与 27 个衰老表型、全因死亡和 26 种年龄相关疾病关联，并在 CKB（3,977 人）和 FinnGen（1,990 人）中独立验证 [5]；其局限是主要发现基于 UKB，外部队列样本较小或病例少，观察性关联不能证明因果 [5]。PAC 则直接以全因死亡风险为代理，在 UKB Pharma Proteomics Project 的 53,021 名 39–70 岁参与者、2,923 个 Olink 蛋白上用 LASSO 建模，随访超 10 年，PAC 年龄偏差与全因死亡及多种年龄相关疾病显著关联 [41]；训练仅限 UKB、蛋白平台单一、外部验证有限 [41]。器官特异化是另一条路线：在 UKB 43,616 人及中国 3,977 人、美国 800 人队列中，基于 Olink 2,916 蛋白和非线性机器学习构建整体及十个器官时钟，跨队列 r 分别达 **0.98 和 0.93**，加速的器官衰老可超越临床和遗传风险因素预测疾病发生、进展与死亡，其中脑衰老与死亡关联最强，精简蛋白面板可保持性能 [6]。

蛋白质组时钟的目标也从年龄预测扩展到健康寿命与特定系统。HPS 基于 UKB Pharma Proteomics Project 的 2,920 种蛋白和 53,018 人、随访 13.5 年构建，在 43,119 名基线健康者中 12,427 人（**28.8%**）发生健康寿命终点事件，较低 HPS 与更高死亡风险和慢性阻塞性肺病等年龄相关疾病相关 [42]；其局限包括 UKB 以欧洲裔为主、健康寿命定义尚无共识、外部验证有限 [42]。ECM 时钟则聚焦循环细胞外基质蛋白，发现其随龄呈 **U 型轨迹**、最低点约 40–50 岁，由 14 个血浆蛋白构成的时钟可预测年龄并区分健康与疾病， rejuvenation 干预可逆转 ECM 衰老特征 [43]；但 Robbins 队列最老仅 66 岁、U 型轨迹较弱，蛋白轨迹异质性大 [43]。肌肉骨骼方向构建了 MSKAge 与 MSKAgeMort，在 21,070 名 UKB 参与者中开发，MSKAge 与实际年龄相关 r 女性=0.62、男性=0.56，MSKAgeMort 相关 r 女性=0.93、男性=0.88，其加速指标可预测死亡、肌肉骨骼病和年龄相关病 [44]。

转录组时钟面临平台依赖、组织特异性和可用性等批评。Pasta 采用"age-shift"学习框架，声称可跨组织、数据类型（bulk、单细胞 RNA-Seq、微阵列）和物种预测相对年龄，优于 MultiTIMER 和 tAge，能区分衰老、静息和干细胞状态，p53 相关基因贡献显著，并可分层肿瘤分级和生存 [45]；其局限是转录组噪声和批次效应、跨平台泛化仍受限、部分验证依赖公开扰动数据 [45]。在 ARCHS4 的 56,877 例人类 RNA-seq（2–114 岁、多组织）上，混合专家模型达到 **MAE=7.58 年**，肺和脑预测最佳、肝较差，FOSB 重要性 1.00、C4B_2 为 0.95、PAX8-AS1 为 0.85、MT-RNR2 为 0.64、GFAP 为 0.53，残差随年龄增大，百岁老人误差达 ±40 年 [7]。DeepQA 针对现有方法仅在健康受试者训练却推断健康与非健康受试者的偏倚，采用混合专家与 Hinge-MAE 损失，在 MCATS 数据库 3,060 样本、31 数据集上训练，声称在健康和非健康受试者上均显著优于现有方法 [46]；其局限是依赖公开数据库、非健康样本生物年龄缺乏金标准 [46]。

不确定性量化和多组学整合代表了较新的方向。K-Dense 多智能体系统在 ARCHS4 的 57,584 样本、28 组织、1,039 队列、1–114 岁数据上训练统一集成时钟，达到 **R²=0.854、MAE=4.26 年**，并提供校准置信区间，可标记过渡期和极端年龄预测，发现 CDKN2A/p16、AMPD3、MIR29B2CHG、SEPTIN3 等阶段标志物，85 个重叠窗口显示基因重要性波状变化 [8]。StackAge 则整合 UKB 30,376 人的 2,923 个蛋白与 251 个代谢物，结合线性与非线性学习器，与实际年龄 Pearson r≈0.93，对 12 种慢性病风险预测增强，2 型糖尿病、阿尔茨海默病和慢性肾脏病 AUC 超过 **0.90**，中位随访 11.7 年 [9]；其局限是仅含血浆蛋白与代谢组、未整合表观遗传层、以横断面基线为主 [9]。代谢组方向，MetaboAgeMort 利用 UKB 239,291 人血浆代谢组、以 10 年全因死亡为替代指标，先选 **185 个**死亡相关代谢标志物，再用 LASSO Cox 和 Gompertz 回归建模，训练 167,506、测试 71,785，可提升 10 年死亡预测并关联疾病、可调因素和遗传位点 [47]；其局限是以全因死亡为替代指标、主要欧洲白人样本、外推性受限 [47]。此外，LivAge 作为基于小鼠肝脏 RNA-seq 的转录组时钟，在早衰综合征中显示转录组年龄增加，并可评估 Snell Dwarf、Ames Dwarf、GHR 缺陷及热量限制等干预 [48]；其仅基于肝脏组织、全文未完全公开、验证范围有限 [48]。

### 2.2 多模态整合与跨队列泛化

多模态整合的核心思路是把不同分子层与影像、临床表型拼进同一衰老时钟框架。UK Biobank 血浆蛋白质组（2,916 蛋白、44,498 人）被用来训练 11 个器官年龄 LASSO 模型，脑、动脉和整体年龄预测传统年龄 r²=0.97，器官年龄差与心衰、慢阻肺等未来发病及死亡相关 [49]。同一队列稍小规模（43,498 人、2,448 蛋白）构建的 11 个 ProtBAG 强调年龄偏倚校正与器官蛋白特异性，并报告整合多器官特征可提升系统性疾病和全因死亡预测 [16]。代谢组方向则用 274,247 人的 107 种非衍生代谢物构建 5 个 MetBAG，独立测试集 Pearson r 为 0.25<r<0.42，关联 525 个疾病终点 [13]。影像侧，七个 MRIBAG 在留出测试中 r 为 0.23–0.77、MAE 约 5 年，并关联 2,923 种蛋白和 327 种代谢物 [14]；CT 模型则以 123,281 名成人的 8 个心脏代谢标志物取得 IPA=29.2，优于人口学模型的 21.7 [15]。

跨队列泛化是这些工作共同的薄弱环节。表观遗传时钟方面，Horvath 和 PedBE 等常用时钟在墨西哥儿童青少年队列（523 份血样）预测准确性下降，迁移学习被用来缩小目标数据差距 [17]。OMICmAge 在 MGB 约 31,264 人开发，并在 All of Us 10,769、TruDiagnostic 14,213、Generation Scotland 18,672 等独立队列验证，与慢病和死亡强相关，但作者指出跨队列泛化与临床效用仍需验证 [18]。GOLD BioAge 基于 Gompertz 风险函数构建轻量线性模型，在 CHARLS、CLHLS、RuLAS 三个中国队列验证有效，同时承认跨人群泛化仍需更多验证 [50]。mCAS 则完全建立在中国人群（2,019 人、18–91 岁）之上，其外部验证和跨族群适用性未说明 [19]。这些证据显示，多数时钟的验证仍局限于开发队列或相近人群，跨平台、跨族群的系统比较尚不充分。

方法学争议集中在预测偏差与不确定性。有研究指出常用 ML/AI 连续结局回归模型存在系统预测偏差，可扭曲甚至逆转下游关联，例如产生“预测脑龄越大认知越好”或“表观年龄越大肾功能越好”的虚假关联，约束优化可改善校准和下游推断 [30]。另一项工作提出概率框架，从预测年龄分布的均值和宽度推导 BAG 与生物年龄不确定性（BAU），在超过 45 万名 UK Biobank 参与者中发现 BAU 与 BAG 弱相关，并随个体分子间年龄信号不一致而增加 [31]。这与前述强调年龄偏倚校正的 ProtBAG 工作 [16] 形成呼应：时钟输出的稳健性本身已成为独立问题，而非仅关乎预测精度。

多模态整合也被用于干预筛选和临床试验。ClockBase Agent 整合 40 余种衰老时钟，评估 43,602 个干预-对照比较，发现超 500 种干预显著降低生物年龄，并报告更多干预加速而非延缓衰老、疾病状态多加速生物年龄 [33]。AURORA 生成式多模态框架通过降低年龄差的干预计算筛选，预测 Neisseria flavescens 为顶级候选，并在线虫中验证活菌可延长寿命和健康寿命 [51]。在 12 周 rentosertib 特发性肺纤维化 2a 期试验中，六种蛋白质组时钟（ProtAge、OrganAgemortality、OrganAgechrono、PAC、ipfP3GPT、PAOPAC）一致预测治疗组生物年龄更低，但作者强调蛋白质组时钟无法单独区分衰老与疾病特异效应，需借助通路分析间接区分抗衰老与抗纤维化 [34]。

人群异质性方面，以色列 10K 项目对 1 万名 40–70 岁健康人每 2 年随访，构建多生理系统 BA 评分，揭示男女衰老模式差异，高 BA 与年龄相关疾病患病率升高相关 [52]。这与 mCAS 的三层级框架（核心能力时钟、多模态时钟、器官相关时钟）所报告的血浆蛋白时钟可代理系统生理能力、凝血因子年龄依赖积累驱动多器官衰老和炎症 [19] 一起，提示性别、族群和器官层级都是泛化评估中不可忽略的维度。总体来看，多模态整合已从单一组学扩展到蛋白、代谢、影像、临床与微生物，但跨队列可迁移性、偏差校正和干预特异性仍是尚未收敛的问题。

### 2.3 单细胞与空间衰老图谱

单细胞转录组衰老时钟已从泛化模型走向细胞类型特异。**sc-ImmuAging** 基于1081名18至97岁健康欧洲人PBMC的约130万细胞，用LASSO、随机森林和PointNet为五类免疫细胞分别建模，内外验证优于对照，并揭示COVID-19感染后单核细胞和BCG接种后CD8+T细胞的年龄改变异质性[20]。**scAgeClock** 则用门控多头注意力神经网络，在CZ CELLxGENE超7000万细胞上训练，精度高于偏最小二乘、弹性网等基线[21]。另一条路线把单细胞转录组表示为基因名序列的"细胞句子"，微调预训练大语言模型，在数百万细胞上训练实现单细胞分辨率年龄预测，并提名可降低转录年龄的候选靶点[53]。三者数据规模与建模思路不同，但都指向同一目标：在单细胞层面估计生物学年龄。

空间维度上，小鼠九组织空间转录组显示衰老敏感位点与组织结构熵升高共定位，免疫球蛋白表达细胞聚集是其微环境特征，IgG在雌雄小鼠及人组织中随龄积累，并可诱导巨噬细胞和小胶质细胞促衰老，靶向降低IgG缓解多组织衰老[22]。乳腺多组学图谱比较3月龄与18月龄小鼠，发现上皮AV/HS减少、肌上皮增加，免疫髓系、浆细胞、记忆T增加而naive T减少，成纤维细胞增加，并伴随代谢、促炎和癌症相关基因的表观与转录改变[54]。人皮肤研究构建**SenSkin™**皮肤特异衰老基因集，发现光老化衰老细胞负担高于时序衰老，衰老细胞倾向聚集，衰老黑素细胞黑色素合成升高、衰老网状真皮成纤维细胞胶原和弹性纤维合成下降[55]。人骨骼肌单核多组学则构建首个衰老人肌衰老细胞图谱，解析SASP异质性与动态，并提出Maraviroc作为肌少症治疗候选[56]。

衰老细胞识别方法本身存在争议。**SenePy** 用72个小鼠和64个人类加权单细胞signature构建评分平台，发现其比体外来源signature更能重现体内衰老，且已知标志物高度细胞类型特异——仅58/1540细胞类型组合的标志物重叠显著，Cdkn2a等随龄增加（FDR p=0.01）[23]。**hUSI** 基于73项公开RNA-seq研究、用One-Class Logistic Regression学习通用衰老特征，在bulk和单细胞多种条件下优于31种方法，并适用于COVID-19肺和黑色素瘤组织[24]。两者一强调细胞类型特异、一强调通用性，反映出该领域对"通用衰老标志物是否存在"的分歧；综述亦指出缺乏特异性标志物、衰老细胞稀少且异质动态是核心障碍[57]。

将时钟用于神经元类型可揭示易感性差异。在线虫128种神经元类型中，BitAge与Stochastic Clock预测年龄约98h至177h，近2倍差异，两时钟相关Pearson 0.65（P=5.5×10−17）；高神经肽和蛋白生物合成基因表达的纤毛感觉神经元衰老与退化加速，翻译抑制可预防，丁香酸和vanoxerine被验证可保护神经元[58]。脑衰老综述则从细胞类型中心视角总结年龄相关变化与细胞互作，并评述单细胞组学如何无偏评估年轻化干预[59]。这些工作共同表明，单细胞与空间图谱正把生物年龄从整体测量推进到细胞类型乃至单细胞分辨率，但跨物种泛化与因果验证仍是共同限制。

### 2.4 衰老生物学基准与基础模型

衰老生物学正从单一模态的专用时钟走向跨模态基准与基础模型。**LongevityBench** 覆盖17项任务、5个生物数据域，评测了来自6个开发团队的18个前沿AI系统，结论是**没有单一模型主导所有任务**，且组学年龄预测被识别为最难的任务；同一工作中微调的5个0.6B–9B多任务Longevity-LLM可匹配或超过更大的通用前沿系统[10]。与之呼应，Longevity-LLM v0.1将Qwen3-14B在DNA甲基化、蛋白质组、临床生物标志物和RNA表达上微调，强化微调后表观年龄预测**MAE为4.34年**，超过Horvath多组织时钟，蛋白质组谱生成也显著优于所比较的前沿LLM[25]。在单细胞层面，一项基准评估了10个通用单细胞基础模型、3个衰老专用模型及传统方法，覆盖5个生物学问题、超过250万单细胞转录组，冻结预训练表征时Geneformer在时序年龄预测和年龄伪时间一致性上最佳，但**2000个高变基因平均表现更高**，多个模型在三种疾病背景中捕捉到正向分子年龄偏移[26]。这些结果共同指向一个争议点：专用小模型与通用大模型、基础模型表征与简单高变基因基线之间，谁更适用于衰老任务尚无定论。

在评测标准化的方向上，**ComputAgeBench**提出以“可靠时钟应能区分健康个体与衰老加速疾病个体”为核心假设的统一框架，整合66个公开血液DNA甲基化数据集、覆盖19种衰老加速疾病，测试13个已发表表观遗传时钟模型，并另建46个数据集用于训练新时钟[27]。该工作仅基于血液DNA甲基化，未覆盖其他模态，且未给出具体模型性能数值，这与LongevityBench的多域、多模型覆盖形成互补，也说明现有基准在模态广度与评测深度上各有取舍[27][10]。方法学综述进一步指出，AI驱动的生物年龄预测涵盖生物标志物选择、特征工程、模型开发、偏倚校正和性能评估等环节，当前挑战集中在数据异质性、泛化性有限、可解释性不足和临床转化障碍，未来需多组学与纵向数据整合[60]。另有综述认为AI、集成学习和深度学习正推动临床衰老时钟从表观遗传向多组学、多模态整合，在准确性、可解释性和泛化性方面取得进展，但该文全文不可得，具体数据、验证队列和定量性能无法提取[61]。

应用侧的讨论则把生物年龄预测器与“人类数字孪生”联系起来，认为表观时钟在预测生物年龄和健康表型上较准确，数字孪生可动态模拟干预与风险，但落地受数据整合、隐私、互操作性和纵向建模挑战限制[62]。一篇覆盖2016–2024年125篇同行评审研究的叙述性综述总结了CNN、RNN、GAN、LLM和扩散模型在衰老时钟、合成数据生成、药物发现和多模态健康评估中的应用，但作为综述缺乏定量荟萃分析[63]。针对干预评估，有观点类论文主张AI与LLM的评估应正确、有用、全面、可解释，并考虑因果、跨学科、标准、纵向数据和已知衰老生物学，建议采用LLM结合知识图谱与检索增强生成并开展基准测试，但未提供具体实验验证或定量结果[64]。总体来看，基准建设、基础模型微调与验证要求三条线索并行推进，而模态覆盖、基线选择与临床转化仍是尚未收敛的分歧所在。

### 2.5 类器官、扰动与 Cell Painting 衰老建模

Cell Painting 是一种基于显微成像的细胞标记 assay，旨在捕获细胞状态，并于 2013 年被提出以优化和标准化图像型 profiling [65]。其核心思路是借助现代定量图像分析实现高通量、高内涵成像，并通过图像型 profiling 利用图像中的丰富信息识别生物样本间的相似性或差异，而非像传统高内涵筛选那样只测量少量特征 [65]。该综述指出，**Cell Painting** 能够捕获细胞对多种扰动的响应，十年来其协议、特征提取、质控和批次校正持续改进，并已应用于机制研究、毒性评估和多组学整合等场景 [65]。

作为一篇综述，该工作本身未提供统一的定量基准，其结论依赖公开数据集和计算实验技术的进展 [65]。文章将未来方向指向计算与实验技术的进一步发展、新公开数据集的建立，以及与其他高内涵数据的整合 [65]。就本节关注的类器官、扰动与衰老建模而言，该证据仅提供了 Cell Painting 作为扰动响应成像分析工具的总体定位与方法学演进脉络，未涉及具体的类器官衰老时钟或生物年龄建模结果 [65]。

## 3 数据与资源

面向多模态衰老时钟与生物年龄研究，现有资源可大致分为两类：一类以统一整理与评估既有标志物为目标，另一类以汇聚特定生理系统的多组学数据为目标。**Biolearn** 作为开源库，针对跨人群验证缺乏标准化方法、标志物设计分散、数据集结构不一致等问题，提供整理、协调与系统评估的统一框架，并据此对多种衰老生物标志物开展综合评估，输出可复现的评估流程 [28]。其数据基础为多公开数据集与多种衰老生物标志物，应用场景为跨人群衰老标志物验证与比较，评估维度涵盖性能、稳健性与泛化性 [28]。该工作依赖已有公开数据，临床验证仍待推进 [28]。

另一类资源聚焦免疫系统。**Immunosenescence Inventory** 是面向免疫衰老的多组学数据库，整合单细胞转录组、bulk 转录组、表观组以及 TCR/BCR 等多物种数据，并提供知识 curation、多模态数据集与工具 [29]。其工具包括免疫细胞识别与**免疫时钟**计算，用于评估生物年龄、预测年龄相关疾病和干预影响，覆盖多物种和年龄阶段 [29]。与 Biolearn 以统一评估框架为核心不同，该数据库以数据与工具集成为主，且其局限在于整合依赖已有数据、未提供统一预测性能基准、单细胞免疫衰老覆盖仍有限 [29]。两者在资源定位上形成互补：前者侧重跨数据集标志物评估的标准化，后者侧重免疫衰老多模态数据的汇聚，但均受制于对既有公开数据的依赖。

## 4 应用与结果

在血液与多组织样本中，DNA甲基化年龄差（Δage）与死亡风险的关联得到多队列验证。四个老年人纵向队列的荟萃分析显示，**Δage每高5年全因死亡风险增加21%，校正健康、生活方式与APOE后仍增加16%**，且Δage遗传度为0.43 [66]。随后扩展到13个队列、13,089人（2,734例死亡）的荟萃分析中，Horvath 353 CpG与Hannum 71 CpG时钟估计的表观年龄与实足年龄相关系数为0.65–0.89，年龄加速与全因死亡风险增加相关，且纳入血液细胞组成信息可提升预测 [67]。同一353 CpG时钟用于种族/性别与冠心病分析时，发现表观年龄加速存在种族和性别差异，并与冠心病及相关风险因素相关 [68]。在HIV感染场景中，基于11个甲基化数据集（含血液与脑组织）的比较显示，HIV感染与显著增加的表观年龄加速相关 [69]。

时钟与功能表型的关联则呈现时间维度上的分歧。Lothian Birth Cohort 1936在70、73、76岁三波测量中发现，表观年龄加速与70岁时的步行速度、握力、肺功能和认知能力横断面相关，但**不预测70至76岁间的功能下降** [70]。系统综述与荟萃分析检索299篇文献、提取1050个EAA-因素关联和53种甲基化时钟，对选定配对做随机效应荟萃分析，发现若干EAA与生理、认知、社会和环境因素存在显著汇总关联，并建立四级分类与TEAPEE数据库；但研究异质性大、部分关联证据有限、因果方向不明确 [71]。

在干预与器官层面，多组学时钟被用于评估可塑性与临床结局。40个月二甲双胍干预雄性食蟹猴的研究，基于多组织转录组、DNA甲基化、血浆蛋白与代谢组构建猴衰老时钟，发现**二甲双胍显著延缓衰老指标，脑衰老约回退6年**，并保护脑结构、增强认知，部分由Nrf2激活介导 [72]。异时心脏移植的多组学分析（小鼠与患者）显示，移植心脏的DNA甲基化和基因表达生物年龄快速同化受体年龄，而非保留供体年龄，且该效应仅限移植物、不影响受体全身生物年龄 [35]。另有研究提出干细胞衰老时钟，将生物学年龄偏差与急性髓系白血病临床结局相关联，但具体定量结果与验证细节未在提供文本中给出 [73]。

## 5 评测、可复现性与争议

（本节暂无入库证据）

## 6 空白与趋势

综合上述证据，多模态衰老时钟领域已从单组学年龄预测扩展到跨模态整合、单细胞/空间图谱、基础模型与基准建设，但若干结构性空白仍然清晰。

1. **跨队列、跨族群、跨平台的系统泛化验证仍是最大缺口。** 现有工作多在开发队列或相近人群内验证：OMICmAge 虽在 All of Us、TruDiagnostic、Generation Scotland 等独立队列验证，作者仍指出跨队列泛化与临床效用待验证 [18]；GOLD BioAge 在三个中国队列验证有效，但承认跨人群泛化需更多验证 [50]；mCAS 完全建立在中国人群之上，外部验证与跨族群适用性未说明 [19]；常用表观时钟在墨西哥儿童青少年队列预测准确性下降，需迁移学习弥补 [17]。**目前尚无覆盖多族群、多平台、多模态的统一泛化基准。**

2. **模态覆盖高度不均衡，表观遗传与蛋白质组占主导，影像、代谢、单细胞与空间模态的整合仍处早期。** 蛋白质组时钟已有 UKB 45,441 人 [5]、53,021 人 [41]、43,616 人 [6] 等多套大规模模型，表观时钟亦有 14 种在 18,859 人中无偏比较 [3]；而影像侧 MRIBAG 仅 7 个器官、MAE 约 5 年 [14]，CT 模型仅 8 个心脏代谢标志物 [15]，代谢组 MetBAG 独立测试 r 仅 0.25–0.42 [13]。**真正把蛋白、代谢、影像、表观与临床表型在同一框架内联合建模并做消融比较的工作仍然稀缺**，StackAge 仅整合蛋白与代谢两层且未纳入表观遗传 [9]。

3. **单细胞与空间衰老时钟尚未与整体生物年龄框架打通。** sc-ImmuAging 基于 1081 人约 130 万 PBMC 细胞 [20]，scAgeClock 在 CZ CELLxGENE 超 7000 万细胞上训练 [21]，但两者均聚焦转录组单层，未与表观、蛋白或影像层对齐；空间图谱方面，小鼠九组织空间转录组 [22]、乳腺多组学图谱 [54]、人骨骼肌单核多组学 [56] 均提供了衰老的空间/细胞类型特征，但**尚未有工作把这些空间特征转化为可跨组织、跨队列应用的生物年龄估计器**。

4. **衰老细胞识别与通用衰老标志物是否存在仍无共识，直接影响单细胞衰老建模的可比性。** SenePy 发现已知标志物高度细胞类型特异，仅 58/1540 细胞类型组合的标志物重叠显著 [23]；hUSI 则用 One-Class Logistic Regression 学习通用衰老特征并在多种条件下优于 31 种方法 [24]；综述亦指出缺乏特异性标志物、衰老细胞稀少且异质动态是核心障碍 [57]。**两种路线（细胞类型特异 vs 通用）的对立尚未通过统一基准解决。**

5. **AI 基准与基础模型刚起步，专用小模型与通用大模型、基础模型表征与简单基线之间谁更适用尚无定论。** LongevityBench 覆盖 17 项任务、5 个数据域、18 个前沿系统，结论是没有单一模型主导所有任务，组学年龄预测最难 [10]；Longevity-LLM v0.1 在表观年龄预测 MAE 为 4.34 年 [25]；单细胞基础模型基准覆盖超 250 万细胞，发现冻结预训练表征时 Geneformer 最佳，但 2000 个高变基因平均表现更高 [26]；ComputAgeBench 仅基于血液 DNA 甲基化、未覆盖其他模态 [27]。**现有基准在模态广度与评测深度上各有取舍，尚无同时覆盖多模态、多族群、多任务的统一评测平台。**

6. **预测偏差与不确定性量化正成为独立方法学问题，但尚未被纳入时钟开发的标准流程。** 有研究指出常用 ML/AI 连续结局回归模型存在系统预测偏差，可产生虚假甚至方向相反的下游关联 [30]；概率框架从预测年龄分布推导 BAG 与生物年龄不确定性，在超 45 万 UKB 参与者中发现 BAU 与 BAG 弱相关 [31]；ProtBAG 工作亦强调年龄偏倚校正 [16]。**目前多数时钟论文仍只报告 MAE 或相关系数，未系统报告偏差校正与不确定性区间。**

7. **类器官、扰动与 Cell Painting 体系中的衰老建模几乎空白。** Cell Painting 综述仅提供该 assay 作为扰动响应成像分析工具的总体定位与方法学演进，未涉及具体的类器官衰老时钟或生物年龄建模结果 [65]。ClockBase Agent 虽评估了 43,602 个干预-对照比较 [33]，AURORA 通过生成式框架筛选并在线虫验证候选干预 [51]，但**这些工作均未把类器官或 Cell Painting 体系中的衰老表型转化为可校准的生物年龄读数**，扰动体系与整体生物年龄时钟之间缺少映射。

8. **干预特异性与疾病-衰老解耦仍是未解问题。** rentosertib 2a 期试验中六种蛋白质组时钟一致提示治疗组生物年龄更低，但作者强调蛋白质组时钟无法单独区分衰老与疾病特异效应，需借助通路分析间接区分 [34]；ClockBase Agent 报告更多干预加速而非延缓衰老、疾病状态多加速生物年龄 [33]。**如何设计能区分“抗衰老”与“抗疾病”效应的时钟或基准，目前没有公认方案。**

9. **纵向动态与增量学习尚未成为主流。** 现有大规模时钟多为横断面训练：MetaboAgeMort 以 10 年全因死亡为替代指标 [47]，PAC 随访超 10 年但为基线建模 [41]，OMICmAge 亦以基线为主 [18]。Lothian Birth Cohort 1936 的三波测量显示表观年龄加速与 70 岁功能横断面相关但不预测 70–76 岁功能下降 [70]，**提示横断面时钟与纵向衰老速率可能是不同构念**，但纵向增量学习时钟仍稀缺。

10. **资源与标准化建设已有起步，但覆盖不均。** Biolearn 提供统一整理、协调与评估框架 [28]，Immunosenescence Inventory 整合免疫衰老多组学数据并提供免疫时钟工具 [29]，但前者依赖已有公开数据、临床验证待推进，后者未提供统一预测性能基准、单细胞免疫衰老覆盖有限。**面向多模态衰老时钟的公共数据资源、系数公开与可复现评测流程仍不完整。**

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 单组学衰老时钟（表观/蛋白/转录） | 成熟 | 表观时钟已有 Horvath 2013 [1] 与 PhenoAge [2] 这类被反复引用、系数公开的锚点工作，说明方法框架已收敛；同时蛋白组时钟 [5] 与因果增强表观年龄 [12] 仍在拓展新模态与因果解释，属于「成熟但仍有增量空间」，不是夕阳。 |
| 2.2 多模态整合与跨队列泛化 | 朝阳 | 雷达样本中该节 **n=15、近两年占比 0.92、CNS 占比 0.53**，且时间跨度仅 2024–2026，说明近两年集中爆发；血浆蛋白组连接脑-免疫衰老 [49]、MRI 多器官时钟 [14] 代表影像+组学整合刚起步，方法尚未收敛。 |
| 2.3 单细胞与空间衰老图谱 | 朝阳 | 空间转录组揭示免疫球蛋白相关衰老 [22] 与单细胞免疫衰老时钟揭示个体异质性 [20] 均为 2024–2025 新工作，说明单细胞/空间分辨率下的衰老建模正在快速扩张；乳腺单细胞衰老图谱 [54] 进一步支持图谱类资源仍在积累，方法未定型。 |
| 2.4 衰老生物学基准与基础模型 | 萌芽 | 已有 ComputAgeBench 表观时钟基准 [27] 和 AI 干预评估验证要求 [64]，说明基准意识出现；但雷达样本中该节 **n=9、median_citations=0、CNS 占比 0.11**，且多为观点/框架类，尚缺大规模可复现基础模型，故判萌芽。 |
| 2.5 类器官、扰动与 Cell Painting 衰老建模 | 证据不足 | 雷达样本中该节仅 **n=1**，即 Cell Painting 十年综述 [65]，它本身不是衰老建模专用工作，无法与第二篇衰老/类器官扰动证据互证，故阶段写证据不足。 |
| 3 数据与资源 | 萌芽 | 统一衰老生物标志物 curation/evaluation 框架 [28] 与免疫衰老多组学数据库 [29] 均为 2025 年新资源，说明数据层正在起步；但雷达样本中该节 **n=2**，尚不足以判朝阳。 |
| 4 应用与结果 | 成熟 | DNA 甲基化年龄预测全因死亡 [66] 与表观时钟 meta 分析预测寿命 [67] 是 2015–2016 的高引应用验证，说明单组学时钟的临床/流行病学关联已被反复确认；该节 **median_citations=524**，属于成熟应用层，增量为主。 |
| 5 评测、可复现性与争议 | 证据不足 | 雷达样本中该节 **n=0**，无任何给定 [id] 可引用，无法判断阶段。 |

**整体判断**：这个方向整体处于「单组学时钟成熟、多模态与单细胞/空间衰老建模朝阳、基准与类器官扰动萌芽」的叠加阶段。雷达样本中 **n=74、近两年占比 0.7、CNS 占比 0.31**，说明近两年是明显加速期；但加速主要集中在 2.2 多模态整合与 2.3 单细胞/空间图谱，而不是传统表观时钟。窗口期我判断还有 **约 2–3 年**：多模态整合的方法尚未收敛，跨队列、缺失模态、纵向增量学习还没有形成像 Horvath/PhenoAge 那样的默认标准；单细胞/空间衰老时钟也还没有统一评测。最大不确定性是 **基准与可复现性缺位**——2.4 和 5 两节在雷达样本中分别只有 **n=9、n=0**，意味着大量新时钟可能无法公平比较，谁先做出被社区接受的 benchmark 或 foundation model，谁就可能重新定义赛道。

**接下来怎么做**：
1. **切入「多模态缺失模态 + 跨队列校正」的衰老时钟**：用公共大队列（UK Biobank、CHARLS、NHANES 等）的表观/蛋白/代谢/影像，做模态对齐与缺失模态补全，产出可迁移的生物年龄估计器。现在做是因为 2.2 近两年爆发但方法未收敛 [49] [14]，且跨队列泛化仍是痛点。
2. **把单细胞/空间衰老图谱转成「细胞类型特异时钟」**：用公开单细胞/空间衰老数据，训练细胞类型分辨率的衰老评分，并在独立组织验证。现在做是因为单细胞免疫衰老时钟已显示个体异质性 [20]，空间图谱也刚起步 [22]，但细胞类型特异时钟尚未标准化。
3. **与合作项目的类器官 + 多组学结合，做扰动体系中的衰老/年轻化建模**：用类器官扰动 + 转录组/表观组/cell painting，建立「扰动-衰老状态」预测模型。现在做是因为 2.5 在雷达样本中仅 **n=1** [65]，属于明显空白；但 Cell Painting 已证明成像表型可规模化，适合与类器官多组学拼接。
4. **优先做衰老时钟 benchmark / 可复现评测，而不是再发一个时钟**：整合公开系数与数据，复现并比较表观、蛋白、转录、多模态时钟，产出开源 benchmark。现在做是因为 ComputAgeBench 已出现 [27]，统一 curation 框架也在 2025 年出现 [28]，但雷达样本中评测争议节 **n=0**，先占位收益高。
5. **用公共数据做 demo，验证「纵向/增量学习」的衰老速率模型**：用有重复随访的队列，建模个体衰老速率而非横截面年龄，并测试增量学习对跨队列漂移的鲁棒性。现在做是因为 2.1 的成熟时钟多为横截面 [1] [2]，而 2.2 的纵向/增量方法尚未收敛 [52]，这是博后算法切入的低成本高差异点。

## 参考文献

1. DNA methylation age of human tissues and cell types. Genome Biology 2013. https://doi.org/10.1186/gb-2013-14-10-r115
2. An epigenetic biomarker of aging for lifespan and healthspan. bioRxiv 2018. https://doi.org/10.18632/aging.101414
3. An unbiased comparison of 14 epigenetic clocks in relation to 174 incident disease outcomes.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66106-y
4. Cross-tissue comparison of epigenetic aging clocks in humans.. Aging cell 2025. https://doi.org/10.1111/acel.14451
5. Proteomic aging clock predicts mortality and risk of common age-related diseases in diverse populations. Nature Medicine 2023. https://doi.org/10.1038/s41591-024-03164-7
6. Organ-specific proteomic aging clocks predict disease and longevity across diverse populations.. Nature aging 2025. https://doi.org/10.1038/s43587-025-01016-8
7. Transcriptomic age prediction using mixture-of-experts models reveals tissue-specific aging signatures in large-scale human RNA-sequencing data. medRxiv 2025. https://doi.org/10.1101/2025.06.28.25330474
8. Guided multi-agent AI invents highly accurate, uncertainty-aware transcriptomic aging clocks. bioRxiv 2025. https://doi.org/10.1101/2025.09.08.674588
9. StackAge: an ensemble-based clock for precise quantification of biological age using multi-omics data.. Briefings in bioinformatics 2026. https://doi.org/10.1093/bib/bbag271
10. An open benchmark and language models for AI in aging biology.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.026
11. LinAge2: providing actionable insights and benchmarking with epigenetic clocks.. npj aging 2025. https://doi.org/10.1038/s41514-025-00221-4
12. Causality-Enriched Epigenetic Age Uncouples Damage and Adaptation. bioRxiv 2023. https://doi.org/10.1038/s43587-023-00557-0
13. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
14. MRI-based multi-organ clocks for healthy aging and disease assessment.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03999-8
15. Biological age model using explainable automated CT-based cardiometabolic biomarkers for phenotypic prediction of longevity.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56741-w
16. Refining the generation, interpretation and application of multi-organ, multi-omics biological aging clocks.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00928-9
17. BRIDGING THE GAP: ENHANCING THE GENERALIZABILITY OF EPIGENETIC CLOCKS THROUGH TRANSFER LEARNING.. The annals of applied statistics 2026. https://doi.org/10.1214/26-aoas2136
18. OMICmAge quantifies biological age by integrating multi-omics with electronic medical records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01073-7
19. Multimodal clocks of human aging.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.025
20. Single-cell immune aging clocks reveal inter-individual heterogeneity during infection and vaccination.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00819-z
21. scAgeClock: a single-cell transcriptome-based human aging clock model using gated multi-head attention neural networks.. npj aging 2026. https://doi.org/10.1038/s41514-026-00379-5
22. Spatial transcriptomic landscape unveils immunoglobin-associated senescence as a hallmark of aging.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.019
23. Unveiling the cell-type-specific landscape of cellular senescence through single-cell transcriptomics using SenePy.. Nature communications 2025. https://doi.org/10.1038/s41467-025-57047-7
24. A transcriptome-based human universal senescence index (hUSI) robustly predicts cellular senescence under various conditions.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00886-2
25. The End of Aging Clocks: Training Foundation Models to Reason in Aging and Longevity. bioRxiv 2026. https://doi.org/10.64898/2026.03.28.714980
26. Benchmarking single-cell foundation models for aging biology.  . https://doi.org/10.64898/2026.09.21.753191
27. ComputAgeBench: Epigenetic Aging Clocks Benchmark. bioRxiv 2025. https://doi.org/10.1145/3711896.3737382
28. A unified framework for systematic curation and evaluation of aging biomarkers.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00987-y
29. Immunosenescence Inventory-a multi-omics database for immune aging research.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1102
30. Trustworthy ML/AI for Aging Clocks: Preventing Systematic Prediction Bias in Biological Age Estimation. bioRxiv 2026. https://doi.org/10.64898/2026.05.27.728155
31. Uncertainty redefines biological age.  . https://doi.org/10.64898/2026.09.26.26364091
32. Biological Versus Technical Reliability of Epigenetic Clocks and Implications for Disease Prognosis and Intervention Response.. Aging cell 2026. https://doi.org/10.1111/acel.70635
33. Autonomous AI Agents Discover Aging Interventions from Millions of Molecular Profiles. bioRxiv 2025. https://doi.org/10.1101/2023.02.28.530532
34. Integration of proteomic aging clocks in a phase 2a clinical trial supports simultaneous geroprotective assessment.. Nature Biotechnology 2026. https://doi.org/10.1038/s41587-026-03286-y
35. Transplanted hearts assimilate the recipient’s biological age. bioRxiv 2026. https://doi.org/10.64898/2026.09.15.751836
36. Epigenetic clocks and programmatic aging.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102546
37. Enhancing the performance and interpretability of epigenetic clocks.. Nucleic acids research 2026. https://doi.org/10.1093/nar/gkag661
38. Characterising developmental dynamics of adult epigenetic clock sites.. EBioMedicine 2024. https://doi.org/10.1016/j.ebiom.2024.105425
39. Decoding disease-specific ageing mechanisms through pathway-level epigenetic clock: insights from multi-cohort validation.. EBioMedicine 2025. https://doi.org/10.1016/j.ebiom.2025.105829
40. Responsiveness of epigenetic aging biomarkers to longevity interventions in humans.. Nature medicine 2026. https://doi.org/10.1038/s41591-026-04562-9
41. Proteomic aging clock (PAC) predicts age‐related outcomes in middle‐aged and older adults. Aging Cell 2024. https://doi.org/10.1111/acel.14195
42. A proteomic signature of healthspan.. Proceedings of the National Academy of Sciences of the United States of America 2025. https://doi.org/10.1073/pnas.2414086122
43. An Extracellular Matrix Aging Clock Based on Circulating Matrisome Proteins Predicts Biological Aging and Disease.. Aging cell 2026. https://doi.org/10.1111/acel.70474
44. Construction and Validation of Plasma Protein-Based Musculoskeletal Biological Age and Genetic and Environmental Risk Profiles.. Aging cell 2026. https://doi.org/10.1111/acel.70636
45. Pasta, a Versatile Transcriptomic Clock, Maps the Chemical and Genetic Determinants of Aging and Rejuvenation. bioRxiv 2025. https://doi.org/10.1002/advs.76740
46. DeepQA: A Unified Transcriptome-Based Aging Clock Using Deep Neural Networks.. Aging cell 2025. https://doi.org/10.1111/acel.14471
47. A Novel Metabolomic Aging Clock Predicting Health Outcomes and Its Genetic and Modifiable Factors. Advancement of science 2024. https://doi.org/10.1002/advs.202406670
48. LivAge: An Online Aging Clock for Murine Transcriptomic Age Estimation.. Aging cell 2026. https://doi.org/10.1111/acel.70677
49. Plasma proteomics links brain and immune system aging with healthspan and longevity.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03798-1
50. Gompertz Law-Based Biological Age (GOLD BioAge): A Simple and Practical Measurement of Biological Ageing to Capture Morbidity and Mortality Risks.. Advanced science (Weinheim, Baden-Wurttemberg, Germany) 2025. https://doi.org/10.1002/advs.202501765
51. Multi-modality profiling identifies Neisseria flavescens as a central geroprotective oral commensal in humans.. Nature aging . https://doi.org/10.1038/s43587-026-01220-0
52. Phenome-wide associations of human aging uncover sex-specific dynamics.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00734-9
53. Universal Single-Cell Transcriptomic Aging Clock powered by LLMs reveals targets to slow cellular aging. Innovation in aging 2025. https://doi.org/10.1093/geroni/igaf122.4305
54. Comprehensive single-cell aging atlas of healthy mammary tissues reveals shared epigenomic and transcriptomic signatures of aging and cancer.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00751-8
55. Mapping epidermal and dermal cellular senescence in human skin aging.. Aging cell 2024. https://doi.org/10.1111/acel.14358
56. Multiomics and cellular senescence profiling of aging human skeletal muscle uncovers Maraviroc as a senotherapeutic approach for sarcopenia.. Nature communications 2025. https://doi.org/10.1038/s41467-025-61403-y
57. Advancing biological understanding of cellular senescence with computational multiomics.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02314-y
58. Aging clocks delineate neuron types vulnerable or resilient to neurodegeneration and identify neuroprotective interventions.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01067-5
59. Brain aging and rejuvenation at single-cell resolution.. Neuron 2025. https://doi.org/10.1016/j.neuron.2024.12.007
60. Artificial intelligence approaches in biological age prediction: current status and challenges.. British journal of biomedical science 2026. https://doi.org/10.3389/bjbs.2026.16141
61. The Evolving Landscape of Clinical Aging Clocks: From Epigenetic to Multi-Omics Integration.. Aging cell 2026. https://doi.org/10.1111/acel.70579
62. From ageing clocks to human digital twins in personalising healthcare through biological age analysis.. NPJ digital medicine 2025. https://doi.org/10.1038/s41746-025-01911-9
63. Deep learning and generative artificial intelligence in aging research and healthy longevity medicine.. Aging 2025. https://doi.org/10.18632/aging.206190
64. Validation Requirements for AI-based Intervention-Evaluation in Aging and Longevity Research and Practice. Ageing Research Reviews 2024. https://doi.org/10.1016/j.arr.2024.102617
65. Cell Painting: a decade of discovery and innovation in cellular imaging.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02528-8
66. DNA methylation age of blood predicts all-cause mortality in later life. Genome Biology 2015. https://doi.org/10.1186/s13059-015-0584-6
67. DNA methylation-based measures of biological age: meta-analysis predicting time to death. Aging 2016. https://doi.org/10.18632/aging.101020
68. An epigenetic clock analysis of race/ethnicity, sex, and coronary heart disease. Genome Biology 2016. https://doi.org/10.1186/s13059-016-1030-0
69. HIV-1 Infection Accelerates Age According to the Epigenetic Clock. Journal of Infectious Diseases 2015. https://doi.org/10.1093/infdis/jiv277
70. The epigenetic clock is correlated with physical and cognitive fitness in the Lothian Birth Cohort 1936. International Journal of Epidemiology 2015. https://doi.org/10.1093/ije/dyu277
71. Breaking new ground on human health and well-being with epigenetic clocks: A systematic review and meta-analysis of epigenetic age acceleration associations.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102552
72. Metformin decelerates aging clock in male monkeys.. Cell 2024. https://doi.org/10.1016/j.cell.2024.08.021
73. A stem cell aging clock links biological age deviation to clinical outcome in acute myeloid leukemia. bioRxiv 2026. https://doi.org/10.64898/2026.02.12.703707
74. A blood-based epigenetic clock for intrinsic capacity predicts mortality and is associated with clinical, immunological and lifestyle factors.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00883-5
