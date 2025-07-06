import sys
from mongoengine import connect
from models import Authors, Quotes

connect(
    db="testdb",
    host="mongodb://localhost:27017/testdb"
    )


def search_by_author(name):
    author = Authors.objects(fullname=name).first()
    if author:
        quotes = Quotes.objects(author=author)
        return [q.qoute for q in quotes]
    return []


def search_by_tag(tag):
    quotes = Quotes.objects(tags=tag)
    return [q.qoute for q in quotes]


def search_by_tags(tags):
    tags_list = tags.split(",")
    quotes = Quotes.objects(tags__in=tags_list)
    return [q.qoute for q in quotes]


print("Скрипт запущено. Введіть команду (name:, tag:, tags:, exit):")

while True:
    user_input = input("> ").strip()
    if user_input.lower() == "exit":
        print("До зустрічі!")
        sys.exit(0)

    if ":" not in user_input:
        print("Некоректна команда. Формат: команда:значення")
        continue

    cmd, value = user_input.split(":", 1)
    cmd = cmd.strip().lower()
    value = value.strip()

    if cmd == "name":
        results = search_by_author(value)
    elif cmd == "tag":
        results = search_by_tag(value)
    elif cmd == "tags":
        results = search_by_tags(value)
    else:
        print(
            f"Невідома команда '{cmd}'. Спробуйте name:, tag:, tags: або exit."
        )
        continue

    if results:
        print("\n".join(results))
    else:
        print("Нічого не знайдено.")
