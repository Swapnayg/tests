from contextlib import nullcontext
import email
from mailjet_rest import Client
import os
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import smtplib
import json
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout
from django.template import defaultfilters
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views import  View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
import requests
from fpdf import FPDF
from PyPDF2 import PdfFileWriter, PdfFileReader
import time
from requests.structures import CaseInsensitiveDict
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from numpy import true_divide
import shortuuid
from .tokens import account_activation_token
from django.urls import resolve
from NeatellerApp.models import Contactus, User
from django.core import serializers
from social_django.models import UserSocialAuth
from .models import About_Service, AddOn_Service, Advance_Service, Apartment_Categorie, Apartment_Unit, Choice_Service, Cities, Countries, Date_Service, Description_Service, InternAddre_Service, LocalAddre_Service, Offer_Service, User_Booking_Details,User_Payment_Transaction, RandoChoice_Service, Service, Service_Section, ServiceCategories, UsersAddress, material_perHOur
import pandas as pd
# Create your views here.

configuration = sib_api_v3_sdk.Configuration()

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


class index(View):
    return_url = None
    def get(self , request,Id=0):
        return render(request, 'index.html', {'services':  ServiceCategories.objects.all(),'socialuserName':request.user,'isAnosy':request.user.is_anonymous})

class about_View(View):
	return_url = None
	def get(self , request,Id=0):
		return render(request , 'about.html', {'services':  ServiceCategories.objects.all()})

class profile_View(View):
    return_url = None
    def get(self , request,Id=0):
        return render(request , 'userprofile.html', {'services':  ServiceCategories.objects.all()})

class locations_View(View):
    return_url = None
    def get(self , request,Id=0):

        return render(request , 'locations.html', {'services':  ServiceCategories.objects.all()})

class mybookings_View(View):
    return_url = None
    def get(self , request,Id=0):
        return render(request , 'mybookings.html', {'services':  ServiceCategories.objects.all()})

class mypayments_View(View):
    return_url = None
    def get(self , request,Id=0):
        return render(request , 'paymenthistory.html', {'services':  ServiceCategories.objects.all()})


class text_View(View):
    return_url = None
    def get(self , request,Id=0):
        return render(request , 'text.html')


class booking_View(View):
    return_url = None
    def get(self , request,Id=0):
        serviced = Service.objects.get(page=Id)
        return render(request , 'booking.html' , {'page':serviced.name,'image':serviced.image,'services':  ServiceCategories.objects.all()})

class page_Temp_View(View):
	return_url = None
	def get(self , request,Id=0):
		current_url = resolve(request.path_info).url_name
		category = ServiceCategories.objects.get(name = 'HOME')
		serviced = Service.objects.filter(category=category).order_by('?')[:4]
		return render(request , 'page_template.html',{'Service': 'HOME',"serlist":serviced,'services':  ServiceCategories.objects.all()})

class services_View(View):
	return_url = None
	def get(self , request,Id=0):
		return render(request , 'services.html',{'services':  ServiceCategories.objects.all()})


class terms_View(View):
	return_url = None
	def get(self , request,Id=0):
		return render(request , 'terms.html',{'services':  ServiceCategories.objects.all()})

class privary_View(View):
	return_url = None
	def get(self , request,Id=0):
		return render(request , 'privacy.html',{'services':  ServiceCategories.objects.all()})

class payment_View(View):
	return_url = None
	def get(self , request,Id=0):
		return render(request , 'payment.html',{'services':  ServiceCategories.objects.all()})

class sucess_View(View):
    return_url = None
    def get(self , request,Id=0):
        return render(request , 'sucess.html')

class contact_View(View):
	return_url = None
	def get(self , request,Id=0):
		return render(request , 'contact.html',{'services':  ServiceCategories.objects.all()})

def checkemail(request):
   if request.method == 'GET':  
        uemail = request.GET['uEmail']
        ouemail =  User.objects.filter(email=uemail.strip())
        if len(ouemail)!=0:
            result= "Exits"
        else:
            result= "Valid"
        return HttpResponse(result) 

	
@csrf_exempt
def pregister_view(request):
	if request.method == 'POST':
		ufName = request.POST.get("uFName")
		ulName = request.POST.get("uLName")
		uemail = request.POST.get("uEmail")
		upassword = request.POST.get("uPassword")
		register = User(username=ufName,first_name=ufName,last_name=ulName,email=uemail,password=make_password(upassword),is_active=True)
		register.save()
		return HttpResponse('Success.')

@csrf_exempt
def deladdresslist(request):
    if request.method == 'POST':
        uusername = request.POST.get("username")
        uu_id = request.POST.get("u_id")
        userDetails = User.objects.get(email = str(uusername).strip())
        UsersAddress.objects.filter(pk=uu_id, _userid= userDetails).delete()
        return HttpResponse('Success') 

class thankyou_View(View):
    return_url = None
    def get(self , request,Id=0,Id1=0):
        return render(request , 'Thankyou.html', {'services':  ServiceCategories.objects.all()})

@csrf_exempt
def create_paylink(request):
    if request.method == 'POST':
        url = "https://api.test.paymennt.com/mer/v2.0/checkout/web"
        headers = CaseInsensitiveDict()
        headers["X-PointCheckout-Api-Key"] = "1801769fcfc1d880"
        headers["X-PointCheckout-Api-Secret"] = "mer_b1baf6dc6a5232abfc251da78f1272a4921220e19703187d8790380f3e93845e"
        headers["Content-Type"] = "application/json"
        uniqid =   shortuuid.ShortUUID(alphabet="0123456789")
        uniqidstr = uniqid.random(length=8)
        requestId = 'CHK-'+ str(uniqidstr)+'-r1'
        orderid= 'CHK-'+str(uniqidstr)
        amount = str(request.POST.get("u_p_amount"))
        id = str(request.POST.get("u_p_id"))
        add_id = str(request.POST.get("u_p_add_id"))
        firstName = str(request.POST.get("u_p_firstName"))
        lastName = str(request.POST.get("u_p_lastName"))
        emailAddress = str(request.POST.get("u_p_email"))
        phoneNumer = str(request.POST.get("u_p_phone"))
        bulding =str(request.POST.get("u_p_bulding"))
        apartment = str(request.POST.get("u_p_apartment"))
        city = str(request.POST.get("u_p_city"))
        country = str(request.POST.get("u_p_country"))
        data = {
            "requestId": requestId,
            "orderId": orderid,
            "currency": "AED",
            "amount": int(amount),
            "totals": {
                "subtotal": int(amount),
                "tax": 5,
                "shipping": 3,
                "handling": 2,
                "discount": 10,
                "skipTotalsValidation": "true"
            },
            "items": [
            {
                "name": "Dark grey sunglasses",
                "sku": "1116521",
                "unitprice": int(amount),
                "quantity": 1,
                "linetotal": int(amount)
            }],
            "customer": {
                "id": id,
                "firstName": firstName,
                "lastName": lastName,
                "email": emailAddress,
                "phone": phoneNumer
            },
            "billingAddress": {
                "name": firstName + " " + lastName,
                "address1": apartment,
                "address2": bulding,
                "city": city,
                "state": city,
                "zip": "",
                "country": country
            },
            "deliveryAddress": {
                "name": firstName + " " + lastName,
                "address1": apartment,
                "address2": bulding,
                "city": city,
                "state": city,
                "zip": "",
                "country": country
            },
            "returnUrl": "http://127.0.0.1:8000/payment/sucess/" + requestId,
            "branchId": 0,
            "allowedPaymentMethods": [
                "CARD"
            ],
            "defaultPaymentMethod": "CARD",
            "language": "EN"
        }
        userDetails = User.objects.get(pk = str(id).strip())
        addrDetails = UsersAddress.objects.get(pk = str(add_id).strip())
        resp = requests.post(url, headers=headers, data=json.dumps(data, separators=(',', ':')))
        tmpObj = json.loads(resp.content)
        paytransaction = User_Payment_Transaction(_id=tmpObj["result"]["id"],_displayid=tmpObj["result"]["displayId"],_checkoutKey=tmpObj["result"]["checkoutKey"],_requestId=tmpObj["result"]["requestId"],_orderId=tmpObj["result"]["orderId"],_currency=tmpObj["result"]["currency"],_amount=tmpObj["result"]["amount"],_cashAmount=tmpObj["result"]["cashAmount"],_status=tmpObj["result"]["status"],_totalRefunded=tmpObj["result"]["totalRefunded"],_usedPaymentMethod=tmpObj["result"]["usedPaymentMethod"],_firebaseDocument=tmpObj["result"]["firebaseDocument"],_timestamp=tmpObj["result"]["timestamp"],_userid=userDetails,_addressid=addrDetails)
        paytransaction.save()
        tmpObj.update({'payment_transaction_id': paytransaction.pk})
        return HttpResponse(json.dumps(tmpObj))

