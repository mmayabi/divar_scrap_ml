# divar_scrap_ml
Scraping divar website and gathering extracted data in to db and then predicting the price of apartment based on its features. The code was for final project of maktabkhooneh Python Advanced Programming course.

Code containes two part:
1. Extracting data and gather them in mariadb. User can enter the city and number of pages for scroll. 
2. Training based these data and predicting apartment price.In this step user enter apartment features and get prediction of apartment price.

Steps to run:
1. having mariadb sql (DB name:divar table:buyapartment [divar.sql](divar.sql))
2. install [requirement.txt](requirement.txt) (beter use venv)
3. run [main.py](main.py)
