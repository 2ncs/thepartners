from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q

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

import django_tables2 as tables
# Create your views here.


class user_sales_table(tables.Table):
	Promo_Code=tables.Column(orderable=False)
	First_Name=tables.Column(orderable=False)
	Surname=tables.Column(orderable=False)
	Order_Date=tables.Column(orderable=False)
	class Meta:
		attrs={'class':'table table-hover table-striped'}


class update_table(tables.Table):
	Promo_Code=tables.Column(orderable=False)
	First_Name=tables.Column(orderable=False)
	Surname=tables.Column(orderable=False)
	Order_Date=tables.Column(orderable=False)
	Net_Price=tables.Column(orderable=False)
	Discount=tables.Column(orderable=False)
	Total=tables.Column(orderable=False)
	class Meta:
		attrs={'class':'table table-hover table-striped'}

		
		
class user_statistics_sales(tables.Table):
	month=tables.Column(orderable=False)
	no_of_sales=tables.Column(orderable=False)
	commission=tables.Column(orderable=False)
	settled=tables.Column(orderable=False)
	class Meta:
		attrs={'class':'table table-hover table-striped'}


class user_statistics_customers_served(tables.Table):
	month=tables.Column(orderable=False)
	no_of_guests_served=tables.Column(orderable=False)
	total_cost=tables.Column(orderable=False)
	settled=tables.Column(orderable=False)
	class Meta:
		attrs={'class':'table table-hover table-striped'}

		
		
class user_clients_fnames(tables.Table):
	First_Name=tables.Column(attrs={'th':{'align':'center'}})
	class Meta:
		attrs={'width':'100%','margin-left':'auto','margin-right':'auto'}


class user_clients_snames(tables.Table):
	Surname=tables.Column(attrs={'th':{'align':'center'}})
	class Meta:
		attrs={'width':'100%','margin-left':'auto','margin-right':'auto'}

class user_table(tables.Table):
	Promo_Code = tables.Column(attrs={'th':{'width':'25%','align':'center'}})
	First_Name = tables.Column(attrs={'th':{'width':'25%','align':'center'}})
	Surname= tables.Column(attrs={'th':{'width':'25%','align':'center'}})
	Order_Date= tables.Column(attrs={'th':{'width':'25%','align':'center'}})
	class Meta:
		attrs={'background-color':'#00FF00','width':'100%','margin-left':'auto','margin-right':'auto'}

class super_table(tables.Table):
	Arrival_Date=tables.Column(attrs={'th':{'align':'center'},'td':{'align':'left'}})
	Service_Days=tables.Column(attrs={'th':{'align':'center'},'td':{'align':'left'}})
	Social_Profile=tables.Column(attrs={'th':{'align':'center'},'td':{'align':'left'}})
	First_Name=tables.Column(attrs={'th':{'align':'center'},'td':{'align':'left'}})
	Surname=tables.Column(attrs={'th':{'align':'center'},'td':{'align':'left'}})
	Order_Date=tables.Column(attrs={'th':{'align':'center'},'td':{'align':'left'}})
	Social_Profile_Name=tables.Column(attrs={'th':{'align':'center'},'td':{'align':'left'}})
	Promo_Code=tables.Column(attrs={'th':{'align':'center'},'td':{'align':'left'}})

	class Meta:
		attrs={'class':'paleblue','width':'125%','align':'center','table':{'align':'center'}}
		headers_attrs={'th':{'align':'center'}}



def check_for_template(request):
	try:
		theuser=MyAppUser.objects.get(user=request.user)
		if (theuser.code_metapolishs and not theuser.code_paroxhs):
			return 's'
		elif (not theuser.code_metapolishs and theuser.code_paroxhs):
			return 'cs'
		elif (theuser.code_metapolishs and theuser.code_paroxhs):
			return 'both'
		else:
			return 'error'	
	except MyAppUser.DoesNotExist:
		return 'error'

def statistics_sales(request):
	theuser=MyAppUser.objects.get(user=request.user)
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

def statistics_customers_served(request):
	theuser=MyAppUser.objects.get(user=request.user)
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
	


def fetch_paroxhs(request,mon,year):
	board=Clients.objects.filter(Q(connection_came_from__user=request.user) & Q(promo_kind_code='paroxhs') & Q(Order_Date__year=year) & Q(Order_Date__month=mon))
	used=user_sales_table(board)
	message=board.count()
	user=MyAppUser.objects.get(user=request.user)
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
	return used