@csrf_exempt
def updateaddresslist(request):
    if request.method == 'POST':
        uusername = request.POST.get("username")
        uu_type = request.POST.get("u_type")
        uu_id = request.POST.get("u_id")
        uu_country = request.POST.get("u_country")
        uu_city = request.POST.get("u_city")
        uu_building = request.POST.get("u_building")
        uu_appartno = request.POST.get("u_appartno")
        countryDetails = Countries.objects.get(slug = str(uu_country).strip())
        addaddress = UsersAddress.objects.get(pk = uu_id)
        addaddress._type = uu_type
        addaddress._country = countryDetails
        addaddress._city = uu_city
        addaddress._building = uu_building
        addaddress._appartno = uu_appartno
        addaddress.save()
        return HttpResponse('Success') 
@csrf_exempt
def addaddresslist(request):
    if request.method == 'POST':
        uusername = request.POST.get("username")
        uu_type = request.POST.get("u_type")
        uu_country = request.POST.get("u_country")
        uu_city = request.POST.get("u_city")
        uu_building = request.POST.get("u_building")
        uu_appartno = request.POST.get("u_appartno")
        userDetails = User.objects.get(email = str(uusername).strip())
        countryDetails = Countries.objects.get(slug = str(uu_country).strip())
        addaddress = UsersAddress(_type = uu_type,_country =countryDetails ,_userid=userDetails,_city=uu_city,_building=uu_building,_appartno=uu_appartno)
        addaddress.save()
        return HttpResponse('Success') 
@csrf_exempt
def profile_update_view(request):
    if request.method == 'POST':
        uUserName = request.POST.get("uusername")
        ufName = request.POST.get("uf_name")
        ulName = request.POST.get("ul_name")
        uemail = request.POST.get("uemail")
        uphone = request.POST.get("uphone")
        ucode = request.POST.get("udialcode")
        ucurrent_email = request.POST.get("ucurre_email")
        ucountry = request.POST.get("ucountry")
        complePhone = str(ucode.strip())+" " + str(uphone.strip());
        userDetails = User.objects.get(email = ucurrent_email)
        userDetails.username = uUserName
        userDetails.first_name = ufName
        userDetails.last_name = ulName
        userDetails.email = uemail
        userDetails.phoneNumber = complePhone
        userDetails.country = ucountry
        userDetails.save()
        return HttpResponse('Success')

def EmailSendFunction(sendmessage,toaddress,subject,cusName):
    sender = {"name":"support","email":"support@skillyservices.com"}
    to = [{"email":toaddress,"name":cusName}]
    cc = [{"email":"support@skillyservices.com","name":"support"}]
    reply_to = {"email":toaddress,"name":cusName}
    headers = {"SkillyServices":"unique-id-1234"}
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, cc=cc, reply_to=reply_to, headers=headers, html_content=sendmessage, sender=sender, subject=subject)
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
    return "success"

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

def logout_view(request):
    del request.session["userName"]
    return redirect('index')

def logout_social(request):
    logout(request)
    return redirect('index')

@csrf_exempt
def pLogin_view(request):
    if request.method == 'POST':
        useremail = request.POST.get('uEmail')
        passwrd = request.POST.get('uPassword')
        error_message = None
        user = authenticate(email=useremail, password=passwrd)
        if user is not None:
            userdetails = User.objects.get(email = useremail)
            if(userdetails.is_admin == False):
                request.session['userName'] =	userdetails.first_name
                request.session['userEmail'] =	userdetails.email
                error_message = "success"
        else:
            error_message = 'Invalid'
        return HttpResponse(error_message)

@csrf_exempt
def pContact_view(request):
	if request.method == 'POST':
		uf_name = request.POST.get('uf_name')
		ul_name = request.POST.get('ul_name')
		uemail = request.POST.get('uemail')
		uphone = request.POST.get('uphone')
		ucountry = request.POST.get('ucountry')
		udialcode = request.POST.get('udialcode')
		umessage = request.POST.get('umessage')
		fullName =uf_name.capitalize() + " " + ul_name.capitalize()
		phoneNumber = udialcode+ " " + uphone + " (" + ucountry + ") "
		contactdtls = Contactus(first_name=uf_name,last_name=ul_name,email=uemail,phone=uphone,country=ucountry,countrycode=udialcode,message=umessage,status='Received')
		contactdtls.save()
		ticket =  contactdtls.pk
		mail_content = """
<!doctype html>
<html lang="en-US">

<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <title>SkillY - Reset Password</title>
    <meta name="description" content="Reset Password Email Template.">
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
                                style="max-width:670px;background:#fff; border-radius:3px; text-align:center;-webkit-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);-moz-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);box-shadow:0 6px 18px 0 rgba(0,0,0,.06);">
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                                <tr>
                                    <td style="text-align:center;">
                                        <h1 style="color:#1e1e2d; font-weight:500; margin:0;font-size:32px;font-family:'Rubik',sans-serif;">Skilly Support</h1>
                                    </td>
                                </tr>
                                <tr style="text-align:left;">
                                  <td style="">    <span style="display:inline-block; vertical-align:middle; Padding:15px;">Thank you for contacting Skilly Support. Your request ("""+ticket+""") has been received and will be reviewed by our support staff.</span>
    <span style="display:inline-block; vertical-align:middle; Padding:15px;"> Kindly note that our email support hours are from 8:00AM to 7:00PM (Saturday to Thursday) and we will attempt to get back to you as soon as possible during business hours.</span>
	  <span style="display:inline-block; vertical-align:middle; Padding:15px;"> You can add additional comments to your request by replying to this email.</span>
	    
  </td> 
                                </tr>
								<tr style="text-align:left;">
                                   <span style="display:inline-block; vertical-align:middle; Padding:15px;">Thank you</span>
								</tr>
								<tr style="text-align:left;">
                               <span style="display:inline-block; vertical-align:middle; Padding:15px;">Support</span>
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
		mail_contentAdmin = """
<!doctype html>
<html lang="en-US">

<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <title>SkillY - Reset Password</title>
    <meta name="description" content="Reset Password Email Template.">
    <style type="text/css">
        a:hover {text-decoration: underline !important;}
    </style>
</head>

<body marginheight="0" topmargin="0" marginwidth="0" style="margin: 0px; background-color: #f2f3f8;" leftmargin="0">
    <table cellspacing="0" border="0" cellpadding="0" width="100%" bgcolor="#f2f3f8"
        style="@import url(https://fonts.googleapis.com/css?family=Rubik:300,400,500,600|Open+Sans:300,400,600,600); font-family: 'Open Sans', sans-serif;">
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
                                style="max-width:670px;background:#fff; border-radius:3px; text-align:center;-webkit-box-shadow:0 6px 14px 0 rgba(0,0,0,.06);-moz-box-shadow:0 6px 14px 0 rgba(0,0,0,.06);box-shadow:0 6px 14px 0 rgba(0,0,0,.06);">
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                                <tr>
                                    <td style="text-align:center;">
                                        <h1 style="color:#1e1e2d; font-weight:500; margin:0;font-size:32px;font-family:'Rubik',sans-serif;">Contact Received From:</h1>
                                    </td>
                                </tr>
                                <tr style="text-align:left;">
                                  <td style="">    <span style="display:inline-block; vertical-align:middle; Padding:20px;"><span style="font-weight:600;font-size:14px;">Ticket Number :</span> """+ticket+"""</span></td> 
                                </tr>
                                <tr style="text-align:left;">
                                  <td style="">    <span style="display:inline-block; vertical-align:middle; Padding:20px;"><span style="font-weight:600;font-size:14px;">Full Name :</span> """+fullName+"""</span></td> 
                                </tr>
                                <tr style="text-align:left;">
                                 <span style="display:inline-block; vertical-align:middle; Padding:20px;"><span style="font-weight:600;font-size:14px;">Email Address :</span> """+uemail+"""</span>
								</tr>
								<tr style="text-align:left;">
                                <span style="display:inline-block; vertical-align:middle; Padding:20px;"><span style="font-weight:600;font-size:14px;">Phone Number :</span> """+phoneNumber+"""</span>
								</tr>
								<tr style="text-align:left;">
                                <span style="display:inline-block; vertical-align:middle; Padding:20px;"><span style="font-weight:600;font-size:14px;">Message :</span> """+umessage.capitalize()+"""</span>
								</tr>
								<tr style="text-align:left;">
                                <span style="display:inline-block; vertical-align:middle; Padding:20px;">Thank you.</span>
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
                            <p style="font-size:14px; color:rgba(69, 80, 86, 0.7411764705882353); line-height:14px; margin:0 0 0;">&copy; <strong>www.skillyservices.com</strong></p>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:80px;">&nbsp;</td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>

