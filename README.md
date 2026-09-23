# radar — 个人科研情报系统

跨 5 个领域（衰老多模态 / 数据库与模型 / 人群健康与多组学 AI / ML 底层算法 / Agent 进展）自动抓取信息，
按 `config/profile.md` 里的研究画像用 LLM 打分，高分论文自动深读全文，
生成中文 digest，并发布成一个手机友好的可浏览站点。

- **每日**（GitHub Actions，北京时间 08:23）：arXiv + EuropePMC(PubMed/bioRxiv) +
  Semantic Scholar 引用追踪 + HuggingFace + GitHub + RSS → `digests/YYYY-MM-DD.md`
  → 深读当日 ≥7.5 分 top 3 篇全文（折叠在条目下）
- **每周**（北京时间周日 20:41）：汇总一周 digest → 跨域趋势 + 项目启发 +
  registry 增补建议 → `weekly/YYYY-Www.md`
- **每月**（1 号 09:17）：对照近 30 天 digest 审查 `registry/` 长期知识库，提增补/修订建议

定时任务刻意避开整点/半点——GitHub Actions 高峰期排队，整点 cron 可能延迟数小时。
- **站点**：`docs/index.html` 由 `radar run site` 生成，GitHub Pages 零成本发布，
  暗色、按天折叠、可关键词过滤，手机上比翻仓库舒服
- `registry/` 是长期知识库（数据库/模型/人物索引），**人工维护**，weekly 只提建议。

## 本地运行

```bash
pip install -r requirements.txt

# 无 LLM（纯关键词打分），先试试
python -m radar.run daily --days 2 --no-llm

# 带 LLM 打分 + 深读（DeepSeek，OpenAI 兼容）
export LLM_API_KEY=sk-xxx
export LLM_BASE_URL=https://api.deepseek.com   # 默认就是它
python -m radar.run daily --days 1
python -m radar.run weekly
python -m radar.run landscape                  # 月度 registry 审查
python -m radar.run site                       # 重新生成 docs/index.html
```

无 `LLM_API_KEY` 时自动降级为关键词打分、跳过深读，不会崩。

**网络注意**：arXiv 在国内直连会被重置。本机跑要代理：
`HTTPS_PROXY=http://127.0.0.1:7890 python -m radar.run ...`。
GitHub Actions 跑在境外，不需要。

## LLM 配置

全部是 OpenAI 兼容端点，一个 key 即可（默认 DeepSeek）：

| env | 用途 | 默认 |
|---|---|---|
| `LLM_API_KEY` / `DEEPSEEK_API_KEY` | key（二选一） | 无 |
| `LLM_BASE_URL` | 端点 | `https://api.deepseek.com` |
| `SCORE_MODEL` | 每日打分（走量，用便宜档） | `deepseek-chat` |
| `DEEP_MODEL` | 高分论文全文深读 | `deepseek-chat` |
| `SYNTH_MODEL` | weekly / landscape 综合 | `deepseek-chat` |
| `DEEPREAD_MIN` | 深读分数门槛（0-10） | `7.5` |
| `DEEPREAD_MAX` | 每天最多深读篇数（控成本） | `3` |
| `DIGEST_MIN_SCORE` | digest 只保留 ≥ 此分的条目（低分直接过滤） | `6` |

GitHub Actions 设置（一次性）：

```bash
gh secret set DEEPSEEK_API_KEY          # 粘贴 key
gh variable set SCORE_MODEL -b deepseek-chat   # 可选，默认值就是 deepseek-chat
```

三个 workflow 也可在 Actions 页面手动触发（workflow_dispatch）。
digests、去重状态（`data/seen.json`）和站点（`docs/`）由 bot 自动 commit 回 main。

## 定制（90% 的维护动作都在这两个文件）

| 文件 | 作用 |
|---|---|
| `config/sources.yaml` | 加/减信息源：关键词、arxiv query、RSS feed、GitHub/HF 搜索词、种子论文、追踪作者 |
| `config/profile.md` | 研究画像。方向变了改这里，打分质量立刻跟着变 |

追踪某作者的新论文：在 Semantic Scholar 找到其一篇代表论文，
从 `https://api.semanticscholar.org/graph/v1/paper/DOI:<doi>?fields=authors.authorId`
反查 author id（author/search 返回的多是碎片档案），填进 `sources.yaml` 的 `tracked_authors`。

## 结构

```
radar/            Python 包
  collectors/     每个源一个 collector，统一返回 List[Item]，单源失败不影响整体
  pipeline/       dedup（去重）→ score（关键词粗筛 top40 → LLM 精排）
                  → deepread（高分全文深读）→ digest → site（渲染站点）
  llm.py          全项目唯一 LLM 出口（OpenAI 兼容）
  run.py          CLI 入口（daily / weekly / landscape / site）
config/           sources.yaml + profile.md
digests/  weekly/ data/ docs/   产物与去重状态（自动 commit）
registry/         长期知识库（人工维护）
.github/workflows/ 每日 + 每周 + 每月定时任务
```

### 复用契约（agent-discovery-log 等共用基建）

`collectors/` 和 `pipeline/dedup.py` 是通用件，其他项目直接搬：

- `mod.collect(cfg, freqs) -> List[Item]`：`cfg` 是 `sources.yaml` 加载的 dict
  （`domains` + `arxiv`/`rss`/`github_queries`/`hf_queries`/`seed_papers`/`tracked_authors`），
  `freqs` 是 `{"daily": 1, "weekly": 7, ...}` 节奏表；collector 内部自己管失败隔离
- `filter_new(items, state_path=...) -> List[Item]`：状态文件路径可注入，
  复用方传自己的 seen.json
- `Item`：统一条目 schema（id/source/domain/title/url/authors/abstract/published/extra）

## 已知边界

- Semantic Scholar 无 key 时限速（~1 req/s 共享），seed papers 别超过 ~20 篇
- GitHub 搜索未认证限 10 req/min；workflow 里已注入 GITHUB_TOKEN 提速
- arXiv 请求间隔 3s，daily 全量约 4-6 分钟，正常
- RSS 源个别会失效，日志里会有 `[rss] ... returned no entries`，换掉即可
- EuropePMC 每日采集按 `CREATION_DATE`（记录入库日）取窗，不能用 `FIRST_PDATE`（发表日）：
  CNS 正刊进 PubMed 索引滞后 3-20 天，按发表日取 1 天窗口几乎抓不到 Nature/Science/Cell 新文
  （实测 1 条 vs 17 条）。deepdive 回溯调研仍按发表日取存量
- 整刊订阅条目最多 40 条/天直通 LLM，超额按全领域关键词分截断（Nature 周三、Science 周四发刊日会超）
