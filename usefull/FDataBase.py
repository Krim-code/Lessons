import math
import sqlite3
import time
import re
from flask import url_for


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res: return res
        except:
            print("Error get data from DataBase")
        return []

    def addPost(self,title,text,url):
        try:
            self.__cur.execute("SELECT COUNT() as `count` FROM posts WHERE url LIKE ?",(url,))
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Статья с данным url уже есть!")
                return False

            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO posts VALUES(NULL,?,?,?,?)",(title,text,url,tm))
            self.__db.commit()
        except:
            print("Error adding post")
            return False
        return True

    def getPost(self, alias):
        try:
            self.__cur.execute(f"SELECT title,text FROM posts WHERE url LIKE ? LIMIT 1",(alias,))
            res = self.__cur.fetchone()
            if res:
                base = url_for('static', filename = "img")
                text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
        "\\g<tag>"+base+"/\\g<url>>",
        res['text'])
                return (res['title'], text)

        except sqlite3.Error as e:
            print(f"Ошибка при получении поста из БД {e}")

        return (False,False)

    def getPostAnonce(self):
        try:
            self.__cur.execute(f"SELECT id,title,text,url FROM posts ORDER BY time DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print(f"Ошибка при получении постов из БД {e}")

        return []
