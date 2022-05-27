from apscheduler.schedulers.background import BackgroundScheduler
from ics import Calendar
import argparse
import requests

parser = argparse.ArgumentParser(
     prog='notification-service.py',
     description='''Schedule notifications from Indico server to Mattermost'''
)
parser.add_argument("-i", "--ics", help="ics url to read", default=None)
parser.add_argument("-o", "--out", help="webhook url", default=None)
args = parser.parse_args()

# notification job
def notify_job(out, event):
    text = "Event " + event.name + " starts now."
    requests.post(out, json={"text": text})

if __name__ == "__main__":

    # load events from category ics
    calendar = Calendar(requests.get(args.ics).text)

    # create scheduler
    scheduler = BackgroundScheduler()

    # add jobs to scheduler
    for event in calendar.timeline:
        if event.begin.datetime < datetime.now(event.begin.datetime.tzinfo):
            scheduler.add_job(notify_job, 'date', run_date=event.begin.datetime, args=[event])

    # print jobs
    schedule.print_jobs()

    # start scheduler
    scheduler.start()
