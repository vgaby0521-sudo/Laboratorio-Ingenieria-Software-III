from playwright.sync_api import sync_playwright

def run_tests():
    desktop_path = "C:/Users/vgaby/Desktop/" 

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()


        page.goto("https://the-internet.herokuapp.com/login")
        page.fill("#username", "tomsmith")
        page.fill("#password", "SuperSecretPassword!")
        page.click("button.radius")

        mensaje_tc01 = page.text_content("#flash")
        print("\n[TC01 Login válido] Resultado:", mensaje_tc01.strip())
        page.screenshot(path=desktop_path + "TC01_login_valido.png")


        page.goto("https://the-internet.herokuapp.com/login")
        page.fill("#username", "tonsmith") 
        page.fill("#password", "SuperSecretPassword!")
        page.click("button.radius")

        mensaje_tc02 = page.text_content("#flash")
        print("[TC02 Usuario inválido] Resultado:", mensaje_tc02.strip())
        page.screenshot(path=desktop_path + "TC02_usuario_invalido.png")

        page.goto("https://the-internet.herokuapp.com/login")
        page.fill("#username", "tomsmith")
        page.fill("#password", "12345")  
        page.click("button.radius")

        mensaje_tc03 = page.text_content("#flash")
        print("[TC03 Contraseña inválida] Resultado:", mensaje_tc03.strip())
        page.screenshot(path=desktop_path + "TC03_contrasena_invalida.png")

    
        page.goto("https://the-internet.herokuapp.com/login")
        page.fill("#username", "tomsmith")
        page.fill("#password", "SuperSecretPassword!")
        page.click("button.radius")

        page.click("a[href='/logout']")
        mensaje_tc04 = page.text_content("#flash")
        print("[TC04 Logout] Resultado:", mensaje_tc04.strip())
        page.screenshot(path=desktop_path + "TC04_logout.png")

        browser.close()

if __name__ == "__main__":
    run_tests()
