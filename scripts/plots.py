import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def create_enhanced_plots():
    # 1. Load the data
    try:
        df = pd.read_csv('final_mutation_analysis.csv')
    except:
        print("❌ Error: Could not find 'final_mutation_analysis.csv'.")
        return

    # Set high-resolution and professional style
    plt.rcParams['figure.dpi'] = 300 
    sns.set_theme(style="whitegrid", palette="muted")
    
    fig, axes = plt.subplots(1, 3, figsize=(22, 7))

    # --- PLOT 1: PARITY PLOT (Accuracy Toolkit) ---
    sns.regplot(x='target_ddg', y='predicted_ddg', data=df, ax=axes[0], 
                scatter_kws={'alpha':0.4, 'color':'#2c3e50'}, 
                line_kws={'color':'#e74c3c', 'label':'Ideal Fit'})
    
    axes[0].set_title('Model Reliability Analysis', fontsize=15, fontweight='bold')
    axes[0].set_xlabel('Experimental ΔΔG (kcal/mol)', fontsize=12)
    axes[0].set_ylabel('Predicted ΔΔG (kcal/mol)', fontsize=12)
    
    # Labeling Zones (Toolkit for non-experts)
    axes[0].text(0.5, -3.5, "Destabilizing ↓", color='red', fontweight='bold', fontsize=10)
    axes[0].text(0.5, 0.5, "Stabilizing ↑", color='green', fontweight='bold', fontsize=10)

    # --- PLOT 2: THERMODYNAMIC DISTRIBUTION ---
    sns.kdeplot(df['predicted_ddg'], fill=True, ax=axes[1], color='#3498db', linewidth=2)
    axes[1].axvline(0, color='black', linestyle='--', alpha=0.6)
    axes[1].set_title('Thermodynamic Stability Profile', fontsize=15, fontweight='bold')
    axes[1].set_xlabel('Predicted ΔΔG Change', fontsize=12)
    
    # Annotation for biological relevance
    axes[1].annotate('Most Mutations\nare Destabilizing', xy=(-1.5, 0.2), xytext=(-3.5, 0.4),
                     arrowprops=dict(facecolor='black', shrink=0.05, width=1))

    # --- PLOT 3: FEATURE IMPACT (Biochem Toolkit) ---
    # Calculating Feature Importance (Absolute Correlation)
    feat_imp = df[['delta_hydro', 'delta_mw', 'delta_pi', 'target_ddg']].corr()['target_ddg'].drop('target_ddg').abs()
    feat_imp.index = ['Hydrophobicity Δ', 'Molecular Weight Δ', 'pI (Charge) Δ']
    feat_imp = feat_imp.sort_values()

    colors = sns.color_palette("YlGnBu", len(feat_imp))
    feat_imp.plot(kind='barh', ax=axes[2], color=colors)
    
    axes[2].set_title('Key Stability Drivers', fontsize=15, fontweight='bold')
    axes[2].set_xlabel('Impact Magnitude (Correlation)', fontsize=12)
    
    # Add data labels to the bars
    for i, v in enumerate(feat_imp):
        axes[2].text(v + 0.01, i, f'{v:.2f}', color='black', va='center', fontweight='bold')

    plt.tight_layout()
    
    # Save with high DPI for GitHub
    plt.savefig('biochem_analytics_final.png', bbox_inches='tight', dpi=300)
    print("✅ SUCCESS: Sharper plots saved as 'biochem_analytics_final.png'")
    plt.show()

if __name__ == "__main__":
    create_enhanced_plots()