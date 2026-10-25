# 人群健康与多组学 AI · 方向背景报告

证据 111 篇 · 覆盖度 0.83 · 第 12 轮 · 更新 2026-10-25 · 数字核验删句 2

## 本次变更

- 新增 [12] Choice of phenotype scale is critical in biobank-based G × E tests.
- 新增 [87] Large-scale plasma proteomic profiling enhances prediction of heart failure among hypertensive individuals: prospective insights from the UK Biobank.
- 新增 [16] Genomic foundation models do not yet boost common variant discovery beyond standard functional annotations
- 新增 [76] Functional architecture of rare protein coding variation across 786,871 exomes
- 新增 [74] Multimodal mediators connecting APOE4 to dementia
- 新增 [63] Genome-wide detection of genotype-environment interactions at biobank scale with fastGxE.

## 摘要（TL;DR）

- Foresight 基于生成式预训练 Transformer，整合结构化数据与约占 80% 的自由文本，覆盖 18 类 SNOMED 概念并支持日/周/月不同时间分辨率，但作者明确其当前形式不宜直接用于临床决策支持 [1]。
- ALADYNOULLI 以贝叶斯生成路线在 3 个生物库、n>683,000、随访 52 年、348 种疾病上识别出 21 个可复制特征，跨队列组成保留中位 80%，亚型 Cohen's d 达 4.25，基于特征的 GWAS 发现 151 个全基因组显著位点 [2]。
- Foresight-England 报告首个国家级 EHR 生成式基础模型，243M 参数 Transformer 解码器使用约 6100 万人去标识化纵向 EHR（训练 5490 万、评估 610 万），但因数据访问暂停，定量结果无法导出，论文仅作为方法学模板 [3]。
- NOAH 采用双向时间整合与变分隐空间，在 MIMIC 家族 559M 事件、299,000 患者上原生处理图像、时序、分类与文本记录，支持自回归预测、零样本分类与反事实干预模拟 [4]。
- LifeLong Digital Twin 在 25 个疾病终点、3 类任务、4 个语言模型上，16 个模型-读出比较全部优于无 Context/Harness 的基线，疾病识别 F1 从 0.422 升至 0.504（Context）、0.515（Harness），但作者自陈缺乏配对不确定性、疾病支持计数与组件消融，未确立统计显著性 [5]。
- EHR-MPC 把脓毒症治疗优化重构为推理时控制问题，在 Mass General Brigham 8 家医院 ICU 脓毒症队列上离线策略性能与强化学习基线相当、模拟性能更优，但作者指出依赖离线数据、仿真评估可能与真实临床存在差距 [6]。
- AD/PD 亚型研究在 CPRD Aurum 与 UK Biobank 两个英国队列、超过 100,000 名患者中为每种疾病识别出 5 个可复现亚型，5 年随访显示亚型间死亡与住院预后差异并与基因型关联，局限在于依赖 EHR 记录质量、外部验证仅限 UK Biobank、生物学机制仍待验证 [7]。
- 功能衰退预警基于 All of Us 297,861 人（11.1% 为病例）、12 项生物标志物 3 年轨迹特征训练 LightGBM，AUROC 0.797 显著优于静态汇总的 0.755（P<0.001），但仅用常规实验室数据且缺乏外部队列验证 [8]。
- Pharma Proteomics Project 对 54,219 名参与者、2,923 种蛋白开展定位，发现 14,287 个主要遗传关联，81% 为既往未报道，并精细映射出 29,420 个独立信号 [9]。
- 基于 53,026 人、2,920 种蛋白的图谱报告 168,100 个蛋白—疾病关联和 554,488 个蛋白—性状关联，183 种疾病判别 AUC>0.80，并通过 pQTL 确定 474 个因果蛋白 [10]。
- 正交等位基因重编码框架在最多 399,943 名 UKB 个体、2,906 个血浆蛋白和 55 个数量性状上发现约三分之一同源基因—蛋白关系呈非线性剂量效应，且标准重编码在 HWE 偏离下膨胀（λGC=78.3）而新方法保持校准（λGC=0.94）[11]。
- 表型尺度问题提示许多 biobank GWAS 检出的 G×E 信号可能只是另一尺度上的加性效应，在 UKB 32 个表型中幂变换可解释 45% 的多基因评分 G×E 信号 [12]。
- 泛 UKB 跨祖源荟萃在 7,271 个表型上新发现 14,676 个仅欧洲祖源分析未检出的位点 [13]。
- 在 AOU、PMBB 与 UCLA 三个生物库、171,095 人中比较 48 个冠心病 PRS，发现群体水平表现相似的评分在个体层面一致性差（ICC 与 Light κ 低）[14]。
- 性别分层分析显示 69.1% 的蛋白存在性别差异，但遗传效应对蛋白的影响跨性别高度相似，仅 103 个 sd-pQTL [15]。
- 在 27 个 UKB 性状上，AlphaGenome、Borzoi、GPN-Star 三种基因组基础模型衍生的注释均未超越 baselineLD，中位增益分别为 1.8%、3.8% 对 5.1%，GPN-Star 甚至减少位点发现 [16]。
- GRASP 用大语言模型将医学编码映射到共享语义空间并结合 transformer 预测，在 UKB 391921 人、FinnGen 253991 人、Mount Sinai 386755 人上预测 21 种疾病和全因死亡，其平均 ΔC-index 较语言无关模型在芬兰高 88%、美国高 47% [17]。
- 在 335 名女性、8 年随访的全血基因表达与代谢组数据中，5,061 个基因和 181 个代谢物随时间变化，且个体轨迹常偏离群体水平趋势，变化受遗传、昼夜节律、季节和污染物影响 [18]。
- UK Biobank 274,247 人的 107 个血浆非衍生代谢物被用于开发 5 个器官特异性代谢组生物年龄 MetBAG，年龄预测平均绝对误差约 6 年，独立测试 Pearson r 为 0.25–0.42，并关联 525 个疾病终点、预测 14 类疾病与死亡风险 [19]。
- UK Biobank 45,438 人血浆蛋白分析显示体力活动越高 ProtAgeGap 越低，ProtAgeGap 与 2 型糖尿病风险相关（HR=1.06），高活动交互 HR=1.05；在 26 名男性的 12 周监督运动研究中，ProtAgeGap 下降相当于 10 个月 [20]。
- UK Biobank 420,746 人、312 种血液学、生化与代谢分子与采血时间关联，用贝叶斯加性回归树推导相位偏移与节律紊乱两个正交指标，节律紊乱基本独立于睡眠，可独立预测 98 种未来发病风险并映射到肝脏代谢通路 [21]。
- UK Biobank 在2006–2010年间招募50万名40–69岁参与者，预计20年随访可累积糖尿病约68,000例、心梗与冠心病死亡47,000例、卒中20,000例、阿尔茨海默病30,000例等事件量 [22]。
- UK Biobank 对490,640人开展全基因组测序，平均覆盖32.5×，识别约15亿变异，较插补芯片增18.8倍、较全外显子测序增>40倍，其中93.5%为芬兰以外的欧洲 ancestry [23]。
- All of Us 计划在美国招募至少100万人；截至2019年7月，超过175,000人贡献生物样本，其中>80%来自历史上研究不足群体，34个站点收集了>112,000人的EHR数据 [24]。
- All of Us 的EHR比较研究纳入393,590名参与者（患者介导EHR 19,703人、提供者来源EHR 373,887人），发现患者介导来源人群更白、更女性、更多保险、随访更长，而WGS覆盖更少（35.2% vs 83.2%）[25]。
- FinnGen R5 整合9个芬兰生物库与全国健康登记，基于224,737人插补基因型和1,932个终点开展GWAS与精细定位，发现隔离人群富集低频有害等位（0.1%≤MAF<5%）[26]。
- GWAS Catalog 截至2024年7月收录625,113条关联、>15.5K性状和>85K全基因组汇总统计数据集，但汇总统计标准化不足、非欧祖源偏少且依赖作者提交 [27]。
- UK Biobank 发布覆盖28种疾病和25种数量性状的PRS Release及基准测试软件，广泛基准测试中优于81个已发表PRS，但主要基于UK Biobank人群、跨种族适用性有限 [28]。
- 基于 GIANT 与 23andMe 最多 510 万人构建的多祖源 BMI 评分在欧洲裔 UK Biobank 参与者中解释 17.6% 的 BMI 变异，其他人群从 16%（东亚裔美国人）到 2.2%（农村乌干达人）不等 [29]。
- 纵向分析在 FOS 3,588 人与 UK Biobank 327,837 人中显示 PRS 的风险比随年龄下降（19 岁 3.58 降至 70 岁 1.51），且在 40–45 岁组 PRS 显著优于 PCE、多 3.2 倍适宜 [30]。
- UK Biobank 53,026 人 Olink 蛋白组训练的 15 种疾病模型平均 AUC 0.74（范围 0.56–0.89），较仅用临床因素平均提升 ΔAUC=0.03，且不依赖模型架构、简单模型如 L2 表现相当 [31]。
- EPIC-Norfolk 中 >11,000 人、>1,000 种代谢物、219,415 人年的分析识别出 640 个显著代谢物-疾病关联，其中 420 个（65.5%）跨至少 2 种非传染性疾病共享 [32]。
- 贝叶斯Cox回归通过计数过程表示的偏似然结合随机变分推断与似然重加权，可处理百万级数据点、数千时变协变量，但依赖变分近似，精度受子采样影响 [33]。

## 1 背景与定义

