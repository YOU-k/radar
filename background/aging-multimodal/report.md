# 多模态衰老时钟与生物年龄 · 方向背景报告

证据 78 篇 · 覆盖度 0.60 · 第 7 轮 · 更新 2026-10-18

## 本次变更

- 新增 [50] Epigenetic aging and transposon dysregulation reflect size-related lifespan compression in dogs.
- 新增 [72] Longer lipids mark aging and constrain lifespan.
- 新增 [57] Longitudinal multiomics reveals personalized aging trajectories.

## 摘要（TL;DR）

- Horvath 多组织时钟整合 82 个 Illumina 27K/450K 数据集、7844 个非癌样本，用弹性网络从 21,369 个共有 CpG 中选出 **353 个 CpG**，在多数组织中预测误差约 **3.6 年** [1]。
- 一项基于 Generation Scotland 队列 **18,859 人**的系统比较，将 14 种常用时钟与 174 种新发疾病及 10 年全因死亡关联分析，完全校正模型下 13 种时钟与 57 种疾病共 **176 个** Bonferroni 显著关联，其中 **GrimAge v2 和 DunedinPACE 各 72 个** [2]。
- 跨五种组织、83 人、284 份样本的研究显示，口腔与血液组织的表观年龄平均差**近 30 年**，多数血液时钟与口腔组织相关性低，**Skin and Blood clock** 跨组织一致性最好 [3]。
- UK Biobank 中 **45,441 人**、2,897 个血浆蛋白的训练得到 204 个蛋白的时钟，预测实际年龄 **Pearson r=0.94**，蛋白年龄差与 27 个衰老表型、全因死亡和 26 种年龄相关疾病关联 [4]。
- 基于 ARCHS4 **56,877 例**、2-114 岁人类 RNA-seq 的混合专家模型取得 **MAE=7.58 年**，肺和脑预测最佳、肝较差，但极端年龄误差大，百岁老人达 **±40 年** [5]。
- StackAge 整合 UKB 30,376 人的 2,923 个蛋白与 251 个代谢物，年龄预测 **Pearson r≈0.93**，对 2 型糖尿病、阿尔茨海默病和慢性肾脏病的 **AUC 超过 0.90**，但未整合表观遗传层、以横断面基线为主 [6]。
- 有研究指出常用 ML/AI 连续结局回归存在系统预测偏差并传播到下游关联，可产生“预测脑龄越大认知越好”这类虚假甚至反向关联，约束优化框架可改善校准与下游推断 [7]。
- **LongevityBench** 构建了覆盖 **17 项任务、5 个生物数据域**的开放评测套件，评估来自 6 个开发团队的 **18 个前沿 AI 系统**，结论是没有单一模型主导所有任务，且组学年龄预测是无论规模大小都最难的任务 [8]。
- **ComputAgeBench** 以「可靠时钟应能区分健康个体与衰老加速疾病个体」为核心假设，整合 **66 个公开血液 DNA 甲基化数据集、覆盖 19 种疾病**，测试 **13 个已发表表观遗传时钟模型**，并另建 46 个数据集用于训练新时钟 [9]。
- 四个老年人纵向队列的荟萃分析显示，**Δage每高5年全因死亡风险增加21%，校正健康、生活方式和APOE后仍增加16%**，且Δage遗传度为0.43 [10]。

## 1 背景与定义

表观遗传时钟的成熟并未终结“生物年龄”的定义之争，反而把争议从“能否预测年龄”推进到“预测的究竟是什么”。以实际年龄为训练目标的第一代时钟，其 CpG 位点在生命前二十年即呈现高度异质、非线性的发育轨迹，超过三分之一自出生便存在个体差异，并与遗传背景和产前暴露相关 [11]；这提示时钟信号部分承载的是发育程序的残留而非纯粹的损伤累积。与之呼应，程序性衰老假说将时钟 CpG 邻近的发育基因视为生命后期转为有害的持续运行程序 [12]。**因此，本方向的核心问题不是再训练一个更准的年龄回归器，而是界定“生物年龄”这一构念本身：它是损伤累积、适应能力、发育程序残留，还是系统生理能力的综合读数。** 因果时钟的分裂——DamAge 追踪损伤、AdaptAge 追踪适应，二者对短期干预均敏感但关联结局方向相反 [13]——正是这一构念张力的直接体现。概率框架进一步表明，单点年龄差之外还存在“生物年龄不确定性”，其与年龄差弱相关、随个体分子间年龄信号不一致而升高 [14]，说明把生物年龄压缩为一个标量可能系统性地丢失信息。

方向边界由此可以划清。**本方向区别于传统衰老生物标志物研究的关键，在于以“可跨数据集复现的预测模型”为产出形式，而非以单一标志物的机制阐释为终点。** 这带来两个必然的纳入要求：模型须有公开数据或系数，评测须有可比的基准。Biolearn 之所以构成本方向的基础设施型工作，正因它把标志物整理、数据集协调与系统评估统一为可复现流程，并直接暴露标志物跨人群、跨数据集的表现差异 [15]；ComputAgeBench 则以“区分健康与衰老加速疾病”为判据，整合 66 个公开血液 DNA 甲基化数据集、19 种疾病、13 个已发表时钟 [9]。**但现有基准普遍窄于方向边界**：ComputAgeBench 仅覆盖血液 DNA 甲基化 [9]，单细胞基准局限于转录组 [16]，而本方向明确包含影像、功能表型、类器官与扰动体系。跨模态可比性因此不是待办事项，而是当前基准版图的空缺。

演化脉络上，本方向经历了三次重心转移。第一次是从单组学时钟向器官特异化时钟的转移：血浆蛋白组可拆分为整体与十个器官系统的时钟，并在中国与美国队列中取得跨队列相关 r=0.98 和 0.93 [17]；代谢组可拆为五个器官特异 MetBAG [18]；影像可拆为七个 MRI 器官时钟 [19]。**器官特异化的意义不在于精度提升，而在于把“生物年龄”从全身单一读数变为可归因的器官向量**，从而使脑、动脉等特定器官的衰老加速能与特定疾病风险对应 [20]。第二次是从横断面预测向纵向与干预响应的转移：异时心脏移植显示移植心脏的表观与表达年龄快速同化受体年龄而非保留供体年龄，且不影响受体全身生物年龄 [21]；二甲双胍干预食蟹猴的多组学时钟报告脑衰老约回退 6 年 [22]；2a 期临床试验中六种蛋白质组时钟一致提示治疗组生物年龄更低，但需通路分析才能间接区分抗衰老与抗纤维化效应 [23]。**这些结果共同把时钟的效度标准从“与年龄相关”推向“对扰动敏感且方向可解释”，而后者恰恰是现有基准尚未覆盖的维度。** 第三次是从手工特征向基础模型与智能体的转移：LongevityBench 以 17 项任务、5 个数据域评测 18 个前沿系统，结论是没有单一模型全能、组学年龄预测对大小模型都最难，而 0.6B–9B 的专用 Longevity-LLM 可匹配更大通用模型 [8]；ClockBase Agent 以 40 余种时钟评估 43,602 个干预-对照比较 [24]。

**当前最尖锐的方法学争议是预测偏差与下游推断的可靠性。** 有研究指出常用 ML/AI 连续结局回归存在系统预测偏差，可产生虚假甚至方向相反的关联，并传播到“年龄差—疾病风险”这类下游分析 [7]；这与大量时钟研究报告的正向关联形成直接张力，意味着**关联方向本身可能是建模产物而非生物学信号**。与此并行的是生物学可靠性与技术重现性的脱钩：TranslAGE 对 18 种 DNAm 标志物的评估发现多数时钟技术重现性好但生物学可靠性仅低至中等，调整免疫组成后进一步下降，且技术重现性不能预测生物学可靠性 [25]。跨组织可比性同样未解：口腔与血液的表观年龄平均差近 30 年，多数血液时钟与口腔组织相关性低 [3]。**这些争议指向同一个空白：本方向缺少一个同时约束预测校准、生物学可靠性、跨组织一致性与扰动响应性的统一评测协议**；现有工作各自只覆盖其中一两个维度，且多以欧洲裔血液样本为主。

