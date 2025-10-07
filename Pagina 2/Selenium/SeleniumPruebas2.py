import unittest
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


desktop_path = r"C:\Users\vgaby\Desktop"

class TestCalculadora(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get("https://testsheepnz.github.io/BasicCalculator.html")

    def tearDown(self):
        self.driver.quit()

    def ingresar_datos(self, first, second, operacion, nombre_captura):
        driver = self.driver
        driver.find_element(By.ID, "number1Field").clear()
        driver.find_element(By.ID, "number1Field").send_keys(first)

        driver.find_element(By.ID, "number2Field").clear()
        driver.find_element(By.ID, "number2Field").send_keys(second)

        select = Select(driver.find_element(By.ID, "selectOperationDropdown"))
        select.select_by_visible_text(operacion)

        driver.find_element(By.ID, "calculateButton").click()
        time.sleep(1)

        resultado = driver.find_element(By.ID, "numberAnswerField").get_attribute("value")

        ruta = os.path.join(desktop_path, f"{nombre_captura}.png")
        driver.save_screenshot(ruta)
        print(f"📸 Captura guardada en: {ruta} | Resultado mostrado: {resultado}")

        return resultado
    
    # SUMA

    def test_suma_valida(self):
        resultado = self.ingresar_datos("5", "3", "Add", "TC01_suma_valida")
        self.assertEqual(resultado, "8")

    def test_suma_invalida(self):
        resultado = self.ingresar_datos("a", "3", "Add", "TC01_suma_invalida")
        self.assertEqual(resultado, "")  

    def test_suma_negativos(self):
        resultado = self.ingresar_datos("-5", "10", "Add", "TC01_suma_negativos")
        self.assertEqual(resultado, "5")

    def test_suma_decimales_valida(self):
        resultado = self.ingresar_datos("2.5", "3.5", "Add", "TC01_suma_decimales_valida")
        self.assertEqual(resultado, "6")

    def test_suma_decimales_invalida(self):
        resultado = self.ingresar_datos("2,5", "3", "Add", "TC01_suma_decimales_invalida")
        self.assertEqual(resultado, "")  

  
    # RESTA
    def test_resta_valida(self):
        resultado = self.ingresar_datos("10", "7", "Subtract", "TC02_resta_valida")
        self.assertEqual(resultado, "3")

    def test_resta_invalida(self):
        resultado = self.ingresar_datos("b", "7", "Subtract", "TC02_resta_invalida")
        self.assertEqual(resultado, "") 

    def test_resta_resultado_negativo(self):
        resultado = self.ingresar_datos("7", "10", "Subtract", "TC02_resta_negativo")
        self.assertEqual(resultado, "-3")

    def test_resta_decimales_valida(self):
        resultado = self.ingresar_datos("10.5", "7.2", "Subtract", "TC02_resta_decimales_valida")
        self.assertEqual(resultado, "3.3")

    def test_resta_decimales_invalida(self):
        resultado = self.ingresar_datos("10,5", "7,2", "Subtract", "TC02_resta_decimales_invalida")
        self.assertEqual(resultado, "")  

    def test_resta_mixta(self):
        resultado = self.ingresar_datos("10,5", "7.2", "Subtract", "TC02_resta_mixta")
        self.assertEqual(resultado, "")  


   
    # MULTIPLICACIÓN

    def test_multiplicacion_valida(self):
        resultado = self.ingresar_datos("4", "5", "Multiply", "TC03_multiplicacion_valida")
        self.assertEqual(resultado, "20")

    def test_multiplicacion_invalida(self):
        resultado = self.ingresar_datos("c", "5", "Multiply", "TC03_multiplicacion_invalida")
        self.assertEqual(resultado, "")  

    def test_multiplicacion_cero(self):
        resultado = self.ingresar_datos("0", "7", "Multiply", "TC03_multiplicacion_cero")
        self.assertEqual(resultado, "0")

    def test_multiplicacion_negativos(self):
        resultado = self.ingresar_datos("-3", "5", "Multiply", "TC03_multiplicacion_negativos")
        self.assertEqual(resultado, "-15")

    def test_multiplicacion_decimales_valida(self):
        resultado = self.ingresar_datos("2.5", "2", "Multiply", "TC03_multiplicacion_decimales_valida")
        self.assertEqual(resultado, "5")

    def test_multiplicacion_decimales_invalida(self):
        resultado = self.ingresar_datos("2,5", "2", "Multiply", "TC03_multiplicacion_decimales_invalida")
        self.assertEqual(resultado, "")  

    
    # DIVISIÓN
    def test_division_valida(self):
        resultado = self.ingresar_datos("9", "3", "Divide", "TC04_division_valida")
        self.assertEqual(resultado, "3")

    def test_division_por_cero(self):
        resultado = self.ingresar_datos("9", "0", "Divide", "TC04_division_por_cero")
        self.assertEqual(resultado, "")  

    def test_division_negativa(self):
        resultado = self.ingresar_datos("-9", "3", "Divide", "TC04_division_negativa")
        self.assertEqual(resultado, "-3")

    def test_division_decimales_valida(self):
        resultado = self.ingresar_datos("9.0", "4.5", "Divide", "TC04_division_decimales_valida")
        self.assertEqual(resultado, "2")

    def test_division_decimales_invalida(self):
        resultado = self.ingresar_datos("9,0", "4,5", "Divide", "TC04_division_decimales_invalida")
        self.assertEqual(resultado, "")  

    def test_division_cero_cero(self):
        resultado = self.ingresar_datos("0", "0", "Divide", "TC04_division_cero_cero")
        self.assertEqual(resultado, "")  

  
    # CONCATENACIÓN
    def test_concatenacion_valida(self):
        resultado = self.ingresar_datos("12", "34", "Concatenate", "TC09_concatenacion_valida")
        self.assertEqual(resultado, "1234")

    def test_concatenacion_decimales_punto(self):
        resultado = self.ingresar_datos("1.5", "2", "Concatenate", "TC09_concatenacion_decimales_punto")
        self.assertEqual(resultado, "1.52")

    def test_concatenacion_coma(self):
        resultado = self.ingresar_datos("1,5", "2", "Concatenate", "TC09_concatenacion_coma")
        self.assertEqual(resultado, "1,52")

    def test_concatenacion_invalida(self):
        resultado = self.ingresar_datos("12", "b", "Concatenate", "TC09_concatenacion_invalida")
        self.assertEqual(resultado, "12b")  


if __name__ == "__main__":
    unittest.main()
