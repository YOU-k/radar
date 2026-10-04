# 人群健康与多组学 AI · 方向背景报告

证据 100 篇 · 覆盖度 0.83 · 第 9 轮 · 更新 2026-10-04 · 数字核验删句 1

## 本次变更

- 新增 [56] Phenome-wide and proteomic analysis of APOE alleles across different ancestries in the All of Us Research Program
- 新增 [75] Age Acceleration and Mortality Risk Constitute Distinct Dimensions of Organ Aging
- 新增 [59] A pre-train and fine-tune framework for adaptive boosting of pre-trained polygenic risk scores.
- 新增 [10] Deviations from genetic additivity driven by rare variants at biobank scale.
- 新增 [89] Generalizability of proteomic risk prediction across biobanks reveals dependence on phenotype definitions
- 新增 [93] NMR metabolomics for cardiovascular-kidney-metabolic risk stratification in an integrated healthcare system

## 摘要（TL;DR）

- 生成式疾病轨迹模型正从单病种、结构化数据转向多病共存、多模态、终身轨迹联合建模，ALADYNOULLI 在 3 个生物库、n>683,000、随访 52 年、348 种疾病上识别出 21 个可复制特征 [1]
- Foresight 整合结构化数据与占约 80% 的自由文本，支持跨日/周/月预测与死亡前全程模拟，但作者强调当前形式不宜直接用于临床决策支持 [2]
- NOAH 基于 MIMIC 家族 559M 事件、299,000 患者训练，支持自回归预测、零样本分类与反事实干预模拟，但其外部泛化待验证 [3]
- Foresight-England 作为首个国家级 EHR 生成式基础模型，采用 243M 参数 Transformer 解码器，但因 NHS England 暂停数据访问，定量结果无法导出 [4]
- 一项基于 All of Us 297,861 人、12 项生物标志物 3 年轨迹特征的研究用 LightGBM 建模，轨迹模型 AUROC 0.797 显著优于静态汇总 0.755（P<0.001），但缺乏外部队列验证 [5]
- UK Biobank Pharma Proteomics Project 对 54,219 人检测 2,923 种蛋白，发现 14,287 个主要遗传关联，81% 为既往未报道 [6]
- 跨祖源方面，ARIC 中 7,213 名欧裔和 1,871 名非裔的 4,657 种蛋白 cis-pQTL 定位显示多数关联共享，但非裔样本可缩小可信集并发现人群特异位点 [7]
- 在 All of Us、Penn Medicine 与 UCLA 生物库 171,095 人中计算 48 个冠心病 PRS，发现群体预测表现相似的 PRS 在个体层面一致性差（ICC 与 Light κ 低），提示临床使用需谨慎 [8]
- 综合来看，多组学与遗传整合已从单一组学关联走向跨分子层、跨祖源、跨队列的系统映射，但欧洲祖源主导、个体级 PRS 一致性差、非加性效应与上位效应尚待功能验证等争议仍未解决 [8][9][10]
- 纵向多组学研究的核心进展是把衰老时钟从单时点快照推向轨迹建模，Science 的 8 年随访对 335 名女性的全血基因表达和代谢组做纵向分析，发现 5,061 个基因和 181 个代谢物随时间变化 [11]

## 1 背景与定义

人群健康与多组学 AI 的边界，首先由数据资源的规模与结构决定。**UK Biobank** 在 2006—2010 年招募 50 万名 40—69 岁参与者，收集遗传与非遗传决定因素，并预计 20 年随访累积糖尿病约 68,000 例、心梗与冠心病死亡 47,000 例、卒中 20,000 例、阿尔茨海默病 30,000 例 [12]；其基因型数据经质控与单倍型估计后插补约 9600 万变异，并通过身高 GWAS 和 HLA-疾病关联复制验证质量 [13]。测序深度进一步从芯片插补推进到全基因组：490,640 名参与者完成平均 32.5× WGS，识别约 15 亿变异，较插补芯片增 18.8 倍、较 WES 增 >40 倍，其中 93.5% 为非芬兰欧洲 ancestry [14]。与之互补，**FinnGen** 基于 224,737 人插补基因型和 1,932 个终点，利用隔离人群富集低频有害等位，在既往研究充分的疾病中识别新的低频变异关联 [15]；**All of Us** 则针对多样性不足设计，拟招募至少 100 万名多样化参与者，截至 2019 年 7 月已有 >175,000 人贡献生物样本，其中 >80% 来自历史上研究不足群体 [16]。这三类资源分别代表规模覆盖、隔离人群定位分辨率与祖源多样性三种取向，**但欧洲祖源主导、随访时序与数据通路差异仍是共同约束** [14][15][16]。

在表型与编码层面，方向的核心问题从「能否关联」转向「能否跨版本、跨系统、跨机构复用」。Phecodes 基于 ICD 编码定义数千种临床有意义疾病的病例/对照状态，从 PheWAS 扩展到表型风险评分，但依赖 ICD 编码，存在编码误差与表型异质性 [17]。跨版本障碍由 ICD-8 到 ICD-10 的单向映射部分缓解，该映射覆盖完整 ICD 及丹麦本地扩展，可连接 1965 年以来超半世纪医疗数据，但未提供反向映射 [18]。自动化扫描方面，PHESANT 用规则算法为 UK Biobank 连续、整数和分类变量自动选择统计检验并执行全表型关联，但依赖 UKB 变量规则 [19]；PheWeb 聚焦结果呈现，整合 Manhattan、LocusZoom 与 PheWAS 视图，但不含统计建模功能 [20]。**表型定义的标准化程度，直接决定多组学模型能否跨队列复现**，这也是后续生成式轨迹模型与遗传发现共享的前置条件 [21]。

从演化脉络看，该方向经历了「单组学关联 → 多组学图谱 → 生成式轨迹建模 → 跨祖源与个体级验证」的递进。早期工作以大规模关联图谱为主：UKB 118,461 人的 249 个 NMR 代谢指标与 700 多种疾病的患病、发病和死亡关联在 THL Biobank 3 万余人重复验证 [22]；血浆蛋白图谱在 53,026 人中关联 406 种现患和 660 种新发疾病及 986 种健康性状，报告 168,100 个蛋白-疾病关联和 554,488 个蛋白-性状关联，183 种疾病判别 AUC>0.80，并通过 pQTL 确定 474 个因果蛋白及 37 个药物重定位机会 [23]。随后方法学转向整合建模：MILTON 用常规临床生物标志物、血浆蛋白和定量性状预测 3,213 种疾病，扩充病例队列后发现多个基线未显著的新基因-表型关联 [24]；PULSE 纵向自监督框架从稀疏常规血检生成代谢组和蛋白质组，生成代谢组优于所有基准，生成蛋白质组对 6 种常见病 AUC 达 0.72–0.83，接近真实蛋白质组 [25]。**这一脉络的主线，是把分子层从「关联标签」转为「可生成、可干预、可跨队列对齐的中间表型」** [23][24][25]。

共病结构与疾病亚型识别构成另一条独立线索，其方法从主题模型、遗传矩阵分解延伸到生成式贝叶斯框架。年龄依赖主题模型 ATM 在 UKB 282,957 样本中识别 52 种共病异质性疾病，并在 All of Us 211,908 样本验证，18 个亚型的 PRS 显著异于同病其他亚型 [26]。DeGAs 对 2,138 个 UKB 表型的遗传关联矩阵做截断 SVD，100 个成分解释 41.9%/62.8%/75.5% 方差，PTV 富集肥胖性状并突出脂肪细胞生物学 [27]。FinnGen 176,899 人的隐性关联扫描在标准加性 GWAS 之外揭示同一变异杂合与纯合状态可呈现不同疾病表型 [28]；CNV 全表型分析在 472,228 人中刻画 16p11.2、22q11.2、9p23 等位点效应 [29]。**这些工作共同表明，共病不是单病的简单叠加，而是具有可遗传的低秩结构**，但亚型定义依赖编码粒度与聚类超参，跨系统稳定性仍需检验 [26][27]。

