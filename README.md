# finance_backtest_system

Using backtesting to check if a strategy of stock buying is good or bad

# Plan: 

- 1. 定期定額報酬計算
    - [ ] 將玉山證券的各個定期定額方法與流程用 backtesting.py 實作出來 (要能夠得到相同結果)
    - [ ] 套用到DVC版控平台中
- 2. 進階基於指標的買賣策略開發 (e.g., Based on MACD, KDJ, ...) 
    - [ ] 用AI生成各種策略模板
    - [ ] 將回測結果納入DBV版控中
    - [ ] 各種加密貨幣相關指標要能夠被納入
    
# Implementation 

- 1. 建立DVC Pipeline 
    - [ ] 將 strategy 然後把backtesting report 放進 DVC metrics 