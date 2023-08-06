from setuptools import setup

setup(
    name='gpassw',
    version='0.1.5',
    description='A very easy generator of passwords',
    packages=['gpassw'],
    author="barlin41k",
    author_email='sasaigrypocta@gmail.com',
    zip_safe=False,
    long_description='''# gpassw - генератор паролей!
`gpassw` - очень простой в использовании генератор паролей для Вашех потребностей.

# Минимальный пример использования
```python
from os import system
try: 
    from colorama import Style, Fore, init
    init()
except:
    system("pip install colorama")
    from colorama import Style, Fore, init
    init()
try: 
    from gpassw.functions import password
except:
    system("pip install gpassw")
    from gpassw.functions import password

name = input("Напиши своё имя: ")
print(f"Привет, {name}! Сейчас подберём для тебя оптимальный пароль...")
password = password.easy(10) #Генерация лёгкого пароля
print(f"Мы подобрали тебе пароль - {password}\nОкей?")
answer = input("Да/Нет: ")
if answer == "Да" or answer == "да":
    print("Теперь напиши пароль, который мы тебе подобрали для входа в аккаунт.")
else:
    raise SystemExit(1)
hello_password = input("Пароль: ")
while hello_password != password:
    print(Fore.RED + "Пароль неверный." + Style.RESET_ALL)
    hello_password = input("Пароль: ")
print("Вы успешно вошли!")
```

# Как установить?
Всего лишь требуеться просто прописать команду в консоли: `pip install gpassw`


    ''',
    long_description_content_type="text/markdown",
    )