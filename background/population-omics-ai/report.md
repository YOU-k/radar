# 人群健康与多组学 AI · 方向背景报告

证据 119 篇 · 覆盖度 0.80 · 第 14 轮 · 更新 2026-11-08 · 数字核验删句 5

## 本次变更

- 新增 [16] Multi-omics in the All Of Us Research Program expands mapping genetic mechanisms in health and disease
- 新增 [100] Sex shapes plasma molecular signatures of dementia risk across APOE ε4 strata

## 摘要（TL;DR）

- 生成式EHR轨迹模型沿“更大规模、更多模态、更强干预能力”推进，而 ALADYNOULLI 以“概率的混合”联合建模纵向诊断、年龄与多基因风险，在三个生物库 n>683,000、随访52年、348种疾病上识别出21个可复制特征 [1]。
- Foresight 强调 EHR 中约80%的信息以自由文本存在，覆盖18类 SNOMED 概念并支持日/周/月分辨率，但作者明确其当前形式不宜直接用于临床决策支持 [2]。
- NOAH 基于 MIMIC 家族559M事件、299,000患者原生处理图像、时序、分类与文本，支持自回归预测、零样本分类与反事实干预模拟 [3]。
- Foresight-England 的243M参数解码器在约6100万人去标识化纵向EHR上从头训练，但因 NHS England 暂停数据访问，定量结果无法导出，提示国家级生成式模型的可复现性受数据治理约束 [4]。
- EHR-MPC 把脓毒症治疗优化重构为推理时控制问题，在8家医院多中心ICU队列上离线策略性能与强化学习基线相当、模拟性能更优，但仿真评估与真实临床仍有差距 [5]。
- LifeLong Digital Twin 在25个疾病终点、3类任务、4个语言模型上16个模型-读出比较全部优于无 Context/Harness 基线，疾病识别 F1 从0.422升至0.504（Context）、0.515（Harness），相对增益19.4%、22.0%，但作者自陈未确立统计显著性 [6]。
- 神经退行性疾病工作将诊断前时间戳EHR标记化后用 Transformer 生成嵌入并 K-means 聚类，在 CPRD Aurum 与 UK Biobank 逾100,000患者中为 AD 和 PD 各识别出5个可重复亚型，但外部验证仅限 UK Biobank、生物学机制仍待验证 [7]。
- 面向早期预警的 LightGBM 轨迹模型在 All of Us 297,861人、12项生物标志物3年轨迹上 AUROC 0.797 优于静态汇总0.755（P<0.001），匹配分析0.727 vs 0.680，说明即便非生成式方法轨迹特征本身也携带独立信号 [8]。
- UK Biobank Pharma Proteomics Project 对54,219名参与者检测2,923种血浆蛋白，发现14,287个主要遗传关联，其中81%为既往未报道，并精细映射出29,420个独立信号 [9]。
- 蛋白组图谱基于53,026人、2,920种蛋白报告168,100个蛋白—疾病关联和554,488个蛋白—性状关联，183种疾病的判别 AUC >0.80，并通过 pQTL 确定474个因果蛋白 [10]。
- 结构变异与重复序列方面，长读长组装参考面板在54,306人中插补54,578个 SV 和15,826个 VNTR，二者共同解释蛋白丰度遗传力约8.0%，123种蛋白主要由 SV 驱动 [11]。
- UK Biobank 暴露组全关联在492,567人中识别25个与死亡和蛋白组衰老时钟相关的独立暴露，并报告暴露组对死亡和25种年龄相关病的解释度常高于基因组，但该结论来自观察性设计，存在残余混杂与暴露测量误差 [12]。
- All of Us 245,388例全基因组序列与 UKB 联合开发的32个性状多血统 PRS 显示，增加多样性提升部分性状精度，但最大化样本量并非普遍最优，PRS 精度随血统分歧线性下降、多血统训练可减缓 [13]。
- 在 AOU、PMBB、UCLA 三个生物库171,095人中对48个冠心病 PRS 的评估发现，群体水平表现相似的评分在个体层面一致性差（ICC 与 Light κ 低），提示以群体 AUC 为唯一标准的评估不足以支撑临床决策 [14]。
- 在27个 UK Biobank 性状上，AlphaGenome 与 Borzoi 衍生注释的位点发现中位增益分别为1.8%和3.8%，低于 baselineLD 的5.1%，GPN-Star 甚至减少发现，说明表征学习的价值可能更多体现在风险分层而非位点发现 [15]。
- All of Us 多组学 QTL 分析检出182,246个 QTL，54,255个精细定位到罕见变异、其中59.4%（32,235个）解析为单一因果变异，罕见变异效应更易受祖源限制并富集于孟德尔疾病基因（OR=1.4）和获批药物靶点 [16]。
- HELICS 提出潜空间流匹配框架用于无定相基因型条件合成，实验覆盖 UKB chr15 18,784个 SNP 及全基因组600,336个 SNP，在 MAF、LD 和隐私代理指标上优于 HAPNEST 等基线，但低 MAF 变异 R² 偏低且生成样本 NN IBS 相似度较高 [17]。
- UK Biobank 最新全基因组测序覆盖490,640名参与者、平均32.5×，识别约15亿变异，较芯片插补增18.8倍、较全外显子测序增>40倍，其中93.5%为芬兰以外欧洲 ancestry [18]。
- All of Us 内部比较研究纳入393,590名参与者，发现 PME 人群 WGS 覆盖更少（35.2% vs 83.2%），两种 EHR 来源在疾病患病率、表型关联和已知基因型-表型关联复制率上存在差异，提示同一队列内部不同 EHR 通路的研究效用不可互换 [19]。
- 对 UK Biobank 多遗传祖源人群开展混合模型 GWAS 与跨祖源荟萃分析覆盖7,266个性状，发现14,676个仅欧洲祖源分析未发现的显著位点，但多数关联仍主要见于欧洲祖源 [20]。
- 多祖源 BMI 评分在 UK Biobank 欧洲裔中解释17.6%的 BMI 变异，其他人群从东亚裔美国人16%到农村乌干达2.2%不等；同一研究内8岁时加入 PGS 使解释方差从11%升至21%，5岁时预测18岁 BMI 从22%升至35% [21]。
- 在 FOS 3,588人与 UK Biobank 327,837人中，CAD 的 PRS 风险比从19岁3.58降至70岁1.51，40–45岁组 PRS 显著优于 PCE，多3.2倍适宜 [22]。
- UK Biobank 中整合传统风险因素、PRS 与202蛋白评分后，CAD 内部验证 AUC 从0.750升至0.789，外部验证从0.717升至0.762，9蛋白面板即可捕获大部分预测信息 [23]。
- EPIC-Norfolk 中 >11,000人、219,415人年的非靶向代谢组学发现640个显著代谢物-疾病关联，其中420个（65.5%）跨至少2种 NCD 共享 [24]。
- UKB-MDRMF 整合六类数据联合建模1,560种疾病，优于单类别风险评估，并揭示风险因素-疾病及共病关联，但依赖单一生物库人群与表型定义，跨机构可比性仍是待解问题 [25]。
- 利用 UK Biobank 与 All of Us 的 EHR 纵向用药与生物标志物数据对10个药物-表型对做常见变异 GWAS 与罕见变异负荷检验，证明疾病 PRS 可预测药效，同时指出用药与检测时点不齐、依从性与适应证混杂等纵向表型分析陷阱 [26]。
- 贝叶斯Cox回归结合随机变分推断与似然重加权支持百万级数据点、数千时变协变量分析，并在 UK Biobank 心肌梗死应用中给出可行不确定性估计，但作者明确指出方法依赖变分近似、精度受子采样影响 [27]。
- 共病研究方向的AI方法证据目前仅停留在综述层面，抽取字段明确标注“仅摘要信息，无具体方法细节”、具体方法与结果不详，该方向尚无可用于评测对比的模型、数据集或核心数字 [28]。

## 1 背景与定义

人群健康与多组学 AI 的边界，首先由“数据底座”划定：它要求生物样本库级别（≥万人）的队列，而非单中心小样本关联研究。UK Biobank 以 50 万 40–69 岁参与者、基线问卷/生物样本/影像/加速度计与健康记录链接为骨架，预计 20 年随访可累积糖尿病约 68,000 例、心梗与冠心病死亡 47,000 例、卒中 20,000 例、阿尔茨海默病 30,000 例 [29]；其后扩展为插补约 9600 万变异的深度表型遗传资源 [30]，并完成 490,640 人、平均覆盖 32.5× 的全基因组测序 [18]。All of Us 以多样性为目标，拟招募至少 100 万人，截至 2019 年 7 月已有 >175,000 人贡献生物样本、其中 >80% 来自历史上生物医学研究不足群体 [31]；FinnGen 则整合 9 个芬兰生物库与全国健康登记，基于 224,737 人插补基因型和 1,932 个终点开展 GWAS 与精细定位 [32]。**这三类资源分别代表“深度表型”“祖先多样性”“隔离人群富集”三种互补设计，也各自携带健康志愿者偏倚、EHR 通路异质与外推受限的结构性局限** [29][19][32]。

从演化脉络看，该方向经历了三次重心迁移。第一次是把结构化 EHR 当作“医学概念序列”做自监督建模：BEHRT 用 Transformer 结合就诊位置、年龄与事件顺序学习患者表示 [33]，Med-BERT 把 BERT 式预训练迁移到 ICD 诊断序列并强调小样本迁移 [34]。第二次是从“预测单病”转向“生成整条轨迹”：Foresight 同时整合占约 80% 的自由文本与结构化格式，覆盖 18 类 SNOMED 概念 [2]；Delphi-2M 在 UK Biobank 训练、丹麦登记验证，同时预测 1000 多种疾病并模拟个体终身轨迹 [35]；ALADYNOULLI 进一步把纵向诊断、年龄与多基因风险纳入贝叶斯生成框架，在三个生物库 n>683,000 上识别 21 个可复制特征并发现 151 个全基因组显著位点 [1]。第三次是“从预测到决策与表征”：EHR-MPC 把脓毒症治疗重构为推理时控制 [5]，NOAH 走向任务无关的多模态患者旅程表示 [3]，PULSE 则从稀疏常规血检生成代谢组与蛋白组谱 [36]。**这条脉络的核心张力是：生成能力越强，对数据治理与可复现性的依赖越重**——Foresight-England 在约 6100 万人 EHR 上训练却因数据访问暂停无法导出定量结果，即是明证 [4]。