人群健康与多组学 AI 的边界，首先由“数据底座”划定：它要求至少万人级、带纵向随访与生物样本的队列或登记系统，而非单中心小样本关联研究。UK Biobank 以 50 万 40–69 岁参与者、健康记录链接与 20 年随访的事件量设计确立了这一范式 [22][34]；All of Us 以至少 100 万人、>80% 来自历史上研究不足群体为目标，补上多样性维度 [24]；FinnGen 以 224,737 人、1,932 个终点展示隔离人群的低频变异发现能力 [26]；丹麦国家登记则凭 ICD-8 到 ICD-10 的单向映射，把 1965 年以来的高粒度医疗数据接成可纵向分析的轨迹 [35]。**这一方向的“人群”属性不是样本量修辞，而是可复现性要求：结论需在至少两个独立队列或登记中成立。** 综述亦指出，组学技术、EHR 普及与 AI 正推动队列研究从描述性关联转向机制发现、精细风险分层与遗传导向的治疗开发 [36]。

演化脉络上，三条技术线各自独立成形后又开始交汇。EHR 侧从 BEHRT、Med-BERT 的“诊断码序列 + 自监督预训练”起步 [37][38]，经 GRASP 的跨系统语义映射 [17] 与 SurvivEHR 的竞争风险时间事件预训练 [39]，走到 Delphi-2M、Foresight、ALADYNOULLI 这类生成式轨迹模型 [40][1][2]，并进一步外推到国家级规模（Foresight-England，约 6100 万人）[3] 与多模态患者旅程（NOAH，559M 事件）[4]。遗传侧则从芯片插补的约 9600 万变异 [34] 升级到 490,640 人、32.5× 的全基因组测序 [23]，并把常见变异、罕见变异、结构变异与非加性效应逐层纳入 [41][42][11]。分子侧以 pQTL 图谱为枢纽，把“位点—蛋白—疾病”串成链条：54,219 人、2,923 种蛋白的定位发现 14,287 个主要关联、81% 为既往未报道 [9]，53,026 人的蛋白—疾病图谱报告 168,100 个蛋白—疾病关联、183 种疾病判别 AUC>0.80 [10]。**三条线的交汇点正是本方向的核心问题：如何把纵向 EHR 的表型轨迹、胚系遗传的因果锚点与血浆蛋白/代谢组的分子中介，放进同一个可跨队列复现的生成式或概率框架里。**

由此可提炼出四个核心问题。其一是**轨迹的粒度与可解释性**：Delphi-2M 与 Foresight 以事件序列预测为核心，ALADYNOULLI 则把轨迹压缩为潜在特征再回到遗传发现，粒度设定直接决定能回答哪类子问题 [40][2]。其二是**共病结构与亚型识别**：年龄依赖主题模型在 UK Biobank 282,957 样本中识别 52 种共病异质性疾病并在 All of Us 211,908 样本验证，18 个亚型 PRS 显著异于同病其他亚型 [43]；VaDeSC-EHR 则把风险建模与聚类整合而非先聚类再分层 [44]。其三是**跨队列与跨祖源可复现性**：泛 UKB 跨祖源荟萃在 7,266 个性状上新发现 14,676 个仅欧洲祖源分析未检出的位点 [45]，而 48 个冠心病 PRS 在三个生物库 171,095 人中群体表现相似却个体一致性差 [14]，说明**“群体 AUC 可复现”不等于“个体判断可复现”**。其四是**分子层的因果与中介**：pQTL 确定 474 个因果蛋白与 37 个药物重定位机会 [10]，但多数蛋白—疾病关联仍为观察性，因果解释依赖 MR 等假设。

方法学上，该方向的“AI”并非单一架构，而是覆盖贝叶斯混合、自回归 Transformer、图 Transformer、变分生存聚类与梯度提升等多类工具 [2][46][44][8]。与之配套的是生物样本库规模下的统计与计算基础设施：BOLT-LMM 在 UKB 全部 459K 欧洲样本上运行并保留相关个体 [47]，BASIL 在约 50 万人、>80 万 SNP 上精确求解完整 Lasso 路径 [48]，贝叶斯 Cox 回归借随机变分推断支持百万级数据点并给出不确定性估计 [33]。表型与结果的标准化工具则决定这些资源能否被复用：GWAS Catalog 截至 2024 年 7 月收录 625,113 条关联 [27]，Phecodes 支撑 PheWAS 与表型风险评分但依赖 ICD 编码 [49]，PHESANT 与 PheWeb 分别承担全表型扫描与结果可视化共享 [50][51]。

需要明确排除的邻近领域：单中心 <1000 人的组学关联研究、无公开数据也无代码的纯预测模型、无方法学新意的单病种临床评分改良，以及不与组学/EHR 联合的纯影像 AI，均不属本方向。**本方向的准入标准可归纳为三条：队列规模达生物样本库级、方法上有生成式/基础模型或概率整合的方法学贡献、结果在独立队列或登记中可复现。** 三者缺一，即落入“大规模但无方法新意”或“方法新颖但不可复现”的两类边缘地带——Foresight-England 因数据访问暂停而无法导出定量结果，正是后者的现实注脚 [3]。

## 2 方法学


### 2.1 生成式疾病轨迹模型

在纵向电子健康记录（EHR）上学习疾病轨迹，主流路线已从判别式预测转向生成式建模。**Foresight** 同样基于生成式预训练 Transformer，但强调整合结构化数据与约占 80% 的自由文本，覆盖 18 类 SNOMED 概念并支持日/周/月不同时间分辨率，作者明确其当前形式不宜直接用于临床决策支持 [1]。**ALADYNOULLI** 则走贝叶斯生成路线，以概率混合而非混合概率的形式联合建模纵向诊断、年龄与多基因风险，在 3 个生物库、n>683,000、随访 52 年、348 种疾病上识别出 **21 个可复制特征**，跨队列组成保留中位 80%，亚型 Cohen's d 达 4.25，基于特征的 GWAS 发现 **151 个全基因组显著位点**，包括单性状分析遗漏的心血管关联 [2]。三者对"轨迹"的粒度设定不同：Delphi-2M 与 Foresight 以事件序列预测为核心，ALADYNOULLI 则把轨迹压缩为潜在特征再回到遗传发现，这一差异也决定了各自能回答的子问题。

规模化与多模态是另一条分化轴。**Foresight-England** 报告了首个国家级 EHR 生成式基础模型，243M 参数 Transformer 解码器在 NHS England 安全数据环境内从头训练，使用约 **6100 万人**去标识化纵向 EHR（训练 5490 万、评估 610 万），整合基层/二级诊疗、死亡登记与 COVID-19 数据，并设计了 30 天住院与死亡预测评估框架；但因数据访问暂停，定量结果无法导出，论文仅作为分词、架构、训练与评估的方法学模板 [3]。**NOAH** 主张现有方法多为判别式、模态受限、受封闭类别词表约束且把时间当作单调归纳偏置，因而采用双向时间整合与变分隐空间，在 MIMIC 家族 **559M 事件、299,000 患者**上原生处理图像、时序、分类与文本记录，支持自回归预测、零样本分类与反事实干预模拟 [4]。**LifeLong Digital Twin** 把 Life Events 组织为每日 Health States 并累积为 Lifelong Health Context，配合 Agent Harness 引入语言模型文本之外的多模态证据，在 25 个疾病终点、3 类任务、4 个语言模型上，16 个模型-读出比较全部优于无 Context/Harness 的基线，疾病识别 F1 从 0.422 升至 0.504（Context）、0.515（Harness），相对增益 19.4%、22.0%，五年 C 微 F1 从 0.481 升至 0.559、0.569；但作者自陈缺乏配对不确定性、疾病支持计数与组件消融，未确立统计显著性 [5]。值得注意的是，Foresight-England 的规模叙事与其结果不可得形成明显张力，而 LifeLong Digital Twin 的增益虽一致却尚未通过显著性检验，二者都提示"更大/更统一"并不自动等于更强证据。

生成式轨迹模型的下游用法已超出单纯预测。**EHR-MPC** 把脓毒症治疗优化重构为推理时控制问题：先训练生成式 EHR 患者数字孪生预测干预下的临床轨迹，再用模型预测控制在推理阶段规划治疗，在 Mass General Brigham **8 家医院** ICU 脓毒症队列上离线策略性能与强化学习基线相当、模拟性能更优，但作者指出依赖离线数据、仿真评估可能与真实临床存在差距 [6]。与之相对，**VaDeSC-EHR** 用 Transformer 变分自编码器结合 Weibull 混合生存分布，把风险建模与聚类直接整合，而非先聚类再分层，从而识别兼具不同诊断轨迹与时间-事件特征的患者亚群 [44]。**MiGHT-EHR** 则以归一化 PMI 构建异质时序图，用带时序注意力的图 Transformer 自监督预训练并配合双平衡多任务学习，在 MIMIC-III/IV 四个任务上平均超越 SOTA，死亡率与再入院提升尤为显著，表征按结局聚类、医学概念可线性恢复且概率校准良好，但仅在 MIMIC 两个数据集上验证 [46]。这些工作共享"生成模型作为可干预/可分型底座"的思路，分歧在于评估落点：EHR-MPC 看策略优劣，VaDeSC-EHR 与 MiGHT-EHR 看表征结构与任务均值。

