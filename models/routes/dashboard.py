from flask_apispec import MethodResource
from flask import render_template, make_response, request, redirect, url_for

from sqlalchemy import func

from models.database.databasemodel import Logs, db

class Dashboard(MethodResource):
    def load_get_method(self):
        latest_log = db.session.query(
            Logs.computer,
            func.max(Logs.date).label('latest_date')
        ).group_by(Logs.computer).subquery()

        last_logs = db.session.query(Logs).join(
            latest_log,
            (Logs.computer == latest_log.c.computer) & (Logs.date == latest_log.c.latest_date)
        ).all()

        # all_logs = Logs.query.all()
        #
        # last_login_log = {}
        # for log in all_logs:
        #     computer = log.computer
        #     if computer in last_login_log:
        #         if last_login_log[computer]["date"] > log.date:
        #             break
        #     last_login_log[computer] = {"date": log.date, "user": log.user}

        template = render_template('dashboard.html', all_logs=last_logs)
        response = make_response(template)
        response.headers['Content-Type'] = 'text/html'
        return response


    def get(self):
        return self.load_get_method()