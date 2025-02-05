from django.shortcuts import render
from ninja import NinjaAPI

api = NinjaAPI()


@api.get("/hello")
def hellp(request):
    return {"greeting": "hello"}
