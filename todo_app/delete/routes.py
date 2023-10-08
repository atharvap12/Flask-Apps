
from flask import Blueprint, request, jsonify
from models import db, Task
from logger import create_blueprint_logger

delete_bp = Blueprint('delete', __name__)
delete_bp_logger = create_blueprint_logger('delete_bp')

@delete_bp.route('/todos/<int:id>', methods=['DELETE'])
def del_task(id):
    t = db.session.get(Task, id)

    if t == None:
        delete_bp_logger.info(
            ">>REQ>> A user tried to DELETE a task which doesn't exist. | ID: %s ", id
        )

        return jsonify(error="No task exists with this ID"), 404
    
    else:
        db.session.delete(t)
        db.session.commit()
        delete_bp_logger.info(
            ">>REQ>> A user performed DELETE on a task successfully. | ID: %s .", id
        )

        return jsonify({
            "success" : "The task has been deleted the data dictionary successfully. Verify using GET localhost:5000/todos"
        }), 200