# 人群健康与多组学 AI · 方向背景报告

证据 126 篇 · 覆盖度 0.80 · 第 16 轮 · 更新 2026-11-22 · 数字核验删句 1

## 本次变更

- 新增 [53] Machine learning-based proteomics analysis identified 23 protein biomarkers for enhanced risk prediction of myocardial infarction in Chinese and Europeans.
- 新增 [54] Prospective multi-omic profiling identifies predictive and genetically supported molecular determinants of incident epilepsy
- 新增 [32] Identifying cohorts at elevated risk of cancers using generative modeling of patient health states
- 新增 [59] Regularized ensemble polygenic risk prediction with GWAS summary statistics.
- 新增 [45] Optimizing phenotype scale improves genetic analyses in large-scale biobanks.

## 摘要（TL;DR）

- Foresight 强调结构化数据之外约 **80% 的自由文本**，在 3 家医院数据上覆盖 18 类 SNOMED 概念 [1]。
- Foresight-England 使用 243M 参数解码器与约 **6100 万人**纵向 EHR，但 NHS England 暂停数据访问导致定量结果无法导出 [2]。
- NOAH 基于 MIMIC 家族 **559M 事件、299,000 患者**训练时间感知变分隐空间，支持零样本分类与反事实干预模拟 [3]。
- ALADYNOULLI 在 3 个生物库 **n>683,000**、348 种疾病上识别出 **21 个可复制特征**，基于特征的 GWAS 发现 **151 个全基因组显著位点** [4]。
- EHR-MPC 在 Mass General Brigham **8 家医院** ICU 队列上把脓毒症治疗优化重构为推理时控制问题，离线策略性能与强化学习基线相当 [5]。
- LifeLong Digital Twin 在 25 个疾病终点上报告 **16 个模型-读出比较全部提升**，但自述缺乏配对不确定性、疾病支持计数与组件消融，尚未确立统计显著性 [6]。
- All of Us 研究（**N=297,861**，11.1% 病例）仅用 12 项常规生物标志物 3 年轨迹特征，LightGBM 预测临床前功能衰退 AUROC **0.797 vs 0.755**（P<0.001）[7]。
- UK Biobank 454,787 人外显子数据得到 8,865 个显著关联、涉及 564 个基因，其中 **91% 不能由常见变异 LD 解释** [8]。
- UKB-PPP 对 54,219 名参与者检测 2,923 种蛋白，发现 14,287 个主要遗传关联，**81% 为既往未报道** [9]。
- All of Us、Penn Medicine 与 UCLA 三个生物库 171,095 人、48 个冠心病 PRS 的比较显示，群体水平表现相似的 PRS 在个体层面一致性差 [10]。
- 27 个 UK Biobank 性状上，AlphaGenome 与 Borzoi 增加位点发现但低于 baselineLD（中位 1.8%、3.8% 对 5.1%），GPN-Star 反而减少发现 [11]。
- HELICS 在 **chr15 18,784 SNP** 及全基因组 **600,336 SNP** 基准上于 MAF、LD 和隐私代理指标优于 HAPNEST 等基线，但低 MAF 变异 R² 偏低且生成样本 NN IBS 相似度较高 [12]。

## 1 背景与定义

人群健康与多组学 AI 的边界，首先由“队列规模”与“数据层次”共同划定。它区别于单中心临床预测模型的地方在于：建模对象是生物样本库级别的纵向人群，输入至少包含 EHR 诊断/就诊序列，通常叠加胚系遗传、血浆蛋白组、代谢组或甲基化中的一层或多层，输出则落在疾病风险、健康轨迹、共病结构与亚型三类目标上。UK Biobank 约 **50 万** 40–69 岁参与者的基线评估、生物样本与健康记录链接设计，从一开始就是为“20 年随访累积足够事件数”而建的 [13]；其基因组资源随后扩展到约 **9600 万变异插补** [14]，再到 **490,640 人**、平均 **32.5×** 的全基因组测序 [15]。All of Us 则以多样性为目标，计划招募至少 **100 万** 人，截至 2019 年 7 月已有超过 175,000 人贡献生物样本、**>80%** 来自历史上研究不足群体 [16]；FinnGen 走的是另一条路——**224,737 人** 插补基因型加 **1,932 个终点**，依托全国登记与隔离人群富集的低频有害等位 [17]。**这三类资源分别代表“深度表型”“人群多样性”“登记链接与隔离人群”，也决定了同一方法在不同队列上的可复现性边界。**

演化脉络上，这个方向经历了三次重心转移。第一次是从“关联”到“表征”：早期工作以 GWAS/PheWAS 汇总统计为核心，如 GeneATLAS 覆盖 9,113,133 个变异关联 [18]，BOLT-LMM 用全部 459K 欧洲样本把 23 个性状的独立位点由 5,839 增至 10,759 [19]；随后 BEHRT、Med-BERT 把患者历史当作概念序列学习个体表示 [20][21]，EHR 从“表型来源”变成“建模对象”。第二次是从“表征”到“生成”：Foresight 用生成式预训练 Transformer 预测未来疾病与生物医学概念 [1]，Delphi-2M 在 UK Biobank 训练、丹麦登记验证，同时预测 1000 多种疾病未来发生率并模拟个体终身轨迹 [22]，Foresight-England 把规模推到约 **6100 万人** 纵向 EHR [2]。第三次是从“预测”到“结构发现与控制”：ALADYNOULLI 用贝叶斯生成框架联合建模纵向诊断、年龄与多基因风险，在 3 个生物库 **n>683,000** 上识别 **21 个可复制特征** [4]；EHR-MPC 把生成式数字孪生用于推理时治疗规划 [5]。**这条脉络的关键判断是：模型容量与队列规模的增长并未自动带来临床可用性，反而把“可复现性”和“个体层面一致性”推到了前台。**

核心问题可以归为四组。其一是**表型与编码的可比性**：Phecodes 依赖 ICD 编码定义病例/对照，存在编码误差与表型异质性 [23]；ICD-8 到 ICD-10 的单向映射虽能桥接丹麦自 1965 年以来的数据，却不提供回映射 [24]；All of Us 的 PME 与 HPO 两种 EHR 来源在患病率、PheWAS 与已知基因型-表型关联复制率上均存在差异，WGS 覆盖率为 **35.2% vs 83.2%** [25]。其二是**跨队列与跨祖源迁移**：GRASP 用 LLM 把医学编码映射到共享语义空间，在 UKB **391921**、FinnGen **253991**、Mount Sinai **386755** 人上验证，平均 ΔC-index 在芬兰高 **88%**、美国高 **47%** [26]；但 48 个冠心病 PRS 在三个生物库 171,095 人上的比较显示，群体表现相似的评分在个体层面一致性差 [10]。其三是**多组学层次的整合深度**：UKB-PPP 在 54,219 人中检出 14,287 个主要遗传关联、**81% 为既往未报道** [9]；53,026 人、2,920 种蛋白的图谱报告 183 种疾病判别 AUC>0.80，并通过 pQTL 确定 474 个因果蛋白 [27]；但 ARIC 与 MHC 区的工作都表明，单一欧洲裔、单一平台的 pQTL 图谱不足以覆盖调控架构 [28][29]。其四是**评估与基准的缺位**：All of Us v9 的家族感知基准把整个家族组分固定分配到发现、校准与测试集以消除亲属泄漏 [30]，而基因组基础模型在 27 个 UK Biobank 性状上尚未超越标准注释（AlphaGenome 与 Borzoi 中位 1.8%、3.8% 对 baselineLD 5.1%）[11]。**这四组问题共同界定了方向的“未完成”状态：数据规模已足够大，但表型语义、人群覆盖与评测协议尚未收敛。**

因此，本方向当前的合理定义应包含三层：**数据层**是万人以上、带纵向 EHR 与至少一层组学的队列或其联合；**方法层**是生成式/基础模型、纵向轨迹建模、共病结构学习与多组学-遗传整合，而非单病种评分改良；**验证层**要求跨队列或跨祖源的可复现性证据，或至少公开数据与代码。按此边界，纯影像 AI、单中心小样本关联、无公开数据也无代码的预测模型均不在范围内。队列发展趋势综述也指出，组学技术、EHR 普及与 AI 正推动队列从描述性关联转向机制发现、精细风险分层与遗传导向的治疗开发，并日益全球化与多样化 [31]——**“全球化与多样化”既是方向的机会，也是它目前最大的证据缺口。**

## 2 方法学


### 2.1 生成式疾病轨迹模型

在纵向电子健康记录（EHR）上学习疾病自然史的主流路线，是把患者病史当作离散事件序列做自回归生成。Foresight 则强调结构化数据之外约 **80% 的自由文本**，在 3 家医院的躯体和精神健康数据上覆盖 18 类 SNOMED 概念，支持日/周/月不同时间分辨率 [1]。规模化的极端案例是 Foresight-England：243M 参数解码器、约 **6100 万人**纵向 EHR，但 NHS England 暂停数据访问导致定量结果无法导出，论文只留下分词、训练与评估的方法学模板 [2]。GenEHR 同样走自回归路线，显式建模就诊间隔并融合诊断、用药、检验值与操作，用于 17 种癌症风险分层并在五个大型 EHR 队列验证 [32]；NOAH 进一步把图像、时序、分类与文本纳入时间感知变分隐空间，基于 MIMIC 家族 **559M 事件、299,000 患者**训练，支持零样本分类与反事实干预模拟 [3]。

与纯预测路线不同，ALADYNOULLI 把生成模型用于暴露潜在结构：以概率混合而非混合概率的形式联合建模纵向诊断、年龄与多基因风险，在 3 个生物库 **n>683,000**、随访 52 年、348 种疾病上识别出 **21 个可复制特征**，跨队列组成保留中位 80%，基于特征的 GWAS 发现 **151 个全基因组显著位点**，包括单性状分析遗漏的心血管关联 [4]。这条线索与亚型聚类工作相呼应：一项 Transformer+K-means 框架在 CPRD Aurum 与 UK Biobank 逾 10 万患者中为 AD 和 PD 各识别出 5 个可复制亚型，亚型间 5 年死亡与住院预后、共病及基因型存在差异 [33]；VaDeSC-EHR 则把 Weibull 混合生存分布直接嵌入变分自编码器，使聚类与风险建模同步完成，避免先聚类再分层的异质性残留 [34]。两者的差别在于前者以诊断前时间戳序列做无监督分型、后者以生存结局驱动表征学习，是否应把结局信号纳入聚类本身仍是开放问题。

生成式轨迹模型的下游用法开始从“预测”转向“控制”。EHR-MPC 把脓毒症治疗优化重构为推理时控制问题：先训练生成式 EHR 患者数字孪生预测干预下轨迹，再用模型预测控制在推理阶段规划治疗，在 Mass General Brigham **8 家医院** ICU 队列上离线策略性能与强化学习基线相当、模拟性能更优 [5]。LifeLong Digital Twin 则提出把 Life Events 组织为每日 Health States 并累积为 Lifelong Health Context 的统一范式，配合 Agent Harness 整合多模态证据，在 25 个疾病终点、3 类任务、4 个语言模型上报告 **16 个模型-读出比较全部提升**，疾病识别 F1 从 0.422 升至 0.504（Context）与 0.515（Harness）[6]；但该工作自述缺乏配对不确定性、疾病支持计数与组件消融，尚未确立统计显著性，其增益幅度不宜与上述其他研究报告的数字直接比较。

值得注意的是，并非所有“轨迹”建模都依赖生成式架构。一项 All of Us 研究（**N=297,861**，11.1% 病例）仅提取 12 项常规生物标志物 3 年轨迹的斜率、变异性等特征，用 LightGBM 预测临床前功能衰退，AUROC **0.797 vs 0.755**（P<0.001），匹配分析为 0.727 vs 0.680，并可提前 3–12 个月持续预测 [7]；MiGHT-EHR 用异质时序图 Transformer 加双平衡多任务学习，在 MIMIC-III/IV 四任务上平均超越 SOTA，死亡率与再入院提升尤为显著 [35]。这些结果提示，在结构化信号充分、终点明确的场景下，轻量轨迹特征或图结构模型可能与大规模生成模型形成竞争；而生成式方法的独特价值更多体现在多模态融合、反事实模拟与跨病种联合建模上。共同的方法学约束也很清楚：多数工作报告依赖登记或诊断编码、外部验证局限于少数队列（如 UK Biobank、MIMIC），Foresight 作者明确其当前形式不宜直接用于临床决策支持 [1]，EHR-MPC 的仿真评估与真实临床之间亦存在差距 [5]。

### 2.2 多组学与遗传整合

在生物样本库尺度上，多组学与遗传数据的整合首先体现为对遗传关联本身的系统化编目。UK Biobank 452,264 名欧洲裔参与者的 118 个连续性状与 660 个二分类性状被汇总为 **GeneATLAS**，覆盖 9,113,133 个遗传变异关联，并可下载超 3000 万插补变异的汇总统计 [18]。在方法层面，**BOLT-LMM** 在全部 459K 欧洲样本上保留相关个体运行，身高的统计功效等效于 650K 样本，23 个性状的独立位点由 5,839 增至 10,759 [19]；跨祖源方面，混合模型关联加荟萃分析覆盖 7,271 个表型，新发现 14,676 个仅欧洲祖源分析未检出的位点 [36]。这些工作共同把「基因型—表型」关联从单性状扩展到表型组，但多数仍以欧洲裔为主。

罕见编码变异的贡献通过外显子测序被系统刻画。UK Biobank 454,787 人的外显子数据识别出 12 million 编码变异，与 3,994 个健康表型关联得到 8,865 个显著关联、涉及 564 个基因，其中 **91% 不能由常见变异 LD 解释**，81% 可复制 [8]。另一项 281,104 人的外显子 PheWAS 覆盖 17,361 个二分类与 1,419 个定量表型，识别 632 个全基因组显著 ExWAS 变异 [37]；394,841 名欧洲裔外显子的系统分析则测试了 8,074,878 个单变异和 75,767 个基因-注释组 × 4,529 表型 [38]。资源建设方面，首批 49,960 人外显子释放约 4 million 编码变异，其中 198,269 个为预测 LOF [39]；UKB-ESC 首批 200,643 人数据含约 10M 变异、453,733 个 LOF [40]。不同规模研究给出的显著关联数不可直接比较，但均指向罕见变异在常见病遗传结构中不可忽略。

非加性与非编码结构的工作补充了加性 GWAS 的盲区。FinnGen 176,899 名芬兰人的 44,370 个编码变异对 2,444 个疾病表型做加性与隐性扫描，显示纯合子富集可提升隐性致病变异检出，且同一变异在杂合与纯合状态可呈现不同表型 [41]。UK Biobank 472,228 人芯片数据的 CNV 全表型分析覆盖 >3,000 个性状，发现 16p11.2、22q11.2、9p23 等位点关联 [42]。在 399,943 名 UK Biobank 个体、2,906 个血浆蛋白和 55 个数量性状上，正交等位基因重编码框架发现约三分之一同源基因-蛋白关系呈非线性剂量效应，且该方法在 HWE 偏离下保持校准（λGC=0.94），而标准重编码膨胀至 λGC=78.3 [43]。表型尺度问题同样影响结论：UK Biobank 32 个表型中，幂变换可解释 **45%** 的多基因评分 G×E 信号 [44]；SIQReg 在 25 个性状中 24 个拒绝默认尺度，并消除含 97% 方差数量性状位点的非加性信号 [45]。这些结果提示，部分「交互」或「非加性」信号可能源于尺度选择而非真实生物学。

血浆蛋白组是整合遗传与分子表型最成熟的层面。**UKB-PPP** 对 54,219 名参与者检测 2,923 种蛋白，发现 14,287 个主要遗传关联，**81% 为既往未报道**，精细映射出 29,420 个独立信号 [9]；同一队列 49,736 人的罕见编码变异分析识别 5,433 个罕见基因型-蛋白关联（81% 既往 GWAS 未检出）和 1,962 个基因水平关联，STAB1/STAB2 分别关联 77 和 41 个蛋白 [46]。蛋白组图谱将关联推向疾病：53,026 人、2,920 种蛋白的分析报告 168,100 个蛋白-疾病关联和 554,488 个蛋白-性状关联，183 种疾病判别 AUC>0.80，并通过 pQTL 确定 474 个因果蛋白 [27]。方法上，蛋白比值 GWAS 复制 4,248 个 rQTL，显著 p-gain 蛋白对富集已知互作 **7.6 倍**，较单蛋白 GWAS 新增 24.7% 遗传信号 [47]；cis-by-trans 上位效应分析则识别出以 ABO 为中心的互作网络 [48]。

蛋白组遗传调控的祖源与性别异质性得到专门检验。ARIC 中 7,213 名欧裔与 1,871 名非裔的 4,657 种蛋白分析发现欧裔 2,004 种、非裔 1,618 种蛋白有 cis 关联，多数共享但存在人群特异 pQTL [28]；MHC 区多祖源 pQTL 映射在 2,920 种蛋白中鉴定 13 个 cis、606 个 trans 关联，多数跨祖源一致，东亚人群出现 EDAR 祖先富集关联 [29]。性别方面，Fenland 与 UK Biobank 合计 30,307 名女性与 26,058 名男性、>5,800 个蛋白靶点的分析显示 **69.1%** 蛋白水平存在性别差异，但遗传效应对蛋白靶点的影响跨性别高度相似，仅 103 个 sd-pQTL [49]。结构变异层面，54,306 名 UK Biobank 参与者中插补的 54,578 个 SV 与 15,826 个 VNTR 共同解释蛋白丰度遗传力约 **8.0%**，鉴定 8,065 个 SV-蛋白与 4,101 个 VNTR-蛋白独立关联 [50]。这些结果一致表明，单一欧洲裔、单一平台的 pQTL 图谱不足以覆盖调控架构。

代谢组与蛋白组评分被用于疾病风险预测，并与多基因评分直接对照。三国生物库 700,217 人的 NMR 代谢组研究训练 12 种高 DALY 疾病的 Cox 模型，多数纳入超过半数 36 个代谢标志物，并实现跨三库重复 [51]；UK Biobank 118,461 人、249 个 NMR 指标的分析构建了与 700 多种疾病的关联图谱，并在 THL Biobank 3 万余人重复验证 [52]。蛋白组评分方面，中国 4,000 名成人联合 Olink 与 SomaScan 测量逾 9,500 种蛋白，识别 **23 个心肌梗死蛋白标志物**，并在 37,187 名欧洲人中外部验证 [53]；UK Biobank 5.3 万人的癫痫分析识别 116 种相关蛋白，以 NEFL（HR=2.03）和 GDF15（HR=1.73）为首 [54]。多组学评分的整合尝试也已出现：UK Biobank 50,673 人基于 999 种蛋白构建疾病特异评分，并在 PURE 9,358 人验证，进一步整合 2,279 个多基因评分与 479 个 DNA 甲基化评分构建 4 种 **MEGASCORE** [55]。这些研究报告的预测增益多来自同一研究内部的对照，跨研究数值不宜直接比较。

