from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Amenities Model
class Amenities(models.Model):
    name = models.CharField(max_length=255, null=True, unique=True, blank=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name

# Property Model

class Property(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    location = models.CharField(max_length=255, null=False, blank=False)
    num_of_guest = models.PositiveSmallIntegerField(default=1, max=10)
    num_of_bedroom = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(null=True)
    amenities = models.ForeignKey(Amenities, on_delete=models.CASCADE)
    price = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    hosted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
# Property Image Model
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/', null=True, blank=True, editable=True)


# Review Model
class Review(models.Model):
    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='rating')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='rated')
    rating = models.PositiveIntegerField(choices=(
        (1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')))
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['property', 'user']

    def __str__(self):
        return f"Review: {self.user} gave {self.rating}-star to {self.property}"