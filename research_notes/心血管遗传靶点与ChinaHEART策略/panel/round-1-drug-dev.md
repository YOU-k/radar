# Round 1 评审：心血管药物研发负责人视角

评审对象：`reports/心血管遗传靶点与ChinaHEART策略.md`（截至 2026-09-27）
评审人设：大型药企心血管管线负责人（靶点验证、CVOT 设计、监管路径）

## 一句话总评

作为学术综述，这份报告的分层框架清楚、诚实，对 ChinaHEART 数据现实的判断也准确。但从投资决策的角度看，核心论断"分子把手决定能否成药"有一处硬伤：Lp(a) 和 IL-6 恰恰都有血浆把手，照样失败了。报告还系统性地漏掉了 2025–2026 年心血管研发的主线，即在已验证靶点上换给药方式（口服 PCSK9、siRNA、一次性碱基编辑、醛固酮合酶抑制剂）以及 incretin 的 CV 获益。它的研究问题清单偏"学术发现"，偏离了"药企和监管能拿来用"。建议补正事实，并把研究问题重排到富集、可迁移性和 benefit-risk 校准上。

---

## 具体发现

**1.「分子把手」框架需要从"有没有把手"改成"把手有没有经过事件校准"（《一张记分牌》末段、《Lp(a) 与 IL-6》一节）。**
报告称"靶点能不能成药，看因果链里有没有一个可在血浆中测量、并且有剂量反应的中间分子"。但 Lp(a) 浓度本身就是一个可测、有剂量反应的血浆分子，pelacarsen 也确实把它降下来了；IL-6 和 hsCRP 在 ZEUS 中同样"按预期下降"（原文自述）。两者的把手都在，试验照样阴性。所以把手是必要条件，远不充分。药企真正依赖的是**经过事件校准的替代终点**：一个"每降低一个单位对应多少事件下降"的对数线性关系，而且这个关系要经过多个机制的 RCT 反复验证，监管机构才会接受。LDL-C/apoB 和血压属于这一类，HbA1c 只能算半个；Lp(a)、hsCRP 和 LVOT 压差以外的 HCM 读数都还不是。这一区分直接决定了监管路径。obicetrapib 在欧盟（2026-09-21）和 enlicitide 在美国（2026-07-16 获批，CORALreef Outcomes 入组超过 14,500 例、尚未读出）都凭 LDL-C 获批上市，不必等 CVOT；Lp(a) 药物则必须先拿出硬终点。建议把框架改写为三层："有无可测分子 → 分子与事件之间有无跨机制校准的剂量关系 → 监管是否接受它作替代终点"。ODYSSEY-HCM 可以作为反例补进来：梗阻性 HCM 有 LVOT 压差这个把手，所以 mavacamten 和 aficamten 能成功；非梗阻性 HCM 没有，峰值 VO2 又太"软"，于是失败。这比报告在表格里写的"瓶颈在递送"更贴切。表格中心肌病一行把 ODYSSEY 的失败归到"分子→干预（递送）"，与后文的叙述自相矛盾。

**2.「遗传效应大小不能预测药物效应大小」说过头了，这恰恰是 HORIZON 本可预见的地方（《一张记分牌》末段、《Lp(a) 与 IL-6》【推断】段）。**
HMGCR 的例子只说明"变异效应 ≠ 药物效应"。按每单位生物标志物折算后，遗传学对效应量有相当强的预测力：Ference 等的析因 MR 用"每 mmol/L LDL 或每 mmol/L apoB"成功预言了 PCSK9 抑制剂、依折麦布和 CETP 抑制剂（REVEAL）的获益幅度。报告自己引用的 CETP 证据就属于这种用法。药企评估 Lp(a) 时用的正是这套逻辑：降多少**绝对量**（mg/dL 或 nmol/L）才相当于 LDL 降 1 mmol/L。Burgess 2018 给出约 100 mg/dL，之后的估计多在 50–65 mg/dL 之间。HORIZON 入组门槛是 ≥70 mg/dL，pelacarsen 每月 80 mg 的相对降幅约 70–80%，推算出的绝对降幅很可能只落在这个阈值附近甚至更低【推断，待完整数据】。因此 HORIZON 的结果更像"每单位校准框架下的边际剂量不足"，而不是"MR 预测不了幅度"。结论应当改成：**MR 能预测每单位的效应；试验设计（入组门槛、绝对降幅、疗程）决定暴露了多少单位。** 这一改动同时指明了 ChinaHEART 能做什么（见修订问题 3）。另外需要更正：HORIZON 的 ≥90 mg/dL 人群按设计是**共同主要分析人群**（设计文献写明检验效能为全人群 HR 0.80、该亚人群 HR 0.75），不是事后亚组。原文"≥90 mg/dL 亚组的数据尚未公布"的写法会误导读者。还应补一句：OCEAN(a)-Outcomes（olpasiran）和 ACCLAIM 用的是 siRNA，降幅约 95% 以上，每 3–6 个月给药一次，入组门槛更高，所以 HORIZON 不能直接外推为 Lp(a) 这一类药物的失败。

