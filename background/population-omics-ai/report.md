# 人群健康与多组学 AI · 方向背景报告

证据 94 篇 · 覆盖度 0.83 · 第 8 轮 · 更新 2026-09-27 · 数字核验删句 1

## 摘要（TL;DR）

- 生成式疾病轨迹模型用生成式架构从纵向 EHR 学习疾病演化并预测未来事件，但 Foresight、ALADYNOULLI 等都依赖登记或诊断编码，作者均提示记录偏倚与人群偏倚风险 [1][2]。
- Foresight-England 报告了迄今最大规模尝试：243 百万参数 Transformer 解码器，在约 6100 万人去标识化纵向 EHR 上训练（训练 5490 万、评估 610 万），但因 NHS England 暂停数据访问，定量结果无法导出，仅作为方法学模板 [3]。
- 一项基于 All of Us 297,861 人（11.1% 为病例）的研究仅用 12 项常规生物标志物三年轨迹特征加 LightGBM，其 AUROC 0.797 显著优于静态汇总的 0.755（P<0.001），并可提前 3–12 个月持续预测（AUROC 0.768–0.740），与大规模生成式模型形成方法学张力 [4]。
- UK Biobank 的 Pharma Proteomics Project 对 54,219 名参与者的 2,923 种血浆蛋白进行检测，发现 14,287 个主要遗传关联，其中 81% 为既往未报道，并精细映射出 29,420 个独立信号 [5]。
- 一项对 53,026 人、2,920 种血浆蛋白的图谱研究报告了 168,100 个蛋白-疾病关联和 554,488 个蛋白-性状关联，183 种疾病的判别 AUC 超过 0.80，并通过 pQTL 确定 474 个因果蛋白 [6]。
- 在 UK Biobank、爱沙尼亚生物库和芬兰 THL 生物库共 700,217 名参与者中，研究者用 Cox 模型和 Lasso 从 36 个临床验证代谢标志物中为 12 种高 DALY 疾病构建代谢组评分，并实现跨三库重复 [7]。
- 整合 Fenland 和 UK Biobank 的 SomaLogic 与 Olink 数据（30,307 名女性、26,058 名男性、5,823 个蛋白靶点）发现，69.1% 的蛋白存在性别差异，男性偏高占 62.1%/63.8%，而激素和 BMI 等仅解释 15.3%/20.5%，提示蛋白组整合模型若只在单一性别或祖源中训练，可能系统性丢失可迁移信号 [8]。
- 一项在 All of Us、Penn Medicine 和 UCLA 生物库中对 171,095 人计算 48 个冠心病 PRS 的研究发现，群体水平表现相似的 PRS 在个体层面一致性差（ICC 与 Light κ 低），提示临床使用需谨慎 [9]。
- PULSE 框架在 UK Biobank 上从稀疏常规血检生成代谢组和蛋白质组谱，生成代谢组在 251 个标志物上优于所有基准方法，生成蛋白质组对 6 种常见病 AUC 达 0.72–0.83，接近真实蛋白质组数据 [10]。
- 在 UKB 492,567 人的暴露组全关联和 45,441 人的蛋白组衰老时钟分析中，识别出 25 个独立暴露与死亡和蛋白组衰老相关，并发现环境暴露对死亡与 25 种年龄相关病的解释度常高于基因组，提示整合模型需同时纳入环境层 [11]。

## 1 背景与定义

人群健康与多组学 AI 的边界，首先由数据基础设施的规模与形态决定。**UK Biobank** 自 2006–2010 年招募 50 万名 40–69 岁参与者，收集遗传与非遗传决定因素并链接健康记录，预计 20 年随访累积糖尿病约 68,000 例、心梗与冠心病死亡 47,000 例、卒中 20,000 例、阿尔茨海默病 30,000 例 [12]；其基因型资源完成约 9600 万变异插补 [13]，后续全基因组测序在 490,640 人中以平均 32.5× 覆盖识别约 15 亿变异 [14]。与之互补，**All of Us** 计划招募至少 100 万人，截至 2019 年 7 月已有 >175,000 人贡献生物样本，其中 >80% 来自历史上研究不足群体 [15]；**FinnGen** 整合 9 个芬兰生物库与全国健康登记，基于 224,737 人插补基因型和 1,932 个终点开展 GWAS 与精细定位 [16]。这些资源共同界定了本方向的准入线：**研究须建立在万人级以上、具备纵向健康记录 linkage 的人群队列之上**，而非单中心小样本关联。

从演化脉络看，本方向经历了三个相互叠加的阶段。第一阶段以结构化 EHR 序列建模为起点：**BEHRT** 用 Transformer 处理百万级患者诊断序列，纳入就诊位置、年龄与事件顺序，在多项未来诊断预测任务中优于 Deepr、RNN、LSTM、RETAIN [17]；**Med-BERT** 把 BERT 预训练-微调范式迁移到千万级 ICD 序列，显示预训练在标注样本有限时尤为有益 [18]。第二阶段转向生成式与基础模型：**Foresight** 整合结构化数据与约占 80% 的自由文本，覆盖 18 类 SNOMED 概念 [19]；**Foresight-England** 在约 6100 万人去标识化纵向 EHR 上训练 243 百万参数 Transformer 解码器，但因数据访问暂停无法导出定量结果 [3]；**Delphi-2M** 在 UK Biobank 训练、丹麦登记验证，可同时预测 1000 多种疾病未来发生率 [1]；**ALADYNOULLI** 以贝叶斯生成框架联合建模纵向诊断、年龄与多基因风险，覆盖三队列 68.3 万余人、348 种疾病 [2]。第三阶段则是多组学与遗传的系统整合，把血浆蛋白组、代谢组、甲基化等分子层与 EHR、PRS 并置，代表性图谱包括 53,026 人、2,920 种血浆蛋白的蛋白-疾病-性状关联图谱 [6]，以及跨三国家生物库 700,217 人的代谢组疾病预测 [7]。

本方向的核心问题可归纳为四类。**其一是轨迹的生成式建模与可复现性**：生成式模型能否在跨队列、跨编码系统条件下稳定预测多病共存轨迹，仍存争议——Delphi-2M 在 UK Biobank 训练、丹麦登记验证 [1]，ALADYNOULLI 报告跨队列组成保留中位 80%、亚型 Cohen's d 达 4.25 [2]，但作者均提示记录偏倚与人群偏倚风险。**其二是共病结构与疾病亚型的发现**：ATM 对 UK Biobank 282,957 人与 All of Us 211,908 人的纵向 EHR 做低秩表示，识别 52 种共病异质性疾病，18 个亚型的 PRS 显著异于同病其他亚型 [20]；VaDeSC-EHR 则用 Transformer 变分自编码器结合 Weibull 混合生存分布，把风险建模与聚类直接整合 [21]。**其三是遗传-分子-疾病链条的因果解析**：pQTL 图谱已确定 474 个因果蛋白 [6]，全基因组 T2D PGS 关联 648 个蛋白、617 个复制 [22]，但 PRS 关联受水平多效性影响、关联不等于因果 [23]。**其四是跨祖源与跨性别的可迁移性**：Pan-UK Biobank 新发现 14,676 个仅欧洲祖源分析未检出的位点 [24]；蛋白组性别差异分析显示 69.1% 的蛋白存在性别差异，而遗传效应对蛋白靶点在两性间高度相似 [8]；ARIC 在欧裔与非裔美国人中发现多数 cis 关联重叠但存在人群特异位点 [25]。

方法学层面，本方向的另一条主线是**统计与计算工具对生物样本库规模的适配**。BOLT-LMM 在 UKB 全部 459K 欧洲样本上运行并保留相关个体，身高等效 650K 样本，23 个性状独立位点从 5,839 增至 10,759 [26]；SPA_GRM 针对纵向性状控制样本亲缘关系，在 UK Biobank 79 个纵向性状中识别 7,463 个遗传位点 [27]；贝叶斯 Cox 模型结合随机变分推断与似然重加权，可处理百万级数据并给出可行不确定性估计 [28]。这些工具解决了相关个体、纵向数据与超高维稀疏回归的瓶颈，使多组学整合在人群尺度上成为可能。

最后，**表型标准化与数据资源共享程度决定了方向的可复用边界**。Phecodes 基于 ICD 编码高通量定义数千种疾病状态，支撑 PheWAS 与表型风险评分，但依赖 ICD 编码、可能存在编码误差与表型异质性 [29]；ICD-8 到 ICD-10 的单向映射可连接丹麦 1965 年以来超半世纪医疗数据，但未提供回映射 [30]；NHGRI-EBI GWAS Catalog 截至 2024 年 7 月含 625,113 个关联、>15.5K 性状和 >85K 数据集，但汇总统计标准化不足、非欧祖源仍偏少 [31]。UK Biobank 发布的 PRS Release 覆盖 28 种疾病和 25 种数量性状，基准测试显示优于 81 个已发表 PRS，但主要基于 UK Biobank 人群、跨种族适用性有限 [32]。**因此，本方向的边界不仅是"用了多组学与 AI"，更在于是否在公开队列资源、可复现流程与跨人群验证上具备可检验性**；单中心小样本关联、无公开数据也无代码的纯预测模型、以及无方法学新意的单病种评分改良，均不构成本方向的核心贡献。

## 2 方法学


### 2.1 生成式疾病轨迹模型

生成式疾病轨迹模型的核心思路，是用生成式架构从纵向电子健康记录（EHR）中学习疾病随时间的演化规律，并据此预测未来事件或模拟个体终身轨迹。**Foresight** 同样基于生成式预训练 Transformer，但强调整合结构化数据与约占 80% 的自由文本，覆盖 18 类 SNOMED 概念，支持跨日/周/月的时间分辨率预测 [19]。**ALADYNOULLI** 则走贝叶斯生成路线，以概率混合而非混合概率的形式联合建模纵向诊断、年龄与多基因风险，从而容纳同时性与慢性病 [2]。三者都依赖登记或诊断编码，作者均提示记录偏倚与人群偏倚风险 [1][2]。

在规模与多模态方向上，工作出现明显分化。**Foresight-England** 报告了迄今最大规模的尝试：243 百万参数 Transformer 解码器，在约 6100 万人去标识化纵向 EHR 上训练（训练 5490 万、评估 610 万），整合初级/次级诊疗、死亡登记与 COVID-19 数据，设计 30 天住院与死亡预测评估框架，但因 NHS England 暂停数据访问，定量结果无法导出，仅作为方法学模板 [3]。**NOAH** 则强调时间感知与多模态，采用双向时间整合和变分隐空间，基于 MIMIC 家族 559M 临床事件、299,000 患者训练，原生处理图像、时序、分类及文本记录，支持自回归预测、零样本分类与反事实干预模拟 [33]。**MiGHT-EHR** 用归一化 PMI 构建异质时序图，以带时序注意力的图 Transformer 自监督预训练并做双平衡多任务学习，在 MIMIC-III/IV 四任务上平均超越 SOTA，死亡率与再入院提升尤为显著 [34]。这些模型的数据基础差异很大，跨研究不宜直接比较性能高低。

生成式轨迹模型也被用于治疗决策与亚型发现。**EHR-MPC** 将脓毒症治疗优化转化为推理时控制问题：训练生成式 EHR 患者数字孪生预测干预下轨迹，再用模型预测控制在推理时规划治疗，在 Mass General Brigham 8 家医院 ICU 脓毒症队列上离线策略性能与强化学习基线相当、模拟性能更优 [35]。亚型方向上有两条不同技术路线：一项工作用 Transformer 生成患者嵌入后以 K-means 聚类，在 CPRD Aurum 与 UK Biobank 逾 100,000 患者中为阿尔茨海默病和帕金森病各识别出五个可复制亚型，亚型间 5 年死亡与住院预后、共病、症状轨迹及遗传背景存在差异 [36]；**VaDeSC-EHR** 则用 Transformer 变分自编码器结合 Weibull 混合生存分布，把风险建模与聚类直接整合，以识别兼具不同诊断轨迹和时间-事件特征的患者亚群 [21]。两者都指出聚类数需预设、EHR 异质与缺失、外部验证有限等局限 [21][36]。

一个值得注意的争议点是：生成式模型是否必须依赖深度序列架构才能捕捉轨迹信号。一项基于 All of Us 297,861 人（11.1% 为病例）的研究，仅提取 12 项常规生物标志物三年轨迹特征（斜率、变异性、delta、均值），用 LightGBM 建模，其 AUROC 0.797 显著优于静态汇总的 0.755（P<0.001），匹配分析为 0.727 vs 0.680，并可提前 3–12 个月持续预测（AUROC 0.768–0.740）[4]。这表明在特定早期预警任务上，轻量轨迹特征即可带来增益，与前述大规模生成式模型形成方法学张力；但该研究仅用常规实验室数据且缺乏外部队列验证 [4]。此外，ALADYNOULLI 报告识别 21 个可复制特征、跨队列组成保留中位 80%、亚型 Cohen's d 达 4.25、95% 比较 P≤1×10⁻⁸，并发现 151 个全基因组显著位点，包括单性状分析遗漏的心血管关联 [2]，提示生成式轨迹建模的价值可能更多体现在与遗传等多组学整合后的发现能力上。

### 2.2 多组学与遗传整合

多组学与遗传整合的核心目标之一，是把遗传变异、分子表型和疾病结局串成可解释的链条。UK Biobank 的 Pharma Proteomics Project 对 **54,219 名**参与者的 **2,923 种**血浆蛋白进行检测，发现 **14,287 个**主要遗传关联，其中 **81%** 为既往未报道，并精细映射出 **29,420 个**独立信号 [5]。同一队列的罕见编码变异分析在 **49,736 人**中鉴定出 **5,433 个**罕见基因型-蛋白关联，**81%** 为既往 GWAS 未检出，基因水平另有 **1,962 个**关联，STAB1/STAB2 分别关联 **77 和 41 个**蛋白 [37]。这些结果说明常见与罕见变异对血浆蛋白组的贡献高度互补，单靠常见变异 GWAS 会遗漏大量信号。

在蛋白组与疾病的关联层面，一项对 **53,026 人**、**2,920 种**血浆蛋白的图谱研究报告了 **168,100 个**蛋白-疾病关联和 **554,488 个**蛋白-性状关联，**183 种**疾病的判别 AUC 超过 **0.80**，并通过 pQTL 确定 **474 个**因果蛋白 [6]。与之呼应，利用 UKB-PPP 与两项随机对照试验数据的工作发现，全基因组 2 型糖尿病多基因评分关联 **648 个**蛋白，其中 **617 个**复制，而分区 PGS 关联的蛋白谱不同，提示多基因风险可分解到不同生物过程 [22]。这些研究共同把蛋白组定位为连接遗传风险与疾病机制的中介层。

代谢组提供了另一条整合路径。在 UK Biobank、爱沙尼亚生物库和芬兰 THL 生物库共 **700,217 名**参与者中，研究者用 Cox 模型和 Lasso 从 **36 个**临床验证代谢标志物中为 **12 种**高 DALY 疾病构建代谢组评分，并实现跨三库重复 [7]。UK Biobank 的 NMR 图谱则覆盖 **118,461 人**、**249 个**脂质与代谢指标，系统关联 **700 多种**疾病的患病、发病和死亡，并在 THL Biobank **3 万余人**中重复验证 [38]。代谢组评分与多基因评分的比较显示，单一测量可同时刻画多种疾病的分子风险，但其跨人群可迁移性仍受队列构成限制。

多基因评分与分子表型的整合被用于机制推断。一项研究测试全基因组和五个分区 T2D PGS 及 CAD、CKD、BMI PGS 与循环蛋白的关联，并做因果推断和心肾结局生存分析 [22]。另一项工作构建 **162 个** PRS 与 UK Biobank **551 个**复杂表型的关联图谱，完成 **89,262 次**检验，并用孟德尔随机化敏感性分析区分因果与多效性，明确指出 PRS 关联受水平多效性影响、关联不等于因果 [23]。这类整合的价值在于提示机制，但其因果解释依赖 MR 假设。

蛋白比值分析进一步挖掘了蛋白-蛋白关系。利用 UKB Olink **1,463 种**蛋白、**54,000 余**样本，研究者复制了 **4,248 个** rQTL，覆盖 **2,821 个**蛋白对，显著 p-gain 蛋白对富集已知互作 **7.6 倍**，比值 GWAS 较单蛋白 GWAS 新增 **24.7%** 遗传信号 [39]。在 MHC 区，多祖先 pQTL 映射在 **2,920 个**血浆蛋白中鉴定出 **13 个** cis 和 **606 个** trans 关联，多数信号跨祖先一致，同时发现东亚人群 EDAR 的祖先富集关联 [40]。以 ABO 为中心的上位效应网络也被系统映射，采用三明治方差估计器控制假阳性并经模拟验证 [41]。这些工作表明，整合层级正从单变异-单蛋白扩展到蛋白互作与上位效应网络。

性别与祖源分层揭示了遗传调控的异质性。整合 Fenland 和 UK Biobank 的 SomaLogic 与 Olink 数据（**30,307 名**女性、**26,058 名**男性、**5,823 个**蛋白靶点）发现，**69.1%** 的蛋白存在性别差异，男性偏高占 **62.1%/63.8%**，而激素和 BMI 等仅解释 **15.3%/20.5%**；相比之下遗传效应对蛋白靶点在两性间高度相似，仅 **103 个** sd-pQTL [8]。在祖源维度，ARIC 研究对 **7,213 名**欧裔和 **1,871 名**非裔美国人分析 **4,657 种**蛋白，发现欧裔 **2,004 个**、非裔 **1,618 个**蛋白有 cis 关联，多数重叠但存在人群特异位点 [25]。这些差异提示，蛋白组整合模型若只在单一性别或祖源中训练，可能系统性丢失可迁移信号。

跨祖源遗传发现的方法学也在快速演进。Pan-UK Biobank 对 **7,271 个**表型做跨祖源混合模型关联与荟萃分析，新发现 **14,676 个**仅欧洲祖源分析未检出的位点，并揭示 G6PD 等祖源富集变异的多效性 [42]。GBMI 汇集 **23 个**生物样本库、**220 万**人、**14 个**疾病终点，覆盖六大祖先（欧 **1.4M**、东亚 **415K** 等），通过统一表型和质控提升发现能力 [43]。在 PRS 构建上，GBMI 比较 P+T 与 PRS-CS，发现 **PRS-CS 总体优于 P+T**，且欧洲 LD 面板预测精度相当或更高，原因在于参与者仍以欧洲祖源为主 [44]。All of Us 与 UK Biobank 联合开发的 **32 个**性状多血统 PRS 显示，增加多样性提升部分性状精度，但最大化样本量并非普遍最优，多血统训练可减缓随血统分歧的精度衰减 [45]。台湾精准医学计划基于 **463,447 名**汉族人构建人群特异 PRS，并在 TWB、UKB、All of Us 验证，证明汉族特异模型优于欧洲为主模型 [46]。这些结果共同指向一个争议：跨祖源整合的收益依赖于研究设计与性状遗传结构，而非简单地扩大样本量。

PRS 的临床可用性受到个体层面一致性的挑战。一项在 All of Us、Penn Medicine 和 UCLA 生物库中对 **171,095 人**计算 **48 个**冠心病 PRS 的研究发现，群体水平表现相似的 PRS 在个体层面一致性差（ICC 与 Light κ 低），提示临床使用需谨慎 [9]。外周动脉疾病的整合多祖源评分 PRS-PAD 在 UKB **400,533 人**、AoU **218,500 人**、MGBB **32,982 人**中与 PAD 及主要肢体不良事件显著关联，支持高危个体识别，但摘要未给出完整 AUC/OR 数值 [47]。这说明从群体区分度到个体决策之间仍有明显缺口。

外显子测序资源为罕见变异整合提供了基础。UK Biobank 首批 **49,960 人** WES 释放约 **400 万**编码变异，其中约 **98.6%** 频率低于 **1%**，含 **198,269 个**常染色体预测 LOF 变异，超过 **97%** 的基因至少有一个 LOF 携带者 [48]。UKB-ESC 首批 **200,643 人**数据包含约 **1000 万**变异，其中 **84.5%** 为编码，LOF **453,733 个** [49]。更大规模分析在 **454,787 人**中发现 **8,865 个**显著关联，涉及 **564 个**基因、**492 个**表型、**2,283 个**基因-表型对，**91%** 不能由常见变异 LD 解释，**81%** 可复制 [50]。另一项对 **281,104 人**外显子的 PheWAS 识别 **632 个**显著 ExWAS 变异，并刻画 PTV 携带谱：**96%** 基因有杂合 PTV，**20%** 有纯合/半合 PTV [51]。系统单变异与基因负荷分析覆盖 **4,529 个**表型、**8,074,878 个**单变异和 **75,767 个**基因-注释组，并公开 summary statistics 浏览器 [52]。这些资源使罕见变异得以与常见变异、分子表型并列整合。

方法学创新支撑了上述整合的规模与稳健性。BOLT-LMM 在 UKB 全部 **459K** 欧洲样本上运行并保留相关个体，身高等效 **650K** 样本（有效样本 **+93%**），**23 个性状**独立位点从 **5,839 增至 10,759（+84%）** [26]。BASIL 通过 screen-solve-check 迭代支持大于内存的数据，可扩展至 TB 级基因型矩阵 [53]。SPA_GRM 针对纵向性状控制样本亲缘关系，在 UK Biobank **79 个**纵向性状中识别 **7,463 个**遗传位点 [27]。DeGAs 对 **2,138 个**表型、**235,907 个**变异做截断 SVD，**100 个**成分分别解释 **41.9%/62.8%/75.5%** 方差，PTV 富集肥胖性状并突出脂肪细胞生物学 [54]。这些工具共同解决了生物样本库规模下相关个体、纵向数据和超高维稀疏回归的统计与计算瓶颈。

纵向与多模态整合开始进入临床预测场景。PULSE 框架在 UK Biobank 上从稀疏常规血检生成代谢组和蛋白质组谱，生成代谢组在 **251 个**标志物上优于所有基准方法，生成蛋白质组对 **6 种**常见病 AUC 达 **0.72–0.83**，接近真实蛋白质组数据 [10]。MILTON 利用 UKB **484,230** 基因组、**3,213** 表型及血浆蛋白等，预测招募时未诊断的新发病例，大幅优于现有 PRS，扩充后 PheWAS 发现多个基线未显著的新基因-表型关联 [55]。ATM 对 UK Biobank **282,957 人**和 All of Us **211,908 人**的纵向 EHR 做低秩表示，识别 **52 种**共病异质性疾病，**18 个**亚型的 PRS 显著异于同病其他亚型 [20]。这些工作把多组学整合从横断面关联推进到纵向轨迹与亚型分层。

环境暴露与遗传的整合则提供了另一维度的对照。在 UKB **492,567 人**的暴露组全关联和 **45,441 人**的蛋白组衰老时钟分析中，识别出 **25 个**独立暴露与死亡和蛋白组衰老相关，并发现环境暴露对死亡与 **25 种**年龄相关病的解释度常高于基因组 [11]。这一结果与以遗传为主线的多组学整合形成张力：分子表型的遗传架构虽可精细解析，但疾病风险的可解释方差有相当部分来自非遗传暴露，提示整合模型需同时纳入环境层。

药物靶点发现是多组学遗传整合最直接的应用出口。脑龄差 GWAS 发现 **2 个**新位点和 **7 个**已知位点，整合 MR 与共定位优先 **7 个**可成药基因，重发现 **13 种**有临床试验证据的潜在药物 [56]。35 项血尿标志物的遗传分析在 **363,228 人**中发现 **5,794 个**独立位点、**3,374 个**精细映射关联和 **51 个**因果关系，多 PRS 模型在 FinnGen 中改善慢性肾病、2 型糖尿病、痛风和酒精性肝硬化的风险分层 [57]。跨四队列 PheWAS 对 **19 个**候选药物靶点、最多 **697,815 人**、**1,683 个**二分类终点做验证，识别真实多效性并提示疗效或安全性信号 [58]。FinnGen 对 **176,899 名**芬兰人、**2,444 种**疾病表型分析 **44,370 个**编码变异的单等位与双等位效应，发现芬兰人群瓶颈效应导致的纯合子富集可提升隐性致病变异检出，并揭示同一变异在杂合与纯合状态下可呈现不同疾病表型 [59]。CNV 全表型分析在 **472,228 人**、**>3,000 个性状**中发现 16p11.2、22q11.2、9p23 等位点关联 [60]。慢性疼痛的处方定义 GWAS 在 UK Biobank 与 FinnGen 各约 **50 万人**中识别 **140 个**全基因组关联，其中 **78 个**为新发现 [61]。这些研究显示，多组学整合正在把统计关联转化为可成药靶点和风险分层工具，但其临床效用仍需前瞻性验证。

### 2.3 医学 / EHR 基础模型

早期工作把结构化 EHR 当作医学概念序列来建模。**BEHRT** 用 Transformer 处理百万级患者的诊断序列，纳入就诊位置、年龄和事件顺序，在多种未来诊断预测任务中优于 Deepr、RNN、LSTM、RETAIN 等基线 [17]。**Med-BERT** 进一步把 BERT 的预训练-微调范式迁移到千万级患者的 ICD 诊断序列上，先自监督预训练再针对糖尿病、心衰等任务微调，与 BEHRT、G-BERT 及任务内训练模型比较，显示预训练能提升预测性能，在标注样本有限时尤为明显 [18]。两者的共同局限是仅依赖诊断码、跨机构泛化未充分验证 [17][18]。

