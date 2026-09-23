# 方向背景库（Background）设计 v3 —— 已实现的区块与测试

> 目标：任一新方向 = 写一份 `topic.yaml` → `bootstrap` 8 轮搭底出报告 → 之后 `renew` 吃日报增量，整篇重编。
> 每个区块一个模块、一个契约、一组测试。代码在 `radar/background/`，测试在 `tests/background/`。
> 状态：2026-09-23，40 个单元/集成测试通过，3 个联网契约测试（`RADAR_LIVE=1`）。

## 0. 调研结论（保留，见 git 历史 v2）

没有开源项目开箱即做"持续增长的证据库 → 重跑得到更新后的整篇综述"（唯一为此设计的 DAS 未放码）。
部件都现成：PaperQA2 做持久全文索引（可选插件）、radar 已有 collectors 做发现、`paper-lookup` skill、
WebWeaver 的"动态大纲 + 按节只喂该节证据"写法、多角色 AND 规则筛选（已验证：自动分类 ~80%，F1 0.91-0.95）。
所以放在 radar 仓库内，胶水层几百行，不另起 repo。

## 1. 一条区块链，两种入口

```
             bootstrap（每轮）: gap ──► discover ─┐
                                                  ├─► dedup ► screen ► fetch ► extract ► store ► outline ► compile ► metrics/log
             renew（每周）:            Inbox ────┘
```

`runner.Pipeline.run_round(candidates)` 是唯一的回合函数；bootstrap 和 renew 只在"候选从哪来"上不同。

| 区块 | 模块 | 契约（输入 → 输出） | 依赖 LLM | 测试 |
|---|---|---|---|---|
| 方向定义 | `spec.py` | `topic.yaml` → `TopicSpec`（含路径约定、画像文本、校验） | 否 | `test_spec.py`：默认角色/预算、路径、非法配置报错、模板只写一次 |
| 数据契约 | `models.py` | `Candidate / Vote / Decision / Evidence / DiscoveryPlan / RoundLog`；id 归一化 doi/arxiv/pmid；标题指纹 | 否 | `test_models.py`：id 归一化 6 种写法、`Item`→`Candidate`、JSON 往返 |
| LLM 协议 | `llmio.py` | `LLM.chat(prompt, task)`；prompt 以 `[[TASK:x]]` 开头；`RadarLLM` 走 `radar/llm.py` | — | FakeLLM 按 task 路由（conftest） |
| 缺口分析 | `gap.py` | 大纲 + 指标 + 上轮日志 → `DiscoveryPlan`；LLM 失败退化为规则 | 可选 | `test_discover_gap.py`：冷启动计划、LLM 计划、失败退化 |
| 发现 | `discover.py` | `Source.fetch(spec, plan) → [Candidate]`；内置 EuropePMC 关键词 / 整刊回溯 / arXiv / S2 滚雪球 / Inbox；单源失败隔离；按引用截预算 | 否 | 每个源用假 HTTP 测；失败隔离；Inbox 过滤 domain/分数/日期；`test_live.py` 打真 API |
| 去重 | `dedup.py` | 批内合并（同 id 或同标题，合并 found_by）+ 对照证据库/落选表 | 否 | `test_store_dedup.py` |
| 评审团 | `screen.py` | 角色独立投票 → 分歧项互看理由可修订一次 → `all` 规则 → `Decision`（accepted / borderline） | 是 | `test_screen.py`：规则真值表、一致免讨论、分歧触发讨论并可翻转、缺票记 no、边缘记录 |
| 全文 | `fetch.py` | Europe PMC OA XML / arXiv PDF → 文本，缓存；失败返回空 | 否 | `test_extract_fetch.py`：缓存命中一次网络、失败不落盘、无来源不请求 |
| 抽取 | `extract.py` | 8 字段（method/data/scenario/benchmark/results/availability/limitations/summary），有全文用全文 | 是 | 字段对齐、全文标记、失败留空 |
| 证据库 | `store.py` | 每篇一个 JSON；`rejected.jsonl`；`is_seen`；`CorpusIndex` 插件（默认 Null，可换 PaperQA2） | 否 | 增删查、拒绝记录、统计 |
| 大纲 | `outline.py` | markdown ↔ 节树；LLM 只输出操作（attach/add_section/rename/detach），程序执行；漏挂进「未归类」 | 可选 | `test_outline.py`：编号、往返、操作幂等、未归类兜底、无 LLM 路径 |
| 编译 | `compile.py` | 每节只喂该节证据 → 节文本（逐句 `[id]`）→ TL;DR → 装配 → 未知引用剔除 → 编号 + 参考文献 | 是 | `test_compile_metrics.py`：幻觉引用被删、编号、节隔离、空节占位、头部统计 |
| 指标 | `metrics.py` | 覆盖度 = 种子 0.3 + 饱和 0.3 + 高引 0.4；历史；平台期停止 | 否 | 数值、历史追加、停止判据 |
| 阶段判断 | `stage.py` | 程序算每个子题的近两年占比 / 年份跨度 / 引用中位数 / CNS 占比 / 逐轮新增衰减 → LLM 打 萌芽/朝阳/成熟/夕阳 并给"算法提供方怎么切入" | 是 | `test_stage_joint_resources.py`：统计正确、综合节不计、报告含该节 |
| 联合分析 | `joint.py` | 各方向报告的 TL;DR + 阶段判断 + 头部文献 → 全景表 / 交叉点 / 联合项目 / 不要做的事 → `background/_joint/report.md` | 是 | 摘要块提取、报告头、跳过无报告方向 |
| 资源登记 | `resources.py` | 全部证据的 data/availability 字段 → 命名资源（数据集/模型/基准/数据库/工具）→ 按名合并、方向数与证据数投票 → 链接可达性核验 → 分类型表 | 是 | 挖掘过滤非法类型、合并并集、核验 ok/dead/n/a、渲染 |
| 日报/周报挂靠 | `context.py` | 日报 ≥6 分条目对照方向大纲 → "落在哪个子题 · 相对已有证据的增量"；周报末尾汇总各方向「本次变更」 | 是 | `test_context.py` |
| 编排 | `runner.py` | `bootstrap(rounds)` / `renew(inbox)`；日志、指标、末轮编译、平台期提前收尾 | — | `test_runner.py`：2 轮 + renew 端到端、平台期仍编译、无 LLM 只采集、注入全文抓取 |

