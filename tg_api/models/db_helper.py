import asyncio

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from tg_api.config import settings
from tg_api.models.models import Product, Base

DATABASE_URL = settings.DATABASE_URL_asyncpg

# Создание асинхронного движка и сессии
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def create_product(type_product: str, name: str, description: str, price: int,
                         url_download: str, url_guide: str, active: bool = True):
    async with AsyncSessionLocal() as session:
        try:
            async with session.begin():
                new_product = Product(type_product=type_product, name=name, description=description, price=price,
                                      url_download=url_download, url_guide=url_guide, active=True)
                session.add(new_product)
            await session.commit()
            return new_product.id
        except Exception as e:
            await session.rollback()
            return None


# Функция для получения товара по id
async def get_product_by_id(id: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product).where(Product.id == id))
        product = result.scalars().first()
        return product


# Функция для получения всех продуктов одного типа
async def get_products_by_type(type_product: str, filter: bool = True):
    async with AsyncSessionLocal() as session:
        if filter:
            result = await session.execute(
                select(Product).where(
                    Product.type_product == type_product,
                    Product.active == True
                )
            )
        else:
            result = await session.execute(
                select(Product).where(
                    Product.type_product == type_product
                )
            )
        products = result.scalars().all()
        return products


async def get_all_products():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product))
        products = result.scalars().all()
        return products


async def get_all_types() -> list:
    """Получить все уникальные типы продуктов, где активен (active == True)."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Product.type_product).filter(Product.active.is_(True)).distinct())
        types = result.scalars().all()
        return list(types)


async def update_product(id: int, type: str = None, name: str = None, description: str = None, price: float = None,
                         url_download: str = None, url_guide: str = None):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            product = await session.get(Product, id)
            if product is not None:
                if type is not None:
                    product.type_product = type
                if name is not None:
                    product.name = name
                if description is not None:
                    product.description = description
                if price is not None:
                    product.price = price
                if url_download is not None:
                    product.url_download = url_download
                if url_guide is not None:
                    product.url_guide = url_download
            await session.commit()
        return product


async def delete_product_active(id: int, b: bool = False):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            product = await session.get(Product, id)
            if product is not None:
                product.active = b
            await session.commit()
        return product


async def delete_product():
    pass
