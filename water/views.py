from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from .forms import *

from .trapezia import *
from .superfunctions import *
from .models import *
import os
import sys
import smtplib
import email
import re
from HTMLParser import HTMLParser
import string
import imaplib
import base64
import datetime
import json
import django_tables2 as tables
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
from django.core import serializers
@ensure_csrf_cookie
@csrf_exempt
# Create your views here.


def menu(request):
	if request.user.is_authenticated():
		if (not request.user.is_superuser):
				check=check_for_template(request)
				if (check=='both'):
					return render(request,'water/menu.html')
				if (check=='cs'):
					return render(request,'water/menu_cs.html')
				if (check=='s'):
					return render(request,'water/menu_s.html')
				else:
					return HttpResponseRedirect('/account/login/')			
		
		else:
			########****SUPER USER*****#########
			return render(request,'water/superuser/menu.html')
	else:
		return HttpResponseRedirect('/account/login/')		



def statistics(request):
	if request.user.is_authenticated():
		if (not request.user.is_superuser):
			try:
				theuser=MyAppUser.objects.get(user=request.user)
				if (theuser.code_metapolishs and not theuser.code_paroxhs):
					data_sales=statistics_sales(request)
					return	render(request,'water/statistics_s.html',{'data':data_sales})
				elif (not theuser.code_metapolishs and theuser.code_paroxhs):
					data_customers_served=statistics_customers_served(request)
					return	render(request,'water/statistics_cs.html',{'data':data_customers_served})
				elif (theuser.code_metapolishs and theuser.code_paroxhs):
					data_customers_served=statistics_customers_served(request)
					data_sales=statistics_sales(request)
					return	render(request,'water/statistics.html',{'datas':data_sales,'datac':data_customers_served})	
				#post_stats.objects.filter(user=theuser).delete()
				else :
					return HttpResponseRedirect('/account/login/')
			except MyAppUser.DoesNotExist:
				return HttpResponseRedirect('/account/login/')
		else:				
			###########***SUPER USER****###########
			if request.method=='POST':
				form = profile_all(request.POST)
				if form.is_valid():
					seek=form.cleaned_data.get('user')
					return super_statistics(request,seek,form)
				else:
					form=profile_all()
					return	render(request,'water/superuser/statistics_get.html',{'form':form}) 
			else:
				form=profile_all()
				return	render(request,'water/superuser/statistics_get.html',{'form':form})
	else:
		return HttpResponseRedirect('/account/login/')


@csrf_exempt
def usersales(request):
	if request.user.is_authenticated():
		if (not request.user.is_superuser):
			check=check_for_template(request)
			if (check=='both'):
				if request.method=='POST' and request.is_ajax():
					month_fetch=request.POST['month']
					month=month_number(month_fetch)
					year=request.POST['year']
					dota=fetch_metapolishs_ajax(request,month,year)
					data=serializers.serialize('json',dota,fields=('id','Promo_Code','First_Name','Surname','Order_Date'))
					return HttpResponse(json.dumps({'data':data}),content_type="application/json")
				else:	
					now=datetime.datetime.now()
					try:
						data=fetch_metapolishs(request,now.month,now.year)
						mon=month_name(now.month)
						return render(request,'water/usersales.html',{'data':data,'month':mon,'year':str(now.year)})	
					except MyAppUser.DoesNotExist:
						return render(request,'water/usersales_error.html',{'month':"No records found"})	

			elif (check=='s'):
				if request.method=='POST' and request.is_ajax():
					month_fetch=request.POST['month']
					month=month_number(month_fetch)
					year=request.POST['year']
					dota=fetch_metapolishs_ajax(request,month,year)
					data=serializers.serialize('json',dota,fields=('id','Promo_Code','First_Name','Surname','Order_Date'))
					return HttpResponse(json.dumps({'data':data}),content_type="application/json")
				else:	
					now=datetime.datetime.now()
					try:
						data=fetch_metapolishs(request,now.month,now.year)
						mon=month_name(now.month)
						return render(request,'water/usersales_s.html',{'data':data,'month':mon,'year':str(now.year)})	
					except MyAppUser.DoesNotExist:
						return render(request,'water/usersales_error_s.html',{'month':"No records found"})

			elif (check=='cs'):
				return render(request,'water/usersales_error_cs.html',{'month':"No records found"})
			
			else:
				return HttpResponseRedirect('/account/login/')

		else:
			###########***SUPER USER****###########
			if request.method=='POST':
				if request.is_ajax():
					month_fetch=request.POST['month']
					month=month_number(month_fetch)
					year=request.POST['year']
					name=request.POST['name']
					dota=fetch_metapolishs_super_ajax(name,month,year)
					data=serializers.serialize('json',dota,fields=('id','Promo_Code','First_Name','Surname','Order_Date'))
					return HttpResponse(json.dumps({'data':data}),content_type="application/json")
				else:	
					form = profile_sales(request.POST)
					if form.is_valid():
						foruser=form.cleaned_data.get('user')
						now=datetime.datetime.now()
						try:
							data=fetch_metapolishs_super(foruser,now.month,now.year)
							mon=month_name(now.month)
							return render(request,'water/superuser/usersales.html',{'data':data,'month':mon,'year':str(now.year),'form':form})	
						except ValueError:
							return render(request,'water/usersales_error.html',{'month':"No records found"})
					else:
						form=profile_sales()	
						return	render(request,'water/superuser/usersales_get.html',{'form':form})		
			else:
				form=profile_sales()
				return	render(request,'water/superuser/usersales_get.html',{'form':form})
			return HttpResponseRedirect('/account/login/')
	
	else:
		return HttpResponseRedirect('/account/login/')
			
			
			
			
			
