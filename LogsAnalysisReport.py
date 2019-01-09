from datetime import datetime
import psycopg2

DBNAME = "news"


def get_top_three_articles():
    """ Return top 3 articles of all time """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select articles.title, count(*) as total_views from log, articles
              where substring(log.path,10)=articles.slug
                    and status = '200 OK'
              group by articles.title
              order by total_views desc""")
    articles = c.fetchall()
    for article in articles:
        name, views = article
        print("\"{}\" - {} views".format(name, views))


def get_popular_authors():
    """ Return top 3 articles of all time """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select authors.name, sum(tav.total_views) as tot_views
               from articles, authors, total_articles_views as tav
               where articles.slug=tav.article
                     and articles.author=authors.id
               group by authors.id order by tot_views desc;""")
    authors = c.fetchall()
    for author in authors:
        name, views = author
        print("{} - {} views".format(name, views))


def get_days_with_most_errors():
    """ Return days with more than 1% of requests lead to errors """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""select a.day, (a.views/cast(b.total_views as float))*100.0 as error_rate
                 from requests_perday_perstatus as a,total_requests_perday as b
                 where a.day=b.day
                       and status='404 NOT FOUND'
                       and ((a.views/cast(b.total_views as float))*100.0)>=1;
              """)
    days_with_errors = c.fetchall()
    for day_with_error in days_with_errors:
        day, error_rate = day_with_error
        print("{} - {}% errors".format(datetime.strftime(day, '%B %d, %Y'),
                                       round(error_rate, 1)))


if __name__ == '__main__':
    print("******Most popular articles******")
    get_top_three_articles()
    print("\n******Most popular article authors******")
    get_popular_authors()
    print("""\n******Days with more than 1%
          of requests that lead to errors******""")
    get_days_with_most_errors()