当前方向的核心争议集中在三处。其一是**个体级 PRS 一致性**：在 All of Us、Penn Medicine 与 UCLA 生物库 171,095 人中计算 48 个冠心病 PRS，发现群体预测表现相似的 PRS 在个体层面一致性差（ICC 与 Light κ 低），提示临床使用需谨慎 [8]。其二是**非加性效应与上位效应**：正交等位基因重编码框架在不依赖 Hardy-Weinberg 假设下检验非加性效应，分析最多 399,943 名 UKB 个体、2,906 个血浆蛋白和 55 个数量性状，发现约三分之一同源基因-蛋白关系表现非线性剂量效应，方法在 HWE 偏离下保持校准（λGC=0.94），而标准重编码膨胀至 λGC=78.3 [10]。其三是**跨祖源泛化**：GBMI 覆盖 23 个生物样本库、220 万人、14 个疾病终点，统一表型与质控后提升发现能力，但祖先代表性仍不均 [9]；All of Us 245,388 全基因组序列与 UKB 联合开发 32 个性状多血统 PRS，发现增加多样性提升部分性状精度，但最大化样本量并非普遍最优 [30]；台湾 TPMI 463,447 名汉族人的全表型 GWAS 与 PRS 建模在 TWB、UKB、All of Us 验证，证明汉族特异 PRS 优于欧洲为主模型 [31]。**这三类争议指向同一结论：多组学与遗传整合的发现能力已大幅扩张，但从群体统计到个体决策、从欧洲祖源到全球人群的转化路径尚未打通** [8][10][9]。

综合而言，人群健康与多组学 AI 的定义边界可概括为：以万人级以上人群队列与生物样本库为数据底座，以 EHR 纵向轨迹、胚系遗传、血浆蛋白组/代谢组/甲基化等多组学为输入，以生成式预测、共病结构发现、亚型识别与跨队列复现为目标。其演化脉络从单组学关联图谱，经多组学整合与共病低秩建模，走向生成式终身轨迹模拟与跨祖源验证；核心问题则从「关联是否显著」转为「轨迹能否生成、亚型能否复现、评分能否个体化、效应能否跨祖源迁移」。**当前最突出的空白，是缺乏统一的跨队列、跨祖源、跨模态评测框架**，使生成式模型、多组学图谱与 PRS 工具之间的性能无法直接比较 [32][21]。

## 2 方法学


### 2.1 生成式疾病轨迹模型

生成式疾病轨迹模型正从单病种、结构化数据建模，转向对多病共存、多模态、终身轨迹的联合建模。ALADYNOULLI 以贝叶斯生成框架联合建模纵向 EHR 诊断、年龄与多基因风险，采用概率混合而非混合概率的形式处理同时性与慢性病，在 3 个生物库、**n>683,000**、随访 52 年、348 种疾病上识别出 **21 个可复制特征**，跨队列组成保留中位 80%，亚型 Cohen's d 达 4.25，基于特征的 GWAS 发现 **151 个全基因组显著位点**，包括单性状分析遗漏的心血管关联 [1]。两者都强调从孤立疾病转向共病轨迹，但前者侧重遗传发现与亚型，后者侧重终身风险模拟。

在数据模态与时间分辨率上，工作间差异明显。Foresight 整合结构化数据与占约 **80% 的自由文本**，覆盖 18 类 SNOMED 概念，支持跨日/周/月预测与死亡前全程模拟，但作者强调当前形式不宜直接用于临床决策支持 [2]。NOAH 进一步原生处理图像、时序、分类及文本记录，采用双向时间整合与变分隐空间，基于 MIMIC 家族 **559M 事件、299,000 患者**训练，支持自回归预测、零样本分类与反事实干预模拟，但其外部泛化待验证 [3]。MiGHT-EHR 走异质图路线，基于归一化 PMI 构建异质时序图，用带时序注意力的图 Transformer 自监督预训练，在 MIMIC-III/IV 四任务上平均超越 SOTA，死亡率与再入院提升尤为显著 [33]。这些模型在模态覆盖与任务通用性上各有取舍，尚无统一评测。

轨迹建模也被用于治疗决策与亚型发现。EHR-MPC 将脓毒症治疗优化转化为推理时控制问题，训练生成式 EHR 患者数字孪生预测干预下轨迹，再用模型预测控制规划治疗，在 Mass General Brigham 8 家医院 ICU 队列上离线策略性能与 RL 相当、模拟性能更优 [34]。VaDeSC-EHR 用基于 Transformer 的变分自编码器结合 Weibull 混合生存分布，将风险建模与聚类直接整合，识别兼具不同诊断轨迹和时间-事件特征的患者亚群 [35]。AD/PD 亚型研究将诊断前时间戳 EHR 按就诊、年龄和日历年标记化，用 Transformer 嵌入加 K-means 聚类，在 CPRD Aurum 与 UK Biobank 上各识别出 **5 个可复制亚型**，5 年随访显示亚型间死亡和住院预后差异并与基因型关联 [36]。

方法学上仍有明显张力与空白。Foresight-England 作为首个国家级 EHR 生成式基础模型，采用 **243M 参数** Transformer 解码器，基于约 6100 万人纵向 EHR（训练 5490 万、评估 610 万）自回归预测下一医疗事件，但因 NHS England 暂停数据访问，定量结果无法导出，仅提供分词、架构、训练、推理与评估策略作为方法学模板 [4]。与之相对，一项基于 All of Us **297,861 人**、12 项生物标志物 3 年轨迹特征的研究用 LightGBM 建模，轨迹模型 AUROC **0.797** 显著优于静态汇总 0.755（P<0.001），匹配分析 0.727 vs 0.680，并可提前 3-12 个月持续预测，但缺乏外部队列验证 [5]。这提示：生成式模型在规模与通用性上扩张，而轻量轨迹特征在特定预警任务上仍有竞争力；同时多数工作依赖登记编码或单一数据集，记录偏倚与外部泛化是共同争议点 [1][37][3]。

### 2.2 多组学与遗传整合

**大规模外显子测序**把罕见编码变异推到了多组学整合的前台。UK Biobank 首批 49,960 人外显子数据释放约 400 万编码变异，其中约 98.6% 频率低于 1%，含 198,269 个常染色体预测功能缺失（LOF）变异，较插补序列增加逾 14 倍 [38]。随后 UKB-ESC 将首批 200,643 人数据开放，约 1000 万变异中约 800 万为编码变异，LOF 达 453,733 个 [39]。在 454,787 人、3,994 个健康表型上，REGENIE 基因负荷分析发现 **8,865 个显著关联**，涉及 564 个基因、492 个表型、2,283 个基因-表型对，其中 91% 不能由常见变异 LD 解释，81% 可复制 [40]。另一项 281,104 人外显子研究覆盖 17,361 个二分类和 1,419 个定量表型，识别 632 个全基因组显著 ExWAS 变异，并刻画 PTV 携带谱：96% 基因有杂合 PTV，20% 有纯合/半合 PTV [41]。394,841 名欧洲裔外显子上则系统测试了 8,074,878 个单变异和 75,767 个基因-注释组 × 4,529 表型，并公开全 summary statistics 浏览器 [42]。这些工作共同表明，**罕见编码变异**贡献了 GWAS 难以捕获的遗传结构，但三项研究均以欧洲裔为主（约 95%），非欧洲分辨率有限 [40][41][42]。

**血浆蛋白质组**成为连接遗传变异与疾病的核心中间层。UK Biobank Pharma Proteomics Project 对 54,219 人检测 2,923 种蛋白，发现 14,287 个主要遗传关联，**81% 为既往未报道**，精细映射出 29,420 个独立信号，并揭示 ABO 与 FUT2 对胃肠道表达蛋白的远距离上位效应 [6]。同一队列的罕见变异分析在 49,736 人中识别 5,433 个罕见基因型-蛋白关联（81% 为既往 GWAS 未检出）和 1,962 个基因水平关联，STAB1/STAB2 分别关联 77 和 41 个蛋白，PTV 信号 99.4% 与蛋白降低相关 [43]。跨祖源方面，ARIC 中 7,213 名欧裔和 1,871 名非裔的 4,657 种蛋白 cis-pQTL 定位显示多数关联共享，但非裔样本可缩小可信集并发现人群特异位点 [7]；MHC 区多祖先映射在 2,920 种蛋白中鉴定 13 个 cis、606 个 trans 关联，多数跨祖先一致，并发现东亚 EDAR 祖先富集关联 [44]。蛋白比值 GWAS 进一步扩展了信号空间：利用 Olink 1,463 种蛋白、54,000 余样本复制 4,248 个 rQTL，覆盖 2,821 个蛋白对，p-gain 显著蛋白对富集已知互作 7.6 倍，比值 GWAS 较单蛋白 GWAS 新增 24.7% 遗传信号 [45]。上位效应层面，UKB-PPP 数据映射出以 **ABO 为中心**的稳健 cis-by-trans 互作网络 [46]。性别维度上，整合 Fenland 与 UKB 共 5,823 种蛋白发现 69.1% 蛋白存在性别差异，男性偏高占 62.1%/63.8%，而激素和 BMI 等仅解释 15.3%/20.5%，遗传效应对蛋白靶点则跨性别高度相似，仅 103 个 sd-pQTL [47]。

