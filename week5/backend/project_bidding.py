'''
Here Users are students, each student has 10 bids and can nominate themselves to 1 project
Students can submit their bids to the three categories: technical, communication, innovation, indicating their ability/confidence in each of these category
Each project defines the weights for each of these categories
The weighted_bids is calculated as the sum of the weighted bids in all categories
Each project also defines the maximum number of students, with 6 being the default maximum
Students are ranked based on their weighted_bids and the the top X students are selected where X is the maximum number of students for each project
'''

class User:
    def __init__(self,id,name,db):
        self.id = id
        self.name = name
        self.bids = 10
        self.db = db
        self.registered = False
    
    def register(self,project_name,technical,communication,innovation):
        if (self.registered == True):
            return "You have already registered"
        if (technical < 0 or communication < 0 or innovation < 0):
            return "Bids should be no less than 0."
        if (technical + communication + innovation > self.bids):
            return "You have exceeded your bid limit."
        self.registered = True
        self.db.add_registration(Registration(self.id,project_name,technical,communication,innovation))
        return "Registration successful!"
        
class Project:
    def __init__(self, id, name, max_students=6, 
                 technical_weight=0.5, communication_weight=0.3, innovation_weight=0.2):
        self.id = id
        self.name = name
        self.max_students = max_students
        self.technical = technical_weight
        self.communication = communication_weight
        self.innovation = innovation_weight

# Registration & Allocation both use composite key (student_id, project_name) as the primary key
class Registration:
    def __init__(self,student_id,project_name,technical,communication,innovation):
        self.student = student_id
        self.project = project_name
        self.technical = technical
        self.communication = communication
        self.innovation = innovation

class Allocation:
    def __init__(self, student_id, project_name):
        self.student = student_id
        self.project = project_name
        
class DB:
    def __init__(self):
        self.students = []
        self.projects = []
        self.registrations = []
        self.allocations = []
        
    def add_student(self, student):
        self.students.append(student)
        
    def add_project(self, project):
        self.projects.append(project)

    def add_registration(self,registration):
        self.registrations.append(registration)
        
    def add_allocation(self, allocation):
        self.allocations.append(allocation)
    
    def get_student_by_id(self,student_id):
        for s in self.students:
            if s.id == student_id:
                return s
        return None
    
    def get_project_by_name(self,project_name):
        for p in self.projects:
            if p.name == project_name:
                return p
        return None
    
    def get_registration_by_student_id(self,student_id):
        for r in self.registrations:
            if r.student == student_id:
                return r
        return None
    
    def get_allocations_by_project_name(self,project_name):
        allocs = []
        for a in self.allocations:
            if a.project == project_name:
                allocs.append(a)
        return allocs

# admin has access to the entire db
class Admin:
    def __init__(self, db):
        self.db = db
        
    # the input is all registrations
    def allocate(self,project_name):
        # get the project obj by name
        project = self.db.get_project_by_name(project_name)
        
        # getting only registrations for the particular project and names of all registered students
        project_registrations = []
        all_registrations = self.db.registrations
        project_registrations = [r for r in all_registrations if r.project == project_name]
        registered_student_ids = [r.student for r in project_registrations]
        
        selected_student_ids = []
        
        if len(registered_student_ids) <= project.max_students:
            selected_student_ids = registered_student_ids
        else:
            id_bids_pairs = []
            for registration in project_registrations:
                # calculate weighted bids
                weighted_bids = registration.technical*project.technical+\
                    registration.communication*project.communication+\
                        registration.innovation*project.innovation
                        
                id_bids_pairs.append((registration.student,weighted_bids))
                
            sorted_id_bids_pairs = sorted(id_bids_pairs,key=lambda x: x[1], reverse=True)
            selected_student_ids = [pair[0] for pair in sorted_id_bids_pairs][:project.max_students]
            
            # TODO: implement tie breaking
        
        # generate allocations
        project_allocations = []
        for id in selected_student_ids:
            alloc = Allocation(id, project_name)
            project_allocations.append(alloc)
            self.db.add_allocation(alloc)