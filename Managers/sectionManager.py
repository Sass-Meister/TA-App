from Managers.DjangoStorageManager import DjangoStorageManager as dsm
from Managers.ManagerInterface import ManagerInterface
from TAServer.models import Section, Course as Course, User as User


class SectionManager(ManagerInterface):

    def __init__(self, db: dsm):
        self.db = db

    def add(self, fields: dict)->bool:

        # check if user inputs information needed for adding
        invalid = self.actionHelper(fields.get("dept"), fields.get("cnum"), fields.get("snum"), "addition")
        if invalid != "okay":
            print(invalid)
            return False

        # Make sure course already exists
        if not self.courseExists(cnum=fields.get("cnum"), dept=fields.get("dept")):
            return False

        course = self.db.get_course(dept=fields.get("dept"), cnum=fields.get("cnum"))

        # Make sure section doesn't already exist (Should be edit instead)
        if self.sectionExists(cnum=fields.get("cnum"), dept=fields.get("dept"), snum=fields.get("snum")):
            return False

        try:
            snum = int(fields.get("snum"))
        except ValueError:
            print('Section number is not a valid integer')
            return False

        # section number should be greater than 0
        if snum < 1:
            return False

        # Make sure user exists if inst is to be added
        if fields.get('instructor') is not None and not self.userExists(fields.get('instructor')):
            return False

        # Check days
        if not self.checkDays(fields.get("days")):
            return False

        # Check for correct time format of start and end time
        if not self.timeFormat(fields.get('startTime')) or not self.timeFormat(fields.get('endTime')):
            return False

        start = fields.get('startTime')
        end = fields.get('endTime')
        days = fields.get('days').upper()
        room = fields.get('room')
        # try to convert room into integers
        if room is not None:
            try:
                room = int(room)
            except ValueError:
                print('Room is not a valid integer')
                return False

            # Check if time and room conflict
            if not self.roomConflict(start=start, end=end, room=room, days=days, sec=self.db.get_section(fields.get("cnum"), fields.get("dept"), fields.get("snum")), action="add"):
                return False

        # With and without instructor adding to course and sections db
        if fields.get('instructor') is None:
            toAdd = Section(course=course, snum=snum, stype=fields.get("type"), days=fields.get("days"),
                            room=room, endTime=end, startTime=start)
            self.addHelper(toAdd)
            return True
        else:
            if not self.valUser(fields.get("instructor")):
                return False
            ins = self.db.get_user(fields.get("instructor"))
            toAdd = Section(course=course, snum=snum, stype=fields.get("type"), days=fields.get("days"),
                            room=room, endTime=end, startTime=start, instructor=ins)
            self.addHelper(toAdd)
            return True



    def view(self, fields: dict)->str:

        invalid = self.actionHelper(fields.get("dept"), fields.get("cnum"), fields.get("snum"), "viewing")
        if invalid != "okay":
            return invalid

        result = self.db.get_section(dept = fields.get("dept"), cnum = fields.get("cnum"), snum = fields.get("snum"))
        if result is None:
            return "Could not find " + fields.get("dept") + "-" + str(fields.get("cnum")) + "-" + str(fields.get("snum"))
        else:
            return "Course: " + str(result.course.dept) + "-" + str(result.course.cnum) + "<br>Section: " + str(result.snum) \
                   + "<br>Instructor: " + result.instructor.username + "<br>Meeting time(s): " + str(result.days) + " " \
                   + result.startTime + "-" + result.endTime + "<br>Room: " + str(result.room)


    # Edit will need cnum, snum and dept (like all other commands)
    # Any other fields specified that aren't above(e.g. room, instructor, ect.) will replace what is already in the section
    # You can not change cnum and dept, but if you want to change snum use key "snumNew" as a replacement
    def edit(self, fields: dict)->bool:

        # check if user inputs information needed for adding
        invalid = self.actionHelper(fields.get("dept"), fields.get("cnum"), fields.get("snum"), "addition")
        if invalid != "okay":
            print(invalid)
            return False

        # Make sure course already exists
        if not self.courseExists(cnum=fields.get("cnum"), dept=fields.get("dept")):
            return False

        course = self.db.get_course(fields.get("dept"), fields.get("cnum"))

        # Make sure section exists
        if not self.sectionExists(cnum=fields.get("cnum"), dept=fields.get("dept"), snum=fields.get("snum")):
            return False

        try:
            snum = int(fields.get("snum"))
        except ValueError:
            print('Section number is not a valid integer')
            return False


        # Make sure user exists if inst is to be added
        if fields.get('instructor') is not None and not self.userExists(fields.get('instructor')):
            return False

        # Check days
        if not self.checkDays(fields.get("days")):
            return False

        # Check for correct time format of start and end time
        if not self.timeFormat(fields.get('startTime')) or not self.timeFormat(fields.get('endTime')):
            return False

        start = fields.get('startTime')
        end = fields.get('endTime')
        days = fields.get('days').upper()
        room = fields.get('room')
        # try to convert room into integers
        if room is not None:
            try:
                room = int(room)
            except ValueError:
                print('Room is not a valid integer')
                return False

            # Check if time and room conflict
            if not self.roomConflict(start=start, end=end, room=room, days=days, sec=self.db.get_section(fields.get("cnum"), fields.get("dept"), fields.get("snum")), action="edit"):
                return False

        # With and without instructor adding to course and sections db
        if fields.get('instructor') is None:
            toAdd = Section(course=course, snum=snum, stype=fields.get("type"), days=fields.get("days"),
                            room=room, endTime=end, startTime=start)
            self.editHelper(sec=toAdd, snumNew=fields.get("snumNew"))
            return True
        else:
            if not self.valUser(fields.get("instructor")):
                return False
            ins = self.db.get_user(fields.get("instructor"))
            toAdd = Section(course=course, snum=snum, stype=fields.get("type"), days=fields.get("days"),
                            room=room, endTime=end, startTime=start, instructor=ins)
            self.editHelper(sec=toAdd, snumNew=fields.get("snumNew"))
            return True



    def delete(self, fields: dict)->bool:

        invalid = self.actionHelper(fields.get("dept"), fields.get("cnum"), fields.get("snum"), "deletion")
        if invalid != "okay":
            print(invalid)
            return False

        if self.sectionExists(cnum=fields.get("cnum"), dept=fields.get("dept"), snum=fields.get("snum")):
            section = self.db.get_section(fields.get("cnum"), fields.get("dept"), fields.get("snum"))
            self.db.delete(section)
            return True
        else:
            return False



    # Make sure user exists
    def userExists(self, ins):
        user = self.db.get_user(username=ins)
        return user is not None

    # Make sure course exists
    def courseExists(self, cnum, dept):
        course = self.db.get_course(cnum=cnum, dept=dept)
        return course is not None

    # Make sure section exists
    def sectionExists(self,cnum, dept, snum):
        section = self.db.get_section(cnum=cnum, dept=dept, snum=snum)
        return section is not None

    # make sure necessary fields are not set to None
    def actionHelper(self, dept, cnum, snum, action):
        okay = ""
        switch = {
            dept: "Could not complete " + action + ", department is needed",
            cnum: "Could not complete " + action + ", course number is needed",
            snum: "Could not complete " + action + ", section number is needed"
        }
        return switch.get(None, "okay")

    def addHelper(self, sec: Section):
        self.db.insert_section(sec)

    def editHelper(self, sec: Section, snumNew: str):
        # Check fields that are empty from sec and set them to whatever the current section has
        # Users need to explicitly enter "None" to edit the value to None/default
        toChange = self.db.get_section(cnum=sec.course.cnum, dept=sec.course.dept, snum=sec.snum)

        if sec.stype is None:
            sec.stype = toChange.stype
        if sec.days is None:
            sec.days = toChange.days
        if sec.startTime is None:
            sec.startTime = toChange.startTime
        if sec.endTime is None:
            sec.endTime = toChange.endTime
        if sec.room is None:
            sec.room = toChange.room
        if sec.instructor is None:
            sec.instructor = toChange.instructor


        # remove old section and replace with the new one
        self.db.insert_section(sec)

    # Make sure user is a TA or instructor
    def valUser(self, ins):
        user = self.db.get_user(ins)
        if user.role.lower() != "ta" and user.role.lower() != "instructor" and user.role is not None:
            return False
        else:
            return True

    # Check if days are correct
    def checkDays(self, days=None):
        if days is None:
            return True
        switch = {
            'M': "fine",
            'T': "fine",
            'W': "fine",
            'H': "fine",
            'F': "fine",
            'MW': "fine",
            'TH': "fine",
            'MWF': "fine",
        }
        if switch.get(days.upper(), "Wrong") == "Wrong":
            return False
        else:
            return True
    # check the time input to make sure it's in the correct format 12:20 PM
    def timeFormat(self, time : str)->bool:
        #Note: strip string before passing
        if time is "" or None:
            return True
        broken = time.split(" ")
        if len(broken) is not 2:
            return False
        minHr = broken[0].split(":")
        Hr = minHr[0]
        min = minHr[1]

        #check if min has  2 characters (1:5 pm or 1:0 pm will not be accepted) and hr has at least one but not more than 2 (01:30 or 1:30 is fine)
        if len(min) != 2 or len(Hr) > 2 or len(Hr) < 1:
            return False

        # try to convert two strings into integers (minute and hour)
        try:
            min = int(min)
            Hr = int(Hr)
        except ValueError:
            print ('Time is not a valid integer')
            return False

       # for min and Hr, check appropriate range
        if min < 0 or min >= 60:
            return False
        if Hr < 1 or Hr > 12:
            return False

        # check if the second half of the original split string broken[1] should be
        # either am or pm (lower case)
        partDay = broken[1].lower()
        if partDay == "am" or partDay == "pm":
            return True
        else:
            return False

    # This helper will take a time in string format and return a integer time
    # The integer will be in military hours for easy comparison in roomConflict()
    # NOTE: time format should be called before calling this method or else int() conversion will fail
    def intTime(self, time: str)->int:

        breakDown = time.split(" ")
        meridies = breakDown[1]
        minHr = breakDown[0].split(":")
        hr = int(minHr[0])
        min = int(minHr[1])

        # convert to military time
        if meridies.lower() == "pm" and hr != 12:
            hr = hr + 12
        elif meridies.lower() == "am" and hr == 12:
            hr = 0
        if min == 0:
            min = "00"
        else:
            min = str(min)

        hr = str(hr)
        intTime = hr + min
        intTime = int(intTime)
        return intTime

    # NOTE: timeFormat() should be called before calling this method
    def roomConflict(self, start: str, end: str, room: int, days: str, sec: Section, action: str)->bool:

        if start is None or room is -1 or end is None or days is None:
            return True

        roomUse = Section.objects.filter(room=room)
        if roomUse.count() > 0:

            # get integer values for start and end times for comparison
            startTime = self.intTime(start)
            endTime = self.intTime(end)

            for x in roomUse:
                # Need to make certain not to compare the same object on edit, this shouldn't happen with add
                if sec is None or action == "edit" and sec.snum != x.snum:
                    if days == x.days:
                        xStart = self.intTime(x.startTime)
                        xEnd = self.intTime(x.endTime)

                        # check if start and end time is between each other class that shares the same room
                        if xStart <= startTime <= xEnd:
                            return False
                        elif xStart <= endTime <= xEnd:
                            return False
                else:
                    if days == x.days:
                        xStart = self.intTime(x.startTime)
                        xEnd = self.intTime(x.endTime)

                        # check if start and end time is between each other class that shares the same room
                        if xStart <= startTime <= xEnd:
                            return False
                        elif xStart <= endTime <= xEnd:
                            return False

        return True

    @staticmethod
    def reqFields()->list:
        return ["dept", "cnum", "snum"]

    # Note: "snumNew" will only do something if the user calls edit and wants to change the section number
    @staticmethod
    def optFields()->list:
        return ["instructor", "type", "days", "room", "startTime", "endTime"]