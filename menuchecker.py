import requests
import schedule
import time
from bs4 import BeautifulSoup

# List of URLs to check
MENU_URLS = [
    "https://usf.campusdish.com/en/locationsandmenus/tampa/thehub/",  
    "https://usf.campusdish.com/LocationsAndMenus/Tampa/JuniperDining" 
]
ITEM_TO_CHECK = "Mojo Pork" 

# Notification placeholder
def send_notification(message):
    print("Notification:", message)

# Function to check if the item is on the menu for each URL
def check_menu(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')
        
        menu_items = soup.find_all('div', class_='menu-item') #ill find this tmrw
        
        for item in menu_items:
            if ITEM_TO_CHECK.lower() in item.get_text().lower():
                send_notification(f"{ITEM_TO_CHECK} at {url} today")
                return
        
    except requests.RequestException as e:
        print(f"Failed {url}: {e}")

# Function to check all menus
def check_all_menus():
    for url in MENU_URLS:
        check_menu(url)

# Runs for lunch and dinner
schedule.every().day.at("10:45").do(check_all_menus)
schedule.every().day.at("4:45").do(check_all_menus)

while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute for scheduled tasks