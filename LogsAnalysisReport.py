#!/usr/bin/env python2.7

from datetime import datetime
import psycopg2

DBNAME = "news"


def execute_query(query):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    return c.fetchall()


def get_top_three_articles():
    """ Return top 3 articles of all time """
    articles = execute_query("""select articles.title, count(*) as total_views
              from log, articles
              where substring(log.path,10)=articles.slug
                    and status = '200 OK'
              group by articles.title
              order by total_views desc""")
    for name, views in articles:
        print("\"{}\" - {} views".format(name, views))


def get_popular_authors():
    """ Return top 3 articles of all time """
    authors = execute_query("""select authors.name,
               sum(tav.total_views) as tot_views
               from articles, authors, total_articles_views as tav
               where articles.slug=tav.article
                     and articles.author=authors.id
               group by authors.id order by tot_views desc;""")
    for name, views in authors:
        print("{} - {} views".format(name, views))


def get_days_with_most_errors():
    """ Return days with more than 1% of requests lead to errors """
    days_with_errors = execute_query("""select to_char(a.day, 'Mon DD, YYYY'),
                 round(a.views*100.00/b.total_views, 1) as error_rate
                 from requests_perday_perstatus as a,total_requests_perday as b
                 where a.day=b.day
                       and status='404 NOT FOUND'
                       and ((a.views/cast(b.total_views as float))*100.0)>=1;
                 """)
    for day, error_rate in days_with_errors:
        print("{} - {}% errors".format(day, error_rate))


if __name__ == '__main__':
    print("******Most popular articles******")
    get_top_three_articles()
    print("\n******Most popular article authors******")
    get_popular_authors()
    print("""\n******Days with more than 1%
         of requests that lead to errors******""")
    get_days_with_most_errors()