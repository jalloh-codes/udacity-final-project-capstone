import os
import json
import unittest

from .database.models import setup_db,  Leader, Project, Member, Task
from .auth.auth import AuthError, requires_auth
from .api import  app


manager_auth_header = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1rUTFRa1pGT0RCR01ETTVNREEwUWtGQ05FVTNNakZHTlRkR1FUZzBPVFl4TlVNelJEWTRNQSJ9.eyJpc3MiOiJodHRwczovL21hLXRva2EuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTEwMzMzMjQ3ODI0MTEzNDgyNjA0IiwiYXVkIjpbImFwaS1tYW5hZ2VyIiwiaHR0cHM6Ly9tYS10b2thLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTQwMTAwNjIsImV4cCI6MTYxNDA5NjQ2MiwiYXpwIjoiWWJBSDlZODk5RWtHQ0J4WHljT2NoVEF4c0ZyRENWYkEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnRhc2siLCJnZXQ6cHJvamVjdCIsImdldDp0YXNrIiwicGF0Y2g6cHJvamVjdCIsInBhdGNoOnRhc2siLCJwb3N0Om1lbWJlciIsInBvc3Q6cHJvamVjdCIsInBvc3Q6dGFzayJdfQ.Ug35ZdtzGrB8TU85Aho0VyISxmVjuYDKH-mVRdO9on1dUntC9JpTI2lr9VzDRJwVhwru_kSKQWzn5YQ8fcHplXJgog_r_I1lCrucDFKISZk4nypjJ4vevW3iId3sj3XrIrRByIWy9biHHsGzBGPrPA1jQubRRnrVGFaLxCWYHw9JYdmsU9N4QbO1w4-EJSRyaRnHIGCgkm8E5klfdp7G7GiHC0HYD4MuqhVtbW1mtdihe06IC7eDMDOlh1NtUzvcGecXeci5ZjlWbAUOMSn_Ssi3tTYmNrLc2ZaMMFst-mV1Ul9txDxLk2qXSsXVcFDVC7aIk60cGof6tJa67rP3KQ'
}

member_auth_header = {
    'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1rUTFRa1pGT0RCR01ETTVNREEwUWtGQ05FVTNNakZHTlRkR1FUZzBPVFl4TlVNelJEWTRNQSJ9.eyJpc3MiOiJodHRwczovL21hLXRva2EuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTAxMzc4NzY0NDI1ODQ4Mzk5MjM2IiwiYXVkIjpbImFwaS1tYW5hZ2VyIiwiaHR0cHM6Ly9tYS10b2thLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTQwMDg5MDEsImV4cCI6MTYxNDA5NTMwMSwiYXpwIjoiWWJBSDlZODk5RWtHQ0J4WHljT2NoVEF4c0ZyRENWYkEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnRhc2siLCJnZXQ6cHJvamVjdCIsImdldDp0YXNrIiwicGF0Y2g6dGFzayJdfQ.Vr54b0_jlopOS7tN-3EEmmPwYfgBCS68L0Q4TdH6qlgKrWf2QWUn5TyElsE2reGyDQbQIp5pV82EyeMoT2sQ79nQ6kDUtJWssiimJomBwXqevkbrWJv2kQ99DRGokFerHNE6h6KpTeAFNR1F1bm1YWiYrONPzySlPO20Fu165bFgw9ISZI9RJbLhXxW6isONbylIOTOyOHZjcR9-nP6w0Q4notnCDtCTUXxu2WDYT9chjp_GeOI0n4e5zyTP-Sv4Ygq4QVt_aMGJvM-TeG23FBJJcQbRJQzqXaVqF9mv4shK0yr5_4HGdDzKZF4fNqggGQyF718gi21cziWotvZ9aQ'
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
            'leader_id': 1,
            'member_id': 1
        }

        self.update_task = {
            'name': 'home page',
            'details': 'create the home make sure their is errors',
            'complete': True,
            'leader_id': 1,
            'member_id': 1
        }

    ''''
    Leader class test
    '''
    #get a leader by email
    def get_leader(self):
        res = self.client().get('/leader')
        data =  json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'])

    def error_get_leader(self):
        res = self.client().get('/leader')
        self.assertEqual(res.status_code, 401)
        
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
    #create a new member
    def create_member(self):
        res =  self.client().post('/member', json = self.create_member, headers = manager_auth_header)
        data =  json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'])

    def error_create_member(self):
        res = self.client().post('/member', json =self.create_member)
        self.assertEqual(res.status_code, 401)

    def get_member(self):
        res = self.client().get('/member/1', headers=manager_auth_header)
        data =  json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'])

    def error_get_member(self):
        res = self.client().get('/member/1')
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