# 人群健康与多组学 AI · 方向背景报告

证据 121 篇 · 覆盖度 0.80 · 第 15 轮 · 更新 2026-11-15 · 数字核验删句 3

## 本次变更

- 新增 [72] Large-scale cross-species proteomics and machine learning identify biomarkers and peripheral therapeutic targets for delirium
- 新增 [86] ClinicalAge, a framework for modelling ageing trajectories from longitudinal electronic health records in the UK: a model development and validation study.

## 摘要（TL;DR）

- Delphi-2M 改造 GPT 架构建模疾病进展与竞争风险，在 UK Biobank 约 40 万参与者上训练、丹麦登记数据中验证，可同时预测 1000 多种疾病的未来发生率并模拟个体终身轨迹 [1]。
- Foresight-England 的 243M 参数自回归解码器在 NHS England 安全数据环境内从头训练、数据约 6100 万人，但数据访问暂停导致定量结果无法导出，说明国家级部署的生成式轨迹模型目前仍缺少可核验的性能证据 [2]。
- ALADYNOULLI 以贝叶斯生成框架联合建模纵向 EHR 诊断、年龄与多基因风险，在三个生物库 68.3 万余人、348 种疾病、52 年随访上识别出 21 个可复制特征，亚型 Cohen's d 达 4.25 [3]。
- LifeLong Digital Twin 在 25 个疾病终点、3 类任务、4 个语言模型上，16 个模型-读出比较全部优于无 Context/Harness 的基线，疾病识别 F1 从 0.422 升至 0.504（Context）与 0.515（Harness），但缺少配对不确定性、疾病支持计数与组件消融，未确立统计显著性 [4]。
- 当前证据不足以判定生成式轨迹模型相对判别式基线在真实临床场景中的净收益，因各研究队列、结局定义与评估协议不同，且 Foresight-England 的定量结果缺失、LifeLong Digital Twin 未做显著性检验 [5]。
- UKB Pharma Proteomics Project 对 54,219 人、2,923 种蛋白开展 pQTL 定位，发现 14,287 个主要遗传关联，其中 81% 为既往未报道，精细映射出 29,420 个独立信号 [6]。
- 48 个冠心病 PRS 在 AOU、PMBB 与 UCLA 共 171,095 人中，群体水平表现相似者在个体层面一致性差（ICC 与 Light κ 低）[7]。
- 基因组基础模型衍生的注释在 27 个 UKB 性状上均未超越 baselineLD，AlphaGenome 与 Borzoi 的中位增益分别为 1.8% 与 3.8%，低于 baselineLD 的 5.1%，GPN-Star 甚至减少位点发现 [8]。
- HELICS 提出无定相的潜空间流匹配框架用于条件合成基因组生成，使用 UKB 无定相基因型覆盖 chr15 的 18,784 SNP 及全基因组 600,336 SNP，局限在于低 MAF 变异 R² 偏低且生成样本的 NN IBS 相似度较高、多样性有限 [9]。
- 现有纵向时钟证据在「纵向时钟是否优于横断面时钟」「年龄加速是否等同于死亡风险」上尚未收敛，且多数模型训练与验证集中于 UK Biobank/ARIC/MESA 等队列，跨人群外推仍是共同局限 [10][11][12]。

## 1 背景与定义

人群健康与多组学 AI 的边界，首先由“队列规模”与“数据层次”共同划定。它区别于单中心小样本关联研究的地方，在于以 UK Biobank 约 **50 万** 参与者 [13]、All of Us 计划至少 **100 万** 人 [14]、FinnGen 224,737 人 [15] 这类生物样本库为建模底座；区别于纯临床预测模型的地方，在于它要求把 EHR 纵向轨迹、胚系遗传与血浆蛋白组/代谢组/甲基化等分子层联合起来，回答风险、轨迹、亚型与共病结构问题。**这一方向的核心不是某一个模型，而是“人群尺度 + 多组学 + 纵向健康记录”三者的可复现整合**：UK Biobank 从芯片插补约 9600 万变异 [16] 到 490,640 人平均 32.5× 全基因组测序 [17]，血浆蛋白组从 54,219 人、2,923 种蛋白的 pQTL 图谱 [6] 到 53,026 人、2,920 种蛋白的蛋白-疾病-性状关联图谱 [18]，正是这一整合得以成立的资源前提。

演化脉络上，该方向经历了三次重心转移。**第一次是从关联扫描转向纵向轨迹建模**：早期 EHR 工作把患者历史当作医学概念序列做未来诊断预测，BEHRT [19] 与 Med-BERT [20] 确立了“预训练 + 微调”的范式，但受限于仅用诊断码、跨机构泛化不足；随后 Delphi-2M 在 UK Biobank 训练、丹麦登记验证，把词表扩展到 ICD-10 顶层诊断、性别、BMI、吸烟、饮酒与死亡，可同时预测 **1000 多种疾病** [1]，Foresight 则把占约 **80%** 的自由文本纳入生成式预训练 [21]。**第二次是从单病种预测转向共病结构与亚型发现**：ATM 在 UK Biobank 282,957 人与 All of Us 211,908 人上识别 **52 种**共病异质性疾病、18 个亚型 PRS 显著异于同病其他亚型 [22]，ALADYNOULLI 进一步把纵向 EHR 诊断、年龄与多基因风险联合建模，在三个生物库 **68.3 万余人**、348 种疾病上识别 21 个可复制特征并做基于特征的 GWAS [3]。**第三次是从临床表型转向分子机制与靶点**：pQTL 图谱把遗传变异锚定到蛋白丰度 [6][23]，蛋白组-疾病图谱把关联推到 183 种疾病 AUC>0.80 与 474 个因果蛋白 [18]，代谢组评分则在 UK Biobank、爱沙尼亚生物库与芬兰 THL 生物库共 **700,217 人** 上实现跨库重复 [24]。

当前方向的核心问题可归为四组张力。**其一是预测性能与个体可靠性之间的张力**：48 个冠心病 PRS 在 All of Us、Penn Medicine 与 UCLA 共 171,095 人中群体表现相似、个体层面一致性却很差 [7]；BMI 多祖源评分在欧洲裔中解释 **17.6%** 变异，其他人群从东亚裔美国人 16% 到农村乌干达 2.2% 不等 [25]。**其三是遗传发现与生物学解释之间的张力**：T2D 全基因组 PGS 在 UKB-PPP 中关联 **648 个**蛋白 [26]，冠心病 526 个显著变异可分解为 **8 个**遗传组分并构建过程特异性 pPRS [27]，但基因组基础模型衍生注释在 27 个 UKB 性状上均未超越 baselineLD，AlphaGenome 与 Borzoi 中位增益仅 **1.8%** 与 **3.8%** [8]，提示“更大模型”并不自动等于“更好机制”。**其四是环境与遗传的相对贡献**：UKB 暴露组全关联在 492,567 人中识别 25 个与死亡和蛋白组衰老时钟相关的独立暴露，环境暴露对死亡与 25 种年龄相关病的解释度常高于基因组 [28]，而 G×E 检验显示幂变换可解释 **45%** 的多基因评分 G×E 信号 [29]，说明部分“交互”可能只是尺度或建模假设的产物。

方法学层面，该方向已形成几条相对独立的技术栈。**纵向 EHR 侧**从 BEHRT/Med-BERT 的序列预训练，走向 GRASP 用大语言模型把医学编码映射到共享语义空间、在 UKB 391921 人、FinnGen 253991 人、Mount Sinai 386755 人上报告跨编码系统迁移增益 [30]，以及 SurvivEHR 基于英国初级保健 2300 万患者、76 亿编码事件的竞争风险时间事件预训练 [31]；**多模态侧**NOAH 基于 MIMIC 家族 **5.59 亿**临床事件、29.9 万患者原生处理图像、时序、分类与文本 [32]，PULSE 则从稀疏常规血检生成代谢组与蛋白组谱、生成蛋白组对 6 种常见病 AUC 达 **0.72–0.83** [33]；**遗传整合侧**从 MSGene 以年龄为时间尺度的多状态模型整合 CAD-PRS 与 EHR [34]，到 ALADYNOULLI 的贝叶斯生成框架 [3]，再到 HELICS 在 UKB 无定相基因型上做全基因组 SNP 级条件合成 [9]。这些栈之间尚缺统一的评测框架：Phecodes 提供了基于 ICD 编码的高通量表型工具 [35]，ICD-8 到 ICD-10 的单向映射使丹麦自 1965 年以来的纵向轨迹可桥接 [36]，GWAS Catalog 截至 2024 年 7 月收录 625,113 条关联、>15.5K 性状 [37]，但**跨队列、跨编码系统、跨祖源的统一基准仍是空白**，这也是该方向从“各自报告增益”走向“可比较证据”的关键瓶颈。

最后需要明确本方向的排除边界与证据强度分层。单中心 <1000 人的关联研究、无公开数据也无代码的纯预测模型、无方法学新意的单病种临床评分改良、以及不与组学/EHR 联合的纯影像 AI，均不构成本方向的核心证据。**当前最稳健的证据集中在资源与关联层**——UK Biobank 的深度表型与测序资源 [16][17]、All of Us 的多样性设计 [14]、pQTL 与蛋白-疾病图谱 [6][18]、跨三国生物库可重复的代谢组评分 [24]；**中等强度证据在共病亚型与纵向轨迹**——ATM、ALADYNOULLI、Delphi-2M 均有外部队列验证，但验证队列仍集中于欧洲祖源人群 [22][3][1]；**最弱的是生成式基础模型在真实临床场景中的净收益**——Foresight-England 定量结果缺失 [2]、LifeLong Digital Twin 未做显著性检验 [4]、EHR-MPC 以仿真评估为主 [38]。大型人群队列正因高通量组学、EHR 普及与 AI 而从描述性关联转向机制发现、精细风险分层与遗传导向的治疗开发，并日益全球化与多样化 [39]；但**这一转向能否成立，取决于跨祖源外推、跨编码系统迁移与统一评测框架这三个尚未解决的问题**。

