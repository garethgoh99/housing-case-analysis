# Methods

How the dashboard compares housing paths in Singapore. Last updated 26 Oct 2026.

The design rule: allow for flexibility and nuance, but default to what you'd expect, so the tool stays quick to use. Every input has a sensible default; the yellow *key* fields are the ones you'll usually change, and everything else sits under *More settings*.

## Cases (tiles)

The page starts empty. You add cases as tiles, any number and any mix, including the same type twice (two condos at different prices, say). Each tile can be renamed, duplicated, collapsed or removed.

| Tile | What it models |
|---|---|
| Rent | Renting (or living with family) for the whole period, with rent changes on dates you set. |
| BTO | A new HDB flat: booking, agreement for lease, keys years later, MOP of 5 or 10 years, subsidy clawback for Plus and Prime flats. |
| Resale HDB | A resale flat: payment at completion, keys, 5-year MOP. |
| Resale condo | A completed private condo: option, exercise, completion, move-in. |
| New-launch condo | An off-plan condo on progressive payment, with editable construction milestones. |

## The deciding metric: wealth at exit

Comparing net gain on the home alone favours whichever path puts the most cash into the home. So every case gets the same money:

- The same **starting cash** (cash plus usable CPF OA).
- The same **monthly income** (take-home pay plus CPF OA contributions), which can grow once a year.
- The same **living costs**, which can inflate once a year.

Each month, for each case:

> pot = pot × (1 + monthly return) + income − living costs − that case's housing and utility costs (+ sale proceeds in the month it sells)

- The monthly return is the annual investment return converted to a monthly rate. Growth starts the month after money enters the pot.
- If a pot goes below zero, the case has run out of cash: the negative balance is charged **shortfall interest** instead, and the card flags when it happened. A balance under $20,000 is flagged as tight.
- Anything a case paid before the start month comes out of its starting cash.
- **Wealth at exit** = the pot in the last month, after every home in the comparison has been sold.
- Optionally, wealth is shown in today's dollars, discounted at a rate you set (default 2.5%, the CPF OA rate).

Money put into a home isn't double-counted: it leaves the pot when paid and comes back through the sale.

## Where you live, and when costs apply

- **Before move-in**, each buying case follows its own schedule: rent at a set amount (blank = the shared typical rent) or live with family at no cost. A schedule can change over time ("with family until Jul 2027, then rent at $2,500").
- **After selling**, if a case sells before the last case does, it rents at the typical rent (or lives with family) until the comparison ends.
- **Utilities** apply only in months you live in a rented or owned home, not while living with family. One shared figure; each case can override it.
- **Running costs** are monthly, and start when the home is yours to live in:
  - Resale HDB and BTO: service & conservancy charges and property tax from key collection.
  - Resale condo: maintenance and property tax from completion.
  - New-launch condo: maintenance and property tax from TOP.
- **Renovation** is paid in the move-in month and builds no equity.

## Exit (selling)

- By default every home is sold in the same month: the latest of each case's earliest sensible sale.
  - HDB and BTO: end of MOP (key collection + MOP).
  - Resale condo: 4 years after the option, when seller's stamp duty stops applying.
  - New-launch condo: the later of TOP and 4 years after S&P.
  - With no buying cases: 5 years from the start.
- You can set the shared exit by hand. An HDB or BTO flat can never be sold before its MOP ends; if the shared exit is earlier, that flat sells at its MOP and the other cases rent until then.
- Any case can be given its own sale date. The comparison runs until the last sale.
- **Cash back** = sale price − loan still owed − agent fee − legal fees − SSD − subsidy clawback.
  - **SSD** (condos): 16% / 12% / 8% / 4% of the sale price if sold within 1 / 2 / 3 / 4 years of the option (resale) or S&P (new launch).
  - **Clawback** (BTO): Plus 6%, Prime 9% of the sale price; Standard none. Editable.
- CPF used and CPF grants received must be refunded to your own CPF account, with accrued interest, on sale. That money is still yours, so it counts as cash back.

## Payment timing by case

**Resale HDB**
- At completion: downpayment (price − loan) + BSD + ABSD + legal. Loan drawn; instalments from the next month. Grants credited.
- Keys can be later than completion (extension of stay); MOP counts from keys.
- HDB concessionary loan (default, 2.6%) or bank loan.

