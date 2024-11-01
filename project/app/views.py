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

        # Query projects with prefetching for related fields
        projects = DeltekProjectID.objects.all().prefetch_related(
            Prefetch("projectdeliverables_set", queryset=ProjectDeliverables.objects.select_related("keywordid")),
            Prefetch("projectstatus_set", queryset=ProjectStatus.objects.select_related("keywordid")),
            Prefetch("projecttherapeuticarea_set", queryset=ProjectTherapeuticArea.objects.select_related("keywordid")),
            Prefetch("projectingredientcategory_set", queryset=ProjectIngredientCategory.objects.select_related("keywordid")),
            Prefetch("projectingredients_set", queryset=ProjectIngredients.objects.all()),
            Prefetch("projectresponsibleparty_set", queryset=ProjectResponsibleParty.objects.select_related("keywordid")),
            Prefetch("projectrouteofadmin_set", queryset=ProjectRouteofAdmin.objects.select_related("keywordid")),
        )

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
            projects = projects.filter(projectingredients__keywordid__icontains=filters["Ingredients"])
        if filters["ResponsibleParty"]:
            projects = projects.filter(projectresponsibleparty__keywordid__keyword__icontains=filters["ResponsibleParty"])
        if filters["RouteOfAdmin"]:
            projects = projects.filter(projectrouteofadmin__keywordid__keyword__icontains=filters["RouteOfAdmin"])



        # Pagination
        paginator = Paginator(projects, 10)  # Show 10 projects per page
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Prepare context with dropdown options for each category
        context = {
            "projects": page_obj,
            "filters": filters,
            "status_keywords": ProjectStatusKeyword.objects.all(),
            "deliverable_keywords": DeliverablesKeyword.objects.all(),
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

    def update_project_status(request):
            if request.method == "POST":
                project_id = request.POST.get("project_id")
                keyword_id = request.POST.get("keyword_id")
                
                try:
                    project = DeltekProjectID.objects.get(pk=project_id)
                    keyword = ProjectStatusKeyword.objects.get(pk=keyword_id)
                    
                    # Update or create the project status entry
                    ProjectStatus.objects.update_or_create(
                        projectid=project, defaults={"keywordid": keyword}
                    )
                    
                    return JsonResponse({"status": "success", "keyword": keyword.keyword})
                
                except Exception as e:
                    return JsonResponse({"status": "error", "message": str(e)})