# 类器官与模式生物虚拟响应建模 · 方向背景报告

证据 64 篇 · 覆盖度 0.47 · 第 5 轮 · 更新 2026-09-27

## 本次变更

- 新增 [49] A lifespan single-cell atlas of the human developing hippocampus benchmarks familial Alzheimer's disease brain organoids.
- 新增 [24] Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling

## 摘要（TL;DR）

- 类器官扰动建模正从单一标记读出转向多维读出（regulon活性、因果配对、空间邻域、PTM/凋亡），但读出维度越高，通量与标准化越受限 [1][2][3][4]
- OSCAR在3D类器官中以调控网络为读出，鉴定出c-Fos扰动加速肝细胞分化成熟、Ubr5缺失起相反作用，但受单细胞噪声与dropout限制 [1]
- 类器官CRISPR筛选已扩展到基因-药物互作与多模态体系，如胃肿瘤类器官中揭示DNA修复通路趋同与蛋白岩藻糖化关联顺铂敏感性 [5]
- Perturb-FISH将CRISPR筛选与空间转录组联合，揭示细胞密度与邻居扰动对基因回路的影响，但gRNA仅20bp难以tiling、3D组织应用仍有限 [3]
- 药敏预测正从终点活力走向动态、组合与微环境感知，切片培养可在24小时内完成GBM药敏筛选并保留肿瘤微环境，但仅7例、短期培养 [6]
- Trellis分析>2500个CRC PDO与CAF发现凋亡罕见且患者特异，CAF促proCSC向revCSC转变以耐药，但预印本版本无全文、数据规模未提供 [4][7]
- 图像与深度学习已能预测类器官凋亡强度（与真值相关0.91）和早期组织结局，但各方法基准不统一（真值相关、ATP金标准、表型分组） [8][9][10][11]
- AI驱动扰动建模在预测目标上分化明显（全基因组扰动响应、多步扰动策略、药物重定位、靶向治疗响应），但多数预测仍停留在计算验证或有限实验验证阶段 [12][13][14][15]
- 患者来源类器官临床预测证据强度不一：直肠癌PDO预测准确率84.43%、灵敏度78.01%、特异性91.97%，但受单一临床试验来源限制，且正常细胞过度生长与克隆性漂移可能削弱保真度 [16][17]
- 跨物种迁移方法从显式对齐（CellOT、CAME）演进到通用嵌入与生成建模（SATURN、UCE、GeneCompass、Nicheformer、Speciesformer），但保守与特异变异的区分至今尚无系统性定量答案 [18][19][20][21][22][23][24]
- 类器官数字孪生（AIVOs）提出数据层-模型层-交互层三层结构与可复用基元，但Matrigel依赖、批次差异与终点测量使全链条可重复性仍受制于湿实验端标准化程度 [25]

## 1 背景与定义

在类器官与模式生物虚拟响应建模的边界划定上，**该方向的核心不是类器官构建或培养方案本身，而是以扰动为自变量、以组织/器官/个体层面响应为因变量的可预测建模**[25]。AIVOs框架把这一边界明确表述为数据层-模型层-交互层的三层结构：数据层整合多模态组学、高内涵成像与空间profiling，模型层以虚拟干细胞、功能细胞与肿瘤细胞为可复用基元连接单细胞表征与类器官乃至患者尺度模拟，交互层则要求计算模型与物理类器官及临床决策形成闭环[25]。这意味着方向的外延同时覆盖类器官/器官芯片上的扰动筛选、模式生物的多器官单细胞图谱与剂量/时间响应、跨物种迁移方法，以及类器官药敏与患者结局对应；而纯构建、纯培养、纯细胞系扰动预测与单一基因敲除的常规表型描述则被排除在外。**边界的关键判据是"是否有扰动与建模成分"，而非体系本身是3D还是体内**[25]。

从演化脉络看，该方向经历了从"终点活力测定"到"多模态扰动读出"、从"单物种单体系"到"跨物种基础模型"的两条并行迁移。早期类器官药敏以终点ATP或活力为读出，直肠癌PDO与III期临床试验对比达到**预测准确率84.43%、灵敏度78.01%、特异性91.97%**，确立了PDO作为伴随诊断工具的临床效度基线[16]；但这一代工作的读出维度单一，难以区分细胞毒、细胞静止与延迟响应。随后扰动读出向调控网络、空间邻域、钙活动与PTM扩展：OSCAR以regulon活性为读出在3D类器官中鉴定c-Fos加速肝细胞分化成熟、Ubr5缺失起相反作用[1]；Perturb-FISH把CRISPR筛选与MERFISH空间转录组联合，在THP1巨噬细胞中揭示细胞密度与邻居扰动对基因回路的影响[3]；Trellis在单细胞水平检测>2500个CRC PDO与CAF的PTM信号，发现凋亡罕见且患者特异、CAF促proCSC向revCSC转变以耐药[4]。**读出维度越高，通量与标准化越受限**，这解释了为何胃类器官全套CRISPR筛选仍强调3D技术难度[5]，而单细胞来源STO阵列虽能识别耐药亚群，通量与标准化仍受限[26]。

第二条演化脉络是跨物种迁移从显式对齐走向通用嵌入与生成建模。CellOT用输入凸神经网络参数化对偶势，从非时间分辨的未配对单细胞数据学习扰动响应映射，在跨物种LPS响应等任务上优于线性潜空间位移类方法，但其前提是训练队列需覆盖足够大的生物学变异谱[18]。CAME则用半监督异构图神经网络把参考与查询物种的表达矩阵及同源基因映射编码为异质细胞-基因图，支持一对多与多对多同源映射，但性能受同源基因映射质量制约[19]。**两者对"跨物种"给出了不同前提：CellOT要求扰动数据，CAME要求同源注释**。此后SATURN以蛋白语言模型嵌入耦合基因表达、引入宏基因概念，在哺乳动物335,000细胞图谱及蛙/斑马鱼胚胎数据上实现跨物种注释迁移[20]；UCE完全自监督构建含3600万细胞、1000+细胞类型、8物种的统一潜空间[21]；LucaCell用预训练mRNA序列嵌入替代固定基因ID，在8500万人鼠单细胞上预训练，实现无手动映射的跨物种注释并预测流感病毒载量[27]。**这一脉络的共同趋势是用序列或蛋白语义重建基因表示，以绕开基因ID不可通约问题，但各自的先验依赖不同**[20][21][27]。

第三条脉络是知识注入与空间维度的扩展，把跨物种建模从"细胞类型对齐"推进到"空间组织与调控机制对齐"。GeneCompass在scCompass-126M的1.017亿人鼠单细胞上预训练，整合启动子、GRN、基因家族与共表达四类先验知识，微调后在扰动预测、剂量响应与GRN推断等任务达到或接近SOTA[22]；mouse-Geneformer则用1089个数据集、过滤前1.19亿细胞构建mouse-Genecorpus-20M，评估细胞类型分类与in silico扰动效用，但仅用健康野生型小鼠数据，跨物种应用需进一步验证[28]。**前者靠先验知识注入，后者靠数据规模与架构迁移，物种覆盖与同质性取舍相反**。Nicheformer构建SpatialCorpus-110M，涵盖超1.1亿细胞、5383万空间细胞、73组织，通过模态、物种和检测平台token学习联合表征，在空间依赖任务上系统性优于Geneformer、scGPT、UCE、CellPLM[23]；BrainBeacon基于1.33亿空间分辨细胞、四物种五平台数据，实现跨物种脑细胞类型与解剖区域对齐并揭示衰老空间调控机制[29]。**空间维度的加入使跨物种迁移从"哪些细胞类型保守"扩展到"哪些空间组织原则保守"，但两项工作的独立基准复现与全文可及性仍存疑**[23][29]。

第四条脉络是类器官药敏与患者结局对应，其证据强度呈现明显的分层。直肠癌PDO以84.43%准确率匹配化放疗反应，是少数与前瞻性临床试验直接对比的工作[16]；胃癌PDO生物库通过73例组织构建57个类器官，结合RNA-seq、药敏、PDOX与患者实际治疗反应验证，提示高增殖类器官富集干性与增殖相关基因[30]；卵巢癌PDO对36个样本进行全基因组特征分析与药筛，88%患者可找到有效药物，但长期药敏稳定性仍需验证[31]。**这些工作的共同边界是：类器官可重现患者间与患者内异质性，但培养中的正常细胞过度生长与克隆性漂移可能削弱预测保真度**[17]。系统综述17项研究后指出，PDO有潜力预测治疗反应，但需满足分析效度、临床效度和临床效用，建立率与周转时间仍影响临床落地[32]。**因此，类器官药敏的"预测"目前更多是回顾性对应而非前瞻性决策验证，这是该方向与临床转化之间的核心缺口**[32][16]。

把上述脉络并置，该方向当前的核心问题可归纳为三个尚未收敛的张力。其一是**扰动读出维度与通量的张力**：regulon活性[1]、因果细胞配对[2]、空间邻域与钙活动[3]、单细胞PTM与凋亡[4]各自捕捉不同层面的响应，但尚无统一基准能同时评估这些读出。其二是**微环境保真度与可扩展性的张力**：急性切片培养保留肿瘤微环境与异质性但仅24小时[6]，自动化微流控平台支持长期培养与动态组合刺激但系统复杂[33]，Trellis揭示CAF可保护癌细胞抵抗化疗[4]，而多数PDO药敏仍以单细胞类型为主[16][17]。其三是**预测与验证的张力**：脑类器官扰动信息基础模型排序出343个自闭症候选基因、其中167个在关键簇中[12]，DiRL对随机扰动胜率69%[13]，Leigh研究用酵母与类器官双筛选识别唑类化合物[14]，多组学嵌入识别KRAS抑制剂敏感邻域[15]，但多数工作未报告前瞻性临床验证。**这些张力共同定义了方向的方法学前沿：不是缺少扰动工具，而是缺少能在同一体系中同时满足通量、空间分辨率、微环境保真度与临床可验证性的整合框架**[25]。