def fetch_paroxhs_ajax(request,mon,year):
	board=Clients.objects.filter(Q(connection_came_from__user=request.user) & Q(promo_kind_code='paroxhs') & Q(Order_Date__year=year) & Q(Order_Date__month=mon))
	used=user_sales_table(board)
	message=board.count()
	user=MyAppUser.objects.get(user=request.user)
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



def fetch_metapolishs(request,mon,year):
	board=Clients.objects.filter(Q(connection_came_from__user=request.user) & Q(promo_kind_code='metapolisis') & Q(Order_Date__year=year) & Q(Order_Date__month=mon))
	summ=0
	for i in board:
		summ=summ+float(i.Total)
	used=user_sales_table(board)
	message=board.count()
	user=MyAppUser.objects.get(user=request.user)
	#data=summ*user.price_metapolishs
	cost_of_cat=user.price_metapolishs
	return used




def fetch_paroxhs_super(foruser,mon,year):
	seek=MyAppUser.objects.get(user__username=foruser)
	board=Clients.objects.filter(Q(connection_came_from__user=seek.user) & Q(promo_kind_code='paroxhs') & Q(Order_Date__year=year) & Q(Order_Date__month=mon))
	used=user_sales_table(board)
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
	return used


def fetch_metapolishs_test1(request,mon,year):
	board=Clients.objects.filter(Q(Order_Date__year=year) & Q(Order_Date__month=mon))
	data=user_sales_table(board)
	return data
	
def fetch_metapolishs_test2(request,mon,year):
	board=Clients.objects.filter(Q(Order_Date__year=year) & Q(Order_Date__month=mon))
	#data=user_sales_table(board)
	return board
	



def fetch_metapolishs_ajax(request,mon,year):
	board=Clients.objects.filter(Q(connection_came_from__user=request.user) & Q(promo_kind_code='metapolisis') & Q(Order_Date__year=year) & Q(Order_Date__month=mon))
	summ=0
	for i in board:
		summ=summ+float(i.Total)
	used=user_table(board)
	message=board.count()
	user=MyAppUser.objects.get(user=request.user)
	data=summ*user.price_metapolishs
	cost_of_cat=user.price_metapolishs
	return board



def fetch_metapolishs_super(foruser,mon,year):
	seek=MyAppUser.objects.get(user__username=foruser)
	board=Clients.objects.filter(Q(connection_came_from__user=seek.user) & Q(promo_kind_code='metapolisis') & Q(Order_Date__year=year) & Q(Order_Date__month=mon))
	summ=0
	for i in board:
		summ=summ+float(i.Total)
	used=user_sales_table(board)
	message=board.count()
	user=MyAppUser.objects.get(user=seek.user)
	#data=summ*user.price_metapolishs
	cost_of_cat=user.price_metapolishs
	return used
	


def fetch_pinaka(request):
	Query=MyAppUser.objects.get(user=request.user)
	paroxhs_id=Query.price_per_traveler.id
	pinakas_timwn=Number_of_travelers.objects.get(id=paroxhs_id)
	timh1=pinakas_timwn.Cost_per_traveler_prwths_kathgorias
	timh2=pinakas_timwn.Cost_per_traveler_deuterhs_kathgorias
	timh3=pinakas_timwn.Cost_per_traveler_triths_kathgorias
	orio1=pinakas_timwn.maximum_travelers_prwths_kathgorias
	orio2=pinakas_timwn.maximum_travelers_deuterhs_kathgorias
	return timh1,timh2,timh3,orio1,orio2
	
def fetch_times_paroxhs(foruser):
	paroxhs_id=foruser.price_per_traveler.id
	pinakas_timwn=Number_of_travelers.objects.get(id=paroxhs_id)
	timh1=pinakas_timwn.Cost_per_traveler_prwths_kathgorias
	timh2=pinakas_timwn.Cost_per_traveler_deuterhs_kathgorias
	timh3=pinakas_timwn.Cost_per_traveler_triths_kathgorias
	orio1=pinakas_timwn.maximum_travelers_prwths_kathgorias
	orio2=pinakas_timwn.maximum_travelers_deuterhs_kathgorias
	return timh1,timh2,timh3,orio1,orio2	
		
	
	
def fetch_pinaka2(request):
	Query=MyAppUser.objects.get(user=request.user)
	pososto=Query.price_metapolishs
	return pososto



