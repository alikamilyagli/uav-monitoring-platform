from flask import jsonify

class HTTPResponse:
    @staticmethod
    def success(data=None, message="Success", status_code=200, pagination=None):
        response = {
            "status": "success",
            "message": message,
            "data": data if data is not None else {}
        }
        if pagination:
            response['pagination'] = pagination
        return jsonify(response), status_code

    @staticmethod
    def error(message="An error occurred", status_code=400, details=None):
        response = {
            "status": "error",
            "message": message
        }
        if details:
            response['details'] = details
        return jsonify(response), status_code
