from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q, F
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Collection, Order, OrderItem
from tags.models import TagItem
from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from templated_mail.mail import BaseEmailMessage
from .tasks import notify_customer
import requests
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import logging


# Create your views here.

# Caching views
@cache_page(5 * 60)
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
    # Slice the Object
    # query_set = Product.objects.order_by('title')[:5]
    # Select related
    # query_set = Product.objects.select_related('collection').all()

    # Quering Generic Relationship
    content_type = ContentType.objects.get_for_model(Product)
    query_set = TagItem.objects.select_related('tag').filter(
        content_type=content_type,
        object_id=1
    )

    # Creating Objects and then save it in the Database
    #     collection = Collection()
    #     collection.title='Videos Games'
    #     collection.featured_product = Product(pk=11)
    #     collection.save()

    # Updating Objects and then save it in the Database
    #     collection = Collection(pk=11)
    #     collection.title = 'Games'
    #     collection.featured_product = None
    #     collection.save()

    # Deleting Objects from Database
    # collection = Collection(pk=11)
    # collection.delete()
    # Transaction means Set of atomic db queries ; either all the changes will be applied, or none
    # with transaction.Atomic:
    #     order = Order()
    #     order.customer_id = 1
    #     order.save()
    #
    #     item = OrderItem()
    #     item.order = order
    #     item.product_id = 1
    #     item.quantity = 1
    #     item.unit_price = 10
    #     item.save()

    # BaseEmailMessage
    # message = BaseEmailMessage(
    #     template_name='emails/hello.html',
    #     context={'name': 'Asher'}
    # )
    # message.send(['everyone@gmail.com'])

    # EmailMessage
    # message = EmailMessage('subject', 'message', 'everyone@gmail.com', ['anyone@phpstudios.com'])
    # message.attach_file('playground/static/images/title.png')
    # message.send()

    # mail_admins
    # mail_admins('subject', 'message', html_message='Training Message')

    # send_mail
    # send_mail('subject', 'message', 'anyone@phpstudios.com', ['everyone@gmail.com'])

    # Celery
    # notify_customer.delay('hello')

    # Simulating a Slow API
    # requests.get('https://httpbin.org/delay/2')

    # Using the Low Level Cache API
    logger = logging.getLogger(__name__)
    try:
        logger.info('Calling httpbin')
        response = requests.get('https://httpbin.org/delay/2')
        logger.info('Revieved the response')
        data = response.json()
    except requests.ConnectionError:
        logger.critical('Httpbin is offline')
    return render(request, 'hello.html', {'name': data, 'products': list(query_set)})
