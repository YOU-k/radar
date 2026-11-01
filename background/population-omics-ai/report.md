# 人群健康与多组学 AI · 方向背景报告

证据 117 篇 · 覆盖度 0.80 · 第 13 轮 · 更新 2026-11-01

## 本次变更

- 新增 [84] A family-aware All of Us benchmark for polygenic prediction and genomic machine learning
- 新增 [90] HELICS: Biobank-scale Conditional Synthetic Genome Generation via Latent Flow Matching
- 新增 [77] fastGxE is a powerful method for uncovering genotype-environment interactions in biobanks.
- 新增 [59] MetabHub: an integrative platform for plasma nuclear magnetic resonance metabolomics using mediation analysis, disease prediction, and risk stratification.
- 新增 [64] Integrated multiomic scores for cardiovascular disease prediction across multiancestral populations
- 新增 [65] Biobank-scale self-supervised genotype pretraining yields transferable representations for human genetics.

## 摘要（TL;DR）

- ALADYNOULLI 以贝叶斯生成框架同时建模纵向诊断、年龄与多基因风险，在三个生物库 n>683,000、随访 52 年、348 种疾病上识别出 21 个可复制特征，跨队列组成保留中位 80%，并据此开展基于特征的 GWAS 发现 151 个全基因组显著位点 [1]。
- Delphi-2M 改造 GPT 架构建模疾病进展与竞争风险，在 UK Biobank 训练、丹麦登记验证，覆盖 1000 多种 ICD-10 疾病，并纳入性别、BMI、吸烟、饮酒与死亡以模拟个体终身轨迹、评估人口亚组公平性 [2]。
- Foresight-England 把自回归 Transformer 解码器（243M 参数）推到国家级规模，基于约 6100 万人纵向 EHR、训练 5490 万、评估 610 万，但因 NHS England 暂停数据访问，定量结果无法导出，文中表格与图均为占位符 [3]。
- 基于 All of Us 297,861 人、12 项生物标志物 3 年轨迹特征的研究报告轨迹模型 AUROC 0.797 优于静态汇总 0.755（P<0.001），匹配分析为 0.727 对 0.680，并可提前 3–12 个月预测，但仅用常规实验室数据、缺乏外部队列验证 [4]。
- LifeLong Digital Twin 在 25 个疾病终点、3 类任务、4 个语言模型上报告 16 个模型-读出比较全部提升，疾病识别 F1 由 0.422 升至 0.504（Context）与 0.515（Harness），相对增益 19.4% 与 22.0%，但缺乏配对不确定性、疾病支持计数与组件消融，未确立统计显著性 [5]。
- 对 454,787 人的外显子测序与 3,994 个健康表型分析发现 8,865 个显著关联、涉及 564 个基因，91%不能由常见变异LD解释，81%可独立复制 [6]。
- UKB Pharma Proteomics Project 在 54,219 人中检测 2,923 种蛋白，发现 14,287 个主要遗传关联，81%为既往未报道，精细映射出 29,420 个独立信号 [7]。
- 性别分层分析整合 Fenland 与 UKB 共 5,823 种蛋白，发现 69.1%蛋白存在性别差异，而遗传效应对蛋白的影响跨性别高度相似，仅 103 个 sd-pQTL [8]。
- All of Us 245,388 全基因组序列与 UKB 联合开发的 32 性状多祖源 PRS 显示，增加多样性提升部分性状精度，但最大化样本量并非普遍最优，PRS 精度随血统分歧线性下降、多祖源训练可减缓 [9]。
- 基因组基础模型衍生的注释在 27 个 UKB 性状上均未超越 baselineLD，AlphaGenome 与 Borzoi 中位增益 1.8%、3.8%，低于 baselineLD 的 5.1%，GPN-Star 甚至减少位点发现 [10]。

## 1 背景与定义

人群健康与多组学 AI 的边界，首先由“队列规模”与“数据层数”共同划定。它区别于单中心临床预测研究的地方在于：建模对象是生物样本库级别的前瞻或登记队列（UK Biobank 约 50 万人、All of Us 目标 100 万人、FinnGen R5 的 224,737 人、丹麦国家登记可回溯至 1965 年），输入至少覆盖 EHR 纵向诊断序列与胚系遗传之一，通常还叠加血浆蛋白组、NMR 代谢组、DNA 甲基化等分子层，输出则落在疾病风险、健康轨迹、共病结构与亚型四类任务上 [11][12][13][14]。**这一方向的核心问题不是“能否预测”，而是“在何种人群、何种表型定义、何种时间尺度上可复现地预测”**，因此跨队列验证、编码统一与评测基准被内在地纳入方法设计，而非事后补充。

演化脉络可以沿三条线看。第一条是 EHR 表示学习的谱系：BEHRT 把患者历史视为医学概念序列、以 Transformer 学习个体表示 [15]，Med-BERT 引入大规模自监督预训练并显示标注样本有限时的增益 [16]，随后 GRASP 用大语言模型做跨编码系统的语义对齐、SurvivEHR 引入竞争风险时间事件目标，把“跨机构迁移”与“时间-事件结构”变成一等公民 [17][18]。第二条是生成式轨迹建模：Foresight 证明结构化数据之外约 80% 的自由文本可支撑 18 类 SNOMED 概念预测 [19]，Delphi-2M 把范围推到 1000 多种 ICD-10 疾病并模拟终身轨迹 [2]，ALADYNOULLI 则把多基因风险并入生成过程、以特征发现为目标 [1]。第三条是组学-遗传整合：从 UK Biobank 深度表型与插补 9600 万变异 [20]、到 490,640 人全基因组测序 [21]，再到 UKB-PPP 的 2,923 种蛋白与 14,287 个主要遗传关联（81% 为新）[7]，以及 53,026 人血浆蛋白组-疾病图谱中 183 种疾病判别 AUC>0.80、pQTL 支持 474 个因果蛋白 [22]。三条线在近两年合流：PULSE 从稀疏血检生成代谢组与蛋白组谱并用于疾病预测 [23]，MILTON 用生物标志物与蛋白预测 3,213 种疾病状态并反哺遗传发现 [24]，说明**“组学补全—表型扩展—遗传发现”正在形成闭环**。

共病结构与亚型识别构成该方向区别于单病种预测的方法学内核。ATM 在 UK Biobank 282,957 人与 All of Us 211,908 人中用年龄依赖主题模型识别 52 种共病异质性疾病，18 个亚型 PRS 显著异于同病其他亚型 [25]；VaDeSC-EHR 把风险建模与聚类直接整合 [26]；AD/PD 研究在逾 100,000 名患者上得到每种疾病 5 个可重复亚型并经 UK Biobank 外部验证 [27]。**这些工作的共同判断是：同一诊断标签下的个体在轨迹与遗传风险上并不同质，亚型必须同时具备统计可重复性与外部队列可复制性才算成立**。与之配套的表型基础设施——Phecodes 的 ICD 高通量表型 [28]、ICD-8 到 ICD-10 的单向映射 [14]、GWAS Catalog 截至 2024 年 7 月的 625,113 条关联与 >85K 汇总统计数据集 [29]——决定了上述亚型能否被别的队列复用。

可复现性是当前最集中的张力所在，也是界定方向成熟度的关键。正面证据包括：代谢组风险评分在 UK Biobank、爱沙尼亚生物库与芬兰 THL 生物库共 700,217 人中跨三国重复 [30]；ALADYNOULLI 跨队列组成保留中位 80% [1]；GBMI 覆盖 23 个生物库、220 万人、14 个疾病终点证明多祖源聚合提升跨库验证 [31]。反面证据同样明确：48 个冠心病 PRS 在 171,095 人中群体表现相似却在个体层面一致性差 [32]；All of Us 与 UKB 联合的 32 性状多祖源 PRS 显示最大化样本量并非普遍最优、精度随血统分歧线性下降 [9]；多祖源 BMI 评分在欧洲裔解释 17.6% 变异，其他人群从 16% 到 2.2% 不等 [33]。**因此“跨队列可复现”应被理解为方向的定义性约束，而非附加卖点：一个模型若只在训练队列内报告增益，按本方向的纳入逻辑即不构成证据。**

最后需要明确几条边界，用以区分本方向与相邻领域。其一，纯影像 AI 不在范围内，除非与组学或 EHR 联合，如脑龄差 GWAS 整合 eQTL/pQTL 做药物靶点优先 [34]、或 PULSE 将视网膜图像与血液标志物共同纳入预测 [23]。其二，组学衰老时钟只有在人群健康结局上得到验证时才纳入，且需注意“年龄加速”与“死亡风险”可能是可分离的维度 [35]，纵向设计才能刻画变化速度而非仅累积负担 [36][37]。其三，方法学增益并非无条件：基因组基础模型注释在 27 个 UKB 性状上均未超越 baselineLD [10]，提示**数据层叠加本身不构成方法学贡献，校准、评测设计与不确定性量化才是该方向的实质门槛**。

## 2 方法学


### 2.1 生成式疾病轨迹模型

