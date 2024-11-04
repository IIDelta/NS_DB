from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.db.models import Prefetch
from django.http import JsonResponse
from .models import (
    DeltekProjectID,
    ProjectDeliverables,
    ProjectStatus,
    ProjectTherapeuticArea,
    ProjectIngredientCategory,
    ProjectIngredients,
    ProjectResponsibleParty,
    ProjectRouteofAdmin,
    DeliverablesKeyword,
    ProjectStatusKeyword,
    TherapeuticAreaKeyword,
    IngredientCategoryKeyword,
    ResponsiblePartyKeyword,
    RouteofAdminKeyword,
)
from django.views.decorators.csrf import csrf_exempt
import json

class ProjectListView(View):
    def get(self, request):
        # Filter parameters
        filters = {
            "ProjectID": request.GET.get("ProjectID"),
            "ProjectName": request.GET.get("ProjectName"),
            "SponsorName": request.GET.get("SponsorName"),
            "Deliverables": request.GET.get("Deliverables"),
            "Status": request.GET.get("Status"),
            "TherapeuticAreas": request.GET.get("TherapeuticAreas"),
            "IngredientCategories": request.GET.get("IngredientCategories"),
            "Ingredients": request.GET.get("Ingredients"),
            "ResponsibleParty": request.GET.get("ResponsibleParty"),
            "RouteOfAdmin": request.GET.get("RouteOfAdmin"),
        }

        # Query projects with filtering
        projects = DeltekProjectID.objects.all()

        # Apply filters
        if filters["ProjectID"]:
            projects = projects.filter(projectid__icontains=filters["ProjectID"])
        if filters["ProjectName"]:
            projects = projects.filter(projectname__icontains=filters["ProjectName"])
        if filters["SponsorName"]:
            projects = projects.filter(sponsorserial__sponsorname__icontains=filters["SponsorName"])
        if filters["Deliverables"]:
            projects = projects.filter(projectdeliverables__keywordid__keyword__icontains=filters["Deliverables"]).distinct()
        if filters["Status"]:
            projects = projects.filter(projectstatus__keywordid__keyword__icontains=filters["Status"])
        if filters["TherapeuticAreas"]:
            projects = projects.filter(projecttherapeuticarea__keywordid__keyword__icontains=filters["TherapeuticAreas"])
        if filters["IngredientCategories"]:
            projects = projects.filter(projectingredientcategory__keywordid__keyword__icontains=filters["IngredientCategories"])
        if filters["Ingredients"]:
            projects = projects.filter(projectingredients__keywordid__icontains=filters["Ingredients"])  # Adjusted for free text
        if filters["ResponsibleParty"]:
            projects = projects.filter(projectresponsibleparty__keywordid__keyword__icontains=filters["ResponsibleParty"])
        if filters["RouteOfAdmin"]:
            projects = projects.filter(projectrouteofadmin__keywordid__keyword__icontains=filters["RouteOfAdmin"])

        # Query projects with prefetching for related fields (including filters)
        projects = projects.prefetch_related(
            Prefetch("projectdeliverables_set", queryset=ProjectDeliverables.objects.select_related("keywordid")),
            Prefetch("projectstatus_set", queryset=ProjectStatus.objects.select_related("keywordid")),
            Prefetch("projecttherapeuticarea_set", queryset=ProjectTherapeuticArea.objects.select_related("keywordid")),
            Prefetch("projectingredientcategory_set", queryset=ProjectIngredientCategory.objects.select_related("keywordid")),
            Prefetch("projectingredients_set", queryset=ProjectIngredients.objects.all()),  # This line is important
            Prefetch("projectresponsibleparty_set", queryset=ProjectResponsibleParty.objects.select_related("keywordid")),
            Prefetch("projectrouteofadmin_set", queryset=ProjectRouteofAdmin.objects.select_related("keywordid")),
        )


        for project in projects:
            project.selected_deliverable_ids = [
                deliverable.keywordid_id for deliverable in project.projectdeliverables_set.all()
            ]
            project.selected_therapeutic_areas = [
                therapeutic_area.keywordid_id for therapeutic_area in project.projecttherapeuticarea_set.all()
            ]
            project.selected_ingredient_category_ids = [
                ingredient.keywordid_id for ingredient in project.projectingredientcategory_set.all()
            ]
            project.selected_ingredient_values = [
                ingredient.keywordid for ingredient in project.projectingredients_set.all()
            ]
            project.selected_responsible_party_ids = [
                party.keywordid_id for party in project.projectresponsibleparty_set.all()
            ]
            project.selected_route_of_admin_ids = [
                route.keywordid_id for route in project.projectrouteofadmin_set.all()
            ]


        # Pagination
        paginator = Paginator(projects, 10)  # Show 10 projects per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Prepare context with dropdown options for each category
        context = {
            "projects": page_obj,
            "filters": filters,
            "status_keywords": ProjectStatusKeyword.objects.all(),
            "deliverables_keywords": DeliverablesKeyword.objects.all(),  # Deliverable keywords
            "therapeutic_area_keywords": TherapeuticAreaKeyword.objects.all(),
            "ingredient_category_keywords": IngredientCategoryKeyword.objects.all(),
            "responsible_party_keywords": ResponsiblePartyKeyword.objects.all(),
            "route_of_admin_keywords": RouteofAdminKeyword.objects.all(),
        }

        return render(request, "project_list.html", context)

 # AJAX endpoint to add a keyword
    def add_keyword(request):
        if request.method == "POST":
            project_id = request.POST.get("project_id")
            keyword_id = request.POST.get("keyword_id")
            keyword_type = request.POST.get("keyword_type")

            # Determine the keyword type and add the keyword
            try:
                project = DeltekProjectID.objects.get(pk=project_id)
                
                if keyword_type == "deliverable":
                    keyword = DeliverablesKeyword.objects.get(pk=keyword_id)
                    ProjectDeliverables.objects.create(projectid=project, keywordid=keyword)
                
                elif keyword_type == "status":
                    keyword = ProjectStatusKeyword.objects.get(pk=keyword_id)
                    ProjectStatus.objects.update_or_create(projectid=project, keywordid=keyword)
                
                elif keyword_type == "therapeutic_area":
                    keyword = TherapeuticAreaKeyword.objects.get(pk=keyword_id)
                    ProjectTherapeuticArea.objects.create(projectid=project, keywordid=keyword)
                
                elif keyword_type == "ingredient_category":
                    keyword = IngredientCategoryKeyword.objects.get(pk=keyword_id)
                    ProjectIngredientCategory.objects.create(projectid=project, keywordid=keyword)
                
                elif keyword_type == "responsible_party":
                    keyword = ResponsiblePartyKeyword.objects.get(pk=keyword_id)
                    ProjectResponsibleParty.objects.create(projectid=project, keywordid=keyword)
                
                elif keyword_type == "route_of_admin":
                    keyword = RouteofAdminKeyword.objects.get(pk=keyword_id)
                    ProjectRouteofAdmin.objects.create(projectid=project, keywordid=keyword)
                
                return JsonResponse({"status": "success", "keyword": keyword.keyword})
            
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})
    
    # AJAX endpoint to delete a keyword
    def delete_keyword(request):
        if request.method == "POST":
            project_id = request.POST.get("project_id")
            keyword_id = request.POST.get("keyword_id")
            keyword_type = request.POST.get("keyword_type")

            # Determine the keyword type and delete the keyword
            try:
                project = DeltekProjectID.objects.get(pk=project_id)
                
                if keyword_type == "deliverable":
                    ProjectDeliverables.objects.filter(projectid=project, keywordid=keyword_id).delete()
                
                elif keyword_type == "status":
                    ProjectStatus.objects.filter(projectid=project, keywordid=keyword_id).delete()
                
                elif keyword_type == "therapeutic_area":
                    ProjectTherapeuticArea.objects.filter(projectid=project, keywordid=keyword_id).delete()
                
                elif keyword_type == "ingredient_category":
                    ProjectIngredientCategory.objects.filter(projectid=project, keywordid=keyword_id).delete()
                
                elif keyword_type == "responsible_party":
                    ProjectResponsibleParty.objects.filter(projectid=project, keywordid=keyword_id).delete()
                
                elif keyword_type == "route_of_admin":
                    ProjectRouteofAdmin.objects.filter(projectid=project, keywordid=keyword_id).delete()
                
                return JsonResponse({"status": "success", "keyword": keyword_id})
            
            except Exception as e:
                return JsonResponse({"status": "error", "message": str(e)})