疾病分型与早期预警构成了轨迹建模最接近临床的一类应用，也暴露出验证强度的不均。AD/PD 亚型研究将诊断前带时间戳的 EHR 按就诊、年龄与日历年标记化，用 Transformer 生成患者嵌入后以 K-means 聚类，在 CPRD Aurum 与 UK Biobank 两个英国队列、**超过 100,000 名患者**中为每种疾病识别出 **5 个可复现亚型**，5 年随访显示亚型间死亡与住院预后差异并与基因型关联，局限在于依赖 EHR 记录质量、外部验证仅限 UK Biobank、生物学机制仍待验证 [7]。功能衰退预警则走轻量路线：基于 All of Us **297,861 人**（11.1% 为病例）、12 项生物标志物 3 年轨迹特征（斜率、变异性、delta、均值）训练 LightGBM，AUROC **0.797** 显著优于静态汇总的 0.755（P<0.001），匹配分析为 0.727 对 0.680，并可提前 3–12 个月持续预测（AUROC 0.768–0.740），但仅用常规实验室数据且缺乏外部队列验证 [8]。两类研究的设计不可直接比较高低：前者是聚类分型、后者是二分类预警，样本与终点均不同；可比较的只是各自研究内部的对照——轨迹特征优于静态特征、亚型间预后存在差异。整体上，本组证据在"生成式"标签下实际覆盖了贝叶斯混合、自回归 Transformer、图 Transformer、变分生存聚类与梯度提升等多类方法，真正的争议不在架构选择，而在于外部验证、结果可复现性与统计显著性能否跟上模型规模的扩张。

### 2.2 多组学与遗传整合

多组学与遗传整合的第一条主线，是把遗传关联从“位点—表型”推进到“位点—分子—表型”的链条。UK Biobank 的 pQTL 资源是这一链条的基础：Pharma Proteomics Project 对 **54,219 名参与者、2,923 种蛋白**开展定位，发现 **14,287 个主要遗传关联，81% 为既往未报道**，并精细映射出 29,420 个独立信号 [9]；同一队列的罕见编码变异分析在 49,736 人中鉴定 5,433 个罕见基因型—蛋白关联，其中 81% 未被既往 GWAS 检出，并显示 PTV 信号 99.4% 与蛋白降低相关 [52]。这两项工作共同说明常见与罕见变异对血浆蛋白组的贡献具有互补性。

蛋白组图谱把 pQTL 推向疾病端。基于 53,026 人、2,920 种蛋白的图谱报告 **168,100 个蛋白—疾病关联和 554,488 个蛋白—性状关联**，183 种疾病判别 AUC>0.80，并通过 pQTL 确定 474 个因果蛋白 [10]。类似地，NMR 代谢组图谱在 118,461 人中覆盖 249 个指标与 700 多种疾病的患病、发病和死亡关联，并在 THL Biobank 三万余人中重复验证 [53]。这些图谱的价值在于把遗传信号落到可测量的分子层，但其关联多为观察性，因果解释依赖 MR 等假设。

多基因风险评分与分子数据的结合提供了另一条路径。T2D 全基因组 PGS 在 UKB-PPP 中关联 **648 个蛋白，其中 617 个复制**，分区 PGS 则指向不同生物过程 [54]；血尿生物标志物的遗传分析在 363,228 人中识别 5,794 个独立位点与 51 个因果关系，多 PRS 模型在 FinnGen 中改善慢性肾病、2 型糖尿病、痛风与酒精性肝硬化的风险分层 [55]。代谢组评分在三个国家生物库 700,217 人中跨库重复，说明单一血液测量可同时分层多种疾病风险 [56]。

方法学上，混合模型与稀疏回归支撑了生物样本库规模的关联发现。BOLT-LMM 在 UKB 全部 459K 欧洲样本上运行并保留相关个体，身高等效 **650K 样本**，23 个性状独立位点增加 84% [47]；BASIL 则以迭代筛选—求解—校验的方式在约 50 万人、>80 万 SNP 的数据上精确求解完整 Lasso 路径 [48]。这些工具解决的是计算与统计功效问题，而非因果识别本身。

外显子测序把罕见变异纳入同一框架。454,787 人的 WES 分析发现 **8,865 个显著关联，涉及 564 个基因**，91% 不能由常见变异 LD 解释，81% 可复制 [41]；另一项 281,104 人的外显子 PheWAS 识别 632 个显著 ExWAS 变异，并刻画 PTV 携带谱 [57]；394,841 人的系统分析覆盖 4,529 个表型并公开汇总统计 [58]。UKB-ESC 首批 200,643 人数据开放，约 1000 万变异中含 453,733 个 LOF [59]，早期 49,960 人资源则显示测序人群总体代表 UKB 但富集哮喘（16.5% vs 13.5%）[60]。

非加性与非编码结构变异正在修正“加性常见变异”的默认假设。正交等位基因重编码框架在最多 399,943 名 UKB 个体、2,906 个血浆蛋白和 55 个数量性状上发现 **约三分之一同源基因—蛋白关系呈非线性剂量效应**，且标准重编码在 HWE 偏离下膨胀（λGC=78.3）而新方法保持校准（λGC=0.94）[11]。结构变异图谱在 54,306 人中插补 54,578 个 SV 和 15,826 个 VNTR，二者共同解释蛋白丰度遗传力约 **8.0%**，鉴定 8,065 个 SV—蛋白与 4,101 个 VNTR—蛋白独立关联 [42]。FinnGen 的 176,899 人分析则利用人群瓶颈导致的纯合子富集，系统搜索隐性关联，揭示同一变异在杂合与纯合状态下可呈不同表型 [61]。

上位效应与基因—环境交互是整合分析中争议较集中的部分。基于 UKB-PPP 的 cis-by-trans 上位效应映射以蛋白水平互作为单位、用三明治方差估计控制假阳性，识别出以 **ABO 为中心**的稳健互作网络 [62]；而表型尺度问题提示，许多 biobank GWAS 检出的 G×E 信号可能只是另一尺度上的加性效应，在 UKB 32 个表型中幂变换可解释 **45%** 的多基因评分 G×E 信号 [12]。fastGxE 则从计算端推进，声称在控制多基因效应与噪声异质性的同时实现 32.98 倍以上加速 [63]。两类工作指向同一警示：交互信号的统计显著不等于生物学交互。

跨祖源整合暴露了欧洲中心偏倚的代价。GBMI 汇集 23 个生物库、220 万人、14 个疾病终点，覆盖六大祖源（欧 1.4M、东亚 415K 等）[64]；泛 UKB 跨祖源荟萃在 7,271 个表型上新发现 **14,676 个**仅欧洲祖源分析未检出的位点 [13]。PRS 方面，PRS-CS 总体优于 P+T，且欧洲 LD 面板预测精度相当或更高，原因在于 GBMI 仍以欧洲祖源为主 [65]；All of Us 的 245,388 个全基因组序列显示增加多样性可提升部分性状精度，但最大化样本量并非普遍最优，PRS 精度随血统分歧线性下降、多血统训练可减缓 [66]。汉族 TPMI 463,447 人的分析则直接证明人群特异 PRS 优于欧洲为主模型 [67]。

同一人群内的对照研究进一步说明“群体表现相似”不等于“个体判断一致”。在 AOU、PMBB 与 UCLA 三个生物库、171,095 人中比较 48 个冠心病 PRS，发现群体水平表现相似的评分在个体层面一致性差（ICC 与 Light κ 低）[14]。这提示多组学整合若只报告群体 AUC，可能掩盖临床决策所需的一致性信息。

蛋白组遗传调控的祖源与性别异质性同样需要分层看待。ARIC 中欧裔 2,004 个、非裔 1,618 个蛋白有 cis 关联，多数共享但存在人群特异 pQTL，非裔样本可缩小可信集 [68]；MHC 区多祖源映射在 2,920 个蛋白中鉴定 13 个 cis、606 个 trans 关联，多数跨祖源一致，同时发现东亚 EDAR 的祖先富集关联 [69]。性别分层分析显示 **69.1% 的蛋白存在性别差异**，但遗传效应对蛋白的影响跨性别高度相似，仅 103 个 sd-pQTL [15]。这些结果共同表明，分子层异质性更多来自丰度而非遗传调控本身。

将遗传风险分解为生物学过程是近年的新方向。对 526 个 CAD 显著变异与 78 个相关表型做潜在因子分解，识别出 **8 个遗传组分**（如富含胆固醇脂蛋白、脂蛋白(a)、内皮功能障碍、凝血等），并据此构建过程特异性 pPRS，在 UK Biobank 458,905 人中验证其捕捉传统风险因素之外的生物学特征 [70]。类似地，DeGAs 对 2,138 个 UKB 表型的汇总统计做截断 SVD，100 个成分解释 41.9%/62.8%/75.5% 方差，PTV 富集肥胖性状并突出脂肪细胞生物学 [71]。这类方法把“多基因”拆成可解释的通路，但成分的生物学命名仍需功能验证。

多模态与纵向整合开始进入临床预测场景。PULSE 在 UKB 中从稀疏常规血检生成代谢组与蛋白质组，生成代谢组优于所有基准，生成蛋白质组对 6 种常见病 AUC 达 **0.72–0.83**，接近真实蛋白质组 [72]；MILTON 用生物标志物预测 3,213 种疾病，扩充病例后 PheWAS 发现多个基线未显著的新基因—表型关联 [73]。APOE4 致痴呆的中介分析整合神经影像 58,876、蛋白组 51,623 与代谢组 267,627 人，区分共享与疾病特异中介通路 [74]；APOE 跨六祖源的全表型分析在 367,757 人中识别 27 个相关表型，9 个具祖源特异性 [75]。这些工作把分子中介与预测连接起来，但中介假设与生成数据的临床效用仍是主要限制。

