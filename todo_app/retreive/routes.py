from flask import Blueprint, request, jsonify
from models import db, Task
from schemas import Post_GetSchema
from logger import create_blueprint_logger

retreive_bp = Blueprint('retreive', __name__)

retreive_bp_logger = create_blueprint_logger('retreive_bp')

post_get_schema = Post_GetSchema()
get_all_schema = Post_GetSchema(many=True)

@retreive_bp.route('/todos', methods=['GET'])
def getall():

    query = db.session.query(Task)
    
    if (query.count() == 0):
        
        retreive_bp_logger.info(
            ">>REQ>> A user tried to retrieve all tasks when 0 tasks were added."
        )

        return jsonify(error="no tasks added yet!")


    title_filter = request.args.get('title')
    status_filter = request.args.get('status')
    limit_val = request.args.get('limit', default=None, type=int)
    offset_val = request.args.get('offset', default=None, type=int)

    if title_filter is not None:
        query = query.filter(Task.Title.ilike(f'%{title_filter}%'))

    if status_filter is not None:
        status_filter = status_filter.lower() == 'true'  # Convert to bool
        query = query.filter(Task.Status == status_filter)

    if offset_val is not None:
        query = query.offset(offset_val)

    tasks = query.limit(limit_val).all() if limit_val is not None else query.all()

    serialized_tasks = get_all_schema.dumps(tasks)

    retreive_bp_logger.info(
        ">>REQ>> A user retrieved all added tasks."
    )
    
    return serialized_tasks, 200, {'Content-Type': 'application/json'}

@retreive_bp.route('/todos/<int:id>', methods=['GET'])
def get_by_id(id):
    t = db.session.get(Task, id)

    if t == None:

        retreive_bp_logger.info(
            ">>REQ>> A user tried to GET a task which doesn't exist. | ID: %s .", id
        )
        return jsonify(error="No task exists with this ID"), 404
    else:
        serialized_task = post_get_schema.dumps(t)

        retreive_bp_logger.info(
            ">>REQ>> A user performed GET on a task successfully. | ID: %s .", id
        )
        return serialized_task, 200, {'Content-Type': 'application/json'} 

@retreive_bp.route('/todos/pages/<int:page_num>', methods=['GET'])
def get_pages(page_num):
    pagination_object = Task.query.paginate(per_page = 5, page =page_num, error_out = False)

    tasks = pagination_object.items  # List of tasks on the current page

    serialized_tasks = get_all_schema.dump(tasks)

    response = {
        'tasks': serialized_tasks,  # Customize this as needed
        'pagination': {
            'page': pagination_object.page,
            'per_page': pagination_object.per_page,
            'total_pages': pagination_object.pages,
            'total_items': pagination_object.total,
            'has_prev': pagination_object.has_prev,
            'has_next': pagination_object.has_next,
        }
    }

    retreive_bp_logger.info(
        ">>REQ>> A user retrieved all tasks with pagination."
    )

    return jsonify(response), 200