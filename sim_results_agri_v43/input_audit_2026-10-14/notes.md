# Agriculture input audit: 2026-10-14

Calendar crush now merges historical and live contract settles under contract_source_policy.csv. Contract schedules, signal rules, allocations and hedging are unchanged. Required signal fields and lookbacks must be finite; an older zero signal cannot bypass missing inputs.

Sources: {'soybean_crush': PosixPath('data/processed/soybean_complex_signals_2.parquet'), 'stock_cache': PosixPath('data/cache/feature_return_observation_v1/ZS-soybean-common_2.parquet')}

No broker targets or orders were published. Review any changed research weights before regenerating an already traded session.
