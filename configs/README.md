# Configuration Samples

This folder contains small public configuration files used by the open-source demo and dry-run paths.

## `targets.csv`

`targets.csv` is the default covered-stock universe used by:

```powershell
python daily_news_impact_pipeline\run_daily_news_impact_one_click.py --dry-run ...
```

The production system can replace this file with any universe that follows the same columns:

```text
ts_code,ticker,company_name,market,area,industry,list_date,index_code,column,orgId
```

The dry-run path uses this file to build selected target lists and source-update command plans without calling live crawlers or LLM APIs.
