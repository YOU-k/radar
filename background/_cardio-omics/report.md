# 心血管队列多组学与临床 AI · 方向背景报告

证据 100 篇 · 覆盖度 0.66 · 第 10 轮 · 更新 2026-10-18 · 数字核验删句 9

## 本次变更

- 新增 [64] Decomposing polygenic risk of coronary artery disease into distinct biological processes

## 摘要（TL;DR）

- China-PAR 基于 4 个中国当代队列推导 10 年 ASCVD 风险方程，男性 C 统计量 0.794、女性 0.811，并与 ACC/AHA 指南 Pooled Cohort Equations 对比 [1]。
- QRISK3 在 UK Biobank 中系统性高估 CVD 风险，老年参与者高估达 20%，作者建议重新校准或开发定制模型 [2]。
- CKB 吴忠子队列与 JBPCD 验证中，糖尿病人群 C 统计量仅 0.584–0.629，重校准后区分度变化不大但校准显著改善 [3]。
- CHARLS 2011–2020 年 8080 名 ≥45 岁无基线 CVD 者中，十种机器学习模型里 GBM AUC 0.828 最高，但局限是单队列、缺乏外部验证 [4]。
- 开滦队列 16378 名中国 T2DM 患者中，ML-CVD-C 用功能主成分分析提取 4 年风险因子轨迹并纳入机器学习，整合纵向轨迹的模型优于仅用基线变量的模型，但限于单队列、需外部验证 [5]。
- UK Biobank 306654 人中评估 PRS 加入传统风险因素的判别与重分类增益，结论是 PRS 临床效用仍不确定、主要基于欧洲人群、建模依赖假设 [6]。
- Echo2HF 基于 MGH 4057664 段超声视频、70763 例患者开发，10 年内部 AUROC 0.83（95%CI 0.81–0.85）、外部 0.82（0.81–0.83），但仅回顾性、外部仅单中心 [7]。
- UKB 52,164 人、2,919 个蛋白的观察性分析中，636 个蛋白与任一 CVD 相关，MR 提示 47 个蛋白与 CVD 相关、18 个有共定位证据，但多数观察性关联并非因果 [8]。
- 在 41,931 人中开发 5–20 个蛋白的稀疏模型预测 218 种疾病 10 年发病，基础临床模型中位 C-index 为 0.64，67 种加 5–20 蛋白显著提升，中位 ΔC-index=0.07（0.02–0.31） [9]。
- 嘉道理生物库测试集 11.2 年随访中，最优 PRS 每 SD 对硬 CAD 的 HR 1.26，加入传统模型后 Harrell C 男性仅增 0.003、女性增 0.001，最高 NRI 3.2% [10]。

## 1 背景与定义

传统风险方程在中国人群中的推导与验证构成了这一方向的基础，但**方程设计高度依赖目标人群与可用变量，跨体系直接套用存在风险**——China-PAR 基于 4 个中国当代队列推导并在两个独立队列外部验证，SCORE2 采用性别特异、竞争风险调整的 Cox 模型并按欧洲四类风险区域重校准，QRISK3 则通过新增 HIV/AIDS、SLE、严重精神疾病等变量改进 QRISK2 [1]。外部验证反复暴露校准问题且方向并不一致：QRISK3 在 UK Biobank 中系统性高估 CVD 风险、老年参与者高估达 20% [2]；SCORE2 在荷兰族裔与社会经济多样化人群中按高危亚组调整后符合治疗资格人数几乎翻倍 [11]；CKB 吴忠子队列与 JBPCD 中糖尿病人群 C 统计量仅 0.584–0.629、原模型 E/O 在一般人群达 1.47–3.78 [3]；新西兰与中国 T2D 队列的跨国检验更显示女性每 10 年年龄风险比分别为 1.61 与 2.51，标准重校准未能改善中国队列校准 [12]。**这些结果共同界定了本方向的第一个核心问题：区分度增益不等于跨人群校准改善，外部验证与重校准是模型进入临床前的必要环节，而非可选项。**

机器学习与深度学习在区分度上普遍报告相对传统方程的增益，但增益幅度与验证强度差异明显。UK Biobank 473611 人、645 个候选变量建立的 UKCRP 含 10 个预测因子、AUC 0.762±0.010，但人群以白人为主（94.0%）、出血性卒中预测较差 [13]；AutoPrognosis 在同一数据库 423604 人、473 个变量上报告机器学习可整合大量变量与复杂交互，但受变量缺失严重与外部验证有限制约 [14]；CHARLS 8080 名 ≥45 岁中国人群、随访 9 年、77 个候选变量筛出 11 个预测因子，GBM AUC 0.828 为十种模型最优，但限于单队列、缺乏外部验证 [4]。**同一人群内报告的高 AUC 与跨队列外部验证的稳健性必须分开看待**，这是本方向从「模型开发」走向「模型可用」的关键分界。纵向轨迹与动态预测构成另一条独立路线：开滦队列 16378 名中国 T2DM 患者中，ML-CVD-C 用功能主成分分析提取 4 年风险因子轨迹并纳入机器学习，整合纵向轨迹的模型优于仅用基线变量的模型 [5]，但风险因子的变化信息是否应进入方程，目前只有单队列证据支持。

多组学与影像表型的增量价值证据正在积累，但**多停留在再分层而非替代临床评分**。UK Biobank 306654 人中评估 PRS 加入传统风险因素的判别与重分类增益，并用 CPRD 210 万人模拟按指南启动他汀的临床影响，结论是 PRS 临床效用仍不确定、主要基于欧洲人群、建模依赖假设 [6]；多族裔验证的 ASCVD-IRT 将 PRS 与 ASCVD-PCE 结合，NRI 白人 2.7%、黑人 2.5%、南亚 8.7%、西班牙裔 7.5% 但 CI 含 0，部分族裔样本小、CI 宽 [15]；脂质组学与基因组整合模型在 AusCVDRisk 路径上改善中间风险人群再分层，能正确上调未来事件并识别亚临床斑块负担者，但需前瞻性真实世界验证、脂质组学平台可扩展性受限 [16]；CMR 方面，UKBB 27254 人联合 15 个临床风险因子的可解释机器学习显示 CMR 表型可提升 MACE 预测，并在西安交大附二院 522 人超声队列做跨模态可迁移性评估，但超声替代 CMR 存在测量精度与定义差异、非直接外部验证 [17]。心衰与房颤专项模型提供了另一类对照：Echo2HF 基于 MGH 4057664 段超声视频、70763 例患者开发，外部 BWH 34802 例验证，10 年内部 AUROC 0.83、外部 0.82，数值上优于 PCP-HF 与 PREVENT，但仅回顾性、外部仅单中心 [7]；房颤方面 CHARGE-AF 合并 ARIC、CHS、FHS 共 18556 例推导、7672 例 5 队列验证，仅限白人/非裔、年龄 46–94 [18]，而基于多机构 EHR 的 412085 例 45–95 岁人群、14334 例新发 AF 的 5 年模型验证 C-statistic 0.777、校准 0.99，判别与校准优于 CHARGE-AF 的 0.753，但依赖编码、外部验证有限 [19]。**同一结局下数据源（影像 vs EHR vs 问卷变量）会实质改变可比性与结论**，这决定了多组学与影像 AI 在本方向中的定位应是临床评分的增量层，而非替代层。

血浆蛋白组遗传学的基础图谱已由 UK Biobank Pharma Proteomics Project 奠定：54,219 名参与者、2,923 个蛋白 pQTL 定位、14,287 个主要遗传关联、81% 为新发现，并揭示跨生物域的 trans pQTL、配体-受体相互作用与通路扰动 [20]；该资源以欧洲 ancestry 为主、非欧样本量小，这一局限贯穿后续多数分析 [20]。结构变异层面的解析进一步展开：利用长读长组装参考面板在 54,306 名 UK Biobank 参与者中插补 54,578 个 SV 和 15,826 个 VNTR，检测其对 2,923 种血浆蛋白丰度的影响，SV 和 VNTR 共同解释蛋白丰度变异遗传力的约 8.0%，鉴定出 8,065 个 SV-蛋白和 4,101 个 VNTR-蛋白独立关联 [21]。从关联走向因果推断，孟德尔随机化与共定位成为区分病因相关蛋白的核心手段：UKB 52,164 人、2,919 个蛋白的观察性分析中 636 个蛋白与任一 CVD 相关、126 个与 MI/IS/HF 三类结局均相关、118 个在中国慢性病前瞻性队列（1,937 人）复制，MR 提示 47 个蛋白与 CVD 相关、18 个有共定位证据，FGF5、PROCR 和 FURIN 等显示潜在因果性，但多数观察性关联并非因果 [8]；跨人群 MR 进一步将范围扩至非洲、东亚、欧洲人群，系统评估 2,922 个循环蛋白对 AF、CAD、HF、IHD、PAD 五类 CVD 的潜在因果作用，强调人群特异 pQTL 与跨人群一致性评估 [22]。**pQTL 资源、MR 与共定位的组合，构成了本方向「从预测标志物走向可干预靶点」的方法学骨架，但其跨 ancestry 可迁移性仍是未解约束。**

蛋白组对心血管风险的增量预测价值已在多个 UKB 子集中被反复检验，但**增益幅度与对照模型高度相关，不同子集与不同对照的数字不能直接横向比较**。41,931 人中开发 5–20 个蛋白的稀疏模型预测 218 种疾病 10 年发病，基础临床模型中位 C-index 0.64，67 种疾病加 5–20 蛋白显著提升、中位 ΔC-index=0.07（0.02–0.31）[9]；针对 MACE，38,380 人、2,919 蛋白的极端梯度提升分析显示 SCORE2 AUC 0.740，数据驱动选出的 114 个蛋白单独预测 AUC 0.758，与 SCORE2 联合升至 0.771（NRI 0.140），而随机选 114 个蛋白无改善 [23]；46,009 名无基线 CVD 者中可解释提升机蛋白组模型 AUROC 0.767、AUPRC 0.241，优于 PREVENT 等方程评分及多个 PRS，加入临床特征后升至 0.785 和 0.284 [24]；44,431 人、Olink 1,460 蛋白的研究构建 117 蛋白 ProtRS，C-index 0.769，优于 SCORE2 0.667、PREVENT 0.645、FRS 0.672，加入基线模型后 C-index 由 0.669 升至 0.774、ΔC=0.105 [25]。冠心病方向，基于 UKB 蛋白组与遗传数据（训练 32,330、内部验证 13,857、外部 5,775），LASSO Cox 推导 202 蛋白风险评分并以 CatBoost 整合，内部验证 AUC 从 0.750 升至 0.789，外部验证从 0.717 提升 [26]；51,859 人、中位 13.6 年随访发生 4,857 例 MACE 的分析中，NT-proBNP 每 SD 的 HR 为 1.68，蛋白模型在校准、NRI 和 C 统计量上优于 PREVENT [27]；房颤方面 UKB-PPP 51,680 人、1,459 蛋白开发的 165 蛋白 Lasso-Cox 评分每 SD 风险比 2.20，加入 CHARGE-AF、NT-proBNP 和多基因风险评分后 C 指数由 0.771 升至 0.816，并在 ARIC 11,012 人外部验证 [28]。**这些一致指向蛋白组在传统评分之上的增量信息，但泛化性与表型定义密切相关**：UKB 53,026 人中训练 15 种疾病模型，平均 AUC 0.74（范围 0.56–0.89），较仅用临床因素平均提升 ΔAUC=0.03，且不依赖模型架构，简单模型如 L2 表现相当 [29]。

