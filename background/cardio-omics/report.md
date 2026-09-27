# 心血管队列多组学与临床 AI · 方向背景报告

证据 92 篇 · 覆盖度 0.66 · 第 7 轮 · 更新 2026-09-27 · 数字核验删句 9

## 摘要（TL;DR）

- China-PAR 基于 4 个中国当代队列开发性别特异性方程，男性 C 统计量 0.794、女性 0.811，12 年随访 1048 例首发 ASCVD [1]。
- 同一模型在 CKB 吴忠子队列 42937 人与 JBPCD 14125 人中一般人群 C 统计量 0.723-0.778，而糖尿病人群仅 0.584-0.629 [2]。
- 新西兰 47958 人与中国 46558 人 T2D 无 CVD 队列中，女性每 10 年年龄风险比新西兰 1.61、中国 2.51，标准重校准未能改善中国队列校准 [3]。
- UK Biobank 473611 名无 CVD 者、645 个候选变量中筛出 10 个预测因子的 UKCRP，AUC 0.762±0.010，但出血性卒中仅 0.644 [4]。
- CHARLS 8080 名≥45 岁无基线 CVD 者随访 9 年，GBM 的 AUC 0.828 为十种模型最高，但缺乏外部验证 [5]。
- SCORE2 基于 13 国 45 队列 677684 人、30121 例 CVD 事件推导，外部 25 队列 113 万人验证，C-index 0.67-0.81 [6]。
- QRISK3 在 UK Biobank 中独立外部验证显示区分度中等且随年龄下降，系统性高估 CVD 风险，老年参与者高估达 20% [7]。
- ASCVD-IRT 将 PRS 与 ASCVD-PCE 结合，NRI 在白人 2.7%、黑人 2.5%、南亚 8.7%，西班牙裔 7.5% 但置信区间含 0 [8]。
- Pharma Proteomics Project 在 54,219 名 UK Biobank 参与者中表征血浆蛋白组，对 2,923 个蛋白进行 pQTL 定位，鉴定 14,287 个主要遗传关联，其中 81% 为新发现 [9]。
- UKB-PPP 41,931 人中稀疏蛋白模型显示 163 种疾病 5 蛋白即媲美临床模型，67 种疾病加 5-20 蛋白显著提升，中位 ΔC-index=0.07（0.02-0.31）[10]。
- 基于 UKB-PPP 51,680 人、1,459 个蛋白开发的 165 蛋白 Lasso-Cox 风险评分，加入 CHARGE-AF、NT-proBNP 和多基因风险评分后 C 指数由 0.771 升至 0.816 [11]。
- 多中心外部验证显示模型判为高风险的 391 例里 74 例发生房颤，敏感性 31%（95%CI 25–37），提示单机构评估可能高估泛化能力 [12]。
- 房颤患者预后 AI 模型的系统综述与 Meta 分析显示 AI 模型总体呈现中等至良好区分度，但多数研究缺乏外部验证、偏倚风险高、报告不完整 [id:10.1136/bmjdhai-2025-000154]。

## 1 背景与定义

**方向边界与演化脉络**：本方向的核心，是在**万人级以上人群队列/生物样本库**上，把心血管病（冠心病、心衰、房颤、卒中、高血压、动脉粥样硬化）的风险预测与机制发现，从传统临床评分推进到「多组学 + 临床 AI」的联合建模。其边界由三条线划定：一是**规模线**，纳入标准要求 ≥万人队列并含外部验证，排除单中心 <1000 人的关联研究；二是**模态线**，涵盖血浆蛋白组（Olink/SomaScan）、代谢组、脂质组、PRS、pQTL/MR，以及 ECG/影像 AI 与 EHR 的联合，排除纯介入/器械报告与单一标志物横断面描述；三是**转化线**，从风险预测延伸到筛查—干预闭环与实用性试验设计。演化上，这一方向经历了从「传统方程跨人群校准」到「机器学习变量筛选」再到「多组学增量 + 基础模型」的迁移：China-PAR 以 4 个中国队列推导性别特异方程（男 C=0.794、女 C=0.811）[1]，SCORE2 基于 13 国 45 队列 677684 人推导、25 队列 113 万人外部验证（C-index 0.67-0.81）[6]，而 UKCRP 从 645 个候选变量中数据驱动筛出 10 个预测因子（AUC 0.762±0.010）[4]，标志着范式从「预设变量」转向「高维数据驱动」。

**核心问题之一：跨人群校准与迁移**。这是贯穿本方向所有子领域的第一性问题。中国糖尿病人群中 China-PAR 的 C 统计量低至 0.584-0.629，标准重校准未能改善部分队列校准 [2][3]；QRISK3 在 UK Biobank 中系统性高估 CVD 风险、老年参与者高估达 20% [7]；SCORE2 在荷兰族裔与社会经济多样化人群中，按高危亚组调整后治疗资格人数几乎翻倍（男 10%→17%，女 2%→5%）[13]。**跨人群迁移不是单一模型的校准问题，而是预测因子效应本身不可完全移植**：新西兰与中国 T2D 队列中女性每 10 年年龄风险比分别为 1.61 与 2.51，标准重校准无效 [3]。PRS 同样如此：GPS_Mult 整合五 ancestry GWAS（>269,000 病例、>1,178,000 对照）后在多族裔外部验证中优于既往 CAD 评分 [14]，但中国嘉道理生物库中每 SD 对硬 CAD 的 HR 仅 1.26，加入传统模型后 Harrell C 男性增 0.003、女性增 0.001 [15]；跨祖先房颤 GWAS 的 PRS 可迁移性仍有限 [16]。**Mondrian 交叉共形预测（MCCP）** 尝试用不确定性量化控制跨祖源错误率并识别不可靠预测个体，但非欧人群样本量小、PRS 原始开发仍以欧洲为主 [17]。

**核心问题之二：多组学的增量价值及其边界**。蛋白组预测在多个终点上显示增量，但幅度与可外推性存在争议。UKB-PPP 41,931 人中稀疏蛋白模型对 218 种疾病 10 年发病预测，**163 种疾病 5 蛋白即媲美临床模型**，67 种疾病加 5-20 蛋白显著提升（中位 ΔC-index=0.07）[10]；117 蛋白 ProtRS 的 C-index 0.769，优于 SCORE2 0.667、PREVENT 0.645、FRS 0.672，加入基线模型后 C-index 由 0.669 升至 0.774 [18]；房颤方向 165 蛋白 Lasso-Cox 评分加入 CHARGE-AF、NT-proBNP 和 PRS 后 C 指数由 0.771 升至 0.816，并在 ARIC 外部验证 [11]。但另一项 UKB 研究结论更保守：SCORE2 AUC 0.740，114 蛋白单独预测 0.758，联合升至 0.771（NRI 0.140），与 10 项 TRF 联合仅 0.767（NRI 0.053），随机选 114 个蛋白无改善，**作者认为改善幅度有限且仅限 UKB 人群** [19]。综述亦指出蛋白组和脂质组研究一致显示区分度与重分类改善，但**尚未被当前预防指南采纳** [20]。机制层面，Pharma Proteomics Project 对 2,923 个蛋白 pQTL 定位、鉴定 14,287 个主要遗传关联（81% 为新发现）[9]，但该资源以欧洲 ancestry 为主；跨人群蛋白组 MR 评估五类 CVD 的因果蛋白，跨人群遗传结构评估仍不完整 [21]；UKB 与 CKB 联合分析发现 636 个蛋白与 MI/IS/HF 相关、47 个具遗传预测关联，但**多数观察性关联非因果** [22]。

**核心问题之三：ECG/影像 AI 的泛化与终点定义**。ECG AI 已从单任务走向多终点、多模态与基础模型，但外部验证时区分度普遍下降，且终点定义显著影响性能。窦律期预测房颤的早期工作把「电信号特征识别」作为筛查切入点 [23]，Geisinger 在 160 万份 ECG 上模拟监测部署，报告近三分之二房颤相关卒中患者在卒中前被预测为高风险 [24]；但多中心外部验证给出更保守的数字：3 个中心 4,017 例中模型判为高风险者敏感性仅 31%（95%CI 25-37）[12]。心衰方向 AI-ECG 阳性者风险比 3.88-23.50，C 统计量 0.718-0.810 [25]；左房结构估计与 CMR 仅中度相关（r=0.40-0.50），但与 AF、卒中、心衰独立相关 [26][27]。**基础模型正在改变建模范式**：CARDIAC-FM 在 57,609 对 ECG-CMR 上对比学习，所有队列优于单模态 [28]；ECG-LFM 用 1,157 万份 ECG 预训练，平均 AUROC 0.930，并通过 GWAS 发现 11 个位点 [29]；ECG-FM 公开权重、代码与基准 [30]。**但终点定义（ICD 编码 vs 人工抽象）与随访长度对性能的影响，仍是这一子领域最未被系统解决的争议** [31]。

