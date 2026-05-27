\"""
Database module for Mira Bot
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
    language = Column(String, default="en")
    welcome_enabled = Column(Boolean, default=True)
    welcome_text = Column(Text, default="Welcome {first} to {chatname}!")
    goodbye_enabled = Column(Boolean, default=False)
    goodbye_text = Column(Text, default="Goodbye {first}!")
    rules_text = Column(Text, default="No rules set")
    antiflood_enabled = Column(Boolean, default=False)
    antiflood_limit = Column(Integer, default=5)
    captcha_enabled = Column(Boolean, default=False)
    antiraid_enabled = Column(Boolean, default=False)
    raid_count = Column(Integer, default=10)
    max_warnings = Column(Integer, default=3)

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

class Staff(Base):
    """Staff members storage"""
    __tablename__ = "staff"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger)
    user_id = Column(BigInteger)
    rank = Column(String)  # admin, mod, etc

class UserNotes(Base):
    """Notes on users"""
    __tablename__ = "user_notes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(BigInteger)
    user_id = Column(BigInteger)
    note = Column(Text)
    added_by = Column(BigInteger)
    timestamp = Column(Float)

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session():
    """Get database session"""
    async with AsyncSessionLocal() as session:
        yield session