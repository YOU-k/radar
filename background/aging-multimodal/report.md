# 多模态衰老时钟与生物年龄 · 方向背景报告

证据 88 篇 · 覆盖度 0.63 · 第 12 轮 · 更新 2026-11-22 · 数字核验删句 2

## 本次变更

- 新增 [70] A spatiotemporal atlas of maturation and aging of the male monkey hypothalamic-pituitary-testicular axis.
- 新增 [73] GenVinci reconstructs 3D molecular tissue scenes from histology to map senescence across aging and disease
- 新增 [79] LACA: a cross-species single-cell resource for exploring longevity and aging-associated cellular and molecular programs.

## 摘要（TL;DR）

- 表观遗传时钟以 Horvath 多组织预测器为第一代范式代表，从 21,369 个 CpG 中选出 353 个时钟 CpG，多数组织预测误差约 3.6 年 [1]。
- 第二代时钟转向以表型或结局为训练目标，DNAm PhenoAge 在全因死亡、癌症、健康寿命等预测上显著优于第一代指标 [2]。
- Generation Scotland 队列 18,859 人的系统比较显示，完全校正模型下 13 种时钟与 57 种疾病共 176 个 Bonferroni 显著关联，GrimAge v2 和 DunedinPACE 各 72 个 [3]。
- 跨组织适用性是尖锐争议：284 份口腔与血液样本比较发现表观年龄估计平均差近 30 年，Skin and Blood clock 跨组织一致性最好 [4]。
- 蛋白组时钟规模优势明显，UK Biobank 基于 2,897 个血浆蛋白、45,441 人训练并筛选出 204 个蛋白，与实际年龄 Pearson r=0.94 [5]。
- 器官分辨蛋白时钟在跨队列中验证，整体加十个器官特异时钟在中国（3,977 人）和美国（800 人）队列跨队列 r 分别为 0.98 和 0.93 [6]。
- 大规模转录组时钟精度可比但不宜直接比较：ARCHS4 56,877 例模型 MAE=7.58 年 [7]，K-Dense 在 57,584 样本上达 R²=0.854、MAE=4.26 年 [8]。
- 跨队列泛化被直接量化：523 份儿童青少年血样中常用时钟目标队列预测准确性下降，迁移学习可缩小目标数据差距 [9]。
- 方法学风险包括系统预测偏差可制造方向相反的虚假关联 [10]，以及生物年龄不确定性 BAU 与 BAG 仅弱相关、随分子间年龄信号不一致而增加 [11]。
- 单细胞衰老时钟推进到细胞类型层面，sc-ImmuAging 基于 1081 名 18 至 97 岁健康欧洲人 PBMC 的约 130 万细胞建模 [12]，但外部验证有限、组织覆盖偏血液 [12][13]。
- 细胞衰老标志物存在通用性争议：SenePy 发现仅 58/1540 个细胞类型组合的标志物重叠显著 [14]，hUSI 则称在 bulk 和单细胞多种条件下优于 31 种方法 [15]。
- 基准与基础模型并存：LongevityBench 评估 18 个前沿 AI 系统后结论是没有单一模型主导所有任务 [16]，Longevity-LLM v0.1 报告表观年龄预测 MAE 为 4.34 年 [17]。
- 现有基准各自局限于单一模态，ComputAgeBench 仅基于血液 DNA 甲基化、未覆盖其他模态 [18]，跨模态可比性仍缺统一口径。
- 干预与可塑性证据开始出现：40 个月二甲双胍干预雄性食蟹猴使脑衰老约回退 6 年 [19]，异时心脏移植显示移植心脏生物年龄快速同化受体年龄且该效应仅限移植物 [20]。
- 纵向多组学被提出用于刻画个体化衰老轨迹，但现有摘要未提供可提取的方法与定量结果，尚不足以支撑具体结论 [21]。

## 1 背景与定义

表观遗传时钟的成熟并未自动带来“生物年龄”定义的统一。Horvath 353 CpG 时钟以实际年龄为训练目标、跨组织误差约 3.6 年 [1]，但后续工作反复表明，以实际年龄为标签的模型与以结局为标签的模型在临床效用上并不等价：14 种时钟对 174 种新发疾病的系统比较中，第二代与第三代时钟显著优于第一代 [3]；LinAge2 在同一研究内报告 20 年死亡预测优于 PhenoAge DNAm 与 GrimAge2 [22]。**因此本方向的核心边界不是“能否预测年龄”，而是“预测什么、在谁身上、用于何种推断”**——年龄、死亡、疾病、健康寿命与内在能力是不同目标，跨研究数字不可互换。内在能力表观时钟以 91 个 CpG 预测死亡并关联临床、免疫与生活方式因素 [23]，正是这一目标分化的体现。

从单组学到多组学的演化脉络中，**“多器官”先于“多模态”出现**。这些工作的共同前提是器官富集蛋白/特征的可定义性，而方法学综述明确指出年龄偏倚校正与器官蛋白特异性是框架成立的前提 [24]。**多模态整合的真正难点不在拼接，而在模态间的信号不一致与缺失模态处理**：概率框架显示生物年龄不确定性随个体分子间年龄信号不一致而增加 [11]，系统预测偏差还会制造方向相反的虚假下游关联 [10]。

跨组织与跨队列泛化是本方向最尖锐的未解问题。颊上皮与血液的表观年龄估计平均差近 30 年，多数血液时钟与口腔组织相关性低 [4]；儿童青少年血样中常用时钟的目标队列准确性下降，需迁移学习补救 [9]；MRIBAG 作者自述腹部特征共线性导致泛化较差、脑模型存在域偏移 [25]。**同一生物库内的随机留出集表现不能等同于跨人群泛化**，这是当前大量时钟报告高 r 值时最容易被忽略的限定。Biolearn 试图以统一整理、协调与评估框架应对标志物设计分散与数据集结构不一致 [26]，但其依赖已有公开数据、临床验证仍待推进 [26]。

单细胞与空间图谱把“生物年龄”推进到细胞类型分辨率，同时暴露出标志物通用性的分歧。sc-ImmuAging 在 1081 名健康成人约 130 万 PBMC 上建立五类免疫细胞特异时钟 [12]，scAgeClock 以门控多头注意力覆盖 400 余种细胞类型、40 余种组织 [13]；而 SenePy 发现仅 58/1540 个细胞类型组合的衰老标志物重叠显著，主张高度细胞类型特异 [14]，hUSI 则从 73 项研究学习通用特征并称优于 31 种方法 [15]。**两者结论相反，部分源于评测任务与负样本质量不同，目前没有跨任务统一的裁决性基准** [14][15]。空间图谱提供了机制线索——IgG 积累作为保守衰老特征可被靶向缓解 [27]，人乳腺呈现衰老与癌症共享的表观与转录特征 [28]——但多数图谱为描述性，缺乏跨物种因果验证。

基准与基础模型的兴起正在重塑评价方式，但**现有基准各自局限于单一模态**。LongevityBench 以 17 项任务、5 个数据域评测 18 个前沿系统，结论是没有单一模型全能、组学年龄预测最难，小型专用 Longevity-LLM 可匹配更大通用模型 [16]；ComputAgeBench 仅基于血液 DNA 甲基化、覆盖 19 种疾病与 13 个已发表时钟 [18]；单细胞基准限于转录组表征，且 2000 个高变基因的平均表现高于冻结预训练表征 [29]。Longevity-LLM v0.1 报告表观年龄 MAE 4.34 年 [17]，与上述基准任务集和口径不同，不能直接比较高下。**跨模态可比性、因果与干预验证的缺失，是当前 AI 衰老基准最明确的空白**；有观点文章主张评估应兼顾因果、纵向数据与已知衰老生物学，但未提供实验验证 [30]。

扰动与类器官体系为“时钟读出”提供了因果检验场景，但证据仍零散。人成纤维细胞中可解释转录组年龄预测器驱动的 cDNA 过表达筛选鉴定出 SRSF1，诱导年轻化转录特征且不丧失细胞身份 [31]；Cell Painting 作为成像表型读出已标准化十年，可用于机制与多组学整合 [32]，但与转录组筛选尚无可直接对照的同一研究内证据。跨物种脂质组学发现脂酰链延长是保守衰老标志、表现为比值性重塑，饮食限制可缩短小鼠心脏脂质 [33]，提示**代谢/脂质层可能提供比甲基化更接近机制的读出**，但其在人类多组织与疾病背景下的普遍性仍待验证。总体而言，本方向的边界应被表述为：**以多组学、影像与功能表型估计生物年龄与衰老速率的模型体系，其有效性取决于目标结局、组织来源、队列构成与评测口径四者的显式匹配**；脱离这四项限定的“生物年龄”数字不具备跨研究可比性。

