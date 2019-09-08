from django.db import models
from django.contrib.auth.models import User

class Event (models.Model) :
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	name_of_event = models.CharField(max_length=150)
	date = models.DateField()
	Time = models.TimeField()
	num_of_tickets = models.IntegerField()
	description = models.TextField()
	location = models.CharField(max_length=150)
	# check for image field arguments
	image = models.ImageField(null=True, blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=3)