**核心问题之四：从预测到筛查—干预闭环**。本方向区别于纯预测研究的标志，是能否形成可复用的临床转化证据。ESCALATE 把 CAD PRS 纳入初级保健风险评估、对 5 年绝对风险低/中危者计算 PRS、将 CAD PRS≥80% 者转诊冠脉钙化扫描，主要结局为亚临床 CAD（CACS>0 AU），但**目前处于方案阶段，尚无疗效、体验和成本效果结果** [32][33]。房颤 AI 预后的系统综述与 Meta 分析纳入使用 ML/DL 预测房颤患者临床结局的研究，采用 TRIPOD+AI 和 PROBAST+AI 评估，结果显示 **AI 模型总体呈中等至良好区分度、在同一数据集上多优于风险评分和回归模型**，但**多数研究缺乏外部验证、偏倚风险高、报告不完整** [34]。中国本土的转化证据仍稀缺：CHARLS 的 GBM 模型 AUC 0.828 但缺乏外部验证 [5]；开滦 T2DM 队列的 ML-CVD-C 整合 4 年风险因子轨迹，优于仅用基线变量模型 [35]；ChinaHEART 巢式病例对照检测 28 种蛋白并评估对传统模型的增量价值、在 UKB 评估可迁移性，但**未给出具体效应量或迁移性能数值** [36]。**筛查—干预闭环的临床转化证据，是本方向从「预测性能」走向「健康收益」的关键缺口**。

## 2 方法学


### 2.1 心血管风险预测与疾病轨迹模型

**中国人群的10年ASCVD风险预测**长期依赖西方推导的方程，China-PAR项目基于4个中国当代队列（推导21320人，外部验证14123与70838人）开发性别特异性方程，**男性C统计量0.794、女性0.811**，校准χ²男13.1（P=0.16）、女12.8（P=0.17），12年随访1048例首发ASCVD [1]。但同一模型在不同人群中的表现并不一致：在CKB吴忠子队列42937人与JBPCD 14125人中，一般人群C统计量0.723-0.778，而糖尿病人群仅0.584-0.629，原模型E/O在一般人群为1.47-3.78、糖尿病为0.32-2.70，重校准后CKB-CVD高风险组预测48.4%、实际10年风险25.7% [2]。跨国比较进一步显示预测因子效应不可完全移植：新西兰47958人与中国46558人T2D无CVD队列中，新西兰5年CVD事件5622例（11.7%）、中国3650例（7.8%），女性每10年年龄风险比新西兰1.61、中国2.51，标准重校准未能改善中国队列校准 [3]。

**机器学习被用于突破传统变量筛选的局限**。UK Biobank 473611名无CVD者、645个候选变量中数据驱动筛出10个预测因子的UKCRP，**AUC 0.762±0.010**、Brier 0.057±0.006，10年内31466人发生CVD，心肌梗死AUC 0.774、缺血性卒中0.730，但出血性卒中仅0.644 [4]。AutoPrognosis在UK Biobank 423604人、473个变量上构建模型，与Framingham等传统算法比较，提示机器学习可整合大量变量与复杂交互 [37]。

**中国本土的深度学习与可解释模型**也在推进。CHARLS 8080名≥45岁无基线CVD者随访9年，从77个候选变量筛出11个预测因子，GBM的**AUC 0.828**为十种模型最高，Logistic为0.792，验证集n=2423，并提供网络风险计算器，但缺乏外部验证 [5]。开滦队列16378名中国T2DM患者用功能主成分分析提取4年风险因子轨迹构建ML-CVD-C，整合纵向轨迹的模型优于仅用基线变量模型，并与PREVENT、China-PAR、SCORE-2D、ADVANCE比较 [35]。

**欧洲模型的跨人群校准问题**同样突出。SCORE2基于13国45队列677684人、30121例CVD事件推导，外部25队列113万人验证，**C-index 0.67-0.81**，50岁吸烟男性10年风险5.9%-14.0% [6]。在荷兰族裔与社会经济多样化人群中，按高危亚组调整至高危欧洲国家SCORE2模型后，符合治疗资格人数几乎翻倍（男10%→17%，女2%→5%）[13]。QRISK3基于QResearch 1998-2015年25-84岁开放队列开发，纳入HIV/AIDS、SLE、严重精神疾病、勃起功能障碍、偏头痛和血压变异性等新增因素 [38]；但在UK Biobank中独立外部验证显示其**区分度中等且随年龄下降，系统性高估CVD风险，老年参与者高估达20%**，提示需重新校准或开发定制模型 [7]。

**多组学与影像标志物的增量价值**是另一条主线。UK Biobank 306654人中加入CHD和卒中PRS可改善判别与重分类，并用CPRD 210万人模拟按指南启动他汀的临床影响，同时比较PRS与CRP的增量价值 [39]。ASCVD-IRT将PRS与ASCVD-PCE结合，**NRI在白人2.7%、黑人2.5%、南亚8.7%**，西班牙裔7.5%但置信区间含0，部分族裔样本小、CI宽 [8]。多澳大利亚队列在AusCVDRisk基础上加入高维脂质组学与基因组信息，联合模型改善中间风险人群再分层，正确上调未来事件并识别亚临床斑块负担者，但需前瞻性真实世界验证 [40]。UKBB CMR 27254人中，可解释机器学习整合CMR表型与15个临床风险因子提升MACE预测，并在西安交大附二院522人超声队列做跨模态可迁移性评估，但超声替代CMR存在测量精度与定义差异 [41]。

**心衰与房颤的专项预测**呈现不同技术路径。房颤方面，CHARGE-AF在ARIC、CHS、FHS合并的18556例中推导、7672例5队列验证，模型含常规临床变量、部分无需12导联ECG，摘要未给AUC等具体数值 [42]；而基于多机构EHR 412085例45–95岁人群（14334例新发AF）的5年房颤模型，**验证C-statistic 0.777（95%CI 0.771–0.783）、校准0.99**，判别与校准优于CHARGE-AF的0.753，但依赖编码变量、外部验证有限 [43]。

**争议与共性局限**集中在三点：其一，模型跨人群校准普遍不佳，中国糖尿病人群C统计量低至0.584-0.629 [2]，QRISK3在UKB高估达20% [7]，SCORE2在荷兰多元人群中治疗资格人数近乎翻倍 [13]，而标准重校准对部分队列无效 [3]；其二，机器学习虽在多数研究中判别力占优 [44][5]，但UKCRP对出血性卒中预测较差 [4]，且多数模型缺乏外部验证 [5]；其三，PRS与组学标志物的增量价值在不同族裔间差异明显，南亚NRI 8.7%而西班牙裔置信区间含0 [8]，临床效用仍不确定 [39]。

### 2.2 心血管多组学与遗传整合

血浆蛋白组遗传学研究已形成大规模开放资源。**Pharma Proteomics Project** 在 **54,219 名 UK Biobank 参与者**中表征血浆蛋白组，对 2,923 个蛋白进行 pQTL 定位，鉴定 **14,287 个主要遗传关联**，其中 **81% 为新发现**，并在 n=17,806 的复制队列中验证；研究还揭示跨生物域的 trans pQTL、配体-受体相互作用与通路扰动，以及 ABO 和 FUT2 对胃肠组织富集蛋白的远距离上位效应 [9]。该资源以欧洲 ancestry 为主，非欧样本量小 [9]。跨人群蛋白组孟德尔随机化进一步将 UKB-PPP 的 2,922 个蛋白与非洲、东亚、欧洲人群 GWAS 结合，系统评估其对 AF、CAD、HF、IHD、PAD 的潜在因果作用，但跨人群遗传结构评估仍不完整 [21]。

观察性蛋白组关联研究覆盖多种心血管终点。在 UKB 47,665 名无 CVD 个体、1,459 个 Olink 蛋白、随访 11.1 年的分析中，CAD、AF、HF、AS 分别有 270、156、385、21 个显著蛋白关联，事件数分别为 2,941、2,502、1,470、420 [45]。另一项研究在 UKB 52,164 人中测量 2,919 个蛋白，发现 636 个蛋白与 MI、IS 或 HF 任一相关，126 个与三类 CVD 均相关，118 个在中国慢性病前瞻性队列（1,937 人）复制；MR 提示 47 个蛋白与 CVD 相关，18 个共定位，但多数观察性关联非因果，部分 MR 蛋白在心脏或动脉表达弱 [22]。ARIC 队列用 SomaScan v4 测量 4,877 个 aptamer，识别心衰与衰弱的共享通路，并用 MR 评估候选蛋白的潜在因果效应 [46]。

该研究受 MR 假设限制，需实验验证 [47]。中性粒细胞计数的观察性队列（CGPS 101,730 人）结合 MR 发现，中性粒细胞升高与九类心血管终点风险增加一致相关，遗传证据支持潜在因果性，而淋巴、单核、嗜碱和嗜酸细胞关联不一致 [48]。

蛋白组风险预测模型在多个终点上显示增量价值。在 UKB-PPP 41,931 人中，稀疏蛋白模型（5-20 个蛋白）对 218 种疾病 10 年发病进行预测，临床模型中位 C-index=0.64；**163 种疾病 5 蛋白即媲美临床模型**，另 30 种更优；67 种疾病加 5-20 蛋白显著提升，中位 ΔC-index=0.07（0.02-0.31），多发性骨髓瘤 Δ=0.25，非霍奇金淋巴瘤 Δ=0.21 [10]。该研究部分疾病病例数有限，初级保健数据仅部分个体可得 [10]。

