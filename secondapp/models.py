from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    roll_num = models.IntegerField(unique=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField()
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " - " + str(self.roll_num)
    
    class Meta: 
        verbose_name_plural = "Students"

class Contact_Us(models.Model):
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, unique=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " - " + self.subject
    
    class Meta:
        verbose_name_plural = "Contact Us"
        
class Category(models.Model):
    cat_name = models.CharField(max_length=100)
    cover_pic = models.FileField(upload_to="media/%Y/%m/%d")
    description = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cat_name
    
    class Meta:
        verbose_name_plural = "Categories"        
        
class register_table(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15)
    profile_pic = models.FileField(upload_to="profiles/%Y/%m/%d", null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    about = models.TextField(blank=True, null=True) 
    city = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, default="M")
    occupation = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField()
    utype = models.CharField(max_length=1)
    added_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = "User Registration"
        
class add_product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    product_desc = models.TextField()
    product_image = models.FileField(upload_to="products/%Y/%m/%d")
    details = models.TextField()
    added_on = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
    
    class Meta:
        verbose_name_plural = "Products"
        
class cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(add_product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.BooleanField(default=False)
    added_on = models.DateTimeField(auto_now_add=True, null=True)
    update_on = models.DateTimeField(auto_now=True, null=True)
    
# class cart(models.Model):
#     user =models.ForeignKey(User,on_delete = models.CASCADE)
#     product = models.ForeignKey(add_product,on_delete = models.CASCADE)
#     quantity = models.IntegerField()
#     status = models.BooleanField(default=False)
#     added_on =models.DateTimeField(auto_now_add=True,null=True)
#     update_on = models.DateTimeField(auto_now=True,null=True)

    # def __str__(self):
    #     return self.user.username

    def __str__(self):
        return f"{self.user.username} - {self.product.product_name} ({self.quantity})"
    
    class Meta:
        verbose_name_plural = "carts"
        
class Order(models.Model):
    cust_id = models.ForeignKey(User,on_delete=models.CASCADE)
    cart_ids = models.CharField(max_length=250)
    product_ids = models.CharField(max_length=250)
    txn_ref = models.CharField(max_length=100, unique=True, null=True)
    invoice_id = models.CharField(max_length=250)
    status = models.BooleanField(default=False)
    processed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cust_id.username
    
    class Meta:
        verbose_name_plural = "Orders"