在扰动与类器官一侧，方向的边界正在向实验体系延伸，但证据形态明显弱于人群时钟。Cell Painting 作为以捕获细胞状态为目标的图像型 profiling 方法，自 2013 年提出以来协议、特征提取、质控与批次校正持续改进，已被用于机制、毒性研究与多组学整合，但该综述未提供统一定量基准 [26]。**这意味着图像型衰老建模尚缺可比的年龄标度与扰动响应基准，是本方向与高通量实验体系之间最明显的接口空缺。** 单细胞层面的衰老细胞识别则暴露出“通用 signature 与细胞类型特异 signature”的对立：SenePy 发现仅 58/1540 细胞类型组合的标志物重叠显著，通用 signature 会被异质性掩盖 [27]；hUSI 反向从 73 项研究学习通用特征并在多种条件下优于 31 种方法 [28]。**这一张力直接约束类器官与扰动体系中衰老建模的特征选择策略**：若衰老表型高度细胞类型特异，则跨体系迁移的时钟必须先做细胞类型对齐，而现有单细胞时钟多偏血液、外部验证有限 [29]。

综合来看，本方向的边界可概括为三层：底层是可公开复现的分子、影像与功能表型数据资源 [15][30]；中层是以生物年龄与衰老速率为输出的多模态模型，须处理模态对齐、缺失模态与跨队列校正 [31][32]；顶层是面向衰老生物学的 AI 基准与基础模型，须同时约束预测精度、校准、可解释性与扰动响应 [8][33]。**三层之间的衔接尚不完整：数据资源缺少统一性能基准，基准缺少跨模态与扰动维度，基础模型缺少因果与纵向验证**。这正是本方向从“造更多时钟”转向“定义生物年龄的可检验构念”的枢纽所在。

## 2 方法学


### 2.1 单组学衰老时钟（表观 / 蛋白 / 转录）

表观遗传时钟是单组学衰老时钟中发展最成熟的一支。Horvath 多组织时钟整合 82 个 Illumina 27K/450K 数据集、7844 个非癌样本，用弹性网络从 21,369 个共有 CpG 中选出 **353 个 CpG**，在多数组织中预测误差约 **3.6 年**，并显示早衰症不符合正常衰老轨迹、iPS 重编程可将时钟重置为 0 [1]。该工作确立了跨组织 DNAm 年龄预测的可行性，但其训练数据异质、组织覆盖仍有限 [1]。后续综述将这类时钟与程序性衰老理论联系起来，指出时钟 CpG 邻近 Hox、polycomb 等发育基因，提出发育程序在生命后期持续运行并转为有害的假说 [12]。

以实际年龄为替代的第一代时钟之后，训练目标转向表型与结局。DNAm PhenoAge 用包含临床表型年龄的复合指标替代实际年龄，通过两步流程筛选 CpG，在全因死亡、癌症、健康寿命、身体功能和阿尔茨海默病等预测上优于既往指标 [34]。但该模型基于全血开发，摘要未给出样本规模与误差指标，机制解释有限 [34]。另一条路线引入因果信息：通过表观全基因组孟德尔随机化识别可能因果影响衰老性状的 CpG，构建追踪损伤性变化的 **DamAge** 与适应性变化的 **AdaptAge**，前者与死亡等不良结局相关，后者与有益适应相关，且两者对短期干预敏感 [13]；其局限在于因果 CpG 的功能验证有限、依赖 MR 假设 [13]。

时钟数量的膨胀带来了可比性问题。一项基于 Generation Scotland 队列 **18,859 人**的系统比较，将 14 种常用时钟与 174 种新发疾病及 10 年全因死亡关联分析，完全校正模型下 13 种时钟与 57 种疾病共 **176 个** Bonferroni 显著关联，其中 **GrimAge v2 和 DunedinPACE 各 72 个**；第二代和第三代时钟显著优于第一代，后者在疾病场景中应用有限 [2]。该研究以欧洲裔为主、为观察性设计，且部分时钟与协变量信息重叠 [2]。LinAge2 的评测给出另一组内部对照：其预测死亡 **AUC=0.8684**，优于 PhenoAge Clinical 的 0.8479 和 ChronAge 的 0.8288；20 年死亡 **AUC=0.8440**，优于 PhenoAge DNAm 的 0.7859 和 GrimAge2 的 0.8233，但部分对比未达统计显著 [35]。这些数字来自不同队列与不同对照集，不宜跨研究直接比高低。

除预测精度外，时钟的生物学与工程属性也受到检验。跨五种组织、83 人、284 份样本的研究显示，口腔与血液组织的表观年龄平均差**近 30 年**，多数血液时钟与口腔组织相关性低，**Skin and Blood clock** 跨组织一致性最好 [3]；样本量与年龄范围有限 [3]。TranslAGE 平台对 18 种 DNAm 标志物的评估发现，多数时钟技术重现性好，但生物学可靠性低至中等，调整免疫组成后进一步下降，且技术重现性不能预测生物学可靠性 [25]。对 51 项人类干预研究统一计算 16 种时钟与 94 种额外 DNAm 标志物后，不同干预与时钟的响应差异显著，文献碎片化与面板不一致使跨研究比较困难 [36]。机制层面，多数时钟 CpG 并不与转录因子结合位点重叠，说明精度并非主要来自 TF 结合动态；但仅用弱相关的非 TFBS CpG 建模，**MdAE=3.77 年**，优于 Horvath1 的 5.95 年、接近 PhenoAge 的 3.79 年 [37]。此外，成人时钟位点在生命前二十年的发育轨迹高度异质且非线性，超过三分之一自出生即存在个体差异，高于非时钟位点，并与遗传背景和产前暴露相关 [11]。PathwayAge 则放弃单 CpG、改用 GO/KEGG 通路级甲基化建模，在多队列中保持预测与泛化能力，并识别神经退行、免疫失调、代谢病相关通路 [38]。以内在能力为目标的 IC clock 在 INSPIRE-T 队列 933 人中筛选 **91 个 CpG**，DNAm IC 与临床 IC 相关 **0.61**，并可预测死亡 [39]。

蛋白质组时钟依托大规模血浆蛋白面板迅速扩展。UK Biobank 中 **45,441 人**、2,897 个血浆蛋白的训练得到 204 个蛋白的时钟，预测实际年龄 **Pearson r=0.94**，蛋白年龄差与 27 个衰老表型、全因死亡和 26 种年龄相关疾病关联，并在 CKB（3,977 人）与 FinnGen（1,990 人）中独立验证 [4]；其局限是主要发现基于 UKB、外部样本较小、观察性关联不能证明因果 [4]。同样基于 UKB 的 PAC 使用 53,021 人、2,923 个 Olink 蛋白，以全因死亡为代理、LASSO 建模，随访超 10 年，年龄偏差与死亡及多种年龄相关疾病相关，但训练仅限 UKB、平台单一 [40]。器官特异化是另一方向：UKB 43,616 人构建整体与十个器官时钟，在中国（3,977 人）和美国（800 人）队列中跨队列 **r=0.98 和 0.93**，加速的器官衰老可预测疾病发生、进展与死亡，脑衰老与死亡关联最强 [17]。MSKAge/MSKAgeMort 聚焦肌肉骨骼系统，在 21,070 人中建模，MSKAge 相关 **r 女性=0.62、男性=0.56**，MSKAgeMort 相关 **r 女性=0.93、男性=0.88**，其加速指标可预测死亡与肌肉骨骼疾病 [41]。ECM 时钟仅用 **14 个血浆蛋白**，发现 ECM 蛋白随龄呈 U 型轨迹、最低点约 40-50 岁，但最老队列仅 66 岁、轨迹较弱 [42]。

