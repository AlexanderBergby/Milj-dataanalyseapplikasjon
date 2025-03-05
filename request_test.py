import requests

url = "https://api.met.no/weatherapi/nowcast/2.0/complete"

params = {
    "lat": 63.4308,   # Latitude for Trondheim
    "lon": 10.4034    # Longitude for Trondheim
}

# MET User-Agent header.
headers = {
    "User-Agent": "MyWeatherApp/1.0 (abergby@gmail.com)"
}

# GET request
response = requests.get(url, params=params, headers=headers)

# GET request check
if response.status_code == 200:
    
    data = response.json()
    
    # Print tidspunkt for når data ble oppdatert
    updated_at = data["properties"]["meta"]["updated_at"]
    print(f"Data updated at: {updated_at}\n")
    
    # Print værdata for hvert tidspunkt
    for entry in data["properties"]["timeseries"]:
        time = entry.get("time", "Unknown time")
        details = entry.get("data", {}).get("instant", {}).get("details", {})
        
        air_temperature = details.get("air_temperature", "N/A")
        precipitation_rate = details.get("precipitation_rate", "N/A")
        relative_humidity = details.get("relative_humidity", "N/A")
        wind_direction = details.get("wind_from_direction", "N/A")
        wind_speed = details.get("wind_speed", "N/A")
        wind_gust = details.get("wind_speed_of_gust", "N/A")
        
        print(f"Time: {time}")
        print(f"  Air Temperature: {air_temperature} °C")
        print(f"  Precipitation Rate: {precipitation_rate} mm/h")
        print(f"  Relative Humidity: {relative_humidity} %")
        print(f"  Wind From Direction: {wind_direction}°")
        print(f"  Wind Speed: {wind_speed} m/s")
        print(f"  Wind Speed of Gust: {wind_gust} m/s")
        print("-" * 40)
else:
    print("Error fetching data. Status code:", response.status_code)
