from django.shortcuts import render
from . serializers import UserSerializer, UrlSerializer, ClickSerializer
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
import json
import random
import string
from . models import Url, Click
import validators
from django.views.decorators.csrf import csrf_exempt
import requests




class UserCreationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


def generate_keyword(length=6):
    # Define the characters to choose from (upper and lower case letters)
    characters = string.ascii_letters
    # Generate a random string by choosing characters randomly
    random_string = ''.join(random.choice(characters) for _ in range(length))
    if Url.objects.filter(keyword=random_string).first():
        return generate_keyword()
    return random_string



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def shorten_url(request):
    if request.method == "POST":
        data = json.loads(request.body)
        url = data["url"]
        keyword = data["keyword"]
        user = request.user

        if not validators.url(url):
            return Response({"error": "Invalid URL"}, status=status.HTTP_400_BAD_REQUEST)

        if Url.objects.filter(keyword=keyword).first():
            return Response({"error": "Keyword already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        

        if keyword == "":
            keyword = generate_keyword()
            print(keyword)
        else:
            if len(keyword) < 6:
                return Response({"error": "Keyword must be at least 6 characters long"}, status=status.HTTP_400_BAD_REQUEST)
        
        url = Url(url=url, keyword=keyword, user=user)
        url.save()

        serializer = UrlSerializer

        return Response({"success": "Link Shortened Successfully"}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_urls(request):
    if request.method == "GET":
        user = request.user
        urls = Url.objects.filter(user=user)
        serializer = UrlSerializer(urls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

def get_location(ip_address):
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "city": response.get("city"),
        "country": response.get("country_name")
    }
    return f"{location_data['city']}, {location_data['country']}"

@api_view(["GET"])
@permission_classes([AllowAny])
def get_url(request, pk):

    ip = get_ip()
    location = get_location(ip)

    print(location)

    url = Url.objects.filter(keyword=pk).first()
    if url:
        click = Click.objects.create(
            url = url,
            ip_address = ip,
            location = location,
        )
        
        click.save()
        url.clicks = Click.objects.filter(url=url).count()
        url.save()

        return Response({"url": url.url}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid Keyword"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_stats(request, pk):
    url = Url.objects.get(id=pk)
    clicks = Click.objects.filter(url=url)

    click_serializer = ClickSerializer(clicks, many=True) 

    url_serializer = UrlSerializer(url, many=False)

    data = {
        "click" : click_serializer.data,
        "url" : url_serializer.data
    }
    return Response(data, status=status.HTTP_200_OK)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_stats_url(request, pk):
    url = Url.objects.get(id=pk)

    serializer = UrlSerializer(url, many=False) 
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_url(request, pk):
    url = Url.objects.get(id=pk)
    url.delete()
    return Response({"message": "deleted"}, status=status.HTTP_200_OK)
