# P3-6 维护说明：自适应策略引擎

## 范围

P3-6 在 P3-5 的 AI 建议流水和结果评分之后，增加一层本地自适应策略审查：

```text
MT5 运行快照 / 影子盘账本 / AI 建议流水
→ 路线评分
→ 动态入场闸门
→ 动态止损止盈建议
→ 中文 Telegram 摘要
```

它只做数据判断和人工复核建议，不接管 EA，不修改实盘配置。

## 验收命令

Backend：

```powershell
python -m py_compile tools\run_adaptive_policy.py tools\adaptive_policy\schema.py tools\adaptive_policy\data_loader.py tools\adaptive_policy\route_score.py tools\adaptive_policy\entry_gate.py tools\adaptive_policy\dynamic_sltp.py tools\adaptive_policy\policy_engine.py tools\adaptive_policy\telegram_text.py
python -m unittest discover tests -v
node --test tests\node\test_adaptive_policy_guard.mjs
python tools\run_adaptive_policy.py --runtime-dir .\runtime build --symbols USDJPYc
python tools\run_adaptive_policy.py --runtime-dir .\runtime telegram-text --symbol USDJPYc
```

Docs：

```powershell
python scripts\check_docs_quality_gate.py --root .
python scripts\check_docs_links.py --root .
python scripts\check_api_contract_matches_backend.py --contract docs\contracts\api-contract.json --backend ..\QuantGodBackend
python -m unittest discover tests -v
```

## 禁止范围

不要加入：

- MT5 下单；
- 平仓、撤单、改单；
- 修改实盘 preset；
- broker 执行适配器；
- Telegram 命令接收；
- webhook 接收；
- 邮件投递；
- 钱包或 外部市场下单；
- 多用户、计费或积分系统。

## 运行原则

先由数据决定路线是否有资格继续观察。DeepSeek 和本地 AI 只能解释结果，不能覆盖弱样本、连续亏损或影子表现不足的治理结论。
