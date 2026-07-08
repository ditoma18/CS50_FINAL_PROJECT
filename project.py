import json
import random
import sys
import requests

# Constant Port Coordinates for Gbétsogbé / Lomé, Togo
LOME_LAT = 6.12
LOME_LON = 1.22


def main():
    print("=========================================")
    print("   LOMÉ PORT MARITIME APP CORE SYSTEM   ")
    print("=========================================")

    while True:
        print("\n[MAIN MENU]")
        print("1. Assess Localized Weather & Marine previsions")
        print("2. Get Fish Species Regulations")
        print("3. BROADCAST PANIC EMERGENCY (SOS)")
        print("4. View Shore Command Center Alerts (Land-Base)")
        print("5. Terminate Connection")

        choice = input("\nSelect an option from 1 to 5: ").strip()

        if choice == "1":
            curr_lat, curr_lon = simulate_gps()
            print("Getting atmospheric and marine previsons from Open meteo...")

            forecast_data = get_combined_marine_forecast(curr_lat, curr_lon)
            
            # The Warning System
            if forecast_data["is_live"] is False:
                print("\n" + "!"*50)
                print(" ⚠️ WARNING: SATELLITE CONNECTION LOST")
                print("!"*50)
                print(forecast_data["timeline"])
            elif forecast_data["is_live"] is True:
                print_marine_dashboard(forecast_data["timeline"])
                
            

        elif choice == "2":
            fish = input("\nWhat fish species are you interested in? (Sardinella / Anchovy): ")
            print(get_species_advice(fish))

        elif choice == "3":
            uid = input("Confirm unique Fisher registration code: ").strip()
            if not uid:
                uid = "ANONYMOUS_PIROGUE"
            curr_lat, curr_lon = simulate_gps()
            sos_message = trigger_sos(uid, curr_lat, curr_lon)
            print(sos_message)

        elif choice == "4":
            print("\nConnecting to land-based emergency repository standard protocols...")
            alerts = read_shore_alerts()
            if not alerts:
                print("🟢 Operational Status: Clear. No active SOS alerts recorded.")
            for idx, alert in enumerate(alerts, 1):
                print(f"\n[INCIDENT #{idx}] - TARGET: {alert['fisher_id']}")
                print(f"-> Position Vector: ({alert['latitude']}, {alert['longitude']})")
                print(f"-> Active Tracking Marker: {alert['map_anchor']}")
                print(f"-> Mission Lifecycle Status: {alert['status']}")

        elif choice == "5":
            print("\nShutting down.........\nStay safe on the water! We love what you do.\n")
            sys.exit(0)

        else:
            print("❌ Input unrecognized. Select an option from 1 to 5.")


def simulate_gps():
    """Varies coordinates near Lomé Port to simulate vessel spatial tracking."""
    lat = LOME_LAT + random.uniform(-0.04, 0.04)
    lon = LOME_LON + random.uniform(-0.04, 0.04)
    return round(lat, 4), round(lon, 4)

def get_combined_marine_forecast(lat=LOME_LAT, lon=LOME_LON):
    """Fetches atmospheric and marine parameters, stitching them into a 24-hour timeline."""
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation_probability,visibility,wind_speed_10m&forecast_days=1"
    marine_url = f"https://marine-api.open-meteo.com/v1/marine?latitude={lat}&longitude={lon}&hourly=wave_height,wave_direction,ocean_current_velocity,ocean_current_direction&forecast_days=1"

    try:
        w_res = requests.get(weather_url, timeout=5)
        m_res = requests.get(marine_url, timeout=5)

        w_res.raise_for_status()
        m_res.raise_for_status()

        w_data = w_res.json().get("hourly", {})
        m_data = m_res.json().get("hourly", {})

        timeline = []
        total_hours = len(w_data.get("time", []))

        for i in range(total_hours):
            hour_str = w_data["time"][i].split("T")[1]
            visibility_km = w_data["visibility"][i] / 1000 if w_data.get("visibility") else 10.0

            timeline.append({
                "hour": hour_str,
                "temp": w_data["temperature_2m"][i],
                "rain_prob": w_data["precipitation_probability"][i],
                "visibility": round(visibility_km, 1),
                "wind_speed": w_data["wind_speed_10m"][i],
                "wave_height": m_data["wave_height"][i] if m_data.get("wave_height") else 0.0,
                "wave_dir": m_data["wave_direction"][i] if m_data.get("wave_direction") else 0,
                "current_vel": m_data["ocean_current_velocity"][i] if m_data.get("ocean_current_velocity") else 0.0,
                "current_dir": m_data["ocean_current_direction"][i] if m_data.get("ocean_current_direction") else 0
            })

        # SUCCESS PATH: This return a dictionary matching the error fallback path!
        return {"timeline": timeline, "is_live": True}

    except (requests.RequestException, KeyError, IndexError):
        # Offline situation
        fallback = "Internet connection is needed to be able to see weather forcasts"
        return {"timeline": fallback, "is_live": False}
        
        