代谢组与多基因风险评分构成与蛋白组互补的两条支柱，其跨人群可迁移性同样是核心争议。代谢组在 SCORE2 框架下被系统评估：UKB 10,257 例与 ESTHER 1,039 例、249 种代谢物选出 7 种，内部验证 C 指数从 0.660 升至 0.678（P=0.037），外部验证增 0.043（P=0.011）[30]；183,237 名 50–69 岁无 CVD/糖尿病者中 PUFA/MUFA 比值加入 SCORE2 使验证集（54,971 人）C 指数从 0.740 升至 0.744（P<0.001）、NRI 7.5%、IDI 0.025 [31]；54,933 名美国整合医疗系统参与者中检测 250 个 NMR 代谢标志物并评估 9 个心血管-肾脏-代谢终点，加入标准诊疗预测因子后几乎所有终点判别能力提升 [32]。PRS 方面，GPS_Mult 整合五个 ancestry 的 CAD GWAS（>269,000 病例、>1,178,000 对照）及十项危险因素，在 UKB 116,649 名欧洲 ancestry 个体训练、325,991 人独立验证，与患病 CAD 关联 OR/SD 2.14，与事件 CAD 关联 HR/SD 1.73，并在多族裔外部验证中优于所有既往 CAD 评分 [33]；然而在中国人群中，嘉道理生物库训练 28,490、测试 72,150 人，最优 PRS 每 SD 对硬 CAD 的 HR 仅 1.26，加入传统模型后 Harrell C 男性仅增 0.003、女性增 0.001，最高 NRI 3.2%，对软 CAD 改善极小或无改善 [10]。**PRS 的跨人群可迁移性不足，是中国与东亚队列在本方向中必须独立建模而非直接移植欧洲评分的直接依据**；跨祖源可靠性问题也在方法学层面被处理，UKBB T2D 19,468 人及 ADVANCE 试验中 Mondrian 交叉共形预测可控制预设错误率并识别不可可靠预测个体 [34]。

ECG 与影像 AI 是本方向中证据最密集、也最能体现「AI 与队列结局联合」的子领域，但其证据结构呈现明显的**内部性能乐观、外部验证收敛**特征。窦性心律 ECG 预测新发房颤方面，Mayo Clinic 早期工作用 CNN 从 10 秒 12 导联窦律 ECG 识别房颤电信号特征 [35]；Geisinger 以 280 万份 ECG 为池、保留 160 万份/43.1 万人建模，回顾性模拟部署后发现无房颤史且发生房颤相关卒中的患者中近三分之二在卒中前被预测为高风险 [36]；退伍军人队列纳入 907858 份 ECG、平均年龄 62.4 岁、男性 93.6%，在 2 个 VA 网络训练、另 4 个 VA 及 1 个非 VA 中心测试，预测 31 天内 AF [37]；FHS 用 10,097 人 28,151 份 ECG 优化 ECG-AF 并与 CHARGE 评分比较，报告中等区分度 [38]。但一项 3 中心、4017 例 65 岁以上无房颤史患者的研究，按预设敏感性 20%、特异性 85% 评估，模型判 391 例高风险其中 74 例发生房颤，敏感性仅 31%（95%CI 25–37），作者明确指出单机构评估常高估性能 [39]。**部署场景与阈值选择会显著改变可检出比例，这是 ECG-AI 从回顾性模拟走向筛查闭环时最直接的约束。** 心衰方向，YNHHS、UKB、ELSA-Brasil 多国队列中 AI-ECG 阳性者新发心衰风险高 4 至 24 倍，C 统计量 0.718/0.769/0.810，对照为 PCP-HF 方程 [40]；结构性心脏病方面，美国大型医疗系统开发的集成模型在伊朗三级中心 879 例 ≥45 岁高危门诊患者中前瞻验证，检测 LVSD、瓣膜病与严重 LV 肥厚 [41]。左房结构功能是 ECG 与影像交叉的典型切口：UKB 48,300 名配对参与者上训练，LAVmin/LAVmax 相关 r=0.50、LAEF r=0.40，与 CMR 仅中等相关，却与新发房颤、卒中、心衰独立相关，且在 14 天监测中预测房颤优于现有工具和 NT-proBNP [42]。**ECG 捕捉的是与影像中度相关的电学替代标记，而非影像测量本身**，这一判断决定了 ECG-AI 在多组学联合中的角色是低成本、可规模化的初筛层。

多模态与基础模型正在把 ECG 与 CMR、超声、EHR 联合，并逐步把「单模态性能」推进到「跨模态增量」。CARDIAC-FM 用对比学习在 UKB 57,609 对 ECG-CMR 样本上训练，在 CHS 与 MESA 外部验证，报告持续优于单模态并可在无 MRI 时仅用 ECG 部署 [43]；ECG 与超声心动图的多模态基础模型用 129424 例超声视频 4391610 段、配对 1094656 份 ECG（53876 人），测试集 LVSD 分类 AUROC 0.94，优于单模态 [44]；ECG-LFM 用 1157 万份 12 导联 ECG、197.9 万人预训练，在 PTB-XL、Chapman、CODE-15、CPSC-2018、UKB 外部测试，平均 AUROC 0.930，并经 PheWAS 关联 167 个心功能因子、GWAS 发现 11 个位点 12 个 SNP [45]；ECG-FM 用 140 万 ECG 片段预训练并在 UHN-ECG 外部机构验证多标签解读与降低 LVEF 预测，公开权重、代码与基准 [46]。**基础模型路线的共同短板是可解释性有限、预训练数据以公开集或单机构私有数据为主**，这与本方向对「机制解释与临床可行动性」的要求之间存在张力。**外部 C-index 相对内部下降是这类工作的共同特征** [47]，这与前述风险方程的外部校准问题在方法学上同源。

中国与东亚队列在本方向中的定位，目前更多体现为「开发—迁移验证」的路径尝试，而非已闭环的筛查—干预证据。ChinaHEART 全国社区队列的巢式病例对照研究使用 MSD 平台检测 28 种血浆蛋白，识别与新发颈动脉斑块相关的候选蛋白并评估其对传统风险因素模型的增量预测价值，随后在 UK Biobank 中对该蛋白标志物组合进行跨人群可迁移性评估；作者指出两队列在人群特征、结局定义和检测平台上的差异会影响可比性，且可用蛋白标志物数量有限 [48]。CKB 的前瞻性分析则聚焦早成年期 BMI 与心血管疾病的关联，采用 Cox 模型并以正常体重组为参照，发现早成年期 BMI 升高与 CVD 风险呈单调剂量反应关系，该关联基本独立于后续体重变化，出血性卒中风险亦升高，而中年健康生活方式因素未显示显著交互作用 [49]。**前者强调跨人群迁移验证的方法学框架，后者提供中国人群内部剂量反应证据，但两者均未触及筛查—干预闭环**；ESCALATE 试验将 CAD PRS 纳入初级保健 CVD 风险评估、对 5 年绝对风险低/中危者计算 PRS 并将 CAD PRS≥80% 者转诊行冠脉钙化扫描，主要结局为亚临床 CAD（CACS>0 AU），代表了本方向向实施研究延伸的设计雏形 [50]。**从「模型在队列中表现好」到「筛查路径能改变临床决策与结局」，本方向目前最薄弱的环节正是这一转化证据层**，而这也正是「心血管队列多组学与临床 AI」区别于纯预测建模研究的边界所在。

## 2 方法学


### 2.1 心血管风险预测与疾病轨迹模型

传统风险方程在中国人群中的推导与验证构成了这一方向的基础。China-PAR 项目基于 **4 个中国当代队列**推导 10 年 ASCVD 风险方程，推导队列 21320 人，外部验证 14123 人与 70838 人，男性 C 统计量 **0.794**、女性 **0.811**，校准 χ² 男 13.1（P=0.16）、女 12.8（P=0.17），12 年随访 1048 例首发 ASCVD，并与 ACC/AHA 指南 Pooled Cohort Equations 对比 [1]。SCORE2 则采用性别特异、竞争风险调整的 Cox 模型，基于 13 国 45 队列 677684 人、30121 例 CVD 事件推导，外部 25 队列 113 万人验证，C-index **0.67–0.81**，并按欧洲四类风险区域重校准 [51]。QRISK3 走的是另一条路：在 QResearch 1998–2015 年 25–84 岁开放队列中开发，推导 789 万人、验证 267 万人，加入 HIV/AIDS、SLE、严重精神疾病、勃起功能障碍、偏头痛和血压变异性等新增因素以改进 QRISK2 [52]。三者提示方程设计高度依赖目标人群与可用变量，跨体系直接套用存在风险。

外部验证反复暴露校准问题，且方向并不一致。QRISK3 在 UK Biobank 中区分度中等且随年龄下降，**系统性高估** CVD 风险，老年参与者高估达 **20%**，作者建议重新校准或开发定制模型 [2]。SCORE2 在荷兰族裔与社会经济多样化人群中验证时，按高危亚组调整至高危欧洲国家模型后，符合治疗资格人数几乎翻倍（男 10%→17%，女 2%→5%），说明族裔与社会经济地位可进一步区分绝对风险 [11]。中国人群的验证结果同样不乐观：CKB 吴忠子队列 42937 人与 JBPCD 14125 人中，一般人群 C 统计量 0.723–0.778、糖尿病人群 **0.584–0.629**，原模型 E/O 一般人群 1.47–3.78、糖尿病 0.32–2.70，重校准后区分度变化不大但校准显著改善 [3]。跨国直接检验进一步显示预测因子效应并不完全可移植：新西兰 47958 人与中国 46558 人 T2D 无 CVD 队列中，新西兰 5622 例（11.7%）、中国 3650 例（7.8%）CVD 事件，女性每 10 年年龄风险比新西兰 **1.61** vs 中国 **2.51**，标准重校准未能改善中国队列校准 [12]。

