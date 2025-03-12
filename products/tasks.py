from background_task import background
from .models import Product, Order

@background(schedule=60)  
def update_products():
    products = Product.objects.all()
    for product in products:
        product.price += 5  
        product.save()
    print("Products updated successfully.")

@background(schedule=120) 
def update_orders():
    orders = Order.objects.filter(status="Pending")
    for order in orders:
        order.status = "Processing"
        order.save()
    print("Orders updated successfully.")



@background(schedule=60)  # Run every 10 minutes
def update_products_recurring():
    products = Product.objects.all()
    for product in products:
        product.price += 10 
        product.save()
    print(" Products updated successfully!")

@background
def update_products_recurring_dynamic():
    """
    Background task to update product prices every X minutes.
    """
    products = Product.objects.all()
    for product in products:
        product.price += 10  
        product.save()
    print("Products updated successfully!")