针对 MACE 的预测研究结论存在差异。在 UKB 38,380 名参与者、2,919 个蛋白中，SCORE2 AUC 0.740，数据驱动选出 114 个蛋白单独预测 AUC 0.758，与 SCORE2 联合升至 0.771（NRI 0.140），与 10 项 TRF 联合为 0.767（NRI 0.053），而随机选 114 个蛋白无改善；作者认为改善幅度有限且仅限 UKB 人群 [19]。另一项 UKB 研究用可解释提升机（EBM）在 46,009 名无基线 CVD 参与者中预测 10 年首发冠脉疾病、缺血性卒中或心梗，蛋白组模型 AUROC 0.767、AUPRC 0.241，加入临床特征后升至 0.785 和 0.284，优于 PREVENT 等方程评分及多个 PRS [49]。在 UKB 51,859 人（平均 56.7 岁，45.5% 男性，中位随访 13.6 年，4,857 例 MACE）中，NT-proBNP HR 1.68/SD，蛋白模型在校准、重分类和 C 统计量上优于 PREVENT [50]。基于 UKB-PPP 44,431 名无 CVD 参与者、Olink 1,460 蛋白构建的 **117 蛋白 ProtRS** C-index 0.769，优于 SCORE2 0.667、PREVENT 0.645、FRS 0.672；加入基线模型后 C-index 由 0.669 升至 0.774，ΔC=0.105 [18]。这些研究均以 UKB 为主，需外部验证 [50][18]。

冠心病专项预测中，一项研究用 LASSO Cox 推导 **202 蛋白风险评分**并用 CatBoost 建模，内部验证 AUC 从 0.750（0.732-0.767）升至 0.789（0.772-0.805），外部验证从 0.717（0.683-0.750）提升；中位年龄 58 岁，约 45% 男性 [51]。该蛋白评分需外部多队列进一步验证 [51]。另一项 UKB 研究在 41,650 人中整合临床变量、QRISK3、血脂、36 个 PRS 和 2,920 个 Olink 蛋白，采用 LASSO 及稳定性选择并用两样本 MR 识别潜在因果蛋白，但摘要未报告具体 AUC 或 ΔAUC [52]。综述指出，蛋白组和脂质组研究一致显示相较临床特征风险评分在区分度和重分类上有改善，但尚未被当前预防指南采纳 [20]。

房颤蛋白组预测进展显著。基于 UKB-PPP 51,680 人、1,459 个蛋白开发的 **165 蛋白 Lasso-Cox 风险评分**，1-SD 风险比 2.20，加入 CHARGE-AF、NT-proBNP 和多基因风险评分后 C 指数由 0.771 升至 0.816，并在 ARIC（11,012 人）外部验证 [11]。该研究蛋白检测平台和人群差异可能影响外推 [11]。在 UKB 158,733 名欧洲裔中，AF 模型加入 AF-PRS 后 C 指数 0.762 vs 0.746（P<0.001），再加 CV-PRS 为 0.765；VA 模型加入 CAD-PRS 后 C 指数 0.692 vs 0.681（P<0.001），非欧洲裔样本量较小，VA 预测增益有限 [53]。

动脉粥样硬化负荷与亚临床表型的蛋白组特征也在探索中。在 UKB 嵌套匹配病例对照（1,666 对，Olink 2,920 蛋白）中训练四种 **AtheroBurden 特征**，在 41,200 名无病者中计算评分，并通过颈动脉超声、13.7 年 MACE 随访及 KORA 外部队列验证，显示可反映系统性动脉粥样硬化负荷并改善 MACE 预测和风险重分类 [54]。颈动脉狭窄方面，在 Mass General Brigham Biobank 的 670 例病例和 52,636 例对照中，IS PRS OR 1.31、CAD PRS OR 1.62、PAD PRS OR 1.66（均 p<0.0001），cIMT PRS 无关联；PAD PRS ΔC 统计量 0.017，C 0.845；病例以欧洲裔为主，表型依赖 ICD/CPT 算法 [55]。

多基因风险评分本身在多 ancestry 和跨疾病场景中持续改进。**GPS_Mult** 整合五个 ancestry 的 CAD GWAS（>269,000 病例、>1,178,000 对照）及十项危险因素，在 UKB 116,649 名欧洲 ancestry 个体中训练、325,991 人独立验证；患病 CAD OR/SD 2.14，事件 CAD HR/SD 1.73，识别 20.0% 人群风险增 3 倍、13.9% 风险降 3 倍，并在多族裔外部验证中优于所有既往 CAD 评分 [14]。但跨人群迁移仍是问题：中国嘉道理生物库训练 28,490、测试 72,150 人，测试集 11.2 年随访 1,214 例硬 CAD、7,201 例软 CAD，最优 PRS 每 SD 对硬 CAD 的 HR 1.26，加入传统模型后 Harrell C 男性增 0.003、女性增 0.001，最高 NRI 3.2%，对软 CAD 改善极小 [15]。东亚 metaPRS 在 China-PAR 41,271 人中显示可改善 CAD 风险分层并评估终生风险轨迹 [56]。跨祖先房颤 GWAS 中，BBJ 发现 31 个位点（5 个新位点），跨祖先共 49 个独立信号，SNP h² 6.1%、liability h² 11.7%，但 PRS 跨祖先可迁移性仍有限 [16]。AHA 科学声明指出多基因风险评分可捕捉群体遗传易感性，成本下降推动大规模遗传分析，但临床效用、公平性和实施路径仍不明确 [57]。

PRS 与生活方式、代谢物的交互及联合建模是另一方向。在 UKB 276,096 名无亲缘关系白人中发现 AnnoPred 预测最优，健康生活方式在不同 PRS 组相对风险降低相似，但高 PRS 者绝对风险降低更大，如 T2D 最高 1% PRS 组 ARR 12.4% vs 最低十分位 2.8% [58]。在 2 型糖尿病人群中，UKB 10,257 例和 ESTHER 1,039 例选出 7 种代谢物加入 SCORE2-Diabetes，UKB 内部验证 C 指数从 0.660 升至 0.678（P=0.037），ESTHER 外部验证增 0.043（P=0.011），白蛋白、omega-3 百分比、乳酸改善区分度 [59]。PUFA/MUFA 比值加入 SCORE2 后，UKB 183,237 人验证集（54,971 人）C 指数从 0.740 升至 0.744（P<0.001），NRI 7.5%、IDI 0.025，比值每增 1 单位 MACE 风险 HR 1.21，改善幅度较小 [60]。

2 型糖尿病人群的多组学整合研究显示性别特异性和联合建模潜力。一项研究基于 UKB 蛋白组（1,751 人）和多组学（990 人）开发性别特异性蛋白算法，在 SCORE2-Diabetes 基础上加入 7 个性别特异代谢物和 CVD-PRS 进一步改善预测，但样本量较小、主要为 White 人群、需外部验证 [61]。在 UKB 2,198 例 T2D、2,920 个血浆蛋白、中位随访 13.1 年的研究中，298 例新发心衰，455 个蛋白相关，WAP 4-disulfide core domain protein 2 风险最高，蛋白组数据可增强超越临床变量、多基因风险和 NT-proBNP 的预测 [62]。CKD 与心血管结局方面，UKB 44,779 名无 CKD 参与者中，598 个蛋白跨至少两种疾病共享、471 个疾病特异，POLR2F、TNFRSF10B、IGFBP2 与 CKD、ESKD、CHD、卒中、心衰全部五种疾病正相关，加入预测蛋白改善 CKD、CHD、卒中和心衰预测 [63]。

跨祖源可靠性与不确定性量化开始受到关注。在 UKBB T2D 19,468 人（WB 17,574、SA 1,145、AFR 749）及 ADVANCE 试验中，**Mondrian 交叉共形预测（MCCP）** 提升跨祖源 PRS 预测可靠性与不确定性量化，可控制预设错误率并识别不可可靠预测个体，但非欧人群样本量较小、PRS 原始开发主要基于欧洲人群 [17]。脂质组遗传方面，AIDHS/SDS 3,000 人与 UKBB 468,515 人（EU 459,143、SA 9,372）的代谢物 GWAS 结合精细定位、共定位和 MR，发现新遗传关联及祖源特异性差异，并识别与 T2D 和心血管病共享的候选因果变异，但样本以旁遮普锡克族为主，外推性受限 [64]。Lp(a) 与 LPA 遗传风险评分方面，UKB 约 50 万成人中 LPA GRS 与 Lp(a) 水平相关，≥120 nmol/L 为升高，LPA GRS 未在测量 Lp(a) 之外提供额外预后信息，两者相对 Pooled Cohort Equation 仅带来适度区分度改善 [65]。

### 2.3 ECG 与心脏影像 AI

在窦性心律心电图上用深度学习识别房颤电信号特征，是这一方向最早被验证的任务之一。Mayo Clinic 用卷积神经网络从 1993–2017 年的 10 秒 12 导联窦律 ECG 中学习房颤特征，按 7:1:2 划分训练、内部验证与测试，并以验证集 AUC 选阈值 [23]。Geisinger 则用 280 万份 ECG 中保留的 160 万份、覆盖 43.1 万人训练深度神经网络预测新发房颤，并回顾性模拟监测部署场景，结果显示在无房颤史且发生房颤相关卒中的患者中，**近三分之二在卒中前被预测为高风险** [24]。这两项工作都把「窦律期预测」作为筛查切入点，但前者侧重房颤电信号识别，后者侧重卒中相关结局的部署模拟。

