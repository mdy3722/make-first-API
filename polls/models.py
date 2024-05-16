from django.db import models

# Create your models here.
class Poll(models.Model):
    # pollID
    title = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    agree = models.IntegerField(default=0)
    disagree = models.IntegerField(default=0)
    agreeRate = models.FloatField(default=0)
    disagreeRate = models.FloatField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    def calculate_rate(self):
        total = self.agree + self.disagree
        if total > 0:
            self.agreeRate = round((self.agree / total), 4)
            self.disagreeRate = round((self.disagree / total), 4)
            
        
        