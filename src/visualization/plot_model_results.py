import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

def set_publication_style():
    """Set the matplotlib parameters for publication-quality figures."""
    rcParams['font.family'] = 'Times New Roman'
    rcParams['font.size'] = 8
    rcParams['axes.labelsize'] = 8
    rcParams['axes.titlesize'] = 9
    rcParams['xtick.labelsize'] = 8
    rcParams['ytick.labelsize'] = 8
    rcParams['legend.fontsize'] = 8
    
    # Set figure size for IEEE column width
    rcParams['figure.figsize'] = (3.5, 7)  # Adjusted height for three subplots
    rcParams['figure.dpi'] = 300
    
    rcParams['axes.linewidth'] = 0.5
    rcParams['grid.linewidth'] = 0.5
    rcParams['lines.linewidth'] = 0.5
    rcParams['lines.markersize'] = 3
    rcParams['axes.labelpad'] = 4

def visualize_model_results():
    """Visualize the results of all models in separate subplots."""
    set_publication_style()
    
    # Read the evaluation results
    df = pd.read_csv('data/results/evaluation_dataset_with_model_output.csv')
    df['date_report'] = pd.to_datetime(df['date_report'], format='%Y/%m/%d')
    
    # Define models and their thresholds
    models = {
        'Baseline Model': ('baseline_model', None),
        'Proposed Model (t=40)': ('proposed_model_40', 40),
        'Proposed Model (t=60)': ('proposed_model_60', 60)
    }
    
    # Create figure with subplots
    fig, axes = plt.subplots(3, 1, sharex=True)
    # fig.suptitle('Comparison of Model Predictions', y=0.95)
    
    for (title, (model_col, threshold)), ax in zip(models.items(), axes):
        # Create prediction correctness column
        df['prediction_correct'] = (df['label_encoded'] == df[model_col].astype(int))
        
        # Create scatter plot
        scatter = ax.scatter(
            df['date_report'], 
            df['score_by_proposed_model'],
            c=df['prediction_correct'],
            cmap='bwr',  # Changed colormap for binary data
            alpha=0.7,
            s=20
        )
        
        # Add threshold line if applicable
        if threshold:
            ax.axhline(
                y=threshold,
                color='r',
                linestyle='--',
                linewidth=0.5,
                label=f'Threshold (t={threshold})'
            )
        
        # Customize subplot
        ax.set_ylabel('Model Score')
        ax.set_title(title, pad=10, size=8)
        
    # Add legend outside subplots
    legend_labels = ['Incorrect', 'Correct']
    legend = plt.legend(
        handles=scatter.legend_elements()[0],
        labels=legend_labels,
        title="Prediction:",
        frameon=True,
        edgecolor='black',
        fancybox=False,
        loc='lower center',
        bbox_to_anchor=(0.15, -0.02)  # Adjust location below subplots
    )
    legend.get_frame().set_linewidth(0.5)
        
    # Add grid
    ax.grid(True, alpha=0.3, linewidth=0.5)
    
    # Set common x-label
    axes[-1].set_xlabel('Report Date')
    
    # Rotate x-axis labels
    plt.setp(axes[-1].get_xticklabels(), rotation=45, ha='right')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save plots
    plt.savefig(
        'docs/figures/model_comparison_results.pdf',
        dpi=300,
        bbox_inches='tight',
        pad_inches=0.1,
        format='pdf'
    )
    plt.savefig(
        'docs/figures/model_comparison_results.png',
        dpi=300,
        bbox_inches='tight',
        pad_inches=0.1
    )
    
    plt.close()

if __name__ == "__main__":
    visualize_model_results()