@csrf_exempt
def update_project_status(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            project_id = data.get('project_id')
            keyword_id = data.get('keyword_id')

            # Check if project_id and keyword_id are provided
            if not project_id or not keyword_id:
                return JsonResponse({"error": "Missing project_id or keyword_id"}, status=400)

            # Update the project status here (replace with your actual logic)
            project_status = ProjectStatus.objects.get(projectid=project_id)
            project_status.keywordid_id = keyword_id  # or however your foreign key is set up
            project_status.save()

            return JsonResponse({"status": "success", "message": "Status updated successfully"})

        except ProjectStatus.DoesNotExist:
            return JsonResponse({"error": "Project status not found"}, status=404)
        except Exception as e:
            # Log the error if necessary
            print("Error:", e)
            return JsonResponse({"error": "An error occurred"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt
def update_deliverables(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        deliverable_ids = request.POST.getlist("deliverable_ids[]")

        # Clear existing deliverables
        ProjectDeliverables.objects.filter(projectid=project_id).delete()

        # Add selected deliverables
        for keyword_id in deliverable_ids:
            ProjectDeliverables.objects.create(projectid_id=project_id, keywordid_id=keyword_id)

        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Invalid request"}, status=400)


        
@csrf_exempt
def update_therapeutic_areas(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        therapeutic_area_ids = request.POST.getlist("therapeutic_area_ids[]")  # Note: this assumes you're passing an array of therapeutic area IDs

        # Clear existing therapeutic areas for this project
        ProjectTherapeuticArea.objects.filter(projectid=project_id).delete()

        # Add the new set of therapeutic areas
        for keyword_id in therapeutic_area_ids:
            ProjectTherapeuticArea.objects.create(projectid_id=project_id, keywordid_id=keyword_id)

        return JsonResponse({"status": "success"})

@csrf_exempt
def update_ingredient_categories(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        ingredient_category_ids = request.POST.getlist("ingredient_category_ids[]")

        # Clear existing ingredient categories
        ProjectIngredientCategory.objects.filter(projectid=project_id).delete()

        # Add selected ingredient categories
        for keyword_id in ingredient_category_ids:
            ProjectIngredientCategory.objects.create(projectid_id=project_id, keywordid_id=keyword_id)

        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def update_responsible_parties(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        responsible_party_ids = request.POST.getlist("responsible_party_ids[]")

        # Clear existing responsible parties
        ProjectResponsibleParty.objects.filter(projectid=project_id).delete()

        # Add selected responsible parties
        for keyword_id in responsible_party_ids:
            ProjectResponsibleParty.objects.create(projectid_id=project_id, keywordid_id=keyword_id)

        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def update_route_of_admin(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        route_of_admin_ids = request.POST.getlist("route_of_admin_ids[]")

        # Clear existing route of admin entries
        ProjectRouteofAdmin.objects.filter(projectid=project_id).delete()

        # Add selected route of admin entries
        for keyword_id in route_of_admin_ids:
            ProjectRouteofAdmin.objects.create(projectid_id=project_id, keywordid_id=keyword_id)

        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def update_ingredients(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        ingredients = request.POST.getlist("ingredients[]")  # List of free-text ingredients

        # Clear existing ingredients for the project
        ProjectIngredients.objects.filter(projectid=project_id).delete()

        # Add new ingredients (keywordid field will store free-text values here)
        for ingredient in ingredients:
            ProjectIngredients.objects.create(projectid_id=project_id, keywordid=ingredient)

        return JsonResponse({"status": "success"})
    return JsonResponse({"error": "Invalid request"}, status=400)

