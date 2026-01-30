from django import forms

from .models import Job, Application


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "company", "source", "url", "location", "salary_range"]


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["status", "applied_date", "next_step_date", "notes"]