## 2 方法学


### 2.1 生成式疾病轨迹模型

在纵向电子健康记录上学习疾病轨迹，早期工作以生成式 Transformer 为主。**Delphi-2M** 改造 GPT 架构以建模疾病进展与竞争风险，在 UK Biobank 约 40 万参与者上训练、在丹麦登记数据中验证，词表覆盖 ICD-10 顶层诊断、性别、BMI、吸烟、饮酒与死亡，可同时预测 **1000 多种疾病**的未来发生率并模拟个体终身轨迹 [1]。**Foresight** 则强调把占约 **80%** 的自由文本与结构化数据一起纳入生成式预训练，覆盖 18 类 SNOMED 概念、支持日/周/月不同时间分辨率，并在三家医院的躯体与精神健康数据上测试；作者明确其基于历史实践，当前形式不宜直接用于临床决策支持 [21]。规模化的尝试是 Foresight-England：243M 参数自回归解码器在 NHS England 安全数据环境内从头训练，数据约 6100 万人（训练 5490 万、评估 610 万），但数据访问暂停导致定量结果无法导出，只留下分词、架构、训练与评估的方法学模板 [2]。这一空缺说明，国家级部署的生成式轨迹模型目前仍缺少可核验的性能证据。

另一条路线把生成模型与遗传、多模态或控制目标结合。**ALADYNOULLI** 以贝叶斯生成框架联合建模纵向 EHR 诊断、年龄与多基因风险，用概率混合而非混合概率的形式容纳同时与慢性疾病，在三个生物库 **68.3 万余人**、348 种疾病、52 年随访上识别出 21 个可复制特征，亚型 Cohen's d 达 **4.25**，基于特征的 GWAS 发现 151 个全基因组显著位点，包括单性状分析遗漏的心血管关联 [3]。NOAH 走多模态与时间感知路线，用双向时间整合和变分隐空间原生处理图像、时序、分类与文本记录，基于 MIMIC 家族 **5.59 亿**临床事件、29.9 万患者训练，支持自回归预测、零样本分类与反事实干预模拟，但外部泛化尚待验证 [32]。EHR-MPC 把生成式 EHR 模型当作患者数字孪生，用模型预测控制在推理时规划脓毒症治疗，在 8 家医院 ICU 队列上离线策略性能与强化学习基线相当、模拟性能更优，其局限在于仿真评估与真实临床之间可能存在差距 [38]。LifeLong Digital Twin 则提出把 Life Events 组织为每日 Health States 并累积为 Lifelong Health Context 的统一范式，配合 Agent Harness 整合多模态证据，在 25 个疾病终点、3 类任务、4 个语言模型上，16 个模型-读出比较全部优于无 Context/Harness 的基线，疾病识别 F1 从 **0.422** 升至 0.504（Context）与 0.515（Harness），相对增益 19.4% 与 22.0%；不过该工作缺少配对不确定性、疾病支持计数与组件消融，未确立统计显著性 [4]。

在“生成”与“分型”的交叉处，一批工作用生成式表征服务亚型发现而非直接预测未来事件。AD/PD 研究将诊断前带时间戳的 EHR 按就诊、年龄和日历年标记化，用 Transformer 生成患者嵌入后以 K-means 聚类，在 CPRD Aurum 的 10 万余名患者上识别并在 UK Biobank 外部验证，每种疾病得到 **5 个可复制亚型**，5 年随访显示亚型间死亡与住院预后差异并与基因型关联 [40]。VaDeSC-EHR 则把变分自编码器与 Weibull 混合生存分布直接整合，使风险建模与聚类同步进行，相比先聚类或先分层的方法能识别兼具不同诊断轨迹与时间-事件特征的患者亚群，其限制是聚类数需预设、外部验证有限 [41]。这两项工作与 ALADYNOULLI 的差别在于：后者把遗传信息纳入生成过程并输出可做 GWAS 的特征，前两者主要停留在临床表型层面。

还有一类证据并不依赖生成式架构，却为轨迹建模提供了必要的对照与边界。MiGHT-EHR 用异质时序图加图 Transformer 做多任务预测，在 MIMIC-III/IV 四个任务上平均超越现有方法，死亡率与再入院提升尤为显著，但仅在 MIMIC 两个数据集上验证 [42]。All of Us 的功能衰退研究用 LightGBM 对 12 项常规生物标志物 3 年轨迹特征建模，AUROC **0.797** 显著优于静态汇总的 0.755（P<0.001），匹配分析为 0.727 对 0.680，并可提前 3–12 个月持续预测（AUROC 0.768–0.740），说明简单轨迹特征在缺乏外部队列验证时也能提供独立信号 [5]。这些结果与生成式模型之间尚不可直接比较：各研究队列、结局定义与评估协议不同，且 Foresight-England 的定量结果缺失、LifeLong Digital Twin 未做显著性检验，当前证据不足以判定生成式轨迹模型相对判别式基线在真实临床场景中的净收益。

### 2.2 多组学与遗传整合

以UK Biobank为核心的大规模遗传资源构成了多组学与遗传整合的基础设施。另一项覆盖281,104人的外显子PheWAS识别出**632个**全基因组显著ExWAS变异，并刻画了PTV携带谱[43]；394,841名欧洲裔的外显子分析则系统测试了4,529个表型并公开全部summary statistics[44]。测序资源本身也经历了从首批约5万人[45]到UKB-ESC首批**200,643人**、约1000万变异的开放过程[46]。

常见变异一侧，方法学改进直接改变了发现规模。GeneATLAS汇总了452,264名欧洲裔参与者的118个连续与660个二分类性状，覆盖**9,113,133个**变异关联结果[47]。跨祖源方面，Pan-UKB对7,271个表型做混合模型关联与跨祖源荟萃，新发现**14,676个**仅欧洲祖源分析未检出的位点[48]；GBMI则联合23个生物样本库、**220万人**、14个疾病终点，覆盖六大祖源[49]。这些工作共同表明，样本量与祖源多样性是两个相对独立的增益维度。

罕见变异的效应结构比常见变异更依赖功能注释与建模方式。FinnGen在176,899名芬兰人中分析44,370个编码变异对2,444个疾病表型的单等位与双等位效应，显示纯合子富集可提升隐性致病变异检出，且同一变异在杂合与纯合状态下可呈现不同表型[50]。KASM用35个蛋白结构与功能注释构建核函数，在UKB与All of Us共**786,871人**外显子组、26个复杂性状上刻画基因内等位基因效应的协变结构[51]。非加性效应同样不可忽略：正交等位基因重编码框架在最多399,943名UKB个体、2,906个血浆蛋白中，发现约**三分之一**同源基因-蛋白关系呈非线性剂量效应，且该方法在HWE偏离下保持校准（λGC=0.94），而标准重编码出现膨胀（λGC=78.3）[52]。CNV层面，472,228人的芯片数据揭示了16p11.2、22q11.2、9p23等位点的全表型负担[53]。

血浆蛋白组是遗传整合中数据最密集的层面。UKB Pharma Proteomics Project对**54,219人**、2,923种蛋白开展pQTL定位，发现**14,287个**主要遗传关联，其中**81%**为既往未报道，精细映射出29,420个独立信号[6]。同一队列的罕见变异分析在49,736人中鉴定出**5,433个**罕见基因型-蛋白关联（81%为新），基因水平1,962个关联，STAB1/STAB2分别关联77和41个蛋白，PTV信号**99.4%**与蛋白降低相关[23]。蛋白组图谱将关联扩展到疾病终点：53,026人、2,920种蛋白的分析报告**168,100个**蛋白-疾病关联与554,488个蛋白-性状关联，183种疾病AUC>0.80，并通过pQTL确定474个因果蛋白[18]。

蛋白组遗传架构的精细结构正在被多类设计拆解。蛋白比值GWAS在UKB Olink 1,463种蛋白、54,000余样本中复制**4,248个**rQTL，显著p-gain蛋白对富集已知互作**7.6倍**，比值分析较单蛋白GWAS新增**24.7%**遗传信号[54]。cis-by-trans上位效应映射识别出以**ABO**为中心的稳健互作网络[55]；多祖先MHC-pQTL在2,920种蛋白中鉴定13个cis、**606个**trans关联，多数跨祖先一致，并发现东亚人群EDAR的祖先富集关联[56]。结构变异层面，长读长参考面板插补的54,578个SV与15,826个VNTR共同解释蛋白丰度遗传力约**8.0%**，鉴定8,065个SV-蛋白与4,101个VNTR-蛋白独立关联[57]。祖源与性别是两个反复出现的分层变量：ARIC中欧裔2,004、非裔**1,618**种蛋白有cis关联，非裔样本缩小可信集并发现人群特异pQTL[58]；跨Fenland与UKB的分析显示**69.1%**蛋白存在性别差异，而遗传效应跨性别高度相似，仅103个sd-pQTL[59]。

