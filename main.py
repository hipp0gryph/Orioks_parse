from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import config
import time
import sqlite3

import spisok
import json


class DatabaseLoad:
    def __init__(self):
        self.db = sqlite3.connect('db.sqlite')

    def load(self, json):
        for obj in json:
            columns = []
            column = []
            for data in obj:
                print(data)
                column = list(data.keys())
            for col in column:
                if col not in columns:
                    columns.append(col)

            value = []
            values = []
            for data in obj:
                for i in columns:
                    value.append(str(dict(data).get(i)))
            values.append(list(value))
            value.clear()

            create_query = "create table if not exists myTable ({0})".format(" text,".join(columns))
            insert_query = "insert into myTable ({0}) values(?{1})".format(", ".join(columns), ",?" * (len(columns) - 1))
            c = self.db.cursor()
            c.execute(create_query)
            c.executemany(insert_query, values)
            values.clear()
            self.db.commit()
            c.close()


class OrioksParse:
    def __init__(self):
        self.d = {"Empty": []}
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.implicitly_wait(5)
        self.driver.get('https://orioks.miet.ru/user/login')
        element = self.driver.find_elements(By.CSS_SELECTOR, 'input')
        element[1].send_keys(config.login)
        element[2].send_keys(config.pas)
        time.sleep(2)
        element[2].submit()
        time.sleep(2)

    def __get_data(self, num):
        try:
            self.driver.get('https://orioks.miet.ru/portfolio/view-project?id_project=' + str(num))
            time.sleep(2)
            return self.driver.find_element(By.CSS_SELECTOR, "#forang").get_attribute("innerText")
        except:
            self.__get_data(num)

    def get_list_works(self, min, max):
        elements = list()
        for i in range(min, max + 1):
            elements.append(json.loads(self.__get_data(i)))
        return elements


if __name__ == "__main__":
    parser = OrioksParse()
    json = parser.get_list_works(0, 5)
    print(json)
    for i in json:
        print(i)
    loader = DatabaseLoad()
    loader.load(json)
