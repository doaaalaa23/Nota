from typing import List, Optional
from sqlalchemy.orm import Session
from app.domain.models.product_model import Product
from app.domain.repositories.product_repository import ProductRepository
from app.infrastructure.models.product_model import ProductTable


class ProductRepositoryImpl(ProductRepository):
    """
    Concrete implementation of ProductRepository using SQLAlchemy ORM.
    """

    def __init__(self, session: Session, user_id: Optional[int] = None):
        self.session = session
        self.user_id = user_id

    def set_user_id(self, user_id: int) -> None:
        self.user_id = user_id

    def _require_user_id(self) -> int:
        if self.user_id is None:
            raise ValueError("User context is required")
        return self.user_id

    def add(self, product: Product) -> Product:
        try:
            self._require_user_id()
            product_table = ProductTable(
                product_name=product.product_name,
                product_price=product.product_price,
                user_id=self.user_id,
            )
            self.session.add(product_table)
            self.session.commit()
            self.session.refresh(product_table)
            return Product(
                product_id=product_table.product_id,
                product_name=product_table.product_name,
                product_price=product_table.product_price,
            )
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error adding product: {str(e)}")

    def read(self, product_id: str) -> Optional[Product]:
        try:
            self._require_user_id()
            product_table = self.session.query(ProductTable).filter(
                ProductTable.product_id == int(product_id),
                ProductTable.user_id == self.user_id,
            ).first()
            if not product_table:
                return None

            return Product(
                product_id=product_table.product_id,
                product_name=product_table.product_name,
                product_price=product_table.product_price,
            )
        except Exception as e:
            raise ValueError(f"Error reading product: {str(e)}")

    def read_by_name(self, product_name: str) -> List[Product]:
        try:
            self._require_user_id()
            product_table = self.session.query(ProductTable).filter(
                ProductTable.product_name.ilike(f"%{product_name}%"),
                ProductTable.user_id == self.user_id,
            ).all()
            if not product_table:
                return []

            return [
                Product(
                    product_id=pt.product_id,
                    product_name=pt.product_name,
                    product_price=pt.product_price,
                )
                for pt in product_table
            ]
        except Exception as e:
            raise ValueError(f"Error reading product: {str(e)}")

    def read_all(self) -> List[Product]:
        try:
            self._require_user_id()
            product_tables = self.session.query(ProductTable).filter(ProductTable.user_id == self.user_id).all()
            return [
                Product(
                    product_id=pt.product_id,
                    product_name=pt.product_name,
                    product_price=pt.product_price,
                )
                for pt in product_tables
            ]
        except Exception as e:
            raise ValueError(f"Error reading all products: {str(e)}")

    def update(self, product_id: str, product: Product) -> Optional[Product]:
        try:
            self._require_user_id()
            product_table = self.session.query(ProductTable).filter(
                ProductTable.product_id == int(product_id),
                ProductTable.user_id == self.user_id,
            ).first()
            if not product_table:
                return None

            product_table.product_name = product.product_name
            product_table.product_price = product.product_price
            self.session.commit()

            return Product(
                product_id=product_table.product_id,
                product_name=product_table.product_name,
                product_price=product_table.product_price,
            )
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error updating product: {str(e)}")

    def delete(self, product_id: str) -> bool:
        try:
            self._require_user_id()
            product_table = self.session.query(ProductTable).filter(
                ProductTable.product_id == int(product_id),
                ProductTable.user_id == self.user_id,
            ).first()
            if not product_table:
                return False

            self.session.delete(product_table)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error deleting product: {str(e)}")

    def exists(self, product_id: str) -> bool:
        try:
            self._require_user_id()
            result = self.session.query(ProductTable).filter(
                ProductTable.product_id == int(product_id),
                ProductTable.user_id == self.user_id,
            ).first()
            return result is not None
        except Exception as e:
            raise ValueError(f"Error checking product existence: {str(e)}")
