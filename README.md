# radar — 个人科研情报系统

跨 4 个领域（衰老多模态 / 数据库与模型 / ML 底层算法 / Agent 进展）自动抓取信息，
按 `config/profile.md` 里的研究画像用 LLM（DeepSeek，OpenAI 兼容）打分，生成中文 digest。

## 三层节奏（信息按半衰期分层）

| 层 | 内容 | 频率 | 产物 |
|---|---|---|---|
| 新闻流 | 新论文 / 模型 / repo / 新闻 | **每日**（北京 09:00） | `digests/YYYY-MM-DD.md` |
| 慢速源 | 格局型源（GitHub 全景 / HF / blog） | **每周日** 随每日任务顺带收 | 同上当周日的 digest |
| 月度源 | 更慢的格局源 | **每月 1 号** 顺带收 | 同上 |
| 每周综合 | 跨域趋势 + 项目启发 + registry 建议 | **每周日 21:00** | `weekly/YYYY-Www.md` |
| 背景知识刷新 | registry 月度审查：新增/修订建议 | **每月 1 号 09:30** | `registry_updates/YYYY-MM.md` |

每个源的节奏在 `config/sources.yaml` 里用 `cadence: daily|weekly|monthly` 标注
（文件头部注释有完整说明）。`registry/` 是长期知识库，**人工维护**，weekly 和
landscape 只提建议、不自动改。

## 本地运行

```bash
pip install -r requirements.txt   # 注意用 /usr/bin/python3 对应的 pip

# 无 LLM（纯关键词打分），先试试
/usr/bin/python3 -m radar.run daily --no-llm

# 带 LLM：自动 source /data3/yy/key.env（含 DEEPSEEK_API_KEY 即可），不用手动 export
/usr/bin/python3 -m radar.run daily
/usr/bin/python3 -m radar.run weekly
/usr/bin/python3 -m radar.run landscape
```

无 key 时自动降级为关键词打分，不会崩。换模型/服务商改环境变量
`LLM_BASE_URL` / `LLM_MODEL`（默认 `https://api.deepseek.com` + `deepseek-chat`）。

## GitHub Actions 设置（一次性）

```bash
# key 从本机 key.env 推进 Secrets，全程不显示（在任意目录跑）
grep '^DEEPSEEK_API_KEY=' /data3/yy/key.env | cut -d= -f2- | gh secret set DEEPSEEK_API_KEY -R YOU-k/radar
```

三个 workflow（daily / weekly / monthly）都可在 Actions 页面手动触发。
digests、去重状态（`data/seen.json`）、weekly、registry_updates 由 bot 自动 commit 回 main。

## 定制（90% 的维护动作都在这两个文件）

| 文件 | 作用 |
|---|---|
| `config/sources.yaml` | 加/减信息源：关键词、arxiv query、RSS feed、GitHub/HF 搜索词、种子论文、追踪作者、每个源的 cadence |
| `config/profile.md` | 研究画像。方向变了改这里，打分质量立刻跟着变 |

追踪某作者的新论文：先查 author id
`https://api.semanticscholar.org/graph/v1/author/search?query=Steve+Horvath&fields=name,affiliations`，
然后填进 `sources.yaml` 的 `tracked_authors`。

## 结构

```
radar/            Python 包
  collectors/     每个源一个 collector，统一 collect(cfg, freqs) -> List[Item]，单源失败不影响整体
  pipeline/       dedup（JSON 状态）→ score（关键词粗筛 top40 → LLM 精排）→ digest
  run.py          CLI：daily / weekly / landscape
config/           sources.yaml + profile.md
digests/  weekly/  registry_updates/  data/   产物与状态（自动 commit）
registry/         长期知识库（人工维护）
.github/workflows/ daily + weekly + monthly 定时任务
```

## 已知边界

- Semantic Scholar 无 key 时限速（~1 req/s 共享），seed papers 别超过 ~20 篇
- GitHub 搜索未认证限 10 req/min；workflow 里已注入 GITHUB_TOKEN 提速
- arXiv 请求间隔 3s，daily 全量约 2-4 分钟，正常
- RSS 源个别会失效或挂起（已加 30s 超时），日志里会有 `[rss] ... returned no entries`，换掉即可
- 本机（中国大陆网络）访问 arXiv / HuggingFace / 部分美国 blog 不通，属环境问题；
  GitHub Actions 美国机器全部正常
