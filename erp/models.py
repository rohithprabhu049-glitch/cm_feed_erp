from django.db import models


# =========================================
# PRODUCT MODEL
# =========================================

class Product(models.Model):

    name = models.CharField(
        max_length=100
    )

    stock = models.IntegerField(
        default=0
    )

    def __str__(self):

        return self.name


# =========================================
# SALES BILL MODEL
# =========================================

# =========================================
# BILL MODEL
# =========================================

class Bill(models.Model):

    bill_no = models.CharField(
        max_length=100,
        unique=True
    )

    date = models.DateField()

    rd_name = models.CharField(
        max_length=100
    )

    retail_partner = models.CharField(
        max_length=100
    )

    mobile = models.CharField(
        max_length=20
    )

    customer_name = models.CharField(
        max_length=200,
        default=''
    )

    sales_person_name = models.CharField(
        max_length=200,
        default=''
    )

    address = models.TextField()

    collected_payment = models.FloatField(
        default=0
    )

    due = models.FloatField(
        default=0
    )

    total_amount = models.FloatField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.bill_no


# =========================================
# SALES ITEM MODEL
# =========================================

class SaleItem(models.Model):

    bill = models.ForeignKey(

        Bill,

        on_delete=models.CASCADE,

        related_name='items'

    )

    product = models.ForeignKey(

        Product,

        on_delete=models.CASCADE

    )

    bag_count = models.IntegerField()

    unit_price = models.FloatField()

    total_price = models.FloatField()

    def save(self, *args, **kwargs):

        if self.pk is None:

            if self.product.stock >= self.bag_count:

                self.product.stock -= self.bag_count

                self.product.save()

            else:

                raise ValueError(

                    "Insufficient Stock"

                )

        self.total_price = (

            self.bag_count *

            self.unit_price

        )

        super().save(*args, **kwargs)

    def __str__(self):

        return (

            f"{self.bill.bill_no}"

            f" - "

            f"{self.product.name}"

        )

# =========================================
# PRODUCTION MODEL
# =========================================

class Production(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    approved = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    date = models.DateField()

    bag_count = models.IntegerField()

    def __str__(self):

        return (
            f"{self.product.name}"
            f" - "
            f"{self.bag_count}"
        )


# =========================================
# RAW MATERIAL MODEL
# =========================================

class RawMaterial(models.Model):

    item_name = models.CharField(
        max_length=100
    )

    date = models.DateField()

    used_kg = models.FloatField()

    current_balance = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.item_name