最后，证据中也存在对“新方法必然增益”的冷静检验。在 27 个 UKB 性状上，AlphaGenome、Borzoi、GPN-Star 三种基因组基础模型衍生的注释均未超越 baselineLD，中位增益分别为 1.8%、3.8% 对 5.1%，GPN-Star 甚至减少位点发现 [16]；而 KASM 整合 35 个蛋白结构与功能注释，在 786,871 人外显子组、26 个复杂性状上促进基因发现 [76]。两者对比说明，注释是否有用取决于其与性状的匹配程度，而非模型规模。

### 2.3 医学 / EHR 基础模型

结构化 EHR 基础模型的主线，是把患者历史视为医学概念序列、以自监督预训练获取可迁移表示。**BEHRT** 将 Transformer 用于结构化 EHR，利用就诊位置、年龄和事件顺序学习个体表示以预测未来诊断，在多项任务中优于 Deepr、RNN、LSTM 和 RETAIN 等基线 [37]。**Med-BERT** 进一步把 BERT 迁移到大规模 ICD 诊断序列，先自监督预训练再针对糖尿病、心衰等任务微调，与 BEHRT、G-BERT 及任务内训练模型比较，显示预训练可提升性能，尤其在标注样本有限时 [38]。两者的共同局限也相近：均主要依赖诊断码，跨机构泛化未充分验证 [37][38]。

针对跨系统迁移，**GRASP** 用大语言模型将医学编码映射到共享语义空间并结合 transformer 预测，在 UKB **391921** 人、FinnGen **253991** 人、Mount Sinai **386755** 人上预测 21 种疾病和全因死亡；其平均 ΔC-index 较语言无关模型在芬兰高 **88%**、美国高 **47%**，且 62% 疾病与 PRS 相关性显著更高 [17]。时间事件方向，**SurvivEHR** 以竞争风险时间事件目标在英国初级保健 **2300 万**患者、**76 亿**编码事件上预训练，风险分层超越基准生存模型并支持低资源微调，但外部多国泛化未验证 [39]。与之互补的是面向交互查询的 **EHRAgent**，以 LLM 智能体自主生成并执行代码完成多表 EHR 推理，成功率最高超最强基线 **29.6%**，仅在三个数据集验证 [77]。可见争议在于：语义嵌入能否替代统一数据模型尚无定论，而预测建模与自然语言交互两条路线在评估口径上并不可直接比较。

### 2.4 组学衰老时钟与纵向多组学动态

纵向多组学研究的核心进展之一，是把衰老时钟从单时点横断面估计推进到对个体轨迹的刻画。在 **335 名女性、8 年随访**的全血基因表达与代谢组数据中，**5,061 个基因和 181 个代谢物**随时间变化，且个体轨迹常偏离群体水平趋势，变化受遗传、昼夜节律、季节和污染物影响 [18]。这一结果提示，群体水平拟合的时钟可能掩盖个体异质性；但该队列仅限女性、样本量有限，其轨迹特征能否外推仍需其他队列检验。与之呼应，ARIC 研究基于三次访视的血浆蛋白组构建纵向蛋白衰老指数 **LPAI**，用 FPCA 提取纵向成分、Cox 弹性网训练死亡风险模型，并在 MESA 验证，声称同时捕捉衰老累积负担与变化速度，较单时点蛋白时钟提供额外预测信息 [78]。两者都强调纵向动态的价值，但前者侧重描述轨迹异质性，后者侧重预测效能，方法路径与验证方式不同。

在时钟构建的组学层次与器官维度上，工作呈现明显分化。UK Biobank **274,247 人**的 **107 个血浆非衍生代谢物**被用于开发 5 个器官特异性代谢组生物年龄 **MetBAG**，年龄预测平均绝对误差约 **6 年**，独立测试 Pearson r 为 0.25–0.42，并关联 525 个疾病终点、预测 14 类疾病与死亡风险 [19]。另一项工作为 **409,206 名**参与者的 **14 个器官**整合 NMR 代谢组、Olink 蛋白组与临床表型构建多组学器官时钟，发现年龄加速与死亡风险是器官生物学的不同维度，具有可分离的表型、分子和遗传结构 [79]。这两项研究都指向器官特异性，但前者以代谢物单一组学、以预测疾病终点为目标，后者以多组学整合、以区分年龄加速与死亡风险两个维度为目标，结论层面并不直接可比。此外，基于 **36 项常规临床指标**的生理衰老指数 **PAI/ΔPAI** 用限制立方样条 Cox 捕捉 U 型关系，在 DFTJ 与 UK Biobank 中预测死亡、心血管病及 9 种慢性病风险 [80]，说明低成本临床指标亦可构建衰老度量，但其训练主要来自中国老年人，外推受限。

干预与可逆性方面，UK Biobank **45,438 人**血浆蛋白分析显示体力活动越高 **ProtAgeGap** 越低，ProtAgeGap 与 2 型糖尿病风险相关（**HR=1.06**），高活动交互 **HR=1.05**；在 **26 名男性**的 12 周监督运动研究中，ProtAgeGap 下降相当于 **10 个月**，204 个评分蛋白多数稳定、部分如 CLEC14A 随运动变化并与胰岛素敏感性改善相关 [20]。该证据以观察性关联为主、干预样本量小，尚不能确立因果。时间维度上还有一类工作关注昼夜节律：UK Biobank **420,746 人**、**312 种**血液学、生化与代谢分子与采血时间关联，用贝叶斯加性回归树推导相位偏移与节律紊乱两个正交指标，节律紊乱基本独立于睡眠，可独立预测 **98 种**未来发病风险并映射到肝脏代谢通路 [21]。这提示纵向采样中的采血时间本身可能是混杂或信息源，与前述轨迹类研究对季节、昼夜节律的归因相互印证，但该研究为观察性关联，未明确因果机制。

## 3 数据与资源

大型前瞻性队列仍是人群健康多组学研究的骨干资源。**UK Biobank** 在2006–2010年间招募**50万**名40–69岁参与者，收集中老年复杂疾病的遗传与非遗传决定因素，并预计20年随访可累积糖尿病约68,000例、心梗与冠心病死亡47,000例、卒中20,000例、阿尔茨海默病30,000例等事件量 [22]。其深度表型覆盖生物测量、生活方式、血尿生物标志物及身体与脑影像，随访通过健康与医疗记录链接获得 [34]。该资源已被**超8000家机构使用、发表8000余篇论文**，并被用于神经疾病遗传与转化研究 [81]。需注意其参与者相对健康、以欧洲 ancestry 为主，且40–69岁的年龄范围为折中设计，可能影响暴露与结局的时序 [22][34]。

基因组数据经历了从芯片到全基因组的升级。UK Biobank 先完成50万人基因型质控、单倍型估计与**约9600万变异插补**，并通过身高GWAS和HLA-疾病关联复制验证数据质量 [34]；随后对**490,640人**开展全基因组测序，平均覆盖**32.5×**，识别约15亿变异，较插补芯片增18.8倍、较全外显子测序增>40倍，其中93.5%为芬兰以外的欧洲 ancestry [23]。这一测序资源改善了非编码与罕见变异的检测能力，但非欧洲样本仍有限 [23]。多国生物样本库综述将 UK Biobank、All of Us、新加坡 PRECISE、Biobank Japan 和韩国 NPBBD-Korea 并列比较，指出 WGS 可发现罕见变异、结构变异和调控元件，而计算基础设施、隐私伦理、临床整合与祖先多样性不足仍是共同挑战 [82]。

多样化队列的代表是 **All of Us**，计划在美国招募至少**100万人**；截至2019年7月，超过175,000人贡献生物样本，其中**>80%来自历史上研究不足群体**，34个站点收集了>112,000人的EHR数据 [24]。该计划尚处招募早期，长期随访和数据完整性有待建立 [24]。其EHR数据存在两条互补来源：一项比较研究纳入393,590名参与者（患者介导EHR 19,703人、提供者来源EHR 373,887人），发现患者介导来源人群更白、更女性、更多保险、随访更长，而WGS覆盖更少（**35.2% vs 83.2%**），两种来源在疾病患病率、表型关联和已知基因型-表型关联复制率上存在差异 [25]。这提示同一队列内部不同数据采集路径的研究效用不可互换，但该比较中患者介导样本量小、人群构成差异大，可能影响泛化 [25]。

隔离人群提供了另一类遗传发现资源。**FinnGen R5** 整合9个芬兰生物库与全国健康登记，基于**224,737人**插补基因型和**1,932个终点**开展GWAS与精细定位，发现隔离人群富集低频有害等位（0.1%≤MAF<5%），并能在既往研究充分的疾病中识别新的低频变异关联和可能因果编码变异 [26]。其代价是芬兰隔离人群遗传结构特殊，结果外推至其他人群受限 [26]。这与 UK Biobank 以常见变异插补为主、All of Us 以多样性为目标形成方法学上的分工，而非可直接比较高低的优劣。

表型与结果的标准化工具决定了这些资源能否被复用。**GWAS Catalog** 截至2024年7月收录**625,113条关联**、>15.5K性状和>85K全基因组汇总统计数据集，通过EFO性状映射、祖源框架及与PGS Catalog互链提升可复用性，但汇总统计标准化不足、非欧祖源偏少且依赖作者提交 [27]。EHR侧，**Phecodes** 基于ICD编码快速定义数千种临床有意义疾病的病例/对照状态，支撑PheWAS与表型风险评分，但依赖ICD编码，存在编码误差和表型异质性 [49]；跨版本纵向分析则需编码映射，已有工作构建了ICD-8到ICD-10的单向映射，覆盖完整ICD及丹麦本地扩展，可连接1965年以来超半世纪医疗数据，但未提供ICD-10回映射ICD-8 [35]。在UK Biobank内部，**PHESANT** 用规则算法为连续、整数和分类变量自动选择统计检验以执行全表型扫描 [50]，**PheWeb** 则以Manhattan、LocusZoom和PheWAS视图可视化与共享大规模关联结果，本身不含统计建模 [51]。

