import pandas as pd
import matplotlib.pyplot as plt

# Čitaj postojeći rezultati.csv
df = pd.read_csv('rezultati.csv', sep=';', decimal=',')
df['CER'] = pd.to_numeric(df['CER'], errors='coerce')
df['Linija'] = pd.to_numeric(df['Linija'], errors='coerce')

# Graf CER po linijama
plt.figure(figsize=(15, 6))
plt.subplot(1, 2, 1)
plt.plot(df['Linija'], df['CER'], marker='o', linewidth=2, markersize=3)
plt.title('CER per Line')
plt.xlabel('Line')
plt.ylabel('CER (%)')
plt.grid(True, alpha=0.3)

# Prosječni CER i boxplot
plt.subplot(1, 2, 2)
plt.boxplot(df['CER'].dropna())
plt.title(f' CER Distribution\nAvg: {df["CER"].mean():.2f}%')
plt.ylabel('CER (%)')

plt.tight_layout()
plt.savefig('cer_results.png', dpi=300)
plt.show()

print(f'Average CER: {df["CER"].mean():.2f}%')
print(f'Min CER: {df["CER"].min():.2f}%')
print(f'Max CER: {df["CER"].max():.2f}%')
