
import psycopg2

CONNECTION_STRING = 'dbname=news'

class Database(object):
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
    def __init__(self):
        self.db = Database(CONNECTION_STRING)
        
    def top_articles(self):
        sql_top_articles = """
        SELECT title, qtd FROM articles a INNER JOIN 
                (SELECT path, count(*) AS qtd FROM log GROUP BY path) AS l 
                ON '/article/' || a.slug = l.path
            ORDER BY qtd DESC
            LIMIT 3;
        """
        self.db.query(sql_top_articles)
        results = self.db.fetchall()

        print("Top 3 articles:")
        for r in results:
            print('\t"{}" - {} views'.format(*r))

    def top_authors(self):
        sql_top_authors = """
            SELECT name, qtd FROM authors a INNER JOIN (
                SELECT author, count(*) as qtd FROM 
                    articles a INNER JOIN 
                        (SELECT path FROM log) AS l 
                        ON '/article/' || a.slug = l.path
                        GROUP BY author
                ) AS qry_article
                ON qry_article.author = a.id
                ORDER BY qtd DESC;
        """
        self.db.query(sql_top_authors)
        results = self.db.fetchall()

        print('Top authors:')
        for r in results:
            print('\t{} - {} views'.format(*r))

    def top_days_with_errors(self):
        sql_days_errors = """
        SELECT date(time) as dt, (100.0 * error_log.qtd / request_log.qtd) AS perc FROM log 
            JOIN (select date(time) AS de, count(*) AS qtd FROM log WHERE status != '200 OK' GROUP BY de) AS error_log
            ON date(log.time) = error_log.de
            JOIN (SELECT date(time) AS ds, count(*) AS qtd from log group by ds) AS request_log
            ON date(log.time) = request_log.ds
            WHERE ((100.0 * error_log.qtd) / request_log.qtd) > 1.0
            GROUP BY dt, perc;
        """
        self.db.query(sql_days_errors)
        results = self.db.fetchall()

        print('Days with more than 1% of requests with errors:')
        for r in results:
            print('\t{} - {:.2}% errors'.format(*r))

    def get_report(self):
        self.top_articles()
        self.top_authors()
        self.top_days_with_errors()


if __name__ == '__main__':
    report = Report()
    report.get_report()