多基因评分本身的方法学差异与个体层面局限构成另一条主线。GBMI 在 9 个生物样本库、14 个疾病终点上比较 P+T 与 PRS-CS，发现 **PRS-CS 总体优于 P+T**，且欧洲 LD 面板预测精度相当或更高 [56]；All of Us 245,388 全基因组序列加 UK Biobank 的 32 个性状分析显示，增加多样性提升部分性状精度，但最大化样本量并非普遍最优，PRS 精度随血统分歧线性下降、多血统训练可减缓 [57]。台湾 TPMI 463,447 名汉族人的全表型 GWAS 与 PRS 建模在 TWB、UKB、All of Us 验证，支持汉族特异 PRS 优于欧洲为主模型 [58]。然而个体层面一致性存在争议：All of Us、Penn Medicine 与 UCLA 三个生物库 171,095 人、48 个冠心病 PRS 的比较显示，群体水平表现相似的 PRS 在个体层面一致性差（ICC 与 Light κ 低）[10]。改进方向包括仅用汇总统计的正则化集成 PRS，在人群内及跨人群持续优于现有最先进方法 [59]，以及预训练 PRS 的自适应提升框架，模拟中各场景 R² 普遍优于基线且噪声选择比例 <28% [60]。

将 PRS 与分子表型连接，可把统计关联推进到机制与靶点。UKB-PPP 中全基因组 T2D PGS 关联 **648 个蛋白**，其中 617 个复制，分区 PGS 关联不同生物过程相关蛋白 [61]；35 项血尿标志物的遗传分析识别 5,794 个独立位点与 51 个因果关系，多 PRS 模型在 FinnGen 135,500 人中改善慢性肾病、2 型糖尿病、痛风与酒精性肝硬化的风险分层 [62]。PRS 全表型关联图谱以 162 个 PRS × 551 个表型、89,262 次检验提示潜在因果，但明确指出水平多效性可导致假阳性 [63]；跨四队列最多 697,815 人的 PheWAS 则用 19 个候选药物靶点验证了多效性信号对疗效与安全性的提示价值 [64]。冠心病方向，526 个显著变异 × 78 个相关表型的潜在因子分解得到 **8 个遗传组分**，并据此构建过程特异性 pPRS，在 UK Biobank 458,905 人中验证 [65]。这些工作显示，PGS 与蛋白组的配对能揭示分区生物学，但因果解释仍依赖 MR 假设。

组学整合也被用于解析特定基因、特定疾病的中介通路。APOE4 与痴呆之间，UK Biobank 神经影像 58,876 人、蛋白组 51,623 人与代谢组 267,627 人的多模态中介分析区分了全因痴呆、阿尔茨海默病与血管性痴呆的共享及特异通路 [66]；All of Us 367,757 名、六个祖源群体的 APOE 全表型分析识别 **27 个相关表型**，集中于神经与脂质性状，5 个脂质性状女性效应更大、9 个关联具祖源特异性 [67]。脑老化方向，UK Biobank MRI 脑龄深度学习模型在三个外部数据集验证，BAG 的 GWAS 发现 2 个新位点与 7 个已知位点，整合 eQTL/pQTL 的 MR 与共定位优先 7 个可成药基因 [68]。衰老与暴露组方面，UK Biobank 492,567 人的暴露组全关联与 45,441 人蛋白组衰老时钟结合，识别 25 个独立暴露，并发现环境暴露对死亡与 25 种年龄相关病的解释度常高于基因组 [69]；All of Us 10,043 人、5,416 种蛋白的分析则显示蛋白暴露特征跨人群基本一致，仅 <1% 蛋白存在显著异质性，BMI 为例外 [70]。

跨组学层的 QTL 与多模态补全进一步扩展了整合的边界。All of Us 祖源多样化参与者的蛋白组（N=10,043）与转录组（N=9,043）e/s/pQTL 分析检出 **182,246 个 QTL**，54,255 个精细定位到罕见变异，59.4%（32,235 个）解析为单一因果变异，罕见变异效应富集于孟德尔疾病基因（OR=1.4）与获批药物靶点 [71]。PULSE 纵向自监督框架在 UK Biobank 上从稀疏常规血检生成代谢组与蛋白组谱，生成代谢组优于所有基准方法，生成蛋白组对 6 种常见病 AUC 达 **0.72–0.83**，接近真实蛋白组数据 [72]。罕见变异功能注释方面，KASM 在 UK Biobank 与 All of Us 共 786,871 人外显子组、26 个复杂性状上整合 35 个蛋白结构与功能注释 [73]；慢性疼痛的处方定义 GWAS 在 UK Biobank 与 FinnGen 各约 50 万人中识别 140 个关联，其中 **78 个为新发现** [74]。这些结果把整合从「关联并列」推向「跨分子层因果链」，但多数仍缺乏功能实验验证。

统计工具与评估基准的进展决定了上述整合的可信度。纵向性状方面，SPA_GRM 在 UK Biobank 79 个纵向性状上控制 I 型错误并识别 7,463 个遗传位点 [75]；fastGxE 控制多基因效应、多基因交互与噪声异质性，在大型生物样本库中实现 **32.98 倍以上**速度提升 [76]，但另一篇同方法摘要信息有限、未给出建模策略与定量结果 [77]。超大规模稀疏回归的 BASIL 面向约 50 万人、>80 万 SNP 的数据，解决内存与效率瓶颈并保证 Lasso 解精确 [78]。评估层面，All of Us v9 的家族感知基准将整个家族组分固定分配到发现、校准与测试集，以消除亲属数据泄漏并区分仅 AoU 训练与外部 GWAS 汇总统计两类策略 [30]；SNPBERT 基于 485,923 名参与者基因型自监督预训练，嵌入效果与 PCA 相当（UKB 子集 ARI 0.93 对 0.92），微调后风险评分与 PRS 互补 [79]。值得注意的是，基因组基础模型尚未超越标准注释：27 个 UK Biobank 性状上，AlphaGenome 与 Borzoi 增加位点发现但低于 baselineLD（中位 1.8%、3.8% 对 5.1%），GPN-Star 反而减少发现 [11]。

跨祖源与跨队列的比较还暴露出代表性不足这一系统性约束。GBMI 覆盖 23 个生物样本库、220 万人、14 个疾病终点，六大祖源中欧裔 1.4M、东亚 415K，但祖先代表性仍不均 [80]；墨西哥城前瞻队列 136,401 人与 UK Biobank 416,118 人的克隆性造血比较显示，MCPS 中 CH 显著更少（调整 OR=0.59），且 CH 频率与欧洲祖源比例正相关（调整 beta=0.84），并发现祖先特异风险变异 [81]。外周动脉疾病的 PRS-PAD 在 UKB 400,533、AoU 218,500、MGBB 32,982 人中验证风险分层 [82]，但队列仍以欧美为主。这些证据共同说明，多组学与遗传整合的发现能力在扩张，而人群覆盖与个体层面可迁移性仍是主要争议点。

### 2.3 医学 / EHR 基础模型

基于Transformer的EHR基础模型沿着两条技术路线展开。**BEHRT**将患者历史视为医学概念序列，利用就诊位置、年龄和事件顺序学习个体表示以预测未来诊断，在多项任务上优于Deepr、RNN、LSTM和RETAIN等基线[20]；**Med-BERT**则把BERT迁移到结构化EHR诊断序列，先在大规模ICD数据上自监督预训练再微调，在糖尿病、心衰等预测任务上优于BEHRT、G-BERT及任务内训练模型，且在标注样本有限时提升更明显[21]。两者均受限于仅用诊断编码、跨机构泛化未充分验证[20][21]。在时间维度上，**SurvivEHR**引入竞争风险时间事件预训练目标，基于英国初级保健**2300万患者、76亿编码事件**学习患者轨迹，风险分层超越基准生存模型并支持低资源微调迁移，但外部多国泛化尚未验证[83]。

跨机构迁移是另一条主线。**GRASP**用大语言模型将医学编码映射到共享语义空间并结合transformer预测，在UKB **391921**、FinnGen **253991**、Mount Sinai **386755**人上验证，其平均ΔC-index较语言无关模型在芬兰高**88%**、美国高**47%**，且62%疾病与多基因风险评分的相关性显著更高[26]。与之互补，**EHRAgent**让LLM智能体自主生成并执行代码，将多表EHR推理形式化为工具使用规划，在三个真实EHR数据集上成功率最高超最强基线**29.6%**，少样本即可处理复杂临床查询，但依赖代码执行反馈迭代且仅在三个数据集验证[84]。前者面向跨编码系统的预测迁移，后者面向临床医生的自然语言交互，二者共同显示LLM正在把EHR基础模型的能力从单一编码体系内的预测扩展到语义对齐与工具化推理。

### 2.4 组学衰老时钟与纵向多组学动态

纵向多组学衰老研究的核心进展，是把时钟从单时点横断面估计推进到对个体轨迹的刻画。在 **335 名女性、8 年随访**的全血队列中，**5,061 个基因和 181 个代谢物**随时间变化，且个体轨迹常偏离群体水平趋势，变化受遗传、昼夜节律、季节和污染物影响[85]。与之呼应，ARIC 三次访视的蛋白组数据经 FPCA 加 Cox 弹性网构建纵向蛋白衰老指数 **LPAI**，在 MESA 验证，同时捕捉衰老累积负担与变化速度，较单时点蛋白时钟提供额外预测信息[86]。两条路线都强调纵向成分的价值，但前者侧重轨迹异质性与暴露因素，后者侧重死亡、多病共存和衰弱的预测效用，样本平台与随访间隔也不同，尚不能直接比较效应大小。

