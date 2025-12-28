import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Podaci
data = {
    'Page': [1,2,3,4,5,6,7,8,9,10],
    'CER': [76.10,56.11,75.06,75.97,76.53,75.80,76.02,75.73,76.70,76.69],
    'WER': [98.32,54.87,98.07,97.57,98.38,97.99,97.60,97.76,98.91,97.38]
}

df = pd.DataFrame(data)

# Kreiranje grafikona
fig, ax1 = plt.subplots(figsize=(8, 5))

# Lijeva os - CER (plava)
color_cer = 'tab:blue'
line1 = ax1.plot(df['Page'], df['CER'], color=color_cer, marker='o', linewidth=2, markersize=6, label='CER')
ax1.set_xlabel('Page', fontsize=11, fontweight='bold')
ax1.set_ylabel('CER (%)', color=color_cer, fontsize=11, fontweight='bold')
ax1.tick_params(axis='y', labelcolor=color_cer)
ax1.set_ylim(0, 100)
ax1.grid(True, alpha=0.3)

# Desna os - WER (narančasta)
ax2 = ax1.twinx()
color_wer = 'tab:orange'
line2 = ax2.plot(df['Page'], df['WER'], color=color_wer, marker='s', linewidth=2, markersize=6, label='WER')
ax2.set_ylabel('WER (%)', color=color_wer, fontsize=11, fontweight='bold')
ax2.tick_params(axis='y', labelcolor=color_wer)
ax2.set_ylim(0, 110)

# Outlier Page 2 - CRVENA CRTA
ax1.axvline(x=2, color='red', linestyle='--', alpha=0.7, linewidth=1.5, label='Page 2 outlier')

# NASLOV
plt.title('Page-level CER and WER: Glagolitic PyLaia model\nMestrija dobra umrtija (10 pages, 250 lines)', 
          fontsize=12, fontweight='bold', pad=15)

# LEGENDA 
lines = line1 + line2
labels = ['CER', 'WER', 'Page 2 outlier']
fig.legend(lines, labels, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=3, fontsize=10)

plt.tight_layout()
plt.xticks(df['Page'])

# SPREMI
plt.savefig('mestrija_cer_wer.png', dpi=150, bbox_inches='tight', facecolor='white')
plt.savefig('mestrija_cer_wer_small.png', dpi=100, bbox_inches='tight')
plt.show()

print(" Grafikoni spremljeni:")
print(" mestiija_cer_wer.png (150 DPI)")
print(" mestiija_cer_wer_small.png (100 DPI)")
print(f"Mean CER: {df['CER'].mean():.2f}% (σ={df['CER'].std():.2f}%)")
print(f"Mean WER: {df['WER'].mean():.2f}% (σ={df['WER'].std():.2f}%)")
