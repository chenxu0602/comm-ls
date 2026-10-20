Research only; legacy continuous explicit frozen-position PnL, not actual IB.
At close T use same-date 5-observation WTI chained log-return sum and crack_03 change.
Outcomes use T+1..T+h only. Incomplete and cross-split horizons excluded.
Commodity settlement is assumed available for the next US execution session; release/arrival-time audit still required before deployment.
Zeros define four fixed states; no threshold fitting or parameter search.
Sleeve active at decision; future PnL follows original entries/exits, not constant holdings.
Spaced windows do not overlap within each reported cell; this does not imply independence.
All-active and conditional samples are different subsets, not randomized controls.
2024+ is a post-hoc stability split, NOT clean OOS. Small samples are not deployable evidence.
Costs are those allocated to the original portfolio, NOT costs of a hypothetical risk gate.
A gate would require a separate explicit simulation with new turnover and re-entry costs.
No beta re-estimation, production writes, or hedge changes.
