from flask import Flask, request
from logging.config import dictConfig
from flask_sqlalchemy.record_queries import get_recorded_queries

from config import Config

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(levelname)s | %(module)s] %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "todo.log",
                "formatter": "default",
            },
        },
        "root": {"level": "DEBUG", "handlers": ["file"]},
    }
)

myapp = Flask(__name__)
myapp.config.from_object(Config)

from models import db
from schemas import ma

db.init_app(myapp)
ma.init_app(myapp)

from create.routes import create_bp
from retreive.routes import retreive_bp
from update.routes import update_bp
from delete.routes import delete_bp

myapp.register_blueprint(create_bp)
myapp.register_blueprint(retreive_bp)
myapp.register_blueprint(update_bp)
myapp.register_blueprint(delete_bp)


@myapp.route('/')
def hellofunc():

    myapp.logger.info(">>REQ>> A user visited the home page.")
    return "Hello there!"


@myapp.after_request
def logAfterRequest(response):

    queries = list(get_recorded_queries())
    query_str = ''
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration
        stmt = str(q.statement % q.parameters).replace('\n', '\n       ')
        query_str += 'Query: {0}\nDuration: {1}ms\n\n'.format(stmt, round(q.duration * 1000, 2))

    myapp.logger.info('=' * 80)
    myapp.logger.info(' SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2))) 
    myapp.logger.info('=' * 80) 
    myapp.logger.info(query_str.rstrip('\n')) 
    myapp.logger.info('=' * 80)

    myapp.logger.info(
        ">>RESP>> path: %s | method: %s | status: %s | size: %s",
        request.path,
        request.method,
        response.status,
        response.content_length,
    )

    return response

if __name__ == "__main__":
    #with myapp.app_context():
        #db.create_all()
    
    myapp.run(debug=True)