蛋白质组也被用于刻画健康寿命而非单纯年龄。HPS 基于 UKB 53,018 人、2,920 个蛋白构建，在 43,119 名基线健康者中 **12,427 人（28.8%）** 发生健康寿命终点事件，低 HPS 与更高死亡风险和慢性阻塞性肺病等年龄相关疾病相关 [43]；该研究以欧洲裔为主、健康寿命定义尚无共识 [43]。纵向设计提供了风险因素层面的信息：KORA 队列 9105 样本、4100 人、25-88 岁的 LC-MS 血浆蛋白质组时钟显示，蛋白质组年龄加速与生活方式和临床风险因素相关，心血管代谢暴露共享蛋白质组特征，而吸烟和体力活动具独特特征，个体内血脂异常和肾功能受损与年龄加速增加相关 [44]。

转录组时钟的突出困难是平台与组织依赖。Pasta 采用“年龄偏移”学习框架，声称可跨组织、跨 bulk/单细胞 RNA-Seq 与芯片数据及物种预测相对年龄，优于 MultiTIMER 和 tAge，能区分衰老、静息与干细胞状态，p53 相关基因贡献显著 [45]；其限制包括转录组噪声与批次效应、跨平台泛化仍受限 [45]。基于 ARCHS4 **56,877 例**、2-114 岁人类 RNA-seq 的混合专家模型取得 **MAE=7.58 年**，肺和脑预测最佳、肝较差，FOSB 重要性 1.00、C4B_2 为 0.95，但极端年龄误差大，百岁老人达 **±40 年** [5]。K-Dense 多智能体系统在 ARCHS4 57,584 样本、28 组织、1,039 队列上构建的集成时钟达到 **R²=0.854、MAE=4.26 年**，并提供校准置信区间、标记过渡期与极端年龄预测 [46]。DeepQA 针对“仅在健康样本训练、却在非健康样本推断”的偏倚，用混合专家与 Hinge-MAE 损失在 3060 样本、31 数据集上训练，在健康和非健康受试者上均优于现有方法 [47]；非健康样本缺乏生物年龄金标准仍是其局限 [47]。物种与组织边界也在拓展：小鼠肝脏 RNA-seq 时钟 LivAge 在早衰模型中显示转录组年龄增加，并可评估 Snell Dwarf、Ames Dwarf、GHR 缺陷及热量限制等干预，但仅基于肝脏组织 [48]。

跨组学与跨物种的证据提示单组学时钟各有盲区。StackAge 整合 UKB 30,376 人的 2,923 个蛋白与 251 个代谢物，年龄预测 **Pearson r≈0.93**，对 2 型糖尿病、阿尔茨海默病和慢性肾脏病的 **AUC 超过 0.90**，并以单组学时钟（Horvath、Hannum、MileAge）为对照，但未整合表观遗传层、以横断面基线为主 [6]。代谢组方面，MetaboAgeMort 基于 UKB **239,291 人**、以 10 年全因死亡为目标，先选 **185 个**死亡相关代谢标志物再用 LASSO Cox 与 Gompertz 回归建模，可提升死亡预测并关联疾病、可调因素与遗传位点，但以死亡为替代指标、样本主要为欧洲白人 [49]。在犬中，894 只犬的 1640 份甲基化组构建的表观时钟可预测死亡率、生命早期表观遗传衰老最快，大体型和雄性犬寿命更短且分子衰老加速，体型相关变化集中于转座子元件、性别相关变化集中于 X 染色体 [50]。这些结果共同表明，单组学时钟的预测能力已在多个分子层得到验证，但组织可比性、生物学可靠性、极端年龄误差与跨人群泛化仍是尚未解决的争议点。

### 2.2 多模态整合与跨队列泛化

多模态整合的起点是同一平台内不同组学层的拼接。UK Biobank 中基于 **2,916 个血浆蛋白**、44,498 人的器官年龄模型覆盖 11 个器官，脑、动脉和整体年龄对传统年龄的预测 r² 达 **0.97** [20]；同一队列另一项工作用 2,448 个血浆蛋白、43,498 人构建 11 个 ProtBAG，并与 9 个表型年龄差时钟整合，报告跨器官特征可提升系统性疾病类别和全因死亡预测 [31]。代谢组层则用 107 种非衍生代谢物、274,247 人构建 5 个 MetBAG，独立测试集 Pearson r 为 **0.25<r<0.42**，关联 525 个疾病终点 [18]。影像层在 313,645 人中构建 7 个 MRIBAG，留出测试 Pearson r **0.23–0.77**、MAE 约 5 年，并关联 2,923 种蛋白与 327 种代谢物 [19]。这些数字来自不同组学与不同建模流程，不能横向比高低，只能说明各层内部预测精度差异较大。

跨模态整合的证据集中在少数队列。mCAS 基于 2,019 名 18–91 岁中国人，构建核心能力时钟、多模态时钟与器官相关时钟三层框架，报告血浆蛋白时钟可代理系统生理能力，凝血因子年龄依赖积累与多器官衰老和炎症相关 [51]。MGB Biobank 约 31,000 人开发 EMRAge，并在 3,451 人多组学子集训练 DNAmEMRAge 与 OMICmAge，随后在 All of Us 10,769 人、TruDiagnostic 14,213 人、Generation Scotland 18,672 人验证 [32]。10K 项目则以 1 万名 40–70 岁以色列健康人、每 2 年随访的纵向设计，报告男女衰老模式存在差异 [52]。三者人群与模态组合不同，尚不能判断哪种整合策略更优。

跨队列泛化被多项工作直接视为薄弱环节。表观遗传时钟方面，Horvath 与 PedBE 时钟在 523 份墨西哥儿童青少年血样中预测准确性下降，迁移学习被用于缩小目标队列差距 [53]。MRIBAG 的作者也指出腹部 MRI 特征共线性导致泛化较差、脑模型在外部队列存在域偏移 [19]；蛋白组时钟则被批评训练数据的病理构成会影响泛化与可解释性 [31]。相对轻量的路线是 GOLD BioAge：基于 Gompertz 风险函数的线性模型在 NHANES、UK Biobank 及 CHARLS、CLHLS、RuLAS 三个中国队列中验证有效 [54]；CT 模型在 123,281 名成人中 IPA 为 **29.2**，优于人口学模型的 21.7，但队列 92% 为白人、外部验证有限 [55]。

方法学争议首先落在预测偏差上。有研究指出常用 ML/AI 连续结局回归存在系统预测偏差并传播到下游关联，可产生“预测脑龄越大认知越好”这类虚假甚至反向关联，约束优化框架可改善校准与下游推断 [7]；这与上述各时钟普遍报告“年龄差—疾病风险”正向关联形成张力，提示关联方向本身可能受建模方式影响。另一条争议是年龄差之外的信息：概率框架在超过 45 万名 UK Biobank 参与者中把生物年龄差（BAG）与生物年龄不确定性（BAU）分开，报告 BAU 与 BAG 弱相关、随个体分子间年龄信号不一致而增加 [14]。这意味着单点 BAG 可能遗漏了预测分布的宽度所携带的信息。