最后需要指出，该方向的数据资源与评测体系本身正在成为独立的研究对象。Stereo-seq在多种人源类器官中优化芯片包被与通透条件，实现单芯片多样本空间全转录组，但小类器官捕获偏低、单细胞注释困难[34][35]；皮层脑类器官多重化策略开发SCanSNP去卷积进行基因型识别，在50/100/300天纵向采样中重建神经发育轨迹，但成本与批次间变异仍限制其系统应用[36]。在基础模型评测方面，统一基准测试六个代表性单细胞与空间基础模型后发现**模型性能高度条件依赖，无模型全面占优，排名随多种因素变化**[37]；而通用表格基础模型TabICL与TabPFN在五个Perturb-seq数据集、CD4+ T全基因组CRISPR筛选及斑马鱼图谱上，于细胞水平持平或更优、伪bulk扰动预测持续优于专用基线、胚胎组成预测具竞争力[38]。**这两项评测共同指向一个判断：该方向尚未形成稳定的模型选择共识，任务尺度与数据形态决定通用与专用方法的相对优势，二者更接近互补而非替代**[37][38]。跨物种细胞景观研究用Microwell-seq分析小鼠、斑马鱼和果蝇超260万细胞并整合15物种，发现结构炎症与线粒体功能障碍为常见衰老标志[39]；Speciesformer在1.31亿细胞的SpeciesCorpus上预训练，明确把"区分保守原理与物种、组织及细胞环境特异变异"列为待解挑战[24]。**这一挑战实际上是对前述所有跨物种工作的共同拷问：宏基因、通用嵌入、知识注入、空间token究竟捕捉的是保守生物学还是物种特异的统计规律，目前尚无任何一项证据给出系统性定量答案**[24]。

## 2 方法学


### 2.1 类器官与器官芯片扰动建模

类器官扰动建模的第一条主线，是把CRISPR扰动从2D细胞系搬进3D组织结构，并以调控网络而非单一标记基因作为读出。**OSCAR**在3D类器官中以调控网络变化为读出进行单细胞CRISPR筛选，应用于小鼠与人ICO类器官的肝细胞分化成熟，鉴定出**c-Fos扰动加速肝细胞分化成熟**，而**Ubr5缺失起相反作用**，并按调控效应排序[1]。该工作的方法学意义在于把scCRISPR的读出从“基因表达变化”提升到“regulon活性变化”，但作者也指出单细胞噪声与dropout会影响低丰度转录本估计，且结论依赖regulon活性读出[1]。与之形成对照的是CINEMA-OT，它不依赖调控网络读出，而是用独立成分分析与加权最优传输实现因果细胞配对，在气道类器官病毒感染/烟雾及PBMC细胞因子组合刺激数据中优于现有方法[2]。两者都试图解决“扰动效应估计”这一子问题，但OSCAR以生物学调控结构为中介，CINEMA-OT以统计因果配对为中介，其假设（独立性与线性）可能成为潜在混杂因素影响估计的来源[2]。

第二条主线是类器官CRISPR筛选从“单基因扰动”扩展到“基因-药物互作”与“多模态筛选体系”。人胃肿瘤类器官（TP53/APC DKO）中建立了切割、CRISPRi、CRISPRa与单细胞筛选的全套体系，用于顺铂基因-药物互作筛选，鉴定出顺铂敏感性相关基因，揭示**DNA修复通路转录组趋同**，并发现**蛋白岩藻糖化与顺铂敏感性关联**及TAF6L在DNA损伤恢复期增殖中的作用[5]。该研究以2D细胞系CRISPR筛选为基准，但其局限在于基于单一工程化类器官模型，且3D类器官筛选技术难度较高[5]。在宫颈鳞癌中，单细胞分析引导的类器官CRISPR筛选把**NF1鉴定为恶性转化首要抑制因子**，其缺失将**5~10年癌变压缩至3~6个月**，NF1恢复诱导凋亡，AI设计的NF1模拟肽可降低肿瘤负荷[40]。该工作整合了患者样本单细胞转录组、HPV阳性前瘤类器官与HPV16小鼠模型，但全文未获取，局限未明确[40]。值得注意的是，Perturb-FISH把CRISPR筛选与空间转录组联合起来，用MERFISH结合gRNA原位扩增，在THP1巨噬细胞LPS响应体系中验证KO效应与Perturb-seq一致，并揭示细胞密度和邻居扰动对基因回路的影响，还记录了ASD风险基因KD对钙活动与表达的影响[3]。其技术限制在于gRNA仅20bp难以像mRNA一样tiling，需原位扩增，3D组织应用仍有限[3]。与前述胃类器官筛选相比，Perturb-FISH的读出维度从“基因必要性”扩展到“空间邻域依赖的扰动效应”，但两者都尚未解决3D组织中扰动通量与空间分辨率的根本张力[5][3]。

第三条主线是类器官药敏预测从“终点活力测定”走向“动态、组合与微环境感知”。自动化微流控平台兼容Matrigel，支持长期培养、动态程序化刺激与实时监测，降低试剂与人工消耗，其基准是传统2D培养、PDX及现有微流控/器官芯片[33]。但该系统复杂性与通量仍受凝胶和微流控限制[33]。单细胞来源肿瘤类器官（STO）阵列在微流控芯片上实现数千STO同焦面培养，识别耐药STO及差异表达基因，候选药再验证有效，其对照是多细胞来源类器官MTO[26]。该工作针对异质性耐药，但通量与标准化仍受限，单细胞来源代表性需更多临床验证[26]。在组织层面，急性切片培养结合microwell scRNA-seq去卷积，从7例GBM手术标本制备500μm切片，在**24小时内完成药敏筛选**，去卷积细胞类型特异药物反应，保留肿瘤微环境与异质性[6]。其局限是样本量7例、短期培养24小时，可能无法完全反映长期治疗反应[6]。Trellis树基分析则在单细胞水平检测**>2500个CRC PDO与CAF**的PTM信号、DNA损伤、细胞周期和凋亡，发现靶向细胞周期阻断和DNA损伤常见，但**凋亡罕见且患者特异**，CAF促proCSC向revCSC转变以耐药[4]。其预印本版本核心方法与Cell论文一致，但无全文，具体数据规模、基准和定量结果未提供[7]。这些工作在“是否保留微环境”上形成分歧：微流控平台强调可控灌注与组合刺激[33]，切片培养强调原位微环境[6]，而Trellis强调基质细胞对耐药的可塑性调控[4]。

第四条主线是图像与深度学习对类器官形态、功能与发育结局的预测。结直肠癌类器官图像profiling分析**31360张明场图**，结合目标检测网络和深度生成模型预测凋亡强度，识别囊性与实性两亚型，囊性活性更高，**凋亡预测与真值相关0.91**[8]。其局限是样本来源与泛化性未充分验证，仅明场与荧光配对数据[8]。视网膜类器官研究采集**988个类器官、117249张明场延时图像**，训练DL模型在RPE与晶状体组织可见出现前很早期准确预测其发生与大小及整体形态相似性，明确组织结局决定时间窗[9]。该工作指出监督深度学习需大量标注高质量数据集，是类器官研究主要限制之一[9]。在药效评估方面，PDO延时显微视频用SAM分割和DI-NOv2模型处理帧，注意力机制融合时空特征预测ATP，结果优于非时间分辨方法，可实时评估单PDO药物反应[10]。其局限是未提及临床验证，依赖ATP金标准[10]。胃癌类器官的AFM纳米机械振动传感则显示**pM级紫杉醇即可检测振动变化**，早于形态改变，CNN分类准确率**97%**[41]。该工作依赖AFM设备，通量有限，临床样本验证规模有限[41]。SCOPE系统整合AI图像分析类器官活力与生长追踪及数学建模，提出**GV评分与CCTR**两个新指标，将药物反应分为细胞毒、细胞静止加细胞毒、延迟细胞毒、细胞静止四类[11]。这些工作共同把“药效”从单一终点扩展为时间-剂量依赖的表型轨迹，但图像方法之间在基准上并不统一：凋亡预测以真值相关为基准[8]，药效分类以ATP为金标准[10]，而SCOPE以表型分组为输出[11]。

第五条主线是类器官的几何、成熟与电生理设计优化。心脏类器官几何设计研究构建**7种几何设计、230个心脏类器官**，采集收缩运动与钙瞬变**10项变量**，结合流形学习、无监督聚类和集成学习，发现AI流程可无偏降低异质性并识别形状决定生理属性[42]。其局限是仅分化第20天、样本量与几何设计有限、未验证长期功能[42]。心脏类器官成熟研究筛选出短暂激活AMPK和ERR的条件，**MK8722+DY131使cTnI显著升高，TNNI3比例达18%（约20周胎儿心脏）**，DM-hCOs可建模复杂疾病并用于药物测试[43]。其基准是与SF-hCO方案及起搏/代谢成熟方案对比，但成年心脏特性仍未完全实现，长期电起搏有毒性[43]。Heart-on-a-Miniscope采用长工作距离微型荧光显微镜，在芯片上以高时空分辨率成像人心脏钙瞬变，**分辨率达228 lp/mm@60帧/秒**，其基准是传统MEA、膜片钳及常规荧光显微镜系统[44]。该设备针对既往微型显微镜因GRIN透镜工作距离近零而不适用于芯片底部成像的问题，但需适配体外芯片应用[44]。这三项工作在“成熟”定义上存在差异：几何优化以功能变量异质性降低为成熟标志[42]，AMPK/ERR激活以转录组、蛋白质组、收缩功能和代谢能力的稳健成熟为标志[43]，而Miniscope以电生理读出能力为标志[44]。