代谢组提供了蛋白组之外的另一条分子通路。UKB 118,461人、**249项**NMR指标的图谱覆盖700多种疾病的患病、发病与死亡关联，并在THL Biobank 3万余人重复验证[60]。三国生物库**700,217人**的NMR代谢组评分针对12种高DALY疾病训练Cox模型，多数纳入超过半数36个代谢标志物，并实现跨库重复[24]。MetabHub进一步把251项NMR代谢物、129项临床指标、54项环境暴露、全基因组变异与57种新发疾病整合到同一平台，支持性别特异关联与中介分析[61]。这些资源使代谢物成为连接遗传、暴露与疾病结局的中间变量。

将遗传风险映射到具体生物学过程，是整合分析的核心目标之一。T2D全基因组PGS在UKB-PPP中关联**648个**蛋白、617个复制，分区PGS则指向不同生物过程的蛋白集[26]。冠心病方面，对526个显著变异与78个相关表型做潜在因子分解，识别出**8个**遗传组分（如富含胆固醇脂蛋白、脂蛋白(a)、内皮功能障碍、凝血），据此构建的过程特异性pPRS可捕捉传统风险因素之外的生物学特征，并在UKB 458,905人中验证[27]。DeGAs对2,138个UKB表型的截断SVD给出100个潜在成分，PTV在肥胖相关性状上富集，指向脂肪细胞生物学[62]。35项血尿标志物的遗传分析识别**5,794个**独立位点与51个因果关系，多PRS模型在FinnGen中改善慢性肾病、2型糖尿病、痛风与酒精性肝硬化的风险分层[63]。

多基因评分的预测价值与其个体层面可靠性之间存在张力。48个冠心病PRS在AOU、PMBB与UCLA共171,095人中，群体水平表现相似者在个体层面一致性差（ICC与Light κ低）[7]。跨祖源构建方法上，GBMI比较显示PRS-CS总体优于P+T，且欧洲LD面板预测精度相当或更高[64]；All of Us 245,388全基因组序列与UKB联合开发的32个性状多血统PRS则表明，增加多样性提升部分性状精度，但最大化样本量并非普遍最优，PRS精度随血统分歧线性下降、多血统训练可减缓该衰减[65]。汉族人群的TPMI 463,447人研究证明人群特异PRS优于欧洲为主模型[66]；PRS-PAD在三队列中与PAD及主要肢体不良事件显著关联[67]。方法层面，AB-PRS通过自适应提升微调预训练PRS，模拟中各场景R²普遍优于基线且噪声选择比例<28%[68]；家族感知基准则针对亲属数据泄漏问题，将整个家族组分固定分配到发现、校准与测试集[69]。

组学与遗传的整合也被用于靶点发现与药物重定位。脑龄差GWAS发现**2个**新位点与7个已知位点，整合eQTL/pQTL的MR与共定位优先7个可成药基因，并重发现13种有临床试验证据的潜在药物[70]。跨四队列、最多697,815人的PheWAS对19个候选药物靶点做验证，显示其可识别多效性并提示疗效或安全性信号[71]。谵妄研究整合UKB 52,936人、2,911种蛋白的机器学习预测、两样本MR与跨物种蛋白组，识别**1,470个**血浆蛋白标志物并验证候选外周靶点[72]。All of Us多组学队列在蛋白组10,043人与转录组9,043人中检出**182,246个**QTL，54,255个精细定位到罕见变异，罕见变异效应富集于孟德尔疾病基因（OR=1.4）与获批药物靶点[73]。

环境与遗传的相对贡献、以及二者交互，是整合框架必须处理的问题。UKB暴露组全关联在492,567人中识别25个与死亡和蛋白组衰老时钟相关的独立暴露，并发现环境暴露对死亡与25种年龄相关病的解释度常高于基因组[28]。All of Us 10,043人、5,416种蛋白的分析显示蛋白暴露特征跨人群与社会经济阶层基本一致，仅**<1%**蛋白存在显著异质性，BMI为例外、瘦素异质性最高[74]。G×E检验则暴露出尺度问题：在UKB 32个表型中，幂变换可解释**45%**的多基因评分G×E信号，身高G×性别效应随对数尺度消失[29]；fastGxE通过控制多基因效应、多基因交互与噪声异质性，在大型生物样本库中实现**32.98倍以上**速度提升[75]。这些结果提示，部分所谓交互可能只是表型尺度或建模假设的产物。

纵向与多模态数据结构要求专门的方法设计。ATM对UKB 282,957人与All of Us 211,908人的纵向EHR做低秩表示，识别**52种**共病异质性疾病，18个亚型的PRS显著异于同病其他亚型[22]。SPA_GRM针对纵向性状控制样本亲缘关系，在UKB 79个纵向性状中识别**7,463个**遗传位点[76]。PULSE从稀疏常规血检生成代谢组与蛋白组谱，生成代谢组优于所有基准，生成蛋白组对6种常见病AUC达**0.72–0.83**，接近真实蛋白组数据[33]。表型填充同样能提升效力：流体智力评分填充使样本量从约27万增至超**45.5万**，独立显著常见SNP关联从390增至550，罕见变异分析鉴定26个显著基因[77]。

若干证据对当前方法的增益提出了审慎甚至相反的判断。基因组基础模型衍生的注释在27个UKB性状上均未超越baselineLD，AlphaGenome与Borzoi的中位增益分别为**1.8%**与**3.8%**，低于baselineLD的5.1%，GPN-Star甚至减少位点发现[8]。多组学评分的整合虽已推进到蛋白组、多基因与甲基化评分的组合（UKB 50,673人构建、PURE 9,358人验证的4种MEGASCORE）[78]，以及APOE4经脑结构与外周分子中介痴呆风险的因果中介解析[79]，但多数摘要未给出可比的定量预测性能。跨祖源APOE PheWAS在367,757人中识别**27个**相关表型，9个关联具祖源特异性[80]；MCPS与UKB比较显示克隆性造血在MCPS显著更少（调整OR=0.59），且频率与欧洲祖源比例正相关[81]。这些差异说明，整合模型的迁移性仍受祖源、表型定义与评估设计的三重制约。

### 2.3 医学 / EHR 基础模型

在结构化电子健康记录（EHR）上，早期工作主要把患者历史视为医学概念序列，用Transformer做未来诊断预测。**BEHRT**将就诊位置、年龄和事件顺序纳入个体表示，在多项未来诊断预测任务中优于Deepr、RNN、LSTM和RETAIN等基线[19]。随后**Med-BERT**把BERT式自监督预训练迁移到ICD诊断序列，先在大规模数据上预训练再针对糖尿病、心衰等任务微调，结果显示预训练可提升预测性能，尤其在标注样本有限时[20]。两者都受限于仅用诊断码、跨机构泛化未充分验证；Med-BERT明确未纳入药物与检验信息[20]。

跨机构、跨编码系统的迁移是后续工作的重点分歧所在。**GRASP**用大语言模型将医学编码映射到共享语义空间，再结合transformer预测21种疾病和全因死亡，在UKB 391921人、FinnGen 253991人、Mount Sinai 386755人上评估，报告平均ΔC-index较语言无关模型在芬兰高**88%**、美国高**47%**，且62%疾病与多基因风险评分的相关性显著更高[30]。与之不同，**SurvivEHR**面向多长期病症共病，采用竞争风险时间事件预训练目标，基于英国初级保健2300万患者、76亿编码事件训练，风险分层超越基准生存模型并支持低资源微调迁移，但外部多国泛化尚未验证[31]。上述迁移增益均来自各自研究内部的对照，不同队列间的数值不宜直接比较。另一条路线是**EHRAgent**，让LLM智能体自主生成并执行代码以完成多表EHR推理，在三个真实EHR数据集上成功率最高超最强基线**29.6%**，少样本即可处理复杂临床任务，但依赖代码执行反馈迭代且仅在三个数据集上验证[82]。

### 2.4 组学衰老时钟与纵向多组学动态

纵向多组学证据的核心进展，是把衰老时钟从单时点横断面估计推进到对轨迹、速度和累积负担的建模。ARIC 研究用三次访视的血浆蛋白组（SomaScan 5K）构建纵向蛋白衰老指数 **LPAI**，先以 FPCA 提取纵向成分、再用 Cox 弹性网训练死亡风险模型，并在 MESA 验证；作者明确指出既往蛋白时钟基于横断面数据、只能反映单时点累积负担，而 LPAI 同时捕捉衰老累积负担与变化速度，较单时点蛋白时钟提供额外预测信息 [10]。与之呼应，335 名女性 8 年全血纵向多组学分析发现 **5,061 个基因和 181 个代谢物**随时间变化，且个体轨迹常偏离群体水平趋势，提示群体时钟与个体动态之间存在系统性差异 [83]。这两项工作共同把「纵向」本身作为信息源，但前者落在蛋白组与死亡预测，后者落在基因表达/代谢组的个体动态刻画，随访时长与组学层次不同，不能直接比较效应大小。

