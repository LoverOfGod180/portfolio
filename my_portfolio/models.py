from django.db import models

class Projects(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    link = models.URLField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically sets the field to the current time when a project is created

    def __str__(self):
        return self.name
