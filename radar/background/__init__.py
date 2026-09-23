"""方向背景库：topic 为单位的可复用区块流水线。

bootstrap（N 轮搭底）和 renew（增量更新）走同一条区块链：
  gap → discover → dedup → screen → fetch → extract → store → outline → compile → metrics
每个区块只依赖 models 里的数据契约和 llmio 里的 LLM 协议，可单独测试、单独替换。
"""
