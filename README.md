# radar — 个人科研情报系统

跨 4 个领域（衰老多模态 / 数据库与模型 / ML 底层算法 / Agent 进展）自动抓取信息，
按 `config/profile.md` 里的研究画像用 LLM 打分，生成中文 digest。

- **每日**（GitHub Actions，北京时间 09:00）：arXiv + EuropePMC(PubMed/bioRxiv) +
  Semantic Scholar 引用追踪 + HuggingFace + GitHub + RSS → `digests/YYYY-MM-DD.md`
- **每周**（北京时间周日 21:00）：汇总一周 digest → 跨域趋势 + 项目启发 +
  registry 增补建议 → `weekly/YYYY-Www.md`
- `registry/` 是长期知识库（数据库/模型/人物索引），**人工维护**，weekly 只提建议。

## 本地运行

```bash
pip install -r requirements.txt

# 无 LLM（纯关键词打分），先试试
python -m radar.run daily --days 2 --no-llm

# 带 LLM 打分（火山方舟 Ark，OpenAI 兼容）
export ARK_API_KEY=sk-xxx
export ARK_MODEL=doubao-seed-1-6-250615   # 可选，默认就是它
python -m radar.run daily --days 1
python -m radar.run weekly
```

无 `ARK_API_KEY` 时自动降级为关键词打分，不会崩。

## GitHub Actions 设置（一次性）

```bash
gh secret set ARK_API_KEY          # 粘贴 key
gh variable set ARK_MODEL -b doubao-seed-1-6-250615   # 可选，换模型才需要
```

两个 workflow 也可在 Actions 页面手动触发（workflow_dispatch）。
digests 和去重状态（`data/seen.json`）由 bot 自动 commit 回 main。

## 定制（90% 的维护动作都在这两个文件）

| 文件 | 作用 |
|---|---|
| `config/sources.yaml` | 加/减信息源：关键词、arxiv query、RSS feed、GitHub/HF 搜索词、种子论文、追踪作者 |
| `config/profile.md` | 研究画像。方向变了改这里，打分质量立刻跟着变 |

追踪某作者的新论文：先查 author id
`https://api.semanticscholar.org/graph/v1/author/search?query=Steve+Horvath&fields=name,affiliations`，
然后填进 `sources.yaml` 的 `tracked_authors`。

## 结构

```
radar/            Python 包
  collectors/     每个源一个 collector，统一返回 List[Item]，单源失败不影响整体
  pipeline/       dedup（SQLite 式 JSON 状态）→ score（关键词粗筛 top40 → LLM 精排）→ digest
  run.py          CLI 入口
config/           sources.yaml + profile.md
digests/  weekly/ data/        产物与去重状态（自动 commit）
registry/         长期知识库（人工维护）
.github/workflows/ 每日 + 每周定时任务
```

## 已知边界

- Semantic Scholar 无 key 时限速（~1 req/s 共享），seed papers 别超过 ~20 篇
- GitHub 搜索未认证限 10 req/min；workflow 里已注入 GITHUB_TOKEN 提速
- arXiv 请求间隔 3s，daily 全量约 2-4 分钟，正常
- RSS 源个别会失效，日志里会有 `[rss] ... returned no entries`，换掉即可