在组学层次与器官维度上，多项工作把时钟从整体衰老拆向特定组学或器官。UK Biobank 274,247 人、107 个血浆非衍生代谢物被用于构建 5 个器官特异性代谢组生物年龄 **MetBAG**，独立测试 Pearson r 为 **0.25–0.42**，并关联 525 个疾病终点、预测 14 类疾病与死亡风险 [11]；同一队列 409,206 人、14 个器官则整合 NMR 代谢组、Olink 蛋白组与临床表型构建多组学器官时钟，其关键论点是年龄加速与死亡风险构成器官生物学的**不同维度**，具有可分离的表型、分子和遗传结构 [84]。这两项研究都基于 UK Biobank，但前者以代谢物单一组学定义器官年龄差、后者以多组学整合定义器官时钟，且对「年龄加速是否等同于风险」给出不同侧重——前者直接把 MetBAG 与疾病/死亡关联，后者强调加速与死亡风险可分离，构成该子问题上值得注意的张力。蛋白组方面，UK Biobank 45,438 人分析显示体力活动越高 **ProtAgeGap** 越低，ProtAgeGap 与 2 型糖尿病风险 HR=**1.06**、高活动交互 HR=**1.05**，并在 26 名男性的 12 周监督运动研究中使 ProtAgeGap 下降相当于 **10 个月** [85]；该干预样本量小、以观察性关联为主，其「可逆性」结论的强度明显弱于上述预测性队列证据。

非蛋白组学路线则把纵向动态扩展到临床常规数据与节律维度。DFTJ 中国老年人队列用 36 项常规临床指标、以限制立方样条 Cox 捕捉 U 型关系构建生理衰老指数 **PAI/ΔPAI**，并在 UK Biobank 中验证其与死亡、心血管病及 9 种慢性病的关联，作者称其优于仅以年龄为标签的模型 [12]；ClinicalAge 则从 UK Biobank 与 CPRD Aurum 的纵向电子健康记录（诊断与用药轨迹）估计衰老程度并评估发病与死亡风险 [86]。这两项工作说明纵向信息不必来自高通量组学，常规临床与 EHR 轨迹同样可承载衰老动态，但其证据以关联预测为主，机制解释有限。另一条线索提示纵向组学动态中的时间混杂不可忽视：UK Biobank 420,746 人、312 种血液学/生化/代谢分子与采血时间的分析推导出相位偏移与节律紊乱两个正交指标，其中节律紊乱基本独立于睡眠，可独立预测 **98 种**未来发病风险并映射到肝脏代谢通路 [87]；这与前述纵向研究将遗传、昼夜节律、季节和污染物列为轨迹影响因素的说法一致 [83]，也提示单次采样的时钟估计可能混入采样时刻相关的节律成分。总体而言，现有证据在「纵向时钟是否优于横断面时钟」「年龄加速是否等同于死亡风险」上尚未收敛，且多数模型训练与验证集中于 UK Biobank/ARIC/MESA 等队列，跨人群外推仍是共同局限 [10][11][12]。

### 2.5 隐私保护合成基因组与生物样本库规模生成

面向生物样本库规模的基因型数据，**HELICS** 提出了无定相的潜空间流匹配框架，用于在数十万至数千万相关 SNP 的超高维离散分布上做条件合成基因组生成，目标场景包括隐私保护的基准测试、模拟与数据增强，尤其针对代表性不足人群、罕见或失衡疾病队列及受限生物样本库等数据有限情形 [9]。方法上采用染色体特异编码与多染色体潜空间流实现全基因组 SNP 级生成，并支持性状条件合成；数据上使用 UKB 无定相基因型，覆盖 chr15 的 **18,784 SNP** 及全基因组 **600,336 SNP** [9]。

在与 HAPNEST、Sim1000G、HAPGEN2、GAN、RBM、HCLT 等基线的对比中，HELICS 在 chr15 及全 22 条常染色体基准上于 MAF、LD 和隐私代理指标上优于 HAPNEST 等基线，并能对多基因性状的遗传易感性进行条件控制 [9]。其局限在于低 MAF 变异 R² 偏低，且生成样本的 NN IBS 相似度较高，提示多样性有限 [9]。

## 3 数据与资源

人群健康与多组学 AI 所依赖的资源，首先是以大型前瞻性队列为骨架、叠加深度组学与健康记录链接的基础设施。**UK Biobank** 纳入约 **50 万** 40–69 岁参与者，2006–2010 年完成基线评估，收集问卷、体格测量、生物样本、影像、加速度计及健康记录链接数据，并预计 20 年随访期间累积糖尿病约 68,000 例、心梗与冠心病死亡 47,000 例、卒中 20,000 例、阿尔茨海默病 30,000 例 [13]。其遗传资源从芯片基因型扩展到全基因组测序：早期对全部参与者完成质控、群体结构与亲缘关系分析，插补约 **9600 万** 变异及 11 个 HLA 基因经典等位变异，并以身高 GWAS 和 HLA-疾病关联复制验证数据质量 [16]；后续对 **490,640** 人完成平均 **32.5×** 的全基因组测序，识别约 15 亿变异，较芯片插补增 18.8 倍、较全外显子测序增 >40 倍，其中 93.5% 为非芬兰欧洲 ancestry [17]。该队列的局限也被明确指出：年龄范围 40–69 岁为折中，可能影响暴露与结局时序 [13]；参与者相对健康、以欧洲 ancestry 为主 [16]；健康志愿者偏倚且部分神经疾病病例仍有限 [88]。

与 UK Biobank 的深度单队列路线不同，**All of Us** 以多样性和规模为目标，计划在美国招募至少 **100 万** 人；截至 2019 年 7 月，超过 175,000 人贡献生物样本，其中 >80% 来自历史上研究不足群体，34 个站点收集了 >112,000 人的 EHR 数据 [14]。其数据来源本身成为研究对象：一项比较患者介导 EHR（PME）与提供者来源 EHR（HPO）的工作纳入 393,590 名参与者（PME 19,703、HPO 373,887），发现 PME 人群更白、更女性、更多保险、随访更长，WGS 覆盖更少（35.2% vs 83.2%），并在疾病患病率、10 个表型 PheWAS 及 5,000 多个已知基因型-表型关联复制率上存在系统差异 [89]。这提示同一队列内部不同采集路径的数据效用不可互换，是 AI 建模前必须处理的异质性来源。

在人群遗传发现层面，隔离人群提供了与主流欧洲队列互补的变异谱。**FinnGen** 基于 224,737 人插补基因型和 **1,932** 个终点开展 GWAS 与统计精细定位，发现芬兰隔离人群富集低频有害等位（0.1% ≤ MAF < 5%），并能在既往研究充分的疾病中识别新的低频变异关联和可能因果编码变异 [15]。其外推限制同样明确：芬兰隔离人群遗传结构特殊，结果推广至其他人群受限 [15]。多国生物样本库综述将 UK Biobank、All of Us、新加坡 PRECISE、Biobank Japan 和韩国 NPBBD-Korea 并列比较，指出 WGS 可发现罕见变异、结构变异和调控元件，但计算基础设施、隐私伦理、临床整合和祖先多样性不足仍是共同挑战 [90]。

表型侧的资源建设围绕 EHR 编码与标准化展开。**Phecodes** 作为基于 ICD 编码的高通量表型工具，可快速定义数千种临床有意义疾病和状况的病例/对照状态，最初用于 PheWAS，后扩展到表型风险评分等方法，但其依赖 ICD 编码，可能存在编码误差和表型异质性 [35]。跨版本编码的统一是纵向研究的前提：一项工作构建了 ICD-8 到 ICD-10 的单向映射，覆盖完整 ICD 及丹麦本地扩展，可连接丹麦自 1965 年以来超半世纪的医疗数据，但未提供 ICD-10 回映射 ICD-8 [36]。在更宏观的尺度上，基于爱沙尼亚 30% 随机人群样本 EST-Health-30 的自动化框架将异质临床事件压缩为以诊断为中心的标准化摘要，形成覆盖 **1000 多个** ICD-10 三位字符诊断类别的全国尺度诊疗模式数字图谱，其局限是回顾性观察设计且仅基于单一国家样本 [91]。

数据的可复用性还依赖汇总层资源与工具链。**NHGRI-EBI GWAS Catalog** 截至 2024 年 7 月收录 625,113 条关联、>15.5K 性状和 >85K 全基因组汇总统计数据集，通过 EFO 性状映射、祖源框架和与 PGS Catalog 互链提升可复用性，但汇总统计标准化不足、非欧祖源仍偏少、依赖作者提交 [37]。多基因风险评分方面，UK Biobank PRS Release 覆盖 **28 种疾病和 25 种数量性状**，基准测试显示其优于 81 个已发表 PRS 并在其他队列验证，但主要基于 UK Biobank 人群，跨种族适用性有限 [92]。分析工具上，PHESANT 以规则算法为 UK Biobank 异质表型自动选择统计检验并输出图表，依赖 UKB 变量规则、自动化模型未必适用于所有复杂表型 [93]；PheWeb 整合 Manhattan、LocusZoom 和 PheWAS 视图支持单性状与多性状切换，但仅做可视化与共享、不含统计建模 [94]。

组学数据的质量控制是上述资源可用性的隐性前提。针对 UK Biobank 约 **121,657** 人、168 个标志物加 81 个比值的 NMR 代谢数据，一项工作识别了样本制备时间、运输板孔位、光谱仪批次与时间漂移等技术变异来源，多数标志物技术因素中位解释 1.5%，3,169 个盲重复中位 CV 4.55%、R² 0.928，并发布 ukbnmr R 包，但仅覆盖约三分之一 UKB 参与者且基于已校准浓度而非原始谱 [95]。从趋势看，大型人群队列正因高通量组学、EHR 普及和 AI 而整合深度分子 profiling 与纵向真实世界数据，从描述性关联转向机制发现、精细风险分层和遗传导向的治疗开发，并日益全球化与多样化 [39]；UK Biobank 自身的使用统计亦显示其已超 8000 机构使用、8000 余篇论文，且遗传证据使药物获批概率高 2 倍以上 [88]。

