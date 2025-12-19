# Typical Proportional Transaction Costs for Liquid Assets

## Executive Summary

Transaction costs for liquid assets vary significantly by asset class, ranging from as low as **0.5–2 basis points (bps)** for major FX pairs to **20–50+ bps** for less liquid equity segments. A basis point equals 0.01% (1/100th of 1%), so 10 bps = 0.10%. The table below summarizes typical round-trip costs across major liquid asset classes:[1]

| Asset Class | Typical Range (BPS) | Typical Range (%) | Notes |
|-------------|---------------------|-------------------|-------|
| **FX (Major Pairs)** | 2–5 bps | 0.02–0.05% | Institutional spot trades[2][3] |
| **FX (Retail/Minor Pairs)** | 8–30 bps | 0.08–0.30% | Retail spreads wider[4][5] |
| **U.S. Large-Cap Equities** | 5–15 bps | 0.05–0.15% | NYSE/NASDAQ stocks[6][7] |
| **Global Equities** | 6–20 bps | 0.06–0.20% | Higher for EM markets[6][8] |
| **Equity Index Futures (ES, SPY)** | 1–3 bps | 0.01–0.03% | E-mini S&P 500[9][10] |
| **Commodity Futures** | 15–25 bps | 0.15–0.25% | Crude oil, agricultural[11][12] |
| **Large-Cap Equity ETFs** | 1–10 bps | 0.01–0.10% | S&P 500 trackers[13][14] |
| **Bond ETFs (Investment Grade)** | 10–30 bps | 0.10–0.30% | Varies with liquidity[15][16] |
| **Commodity ETFs** | 25–50+ bps | 0.25–0.50%+ | Including roll costs[12] |

***

## 1. Foreign Exchange (FX)

Foreign exchange markets are among the most liquid globally, with daily turnover exceeding $7 trillion. Transaction costs in FX are exceptionally low for major currency pairs:[17]

**Institutional FX (Spot):**
- **Major pairs (EUR/USD, GBP/USD, USD/JPY):** 2–3 bps (0.02–0.03%) mean effective spread[2]
- **Minor currency pairs:** 5–10 bps or higher depending on liquidity[2]
- IMF data shows spot market spreads averaging 3–4 bps during normal conditions, widening to 4–5 bps during market stress[3]

**Retail/Broker FX:**
- **ECN/Raw spreads:** 0.0–0.2 pips (0–2 bps) plus commissions of $3.50–7.00 per standard lot round-trip[4][5]
- **Standard accounts:** 0.8–2.0 pips (8–20 bps) all-in spread[5]
- One pip in EUR/USD equals 0.0001, or approximately 1 bps of notional value[18]

**FX Forwards/Swaps:**
- Proportional costs for FX forwards are estimated at 0.5–7 bps depending on tenor and currency pair[19]
- Cross-currency basis can add 5–20+ bps for certain currency pairs[20]

Interactive Brokers charges tiered commissions of **0.08–0.20 bps** on spot FX trades based on monthly volume.[21][22]

***

## 2. Equities

Equity transaction costs include both explicit costs (commissions, exchange fees) and implicit costs (bid-ask spread, market impact):

**U.S. Equities:**
- **NYSE stocks:** Average transaction cost of 8.8 bps[6]
- **NASDAQ stocks:** Average transaction cost of 13.8 bps[6]
- **Median cost (U.S.):** 4.9 bps; value-weighted average: 9.5 bps[7][6]
- **Large-cap stocks:** 11.2 bps market impact; small-cap stocks: 21.3 bps[23]

**Institutional Equity Trading:**
- **Average market impact costs:** 20 bps for buys, 30 bps for sells[8][24]
- **Implementation shortfall (2022 data):** Improved to approximately 17 bps from 21 bps earlier in the year[25]
- **Large-cap real-world execution:** 15–35 bps per trade (AQR data); academic estimates of 100–200 bps are significantly overstated[26]

**Global Equities:**
- Median transaction cost: 5.9 bps; value-weighted average: 12.9 bps[7][6]
- International equity ETFs typically have wider spreads than domestic equivalents due to local market costs, taxes, and currency hedging[27]

**Market-Specific Fees (Examples):**
- South Korea: Exchange levy 4.33 bps, sales tax 10 bps[28]
- Dubai: Market fee 5.25 bps[28]
- Block trades on Euronext: 0.05 bps per side[29]

***

## 3. Equity Index Futures

