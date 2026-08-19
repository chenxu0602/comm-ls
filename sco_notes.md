 目前最值得进一步验证的 feature family 是：

  1. gc_hg_relative_log_price_index 的 rolling z-score
  2. gc_hg_relative_log_momentum_21d
  3. M0_atr_14 / M0_ret_std_20
  4. carry_360_perc
  5. SCCO 上的 hg_gc_matched_ratio_ma_gap

  其中 volatility state 是跨 BHP、RIO、Vale、FCX、SCCO 最一致的共同模式；GC/HG relative price z-score 则是目前最有 peer confirmation 的相对金属 regime feature。


feature_z__gc_hg_relative_log_price_index 目前的 peer 结果：

  SCCO: +0.223 → +0.300
  RIO : +0.186 → +0.158
  FCX : +0.128 → +0.041
  BHP : +0.175 → -0.153

 1. GC/HG relative price index z-score
  2. GC M0_atr_14，但主要限于 SCCO/FCX
  3. GC M0_ret_std_20
  4. GC lis_carry_0p30y，暂时只作为研究候选

  总体上，SCO volatility 的跨 peer 证据明显强于 GC volatility。GC 更适合做“铜矿股专用风险状态”，不适合作为整个矿业篮子的统一 signal。