## 2 方法学


### 2.1 单组学衰老时钟（表观 / 蛋白 / 转录）

表观遗传时钟是单组学衰老时钟中发展最成熟的一支。Horvath 多组织预测器整合 82 个 Illumina 27K/450K 数据集、7844 个非癌样本，用弹性网络回归从 21,369 个 CpG 中选出 **353 个时钟 CpG**，在多数组织中预测误差约 **3.6 年**，并显示早衰症不符合正常衰老、iPS 重编程可将表观时钟重置为 0 [1]。该工作奠定了「以实际年龄为训练目标」的第一代时钟范式，其局限也明确：仅用两平台共有的 21,369 个 CpG，训练/测试数据存在异质性，癌症组织被排除 [1]。

第二代时钟转而以表型或结局为训练目标。DNAm PhenoAge 用包含临床表型年龄的复合指标替代实际年龄，通过两步流程筛选 CpG，在全因死亡、癌症、健康寿命、身体功能和阿尔茨海默病预测上显著优于第一代指标，并关联炎症、干扰素及线粒体等通路 [2]。但该研究基于全血开发，摘要未给出样本规模、验证队列和误差指标 [2]。更激进的思路来自因果信息：通过表观全基因组孟德尔随机化识别可能因果影响衰老性状的 CpG，构建追踪损伤性变化的 **DamAge** 与适应性变化的 **AdaptAge**，前者与死亡等不良结局相关，后者与有益适应相关，且两者对短期干预敏感 [34]；其限制在于因果 CpG 的功能验证有限、依赖 MR 假设 [34]。

时钟的临床效用需要横向比较才能判断。一项基于 Generation Scotland 队列 **18,859 人**的系统比较，将 14 种常用时钟与 174 种新发疾病及 10 年全因死亡关联，完全校正模型下 13 种时钟与 57 种疾病共 176 个 Bonferroni 显著关联，**GrimAge v2 和 DunedinPACE 各 72 个**显著关联，第二代和第三代时钟显著优于第一代，后者在疾病场景应用有限 [3]。LinAge2 的评测给出同研究内部的对照：20 年全因死亡预测 **AUC=0.8684**，优于 PhenoAge Clinical 的 0.8479 和 ChronAge 的 0.8288；20 年死亡 AUC=0.8440，优于 PhenoAge DNAm 的 0.7859 和 GrimAge2 的 0.8233 [22]。这些结果支持「以生存和功能衰老为训练目标的时钟优于以实际年龄为目标的时钟」，但 LinAge2 部分对比未达统计显著，且未满足理想时钟全部标准 [22]。

表观时钟的生物学解释仍是争议点。对已建立时钟中预测性 CpG 的分析显示，多数时钟 CpG 并不与已知转录因子结合位点重叠，说明时钟准确性并非主要由 TF 结合动态驱动；但用弱相关非 TFBS CpG 结合噪声稳定特征工程构建的 **TFMethyl Clock** 达到 **MdAE=3.77 年**，优于 Horvath1 的 5.95 年、接近 PhenoAge 的 3.79 年，且移除 88,007 个 CpG 后误差才达随机水平 [35]。另一条路径放弃单 CpG，改用 GO/KEGG 通路级甲基化构建 **PathwayAge**，在多队列和疾病组织中验证，能预测年龄并识别神经退行、免疫失调、代谢病相关通路，提升机制解释性 [36]。与之呼应，综述性工作指出 Horvath 时钟的 353 个 CpG 邻近 Hox 和 polycomb 等发育基因，表观时钟从胚胎发育到老年持续运行，支持发育程序驱动衰老的假说 [37]；但该文为综述，缺乏原始实验验证，部分观点属推测 [37]。

时钟位点在生命早期的行为为「早期起源」假说提供了直接证据。将成人时钟分解到单个 CpG 后发现，时钟位点发育轨迹高度异质且非线性，超过三分之一位点自出生即存在个体差异，比例高于非时钟位点，且出生时的变异与遗传背景和产前暴露相关 [38]。该研究聚焦生命前二十年，成人疾病结局未直接验证 [38]。

跨组织适用性是表观时钟最尖锐的方法学争议。对 83 名 9–70 岁个体的 284 份颊上皮、唾液、干血斑、白细胞层和外周血单核细胞样本比较发现，口腔与血液组织的表观年龄估计**平均差近 30 年**，多数血液时钟与口腔组织相关性低，**Skin and Blood clock** 跨组织一致性最好 [4]。这直接挑战了把血液训练时钟外推到口腔等微创样本的做法，尽管该研究样本量和组织类型有限 [4]。

可靠性问题同样不容忽视。在干预响应层面，整合 51 项人类纵向干预研究、统一计算 16 种时钟和 94 种额外 DNAm 标志物的 TranslAGE 分析发现，不同干预与时钟的响应差异显著，并建立了可跨研究比较的响应性框架 [39]；其限制是文献碎片化、时钟面板不一致，部分研究未计算全部时钟 [39]。此外，SARDINE 框架证明仅用 EWAS 汇总统计、时钟权重和参考甲基化协方差即可在 **15,677 人**中准确复现个体水平的时钟—表型关联，并揭示标志物与衰老、疾病、生活方式关联的异质性，为无法获取个体数据的场景提供了替代方案 [40]。

蛋白质组时钟以血浆蛋白为底物，规模优势明显。UK Biobank 中基于 **2,897 个血浆蛋白**、**45,441 人**训练的模型经 Boruta 筛选出 **204 个蛋白**，与实际年龄的 Pearson r=0.94，蛋白质组年龄差与 27 个衰老表型、全因死亡和 26 种年龄相关疾病关联，并在 CKB（3,977 人）和 FinnGen（1,990 人）中独立验证 [5]；作者指出观察性关联不能证明因果，且外部队列样本较小 [5]。同样基于 UKB 的 PAC 使用 Olink 2,923 蛋白、**53,021 名 39–70 岁**参与者，以 LASSO 训练预测全因死亡，随访超 10 年，发现 PAC 年龄偏差与死亡和多种年龄相关疾病风险显著相关 [41]；其训练仅限 UKB、蛋白平台单一、外部验证有限 [41]。

蛋白组时钟正从整体走向器官分辨。基于 UKB **43,616 人**与 Olink 2,916 蛋白构建的整体加十个器官特异时钟，在中国（3,977 人）和美国（800 人）队列中验证，跨队列 r 分别为 **0.98 和 0.93**；加速的器官衰老在临床和遗传风险因素之外预测疾病发生、进展和死亡，其中脑衰老与死亡关联最强，精简蛋白面板仍保持性能 [6]。肌肉骨骼方向则先整合转录组富集、蛋白功能注释和文献构建 39 个蛋白池，在 **21,070 名** UKB 参与者中开发 MSKAge 与 MSKAgeMort，MSKAge 相关 r 女性 0.62、男性 0.56，MSKAgeMort 相关 r 女性 0.93、男性 0.88，其加速指标可预测死亡、肌肉骨骼病和年龄相关病 [42]。ECM 方向刻画出血浆 ECM 蛋白随龄的 **U 型轨迹**，最低点约 40–50 岁，基于 **14 个血浆蛋白**的时钟可预测年龄并区分健康与疾病 [43]；但所用 Robbins 队列最老仅 66 岁，U 型轨迹较弱、蛋白轨迹异质性大 [43]。

以结局而非年龄为目标的蛋白评分进一步拓展了用途。健康寿命蛋白评分 HPS 基于 UKB 53,018 人、2,920 种蛋白构建，随访 13.5 年，在 43,119 名基线健康者中 **12,427 人（28.8%）**发生健康寿命终点事件，较低 HPS 与更高死亡风险和慢性阻塞性肺病等年龄相关疾病相关 [44]；其局限是 UKB 以欧洲裔为主、健康寿命定义尚无共识、外部验证有限 [44]。疾病特异的蛋白时钟则针对 31 种年龄相关疾病提取最大化年龄介导疾病风险成分的蛋白复合评分，在 **44,526 名** UKB 参与者中，疾病年龄差可将同龄人 10 年发病率区分达 **20 倍**，每增加 1 年差距使 2 型糖尿病风险升高 **24%**、慢性肾病 **21%**，阿尔茨海默病风险亦升高 [45]。纵向数据方面，KORA 队列基于最多三个时间点的 LC-MS 血浆蛋白组（9,105 样本、4,100 人、25–88 岁）构建时钟并计算年龄加速，发现其与生活方式和临床风险因素相关，心血管代谢暴露共享蛋白组特征而吸烟和体力活动具独特特征，个体内血脂异常和肾功能受损与年龄加速增加相关 [46]。

