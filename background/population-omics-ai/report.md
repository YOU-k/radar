# 人群健康与多组学 AI · 方向背景报告

证据 105 篇 · 覆盖度 0.83 · 第 11 轮 · 更新 2026-10-18

## 本次变更

- 新增 [49] Decomposing polygenic risk of coronary artery disease into distinct biological processes
- 新增 [63] Imputation of fluid intelligence scores reduces ascertainment bias and increases power for analyses of common and rare variants.

## 摘要（TL;DR）

- Delphi-2M 改造 GPT 架构，在 UK Biobank 约 40 万参与者上训练、在丹麦登记数据中验证，词汇覆盖 1000 多种 ICD-10 顶层诊断及性别、BMI、吸烟、饮酒和死亡，可同时预测多种疾病的未来发生率并模拟个体终身轨迹 [1]。
- Foresight 强调自由文本约占 EHR 的 80%，用生成式预训练 Transformer 融合结构化与非结构化数据，覆盖 18 类 SNOMED 概念，支持日/周/月不同时间分辨率的预测 [2]。
- Foresight-England 是 243M 参数的 Transformer 解码器，在 NHS England 安全数据环境内从头训练，使用约 6100 万人的去标识化纵向 EHR（训练 5490 万、评估 610 万），但因数据访问暂停，定量结果无法导出 [3]。
- ALADYNOULLI 在三个生物库 n>683,000、随访 52 年、348 种疾病上识别出 21 个可复制特征，跨队列组成保留中位 80%，基于特征的 GWAS 发现 151 个全基因组显著位点 [4]。
- 在 All of Us 297,861 人（11.1% 为病例）中，仅用 12 项常规生物标志物 3 年轨迹特征的 LightGBM 模型 AUROC 达 0.797，显著优于静态汇总的 0.755（P<0.001），说明结构化轨迹特征本身已含可观信号 [5]。
- 真正的争议在于：生成式框架带来的增益究竟来自对时间与共病结构的建模，还是来自更大数据规模与更强表征，目前尚无同一研究内部的对照给出答案。
- UK Biobank 的 Pharma Proteomics Project 在 54,219 名参与者、2,923 种血浆蛋白中报告 14,287 个主要遗传关联，81% 为既往未报道，并精细映射出 29,420 个独立信号 [6]。
- 基于正交等位基因重编码的框架在最多 399,943 名 UKB 个体、2,906 个血浆蛋白和 55 个数量性状中分析，发现约三分之一同源基因—蛋白关系表现非线性剂量效应 [7]。
- 在 All of Us、Penn Medicine 与 UCLA 生物库 171,095 人中比较 48 个冠心病 PRS，发现群体预测表现相似的评分在个体层面一致性低（ICC 与 Light κ 低）[8]。
- 现有证据多来自 UKB 及其欧洲裔主体，非欧人群的 pQTL、PRS 与暴露组特征虽有进展，样本量与平台覆盖仍不足以支撑同等强度的结论。

## 1 背景与定义

人群健康与多组学 AI 的边界，首先由“队列规模”与“数据层级”共同划定。它区别于单中心临床预测模型的地方在于：建模对象是生物样本库级别的前瞻性队列或全国登记（UK Biobank 约 50 万参与者、All of Us 拟招募至少 100 万人、FinnGen 22 万余人、丹麦登记自 1965 年以来的纵向医疗数据），输入至少覆盖 EHR 诊断/就诊序列与胚系遗传之一，通常还叠加血浆蛋白组、代谢组或甲基化等分子层 [9][10][11][12]。**这一方向的核心问题不是“能否预测”，而是“在何种人群、何种时间尺度、何种分子层上可复现地预测”**——跨队列复现、跨祖源可移植、个体级校准三者构成其方法学门槛，也解释了为何大量工作报告了内部高性能却难以外推 [8][13]。

演化脉络上，EHR 建模经历了从“概念序列判别”到“生成式轨迹”的转向。BEHRT 与 Med-BERT 把患者历史视为诊断码序列，用 Transformer 与自监督预训练提升未来诊断预测，但仅依赖编码、跨机构泛化未充分验证 [14][15]。Delphi-2M 与 Foresight 把目标从“预测单个标签”改为“生成下一医疗事件”，前者在 UKB 训练、丹麦登记验证，覆盖 1000 多种 ICD-10 顶层诊断 [1]；后者强调自由文本约占 EHR 的 80%，支持多时间分辨率 [2]。**生成式路线的真正贡献在于把“共病结构”与“时间顺序”变成可采样、可反事实模拟的对象**，ALADYNOULLI 以贝叶斯生成框架联合建模纵向诊断、年龄与多基因风险，在三个生物库 n>683,000 上识别 21 个可复制特征 [4]；EHR-MPC 则把生成式数字孪生用于脓毒症治疗规划的推理时控制 [16]。但判别式路线并未退场：All of Us 297,861 人中仅用 12 项常规生物标志物 3 年轨迹特征的 LightGBM 模型 AUROC 达 0.797，显著优于静态汇总的 0.755 [5]，提示**生成式框架的增益究竟来自时间结构建模还是数据规模，目前缺乏同一研究内部的对照**。

第二条脉络是遗传与分子组学的整合，其演化逻辑是从“位点—表型”走向“位点—分子—表型”的链条。UK Biobank 的 pQTL 图谱在 54,219 人、2,923 种蛋白中报告 14,287 个主要遗传关联、81% 为既往未报道 [6]，罕见变异分析补充了常见变异之外的部分 [17]；53,026 人的血浆蛋白组图谱进一步把蛋白与 406 种现患、660 种新发疾病关联，并通过 pQTL 确定 474 个因果蛋白 [18]。**这一层的边界在于：pQTL 提供的是机制锚点，而非因果结论**——因果推断仍依赖 MR 与共定位，且加性常见变异模型之外的成分（非加性剂量效应、结构变异、蛋白比值）已被证明不可忽略 [7][19][20]。代谢组则以更低成本提供可规模化的分子层，三国生物库 700,217 人的 NMR 代谢组评分实现跨库重复 [21]，但其遗传解析深度不及蛋白组，两类组学在风险预测中的相对价值尚无头对头比较。

第三条脉络是“疾病作为异质实体”的分解与共病结构发现。ATM 对 UKB 282,957 人与 All of Us 211,908 人的纵向 EHR 做低秩表示，识别 52 种共病异质性疾病，18 个亚型的 PRS 显著异于同病其他亚型 [22]；ALADYNOULLI 的概率混合框架在 348 种疾病上给出可复制特征与亚型内生物学信号 [4]。**共病结构发现的方法学分歧在于“亚型由什么定义”**：共病轨迹、遗传—表型协方差、分子聚类给出的亚型并不天然可比，跨队列复现率（如 ALADYNOULLI 报告跨队列组成保留中位 80%）因此成为比内部区分度更硬的指标 [4]。与之配套的是表型标准化基础设施：Phecodes 把 ICD 编码映射为高通量病例/对照定义 [23]，ICD-8 到 ICD-10 的单向映射使丹麦半世纪数据可纵向复用 [12]，GWAS Catalog 与 UKB PRS Release 则提供可复用的汇总统计与基准 [24][25]。

贯穿三条脉络的共同约束是人群代表性。UK Biobank 以 40–69 岁、相对健康、欧洲 ancestry 为主 [26][27]；All of Us 虽以 >80% 历史上研究不足群体为目标 [10]，但其内部患者介导与提供者来源两种 EHR 路径在 WGS 覆盖（35.2% vs 83.2%）与关联复制率上存在差异 [28]；多祖源 PRS 在 UKB 欧洲裔中解释 17.6% 的 BMI 变异，而在农村乌干达人中仅 2.2% [29]。**因此本方向的“可复现性”必须同时指跨队列、跨祖源与跨 EHR 采集路径三层**，任何单层验证都不足以支撑人群级结论。这也界定了与相邻方向的接口：与衰老方向的交叉落在组学衰老时钟的人群结局验证（如蛋白组时钟与体力活动、代谢组器官年龄差与 525 个疾病终点）[30][31]；与临床 AI 的分界则在于是否以生物样本库级队列与分子层为必要输入，纯影像或单病种评分改良不属此列。

## 2 方法学


### 2.1 生成式疾病轨迹模型

在纵向电子健康记录（EHR）上学习疾病轨迹，当前主流路线是把患者病史当作序列来生成式建模。Delphi-2M 改造 GPT 架构，在 **UK Biobank** 约 40 万参与者上训练、在丹麦登记数据中验证，词汇覆盖 **1000 多种 ICD-10 顶层诊断**及性别、BMI、吸烟、饮酒和死亡，可同时预测多种疾病的未来发生率并模拟个体终身轨迹 [1]。Foresight 则强调自由文本约占 EHR 的 **80%**，用生成式预训练 Transformer 融合结构化与非结构化数据，覆盖 **18 类 SNOMED 概念**，支持日/周/月不同时间分辨率的预测 [2]。两者都报告了跨队列或跨机构验证，但前者依赖登记编码、后者作者明确其当前形式不宜直接用于临床决策支持 [1][2]。

