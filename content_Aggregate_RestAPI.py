from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
import csv
from datetime import datetime

app = FastAPI()

# Load articles from CSV
def read_articles_from_csv():
    articles = []
    try:
        with open('news_articles.csv', mode='r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                articles.append({
                    "ID": row["ID"],
                    "Title": row["Title"],
                    "Summary": row["Summary"],
                    "Published Date": row["Published Date"],
                    "URL": row["URL"],
                    "Source": row["Source"],
                    "Category": row["Category"]
                })
    except Exception as e:
        print(f"Error reading CSV: {e}")
    return articles

articles = read_articles_from_csv()

@app.get("/", response_model=dict)
def read_root():
    return {"message": "Welcome to the News API! Use /articles to get a list of articles or /articles/{id} to get a specific article."}

@app.get("/articles", response_model=List[dict])
def get_articles(start_date: Optional[str] = None, end_date: Optional[str] = None, category: Optional[str] = None):
    filtered_articles = articles
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        filtered_articles = [article for article in filtered_articles if datetime.strptime(article["Published Date"], "%Y-%m-%d %H:%M:%S") >= start_date]
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        filtered_articles = [article for article in filtered_articles if datetime.strptime(article["Published Date"], "%Y-%m-%d %H:%M:%S") <= end_date]
    if category:
        filtered_articles = [article for article in filtered_articles if article["Category"].lower() == category.lower()]
    return filtered_articles

@app.get("/articles/{id}", response_model=dict)
def get_article(id: int):
    try:
        article = next(article for article in articles if int(article["ID"]) == id)
        return article
    except StopIteration:
        raise HTTPException(status_code=404, detail="Article not found")

@app.get("/search", response_model=List[dict])
def search_articles(keyword: str):
    keyword = keyword.lower()
    filtered_articles = [article for article in articles if keyword in article["Title"].lower() or keyword in article["Summary"].lower()]
    return filtered_articles
