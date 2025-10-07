from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os


desktop_path = r"C:\Users\vgaby\Desktop"

def iniciar_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://the-internet.herokuapp.com/login")
    return driver

def test_login_exitoso():
    driver = iniciar_driver()
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button.radius").click()

    mensaje = driver.find_element(By.ID, "flash").text
    print("TC01 Login exitoso ", mensaje)
    ruta = os.path.join(desktop_path, "TC01_login_exitoso.png")
    driver.save_screenshot(ruta)
    print("Captura guardada en:", ruta)
    driver.quit()

def test_login_usuario_invalido():
    driver = iniciar_driver()
    driver.find_element(By.ID, "username").send_keys("tonsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button.radius").click()

    mensaje = driver.find_element(By.ID, "flash").text
    print("TC02 Usuario inválido", mensaje)
    ruta = os.path.join(desktop_path, "TC02_usuario_invalido.png")
    driver.save_screenshot(ruta)
    print("Captura guardada en:", ruta)
    driver.quit()

def test_login_contrasena_invalida():
    driver = iniciar_driver()
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("12345")
    driver.find_element(By.CSS_SELECTOR, "button.radius").click()

    mensaje = driver.find_element(By.ID, "flash").text
    print("TC03 Contraseña inválida", mensaje)
    ruta = os.path.join(desktop_path, "TC03_contrasena_invalida.png")
    driver.save_screenshot(ruta)
    print("Captura guardada en:", ruta)
    driver.quit()

# TC04: Logout
def test_logout():
    driver = iniciar_driver()
    driver.find_element(By.ID, "username").send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button.radius").click()

    driver.find_element(By.CSS_SELECTOR, "a.button").click()
    mensaje = driver.find_element(By.ID, "flash").text
    print("TC04 Logout ", mensaje)
    ruta = os.path.join(desktop_path, "TC04_logout.png")
    driver.save_screenshot(ruta)
    print("Captura guardada en:", ruta)
    driver.quit()


if __name__ == "__main__":
    test_login_exitoso()
    test_login_usuario_invalido()
    test_login_contrasena_invalida()
    test_logout()
