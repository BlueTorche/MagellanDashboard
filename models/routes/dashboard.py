from flask_apispec import MethodResource
from flask import render_template, make_response, request, redirect, url_for

from models.database.databasemodel import Logs, db

class Dashboard(MethodResource):
    def load_get_method(self):

        all_logs = Logs.query.all()

        print(all_logs)

        template = render_template('dashboard.html', all_logs=all_logs)
        response = make_response(template)
        response.headers['Content-Type'] = 'text/html'
        return response


    def get(self):
        return self.load_get_method()