预测时间窗与外部验证强度是区分后续工作的关键。MGH 训练卷积神经网络推断 **5 年新发房颤风险**，构建 ECG-AI、CHARGE-AF 及联合 Cox 模型，并在 BWH 与 UK Biobank 外部测试，发现 AI 可提供超越临床风险因素的增益，但 UKB 随访有限、模型需重新校准为 2 年房颤风险 [66]。Framingham 心脏研究在 10,097 人、28,151 份 ECG 中优化 ECG-AF 模型，并在剩余 FHS 样本与 UK Biobank 49,280 人中与 CHARGE 评分比较，报告对 incident AF 仅中等区分度 [67]。退伍军人队列则把预测窗缩短到 **31 天内 AF**，用 2 个 VA 网络训练、另 4 个 VA 及 1 个非 VA 中心测试，纳入 907,858 份 ECG，人群平均年龄 62.4 岁、男性 93.6%、平均 CHA2DS2-VASc 1.9 [68]。三级心脏中心的 ResNet-50 研究纳入 2004–2022 年 140 万份 ECG、25 万成人，以 5 年新发 AF 为二分类结局在患者层面评估敏感性、特异性 [69]。多中心外部验证则给出更保守的数字：3 个中心 4,017 例 65 岁以上无房颤史者中，模型判为高风险的 391 例里 74 例发生房颤，**敏感性 31%**（95%CI 25–37），3,626 例非高风险者中 3,460 例保持无房颤 [12]。同一任务在不同队列、不同预测窗下的性能差异，提示单机构评估可能高估泛化能力。

死亡与复合心血管风险是另一条主线。Stanford 的 SEER 用 CNN 在 312,422 份 12 导联 ECG 上训练，在 Stanford、Cedars-Sinai 和 Columbia 测试，**5 年心血管死亡 AUC 为 0.83、0.78、0.83**，C-statistic 为 0.82、0.78、0.81，并与 PCE 联合重分类患者 [70]。另一项生存深度学习模型用两家医院 291,778 名患者的 451,950 份 ECG 开发，调优 89,302 份、内部验证 27,808 人、外部验证 33,047 人，并在 CODE15 与 SaMi-Trop 国际验证，比较生存模型与 1 年死亡率模型风险评分 [71]。巴西 230 万份 ECG、155 万患者、7 年随访的可解释深度网络则把诊断与死亡风险分层合并，并推导简化导联 [72]。这些工作共同点是外部验证时区分度普遍下降，AIRE 作者也明确将前瞻验证列为待办。

心衰风险分层出现了从多导联到单导联、从图像到可穿戴信号的迁移。YNHHS、UK Biobank 与 ELSA-Brasil 的多国研究用 AI-ECG 图像模型预测新发心衰住院，**AI-ECG 阳性者风险比 3.88–23.50**，C 统计量 0.718/0.769/0.810，并与 PCP-HF 比较 [25]。JAMA Cardiology 的单导联工作从门诊 ECG 分离 I 导联，部署噪声自适应 AI-ECG 模型识别左室收缩功能障碍，在 YNHHS、UKB、ELSA-Brasil 中评估新发心衰，并与 PCP-HF、PREVENT 评分比较 Harrell C 统计量 [73]。UK Biobank 训练、SHIP-START（4,308 人）与 SHIP-TREND（4,420 人）外部验证的 AI-HF 模型则直接用单导联（lead I）ECG，纳入 31,740 名 UKB 参与者（中位年龄 64，5.2 年随访，243 例事件），发现加入生物特征和生活方式参数可能改善区分度，但无法区分基于射血分数的心衰表型 [74]。单导联路线的方法学意义在于可对接医疗系统与可穿戴设备，代价是表型分辨率受限。

结构性心脏病与左房病变的 ECG 推断，把「电信号替代影像」的可行性推到台前。一项集成深度学习算法从 12 导联 ECG 图像检测结构性心脏病，在伊朗三级中心前瞻性连续纳入 879 例 ≥45 岁高危门诊患者（中位 62 岁），评估 LVSD、瓣膜病和严重 LV 肥厚 [75]。左房方向有两项高度重叠的工作：一项在 UKB 21,749 人心脏 MRI 上训练 ECG-AI 估计左房最小/最大容积和射血分数，在 ≥65 岁心血管健康研究外部队列评估，报告与影像**中度相关 r=0.40–0.50**，与 AF、缺血性卒中、心源性卒中强独立相关，优于传统 P 波终末电势指标 [26]；另一项在 UKB 48,300 名配对参与者上训练，两个大型人群队列外部验证，报告 LAVmin/LAVmax r=0.50、LAEF r=0.40，预测监测房颤优于现有工具和 NT-proBNP，但指出极端值存在回归均值偏差 [27]。两项研究对同一任务给出相近的中等相关性，说明 ECG 对左房结构与功能的估计仍有信息上限，但其与下游结局的独立关联支持其作为筛查信号。

缺血性卒中与冠脉疾病的 ECG 风险估计，强调机制可解释性与临床评分对照。MGH 训练卷积神经网络估计 **10 年缺血性卒中风险**，将 ECG 概率、年龄和性别整合入 Cox 模型形成 ECG2Stroke，在 MGH 测试集（4,771 人）及 BWH（68,884 人）、BIDMC（29,882 人）外部验证，训练集 101,496 人、MGH 10 年 346 例卒中，与修订版 Framingham 卒中风险谱比较区分度、校准、显著图及卒中亚型 [76]。ECG2CAD 在 MGH 的 764,670 份 ECG（137,199 人）上训练，在 MGB 队列 52.1 万+9.9 万人及 UK Biobank 50.3 万人外部验证，对 CAD 具有判别力且不劣于临床风险或年龄性别模型，但 CAD 定义依赖 ICD 编码 [31]。中国 Kadoorie Biobank 复查人群的 25,239 名成人用 Mortara VERITAS 自动判读，随访 5 年，报告正常 ECG 44.3%、房颤 1.2%、缺血 28.1%、LVH 13.6%，病理 ECG 随年龄和既往 CVD 增加，并与改良 CHA2DS2-VA 评分比较 [77]。这一组工作的共同争议在于终点定义（ICD 编码 vs 人工抽象）和随访长度对性能的影响。

多模态与基础模型正在改变这一方向的建模范式。CARDIAC-FM 通过对比学习联合建模 12 导联 ECG 与心脏 MRI，在 UK Biobank **57,609 对** ECG-CMR 样本上训练，在 CHS 和 MESA 外部验证，报告所有队列均优于单模态，ECG 联合临床评分有判别增益，并可在无 MRI 时仅用 ECG 部署 [28]。ECG 与超声心动图的多模态基础模型用 129,424 例超声心动图视频 4,391,610 段、配对 1,094,656 份 ECG（53,876 人）自监督对比训练，测试集 **LVSD 分类 AUROC 达 0.94**，优于单模态 [78]。TRIM 则把非结构化报告转为文本表征融入 EHR 轨迹，训练带 ECG 的 EHR 基础模型预测心血管病，报告整合提升整体 CVD 预测性能、模型优先关注 ECG 诊断信息、生存分析风险比一致升高，但未报告具体样本规模与外部验证 [79]。多模态路线的核心张力是：配对影像数据稀缺限制了训练规模，而单模态 ECG 部署成本更低。

自监督基础模型与开放基准是提升泛化性的另一条路径。ECG-LFM 用超千万份 12 导联 ECG（1,157 万份、197.9 万人，HEEDB+MIMIC-IV-ECG）预训练，结合对比学习与掩码语言建模，在 PTB-XL、Chapman、CODE-15、CPSC-2018、UK Biobank 外部测试，报告**平均 AUROC 0.930**，并通过 PheWAS 关联 167 个心功能因子、GWAS 发现 11 个位点 12 个 SNP、1024 个 EDF 中 8 个新 SNP，孟德尔随机化提示 4 个 EDF 与 2 种 CVD 有因果 [29]。ECG-FM 用 Transformer 混合自监督在 140 万 ECG 片段（UHN/PhysioNet/MIMIC-IV）上预训练，在 UHN-ECG 外部机构队列验证多标签解读与降低 LVEF 预测，报告表现强、标签高效且具泛化性，并公开权重、代码、教程和基准 [30]。开放权重与公开基准的差异，直接影响这些模型能否被独立复现和横向比较。

ECG 之外，非 ECG 门控胸部 CT 的机会性风险估计提供了影像 AI 的对照。NLST 研究用开源 TotalSegmentator 从 27,943 例非增强非 ECG 门控胸部 CT（17,241 名参与者）提取心脏和胸主动脉体积，用 10,356 例训练 3D DenseNet169 预测 12 年心血管死亡，在 5,165 例独立测试集评估，**深度学习 AUC 0.72 vs 基线 0.66**（基线含人口学、吸烟、BMI、合并症及 CT 放射科发现），测试集中位年龄 60.0±8.0 岁、男性 62.6%、CV 死亡 3.3% [80]。视网膜照片方向的 Reti-CVD 在 UK Biobank 44,677 人、7 年随访中，按评分低/中/高风险分层，记录卒中 277 例（0.62%）、MI 506 例（1.13%）、AF 1,053 例（2.32%）、HF 431 例（0.94%），评分升高与四类事件风险显著增加相关 [81]。这两项工作说明心血管风险信号并不限于心脏电活动或心脏影像，但事件数相对有限、外推性仍需验证。

