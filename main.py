from flask import Flask, jsonify, request, abort
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from functools import lru_cache

chrome_options = Options()
app = Flask(__name__)
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)

@lru_cache()
def fetch_ig_code(url):
    driver.get(url)
    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.TAG_NAME, "video"))
    )

    a = driver.find_element(By.TAG_NAME, "video")
    data = {"url": a.get_attribute("src")}

    return jsonify(data)

@app.route('/')
def home():
    return "Welcome to the Basic Flask Server!"

@app.route('/api/data', methods=['GET'])
def get_data():
    ig_code = request.args.get("url")
    url = f"https://www.instagram.com/reel/{ig_code}/embed/"

    try:
        data = fetch_ig_code(url)
        return data
    except Exception as e:
        print(e)
        abort(500)

if __name__ == '__main__':
    app.run(debug=False)