第六条主线是空间转录组与多重化策略在类器官中的应用。Stereo-seq在脑、心、肾、肺、软骨、造血等类器官中优化芯片包被与通透条件，实现单芯片多样本类器官空间转录组，评估RNA捕获效率与局限，提出区域分区分析方法，基准是E13.5小鼠头与21 PCW小鼠心脏参考组织[35]。其局限是小类器官捕获偏低，单细胞分辨率与细胞注释困难[35]。另一项Stereo-seq研究分析**8种人源类器官、10张芯片**，优化poly-L-赖氨酸包被与通透，评估UMI/基因捕获，保留5种类器官分析，4种用于区域分析，基准同样是E13.5小鼠头与21 PCW小鼠心脏组织[34]。该研究指出造血与悬浮肾类器官转录扩散，单细胞注释困难[34]。两项工作高度相似，但一项以bioRxiv预印本形式报告[35]，另一项以iScience正式发表[34]，后者在类器官种类与芯片数量上更明确，提示该基准数据集经历了从预印本到正式发表的迭代。在多重化方面，皮层脑类器官研究比较了类器官生成时混合细胞系的mosaic策略与单细胞建库前混合的下游策略，开发**SCanSNP去卷积**方法进行基因型识别，在50/100/300天纵向采样中重建神经发育轨迹并关联遗传变异与发育轨迹表型[36]。其局限是成本与工作量大、批次间变异，尚未系统应用于类器官[36]。形态发生素 patterning 研究则用多重单细胞转录组筛选结合微流控浓度梯度与多孔板静态浓度，发现形态发生素时序、浓度与组合显著决定区域组成，且细胞系和诱导方法影响响应[45]。该工作缺乏全文，未明确公开资源与验证范围[45]。这些空间与多重化工作共同指向一个方法学瓶颈：类器官的空间转录组捕获效率与单细胞注释仍受组织大小和类型限制[35][34]，而多重化策略虽能提高通量，却引入批次间变异与去卷积不确定性[36]。

第七条主线是AI驱动的扰动建模与药物发现，其核心是把类器官图谱或表型数据转化为可预测的扰动响应空间。脑类器官扰动信息基础模型构建了**360万细胞类器官图谱**，基准测试**17个模型**，发现端脑神经元特异性模型最佳保留自闭症相关扰动结构，整合预测扰动效应与基因组证据优先排序出**343个自闭症候选基因**，其中**167个在关键簇中**，NBEA和KLHDC10有复现证据[12]。该工作整合了**89,916个家庭样本**，但预测扰动效应需进一步实验验证[12]。强化学习框架DiRL把分化建模为目标条件序列决策问题，在iPSC来源类器官数据上训练智能体导航基因表达潜空间，对随机扰动**胜率69%**，随规划步长提升，恢复Wnt与Hedgehog通路调控因子，价值函数重现伪时间排序[13]。其局限是依赖基础模型环境建模，真实生物验证有限[13]。Leigh综合征药物发现建立基于Leigh脑类器官scRNAseq的细胞类型特异性深度学习药物重定位算法，并在ΔSHY酵母中筛选**2250种FDA药物**，两种方法独立识别唑类化合物，其中sertaconazole和talarozole可促进Leigh神经细胞神经定向并挽救中脑类器官生长和乳酸释放异常[14]。其局限是依赖已有scRNAseq数据、酵母与人类差异、需进一步临床验证[14]。多组学类器官嵌入研究整合**135个CRC/PDAC PDO**的WES、bulk RNA-seq和药敏数据，生成多模态患者表征并训练机器学习模型预测药物AUC，在嵌入空间中识别KRAS抑制剂敏感或耐药富集的分子邻域[15]。该摘要未提局限，但队列仍有限，需系统验证临床转化价值[15]。这些AI工作在“预测目标”上分化明显：脑类器官模型预测全基因组扰动响应并排序候选基因[12]，DiRL预测多步扰动策略[13]，Leigh研究预测药物重定位[14]，多组学嵌入预测靶向治疗响应[15]。它们共享的争议是：预测结果是否能在真实类器官或临床中复现，目前多数工作仍停留在计算验证或有限实验验证阶段[12][13][14][15]。

第八条主线是患者来源类器官作为临床反应预测工具的证据强度与边界。局部晚期直肠癌PDO活体生物库与III期临床试验对比，**预测准确率84.43%，灵敏度78.01%，特异性91.97%**，证实RCO重现肿瘤病理生理和遗传变化，可作为直肠癌治疗的伴随诊断工具[16]。其局限是样本来源单一临床试验，需更多验证[16]。头颈鳞癌研究开发基于Hover-Net架构与ResNet50骨干的单细胞CNN分类器**TransferNet-PDO**，结合H&E图像与全外显子测序分析PDO形态、基因组与克隆结构，对顺铂、西妥昔单抗、仑伐替尼、放疗及放化疗显示临床相关敏感性[17]。其基准是传统病理AI工具（多基于原发人体组织训练），代码与模型均公开，但HNSCC PDO模型仍相对不成熟，正常上皮或基质细胞过度生长，肿瘤异质性与克隆性难以跨传代保持，新鲜手术标本获取受限[17]。这两项工作在“预测什么”上不同：直肠癌PDO预测化放疗反应[16]，HNSCC PDO预测多种药物与放疗敏感性并保留克隆结构[17]。共同争议是类器官培养中的正常细胞过度生长与克隆性漂移可能削弱预测保真度[17]，而直肠癌研究的单一临床试验来源也限制了外推[16]。

把上述主线并置，可以看到类器官扰动建模的三个核心张力。其一是**扰动读出维度**的张力：OSCAR以regulon活性为读出[1]，CINEMA-OT以因果细胞配对为读出[2]，Perturb-FISH以空间邻域与钙活动为读出[3]，Trellis以单细胞PTM与凋亡为读出[4]。读出维度越高，通量与标准化越受限，这解释了为何胃类器官筛选仍强调3D技术难度[5]，而STO阵列强调通量与标准化仍受限[26]。其二是**微环境保真度**的张力：切片培养保留肿瘤微环境与异质性但仅24小时[6]，微流控平台支持长期培养与动态刺激但系统复杂[33]，Trellis揭示CAF可保护癌细胞抵抗化疗[4]，而多数PDO药敏研究仍以单细胞类型为主[16][17]。其三是**预测与验证**的张力：AI模型在脑类器官中排序出343个候选基因[12]，DiRL对随机扰动胜率69%[13]，Leigh研究用酵母与类器官双筛选识别唑类化合物[14]，多组学嵌入识别KRAS抑制剂敏感邻域[15]，但这些预测的实验与临床验证程度差异很大，且多数工作未报告前瞻性临床验证[12][13][14][15]。这些张力共同定义了类器官与器官芯片扰动建模当前的方法学前沿：不是缺少扰动工具，而是缺少能在同一体系中同时满足通量、空间分辨率、微环境保真度与临床可验证性的整合框架。

### 2.2 模式生物扰动响应模型

在模式生物扰动响应建模的方法谱系中，一条主线是评估通用表格基础模型能否替代为特定扰动任务定制的专用模型。该工作将 **TabICL** 与 **TabPFN** 同 PRESAGE、scGPT、scLAMBDA、STACK、Prophet 等专用基线在四个互补评估设置中对比，数据覆盖五个 Perturb-seq 数据集、CD4+ T 全基因组 CRISPR 筛选以及斑马鱼图谱 [38]。结果显示，表格基础模型在细胞水平跨类型预测中持平或更优，在伪 bulk 扰动预测中持续优于专用基线，在胚胎组成预测中亦具竞争力 [38]。这一结论对"扰动响应必须依赖领域专用架构"的默认假设构成挑战，但作者也明确指出评估未覆盖所有生物尺度，专用模型在部分任务上仍可能更优 [38]。因此，该证据支持的并非通用模型全面胜出，而是任务尺度与数据形态决定了通用与专用方法之间的相对优势，二者关系更接近互补而非替代。

另一条主线把跨物种单细胞图谱与扰动/疾病轨迹的预测建模直接耦合，但在疾病与发育两个方向上呈现出不同的成熟度。在动脉粥样硬化方向，研究整合人晚期稳定与不稳定斑块单细胞数据及多时间点小鼠模型，重建跨物种多阶段连续轨迹，鉴定出富集于不稳定病变的 **PIM 单核细胞群**，并由此衍生 **362 基因血液特征**，再用可解释深度学习筛选出 20 基因 panel 以区分不稳定与稳定病例 [46]。该工作把模式生物时间序列与人类病变样本对齐，试图将细胞群发现转化为可用于急性冠脉事件预测的血液标志物，但其 AUC 数值不完整、临床验证规模未明，预测性能的可复现性仍待确认 [46]。在小脑皮层方向，研究构建猕猴、狨猴与小鼠的单细胞空间转录组图谱，发现灵长类特异 Purkinje 细胞和分子层中间神经元亚型、**GRID2** 表达差异，以及区域选择性表达在灵长类主要位于颗粒层、在小鼠位于 Purkinje 层的物种分歧，并进一步显示基因表达梯度与清醒 fMRI 功能连接梯度相匹配 [47]。与前者直接输出预测标志物不同，后者提供的是跨物种细胞类型与空间组织的对应关系，其功能验证深度与数据公开性尚未明确 [47]。两项工作共同表明，跨物种建模的价值既可能体现为临床预测特征，也可能体现为进化层面的组织原则，但前者受限于验证不完整，后者受限于功能因果证据不足，二者在"预测"与"解释"之间的定位差异，正是该方向尚未收敛的争议所在。

### 2.3 跨物种迁移

跨物种迁移在单细胞扰动响应建模中的第一条技术路线，是以最优传输为核心显式学习控制态与扰动态之间的映射。CellOT 用输入凸神经网络参数化对偶势，从非时间分辨的未配对单细胞数据中学习扰动响应映射，在黑色素瘤药物响应、狼疮与胶质瘤患者活检、跨物种 LPS 响应及造血命运演化任务上均优于当时的线性潜空间位移类 SOTA 方法 [18]。这一工作的关键贡献在于把"跨物种"作为检验泛化能力的场景之一：LPS 刺激在不同物种间具有相对保守的免疫响应结构，因此适合考察模型是否学到了可迁移的响应机制而非队列特异的伪影。但 CellOT 的局限同样明显——它依赖未配对数据假设，且必须捕获训练队列的异质性才能泛化到新患者 [18]。这意味着跨物种迁移的成败在很大程度上取决于训练数据是否覆盖了足够大的生物学变异谱，而非仅仅取决于映射函数本身的容量。与之形成方法学对照的是 CAME，它不学习扰动映射，而是用半监督异构图神经网络把参考物种与查询物种的表达矩阵及同源基因映射编码为异质细胞-基因图，并加入种内 KNN 细胞-细胞边，从而学习对齐且可解释的细胞与基因嵌入 [19]。CAME 的价值在于支持一对多与多对多的同源映射，突破了简单一对一同源假设，但其性能仍受同源基因映射质量制约，跨物种转录组差异与测序深度不一致依旧影响整合效果 [19]。两者对比可见一个核心分歧：CellOT 把跨物种迁移视为响应函数的泛化问题，CAME 则视为表征对齐问题；前者要求扰动数据，后者要求同源注释，二者对先验知识的依赖方向不同。

