from scipy import stats
from sql import queries as q
import raw as r


warehouse_candidates = (q.delivery_by_state.merge(
    q.growth_by_state, on ='customer_state').merge(
        q.cancellations_by_state, on = 'customer_state'))

print(warehouse_candidates.shape)
print(warehouse_candidates)

correlation, p_value = stats.pearsonr(
    warehouse_candidates['avg_delivery_days'],
    warehouse_candidates['cancel_rate_pct'])


#correlation - strength of the connection and p-value - the probability that such a connection could have arisen by chanceprint('cor: ',correlation,' val: ', p_value)
correlation, p_value = stats.pearsonr(
    q.category_freight_stats['avg_freight_ratio_pct'],
    q.category_freight_stats['cancel_rate_pct']
)
print(correlation, ' val: ', p_value)

combined = q.delivery_by_state.merge(q.cancellations_by_state, on='customer_state')

corr_speed_cost, p_speed_cost = stats.pearsonr(
    combined['avg_delivery_days'],
    combined['avg_freight_ratio_pct']
)

print(f"Speed and price: r={corr_speed_cost:.3f}, p={p_speed_cost:.4f}")
#Price and delivery time are connected – which means we need to combine them into one specific variable since we can't consider them separately anymore
combined['logistics_burden'] = (combined['avg_delivery_days'].rank() + combined['avg_freight_ratio_pct'].rank())/2
corr_final, p_final = stats.pearsonr(combined['logistics_burden'], combined['cancel_rate_pct'])
print(f"\nLogistics burden vs отмены: r={corr_final:.3f}, p={p_final:.4f}")

# Cancellations at the state level are not explained by logistics. There’s no reason to open warehouses to solve this problem
sellers_share = (r.sellers['seller_state'].value_counts(normalize=True) * 100).round(2)
print('top-5 states sellers:')

print(sellers_share.head())
merged_df = (
    r.order_items
    .merge(r.sellers[['seller_id', 'seller_state']], on='seller_id')
    .merge(r.orders[['order_id', 'customer_id']], on='order_id')
    .merge(r.customers[['customer_id', 'customer_state']], on='customer_id')
)
merged_df['is_same_state'] = merged_df['seller_state'] == merged_df['customer_state']
#pct of delivery between different states
cross_state_pct = (1 - merged_df['is_same_state'].mean()) * 100
print(f"\nShare of interstate deliveries: {cross_state_pct:.2f}%")

sp_to_others_pct = ((merged_df['seller_state'] == 'SP') & (~merged_df['is_same_state'])).mean() * 100
print(f"The share of all orders going from SP to other states: {sp_to_others_pct:.2f}%\n")

#----------------------------------------

#открыть склад чтобы снизить логистические издержки в регионах, где растет срос
reliable_growth = q.growth_by_state[(q.growth_by_state['orders_2017'] >= 100) & (q.growth_by_state['customer_state'] != 'SP')]

combined2 = q.delivery_by_state.merge(reliable_growth, on = 'customer_state')

combined2['priority_score'] = (
        combined2['avg_delivery_days'].rank(ascending = False)
        + combined2['increase_pct'].rank(ascending=False)
        + combined2['absolute_growth'].rank(ascending=False)
        )/3

top_candidates = combined2.sort_values('priority_score', ascending = True).head(5)
print(top_candidates[['customer_state', 'avg_delivery_days', 'increase_pct', 'absolute_growth','priority_score']])


top_candidates = top_candidates.merge(
    q.cancellations_by_state[['customer_state', 'avg_price']],
    on = 'customer_state'
)

#roi - rough ratio of total revenue
top_candidates['current_revenue'] = top_candidates['orders_2018'] * top_candidates['avg_price']
top_candidates['project_revenue'] = top_candidates['current_revenue'] * (1 + top_candidates['increase_pct'] /100)
#current revenue is multiplying by pct increase
top_candidates['potential_revenue_gain'] = top_candidates['project_revenue'] - top_candidates['current_revenue']

print(top_candidates[['customer_state', 'current_revenue', 'potential_revenue_gain']])

#----------------------------------------------
corr_cat, p_val_cat = stats.pearsonr(
    q.category_freight_stats['avg_freight_ratio_pct'],
    q.category_freight_stats['cancel_rate_pct']
)

print(f"Categories (Freight Ratio vs Cancel Rate): r = {corr_cat:.3f}, p-value = {p_val_cat:.4f}")