测量层面的基础工作同样影响下游模型的可信度。UK Biobank 的参考数据集包含 1,030 名随机选取参与者、11,330 条导联级专家标注，1D 卷积网络分割波形估计 PR、QRS、QT，**MAE 分别为 7.7 ms、7.5 ms、4.9 ms**，优于 UKB CardioSoft、开源信号处理工具箱和小波 delineation，观察者 ICC 0.81–0.97，多数间期 >80% 有效，并在 46,749 人随访中与房颤及 MACE 相关，但参考集仅 1,030 人、随访中位仅 4 年 [82]。这类工作不直接产出风险评分，却决定了间期相关表型和遗传关联研究的可靠性。

### 2.4 房颤与心律失常 AI 预后模型

针对房颤患者预后预测，一项系统综述与Meta分析检索了PubMed、Embase、Scopus、Cochrane Library、Web of Science和ProQuest自建库至2024年10月21日的队列、病例对照、横断面及随机对照研究，纳入使用ML或DL模型预测房颤患者临床结局的研究，并采用TRIPOD+AI和PROBAST+AI评估报告质量与偏倚风险[id:10.1136/bmjdhai-2025-000154]。该研究将ML/DL模型与临床风险评分及传统回归模型进行对比，结果显示**AI模型总体呈现中等至良好区分度**，且在同一数据集上多优于风险评分和回归模型[id:10.1136/bmjdhai-2025-000154]。

该综述同时指出当前证据的主要局限：**多数研究缺乏外部验证、偏倚风险高、报告不完整**，且许多结局的研究数量不足[id:10.1136/bmjdhai-2025-000154]。这些方法学缺陷提示，现有AI预后模型在同数据集内的性能优势能否推广至外部人群尚不明确，是房颤AI预后研究的关键空白[id:10.1136/bmjdhai-2025-000154]。

## 3 数据与资源

（本节暂无入库证据）

## 4 中国人群队列与跨人群迁移

在跨人群迁移评估方面，一项基于 **ChinaHEART** 队列的巢式病例对照研究检测了血浆 **28 种蛋白**，筛选出与血管损伤、炎症、血管生成相关的候选蛋白，并评估其对传统风险因素模型的增量预测价值；该研究进一步在 **UK Biobank** 中评估可迁移性，但两队列在人群特征、结局定义和检测平台上的差异，以及可用蛋白标志物数量有限，均影响跨人群可比性[36]。该证据仅报告了候选蛋白与颈动脉斑块发生的关联方向及增量预测的评估框架，未给出具体的效应量或迁移性能数值[36]。

在传统危险因素的长期关联上，基于 **China Kadoorie Biobank** 的前瞻性队列分析显示，早成年期 BMI 升高与 CVD 风险呈单调剂量反应关系，且该关联基本独立于后续体重变化，出血性卒中风险亦升高；中年健康生活方式因素未表现出显著交互作用[83]。该研究为观察性设计，早成年期 BMI 多来自回忆或历史数据，残余混杂可能存在[83]。两项工作分别聚焦蛋白标志物与 BMI 暴露，前者强调跨队列迁移评估，后者强调暴露时间窗与生活方式交互，尚未形成可直接比较的结论。

## 5 临床转化与评测

其设计为非随机、12个月多中心实施研究，目前处于方案阶段，尚无疗效、体验和成本效果结果，因此其相对于传统CVD风险评估与冠脉钙化扫描决策的增量价值仍待验证[33][32]。

与上述前瞻性实施路径不同，另两项工作转向真实世界数据中的疗效推断与风险分层。DISCO数字孪生框架利用AI-ECG进行高维表型匹配，在符合PARADIGM-HF标准的HFrEF患者中比较ARNi与ACEi，并以PARADIGM-HF试验结果及传统生存分析校正为参照，其局限在于观察性数据的残余混杂[84]。Reti-CVD则用视网膜图像训练的深度学习模型识别高危者，在UK Biobank中经1:1倾向评分匹配得到**3,008对**、平均随访**9.83年**，评估他汀使用者的CVD事件风险比，但同样受限于观察性设计与倾向评分匹配无法完全消除混杂[85]。两者均以观察性数据模拟干预效应，与ESCALATE的前瞻性实施设计形成方法学差异，其结论能否外推至临床决策尚存争议。

## 6 空白与趋势

**趋势一：多组学从“关联发现”走向“风险预测增量”，但增量幅度与终点高度异质。** UKB-PPP 41,931 人中稀疏蛋白模型对 218 种疾病的中位 ΔC-index=0.07，多发性骨髓瘤 Δ=0.25、非霍奇金淋巴瘤 Δ=0.21 [10]；而 MACE 方向，SCORE2 AUC 0.740、114 蛋白单独 0.758、联合 0.771（NRI 0.140），作者自评改善有限且仅限 UKB [19]。117 蛋白 ProtRS 的 C-index 0.769 优于 SCORE2 0.667、PREVENT 0.645、FRS 0.672，加入基线模型后 ΔC=0.105 [18]；房颤方向 165 蛋白 Lasso-Cox 评分加入 CHARGE-AF、NT-proBNP 和 PRS 后 C 指数由 0.771 升至 0.816，并在 ARIC 11,012 人外部验证 [11]。**同一类组学特征在不同终点上的增量差异，说明“蛋白组能否改善预测”不能脱离具体疾病与基线模型回答。**

**趋势二：跨人群校准与迁移成为核心瓶颈，而非附属问题。** 中国糖尿病人群 C 统计量仅 0.584-0.629，重校准后 CKB-CVD 高风险组预测 48.4%、实际 25.7% [2]；QRISK3 在 UKB 中系统性高估，老年参与者高估达 20% [7]；SCORE2 在荷兰多元人群中按高危亚组调整后治疗资格人数近乎翻倍 [13]；新西兰与中国 T2D 队列中标准重校准未能改善中国队列校准 [3]。PRS 侧同样受限：CKB 中最优 PRS 每 SD 对硬 CAD 的 HR 1.26，加入传统模型后 Harrell C 男性仅增 0.003、女性增 0.001，最高 NRI 3.2% [15]；跨祖先房颤 GWAS 的 PRS 可迁移性仍有限 [16]。**跨人群校准不佳与 PRS 迁移增益微弱，是当前多组学落地最一致的障碍。**

**趋势三：ECG-AI 从“单任务判别”转向“生存曲线、图像化、单导联与基础模型”，但外部验证普遍掉点。心衰方向 AI-ECG 阳性者风险比 3.88–23.50，C 统计量 0.718/0.769/0.810 [25]；单导联路线在 UKB 31,740 人训练、SHIP-START 4,308 人与 SHIP-TREND 4,420 人外部验证，但无法区分基于射血分数的心衰表型 [74]。基础模型侧，ECG-LFM 用 1,157 万份 ECG、197.9 万人预训练，平均 AUROC 0.930，并通过 GWAS 发现 11 个位点 12 个 SNP [29]；CARDIAC-FM 在 UKB 57,609 对 ECG-CMR 上训练，CHS 和 MESA 外部验证，所有队列均优于单模态 [28]。**多中心外部验证中区分度下降、单机构评估可能高估泛化能力，是这一方向反复出现的模式。**

**趋势四：多模态与“电信号替代影像”路线已出现信息上限证据。** 左房方向两项高度重叠工作均报告 ECG-AI 与 CMR 仅中度相关：r=0.40–0.50 [26] 与 LAVmin/LAVmax r=0.50、LAEF r=0.40 [27]，但均与 AF、卒中、心衰独立相关，且预测监测房颤优于现有工具和 NT-proBNP [27]。ECG 与超声心动图多模态基础模型在 129,424 例超声视频、配对 1,094,656 份 ECG（53,876 人）上自监督对比训练，测试集 LVSD 分类 AUROC 达 0.94 [78]。**中等影像相关性提示 ECG 对结构表型的估计存在信息上限，但其与下游结局的独立关联支持其作为低成本筛查信号；配对影像数据稀缺与单模态部署成本之间的张力，将决定多模态路线的实际边界。**

**空白一：中国/东亚人群的蛋白组—PRS—ECG 联合模型与外部验证仍稀缺。** 现有蛋白组预测研究几乎全部以 UKB 为主 [50][18][51]，中国证据多停留在单队列、无外部验证的机器学习模型 [5] 或观察性蛋白关联 [22]。ChinaHEART 巢式病例对照仅检测 28 种蛋白并在 UKB 评估可迁移性，未给出具体效应量或迁移性能数值 [36]。**在 ChinaHEART、CKB 等万级以上中国队列上，把血浆蛋白组、东亚 PRS 与 ECG-AI 联合建模并做跨队列外部验证，目前没有入库证据。**

**空白二：筛查—干预闭环的硬终点证据几乎空白。** ESCALATE 将 CAD PRS≥80% 者转诊冠脉钙化扫描，但为非随机、12 个月多中心实施研究，目前处于方案阶段，尚无疗效、体验和成本效果结果 [33][32]。**PRS 或组学评分触发下游检查/治疗能否改变硬终点，缺乏实用性随机试验证据。**