**代谢组与蛋白组图谱**将分子层与疾病谱系统对接。UKB 118,461 人的 249 个 NMR 代谢指标与 700 多种疾病的患病、发病和死亡关联图谱在 THL Biobank 3 万余人重复验证 [22]。三国生物库 700,217 人的 NMR 代谢组评分训练 12 种高 DALY 疾病 Cox 模型，多数纳入超过半数 36 个代谢标志物，并实现跨库重复 [48]。血浆蛋白图谱在 53,026 人中关联 406 种现患和 660 种新发疾病及 986 种健康性状，报告 168,100 个蛋白-疾病关联和 554,488 个蛋白-性状关联，183 种疾病判别 AUC>0.80，并通过 pQTL 确定 474 个因果蛋白及 37 个药物重定位机会 [23]。这些图谱的共同局限是人群代表性有限、缺乏外部验证 [23][22]。

**多基因评分与分子表型的整合**是本节另一条主线。T2D 全基因组 PGS 在 UKB-PPP 中关联 648 个蛋白，其中 617 个复制，分区 PGS 则关联不同生物过程的蛋白 [49]。35 项血尿标志物的 GWAS 在 363,228 人中识别 5,794 个独立位点和 3,374 个精细映射关联，MR 推断 51 个因果关系，多 PRS 模型在 FinnGen 中改善慢性肾病、2 型糖尿病、痛风和酒精性肝硬化的风险分层 [50]。162 个 PRS 与 551 个表型的 89,262 次检验构建了人类表型组 PRS 关联图谱，但作者强调 PRS 受水平多效性影响，关联不等于因果 [51]。方法学上，BOLT-LMM 在 UKB 全部 459K 欧洲样本上运行，身高等效 650K 样本（有效样本 +93%），23 性状独立位点从 5,839 增至 10,759（+84%）[52]；BASIL 则针对约 50 万人、>80 万 SNP 的超大规模稀疏回归解决内存瓶颈 [53]。

**跨祖源与人群特异**是当前最突出的争议点。GBMI 覆盖 23 个生物样本库、220 万人、14 个疾病终点，统一表型与质控后提升发现能力，但祖先代表性仍不均 [9]。PRS 构建方法比较显示 **PRS-CS 总体优于 P+T**，且欧洲 LD 面板预测精度相当或更高，主因是 GBMI 参与者仍以欧洲祖源为主 [54]。All of Us 245,388 全基因组序列与 UKB 联合开发 32 个性状多血统 PRS，发现增加多样性提升部分性状精度，但最大化样本量并非普遍最优，多血统训练可减缓随血统分歧的精度衰减 [30]。台湾 TPMI 463,447 名汉族人的全表型 GWAS 与 PRS 建模在 TWB、UKB、All of Us 验证，证明汉族特异 PRS 优于欧洲为主模型 [31]。Pan-UKB 跨祖源荟萃分析覆盖 7,271 个表型，新发现 14,676 个仅欧洲祖源分析未检出的位点 [55]。APOE 全表型组研究在 All of Us 367,757 人、六个祖源群体中识别 27 个相关表型，5 个脂质性状女性效应更大，9 个关联具祖源特异性 [56]。MCPS 与 UKB 比较则发现克隆性造血在 MCPS 显著更少（校正 OR=0.59），且 CH 频率与欧洲祖源比例正相关（校正 beta=0.84）[57]。

**疾病亚型与共病结构**提供了另一类整合视角。年龄依赖主题模型 ATM 在 UKB 282,957 样本中识别 52 种共病异质性疾病，并在 All of Us 211,908 样本验证，18 个亚型的 PRS 显著异于同病其他亚型 [26]。DeGAs 对 2,138 个 UKB 表型的遗传关联矩阵做截断 SVD，100 个成分解释 41.9%/62.8%/75.5% 方差，PTV 富集肥胖性状并突出脂肪细胞生物学 [27]。FinnGen 176,899 人的隐性关联扫描在标准加性 GWAS 之外揭示同一变异杂合与纯合状态可呈现不同疾病表型 [28]。CNV 全表型分析在 472,228 人中刻画 16p11.2、22q11.2、9p23 等位点效应 [29]。

**方法学创新**持续处理生物库规模数据的统计与计算挑战。SPA_GRM 通过回顾性策略控制样本亲缘关系，在 UKB 79 个纵向性状中识别 7,463 个遗传位点 [58]。正交等位基因重编码框架在不依赖 Hardy-Weinberg 假设下检验非加性效应，分析最多 399,943 名 UKB 个体、2,906 个血浆蛋白和 55 个数量性状，发现约三分之一同源基因-蛋白关系表现非线性剂量效应，方法在 HWE 偏离下保持校准（λGC=0.94），而标准重编码膨胀至 λGC=78.3 [10]。AB-PRS 预训练微调框架在模拟中预测性能普遍优于 PRS(basic)、PRS-CS、LDpred、MegaPRS 等基线，噪声选择比例 <28%，重要预测因子选择 >50% [59]。PULSE 纵向自监督框架从稀疏常规血检生成代谢组和蛋白质组，生成代谢组优于所有基准，生成蛋白质组对 6 种常见病 AUC 达 0.72–0.83，接近真实蛋白质组 [25]。

**临床转化与靶点验证**方面，MILTON 用常规临床生物标志物、血浆蛋白和定量性状预测 3,213 种疾病，扩充病例队列后发现多个基线未显著的新基因-表型关联 [24]。脑龄差 GWAS 发现 2 个新位点和 7 个已知位点，整合 MR 与共定位优先 7 个可成药基因，重发现 13 种有临床试验证据的潜在药物 [60]。暴露组全关联研究识别 25 个独立环境暴露，量化其对死亡和 25 种年龄相关病的贡献常高于基因组 [61]。跨队列 PheWAS 在最多 697,815 人中检验 19 个候选药物靶点，证明可识别多效性并提示疗效或安全性信号 [62]。慢性疼痛处方 GWAS 在 UKB 与 FinnGen 各约 50 万人中识别 140 个全基因组关联，78 个为新发现 [63]。

**PRS 的个体级一致性**构成对临床应用的直接警示。在 All of Us、Penn Medicine 与 UCLA 生物库 171,095 人中计算 48 个冠心病 PRS，发现群体预测表现相似的 PRS 在个体层面一致性差（ICC 与 Light κ 低），提示临床使用需谨慎 [8]。外周动脉疾病 PRS-PAD 在 UKB 400,533、AoU 218,500、MGBB 32,982 人中与 PAD 及主要肢体不良事件显著关联，支持高危个体识别，但摘要未给出完整 AUC/OR 数值 [64]。GeneATLAS 汇总 452,264 名 UKB 欧洲裔参与者的 118 个连续和 660 个二分类性状，支持查询 9,113,133 个遗传变异关联 [65]。

综合来看，多组学与遗传整合已从单一组学关联走向**跨分子层、跨祖源、跨队列**的系统映射，但欧洲祖源主导、个体级 PRS 一致性差、非加性效应与上位效应尚待功能验证等争议仍未解决 [8][9][10]。

### 2.3 医学 / EHR 基础模型

医学 EHR 基础模型的技术路线经历了从序列建模到预训练、再到跨系统迁移与生成式时间事件建模的演进。**BEHRT** 将 Transformer 用于结构化 EHR，把患者历史视为医学概念序列，并结合就诊位置、年龄与事件顺序学习个体表示以预测未来诊断，在多项任务中优于 Deepr、RNN、LSTM、RETAIN 等基线 [66]。**Med-BERT** 进一步把 BERT 迁移到 ICD 诊断序列，先在大规模数据上自监督预训练再微调，在糖尿病、心衰等预测任务上优于 BEHRT、G-BERT 及任务内训练模型，且在标注样本有限时提升更明显 [67]。两者共同确立了「预训练+微调」范式，但均仅依赖诊断编码，未纳入药物与检验信息，跨机构泛化也未充分验证 [66][67]。

