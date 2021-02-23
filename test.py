import os
import json
import unittest

from .database.models import setup_db,  Leader, Project, Member, Task
from .auth.auth import AuthError, requires_auth
from .api import  app


manager_auth_header = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1rUTFRa1pGT0RCR01ETTVNREEwUWtGQ05FVTNNakZHTlRkR1FUZzBPVFl4TlVNelJEWTRNQSJ9.eyJpc3MiOiJodHRwczovL21hLXRva2EuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTEwMzMzMjQ3ODI0MTEzNDgyNjA0IiwiYXVkIjpbImFwaS1tYW5hZ2VyIiwiaHR0cHM6Ly9tYS10b2thLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTQwOTIwOTAsImV4cCI6MTYxNDE3ODQ5MCwiYXpwIjoiWWJBSDlZODk5RWtHQ0J4WHljT2NoVEF4c0ZyRENWYkEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnRhc2siLCJnZXQ6bWVtYmVyIiwiZ2V0OnByb2plY3QiLCJnZXQ6dGFzayIsInBhdGNoOnByb2plY3QiLCJwYXRjaDp0YXNrIiwicG9zdDptZW1iZXIiLCJwb3N0OnByb2plY3QiLCJwb3N0OnRhc2siXX0.e-IlOQhoJMZji0TcH5hXWUmOjKhXLayivRfZvLwil7lveIPDbmdOEix29bwZAGHVMx_QiVTQT35tj7Z8rs26cR3F4S3ip2BuD_NRpuW73sR4YRAu6f7UfK5wGqYHogcu0Ii-KBUFIx9ied4c7Vyl_fBXzvSNdmW87pbKfYDeV4xicoSqSFqLqUxiZftDBGgO8hUp1keZ98AlQAQT8tSWU5uMc2LOLArSgQzLtFEWooEPzQjBYIHmZ96tUHX0R-6kOvNn7sZPEnuhQ4wI1O1BzAj_iB8Ntf9GOOncuCEkFtKODANoRnbgI7WYCSB9XYVTyvqWrtvA-m_eQm87mKo1Hw'
}

member_auth_header = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1rUTFRa1pGT0RCR01ETTVNREEwUWtGQ05FVTNNakZHTlRkR1FUZzBPVFl4TlVNelJEWTRNQSJ9.eyJpc3MiOiJodHRwczovL21hLXRva2EuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTAxMzc4NzY0NDI1ODQ4Mzk5MjM2IiwiYXVkIjpbImFwaS1tYW5hZ2VyIiwiaHR0cHM6Ly9tYS10b2thLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTQwOTIxNTksImV4cCI6MTYxNDE3ODU1OSwiYXpwIjoiWWJBSDlZODk5RWtHQ0J4WHljT2NoVEF4c0ZyRENWYkEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnRhc2siLCJnZXQ6bWVtYmVyIiwiZ2V0OnByb2plY3QiLCJnZXQ6dGFzayIsInBhdGNoOnRhc2siXX0.kXbCBQOU9UtexZgrY3IusvPu-jZoVgVUjFmFZgK3snrSgkouJ0SLy0V4nLtHY81vBpIP8wgD9ybsE8RviKk6ZbKxx9dQDX4a1LF5gOYUnma1TC9uF24oNddiqRDSK2G4An-45I_V5YXeFCxTgIpdSSs-RYqCxAHCZBs0iuy6j4xwJZ8mW_F9X1kdPVn2GAf2GoE-ITDrfwtGCnE6GTGSyAPTERqmSOWsr5SiwEKgE7DO6pznD3DBRjV5WAaMqfP47-ny8QWqao93o5JGVNmHqEqck9m85Ftrn3NTMohXEZOFkggqve4LgbSfRN4mL9jhcvF6fC79UDz5fhFsRlrZjA'
}