第二条路线转向以基础模型构建通用细胞嵌入，试图用大规模预训练替代逐任务的显式对齐。SATURN 通过耦合基因表达与大型蛋白语言模型嵌入实现跨物种 scRNA-seq 整合，引入"宏基因"概念，将功能相关基因按蛋白嵌入相似性分组并映射到联合低维空间，在哺乳动物 **335,000 细胞、9 组织**图谱以及蛙与斑马鱼胚胎数据上实现了跨物种注释迁移，性能优于基于序列相似性或一对一同源的现有整合方法 [20]。SATURN 的方法论要点是用蛋白语言模型嵌入作为跨物种的"公共语言"，从而绕开基因 ID 不可通约的问题；但其局限也正源于此——整合质量依赖蛋白语言模型嵌入质量，宏基因的可解释性受初始注释影响 [20]。UCE 走得更远，完全自监督地在无标注细胞图谱上训练，构建统一生物潜空间，新细胞无需再训练或微调即可映射，并构建了含 **3600 万细胞、1000+ 细胞类型、8 物种**的 Integrated Mega-scale Atlas [21]。UCE 的"零样本"主张与 SATURN 的"嵌入耦合"形成对照：前者强调无需微调的通用性，后者强调蛋白语义带来的可解释分组。但 UCE 的全文未获取，其局限未明确 [21]，因此对其跨物种迁移能力的判断应保持谨慎。LucaCell 则从另一个角度切入，指出固定基因 ID 是跨物种的根本障碍，转而用预训练 mRNA 序列嵌入表示基因，将表达离散分箱后用 Transformer 编码，在 **8500 万人鼠单细胞**上预训练，实现无手动映射的跨物种注释、区分细菌种与生理状态、改善表达重建并预测流感病毒载量 [27]。LucaCell 把跨物种迁移扩展到 50+ 原核与 5 株流感，其野心超出真核细胞注释；但它依赖预训练 mRNA 序列嵌入，且未覆盖所有物种与数据模态 [27]。这三项工作共同指向一个趋势：跨物种迁移正从"对齐已有基因"转向"用序列或蛋白语义重建基因表示"，但各自的先验依赖不同——SATURN 依赖蛋白语言模型，UCE 依赖无标注图谱规模，LucaCell 依赖 mRNA 序列嵌入。

第三条路线是知识注入与空间维度的扩展。GeneCompass 在 **scCompass-126M 的 1.017 亿人鼠单细胞**上预训练，整合启动子、GRN、基因家族和共表达四类先验知识，微调后在细胞注释、扰动预测、剂量响应和 GRN 推断等任务达到或接近 SOTA，预训练语料超 **1.2 亿细胞** [22]。GeneCompass 的跨物种性主要体现在人鼠之间，其知识注入策略依赖先验质量，且下游任务覆盖有限 [22]。与之相比，mouse-Geneformer 是原始人类 Geneformer 的小鼠版，基于 Transformer 编码器与 Rank Value Encoding，使用 **1089 个数据集、过滤前 1.19 亿细胞**构建 mouse-Genecorpus-20M 进行自监督预训练，评估了细胞类型分类与 in silico 扰动效用，并探索跨物种应用潜力 [28]。mouse-Geneformer 的局限很明确：仅用健康野生型小鼠数据，跨物种应用需进一步验证 [28]。这与 GeneCompass 的知识注入形成方法学对比：前者靠数据规模与架构迁移，后者靠先验知识注入；前者物种覆盖窄但数据同质，后者物种覆盖稍宽但先验依赖强。Nicheformer 则把跨物种迁移推进到空间维度，构建 **SpatialCorpus-110M**，涵盖超 **1.1 亿细胞、5383 万空间细胞、73 组织**，通过模态、物种和检测平台 token 学习联合表征，在空间依赖下游任务上系统性优于 Geneformer、scGPT、UCE、CellPLM 等模型，并能将空间背景迁移至解离 scRNA-seq 数据 [23]。Nicheformer 指出现有单细胞基础模型未考虑空间关系，但其独立基准结果未完全复现 [23]，这一争议提示跨物种空间迁移的评估标准尚不统一。BrainBeacon 进一步聚焦脑空间转录组，基于 **1.33 亿空间分辨细胞、210194 mm²**、人/猕猴/狨猴/小鼠四物种五平台数据，采用两阶段训练整合基因表达排序、空间组织与保守遗传关系，实现跨物种脑细胞类型与解剖区域对齐并揭示衰老空间调控机制 [29]。BrainBeacon 与 Nicheformer 的差异在于前者强调解剖区域对齐与衰老机制，后者强调通用空间表征；但两者全文均未获取或局限未明确 [29][23]，其跨物种结论的可复现性有待检验。

第四条路线以图谱构建和生成式建模直接回答"哪些细胞状态是保守的"。跨物种细胞景观研究用 Microwell-seq 分析小鼠、斑马鱼和果蝇不同生命阶段超 **260 万细胞**，并结合公开数据整合 **15 物种**，发现免疫细胞随发育衰老变化显著，结构炎症与线粒体功能障碍为常见衰老标志，药物激活线粒体代谢可缓解小鼠衰老表型 [39]。这一工作的跨物种价值在于用统一实验平台降低批次效应，但其部分物种与组织覆盖有限，跨物种注释依赖参考数据 [39]。小胶质细胞图谱研究整合 scRNA-seq 与空间转录组数据，分析 **>20 万小胶质细胞**，覆盖人鼠脑多区域、性别、年龄，基准比较 anchor-based 与 deep manifold alignment 整合方法，识别出保守亚型——稳态、干扰素响应、吞噬/激活状态，并发现保守 LAM 状态高表达 **APOE、TREM2、GPNMB** [48]。该研究依赖已有数据二次分析，可能受批次和模态整合限制 [48]，其"保守 LAM 状态"的结论与跨物种细胞景观中"结构炎症为常见衰老标志"在概念上呼应，但两者使用的物种、组织和衰老定义不同，不能直接互证。Speciesformer 则把目标设定为跨物种生成式虚拟细胞建模，针对现有单细胞基础模型多局限于单物种、判别任务或特定生成形式的问题，将进化表征学习与虚拟细胞状态生成结合，在包含 **1.31 亿细胞**的 SpeciesCorpus 上预训练，学习可迁移的细胞状态与状态转变 [24]。Speciesformer 明确提出的挑战是需区分保守原理与物种、组织及细胞环境特异变异 [24]，这实际上是对前述所有工作的共同拷问：SATURN 的宏基因、UCE 的通用嵌入、GeneCompass 的知识注入、Nicheformer 的空间 token，究竟捕捉的是保守生物学还是物种特异的统计规律？综合来看，跨物种迁移的方法谱系呈现出从显式对齐到通用嵌入、从判别注释到生成建模的演进，但证据之间的冲突同样突出：UCE 与 Nicheformer 都宣称优于现有基础模型，却分别因全文未获取和独立基准未复现而使比较难以定论 [21][23]；CellOT 依赖未配对扰动数据，CAME 依赖同源基因映射，二者对"跨物种"的可迁移性给出了不同前提 [18][19]；而 Speciesformer 提出的保守与特异变异区分问题，至今尚无任何一项证据给出系统性定量答案 [24]。

### 2.4 虚拟组织与数字孪生建模

类器官数字孪生的核心挑战在于如何把物理培养体系中的多尺度信息转化为可计算、可复用的虚拟表征。**Artificial Intelligence Virtual Organoids（AIVOs）** 框架的提出正是对这一问题的直接回应：它不再停留于单细胞层面的虚拟细胞建模，而是将虚拟细胞扩展为组织尺度的数字模型，并以**数据层-模型层-交互层**三层结构组织整个建模流程[25]。在数据层，该框架综合多模态组学、高内涵成像与空间profiling等来源，试图覆盖从分子到空间结构的异质性信息；在模型层，它提出虚拟干细胞、功能细胞与肿瘤细胞可作为可复用基元，从而在单细胞表征与类器官乃至患者尺度模拟之间建立可组合的桥梁；在交互层，则强调计算模型需与物理类器官及临床决策形成闭环耦合[25]。这一方法路径的差异在于，它把类器官数字孪生定位为面向药物筛选的动态交互系统，而非静态的形态学复现，其基准对照涵盖传统类器官、AIVC与器官数字孪生三类对象[25]。

不过，该框架的可行性受制于物理类器官本身的固有瓶颈。证据明确指出，类器官培养依赖**Matrigel**、批次差异大、手动操作频繁、测量多为终点式，并伴随伦理成本与可扩展性限制[25]。这意味着数据层所依赖的输入信号在来源上就存在噪声与不可重复性，模型层即便设计了可复用基元，其参数标定仍可能因批次漂移而失效；交互层所设想的闭环耦合，也面临终点测量无法提供连续动态反馈的现实约束[25]。由此产生的争议在于：虚拟组织建模究竟应优先追求与物理类器官的一一对应，还是允许虚拟基元在一定程度上脱离具体培养条件而独立演化？该综述并未给出消解这一张力的方案，而是将Matrigel依赖与批次差异列为限制，暗示数字孪生的保真度上限受制于湿实验端的标准化程度[25]。因此，AIVOs框架的价值更多体现在提出了可复用基元与三层耦合的组织逻辑，而非已经解决了类器官数字孪生从数据到决策的全链条可重复性问题。

## 3 数据资源与基准

在类器官与模式生物虚拟响应建模中，基准资源的构建直接决定了模型能否区分真实的疾病扰动与培养体系自身的噪声。**doi:10.64898/2026.09.18.752796** 所报道的工作正是围绕这一子问题展开：它构建了覆盖人海马发育过程的**连续发育单细胞图谱**，并将其作为基准来评估家族性阿尔茨海默病（fAD）脑类器官 [49]。其方法学要点在于，不是把类器官与成体组织或单一时间点样本直接比对，而是以发育连续体作为参照系，对fAD类器官中的神经发育相关扰动进行校准 [49]。这一设计针对的正是iPSC来源脑类器官的核心难题：区域身份、成熟状态和细胞组成存在异质性，若缺乏统一的发育坐标，突变效应与培养偏差会相互混淆 [49]。因此，该基准的价值不在于提供一个静态的"正常对照"，而在于提供一个可定位发育阶段的动态参照，使fAD突变对早期海马发育的影响能够在统一发育参照下被解读 [49]。