第二个核心问题是“遗传—分子—表型”链条能否支撑机制发现，而非仅提升预测。UK Biobank Pharma Proteomics Project 在 54,219 人中检测 2,923 种血浆蛋白，发现 14,287 个主要遗传关联、其中 81% 为既往未报道 [9]；罕见变异分析在 49,736 人中识别 5,433 个罕见基因型—蛋白关联、81% 未被既往 GWAS 检出 [37]。蛋白组图谱把调控信息连到终点：53,026 人、2,920 种蛋白的报告给出 183 种疾病判别 AUC>0.80，并通过 pQTL 确定 474 个因果蛋白 [10]。代谢组侧，118,461 人、249 个 NMR 指标的图谱覆盖 700 多种疾病的患病、发病与死亡关联 [38]，跨国研究在 700,217 人中用 36 个代谢标志物训练 12 种疾病 Cox 评分并跨三库重复 [39]。**这些工作共同把“关联”推进到“可解释的中介证据”，但因果推断普遍依赖 MR 假设，且样本以欧洲裔为主** [40][9]。

第三个核心问题是人群可迁移性，它同时出现在遗传与表型两侧。跨祖源 GWAS 在 UK Biobank 多祖源人群中发现 14,676 个仅欧洲祖源分析未发现的显著位点 [20]；多祖源 BMI 评分在欧洲裔中解释 17.6% 的 BMI 变异，其他人群从东亚裔美国人 16% 到农村乌干达 2.2% 不等 [21]。更棘手的是同一人群内的个体层面不一致：在三个生物库 171,095 人中对 48 个冠心病 PRS 的评估显示，群体表现相似的评分在个体层面一致性差 [14]。表型侧同样如此：All of Us 内部患者介导 EHR 与提供者来源 EHR 在 WGS 覆盖（35.2% vs 83.2%）、患病率与关联复制率上存在差异 [19]；ICD-8 到 ICD-10 的单向映射虽可桥接丹麦自 1965 年以来的纵向数据，却不提供反向映射 [41]。**因此“跨队列可复现”不能仅以群体 AUC 或显著性复制为标准，还需校准、编码 harmonization 与个体一致性检验** [14][41]。

最后是评测与资源基础设施的缺位。GWAS Catalog 截至 2024 年 7 月收录 625,113 条关联、>15.5K 性状和 >85K 汇总统计数据集，但标准化不足、非欧祖源偏少 [42]；UK Biobank PRS Release 覆盖 53 种性状并优于 81 个已发表 PRS，却主要基于 UK Biobank 人群 [43]。Phecodes 提供高通量 ICD 表型但受编码误差制约 [44]，NMR 代谢组的技术变异校正流程仅覆盖约三分之一 UKB 参与者 [45]。**这意味着该方向当前最实质的空白不是模型容量，而是“同一队列、同一终点、同一评测协议”下的系统比较**：生成式轨迹模型、判别式轨迹模型、蛋白/代谢评分与 PRS 各自报告增量，却少有头对头基准；跨祖源、跨编码系统、跨 EHR 通路的可复现性也尚缺统一框架 [46][1]。

## 2 方法学


### 2.1 生成式疾病轨迹模型

在纵向 EHR 上学习疾病轨迹的生成式模型，近两年沿着「更大规模、更多模态、更强干预能力」三条线推进。与之互补的是 **ALADYNOULLI**：它不把疾病孤立处理，而以「概率的混合」而非「混合的概率」形式联合建模纵向诊断、年龄与多基因风险，在三个生物库 **n>683,000**、随访 52 年、348 种疾病上识别出 **21 个可复制特征**，跨队列组成保留中位 **80%**，基于特征的 GWAS 发现 **151 个全基因组显著位点**，包括单性状分析遗漏的心血管关联 [1]。两者的差异在于证据来源：前者以预测与模拟为主，后者把遗传层纳入生成框架以支撑发现。

在数据形态上，Foresight 强调 EHR 中约 **80%** 的信息以自由文本存在，因而同时整合自由文本与结构化格式，覆盖 **18 类 SNOMED 概念**并支持日/周/月不同时间分辨率，但作者明确其当前形式不宜直接用于临床决策支持 [2]。**NOAH** 进一步走向多模态与任务无关：基于 MIMIC 家族 **559M 事件、299,000 患者**，原生处理图像、时序、分类与文本，采用双向时间整合与变分隐空间，支持自回归预测、零样本分类与反事实干预模拟 [3]。规模化的极端案例是 **Foresight-England**，243M 参数解码器在约 **6100 万人**去标识化纵向 EHR 上从头训练，但因 NHS England 暂停数据访问，定量结果无法导出，仅留下分词、架构、训练与评估的方法学模板 [4]——这本身提示国家级生成式模型的可复现性受数据治理约束。

从「预测」走向「决策」的代表是 EHR-MPC：它把脓毒症治疗优化重构为推理时控制问题，先训练生成式 EHR 患者数字孪生预测干预下轨迹，再用模型预测控制在推理时规划治疗；在 8 家医院多中心 ICU 队列上离线策略性能与强化学习基线相当、模拟性能更优，但仿真评估与真实临床仍有差距 [5]。**LifeLong Digital Twin** 则提出把 Life Events 组织为每日 Health States 并累积为 Lifelong Health Context 的统一范式，配套 Agent Harness 整合多模态证据，在 25 个疾病终点、3 类任务、4 个语言模型上，16 个模型-读出比较全部优于无 Context/Harness 的基线，疾病识别 F1 从 **0.422** 升至 0.504（Context）、0.515（Harness），相对增益 **19.4%、22.0%**；但作者自陈缺乏配对不确定性、疾病支持计数与组件消融，未确立统计显著性 [6]。

亚型与分型是另一条与生成式轨迹交叉的子问题，且方法上多为「表示学习+聚类」而非纯生成。VADeSC-EHR 用 Transformer 变分自编码器结合 Weibull 混合生存分布，把风险建模与聚类直接整合，以识别兼具不同诊断轨迹与时间-事件特征的患者亚群，局限在于聚类数需预设、外部验证有限 [47]。在神经退行性疾病上，一项工作将诊断前时间戳 EHR 按就诊、年龄与日历年标记化，用 Transformer 生成患者嵌入后 K-means 聚类，在 CPRD Aurum 与 UK Biobank 逾 **100,000 患者**中为 AD 和 PD 各识别出 **5 个可重复亚型**，5 年随访显示亚型间死亡与住院预后差异并与基因型关联，但外部验证仅限 UK Biobank、生物学机制仍待验证 [7]。值得注意的是，这类工作与 ALADYNOULLI 都声称能揭示「诊断类别内的生物学亚型」，但前者依赖无监督聚类、后者依赖贝叶斯生成框架与遗传关联，二者对亚型可信度的证据标准并不一致，尚缺直接对照。此外，面向早期预警的 LightGBM 轨迹模型在 All of Us **297,861 人**、12 项生物标志物 3 年轨迹上 AUROC **0.797** 优于静态汇总 **0.755**（P<0.001），匹配分析 **0.727 vs 0.680**，并可提前 3–12 个月持续预测（AUROC 0.768–0.740），说明即便非生成式方法，轨迹特征本身也携带独立信号 [8]；MiGHT-EHR 则以异构图 Transformer 加多任务学习在 MIMIC-III/IV 四任务上平均超越 SOTA，表征可按结局聚类、医学概念可线性恢复 [48]。这些结果与生成式路线构成方法学竞争：生成模型提供模拟与干预能力，判别式轨迹模型在特定终点上仍有强基线表现，二者尚未在同一队列、同一终点上被系统比较。

### 2.2 多组学与遗传整合

多组学与遗传整合的第一条主线是把遗传关联从“位点—表型”推进到“位点—分子—表型”的链条。UK Biobank Pharma Proteomics Project 对 **54,219** 名参与者检测 **2,923** 种血浆蛋白，发现 **14,287** 个主要遗传关联，其中 **81%** 为既往未报道，并精细映射出 **29,420** 个独立信号 [9]。同一队列的罕见变异分析在 **49,736** 人中识别 **5,433** 个罕见基因型—蛋白关联，**81%** 未被既往 GWAS 检出，基因水平另有 **1,962** 个关联，STAB1/STAB2 分别关联 **77** 和 **41** 个蛋白 [37]。两项工作共同说明常见与罕见变异对血浆蛋白组的贡献高度互补，但均以欧洲裔为主，非欧洲裔样本量很小（AMR 仅 **97** 人）[9]。

蛋白组图谱把上述遗传调控信息与疾病终点连接起来。基于 **53,026** 人、**2,920** 种蛋白的图谱报告 **168,100** 个蛋白—疾病关联和 **554,488** 个蛋白—性状关联，**183** 种疾病的判别 AUC **>0.80**，并通过 pQTL 确定 **474** 个因果蛋白 [10]。在 2 型糖尿病方向，全基因组 T2D PGS 关联 **648** 个蛋白、其中 **617** 个复制，分区 PGS 则指向不同生物过程的蛋白 [40]。这些结果支持“PGS→蛋白→疾病”的机制解析路径，但因果推断依赖 MR 假设，且主要基于欧洲人群 [40]。

