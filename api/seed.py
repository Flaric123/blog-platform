from models import Category, Comment, Article, User
from database import engine, get_db
import models

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
with get_db().__next__() as session:
    categories=[
        Category(name='category1'),
        Category(name='category2'),
        Category(name='category3'),
    ]

    users=[
        User(username='user1', email='u1@gmail.com', role='guest'),
        User(username='user2', email='u3@gmail.com', role='user'),
        User(username='user3', email='u2@gmail.com', role='admin')
    ]

    articles=[
        Article(author=users[1],title='This is my first post on this site',
                content='please help me write something')
    ]

    comments=[
        Comment(content='My first comment on this site', article=articles[0], user=users[1])
    ]

    session.add_all(categories)
    session.add_all(users)
    session.add_all(articles)
    session.add_all(comments)
    session.commit()
    print('Посев прошел успешно!')
    print(articles[0].comments)