Index futures offer among the lowest transaction costs of any tradable instrument due to deep liquidity:

**E-mini S&P 500 (ES):**
- **Total cost advantage:** Institutional investors save 8.9–13.3 bps versus trading ETFs[10][30]
- **Bid-ask spread:** Often 0.25 index points (1 tick), representing approximately 0.4–0.5 bps of notional value[31]
- **Commission:** $1.20–2.50 per contract plus exchange fees, negligible as percentage of notional (~$300,000 per contract)[31]
- **Round-trip trading cost (including slippage):** ~1.25 bps for S&P/TSX futures example[9]

**Long Gilt Futures:**
- Average bid-ask spread: 1.09 bps of notional[32]
- Implementation shortfall can range from -5 to +5 bps depending on execution quality[32]

**S&P 500 ESG Index Futures:**
- Market typically displays 500 contracts per side with 6–7 bps spread[33]

***

## 4. Commodity Futures

Commodity futures transaction costs vary significantly by contract:

**Crude Oil (WTI):**
- **Roll costs for commodity ETFs (USO):** ~25 bps per quarterly roll, or approximately 3% annually[12]
- Exchange fees: $0.65–1.50 per contract depending on contract size[34]
- Transaction costs for oil futures using one or two currencies estimated at ~4 bps[35]

**Precious Metals (Gold/Silver):**
- **Spot gold/silver (IBKR):** 1.5 bps minimum commission per transaction[36]
- **Physical gold:** Dealer spreads of 1–4% for coins, 0.5–2% for large bars[37][38]
- **Futures spreads:** Gold generally tighter than silver due to higher liquidity[39]

**Agricultural/Other Commodities:**
- Conservative trading cost estimates: ~22 bps per trade[11]
- Commodity index hedging: Typical cost reduction of 1.5 bps from CIT activity[40]

***

## 5. Exchange-Traded Funds (ETFs)

ETF costs comprise expense ratios (ongoing) and trading costs (transactional):

**Large-Cap Equity ETFs (S&P 500):**
- **SPY (SPDR S&P 500):** 30-day median bid-ask spread of 0.03% (3 bps)[41][42]
- **Most liquid equity ETFs:** Transaction costs below 6 bps average[14]
- **Typical spreads:** 1–10 bps for highly liquid products[43]

**Bid-Ask Spreads by Category (Median):**[15]
| ETF Category | Typical Range (bps) | Median (bps) |
|--------------|---------------------|--------------|
| Canadian equities | 3–17 | 9 |
| U.S. equities | 2–20 | 9 |
| Emerging markets equities | 4–100 | 39 |
| Investment grade bonds | 2–26 | 13 |
| High yield bonds | 11–100 | 34 |

**Additional ETF Cost Considerations:**
- **Expense ratios:** 0.03–1.50% annually (deducted daily from NAV)[44][13]
- **Premium/discount volatility:** Can add 4–125 bps in round-trip costs[45]
- **Leveraged ETFs:** Higher expense ratios of 0.9–1.5% due to derivative complexity[13]
- **Currency hedging:** Adds 10–60 bps to total expense ratio[13]

***

## 6. Fixed Income

Bond transaction costs tend to be higher than equities due to lower liquidity:

**Corporate Bonds:**
- **Fixed cost (half bid-ask):** ~3 bps average[46]
- **Price impact:** 32 bps per traded amount for typical bonds[46]
- **Median fund trading costs:** 30–35 bps annually (2.4–2.9 bps monthly)[46]
- **Trade size effect:** V-shaped cost curve with 15 bps for $10 million IG bonds, higher for smaller/larger trades[46]

**Bond ETFs:**
- Industry average OCF: 23 bps (down from 28 bps)[47]
- **Investment grade:** 10–30 bps spreads[15]
- **High yield:** 34 bps median, up to 100 bps for illiquid products[15]
- Physical bond transaction costs range 1–5% of value for retail investors[16]

***

## 7. Cost Component Breakdown

Transaction costs can be decomposed into explicit and implicit components:

**Explicit Costs:**
- Commissions: 0–10 bps (many platforms now offer zero commissions)[44][13]
- Exchange fees: 0.05–5 bps depending on venue[29][28]
- Transaction taxes: 0–50 bps (varies by jurisdiction)[28]

**Implicit Costs:**
- **Bid-ask spread:** Primary component, 1–100+ bps depending on liquidity[48][49]
- **Market impact:** 5–50+ bps for institutional-size trades[8][23]
- **Timing/delay costs:** Variable, captured in implementation shortfall metrics[50]

