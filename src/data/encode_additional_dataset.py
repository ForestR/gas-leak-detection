import pandas as pd
import numpy as np
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from utils import map_label, EncodingDictManager

class DataEncoder:
    def __init__(self):
        self.encoding_manager = EncodingDictManager()
        self.building_types = {
            '期': 'phase_',
            '栋': 'building_',
            '楼': 'building_',
            '号楼': 'building_',
            '单元': 'unit_',
            '层': 'floor_',
            '室': 'room_'
        }
        
    def _get_or_create_encoding(self, category: str, value: str) -> str:
        """Get existing encoding or create new one for a value."""
        if pd.isna(value) or value == '':
            return 'MISSING'
            
        if value not in self.encoding_manager.get_encoding_dict(category):
            existing_codes = set(self.encoding_manager.get_encoding_dict(category).values())
            new_code = f"{category[0].upper()}{len(self.encoding_manager.get_encoding_dict(category)) + 1:03d}"
            
            while new_code in existing_codes:
                new_code = f"{category[0].upper()}{int(new_code[1:]) + 1:03d}"
                
            self.encoding_manager.get_encoding_dict(category)[value] = new_code
            self.encoding_manager.save_dicts()
            
        return self.encoding_manager.get_encoding_dict(category)[value]

    def encode_address(self, address: str) -> Dict[str, str]:
        """Encode a Chinese address into structured components."""
        if pd.isna(address):
            return {
                'community_name': 'MISSING',
                'phase': 'MISSING',
                'building': 'MISSING',
                'unit': 'MISSING',
                'floor': 'MISSING',
                'room': 'MISSING',
                'original': ''
            }
            
        result = {
            'community_name': 'MISSING',
            'phase': 'MISSING',
            'building': 'MISSING',
            'unit': 'MISSING',
            'floor': 'MISSING',
            'room': 'MISSING',
            'original': address
        }
        
        try:
            # Extract community name
            community_pattern = r'^[^\d]+'
            community_match = re.search(community_pattern, address)
            if community_match:
                community_name = community_match.group().strip()
                result['community_name'] = self._get_or_create_encoding('community', community_name)
            
            # Extract numbers for different components
            for key, marker in self.building_types.items():
                pattern = fr'(\d+){key}'
                match = re.search(pattern, address)
                if match:
                    component_name = marker.rstrip('_')
                    result[component_name] = match.group(1)
        except Exception as e:
            print(f"Error processing address: {address}")
            print(f"Error details: {str(e)}")
            
        return result

    def encode_to_string(self, address: str) -> str:
        """Convert encoded address components to a standardized string format."""
        try:
            components = self.encode_address(address)
            encoded_parts = []
            
            if components['community_name'] != 'MISSING':
                encoded_parts.append(f"COM_{components['community_name']}")
            if components['phase'] != 'MISSING':
                encoded_parts.append(f"PH_{components['phase']}")
            if components['building'] != 'MISSING':
                encoded_parts.append(f"BLD_{components['building']}")
            if components['unit'] != 'MISSING':
                encoded_parts.append(f"UN_{components['unit']}")
            if components['floor'] != 'MISSING':
                encoded_parts.append(f"FL_{components['floor']}")
            if components['room'] != 'MISSING':
                encoded_parts.append(f"RM_{components['room']}")
                
            return '_'.join(encoded_parts) if encoded_parts else 'INVALID_ADDRESS'
        except Exception as e:
            print(f"Error encoding address: {address}")
            print(f"Error details: {str(e)}")
            return 'INVALID_ADDRESS'

    def encode_metadata(self, row: pd.Series) -> Dict[str, str]:
        """Encode device_id, usage, type, and annotation fields."""
        try:
            return {
                'device_id_encoded': self._get_or_create_encoding('device_id', row['device_id']),
                'usage_encoded': self._get_or_create_encoding('usage', row['usage']),
                'type_encoded': self._get_or_create_encoding('type', row['type']),
                'annotation_encoded': self._get_or_create_encoding('annotation', row['annotation'])
            }
        except Exception as e:
            print(f"Error encoding metadata for row: {row}")
            print(f"Error details: {str(e)}")
            return {
                'device_id_encoded': 'ERROR',
                'usage_encoded': 'ERROR',
                'type_encoded': 'ERROR',
                'annotation_encoded': 'ERROR'
            }

