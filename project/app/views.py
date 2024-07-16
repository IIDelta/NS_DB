# app/views.py
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import DeltekProjectID, Client
from .forms import ProjectForm


class ClientListView(View):
    def get(self, request):
        clients = Client.objects.all()
        return render(request, "client_list.html", {"clients": clients})


class ProjectListView(View):
    template_name = "project_list.html"
    paginate_by = 10  # Number of items per page

    def get(self, request):
        form = ProjectForm(request.GET)
        project_list = DeltekProjectID.objects.all()

        if form.is_valid():
            projectid = form.cleaned_data.get("projectid")
            projectname = form.cleaned_data.get("projectname")
            sponsorname = form.cleaned_data.get("sponsorname")

            if projectid:
                project_list = project_list.filter(projectid__icontains=projectid)
            if projectname:
                project_list = project_list.filter(projectname__icontains=projectname)
            if sponsorname:
                project_list = project_list.filter(
                    sponsorserial__sponsorname__icontains=sponsorname
                )

        paginator = Paginator(project_list, self.paginate_by)
        page = request.GET.get("page", 1)

        try:
            projects = paginator.page(page)
        except PageNotAnInteger:
            projects = paginator.page(1)
        except EmptyPage:
            projects = paginator.page(paginator.num_pages)

        return render(request, self.template_name, {"projects": projects, "form": form})


class ProjectDetailView(View):
    def get(self, request, pk):
        project = get_object_or_404(DeltekProjectID, pk=pk)
        return render(request, "project_detail.html", {"project": project})


class ProjectCreateView(View):
    def get(self, request):
        form = ProjectForm()
        return render(request, "project_form.html", {"form": form})

    def post(self, request):
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("project-list")
        return render(request, "project_form.html", {"form": form})


class ProjectUpdateView(View):
    def get(self, request, pk):
        project = get_object_or_404(DeltekProjectID, pk=pk)
        form = ProjectForm(instance=project)
        return render(request, "project_form.html", {"form": form})

    def post(self, request, pk):
        project = get_object_or_404(DeltekProjectID, pk=pk)
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("project-list")
        return render(request, "project_form.html", {"form": form})


class ProjectDeleteView(View):
    def get(self, request, pk):
        project = get_object_or_404(DeltekProjectID, pk=pk)
        return render(request, "project_confirm_delete.html", {"project": project})

    def post(self, request, pk):
        project = get_object_or_404(DeltekProjectID, pk=pk)
        project.delete()
        return redirect("project-list")
