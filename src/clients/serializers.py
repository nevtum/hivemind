from clients.models import Contact, RecommendationSubscription
from rest_framework import serializers

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id',
        'employed_by',
        'role',
        'title',
        'first_name',
        'last_name',
        'email')

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendationSubscription
        fields = ('user_id', 'jurisdiction')
