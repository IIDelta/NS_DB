from django.contrib import admin
from .models import (
    DeltekProjectID,
    ProjectDeliverables,
    ProjectStatus,
    ProjectTherapeuticArea,
    ProjectIngredientCategory,
    ProjectIngredients,        # Ensure this matches exactly
    ProjectResponsibleParty,
    ProjectRouteofAdmin,        # Correctly spelled as ProjectRouteofAdmin
)


admin.site.register(DeltekProjectID)
admin.site.register(ProjectIngredients)
admin.site.register(ProjectDeliverables)
admin.site.register(ProjectStatus)
admin.site.register(ProjectTherapeuticArea)
admin.site.register(ProjectIngredientCategory)
admin.site.register(ProjectResponsibleParty)
admin.site.register(ProjectRouteofAdmin)