应用侧的证据显示多模态时钟开始进入干预评估。在 rentosertib 治疗特发性肺纤维化的 12 周 2a 期试验中，六种蛋白质组时钟（ProtAge、OrganAgemortality、OrganAgechrono、PAC、ipfP3GPT、PAOPAC）一致预测治疗组生物年龄更低，但作者强调需借助通路分析间接区分抗衰老与抗纤维化效应 [23]。ClockBase Agent 整合 40 余种时钟、评估 43,602 个干预-对照比较，报告超 500 种干预显著降低生物年龄，并称更多干预加速而非延缓衰老 [24]；AURORA 框架则从多模态时钟的计算筛选中预测 *Neisseria flavescens* 为顶级候选，并在线虫中验证活菌延长寿命和健康寿命 [56]。这些结果依赖已有时钟的预测，实验验证范围有限，与临床试验中“时钟一致但机制难分”的局限相互呼应。纵向多组学刻画个体化衰老轨迹的方向已被提出，但现有摘要未给出可提取的定量结果 [57]。

### 2.3 单细胞与空间衰老图谱

单细胞转录组衰老时钟已从泛化模型走向细胞类型特异化。sc-ImmuAging 基于 **1081 名 18 至 97 岁健康欧洲人** PBMC 的约 **130 万细胞**，用 LASSO、随机森林和 PointNet 为五类免疫细胞分别建模，内外验证优于对照，并能揭示 COVID-19 感染后单核细胞与 BCG 接种后 CD8+T 细胞的年龄改变异质性 [58]。scAgeClock 则用门控多头注意力网络在 CZ CELLxGENE 大规模数据上训练，精度高于偏最小二乘、弹性网等基线 [29]；另有工作把单细胞转录组编码为基因名序列的「细胞句子」微调大语言模型，在数百万细胞上实现单细胞分辨率年龄预测，并提名可降低预测转录年龄的候选靶点 [59]。三者数据规模与建模路线不同，不宜直接比较精度高低；共同局限是外部验证有限、组织覆盖偏血液 [29]。在神经元层面，BitAge 与 Stochastic Clock 预测线虫 **128 种神经元类型**的年龄从约 **98h 到 177h**、近 **2 倍差异**，两时钟相关 Pearson **0.65**，并据此筛选出丁香酸和 vanoxerine [60]。

空间维度上，小鼠 **9 种组织**的空间转录组显示衰老敏感斑点与组织结构熵升高共定位，免疫球蛋白表达细胞聚集是其微环境特征，IgG 在雄性与雌性小鼠及人组织中积累，靶向降低 IgG 可缓解小鼠多组织衰老 [61]。人皮肤的单细胞与空间图谱构建了 SenSkin™ 基因集，发现光老化的衰老细胞负担高于时序衰老，衰老黑素细胞黑色素合成升高、衰老网状真皮成纤维细胞胶原和弹性纤维合成下降 [62]。小鼠乳腺 scRNA-seq 与 snATAC-seq 比较 **3 月龄与 18 月龄**，报告上皮 AV/HS 减少、肌上皮增加、成纤维细胞增加及衰老与癌症相关表观转录特征 [63]；人骨骼肌单核 RNA+ATAC 多组学则构建首个衰老人肌衰老细胞图谱，解析 SASP 异质性并提出 Maraviroc 作为候选干预 [64]。

衰老细胞识别本身存在方法学争议。SenePy 用 **72 个小鼠和 64 个人类**加权单细胞 signature 构建评分平台，发现仅 **58/1540** 细胞类型组合的标志物重叠显著，即标志物高度组织细胞特异，通用 signature 会被异质性掩盖 [27]。hUSI 走相反路线，从 **73 项**公开 RNA-seq 研究学习通用衰老特征，在 bulk 和单细胞多种条件下优于 **31 种**方法 [28]。两者对「通用」与「细胞类型特异」的侧重不同，构成该子问题的核心张力；综述亦指出缺乏特异性标志物、衰老细胞稀少且异质动态是多组学识别的主要障碍 [65]。脑衰老方面，单细胞组学综述总结了细胞类型变化、细胞互作与年轻化干预评估，但未给出定量结果 [66]。

### 2.4 衰老生物学基准与基础模型

衰老生物学正从单一模态的专用时钟走向标准化基准与基础模型。**LongevityBench** 构建了覆盖 **17 项任务、5 个生物数据域**的开放评测套件，评估来自 6 个开发团队的 **18 个前沿 AI 系统**，结论是没有单一模型主导所有任务，且组学年龄预测是无论规模大小都最难的任务；作者同时微调 5 个 **0.6B–9B** 参数的多任务 Longevity-LLM，可匹配或超过更大的前沿系统 [8]。与之呼应，**Longevity-LLM v0.1** 将 Qwen3-14B 在 DNA 甲基化、蛋白质组、临床生物标志物和 RNA 表达上微调，强化微调后表观年龄预测 **MAE 为 4.34 年**，超过 Horvath 多组织时钟，蛋白质组谱生成显著优于所有前沿 LLM [33]。在单细胞层面，一项基准评估 **10 个通用单细胞基础模型、3 个衰老专用模型**及传统方法，覆盖 5 个生物学问题、**超过 250 万单细胞转录组**，冻结预训练表征下 Geneformer 在时序年龄预测和年龄伪时间一致性上最佳，但 **2000 个高变基因**平均表现更高，多个模型在三种疾病背景中捕捉到正向分子年龄偏移 [16]。这些工作共同显示：专用小模型与通用大模型各有胜场，评测结论高度依赖任务与表征方式。

表观遗传时钟的标准化评测已有专门尝试。**ComputAgeBench** 以「可靠时钟应能区分健康个体与衰老加速疾病个体」为核心假设，整合 **66 个公开血液 DNA 甲基化数据集、覆盖 19 种疾病**，测试 **13 个已发表表观遗传时钟模型**，并另建 46 个数据集用于训练新时钟 [9]。综述层面，临床衰老时钟正从表观遗传向多组学、多模态整合演进，AI 的集成学习与深度学习被认为推动了准确性、可解释性和泛化性进展 [67]；另一篇系统综述将 AI 生物年龄预测拆解为生物标志物选择、特征工程、模型开发、偏倚校正和性能评估，并指出数据异质性、泛化性有限、可解释性不足与临床转化障碍等挑战 [68]。更广的综述梳理 2016–2024 年间 **125 篇同行评审研究**，总结 CNN、RNN、GAN、LLM 和扩散模型在衰老时钟、合成数据生成、药物发现和多模态健康评估中的应用，但属叙述性综述、缺乏定量荟萃分析 [69]。生物年龄预测器与「人类数字孪生」的结合被提出用于动态模拟干预与风险，其中表观时钟被认为预测生物年龄和健康表型最准确，落地则受数据整合、隐私、互操作性和纵向建模限制 [70]。

争议与空白集中在验证环节。有观点指出，AI 与 LLM 用于 geroprotective 干预评估时应满足正确、有用、全面、可解释，并考虑因果、跨学科、标准、纵向数据和已知衰老生物学，建议采用 LLM 加知识图谱与检索增强生成并开展基准测试，而非依赖传统生物医学数据库比较或朴素 LLM 查询；该文为要求类论文，未提供具体实验验证或定量结果 [71]。与此相对，上述基准工作多以区分疾病或预测年龄为判据，尚未统一到干预评估的因果与纵向要求上；同时 ComputAgeBench 仅基于血液 DNA 甲基化、未覆盖其他模态 [9]，单细胞基准则局限于转录组 [16]，跨模态可比性仍是未解问题。

### 2.5 类器官、扰动与 Cell Painting 衰老建模

