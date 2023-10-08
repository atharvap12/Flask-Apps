from flask import Blueprint, request, jsonify
from models import db, Task
from schemas import Post_GetSchema
from marshmallow import ValidationError
from logger import create_blueprint_logger

create_bp = Blueprint('create', __name__)
create_bp_logger = create_blueprint_logger('create_bp')

post_get_schema = Post_GetSchema()


@create_bp.route('/todos', methods=['POST'])
def post_task():
    #body_dict = request.get_json()
    json_data = request.data.decode('utf-8')
    try:
        post_obj = post_get_schema.loads(json_data)
    
    except ValidationError as err:
        #d = { "error" : "the body must be of the format - {ID : Int val, Title : String val, Status: Boolean val}" }
        create_bp_logger.info(
            ">>REQ>> A user performed a POST operation with bad request body. | ValidationError: %s ", err.messages
        )
        return jsonify(err.messages), 400

    else:
        #s = post_obj.ID
        is_there = db.session.get(Task, 9)
        if is_there != None:
            create_bp_logger.info(
                ">>REQ>> A user tried to POST a tasks whose ID already exits."
            )

            return jsonify(error="Task with this ID is already present.")
        
        db.session.add(post_obj)
        db.session.commit()
        create_bp_logger.info(
            ">>REQ>> A user performed a POST operation succesfully."
        )
        return jsonify({
            "success" : f"The task has been added to the data dictionary successfully. Verify using GET localhost:5000/todos. s = {s}"
        }), 200