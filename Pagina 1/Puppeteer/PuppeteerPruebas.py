import asyncio
import os
from pyppeteer import launch

desktop_path = r"C:\Users\Hary Tatiana\Desktop"


async def iniciar_browser():
    browser = await launch(
        headless=False,
        executablePath=r"C:\Program Files\Google\Chrome\Application\Chrome.exe" 
    )
    page = await browser.newPage()
    await page.setViewport({'width': 1280, 'height': 800})
    return browser, page


async def test_login_exitoso():
    browser, page = await iniciar_browser()
    await page.goto("https://the-internet.herokuapp.com/login")

    await page.type("#username", "tomsmith")
    await page.type("#password", "SuperSecretPassword!")

    
    await asyncio.gather(
        page.click("button.radius"),
        page.waitForNavigation(waitUntil="load")   
    )

    
    await page.waitForSelector("#flash", timeout=5000)

    mensaje = await page.evaluate("document.querySelector('#flash').textContent")
    print("TC01 Login exitoso", mensaje.strip())

    ruta = os.path.join(desktop_path, "TC01_login_exitoso.png")
    await page.screenshot({'path': ruta})
    print("Captura guardada en:", ruta)
    await browser.close()

async def test_login_usuario_invalido():
    browser, page = await iniciar_browser()
    await page.goto("https://the-internet.herokuapp.com/login")

    await page.type("#username", "tonsmith")
    await page.type("#password", "SuperSecretPassword!")
    await page.click("button.radius")
    await page.waitForSelector("#flash")

    mensaje = await page.evaluate("document.querySelector('#flash').textContent")
    print("TC02 Usuario inválido", mensaje.strip())
    ruta = os.path.join(desktop_path, "TC02_usuario_invalido.png")
    await page.screenshot({'path': ruta})
    print("Captura guardada en:", ruta)
    await browser.close()

async def test_login_contrasena_invalida():
    browser, page = await iniciar_browser()
    await page.goto("https://the-internet.herokuapp.com/login")

    await page.type("#username", "tomsmith")
    await page.type("#password", "12345")
    await page.click("button.radius")
    await page.waitForSelector("#flash")

    mensaje = await page.evaluate("document.querySelector('#flash').textContent")
    print("TC03 Contraseña inválida", mensaje.strip())
    ruta = os.path.join(desktop_path, "TC03_contrasena_invalida.png")
    await page.screenshot({'path': ruta})
    print("Captura guardada en:", ruta)
    await browser.close()

async def test_logout():
    browser, page = await iniciar_browser()
    await page.goto("https://the-internet.herokuapp.com/login")

    await page.type("#username", "tomsmith")
    await page.type("#password", "SuperSecretPassword!")

    
    await asyncio.gather(
        page.click("button.radius"),
        page.waitForNavigation(waitUntil="load")
    )

    
    await asyncio.gather(
        page.click("a.button"),
        page.waitForNavigation(waitUntil="load")
    )

   
    await page.waitForSelector("#flash", timeout=5000)

    mensaje = await page.evaluate("document.querySelector('#flash').textContent")
    print("TC04 Logout", mensaje.strip())

    ruta = os.path.join(desktop_path, "TC04_logout.png")
    await page.screenshot({'path': ruta})
    print("Captura guardada en:", ruta)
    await browser.close()


async def main():
    await test_login_exitoso()
    await test_login_usuario_invalido()
    await test_login_contrasena_invalida()
    await test_logout()

if __name__ == "__main__":
    asyncio.run(main())   