def calculate_safety_flag(wind, wave, visibility):
    """Evaluates combined risk matrix parameters to determine an operational flag."""
    if wind > 7.0 or wave > 1.8 or visibility < 3.0:
        return "🔴 DANGER"
    elif wind > 5.0 or wave > 1.2 or visibility < 6.0:
        return "⚠️ CAUTION"
    return "🟢 SAFE"


def print_marine_dashboard(timeline):
    """Renders a structured terminal dashboard showing evolution of metrics."""
    print("\n📊 24-HOUR COMBINED MARITIME TIMELINE FORECAST")
    print("=" * 105)
    header = f"{'Hour':<6} | {'Wind(m/s)':<10} | {'Wave(m)':<8} | {'Wave Dir':<8} | {'Current(m/s)':<12} | {'Vis(km)':<8} | {'Rain%':<6} | {'Status'}"
    print(header)
    print("=" * 105)

    for index, pt in enumerate(timeline):
        if index % 2 == 0:  # Sample values every 2 hours
            status = calculate_safety_flag(pt["wind_speed"], pt["wave_height"], pt["visibility"])
            print(f"{pt['hour']:<6} | {pt['wind_speed']:<10.1f} | {pt['wave_height']:<8.1f} | {pt['wave_dir']:<8}° | {pt['current_vel']:<12.2f} | {pt['visibility']:<8.1f} | {pt['rain_prob']:<5}% | {status}")
    print("=" * 105)


def get_species_advice(species_name):
    """Provides biological and regulatory information for Togo."""
    database = {
        "sardinella": {
            "scientific name": "Sardinella aurita",
            "min_size": "12 cm",
            "status": "Overfished Threat",
            "tip": "Avoid juvenile spawning zones during the major upwelling window (July - September)."
        },
        "anchovy": {
            "scientific name": "Engraulis encrasicolus",
            "min_size": "10 cm",
            "status": "Stable Exploitation",
            "regulation": "Use a regulated mesh diameter size to allow immature stocks to escape nets."
        }
    }

    clean_name = species_name.strip().lower()
    if clean_name in database:
        info = database[clean_name]
        return f"\n[INFO] {clean_name.upper()} ({info['scientific']})\n- Legal Size Limit: >= {info['min_size']}\n- Sustainability: {info['status']}\n- Management: {info['tip']}"
    else:
        user_contribution = []
        print('Species data is unavailable or not registered yet in our database.\n\nIf you want to register new species, Put it here. Thank you! :)')
        specie_name = input('specie_name : ')
        scientific_name = input('scientific name : ')
        min_size = input('minimum size : ')
        status = ('status : ')
        regulation = ('Regulation : ')
        new_info = {specie_name : {
                    "scientific name": scientific_name,
                    "min_size": min_size,
                    "status": status,
                    "regulation": regulation }
                    }
        user_contribution.append(new_info)
        with open('User_contribution.json', 'w') as f:
            json.dump(user_contribution, f, indent = 4, ensure_ascii=False)
        # return f"new contribution : {user_contribution}"

        #return "❌ Species data is unavailable or not registered yet in our database."


def trigger_sos(fisher_id, lat, lon):
    """Pushes a validation event to the land-based JSON command repository."""
    if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
        raise ValueError("Invalid geographic coordinates.")

    maps_link = f"https://www.google.com/maps?q={lat},{lon}"

    new_incident = {
        "fisher_id": fisher_id,
        "latitude": lat,
        "longitude": lon,
        "map_anchor": maps_link,
        "status": "UNRESOLVED / ACTIVE "
    }

    repository_data = read_shore_alerts()
    repository_data.append(new_incident)

    with open("sos_repository.json", "w", encoding="utf-8") as file:
        json.dump(repository_data, file, indent=4)

    return f"\n🚨 TRANSMISSION LOCKOUT PROCESSED 🚨\nData dropped securely inside the Shore Command Base repository.\nLink generated for Rescue Crews: {maps_link}"


def read_shore_alerts():
    """Helper method to parse current state of the land-based data repository safely."""
    try:
        with open("sos_repository.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


if __name__ == "__main__":
    main()