纵向电子健康记录（EHR）的生成式建模正从单病种预测转向对共病与终身轨迹的联合刻画。ALADYNOULLI 以贝叶斯生成框架同时建模纵向诊断、年龄与多基因风险，采用“概率的混合”而非“混合的概率”以容纳同时与慢性疾病，在三个生物库 **n>683,000**、随访 52 年、348 种疾病上识别出 **21 个可复制特征**，跨队列组成保留中位 80%，并据此开展基于特征的 GWAS 发现 **151 个全基因组显著位点**，包括单性状分析遗漏的心血管关联 [1]。与之相对，Delphi-2M 改造 GPT 架构建模疾病进展与竞争风险，在 UK Biobank 训练、丹麦登记验证，覆盖 **1000 多种 ICD-10 疾病**，并纳入性别、BMI、吸烟、饮酒与死亡以模拟个体终身轨迹、评估人口亚组公平性 [2]。两者都强调多病共存，但前者把遗传信息纳入生成过程并以特征发现为目标，后者侧重以序列生成做多终点发生率预测，评价取向不同。

在数据模态与规模上，工作间差异明显。Foresight 强调结构化数据之外约 **80%** 的自由文本，覆盖 18 类 SNOMED 概念，支持日/周/月分辨率预测与死亡前全程模拟，但作者明确其基于历史实践、当前形式不宜直接用于临床决策支持 [19]。Foresight-England 进一步把自回归 Transformer 解码器（**243M 参数**）推到国家级规模，基于约 **6100 万人**纵向 EHR、训练 5490 万、评估 610 万，整合基层/二级诊疗、死亡登记与 COVID-19 数据；然而因 NHS England 暂停数据访问，定量结果无法导出，文中表格与图均为占位符，仅留下分词、架构、训练与评估的方法学模板 [3]。NOAH 则主张原生处理图像、时序、分类与文本，以双向时间整合和变分隐空间在 MIMIC 家族 **559M 事件、299,000 患者**上训练，支持自回归预测、零样本分类与反事实干预模拟，但外部泛化尚待验证 [38]。可见“多模态、大规模”是共同方向，而可复现的定量证据在国家级部署中反而最薄弱。

面向临床决策的生成式轨迹模型开始与控制和分型任务结合。EHR-MPC 把脓毒症治疗优化重构为推理时控制：训练生成式 EHR 患者数字孪生预测干预下轨迹，再用模型预测控制在推理时规划治疗，在 8 家医院多中心 ICU 队列上离线策略性能与强化学习基线相当、模拟性能更优，但仿真评估与真实临床仍有差距 [39]。分型方面，VaDeSC-EHR 用 Transformer 变分自编码器与 Weibull 混合生存分布把风险建模与聚类直接整合，识别兼具不同诊断轨迹与时间-事件特征的患者亚群，其局限在于聚类数需预设、外部验证有限 [26]；针对 AD/PD 的研究则在 CPRD Aurum 逾 **100,000 名**患者上以 Transformer 嵌入加 K-means 得到每种疾病 **5 个可重复亚型**，经 UK Biobank 外部验证，5 年随访显示亚型间死亡与住院预后差异并与基因型关联 [27]。二者都做亚型，但前者以生存结局为聚类约束、后者以诊断前时间戳序列为输入并强调跨队列可复制性。

其余证据提示轨迹建模的边界与不确定性。基于 All of Us **297,861 人**、12 项生物标志物 3 年轨迹特征的研究报告轨迹模型 AUROC **0.797** 优于静态汇总 **0.755**（P<0.001），匹配分析为 0.727 对 0.680，并可提前 3–12 个月预测，但仅用常规实验室数据、缺乏外部队列验证 [4]。MiGHT-EHR 以异质时序图 Transformer 加双平衡多任务学习，在 MIMIC-III/IV 四任务上平均超越 SOTA，死亡率与再入院提升尤为显著，然仅限两个 MIMIC 数据集 [40]。LifeLong Digital Twin 将事件组织为每日健康状态并累积为终身上下文，在 25 个疾病终点、3 类任务、4 个语言模型上报告 **16 个模型-读出比较全部提升**，疾病识别 F1 由 0.422 升至 0.504（Context）与 0.515（Harness），相对增益 19.4% 与 22.0%，但缺乏配对不确定性、疾病支持计数与组件消融，未确立统计显著性 [5]。总体而言，证据在“生成式模型能否改善轨迹预测”上方向一致，争议集中在评估可信度：国家级模型因数据访问中断而无定量结果，多项研究报告的提升缺少外部验证或统计显著性检验，跨队列可复制性目前仅少数工作（如 ALADYNOULLI 的中位 80% 组成保留、AD/PD 的 UK Biobank 外部验证）给出直接证据。

### 2.2 多组学与遗传整合

以UK Biobank为代表的大规模生物样本库把遗传变异与数百至数千种表型连接起来，构成了多组学与遗传整合的基础资源。**GeneATLAS** 汇总了452,264名欧洲裔参与者的118个连续性状和660个二分类性状，公开9,113,133个变异关联结果及超3000万插补变异汇总统计 [41]；跨祖源的 **Pan-UK Biobank** 进一步覆盖7,271个表型，荟萃分析新发现14,676个仅欧洲祖源分析未检出的位点 [42]。外显子层面，UKB首批49,960人测序释放约400万编码变异，其中约98.6%频率低于1% [43]；UKB-ESC首批200,643人数据含约1000万变异，预测LOF达453,733个 [44]。

罕见编码变异的系统关联是这一整合路线的核心产出。对454,787人的外显子测序与3,994个健康表型分析发现8,865个显著关联、涉及564个基因，**91%不能由常见变异LD解释**，81%可独立复制 [6]；另一项281,104人外显子PheWAS识别632个全基因组显著ExWAS变异，并刻画了PTV携带谱 [45]。在394,841名欧洲裔外显子上对4,529个表型的单变异与基因负荷检验释放了全summary statistics [46]。方法层面，BOLT-LMM在459K欧洲样本上保留相关个体，身高等效650K样本，23性状独立位点由5,839增至10,759 [47]；BASIL则以迭代筛选求解完整Lasso路径应对>80万SNP的超高维回归 [48]。对非加性效应，正交等位基因重编码框架在最多399,943人中显示约三分之一同源基因-蛋白关系呈非线性剂量效应，且该方法在HWE偏离下保持校准（λGC=0.94），标准重编码则膨胀至λGC=78.3 [49]；KASM整合35个蛋白结构与功能注释，在786,871人外显子组、26个复杂性状上促进基因发现 [50]。

血浆蛋白组是遗传整合中数据最密集的组学层。UKB Pharma Proteomics Project在54,219人中检测2,923种蛋白，发现14,287个主要遗传关联，**81%为既往未报道**，精细映射出29,420个独立信号 [7]；同一资源的罕见变异分析在49,736人中鉴定5,433个罕见基因型-蛋白关联（81%为新），STAB1/STAB2分别关联77和41个蛋白，PTV信号99.4%与蛋白降低相关 [51]。蛋白组图谱将关联扩展到疾病终点：53,026人中2,920种蛋白产生168,100个蛋白-疾病关联和554,488个蛋白-性状关联，183种疾病判别AUC>0.80，pQTL支持474个因果蛋白 [22]。比值分析提供了另一条发现路径：基于1,463种蛋白、54,000余样本复制4,248个rQTL，显著p-gain蛋白对富集已知互作7.6倍，比值GWAS较单蛋白GWAS新增24.7%信号 [52]。此外，cis-by-trans上位效应映射识别出以ABO为中心的互作网络 [53]，MHC区在2,920种蛋白中检出13个cis、606个trans关联且多数跨祖先一致 [54]，长读长参考面板插补的54,578个SV和15,826个VNTR共同解释蛋白丰度遗传力约8.0% [55]。

蛋白组遗传调控的群体与个体差异值得单独讨论。ARIC中欧裔2,004种、非裔1,618种蛋白有cis关联，多数重叠但存在人群特异pQTL，非裔样本可缩小可信集 [56]。性别分层分析整合Fenland与UKB共5,823种蛋白，发现**69.1%蛋白存在性别差异**，而遗传效应对蛋白的影响跨性别高度相似，仅103个sd-pQTL [8]。这些结果提示，蛋白水平的差异更多来自丰度调控而非遗传效应本身，与遗传关联跨人群高度共享的观察相互呼应。

代谢组与临床生物标志物提供了成本更低的整合入口。UKB 118,461人的249项NMR指标与700多种疾病的患病、发病和死亡关联图谱在THL Biobank 3万余人重复验证 [57]；三国生物库700,217人用NMR代谢组训练12种高DALY疾病Cox模型，多数纳入超过半数36个代谢标志物并跨库重复 [30]。35项血尿指标的遗传分析在363,228人中识别5,794个独立位点和51个因果关系，多PRS模型在FinnGen中改善慢性肾病、2型糖尿病、痛风与酒精性肝硬化的风险分层 [58]。MetabHub则把251项NMR代谢物、129项临床指标、54项环境暴露、全基因组变异与57种新发疾病整合到同一平台并引入中介分析 [59]。

