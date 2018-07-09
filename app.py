from flask import Flask, jsonify, make_response
from flask_restful import Api
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from config import load_env_variables, DevelopmentConfig, ProdConfig
load_env_variables() #loading enviornment variables

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)#loading config data into flask app from config object.

api = Api(app)

db = SQLAlchemy(app)

error={"status":404,"error":"Not Found"}

#TODO: Check why reflect takes so much time (1-2 min) to setup. low-priority
db.Model.metadata.reflect(db.engine)#This takes upto a min to reflect the database. Not a big problem now but might want to take a look later.

#loading resources
from resources.faqs import Faqs_RUD
from resources.faqs import Faqs_CR

@api.representation('application/json')
def ret_json(data, code, headers=None):
    resp = make_response(jsonify(data), code)
    resp.headers.extend(headers)
    return resp

task_queue=Celery("SpartaHack_API_2019",broker=app.config["CELERY_BROKER_URL"])

api.add_resource(Faqs_RUD,"/faqs/<int:faq_id>")
api.add_resource(Faqs_CR,"/faqs/")

@app.route("/")#for flask app test and general info about the product
def helloworld():
    return jsonify({"Organisation":"SpartaHack",
                    "Backend Developers":"Yash, Jarek",
                    "Frontend Developers":"Harrison, Jessica, Jarek",
                    "Contact":"hello@spartahack.com",
                    "Version":"0.1.0"})

if __name__ == '__main__': #running on local server. This needs to change for prod
    app.run(debug=True)