方法学上，蛋白比值 GWAS 提供了检测蛋白互作的新角度：在 **1,463** 种 Olink 蛋白、**54,000** 余样本中复制 **4,248** 个 rQTL，覆盖 **2,821** 个蛋白对，显著 p-gain 蛋白对富集已知互作 **7.6** 倍，比值 GWAS 较单蛋白 GWAS 新增 **24.7%** 遗传信号 [49]。更上游的调控层面，MHC 区多祖先 pQTL 映射在 **2,920** 个蛋白中鉴定 **13** 个 cis、**606** 个 trans 关联，多数跨祖先一致，同时发现东亚人群 EDAR 的祖先富集关联 [50]；cis-by-trans 上位效应分析则识别出以 **ABO** 为中心的稳健互作网络 [51]。非加性效应同样不可忽略：在最多 **399,943** 人中，约**三分之一**同源基因—蛋白关系呈非线性剂量效应，正交等位基因重编码在 HWE 偏离下保持校准（λGC=**0.94**），而标准重编码膨胀至 **78.3** [52]。

结构变异与重复序列是蛋白组遗传力的另一来源。利用长读长组装参考面板在 **54,306** 人中插补 **54,578** 个 SV 和 **15,826** 个 VNTR，二者共同解释蛋白丰度遗传力约 **8.0%**，**123** 种蛋白主要由 SV 驱动，并鉴定 **8,065** 个 SV—蛋白和 **4,101** 个 VNTR—蛋白独立关联 [11]。这与常见/罕见 SNV 主导的关联图谱形成互补，提示仅用 SNV 会系统性低估蛋白组的遗传架构。

代谢组方面，UK Biobank **118,461** 人、**249** 个 NMR 指标的图谱覆盖 **700** 多种疾病的患病、发病与死亡关联，并在 THL Biobank **3** 万余人重复验证 [38]；跨国研究在 **700,217** 人中用 **36** 个临床验证代谢标志物训练 **12** 种疾病的 Cox 评分，实现跨三库重复 [39]。MetabHub 进一步把 **251** 项 NMR 代谢物、**129** 项临床指标、**54** 项环境暴露与 **57** 种新发疾病整合，支持性别特异关联与中介分析 [53]。代谢组评分与 PGS、临床评分的比较显示其可同时分层多种疾病风险，但 NMR 主要捕获高丰度分子，且以欧洲裔为主 [38]。

暴露组与遗传的相对贡献是本节争议较集中的问题。UK Biobank 暴露组全关联在 **492,567** 人中识别 **25** 个与死亡和蛋白组衰老时钟相关的独立暴露，并报告暴露组对死亡和 **25** 种年龄相关病的解释度常高于基因组 [12]。但该结论来自观察性设计，存在残余混杂与暴露测量误差 [12]。蛋白组能否稳定捕捉暴露也受到检验：All of Us **10,043** 人、**5,416** 种蛋白的分析显示蛋白暴露特征跨人群基本一致，仅 **<1%** 蛋白存在显著异质性，BMI 为例外、瘦素异质性最高 [54]。G×E 方向则提示方法学陷阱：在 **32** 个表型中，幂变换可解释 **45%** 的多基因评分 G×E 信号，许多信号实为另一尺度上的加性效应 [55]；fastGxE 声称控制多基因效应与噪声异质性并实现 **32.98** 倍以上加速 [56]，但另一条目未给出建模细节与定量结果 [57]。

多基因评分的跨祖源迁移是整合遗传信息用于人群健康的核心瓶颈。GBMI 覆盖 **23** 个生物样本库、**220** 万人、**14** 个疾病终点，指出祖先代表性仍不均 [58]；方法比较显示 **PRS-CS** 总体优于 P+T，欧洲 LD 面板精度相当或更高，原因仍是参与者以欧洲祖源为主 [59]。All of Us **245,388** 例全基因组序列与 UKB 联合开发的 **32** 个性状多血统 PRS 显示，增加多样性提升部分性状精度，但最大化样本量并非普遍最优，PRS 精度随血统分歧线性下降、多血统训练可减缓 [13]。汉族人群 TPMI **463,447** 人的全表型 GWAS 与 PRS 建模在 TWB、UKB、All of Us 验证，报告汉族特异 PRS 优于欧洲为主模型 [60]。这些结果一致指向“人群特异建模”，但各研究队列与性状不同，精度数字不可直接横向比较。

即使在同一人群内，PRS 的个体层面可靠性也存疑。在 AOU、PMBB、UCLA 三个生物库 **171,095** 人中对 **48** 个冠心病 PRS 的评估发现，群体水平表现相似的评分在个体层面一致性差（ICC 与 Light κ 低）[14]。这提示以群体 AUC 为唯一标准的评估不足以支撑临床决策，需要校准与个体一致性检验。

为提升 PRS 效力，多条路线并行。预训练 PRS 的自适应提升框架在模拟中各场景 R² 普遍优于基线，并控制 FDR、噪声选择比例 **<28%** [61]；表型填充把流体智力样本从约 **27** 万增至超 **45.5** 万，独立显著常见 SNP 关联由 **390** 增至 **550**，罕见变异分析鉴定 **26** 个显著基因 [62]；家族感知的 All of Us 基准则针对跨研究 PRS 性能不可比与亲属数据泄漏问题，将整个家族组分固定分配到发现、校准与测试集 [63]。三者分别从建模、表型扩充与评估设计入手，尚未在同一基准上直接比较。

把 PRS 分解为生物学过程是另一条解释性更强的路径。对 **526** 个 CAD 显著变异与 **78** 个 CAD 相关表型做潜在因子分解，识别出 **8** 个遗传组分（如富含胆固醇脂蛋白、脂蛋白(a)、内皮功能障碍、凝血等），据此构建的过程特异性 pPRS 能捕捉传统风险因素之外的生物学特征，并在 UK Biobank **458,905** 人中验证 [64]。类似地，**162** 个 PRS 与 **551** 个表型的关联图谱通过 **89,262** 次检验提示潜在因果，但作者强调 PRS 受水平多效性影响、关联不等于因果 [65]。

组学与遗传整合在药物靶点与疾病机制上的应用已有多类示范。脑龄差 GWAS 发现 **2** 个新位点和 **7** 个已知位点，整合 eQTL/pQTL 的 MR 与共定位优先 **7** 个可成药基因、重发现 **13** 种有临床试验证据的潜在药物 [66]；跨四队列 PheWAS 对 **19** 个候选靶点的检验表明可识别多效性并提示疗效或安全性信号 [67]；**35** 项血尿标志物的遗传分析发现 **5,794** 个独立位点、**51** 个因果关系，多 PRS 模型在 FinnGen 中改善慢性肾病、2 型糖尿病、痛风与酒精性肝硬化的风险分层 [68]。这些工作共同点是依赖 pQTL/eQTL 作为中介证据，差异在于是否做正式因果推断与外部验证。

多模态与多组学评分的整合正在从单一分子层走向联合建模。PULSE 在 UK Biobank 中从稀疏常规血检生成代谢组与蛋白质组，生成代谢组优于所有基准，生成蛋白质组对 **6** 种常见病 AUC 达 **0.72–0.83**，接近真实蛋白组数据 [36]。心血管方向在 UKB **50,673** 人中基于 **999** 种蛋白构建疾病特异评分，并在 PURE **9,358** 人验证，进一步整合 **2,279** 个多基因评分和 **479** 个 DNA 甲基化评分构建 **4** 种 MEGASCORE [69]。APOE4 致痴呆的中介分析则整合神经影像 **58,876**、蛋白组 **51,623** 与代谢组 **267,627**，区分共享与疾病特异中介通路 [70]。这些研究报告了整合框架与验证队列，但多数未给出可直接比较的增量性能数值。

自监督与基础模型开始进入基因型与多组学表征。SNPBERT 在 **485,923** 人基因型上用掩码 rsID 预训练，验证 MLM 损失 **0.435**、掩码 token 准确率 **78.5%**，UKB 子集 ARI **0.93**（PCA **0.92**），1KGP ARI **0.99**，微调后的疾病风险评分较传统 PRS 提供互补信息 [71]。但基因组基础模型在常见变异发现上的增益仍受质疑：在 **27** 个 UK Biobank 性状上，AlphaGenome 与 Borzoi 衍生注释的位点发现中位增益分别为 **1.8%** 和 **3.8%**，低于 baselineLD 的 **5.1%**，GPN-Star 甚至减少发现 [15]。这一冲突说明表征学习的价值可能更多体现在风险分层而非位点发现。

跨祖源与人群特异的遗传架构差异在多条证据中反复出现。All of Us 多组学 QTL 分析检出 **182,246** 个 QTL，**54,255** 个精细定位到罕见变异、其中 **59.4%**（**32,235** 个）解析为单一因果变异，罕见变异效应更易受祖源限制并富集于孟德尔疾病基因（OR=**1.4**）和获批药物靶点 [16]。APOE 在 **367,757** 人、六个祖源群体中测试 **2,632** 个表型，识别 **27** 个相关表型，**5** 个脂质性状女性效应更大、**9** 个关联具祖源特异性 [72]。克隆性造血比较中，MCPS 的 CH 显著少于 UKB（调整 OR=**0.59**，95% CI **0.57–0.61**），且 MCPS 内 CH 频率与欧洲祖源比例正相关（调整 beta=**0.84**）[73]。这些结果共同表明，把欧洲人群建立的遗传—组学关系直接外推存在系统性风险。

大规模关联资源与统计方法是上述整合的基础设施。FinnGen **176,899** 人的隐性关联扫描显示纯合子富集可提升隐性致病变异检出 [74]；CNV 全表型分析覆盖 **472,228** 人、**>3,000** 性状 [75]。这些资源的公开程度不一，跨祖源覆盖仍是共同短板。

### 2.3 医学 / EHR 基础模型