在时钟构建的组学层次上，不同工作覆盖了代谢组、蛋白组与临床指标。UK Biobank **274,247 人**的 **107 个血浆非衍生代谢物**被用于构建 5 个器官特异性代谢组生物年龄 MetBAG，独立测试 Pearson r 为 **0.25–0.42**，关联 **525 个疾病终点**并预测 14 类疾病与死亡风险[87]；另一项工作则为 **409,206 名**参与者的 **14 个器官**整合 NMR 代谢组、Olink 蛋白组和临床表型，发现年龄加速与死亡风险是器官生物学的不同维度，具有可分离的表型、分子和遗传结构[88]。这两项研究提示，同一多组学框架下“衰老程度”与“死亡风险”未必是同一维度，评估时钟时应区分预测目标。基于常规指标的路线则更贴近应用：DFTJ 中国老年人 **36 项临床指标**经限制立方样条 Cox 捕捉 U 型关系构建 PAI/ΔPAI，并在 UK Biobank 验证其预测死亡、心血管病及 **9 种慢性病**风险[89]；ClinicalAge 则从 UK Biobank 与 CPRD Aurum 的纵向电子健康记录轨迹估计衰老程度并评估发病与死亡风险[90]。前者训练人群以中国老年人为主，后者依赖 EHR 记录质量，外推性均受限。

动态性的另一来源是干预与节律。UK Biobank **45,438 人**中体力活动越高 ProtAgeGap 越低，ProtAgeGap 与 2 型糖尿病风险 **HR=1.06**、高活动交互 **HR=1.05**[91]；在 **26 名男性**的 12 周监督运动研究中，ProtAgeGap 下降相当于 **10 个月**，但干预样本量小、以观察性关联为主[91]。节律层面，UK Biobank **420,746 人**的 **312 种**血液学、生化与代谢分子与采血时间广泛关联，所推导的节律紊乱基本独立于睡眠，可独立预测 **98 种**未来发病风险并映射到肝脏代谢通路[92]。这些结果共同表明，纵向多组学时钟的“变化”既可能来自行为干预，也可能来自采样时相与节律紊乱；若不在建模中区分二者，轨迹估计与风险关联都可能被混淆，而现有证据多为观察性关联，因果机制尚未明确。

### 2.5 隐私保护合成基因组与生物样本库规模生成

HELICS 是面向生物样本库规模基因型数据的**无定相潜空间流匹配**框架，目标是在数十万至数千万相关 SNP 的超高维离散分布上做条件合成基因组生成，以支持隐私保护的基准测试、模拟和数据增强，尤其针对代表性不足人群、罕见或失衡疾病队列及受限生物样本库等数据有限场景 [12]。方法上，它通过染色体特异编码与多染色体潜空间流实现全基因组 SNP 级生成，并支持性状条件合成；在 **chr15 18,784 SNP** 及全基因组 **600,336 SNP** 的基准上，HELICS 在 MAF、LD 和隐私代理指标上优于 HAPNEST 等基线，并能对多基因性状的遗传易感性进行条件控制 [12]。

与 HAPNEST、Sim1000G、HAPGEN2、GAN、RBM、HCLT 等基线相比，HELICS 的差异在于以潜空间流匹配做条件合成而非直接建模高维离散分布 [12]。其局限也被作者指出：低 MAF 变异 R² 偏低，且生成样本的 NN IBS 相似度较高，提示多样性有限 [12]。这两点意味着在罕见变异与样本多样性方面，合成数据与真实生物样本库数据之间仍存在差距，也是该类方法在隐私保护场景落地时需要权衡的问题 [12]。

## 3 数据与资源

人群队列资源构成了多组学 AI 研究的基础设施，其规模与表型深度在过去十余年快速扩展。**UK Biobank** 纳入约 **50 万** 40–69 岁参与者，2006–2010 年完成基线评估，收集问卷、体格测量、生物样本、影像、加速度计及健康记录链接数据，预计 20 年随访可累积糖尿病约 68,000 例、心梗与冠心病死亡 47,000 例、卒中 20,000 例、阿尔茨海默病 30,000 例 [13]。该队列的深度表型与基因组资源包括约 50 万人的基因型质控、单倍型估计和约 **9600 万变异插补**，并通过身高 GWAS 和 HLA-疾病关联复制验证数据质量 [14]。2025 年进一步完成 **490,640 人** 全基因组测序，平均覆盖 **32.5×**，识别约 15 亿变异，较芯片插补增 18.8 倍、较全外显子测序增 >40 倍，其中 93.5% 为非芬兰欧洲 ancestry [15]。该队列已超 8000 机构使用、8000 余篇论文，但参与者以 40–69 岁为主、存在健康志愿者偏倚，部分神经疾病病例仍有限 [93]。

与 UK Biobank 以深度表型见长不同，**All of Us** 研究计划以多样性为核心目标，计划在美国招募至少 **100 万** 人；截至 2019 年 7 月，超过 175,000 人贡献生物样本，其中 **>80%** 来自历史上生物医学研究不足群体，34 个站点收集了 >112,000 人的 EHR 数据 [16]。该计划后续系统比较了患者介导 EHR（PME）与提供者来源 EHR（HPO）两种数据路径：在 393,590 名参与者中，PME 为 19,703 人、HPO 为 373,887 人，PME 人群更白、更女性、更多保险、随访更长，而 WGS 覆盖更少（**35.2% vs 83.2%**），两种来源在疾病患病率、10 个表型 PheWAS 及 5,000 多个已知基因型-表型关联复制率上存在差异 [25]。这一比较提示，EHR 数据来源本身会塑造可复现性，PME 样本量小且人群构成差异大，可能影响泛化 [25]。

隔离人群队列提供了另一条发现路径。**FinnGen** 整合 9 个芬兰生物库与全国健康登记数据，基于 **224,737 人** 插补基因型和 **1,932 个终点** 进行 GWAS 与统计精细定位，发现芬兰隔离人群富集低频有害等位（0.1% ≤ MAF < 5%），可在既往研究充分的疾病中识别新的低频变异关联和可能因果编码变异 [17]。其局限在于芬兰隔离人群遗传结构特殊，结果外推至其他人群受限 [17]。国家生物样本库 WGS 综述进一步比较了 UK Biobank、All of Us、新加坡 PRECISE、Biobank Japan 和韩国 NPBBD-Korea 等项目，指出 WGS 可发现罕见变异、结构变异和调控元件，但计算基础设施、隐私伦理、临床整合和祖先多样性不足仍是共同挑战 [94]。队列发展趋势综述则概括，组学技术、EHR 普及与 AI 正推动队列从描述性关联转向机制发现、精细风险分层与遗传导向的治疗开发，并日益全球化与多样化 [31]。

在数据复用层面，**NHGRI-EBI GWAS Catalog** 截至 2024 年 7 月收录 **625,113** 条 SNP-性状关联、6,921 篇论文、>15.5K 性状和 >85K 全基因组汇总统计数据集，通过 EFO 性状映射、祖源框架和与 PGS Catalog 互链提升可复用性；但汇总统计标准化不足、非欧祖源仍偏少、依赖作者提交 [95]。**UK Biobank PRS Release** 则发布 28 种疾病和 25 种数量性状的多基因风险评分及基准测试软件，广泛基准测试显示其优于 **81 个** 已发表 PRS，并在其他队列验证，但主要基于 UK Biobank 人群，跨种族适用性有限 [96]。这两类资源分别代表"汇总统计复用"与"个体级评分发布"两种共享模式，前者覆盖面广但标准化受制于提交质量，后者性能可比但人群外推受限。

表型定义与数据清洗工具是连接原始记录与可分析表型的关键环节。**Phecodes** 基于 ICD 编码快速定义数千种临床有意义疾病的病例/对照状态，最初用于 PheWAS，后扩展至表型风险评分，但依赖 ICD 编码，可能存在编码误差和表型异质性 [23]。跨版本编码统一方面，一项研究构建了 ICD-8 到 ICD-10 的单向映射，覆盖完整 ICD 及丹麦本地扩展，可连接丹麦自 1965 年以来超半世纪医疗数据，但未提供 ICD-10 回映射 ICD-8 [24]。针对 UK Biobank 异质表型，**PHESANT** 用规则算法自动选择统计检验，对指定性状与全部或子集变量做关联并生成图表，以 R 实现并在 GitHub 公开，但自动化模型可能不适用于所有复杂表型 [97]。代谢组数据方面，针对约 **121,657** 人、168 标志物加 81 比值的 NMR 数据，质控流程识别运输批次、板、孔位、光谱仪等协变量，多数标志物技术因素中位解释 **1.5%**，3,169 个盲重复中位 CV **4.55%**、R² **0.928**，并发布 ukbnmr R 包；局限是仅覆盖约三分之一 UKB 参与者、基于已校准浓度而非原始谱 [98]。