@csrf_exempt
def customersserved(request):
	if request.user.is_authenticated():
		if (not request.user.is_superuser):
			check=check_for_template(request)
			if (check=='both'):
				if request.method=='POST' and request.is_ajax():
					month_fetch=request.POST['month']
					month=month_number(month_fetch)
					year=request.POST['year']
					dota=fetch_paroxhs_ajax(request,month,year)
					data=serializers.serialize('json',dota,fields=('id','Promo_Code','First_Name','Surname','Order_Date'))
					return HttpResponse(json.dumps({'data':data}),content_type="application/json")
				else:	
					now=datetime.datetime.now()
					try:
						data=fetch_paroxhs(request,now.month,now.year)
						mon=month_name(now.month)
						return render(request,'water/customersserved.html',{'data':data,'month':mon,'year':str(now.year)})	
					except MyAppUser.DoesNotExist:
						return render(request,'water/usersales_error.html',{'month':"No records found"})

			elif (check=='cs'):
				if request.method=='POST' and request.is_ajax():
					month_fetch=request.POST['month']
					month=month_number(month_fetch)
					year=request.POST['year']
					dota=fetch_paroxhs_ajax(request,month,year)
					data=serializers.serialize('json',dota,fields=('id','Promo_Code','First_Name','Surname','Order_Date'))
					return HttpResponse(json.dumps({'data':data}),content_type="application/json")
				else:	
					now=datetime.datetime.now()
					try:
						data=fetch_paroxhs(request,now.month,now.year)
						mon=month_name(now.month)
						return render(request,'water/customersserved_cs.html',{'data':data,'month':mon,'year':str(now.year)})	
					except MyAppUser.DoesNotExist:
						return render(request,'water/usersales_error_cs.html',{'month':"No records found"})
		
			elif (check=='s'):
				return render(request,'water/usersales_error_s.html',{'month':"No records found"})
			
			else:
				return HttpResponseRedirect('/account/login/')

		else:
			###########***SUPER USER****###########
			if request.method=='POST':
				if request.is_ajax():
					month_fetch=request.POST['month']
					month=month_number(month_fetch)
					year=request.POST['year']
					name=request.POST['name']
					dota=fetch_paroxhs_super_ajax(name,month,year)
					data=serializers.serialize('json',dota,fields=('id','Promo_Code','First_Name','Surname','Order_Date'))
					return HttpResponse(json.dumps({'data':data}),content_type="application/json")
				else:	
					form = profile_customers_served(request.POST)
					if form.is_valid():
						foruser=form.cleaned_data.get('user')
						now=datetime.datetime.now()
						try:
							data=fetch_paroxhs_super(foruser,now.month,now.year)
							mon=month_name(now.month)
							return render(request,'water/superuser/customersserved.html',{'data':data,'month':mon,'year':str(now.year),'form':form})	
						except MyAppUser.DoesNotExist:
							return render(request,'water/usersales_error.html',{'month':"No records found"})
					else:
						form=profile_customers_served()	
						return	render(request,'water/superuser/customersserved_get.html',{'form':form})		
			else:
				form=profile_customers_served()
				return	render(request,'water/superuser/customersserved_get.html',{'form':form})
	else:
		return HttpResponseRedirect('/account/login/')



			
