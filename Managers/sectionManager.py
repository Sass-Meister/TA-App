from Managers.JSONStorageManager import JSONStorageManager as jsm
import abc



class SectionManager(abc.ABC):

    # validates and adds to database if okay
    def add(self, dept=None, cnum=None, snum=None, ins=None):
        pass

    # validates and deletes from database
    def delete(self, dept=None, cnum=None, snum=None, ins=None):
        pass

    # validates and copies information from database to report
    def view(self, dept=None, cnum=None, snum=None, ins=None):
        pass

    # validates and takes given section and edits what is asked to edit
    def edit(self, dept=None, cnum=None, snum=None, ins=None):
        pass


class mySectionManager(SectionManager):

    def __init__(self):
        self.db = jsm()


    # validates and adds to database if okay
    def add(self, dept=None, cnum=None, snum=None, ins=None):

        """check if user inputs information needed for adding"""
        invalid = self.actionHelper(dept, cnum, snum, "addition")
        if invalid != "okay":
            return invalid

        """Make sure user exists if inst is to be added"""
        if ins is not None and not self.userExists(ins):
            return ins + " does not exist in the system"

        """With and without instructor adding to course and sections db"""
        if ins is None:
            self.addHelper(dept, cnum, snum, ins)
            return "Section Added: " + dept + "-" + cnum + "-" + snum
        else:
            if not self.valUser(ins):
                return "User can't instruct the course"
            self.addHelper(dept, cnum, snum, ins)
            return "Section Added: " + dept + "-" + cnum + "-" + snum + " instructor: " + ins



    # validates and deletes from database
    def delete(self, dept=None, cnum=None, snum=None, ins=None):
        pass

    # validates and copies information from database to report
    def view(self, dept=None, cnum=None, snum=None, ins=None):

        """check if user has input enough information"""
        invalid = self.actionHelper(dept, cnum, snum, "view")
        if invalid != "okay":
           return invalid

        """Check if Section exists in the database and return (e.g. Course: CS-251 Section: 401 Instructor: Bob)"""
        result = self.db.get_section(dept, cnum, snum)
        if result is None:
            return "Could not find " + dept + "-" + cnum + "-" + snum
        else:
            return "Course: " + result.dept + "-" + result.cnum + "\nSection: " + result.snum \
                   + "\nInstructor: " + result.instructor

    # validates and takes given section and edits what is asked to edit
    def edit(self, dept=None, cnum=None, snum=None, ins=None):
        pass

    # make sure necessary fields are not set to None
    def actionHelper(self, dept, cnum, snum, action):
        okay = ""
        switch = {
            dept: "Could not complete " + action + ", department is needed",
            cnum: "Could not complete " + action + ", course number is needed",
            snum: "Could not complete " + action + ", section number is needed"
        }
        return switch.get(None, "okay")

    # Make sure user exists
    def userExists(self, ins):
        user = self.db.get_user(ins)
        return user is not None

    # Make sure user is a TA or instructor
    def valUser(self, ins):
        user = self.db.get_user(ins)
        if user.role.lower() != "ta" and user.role.lower() != "instructor":
            return False
        else:
            return True

    def addHelper(self, dept, cnum, snum, ins):
        sec = self.db.Section(dept, cnum, snum, ins)
        self.db.insert_section(sec)
        course = self.db.get_course(dept, cnum)
        if snum not in course.sections:
            course.sections.append(snum)
        self.db.insert_course(course)