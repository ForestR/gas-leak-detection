from pickle import TRUE
import pandas as pd
from datetime import datetime
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns

def merge_evaluation_with_model_output(eval_dataset_path: str, model_output_path: str, output_path: str | None = None):
    """
    Merge evaluation dataset with model output based on device ID and date.
    
    Parameters:
    eval_dataset_path (str): The file path of the evaluation dataset.
    model_output_path (str): The file path of the model output.
    output_path (str | None): The file path to save the merged dataset. If None, skip saving.
    """
    
    # Load evaluation dataset
    eval_df = pd.read_csv(eval_dataset_path, 
                         usecols=['device_id_encoded', 'date_report', 'label'])
    
    # Load model output dataset
    model_df = pd.read_csv(model_output_path,
                          usecols=['device_id', 'date', 'score_likelihood', 'pulse_hourly'])
    model_df['score_likelihood'] = pd.to_numeric(model_df['score_likelihood'], errors='coerce')
    
    # Create merge keys
    eval_df['merge_key'] = eval_df.apply(
        lambda x: f"{x['device_id_encoded']}_{datetime.strptime(x['date_report'], '%Y/%m/%d').strftime('%Y-%m-%d')}", 
        axis=1
    )
    # debug: check the merge key for device D894
    print(eval_df[eval_df['device_id_encoded'] == 'D894']['merge_key'])
    
    model_df['merge_key'] = model_df.apply(
        lambda x: f"{x['device_id']}_{x['date']}", 
        axis=1
    )
    # debug: check the merge key for device D894
    print(model_df[model_df['device_id'] == 'D894']['merge_key'])
    
    # Merge datasets
    merged_df = pd.merge(
        eval_df,
        model_df,
        on='merge_key',
        how='inner'
    )
 

    # replace the value of LABEL
    merged_df['label'] = merged_df['label'].replace({'NORMAL': 'NO_LEAKAGE'})

    # add a column to encode the LABEL
    merged_df['label_encoded'] = merged_df['label'].map({'LEAKAGE': 1, 'NO_LEAKAGE': 0})

    # add a column to annotate the output of the baseline model
    merged_df['baseline_model'] = True  # ALL LEAKAGE FOR BASELINE MODEL

    # add a column to annotate the output of the proposed model (threshold = 40)
    merged_df['proposed_model_40'] = merged_df['score_likelihood'] >= 40

    # add a column to annotate the output of the proposed model (threshold = 60)
    merged_df['proposed_model_60'] = merged_df['score_likelihood'] >= 60

    # rename columns
    merged_df = merged_df.rename(columns={'score_likelihood': 'score_by_proposed_model'})

    # select columns    
    cols = ['device_id_encoded', 'date_report', 'label', 'label_encoded', 
            'baseline_model', 'proposed_model_40', 'proposed_model_60', 
            'score_by_proposed_model', 'pulse_hourly']
    
    # save to csv only if output_path is provided
    if output_path is not None:
        merged_df[cols].to_csv(output_path, index=False)
    
    return merged_df

def calculate_model_performance():
    """Calculate performance metrics for baseline and proposed models."""
    # Read the evaluation results
    df = pd.read_csv('data/results/evaluation_dataset_with_model_output.csv')
    
    # Models to evaluate
    models = {
        'Baseline Model': 'baseline_model',
        'Proposed Model (t=40)': 'proposed_model_40',
        'Proposed Model (t=60)': 'proposed_model_60'
    }
    
    # Store results
    results = {}
    
    for model_name, column in models.items():
        # Get predictions and true labels
        y_true = df['label_encoded']
        y_pred = df[column].astype(int)
        
        # Calculate confusion matrix
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        
        # Calculate metrics
        accuracy = (tp + tn) / (tp + tn + fp + fn)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        results[model_name] = {
            'Confusion Matrix': confusion_matrix(y_true, y_pred),
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1
        }
    
    return results

def get_roc_curve_data(eval_dataset_path: str, model_output_path: str):
    """
    Get ROC curve data using continuous prediction scores.

    Parameters:
    eval_dataset_path (str): Path to the evaluation dataset.
    model_output_path (str): Path to the model output dataset.

    Returns:
    dict: ROC curve data including FPR, TPR, and AUC
    """
    # Merge datasets
    merged_df = merge_evaluation_with_model_output(
        eval_dataset_path=eval_dataset_path,
        model_output_path=model_output_path,
        output_path=None  # Prevent saving during intermediate step
    )
    
    # Get true labels and scores
    y_true = merged_df['label_encoded']
    # Normalize scores to [0,1] range
    y_score = (merged_df['score_by_proposed_model'] / 100)
    
    # Calculate ROC curve and AUC
    fpr, tpr, thresholds = roc_curve(y_true, y_score)
    roc_auc = auc(fpr, tpr)
    
    return {
        'fpr': fpr,
        'tpr': tpr,
        'thresholds': thresholds,
        'auc': roc_auc
    }

