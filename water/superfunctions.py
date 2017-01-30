from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q

from .models import *
from .forms import *
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
import django_tables2 as tables
from .trapezia import *

@ensure_csrf_cookie
@csrf_exempt

# Create your views here.

######### STATISTICS ###############
def super_statistics(request,foruser,form):
	try:
		theuser=MyAppUser.objects.get(user__username=foruser)
		if (theuser.code_metapolishs and not theuser.code_paroxhs):
			data_sales=statistics_sales_super(theuser)
			return	render(request,'water/superuser/statistics_s.html',{'data':data_sales,'form':form})
		elif (not theuser.code_metapolishs and theuser.code_paroxhs):
			data_customers_served=statistics_customers_served_super(theuser)
			return	render(request,'water/superuser/statistics_cs.html',{'data':data_customers_served,'form':form})
		elif (theuser.code_metapolishs and theuser.code_paroxhs):
			data_customers_served=statistics_customers_served_super(theuser)
			data_sales=statistics_sales_super(theuser)
			return	render(request,'water/superuser/statistics.html',{'datas':data_sales,'datac':data_customers_served,'form':form})	
		#post_stats.objects.filter(user=theuser).delete()
		else :
			return HttpResponseRedirect('/account/login/')
	except MyAppUser.DoesNotExist:
		return HttpResponseRedirect('/account/login/')

def statistics_sales_super(theuser):
	#theuser=MyAppUser.objects.get(user=foruser)
	post_stats_sales.objects.filter(user=theuser).delete()
	usersstatistics=sales.objects.filter(user=theuser).order_by('fordate')
	
	#counter=sales.objects.filter(user=theuser).count()
	
	for foo in usersstatistics:
		monthdate=(foo.fordate).month
		yeardate=(foo.fordate).year
		stringmonth=month_name(monthdate)
		final_date= stringmonth + " "+ str(yeardate)
		stat=post_stats_sales(user=theuser,month=final_date,no_of_sales=foo.no_of_sales,commission=foo.commission,settled=foo.settled)
		stat.save()
		#print stat.month
	dota=post_stats_sales.objects.filter(user=theuser)
	data=user_statistics_sales(dota)
	return data

def statistics_customers_served_super(theuser):
	#theuser=MyAppUser.objects.get(user=foruser)
	post_stats_customers_served.objects.filter(user=theuser).delete()
	usersstatistics=customers_served.objects.filter(user=theuser).order_by('fordate')
	
	#counter=sales.objects.filter(user=theuser).count()
	
	for foo in usersstatistics:
		monthdate=(foo.fordate).month
		yeardate=(foo.fordate).year
		stringmonth=month_name(monthdate)
		final_date= stringmonth + " "+ str(yeardate)
		stat=post_stats_customers_served(user=theuser,month=final_date,no_of_guests_served=foo.no_of_sales,total_cost=foo.total_cost,settled=foo.settled)
		stat.save()
		#print stat.month
	dota=post_stats_customers_served.objects.filter(user=theuser)
	data=user_statistics_customers_served(dota)
	return data	

#############################################################

############# SALES #########################################

def fetch_metapolishs_super_ajax(foruser,mon,year):
	
	seek=MyAppUser.objects.get(user__username=foruser)
	board=Clients.objects.filter(Q(connection_came_from__user=seek.user) & Q(promo_kind_code='metapolisis') & Q(Order_Date__year=year) & Q(Order_Date__month=mon))
	summ=0
	for i in board:
		summ=summ+float(i.Total)
	#used=user_sales_table(board)
	message=board.count()
	user=MyAppUser.objects.get(user=seek.user)
	data=summ*user.price_metapolishs
	cost_of_cat=user.price_metapolishs
	return board			
########################################################


###################CUSTOMERS SERVED##########################

def fetch_paroxhs_super_ajax(foruser,mon,year):
	seek=MyAppUser.objects.get(user__username=foruser)
	board=Clients.objects.filter(Q(connection_came_from__user=seek.user) & Q(promo_kind_code='paroxhs') & Q(Order_Date__year=year) & Q(Order_Date__month=mon))
	#used=user_sales_table(board)
	message=board.count()
	user=MyAppUser.objects.get(user=seek.user)
	cat_id=user.price_per_traveler.id
	cat=Number_of_travelers.objects.get(id=cat_id)
	data=message*cat.Cost_per_traveler_prwths_kathgorias
	cost_of_cat=cat.Cost_per_traveler_prwths_kathgorias
	if (message>cat.maximum_travelers_prwths_kathgorias):
		data=message*cat.Cost_per_traveler_deuterhs_kathgorias
		cost_of_cat=cat.Cost_per_traveler_deuterhs_kathgorias
		if (message>cat.maximum_travelers_deuterhs_kathgorias):
			data=message*cat.Cost_per_traveler_triths_kathgorias
			cost_of_cat=cat.Cost_per_traveler_triths_kathgorias
	return board

##############################################################

##############PROMO CODES#####################################

def promocodes_super(request,foruser,form):
	theuser=MyAppUser.objects.get(user__username=foruser)
	check=check_for_template_super(theuser)
	if (check=='both'):
		try:
			timh1,timh2,timh3,orio1,orio2=fetch_times_paroxhs(theuser)
			scale1=orio1+1
			scale2=orio2+1
			pososto_metapolishs=str(fetch_pinaka2(theuser)).strip("0.")
			if (len(pososto_metapolishs)==1):
				pososto_metapolishs=pososto_metapolishs+'0'
			return render(request,'water/superuser/promocodes.html',{'form':form,'scale1':scale1,'scale2':scale2,'orio1':orio1,'orio2':orio2,'timh1':timh1,'timh2':timh2,'timh3':timh3,'pososto':pososto_metapolishs})
		except ValueError:
			return HttpResponseRedirect('water/menu.html')
	elif (check=='cs'):
		try:
			timh1,timh2,timh3,orio1,orio2=fetch_times_paroxhs(theuser)
			scale1=orio1+1
			scale2=orio2+1
			return render(request,'water/superuser/promocodes_cs.html',{'form':form,'scale1':scale1,'scale2':scale2,'orio1':orio1,'orio2':orio2,'timh1':timh1,'timh2':timh2,'timh3':timh3})
		except ValueError:
			return HttpResponseRedirect('water/menu.html')
	elif (check=='s'):
		try:
			pososto_metapolishs=str(fetch_pinaka2_super(theuser)).strip("0.")
			if (len(pososto_metapolishs)==1):
				pososto_metapolishs=pososto_metapolishs+'0'
			return render(request,'water/superuser/promocodes_s.html',{'form':form,'pososto':pososto_metapolishs})
		except ValueError:
			return HttpResponseRedirect('water/menu.html')		
	else:
		return HttpResponseRedirect('/account/login/')


def check_for_template_super(theuser):
	if (theuser.code_metapolishs and not theuser.code_paroxhs):
		return 's'
	elif (not theuser.code_metapolishs and theuser.code_paroxhs):
		return 'cs'
	elif (theuser.code_metapolishs and theuser.code_paroxhs):
		return 'both'
	else:
		return 'error'	

def fetch_pinaka2_super(Query):
	pososto=Query.price_metapolishs
	return pososto
	
##################################################################################
