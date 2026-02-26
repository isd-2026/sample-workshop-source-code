import unittest
from backend.project_bidding import User, Project, Allocation, DB, Admin
import random

class TestAllocation(unittest.TestCase):

    def setUp(self):
        self.db = DB()
        self.admin = Admin(self.db)

        # create 3 projects (Coorporate Website Redesign (5), Marketplace (6, default), Health Monitoring App (6, default))
        p1 = Project(1,"Coorporate Website Redesign",max_students=5)
        p2 = Project(2,"Marketplace",technical_weight=0.4,communication_weight=0.4,innovation_weight=0.2)
        p3 = Project(3,"Health Monitoring App",technical_weight=0.4,communication_weight=0.2,innovation_weight=0.4)
        self.projects = [p1,p2,p3]
        self.db.add_project(p1)
        self.db.add_project(p2)
        self.db.add_project(p3)

        # create 20 test users with randomly generated ids and names at the start
        user_ids_set = set()  # Use a set to ensure uniqueness
        while len(user_ids_set) < 20:
            user_id = str(random.randint(1, 9)) + ''.join(str(random.randint(0, 9)) for _ in range(5))
            user_ids_set.add(user_id)
            
        user_ids = list(user_ids_set)

        student_names = ["Olivia Smith","Liam Johnson","Emma Williams","Noah Brown","Ava Jones",\
            "Elijah Garcia","Sophia Miller","Lucas Davis","Isabella Rodriguez","Alexander White",\
            "Mason Martinez","Mia Hernandez","Ethan Lopez","Amelia Gonzalez","Logan Wilson",\
            "Harper Anderson","James Thomas","Charlotte Taylor","Benjamin Moore","Evelyn Jackson"]

        students = []
        for i in range(20):
            s = User(user_ids[i],student_names[i],self.db)
            students.append(s)
            self.db.add_student(s)
        self.students = students
        
    def test_registration_success(self):
        student = self.students[0]
        m = student.register("Coorporate Website Redesign",5,3,2)
        self.assertEqual(student.registered,True)
        self.assertEqual(m,"Registration successful!")

    def test_duplicated_registration_fail(self):
        student = self.students[0]
        student.register("Coorporate Website Redesign",5,3,2)
        m = student.register("Coorporate Website Redesign",5,3,2)
        self.assertEqual(m,"You have already registered")

    def test_allocation_success(self):
        # for each student randomly generate parameters project name, technical, communication, innovation
        for student in self.students:
            project_name = random.choice(["Coorporate Website Redesign","Marketplace","Health Monitoring App"])
            
            remaining_bids = 10
            technical = random.randint(0,remaining_bids)
            remaining_bids -= technical
            communication = random.randint(0,remaining_bids)
            remaining_bids -= communication
            innovation = random.randint(0,remaining_bids)
            remaining_bids -= innovation
            
            student.register(project_name,technical,communication,innovation)
        
        project_name = "Coorporate Website Redesign"
        self.admin.allocate(project_name)
        project_allocations = self.db.get_allocations_by_project_name(project_name)
        project = self.db.get_project_by_name(project_name)
        print([a.student for a in project_allocations])
        self.assertTrue(len(project_allocations) <= project.max_students)

    def tearDown(self):
        # Clear all lists in DB
        self.db.students.clear()
        self.db.projects.clear()
        self.db.registrations.clear()
        self.db.allocations.clear()
        
        # Remove references to objects
        self.students = []
        self.projects = []
        self.admin = None
        self.db = None

if __name__ == "__main__":
    unittest.main()