## 2. 目录与文件（每方向）

```
background/<slug>/
  topic.yaml        人改。新方向只需要这一份
  evidence/*.json   证据库（唯一真源）
  rejected.jsonl    落选 + borderline
  outline.md        动态大纲（可人工微调，下轮尊重）
  report.md         编译产物，永远整体重生成
  log.md            每轮一条
  metrics.json      覆盖度时间序列
  cache/            全文缓存（gitignore）
```

## 3. 命令

```bash
python -m radar.run background init --topic <slug> --name <中文名>   # 生成 topic.yaml 模板
python -m radar.run background bootstrap --topic <slug> [--rounds N] [--no-llm] [--no-fulltext]
python -m radar.run background renew --topic <slug>                    # 吃 data/extractions.jsonl 近 7 天
python -m radar.run background compile --topic <slug>                  # 只重编报告
python -m pytest                                                        # 40 个离线测试
RADAR_LIVE=1 python -m pytest tests/background/test_live.py             # 真 API 契约
```

## 3b. 站点与工作流（2026-09-23 整理后）

- 站点 tab：方向背景（默认，`_joint` 联合分析置顶）/ 周报 / 日报 / 资源库（只展示核验过的登记表，日报新发现折叠在下）。
- 专题报告 tab 与 `deepdive` 命令已下架；原「虚拟细胞」专题改为单细胞方向下的窄主题 `background/virtual-cell/`（months 9）。
- weekly 工作流顺序：renew 全部方向 → resources → joint → weekly 综合（末尾附各方向本周变更）→ 站点。
- 日报每条带「定位」行：方向 › 子题 · 增量。

