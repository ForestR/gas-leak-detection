from pickle import TRUE
import pandas as pd
from datetime import datetime
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

def merge_evaluation_with_model_output(eval_dataset_path: str, model_output_path: str, output_path: str):
    """
    Merge evaluation dataset with model output based on device ID and date.
    
    Parameters:
    eval_dataset_path (str): The file path of the evaluation dataset.
    model_output_path (str): The file path of the model output.
    output_path (str): The file path to save the merged dataset.
    """
    
    # Load evaluation dataset
    eval_df = pd.read_csv(eval_dataset_path, 
                         usecols=['device_id_encoded', 'date_report', 'label'])
    
    # Load model output dataset
    model_df = pd.read_csv(model_output_path,
                          usecols=['device_id', 'date', 'score_likelihood', 'pulse_hourly'])
    print(model_df.head())  
    model_df['score_likelihood'] = pd.to_numeric(model_df['score_likelihood'], errors='coerce')
    
    # Create merge keys
    eval_df['merge_key'] = eval_df.apply(
        lambda x: f"{x['device_id_encoded']}_{datetime.strptime(x['date_report'], '%Y/%m/%d').strftime('%Y-%m-%d')}", 
        axis=1
    )
    
    model_df['merge_key'] = model_df.apply(
        lambda x: f"{x['device_id']}_{x['date']}", 
        axis=1
    )
    
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
    
    # save to csv
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

    
