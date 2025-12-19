from django import forms 
from . models import questions,faculty_registration,question_bank,student_registration,quiz,admin_registration,department,feedback_and_notification
class faculty_RegistrationForm(forms.ModelForm):
    class Meta:
        model=faculty_registration
        fields='__all__'
        widgets = {
            'faculty_id': forms.TextInput(attrs={
                "placeholder": "Enter your id",
                "class": "form-control",
            }),#customized text input
            'password': forms.PasswordInput(attrs={
                "placeholder": "Enter password",
                "class": "form-control",
            }),
            'department_name': forms.TextInput(attrs={
                "placeholder": "Enter department name",
                "class": "form-control",
            }),#customized text input
            'faculty_name': forms.TextInput(attrs={
                "placeholder": "Enter faculty name",
                "class": "form-control",
            }),#customized text input
            
        }
class departmentForm (forms.ModelForm):
    class Meta:
        model=department
        fields='__all__'
        widgets = {
            'department_name': forms.TextInput(attrs={
                "placeholder": "Enter department name",
                "class": "form-control",
            })
            
        }

class question_bankForm (forms.ModelForm):
    class Meta:
        model=question_bank
        fields='__all__'
        
class student_registrationForm (forms.ModelForm):
    class Meta:
        model=student_registration
        fields='__all__'
        widgets ={
            'roll_no': forms.TextInput(attrs={
                "placeholder": "Enter your roll no",
                "class": "form-control",
            }),#customized text input
            'password': forms.PasswordInput(attrs={
                "placeholder": "Enter password",
                "class": "form-control",
            }),
            'student_name': forms.TextInput(attrs={
                "placeholder": "Enter student name",
                "class": "form-control",
            }),#customized text input
            'department_name': forms.TextInput(attrs={
                "placeholder": "Enter department name",
                "class": "form-control",
            }),#customized text input
             'year': forms.NumberInput(attrs={
                "placeholder": "Enter year",
                "class": "form-control",
            }),
            'email_id': forms.EmailInput(attrs={
                "placeholder": "Enter email id",
                "class": "form-control",
            }),#customized email input


            
        }

class quizForm(forms.ModelForm):

    CORRECT_OPTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    correct_option = forms.ChoiceField(
        choices=CORRECT_OPTION_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )

    Difficulty_Level = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )

    class Meta:
        model = quiz
        fields = '__all__'
        widgets = {
            'quiz_id': forms.TextInput(attrs={
                "placeholder": "Enter quiz id",
                "class": "form-control",
            }),
            'question_id': forms.TextInput(attrs={
                "placeholder": "Enter question id",
                "class": "form-control",
            }),
            'option_A': forms.TextInput(attrs={
                "placeholder": "Enter option",
                "class": "form-control",
            }),
            'option_B': forms.TextInput(attrs={
                "placeholder": "Enter option",
                "class": "form-control",
            }),
            'option_C': forms.TextInput(attrs={
                "placeholder": "Enter option",
                "class": "form-control",
            }),
            'option_D': forms.TextInput(attrs={
                "placeholder": "Enter option",
                "class": "form-control",
            }),
        }


class quizquestionForm(forms.ModelForm):
    class Meta:
        model=question_bank
        fields='__all__'
        widgets = {
            'course_name': forms.TextInput(attrs={
                "placeholder": "Enter course name",
                "class": "form-control",
            }),#customized text input
            'year': forms.NumberInput(attrs={
                "placeholder": "Enter year",
                "class": "form-control",
            }),
            'subject': forms.TextInput(attrs={
                "placeholder": "Enter subject",
                "class": "form-control",
            }),
        }
class admin_registrationForm(forms.ModelForm):
    class Meta:
        model=admin_registration
        fields='__all__'
        widgets ={
        'user_id': forms.TextInput(attrs={
                "placeholder": "Enter user id",
                "class": "form-control",
            }),#customized text input
            'password': forms.PasswordInput(attrs={
                "placeholder": "Enter password",
                "class": "form-control",
            }),
            
        
            'email_id': forms.EmailInput(attrs={
                "placeholder": "Enter email id",
                "class": "form-control",
            }),#customized email input
            'phone_no': forms.NumberInput(attrs={
                "placeholder": "Enter phone no",
                "class": "form-control",
            }),



            
        }



class questionsForm(forms.ModelForm):
    class Meta:
        model=questions
        fields=['subject_id','semester','questionupload','subject_k']
        widgets = {
            'subject_id': forms.TextInput(attrs={
                "placeholder": "Enter subject id",
                "class": "form-control",
            }),#customized text input
            'semester': forms.NumberInput(attrs={
                "placeholder": "Enter semester",
                "class": "form-control",
            }),
            # 'subject_k': forms.TextInput(attrs={
            #     "placeholder": "Enter subject",
            #     "class": "form-control",
            # }),
            
        }

class feedbackForm(forms.ModelForm):
    class Meta:
        model=feedback_and_notification
        fields=['roll_no','faculty_id','summary','notification_id','send','receive']
        widgets = {
            # 'roll_no': forms.TextInput(attrs={
            #     "placeholder": "Enter roll no",
            #     "class": "form-control",
            # }),#customized text input
            # # 'faculty_id': forms.TextInput(attrs={
            #     "placeholder": "Enter your id",
            #     "class": "form-control",
            # }),
            'summary': forms.TextInput(attrs={
                "placeholder": "Enter summary",
                "class": "form-control",
            }),
            'notification_id': forms.TextInput(attrs={
                "placeholder": "Enter notification id",
                "class": "form-control",
            }),
             'send': forms.TextInput(attrs={
                "placeholder": "Enter sender",
                "class": "form-control",
            }),
            'receive': forms.TextInput(attrs={
                "placeholder": "Enter receiver",
                "class": "form-control",
            }),
            
            
        }
from django import forms
from .models import question_bank

class PYQFilterForm(forms.Form):
    semester = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Semester"
        })
    )

    subject = forms.ModelChoiceField(
        queryset=question_bank.objects.all(),
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )
