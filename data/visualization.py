import seaborn as sns
import matplotlib.pyplot as plt
import work as w
from sql import queries as q


fig, axes = plt.subplots(
    nrows = 1,
    ncols = 2,
    figsize=(11, 4.5))
axes[0].scatter(
    x = w.combined['avg_delivery_days'],
    y = w.combined['avg_freight_ratio_pct'],
    color = 'steelblue',
    alpha = 0.7
)
axes[0].set_xlabel('Average Delivery Days')
axes[0].set_ylabel('Freight Ratio (% of Price)')
axes[0].set_title(f'Delivery Speed VS Cost\n (r = {w.corr_speed_cost:.3f}, p < 0.001)')

axes[1].scatter(w.combined['logistics_burden'],
                w.combined['cancel_rate_pct'],
                color = 'red',
                alpha = 0.7
                )
axes[1].set_xlabel('Logistic Burden Score')
axes[1].set_ylabel('Cancel Rate %')
axes[1].set_title(f'Logistics Burden VS Cancellations\n(r={w.corr_final:.3f}, p={w.p_final:.3f})')

plt.tight_layout()
plt.savefig('../images/state_level_investigation.png',
            dpi=150,
            bbox_inches='tight')



top_sorted = w.top_candidates.sort_values(
    by = 'priority_score',
    ascending = False
)
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(top_sorted['customer_state'], top_sorted['increase_pct'],
       color='steelblue'
       )
ax.set_xlabel('State')
ax.set_ylabel('Order Growth (%)')
ax.set_title('Order Growth Rate in Top Warehouse Candidate States (2017→2018)')

for i, v in enumerate(top_sorted['increase_pct']):
    ax.text(i, v + 2, f'{v:.0f}%', ha='center')

plt.tight_layout()
plt.savefig('../images/top_states_growth.png',
            dpi=150,
            bbox_inches='tight')



#---------------------------
print('-'*50)




plt.figure(figsize=(9, 6))

ax = sns.regplot(
    data=q.category_freight_stats,
    x='avg_freight_ratio_pct',
    y='cancel_rate_pct',
    scatter_kws={
        'color': 'cadetblue',
        'alpha': 0.7,
        's': 60,
    },
    line_kws={
        'color': 'tomato',
        'linewidth': 2,
        'linestyle': '--',
    },
)

plt.title(
    f'Freight Ratio vs Cancel Rate by Category (r = {w.corr_cat:.3f}, p = {w.p_val_cat:.3f})',
    fontsize=13,
    pad=15,
)


plt.xlabel('Average Freight Ratio (%)', fontsize=11)
plt.ylabel('Cancellation Rate (%)', fontsize=11)
plt.grid(True, linestyle=':', alpha=0.6)

sns.despine()

plt.tight_layout()
plt.savefig(
    '../images/category_cancellations.png', dpi=150, bbox_inches='tight'
)
plt.show()
