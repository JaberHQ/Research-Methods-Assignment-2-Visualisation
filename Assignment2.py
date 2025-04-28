import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

df = pd.read_csv('Results_21MAR2022_nokcaladjust.csv')

if (df is not None):
    print("Data successfully imported")
else:
    print("Failed to load data")
    exit()

print("Columns in the dataset:", df.columns.tolist())
print("\nPreview of the data:")
print(df.head())

group_col = 'diet_group'
impact_cols = ['mean_ghgs', 'mean_land', 'mean_watuse', 'mean_eut', 'mean_bio']

diet_data = df.groupby(group_col)[impact_cols].mean()
print("\nDiet categories found:", diet_data.index.tolist())

if 'meat' not in diet_data.index:
    print("'meat' not found in the dataset")
    exit()

ref_vals = diet_data.loc['meat']
rel_impact = diet_data.copy()
for col in impact_cols:
    rel_impact[col] = (rel_impact[col] / ref_vals[col]) * 100

selected_diets = ['vegan', 'veggie', 'fish', 'meat', 'meat50', 'meat100']
available_diets = [d for d in selected_diets if d in rel_impact.index]

rel_impact = rel_impact.loc[available_diets]

categories = impact_cols
N = len(categories)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
angles += angles[:1]  

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

for diet in available_diets:
    values = rel_impact.loc[diet].tolist()
    values += values[:1]  # loop back to the first point
    ax.plot(angles, values, label=diet.capitalize())
    ax.fill(angles, values, alpha=0.1)

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)
ax.set_title("Relative Environmental Impact by Diet Type", y=1.1)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))

plt.tight_layout()
plt.show()