后续工作转向跨系统迁移、时间事件建模与交互式查询。**GRASP** 用大语言模型把医学编码映射到共享语义空间，再结合 transformer 预测 21 种疾病和全因死亡，在 UKB 391921、FinnGen 253991、Mount Sinai 386755 人上验证，平均 ΔC-index 较语言无关模型在芬兰高 88%、美国高 47%，且 62% 疾病与 PRS 相关性显著更高 [62]。**SurvivEHR** 则以竞争风险时间事件目标在英国初级保健 2300 万患者、76 亿编码事件上预训练，风险分层超越基准生存模型并支持低资源微调，但外部多国泛化未验证 [63]。与前两者不同，**EHRAgent** 不训练预测模型，而是让 LLM 智能体自主生成并执行代码，把多表 EHR 推理形式化为工具使用规划，在三个真实数据集上成功率超最强基线 29.6% [64]。这些路线在目标上互补，但跨机构、跨编码系统的泛化仍是共同争议点 [62][63]。

### 2.4 组学衰老时钟与纵向多组学动态

纵向多组学研究的核心进展，是把衰老时钟从单时点横截面测量推进到对个体轨迹的刻画。针对335名女性8年全血随访，**5,061个基因和181个代谢物**随时间变化，且个体轨迹常偏离群体水平趋势，这些纵向变化基因具有细胞类型特异性并富集于心血管代谢和神经退行性疾病相关通路，同时受遗传、昼夜节律、季节和污染物影响[65]。与之呼应，ARIC研究基于三次访视的4,684个血浆蛋白构建纵向蛋白衰老指数LPAI，采用FPCA提取纵向成分再用Cox弹性网训练，在MESA中验证，**LPAI同时捕捉衰老累积负担与变化速度**，较单时点蛋白时钟提供额外预测信息，可预测全因死亡、多病共存和衰弱[66]。两者都强调纵向动态相对横截面的增量价值，但前者聚焦基因表达与代谢组的跨组学连接、样本仅335名女性，后者聚焦蛋白组、训练与验证队列规模更大，随访间隔较长且存在蛋白平台差异。

在应用层面，多组学衰老时钟被用于风险预测与干预评估，但不同组学与建模路径各有取舍。UK Biobank 274,247人的107个血浆非衍生代谢物被用于构建5个器官特异性代谢组生物年龄MetBAG，独立测试Pearson r为0.25–0.42，关联525个疾病终点并预测14类疾病与死亡风险，其局限在于代谢物覆盖有限、预测相关性中等且需跨人群验证[67]。蛋白组方面，UK Biobank 45,438人显示体力活动越高ProtAgeGap越低，ProtAgeGap与2型糖尿病风险HR=1.06、高活动交互HR=1.05，12周监督运动干预（MyoGlu，26名男性）使ProtAgeGap下降相当于10个月，204个评分蛋白多数稳定而CLEC14A等随运动改变并关联胰岛素敏感性改善，但以观察性关联为主且干预样本量小[68]。此外，基于DFTJ中国老年人36项常规临床指标、用限制立方样条Cox捕捉U型关系构建的生理衰老指数PAI/ΔPAI，在DFTJ和UK Biobank中预测死亡、心血管病及9种慢性病风险，优于仅以年龄为标签的模型，但训练主要基于中国老年人、临床指标可受药物影响[69]。这些工作提示组学与临床时钟在预测力、可干预性和外推性上存在张力；而UK Biobank 420,746人312种血液分子分析进一步表明，用贝叶斯加性回归树推导的节律紊乱指标基本独立于睡眠，可独立预测98种未来发病风险并映射到肝脏代谢通路，说明**昼夜节律扰动是独立于传统衰老时钟的疾病风险维度**，但该证据为观察性关联、未明确因果机制[70]。

## 3 数据与资源

大规模人群队列是人群健康与多组学 AI 的基础设施。**UK Biobank** 于 2006–2010 年招募 50 万名 40–69 岁参与者，收集中老年复杂疾病的遗传与非遗传决定因素，预计 20 年随访累积糖尿病约 68,000 例、心梗与冠心病死亡 47,000 例、卒中 20,000 例、阿尔茨海默病 30,000 例 [12]。其深度表型与基因型资源覆盖约 50 万人的生物测量、生活方式、血尿标志物及影像，并完成约 **9600 万变异插补**，复制 HLA-疾病关联以验证数据质量 [13]。后续全基因组测序在 490,640 人中以平均 32.5× 覆盖识别约 **15 亿变异**，较芯片插补增 18.8 倍、较全外显子测序增 >40 倍 [14]。该队列已超 8000 机构使用、8000 余篇论文，但以 40–69 岁为主、存在健康志愿者偏倚，部分神经疾病病例仍有限 [71]。

面向多样性与精准医学，美国 **All of Us** 计划招募至少 100 万人；截至 2019 年 7 月，>175,000 人贡献生物样本，其中 >80% 来自历史上研究不足群体，34 个站点收集 >112,000 人 EHR [15]。该项目的 EHR 存在两条互补路径：提供者组织来源（HPO）与患者介导（PME）。基于 393,590 名参与者（PME 19,703、HPO 373,887）的比较显示，PME 人群更白、更女性、更多保险、随访更长，WGS 覆盖更少（35.2% vs 83.2%），两种来源在疾病患病率、表型关联和已知基因型-表型关联复制率上存在差异 [72]。这提示数据来源本身会塑造下游关联结果。

隔离人群与全国登记表型提供了另一条路径。**FinnGen** 整合 9 个芬兰生物库与全国健康登记，基于 224,737 人插补基因型和 1,932 个终点开展 GWAS 与精细定位，发现隔离人群富集低频有害等位，可在既往研究充分的疾病中识别新的低频变异关联和可能因果编码变异，但遗传结构特殊、外推受限 [16]。多国 WGS 生物样本库综述比较 UK Biobank、All of Us、PRECISE、Biobank Japan 和 NPBBD-Korea，指出 WGS 可发现罕见变异、结构变异和调控元件，但计算基础设施、隐私伦理、临床整合和祖先多样性不足仍是挑战 [73]。队列研究整体正从描述性关联转向机制发现、精细风险分层与遗传导向治疗开发，并日益全球化与多样化 [74]。

表型与遗传数据的标准化工具决定了这些资源的可复用性。**Phecodes** 基于 ICD 编码高通量定义数千种疾病的病例/对照状态，支撑 PheWAS 与表型风险评分，但依赖 ICD 编码、可能存在编码误差和表型异质性 [29]。跨版本编码方面，一项研究构建 ICD-8 到 ICD-10 的单向映射，覆盖完整 ICD 及丹麦本地扩展，可连接 1965 年以来超半世纪医疗数据，但未提供 ICD-10 回映射 [30]。**PHESANT** 用规则算法为 UK Biobank 异质表型自动选择统计检验，执行全表型扫描并输出图表，但自动化模型可能不适用于所有复杂表型 [75]。**PheWeb** 则整合 Manhattan、LocusZoom 和 PheWAS 视图，支持单性状与多性状切换，已用于 UKB 等数据集，但仅可视化与共享、不含统计建模 [76]。

多组学与评分资源的公开程度不一。UK Biobank 发布覆盖 28 种疾病和 25 种数量性状的 **PRS Release**，基准测试显示其优于 81 个已发表 PRS 并在其他队列验证，但主要基于 UK Biobank 人群、跨种族适用性有限 [32]。NMR 代谢标志物方面，针对约 121,657 人的 168 个标志物与 81 个比值建立额外质控流程，多数标志物技术因素中位解释 1.5%，盲重复中位 CV 4.55%、R² 0.928，并发布 ukbnmr R 包，但仅覆盖约三分之一 UKB 参与者、基于已校准浓度而非原始谱 [77]。**NHGRI-EBI GWAS Catalog** 截至 2024 年 7 月含 625,113 个关联、>15.5K 性状和 >85K 数据集，通过 EFO 性状映射、祖源框架和与 PGS Catalog 互链提升可复用性，但汇总统计标准化不足、非欧祖源仍偏少、依赖作者提交 [31]。

真实世界诊疗数据的规模化摘要构成较新的方向。一项研究扩展自动化框架，将异质临床事件压缩为以诊断为中心的真实世界诊疗模式标准化摘要，基于爱沙尼亚 30% 随机人群样本 EST-Health-30，构建 ICD-10 三位字符诊断队列并汇总索引前 90 天、索引后 30 天等窗口事件，最终形成覆盖 **1000 多个诊断类别**的全国尺度数字图谱，但属回顾性观察研究且仅基于单一国家样本 [78]。

## 4 应用与结果

