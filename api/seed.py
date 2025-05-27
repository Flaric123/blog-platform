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

    session.add_all(categories)
    session.commit()
    print('Посев прошел успешно!')