针对跨系统迁移这一核心争议，**GRASP** 用大语言模型将医学编码映射到共享语义空间并结合 transformer 预测，在 UKB 391921、FinnGen 253991、Mount Sinai 386755 人数据上，平均 ΔC-index 较语言无关模型在芬兰高 88%、美国高 47%，且 62% 疾病与 PRS 相关性显著更高，未统一数据模型仍稳健 [68]。与之不同，**SurvivEHR** 面向多长期病症共病，采用竞争风险时间事件预训练目标，基于英国初级保健 2300 万患者、76 亿编码事件，风险分层超越基准生存模型并支持低资源微调迁移，但外部多国泛化未验证 [69]。**EHRAgent** 则转向应用交互层，以 LLM 智能体自主生成并执行代码进行多表 EHR 推理，在三个真实数据集上成功率超最强基线 29.6%，少样本即可完成复杂临床任务，但依赖代码执行反馈迭代 [70]。可见，语义嵌入迁移与时间事件建模分别回应了跨编码系统与共病时序两类挑战，而编码覆盖范围、外部泛化与可解释性仍是共同未决问题。

### 2.4 组学衰老时钟与纵向多组学动态

纵向多组学研究的核心进展，是把衰老时钟从单时点快照推向轨迹建模。Science 的 8 年随访对 **335 名女性**的全血基因表达和代谢组做纵向分析，发现 **5,061 个基因和 181 个代谢物**随时间变化，且个体轨迹常偏离群体趋势，这些基因具细胞类型特异性并富集于心血管代谢和神经退行性疾病通路 [11]。该研究同时指出，分子水平受遗传、昼夜节律、季节和污染物影响 [11]。与之呼应，UK Biobank 中 420,746 人的 312 种血液分子分析显示，用贝叶斯加性回归树推导的节律紊乱指标基本独立于睡眠，可独立预测 **98 种**未来发病风险并映射到肝脏代谢通路 [71]。这两项工作共同提示，纵向动态中的时间结构（个体轨迹、昼夜节律）本身携带独立于静态水平的疾病预测信息，但前者样本量和性别代表性有限，后者仅为观察性关联、未明确因果机制。

在蛋白组层面，纵向时钟与横断面时钟的差异被直接检验。ARIC 研究基于三次访视的 4,684 个血浆蛋白，用 FPCA 加 Cox 弹性网构建纵向蛋白衰老指数 **LPAI**，并在 MESA 验证，结果显示 LPAI 同时捕捉衰老累积负担和变化速度，较单时点蛋白时钟提供额外预测信息 [72]。干预方向上，UK Biobank 45,438 人分析发现体力活动越高 ProtAgeGap 越低，ProtAgeGap 与 2 型糖尿病风险 HR=1.06，高活动交互 HR=1.05；在 26 名男性的 12 周监督运动研究中，ProtAgeGap 下降相当于 10 个月，204 个评分蛋白多数稳定，但 CLEC14A 等随运动改变并与胰岛素敏感性改善相关 [73]。需注意后者干预样本量小、以观察性关联为主，其"逆转"幅度不能与 LPAI 的预测增益直接比较。

代谢组与多器官框架则把时钟扩展到器官分辨率和维度可分性。UK Biobank 274,247 人的 107 个血浆非衍生代谢物被用于构建 5 个器官特异性 MetBAG，独立测试 Pearson r 为 0.25–0.42，关联 525 个疾病终点并预测 14 类疾病与死亡风险，SNP 遗传力估计为 0.09<hSNP2<0.18 [74]。另一项 UK Biobank 409,206 人、14 个器官的研究整合 NMR 代谢组、Olink 蛋白组和临床表型，发现年龄加速与死亡风险是器官生物学的不同维度，具有可分离的表型、分子和遗传结构 [75]。此外，DFTJ 中国老年人队列用 36 项常规临床指标经限制立方样条 Cox 构建生理衰老指数 PAI/ΔPAI，捕捉 U 型关系，并在 UK Biobank 中验证其预测死亡、心血管病及 9 种慢性病风险 [76]。这些工作的方法学分歧在于：以死亡为标签还是以年龄为标签、单器官还是多器官、横断面还是纵向，而"年龄加速"与"死亡风险"是否同一维度，正是 [75] 与既往单维时钟之间的核心争议。

## 3 数据与资源

大型前瞻性队列仍是人群健康多组学研究的骨干资源。**UK Biobank** 在2006—2010年间招募50万名40—69岁参与者，收集中老年复杂疾病的遗传与非遗传决定因素，并预计20年随访期间累积糖尿病约68,000例、心梗与冠心病死亡47,000例、卒中20,000例、阿尔茨海默病30,000例 [12]。其深度表型覆盖生物测量、生活方式、血尿生物标志物及身体与脑影像，随访依靠健康与医疗记录链接，全基因组基因型数据经质控、单倍型估计后插补约9600万变异，并通过身高GWAS和HLA-疾病关联复制验证数据质量 [13]。该队列已超8000家机构使用、发表8000余篇论文，且人类遗传证据支持的药物获批概率高2倍以上 [77]。局限在于参与者相对健康、以欧洲ancestry为主，且40—69岁的年龄范围为折中，可能影响暴露与结局时序 [12][13]。

测序深度正从芯片插补推进到全基因组。UK Biobank对490,640名参与者完成平均32.5×的全基因组测序，识别约15亿变异，较插补芯片增18.8倍、较全外显子测序增>40倍，其中93.5%为非芬兰欧洲ancestry [14]。FinnGen则走隔离人群路线，基于224,737人插补基因型和1,932个终点开展GWAS与精细定位，发现芬兰隔离人群富集低频有害等位，并能在既往研究充分的疾病中识别新的低频变异关联和可能因果编码变异 [15]。两者设计取向不同：前者以规模与变异覆盖取胜，后者以隔离人群的低频等位富集提高定位分辨率，但芬兰遗传结构特殊，结果外推受限 [15]。多国生物样本库综述进一步指出，WGS可发现罕见变异、结构变异和调控元件，但计算基础设施、隐私伦理、临床整合和祖先多样性不足仍是共同挑战 [78]。

多样性不足是现有资源被反复指出的短板，All of Us 正是针对这一问题的设计。该计划拟在美国招募至少100万名多样化参与者，截至2019年7月已有>175,000人贡献生物样本，其中>80%来自历史上研究不足群体，34个站点收集>112,000人的EHR数据 [16]。但该计划当时仍处招募早期，长期随访和数据完整性有待建立 [16]。在EHR来源层面，All of Us内部对393,590名参与者的比较显示，患者介导EHR（PME，19,703人）与提供者来源EHR（HPO，373,887人）在人群特征、测序覆盖和关联复制上存在差异：PME人群更白、更女性、更多保险、随访更长，而WGS覆盖更少（35.2% vs 83.2%）[79]。这提示同一队列内不同数据通路的研究效用并不等价，PME样本量小且人群构成差异大，可能影响泛化和比较 [79]。

表型定义的标准化工具决定了这些资源能否被高效复用。Phecodes基于ICD编码，可快速定义数千种临床有意义疾病和状况的病例/对照状态，最初用于PheWAS，后扩展到表型风险评分等方法，但依赖ICD编码，可能存在编码误差和表型异质性 [17]。跨版本编码是纵向研究的另一障碍：一项工作构建了ICD-8到ICD-10的单向映射，覆盖完整ICD及丹麦本地扩展，可连接1965年以来超半世纪的医疗数据，但未提供ICD-10回映射ICD-8 [18]。在自动化扫描方面，PHESANT用规则算法为UK Biobank的连续、整数和分类变量自动选择合适统计检验，执行全表型关联并输出图表，但依赖UKB变量规则，自动化模型可能不适用于所有复杂表型 [19]。PheWeb则聚焦结果呈现，整合Manhattan、LocusZoom和PheWAS视图，支持单性状与多性状视图切换，已用于UKB等数据集，但不含统计建模功能 [20]。

关联结果的集中归档与评分发布构成下游复用基础。NHGRI-EBI GWAS Catalog截至2024年7月含625,113个关联、>15.5K性状和>85K数据集，通过EFO性状映射、祖源框架和与PGS Catalog互链提升可复用性，但汇总统计标准化不足、非欧祖源仍偏少、依赖作者提交 [80]。UK Biobank PRS Release发布覆盖28种疾病和25种数量性状的多基因风险评分，并提供基准测试软件；广泛基准测试显示其PRS优于81个已发表PRS，并在其他队列验证，但主要基于UK Biobank人群，跨种族适用性有限 [81]。代谢组学层面，针对约121,657名UK Biobank参与者的NMR代谢标志物数据建立了额外质控流程，分析运输批次、板、孔位、机器人、光谱仪等协变量，在3,169个盲重复中评估，多数标志物技术因素中位解释1.5%，盲重复中位CV 4.55%、R² 0.928，并发布ukbnmr R包，但仅覆盖约三分之一UKB参与者且基于已校准浓度而非原始谱 [82]。