在跨祖源遗传关联发现方面，对 UK Biobank 多遗传祖源人群开展混合模型关联与跨祖源荟萃分析，覆盖比以往更大比例的样本，生成 **7,266 个性状**的自由可用汇总统计，并发现 **14,676 个仅欧洲祖源分析未发现的显著位点**，如 CAMK2D 与甘油三酯、G6PD 多效错义变异；但多数关联仍主要见于欧洲祖源，解释需注意人群结构等 caveats [24]。在 BMI 与肥胖的终生预测上，利用 GIANT 与 23andMe 最多 510 万人遗传数据开发祖源特异与多祖源多基因评分，多祖源评分在 UK Biobank 欧洲裔中解释 **17.6% 的 BMI 变异**，其他人群从东亚裔美国人 16% 到农村乌干达 2.2% 不等，非欧洲裔预测效能显著较低；儿童期加入评分可提升预测，8 岁时解释方差从 11% 升至 21%，5 岁时预测 18 岁 BMI 从 22% 升至 35% [79]。

在冠心病风险预测上，多项工作从不同角度切入。MSGene 多状态模型整合遗传风险与电子健康记录，以年龄为时间尺度估计 10 种心脏代谢状态的年龄特异转移，纳入性别、CAD-PRS、吸烟、降压药和他汀等协变量，相比 Framingham 30 年与 PCE 10 年模型可提供动态、年龄特异的终身风险并用于指导他汀治疗启动 [80]。另一项纵向研究利用 FOS 3,588 人与 UK Biobank 327,837 人，发现 PRS 风险比随年龄下降（**19 岁 3.58 降至 70 岁 1.51**），在 40–45 岁组 PRS 显著优于 PCE，多 3.2 倍适宜，但两队列年龄范围有限、未涵盖全生命周期 [81]。整合传统风险因素、多基因风险评分与大规模蛋白质组学的工作，在 UK Biobank 中按地区划分训练 32,330、内部验证 13,857、外部验证 5,775，采用 LASSO Cox 构建 202 蛋白风险评分并用 CatBoost 建模，加入 PRS 与蛋白评分后内部验证 AUC 从 0.750 升至 **0.789**，外部验证从 0.717 升至 0.762，9 蛋白面板即可捕获大部分预测信息 [82]。这些研究在预测时间尺度（终身 vs 10 年）与数据模态（EHR、PRS、蛋白组）上存在差异，尚难直接比较优劣。

在心肾代谢共病与衰老方面，基于 330,177 名 UK Biobank 参与者与 2,911 个血浆蛋白，用多状态模型刻画 CRM 疾病轨迹并结合蛋白组识别中介蛋白，发现生物衰老可预测 CRM 共病进展，关键循环蛋白可能作为风险预测标志物与抗衰老干预靶点，但为观察性队列、中介推断因果性有限 [83]。另一项前瞻队列在 269,530 名横断面与 240,576 名随访参与者中评估代谢组学评分，随访 8,876 人发病，**MVX 每 1-SD HR=1.213、MetaboHealth HR=1.503**，两评分均与发病风险升高相关，MetaboHealth 与现患相关更强，提示代谢负担可补充传统风险因素 [84]。更早的 EPIC-Norfolk 研究用 >1,000 代谢物非靶向血浆代谢组学刻画 27 种新发非传染性疾病，在 >11,000 人、219,415 人年中识别 640 个显著代谢物-疾病关联，其中 **420 个（65.5%）跨≥2 种 NCD 共享**，涉及肝肾功能、脂糖代谢、低度炎症与肠道微生物等可干预通路，并上线开放网络服务器 [85]。

在多疾病与多组学框架及工具方面，UKB-MDRMF 整合 UK Biobank 基本、生活方式、测量、环境、遗传与影像六类数据，经标准化预处理后联合建模 **1,560 种疾病**，优于单类别评估，揭示风险因素-疾病及共病关联并提供交互平台，但依赖 UKB 人群、存在缺失值插补与遗传/影像覆盖不全 [86]。PheMIME 整合 VUMC、Mass General Brigham、UK Biobank 三大 EHR 系统的表型组多病共病汇总统计，结合增强版 associationSubgraphs 实现交互可视化与疾病聚类推断，并以精神分裂症为例展示跨系统多病共病网络，但依赖已有汇总统计、未提样本量与统计效能细节 [87]。在特定疾病的多组学深度表型上，HFpEF 研究用 UK Biobank 多组学（蛋白/代谢/影像/EHR，HFpEF 33,480 例）训练监督分类器识别症状性 HFpEF 风险并在独立多中心队列验证，用无监督聚类划分多组学亚型，结合可解释 AI、去混杂与通路分析揭示分子异质性，但 HFpEF 定义依赖多阶段规则、影像/NT-proBNP 缺失者用替代标准、以欧洲人群为主 [88]；骨质疏松研究基于 UKB 血浆蛋白组学用 XGBoost 建模并以 SHAP 解释，构建 SPX-OP 模型，发现 SHAP 筛选标志物（FSHB、ADIPOQ、SOST、COL9A1、CHAD）即可区分正常、现患与未来发病且优于全蛋白组模型，但全文未获取、外部验证与样本规模细节不明 [89]。

在药效遗传预测与早期筛查方面，利用 UKB 与 All of Us 的 EHR 纵向用药与生物标志物数据开展心血管代谢药效 PGx 分析，对 10 个药物-表型对（他汀 LDL-C、二甲双胍 HbA1c、降压药 SBP 等）做常见变异 GWAS 与罕见变异负荷检验并在 All of Us 重复，证明疾病 PRS 可预测药效，但 EHR 用药与检测时点不齐、依从性/适应证混杂、纵向表型分析陷阱多 [90]。胰腺癌早期风险方面，利用丹麦 DNPR 860 万患者（1977–2018）与美国 VA EHR 的纵向疾病轨迹构建深度学习模型，可提前最多 3 年预测风险，输出不同时间间隔的增量风险并分析最具信息量的诊断码，从真实世界噪声序列中识别中等数量高风险患者，但为回顾性登记数据、外推有限、筛查成本与假阳性需权衡 [91]。

## 5 评测、可复现性与争议

在大规模电子健康记录生存分析中，**贝叶斯Cox回归结合随机变分推断**被用于应对高维、时变协变量与内存受限的挑战：该方法基于计数过程表示的Cox偏似然，通过随机变分推断与似然重加权，使后验分布可因子化到子样本，从而支持大数据分析[28]。其评测以传统Cox模型实现为基准，模拟与**UK Biobank心肌梗死**应用显示可处理百万级数据点并给出可行不确定性估计，但方法依赖变分近似，精度受子采样影响[28]。这一局限意味着其不确定性估计的可靠性需结合具体子采样方案审视，而非无条件外推。

相比之下，面向电子健康记录共病研究的AI方法综述仅提供了从数据到知识的研究框架梳理，因仅有标题信息，具体方法与结果不详[92]。两篇证据在可复现性上信息极不对称：前者给出了方法、数据规模、基准与应用场景，后者则缺乏可核验的方法细节与评测结果，因此难以就共病AI方法的可复现性做出实质判断，也尚不构成与贝叶斯Cox方法之间的直接争议。

## 6 空白与趋势

在生成式轨迹建模与多组学整合之外，**跨队列可复现性**正从附属验证步骤上升为核心方法学问题。Delphi-2M 在 UK Biobank 训练、丹麦人群登记验证，词汇覆盖 ICD-10 顶层诊断、性别、BMI、吸烟、饮酒与死亡，可同时预测 1000 多种疾病未来发生率并模拟个体终身轨迹，但作者明确指出记录偏倚与人群偏倚风险 [1]。ALADYNOULLI 则在 UK Biobank、Mass General Brigham 与 All of Us 共 68.3 万余人、348 种疾病上联合建模纵向 EHR 与多基因风险，报告 21 个可复制特征、跨队列组成保留中位 80%，并发现 151 个全基因组显著位点 [2]。**两个模型都提示：轨迹模型的"可复现"目前主要停留在特征或关联层面，而非个体级预测一致性**，这与 PRS 领域观察到的群体表现相似、个体一致性差的问题同构 [9]。

从证据分布看，当前方向存在若干结构性空白，可归纳为以下趋势与缺口：