**空白三：房颤 AI 预后模型的方法学缺陷尚未被系统性填补。** 系统综述与 Meta 分析（检索至 2024 年 10 月 21 日）显示 AI 模型总体呈中等至良好区分度、多优于风险评分和回归模型，但**多数研究缺乏外部验证、偏倚风险高、报告不完整**，许多结局研究数量不足 [34]。**在同数据集内性能优势能否推广至外部人群尚不明确。**

**空白四：不确定性量化与跨祖源可靠性评估刚起步。** Mondrian 交叉共形预测在 UKBB T2D 19,468 人（WB 17,574、SA 1,145、AFR 749）及 ADVANCE 试验中提升跨祖源 PRS 预测可靠性与不确定性量化，可控制预设错误率并识别不可可靠预测个体，但非欧人群样本量较小、PRS 原始开发主要基于欧洲人群 [17]。**将共形预测等方法用于蛋白组/ECG-AI 风险评分的跨人群可靠性标注，尚无入库证据。**

**空白五：终点定义与测量层面对模型性能的影响缺乏统一评估。** ECG2CAD 的 CAD 定义依赖 ICD 编码 [31]；UKB 参考数据集仅 1,030 人、随访中位仅 4 年，波形分割 MAE 为 PR 7.7 ms、QRS 7.5 ms、QT 4.9 ms [82]。**终点定义（ICD 编码 vs 人工抽象）与测量精度对下游风险模型性能的贡献，缺少系统性的量化研究。**

## 阶段判断与行动建议

| 细分方向 | 阶段 | 依据 |
|---|---|---|
| 2.1 心血管风险预测与疾病轨迹模型 | 成熟 | QRISK3、SCORE2、China-PAR 已形成被广泛外部验证的评分体系，[38]（QRISK3，2017，1547 引）与 [6]（SCORE2，2021，1501 引）代表传统评分方法已收敛并被指南采纳；[1]（China-PAR，2016，582 引）说明中国人群专用评分也已建立。新工作若只是「深度学习略优于 PCE/SCORE2」属增量，需跨人群校准或新数据模态才有新意。 |
| 2.2 心血管多组学与遗传整合 | 朝阳 | 近两年蛋白组/PRS 大规模工作密集且频出 CNS：[9]（UK Biobank 血浆蛋白组-遗传-健康关联，2023，1564 引）奠定 pQTL/蛋白组资源底座；[14]（多祖先 PRS 改善 CAD 预测，2023）与 [10]（蛋白组特征改善常见/罕见病预测，2024）显示方法仍在快速迭代、尚未收敛；[57]（AHA PRS 科学声明，2022）说明临床转化路径刚被系统化。 |
| 2.3 ECG 与心脏影像 AI | 朝阳 | 方法未收敛、近两年占比高（雷达样本中 recent_share **0.55**）：[23]（AI-ECG 识别低射血分数，2019，1352 引）与 [86]（AI-ECG 筛查收缩功能障碍，2019，1266 引）证明单模态 ECG AI 已可行；[66]（ECG 深度学习+临床因素预测房颤，2021）与 [24]（DNN 从 12 导联预测新发房颤，2021）显示正在向「ECG+临床/EHR 联合」演进，但外部验证与跨人群泛化仍不统一。 |
| 2.4 房颤与心律失常 AI 预后模型 | 证据不足 | 雷达样本中仅 1 篇：[34]（2025，ML/DL 房颤预后预测模型综述），单篇无法判断阶段；该细分方向可能被 2.3 节证据覆盖，需补充检索。 |
| 3 数据与资源 | 证据不足 | 雷达样本中 n=0，无证据可引用，不能据此判断领域空白或成熟。 |
| 4 中国人群队列与跨人群迁移 | 萌芽 | 雷达样本中仅 2 篇且方向分散：[83]（中国队列早成年 BMI 与 CVD 前瞻研究，2024，43 引）属队列流行病学而非建模；[36]（颈动脉斑块蛋白标志物巢式病例对照，2026，0 引）为预测标志物探索。缺少大规模中国队列上的多组学/ECG AI 建模与外部验证，方法尚未成型。 |
| 5 临床转化与评测 | 萌芽 | 雷达样本中 n=4、median_citations **0**，多为会议摘要与设计性工作：[32]（PRS 分层冠脉钙化评分纳入 CVD 评估，2023，20 引）与 [33]（PRS 纳入 CVD 检查，2023）显示「组学→筛查」闭环刚起步；[84]（AI-ECG 高维表型匹配，2025）提示评测方法仍在探索，尚无实用性随机试验的成熟证据。 |

**整体判断**：这个方向整体处于「**传统风险评分已成熟、多组学与 ECG AI 正在朝阳期、中国人群与临床转化仍处萌芽**」的叠加态。雷达样本中 2.2（n=36）与 2.3（n=29）合计占 **65/92**，且 2.2 的 CNS 占比 **0.14**、2.3 近两年占比 **0.55**，说明资源与注意力正快速向「蛋白组/PRS 预测」和「ECG/影像 AI 联合」集中；而 2.1 的头部证据仍是 2016–2021 的评分体系，增量空间收窄。窗口期判断：多组学预测的方法红利大约还有 **2–3 年**（等 UK Biobank 蛋白组+PRS 的预测增益被反复验证、临床声明落地后即转入成熟）；ECG AI 与组学/EHR 联合的窗口稍长，但竞争激烈。最大不确定性有三：一是**跨人群校准**——多祖先 PRS [14] 与中国队列证据 [83] 之间仍缺桥接，东亚人群蛋白组 pQTL 资源远少于欧洲；二是**临床效用**——预测增益能否转化为筛查-干预闭环，目前只有设计性/摘要级证据 [32]，无实用性随机试验；三是**数据可及性**——雷达样本中「3 数据与资源」n=0，说明公开可复用的中国多组学+ECG 配对资源稀缺，可能卡住切入。

**接下来怎么做**：

1. **用公共 UK Biobank 蛋白组+PRS 做「东亚迁移性」方法学 demo**：以 [9] 的 pQTL 资源为底座，复现 [10] 的蛋白组预测框架，但把评估重点放在「欧洲训练→东亚外部校准」的衰减曲线与重校准策略。现在做：多祖先 PRS 已被证明有效 [14]，但蛋白组层面的跨人群迁移几乎空白，方法学新意明确，且可用公共数据快速产出。

2. **把衰老/单细胞背景接进心血管多组学，做「细胞类型来源的蛋白组特征」**：用 UK Biobank pQTL + 单细胞 eQTL/表达谱，把血浆蛋白信号反卷积到细胞类型（如心肌细胞、成纤维、免疫），检验细胞来源特征是否比原始蛋白水平预测增益更高。切入点：公共 pQTL [9] + 单细胞图谱；产出：可解释的细胞类型风险特征。现在做：蛋白组预测已到「signature 层面」[10]，下一步必然是机制归因，而你的单细胞+衰老背景正是稀缺能力。

3. **ECG AI × 组学/EHR 联合建模，优先做房颤**：以 [66] 和 [24] 的 ECG-DL 房颤预测为基线，加入 PRS 与蛋白组特征，检验多模态是否在 ECG 之外有增量。现在做：ECG AI 单模态已成熟到可做基线 [23]，但「ECG+组学」联合证据稀少，2.4 节雷达样本仅 1 篇 [34]，先发优势明显。

4. **与中国队列合作方锁定一个「蛋白组+ECG 配对」子队列，做筛查-干预闭环设计**：参考 [32] 的 PRS 分层钙化评分设计，把蛋白组风险分层替换/叠加进去，产出实用性试验方案或真实世界证据。现在做：临床转化节雷达样本 median_citations **0**、多为摘要 [33]，谁先拿出完整闭环设计谁定义评测标准；且中国队列证据仅 2 篇 [83]、[36]，合作切入的边际价值高。

5. **把类器官/多组学合作项目定位为「机制验证层」而非预测层**：用类器官扰动实验验证多组学筛出的候选蛋白/pQTL 靶点，形成「队列 MR/pQTL 发现 → 类器官功能验证」的闭环。现在做：MR/pQTL 靶点发现已是多组学主流产出 [9]，但绝大多数停在关联，功能验证稀缺；你的类器官+多组学合作正好补这一环，且能反哺预测模型的特征选择，避免与纯生信团队在同质化预测任务上竞争。

## 参考文献

