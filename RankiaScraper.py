from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv

load_dotenv()

class RankiaScraper:
    URL = "https://www.rankia.com"
    LOGIN_URL = "https://www.rankia.com/login?destino_login=%2F"
    LOGOUT_URL = "https://www.rankia.com/logout?url=%2F"
    FORUM_URL = "https://www.rankia.com/foro/oro"

    def __init__(self):
        self.driver = self.open_browser()

    def open_browser(self):
        # Crea una instancia del navegador
        driver = webdriver.Chrome()
        return driver

    def login(self, username, password):
        self.driver.get(self.LOGIN_URL)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, "usuario_nick")))

        username_field = self.driver.find_element(By.ID, "usuario_nick")
        password_field = self.driver.find_element(By.ID, "usuario_password")
        login_button = self.driver.find_element(By.NAME, "commit")

        if username is None or password is None:
            print("ERROR: USERNAME or PASSWORD environment variable is not set.")
            return  # Exit the function if credentials are not available

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        # Esperar a ver si se redirige a la página principal o aparece un mensaje de error
        try:
            success_element = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CLASS_NAME, "rnk-MainHeader_Logo")
            ))
            return True, "El login fue correcto."
        except Exception as e:
            error_message_element = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "rnk-Flash-danger")))
            error_message = error_message_element.text
            return False, f"Error de login: {error_message}"
    
    def logout(self):
        self.driver.get(self.LOGOUT_URL)
        
    def get_usernames(self):
        self.driver.get(self.FORUM_URL)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "rnk-Section_ForumTopicUserName")))
        elements = self.driver.find_elements(By.CLASS_NAME, "rnk-Section_ForumTopicUserName")
        usernames = [element.text.lower().split(' |')[0].replace(' ', '-').replace('.', '-') for element in elements]
        unique_usernames = list(set(usernames))

        with open('usernames.txt', 'w') as file:
            for username in unique_usernames:
                file.write(username + '\n')

        return unique_usernames

    def send_message(self, username, subject, message):
        try:
            url = f'https://www.rankia.com/correo/{username}'
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(EC.url_contains(url))

            topic_field = self.driver.find_element(By.ID, "mail_entre_usuarios_asunto")
            message_field = self.driver.find_element(By.ID, "mail_entre_usuarios_cuerpo")

            topic_field.send_keys(subject)
            message_field.send_keys(message)

            send_button = self.driver.find_element(By.NAME, "commit")
            send_button.click()  # Ensure the send button is clicked

            text = 'Mensaje enviado'
            WebDriverWait(self.driver, 10).until(EC.text_to_be_present_in_element((By.XPATH, f"//*[contains(text(), '{text}')]"), text))

            return True, "Mensje enviado correctamente."
        except Exception as e:
            return False, f"Fallo el envio del mensaje: {str(e)}"
    
    def send_message_all(self, subject, message):
        with open("usernames.txt", "r", encoding="utf-8") as file:
            usernames = [line.strip() for line in file.readlines()]
            
            if not usernames:
                print("La lista de usuarios está vacía. Obteniendo nombres de usuario...")
                usernames = self.get_usernames()
            for username in usernames:
                success, message = self.send_message(username, subject, message)
                if success:
                    print(f"Mensaje enviado a {username}")
                else:
                    print(message)
                
    def print_saved_usernames(self):
        try:
            with open('usernames.txt', 'r') as file:
                usernames = file.readlines()
                print("Usernames:")
                for username in usernames:
                    print(username.strip())
        except FileNotFoundError:
            print("No se encontró el archivo de nombres de usuario.")

    def close_browser(self):
        # Cierra el navegador
        self.driver.quit()
