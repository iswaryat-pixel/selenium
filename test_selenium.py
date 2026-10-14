from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome()

try:
    page = (Path(__file__).parent / "index.html").resolve().as_uri()
    driver.get(page)

    username = driver.find_element(By.ID, "username")
    password = driver.find_element(By.ID, "password")
    login_button = driver.find_element(By.ID, "loginBtn")

    assert username.is_displayed()
    assert password.is_displayed()
    assert login_button.is_displayed()
    assert login_button.text == "Login"
    print("Interface testing: PASS")

    assert username.get_attribute("placeholder") == "Enter username"
    assert password.get_attribute("placeholder") == "Enter password"
    assert driver.find_element(By.CSS_SELECTOR, "label[for='username']").is_displayed()
    assert driver.find_element(By.CSS_SELECTOR, "label[for='password']").is_displayed()
    print("Usability testing: PASS")

    username.send_keys("testuser")
    password.send_keys("correct-password")
    login_button.click()

    WebDriverWait(driver, 5).until(lambda d: d.title == "Dashboard")
    assert "Login Successful" in driver.find_element(By.ID, "message").text
    print("Valid login testing: PASS")

    driver.get(page)
    driver.find_element(By.ID, "username").send_keys("testuser")
    driver.find_element(By.ID, "password").send_keys("wrong-password")
    driver.find_element(By.ID, "loginBtn").click()

    WebDriverWait(driver, 5).until(
        lambda d: d.find_element(By.ID, "error").text != ""
    )
    error = driver.find_element(By.ID, "error").text
    assert error == "Invalid username or password"

    print("Invalid login testing: PASS")
    print("All test cases passed")

finally:
    driver.quit()
