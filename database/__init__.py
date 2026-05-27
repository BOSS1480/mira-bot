\"""
Database module - SQLite with SQLAlchemy
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Text, Float, BigInteger
from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Models
class ChatSettings(Base):
    """Chat settings storage"""
    __tablename__ = "chat_settings"
    
    chat_id = Column(BigInteger, primary_key=True)
    welcome_enabled = Column(Boolean, default=True)
    welcome_text = Column(Text, default="{first} welcome to {chatname}!")
    goodbye_enabled = Column(Boolean, default=False)
    goodbye_text = Column(Text, default="{first} left the chat")
    rules_text = Column(Text, default="No rules set")
    antiflood_enabled = Column(Boolean, default=False)
    antiflood_limit = Column(Integer, default=5)
    antiraid_enabled = Column(Boolean, default=False)
    captcha_enabled = Column(Boolean, default=False)
    lang = Column(String, default="en")
    
class UserWarnings(Base):
    """User warnings storage"""
    __tablename__ = "user_warnings"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger)
    user_id = Column(BigInteger)
    reason = Column(Text)
    timestamp = Column(Float)

class Filters(Base):
    """Custom filters storage"""
    __tablename__ = "filters"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger)
    keyword = Column(String)
    response = Column(Text)

class Blocklist(Base):
    """Blocklist storage"""
    __tablename__ = "blocklist"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger)
    word = Column(String)

class Notes(Base):
    """Notes storage"""
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger)
    name = Column(String)
    content = Column(Text)

class ConnectedChats(Base):
    """Connected chats for private bot usage"""
    __tablename__ = "connected_chats"
    
    chat_id = Column(BigInteger, primary_key=True)
    connected_group_id = Column(BigInteger)

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    """Get database session"""
    async with AsyncSessionLocal() as session:
        yield session