多组学与遗传的整合也被用于解析特定疾病的分子通路。T2D全基因组PGS在UKB-PPP中关联648个蛋白、617个复制，分区PGS揭示不同生物过程相关蛋白 [60]；冠心病风险被分解为8个遗传组分并构建过程特异性pPRS，在458,905人中验证其捕捉传统风险因素之外的生物学特征 [61]。脑龄差GWAS发现2个新位点和7个已知位点，整合eQTL/pQTL的MR与共定位优先7个可成药基因 [34]；APOE4致痴呆的多模态中介分析整合神经影像58,876人、蛋白组51,623人和代谢组267,627人，区分共享与疾病特异中介通路 [62]。慢性疼痛以处方镇痛药定义表型，在UKB与FinnGen各约50万人中识别140个关联、78个为新 [63]。

预测建模方面，MILTON用常规临床生物标志物、血浆蛋白和定量性状预测3,213种疾病，并通过对对照中隐性病例的识别扩充病例队列，扩充后PheWAS发现多个基线未显著的新基因-表型关联 [24]。PULSE以纵向自监督方式从稀疏血检生成代谢组与蛋白组谱，生成代谢组优于所有基准方法，生成蛋白组对6种常见病AUC达0.72–0.83 [23]。多组学评分整合在UKB 50,673人基于999种血浆蛋白构建疾病特异评分，并在PURE 9,358人验证，进一步整合2,279个多基因评分和479个DNA甲基化评分形成4种MEGASCORE [64]。SNPBERT在485,923人基因型上自监督预训练，掩码token准确率78.5%，嵌入聚类ARI在UKB子集为0.93（PCA 0.92），微调后的风险评分与PRS互补 [65]。

多基因评分的跨人群表现是整合研究中最集中的争议点。GBMI覆盖23个生物库、220万人、14个疾病终点，证明聚合多样祖源可提升发现与跨库验证能力 [31]；其PRS方法学比较显示PRS-CS总体优于P+T，且欧洲LD面板精度相当或更高，原因在于参与者仍以欧洲祖源为主 [66]。All of Us 245,388全基因组序列与UKB联合开发的32性状多祖源PRS显示，增加多样性提升部分性状精度，但**最大化样本量并非普遍最优**，PRS精度随血统分歧线性下降、多祖源训练可减缓 [9]。汉族人群TPMI 463,447人的全表型GWAS证明人群特异PRS优于欧洲为主模型 [67]；PAD的PRS-PAD在UKB 400,533、AoU 218,500、MGBB 32,982人中验证风险分层 [68]。与之相对，48个冠心病PRS在171,095人中群体表现相似却在个体层面一致性差 [32]，提示群体级指标不足以支撑个体化解读。

遗传关联向表型组的扩展同时暴露了方法学边界。162个PRS对551个表型的89,262次检验构建了PRS-表型图谱，但水平多效性可导致假阳性，需MR敏感性分析辅助判别 [69]；19个候选药物靶点在最多697,815人中做PheWAS，可识别真实多效性并提示疗效或安全性信号 [70]。DeGAs对2,138个表型的汇总统计做截断SVD，100个成分解释41.9%/62.8%/75.5%方差，PTV富集肥胖性状 [71]；ATM在UKB 282,957人与All of Us 211,908人中识别52种共病异质性疾病，18个亚型PRS显著异于同病其他亚型 [25]。CNV层面，472,228人芯片数据的全表型分析刻画了16p11.2、22q11.2、9p23等位点的负担 [72]；FinnGen 176,899人的隐性关联扫描显示纯合子富集可提升隐性致病变异检出，同一变异在杂合与纯合状态可呈现不同表型 [73]。

环境与遗传的相对贡献、以及交互检验的可靠性，构成另一组需要谨慎对待的结论。UKB 492,567人的暴露组全关联结合45,441人蛋白组衰老时钟，识别25个独立暴露，并发现环境暴露对死亡与25种年龄相关病的解释度常高于基因组 [74]。但G×E信号的可解释性受表型尺度影响：在32个表型上，幂变换可解释45%的多基因评分G×E信号，身高G×性别效应随对数尺度消失 [75]。方法学上，fastGxE通过控制多基因效应、多基因交互与噪声异质性实现32.98倍以上加速 [76]，另一篇同方法论文摘要信息有限、未给出定量结果 [77]；SPA_GRM针对纵向性状控制样本亲缘关系，在UKB 79个纵向性状中识别7,463个位点 [78]。

跨祖源的表型关联还揭示了同一基因的效应异质性。All of Us 367,757人、六个祖源群体的APOE全表型分析识别27个相关表型，集中于神经与脂质性状，5个脂质性状女性效应更大，9个关联具祖源特异性 [79]。MCPS 136,401人与UKB 416,118人的比较显示克隆性造血在MCPS显著更少（调整OR=0.59），且MCPS内部CH频率与欧洲祖源比例正相关（调整beta=0.84）[80]。蛋白组能否稳定捕捉环境暴露也受到检验：All of Us 10,043人、5,416种蛋白的分析发现蛋白暴露特征跨人群基本一致，仅<1%蛋白存在显著异质性，BMI为例外 [81]。

最后，若干工具性工作提示整合增益并非无条件。基因组基础模型衍生的注释在27个UKB性状上均未超越baselineLD，AlphaGenome与Borzoi中位增益1.8%、3.8%，低于baselineLD的5.1%，GPN-Star甚至减少位点发现 [10]。表型填充可提升效力：流体智力样本由约27万增至超45.5万后，独立显著常见SNP由390增至550，罕见变异分析鉴定26个显著基因 [82]。PRS微调框架AB-PRS在模拟中普遍优于预训练基线并控制FDR [83]；而All of Us v9的家族感知基准通过整家族分组划分发现、校准与测试集，针对跨研究PRS可比性与亲属数据泄漏问题提供了评估设计 [84]。这些结果共同表明，多组学与遗传整合的收益高度依赖队列多样性、表型定义与方法校准，而非单纯的数据层叠加。

### 2.3 医学 / EHR 基础模型

在结构化 EHR 上，早期工作主要把患者历史当作医学概念序列来建模。**BEHRT** 将 Transformer 用于结构化 EHR，利用就诊位置、年龄和事件顺序学习个体表示以预测未来诊断，在多种未来诊断预测任务中优于 Deepr、RNN、LSTM、RETAIN 等基线 [15]。随后 **Med-BERT** 把 BERT 迁移到 ICD 诊断序列，先在大规模数据上自监督预训练再针对糖尿病、心衰等任务微调，与 BEHRT、G-BERT 及任务内训练模型比较，显示预训练可提升预测性能，尤其在标注样本有限时 [16]。两者的共同局限也相似：BEHRT 依赖编码质量、跨机构泛化未充分验证 [15]；Med-BERT 仅用诊断码、未含药物检验，跨机构泛化同样待验证 [16]。

针对跨机构、跨编码系统的迁移问题，后续工作转向语义对齐与时间事件建模。**GRASP** 用大语言模型把医学编码映射到共享语义空间并结合 transformer 预测疾病，在 UKB 391921、FinnGen 253991、Mount Sinai 386755 人的数据上，平均 ΔC-index 较语言无关模型在芬兰高 **88%**、美国高 **47%**，且 62% 疾病与 PRS 相关性显著更高 [17]。**SurvivEHR** 则引入竞争风险时间事件预训练目标，基于英国初级保健 2300 万患者、76 亿编码事件训练生成式 Transformer，风险分层强、多任务超越基准生存模型，但仅限英国初级保健数据、外部多国泛化未验证 [18]。与前两类预测模型不同，**EHRAgent** 关注临床医生用自然语言直接查询 EHR：它将多表推理形式化为工具使用规划，借助交互式代码执行反馈迭代生成代码，在三个真实 EHR 数据集上成功率最高超最强基线 **29.6%**，少样本即可处理复杂临床任务，但依赖代码执行反馈迭代、仅在三个数据集验证 [85]。

### 2.4 组学衰老时钟与纵向多组学动态

纵向多组学研究的核心发现是，群体水平的衰老趋势不能代表个体轨迹。对 **335 名女性** 8 年全血基因表达与代谢组的纵向分析显示，**5,061 个基因和 181 个代谢物**随时间变化，但个体轨迹常偏离群体趋势；这些纵向变化基因具有细胞类型特异性并富集于心血管代谢和神经退行性疾病相关通路，且受遗传、昼夜节律、季节和污染物影响 [36]。这一结果提示，单时点横断面时钟只能捕捉累积负担，而纵向设计才能刻画变化速度。与此呼应，基于 ARIC 三次访视蛋白组构建的纵向蛋白衰老指数 **LPAI** 同时捕捉衰老累积负担和变化速度，在 MESA 验证中较单时点蛋白时钟提供额外预测信息，用于预测全因死亡、多病共存和衰弱 [37]。不过该研究训练与验证队列有限、蛋白平台存在差异、随访间隔较长 [37]，其额外预测增益的稳健性仍需更多队列检验。