基于图像的高内涵成像已能支撑高通量实验，而图像型profiling 不再只测量少量特征，而是利用图像中的丰富信息识别生物样本之间的相似性与差异；**Cell Painting** 正是一种以捕获细胞状态为目标的显微细胞标记 assay，于 **2013 年**提出，用于优化和标准化图像型profiling [26]。该综述指出，Cell Painting 能捕获细胞对各种扰动的响应，其协议、特征提取、质控与批次校正持续改进，并已被用于机制、毒性等研究以及多组学整合 [26]。

在方法学定位上，该工作将图像型profiling 与传统高内涵筛选所代表的少量特征测量相对照，强调前者对样本间相似/差异的判别能力 [26]。不过，作为一篇综述，它**未提供统一定量基准**，其结论依赖公开数据集与计算、实验技术的进展，未来方向包括计算与实验技术、新公开数据集以及与其他高内涵数据的整合 [26]。

### 2.6 跨物种与跨组织衰老标志（脂质组等）

跨物种、多组织脂质组学比较显示，**脂酰链延长**是小鼠、线虫、果蝇和人类衰老的保守标志；衰老并非单一脂质分子的增减，而是表现为向长链脂质转变并伴随短链脂质耗竭的**比值性重塑**，人类心脏病进展中也出现类似延长 [72]。该研究同时鉴定了脂质重塑因子 **Plb1** 参与调控这一过程 [72]。

在干预层面，同一研究内的对照显示，饮食限制可缩短小鼠心脏脂质 [72]，提示脂质链长重塑不仅是衰老的伴随现象，也可能受寿命调控干预影响。上述证据覆盖多物种与多组织，但各物种、组织间的具体脂质变化幅度未在证据中给出，尚无法据此比较不同队列或物种间差异的大小 [72]。

## 3 数据与资源

面向多模态衰老时钟的数据资源建设，目前主要沿两条路径展开。其一是以统一整理与评估为目标的通用框架：**Biolearn** 作为开源库，针对跨人群验证缺乏标准化方法、标志物设计分散、数据集结构不一致等问题，提供整理、协调与系统评估的统一框架，并基于多公开数据集对多种衰老生物标志物进行系统比较，输出可复现的评估流程 [15]。其二是面向特定系统的多组学数据库：**Immunosenescence Inventory** 整合单细胞转录组、bulk 转录组、表观组与 TCR/BCR 等多物种数据，提供知识整理、多模态数据集与工具，其中工具涵盖免疫细胞识别与免疫时钟计算，用于评估生物年龄、预测年龄相关疾病及干预影响 [30]。

两者在定位与覆盖上存在差异。Biolearn 侧重跨数据集的标志物性能、稳健性与泛化性比较，但依赖已有公开数据，临床验证仍待推进 [15]；Immunosenescence Inventory 以免疫系统为聚焦，覆盖多物种与年龄阶段并开放获取，但与 ImmPort、InnateDB、Aging Atlas 等既有数据库的整合依赖已有数据，未提供统一预测性能基准，单细胞层面的免疫衰老覆盖仍有限 [30]。前者提供可复现的评估框架而缺少专门的多模态免疫数据资源，后者提供多模态数据与免疫时钟工具而缺少统一性能基准，二者在「可比较的评估标准」上尚未形成衔接。

## 4 应用与结果

在血液DNA甲基化时钟的死亡预测上，多项队列研究给出了方向一致但强度不同的证据。四个老年人纵向队列的荟萃分析显示，**Δage每高5年全因死亡风险增加21%，校正健康、生活方式和APOE后仍增加16%**，且Δage遗传度为0.43 [10]。随后扩展到**13个队列13,089人、2,734例死亡**的荟萃分析比较了Horvath 353 CpG与Hannum 71 CpG时钟，表观年龄与实足年龄相关系数为0.65–0.89，年龄加速与全因死亡风险增加相关，并报告血液细胞组成信息可提升预测 [73]。同一353 CpG时钟还被用于种族/民族、性别与冠心病分析，发现表观年龄加速存在种族和性别差异并与CHD相关，但以横断面为主、组织来源异质 [74]。系统综述则汇总299篇文献、1050个EAA-因素关联和53种时钟，对选定配对做随机效应荟萃分析，报告若干EAA与生理、认知、社会和环境因素存在显著汇总关联，同时指出研究异质性大、因果方向不明确 [75]。

在特定暴露与功能结局方面，证据呈现出“横断面有关、纵向预测有限”的分化。HIV感染研究使用11个甲基化数据集，在血液和脑组织均观察到感染者表观年龄加速显著增加，但样本量有限且为横断面设计 [76]。Lothian Birth Cohort 1936在70岁（n=920）、73岁（n=299）、76岁（n=273）三波测量中发现，表观年龄加速与70岁步行速度、握力、肺功能和认知能力横断面相关，**但不预测70至76岁间的功能下降** [77]。这一差异提示时钟与功能指标的关联可能更多反映同期状态而非后续变化轨迹。

干预与器官层面的应用开始把时钟从关联推向动态评估。40个月二甲双胍干预雄性食蟹猴的研究构建了多组织转录组、DNA甲基化、血浆蛋白和代谢组的猴衰老时钟，报告**脑衰老约回退6年**、脑结构保护与认知增强，部分由Nrf2激活介导，但仅限雄性食蟹猴、人类转化待验证 [22]。异时心脏移植的多组学分析则显示，移植心脏的DNA甲基化和基因表达生物年龄快速同化受体年龄而非保留供体年龄，且**仅限移植物、不影响受体全身生物年龄**，全文尚未公开、样本与组学细节不明 [21]。另有研究提出干细胞衰老时钟连接生物学年龄偏差与急性髓系白血病临床结局，但仅有标题、无摘要，具体定量结果与验证细节无法评估 [78]。

## 5 评测、可复现性与争议

（本节暂无入库证据）

## 6 空白与趋势

**趋势一：从“单组学专用时钟”走向“可比较的基准与基础模型”，但评测维度仍不完整。** LongevityBench 以 17 项任务、5 个数据域、18 个前沿系统给出“无单一模型全能、组学年龄预测最难”的结论，并显示 0.6B–9B 的专用 Longevity-LLM 可匹配更大通用模型 [8]；Longevity-LLM v0.1 在表观年龄预测上 MAE 4.34 年 [33]；单细胞基准覆盖超 250 万细胞、10 个通用基础模型与 3 个衰老专用模型，发现冻结表征下 Geneformer 最佳但 2000 高变基因平均更高 [16]。**空白在于：现有基准多以“预测年龄/区分疾病”为判据，尚未统一到干预评估所需的因果与纵向要求**；ComputAgeBench 仅覆盖血液 DNA 甲基化、19 种疾病、13 个时钟 [9]，单细胞基准局限于转录组 [16]，跨模态可比性无人系统解决。要求类论文已明确提出 LLM 用于 geroprotective 评估须满足正确、有用、全面、可解释并考虑因果与纵向数据，但未提供实验验证 [71]。

**趋势二：多模态整合从“同平台拼接”走向“器官特异 + 跨队列验证”，但整合策略孰优无人判定。** 蛋白组侧已有 11 器官 ProtBAG 与 9 个表型年龄差时钟的整合分析 [31]、11 器官蛋白组时钟跨中国与美国队列 r=0.98/0.93 [17]；代谢组 5 个 MetBAG 独立测试 r 仅 0.25–0.42 [18]；影像 7 个 MRIBAG 留出测试 r 0.23–0.77 [19]。跨模态证据集中在少数队列：mCAS 2,019 名中国人三层框架 [51]、MGB Biobank 约 31,000 人 EMRAge 及三个外部验证集 [32]、10K 项目 1 万人纵向 [52]。**空白在于：三者人群与模态组合不同，尚无头对头比较判断哪种整合策略更优；也缺少在缺失模态条件下仍可用的整合方法在真实多队列上的系统评估。**

