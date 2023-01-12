from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from .models import Flower
def start():
    scheduler = BackgroundScheduler()
    #scheduler.add_job(schedule_api,'cron',second=10)
    scheduler.add_job(schedule_api,'cron',second=1)#minute
    scheduler.start()



def schedule_api():
    for i in Flower.objects.all():
                i.count=0
                i.save()

            