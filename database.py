from peewee import *


db = SqliteDatabase('stats.db')


class BaseModel(Model):
    class Meta:
        database = db


class Imageboard(BaseModel):
    imageboard = CharField(unique=True)


class Board(BaseModel):
    board = CharField()
    imageboard = ForeignKeyField(Imageboard, related_name='boards')


class Post(BaseModel):
    board = ForeignKeyField(Board, related_name='data')
    timestamp = DateTimeField()
    post_id = BigIntegerField()


def create_tables():
    db.connect()
    db.create_tables([Imageboard, Board, Post])


def add_imageboards(data):
    for imageboard in data.keys():
        try:
            db_imageboard = Imageboard.get(imageboard=imageboard)
        except DoesNotExist:
            db_imageboard = Imageboard.create(imageboard=imageboard)
        for board in data[imageboard]:
            try:
                Board.get(imageboard=db_imageboard, board=board)
            except DoesNotExist:
                Board.create(imageboard=db_imageboard, board=board)