**趋势三：预测偏差与不确定性正被当作独立问题处理，但尚未进入主流时钟的下游关联流程。** 有研究指出 ML/AI 连续结局回归的系统预测偏差会传播到下游关联，可产生虚假甚至方向相反的关联，约束优化框架可改善校准 [7]；概率框架在超 45 万 UKB 参与者中把 BAG 与生物年龄不确定性 BAU 分离，报告 BAU 与 BAG 弱相关 [14]。**这与大量时钟普遍报告的“年龄差—疾病风险”正向关联形成张力**：若偏差可致关联反向，则现有以 BAG 为暴露的关联结论方向本身需重新检验。**空白在于：尚无工作把偏差校正与不确定性量化同时嵌入多模态时钟的构建—验证—下游关联全链条。**

**趋势四：单细胞与空间衰老建模快速扩张，但“通用 signature 还是细胞类型特异 signature”仍是未决张力。** SenePy 用 72 小鼠 + 64 人类 signature 发现仅 58/1540 细胞类型组合标志物重叠显著 [27]；hUSI 从 73 项研究学习通用特征并在 bulk 与单细胞优于 31 种方法 [28]；综述指出缺乏特异性标志物、衰老细胞稀少且异质动态是主要障碍 [65]。单细胞时钟已细胞类型特异化：sc-ImmuAging 基于 1081 人约 130 万细胞 [58]、scAgeClock 门控多头注意力 [29]、LLM 编码“细胞句子” [59]，但**外部验证有限、组织覆盖偏血液** [29]。空间侧有 9 组织小鼠图谱与 IgG 机制验证 [61]、人皮肤 SenSkin™ [62]、乳腺 3 月龄 vs 18 月龄多组学 [63]、人骨骼肌单核 RNA+ATAC [64]。**空白在于：空间衰老时钟本身尚未被提出——现有空间工作输出的是图谱与机制，而非可跨组织泛化的年龄/衰老速率预测器；单细胞时钟也尚未与空间坐标或影像表型对齐。**

**趋势五：类器官、扰动与 cell painting 体系中的衰老建模几乎空白。** Cell Painting 自 2013 年提出，已能捕获细胞对扰动的响应并用于机制、毒性及多组学整合，但该综述明确未提供统一定量基准 [26]。**在纳入证据中，没有任何一项工作把 Cell Painting 或类器官体系直接用于训练衰老时钟或估计生物学年龄**；现有扰动侧证据是 ClockBase Agent 对 43,602 个干预-对照比较的计算再分析 [24] 与 AURORA 的计算筛选加线虫验证 [56]，均非图像表型。**这是方向内最明确的空白：图像型高内涵表型尚未接入多模态衰老时钟，类器官中的年轻化/衰老建模缺少可公开的系数与基准。**

**趋势六：跨队列泛化与数据资源正从“各自建库”走向“统一整理”，但评估标准与数据资源尚未衔接。** 泛化薄弱已被多方直接指出：Horvath 与 PedBE 在 523 份墨西哥儿童青少年血样中准确性下降、需迁移学习 [53]；MRIBAG 腹部特征共线性致泛化差、脑模型存在域偏移 [19]；蛋白组时钟训练数据的病理构成影响泛化与可解释性 [31]。资源侧 Biolearn 提供统一整理与系统评估框架但依赖已有公开数据、临床验证待推进 [15]；Immunosenescence Inventory 提供多物种多模态免疫数据与免疫时钟工具但无统一性能基准、单细胞免疫衰老覆盖有限 [30]。**空白在于：前者有评估框架缺专门多模态免疫数据，后者有数据缺统一基准，二者在“可比较的评估标准”上尚未形成衔接；跨模态、跨人群的公开系数与可复现评测流程仍是稀缺品。**

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 单组学衰老时钟（表观/蛋白/转录） | 成熟 | 表观时钟的方法学骨架早在 2013 年就已奠定（[1]，6423 次引用），随后 Horvath 二代时钟（[34]）与因果富集表观年龄（[13]）主要是在同一框架内做增量改进；蛋白组时钟（[4]）把模态从甲基化换到蛋白，但建模范式（惩罚回归/弹性网 + 年龄预测 + 死亡率关联）没有变。雷达样本中该节 n=28、中位引用仅 9，说明新工作多为应用与增量。 |
| 2.2 多模态整合与跨队列泛化 | 朝阳 | 该节雷达样本 n=16、近两年占比 **0.92**、CNS 占比 **0.56**，是典型的近两年爆发；但方法明显未收敛：血浆蛋白组连接脑—免疫衰老（[20]）、MRI 多器官时钟（[19]）、表型组性别特异动态（[52]）各自用不同模态组合与不同对齐策略，尚无统一的多模态衰老表征与缺失模态处理标准。 |
| 2.3 单细胞与空间衰老图谱 | 朝阳 | 空间转录组揭示免疫球蛋白相关衰老（[61]）与单细胞免疫衰老时钟揭示个体异质性（[58]）代表两条尚未合流的技术路线：前者是图谱式描述，后者是时钟式建模；细胞类型特异的衰老景观（[27]）与乳腺单细胞衰老图谱（[63]）进一步说明数据在快速积累但标注与衰老标签定义不统一。 |
| 2.4 衰老生物学基准与基础模型 | 萌芽 | 该节雷达样本 n=9、中位引用 **0**、CNS 占比仅 0.11，说明尚无被广泛引用的旗舰基准；现有工作主要是基准的初步尝试（[9] ComputAgeBench 表观时钟基准）与验证规范讨论（[71]），以及综述性梳理（[69]）。缺少跨模态、跨队列的统一评测协议，是典型的萌芽期特征。 |
| 2.5 类器官、扰动与 Cell Painting 衰老建模 | 证据不足 | 雷达样本中该节仅 1 篇（[26]，Cell Painting 十年综述），且是成像方法综述而非衰老建模；无法据此判断阶段，需补充检索类器官衰老与扰动筛选的原始研究。 |
| 2.6 跨物种与跨组织衰老标志（脂质组等） | 证据不足 | 雷达样本中该节仅 1 篇（[72]，长链脂质标记衰老并约束寿命），单篇不足以判断阶段。 |
| 3 数据与资源 | 萌芽 | 雷达样本中该节仅 2 篇：衰老生物标志物统一 curation 与评估框架（[15]）与免疫衰老多组学数据库（[30]），均为 2025 年新出，说明资源层刚开始被系统化，尚未形成社区标准。 |
| 4 应用与结果 | 成熟 | 该节中位引用 **524**、近两年占比仅 **0.22**，高引用集中在 2015–2016 年的死亡率预测与荟萃分析（[10]、[73]），以及种族/性别与冠心病关联（[74]）、HIV 加速衰老（[76]）；这些是时钟作为暴露/结局关联工具的成熟应用，新意主要在应用场景而非方法。 |
| 5 评测、可复现性与争议 | 证据不足 | 雷达样本中该节 n=0，无证据可判断；但结合 2.4 的基准萌芽状态，可推测评测层整体薄弱。 |