机器学习模型在区分度上普遍报告了相对传统方程的增益，但增益幅度与验证强度差异明显。UK Biobank 473611 名无 CVD 者、645 个候选变量中数据驱动建立的 UKCRP 含 **10 个预测因子**，AUC **0.762±0.010**、Brier 0.057±0.006，MI AUC 0.774、IS 0.730、HS 0.644，10 年内 31466 人发生 CVD，但人群以白人为主（94.0%），出血性卒中预测较差 [13]。同一数据库上，AutoPrognosis 利用 423604 人、473 个变量、9 类特征构建模型并与 Framingham 等比较，报告机器学习可整合大量变量与复杂交互、在总体及糖尿病等亚组具潜在优势，但受变量缺失严重与外部验证有限制约 [14]。这些结果共同的问题是：内部或单库验证的区分度提升，未必等于跨人群的校准改善。

中国人群的深度学习与可解释模型开始出现更严格的对照设计。CHARLS 2011–2020 年 8080 名 ≥45 岁无基线 CVD 者、随访 9 年、77 个候选变量筛出 11 个预测因子，按 7:3 分为训练集 5657 与验证集 2423，十种机器学习模型中 **GBM AUC 0.828** 最高、Logistic 0.792，并以 SHAP 解释、提供网络风险计算器，局限是单队列、缺乏外部验证 [4]。两者对照说明，同一人群内报告的高 AUC 与跨队列外部验证的稳健性需要分开看待。

纵向轨迹与动态预测是区别于基线模型的一条独立路线。开滦队列 16378 名中国 T2DM 患者中，ML-CVD-C 用功能主成分分析提取 **4 年风险因子轨迹**并纳入机器学习，与 PREVENT、China-PAR、SCORE-2D、ADVANCE 比较，整合纵向轨迹的模型优于仅用基线变量的模型，支持动态风险评估，但限于单队列、需外部验证 [5]。这与上述基线模型形成方法学分歧：风险因子的变化信息是否应进入方程，目前只有单队列证据支持。

多组学与影像表型的增量价值证据正在积累，但多停留在再分层而非替代临床评分。UK Biobank 306654 人中评估 PRS 加入传统风险因素的判别与重分类增益，并用 CPRD 210 万人模拟按指南启动他汀的临床影响，同时比较 PRS 与 CRP 的增量价值，结论是 PRS 临床效用仍不确定、主要基于欧洲人群、建模依赖假设 [6]。多族裔验证的 ASCVD-IRT 将 PRS 与 ASCVD-PCE 结合，NRI 白人 **2.7%**、黑人 2.5%、南亚 **8.7%**、西班牙裔 7.5% 但 CI 含 0，部分族裔样本小、CI 宽，摘要缺校准与绝对风险 [15]。脂质组学与基因组整合模型在 AusCVDRisk 路径上改善中间风险人群再分层，能正确上调未来事件并识别亚临床斑块负担者，条件性检测临床获益最大，但需前瞻性真实世界验证、脂质组学平台可扩展性受限 [16]。CMR 方面，UKBB 27254 人联合 15 个临床风险因子的可解释机器学习显示 CMR 表型可提升 MACE 预测，并在西安交大附二院 522 人超声队列做跨模态可迁移性评估，但超声替代 CMR 存在测量精度与定义差异、非直接外部验证 [17]。

心衰与房颤的专项预测模型提供了另一类对照。Echo2HF 基于 MGH **4057664 段**超声视频、70763 例患者开发，外部 BWH 34802 例验证，10 年内部 AUROC **0.83**（95%CI 0.81–0.85）、外部 0.82（0.81–0.83），数值上优于 PCP-HF 与 PREVENT，但仅回顾性、外部仅单中心 [7]。房颤方面，CHARGE-AF 合并 ARIC、CHS、FHS 共 18556 例推导、7672 例 5 队列验证，模型含常规临床变量、部分无需 12 导联 ECG，摘要未给 AUC 等具体数值，仅限白人/非裔、年龄 46–94 [18]；而基于多机构 EHR 的 412085 例 45–95 岁人群、14334 例新发 AF 的 5 年模型，验证 C-statistic **0.777**（95%CI 0.771–0.783）、校准 0.99，判别与校准优于 CHARGE-AF 的 0.753，但依赖编码、外部验证有限 [19]。这两组结果说明，同一结局下数据源（影像 vs EHR vs 问卷变量）会实质改变可比性与结论。

### 2.2 心血管多组学与遗传整合

血浆蛋白组遗传学的基础图谱已由UK Biobank的Pharma Proteomics Project奠定：该项目在**54,219名**参与者中表征血浆蛋白组，对**2,923个蛋白**进行pQTL定位，鉴定**14,287个主要遗传关联**，其中**81%为新发现**，并揭示跨生物域的trans pQTL、配体-受体相互作用与通路扰动，以及ABO和FUT2对胃肠组织富集蛋白的远距离上位效应[20]。该资源以欧洲ancestry为主、非欧样本量小，这一局限贯穿后续多数分析[20]。在此基础上，结构变异层面的解析进一步展开：利用长读长组装参考面板在**54,306名**UK Biobank参与者中插补**54,578个SV**和**15,826个VNTR**，检测其对2,923种血浆蛋白丰度的影响，发现SV和VNTR共同解释蛋白丰度变异遗传力的**约8.0%**，鉴定出**8,065个SV-蛋白**和**4,101个VNTR-蛋白**独立关联，这些关联常扰动活跃调控元件、TAD边界和转录后过程[21]。

从关联走向因果推断，孟德尔随机化与共定位成为区分病因相关蛋白的核心手段。在UKB **52,164人**、2,919个蛋白的观察性分析中，**636个蛋白**与任一CVD相关，**126个**与MI、IS、HF三类结局均相关，**118个**在中国慢性病前瞻性队列（1,937人）复制；MR提示**47个蛋白**与CVD相关，**18个**有共定位证据，FGF5、PROCR和FURIN等显示潜在因果性，但多数观察性关联并非因果，部分MR蛋白在心脏或动脉表达弱[8]。跨人群MR进一步将范围扩至非洲、东亚、欧洲人群，系统评估**2,922个**循环蛋白对AF、CAD、HF、IHD、PAD五类CVD的潜在因果作用，强调人群特异pQTL与跨人群一致性评估[22]。

蛋白组对心血管风险的增量预测价值已在多个UKB子集中被反复检验，但增益幅度与对照模型高度相关。在**41,931人**中开发5–20个蛋白的稀疏模型预测218种疾病10年发病，基础临床模型中位C-index为**0.64**，**163种**疾病5蛋白即媲美临床模型，另**30种**更优，**67种**加5–20蛋白显著提升，中位**ΔC-index=0.07（0.02–0.31）**，多发性骨髓瘤Δ=**0.25**、非霍奇金淋巴瘤Δ=**0.21**[9]。针对MACE，**38,380人**、2,919蛋白的极端梯度提升分析显示SCORE2 AUC **0.740**，数据驱动选出的**114个蛋白**单独预测AUC **0.758**，与SCORE2联合升至**0.771（NRI 0.140）**，与10项TRF联合为**0.767（NRI 0.053）**，而随机选114个蛋白无改善[23]。在**46,009名**无基线CVD者中，可解释提升机蛋白组模型AUROC **0.767**、AUPRC **0.241**，优于PREVENT等方程评分及多个PRS，加入临床特征后升至**0.785**和**0.284**[24]。另一项**44,431人**、Olink 1,460蛋白的研究构建**117蛋白**ProtRS，C-index **0.769**，优于SCORE2 **0.667**、PREVENT **0.645**、FRS **0.672**，加入基线模型后C-index由**0.669**升至**0.774**，**ΔC=0.105**[25]。这些数字来自不同子集与不同对照，不能直接横向比较高低，但一致指向蛋白组在传统评分之上的增量信息。

冠心病方向的专门建模同样显示中等幅度提升。基于UKB蛋白组与遗传数据（训练**32,330**、内部验证**13,857**、外部**5,775**），LASSO Cox推导**202蛋白**风险评分并以CatBoost整合，内部验证AUC从**0.750（0.732–0.767）**升至**0.789（0.772–0.805）**，外部验证从**0.717（0.683–0.750）**提升[26]。在**51,859人**、平均**56.7岁**、中位**13.6年**随访发生**4,857例**MACE的分析中，NT-proBNP每SD的HR为**1.68**，蛋白模型在校准、NRI和C统计量上优于PREVENT[27]。房颤方面，UKB-PPP **51,680人**、1,459蛋白开发的**165蛋白**Lasso-Cox评分每SD风险比**2.20**，加入CHARGE-AF、NT-proBNP和多基因风险评分后C指数由**0.771**升至**0.816**，并在ARIC **11,012人**外部验证[28]。心衰与衰弱共享通路的研究在ARIC测量**4,877个**Somascan v4 aptamer（V3 n=**10,638**、V5 n=**3,908**），并在CHS（n=**3,189**）外部复制，结合MR评估候选蛋白的潜在因果效应[53]。

蛋白组预测的泛化性与表型定义密切相关。在UKB **53,026人**中训练15种疾病模型，平均AUC **0.74**（范围**0.56–0.89**），较仅用临床因素平均提升**ΔAUC=0.03**，且不依赖模型架构，简单模型如L2表现相当，提示跨队列泛化性受表型定义影响[29]。动脉粥样硬化负荷方向，UKB嵌套匹配病例对照**1,666对**、Olink **2,920蛋白**训练四种AtheroBurden特征，在**41,200名**无病者中计算评分并经颈动脉超声、**13.7年**MACE随访及KORA外部队列验证，显示可反映系统性负荷并改善MACE预测与风险重分类[54]。在2型糖尿病人群中，**2,198例**T2D、2,920蛋白、中位**13.1年**随访发生**298例**新发心衰，**455个**蛋白相关，WAP 4-disulfide core domain protein 2风险最高，蛋白组可增强超越临床变量、多基因风险和NT-proBNP的预测[55]。CKD与心血管结局的整合分析纳入**44,779名**无CKD及**3,749–4,272名**现患CKD者，发现**598个**蛋白跨至少两种疾病共享、**471个**疾病特异，POLR2F、TNFRSF10B、IGFBP2与全部五种疾病正相关，加入预测蛋白改善CKD、CHD、卒中和心衰预测[56]。

