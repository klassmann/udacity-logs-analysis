# Logs Analysis
Report generator for Udacity FSWD Logs Analysis Project

## Requirements

- python 3
- PostgreSQL (I used the 10.2 version)
- psycopg2-binary >= 2.7.4
- [The news Database from Udacity](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)


## How to use this project
I assume that you have PostgreSQL and know how to restore the database.

### Clone this repository
You will need the **report.py** and the queries inside the **queries/** folder.

    $ git clone https://github.com/klassmann/udacity-logs-analysis.git

### Install the dependencies
    $ pip3 install -r requirements.txt

### Usage
    $ python3 report.py

## Extra Information

### SQL Queries
You will find the queries inside the **queries/** folder.

- queries\
    - top_articles.sql
    - top_authors.sql
    - days_with_errors.sql

### Output
The program will output a report for the following questions:

- Top Articles, the 3 most viewed articles
- Top Authors, the most popular authors
- Requests with errors, The days with more than 1% of error on page requests.

### Example of output
![Sample](sample.png)

You also find an example of output in [sample_output.txt](sample_output.txt)


### My tests
This project was tested with:

- python 3.4.2 and PostgreSQL 10.2 on MacOSX

## License
You can't use this project as your project for Udacity, but you can use for study purposes if you want.