向更大规模和多模态推进的工作呈现出明显的方法分化。Foresight-England 是 **243M 参数**的 Transformer 解码器，在 NHS England 安全数据环境内从头训练，使用约 **6100 万人**的去标识化纵向 EHR（训练 5490 万、评估 610 万），整合初级/二级诊疗、死亡登记与 COVID-19 数据，并设计了 30 天住院与死亡预测评估框架；但因数据访问暂停，定量结果无法导出，论文只留下分词、架构、训练与评估策略作为方法学模板 [3]。NOAH 走时间感知、任务无关路线，用双向时间整合与变分隐空间原生处理图像、时序、分类和文本，基于 MIMIC 家族 **559M 事件、299,000 患者**训练，支持自回归预测、零样本分类和反事实干预模拟 [32]。LifeLong Digital Twin 则把事件组织为每日健康状态并累积为终身健康上下文，配合 Agent Harness 整合多模态证据，在 **25 个疾病终点**、3 类任务上评估 4 个语言模型，报告疾病识别 F1 从 **0.422** 升至 0.504（Context）和 0.515（Harness），但作者自述缺乏配对不确定性与组件消融、未确立统计显著性 [33]。

除预测未来事件外，生成式轨迹模型也被用于分型与治疗决策。ALADYNOULLI 以贝叶斯生成框架联合建模纵向 EHR 诊断、年龄与多基因风险，采用概率混合而非混合概率的形式处理共病与慢性病，在三个生物库 **n>683,000**、随访 52 年、**348 种疾病**上识别出 **21 个可复制特征**，跨队列组成保留中位 **80%**，基于特征的 GWAS 发现 **151 个**全基因组显著位点，包括单性状分析遗漏的心血管关联 [4]。面向 AD/PD，有工作将诊断前带时间戳的 EHR 标记化后用 Transformer 生成患者嵌入、再以 K-means 聚类，在 CPRD Aurum 与 UK Biobank 两个英国队列、**超过 100,000 名**患者中为每种疾病各识别出 **5 个**可复制亚型，5 年随访显示亚型间死亡与住院预后差异并与基因型关联 [34]。EHR-MPC 把脓毒症治疗优化重构为推理时控制问题：训练生成式 EHR 患者数字孪生预测干预下轨迹，再用模型预测控制在推理时规划治疗，在 Mass General Brigham **8 家医院** ICU 队列上离线策略性能与强化学习基线相当、模拟性能更优，但作者指出仿真评估可能与真实临床存在差距 [16]。

值得注意的是，"生成式"并非这一节的唯一技术路径，判别式与表征学习工作提供了对照与争议点。VaDeSC-EHR 用 Transformer 变分自编码器结合 Weibull 混合生存分布，把风险建模与聚类直接整合，以识别兼具不同诊断轨迹和时间-事件特征的患者亚群，其局限包括聚类数需预设、外部验证有限 [35]。MiGHT-EHR 以异质时序图加图 Transformer 做多任务预测，在 MIMIC-III/IV 四个任务上平均超越 SOTA，但仅在 MIMIC 两个数据集上评估、未提外部验证 [36]。在 All of Us **297,861 人**（11.1% 为病例）中，仅用 12 项常规生物标志物 3 年轨迹特征的 LightGBM 模型 AUROC 达 **0.797**，显著优于静态汇总的 **0.755**（P<0.001），匹配分析为 0.727 对 0.680，并可提前 3–12 个月持续预测（AUROC 0.768–0.740），说明结构化轨迹特征本身已含可观信号，而该研究缺乏外部队列验证 [5]。这些结果与生成式模型报告的高亚型区分度（如 Cohen's d 达 **4.25** [4]）不可直接比较，因为队列、任务与评价指标均不同；真正的争议在于：生成式框架带来的增益究竟来自对时间与共病结构的建模，还是来自更大数据规模与更强表征，目前尚无同一研究内部的对照给出答案。

### 2.2 多组学与遗传整合

多组学与遗传整合的第一条主线，是把遗传关联从“位点—表型”推进到“位点—分子—表型”的链条。UK Biobank 的 pQTL 图谱提供了这一链条的起点：**Pharma Proteomics Project** 在 54,219 名参与者、2,923 种血浆蛋白中报告 **14,287 个主要遗传关联，81% 为既往未报道**，并精细映射出 29,420 个独立信号 [6]。同一队列的罕见变异分析补充了常见变异之外的部分：49,736 人的 exome-wide 分析识别 5,433 个罕见基因型—蛋白关联，其中 81% 未被既往 GWAS 检出，基因水平另有 1,962 个关联 [17]。两项工作共同说明，蛋白组遗传架构中常见与罕见变异贡献的是不同尺度的信号，而非彼此替代。

在 pQTL 之上，整合策略开始分化。一类是把蛋白 QTL 与疾病 GWAS 共定位，推断因果蛋白与药物靶点：53,026 人的血浆蛋白组图谱报告 **168,100 个蛋白—疾病关联**、554,488 个蛋白—性状关联，并通过 pQTL 确定 474 个因果蛋白 [18]。另一类是把多基因评分作为暴露，反向映射到蛋白组：全基因组 2 型糖尿病 PGS 关联 648 个蛋白、其中 617 个复制，分区 PGS 则指向不同生物过程的蛋白 [37]。前者从蛋白出发找疾病，后者从遗传风险出发找蛋白，二者互补但都不能单独确立方向性。

蛋白比值 GWAS 是对单蛋白 pQTL 的方法学修正。利用 UKB Olink 1,463 种蛋白、54,000 余样本，研究复制了 4,248 个 rQTL、覆盖 2,821 个蛋白对，**p-gain 显著的蛋白对富集已知蛋白互作 7.6 倍**，比值 GWAS 较单蛋白 GWAS 新增 24.7% 遗传信号 [20]。与之呼应，cis-by-trans 上位效应分析在 UKB-PPP 数据中识别出以 **ABO 为中心**的稳健互作网络 [38]。这两项结果提示，蛋白组遗传架构中存在单蛋白加性模型捕捉不到的互作与比值结构，但复制队列样本量偏小、功能验证缺失仍是共同短板。

非加性效应的证据进一步挑战了常规加性编码。基于正交等位基因重编码的框架在最多 399,943 名 UKB 个体、2,906 个血浆蛋白和 55 个数量性状中分析，发现**约三分之一同源基因—蛋白关系表现非线性剂量效应**；在 HWE 偏离下该方法保持校准（λGC=0.94），而标准重编码出现膨胀（λGC=78.3）[7]。结构变异层面，长读长参考面板在 54,306 名 UKB 参与者中插补 54,578 个 SV 和 15,826 个 VNTR，二者共同解释蛋白丰度遗传力约 **8.0%**，并鉴定 8,065 个 SV—蛋白与 4,101 个 VNTR—蛋白独立关联 [19]。这些结果说明，加性常见变异模型之外的遗传成分对蛋白组有可观贡献，但各研究采用的变异类别与统计框架不同，贡献比例不宜直接相加或横向比较。

跨祖源比较揭示了 pQTL 的可移植性与局限。ARIC 中 7,213 名欧裔与 1,871 名非裔的 4,657 种蛋白分析显示，欧裔 2,004 个、非裔 1,618 个蛋白有 cis 关联，多数重叠但存在人群特异位点，非裔样本可缩小可信集 [39]。MHC 区的多祖先映射在 UKB 43,762 人与中国慢性病前瞻性研究 3,977 人中鉴定 13 个 cis、606 个 trans MHC 关联，多数跨祖先一致，同时发现东亚人群 EDAR 的祖先富集关联 [40]。性别分层则显示另一维度异质性：**69.1% 的蛋白靶标存在性别差异**，但遗传效应对蛋白的影响跨性别高度相似，仅 103 个 sd-pQTL [41]。三项研究一致指向“多数共享、少数特异”的格局，但特异位点的比例随人群与蛋白平台而变。

代谢组与蛋白组之外，NMR 代谢组提供了低成本、可规模化的分子层。UKB 118,461 人、249 个 NMR 指标的图谱覆盖 700 多种疾病的患病、发病与死亡关联，并在 THL Biobank 3 万余人重复验证 [42]。三国生物库 700,217 人的 NMR 代谢组评分针对 12 种高 DALY 疾病训练 Cox 模型，多数模型纳入超过半数 36 个代谢标志物，并实现跨库重复 [21]。与蛋白组相比，代谢组的遗传解析深度较浅，但其跨库重复性证据更直接；两类组学在风险预测中的相对价值，现有证据尚未在同一研究内做头对头比较。