**3. ZEUS 的机制解释有误（《Lp(a) 与 IL-6》【推断】段）。**
原文认为"IL6R Asp358Ala 这一工具变量作用于膜受体的经典信号通路，ZEUS 阻断的是配体"，言下之意是两者的作用面不同。实际上，Asp358Ala 通过增加受体脱落来削弱膜结合的经典信号，而阻断配体会**同时**抑制经典信号和转导信号，覆盖面只多不少。这个差异解释不了阴性结果，反而会让读者低估 ZEUS 的信息量。药企内部更可能讨论的解释有四个：(a) CKD 人群的非动脉粥样硬化死亡和竞争风险很高，稀释了 MACE；(b) hsCRP 是靶点结合的标志物，不是经过校准的替代终点，入组门槛 hsCRP ≥2 富集到的是"炎症高"的人，未必是"IL-6 驱动事件"的人；(c) 严重感染增加抵消了部分获益；(d) CANTOS（canakinumab，MACE −15%）和 LoDoCo2（秋水仙碱，已获 FDA 批准）是阳性的，CLEAR-SYNERGY 是中性的，所以炎症假说没有被"证伪"，而是出现了"上游 IL-1β、NLRP3 与下游 IL-6 效果不同"的分化。研究笔记里有秋水仙碱的内容（ascvd_stroke_targets.md 第 76–77 行），CANTOS 和秋水仙碱却都没有进入报告正文，这是明显的遗漏。

**4. VESALIUS-CV 并不是"推进到一级预防"（开篇结论段、《LDL 轴是唯一的完整闭环》一节）。**
VESALIUS-CV 入组的是**既往没有心梗或卒中**、但已有动脉粥样硬化证据（冠脉、外周或脑血管病变、血运重建史）或高危糖尿病的患者。它在药企和监管的语境里被称作"首次事件预防"，不是传统意义上的一级预防（无动脉粥样硬化病证据的风险因素人群）。原文"第一个在一级和二级预防中都证明能减少事件"这一说法会被监管和医学事务团队直接挑出来。建议改为"把 PCSK9 单抗的获益扩展到无既往心梗或卒中的高危动脉粥样硬化人群"。这对 ChinaHEART 反而更有用：高危层里正是这类人群多、治疗率低（见修订问题 1）。