可视化与真实世界诊疗模式图谱代表了结果呈现与临床事件压缩的两个方向。**PheWeb** 开源网页工具整合 Manhattan、LocusZoom 和 PheWAS 视图，支持单性状与多性状切换，已用于 UKB 等数据集，但仅做可视化与共享、不含统计建模 [99]。爱沙尼亚 **EST-Health-30** 基于 30% 随机人群样本，将异质临床事件压缩为以 ICD-10 三位字符诊断为中心的标准化摘要，汇总索引前 90 天、索引后 30 天等窗口事件，形成覆盖 **1000 多个** 诊断类别的全国尺度数字图谱；作为回顾性观察研究，其局限在于仅基于单一国家样本 [100]。两者差异在于，前者面向遗传关联结果的浏览与假设生成，后者面向诊疗路径的模式归纳，尚未见证据将二者直接整合。

## 4 应用与结果

在冠心病风险预测方向，多组学整合的证据较为集中。一项研究在UK Biobank中整合传统风险因素、多基因风险评分与大规模血浆蛋白组学，采用LASSO Cox构建**202蛋白风险评分**并用CatBoost建模，内部验证AUC从**0.750升至0.789**，外部验证从**0.717升至0.762**，且**9蛋白面板**即可捕获大部分预测信息[101]。另一项在UK Biobank 53,026人中基于Olink蛋白组训练15种疾病预测模型的工作则显示，蛋白组模型平均AUC为**0.74**（范围0.56-0.89），较仅用临床因素平均仅提升**ΔAUC=0.03**，且不依赖模型架构，简单模型如L2表现相当，并提示跨队列泛化性受表型定义影响[102]。两者增益幅度的差异可能来自疾病谱、终点定义与对照模型的不同，不宜直接比较高低。

在风险随生命历程变化这一子问题上，证据指向遗传与非遗传风险的时变特征。基于FOS 3,588人与UK Biobank 327,837人的纵向分析发现，冠心病PRS的风险比从19岁的**3.58**降至70岁的**1.51**，且在40-45岁组PRS显著优于PCE[103]。MSGene则以年龄为时间尺度的多状态模型整合遗传风险与EHR，跨10个心脏代谢状态估计年龄特异转移，相比Framingham 30年与PCE 10年模型可提供动态终身风险并用于指导他汀治疗启动[104]。BMI多基因评分方面，多祖源评分在UK Biobank欧洲裔中解释**17.6%**的BMI变异，其他人群从东亚裔美国人16%到农村乌干达**2.2%**不等；8岁时加入PGS使解释方差从11%升至21%，5岁时预测18岁BMI从22%升至35%[105]，显示非欧洲裔人群效能明显偏低。

跨祖源关联发现方面，Pan-UK Biobank对7,266个性状开展混合模型GWAS与跨祖源荟萃分析，发现**14,676个**仅欧洲祖源分析未发现的显著位点，并公开汇总统计，但多数关联仍主要见于欧洲祖源[106]。药效遗传学上，一项研究利用UKB与All of Us的EHR纵向用药与生物标志物数据，对10个药物-表型对（他汀LDL-C、二甲双胍HbA1c、降压药SBP等）做GWAS与罕见变异负荷检验，并证明疾病PRS可预测药效，同时指出用药与检测时点不齐、依从性与适应证混杂等纵向表型分析陷阱[107]。

多病共存与多组学机制是另一条主线。EPIC-Norfolk中>11,000人、>1,000代谢物的分析识别出**640个**显著代谢物-疾病关联，其中**420个（65.5%）**跨至少2种非传染性疾病共享，涉及肝肾功能、脂糖代谢、低度炎症与肠道微生物等通路[108]。UKB-MDRMF整合六类多模态数据联合建模**1560种疾病**，联合预测优于单类别评估[109]；PheMIME则整合三大EHR系统汇总统计实现跨机构共病网络交互可视化[110]。心肾代谢方向上，330,177名UKB参与者的多状态模型结合**2,911个**血浆蛋白识别中介蛋白[111]；另有研究在269,530名横断面与240,576名随访参与者中报告MVX每1-SD **HR=1.213**、MetaboHealth **HR=1.503**，随访8,876人发病[112]；美国整合医疗系统54,933人中加入250个NMR代谢标志物后几乎所有9个终点判别能力提升，2型糖尿病、慢性肾病与代谢功能障碍相关脂肪性肝病增益最大[113]。

特定疾病的分子分层与早期识别也有多项结果。HFpEF研究用UKB多组学（蛋白/代谢/影像/EHR，HFpEF 33,480例）训练监督分类器并在独立多中心队列验证，结合无监督聚类划分多组学亚型与可解释AI揭示分子异质性[114]。高血压人群心衰预测中，16,128名参与者检测2,911种Olink蛋白，随访**15.1年**1074人（**6.66%**）发生心衰，NT-proBNP关联最强（**HR=1.68**）[115]。骨质疏松方面，XGBoost+SHAP筛选的少数蛋白标志物（FSHB、ADIPOQ、SOST、COL9A1、CHAD）模型优于全蛋白组模型[116]。痴呆预测按性别与APOE ε4分层，交互**p=0.027**，携带者模型AUC **0.85-0.90**且女性携带者最佳，关键预测因子呈亚组特异[117]。胰腺癌方向，基于丹麦DNPR与美国VA EHR疾病轨迹的深度学习模型可提前**3年**预测风险并输出分时间间隔风险，但属回顾性验证，筛查成本与假阳性需权衡[118]。

总体看，证据在“多组学能否实质提升预测”上并不一致：蛋白组在部分疾病中带来可观增益[101]，在跨15种疾病的系统评估中平均增益有限且受表型定义制约[102]；祖源与性别分层普遍显示非欧洲裔及部分亚组效能下降[105][106]。多数研究为观察性设计，残余混杂、单时点测量与外部验证不足是共同局限[112][115]。

## 5 评测、可复现性与争议

在生存分析的大规模推断上，方法层面的可复现性挑战主要来自数据规模与近似策略。针对百万级数据点、数千时变协变量的大规模电子健康记录场景，**贝叶斯Cox回归结合随机变分推断**被提出以替代传统Cox模型实现，其基于计数过程表示的Cox偏似然，配合随机变分推断与似然重加权，使后验分布可因子化到子样本，从而支持大数据分析[119]。该工作在模拟与 **UK Biobank 心肌梗死**应用中报告可处理百万级数据并给出可行不确定性估计[119]；但其局限也明确落在评测可信度上——**依赖变分近似，精度受子采样影响**[119]。这意味着此类方法的复现与比较不能只看能否跑通大规模数据，还需交代子采样设置对精度的影响。

相比之下，面向电子健康记录共病研究的AI方法综述目前只能提供选题层面的线索。该文以「从数据到知识」的角度梳理电子健康记录中共病研究的AI方法[120]，但证据中缺少摘要与具体方法细节，无法据此评估其评测基准、复现条件或争议点[120]。因此两篇证据之间不构成方法优劣的直接对照：前者给出了可核查的规模与不确定性估计陈述，后者尚无可展开的实质评测信息。

## 6 空白与趋势

现有证据在“空白与趋势”上呈现出几个可辨识的方向，以下逐条给出判断与依据。

1. **生成式EHR模型正从“预测下一事件”走向“推理时控制与反事实模拟”，但真实临床验证仍是空白。** Foresight 已支持患者旅程模拟与因果推断，作者同时声明其当前形式不宜直接用于临床决策支持 [1]；EHR-MPC 把脓毒症治疗重构为推理时控制问题，在 8 家医院 ICU 队列上离线策略与强化学习相当、模拟更优，但仿真与真实临床之间仍有差距 [5]；NOAH 亦以反事实干预模拟为卖点 [3]。**目前尚无一项生成式轨迹模型报告前瞻性、干预性临床终点**，这是该方向最明确的方法学缺口。

2. **跨队列可复现性正从“同一模型换数据”升级为“跨编码系统语义对齐”，但覆盖人群仍高度集中。** GRASP 在 UKB、FinnGen、Mount Sinai 三队列验证，平均 ΔC-index 在芬兰高 88%、美国高 47% [26]；ALADYNOULLI 在 3 个生物库 n>683,000 上识别 21 个可复制特征、跨队列组成保留中位 80% [4]；ATM 在 UK Biobank 与 All of Us 间验证共病亚型 [121]。但上述队列均以欧美人群为主，**非欧祖源、非英语医疗系统下的EHR基础模型外部验证几乎空白**，而 All of Us 自身已显示 PME 与 HPO 两种数据路径在患病率与关联复制率上存在差异 [25]，提示“数据来源”本身就是未被系统建模的异质性来源。

3. **多组学与遗传的整合正从“关联并列”走向“跨分子层因果链与靶点”，但功能验证与个体层面可迁移性缺位。** 血浆蛋白组图谱已给出 183 种疾病判别 AUC>0.80、474 个因果蛋白与 37 个药物重定位机会 [27]；T2D PGS 关联 648 个蛋白、617 个复制 [61]；All of Us 的 e/s/pQTL 分析把 59.4% 信号精细定位到单一因果变异并富集于获批药物靶点 [71]。然而 **MR 与共定位结论普遍缺乏功能实验验证**，且 48 个冠心病 PRS 在三个生物库 171,095 人上群体表现相似、个体层面一致性差 [10]，说明“群体可复现”不等于“个体可迁移”，**个体层面的评分一致性与不确定性量化是明显空白**。

4. **组学衰老时钟正从横断面估计转向纵向轨迹，但“变化”的归因尚未分离。** LPAI 同时捕捉累积负担与变化速度 [86]；MetBAG 关联 525 个疾病终点 [87]；14 器官框架显示年龄加速与死亡风险是可分离维度 [88]。但体力活动与 ProtAgeGap 的关联为观察性、干预样本仅 26 名男性 [91]，而采血时相与节律紊乱可独立预测 98 种发病风险 [92]。**行为干预、采样时相与真实生物学衰老三者在轨迹建模中未被区分**，是时钟走向因果解释的关键障碍。

