from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    """
    Schema for creating a new product.
    """
   
    product_name: str
    product_price: float


class UpdateProductRequest(BaseModel):
    """
    Schema for updating an existing product.
    Note: product_id is taken from the URL path, not the request body.
    """
    product_name: str
    product_price: float


class ProductResponse(BaseModel):
    """
    Schema for product response data.
    """
    product_id: int
    product_name: str
    product_price: float

    class Config:
        from_attributes = True
