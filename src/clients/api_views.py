from clients.models import Contact, RecommendationSubscription
from rest_framework import viewsets, generics
from clients import serializers

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = serializers.ContactSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = RecommendationSubscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer
