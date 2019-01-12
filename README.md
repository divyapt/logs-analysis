# Logs Analysis 

The Logs Analysis project is a simple python script which generates the following 3 reports using the data present in tables in the **news** database:
- Most popular three articles of all time
- Most popular article authors of all time
- Which days did more than 1% of requests lead to errors

## Prerequisites
* VirtualBox and Vagrant
  For detailed information on setting up the Virtual Machine please visit [Installing the Virtual Machine](https://classroom.udacity.com/courses/ud197/lessons/3423258756/concepts/14c72fe3-e3fe-4959-9c4b-467cf5b7c3a0)
* Next, for downloading the news data and loading it into the db please visit here [Preparing the software and data](https://classroom.udacity.com/nanodegrees/nd004/parts/51200cee-6bb3-4b55-b469-7d4dd9ad7765/modules/c57b57d4-29a8-4c5f-9bb8-5d53df3e48f4/lessons/bc938915-0f7e-4550-a48f-82241ab649e3/concepts/a9cf98c8-0325-4c68-b972-58d5957f1a91)
* Execute the below queries in psql to create the required views in the **news** database:
```
create view total_articles_views as 
select substring(path,10) as article, count(*) as total_views 
       from log where status = '200 OK' 
       group by article 
       having substring(path,10) != '' 
       order by total_views;
```
```
create view total_requests_perday as 
select date_trunc('day', log.time) as "day" , count(*) as total_views 
       from log 
       group by 1 
       ORDER BY 1;
```
```
create view requests_perday_perstatus as 
select date_trunc('day', log.time) as "day" , status, count(*) as views 
       from log 
       group by 1,status 
       ORDER BY 1;
```       

## Deployment
Finally, after all the prerequisites are done, execute the below command generates, to generate the required reports
`python LogsAnalysisReport.py`

## Authors
* **Divya Tuduma**
       