转录组时钟面临平台依赖和组织特异性的双重约束。Pasta 采用「年龄偏移」学习框架，声称可跨组织、跨数据类型（bulk 与单细胞 RNA-Seq、微阵列）和跨物种预测相对年龄，优于 MultiTIMER 和 tAge，能区分衰老、静息和干细胞状态，可分层肿瘤分级和生存，p53 相关基因贡献显著 [47]；但转录组噪声和批次效应、跨平台泛化仍受限 [47]。DeepQA 针对「仅在健康受试者上训练、却在健康与非健康受试者上推断」这一固有偏倚，用混合专家加 Hinge-MAE 损失，在 MCATS 数据库 3,060 样本、31 数据集上训练，报告在健康和非健康受试者上均显著优于现有方法 [48]；其非健康样本的生物年龄缺乏金标准 [48]。

大规模数据使转录组时钟的精度指标可比。基于 ARCHS4 **56,877 例**人类 RNA-seq（2–114 岁、多组织）的混合专家模型达到 **MAE=7.58 年**，肺和脑预测最佳、肝较差，FOSB 重要性 1.00、C4B_2 为 0.95、PAX8-AS1 为 0.85、MT-RNR2 为 0.64、GFAP 为 0.53，残差随年龄增大，百岁老人误差达 **±40 年** [7]。K-Dense 多智能体系统在 ARCHS4 57,584 样本、28 组织、1,039 队列、1–114 岁上训练的集成时钟达到 **R²=0.854、MAE=4.26 年**，并提供校准置信区间以标记过渡期和极端年龄的预测，识别出 CDKN2A/p16、AMPD3、MIR29B2CHG、SEPTIN3 等阶段标志物，85 个重叠窗口显示基因重要性呈波状变化 [8]。两项工作使用同一数据资源但样本数与精度不同，不宜直接比较高低，只能视为同一平台上的不同建模尝试。物种与组织拓展方面，小鼠肝脏 RNA-seq 训练的 **LivAge** 在早衰综合征中显示转录组年龄增加，并可评估 Snell Dwarf、Ames Dwarf、GHR 缺陷及热量限制等干预 [49]；犬的 **1,640 份**甲基化组时钟可预测死亡率、生命早期表观遗传衰老最快，大体型和雄性犬寿命更短且分子衰老加速，体型相关变化集中于转座子元件、性别相关变化集中于 X 染色体 [50]。

单组学时钟之间的直接对照仍稀缺，但已有工作提示整合的边际收益。StackAge 在 UKB **30,376 人**上整合 2,923 蛋白与 251 代谢物，与实际年龄 Pearson r≈0.93，对 12 种慢性病风险预测增强，2 型糖尿病、阿尔茨海默病和慢性肾病 **AUC 超过 0.90**，中位随访 11.7 年 [51]；该工作仅整合血浆蛋白与代谢组、未纳入表观遗传层，且以横断面基线为主 [51]。代谢组单组学方面，MetaboAgeMort 基于 UKB **239,291 人**血浆代谢组，先选 **185 个**全因死亡相关代谢标志物再用 LASSO Cox 与 Gompertz 回归建模，训练 167,506、测试 71,785，可提升 10 年死亡预测并关联疾病、可调因素和遗传位点 [52]；其以全因死亡为替代指标、样本主要为欧洲白人，外推性受限 [52]。这些结果说明不同组学时钟在预测目标（年龄、死亡、疾病、健康寿命）上各有侧重，跨组学、跨队列的数字不可直接比高低，判断优劣须回到同一研究内部的对照设计。

### 2.2 多模态整合与跨队列泛化

多模态整合的起点是同一平台内多器官时钟的构建与比较。UK Biobank 血浆蛋白质组学（2,916 个蛋白、44,498 人）被用于训练 11 个器官的 LASSO 年龄模型，器官年龄差对生活方式、用药和随访 17 年内的多种疾病发生具有关联，脑、动脉和整体年龄对传统年龄的预测 r²=0.97 [53]。同一队列的另一项工作用 2,448 个血浆蛋白、43,498 人构建 11 个 ProtBAG，并与 9 个多器官表型年龄差时钟整合，报告跨器官特征可提升系统性疾病类别和全因死亡预测，同时强调年龄偏倚校正与器官蛋白特异性是方法学前提 [24]。代谢组层面，274,247 人的 107 种非衍生代谢物经 Lasso 与神经网络生成 5 个 MetBAG，独立测试集 Pearson r 为 0.25<r<0.42，平均绝对误差约 6 年，并关联 525 个疾病终点 [54]。影像层面，313,645 人的 7 个 MRIBAG 在留出测试中 Pearson r 0.23–0.77、MAE 约 5 年，并关联 2,923 个血浆蛋白与 327 个代谢物 [25]；腹部 CT 的 CTBA 模型则以 IPA 29.2 对 21.7 优于人口学模型（p<0.001），但队列 92% 为白人、外部验证有限 [55]。这些数字来自不同组学、不同队列与不同结局，不能横向比较优劣，只能在同一研究内部对照模型或标志物。

跨模态整合的另一条路径是把组学嵌入电子病历与临床表型。Mass General Brigham 约 31,264 人开发 EMRAge，并在多组学子集中生成 DNAmEMRAge 与 OMICmAge，随后在 All of Us 10,769、TruDiagnostic 14,213、Generation Scotland 18,672 等独立队列验证，报告与慢病和死亡强相关 [56]。中国 mCAS 队列以 2,019 名 18–91 岁个体整合临床、生理与分子数据，建立核心能力时钟、多模态时钟与器官相关时钟三层框架，并报告血浆蛋白时钟可代理系统生理能力、凝血因子年龄依赖积累驱动多器官衰老和炎症 [57]。以色列 10K 项目则在 1 万名 40–70 岁健康人中用临床、生理、行为、环境与多组学参数训练年龄模型，揭示男女衰老模式差异 [58]。GOLD BioAge 走的是轻量化路线，以 Gompertz 风险函数把实际年龄与常规生物标志物映射到死亡风险，并在 CHARLS、CLHLS、RuLAS 三个中国队列验证轻量版本 [59]。上述工作的人群构成、模态覆盖与验证队列各不相同，跨队列可比性仍是未解问题。

跨队列泛化的困难在表观遗传时钟上被直接量化。针对 Horvath 与 PedBE 等常用时钟，研究在 523 份儿童青少年血样中发现目标队列预测准确性下降，并以基于 Kriging 和 DNN 特征适配的迁移学习缩小目标数据差距 [9]。这一结果与蛋白、代谢、影像时钟普遍报告的“留出测试”性能形成张力：后者多为同一生物库内的随机划分，而 MRIBAG 的作者也指出腹部 MRI 特征共线性导致泛化较差、脑模型在外部队列存在域偏移 [25]。换言之，**同一研究内部的留出集表现不能等同于跨人群泛化**，迁移学习与外部验证是目前少有的直接应对手段。

方法学层面还有两类被明确提出的风险。其一是系统预测偏差：常用 ML/AI 连续结局回归模型会产生系统性偏差并传播到下游关联，甚至制造“预测脑龄越大认知越好”“表观年龄越大肾功能越好”这类方向相反的虚假关联，约束优化回归框架可改善校准与下游推断 [10]。其二是“点估计”的信息损失：概率框架从预测年龄分布的均值与宽度分别导出 BAG 与生物年龄不确定性 BAU，在超过 45 万名 UK Biobank 参与者中 BAU 与 BAG 仅弱相关，并随个体分子间年龄信号不一致而增加 [11]。这两项工作提示，多模态时钟的整合不只是拼接模态，还涉及偏差校正与不确定性刻画。

应用侧的证据显示多模态时钟已进入干预评估与假设生成。在 rentosertib 治疗特发性肺纤维化的 12 周 2a 期试验中，ProtAge、OrganAgemortality、OrganAgechrono、PAC、ipfP3GPT、PAOPAC 六种蛋白质组时钟一致预测治疗组生物年龄更低，但作者承认时钟无法单独区分衰老与疾病特异效应，需借助通路分析间接区分抗衰老与抗纤维化活性 [60]。ClockBase Agent 则以 40 余种衰老时钟再分析人鼠甲基化与 RNA-seq 数百万样本、43,602 个干预-对照比较，报告超 500 种干预显著降低生物年龄，并指出更多干预加速而非延缓衰老、疾病状态多加速生物年龄 [61]。AURORA 生成式多模态框架通过降低年龄差的干预筛选预测 Neisseria flavescens 为顶级候选，并以线虫实验验证活菌延长寿命和健康寿命 [62]。这些结果依赖已有时钟的预测，实验验证有限，其结论强度受时钟本身泛化性的约束。

总体而言，证据呈现出一条从单组学多器官时钟走向多模态、多队列整合的路径，但整合的收益与代价并存：跨器官特征被报告可提升系统性疾病与死亡预测 [24]，而系统预测偏差、模态间信号不一致与域偏移则可能同时被放大 [10][11][25]。纵向多组学被提出用于刻画个体化衰老轨迹，但现有摘要未提供可提取的方法与定量结果，尚不足以支撑具体结论 [21]。

### 2.3 单细胞与空间衰老图谱

单细胞衰老时钟把“生物年龄”从组织或个体层面推进到细胞类型层面。**sc-ImmuAging** 基于 **1081** 名 **18 至 97 岁**健康欧洲人 PBMC 的约 **130 万**细胞，用 LASSO、随机森林和 PointNet 为髓系与淋系五类免疫细胞分别建模，内部与外部验证均优于对照，并能揭示 COVID-19 感染后单核细胞与 BCG 接种后 CD8+T 细胞的年龄改变异质性 [12]。与之不同，**scAgeClock** 用门控多头注意力神经网络在 CZ CELLxGENE 大规模单细胞转录组上训练，摘要称覆盖 **400 余种细胞类型**、**40 余种人体组织**，精度高于偏最小二乘、弹性网等基线 [13]；另有工作把单细胞转录组转成“细胞句子”微调预训练大语言模型，在数百万细胞上训练并提名可降低预测转录年龄的候选靶点 [63]。三者都报告了优于基线的精度，但训练数据、细胞类型划分与验证方式不同，跨研究的精度数字不可直接比较；共同局限是外部验证有限、组织覆盖偏血液 [12][13]。

细胞衰老识别是图谱类工作的另一条主线，争议集中在“通用标志物是否存在”。**SenePy** 用 **72** 个小鼠和 **64** 个人类加权单细胞转录组 signature 构建评分平台，发现仅 **58/1540** 个细胞类型组合的标志物重叠显著，即衰老标志物高度组织与细胞类型特异，通用 signature 会被异质性掩盖 [14]。**hUSI** 走相反路线，从 **73** 项公开 RNA-seq 研究学习通用衰老特征，基准测试称在 bulk 和单细胞多种条件下优于 **31** 种方法 [15]。两者结论方向相反：一个强调特异性、一个强调通用性，其分歧部分源于评测任务与负样本质量不同 [14][15]。综述则指出缺乏特异标志物、衰老细胞稀少且表型异质动态，是计算多组学识别衰老细胞的核心障碍 [64]。

空间维度上，小鼠多组织图谱给出了机制性线索。对雄性小鼠 **9** 种组织的空间转录组分析发现，衰老敏感斑点与组织结构熵升高共定位，免疫球蛋白表达细胞聚集于其微环境，**IgG** 在雌雄小鼠及人组织中随衰老积累，靶向降低 IgG 可缓解小鼠多组织衰老 [27]。人皮肤的单细胞与空间转录组则显示，光老化相关衰老细胞负担高于时序衰老，衰老黑素细胞黑色素合成升高、衰老网状真皮成纤维细胞胶原与弹性纤维合成下降 [65]。人骨骼肌单核 RNA+ATAC 多组学构建了首个衰老人肌衰老细胞图谱，解析 SASP 异质性并提出 Maraviroc 作为候选 senotherapeutic [66]；但该研究自述人肌肉衰老细胞与 SASP 信息稀疏、既往证据存在冲突 [66]。