早期工作把结构化 EHR 当作“医学概念序列”来做自监督建模。**BEHRT** 用 Transformer 建模大规模诊断序列，结合就诊位置、年龄与事件顺序学习患者表示，在多种未来诊断预测任务中优于 Deepr、RNN、LSTM、RETAIN 等基线，但依赖编码质量、跨机构泛化与解释性仍有限 [33]。**Med-BERT** 进一步把 BERT 式预训练迁移到 ICD 诊断序列，先在大规模数据上自监督预训练再针对糖尿病、心衰等任务微调，与 BEHRT、G-BERT 及任务内训练模型比较显示预训练可提升性能，尤其在标注样本有限时；其局限是仅用诊断码、未纳入药物与检验 [34]。两者都把“预训练—微调”作为小样本场景的核心卖点，差别在于 BEHRT 强调序列结构与就诊上下文，Med-BERT 强调跨任务迁移。

跨机构、跨编码系统的迁移是后续工作的主要争议点。**GRASP** 用大语言模型把医学编码映射到共享语义空间，再结合 Transformer 预测 21 种疾病与全因死亡，在 UKB 391921、FinnGen 253991、Mount Sinai 386755 人的数据上，平均 ΔC-index 较语言无关模型在芬兰高 **88%**、美国高 **47%**，且 62% 疾病与多基因风险评分的相关性显著更高 [76]。与之不同，**SurvivEHR** 面向多长期病症共病，用竞争风险时间事件目标在英国初级保健 2300 万患者、76 亿编码事件上预训练，风险分层强并超越基准生存模型，但外部多国泛化未验证 [77]。另一条路线不直接预测结局，而是让 LLM 智能体自主生成并执行代码来查询多表 EHR，**EHRAgent** 在三个真实数据集上成功率最高超最强基线 **29.6%**，少样本即可完成复杂临床任务，代价是依赖代码执行反馈迭代 [78]。这些工作分别押注语义对齐、时间事件建模与工具化推理，尚未在统一基准上直接比较。

### 2.4 组学衰老时钟与纵向多组学动态

纵向多组学研究的核心增量在于把衰老从单时点“负荷”推进到“轨迹与速度”。在 335 名女性、8 年随访的全血队列中，**5,061 个基因和 181 个代谢物**随时间变化，且个体轨迹常偏离群体水平趋势，提示群体时钟可能掩盖个体异质性；这些纵向变化基因具细胞类型特异性并富集于心血管代谢与神经退行性疾病通路，同时受遗传、昼夜节律、季节和污染物影响 [79]。方法上，ARIC 研究用 FPCA 提取纵向蛋白成分、再以 Cox 弹性网训练，构建纵向蛋白组衰老指数 **LPAI**，在 MESA 验证，声称其同时捕捉衰老累积负担与变化速度，较单时点蛋白时钟提供额外预测信息 [80]。两条路线都强调纵向设计，但前者侧重描述分子轨迹的异质性，后者侧重构建可预测死亡、多病共存和衰弱的纵向指数，样本平台与随访间隔不同，不宜直接比较效应大小。

时钟的组学载体与器官粒度也在分化。UK Biobank 中基于 **107 个血浆非衍生代谢物**、274,247 人构建的 5 个器官特异性代谢组生物年龄 MetBAG，独立测试 Pearson r 为 **0.25–0.42**，关联 525 个疾病终点并预测 14 类疾病与死亡风险，作者自述预测相关性中等、代谢物覆盖有限 [81]。另一项工作对 409,206 名参与者的 14 个器官整合 NMR 代谢组、Olink 蛋白组和临床表型构建多组学器官时钟，关键论点是**年龄加速与死亡风险是器官生物学的不同维度**，具可分离的表型、分子和遗传结构 [82]。这与把“衰老程度”与“结局风险”视为同一标尺的时钟设计形成张力：前者提示时钟读数与风险预测可能并不等价。此外，基于 36 项常规临床指标的 PAI 用限制立方样条 Cox 捕捉 U 型关系，在 DFTJ 与 UK Biobank 中预测死亡、心血管病及 9 种慢性病风险，其优势在于低成本可迁移，但训练主要来自中国老年人、指标可受药物影响 [83]。

干预与节律两条证据则指向时钟的动态可塑性与混杂来源。UK Biobank 45,438 人分析中，较高体力活动与较低 **ProtAgeGap** 相关，ProtAgeGap 与 2 型糖尿病风险 HR=1.06、高活动交互 HR=1.05；12 周监督运动研究（26 名男性）中 ProtAgeGap 下降相当于 **10 个月**，但干预样本小、以观察性关联为主 [84]。这为“时钟可被行为干预逆转”提供了初步证据，然而不同研究间时钟构建与人群差异大，不能据此推断其他时钟同样可逆。另一项 UK Biobank 420,746 人、312 种血液分子的研究用贝叶斯加性回归树分离出相位偏移与节律紊乱两个正交指标，发现节律紊乱基本独立于睡眠，可独立预测 **98 种**未来发病风险并映射到肝脏代谢通路 [85]。这提示采血时间相关的节律扰动可能是纵向组学时钟的重要混杂或独立信号，而现有纵向时钟工作多未显式建模该维度，构成方法上的待解争议。

### 2.5 隐私保护合成基因组与生物样本库规模生成

针对生物样本库规模的无定相基因型数据，HELICS 提出了一种**潜空间流匹配**框架，用于在数十万至数千万相关 SNP 的超高维离散分布上进行条件合成基因组生成，目标场景包括隐私保护基准测试、模拟与数据增强，尤其面向代表性不足人群、罕见或失衡疾病队列及受限生物样本库 [17]。方法上采用染色体特异编码与多染色体潜空间流实现全基因组 SNP 级生成，并支持性状条件合成；实验数据覆盖 UKB 无定相基因型的 chr15 **18,784 个 SNP** 及全基因组 **600,336 个 SNP** [17]。

在与 HAPNEST、Sim1000G、HAPGEN2、GAN、RBM、HCLT 等基线的对比中，HELICS 在 chr15 及全 22 条常染色体基准上于 MAF、LD 和隐私代理指标上优于 HAPNEST 等基线，并能对多基因性状的遗传易感性进行条件控制 [17]。其局限在于低 MAF 变异 **R² 偏低**，且生成样本的 NN IBS 相似度较高，提示多样性有限 [17]。

## 3 数据与资源

大型前瞻性队列仍是人群健康多组学研究的骨架。**UK Biobank** 在2006–2010年招募**50万**名40–69岁参与者，收集基线问卷、体格测量、生物样本、影像、加速度计及健康记录链接数据，并预计20年随访可累积糖尿病约68,000例、心梗与冠心病死亡47,000例、卒中20,000例、阿尔茨海默病30,000例，从而支撑中老年复杂疾病遗传与非遗传决定因素的可靠评估[29]。该资源随后扩展为深度表型与遗传资源：对全部参与者完成基因型质控、群体结构与亲缘关系分析，估计单倍型并插补约**9600万**变异及11个HLA基因经典等位变异，通过身高GWAS和HLA-疾病关联复制验证数据质量[30]。最新进展是**490,640**名参与者的全基因组测序，平均覆盖**32.5×**，识别约**15亿**变异，较芯片插补增18.8倍、较全外显子测序增>40倍，其中93.5%为芬兰以外欧洲 ancestry[18]。不过该队列参与者相对健康、以欧洲 ancestry 为主，非欧洲样本仍有限[30][18]；其40–69岁年龄范围本身即为折中，可能影响暴露与结局的时序[29]。

与UK Biobank互补的是以多样性为目标的美国 **All of Us** 计划，拟招募至少**100万**人；截至2019年7月已有>175,000人贡献生物样本，其中**>80%**来自历史上生物医学研究不足群体，34个站点收集>112,000人的EHR数据[31]。该计划的数据来源并非单一：一项比较研究纳入393,590名参与者（患者介导EHR即PME 19,703人、提供者来源EHR即HPO 373,887人），发现PME人群更白、更女性、更多有保险、随访更长，而WGS覆盖更少（**35.2% vs 83.2%**），两种来源在疾病患病率、表型关联和已知基因型-表型关联复制率上存在差异[19]。这提示同一队列内部不同EHR通路的研究效用不可互换，PME样本量小且人群构成差异大也限制其泛化[19]。

隔离人群队列提供了另一类遗传发现资源。**FinnGen** 整合9个芬兰生物库与全国健康登记数据，基于**224,737**人插补基因型和**1,932**个终点开展GWAS与统计精细定位，发现芬兰隔离人群富集低频有害等位（0.1%≤MAF<5%），并能在既往研究充分的疾病中识别新的低频变异关联和可能因果编码变异[32]。其局限在于芬兰隔离人群遗传结构特殊，结果外推至其他人群受限[32]。国家层面，综述比较了UK Biobank、All of Us、新加坡PRECISE、Biobank Japan和韩国NPBBD-Korea等WGS生物样本库项目，指出WGS可发现罕见变异、结构变异和调控元件，但计算基础设施、隐私伦理、临床整合和祖先多样性不足仍是共同挑战[86]。

在关联结果的汇总与复用层面，**NHGRI-EBI GWAS Catalog** 截至2024年7月收录**625,113**条关联、>15.5K性状和>85K全基因组汇总统计数据集，通过EFO性状映射、祖源框架及与PGS Catalog互链提升可复用性；其限制是汇总统计标准化不足、非欧祖源仍偏少、依赖作者提交[42]。多基因风险评分的资源化以UK Biobank **PRS Release** 为代表，覆盖28种疾病和25种数量性状共53种性状，基准测试显示其优于**81个**已发表PRS并在其他队列验证，但主要基于UK Biobank人群，跨种族适用性有限[43]。可视化与扫描工具则降低了这些高维结果的使用门槛：**PheWeb** 整合Manhattan、LocusZoom和PheWAS视图，支持单性状与多性状切换，已用于UKB等数据集，但仅做可视化与共享、不含统计建模[87]；**PHESANT** 以规则算法为UK Biobank异质表型自动选择统计检验并输出图表，其自动化模型可能不适用于所有复杂表型[88]。

