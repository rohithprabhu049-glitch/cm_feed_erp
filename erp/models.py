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
# SALES MODEL
# =========================================

class Sale(models.Model):

    bill_no = models.CharField(
        max_length=100,
        unique=True,
        blank=True
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

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    bag_count = models.IntegerField()

    unit_price = models.FloatField()

    collected_payment = models.FloatField(
        default=0
    )

    due = models.FloatField(
        default=0
    )

    total_price = models.FloatField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def save(self, *args, **kwargs):

        # TOTAL PRICE
        self.total_price = (
            int(self.bag_count) *
            float(self.unit_price)
        )

        # AUTO BILL NUMBER
        if not self.bill_no:

            last_sale = Sale.objects.order_by(
                '-id'
            ).first()

            if last_sale:
                new_id = last_sale.id + 1
            else:
                new_id = 1

            self.bill_no = f"CM_{new_id:04d}"

        # STOCK CHECK ONLY FOR NEW SALE
        if self.pk is None:

            if self.product.stock >= int(
                self.bag_count
            ):

                self.product.stock -= int(
                    self.bag_count
                )

                self.product.save()

            else:

                raise ValueError(
                    "Insufficient Stock"
                )

        super().save(*args, **kwargs)

    def __str__(self):

        return self.bill_no


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