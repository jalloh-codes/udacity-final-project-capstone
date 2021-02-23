import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from  models import setup_db,  Leader, Project, Member, Task
from auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/": {"origins": "*"}})


    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',  'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response


    ## ROUTES
    #--------------------GET METHODS------------------#
    @app.route('/', methods=['GET'])
    def all_leader():
        try:
            leaders = Leader.query.filter(Leader.id == id).all()
            data = [leader.long() for leader in leaders]
            return jsonify({
                'success': True,
                'data': data
            })
        except Exception as e:
            print(e)
            abort(404)


    @app.route('/leader/<int:id>',  methods=['GET'])
    def get_leader(id):
        try:
            req= request.get_json()
            email = req['email']
            data = Leader.query.filter(Leader.id == id).first()
            leader = [data.long()]
            print(req)

            return jsonify({
                'success': True,
                'data': [data.long()]

            }), 200
        except Exception as e:
            print(e)
            abort(404)

    #get project by  a leader id 
    @app.route('/project/<int:id>', methods=['GET'])
    @requires_auth('get:project')
    def get_project(payload, id):
        try:
            projects = Project.query.filter(Project.leader_id == id).all()
            data = [project.long() for project in projects]

            return jsonify({
                'success': True,
                'data': data
            }), 200
        except Exception as e:
            print(e)
            abort(401)


    #get tasks by a member is
    @app.route('/task/<int:id>', methods=['GET'])
    @requires_auth('get:task')
    def get_task(payload, id):
        try:
            tasks = Task.query.filter(Task.member_id == id).all()
            data =  [task.long() for task in tasks]
            return jsonify({
                'success': True,
                'data': data
            }), 200
        except Exception as e:
            print(e)
            abort(401)


    #---------------POST FUNC---------------------#
    @app.route('/leader', methods=['POST'])
    def new_leader():
        try:
            req = request.get_json()
            email = req['email']
            firstname = req['firstname']
            lastname =  req['lastname']
            exist = Leader.query.filter_by(email=email).first()
            if exist:
                leader = [exist.long()]
                return jsonify({
                    'success': True,
                    'data': leader
                }), 200
            else:
                new_leader = Leader(email= email, firstname=firstname, lastname=lastname)
                new_leader.insert()
                return jsonify({
                    'success': True
                }), 200
        except Exception as e:
            print(e)
            abort(401)
    #create a new project only by a leader


    @app.route('/project', methods=['POST'])
    @requires_auth('post:project')
    def new_project(payload):
        try:
            req = request.get_json()
            name = req['name']
            about = req['about']
            complete =  req['complete']
            leader_id = req['leader_id']

            new_project = Project(name=name, about=about, complete=complete, leader_id=leader_id)
            new_project.insert()
            projects = Project.query.all()
            data = [project.long() for project in projects]

            return jsonify({
                'success': True,
            }), 200
        except Exception as e :
            print(e)
            abort(401)


    @app.route('/member', methods=['POST'])
    @requires_auth('post:member')
    def new_member(payload):
        try:
            req = request.get_json()
            email = req['email']
            firstname = req['firstname']
            lastname =  req['lastname']
            leader_id = req['leader_id']

            new_member = Member(email=email, firstname=firstname, lastname=lastname, leader_id=leader_id)
            new_member.insert()
            members = Member.query.all()
            # data = [member.long() for member in members]

            return jsonify({
                'success': True,
                'msg': firstname + ' have been added'
            }), 200
        except Exception as e :
            print(e)
            abort(401)

    @app.route('/task', methods=['POST'])
    @requires_auth('post:task')
    def new_task(payload):
        try:
            req = request.get_json()
            name = req['name']
            details = req['details']
            complete = req['complete']
            project_id = req['project_id']
            member_id =  req['member_id']
            new_task = Task(name=name, details=details, complete=complete, project_id=project_id, member_id=member_id)
            new_task.insert()
            tasks = Task.query.all()
            data = [task.long() for task in tasks]
            return jsonify({
                'success': True,
                'data': data
            }), 200
        except Exception as e :
            print(e)
            abort(401)


    #---------------UPDATE FUNC---------------------#
    @app.route('/project/<int:id>', methods=['PATCH'])
    @requires_auth('patch:project')
    def update_project(payload, id):
        try:
            getproject  =  Project.query.filter(Project.id == id).first()
            req =   request.get_json()
            getproject.name = req['name']
            getproject.about = req['about']
            getproject.complete =  req['complete']
            getproject.leader_id = req['leader_id']
            getproject.update()
            projects = Project.query.all()
            data = [project.long() for project in projects]
            return jsonify({
                'success': True,
                'data': data
            }), 200
        except Exception as e:
            print(e)
            abort(401)

    @app.route('/task/<int:id>', methods=['PATCH'])
    @requires_auth('patch:task')
    def update_task(payload, id):
        try:
            getTask  =  Task.query.filter(Task.id == id).first()
            req =   request.get_json()
            getTask.name = req['name']
            getTask.details = req['details']
            getTask.complete =  req['complete']
            getTask.project_id = req['project_id']
            getTask.member_id = req['member_id']
            getTask.update()
    
            tasks = Task.query.all()
            data = [task.long() for task in tasks]
            return jsonify({
                'success': True,
                'data': data
            }), 200
        except Exception as e:
            print(e)
            abort(401)
        

    #---------------DELETE FUNC---------------------#
    @app.route('/task/<int:id>', methods=['DELETE'])
    @requires_auth('delete:task')
    def delete_task(payload, id):
        try:
            task = Task.query.filter(Task.id == id).first()
            task.delete()
            return jsonify({
                'success': True,
                'delete': id
            }), 200
        except Exception as e:
            print(e)
            abort(401)



    '''
    error handlers
    '''

    @app.errorhandler(404)
    def error_not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
            }), 404

    @app.errorhandler(AuthError)
    def autherror(error):
        
        return jsonify({
            "success": False, 
            "error": error.status_code,
            "message": error.error['description']
            }), error.status_code

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unathorized'
        }), 401

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        })

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        })

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        })

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)