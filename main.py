from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import config
import time
from pymongo import MongoClient
from config import Config
import json
import asyncio


class Load:
    def __init__(self):
        config = Config()
        self.client = MongoClient(config["MONGO_DB"]["host"])
        self.db = self.client.get_database(config["MONGO_DB"]["db"])
        self.collection = self.db.get_collection(config["MONGO_DB"]["table"])

    def insert_many(self, data):
        self.collection.insert_many(data)


class OrioksParse:
    def __init__(self):
        self.loader = Load()
        self.d = {"Empty": []}
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(5)
        self.driver.get('https://orioks.miet.ru/user/login')
        element = self.driver.find_elements(By.CSS_SELECTOR, 'input')
        config = Config()
        element[1].send_keys(config['DEFAULT']['user'])
        element[2].send_keys(config['DEFAULT']['pass'])
        time.sleep(2)
        element[2].submit()
        time.sleep(2)

    def __get_data(self, num, check=0):
        self.driver.get('https://orioks.miet.ru/portfolio/view-project?id_project=' + str(num))
        try:
            return self.driver.find_element(By.CSS_SELECTOR, "#forang").get_attribute("innerText")
        except:
            time.sleep(1)
            check += 1
            if check == 3:
                return None
            self.__get_data(num, check)

    def parse(self, min, max):
        elements = list()
        for i in range(min, max + 1):
            data = self.__get_data(i)
            if data is not None:
                try:
                    elements.append(json.loads(data))
                    self.loader.insert_many(elements)
                except:
                    pass


if __name__ == "__main__":
    max = int(input("Enter max, please: "))
    min = int(input("Enter min, please: "))
    parser = OrioksParse()
    for i in range(min // 50, max // 50):
        parser.parse(50 * i, (50 * (i + 1) - 1))
        print(f"Iteration now: {i}.\nRows inserted: {50 * (i + 1)}")