将分子层纳入疾病预测的代表性工作是 MILTON：在 UKB 484,230 基因组与 3,213 种表型上，用常规临床生物标志物、血浆蛋白和定量性状预测疾病，并识别招募时未诊断的隐性病例以扩充病例队列，扩充后 PheWAS 发现多个基线未显著的新基因—表型关联 [43]。PULSE 则从纵向多模态角度切入，用自监督框架从稀疏常规血检生成代谢组与蛋白组谱，生成代谢组优于所有基准方法，生成蛋白组对 6 种常见病 AUC 达 **0.72–0.83**，接近真实蛋白组数据 [44]。两者都把“分子数据缺失”当作可建模对象而非不可逾越的障碍，但生成数据用于临床决策仍需验证。

多基因评分的跨祖源与个体级可靠性，是遗传整合能否落地的前提。GBMI 比较 P+T 与 PRS-CS，发现 **PRS-CS 总体优于 P+T**，且欧洲 LD 面板预测精度相当或更高，原因在于成员生物库仍以欧洲祖源为主 [45]。All of Us 245,388 全基因组序列联合 UKB 开发 32 个性状的多血统 PRS，发现增加多样性提升部分性状精度，但最大化样本量并非普遍最优，PRS 精度随血统分歧线性下降、多血统训练可减缓 [13]。汉族人群的 TPMI 463,447 人研究则直接证明人群特异 PRS 优于欧洲为主模型 [46]。三项研究在“多祖源训练是否普遍有益”上并不完全一致，差异来自性状遗传结构、样本构成与验证队列。

即便群体水平表现相近，个体层面的评分一致性也可能很差。在 All of Us、Penn Medicine 与 UCLA 生物库 171,095 人中比较 48 个冠心病 PRS，发现群体预测表现相似的评分在个体层面一致性低（ICC 与 Light κ 低）[8]。这一结果对“用 PRS 做个体风险分层”的临床假设构成直接约束，也解释了为何需要把 PRS 与分子标志物、环境暴露联合建模，而非单独依赖遗传评分。

环境暴露与遗传的相对贡献，为多组学整合提供了另一条校准线。UKB 492,567 人的暴露组全关联结合 45,441 人的蛋白组衰老时钟，识别 25 个与死亡和蛋白组衰老独立相关的暴露，并发现暴露组对死亡与 25 种年龄相关病的解释度常高于基因组 [47]。All of Us 10,043 人、5,416 种蛋白的分析则显示，蛋白暴露特征在不同人群和社会经济阶层间基本一致，仅 **<1% 蛋白存在显著跨人群异质性**，BMI 为例外、瘦素关联异质性最高 [48]。前者强调环境解释度，后者强调蛋白暴露特征的可移植性，二者并不矛盾，但提示“遗传 vs 环境”的贡献比例高度依赖所测暴露与结局。

疾病端的遗传解析也在向亚型与过程分解推进。ATM 对 UKB 282,957 人与 All of Us 211,908 人的纵向 EHR 做低秩表示，识别 52 种共病异质性疾病，18 个亚型的 PRS 显著异于同病其他亚型 [22]。冠心病方面，对 526 个显著变异与 78 个相关表型做潜在因子分解，识别 8 个遗传组分并构建过程特异性 pPRS，在 UKB 458,905 人中验证其捕捉传统风险因素之外的生物学特征 [49]。两项工作都把“疾病”拆成异质实体，但前者基于共病轨迹、后者基于遗传—表型协方差，亚型定义的可比性尚不明确。

大队列关联资源的建设降低了整合分析的门槛。GeneATLAS 汇总 452,264 名欧洲裔参与者 118 个连续与 660 个二分类性状、9,113,133 个变异关联 [50]；Pan-UKB 跨祖源荟萃覆盖 7,271 个表型，新发现 14,676 个仅欧洲祖源分析未检出的位点 [51]；BOLT-LMM 在 459K 欧洲样本上使身高统计功效等效 650K 样本、23 性状独立位点增加 84% [52]。这些资源与方法使 pQTL、PheWAS 与 PRS 的交叉整合得以在统一框架内进行，但其欧洲祖源偏倚也被反复标注。

外显子与罕见变异资源构成另一支柱。UKB 454,787 人 WES 在 3,994 个表型上发现 8,865 个显著关联、涉及 564 个基因，**91% 不能由常见变异 LD 解释**、81% 可复制 [53]；281,104 人的外显子 PheWAS 识别 632 个显著 ExWAS 变异并刻画 PTV 携带谱 [54]；394,841 名欧洲裔的 4,529 个表型分析释放了全 summary statistics [55]。FinnGen 176,899 人的隐性关联扫描进一步显示，人群瓶颈导致的纯合子富集可提升隐性致病变异检出，同一变异在杂合与纯合状态下可呈现不同表型 [56]。这些结果共同支持罕见变异在疾病遗传结构中的独立地位，但均以编码区为主、非欧洲分辨率有限。

方法学层面的进展集中在亲缘关系、纵向性状与非加性检验。SPA_GRM 通过回顾性策略控制样本亲缘关系，在 UKB 79 个纵向性状中识别 **7,463 个遗传位点** [57]；BASIL 以 screen-solve-check 迭代求解完整 Lasso 路径，面向 UKB 约 50 万人、>80 万 SNP 的内存瓶颈 [58]。这些工具解决的是“能否在大规模相关样本上得到校准的关联”，而非“关联是否因果”，后者仍依赖 MR、共定位与试验数据。

整合分析的下游应用已延伸到药物靶点与临床风险。脑龄差 GWAS 发现 2 个新位点与 7 个已知位点，整合 eQTL/pQTL 的 MR 与共定位优先 7 个可成药基因、重发现 13 种有临床试验证据的潜在药物 [59]；跨四队列 PheWAS 在最多 697,815 人中检验 19 个候选靶点，证明其可识别多效性并提示疗效或安全性信号 [60]；35 项血尿标志物的遗传分析识别 5,794 个独立位点与 51 个因果关系，多 PRS 模型在 FinnGen 中改善慢性肾病、2 型糖尿病、痛风与酒精性肝硬化的风险分层 [61]。这些应用共享同一逻辑：遗传证据提供方向，分子数据提供机制，临床结局提供验证。

预测模型的改进仍在持续。AB-PRS 框架对预训练 PRS 做自适应提升微调，模拟中各场景 R² 普遍优于基线，并控制 FDR、噪声选择比例 <28% [62]；流体智力表型填充使样本从约 27 万增至超 45.5 万，独立显著常见 SNP 关联由 390 增至 550，罕见变异分析鉴定 26 个显著基因 [63]。两者分别从“模型层”和“表型层”扩充信息量，但都依赖 UKB 的测量结构，外推性尚未验证。

综合来看，多组学与遗传整合的证据呈现出清晰的分层：pQTL 与罕见变异提供分子机制锚点，PRS 与 PheWAS 提供表型广度，MR/共定位提供方向性推断，而跨祖源与个体级一致性构成主要争议面。**多数 pQTL 与蛋白—疾病关联跨人群共享，但人群特异位点、性别差异与非加性效应合计构成不可忽略的剩余部分**；同时，群体水平表现相近的 PRS 在个体层面一致性差，提示整合模型的价值需在个体级校准与外部验证中重新评估。现有证据多来自 UKB 及其欧洲裔主体，非欧人群的 pQTL、PRS 与暴露组特征虽有进展，样本量与平台覆盖仍不足以支撑同等强度的结论。

### 2.3 医学 / EHR 基础模型

早期工作把结构化 EHR 当作“医学概念序列”来建模。**BEHRT** 用 Transformer 处理大规模诊断序列，结合就诊位置、年龄与事件顺序学习患者表示以预测未来诊断，在多种未来诊断预测任务中优于 Deepr、RNN、LSTM、RETAIN 等基线 [14]。**Med-BERT** 沿用 BERT 式自监督预训练思路，先在大规模 ICD 诊断序列上预训练再微调，在糖尿病、心衰等预测任务上优于 BEHRT、G-BERT 及任务内训练模型，且标注样本有限时提升更明显 [15]。两者的共同局限是仅依赖诊断码、跨机构泛化未充分验证 [14][15]。

后续工作转向跨系统迁移与时间事件建模。**GRASP** 用大语言模型把医学编码映射到共享语义空间，再结合 transformer 预测 21 种疾病和全因死亡；在 UKB 391921、FinnGen 253991、Mount Sinai 386755 人的数据上，其平均 ΔC-index 较语言无关模型在芬兰高 **88%**、美国高 **47%**，且 62% 疾病与多基因风险评分的相关性显著更高 [64]。**SurvivEHR** 则以竞争风险时间事件为预训练目标，基于英国初级保健 2300 万患者、**76 亿**编码事件训练生成式 Transformer，风险分层强于基准生存模型并支持低资源微调，但仅限英国数据、外部泛化未验证 [65]。与上述“预测模型”不同，**EHRAgent** 让 LLM 智能体自主生成并执行代码，把多表 EHR 推理形式化为工具使用规划，在三个真实数据集上成功率最高超最强基线 **29.6%**，但依赖代码执行反馈迭代、验证数据集有限 [66]。可见争议在于：语义嵌入能否真正解决跨编码系统迁移 [64]，以及基础模型在单一医疗系统内的高性能能否外推 [65]。