从数据资源与基准的角度看，这项工作也暴露出当前虚拟响应建模的一个结构性张力。一方面，单细胞图谱提供了高分辨率的细胞状态与发育轨迹信息，可作为类器官响应的参照底图 [49]；另一方面，该研究明确将类器官的区域身份、成熟状态和细胞组成异质性列为局限，这意味着即便有连续发育图谱，类器官样本与图谱之间的映射仍可能因批次、分化方案和培养时长而产生偏移 [49]。与那些仅以少数标记基因或单一时间点评估类器官成熟度的做法相比，该工作的方法论差异在于把"发育阶段定位"本身作为基准任务，而非把类器官简单归类为某一种细胞类型 [49]。由此产生的争议点在于：当fAD类器官的扰动信号被映射到发育图谱后，究竟应归因于突变效应，还是应归因于类器官尚未达到相应发育阶段？该研究给出的答案是，只有在统一发育参照下解读，才能避免将成熟度差异误判为疾病表型 [49]。这一立场对后续虚拟响应建模提出了明确要求：基准数据集不仅要覆盖细胞类型多样性，还需覆盖连续的发育时间轴，否则模型在跨样本、跨批次泛化时难以区分"疾病响应"与"发育阶段错配" [49]。

## 4 与临床响应的对应

患者来源类器官在预测临床治疗反应方面的证据，首先来自对模型保真度的系统验证。胰腺癌类器官库的研究对30例患者来源类器官（PDO）进行了全基因组测序、RNA测序和组织学表征，发现PDO能够重现肿瘤的组织学特征与遗传改变，并在76种治疗药物的筛选中揭示了临床尚未利用的敏感性，其中PRMT5抑制剂EZP015556对MTAP阴性及部分阳性肿瘤有效[50]。这一发现的意义在于，类器官不仅复制了已知的临床治疗格局，还暴露了常规诊疗路径之外的可操作靶点。与之呼应，转移性胃肠癌PDO活体生物库的工作同样显示，类器官的分子谱与原始肿瘤高度相似，并能够补充现有方法以定义癌症治疗反应[51]。然而，保真度并不自动等同于预测力。一项系统综述在评估17项肿瘤学研究后指出，PDO虽可预测治疗反应，但必须同时满足分析效度、临床效度和临床效用三个层次的要求，而建立率与周转时间仍直接影响其临床可行性[32]。这意味着，从"类器官重现肿瘤"到"类器官指导临床决策"之间存在一个需要前瞻性证据填充的转化缺口。

在消化道肿瘤中，类器官药敏与临床反应的对应关系得到了较为密集的检验。胃癌研究通过73例组织建成57个类器官，建成成功率为**78%（57/73）**，类器官可传至17代，高增殖类器官富集REG4、KLF4、ERBB3、HRAS、NOTCH1、MYC等干性与增殖相关基因，并借助PDOX模型及患者实际治疗反应进行验证[30]。该研究的局限在于既往工作样本量小且缺乏化疗敏感性相关基因表达分析，而自身也未报告药敏与临床反应一致性的量化指标。相比之下，转移性结直肠癌的前瞻性研究给出了更明确的数字：PDO测试对以伊立替康为基础治疗的活检病灶反应预测准确率**超过80%**，且未将不应治疗的患者误分类[52]。这一结果在方法学上更为有力，因为它是前瞻性设计而非回顾性关联。但该研究同样受限于样本量，需扩大验证。结直肠癌肝转移领域的最新前瞻性观察研究纳入30例患者、成功建立39个类器官，对化疗与靶向药物进行药敏筛查，以体外药敏与体内客观反应的一致性为主要终点[53]。该研究尚属观察性、随访时间有限，其结论有待更长期的数据支持。将这三项工作并置可以看出，消化道肿瘤类器官预测的准确性数字虽令人鼓舞，但研究间在癌种、治疗线数、终点定义和样本规模上的异质性，使得跨研究的直接比较仍存在困难。

妇科肿瘤领域的证据进一步揭示了类器官预测能力的边界条件。卵巢癌PDO研究对23例患者的36个全基因组特征类器官进行药物筛选，与患者新辅助卡铂/紫杉醇临床反应对比，发现PDO保留原肿瘤基因组特征，**88%患者对至少一种药物高响应**，药物反应异质性可部分由遗传变异解释[31]。该研究的局限在于样本量有限且异质性机制未完全阐明。针对高级别浆液性卵巢癌的纵向研究则聚焦于长期培养后药敏稳定性的问题，比较临床反应并探索Pin1抑制剂等新靶向治疗，但长期培养后药敏变化研究不足、样本与临床验证有限[54]。更近期的研究建立了21例初治晚期上皮性卵巢癌患者来源类器官（EOC_Os），发现其紧密重现原发肿瘤组织病理与分子特征、维持肿瘤异质性且突变谱一致，但作者明确指出EOC_Os药物敏感性检测指导个体化治疗的临床应用仍待确定[55]。最具规模的一项工作构建了**191个卵巢癌类器官**，来自123例患者，结合药敏试验、随访数据和多模态组学AI模型预测铂敏感与耐药复发，结果显示原发肿瘤来源类器官预测准确性最高，转移灶次之，腹水来源类器官预测能力较低[56]。这一来源分层的结果提示，类器官的预测效度并非均质，取材部位本身就是一个影响对应关系的关键变量，而该研究摘要未完整展示AI模型性能，也留下了方法学透明度上的疑问。

脑肿瘤与骨肉瘤等难治性肿瘤的证据，则把讨论从"能否预测"推进到"能否优于现有标志物"。胶质母细胞瘤研究从55例患者建立59份类器官，开发GBO-DST药物敏感性检测流程，发现GBO比MGMT启动子甲基化状态更准确地预测TMZ个体反应，并筛选出第三代EGFR抑制剂lazertinib可有效抑制GBO生长与存活，且在体内移植模型中验证[57]。这是少数直接将类器官药敏与传统分子标志物进行头对头比较的工作，其结论对临床实践具有挑战性，但作者也承认GBO-DST预测临床药物反应仍需在结构良好的临床队列中广泛验证，并需深入基因组与转录组分析。骨肉瘤研究从23份肿瘤样本（20成骨型、3软骨母细胞型）建立PDO，将类器官活力指标与RECIST影像、组织学肿瘤坏死分级及临床随访关联，发现PDO可预测新辅助化疗反应与长期生存[58]。该研究面临肉瘤3D培养启动的技术挑战、化疗后残留肿瘤增殖能力低以及缺乏验证的功能性指标等限制。另一项脑肿瘤工作采用iPSC来源脑类器官与外植体共培养构建IPTO系统，覆盖成人、儿童和转移性脑癌，通过组织病理、基因组、表观基因组和scRNA-seq证明IPTO重现原肿瘤细胞异质性和分子特征，并在前瞻性患者队列中预测患者特异药物响应及耐药机制[59]。该研究未提及培养通量、成本及长期稳定性，而这些恰是临床转化的现实约束。这些工作共同表明，类器官在传统标志物预测失败的场景中可能提供增量信息，但其优势的稳健性仍取决于更大规模的前瞻性验证。

乳腺癌领域的证据引入了生物标志物引导的预测框架。研究评估早期乳腺癌类器官能否模拟I-SPY2临床试验的预测生物标志物，将HUB类器官RNA-seq与TCGA数据整合，构建类器官定制预测模型识别耐药培养物，并进行**386化合物10剂量**高通量筛选，结果显示类器官重现多数亚型，耐药模型筛选出多药或单药方案，亚型匹配患者显示生存获益[60]。该工作的独特之处在于将类器官药敏嵌入已确立的临床试验生物标志物体系（I-SPY2的RPS分型）中进行校验，而非孤立地评估药敏与反应的相关性。但其类器官样本量有限，预测模型仍需更大临床队列验证。这一思路与PharmaFormer的计算框架形成方法学上的互补：后者针对类器官药敏数据不足的问题，提出基于定制Transformer与迁移学习的模型，先在**900+细胞系、100+药物**的GDSC数据上预训练，再用肿瘤特异性类器官药敏数据微调，融合基因表达与药物SMILES结构，在三个肿瘤队列的临床药物反应预测中优于传统方法[61]。该模型的局限在于类器官药敏数据不足、依赖细胞系预训练、临床样本规模有限。将乳腺癌的生物学验证路径与PharmaFormer的计算增强路径对比，可以看到两种应对"类器官数据稀缺"的策略：一是将类器官锚定在已有临床生物标志物框架内，二是用迁移学习从细胞系数据中借用统计效力。两者的有效性均尚未在独立前瞻性队列中得到确认。

肺癌领域的方法学创新则指向药敏指标本身的优化。针对传统AUC/IC50药敏分析准确性有限的问题，研究开发了整合AUC、类器官生长率与癌症分期的多参数方法CODRP，用患者来源肺癌组织建立类器官，经病理验证后行药敏检测并分析无进展生存期，结果显示CODRP在PFS预后准确性上优于传统AUC方法[62]。该研究的限制在于患者来源细胞量有限、样本规模未明确、需进一步验证。这一工作的重要性在于它质疑了类器官药敏领域一个被广泛默认的假设：即AUC或IC50是衡量体外药物反应的最佳指标。如果CODRP的多参数整合确实优于单一AUC，那么此前大量基于AUC的类器官-临床对应性研究可能系统性地低估了类器官的预测潜力，也可能部分解释了不同研究间准确率数字的离散。

