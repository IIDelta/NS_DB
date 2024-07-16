from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views import View
from .models import (
    Project,
    ProjectStatus,
    ProjectResponsibleParty,
    ProjectDeliverables,
    ProjectTherapeuticArea,
    ProjectIngredientCategory,
    ProjectIngredients,
    Client,
)


class ClientListView(View):
    def get(self, request):
        clients = Client.objects.all()
        return render(request, "client_list.html", {"clients": clients})


class ProjectListView(View):
    def get(self, request):
        projects = Project.objects.all()
        project_id = request.GET.get("project_id")
        project_name = request.GET.get("project_name")
        sponsor_name = request.GET.get("sponsor_name")

        if project_id:
            projects = projects.filter(projectid__icontains=project_id)
        if project_name:
            projects = projects.filter(projectname__icontains=project_name)
        if sponsor_name:
            projects = projects.filter(sponsorname__icontains=sponsor_name)

        return render(request, "project_list.html", {"projects": projects})


class ProjectDetailView(View):
    def get(self, request, pk):
        project = get_object_or_404(Project, pk=pk)
        project_status = ProjectStatus.objects.filter(projectid=project)
        responsible_party = ProjectResponsibleParty.objects.filter(projectid=project)
        deliverables = ProjectDeliverables.objects.filter(projectid=project)
        therapeutic_areas = ProjectTherapeuticArea.objects.filter(projectid=project)
        ingredient_categories = ProjectIngredientCategory.objects.filter(
            projectid=project
        )
        ingredients = ProjectIngredients.objects.filter(projectid=project)

        context = {
            "project": project,
            "project_status": project_status,
            "responsible_party": responsible_party,
            "deliverables": deliverables,
            "therapeutic_areas": therapeutic_areas,
            "ingredient_categories": ingredient_categories,
            "ingredients": ingredients,
        }
        return render(request, "project_detail.html", context)


class ProjectCreateView(CreateView):
    model = Project
    fields = ["projectid", "projectname", "sponsorname"]
    template_name = "project_form.html"
    success_url = reverse_lazy("project-list")


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ["projectid", "projectname", "sponsorname"]
    template_name = "project_form.html"
    success_url = reverse_lazy("project-list")


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "project_confirm_delete.html"
    success_url = reverse_lazy("project-list")