def promocodes(request):
	if request.user.is_authenticated():
		if not (request.user.is_superuser):
			check=check_for_template(request)
			if (check=='both'):
				try:
					timh1,timh2,timh3,orio1,orio2=fetch_pinaka(request)
					scale1=orio1+1
					scale2=orio2+1
					pososto_metapolishs=str(fetch_pinaka2(request)).strip("0.")
					if (len(pososto_metapolishs)==1):
						pososto_metapolishs=pososto_metapolishs+'0'
					return render(request,'water/promocodes.html',{'scale1':scale1,'scale2':scale2,'orio1':orio1,'orio2':orio2,'timh1':timh1,'timh2':timh2,'timh3':timh3,'pososto':pososto_metapolishs})
				except ValueError:
					return HttpResponseRedirect('water/menu.html')
			elif (check=='cs'):
				try:
					timh1,timh2,timh3,orio1,orio2=fetch_pinaka(request)
					scale1=orio1+1
					scale2=orio2+1
					return render(request,'water/promocodes_cs.html',{'scale1':scale1,'scale2':scale2,'orio1':orio1,'orio2':orio2,'timh1':timh1,'timh2':timh2,'timh3':timh3})
				except ValueError:
					return HttpResponseRedirect('water/menu.html')
			elif (check=='s'):
				try:
					pososto_metapolishs=str(fetch_pinaka2(request)).strip("0.")
					if (len(pososto_metapolishs)==1):
						pososto_metapolishs=pososto_metapolishs+'0'
					return render(request,'water/promocodes_s.html',{'pososto':pososto_metapolishs})
				except ValueError:
					return HttpResponseRedirect('water/menu.html')		
			else:
				return HttpResponseRedirect('/account/login/')
		else:
		###########***SUPER USER****###########
			if (request.method=='POST'):
				form=profile_all(request.POST)
				if (form.is_valid()):
					name=form.cleaned_data.get('user')
					return promocodes_super(request,name,form)
				else:
					form=profile_all()
					return render(request,'water/superuser/promocodes_get.html',{'form':form})
			else:
				form=profile_all()
				return render(request,'water/superuser/promocodes_get.html',{'form':form})				
	else:
		return HttpResponseRedirect('/account/login/')
	
	
	
def pinakas_timwn(request):
	if request.user.is_authenticated():
		if not (request.user.is_superuser):
			try:
				timh1,timh2,timh3,orio1,orio2=fetch_pinaka(request)
				pososto_metapolishs=str(fetch_pinaka2(request)).strip("0.")
				if (len(pososto_metapolishs)==1):
					pososto_metapolishs=pososto_metapolishs+'0'
				return render(request,'water/promocodes.html',{'orio1':orio1,'orio2':orio2,'timh1':timh1,'timh2':timh2,'timh3':timh3,'pososto':pososto_metapolishs})
			except ValueError:
				return HttpResponseRedirect('water/menu.html')
		else:
			return HttpResponseRedirect('/account/login/')	
				
				
				
def select_paroxhs(request):
	if request.user.is_authenticated():
		if not (request.user.is_superuser):
			form=search()
			return render(request,'water/paroxhs.html',{'form':form})
		else:
			form=search()
			user=profile()
			return render(request,'water/superparoxhs.html',{'form':form,'user':user})
	else:
			return HttpResponseRedirect('/account/login/')			


def select_metapolishs(request):
	if request.user.is_authenticated():
		if not (request.user.is_superuser):
			form=search()
			return render(request,'water/metapolishs.html',{'form':form})
		else:
			form=search()
			user=profile()
			return render(request,'water/supermetapolishs.html',{'form':form,'user':user})	
	else:
			return HttpResponseRedirect('/account/login/')					
				
				