## 4 应用与结果

在跨祖源遗传关联发现方面，Pan-UK Biobank 对 UK Biobank 多遗传祖源人群开展混合模型关联与跨祖源荟萃分析，覆盖比以往更大比例的样本，产出 **7,266 个性状**的公开汇总统计，并报告了 **14,676 个仅欧洲祖源分析未发现的显著位点**，如 CAMK2D 与甘油三酯、G6PD 多效错义变异；但多数关联仍主要见于欧洲祖源，解释需注意人群结构等 caveats [96]。多基因评分方面，基于 GIANT 与 23andMe 最多 510 万人数据构建的祖源特异与多祖源 BMI 评分，其多祖源评分在 UK Biobank 欧洲裔中解释 **17.6%** 的 BMI 变异，其他人群从东亚裔美国人 16% 到农村乌干达 2.2% 不等，显示非欧洲裔预测效能显著较低；儿童期加入评分使 8 岁时解释方差从 11% 升至 21%，5 岁时对 18 岁 BMI 的预测从 22% 升至 35% [25]。

在冠心病风险预测上，不同方法给出了互补但需区分设计的证据。MSGene 以年龄为时间尺度的多状态模型整合 CAD-PRS、EHR 与时间依赖协变量，跨 10 个心脏代谢状态估计终身风险，相对 Framingham 30 年与 PCE 10 年模型可提供动态、年龄特异的终身风险并用于他汀治疗决策 [34]。同一问题上的时变分析（FOS 3,588 人、UK Biobank 327,837 人）显示 PRS 风险比从 19 岁 **3.58** 降至 70 岁 **1.51**，40–45 岁组 PRS 显著优于 PCE、多 3.2 倍适宜 [97]；两项工作对 PRS 价值的表述并不冲突，但前者强调终身动态建模、后者强调年龄段的相对优势，且后者指出两队列年龄范围有限、未涵盖全生命周期。蛋白组学路线在 UK Biobank 中按地区划分训练 32,330、内部验证 13,857、外部验证 5,775 人，整合传统风险因素、PRS 与 202 蛋白 LASSO Cox 评分后用 CatBoost 建模，内部验证 AUC 从 **0.750 升至 0.789**、外部验证从 **0.717 升至 0.762**，9 蛋白面板即可捕获大部分预测信息 [98]。

多病共存与多模态框架方面，UKB-MDRMF 整合基本、生活方式、测量、环境、遗传和影像六类数据联合建模 **1,560 种疾病**，联合预测优于单类别评估，并揭示风险因素-疾病及共病关联，提供交互平台，但依赖 UKB 人群、存在缺失值插补与遗传/影像覆盖不全 [99]。PheMIME 则整合 VUMC、Mass General Brigham、UK Biobank 三大 EHR 系统的表型组多病共病汇总统计，结合增强版 associationSubgraphs 实现跨系统交互可视化与疾病聚类推断，并以精神分裂症为例展示跨系统共病网络，其局限是依赖已有汇总统计、未提样本量与统计效能细节 [100]。代谢组学层面，EPIC-Norfolk 对 >11,000 人、>1,000 种代谢物与 27 种新发 NCD 做关联，发现 **640 个显著代谢物-疾病关联**，其中 **420 个（65.5%）跨≥2 种 NCD 共享**，涉及肝肾功能、脂糖代谢、低度炎症和肠道微生物等通路，并上线开放网络服务器；局限为观察性、单一队列、单时点测量 [101]。在 UK Biobank 代谢组数据中，MVX 每 1-SD HR=**1.213**、MetaboHealth HR=**1.503**，随访 8,876 人发病，提示代谢负担可补充传统风险因素，但为观察性设计、残余混杂与单时点测量限制因果推断 [102]；美国整合医疗系统 54,933 人中加入 250 个 NMR 代谢标志物后几乎所有 9 个心血管-肾脏-代谢终点判别能力提升，2 型糖尿病、慢性肾病和代谢功能障碍相关脂肪性肝病增益最大 [103]。心肾代谢共病与衰老方面，330,177 名 UKB 参与者、2,911 个血浆蛋白的多状态模型显示生物衰老可预测 CRM 共病进展并识别关键中介血浆蛋白，属观察性队列、中介推断因果性有限 [104]。

蛋白组与多组学在具体疾病早期识别中的应用呈现方法差异。胰腺癌方向用丹麦 DNPR 与美国 VA EHR 的纵向疾病轨迹训练深度学习模型，可提前最多 3 年预测风险并输出分时间间隔的增量风险，支持监测项目设计，但为回顾性登记数据、外推有限、筛查成本与假阳性需权衡 [105]。HFpEF 方向用 UKB 蛋白/代谢/影像/EHR 多组学（HFpEF 33,480 例）训练监督分类器并在独立多中心 80/20 验证，结合无监督聚类划分多组学亚型与可解释 AI、去混杂和通路分析揭示分子异质性，局限包括 HFpEF 定义依赖多阶段规则、影像/NT-proBNP 缺失者用替代标准、以欧洲人群为主 [106]。骨质疏松方向以 XGBoost+SHAP 构建 SPX-OP 模型，SHAP 筛选的 FSHB、ADIPOQ、SOST、COL9A1、CHAD 等少数标志物即可区分正常、现患与未来发病且优于全蛋白组模型，但全文未获取、外部验证与样本规模细节不明 [107]。高血压人群心衰预测中，16,128 名参与者检测 2,911 种 Olink 蛋白、1:1 划分训练验证，随访 15.1 年 1,074 人（6.66%）发生心衰，NT-proBNP 关联最强（HR=**1.68**），蛋白组学提升风险预测，局限为观察性、仅高血压人群、需外部验证 [108]。

跨队列泛化性与分层异质性是上述应用共同面对的问题。UK Biobank 53,026 人 Olink 蛋白组训练的 15 种疾病预测模型平均 AUC **0.74**（范围 0.56–0.89），较仅用临床因素平均提升 **ΔAUC=0.03**，且不依赖模型架构、简单模型如 L2 表现相当，研究提示跨队列泛化性受表型定义影响 [109]。痴呆风险预测中，43,759 名 UKB 参与者按性别与 APOE ε4 分层，APOE ε4 与痴呆关联存在性别差异（交互 p=**0.027**），携带者模型 AUC **0.85–0.90**、女性携带者最佳，多数关键分子预测因子为亚组特异（女性 C7、CDON、EDIL3；男性 KLK4、MMP12、TGFBI）[110]。药物基因组学方面，UKB 与 All of Us 的 EHR 纵向用药与生物标志物数据对 10 个药物-表型对（他汀 LDL-C、二甲双胍 HbA1c、降压药 SBP 等）做常见变异 GWAS 与罕见变异负荷检验并在 All of Us 重复，证明疾病 PRS 可预测药效，但 EHR 用药与检测时点不齐、依从性/适应证混杂、纵向表型分析陷阱多 [111]。这些结果共同表明，多组学与 AI 模型的增益在不同祖源、性别、疾病定义与队列间并不均一，跨队列迁移前需针对表型定义与亚组异质性做验证。

## 5 评测、可复现性与争议

在大规模生存分析的可扩展推断上，**贝叶斯Cox回归结合随机变分推断**试图回应电子健康记录数据高维、时变协变量多、难以整体载入内存的困难：该方法基于计数过程表示的Cox偏似然，通过随机变分推断与似然重加权使后验可因子化到子样本，在模拟与**UK Biobank心肌梗死**应用中可处理**百万级数据点**并给出可行不确定性估计[112]。其代价是依赖变分近似、精度受子采样影响，且评测仅以传统Cox模型实现为对照，属于同一研究内部的比较，尚不足以说明跨队列的普遍优势[112]。另一篇关于电子健康记录共病研究的AI方法综述仅见标题与主题，缺少可核对的方法与结果细节，无法就评测与可复现性提供实质证据[113]。

## 6 空白与趋势

现有证据在“生成式轨迹模型是否优于判别式基线”上尚未收敛，且多数比较受制于队列、结局定义与评估协议的不一致。Delphi-2M 在 UK Biobank 训练、丹麦登记验证，可同时预测 1000 多种疾病 [1]；Foresight 覆盖 18 类 SNOMED 概念并明确当前形式不宜直接用于临床决策 [21]；Foresight-England 虽在约 6100 万人数据上训练，却因数据访问暂停无法导出定量结果 [2]。与之对照，MiGHT-EHR 仅在 MIMIC-III/IV 上验证 [42]，All of Us 的 LightGBM 轨迹模型 AUROC 0.797 优于静态 0.755 但缺外部队列验证 [5]。**因此，当前最紧迫的空白不是再训练一个更大的生成模型，而是建立跨队列、预注册、可核验的评测协议**，把 Foresight-England 这类“有架构无结果”的工作纳入统一基准。

多组学与遗传整合的空白集中在三个层面。其一是**从关联图谱走向可复现的预测增益**：血浆蛋白组图谱已报告 183 种疾病 AUC>0.80 并确定 474 个因果蛋白 [18]，代谢组评分在三国 700,217 人中跨库重复 [24]，但多数整合评分（如 UKB 50,673 人构建、PURE 9,358 人验证的 MEGASCORE）未给出可比的定量预测性能 [78]。其二是**祖源与个体层面可靠性**：48 个冠心病 PRS 在 171,095 人中群体表现相似而个体一致性差 [7]，多血统 PRS 精度随血统分歧线性下降 [65]，提示跨祖源迁移仍是整合模型的共同瓶颈。其三是**环境与遗传的相对贡献尚未进入预测框架**：UKB 暴露组分析显示环境对死亡与 25 种年龄相关病的解释度常高于基因组 [28]，而 G×E 信号中 45% 可由幂变换解释 [29]，说明现有“遗传+组学”模型可能系统性遗漏了尺度依赖的交互结构。

