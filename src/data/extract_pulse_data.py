import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
from utils import EncodingDictManager

def load_device_dates(eval_file: str) -> Dict[str, List[str]]:
    """Load device IDs and their corresponding report dates from evaluation dataset.
    
    Args:
        eval_file (str): Path to evaluation dataset CSV file
        
    Returns:
        Dict[str, List[str]]: Dictionary mapping encoded device IDs to lists of report dates
    """
    df = pd.read_csv(eval_file)
    
    # Load encoding dictionary
    encoding_file = Path('data/interim/encoding_dicts.json')
    with open(encoding_file, 'r', encoding='utf-8') as f:
        encoding_dict = json.load(f)
    
    # Create reverse mapping (encoded -> original device_id)
    device_mapping = {v: k for k, v in encoding_dict['device_id'].items()}
    
    # Group dates by device ID
    device_dates = {}
    for _, row in df.iterrows():
        device_id = device_mapping[row['device_id_encoded']]
        date = datetime.strptime(row['date_report'], '%Y/%m/%d')
        date_str = date.strftime('%y%m%d')  # Convert to format matching pulseDate
        
        if device_id not in device_dates:
            device_dates[device_id] = []
        if date_str not in device_dates[device_id]:
            device_dates[device_id].append(date_str)
    
    return device_dates

def extract_pulse_data(raw_file: str, device_dates: Dict[str, List[str]], output_file: str, test: bool = False):
    """Extract pulse data for specified devices and dates.
    
    Args:
        raw_file (str): Path to raw data CSV file
        device_dates (Dict[str, List[str]]): Dictionary of device IDs and their dates
        output_file (str): Path to output file
    """
    # Read raw data file in chunks
    chunk_size = 10000
    column_map = {'表号': 'device_id', '数据': 'data'}
    # Force 'data' column to be read as string
    dtype_map = {'表号': str, '数据': str}
    chunks = pd.read_csv(raw_file, chunksize=chunk_size, usecols=column_map.keys(), 
                        dtype=dtype_map, encoding='gbk')
    extracted_records = []
    
    for chunk in chunks:
        # Rename columns for this chunk
        chunk = chunk.rename(columns=column_map)

        if test:
            # Add debug print
            print(f"Chunk columns: {chunk.columns}")
            print(f"First few rows of chunk:\n{chunk.head()}")
        
        # Filter devices
        chunk = chunk[chunk['device_id'].isin(device_dates.keys())]

        # Add debug print
        if test:    
            print(f"Matching devices in chunk: {len(chunk)}")
        
        for _, row in chunk.iterrows():
            device_id = row['device_id']
            try:
                # Convert NaN or float to empty JSON string if necessary
                data_str = row['data']
                if pd.isna(data_str):
                    data_str = '{}'
                
                data = json.loads(str(data_str))
                pulse_date = data.get('pulseDate')

                if test:    
                    # Add debug print
                    print(f"Device ID: {device_id}")
                    print(f"Pulse date: {pulse_date}")
                
                # Check if this date is needed for this device
                if pulse_date and pulse_date in device_dates[device_id]:
                    extracted_records.append({
                        'device_id': device_id,
                        'date': pulse_date,
                        'data': data_str
                    })
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Error parsing JSON for device {device_id}: {e}")
                continue
    
    # Initialize encoding manager
    encoding_manager = EncodingDictManager()
    
    # Save extracted records
    output_df = pd.DataFrame(extracted_records)
    
    # Add safety check for empty DataFrame
    if len(output_df) == 0:
        print("\nWarning: No records were extracted!")
        return
    
    # Encode device IDs before saving
    output_df['device_id_encoded'] = output_df['device_id'].apply(
        lambda x: encoding_manager.get_or_create_encoding('device_id', x)
    )
    # Drop the original device_id column
    output_df = output_df.drop(columns=['device_id'])

    # Reorder columns
    output_df = output_df[['device_id_encoded', 'date', 'data']]
    
    # Save to CSV
    output_df.to_csv(output_file, index=False)
    
    print(f"\nExtraction Statistics:")
    print(f"Total devices processed: {len(device_dates)}")
    print(f"Records extracted: {len(output_df)}")
    print(f"Unique devices found: {output_df['device_id_encoded'].nunique()}")
    print(f"Unique dates found: {output_df['date'].nunique()}")

def main(test: bool = False):
    """Process pulse data from raw CSV files.
    
    Args:
        test (bool, optional): If True, only process a single test file. Defaults to False.
    """
    # Define file paths using pathlib
    data_dir = Path("data")
    eval_file = data_dir / "processed" / "evaluation_dataset.csv"
    raw_dir = data_dir / "raw"
    interim_dir = data_dir / "interim"
    
    # Validate directory structure
    if not raw_dir.exists():
        raise FileNotFoundError(f"Raw data directory not found: {raw_dir}")
    if not eval_file.exists():
        raise FileNotFoundError(f"Evaluation dataset not found: {eval_file}")
    
    # Ensure interim directory exists
    interim_dir.mkdir(parents=True, exist_ok=True)
    
    # Load device IDs and dates from evaluation dataset
    try:
        device_dates = load_device_dates(str(eval_file))
        print(f"Loaded device dates for {len(device_dates)} devices")
    except Exception as e:
        print(f"Error loading device dates: {str(e)}")
        return
    
    # Get list of raw files to process
    if test:
        test_file = raw_dir / "202401_01-09.csv"
        if not test_file.exists():
            raise FileNotFoundError(f"Test file not found: {test_file}")
        raw_files = [test_file]
    else:
        raw_files = list(raw_dir.glob("2024*_*.csv"))
        raw_files.sort()  # Ensure consistent processing order
    
    if not raw_files:
        print("No matching CSV files found to process")
        return
    
    print(f"Found {len(raw_files)} files to process:")
    for file in raw_files:
        print(f"  - {file.name}")
    
    # Process each file
    successful = 0
    failed = 0
    
    for raw_file in raw_files:
        print(f"\nProcessing {raw_file.name}...")
        output_file = interim_dir / f"pulse_data_{raw_file.stem}.csv"
        
        try:
            extract_pulse_data(str(raw_file), device_dates, str(output_file), test)
            print(f"✓ Successfully processed {raw_file.name}")
            successful += 1
        except Exception as e:
            print(f"✗ Error processing {raw_file.name}: {str(e)}")
            failed += 1
            continue
    
    # Print summary
    print("\nProcessing Summary:")
    print(f"Total files: {len(raw_files)}")
    print(f"Successful: {successful}")
    print(f"Failed: {failed}")

    # Combine all processed files
    processed_files = list(interim_dir.glob('pulse_data_*.csv'))
    dfs = []
    for file in processed_files:
        df = pd.read_csv(file)
        dfs.append(df)  
    combined_df = pd.concat(dfs, ignore_index=True)
    print(f"Total records: {len(combined_df)}")
    print(f"Unique devices: {combined_df['device_id_encoded'].nunique()}")
    print(f"Date range: {combined_df['date'].min()} to {combined_df['date'].max()}")  
    
    # Save combined file
    combined_file = data_dir / "processed" / "pulse_data_for_evaluation.csv"
    combined_df.to_csv(combined_file, index=False)  


if __name__ == "__main__":
    main(test=False) 
