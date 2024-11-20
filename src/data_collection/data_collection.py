import requests
import pandas as pd
import time

# Your WAQI API token
API_TOKEN = 'f7b74d642f440311a13febeb994715999e66ecdc'

# Base URL for the API
API_URL = 'https://api.waqi.info/feed/{location}/?token={token}'

# List of locations you want to track AQI for
locations = [
    'Albania', 'Algeria', 'Andorra', 'Angola', 'Argentina', 'Armenia', 'Australia', 
    'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium', 'Belize', 
    'Bermuda', 'Bolivia', 'Bosnia and Herzegovina', 'Brazil', 'Brunei', 'Bulgaria', 
    'Burkina Faso', 'Cambodia', 'Canada', 'Cape Verde', 'Cayman Islands', 
    'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Costa Rica', 
    'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Dominican Republic', 'Ecuador', 
    'Egypt', 'El Salvador', 'Estonia', 'Ethiopia', 'Finland', 'France', 'French Guiana', 
    'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Grenada', 
    'Guadeloupe', 'Guam', 'Guatemala', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 
    'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Ivory Coast', 
    'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya'
]


# Function to fetch data from the WAQI API
def fetch_aqi_data(location):
    try:
        url = API_URL.format(location=location, token=API_TOKEN)
        response = requests.get(url)
        data = response.json()

        if data['status'] == 'ok':
            aqi = data['data']['aqi']
            time_local = data['data']['time']['s']
            ts_utc = data['data']['time']['tz']
            pollutants = data['data']['iaqi']

            # Extract key pollutants
            pm25 = pollutants.get('pm25', {}).get('v', None)
            pm10 = pollutants.get('pm10', {}).get('v', None)
            co = pollutants.get('co', {}).get('v', None)
            no2 = pollutants.get('no2', {}).get('v', None)
            o3 = pollutants.get('o3', {}).get('v', None)
            so2 = pollutants.get('so2', {}).get('v', None)

            return {
                'country': location,
                'aqi': aqi,
                'co': co,
                'datetime': time_local,
                'no2': no2,
                'o3': o3,
                'pm10': pm10,
                'pm25': pm25,
                'so2': so2,
                'timestamp_local': time_local,
                'timestamp_utc': ts_utc,
                'ts': time.time()  # Current timestamp in seconds
            }
        else:
            print(f"Error fetching data for {location}: {data.get('data', 'Unknown error')}")
            return None
    except Exception as e:
        print(f"Error occurred for {location}: {e}")
        return None

# Collect data for multiple locations
def collect_data():
    records = []
    for location in locations:
        data = fetch_aqi_data(location)
        if data:
            records.append(data)
        time.sleep(1)  # To avoid hitting the rate limit

    # Convert the list of records to a DataFrame
    df = pd.DataFrame(records)
    return df

# Save the data to a CSV file
def save_data_to_csv(df, filename='aqi_data.csv'):
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main execution
if __name__ == '__main__':
    print("Fetching AQI data...")
    df = collect_data()
    
    if not df.empty:
        save_data_to_csv(df)
    else:
        print("No data fetched.")
