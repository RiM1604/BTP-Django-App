from django import forms

class IngestLogForm(forms.Form):
    timestamp = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text="Select date and time"
    )
    service_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    log_content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

class QueryLogsForm(forms.Form):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text="Start date and time"
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text="End date and time"
    )
    service_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )