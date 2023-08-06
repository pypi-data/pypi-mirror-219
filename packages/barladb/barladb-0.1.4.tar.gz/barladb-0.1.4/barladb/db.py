from barladb.classes import Json
from barladb import config
from os import system
import os
try:
    from colorama import Style, Fore, init
except:
    system("pip install colorama")
    from colorama import Style, Fore, init
init()
data = {

}

#get - получить
def get(filepath: str):
    try:
        data = Json.get(filepath)
        if config.debug:
            print("BarlaDB: " + Fore.GREEN + "Данные успешно были получены!" + Style.RESET_ALL)
        if data == {}:
            print("BarlaDB: " + Fore.YELLOW + "База данных пустая." + Style.RESET_ALL)
            return
        else:
            return data
    except:
        print("BarlaDB: " + Fore.RED + f"Базы данных {filepath} не существует!" + Style.RESET_ALL)
        return
#save - сохранить в БД
def save(filepath: str, data: str):
    try:
        Json.save(filepath, data)
        if config.debug:
            print("BarlaDB: " + Fore.GREEN + "Данные успешно были обновлены!" + Style.RESET_ALL)
        if data == None:
            print("BarlaDB: " + Fore.YELLOW + "Переменная с данными пуста." + Style.RESET_ALL)
        else:
            return
    except:
        print("BarlaDB: " + Fore.RED + f"Базы данных {filepath} не существует!" + Style.RESET_ALL)
        return
def create(filename: str):
    Json.save(filename, data)
    if config.debug:
        print("BarlaDB: " + Fore.GREEN + f"База данных {filepath} была успешно создана!" + Style.RESET_ALL)
def delete(filename: str):
  try:
    os.remove(f"{filename}.json")
    if config.debug:
      print("BarlaDB: " + Fore.GREEN + f"База данных {filepath} была успешно удалена!" + Style.RESET_ALL)
    else:
       return data
  except:
    print("BarlaDB: " + Fore.RED + f"Базы данных {filepath} не существует!" + Style.RESET_ALL)
    return