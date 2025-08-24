import pandas as pd
import numpy as np

def calculate_airport_metrics(df, airport_name):
    """
    Calculate comprehensive airport performance metrics

    """
    print(f"\n{'='*60}")
    print(f"AIRPORT PERFORMANCE METRICS FOR {airport_name.upper()}")
    print(f"{'='*60}")
    
    # Basic statistics
    total_flights = len(df)
    departures = df[df['Flight Type'] == 'Departure']
    arrivals = df[df['Flight Type'] == 'Arrival']
    
    print(f"\n1. BASIC STATISTICS:")
    print(f"   Total Flights: {total_flights:,}")
    print(f"   Departures: {len(departures):,}")
    print(f"   Arrivals: {len(arrivals):,}")
    
    # Delay metrics for departures
    departure_delays = departures['Departure Delay (min)'].dropna()
    if len(departure_delays) > 0:
        print(f"\n2. DEPARTURE PERFORMANCE:")
        print(f"   Average Departure Delay: {departure_delays.mean():.2f} minutes")
        print(f"   Median Departure Delay: {departure_delays.median():.2f} minutes")
        print(f"   Max Departure Delay: {departure_delays.max():.0f} minutes")
        print(f"   Min Departure Delay: {departure_delays.min():.0f} minutes")
        
        # On-time performance (within 15 minutes)
        on_time_departures = (departure_delays <= 15).sum()
        departure_punctuality = (on_time_departures / len(departure_delays)) * 100
        print(f"   On-time Departure Rate (≤15 min): {departure_punctuality:.1f}%")
        
        # Severely delayed flights (>60 minutes)
        severely_delayed_dep = (departure_delays > 60).sum()
        severe_delay_rate_dep = (severely_delayed_dep / len(departure_delays)) * 100
        print(f"   Severely Delayed Departures (>60 min): {severe_delay_rate_dep:.1f}%")
    
    # Delay metrics for arrivals
    arrival_delays = arrivals['Arrival Delay (min)'].dropna()
    if len(arrival_delays) > 0:
        print(f"\n3. ARRIVAL PERFORMANCE:")
        print(f"   Average Arrival Delay: {arrival_delays.mean():.2f} minutes")
        print(f"   Median Arrival Delay: {arrival_delays.median():.2f} minutes")
        print(f"   Max Arrival Delay: {arrival_delays.max():.0f} minutes")
        print(f"   Min Arrival Delay: {arrival_delays.min():.0f} minutes")
        
        # On-time performance
        on_time_arrivals = (arrival_delays <= 15).sum()
        arrival_punctuality = (on_time_arrivals / len(arrival_delays)) * 100
        print(f"   On-time Arrival Rate (≤15 min): {arrival_punctuality:.1f}%")
        
        # Severely delayed flights
        severely_delayed_arr = (arrival_delays > 60).sum()
        severe_delay_rate_arr = (severely_delayed_arr / len(arrival_delays)) * 100
        print(f"   Severely Delayed Arrivals (>60 min): {severe_delay_rate_arr:.1f}%")
    
    # Carrier performance
    print(f"\n4. TOP 10 CARRIERS BY FLIGHT COUNT:")
    carrier_counts = df['Carrier'].value_counts().head(10)
    for i, (carrier, count) in enumerate(carrier_counts.items(), 1):
        percentage = (count / total_flights) * 100
        print(f"   {i:2d}. {carrier:<20} {count:4d} flights ({percentage:5.1f}%)")
    
    # Carrier delay analysis (for carriers with significant operations)
    print(f"\n5. CARRIER DELAY PERFORMANCE (Carriers with >50 flights):")
    major_carriers = df['Carrier'].value_counts()[df['Carrier'].value_counts() > 50].index
    
    carrier_delay_stats = []
    for carrier in major_carriers:
        carrier_data = df[df['Carrier'] == carrier]
        
        # Departure delays
        dep_delays = carrier_data[carrier_data['Flight Type'] == 'Departure']['Departure Delay (min)'].dropna()
        arr_delays = carrier_data[carrier_data['Flight Type'] == 'Arrival']['Arrival Delay (min)'].dropna()
        
        avg_dep_delay = dep_delays.mean() if len(dep_delays) > 0 else 0
        avg_arr_delay = arr_delays.mean() if len(arr_delays) > 0 else 0
        
        carrier_delay_stats.append({
            'Carrier': carrier,
            'Total_Flights': len(carrier_data),
            'Avg_Dep_Delay': avg_dep_delay,
            'Avg_Arr_Delay': avg_arr_delay
        })
    
    carrier_df = pd.DataFrame(carrier_delay_stats).sort_values('Total_Flights', ascending=False)
    
    for _, row in carrier_df.head(10).iterrows():
        print(f"   {row['Carrier']:<20} Flights: {row['Total_Flights']:3d} | "
              f"Dep: {row['Avg_Dep_Delay']:6.1f}min | Arr: {row['Avg_Arr_Delay']:6.1f}min")
    
    # Hourly distribution
    print(f"\n6. FLIGHT DISTRIBUTION BY HOUR:")
    
    # Extract hours from scheduled times
    def extract_hour(time_str):
        if pd.isna(time_str):
            return None
        try:
            return pd.to_datetime(time_str).hour
        except:
            return None
    
    # Departure hours
    dep_scheduled = departures['Scheduled Departure (Local)'].dropna()
    if len(dep_scheduled) > 0:
        dep_hours = dep_scheduled.apply(extract_hour).dropna()
        hourly_dep = dep_hours.value_counts().sort_index()
        print("   Busiest Departure Hours:")
        for hour, count in hourly_dep.head(5).items():
            print(f"     {hour:2d}:00 - {count:3d} departures")
    
    # Arrival hours
    arr_scheduled = arrivals['Scheduled Arrival (Local)'].dropna()
    if len(arr_scheduled) > 0:
        arr_hours = arr_scheduled.apply(extract_hour).dropna()
        hourly_arr = arr_hours.value_counts().sort_index()
        print("   Busiest Arrival Hours:")
        for hour, count in hourly_arr.head(5).items():
            print(f"     {hour:2d}:00 - {count:3d} arrivals")
    
    return {
        'total_flights': total_flights,
        'departure_punctuality': departure_punctuality if len(departure_delays) > 0 else 0,
        'arrival_punctuality': arrival_punctuality if len(arrival_delays) > 0 else 0,
        'avg_departure_delay': departure_delays.mean() if len(departure_delays) > 0 else 0,
        'avg_arrival_delay': arrival_delays.mean() if len(arrival_delays) > 0 else 0
    }

