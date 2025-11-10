from django.db import models


class Schedule(models.Model):
    day = models.DateField()
    title = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    artist = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.day} - {self.title} - {self.time} - {self.artist}"
