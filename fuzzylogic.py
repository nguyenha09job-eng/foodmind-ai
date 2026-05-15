import pandas as pd
import json
import math
from datetime import datetime
from geopy.distance import geodesic

# ==========================================
# CÁC HÀM TOÁN HỌC FUZZY CƠ BẢN
# ==========================================
def trimf(x, abc):
    """Hàm liên thuộc tam giác (Triangular Membership Function)"""
    a, b, c = abc
    if x <= a or x >= c: return 0.0
    elif a < x <= b: return (x - a) / (b - a) if a != b else 1.0
    elif b < x < c: return (c - x) / (c - b) if b != c else 1.0
    return 0.0

def trapmf(x, abcd):
    """Hàm liên thuộc hình thang (Trapezoidal Membership Function)"""
    a, b, c, d = abcd
    if x <= a or x >= d: return 0.0
    elif a < x <= b: return (x - a) / (b - a) if a != b else 1.0
    elif b < x <= c: return 1.0
    elif c < x < d: return (d - x) / (d - c) if c != d else 1.0
    return 0.0

# ==========================================
# 1. TẢI DỮ LIỆU
# ==========================================
def load_data():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except:
        config = {
            "price_membership_fn": {"under_30k": [0, 15000, 30000], "30_50k": [20000, 40000, 60000], "50_100k": [45000, 75000, 120000], "over_100k": [90000, 150000, 10000000]},
            "time_membership_fn": {"express": [0, 0, 10, 15], "fast": [10, 15, 25, 30], "normal": [20, 30, 45, 60], "no_rush": [45, 60, 120, 120]},
            "hunger_to_calorie_map": {"Light": 200, "Hungry": 500, "Very_Hungry": 800, "Starving": 1200},
            "score_weights": {"price": 0.3, "time": 0.2, "calorie": 0.2, "diet": 0.15, "weather": 0.15}
        }
    
    dishes_df = pd.read_csv('dishes.csv', sep=';')
    if len(dishes_df.columns) < 5: 
        dishes_df = pd.read_csv('dishes.csv', sep=',')
        
    restaurants_df = pd.read_csv('restaurant.csv')
    return config, dishes_df, restaurants_df

# ==========================================
# 2. CÁC HÀM TÍNH ĐIỂM THÀNH PHẦN (FUZZY LOGIC)
# ==========================================
def calculate_price_score(dish_price, user_budget_label, config):
    abc = config['price_membership_fn'].get(user_budget_label, [0, 1000000, 1000000])
    return trimf(float(dish_price), abc)

def calculate_time_score(est_delivery_time, user_time_label, config):
    abcd = config['time_membership_fn'].get(user_time_label, [0, 0, 120, 120])
    return trapmf(float(est_delivery_time), abcd)

def calculate_calorie_score(dish_calories, user_hunger_label, config):
    target_cal = config['hunger_to_calorie_map'].get(user_hunger_label, 500)
    dish_cal = float(dish_calories)
    diff = abs(dish_cal - target_cal)
    score = 1.0 - min(1.0, diff / target_cal)
    return max(0.0, score)

def calculate_diet_score(p, c, f, cal, user_diet_mode, config):
    targets = config.get('diet_macro_targets', {}).get(user_diet_mode, {})
    if user_diet_mode == "Normal" or not targets:
        return 1.0
    score = 1.0
    if user_diet_mode == "Diet":
        if c > targets.get('carb_max', 50): score -= (c - targets['carb_max']) / 100
        if f > targets.get('fat_max', 20): score -= (f - targets['fat_max']) / 50
        if cal > targets.get('calorie_max', 500): score -= (cal - targets['calorie_max']) / 500
    elif user_diet_mode == "Bulking":
        if p < targets.get('protein_min', 30): score -= (targets['protein_min'] - p) / 50
        if c < targets.get('carb_min', 80): score -= (targets['carb_min'] - c) / 100
        if cal < targets.get('calorie_min', 800): score -= (targets['calorie_min'] - cal) / 1000
    if score < 0.1:
        score = 0.1
    return score
        
    return 0.2
def normalize_category(raw_cat):
    raw_cat = str(raw_cat).lower().strip()
    
    # Bản đồ quy đổi
    mapping = {
        'full_meal': ['rice', 'pho', 'bun_bo', 'hotpot', 'noodle', 'sashimi', 'sushi', 'bread', 'pasta', 'nuong'],
        'snack': ['snack', 'fried_food', 'cake', 'dimsum', 'skewer'],
        'drink': ['drink', 'coffee', 'tea', 'juice', 'milkshake'],
        'dessert': ['dessert', 'che', 'ice_cream', 'yogurt'],
        'healthy_meal': ['salad', 'healthy', 'wrap', 'poke', 'soup'],
        'fast_food': ['fast_food', 'burger', 'pizza', 'fried_chicken']
    }
    
    for main_cat, sub_cats in mapping.items():
        if raw_cat == main_cat or raw_cat in sub_cats:
            return main_cat
            
    return 'full_meal'
def calculate_weather_score(food_category, current_weather, config):
    normalized_cat = normalize_category(food_category)
    weather_map = config.get('weather_food_map', {})
    weights_for_current_weather = weather_map.get(current_weather, {})
    weight = weights_for_current_weather.get(normalized_cat, 1.0)
    return min(1.0, weight / 1.5)