5. **合成基因组数据开始进入生物样本库规模，但罕见变异与多样性仍是硬约束。** HELICS 以无定相潜空间流匹配在 chr15 18,784 SNP 与全基因组 600,336 SNP 上优于 HAPNEST 等基线，并支持性状条件合成 [12]；作者自述低 MAF 变异 R² 偏低、生成样本 NN IBS 相似度较高、多样性有限 [12]。**面向代表性不足人群与罕见病队列的合成数据基准尚不存在**，而这恰是该类方法宣称的主要应用场景。

6. **评测框架正在成形，但基因组基础模型尚未证明超越标准注释。** All of Us v9 的家族感知基准通过整家族分配消除亲属泄漏 [30]；UK Biobank PRS Release 提供 53 性状系统基准并优于 81 个已发表 PRS [96]。但 27 个 UKB 性状上 AlphaGenome 与 Borzoi 的位点发现中位仅 1.8%、3.8%，低于 baselineLD 的 5.1%，GPN-Star 反而减少发现 [11]。**“基础模型优于任务特异基线”这一假设在遗传学侧尚未成立**，提示多组学AI的评测应把强基线（如 baselineLD、PRS-CS [56]）作为默认对照，而非可选项。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 生成式疾病轨迹模型 | **朝阳** | Foresight 用 GPT 式生成模型建模患者时间线 [1]，随后 Nature 上「用生成式 transformer 学习人类疾病自然史」把同一范式推到全人群尺度 [22]；但同期还有纵向生存聚类的深度表征学习 [34] 和贝叶斯纵向 EHR+遗传框架 [4]，说明**建模范式尚未收敛**（生成式 vs 表征学习 vs 贝叶斯推断并存），雷达样本中该节 12 篇里 90% 为 2024–2026，属近两年爆发。 |
| 2.2 多组学与遗传整合 | **成熟** | UK Biobank 血浆蛋白组-遗传-健康关联图谱 [9]（被引 1547）与 45 万人外显子测序分析 [8] 已把「大队列 + 组学 + 遗传」的基础设施和方法栈做透；BOLT-LMM 类混合模型 [19] 与 35 项血尿标志物遗传学 [62] 表明关联发现已进入**增量为主**阶段，新意更多转向下游整合与预测而非方法本身。 |
| 2.3 医学 / EHR 基础模型 | **成熟（方法层）/ 证据偏薄** | Med-BERT [21] 与 BEHRT [20] 确立了结构化 EHR 预训练范式并被广泛复用；近两年工作转向 LLM 智能体做表格推理 [84] 和提升跨机构可迁移性 [26]，属**范式内改良**。但雷达样本该节仅 5 篇、CNS 占比 0，判断置信度有限。 |
| 2.4 组学衰老时钟与纵向多组学动态 | **朝阳（偏萌芽）** | 多器官代谢组生物学年龄关联心血管代谢病 [87] 与常规临床标志物生理衰老的前瞻性估计 [89] 显示「时钟 → 结局验证」正在铺开；纵向蛋白组衰老指数预测死亡与多病 [86]、运动逆转蛋白组衰老 [91] 说明**纵向动态与可干预性**是新增量，但样本量小、被引低（中位 1），方法未定型。 |
| 2.5 隐私保护合成基因组与生物样本库规模生成 | **证据不足** | 雷达样本仅 1 篇（HELICS 生物样本库规模条件合成基因组 [12]），无法判断阶段。 |
| 3 数据与资源 | **成熟** | UK Biobank 资源描述 [13] 与深度表型+基因组数据说明 [14] 是长期被引的基础设施；FinnGen [17] 与 All of Us [16] 补齐了隔离人群与多样性队列，**数据层已稳定供给**，新工作主要是复用而非新建。 |
| 4 应用与结果 | **朝阳** | 从疾病轨迹深度学习预测胰腺癌风险 [118] 到血浆代谢组刻画非传染性多病通路 [108]，再到 Pan-UKB 跨人群 GWAS [106] 与全生命周期 BMI 多基因预测 [105]，应用端正**快速扩张且开始强调跨人群泛化**，但落地口径尚未统一。 |
| 5 评测、可复现性与争议 | **证据不足（且是明显空白）** | 雷达样本仅 2 篇：大规模 EHR 贝叶斯 Cox 推断 [119] 与共病 AI 方法综述 [120]，**没有专门的基准/评测框架证据**，无法判定阶段，但这本身说明该环节供给稀缺。 |

**整体判断**：这个方向整体处于**朝阳期偏后段**——数据基础设施（UKB/FinnGen/All of Us）已成熟 [13][17]，关联发现层（蛋白组/pQTL/GWAS）已进入增量阶段 [9][106]，而**生成式轨迹建模与纵向多组学动态**是近两年真正在爆发的两层 [22][87]。窗口期估计 **18–30 个月**：一旦生成式轨迹范式收敛出公认基线（类似 BEHRT 之于 EHR），纯应用型工作会迅速贬值。最大不确定性有三：**（1）评测与可复现性几乎空白**（雷达样本第 5 节仅 2 篇，无基准框架），意味着现在的方法优劣缺乏公认裁判；**（2）跨队列泛化未验证**，多数结果仍在 UKB 单队列内；**（3）隐私/数据访问约束**可能限制生物样本库规模生成这条线 [12]。

**接下来怎么做**

1. **把「纵向多组学衰老时钟 + 生成式轨迹」缝起来，做跨队列可复现性研究**。切入点：UKB 重复测量蛋白组/代谢组 + FinnGen 或 All of Us 做外部验证，用生成式 transformer 建模个体组学轨迹而非单时点时钟，产出「组学衰老速率 → 多病发生顺序」的预测模型与复现性报告。为什么现在做：时钟侧已有纵向蛋白组指数预测死亡/多病 [86] 和运动逆转证据 [91]，轨迹侧生成式范式刚起 [22]，两者尚未合并，且**跨队列复现正是空白**。这直接对接他的衰老 + 多模态建模背景。

2. **用类器官/多组学合作项目做「机制锚点」验证，避免纯关联**。切入点：把人群队列里发现的蛋白组/代谢组衰老特征，在类器官多组学（转录+蛋白/代谢）中做扰动验证，产出「人群信号 → 体外可干预」的闭环论文。为什么现在做：人群端 pQTL/蛋白组关联已成熟到可作为假设来源 [9]，而代谢组-多病通路已有可复用框架 [108]，缺的正是机制层；这是他合作项目的**独特差异化**。

3. **抢占评测/基准这块空地，做一个小而硬的公开 benchmark**。切入点：用公开 UKB/All of Us 派生数据 + 统一划分，评测「EHR 轨迹模型 vs 组学时钟」在下游多病预测上的表现与校准，产出数据集划分、指标协议与开源代码。为什么现在做：雷达样本第 5 节仅 2 篇且无基准框架 [119][120]，而方法层已多范式并存 [34][4]，**谁先给出裁判标准谁定义赛道**；也最契合他「公共数据 demo」的诉求。

4. **在生成式轨迹模型上做「组学条件化」的窄切口，而不是再训一个通用 EHR 基础模型**。切入点：以 Foresight/疾病自然史 transformer 为骨架 [1][22]，把血浆蛋白组/代谢组作为条件 token 注入，预测共病序列，产出「组学增强的轨迹生成」方法论文。为什么现在做：通用 EHR 基础模型已成熟且拥挤 [21][20]，单纯复刻无新意；**组学条件化是尚未被占的位置**，且能复用他的多模态建模能力。

5. **把多基因风险作为先验并入纵向模型，做「遗传 + 组学 + 轨迹」三层整合**。切入点：用 Pan-UKB 跨人群 GWAS 与全生命周期多基因预测 [106][105] 作为静态先验，与贝叶斯纵向 EHR+遗传框架 [4] 结合，产出带不确定性量化的个体风险轨迹。为什么现在做：贝叶斯框架刚出现、尚未与生成式方法对比 [34]，**不确定性量化 + 跨人群泛化**是审稿人现在最认的增量点。

## 参考文献

