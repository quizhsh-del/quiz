from django import forms
from .models import (
    Department,
    FacultyRegistration,
    StudentRegistration,
    Course,
    Subject,
    QuestionBank,
    Quiz,
    Result,
    FeedbackAndNotification,
    QuizQuestion,
    QuizOption,
    QuizAttempt,
    QuizAnswer,
)

# ---------------------------------
# Department Form
# ---------------------------------
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'
        widgets = {
            'department_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Department Name'
            })
        }



# ---------------------------------
# Faculty Registration Form
# ---------------------------------
class FacultyRegistrationForm(forms.ModelForm):
    class Meta:
        model = FacultyRegistration
        fields = '__all__'
        widgets = {
            'faculty_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Faculty ID'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Password'
            }),
            'faculty_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Faculty Name'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


# ---------------------------------
# Student Registration Form
# ---------------------------------
class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = StudentRegistration
        fields = '__all__'
        widgets = {
            'roll_no': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Roll Number'
            }),
            'student_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Student Name'
            
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Password'
            }),
            'email_id': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email'
            
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Year'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class StudentLoginForm(forms.Form):
    roll_no = forms.CharField(
        label="Roll Number",
        widget=forms.TextInput(attrs={'placeholder': 'Enter Roll Number'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'})
    )


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = StudentRegistration
        exclude = ['roll_no', 'password']   
        widgets = {
            'student_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Student Name'
            }),
            'email_id': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Email'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Year'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
        }



# ---------------------------------
# Course Form
# ---------------------------------
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
            'course_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Course Name'
            }),
        }


# ---------------------------------
# Subject Form
# ---------------------------------
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
        widgets = {
            'course': forms.Select(attrs={
                'class': 'form-control'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control'
            }),
            'subject_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Subject Name'
            }),
        }


# ---------------------------------
# Question Bank Form
# ---------------------------------
class QuestionBankForm(forms.ModelForm):
    class Meta:
        model = QuestionBank
        fields = '__all__'
        widgets = {
            'course_name': forms.Select(attrs={
                'class': 'form-control'
            }),
            'file': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Year'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


# ---------------------------------
# Quiz Form
# ---------------------------------
class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'
        widgets = {
            'subject': forms.Select(attrs={
                'class': 'form-control'
            }),
            'semester': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Semester'
            }),
        
            'quiz_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Quiz Name'
            }),
            'pass_mark': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Pass Mark'
            }),
        }


# ---------------------------------
# Quiz Question Form
# ---------------------------------
class QuizQuestionForm(forms.ModelForm):
    class Meta:
        model = QuizQuestion
        fields = '__all__'
        widgets = {
            'quiz': forms.Select(attrs={
                'class': 'form-control'
            }),
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter Question'
            }),
        }


# ---------------------------------
# Quiz Option Form
# ---------------------------------
class QuizOptionForm(forms.ModelForm):
    class Meta:
        model = QuizOption
        fields = ['option_text', 'is_correct', 'explananation']

        widgets = {
            'question': forms.Select(attrs={
                'class': 'form-control'
            }),
            'option_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Option'
            }),
            'explananation': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Explanation (optional)'
            }),
        }


# ---------------------------------
# Quiz Attempt Form
# ---------------------------------
class QuizAttemptForm(forms.ModelForm):
    class Meta:
        model = QuizAttempt
        fields = ['quiz', 'student', 'is_mock']
        widgets = {
            'quiz': forms.Select(attrs={
                'class': 'form-control'
            }),
            'student': forms.Select(attrs={
                'class': 'form-control'
            }),
            'is_mock': forms.CheckboxInput(),
        }


# ---------------------------------
# Quiz Answer Form
# ---------------------------------
class QuizAnswerForm(forms.ModelForm):
    class Meta:
        model = QuizAnswer
        fields = '__all__'
        widgets = {
            'attempt': forms.Select(attrs={
                'class': 'form-control'
            }),
            'question': forms.Select(attrs={
                'class': 'form-control'
            }),
            'selected_option': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


# ---------------------------------
# Feedback & Notification Form
# ---------------------------------
class FeedbackAndNotificationForm(forms.ModelForm):
    class Meta:
        model = FeedbackAndNotification
        fields = '__all__'
        widgets = {
            'notification_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Notification ID'
            }),
            'student': forms.Select(attrs={
                'class': 'form-control'
            }),
            'faculty': forms.Select(attrs={
                'class': 'form-control'
            }),
            'summary': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Summary'
            }),
            'send': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Sender'
            }),
            'receive': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Receiver'
            }),
        }