# Load the data
blore_df = pd.read_csv('data/blore_airport_data.csv')
delhi_df = pd.read_csv('data/delhi_airport_data.csv')

# Calculate metrics for both airports
blore_metrics = calculate_airport_metrics(blore_df, 'Bangalore')
delhi_metrics = calculate_airport_metrics(delhi_df, 'Delhi')

# Comparative analysis
print(f"\n{'='*60}")
print("COMPARATIVE ANALYSIS")
print(f"{'='*60}")

print(f"\nMetric                          Bangalore    Delhi")
print(f"{'─'*50}")
print(f"Total Flights                   {blore_metrics['total_flights']:8,} {delhi_metrics['total_flights']:8,}")
print(f"Departure Punctuality (≤15min)    {blore_metrics['departure_punctuality']:6.1f}%   {delhi_metrics['departure_punctuality']:6.1f}%")
print(f"Arrival Punctuality (≤15min)      {blore_metrics['arrival_punctuality']:6.1f}%   {delhi_metrics['arrival_punctuality']:6.1f}%")
print(f"Avg Departure Delay               {blore_metrics['avg_departure_delay']:6.1f}min  {delhi_metrics['avg_departure_delay']:6.1f}min")
print(f"Avg Arrival Delay                 {blore_metrics['avg_arrival_delay']:6.1f}min  {delhi_metrics['avg_arrival_delay']:6.1f}min")