真实世界诊疗数据的规模化组织出现了新形态。一项回顾性观察研究扩展自动化框架，将异质临床事件压缩为以诊断为中心的真实世界诊疗模式标准化摘要，基于爱沙尼亚30%随机人群样本EST-Health-30构建ICD-10三位字符诊断类别队列，汇总索引前90天、索引后30天等窗口内的临床事件，最终形成覆盖1000多个诊断类别的全国尺度数字图谱，但仅基于单一国家样本 [83]。综述性工作则把上述趋势概括为：组学技术、EHR普及与AI推动队列整合深度分子profiling与纵向真实世界数据，研究重心从描述性关联转向机制发现、精细风险分层与遗传导向的治疗开发，并日益全球化与多样化 [32]。

## 4 应用与结果

跨祖源遗传关联发现方面，对 UK Biobank 多遗传祖源人群开展混合模型关联与跨祖源荟萃分析，覆盖比以往更大比例样本，生成 **7,266 个性状**的自由可用汇总统计，并发现 **14,676 个**仅欧洲祖源分析未发现的显著位点，如 CAMK2D 与甘油三酯、G6PD 多效错义变异；但多数关联仍主要见于欧洲祖源，解释需注意人群结构等 caveats [84]。多基因评分方面，利用 GIANT 与 23andMe 最多 510 万人数据开发祖源特异与多祖源 BMI 评分，多祖源评分在 UK Biobank 欧洲裔中解释 **17.6%** 的 BMI 变异，其他人群从东亚裔美国人 16% 到农村乌干达 2.2% 不等，非欧洲裔预测效能显著较低；儿童期加入评分使 8 岁时解释方差从 11% 升至 21%，5 岁时预测 18 岁 BMI 从 22% 升至 35% [85]。

冠心病风险预测呈现多种建模路径。MSGene 多状态模型整合遗传风险与电子健康记录，以年龄为时间尺度估计 10 种心脏代谢状态的年龄特异转移，并评估他汀治疗获益，相较 Framingham 30 年与 PCE 10 年模型可提供动态终身风险 [86]。另一项纵向队列研究（FOS 3,588 人、UKB 327,837 人）发现 PRS 风险比从 19 岁 **3.58** 降至 70 岁 **1.51**，在 40–45 岁组 PRS 显著优于 PCE，多 3.2 倍适宜 [87]。在 UK Biobank 蛋白组学方向，整合传统风险因素、PRS 与 202 蛋白风险评分并用 CatBoost 建模，内部验证 AUC 从 0.750 升至 **0.789**，外部验证从 0.717 升至 **0.762**，9 蛋白面板即可捕获大部分预测信息 [88]。跨队列蛋白组预测研究在 53,026 人中训练 15 种疾病模型，平均 AUC 达 0.74（范围 0.56–0.89），较仅用临床因素平均提升 ΔAUC=0.03，且不依赖模型架构，简单模型如 L2 表现相当，提示泛化性受表型定义影响 [89]。

心肾代谢共病与衰老、代谢组学关联密切。基于 330,177 名 UK Biobank 参与者与 2,911 个血浆蛋白的多状态模型显示，生物衰老可预测 CRM 共病进展，并识别关键中介血浆蛋白，提示衰老蛋白标志物用于风险预测与抗衰老干预靶点 [90]。在 UKB 代谢组学中，MVX 每 1-SD HR=**1.213**、MetaboHealth HR=**1.503**，随访 8,876 人发病，两评分均与发病风险升高相关，MetaboHealth 与现患相关更强 [91]。EPIC-Norfolk 中 >11,000 人、>1,000 代谢物的非靶向代谢组学发现 640 个显著代谢物-疾病关联，其中 **420 个（65.5%）**跨≥2 种 NCD 共享，涉及肝肾功能、脂糖代谢、低度炎症和肠道微生物等可干预通路 [92]。另有研究在 54,933 名美国整合医疗系统参与者中检测 250 个 NMR 代谢标志物，加入标准诊疗预测因子后几乎所有 9 个心血管-肾脏-代谢终点判别能力提升，2 型糖尿病、慢性肾病和代谢功能障碍相关脂肪性肝病增益最大 [93]。

多疾病与多组学整合框架方面，UKB-MDRMF 整合基本、生活方式、测量、环境、遗传和影像六类数据，联合建模 **1,560 种疾病**，优于单类别评估，并揭示风险因素-疾病及共病关联，提供交互平台 [94]。PheMIME 整合 VUMC、Mass General Brigham、UK Biobank 三大 EHR 系统的表型组多病共病汇总统计，结合增强版 associationSubgraphs 实现跨系统交互可视化与疾病聚类推断，以精神分裂症为例展示跨系统多病共病网络 [95]。HFpEF 方向用 UKB 多组学（蛋白/代谢/影像/EHR，HFpEF 33,480 例）训练监督分类器识别症状性 HFpEF 风险并在独立多中心队列验证，无监督聚类划分多组学亚型，结合可解释 AI、去混杂与通路分析揭示分子异质性 [96]。

药物基因组学与特定疾病预测亦有进展。利用 UKB 与 All of Us 的 EHR 纵向用药与生物标志物数据，对 10 个药物-表型对（他汀 LDL-C、二甲双胍 HbA1c、降压药 SBP 等）做常见变异 GWAS 与罕见变异负荷检验并在 All of Us 重复，证明疾病 PRS 可预测药效，但 EHR 用药与检测时点不齐、依从性/适应证混杂带来分析陷阱 [97]。胰腺癌方向用丹麦 DNPR 与美国 VA EHR 的纵向疾病轨迹构建深度学习模型，可提前 3 年预测风险并输出分时间间隔增量风险，从真实世界噪声序列中识别中等数量高风险患者，但属回顾性登记数据、外推有限、筛查成本与假阳性需权衡 [98]。骨质疏松方向基于 UKB 血浆蛋白组学用 XGBoost 与 SHAP 构建 SPX-OP 模型，SHAP 筛选标志物（FSHB、ADIPOQ、SOST、COL9A1、CHAD）模型优于全蛋白组，但外部验证与样本规模细节不明 [99]。

## 5 评测、可复现性与争议

针对大规模电子健康记录生存分析，一项工作提出**贝叶斯Cox回归随机变分推断**方法，基于计数过程表示的Cox偏似然，结合随机变分推断与似然重加权，使后验分布可因子化到子样本，从而支持大数据分析；其数据规模为**百万级数据点、数千时变协变量**，可处理百万数据点并产生可行不确定性估计，并应用于UK Biobank心肌梗死，但局限在于依赖变分近似、精度受子采样影响 [100]。该工作以传统Cox模型实现为对照基准 [100]。

另一篇综述从数据到知识的角度梳理电子健康记录中共病研究的AI方法，场景为共病研究，但仅有标题信息，具体方法与结果不详，未提供可展开的评测或可复现性细节 [21]。两篇证据在研究对象上不同（生存分析推断方法 vs. 共病研究综述），前者给出了可复现相关的数据规模与对照基准，后者缺乏实质内容，二者之间不存在可直接比较的数字或结论冲突。

## 6 空白与趋势

**趋势一：生成式轨迹模型正从“预测下一事件”走向“可干预的数字孪生”，但干预语义与因果有效性尚未被系统评测。** Foresight 已支持患者旅程模拟与因果推断 [2]，NOAH 支持反事实干预模拟 [3]，EHR-MPC 更进一步把脓毒症治疗优化转化为推理时控制问题，用生成式数字孪生加模型预测控制在 Mass General Brigham 8 家医院 ICU 队列上取得与 RL 相当的离线策略性能 [34]。**但清单中没有任何工作在多个生物库上评测“反事实预测”的校准与因果正确性**：Foresight 作者明确强调当前形式不宜直接用于临床决策支持 [2]，EHR-MPC 仅单系统 ICU 队列 [34]。这是一个明确的空白：**面向干预的生成式轨迹模型缺少跨队列、跨编码系统的反事实基准**。

**趋势二：EHR 基础模型的规模竞赛与轻量轨迹特征形成张力，评测框架缺位。** Foresight-England 以 243M 参数、约 6100 万人纵向 EHR 训练，却因数据访问暂停无法导出定量结果 [4]；NOAH 基于 559M 事件、299,000 患者 [3]；MiGHT-EHR 在 MIMIC-III/IV 四任务上平均超越 SOTA [33]。与之对照，All of Us 297,861 人、12 项生物标志物 3 年轨迹特征用 LightGBM 即达 AUROC 0.797，显著优于静态汇总 0.755 [5]。**规模扩张并未带来可比的评测口径**：前者缺定量结果，后者缺外部队列验证，MIMIC 系与生物库系数据分布差异大。**目前没有跨“登记编码—EHR 文本—生物库多模态”的统一基准**，这是方法学上的关键空白。

