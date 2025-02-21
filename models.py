from asyncio import format_helpers
from math import fabs
from operator import truediv
import os
from tkinter import CASCADE
import uuid
from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import redirect,render
import datetime
from django.core.validators import MaxValueValidator
import shortuuid
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    def _create_user(self, email, username=None, is_admin=False, is_staff=False, is_active=True, password=None):
        'Method for actual creation of a user'

        if not email:
            raise ValueError('User must have an email')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            is_admin=is_admin,
            is_staff=is_staff,
            is_active=is_active
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username=None, password=None):
        'Create a simple user'
        return self._create_user(email=email, username=username, password=password)

    def create_staffuser(self, email, username=None, password=None):
        'Create a staff user'
        return self._create_user(email=email, username=username, is_staff=True, password=password)

    def create_superuser(self, email, username=None, password=None):
        'Create a super user'
        return self._create_user(
            email=email, username=username, is_admin=True,
             is_staff=True, is_active=True, password=password
        )

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=False,default="")
    phoneNumber = models.CharField(max_length=150, unique=False,default="")
    country = models.CharField(max_length=150, unique=False,default="")
    first_name = models.CharField(max_length=250,blank=True,default="")
    last_name = models.CharField(max_length=250,blank=True,default="")
    name = models.CharField(max_length=150, blank=True,default="")
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.email}'

    def get_full_name(self):
        return f'{self.name}'

    def get_short_name(self):
        return f'{self.username}'

    def has_perm(self, perm, obj=None):
        'Does the user have a specific permission?'
        return True

    def has_module_perms(self, app_label):
        'Does the user have permissions to view the app `app_label`?'
        return True

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this User."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    @property
    def has_staff_perm(self):
        'Is the user a member of staff?'
        return self.is_staff

    @property
    def has_active_perm(self):
        'Is the user active?'
        return self.is_active

    @property
    def has_admin_perm(self):
        'Is the user is super admin?'
        return self.is_admin

class Contactus(models.Model):
    BOOL_CHOICES =[('Received', 'Received'),('Contacted', 'Contacted'),]
    id = ShortUUIDField(length=6,max_length=6,alphabet="123456",primary_key=True,)
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True)
    phone = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    countrycode = models.CharField(max_length=250, blank=True, null=True)
    message = models.CharField(max_length=1000, blank=True, null=True)
    status =  models.CharField(max_length=200,choices=BOOL_CHOICES,default='NA',)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return str(self.id)

class PopupBuilders(models.Model):

    name = models.CharField(max_length=191)
    type = models.CharField(max_length=191, blank=True, null=True)
    title = models.CharField(max_length=191, blank=True, null=True)
    only_image = models.CharField(max_length=191, blank=True, null=True)
    background_image = models.CharField(max_length=191, blank=True, null=True)
    offer_time_end = models.CharField(max_length=191, blank=True, null=True)
    button_text = models.CharField(max_length=191, blank=True, null=True)
    button_link = models.CharField(max_length=191, blank=True, null=True)
    btn_status = models.CharField(max_length=191, blank=True, null=True)
    lang = models.CharField(max_length=191, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)

    def __str__(self):
        return self.name

class ProductCoupons(models.Model):
    code = models.CharField(max_length=191)
    discount = models.CharField(max_length=191, blank=True, null=True)
    discount_type = models.CharField(max_length=191, blank=True, null=True)
    expire_date = models.CharField(max_length=191, blank=True, null=True)
    status = models.CharField(max_length=191)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)

    def __str__(self):
        return self.discount