def plot_model_performance(results: dict, roc_data: dict, output_path: str | None = None):
    """
    Plot performance metrics and ROC curve following IEEE/ACM publication standards.
    
    Parameters:
    results (dict): Dictionary containing model performance metrics
    roc_data (dict): Dictionary containing ROC curve data
    output_path (str | None): Base path to save the plots. If None, display instead.
    """
    # Set IEEE/ACM compatible settings
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({
        'font.family': 'Times New Roman',
        'font.size': 8,
        'axes.labelsize': 9,
        'axes.titlesize': 9,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8,
        'figure.dpi': 300,
        'lines.linewidth': 1,
        'axes.linewidth': 0.5,
        'grid.linewidth': 0.5
    })

    # Figure 1: Performance Metrics
    fig1, ax1 = plt.subplots(figsize=(3.5, 2.5))  # Column width for IEEE
    
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    model_names = list(results.keys())
    data = [[results[model][metric] for metric in metrics] for model in model_names]
    
    sns.heatmap(data, 
                annot=True, 
                fmt='.3f', 
                xticklabels=metrics, 
                yticklabels=model_names,
                cmap='YlOrRd',
                ax=ax1,
                annot_kws={'size': 7},
                cbar_kws={'shrink': .8})
    ax1.set_title('Performance Metrics')
    ax1.tick_params(axis='both', which='major', labelsize=8)
    
    # Save or display metrics plot
    if output_path:
        fig1.savefig(f"{output_path}_metrics.png", bbox_inches='tight', pad_inches=0.1)
        fig1.savefig(f"{output_path}_metrics.pdf", bbox_inches='tight', pad_inches=0.1)
    else:
        plt.show()
    plt.close(fig1)

    # Figure 2: ROC Curve
    fig2, ax2 = plt.subplots(figsize=(3.5, 2.5))  # Column width for IEEE
    
    ax2.plot(roc_data['fpr'], 
             roc_data['tpr'], 
             color='black',
             lw=1, 
             label=f'ROC (AUC = {roc_data["auc"]:.3f})')
    ax2.plot([0, 1], [0, 1], 
             color='gray', 
             lw=1, 
             linestyle='--',
             label='Random')
    ax2.set_xlim([0.0, 1.0])
    ax2.set_ylim([0.0, 1.05])
    ax2.set_xlabel('False Positive Rate')
    ax2.set_ylabel('True Positive Rate')
    ax2.set_title('Receiver Operating Characteristic')
    ax2.legend(loc="lower right", 
              frameon=True, 
              fancybox=False, 
              edgecolor='black')
    ax2.grid(True, linestyle='--', alpha=0.7)
    
    # Save or display ROC plot
    if output_path:
        fig2.savefig(f"{output_path}_roc.png", bbox_inches='tight', pad_inches=0.1)
        fig2.savefig(f"{output_path}_roc.pdf", bbox_inches='tight', pad_inches=0.1)
    else:
        plt.show()
    plt.close(fig2)

if __name__ == "__main__":
    # Merge evaluation dataset with model output
    merged_data = merge_evaluation_with_model_output(eval_dataset_path='data/processed/evaluation_dataset.csv',
                                                    model_output_path='data/processed/weeg_model_output_on_evaluation_dataset.csv',
                                                    output_path='data/results/evaluation_dataset_with_model_output.csv')
    print(f"Merged dataset shape: {merged_data.shape}")
    print("\nFirst few rows:")
    print(merged_data.head())
    
    # Calculate and display performance metrics
    results = calculate_model_performance()
    
    for model_name, metrics in results.items():
        print(f"\n{model_name}:")
        print("Confusion Matrix:")
        print(metrics['Confusion Matrix'])
        print(f"Accuracy: {metrics['Accuracy']:.3f}")
        print(f"Precision: {metrics['Precision']:.3f}")
        print(f"Recall: {metrics['Recall']:.3f}")
        print(f"F1-Score: {metrics['F1-Score']:.3f}")
    
    # Calculate ROC curve data
    roc_data = get_roc_curve_data(
        eval_dataset_path='data/processed/evaluation_dataset.csv',
        model_output_path='data/processed/weeg_model_output_on_evaluation_dataset.csv'
    )
    
    print(f"\nROC Curve Analysis:")
    print(f"AUC: {roc_data['auc']:.3f}")
    
    # Plot and save the results
    plot_model_performance(
        results=results,
        roc_data=roc_data,
        output_path='docs/figures/model_performance'  # Will create model_performance_metrics.{png,pdf} and model_performance_roc.{png,pdf}
    )