### 2.4 组学衰老时钟与纵向多组学动态

纵向多组学研究的核心发现之一是，群体水平趋势不能替代个体轨迹。在 **335 名女性、8 年随访**的全血基因表达与代谢组分析中，**5,061 个基因和 181 个代谢物**随时间变化，但个体轨迹常偏离群体趋势；这些纵向变化基因具有细胞类型特异性并富集于心血管代谢和神经退行性疾病通路，且受遗传、昼夜节律、季节和污染物影响 [67]。与之呼应，UK Biobank 中 **420,746 人、312 种血液分子**的分析显示，由贝叶斯加性回归树推导的节律紊乱指标基本独立于睡眠，可独立预测 **98 种**未来发病风险并映射到肝脏代谢通路 [68]。这两项工作共同提示，采血时间与个体内波动是纵向组学时钟必须处理的混杂维度，但前者样本限于女性、后者为观察性关联，均未确立因果机制。

在时钟构建层面，方法差异集中在如何利用纵向结构与多器官分解。ARIC 研究基于三次访视的 **4,684 个血浆蛋白**（SomaScan 5K），用 FPCA 提取纵向成分再以 Cox 弹性网训练，构建纵向蛋白衰老指数 LPAI，并在 MESA **3,726 人**中验证，声称其同时捕捉衰老累积负担与变化速度，较单时点蛋白时钟提供额外预测信息 [69]。UK Biobank 的另一项工作则用 **107 个血浆非衍生代谢物**在 **274,247 人**中构建 5 个器官特异性代谢组年龄差 MetBAG，年龄预测平均绝对误差约 **6 年**，独立测试 Pearson r 为 **0.25–0.42**，关联 **525 个**疾病终点 [31]。更细的器官分解见于 **409,206 名**参与者、**14 个器官**的多组学衰老时钟，该研究发现年龄加速与死亡风险是器官生物学的不同维度，具有可分离的表型、分子和遗传结构 [70]。三者对“纵向”的利用程度不同：LPAI 直接建模重复测量轨迹，MetBAG 与 14 器官时钟主要基于单时点横断面数据，因而对变化速度的刻画能力不可直接比较。

干预与临床转化方面，蛋白组时钟显示出可塑性信号。UK Biobank **45,438 名**参与者中，较高体力活动与较低 ProtAgeGap 相关，ProtAgeGap 与 2 型糖尿病风险 **HR=1.06**、高活动交互 **HR=1.05**；在 **26 名男性**的 12 周监督运动研究中，ProtAgeGap 下降相当于 **10 个月**，多数评分蛋白稳定，但 CLEC14A 等随运动变化并与胰岛素敏感性改善相关 [30]。临床指标路线则提供了低成本替代：基于 DFTJ 中国老年人 **36 项**常规临床指标、用限制立方样条 Cox 捕捉 U 型关系构建的生理衰老指数 PAI/ΔPAI，在 DFTJ 与 UK Biobank 中预测死亡、心血管病及 **9 种**慢性病风险 [71]。需注意，运动干预样本量小且以观察性关联为主，PAI 训练主要基于中国老年人、外推受限，这些数字均来自不同队列与设计，不宜跨研究直接比较高低。

## 3 数据与资源

大型前瞻性队列是人群健康多组学 AI 的基础资源。**UK Biobank** 纳入 **50 万** 40–69 岁参与者，2006–2010 年完成基线评估，收集生物样本、影像、加速度计与健康记录链接数据，并预计 20 年随访期间累积糖尿病约 **68,000 例**、心梗与冠心病死亡 47,000 例、卒中 20,000 例、阿尔茨海默病 30,000 例 [9]。其深度表型与基因型资源覆盖约 50 万人，完成基因型质控、单倍型估计和约 **9600 万变异插补**，并通过身高 GWAS 与 HLA-疾病关联复制验证数据质量 [26]。该队列的局限在于参与者相对健康、以欧洲 ancestry 为主 [26]，且 40–69 岁的年龄范围为折中，可能影响暴露与结局的时序 [9]。

测序技术把队列资源从芯片插补推进到全基因组层面。UK Biobank 对 **490,640 人** 完成全基因组测序，平均覆盖 **32.5×**，识别约 **15 亿变异**，较插补芯片增 18.8 倍、较全外显子测序增 >40 倍，其中 93.5% 为非芬兰欧洲 ancestry [72]。同一资源内部，WGS 相对芯片插补和 WES 显著增加可检测变异，尤其改善非编码和罕见变异检测 [72]。FinnGen 则代表隔离人群路线：基于 **224,737 人** 插补基因型和 **1,932 个终点** 做 GWAS 与精细定位，发现芬兰隔离人群富集低频有害等位，可在既往研究充分的疾病中识别新的低频变异关联和可能因果编码变异 [11]；其遗传结构特殊，结果外推至其他人群受限 [11]。综述层面，UK Biobank、All of Us、PRECISE、Biobank Japan 和 NPBBD-Korea 等项目均以 WGS 整合表型、环境与临床信息，但计算基础设施、隐私伦理、临床整合和祖先多样性不足仍是共同挑战 [73]。

多样化与数据来源异质性是美国 All of Us 的核心议题。该计划拟招募至少 **100 万人**，截至 2019 年 7 月已有 >175,000 人贡献生物样本，其中 **>80%** 来自历史上生物医学研究不足群体，34 个站点收集 >112,000 人 EHR [10]；当时仍处招募早期，长期随访和数据完整性待建立 [10]。后续研究比较了患者介导 EHR（PME）与提供者来源 EHR（HPO）两种路径，样本为 19,703 名 PME 与 373,887 名 HPO 参与者；PME 人群更白、更女性、更多保险、随访更长，WGS 覆盖更少（**35.2% vs 83.2%**），两种来源在疾病患病率、表型关联和已知基因型-表型关联复制率上存在差异 [28]。这提示同一队列内部不同 EHR 采集路径不可简单互换，PME 样本量小且人群构成差异大，可能影响泛化和比较 [28]。

表型定义与跨版本编码统一决定多组学数据能否纵向复用。Phecodes 基于 ICD 编码，可快速定义数千种临床有意义疾病和状况的病例/对照状态，最初用于 PheWAS，后扩展到表型风险评分等 EHR 表型方法，但依赖 ICD 编码，可能存在编码误差和表型异质性 [23]。针对 ICD 版本更替，有研究构建了 ICD-8 到 ICD-10 的单向映射，覆盖完整 ICD 及丹麦本地扩展，可连接丹麦自 **1965 年** 以来超半世纪医疗数据，但未提供 ICD-10 回映射 ICD-8 [12]。在真实世界数据侧，爱沙尼亚 **EST-Health-30** 30% 随机人群样本被用于把异质临床事件压缩为以诊断为中心的标准化摘要，形成覆盖 **1000 多个** ICD-10 三位字符诊断类别的全国尺度诊疗模式数字图谱，属回顾性观察研究且仅基于单一国家样本 [74]。

围绕这些资源的分析工具与派生数据层逐步标准化。GWAS Catalog 截至 2024 年 7 月收录 **625,113** 条关联、>15.5K 性状和 >85K 全基因组汇总统计数据集，通过 EFO 性状映射、祖源框架和与 PGS Catalog 互链提升可复用性，但汇总统计标准化不足、非欧祖源仍偏少、依赖作者提交 [24]。UK Biobank 发布覆盖 **28 种疾病和 25 种数量性状** 的 PRS Release 及基准测试软件，广泛基准测试显示其优于 **81 个** 已发表 PRS，并在其他队列验证，但主要基于 UK Biobank 人群，跨种族适用性有限 [25]。工具层面，PHESANT 以规则算法为 UK Biobank 异质表型自动选择统计检验并输出图表，依赖 UKB 变量规则、自动化模型可能不适用于所有复杂表型 [75]；PheWeb 整合 Manhattan、LocusZoom 和 PheWAS 视图供浏览共享大规模结果，但仅可视化与共享、不含统计建模 [76]。

组学数据的技术质控是可用性的前提。针对 UK Biobank 约 **121,657 人** 的 NMR 代谢标志物数据（168 个标志物加 81 个比值，3,169 个盲重复），研究识别了样品制备时间、运输板孔位、光谱仪批次与时间漂移等额外技术变异来源，多数标志物技术因素中位解释 **1.5%**，盲重复中位 CV **4.55%**、R² **0.928**，并发布 ukbnmr R 包；该流程仅覆盖约三分之一 UKB 参与者，且基于已校准浓度而非原始谱 [77]。在应用端，UK Biobank 已被超 **8000 机构** 使用、产出 8000 余篇论文，其遗传证据对应药物获批概率高 2 倍以上，但队列以 40–69 岁为主、存在健康志愿者偏倚，部分神经疾病病例仍有限 [27]。综述指出，组学技术、EHR 普及与 AI 正推动队列从描述性关联转向机制发现、精细风险分层与遗传导向治疗开发，并日益全球化与多样化 [78]。