EHR表型与跨版本编码是另一条资源主线。**Phecodes** 基于ICD编码快速定义数千种临床有意义疾病的病例/对照状态，最初用于PheWAS，后扩展至表型风险评分等方法，但依赖ICD编码，可能存在编码误差和表型异质性[44]。针对ICD版本更替造成的纵向分析障碍，有研究构建了ICD-8到ICD-10的单向映射，覆盖完整ICD及丹麦本地扩展，可连接丹麦自**1965年**以来超半世纪的医疗数据，但未提供ICD-10回映射ICD-8[41]。在真实世界诊疗模式层面，基于爱沙尼亚**EST-Health-30** 30%随机人群样本的自动化框架将异质临床事件压缩为以诊断为中心的标准化摘要，形成覆盖**1000多个**ICD-10三位字符诊断类别的全国尺度数字图谱，其局限是回顾性观察且仅基于单一国家样本[89]。

组学数据自身的质量控制同样构成资源可用性的一部分。针对UK Biobank约**121,657**人NMR代谢标志物数据（168个标志物+81个比值，3,169个盲重复），研究识别了样本制备时间、运输板孔位、光谱仪批次与时间漂移等技术变异来源，多数标志物技术因素中位解释**1.5%**，盲重复中位CV **4.55%**、R² **0.928**，并发布ukbnmr R包；该流程仅覆盖约三分之一UKB参与者，且基于已校准浓度而非原始谱[45]。从更宏观的趋势看，综述指出大型人群队列正因高通量组学、EHR普及和AI而整合深度分子 profiling 与纵向真实世界数据，从描述性关联转向机制发现、精细风险分层与遗传导向的治疗开发，并日益全球化与多样化[46]；UK Biobank用于神经疾病研究的综述则称其已被**8000**余家机构使用、发表8000余篇论文，并强调人类遗传证据可提高药物研发成功率，同时提醒该队列以40–69岁为主、存在健康志愿者偏倚且部分神经疾病病例仍有限[90]。

## 4 应用与结果

在遗传关联发现层面，跨祖源分析显著扩展了可检测的关联集合。对 UK Biobank 多遗传祖源人群开展混合模型 GWAS 与跨祖源荟萃分析，覆盖 7,266 个性状，发现 **14,676 个仅欧洲祖源分析未发现的显著位点**，并公开汇总统计与质控框架 [20]。但该工作同时指出，多数关联仍主要见于欧洲祖源，解释需注意人群结构等 caveats [20]。多基因评分的跨祖源效能差异更为直接：多祖源 BMI 评分在 UK Biobank 欧洲裔中解释 **17.6%** 的 BMI 变异，其他人群从东亚裔美国人 16% 到农村乌干达 2.2% 不等 [21]；同一研究内，8 岁时加入 PGS 使解释方差从 11% 升至 21%，5 岁时预测 18 岁 BMI 从 22% 升至 35% [21]。

风险预测的时间维度上，不同研究一致显示遗传风险的重要性随年龄衰减，但对临床落点的判断存在差异。在 FOS 3,588 人与 UK Biobank 327,837 人中，CAD 的 PRS 风险比从 19 岁 **3.58** 降至 70 岁 **1.51**，40–45 岁组 PRS 显著优于 PCE，多 3.2 倍适宜 [22]。MSGene 则以年龄为时间尺度的多状态模型整合 CAD-PRS 与 EHR，跨 10 个心血管代谢状态估计年龄特异转移，相比 Framingham 30 年与 PCE 10 年模型可提供动态终身风险并评估他汀获益 [91]。两者都针对现有 10 年框架的不足，但前者侧重风险因素权重的时变比较，后者侧重状态转移建模，尚未见直接头对头比较。

蛋白质组学在多个疾病场景中带来一致的增量预测价值，但增益幅度有限且受表型定义制约。在 UK Biobank 中整合传统风险因素、PRS 与 202 蛋白评分后，CAD 内部验证 AUC 从 **0.750 升至 0.789**，外部验证从 0.717 升至 0.762，9 蛋白面板即可捕获大部分预测信息 [23]。跨 15 种疾病的 Olink 蛋白组模型平均 AUC 达 **0.74**（范围 0.56–0.89），较仅用临床因素平均提升 ΔAUC=0.03，且不依赖模型架构，简单模型如 L2 表现相当，跨队列泛化性受表型定义影响 [92]。在高血压人群中，2,911 种 Olink 蛋白经 Cox 筛选与 LASSO 构建蛋白风险评分，随访 15.1 年 1,074 人（6.66%）发生心衰，NT-proBNP 关联最强（HR=1.68），蛋白组学提升风险预测 [93]。骨质疏松方面，SHAP 筛选的少数标志物（FSHB、ADIPOQ、SOST、COL9A1、CHAD）模型优于全蛋白组模型 [94]。这些结果共同提示蛋白组学的价值更多体现在少数高信息蛋白而非全组学规模，但各研究疾病与队列不同，AUC 不宜直接横向比较。

代谢组学与多病共存研究则把焦点从单病预测转向跨器官轨迹。EPIC-Norfolk 中 >11,000 人、219,415 人年的非靶向代谢组学发现 640 个显著代谢物-疾病关联，其中 **420 个（65.5%）跨至少 2 种 NCD 共享**，涉及肝肾功能、脂糖代谢、低度炎症与肠道微生物等可干预通路 [24]。在 UK Biobank 代谢组学数据中，MVX 每 1-SD 的 HR=**1.213**、MetaboHealth HR=1.503，随访 8,876 人发病，提示代谢负担可补充传统风险因素 [95]。美国整合医疗系统 54,933 人中加入 250 个 NMR 代谢标志物后，9 个心血管-肾脏-代谢终点几乎全部判别能力提升，2 型糖尿病、慢性肾病与代谢功能障碍相关脂肪性肝病增益最大 [96]。心肾代谢共病方面，330,177 名 UK Biobank 参与者与 2,911 个血浆蛋白的多状态模型显示生物衰老可预测 CRM 进展，并识别关键中介血浆蛋白 [97]。

多模态与多病框架尝试把上述单病、单组学结果整合到个体层面。UKB-MDRMF 整合基本、生活方式、测量、环境、遗传与影像六类数据，联合建模 **1,560 种疾病**，优于单类别风险评估，并揭示风险因素-疾病及共病关联 [25]。PheMIME 则整合 VUMC、Mass General Brigham 与 UK Biobank 三大 EHR 系统的表型组多病共病汇总统计，实现跨系统共病网络交互可视化与疾病聚类推断，以精神分裂症为例展示跨系统网络生成能力 [98]。HFpEF 的多组学工作用监督分类器识别症状性 HFpEF 风险并在独立多中心队列验证，无监督聚类划分多组学亚型，结合可解释 AI 与通路分析揭示分子异质性 [99]。这些框架的共同局限是依赖单一生物库人群与表型定义，跨机构可比性仍是待解问题。

药物基因组学与亚组异质性构成应用谱系的另一端。利用 UK Biobank 与 All of Us 的 EHR 纵向用药与生物标志物数据，对 10 个药物-表型对（他汀 LDL-C、二甲双胍 HbA1c、降压药 SBP 等）做常见变异 GWAS 与罕见变异负荷检验，并在 All of Us 重复，证明疾病 PRS 可预测药效，同时指出用药与检测时点不齐、依从性与适应证混杂等纵向表型分析陷阱 [26]。痴呆风险预测中，43,759 名 UK Biobank 参与者按性别与 APOE ε4 分层后，APOE ε4 与痴呆关联存在性别差异（交互 p=0.027），携带者模型 AUC **0.85–0.90**，女性携带者最佳，关键分子预测因子呈亚组特异（女性 C7、CDON、EDIL3；男性 KLK4、MMP12、TGFBI）[100]。这与前述跨祖源 PGS 效能差异相呼应：无论是祖源、性别还是 APOE 分层，统一模型在亚组间的判别力并不一致，分层建模的必要性在多项证据中被反复提出，但各研究尚未在同一队列内系统比较分层与统一策略的净收益。

## 5 评测、可复现性与争议

在方法层面，面向大规模电子健康记录的生存分析已有可复现性相关的具体报告：**贝叶斯Cox回归**结合随机变分推断与似然重加权，使后验分布可因子化到子样本，从而支持**百万级数据点、数千时变协变量**的分析，并在模拟与 **UK Biobank 心肌梗死**应用中给出可行不确定性估计[27]。其评测以传统Cox模型实现为对照基准，但作者明确指出方法依赖变分近似、精度受子采样影响[27]——这构成精度与可扩展性之间的取舍争议：可行性证据来自单一应用场景，尚不足以判断该近似在更广泛人群与数据条件下的稳健性。

相比之下，共病研究方向的AI方法证据目前仅停留在综述层面，抽取字段显示其数据为电子健康记录文献综述、场景为共病研究，且明确标注“仅摘要信息，无具体方法细节”、具体方法与结果不详[28]。因此该方向尚无可用于评测对比的模型、数据集或核心数字，与上述生存分析方法在证据完备性上形成明显落差，也提示该子领域的可复现性讨论缺乏可核验的实证基础。

## 6 空白与趋势

在「空白与趋势」层面，现有证据最一致的信号是：**方法能力已经跑在评估与治理前面**。生成式 EHR 模型从 Delphi-2M 的 UK Biobank 训练—丹麦登记验证 [35]、Foresight 的多院区 SNOMED 概念预测 [2]，推进到 Foresight-England 的约 6100 万人国家级训练 [4] 与 NOAH 的 559M 事件多模态患者旅程 [3]，但 Foresight-England 因数据访问暂停而无法导出定量结果 [4]，Foresight 作者亦明确当前形式不宜直接用于临床决策支持 [2]。**规模扩张与可复现性、临床可用性之间尚未建立同步的评测契约**，这是本方向最结构性的一处空白。

1. **跨队列、同终点的生成式 vs 判别式头对头基准缺位。**「生成能力」目前无法被折算成可比较的预测增益。**

2. **亚型可信度的证据标准不统一，且缺直接对照。三者对「亚型为真」的判据分别是遗传关联、PRS 分化与生存轨迹差异，**尚无工作在同一数据上并列检验这些判据的一致性**。

