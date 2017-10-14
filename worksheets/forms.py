from django import forms

from .models import Job


class JobUpdateForm(forms.ModelForm):
    """ needs special validation so cannot use generic CBV form """

    class Meta:
        model = Job
        fields = [
            'customer',
            'scheduled_date',
            'allocated_date',
            'completed_date',
            'price',
            'job_notes',
            'job_status',
            'payment_status',
            'window_cleaner']

    def clean(self):
        cleaned_data = super(JobUpdateForm, self).clean()
        scheduled_date = cleaned_data.get("scheduled_date")
        completed_date = cleaned_data.get("completed_date")
        job_status = cleaned_data.get("job_status")
        # !!brackets because dictionary!!
        payment_status = cleaned_data.get("payment_status")
        window_cleaner = cleaned_data["window_cleaner"]
        allocated_date = cleaned_data.get("allocated_date")
        if (completed_date is None and
                str(job_status) == 'Completed'):
                raise forms.ValidationError(
                    "You are trying to check in a job as completed with no "
                    "completed date - please enter a completed date"
                )
        elif (payment_status is None and
                completed_date is not None):
                raise forms.ValidationError(
                    "Please enter a payment status"
                )
        elif (window_cleaner is None and
                completed_date is not None):
                raise forms.ValidationError(
                    "Please enter a window cleaner"
                )
        elif (completed_date is not None and
                allocated_date is None):
                raise forms.ValidationError(
                    "Please enter an allocated date"
                )
        elif (completed_date is not None and
                str(job_status) != 'Completed'):
                raise forms.ValidationError(
                    "Job has a completed date but not a 'completed' "
                    "job status - please correct"
                )
        elif (str(job_status) == 'Due' and
                str(payment_status) == 'Paid'):
                raise forms.ValidationError(
                    "Job has 'Due' status but is set as paid - please correct"
                )
        elif (str(job_status) == 'Booked' and
                str(payment_status) == 'Paid'):
                raise forms.ValidationError(
                    "Job has 'Booked' status but is "
                    "set as paid - please correct"
                )
        elif (scheduled_date is None):
                raise forms.ValidationError(
                    "Please enter a due date"
                )
        # keep this order:
        elif (str(job_status) == 'Booked' and
                window_cleaner is None and
                allocated_date is None):
                raise forms.ValidationError(
                    "Job is booked - please enter a window "
                    "cleaner and an allocated date"
                )
        elif (str(job_status) == 'Booked' and
                allocated_date is None):
                raise forms.ValidationError(
                    "Job is booked - please enter an allocated date"
                )
        elif (str(job_status) == 'Booked' and
                window_cleaner is None):
                raise forms.ValidationError(
                    "Job is booked - please enter a window cleaner"
                )
        else:
            return cleaned_data
