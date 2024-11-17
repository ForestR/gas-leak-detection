import pandas as pd
import numpy as np
from typing import Dict, List
from pathlib import Path
from utils import map_label, EncodingDictManager

def load_tp_data(file_path: str) -> pd.DataFrame:
    """Load true positive (TP) report data."""
    # Read TP data with specified columns
    df_tp = pd.read_csv(file_path, encoding='gbk', dtype={'device_id': str})
    
    # Select and rename columns
    df_tp = df_tp[['device_id', 'type', 'annotation', 'date_report', 'label']]
    
    # Add missing columns
    df_tp['usage'] = 'MISSING'  # TP reports don't have usage information
    df_tp['date_inspect'] = df_tp['date_report']  # Use report date as inspect date
    
    return df_tp

def load_fp_data(file_path: str) -> pd.DataFrame:
    """Load false positive (FP) report data."""
    # Read FP data with specified columns
    df_fp = pd.read_csv(file_path, encoding='gbk', dtype={'device_id': str})
    
    # Select required columns
    df_fp = df_fp[['device_id', 'usage', 'type', 'annotation', 
                   'date_report', 'date_inspect', 'label']]
    
    return df_fp

def process_reports(tp_path: str, fp_path: str, output_path: str):
    """Process and merge TP and FP reports."""
    try:
        # Load data
        df_tp = load_tp_data(tp_path)
        df_fp = load_fp_data(fp_path)
        
        # Merge dataframes
        df = pd.concat([df_tp, df_fp], ignore_index=True)
        
        # Initialize encoding manager
        encoder = EncodingDictManager()
        
        # Encode columns
        for col in ['device_id', 'usage', 'type', 'annotation']:
            df[f'{col}_encoded'] = df[col].apply(lambda x: encoder.get_or_create_encoding(col, x))
        
        # Convert dates to standard format
        df['date_report'] = pd.to_datetime(df['date_report']).dt.strftime('%Y/%m/%d')
        df['date_inspect'] = pd.to_datetime(df['date_inspect']).dt.strftime('%Y/%m/%d')
        
        # Map labels before final column selection
        df['label'] = df['label'].apply(map_label)
        
        # Select and reorder columns
        output_df = df[[
            'device_id_encoded',
            'usage_encoded',
            'type_encoded',
            'annotation_encoded',
            'date_report',
            'date_inspect',
            'label'
        ]]

        # Sort by "date_report"
        output_df = output_df.sort_values(by='date_report', ascending=True)
        
        # Save processed data
        output_df.to_csv(output_path, index=False)
        
        # Print statistics
        print("\nProcessing Statistics:")
        print(f"Total records: {len(df)}")
        print(f"TP records: {len(df_tp)}")
        print(f"FP records: {len(df_fp)}")
        
        print("\nEncoding Statistics:")
        for col in ['device_id', 'usage', 'type', 'annotation']:
            unique_count = len([k for k, v in encoder.get_encoding_dict(col).items() 
                              if v != 'MISSING' and k is not np.nan])
            print(f"Unique {col}: {unique_count}")
        
        print("\nMissing Value Statistics:")
        for col in ['usage_encoded', 'type_encoded', 'annotation_encoded']:
            missing_count = (output_df[col] == 'MISSING').sum()
            print(f"Missing {col}: {missing_count}")
        
    except Exception as e:
        print(f"Error processing files: {str(e)}")
        raise

if __name__ == "__main__":
    # Define file paths
    data_dir = Path("data")
    tp_file = data_dir / "raw" / "report_202401-202404_TP.csv"
    fp_file = data_dir / "raw" / "report_202401-202404_FP.csv"
    output_file = data_dir / "processed" / "evaluation_dataset.csv"
    
    # Process reports
    process_reports(str(tp_file), str(fp_file), str(output_file))
    print(f"\nProcessed data saved to {output_file}") 
    