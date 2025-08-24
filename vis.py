import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import os
warnings.filterwarnings('ignore')

# Create the plots folder if it doesn't exist
if not os.path.exists('plots'):
    os.makedirs('plots')

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

def create_individual_visualizations(blore_df, delhi_df):
    """
    Create comprehensive visualizations and save each plot individually
    """
    
    # 1. Flight Volume Comparison
    plt.figure(figsize=(10, 6))
    airports = ['Bangalore', 'Delhi']
    flight_counts = [len(blore_df), len(delhi_df)]
    colors = ['#FF6B6B', '#4ECDC4']
    
    bars = plt.bar(airports, flight_counts, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
    plt.title('Total Flight Volume Comparison', fontsize=14, fontweight='bold')
    plt.ylabel('Number of Flights')
    
    # Add value labels on bars
    for bar, count in zip(bars, flight_counts):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                f'{count:,}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('plots/01_flight_volume_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Flight Type Distribution - Bangalore
    plt.figure(figsize=(8, 6))
    blore_flight_types = blore_df['Flight Type'].value_counts()
    plt.pie(blore_flight_types.values, labels=blore_flight_types.index, autopct='%1.1f%%', 
            colors=['#FF9999', '#66B2FF'], startangle=90)
    plt.title('Bangalore: Flight Type Distribution', fontsize=12, fontweight='bold')
    plt.savefig('plots/02_bangalore_flight_type_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Flight Type Distribution - Delhi
    plt.figure(figsize=(8, 6))
    delhi_flight_types = delhi_df['Flight Type'].value_counts()
    plt.pie(delhi_flight_types.values, labels=delhi_flight_types.index, autopct='%1.1f%%', 
            colors=['#FFB366', '#66FFB2'], startangle=90)
    plt.title('Delhi: Flight Type Distribution', fontsize=12, fontweight='bold')
    plt.savefig('plots/03_delhi_flight_type_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Delay Distribution Comparison
    plt.figure(figsize=(12, 6))
    
    # Combine all delays for both airports
    blore_all_delays = pd.concat([
        blore_df['Departure Delay (min)'].dropna(),
        blore_df['Arrival Delay (min)'].dropna()
    ])
    
    delhi_all_delays = pd.concat([
        delhi_df['Departure Delay (min)'].dropna(),
        delhi_df['Arrival Delay (min)'].dropna()
    ])
    
    # Filter extreme outliers for better visualization
    blore_delays_filtered = blore_all_delays[(blore_all_delays >= -60) & (blore_all_delays <= 180)]
    delhi_delays_filtered = delhi_all_delays[(delhi_all_delays >= -60) & (delhi_all_delays <= 180)]
    
    plt.hist(blore_delays_filtered, bins=30, alpha=0.7, label='Bangalore', color='#FF6B6B', density=True)
    plt.hist(delhi_delays_filtered, bins=30, alpha=0.7, label='Delhi', color='#4ECDC4', density=True)
    plt.xlabel('Delay (minutes)')
    plt.ylabel('Density')
    plt.title('Delay Distribution Comparison', fontsize=12, fontweight='bold')
    plt.legend()
    plt.axvline(x=0, color='black', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('plots/04_delay_distribution_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Top Airlines by Flight Count - Bangalore
    plt.figure(figsize=(10, 8))
    top_airlines_blore = blore_df['Carrier'].value_counts().head(8)
    plt.barh(range(len(top_airlines_blore)), top_airlines_blore.values, color='#FF6B6B', alpha=0.8)
    plt.yticks(range(len(top_airlines_blore)), top_airlines_blore.index)
    plt.xlabel('Number of Flights')
    plt.title('Bangalore: Top Airlines', fontsize=12, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('plots/05_bangalore_top_airlines.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6. Top Airlines by Flight Count - Delhi
    plt.figure(figsize=(10, 8))
    top_airlines_delhi = delhi_df['Carrier'].value_counts().head(8)
    plt.barh(range(len(top_airlines_delhi)), top_airlines_delhi.values, color='#4ECDC4', alpha=0.8)
    plt.yticks(range(len(top_airlines_delhi)), top_airlines_delhi.index)
    plt.xlabel('Number of Flights')
    plt.title('Delhi: Top Airlines', fontsize=12, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('plots/06_delhi_top_airlines.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 7. Hourly Traffic Pattern - Combined
    plt.figure(figsize=(14, 6))
    
    def extract_hour_safe(time_str):
        if pd.isna(time_str):
            return None
        try:
            return pd.to_datetime(time_str).hour
        except:
            return None
    
    # Extract hours for all flights
    blore_hours = []
    delhi_hours = []
    
    for df, hours_list in [(blore_df, blore_hours), (delhi_df, delhi_hours)]:
        for col in ['Scheduled Departure (Local)', 'Scheduled Arrival (Local)']:
            hours = df[col].dropna().apply(extract_hour_safe).dropna()
            hours_list.extend(hours.tolist())
    
    # Create hourly distribution
    hours_range = range(24)
    blore_hourly = [blore_hours.count(h) for h in hours_range]
    delhi_hourly = [delhi_hours.count(h) for h in hours_range]
    
    x = np.arange(24)
    width = 0.35
    
    plt.bar(x - width/2, blore_hourly, width, label='Bangalore', alpha=0.8, color='#FF6B6B')
    plt.bar(x + width/2, delhi_hourly, width, label='Delhi', alpha=0.8, color='#4ECDC4')
    
    plt.xlabel('Hour of Day')
    plt.ylabel('Number of Flights')
    plt.title('Hourly Traffic Pattern', fontsize=12, fontweight='bold')
    plt.legend()
    plt.xticks(range(0, 24, 3))
    plt.tight_layout()
    plt.savefig('plots/07_hourly_traffic_pattern.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 8. On-Time Performance Comparison
    plt.figure(figsize=(10, 6))
    
    # Calculate on-time performance
    def calculate_punctuality(df):
        dep_delays = df[df['Flight Type'] == 'Departure']['Departure Delay (min)'].dropna()
        arr_delays = df[df['Flight Type'] == 'Arrival']['Arrival Delay (min)'].dropna()
        
        dep_ontime = (dep_delays <= 15).sum() / len(dep_delays) * 100 if len(dep_delays) > 0 else 0
        arr_ontime = (arr_delays <= 15).sum() / len(arr_delays) * 100 if len(arr_delays) > 0 else 0
        
        return dep_ontime, arr_ontime
    
    blore_dep_ot, blore_arr_ot = calculate_punctuality(blore_df)
    delhi_dep_ot, delhi_arr_ot = calculate_punctuality(delhi_df)
    
    metrics = ['Departure\nOn-Time', 'Arrival\nOn-Time']
    blore_values = [blore_dep_ot, blore_arr_ot]
    delhi_values = [delhi_dep_ot, delhi_arr_ot]
    
    x = np.arange(len(metrics))
    width = 0.35
    
    plt.bar(x - width/2, blore_values, width, label='Bangalore', alpha=0.8, color='#FF6B6B')
    plt.bar(x + width/2, delhi_values, width, label='Delhi', alpha=0.8, color='#4ECDC4')
    
    plt.ylabel('On-Time Performance (%)')
    plt.title('On-Time Performance (≤15 min delay)', fontsize=12, fontweight='bold')
    plt.xticks(x, metrics)
    plt.legend()
    plt.ylim(0, 100)
    
    # Add percentage labels
    for i, (b_val, d_val) in enumerate(zip(blore_values, delhi_values)):
        plt.text(i - width/2, b_val + 1, f'{b_val:.1f}%', ha='center', fontweight='bold')
        plt.text(i + width/2, d_val + 1, f'{d_val:.1f}%', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('plots/08_ontime_performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 9. Average Delay by Carrier (Top 5)
    plt.figure(figsize=(10, 6))
    
    def get_carrier_delays(df, top_n=5):
        top_carriers = df['Carrier'].value_counts().head(top_n).index
        carrier_delays = []
        
        for carrier in top_carriers:
            carrier_data = df[df['Carrier'] == carrier]
            all_delays = pd.concat([
                carrier_data['Departure Delay (min)'].dropna(),
                carrier_data['Arrival Delay (min)'].dropna()
            ])
            avg_delay = all_delays.mean() if len(all_delays) > 0 else 0
            carrier_delays.append(avg_delay)
        
        return top_carriers, carrier_delays
    
    carriers, delays = get_carrier_delays(pd.concat([blore_df, delhi_df]), 6)
    
    plt.barh(range(len(carriers)), delays, alpha=0.8, color='#45B7D1')
    plt.yticks(range(len(carriers)), carriers)
    plt.xlabel('Average Delay (minutes)')
    plt.title('Average Delay by Top Carriers', fontsize=12, fontweight='bold')
    plt.gca().invert_yaxis()
    
    # Add delay values
    for i, delay in enumerate(delays):
        plt.text(delay + 0.2, i, f'{delay:.1f}', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('plots/09_average_delay_by_carrier.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 10. Delay Heatmap by Hour and Airport
    plt.figure(figsize=(12, 4))
    
    def create_delay_heatmap_data(df, airport_name):
        hourly_delays = {}
        for hour in range(24):
            hour_data = []
            for col in ['Scheduled Departure (Local)', 'Scheduled Arrival (Local)']:
                time_col = df[col].dropna()
                delay_col = 'Departure Delay (min)' if 'Departure' in col else 'Arrival Delay (min)'
                
                for idx, time_str in time_col.items():
                    try:
                        if pd.to_datetime(time_str).hour == hour:
                            delay = df.loc[idx, delay_col]
                            if pd.notna(delay):
                                hour_data.append(delay)
                    except:
                        continue
            
            hourly_delays[hour] = np.mean(hour_data) if hour_data else 0
        
        return list(hourly_delays.values())
    
    blore_hourly_delays = create_delay_heatmap_data(blore_df, 'Bangalore')
    delhi_hourly_delays = create_delay_heatmap_data(delhi_df, 'Delhi')
    
    heatmap_data = np.array([blore_hourly_delays, delhi_hourly_delays])
    
    sns.heatmap(heatmap_data, 
                xticklabels=range(24), 
                yticklabels=['Bangalore', 'Delhi'],
                annot=False, 
                cmap='RdYlBu_r', 
                center=0,
                cbar_kws={'label': 'Average Delay (min)'})
    plt.title('Average Delay by Hour', fontsize=12, fontweight='bold')
    plt.xlabel('Hour of Day')
    plt.tight_layout()
    plt.savefig('plots/10_delay_heatmap_by_hour.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 11. Severe Delay Analysis
    plt.figure(figsize=(12, 6))
    
    def severe_delay_analysis(df):
        all_delays = pd.concat([
            df['Departure Delay (min)'].dropna(),
            df['Arrival Delay (min)'].dropna()
        ])
        
        categories = ['On-Time\n(≤15 min)', 'Minor Delay\n(16-60 min)', 'Major Delay\n(61-120 min)', 'Severe Delay\n(>120 min)']
        
        on_time = (all_delays <= 15).sum()
        minor = ((all_delays > 15) & (all_delays <= 60)).sum()
        major = ((all_delays > 60) & (all_delays <= 120)).sum()
        severe = (all_delays > 120).sum()
        
        return categories, [on_time, minor, major, severe]
    
    blore_cats, blore_severe = severe_delay_analysis(blore_df)
    delhi_cats, delhi_severe = severe_delay_analysis(delhi_df)
    
    x = np.arange(len(blore_cats))
    width = 0.35
    
    plt.bar(x - width/2, blore_severe, width, label='Bangalore', alpha=0.8, color='#FF6B6B')
    plt.bar(x + width/2, delhi_severe, width, label='Delhi', alpha=0.8, color='#4ECDC4')
    
    plt.xlabel('Delay Categories')
    plt.ylabel('Number of Flights')
    plt.title('Delay Severity Distribution', fontsize=12, fontweight='bold')
    plt.xticks(x, blore_cats, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()
    plt.savefig('plots/11_delay_severity_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 12. Daily Flight Volume Trend
    plt.figure(figsize=(12, 6))
    
    def extract_date(time_str):
        if pd.isna(time_str):
            return None
        try:
            return pd.to_datetime(time_str).date()
        except:
            return None
    
    # Get dates from both airports
    for df, name in [(blore_df, 'Bangalore'), (delhi_df, 'Delhi')]:
        dates = []
        for col in ['Scheduled Departure (Local)', 'Scheduled Arrival (Local)']:
            dates.extend(df[col].dropna().apply(extract_date).dropna().tolist())
        
        date_counts = pd.Series(dates).value_counts().sort_index()
        
        plt.plot(range(len(date_counts)), date_counts.values, 
                marker='o', label=name, linewidth=2, markersize=6)
    
    plt.xlabel('Days')
    plt.ylabel('Number of Flights')
    plt.title('Daily Flight Volume Trend', fontsize=12, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('plots/12_daily_flight_volume_trend.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ All individual plots saved successfully!")
    print("\n📁 Saved Files:")
    for i, filename in enumerate([
        "01_flight_volume_comparison.png",
        "02_bangalore_flight_type_distribution.png", 
        "03_delhi_flight_type_distribution.png",
        "04_delay_distribution_comparison.png",
        "05_bangalore_top_airlines.png",
        "06_delhi_top_airlines.png", 
        "07_hourly_traffic_pattern.png",
        "08_ontime_performance_comparison.png",
        "09_average_delay_by_carrier.png",
        "10_delay_heatmap_by_hour.png",
        "11_delay_severity_distribution.png",
        "12_daily_flight_volume_trend.png"
    ], 1):
        print(f"   {i:2d}. plots/{filename}")


# Load the data - Update these paths to match your file locations
blore_df = pd.read_csv('data/blore_airport_data.csv')  # Adjust path as needed
delhi_df = pd.read_csv('data/delhi_airport_data.csv')   # Adjust path as needed

# Create individual visualizations
create_individual_visualizations(blore_df, delhi_df)

print(f"\n🎨 All plots saved individually in the 'plots/' folder!")
print(f"📱 Perfect for frontend integration - each chart is a separate, optimized file!")
