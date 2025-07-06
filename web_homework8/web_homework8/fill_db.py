import json
from models import Authors, Quotes
from mongoengine import connect


connect(
    db="testdb",
    host="mongodb://localhost:27017/testdb",
)


with open("authors.json", "r", encoding="utf-8") as f:
    authors_list = json.load(f)

for item in authors_list:
    author = Authors(
        fullname=item.get("fullname"),
        born_date=item.get("born_date"),
        born_location=item.get("born_location"),
        description=item.get("description"),
    )
    author.save()
with open("quotes.json", "r", encoding="utf-8") as f:
    quotes_list = json.load(f)

for item in quotes_list:
    author_name = item.get("author")
    author = Authors.objects(fullname=author_name).first()
    if author:
        quote = Quotes(
            tags=item.get("tags", []),
            author=author,
            qoute=item.get("qoute"),
        )
        quote.save()
    else:
        print("Автор {author_name} не знайдений!")