class ProductOrders(models.Model):

    status = models.CharField(max_length=191, blank=True, null=True)
    payment_status = models.CharField(max_length=191, blank=True, null=True)
    transaction_id = models.CharField(max_length=191, blank=True, null=True)
    payment_track = models.CharField(max_length=191, blank=True, null=True)
    payment_gateway = models.CharField(max_length=191, blank=True, null=True)
    user_id = models.CharField(max_length=191, blank=True, null=True)
    subtotal = models.CharField(max_length=191, blank=True, null=True)
    coupon_discount = models.CharField(max_length=191, blank=True, null=True)
    shipping_cost = models.CharField(max_length=191, blank=True, null=True)
    product_shippings_id = models.CharField(max_length=191, blank=True, null=True)
    total = models.CharField(max_length=191, blank=True, null=True)
    billing_name = models.TextField(blank=True, null=True)
    billing_email = models.TextField(blank=True, null=True)
    billing_phone = models.TextField(blank=True, null=True)
    billing_country = models.TextField(blank=True, null=True)
    billing_street_address = models.TextField(blank=True, null=True)
    billing_town = models.TextField(blank=True, null=True)
    billing_district = models.TextField(blank=True, null=True)
    different_shipping_address = models.TextField(blank=True, null=True)
    shipping_name = models.TextField(blank=True, null=True)
    shipping_email = models.TextField(blank=True, null=True)
    shipping_phone = models.TextField(blank=True, null=True)
    shipping_country = models.TextField(blank=True, null=True)
    shipping_street_address = models.TextField(blank=True, null=True)
    shipping_town = models.TextField(blank=True, null=True)
    shipping_district = models.TextField(blank=True, null=True)
    coupon_code = models.CharField(max_length=191, blank=True, null=True)
    cart_items = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)

    def __str__(self):
        return self.status


class ProductRatings(models.Model):

    ratings = models.IntegerField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    product_id = models.PositiveIntegerField()
    user_id = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)

    def __str__(self):
        return self.message

class ServiceCategories(models.Model):
    name = models.CharField(max_length=500,default=None,null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = _("Service Category")
        verbose_name_plural = _("Service Categories")

def servicefilename(instance, filename):
    ext = filename.split('.')[-1]
    filenm = os.path.splitext(filename)[0]
    filename = "%s_%s.%s" % (filenm,instance.name, ext)
    return os.path.join( 'services/'+filename)

class Service(models.Model):
    name = models.CharField(max_length=500)
    category = models.ForeignKey(ServiceCategories,max_length=100,null=True, on_delete=models.CASCADE)
    page = models.CharField(max_length=500,unique=True)
    image = models.FileField(upload_to = servicefilename ,max_length=255, null=True,blank=True)
    isActive = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)

    def settings_mode(self):
        return format_html(
            '<a class="btn" target="_blank" href="/admin/settings/{}/">Settings</a>',
            self.page,
        )
    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
    def __str__(self):
        return self.name

class Apartment_Unit(models.Model):
    name = models.CharField(max_length=500,null=False,unique=True)
    slug = models.CharField(max_length=500,null=True,)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Unit Type")
        verbose_name_plural = _("Unit Types")

    def __str__(self):
        return self.name

