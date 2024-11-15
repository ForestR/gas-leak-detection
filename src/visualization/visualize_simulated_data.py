import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator, MultipleLocator

def setup_plotting_style():
    """Set up the plotting style for publication-quality figures."""
    # Use IEEE style settings
    plt.style.use('seaborn-v0_8-paper')
    sns.set_context("paper", font_scale=1.2)
    
    # Set general plotting parameters for publication
    plt.rcParams.update({
        # Resolution settings
        'figure.dpi': 300,
        'savefig.dpi': 300,
        
        # Font settings
        'font.family': 'serif',  # IEEE standard font
        'font.serif': ['Times New Roman'],  # IEEE preferred font
        'font.size': 10,  # Base font size
        'axes.titlesize': 10,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8,
        'legend.title_fontsize': 9,
        
        # Figure size (IEEE column width)
        'figure.figsize': (3.5, 2.5),  # IEEE single column width
        # 'figure.figsize': (7.16, 5),  # IEEE double column width
        
        # Line settings
        'lines.linewidth': 1,
        'lines.markersize': 4,
        
        # Grid settings
        'grid.linewidth': 0.5,
        'grid.alpha': 0.3,
        
        # Legend settings
        'legend.frameon': True,
        'legend.framealpha': 0.8,
        'legend.edgecolor': '0.8',
        
        # Margin settings
        'figure.constrained_layout.use': True,
        'figure.constrained_layout.h_pad': 0.1,
        'figure.constrained_layout.w_pad': 0.1,
    })

def plot_pulse_counts(df: pd.DataFrame):
    """Plot pulse counts per minute."""
    fig, ax = plt.subplots()
    
    # Create the bar plot
    unique_minutes = df['time_minutes'].unique()
    pulse_counts = df.groupby('time_minutes')['pulse_counts'].sum().values
    
    ax.bar(unique_minutes, pulse_counts, 
           color=sns.color_palette("husl")[0],
           alpha=0.7, width=0.8)
    
    # Customize the plot
    ax.set_xlabel('Time (min)')
    ax.set_ylabel('Pulse Count')
    ax.set_title('Gas Flow Meter Pulse Counts')
    
    # Adjust axes
    ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))
    ax.xaxis.set_major_locator(MultipleLocator(10))  # Major ticks every 10 minutes
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Add grid only for y-axis
    ax.grid(True, axis='y', linestyle='--', alpha=0.3)
    
    # Save the figure
    plt.savefig('docs/figures/pulse_counts.pdf', 
                bbox_inches='tight', 
                pad_inches=0.1)
    plt.close()

def plot_flow_rates_by_event(df: pd.DataFrame):
    """Plot flow rates by event source."""
    fig, ax = plt.subplots()
    
    # Plot combined flow rate
    ax.plot(df['time_seconds']/60, df['actual_flow_rate'],
            color=sns.color_palette("husl")[2],
            label='Combined',
            linewidth=1.2)
    
    # Plot individual event rates if available
    if 'event1_rate' in df.columns:
        ax.plot(df['time_seconds']/60, df['event1_rate'],
                linestyle='--', color=sns.color_palette("husl")[0],
                label='Micro-leak',
                linewidth=1)
        ax.plot(df['time_seconds']/60, df['event2_rate'],
                linestyle='--', color=sns.color_palette("husl")[1],
                label='Gas Stove',
                linewidth=1)
        ax.plot(df['time_seconds']/60, df['event3_rate'],
                linestyle='--', color=sns.color_palette("husl")[3],
                label='Water Heater',
                linewidth=1)
    
    # Customize the plot
    ax.set_xlabel('Time (min)')
    ax.set_ylabel('Flow Rate (m³/h)')
    ax.set_title('Gas Flow Rate Components')
    
    # Enhance legend
    ax.legend(ncol=1, loc='upper left', 
             bbox_to_anchor=(0.05, 1),
             borderaxespad=0.1,
             columnspacing=0.8)
    
    # Adjust axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # Save the figure
    plt.savefig('docs/figures/flow_rates_by_event.pdf',
                bbox_inches='tight',
                pad_inches=0.1)
    plt.close()

def plot_flow_rates_comparison(df: pd.DataFrame):
    """Plot comparison of actual, observed, and smoothed flow rates."""
    fig, ax = plt.subplots()
    
    # Plot the three flow rates
    ax.plot(df['time_seconds'] / 60, df['actual_flow_rate'],
            color=sns.color_palette("husl")[2],
            label='Actual',
            linewidth=1.2)
    ax.step(df['time_minutes'], df['observed_flow_rate'],
            where='mid', color=sns.color_palette("husl")[0],
            label='Observed',
            linewidth=1)
    ax.step(df['time_minutes'], df['smoothed_flow_rate'],
            where='mid', color=sns.color_palette("husl")[1],
            linestyle='--',
            label='Smoothed',
            linewidth=1)
    
    # Customize the plot
    ax.set_xlabel('Time (min)')
    ax.set_ylabel('Flow Rate (m³/h)')
    ax.set_title('Flow Rate Measurements Comparison')
    
    # Enhance legend
    ax.legend(ncol=1, loc='upper left',
             bbox_to_anchor=(0.05, 1),
             borderaxespad=0.1,
             columnspacing=0.8)
    
    # Set y-axis limits
    ax.set_ylim(0, df['observed_flow_rate'].max() * 1.1)
    
    # Adjust axes
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.3)
    
    # Save the figure
    plt.savefig('docs/figures/flow_rates_comparison.pdf',
                bbox_inches='tight',
                pad_inches=0.1)
    plt.close()

def generate_all_plots():
    """Generate all plots from the simulated data."""
    try:
        # Set up plotting style
        setup_plotting_style()
        
        # Read the data
        df = pd.read_csv('data/processed/simulated_flow_data.csv')
        
        # Generate all plots
        print("Generating plots...")
        plot_pulse_counts(df)
        plot_flow_rates_by_event(df)
        plot_flow_rates_comparison(df)
        print("All plots generated successfully!")
        
    except FileNotFoundError:
        print("Error: Simulated data file not found. Please run generate_data.py first.")
    except Exception as e:
        print(f"Error generating plots: {str(e)}")

if __name__ == "__main__":
    generate_all_plots() 