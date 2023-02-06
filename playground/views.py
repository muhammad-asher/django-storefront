from django.http import HttpResponse
from django.shortcuts import render
from django.db.models import Q,F
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product


# Create your views here.


def say_hello(request):
    # query_set = Product.objects.all()

    # try:
    #     query_set = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     pass
    # query_set= Product.objects.filter(title__icontains='Coffee')

# Using Q objects
#     query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))

# Using F objects
#     query_set = Product.objects.filter(inventory=F('unit_price'))
#Slice the Object
    # query_set = Product.objects.order_by('title')[:5]
    query_set = Product.objects.select_related('collection').all()

    return render(request, 'hello.html', {'name': 'Asher Khan', 'products': list(query_set)})
