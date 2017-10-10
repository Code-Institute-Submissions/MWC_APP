from django import forms

from .models import Jobs

class JobUpdateForm(forms.ModelForm):
    class Meta:
        model = Jobs
        fields = [
        'customer', 'scheduled_date', 'allocated_date', 'completed_date', 'price', 'job_notes', 'job_status', 'payment_status', 'window_cleaner'
        ]

    def clean(self):
        cleaned_data = super(JobUpdateForm, self).clean()
        completed_date = cleaned_data.get("completed_date")
        job_status = cleaned_data.get("job_status")
        payment_status = cleaned_data["payment_status"] #!!brackets because dictionary!!
        window_cleaner = cleaned_data["window_cleaner"]
        allocated_date = cleaned_data["allocated_date"]
        # print '%s - %s' % (completed_date, payment_status)
        if completed_date is None and str(job_status) == 'Completed':
            raise forms.ValidationError(
                        "You are trying to check in a job as completed with no completed date - please enter a completed date"
                    )
        elif payment_status is None and completed_date is not None:
            raise forms.ValidationError(
                        "Please enter a payment status"
                    )
        elif window_cleaner is None and completed_date is not None:
            raise forms.ValidationError(
                        "Please enter a window cleaner"
                    )
        elif completed_date is not None and allocated_date is None:
            raise forms.ValidationError(
                        "Please enter an allocated date"
                    )
        elif completed_date is not None and str(job_status) != 'Completed':
            raise forms.ValidationError(
                        "Job has a completed date but not a 'completed' job status - please correct"
                    )

        else:
            return cleaned_data