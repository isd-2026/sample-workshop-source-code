import unittest
from backend.app import create_app
from backend.models.db_connect import get_connection

class AppTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.app = app.test_client()
        # TODO: explain ctx
        self.ctx = app.app_context()
        self.ctx.push()

    # ---------- auth ----------
    # register a dupilcated user
    # use TU* as a naming convention for all test users
    def test_register_route_duplicated_user(self):
        response1 = self.app.post('/auth/register',json={'name':'TU1','email':'tu1@email.com','password':'pw','gender':'f','favcol':'yellow'})
        response2 = self.app.post('/auth/register',json={'name':'TU1','email':'tu1@email.com','password':'pw','gender':'f','favcol':'yellow'})
        self.assertEqual(response2.status_code, 409)

    # register a new user with the correct details
    def test_register_route_success(self):
        response1 = self.app.post('/auth/register',json={'name':'TU2','email':'tu2@email.com','password':'pw','gender':'m','favcol':'pink'})
        data = response1.get_json()
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(data["user"]["email"],"tu2@email.com")
        # delete after the test to avoid duplication error in the next run
        response2 = self.app.delete('/users/delete',json={'email':'tu2@email.com'})

    # a successful login
    def test_login_route_success(self):
        response1 = self.app.post('/auth/register',json={'name':'TU3','email':'tu3@email.com','password':'pw','gender':'m','favcol':'pink'})
        response2 = self.app.post('/auth/login',json={'email':'tu3@email.com','password':'pw'})
        self.assertEqual(response2.status_code,200)

    # a failed login for an nonexistent user
    def test_login_nonexistent_user(self):
        response = self.app.post('/auth/login',json={'email':'tu4@test.com','password':'pw'})
        self.assertEqual(response.status_code, 404)

    # def test_login_session_variable(self):
    #     # retrieve the user_name from session
    #     with self.app as client:
    #         response1 = self.app.post('/auth/register',json={'name':'TU7','email':'tu7@email.com','password':'pw','gender':'m','favcol':'pink'})
    #         response2 = self.app.post('/auth/login',json={'email':'tu7@email.com','password':'pw'})

    #         # Access session variables
    #         with client.session_transaction() as sess:
    #             self.assertEqual(sess["user_email"], "tu7@email.com")

    # def test_logout_route(self):
    #     response = self.app.get('/auth/logout')
    #     self.assertEqual(response.status_code, 200)

    # ---------- users ----------
    def test_list_users_route(self):
        # add 2 test users
        response1 = self.app.post("/users/add", json={"name":"TU8","email":"tu8@email.com","password":"pw","gender":"f","favcol":"black"}, headers={"x-api-key": "admin-secret-key"})
        response1 = self.app.post("/users/add", json={"name":"TU9","email":"tu9@email.com","password":"pw","gender":"f","favcol":"black"}, headers={"x-api-key": "admin-secret-key"})

        response3 = self.app.get('/users/list', headers={"x-api-key": "admin-secret-key"})
        user_list = response3.get_json()["user_list"]
        self.assertTrue(any(u["email"] == "tu8@email.com" for u in user_list))
        self.assertTrue(any(u["email"] == "tu9@email.com" for u in user_list))

    def test_add_and_view_user_route(self):
        response1 = self.app.post("/users/add", json={"name":"TU5","email":"tu5@email.com","password":"pw","gender":"f","favcol":"black"}, headers={"x-api-key": "admin-secret-key"})
        response2 = self.app.get("/users/view", json={"email": "tu5@email.com"}, headers={"x-api-key": "admin-secret-key"})
        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.get_json()["user"]["email"],"tu5@email.com")
        response3 = self.app.delete('/users/delete',json={'email':'tu5@email.com'})

    def test_update_user_route(self):
        new_email = "tu5.new@email.com"
        response1 = self.app.post("/users/add", json={"name":"TU5","email":"tu5@email.com","password":"pw","gender":"f","favcol":"black"}, headers={"x-api-key": "admin-secret-key"})
        response2 = self.app.post("/users/update", json={"email":"tu5@email.com","new_email":new_email}, headers={"x-api-key": "admin-secret-key"})
        response3 = self.app.get("/users/view", json={"email":new_email}, headers={"x-api-key": "admin-secret-key"})
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.get_json()["user"]["email"],new_email)
        response4 = self.app.delete('/users/delete',json={"email":new_email}, headers={"x-api-key": "admin-secret-key"})

    def test_delete_user_route(self):
        response1 = self.app.post("/users/add", json={"name":"TU6","email":"tu6@email.com","password":"pw","gender":"f","favcol":"black"}, headers={"x-api-key": "admin-secret-key"})
        response2 = self.app.delete('/users/delete',json={'email':'tu6@email.com'}, headers={"x-api-key": "admin-secret-key"})
        self.assertEqual(response2.status_code, 200)

    def tearDown(self):
        self.ctx.pop() # remove the app context

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE name LIKE 'TU%'")
        conn.commit()
        return super().tearDown()

if __name__ == '__main__':
    unittest.main()