class MangerTest(unittest.TestCase):



    def setUp(self):
        self.app = app
        self.client =  self.app.test_client
        self.database_path = "postgres://hllanhox:gUGLEZB43EJ7YDV0XRV8V9pefd3SyKB1@ziggy.db.elephantsql.com:5432/hllanhox"
        self.init_app(app)
        self.create_all()

        self.create_leader = {
            'email': 'test@mail.com',
            'firstname': 'Oumou',
            'lastname': 'Bah',
        }
        
        self.create_member = {
            'email': 'test@mail.com',
            'firstname': 'Ra',
            'lastname': 'Diallo',
            'leader_id': 1
        }

        self.create_project = {
            'name': 'Toka App',
            'about': 'This is app messaging application project',
            'complete': False,
            'leader_id': 1
        }

        self.update_project = {
            'name': 'Toka App',
            'about': 'This is app messaging application project',
            'complete': True,
            'leader_id': 1
        }

        self.create_task = {
            'name': 'home page',
            'details': 'create the home make sure their is errors',
            'complete': False,
            'project_id': 1,
            'member_id': 1
        }

        self.update_task = {
            'name': 'home page',
            'details': 'create the home make sure their is errors',
            'complete': True,
            'project_id': 1,
            'member_id': 1
        }

    ''''
    Leader class test
    '''
    #get a leader by email
    def get_leader(self):
        res = self.client().get('/')
        data =  json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'])

    def error_get_leader(self):
        res = self.client().get('/leader')
        self.assertEqual(res.status_code, 404)
        
    #create a new leader
    def create_leader(self):
        res =  self.client().post('/leader', json = self.create_leader)
        data =  json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'])
        
    def error_create_leader(self):
        res = self.client().post('/member', json =self.create_leader)
        self.assertEqual(res.status_code, 401)

    ''''
    Member class test
    '''
    def get_member(self):
        res =  self.client().post('/member', headers=manager_auth_header)
        data =  json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'])
    
    def error_get_leader(self):
        res = self.client().get('/member')
        self.assertEqual(res.status_code, 401)

    #create a new member
    def create_member(self):
        res =  self.client().post('/member', json = self.create_member, headers = manager_auth_header)
        data =  json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'])

    def error_create_member(self):
        res = self.client().post('/member', json =self.create_member)
        self.assertEqual(res.status_code, 401)


    '''
    Project class test
    '''
    def create_project(self):
        res = self.client().post('/project', json=self.create_project, headers=manager_auth_header)
        data =  json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'])

    def error_create_project(self):
        res = self.client().post('/project', json=self.create_project)
        self.assertEqual(res.status_code, 401)


    def get_project(self):
        res =  self.client().get('/project/1', headers=manager_auth_header)
        data =  json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'])

    def error_get_project(self):
        res = self.client().get('/project/1')
        self.assertEqual(res.status_code, 401)

    def patch_project(self):
        res =  self.client().patch('/project/1', json=self.update_project, headers=manager_auth_header)
        data =  json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'])


    def error_patch_project(self):
        res =  self.client().patch('/project/1', json=self.update_project)
        self.assertEqual(res.status_code, 401)


    '''
    Task class test
    '''
    def create_task(self):
        res = self.client().post('/task/1',json=self.create_task, headers=manager_auth_header)
        data =  json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'])

    def error_create_task(self):
        res = self.client().post('/task/', json=self.create_task)
        self.assertEqual(res.status_code, 401)

    def get_task(self):
        res = self.client().get('/task/1', headers=manager_auth_header)
        data =  json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'])

    def error_get_task(self):
        res = self.client().get('/task/1')
        self.assertEqual(res.status_code, 401)
    
    def patch_task(self):
        res =  self.client().patch('/task/1', json=self.update_task, headers=member_auth_header)
        data =  json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'])

    def error_patch_task(self):
        res =  self.client().patch('/task/1', json=self.update_project)
        self.assertEqual(res.status_code, 401)

    def delete_task(self):
        res = self.client().delete('/task/1', headers=member_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'])
        self.assertEqual(data['delete'], 1)

    def error_delete_task(self):
        res =  self.client().delete('/task/1')
        self.assertEqual(res.status_code, 401)

if __name__ == "__main__":
    unittest.main()