**趋势三：共病结构发现从主题模型、图模型走向贝叶斯生成框架，但亚型的跨队列可复现性仍是瓶颈。** ATM 在 UKB 282,957 样本识别 52 种共病异质性疾病并在 All of Us 211,908 样本验证，18 个亚型 PRS 显著异于同病其他亚型 [26]；ALADYNOULLI 在 3 个生物库、n>683,000、348 种疾病上识别 21 个可复制特征，跨队列组成保留中位 80% [1]。**但两者对“可复制”的定义与度量不同**（前者为亚型 PRS 差异，后者为组成保留比例），且均以欧洲裔为主。**缺少统一的亚型可复现性度量与跨祖源验证协议**，是共病结构研究向临床推进的直接障碍。

**趋势四：多组学整合的重心正从“关联图谱”转向“生成缺失模态”与“隐性病例扩充”，但外部验证普遍不足。** PULSE 从稀疏常规血检生成代谢组与蛋白质组，生成蛋白质组对 6 种常见病 AUC 达 0.72–0.83，接近真实蛋白质组 [25]；MILTON 用临床生物标志物、血浆蛋白和定量性状预测 3,213 种疾病并扩充病例队列，发现基线未显著的新基因-表型关联 [24]。**但清单中这些工作均未报告跨生物库的外部验证**，而血浆蛋白图谱本身已指出人群代表性有限、缺乏外部验证 [23]。**“生成式补全 + 隐性病例发现”这一组合尚未在独立队列上闭环验证**，是明确的空白方向。

**趋势五：跨祖源与个体级一致性构成对 PRS 临床化的双重约束，但二者尚未被联合建模。** Pan-UKB 跨祖源荟萃分析覆盖 7,266 个性状、新发现 14,676 个仅欧洲祖源分析未检出的位点 [84]；多祖源 BMI 评分在欧洲裔解释 17.6% 变异，非欧洲裔显著较低 [85]；而 48 个冠心病 PRS 在 171,095 人中群体表现相似、个体层面一致性差 [8]。**清单中没有工作把“跨祖源精度衰减”与“个体级评分不一致”放在同一框架下量化**，也缺少将 PRS 与纵向 EHR、蛋白组动态联合的个体级不确定性传播方法。**面向个体的、带不确定性量化的多组学风险沟通**是尚未被填补的方向。

**趋势六：队列资源与标准化工具快速扩张，但“数据通路差异”本身成为新的偏倚来源。** All of Us 内部比较显示患者介导 EHR（19,703 人）与提供者来源 EHR（373,887 人）在人群特征、WGS 覆盖（35.2% vs 83.2%）和关联复制上存在系统差异 [79]；ICD-8 到 ICD-10 单向映射可桥接丹麦 1965 年以来的纵向数据，但不支持回映射 [18]；Phecodes 依赖 ICD 编码，存在编码误差与表型异质性 [17]。**清单中尚无工作系统量化“数据通路/编码版本/表型定义”三类差异对多组学模型跨队列迁移的联合影响**，而这正是生物库级 AI 从方法演示走向可复现发现的前提。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 生成式疾病轨迹模型 | **朝阳** | [2] 用 GPT 式预训练建模患者时间线，[37] 用生成式 transformer 学习疾病自然史，两篇分别落在 2024/2025 且被引 135/78，说明「EHR 序列 → 生成式建模」已被顶刊验证；但 [35] 仍在做纵向生存聚类、[1] 2026 年才提出纵向 EHR+遗传的贝叶斯框架，说明**方法尚未收敛**，仍在多路线竞争。 |
| 2.2 多组学与遗传整合 | **成熟（偏基础设施化）** | [6] 的 UKB 血浆蛋白组×遗传×健康关联（被引 1547）与 [40] 的 45 万人外显子分析（被引 822）已经把「大队列 + 遗传 + 组学关联图谱」做成标准范式；[52] 的混合模型关联方法和 [50] 的 35 项血液尿液生物标志物遗传学进一步说明统计工具与图谱层已高度沉淀，新工作多为**增量扩展**（如 [84] 的 Pan-UKB GWAS）。 |
| 2.3 医学 / EHR 基础模型 | **萌芽→朝阳之间，证据偏少** | [67] Med-BERT 与 [66] BEHRT 是结构化 EHR 预训练的开创性工作，但分别停在 2020/2019；近两年只有 [70] EHRAgent 和 [68] 2026 年的可迁移性改进，**雷达样本中该节 n=5、CNS 占比 0**，说明这条线在顶刊层面的规模化验证尚未出现，方法也未收敛。 |
| 2.4 组学衰老时钟与纵向多组学动态 | **朝阳（与衰老方向强交叉）** | [74] 多器官代谢组生物学年龄关联心血管代谢病、[72] 纵向蛋白组衰老指数预测死亡与多病，两篇均为 2025 年且直接对接人群健康结局；[73] 用 UKB + 12 周运动干预验证蛋白组衰老可逆，说明**从「时钟构建」走向「干预验证」**，但被引都只有 3–17，属于刚起量、方法未定型的阶段。 |
| 3 数据与资源 | **成熟** | [12] UK Biobank 开放资源（被引 11473）与 [13] 深度表型+基因组数据（被引 8002）确立了队列基础设施；[15] FinnGen 与 [16] All of Us 说明多队列、跨人群资源已就位，这一层**不再是瓶颈**，竞争点已上移到建模与验证。 |
| 4 应用与结果 | **朝阳** | [98] 用疾病轨迹深度学习预测胰腺癌风险（被引 311）与 [92] 用血浆代谢物刻画非传染性多病通路（被引 200）证明「EHR/组学 → 临床结局」已有高影响力落地；[85] 2025 年做 BMI 多基因预测的生命历程验证，说明**应用层仍在快速扩张**，但每个适应症的方法各自为战。 |
| 5 评测、可复现性与争议 | **证据不足** | 雷达样本中仅 [100]（大规模 EHR 贝叶斯 Cox）与 [21]（共病 AI 方法综述）两篇，且被引 5/0，**无法支撑阶段判断**；但这恰恰提示该方向缺少统一的基准与可复现评测。 |

**整体判断**：这个方向整体处于**朝阳期偏早期**——雷达样本中 2025+2026 年证据合计 **43/100**，CNS 占比 **0.33**，说明顶刊入口已经打开；但分化明显：**数据资源（3 节）和多组学关联图谱（2.2 节）已成熟**，真正的方法竞争集中在**生成式疾病轨迹（2.1）**和**组学衰老时钟（2.4）**，而 **EHR 基础模型（2.3）与评测（5 节）仍是洼地**。窗口期估计还有 **2–3 年**：一旦纵向 EHR+遗传+蛋白组的统一基础模型出现并被多队列复现（[1] 已露苗头），2.1 会迅速从朝阳转向成熟。最大不确定性是**跨队列可复现性与评测标准缺失**——雷达样本中评测节仅 2 篇、CNS 占比 0，意味着现在的高分工作可能无法在 All of Us/FinnGen 上复现，这会决定哪些方法能沉淀为基础设施。

**接下来怎么做**：

1. **把衰老时钟接到 EHR 轨迹上，做「纵向多组学衰老 → 疾病轨迹」的生成式模型**。切入点：用 UKB 的纵向蛋白组/代谢组 + 诊断时间序列，把 [72] 的纵向蛋白组衰老指数作为隐状态，喂给 [37] 式生成式 transformer 预测多病轨迹。为什么现在做：2.4 刚起量（被引 3–17）、2.1 方法未收敛，两者交叉几乎无人占位；且这直接复用你衰老 + 单细胞 + 多模态建模的既有能力。产出：一个可解释的「衰老隐状态 → 共病轨迹」生成模型 + 跨队列复现。

2. **用类器官/多组学合作项目做 pQTL→机制的下游验证闭环**。切入点：以 [6] 的 UKB 血浆蛋白组 pQTL 图谱为发现层，挑出与衰老/共病强关联的蛋白，在你的类器官 + 多组学合作体系里做扰动验证。为什么现在做：2.2 已成熟，纯关联图谱增量价值低，但**「人群 pQTL → 类器官因果验证」的闭环**是稀缺的，能把你的湿实验合作变成方法学差异化。

3. **在公共数据上做一个跨队列复现基准（demo），抢占 5 节洼地**。切入点：用 UKB + FinnGen + All of Us 的公开摘要/派生数据，对 [2]、[37]、[98] 三个轨迹模型做统一评测，报告跨队列迁移衰减。为什么现在做：雷达样本中评测节仅 2 篇、CNS 占比 0，**基准论文的引用红利高**，且能低成本产出 demo。

