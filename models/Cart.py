from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship 
from db.session import Base
class Cart(Base):
    __tablename__ = "cart"

    cart_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"))
    quantity = Column(Integer, default=1)
    

    user = relationship("User", back_populates="carts")
    product = relationship("Product", back_populates="carts")