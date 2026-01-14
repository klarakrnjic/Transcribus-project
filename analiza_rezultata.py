import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

# Load data
char_subs = pd.read_csv('moj_rezultat_char_subs.csv')
errors = pd.read_csv('moj_rezultat_errors.csv')
with open('moj_rezultat_stats.json', 'r') as f:
    stats = json.load(f)

# Errors from errors.csv
insertions = len(errors[errors['error_type'] == 'I'])
substitutions = len(errors[errors['error_type'] == 'S'])
total_chars = stats['total_chars_hyp']

# Plots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Error count by type
ax1.bar(['Insertions', 'Substitutions'], [insertions, substitutions], color=['blue', 'red'])
ax1.set_title('Error Count')
ax1.set_ylabel('Count')

# Plot 2: Top 10 substitutions (if any)
if len(char_subs) > 1 and char_subs['count'].sum() > 0:
    top_subs = char_subs.nlargest(10, 'count')[['ref_char', 'hyp_char', 'count']]
    pivot = top_subs.pivot(index='ref_char', columns='hyp_char', values='count').fillna(0)
    sns.heatmap(pivot, annot=True, ax=ax2)
    ax2.set_title('Most Common Substitutions')
else:
    ax2.text(0.5, 0.5, 'No substitutions\n(0 found)', ha='center', va='center', transform=ax2.transAxes)
    ax2.set_title('Substitutions')

plt.tight_layout()
plt.savefig('results_graphs.png', dpi=300)
plt.show()

cer = (insertions + substitutions) / total_chars if total_chars > 0 else 0
print(f'Insertions: {insertions}, Substitutions: {substitutions}')
print(f'Total chars: {total_chars}, CER: {cer:.4f}')