def sales_calc(foruser,formonth,foryear,cost):
	try:
		exist=sales.objects.get(Q(user=foruser) & Q(fordate__month=formonth) & Q(fordate__year=foryear))
		exist.no_of_sales=exist.no_of_sales+1
		exist.commission=exist.commission + (cost * exist.user.price_metapolishs)
		exist.save()
	except sales.DoesNotExist:
		#getuser=MyAppUser.objects.get(user=foruser)
		date="1"+"/"+str(formonth)+"/"+str(foryear)
		order_date=datetime.datetime.strptime(date, '%d/%m/%Y')
		obj=sales(user=foruser,fordate=order_date,commission=cost*foruser.price_metapolishs,)
		obj.save()
	


def customers_served_calc(foruser,formonth,foryear):
	c1,c2,c3,fmax,smax=fetch_times_paroxhs(foruser)
	try:
		exist=customers_served.objects.get(Q(user=foruser) & Q(fordate__month=formonth) & Q(fordate__year=foryear))
		exist.no_of_sales=exist.no_of_sales+1
		if(exist.no_of_sales <= fmax):
			exist.total_cost=exist.no_of_sales * c1
		elif (exist.no_of_sales>fmax and exist.no_of_sales<=smax):
			exist.total_cost=exist.no_of_sales * c2
		else :
			exist.total_cost=exist.no_of_sales * c3		
		exist.save()
	except customers_served.DoesNotExist:
		#getuser=MyAppUser.objects.get(user=foruser)
		date="1"+"/"+str(formonth)+"/"+str(foryear)
		order_date=datetime.datetime.strptime(date, '%d/%m/%Y')
		obj=customers_served(user=foruser,fordate=order_date,total_cost=c1)
		obj.save()






def month_number(mon):
	if (mon=='January'):
		return 1
	if (mon=='February'):
		return 2
	if (mon=='March'):
		return 3
	if (mon=='April'):
		return 4
	if (mon=='May'):
		return 5
	if (mon=='June'):
		return 6
	if (mon=='July'):
		return 7
	if (mon=='August'):
		return 8
	if (mon=='September'):	
		return 9
	if (mon=='October'):
		return 10
	if (mon=='November'):
		return 11
	if (mon=='December'):
		return 12	


def month_name(mon):
	if (mon==1):
		return 'January'
	if (mon==2):
		return 'February'
	if (mon==3):
		return 'March'
	if (mon==4):
		return 'April'
	if (mon==5):
		return 'May'
	if (mon==6):
		return 'June'
	if (mon==7):
		return 'July'
	if (mon==8):
		return 'August'
	if (mon==9):	
		return 'September'
	if (mon==10):
		return 'October'
	if (mon==11):
		return 'November'
	if (mon==12):
		return 'December'			



class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
    
def fetch_email(mail,id_list,num):

	latest_email_id = id_list[-num] # get the latest

	result, data = mail.fetch(latest_email_id, "(RFC822)") # fetch the email body (RFC822)             for the given ID

	raw_email = data[0][1] # here's the body, which is raw text of the whole email
	return raw_email   
    
def fetch_data_from_email(raw_email):
	number_of_lines=len(raw_email.split('\n'))
	line=raw_email.splitlines()
	i=0
	while(line[i]!='PCFET0NUWVBFIGh0bWw+DQo8aHRtbCB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMTk5'):
		i=i+1
		
	new_list=[]

	for j in range(i-1,number_of_lines-1):
		new_list.append(line[j])
		
	new=''
	new='\n'.join(new_list)
		

	########################

	last_string=new.decode('base64')
	msg=strip_tags(last_string)
	line=msg.splitlines()
	number_of_lines=len(msg.split('\n'))
	i=0
	last_list=[]
	for j in range(i-1,number_of_lines-1):
		if line[j].strip():
			last_list.append(line[j].strip())
	return last_list,len(last_list)

def get_info(last_list,num):
	if (num>36):
		return last_list[3],last_list[5],last_list[7],last_list[11],last_list[14],last_list[15],last_list[18],last_list[19],last_list[22],last_list[23],last_list[26],last_list[27],last_list[30],last_list[32],last_list[34],last_list[36]
	else:
		return last_list[3],last_list[5],last_list[7],last_list[11],last_list[14],last_list[15],last_list[18],last_list[19],last_list[22],last_list[23],last_list[25],last_list[28],last_list[30],last_list[32],last_list[34]


	




