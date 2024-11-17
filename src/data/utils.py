import json
import pandas as pd
from pathlib import Path
from typing import Dict, Optional

class EncodingDictManager:
    """Manages shared encoding dictionaries across different scripts."""
    
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = Path(file_path) if file_path else Path('data/interim/encoding_dicts.json')
        self.encoding_dicts = self._load_dicts()
    
    def _load_dicts(self) -> Dict[str, Dict[str, str]]:
        """Load existing encoding dictionaries or create new ones."""
        if self.file_path.exists():
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        return {
            'device_id': {},
            'community': {},
            'usage': {},
            'type': {},
            'annotation': {}
        }
    
    def save_dicts(self):
        """Save encoding dictionaries to file."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.encoding_dicts, f, ensure_ascii=False, indent=2)
    
    def get_or_create_encoding(self, category: str, value: str) -> str:
        """Get existing encoding or create new one for a value.
        
        Args:
            category (str): Category of the encoding (e.g., 'device_id', 'annotation')
            value (str): Value to be encoded
            
        Returns:
            str: Encoded value or 'MISSING' for empty/NaN values
        """
        # Handle NaN, None, and empty values
        if pd.isna(value) or value == '' or value is None:
            return 'MISSING'
        
        # Convert value to string for consistency
        value = str(value).strip()
        
        # Create new encoding if value doesn't exist
        if value not in self.encoding_dicts[category]:
            existing_codes = set(self.encoding_dicts[category].values())
            new_code = f"{category[0].upper()}{len(self.encoding_dicts[category]) + 1:03d}"
            
            while new_code in existing_codes:
                new_code = f"{category[0].upper()}{int(new_code[1:]) + 1:03d}"
            
            self.encoding_dicts[category][value] = new_code
            self.save_dicts()
        
        return self.encoding_dicts[category][value]
    
    def get_encoding_dict(self, category: str) -> Dict[str, str]:
        """Get the encoding dictionary for a specific category."""
        return self.encoding_dicts.get(category, {})

def map_label(label: str) -> str:
    """Map Chinese labels to standardized English labels.
    
    Args:
        label (str): Chinese label to be mapped
        
    Returns:
        str: Standardized English label
    """
    label_mapping = {
        '正': 'NORMAL',      # Healthy state
        '漏': 'LEAKAGE',     # Leakage detected
        '未': 'UNCERTAIN'    # Inconclusive inspection
    }
    return label_mapping.get(label, 'UNKNOWN') 
