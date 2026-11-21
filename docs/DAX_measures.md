# DAX measures

All measures are in the `_Measures` table of the Power BI model. Tables: `Opportunities` and `Leads` (facts); `DimAccount`, `DimDate`, `DimLeadSource`, `DimProduct`, `DimRep`, `DimStage` (dimensions).

| Measure | Formula | What it shows |
|---|---|---|
| Total Opportunities | `COUNTROWS(Opportunities)` | Number of opportunities |
| Closed Won Count | `CALCULATE(COUNTROWS(Opportunities), Opportunities[Stage] = "Closed Won")` | Won deals |
| Closed Lost Count | `CALCULATE(COUNTROWS(Opportunities), Opportunities[Stage] = "Closed Lost")` | Lost deals |
| Closed Won Revenue | `CALCULATE(SUM(Opportunities[Amount]), Opportunities[Stage] = "Closed Won")` | Revenue from won deals |
| Win Rate | `DIVIDE([Closed Won Count], [Closed Won Count] + [Closed Lost Count])` | Share of closed deals that were won |
| Avg Deal Size | `DIVIDE([Closed Won Revenue], [Closed Won Count])` | Average won deal |
| Open Pipeline | `CALCULATE(SUM(Opportunities[Amount]), NOT(Opportunities[Stage] IN {"Closed Won", "Closed Lost"}))` | Value of deals still open |
| Open Deal Count | `CALCULATE(COUNTROWS(Opportunities), NOT(Opportunities[Stage] IN {"Closed Won", "Closed Lost"}))` | Number of open deals |
| Weighted Pipeline | `SUMX(FILTER(Opportunities, NOT(Opportunities[Stage] IN {"Closed Won", "Closed Lost"})), Opportunities[Amount] * RELATED(DimStage[Probability]))` | Open pipeline weighted by stage probability |
| Avg Sales Cycle Days | `AVERAGEX(FILTER(Opportunities, Opportunities[Stage] = "Closed Won"), DATEDIFF(Opportunities[Opp Created Date], Opportunities[Close Date], DAY))` | Days from creation to close for won deals |
| Lead Count | `COUNTROWS(Leads)` | Number of leads |
| Lead to Opp Rate | `DIVIDE(CALCULATE(COUNTROWS(Opportunities), Opportunities[Type] = "New Customer"), [Lead Count])` | Share of leads that became opportunities (use by lead source) |
| Revenue YTD | `TOTALYTD([Closed Won Revenue], DimDate[Date])` | Year-to-date revenue |
| Revenue PY | `IF(ISBLANK([Closed Won Revenue]), BLANK(), CALCULATE([Closed Won Revenue], SAMEPERIODLASTYEAR(DimDate[Date])))` | Revenue in the same period one year earlier |
| Revenue YoY % | `DIVIDE([Closed Won Revenue] - [Revenue PY], [Revenue PY])` | Year-over-year growth |
| Open Pipeline Display / Avg Deal Size Display | `FORMAT(<measure>, "€ #,##0")` | Text versions for card visuals |

Notes: Year-over-year is shown per quarter only. Q4 2026 is incomplete.
