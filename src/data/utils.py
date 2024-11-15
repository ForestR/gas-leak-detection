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