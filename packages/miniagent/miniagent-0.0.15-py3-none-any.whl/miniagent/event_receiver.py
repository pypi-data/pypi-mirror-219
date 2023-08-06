from flask import jsonify
from flask_api import status
from flask_restful import Resource, reqparse
from .executer import ExecuterCaller

class Command(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('command_code', type=str)
    parser.add_argument('initial_param', type=dict)
    parser.add_argument('executer', type=str)
    #parser.add_argument('items', type=list, location='json')

    def post(self):

        data = Command.parser.parse_args()

        rtn, message = ExecuterCaller.instance().execute_command(data)

        if rtn:
            status_code = status.HTTP_200_OK            
        else:
            status_code = status.HTTP_400_BAD_REQUEST

        return dict(message=message['message']), status_code