1. **生成式轨迹模型与多组学的深度耦合仍属少数**。现有生成式工作多依赖诊断编码序列：Foresight 整合结构化数据与约 80% 自由文本但仅覆盖 18 类 SNOMED 概念 [19]；NOAH 原生处理图像、时序、分类与文本，但训练数据为 MIMIC 家族 559M 事件、299,000 患者，未纳入组学层 [33]；Foresight-England 规模达约 6100 万人但仅整合诊疗、死亡登记与 COVID-19 数据，且因数据访问暂停无法导出定量结果 [3]。**真正把血浆蛋白组、代谢组或甲基化作为生成式轨迹模型输入并做跨队列验证的工作尚未出现**，而蛋白组图谱已证明 183 种疾病判别 AUC>0.80、474 个因果蛋白可经 pQTL 确定 [6]，代谢组评分已在三国 700,217 人中跨库重复 [7]，具备接入轨迹模型的证据基础。

2. **纵向多组学轨迹的建模仍以单组学、单时点为主，跨组学动态耦合缺乏统一框架**。335 名女性 8 年随访显示 5,061 个基因和 181 个代谢物随时间变化且个体轨迹常偏离群体趋势 [65]；ARIC 基于三次访视 4,684 个血浆蛋白构建 LPAI，同时捕捉衰老累积负担与变化速度 [66]；UK Biobank 274,247 人的 MetBAG 独立测试 Pearson r 仅 0.25–0.42 [67]。**这些工作各自刻画了纵向动态的增量价值，但没有一个把转录组、代谢组、蛋白组的纵向变化在同一生成式或状态空间框架内联合建模**，也没有回答"哪一层组学的纵向变化最先偏离、可最早预警"这一机制性问题。

3. **共病结构与疾病亚型的发现方法正在分化，但缺乏统一评测基准**。ATM 用年龄依赖主题模型在 UK Biobank 282,957 人与 All of Us 211,908 人中识别 52 种共病异质性疾病、18 个亚型 PRS 显著异于同病其他亚型 [20]；VaDeSC-EHR 用 Transformer 变分自编码器结合 Weibull 混合生存分布把风险建模与聚类整合 [21]；另一路线用生成嵌入加 K-means 在逾 100,000 患者中为阿尔茨海默病和帕金森病各识别五个可复制亚型 [36]。**三者对"亚型"的定义、聚类数选择、外部验证标准均不统一，且都指出聚类数需预设、EHR 异质与缺失、外部验证有限** [21][36]，目前尚无公开的共病亚型基准或评测框架。

4. **跨祖源与跨性别的组学整合模型仍稀缺，且收益依赖研究设计而非样本量**。性别分层分析显示 69.1% 的蛋白存在性别差异，而遗传效应对蛋白靶点在两性间高度相似，仅 103 个 sd-pQTL [8]；ARIC 在欧裔与非裔中分别发现 2,004 与 1,618 个 cis 关联，多数重叠但存在人群特异位点 [25]。跨祖源 PRS 方面，多血统训练可减缓随血统分歧的精度衰减，但最大化样本量并非普遍最优 [45]；台湾精准医学计划基于 463,447 名汉族人构建的人群特异 PRS 优于欧洲为主模型 [46]。**这些结果共同指向一个尚未被系统回答的问题：在生成式轨迹模型或多组学整合模型中，祖源与性别分层应作为协变量、分层训练还是独立模型，目前没有方法学共识**。

5. **环境暴露层与遗传/组学层的整合严重不足**。UKB 492,567 人暴露组全关联与 45,441 人蛋白组衰老时钟分析发现，环境暴露对死亡与 25 种年龄相关病的解释度常高于基因组 [11]；节律紊乱指标基本独立于睡眠，可独立预测 98 种未来发病风险 [70]。**但现有生成式轨迹模型与多组学整合工作几乎都以遗传和分子层为主轴，环境暴露多作为协变量或事后解释，尚无把暴露组作为一等公民纳入生成式轨迹建模的公开工作**。

6. **公开基准与评测框架滞后于模型与资源的增长速度**。资源侧，UK Biobank 已发布覆盖 28 种疾病和 25 种数量性状的 PRS Release 并基准测试优于 81 个已发表 PRS [32]；GWAS Catalog 截至 2024 年 7 月含 625,113 个关联、>15.5K 性状和 >85K 数据集 [31]；UKB 外显子系统分析覆盖 4,529 个表型、8,074,878 个单变异和 75,767 个基因-注释组并公开 summary statistics 浏览器 [52]。**但模型侧缺乏与这些资源配套的、面向轨迹预测与共病亚型的标准化评测**：Foresight-England 因数据访问暂停无法导出定量结果 [3]，SurvivEHR 外部多国泛化未验证 [63]，GRASP 虽在 UKB、FinnGen、Mount Sinai 三系统验证但跨编码系统泛化仍是共同争议点 [62]。**"有资源、有模型、无统一评测"是本方向当前最突出的结构性缺口**。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 生成式疾病轨迹模型 | **朝阳** | 近两年集中出现生成式 transformer 做患者时间线/疾病自然史建模：[19]（Foresight，GPT 式患者时间线预训练）与 [1]（生成式 transformer 学习疾病自然史）把「EHR 序列 → 生成式预测」推到主刊级别；但方法路线尚未收敛——[21] 走纵向生存数据的深度表征聚类，[2] 走贝叶斯纵向 EHR+遗传发现，说明「生成式 vs 表征学习 vs 贝叶斯」并存，评测与基准缺位。 |
| 2.2 多组学与遗传整合 | **成熟（偏基础设施化）** | 大规模 pQTL/蛋白组-遗传图谱已形成标准范式：[5]（UKB 血浆蛋白组与遗传、健康关联，**1547 引用**）与 [50]（**454,787 人**外显子测序）确立了「大队列 + 组学 + 遗传」的规模化基线；方法层面 [26]（biobank 尺度混合模型关联）与 [57]（35 项血尿生物标志物遗传学）显示统计工具已收敛，新工作多为增量扩展与图谱补全。 |
| 2.3 医学 / EHR 基础模型 | **萌芽（方法早期，CNS 缺位）** | 奠基工作 [18]（Med-BERT）与 [17]（BEHRT）确立了结构化 EHR 预训练范式，但雷达样本中该节 **CNS 占比 0.0**、近两年仅见 [64]（EHRAgent，LLM 少样本表格推理）与 [62]（LLM 提升 EHR 模型迁移性）等零星探索，尚未出现大规模跨队列验证与统一基准。 |
| 2.4 组学衰老时钟与纵向多组学动态 | **朝阳（与衰老方向强交叉）** | 近两年出现多器官/纵向组学衰老指标：[67]（多器官代谢组生物学年龄关联心血管代谢病）与 [66]（纵向蛋白组衰老指数预测死亡、多病）把衰老时钟从「单时点预测」推向「纵向动态 + 人群健康结局」；[68]（UKB 运动逆转蛋白组衰老）进一步指向可干预性，但样本量小、指标未标准化。 |
| 3 数据与资源 | **成熟** | 队列资源本身已是领域公共底座：[12]（UK Biobank，**11473 引用**）与 [13]（UKB 深度表型+基因组，**8002 引用**）定义了「大队列+深表型」标准；[16]（FinnGen 隔离人群精细表型）与 [15]（All of Us）补齐跨队列多样性，资源层不再是瓶颈。 |
| 4 应用与结果 | **朝阳** | 应用端已产出可落地结果：[91]（从疾病轨迹深度学习预测胰腺癌风险）与 [85]（血浆代谢物刻画非传染性多病通路）证明「EHR/组学 → 疾病风险与共病结构」可行；[24]（Pan-UKB GWAS 提升发现与分辨率）与 [79]（BMI 多基因预测贯穿生命历程）显示跨队列、纵向应用正在扩张，但多为单点应用，缺统一评测。 |
| 5 评测、可复现性与争议 | **证据不足** | 雷达样本仅 2 篇：[28]（大规模 EHR 贝叶斯 Cox 推断）与 [92]（AI 研究共病的方法综述，**0 引用**），不足以判断该细分方向所处阶段；但这恰恰说明**评测/基准/可复现性是该方向的结构性缺口**。 |

**整体判断**：这个方向整体处于**朝阳期偏早期**——数据底座（UKB/FinnGen/All of Us）已成熟，多组学-遗传整合（2.2）方法收敛、进入增量阶段，而**生成式疾病轨迹（2.1）、EHR 基础模型（2.3）、组学衰老时钟（2.4）三条方法线尚未收敛**，雷达样本中 2.1 近两年占比 **0.9**、2.4 为 **0.8**，且 2.1 已出现 Nature 级工作（[1]），说明窗口期仍在，但**预计 12–24 个月内方法会快速收敛**，先发者将占据基准与数据接口。最大不确定性有三：一是**评测与可复现性缺位**（第 5 节仅 2 篇、CNS 占比 0.0），没有统一基准就无法判断谁的方法真正更好；二是**跨队列泛化**，EHR 编码体系、队列人群结构差异大，[62] 才刚开始处理迁移性；三是**生成式模型的因果/临床可解释性**，[2] 用贝叶斯框架补遗传发现，暗示纯生成式路线在机制解释上仍有短板。

