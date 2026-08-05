from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.presentation.schemas.product_schema import (
    CreateProductRequest,
    UpdateProductRequest,
    ProductResponse
)
from app.application.usecases.add_product import AddProductUseCase
from app.application.usecases.get_product import GetProductUseCase
from app.application.usecases.get_all_product import GetAllProductUseCase
from app.application.usecases.update_product import UpdateProductUseCase
from app.application.usecases.delete_product import DeleteProductUseCase
from app.application.usecases.get_product import GetProductByNameUseCase
from app.infrastructure.repositories.product_repository_impl import ProductRepositoryImpl
from app.infrastructure.database.session import get_db
from app.presentation.routes.dependencies import get_current_user_id

router = APIRouter(prefix="/api/products", tags=["products"])


def get_product_repository(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
) -> ProductRepositoryImpl:
    repository = ProductRepositoryImpl(db)
    repository.set_user_id(user_id)
    return repository


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    request: CreateProductRequest,
    repository: ProductRepositoryImpl = Depends(get_product_repository)
):
    try:
        use_case = AddProductUseCase(repository)
        product = use_case.execute(
            product_name=request.product_name,
            product_price=request.product_price
        )
        return product
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    repository: ProductRepositoryImpl = Depends(get_product_repository)
):
    try:
        use_case = GetProductUseCase(repository)
        product = use_case.execute(product_id=product_id)
        return product
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/name/{product_name}", response_model=List[ProductResponse])
async def get_product_by_name(
    product_name: str,
    repository: ProductRepositoryImpl = Depends(get_product_repository)
):
    try:
        use_case = GetProductByNameUseCase(repository)
        products = use_case.execute(product_name=product_name)
        return products
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@router.get("/", response_model=List[ProductResponse])
async def get_all_products(
    repository: ProductRepositoryImpl = Depends(get_product_repository)
):
    try:
        use_case = GetAllProductUseCase(repository)
        return use_case.execute()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    request: UpdateProductRequest,
    repository: ProductRepositoryImpl = Depends(get_product_repository)
):
    try:
        use_case = UpdateProductUseCase(repository)
        product = use_case.execute(
            product_id=product_id,
            product_name=request.product_name,
            product_price=request.product_price
        )
        return product
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    repository: ProductRepositoryImpl = Depends(get_product_repository)
):
    try:
        use_case = DeleteProductUseCase(repository)
        use_case.execute(product_id=product_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
