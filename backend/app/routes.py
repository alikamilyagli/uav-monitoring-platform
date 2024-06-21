from flask import Blueprint, request, current_app
from flask_httpauth import HTTPBasicAuth
from .services import DroneService, TaskService
from .responses import HTTPResponse

auth = HTTPBasicAuth()

api_bp = Blueprint('api', __name__, url_prefix='/api')

@auth.verify_password
def verify_password(username, password):
    expected_username = current_app.config.get('ADMIN_USERNAME', 'admin')
    expected_password = current_app.config.get('ADMIN_PASSWORD', 'admin')
    if username == expected_username and password == expected_password:
        return username

@api_bp.route('/drones', methods=['GET'])
@auth.login_required
def get_drones():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        drones = DroneService.get_all_drones(page, per_page)
        if drones is None:
            return HTTPResponse.error("Failed to fetch drones", 500)
        drone_data = [{'id': drone.id, 'name': drone.name} for drone in drones.items]
        pagination = {
            'page': drones.page,
            'per_page': drones.per_page,
            'total': drones.total,
            'pages': drones.pages
        }
        return HTTPResponse.success(drone_data, "Drones fetched successfully", 200, pagination)
    except Exception as e:
        current_app.logger.error(f"Error in get_drones: {str(e)}")
        return HTTPResponse.error("An unexpected error occurred", 500)

@api_bp.route('/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        tasks = TaskService.get_all_tasks(page, per_page)
        if tasks is None:
            return HTTPResponse.error("Failed to fetch tasks", 500)
        task_data = [{'id': task.id, 'name': task.name, 'description': task.description, 'drone_ids': [drone.id for drone in task.drones]} for task in tasks.items]
        pagination = {
            'page': tasks.page,
            'per_page': tasks.per_page,
            'total': tasks.total,
            'pages': tasks.pages
        }
        return HTTPResponse.success(task_data, "Tasks fetched successfully", 200, pagination)
    except Exception as e:
        current_app.logger.error(f"Error in get_tasks: {str(e)}")
        return HTTPResponse.error("An unexpected error occurred", 500)

@api_bp.route('/tasks', methods=['POST'])
@auth.login_required
def create_task():
    try:
        data = request.json
        task = TaskService.create_task(data)
        if task is None:
            return HTTPResponse.error("Failed to create task", 500)
        return HTTPResponse.success({'id': task.id}, "Task created successfully", 201)
    except Exception as e:
        current_app.logger.error(f"Error in create_task: {str(e)}")
        return HTTPResponse.error("An unexpected error occurred", 500)

@api_bp.route('/tasks/<int:id>', methods=['GET'])
@auth.login_required
def get_task(id):
    try:
        task = TaskService.get_task(id)
        if task is None:
            return HTTPResponse.error("Task not found", 404)
        task_data = {
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'drones': [{'id': drone.id, 'name': drone.name} for drone in task.drones]
        }
        return HTTPResponse.success(task_data, "Task fetched successfully")
    except Exception as e:
        current_app.logger.error(f"Error in get_task: {str(e)}")
        return HTTPResponse.error("An unexpected error occurred", 500)

@api_bp.route('/tasks/<int:id>', methods=['POST'])
@auth.login_required
def update_task(id):
    try:
        data = request.get_json()
        task = TaskService.update_task(id, data)
        if task is None:
            return HTTPResponse.error("Task not found or could not be updated", 404)

        task_data = {
            'id': task.id,
            'name': task.name,
            'description': task.description,
            'drones': [{'id': drone.id, 'name': drone.name} for drone in task.drones]
        }
        return HTTPResponse.success(task_data, "Task updated successfully")
    except Exception as e:
        current_app.logger.error(f"Error in update_task: {str(e)}")
        return HTTPResponse.error("An unexpected error occurred", 500)

@api_bp.route('/tasks/<int:id>/execute', methods=['POST'])
@auth.login_required
def execute_task(id):
    try:
        task = TaskService.execute_task(id)
        if task is None:
            return HTTPResponse.error("Failed to execute task", 500)
        return HTTPResponse.success({'id': task.id}, "Task executed successfully")
    except Exception as e:
        current_app.logger.error(f"Error in execute_task: {str(e)}")
        return HTTPResponse.error("An unexpected error occurred", 500)

@api_bp.route('/tasks/<int:id>/images', methods=['GET'])
@auth.login_required
def get_task_images(id):
    try:
        image_urls = TaskService.get_task_images(id)
        if image_urls is None:
            return HTTPResponse.error("Failed to fetch images", 500)
        return HTTPResponse.success(image_urls, "Images fetched successfully")
    except Exception as e:
        current_app.logger.error(f"Error in get_task_images: {str(e)}")
        return HTTPResponse.error("An unexpected error occurred", 500)