## 4. 与 radar 的接口

- 入：`data/extractions.jsonl`（日报 ≥7 分 + domain 匹配）→ `Inbox` 源。
- 出：`background/<slug>/report.md` → 站点「专题报告」tab 加入口（待接）；`resources.md` 基础设施通道改吃 `evidence/*.json` 的 data 字段（待接）。
- weekly workflow 末尾加 `background renew`（待接，等第一个方向 bootstrap 验证通过）。

## 5. 现在到哪一步（2026-09-23 实跑）

第一个方向「人群健康与多组学 AI」用 DeepSeek 跑满 bootstrap，第 7 轮触发覆盖度平台期自动收尾：

| 轮 | 新候选 | 入库 | 累计证据 | 覆盖度 |
|---|---|---|---|---|
| 1 | 60 | 32 | 32 | 0.637 |
| 2 | 60 | 24 | 56 | 0.663 |
| 3 | 49 | 17 | 73 | 0.677 |
| 4 | 22 | 8 | 81 | 0.707 |
| 5 | 17 | 4 | 85 | 0.727 |
| 6 | 9 | 3 | 88 | 0.727 |
| 7 | 14 | 2 | 90 | 0.713（平台期停） |

- 90 篇证据、141 篇落选（13 篇边缘）；Nature 正刊 12、Nature Genetics 11、Nature Communications 13；2025-2026 占 43 篇；54 篇有 OA 全文。
- 报告约 5.4 万字：背景与定义、空白与趋势为综合节，方法学自动长出「组学衰老时钟与纵向多组学动态」子节。
- 新候选逐轮递减（60 → 9）说明检索面已饱和；高引覆盖率改为累计 top-50 后不再随轮次候选波动。
- 实跑修掉的问题：纯引用排序被通用方法挤占 → 相关性优先；Europe PMC 限流返回空 → 重试；全文 URL 错 → 修正并按 DOI 反查 pmcid；综合节被误挂论文 → 按节名判定并自动摘下；LLM 重复写标题 → 剥离。
- 边缘案例合理：TransformEHR / Hi-BEHRT 生物专家 yes、媒体专家 no（非生物库级），记录待复审。

### 六个方向现状（2026-09-23 收尾）

| 方向 | 轮 | 证据 | 全文 | 覆盖度 | 报告 | 备注 |
|---|---|---|---|---|---|---|
| population-omics-ai | 7 | 90 | 54 | 0.71 | 5.3 万字 | 平台期停 |
| aging-multimodal | 4 | 71 | 39 | 0.62 | 4.0 万字 | 平台期停；每轮新候选 20 篇左右，检索面已尽 |
| single-cell-foundation | 5 | 86 | 51 | 0.65 | 4.6 万字 | 平台期停 |
| virtual-cell（窄主题） | 2 | 36 | 16 | 0.56 | 2.6 万字 | 第 2 轮 60 候选只收 4，检索词需调 |
| world-models-ssl | 3 | 65 | 26 | 0.34 | 3.9 万字 | S2 限速拖累种子 |
| research-agents-rlvr | 3 | 91 | 35 | 0.61 | 5.6 万字 | — |

六份报告都含「阶段判断与行动建议」；`_joint` 联合分析、`_resources` 资源登记（348 项，主表 96）已生成。

多方向实跑后新增的机制：Semantic Scholar 关键词源（ML 方向 EuropePMC 无覆盖、arXiv 本机 406）；S2 429 指数退避 + 可选 `S2_API_KEY`；
同一篇论文的 DOI / arXiv / PMID 互认（`alt_ids`），种子命中与去重都按此；S2 不通时经 DataCite / Crossref 取标题链接种子；
媒体专家口径：CNS 及子刊综述属背景必读，通用方法套小众领域不算影响力。

已知限制：S2 无 key 时限速严重，ML/agent 方向的种子与滚雪球受影响，配 `S2_API_KEY` 后会明显改善。

下一步：其余四个方向放开到 8 轮；站点入口；weekly 接 renew；PaperQA2 插件可选。
