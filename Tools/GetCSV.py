# Imports to make the Program Run

import csv
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

def csv_File_Name(keyword,time):

    date_today = datetime.today()

    if time == "Past hour":
        file_name = f"{keyword} Articles From {(date_today - timedelta(hours=1)).strftime('%Y-%m-%d %I:%M %p')} To {date_today.strftime('%Y-%m-%d %I:%M %p')}"
    elif time == "Past 24 hours":
        file_name = f"{keyword} Articles From {(date_today - timedelta(days=1)).strftime('%Y-%m-%d %I:%M %p')} To {date_today.strftime('%Y-%m-%d %I:%M %p')}"
    elif time == "Past week":
        file_name = f"{keyword} Articles From {(date_today - timedelta(days=7)).strftime('%Y-%m-%d %I:%M %p')} To {date_today.strftime('%Y-%m-%d %I:%M %p')}"
    elif time == "Past month":
        file_name = f"{keyword} Articles From {(date_today - relativedelta(months=1)).strftime('%Y-%m-%d %I:%M %p')} To {date_today.strftime('%Y-%m-%d %I:%M %p')}v"
    elif time == "Past year":
        file_name = f"{keyword} Articles From {(date_today - relativedelta(years=1)).strftime('%Y-%m-%d %I:%M %p')} To {date_today.strftime('%Y-%m-%d %I:%M %p')}"
    else:
        file_name = f"{keyword} Articles From {date_today.strftime('%Y-%m-%d %I:%M %p')} To No Specified Date And Time"

    return file_name


# Flattens the 3d Array into a list of tuples for each News Article

def newsArticleFlatter(newsArticles):
    newsArticles = [tup for group in newsArticles for tup in group]
    return newsArticles


# A function used to write the News Articles into the CSV file

def csv_Writer(news_articles, keyword,time):

    file_name = csv_File_Name(keyword,time)
    headers = ['Title', 'Description', 'Publication Date (Relative To When Script Was Run)', 'Link']

    with open(file_name,'w',newline="",encoding='utf-8-sig') as file:
        rowWrite = csv.writer(file)
        rowWrite.writerow(headers)
        for news in news_articles:
            rowWrite.writerow(news)


# Function used to get the actual CSV Files

def get_CSV(newsArticles,keyword,time):
    flatNewsArticles = newsArticleFlatter(newsArticles)
    csv_Writer(flatNewsArticles,keyword,time)