</html>"""
		error_message = EmailSendFunction(mail_content,uemail,"Skilly - Support",fullName)
		error_message = EmailSendFunction(mail_contentAdmin,"infoswap90@gmail.com","Skilly - Contact Received",fullName)
		return HttpResponse("Success")



@csrf_exempt
def pForgot_view(request):
	if request.method == 'POST':
		useremail = request.POST.get('uEmail')
		error_message = None
		userdetails = User.objects.get(email =useremail)
		current_site = get_current_site(request)
		url = "http://" + current_site.domain + '''/reset/''' + str(urlsafe_base64_encode(force_bytes(userdetails.id))) + '''/''' + str(account_activation_token.make_token(userdetails))
		mail_content = """
		<!doctype html>
		<html lang="en-US">
		<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <title>SkillY - Reset Password</title>
    <meta name="description" content="Reset Password Email Template.">
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
                          <a href="www.skillyservices.com" title="logo" target="_blank">
                            <img width="250" src="https://i.ibb.co/RYDrTx7/site-logo1618651031.png" title="logo" alt="logo">
                          </a>
                        </td>
                    </tr>
                    <tr>
                        <td style="height:20px;">&nbsp;</td>
                    </tr>
                    <tr>
                        <td>
                            <table width="95%" border="0" align="center" cellpadding="0" cellspacing="0"
                                style="max-width:670px;background:#fff; border-radius:3px; text-align:center;-webkit-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);-moz-box-shadow:0 6px 18px 0 rgba(0,0,0,.06);box-shadow:0 6px 18px 0 rgba(0,0,0,.06);">
                                <tr>
                                    <td style="height:40px;">&nbsp;</td>
                                </tr>
                                <tr>
                                    <td style="padding:0 35px;">
                                        <h1 style="color:#1e1e2d; font-weight:500; margin:0;font-size:32px;font-family:'Rubik',sans-serif;">You have
                                            requested to reset your password</h1>
                                        <span
                                            style="display:inline-block; vertical-align:middle; margin:29px 0 26px; border-bottom:1px solid #cecece; width:100px;"></span>
                                        <p style="color:#455056; font-size:15px;line-height:24px; margin:0;">
                                            We cannot simply send you your old password. A unique link to reset your
                                            password has been generated for you. To reset your password, click the
                                            following link and follow the instructions.
                                        </p>
                                        <a href= """ + url + """
                                            style="background:#8d006b;text-decoration:none !important; font-weight:500; margin-top:35px; color:#fff;text-transform:uppercase; font-size:14px;padding:10px 24px;display:inline-block;border-radius:50px;">Reset
                                            Password</a>
                                    </td>
                                </tr>
								<tr>
                                    <td style="height:40px;">Note: above link is only valid for 24 Hours.</td>
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
</body>