def index(request):
	if request.user.is_authenticated():
		#data = request.user.username
		if (request.user.is_superuser):
			#data=super_table(Clients.objects.all())
			data=super_table(Clients.objects.filter(Q(Order_Date__year='2016') & Q(Order_Date__month=1)))
			
			return render(request,'water/home_super.html',{'data':data})
		else:
			form=search()
			used,message,data,cost=fetch_paroxhs(request)
			
			#used=user_table(Clients.objects.filter(connection_came_from__user=request.user))
			#message=Clients.objects.filter(connection_came_from__user=request.user).count()
			
			#notused=user_table(MyAppUser.objects.filter(Q(user=request.user) & Q(status='Not Used')))
			
			#used_r=MyAppUser.objects.filter(Q(user=request.user) & Q(status='Used'))
			#check_list=[]
			#for i in used_r:
				#check_list.append(i.code)
				#print i.code
			
			#f_names=user_clients_fnames(Clients.objects.filter(Promo_Code__in=check_list))
			#s_names=user_clients_snames(Clients.objects.filter(Promo_Code__in=check_list))
			#return render(request,'water/home.html',{'used':used,'notused':notused,'f_names':f_names,'s_names':s_names})
			return render(request,'water/home.html',{'form':form,'used':used,'data':data,'message':message,'cost':cost})
			
	else:
		return HttpResponseRedirect('/account/login/')



def month_paroxhs(request):
	if request.user.is_authenticated():
		#data = request.user.username
		if (request.user.is_superuser):
			form_completed = search(request.POST)
			users=profile(request.POST)
			if form_completed.is_valid() and users.is_valid():
				flip=form_completed.cleaned_data.get('onoma')
				date= flip.split()
				mon=month_number(date[0])
				year=date[1]
				for_user=users.cleaned_data.get('user')
				used,message,data,cost=fetch_paroxhs_super(for_user,mon,year)
				form=search(request.POST)
				users=profile(request.POST)
				return render(request,'water/supermonthparoxhs.html',{'form':form,'used':used,'data':data,'message':message,'cost':cost,'user':users})
			
		else:
			form_completed = search(request.POST)
			if form_completed.is_valid():
				flip=form_completed.cleaned_data.get('onoma')
				date= flip.split()
				mon=month_number(date[0])
				year=date[1]
				used,message,data,cost=fetch_paroxhs(request,mon,year)	
			form=search(request.POST)	
			return render(request,'water/monthparoxhs.html',{'form':form,'used':used,'data':data,'message':message,'cost':cost})
			
	else:
		return HttpResponseRedirect('/account/login/')



def month_metapolishs(request):
	if request.user.is_authenticated():
		#data = request.user.username
		if (request.user.is_superuser):
			form_completed = search(request.POST)
			users=profile(request.POST)
			if form_completed.is_valid() and users.is_valid():
				flip=form_completed.cleaned_data.get('onoma')
				date= flip.split()
				mon=month_number(date[0])
				year=date[1]
				for_user=users.cleaned_data.get('user')
				used,summ,data,cost=fetch_metapolishs_super(for_user,mon,year)
				pososto_metapolishs=str(cost).strip("0.")
				if (len(pososto_metapolishs)==1):
					pososto_metapolishs=pososto_metapolishs+'0'
				form=search(request.POST)	
				users=profile(request.POST)
			return render(request,'water/supermonthmetapolishs.html',{'form':form,'used':used,'data':data,'summ':summ,'cost':pososto_metapolishs,'user':users})
			
		else:
			form_completed = search(request.POST)
			if form_completed.is_valid():
				flip=form_completed.cleaned_data.get('onoma')
				date= flip.split()
				mon=month_number(date[0])
				year=date[1]
				used,summ,data,cost=fetch_metapolishs(request,mon,year)
				pososto_metapolishs=str(cost).strip("0.")
				if (len(pososto_metapolishs)==1):
					pososto_metapolishs=pososto_metapolishs+'0'	
			form=search(request.POST)	
			return render(request,'water/monthmetapolishs.html',{'form':form,'used':used,'data':data,'summ':summ,'cost':pososto_metapolishs})
			
	else:
		return HttpResponseRedirect('/account/login/')






def update_from_mail(request):
	if request.user.is_authenticated():
		#data = request.user.username
		if (request.user.is_superuser):
			update_data()
			data=update_table(Clients.objects.all().order_by('-Order_Date'))
			return render(request,'water/superuser/update.html',{'data':data})
		else:
			return HttpResponseRedirect('/account/login/')
			
	else:
		return HttpResponseRedirect('/account/login/')