纵向与衰老时钟方向的空白在于**动态定义与结局锚定的分离**。LPAI 用三次访视蛋白组捕捉累积负担与变化速度 [10]，335 名女性 8 年纵向多组学显示个体轨迹常偏离群体趋势 [83]；但 UKB 274,247 人的 MetBAG 直接把器官年龄差与疾病/死亡关联 [11]，而 409,206 人的多组学器官时钟强调年龄加速与死亡风险是**可分离的不同维度** [84]。**“纵向时钟是否优于横断面时钟”“年龄加速是否等同于风险”两个问题均未收敛**，且训练与验证集中于 UK Biobank/ARIC/MESA，跨人群外推仍是共同局限 [10][11][12]。此外，采血时刻相关的节律成分可独立预测 98 种未来发病 [87]，提示单次采样时钟估计可能混入采样时间混杂，这一方向几乎无人系统处理。

资源与评测层面的空白同样明确。UK Biobank 已完成 490,640 人 32.5× WGS [17]，All of Us 计划百万级且 >80% 来自研究不足群体 [14]，但同一队列内 PME 与 HPO 两种采集路径在患病率、PheWAS 与关联复制率上存在系统差异 [89]，**数据采集路径异质性尚未被主流建模流程显式处理**。GWAS Catalog 收录 625,113 条关联但非欧祖源仍偏少 [37]，UKB PRS Release 覆盖 28 种疾病和 25 种数量性状却主要基于 UKB 人群 [92]。与此同时，基因组基础模型注释在 27 个 UKB 性状上均未超越 baselineLD（AlphaGenome 与 Borzoi 中位增益 1.8% 与 3.8%，低于 5.1%）[8]，**这提示“更大模型必然更好”的假设在人群遗传学任务上缺乏证据支持**，亟需把负结果纳入常规报告。

综合来看，该方向正从“单队列、单组学、单病种预测”转向“跨队列、多组学、轨迹与亚型并重”，但**可复现性基础设施明显滞后于模型规模的增长**。可列为优先空白的方向包括：(1) 国家级生成式 EHR 模型的可核验外部评测，当前仅有方法学模板而无性能证据 [2]；(2) 多组学整合评分的头对头基准，现有工作多各自报告 AUC 而缺统一协议 [18][24]；(3) 纵向时钟的因果锚定与采样时刻校正 [10][87]；(4) 采集路径与祖源异质性的显式建模 [89][7]；(5) 把负结果与失败复现纳入公开基准 [8]。这些空白共同指向一个判断：**该方向的下一阶段瓶颈不在模型容量，而在数据治理、评测标准与跨人群可迁移性**。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 生成式疾病轨迹模型 | 朝阳 | [21] 用 GPT 式生成预训练建模患者时间线（Foresight），[1] 用生成式 transformer 学习人类疾病自然史，两篇均为近两年高影响力工作，说明「EHR 序列 → 生成式轨迹」范式已被顶刊接受；但 [41] 仍在做纵向生存数据的深度表征聚类、[3] 提出贝叶斯纵向 EHR+遗传框架，方法路线（生成式 vs 表征学习 vs 贝叶斯）尚未收敛，属近两年爆发、方法未定型的朝阳期。 |
| 2.2 多组学与遗传整合 | 成熟 | [6] 的 UK Biobank 血浆蛋白组-遗传-健康关联图谱与 [63] 的 35 项血尿标志物遗传学，已把 pQTL/生物标志物遗传图谱做成标准化资源；[114] 的 BOLT-LMM 类混合模型关联与 [115] 的外显子组测序分析表明统计方法已收敛、以规模和增量为主，属成熟期。 |
| 2.3 医学 / EHR 基础模型 | 萌芽 | [20]（Med-BERT）与 [19]（BEHRT）是结构化 EHR 预训练的早期代表，但雷达样本中该节仅 5 篇、CNS 占比 0；近两年 [82]（EHRAgent）与 [30]（LLM 提升 EHR 模型可迁移性）仍在探索 LLM/agent 新路线，说明方向有探索但未形成稳定范式，属萌芽。 |
| 2.4 组学衰老时钟与纵向多组学动态 | 朝阳 | [11] 的多器官代谢组生物学年龄与 [10] 的纵向蛋白组衰老指数预测死亡/多病，均为 2025 年新工作且直接对接人群健康结局；[85] 用 UK Biobank 蛋白组衰老验证运动逆转，说明「组学时钟 → 干预/结局验证」正在快速扩张，但样本中位数引用仅 1、方法各异，属近两年爆发、未收敛的朝阳期。 |
| 2.5 隐私保护合成基因组与生物样本库规模生成 | 证据不足 | 雷达样本中仅 [9]（HELICS 生物样本库规模条件合成基因组）一篇，无法判断阶段。 |
| 3 数据与资源 | 成熟 | [13] 与 [16] 确立 UK Biobank 作为开放资源与深度表型标准，[15]（FinnGen）与 [14]（All of Us）表明多队列资源格局已稳定，属成熟的基础设施层。 |
| 4 应用与结果 | 朝阳 | [105] 用疾病轨迹深度学习预测胰腺癌风险、[101] 用血浆代谢组刻画非传染性疾病多病通路，显示应用层已出高影响力结果；[96]（Pan-UKB GWAS）与 [25]（BMI 多基因预测贯穿生命历程）说明应用仍在快速扩展、尚未饱和。 |
| 5 评测、可复现性与争议 | 证据不足 | 雷达样本中仅 [112]（大规模 EHR 贝叶斯 Cox）与 [113]（共病 AI 方法综述）两篇，且均非专门评测框架，不足以判定阶段。 |

**整体判断**：这个方向整体处于**朝阳期偏成熟的分层状态**——基础设施（2.2 多组学遗传整合、3 数据资源）已成熟、以增量和规模为主；而**生成式疾病轨迹（2.1）、组学衰老时钟（2.4）、应用层（4）近两年集中爆发**，雷达样本中 2.1 近两年占比 **0.9**、2.4 为 **0.8**，但方法路线（生成式 transformer vs 贝叶斯纵向框架 vs 表征聚类）尚未收敛，评测与可复现性（第 5 节仅 2 篇）明显滞后。窗口期估计 **1–2 年**：一旦 EHR 基础模型与轨迹生成的方法范式被少数团队锁定、且 UK Biobank/All of Us 上的基准评测标准化，后来者只能做增量。最大不确定性是**跨队列可复现性与外部验证缺失**——现有高影响力工作多集中在 UK Biobank 单队列，FinnGen、All of Us 上的迁移与公平性证据薄弱，且隐私/合成数据路线（2.5）几乎空白，可能改变数据获取与建模的整个前提。

**接下来怎么做**：
1. **把衰老时钟接到人群健康结局上做纵向验证**：用 UK Biobank 血浆蛋白组/代谢组 + 重复测量，构建纵向组学衰老指数并预测多病共存与死亡，方法上对比静态时钟与动态轨迹模型。现在做是因为 [11] 与 [10] 刚证明可行但样本小、方法未定，[85] 显示干预可逆性可验证——正好衔接他的衰老 + 多组学背景，且能复用类器官项目的蛋白/代谢标志物做机制解释。
2. **做「生成式轨迹 + 多组学」的交叉切口**：以 [21] 与 [1] 的 EHR 生成式轨迹为骨架，把血浆蛋白组/pQTL 作为条件输入，预测疾病轨迹并做机制归因。现在做是因为轨迹模型尚未整合组学、[3] 刚提出贝叶斯 EHR+遗传框架，空白明确；产出可对接公共数据 demo。
3. **主攻跨队列可复现性作为方法学卖点**：在 UK Biobank 训练、FinnGen/All of Us 外部验证多组学风险与轨迹模型，量化迁移损失并给出校正方法。现在做是因为 [15] 与 [14] 提供队列基础，而第 5 节评测证据仅 [112]、[113] 两篇，评测缺口就是发表空间。
4. **用类器官多组学做小规模机制锚定**：把人群 pQTL/蛋白组发现的候选标志物在类器官模型中做扰动验证，形成「人群关联 → 类器官因果」的闭环。现在做是因为 [6] 的 pQTL 图谱提供了大量可验证靶点，而多数人群研究缺机制验证，这是他与众不同的合作优势。
5. **避开纯 EHR 基础模型的红海预训练**：不追 Med-BERT/BEHRT 式通用预训练（[20]、[19] 已被大厂占据），而是做**面向多组学条件化的轻量适配与评测基准**，结合 [30] 的可迁移性思路，产出可复现 benchmark，风险低、差异化强。

## 参考文献