在时钟构建的方法与子问题上，不同工作走向了不同方向。生理衰老指数 **PAI** 基于 36 项常规临床指标，用限制立方样条 Cox 模型捕捉生物标志物与死亡的 U 型关系，在 DFTJ 中国老年人和 UK Biobank 中预测死亡、心血管病及 9 种慢性病风险，优于仅以年龄为标签的模型 [86]；其局限在于训练主要来自中国老年人、欧洲验证外推有限、临床指标可受药物影响 [86]。代谢组方向则扩展到多器官框架：利用 UK Biobank **274,247 人**的 107 个血浆非衍生代谢物构建 5 个器官特异性代谢组生物年龄 **MetBAG**，独立测试 Pearson r 为 **0.25–0.42**，关联 525 个疾病终点并预测 14 类疾病与死亡风险，但代谢物覆盖有限、预测相关性中等、需跨人群验证 [87]。蛋白组时钟 **ProtAgeGap** 在 UK Biobank **45,438 人**中与体力活动负相关、与 2 型糖尿病风险相关（HR=1.06，高活动交互 HR=1.05），并在 26 名男性的 12 周运动干预中下降相当于 **10 个月**，但以观察性关联为主、干预样本量小、机制未完全明确 [88]。这些工作分别以临床指标、代谢物、蛋白为输入，队列与人群各异，其数字不宜直接横向比较高低。

一个值得注意的争议点是「年龄加速」与「死亡风险」是否同一维度。针对 UK Biobank **409,206 名**参与者 14 个器官、整合 NMR 代谢组、Olink 蛋白组和临床表型的多组学器官特异性衰老时钟研究发现，年龄加速与死亡风险是器官生物学的不同维度，具有可分离的表型、分子和遗传结构 [35]。这与将时钟偏差直接视为风险代理的常见做法形成张力，提示纵向时钟的评估指标需要区分「衰老程度」与「风险预测」。此外，时间维度本身也引入混杂：对 UK Biobank **420,746 人**、312 种血液分子的分析发现广泛昼夜节律改变，其中节律紊乱基本独立于睡眠，可独立预测 **98 种**未来发病风险并映射到肝脏代谢通路，但属观察性关联、因果机制未明 [89]。这提醒纵向采样时刻与节律状态可能系统性地影响组学衰老读数的解释。

### 2.5 隐私保护合成基因组与生物样本库规模生成

面向生物样本库规模的合成基因组生成，HELICS 提出无定相潜空间流匹配框架，在数十万至数千万相关 SNP 的超高维离散分布上做条件合成，通过染色体特异编码与多染色体潜空间流实现全基因组 SNP 级生成，并支持性状条件合成 [90]。其数据规模覆盖 **chr15 的 18,784 个 SNP 及全基因组 600,336 个 SNP**（UKB 无定相基因型），定位是隐私保护的基准测试、模拟与数据增强，尤其针对代表性不足人群、罕见或失衡疾病队列及受限生物样本库 [90]。

在与 HAPNEST、Sim1000G、HAPGEN2、GAN、RBM、HCLT 等基线的对比中，HELICS 在 MAF、LD 和隐私代理指标上占优，并能对多基因性状的遗传易感性进行条件控制 [90]。其局限同样明确：**低 MAF 变异 R² 偏低**，且生成样本的 **NN IBS 相似度较高**，提示多样性有限 [90]。

## 3 数据与资源

大型前瞻性队列仍是人群健康多组学研究的骨干资源。**UK Biobank** 在2006—2010年招募**50万**名40—69岁参与者，收集体检、生物样本、影像、加速度计与健康记录链接数据，并预计20年随访可累积糖尿病约**68,000**例、心梗与冠心病死亡47,000例、卒中20,000例、阿尔茨海默病30,000例[11]。其后续深度表型与基因组释放对全部参与者完成基因型质控、群体结构与亲缘关系分析，并插补约**9600万**变异、估计11个HLA基因经典等位变异，通过身高GWAS和HLA-疾病关联复制验证数据质量[20]。2025年进一步报告**490,640**人全基因组测序，平均覆盖**32.5×**，识别约15亿变异，较芯片插补增18.8倍、较全外显子测序增>40倍，其中93.5%为芬兰以外欧洲祖源[21]。该队列的局限也明确：年龄范围40—69岁为折中，可能影响暴露与结局时序[11]；参与者相对健康、以欧洲祖源为主[20][21]；神经疾病部分病例数仍有限[91]。

面向多样性与全国尺度的资源构成另一条路线。**All of Us** 计划在美国招募至少**100万**名多样化参与者，截至2019年7月已有>175,000人贡献生物样本，其中**>80%**来自历史上研究不足群体，34个站点收集>112,000人EHR数据[12]。该计划内部对EHR来源的系统比较显示，患者介导EHR（PME）与提供者来源EHR（HPO）在人群构成与测序覆盖上存在差异：PME参与者19,703人、HPO 373,887人，PME中WGS比例为**35.2%**而HPO为**83.2%**，PME人群更白、更女性、更多保险、随访更长[92]。这提示同一队列内不同数据采集路径不能简单互换，比较须限定在同一研究内部。

隔离人群与登记表型提供互补的发现能力。**FinnGen R5** 整合9个芬兰生物库与全国健康登记，基于**224,737**人插补基因型和**1,932**个终点开展GWAS与精细定位，发现芬兰隔离人群富集低频有害等位（0.1%≤MAF<5%），并能在既往研究充分的疾病中识别新的低频变异关联与可能因果编码变异[13]。其遗传结构特殊，结果外推至其他人群受限[13]。跨国综述将UK Biobank、All of Us、新加坡PRECISE、Biobank Japan与韩国NPBBD-Korea并置，指出WGS可发现罕见变异、结构变异和调控元件，但计算基础设施、隐私伦理、临床整合与祖先多样性不足仍是共同挑战[93]。

表型定义与编码统一决定多组学数据能否复用。**Phecodes** 基于ICD编码快速定义数千种临床有意义疾病的病例/对照状态，最初用于PheWAS，后扩展至表型风险评分[28]，但依赖ICD编码，存在编码误差与表型异质性[28]。针对跨版本问题，有研究构建ICD-8到ICD-10的单向映射，覆盖完整ICD及丹麦本地扩展，可连接丹麦自1965年以来超半世纪医疗数据，但未提供ICD-10回映射ICD-8[14]。在真实世界数据侧，基于爱沙尼亚**EST-Health-30**（30%随机人群样本）的自动化框架将异质临床事件压缩为以诊断为中心的标准化摘要，形成覆盖**1000多个**ICD-10三位字符诊断类别的全国尺度诊疗模式数字图谱，属回顾性观察且仅基于单一国家样本[94]。

关联结果的汇聚与复用依赖标准化数据库与工具链。**NHGRI-EBI GWAS Catalog** 截至2024年7月收录**625,113**条关联、>15.5K性状和>85K全基因组汇总统计数据集，通过EFO性状映射、祖源框架及与PGS Catalog互链提升可复用性，但汇总统计标准化不足、非欧祖源偏少、依赖作者提交[29]。**UKB PRS Release** 发布28种疾病和25种数量性状的多基因风险评分及基准测试软件，广泛基准测试中优于**81**个已发表PRS并在其他队列验证，但主要基于UK Biobank人群，跨种族适用性有限[95]。工具层面，**PHESANT** 以规则算法为UK Biobank异质表型自动选择统计检验并输出图表，依赖UKB变量规则、自动化模型未必适用于所有复杂表型[96]；**PheWeb** 整合Manhattan、LocusZoom与PheWAS视图供浏览共享大规模GWAS/PheWAS结果，仅作可视化与共享、不含统计建模[97]。

组学数据的质量控制是可分析性的前提。针对UK Biobank约**121,657**人NMR代谢标志物数据（168个标志物加81个比值、3,169个盲重复），研究识别样本制备时间、运输板孔位、光谱仪批次与时间漂移等额外技术变异来源，多数标志物技术因素中位解释**1.5%**，盲重复中位CV **4.55%**、R² **0.928**，并发布ukbnmr R包；该流程仅覆盖约三分之一UKB参与者，且基于已校准浓度而非原始谱[98]。综述层面，大型人群队列正随高通量组学、EHR普及与AI整合深度分子谱与纵向真实世界数据，从描述性关联转向机制发现、精细风险分层与遗传导向治疗开发，并日益全球化与多样化[99]；UK Biobank自身已超8000机构使用、8000余篇论文，其遗传证据对应药物获批概率高2倍以上[91]。

## 4 应用与结果

在跨祖源遗传关联发现方面，Pan-UK Biobank 对 UK Biobank 多遗传祖源人群开展混合模型关联与跨祖源荟萃分析，覆盖比以往更大比例的样本，生成 **7,266 个性状**的公开汇总统计，并报告 **14,676 个仅欧洲祖源分析未发现的显著位点**，如 CAMK2D 与甘油三酯、G6PD 多效错义变异；作者同时指出多数关联仍主要见于欧洲祖源，解释需注意人群结构等 caveats [100]。多基因评分方面，基于 GIANT 与 23andMe 最多 510 万人数据构建的祖源特异与多祖源 BMI 评分，其多祖源评分在 UK Biobank 欧洲裔中解释 **17.6%** 的 BMI 变异，其他人群从东亚裔美国人 16% 到农村乌干达 2.2% 不等；儿童期加入评分使 8 岁时解释方差从 11% 升至 21%，5 岁时预测 18 岁 BMI 从 22% 升至 35% [33]。可见跨祖源覆盖扩大了发现，但非欧洲裔预测效能显著较低仍是共同限制。