def update_data():
	#SERVER = "imap.gmail.com"
	SERVER = "mail.butlair.com"
	#USER = "greekou@gmail.com"
	#USER = "djatlair.service@gmail.com"
	USER = "leonidas@butlair.com"
	PASSWORD = "l4(Lh+1*Pj"
	#PASSWORD = "marlboro29"



	mail = imaplib.IMAP4_SSL(SERVER)
	mail.login(USER, PASSWORD)


	mail.list()
	# Out: list of "folders" aka labels in gmail.
	mail.select("inbox") # connect to inbox.

	result, data = mail.search(None,'(SUBJECT "Butlair.com - Your Order has been placed")')
	ids = data[0] # data is a list.
	id_list = ids.split() # ids is a space separated string
	
	####################################
	all_mails=len(id_list)
	####################################
	
	for i in range(0,all_mails):
		raw_email=fetch_email(mail,id_list,i)
		info,num=fetch_data_from_email(raw_email)
		if (num==38):
			ar_date,serv_day,order_code,plat,f_name,sur,email,pay_stat,ord_date,soc_pro,soc_pro_name,pro_code,net_pri,dc,pay_fee,total=get_info(info,num)
			
			order_date=datetime.datetime.strptime(ord_date, '%d/%m/%Y')
			
			try:
				a=Clients.objects.get(Order_Code=order_code)
			except Clients.DoesNotExist:
				try:
					MyAppUser.objects.get(Q(code_paroxhs=pro_code) | Q(code_metapolishs=pro_code))
					try:
						obj_paroxhs=MyAppUser.objects.get(code_paroxhs=pro_code)
						if (obj_paroxhs):
							entry=Clients(Arrival_Date=ar_date,Service_Days=serv_day,Order_Code=order_code,Contact_App=plat,First_Name=f_name,Surname=sur,Email=email,Payment_Status=pay_stat,Order_Date=order_date,Social_Profile=soc_pro,Social_Profile_Name=soc_pro_name,Promo_Code=pro_code,Net_Price=net_pri,Discount=dc,Payment_Fee=pay_fee,Total=total,connection_came_from=obj_paroxhs,promo_kind_code='paroxhs')
							entry.save()
							obj=customers_served_calc(obj_paroxhs,order_date.month,order_date.year)
					except MyAppUser.DoesNotExist:	
						obj_metapolishs=MyAppUser.objects.get(code_metapolishs=pro_code)
					
						if (obj_metapolishs):
							entry=Clients(Arrival_Date=ar_date,Service_Days=serv_day,Order_Code=order_code,Contact_App=plat,First_Name=f_name,Surname=sur,Email=email,Payment_Status=pay_stat,Order_Date=order_date,Social_Profile=soc_pro,Social_Profile_Name=soc_pro_name,Promo_Code=pro_code,Net_Price=net_pri,Discount=dc,Payment_Fee=pay_fee,Total=total,connection_came_from=obj_metapolishs,promo_kind_code='metapolisis')
							entry.save()
							obj=sales_calc(obj_metapolishs,order_date.month,order_date.year,float(total))
				except MyAppUser.DoesNotExist:
					entry=Clients(Arrival_Date=ar_date,Service_Days=serv_day,Order_Code=order_code,Contact_App=plat,First_Name=f_name,Surname=sur,Email=email,Payment_Status=pay_stat,Order_Date=order_date,Social_Profile=soc_pro,Social_Profile_Name=soc_pro_name,Promo_Code=pro_code,Net_Price=net_pri,Discount=dc,Payment_Fee=pay_fee,Total=total)
					entry.save()	
		else:
			 ar_date,serv_day,order_code,plat,f_name,sur,email,pay_stat,ord_date,soc_pro,soc_pro_name,net_pri,dc,pay_fee,total=get_info(info,num)
			 a=Clients.objects.filter(Order_Code=order_code)
			 if not a:
				 order_date=datetime.datetime.strptime(ord_date, '%d/%m/%Y')
				 entry=Clients(Arrival_Date=ar_date,Service_Days=serv_day,Order_Code=order_code,Contact_App=plat,First_Name=f_name,Surname=sur,Email=email,Payment_Status=pay_stat,Order_Date=order_date,Social_Profile=soc_pro,Social_Profile_Name=soc_pro_name,Promo_Code='-',Net_Price=net_pri,Discount=dc,Payment_Fee=pay_fee,Total=total)
				 entry.save()
				 
				 
				 
					
	mail.close()
	mail.logout()
	