代谢组作为与蛋白组互补的维度，在SCORE2框架下被系统评估。2型糖尿病专属模型中，UKB **10,257例**与ESTHER **1,039例**、249种代谢物选出**7种**，内部验证C指数从**0.660**升至**0.678（P=0.037）**，外部验证增**0.043（P=0.011）**，白蛋白、omega-3百分比和乳酸改善区分度[30]。单一脂质比值方面，**183,237名**50–69岁无CVD/糖尿病者中，PUFA/MUFA比值加入SCORE2使验证集（**54,971人**）C指数从**0.740**升至**0.744（P<0.001）**，NRI **7.5%**、IDI **0.025**，比值每增1单位MACE风险HR **1.21**[31]。在**54,933名**美国整合医疗系统参与者中检测**250个**NMR代谢标志物并评估9个心血管-肾脏-代谢终点，加入标准诊疗预测因子后几乎所有终点判别能力提升，2型糖尿病、慢性肾病和MASLD增益最大[32]。多组学联合在T2D中亦有尝试：UKB蛋白组**1,751人**、多组学**990人**构建性别特异蛋白特征提升SCORE2-Diabetes，加入**7个**性别特异代谢物和CVD-PRS进一步改善预测，但样本量较小、以White人群为主[57]。

多基因风险评分是遗传整合的另一支柱，其跨人群可迁移性是核心争议。GPS_Mult整合五个ancestry的CAD GWAS（>**269,000**病例、>**1,178,000**对照）及十项危险因素，在UKB **116,649名**欧洲ancestry个体训练、**325,991人**独立验证，与患病CAD关联**OR/SD 2.14**，识别**20.0%**人群风险增3倍、**13.9%**风险降3倍，与事件CAD关联**HR/SD 1.73**，识别**3%**健康个体风险等同现患病人，并在多族裔外部验证中优于所有既往CAD评分[33]。然而在中国人群中，嘉道理生物库训练**28,490**、测试**72,150人**，测试集**11.2年**随访**1,214例**硬CAD、**7,201例**软CAD，最优PRS每SD对硬CAD的**HR 1.26**，加入传统模型后Harrell C男性仅增**0.003**、女性增**0.001**，最高NRI **3.2%**，对软CAD改善极小或无改善[10]。中国人群的另一项工作以**2,800例**CAD和**2,055例**对照训练metaPRS，在China-PAR **41,271人**中评估其与临床风险评分结合对终生风险轨迹的影响，显示可改善风险分层[58]。跨祖源可靠性问题也被方法学层面处理：UKBB T2D **19,468人**（WB **17,574**、SA **1,145**、AFR **749**）及ADVANCE试验中，Mondrian交叉共形预测提升跨祖源PRS预测可靠性与不确定性量化，可控制预设错误率并识别不可可靠预测个体[34]。

PRS在不同心血管表型与合并症场景中的表现差异明显。房颤与室性心律失常方面，UKB **158,733名**欧洲裔中AF2模型C指数**0.762** vs AF1 **0.746（P<0.001）**，AF3为**0.765**；VA2 C指数**0.692** vs VA1 **0.681（P<0.001）**，非欧洲裔样本量较小、VA预测增益有限[59]。房颤遗传结构解析中，BioBank Japan **9,826例**/140,446对照发现**31个**位点、其中**5个**新位点，跨祖先共**49个**独立信号，SNP h² **6.1%**、liability h² **11.7%**，跨祖先PRS与长期心血管死亡风险相关，但跨祖先可迁移性仍有限[60]。颈动脉狭窄方面，Mass General Brigham Biobank **670例**狭窄与**52,636例**对照中，IS PRS **OR 1.31**、CAD PRS **OR 1.62**、PAD PRS **OR 1.66**（均p<0.0001），cIMT PRS无关联，PAD PRS **ΔC统计量0.017**、C **0.845**[61]。Lp(a)方向，UKB约**50万**成人中LPA GRS与Lp(a)水平强相关，**≥120 nmol/L**为升高，LPA GRS未在实测Lp(a)之外提供额外预后信息，两者相对Pooled Cohort Equation仅带来适度判别改善[62]。

PRS与生活方式、代谢特征的交互为风险分层提供另一视角。UKB **276,096名**白人比较P+T、LDpred、PRS-CS与AnnoPred，AnnoPred预测最优；健康生活方式在不同PRS组相对风险降低相似，但高PRS者绝对风险降低更大，T2D最高**1%** PRS组**ARR 12.4%** vs 最低十分位**2.8%**[63]。将CAD多基因风险分解为生物学过程的工作，对**526个**全基因组显著变异结合**78个**CAD相关表型做潜在因子分解，识别**8个**遗传组分（富含胆固醇脂蛋白、富甘油三酯脂蛋白、脂蛋白(a)、代谢不健康正常体重、肥胖、内皮功能障碍、凝血和心脏重构），据此构建的pPRSs可捕捉传统风险因素之外的生物学特征，并在UKB（n=**458,905**）等队列验证[64]。衰弱与CAD关联的代谢中介研究在**223,907名**基线无冠心病者中定义衰弱，并在**122,959名**有NMR数据者中分析**169种**代谢物，用弹性网构建代谢特征并以Cox模型评估中介与遗传交互，摘要未报告具体定量结果[65]。

观察性与遗传证据的整合还延伸到炎症标志物、脂质遗传与器官衰老等外围维度。哥本哈根一般人群研究（n=**101,730**）结合孟德尔随机化检验中性粒细胞计数与九类心血管终点，发现中性粒细胞升高与广泛心血管终点风险增加一致相关，遗传证据支持潜在因果性，而淋巴、单核、嗜碱和嗜酸细胞关联不一致[66]。血脂组学方面，AIDHS/SDS **3,000人**与UKBB **468,515人**（EU **459,143**、SA **9,372**）的代谢物GWAS结合精细定位、共定位与MR，发现新的血脂遗传关联及祖源特异性差异，并识别与T2D和心血管病共享的候选因果变异[67]。APOE跨祖源表型组分析在All of Us **367,757名**参与者、六个遗传祖源群体中按阿尔茨海默病风险层级测试**2,632个**表型，识别**27个**APOE相关表型，集中于神经和脂质性状，**5个**脂质性状女性效应更大、**9个**关联具祖源特异性[68]。器官衰老方向，UKB **409,206名**参与者的**14个**器官多组学衰老时钟整合NMR代谢组、Olink蛋白组与临床表型，发现年龄加速与死亡风险是器官生物学的不同维度，具有可分离的表型、分子和遗传结构[69]。

方法学共识与争议并存。AHA科学声明综述GWAS、家系与双生子证据，指出多基因风险评分可捕捉群体遗传易感性、成本下降推动大规模遗传分析，但其风险预测精度、临床效用、公平性和实施路径仍不明确[70]。欧洲心脏杂志综述认为蛋白组与脂质组在判别与重分类上相对临床评分一致显示改善，但尚未被当前预防指南采纳，临床效用研究仍待开展[71]。

### 2.3 ECG 与心脏影像 AI

在窦性心律心电图上用深度学习预测新发房颤，是这一方向证据最密集的子问题，但各研究在队列、预测窗与验证设计上差异明显。Mayo Clinic 的早期工作用卷积神经网络从 10 秒 12 导联窦律 ECG 中识别房颤电信号特征，按 7:1:2 划分训练、内部验证与测试，并以验证集 AUC 选阈值 [35]；Geisinger 则以 **280 万份 ECG** 为池、保留 160 万份/43.1 万人建模，回顾性模拟部署后发现无房颤史且发生房颤相关卒中的患者中近三分之二在卒中前被预测为高风险 [36]。MGH 的工作把 ECG-AI 与 CHARGE-AF 联合为 CH-AI 模型，在内部与 BWH、UKB 外部测试集评估，摘要未给出具体 AUC [72]；退伍军人队列纳入 **907858 份 ECG**、平均年龄 62.4 岁、男性 93.6%，在 2 个 VA 网络训练、另 4 个 VA 及 1 个非 VA 中心测试，预测 31 天内 AF [37]。社区场景下，FHS 用 10,097 人 28,151 份 ECG 优化 ECG-AF 并与 CHARGE 评分比较，报告中等区分度但摘要数值被截断 [38]；三级心脏中心用 140 万份 ECG、25 万成人训练 ResNet-50 预测 5 年新发 AF [73]。

外部验证的结果对上述乐观性能构成直接约束。一项 3 中心、**4017 例** 65 岁以上无房颤史患者的研究，按预设敏感性 20%、特异性 85% 评估，模型判 391 例高风险其中 74 例发生房颤，**敏感性仅 31%**（95%CI 25–37），3626 例无高风险者中 3460 例保持无房颤 [39]；作者明确指出单机构评估常高估性能。这与 Geisinger 的回顾性模拟形成对照，提示部署场景与阈值选择会显著改变可检出比例。

心衰与左室收缩功能障碍方向，方法从单导联到多模态递进。YNHHS、UKB、ELSA-Brasil 多国队列中，AI-ECG 阳性者新发心衰风险高 **4 至 24 倍**，C 统计量 0.718/0.769/0.810，对照为 PCP-HF 方程 [40]；同一团队进一步用噪声自适应模型从单导联 I 导联预测 LVSD 并与 PCP-HF、PREVENT 评分比较 [74]。UKB 训练、SHIP-START（4308 人）与 SHIP-TREND（4420 人）外部验证的 AI-HF 表明单导联 ECG 可行，但摘要未给出区分度数值，且无法区分射血分数表型 [75]。结构性心脏病方面，美国大型医疗系统开发的集成模型在伊朗三级中心 **879 例** ≥45 岁高危门诊患者中前瞻验证，检测 LVSD、瓣膜病与严重 LV 肥厚 [41]；更早的 AI 增强 ECG 筛查收缩功能障碍工作因全文未获取，方法与结果细节无法评估 [76]。

左房结构功能是 ECG 与影像交叉的典型切口，但“预测相关性强”与“测量一致性有限”并存。Nature Communications 版本在 UKB **48,300 名**配对参与者上训练，LAVmin/LAVmax 相关 r=0.50、LAEF r=0.40，与 CMR 仅中等相关，却与新发房颤、卒中、心衰独立相关，且在 14 天监测中预测房颤优于现有工具和 NT-proBNP [42]；同一工作的会议摘要给出 r=0.40–0.50、训练集 21,749 人、外部队列为 ≥65 岁心血管健康研究，并称优于传统 P 波终末电势指标 [77]。两处报告指向同一结论：ECG 捕捉的是与影像中度相关的电学替代标记，而非影像测量本身，极端值还存在回归均值偏差 [42]。

