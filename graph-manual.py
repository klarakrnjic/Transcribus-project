import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Data
data_krnjic = {
    'Page': [1,2,3,4,5,6,7,8,9,10],
    'CER': [23.77,19.12,17.65,20.97,19.51,20.17,20.06,19.83,17.53,21.82],
    'WER': [75.90,76.88,69.57,77.16,82.02,76.00,68.71,76.09,77.91,75.81]
}

df_krnjic = pd.DataFrame(data_krnjic)

# create figure and axis objects
fig, ax1 = plt.subplots(figsize=(8, 5))

# left y-axis - CER (blue)
color_cer = 'tab:blue'
line1 = ax1.plot(df_krnjic['Page'], df_krnjic['CER'], color=color_cer, 
                 marker='o', linewidth=2, markersize=6, label='CER')
ax1.set_xlabel('Page', fontsize=11, fontweight='bold')
ax1.set_ylabel('CER (%)', color=color_cer, fontsize=11, fontweight='bold')
ax1.tick_params(axis='y', labelcolor=color_cer)
ax1.set_ylim(0, 85)
ax1.grid(True, alpha=0.3)

# right y-axis - WER (orange)
ax2 = ax1.twinx()
color_wer = 'tab:orange'
line2 = ax2.plot(df_krnjic['Page'], df_krnjic['WER'], color=color_wer, 
                 marker='s', linewidth=2, markersize=6, label='WER')
ax2.set_ylabel('WER (%)', color=color_wer, fontsize=11, fontweight='bold')
ax2.tick_params(axis='y', labelcolor=color_wer)
ax2.set_ylim(0, 90)

# title
plt.title('Page-level CER and WER \nMestrija dobra umrtija - Glagolitic PyLaia model (10 pages, 250 lines)', 
          fontsize=12, fontweight='bold', pad=15)

# legend
lines = line1 + line2
labels = ['CER', 'WER']
fig.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=2, fontsize=10)

plt.tight_layout()
plt.xticks(df_krnjic['Page'])

# save
plt.savefig('graph-manual.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.savefig('graph-manual_small.png', dpi=100, bbox_inches='tight')
plt.show()

print("Krnjić grafikon spremljen:")
print("graph-manual.png (150 DPI)")
print(f"Mean CER: {df_krnjic['CER'].mean():.2f}% (σ={df_krnjic['CER'].std():.2f}%)")
print(f"Mean WER: {df_krnjic['WER'].mean():.2f}% (σ={df_krnjic['WER'].std():.2f}%)")
