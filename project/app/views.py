# app/views.py
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.db.models import Prefetch
from .models import DeltekProjectID, Client, ProjectDeliverables, ProjectStatus, ProjectTherapeuticArea


class ClientListView(View):
    def get(self, request):
        clients = Client.objects.all()
        return render(request, "client_list.html", {"clients": clients})


class ProjectListView(View):
    def get(self, request):
        project_id_filter = request.GET.get("ProjectID")
        project_name_filter = request.GET.get("ProjectName")
        sponsor_name_filter = request.GET.get("SponsorName")
        deliverables_filter = request.GET.get("Deliverables")
        status_filter = request.GET.get("Status")
        therapeutic_area_filter = request.GET.get("TherapeuticAreas")

        projects = DeltekProjectID.objects.all().prefetch_related(
            Prefetch(
                "projectdeliverables_set",
                queryset=ProjectDeliverables.objects.select_related("keywordid"),
            ),
            Prefetch(
                "projectstatus_set",
                queryset=ProjectStatus.objects.select_related("keywordid"),
            ),
            Prefetch(
                "projecttherapeuticarea_set",
                queryset=ProjectTherapeuticArea.objects.select_related("keywordid")
            )
        )

        if project_id_filter:
            projects = projects.filter(projectid__icontains=project_id_filter)
        if project_name_filter:
            projects = projects.filter(projectname__icontains=project_name_filter)
        if sponsor_name_filter:
            projects = projects.filter(
                sponsorserial__sponsorname__icontains=sponsor_name_filter
            )
        if deliverables_filter:
            projects = projects.filter(
                projectdeliverables__keywordid__keyword__icontains=deliverables_filter
            ).distinct()
        if status_filter:
            projects = projects.filter(
                projectstatus__keywordid__keyword__icontains=status_filter
            )
        if therapeutic_area_filter:
            projects = projects.filter(
                projecttherapeuticarea__keywordid__keyword__icontains=therapeutic_area_filter
            )

        project_list = []
        for project in projects:
            deliverables = ", ".join(
                [
                    deliverable.keywordid.keyword
                    for deliverable in project.projectdeliverables_set.all()
                ]
            )
            therapeutic_areas = ", ".join(
                [
                    therapeuticarea.keywordid.keyword
                    for therapeuticarea in project.projecttherapeuticarea_set.all()
                ]
            )
            status = ", ".join(
                [status.keywordid.keyword for status in project.projectstatus_set.all()]
            )
            project_list.append(
                {
                    "project": project,
                    "deliverables": deliverables,
                    "status": status,
                    "therapeutic_areas": therapeutic_areas,
                }
            )

        paginator = Paginator(project_list, 50)  # Show 50 projects per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "projects": page_obj,
            "filters": {
                "ProjectID": project_id_filter,
                "ProjectName": project_name_filter,
                "SponsorName": sponsor_name_filter,
                "Deliverables": deliverables_filter,
                "TherapeuticAreas": therapeutic_area_filter,
                "Status": status_filter,
            },
        }

        return render(request, "project_list.html", context)