多模态与基础模型正在把 ECG 与 CMR、超声、EHR 联合。CARDIAC-FM 用对比学习在 UKB **57,609 对** ECG-CMR 样本上训练，在 CHS 与 MESA 外部验证，报告持续优于单模态并可在无 MRI 时仅用 ECG 部署 [43]；ECG 与超声心动图的多模态基础模型用 129424 例超声视频 4391610 段、配对 1094656 份 ECG（53876 人），测试集 LVSD 分类 **AUROC 0.94**，优于单模态 [44]。TRIM 则把非结构化报告转为文本表征融入 EHR 轨迹并保留跨模态时间上下文，报告整体 CVD 预测提升、生存分析风险比一致升高，但未报告样本规模与外部验证 [78]。

基础模型路线的代表工作强调规模与公开可复现。ECG-LFM 用 **1157 万份** 12 导联 ECG、197.9 万人预训练，结合对比学习与掩码语言建模，在 PTB-XL、Chapman、CODE-15、CPSC-2018、UKB 外部测试，平均 **AUROC 0.930**，并经 PheWAS 关联 167 个心功能因子、GWAS 发现 11 个位点 12 个 SNP [45]；ECG-FM 用 140 万 ECG 片段预训练并在 UHN-ECG 外部机构验证多标签解读与降低 LVEF 预测，公开权重、代码与基准 [46]。二者均承认可解释性有限，且预训练数据以公开集或单机构私有数据为主。

死亡与复合心血管风险的生存建模更接近临床可行动性。另有生存深度学习模型用两家医院 291778 名患者、开发集 451950 份 ECG，并在 CODE15 与 SaMi-Trop 国际验证，主张死亡风险优于 ECG 年龄 [79]；巴西 230 万份 ECG、155 万患者的可解释网络则把诊断与死亡风险分层放在同一框架内 [80]。外部 C-index 相对内部下降是这类工作的共同特征 [47]。

房颤之外的具体疾病靶点也在扩展。ECG2CAD 在 MGH **764,670 份** ECG（137,199 人）上训练，在 MGB 52.1 万+9.9 万人与 UKB 50.3 万人外部验证，报告对 CAD 有判别力且不劣于临床风险或年龄性别模型，但 CAD 定义依赖 ICD 编码 [81]；ECG2Stroke 在 MGH 101496 人训练、预测 10 年缺血性卒中，在 MGH 测试集 4771 人、BWH 68884、BIDMC 29882 外部验证，对照修订版 FSRP，并分析卒中亚型与显著图 [82]。这些工作共同的问题是终点依赖编码或病历表型，机制解释仍有限。

影像侧的机会性筛查提供了非 ECG 的对照证据。NLST 中用开源 TotalSegmentator 从 **27,943 例**非增强非 ECG 门控胸部 CT 提取心脏与胸主动脉体积，10356 例训练 3D DenseNet169 预测 12 年心血管死亡，5165 例测试集 **AUC 0.72** 高于基线模型 0.66 [83]；视网膜方向的 Reti-CVD 在 UKB 44,677 人、随访 7 年，评分升高与卒中 277 例、MI 506 例、AF 1053 例、HF 431 例风险显著增加相关 [84]。二者说明 ECG 之外的常规影像同样承载风险信息，但均缺乏与 ECG 模型的头对头比较。

测量层面的基础工作与人群表型描述构成上述模型的底层支撑。UKB 专家标注参考集含 1030 人、**11330 条**导联级标注，1D CNN 估计 PR/QRS/QT 的 MAE 分别为 **7.7、7.5、4.9 ms**，优于 CardioSoft、开源工具箱与小波方法，观察者 ICC 0.81–0.97 [85]；中国 Kadoorie Biobank 25,239 名成人用 Mortara VERITAS 自动判读，正常 ECG 44.3%、房颤 1.2%、缺血 28.1%、LVH 13.6%，病理表型随年龄与既往 CVD 增加，但摘要未完整展示与改良 CHA2DS2-VA 评分的预测性能比较 [86]。这两项提示：自动测量与自动判读的误差和人群分布，会直接传导到下游风险模型的校准与泛化。

### 2.4 房颤与心律失常 AI 预后模型

在房颤预后预测方向，系统综述与Meta分析证据显示，机器学习与深度学习模型总体呈现**中等至良好区分度**，且在同一数据集上多优于临床风险评分与传统回归模型[87]。该综述检索PubMed、Embase、Scopus、Cochrane Library、Web of Science与ProQuest至2024年10月21日，采用TRIPOD+AI与PROBAST+AI评估报告质量与偏倚[87]。但其同时指出，多数研究**缺乏外部验证、偏倚风险高、报告不完整**，部分结局研究不足[87]；这些方法学缺陷构成当前AI预后模型证据向临床转化时的主要争议点。

在风险预测的输入信息层面，另一项基于**UK Biobank 39,478名**无既往房颤参与者的研究，评估了在CHARGE-AF临床风险模型基础上整合房颤多基因风险评分、AI-ECG年龄差与AI-ECG预测性别错配的效果，通过序贯预测模型比较后显示，整合遗传信息与AI-ECG数据可提升房颤风险预测[88]。该工作与上述综述关注的差异在于：前者聚焦多组学与AI-ECG特征对既有临床风险模型的增量价值，后者则系统评估ML/DL预后模型相对非AI方法的整体表现；两者人群、设计与结局不同，其数字不宜直接比较。

## 3 数据与资源

（本节暂无入库证据）

## 4 中国人群队列与跨人群迁移

在 ChinaHEART 全国社区队列中，一项巢式病例对照研究使用 MSD 平台检测 **28 种血浆蛋白**，以识别与新发颈动脉斑块相关的候选蛋白，并评估其对传统风险因素模型的增量预测价值；随后在 **UK Biobank** 中对该蛋白标志物组合进行跨人群可迁移性评估 [48]。该研究提示候选蛋白涉及血管损伤、炎症与血管生成等通路，但作者指出两队列在人群特征、结局定义和检测平台上的差异会影响可比性，且可用蛋白标志物数量有限，跨人群预测效果受此制约 [48]。这一设计代表了「中国队列开发—外部队列迁移验证」的路径，但其迁移性结论目前仅停留在评估层面，尚未给出可推广的定量证据。

与之相对，China Kadoorie Biobank 的前瞻性分析聚焦早成年期 BMI 与心血管疾病的关联，采用 Cox 模型并以正常体重组为参照，发现早成年期 BMI 升高与 CVD 风险呈单调剂量反应关系，该关联基本独立于后续体重变化，出血性卒中风险亦升高，而中年健康生活方式因素未显示显著交互作用 [49]。该研究为观察性设计，早成年期 BMI 多依赖回忆或历史数据，残余混杂可能存在 [49]。两项工作分属蛋白标志物预测与生活方式相关风险因素两条线索，前者强调跨人群迁移验证的方法学框架，后者提供中国人群内部剂量反应关联，二者在结局（颈动脉斑块 vs 临床 CVD）与暴露（蛋白 vs BMI）上不可直接比较，共同构成中国人群队列证据的不同侧面。

## 5 临床转化与评测

在临床转化路径上，ESCALATE 试验代表了将多基因风险评分嵌入初级保健的前瞻性实施研究：针对 45–65 岁、5 年绝对风险低/中危者计算 CAD PRS，将 **CAD PRS≥80%** 者转诊行冠脉钙化扫描，主要结局为亚临床 CAD（**CACS>0 AU**），并评估血脂血压治疗、用药强度及健康相关生活质量等次要结局 [50]。该研究设计为 12 个月前瞻性多中心、非随机实施试验，纳入 **1000 名**参与者，方案阶段尚无结局数据 [50]；同一试验的另一份设计论文亦强调其关注新诊断 CAD、共同治疗决策以及参与者和提供者体验，且尚未报告疗效、体验和成本效果结果 [89]。两项证据均处于方案阶段，尚不能提供转化有效性的实证结论，其非随机设计也是需要指出的局限 [50][89]。

在真实世界数据模拟试验与模型指导治疗决策两条路线上，方法差异明显。DISCO 数字孪生框架以 AI-ECG 嵌入进行高维表型匹配，在符合 PARADIGM-HF 标准的 HFrEF 患者中比较 ARNi 与 ACEi，并以 PARADIGM-HF 试验结果及传统生存分析校正为参照，声称可估计药物效应风险比并校正年龄、性别及心血管危险因素等基线差异，但观察性数据的残余混杂仍是其局限 [90]。另一项基于 UK Biobank 的研究用视网膜图像训练的 Reti-CVD 深度学习模型识别高危者，经 1:1 倾向评分匹配后得到 **3,008 对**、平均随访 **9.83 年**，计算他汀使用者的 CVD 事件风险比以评估获益，作者亦承认倾向评分匹配不能完全消除混杂 [91]。两者同属观察性设计下的因果推断尝试，但前者以 AI-ECG 高维匹配对齐 RCT 入选标准，后者以视网膜模型分层加倾向评分匹配评估治疗效应，证据均限于摘要层面，尚不足以判断何者更接近真实治疗效果 [90][91]。

## 6 空白与趋势

**空白一：中国人群的蛋白组/代谢组风险模型几乎全部停留在“单队列开发、缺外部验证”，且与PRS、临床评分的联合方式尚未定型。** 现有蛋白组增量证据高度集中于UK Biobank子集，ProtRS、EBM、LASSO-Cox等模型报告的C-index提升幅度从0.02到0.105不等，但对照模型、蛋白平台（Olink 1,460 vs 2,923 vs Somascan）与人群构成各不相同，无法横向比较 [25][24][23]。中国人群方面，目前仅有ChinaHEART巢式病例对照的28种蛋白组合在UKB做迁移性评估，且作者自陈两队列人群特征、结局定义与检测平台差异制约可比性，未给出可推广的定量结论 [48]。**这意味着“在中国万人级队列上训练蛋白组风险模型、并在独立中国队列或东亚队列外部验证”的工作仍是空白**；CKB虽已提供蛋白-MR与观察性关联的复制证据（636个蛋白相关、47个MR阳性、18个共定位）[8]，但尚未推进到预测建模与校准评估。

**空白二：跨人群校准而非仅区分度，是组学与PRS落地中国人群的核心缺口，现有证据一致指向“增益极小或不可迁移”。** CKB 28,490训练/72,150测试中，最优PRS对硬CAD每SD的HR 1.26，加入传统模型后Harrell C男性仅增0.003、女性增0.001，最高NRI 3.2% [10]；GPS_Mult虽在欧洲ancestry验证中OR/SD 2.14、优于既往所有CAD评分，但其训练与主要验证均在UKB欧洲人群 [33]。跨祖源可靠性已有方法学尝试（Mondrian交叉共形预测可控制预设错误率并识别不可靠预测个体）[34]，但**尚未见其在中国心血管队列的实证应用**。同时，SCORE2在荷兰多样化人群的验证显示族裔与社会经济分层可使治疗资格人数近乎翻倍 [11]，提示中国人群的跨体系校准研究不能只做“整体重校准”，还需亚组分层。