**5. 漏掉了 2025–2026 年心血管研发的主线：在已验证靶点上换给药方式，以及 incretin（《ASCVD 与卒中》全节、记分牌表格）。**
这一遗漏直接削弱了"缺的是可干预的因果层"这一论断的政策含义。从投资组合的角度，过去两年最大的资金流向不是新靶点，而是：
- **LDL 轴的新给药方式**：enlicitide 口服 PCSK9 于 2026-07-16 获 FDA 批准，LDL-C 降幅 56–59%，CORALreef Outcomes 入组超过 14,500 例，尚未读出（[Merck](https://www.merck.com/news/mercks-lipfendra-enlicitide-is-the-first-and-only-once-daily-oral-pcsk9-inhibitor-approved-by-the-u-s-fda-to-reduce-ldl-c-in-adults-with-hypercholesterolemia/)；[TCTMD](https://www.tctmd.com/news/fda-approves-enlicitide-oral-pcsk9-inhibitor-ldl-lowering)）。inclisiran 的 ORION-4 共 16,124 例，结果预计 2027 年初公布；VICTORION-2 PREVENT 预计 2027 年读出（[AHJ 2026 设计文](https://www.sciencedirect.com/science/article/pii/S0002870326002085)）。VERVE-102 做 PCSK9 碱基编辑（Lilly）：单次给药使 PCSK9 最多降 88%、LDL-C 最多降 62%，效果持续到 18 个月，已发表于 NEJM 2026，II 期计划 2026 年底开始入组（[Lilly](https://investor.lilly.com/news-releases/news-release-details/single-dose-lillys-pcsk9-base-editor-verve-102-reduced-pcsk9-88)）。另有 bempedoic acid（CLEAR Outcomes）。
- **incretin**：SELECT（非糖尿病肥胖人群，MACE 约 −20%）、SOUL（口服司美格鲁肽）、SURPASS-CVOT（替尔泊肽对度拉糖肽），以及 STEP-HFpEF 和 SUMMIT。这是 PCSK9 之后最大的 CV 获益事件，靶点**不**来自 CAD 遗传学（BMI 的 MR 对它有支持）。报告只在 HFpEF 部分提了一句 STEP-HFpEF，SUMMIT 在笔记里有，报告里却没有。
- **降压新机制**（中国归因第一位的危险因素）：baxdrostat 于 2026-05-18 获 FDA 批准，是首个醛固酮合酶抑制剂（[AstraZeneca](https://www.astrazeneca.com/media-centre/press-releases/2026/Baxdrostat-MNR-2026.html)）；lorundrostat 在研；zilebesiran（每半年一次 siRNA）已启动约 11,000 例的 ZENITH CVOT（[Roche](https://www.roche.com/media/releases/med-cor-2025-08-30)）。
- **TRL 轴**：olezarsen 和 plozasiran 已在胰腺炎和甘油三酯上获益，CAPITAN CVOT 在研（笔记里有，报告正文缺失）。

这些管线说明，行业已经把"人群→干预"层的依从性和可及性问题当成**药物设计问题**来做：每半年一针、一次性编辑、口服替代注射。报告把"人群→干预"只归为实施科学和政策问题，漏掉了这条与中国高度相关的产业路径。高血压控制率只有 7.2%、高危人群他汀使用率不到 3%，这类场景正是长效或一次性疗法的卫生经济学论证所需要的背景。建议在记分牌表格之后新增一张"已验证靶点的新给药方式与待读出 CVOT"时间表（ORION-4 2027 年初、CORALreef Outcomes、OCEAN(a) 约 2026 年 12 月、PREVAIL 2027 年第一季度、HERMES/ARTEMIS 2027 年上半年、LIBREXIA-AF、ZENITH、CAPITAN）。

**6. FXI 的解读方向对，但漏了关键变量和最新读出（《卒中》一节）。**
原文把 FXI 的问题归为"剂量、对照药和卒中亚型"，这个判断成立，但还需要三点补充。(a) **抑制深度**：asundexian 50 mg 的谷浓度抑制不足，是 OCEANIC-AF 劣于阿哌沙班的主要解释。milvexian 在 LIBREXIA-AF 中用了按模型选定的更高剂量（2026 年 CPT 有剂量选择论文），这是药企真正盯着的变量。(b) **对照药**：在安慰剂对照的加药设计中（OCEANIC-STROKE）赢，在与 DOAC 头对头的设计中（OCEANIC-AF）输。这是试验设计的问题，不是亚型生物学的问题。(c) **更新**：LIBREXIA-ACS 的最终结果已在 ESC 2026 公布，milvexian 组 5.4%，安慰剂组 5.1%（[ESC](https://www.escardio.org/news/press/press-releases/milvexian-did-not-reduce-cardiovascular-events-in-the-librexia-acs-trial/)）；LIBREXIA-AF 尚未读出，预计完成日期为 2027-05。abelacimab（LILAC-TIMI 76，面向不适合抗凝的房颤患者，安慰剂对照）也被漏掉了，而这恰好是"低出血"价值主张最干净的检验。**对中国最关键、报告却没有点出的联系是：FXI 的核心卖点是低出血，而中国卒中中 ICH 占比高、抗栓治疗严重不足。** ChinaHEART 能为"OCEANIC-STROKE 型"人群估计基线 ICH 与缺血性卒中的比例，这正是 FXI 在中国做 benefit-risk 定位和 NMPA 桥接所需要的数据。

**7. 研究问题清单偏学术发现，对药企和监管的可用性排序需要重做（《给 ChinaHEART 算法团队的研究问题》全节）。**
- **A2（TTE）**高估了可用性。ChinaHEART 没有处方或配药记录，只有高危层问卷式的用药信息；非致死事件只在高危层有记录；血脂是 POC 检测。按 NMPA《真实世界证据支持药物研发的指导原则》，这样的数据达不到回答疗效问题的 RWE 标准，最多用于流行病学背景和外部对照中的"自然史"部分。建议降级，并把 TTE 改成"用已知 RCT 结果作基准，检验数据能否复现"的**数据适用性验证**，不作为主结论。
- **A1** 的方向最对，但报告没有提 **I64（未分型卒中）**。中国死因登记里未分型卒中的比例可能很高【需向数据方核实】，一旦把它归到 I61 或 I63，LDL 与 ICH 权衡的结论就可能翻转，必须把它作为主要的敏感性分析。
- **B1**（事先登记 MR）学术上优雅，但对药企增量有限，因为各大药企都有内部的 MR 与 PheWAS 流程。它对药企真正有价值的只是**东亚人群的 ICH 安全性信号**（CETP、Lp(a)、FXI、PCSK9 在遗传学上对 ICH 的方向）。建议缩窄到这一点。
- **B4（CHIP）**在以死亡为主要结局、随访中位 3.6 年的条件下检验效能很弱，药企短期内也不会在中国做按 CHIP 分层的 CVOT，应降到 P2。
- 清单缺了药企最常向学术队列要的三样东西：**入组富集和可行性地图**（按具体试验的入排标准估计合格人数和事件率）、**全球 CVOT 效应向中国人群的可迁移性**（ICH E17 多区域试验的一致性评估，以及医保谈判时的 NNT 和预算影响），以及**生物标志物分布**（Lp(a) 的中国分布直接决定入组筛选的成功率）。

**8. 数据治理约束对药企合作的影响被低估了（《ChinaHEART 的数据现实》末段）。**
报告提到了《人类遗传资源管理条例》，但没有推到它的后果：外资或合资药企原则上拿不到个体数据，合作只能以"中方主导分析、输出汇总结果"的形式进行，基因分型数据的跨境与联合使用还要走单独审批。所以研究问题设计时就应当让**产出是可以出境的汇总量**：分层事件率、合格人群比例、校准曲线、NNT 表。这进一步说明富集和可迁移性这类问题最适合与药企合作，个体水平的遗传发现并不适合。

---

## P0 / P1 / P2 分级建议

**P0（必须修改，否则药企或监管读者会质疑整份报告的可信度）**
1. 重写"分子把手"框架，改成"可测分子 → 跨机制事件校准 → 监管接受的替代终点"三层，并把 Lp(a)/hsCRP（有把手但未校准）和 ODYSSEY-HCM（缺少把手）写成正反例；修正心肌病一行"瓶颈在递送"与 ODYSSEY 叙述之间的矛盾。（发现 1）
2. 把"遗传效应大小不能预测药物效应大小"改为"MR 能预测每单位效应，试验设计决定暴露了多少单位"；更正 HORIZON 的 ≥90 mg/dL 为共同主要人群；补充绝对降幅的推算和 siRNA 与 ASO 的差别。（发现 2）
3. 删除或改写 ZEUS 的"膜受体对配体"解释，改为竞争风险、hsCRP 未经校准、感染这几点，并把 CANTOS 和秋水仙碱补进正文。（发现 3）
4. 把 VESALIUS-CV 的"一级预防"改为"无既往心梗或卒中的高危动脉粥样硬化人群"。（发现 4）
5. 按修订清单（见下）重排研究问题：以富集、可迁移性、benefit-risk 校准和生物标志物分布为主，TTE 和 CHIP 降级。（发现 7）

**P1（应当补充）**
6. 新增"已验证靶点的新给药方式与 incretin"一节，外加 2026–2027 年待读出 CVOT 的时间表（enlicitide、inclisiran ORION-4/V2P、VERVE-102、SELECT/SOUL/SURPASS-CVOT、baxdrostat/lorundrostat/zilebesiran ZENITH、olezarsen/plozasiran CAPITAN、OCEAN(a)、PREVAIL、LIBREXIA-AF）。（发现 5）
7. FXI 部分补充抑制深度、对照药设计、LIBREXIA-ACS 的 ESC 2026 最终数据、LIBREXIA-AF 预计 2027 年读出、abelacimab LILAC，以及"FXI 低出血 × 中国 ICH 高占比"这条联系。（发现 6）
8. A1 加上 I64 未分型卒中的敏感性分析和编码质量评估。（发现 7）

**P2（可选改进）**
9. 写明人类遗传资源条例对药企合作形式的约束，以及"产出应为可出境的汇总量"这一设计原则。（发现 8）
10. 中国司美格鲁肽化合物专利约于 2026 年到期，国产仿制药陆续上市【需核实】，这可能构成一个 GLP-1 可及性骤增的自然实验，可以挂在 A3 的县级自然实验框架下。
11. Minikel 的 2.6 倍是"从 I 期到获批"的相对成功率。建议补一句：对心血管而言，这一优势主要体现在降低 II→III 期的失败率，而 CVOT 的成本结构（上万例、4–5 年）意味着"遗传支持但暴露量不足"的失败代价远高于其他领域，HORIZON 就是例子。

---

## 修订后的研究问题清单（前 5）

**1. 中国 CVOT 入组可行性与富集地图（仅用现有数据）。**
按正在进行或计划中的关键试验的入排标准，在 ChinaHEART 高危层中操作化定义合格人群：VESALIUS 型（无既往心梗或卒中的动脉粥样硬化和高危糖尿病）、ZENITH 型（未控制高血压加高 CV 风险）、OCEANIC-STROKE 型、CAPITAN 型（混合型血脂异常加残余风险，受 POC 血脂所限）。估计各类合格人群的规模和县级分布，以及在竞争风险下的 CV 死亡率与全因死亡率，同时给出这些人群中 ICH 与缺血性卒中的比例。
*理由*：这是药企最直接可用的产出。它决定中国能否纳入多区域 CVOT（ICH E17）、样本量怎么算、中心选在哪里；产出是汇总量，可以合规共享；也不依赖基因组或住院数据关联。

**2. 卒中亚型的 benefit-risk 校准：降脂强度、血压与抗栓对 ICH 和缺血性卒中的非对称效应（A1 修订版）。**
以亚型死亡为结局做竞争风险模型，把 I64 未分型卒中的分配作为主要敏感性分析，用校准亚样本校正 POC 血脂，并与 CKB 的 LDL→ICH MR 以及东亚人群中 CETP、PCSK9、Lp(a)、FXI 的遗传 ICH 方向做三角验证。输出"强化降脂或加用抗栓后净获益为正"的人群边界（按血压控制情况、年龄和地区划分）。
*理由*：这是中国与西方最大的结构差异，直接影响 PCSK9、CETP 和 FXI 在中国的说明书人群、NMPA 审评中的安全性关注点以及指南目标值。FXI"低出血"的定位在中国能值多少，全取决于这一问题的答案。

**3. 在存储样本中测 Lp(a)（nmol/L，采用对 apo(a) 同型不敏感的检测方法）和 apoB：嵌套病例队列，外加"每单位"风险校准。**
描述中国人群的 Lp(a) 分布，以及达到各试验入组门槛（≥70/≥90 mg/dL，≥175/≥200 nmol/L）的比例。估计 Lp(a) 每单位绝对量与冠心病、缺血性卒中和 ICH 死亡的风险梯度，并与东亚 LPA 的 MR 结果比对。据此推算各 Lp(a) 药物在中国人群中按绝对降幅能期望多少获益。
*理由*：HORIZON 之后，整个行业都在重算"需要降多少绝对量、该在谁身上用"。中国人群的 Lp(a) 分布决定筛选成功率和桥接策略，检测成本也很低。需要先确认冻存样本中 Lp(a) 的稳定性。

**4. 全球 CVOT 效应向中国人群的可迁移性，以及可挽回负担的估计。**
用可迁移性和标准化方法，把 SELECT、VESALIUS、FOURIER、ORION-4（读出后）、STEP/ESPRIT 强化降压、SSaSS、SECURE 多效片的相对效应，按 ChinaHEART 高危层的协变量分布、基线事件率和亚型构成重新加权。估计 NNT 和可预防的死亡数，并按给药方式（每日口服、每半年一次 siRNA、一次性编辑）分别设定依从性情景，模拟对应的人群获益。
*理由*：药企的医保谈判、卫生经济学评价和中国上市策略都需要这组数字，监管也会用它评估中国亚组一致性是否在合理范围。这个问题把报告"瓶颈在人群→干预"的判断变成了可以定价、可以用来决策的产出。

**5. 未控制和顽固高血压的表型地图：服务于新型降压药（ASI、siRNA）的入组富集。**
在 ChinaHEART 中识别用药后仍未控制的人群、服用 3 种以上药物的人群、肥胖或 CKD 合并高血压的人群，把盐摄入（问卷或自然实验中的替代指标）等可能与醛固酮驱动相关的表型分层，估计它们的规模、县级分布和 CV 死亡风险，并与县级盐替代品推广和基层用药可及性等自然实验衔接。
*理由*：高收缩压是中国归因的第一位危险因素。baxdrostat 已经获批，lorundrostat 在研，zilebesiran 的 ZENITH 已经启动。这些药物在中国的临床开发和定位，需要知道"已经在用药、但仍未控制"的人有多少、分布在哪里、风险多高。这是 ChinaHEART 相对 CKB 和 UKB 的独特优势，因为它有 440 万人的血压数据，而且覆盖县级。

*备选（第 6 位）*：B1 缩窄版，即事先登记东亚人群中 CETP、Lp(a)、FXI、PCSK9 在遗传学上对 ICH 的方向，作为问题 2 的外部三角验证，不单独立项。CHIP、Olink 靶点发现和湿实验（原 B4、B5、C 组）从药企视角看都属于长周期、低转化率的方向，建议放到基础设施（住院关联、基因分型审批）落实之后再做。

---

*本轮新核实的来源*：[Merck enlicitide 获批](https://www.merck.com/news/mercks-lipfendra-enlicitide-is-the-first-and-only-once-daily-oral-pcsk9-inhibitor-approved-by-the-u-s-fda-to-reduce-ldl-c-in-adults-with-hypercholesterolemia/)；[TCTMD enlicitide](https://www.tctmd.com/news/fda-approves-enlicitide-oral-pcsk9-inhibitor-ldl-lowering)；[ORION-4 设计与时间表（AHJ 2026）](https://www.sciencedirect.com/science/article/pii/S0002870326002085)；[Lilly VERVE-102](https://investor.lilly.com/news-releases/news-release-details/single-dose-lillys-pcsk9-base-editor-verve-102-reduced-pcsk9-88)；[NEJM VERVE-102](https://www.nejm.org/doi/full/10.1056/NEJMoa2601283)；[Novartis Lp(a)HORIZON](https://www.novartis.com/news/media-releases/novartis-announces-lpahorizon-phase-iii-topline-results-pelacarsen-patients-elevated-lpa-and-established-cardiovascular-disease-cvd)；[HORIZON 设计（AHJ 2025）](https://www.sciencedirect.com/science/article/pii/S0002870325001012)；[AstraZeneca baxdrostat](https://www.astrazeneca.com/media-centre/press-releases/2026/Baxdrostat-MNR-2026.html)；[Roche/Alnylam ZENITH](https://www.roche.com/media/releases/med-cor-2025-08-30)；[ESC 2026 LIBREXIA-ACS](https://www.escardio.org/news/press/press-releases/milvexian-did-not-reduce-cardiovascular-events-in-the-librexia-acs-trial/)；[milvexian 剂量选择（JTH 2026）](https://www.jthjournal.org/article/S1538-7836(26)00138-8/fulltext)。SELECT、SOUL、SURPASS-CVOT、CANTOS 和 CLEAR Outcomes 的具体数字属于评审人的背景知识，本轮没有重新检索，写入报告前应核实原文。
