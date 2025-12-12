import logging
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas, crud, database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger("cloud-infra-api")

# OAuth2/JWT security setup (placeholder, to be integrated with real auth provider)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_db():
    """
    Dependency to get DB session.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Placeholder for user authentication.
    Replace with real JWT/OAuth2 validation.
    """
    # TODO: Integrate with real authentication provider
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # For demo, accept any non-empty token
    return {"username": "demo-user"}

app = FastAPI(
    title="Cloud Infrastructure Automation Platform API",
    description="RESTful API for managing products and automating cloud resources.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
def on_startup():
    """
    Initialize database and log startup.
    """
    logger.info("Starting Cloud Infrastructure Automation Platform API...")
    models.Base.metadata.create_all(bind=database.engine)

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """
    Handle SQLAlchemy errors globally.
    """
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal database error."}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handle HTTP exceptions globally.
    """
    logger.warning(f"HTTP error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.get("/health", tags=["Health"], response_model=dict)
def health_check():
    """
    Health check endpoint.
    """
    return {"status": "ok"}

# --- Product CRUD Endpoints ---

@app.post(
    "/products/",
    response_model=schemas.Product,
    status_code=status.HTTP_201_CREATED,
    tags=["Products"],
    summary="Create a new product"
)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Create a new product.
    """
    try:
        db_product = crud.create_product(db=db, product=product, user=user["username"])
        logger.info(f"Product created: {db_product.id} by {user['username']}")
        return db_product
    except IntegrityError as e:
        logger.error(f"Integrity error on product creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exists."
        )
    except Exception as e:
        logger.error(f"Unexpected error on product creation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create product."
        )

@app.get(
    "/products/",
    response_model=List[schemas.Product],
    status_code=status.HTTP_200_OK,
    tags=["Products"],
    summary="List all products"
)
def list_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Retrieve all products.
    """
    products = crud.get_products(db=db, skip=skip, limit=limit)
    logger.info(f"Products listed by {user['username']}: count={len(products)}")
    return products

@app.get(
    "/products/{product_id}",
    response_model=schemas.Product,
    status_code=status.HTTP_200_OK,
    tags=["Products"],
    summary="Get product by ID"
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Retrieve a product by its ID.
    """
    product = crud.get_product(db=db, product_id=product_id)
    if not product:
        logger.warning(f"Product not found: id={product_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    logger.info(f"Product retrieved: id={product_id} by {user['username']}")
    return product

@app.put(
    "/products/{product_id}",
    response_model=schemas.Product,
    status_code=status.HTTP_200_OK,
    tags=["Products"],
    summary="Update product by ID"
)
def update_product(
    product_id: int,
    product_update: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Update an existing product.
    """
    product = crud.get_product(db=db, product_id=product_id)
    if not product:
        logger.warning(f"Product not found for update: id={product_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    try:
        updated_product = crud.update_product(
            db=db,
            product_id=product_id,
            product_update=product_update,
            user=user["username"]
        )
        logger.info(f"Product updated: id={product_id} by {user['username']}")
        return updated_product
    except IntegrityError as e:
        logger.error(f"Integrity error on product update: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product update failed due to integrity error."
        )
    except Exception as e:
        logger.error(f"Unexpected error on product update: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update product."
        )

@app.delete(
    "/products/{product_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    tags=["Products"],
    summary="Delete product by ID"
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    """
    Delete a product by its ID.
    """
    product = crud.get_product(db=db, product_id=product_id)
    if not product:
        logger.warning(f"Product not found for deletion: id={product_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found."
        )
    try:
        crud.delete_product(db=db, product_id=product_id, user=user["username"])
        logger.info(f"Product deleted: id={product_id} by {user['username']}")
        return {"detail": "Product deleted successfully."}
    except Exception as e:
        logger.error(f"Unexpected error on product deletion: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete product."
        )

# Export FastAPI app instance
# This is used by ASGI servers (e.g., uvicorn) to run the application
# Usage: uvicorn api.main:app --host 0.0.0.0 --port 8000