class Apartment_Categorie(models.Model):
    name = models.CharField(max_length=500,null=False,unique=False)
    type= models.ForeignKey(Apartment_Unit,max_length=100,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Sub Unit")
        verbose_name_plural = _("Sub Units")
    def __str__(self):
        return self.name

class Cities(models.Model):
    name = models.CharField(max_length=500,null=False,unique=True)
    country = models.CharField(max_length=500,null=True,)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Local City")
        verbose_name_plural = _("Local Cities")

    def __str__(self):
        return self.name

class Countries(models.Model):
    name = models.CharField(max_length=500,null=False,unique=True)
    slug = models.CharField(max_length=500,null=True,)
    created_at = models.DateField(default=datetime.datetime.today(), blank=True , null=True)
    updated_at = models.DateField(default=datetime.datetime.today(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Country List")
        verbose_name_plural = _("Country Lists")

    def __str__(self):
        return self.name


class Service_Section(models.Model):
    name = models.CharField(max_length=500)
    sec_label = models.CharField(max_length=500,default=None,null=True )
    base_price = models.CharField(max_length=500,default=None,null=True )
    invoice_price = models.BooleanField(default=True )
    sec_divs = models.CharField(max_length=500,default=None,null=True )
    service = models.ForeignKey(Service,max_length=100,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Service Section")
        verbose_name_plural = _("Service Sections")
    def __str__(self):
        return self.name


class About_Service(models.Model):
    description = models.CharField(max_length=500)
    points = models.CharField(max_length=500)
    sectionName = models.ForeignKey(Service_Section,max_length=100,null=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service,max_length=100,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("About Service")
        verbose_name_plural = _("About Services")
    def __str__(self):
        return self.description


class Description_Service(models.Model):
    question = models.CharField(max_length=500)
    placeholder = models.CharField(max_length=500)
    required = models.CharField(max_length=500,null=True,default=None)
    sectionName = models.ForeignKey(Service_Section,max_length=100,null=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service,max_length=100,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Description Service")
        verbose_name_plural = _("Description Services")
    def __str__(self):
        return self.question


class AddOn_Service(models.Model):
    serName = models.CharField(max_length=500)
    serPrice = models.CharField(max_length=500)
    adonpoints = models.CharField(max_length=1000,null=True,default=None)
    sectionName = models.ForeignKey(Service_Section,max_length=100,null=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service,max_length=100,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Add-On Service")
        verbose_name_plural = _("Add-On Services")
    def __str__(self):
        return self.serName

class RandoChoice_Service(models.Model):
    choiceques = models.CharField(max_length=500,default=None)
    cinvoiceName = models.CharField(max_length=500,default=None,null=True)
    multiple = models.BooleanField(max_length=500,default=None,null=True)
    serName = models.CharField(max_length=500)
    serNumber = models.CharField(max_length=500,null=True,default=None)
    sectionName = models.ForeignKey(Service_Section,max_length=100,null=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service,max_length=100,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Random Choice")
        verbose_name_plural = _("Random Choices")
    def __str__(self):
        return self.serName


class Offer_Service(models.Model):
    offquestion = models.CharField(max_length=800,default=None,null=True)
    offserName = models.CharField(max_length=500)
    offserperc = models.CharField(max_length=500)
    sectionName = models.ForeignKey(Service_Section,max_length=100,null=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service,max_length=100,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Offered Service")
        verbose_name_plural = _("Offered Services")
    def __str__(self):
        return self.offserName


class Choice_Service(models.Model):
    choicequestion = models.CharField(max_length=800,default=None,null=True)
    choicesubtext = models.CharField(max_length=800,default=None,null=True)
    MinBasePriceVal = models.CharField(max_length=800,default=None,null=True)
    invoiceName = models.CharField(max_length=800,default=None,null=True)
    basepricerel =  models.CharField(max_length=800,default=None,null=True)
    choiserName = models.CharField(max_length=500)
    choiserPrice = models.CharField(max_length=500)
    choiceType = models.CharField(max_length=500,default=None,null=True)
    popup = models.BooleanField(max_length=500,null=True,default=None)
    popuptext = models.CharField(max_length=500,null=True,default=None)
    choiseserNumber = models.CharField(max_length=500,null=True,default=None)
    sectionName = models.ForeignKey(Service_Section,max_length=100,null=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service,max_length=100,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Choice Service")
        verbose_name_plural = _("Choice Services")
    def __str__(self):
        return self.choiserName


class material_perHOur(models.Model):
    perHourRate = models.CharField(max_length=500,null=True,default=None)
    referencediv = models.CharField(max_length=500,null=True,default=None)
    referenceText = models.CharField(max_length=500,null=True,default=None)
    hourquestion = models.CharField(max_length=500,null=True,default=None)
    hourdescription = models.CharField(max_length=500,null=True,default=None)
    hourchoiceName = models.CharField(max_length=500,null=True,default=None)
    hourchoiceprice = models.CharField(max_length=500,null=True,default=None)
    invoiceName = models.CharField(max_length=500,null=True,default=None)
    serNumber = models.CharField(max_length=500,null=True,default=None)
    sectionName = models.ForeignKey(Service_Section,max_length=100,null=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service,max_length=100,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Hourly Rate Service")
        verbose_name_plural = _("Hourly Rate Services")
    def __str__(self):
        return self.perHourRate


class LocalAddre_Service(models.Model):
    locquesName = models.CharField(max_length=500)
    sectionName = models.ForeignKey(Service_Section,max_length=100,null=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service,max_length=100,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("LocalAddress Service")
        verbose_name_plural = _("LocalAddress Services")
    def __str__(self):
        return self.locquesName


class InternAddre_Service(models.Model):
    interquesName = models.CharField(max_length=500)
    sectionName = models.ForeignKey(Service_Section,max_length=100,null=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service,max_length=100,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("International Address Service")
        verbose_name_plural = _("International Address Services")
    def __str__(self):
        return self.interquesName
    
class Advance_Service(models.Model):
    servlist = models.CharField(max_length=800)
    sectionName = models.ForeignKey(Service_Section,max_length=100,null=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service,max_length=100,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Advance Service")
        verbose_name_plural = _("Advance Service")
    def __str__(self):
        return self.servlist


class Date_Service(models.Model):
    dquestion = models.CharField(max_length=800)
    drequired = models.CharField(max_length=500,null=True,default=None)
    sectionName = models.ForeignKey(Service_Section,max_length=100,null=True, on_delete=models.CASCADE)
    service = models.ForeignKey(Service,max_length=100,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Date Service")
        verbose_name_plural = _("Date Service")
    def __str__(self):
        return self.dquestion


class UsersAddress(models.Model):
    BOOL_CHOICES =[('Home', 'Home'),('Office', 'Office'),('Other', 'Other'),]
    _type =  models.CharField(max_length=10,choices=BOOL_CHOICES,default="",null=True)
    _country = models.ForeignKey(Countries,max_length=100,null=True, on_delete=models.CASCADE)
    _userid = models.ForeignKey(User,max_length=100,null=True, on_delete=models.CASCADE)
    _city = models.CharField(max_length=800,default=None,null=True)
    _building = models.CharField(max_length=800,default=None,null=True)
    _appartno = models.CharField(max_length=800,default=None,null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("User Address")
        verbose_name_plural = _("User Address")
    def __str__(self):
        return self._type


class User_Payment_Transaction(models.Model):
    _id =  models.CharField(max_length=800,default=None,null=True)
    _displayid = models.CharField(max_length=800,default=None,null=True)
    _checkoutKey = models.CharField(max_length=800,default=None,null=True)
    _requestId = models.CharField(max_length=800,default=None,null=True)
    _orderId = models.CharField(max_length=800,default=None,null=True)
    _currency = models.CharField(max_length=800,default=None,null=True)
    _amount = models.CharField(max_length=800,default=None,null=True)
    _cashAmount = models.CharField(max_length=800,default=None,null=True)
    _status = models.CharField(max_length=800,default=None,null=True)
    _totalRefunded = models.CharField(max_length=800,default=None,null=True)
    _usedPaymentMethod = models.CharField(max_length=800,default=None,null=True)
    _firebaseDocument = models.CharField(max_length=800,default=None,null=True)
    _timestamp = models.CharField(max_length=800,default=None,null=True)
    _userid = models.ForeignKey(User,max_length=100,null=True, on_delete=models.CASCADE)
    _addressid = models.ForeignKey(UsersAddress,max_length=100,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Payment Transactions")
        verbose_name_plural = _("Payment Transactions")
    def __str__(self):
        return self._requestId


class User_Booking_Details(models.Model):
    BOOL_CHOICES =[('cash', 'Cash Payment'),('card', 'Card Payment'),]
    cancelled_BOOL_CHOICES =[('admin', 'Admin'),('user', 'User'),]
    Status_CHOICES =[('pending', 'Waiting'),('approved', 'Approved'),('declined', 'Decline')]
    _confirm_id =  ShortUUIDField(length=16,max_length=16,alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ123456",primary_key=True,)
    _payment_mode = models.CharField(max_length=10,choices=BOOL_CHOICES,default="",null=True)
    _booking_status = models.CharField(max_length=10,choices=Status_CHOICES,default="",null=True)
    _service_name = models.CharField(max_length=800,default=None,null=True)
    _booking_id = models.CharField(max_length=800,default=None,null=True)
    _service_date = models.CharField(max_length=800,default=None,null=True)
    _service_time = models.CharField(max_length=800,default=None,null=True)
    _currency = models.CharField(max_length=800,default=None,null=True)
    _amount = models.CharField(max_length=800,default=None,null=True)
    _invoice_url = models.CharField(max_length=800,default=None,null=True)
    _cancelled_by = models.CharField(max_length=10,choices=cancelled_BOOL_CHOICES,default="",null=True)
    _Descriptions = models.CharField(max_length=800,default=None,null=True)
    _attachments = models.CharField(max_length=1500,default=None,null=True)
    _transaction_id= models.ForeignKey(User_Payment_Transaction,max_length=100,null=True, on_delete=models.CASCADE,default='', blank=True,)
    _userid = models.ForeignKey(User,max_length=100,null=True, on_delete=models.CASCADE)
    _addressid = models.ForeignKey(UsersAddress,max_length=100,null=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now(), blank=True , null=True)
    
    class Meta:
        verbose_name = _("Booking Detail")
        verbose_name_plural = _("Booking Details")
    def __str__(self):
        return self._booking_id


    