衍生数据产品与质量控制构成资源的第二层。UK Biobank 发布了覆盖**28种疾病和25种数量性状**的PRS Release及基准测试软件，广泛基准测试中优于**81个已发表PRS**，并在其他队列验证，但主要基于UK Biobank人群、跨种族适用性有限 [28]。NMR代谢组方面，针对约121,657人的168个标志物与81个比值建立额外质控流程，多数标志物技术因素中位解释**1.5%**，3,169个盲重复中位CV **4.55%**、R² **0.928**，并发布ukbnmr R包；该流程仅覆盖约三分之一UKB参与者，且基于已校准浓度而非原始谱 [83]。真实世界诊疗模式方面，基于爱沙尼亚30%随机人群样本EST-Health-30，将异质临床事件压缩为以诊断为中心的标准化摘要，形成覆盖**1000多个ICD-10三位字符诊断类别**的全国尺度数字图谱，属回顾性观察且仅基于单一国家样本 [84]。综述层面则指出，组学技术、EHR普及与AI正推动队列研究从描述性关联转向机制发现、精细风险分层与遗传导向的治疗开发，并日益全球化与多样化 [36]。

## 4 应用与结果

在跨祖源遗传关联发现方面，对 UK Biobank 多遗传祖源人群开展混合模型关联与跨祖源荟萃分析，覆盖了比以往更大比例的样本，生成 **7,266 个性状**的公开汇总统计，并报告了 **14,676 个**仅欧洲祖源分析未发现的显著位点，同时指出多数关联仍主要见于欧洲祖源、解释需注意人群结构等 caveats [45]。多基因评分的跨祖源效能差异同样明显：基于 GIANT 与 23andMe 最多 **510 万人**构建的多祖源 BMI 评分在欧洲裔 UK Biobank 参与者中解释 **17.6%** 的 BMI 变异，其他人群从 16%（东亚裔美国人）到 2.2%（农村乌干达人）不等；儿童期加入评分使 8 岁时解释方差从 11% 升至 21%，5 岁时对 18 岁 BMI 的预测从 22% 升至 35% [29]。这两项工作共同显示，扩大祖源覆盖能提升发现与分辨率，但非欧洲裔人群的预测效能仍显著偏低。

在冠心病风险预测上，不同建模路径给出了可对照的结果。时间依赖多状态模型 MSGene 整合遗传风险与电子健康记录，以年龄为时间尺度估计 10 种心血管代谢状态间的转移，相较 Framingham 30 年风险与 PCE 10 年风险可提供动态、年龄特异的终身风险并用于指导他汀治疗启动 [85]。另一项纵向分析在 FOS 3,588 人与 UK Biobank 327,837 人中显示 PRS 的风险比随年龄下降（**19 岁 3.58 降至 70 岁 1.51**），且在 40–45 岁组 PRS 显著优于 PCE、多 3.2 倍适宜 [30]；该研究自述两队列年龄范围有限、未涵盖全生命周期。蛋白组学路线则报告了增量增益：在 UK Biobank 中整合传统风险因素、PRS 与大规模蛋白组学，内部验证 AUC 从 **0.750 升至 0.789**、外部验证从 0.717 升至 0.762，9 蛋白面板即可捕获大部分预测信息 [86]。这些结果分别来自不同队列与设计，增益幅度不宜直接横向比较，但一致指向遗传与分子信息在较年轻阶段或增量判别上的价值。

蛋白组与代谢组风险分层在多病共存场景中被反复评估。UK Biobank 53,026 人 Olink 蛋白组训练的 15 种疾病模型平均 **AUC 0.74**（范围 0.56–0.89），较仅用临床因素平均提升 **ΔAUC=0.03**，且不依赖模型架构、简单模型如 L2 表现相当，跨队列泛化性受表型定义影响 [31]。在 16,128 名高血压参与者中检测 2,911 种 Olink 蛋白，随访 15.1 年 1,074 人（6.66%）发生心衰，NT-proBNP 关联最强（HR=1.68），蛋白组学可提升心衰风险预测 [87]。代谢组方面，54,933 名美国整合医疗系统参与者检测 250 个 NMR 标志物后，加入标准诊疗预测因子使几乎所有 9 个心血管-肾脏-代谢终点判别能力提升，2 型糖尿病、慢性肾病与代谢功能障碍相关脂肪性肝病增益最大 [88]；UK Biobank 中 MVX 每 1-SD **HR=1.213**、MetaboHealth **HR=1.503**，随访 8,876 人发病，提示代谢负担可补充传统风险因素 [89]。上述增益均以各自研究内的临床因素模型为对照，量级差异反映终点与人群不同。

多病共存的通路与轨迹研究提供了机制层面的结果。EPIC-Norfolk 中 >11,000 人、>1,000 种代谢物、219,415 人年的分析识别出 **640 个**显著代谢物-疾病关联，其中 **420 个（65.5%）**跨至少 2 种非传染性疾病共享，涉及肝肾功能、脂糖代谢、低度炎症与肠道微生物等可干预通路 [32]。UK Biobank 330,177 名基线无 CRM 疾病者、2,911 个血浆蛋白的多状态模型显示生物衰老可预测心肾代谢共病进展，并识别关键中介血浆蛋白 [90]；该研究为观察性设计，残余混杂与中介推断的因果性有限。UKB-MDRMF 整合六类多模态数据联合建模 **1,560 种疾病**，报告联合预测优于单类别评估并揭示风险因素-疾病及共病关联 [91]。PheMIME 则整合三大 EHR 系统汇总统计，实现跨机构多病共病网络的交互可视化与疾病聚类推断 [92]。

在特定疾病与药效场景中，深度学习与可解释模型各有应用。基于丹麦 DNPR 与美国 VA EHR 纵向疾病轨迹的深度学习模型可提前最多 3 年预测胰腺癌风险，输出分时间间隔的增量风险并识别最具信息量的诊断码，但属回顾性登记数据、外推有限、筛查成本与假阳性需权衡 [93]。HFpEF 方面，UKB 多组学（蛋白/代谢/影像/EHR，HFpEF 33,480 例）结合监督分类、无监督聚类与可解释 AI，在独立多中心 80/20 验证队列中识别症状性 HFpEF 风险并划分多组学亚型，局限包括定义依赖多阶段规则、欧洲人群为主 [94]。骨质疏松的可解释蛋白组框架用 XGBoost 与 SHAP 筛选出 FSHB、ADIPOQ、SOST、COL9A1、CHAD 等标志物，报告其优于全蛋白组模型，但外部验证与样本规模细节不明 [95]。药效遗传学方面，UKB 与 All of Us 的 EHR 纵向数据对 10 个药物-表型对（他汀 LDL-C、二甲双胍 HbA1c、降压药 SBP 等）开展 GWAS 与罕见变异负荷检验并证明疾病 PRS 可预测药效，主要局限为用药与检测时点不齐、依从性与适应证混杂 [96]。

## 5 评测、可复现性与争议

在大规模生存分析的可复现性上，**贝叶斯Cox回归**通过计数过程表示的偏似然结合**随机变分推断**与似然重加权，使后验分布可因子化到子样本，从而支持百万级数据点并给出可行的不确定性估计[33]。其评测以模拟和 **UK Biobank 心肌梗死**应用为对照，基准为传统Cox模型实现，可处理**百万级数据点、数千时变协变量**[33]。争议点在于该方法依赖变分近似，精度受子采样影响[33]，即近似推断的可行性与估计精度之间存在取舍，这一局限在证据中未被定量刻画。

相比之下，面向电子健康记录共病研究的AI方法仅有综述性梳理，从数据到知识的角度归纳相关方法，但证据中缺乏具体方法细节与结果[97]，因而无法与上述生存分析工作在评测设计或可复现性上直接比较；两者在任务（生存分析 vs 共病研究）与证据完备度上的差异，本身构成该方向评测证据不均衡的一个体现。

## 6 空白与趋势

综合上述证据，本方向当前最清晰的空白不在模型架构，而在**证据链的闭合程度**：生成式轨迹模型、多组学图谱与跨祖源遗传资源各自都已达到生物样本库级规模，但"规模—可复现—可临床转化"三者之间仍存在系统性缺口。以下按趋势与空白列出六条判断。

1. **生成式轨迹模型已跨过"能否建模"的门槛，但尚未跨过"能否被独立验证"的门槛。** Delphi-2M 在 UK Biobank 训练、丹麦登记验证，ALADYNOULLI 在 3 个生物库、n>683,000 上给出 21 个可复制特征与 151 个全基因组显著位点 [2]，说明跨队列复现已被纳入设计；但 Foresight-England 因数据访问暂停无法导出任何定量结果 [3]，LifeLong Digital Twin 的增益虽一致却自陈未确立统计显著性 [5]，EHR-MPC 仅在离线数据与仿真中评估 [6]。**"国家级规模"与"可审计的效应量"目前并不同时成立**，这是最值得投入的空白：需要把预注册的外部验证、配对不确定性与组件消融作为发表的最低门槛，而非可选项。

