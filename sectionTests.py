import unittest
from courseManager import CourseManager
from sectionManager import mySectionManager
from user_manager import UserManager
from JSONStorageManager import JSONStorageManager as StorageManager

class sectionTest(unittest.TestCase):

    def setUp(self):
        self.course = CourseManager()
        self.course.add(dept="CS", cnum="251")
        self.user = UserManager(StorageManager())
        self.db = StorageManager()
        Bob = self.db.User("Bob", "123", "Instructor")
        self.db.insert_user(Bob)
        Rob = self.db.User("Rob", "123")
        self.db.insert_user(Rob)
        Cobb = self.db.User("Randall Cobb", "123",  "Instructor")
        self.db.insert_user(Cobb)
        self.course.add(dept="CS", cnum="351", instr="Bob", section="401")
        self.course.add(dept="CS", cnum="337")
        self.sec = mySectionManager()

    def tearDown(self):
        del self.course
        del self.user
        del self.sec

    def test_add(self):
        self.assertEqual(self.sec.add("CS", "251", "401"), "Section Added: CS-251-401")
        self.assertEqual(self.sec.add("CS", "251", "401", "Bob"), "Section Added: CS-251-401 instructor: Bob")

    def test_addNoInfo(self):
        self.assertEqual("Could not complete addition, section number is needed",
                               self.sec.add(dept="CS", cnum="251"))
        self.assertEqual("Could not complete addition, section number is needed",
                               self.sec.add(dept="CS", cnum="251", ins="Bob"))
        self.assertEqual("Could not complete addition, course number is needed",
                               self.sec.add(dept="CS", snum="401", ins="Bob"))
        self.assertEqual("Could not complete addition, department is needed",
                               self.sec.add(cnum="251", snum="401", ins="Bob"))

    # user does not exist and shouldn't be able to be added
    def user_none(self):
        self.assertEqual("Nobody does not exist in the system", self.sec.add(dept="CS", cnum="251", snum="401", ins="Nobody"))

    def test_notQualified(self):
        self.assertEqual("User can't instruct the course", self.sec.add(dept="CS", cnum="337", snum="401", ins="Rob"))

    # test "section view secNum" command output
    def test_view(self):
        self.assertEqual(self.sec.view(dept="CS", cnum="351", snum="401"), "Course: CS-351\nSection: 401\nInstructor: Bob")

    def test_viewNoInfo(self):
        self.assertEqual("Could not complete view, section number is needed",
                               self.sec.view(dept="CS", cnum="251"))
        self.assertEqual("Could not complete view, section number is needed",
                               self.sec.view(dept="CS", cnum="251", ins="Bob"))
        self.assertEqual("Could not complete view, course number is needed",
                               self.sec.view(dept="CS", snum="401", ins="Bob"))
        self.assertEqual("Could not complete view, department is needed",
                               self.sec.view(cnum="251", snum="401", ins="Bob"))