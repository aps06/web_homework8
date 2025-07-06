from mongoengine import Document, StringField, ListField, ReferenceField, BooleanField


class Authors(Document):
    fullname = StringField(max_length=120)
    born_date = StringField(max_length=120)
    born_location = StringField(max_length=120)
    description = StringField()

    meta = {
        "collection": "authors",
        "ordering": ["fullname"],
        "indexes": ["fullname"],
    }


class Quotes(Document):
    tags = ListField(StringField(max_length=30))
    author = ReferenceField(Authors, reverse_delete_rule=2)
    qoute = StringField()

    meta = {
        "collection": "qoutes",
        "indexes": ["author", "tags"],
    }


class Contacts(Document):
    name = StringField(max_length=120)
    email = StringField(max_length=120)
    send_mesage = BooleanField(default=False)

    meta = {
        "collection": 'contacts',
        "indexes": ["name", "email"]
        }