**接下来怎么做**：
1. **用 UKB 纵向蛋白组 + EHR 做「生成式疾病轨迹 + 组学衰老时钟」的交叉切入点**：以 [5] 的 pQTL/蛋白组图谱为特征底座，套用 [1] 的生成式 transformer 做疾病自然史建模，再用 [66] 的纵向蛋白组衰老指数作为中间表型。现在做是因为 2.1 与 2.4 都处朝阳、尚未有人把两者缝合，且 UKB 蛋白组数据已公开可用。
2. **把类器官/多组学合作项目做成「人群队列验证层」**：类器官产生的是机制与扰动响应，正好补 [1] 这类纯观察性生成模型的因果短板；用 [50] 的外显子数据做胚系过滤、[57] 的生物标志物遗传结构做锚点，产出「类器官扰动 → 人群 pQTL/疾病轨迹」的可复现映射。
3. **抢占评测与基准空白（第 5 节证据不足即机会）**：以 [16]（FinnGen）与 [15]（All of Us）做跨队列复现集，参照 [28] 的贝叶斯大规模推断思路，构建 EHR 轨迹模型的统一评测框架。现在做是因为方法未收敛、基准未定，先定义指标者掌握话语权。
4. **用公共数据做低成本 demo，验证「EHR 基础模型 + 多组学」的迁移性**：以 [18]（Med-BERT）与 [17]（BEHRT）为基线，叠加  的 LLM 迁移思路，在 [24]（Pan-UKB）表型上做 zero/few-shot 迁移测试。现在做是因为 2.3 尚处萌芽、CNS 占比 0.0，小成本即可产出差异化结果。
5. **把共病结构发现作为「方法学新意」的落点**：用 [85]（代谢物-多病通路）与 [91]（疾病轨迹预测胰腺癌）的思路，结合 [92] 综述指出的共病 AI 方法缺口，做「生成式轨迹 → 共病模块 → 亚型」的端到端管线，产出可跨 [16] 与 [15] 复现的共病结构。

## 参考文献