在模型层面的横向比较中，一项系统综述与荟萃分析提供了目前最综合的量化证据。该研究纳入使用相同抗癌药物治疗的实体瘤PDX或PDO研究，共**411对患者-模型配对（267 PDX、144 PDO）**，发现患者与匹配模型的总体治疗反应一致率为**70%**，PDX与PDO之间无显著差异，敏感性、特异性、阳性与阴性预测值相当；PDO应答者无进展生存延长，而PDX的这一关联仅在低偏倚风险配对中成立[63]。这一结果对领域具有双重含义：一方面，它表明类器官作为"替身模型"的预测能力与已被广泛接受的PDX模型相当，为其临床转化提供了合法性依据；另一方面，70%的一致率也意味着约三成的患者-模型配对存在预测偏差，且该分析仍受限于原始研究的异质性，作者明确指出需更多前瞻性研究才能给出确定性推荐。值得注意的是，PDO应答者PFS延长的证据在全部配对中成立，而PDX仅在低偏倚风险配对中成立，这一差异可能暗示类器官在预后分层方面具有相对优势，但也可能反映了两类模型在研究设计与偏倚控制上的系统差异，尚不能作为确定性结论。

综合上述证据，类器官与临床响应的对应关系呈现出几个需要正视的张力。第一，预测准确率的报告值在不同癌种和研究设计间差异显著，从结直肠癌的**超过80%**到荟萃分析的总体**70%**，这一离散既源于癌种生物学差异，也源于终点定义、药敏指标和患者选择的不同[52][63]。第二，类器官相对于传统分子标志物的增量价值已在胶质母细胞瘤的MGMT比较中得到初步展示，但这一优势能否推广到其他标志物体系尚不明确[57]。第三，取材部位、培养时长和药敏指标的选择均被证明影响预测效度，卵巢癌的原发灶-转移灶-腹水梯度[56]、高级别浆液性卵巢癌长期培养后的药敏稳定性问题[54]以及CODRP对AUC方法的挑战[62]共同表明，类器官的预测能力并非模型的固有属性，而是高度依赖于方法学决策。第四，计算方法的介入正在改变证据生成的模式，PharmaFormer的迁移学习策略[61]和乳腺癌研究中与I-SPY2框架的对接[60]代表了两种不同的增强路径，但两者均未解决类器官数据本身规模有限这一根本约束。当前证据足以支持类器官作为临床反应预测的有前景工具，但尚不足以支持其在任何癌种中替代标准诊疗决策，前瞻性、多中心、预设终点的验证仍是这一领域从相关性走向因果性的必经之路。

## 5 评测、可复现性与争议

单细胞与空间组学基础模型的评测在2026年出现了两条取向不同的路线：一条以统一框架横向比较既有模型，另一条以多维能力矩阵重新界定“基础模型是否真的优于简单基线”。前者对**Nicheformer、CellPLM、scGPT-spatial、GenePT、scELMo、Novae**六个代表性模型做统一基准测试，覆盖scRNA-seq、空间转录组与Perturb-seq，任务包括零样本与持续预训练下的聚类、监督注释、标记基因一致性和扰动预测 [37]。其核心发现是**没有任何模型全面占优**，排名会随模态、预处理、token化、生物先验、域偏移和指标选择而变化，说明“最优模型”的结论高度依赖评测条件 [37]。该工作同时指出模型对域偏移脆弱、可解释性有限，这实际上把争议从“谁更强”转向“在何种分布与何种任务下更强”，并暗示跨数据集泛化能力本身尚未被可靠刻画 [37]。

与之形成张力的是VCBench：它针对评测碎片化问题，整合四个虚拟细胞框架、七个能力维度，对**Geneformer、scGPT、UCE、TranscriptFormer、Arc State**五个基础模型与预注册线性/KNN基线在五个可测维度上比较 [64]。其结论更为尖锐——**基线在5个可测维度中的4个匹配或超越所有基础模型**，只有TranscriptFormer在跨模态RNA-蛋白预测上显著领先，**Pearson提升53%** [64]。这与前一工作“无模型全面占优”的结论并不直接冲突，但争议点在于：统一框架下的条件依赖排名，是否掩盖了简单基线在多数维度上的竞争力；而VCBench的强基线结论，又是否因维度选择与任务可测性而低估了基础模型在多尺度整合上的潜力 [37][64]。两篇证据共同暴露的可复现性缺口也各有侧重：前者强调域偏移与指标敏感性导致排名不稳定，后者则明确多尺度整合与in silico实验无法端到端测试，并对跨模态结果给出污染警告 [37][64]。因此，当前评测的争议不在于某一模型是否领先，而在于评测协议本身——任务维度、基线强度、预处理与污染控制——尚未收敛为可复现的共识标准 [37][64]。

## 6 空白与趋势

在跨物种迁移与虚拟细胞建模的交叉地带，一个尚未被充分回答的问题是：**当基础模型宣称学到“通用”细胞表征时，这些表征究竟在多大程度上编码了保守的调控机制，又在多大程度上只是拟合了物种特异的统计规律**。前述SATURN的宏基因、UCE的通用嵌入、GeneCompass的知识注入、Nicheformer的空间token，各自用不同的先验假设回答这一问题，但彼此之间缺乏统一的评测框架[20][21][22][23]。Speciesformer明确提出需区分保守原理与物种、组织及细胞环境特异变异，却未给出系统性定量答案[24]。更关键的是，跨物种扰动响应预测的评测目前高度碎片化：CellOT在LPS跨物种响应上验证[18]，CAME在同源映射质量上受限[19]，而TabICL/TabPFN的评估虽覆盖斑马鱼胚胎组成预测，却未系统检验跨物种扰动迁移[38]。**这意味着“跨物种迁移能力”目前更多是各模型的自证属性，而非可横向比较的基准维度**。

在类器官药敏与患者结局对应的方向上，证据的临床验证强度呈现出明显的分层。直肠癌PDO以**84.43%准确率、78.01%灵敏度、91.97%特异性**与III期临床试验对比，是目前证据链最完整的一项[16]；卵巢癌PDO在36个样本中显示**88%患者可找到有效药物**，但长期药敏稳定性仍需验证[31]；胃癌PDO生物库以57个类器官结合PDOX与患者实际治疗反应验证[30]；乳腺癌PDO则通过整合TCGA数据构建定制预测模型，并在386化合物筛选中识别耐药方案[60]。然而，这些研究在**预测终点、药敏读出方式、临床对照标准**上并不统一：直肠癌以化放疗反应为终点[16]，胃癌以化疗反应为终点[30]，卵巢癌以多药反应为终点[31]，乳腺癌则以I-SPY2生物标志物为参照[60]。PharmaFormer试图用迁移学习在GDSC预训练后以类器官数据微调来统一预测框架，在三个肿瘤队列中优于传统方法[61]，但其临床验证仍限于回顾性队列。**当前的核心空白是：没有任何一项研究在同一前瞻性临床试验中同时验证多种类器官药敏读出与患者结局的对应关系**，这使得“类器官药敏能否作为伴随诊断”这一问题在不同癌种间无法给出统一答案[32]。

心脏与血管类器官的扰动建模则面临另一类空白：**成熟度与功能读出的标准化尚未建立**。心脏类器官几何设计研究以收缩运动与钙瞬变10项变量为读出，发现形状决定生理属性[42]；AMPK/ERR激活方案以转录组、蛋白质组、收缩功能和代谢能力的稳健成熟为标志，使TNNI3比例达18%[43]；Heart-on-a-Miniscope以228 lp/mm@60帧/秒的钙瞬变成像能力为读出[44]。三者对“成熟”的定义分别落在功能异质性、分子表型和电生理读出三个不同层面，彼此之间无法直接换算。更关键的是，**目前没有一项心脏类器官研究将扰动响应预测与患者临床结局（如心律失常、心衰事件）直接对应**，这与肿瘤类器官领域已有多项临床对照研究形成鲜明对比[16][30]。跨物种动脉粥样硬化研究虽从PIM单核细胞衍生出362基因血液特征并筛选20基因panel[46]，但其AUC数值不完整、临床验证规模未明，尚不能视为心血管类器官临床转化的直接证据。

空间转录组与多重化策略在类器官中的应用，暴露出**通量、空间分辨率与微环境保真度之间的三角约束**。Stereo-seq在类器官中优化芯片包被与通透条件，实现单芯片多样本空间转录组，但小类器官捕获偏低、单细胞注释困难[35][34]。皮层脑类器官的mosaic多重化策略开发了SCanSNP去卷积方法，在50/100/300天纵向采样中重建神经发育轨迹[36]，但成本与批次间变异仍是限制。形态发生素patterning研究用微流控浓度梯度结合多重单细胞转录组筛选，发现时序、浓度与组合显著决定区域组成[45]。这些工作共同指向一个方法学瓶颈：**类器官的空间转录组捕获效率与单细胞注释仍受组织大小和类型限制，而多重化策略虽提高通量却引入去卷积不确定性**。更值得注意的是，Perturb-FISH虽在3D肿瘤异种移植组织中展示了空间扰动读取的可行性[3]，但其gRNA原位扩增策略在类器官中的系统应用尚未见报道。**将CRISPR扰动、空间转录组与类器官三者整合的通用框架，目前仍是空白**。

AI驱动的扰动建模在类器官中的验证深度差异悬殊。脑类器官扰动信息基础模型构建了360万细胞图谱，优先排序出343个自闭症候选基因，其中167个在关键簇中[12]；DiRL在iPSC来源类器官数据上训练强化学习智能体，对随机扰动胜率69%[13]；Leigh综合征研究用酵母与类器官双筛选识别唑类化合物[14]；多组学类器官嵌入整合135个CRC/PDAC PDO预测药物AUC[15]。这些工作在预测目标上分化明显，但共享一个未解决的争议：**预测结果是否能在真实类器官或临床中复现**。目前多数工作停留在计算验证或有限实验验证阶段，缺乏前瞻性临床验证[12][13][14][15]。与此同时，基础模型在扰动预测中的表现高度条件依赖：统一基准测试发现六个代表性单细胞与空间基础模型在零样本和持续预训练设置下，**无模型全面占优，排名随任务、数据模态和评估指标变化**[37]。TabICL/TabPFN在伪bulk扰动预测中持续优于专用基线[38]，进一步说明**通用表格模型与领域专用架构之间并非替代关系，而是任务尺度决定了相对优势**。

