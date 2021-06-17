from django.shortcuts import render, get_object_or_404
from django.views import View
from products.models import *
# Create your views here.


class Home(View):
    def get(self, request):
        category = Category.objects.all()
        products = Products.objects.all()
        # filter category
        if request.GET.get("category"):
            products = products.filter(category__slug_category=request.GET.get("category"))
        # advance filter
        property = {
            "orderBy": request.GET.get("order-by"),
            "promotion": request.GET.get("promotion"),
            "available": request.GET.get("available"),
        }
        if property["orderBy"]:
            if property["orderBy"] == "price-up":
                products = products.order_by("price")
            if property["orderBy"] == "price-down":
                products = products.order_by("-price")
        if property["available"]:
            if property["available"] == "yes":
                products = products.filter(num_available__gt=0)
            if property["available"] == "no":
                products = products.filter(num_available=0)
        if property["promotion"]:
            if property["promotion"] == "yes":
                products = products.filter(discount__gt=0)
            if property["promotion"] == "no":
                products = products.filter(discount=0)
        context = {
            "category": category,
            "products": products,
            "filter": property,
        }
        return render(request, "home.html", context)


class Search(View):
    def get(self, request):
        category = Category.objects.all()
        products = Products.objects.all()
        products = products.filter(name_product__icontains=request.GET.get("q", ""))
        # advance filter
        property = {
            "orderBy": request.GET.get("order-by"),
            "promotion": request.GET.get("promotion"),
            "available": request.GET.get("available"),
        }
        if property["orderBy"]:
            if property["orderBy"] == "price-up":
                products = products.order_by("price")
            if property["orderBy"] == "price-down":
                products = products.order_by("-price")
        if property["available"]:
            if property["available"] == "yes":
                products = products.filter(num_available__gt=0)
            if property["available"] == "no":
                products = products.filter(num_available=0)
        if property["promotion"]:
            if property["promotion"] == "yes":
                products = products.filter(discount__gt=0)
            if property["promotion"] == "no":
                products = products.filter(discount=0)
        context = {
            "category": category,
            "products": products,
            "filter": property,
        }
        return render(request, "home.html", context)


class DetailProduct(View):
    def get(self, request, slug):
        product = get_object_or_404(Products, slug_product=slug)
        context = {
            "product": product,
        }
        return render(request, "products/detail-product.html", context)


