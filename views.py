# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import django
import socket    
from string import Template
from datetime import datetime
import time
from django.http import Http404, HttpResponseRedirect, HttpResponse,JsonResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .utils import *
from django.db import transaction as transaction_atomic
import json
import requests
from .models import Credential
from django.conf import settings


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def hesabe_payment(req,amount,paymentType,args):
	error_dict = {
	0 :	'Invalid Response',
	422 :'Invalid Input',
	500 :'Invalid Token',
	501 :'Invalid Merchant',
	503 :'Invalid Merchant Service',
	504 :'Invalid Merchant Login Credentials',
	505 :'Invalid Payment Token',
	506 :'Invalid Request Data',
	507 :'Transaction Error'
	}
	with transaction_atomic.atomic():
		credential_obj = Credential.objects.all()
		try:
			if(len(credential_obj) == 1):
				merchantCode = credential_obj[0].merchant_code
				success_url = credential_obj[0].success_url
				failure_url = credential_obj[0].failure_url
				working_key = credential_obj[0].working_key
				iv = credential_obj[0].iv
				
				variable1 = args.get("variable1",None)
				variable2 = args.get("variable2",None)
				variable3 = args.get("variable3",None)
				variable4 = args.get("variable4",None)
				variable5 = args.get("variable5",None)
				orderReferenceNumber = args.get("order_id",None)
				data = {'merchantCode' : merchantCode,"orderReferenceNumber":orderReferenceNumber,"variable1":variable1,"variable2":variable2,"variable3":variable3,
						"variable4":variable4,"variable5":variable5, "paymentType": paymentType,"version":2.0,'amount':amount,'responseUrl':success_url,'failureUrl':failure_url }
				encryptedText = encrypt(str(json.dumps(data)), working_key , iv)
				checkoutToken = checkout(encryptedText)
				result = decrypt(checkoutToken,working_key,iv)
				response = json.loads(result)
				try:
					
					if response.get("status"):
						decryptToken = response['response']['data']
						url =  credential_obj[0].payment_url +"/payment"
						html = '''\
				            <html>
				            <head>
				                <title>Sub-merchant checkout page</title>
				                <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
				            </head>
				            <body>
				            <form id="nonseamless" method="get" name="redirect" action='$url'>
				                    <input type="hidden" id="data" name="data" value='$data'>
				                    <script language='javascript'>document.redirect.submit();</script>
				            </form>
				            </body>
				            </html>
				            '''
						fin = Template(html).safe_substitute(url=url,data=decryptToken)
						return django.http.HttpResponse(fin)
					elif response.get("status") == False :
						raise Exception(error_dict.get(response.get("code")))
					else:
						raise Exception('Merchant is inactive')
				except Exception as err:
					response = JsonResponse({"error": str(err)})
					response.status_code = 403 
					return response
		except Exception:
			response = JsonResponse({"error": 'Internal Server Error'})
			response.status_code = 403 
			return response



@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment(req):
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	hostname = socket.gethostname()    
	IPAddr = socket.gethostbyname(hostname) 
	# value of order_id should be Id of your order.    
	payment_variables = {
		"order_id"	: time.time(),
		"variable1" : current_time,
		"variable2" : None,
		"variable3" : None,
		"variable4" : None,
		"variable5" : IPAddr,
		"amount":10

	}
	return render(req, 'hesabe_app/pay.html',payment_variables)


@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def knet_payment(req,**kwargs):
	parameter = json.loads(req.POST.get('parameter'))
	try:

			amount = float(parameter.get('amount'))
	except:
		response = JsonResponse({"error": "Enter proper amount"})
		response.status_code = 403 
		return response
	del parameter["amount"]
	return hesabe_payment(req,amount, 1 ,parameter)


def mpgs_payment(req,**kwargs):
	parameter = json.loads(req.POST.get('parameter'))
	try:
		amount = float(parameter.get('amount'))
	except:
		response = JsonResponse({"error": "Enter proper amount"})
		response.status_code = 403 
		return response
	del parameter["amount"]
	return hesabe_payment(req,amount, 2 ,parameter)

@csrf_exempt
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def response(request):
	
	credential_obj = Credential.objects.all()
	if(len(credential_obj)==1):
		working_key = credential_obj[0].working_key
		iv =credential_obj[0].iv

	response = request.GET
	data = json.loads(decrypt(response.get('data'),working_key,iv))
	if(data.get('status') == 1):
		return django.http.JsonResponse(data.get('response'))
	elif(data.get('status') == 0):
		return django.http.JsonResponse(data.get('response'))