在冠心病风险预测上，不同方法给出的改进路径与量级各异。MSGene 以年龄为时间尺度的多状态模型整合 CAD-PRS、吸烟、降压药与他汀等协变量，相较 Framingham 30 年风险与 PCE 10 年风险，可给出动态、年龄特异的终身风险并用于指导他汀启动 [101]；同一问题上的时变分析显示 PRS 风险比从 19 岁 **3.58** 降至 70 岁 **1.51**，40–45 岁组 PRS 显著优于 PCE [102]。蛋白组学路线则在 UK Biobank 中整合传统风险因素、PRS 与 202 蛋白风险评分，内部验证 AUC 从 **0.750 升至 0.789**，外部验证从 0.717 升至 0.762，且 9 蛋白面板即可捕获大部分预测信息 [103]。这些结果说明遗传与蛋白信息在不同年龄段、不同终点定义下的增益并不一致，直接横向比较不同队列的数值并不合适。

心肾代谢共病是多个队列集中发力的子问题，方法从多状态模型到代谢组评分不等。UK Biobank 330,177 名基线无 CRM 疾病者中，生物衰老指标结合 2,911 个血浆蛋白的多状态与中介分析提示关键循环蛋白可作为风险预测标志物与抗衰老干预靶点 [104]；在 269,530 名横断面与 240,576 名随访参与者中，MVX 每 1-SD **HR=1.213**、MetaboHealth **HR=1.503**，随访 8,876 人发病，提示代谢负担可补充传统风险因素 [105]。更早的 EPIC-Norfolk 研究以 >1,000 代谢物刻画 27 种新发 NCD，发现 640 个显著代谢物-疾病关联中 **420 个（65.5%）跨至少 2 种 NCD 共享**，涉及肝肾功能、脂糖代谢、低度炎症与肠道微生物等通路 [106]。美国整合医疗系统 54,933 人中加入 250 个 NMR 代谢标志物后，9 个 CKM 终点几乎均获判别提升，2 型糖尿病、慢性肾病与代谢功能障碍相关脂肪性肝病增益最大 [107]。这些工作一致指向共享代谢通路，但队列、人群与终点定义不同，效应量不可直接对比。

多病共存与多模态整合框架方面，UKB-MDRMF 整合基本、生活方式、测量、环境、遗传与影像六类数据联合建模 **1,560 种疾病**，报告联合预测优于单类别评估并揭示风险因素-疾病及共病关联，同时提供交互平台 [108]；PheMIME 则整合 VUMC、Mass General Brigham 与 UK Biobank 三大 EHR 系统的表型组多病共病汇总统计，实现跨系统共病网络交互可视化与疾病聚类推断，并以精神分裂症为例展示 [109]。两者一为预测建模、一为可视化知识库，均依赖既有汇总统计或 UKB 人群，遗传与影像覆盖不全、缺失值插补等限制被明确列出。

药效遗传学与专科疾病的多组学应用提供了另一类结果。利用 UKB 与 All of Us 的 EHR 纵向用药与生物标志物数据，研究者对 10 个药物-表型对（他汀 LDL-C、二甲双胍 HbA1c、降压药 SBP 等）做常见变异 GWAS 与罕见变异负荷检验并在 All of Us 重复，证明疾病 PRS 可预测药效，同时指出用药与检测时点不齐、依从性与适应证混杂等纵向表型分析陷阱 [110]。HFpEF 方面，UKB 多组学（蛋白/代谢/影像/EHR，33,480 例）结合监督分类、无监督聚类与可解释 AI，在独立多中心 80/20 验证中识别症状性 HFpEF 风险并划分多组学亚型 [111]；高血压人群 16,128 人中检测 2,911 种 Olink 蛋白，随访 15.1 年 1,074 人（6.66%）发生心衰，NT-proBNP 关联最强（**HR=1.68**），蛋白组学提升风险预测 [112]。骨质疏松的可解释蛋白组学框架用 XGBoost 与 SHAP 筛选出 FSHB、ADIPOQ、SOST、COL9A1、CHAD 等标志物，报告其模型优于全蛋白组模型 [113]。

蛋白组风险预测的泛化性是上述工作共同的争议点。UK Biobank 53,026 人 Olink 数据训练的 15 种疾病模型平均 **AUC 0.74（范围 0.56–0.89）**，较仅用临床因素平均提升 **ΔAUC=0.03**，且不依赖模型架构、简单模型如 L2 表现相当，作者强调跨队列泛化性受表型定义影响 [114]。这与前述 CAD、心衰等单一疾病中蛋白组学带来的增益在量级上并不一致，提示增益大小取决于终点、人群与表型定义，而非单纯由组学数据规模决定。

## 5 评测、可复现性与争议

在方法层面，大规模生存分析的可复现性挑战主要来自计算实现与近似推断的取舍。针对传统Cox模型实现难以适配高维、不规则时点且超出内存的数据，有工作提出**贝叶斯Cox回归随机变分推断**，基于计数过程表示的Cox偏似然结合随机变分推断与似然重加权，使后验分布可因子化到子样本，从而支持**百万级数据点**与数千时变协变量的分析，并在UK Biobank心肌梗死应用中给出可行不确定性估计[115]。其局限也被明确指出：依赖变分近似，精度受子采样影响[115]。这意味着评测此类方法时，不确定性估计的可靠性需与子采样策略一并考察，而非仅看其能否处理大规模数据。

相比之下，面向电子健康记录共病研究的AI方法综述仅停留在方法梳理层面，抽取字段显示其仅有摘要信息、无具体方法细节，具体方法与结果不详[116]。因此该证据无法为评测指标或可复现性争议提供可核对的数字或对照，两篇证据之间也不构成直接的方法学冲突，只是前者提供了可检验的实现与局限，后者尚缺可展开的实质内容。

## 6 空白与趋势

现有证据在“生成式模型能否改善轨迹预测”上方向一致，但**评估可信度是当前最薄弱的环节**。国家级模型 Foresight-England 因 NHS England 暂停数据访问而无法导出任何定量结果，表格与图均为占位符，只留下分词、架构与训练的方法学模板 [3]；NOAH 在 MIMIC 家族 559M 事件上训练并支持反事实干预模拟，但外部泛化尚待验证 [38]；LifeLong Digital Twin 报告 16 个模型-读出比较全部提升、疾病识别 F1 由 0.422 升至 0.515，却缺乏配对不确定性、疾病支持计数与组件消融，未确立统计显著性 [5]。与之对照，跨队列可复制性目前只有少数工作给出直接证据：ALADYNOULLI 在三个生物库上跨队列组成保留中位 80% [1]，AD/PD 亚型研究经 UK Biobank 外部验证 [27]。**“大规模”与“可复现”尚未在同一项工作中同时成立**，这是本方向最需要补的空白。

围绕这一空白，可以归纳出若干条趋势与尚未被占据的位置：

1. **从单点预测走向“推理时控制”与反事实轨迹**。EHR-MPC 把脓毒症治疗优化重构为推理时控制问题，用生成式数字孪生预测干预下轨迹再由模型预测控制规划治疗，在 8 家医院 ICU 队列上离线策略与强化学习相当、模拟更优 [39]；NOAH 亦支持反事实干预模拟 [38]。但**尚无工作在生物库级别队列上把反事实轨迹与遗传/多组学分层结合**，也缺少对仿真-现实差距的系统评估。

2. **共病结构发现与遗传发现开始闭环，但亚型定义仍依赖预设**。ALADYNOULLI 以贝叶斯生成框架联合建模纵向诊断、年龄与多基因风险，识别 21 个可复制特征并据此发现 151 个全基因组显著位点 [1]；ATM 在 UKB 282,957 人与 All of Us 211,908 人中识别 52 种共病异质性疾病，18 个亚型 PRS 显著异于同病其他亚型 [25]。然而 VaDeSC-EHR 的聚类数需预设、外部验证有限 [26]，**亚型数目与稳定性缺乏跨队列的客观判据**，也少见把亚型回投到 pQTL/蛋白组层面做机制解释的工作。

3. **纵向组学时钟揭示“群体趋势≠个体轨迹”，但纵向时钟的评估维度尚未统一**。335 名女性 8 年纵向分析显示 5,061 个基因和 181 个代谢物随时间变化、个体轨迹常偏离群体趋势 [36]；纵向蛋白衰老指数 LPAI 同时捕捉累积负担与变化速度，在 MESA 验证中较单时点时钟提供额外预测信息 [37]。但 UK Biobank 409,206 人、14 个器官的多组学时钟研究指出**年龄加速与死亡风险是器官生物学的不同维度**，具有可分离的表型、分子与遗传结构 [35]，这与把时钟偏差直接当作风险代理的常见做法形成张力。**目前缺少在生物库规模上同时报告“衰老程度”与“风险预测”两套指标、并做跨人群验证的纵向时钟基准**。

