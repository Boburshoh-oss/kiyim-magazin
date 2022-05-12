from django.db import models


class Payment(models.Model):
    user = models.ForeignKey("account.Account", on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.payment_id


class Order(models.Model):
    Status = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    )
    user = models.ForeignKey(
        "account.Account", on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(
        "orders.Payment", on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=10, choices=Status, default="New")
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.first_name


class OrderProduct(models.Model):
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE)
    payment = models.ForeignKey("orders.Payment", on_delete=models.CASCADE)
    user = models.ForeignKey("account.Account", on_delete=models.CASCADE)
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE)
    variation = models.ForeignKey("store.Variation", on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=60)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.product.title

