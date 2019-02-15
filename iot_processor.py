import threading
import pymysql
from configparser import ConfigParser


class IOTMsgProcessor(threading.Thread):

    def __init__(self, identifier, name, queue):
        threading.Thread.__init__(self)
        self.identifier = identifier
        self.name = name
        self.queue = queue

        # Global Configurations
        self.config = ConfigParser()
        self.config.read("server.config")

        try:
            self.db = pymysql.connect(host=self.config.get("db", "host"),
                                      port=self.config.getint("db", "port"),
                                      user=self.config.get("db", "user"),
                                      passwd=self.config.get("db", "pass"),
                                      db=self.config.get("db", "name"),
                                      charset=self.config.get("db", "char"))
            self.cursor = self.db.cursor()
        except:
            print("Fail to connect to database")

    def __del__(self):
        self.db.close()

    def run(self):
        while True:
            line = self.queue.get()
            self.proc(line)

    def proc(self, data_to_save):
        elements = str(data_to_save).split(":")

        # Access Database
        searchsql = self.replace_params(self.config.get("sql", "search"), "@PARAM@", elements[0])
        updatesql = self.replace_params(self.config.get("sql", "update"), "@PARAM@", elements[1], elements[0])
        insertsql = self.replace_params(self.config.get("sql", "insert"), "@PARAM@", elements[0], elements[1])

        self.cursor.execute(searchsql)

        if self.cursor.fetchone():
            try:
                self.cursor.execute(updatesql)
                self.db.commit()
            except:
                self.db.rollback()
        else:
            try:
                self.cursor.execute(insertsql)
                self.db.commit()
            except:
                self.db.rollback()

    def replace_params(self, line, mark, *params):
        for i in range(len(params)):
            line = str(line).replace(mark, params[i], 1)

        return line
