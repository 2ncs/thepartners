from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

STATUS=(
	('p','Pending'),
	('c','Complete'),
	)



class Number_of_travelers(models.Model):
	maximum_travelers_prwths_kathgorias=models.IntegerField(blank=True,null=True)
	Cost_per_traveler_prwths_kathgorias=models.FloatField(blank=True,null=True)
	maximum_travelers_deuterhs_kathgorias=models.IntegerField(blank=True,null=True)
	Cost_per_traveler_deuterhs_kathgorias=models.FloatField(blank=True,null=True)
	Cost_per_traveler_triths_kathgorias=models.FloatField(blank=True,null=True)
	class Meta:
		verbose_name = 'Pinakas Timwn Paroxhs'
	

class MyAppUser( models.Model ):
    def __unicode__( self ) :
       return self.user.username

    user    = models.ForeignKey( User,related_name='profile' )
    status    = models.TextField( blank = True,verbose_name="Status",default='Not Used',editable='True' ) 
    code_metapolishs = models.CharField( max_length = 135, blank =True)
    price_metapolishs=models.FloatField(blank=True,null=True)
    code_paroxhs = models.CharField( max_length = 135, blank = True)
    price_per_traveler=models.ForeignKey(Number_of_travelers,blank=True,null=True,verbose_name="Pinakas")
    class Meta:
		verbose_name = 'Partners'


    
    
  
	
	
	

class Clients(models.Model):
	Arrival_Date=models.CharField(max_length=50,blank=False,verbose_name="Arrival Date")
	Service_Days=models.CharField(max_length=50,blank=False,verbose_name="Service Days")
	Order_Code=models.CharField(max_length=135,blank=False,verbose_name="Order Code")
	Contact_App=models.CharField(max_length=135,blank=False,verbose_name="Application")
	First_Name=models.CharField(max_length=135,blank=False,verbose_name="First Name")
	Surname=models.CharField(max_length=135,blank=False,verbose_name="Surname")
	Email=models.CharField(max_length=135,blank=False,verbose_name="E-Mail")
	Payment_Status=models.CharField(max_length=135,blank=False,verbose_name="Payment Status")
	Order_Date=models.DateField(auto_now=False,auto_now_add=False,blank=False,verbose_name="Order Date")
	Social_Profile=models.CharField(max_length=135,blank=False,verbose_name="Social Profile")
	Social_Profile_Name=models.CharField(max_length=135,blank=False,verbose_name="Social Profile Name/Number")
	Promo_Code=models.CharField(max_length=135,blank=True,verbose_name="Promo Code")
	Net_Price=models.CharField(max_length=135,blank=False,verbose_name="Net Price")
	Discount=models.CharField(max_length=135,blank=False,verbose_name="Discount")
	Payment_Fee=models.CharField(max_length=135,blank=False,verbose_name="Payment Fee")
	Total=models.CharField(max_length=135,blank=False,verbose_name="Total")
	connection_came_from=models.ForeignKey(MyAppUser,blank=True,null=True)
	promo_kind_code=models.CharField(max_length=135,blank=True)
	class Meta:
		verbose_name = 'Clients'
	def __unicode__( self ):
		return self.Order_Code



class sales(models.Model):
	user=models.ForeignKey(MyAppUser,blank=False,null=False)
	fordate=models.DateField(auto_now=False,auto_now_add=False,blank=False,null=True)
	no_of_sales=models.IntegerField(blank=False,null=False,default=1)
	commission=models.FloatField(blank=False,null=False,default=0)
	settled=models.CharField(blank=False,choices=STATUS,default='p',max_length=1)
	def __unicode__(self):
		objmonth=str(self.fordate.month)
		objyear=str(self.fordate.year)
		
		return str(self.user.user.username)	 +" "+objmonth+"/"+objyear
	class Meta:
		verbose_name = 'Sales per month for partners'



class post_stats(models.Model):
	user=models.ForeignKey(MyAppUser,blank=False,null=False)
	month=models.CharField(blank=False,max_length=50)
	no_of_sales=models.IntegerField(blank=False,null=False,default=1)
	commission=models.FloatField(blank=False,null=False,default=0)
	settled=models.CharField(blank=False,choices=STATUS,default='p',max_length=1)


class post_stats_sales(models.Model):
	user=models.ForeignKey(MyAppUser,blank=False,null=False)
	month=models.CharField(blank=False,max_length=50)
	no_of_sales=models.IntegerField(blank=False,null=False,default=1)
	commission=models.FloatField(blank=False,null=False,default=0)
	settled=models.CharField(blank=False,choices=STATUS,default='p',max_length=1)


class post_stats_customers_served(models.Model):
	user=models.ForeignKey(MyAppUser,blank=False,null=False)
	month=models.CharField(blank=False,max_length=50)
	no_of_guests_served=models.IntegerField(blank=False,null=False,default=1)
	total_cost=models.FloatField(blank=False,null=False,default=0)
	settled=models.CharField(blank=False,choices=STATUS,default='p',max_length=1)
	

class customers_served(models.Model):
	user=models.ForeignKey(MyAppUser,blank=False,null=False)
	fordate=models.DateField(auto_now=False,auto_now_add=False,blank=False,null=True)
	no_of_sales=models.IntegerField(blank=False,null=False,default=1)
	total_cost=models.FloatField(blank=False,null=False,default=0)
	settled=models.CharField(blank=False,choices=STATUS,default='p',max_length=1)
	def __unicode__(self):
		objmonth=str(self.fordate.month)
		objyear=str(self.fordate.year)
		
		return str(self.user.user.username)	 +" "+objmonth+"/"+objyear		
	class Meta:
		verbose_name = 'Customers Served per month for partners'

