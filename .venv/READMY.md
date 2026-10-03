# Brazilian E-Commerce: Warehouse Placement Analysis

## Business Question
Which Brazilian states are the best candidates for a new warehouse, and does
delivery logistics actually explain order cancellations?

## Data Source
Brazilian E-Commerce Public Dataset by Olist (Kaggle)
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

## Tools Used
SQL (SQLite), Python (pandas, scipy.stats, matplotlib, seaborn)

## Data Cleaning
- Merged duplicate product categories created by data re-ingestion
  (e.g. `casa_conforto_2` -> `casa_conforto`, `eletrodomesticos_2` ->
  `eletrodomesticos`), confirmed by comparing product counts before merging.
- Handled missing values in category and delivery-date fields.
- Filtered states with an unreliably small 2017 order base (< 100 orders)
  before computing growth rates, since percentage growth on a tiny base is
  misleading (e.g. 16 -> 44 orders shows as +175% but is not commercially
  meaningful).

## Context: Seller Concentration
Before looking at warehouse placement, it's worth noting how centralized
Olist's current logistics already are:
- **59.74%** of all sellers are based in a single state, SP.
- **63.82%** of all deliveries cross state lines (seller and customer are in
  different states).
- **39.19%** of all orders ship specifically from SP to other states.

This heavy reliance on one state as a shipping origin is part of why
delivery is slower and more expensive for customers farther from SP, and
why SP itself was excluded from the warehouse-candidate search below — the
question here is where a *second* hub would help most, not where the
existing one is.

---

## Investigation 1: Does delivery logistics drive cancellations?

**Hypothesis:** Slower and/or more expensive delivery leads to higher order
cancellation rates.

**Step 1 - Delivery speed vs. cancellation rate, by state**
r = 0.157, p = 0.433 -> weak, not statistically significant.

**Step 2 - Checking for multicollinearity**
Before testing delivery cost separately, delivery speed and freight-to-price
ratio were checked against each other, since both describe "logistics
quality" and could be redundant.
r = 0.755, p < 0.001 -> strong, significant correlation. Slower states are
also the states where freight eats a larger share of the order price,
likely reflecting distance from SP, the main shipping hub.

![Delivery Speed vs Cost, and Logistics Burden vs Cancellations](images/state_level_investigation.png)

**Step 3 - Combined logistics burden vs. cancellation rate**
Because speed and cost overlap, they were combined into a single rank-based
`logistics_burden` score and tested against cancellations, rather than
testing two redundant metrics separately.
r = 0.133, p = 0.509 -> still not significant.

**Step 4 - Independent check at the category level**
The same hypothesis was re-tested on a different slice of the data - freight
ratio vs. cancellation rate by product category, instead of by state.

![Freight Ratio vs Cancel Rate by Category](images/category_cancellations.png)

At first glance, this looked like it might support the hypothesis: the
`kids_and_baby` category had both a high cancellation rate (72%) and sat
away from the rest of the group, which could suggest a pattern. However,
other categories broke that pattern immediately - `books_hobbies_and_media`
had the single highest cancellation rate (88%) while its freight ratio
(35.98%) was close to the middle of the range, and the category with the
highest freight ratio (`technology_and_electronics`, 40.63%) did not have
an unusually high cancellation rate (52%). Running the correlation
confirmed what the mixed pattern suggested:
r = 0.137, p = 0.707 -> not significant. The wide confidence band in the
chart above (especially past ~34%) also reflects how few categories there
are (10) and how much individual outliers can swing the trend line.

**Conclusion:** The original idea behind this analysis was to find a
warehouse-placement answer through cancellations: if slow or costly
delivery was driving customers to cancel, building a warehouse in the
affected states would directly fix the cancellation problem. That theory
did not hold up — logistics (speed, cost, or a combined score, at both the
state and category level) does not explain cancellation rates in this
dataset. The cause likely lies elsewhere (price point, payment method, or
product-specific factors), which is outside this analysis's scope but
noted below as a next step.

> Note: freight costs in this dataset are paid by the customer, not
> absorbed by Olist or the seller. This means "logistics burden" reflects a
> customer-facing barrier to purchase, not a company operating cost.

---

## Investigation 2: Warehouse Placement Recommendation

Since cancellations turned out not to be a logistics problem, warehouse
placement could not be justified by "fewer cancellations." Instead, the
question was reframed around where a warehouse creates the most business
value directly — regardless of cancellations: states were ranked on two
independent, business-relevant criteria:
- **Delivery speed** (`avg_delivery_days`) - slower states benefit more
  from a nearby warehouse.
- **Order growth**, 2017 -> 2018 (same year-to-date period, since 2018 data
  ends around September), using both the growth rate and the absolute
  number of additional orders, so a small base inflating a percentage
  doesn't distort the ranking.

SP was excluded from the candidate pool, since it is already the dominant
shipping hub (see context above) — the goal here is to find the best
*additional* location, not to re-confirm SP's existing role.

**Top 5 candidate states** (ranked by combined priority score):

| State | Avg. Delivery Days | Order Growth Rate | Absolute Growth |
|-------|---------------------|--------------------|-------------------|
| BA    | 19.34                | 125%               | +1,038            |
| PE    | 18.45                | 132%               | +526              |
| MT    | 18.06                | 137%               | +295              |
| DF    | 12.97                | 169%               | +783              |
| MS    | 15.62                | 150%               | +257              |

![Order Growth Rate in Top Warehouse Candidate States](images/top_states_growth.png)

**DF** is a notable exception in this group: it already has the fastest
delivery by far (12.97 days, versus 15.6-19.3 days for the other four), yet
still ranks in the top 5 thanks to the highest growth rate (169%) and a
large absolute gain (+783 orders). This suggests DF's priority comes from
capturing a fast-growing market rather than fixing a delivery problem —
worth distinguishing from BA, PE, MT, and MS, where slow delivery is
clearly part of the case for a warehouse.

### Estimated Revenue Opportunity

Based on 2018 order volume x average order value, extrapolated using each
state's observed year-over-year growth rate:

| State | Current Revenue (R$) | Potential Additional Revenue (R$) |
|-------|------------------------|--------------------------------------|
| BA    | 284,841                | 354,940                              |
| PE    | 146,092                | 193,558                              |
| MT    | 87,759                 | 119,853                              |
| DF    | 178,358                | 300,980                              |
| MS    | 70,410                 | 105,820                              |

> This is a directional revenue opportunity estimate, not a full ROI
> calculation - warehouse setup and operating costs were not available in
> this dataset. Because freight is customer-paid, the mechanism here is
> indirect: faster/cheaper delivery is expected to improve conversion and
> repeat purchases, not reduce company costs directly.

---

## Limitations
- Small sample size (27 states, 10 macro-categories) limits statistical
  power for correlation tests.
- No warehouse cost data - recommendations are based on revenue
  opportunity, not full financial ROI.
- Cancellation drivers remain unidentified at the logistics level;
  category- and price-level analysis would be the next step.

## Next Steps
- Test whether cancellation rate correlates with payment method
  (installments vs. lump sum).
- Investigate price point as a possible cancellation driver.
- RFM customer segmentation as a complementary retention-focused analysis.

## How to Run
1. Clone the repo
2. Download the dataset from the Kaggle link above into `data/raw/`
3. `pip install -r requirements.txt`
4. Open `notebooks/analysis.ipynb`