1. Foresight—a generative pretrained transformer for modelling of patient timelines using electronic health records: a retrospective modelling study. The Lancet Digital Health 2024. https://doi.org/10.1016/s2589-7500(24)00025-6
2. Foresight-England: Development of a National-Scale Generative AI Model of Electronic Health Records for Medical Event Prediction across the COVID-19 Pandemic.  2026. https://arxiv.org/abs/2608.16273
3. NOAH: Learning the Full Patient Journey. A Longitudinal Multimodal Time-Aware Model for Representation and Forecasting.  2026. https://arxiv.org/abs/2609.09140
4. A Bayesian framework for longitudinal EHR and genetic discovery. Nature 2026. https://doi.org/10.1038/s41586-026-10780-5
5. EHR-MPC: Inference-Time Control for Sepsis Treatment with Generative Patient Digital Twins. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.08793
6. LifeLong Digital Twin: A Unified Modeling Paradigm and Agent Harness for Event-Driven Lifelong Health State Trajectories.  . https://arxiv.org/abs/2610.05566
7. Predicting Early Functional Decline from Longitudinal Laboratory and Vital Sign Trajectories: A Large-Scale Study Using the All of Us Research Program.  2026. https://arxiv.org/abs/2608.21589
8. Exome sequencing and analysis of 454,787 UK Biobank participants. Nature 2021. https://doi.org/10.1038/s41586-021-04103-z
9. Plasma proteomic associations with genetics and health in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06592-6
10. Evaluating Performance and Agreement of Coronary Heart Disease Polygenic Risk Scores.. JAMA 2025. https://doi.org/10.1001/jama.2024.23784
11. Genomic foundation models do not yet boost common variant discovery beyond standard functional annotations.  . https://doi.org/10.64898/2026.10.13.758880
12. HELICS: Biobank-scale Conditional Synthetic Genome Generation via Latent Flow Matching.  . https://arxiv.org/abs/2610.36361
13. UK Biobank: An Open Access Resource for Identifying the Causes of a Wide Range of Complex Diseases of Middle and Old Age. PLoS Medicine 2015. https://doi.org/10.1371/journal.pmed.1001779
14. The UK Biobank resource with deep phenotyping and genomic data. Nature 2018. https://doi.org/10.1038/s41586-018-0579-z
15. Whole-genome sequencing of 490,640 UK Biobank participants.. Nature 2025. https://doi.org/10.1038/s41586-025-09272-9
16. The “All of Us” Research Program. New England Journal of Medicine 2019. https://doi.org/10.1056/NEJMsr1809937
17. FinnGen provides genetic insights from a well-phenotyped isolated population. Nature 2023. https://doi.org/10.1038/s41586-022-05473-8
18. An atlas of genetic associations in UK Biobank. Nature Genetics 2017. https://doi.org/10.1038/s41588-018-0248-z
19. Mixed model association for biobank-scale data sets. Nature Genetics 2018. https://doi.org/10.1038/s41588-018-0144-6
20. BEHRT: Transformer for Electronic Health Records. Scientific Reports 2019. https://doi.org/10.1038/s41598-020-62922-y
21. Med-BERT: pretrained contextualized embeddings on large-scale structured electronic health records for disease prediction. npj Digital Medicine 2020. https://doi.org/10.1038/s41746-021-00455-y
22. Learning the natural history of human disease with generative transformers.. Nature 2025. https://doi.org/10.1038/s41586-025-09529-3
23. Using Phecodes for Research with the Electronic Health Record: From PheWAS to PheRS. Annual Review of Biomedical Data Science 2021. https://doi.org/10.1146/annurev-biodatasci-122320-112352
24. A unidirectional mapping of ICD-8 to ICD-10 codes, for harmonized longitudinal analysis of diseases. European Journal of Epidemiology 2023. https://doi.org/10.1007/s10654-023-01027-y
25. Robust replication of associations across patient-mediated and provider-sourced EHR data in the All of Us research program. npj Digital Public Health 2026. https://doi.org/10.1038/s44482-026-00032-8
26. Large language models improve transferability of electronic health record-based predictions across countries and coding systems.. NPJ digital medicine 2026. https://doi.org/10.1038/s41746-026-02363-5
27. Atlas of the plasma proteome in health and disease in 53,026 adults.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.045
28. Plasma proteome analyses in individuals of European and African ancestry identify cis-pQTLs and models for proteome-wide association studies. Nature Genetics 2022. https://doi.org/10.1038/s41588-022-01051-w
29. Multi-ancestry MHC-pQTL mapping reveals disease-linked HLA protein networks and shared genetic architecture.  . https://doi.org/10.21203/rs.3.rs-10956233/v1
30. A family-aware All of Us benchmark for polygenic prediction and genomic machine learning.  . https://doi.org/10.64898/2026.10.22.26366229
31. Trends in large-scale human population cohorts.. Trends in Genetics 2026. https://doi.org/10.1016/j.tig.2026.08.002
32. Identifying cohorts at elevated risk of cancers using generative modeling of patient health states.  . https://doi.org/10.21203/rs.3.rs-11733688/v1
33. Subtyping Alzheimer's disease and Parkinson's disease using longitudinal electronic health records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01085-3
34. Deep representation learning for clustering longitudinal survival data from electronic health records.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56625-z
35. MiGHT-EHR: A Multi-task Graph Transformer for Heterogeneous Temporal Electronic Health Records.  2026. https://arxiv.org/abs/2608.06430
36. Pan-UK Biobank GWAS improves discovery, analysis of genetic architecture, and resolution into ancestry-enriched effects. medRxiv 2024. https://doi.org/10.1101/2024.03.13.24303864
37. Rare variant contribution to human disease in 281,104 UK Biobank exomes. Nature 2021. https://doi.org/10.1038/s41586-021-03855-y
38. Systematic single-variant and gene-based association testing of thousands of phenotypes in 394,841 UK Biobank exomes. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100168
39. Exome sequencing and characterization of 49,960 individuals in the UK Biobank. Nature 2020. https://doi.org/10.1038/s41586-020-2853-0
40. Advancing human genetics research and drug discovery through exome sequencing of the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-021-00885-0
41. Mono- and biallelic variant effects on disease at biobank scale. Nature 2023. https://doi.org/10.1038/s41586-022-05420-7
42. Phenome-wide Burden of Copy Number Variation in the UK Biobank.. American Journal of Human Genetics 2019. https://doi.org/10.1016/j.ajhg.2019.07.001
43. Deviations from genetic additivity driven by rare variants at biobank scale.. Nature communications . https://doi.org/10.1038/s41467-026-76151-w
44. Choice of phenotype scale is critical in biobank-based G × E tests.. Cell genomics . https://doi.org/10.1016/j.xgen.2026.101391
45. Optimizing phenotype scale improves genetic analyses in large-scale biobanks.. Nature genetics . https://doi.org/10.1038/s41588-026-02826-1
46. Rare variant associations with plasma protein levels in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06547-x
47. Genetic associations with ratios between protein levels detect new pQTLs and reveal protein-protein interactions. bioRxiv 2023. https://doi.org/10.1016/j.xgen.2024.100506
48. Robust cis-by-trans epistasis in the human plasma proteome highlights an ABO-centered interaction network.. American journal of human genetics . https://doi.org/10.1016/j.ajhg.2026.09.003
49. Sex differences in the genetic regulation of the human plasma proteome.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59034-4
50. A proteome atlas of structural variation and VNTR effects on complex traits and diseases.  . https://doi.org/10.64898/2026.09.26.26364064
51. Metabolomic and genomic prediction of common diseases in 700,217 participants in three national biobanks.. Nature communications 2024. https://doi.org/10.1038/s41467-024-54357-0
52. Atlas of plasma NMR biomarkers for health and disease in 118,461 individuals from the UK Biobank. Nature Communications 2023. https://doi.org/10.1038/s41467-023-36231-7
53. Machine learning-based proteomics analysis identified 23 protein biomarkers for enhanced risk prediction of myocardial infarction in Chinese and Europeans.. GigaScience . https://doi.org/10.1093/gigascience/giag102
54. Prospective multi-omic profiling identifies predictive and genetically supported molecular determinants of incident epilepsy.  . https://doi.org/10.64898/2026.11.18.26364966
55. Integrated multiomic scores for cardiovascular disease prediction across multiancestral populations.  . https://doi.org/10.64898/2026.10.23.26366372
56. Global biobank analyses provide lessons for computing polygenic risk scores across diverse cohorts. medRxiv 2021. https://doi.org/10.1101/2021.11.18.21266545
57. All of Us diversity and scale yield context-dependent improvements in polygenic prediction.. Nature Genetics 2026. https://doi.org/10.1038/s41588-026-02734-4
58. Population-specific polygenic risk scores for people of Han Chinese ancestry.. Nature 2025. https://doi.org/10.1038/s41586-025-09350-y
59. Regularized ensemble polygenic risk prediction with GWAS summary statistics.. Nature genetics . https://doi.org/10.1038/s41588-026-02844-z
60. A pre-train and fine-tune framework for adaptive boosting of pre-trained polygenic risk scores.. Nature communications . https://doi.org/10.1038/s41467-026-77128-5
61. Identification of plasma proteomic markers underlying polygenic risk of type 2 diabetes and related comorbidities.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56695-z
62. Genetics of 35 blood and urine biomarkers in the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-020-00757-z
63. An atlas of polygenic risk score associations to highlight putative causal relationships across the human phenome. bioRxiv 2018. https://doi.org/10.7554/eLife.43657
64. Phenome-wide association studies across large population cohorts support drug target validation. Nature Communications 2018. https://doi.org/10.1038/s41467-018-06540-3
65. Decomposing polygenic risk of coronary artery disease into distinct biological processes.  . https://doi.org/10.64898/2026.10.08.26365088
66. Multimodal mediators connecting APOE4 to dementia.  . https://doi.org/10.21203/rs.3.rs-11445203/v1
67. Phenome-wide and proteomic analysis of APOE alleles across different ancestries in the All of Us Research Program.  . https://doi.org/10.64898/2026.09.26.26364080
68. Genetically supported targets and drug repurposing for brain aging: A systematic study in the UK Biobank.. Science advances 2025. https://doi.org/10.1126/sciadv.adr3757
69. Integrating the environmental and genetic architectures of aging and mortality.. Nature medicine 2025. https://doi.org/10.1038/s41591-024-03483-9
70. Proteomic Signatures Capture Environmental Exposures Across Diverse Populations.  . https://doi.org/10.64898/2026.10.06.26364311
71. Multi-omics in the All Of Us Research Program expands mapping genetic mechanisms in health and disease.  . https://doi.org/10.64898/2026.10.29.26366507
72. Longitudinal alignments and syntheses of multimodal clinical data for personalized medicine with the PULSE framework. Nature Computational Science 2026. https://doi.org/10.1038/s43588-026-01026-5
73. Functional architecture of rare protein coding variation across 786,871 exomes.  . https://doi.org/10.64898/2026.10.16.26365771
74. GWAS of extended prescription analgesic use identifies genetic loci in chronic pain.. Nature communications 2026. https://doi.org/10.1038/s41467-026-71434-8
75. SPA<sub>GRM</sub>: effectively controlling for sample relatedness in large-scale genome-wide association studies of longitudinal traits.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56669-1
76. Genome-wide detection of genotype-environment interactions at biobank scale with fastGxE.. Nature genetics . https://doi.org/10.1038/s41588-026-02809-2
77. fastGxE is a powerful method for uncovering genotype-environment interactions in biobanks.. Nature genetics . https://doi.org/10.1038/s41588-026-02806-5
78. A fast and scalable framework for large-scale and ultrahigh-dimensional sparse regression with application to the UK Biobank. bioRxiv 2019. https://doi.org/10.1371/journal.pgen.1009141
79. Biobank-scale self-supervised genotype pretraining yields transferable representations for human genetics.. Nucleic acids research . https://doi.org/10.1093/nar/gkag1059
80. Global Biobank Meta-analysis Initiative: Powering genetic discovery across human disease. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100192
81. Comparative analysis of the Mexico City Prospective Study and the UK Biobank identifies ancestry-specific effects on clonal hematopoiesis.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02085-6
82. Polygenic Prediction of Peripheral Artery Disease and Major Adverse Limb Events.. JAMA cardiology 2025. https://doi.org/10.1001/jamacardio.2025.1182
83. SurvivEHR: a competing risks, time-to-event foundation model for multiple long-term conditions from primary care electronic health records.  2025. https://doi.org/10.1101/2025.08.04.25332916
84. EHRAgent: Code Empowers Large Language Models for Few-shot Complex Tabular Reasoning on Electronic Health Records.. Proceedings of the Conference on Empirical Methods in Natural Language Processing. Conference on Empirical Methods in Natural Language Processing 2024. https://doi.org/10.18653/v1/2024.emnlp-main.1245
85. Longitudinal dynamics of gene expression and metabolomics in an aging population cohort.. Science 2026. https://doi.org/10.1126/science.aed6452
86. A Novel Longitudinal Proteomic Aging Index Predicts Mortality, Multimorbidity, and Frailty in Older Adults.. Aging cell 2025. https://doi.org/10.1111/acel.70317
87. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
88. Age Acceleration and Mortality Risk Constitute Distinct Dimensions of Organ Aging.  . https://doi.org/10.21203/rs.3.rs-10881849/v1
89. Estimation of physiological aging based on routine clinical biomarkers: a prospective cohort study in elderly Chinese and the UK Biobank.. BMC medicine 2024. https://doi.org/10.1186/s12916-024-03769-2
90. ClinicalAge, a framework for modelling ageing trajectories from longitudinal electronic health records in the UK: a model development and validation study.. The Lancet. Digital health . https://doi.org/10.1016/j.landig.2026.101060
91. Reversal of proteomic aging with exercise-results from the UK biobank and a 12-week intervention study.. npj aging 2025. https://doi.org/10.1038/s41514-025-00318-w
92. Molecular Circadian Disturbance in Human Blood Independently Predicts Multi-Disease Risk and Maps to Hepatic metabolism Pathways.  . https://doi.org/10.21203/rs.3.rs-11120748/v1
93. UK Biobank-A Unique Resource for Discovery and Translation Research on Genetics and Neurologic Disease.. Neurology. Genetics 2025. https://doi.org/10.1212/nxg.0000000000200226
94. Lessons from national biobank projects utilizing whole-genome sequencing for population-scale genomics.. Genomics & informatics 2025. https://doi.org/10.1186/s44342-025-00040-9
95. The NHGRI-EBI GWAS Catalog: standards for reusability, sustainability and diversity.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1070
96. UK Biobank release and systematic evaluation of optimised polygenic risk scores for 53 diseases and quantitative traits. medRxiv 2022. https://doi.org/10.1101/2022.06.16.22276246
97. Software Application Profile: PHESANT: a tool for performing automated phenome scans in UK Biobank. International Journal of Epidemiology 2017. https://doi.org/10.1093/ije/dyx204
98. Quality control and removal of technical variation of NMR metabolic biomarker data in ~120,000 UK Biobank participants. Scientific Data 2021. https://doi.org/10.1038/s41597-023-01949-y
99. Exploring and visualizing large-scale genetic associations using PheWeb. Nature Genetics 2020. https://doi.org/10.1038/s41588-020-0622-5
100. A national-scale digital atlas of recorded care patterns across more than 1000 diagnostic categories using real-world health data: a retrospective observational study.  . https://doi.org/10.64898/2026.09.16.26363186
101. Machine Learning‐Driven Prediction of Coronary Artery Disease Risk Based on UK Biobank Plasma Proteomics. Journal of the American Heart Association : Cardiovascular and Cerebrovascular Disease 2026. https://doi.org/10.1161/JAHA.125.047248
102. Generalizability of proteomic risk prediction across biobanks reveals dependence on phenotype definitions.  . https://doi.org/10.64898/2026.10.01.26364038
103. Dynamic Importance of Genomic and Clinical Risk for Coronary Artery Disease Over the Life Course. medRxiv 2023. https://doi.org/10.1101/2023.11.03.23298055
104. MSGene: a multistate model using genetic risk and the electronic health record applied to lifetime risk of coronary artery disease. Nature Communications 2024. https://doi.org/10.1038/s41467-024-49296-9
105. Polygenic prediction of body mass index and obesity through the life course and across ancestries.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03827-z
106. Pan-UK Biobank genome-wide association analyses enhance discovery and resolution of ancestry-enriched effects.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02335-7
107. Leveraging large-scale biobank EHRs to enhance pharmacogenetics of cardiometabolic disease medications.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58152-3
108. Plasma metabolites to profile pathways in noncommunicable disease multimorbidity. Nature Medicine 2021. https://doi.org/10.1038/s41591-021-01266-0
109. UKB-MDRMF: a multi-disease risk and multimorbidity framework based on UK biobank data.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58724-3
110. PheMIME: an interactive web app and knowledge base for phenome-wide, multi-institutional multimorbidity analysis.. Journal of the American Medical Informatics Association : JAMIA 2024. https://doi.org/10.1093/jamia/ocae182
111. Proteomics mediates the effects of biological aging on the progression of cardio-renal-metabolic comorbidity: a UK biobank cohort study.. Cardiovascular diabetology 2025. https://doi.org/10.1186/s12933-025-03035-6
112. MetaboHealth and Metabolic Vulnerability Index as Risk Factors for Cardio-Renal-Metabolic Multimorbidity: A Large-Scale Prospective Cohort Study.. Diabetes, obesity and metabolism 2026. https://doi.org/10.1111/dom.71112
113. NMR metabolomics for cardiovascular-kidney-metabolic risk stratification in an integrated healthcare system.  . https://doi.org/10.64898/2026.10.01.26364322
114. Deep phenotyping of heart failure with preserved ejection fraction through multi-omics integration.. European journal of heart failure 2025. https://doi.org/10.1002/ejhf.70041
115. Large-scale plasma proteomic profiling enhances prediction of heart failure among hypertensive individuals: prospective insights from the UK Biobank.. Journal of global health . https://doi.org/10.7189/jogh.16.04313
116. Explainable Plasma Proteomics–Based Machine Learning for Osteoporosis Diagnosis, Prognosis, and Protein Biomarker Discovery in the UK Biobank. The FASEB Journal 2026. https://doi.org/10.1096/fj.202600647R
117. Sex shapes plasma molecular signatures of dementia risk across APOE ε4 strata.  . https://doi.org/10.64898/2026.11.02.26366836
118. A deep learning algorithm to predict risk of pancreatic cancer from disease trajectories. Nature Medicine 2023. https://doi.org/10.1038/s41591-023-02332-5
119. Bayesian Cox regression for large-scale inference with applications to electronic health records. Annals of Applied Statistics 2021. https://doi.org/10.1214/22-aoas1658
120. From data to knowledge: artificial intelligence methods for studying comorbidity in electronic health records. The European Physical Journal Special Topics 2026. https://doi.org/10.1140/epjs/s11734-026-02571-w
121. Age-dependent topic modelling of comorbidities in UK Biobank identifies disease subtypes with differential genetic risk. Nature Genetics 2023. https://doi.org/10.1038/s41588-023-01522-8
122. Disease prediction with multi-omics and biomarkers empowers case–control genetic discoveries in the UK Biobank. Nature Genetics 2024. https://doi.org/10.1038/s41588-024-01898-1
123. Components of genetic associations across 2,138 phenotypes in the UK Biobank highlight adipocyte biology. Nature Communications 2019. https://doi.org/10.1038/s41467-019-11953-9
124. Imputation of fluid intelligence scores reduces ascertainment bias and increases power for analyses of common and rare variants.. Nature genetics . https://doi.org/10.1038/s41588-026-02787-5
125. MetabHub: an integrative platform for plasma nuclear magnetic resonance metabolomics using mediation analysis, disease prediction, and risk stratification.. Nucleic acids research . https://doi.org/10.1093/nar/gkag1066
126. Large-scale cross-species proteomics and machine learning identify biomarkers and peripheral therapeutic targets for delirium.  . https://doi.org/10.21203/rs.3.rs-10672346/v1
