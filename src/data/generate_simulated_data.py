from typing import Tuple
import numpy as np
import pandas as pd
from scipy.ndimage import gaussian_filter1d

def add_perturbation(flow_rate: np.ndarray | float, time: np.ndarray) -> np.ndarray:
    """
    Add random perturbation to the flow rate with two characteristic frequencies.
    :param flow_rate: Base flow rate (float or numpy array).
    :param time: Array of time values.
    :return: Flow rate array with perturbations.
    """
    long_periodic = 0.03 * flow_rate * np.sin(np.pi * time / 1800)
    short_periodic = 0.002 * flow_rate * np.cos(np.pi * time / 30)
    return flow_rate + long_periodic + short_periodic

def calculate_pulse_counts(flow_rates: np.ndarray, chamber_volume: float, time_interval: int = 1) -> np.ndarray:
    """
    Calculate the pulse counts per minute.
    """
    cumulative_volume = np.cumsum(flow_rates) * time_interval
    pulse_counts = np.zeros_like(flow_rates)

    volume_threshold_accumulated = chamber_volume
    for i in range(len(pulse_counts)):
        while cumulative_volume[i] >= volume_threshold_accumulated:
            pulse_counts[i] += 1
            volume_threshold_accumulated += chamber_volume

    return pulse_counts

def calculate_observed_flow_rate(pulse_counts: np.ndarray, chamber_volume: float, time_interval: int = 1) -> np.ndarray:
    """
    Calculate the observed flow rate based on pulse counts.
    """
    observed_flow_rates = np.zeros_like(pulse_counts, dtype=float)
    for i in range(len(pulse_counts)):
        if pulse_counts[i] > 0:
            observed_flow_rates[i] = (chamber_volume * pulse_counts[i]) / time_interval
    return observed_flow_rates

def calculate_event_flow_rates(time: np.ndarray, duration: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Calculate flow rates for three different events.
    """
    event1_flow_rate = np.full_like(time, 0.05 / 3600, dtype=np.double)

    event2_flow_rate = np.zeros_like(time, dtype=np.double)
    event2_start, event2_end = int(3 * duration / 5), int(4 * duration / 5)
    event2_flow_rate[event2_start:event2_end] = 0.2 / 3600

    event3_flow_rate = np.zeros_like(time, dtype=np.double)
    period_length = duration // 6
    for start in range(duration // 2, duration, period_length):
        end = start + int(0.2 * period_length)
        event3_flow_rate[start:end] = 1.2 / 3600

    return event1_flow_rate, event2_flow_rate, event3_flow_rate

def generate_flow_data(duration: int = 3600, chamber_volume: float = 0.01, superposition: bool = True) -> pd.DataFrame:
    """
    Generate flow data and return as a DataFrame.
    """
    time_seconds = np.arange(0, duration, 1)
    time_minutes = np.arange(0, duration // 60)

    if not superposition:
        flow_rate_base = 1.3
        flow_rates_with_perturbation = add_perturbation(flow_rate_base / 3600, time_seconds)
    else:
        event1_rate, event2_rate, event3_rate = calculate_event_flow_rates(time_seconds, duration)
        combined_flow_rates = event1_rate + event2_rate + event3_rate
        flow_rates_with_perturbation = add_perturbation(combined_flow_rates, time_seconds)

    pulse_counts = calculate_pulse_counts(flow_rates_with_perturbation, chamber_volume, 1)
    pulse_counts_per_minute = np.array([np.sum(pulse_counts[i * 60:(i + 1) * 60]) for i in time_minutes])
    observed_flow_rates = calculate_observed_flow_rate(pulse_counts_per_minute, chamber_volume, 1)
    smoothed_flow_rates = gaussian_filter1d(observed_flow_rates, sigma=2)

    # Create DataFrame
    df = pd.DataFrame({
        'time_seconds': time_seconds,
        'time_minutes': np.repeat(time_minutes + 1, 60),
        'actual_flow_rate': flow_rates_with_perturbation * 3600,  # Convert to m³/hour
        'pulse_counts': pulse_counts,
        'pulse_counts_per_minute': np.repeat(pulse_counts_per_minute, 60),
        'observed_flow_rate': np.repeat(observed_flow_rates.astype(np.float64) * 60, 60),  # Convert to m³/hour
        'smoothed_flow_rate': np.repeat(smoothed_flow_rates.astype(np.float64) * 60, 60)  # Convert to m³/hour
    })

    if superposition:
        df['event1_rate'] = event1_rate * 3600
        df['event2_rate'] = event2_rate * 3600
        df['event3_rate'] = event3_rate * 3600

    return df

if __name__ == "__main__":
    # Generate data
    df = generate_flow_data()
    
    # Save to CSV
    df.to_csv('data/processed/simulated_flow_data.csv', index=False)
    print("Data generated and saved successfully!") 