## 4 应用与结果

在遗传关联发现层面，跨祖源分析显著扩展了可检出的位点集合。对 UK Biobank 多遗传祖源人群开展混合模型关联与跨祖源荟萃分析，覆盖 **7,266 个性状**，发现 **14,676 个仅欧洲祖源分析未发现的显著位点**，并公开汇总统计与解释注意事项[79]。但该工作也指出多数关联仍主要见于欧洲祖源，人群结构带来的假阳性风险需在质控框架下处理[79]。这与多基因评分跨祖源效能的证据相互呼应：基于 GIANT 与 23andMe 最多 **510 万人**构建的多祖源 BMI 评分在 UK Biobank 欧洲裔中解释 **17.6%** 的 BMI 变异，而在其他人群中从东亚裔美国人的 16% 到农村乌干达人的 **2.2%** 不等[29]。同一研究内，儿童期加入评分使 8 岁时解释方差从 11% 升至 21%，5 岁时对 18 岁 BMI 的预测从 22% 升至 35%[29]。可见祖源差异是当前多组学预测的共同约束，而非单一研究的偶然结果。

在冠心病风险预测上，多条证据围绕"遗传与临床因素的时变性"展开，但结论侧重不同。纵向队列分析显示 PRS 的风险比随年龄从 19 岁的 **3.58** 降至 70 岁的 **1.51**，且在 40–45 岁组 PRS 显著优于 PCE，多出 **3.2 倍**适宜性[80]；该研究同时承认两队列年龄范围有限、未涵盖全生命周期[80]。MSGene 则用时间依赖多状态模型整合 EHR、CAD-PRS 与吸烟、降压药、他汀等协变量，按年龄估计 10 个心血管代谢状态间的转移，并与 Framingham 30 年风险和 PCE 10 年风险对照，用于指导他汀启动[81]。蛋白组学路线给出另一维度的增益：在 UK Biobank 中整合传统风险因素、PRS 与 **202 蛋白**风险评分，内部验证 AUC 从 **0.750 升至 0.789**，外部验证从 **0.717 升至 0.762**，且 **9 蛋白面板**即可捕获大部分预测信息[82]。三者方法不同、队列不同，不宜直接比较 AUC 高低，但共同指向"单一时间点、单一因素"框架的不足。

多病共存与心肾代谢轨迹是另一条主线，多状态模型与组学中介分析被反复使用。基于 **330,177 名** UK Biobank 参与者和 **2,911 个血浆蛋白**的研究，用多状态模型刻画从无 CRM 疾病到首发、双重、三重 CRM 疾病的进展，并识别中介蛋白，提示衰老蛋白标志物可用于风险预测和抗衰老干预靶点[83]。代谢组学方面，EPIC-Norfolk 中 **>11,000 人**、**>1,000 代谢物**、**219,415 人年**的分析发现 **640 个**显著代谢物-疾病关联，其中 **420 个（65.5%）**跨至少 2 种 NCD 共享，涉及肝肾功能、脂糖代谢、低度炎症和肠道微生物等通路[84]。在 UK Biobank 代谢组学队列中，MVX 每 1-SD 的 HR 为 **1.213**、MetaboHealth 为 **1.503**，随访 **8,876 人**发病，作者提示代谢负担可补充传统风险因素[85]。美国整合医疗系统 **54,933 名**参与者、**250 个** NMR 代谢标志物的研究则报告加入 NMR 后几乎所有 **9 个** CKM 终点判别能力提升，2 型糖尿病、慢性肾病和代谢功能障碍相关脂肪性肝病增益最大[86]。这些研究设计（横断面、Cox、Fine-Grey、多状态）与人群各异，效应量不可横向比较，但都支持多组学标志物在传统风险因素之外的增量价值。

多疾病联合建模与工具化是较新的方向。UKB-MDRMF 整合基本、生活方式、测量、环境、遗传和影像六类数据，联合建模 **1,560 种疾病**，报告联合预测优于单类别评估，并揭示风险因素-疾病及共病关联，提供交互平台[87]；其局限在于依赖 UKB 人群、缺失值插补及遗传/影像覆盖不全[87]。PheMIME 则整合 VUMC、Mass General Brigham、UK Biobank 三大 EHR 系统的表型组多病共病汇总统计，结合增强版 associationSubgraphs 实现跨系统交互可视化与疾病聚类推断，以精神分裂症为例展示跨系统共病网络[88]。两者一为预测建模、一为可视化知识库，均以"多病"为单位而非单病，但前者未提外部验证、后者依赖已有汇总统计而未提样本量与统计效能细节[87][88]。

药物基因组学与特定疾病的深度表型展示了 EHR 纵向数据的另一类用法。利用 UK Biobank 与 All of Us 的用药与生物标志物纵向数据，对 **10 个**药物-表型对（他汀 LDL-C、二甲双胍 HbA1c、降压药 SBP 等）做常见变异 GWAS 与罕见变异负荷检验并在 All of Us 重复，证明疾病 PRS 可预测药效；作者同时指出用药与检测时点不齐、依从性与适应证混杂、纵向表型分析陷阱多[89]。HFpEF 方面，UKB 多组学（蛋白/代谢/影像/EHR）研究以 **33,480 例** HFpEF 训练监督分类器并在独立多中心 80/20 队列验证，结合无监督聚类、可解释 AI、去混杂与通路分析揭示分子异质性，局限包括 HFpEF 定义依赖多阶段规则、影像/NT-proBNP 缺失者用替代标准、以欧洲人群为主[90]。骨质疏松的可解释蛋白组学框架用 XGBoost 与 SHAP 筛选出 FSHB、ADIPOQ、SOST、COL9A1、CHAD 等标志物，报告其模型优于全蛋白组模型，但外部验证与样本规模细节不明[91]。

蛋白组风险预测的泛化性是上述工作共同的未决问题。在 UK Biobank **53,026 人** Olink 蛋白组数据上训练的 **15 种**疾病预测模型平均 AUC 为 **0.74**（范围 0.56–0.89），较仅用临床因素平均提升 **ΔAUC=0.03**，且不依赖模型架构、简单模型如 L2 表现相当；研究明确指出跨队列泛化性受表型定义影响[92]。这一"增益有限且依赖表型定义"的结论，与前述蛋白组在 CAD 中较大 AUC 提升[82]形成张力——差异可能来自疾病种类、终点定义与验证设计，而非蛋白组本身效能的高低，提示在解读跨研究报告的预测增益时需回到同一研究内部的对照。

## 5 评测、可复现性与争议

在方法层面，大规模电子健康记录生存分析的可复现性挑战首先来自计算实现与推断精度的权衡。针对传统 Cox 模型实现在高维、不规则时点测量和超大规模数据上的不适配，有工作提出**贝叶斯 Cox 回归**结合随机变分推断与似然重加权，使后验分布可因子化到子样本，从而支持**百万级数据点**与数千时变协变量的分析，并在 UK Biobank 心肌梗死应用中给出可行不确定性估计[93]。但其局限也明确：依赖变分近似，精度受子采样影响[93]。这意味着同一研究内部的对照（相对传统 Cox 实现）支持其可扩展性，而近似推断带来的精度损失则是复现与评测中需要单独报告的不确定性来源。

相比之下，面向电子健康记录共病研究的 AI 方法综述仅提供了领域梳理的定位，抽取字段显示其仅有标题级信息、无具体方法细节与结果[94]，因此无法就评测指标、复现流程或争议点展开实质比较。两篇证据在子问题上并不重叠：前者聚焦生存分析推断的可扩展性与不确定性估计，后者聚焦共病研究的 AI 方法版图，尚不构成可直接对照或相互冲突的结论。

## 6 空白与趋势

现有证据在“空白与趋势”上最清楚的一条，是**生成式轨迹模型与多组学/遗传层尚未真正合流**。Delphi-2M 的词汇表只含 ICD-10 顶层诊断、性别、BMI、吸烟、饮酒和死亡，不含蛋白组、代谢组或 PRS [1]；ALADYNOULLI 虽把多基因风险纳入纵向 EHR 联合建模，但分子层仍停留在遗传评分而非蛋白/代谢测量 [4]；PULSE 能从稀疏血检生成代谢组与蛋白组谱并用于疾病预测，却未与疾病轨迹生成模型对接 [44]。**把 pQTL 锚定的因果蛋白、NMR 代谢组与纵向诊断序列放进同一个生成式框架，目前没有看到公开工作**；已有的蛋白组图谱 [18]、代谢组跨库评分 [21] 与轨迹模型各自成立，但缺少同一研究内部的对照来回答“分子层到底带来多少增量”。