**整体判断**：这个方向整体处于**朝阳期偏早期**——单组学时钟（2.1）与应用层（4）已成熟，构成稳定的方法底座；真正的增量与竞争集中在**多模态整合（2.2）与单细胞/空间（2.3）**，雷达样本中这两节近两年占比分别为 **0.92** 与 **0.75**、CNS 占比 **0.56** 与 **0.58**，说明热度与发表通道都在，但方法未收敛、评测标准缺失（2.4 中位引用 **0**、5 节 n=0）。窗口期估计**还有 12–24 个月**：一旦跨模态对齐与缺失模态处理出现被广泛复用的范式，或 LongevityBench 类基准定型，后来者将只能做增量。最大不确定性是**衰老标签本身的定义不统一**（ chronological age、死亡率、衰弱指数、细胞衰老标志混用），以及**跨队列泛化的可复现性**——若基准层不能建立，多模态时钟的“更强”很难被审稿人认可。

**接下来怎么做**：

1. **把类器官多组学做成“扰动—衰老时钟”闭环，抢占 2.5 的空白**。切入点：用合作项目的类器官体系，在扰动（基因敲低/化合物/年轻化因子）前后采集转录组 + 甲基化或成像（Cell Painting 式）多模态读出，训练“扰动响应型衰老时钟”，输出的是扰动对生物年龄的效应量而非单纯年龄预测。为什么现在做：2.5 在雷达样本中仅 1 篇综述（[26]），而 2.2 的多模态方法已证明蛋白/影像时钟可行（[20]、[19]），把成熟时钟范式迁移到扰动体系是低风险高差异化的切口。

2. **做“缺失模态鲁棒”的多模态衰老表征，直接打 2.2 的方法缺口**。切入点：用公共大队列（蛋白组 + 甲基化 + 影像 + 表型）构造模态缺失场景，比较模态对齐（对比学习/跨模态翻译）与缺失模态插补对年龄预测与死亡率关联的影响，产出可复用的缺失模态基准与代码。为什么现在做：2.2 近两年占比 **0.92** 但各工作模态组合互不兼容（[20]、[52]），缺失模态处理尚无人系统做；且 2.4 的基准层薄弱（[9] 仅覆盖表观时钟），先发即标准。

3. **把单细胞衰老时钟从“描述异质性”推进到“跨组织可迁移”**。切入点：整合公开单细胞/空间衰老图谱（[63]、[27]），用细胞类型特异的衰老评分做迁移学习，检验在合作项目类器官数据上的零样本/少样本迁移能力，产出跨组织衰老时钟与迁移性评估。为什么现在做：单细胞免疫衰老时钟已证明个体异质性可建模（[58]），但跨组织迁移未验证；空间图谱（[61]）提供了空间标签，正好补上“组织微环境”这一维。

4. **参与/自建衰老时钟评测基准，作为方法工作的放大器**。切入点：以 ComputAgeBench（[9]）与统一 curation 框架（[15]）为起点，扩展为多模态、含缺失模态与跨队列划分的基准，纳入免疫衰老数据库（[30]）作为数据源之一。为什么现在做：2.4 中位引用 **0**、5 节 n=0，评测层是明显空位；基准工作能让你后续的多模态时钟方法获得“被引用为评测标准”的复利，且与博后的算法背景高度匹配。

5. **用公共数据先做 demo，锁定“多模态 vs 单模态”的增量证据**。切入点：选一个同时有甲基化、蛋白组与死亡随访的公共队列，复现单组学时钟（[1]、[4]）作为基线，再叠加多模态融合，量化增量预测增益与跨队列衰减。为什么现在做：应用层已成熟（[10]、[73]），审稿人默认要求与单组学基线对比；先有 demo 才能在类器官项目上主张多模态的必要性，也便于在 12–24 个月窗口内快速产出第一篇方法论文。

## 参考文献