**空白三：ECG/影像AI与组学、EHR的“真联合”多停留在概念验证，缺少在同一万人级队列上同时具备多模态输入与硬终点外部验证的设计。多模态尝试如CARDIAC-FM（57,609对ECG-CMR，CHS与MESA外部验证）[43]、ECG-超声基础模型（LVSD AUROC 0.94）[44]已出现，但**均未与血浆蛋白组或PRS联合**；而蛋白组模型（如165蛋白房颤评分加入CHARGE-AF、NT-proBNP与PRS后C指数0.771→0.816，ARIC 11,012人外部验证）[28]也**未纳入ECG-AI特征**。两条证据链平行推进、尚未交汇，是明确的空白。

**趋势一：从“单组学增量”走向“临床评分+蛋白组+PRS”的三元整合，但整合顺序与简约性尚未形成共识。** UKB 44,431人的ProtRS在SCORE2、PREVENT、FRS之上将C-index由0.669升至0.774（ΔC=0.105）[25]；46,009人的EBM模型AUROC 0.767、加临床特征后0.785 [24]；CAD专门模型中202蛋白评分加CatBoost使内部AUC 0.750→0.789、外部0.717起提升 [26]。

**趋势二：MR/pQTL正从“找关联”转向“跨人群因果推断+结构建模”，但转化到预测模型的路径尚未打通。** 跨非洲、东亚、欧洲人群的蛋白组MR已系统评估2,922个蛋白对五类CVD的因果效应，强调人群特异pQTL与跨人群一致性 [22]；UKB与CKB联合的MR+共定位给出47个遗传预测关联蛋白、FGF5/PROCR/FURIN等潜在因果 [8]；结构层面已整合AlphaFold3对5,813个蛋白做因果优先级排序 [92]。**但这些因果蛋白极少被回投到风险预测模型中检验增量价值**——现有预测模型用的是数据驱动的LASSO/EBM蛋白集，与MR因果集几乎不重叠，这是“机制发现”与“预测建模”之间的明显断层。

**趋势三：筛查—干预闭环开始出现，但证据仅到“实施可行性”层面，缺硬终点。** ESCALATE将CAD PRS≥80%者转诊冠脉钙化扫描，12个月前瞻性多中心、1,000名45–65岁低/中危者，主要结局为CACS>0 AU [50][89]。这是本方向少见的“PRS→影像筛查→临床决策”闭环设计，但**样本仅1,000人、非随机、主要结局为亚临床CAD而非事件**，距实用性随机试验与硬终点证据仍有距离。相比之下，蛋白组与代谢组的临床效用研究整体仍缺位，综述明确指出这些组学方法“有前景但尚未被当前预防指南采纳” [71]。

**趋势四：中国人群的机器学习预测正从“单队列高AUC”转向“纵向轨迹与动态风险”，但外部验证仍是共同短板。** CHARLS 8,080人、9年随访、GBM AUC 0.828，作者自陈单队列缺外部验证 [4]；开滦16,378名T2DM患者用4年风险因子轨迹的ML-CVD-C优于基线变量模型，同样限于单队列 [5]。**两者的共同信息是：纵向轨迹携带基线模型之外的信息，但“轨迹模型在中国独立队列的外部验证与校准”尚无人完成**，而这恰是China-PAR、ChinaHEART、CKB等队列可以支撑、目前却未见发表的方向。

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 心血管风险预测与疾病轨迹模型 | 成熟 | 传统评分体系已完成多轮迭代并被大规模外部验证：QRISK3 [52] 与 SCORE2 [51] 分别覆盖英国与欧洲人群，China-PAR [1] 完成中国人群 10 年 ASCVD 风险建模，三者构成「区域评分已收敛」的证据链；近两年该节新增工作多为对既有评分的增量改进或再校准，雷达样本中该节 **n=20、CNS 占比 0**、中位引用 56，说明高影响力位置已被经典评分占据，新工作以增量为主。 |
| 2.2 心血管多组学与遗传整合 | 朝阳 | 血浆蛋白组与遗传的关联图谱已在 UK Biobank 规模上系统建立 [20]，多 ancestry PRS 显著改善 CAD 预测 [33]，蛋白组特征对常见与罕见病的预测增益已被独立验证 [9]；同时 AHA 的 PRS 科学声明 [70] 表明临床转化路径尚未定型。方法（Olink/SomaScan 平台、PRS 构建策略、MR 靶点发现）仍在快速分化，雷达样本中该节 **n=43、CNS 占比 0.12**、中位引用仅 4，是典型的「近两年爆发、方法未收敛」形态。 |
| 2.3 ECG 与心脏影像 AI | 朝阳 | 深度学习 ECG 识别房颤与左室收缩功能障碍的两项奠基工作 [35]、[76] 已确立可行性，随后 ECG-DL 联合临床风险因子预测新发房颤 [72] 与 12 导联 DNN 预测新发房颤 [36] 把方向推向「与 EHR/结局联合」；但模型架构、标签定义、外部验证口径均未统一，雷达样本中该节 **n=29、近两年占比 0.55**、中位引用 3，属于爆发期而非收敛期。 |
| 2.4 房颤与心律失常 AI 预后模型 | 证据不足 | 雷达样本中该节仅 **n=2**，且均为 2025 年新刊、引用极低（[87] 引用 2，[88] 引用缺失），不足以判断阶段；从内容看前者是 ML/DL 预后模型的综述性梳理，后者尝试整合遗传信息做房颤风险预测，方向可能真实存在但证据挂载不足。 |
| 3 数据与资源 | 证据不足 | 雷达样本中该节 **n=0**，无任何证据可引用；不能据此推断领域空白，只能说明本雷达未收录该节证据。 |
| 4 中国人群队列与跨人群迁移 | 萌芽 | 中国大型队列已产出高质量前瞻性结果，如 CKB 中早年成年 BMI 与 CVD 的长期关联 [49]；但「跨人群迁移」的关键环节——中国人群蛋白组预测颈动脉斑块的巢式病例对照 [48] 尚属 2026 年新刊、引用为 0，说明该细分仍处早期探索。雷达样本中该节 **n=2**，样本量小，判断需谨慎。 |
| 5 临床转化与评测 | 萌芽 | 已有把 PRS 嵌入冠脉钙化评分分诊的实用性设计 [50]，以及把 PRS 纳入 CVD 检查流程的尝试 [89]；AI-ECG 的高维表型匹配 [90] 与他汀在高危人群中的疗效评估 [91] 均为 2024–2025 会议摘要、引用为 0，说明筛查—干预闭环尚缺完整 RCT 证据。雷达样本中该节 **n=4、中位引用 0**。 |

**整体判断**：这个方向整体处于**「成熟评分体系 + 朝阳多组学/AI 层」的叠加态**，而非单一阶段。风险预测的骨架（SCORE2、QRISK3、China-PAR）已经收敛并被指南吸收 [51]、[1]，单纯做「新评分 + 外部验证」的空间已被压缩；真正的增量集中在**蛋白组/代谢组/PRS 的预测增益**与**ECG/影像 AI 与组学、EHR 的联合**两条线上，且这两条线的方法尚未定型（雷达样本中 2.2 与 2.3 合计 **n=72**，占全样本 **72%**，近两年占比分别 0.39 与 0.55）。窗口期判断：多组学预测增益的「第一波大样本验证」已在 2023–2024 完成 [20]、[9]，**留给「用新方法做增量」的时间大约 12–24 个月**；此后将进入平台期，竞争点转向跨人群校准与临床转化证据。最大不确定性有三：其一，**跨人群迁移**——中国/东亚队列的蛋白组与 PRS 证据仍薄弱（2.4 节雷达样本仅 n=2），UK Biobank 训练的模型能否迁移到 ChinaHEART/CKB 尚无定论；其二，**临床效用**——PRS 与蛋白组评分相对 SCORE2/China-PAR 的增量是否达到改变治疗决策的阈值，目前只有设计层面的证据 [50]，缺 RCT 读数；其三，**平台与批次效应**——Olink 与 SomaScan 的可比性、ECG 模型在不同设备/人群间的漂移，都会决定方法能否收敛。

**接下来怎么做**：

1. **把「衰老 + 单细胞」作为差异化切口，做细胞来源感知的蛋白组/代谢组风险建模**。切入点：用 UK Biobank Olink 蛋白组 [20] 与已发表的单细胞/衰老图谱做 deconvolution 或细胞来源先验，构建「器官/细胞类型特异的蛋白组风险评分」，再与 SCORE2 [51] 做增量比较。为什么现在做：蛋白组预测增益已被证明存在 [9]，但现有工作把血浆蛋白当黑箱特征，**细胞来源解释是明显空位**，且正好复用他的单细胞与衰老背景。产出：一个可解释的蛋白组风险评分 + 增量 ΔAUC/ΔNRI 报告。

2. **做跨人群校准，而不是再训练一个模型**。切入点：以 China-PAR [1] 为锚，把 UK Biobank 训练的多 ancestry PRS [33] 与蛋白组评分迁移到中国队列（CKB/ChinaHEART 公开汇总统计或合作数据），系统报告校准斜率、再校准前后的净获益。为什么现在做：跨人群证据是当前最大不确定性，且中国人群蛋白组预测工作才刚起步 [48]，**先做校准的人拿到话语权**。产出：跨人群校准基准 + 再校准方法。

3. **用 MR + pQTL 做「可成药靶点」筛选，与类器官项目对接**。切入点：基于 UK Biobank pQTL [20] 做心血管结局的双样本 MR，筛出因果蛋白，再用他的类器官 + 多组学平台做体外验证（表达、分泌、通路扰动）。为什么现在做：MR 靶点发现已是多组学节的标准动作，但**「MR 命中 → 类器官验证」的闭环在心血管领域仍稀缺**，这是他能独家提供的环节。产出：因果蛋白清单 + 类器官验证数据，可写成「计算 + 实验」的复合论文。

4. **把 ECG/影像 AI 与组学做联合，而不是单独做 ECG 模型**。切入点：以 ECG-DL 预测新发房颤的既有范式 [72]、[36] 为基线，加入 PRS 与蛋白组特征做多模态融合，重点看**在 ECG 模型之上组学是否还有增量**。为什么现在做：ECG AI 单模态已高度拥挤（雷达样本 2.3 节 n=29、近两年占比 0.55），**单模态再做一遍没有位置，多模态融合才是未收敛区**。产出：多模态融合模型 + 消融实验证明组学增量。