第二条趋势是**评测框架开始独立于模型出现，但跨队列可复现性仍是薄弱环节**。Foresight-England 明确把分词、架构、训练、推理与 30 天住院/死亡预测评估框架作为可复用产出，而定量结果因数据访问暂停无法导出 [3]；这与 Delphi-2M 在 UK Biobank 训练、丹麦登记验证的跨队列设计形成对照 [1]。**目前缺少的是统一的、跨生物库的轨迹预测基准**：ATM 在 UK Biobank 与 All of Us 间验证了共病亚型 [22]，ALADYNOULLI 在三个生物库报告特征保留中位 80% [4]，但两者任务定义、疾病词汇与评价指标不同，结果不可横向比较。ICD-8 到 ICD-10 的单向映射 [12] 与 Phecodes 表型工具 [23] 提供了编码统一的底层条件，却尚未被轨迹基础模型的评测协议普遍采纳。

第三条是**个体级可靠性与群体级性能之间的落差正在成为显式议题，但轨迹模型尚未跟进**。48 个冠心病 PRS 在 171,095 人中群体表现相近而个体一致性低 [8]，多祖源 BMI 评分在欧洲裔解释 17.6%、在农村乌干达人群降至 2.2% [29]，说明“平均判别力”不足以支撑个体风险分层。**生成式轨迹模型目前几乎不报告个体级校准或不确定性**：Delphi-2M 报告同时预测 1000 多种疾病的能力 [1]，LifeLong Digital Twin 的作者自述缺乏配对不确定性与组件消融、未确立统计显著性 [33]，EHR-MPC 承认仿真评估可能与真实临床存在差距 [16]。把 PRS 个体一致性检验的思路移植到轨迹预测，是一个明确空白。

第四条是**非加性、结构变异与比值结构正在改写“加性常见变异”的默认假设，但尚未进入疾病预测模型**。约三分之一同源基因—蛋白关系表现非线性剂量效应，标准重编码在 HWE 偏离下 λGC 达 78.3 而正交框架保持 0.94 [7]；SV 与 VNTR 共同解释蛋白丰度遗传力约 8.0% [19]；蛋白比值 GWAS 较单蛋白新增 24.7% 遗传信号、p-gain 显著蛋白对富集已知互作 7.6 倍 [20]。这些结果都指向单蛋白加性编码之外的可观剩余，**但现有 PRS 与多组学风险评分仍以加性常见变异为主**，非加性效应与 SV/VNTR 如何进入人群级预测，尚无公开的方法学方案。

第五条是**环境暴露与蛋白暴露特征的可移植性证据开始出现，提示“遗传 vs 环境”的贡献比例依赖测量层**。UKB 492,567 人的暴露组分析发现暴露组对死亡与 25 种年龄相关病的解释度常高于基因组 [47]；All of Us 10,043 人、5,416 种蛋白的分析则显示仅 <1% 蛋白存在显著跨人群异质性，BMI 为例外 [48]。**两者并不冲突，但共同指向一个没人系统做的方向：把暴露组、蛋白组与遗传放在同一纵向框架里做贡献分解**，而不是各自与结局单独关联。现有轨迹模型 [1][2] 的输入变量表里，环境暴露几乎缺席。

第六条是**资源与工具层已具备，但“生成式 + 多组学 + 跨祖源”三者叠加的工作仍属空白**。UK Biobank 完成 490,640 人 WGS、平均覆盖 32.5×、识别约 15 亿变异 [72]，Pan-UKB 跨祖源荟萃覆盖 7,266 个性状、新发现 14,676 个仅欧洲祖源未检出的位点 [79]，All of Us 的 PME 与 HPO 两种 EHR 路径在 WGS 覆盖（35.2% vs 83.2%）与关联复制率上存在差异 [28]。**数据规模与祖源多样性已不再是唯一瓶颈，瓶颈在于模型侧**：现有生成式轨迹模型多在单一或双队列上训练验证 [1][3]，尚未见在 UK Biobank、All of Us、FinnGen 三类祖源与编码体系上同时做零样本迁移的公开报告。综述层面已指出队列正从描述性关联转向机制发现与精细风险分层 [78]，但这一转向在生成式模型上的落地证据仍然稀薄。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 生成式疾病轨迹模型 | **朝阳** | [2] 把 GPT 式生成预训练用于患者时间线建模，[1] 用生成式 transformer 学习疾病自然史，两篇均为近两年高影响工作，说明范式已立但方法仍在快速分化；[35] 与 [4] 分别从纵向生存聚类和贝叶斯纵向 EHR+遗传切入，显示表示学习与概率框架尚未收敛，属典型「近两年爆发、方法未收敛」。 |
| 2.2 多组学与遗传整合 | **成熟** | [6] 的 UKB 血浆蛋白组-遗传-健康关联图谱与 [61] 的 35 项血尿标志物遗传学已把 pQTL/生物标志物遗传架构做成标准范式；[52] 的混合模型关联与 [53] 的外显子组分析表明统计方法与大样本流程已收敛，新工作多为增量扩展（如 [79] 的 Pan-UKB GWAS 精细化）。 |
| 2.3 医学 / EHR 基础模型 | **朝阳（偏早期）** | [15] Med-BERT 与 [14] BEHRT 奠定结构化 EHR 预训练范式，但雷达样本仅 5 篇、CNS 占比 0，[66] 与 [64] 显示近期才转向 LLM/代码推理与跨机构迁移，方法远未收敛，属爆发前夜。 |
| 2.4 组学衰老时钟与纵向多组学动态 | **萌芽→朝阳** | [31] 的多器官代谢组生物学年龄与 [71] 的常规临床标志物生理年龄验证，说明「组学时钟→人群结局」路线刚被系统验证；[69] 的纵向蛋白组衰老指数与 [30] 的运动逆转蛋白组衰老，显示纵向动态与干预可逆性才起步，样本少、引用低，方法未定。 |
| 3 数据与资源 | **成熟** | [9] 与 [26] 确立 UKB 作为开放资源与深度表型标准，[11] FinnGen 与 [10] All of Us 补齐隔离人群与多样性队列，资源层已稳定，后续工作主要是接入与基准化。 |
| 4 应用与结果 | **朝阳** | [95] 用疾病轨迹深度学习预测胰腺癌风险、[84] 用血浆代谢物刻画非传染性共病通路，显示应用层近两年高影响产出密集；[29] 的 BMI 多基因预测贯穿生命历程与 [79] 的 Pan-UKB 分析说明应用正从单病种走向全表型与纵向，但落地验证仍分散。 |
| 5 评测、可复现性与争议 | **证据不足** | 雷达样本仅 2 篇：[93] 是大规模 EHR 贝叶斯 Cox 推断方法，[94] 是共病 AI 方法综述，均非系统性基准/复现研究，无法据此判定阶段。 |

**整体判断**：这个方向整体处于**朝阳期偏中后段**——资源层（UKB/FinnGen/All of Us）已成熟，多组学-遗传整合（2.2）方法收敛进入增量，而生成式轨迹（2.1）、EHR 基础模型（2.3）、组学衰老时钟（2.4）三块近两年才爆发且方法未定，雷达样本中 2025–2026 年证据占 **48%**、CNS 占比 **32%**，说明高影响窗口仍在打开。窗口期判断：**生成式轨迹与 EHR 基础模型的「方法定义权」窗口约还有 1–2 年**（一旦基准与评测框架（第 5 节）补齐，方法会迅速收敛为增量）；组学衰老时钟的纵向动态与干预验证窗口稍长，约 **2–3 年**。最大不确定性是**跨队列可复现性与评测缺失**——第 5 节雷达样本仅 2 篇且无系统基准，意味着当前大量高影响结果尚未被独立复现，方法优劣难判，谁先做出可信基准谁就占据下一阶段话语权。

**接下来怎么做**：
1. **把「生成式轨迹 + 多组学条件化」作为主切入点**：用 UKB 的 EHR 诊断时间序列 [1] 作为骨架，条件化加入血浆蛋白组 [6] 与遗传 [4]，做「给定组学状态下的疾病轨迹生成」。现在做是因为轨迹生成范式刚立、尚未有人系统接入蛋白组条件，方法定义权仍开放；产出可对接你的多模态建模能力。
2. **用公共数据做「跨队列复现」demo，抢占评测空白**：在 UKB 训练、FinnGen [11] 与 All of Us [10] 上复现轨迹/风险模型，产出可复现基准。第 5 节证据不足正是机会——[94] 只是综述，尚无系统基准；这类工作方法门槛低、影响力高，且直接服务你的公共数据 demo 合作。
3. **把衰老时钟接到人群结局上做纵向验证**：以 [31] 的多器官代谢组年龄与 [69] 的纵向蛋白组衰老指数为基线，在 UKB 纵向样本上验证其对死亡/多病共病的预测增益，并检验干预可逆性 [30]。现在做是因为纵向动态与可逆性才刚起步（2.4 雷达样本仅 7 篇、中位引用 3），与你的衰老方向直接交叉，易出差异化结果。
4. **与类器官 + 多组学合作项目对接，做「人群先验 → 体外验证」闭环**：用人群 pQTL/蛋白组关联 [6] 筛出候选蛋白/通路，在类器官多组学中做扰动验证，把人群关联转成机制假设。现在做是因为 2.2 已成熟、候选清单现成，缺的是体外验证环节，你的合作项目正好补位，且能避免在成熟方向做纯增量。
5. **避开纯单病种评分改良，转向共病结构 + 多模态**：以 [84] 的代谢物-共病通路与 [95] 的轨迹风险为参照，做多病共病结构的生成式发现而非单病种 AUC 提升。理由：单病种评分改良已被排除标准判为无方法学新意，而共病结构 + 生成式建模仍在朝阳段，且能复用你的单细胞/多模态建模栈。

