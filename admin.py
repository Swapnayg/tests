from asyncio import format_helpers
from email import encoders
from email.mime.base import MIMEBase
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from importlib import resources
import smtplib
from django.conf import settings
from django.contrib import admin
from import_export.widgets import ForeignKeyWidget
from import_export import fields, resources, widgets
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.dispatch import receiver
from django.shortcuts import render

from .models import About_Service, AddOn_Service,User_Booking_Details, Advance_Service, Choice_Service, Date_Service, Description_Service, InternAddre_Service, LocalAddre_Service, Offer_Service, RandoChoice_Service, Service_Section, User, User_Payment_Transaction,material_perHOur
from .forms import UserChangeForm, UserCreationForm
from .models import Contactus
from .models import PopupBuilders
from .models import ProductCoupons
from .models import ProductOrders
from .models import ProductRatings
from .models import ServiceCategories
from .models import Service
from django.urls import URLPattern, path,include
from django.db.models.signals import post_save,pre_save
from .models import Apartment_Unit
from .models import Apartment_Categorie
from .models import Cities
from .models import Countries
from .models import UsersAddress
from import_export.admin import ExportActionMixin, ImportExportActionModelAdmin,ExportActionModelAdmin, ImportExportModelAdmin, ImportMixin


configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = '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'
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm


    list_display = ('email', 'username','first_name','last_name','phoneNumber','country', 'name', 'is_admin', 'is_staff', 'is_active')
    list_filter = ('is_admin', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'name', 'password')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'username', 'name')
    ordering = ('email',)
    filter_horizontal = ()

class AdminAdRolesModel(admin.ModelAdmin):
    list_display = ['name','username','email','email_verified','role','password','remember_token']

class AdminContact(admin.ModelAdmin):
    list_display = ['id','first_name','last_name','email','phone','country','countrycode','created_at']

class AdminServiceCategories(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['name','created_at','updated_at']

class AdminApartmet_Units(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['name','slug','created_at','updated_at']

class AdminUsers_Address(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['_type','_country','_city','_building','_userid','_appartno','created_at','updated_at']

class AdminUsers_Booking(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['_service_name','_booking_id','_confirm_id','_payment_mode','_booking_status','_invoice_url','created_at','updated_at']

class AdminPayments_Transactions(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['_id','_checkoutKey','_requestId','_orderId','_amount','_status','_userid','_addressid','created_at','updated_at']


class AdminApartmet_Category(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['name','type','created_at','updated_at']

class AdminCities(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['name','country','created_at','updated_at']


class AdminCountries(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['name','slug','created_at','updated_at']

class AdminService( ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['name','category','page','isActive', 'settings_mode']

class Service_sectionImportResource(resources.ModelResource):
    name = fields.Field(column_name='Name', attribute='name',
               widget=widgets.CharWidget())
    sec_label = fields.Field(column_name='Sec Label', attribute='sec_label',
               widget=widgets.CharWidget())
    base_price = fields.Field(column_name='Base Price', attribute='base_price',
               widget=widgets.CharWidget())
    invoice_price = fields.Field(column_name='Invoice Price', attribute='invoice_price',
               widget=widgets.CharWidget())
    sec_divs = fields.Field(column_name='Sec Divs', attribute='sec_divs',
               widget=widgets.CharWidget())
    service = fields.Field(column_name='Service', attribute='service',
               widget=widgets.ForeignKeyWidget(model=Service, field='name'))
    created_at = fields.Field(column_name='Created', attribute='created',
               widget=widgets.DateWidget('%d/%m/%Y'))
    updated_at = fields.Field(column_name='Updated', attribute='updated',
               widget=widgets.DateWidget('%d/%m/%Y'))
    class Meta:
        model = Service_Section
        fields = ('Id','Name','Sec Label','Base Price','Invoice Price','Sec Divs','Service','Created','Updated')
        exclude = ('id', 'created_at', 'updated_at')
        import_id_fields = ['name','sec_label','base_price','invoice_price','sec_divs','service']
        export_order = ('name','sec_label','base_price','invoice_price','sec_divs','service','created_at','updated_at')

class AdminServiceSections(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name','base_price','invoice_price','service','sec_divs','created_at','updated_at']
    def get_export_resource_class(self):
        return Service_sectionImportResource
    def get_import_resource_class(self):
        return Service_sectionImportResource

class About_serviceImportResource(resources.ModelResource):
    description = fields.Field(column_name='Description', attribute='description',
               widget=widgets.CharWidget())
    points = fields.Field(column_name='Points', attribute='points',
               widget=widgets.CharWidget())
    sectionName = fields.Field(column_name='Section', attribute='sectionName',
               widget=widgets.ForeignKeyWidget(model=Service_Section, field='name'))
    service = fields.Field(column_name='Service', attribute='service',
               widget=widgets.ForeignKeyWidget(model=Service, field='name'))
    created_at = fields.Field(column_name='Created', attribute='created',
               widget=widgets.DateWidget('%d/%m/%Y'))
    updated_at = fields.Field(column_name='Updated', attribute='updated',
               widget=widgets.DateWidget('%d/%m/%Y'))
    class Meta:
        model = About_Service
        fields = ('Id','Description','Points','Section','Service','Created','Updated')
        exclude = ('id', 'created_at', 'updated_at')
        import_id_fields = ['description','points','sectionName','service']
        export_order = ('description','points','sectionName','service')

class AdminAboutService( ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['description','points','sectionName','service','created_at','updated_at']
    def get_export_resource_class(self):
            return About_serviceImportResource
    def get_import_resource_class(self):
        return About_serviceImportResource


class Description_serviceImportResource(resources.ModelResource):
    question = fields.Field(column_name='Question', attribute='question',
               widget=widgets.CharWidget())
    placeholder = fields.Field(column_name='Placeholder', attribute='placeholder',
               widget=widgets.CharWidget())
    required = fields.Field(column_name='Required', attribute='required',
               widget=widgets.CharWidget())
    sectionName = fields.Field(column_name='Section', attribute='sectionName',
               widget=widgets.ForeignKeyWidget(model=Service_Section, field='name'))
    service = fields.Field(column_name='Service', attribute='service',
               widget=widgets.ForeignKeyWidget(model=Service, field='name'))
    created_at = fields.Field(column_name='Created', attribute='created',
               widget=widgets.DateWidget('%d/%m/%Y'))
    updated_at = fields.Field(column_name='Updated', attribute='updated',
               widget=widgets.DateWidget('%d/%m/%Y'))
    class Meta:
        model = Description_Service
        fields = ('Id','Question','Placeholder','Required','Section','Service','Created','Updated')
        exclude = ('id', 'created_at', 'updated_at')
        import_id_fields = ['question','placeholder','required','sectionName','service']
        export_order = ('question','placeholder','required','sectionName','service')

class AdminDescriptionService(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['question','placeholder','required','sectionName','service','created_at','updated_at']
    def get_export_resource_class(self):
            return Description_serviceImportResource
    def get_import_resource_class(self):
        return Description_serviceImportResource


class AdonService_serviceImportResource(resources.ModelResource):
    serName = fields.Field(column_name='SerName', attribute='serName',
               widget=widgets.CharWidget())
    serPrice = fields.Field(column_name='SerPrice', attribute='serPrice',
               widget=widgets.CharWidget())
    adonpoints = fields.Field(column_name='Adonpoints', attribute='adonpoints',
               widget=widgets.CharWidget())
    sectionName = fields.Field(column_name='Section', attribute='sectionName',
               widget=widgets.ForeignKeyWidget(model=Service_Section, field='name'))
    service = fields.Field(column_name='Service', attribute='service',
               widget=widgets.ForeignKeyWidget(model=Service, field='name'))
    created_at = fields.Field(column_name='Created', attribute='created',
               widget=widgets.DateWidget('%d/%m/%Y'))
    updated_at = fields.Field(column_name='Updated', attribute='updated',
               widget=widgets.DateWidget('%d/%m/%Y'))
    class Meta:
        model = AddOn_Service
        fields = ('Id','SerName','SerPrice','Adonpoints','Section','Service','Created','Updated')
        exclude = ('id', 'created_at', 'updated_at')
        import_id_fields = ['serName','serPrice','adonpoints','sectionName','service']
        export_order = ('serName','serPrice','adonpoints','sectionName','service')

class AdminAddOnService( ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['serName','serPrice','adonpoints','sectionName','service','created_at','updated_at']
    def get_export_resource_class(self):
            return AdonService_serviceImportResource
    def get_import_resource_class(self):
        return AdonService_serviceImportResource


class OfferService_serviceImportResource(resources.ModelResource):
    offquestion = fields.Field(column_name='Offquestion', attribute='offquestion',
               widget=widgets.CharWidget())
    offserName = fields.Field(column_name='OffserName', attribute='offserName',
               widget=widgets.CharWidget())
    offserperc = fields.Field(column_name='Offserperc', attribute='offserperc',
               widget=widgets.CharWidget())
    sectionName = fields.Field(column_name='Section', attribute='sectionName',
               widget=widgets.ForeignKeyWidget(model=Service_Section, field='name'))
    service = fields.Field(column_name='Service', attribute='service',
               widget=widgets.ForeignKeyWidget(model=Service, field='name'))
    created_at = fields.Field(column_name='Created', attribute='created',
               widget=widgets.DateWidget('%d/%m/%Y'))
    updated_at = fields.Field(column_name='Updated', attribute='updated',
               widget=widgets.DateWidget('%d/%m/%Y'))
    class Meta:
        model = Offer_Service
        fields = ('Id','Offquestion','OffserName','Offserperc','Section','Service','Created','Updated')
        exclude = ('id', 'created_at', 'updated_at')
        import_id_fields = ['offquestion','offserName','offserperc','sectionName','service']
        export_order = ('offquestion','offserName','offserperc','sectionName','service')

class AdminOfferService(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['offserName','offserperc','sectionName','service','created_at','updated_at']
    def get_export_resource_class(self):
            return OfferService_serviceImportResource
    def get_import_resource_class(self):
        return OfferService_serviceImportResource


class ChoiceService_serviceImportResource(resources.ModelResource):
    choicequestion = fields.Field(column_name='Choicequestion', attribute='choicequestion',
               widget=widgets.CharWidget())
    choicesubtext = fields.Field(column_name='Choicesubtext', attribute='choicesubtext',
               widget=widgets.CharWidget())
    MinBasePriceVal = fields.Field(column_name='MinBasePriceVal', attribute='MinBasePriceVal',
               widget=widgets.CharWidget())
    invoiceName = fields.Field(column_name='InvoiceName', attribute='invoiceName',
               widget=widgets.CharWidget())
    basepricerel = fields.Field(column_name='Basepricerel', attribute='basepricerel',
               widget=widgets.CharWidget())
    choiserName = fields.Field(column_name='ChoiserName', attribute='choiserName',
               widget=widgets.CharWidget())
    choiserPrice = fields.Field(column_name='ChoiserPrice', attribute='choiserPrice',
               widget=widgets.CharWidget())
    choiceType = fields.Field(column_name='ChoiceType', attribute='choiceType',
               widget=widgets.CharWidget())
    popup = fields.Field(column_name='Popup', attribute='popup',
               widget=widgets.CharWidget())
    popuptext = fields.Field(column_name='Popuptext', attribute='popuptext',
               widget=widgets.CharWidget())
    choiseserNumber = fields.Field(column_name='ChoiseserNumber', attribute='choiseserNumber',
               widget=widgets.CharWidget())
    sectionName = fields.Field(column_name='Section', attribute='sectionName',
               widget=widgets.ForeignKeyWidget(model=Service_Section, field='name'))
    service = fields.Field(column_name='Service', attribute='service',
               widget=widgets.ForeignKeyWidget(model=Service, field='name'))
    created_at = fields.Field(column_name='Created', attribute='created',
               widget=widgets.DateWidget('%d/%m/%Y'))
    updated_at = fields.Field(column_name='Updated', attribute='updated',
               widget=widgets.DateWidget('%d/%m/%Y'))
    class Meta:
        model = Choice_Service
        fields = ('Id','Choicequestion','Choicesubtext','MinBasePriceVal','InvoiceName','Basepricerel','ChoiserName','ChoiserPrice','ChoiceType','Popup','Popuptext','ChoiseserNumber','Section','Service','Created','Updated')
        exclude = ('id', 'created_at', 'updated_at')
        import_id_fields = ['choicequestion','choicesubtext','MinBasePriceVal','invoiceName','basepricerel','choiserName','choiserPrice','choiceType','popup','popuptext','choiseserNumber','sectionName','service']
        export_order = ('choicequestion','choicesubtext','MinBasePriceVal','invoiceName','basepricerel','choiserName','choiserPrice','choiceType','popup','popuptext','choiseserNumber','sectionName','service')

class AdminChoiceService(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['choiserName','invoiceName','basepricerel','choiceType','choicesubtext','MinBasePriceVal','choiserPrice','popup','popuptext','choiseserNumber','sectionName','service','created_at','updated_at']
    def get_export_resource_class(self):
            return ChoiceService_serviceImportResource
    def get_import_resource_class(self):
        return ChoiceService_serviceImportResource

class HourService_serviceImportResource(resources.ModelResource):
    perHourRate = fields.Field(column_name='PerHourRate', attribute='perHourRate',
               widget=widgets.CharWidget())
    referencediv = fields.Field(column_name='Referencediv', attribute='referencediv',
               widget=widgets.CharWidget())
    referenceText = fields.Field(column_name='ReferenceText', attribute='referenceText',
               widget=widgets.CharWidget())
    hourquestion = fields.Field(column_name='Hourquestion', attribute='hourquestion',
               widget=widgets.CharWidget())
    hourdescription = fields.Field(column_name='Hourdescription', attribute='hourdescription',
               widget=widgets.CharWidget())
    hourchoiceName = fields.Field(column_name='HourchoiceName', attribute='hourchoiceName',
               widget=widgets.CharWidget())
    hourchoiceprice = fields.Field(column_name='Hourchoiceprice', attribute='hourchoiceprice',
               widget=widgets.CharWidget())
    invoiceName = fields.Field(column_name='InvoiceName', attribute='invoiceName',
               widget=widgets.CharWidget())
    serNumber = fields.Field(column_name='SerNumber', attribute='serNumber',
               widget=widgets.CharWidget())
    sectionName = fields.Field(column_name='Section', attribute='sectionName',
               widget=widgets.ForeignKeyWidget(model=Service_Section, field='name'))
    service = fields.Field(column_name='Service', attribute='service',
               widget=widgets.ForeignKeyWidget(model=Service, field='name'))
    created_at = fields.Field(column_name='Created', attribute='created',
               widget=widgets.DateWidget('%d/%m/%Y'))
    updated_at = fields.Field(column_name='Updated', attribute='updated',
               widget=widgets.DateWidget('%d/%m/%Y'))
    class Meta:
        model = material_perHOur
        fields = ('Id','PerHourRate','Referencediv','ReferenceText','Hourquestion','Hourdescription','HourchoiceName','Hourchoiceprice','InvoiceName','SerNumber','Section','Service','Created','Updated')
        exclude = ('id', 'created_at', 'updated_at')
        import_id_fields = ['perHourRate','referencediv','referenceText','hourquestion','hourdescription','hourchoiceName','hourchoiceprice','invoiceName','serNumber','sectionName','service']
        export_order = ('perHourRate','referencediv','referenceText','hourquestion','hourdescription','hourchoiceName','hourchoiceprice','invoiceName','serNumber','sectionName','service')


class AdminHourRate(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['perHourRate','invoiceName','hourchoiceName','hourchoiceprice','referencediv','referenceText','serNumber','sectionName','service','created_at','updated_at']
    def get_export_resource_class(self):
            return HourService_serviceImportResource
    def get_import_resource_class(self):
        return HourService_serviceImportResource

class LocalService_serviceImportResource(resources.ModelResource):
    locquesName = fields.Field(column_name='LocquesName', attribute='locquesName',
               widget=widgets.CharWidget())
    sectionName = fields.Field(column_name='Section', attribute='sectionName',
               widget=widgets.ForeignKeyWidget(model=Service_Section, field='name'))
    service = fields.Field(column_name='Service', attribute='service',
               widget=widgets.ForeignKeyWidget(model=Service, field='name'))
    created_at = fields.Field(column_name='Created', attribute='created',
               widget=widgets.DateWidget('%d/%m/%Y'))
    updated_at = fields.Field(column_name='Updated', attribute='updated',
               widget=widgets.DateWidget('%d/%m/%Y'))
    class Meta:
        model = LocalAddre_Service
        fields = ('Id','LocquesName','Section','Service','Created','Updated')
        exclude = ('id', 'created_at', 'updated_at')
        import_id_fields = ['locquesName','sectionName','service']
        export_order = ('locquesName','sectionName','service')

class AdminLocalService(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['locquesName','sectionName','service','created_at','updated_at']
    def get_export_resource_class(self):
            return LocalService_serviceImportResource
    def get_import_resource_class(self):
        return LocalService_serviceImportResource


class InternationalService_serviceImportResource(resources.ModelResource):
    interquesName = fields.Field(column_name='InterquesName', attribute='interquesName',
               widget=widgets.CharWidget())
    sectionName = fields.Field(column_name='Section', attribute='sectionName',
               widget=widgets.ForeignKeyWidget(model=Service_Section, field='name'))
    service = fields.Field(column_name='Service', attribute='service',
               widget=widgets.ForeignKeyWidget(model=Service, field='name'))
    created_at = fields.Field(column_name='Created', attribute='created',
               widget=widgets.DateWidget('%d/%m/%Y'))
    updated_at = fields.Field(column_name='Updated', attribute='updated',
               widget=widgets.DateWidget('%d/%m/%Y'))
    class Meta:
        model = LocalAddre_Service
        fields = ('Id','InterquesName','Section','Service','Created','Updated')
        exclude = ('id', 'created_at', 'updated_at')
        import_id_fields = ['interquesName','sectionName','service']
        export_order = ('interquesName','sectionName','service')

class AdminInternalService(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['interquesName','sectionName','service','created_at','updated_at']
    def get_export_resource_class(self):
            return InternationalService_serviceImportResource
    def get_import_resource_class(self):
        return InternationalService_serviceImportResource

class AdvanceService_serviceImportResource(resources.ModelResource):
    servlist = fields.Field(column_name='Servlist', attribute='servlist',
               widget=widgets.CharWidget())
    sectionName = fields.Field(column_name='Section', attribute='sectionName',
               widget=widgets.ForeignKeyWidget(model=Service_Section, field='name'))
    service = fields.Field(column_name='Service', attribute='service',
               widget=widgets.ForeignKeyWidget(model=Service, field='name'))
    created_at = fields.Field(column_name='Created', attribute='created',
               widget=widgets.DateWidget('%d/%m/%Y'))
    updated_at = fields.Field(column_name='Updated', attribute='updated',
               widget=widgets.DateWidget('%d/%m/%Y'))
    class Meta:
        model = Advance_Service
        fields = ('Id','Servlist','Section','Service','Created','Updated')
        exclude = ('id', 'created_at', 'updated_at')
        import_id_fields = ['servlist','sectionName','service']
        export_order = ('servlist','sectionName','service')

class AdminAdvanceService( ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['servlist','sectionName','service','created_at','updated_at']
    def get_export_resource_class(self):
            return AdvanceService_serviceImportResource
    def get_import_resource_class(self):
        return AdvanceService_serviceImportResource

class RandomService_serviceImportResource(resources.ModelResource):
    choiceques = fields.Field(column_name='Choiceques', attribute='choiceques',
               widget=widgets.CharWidget())
    cinvoiceName = fields.Field(column_name='CinvoiceName', attribute='cinvoiceName',
               widget=widgets.CharWidget())
    multiple = fields.Field(column_name='Multiple', attribute='multiple',
               widget=widgets.CharWidget())
    serName = fields.Field(column_name='SerName', attribute='serName',
               widget=widgets.CharWidget())
    serNumber = fields.Field(column_name='SerNumber', attribute='serNumber',
               widget=widgets.CharWidget())
    sectionName = fields.Field(column_name='Section', attribute='sectionName',
               widget=widgets.ForeignKeyWidget(model=Service_Section, field='name'))
    service = fields.Field(column_name='Service', attribute='service',
               widget=widgets.ForeignKeyWidget(model=Service, field='name'))
    created_at = fields.Field(column_name='Created', attribute='created',
               widget=widgets.DateWidget('%d/%m/%Y'))
    updated_at = fields.Field(column_name='Updated', attribute='updated',
               widget=widgets.DateWidget('%d/%m/%Y'))
    class Meta:
        model = RandoChoice_Service
        fields = ('Id','Choiceques','CinvoiceName','Multiple','SerName','SerNumber','Section','Service','Created','Updated')
        exclude = ('id', 'created_at', 'updated_at')
        import_id_fields = ['choiceques','cinvoiceName','multiple','serName','serNumber','sectionName','service']
        export_order = ('choiceques','cinvoiceName','multiple','serName','serNumber','sectionName','service')

class AdminRandoChoice(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['cinvoiceName','choiceques','multiple','serName','serNumber','sectionName','service','created_at','updated_at']
    def get_export_resource_class(self):
            return RandomService_serviceImportResource
    def get_import_resource_class(self):
        return RandomService_serviceImportResource

class AdminDateService( admin.ModelAdmin):
    list_display = ['dquestion','drequired','sectionName','service','created_at','updated_at']

@receiver(post_save, sender=Service)
def add_page(sender, **kwargs):
    if kwargs['created']:
        service = Service.objects.get(id=kwargs.get('instance').id)
        pagename = service.page
        htmlcontent = open("NeatellerApp/templates/pagetemplates.html", "r", encoding='utf-8')
        source_code = htmlcontent.read() 
        with open(('NeatellerApp/templates/services/'+ pagename +'.html'), 'w+') as static_file:
            static_file.write(source_code)

@receiver(post_save, sender=User_Booking_Details)
def booking_status(sender, instance, **kwargs):
    if kwargs['created']:
        pass
    else:
        bookingupdate =  User_Booking_Details.objects.filter(_confirm_id=instance._confirm_id).update(_cancelled_by = 'admin')
        bookingDetails = User_Booking_Details.objects.get(_confirm_id=instance._confirm_id)
        if(bookingDetails._booking_status == 'approved'):
            b_userid = bookingDetails._userid
            userDetails = User.objects.get(email = str(b_userid).strip())
            fullName = userDetails.first_name.capitalize() + " " +  userDetails.last_name.capitalize()
            invoiceName = "invoice_"+bookingDetails._booking_id.replace("-r1",'') + ".pdf"
            emailAddress = userDetails.email
            ServiceDate = bookingDetails._service_date
            ServiceTime = bookingDetails._service_time
            mail_content =  """
                    <!doctype html>
                    <html lang="en-US">

                    <head>
                    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
                    <title>SkillY - Booking Confirmation Details</title>
                    <meta name="description" content="Booking Confirmation Details.">
                    <style type="text/css">
                        a:hover {text-decoration: underline !important;}
                    </style>
                    </head>

                    <body marginheight="0" topmargin="0" marginwidth="0" style="margin: 0px; background-color: #f2f3f8;" leftmargin="0">
                        <table cellspacing="0" border="0" cellpadding="0" width="100%" bgcolor="#f2f3f8"
                            style="@import url(https://fonts.googleapis.com/css?family=Rubik:300,400,500,700|Open+Sans:300,400,600,700); font-family: 'Open Sans', sans-serif;">
                            <tr>
                                <td>
                            <table style="background-color: #f2f3f8; max-width:670px;  margin:0 auto;" width="100%" border="0"
                                align="center" cellpadding="0" cellspacing="0">
                                 <tr>
                                        <td style="height:80px;">&nbsp;</td>
                                </tr>
                                <tr>
                                <td style="text-align:center;">
                                    <a href="https://i.ibb.co/RYDrTx7/site-logo1618651031.png" title="logo" target="_blank">
                            <img width="250" src="https://i.ibb.co/RYDrTx7/site-logo1618651031.png" title="logo" alt="logo">
                          </a>
                        </td>
                        </tr>
                        <tr>
                            <td style="height:20px;">&nbsp;</td>
                        </tr>
                        <tr>
                            <td>
                                <table width="95%" border="0" cellpadding="0" cellspacing="0"
                                    style="max-width:670px;background:#fff;padding: 5%;border-radius:3px; text-align:center;-webkit-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);-moz-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);box-shadow:0 6px 18px 0 rgba(0,0,0,.06);">
                                    <tr>
                                        <td style="height:40px;">&nbsp;</td>
                                    </tr>
                                    <tr>
                                        <td style="text-align:center;">
                                            <h1 style="color:#e424b7; font-weight:600; margin:0;font-size:28px;font-family:'Rubik',sans-serif;">Your booking is confirmed</h1>
                                        </td>
                                    </tr>
                                    <tr style="text-align:left;">
                                        <td style="">    <span style="display:inline-block; vertical-align:middle; Padding:15px;">"""+fullName+""",</span>
                                            <span style="display:inline-block; vertical-align:middle; Padding:15px;padding-top: 0px;">Your booking is confirmed and will be carried out on """+ServiceDate+""" at """+ServiceTime+""".</span>
	                                        <span style="display:inline-block; vertical-align:middle; Padding:15px;padding-top: 0px;"> If you need to change your booking please do so at least 24 hours before the job to avoid late cancellation fees. You can easily make changes to your booking by login to our <a href ="www.skillyservices.com" target="_blank">website</a>. </span>

                                           
	    
                                        </td> 
                                    </tr>
                                    <tr style="text-align:left;">
                                    <span style="display:inline-block; vertical-align:middle; Padding:15px;">If you have any questions, we're happy to help. Please reach out to us at sdz@skillyservices.com or +971 55 548 7771.</span>
								    </tr>
								    <tr style="text-align:left;">
                                    <span style="display:inline-block; vertical-align:middle; Padding:15px;font-style: italic;">Have a lovely day!</span>
								    </tr>
								    <tr style="text-align:left;">
                                <span style="display:inline-block; vertical-align:middle; Padding:15px;padding-top: 0px;">The Skilly Services Team</span>
								    </tr>
                                    <tr>
                                        <td style="height:40px;">&nbsp;</td>
                                    </tr>
                            </table>
                        </td>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td style="text-align:center;">
                            <p style="font-size:14px; color:rgba(69, 80, 86, 0.7411764705882353); line-height:18px; margin:0 0 0;">&copy; <strong>www.skillyservices.com</strong></p>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                </table>
            </td>
            </tr>
            </table>
            </body></html>"""
            error_message = EmailSendwithAttachmentFunction(mail_content,emailAddress,"Your booking is confirmed",fullName,invoiceName)
        elif(bookingDetails._booking_status=="declined"):
            pass
        else:
            pass


def EmailSendwithAttachmentFunction(sendmessage,toaddress,subject,cusName,invoiceName):
    sender = {"name":"support","email":"support@skillyservices.com"}
    to = [{"email":toaddress,"name":cusName}]
    cc = [{"email":"support@skillyservices.com","name":"support"}]
    reply_to = {"email":toaddress,"name":cusName}
    headers = {"SkillyServices":"unique-id-1234"}
    url = "http://127.0.0.1:8000/media/invoice/"+invoiceName
    attachment = [{"url":url, "name": invoiceName}]
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, cc=cc, reply_to=reply_to, headers=headers, html_content=sendmessage, sender=sender, subject=subject,attachment = attachment)
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
    return "success"

       
# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
admin.site.register(Contactus,AdminContact)
admin.site.register(ServiceCategories,AdminServiceCategories)
admin.site.register(Service,AdminService)
admin.site.register(Service_Section,AdminServiceSections)
admin.site.register(Apartment_Unit,AdminApartmet_Units)
admin.site.register(Apartment_Categorie,AdminApartmet_Category)
admin.site.register(Cities,AdminCities)
admin.site.register(Countries,AdminCountries)
admin.site.register(About_Service,AdminAboutService)
admin.site.register(Description_Service,AdminDescriptionService)

admin.site.register(AddOn_Service,AdminAddOnService)
admin.site.register(Offer_Service,AdminOfferService)
admin.site.register(Choice_Service,AdminChoiceService)
admin.site.register(material_perHOur,AdminHourRate)

admin.site.register(LocalAddre_Service,AdminLocalService)
admin.site.register(InternAddre_Service,AdminInternalService)

admin.site.register(Advance_Service,AdminAdvanceService)
admin.site.register(Date_Service,AdminDateService)
admin.site.register(RandoChoice_Service,AdminRandoChoice)
admin.site.register(UsersAddress,AdminUsers_Address)
admin.site.register(User_Payment_Transaction,AdminPayments_Transactions)

admin.site.register(User_Booking_Details,AdminUsers_Booking)

def get_admin_urls(urls):
    def get_urls():
        my_urls =  [
           path('settings/<str:Id>/', SettingsView,name='settings'), 
        ]
        return my_urls + urls
    return get_urls

admin.autodiscover()

admin_urls = get_admin_urls(admin.site.get_urls())
admin.site.get_urls = admin_urls

def SettingsView(request,Id=''):
    serviced = Service.objects.get(page=Id)
    return render(request , 'settings.html',{'page':serviced.name,'image':serviced.image})