1. DNA methylation age of human tissues and cell types. Genome Biology 2013. https://doi.org/10.1186/gb-2013-14-10-r115
2. An unbiased comparison of 14 epigenetic clocks in relation to 174 incident disease outcomes.. Nature communications 2025. https://doi.org/10.1038/s41467-025-66106-y
3. Cross-tissue comparison of epigenetic aging clocks in humans.. Aging cell 2025. https://doi.org/10.1111/acel.14451
4. Proteomic aging clock predicts mortality and risk of common age-related diseases in diverse populations. Nature Medicine 2023. https://doi.org/10.1038/s41591-024-03164-7
5. Transcriptomic age prediction using mixture-of-experts models reveals tissue-specific aging signatures in large-scale human RNA-sequencing data. medRxiv 2025. https://doi.org/10.1101/2025.06.28.25330474
6. StackAge: an ensemble-based clock for precise quantification of biological age using multi-omics data.. Briefings in bioinformatics 2026. https://doi.org/10.1093/bib/bbag271
7. Trustworthy ML/AI for Aging Clocks: Preventing Systematic Prediction Bias in Biological Age Estimation. bioRxiv 2026. https://doi.org/10.64898/2026.05.27.728155
8. An open benchmark and language models for AI in aging biology.. Cell 2026. https://doi.org/10.1016/j.cell.2026.08.026
9. ComputAgeBench: Epigenetic Aging Clocks Benchmark. bioRxiv 2025. https://doi.org/10.1145/3711896.3737382
10. DNA methylation age of blood predicts all-cause mortality in later life. Genome Biology 2015. https://doi.org/10.1186/s13059-015-0584-6
11. Characterising developmental dynamics of adult epigenetic clock sites.. EBioMedicine 2024. https://doi.org/10.1016/j.ebiom.2024.105425
12. Epigenetic clocks and programmatic aging.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102546
13. Causality-Enriched Epigenetic Age Uncouples Damage and Adaptation. bioRxiv 2023. https://doi.org/10.1038/s43587-023-00557-0
14. Uncertainty redefines biological age.  . https://doi.org/10.64898/2026.09.26.26364091
15. A unified framework for systematic curation and evaluation of aging biomarkers.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00987-y
16. Benchmarking single-cell foundation models for aging biology.  . https://doi.org/10.64898/2026.09.21.753191
17. Organ-specific proteomic aging clocks predict disease and longevity across diverse populations.. Nature aging 2025. https://doi.org/10.1038/s43587-025-01016-8
18. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
19. MRI-based multi-organ clocks for healthy aging and disease assessment.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03999-8
20. Plasma proteomics links brain and immune system aging with healthspan and longevity.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03798-1
21. Transplanted hearts assimilate the recipient’s biological age. bioRxiv 2026. https://doi.org/10.64898/2026.09.15.751836
22. Metformin decelerates aging clock in male monkeys.. Cell 2024. https://doi.org/10.1016/j.cell.2024.08.021
23. Integration of proteomic aging clocks in a phase 2a clinical trial supports simultaneous geroprotective assessment.. Nature Biotechnology 2026. https://doi.org/10.1038/s41587-026-03286-y
24. Autonomous AI Agents Discover Aging Interventions from Millions of Molecular Profiles. bioRxiv 2025. https://doi.org/10.1101/2023.02.28.530532
25. Biological Versus Technical Reliability of Epigenetic Clocks and Implications for Disease Prognosis and Intervention Response.. Aging cell 2026. https://doi.org/10.1111/acel.70635
26. Cell Painting: a decade of discovery and innovation in cellular imaging.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02528-8
27. Unveiling the cell-type-specific landscape of cellular senescence through single-cell transcriptomics using SenePy.. Nature communications 2025. https://doi.org/10.1038/s41467-025-57047-7
28. A transcriptome-based human universal senescence index (hUSI) robustly predicts cellular senescence under various conditions.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00886-2
29. scAgeClock: a single-cell transcriptome-based human aging clock model using gated multi-head attention neural networks.. npj aging 2026. https://doi.org/10.1038/s41514-026-00379-5
30. Immunosenescence Inventory-a multi-omics database for immune aging research.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1102
31. Refining the generation, interpretation and application of multi-organ, multi-omics biological aging clocks.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00928-9
32. OMICmAge quantifies biological age by integrating multi-omics with electronic medical records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01073-7
33. The End of Aging Clocks: Training Foundation Models to Reason in Aging and Longevity. bioRxiv 2026. https://doi.org/10.64898/2026.03.28.714980
34. An epigenetic biomarker of aging for lifespan and healthspan. bioRxiv 2018. https://doi.org/10.18632/aging.101414
35. LinAge2: providing actionable insights and benchmarking with epigenetic clocks.. npj aging 2025. https://doi.org/10.1038/s41514-025-00221-4
36. Responsiveness of epigenetic aging biomarkers to longevity interventions in humans.. Nature medicine 2026. https://doi.org/10.1038/s41591-026-04562-9
37. Enhancing the performance and interpretability of epigenetic clocks.. Nucleic acids research 2026. https://doi.org/10.1093/nar/gkag661
38. Decoding disease-specific ageing mechanisms through pathway-level epigenetic clock: insights from multi-cohort validation.. EBioMedicine 2025. https://doi.org/10.1016/j.ebiom.2025.105829
39. A blood-based epigenetic clock for intrinsic capacity predicts mortality and is associated with clinical, immunological and lifestyle factors.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00883-5
40. Proteomic aging clock (PAC) predicts age‐related outcomes in middle‐aged and older adults. Aging Cell 2024. https://doi.org/10.1111/acel.14195
41. Construction and Validation of Plasma Protein-Based Musculoskeletal Biological Age and Genetic and Environmental Risk Profiles.. Aging cell 2026. https://doi.org/10.1111/acel.70636
42. An Extracellular Matrix Aging Clock Based on Circulating Matrisome Proteins Predicts Biological Aging and Disease.. Aging cell 2026. https://doi.org/10.1111/acel.70474
43. A proteomic signature of healthspan.. Proceedings of the National Academy of Sciences of the United States of America 2025. https://doi.org/10.1073/pnas.2414086122
44. Intraindividual longitudinal changes of the proteome reveal dynamic markers of biological aging.  . https://doi.org/10.64898/2026.10.01.755909
45. Pasta, a Versatile Transcriptomic Clock, Maps the Chemical and Genetic Determinants of Aging and Rejuvenation. bioRxiv 2025. https://doi.org/10.1002/advs.76740
46. Guided multi-agent AI invents highly accurate, uncertainty-aware transcriptomic aging clocks. bioRxiv 2025. https://doi.org/10.1101/2025.09.08.674588
47. DeepQA: A Unified Transcriptome-Based Aging Clock Using Deep Neural Networks.. Aging cell 2025. https://doi.org/10.1111/acel.14471
48. LivAge: An Online Aging Clock for Murine Transcriptomic Age Estimation.. Aging cell 2026. https://doi.org/10.1111/acel.70677
49. A Novel Metabolomic Aging Clock Predicting Health Outcomes and Its Genetic and Modifiable Factors. Advancement of science 2024. https://doi.org/10.1002/advs.202406670
50. Epigenetic aging and transposon dysregulation reflect size-related lifespan compression in dogs.. Science (New York, N.Y.) . https://doi.org/10.1126/science.aeb2986
51. Multimodal clocks of human aging.. Cell 2026. https://doi.org/10.1016/j.cell.2026.04.025
52. Phenome-wide associations of human aging uncover sex-specific dynamics.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00734-9
53. BRIDGING THE GAP: ENHANCING THE GENERALIZABILITY OF EPIGENETIC CLOCKS THROUGH TRANSFER LEARNING.. The annals of applied statistics 2026. https://doi.org/10.1214/26-aoas2136
54. Gompertz Law-Based Biological Age (GOLD BioAge): A Simple and Practical Measurement of Biological Ageing to Capture Morbidity and Mortality Risks.. Advanced science (Weinheim, Baden-Wurttemberg, Germany) 2025. https://doi.org/10.1002/advs.202501765
55. Biological age model using explainable automated CT-based cardiometabolic biomarkers for phenotypic prediction of longevity.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56741-w
56. Multi-modality profiling identifies Neisseria flavescens as a central geroprotective oral commensal in humans.. Nature aging . https://doi.org/10.1038/s43587-026-01220-0
57. Longitudinal multiomics reveals personalized aging trajectories.. Nature aging . https://doi.org/10.1038/s43587-026-01248-2
58. Single-cell immune aging clocks reveal inter-individual heterogeneity during infection and vaccination.. Nature aging 2025. https://doi.org/10.1038/s43587-025-00819-z
59. Universal Single-Cell Transcriptomic Aging Clock powered by LLMs reveals targets to slow cellular aging. Innovation in aging 2025. https://doi.org/10.1093/geroni/igaf122.4305
60. Aging clocks delineate neuron types vulnerable or resilient to neurodegeneration and identify neuroprotective interventions.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01067-5
61. Spatial transcriptomic landscape unveils immunoglobin-associated senescence as a hallmark of aging.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.019
62. Mapping epidermal and dermal cellular senescence in human skin aging.. Aging cell 2024. https://doi.org/10.1111/acel.14358
63. Comprehensive single-cell aging atlas of healthy mammary tissues reveals shared epigenomic and transcriptomic signatures of aging and cancer.. Nature aging 2024. https://doi.org/10.1038/s43587-024-00751-8
64. Multiomics and cellular senescence profiling of aging human skeletal muscle uncovers Maraviroc as a senotherapeutic approach for sarcopenia.. Nature communications 2025. https://doi.org/10.1038/s41467-025-61403-y
65. Advancing biological understanding of cellular senescence with computational multiomics.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02314-y
66. Brain aging and rejuvenation at single-cell resolution.. Neuron 2025. https://doi.org/10.1016/j.neuron.2024.12.007
67. The Evolving Landscape of Clinical Aging Clocks: From Epigenetic to Multi-Omics Integration.. Aging cell 2026. https://doi.org/10.1111/acel.70579
68. Artificial intelligence approaches in biological age prediction: current status and challenges.. British journal of biomedical science 2026. https://doi.org/10.3389/bjbs.2026.16141
69. Deep learning and generative artificial intelligence in aging research and healthy longevity medicine.. Aging 2025. https://doi.org/10.18632/aging.206190
70. From ageing clocks to human digital twins in personalising healthcare through biological age analysis.. NPJ digital medicine 2025. https://doi.org/10.1038/s41746-025-01911-9
71. Validation Requirements for AI-based Intervention-Evaluation in Aging and Longevity Research and Practice. Ageing Research Reviews 2024. https://doi.org/10.1016/j.arr.2024.102617
72. Longer lipids mark aging and constrain lifespan.. Nature aging . https://doi.org/10.1038/s43587-026-01223-x
73. DNA methylation-based measures of biological age: meta-analysis predicting time to death. Aging 2016. https://doi.org/10.18632/aging.101020
74. An epigenetic clock analysis of race/ethnicity, sex, and coronary heart disease. Genome Biology 2016. https://doi.org/10.1186/s13059-016-1030-0
75. Breaking new ground on human health and well-being with epigenetic clocks: A systematic review and meta-analysis of epigenetic age acceleration associations.. Ageing research reviews 2024. https://doi.org/10.1016/j.arr.2024.102552
76. HIV-1 Infection Accelerates Age According to the Epigenetic Clock. Journal of Infectious Diseases 2015. https://doi.org/10.1093/infdis/jiv277
77. The epigenetic clock is correlated with physical and cognitive fitness in the Lothian Birth Cohort 1936. International Journal of Epidemiology 2015. https://doi.org/10.1093/ije/dyu277
78. A stem cell aging clock links biological age deviation to clinical outcome in acute myeloid leukemia. bioRxiv 2026. https://doi.org/10.64898/2026.02.12.703707