4. **多模态与多组学的“生成式补全”是新兴但验证不足的方向**。PULSE 以纵向自监督从稀疏常规血检生成代谢组与蛋白组谱，生成代谢组优于所有基准，生成蛋白组对 6 种常见病 AUC 达 0.72–0.83 [23]；MILTON 用常规生物标志物、血浆蛋白与定量性状预测 3,213 种疾病，并通过识别对照中的隐性病例扩充病例队列，扩充后 PheWAS 发现多个基线未显著的新基因-表型关联 [24]。**但生成谱能否替代真实测量用于下游遗传发现、其误差如何传播到 pQTL 与 PRS，尚无系统评估**。

5. **跨祖源与跨编码系统的可迁移性仍是硬约束**。GRASP 用大语言模型把医学编码映射到共享语义空间，在 UKB 391,921、FinnGen 253,991、Mount Sinai 386,755 人上平均 ΔC-index 较语言无关模型在芬兰高 88%、美国高 47% [17]；Pan-UK Biobank 生成 7,266 个性状汇总统计并报告 14,676 个仅欧洲祖源分析未发现的显著位点，但作者指出多数关联仍主要见于欧洲祖源 [100]。**编码统一方面，ICD-8 到 ICD-10 的单向映射可桥接丹麦自 1965 年以来的数据，却不提供回映射** [14]，跨版本、跨国的轨迹模型因此缺少可逆的表型对齐层。

6. **评测框架与数据治理本身成为独立缺口**。All of Us v9 的家族感知基准通过整家族分组划分发现、校准与测试集，针对跨研究 PRS 可比性与亲属数据泄漏提供评估设计 [84]；UKB PRS Release 发布 28 种疾病和 25 种数量性状评分及基准软件，广泛测试中优于 81 个已发表 PRS [95]。但**面向生成式轨迹模型的公开基准仍缺位**：现有工作多在 MIMIC、UKB、丹麦登记等少数数据上自评，指标（AUC、C-index、F1）与终点定义不统一，且国家级部署因数据访问中断而无法复现 [3]。队列综述亦指出，大型队列正从描述性关联转向机制发现、精细风险分层与遗传导向治疗开发，并日益全球化与多样化 [99]，**但治理与共享模式的差异正在成为跨队列复现的主要摩擦点**。

综合来看，本方向的演化脉络是：从 BEHRT、Med-BERT 的概念序列建模 [15][16]，到 Delphi-2M、ALADYNOULLI 的生成式多病共存建模 [2][1]，再到 Foresight-England 的国家级部署尝试 [3]；与之并行的是蛋白组 pQTL 图谱 [7][22] 与代谢组跨生物库评分 [30] 为轨迹模型提供分子层输入。**核心问题已从“能否预测”转为“预测在谁身上、以何种误差、能否复现”**；相应地，最值得投入的空白是：生物库级别的生成式轨迹公开基准、纵向多组学时钟的双维度评估、生成谱替代真实测量的误差传播分析，以及可逆的跨编码/跨祖源表型对齐层。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 生成式疾病轨迹模型 | 朝阳 | Foresight 用 GPT 式预训练建模患者时间线，证明 EHR 序列可做生成式建模 [19]；2025 年 Nature 工作把「疾病自然史」当作可学习的生成过程 [2]；但 2026 年仍有新的贝叶斯纵向 EHR+遗传框架 [1]，说明建模范式尚未收敛。雷达样本中该节 **n=11、近两年占比 0.9**，属新近爆发但方法未定。 |
| 2.2 多组学与遗传整合 | 成熟 | UK Biobank 血浆蛋白组-遗传关联图谱已成标准参照 [7]；外显子测序与混合模型关联方法早已大规模落地 [6]、[47]；后续多为扩展图谱与泛队列 GWAS [100]。方法收敛、以增量和资源扩展为主。 |
| 2.3 医学 / EHR 基础模型 | 萌芽（偏早期朝阳） | Med-BERT、BEHRT 奠定结构化 EHR 预训练范式 [16]、[15]；但雷达样本中该节 **n=5、CNS 占比 0**，近两年仅见 LLM 提升跨队列迁移 [17] 与表格推理 agent [85]，尚无大规模人群队列上的统一验证。 |
| 2.4 组学衰老时钟与纵向多组学动态 | 朝阳 | 多器官代谢组生物学年龄与心血管代谢结局关联 [87]；纵向蛋白组衰老指数预测死亡与多病 [37]；运动可逆转蛋白组衰老（UKB+干预）[88]。工作新、样本量在上升，但指标定义与验证口径未统一。 |
| 2.5 隐私保护合成基因组与生物样本库规模生成 | 证据不足 | 雷达样本仅 1 篇（HELICS 潜流匹配合成基因组 [90]），不足以判断阶段。 |
| 3 数据与资源 | 成熟 | UK Biobank 资源与深度表型描述已成领域基础设施 [11]、[20]；FinnGen、All of Us 提供跨队列复现底座 [13]、[12]。属稳定供给层。 |
| 4 应用与结果 | 朝阳 | 疾病轨迹深度学习预测胰腺癌风险 [117]；血浆代谢组刻画非传染性疾病多病通路 [106]；多基因评分贯穿生命历程预测 [33]。应用面快速扩张，但多为单点结局验证。 |
| 5 评测、可复现性与争议 | 证据不足 | 雷达样本仅 2 篇：大规模 EHR 贝叶斯 Cox 推断 [115] 与共病 AI 方法综述 [116]，缺少基准/评测框架类实证工作。 |

**整体判断**：这个方向整体处于**朝阳期偏早**——生成式轨迹建模与组学衰老时钟是两条正在爆发但方法未收敛的线（雷达样本中 2.1 近两年占比 **0.9**、2.4 为 **0.8**），而多组学-遗传整合与队列资源层已**成熟**、成为公共底座。窗口期估计 **12–24 个月**：一旦 EHR 基础模型在 UKB/All of Us 上出现统一基准与跨队列复现结果，早期方法学红利会迅速转为增量竞争。最大不确定性有三：**(1)** 生成式轨迹模型缺乏统一评测与跨队列可复现性证据（第 5 节雷达样本仅 **2 篇**）；**(2)** 蛋白组/代谢组衰老时钟的指标定义与验证口径未标准化，易被更大规模图谱淹没；**(3)** 隐私与数据访问限制决定合成数据路线能否成立（2.5 仅 **1 篇**，风险最高）。

**接下来怎么做**：

1. **把「纵向多组学衰老时钟 + 疾病轨迹」做成一个联合模型**：用 UKB 重复测量蛋白组/代谢组 + EHR 诊断序列，输出「个体化衰老轨迹 → 多病发生时间」的生成式预测。现在做是因为两条线各自已有可信起点但尚未合并 [37]、[2]，合并处正是空白。可与你类器官多组学项目对接：用类器官扰动数据做机制先验，人群队列做结局验证。

2. **以「跨队列复现」为方法学卖点切入 EHR 基础模型**：在 UKB 训练、FinnGen/All of Us 外部验证，重点解决迁移与校准而非再刷一个预训练模型 [17]、[13]。现在做是因为该节雷达样本仅 **5 篇、CNS 占比 0**，评测缺口明显，且你有多模态建模能力可直接复用。

3. **做 pQTL/蛋白组 → 衰老表型的机制桥接**：以 UKB 血浆蛋白组 pQTL 图谱为骨架 [7]，把蛋白组衰老指数 [88] 的因果候选基因做孟德尔随机化与共病结构映射 [106]。现在做是因为图谱成熟、增量空间在「从关联到机制」，且能直接产出可复现的公共数据 demo。

4. **搭一个最小评测基准作为公共数据 demo**：针对疾病轨迹生成模型，定义时间切分、跨队列迁移、校准与公平性指标，用 UKB + All of Us 公开派生数据复现 Foresight 类模型 [19]、[2]。现在做是因为第 5 节证据几乎空白（**2 篇**），先发基准易被引用为社区标准。

5. **谨慎押注合成基因组/隐私生成，作为副线而非主线**：以 HELICS 类潜流匹配方法 [90] 在 UKB 规模上做条件合成，评估下游 GWAS/pQTL 保真度。现在做风险高（雷达样本 **1 篇**），建议作为合作项目的数据增广组件，而非独立方向。

## 参考文献

