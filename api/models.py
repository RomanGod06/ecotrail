from django.db import models

from django.db import models

class HotelRoom(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, db_index=True) 
    # Swapped the boolean for real numbers:
    total_rooms = models.PositiveIntegerField(default=10, help_text="Total capacity of this hotel/camp")
    available_rooms = models.PositiveIntegerField(default=10, help_text="Rooms currently empty")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.location} ({self.available_rooms}/{self.total_rooms} available)"