</html>"""
		receiver_address = userdetails.email	
		error_message = EmailSendFunction(mail_content,userdetails.email,"Skilly - Reset Password",str(userdetails.first_name))
		return HttpResponse(error_message)


def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	print(account_activation_token.check_token(user, token))
	if user is not None and account_activation_token.check_token(user, token):
		return render(request , 'index.html')
	else:
		return HttpResponse('Activation link is invalid!')


def getemailtoken(request):
	if request.method == 'GET':
		uidb64 = request.GET['uid']
		token = request.GET['uuid']
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
		return HttpResponse(user.email)

@csrf_exempt
def pReset_view(request):
	if request.method == 'POST':
		token = request.POST.get('uuid')
		useremail = request.POST.get('uemail')
		passwrd = request.POST.get('upassword')
		error_message = None
		try:
			user = User.objects.get(email=useremail)
			user.password = make_password(passwrd.strip())
			user.save()
			#if(account_activation_token.check_token(user, token)):
			error_message = 'Success'
		except User.DoesNotExist:
			error_message = 'Invalid'
		return HttpResponse(error_message)

def service_View(request,Id=''):
	serviced = Service.objects.get(page=Id)
	category = ServiceCategories.objects.get(name = serviced.category)
	serviceList = Service.objects.filter(category=category ,isActive=True ).order_by('?')[:4]
	return render(request , 'services/'+Id+'.html',{'ServiceN': serviced.name,"serlist":serviceList,"serimage":serviced.image,'spage':Id, 'services':  ServiceCategories.objects.all()})


def serviceList_View(request):
   if request.method == 'GET':
       serviceList = ServiceCategories.objects.all()
       tmpsmtJson = serializers.serialize("json",serviceList)
       smttmpObj = json.loads(tmpsmtJson)
       return HttpResponse(json.dumps(smttmpObj))

def getApprtView(request):
   if request.method == 'GET':
       appList = Apartment_Unit.objects.all()
       tmpsmtJson = serializers.serialize("json",appList)
       smttmpObj = json.loads(tmpsmtJson)
       return HttpResponse(json.dumps(smttmpObj))


def getApprtCatView(request):
   if request.method == 'GET':
       appCatList = Apartment_Categorie.objects.all()
       tmpsmtJson = serializers.serialize("json",appCatList)
       smttmpObj = json.loads(tmpsmtJson)
       return HttpResponse(json.dumps(smttmpObj))

def getLocalAddressView(request):
   if request.method == 'GET':
       appList = Cities.objects.all()
       tmpsmtJson = serializers.serialize("json",appList)
       smttmpObj = json.loads(tmpsmtJson)
       return HttpResponse(json.dumps(smttmpObj))

def getInternAddressView(request):
   if request.method == 'GET':
       appList = Countries.objects.all()
       tmpsmtJson = serializers.serialize("json",appList)
       smttmpObj = json.loads(tmpsmtJson)
       return HttpResponse(json.dumps(smttmpObj))


@csrf_exempt
def Imgupload_view(request):
    if request.method == 'POST':
        files = request.FILES.getlist("files") 
        urls = []
        if len(files) != 0:
            for file in files:
                fs= FileSystemStorage(location= settings.MEDIA_ROOT +'/images/')
                file_path=fs.save(file.name.replace(' ','_'),file) 
                url = '/media/images/'+file_path
                urls.append(url)
        else:
            print('No File') 
        responseData = {'data':urls}
        return JsonResponse(responseData,safe=False)

@csrf_exempt
def addSection_view(request):
    if request.method == 'POST':
        udata = request.POST['udata']
        data = json.loads(udata)
        secids= []
        firstAdd = False
        for i, d in enumerate(data):
            usName = d["sName"]
            usLabel = d["sLabel"]
            usbprice = d["sbprice"]
            usinvoice = d["sbinvoice"]
            usdivs= d["sdivs"]
            usservice = d["sservice"]
            inval = ''
            if(usinvoice == 'true'):
                inval = True
            else:
                inval = False
            servName = Service.objects.get(name = usservice)
            if(Service_Section.objects.filter(service=servName).exists() and firstAdd == False):
                Service_Section.objects.filter(service=servName).delete()
                firstAdd = True
            else:
                firstAdd = True
            if(firstAdd == True): 
                secDtls = Service_Section(name=usName.strip(),sec_label=usLabel,base_price=usbprice,invoice_price=inval,sec_divs=usdivs,service=servName)
                secDtls.save()
                secids.append(str(secDtls.pk)) 
        return JsonResponse(json.dumps(secids),safe=False)

@csrf_exempt
def addAboutServ_view(request):
    if request.method == 'POST':
        udata = request.POST['udata']
        usectionid = request.POST.get('secIds')
        data = json.loads(udata)
        sdata = json.loads(usectionid)
        abtids= []
        firstAdd = False
        for i, d in enumerate(data):
            usaDesc = d["aDesc"]
            uaPoint = d["aPoint"]
            uaService = d["aService"]
            servName = Service.objects.get(name = uaService)
            usecNumber = d["secNmbr"]
            serSec = Service_Section.objects.get(pk = sdata[int(usecNumber)])
            if(About_Service.objects.filter(service=servName).exists() and firstAdd == False):
                About_Service.objects.filter(service=servName,sectionName=serSec).delete()
                firstAdd = True
            else:
                firstAdd = True
            if(firstAdd == True): 
                secDtls = About_Service(description=usaDesc.strip(),points=uaPoint,sectionName=serSec,service=servName)
                secDtls.save()
                abtids.append(str(secDtls.pk)) 
        return JsonResponse(json.dumps(abtids),safe=False)

@csrf_exempt
def addDescrServ_view(request):
   if request.method == 'POST':
        udata = request.POST['udata']
        usectionid = request.POST.get('secIds')
        data = json.loads(udata)
        sdata = json.loads(usectionid)
        Descids= []
        firstAdd = False
        for i, d in enumerate(data):
            udQues =  d["dQues"]
            udPlace =  d["dPlace"]
            udRequd=  d["dRequd"]
            udService =  d["dService"]
            servName = Service.objects.get(name = udService)
            usecNumber = d["secNmbr"]
            serSec = Service_Section.objects.get(pk = sdata[int(usecNumber)])
            if(Description_Service.objects.filter(service=servName).exists() and firstAdd == False):
                Description_Service.objects.filter(service=servName,sectionName=serSec).delete()
                firstAdd = True
            else:
                firstAdd = True
            if(firstAdd == True): 
                secDtls = Description_Service(question=udQues.strip(),placeholder=udPlace,required=udRequd,sectionName=serSec,service=servName)
                secDtls.save()
                Descids.append(str(secDtls.pk)) 
        return JsonResponse(json.dumps(Descids),safe=False)


@csrf_exempt
def addadonservServ_view(request):
   if request.method == 'POST':
        udata = request.POST['udata']
        usectionid = request.POST.get('secIds')
        data = json.loads(udata)
        sdata = json.loads(usectionid)
        Addonids= []
        firstAdd = False
        for i, d in enumerate(data):
            uaddonserName = d["addonserName"]
            uaddonserpoints = d["addonserPoints"]
            uaddonserprice = d["addonserprice"]
            udService = d["addService"]
            servName = Service.objects.get(name = udService)
            usecNumber = d["secNmbr"]
            serSec = Service_Section.objects.get(pk = sdata[int(usecNumber)])
            if(AddOn_Service.objects.filter(service=servName).exists() and firstAdd == False):
                AddOn_Service.objects.filter(service=servName,sectionName=serSec).delete()
                firstAdd = True
            else:
                firstAdd = True
            if(firstAdd == True): 
               for i, (price, name) in enumerate(zip(uaddonserName.split(","), uaddonserprice.split(","))):
                    secDtls = AddOn_Service(serName=name.strip(),serPrice=price,adonpoints=uaddonserpoints,sectionName=serSec,service=servName)
                    secDtls.save()
                    Addonids.append(str(secDtls.pk)) 
        return JsonResponse(json.dumps(Addonids),safe=False)


@csrf_exempt
def addofferServ_view(request):
   if request.method == 'POST':
        udata = request.POST['udata']
        usectionid = request.POST.get('secIds')
        data = json.loads(udata)
        sdata = json.loads(usectionid)
        offerids= []
        firstAdd = False
        for i, d in enumerate(data):
            uofferques = d["offerques"]
            uofferserName = d["offerserName"]
            uofferserper = d["offerserper"]
            uoffService = d["offService"]
            servName = Service.objects.get(name = uoffService)
            usecNumber = d["secNmbr"]
            serSec = Service_Section.objects.get(pk = sdata[int(usecNumber)])
            if(Offer_Service.objects.filter(service=servName,sectionName=serSec).exists() and firstAdd == False):
                Offer_Service.objects.filter(service=servName,sectionName=serSec).delete()
                firstAdd = True
            else:
                firstAdd = True
            if(firstAdd == True): 
                for j, (name,price) in enumerate(zip(uofferserName.split(","), uofferserper.split(","))):
                    secDtls = Offer_Service(offquestion=uofferques,offserName=name.strip(),offserperc=price,sectionName=serSec,service=servName)
                    secDtls.save()
                    offerids.append(str(secDtls.pk)) 
        return JsonResponse(json.dumps(offerids),safe=False)

@csrf_exempt
def addchoicServ_view(request):
   if request.method == 'POST':
        udata = request.POST['udata']
        usectionid = request.POST.get('secIds')
        data = json.loads(udata)
        sdata = json.loads(usectionid)
        choiceids= []
        firstAdd = False
        for i, d in enumerate(data):
            uchoiceques = d["choiceques"]
            uchoiceserName = d["choiceserName"]
            uchoicebaseprice = d["choicebaseprice"]
            uchoiceinvoiceName = d["choiceinvoiveName"]
            uchoicesersubText = d["choicesubtxt"]
            uchoicepoptxt = d["choicepoptxt"]
            uchoicepopreq = d["choicepopreq"]
            uchoiceminqty = d["choiceminqty"]
            uchoiceserper = d["choiceserper"]
            uchoiceserNumber = d["servNumb"]
            uoffService = d["choiceService"]
            uchoicediType = d["choicedistype"]
            servName = Service.objects.get(name = uoffService)
            usecNumber = d["secNmbr"]
            serSec = Service_Section.objects.get(pk = sdata[int(usecNumber)])
            if(Choice_Service.objects.filter(service=servName,sectionName=serSec).exists() and firstAdd == False):
                Choice_Service.objects.filter(service=servName,sectionName=serSec).delete()
                firstAdd = True
            else:
                firstAdd = True
            if(firstAdd == True): 
                for k, (cservName,cservPrice,ques,subtxt,poptext,popreq,minqty,serNumbr,invoiceNM,baseprice,ctype) in enumerate(zip(uchoiceserName.split(","),uchoiceserper.split(","),uchoiceques.split(","), uchoicesersubText.split(","),uchoicepoptxt.split(","),uchoicepopreq.split(","),uchoiceminqty.split(","),uchoiceserNumber.split(","),uchoiceinvoiceName.split(","),uchoicebaseprice.split(","),uchoicediType.split(","))):
                    for j , (sname,sprice) in enumerate(zip(cservName.split("~"),cservPrice.split("~"))):
                        if(len(sname.strip())!=0 and len(sprice.strip())!=0):
                            req = "1" if popreq.strip()  == 'Yes' else "0"
                            secDtls = Choice_Service(choicequestion=ques,invoiceName=invoiceNM,choiceType=ctype,basepricerel=baseprice,choicesubtext=subtxt,choiserName=sname.strip(),choiserPrice=sprice,MinBasePriceVal=minqty,popup=int(req),popuptext=poptext,choiseserNumber=serNumbr,sectionName=serSec,service=servName)
                            secDtls.save()
                            choiceids.append(str(secDtls.pk)) 
        return JsonResponse(json.dumps(choiceids),safe=False)


@csrf_exempt
def randChoice_view(request):
   if request.method == 'POST':
        udata = request.POST['udata']
        usectionid = request.POST.get('secIds')
        data = json.loads(udata)
        sdata = json.loads(usectionid)
        randids= []
        firstAdd = False
        for i, d in enumerate(data):
            uchoiceques = d["rchoiceques"]
            uchoiceNumbr = d["rchoicNumber"]
            uchoiceserName = d["rchoiceserName"]
            uchoiceinvoName = d["rchoiceinvoice"]
            urchoicemult = d["rchoicemult"]
            uoffService = d["choiceService"]
            servName = Service.objects.get(name = uoffService)
            usecNumber = d["secNmbr"]
            serSec = Service_Section.objects.get(pk = sdata[int(usecNumber)])
            if(RandoChoice_Service.objects.filter(service=servName,sectionName=serSec).exists() and firstAdd == False):
                RandoChoice_Service.objects.filter(service=servName,sectionName=serSec).delete()
                firstAdd = True
            else:
                firstAdd = True
            if(firstAdd == True): 
                for k, (ques,number,names,invoice,cmultiple) in enumerate(zip(uchoiceques.split(","), uchoiceNumbr.split(","), uchoiceserName.split(","),uchoiceinvoName.split(","),urchoicemult.split(","))):
                    for sname in names.split("~"):
                        if(len(sname.strip())!=0):
                            req = "1" if cmultiple.strip()  == 'Yes' else "0"
                            secDtls = RandoChoice_Service(cinvoiceName=invoice,choiceques=ques,serName=sname.strip(),multiple=req,serNumber=number,sectionName=serSec,service=servName)
                            secDtls.save()
                            randids.append(str(secDtls.pk)) 
        return JsonResponse(json.dumps(randids),safe=False)


@csrf_exempt
def add_hourrate_view(request):
   if request.method == 'POST':
        udata = request.POST['udata']
        usectionid = request.POST.get('secIds')
        data = json.loads(udata)
        sdata = json.loads(usectionid)
        hourids= []
        firstAdd = False
        for i, d in enumerate(data):
            uhourrateval = d["hourrateval"]
            uhourinName = d["hourinvName"]
            uhourrateques = d["hourrateques"]
            uhourratedesc = d["hourratedesc"]
            uhourratecprice = d["hourratecprice"]
            uhourratecname = d["hourratecname"]
            uhourrateChoice = d["hourrateChoice"]
            uhourratechoicediv = d["hourratechoicediv"]
            uhourchoicNumber = d["hourchoicNumber"]
            uchoiceService= d["choiceService"]
            servName = Service.objects.get(name = uchoiceService)
            usecNumber = d["secNmbr"]
            serSec = Service_Section.objects.get(pk = sdata[int(usecNumber)])
            if(material_perHOur.objects.filter(service=servName,sectionName=serSec).exists() and firstAdd == False):
                material_perHOur.objects.filter(service=servName,sectionName=serSec).delete()
                firstAdd = True
            else:
                firstAdd = True
            if(firstAdd == True): 
                for k, (hrate,hchoice,hdiv,hdivnumber,inName,desc,ques,price,name) in enumerate(zip(uhourrateval.split(","), uhourrateChoice.split(","), uhourratechoicediv.split(","), uhourchoicNumber.split(","), uhourinName.split(","), uhourratedesc.split(","), uhourrateques.split(","), uhourratecprice.split(","), uhourratecname.split(","))):
                    for j , (hprice,hname) in enumerate(zip(price.split("~"),name.split("~"))):
                        if(len(hrate.strip())!=0 and len(hchoice.strip())!=0 and len(hdiv.strip())!=0 and len(hdivnumber.strip())!=0 and len(inName.strip())!=0):
                            secDtls = material_perHOur(perHourRate=hrate,invoiceName=inName.strip(),hourquestion=ques.strip(),hourchoiceName=hname.strip(),hourchoiceprice=hprice.strip(),hourdescription=desc.strip(),referencediv=hdiv,referenceText=hchoice.strip(),serNumber=hdivnumber,sectionName=serSec,service=servName)
                            secDtls.save() 
                            hourids.append(str(secDtls.pk)) 
        return JsonResponse(json.dumps(hourids),safe=False)

@csrf_exempt
def addlocalServ_view(request):
    if request.method == 'POST':
        udata = request.POST['udata']
        usectionid = request.POST.get('secIds')
        data = json.loads(udata)
        sdata = json.loads(usectionid)
        localids= []
        firstAdd = False
        for i, d in enumerate(data):
            ulocalques = d["localaddques"]
            ulocalService = d["localService"]
            servName = Service.objects.get(name = ulocalService)
            usecNumber = d["secNmbr"]
            serSec = Service_Section.objects.get(pk = sdata[int(usecNumber)])
            if(LocalAddre_Service.objects.filter(service=servName,sectionName=serSec).exists() and firstAdd == False):
                LocalAddre_Service.objects.filter(service=servName,sectionName=serSec).delete()
                firstAdd = True
            else:
                firstAdd = True
            if(firstAdd == True): 
                for i, (question) in enumerate(ulocalques.split(",")):
                    secDtls = LocalAddre_Service(locquesName=question,sectionName=serSec,service=servName)
                    secDtls.save()
                    localids.append(str(secDtls.pk)) 
        return JsonResponse(json.dumps(localids),safe=False)

@csrf_exempt
def addinternalServ_view(request):
    if request.method == 'POST':
        udata = request.POST['udata']
        usectionid = request.POST.get('secIds')
        data = json.loads(udata)
        sdata = json.loads(usectionid)
        interids= []
        firstAdd = False
        for i, d in enumerate(data):
            uinternques = d["internaddques"]
            uinternService = d["internService"]
            servName = Service.objects.get(name = uinternService)
            usecNumber = d["secNmbr"]
            serSec = Service_Section.objects.get(pk = sdata[int(usecNumber)])
            if(InternAddre_Service.objects.filter(service=servName,sectionName=serSec).exists() and firstAdd == False):
                InternAddre_Service.objects.filter(service=servName,sectionName=serSec).delete()
                firstAdd = True
            else:
                firstAdd = True
            if(firstAdd == True): 
                for i, question in enumerate(uinternques.split(",")):
                    secDtls = InternAddre_Service(interquesName=question,sectionName=serSec,service=servName)
                    secDtls.save()
                    interids.append(str(secDtls.pk)) 
        return JsonResponse(json.dumps(interids),safe=False)

@csrf_exempt
def addadvanceServ_view(request):
    if request.method == 'POST':
        udata = request.POST['udata']
        usectionid = request.POST.get('secIds')
        data = json.loads(udata)
        sdata = json.loads(usectionid)
        servids= []
        firstAdd = False
        for i, d in enumerate(data):
            uadvanceques = d["advanceaddques"]
            uadvanceService = d["advanceService"]
            servName = Service.objects.get(name = uadvanceService)
            usecNumber = d["secNmbr"]
            serSec = Service_Section.objects.get(pk = sdata[int(usecNumber)])
            if(Advance_Service.objects.filter(service=servName,sectionName=serSec).exists() and firstAdd == False):
                Advance_Service.objects.filter(service=servName,sectionName=serSec).delete()
                firstAdd = True
            else:
                firstAdd = True
            if(firstAdd == True): 
                secDtls = Advance_Service(servlist=uadvanceques,sectionName=serSec,service=servName)
                secDtls.save()
                servids.append(str(secDtls.pk)) 
        return JsonResponse(json.dumps(servids),safe=False)


@csrf_exempt
def adddateServ_view(request):
    if request.method == 'POST':
        udata = request.POST['udata']
        usectionid = request.POST.get('secIds')
        data = json.loads(udata)
        sdata = json.loads(usectionid)
        dateids= []
        firstAdd = False
        for i, d in enumerate(data):
            udateques = d["dateddques"]
            udatereq = d["dateddrequd"]
            udateService = d["dateService"]
            servName = Service.objects.get(name = udateService)
            usecNumber = d["secNmbr"]
            serSec = Service_Section.objects.get(pk = sdata[int(usecNumber)])
            if(Date_Service.objects.filter(service=servName,sectionName=serSec).exists() and firstAdd == False):
                Date_Service.objects.filter(service=servName,sectionName=serSec).delete()
                firstAdd = True
            else:
                firstAdd = True
            if(firstAdd == True): 
                secDtls = Date_Service(dquestion=udateques,drequired=udatereq,sectionName=serSec,service=servName)
                secDtls.save()
                dateids.append(str(secDtls.pk)) 
        return JsonResponse(json.dumps(dateids),safe=False)

def getuserDetails(request):
    if request.method == 'GET':
        userName = request.GET['username']
        userDetails = User.objects.get(email = str(userName).strip())
        data = {'firstName':userDetails.first_name,'lastName':userDetails.last_name,'email':userDetails.email,'phone':userDetails.phoneNumber,'username':userDetails.username,'country':userDetails.country,'id':userDetails.pk}
        return JsonResponse(json.dumps(data),safe=False)

def getcountries(request):
    if request.method == 'GET':
        countryDetails = Countries.objects.all()
        tmpJson = serializers.serialize("json",countryDetails)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))


def getlocationDetails(request):
    if request.method == 'GET':
        userName = request.GET['username']
        userDetails = User.objects.get(email = str(userName).strip())
        locDetails = UsersAddress.objects.filter(_userid = userDetails).reverse()
        data = []
        for l in locDetails:
            countryDetails = Countries.objects.get(name=l._country.name)
            data.append({'u_id':l.pk,'u_type':l._type,'u_country':countryDetails.name,'u_country_id':l._country.pk,'u_country_code':countryDetails.slug,'u_city':l._city,'u_building':l._building,'u_appartno':l._appartno,'u_created':defaultfilters.date(l.created_at, "SHORT_DATETIME_FORMAT")})
        data.reverse()
        return HttpResponse(json.dumps(data))
    
def getpaymentDetails(request):
    if request.method == 'GET':
        userName = request.GET['username']
        userDetails = User.objects.get(email = str(userName).strip())
        payDetails = User_Payment_Transaction.objects.filter(_userid = userDetails).reverse()
        data = []
        for p in payDetails:
            data.append({'u_id':p.pk,'u_tran_id':p._checkoutKey,'u_order_id':p._orderId,'u_amount':p._amount,'u_currency':p._currency,'u_status':p._status,'u_created':defaultfilters.date(p.created_at, "SHORT_DATETIME_FORMAT")})
        data.reverse()
        return HttpResponse(json.dumps(data))

def getbookingsDetails(request):
    if request.method == 'GET':
        userName = request.GET['username']
        userDetails = User.objects.get(email = str(userName).strip())
        bookDetails = User_Booking_Details.objects.filter(_userid = userDetails).reverse()
        data = []
        for b in bookDetails:
            status = ''
            if(b._booking_status == 'pending'):
                status = 'Waiting For Approval'
            elif(b._booking_status == 'approved'):
                status = 'Approved by Admin'
            elif(b._booking_status == 'declined' and b._cancelled_by == 'user'):
                status = 'Cancelled by User'
            elif(b._booking_status == 'declined' and b._cancelled_by == 'admin'):
                status = 'Cancelled by Admin'
            data.append({'u_id':b.pk,'u_service_name':b._service_name,'u_order_id':b._booking_id,'u_amount':b._amount,'u_pay_mode':b._payment_mode,'u_status':status,'u_cancel_status':b._cancelled_by,'u_created':defaultfilters.date(b.created_at, "SHORT_DATETIME_FORMAT")})
        data.reverse()
        return HttpResponse(json.dumps(data))

def getservSection(request):
    if request.method == 'GET':
        servName = request.GET['serviceName']
        serDetails = Service.objects.get(name = servName)
        serSec = Service_Section.objects.filter(service = serDetails)
        tmpJson = serializers.serialize("json",serSec)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))

def getaboutSection(request):
    if request.method == 'GET':
        servName = request.GET['serName']
        secId = request.GET['secId']
        serDetails = Service.objects.get(name = servName)
        serSec = Service_Section.objects.get(pk = secId)
        aboutDetails = About_Service.objects.filter(service = serDetails,sectionName=serSec)
        tmpJson = serializers.serialize("json",aboutDetails)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))

def getdescSection(request):
    if request.method == 'GET':
        servName = request.GET['serName']
        secId = request.GET['secId']
        serDetails = Service.objects.get(name = servName)
        serSec = Service_Section.objects.get(pk = secId)
        aboutDetails = Description_Service.objects.filter(service = serDetails,sectionName=serSec)
        tmpJson = serializers.serialize("json",aboutDetails)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))

def getofferSection(request):
    if request.method == 'GET':
        servName = request.GET['serName']
        secId = request.GET['secId']
        serDetails = Service.objects.get(name = servName)
        serSec = Service_Section.objects.get(pk = secId)
        aboutDetails = Offer_Service.objects.filter(service = serDetails,sectionName=serSec)
        tmpJson = serializers.serialize("json",aboutDetails)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))

def getaddonSection(request):
    if request.method == 'GET':
        servName = request.GET['serName']
        secId = request.GET['secId']
        serDetails = Service.objects.get(name = servName)
        serSec = Service_Section.objects.get(pk = secId)
        addonDetails = AddOn_Service.objects.filter(service = serDetails,sectionName=serSec)
        tmpJson = serializers.serialize("json",addonDetails)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))

def getchoiceSection(request):
    if request.method == 'GET':
        servName = request.GET['serName']
        secId = request.GET['secId']
        serDetails = Service.objects.get(name = servName)
        serSec = Service_Section.objects.get(pk = secId)
        choiceDetails = Choice_Service.objects.filter(service = serDetails,sectionName=serSec).values('choicequestion','invoiceName','choicesubtext','MinBasePriceVal','basepricerel','choiserName','choiserPrice','popup','popuptext','choiseserNumber','sectionName','service','choiceType')
        df = pd.DataFrame(choiceDetails)
        data = []
        if(len(df) !=0):
            array_agg = lambda x: ','.join(x.astype(str))
            grp_df = df.groupby(['choicequestion', 'MinBasePriceVal', 'choicesubtext', 'popup', 'popuptext', 'choiseserNumber', 'invoiceName','basepricerel','choiceType']).agg({'choiserName': array_agg,'choiserPrice': array_agg})
            combvalues = grp_df.values.tolist()
            combvalueslist = []
            combvalueslist = combvalues
            combvalueslist.reverse()
            for i, (ques,minqty, subtxt,popup,poptxt,servNumb,inname,baseprice,ctype) in enumerate(reversed(grp_df.index)):
                middle_index = len(combvalueslist[i])/2
                first_half = combvalueslist[i][:int(middle_index)]
                second_half = combvalueslist[i][int(middle_index):]
                data.append({"cques":ques,"csubtxt":subtxt,"cMinQty":minqty,"cPopup":popup,"cpoptxt":poptxt,"cserNum":servNumb,"cinvName":inname,"cbaseprice":baseprice,"cmodetype":ctype,"sNames":str(",".join(first_half)),"sPrices":str(",".join(second_half))})
        return JsonResponse(json.dumps(data),safe=False)

def getRandomSection(request):
    if request.method == 'GET':
        servName = request.GET['serName']
        secId = request.GET['secId']
        serDetails = Service.objects.get(name = servName)
        serSec = Service_Section.objects.get(pk = secId)
        addonDetails = RandoChoice_Service.objects.filter(service = serDetails,sectionName=serSec).values('cinvoiceName','choiceques','serName','serNumber','multiple')
        df = pd.DataFrame(addonDetails)
        data = []
        if(len(df) !=0):
            array_agg = lambda x: ','.join(x.astype(str))
            grp_df = df.groupby(['cinvoiceName','choiceques', 'serNumber','multiple']).agg({'serName': array_agg})
            combvalues = grp_df.values.tolist()
            for i, (invoice,name, group,multiple) in enumerate(grp_df.index):
                data.append({"invoice":invoice,"name":name,"div":group,"multiple":multiple,"values":str(",".join(combvalues[i]))})
        return JsonResponse(json.dumps(data),safe=False)

def get_hoursectionSection(request):
    if request.method == 'GET':
        servName = request.GET['serName']
        secId = request.GET['secId']
        serDetails = Service.objects.get(name = servName)
        serSec = Service_Section.objects.get(pk = secId)
        addonDetails = material_perHOur.objects.filter(service = serDetails,sectionName=serSec).values('perHourRate','invoiceName','referencediv','referenceText','serNumber','hourquestion','hourdescription','hourchoiceName','hourchoiceprice')
        df = pd.DataFrame(addonDetails)
        data = []
        if(len(df) !=0):
            array_agg = lambda x: ','.join(x.astype(str))
            grp_df = df.groupby(['perHourRate', 'invoiceName', 'referencediv', 'referenceText', 'serNumber', 'hourquestion', 'hourdescription']).agg({'hourchoiceName': array_agg,'hourchoiceprice': array_agg})
            combvalues = grp_df.values.tolist()
            combvalueslist = []
            combvalueslist = combvalues
            combvalueslist.reverse()
            for i, (rate,inName, refDiv,refdivTxt,servNumb,hourque,hourdesc) in enumerate(reversed(grp_df.index)):
                middle_index = len(combvalueslist[i])/2
                first_half = combvalueslist[i][:int(middle_index)]
                second_half = combvalueslist[i][int(middle_index):]
                data.append({"HourRate":rate,"HourInvoice":inName,"referdiv":refDiv,"referText":refdivTxt,"serNumber":servNumb,"hourques":hourque,"hourDesc":hourdesc,"hNames":str(",".join(first_half)),"hPrices":str(",".join(second_half))})
        return JsonResponse(json.dumps(data),safe=False)


def getLocaladdrSection(request):
    if request.method == 'GET':
        servName = request.GET['serName']
        secId = request.GET['secId']
        serDetails = Service.objects.get(name = servName)
        serSec = Service_Section.objects.get(pk = secId)
        addonDetails = LocalAddre_Service.objects.filter(service = serDetails,sectionName=serSec)
        tmpJson = serializers.serialize("json",addonDetails)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))

def getInteraddrSection(request):
    if request.method == 'GET':
        servName = request.GET['serName']
        secId = request.GET['secId']
        serDetails = Service.objects.get(name = servName)
        serSec = Service_Section.objects.get(pk = secId)
        addonDetails = InternAddre_Service.objects.filter(service = serDetails,sectionName=serSec)
        tmpJson = serializers.serialize("json",addonDetails)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))


def getServiceSection(request):
    if request.method == 'GET':
        servName = request.GET['serName']
        secId = request.GET['secId']
        serDetails = Service.objects.get(name = servName)
        serSec = Service_Section.objects.get(pk = secId)
        addonDetails = Advance_Service.objects.filter(service = serDetails,sectionName=serSec)
        tmpJson = serializers.serialize("json",addonDetails)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))


def getDateSection(request):
    if request.method == 'GET':
        servName = request.GET['serName']
        secId = request.GET['secId']
        serDetails = Service.objects.get(name = servName)
        serSec = Service_Section.objects.get(pk = secId)
        addonDetails = Date_Service.objects.filter(service = serDetails,sectionName=serSec)
        tmpJson = serializers.serialize("json",addonDetails)
        tmpObj = json.loads(tmpJson)
        return HttpResponse(json.dumps(tmpObj))



@csrf_exempt
@require_http_methods(["POST"])
#@require_POST
def webhook_endpoint(request):
    str1 = ''
    if(request.method=='POST'):
        str1='POST'
        json_body = json.loads(request.body)
        refId = json_body['referenceId']
        status = json_body['status']
        orderid = json_body['orderId']
        paidOn = json_body['paidOn']
        paymentDetails = User_Payment_Transaction.objects.get(_requestId = refId,_orderId = orderid)
        paymentDetails._status = status
        paymentDetails._timestamp = status
        paymentDetails.save()
    return HttpResponse(str1,status=200)


def checkpayment(request):
       if request.method == 'GET':  
        requestid = request.GET['req_id']
        orderid = request.GET['ord_id']
        paymentDetails = User_Payment_Transaction.objects.get(_requestId = requestid,_orderId = orderid)
        return HttpResponse(paymentDetails._status) 

@csrf_exempt
def booking_confirmview(request):
    if request.method == 'POST':
        upersonDtls = request.POST['personalDetails']
        personalData = json.loads(upersonDtls)
        compleName = personalData[0]['FirstName'] +" " +personalData[0]['LastName'] 
        emailAddress = personalData[0]['EmailName'] 
        phoneNumber = personalData[0]['PhoneNumber'] 
        addressId = personalData[0]['AddressId'] 
        userId = personalData[0]['UserId']
        addrDetails = UsersAddress.objects.get(pk = str(addressId).strip())
        country = addrDetails._country.name
        city = addrDetails._city
        apart = addrDetails._appartno
        build = addrDetails._building
        userDetails = User.objects.get(pk = str(userId).strip())
        userDetails.first_name = personalData[0]['FirstName']
        uphone =personalData[0]['uphone']
        ucode = personalData[0]['udialcode']
        ucountry = personalData[0]['ucountry']
        complePhone = str(ucode.strip())+" " + str(uphone.strip());
        userDetails.phoneNumber = complePhone
        userDetails.country = ucountry
        userDetails.last_name =personalData[0]['LastName'] 
        userDetails.save()
        address1 = apart.capitalize() + "," + build.capitalize() + ","
        address2 = city.capitalize() + "," + country.capitalize() + ","
        userviceDtls = request.POST['serviceDetails']
        serviceData = json.loads(userviceDtls)
        upaymentDtls = request.POST['paymentDetails']
        paymentData = json.loads(upaymentDtls)
        address1 = apart.capitalize() + "," + build.capitalize() + ","
        address2 = city.capitalize() + "," + country.capitalize() + ","
        serviceDate = personalData[0]['serv_Date']
        serviceTime = personalData[0]['serv_Time']
        PaymentMode = personalData[0]['PaymentMode']
        serviceName = ''
        totalAmount = ''
        serRequ_id = ''
        serorder_id =''
        paymentText =''
        description =''
        imageurls =''
        transactionid = ''
        if(PaymentMode == "cash"):
            uniqid =   shortuuid.ShortUUID(alphabet="0123456789")
            uniqidstr = uniqid.random(length=8)
            serRequ_id ='CHK-'+ str(uniqidstr)+'-r1'
            serorder_id = 'CHK-'+str(uniqidstr)
            paymentText = 'Cash On Delivery'
            transactionid = None
        elif(PaymentMode == "card"):
            serRequ_id = personalData[0]['Pay_Req_Id']
            serorder_id = personalData[0]['Pay_Order_Id']
            paymentText = 'Credit/Debit Card'
            transactionid = User_Payment_Transaction.objects.get(pk = personalData[0]['transactionId'])
        pdf = FPDF()
        pdf.add_page()
        pdf.set_xy(160,80)
        pdf.set_font('arial','',10)
        pdf.cell(10)
        today_date =  time.strftime("%d, %B %Y")
        pdf.multi_cell( 100, 5,today_date)
        pdf.set_xy(10,100)
        pdf.set_font('arial','',10)
        pdf.cell(10)
        pdf.multi_cell( 100, 5,"To,")
        pdf.set_xy(10,105)
        pdf.set_font('arial','',10)
        pdf.cell(10)
        pdf.multi_cell( 100, 5,compleName)
        pdf.set_xy(10,110)
        pdf.set_font('arial','',10)
        pdf.cell(10)
        pdf.multi_cell( 100, 5,address1)
        pdf.set_xy(10,115)
        pdf.set_font('arial','',10)
        pdf.cell(10)
        pdf.multi_cell( 100, 5,address2)
        pdf.set_xy(10,120)
        pdf.set_font('arial')
        pdf.cell(10)
        pdf.multi_cell( 100, 5,emailAddress)
        pdf.set_xy(10,125)
        pdf.set_font('arial')
        pdf.cell(10)
        pdf.multi_cell( 100, 5,phoneNumber)
        pdf.set_draw_color(105,105,105)
        pdf.line(21, 135, 210-10, 135);
        pdf.set_xy(20,135)
        pdf.cell(100,12,"Service Details",0,0,'L');
        cellPoint = 143
        for i, s in enumerate(serviceData):
            keyName = list(s.keys())[0]
            keyValue = list(s.values())[0]
            if(keyName == "Service"):
                pdf.set_xy(25,cellPoint)
                pdf.set_font('arial','',9)
                pdf.cell(120,12,"Service Name",0,0,'L')
                pdf.cell(50,12,keyValue.capitalize(),0,0,'R')
                serviceName = keyValue.capitalize()
                cellPoint = cellPoint + 5
            elif(keyName == "Additional Services"):
                pdf.set_xy(25,cellPoint)
                pdf.set_font('arial','',9)
                pdf.cell(120,12,keyName,0,0,'L')
                pdf.cell(50,12,keyValue.capitalize(),0,0,'R')
                cellPoint = cellPoint + 5
            elif(keyName == "addservtxt"):
                pdf.set_xy(25,cellPoint)
                pdf.set_font('arial','',9)
                pdf.cell(120,12,keyValue.capitalize(),0,0,'L')
                cellPoint = cellPoint + 5
            elif(keyName == "Description"):
                pass
            elif(keyName == "image"):
                pass
            else:
                pdf.set_xy(25,cellPoint)
                pdf.set_font('arial','',9)
                pdf.cell(120,12,keyName,0,0,'L')
                pdf.cell(50,12,keyValue.capitalize(),0,0,'R')
                cellPoint = cellPoint + 5
        pdf.set_draw_color(105,105,105)
        pdf.line(21, cellPoint+5, 210-10, cellPoint+5)
        pdf.set_xy(20,cellPoint+6)
        pdf.cell(100,12,"Description",0,0,'L')
        for i, s in enumerate(serviceData):
            keyName = list(s.keys())[0]
            keyValue = list(s.values())[0]
            if(keyName == "Description"):
                pdf.set_xy(25,cellPoint+14)
                pdf.set_font('arial','',9)
                pdf.cell(120,12,keyValue.capitalize(),0,0,'L')
                cellPoint = cellPoint + 18
                description = keyValue
        pdf.set_draw_color(105,105,105)
        pdf.line(21, cellPoint+5, 210-10, cellPoint+5)
        pdf.set_xy(20,cellPoint+6)
        pdf.cell(100,12,"Attachments",0,0,'L')
        cellPoint = cellPoint+14
        for i, s in enumerate(serviceData):
            keyName = list(s.keys())[0]
            keyValue = list(s.values())[0]
            if(keyName == "image"):
                pdf.set_xy(25,cellPoint)
                pdf.set_font('arial','',9)
                pdf.cell(120,12,keyValue,0,0,'L')
                cellPoint = cellPoint + 5
                imageurls += keyValue + ","
        pdf.set_draw_color(105,105,105)
        pdf.line(21, cellPoint+5, 210-10, cellPoint+5)
        pdf.set_xy(20,cellPoint+6)
        pdf.cell(100,12,"Date & Time",0,0,'L')
        cellPoint = cellPoint+14
        pdf.set_xy(25,cellPoint)
        pdf.set_font('arial','',9)
        pdf.cell(120,12,"Service Date",0,0,'L')
        pdf.cell(50,12,serviceDate,0,0,'R')
        cellPoint = cellPoint + 5
        pdf.set_xy(25,cellPoint)
        pdf.set_font('arial','',9)
        pdf.cell(120,12,"Service Time",0,0,'L')
        pdf.cell(50,12,serviceTime,0,0,'R')
        cellPoint = cellPoint + 5    
        pdf.add_page();
        cellPoint = 60 
        pdf.set_xy(20,cellPoint+6)
        pdf.cell(100,12,"Address",0,0,'L')
        cellPoint = cellPoint+14
        pdf.set_xy(25,cellPoint)
        pdf.set_font('arial','',9)
        pdf.cell(120,12,address1 + " " + address2,0,0,'L')
        cellPoint = cellPoint + 5
        pdf.set_draw_color(105,105,105)
        pdf.line(21, cellPoint+5, 210-10, cellPoint+5)
        pdf.set_xy(20,cellPoint+6)
        pdf.cell(100,12,"Payment Method",0,0,'L')
        cellPoint = cellPoint+14
        pdf.set_xy(25,cellPoint)
        pdf.set_font('arial','',9)
        pdf.cell(120,12,"Payment Mode",0,0,'L')
        pdf.cell(50,12,paymentText,0,0,'R')
        cellPoint = cellPoint + 5
        pdf.set_xy(25,cellPoint)
        pdf.set_font('arial','',9)
        pdf.cell(120,12,"Request Number",0,0,'L')
        pdf.cell(50,12,serRequ_id,0,0,'R')
        cellPoint = cellPoint + 5   
        pdf.set_xy(25,cellPoint)
        pdf.set_font('arial','',9)
        pdf.cell(120,12,"Order Id",0,0,'L')
        pdf.cell(50,12,serorder_id,0,0,'R')
        cellPoint = cellPoint + 5  
        pdf.set_draw_color(105,105,105)
        pdf.line(21, cellPoint+5, 210-10, cellPoint+5)
        pdf.set_xy(20,cellPoint+6)
        pdf.cell(100,12,"Payment Details",0,0,'L')
        cellPoint = cellPoint+14 
        for i, p in enumerate(paymentData):
            keyName = list(p.keys())[0]
            keyValue = list(p.values())[0]
            if(keyName != "Total Price"):
                pdf.set_xy(25,cellPoint)
                pdf.set_font('arial','',9)
                pdf.cell(120,12,keyName,0,0,'L')
                pdf.cell(50,12,keyValue,0,0,'R')
                cellPoint = cellPoint + 5
        pdf.set_draw_color(105,105,105)
        pdf.line(21, cellPoint+10, 210-10, cellPoint+10)
        cellPoint = cellPoint+12
        for i, p in enumerate(paymentData):
            keyName = list(p.keys())[0]
            keyValue = list(p.values())[0]
            if(keyName == "Total Price"):
                pdf.set_xy(25,cellPoint)
                pdf.set_font('arial','',9)
                pdf.cell(120,12,"Total Price",0,0,'L')
                pdf.cell(50,12,keyValue,0,0,'R')
                totalAmount = keyValue
                cellPoint = cellPoint + 5
        pdf.output('test.pdf', 'F')
        new_pdf = PdfFileReader(open("test.pdf", "rb"))
        existing_pdf = PdfFileReader(open("skilly11.pdf", "rb"))
        existing_pdf1 = PdfFileReader(open("skilly22.pdf", "rb"))
        output = PdfFileWriter()
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        page1 = existing_pdf1.getPage(0)
        page1.mergePage(new_pdf.getPage(1))
        output.addPage(page)
        output.addPage(page1)
        pdfName = 'invoice_'+serorder_id+'.pdf'
        outputStream =  open(settings.MEDIA_ROOT+ '/invoice/'+pdfName,"wb")
        output.write(outputStream)
        outputStream.close()
        if(len(imageurls)== 0):
            imageurls = 'null'
        bookingDetails = User_Booking_Details(_payment_mode=PaymentMode,_booking_status='pending',_service_name=serviceName,_service_date=serviceDate,_service_time=serviceTime,_booking_id =serRequ_id,_currency='AED',_amount=totalAmount,_invoice_url='/invoice/'+pdfName,_Descriptions =description,_attachments = imageurls,_transaction_id = transactionid,_userid = userDetails,_addressid=addrDetails)
        bookingDetails.save()
        mail_content =  """
