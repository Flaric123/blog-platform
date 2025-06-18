from sqlalchemy import (
    Column, Integer, String, Text, DateTime, Enum, ForeignKey, Table, event, UniqueConstraint
)
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column
from sqlalchemy.event import listens_for
import enum
from typing import List
from datetime import datetime

Base = declarative_base()

#
#   BLOG
#

class ArticleStatus(enum.Enum):
    draft = "draft"
    published = "published"

article_category_table = Table(
    'article_category',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id', ondelete='CASCADE'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id', ondelete='CASCADE'), primary_key=True)
)

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Enum(ArticleStatus), default=ArticleStatus.draft, nullable=False)
    published_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    last_changed_by_user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    author = relationship("User", back_populates="articles")
    comments = relationship("Comment", back_populates="article", cascade="all, delete-orphan")
    categories = relationship("Category", secondary=article_category_table, back_populates="articles")
    likes = relationship("Like", back_populates="article", cascade="all, delete-orphan")

@event.listens_for(Article.status, 'set')
def update_published_at(target,value,oldValue, initiator):
    if value==ArticleStatus.published:
        target.published_at=datetime.now()
    else:
        target.published_at=None

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    last_changed_by_user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    articles = relationship("Article", secondary=article_category_table, back_populates="categories")

    def __repr__(self):
        return f"<Category(id={self.id}, title='{self.name}')>"

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    last_changed_by_user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    article = relationship("Article", back_populates="comments")
    user = relationship("User", back_populates="comments")

class Like(Base):
    __tablename__="likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    last_changed_by_user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    user = relationship("User", back_populates="likes")
    article = relationship("Article", back_populates="likes")

    __table_args__ = (
        UniqueConstraint('user_id', 'article_id', name='uq_user_article_like'),
    )
#
#   USERS
#

class User(Base):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    role = Column(String(50), nullable=False)
    hashed_password=Column(String(), nullable=False)

    # Relationships
    articles = relationship("Article", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.username}')>"