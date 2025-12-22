from django.db import models


#admin_registration Table

class admin_registration(models.Model):
    user_id = models.CharField(max_length=30,primary_key=True)
    password = models.CharField(max_length=30)
    email_id = models.EmailField(max_length=30,unique=True)
    phone_number = models.IntegerField()
#faculty_registration Table

class faculty_registration(models.Model):
    faculty_id = models.CharField(max_length=30,primary_key=True)
    password = models.CharField(max_length=30)
    department_name = models.CharField(max_length=30)
    dptname = models.ForeignKey('department',on_delete=models.PROTECT,related_name="FACULTY",null=True,blank=True)
    faculty_name = models.CharField(max_length=30) 
    def __str__(self):
        return self.password

#student_registration Table

class student_registration(models.Model):
    roll_no = models.CharField(max_length=30,primary_key=True)
    password = models.CharField(max_length=30)
    student_name = models.CharField(max_length=50)
    department_name = models.CharField(max_length=30)
    dptname = models.ForeignKey('department',on_delete=models.PROTECT,related_name="STUDENTS",null=True,blank=True)
    year = models.IntegerField()
    email_id = models.EmailField(max_length=30,unique=True)
    def __str__(self):
        return self.password

#question_bank Table
class question_bank(models.Model):
    course_name = models.CharField(max_length=30)
    year = models.IntegerField()
    subject = models.CharField(max_length=30,primary_key=True) 
    
    def __str__(self):
        return self.subject
    


#questions 
class questions(models.Model):
    subject_id = models.CharField(max_length=20,primary_key=True)
    semester = models.CharField(max_length=30)
    subject_k = models.ForeignKey(question_bank,on_delete=models.PROTECT,related_name="QUESTIONS")
    questionupload = models.FileField(upload_to="qndisplay2")

    # def __str__(self):
    #     return self.semester
    
    
    
    
#result Table

class result(models.Model):
    roll_no = models.ForeignKey(student_registration,on_delete=models.PROTECT,related_name="RESULTS")
    score = models.IntegerField()
    correct_answer = models.IntegerField()
    wrong_answer = models.IntegerField()
    remarks = models.CharField(max_length=20)

    
#feedback_and_notification Table

class feedback_and_notification(models.Model):
    roll_no = models.ForeignKey(student_registration,on_delete=models.PROTECT,related_name="FEEDBACKS")
    faculty_id = models.ForeignKey(faculty_registration,on_delete=models.PROTECT,related_name="FEEDBACKS")
    summary = models.CharField(max_length=100)
    notification_id = models.CharField(max_length=20,primary_key=True)
    send = models.CharField(max_length=30)
    receive = models.CharField(max_length=30)


#quiz Table

class quiz(models.Model):   
    quiz_id = models.CharField(max_length=30,primary_key=True)
    question_id = models.CharField(max_length=30,unique=True)
    question = models.CharField(max_length=300)
    correct_option = models.CharField(max_length=300)
    option_A = models.CharField(max_length=300)
    option_B = models.CharField(max_length=300)
    option_C = models.CharField(max_length=300)
    option_D = models.CharField(max_length=300)
    Difficulty_Level = models.CharField(max_length=300,null=True,blank=True,default="easy")

class department(models.Model):
    department_name = models.CharField(max_length=30,primary_key=True)
    
    def __str__(self):
        return self.department_name
    