1. A Bayesian framework for longitudinal EHR and genetic discovery. Nature 2026. https://doi.org/10.1038/s41586-026-10780-5
2. Learning the natural history of human disease with generative transformers.. Nature 2025. https://doi.org/10.1038/s41586-025-09529-3
3. Foresight-England: Development of a National-Scale Generative AI Model of Electronic Health Records for Medical Event Prediction across the COVID-19 Pandemic.  2026. https://arxiv.org/abs/2608.16273
4. Predicting Early Functional Decline from Longitudinal Laboratory and Vital Sign Trajectories: A Large-Scale Study Using the All of Us Research Program.  2026. https://arxiv.org/abs/2608.21589
5. LifeLong Digital Twin: A Unified Modeling Paradigm and Agent Harness for Event-Driven Lifelong Health State Trajectories.  . https://arxiv.org/abs/2610.05566
6. Exome sequencing and analysis of 454,787 UK Biobank participants. Nature 2021. https://doi.org/10.1038/s41586-021-04103-z
7. Plasma proteomic associations with genetics and health in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06592-6
8. Sex differences in the genetic regulation of the human plasma proteome.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59034-4
9. All of Us diversity and scale yield context-dependent improvements in polygenic prediction.. Nature Genetics 2026. https://doi.org/10.1038/s41588-026-02734-4
10. Genomic foundation models do not yet boost common variant discovery beyond standard functional annotations.  . https://doi.org/10.64898/2026.10.13.758880
11. UK Biobank: An Open Access Resource for Identifying the Causes of a Wide Range of Complex Diseases of Middle and Old Age. PLoS Medicine 2015. https://doi.org/10.1371/journal.pmed.1001779
12. The “All of Us” Research Program. New England Journal of Medicine 2019. https://doi.org/10.1056/NEJMsr1809937
13. FinnGen provides genetic insights from a well-phenotyped isolated population. Nature 2023. https://doi.org/10.1038/s41586-022-05473-8
14. A unidirectional mapping of ICD-8 to ICD-10 codes, for harmonized longitudinal analysis of diseases. European Journal of Epidemiology 2023. https://doi.org/10.1007/s10654-023-01027-y
15. BEHRT: Transformer for Electronic Health Records. Scientific Reports 2019. https://doi.org/10.1038/s41598-020-62922-y
16. Med-BERT: pretrained contextualized embeddings on large-scale structured electronic health records for disease prediction. npj Digital Medicine 2020. https://doi.org/10.1038/s41746-021-00455-y
17. Large language models improve transferability of electronic health record-based predictions across countries and coding systems.. NPJ digital medicine 2026. https://doi.org/10.1038/s41746-026-02363-5
18. SurvivEHR: a competing risks, time-to-event foundation model for multiple long-term conditions from primary care electronic health records.  2025. https://doi.org/10.1101/2025.08.04.25332916
19. Foresight—a generative pretrained transformer for modelling of patient timelines using electronic health records: a retrospective modelling study. The Lancet Digital Health 2024. https://doi.org/10.1016/s2589-7500(24)00025-6
20. The UK Biobank resource with deep phenotyping and genomic data. Nature 2018. https://doi.org/10.1038/s41586-018-0579-z
21. Whole-genome sequencing of 490,640 UK Biobank participants.. Nature 2025. https://doi.org/10.1038/s41586-025-09272-9
22. Atlas of the plasma proteome in health and disease in 53,026 adults.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.045
23. Longitudinal alignments and syntheses of multimodal clinical data for personalized medicine with the PULSE framework. Nature Computational Science 2026. https://doi.org/10.1038/s43588-026-01026-5
24. Disease prediction with multi-omics and biomarkers empowers case–control genetic discoveries in the UK Biobank. Nature Genetics 2024. https://doi.org/10.1038/s41588-024-01898-1
25. Age-dependent topic modelling of comorbidities in UK Biobank identifies disease subtypes with differential genetic risk. Nature Genetics 2023. https://doi.org/10.1038/s41588-023-01522-8
26. Deep representation learning for clustering longitudinal survival data from electronic health records.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56625-z
27. Subtyping Alzheimer's disease and Parkinson's disease using longitudinal electronic health records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01085-3
28. Using Phecodes for Research with the Electronic Health Record: From PheWAS to PheRS. Annual Review of Biomedical Data Science 2021. https://doi.org/10.1146/annurev-biodatasci-122320-112352
29. The NHGRI-EBI GWAS Catalog: standards for reusability, sustainability and diversity.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1070
30. Metabolomic and genomic prediction of common diseases in 700,217 participants in three national biobanks.. Nature communications 2024. https://doi.org/10.1038/s41467-024-54357-0
31. Global Biobank Meta-analysis Initiative: Powering genetic discovery across human disease. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100192
32. Evaluating Performance and Agreement of Coronary Heart Disease Polygenic Risk Scores.. JAMA 2025. https://doi.org/10.1001/jama.2024.23784
33. Polygenic prediction of body mass index and obesity through the life course and across ancestries.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03827-z
34. Genetically supported targets and drug repurposing for brain aging: A systematic study in the UK Biobank.. Science advances 2025. https://doi.org/10.1126/sciadv.adr3757
35. Age Acceleration and Mortality Risk Constitute Distinct Dimensions of Organ Aging.  . https://doi.org/10.21203/rs.3.rs-10881849/v1
36. Longitudinal dynamics of gene expression and metabolomics in an aging population cohort.. Science 2026. https://doi.org/10.1126/science.aed6452
37. A Novel Longitudinal Proteomic Aging Index Predicts Mortality, Multimorbidity, and Frailty in Older Adults.. Aging cell 2025. https://doi.org/10.1111/acel.70317
38. NOAH: Learning the Full Patient Journey. A Longitudinal Multimodal Time-Aware Model for Representation and Forecasting.  2026. https://arxiv.org/abs/2609.09140
39. EHR-MPC: Inference-Time Control for Sepsis Treatment with Generative Patient Digital Twins. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.08793
40. MiGHT-EHR: A Multi-task Graph Transformer for Heterogeneous Temporal Electronic Health Records.  2026. https://arxiv.org/abs/2608.06430
41. An atlas of genetic associations in UK Biobank. Nature Genetics 2017. https://doi.org/10.1038/s41588-018-0248-z
42. Pan-UK Biobank GWAS improves discovery, analysis of genetic architecture, and resolution into ancestry-enriched effects. medRxiv 2024. https://doi.org/10.1101/2024.03.13.24303864
43. Exome sequencing and characterization of 49,960 individuals in the UK Biobank. Nature 2020. https://doi.org/10.1038/s41586-020-2853-0
44. Advancing human genetics research and drug discovery through exome sequencing of the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-021-00885-0
45. Rare variant contribution to human disease in 281,104 UK Biobank exomes. Nature 2021. https://doi.org/10.1038/s41586-021-03855-y
46. Systematic single-variant and gene-based association testing of thousands of phenotypes in 394,841 UK Biobank exomes. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100168
47. Mixed model association for biobank-scale data sets. Nature Genetics 2018. https://doi.org/10.1038/s41588-018-0144-6
48. A fast and scalable framework for large-scale and ultrahigh-dimensional sparse regression with application to the UK Biobank. bioRxiv 2019. https://doi.org/10.1371/journal.pgen.1009141
49. Deviations from genetic additivity driven by rare variants at biobank scale.. Nature communications . https://doi.org/10.1038/s41467-026-76151-w
50. Functional architecture of rare protein coding variation across 786,871 exomes.  . https://doi.org/10.64898/2026.10.16.26365771
51. Rare variant associations with plasma protein levels in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06547-x
52. Genetic associations with ratios between protein levels detect new pQTLs and reveal protein-protein interactions. bioRxiv 2023. https://doi.org/10.1016/j.xgen.2024.100506
53. Robust cis-by-trans epistasis in the human plasma proteome highlights an ABO-centered interaction network.. American journal of human genetics . https://doi.org/10.1016/j.ajhg.2026.09.003
54. Multi-ancestry MHC-pQTL mapping reveals disease-linked HLA protein networks and shared genetic architecture.  . https://doi.org/10.21203/rs.3.rs-10956233/v1
55. A proteome atlas of structural variation and VNTR effects on complex traits and diseases.  . https://doi.org/10.64898/2026.09.26.26364064
56. Plasma proteome analyses in individuals of European and African ancestry identify cis-pQTLs and models for proteome-wide association studies. Nature Genetics 2022. https://doi.org/10.1038/s41588-022-01051-w
57. Atlas of plasma NMR biomarkers for health and disease in 118,461 individuals from the UK Biobank. Nature Communications 2023. https://doi.org/10.1038/s41467-023-36231-7
58. Genetics of 35 blood and urine biomarkers in the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-020-00757-z
59. MetabHub: an integrative platform for plasma nuclear magnetic resonance metabolomics using mediation analysis, disease prediction, and risk stratification.. Nucleic acids research . https://doi.org/10.1093/nar/gkag1066
60. Identification of plasma proteomic markers underlying polygenic risk of type 2 diabetes and related comorbidities.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56695-z
61. Decomposing polygenic risk of coronary artery disease into distinct biological processes.  . https://doi.org/10.64898/2026.10.08.26365088
62. Multimodal mediators connecting APOE4 to dementia.  . https://doi.org/10.21203/rs.3.rs-11445203/v1
63. GWAS of extended prescription analgesic use identifies genetic loci in chronic pain.. Nature communications 2026. https://doi.org/10.1038/s41467-026-71434-8
64. Integrated multiomic scores for cardiovascular disease prediction across multiancestral populations.  . https://doi.org/10.64898/2026.10.23.26366372
65. Biobank-scale self-supervised genotype pretraining yields transferable representations for human genetics.. Nucleic acids research . https://doi.org/10.1093/nar/gkag1059
66. Global biobank analyses provide lessons for computing polygenic risk scores across diverse cohorts. medRxiv 2021. https://doi.org/10.1101/2021.11.18.21266545
67. Population-specific polygenic risk scores for people of Han Chinese ancestry.. Nature 2025. https://doi.org/10.1038/s41586-025-09350-y
68. Polygenic Prediction of Peripheral Artery Disease and Major Adverse Limb Events.. JAMA cardiology 2025. https://doi.org/10.1001/jamacardio.2025.1182
69. An atlas of polygenic risk score associations to highlight putative causal relationships across the human phenome. bioRxiv 2018. https://doi.org/10.7554/eLife.43657
70. Phenome-wide association studies across large population cohorts support drug target validation. Nature Communications 2018. https://doi.org/10.1038/s41467-018-06540-3
71. Components of genetic associations across 2,138 phenotypes in the UK Biobank highlight adipocyte biology. Nature Communications 2019. https://doi.org/10.1038/s41467-019-11953-9
72. Phenome-wide Burden of Copy Number Variation in the UK Biobank.. American Journal of Human Genetics 2019. https://doi.org/10.1016/j.ajhg.2019.07.001
73. Mono- and biallelic variant effects on disease at biobank scale. Nature 2023. https://doi.org/10.1038/s41586-022-05420-7
74. Integrating the environmental and genetic architectures of aging and mortality.. Nature medicine 2025. https://doi.org/10.1038/s41591-024-03483-9
75. Choice of phenotype scale is critical in biobank-based G × E tests.. Cell genomics . https://doi.org/10.1016/j.xgen.2026.101391
76. Genome-wide detection of genotype-environment interactions at biobank scale with fastGxE.. Nature genetics . https://doi.org/10.1038/s41588-026-02809-2
77. fastGxE is a powerful method for uncovering genotype-environment interactions in biobanks.. Nature genetics . https://doi.org/10.1038/s41588-026-02806-5
78. SPA<sub>GRM</sub>: effectively controlling for sample relatedness in large-scale genome-wide association studies of longitudinal traits.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56669-1
79. Phenome-wide and proteomic analysis of APOE alleles across different ancestries in the All of Us Research Program.  . https://doi.org/10.64898/2026.09.26.26364080
80. Comparative analysis of the Mexico City Prospective Study and the UK Biobank identifies ancestry-specific effects on clonal hematopoiesis.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02085-6
81. Proteomic Signatures Capture Environmental Exposures Across Diverse Populations.  . https://doi.org/10.64898/2026.10.06.26364311
82. Imputation of fluid intelligence scores reduces ascertainment bias and increases power for analyses of common and rare variants.. Nature genetics . https://doi.org/10.1038/s41588-026-02787-5
83. A pre-train and fine-tune framework for adaptive boosting of pre-trained polygenic risk scores.. Nature communications . https://doi.org/10.1038/s41467-026-77128-5
84. A family-aware All of Us benchmark for polygenic prediction and genomic machine learning.  . https://doi.org/10.64898/2026.10.22.26366229
85. EHRAgent: Code Empowers Large Language Models for Few-shot Complex Tabular Reasoning on Electronic Health Records.. Proceedings of the Conference on Empirical Methods in Natural Language Processing. Conference on Empirical Methods in Natural Language Processing 2024. https://doi.org/10.18653/v1/2024.emnlp-main.1245
86. Estimation of physiological aging based on routine clinical biomarkers: a prospective cohort study in elderly Chinese and the UK Biobank.. BMC medicine 2024. https://doi.org/10.1186/s12916-024-03769-2
87. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
88. Reversal of proteomic aging with exercise-results from the UK biobank and a 12-week intervention study.. npj aging 2025. https://doi.org/10.1038/s41514-025-00318-w
89. Molecular Circadian Disturbance in Human Blood Independently Predicts Multi-Disease Risk and Maps to Hepatic metabolism Pathways.  . https://doi.org/10.21203/rs.3.rs-11120748/v1
90. HELICS: Biobank-scale Conditional Synthetic Genome Generation via Latent Flow Matching.  . https://arxiv.org/abs/2610.36361
91. UK Biobank-A Unique Resource for Discovery and Translation Research on Genetics and Neurologic Disease.. Neurology. Genetics 2025. https://doi.org/10.1212/nxg.0000000000200226
92. Robust replication of associations across patient-mediated and provider-sourced EHR data in the All of Us research program. npj Digital Public Health 2026. https://doi.org/10.1038/s44482-026-00032-8
93. Lessons from national biobank projects utilizing whole-genome sequencing for population-scale genomics.. Genomics & informatics 2025. https://doi.org/10.1186/s44342-025-00040-9
94. A national-scale digital atlas of recorded care patterns across more than 1000 diagnostic categories using real-world health data: a retrospective observational study.  . https://doi.org/10.64898/2026.09.16.26363186
95. UK Biobank release and systematic evaluation of optimised polygenic risk scores for 53 diseases and quantitative traits. medRxiv 2022. https://doi.org/10.1101/2022.06.16.22276246
96. Software Application Profile: PHESANT: a tool for performing automated phenome scans in UK Biobank. International Journal of Epidemiology 2017. https://doi.org/10.1093/ije/dyx204
97. Exploring and visualizing large-scale genetic associations using PheWeb. Nature Genetics 2020. https://doi.org/10.1038/s41588-020-0622-5
98. Quality control and removal of technical variation of NMR metabolic biomarker data in ~120,000 UK Biobank participants. Scientific Data 2021. https://doi.org/10.1038/s41597-023-01949-y
99. Trends in large-scale human population cohorts.. Trends in Genetics 2026. https://doi.org/10.1016/j.tig.2026.08.002
100. Pan-UK Biobank genome-wide association analyses enhance discovery and resolution of ancestry-enriched effects.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02335-7
101. MSGene: a multistate model using genetic risk and the electronic health record applied to lifetime risk of coronary artery disease. Nature Communications 2024. https://doi.org/10.1038/s41467-024-49296-9
102. Dynamic Importance of Genomic and Clinical Risk for Coronary Artery Disease Over the Life Course. medRxiv 2023. https://doi.org/10.1101/2023.11.03.23298055
103. Machine Learning‐Driven Prediction of Coronary Artery Disease Risk Based on UK Biobank Plasma Proteomics. Journal of the American Heart Association : Cardiovascular and Cerebrovascular Disease 2026. https://doi.org/10.1161/JAHA.125.047248
104. Proteomics mediates the effects of biological aging on the progression of cardio-renal-metabolic comorbidity: a UK biobank cohort study.. Cardiovascular diabetology 2025. https://doi.org/10.1186/s12933-025-03035-6
105. MetaboHealth and Metabolic Vulnerability Index as Risk Factors for Cardio-Renal-Metabolic Multimorbidity: A Large-Scale Prospective Cohort Study.. Diabetes, obesity and metabolism 2026. https://doi.org/10.1111/dom.71112
106. Plasma metabolites to profile pathways in noncommunicable disease multimorbidity. Nature Medicine 2021. https://doi.org/10.1038/s41591-021-01266-0
107. NMR metabolomics for cardiovascular-kidney-metabolic risk stratification in an integrated healthcare system.  . https://doi.org/10.64898/2026.10.01.26364322
108. UKB-MDRMF: a multi-disease risk and multimorbidity framework based on UK biobank data.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58724-3
109. PheMIME: an interactive web app and knowledge base for phenome-wide, multi-institutional multimorbidity analysis.. Journal of the American Medical Informatics Association : JAMIA 2024. https://doi.org/10.1093/jamia/ocae182
110. Leveraging large-scale biobank EHRs to enhance pharmacogenetics of cardiometabolic disease medications.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58152-3
111. Deep phenotyping of heart failure with preserved ejection fraction through multi-omics integration.. European journal of heart failure 2025. https://doi.org/10.1002/ejhf.70041
112. Large-scale plasma proteomic profiling enhances prediction of heart failure among hypertensive individuals: prospective insights from the UK Biobank.. Journal of global health . https://doi.org/10.7189/jogh.16.04313
113. Explainable Plasma Proteomics–Based Machine Learning for Osteoporosis Diagnosis, Prognosis, and Protein Biomarker Discovery in the UK Biobank. The FASEB Journal 2026. https://doi.org/10.1096/fj.202600647R
114. Generalizability of proteomic risk prediction across biobanks reveals dependence on phenotype definitions.  . https://doi.org/10.64898/2026.10.01.26364038
115. Bayesian Cox regression for large-scale inference with applications to electronic health records. Annals of Applied Statistics 2021. https://doi.org/10.1214/22-aoas1658
116. From data to knowledge: artificial intelligence methods for studying comorbidity in electronic health records. The European Physical Journal Special Topics 2026. https://doi.org/10.1140/epjs/s11734-026-02571-w
117. A deep learning algorithm to predict risk of pancreatic cancer from disease trajectories. Nature Medicine 2023. https://doi.org/10.1038/s41591-023-02332-5
