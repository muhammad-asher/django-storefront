from time import sleep
from celery import shared_task
@shared_task
def notify_customer(message):
    print('Sending 10K Emails...')
    print(message)
    sleep(10)
    print('Emails were successfully sent!')

