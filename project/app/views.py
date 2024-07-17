from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.db.models import Prefetch
from .models import (
    DeltekProjectID,
    Client,
    ProjectDeliverables,
    ProjectStatus,
    ProjectTherapeuticArea,
    ProjectIngredientCategory,
    ProjectIngredients,
    ProjectResponsibleParty,
    ProjectRouteOfAdmin,
)


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
        ingredient_category_filter = request.GET.get("IngredientCategories")
        ingredient_filter = request.GET.get("Ingredients")
        responsible_party_filter = request.GET.get("ResponsibleParty")
        route_of_admin_filter = request.GET.get("RouteofAdmin")

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
                queryset=ProjectTherapeuticArea.objects.select_related("keywordid"),
            ),
            Prefetch(
                "projectingredientcategory_set",
                queryset=ProjectIngredientCategory.objects.select_related("keywordid"),
            ),
            Prefetch(
                "projectingredients_set",
            ),
            Prefetch(
                "projectresponsibleparty_set",
                queryset=ProjectResponsibleParty.objects.select_related("keywordid"),
            ),
            Prefetch(
                "projectrouteofadmin_set",
                queryset=ProjectRouteOfAdmin.objects.select_related("keywordid"),
            ),
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
        if ingredient_category_filter:
            projects = projects.filter(
                projectingredientcategory__keywordid__keyword__icontains=ingredient_category_filter
            )
        if ingredient_filter:
            projects = projects.filter(
                projectingredients__keywordid__icontains=ingredient_filter
            )
        if responsible_party_filter:
            projects = projects.filter(
                projectresponsibleparty__keywordid__keyword__icontains=responsible_party_filter
            )
        if route_of_admin_filter:
            projects = projects.filter(
                projectrouteofadmin__keywordid__keyword__icontains=route_of_admin_filter
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
            ingredient_categories = ", ".join(
                [
                    ingredient_category.keywordid.keyword
                    for ingredient_category in project.projectingredientcategory_set.all()
                ]
            )
            ingredients = ", ".join(
                [
                    ingredient.keywordid
                    for ingredient in project.projectingredients_set.all()
                ]
            )
            responsible_party = ", ".join(
                [
                    responsible_party.keywordid.keyword
                    for responsible_party in project.projectresponsibleparty_set.all()
                ]
            )
            route_of_admin = ", ".join(
                [
                    route_of_admin.keywordid.keyword
                    for route_of_admin in project.projectrouteofadmin_set.all()
                ]
            )

            project_list.append(
                {
                    "project": project,
                    "deliverables": deliverables,
                    "status": status,
                    "therapeutic_areas": therapeutic_areas,
                    "ingredient_categories": ingredient_categories,
                    "ingredients": ingredients,
                    "responsible_party": responsible_party,
                    "route_of_admin": route_of_admin,
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
                "IngredientCategories": ingredient_category_filter,
                "Ingredients": ingredient_filter,
                "ResponsibleParty": responsible_party_filter,
                "RouteofAdmin": route_of_admin_filter,
            },
        }

    def get(self, request):
        project_id_filter = request.GET.get("ProjectID")
        project_name_filter = request.GET.get("ProjectName")
        sponsor_name_filter = request.GET.get("SponsorName")
        deliverables_filter = request.GET.get("Deliverables")
        status_filter = request.GET.get("Status")
        therapeutic_area_filter = request.GET.get("TherapeuticAreas")
        ingredient_category_filter = request.GET.get("IngredientCategories")
        ingredient_filter = request.GET.get("Ingredients")
        responsible_party_filter = request.GET.get("ResponsibleParty")
        route_of_admin_filter = request.GET.get("RouteOfAdmin")

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
                queryset=ProjectTherapeuticArea.objects.select_related("keywordid"),
            ),
            Prefetch(
                "projectingredientcategory_set",
                queryset=ProjectIngredientCategory.objects.select_related("keywordid"),
            ),
            Prefetch(
                "projectingredients_set",
                queryset=ProjectIngredients.objects.all(),
            ),
            Prefetch(
                "projectresponsibleparty_set",
                queryset=ProjectResponsibleParty.objects.select_related("keywordid"),
            ),
            Prefetch(
                "projectrouteofadmin_set",
                queryset=ProjectRouteOfAdmin.objects.select_related("keywordid"),
            ),
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
        if ingredient_category_filter:
            projects = projects.filter(
                projectingredientcategory__keywordid__keyword__icontains=ingredient_category_filter
            )
        if ingredient_filter:
            projects = projects.filter(
                projectingredients__keywordid__icontains=ingredient_filter
            )
        if responsible_party_filter:
            projects = projects.filter(
                projectresponsibleparty__keywordid__keyword__icontains=responsible_party_filter
            )
        if route_of_admin_filter:
            projects = projects.filter(
                projectrouteofadmin__keywordid__keyword__icontains=route_of_admin_filter
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
            ingredient_categories = ", ".join(
                [
                    ingredient_categories.keywordid.keyword
                    for ingredient_categories in project.projectingredientcategory_set.all()
                ]
            )
            ingredients = ", ".join(
                [
                    ingredient.keywordid
                    for ingredient in project.projectingredients_set.all()
                ]
            )
            responsible_party = ", ".join(
                [
                    responsible_party.keywordid.keyword
                    for responsible_party in project.projectresponsibleparty_set.all()
                ]
            )
            route_of_admin = ", ".join(
                [
                    route_of_admin.keywordid.keyword
                    for route_of_admin in project.projectrouteofadmin_set.all()
                ]
            )

            project_list.append(
                {
                    "project": project,
                    "deliverables": deliverables,
                    "status": status,
                    "therapeutic_areas": therapeutic_areas,
                    "ingredient_categories": ingredient_categories,
                    "ingredients": ingredients,
                    "responsible_party": responsible_party,
                    "route_of_admin": route_of_admin,
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
                "IngredientCategories": ingredient_category_filter,
                "Ingredients": ingredient_filter,
                "ResponsibleParty": responsible_party_filter,
                "RouteOfAdmin": route_of_admin_filter,
            },
        }

        return render(request, "project_list.html", context)
