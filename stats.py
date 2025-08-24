import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Load and prepare data
blore_df = pd.read_csv('data/blore_airport_data.csv')
delhi_df = pd.read_csv('data/delhi_airport_data.csv')

blore_df['Airport'] = 'BLR'
delhi_df['Airport'] = 'DEL'
combined_df = pd.concat([blore_df, delhi_df], ignore_index=True)

# Convert datetime columns
combined_df['Scheduled Departure (Local)'] = pd.to_datetime(combined_df['Scheduled Departure (Local)'])
combined_df['Scheduled Arrival (Local)'] = pd.to_datetime(combined_df['Scheduled Arrival (Local)'])

# Extract time features
combined_df['Hour'] = combined_df['Scheduled Departure (Local)'].dt.hour
combined_df['Minute'] = combined_df['Scheduled Departure (Local)'].dt.minute
combined_df['Weekday'] = combined_df['Scheduled Departure (Local)'].dt.weekday
combined_df['Date'] = combined_df['Scheduled Departure (Local)'].dt.date

# Model 1: Optimal Time Slot Identification
def identify_optimal_slots(df):
    """Identify optimal takeoff/landing times based on delay patterns"""
    
    # Calculate average delay by hour for each airport
    hourly_delays = df.groupby(['Airport', 'Hour', 'Flight Type']).agg({
        'Departure Delay (min)': 'mean',
        'Arrival Delay (min)': 'mean',
        'Flight Number': 'count'  # Traffic volume
    }).reset_index()
    
    # Combine delays into single metric
    hourly_delays['Total_Delay'] = hourly_delays[['Departure Delay (min)', 'Arrival Delay (min)']].mean(axis=1)
    hourly_delays['Flight_Count'] = hourly_delays['Flight Number']
    
    # Score each time slot (lower delay + reasonable traffic = better)
    hourly_delays['Delay_Score'] = 1 / (hourly_delays['Total_Delay'] + 1)  # Avoid division by zero
    hourly_delays['Traffic_Score'] = 1 / (hourly_delays['Flight_Count'] + 1)
    hourly_delays['Optimal_Score'] = hourly_delays['Delay_Score'] * 0.7 + hourly_delays['Traffic_Score'] * 0.3
    
    return hourly_delays

optimal_slots = identify_optimal_slots(combined_df)

# Get top optimal slots for each airport
def get_top_optimal_slots(optimal_df, airport, top_n=5):
    airport_slots = optimal_df[optimal_df['Airport'] == airport].nlargest(top_n, 'Optimal_Score')
    return airport_slots[['Hour', 'Flight Type', 'Total_Delay', 'Flight_Count', 'Optimal_Score']]

print("TOP OPTIMAL DEPARTURE SLOTS - BANGALORE:")
blr_optimal = get_top_optimal_slots(optimal_slots, 'BLR')
print(blr_optimal)

print("TOP OPTIMAL DEPARTURE SLOTS - DELHI:")
del_optimal = get_top_optimal_slots(optimal_slots, 'DEL')
print(del_optimal)

def identify_busiest_slots(df):
    """Identify peak traffic periods and congestion hotspots"""
    
    # Hourly traffic analysis
    hourly_traffic = df.groupby(['Airport', 'Hour', 'Flight Type']).agg({
        'Flight Number': 'count',
        'Departure Delay (min)': 'mean',
        'Arrival Delay (min)': 'mean'
    }).reset_index()
    
    # Identify rush hours (top 20% traffic volume)
    hourly_traffic['Traffic_Percentile'] = hourly_traffic.groupby('Airport')['Flight Number'].rank(pct=True)
    rush_hours = hourly_traffic[hourly_traffic['Traffic_Percentile'] >= 0.8]
    
    # Calculate congestion index (traffic volume × average delay)
    hourly_traffic['Congestion_Index'] = (
        hourly_traffic['Flight Number'] * 
        hourly_traffic[['Departure Delay (min)', 'Arrival Delay (min)']].mean(axis=1)
    )
    
    return hourly_traffic, rush_hours

traffic_analysis, rush_periods = identify_busiest_slots(combined_df)

print("🚦 BUSIEST TIME SLOTS:")
busiest = traffic_analysis.nlargest(10, 'Congestion_Index')[['Airport', 'Hour', 'Flight Type', 'Flight Number', 'Congestion_Index']]
print(busiest)

# Visualize traffic patterns
plt.figure(figsize=(15, 6))
for airport in ['BLR', 'DEL']:
    airport_data = traffic_analysis[traffic_analysis['Airport'] == airport]
    hourly_counts = airport_data.groupby('Hour')['Flight Number'].sum()
    plt.plot(hourly_counts.index, hourly_counts.values, marker='o', label=f'{airport} Traffic', linewidth=2)

