# from datetime import datetime
# from apscheduler.schedulers.background import BackgroundScheduler
# from .models import Flower

# Ranking Scheduler

# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(schedule_api,'cron',minute=0)
#     scheduler.start()

# def schedule_api():
#     for i in Flower.objects.all():
#         i.count=0
#         i.save()
