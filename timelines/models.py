from django.db import models

class Timelines(models.Model):
   

    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(max_length=255)
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField(max_length=100)
    long_description = models.TextField()
    def __str__(self):
        return f"Reminder on {self.date} for {self.description}"
