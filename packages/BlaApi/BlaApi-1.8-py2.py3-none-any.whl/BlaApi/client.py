import datetime
import json
import httpx
from fake_useragent import UserAgent as ua
# from html2text import html2text as h2t
from markdownify import markdownify
import re

class Client:
    client = httpx.Client(verify=False) # instanciate 
    #! BLA credentials must be passed in as string
    def __init__(self, username: str, password: str):
        # Random UserAgent
        self.headers = {'UserAgent': str(ua().chrome)}
        self.username = username
        self.password = password
        login_response=self.login()
        self.token=login_response.get('token')
        self.students=login_response.get('students')
        
        
    def login(self):
        # Construct API endpoint URL
        endpoint = "login"
        api_url = f"https://beaconlightacademy.edu.pk/app/restapi.php?endpoint={endpoint}&rnd=1667581678739&username={self.username}&password={self.password}"
        
        # Send POST request to API endpoint with headers
        response = self.client.post(api_url, headers=self.headers)
        
        #! Raise an error if POST fails
        response.raise_for_status()
        
        # error handling
        if json.loads(response.content).get('success') == False:
            raise ValueError(json.loads(response.content).get('error'))
        
        data = json.loads(response.content)['data']
        # Retrieve access token & student info from JSON response
        token = data.get('accessToken')
        student_data = data.get('students')

        pattern=r'\((\d+[A-Z])\s+[A-Z]+\)'

        # seperate student name and section from name and class string.
        students=[]

        for student in student_data:
            string=student.get('studentName') # name, class and section string eg. 'Foo bar (69C M)'    
            pattern=r'\((.*?)\)' # match values inside parenthesis
            match = re.search(pattern, string) 

            student_name=string.replace(match.group(0), '')
            student_name = student_name.replace('  ', ' ') # remove double spaces from name

            student_class_section = match.group(1).split()[0] # will select '69C' from '69C M'
            student_section = student_class_section[-1] # will select 'C' from '69C'
            student_class=student_class_section.strip(student_section)# student_class=student_class_section.replace(student_section, '')
            students.append(
                {
                'student_name': student_name,
                'section': student_section,
                'class': student_class,
                'student_id': student.get('id'),
                'gr_number': student.get('grNo'),
                }
            )
        # Return retrieved data as dictionary
        output = {
            'token': token,
            'students': students
        }
        return output

    def get_diary_list(self):
        # Construct API endpoint URL
        endpoint = "diaryList"
        api_url = f"https://beaconlightacademy.edu.pk/app/restapi.php?endpoint={endpoint}&accessToken={self.token}&year=1"
        
        # Send POST request to API endpoint with headers
        response = self.client.post(api_url, headers=self.headers)
        
        # error handling
        if json.loads(response.content).get('success') == False:
            raise ValueError(json.loads(response.content).get('error'))
        
        #! Raise an error if POST fails
        response.raise_for_status()
        
        # Retreive diary list from JSON response
        data = json.loads(response.content)['data']
        
        return data

    def get_diary_data(self, notification_ids: list):
        
        output = [] # initialize

        if not isinstance(notification_ids, list): # error check
            raise ValueError("Notification IDs must be passed as a list")
        
        for notification_id in notification_ids:
            # Construct API endpoint URL
            endpoint = "diaryDetails"
            api_url = f"https://beaconlightacademy.edu.pk/app/restapi.php?endpoint={endpoint}&accessToken={self.token}&appUserNotificationId={notification_id}"
            
            # Send POST request to API endpoint with headers
            response = self.client.post(api_url, headers=self.headers)
            
            #! Raise an error if POST fails
            response.raise_for_status()
            
            # error handling
            if json.loads(response.content).get('success') == False:
                raise ValueError(json.loads(response.content).get('error'))
            
            # Retrieve diary data from JSON response
            data = json.loads(response.content)['data']
            # parse diary details by converting to markdown
            data['details'] = markdownify(data.get('details'))
            
            output.append(data)

        return output
    
    def search_by_student(self, passthru=None, student_id=None):

        diary = self.get_diary_list()

        # select the student id on the index: student_number

        
        # parse output from diary list function
        # if student id is a match then
        # return the diaries as a list

        # allows passing of already searched list 
        # to perform further sorting

        output = [] # initialize
        if passthru:
            for p in passthru:
                for d in diary:
                    if p == d['id'] and d['studentId'] == student_id:
                        output.append(d['id'])

        if not passthru:
            for d in diary:
                if d['studentId'] == student_id:  
                    output.append(d['id'])
        if output:
            return output
        else:
            raise LookupError('No entries for provided student id.')
        
    def get_current_date(self):
        
        # Retreive current date in a format that the api requires. 
        #! EXAMPLE: "Tue, 9/11/2001"

        # Get current date and day of week
        current_date = datetime.datetime.today()
        day_of_week = current_date.strftime("%A")

        # Format day of week to abbreviated format (e.g. 'Mon')
        abbreviated_day_of_week = day_of_week[:3]

        # Get current day and month
        current_day = str(current_date.day).zfill(2)
        current_month = str(current_date.month).zfill(2)

        # Format date string
        formatted_date = f"{abbreviated_day_of_week}, {current_day}/{current_month}/{current_date.year}"
        
        return formatted_date

    def search_by_date(self, date, passthru= None):

        diary = self.get_diary_list()
        # parse output from diary list function
        # if student id is a match then
        # return the diaries as a list

        # allows passing of already searched list 
        # to perform further sorting

        output = [] # initialize

        if passthru:
            for p in passthru:
                for d in diary:
                    if p == d['id'] and d['date'] == date:
                        output.append(d['id'])

        if not passthru:
            for d in diary:
                if d['date'] == date:
                    output.append(d['id'])
        if output:
            return output
        else:
            raise LookupError('No matching entries for the specified date.')


    def search_been_read(self, been_read=True, passthru=None):

        diary = self.get_diary_list()

        # parse output from diary list function
        # if diary has been read/unread then
        # return the diaries as a list

        # allows passing of already searched list 
        # to perform further sorting
        # pass in a list of notification ids as passthru arg
         
        
        output = [] # initialize
        
        been_read = str(int(been_read))
        if passthru:
            for p in passthru:
                for d in diary:
                    if p == d['id'] and d['bRead'] == been_read:
                        output.append(d['id'])

        else:
            for d in diary:
                if d['bRead'] == been_read:
                    output.append(d['id'])
        if output:
            return output
        else:
            raise LookupError('No unread/read diaries found.')