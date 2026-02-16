from django.db import models

# Department Table
class Department(models.Model):
    
    department_name = models.CharField(max_length=30,)

    def __str__(self):
        return self.department_name


# Admin Registration

class Adminstrator(models.Model):
    user_name = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=128) 

# Faculty Registration
class FacultyRegistration(models.Model):
    faculty_id = models.CharField(max_length=30, primary_key=True)
    faculty_name = models.CharField(max_length=30)
    password = models.CharField(max_length=128)
    email  = models.EmailField(null=True,unique=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="FACULTY"
    )

    def __str__(self):
        return self.faculty_name


# Student Registration
class StudentRegistration(models.Model):
    roll_no = models.CharField(max_length=30, primary_key=True)
    student_name = models.CharField(max_length=50)
    email_id = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="STUDENTS"
    )
    year = models.IntegerField()
    

    def __str__(self):
        return self.student_name


# Course Table
class Course(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name = "COURSES"
    )
    course_name = course_name = models.CharField(max_length=30)
    def __str__(self):
        return self.course_name


# Subject Table
class Subject(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name = "SUBJECTS"
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name = "SUBJECTS"
    )
    subject_name =  models.CharField(max_length=30)
    
    def __str__(self):
        return self.subject_name



# Question Bank
class QuestionBank(models.Model):
    course_name = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="QUESTION_BANK"
    )
    file= models.FileField(upload_to="qndisplay/")
    year = models.IntegerField()
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name = "QUESTION_BANK"
    )

    def __str__(self):
        return f"{self.subject.subject_name} - {self.year}"


#mcq  Questions practise set
class Quiz(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name = "QUESTIONS"
    )
    semester = models.CharField(max_length=30)
    quiz_name = models.CharField(max_length=40)
    pass_mark = models.IntegerField()

    def __str__(self):
        return self.quiz_name


# Result
class Result(models.Model):
    student = models.ForeignKey(
        StudentRegistration,
        on_delete=models.PROTECT,
        related_name="RESULTS"
    )
    score = models.IntegerField()
    correct_answer = models.IntegerField()
    wrong_answer = models.IntegerField()
    remarks = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.student.roll_no} - {self.score}"


# Feedback and Notification
class FeedbackAndNotification(models.Model):
    notification_id = models.CharField(max_length=20, primary_key=True)
    student = models.ForeignKey(
        StudentRegistration,
        on_delete=models.PROTECT,
        related_name="FEEDBACKS"
    )
    faculty = models.ForeignKey(
        FacultyRegistration,
        on_delete=models.PROTECT,
        related_name="FEEDBACKS"
    )
    summary = models.CharField(max_length=100)
    send = models.CharField(max_length=30)
    receive = models.CharField(max_length=30)

    def __str__(self):
        return self.notification_id


#Questions in quiz
class QuizQuestion(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='questions'
    )
    question_text = models.TextField()

    def __str__(self):
        return self.question_text[:50]


#Options for each question
class QuizOption(models.Model):
    question = models.ForeignKey(
        QuizQuestion,
        on_delete=models.CASCADE,
        related_name='options'
    )
    option_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    explananation = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.option_text
    

#Quiz Attempt by student
class QuizAttempt(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name='attempts'
    )
    student = models.ForeignKey(
        StudentRegistration,
        on_delete=models.CASCADE,
        related_name='quiz_attempts'
    )
    score = models.FloatField(null=True, blank=True)
    passed = models.BooleanField(default=False)
    is_mock = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quiz', 'student','is_mock')


# Answers selected by student
class QuizAnswer(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name='answers'
    )
    question = models.ForeignKey(
        QuizQuestion,
        on_delete=models.CASCADE
    )
    selected_option = models.ForeignKey(
        QuizOption,
        on_delete=models.CASCADE
    )