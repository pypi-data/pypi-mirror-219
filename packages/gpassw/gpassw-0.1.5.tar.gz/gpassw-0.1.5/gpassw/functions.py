from os import system
try:
    import secrets
except:
    system("pip install secrets")
try:
    import string
except:
    system("pip install string")

class password:
    @staticmethod
    def easy(length: int):
        characters = string.ascii_letters
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    @staticmethod
    def medium(length: int):
        characters = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    @staticmethod
    def hard(length: int):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