5. **用公共数据先做 demo，锁定一个「筛查—干预」的实用性设计**。切入点：复用 PRS 分诊冠脉钙化的设计思路 [50] 与 PRS 嵌入 CVD 检查流程的尝试 [89]，在公共队列上做「组学评分触发进一步检查」的成本—效益模拟，作为向临床合作方提案的敲门砖。为什么现在做：转化证据几乎空白（雷达样本 5 节 n=4、中位引用 0），**先用模拟占位，等真实 RCT 数据出现时已有方法框架**。产出：实用性试验设计草案 + 模拟的成本效益曲线。

## 参考文献

1. Predicting the 10-Year Risks of Atherosclerotic Cardiovascular Disease in Chinese Population: The China-PAR Project (Prediction for ASCVD Risk in China). Circulation 2016. https://doi.org/10.1161/CIRCULATIONAHA.116.022367
2. Independent external validation of the QRISK3 cardiovascular disease risk prediction model using UK Biobank. Heart 2023. https://doi.org/10.1136/heartjnl-2022-321231
3. Validation and Comparison of 10-Year Cardiovascular Risk Prediction Models in Two Chinese Prospective Cohorts: The General Population and Patients With Type 2 Diabetes.. Diabetes, obesity and metabolism 2026. https://doi.org/10.1111/dom.71212
4. Explainable machine learning for long-term cardiovascular disease risk prediction in Chinese middle-aged and older adults: a 9-year longitudinal cohort study with web-based risk calculator. Scientific Reports 2026. https://doi.org/10.1038/s41598-026-45297-4
5. Predicting cardiovascular outcomes in Chinese patients with type 2 diabetes by combining risk factor trajectories and machine learning algorithm: a cohort study. Cardiovascular Diabetology 2025. https://doi.org/10.1186/s12933-025-02611-0
6. Polygenic risk scores in cardiovascular risk prediction: A cohort study and modelling analyses. PLoS Medicine 2021. https://doi.org/10.1371/journal.pmed.1003498
7. Deep learning interpretation of echocardiographic images predicts incident heart failure and subtypes. Journal of Cardiac Failure 2026. https://doi.org/10.1016/j.cardfail.2026.07.003
8. Measured and genetically predicted protein levels and cardiovascular diseases in UK Biobank and China Kadoorie Biobank.. Nature cardiovascular research 2024. https://doi.org/10.1038/s44161-024-00545-6
9. Proteomic signatures improve risk prediction for common and rare diseases.. Nature medicine 2024. https://doi.org/10.1038/s41591-024-03142-z
10. Minimal improvement in coronary artery disease risk prediction in Chinese population using polygenic risk scores: evidence from the China Kadoorie Biobank. Chinese Medical Journal 2023. https://doi.org/10.1097/CM9.0000000000002694
11. SCORE2 cardiovascular risk prediction models in an ethnic and socioeconomic diverse population in the Netherlands: an external validation study. EClinicalMedicine 2023. https://doi.org/10.1016/j.eclinm.2023.101862
12. Simultaneous derivation, validation, and comparison of predictor hazard ratios for cardiovascular risk prediction equations in patients with diabetes from high versus non-high income countries: cohort study. British medical journal 2026. https://doi.org/10.1136/bmj-2026-100535
13. Development of machine learning-based models to predict 10-year risk of cardiovascular disease: a prospective cohort study. Stroke and vascular neurology 2023. https://doi.org/10.1136/svn-2023-002332
14. Cardiovascular disease risk prediction using automated machine learning: A prospective study of 423,604 UK Biobank participants. PLoS ONE 2019. https://doi.org/10.1371/journal.pone.0213653
15. Validation of an Integrated Risk Tool, Including Polygenic Risk Score, for Atherosclerotic Cardiovascular Disease in Multiple Ethnicities and Ancestries.. American Journal of Cardiology 2021. https://doi.org/10.1016/j.amjcard.2021.02.032
16. Integration of lipidomic and polygenic risk scores within contemporary clinical cardiovascular risk assessment pathways: a multi-cohort development and validation study. EClinicalMedicine 2026. https://doi.org/10.1016/j.eclinm.2026.104159
17. Incremental predictive value of CMR phenotyping for major adverse cardiovascular events: an interpretable machine learning study from UK Biobank. Frontiers in Medicine 2026. https://doi.org/10.3389/fmed.2026.1852547
18. Simple Risk Model Predicts Incidence of Atrial Fibrillation in a Racially and Geographically Diverse Population: the CHARGE‐AF Consortium. Journal of the American Heart Association : Cardiovascular and Cerebrovascular Disease 2013. https://doi.org/10.1161/JAHA.112.000102
19. Development and Validation of a Prediction Model for Atrial Fibrillation Using Electronic Health Records.. JACC Clinical Electrophysiology 2019. https://doi.org/10.1016/j.jacep.2019.07.016
20. Plasma proteomic associations with genetics and health in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06592-6
21. A proteome atlas of structural variation and VNTR effects on complex traits and diseases.  . https://doi.org/10.64898/2026.09.26.26364064
22. Cross-population proteome-wide mendelian randomization study identifies likely causal proteins for cardiovascular diseases. Zeitschrift für Induktive Abstammungs- und Vererbungslehre 2026. https://doi.org/10.1007/s00438-026-02458-4
23. Large-scale plasma proteomics in the UK Biobank modestly improves prediction of major cardiovascular events in a population without previous cardiovascular disease. medRxiv 2024. https://doi.org/10.1101/2024.03.13.24304196
24. Interpretable machine learning leverages proteomics to improve cardiovascular disease risk prediction and biomarker identification. Communications Medicine 2024. https://doi.org/10.1038/s43856-025-00872-0
25. Integrating clinical, proteomics, and polygenic scores to improve cardiovascular risk prediction: a prospective cohort study.. Journal of Advanced Research 2026. https://doi.org/10.1016/j.jare.2026.06.034
26. Machine Learning‐Driven Prediction of Coronary Artery Disease Risk Based on UK Biobank Plasma Proteomics. Journal of the American Heart Association : Cardiovascular and Cerebrovascular Disease 2026. https://doi.org/10.1161/JAHA.125.047248
27. A Proteomics-Based Approach for Prediction of Different Cardiovascular Diseases and Dementia. Circulation 2024. https://doi.org/10.1161/CIRCULATIONAHA.124.070454
28. Proteomic Signatures for Risk Prediction of Atrial Fibrillation.. Circulation 2025. https://doi.org/10.1161/circulationaha.124.073457
29. Generalizability of proteomic risk prediction across biobanks reveals dependence on phenotype definitions.  . https://doi.org/10.64898/2026.10.01.26364038
30. Improving 10-year cardiovascular risk prediction in patients with type 2 diabetes with metabolomics. Cardiovascular Diabetology 2024. https://doi.org/10.1186/s12933-025-02581-3
31. The polyunsaturated-to-monounsaturated fatty acid ratio and cardiovascular risk prediction: a prospective cohort study of 183,237 adults. Lipids in Health and Disease 2025. https://doi.org/10.1186/s12944-025-02745-w
32. NMR metabolomics for cardiovascular-kidney-metabolic risk stratification in an integrated healthcare system.  . https://doi.org/10.64898/2026.10.01.26364322
33. A multi-ancestry polygenic risk score improves risk prediction for coronary artery disease. Nature Medicine 2023. https://doi.org/10.1038/s41591-023-02429-x
34. Improving the reliability of polygenic risk score-based prediction for cardiovascular and renal complications across ancestries in type 2 diabetes using Mondrian Cross-Conformal Prediction. PLoS Computational Biology 2026. https://doi.org/10.1371/journal.pcbi.1014670
35. An artificial intelligence-enabled ECG algorithm for the identification of patients with atrial fibrillation during sinus rhythm: a retrospective analysis of outcome prediction.. The Lancet 2019. https://doi.org/10.1016/S0140-6736(19)31721-0
36. Deep Neural Networks Can Predict New-Onset Atrial Fibrillation From the 12-Lead ECG and Help Identify Those at Risk of Atrial Fibrillation–Related Stroke. Circulation 2021. https://doi.org/10.1161/CIRCULATIONAHA.120.047829
37. Deep Learning of Electrocardiograms in Sinus Rhythm From US Veterans to Predict Atrial Fibrillation.. JAMA cardiology 2023. https://doi.org/10.1001/jamacardio.2023.3701
38. Prediction of Atrial Fibrillation from the Electrocardiogram in the Community Using Deep Learning: A Multinational Study. Circulation: Arrhythmia and Electrophysiology 2025. https://doi.org/10.1161/CIRCEP.125.013734
39. Multicenter validation of an artificial intelligence-enabled ECG model to predict 1-year risk of atrial fibrillation or flutter.. Heart Rhythm 2026. https://doi.org/10.1016/j.hrthm.2026.03.1956
40. Heart failure risk stratification using artificial intelligence applied to electrocardiogram images: a multinational study.. European heart journal 2025. https://doi.org/10.1093/eurheartj/ehae914
41. Prospective validation of an ensemble deep learning algorithm for detecting structural heart disease using real-world 12-lead electrocardiogram images. European Heart Journal 2025. https://doi.org/10.1093/eurheartj/ehaf784.4483
42. Deep learning prediction of left atrial structure and function from 12-lead electrocardiograms. Nature Communications 2026. https://doi.org/10.1038/s41467-026-76155-6
43. CARDIAC-FM: A Multimodal Foundation Model for Cardiovascular Risk Prediction Using ECG and Cardiac MRI. medRxiv 2026. https://doi.org/10.64898/2026.03.16.26348526
44. Multimodal foundation model for evaluating cardiovascular disease from electrocardiography and echocardiography. European Heart Journal 2025. https://doi.org/10.1093/eurheartj/ehaf784.4471
45. A self-supervised electrocardiogram foundation model for empowering cardiovascular disease prediction and genetic factor discovery. Nature Communications 2026. https://doi.org/10.1038/s41467-026-72436-2
46. ECG-FM: an open electrocardiogram foundation model.. JAMIA open 2025. https://doi.org/10.1093/jamiaopen/ooaf122
47. Artificial intelligence-enabled electrocardiogram for mortality and cardiovascular risk estimation: a model development and validation study.. The Lancet. Digital health 2024. https://doi.org/10.1016/s2589-7500(24)00172-9
48. Protein biomarkers for predicting incident carotid plaque: a nested case-control study in the ChinaHEART cohort with transportability assessment in the UK Biobank.. BMJ open 2026. https://doi.org/10.1136/bmjopen-2025-110220
49. Early adulthood BMI and cardiovascular disease: a prospective cohort study from the China Kadoorie Biobank. Lancet Public Health 2024. https://doi.org/10.1016/s2468-2667(24)00043-4
50. Incorporating a Polygenic Risk Score-Triaged Coronary Calcium Score into Cardiovascular Disease Examinations to Identify SubClinicAL coronAry arTEry Disease (ESCALATE): Protocol for a Prospective, Non-Randomised Implementation Trial.. American Heart Journal 2023. https://doi.org/10.1016/j.ahj.2023.06.009
51. SCORE2 risk prediction algorithms: new models to estimate 10-year risk of cardiovascular disease in Europe.. European Heart Journal 2021. https://doi.org/10.1093/eurheartj/ehab309
52. Development and validation of QRISK3 risk prediction algorithms to estimate future risk of cardiovascular disease: prospective cohort study. British medical journal 2017. https://doi.org/10.1136/bmj.j2099
53. High Throughput Plasma Proteomics and Risk of Heart Failure and Frailty in Late Life.. JAMA cardiology 2024. https://doi.org/10.1001/jamacardio.2024.1178
54. Proteomic signatures as biomarkers of atherosclerosis burden.. Cardiovascular Research 2026. https://doi.org/10.1093/cvr/cvag140
55. Plasma proteomics enhances heart failure risk prediction among individuals with type 2 diabetes: a prospective cohort study.. American Journal of Clinical Nutrition 2026. https://doi.org/10.1016/j.ajcnut.2026.101216
56. Chronic kidney disease onset, progression, and cardiovascular outcomes: proteomics informs biology and risk stratification. Cardiovascular Diabetology 2026. https://doi.org/10.1186/s12933-025-03049-0
57. Improved sex-specific cardiovascular risk prediction with multi-omics data in people with type 2 diabetes. Cardiovascular Diabetology 2025. https://doi.org/10.1186/s12933-025-03036-5
58. A polygenic risk score improves risk stratification of coronary artery disease: a large-scale prospective Chinese cohort study. European Heart Journal 2022. https://doi.org/10.1093/eurheartj/ehac093
59. Prediction of Atrial and Ventricular Arrhythmias using Multiple Cardiovascular Risk Factor Polygenic Risk Scores.. Heart Rhythm 2024. https://doi.org/10.1016/j.hrthm.2024.12.017
60. Cross-ancestry genome-wide analysis of atrial fibrillation unveils disease biology and enables cardioembolic risk prediction. Nature Genetics 2023. https://doi.org/10.1038/s41588-022-01284-9
61. Performance of Cardiovascular Polygenic Risk Scores in Carotid Stenosis Identification. medRxiv 2026. https://doi.org/10.64898/2026.06.22.26356289
62. Clinical Utility of Lipoprotein(a) and LPA Genetic Risk Score in Risk Prediction of Incident Atherosclerotic Cardiovascular Disease. JAMA cardiology 2020. https://doi.org/10.1001/jamacardio.2020.5398
63. Interactions between Enhanced Polygenic Risk Scores and Lifestyle for Cardiovascular Disease, Diabetes Mellitus and Lipid Levels. Circulation Genomic and Precision Medicine 2021. https://doi.org/10.1161/CIRCGEN.120.003128
64. Decomposing polygenic risk of coronary artery disease into distinct biological processes.  . https://doi.org/10.64898/2026.10.08.26365088
65. Frailty-Related Metabolic Signature in the Association Between Frailty and Coronary Artery Disease: Modification by Genetic Susceptibility.. The journal of nutrition, health & aging . https://doi.org/10.1016/j.jnha.2026.100998
66. Neutrophil counts and cardiovascular disease.. European heart journal 2023. https://doi.org/10.1093/eurheartj/ehad649
67. Identification of lipid quantitative trait loci linked with cardiometabolic disease in Asian Indians and Europeans: A genome-wide association study and Mendelian randomization. PLoS Medicine 2026. https://doi.org/10.1371/journal.pmed.1005039
68. Phenome-wide and proteomic analysis of APOE alleles across different ancestries in the All of Us Research Program.  . https://doi.org/10.64898/2026.09.26.26364080
69. Age Acceleration and Mortality Risk Constitute Distinct Dimensions of Organ Aging.  . https://doi.org/10.21203/rs.3.rs-10881849/v1
70. Polygenic Risk Scores for Cardiovascular Disease: A Scientific Statement From the American Heart Association. Circulation 2022. https://doi.org/10.1161/CIR.0000000000001077
71. Proteomics and lipidomics in atherosclerotic cardiovascular disease risk prediction. European Heart Journal 2023. https://doi.org/10.1093/eurheartj/ehad161
72. Electrocardiogram-based Deep Learning and Clinical Risk Factors to Predict Atrial Fibrillation. Circulation 2021. https://doi.org/10.1161/CIRCULATIONAHA.121.057480
73. Incident atrial fibrillation prediction using ECG-based deep learning at a specialized tertiary cardiac care center. European Heart Journal 2024. https://doi.org/10.1093/eurheartj/ehae666.3479
74. Artificial Intelligence-Enabled Prediction of Heart Failure Risk From Single-Lead Electrocardiograms.. JAMA cardiology 2025. https://doi.org/10.1001/jamacardio.2025.0492
75. Deep learning analysis of single-lead electrocardiograms enables pragmatic heart failure risk assessment in the general population. European Heart Journal - Digital Health 2026. https://doi.org/10.1093/ehjdh/ztag099
76. Screening for cardiac contractile dysfunction using an artificial intelligence–enabled electrocardiogram. Nature Medicine 2019. https://doi.org/10.1038/s41591-018-0240-2
77. Abstract 4354222: Deep Learning Prediction of Left Atrial Structure and Function from 12-lead Electrocardiograms. Circulation 2025. https://doi.org/10.1161/circ.152.suppl_3.4354222
78. Multimodal Electronic Health Record Foundation Models with Electrocardiogram for Cardiovascular Disease Prediction. medRxiv 2025. https://doi.org/10.1101/2025.11.10.25339886
79. Mortality risk prediction of the electrocardiogram as an informative indicator of cardiovascular diseases. Digital Health 2023. https://doi.org/10.1177/20552076231187247
80. Decoding 2.3 million ECGs: interpretable deep learning for advancing cardiovascular diagnosis and mortality risk stratification.. European heart journal. Digital health 2024. https://doi.org/10.1093/ehjdh/ztae014
81. Electrocardiogram-Based Artificial Intelligence to Identify Coronary Artery Disease.. JACC. Advances 2025. https://doi.org/10.1016/j.jacadv.2025.102041
82. ECG Signatures and Long-Term Ischemic Stroke Risk: A Deep Learning Analysis of 200,000 Patients.. Journal of the American College of Cardiology 2026. https://doi.org/10.1016/j.jacc.2026.03.084
83. Abstract 4141180: Opportunistic assessment of cardiovascular risk using deep learning of the heart and aorta on non-contrast chest computed tomography. Circulation 2024. https://doi.org/10.1161/circ.150.suppl_1.4141180
84. A deep-learning-based retinal cardiovascular disease biomarker and risk of stroke, myocardial infarction, atrial fibrillation, and heart failure in the UK Biobank. European Heart Journal 2023. https://doi.org/10.1093/eurheartj/ehad655.2920
85. A curated reference dataset and deep learning model for multi-lead electrocardiographic interval measurements in UK Biobank. medRxiv 2026. https://doi.org/10.64898/2026.06.26.26356665
86. Population prevalence of ECG abnormalities and risk of incident CVD outcomes: 5-year follow-up of 25,000 Chinese adults. European Heart Journal 2023. https://doi.org/10.1093/eurheartj/ehad655.2380
87. Machine learning and deep learning predictive models for prognosis in patients with atrial fibrillation: a systematic review and meta-analysis. BMJ digital health & AI 2025. https://doi.org/10.1136/bmjdhai-2025-000154
88. Prediction of Atrial Fibrillation Risk Through the Integration of Genetic Information and Artificial Intelligence-Based Electrocardiogram Data.. Journal of arrhythmia . https://doi.org/10.1002/joa3.70463
89. Incorporating a polygenic risk score into cardiovascular disease examinations to identify subclinical coronary artery disease: rationale and design of the ESCALATE trial. European Heart Journal 2023. https://doi.org/10.1093/eurheartj/ehad655.1337
90. High-dimensional phenotypic matching with artificial intelligence-enhanced ECG to replicate heart failure trial outcomes in real-world data. European Heart Journal 2025. https://doi.org/10.1093/eurheartj/ehaf784.4614
91. Abstract 4140651: Effect of Statin Therapy on Cardiovascular Events in High-Risk Group Identified by a Coronary Artery Calcium-Trained Deep Learning Model Using Retinal Imaging: A Propensity Score-Matched Study from the UK Biobank. Circulation 2024. https://doi.org/10.1161/circ.150.suppl_1.4140651
92. Shared proteomic landscape between arteriosclerosis and cardiovascular endpoints: a Mendelian randomization and observational study integrating AlphaFold3 for structural prediction. medRxiv 2025. https://doi.org/10.1093/cvr/cvag095
93. Integrating Imaging-Derived Clinical Endotypes with Plasma Proteomics and External Polygenic Risk Scores Enhances Coronary Microvascular Disease Risk Prediction. medRxiv 2025. https://doi.org/10.1142/9789819824755_0045
94. A deep learning-based electrocardiogram risk score for long term cardiovascular death and disease. npj Digit. Medicine 2023. https://doi.org/10.1038/s41746-023-00916-6
95. Metabolomics data improve 10-year cardiovascular risk prediction with the SCORE2 algorithm for the general population without cardiovascular disease or diabetes. medRxiv 2024. https://doi.org/10.1101/2024.04.29.24306593
96. A plasma proteomic signature for atherosclerotic cardiovascular disease risk prediction in the UK Biobank cohort. medRxiv 2024. https://doi.org/10.1101/2024.09.13.24313652
97. Abstract 14071: Plasma Protein Concentrations and Risk of Incident Cardiovascular Diseases in the UK Biobank. Circulation 2023. https://doi.org/10.1161/circ.148.suppl_1.14071
98. Transformer-based models for predicting cardiovascular risk in Chinese adults: development and validation.. European Heart Journal 2026. https://doi.org/10.1093/eurheartj/ehag517
99. Abstract 18742: Matrilysin (MMP7) as a Robust Predictor of Hypertension Incidence and Complications: Findings From a Proteomic Analysis in the Atherosclerosis Risk in Communities (ARIC) Study. Circulation 2023. https://doi.org/10.1161/circ.148.suppl_1.18742
100. Cardiovascular Event Prediction by Machine Learning: The Multi-Ethnic Study of Atherosclerosis. Circulation Research 2017. https://doi.org/10.1161/CIRCRESAHA.117.311312