## 参考文献

1. Learning the natural history of human disease with generative transformers.. Nature 2025. https://doi.org/10.1038/s41586-025-09529-3
2. Foresight—a generative pretrained transformer for modelling of patient timelines using electronic health records: a retrospective modelling study. The Lancet Digital Health 2024. https://doi.org/10.1016/s2589-7500(24)00025-6
3. Foresight-England: Development of a National-Scale Generative AI Model of Electronic Health Records for Medical Event Prediction across the COVID-19 Pandemic.  2026. https://arxiv.org/abs/2608.16273
4. A Bayesian framework for longitudinal EHR and genetic discovery. Nature 2026. https://doi.org/10.1038/s41586-026-10780-5
5. Predicting Early Functional Decline from Longitudinal Laboratory and Vital Sign Trajectories: A Large-Scale Study Using the All of Us Research Program.  2026. https://arxiv.org/abs/2608.21589
6. Plasma proteomic associations with genetics and health in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06592-6
7. Deviations from genetic additivity driven by rare variants at biobank scale.. Nature communications . https://doi.org/10.1038/s41467-026-76151-w
8. Evaluating Performance and Agreement of Coronary Heart Disease Polygenic Risk Scores.. JAMA 2025. https://doi.org/10.1001/jama.2024.23784
9. UK Biobank: An Open Access Resource for Identifying the Causes of a Wide Range of Complex Diseases of Middle and Old Age. PLoS Medicine 2015. https://doi.org/10.1371/journal.pmed.1001779
10. The “All of Us” Research Program. New England Journal of Medicine 2019. https://doi.org/10.1056/NEJMsr1809937
11. FinnGen provides genetic insights from a well-phenotyped isolated population. Nature 2023. https://doi.org/10.1038/s41586-022-05473-8
12. A unidirectional mapping of ICD-8 to ICD-10 codes, for harmonized longitudinal analysis of diseases. European Journal of Epidemiology 2023. https://doi.org/10.1007/s10654-023-01027-y
13. All of Us diversity and scale yield context-dependent improvements in polygenic prediction.. Nature Genetics 2026. https://doi.org/10.1038/s41588-026-02734-4
14. BEHRT: Transformer for Electronic Health Records. Scientific Reports 2019. https://doi.org/10.1038/s41598-020-62922-y
15. Med-BERT: pretrained contextualized embeddings on large-scale structured electronic health records for disease prediction. npj Digital Medicine 2020. https://doi.org/10.1038/s41746-021-00455-y
16. EHR-MPC: Inference-Time Control for Sepsis Treatment with Generative Patient Digital Twins. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.08793
17. Rare variant associations with plasma protein levels in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06547-x
18. Atlas of the plasma proteome in health and disease in 53,026 adults.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.045
19. A proteome atlas of structural variation and VNTR effects on complex traits and diseases.  . https://doi.org/10.64898/2026.09.26.26364064
20. Genetic associations with ratios between protein levels detect new pQTLs and reveal protein-protein interactions. bioRxiv 2023. https://doi.org/10.1016/j.xgen.2024.100506
21. Metabolomic and genomic prediction of common diseases in 700,217 participants in three national biobanks.. Nature communications 2024. https://doi.org/10.1038/s41467-024-54357-0
22. Age-dependent topic modelling of comorbidities in UK Biobank identifies disease subtypes with differential genetic risk. Nature Genetics 2023. https://doi.org/10.1038/s41588-023-01522-8
23. Using Phecodes for Research with the Electronic Health Record: From PheWAS to PheRS. Annual Review of Biomedical Data Science 2021. https://doi.org/10.1146/annurev-biodatasci-122320-112352
24. The NHGRI-EBI GWAS Catalog: standards for reusability, sustainability and diversity.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1070
25. UK Biobank release and systematic evaluation of optimised polygenic risk scores for 53 diseases and quantitative traits. medRxiv 2022. https://doi.org/10.1101/2022.06.16.22276246
26. The UK Biobank resource with deep phenotyping and genomic data. Nature 2018. https://doi.org/10.1038/s41586-018-0579-z
27. UK Biobank-A Unique Resource for Discovery and Translation Research on Genetics and Neurologic Disease.. Neurology. Genetics 2025. https://doi.org/10.1212/nxg.0000000000200226
28. Robust replication of associations across patient-mediated and provider-sourced EHR data in the All of Us research program. npj Digital Public Health 2026. https://doi.org/10.1038/s44482-026-00032-8
29. Polygenic prediction of body mass index and obesity through the life course and across ancestries.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03827-z
30. Reversal of proteomic aging with exercise-results from the UK biobank and a 12-week intervention study.. npj aging 2025. https://doi.org/10.1038/s41514-025-00318-w
31. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
32. NOAH: Learning the Full Patient Journey. A Longitudinal Multimodal Time-Aware Model for Representation and Forecasting.  2026. https://arxiv.org/abs/2609.09140
33. LifeLong Digital Twin: A Unified Modeling Paradigm and Agent Harness for Event-Driven Lifelong Health State Trajectories.  . https://arxiv.org/abs/2610.05566
34. Subtyping Alzheimer's disease and Parkinson's disease using longitudinal electronic health records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01085-3
35. Deep representation learning for clustering longitudinal survival data from electronic health records.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56625-z
36. MiGHT-EHR: A Multi-task Graph Transformer for Heterogeneous Temporal Electronic Health Records.  2026. https://arxiv.org/abs/2608.06430
37. Identification of plasma proteomic markers underlying polygenic risk of type 2 diabetes and related comorbidities.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56695-z
38. Robust cis-by-trans epistasis in the human plasma proteome highlights an ABO-centered interaction network.. American journal of human genetics . https://doi.org/10.1016/j.ajhg.2026.09.003
39. Plasma proteome analyses in individuals of European and African ancestry identify cis-pQTLs and models for proteome-wide association studies. Nature Genetics 2022. https://doi.org/10.1038/s41588-022-01051-w
40. Multi-ancestry MHC-pQTL mapping reveals disease-linked HLA protein networks and shared genetic architecture.  . https://doi.org/10.21203/rs.3.rs-10956233/v1
41. Sex differences in the genetic regulation of the human plasma proteome.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59034-4
42. Atlas of plasma NMR biomarkers for health and disease in 118,461 individuals from the UK Biobank. Nature Communications 2023. https://doi.org/10.1038/s41467-023-36231-7
43. Disease prediction with multi-omics and biomarkers empowers case–control genetic discoveries in the UK Biobank. Nature Genetics 2024. https://doi.org/10.1038/s41588-024-01898-1
44. Longitudinal alignments and syntheses of multimodal clinical data for personalized medicine with the PULSE framework. Nature Computational Science 2026. https://doi.org/10.1038/s43588-026-01026-5
45. Global biobank analyses provide lessons for computing polygenic risk scores across diverse cohorts. medRxiv 2021. https://doi.org/10.1101/2021.11.18.21266545
46. Population-specific polygenic risk scores for people of Han Chinese ancestry.. Nature 2025. https://doi.org/10.1038/s41586-025-09350-y
47. Integrating the environmental and genetic architectures of aging and mortality.. Nature medicine 2025. https://doi.org/10.1038/s41591-024-03483-9
48. Proteomic Signatures Capture Environmental Exposures Across Diverse Populations.  . https://doi.org/10.64898/2026.10.06.26364311
49. Decomposing polygenic risk of coronary artery disease into distinct biological processes.  . https://doi.org/10.64898/2026.10.08.26365088
50. An atlas of genetic associations in UK Biobank. Nature Genetics 2017. https://doi.org/10.1038/s41588-018-0248-z
51. Pan-UK Biobank GWAS improves discovery, analysis of genetic architecture, and resolution into ancestry-enriched effects. medRxiv 2024. https://doi.org/10.1101/2024.03.13.24303864
52. Mixed model association for biobank-scale data sets. Nature Genetics 2018. https://doi.org/10.1038/s41588-018-0144-6
53. Exome sequencing and analysis of 454,787 UK Biobank participants. Nature 2021. https://doi.org/10.1038/s41586-021-04103-z
54. Rare variant contribution to human disease in 281,104 UK Biobank exomes. Nature 2021. https://doi.org/10.1038/s41586-021-03855-y
55. Systematic single-variant and gene-based association testing of thousands of phenotypes in 394,841 UK Biobank exomes. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100168
56. Mono- and biallelic variant effects on disease at biobank scale. Nature 2023. https://doi.org/10.1038/s41586-022-05420-7
57. SPA<sub>GRM</sub>: effectively controlling for sample relatedness in large-scale genome-wide association studies of longitudinal traits.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56669-1
58. A fast and scalable framework for large-scale and ultrahigh-dimensional sparse regression with application to the UK Biobank. bioRxiv 2019. https://doi.org/10.1371/journal.pgen.1009141
59. Genetically supported targets and drug repurposing for brain aging: A systematic study in the UK Biobank.. Science advances 2025. https://doi.org/10.1126/sciadv.adr3757
60. Phenome-wide association studies across large population cohorts support drug target validation. Nature Communications 2018. https://doi.org/10.1038/s41467-018-06540-3
61. Genetics of 35 blood and urine biomarkers in the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-020-00757-z
62. A pre-train and fine-tune framework for adaptive boosting of pre-trained polygenic risk scores.. Nature communications . https://doi.org/10.1038/s41467-026-77128-5
63. Imputation of fluid intelligence scores reduces ascertainment bias and increases power for analyses of common and rare variants.. Nature genetics . https://doi.org/10.1038/s41588-026-02787-5
64. Large language models improve transferability of electronic health record-based predictions across countries and coding systems.. NPJ digital medicine 2026. https://doi.org/10.1038/s41746-026-02363-5
65. SurvivEHR: a competing risks, time-to-event foundation model for multiple long-term conditions from primary care electronic health records.  2025. https://doi.org/10.1101/2025.08.04.25332916
66. EHRAgent: Code Empowers Large Language Models for Few-shot Complex Tabular Reasoning on Electronic Health Records.. Proceedings of the Conference on Empirical Methods in Natural Language Processing. Conference on Empirical Methods in Natural Language Processing 2024. https://doi.org/10.18653/v1/2024.emnlp-main.1245
67. Longitudinal dynamics of gene expression and metabolomics in an aging population cohort.. Science 2026. https://doi.org/10.1126/science.aed6452
68. Molecular Circadian Disturbance in Human Blood Independently Predicts Multi-Disease Risk and Maps to Hepatic metabolism Pathways.  . https://doi.org/10.21203/rs.3.rs-11120748/v1
69. A Novel Longitudinal Proteomic Aging Index Predicts Mortality, Multimorbidity, and Frailty in Older Adults.. Aging cell 2025. https://doi.org/10.1111/acel.70317
70. Age Acceleration and Mortality Risk Constitute Distinct Dimensions of Organ Aging.  . https://doi.org/10.21203/rs.3.rs-10881849/v1
71. Estimation of physiological aging based on routine clinical biomarkers: a prospective cohort study in elderly Chinese and the UK Biobank.. BMC medicine 2024. https://doi.org/10.1186/s12916-024-03769-2
72. Whole-genome sequencing of 490,640 UK Biobank participants.. Nature 2025. https://doi.org/10.1038/s41586-025-09272-9
73. Lessons from national biobank projects utilizing whole-genome sequencing for population-scale genomics.. Genomics & informatics 2025. https://doi.org/10.1186/s44342-025-00040-9
74. A national-scale digital atlas of recorded care patterns across more than 1000 diagnostic categories using real-world health data: a retrospective observational study.  . https://doi.org/10.64898/2026.09.16.26363186
75. Software Application Profile: PHESANT: a tool for performing automated phenome scans in UK Biobank. International Journal of Epidemiology 2017. https://doi.org/10.1093/ije/dyx204
76. Exploring and visualizing large-scale genetic associations using PheWeb. Nature Genetics 2020. https://doi.org/10.1038/s41588-020-0622-5
77. Quality control and removal of technical variation of NMR metabolic biomarker data in ~120,000 UK Biobank participants. Scientific Data 2021. https://doi.org/10.1038/s41597-023-01949-y
78. Trends in large-scale human population cohorts.. Trends in Genetics 2026. https://doi.org/10.1016/j.tig.2026.08.002
79. Pan-UK Biobank genome-wide association analyses enhance discovery and resolution of ancestry-enriched effects.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02335-7
80. Dynamic Importance of Genomic and Clinical Risk for Coronary Artery Disease Over the Life Course. medRxiv 2023. https://doi.org/10.1101/2023.11.03.23298055
81. MSGene: a multistate model using genetic risk and the electronic health record applied to lifetime risk of coronary artery disease. Nature Communications 2024. https://doi.org/10.1038/s41467-024-49296-9
82. Machine Learning‐Driven Prediction of Coronary Artery Disease Risk Based on UK Biobank Plasma Proteomics. Journal of the American Heart Association : Cardiovascular and Cerebrovascular Disease 2026. https://doi.org/10.1161/JAHA.125.047248
83. Proteomics mediates the effects of biological aging on the progression of cardio-renal-metabolic comorbidity: a UK biobank cohort study.. Cardiovascular diabetology 2025. https://doi.org/10.1186/s12933-025-03035-6
84. Plasma metabolites to profile pathways in noncommunicable disease multimorbidity. Nature Medicine 2021. https://doi.org/10.1038/s41591-021-01266-0
85. MetaboHealth and Metabolic Vulnerability Index as Risk Factors for Cardio-Renal-Metabolic Multimorbidity: A Large-Scale Prospective Cohort Study.. Diabetes, obesity and metabolism 2026. https://doi.org/10.1111/dom.71112
86. NMR metabolomics for cardiovascular-kidney-metabolic risk stratification in an integrated healthcare system.  . https://doi.org/10.64898/2026.10.01.26364322
87. UKB-MDRMF: a multi-disease risk and multimorbidity framework based on UK biobank data.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58724-3
88. PheMIME: an interactive web app and knowledge base for phenome-wide, multi-institutional multimorbidity analysis.. Journal of the American Medical Informatics Association : JAMIA 2024. https://doi.org/10.1093/jamia/ocae182
89. Leveraging large-scale biobank EHRs to enhance pharmacogenetics of cardiometabolic disease medications.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58152-3
90. Deep phenotyping of heart failure with preserved ejection fraction through multi-omics integration.. European journal of heart failure 2025. https://doi.org/10.1002/ejhf.70041
91. Explainable Plasma Proteomics–Based Machine Learning for Osteoporosis Diagnosis, Prognosis, and Protein Biomarker Discovery in the UK Biobank. The FASEB Journal 2026. https://doi.org/10.1096/fj.202600647R
92. Generalizability of proteomic risk prediction across biobanks reveals dependence on phenotype definitions.  . https://doi.org/10.64898/2026.10.01.26364038
93. Bayesian Cox regression for large-scale inference with applications to electronic health records. Annals of Applied Statistics 2021. https://doi.org/10.1214/22-aoas1658
94. From data to knowledge: artificial intelligence methods for studying comorbidity in electronic health records. The European Physical Journal Special Topics 2026. https://doi.org/10.1140/epjs/s11734-026-02571-w
95. A deep learning algorithm to predict risk of pancreatic cancer from disease trajectories. Nature Medicine 2023. https://doi.org/10.1038/s41591-023-02332-5
96. Polygenic Prediction of Peripheral Artery Disease and Major Adverse Limb Events.. JAMA cardiology 2025. https://doi.org/10.1001/jamacardio.2025.1182
97. An atlas of polygenic risk score associations to highlight putative causal relationships across the human phenome. bioRxiv 2018. https://doi.org/10.7554/eLife.43657
98. Global Biobank Meta-analysis Initiative: Powering genetic discovery across human disease. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100192
99. Exome sequencing and characterization of 49,960 individuals in the UK Biobank. Nature 2020. https://doi.org/10.1038/s41586-020-2853-0
100. Advancing human genetics research and drug discovery through exome sequencing of the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-021-00885-0
101. Comparative analysis of the Mexico City Prospective Study and the UK Biobank identifies ancestry-specific effects on clonal hematopoiesis.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02085-6
102. Phenome-wide Burden of Copy Number Variation in the UK Biobank.. American Journal of Human Genetics 2019. https://doi.org/10.1016/j.ajhg.2019.07.001
103. Components of genetic associations across 2,138 phenotypes in the UK Biobank highlight adipocyte biology. Nature Communications 2019. https://doi.org/10.1038/s41467-019-11953-9
104. GWAS of extended prescription analgesic use identifies genetic loci in chronic pain.. Nature communications 2026. https://doi.org/10.1038/s41467-026-71434-8
105. Phenome-wide and proteomic analysis of APOE alleles across different ancestries in the All of Us Research Program.  . https://doi.org/10.64898/2026.09.26.26364080
