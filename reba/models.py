from django.db import models
from django.contrib.auth.models import User
	
class Reba(models.Model):
	rebaID = models.IntegerField(primary_key = True)
	userID = models.ForeignKey(User, on_delete=models.CASCADE)

	neckPosition = models.CharField(max_length=30)
	neckAdjust = models.CharField(max_length=30)
	neckScore = models.IntegerField()

	trunkPosition = models.CharField(max_length=30)
	trunkAdjust = models.CharField(max_length=30)
	trunkScore = models.IntegerField()

	legPosition = models.CharField(max_length=30)
	legAdjust = models.CharField(max_length=30)
	legScore = models.IntegerField(default=0)

	postureScoreA = models.IntegerField()
	flScore = models.IntegerField()
	scoreA = models.IntegerField()

	upperArmPosition = models.CharField(max_length=30)
	upperArmAdjust = models.CharField(max_length=30)
	upperArmScore = models.IntegerField()

	lowerArmPosition = models.CharField(max_length=30)
	lowerArmScore = models.IntegerField()

	wristPosition = models.CharField(max_length=30)
	wristAdjust = models.CharField(max_length=30)
	wristScore = models.IntegerField()

	postureScoreB = models.IntegerField()
	
	couplingScore = models.IntegerField()

	scoreB = models.IntegerField()

	tableScoreC = models.IntegerField()

	activityScore = models.IntegerField()

	finalRebaScore = models.IntegerField()

	def __str__(self):
		return str(self.rebaID)