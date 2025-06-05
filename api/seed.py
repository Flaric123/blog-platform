from models import Category, Comment, Article, User
from database import engine, get_db
import models
from auth import get_password_hash

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
with get_db().__next__() as session:
    categories=[
        Category(name='category1'),
        Category(name='category2'),
        Category(name='category3'),
    ]

    users=[
        User(username='user1', role='reader', hashed_password=get_password_hash('123'),api_access_token='none'),
        User(username='user2', role='author', hashed_password=get_password_hash('234'),api_access_token='none'),
        User(username='user3', role='admin', hashed_password=get_password_hash('345'),api_access_token='none')
    ]

    articles=[
        Article(author=users[1],title='This is my first post on this site',
                content='please help me write something', categories=[categories[0],categories[1]])
    ]

    comments=[
        Comment(content='My first comment on this site1', article=articles[0], user=users[1])
    ]

    session.add_all(categories)
    session.add_all(users)
    session.add_all(articles)
    session.add_all(comments)
    session.commit()
    print('Посев прошел успешно!')