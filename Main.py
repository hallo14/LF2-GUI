import tkinter as tk
from tkinter import ttk
import random
import time

RANGES = {
    "Last 24 Hours": {
        "energy_used": (10, 50),
        "avg_battery_charge": (20, 100), 
        "distance_traveled": (5, 50), 
        "scooters_used": (1, 20), 
        "revenue_via_distance": (20, 500),
        "revenue_via_time": (10, 400),  
    },
    "Last 30 Days": {
        "energy_used": (300, 1000),
        "avg_battery_charge": (40, 80),
        "distance_traveled": (100, 500),
        "scooters_used": (50, 100),
        "revenue_via_distance": (1000, 5000),
        "revenue_via_time": (500, 4000),
    },
    "Last 365 Days": {
        "energy_used": (1000, 10000),
        "avg_battery_charge": (50, 70),
        "distance_traveled": (1000, 10000),
        "scooters_used": (500, 2000),
        "revenue_via_distance": (5000, 20000),
        "revenue_via_time": (4000, 15000),
    }
}


current_blinds_position = 50
sunlight_change = 5000

def get_random_electricity_price():
    return round(random.uniform(0.10, 0.30), 2)

def generate_random_stats(timeframe):
    return {
        "energy_used": f"{random.uniform(*RANGES[timeframe]['energy_used']):.2f} kWh",
        "avg_battery_charge": f"{random.randint(*RANGES[timeframe]['avg_battery_charge'])}%",
        "distance_traveled": f"{random.uniform(*RANGES[timeframe]['distance_traveled']):.2f} km",
        "scooters_used": random.randint(*RANGES[timeframe]['scooters_used']),
        "revenue_via_distance": f"${random.uniform(*RANGES[timeframe]['revenue_via_distance']):.2f}",
        "revenue_via_time": f"${random.uniform(*RANGES[timeframe]['revenue_via_time']):.2f}",
    }

def get_sunlight_and_blinds():
    global current_blinds_position, sunlight_change

    sunlight_change += random.randint(-20, 10)
    current_sunlight = max(100, abs(10000 - abs(sunlight_change % 20000)))

    target_blinds_position = min(100, max(0, int((current_sunlight - 1000) / 90)))

    if current_blinds_position < target_blinds_position:
        current_blinds_position += 1  
    elif current_blinds_position > target_blinds_position:
        current_blinds_position -= 1

    return current_sunlight, current_blinds_position

root = tk.Tk()
root.title("E-Scooter Company Dashboard")
root.attributes("-fullscreen", True)
root.configure(bg="#F5F5F5")

root.bind("<Escape>", lambda e: root.destroy())

heading_font = ("Arial", 24, "bold")
section_font = ("Arial", 18, "bold")
stat_font = ("Arial", 14)

heading_label = tk.Label(root, text="E-Scooter Dashboard", font=heading_font, bg="#F5F5F5", fg="#333")
heading_label.pack(pady=20)

statistics_frame = ttk.LabelFrame(root, text="Statistics", padding=20)
statistics_frame.pack(fill="both", padx=40, pady=20, expand=True)


timeframes = ["Last 24 Hours", "Last 30 Days", "Last 365 Days"]
stats_labels = {}

for timeframe in timeframes:
    stats = generate_random_stats(timeframe)
    frame = ttk.Frame(statistics_frame, padding=10)
    frame.pack(fill="both", expand=True)
    
    ttk.Label(frame, text=f"{timeframe}:", font=section_font).grid(row=0, column=0, sticky="w", pady=10)
    
    # Statistic labels
    ttk.Label(frame, text=f"Energy Used: {stats['energy_used']}", font=stat_font).grid(row=1, column=0, sticky="w", padx=10)
    ttk.Label(frame, text=f"Average Battery Charge: {stats['avg_battery_charge']}", font=stat_font).grid(row=1, column=1, sticky="w", padx=10)
    ttk.Label(frame, text=f"Distance Traveled: {stats['distance_traveled']}", font=stat_font).grid(row=1, column=2, sticky="w", padx=10)
    ttk.Label(frame, text=f"Scooters Used: {stats['scooters_used']}", font=stat_font).grid(row=2, column=0, sticky="w", padx=10)
    ttk.Label(frame, text=f"Revenue via Distance: {stats['revenue_via_distance']}", font=stat_font).grid(row=2, column=1, sticky="w", padx=10)
    ttk.Label(frame, text=f"Revenue via Time: {stats['revenue_via_time']}", font=stat_font).grid(row=2, column=2, sticky="w", padx=10)

calculator_frame = ttk.LabelFrame(root, text="Ride Price Calculator", padding=20)
calculator_frame.pack(fill="both", padx=40, pady=20)

ttk.Label(calculator_frame, text="Distance (km):", font=stat_font).grid(row=0, column=0, sticky="w", padx=10, pady=5)
distance_entry = ttk.Entry(calculator_frame, width=10)
distance_entry.grid(row=0, column=1, padx=10)

ttk.Label(calculator_frame, text="Time (minutes):", font=stat_font).grid(row=1, column=0, sticky="w", padx=10, pady=5)
time_entry = ttk.Entry(calculator_frame, width=10)
time_entry.grid(row=1, column=1, padx=10)

electricity_cost = random.uniform(0.05, 0.25)

def calculate_price():
    global electricity_cost
    price_per_km = 0.50
    price_per_minute = 0.20
    
    distance = distance_entry.get()
    time = time_entry.get()
    cost = 0
    if distance:
        cost += float(distance) * price_per_km + (float(distance) * electricity_cost)
        time_entry.delete(0, tk.END)
    elif time:
        cost += float(time) * price_per_minute + (float(time) * electricity_cost)
    price_label.config(text=f"Calculated Price: ${cost:.2f}")

calculate_button = ttk.Button(calculator_frame, text="Calculate Price", command=calculate_price)
calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

price_label = ttk.Label(calculator_frame, text="Calculated Price: $0.00", font=section_font)
price_label.grid(row=3, column=0, columnspan=2, pady=10)


top_right_frame = tk.Frame(root, bg="#F5F5F5", padx=10, pady=10)
top_right_frame.place(relx=1.0, rely=0, anchor="ne")


def update_blinds():

    sunlight, blinds_position = get_sunlight_and_blinds()
    sunlight_label.config(text=f"Sunlight: {sunlight} lm")
    blinds_label.config(text=f"Blinds: {blinds_position}%")

    
    root.after(1500, update_blinds)

    
def update_time():

    current_time = time.strftime("%H:%M:%S")
    time_label.config(text=f"Time: {current_time}")
    
    root.after(1000, update_time)

time_label = ttk.Label(top_right_frame, text="Time: 00:00:00", font=("Arial", 14))
time_label.pack(anchor="ne")

sunlight_label = ttk.Label(top_right_frame, text="Sunlight: 0 lm", font=("Arial", 14))
sunlight_label.pack(anchor="ne")

blinds_label = ttk.Label(top_right_frame, text="Blinds: 0%", font=("Arial", 14))
blinds_label.pack(anchor="ne")


update_blinds()
update_time()


root.mainloop()
