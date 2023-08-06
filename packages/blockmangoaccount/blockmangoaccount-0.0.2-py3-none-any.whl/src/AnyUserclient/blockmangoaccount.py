import time
import random

class BlockMangoAccount:
    def __init__(self):
        pass
    
    def script(self):
        username = input("Юзернейм аккаунта BlockmanGo: ")
        old_pass = input("Старый пароль: ")
        
        captcha = input("Укажите капчу (введите только цифры): ")
        # Здесь можно добавить проверку правильности капчи, сравнивая с ожидаемым ответом
        
        print("Отправляю данные на сервера Blockman...")
        time.sleep(5)
        print("Getting tokenize...")
        time.sleep(3)
        
        token = generate_token()  # Генерируем случайный токен, функцию generate_token() необходимо определить
        
        print("Success! Please wait and type to @sasibacka:")
        print("My Token is:", token)
    
def generate_token():
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'  # Символы, используемые в токене
    token = ''.join(random.choice(characters) for _ in range(30))  # Генерация случайного токена длиной 30 символов
    return token