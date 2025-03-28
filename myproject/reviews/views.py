from rest_framework import generics
from .models import Review
from .serializers import ReviewSerializer

class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer