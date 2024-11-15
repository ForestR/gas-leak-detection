import pandas as pd
import re
from typing import List, Dict

class AddressEncoder:
    def __init__(self):
        # Define mapping dictionaries for common components
        self.building_types = {
            '期': 'phase_',
            '栋': 'building_',
            '楼': 'building_',
            '号楼': 'building_',
            '单元': 'unit_',
            '层': 'floor_',
            '室': 'room_'
        }
        
        # Special location markers
        self.location_markers = {
            '小区': 'community',
            '社区': 'community',
            '家园': 'garden',
            '广场': 'plaza',
            '公寓': 'apartment',
            '花园': 'garden',
            '城': 'city',
            '区': 'district'
        }

    def extract_numbers(self, text: str) -> List[str]:
        """Extract numbers from text, including those with Chinese characters."""
        numbers = re.findall(r'\d+', text)
        return numbers

    def encode_address(self, address: str) -> Dict[str, str]:
        """
        Encode a Chinese address into structured components.
        Returns a dictionary with encoded components.
        """
        result = {
            'community_name': '',
            'phase': '',
            'building': '',
            'unit': '',
            'floor': '',
            'room': '',
            'original': address
        }
        
        # Extract community name (everything before the first number)
        community_pattern = r'^[^\d]+'
        community_match = re.search(community_pattern, address)
        if community_match:
            result['community_name'] = community_match.group().strip()
        
        # Extract numbers for different components
        for key, marker in self.building_types.items():
            pattern = f'(\d+){key}'
            match = re.search(pattern, address)
            if match:
                component_name = marker.rstrip('_')
                result[component_name] = match.group(1)
        
        return result

    def encode_to_string(self, address: str) -> str:
        """
        Convert encoded address components to a standardized string format.
        """
        components = self.encode_address(address)
        encoded_parts = []
        
        if components['community_name']:
            encoded_parts.append(f"COM_{components['community_name']}")
        if components['phase']:
            encoded_parts.append(f"PH_{components['phase']}")
        if components['building']:
            encoded_parts.append(f"BLD_{components['building']}")
        if components['unit']:
            encoded_parts.append(f"UN_{components['unit']}")
        if components['floor']:
            encoded_parts.append(f"FL_{components['floor']}")
        if components['room']:
            encoded_parts.append(f"RM_{components['room']}")
            
        return '_'.join(encoded_parts)

def process_csv(input_path: str, output_path: str):
    """
    Process the CSV file and add encoded addresses.
    """
    # Read the CSV file
    df = pd.read_csv(input_path)
    
    # Initialize encoder
    encoder = AddressEncoder()
    
    # Add encoded addresses
    df['address_encoded'] = df['address'].apply(encoder.encode_to_string)
    
    # Add structured address components
    encoded_components = df['address'].apply(encoder.encode_address)
    df['community_name'] = encoded_components.apply(lambda x: x['community_name'])
    df['building_number'] = encoded_components.apply(lambda x: x['building'])
    df['unit_number'] = encoded_components.apply(lambda x: x['unit'])
    df['floor_number'] = encoded_components.apply(lambda x: x['floor'])
    df['room_number'] = encoded_components.apply(lambda x: x['room'])
    
    # Save the processed data
    df.to_csv(output_path, index=False)
    
    # Print some statistics
    print(f"Total addresses processed: {len(df)}")
    print(f"Unique communities: {df['community_name'].nunique()}")
    print(f"Unique buildings: {df['building_number'].nunique()}")
    print("\nSample encodings:")
    for _, row in df.head().iterrows():
        print(f"Original: {row['address']}")
        print(f"Encoded: {row['address_encoded']}\n")

if __name__ == "__main__":
    input_file = 'data/raw/report_202406-202407.csv'
    output_file = 'data/processed/report_encoded.csv'
    
    try:
        process_csv(input_file, output_file)
        print(f"\nProcessed data saved to {output_file}")
    except Exception as e:
        print(f"Error processing file: {str(e)}") 