综合来看，类器官与模式生物虚拟响应建模当前存在五个明确的空白与趋势。**第一，跨物种扰动响应预测缺乏统一基准**：现有工作各自在LPS响应、同源映射或胚胎组成预测上验证，但无一项系统比较不同跨物种迁移策略在相同扰动任务上的表现[18][19][38]。**第二，类器官药敏与临床结局的对应关系缺乏前瞻性多癌种统一验证**：直肠癌、胃癌、卵巢癌、乳腺癌研究各自为战，药敏读出与临床终点不统一，PharmaFormer的迁移学习框架虽提供统一预测思路但尚未经前瞻性验证[16][30][31][60][61]。**第三，心脏与血管类器官的扰动响应建模尚未与患者临床结局直接对应**：现有工作聚焦于成熟度优化与功能读出标准化，跨物种动脉粥样硬化研究虽提供血液特征但临床验证不完整[42][43][44][46]。**第四，CRISPR扰动、空间转录组与类器官三者的整合框架尚未建立**：Perturb-FISH在3D组织中展示可行性，Stereo-seq在类器官中优化了空间捕获，但二者尚未在类器官体系中系统结合[3][35][34]。**第五，AI扰动预测的实验与临床验证深度不足**：脑类器官候选基因排序、DiRL扰动策略、Leigh药物重定位、多组学嵌入预测均停留在计算或有限实验验证阶段，缺乏前瞻性临床验证[12][13][14][15]。这些空白共同指向一个整合性挑战：**如何在同一个类器官或模式生物体系中，同时满足扰动通量、空间分辨率、微环境保真度与临床可验证性**，而这一挑战目前尚无任何单一研究或框架给出完整答案。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据（引用数字与 [id]） |
|---|---|---|
| 2.1 类器官与器官芯片扰动建模 | **朝阳** | **28 篇**、**recent_share 0.54**、**CNS 占比 0.36**，2019–2026 持续产出；但方法未收敛：从患者来源类器官药敏 [16] 到微流控组合药筛 [33]、再到 CRISPR+空间转录组联测 [3]，读出与建模范式仍在换代 |
| 2.2 模式生物扰动响应模型 | **萌芽** | 仅 **3 篇**、**median_citations 1**、**CNS 占比 0.33**，2024–2026 才出现；已有跨物种小脑空间图谱 [47]、表格基础模型做跨物种扰动预测 [38]、跨物种动脉粥样硬化重建 [46]，但样本量极小、无基准 |
| 2.3 跨物种迁移 | **朝阳** | **12 篇**、**median_citations 72**、**CNS 占比 0.17**；神经最优传输做扰动响应迁移 [18]、通用细胞嵌入 [21]、Nicheformer [23]、跨物种细胞图谱 [39] 均为近三年，方法路线明显未定 |
| 2.4 虚拟组织与数字孪生建模 | **萌芽** | 仅 **1 篇**、**recent_share 1.0**、**CNS 占比 0.0**，即 AI 虚拟类器官 [25]，概念先行、无对照基准 |
| 3 数据资源与基准 | **萌芽** | 仅 **1 篇**、**recent_share 0.0**、**median_citations 0**，为发育海马单细胞图谱做基础模型基准 [49]，尚未形成领域级资源 |
| 4 与临床响应的对应 | **成熟** | **17 篇**、**recent_share 0.59**、**CNS 占比 0.41**、**median_citations 9**；从 2018 年转移性胃肠癌类器官预测治疗响应 [51]、2019 年结直肠癌化疗预测 [52]、胰腺癌个体化药筛 [50] 到 2021 年癌症预测生物标志物综述 [32]，范式已收敛为"类器官药敏↔临床结局"相关性验证，增量为主 |
| 5 评测、可复现性与争议 | **萌芽** | 仅 **2 篇**、**recent_share 1.0**、**median_citations 1**、**CNS 占比 0.0**，为单细胞/空间基础模型统一基准 [37] 与 VCBench [64]，2026 年才起步 |

**整体判断**：这个方向整体处于**朝阳期偏早期**——总证据 **64 条**、**recent_share 0.55**、**CNS 占比 0.31**，且 **2024–2026 三年合计 46 条**（12+12+22）占绝对多数，说明是近两年才真正起量的赛道。但结构极不均衡：**临床对应（2.4/4）已成熟**，**类器官扰动建模（2.1）与跨物种迁移（2.3）在爆发但方法未收敛**，而**模式生物响应模型（2.2）、虚拟组织（2.4）、数据基准（3、5）几乎空白**。窗口期判断：**类器官+单细胞/空间扰动建模的"方法卡位"窗口约剩 12–18 个月**，因为 accepted_per_round 已从 **35、36 骤降到 19、4、2**，说明该细分的方法类工作正在被快速消化；而**跨物种迁移 + 虚拟组织 + 基准**这条线窗口更长（**2–3 年**），因为 2.2/2.4/3/5 合计仅 **7 条**证据。最大不确定性有三：一是**评测缺失**——2.1 与 2.3 的高引工作（[3]、[18]）各自定义任务，直到 2026 年才出现统一基准 [37]、[64]，**"预测准不准"尚无公认标尺**；二是**跨物种迁移的可迁移性存疑**，2.2 的 median_citations 仅 **1**，跨物种预测 [38] 只有 **1 次引用**，说明社区尚未认可；三是**临床对应已成熟**，单纯再做"类器官药敏预测患者结局"边际收益低，**必须叠加建模/跨物种/多模态才有增量**。

**接下来怎么做**：

1. **用公共类器官 Perturb-seq / 空间数据做"扰动响应 + 空间"联合建模，抢 2.1 的方法位**。切入点：以 CRISPR+空间转录组联测范式 [3] 为模板，把单细胞扰动响应预测从"表达向量回归"升级为"空间邻域条件生成"，用你已有的多模态建模栈直接复用。为什么现在：2.1 有 **28 篇**、**CNS 0.36**，但 accepted_per_round 已降到 **4、2**，方法红利正在关闭，**12 个月内**是最后的方法卡位期。产出：一个空间感知的扰动响应预测器 + 在公开类器官药筛数据上的复现。

2. **把跨物种迁移做成"评测驱动"的细分，而不是再提一个新 embedding**。切入点：以神经最优传输 [18] 与通用细胞嵌入 [21] 为基线，在跨物种细胞图谱 [39] 与跨物种小脑空间图谱 [47] 上系统评测"小鼠→人"响应迁移，直接对接 2026 年的统一基准 [37] 与 VCBench [64]。为什么现在：2.3 有 **12 篇**、**median_citations 72**，但 **CNS 仅 0.17**，且 2.2 的跨物种预测只有 **1 次引用**——**"没人做对评测"就是最大的空位**，且评测类工作对生物信息学博后门槛最低、复用你现有 benchmark 工程能力。产出：跨物种扰动迁移基准 + 失败模式分析。

3. **切入 2.2 模式生物扰动响应模型，用斑马鱼/小鼠多器官单细胞图谱做剂量-时间响应预测**。切入点：2.2 只有 **3 篇**、**median_citations 1**，且已有工作只做图谱重建 [47]、[46]，**没人做剂量/时间维度的响应建模**。用公共斑马鱼/小鼠扰动图谱 + 你的衰老时间序列建模经验，做"剂量×时间×器官"三轴响应预测。为什么现在：**萌芽期、竞争最少**，且与你的衰老方向天然衔接（时间响应即衰老轨迹）。产出：模式生物剂量-时间响应预测模型，可作为跨物种迁移的源域。

4. **把虚拟组织/数字孪生作为"整合层"，而非独立方向**。切入点：2.4 仅 **1 篇** [25]、**CNS 0.0**，概念先行无基准。不要单独做"虚拟类器官"，而是把建议 1–3 的预测器组装成"类器官数字孪生"demo：输入扰动 → 输出单细胞+空间+表型多尺度响应。为什么现在：**概念已被提出但无人落地**，谁先给出可复现 pipeline 谁定义标准。产出：一个端到端 demo + 开源代码，直接对接你的合作项目（类器官+多组学）。

5. **优先做心脏/血管类器官，避开肿瘤类器官红海**。切入点：纳入标准明确"心脏/血管类器官优先"，而 2.1 与 4 的高引工作几乎全是肿瘤 [16]、[51]、[52]、[50]；心血管侧仅有跨物种动脉粥样硬化摘要 [46]（**0 引用**）。为什么现在：**肿瘤类器官药敏已成熟（阶段 4）、增量为主**，而心血管类器官+扰动建模几乎空白，且与你衰老+多组学背景（血管衰老）高度契合。产出：心血管类器官扰动响应模型 + 患者结局对应验证，形成差异化标签。

## 参考文献