<!doctype html>
<html lang="en-US">

<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type" />
    <title>SkillY - Booking Details</title>
    <meta name="description" content="Booking Details.">
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
                                        <h1 style="color:#e424b7; font-weight:600; margin:0;font-size:28px;font-family:'Rubik',sans-serif;">Your booking request has been received</h1>
                                    </td>
                                </tr>
                                <tr style="text-align:left;">
                                  <td style="">    <span style="display:inline-block; vertical-align:middle; Padding:15px;">"""+compleName+""",</span>
    <span style="display:inline-block; vertical-align:middle; Padding:15px;padding-top: 0px;">Thank you for making a """+serviceName+""" service booking with Skilly Services! You will receive another email shortly confirming your booking.</span>
	  <span style="display:inline-block; vertical-align:middle; Padding:15px;padding-top: 0px;"> In the meantime, please go over your booking details and let us know if you would like to make any changes by replying to this email.</span>

        <span style="display:inline-block; vertical-align:middle; Padding:15px;padding-top: 0px;"> Invoice is attached below.</span>
	    
  </td> 
                                </tr>
                                <tr style="text-align:left;">
                                   <span style="display:inline-block; vertical-align:middle; Padding:15px;">If you have any questions, we're happy to help. Please reach out to us at support@skillyservices.com or +971 55 548 7771.</span>
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
        mail_content_admin = ''
        error_message = EmailSendwithAttachmentFunction(mail_content,emailAddress,"We have received your booking",compleName,pdfName)
        error_message = EmailSendwithAttachmentFunction(mail_content,'support@skillyservices.com',"We have received an new booking",compleName,pdfName)
        data = {'confirmId':bookingDetails._confirm_id,'bookingID':bookingDetails._booking_id,'PaymentMode':paymentText,'invoiceURL':'/media/invoice/'+pdfName}
        return HttpResponse(json.dumps(data))

@csrf_exempt
def cancel_bookingview(request):
    if request.method == 'POST':
        u_bookingId = request.POST['u_id']
        bookingDetails = User_Booking_Details.objects.get(_confirm_id = u_bookingId.strip())
        bookingDetails._booking_status = 'declined'
        bookingDetails._cancelled_by = 'user'
        bookingDetails.save()
        return HttpResponse('sucess')