from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

try:
    driver.get("https://www.instagram.com/reel/DAJY4zjRnAk/embed/")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "video"))
    )
    a = driver.find_element(By.TAG_NAME, "video")
    print(a.get_attribute("src"))
    driver.get("https://google.com")
    time.sleep(100)

finally:
    # driver.quit()
    pass