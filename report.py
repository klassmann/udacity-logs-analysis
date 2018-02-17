
import psycopg2

CONNECTION_STRING = 'dbname=news user='

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
        self.cursor.fetchall()

    def fetchone(self):
        self.cursor.fetchone()

    def __del__(self):
        self.connection.close()



class Report(object):
    def __init__(self):
        self.db = Database(CONNECTION_STRING)
        
    def top_articles(self):
        query_top_articles = """
        SELECT slug, qtd FROM articles a INNER JOIN 
                (SELECT path, count(*) AS qtd FROM log GROUP BY path) AS l 
                ON '/article/' || a.slug = l.path
            ORDER BY qtd DESC
            LIMIT 3;
        """

    def top_authors(self):
        pass

    def top_requests_with_errors(self):
        pass

    def get_report(self):
        pass


if __name__ == '__main__':
    report = Report()