plt.title('Hourly Flight Traffic Patterns')
plt.xlabel('Hour of Day')
plt.ylabel('Number of Flights')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

def identify_high_impact_flights(df):
    """Identify flights that cause cascading delays and operational disruptions"""
    
    # Calculate impact score based on multiple factors
    df_analysis = df.copy()
    
    # Factor 1: Delay magnitude
    df_analysis['Delay_Impact'] = np.abs(df_analysis[['Departure Delay (min)', 'Arrival Delay (min)']].max(axis=1))
    
    # Factor 2: Carrier importance (based on flight frequency)
    carrier_frequency = df_analysis['Carrier'].value_counts()
    df_analysis['Carrier_Importance'] = df_analysis['Carrier'].map(carrier_frequency)
    
    # Factor 3: Time slot criticality (rush hour = higher impact)
    df_analysis['Rush_Hour_Impact'] = np.where(
        df_analysis['Hour'].isin([6, 7, 8, 9, 17, 18, 19, 20, 21]), 2.0, 1.0
    )
    
    # Factor 4: Weekend/weekday impact
    df_analysis['Weekend_Impact'] = np.where(df_analysis['Weekday'] >= 5, 1.5, 1.0)
    
    # Calculate composite impact score
    df_analysis['Impact_Score'] = (
        df_analysis['Delay_Impact'] * 0.4 +
        np.log(df_analysis['Carrier_Importance']) * 0.3 +
        df_analysis['Rush_Hour_Impact'] * 0.2 +
        df_analysis['Weekend_Impact'] * 0.1
    )
    
    return df_analysis

high_impact_df = identify_high_impact_flights(combined_df)

# Get top high-impact flights
print("TOP HIGH-IMPACT FLIGHTS:")
high_impact_flights = high_impact_df.nlargest(15, 'Impact_Score')[
    ['Flight Number', 'Carrier', 'Airport', 'Hour', 'Delay_Impact', 'Impact_Score']
]
print(high_impact_flights)

# Analyze high-impact carriers
print("HIGH-IMPACT CARRIERS:")
carrier_impact = high_impact_df.groupby('Carrier').agg({
    'Impact_Score': ['mean', 'sum', 'count']
}).round(2)
carrier_impact.columns = ['Avg_Impact', 'Total_Impact', 'Flight_Count']
carrier_impact = carrier_impact.sort_values('Total_Impact', ascending=False).head(10)
print(carrier_impact)

def optimize_schedule(df, target_date, airport='BLR'):
    """Generate optimized schedule recommendations"""
    
    # Get current day's flights
    target_flights = df[
        (df['Date'] == target_date) & 
        (df['Airport'] == airport)
    ].copy()
    
    if len(target_flights) == 0:
        return "No flights found for the specified date and airport"
    
    # Optimization recommendations
    recommendations = []
    
    # 1. Identify problematic time slots
    problematic_slots = target_flights.groupby('Hour').agg({
        'Departure Delay (min)': 'mean',
        'Flight Number': 'count'
    })
    
    high_delay_slots = problematic_slots[problematic_slots['Departure Delay (min)'] > 30]
    
    for hour, data in high_delay_slots.iterrows():
        recommendations.append({
            'type': 'Schedule Redistribution',
            'hour': hour,
            'issue': f'High average delay: {data["Departure Delay (min)"]:.1f} min',
            'solution': f'Move {int(data["Flight Number"] * 0.3)} flights to optimal slots: {get_best_alternative_slots(hour)}',
            'priority': 'High' if data["Departure Delay (min)"] > 60 else 'Medium'
        })
    
    # 2. Runway utilization optimization
    runway_utilization = target_flights.groupby('Hour')['Flight Number'].sum()
    peak_hours = runway_utilization[runway_utilization > runway_utilization.quantile(0.8)].index
    
    for hour in peak_hours:
        recommendations.append({
            'type': 'Capacity Management',
            'hour': hour,
            'issue': f'Peak traffic: {runway_utilization[hour]} flights',
            'solution': 'Implement ground holds, increase spacing between flights',
            'priority': 'High'
        })
    
    return recommendations

def get_best_alternative_slots(current_hour):
    """Find best alternative time slots"""
    optimal_hours = optimal_slots.nlargest(3, 'Optimal_Score')['Hour'].tolist()
    alternatives = [h for h in optimal_hours if abs(h - current_hour) >= 2]
    return alternatives[:2] if alternatives else [current_hour - 2, current_hour + 2]