**BTO**
- Booking: booking fee (default $2,000; part of the downpayment).
- Agreement for lease: rest of the downpayment due at signing + BSD + ABSD + legal.
  - Bank loan (default): 25% downpayment, of which 5% is paid at keys and the rest at signing.
  - HDB loan: the full downpayment at signing.
  - Staggered downpayment: half at signing, half at keys.
- Keys: any remaining downpayment, loan drawn, instalments from the next month, grants credited, move in.
- **Value:** a BTO is bought below market. Its value is tracked from an estimated **market value at signing**, by default 130% of the BTO price, and grows from there. Set your own estimate from nearby resale prices.
- Classification sets the defaults: Plus and Prime have a 10-year MOP, Standard 5 years. MOP and clawback can both be edited.

**Resale condo**
- Option and exercise: 5% in cash (1% option + 4% exercise) + BSD + ABSD + legal.
- Completion (default 3 months after the option): the rest of the downpayment; loan drawn; maintenance and property tax start.
- Move in (default a month after completion): renovation; utilities start.

**New-launch condo** (progressive payment)

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

- You pay the stages in order until your share (100% − loan %) is covered; then the bank pays.
- Instalments start the month after each disbursement and are recalculated over the remaining tenure, counted from the first disbursement.
- BSD, ABSD and legal fees are paid at S&P.
- Auto-estimated stage dates are spread between S&P and TOP at 15% (foundation, unless already laid), 40%, 60%, 73%, 83% and 93% of the build period. Any date or % can be edited.

## Stamp duty and loan limits

- **BSD (IRAS residential tiers):** 1% on the first $180K, 2% on the next $180K, 3% on the next $640K, 4% on the next $500K, 5% on the next $1.5M, 6% above that.
- **ABSD:** a selectable % (0 for a first home).
- **LTV caps (MAS):**
  - HDB loan: max 75% and max 25-year tenure.
  - Bank loan on an HDB flat: 75% if the tenure is 25 years or less, otherwise 55%. Max 30 years.
  - Private property: 75% if the tenure is 30 years or less, otherwise 55%. Max 35 years.
  - Any loan running past age 65 is capped at 55%.
- **Affordability checks** (optional, with gross household income): MSR for HDB flats (instalment up to 30% of income) and TDSR for bank loans (up to 55% at a 4% stress rate).
- Rates are held flat for the whole period; the SORA picker tests other levels.

## Growth defaults

Each tile's price growth is prefilled automatically, and you can override it.

| Tile | Proxy |
|---|---|
| Resale HDB, BTO | All-Singapore HDB resale prices |
| Resale condo | RCR condo resales (non-landed) |
| New-launch condo | RCR condo resales and sub-sales (non-landed) |

- RCR is used for every condo as a deliberately middle-of-the-market proxy.
- New-sale prices are not used for the new-launch tile: they track launch pricing, not how a unit you own appreciates.

**Method**
- A 12-month (or 4-quarter) median $psf is compared with the same window a year earlier, giving up to 5 year-on-year rates, most recent first.
- These are blended with weights 40% / 25% / 15% / 10% / 10% (renormalised if fewer years exist). The latest year counts most, but the 5-year trend still shows through.