多器官、跨物种资源的规模差异明显。小鼠单核转录组图谱覆盖 **13** 个器官、**5** 个年龄段、雌雄两性，共 **93** 只小鼠、**20,317,820** 个细胞核，默认核心集为 **32** 只野生型小鼠、**11** 个器官，摘要未报告具体分析结论 [https://huggingface.co/datasets/transhumanist-already-exists/pansci-mouse-aging-snrna]。乳腺图谱用 scRNA-seq 与 snATAC-seq 比较 **3** 月龄与 **18** 月龄小鼠，发现上皮 AV/HS 减少、肌上皮增加，免疫髓系/浆细胞/记忆 T 增加、naive T 减少，成纤维细胞增加，并呈现衰老与癌症共享的表观与转录特征 [28]。人内皮图谱 HAECA 整合 **12** 种组织、超 **37.5 万**个内皮细胞，报告静脉内皮血管生成基因下降及细胞外基质与机械转导基因广泛改变 [67]。这些资源多为描述性图谱，规模数字来自不同物种与设计，不宜横向比较。

脑与生殖轴的图谱把空间信息与衰老时钟结合。恒河猴图谱覆盖 **11** 个脑区、**55** 只 **0.5–21 岁**个体、**530 万**细胞，识别衰老耗竭的脆弱神经元群体及仅在单细胞分辨率可见的胶质细胞组成变化，并发现其与阿尔茨海默病特征重叠 [68]。纹状体 Slide-tags 单核空间转录组分析 **19** 例死后供体、**110 万**细胞，揭示纹状体一致分为 **六个**区、每区由分子不同的棘状投射神经元群体界定，并构建小鼠同源图谱推断衰老变化 [69]。食蟹猴下丘脑-垂体-睾丸轴时空图谱覆盖幼年、青春期、成年与老年，发现 KNDy 神经元在静息样与兴奋样状态间转换并发生空间重排 [70]。在神经元类型层面，用 BitAge 与 Stochastic Clock 预测线虫 **128** 种神经元类型，预测年龄约 **98h 至 177h**、近 **2 倍**差异，两时钟相关 Pearson **0.65**（**P=5.5×10−17**），并验证丁香酸和 vanoxerine 可防止神经退化 [71]；该结果基于线虫，人类相关性仍需验证。

上述工作的方法学差异决定了结论边界。时钟类研究以预测精度为评价核心，但训练队列以欧洲健康成人或公共数据库为主，疾病与疫苗样本有限 [12][13]；图谱类研究以细胞组成与分子特征描述为主，多数缺乏跨物种因果验证，小鼠乳腺与小鼠多组织图谱的人类适用性依赖特征映射 [28][27]。综述性证据进一步提示，单细胞技术仍受样本、批次与因果推断限制，脑衰老领域的年轻化干预评估也需无偏的单细胞组学设计 [72]。因此，单细胞与空间衰老图谱当前提供的是高分辨率的关联性框架，而非可直接跨队列比较的年龄标尺。

### 2.4 衰老生物学基准与基础模型

衰老生物学正从单一模态的“时钟”走向标准化基准与基础模型并存的格局。LongevityBench 以 **17 项任务、5 个生物数据域**评估 **18 个前沿 AI 系统**（来自 6 个开发团队），结论是没有单一模型主导所有任务，组学年龄预测被列为最难任务；作者同时微调 5 个 0.6B–9B 参数的多任务 Longevity-LLM，称其可匹配或超过更大的通用系统 [16]。表观遗传方向已有更早的标准化尝试：ComputAgeBench 以“可靠时钟应能区分健康个体与衰老加速疾病个体”为核心假设，整合 **66 个公开血液 DNA 甲基化数据集、覆盖 19 种疾病**，测试 **13 个已发表表观时钟**，并另建 46 个数据集用于训练新时钟 [18]。单细胞层面则建立了覆盖 **5 个生物学问题、超过 250 万单细胞转录组**的细胞表征基准，评估 10 个通用单细胞基础模型、3 个衰老专用模型及传统方法，发现冻结预训练表征下 Geneformer 在时序年龄预测和年龄伪时间一致性上最佳，但 **2000 个高变基因**的平均表现更高 [29]。

基础模型路线在 2026 年出现明显推进。Longevity-LLM v0.1 将 Qwen3-14B 在 DNA 甲基化、蛋白质组、临床生物标志物和 RNA 表达数据上经监督与强化学习微调，报告表观年龄预测 **MAE 为 4.34 年**、超过 Horvath 多组织时钟，并在蛋白质组谱生成上优于所比较的前沿 LLM [17]。这与 LongevityBench 中“小型专用模型可匹配更大通用系统”的结论方向一致，但两者任务集与评测口径不同，不能直接比较高低。组织学方向，GenVinci 基于 ImageOmicsNet-300M 语料库（**3 亿单细胞与空间转录组谱、2490 万 H&E 预测虚拟空间转录组谱、4623 张 H&E 切片**，其中 1782 张来自衰老小鼠器官、人皮肤连续切片跨 50 年），从常规 2D 组织学重建 3D 组织场景并零样本预测空间基因表达以映射衰老 [73]。

综述性证据对上述进展给出较一致的定位，但深度不一。有综述梳理 2016–2024 年间 **125 篇同行评审研究**，指出 CNN、RNN、GAN、LLM 和扩散模型已用于衰老时钟、合成数据生成、药物发现和多模态健康评估，同时自认属叙述性综述、缺乏定量荟萃 [74]。另有综述认为表观时钟在预测生物年龄和健康表型上最准确，并将生物年龄预测器与“人类数字孪生”相连，但指出落地受数据整合、隐私、互操作性和纵向建模限制 [75]；关于临床衰老时钟的综述强调 AI 集成学习与深度学习推动多组学时钟在准确性、可解释性和泛化性上的进展，然全文不可得、无法提取定量性能 [76]。方法学综述则把数据异质性、泛化性有限、可解释性不足和临床转化障碍列为主要挑战 [77]。

争议与空白集中在评测与验证环节。一方面，基准工作显示专用小模型可胜过通用大模型 [16][17]，另一方面，现有基准各自局限于单一模态——ComputAgeBench 仅基于血液 DNA 甲基化、未覆盖其他模态 [18]，单细胞基准限于转录组表征 [29]，跨模态可比性仍缺统一口径。针对干预评估，有观点文章主张 AI 评估应正确、有用、全面、可解释并考虑因果、跨学科、标准、纵向数据和已知衰老生物学，建议 LLM 结合知识图谱与检索增强生成并开展基准测试，但未提供实验验证或定量结果 [30]。这些要求与当前基准多聚焦年龄预测精度、少涉及因果与干预验证的现状形成张力。

### 2.5 类器官、扰动与 Cell Painting 衰老建模

在细胞衰老建模的扰动侧，转录组年龄预测器与过表达筛选提供了可解释的因果线索：研究在人成纤维细胞中构建可解释转录组年龄预测器，并据此开展cDNA过表达筛选，鉴定出RNA加工与剪接因子**SRSF1**，其诱导产生强烈的年轻化转录特征且不丧失细胞身份，体外实验显示可恢复年轻表型[31]。该工作以预测器输出的年龄作为筛选读出，属于单一细胞类型的体外模型，样本规模与体内验证未提及[31]。

成像侧的方法学基础来自Cell Painting：该显微细胞标记assay于**2013年**提出，旨在捕获细胞状态并优化、标准化图像型profiling，十年来协议、特征提取、质控与批次校正持续改进，并用于机制、毒性及多组学整合等应用[32]。作为综述，其未提供统一定量基准，结论依赖公开数据集与计算实验技术进展[32]；与上述转录组筛选相比，两者分处成像表型与转录组读出，尚无可直接对照的同一研究内证据。

### 2.6 跨物种与跨组织衰老标志（脂质组等）

跨物种、多组织脂质组学比较显示，**脂酰链延长**是小鼠、线虫、果蝇和人类衰老的保守标志；衰老并非单一脂质分子的增减，而是表现为向长链脂质转变并伴随短链脂质耗竭的**比值性重塑**，人类心脏病进展中也出现类似的脂质延长 [33]。该研究同时鉴定了脂质重塑因子 **Plb1** 参与调控这一过程 [33]。

在干预层面，同一研究内的对照显示**饮食限制可缩短小鼠心脏脂质**，为脂质链长变化与衰老进程之间的关联提供了可调控的证据 [33]。上述结果支持将脂质组重塑作为跨物种、跨组织的衰老标志候选，但其在人类不同组织与疾病背景下的普遍性仍待进一步验证 [33]。

## 3 数据与资源

在衰老标志物的跨人群验证方面，**Biolearn** 提供了开源统一框架，用于衰老标志物的整理、协调与系统评估，旨在应对跨人群验证缺乏标准化方法、标志物设计分散及数据集结构不一致等问题[26]。该框架依托多公开数据集与多种衰老生物标志物，统一标准化格式并评估其性能、稳健性和泛化性，形成可复现框架；其局限在于依赖已有公开数据，临床验证仍待推进[26]。面向免疫衰老这一子问题，**Immunosenescence Inventory** 作为多组学数据库，整合单细胞转录组、bulk转录组、表观组、TCR/BCR等多物种数据，提供知识 curation、多模态数据集以及免疫细胞识别与免疫时钟计算工具，并以 ImmPort、InnateDB、Aging Atlas 等既有数据库为参照[78]。不过该数据库整合依赖已有数据，未提供统一预测性能基准，单细胞免疫衰老覆盖仍有限[78]。

在跨物种资源层面，**LACA** 整合 **134 个物种**的单细胞转录组数据及其最大寿命信息，包含超 **1.48 亿细胞**和 **190 个注释细胞类型**，并提供长寿基因比较、基因-寿命相关性和细胞-寿命相关性等跨物种分析工具，用于解读进化与寿命相关机制[79]。与前述工作相比，Biolearn 侧重标志物的统一评估框架，Immunosenescence Inventory 侧重免疫衰老的多组学整合与免疫时钟计算，LACA 则侧重跨物种单细胞图谱与寿命关联分析；三者数据来源与评估目标不同，其中 Immunosenescence Inventory 明确未提供统一预测性能基准[78]，因此不同资源间的性能不宜直接比较。

## 4 应用与结果

在应用层面，DNA甲基化年龄差（Δage）与死亡风险的关联是最早被系统检验的结局之一。四个老年人纵向队列的荟萃分析显示，**Δage每高5年全因死亡风险增加21%**，校正健康、生活方式与APOE后仍增加16%，且Δage遗传度为0.43 [80]。随后扩展到13个队列、13,089人（2,734例死亡）的荟萃分析比较了Horvath 353 CpG与Hannum 71 CpG时钟，表观年龄与实足年龄相关系数为0.65–0.89，年龄加速与全因死亡风险增加相关，且引入血液细胞组成信息可提升预测 [81]。同一353 CpG时钟在多组织数据中显示表观年龄加速存在种族与性别差异，并与冠心病及相关风险因素相关 [82]。需要注意的是，上述死亡预测均来自观察性队列，且血液细胞组成对估计的影响、种族/民族亚组有限等问题被作者列为局限 [81]。

在疾病与暴露场景中，时钟被用于刻画"加速衰老"表型。基于11个Illumina甲基化数据集（血液与脑组织）的比较显示，HIV感染者相对未感染对照表现出显著增加的表观年龄加速 [83]；但该证据为横断面设计、样本量有限，抗逆转录病毒治疗等因素未被完全解析 [83]。在老年功能结局上，Lothian Birth Cohort 1936（70岁n=920、73岁n=299、76岁n=273）发现表观年龄加速与70岁步行速度、握力、肺功能和认知能力横断面相关，**但不预测70至76岁间的功能下降** [84]——这与死亡预测证据形成对照，提示时钟对"当前状态"与"后续变化"的预测力可能不同。系统综述层面，299篇文献、1050个EAA-因素关联、53种时钟的汇总显示若干EAA与生理、认知、社会和环境因素存在显著关联，并建立了四级分类与TEAPEE数据库 [85]；作者同时指出研究异质性大、部分关联证据有限、因果方向不明确 [85]。

干预与可塑性方面，证据开始从关联走向扰动。40个月二甲双胍干预雄性食蟹猴的研究利用多组织转录组、DNA甲基化、血浆蛋白与代谢组构建猴衰老时钟，**二甲双胍显著延缓衰老指标，脑衰老约回退6年**，并保护脑结构、增强认知，部分由Nrf2激活介导 [19]；该结果限于雄性食蟹猴，人类转化尚待验证 [19]。异时心脏移植的多组学分析则显示，移植心脏的DNA甲基化和基因表达生物年龄快速同化受体年龄，而非保留供体年龄，且**该效应仅限移植物，不影响受体全身生物年龄** [20]，提示系统环境可驱动局部组织生物年龄。另有研究提出干细胞衰老时钟连接生物学年龄偏差与急性髓系白血病临床结局 [86]，但所提供文本未给出具体定量结果与验证细节，暂难与其他工作作实质比较。

## 5 评测、可复现性与争议

（本节暂无入库证据）

## 6 空白与趋势

单细胞与空间图谱的快速扩张，使「衰老时钟」与「衰老图谱」两类工作开始出现方法学上的分工，但两者的评价标准尚未打通。时钟类工作以预测精度和跨队列验证为核心，图谱类工作以细胞组成与分子特征的描述性发现为核心；前者受限于训练队列以欧洲健康成人或公共数据库为主 [12][13]，后者多数缺乏跨物种因果验证，人类适用性依赖特征映射 [28][27]。**目前尚无一个在同一研究内同时给出「图谱发现—时钟标定—外部队列验证」闭环的工作**，这使空间图谱中的衰老细胞负担、组织熵等指标难以转化为可跨队列比较的年龄标尺。

从上述证据看，本方向的趋势与空白可归纳为以下几点：

1. **从「预测年龄」转向「预测结局与可干预性」，但训练目标与评价口径仍不统一。** 第二代、第三代时钟在疾病与死亡预测上系统性优于第一代 [3]，蛋白组、代谢组、影像时钟也普遍以死亡或疾病为终点 [5][52][25]。**空白在于：不同研究分别以年龄、死亡、疾病、健康寿命为目标，缺少在同一队列、同一终点下横向比较各模态时钟的研究设计**；现有跨组学数字来自不同人群与结局，不能互比。

2. **多模态整合被报告有边际收益，但「整合什么、如何对齐」缺少方法学共识。** 跨器官蛋白特征被报告可提升系统性疾病与死亡预测 [24]，蛋白+代谢的 StackAge 报告 r≈0.93 与多种疾病 AUC 超过 0.90 [51]，但后者未纳入表观遗传层且以横断面基线为主 [51]。**缺失模态、模态间信号不一致与域偏移的处理仍属空白**：概率框架显示 BAU 与 BAG 仅弱相关、随分子间年龄信号不一致而增加 [11]，而现有整合工作多默认模态齐全、质量一致。

3. **系统预测偏差与不确定性刻画刚开始被正视，尚未进入常规流程。** 连续结局回归的系统偏差可制造方向相反的虚假下游关联，约束优化框架可改善校准 [10]；概率框架把点估计拆成均值与宽度 [11]。**空白在于：尚无工作把偏差校正与不确定性输出同时嵌入多模态时钟的构建—验证—下游关联全链条**，多数时钟仍只报告单一 MAE 或 AUC。

4. **跨队列泛化被直接量化，但迁移学习与外部验证仍是少数派。** 表观时钟在目标队列准确性下降，需 Kriging 与 DNN 特征适配的迁移学习缩小差距 [9]；MRIBAG 作者自述腹部 MRI 特征共线性导致泛化较差、脑模型存在域偏移 [25]。**同一生物库内的随机留出集表现不能等同于跨人群泛化**，而蛋白、代谢、影像时钟多以后者代替前者。

5. **AI 基准与基础模型已起步，但基准各自局限于单一模态，跨模态可比性缺统一口径。** LongevityBench 覆盖 17 项任务、5 个数据域，结论是没有单一模型全能、组学年龄预测最难 [16]；ComputAgeBench 仅基于血液 DNA 甲基化 [18]，单细胞基准限于转录组表征 [29]。**空白在于：缺少覆盖表观、蛋白、代谢、影像、单细胞与空间模态的统一评测集**，也缺少把因果与干预验证纳入基准的任务设计——现有观点文章提出的正确、有用、可解释、考虑因果与纵向数据等要求 [30] 尚未落地为可执行基准。

6. **扰动与类器官体系中的衰老建模刚出现可解释的因果线索，但读出维度单一。** 人成纤维细胞中可解释转录组年龄预测器驱动的过表达筛选鉴定出 SRSF1，诱导年轻化转录特征且不丧失细胞身份 [31]；Cell Painting 提供了成像表型 profiling 的方法学基础 [32]。**两者分处转录组与成像读出，尚无可直接对照的同一研究内证据**，类器官中的衰老时钟标定与扰动响应建模基本空白。

7. **资源与图谱的规模快速膨胀，但评估框架与性能基准不匹配。** Biolearn 提供标志物统一整理与评估框架 [26]，Immunosenescence Inventory 整合免疫衰老多组学并含免疫时钟计算工具但未提供统一预测性能基准 [78]，LACA 覆盖 134 个物种、超 1.48 亿细胞 [79]。**空白在于：资源侧缺少与时钟性能评测对接的标准化接口**，图谱规模数字与时钟精度指标分属两套话语，无法互相校验。

综合看，**本方向最迫切的空白不是再增加一个模态或一个时钟，而是建立跨模态、跨队列、含不确定性与因果/干预验证的统一评测与验证基础设施**；现有证据已分别证明各环节可行，但尚未在同一研究内被串联。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 单组学衰老时钟（表观/蛋白/转录） | 成熟 | 表观时钟的方法骨架早在 2013 年就已定型（[1]，Horvath 泛组织甲基化年龄，6423 引），随后是第二代表观时钟（[2]，PhenoAge，3196 引）与大规模结局验证（[80]，甲基化年龄预测全因死亡；[81]，meta 分析预测死亡时间）。近两年增量主要来自换模态：蛋白组时钟（[5]）与因果增强表观年龄（[34]），属于「方法收敛、增量为主」，单组学再做新时钟本身难有方法新意。 |
| 2.2 多模态整合与跨队列泛化 | 朝阳 | 雷达样本中该节 **n=16，近两年占比 0.92，CNS 占比 0.56**，几乎全是 2024–2026 的新工作，且方法尚未收敛：血浆蛋白组连接脑—免疫衰老与健康寿命（[53]）、基于 MRI 的多器官时钟（[25]）、表型组范围性别特异动态（[58]）各自用不同模态、不同队列、不同验证口径，说明「怎么对齐模态、怎么跨队列校正」还没有共识答案，是典型的爆发期。 |
| 2.3 单细胞与空间衰老图谱 | 朝阳 | 近两年集中出现图谱级工作：空间转录组揭示免疫球蛋白相关衰老（[27]）、细胞类型特异的衰老景观（[14]）、单细胞免疫衰老时钟揭示个体异质性（[12]）、健康乳腺单细胞衰老图谱（[28]）。数据在快速积累，但「单细胞层面如何定义并校准生物年龄」仍各做各的，方法未收敛。 |
| 2.4 衰老生物学基准与基础模型 | 萌芽 | 雷达样本中该节 **n=10，中位引用 0**，且以观点/综述为主（[74]，生成式 AI 在衰老研究的综述；[30]，AI 干预评估的验证要求）。真正带评测实体的只有 ComputAgeBench（[18]）与数字孪生视角（[75]），基准与基础模型都还是零星探索，尚无领域公认的 LongevityBench 级基础设施。 |
| 2.5 类器官、扰动与 Cell Painting 衰老建模 | 证据不足 | 雷达样本中该节仅 **n=2**：一篇是 Cell Painting 十年综述（[32]），一篇是转录组重编程筛选鉴定 SRSF1 为衰老调控因子（[31]）。两者都不是「类器官体系里的衰老时钟建模」，无法据此判断阶段；但结合 2.2/2.3 的爆发，这更像证据挂载缺口而非领域空白。 |
| 2.6 跨物种与跨组织衰老标志（脂质组等） | 证据不足 | 雷达样本中该节仅 **n=1**（[33]，长链脂质标记衰老并约束寿命），单篇不足以判断阶段。 |
| 3 数据与资源 | 萌芽 | 雷达样本中该节 **n=3，全部为 2025 年**：衰老标志物系统化 curation 与评估的统一框架（[26]）、免疫衰老多组学数据库（[78]）、跨物种单细胞长寿资源 LACA（[79]）。资源刚起步、彼此未打通，属于早期但高杠杆的位置。 |
| 4 应用与结果 | 成熟 | 高引用集中在 2015–2016 的结局验证：甲基化年龄预测死亡（[80]）、meta 分析预测死亡时间（[81]）、种族/性别与冠心病关联（[82]）、HIV 加速衰老（[83]）。**该节近两年占比仅 0.22、中位引用 524**，说明「时钟→结局」的关联范式已定型，新工作多为应用复刻。 |
| 5 评测、可复现性与争议 | 证据不足 | 雷达样本中该节 **n=0**，无证据可判；但 2.4 中 ComputAgeBench（[18]）与验证要求讨论（[30]）提示评测需求真实存在，只是尚未形成独立证据簇。 |

**整体判断**：这个方向整体处于**「单组学时钟已成熟、多模态整合与单细胞/空间图谱正在朝阳期爆发、基准与基础模型尚在萌芽」的三层叠加状态**。雷达样本里 2.2 与 2.3 合计 **33 篇、近两年占比 0.92/0.75、CNS 占比 0.56/0.65**，而 2.1 与第 4 节的高引工作几乎都停在 2013–2018——**方法重心已从「造时钟」转向「整合、泛化与评测」**。窗口期判断：多模态整合的「方法未收敛」状态大概还有 **1–2 年**（一旦跨队列校正与缺失模态处理出现公认范式，就会迅速滑向成熟）；而**衰老 AI 基准/基础模型（2.4）与类器官扰动建模（2.5）的窗口更长，约 2–3 年**，因为目前连评测实体都只有 ComputAgeBench 一个（[18]）。**最大的不确定性**有三点：一是多模态时钟的**外部验证口径不统一**（[53] 与 [25] 各用各的结局），导致「谁更准」无法裁决；二是**单细胞衰老的定义本身有争议**（[12] 强调个体异质性，[14] 强调细胞类型特异），标签噪声会直接污染任何监督式时钟；三是**评测基础设施缺位**（第 5 节雷达样本 n=0），使方法比较高度依赖作者自选指标。

**接下来怎么做**

1. **把「缺失模态 + 跨队列校正」做成方法论文，而不是再做一个时钟。** 切入点：用公开多模态队列（蛋白组+表观+影像，参考 [53]、[25] 的模态组合）构造「随机丢模态」训练协议，产出可复用的缺失模态插补/对齐模块 + 跨队列校准层。为什么现在做：2.2 节 **近两年占比 0.92、方法明显未收敛**，谁先给出公认的缺失模态处理范式谁就定义标准；且这类工作不依赖湿实验，正好匹配他的公共数据 demo 能力。

2. **用单细胞/空间图谱做「衰老时钟的标签校准」，而不是再画一张图谱。** 切入点：以 [27]、[14]、[28] 的公开图谱为训练源，把「个体级年龄」分解为「细胞类型组成漂移 + 细胞内状态漂移」两部分，产出可解释的分解式时钟。为什么现在做：[12] 已证明个体异质性极大，纯个体级回归会被组成变化混淆；这个分解视角目前没人系统做，且直接复用现有数据。

3. **抢做衰老 AI 基准的一个子赛道：多模态时钟的可复现评测。** 切入点：以 ComputAgeBench（[18]）为起点，补上它缺的多模态与跨队列维度，接入 [26] 的 curation 框架与 [78]、[79] 的资源，产出 benchmark + 排行榜 + 基线代码。为什么现在做：2.4 节 **n=10、中位引用 0**，第 5 节雷达样本 **n=0**，基础设施几乎空白，而 [30] 已明确指出验证要求缺失——**这是投入产出比最高、且最容易被社区引用的位置**。

4. **把类器官 + 多组学做成「扰动体系中的衰老建模」，这是他的合作项目最该切的口。** 切入点：在类器官体系里做「年轻化/衰老扰动 → 多组学读出 → 反事实年龄预测」的模型，方法上借用 2.2 的模态对齐与 2.3 的单细胞分解；参照 [31] 的转录组重编程筛选设计与 [32] 的 Cell Painting 表型读出。为什么现在做：2.5 节雷达样本仅 **n=2 且无一篇是类器官衰老时钟建模**，属于「证据不足但需求明确」的真空；同时 2.4 的 AI 干预评估讨论（[30]）正缺这类带扰动的验证数据，**做出来既是方法也是基准数据**。

5. **避开纯表观时钟的红海，只在需要「对照/基线」时引用。** 切入点：新时钟工作一律以 [1]、[2] 为基线而非贡献点，把精力留给上面 1–4。为什么：2.1 与第 4 节已成熟（**第 4 节近两年占比仅 0.22、中位引用 524**），单组学新时钟的方法边际收益极低，而 [5] 这类蛋白组时钟的成功也主要来自「新模态 + 大队列结局」，不是新算法。

## 参考文献

1. DNA methylation age of human tissues and cell types. Genome Biology 2013. https://doi.org/10.1186/gb-2013-14-10-r115
2. An epigenetic biomarker of aging for lifespan and healthspan. bioRxiv 2018. https://doi.org/10.18632/aging.101414
3. An unbiased comparison of 14 epigenetic clocks in relation to 174 incident disease outcomes.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66106-y
4. Cross-tissue comparison of epigenetic aging clocks in humans.. Aging cell 2025. https://doi.org/10.1111/acel.14451
5. Proteomic aging clock predicts mortality and risk of common age-related diseases in diverse populations. Nature Medicine 2023. https://doi.org/10.1038/s41591-024-03164-7
6. Organ-specific proteomic aging clocks predict disease and longevity across diverse populations.. Nature aging 2025. https://doi.org/10.1038/s43587-025-01016-8
7. Transcriptomic age prediction using mixture-of-experts models reveals tissue-specific aging signatures in large-scale human RNA-sequencing data. medRxiv 2025. https://doi.org/10.1101/2025.06.28.25330474
8. Guided multi-agent AI invents highly accurate, uncertainty-aware transcriptomic aging clocks. bioRxiv 2025. https://doi.org/10.1101/2025.09.08.674588
9. BRIDGING THE GAP: ENHANCING THE GENERALIZABILITY OF EPIGENETIC CLOCKS THROUGH TRANSFER LEARNING.. The annals of applied statistics 2026. https://doi.org/10.1214/26-aoas2136
10. Trustworthy ML/AI for Aging Clocks: Preventing Systematic Prediction Bias in Biological Age Estimation. bioRxiv 2026. https://doi.org/10.64898/2026.05.27.728155
11. Uncertainty redefines biological age.  . https://doi.org/10.64898/2026.09.26.26364091
12. Single-cell immune aging clocks reveal inter-individual heterogeneity during infection and vaccination.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00819-z
13. scAgeClock: a single-cell transcriptome-based human aging clock model using gated multi-head attention neural networks.. npj aging 2026. https://doi.org/10.1038/s41514-026-00379-5
14. Unveiling the cell-type-specific landscape of cellular senescence through single-cell transcriptomics using SenePy.. Nature communications 2025. https://doi.org/10.1038/s41467-025-57047-7
15. A transcriptome-based human universal senescence index (hUSI) robustly predicts cellular senescence under various conditions.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00886-2
16. An open benchmark and language models for AI in aging biology.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.026
17. The End of Aging Clocks: Training Foundation Models to Reason in Aging and Longevity. bioRxiv 2026. https://doi.org/10.64898/2026.03.28.714980
18. ComputAgeBench: Epigenetic Aging Clocks Benchmark. bioRxiv 2025. https://doi.org/10.1145/3711896.3737382
19. Metformin decelerates aging clock in male monkeys.. Cell 2024. https://doi.org/10.1016/j.cell.2024.08.021
20. Transplanted hearts assimilate the recipient’s biological age. bioRxiv 2026. https://doi.org/10.64898/2026.09.15.751836
21. Longitudinal multiomics reveals personalized aging trajectories.. Nature aging . https://doi.org/10.1038/s43587-026-01248-2
22. LinAge2: providing actionable insights and benchmarking with epigenetic clocks.. npj aging 2025. https://doi.org/10.1038/s41514-025-00221-4
23. A blood-based epigenetic clock for intrinsic capacity predicts mortality and is associated with clinical, immunological and lifestyle factors.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00883-5
24. Refining the generation, interpretation and application of multi-organ, multi-omics biological aging clocks.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00928-9
25. MRI-based multi-organ clocks for healthy aging and disease assessment.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03999-8
26. A unified framework for systematic curation and evaluation of aging biomarkers.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00987-y
27. Spatial transcriptomic landscape unveils immunoglobin-associated senescence as a hallmark of aging.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.019
28. Comprehensive single-cell aging atlas of healthy mammary tissues reveals shared epigenomic and transcriptomic signatures of aging and cancer.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00751-8
29. Benchmarking single-cell foundation models for aging biology.  . https://doi.org/10.64898/2026.09.21.753191
30. Validation Requirements for AI-based Intervention-Evaluation in Aging and Longevity Research and Practice. Ageing Research Reviews 2024. https://doi.org/10.1016/j.arr.2024.102617
31. Transcriptomic reprogramming screen identifies SRSF1 as a regulator of aging.. Nature aging . https://doi.org/10.1038/s43587-026-01234-8
32. Cell Painting: a decade of discovery and innovation in cellular imaging.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02528-8
33. Longer lipids mark aging and constrain lifespan.. Nature aging . https://doi.org/10.1038/s43587-026-01223-x
34. Causality-Enriched Epigenetic Age Uncouples Damage and Adaptation. bioRxiv 2023. https://doi.org/10.1038/s43587-023-00557-0
35. Enhancing the performance and interpretability of epigenetic clocks.. Nucleic acids research 2026. https://doi.org/10.1093/nar/gkag661
36. Decoding disease-specific ageing mechanisms through pathway-level epigenetic clock: insights from multi-cohort validation.. EBioMedicine 2025. https://doi.org/10.1016/j.ebiom.2025.105829
37. Epigenetic clocks and programmatic aging.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102546
38. Characterising developmental dynamics of adult epigenetic clock sites.. EBioMedicine 2024. https://doi.org/10.1016/j.ebiom.2024.105425
39. Responsiveness of epigenetic aging biomarkers to longevity interventions in humans.. Nature medicine 2026. https://doi.org/10.1038/s41591-026-04562-9
40. SARDINE unlocks EWAS summary statistics for large-scale epigenetic biomarker analysis.  . https://doi.org/10.64898/2026.11.05.763758
41. Proteomic aging clock (PAC) predicts age‐related outcomes in middle‐aged and older adults. Aging Cell 2024. https://doi.org/10.1111/acel.14195
42. Construction and Validation of Plasma Protein-Based Musculoskeletal Biological Age and Genetic and Environmental Risk Profiles.. Aging cell 2026. https://doi.org/10.1111/acel.70636
43. An Extracellular Matrix Aging Clock Based on Circulating Matrisome Proteins Predicts Biological Aging and Disease.. Aging cell 2026. https://doi.org/10.1111/acel.70474
44. A proteomic signature of healthspan.. Proceedings of the National Academy of Sciences of the United States of America 2025. https://doi.org/10.1073/pnas.2414086122
45. Disease aging clocks in the plasma proteome stratify risk and track preclinical progression.  . https://doi.org/10.21203/rs.3.rs-10675323/v1
46. Intraindividual longitudinal changes of the proteome reveal dynamic markers of biological aging.  . https://doi.org/10.64898/2026.10.01.755909
47. Pasta, a Versatile Transcriptomic Clock, Maps the Chemical and Genetic Determinants of Aging and Rejuvenation. bioRxiv 2025. https://doi.org/10.1002/advs.76740
48. DeepQA: A Unified Transcriptome-Based Aging Clock Using Deep Neural Networks.. Aging cell 2025. https://doi.org/10.1111/acel.14471
49. LivAge: An Online Aging Clock for Murine Transcriptomic Age Estimation.. Aging cell 2026. https://doi.org/10.1111/acel.70677
50. Epigenetic aging and transposon dysregulation reflect size-related lifespan compression in dogs.. Science (New York, N.Y.) . https://doi.org/10.1126/science.aeb2986
51. StackAge: an ensemble-based clock for precise quantification of biological age using multi-omics data.. Briefings in bioinformatics 2026. https://doi.org/10.1093/bib/bbag271
52. A Novel Metabolomic Aging Clock Predicting Health Outcomes and Its Genetic and Modifiable Factors. Advancement of science 2024. https://doi.org/10.1002/advs.202406670
53. Plasma proteomics links brain and immune system aging with healthspan and longevity.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03798-1
54. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
55. Biological age model using explainable automated CT-based cardiometabolic biomarkers for phenotypic prediction of longevity.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56741-w
56. OMICmAge quantifies biological age by integrating multi-omics with electronic medical records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01073-7
57. Multimodal clocks of human aging.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.025
58. Phenome-wide associations of human aging uncover sex-specific dynamics.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00734-9
59. Gompertz Law-Based Biological Age (GOLD BioAge): A Simple and Practical Measurement of Biological Ageing to Capture Morbidity and Mortality Risks.. Advanced science (Weinheim, Baden-Wurttemberg, Germany) 2025. https://doi.org/10.1002/advs.202501765
60. Integration of proteomic aging clocks in a phase 2a clinical trial supports simultaneous geroprotective assessment.. Nature Biotechnology 2026. https://doi.org/10.1038/s41587-026-03286-y
61. Autonomous AI Agents Discover Aging Interventions from Millions of Molecular Profiles. bioRxiv 2025. https://doi.org/10.1101/2023.02.28.530532
62. Multi-modality profiling identifies Neisseria flavescens as a central geroprotective oral commensal in humans.. Nature aging . https://doi.org/10.1038/s43587-026-01220-0
63. Universal Single-Cell Transcriptomic Aging Clock powered by LLMs reveals targets to slow cellular aging. Innovation in aging 2025. https://doi.org/10.1093/geroni/igaf122.4305
64. Advancing biological understanding of cellular senescence with computational multiomics.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02314-y
65. Mapping epidermal and dermal cellular senescence in human skin aging.. Aging cell 2024. https://doi.org/10.1111/acel.14358
66. Multiomics and cellular senescence profiling of aging human skeletal muscle uncovers Maraviroc as a senotherapeutic approach for sarcopenia.. Nature communications 2025. https://doi.org/10.1038/s41467-025-61403-y
67. Uncovering the transcriptional hallmarks of endothelial cell aging via integrated single-cell analysis.. Nature aging . https://doi.org/10.1038/s43587-026-01247-3
68. Single-cell, multi-region profiling of the macaque brain across the lifespan.. Cell . https://doi.org/10.1016/j.cell.2026.09.014
69. Mesoscale molecular architecture of the striatum across cell types and adult aging.. Cell . https://doi.org/10.1016/j.cell.2026.10.029
70. A spatiotemporal atlas of maturation and aging of the male monkey hypothalamic-pituitary-testicular axis.. Cell stem cell . https://doi.org/10.1016/j.stem.2026.10.014
71. Aging clocks delineate neuron types vulnerable or resilient to neurodegeneration and identify neuroprotective interventions.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01067-5
72. Brain aging and rejuvenation at single-cell resolution.. Neuron 2025. https://doi.org/10.1016/j.neuron.2024.12.007
73. GenVinci reconstructs 3D molecular tissue scenes from histology to map senescence across aging and disease.  . https://doi.org/10.64898/2026.11.17.767412
74. Deep learning and generative artificial intelligence in aging research and healthy longevity medicine.. Aging 2025. https://doi.org/10.18632/aging.206190
75. From ageing clocks to human digital twins in personalising healthcare through biological age analysis.. NPJ digital medicine 2025. https://doi.org/10.1038/s41746-025-01911-9
76. The Evolving Landscape of Clinical Aging Clocks: From Epigenetic to Multi-Omics Integration.. Aging cell 2026. https://doi.org/10.1111/acel.70579
77. Artificial intelligence approaches in biological age prediction: current status and challenges.. British journal of biomedical science 2026. https://doi.org/10.3389/bjbs.2026.16141
78. Immunosenescence Inventory-a multi-omics database for immune aging research.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1102
79. LACA: a cross-species single-cell resource for exploring longevity and aging-associated cellular and molecular programs.. Nucleic acids research . https://doi.org/10.1093/nar/gkag1129
80. DNA methylation age of blood predicts all-cause mortality in later life. Genome Biology 2015. https://doi.org/10.1186/s13059-015-0584-6
81. DNA methylation-based measures of biological age: meta-analysis predicting time to death. Aging 2016. https://doi.org/10.18632/aging.101020
82. An epigenetic clock analysis of race/ethnicity, sex, and coronary heart disease. Genome Biology 2016. https://doi.org/10.1186/s13059-016-1030-0
83. HIV-1 Infection Accelerates Age According to the Epigenetic Clock. Journal of Infectious Diseases 2015. https://doi.org/10.1093/infdis/jiv277
84. The epigenetic clock is correlated with physical and cognitive fitness in the Lothian Birth Cohort 1936. International Journal of Epidemiology 2015. https://doi.org/10.1093/ije/dyu277
85. Breaking new ground on human health and well-being with epigenetic clocks: A systematic review and meta-analysis of epigenetic age acceleration associations.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102552
86. A stem cell aging clock links biological age deviation to clinical outcome in acute myeloid leukemia. bioRxiv 2026. https://doi.org/10.64898/2026.02.12.703707
87. Biological Versus Technical Reliability of Epigenetic Clocks and Implications for Disease Prognosis and Intervention Response.. Aging cell 2026. https://doi.org/10.1111/acel.70635
88. [dataset] transhumanist-already-exists/pansci-mouse-aging-snrna.  . https://huggingface.co/datasets/transhumanist-already-exists/pansci-mouse-aging-snrna
