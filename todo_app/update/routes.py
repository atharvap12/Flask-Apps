from flask import Blueprint, request, jsonify
from models import db, Task
from schemas import PatchSchema, PutSchema
from marshmallow import ValidationError
from collections import defaultdict
from logger import create_blueprint_logger

update_bp = Blueprint('update', __name__)

update_bp_logger = create_blueprint_logger('update_bp')

patch_schema = PatchSchema()
put_schema = PutSchema()

@update_bp.route('/todos/<int:id>', methods=['PUT'])
def put_task(id):
    t = db.session.get(Task, id)

    if t == None:
        update_bp_logger.info(
            ">>REQ>> A user tried to perform PUT on a task which doesn't exist. | ID: %s .", id
        )
        return jsonify(error="No task exists with this ID"), 404
    else:
        json_data = request.data.decode('utf-8')
        try:
            put_dict = put_schema.loads(json_data)
    
        except ValidationError as err:
            update_bp_logger.info(
                ">>REQ>> A user performed a PUT operation with bad request body. | ValidationError: %s .", err.messages
            )
            return jsonify(err.messages), 400

        else:
            for field, value in put_dict.items():
                setattr(t, field, value) #setattr(task, field, value) sets the value of the attribute named 'field' on the 'task' object to 
                #the value 'value'.

            db.session.commit()

            update_bp_logger.info(
                ">>REQ>> A user performed PUT operation on a task successfully. | ID: %s .", id
            )
            return jsonify({
                "success" : "The task has been PUT to the data dictionary successfully. Verify using GET localhost:5000/todos"
            }), 200


@update_bp.route('/todos/<int:id>', methods=['PATCH'])
def patch_task(id):
    t = db.session.get(Task, id)

    if t == None:
        update_bp_logger.info(
            ">>REQ>> A user tried to perform PATCH on a task which doesn't exist. | ID: %s .", id
        )
        return jsonify(error="No task exists with this ID"), 404
    else:
        json_data = request.data.decode('utf-8')
        try:
            patch_dict = patch_schema.loads(json_data)
    
        except ValidationError as err:
            update_bp_logger.info(
                ">>REQ>> A user performed a PATCH operation with bad request body. | ValidationError: %s .", err.messages
            )
            return jsonify(err.messages), 400

        else:
            default_dict = defaultdict(int, patch_dict)

            title = default_dict['Title']
            status = default_dict['Status']

            if title != 0:
                t.Title = title

            if status != 0:
                t.Status = status

            db.session.commit()

            update_bp_logger.info(
                ">>REQ>> A user performed PATCH operation on a task successfully. | ID: %s .", id
            )
            return jsonify({
                "success" : "The task has been modified to the data dictionary successfully. Verify using GET localhost:5000/todos"
            }), 200