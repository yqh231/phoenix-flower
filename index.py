from flask import Flask
from flask import render_template
from crontab import CronTab

from database import ServiceDB


app = Flask(__name__)
db = ServiceDB()

def startCron():
    cron = CronTab('catsky')
    cron.remove_all('/usr/bin/python')
    job1 = cron.new(command='/usr/bin/python ~/Desktop/share/Flask/cron.py >>~/Desktop/mycron.txt')
    job1.every().minute()
    job2 = cron.new(command='/usr/bin/python ~/Desktop/share/Flask/cron.py --hours')
    job2.every().hour()
    cron.write()
    print 'cron job started as the following'
    print cron.render()



@app.route("/cur/<string:freq>")
def hello(freq):
    if freq == None or freq == "minutes":
        cur = db.queryMoneyMinutes(30)
        return render_template('currency_minutes.html', currencies=cur)
    elif freq == "hours":
        cur = db.queryMoneyHours(24)
        return render_template('currency_hours.html', currencies=cur)
    else:
        cur1 = db.queryMoneyMinutes(30)
        cur2 = db.queryMoneyHours(24)
        return render_template('currency_all.html', currencies_min=cur1, currencies_hour=cur2)


if __name__ == "__main__":
    startCron()
    app.run()