**Sources and refresh**
- HDB: `q/sg.json` published by [hdb-resale-dashboard](https://github.com/garethgoh99/hdb-resale-dashboard).
- Condo: the permanent transaction archive (`raw-data` branch) of [private-condo-analysis](https://github.com/garethgoh99/private-condo-analysis).
- `tools/growth.py` recomputes the defaults every Monday and on every push, writes `data/growth.json`, and the page loads it as `growth.json`. If a source can't be reached, its last value is kept; if the file can't be loaded, the page uses values built into it.

**Built-in values (26 Oct 2026)**

| | Latest year | Blended default |
|---|---|---|
| HDB (HDB Resale Price Index, to 3Q 2026) | +0.8% | 5.4% |
| RCR condo resales (to Sep 2026) | +3.5% | 5.1% |
| RCR condo resales + sub-sales (to Sep 2026) | +2.4% | 4.5% |

The HDB seed uses HDB's Resale Price Index because the HDB dashboard's data couldn't be reached when this was built. The first workflow run replaces it with that dashboard's median $psf.

These are backward-looking: the past five years include the 2021–2024 boom, so the blended rates are well above the latest year. Treat them as a starting point, not a forecast.

## Defaults

**Shared**
- Start Oct 2026.
- SORA 1.23% + 0.30% spread = 1.53% bank rate.
- Starting cash $560,000.
- Income $11,500 a month; living costs $3,300; utilities $200; typical rent $3,000.
- Invested at 4% a year; shortfall interest 6%.
- No income growth or cost inflation.

**New tiles** (prices are placeholders)

| | Resale HDB | BTO | Resale condo | New-launch condo |
|---|---|---|---|---|
| Price | $600,000 | $450,000 | $1,500,000 | $1,800,000 |
| Key dates | Completion and keys +3 months | Booking now, signing +9 months, keys +4 years | Option now, completion +3 months, move in +4 months | OTP now, S&P +2 months, TOP +3.5 years |
| Loan | HDB loan 2.6%, 75%, 25 years | Bank loan, 75%, 25 years | Bank loan, 75%, 30 years | Bank loan, 75%, 30 years |
| Running costs | S&CC $80, property tax $25 | S&CC $80, property tax $25 | Maintenance $400, property tax $120 | Maintenance $400, property tax $120 |
| Other | MOP 5 years | Plus: MOP 10 years, clawback 6% | | CSC 12 months after TOP |

- Every new buying tile rents at the typical rent until move-in.
- Agent fee 1% on sale; legal on sale $2,500 (HDB) or $3,000 (condo).
- Property tax figures are rough monthly equivalents for an owner-occupied home; replace them with your own.

## The built-in example

**Load example** recreates the original three-way comparison:

**Rent**
- With family until Jul 2027.
- $2,000/mo from Aug 2027, rising to $4,500/mo from Jan 2030.

**Resale HDB**
- $900,000. Completion Jan 2027, keys Aug 2027.
- HDB loan, 75%, 25 years.
- Growth 2.0% a year.
- With family until keys.

**New-launch condo**
- $1,980,000. OTP and S&P Oct 2026, foundation laid. TOP Apr 2029.
- Bank loan, 75%, 30 years.
- Growth 2.5% a year.
- With family until Jul 2027, then rent at $2,500 until TOP.

Everything else uses the defaults above. Exit: Aug 2032 (the HDB MOP).

| Case | Wealth at exit |
|---|---|
| Rent | $1,125,720 |
| Resale HDB | **$1,230,817** |
| New-launch condo | $1,226,247 |

- On these numbers the HDB is just $4.6K ahead.
- The condo's cash bottoms out at $1,600 in Oct 2026: with $560K starting cash, the condo case is only just affordable.

**One of each type**, all with defaults (exit Oct 2040, set by the BTO's 10-year MOP):

| Case | Wealth at exit |
|---|---|
| Rent | $2,095,890 |
| BTO | $2,996,328 |
| Resale HDB | $2,986,181 |
| Resale condo | **$3,362,375** |
| New-launch condo | $3,176,592 |

`tools/check.mjs` re-runs both scenarios on every deploy and fails if any figure drifts by more than $50. It uses the built-in growth values, so the result doesn't depend on the latest data.

## Simplifications

- Interest rates, rents, maintenance and property tax are flat unless you add changes.
- CPF OA usage and accrued interest are not tracked separately. CPF in the pot is assumed to earn the same return as invested cash.
- Investment returns are steady (no volatility) and untaxed.
- Resale levy, valuation-over-price (COV), insurance and the timing of grant disbursement are simplified or left out.

## Open ideas

- Let the bank rate reprice after a lock-in period instead of staying flat.
- Track CPF OA usage and accrued-interest refunds separately.

## Sources

- HDB concessionary rate 2.6%, pegged to CPF OA + 0.1%: HDB / CPF Board quarterly releases, 2026.
- 3M SORA 1.23% on 5 Oct 2026: https://propoagroup.co/market/sora
- BTO payment stages and downpayment splits: https://www.99.co/singapore/insider/bto-payment-timeline/
- Plus and Prime MOP and clawback: https://www.99.co/singapore/insider/bto-subsidy-clawback/
- Resale condo payment timeline: https://buddy.edgeprop.sg/discover/what-is-the-timeline-for-payment-for-a-resale-condo-f1090e15-c1ed-404b-b0f8-1708f5e909dd
- CPF housing grants (EHG up to $120,000; refunded to CPF on sale): https://propertynet.sg/enhanced-cpf-housing-grant-ehg-2026-income-tiers-payouts/
- HDB Resale Price Index: https://www.hdb.gov.sg/-/media/managing-my-home/selling-a-flat/process-for-selling-a-flat/resale-flat-planning/resale-statistics/RPI-Table.pdf

Rough guide only, not financial advice.
