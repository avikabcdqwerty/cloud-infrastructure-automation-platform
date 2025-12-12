from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from . import models, schemas

def create_product(db: Session, product: schemas.ProductCreate, user: str) -> models.Product:
    """
    Create a new product in the database.

    Args:
        db (Session): SQLAlchemy session.
        product (schemas.ProductCreate): Product creation schema.
        user (str): Username of the creator.

    Returns:
        models.Product: The created product instance.

    Raises:
        SQLAlchemyError: If database operation fails.
    """
    db_product = models.Product(
        name=product.name,
        description=product.description,
        created_by=user,
        updated_by=user
    )
    db.add(db_product)
    try:
        db.commit()
        db.refresh(db_product)
        return db_product
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    """
    Retrieve a product by its ID.

    Args:
        db (Session): SQLAlchemy session.
        product_id (int): Product ID.

    Returns:
        Optional[models.Product]: The product instance if found, else None.
    """
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    """
    Retrieve a list of products.

    Args:
        db (Session): SQLAlchemy session.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        List[models.Product]: List of product instances.
    """
    return db.query(models.Product).order_by(models.Product.id).offset(skip).limit(limit).all()

def update_product(
    db: Session,
    product_id: int,
    product_update: schemas.ProductUpdate,
    user: str
) -> models.Product:
    """
    Update an existing product.

    Args:
        db (Session): SQLAlchemy session.
        product_id (int): Product ID.
        product_update (schemas.ProductUpdate): Product update schema.
        user (str): Username of the updater.

    Returns:
        models.Product: The updated product instance.

    Raises:
        SQLAlchemyError: If database operation fails.
    """
    db_product = get_product(db, product_id)
    if db_product is None:
        return None

    # Update fields if provided
    if product_update.name is not None:
        db_product.name = product_update.name
    if product_update.description is not None:
        db_product.description = product_update.description
    db_product.updated_by = user

    try:
        db.commit()
        db.refresh(db_product)
        return db_product
    except SQLAlchemyError as e:
        db.rollback()
        raise e

def delete_product(db: Session, product_id: int, user: str) -> None:
    """
    Delete a product by its ID.

    Args:
        db (Session): SQLAlchemy session.
        product_id (int): Product ID.
        user (str): Username of the deleter (for audit logging).

    Raises:
        SQLAlchemyError: If database operation fails.
    """
    db_product = get_product(db, product_id)
    if db_product is None:
        return

    db.delete(db_product)
    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise e

# Exports:
# - create_product
# - get_product
# - get_products
# - update_product
# - delete_product