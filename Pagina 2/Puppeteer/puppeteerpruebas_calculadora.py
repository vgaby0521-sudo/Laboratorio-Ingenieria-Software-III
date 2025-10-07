import os
import time
import unittest
import asyncio
from pyppeteer import launch

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import logging
logging.getLogger("asyncio").setLevel(logging.CRITICAL)
logging.getLogger("websockets").setLevel(logging.CRITICAL)
logging.getLogger("pyppeteer").setLevel(logging.CRITICAL)


CAPTURA_DIR = r"C:\Users\valen\OneDrive\Documentos\Pruebas IngSoftware\CapturasPuppeteer"
os.makedirs(CAPTURA_DIR, exist_ok=True)


class TestCalculadoraPuppeteer(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        """Inicia el navegador antes de cada prueba"""
        self.browser = await launch(headless=False)
        self.page = await self.browser.newPage()
        await self.page.goto("https://testsheepnz.github.io/BasicCalculator.html")
        await asyncio.sleep(1)

    async def asyncTearDown(self):
        """Cierra el navegador después de cada prueba"""
        await self.browser.close()

    async def ingresar_datos(self, num1, num2, operacion, nombre_captura, esperado=None, descripcion=""):
        """Rellena datos, ejecuta operación, toma captura y retorna resultado"""
        page = self.page


        await page.evaluate('''() => {
            document.querySelector("#number1Field").value = "";
            document.querySelector("#number2Field").value = "";
        }''')

   
        await page.type("#number1Field", str(num1))
        await page.type("#number2Field", str(num2))

     
        opciones = {
            "Add": "0",
            "Subtract": "1",
            "Multiply": "2",
            "Divide": "3",
            "Concatenate": "4"
        }
        await page.select("#selectOperationDropdown", opciones[operacion])


        await page.click("#calculateButton")
        await asyncio.sleep(1)

 
        resultado = await page.evaluate('''() => document.querySelector("#numberAnswerField").value''')

  
        if isinstance(esperado, list):
            passed = any(e in resultado for e in esperado)
        else:
            passed = resultado == esperado

        estado = "PASS" if passed else "FAIL"

 
        ruta_captura = os.path.join(CAPTURA_DIR, f"{nombre_captura}.png")
        await page.screenshot({'path': ruta_captura})
        print(f"{nombre_captura} - {descripcion}: {resultado} - {estado}")
        print(f"Captura guardada: {ruta_captura}\n")

    
        await page.click("#clearButton")

        return resultado


    async def test_suma_valida(self):
        await self.ingresar_datos(5, 3, "Add", "TC01a_suma_valida", "8", "Suma válida (5 + 3)")

    async def test_suma_invalida(self):
        await self.ingresar_datos("a", 3, "Add", "TC01b_suma_invalida", "", "Suma inválida (a + 3)")

    async def test_suma_negativos(self):
        await self.ingresar_datos(-5, 10, "Add", "TC01c_suma_negativos", "5", "Suma con negativos (-5 + 10)")

    async def test_suma_decimales_valida(self):
        await self.ingresar_datos(2.5, 3.5, "Add", "TC01d_suma_decimales_valida", "6", "Suma decimales válida (2.5 + 3.5)")

    async def test_suma_decimales_invalida(self):
        await self.ingresar_datos("2,5", 3, "Add", "TC01e_suma_decimales_invalida", "", "Suma decimales inválida (2,5 + 3)")

  
    async def test_resta_valida(self):
        await self.ingresar_datos(10, 7, "Subtract", "TC02a_resta_valida", "3", "Resta válida (10 - 7)")

    async def test_resta_invalida(self):
        await self.ingresar_datos("b", 7, "Subtract", "TC02b_resta_invalida", "", "Resta inválida (b - 7)")

    async def test_resta_negativo(self):
        await self.ingresar_datos(7, 10, "Subtract", "TC02c_resta_negativo", "-3", "Resta resultado negativo (7 - 10)")

    async def test_resta_decimales_valida(self):
        await self.ingresar_datos(10.5, 7.2, "Subtract", "TC02d_resta_decimales_valida", ["3.3", "3.299"], "Resta decimales válida (10.5 - 7.2)")

    async def test_resta_decimales_invalida(self):
        await self.ingresar_datos("10,5", "7,2", "Subtract", "TC02e_resta_decimales_invalida", "", "Resta decimales inválida (10,5 - 7,2)")

    async def test_resta_mixta(self):
        await self.ingresar_datos("10,5", "7.2", "Subtract", "TC02f_resta_mixta", "", "Resta decimales inválida (10,5 - 7.2)")

 
    async def test_multiplicacion_valida(self):
        await self.ingresar_datos(4, 5, "Multiply", "TC03a_multiplicacion_valida", "20", "Multiplicación válida (4 × 5)")

    async def test_multiplicacion_invalida(self):
        await self.ingresar_datos("c", 5, "Multiply", "TC03b_multiplicacion_invalida", "", "Multiplicación inválida (c × 5)")

    async def test_multiplicacion_cero(self):
        await self.ingresar_datos(0, 7, "Multiply", "TC03c_multiplicacion_cero", "0", "Multiplicación con cero (0 × 7)")

    async def test_multiplicacion_negativos(self):
        await self.ingresar_datos(-3, 5, "Multiply", "TC03d_multiplicacion_negativos", "-15", "Multiplicación con negativos (-3 × 5)")

    async def test_multiplicacion_decimales_valida(self):
        await self.ingresar_datos("2.5", 2, "Multiply", "TC03e_multiplicacion_decimales_valida", "5", "Multiplicación decimales válida (2.5 × 2)")

    async def test_multiplicacion_decimales_invalida(self):
        await self.ingresar_datos("2,5", 2, "Multiply", "TC03f_multiplicacion_decimales_invalida", "", "Multiplicación decimales inválida (2,5 × 2)")

 
    async def test_division_valida(self):
        await self.ingresar_datos(9, 3, "Divide", "TC04a_division_valida", "3", "División válida (9 ÷ 3)")

    async def test_division_por_cero(self):
        await self.ingresar_datos(9, 0, "Divide", "TC04b_division_por_cero", "", "División por cero (9 ÷ 0)")

    async def test_division_negativa(self):
        await self.ingresar_datos(-9, 3, "Divide", "TC04c_division_negativa", "-3", "División negativa (-9 ÷ 3)")

    async def test_division_decimales_valida(self):
        await self.ingresar_datos("9.0", "4.5", "Divide", "TC04d_division_decimales_valida", "2", "División válida (9.0 ÷ 4.5)")

    async def test_division_decimales_invalida(self):
        await self.ingresar_datos("9,0", "4,5", "Divide", "TC04e_division_decimales_invalida", "", "División decimales inválida (9,0 ÷ 4,5)")

    async def test_division_cero_cero(self):
        await self.ingresar_datos(0, 0, "Divide", "TC04f_division_cero_cero", "", "División negativa (0 ÷ 0)")

  
    async def test_concatenacion_valida(self):
        await self.ingresar_datos("12", "34", "Concatenate", "TC09a_concatenacion_valida", "1234", "Concatenación válida (12 & 34)")

    async def test_concatenacion_decimales_punto(self):
        await self.ingresar_datos("1.5", "2", "Concatenate", "TC09b_concatenacion_decimales_punto", "1.52", "Concatenación con decimales punto (1.5 & 2)")

    async def test_concatenacion_coma(self):
        await self.ingresar_datos("1,5", "2", "Concatenate", "TC09c_concatenacion_coma", "1,52", "Concatenación con coma (1,5 & 2)")

    async def test_concatenacion_invalida(self):
        await self.ingresar_datos("12", "b", "Concatenate", "TC09d_concatenacion_invalida", "12b", "Concatenación inválida (12 & b)")


if __name__ == "__main__":
    unittest.main()
