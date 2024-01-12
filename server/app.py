#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# Flask-RESTful's Api class is the constructor for your RESTful API as a whole
api = Api(app)

'''
the Resource class, which includes conditions for throwing exceptions and base methods for each HTTP method that explicitly disallow them.

if you add any non-RESTful views to your app, you still need app.route()!

instead of each HTTP verb getting a code block inside of a view function, they each get an instance method inside of a Resource class.

'''


class Home(Resource):
    def get(self):
        response_body = {
            "success": True,
            "message": "Welcome to the NewsLetter RESTful API"
        }

        response = make_response(jsonify(response_body), 200)

        response.headers["Content-Type"] = "application/json"

        return response


api.add_resource(Home, "/")


class NewsLetters(Resource):
    def get(self):
        newsletters_lc = [newsletter.to_dict()
                          for newsletter in Newsletter.query.all()]

        response = make_response(jsonify(newsletters_lc), 200)

        response.headers["Content-Type"] = "application/json"

        return response

    def post(self):
        data = request.get_json()

        new_newsletter = Newsletter(
            title=data["title"],
            body=data["body"]

        )
        db.session.add(new_newsletter)
        db.session.commit()

        new_newsletter_dict = new_newsletter.to_dict()

        response = make_response(jsonify(new_newsletter_dict), 201)

        response.headers["Content-Type"] = "application/json"

        return response


api.add_resource(NewsLetters, "/newsletters")


class NewsLetter(Resource):
    def get(self, newsletter_id):
        newsletter = Newsletter.query.filter_by(id=newsletter_id).first()

        newsletter_dict = newsletter.to_dict()

        response = make_response(jsonify(newsletter_dict), 200)

        response.headers["Content-Type"] = "application/json"

        return response


api.add_resource(NewsLetter, "/newsletters/<int:newsletter_id>")
if __name__ == '__main__':
    app.run(port=5555, debug=True)