1. In-organoid single-cell CRISPR screening reveals determinants of hepatocyte differentiation and maturation.. Genome biology 2023. https://doi.org/10.1186/s13059-023-03084-8
2. Causal identification of single-cell experimental perturbation effects with CINEMA-OT.. Nature methods 2023. https://doi.org/10.1038/s41592-023-02040-5
3. Simultaneous CRISPR screening and spatial transcriptomics reveal intracellular, intercellular, and functional transcriptional circuits.. Cell 2025. https://doi.org/10.1016/j.cell.2025.02.012
4. Trellis tree-based analysis reveals stromal regulation of patient-derived organoid drug responses.. Cell 2023. https://doi.org/10.1016/j.cell.2023.11.005
5. Large-scale CRISPR screening in primary human 3D gastric organoids enables comprehensive dissection of gene-drug interactions.. Nature communications 2025. https://doi.org/10.1038/s41467-025-62818-3
6. Deconvolution of cell type-specific drug responses in human tumor tissue with single-cell RNA-seq. Genome Medicine 2020. https://doi.org/10.1186/s13073-021-00894-y
7. Trellis Single-Cell Screening Reveals Stromal Regulation of Patient-Derived Organoid Drug Responses. bioRxiv 2023. https://doi.org/10.1101/2022.10.19.512668
8. Image-based profiling and deep learning reveal morphological heterogeneity of colorectal cancer organoids. Comput. Biol. Medicine 2024. https://doi.org/10.1016/j.compbiomed.2024.108322
9. A deep learning-based computational pipeline predicts developmental outcome in retinal organoids.. PLoS biology 2026. https://doi.org/10.1371/journal.pbio.3003597
10. Spatio-Temporal Analysis of Patient-Derived Organoid Videos Using Deep Learning for the Prediction of Drug Efficacy. 2023 IEEE/CVF International Conference on Computer Vision Workshops (ICCVW) 2023. https://doi.org/10.1109/ICCVW60793.2023.00425
11. Systematic modeling of phenotypic drug response profiles in patient-derived organoids. bioRxiv 2026. https://doi.org/10.64898/2026.07.29.741618
12. AI-driven framework modeling perturbation in brain organoids reveals candidate genes for autism. bioRxiv 2026. https://doi.org/10.64898/2026.08.22.746387
13. Reinforcement learning enables single-cell foundation models to learn cellular differentiation. bioRxiv 2025. https://doi.org/10.64898/2025.12.09.693267
14. Accelerating Leigh syndrome drug discovery through deep learning screening in brain organoids.. Nature communications 2026. https://doi.org/10.1038/s41467-026-71391-2
15. Abstract 494: Multi-omics patient-derived organoid embeddings predict targeted therapy response and KRAS inhibitor sensitivity.. Cancer Research 2026. https://doi.org/10.1158/1538-7445.am2026-494
16. Patient-Derived Organoids Predict Chemoradiation Responses of Locally Advanced Rectal Cancer.. Cell Stem Cell 2019. https://doi.org/10.1016/j.stem.2019.10.010
17. Integrating artificial intelligence-driven digital pathology and genomics to establish patient-derived organoids as new approach methodologies for drug response in head and neck cancer.. Oral oncology 2025. https://doi.org/10.1016/j.oraloncology.2025.107742
18. Learning single-cell perturbation responses using neural optimal transport. bioRxiv 2021. https://doi.org/10.1038/s41592-023-01969-x
19. Cross-species cell-type assignment from single-cell RNA-seq data by a heterogeneous graph neural network. bioRxiv 2021. https://doi.org/10.1101/gr.276868.122
20. Toward universal cell embeddings: integrating single-cell RNA-seq datasets across species with SATURN. Nature Methods 2024. https://doi.org/10.1038/s41592-024-02191-z
21. Universal Cell Embeddings: A Foundation Model for Cell Biology. bioRxiv 2026. https://doi.org/10.1101/2023.11.28.568918
22. GeneCompass: deciphering universal gene regulatory mechanisms with a knowledge-informed cross-species foundation model.. Cell research 2024. https://doi.org/10.1038/s41422-024-01034-y
23. Nicheformer: a foundation model for single-cell and spatial omics. bioRxiv 2024. https://doi.org/10.1038/s41592-025-02814-z
24. Speciesformer learns conserved cellular states for cross-species generative virtual cell modeling.  . https://doi.org/10.64898/2026.09.22.752128
25. Artificial Intelligence Virtual Organoids (AIVOs).. Bioactive materials 2025. https://doi.org/10.1016/j.bioactmat.2025.12.030
26. Single-Cell-Derived Tumor Organoid (STO) arrays on a microfluidic chip for personalized drug screening to address heterogeneity-induced drug resistance in colorectal cancer. Microsystems & Nanoengineering 2025. https://doi.org/10.1038/s41378-025-01068-1
27. LucaCell: a sequence-centric foundation model for cross-species single-cell analysis. bioRxiv 2026. https://doi.org/10.64898/2026.09.08.750024
28. Mouse-Geneformer: A deep learning model for mouse single-cell transcriptome and its cross-species utility. bioRxiv 2024. https://doi.org/10.1371/journal.pgen.1011420
29. BrainBeacon: A Cross-Species Foundation Model for Single-cell Resolved Brain Spatial Transcriptomics. bioRxiv 2025. https://doi.org/10.1101/2025.07.08.663729
30. Personalized drug screening using patient-derived organoid and its clinical relevance in gastric cancer.. Cell reports. Medicine 2024. https://doi.org/10.1016/j.xcrm.2024.101627
31. Patient-Derived Ovarian Cancer Organoids Mimic Clinical Response and Exhibit Heterogeneous Inter- and Intrapatient Drug Responses.. Cell Reports 2019. https://doi.org/10.1101/2019.12.12.19014712
32. Patient-derived organoids as a predictive biomarker for treatment response in cancer patients. npj Precision Oncology 2021. https://doi.org/10.1038/s41698-021-00168-1
33. Automated microfluidic platform for dynamic and combinatorial drug screening of tumor organoids. Nature Communications 2020. https://doi.org/10.1038/s41467-020-19058-4
34. Application of spatial transcriptomics across organoids for a high-resolution, spatial whole-transcriptome benchmarking dataset. iScience 2026. https://doi.org/10.1016/j.isci.2026.115827
35. Application of spatial transcriptomics across organoids: a high-resolution spatial whole-transcriptome benchmarking dataset. bioRxiv 2026. https://doi.org/10.1101/2025.05.04.651803
36. Multiplexing cortical brain organoids for the longitudinal dissection of developmental traits at single-cell resolution.. Nature methods 2024. https://doi.org/10.1038/s41592-024-02555-5
37. Harmonised benchmarking of foundation models for single-cell and spatial transcriptomics reveals context-dependent generalisation.  2026. https://arxiv.org/abs/2607.17227
38. Tabular Foundation Models Are Competitive Cellular Perturbation Predictors Across Biological Scales. bioRxiv 2026. https://doi.org/10.64898/2026.06.28.735106
39. Construction of a cross-species cell landscape at single-cell level. Nucleic Acids Research 2022. https://doi.org/10.1093/nar/gkac633
40. Single-Cell Analysis Guides Organoid CRISPR Screening to Reveal NF1 as a Gatekeeper of Cervical Squamous Malignant Transformation.. Cancer Research 2026. https://doi.org/10.1158/0008-5472.CAN-25-5315
41. Deciphering Anti‐Cancer Drug Efficacy Through Nanomechanical Vibrations in Living Gastric Cancer Organoids. Advancement of science 2026. https://doi.org/10.1002/advs.76878
42. Design optimization of geometrically confined cardiac organoids enabled by machine learning techniques.. Cell reports methods 2024. https://doi.org/10.1016/j.crmeth.2024.100798
43. Maturation of human cardiac organoids enables complex disease modeling and drug discovery.. Nature cardiovascular research 2025. https://doi.org/10.1038/s44161-025-00669-3
44. Heart‐on‐a‐Miniscope: A Miniaturized Solution for Electrophysiological Drug Screening in Cardiac Organoids. Small 2024. https://doi.org/10.1002/smll.202409571
45. Decoding morphogen patterning of human neural organoids with a multiplexed single-cell transcriptomic screen. bioRxiv 2024. https://doi.org/10.1101/2024.02.08.579413
46. Abstract 4372183: Cross-species single-cell reconstruction of atherosclerosis reveals predictive monocytes for acute coronary events. Circulation 2025. https://doi.org/10.1161/circ.152.suppl_3.4372183
47. Cross-species single-cell spatial transcriptomic atlases of the cerebellar cortex. Science 2024. https://doi.org/10.1126/science.ado3927
48. Single-Cell Atlas of Microglia Reveals Conserved and Divergent Cell Populations in Mouse and Human Brain 2255696. Journal of Immunology 2026. https://doi.org/10.1093/jimmun/vkag141.278
49. A lifespan single-cell atlas of the human developing hippocampus benchmarks familial Alzheimer's disease brain organoids..  . https://doi.org/10.64898/2026.09.18.752796
50. Pancreatic cancer organoids recapitulate disease and allow personalized drug screening. Proceedings of the National Academy of Sciences of the United States of America 2019. https://doi.org/10.1073/pnas.1911273116
51. Patient-derived organoids model treatment response of metastatic gastrointestinal cancers. Science 2018. https://doi.org/10.1126/science.aao2774
52. Patient-derived organoids can predict response to chemotherapy in metastatic colorectal cancer patients. Science Translational Medicine 2019. https://doi.org/10.1126/scitranslmed.aay2574
53. Prospective comparison of patient-derived organoid drug screening with standard guideline recommendations for colorectal cancer liver metastasis.. Journal of Clinical Oncology 2026. https://doi.org/10.1200/jco.2026.44.16_suppl.e15609
54. Longitudinal prediction of drug response in high-grade serous ovarian cancer organoid cultures aligning with clinical responses. bioRxiv 2024. https://doi.org/10.1016/j.jare.2025.08.009
55. Patient-derived organoids predict responses to chemotherapy and PARP inhibitors in advanced ovarian cancer. Journal of Translational Medicine 2026. https://doi.org/10.1186/s12967-025-07112-y
56. Patient-derived ovarian cancer organoids as platforms for predicting platinum resistance and screening tumor stem cell inhibitors.. Drug resistance updates 2026. https://doi.org/10.1016/j.drup.2026.101411
57. Patient-derived organoids predict personalized drug response and reveal alternative therapeutic options in glioblastoma. Cell Reports Medicine 2026. https://doi.org/10.1016/j.xcrm.2026.102850
58. Personalized prediction of chemotherapy efficacy in osteosarcoma through patient-derived organoids: correlation with survival and tumor proliferation potential. Journal of experimental & clinical cancer research : CR 2025. https://doi.org/10.1186/s13046-025-03541-1
59. Individualized patient tumor organoids faithfully preserve human brain tumor ecosystems and predict patient response to therapy.. Cell stem cell 2025. https://doi.org/10.1016/j.stem.2025.01.002
60. Biomarker-guided responses in patient-derived organoids predict effective therapies in breast cancer. Cell Reports Medicine 2026. https://doi.org/10.1016/j.xcrm.2026.102973
61. PharmaFormer predicts clinical drug responses through transfer learning guided by patient derived organoid. npj Precision Oncology 2025. https://doi.org/10.1038/s41698-025-01082-6
62. Abstract 2503: Lung cancer organoid-based diagnostic response prediction (CODRP) for predicting anticancer drug response and progression-free survival. Cancer Research 2026. https://doi.org/10.1158/1538-7445.am2026-2503
63. Comparative analysis of patient-derived organoids and patient-derived xenografts as avatar models for predicting response to anti-cancer therapy.. Cancer Treatment Reviews 2026. https://doi.org/10.1016/j.ctrv.2026.103190
64. VCBench: A Multi-Dimensional Benchmark for Single-Cell Foundation Models. bioRxiv 2026. https://doi.org/10.64898/2026.06.18.733146
