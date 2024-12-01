import heapq
from flask import Flask, jsonify, request, abort, g
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from flask_cors import CORS
import time

from functools import lru_cache

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")

MAX_DRIVERS = 5
id_c = 0
drivers = []

@app.before_request
def start_timer():
    """Start the timer before the request is processed."""
    g.start_time = time.time()

@app.after_request
def log_request_time(response):
    """Log the request processing time after the request is processed."""
    if hasattr(g, 'start_time'):
        duration = time.time() - g.start_time
        print(f"Request processing time: {duration:.4f} seconds")
    return response

def get_driver():
    global drivers
    global id_c
    if len(drivers) > MAX_DRIVERS:
        drivers = [x for x in drivers if time.time() - x[1] > 60]
        heapq.heapify(drivers)
    elif len(drivers) == 0:
        heapq.heappush(drivers, (id_c, time.time(), webdriver.Chrome(options=chrome_options)))
        id_c += 1
    
    return heapq.heappop(drivers)

@lru_cache()
def fetch_ig_code(url):
    global drivers
    id, _, driver = get_driver()
    driver.get(url)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )

        a = driver.find_element(By.TAG_NAME, "video")
        data = {"url": a.get_attribute("src")}
        heapq.heappush(drivers, (id, time.time(), driver))
        return jsonify(data), not a
    except:
        heapq.heappush(drivers, (id, time.time(), driver))
        return {}, True

@app.route("/api/data", methods=["GET"])
def get_data():
    ig_code = request.args.get("url")
    url = f"https://www.instagram.com/reel/{ig_code}/embed/"

    data, error = fetch_ig_code(url)

    if error:
        abort(500)
    return data


if __name__ == "__main__":
    app.run(debug=False)
