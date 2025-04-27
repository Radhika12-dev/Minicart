from fastapi import Depends, FastAPI, HTTPException, Form, Request
from sqlalchemy.orm import Session
from db import SessionLocal, engine
import models, schemas
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import staticfiles
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add templates directory to the FastAPI app
templates = Jinja2Templates(directory="templates")
app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/create-customer", response_class=HTMLResponse)
async def create_customer_form(request: Request):
    return templates.TemplateResponse("Customer.html", {"request": request})

@app.get("/create-product", response_class=HTMLResponse)
async def create_product_form(request: Request):
    return templates.TemplateResponse("Products.html", {"request": request})

@app.get("/create-orders", response_class=HTMLResponse)
async def create_order_form(request: Request):
    return templates.TemplateResponse("Orders.html", {"request": request})

@app.get("/view-orders", response_class=HTMLResponse)
async def view_order_form(request: Request):
    return templates.TemplateResponse("Views.html", {"request": request})

# Database Connections
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/customers/")
def create_customer(customer: schemas.CreateCustomer, db: Session = Depends(get_db)):
    """Create a new customer."""
    db_customer = db.query(models.Customer).filter(models.Customer.email == customer.email).first()
    if db_customer:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_customer = models.Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,  # Added phone
        address=customer.address,  # Added address
    )
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer


@app.get("/customers/")
def get_customers(db: Session = Depends(get_db)):
    """Fetch all customers."""
    customers = db.query(models.Customer).all()
    # Convert SQLAlchemy models to dictionaries
    result = []
    for customer in customers:
        result.append({
            "id": customer.id,
            "name": customer.name,
            "email": customer.email,
            "phone": customer.phone,
            "address": customer.address
        })
    return JSONResponse(content=result)

@app.get("/view-customers", response_class=HTMLResponse)
async def view_customers_page(request: Request):
    """Render the view customers page."""
    return templates.TemplateResponse("ViewCustomers.html", {"request": request})

@app.post("/products/")
def create_product(product: schemas.CreateProducts, db: Session = Depends(get_db)):
    """Create a new product."""
    db_product = db.query(models.Product).filter(models.Product.name == product.name).first()
    if db_product:
        raise HTTPException(status_code=400, detail="Product already exists")
    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@app.get("/view-products", response_class=HTMLResponse)
async def view_products_page(request: Request):
    """Render the view products page."""
    return templates.TemplateResponse("ViewProducts.html", {"request": request})

@app.get("/products/")
def get_products(db: Session = Depends(get_db)):
    """Fetch all products."""
    products = db.query(models.Product).all()
    return products
@app.post("/orders/", response_model=schemas.OrderOut)
def create_order(order: schemas.CreateOrder, db: Session = Depends(get_db)):
    """Create a new order."""
    customer = db.query(models.Customer).filter(models.Customer.id == order.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    products = db.query(models.Product).filter(models.Product.id.in_(order.products)).all()
    if len(products) != len(order.products):
        raise HTTPException(status_code=404, detail="One or more products not found")
    
    total_amount = sum(product.price for product in products)
    new_order = models.Order(
        customer_id=order.customer_id,
        total_amount=total_amount,
        products=products,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return schemas.OrderOut(
        id=new_order.id,
        customer_id=new_order.customer_id,
        created_at = new_order.order_date,
        total_amount=new_order.total_amount,
        products=new_order.products
    )

@app.get("/view-orders", response_class=HTMLResponse)
async def view_orders_page(request: Request):
    """Render the view orders page."""
    return templates.TemplateResponse("view_orders.html", {"request": request})

# Route to serve the fetch-by-customer form:
@app.get("/fetch-by-customer", response_class=HTMLResponse)
async def fetch_by_customer_form(request: Request):
    """Render the fetch by customer form."""
    return templates.TemplateResponse("fetch_by_customer.html", {"request": request})


@app.get("/orders/customer/{customer_name}", response_model=List[schemas.OrderOut])
def get_orders_by_customer_name(customer_name: str, db: Session = Depends(get_db)):
    """Fetch orders by customer name."""
    cust = db.query(models.Customer).filter(models.Customer.name == customer_name).first()
    if not cust:
        raise HTTPException(status_code=404, detail="Customer not found")

    orders = db.query(models.Order).filter(models.Order.customer_id == cust.id).all()
    if not orders:
        return []

    # 3) serialize via schema
    result = []
    for o in orders:
        total_amount = sum(p.price for p in o.products)
        result.append(schemas.OrderOut(
            id=o.id,
            customer_id=o.customer_id,
            created_at=o.order_date,
            total_price=total_amount,
            products=o.products
        ))
    return result


