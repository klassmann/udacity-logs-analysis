#!/usr/bin/env python3

import os
from datetime import datetime
from datetime import time

try:
    import psycopg2
except:
    print("You need to install the dependencies from requirements.txt")
    exit(-1)

CONNECTION_STRING = 'dbname=news'


class Database(object):
    """
    Database helper class
    Use this to handle the connection and query execution
    """
    def __init__(self, conn_string):
        self.connection = psycopg2.connect(conn_string)

        if not self.connection:
            msg = 'Could not connect with PostgreSQL: {}'.format(conn_string)
            raise Exception(msg)

        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def query(self, sql):
        self.cursor.execute(sql)

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def __del__(self):
        self.connection.close()


class Report(object):
    """
    Report
    Main code for processing the data for the report
    """
    def __init__(self):
        self.db = Database(CONNECTION_STRING)

    def top_articles(self):
        sql_top_articles = self.__load_sql('top_articles.sql')
        self.db.query(sql_top_articles)
        results = self.db.fetchall()

        print("Top 3 articles:")
        for r in results:
            print('"{}" - {} views'.format(*r))

    def top_authors(self):
        sql_top_authors = self.__load_sql('top_authors.sql')
        self.db.query(sql_top_authors)
        results = self.db.fetchall()

        print('\nTop authors:')
        for r in results:
            print('{} - {} views'.format(*r))

    def _conv_date(self, d):
        dt = datetime.combine(d, time(0, 0, 0))
        fmt = dt.strftime('%B %d, %Y')
        return fmt

    def top_days_with_errors(self):
        sql_days_errors = self.__load_sql('days_with_errors.sql')
        self.db.query(sql_days_errors)
        results = self.db.fetchall()

        print('\nDays with more than 1% of requests with errors:')
        for r in results:
            dt = self._conv_date(r[0])
            perc = r[1]
            print('{} - {:.2}% errors'.format(dt, perc))

    def __load_sql(self, filename):
        content = ""
        with open(os.path.join('queries/', filename)) as f:
            content = f.read()
        return content

    def print_report(self):
        self.top_articles()
        self.top_authors()
        self.top_days_with_errors()


if __name__ == '__main__':
    report = Report()
    print('Log Analysis Report\n')
    report.print_report()
