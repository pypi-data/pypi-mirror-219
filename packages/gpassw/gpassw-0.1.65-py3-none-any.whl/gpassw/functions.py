from os import system
import gpassw.config as config
try:
    import secrets
except:
    system("pip install secrets")
    import secrets
try:
    import string
except:
    system("pip install string")
    import string
try:
    from password_strength import PasswordPolicy
except:
    system("pip install password_strength")
    from password_strength import PasswordPolicy
try:
    from colorama import Style, Fore, init
except:
    system("pip install colorama")
    from colorama import Style, Fore, init
init()

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
    @staticmethod
    def check(password: str):
        policy = PasswordPolicy.from_names(
            length=5,  # min length: 5
            uppercase=2,  # need min. 2 uppercase letters
            numbers=2,  # need min. 2 digits
            special=0,  # need min. 2 special characters
            nonletters=0,  # need min. 2 non-letter characters (digits, specials, anything)
        )
        results = policy.test(password)
        if len(results) < 2 or len(results) == 2:
            if config.debug:
                print(Fore.GREEN + "Пароль надёжный." + Style.RESET_ALL)
                return results
        else:
            if config.debug:
                print(Fore.RED + "Пароль ненадёжен." + Style.RESET_ALL)
                return results
        