def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate and clean the input data."""
    # Remove rows with missing device_id
    df = df.dropna(subset=['device_id'])
    
    # Convert device_id to string
    df['device_id'] = df['device_id'].astype(str)
    
    # Fill missing values
    df['address'] = df['address'].fillna('')
    df['usage'] = df['usage'].fillna('')
    df['type'] = df['type'].fillna('')
    df['annotation'] = df['annotation'].fillna('')
    
    # Standardize date formats with year 2024
    df['date_report'] = pd.to_datetime(df['date_report'].apply(lambda x: f"{x}/2024"), format='%m/%d/%Y', errors='coerce')
    df['date_inspect'] = pd.to_datetime(df['date_inspect'].apply(lambda x: f"{x}/2024"), format='%m/%d/%Y', errors='coerce')
    
    # Convert labels to English
    df['label'] = df['label'].apply(map_label)
    
    return df

def process_csv(input_path: str, output_path: str):
    """Process the CSV file and add encoded fields."""
    try:
        # Read and validate the CSV file
        df = pd.read_csv(input_path, encoding='gbk', dtype={'device_id': str})  # Specify encoding and dtype
        df = validate_data(df)
        
        # Initialize encoder
        encoder = DataEncoder()
        
        # Add encoded fields
        df['address_encoded'] = df['address'].apply(encoder.encode_to_string)
        encoded_metadata = df.apply(encoder.encode_metadata, axis=1)
        
        # Create output DataFrame with selected columns
        output_df = pd.DataFrame({
            'device_id_encoded': encoded_metadata.apply(lambda x: x['device_id_encoded']),
            'address_encoded': df['address_encoded'],
            'usage_encoded': encoded_metadata.apply(lambda x: x['usage_encoded']),
            'type_encoded': encoded_metadata.apply(lambda x: x['type_encoded']),
            'annotation_encoded': encoded_metadata.apply(lambda x: x['annotation_encoded']),
            'date_report': df['date_report'].dt.strftime('%Y/%m/%d'),
            'date_inspect': df['date_inspect'].dt.strftime('%Y/%m/%d'),
            'label': df['label']
        })

        # Sort by date_report
        output_df = output_df.sort_values(by='date_report', ascending=True)
        
        # Save the processed data
        output_df.to_csv(output_path, index=False)
        
        # Print statistics
        print("\nEncoding Statistics:")
        print(f"Total records processed: {len(df)}")
        print(f"Valid records: {len(output_df)}")
        print(f"Unique devices: {len(encoder.encoding_manager.get_encoding_dict('device_id'))}")
        print(f"Unique communities: {len(encoder.encoding_manager.get_encoding_dict('community'))}")
        print(f"Unique usage types: {len(encoder.encoding_manager.get_encoding_dict('usage'))}")
        print(f"Unique event types: {len(encoder.encoding_manager.get_encoding_dict('type'))}")
        print(f"Unique annotations: {len(encoder.encoding_manager.get_encoding_dict('annotation'))}")
        
        # Print data quality report
        print("\nData Quality Report:")
        print(f"Missing addresses: {df['address'].isna().sum()}")
        print(f"Invalid addresses: {(output_df['address_encoded'] == 'INVALID_ADDRESS').sum()}")
        print(f"Missing metadata: {(output_df[['usage_encoded', 'type_encoded', 'annotation_encoded']] == 'MISSING').sum()}")
        print(f"Invalid dates: {df['date_report'].isna().sum() + df['date_inspect'].isna().sum()}")
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise

if __name__ == "__main__":
    # Define file paths
    data_dir = Path("data")
    input_file = data_dir / "raw" / "report_202406-202407.csv"
    output_file = data_dir / "processed" / "additional_dataset.csv"
    
    # Process CSV
    process_csv(str(input_file), str(output_file))
    print(f"\nProcessed data saved to {output_file}")
    