1. Predicting the 10-Year Risks of Atherosclerotic Cardiovascular Disease in Chinese Population: The China-PAR Project (Prediction for ASCVD Risk in China). Circulation 2016. https://doi.org/10.1161/CIRCULATIONAHA.116.022367
2. Validation and Comparison of 10-Year Cardiovascular Risk Prediction Models in Two Chinese Prospective Cohorts: The General Population and Patients With Type 2 Diabetes.. Diabetes, obesity and metabolism 2026. https://doi.org/10.1111/dom.71212
3. Simultaneous derivation, validation, and comparison of predictor hazard ratios for cardiovascular risk prediction equations in patients with diabetes from high versus non-high income countries: cohort study. British medical journal 2026. https://doi.org/10.1136/bmj-2026-100535
4. Development of machine learning-based models to predict 10-year risk of cardiovascular disease: a prospective cohort study. Stroke and vascular neurology 2023. https://doi.org/10.1136/svn-2023-002332
5. Explainable machine learning for long-term cardiovascular disease risk prediction in Chinese middle-aged and older adults: a 9-year longitudinal cohort study with web-based risk calculator. Scientific Reports 2026. https://doi.org/10.1038/s41598-026-45297-4
6. SCORE2 risk prediction algorithms: new models to estimate 10-year risk of cardiovascular disease in Europe.. European Heart Journal 2021. https://doi.org/10.1093/eurheartj/ehab309
7. Independent external validation of the QRISK3 cardiovascular disease risk prediction model using UK Biobank. Heart 2023. https://doi.org/10.1136/heartjnl-2022-321231
8. Validation of an Integrated Risk Tool, Including Polygenic Risk Score, for Atherosclerotic Cardiovascular Disease in Multiple Ethnicities and Ancestries.. American Journal of Cardiology 2021. https://doi.org/10.1016/j.amjcard.2021.02.032
9. Plasma proteomic associations with genetics and health in the UK Biobank. Nature 2023. https://doi.org/10.1038/s41586-023-06592-6
10. Proteomic signatures improve risk prediction for common and rare diseases.. Nature medicine 2024. https://doi.org/10.1038/s41591-024-03142-z
11. Proteomic Signatures for Risk Prediction of Atrial Fibrillation.. Circulation 2025. https://doi.org/10.1161/circulationaha.124.073457
12. Multicenter validation of an artificial intelligence-enabled ECG model to predict 1-year risk of atrial fibrillation or flutter.. Heart Rhythm 2026. https://doi.org/10.1016/j.hrthm.2026.03.1956
13. SCORE2 cardiovascular risk prediction models in an ethnic and socioeconomic diverse population in the Netherlands: an external validation study. EClinicalMedicine 2023. https://doi.org/10.1016/j.eclinm.2023.101862
14. A multi-ancestry polygenic risk score improves risk prediction for coronary artery disease. Nature Medicine 2023. https://doi.org/10.1038/s41591-023-02429-x
15. Minimal improvement in coronary artery disease risk prediction in Chinese population using polygenic risk scores: evidence from the China Kadoorie Biobank. Chinese Medical Journal 2023. https://doi.org/10.1097/CM9.0000000000002694
16. Cross-ancestry genome-wide analysis of atrial fibrillation unveils disease biology and enables cardioembolic risk prediction. Nature Genetics 2023. https://doi.org/10.1038/s41588-022-01284-9
17. Improving the reliability of polygenic risk score-based prediction for cardiovascular and renal complications across ancestries in type 2 diabetes using Mondrian Cross-Conformal Prediction. PLoS Computational Biology 2026. https://doi.org/10.1371/journal.pcbi.1014670
18. Integrating clinical, proteomics, and polygenic scores to improve cardiovascular risk prediction: a prospective cohort study.. Journal of Advanced Research 2026. https://doi.org/10.1016/j.jare.2026.06.034
19. Large-scale plasma proteomics in the UK Biobank modestly improves prediction of major cardiovascular events in a population without previous cardiovascular disease. medRxiv 2024. https://doi.org/10.1101/2024.03.13.24304196
20. Proteomics and lipidomics in atherosclerotic cardiovascular disease risk prediction. European Heart Journal 2023. https://doi.org/10.1093/eurheartj/ehad161
21. Cross-population proteome-wide mendelian randomization study identifies likely causal proteins for cardiovascular diseases. Zeitschrift für Induktive Abstammungs- und Vererbungslehre 2026. https://doi.org/10.1007/s00438-026-02458-4
22. Measured and genetically predicted protein levels and cardiovascular diseases in UK Biobank and China Kadoorie Biobank.. Nature cardiovascular research 2024. https://doi.org/10.1038/s44161-024-00545-6
23. An artificial intelligence-enabled ECG algorithm for the identification of patients with atrial fibrillation during sinus rhythm: a retrospective analysis of outcome prediction.. The Lancet 2019. https://doi.org/10.1016/S0140-6736(19)31721-0
24. Deep Neural Networks Can Predict New-Onset Atrial Fibrillation From the 12-Lead ECG and Help Identify Those at Risk of Atrial Fibrillation–Related Stroke. Circulation 2021. https://doi.org/10.1161/CIRCULATIONAHA.120.047829
25. Heart failure risk stratification using artificial intelligence applied to electrocardiogram images: a multinational study.. European heart journal 2025. https://doi.org/10.1093/eurheartj/ehae914
26. Abstract 4354222: Deep Learning Prediction of Left Atrial Structure and Function from 12-lead Electrocardiograms. Circulation 2025. https://doi.org/10.1161/circ.152.suppl_3.4354222
27. Deep learning prediction of left atrial structure and function from 12-lead electrocardiograms. Nature Communications 2026. https://doi.org/10.1038/s41467-026-76155-6
28. CARDIAC-FM: A Multimodal Foundation Model for Cardiovascular Risk Prediction Using ECG and Cardiac MRI. medRxiv 2026. https://doi.org/10.64898/2026.03.16.26348526
29. A self-supervised electrocardiogram foundation model for empowering cardiovascular disease prediction and genetic factor discovery. Nature Communications 2026. https://doi.org/10.1038/s41467-026-72436-2
30. ECG-FM: an open electrocardiogram foundation model.. JAMIA open 2025. https://doi.org/10.1093/jamiaopen/ooaf122
31. Electrocardiogram-Based Artificial Intelligence to Identify Coronary Artery Disease.. JACC. Advances 2025. https://doi.org/10.1016/j.jacadv.2025.102041
32. Incorporating a Polygenic Risk Score-Triaged Coronary Calcium Score into Cardiovascular Disease Examinations to Identify SubClinicAL coronAry arTEry Disease (ESCALATE): Protocol for a Prospective, Non-Randomised Implementation Trial.. American Heart Journal 2023. https://doi.org/10.1016/j.ahj.2023.06.009
33. Incorporating a polygenic risk score into cardiovascular disease examinations to identify subclinical coronary artery disease: rationale and design of the ESCALATE trial. European Heart Journal 2023. https://doi.org/10.1093/eurheartj/ehad655.1337
34. Machine learning and deep learning predictive models for prognosis in patients with atrial fibrillation: a systematic review and meta-analysis. BMJ digital health & AI 2025. https://doi.org/10.1136/bmjdhai-2025-000154
35. Predicting cardiovascular outcomes in Chinese patients with type 2 diabetes by combining risk factor trajectories and machine learning algorithm: a cohort study. Cardiovascular Diabetology 2025. https://doi.org/10.1186/s12933-025-02611-0
36. Protein biomarkers for predicting incident carotid plaque: a nested case-control study in the ChinaHEART cohort with transportability assessment in the UK Biobank.. BMJ open 2026. https://doi.org/10.1136/bmjopen-2025-110220
37. Cardiovascular disease risk prediction using automated machine learning: A prospective study of 423,604 UK Biobank participants. PLoS ONE 2019. https://doi.org/10.1371/journal.pone.0213653
38. Development and validation of QRISK3 risk prediction algorithms to estimate future risk of cardiovascular disease: prospective cohort study. British medical journal 2017. https://doi.org/10.1136/bmj.j2099
39. Polygenic risk scores in cardiovascular risk prediction: A cohort study and modelling analyses. PLoS Medicine 2021. https://doi.org/10.1371/journal.pmed.1003498
40. Integration of lipidomic and polygenic risk scores within contemporary clinical cardiovascular risk assessment pathways: a multi-cohort development and validation study. EClinicalMedicine 2026. https://doi.org/10.1016/j.eclinm.2026.104159
41. Incremental predictive value of CMR phenotyping for major adverse cardiovascular events: an interpretable machine learning study from UK Biobank. Frontiers in Medicine 2026. https://doi.org/10.3389/fmed.2026.1852547
42. Simple Risk Model Predicts Incidence of Atrial Fibrillation in a Racially and Geographically Diverse Population: the CHARGE‐AF Consortium. Journal of the American Heart Association : Cardiovascular and Cerebrovascular Disease 2013. https://doi.org/10.1161/JAHA.112.000102
43. Development and Validation of a Prediction Model for Atrial Fibrillation Using Electronic Health Records.. JACC Clinical Electrophysiology 2019. https://doi.org/10.1016/j.jacep.2019.07.016
44. Cardiovascular Event Prediction by Machine Learning: The Multi-Ethnic Study of Atherosclerosis. Circulation Research 2017. https://doi.org/10.1161/CIRCRESAHA.117.311312
45. Abstract 14071: Plasma Protein Concentrations and Risk of Incident Cardiovascular Diseases in the UK Biobank. Circulation 2023. https://doi.org/10.1161/circ.148.suppl_1.14071
46. High Throughput Plasma Proteomics and Risk of Heart Failure and Frailty in Late Life.. JAMA cardiology 2024. https://doi.org/10.1001/jamacardio.2024.1178
47. Shared proteomic landscape between arteriosclerosis and cardiovascular endpoints: a Mendelian randomization and observational study integrating AlphaFold3 for structural prediction. medRxiv 2025. https://doi.org/10.1093/cvr/cvag095
48. Neutrophil counts and cardiovascular disease.. European heart journal 2023. https://doi.org/10.1093/eurheartj/ehad649
49. Interpretable machine learning leverages proteomics to improve cardiovascular disease risk prediction and biomarker identification. Communications Medicine 2024. https://doi.org/10.1038/s43856-025-00872-0
50. A Proteomics-Based Approach for Prediction of Different Cardiovascular Diseases and Dementia. Circulation 2024. https://doi.org/10.1161/CIRCULATIONAHA.124.070454
51. Machine Learning‐Driven Prediction of Coronary Artery Disease Risk Based on UK Biobank Plasma Proteomics. Journal of the American Heart Association : Cardiovascular and Cerebrovascular Disease 2026. https://doi.org/10.1161/JAHA.125.047248
52. A plasma proteomic signature for atherosclerotic cardiovascular disease risk prediction in the UK Biobank cohort. medRxiv 2024. https://doi.org/10.1101/2024.09.13.24313652
53. Prediction of Atrial and Ventricular Arrhythmias using Multiple Cardiovascular Risk Factor Polygenic Risk Scores.. Heart Rhythm 2024. https://doi.org/10.1016/j.hrthm.2024.12.017
54. Proteomic signatures as biomarkers of atherosclerosis burden.. Cardiovascular Research 2026. https://doi.org/10.1093/cvr/cvag140
55. Performance of Cardiovascular Polygenic Risk Scores in Carotid Stenosis Identification. medRxiv 2026. https://doi.org/10.64898/2026.06.22.26356289
56. A polygenic risk score improves risk stratification of coronary artery disease: a large-scale prospective Chinese cohort study. European Heart Journal 2022. https://doi.org/10.1093/eurheartj/ehac093
57. Polygenic Risk Scores for Cardiovascular Disease: A Scientific Statement From the American Heart Association. Circulation 2022. https://doi.org/10.1161/CIR.0000000000001077
58. Interactions between Enhanced Polygenic Risk Scores and Lifestyle for Cardiovascular Disease, Diabetes Mellitus and Lipid Levels. Circulation Genomic and Precision Medicine 2021. https://doi.org/10.1161/CIRCGEN.120.003128
59. Improving 10-year cardiovascular risk prediction in patients with type 2 diabetes with metabolomics. Cardiovascular Diabetology 2024. https://doi.org/10.1186/s12933-025-02581-3
60. The polyunsaturated-to-monounsaturated fatty acid ratio and cardiovascular risk prediction: a prospective cohort study of 183,237 adults. Lipids in Health and Disease 2025. https://doi.org/10.1186/s12944-025-02745-w
61. Improved sex-specific cardiovascular risk prediction with multi-omics data in people with type 2 diabetes. Cardiovascular Diabetology 2025. https://doi.org/10.1186/s12933-025-03036-5
62. Plasma proteomics enhances heart failure risk prediction among individuals with type 2 diabetes: a prospective cohort study.. American Journal of Clinical Nutrition 2026. https://doi.org/10.1016/j.ajcnut.2026.101216
63. Chronic kidney disease onset, progression, and cardiovascular outcomes: proteomics informs biology and risk stratification. Cardiovascular Diabetology 2026. https://doi.org/10.1186/s12933-025-03049-0
64. Identification of lipid quantitative trait loci linked with cardiometabolic disease in Asian Indians and Europeans: A genome-wide association study and Mendelian randomization. PLoS Medicine 2026. https://doi.org/10.1371/journal.pmed.1005039
65. Clinical Utility of Lipoprotein(a) and LPA Genetic Risk Score in Risk Prediction of Incident Atherosclerotic Cardiovascular Disease. JAMA cardiology 2020. https://doi.org/10.1001/jamacardio.2020.5398
66. Electrocardiogram-based Deep Learning and Clinical Risk Factors to Predict Atrial Fibrillation. Circulation 2021. https://doi.org/10.1161/CIRCULATIONAHA.121.057480
67. Prediction of Atrial Fibrillation from the Electrocardiogram in the Community Using Deep Learning: A Multinational Study. Circulation: Arrhythmia and Electrophysiology 2025. https://doi.org/10.1161/CIRCEP.125.013734
68. Deep Learning of Electrocardiograms in Sinus Rhythm From US Veterans to Predict Atrial Fibrillation.. JAMA cardiology 2023. https://doi.org/10.1001/jamacardio.2023.3701
69. Incident atrial fibrillation prediction using ECG-based deep learning at a specialized tertiary cardiac care center. European Heart Journal 2024. https://doi.org/10.1093/eurheartj/ehae666.3479
70. A deep learning-based electrocardiogram risk score for long term cardiovascular death and disease. npj Digit. Medicine 2023. https://doi.org/10.1038/s41746-023-00916-6
71. Mortality risk prediction of the electrocardiogram as an informative indicator of cardiovascular diseases. Digital Health 2023. https://doi.org/10.1177/20552076231187247
72. Decoding 2.3 million ECGs: interpretable deep learning for advancing cardiovascular diagnosis and mortality risk stratification.. European heart journal. Digital health 2024. https://doi.org/10.1093/ehjdh/ztae014
73. Artificial Intelligence-Enabled Prediction of Heart Failure Risk From Single-Lead Electrocardiograms.. JAMA cardiology 2025. https://doi.org/10.1001/jamacardio.2025.0492
74. Deep learning analysis of single-lead electrocardiograms enables pragmatic heart failure risk assessment in the general population. European Heart Journal - Digital Health 2026. https://doi.org/10.1093/ehjdh/ztag099
75. Prospective validation of an ensemble deep learning algorithm for detecting structural heart disease using real-world 12-lead electrocardiogram images. European Heart Journal 2025. https://doi.org/10.1093/eurheartj/ehaf784.4483
76. ECG Signatures and Long-Term Ischemic Stroke Risk: A Deep Learning Analysis of 200,000 Patients.. Journal of the American College of Cardiology 2026. https://doi.org/10.1016/j.jacc.2026.03.084
77. Population prevalence of ECG abnormalities and risk of incident CVD outcomes: 5-year follow-up of 25,000 Chinese adults. European Heart Journal 2023. https://doi.org/10.1093/eurheartj/ehad655.2380
78. Multimodal foundation model for evaluating cardiovascular disease from electrocardiography and echocardiography. European Heart Journal 2025. https://doi.org/10.1093/eurheartj/ehaf784.4471
79. Multimodal Electronic Health Record Foundation Models with Electrocardiogram for Cardiovascular Disease Prediction. medRxiv 2025. https://doi.org/10.1101/2025.11.10.25339886
80. Abstract 4141180: Opportunistic assessment of cardiovascular risk using deep learning of the heart and aorta on non-contrast chest computed tomography. Circulation 2024. https://doi.org/10.1161/circ.150.suppl_1.4141180
81. A deep-learning-based retinal cardiovascular disease biomarker and risk of stroke, myocardial infarction, atrial fibrillation, and heart failure in the UK Biobank. European Heart Journal 2023. https://doi.org/10.1093/eurheartj/ehad655.2920
82. A curated reference dataset and deep learning model for multi-lead electrocardiographic interval measurements in UK Biobank. medRxiv 2026. https://doi.org/10.64898/2026.06.26.26356665
83. Early adulthood BMI and cardiovascular disease: a prospective cohort study from the China Kadoorie Biobank. Lancet Public Health 2024. https://doi.org/10.1016/s2468-2667(24)00043-4
84. High-dimensional phenotypic matching with artificial intelligence-enhanced ECG to replicate heart failure trial outcomes in real-world data. European Heart Journal 2025. https://doi.org/10.1093/eurheartj/ehaf784.4614
85. Abstract 4140651: Effect of Statin Therapy on Cardiovascular Events in High-Risk Group Identified by a Coronary Artery Calcium-Trained Deep Learning Model Using Retinal Imaging: A Propensity Score-Matched Study from the UK Biobank. Circulation 2024. https://doi.org/10.1161/circ.150.suppl_1.4140651
86. Screening for cardiac contractile dysfunction using an artificial intelligence–enabled electrocardiogram. Nature Medicine 2019. https://doi.org/10.1038/s41591-018-0240-2
87. Artificial intelligence-enabled electrocardiogram for mortality and cardiovascular risk estimation: a model development and validation study.. The Lancet. Digital health 2024. https://doi.org/10.1016/s2589-7500(24)00172-9
88. Integrating Imaging-Derived Clinical Endotypes with Plasma Proteomics and External Polygenic Risk Scores Enhances Coronary Microvascular Disease Risk Prediction. medRxiv 2025. https://doi.org/10.1142/9789819824755_0045
89. Metabolomics data improve 10-year cardiovascular risk prediction with the SCORE2 algorithm for the general population without cardiovascular disease or diabetes. medRxiv 2024. https://doi.org/10.1101/2024.04.29.24306593
90. Transformer-based models for predicting cardiovascular risk in Chinese adults: development and validation.. European Heart Journal 2026. https://doi.org/10.1093/eurheartj/ehag517
91. Abstract 18742: Matrilysin (MMP7) as a Robust Predictor of Hypertension Incidence and Complications: Findings From a Proteomic Analysis in the Atherosclerosis Risk in Communities (ARIC) Study. Circulation 2023. https://doi.org/10.1161/circ.148.suppl_1.18742
92. Deep learning interpretation of echocardiographic images predicts incident heart failure and subtypes. Journal of Cardiac Failure 2026. https://doi.org/10.1016/j.cardfail.2026.07.003
