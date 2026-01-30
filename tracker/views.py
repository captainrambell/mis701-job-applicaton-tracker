from datetime import date

from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ApplicationForm, JobForm
from .models import Application, Job


def dashboard(request):
    status_counts = (
        Application.objects.values("status")
        .annotate(count=Count("id"))
        .order_by("status")
    )

    today = date.today()
    upcoming_applications = (
        Application.objects.filter(next_step_date__gte=today)
        .order_by("next_step_date")
        .select_related("job")
    )

    context = {
        "status_counts": status_counts,
        "upcoming_applications": upcoming_applications,
    }
    return render(request, "tracker/dashboard.html", context)


def job_list(request):
    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()

    jobs = Job.objects.all().order_by("-created_at")

    if search_query:
        jobs = jobs.filter(
            Q(title__icontains=search_query)
            | Q(company__icontains=search_query)
        )

    if status_filter:
        jobs = jobs.filter(applications__status=status_filter).distinct()

    context = {
        "jobs": jobs,
        "search_query": search_query,
        "status_filter": status_filter,
        "status_choices": [choice[0] for choice in Application.STATUS_CHOICES],
    }
    return render(request, "tracker/job_list.html", context)


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    applications = job.applications.all().order_by("-applied_date")
    contacts = job.contacts.all()

    if applications.exists():
        application = applications.first()
    else:
        application = Application(job=job)

    if request.method == "POST":
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            app_obj = form.save(commit=False)
            app_obj.job = job
            app_obj.save()
            messages.success(request, "Application details saved.")
            return redirect(reverse("job_detail", args=[job.pk]))
    else:
        form = ApplicationForm(instance=application)

    context = {
        "job": job,
        "applications": applications,
        "contacts": contacts,
        "form": form,
    }
    return render(request, "tracker/job_detail.html", context)


def job_create(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save()
            messages.success(request, "Job saved successfully.")
            return redirect(reverse("job_detail", args=[job.pk]))
    else:
        form = JobForm()

    context = {
        "form": form,
    }
    return render(request, "tracker/job_form.html", context)


def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk)

    if request.method == "POST":
        job.delete()
        messages.success(request, "Job and related details were deleted.")
        return redirect(reverse("job_list"))

    context = {
        "job": job,
    }
    return render(request, "tracker/job_confirm_delete.html", context)