2. **轨迹的粒度定义尚未统一，导致不同研究回答的子问题不可通约。**没人做的方向是建立轨迹任务的基准套件**：在同一队列、同一表型定义下并列评测"下一事件预测 / 终身风险 / 亚型可分性 / 反事实干预"四类任务，并报告各自的不确定性。现有证据中，AD/PD 亚型研究在 >100,000 名患者中给出 5 个可复现亚型 [7]，而功能衰退预警在 All of Us 297,861 人上报告 AUROC 0.797 对静态 0.755 [8]，二者设计不可比，恰恰说明缺的是共同标尺而非更多单点结果。

3. **多组学图谱的"关联密度"已极高，但因果与中介环节仍主要依赖假设。** 53,026 人、2,920 种蛋白的图谱报告 168,100 个蛋白—疾病关联、183 种疾病 AUC>0.80、474 个因果蛋白 [10]；pQTL 侧 54,219 人、2,923 种蛋白中 81% 关联为既往未报道 [9]，罕见编码变异分析又补充 5,433 个罕见基因型—蛋白关联、81% 未被既往 GWAS 检出 [52]。**空白在于把"蛋白—疾病"关联升级为可干预的剂量—时间证据**：现有 MR 与共定位只能给出方向性判断，缺少在纵向采样下检验蛋白变化先于疾病发生的设计。PULSE 从稀疏血检生成蛋白组、对 6 种常见病 AUC 0.72–0.83 [72] 提供了低成本替代思路，但生成数据能否用于因果推断尚未被检验。

4. **跨祖源与跨机构的"群体表现相似、个体判断不一致"问题已被反复证实，却少有方法层面的回应。** 泛 UKB 跨祖源荟萃新发现 14,676 个仅欧洲祖源分析未检出的位点 [45]；多祖源 BMI 评分在欧洲裔解释 17.6% 变异，其他人群从 16% 到 2.2% [29]；更关键的是，48 个冠心病 PRS 在三个生物库 171,095 人中群体表现相似而个体一致性差 [14]。**没人做的是把"个体层面一致性"作为多组学模型的一等评测指标**：现有报告几乎清一色给 AUC/C-index，缺少 ICC、κ 或决策一致性口径，而这恰是临床落地的前置条件。

5. **纵向与器官特异的衰老时钟正在从"估计年龄"转向"区分维度"，但干预证据薄弱。** 335 名女性 8 年随访显示 5,061 个基因与 181 个代谢物随时间变化、个体轨迹常偏离群体趋势 [18]；274,247 人的 5 个器官 MetBAG 年龄预测 MAE 约 6 年 [19]；409,206 人 14 器官多组学时钟则指出年龄加速与死亡风险是可分离的两个维度 [79]。**趋势是器官化与多组学化，空白是因果与可逆性**：现有干预证据仅来自 26 名男性 12 周运动研究、ProtAgeGap 下降相当于 10 个月 [20]，观察性关联为主、样本极小，尚不足以支撑"时钟可被干预改变"的结论。

6. **数据资源与标准化工具已相当完备，但"同一队列内部数据路径不可互换"这一层风险尚未进入建模实践。** UK Biobank 已完成 490,640 人 WGS、平均覆盖 32.5× [23]，All of Us 计划百万级、截至 2019 年 7 月 >80% 样本来自研究不足群体 [24]，FinnGen R5 基于 224,737 人与 1,932 个终点 [26]；工具侧 GWAS Catalog 收录 625,113 条关联 [27]，Phecodes 支撑 PheWAS 与表型风险评分 [49]，ICD-8→ICD-10 单向映射可连接 1965 年以来数据 [35]。但 All of Us 内部患者介导与提供者来源 EHR 在 WGS 覆盖（35.2% vs 83.2%）、患病率与关联复制率上存在差异 [25]，**提示同一队列不同采集路径构成隐性批次效应**；目前几乎没有工作报告按数据来源分层建模或做敏感性分析，这是低成本、高价值的空白点。

总体判断：**本方向的瓶颈已从"数据与算力"转移到"验证协议与不确定性报告"**。生成式模型、蛋白组图谱与跨祖源资源都已具备万人至百万人级证据，但外部验证、个体一致性、因果中介与数据路径异质性四项，仍普遍停留在讨论而非方法层面；谁能把这几项做成标准流程，谁就能把现有规模优势转化为可复现的临床证据。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 生成式疾病轨迹模型 | 朝阳 | 近两年集中出现生成式 transformer 做患者时间线/疾病自然史建模：[1]（Foresight，GPT 式患者时间线生成，135 引）与 [40]（生成式 transformer 学疾病自然史，78 引）代表方法路线已立起来但仍在快速分化；[44] 做纵向生存数据的深度表征聚类、[2] 把纵向 EHR 与遗传放进贝叶斯框架，说明「生成式轨迹 + 遗传/生存」的整合尚未收敛，属近两年爆发、方法未定型的朝阳段 |
| 2.2 多组学与遗传整合 | 成熟 | 大规模 pQTL/遗传关联图谱已成型且被反复复用：[9]（UK Biobank 血浆蛋白组遗传关联，1547 引）与 [55]（35 项血尿标志物遗传学）确立了「人群多组学 + 遗传」的标准范式；[41]（45 万人外显子）与 [47]（biobank 尺度混合模型关联）说明统计方法已收敛、以增量和图谱扩展为主 |
| 2.3 医学 / EHR 基础模型 | 萌芽 | 雷达样本仅 5 篇且 CNS 占比 0：早期代表 [38]（Med-BERT）与 [37]（BEHRT）奠定了结构化 EHR 预训练路线，但后续 [77]（EHRAgent，LLM+代码做表格推理）与 [17]（LLM 提升 EHR 模型可迁移性）显示范式正被 LLM 重写、尚未形成稳定评测，属少量探索性工作 |
| 2.4 组学衰老时钟与纵向多组学动态 | 萌芽 | 近两年才出现人群尺度多器官/纵向组学衰老指标：[19]（多器官代谢组生物学年龄关联心血管代谢病）与 [78]（纵向蛋白组衰老指数预测死亡与多病）均为 2025 年、引用个位数；[20]（UK Biobank 蛋白组衰老可被运动逆转）进一步说明方向刚起步、以验证性小样本结论为主 |
| 3 数据与资源 | 成熟 | 队列资源本身已是公认基础设施：[22]（UK Biobank 开放资源，11473 引）与 [34]（深度表型+基因组数据）是长期被引的底座；[26]（FinnGen）与 [24]（All of Us）说明多队列资源格局已稳定，新工作主要是资源描述与扩展 |
| 4 应用与结果 | 朝阳 | 应用层近两年高产且不断换任务：[93]（从疾病轨迹深度学习预测胰腺癌风险，311 引）与 [32]（血浆代谢组刻画多病共存通路）证明「EHR/组学 → 结局预测与共病结构」可行；[45]（Pan-UK Biobank GWAS）与 [29]（BMI 多基因预测贯穿生命历程）显示新数据与新结局仍在快速产出，方法未收敛 |
| 5 评测、可复现性与争议 | 证据不足 | 雷达样本仅 2 篇：[33]（大规模 EHR 的贝叶斯 Cox 推断）与 [97]（AI 研究共病的方法综述）分别只覆盖统计推断与方法综述，缺少专门的基准/复现研究，无法据此判定阶段 |

**整体判断**：这个方向整体处于**朝阳期偏成熟的分层状态**——数据底座（2.2、3）已成熟、以图谱扩展和增量为主；生成式轨迹（2.1）与应用层（4）近两年爆发但方法未收敛；EHR 基础模型（2.3）和组学衰老时钟（2.4）仍在萌芽，且正被 LLM 范式重写。雷达样本中 **2025–2026 年证据占 43 篇（25+18），近两年占比 0.48、CNS 占比 0.32**，说明热度高但**评测与可复现性一节仅 2 篇**，是最大的结构性缺口。窗口期判断：**生成式轨迹 + 多组学衰老时钟的交叉还有约 1–2 年**的先发窗口，一旦 UK Biobank 蛋白组/Olink 与 EHR 轨迹的联合基准被大组做出来，增量空间会迅速收窄。最大不确定性是**跨队列可复现性**——现有结论多来自 UK Biobank 单队列，FinnGen/All of Us 上的迁移与公平性证据稀少，且缺少统一评测框架，导致「SOTA」难以比较。

