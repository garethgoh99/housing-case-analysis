# Methods

How the dashboard compares renting, a resale HDB flat and a new-launch condo. Last updated 26 Oct 2026 (wealth comparison added).

## The deciding metric

**Wealth at exit** (the default, "Compare total wealth" switched on). Net gain on its own favours whichever path puts the most cash into the home, so the fair comparison gives all three cases the same money:

- Every case starts with the same **starting cash** (cash plus usable CPF OA), earns the same **monthly income** (household take-home pay plus CPF OA contributions) and pays the same **living costs** and **utilities**. Income and costs can each grow by a set % once a year.
- Each month: pot = pot × (1 + monthly return) + income − living costs − utilities − that case's housing outflow. Only what's left is invested. The monthly return is the annual investment return converted to a monthly rate.
- If a pot goes below zero, that case has run out of cash. The negative balance is charged **shortfall interest** instead of earning the return, and the card shows when it happened and how low it got.
- Anything a case paid before the start month is taken out of its starting cash.
- **Wealth at exit** = pot at exit + cash back from the sale. Money put into the home is not double-counted: it leaves the pot when paid and comes back through the sale.
- The **Net worth** chart shows pot + home equity (value − loan) each month; the last point is after selling.
- With time value of money on, wealth is also shown in today's dollars (discounted at the discount rate).

**Net gain at exit** = cash back from the sale − everything paid in. It is still shown on each card ("Net gain on housing") and becomes the headline if "Compare total wealth" is switched off. With time value of money on, it is the NPV of the monthly flows at the discount rate.

## Period

- The comparison runs from the start month to the exit (sale) month.
- The exit can never be earlier than the end of the HDB MOP (keys + MOP), so all three cases cover the same period. If you pick an earlier exit, the page moves it and says so.

## Default scenario

**Period**
- Start Oct 2026. Exit Aug 2032 = HDB key collection + 5-year MOP.

**Rates**
- 3M compounded SORA 1.23% (5 Oct 2026), plus a 0.30% bank spread = 1.53% bank rate.
- HDB concessionary loan 2.6% (CPF OA 2.5% + 0.1%).
- Discount rate for time value of money: 2.5% (the CPF OA rate).

**Rent**
- $2,000/mo from Aug 2027, rising to $4,500/mo from Jan 2030.

**Resale HDB**
- Price $900,000. Completion/payment Jan 2027. Keys Aug 2027. MOP 5 years.
- HDB loan at 75% LTV over 25 years: about $3,062/mo.
- Upfront at completion $249,600: $225K downpayment + $21.6K BSD + $3K legal.
- No rent before key collection.
- Service & conservancy charges $80/mo from key collection. Property tax $0 (set your own).

**Condo**
- Price $1,980,000. OTP and S&P Oct 2026, foundation already laid. TOP Apr 2029. CSC 12 months after TOP.
- Bank loan at 75% over 30 years.
- Upfront about $566.6K: $495K equity + $68.6K BSD + $3K legal.
- Rent of $2,500/mo from Jul 2027 until TOP.
- Instalment after CSC about $5,470/mo.
- Maintenance $350/mo from TOP. Property tax $0 (set your own).

**Cash & income** (placeholders; set your own)
- Starting cash $600,000. Income $11,500 a month, living costs $3,300 and utilities $200, leaving $8,000 a month for housing and investing. No income growth or cost inflation. Invested at 4% a year; shortfall interest 6% a year.

**Growth and exit**
- HDB 2.0% a year, condo 2.5% a year (the "Base" preset; placeholders, not forecasts).
- Agent fee 1% on each sale. Legal on sale $2,500 (HDB), $3,000 (condo).

### Results with the defaults (nominal)

**Wealth at exit** (start $600,000, $8,000/mo left after living costs, invested at 4%):

| Case | Wealth at exit | Lowest cash balance |
|---|---|---|
| Rent | $1,173,526 | $608,000 (Oct 2026) |
| Resale HDB | $1,280,307 | $388,470 (Jan 2027) |
| Condo | **$1,281,743** | $41,400 (Oct 2026) |

The condo's lead over the HDB is only about $1.4K, and it depends on the investment return. With everything else at the defaults:

| Return on invested cash | Rent | Resale HDB | Condo |
|---|---|---|---|
| 2.5% | $1,091,456 | $1,225,351 | **$1,262,274** |
| 4% | $1,173,526 | $1,280,307 | **$1,281,743** |
| 6% | $1,291,456 | **$1,359,203** | $1,309,380 |

**Net gain at exit:**

| Case | Total paid in | Cash back at exit | Net |
|---|---|---|---|
| Rent | $202,000 | $0 | −$202,000 |
| Resale HDB | $459,652 | $432,886 | −$26,766 |
| Condo | $871,331 | $935,415 | **+$64,085** |

- Before maintenance and S&CC were added, net gain was −$21,886 (HDB) and +$78,435 (condo).

`tools/check.mjs` re-runs the engine on these defaults on every deploy and fails if the nominal net gain or wealth figures drift by more than $50.

## Calculation rules

### Stamp duty
- **BSD (IRAS residential tiers):** 1% on the first $180K, 2% on the next $180K, 3% on the next $640K, 4% on the next $500K, 5% on the next $1.5M, 6% above that.
- **ABSD:** a selectable % (0 for a first home).
- **SSD (condo):** 16% / 12% / 8% / 4% of the sale price if sold within 1 / 2 / 3 / 4 years of S&P.

### Loan limits (MAS)
- HDB loan: max 75% LTV and max 25-year tenure.
- Bank loan on an HDB flat: 75% if the tenure is 25 years or less, otherwise 55%. Max 30 years.
- Private property: 75% if the tenure is 30 years or less, otherwise 55%. Max 35 years.
- Any loan running past age 65 is capped at 55%.
- Bank loans need at least 5% cash.

### Resale HDB cash flows
- At completion: downpayment + BSD + ABSD + legal; the loan is drawn.
- Instalments from the month after completion, at a fixed rate.
- Renovation (optional) is paid at key collection and builds no equity.
- Optional rent runs from its start month until the month before key collection.
- Service & conservancy charges and property tax are paid monthly from key collection. They build no equity.

### Condo progressive payments

| Stage | % of price |
|---|---|
| OTP | 5% |
| S&P | 15% |
| Foundation | 10% |
| Reinforced concrete | 10% |
| Brick walls | 5% |
| Ceiling/roofing | 5% |
| Wiring/plumbing | 5% |
| Roads/carparks/drains | 5% |
| TOP | 25% |
| CSC | 15% |

- The buyer pays the stages in order until their share (100% − LTV) is covered; after that the bank pays.
- Instalments start the month after each disbursement and are recalculated over the remaining tenure, counted from the first disbursement.
- Auto-estimated stage dates are spread between S&P and TOP at 15% (foundation, if not yet laid), 40% (reinforced concrete), 60% (brick walls), 73% (ceiling/roofing), 83% (wiring/plumbing) and 93% (roads/carparks/drains) of the build period. Any date or % can be edited by hand.
- BSD, ABSD and legal fees are paid at S&P. Renovation is paid at TOP.
- Optional rent runs from its start month until TOP.
- Maintenance and property tax are paid monthly from TOP. They build no equity.

### Equity
- Equity = paid towards the price + principal repaid + price growth. Rent builds no equity.
- "Money not coming back" = total paid out − equity gained: rent, interest, stamp duty, fees, renovation, maintenance, S&CC and property tax.

### Exit
- Cash back = sale value − loan outstanding − agent fee − sale legal fees − SSD.
- Growth compounds from HDB completion and from the condo's S&P date.
- CPF refunds on sale (principal plus accrued interest) are treated as the buyer's own money, so they count as cash back.

### Return on cash
- The annualised IRR of the monthly flows, with the sale proceeds in the exit month.

### Affordability checks (optional, need household income)
- MSR: HDB-flat instalment up to 30% of gross monthly income.
- TDSR: total debt up to 55% of income, tested at a 4% stress rate.

### Simplifications
- Interest rates are held flat for the whole period. Bank packages usually reprice after 2–3 years; use the SORA picker to test higher levels.
- Maintenance, S&CC and property tax are flat monthly amounts with no increases. Home insurance is left to living costs.
- CPF OA usage and accrued interest are not tracked separately, and CPF held in the pot is assumed to earn the same return as invested cash.
- Investment returns are steady (no volatility) and untaxed, which is how most Singapore investment gains are treated.

## Open ideas
- Let the bank rate reprice after a lock-in period instead of staying flat.
- Add CPF OA usage and accrued-interest refund tracking.

## Sources
- HDB concessionary rate 2.6%, pegged to CPF OA + 0.1%: HDB / CPF Board quarterly releases, 2026.
- 3M SORA 1.23% on 5 Oct 2026: https://propoagroup.co/market/sora
- 2026 bank package range of about 1.3–1.8%: https://www.homejourney.sg/blog/bank-home-loan-rate-comparison-2026-homejourney-safe-guide
- HDB loan downpayment 25%: https://blog.moneysmart.sg/home-loans/hdb-loans-singapore-ultimate-guide-cost/

Rough guide only, not financial advice.
