from selenium import webdriver
from selenium.webdriver.common.by import By  # Corregido
from selenium.webdriver.common.keys import Keys  # Corregido
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inicia el driver de Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://the-internet.herokuapp.com/login")
time.sleep(2)

# Encuentra los elementos de entrada para usuario y contraseña
user_input = driver.find_element(By.ID, "username")
passw_input = driver.find_element(By.ID, "password")
user_input.send_keys("tonsmith")  # aquí está el error a propósito
passw_input.send_keys("SuperSecretPassword!")

# Encuentra y hace clic en el botón de login
login_button = driver.find_element(By.CSS_SELECTOR, "button.radius")
login_button.click()
time.sleep(2)

# Verifica el mensaje de éxito o error
try:
    succes_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".flash.success"))
    ).text
    print("Login exitoso:", succes_message)
except:
    error_message = driver.find_element(By.CSS_SELECTOR, ".flash").text
    print("Login fallido:", error_message)

