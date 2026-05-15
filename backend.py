import pandas as pd
import folium
from geopy.distance import geodesic
import requests

# ========================================================
# 1. HÀM LẤY THỜI TIẾT THẬT
# ========================================================
def get_real_weather(lat, lng):
    API_KEY = "ac08301614e960cf24bf27409d6a2b9f" 
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={API_KEY}&units=metric"
    
    try:
        res = requests.get(url).json()
        temp = res['main']['temp']
        condition = res['weather'][0]['main'].lower()
        
        if 'rain' in condition or 'drizzle' in condition or 'thunder' in condition:
            weather_label = "Rainy"
        elif temp >= 32:
            weather_label = "Hot"
        elif temp <= 22:
            weather_label = "Cold"
        else:
            weather_label = "Normal"
            
        return weather_label, temp
    except Exception as e:
        print("Lỗi gọi API Thời tiết:", e)
        return "Normal", 28

# ========================================================
# 2. HÀM TẠO BẢN ĐỒ THẬT TỪ FILE CSV
# ========================================================
def generate_real_map(user_lat, user_lng, chosen_restaurant_id=None):
    df = pd.read_csv('restaurant.csv')
    user_coords = (user_lat, user_lng)
    
    m = folium.Map(location=user_coords, zoom_start=14)
    
    folium.Marker(
        location=user_coords,
        tooltip="Vị trí của bạn",
        icon=folium.Icon(color="blue", icon="user", prefix='fa')
    ).add_to(m)
    
    for index, row in df.iterrows():
        res_coords = (row['lat'], row['lng'])
        res_name = row['name']
        
        dist_km = geodesic(user_coords, res_coords).kilometers
        
        if chosen_restaurant_id and row['restaurant_id'] == chosen_restaurant_id:
            folium.Marker(
                location=res_coords,
                tooltip=f"⭐ {res_name} ({dist_km:.1f} km)",
                icon=folium.Icon(color="red", icon="star", prefix='fa')
            ).add_to(m)
            
            folium.PolyLine(
                locations=[user_coords, res_coords],
                color="red", weight=4, opacity=0.8, dash_array='5'
            ).add_to(m)
        else:
            folium.Marker(
                location=res_coords,
                tooltip=f"{res_name} ({dist_km:.1f} km)",
                icon=folium.Icon(color="green", icon="cutlery", prefix='fa')
            ).add_to(m)
            
    return m