3. **组学时钟的「读数」与「风险」是否等价，是尚未收敛的争议。** 多组学器官时钟工作明确主张年龄加速与死亡风险是器官生物学的不同维度、具可分离的表型与遗传结构 [82]，而 MetBAG 报告独立测试 Pearson r 仅 0.25–0.42、作者自述预测相关性中等 [81]；纵向蛋白组 LPAI 声称同时捕捉累积负担与变化速度 [80]，335 人 8 年随访则显示个体轨迹常偏离群体趋势、群体时钟可能掩盖异质性 [79]。**把时钟读数直接当作结局风险代理的做法缺乏跨队列校准证据**；此外采血时间相关的节律紊乱可独立预测 98 种未来发病 [85]，而现有纵向时钟多未显式建模该维度。

4. **跨祖源外推的系统性风险已被反复量化，但「人群特异建模」缺少统一评价协议。** 多祖源 BMI 评分在欧洲裔解释 17.6% 变异，其他人群从东亚裔美国人 16% 到农村乌干达 2.2% [21]；All of Us 多血统 PRS 显示最大化样本量并非普遍最优、精度随血统分歧线性下降 [13]；汉族 TPMI 463,447 人报告汉族特异 PRS 优于欧洲为主模型 [60]；UK Biobank 多祖源分析新增 14,676 个仅欧洲祖源未发现的位点 [20]。但各研究队列与性状不同，**精度数字不可横向比较，领域尚无跨祖源 PRS 的公共基准与报告规范**。

5. **个体层面的一致性与校准被群体 AUC 掩盖。** 三个生物库 171,095 人、48 个冠心病 PRS 的评估显示群体表现相似的评分在个体层面一致性差（ICC 与 Light κ 低）[14]；家族感知的 All of Us 基准则针对跨研究 PRS 性能不可比与亲属数据泄漏，将整个家族组分固定分配到发现、校准与测试集 [63]。**「群体判别力达标即临床可用」的隐含假设尚未被系统性证伪或修正**，校准与个体一致性的报告仍属少数派。

6. **多组学整合的增量性能普遍缺少可比的量化口径。** PULSE 从稀疏血检生成蛋白组对 6 种常见病 AUC 0.72–0.83、接近真实蛋白组数据 [36]；心血管方向整合 2,279 个 PRS 与 479 个甲基化评分构建 4 种 MEGASCORE [69]；APOE4 致痴呆的中介分析整合神经影像 58,876、蛋白组 51,623 与代谢组 267,627 [70]。这些工作多报告框架与验证队列，**但「多组学相对单组学/临床模型的增量」缺乏统一基准与消融规范**，与蛋白组学单病场景中 ΔAUC=0.03 量级的谨慎结论 [92] 难以对接。

7. **生成式模型用于遗传数据合成刚起步，隐私—效用权衡未定。** HELICS 以潜空间流匹配在 UKB 无定相基因型 chr15 18,784 SNP 与全基因组 600,336 SNP 上生成条件合成基因组，在 MAF、LD 与隐私代理指标上优于 HAPNEST 等基线，但低 MAF 变异 R² 偏低、生成样本 NN IBS 相似度较高提示多样性有限 [17]。**面向代表性不足人群与罕见病队列的数据增强尚缺下游任务验证**（如增强后 PRS 或关联发现的实际增益）。

8. **纵向 EHR 的编码 harmonization 与表型定义仍是跨队列复现的隐性瓶颈。** ICD-8 到 ICD-10 的单向映射可桥接丹麦自 1965 年以来的数据，但不提供反向映射 [41]；Phecodes 依赖 ICD 编码、存在编码误差与表型异质性 [44]；All of Us 内部 PME 与 HPO 两种 EHR 通路在患病率、表型关联与已知基因型—表型关联复制率上存在差异，WGS 覆盖 35.2% vs 83.2% [19]。**同一队列内部通路尚不可互换，跨队列「可复现」的声明需要更细的溯源报告。**

9. **共病结构的 AI 方法缺乏统一评测框架。** 综述层面已梳理 EHR 共病研究的 AI 方法 [28]，但仅有标题信息、具体方法与结果不详，本身即反映该子领域**系统比较与基准的稀缺**；ATM 的跨库验证  与 ALADYNOULLI 的三库应用 [1] 是目前少见的跨队列证据，但覆盖的疾病词汇与随访结构不同。

综合看，趋势是清晰的：队列从 UK Biobank 的 50 万人 [29] 与 490,640 人 WGS [18]、All of Us 的百万级多样化招募 [31]、FinnGen 的 224,737 人隔离人群设计 [32]，走向多组学深度表型与纵向真实世界数据整合，并从描述性关联转向机制发现与精细风险分层 [46]。**空白不在「能不能建模」，而在「如何证明模型在另一人群、另一编码体系、另一时间尺度上仍然成立且个体可用」**——这需要公开基准、统一消融与校准报告，而目前这些要素分散在各篇工作中，尚未形成领域共识。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 生成式疾病轨迹模型 | **朝阳** | Foresight 用生成式预训练 Transformer 建模患者时间线 [2]，2025 年 Nature 工作把生成式 Transformer 用于学习人类疾病自然史 [35]，两篇均为近两年高影响力工作，说明范式已从「预测单病」转向「生成轨迹」；但同节还有纵向生存聚类的深度表征学习 [47] 与贝叶斯纵向 EHR+遗传框架 [1]，方法路线（生成式 vs 表征聚类 vs 贝叶斯）尚未收敛，且中位引用仅 1，属早期爆发。 |
| 2.2 多组学与遗传整合 | **成熟** | UK Biobank 血浆蛋白组-遗传-健康关联图谱 [9] 与外显子测序 45 万人分析 [101] 已把「大队列 + 多组学 + 遗传」的关联发现做成标准范式；方法侧混合模型关联 [102] 与 35 项血尿标志物遗传学 [68] 表明统计工具已收敛、以增量和图谱扩展为主。 |
| 2.3 医学 / EHR 基础模型 | **成熟（方法层）/ 证据偏薄** | Med-BERT [34] 与 BEHRT [33] 确立了结构化 EHR 预训练范式，后续 EHRAgent [78] 与 LLM 提升 EHR 模型可迁移性 [76] 属增量改良；但雷达样本仅 5 篇、CNS 占比 0，说明该节证据覆盖不足，判断需谨慎。 |
| 2.4 组学衰老时钟与纵向多组学动态 | **朝阳** | 多器官代谢组生物学年龄关联心脏代谢疾病 [81] 与纵向蛋白组衰老指数预测死亡/多病 [80] 显示「组学时钟 → 人群健康结局」验证正在成规模出现；运动逆转蛋白组衰老 [84] 提示可干预性验证起步，但中位引用仅 3、方法未统一，处早期。 |
| 2.5 隐私保护合成基因组与生物样本库规模生成 | **证据不足** | 仅 1 篇 HELICS 生物样本库规模条件合成基因组 [17]，无法判断阶段。 |
| 3 数据与资源 | **成熟** | UK Biobank 资源描述 [29] 与深度表型+基因组数据 [30]、FinnGen [32]、All of Us [31] 构成稳定基础设施，属被反复引用的成熟底座。 |
| 4 应用与结果 | **朝阳** | 疾病轨迹深度学习预测胰腺癌风险 [103] 与血浆代谢物刻画非传染性多病通路 [24] 展示应用层已出高影响力结果；Pan-UKB GWAS [20] 与 BMI 多基因预测生命周期 [21] 说明应用正快速扩展但未定型。 |
| 5 评测、可复现性与争议 | **证据不足** | 仅 2 篇（贝叶斯 Cox 大规模推断 [27]、共病 AI 方法综述 [28]），且均非专门评测框架，不足以判断阶段。 |

**整体判断**：该方向整体处于**朝阳期偏早**——生成式轨迹建模与组学衰老时钟两条线在近两年出现 Nature 级工作 [35][81]，但方法路线未收敛、评测与跨队列复现证据几乎空白（第 5 节雷达样本仅 2 篇）。**窗口期约 1–2 年**：一旦生成式轨迹模型与 pQTL/蛋白组图谱被少数团队固化为基准，后来者只能做增量。最大不确定性是**跨队列可复现性与评测缺失**——UK Biobank 单队列结论能否在 All of Us / FinnGen 复现尚无系统证据，且隐私约束下合成数据路线仅 1 篇探索 [17]。

**接下来怎么做**：
1. **把衰老时钟接到生成式轨迹上**：用 UK Biobank 血浆蛋白组 + EHR 纵向数据，训练「蛋白组年龄 → 疾病轨迹」的条件生成模型，产出可解释的加速衰老-共病路径。现在做是因为两条线各自已有强证据 [9][35] 但尚未打通，交叉点空白。
2. **做跨队列复现基准**：以 UK Biobank 训练、All of Us / FinnGen 外部验证多基因与蛋白组风险模型，产出可复现性评测框架。第 5 节证据几乎为零，先做即占位；数据资源成熟 [31][32]。
3. **结合类器官多组学做机制锚定**：用人群 pQTL/蛋白组关联 [9] 筛选候选蛋白，在类器官模型中做扰动验证，把人群关联转成因果线索——这是博后合作项目的天然接口，且能规避纯关联研究的审稿质疑。
4. **切入纵向多组学动态建模**：用重复采样蛋白组/代谢组做纵向衰老指数与多病预测 [80][47]，方法上把生存聚类与生成式结合，产出方法学新意而非单病评分改良。
5. **用公共数据做 demo 建立方法信誉**：先在 UK Biobank 公开字段 + Pan-UKB GWAS 汇总统计 [20] 上复现 Foresight 类轨迹模型并公开代码，作为申请大队列数据与合作的敲门砖；避免落入「无公开数据无代码」的排除项。

## 参考文献

