from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker

from src.backend.main.config import config


engine: AsyncEngine = create_async_engine(url=config.postgresql.connection_url)
async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