1. Learning the natural history of human disease with generative transformers.. Nature 2025. https://doi.org/10.1038/s41586-025-09529-3
2. Foresight-England: Development of a National-Scale Generative AI Model of Electronic Health Records for Medical Event Prediction across the COVID-19 Pandemic.  2026. https://arxiv.org/abs/2608.16273
3. A Bayesian framework for longitudinal EHR and genetic discovery. Nature 2026. https://doi.org/10.1038/s41586-026-10780-5
4. LifeLong Digital Twin: A Unified Modeling Paradigm and Agent Harness for Event-Driven Lifelong Health State Trajectories.  . https://arxiv.org/abs/2610.05566
5. Predicting Early Functional Decline from Longitudinal Laboratory and Vital Sign Trajectories: A Large-Scale Study Using the All of Us Research Program.  2026. https://arxiv.org/abs/2608.21589
6. Plasma proteomic associations with genetics and health in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06592-6
7. Evaluating Performance and Agreement of Coronary Heart Disease Polygenic Risk Scores.. JAMA 2025. https://doi.org/10.1001/jama.2024.23784
8. Genomic foundation models do not yet boost common variant discovery beyond standard functional annotations.  . https://doi.org/10.64898/2026.10.13.758880
9. HELICS: Biobank-scale Conditional Synthetic Genome Generation via Latent Flow Matching.  . https://arxiv.org/abs/2610.36361
10. A Novel Longitudinal Proteomic Aging Index Predicts Mortality, Multimorbidity, and Frailty in Older Adults.. Aging cell 2025. https://doi.org/10.1111/acel.70317
11. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
12. Estimation of physiological aging based on routine clinical biomarkers: a prospective cohort study in elderly Chinese and the UK Biobank.. BMC medicine 2024. https://doi.org/10.1186/s12916-024-03769-2
13. UK Biobank: An Open Access Resource for Identifying the Causes of a Wide Range of Complex Diseases of Middle and Old Age. PLoS Medicine 2015. https://doi.org/10.1371/journal.pmed.1001779
14. The “All of Us” Research Program. New England Journal of Medicine 2019. https://doi.org/10.1056/NEJMsr1809937
15. FinnGen provides genetic insights from a well-phenotyped isolated population. Nature 2023. https://doi.org/10.1038/s41586-022-05473-8
16. The UK Biobank resource with deep phenotyping and genomic data. Nature 2018. https://doi.org/10.1038/s41586-018-0579-z
17. Whole-genome sequencing of 490,640 UK Biobank participants.. Nature 2025. https://doi.org/10.1038/s41586-025-09272-9
18. Atlas of the plasma proteome in health and disease in 53,026 adults.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.045
19. BEHRT: Transformer for Electronic Health Records. Scientific Reports 2019. https://doi.org/10.1038/s41598-020-62922-y
20. Med-BERT: pretrained contextualized embeddings on large-scale structured electronic health records for disease prediction. npj Digital Medicine 2020. https://doi.org/10.1038/s41746-021-00455-y
21. Foresight—a generative pretrained transformer for modelling of patient timelines using electronic health records: a retrospective modelling study. The Lancet Digital Health 2024. https://doi.org/10.1016/s2589-7500(24)00025-6
22. Age-dependent topic modelling of comorbidities in UK Biobank identifies disease subtypes with differential genetic risk. Nature Genetics 2023. https://doi.org/10.1038/s41588-023-01522-8
23. Rare variant associations with plasma protein levels in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06547-x
24. Metabolomic and genomic prediction of common diseases in 700,217 participants in three national biobanks.. Nature communications 2024. https://doi.org/10.1038/s41467-024-54357-0
25. Polygenic prediction of body mass index and obesity through the life course and across ancestries.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03827-z
26. Identification of plasma proteomic markers underlying polygenic risk of type 2 diabetes and related comorbidities.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56695-z
27. Decomposing polygenic risk of coronary artery disease into distinct biological processes.  . https://doi.org/10.64898/2026.10.08.26365088
28. Integrating the environmental and genetic architectures of aging and mortality.. Nature medicine 2025. https://doi.org/10.1038/s41591-024-03483-9
29. Choice of phenotype scale is critical in biobank-based G × E tests.. Cell genomics . https://doi.org/10.1016/j.xgen.2026.101391
30. Large language models improve transferability of electronic health record-based predictions across countries and coding systems.. NPJ digital medicine 2026. https://doi.org/10.1038/s41746-026-02363-5
31. SurvivEHR: a competing risks, time-to-event foundation model for multiple long-term conditions from primary care electronic health records.  2025. https://doi.org/10.1101/2025.08.04.25332916
32. NOAH: Learning the Full Patient Journey. A Longitudinal Multimodal Time-Aware Model for Representation and Forecasting.  2026. https://arxiv.org/abs/2609.09140
33. Longitudinal alignments and syntheses of multimodal clinical data for personalized medicine with the PULSE framework. Nature Computational Science 2026. https://doi.org/10.1038/s43588-026-01026-5
34. MSGene: a multistate model using genetic risk and the electronic health record applied to lifetime risk of coronary artery disease. Nature Communications 2024. https://doi.org/10.1038/s41467-024-49296-9
35. Using Phecodes for Research with the Electronic Health Record: From PheWAS to PheRS. Annual Review of Biomedical Data Science 2021. https://doi.org/10.1146/annurev-biodatasci-122320-112352
36. A unidirectional mapping of ICD-8 to ICD-10 codes, for harmonized longitudinal analysis of diseases. European Journal of Epidemiology 2023. https://doi.org/10.1007/s10654-023-01027-y
37. The NHGRI-EBI GWAS Catalog: standards for reusability, sustainability and diversity.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1070
38. EHR-MPC: Inference-Time Control for Sepsis Treatment with Generative Patient Digital Twins. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.08793
39. Trends in large-scale human population cohorts.. Trends in Genetics 2026. https://doi.org/10.1016/j.tig.2026.08.002
40. Subtyping Alzheimer's disease and Parkinson's disease using longitudinal electronic health records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01085-3
41. Deep representation learning for clustering longitudinal survival data from electronic health records.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56625-z
42. MiGHT-EHR: A Multi-task Graph Transformer for Heterogeneous Temporal Electronic Health Records.  2026. https://arxiv.org/abs/2608.06430
43. Rare variant contribution to human disease in 281,104 UK Biobank exomes. Nature 2021. https://doi.org/10.1038/s41586-021-03855-y
44. Systematic single-variant and gene-based association testing of thousands of phenotypes in 394,841 UK Biobank exomes. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100168
45. Exome sequencing and characterization of 49,960 individuals in the UK Biobank. Nature 2020. https://doi.org/10.1038/s41586-020-2853-0
46. Advancing human genetics research and drug discovery through exome sequencing of the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-021-00885-0
47. An atlas of genetic associations in UK Biobank. Nature Genetics 2017. https://doi.org/10.1038/s41588-018-0248-z
48. Pan-UK Biobank GWAS improves discovery, analysis of genetic architecture, and resolution into ancestry-enriched effects. medRxiv 2024. https://doi.org/10.1101/2024.03.13.24303864
49. Global Biobank Meta-analysis Initiative: Powering genetic discovery across human disease. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100192
50. Mono- and biallelic variant effects on disease at biobank scale. Nature 2023. https://doi.org/10.1038/s41586-022-05420-7
51. Functional architecture of rare protein coding variation across 786,871 exomes.  . https://doi.org/10.64898/2026.10.16.26365771
52. Deviations from genetic additivity driven by rare variants at biobank scale.. Nature communications . https://doi.org/10.1038/s41467-026-76151-w
53. Phenome-wide Burden of Copy Number Variation in the UK Biobank.. American Journal of Human Genetics 2019. https://doi.org/10.1016/j.ajhg.2019.07.001
54. Genetic associations with ratios between protein levels detect new pQTLs and reveal protein-protein interactions. bioRxiv 2023. https://doi.org/10.1016/j.xgen.2024.100506
55. Robust cis-by-trans epistasis in the human plasma proteome highlights an ABO-centered interaction network.. American journal of human genetics . https://doi.org/10.1016/j.ajhg.2026.09.003
56. Multi-ancestry MHC-pQTL mapping reveals disease-linked HLA protein networks and shared genetic architecture.  . https://doi.org/10.21203/rs.3.rs-10956233/v1
57. A proteome atlas of structural variation and VNTR effects on complex traits and diseases.  . https://doi.org/10.64898/2026.09.26.26364064
58. Plasma proteome analyses in individuals of European and African ancestry identify cis-pQTLs and models for proteome-wide association studies. Nature Genetics 2022. https://doi.org/10.1038/s41588-022-01051-w
59. Sex differences in the genetic regulation of the human plasma proteome.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59034-4
60. Atlas of plasma NMR biomarkers for health and disease in 118,461 individuals from the UK Biobank. Nature Communications 2023. https://doi.org/10.1038/s41467-023-36231-7
61. MetabHub: an integrative platform for plasma nuclear magnetic resonance metabolomics using mediation analysis, disease prediction, and risk stratification.. Nucleic acids research . https://doi.org/10.1093/nar/gkag1066
62. Components of genetic associations across 2,138 phenotypes in the UK Biobank highlight adipocyte biology. Nature Communications 2019. https://doi.org/10.1038/s41467-019-11953-9
63. Genetics of 35 blood and urine biomarkers in the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-020-00757-z
64. Global biobank analyses provide lessons for computing polygenic risk scores across diverse cohorts. medRxiv 2021. https://doi.org/10.1101/2021.11.18.21266545
65. All of Us diversity and scale yield context-dependent improvements in polygenic prediction.. Nature Genetics 2026. https://doi.org/10.1038/s41588-026-02734-4
66. Population-specific polygenic risk scores for people of Han Chinese ancestry.. Nature 2025. https://doi.org/10.1038/s41586-025-09350-y
67. Polygenic Prediction of Peripheral Artery Disease and Major Adverse Limb Events.. JAMA cardiology 2025. https://doi.org/10.1001/jamacardio.2025.1182
68. A pre-train and fine-tune framework for adaptive boosting of pre-trained polygenic risk scores.. Nature communications . https://doi.org/10.1038/s41467-026-77128-5
69. A family-aware All of Us benchmark for polygenic prediction and genomic machine learning.  . https://doi.org/10.64898/2026.10.22.26366229
70. Genetically supported targets and drug repurposing for brain aging: A systematic study in the UK Biobank.. Science advances 2025. https://doi.org/10.1126/sciadv.adr3757
71. Phenome-wide association studies across large population cohorts support drug target validation. Nature Communications 2018. https://doi.org/10.1038/s41467-018-06540-3
72. Large-scale cross-species proteomics and machine learning identify biomarkers and peripheral therapeutic targets for delirium.  . https://doi.org/10.21203/rs.3.rs-10672346/v1
73. Multi-omics in the All Of Us Research Program expands mapping genetic mechanisms in health and disease.  . https://doi.org/10.64898/2026.10.29.26366507
74. Proteomic Signatures Capture Environmental Exposures Across Diverse Populations.  . https://doi.org/10.64898/2026.10.06.26364311
75. Genome-wide detection of genotype-environment interactions at biobank scale with fastGxE.. Nature genetics . https://doi.org/10.1038/s41588-026-02809-2
76. SPA<sub>GRM</sub>: effectively controlling for sample relatedness in large-scale genome-wide association studies of longitudinal traits.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56669-1
77. Imputation of fluid intelligence scores reduces ascertainment bias and increases power for analyses of common and rare variants.. Nature genetics . https://doi.org/10.1038/s41588-026-02787-5
78. Integrated multiomic scores for cardiovascular disease prediction across multiancestral populations.  . https://doi.org/10.64898/2026.10.23.26366372
79. Multimodal mediators connecting APOE4 to dementia.  . https://doi.org/10.21203/rs.3.rs-11445203/v1
80. Phenome-wide and proteomic analysis of APOE alleles across different ancestries in the All of Us Research Program.  . https://doi.org/10.64898/2026.09.26.26364080
81. Comparative analysis of the Mexico City Prospective Study and the UK Biobank identifies ancestry-specific effects on clonal hematopoiesis.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02085-6
82. EHRAgent: Code Empowers Large Language Models for Few-shot Complex Tabular Reasoning on Electronic Health Records.. Proceedings of the Conference on Empirical Methods in Natural Language Processing. Conference on Empirical Methods in Natural Language Processing 2024. https://doi.org/10.18653/v1/2024.emnlp-main.1245
83. Longitudinal dynamics of gene expression and metabolomics in an aging population cohort.. Science 2026. https://doi.org/10.1126/science.aed6452
84. Age Acceleration and Mortality Risk Constitute Distinct Dimensions of Organ Aging.  . https://doi.org/10.21203/rs.3.rs-10881849/v1
85. Reversal of proteomic aging with exercise-results from the UK biobank and a 12-week intervention study.. npj aging 2025. https://doi.org/10.1038/s41514-025-00318-w
86. ClinicalAge, a framework for modelling ageing trajectories from longitudinal electronic health records in the UK: a model development and validation study.. The Lancet. Digital health . https://doi.org/10.1016/j.landig.2026.101060
87. Molecular Circadian Disturbance in Human Blood Independently Predicts Multi-Disease Risk and Maps to Hepatic metabolism Pathways.  . https://doi.org/10.21203/rs.3.rs-11120748/v1
88. UK Biobank-A Unique Resource for Discovery and Translation Research on Genetics and Neurologic Disease.. Neurology. Genetics 2025. https://doi.org/10.1212/nxg.0000000000200226
89. Robust replication of associations across patient-mediated and provider-sourced EHR data in the All of Us research program. npj Digital Public Health 2026. https://doi.org/10.1038/s44482-026-00032-8
90. Lessons from national biobank projects utilizing whole-genome sequencing for population-scale genomics.. Genomics & informatics 2025. https://doi.org/10.1186/s44342-025-00040-9
91. A national-scale digital atlas of recorded care patterns across more than 1000 diagnostic categories using real-world health data: a retrospective observational study.  . https://doi.org/10.64898/2026.09.16.26363186
92. UK Biobank release and systematic evaluation of optimised polygenic risk scores for 53 diseases and quantitative traits. medRxiv 2022. https://doi.org/10.1101/2022.06.16.22276246
93. Software Application Profile: PHESANT: a tool for performing automated phenome scans in UK Biobank. International Journal of Epidemiology 2017. https://doi.org/10.1093/ije/dyx204
94. Exploring and visualizing large-scale genetic associations using PheWeb. Nature Genetics 2020. https://doi.org/10.1038/s41588-020-0622-5
95. Quality control and removal of technical variation of NMR metabolic biomarker data in ~120,000 UK Biobank participants. Scientific Data 2021. https://doi.org/10.1038/s41597-023-01949-y
96. Pan-UK Biobank genome-wide association analyses enhance discovery and resolution of ancestry-enriched effects.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02335-7
97. Dynamic Importance of Genomic and Clinical Risk for Coronary Artery Disease Over the Life Course. medRxiv 2023. https://doi.org/10.1101/2023.11.03.23298055
98. Machine Learning‐Driven Prediction of Coronary Artery Disease Risk Based on UK Biobank Plasma Proteomics. Journal of the American Heart Association : Cardiovascular and Cerebrovascular Disease 2026. https://doi.org/10.1161/JAHA.125.047248
99. UKB-MDRMF: a multi-disease risk and multimorbidity framework based on UK biobank data.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58724-3
100. PheMIME: an interactive web app and knowledge base for phenome-wide, multi-institutional multimorbidity analysis.. Journal of the American Medical Informatics Association : JAMIA 2024. https://doi.org/10.1093/jamia/ocae182
101. Plasma metabolites to profile pathways in noncommunicable disease multimorbidity. Nature Medicine 2021. https://doi.org/10.1038/s41591-021-01266-0
102. MetaboHealth and Metabolic Vulnerability Index as Risk Factors for Cardio-Renal-Metabolic Multimorbidity: A Large-Scale Prospective Cohort Study.. Diabetes, obesity and metabolism 2026. https://doi.org/10.1111/dom.71112
103. NMR metabolomics for cardiovascular-kidney-metabolic risk stratification in an integrated healthcare system.  . https://doi.org/10.64898/2026.10.01.26364322
104. Proteomics mediates the effects of biological aging on the progression of cardio-renal-metabolic comorbidity: a UK biobank cohort study.. Cardiovascular diabetology 2025. https://doi.org/10.1186/s12933-025-03035-6
105. A deep learning algorithm to predict risk of pancreatic cancer from disease trajectories. Nature Medicine 2023. https://doi.org/10.1038/s41591-023-02332-5
106. Deep phenotyping of heart failure with preserved ejection fraction through multi-omics integration.. European journal of heart failure 2025. https://doi.org/10.1002/ejhf.70041
107. Explainable Plasma Proteomics–Based Machine Learning for Osteoporosis Diagnosis, Prognosis, and Protein Biomarker Discovery in the UK Biobank. The FASEB Journal 2026. https://doi.org/10.1096/fj.202600647R
108. Large-scale plasma proteomic profiling enhances prediction of heart failure among hypertensive individuals: prospective insights from the UK Biobank.. Journal of global health . https://doi.org/10.7189/jogh.16.04313
109. Generalizability of proteomic risk prediction across biobanks reveals dependence on phenotype definitions.  . https://doi.org/10.64898/2026.10.01.26364038
110. Sex shapes plasma molecular signatures of dementia risk across APOE ε4 strata.  . https://doi.org/10.64898/2026.11.02.26366836
111. Leveraging large-scale biobank EHRs to enhance pharmacogenetics of cardiometabolic disease medications.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58152-3
112. Bayesian Cox regression for large-scale inference with applications to electronic health records. Annals of Applied Statistics 2021. https://doi.org/10.1214/22-aoas1658
113. From data to knowledge: artificial intelligence methods for studying comorbidity in electronic health records. The European Physical Journal Special Topics 2026. https://doi.org/10.1140/epjs/s11734-026-02571-w
114. Mixed model association for biobank-scale data sets. Nature Genetics 2018. https://doi.org/10.1038/s41588-018-0144-6
115. Exome sequencing and analysis of 454,787 UK Biobank participants. Nature 2021. https://doi.org/10.1038/s41586-021-04103-z
116. Disease prediction with multi-omics and biomarkers empowers case–control genetic discoveries in the UK Biobank. Nature Genetics 2024. https://doi.org/10.1038/s41588-024-01898-1
117. An atlas of polygenic risk score associations to highlight putative causal relationships across the human phenome. bioRxiv 2018. https://doi.org/10.7554/eLife.43657
118. A fast and scalable framework for large-scale and ultrahigh-dimensional sparse regression with application to the UK Biobank. bioRxiv 2019. https://doi.org/10.1371/journal.pgen.1009141
119. GWAS of extended prescription analgesic use identifies genetic loci in chronic pain.. Nature communications 2026. https://doi.org/10.1038/s41467-026-71434-8
120. fastGxE is a powerful method for uncovering genotype-environment interactions in biobanks.. Nature genetics . https://doi.org/10.1038/s41588-026-02806-5
121. Biobank-scale self-supervised genotype pretraining yields transferable representations for human genetics.. Nucleic acids research . https://doi.org/10.1093/nar/gkag1059