***

## Key Takeaways

1. **FX is cheapest:** Major currency pairs trade with costs of 2–5 bps, making forex among the most cost-efficient markets for institutional traders.[3][2]

2. **Index futures offer excellent value:** E-mini S&P 500 futures provide exposure at 1–3 bps round-trip, significantly cheaper than trading underlying stocks or ETFs.[9][10]

3. **Equity costs scale with liquidity:** Large-cap U.S. stocks average 5–15 bps, while small-caps and emerging markets can exceed 50+ bps.[51][6]

4. **ETF costs vary widely:** S&P 500 ETFs trade at 1–10 bps spreads, but emerging market and high-yield products can reach 50–100+ bps.[15]

5. **Commodity costs include roll premiums:** Beyond direct trading costs (15–25 bps), futures-based commodity products incur quarterly roll costs that can add 100+ bps annually.[12]

6. **Implementation shortfall matters:** Academic "paper" transaction costs are often 2–4x higher than actual institutional execution costs due to sophisticated execution algorithms and internalized fund trading.[50][26]

[1](https://www.investopedia.com/terms/b/basispoint.asp)
[2](https://www.tarunramadorai.com/TarunPapers/TransCostsForex.pdf)
[3](https://www.imf.org/-/media/files/publications/gfsr/2025/october/english/ch2.pdf)
[4](https://www.icmarkets.eu/en/trading-pricing/trading-costs)
[5](https://investingoal.com/cost-forex-trading/)
[6](https://bsic.it/wp-content/uploads/2023/04/Modelling-transaction-costs-for-pdf.pdf)
[7](https://bsic.it/modelling-transaction-costs-and-market-impact/)
[8](https://www.sciencedirect.com/science/article/abs/pii/S0261560607000113)
[9](https://www.m-x.ca/f_publications_en/cost_of_trading_EN.pdf)
[10](https://www.cmegroup.com/markets/equities/sp/e-mini-sandp500.html)
[11](https://www.sciencedirect.com/science/article/abs/pii/S0378426614002751)
[12](https://www.cftc.gov/sites/default/files/idc/groups/public/@economicanalysis/documents/file/oce_predatorysunshine0314.pdf)
[13](https://www.tradingkey.com/learn/intermediate/etf/etf-cost-fee-system-breakdown-tradingkey)
[14](https://www.deutsche-boerse.com/dbg-en/media/news-stories/explainers/spotlight/ETFs-easy-transparent-flexible-144148)
[15](https://www.investmentexecutive.com/newspaper_/etf-guide/key-insights-about-bid-ask-spread-costs/)
[16](https://www.ssga.com/us/en/individual/insights/why-invest-in-bond-etfs)
[17](https://www.bis.org/statistics/rpfx25_fx.htm)
[18](https://atmosfunded.com/what-is-spread-in-forex/)
[19](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID4788137_code1311921.pdf?abstractid=3143970)
[20](https://www.cmegroup.com/articles/whitepapers/covered-interest-parity-implied-forward-foreign-exchange-swaps-cross-currency-basis-and-cme-estr-futures.html)
[21](https://www.interactivebrokers.ie/en/pricing/commissions-spot-currencies.php)
[22](https://www.interactivebrokers.com/en/pricing/commissions-spot-currencies.php)
[23](https://www.hbs.edu/faculty/Shared%20Documents/events/328/TradingCostEfficiency_FULL_112912.pdf)
[24](https://research.utwente.nl/en/publications/market-impact-costs-of-institutional-equity-trades-3/)
[25](https://www.bloomberg.com/professional/insights/trading/buy-side-equity-trading-costs-ease-through-2022/)
[26](https://sghiscock.com.au/wp-content/uploads/2025/01/SGH_EAM-Investors-Momentum-and-Trading-Costs.pdf)
[27](https://www.im.natixis.com/en-us/insights/portfolio-construction/2024/etf-cost-bid-ask-spread)
[28](https://www.jpmorgan.com/content/dam/jpm/global/disclosures/us/mifidii-global-equities-charges-guide.pdf)
[29](https://www.euronext.com/sites/default/files/2025-02/Market%20Maker%20Liquidity%20Provider%20Trading%20Fee%20Guide%20Euronext%20Cash%20Markets_Effective%2001FEB2025.pdf)
[30](https://www.cmegroup.com/markets/equities/sp/e-mini-sandp500.quotes.html)
[31](https://www.dormantrading.com/TraderTools/CMEeminisp500.pdf)
[32](https://www.cmegroup.com/education/files/TCA-4.pdf)
[33](https://www.spglobal.com/spdji/en/documents/presentations/20220607-day1-1635-listed-derivatives-solutions-for-institutional-investors.pdf?force_download=true)
[34](https://tastytrade.com/learn/trading-products/futures/how-to-trade-oil-futures/)
[35](https://www.ecb.europa.eu/pub/pdf/scpops/ecbocp77.pdf)
[36](https://www.interactivebrokers.com/campus/trading-lessons/trading-spot-gold-and-silver-using-ibkrs-tws/)
[37](https://www.gainesvillecoins.com/blog/gold-bid-ask-spread-trading-prices-guide)
[38](https://goldsilver.com/industry-news/article/why-bid-ask-spreads-matter-for-precious-metals-investors/)
[39](https://www.jmbullion.com/investing-guide/bullion/bid-ask-spread/)
[40](https://www.cftc.gov/sites/default/files/idc/groups/public/@economicanalysis/documents/file/oce_commodityindextrading.pdf)
[41](https://www.ssga.com/us/en/intermediary/etfs/spdr-sp-500-etf-trust-spy)
[42](https://www.ssga.com/nl/en_gb/intermediary/etfs/spdr-sp-500-etf-trust-spy)
[43](https://publishedresearch.cambridgeassociates.com/wp-content/uploads/2016/10/Practical-Considerations-for-ETF-Investing.pdf)
[44](https://www.schwab.com/learn/story/etfs-how-much-do-they-really-cost)
[45](https://corporate.vanguard.com/content/corporatesite/us/en/corp/articles/etf-premiums-and-discounts-explained.html)
[46](https://www.tandfonline.com/doi/full/10.1080/0015198X.2024.2360390)
[47](https://www.fr.vanguard/professionnel/analyses/bond-etfs-and-the-total-cost-of-ownership)
[48](https://www.projectivegroup.com/priips-ucits/)
[49](https://www.ici.org/files/2024/per30-10.pdf)
[50](https://academic.oup.com/rof/article/29/1/103/7755053)
[51](https://grokipedia.com/page/Market_impact)
[52](https://www.venturasecurities.com/blog/understanding-basis-point-trading-futures-trading-strategy/)
[53](https://www.grahamcapital.com/wp-content/uploads/2023/08/Transaction-Costs_GCM-Research-Note_Jul-17.pdf)
[54](https://www.investopedia.com/terms/t/transactioncosts.asp)
[55](https://www.accaglobal.com/gb/en/student/exam-support-resources/professional-exams-study-resources/p4/technical-articles/basis-risk.html)
[56](https://northern.finance/en/etf/etf-costs-in-detail/)
[57](https://www.wiwi.hu-berlin.de/en/Professorships/vwl/wtm2/seminar-schumpeter/working_camp_7-2016-1.pdf/@@download/file/working_camp_7-2016%5B1%5D.pdf)
[58](https://www.tastylive.com/concepts-strategies/pips-ticks-bips)
[59](https://www.wisdomtree.eu/-/media/eu-media-files/other-documents/educational/intra-day-pricing-how-etf-shares-are-priced.pdf?sc_lang=fr-fr&hash=E1CEE1822A82282205C609865DCF42CD)
[60](https://www.wienerborse.at/en/listing/fees/shares/)
[61](https://www.invesco.com/content/dam/invesco/uk/en/pdf/etfs-vs-futures-brochure-Q3-2021.pdf)
[62](https://treasuryxl.com/blog/fx-is-hedging-expensive/)
[63](https://russellinvestments.com/nz/blog/futures-etfs-physicals)
[64](https://www.bis.org/publ/work836.pdf)
[65](https://www.blackrock.com/corporate/literature/whitepaper/viewpoint-disclosing-transaction-costs-august-2018.pdf)
[66](https://milltech.com/resources/blog/how-can-you-find-out-your-FX-execution-costs)
[67](https://www.esma.europa.eu/sites/default/files/2025-01/ESMA50-524821-3525_ESMA_Market_Report_-_Costs_and_Performance_of_EU_Retail_Investment_Products.pdf)
[68](https://www.bolsasymercados.es/bme-exchange/docs/docsSubidos/Trading/equities-trading-fees.pdf)
[69](https://escholarship.org/content/qt4qw3p6rp/qt4qw3p6rp_noSplash_49607be9f2665ccf4d434f648d063cae.pdf)
[70](https://www.tradestation.com/insights/2025/05/28/spy-vs-spx-options-explained/)
[71](https://www.sciencedirect.com/science/article/abs/pii/S0304405X24001090)
[72](https://www.barchart.com/etfs-funds/quotes/SPY/options)
[73](https://www.monetary-metals.com/insights/articles/the-curious-widening-of-the-bid-ask-spread-in-silver/)
[74](https://www.investopedia.com/terms/f/foreign-exchange.asp)
[75](https://www.investing.com/etfs/spdr-s-p-500)
[76](https://www.home.saxo/learn/guides/forex/the-major-forex-pairs)
[77](https://www.cmegroup.com/education/courses/understanding-futures-spreads/gold-and-silver-ratio-spread-trade.html)
[78](https://www.millbankfx.com/institutional-fx-rates)
[79](https://www.nasdaq.com/market-activity/etf/spy)
[80](https://dev.to/miles_carter/how-futures-contracts-affect-the-precious-metal-market-23a7)
[81](https://www.elibrary.imf.org/display/book/9798229023184/CH002.xml)
[82](https://arxiv.org/html/2503.09647v4)
[83](https://hedgebook.com/calculating-fx-forward-points-2/)
[84](https://www.oxera.com/wp-content/uploads/2024/10/Oxera-report-on-UK-equity-market-October-2024.pdf)
[85](https://www.ecb.europa.eu/press/financial-stability-publications/fsr/focus/2011/pdf/ecb~938a721854.fsrbox201112_08.pdf?aa5b5e770027fc1fd18ea9c72868172e)
[86](https://www.cmegroup.com/markets/energy/crude-oil/light-sweet-crude.html)
[87](https://assets.kpmg.com/content/dam/kpmgsites/ch/pdf/cost-of-capital-study-2024.pdf.coredownload.inline.pdf)
[88](https://www.sciencedirect.com/science/article/pii/S0304405X22001490)
[89](https://www.investopedia.com/terms/f/forwardpoints.asp)
[90](https://www.commoditiesdemystified.info/pdf/CommoditiesDemystified-section-c-en.pdf)
[91](https://www.bis.org/publ/qtrpdf/r_qt1609y.htm)
[92](https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID3296165_code1709931.pdf?abstractid=2832600)
[93](https://www.greenwich.com/press-release/tca-minimizing-transaction-costs-maximizing-returns)
[94](https://analystprep.com/study-notes/cfa-level-iii/measurement-and-determination-of-cost-of-trade-2/)
[95](https://www.luxalgo.com/blog/how-post-trade-cost-analysis-improves-trading-performance/)
[96](https://developers.lseg.com/en/article-catalog/article/market-impact-calculations)
[97](https://www.tastylive.com/news-insights/spx-vs-es-futures-normal-spx-cheaper)
[98](https://www.ig.com/en-ch/learn-to-trade/ig-academy/the-basics-of-forex-trading/understanding-forex-spreads)
[99](https://www.bankingsupervision.europa.eu/activities/srep/2024/html/ssm.srep202412_aggregatedresults2024.en.html)
[100](https://www.captrader.com/en/glossary/sp-500-futures/)
[101](https://4t.com/en/learn-to-trade/spreads-and-swaps)
[102](https://www.ladwp.com/sites/default/files/2024-07/20240710%20Item%2009%20Pkg.pdf)
[103](https://www.cftc.gov/sites/default/files/filings/orgrules/18/01/rule012618cbotdcm002.pdf)
[104](https://research.lancaster-university.uk/files/422852483/2025BasicPhD.pdf)
[105](https://www.bis.org/publ/work1229.pdf)
[106](https://academic.oup.com/rfs/article/37/10/3092/7738093)
[107](https://alphaarchitect.com/best-times-etf-investors-trade/)
[108](https://www.bnpparibas-am.com/en-fi/institutional/portfolio-perspectives/fixed-income-etfs-bringing-bonds-to-all-investors/)
[109](https://advisors.vanguard.com/strategies/fixed-income/4-things-to-know-about-bond-etfs)
[110](https://www.bundesbank.de/resource/blob/766600/2fd3ae4f0593fb2ce465c092ce40888b/mL/2018-10-exchange-traded-funds-data.pdf)