from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from django.db.models import Prefetch
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Q  # Add at the top of your file if not already imported
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
    ProjectDemographics, 
    DemographicsKeyword
)
from django.views.decorators.csrf import csrf_exempt
import json

class ProjectListView(View):
    def get(self, request):

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
        projects = projects.order_by('projectid')


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
            Prefetch("projectdemographics_set", queryset=ProjectDemographics.objects.select_related("keywordid")),

        )

        # Process dynamic filters: Group filters by field type.
        filter_groups = {}
        for key, val in request.GET.items():
            if key.startswith('field_'):
                index = key.split('_')[1]
                field_name = val  # e.g., 'ProjectID'
                value_key = f'value_{index}'
                filter_value = request.GET.get(value_key, None)
                if filter_value:
                    filter_groups.setdefault(field_name, []).append(filter_value)

        # Apply each group of filters with OR logic for the same field.
        for field_name, values in filter_groups.items():
            q_obj = Q()
            for v in values:
                if field_name == 'ProjectID':
                    q_obj |= Q(projectid__icontains=v)
                elif field_name == 'ProjectName':
                    q_obj |= Q(projectname__icontains=v)
                elif field_name == 'SponsorName':
                    q_obj |= Q(sponsorserial__sponsorname__icontains=v)
                elif field_name == 'Deliverables':
                    q_obj |= Q(projectdeliverables__keywordid__keyword__icontains=v)
                elif field_name == 'Status':
                    q_obj |= Q(projectstatus__keywordid__keyword__icontains=v)
                elif field_name == 'TherapeuticAreas':
                    q_obj |= Q(projecttherapeuticarea__keywordid__keyword__icontains=v)
                elif field_name == 'IngredientCategories':
                    q_obj |= Q(projectingredientcategory__keywordid__keyword__icontains=v)
                elif field_name == 'Ingredients':
                    q_obj |= Q(projectingredients__keywordid__icontains=v)
                elif field_name == 'ResponsibleParty':
                    q_obj |= Q(projectresponsibleparty__keywordid__keyword__icontains=v)
                elif field_name == 'RouteOfAdmin':
                    q_obj |= Q(projectrouteofadmin__keywordid__keyword__icontains=v)
                elif field_name == 'Demographics':
                    q_obj |= Q(projectdemographics__keywordid__keyword__icontains=v)
            projects = projects.filter(q_obj)

        # *** New code: Clear prefetch cache to force fresh retrieval of updated related data ***
        for project in projects:
            if hasattr(project, '_prefetched_objects_cache'):
                del project._prefetched_objects_cache

        # Get a list of project IDs from the current filtered QuerySet
        project_ids = list(projects.values_list('projectid', flat=True))

        # Manual prefetching: Query each linking table once
        deliverables_map = {}
        for pd in ProjectDeliverables.objects.filter(projectid__in=project_ids).values('projectid', 'keywordid'):
            deliverables_map.setdefault(pd['projectid'], []).append(pd['keywordid'])

        therapeutic_areas_map = {}
        for ta in ProjectTherapeuticArea.objects.filter(projectid__in=project_ids).values('projectid', 'keywordid'):
            therapeutic_areas_map.setdefault(ta['projectid'], []).append(ta['keywordid'])

        ingredient_categories_map = {}
        for ic in ProjectIngredientCategory.objects.filter(projectid__in=project_ids).values('projectid', 'keywordid'):
            ingredient_categories_map.setdefault(ic['projectid'], []).append(ic['keywordid'])

        ingredients_map = {}
        for pi in ProjectIngredients.objects.filter(projectid__in=project_ids).values('projectid', 'keywordid'):
            ingredients_map.setdefault(pi['projectid'], []).append(pi['keywordid'])

        responsible_party_map = {}
        for rp in ProjectResponsibleParty.objects.filter(projectid__in=project_ids).values('projectid', 'keywordid'):
            responsible_party_map.setdefault(rp['projectid'], []).append(rp['keywordid'])

        route_of_admin_map = {}
        for ra in ProjectRouteofAdmin.objects.filter(projectid__in=project_ids).values('projectid', 'keywordid'):
            route_of_admin_map.setdefault(ra['projectid'], []).append(ra['keywordid'])

        demographics_map = {}
        for pdemo in ProjectDemographics.objects.filter(projectid__in=project_ids).values('projectid', 'keywordid'):
            demographics_map.setdefault(pdemo['projectid'], []).append(pdemo['keywordid'])

        # Assign the fresh values to each project
        for project in projects:
            project.selected_deliverable_ids = deliverables_map.get(project.projectid, [])
            project.selected_therapeutic_areas = therapeutic_areas_map.get(project.projectid, [])
            project.selected_ingredient_category_ids = ingredient_categories_map.get(project.projectid, [])
            project.selected_ingredient_values = ingredients_map.get(project.projectid, [])
            project.selected_responsible_party_ids = responsible_party_map.get(project.projectid, [])
            project.selected_route_of_admin_ids = route_of_admin_map.get(project.projectid, [])
            project.selected_demographics_ids = demographics_map.get(project.projectid, [])

        page_size = request.GET.get("page_size", 10)
        if page_size == 'all':
            page_size = projects.count()
        else:
            try:
                page_size = int(page_size)
            except ValueError:
                page_size = 10
        
        # Pagination logic
        paginator = Paginator(projects, page_size)
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
            "demographics_keywords": DemographicsKeyword.objects.all(),  # New line
            "page_size": page_size,  # Pass the selected page size to the template

        }

        # Persist current GET parameters (except 'page') for pagination links
        query_params = request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context['query_string'] = query_params.urlencode()


        return render(request, "project_list.html", context)

 # AJAX endpoint to add a keyword
    @csrf_exempt
    @staticmethod
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
    @csrf_exempt
    @staticmethod
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

            ProjectStatus.objects.update_or_create(
                projectid_id=project_id,
                defaults={'keywordid_id': keyword_id}
            )

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
        with transaction.atomic():
            ProjectDeliverables.objects.filter(projectid=project_id).delete()
            for keyword_id in deliverable_ids:
                ProjectDeliverables.objects.create(
                    projectid_id=project_id, 
                    keywordid_id=keyword_id
                )
        # Return the updated list in the response
        return JsonResponse({"status": "success", "new_deliverable_ids": deliverable_ids})
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


