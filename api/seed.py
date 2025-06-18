from models import Category, Comment, Article, User, Like
from database import engine, get_db
import models
from auth import get_password_hash
import random
from models import ArticleStatus
from datetime import datetime,timedelta

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
with get_db().__next__() as session:
    users=[
        User(username='user1', role='reader', hashed_password=get_password_hash('123')),
        User(username='user2', role='author', hashed_password=get_password_hash('234')),
        User(username='user3', role='admin', hashed_password=get_password_hash('345'))
    ]

    def fake_user():
        return random.choice(users)

    def fake_author():
        return random.choice(users[1:])

    categories = [
        Category(name="Technology"),
        Category(name="Health"),
        Category(name="Travel"),
        Category(name="Education"),
        Category(name="Finance"),
        Category(name="Food"),
        Category(name="Lifestyle"),
        Category(name="Science"),
        Category(name="Sports"),
        Category(name="Entertainment"),
    ]
    session.add_all(categories)
    session.commit()

    # Статьи
    articles = [
        Article(
            author=fake_author(),
            title="The Rise of AI in Everyday Life",
            content="Artificial Intelligence is transforming how we live and work...",
            status=ArticleStatus.published,
            categories=[categories[0], categories[7]]  # Technology, Science
        ),
        Article(
            author=fake_author(),
            title="10 Tips for a Healthier Lifestyle",
            content="Living healthy is a combination of diet, exercise and mindset...",
            status=ArticleStatus.published,
            categories=[categories[1], categories[6]]  # Health, Lifestyle
        ),
        Article(
            author=fake_author(),
            title="Exploring the Alps: A Travel Guide",
            content="The Alps are a great destination for adventure and relaxation...",
            status=ArticleStatus.published,
            categories=[categories[2]]  # Travel
        ),
        Article(
            author=fake_author(),
            title="Understanding Cryptocurrency Basics",
            content="Cryptocurrency is a digital or virtual currency that uses cryptography...",
            status=ArticleStatus.draft,
            categories=[categories[4], categories[0]]  # Finance, Technology
        ),
        Article(
            author=fake_author(),
            title="Delicious Vegan Recipes for Beginners",
            content="Eating vegan can be easy and delicious with these simple recipes...",
            status=ArticleStatus.published,
            categories=[categories[5], categories[6]]  # Food, Lifestyle
        ),
        Article(
            author=fake_author(),
            title="The Future of Space Exploration",
            content="Space agencies worldwide are planning new missions to Mars and beyond...",
            status=ArticleStatus.published,
            categories=[categories[7]]  # Science
        ),
        Article(
            author=fake_author(),
            title="How to Manage Personal Finances Effectively",
            content="Budgeting and saving are keys to financial freedom...",
            status=ArticleStatus.published,
            categories=[categories[4], categories[3]]  # Finance, Education
        ),
        Article(
            author=fake_author(),
            title="Top 5 Sports Events to Watch This Year",
            content="From the Olympics to the World Cup, sports fans have much to look forward to...",
            status=ArticleStatus.published,
            categories=[categories[8], categories[9]]  # Sports, Entertainment
        ),
        Article(
            author=fake_author(),
            title="The Importance of Mental Health Awareness",
            content="Mental health is as important as physical health...",
            status=ArticleStatus.published,
            categories=[categories[1], categories[3]]  # Health, Education
        ),
        Article(
            author=fake_author(),
            title="Creative Home Decor Ideas on a Budget",
            content="Transform your living space without breaking the bank...",
            status=ArticleStatus.draft,
            categories=[categories[6]]  # Lifestyle
        ),
    ]
    session.add_all(articles)
    session.commit()

    # Создаем 10 комментариев
    for i in range(1, 11):
        comment = Comment(
            article=articles[i-1],
            user=fake_user(),
            content=f"This is comment {i} content.",
        )
        session.add(comment)
    
    session.commit()

    # Лайки
    used_pairs = set()
    likes = []
    
    for _ in range(10):
        while True:
            user_id = fake_user()
            article = random.choice(articles)
            pair = (user_id, article.id)
            
            if pair not in used_pairs:
                used_pairs.add(pair)
                break
                
        likes.append(
            Like(
                user=user_id,
                article=article,
            )
        )
    
    session.add_all(likes)
    session.commit()

    print('Посев прошел успешно!')