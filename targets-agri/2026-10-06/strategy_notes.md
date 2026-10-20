## 策略变更 Notes

- Agriculture v4.3 自 2026-10-02 纳入主账户，AUM $2,000；目前无 active target，资金留现金，但仍计入 combined AUM $22,000。
- crush_vol/crush_vol2/adm_bg2 使用 SPY + MOO；adm_bg/adm_tsn/bg_tsn 使用 SPY-only。先逐 sleeve 计算 hedge，再账户净额合并。
- 维持独立虚拟账本；仅执行 combined orders，不执行此目录独立订单。