# ==========================================
# 3. HÀM TỔNG HỢP MATCH SCORE & XUẤT KẾT QUẢ
# ==========================================
def check_open_hours(open_hours_str):
    if pd.isna(open_hours_str) or not isinstance(open_hours_str, str):
        return True

    try:
        now = datetime.now().time()
        start_str, end_str = open_hours_str.split('-')
        
        start = datetime.strptime(start_str.strip(), "%H:%M").time()
        end = datetime.strptime(end_str.strip(), "%H:%M").time()
        
        if start <= end:
            return start <= now <= end
        else: 
            return now >= start or now <= end
    except:
        return True
def calculate_quality_score(rating, order_count):
    try:
        r = float(rating) if pd.notna(rating) else 4.0
        c = float(order_count) if pd.notna(order_count) else 100
    except:
        r = 4.0
        c = 100
        
    r_score = r / 5.0
    
    c_score = min(1.0, c / 2000.0)
    
    quality_score = (r_score * 0.7) + (c_score * 0.3)
    return quality_score
def calculate_cuisine_score(dish_cuisine, user_cuisine):
    if not user_cuisine or str(user_cuisine).lower() == "any":
        return 1.0
        
    dish_c = str(dish_cuisine).lower()
    u_c = str(user_cuisine).lower()
    
    if u_c in dish_c:
        return 1.0
        
    return 0.1
def get_recommendations(user_inputs, config, dishes_df, restaurants_df):
    weights = config.get('score_weights', {"price": 0.3, "time": 0.2, "calorie": 0.2, "diet": 0.15, "weather": 0.15})
    results = []
    
    res_dict = restaurants_df.set_index('restaurant_id').to_dict('index')
    
    for index, dish in dishes_df.iterrows():
        if str(dish.get('is_available', 'True')).lower() == 'false': continue
        
        res_id = dish['restaurant_id']
        res_info = res_dict.get(res_id, {})
        
        if str(res_info.get('is_open', 'True')).lower() == 'false': 
            continue
            
        open_hours = res_info.get('open_hours', '00:00-23:59')
        if not check_open_hours(open_hours):
            continue
        #tính thời gian giao
        user_coords = (user_inputs.get('lat', 10.7614), user_inputs.get('lng', 106.6686))
        
        res_lat = res_info.get('lat')
        res_lng = res_info.get('lng')
        
        if pd.notna(res_lat) and pd.notna(res_lng):
            res_coords = (res_lat, res_lng)
            distance_km = geodesic(user_coords, res_coords).kilometers
            travel_time = (distance_km * 4) + 2
        else:
            travel_time = 10
            
        est_delivery_time = res_info.get('avg_prep_time', 15) + travel_time 
            
        p_score = calculate_price_score(dish['price'], user_inputs['budget'], config)
        t_score = calculate_time_score(est_delivery_time, user_inputs['time'], config)
        c_score = calculate_calorie_score(dish['calories'], user_inputs['hunger'], config)
        d_score = calculate_diet_score(
            float(dish['protein_g']), 
            float(dish['carb_g']), 
            float(dish['fat_g']), 
            float(dish['calories']), 
            user_inputs['health_goal'], 
            config
        )
        w_score = calculate_weather_score(
            dish['food_category'], 
            user_inputs['weather'], 
            config
        )
        
        q_score = calculate_quality_score(dish.get('rating', 4.0), dish.get('order_count', 0))
        
        cu_score = calculate_cuisine_score(dish.get('cuisine_type', ''), user_inputs.get('cuisine', 'any'))
        
        base_match_score = (p_score * weights.get('price', 0.25)) + \
                           (t_score * weights.get('time', 0.25)) + \
                           (c_score * weights.get('calorie', 0.20)) + \
                           (d_score * weights.get('diet', 0.20)) + \
                           (w_score * weights.get('weather', 0.10))
                      
        final_score = ((base_match_score * 0.85) + (q_score * 0.15)) * cu_score
        
        results.append({
            'dish_id': dish['dish_id'],
            'dish_name': dish['name'],
            'restaurant_id': res_id,
            'restaurant_name': res_info.get('name', 'Unknown'),
            'price': dish['price'],
            'match_score': round(final_score * 100, 2)
        })
    results.sort(key=lambda x: x['match_score'], reverse=True)
    return results
def generate_daily_plan(user_inputs, config, dishes_df, res_dict):
    recs = get_recommendations(user_inputs, config, dishes_df, res_dict)
    plan = {}
    used = []
    
    for r in recs:
        d_info = dishes_df[dishes_df['dish_id'] == r['dish_id']].iloc[0]
        cat = normalize_category(d_info['food_category'])
        
        if 'Breakfast' not in plan and cat in ['snack', 'healthy_meal', 'drink']:
            plan['Breakfast'] = r
            used.append(r['dish_id'])
            
    for r in recs:
        d_info = dishes_df[dishes_df['dish_id'] == r['dish_id']].iloc[0]
        cat = normalize_category(d_info['food_category'])
        
        if 'Lunch' not in plan and cat == 'full_meal' and r['dish_id'] not in used:
            plan['Lunch'] = r
            used.append(r['dish_id'])
            
    for r in recs:
        if 'Dinner' not in plan and r['dish_id'] not in used:
            plan['Dinner'] = r
            used.append(r['dish_id'])
            
    if 'Breakfast' not in plan and len(recs) > 0:
        for r in recs:
            if r['dish_id'] not in used:
                plan['Breakfast'] = r
                used.append(r['dish_id'])
                break
                
    return plan