1. A Bayesian framework for longitudinal EHR and genetic discovery. Nature 2026. https://doi.org/10.1038/s41586-026-10780-5
2. Foresight—a generative pretrained transformer for modelling of patient timelines using electronic health records: a retrospective modelling study. The Lancet Digital Health 2024. https://doi.org/10.1016/s2589-7500(24)00025-6
3. NOAH: Learning the Full Patient Journey. A Longitudinal Multimodal Time-Aware Model for Representation and Forecasting.  2026. https://arxiv.org/abs/2609.09140
4. Foresight-England: Development of a National-Scale Generative AI Model of Electronic Health Records for Medical Event Prediction across the COVID-19 Pandemic.  2026. https://arxiv.org/abs/2608.16273
5. EHR-MPC: Inference-Time Control for Sepsis Treatment with Generative Patient Digital Twins. arXiv.org 2026. https://doi.org/10.48550/arXiv.2607.08793
6. LifeLong Digital Twin: A Unified Modeling Paradigm and Agent Harness for Event-Driven Lifelong Health State Trajectories.  . https://arxiv.org/abs/2610.05566
7. Subtyping Alzheimer's disease and Parkinson's disease using longitudinal electronic health records.. Nature aging 2026. https://doi.org/10.1038/s43587-026-01085-3
8. Predicting Early Functional Decline from Longitudinal Laboratory and Vital Sign Trajectories: A Large-Scale Study Using the All of Us Research Program.  2026. https://arxiv.org/abs/2608.21589
9. Plasma proteomic associations with genetics and health in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06592-6
10. Atlas of the plasma proteome in health and disease in 53,026 adults.. Cell 2024. https://doi.org/10.1016/j.cell.2024.10.045
11. A proteome atlas of structural variation and VNTR effects on complex traits and diseases.  . https://doi.org/10.64898/2026.09.26.26364064
12. Integrating the environmental and genetic architectures of aging and mortality.. Nature medicine 2025. https://doi.org/10.1038/s41591-024-03483-9
13. All of Us diversity and scale yield context-dependent improvements in polygenic prediction.. Nature Genetics 2026. https://doi.org/10.1038/s41588-026-02734-4
14. Evaluating Performance and Agreement of Coronary Heart Disease Polygenic Risk Scores.. JAMA 2025. https://doi.org/10.1001/jama.2024.23784
15. Genomic foundation models do not yet boost common variant discovery beyond standard functional annotations.  . https://doi.org/10.64898/2026.10.13.758880
16. Multi-omics in the All Of Us Research Program expands mapping genetic mechanisms in health and disease.  . https://doi.org/10.64898/2026.10.29.26366507
17. HELICS: Biobank-scale Conditional Synthetic Genome Generation via Latent Flow Matching.  . https://arxiv.org/abs/2610.36361
18. Whole-genome sequencing of 490,640 UK Biobank participants.. Nature 2025. https://doi.org/10.1038/s41586-025-09272-9
19. Robust replication of associations across patient-mediated and provider-sourced EHR data in the All of Us research program. npj Digital Public Health 2026. https://doi.org/10.1038/s44482-026-00032-8
20. Pan-UK Biobank genome-wide association analyses enhance discovery and resolution of ancestry-enriched effects.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02335-7
21. Polygenic prediction of body mass index and obesity through the life course and across ancestries.. Nature medicine 2025. https://doi.org/10.1038/s41591-025-03827-z
22. Dynamic Importance of Genomic and Clinical Risk for Coronary Artery Disease Over the Life Course. medRxiv 2023. https://doi.org/10.1101/2023.11.03.23298055
23. Machine Learning‐Driven Prediction of Coronary Artery Disease Risk Based on UK Biobank Plasma Proteomics. Journal of the American Heart Association : Cardiovascular and Cerebrovascular Disease 2026. https://doi.org/10.1161/JAHA.125.047248
24. Plasma metabolites to profile pathways in noncommunicable disease multimorbidity. Nature Medicine 2021. https://doi.org/10.1038/s41591-021-01266-0
25. UKB-MDRMF: a multi-disease risk and multimorbidity framework based on UK biobank data.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58724-3
26. Leveraging large-scale biobank EHRs to enhance pharmacogenetics of cardiometabolic disease medications.. Nature communications 2025. https://doi.org/10.1038/s41467-025-58152-3
27. Bayesian Cox regression for large-scale inference with applications to electronic health records. Annals of Applied Statistics 2021. https://doi.org/10.1214/22-aoas1658
28. From data to knowledge: artificial intelligence methods for studying comorbidity in electronic health records. The European Physical Journal Special Topics 2026. https://doi.org/10.1140/epjs/s11734-026-02571-w
29. UK Biobank: An Open Access Resource for Identifying the Causes of a Wide Range of Complex Diseases of Middle and Old Age. PLoS Medicine 2015. https://doi.org/10.1371/journal.pmed.1001779
30. The UK Biobank resource with deep phenotyping and genomic data. Nature 2018. https://doi.org/10.1038/s41586-018-0579-z
31. The “All of Us” Research Program. New England Journal of Medicine 2019. https://doi.org/10.1056/NEJMsr1809937
32. FinnGen provides genetic insights from a well-phenotyped isolated population. Nature 2023. https://doi.org/10.1038/s41586-022-05473-8
33. BEHRT: Transformer for Electronic Health Records. Scientific Reports 2019. https://doi.org/10.1038/s41598-020-62922-y
34. Med-BERT: pretrained contextualized embeddings on large-scale structured electronic health records for disease prediction. npj Digital Medicine 2020. https://doi.org/10.1038/s41746-021-00455-y
35. Learning the natural history of human disease with generative transformers.. Nature 2025. https://doi.org/10.1038/s41586-025-09529-3
36. Longitudinal alignments and syntheses of multimodal clinical data for personalized medicine with the PULSE framework. Nature Computational Science 2026. https://doi.org/10.1038/s43588-026-01026-5
37. Rare variant associations with plasma protein levels in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06547-x
38. Atlas of plasma NMR biomarkers for health and disease in 118,461 individuals from the UK Biobank. Nature Communications 2023. https://doi.org/10.1038/s41467-023-36231-7
39. Metabolomic and genomic prediction of common diseases in 700,217 participants in three national biobanks.. Nature communications 2024. https://doi.org/10.1038/s41467-024-54357-0
40. Identification of plasma proteomic markers underlying polygenic risk of type 2 diabetes and related comorbidities.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56695-z
41. A unidirectional mapping of ICD-8 to ICD-10 codes, for harmonized longitudinal analysis of diseases. European Journal of Epidemiology 2023. https://doi.org/10.1007/s10654-023-01027-y
42. The NHGRI-EBI GWAS Catalog: standards for reusability, sustainability and diversity.. Nucleic acids research 2025. https://doi.org/10.1093/nar/gkae1070
43. UK Biobank release and systematic evaluation of optimised polygenic risk scores for 53 diseases and quantitative traits. medRxiv 2022. https://doi.org/10.1101/2022.06.16.22276246
44. Using Phecodes for Research with the Electronic Health Record: From PheWAS to PheRS. Annual Review of Biomedical Data Science 2021. https://doi.org/10.1146/annurev-biodatasci-122320-112352
45. Quality control and removal of technical variation of NMR metabolic biomarker data in ~120,000 UK Biobank participants. Scientific Data 2021. https://doi.org/10.1038/s41597-023-01949-y
46. Trends in large-scale human population cohorts.. Trends in Genetics 2026. https://doi.org/10.1016/j.tig.2026.08.002
47. Deep representation learning for clustering longitudinal survival data from electronic health records.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56625-z
48. MiGHT-EHR: A Multi-task Graph Transformer for Heterogeneous Temporal Electronic Health Records.  2026. https://arxiv.org/abs/2608.06430
49. Genetic associations with ratios between protein levels detect new pQTLs and reveal protein-protein interactions. bioRxiv 2023. https://doi.org/10.1016/j.xgen.2024.100506
50. Multi-ancestry MHC-pQTL mapping reveals disease-linked HLA protein networks and shared genetic architecture.  . https://doi.org/10.21203/rs.3.rs-10956233/v1
51. Robust cis-by-trans epistasis in the human plasma proteome highlights an ABO-centered interaction network.. American journal of human genetics . https://doi.org/10.1016/j.ajhg.2026.09.003
52. Deviations from genetic additivity driven by rare variants at biobank scale.. Nature communications . https://doi.org/10.1038/s41467-026-76151-w
53. MetabHub: an integrative platform for plasma nuclear magnetic resonance metabolomics using mediation analysis, disease prediction, and risk stratification.. Nucleic acids research . https://doi.org/10.1093/nar/gkag1066
54. Proteomic Signatures Capture Environmental Exposures Across Diverse Populations.  . https://doi.org/10.64898/2026.10.06.26364311
55. Choice of phenotype scale is critical in biobank-based G × E tests.. Cell genomics . https://doi.org/10.1016/j.xgen.2026.101391
56. Genome-wide detection of genotype-environment interactions at biobank scale with fastGxE.. Nature genetics . https://doi.org/10.1038/s41588-026-02809-2
57. fastGxE is a powerful method for uncovering genotype-environment interactions in biobanks.. Nature genetics . https://doi.org/10.1038/s41588-026-02806-5
58. Global Biobank Meta-analysis Initiative: Powering genetic discovery across human disease. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100192
59. Global biobank analyses provide lessons for computing polygenic risk scores across diverse cohorts. medRxiv 2021. https://doi.org/10.1101/2021.11.18.21266545
60. Population-specific polygenic risk scores for people of Han Chinese ancestry.. Nature 2025. https://doi.org/10.1038/s41586-025-09350-y
61. A pre-train and fine-tune framework for adaptive boosting of pre-trained polygenic risk scores.. Nature communications . https://doi.org/10.1038/s41467-026-77128-5
62. Imputation of fluid intelligence scores reduces ascertainment bias and increases power for analyses of common and rare variants.. Nature genetics . https://doi.org/10.1038/s41588-026-02787-5
63. A family-aware All of Us benchmark for polygenic prediction and genomic machine learning.  . https://doi.org/10.64898/2026.10.22.26366229
64. Decomposing polygenic risk of coronary artery disease into distinct biological processes.  . https://doi.org/10.64898/2026.10.08.26365088
65. An atlas of polygenic risk score associations to highlight putative causal relationships across the human phenome. bioRxiv 2018. https://doi.org/10.7554/eLife.43657
66. Genetically supported targets and drug repurposing for brain aging: A systematic study in the UK Biobank.. Science advances 2025. https://doi.org/10.1126/sciadv.adr3757
67. Phenome-wide association studies across large population cohorts support drug target validation. Nature Communications 2018. https://doi.org/10.1038/s41467-018-06540-3
68. Genetics of 35 blood and urine biomarkers in the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-020-00757-z
69. Integrated multiomic scores for cardiovascular disease prediction across multiancestral populations.  . https://doi.org/10.64898/2026.10.23.26366372
70. Multimodal mediators connecting APOE4 to dementia.  . https://doi.org/10.21203/rs.3.rs-11445203/v1
71. Biobank-scale self-supervised genotype pretraining yields transferable representations for human genetics.. Nucleic acids research . https://doi.org/10.1093/nar/gkag1059
72. Phenome-wide and proteomic analysis of APOE alleles across different ancestries in the All of Us Research Program.  . https://doi.org/10.64898/2026.09.26.26364080
73. Comparative analysis of the Mexico City Prospective Study and the UK Biobank identifies ancestry-specific effects on clonal hematopoiesis.. Nature genetics 2025. https://doi.org/10.1038/s41588-025-02085-6
74. Mono- and biallelic variant effects on disease at biobank scale. Nature 2023. https://doi.org/10.1038/s41586-022-05420-7
75. Phenome-wide Burden of Copy Number Variation in the UK Biobank.. American Journal of Human Genetics 2019. https://doi.org/10.1016/j.ajhg.2019.07.001
76. Large language models improve transferability of electronic health record-based predictions across countries and coding systems.. NPJ digital medicine 2026. https://doi.org/10.1038/s41746-026-02363-5
77. SurvivEHR: a competing risks, time-to-event foundation model for multiple long-term conditions from primary care electronic health records.  2025. https://doi.org/10.1101/2025.08.04.25332916
78. EHRAgent: Code Empowers Large Language Models for Few-shot Complex Tabular Reasoning on Electronic Health Records.. Proceedings of the Conference on Empirical Methods in Natural Language Processing. Conference on Empirical Methods in Natural Language Processing 2024. https://doi.org/10.18653/v1/2024.emnlp-main.1245
79. Longitudinal dynamics of gene expression and metabolomics in an aging population cohort.. Science 2026. https://doi.org/10.1126/science.aed6452
80. A Novel Longitudinal Proteomic Aging Index Predicts Mortality, Multimorbidity, and Frailty in Older Adults.. Aging cell 2025. https://doi.org/10.1111/acel.70317
81. Multi-organ metabolome biological age implicates cardiometabolic conditions and mortality risk.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59964-z
82. Age Acceleration and Mortality Risk Constitute Distinct Dimensions of Organ Aging.  . https://doi.org/10.21203/rs.3.rs-10881849/v1
83. Estimation of physiological aging based on routine clinical biomarkers: a prospective cohort study in elderly Chinese and the UK Biobank.. BMC medicine 2024. https://doi.org/10.1186/s12916-024-03769-2
84. Reversal of proteomic aging with exercise-results from the UK biobank and a 12-week intervention study.. npj aging 2025. https://doi.org/10.1038/s41514-025-00318-w
85. Molecular Circadian Disturbance in Human Blood Independently Predicts Multi-Disease Risk and Maps to Hepatic metabolism Pathways.  . https://doi.org/10.21203/rs.3.rs-11120748/v1
86. Lessons from national biobank projects utilizing whole-genome sequencing for population-scale genomics.. Genomics & informatics 2025. https://doi.org/10.1186/s44342-025-00040-9
87. Exploring and visualizing large-scale genetic associations using PheWeb. Nature Genetics 2020. https://doi.org/10.1038/s41588-020-0622-5
88. Software Application Profile: PHESANT: a tool for performing automated phenome scans in UK Biobank. International Journal of Epidemiology 2017. https://doi.org/10.1093/ije/dyx204
89. A national-scale digital atlas of recorded care patterns across more than 1000 diagnostic categories using real-world health data: a retrospective observational study.  . https://doi.org/10.64898/2026.09.16.26363186
90. UK Biobank-A Unique Resource for Discovery and Translation Research on Genetics and Neurologic Disease.. Neurology. Genetics 2025. https://doi.org/10.1212/nxg.0000000000200226
91. MSGene: a multistate model using genetic risk and the electronic health record applied to lifetime risk of coronary artery disease. Nature Communications 2024. https://doi.org/10.1038/s41467-024-49296-9
92. Generalizability of proteomic risk prediction across biobanks reveals dependence on phenotype definitions.  . https://doi.org/10.64898/2026.10.01.26364038
93. Large-scale plasma proteomic profiling enhances prediction of heart failure among hypertensive individuals: prospective insights from the UK Biobank.. Journal of global health . https://doi.org/10.7189/jogh.16.04313
94. Explainable Plasma Proteomics–Based Machine Learning for Osteoporosis Diagnosis, Prognosis, and Protein Biomarker Discovery in the UK Biobank. The FASEB Journal 2026. https://doi.org/10.1096/fj.202600647R
95. MetaboHealth and Metabolic Vulnerability Index as Risk Factors for Cardio-Renal-Metabolic Multimorbidity: A Large-Scale Prospective Cohort Study.. Diabetes, obesity and metabolism 2026. https://doi.org/10.1111/dom.71112
96. NMR metabolomics for cardiovascular-kidney-metabolic risk stratification in an integrated healthcare system.  . https://doi.org/10.64898/2026.10.01.26364322
97. Proteomics mediates the effects of biological aging on the progression of cardio-renal-metabolic comorbidity: a UK biobank cohort study.. Cardiovascular diabetology 2025. https://doi.org/10.1186/s12933-025-03035-6
98. PheMIME: an interactive web app and knowledge base for phenome-wide, multi-institutional multimorbidity analysis.. Journal of the American Medical Informatics Association : JAMIA 2024. https://doi.org/10.1093/jamia/ocae182
99. Deep phenotyping of heart failure with preserved ejection fraction through multi-omics integration.. European journal of heart failure 2025. https://doi.org/10.1002/ejhf.70041
100. Sex shapes plasma molecular signatures of dementia risk across APOE ε4 strata.  . https://doi.org/10.64898/2026.11.02.26366836
101. Exome sequencing and analysis of 454,787 UK Biobank participants. Nature 2021. https://doi.org/10.1038/s41586-021-04103-z
102. Mixed model association for biobank-scale data sets. Nature Genetics 2018. https://doi.org/10.1038/s41588-018-0144-6
103. A deep learning algorithm to predict risk of pancreatic cancer from disease trajectories. Nature Medicine 2023. https://doi.org/10.1038/s41591-023-02332-5
104. Age-dependent topic modelling of comorbidities in UK Biobank identifies disease subtypes with differential genetic risk. Nature Genetics 2023. https://doi.org/10.1038/s41588-023-01522-8
105. Disease prediction with multi-omics and biomarkers empowers case–control genetic discoveries in the UK Biobank. Nature Genetics 2024. https://doi.org/10.1038/s41588-024-01898-1
106. Polygenic Prediction of Peripheral Artery Disease and Major Adverse Limb Events.. JAMA cardiology 2025. https://doi.org/10.1001/jamacardio.2025.1182
107. Systematic single-variant and gene-based association testing of thousands of phenotypes in 394,841 UK Biobank exomes. Cell Genomics 2022. https://doi.org/10.1016/j.xgen.2022.100168
108. Rare variant contribution to human disease in 281,104 UK Biobank exomes. Nature 2021. https://doi.org/10.1038/s41586-021-03855-y
109. Pan-UK Biobank GWAS improves discovery, analysis of genetic architecture, and resolution into ancestry-enriched effects. medRxiv 2024. https://doi.org/10.1101/2024.03.13.24303864
110. Exome sequencing and characterization of 49,960 individuals in the UK Biobank. Nature 2020. https://doi.org/10.1038/s41586-020-2853-0
111. An atlas of genetic associations in UK Biobank. Nature Genetics 2017. https://doi.org/10.1038/s41588-018-0248-z
112. Advancing human genetics research and drug discovery through exome sequencing of the UK Biobank. Nature Genetics 2021. https://doi.org/10.1038/s41588-021-00885-0
113. Plasma proteome analyses in individuals of European and African ancestry identify cis-pQTLs and models for proteome-wide association studies. Nature Genetics 2022. https://doi.org/10.1038/s41588-022-01051-w
114. Components of genetic associations across 2,138 phenotypes in the UK Biobank highlight adipocyte biology. Nature Communications 2019. https://doi.org/10.1038/s41467-019-11953-9
115. Sex differences in the genetic regulation of the human plasma proteome.. Nature communications 2025. https://doi.org/10.1038/s41467-025-59034-4
116. A fast and scalable framework for large-scale and ultrahigh-dimensional sparse regression with application to the UK Biobank. bioRxiv 2019. https://doi.org/10.1371/journal.pgen.1009141
117. GWAS of extended prescription analgesic use identifies genetic loci in chronic pain.. Nature communications 2026. https://doi.org/10.1038/s41467-026-71434-8
118. SPA<sub>GRM</sub>: effectively controlling for sample relatedness in large-scale genome-wide association studies of longitudinal traits.. Nature communications 2025. https://doi.org/10.1038/s41467-025-56669-1
119. Functional architecture of rare protein coding variation across 786,871 exomes.  . https://doi.org/10.64898/2026.10.16.26365771
