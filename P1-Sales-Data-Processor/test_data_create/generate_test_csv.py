import os
import csv
import random
import time
import threading
from datetime import datetime, timedelta

# --- CONFIGURATION ---
INTERVAL_SECONDS = 30     # ⏱ Time gap between file generations (now every 30 seconds)
ROWS_PER_FILE = 100       # Rows per CSV
START_DATE = datetime(2025, 11, 1)

# --- REALISTIC PRODUCT CATALOG ---
PRODUCTS = [
    "Samsung 55-inch LED TV",
    "LG Smart Refrigerator",
    "Apple iPhone 15",
    "OnePlus Nord CE 5G",
    "Sony Noise-Cancelling Headphones",
    "Dell Inspiron Laptop",
    "HP Pavilion Laptop",
    "Xiaomi Mi 11 Mobile",
    "Whirlpool Washing Machine",
    "Bosch Dishwasher",
    "Panasonic Microwave Oven",
    "Philips Air Purifier",
    "Bajaj Mixer Grinder",
    "LG Air Conditioner",
    "Haier Deep Freezer",
    "Canon DSLR Camera",
    "Lenovo Tablet",
    "Boat Bluetooth Speaker",
    "Samsung Galaxy Watch",
    "Apple iPad Air"
]

# --- RESOLVE PROJECT PATH ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "data", "in")

# --- ENSURE DIRECTORY EXISTS ---
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- CONTROL FLAG ---
stop_flag = threading.Event()

# --- HELPER FUNCTION ---
def generate_random_sales_row():
    """Return one row of fake sales data."""
    date = (START_DATE + timedelta(days=random.randint(0, 29))).strftime("%Y-%m-%d")
    product = random.choice(PRODUCTS)
    quantity = random.randint(1, 10)
    price = random.uniform(5000, 150000)  # more realistic price range
    return [date, product, quantity, f"{price:.2f}"]

def create_single_csv_file():
    """Generate one CSV file with timestamp in name."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sales_auto_{timestamp}.csv"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Product", "Quantity", "Price"])  # header
        for _ in range(ROWS_PER_FILE):
            writer.writerow(generate_random_sales_row())

    print(f"✅ Created: {filepath} ({ROWS_PER_FILE} rows)")

# --- MAIN GENERATOR LOOP ---
def run_generator():
    print(f"📁 Output folder: {OUTPUT_DIR}")
    print(f"🕒 A new CSV file will be generated every {INTERVAL_SECONDS} second(s).")
    print("💡 Type 'stop' and press ENTER to stop the program safely.\n")

    while not stop_flag.is_set():
        create_single_csv_file()
        for _ in range(INTERVAL_SECONDS):
            if stop_flag.is_set():
                break
            time.sleep(1)
    print("🛑 CSV generator stopped gracefully.")

# --- LISTEN FOR STOP COMMAND ---
def listen_for_stop():
    """Wait for the user to type 'stop' to end the program."""
    while True:
        user_input = input().strip().lower()
        if user_input in ("stop", "exit", "quit"):
            stop_flag.set()
            break

# --- ENTRY POINT ---
if __name__ == "__main__":
    # Start the listener in a separate thread
    listener_thread = threading.Thread(target=listen_for_stop, daemon=True)
    listener_thread.start()

    # Start the generator
    run_generator()
