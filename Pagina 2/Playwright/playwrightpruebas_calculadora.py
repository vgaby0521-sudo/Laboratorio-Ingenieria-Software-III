import os
import time
import unittest
from playwright.sync_api import sync_playwright


CAPTURA_DIR = r"C:\Users\valen\OneDrive\Documentos\Pruebas IngSoftware\CapturasPlay"
os.makedirs(CAPTURA_DIR, exist_ok=True)


class TestCalculadoraPlaywright(unittest.TestCase):

    def setUp(self):
        """Inicia el navegador antes de cada prueba"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.page.goto("https://testsheepnz.github.io/BasicCalculator.html")
        time.sleep(1)

    def tearDown(self):
        """Cierra el navegador después de cada prueba"""
        self.browser.close()
        self.playwright.stop()

    def ingresar_datos(self, num1, num2, operacion, nombre_captura, esperado=None, descripcion=""):

        """Rellena datos, ejecuta operación, toma captura y retorna resultado"""
        page = self.page

        page.fill("#number1Field", "")
        page.fill("#number2Field", "")

        page.fill("#number1Field", str(num1))
        page.fill("#number2Field", str(num2))

        opciones = {
            "Add": "0",
            "Subtract": "1",
            "Multiply": "2",
            "Divide": "3",
            "Concatenate": "4"
        }
        page.select_option("#selectOperationDropdown", opciones[operacion])

        page.click("#calculateButton")
        time.sleep(1)

        resultado = page.input_value("#numberAnswerField")

        if isinstance(esperado, list):
            passed = any(e in resultado for e in esperado)
        else:
            passed = resultado == esperado

        estado = "PASS " if passed else "FAIL "

        ruta_captura = os.path.join(CAPTURA_DIR, f"{nombre_captura}.png")
        page.screenshot(path=ruta_captura)

        print(f"{nombre_captura} - {descripcion}: {resultado} - {estado}")
        print(f"Captura guardada: {ruta_captura}\n")

        page.click("#clearButton")

        return resultado    



    def test_suma_valida(self):
        self.ingresar_datos(5, 3, "Add", "TC01a_suma_valida", "8", "Suma válida (5 + 3)")

    def test_suma_invalida(self):
        self.ingresar_datos("a", 3, "Add", "TC01b_suma_invalida", "", "Suma inválida (a + 3)")

    def test_suma_negativos(self):
        self.ingresar_datos(-5, 10, "Add", "TC01c_suma_negativos", "5", "Suma con negativos (-5 + 10)")

    def test_suma_decimales_valida(self):
        self.ingresar_datos(2.5, 3.5, "Add", "TC01d_suma_decimales_valida", "6", "Suma decimales válida (2.5 + 3.5)")

    def test_suma_decimales_invalida(self):
        self.ingresar_datos("2,5", 3, "Add", "TC01e_suma_decimales_invalida", "", "Suma decimales inválida (2,5 + 3)")



    def test_resta_valida(self):
        self.ingresar_datos(10, 7, "Subtract", "TC02a_resta_valida", "3", "Resta válida (10 - 7)")

    def test_resta_invalida(self):
        self.ingresar_datos("b", 7, "Subtract", "TC02b_resta_invalida", "", "Resta inválida (b - 7)")

    def test_resta_negativo(self):
        self.ingresar_datos(7, 10, "Subtract", "TC02c_resta_negativo", "-3", "Resta resultado negativo (7 - 10)")

    def test_resta_decimales_valida(self):
        self.ingresar_datos(10.5, 7.2, "Subtract", "TC02d_resta_decimales_valida", ["3.3", "3.299"], "Resta decimales válida (10.5 - 7.2)")

    def test_resta_decimales_invalida(self):
        self.ingresar_datos("10,5", "7,2", "Subtract", "TC02e_resta_decimales_invalida", "", "Resta decimales inválida (10,5 - 7,2)")
    
    def test_resta_mixta(self):
        self.ingresar_datos("10,5", "7.2", "Subtract", "TC02f_resta_mixta", "", "Resta decimales inválida (10,5 - 7.2)")



    def test_multiplicacion_valida(self):
        self.ingresar_datos(4, 5, "Multiply", "TC03a_multiplicacion_valida", "20", "Multiplicación válida (4 × 5)")

    def test_multiplicacion_invalida(self):
        self.ingresar_datos("c", 5, "Multiply", "TC03b_multiplicacion_invalida", "", "Multiplicación inválida (c × 5)")

    def test_multiplicacion_cero(self):
        self.ingresar_datos(0, 7, "Multiply", "TC03c_multiplicacion_cero", "0", "Multiplicación con cero (0 × 7)")

    def test_multiplicacion_negativos(self):
        self.ingresar_datos(-3, 5, "Multiply", "TC03d_multiplicacion_negativos", "-15", "Multiplicación con negativos (-3 × 5)")

    def test_multiplicacion_decimales_valida(self):
        self.ingresar_datos("2.5", 2, "Multiply", "TC03e_multiplicacion_decimales_valida", "5", "Multiplicación decimales valida (2.5 × 2)")

    def test_multiplicacion_decimales_invalida(self):
        self.ingresar_datos("2,5", 2, "Multiply", "TC03f_multiplicacion_decimales_invalida", "", "Multiplicación decimales invalida (2,5 × 2)")



    def test_division_valida(self):
        self.ingresar_datos(9, 3, "Divide", "TC04a_division_valida", "3", "División válida (9 ÷ 3)")

    def test_division_por_cero(self):
        self.ingresar_datos(9, 0, "Divide", "TC04b_division_por_cero", "", "División por cero (9 ÷ 0)")

    def test_division_negativa(self):
        self.ingresar_datos(-9, 3, "Divide", "TC04c_division_negativa", "-3", "División negativa (-9 ÷ 3)")

    def test_division_decimales_valida(self):
        self.ingresar_datos("9.0", "4.5", "Divide", "TC04d_division_decimales_valida", "2", "División válida (9.0 ÷ 4.5)")

    def test_division_decimales_invalida(self):
        self.ingresar_datos("9,0", "4,5", "Divide", "TC04e_division_decimales_invalida", "", "División por cero (9,0 ÷ 4,5)")

    def test_division_cero_cero(self):
        self.ingresar_datos(0, 0, "Divide", "TC04f_division_cero_cero", "", "División negativa (0 ÷ 0)")



    def test_concatenacion_valida(self):
        self.ingresar_datos("12", "34", "Concatenate", "TC09a_concatenacion_valida", "1234", "Concatenación válida (12 & 34)")

    def test_concatenacion_decimales_punto(self):
        self.ingresar_datos("1.5", "2", "Concatenate", "TC09b_concatenacion_decimales_punto", "1.52", "Concatenación con decimales punto (1.5 & 2)")

    def test_concatenacion_coma(self):
        self.ingresar_datos("1,5", "2", "Concatenate", "TC09c_concatenacion_coma", "1,52", "Concatenación con coma (1,5 & 2)")

    def test_concatenacion_invalida(self):
        self.ingresar_datos("12", "b", "Concatenate", "TC09d_concatenacion_invalida", "12b", "Concatenación inválida (12 & b)")


if __name__ == "__main__":
    unittest.main()
