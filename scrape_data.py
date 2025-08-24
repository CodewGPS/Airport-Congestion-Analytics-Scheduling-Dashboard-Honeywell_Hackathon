import requests
import csv
import time
from datetime import datetime, timedelta

API_KEY = "" #redacted
API_HOST = 'aerodatabox.p.rapidapi.com'

AIRPORTS = {
    'Bengaluru': 'VOBL'
}

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": API_HOST
}

def fetch_flight_data(icao, date_from, date_to, retries=3):
    url = f"https://aerodatabox.p.rapidapi.com/flights/airports/icao/{icao}/{date_from}/{date_to}"
    params = {
        'direction': 'Both',
        'withCancelled': 'true',
        'withCodeshared': 'true',
        'withCargo': 'true',
        'withPrivate': 'true'
    }
    for attempt in range(retries):
        response = requests.get(url, headers=HEADERS, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            print(f"Rate limit hit for {icao}. Retrying in 5 minutes...")
            time.sleep(300)  # 5 minutes
        else:
            print(f"Error fetching flights for {icao}: {response.status_code}")
            return None
    print(f"Failed after {retries} retries for {icao}.")
    return None

def calculate_delay(scheduled_utc, revised_utc):
    if scheduled_utc and revised_utc:
        try:
            sched_dt = datetime.fromisoformat(scheduled_utc.replace('Z', '+00:00'))
            rev_dt = datetime.fromisoformat(revised_utc.replace('Z', '+00:00'))
            delay_min = (rev_dt - sched_dt).total_seconds() / 60
            return round(delay_min, 2)
        except Exception:
            return ''
    return ''

def main():
    end_date = datetime(2025, 8, 22, 23, 59)
    start_date = datetime(2025, 8, 16, 0, 0)
    interval = timedelta(hours=12)
    max_requests_per_run = float('inf')  # Effectively unlimited
    max_rows = float('inf')

    all_rows = []
    all_rows.append([
        'Airport Name', 'Flight Type', 'Carrier', 'Flight Number',
        'Scheduled Departure (Local)', 'Revised Departure (Local)', 'Departure Delay (min)',
        'Scheduled Arrival (Local)', 'Revised Arrival (Local)', 'Arrival Delay (min)'
    ])

    request_count = 0
    row_count = 0  # Track data rows (excluding header)

    with open('indian_airports_flights_test.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(all_rows)  # Write header immediately

    for airport_name, airport_icao in AIRPORTS.items():
        current = start_date
        while current < end_date and request_count < max_requests_per_run and row_count < max_rows:
            interval_start = current
            interval_end = min(current + interval, end_date)
            date_from = interval_start.strftime('%Y-%m-%dT%H:%M')
            date_to = interval_end.strftime('%Y-%m-%dT%H:%M')

            flights_data = fetch_flight_data(airport_icao, date_from, date_to)
            request_count += 1
            if flights_data:
                for category, flights in [('Arrival', flights_data.get('arrivals', [])), ('Departure', flights_data.get('departures', []))]:
                    for flight in flights:
                        if row_count >= max_rows:
                            break
                        try:
                            carrier = flight.get('airline', {}).get('name', '')
                            flight_num = flight.get('number', '')

                            # Extract local times and UTC for delay calculation
                            if category == 'Arrival':
                                arr_data = flight.get('movement', {})
                                dep_data = flight.get('otherMovement', {}) if 'otherMovement' in flight else {}
                            else:  # Departure
                                dep_data = flight.get('movement', {})
                                arr_data = flight.get('otherMovement', {}) if 'otherMovement' in flight else {}

                            sched_dep_local = dep_data.get('scheduledTime', {}).get('local', '')
                            revised_dep_local = dep_data.get('revisedTime', {}).get('local', '') or sched_dep_local
                            sched_arr_local = arr_data.get('scheduledTime', {}).get('local', '')
                            revised_arr_local = arr_data.get('revisedTime', {}).get('local', '') or sched_arr_local

                            sched_dep_utc = dep_data.get('scheduledTime', {}).get('utc', '')
                            revised_dep_utc = dep_data.get('revisedTime', {}).get('utc', '') or sched_dep_utc
                            sched_arr_utc = arr_data.get('scheduledTime', {}).get('utc', '')
                            revised_arr_utc = arr_data.get('revisedTime', {}).get('utc', '') or sched_arr_utc

                            dep_delay = calculate_delay(sched_dep_utc, revised_dep_utc)
                            arr_delay = calculate_delay(sched_arr_utc, revised_arr_utc)

                            row = [
                                airport_name, category, carrier, flight_num,
                                sched_dep_local, revised_dep_local, dep_delay,
                                sched_arr_local, revised_arr_local, arr_delay
                            ]
                            all_rows.append(row)
                            row_count += 1
                        except Exception as e:
                            print(f"Data error for flight at {airport_name}: {e}")

            if request_count >= max_requests_per_run or row_count >= max_rows:
                print(f"Reached test limits (requests: {request_count}, rows: {row_count}). Stopping early.")
                break

            #time.sleep(10)  # Delay to respect rate limits (comment out for faster local testing)
            current += interval

    # Append remaining rows to CSV
    with open('Bengaluru_airport_data.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(all_rows[1:])  # Skip header since it's already written

    print(f"Total API requests made: {request_count}")
    print(f"Total data rows added: {row_count}")

if __name__ == "__main__":
    main()