1. Learning the natural history of human disease with generative transformers.. Nature 2025. https://doi.org/10.1038/s41586-025-09529-3
2. A Bayesian framework for longitudinal EHR and genetic discovery. Nature 2026. https://doi.org/10.1038/s41586-026-10780-5
3. Foresight-England: Development of a National-Scale Generative AI Model of Electronic Health Records for Medical Event Prediction across the COVID-19 Pandemic.  2026. https://arxiv.org/abs/2608.16273
4. Predicting Early Functional Decline from Longitudinal Laboratory and Vital Sign Trajectories: A Large-Scale Study Using the All of Us Research Program.  2026. https://arxiv.org/abs/2608.21589
5. Plasma proteomic associations with genetics and health in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06592-6
6. Atlas of the plasma proteome in health and disease in 53,026 adults.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.045
7. Metabolomic and genomic prediction of common diseases in 700,217 participants in three national biobanks.. Nature communications 2024. https://doi.org/10.1038/s41467-024-54357-0
8. Sex differences in the genetic regulation of the human plasma proteome.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59034-4
9. Evaluating Performance and Agreement of Coronary Heart Disease Polygenic Risk Scores.. JAMA 2025. https://doi.org/10.1001/jama.2024.23784
10. Longitudinal alignments and syntheses of multimodal clinical data for personalized medicine with the PULSE framework. Nature Computational Science 2026. https://doi.org/10.1038/s43588-026-01026-5
11. Integrating the environmental and genetic architectures of aging and mortality.. Nature medicine 2025. https://doi.org/10.1038/s41591-024-03483-9
12. UK Biobank: An Open Access Resource for Identifying the Causes of a Wide Range of Complex Diseases of Middle and Old Age. PLoS Medicine 2015. https://doi.org/10.1371/journal.pmed.1001779
13. The UK Biobank resource with deep phenotyping and genomic data. Nature 2018. https://doi.org/10.1038/s41586-018-0579-z
14. Whole-genome sequencing of 490,640 UK Biobank participants.. Nature 2025. https://doi.org/10.1038/s41586-025-09272-9
15. The “All of Us” Research Program. New England Journal of Medicine 2019. https://doi.org/10.1056/NEJMsr1809937
16. FinnGen provides genetic insights from a well-phenotyped isolated population. Nature 2023. https://doi.org/10.1038/s41586-022-05473-8
17. BEHRT: Transformer for Electronic Health Records. Scientific Reports 2019. https://doi.org/10.1038/s41598-020-62922-y
18. Med-BERT: pretrained contextualized embeddings on large-scale structured electronic health records for disease prediction. npj Digital Medicine 2020. https://doi.org/10.1038/s41746-021-00455-y
19. Foresight—a generative pretrained transformer for modelling of patient timelines using electronic health records: a retrospective modelling study. The Lancet Digital Health 2024. https://doi.org/10.1016/s2589-7500(24)00025-6
20. Age-dependent topic modelling of comorbidities in UK Biobank identifies disease subtypes with differential genetic risk. Nature Genetics 2023. https://doi.org/10.1038/s41588-023-01522-8
21. Deep representation learning for clustering longitudinal survival data from electronic health records.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56625-z
22. Identification of plasma proteomic markers underlying polygenic risk of type 2 diabetes and related comorbidities.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56695-z
23. An atlas of polygenic risk score associations to highlight putative causal relationships across the human phenome. bioRxiv 2018. https://doi.org/10.7554/eLife.43657
24. Pan-UK Biobank genome-wide association analyses enhance discovery and resolution of ancestry-enriched effects.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02335-7
25. Plasma proteome analyses in individuals of European and African ancestry identify cis-pQTLs and models for proteome-wide association studies. Nature Genetics 2022. https://doi.org/10.1038/s41588-022-01051-w
26. Mixed model association for biobank-scale data sets. Nature Genetics 2018. https://doi.org/10.1038/s41588-018-0144-6
27. SPA<sub>GRM</sub>: effectively controlling for sample relatedness in large-scale genome-wide association studies of longitudinal traits.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56669-1
28. Bayesian Cox regression for large-scale inference with applications to electronic health records. Annals of Applied Statistics 2021. https://doi.org/10.1214/22-aoas1658
29. Using Phecodes for Research with the Electronic Health Record: From PheWAS to PheRS. Annual Review of Biomedical Data Science 2021. https://doi.org/10.1146/annurev-biodatasci-122320-112352
30. A unidirectional mapping of ICD-8 to ICD-10 codes, for harmonized longitudinal analysis of diseases. European Journal of Epidemiology 2023. https://doi.org/10.1007/s10654-023-01027-y
31. The NHGRI-EBI GWAS Catalog: standards for reusability, sustainability and diversity.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1070
32. UK Biobank release and systematic evaluation of optimised polygenic risk scores for 53 diseases and quantitative traits. medRxiv 2022. https://doi.org/10.1101/2022.06.16.22276246
33. NOAH: Learning the Full Patient Journey. A Longitudinal Multimodal Time-Aware Model for Representation and Forecasting.  2026. https://arxiv.org/abs/2609.09140
34. MiGHT-EHR: A Multi-task Graph Transformer for Heterogeneous Temporal Electronic Health Records.  2026. https://arxiv.org/abs/2608.06430
35. EHR-MPC: Inference-Time Control for Sepsis Treatment with Generative Patient Digital Twins. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.08793
36. Subtyping Alzheimer's disease and Parkinson's disease using longitudinal electronic health records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01085-3
37. Rare variant associations with plasma protein levels in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06547-x
38. Atlas of plasma NMR biomarkers for health and disease in 118,461 individuals from the UK Biobank. Nature Communications 2023. https://doi.org/10.1038/s41467-023-36231-7
39. Genetic associations with ratios between protein levels detect new pQTLs and reveal protein-protein interactions. bioRxiv 2023. https://doi.org/10.1016/j.xgen.2024.100506
40. Multi-ancestry MHC-pQTL mapping reveals disease-linked HLA protein networks and shared genetic architecture.  . https://doi.org/10.21203/rs.3.rs-10956233/v1
41. Robust cis-by-trans epistasis in the human plasma proteome highlights an ABO-centered interaction network.. American journal of human genetics . https://doi.org/10.1016/j.ajhg.2026.09.003
42. Pan-UK Biobank GWAS improves discovery, analysis of genetic architecture, and resolution into ancestry-enriched effects. medRxiv 2024. https://doi.org/10.1101/2024.03.13.24303864
43. Global Biobank Meta-analysis Initiative: Powering genetic discovery across human disease. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100192
44. Global biobank analyses provide lessons for computing polygenic risk scores across diverse cohorts. medRxiv 2021. https://doi.org/10.1101/2021.11.18.21266545
45. All of Us diversity and scale yield context-dependent improvements in polygenic prediction.. Nature Genetics 2026. https://doi.org/10.1038/s41588-026-02734-4
46. Population-specific polygenic risk scores for people of Han Chinese ancestry.. Nature 2025. https://doi.org/10.1038/s41586-025-09350-y
47. Polygenic Prediction of Peripheral Artery Disease and Major Adverse Limb Events.. JAMA cardiology 2025. https://doi.org/10.1001/jamacardio.2025.1182
48. Exome sequencing and characterization of 49,960 individuals in the UK Biobank. Nature 2020. https://doi.org/10.1038/s41586-020-2853-0
49. Advancing human genetics research and drug discovery through exome sequencing of the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-021-00885-0
50. Exome sequencing and analysis of 454,787 UK Biobank participants. Nature 2021. https://doi.org/10.1038/s41586-021-04103-z
51. Rare variant contribution to human disease in 281,104 UK Biobank exomes. Nature 2021. https://doi.org/10.1038/s41586-021-03855-y
52. Systematic single-variant and gene-based association testing of thousands of phenotypes in 394,841 UK Biobank exomes. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100168
53. A fast and scalable framework for large-scale and ultrahigh-dimensional sparse regression with application to the UK Biobank. bioRxiv 2019. https://doi.org/10.1371/journal.pgen.1009141
54. Components of genetic associations across 2,138 phenotypes in the UK Biobank highlight adipocyte biology. Nature Communications 2019. https://doi.org/10.1038/s41467-019-11953-9
55. Disease prediction with multi-omics and biomarkers empowers case–control genetic discoveries in the UK Biobank. Nature Genetics 2024. https://doi.org/10.1038/s41588-024-01898-1
56. Genetically supported targets and drug repurposing for brain aging: A systematic study in the UK Biobank.. Science advances 2025. https://doi.org/10.1126/sciadv.adr3757
57. Genetics of 35 blood and urine biomarkers in the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-020-00757-z
58. Phenome-wide association studies across large population cohorts support drug target validation. Nature Communications 2018. https://doi.org/10.1038/s41467-018-06540-3
59. Mono- and biallelic variant effects on disease at biobank scale. Nature 2023. https://doi.org/10.1038/s41586-022-05420-7
60. Phenome-wide Burden of Copy Number Variation in the UK Biobank.. American Journal of Human Genetics 2019. https://doi.org/10.1016/j.ajhg.2019.07.001
61. GWAS of extended prescription analgesic use identifies genetic loci in chronic pain.. Nature communications 2026. https://doi.org/10.1038/s41467-026-71434-8
62. Large language models improve transferability of electronic health record-based predictions across countries and coding systems.. NPJ digital medicine 2026. https://doi.org/10.1038/s41746-026-02363-5
63. SurvivEHR: a competing risks, time-to-event foundation model for multiple long-term conditions from primary care electronic health records.  2025. https://doi.org/10.1101/2025.08.04.25332916
64. EHRAgent: Code Empowers Large Language Models for Few-shot Complex Tabular Reasoning on Electronic Health Records.. Proceedings of the Conference on Empirical Methods in Natural Language Processing. Conference on Empirical Methods in Natural Language Processing 2024. https://doi.org/10.18653/v1/2024.emnlp-main.1245
65. Longitudinal dynamics of gene expression and metabolomics in an aging population cohort.. Science 2026. https://doi.org/10.1126/science.aed6452
66. A Novel Longitudinal Proteomic Aging Index Predicts Mortality, Multimorbidity, and Frailty in Older Adults.. Aging cell 2025. https://doi.org/10.1111/acel.70317
67. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
68. Reversal of proteomic aging with exercise-results from the UK biobank and a 12-week intervention study.. npj aging 2025. https://doi.org/10.1038/s41514-025-00318-w
69. Estimation of physiological aging based on routine clinical biomarkers: a prospective cohort study in elderly Chinese and the UK Biobank.. BMC medicine 2024. https://doi.org/10.1186/s12916-024-03769-2
70. Molecular Circadian Disturbance in Human Blood Independently Predicts Multi-Disease Risk and Maps to Hepatic metabolism Pathways.  . https://doi.org/10.21203/rs.3.rs-11120748/v1
71. UK Biobank-A Unique Resource for Discovery and Translation Research on Genetics and Neurologic Disease.. Neurology. Genetics 2025. https://doi.org/10.1212/nxg.0000000000200226
72. Robust replication of associations across patient-mediated and provider-sourced EHR data in the All of Us research program. npj Digital Public Health 2026. https://doi.org/10.1038/s44482-026-00032-8
73. Lessons from national biobank projects utilizing whole-genome sequencing for population-scale genomics.. Genomics & informatics 2025. https://doi.org/10.1186/s44342-025-00040-9
74. Trends in large-scale human population cohorts.. Trends in Genetics 2026. https://doi.org/10.1016/j.tig.2026.08.002
75. Software Application Profile: PHESANT: a tool for performing automated phenome scans in UK Biobank. International Journal of Epidemiology 2017. https://doi.org/10.1093/ije/dyx204
76. Exploring and visualizing large-scale genetic associations using PheWeb. Nature Genetics 2020. https://doi.org/10.1038/s41588-020-0622-5
77. Quality control and removal of technical variation of NMR metabolic biomarker data in ~120,000 UK Biobank participants. Scientific Data 2021. https://doi.org/10.1038/s41597-023-01949-y
78. A national-scale digital atlas of recorded care patterns across more than 1000 diagnostic categories using real-world health data: a retrospective observational study.  . https://doi.org/10.64898/2026.09.16.26363186
79. Polygenic prediction of body mass index and obesity through the life course and across ancestries.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03827-z
80. MSGene: a multistate model using genetic risk and the electronic health record applied to lifetime risk of coronary artery disease. Nature Communications 2024. https://doi.org/10.1038/s41467-024-49296-9
81. Dynamic Importance of Genomic and Clinical Risk for Coronary Artery Disease Over the Life Course. medRxiv 2023. https://doi.org/10.1101/2023.11.03.23298055
82. Machine Learning‐Driven Prediction of Coronary Artery Disease Risk Based on UK Biobank Plasma Proteomics. Journal of the American Heart Association : Cardiovascular and Cerebrovascular Disease 2026. https://doi.org/10.1161/JAHA.125.047248
83. Proteomics mediates the effects of biological aging on the progression of cardio-renal-metabolic comorbidity: a UK biobank cohort study.. Cardiovascular diabetology 2025. https://doi.org/10.1186/s12933-025-03035-6
84. MetaboHealth and Metabolic Vulnerability Index as Risk Factors for Cardio-Renal-Metabolic Multimorbidity: A Large-Scale Prospective Cohort Study.. Diabetes, obesity and metabolism 2026. https://doi.org/10.1111/dom.71112
85. Plasma metabolites to profile pathways in noncommunicable disease multimorbidity. Nature Medicine 2021. https://doi.org/10.1038/s41591-021-01266-0
86. UKB-MDRMF: a multi-disease risk and multimorbidity framework based on UK biobank data.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58724-3
87. PheMIME: an interactive web app and knowledge base for phenome-wide, multi-institutional multimorbidity analysis.. Journal of the American Medical Informatics Association : JAMIA 2024. https://doi.org/10.1093/jamia/ocae182
88. Deep phenotyping of heart failure with preserved ejection fraction through multi-omics integration.. European journal of heart failure 2025. https://doi.org/10.1002/ejhf.70041
89. Explainable Plasma Proteomics–Based Machine Learning for Osteoporosis Diagnosis, Prognosis, and Protein Biomarker Discovery in the UK Biobank. The FASEB Journal 2026. https://doi.org/10.1096/fj.202600647R
90. Leveraging large-scale biobank EHRs to enhance pharmacogenetics of cardiometabolic disease medications.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58152-3
91. A deep learning algorithm to predict risk of pancreatic cancer from disease trajectories. Nature Medicine 2023. https://doi.org/10.1038/s41591-023-02332-5
92. From data to knowledge: artificial intelligence methods for studying comorbidity in electronic health records. The European Physical Journal Special Topics 2026. https://doi.org/10.1140/epjs/s11734-026-02571-w
93. An atlas of genetic associations in UK Biobank. Nature Genetics 2017. https://doi.org/10.1038/s41588-018-0248-z
94. Comparative analysis of the Mexico City Prospective Study and the UK Biobank identifies ancestry-specific effects on clonal hematopoiesis.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02085-6
