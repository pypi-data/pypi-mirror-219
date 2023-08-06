from os import system
try:
    import secrets
except:
    system("pip install secrets")
try:
    import string
except:
    system("pip install string")

class Password:
    @staticmethod
    def get(length):
        characters = string.ascii_letters
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password