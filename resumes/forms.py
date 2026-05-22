from django import forms
from django.forms import inlineformset_factory
from .models import Resume, Education, Experience, Skill


FORM_CONTROL_CLASS = 'form-control'


class StyledModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{css_class} {FORM_CONTROL_CLASS}'.strip()


class ResumeForm(StyledModelForm):
    class Meta:
        model = Resume
        fields = [
            'template',
            'title',
            'full_name',
            'job_title',
            'email',
            'phone',
            'location',
            'website',
            'photo',
            'summary',
        ]
        labels = {
            'template': 'Шаблон',
            'title': 'Назва резюме',
            'full_name': "Ім'я та прізвище",
            'job_title': 'Посада',
            'email': 'Email',
            'phone': 'Телефон',
            'location': 'Місто',
            'website': 'Сайт або портфоліо',
            'photo': 'Фото',
            'summary': 'Про себе',
        }
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 4}),
        }


class EducationForm(StyledModelForm):
    class Meta:
        model = Education
        fields = ['institution', 'degree', 'start_date', 'end_date', 'description']
        labels = {
            'institution': 'Навчальний заклад',
            'degree': 'Спеціальність або ступінь',
            'start_date': 'Початок',
            'end_date': 'Завершення',
            'description': 'Опис',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ExperienceForm(StyledModelForm):
    class Meta:
        model = Experience
        fields = ['company', 'position', 'start_date', 'end_date', 'description']
        labels = {
            'company': 'Компанія',
            'position': 'Посада',
            'start_date': 'Початок',
            'end_date': 'Завершення',
            'description': "Обов'язки та досягнення",
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class SkillForm(StyledModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'level']
        labels = {
            'name': 'Навичка',
            'level': 'Рівень',
        }


EducationFormSet = inlineformset_factory(
    Resume,
    Education,
    form=EducationForm,
    extra=1,
    can_delete=True,
)

ExperienceFormSet = inlineformset_factory(
    Resume,
    Experience,
    form=ExperienceForm,
    extra=1,
    can_delete=True,
)

SkillFormSet = inlineformset_factory(
    Resume,
    Skill,
    form=SkillForm,
    extra=2,
    can_delete=True,
)