4. **切入 EHR 基础模型的「组学增强」缺口**。切入点：现有 [67]、[66] 都只用结构化 EHR，[68] 才刚碰可迁移性；你可以做**EHR token + 蛋白组/代谢组 token 的统一预训练**，用 [1] 的纵向 EHR+遗传贝叶斯框架作为对照基线。为什么现在做：2.3 节 n=5、CNS 占比 0，是雷达样本中最空的顶刊入口之一。

5. **用多病共病结构做「生成式轨迹」的评测与解释层**。切入点：以 [92] 的代谢物-多病通路和 [21] 的共病 AI 综述为框架，检验生成式模型产出的轨迹是否符合已知共病结构。为什么现在做：生成式模型最被质疑的就是**不可解释与不可复现**，谁能给出共病结构层面的验证，谁就能定义这个子方向的评测标准。

## 参考文献

1. A Bayesian framework for longitudinal EHR and genetic discovery. Nature 2026. https://doi.org/10.1038/s41586-026-10780-5
2. Foresight—a generative pretrained transformer for modelling of patient timelines using electronic health records: a retrospective modelling study. The Lancet Digital Health 2024. https://doi.org/10.1016/s2589-7500(24)00025-6
3. NOAH: Learning the Full Patient Journey. A Longitudinal Multimodal Time-Aware Model for Representation and Forecasting.  2026. https://arxiv.org/abs/2609.09140
4. Foresight-England: Development of a National-Scale Generative AI Model of Electronic Health Records for Medical Event Prediction across the COVID-19 Pandemic.  2026. https://arxiv.org/abs/2608.16273
5. Predicting Early Functional Decline from Longitudinal Laboratory and Vital Sign Trajectories: A Large-Scale Study Using the All of Us Research Program.  2026. https://arxiv.org/abs/2608.21589
6. Plasma proteomic associations with genetics and health in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06592-6
7. Plasma proteome analyses in individuals of European and African ancestry identify cis-pQTLs and models for proteome-wide association studies. Nature Genetics 2022. https://doi.org/10.1038/s41588-022-01051-w
8. Evaluating Performance and Agreement of Coronary Heart Disease Polygenic Risk Scores.. JAMA 2025. https://doi.org/10.1001/jama.2024.23784
9. Global Biobank Meta-analysis Initiative: Powering genetic discovery across human disease. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100192
10. Deviations from genetic additivity driven by rare variants at biobank scale.. Nature communications . https://doi.org/10.1038/s41467-026-76151-w
11. Longitudinal dynamics of gene expression and metabolomics in an aging population cohort.. Science 2026. https://doi.org/10.1126/science.aed6452
12. UK Biobank: An Open Access Resource for Identifying the Causes of a Wide Range of Complex Diseases of Middle and Old Age. PLoS Medicine 2015. https://doi.org/10.1371/journal.pmed.1001779
13. The UK Biobank resource with deep phenotyping and genomic data. Nature 2018. https://doi.org/10.1038/s41586-018-0579-z
14. Whole-genome sequencing of 490,640 UK Biobank participants.. Nature 2025. https://doi.org/10.1038/s41586-025-09272-9
15. FinnGen provides genetic insights from a well-phenotyped isolated population. Nature 2023. https://doi.org/10.1038/s41586-022-05473-8
16. The “All of Us” Research Program. New England Journal of Medicine 2019. https://doi.org/10.1056/NEJMsr1809937
17. Using Phecodes for Research with the Electronic Health Record: From PheWAS to PheRS. Annual Review of Biomedical Data Science 2021. https://doi.org/10.1146/annurev-biodatasci-122320-112352
18. A unidirectional mapping of ICD-8 to ICD-10 codes, for harmonized longitudinal analysis of diseases. European Journal of Epidemiology 2023. https://doi.org/10.1007/s10654-023-01027-y
19. Software Application Profile: PHESANT: a tool for performing automated phenome scans in UK Biobank. International Journal of Epidemiology 2017. https://doi.org/10.1093/ije/dyx204
20. Exploring and visualizing large-scale genetic associations using PheWeb. Nature Genetics 2020. https://doi.org/10.1038/s41588-020-0622-5
21. From data to knowledge: artificial intelligence methods for studying comorbidity in electronic health records. The European Physical Journal Special Topics 2026. https://doi.org/10.1140/epjs/s11734-026-02571-w
22. Atlas of plasma NMR biomarkers for health and disease in 118,461 individuals from the UK Biobank. Nature Communications 2023. https://doi.org/10.1038/s41467-023-36231-7
23. Atlas of the plasma proteome in health and disease in 53,026 adults.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.045
24. Disease prediction with multi-omics and biomarkers empowers case–control genetic discoveries in the UK Biobank. Nature Genetics 2024. https://doi.org/10.1038/s41588-024-01898-1
25. Longitudinal alignments and syntheses of multimodal clinical data for personalized medicine with the PULSE framework. Nature Computational Science 2026. https://doi.org/10.1038/s43588-026-01026-5
26. Age-dependent topic modelling of comorbidities in UK Biobank identifies disease subtypes with differential genetic risk. Nature Genetics 2023. https://doi.org/10.1038/s41588-023-01522-8
27. Components of genetic associations across 2,138 phenotypes in the UK Biobank highlight adipocyte biology. Nature Communications 2019. https://doi.org/10.1038/s41467-019-11953-9
28. Mono- and biallelic variant effects on disease at biobank scale. Nature 2023. https://doi.org/10.1038/s41586-022-05420-7
29. Phenome-wide Burden of Copy Number Variation in the UK Biobank.. American Journal of Human Genetics 2019. https://doi.org/10.1016/j.ajhg.2019.07.001
30. All of Us diversity and scale yield context-dependent improvements in polygenic prediction.. Nature Genetics 2026. https://doi.org/10.1038/s41588-026-02734-4
31. Population-specific polygenic risk scores for people of Han Chinese ancestry.. Nature 2025. https://doi.org/10.1038/s41586-025-09350-y
32. Trends in large-scale human population cohorts.. Trends in Genetics 2026. https://doi.org/10.1016/j.tig.2026.08.002
33. MiGHT-EHR: A Multi-task Graph Transformer for Heterogeneous Temporal Electronic Health Records.  2026. https://arxiv.org/abs/2608.06430
34. EHR-MPC: Inference-Time Control for Sepsis Treatment with Generative Patient Digital Twins. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.08793
35. Deep representation learning for clustering longitudinal survival data from electronic health records.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56625-z
36. Subtyping Alzheimer's disease and Parkinson's disease using longitudinal electronic health records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01085-3
37. Learning the natural history of human disease with generative transformers.. Nature 2025. https://doi.org/10.1038/s41586-025-09529-3
38. Exome sequencing and characterization of 49,960 individuals in the UK Biobank. Nature 2020. https://doi.org/10.1038/s41586-020-2853-0
39. Advancing human genetics research and drug discovery through exome sequencing of the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-021-00885-0
40. Exome sequencing and analysis of 454,787 UK Biobank participants. Nature 2021. https://doi.org/10.1038/s41586-021-04103-z
41. Rare variant contribution to human disease in 281,104 UK Biobank exomes. Nature 2021. https://doi.org/10.1038/s41586-021-03855-y
42. Systematic single-variant and gene-based association testing of thousands of phenotypes in 394,841 UK Biobank exomes. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100168
43. Rare variant associations with plasma protein levels in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06547-x
44. Multi-ancestry MHC-pQTL mapping reveals disease-linked HLA protein networks and shared genetic architecture.  . https://doi.org/10.21203/rs.3.rs-10956233/v1
45. Genetic associations with ratios between protein levels detect new pQTLs and reveal protein-protein interactions. bioRxiv 2023. https://doi.org/10.1016/j.xgen.2024.100506
46. Robust cis-by-trans epistasis in the human plasma proteome highlights an ABO-centered interaction network.. American journal of human genetics . https://doi.org/10.1016/j.ajhg.2026.09.003
47. Sex differences in the genetic regulation of the human plasma proteome.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59034-4
48. Metabolomic and genomic prediction of common diseases in 700,217 participants in three national biobanks.. Nature communications 2024. https://doi.org/10.1038/s41467-024-54357-0
49. Identification of plasma proteomic markers underlying polygenic risk of type 2 diabetes and related comorbidities.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56695-z
50. Genetics of 35 blood and urine biomarkers in the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-020-00757-z
51. An atlas of polygenic risk score associations to highlight putative causal relationships across the human phenome. bioRxiv 2018. https://doi.org/10.7554/eLife.43657
52. Mixed model association for biobank-scale data sets. Nature Genetics 2018. https://doi.org/10.1038/s41588-018-0144-6
53. A fast and scalable framework for large-scale and ultrahigh-dimensional sparse regression with application to the UK Biobank. bioRxiv 2019. https://doi.org/10.1371/journal.pgen.1009141
54. Global biobank analyses provide lessons for computing polygenic risk scores across diverse cohorts. medRxiv 2021. https://doi.org/10.1101/2021.11.18.21266545
55. Pan-UK Biobank GWAS improves discovery, analysis of genetic architecture, and resolution into ancestry-enriched effects. medRxiv 2024. https://doi.org/10.1101/2024.03.13.24303864
56. Phenome-wide and proteomic analysis of APOE alleles across different ancestries in the All of Us Research Program.  . https://doi.org/10.64898/2026.09.26.26364080
57. Comparative analysis of the Mexico City Prospective Study and the UK Biobank identifies ancestry-specific effects on clonal hematopoiesis.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02085-6
58. SPA<sub>GRM</sub>: effectively controlling for sample relatedness in large-scale genome-wide association studies of longitudinal traits.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56669-1
59. A pre-train and fine-tune framework for adaptive boosting of pre-trained polygenic risk scores.. Nature communications . https://doi.org/10.1038/s41467-026-77128-5
60. Genetically supported targets and drug repurposing for brain aging: A systematic study in the UK Biobank.. Science advances 2025. https://doi.org/10.1126/sciadv.adr3757
61. Integrating the environmental and genetic architectures of aging and mortality.. Nature medicine 2025. https://doi.org/10.1038/s41591-024-03483-9
62. Phenome-wide association studies across large population cohorts support drug target validation. Nature Communications 2018. https://doi.org/10.1038/s41467-018-06540-3
63. GWAS of extended prescription analgesic use identifies genetic loci in chronic pain.. Nature communications 2026. https://doi.org/10.1038/s41467-026-71434-8
64. Polygenic Prediction of Peripheral Artery Disease and Major Adverse Limb Events.. JAMA cardiology 2025. https://doi.org/10.1001/jamacardio.2025.1182
65. An atlas of genetic associations in UK Biobank. Nature Genetics 2017. https://doi.org/10.1038/s41588-018-0248-z
66. BEHRT: Transformer for Electronic Health Records. Scientific Reports 2019. https://doi.org/10.1038/s41598-020-62922-y
67. Med-BERT: pretrained contextualized embeddings on large-scale structured electronic health records for disease prediction. npj Digital Medicine 2020. https://doi.org/10.1038/s41746-021-00455-y
68. Large language models improve transferability of electronic health record-based predictions across countries and coding systems.. NPJ digital medicine 2026. https://doi.org/10.1038/s41746-026-02363-5
69. SurvivEHR: a competing risks, time-to-event foundation model for multiple long-term conditions from primary care electronic health records.  2025. https://doi.org/10.1101/2025.08.04.25332916
70. EHRAgent: Code Empowers Large Language Models for Few-shot Complex Tabular Reasoning on Electronic Health Records.. Proceedings of the Conference on Empirical Methods in Natural Language Processing. Conference on Empirical Methods in Natural Language Processing 2024. https://doi.org/10.18653/v1/2024.emnlp-main.1245
71. Molecular Circadian Disturbance in Human Blood Independently Predicts Multi-Disease Risk and Maps to Hepatic metabolism Pathways.  . https://doi.org/10.21203/rs.3.rs-11120748/v1
72. A Novel Longitudinal Proteomic Aging Index Predicts Mortality, Multimorbidity, and Frailty in Older Adults.. Aging cell 2025. https://doi.org/10.1111/acel.70317
73. Reversal of proteomic aging with exercise-results from the UK biobank and a 12-week intervention study.. npj aging 2025. https://doi.org/10.1038/s41514-025-00318-w
74. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
75. Age Acceleration and Mortality Risk Constitute Distinct Dimensions of Organ Aging.  . https://doi.org/10.21203/rs.3.rs-10881849/v1
76. Estimation of physiological aging based on routine clinical biomarkers: a prospective cohort study in elderly Chinese and the UK Biobank.. BMC medicine 2024. https://doi.org/10.1186/s12916-024-03769-2
77. UK Biobank-A Unique Resource for Discovery and Translation Research on Genetics and Neurologic Disease.. Neurology. Genetics 2025. https://doi.org/10.1212/nxg.0000000000200226
78. Lessons from national biobank projects utilizing whole-genome sequencing for population-scale genomics.. Genomics & informatics 2025. https://doi.org/10.1186/s44342-025-00040-9
79. Robust replication of associations across patient-mediated and provider-sourced EHR data in the All of Us research program. npj Digital Public Health 2026. https://doi.org/10.1038/s44482-026-00032-8
80. The NHGRI-EBI GWAS Catalog: standards for reusability, sustainability and diversity.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1070
81. UK Biobank release and systematic evaluation of optimised polygenic risk scores for 53 diseases and quantitative traits. medRxiv 2022. https://doi.org/10.1101/2022.06.16.22276246
82. Quality control and removal of technical variation of NMR metabolic biomarker data in ~120,000 UK Biobank participants. Scientific Data 2021. https://doi.org/10.1038/s41597-023-01949-y
83. A national-scale digital atlas of recorded care patterns across more than 1000 diagnostic categories using real-world health data: a retrospective observational study.  . https://doi.org/10.64898/2026.09.16.26363186
84. Pan-UK Biobank genome-wide association analyses enhance discovery and resolution of ancestry-enriched effects.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02335-7
85. Polygenic prediction of body mass index and obesity through the life course and across ancestries.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03827-z
86. MSGene: a multistate model using genetic risk and the electronic health record applied to lifetime risk of coronary artery disease. Nature Communications 2024. https://doi.org/10.1038/s41467-024-49296-9
87. Dynamic Importance of Genomic and Clinical Risk for Coronary Artery Disease Over the Life Course. medRxiv 2023. https://doi.org/10.1101/2023.11.03.23298055
88. Machine Learning‐Driven Prediction of Coronary Artery Disease Risk Based on UK Biobank Plasma Proteomics. Journal of the American Heart Association : Cardiovascular and Cerebrovascular Disease 2026. https://doi.org/10.1161/JAHA.125.047248
89. Generalizability of proteomic risk prediction across biobanks reveals dependence on phenotype definitions.  . https://doi.org/10.64898/2026.10.01.26364038
90. Proteomics mediates the effects of biological aging on the progression of cardio-renal-metabolic comorbidity: a UK biobank cohort study.. Cardiovascular diabetology 2025. https://doi.org/10.1186/s12933-025-03035-6
91. MetaboHealth and Metabolic Vulnerability Index as Risk Factors for Cardio-Renal-Metabolic Multimorbidity: A Large-Scale Prospective Cohort Study.. Diabetes, obesity and metabolism 2026. https://doi.org/10.1111/dom.71112
92. Plasma metabolites to profile pathways in noncommunicable disease multimorbidity. Nature Medicine 2021. https://doi.org/10.1038/s41591-021-01266-0
93. NMR metabolomics for cardiovascular-kidney-metabolic risk stratification in an integrated healthcare system.  . https://doi.org/10.64898/2026.10.01.26364322
94. UKB-MDRMF: a multi-disease risk and multimorbidity framework based on UK biobank data.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58724-3
95. PheMIME: an interactive web app and knowledge base for phenome-wide, multi-institutional multimorbidity analysis.. Journal of the American Medical Informatics Association : JAMIA 2024. https://doi.org/10.1093/jamia/ocae182
96. Deep phenotyping of heart failure with preserved ejection fraction through multi-omics integration.. European journal of heart failure 2025. https://doi.org/10.1002/ejhf.70041
97. Leveraging large-scale biobank EHRs to enhance pharmacogenetics of cardiometabolic disease medications.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58152-3
98. A deep learning algorithm to predict risk of pancreatic cancer from disease trajectories. Nature Medicine 2023. https://doi.org/10.1038/s41591-023-02332-5
99. Explainable Plasma Proteomics–Based Machine Learning for Osteoporosis Diagnosis, Prognosis, and Protein Biomarker Discovery in the UK Biobank. The FASEB Journal 2026. https://doi.org/10.1096/fj.202600647R
100. Bayesian Cox regression for large-scale inference with applications to electronic health records. Annals of Applied Statistics 2021. https://doi.org/10.1214/22-aoas1658
