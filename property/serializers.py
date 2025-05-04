# importing models, functions and classes
from django.contrib.auth import get_user_model
from rest_framework import serializers
from decimal import Decimal
from .models import Amenities, Property, PropertyImage, Review

User = get_user_model()

# Amenities Serializer
class AmenitiesSerializer(serializers.Serializer):
    class Meta:
        model = Amenities
        fields = ['id', 'name', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'created_at']

# PropertyImage Serializer
class PropertyImageSerializer(serializers.Serializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image']

# Property Serializer
class PropertySerializer(serializers.Serializer):
    """ 
    this is creating a many-to-many relationship to the product in order to 
    handle image conversion and send multiple images
    """
    images = PropertyImageSerializer(many=True, read_only=True)

    # this is receiving multiple images
    uploaded_images = serializers.ListField(child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False), write_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=Decimal('0.00'), max_value=Decimal('100000.00'))

    class Meta:
        model = Property
        fields = ['id', 'name', 'location', 'num_of_guest', 'num_of_bedroom', 'description', 'amenities', 'price', 'created_at', 'hosted_by', 'images', 'uploaded_images']
        read_only_fields = ['created_at', 'hosted_by', 'images']

        # Name validation: Handles validation for name field to prevent empty field or whitespace

        def validate_name(self, value):
            if not value.strip():
                raise serializers.ValidationError(
                    'Product name cannnot be empty or whitespace')
            return value

        # Price validation: checks price to ensure it's not a zero or negative value
        def validate_price(self, value):
            if value <= 0:
                raise serializers.ValidationError(
                    'Price must be greater than zero')
            return value
        

    # Handles the process of creating a property with multiple images for each at a go

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")
        product = Property.objects.create(**validated_data)
        for image in uploaded_images:
            PropertyImage.objects.create(property=property, image=image)
        return property

    # Handles Property Update
    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop("uploaded_images")

        for attr, value in validated_data.items():
            # Update the property fields
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
                instance.save()

            # Handle the images
            self._handle_images(instance, uploaded_images)

            return instance

    def _handle_images(self, property, uploaded_images):
        # If there are new images, delete the old ones
        if uploaded_images:
            property.images.all().delete()

        # Create new image instances
        for image in uploaded_images:
            PropertyImage.objects.create(property=property, image=image)


# Serializer for the Review Model
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'description']

    # creating review on property by the user
    def create(self, validated_data):
        property_id = self.context['property_id']
        user_id = self.context['user_id']
        property = Property.objects.get(id=property_id)
        user = User.objects.get(id=user_id)
        review = Review.objects.create(
            property=property, user=user, **validated_data)
        return review
    