**接下来怎么做**：
1. **做「生成式轨迹 × 蛋白组衰老时钟」的交叉模型**：用 UK Biobank 的纵向 EHR 诊断序列 + Olink 血浆蛋白组，把 [40] 的生成式疾病自然史框架与 [78] 的纵向蛋白组衰老指数结合，产出「衰老加速 → 疾病轨迹偏移」的可生成式预测器。现在做是因为两条线各自刚起（2.1 与 2.4 均近两年），交叉点尚无人占；可与你的衰老 + 单细胞背景直接对接。
2. **把 pQTL 图谱接到轨迹模型上做机制归因**：以 [9] 的蛋白 pQTL 为锚，用 [2] 的纵向 EHR+遗传贝叶斯框架做「遗传 → 蛋白 → 轨迹」的通路分解。切入点是用公开 pQTL summary stats + 轨迹模型做孟德尔随机化式归因，产出可解释的轨迹驱动蛋白清单；现在做是因为 pQTL 已成熟（可直接复用）而轨迹侧刚开放，属于低成本高杠杆。
3. **抢做跨队列复现基准（填补第 5 节空白）**：在 UK Biobank 训练、FinnGen 与 All of Us 上外部验证 [93] 式轨迹风险模型，产出公开 benchmark + 代码。雷达样本中评测类仅 2 篇、CNS 占比 0，这是最明显的空白；且与你「公共数据 demo」的合作项目天然契合，能快速形成方法学贡献而非又一个预测模型。
4. **用 LLM/agent 重写 EHR 基础模型的迁移层**：沿 [77] 与 [17] 的思路，做「结构化 EHR 预训练模型 + LLM 少样本迁移」在罕见结局与少数族群上的评测。现在做是因为 2.3 仅 5 篇、范式正被 LLM 改写，先发者容易定义评测口径；可与类器官多组学的表型注释结合，把实验表型作为 EHR 模型的弱标签。
5. **把类器官多组学作为轨迹模型的机制验证层**：用公共队列（UK Biobank/All of Us）发现共病/亚型结构（参考 [32] 的代谢组-多病通路），再用合作项目的类器官多组学做体外扰动验证，产出「人群发现 → 机制验证」的闭环论文。现在做是因为应用层（第 4 节）高产但普遍缺机制验证，这一环是差异化护城河，也最能把你现有的单细胞/多模态建模能力变现。

## 参考文献