@csrf_exempt
def update_demographics(request):
    if request.method == "POST":
        # For POST requests using standard form-encoded data:
        project_id = request.POST.get("project_id")
        demographics_ids = request.POST.getlist("demographics_ids[]")
        
        # Alternatively, if you send JSON, uncomment this:
        # data = json.loads(request.body)
        # project_id = data.get('project_id')
        # demographics_ids = data.get('demographics_ids')
        
        try:
            # Clear existing demographics for this project
            from .models import ProjectDemographics  # import here if needed
            ProjectDemographics.objects.filter(projectid=project_id).delete()
            
            # Create new entries for each selected keyword
            for keyword_id in demographics_ids:
                ProjectDemographics.objects.create(
                    projectid_id=project_id,  # Using _id to directly assign the FK
                    keywordid_id=keyword_id
                )
            return JsonResponse({"status": "success"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def search_ingredients(request):
    """
    Returns JSON results for Select2 AJAX search.
    Searches for distinct ingredient values in the ProjectIngredients table.
    """
    term = request.GET.get('term', '')
    suggestions = list(
        ProjectIngredients.objects.filter(keywordid__icontains=term)
        .values_list('keywordid', flat=True)
        .distinct()[:10]
    )
    data = {
        'results': [{'id': suggestion, 'text': suggestion} for suggestion in suggestions]
    }
    return JsonResponse(data)
