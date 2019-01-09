# Logs Analysis 

The Logs Analysis project is a simple python script which generates the following 3 reports using the data present in tables in the **news** database:
- Most popular three articles of all time
- Most popular article authors of all time
- Which days did more than 1% of requests lead to errors

## Design of code
Python code is designed using 3 functions , with each function to generate each of the above mentioned report. The main function, calls all the 3 functions to generate all the reports by running the script once.

## Installation
Running the below command generates, the required reports
`python LogsAnalysisReport.py`

### Usage

For the above script to be working, following three views have to be created in the **news** database
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
       