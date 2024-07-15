from django.contrib import admin
from .models import Client, DeliverablesKeyword, DeltekProjectID, IngredientCategoryKeyword, ProjectDeliverables, ProjectIngredientCategory, ProjectIngredients, ProjectQuestionnaires, ProjectResponsibleParty, ProjectRouteOfAdmin, ProjectStatus, ProjectTherapeuticArea

admin.site.register(Client)
admin.site.register(DeliverablesKeyword)
admin.site.register(DeltekProjectID)
admin.site.register(IngredientCategoryKeyword)
admin.site.register(ProjectDeliverables)
admin.site.register(ProjectIngredientCategory)
admin.site.register(ProjectIngredients)
admin.site.register(ProjectQuestionnaires)
admin.site.register(ProjectResponsibleParty)
admin.site.register(ProjectRouteOfAdmin)
admin.site.register(ProjectStatus)
admin.site.register(ProjectTherapeuticArea)