1. Foresight—a generative pretrained transformer for modelling of patient timelines using electronic health records: a retrospective modelling study. The Lancet Digital Health 2024. https://doi.org/10.1016/s2589-7500(24)00025-6
2. A Bayesian framework for longitudinal EHR and genetic discovery. Nature 2026. https://doi.org/10.1038/s41586-026-10780-5
3. Foresight-England: Development of a National-Scale Generative AI Model of Electronic Health Records for Medical Event Prediction across the COVID-19 Pandemic.  2026. https://arxiv.org/abs/2608.16273
4. NOAH: Learning the Full Patient Journey. A Longitudinal Multimodal Time-Aware Model for Representation and Forecasting.  2026. https://arxiv.org/abs/2609.09140
5. LifeLong Digital Twin: A Unified Modeling Paradigm and Agent Harness for Event-Driven Lifelong Health State Trajectories.  . https://arxiv.org/abs/2610.05566
6. EHR-MPC: Inference-Time Control for Sepsis Treatment with Generative Patient Digital Twins. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.08793
7. Subtyping Alzheimer's disease and Parkinson's disease using longitudinal electronic health records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01085-3
8. Predicting Early Functional Decline from Longitudinal Laboratory and Vital Sign Trajectories: A Large-Scale Study Using the All of Us Research Program.  2026. https://arxiv.org/abs/2608.21589
9. Plasma proteomic associations with genetics and health in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06592-6
10. Atlas of the plasma proteome in health and disease in 53,026 adults.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.045
11. Deviations from genetic additivity driven by rare variants at biobank scale.. Nature communications . https://doi.org/10.1038/s41467-026-76151-w
12. Choice of phenotype scale is critical in biobank-based G × E tests.. Cell genomics . https://doi.org/10.1016/j.xgen.2026.101391
13. Pan-UK Biobank GWAS improves discovery, analysis of genetic architecture, and resolution into ancestry-enriched effects. medRxiv 2024. https://doi.org/10.1101/2024.03.13.24303864
14. Evaluating Performance and Agreement of Coronary Heart Disease Polygenic Risk Scores.. JAMA 2025. https://doi.org/10.1001/jama.2024.23784
15. Sex differences in the genetic regulation of the human plasma proteome.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59034-4
16. Genomic foundation models do not yet boost common variant discovery beyond standard functional annotations.  . https://doi.org/10.64898/2026.10.13.758880
17. Large language models improve transferability of electronic health record-based predictions across countries and coding systems.. NPJ digital medicine 2026. https://doi.org/10.1038/s41746-026-02363-5
18. Longitudinal dynamics of gene expression and metabolomics in an aging population cohort.. Science 2026. https://doi.org/10.1126/science.aed6452
19. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
20. Reversal of proteomic aging with exercise-results from the UK biobank and a 12-week intervention study.. npj aging 2025. https://doi.org/10.1038/s41514-025-00318-w
21. Molecular Circadian Disturbance in Human Blood Independently Predicts Multi-Disease Risk and Maps to Hepatic metabolism Pathways.  . https://doi.org/10.21203/rs.3.rs-11120748/v1
22. UK Biobank: An Open Access Resource for Identifying the Causes of a Wide Range of Complex Diseases of Middle and Old Age. PLoS Medicine 2015. https://doi.org/10.1371/journal.pmed.1001779
23. Whole-genome sequencing of 490,640 UK Biobank participants.. Nature 2025. https://doi.org/10.1038/s41586-025-09272-9
24. The “All of Us” Research Program. New England Journal of Medicine 2019. https://doi.org/10.1056/NEJMsr1809937
25. Robust replication of associations across patient-mediated and provider-sourced EHR data in the All of Us research program. npj Digital Public Health 2026. https://doi.org/10.1038/s44482-026-00032-8
26. FinnGen provides genetic insights from a well-phenotyped isolated population. Nature 2023. https://doi.org/10.1038/s41586-022-05473-8
27. The NHGRI-EBI GWAS Catalog: standards for reusability, sustainability and diversity.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1070
28. UK Biobank release and systematic evaluation of optimised polygenic risk scores for 53 diseases and quantitative traits. medRxiv 2022. https://doi.org/10.1101/2022.06.16.22276246
29. Polygenic prediction of body mass index and obesity through the life course and across ancestries.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03827-z
30. Dynamic Importance of Genomic and Clinical Risk for Coronary Artery Disease Over the Life Course. medRxiv 2023. https://doi.org/10.1101/2023.11.03.23298055
31. Generalizability of proteomic risk prediction across biobanks reveals dependence on phenotype definitions.  . https://doi.org/10.64898/2026.10.01.26364038
32. Plasma metabolites to profile pathways in noncommunicable disease multimorbidity. Nature Medicine 2021. https://doi.org/10.1038/s41591-021-01266-0
33. Bayesian Cox regression for large-scale inference with applications to electronic health records. Annals of Applied Statistics 2021. https://doi.org/10.1214/22-aoas1658
34. The UK Biobank resource with deep phenotyping and genomic data. Nature 2018. https://doi.org/10.1038/s41586-018-0579-z
35. A unidirectional mapping of ICD-8 to ICD-10 codes, for harmonized longitudinal analysis of diseases. European Journal of Epidemiology 2023. https://doi.org/10.1007/s10654-023-01027-y
36. Trends in large-scale human population cohorts.. Trends in Genetics 2026. https://doi.org/10.1016/j.tig.2026.08.002
37. BEHRT: Transformer for Electronic Health Records. Scientific Reports 2019. https://doi.org/10.1038/s41598-020-62922-y
38. Med-BERT: pretrained contextualized embeddings on large-scale structured electronic health records for disease prediction. npj Digital Medicine 2020. https://doi.org/10.1038/s41746-021-00455-y
39. SurvivEHR: a competing risks, time-to-event foundation model for multiple long-term conditions from primary care electronic health records.  2025. https://doi.org/10.1101/2025.08.04.25332916
40. Learning the natural history of human disease with generative transformers.. Nature 2025. https://doi.org/10.1038/s41586-025-09529-3
41. Exome sequencing and analysis of 454,787 UK Biobank participants. Nature 2021. https://doi.org/10.1038/s41586-021-04103-z
42. A proteome atlas of structural variation and VNTR effects on complex traits and diseases.  . https://doi.org/10.64898/2026.09.26.26364064
43. Age-dependent topic modelling of comorbidities in UK Biobank identifies disease subtypes with differential genetic risk. Nature Genetics 2023. https://doi.org/10.1038/s41588-023-01522-8
44. Deep representation learning for clustering longitudinal survival data from electronic health records.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56625-z
45. Pan-UK Biobank genome-wide association analyses enhance discovery and resolution of ancestry-enriched effects.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02335-7
46. MiGHT-EHR: A Multi-task Graph Transformer for Heterogeneous Temporal Electronic Health Records.  2026. https://arxiv.org/abs/2608.06430
47. Mixed model association for biobank-scale data sets. Nature Genetics 2018. https://doi.org/10.1038/s41588-018-0144-6
48. A fast and scalable framework for large-scale and ultrahigh-dimensional sparse regression with application to the UK Biobank. bioRxiv 2019. https://doi.org/10.1371/journal.pgen.1009141
49. Using Phecodes for Research with the Electronic Health Record: From PheWAS to PheRS. Annual Review of Biomedical Data Science 2021. https://doi.org/10.1146/annurev-biodatasci-122320-112352
50. Software Application Profile: PHESANT: a tool for performing automated phenome scans in UK Biobank. International Journal of Epidemiology 2017. https://doi.org/10.1093/ije/dyx204
51. Exploring and visualizing large-scale genetic associations using PheWeb. Nature Genetics 2020. https://doi.org/10.1038/s41588-020-0622-5
52. Rare variant associations with plasma protein levels in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06547-x
53. Atlas of plasma NMR biomarkers for health and disease in 118,461 individuals from the UK Biobank. Nature Communications 2023. https://doi.org/10.1038/s41467-023-36231-7
54. Identification of plasma proteomic markers underlying polygenic risk of type 2 diabetes and related comorbidities.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56695-z
55. Genetics of 35 blood and urine biomarkers in the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-020-00757-z
56. Metabolomic and genomic prediction of common diseases in 700,217 participants in three national biobanks.. Nature communications 2024. https://doi.org/10.1038/s41467-024-54357-0
57. Rare variant contribution to human disease in 281,104 UK Biobank exomes. Nature 2021. https://doi.org/10.1038/s41586-021-03855-y
58. Systematic single-variant and gene-based association testing of thousands of phenotypes in 394,841 UK Biobank exomes. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100168
59. Advancing human genetics research and drug discovery through exome sequencing of the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-021-00885-0
60. Exome sequencing and characterization of 49,960 individuals in the UK Biobank. Nature 2020. https://doi.org/10.1038/s41586-020-2853-0
61. Mono- and biallelic variant effects on disease at biobank scale. Nature 2023. https://doi.org/10.1038/s41586-022-05420-7
62. Robust cis-by-trans epistasis in the human plasma proteome highlights an ABO-centered interaction network.. American journal of human genetics . https://doi.org/10.1016/j.ajhg.2026.09.003
63. Genome-wide detection of genotype-environment interactions at biobank scale with fastGxE.. Nature genetics . https://doi.org/10.1038/s41588-026-02809-2
64. Global Biobank Meta-analysis Initiative: Powering genetic discovery across human disease. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100192
65. Global biobank analyses provide lessons for computing polygenic risk scores across diverse cohorts. medRxiv 2021. https://doi.org/10.1101/2021.11.18.21266545
66. All of Us diversity and scale yield context-dependent improvements in polygenic prediction.. Nature Genetics 2026. https://doi.org/10.1038/s41588-026-02734-4
67. Population-specific polygenic risk scores for people of Han Chinese ancestry.. Nature 2025. https://doi.org/10.1038/s41586-025-09350-y
68. Plasma proteome analyses in individuals of European and African ancestry identify cis-pQTLs and models for proteome-wide association studies. Nature Genetics 2022. https://doi.org/10.1038/s41588-022-01051-w
69. Multi-ancestry MHC-pQTL mapping reveals disease-linked HLA protein networks and shared genetic architecture.  . https://doi.org/10.21203/rs.3.rs-10956233/v1
70. Decomposing polygenic risk of coronary artery disease into distinct biological processes.  . https://doi.org/10.64898/2026.10.08.26365088
71. Components of genetic associations across 2,138 phenotypes in the UK Biobank highlight adipocyte biology. Nature Communications 2019. https://doi.org/10.1038/s41467-019-11953-9
72. Longitudinal alignments and syntheses of multimodal clinical data for personalized medicine with the PULSE framework. Nature Computational Science 2026. https://doi.org/10.1038/s43588-026-01026-5
73. Disease prediction with multi-omics and biomarkers empowers case–control genetic discoveries in the UK Biobank. Nature Genetics 2024. https://doi.org/10.1038/s41588-024-01898-1
74. Multimodal mediators connecting APOE4 to dementia.  . https://doi.org/10.21203/rs.3.rs-11445203/v1
75. Phenome-wide and proteomic analysis of APOE alleles across different ancestries in the All of Us Research Program.  . https://doi.org/10.64898/2026.09.26.26364080
76. Functional architecture of rare protein coding variation across 786,871 exomes.  . https://doi.org/10.64898/2026.10.16.26365771
77. EHRAgent: Code Empowers Large Language Models for Few-shot Complex Tabular Reasoning on Electronic Health Records.. Proceedings of the Conference on Empirical Methods in Natural Language Processing. Conference on Empirical Methods in Natural Language Processing 2024. https://doi.org/10.18653/v1/2024.emnlp-main.1245
78. A Novel Longitudinal Proteomic Aging Index Predicts Mortality, Multimorbidity, and Frailty in Older Adults.. Aging cell 2025. https://doi.org/10.1111/acel.70317
79. Age Acceleration and Mortality Risk Constitute Distinct Dimensions of Organ Aging.  . https://doi.org/10.21203/rs.3.rs-10881849/v1
80. Estimation of physiological aging based on routine clinical biomarkers: a prospective cohort study in elderly Chinese and the UK Biobank.. BMC medicine 2024. https://doi.org/10.1186/s12916-024-03769-2
81. UK Biobank-A Unique Resource for Discovery and Translation Research on Genetics and Neurologic Disease.. Neurology. Genetics 2025. https://doi.org/10.1212/nxg.0000000000200226
82. Lessons from national biobank projects utilizing whole-genome sequencing for population-scale genomics.. Genomics & informatics 2025. https://doi.org/10.1186/s44342-025-00040-9
83. Quality control and removal of technical variation of NMR metabolic biomarker data in ~120,000 UK Biobank participants. Scientific Data 2021. https://doi.org/10.1038/s41597-023-01949-y
84. A national-scale digital atlas of recorded care patterns across more than 1000 diagnostic categories using real-world health data: a retrospective observational study.  . https://doi.org/10.64898/2026.09.16.26363186
85. MSGene: a multistate model using genetic risk and the electronic health record applied to lifetime risk of coronary artery disease. Nature Communications 2024. https://doi.org/10.1038/s41467-024-49296-9
86. Machine Learning‐Driven Prediction of Coronary Artery Disease Risk Based on UK Biobank Plasma Proteomics. Journal of the American Heart Association : Cardiovascular and Cerebrovascular Disease 2026. https://doi.org/10.1161/JAHA.125.047248
87. Large-scale plasma proteomic profiling enhances prediction of heart failure among hypertensive individuals: prospective insights from the UK Biobank.. Journal of global health . https://doi.org/10.7189/jogh.16.04313
88. NMR metabolomics for cardiovascular-kidney-metabolic risk stratification in an integrated healthcare system.  . https://doi.org/10.64898/2026.10.01.26364322
89. MetaboHealth and Metabolic Vulnerability Index as Risk Factors for Cardio-Renal-Metabolic Multimorbidity: A Large-Scale Prospective Cohort Study.. Diabetes, obesity and metabolism 2026. https://doi.org/10.1111/dom.71112
90. Proteomics mediates the effects of biological aging on the progression of cardio-renal-metabolic comorbidity: a UK biobank cohort study.. Cardiovascular diabetology 2025. https://doi.org/10.1186/s12933-025-03035-6
91. UKB-MDRMF: a multi-disease risk and multimorbidity framework based on UK biobank data.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58724-3
92. PheMIME: an interactive web app and knowledge base for phenome-wide, multi-institutional multimorbidity analysis.. Journal of the American Medical Informatics Association : JAMIA 2024. https://doi.org/10.1093/jamia/ocae182
93. A deep learning algorithm to predict risk of pancreatic cancer from disease trajectories. Nature Medicine 2023. https://doi.org/10.1038/s41591-023-02332-5
94. Deep phenotyping of heart failure with preserved ejection fraction through multi-omics integration.. European journal of heart failure 2025. https://doi.org/10.1002/ejhf.70041
95. Explainable Plasma Proteomics–Based Machine Learning for Osteoporosis Diagnosis, Prognosis, and Protein Biomarker Discovery in the UK Biobank. The FASEB Journal 2026. https://doi.org/10.1096/fj.202600647R
96. Leveraging large-scale biobank EHRs to enhance pharmacogenetics of cardiometabolic disease medications.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58152-3
97. From data to knowledge: artificial intelligence methods for studying comorbidity in electronic health records. The European Physical Journal Special Topics 2026. https://doi.org/10.1140/epjs/s11734-026-02571-w
98. Integrating the environmental and genetic architectures of aging and mortality.. Nature medicine 2025. https://doi.org/10.1038/s41591-024-03483-9
99. Genetically supported targets and drug repurposing for brain aging: A systematic study in the UK Biobank.. Science advances 2025. https://doi.org/10.1126/sciadv.adr3757
100. Polygenic Prediction of Peripheral Artery Disease and Major Adverse Limb Events.. JAMA cardiology 2025. https://doi.org/10.1001/jamacardio.2025.1182
101. Genetic associations with ratios between protein levels detect new pQTLs and reveal protein-protein interactions. bioRxiv 2023. https://doi.org/10.1016/j.xgen.2024.100506
102. An atlas of polygenic risk score associations to highlight putative causal relationships across the human phenome. bioRxiv 2018. https://doi.org/10.7554/eLife.43657
103. Phenome-wide association studies across large population cohorts support drug target validation. Nature Communications 2018. https://doi.org/10.1038/s41467-018-06540-3
104. An atlas of genetic associations in UK Biobank. Nature Genetics 2017. https://doi.org/10.1038/s41588-018-0248-z
105. Comparative analysis of the Mexico City Prospective Study and the UK Biobank identifies ancestry-specific effects on clonal hematopoiesis.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02085-6
106. Phenome-wide Burden of Copy Number Variation in the UK Biobank.. American Journal of Human Genetics 2019. https://doi.org/10.1016/j.ajhg.2019.07.001
107. GWAS of extended prescription analgesic use identifies genetic loci in chronic pain.. Nature communications 2026. https://doi.org/10.1038/s41467-026-71434-8
108. SPA<sub>GRM</sub>: effectively controlling for sample relatedness in large-scale genome-wide association studies of longitudinal traits.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56669-1
109. A pre-train and fine-tune framework for adaptive boosting of pre-trained polygenic risk scores.. Nature communications . https://doi.org/10.1038/s41467-026-77128-5
110. Proteomic Signatures Capture Environmental Exposures Across Diverse Populations.  . https://doi.org/10.64898/2026.10.06.26364311
111. Imputation of fluid intelligence scores reduces ascertainment bias and increases power for analyses of common and rare variants.. Nature genetics . https://doi.org/10.1038/s41588-026-02787-5
