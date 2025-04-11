from django.db import models


# Primary model for projects
class DeltekProjectID(models.Model):
    projectid = models.CharField(
        db_column="ProjectID",
        primary_key=True,
        max_length=20,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )
    projectname = models.CharField(
        db_column="ProjectName",
        max_length=40,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )
    sponsorserial = models.ForeignKey(
        "Client", models.DO_NOTHING,
        db_column="SponsorSerial", blank=True, null=True
    )

    @property
    def sponsorname(self):
        return self.sponsorserial.sponsorname if self.sponsorserial else ""

    class Meta:
        managed = False
        db_table = "DeltekProjectID"


class Client(models.Model):
    sponsorserial = models.CharField(
        db_column="SponsorSerial",
        primary_key=True,
        max_length=32,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )
    sponsorname = models.CharField(
        db_column="SponsorName",
        max_length=100,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "Client"


# Keywords Models
class DeliverablesKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "DeliverablesKeyword"


class TherapeuticAreaKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "TherapeuticAreaKeyword"


class IngredientCategoryKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "IngredientCategoryKeyword"


class ProjectStatusKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "ProjectStatusKeyword"


class ResponsiblePartyKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "ResponsiblePartyKeyword"


class RouteofAdminKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "RouteofAdminKeyword"


# Project Keyword Link Models with Composite Keys
class ProjectDeliverables(models.Model):
    entry_id = models.AutoField(primary_key=True)  # Explicit primary key field
    projectid = models.ForeignKey(
        DeltekProjectID, models.DO_NOTHING, db_column="ProjectID"
    )
    keywordid = models.ForeignKey(
        DeliverablesKeyword, models.DO_NOTHING, db_column="KeywordID"
    )

    class Meta:
        managed = False
        db_table = "ProjectDeliverables"
        unique_together = (("projectid", "keywordid"),)


class ProjectIngredients(models.Model):
    entry_id = models.AutoField(primary_key=True)  # Explicit primary key field
    projectid = models.ForeignKey(
        DeltekProjectID, models.DO_NOTHING, db_column="ProjectID"
    )
    keywordid = models.CharField(
        db_column="KeywordID",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )

    class Meta:
        managed = False
        db_table = "ProjectIngredients"
        unique_together = (("projectid", "keywordid"),)


class ProjectTherapeuticArea(models.Model):
    entry_id = models.AutoField(primary_key=True)  # Explicit primary key field
    projectid = models.ForeignKey(
        DeltekProjectID, models.DO_NOTHING, db_column="ProjectID"
    )
    keywordid = models.ForeignKey(
        TherapeuticAreaKeyword, models.DO_NOTHING, db_column="KeywordID"
    )

    class Meta:
        managed = False
        db_table = "ProjectTherapeuticArea"
        unique_together = (("projectid", "keywordid"),)


class ProjectIngredientCategory(models.Model):
    entry_id = models.AutoField(primary_key=True)  # Explicit primary key field
    projectid = models.ForeignKey(
        DeltekProjectID, models.DO_NOTHING, db_column="ProjectID"
    )
    keywordid = models.ForeignKey(
        IngredientCategoryKeyword, models.DO_NOTHING, db_column="KeywordID"
    )

    class Meta:
        managed = False
        db_table = "ProjectIngredientCategory"
        unique_together = (("projectid", "keywordid"),)


class ProjectStatus(models.Model):
    entry_id = models.AutoField(primary_key=True)  # Explicit primary key field
    projectid = models.ForeignKey(
        DeltekProjectID, models.DO_NOTHING, db_column="ProjectID"
    )
    keywordid = models.ForeignKey(
        ProjectStatusKeyword, models.DO_NOTHING, db_column="KeywordID"
    )

    class Meta:
        managed = False
        db_table = "ProjectStatus"
        unique_together = (("projectid", "keywordid"),)


class ProjectResponsibleParty(models.Model):
    entry_id = models.AutoField(primary_key=True)  # Explicit primary key field
    projectid = models.ForeignKey(
        DeltekProjectID, models.DO_NOTHING, db_column="ProjectID"
    )
    keywordid = models.ForeignKey(
        ResponsiblePartyKeyword, models.DO_NOTHING, db_column="KeywordID"
    )

    class Meta:
        managed = False
        db_table = "ProjectResponsibleParty"
        unique_together = (("projectid", "keywordid"),)


class ProjectRouteofAdmin(models.Model):
    entry_id = models.AutoField(primary_key=True)  # Explicit primary key field
    projectid = models.ForeignKey(
        DeltekProjectID, models.DO_NOTHING, db_column="ProjectID"
    )
    keywordid = models.ForeignKey(
        RouteofAdminKeyword, models.DO_NOTHING, db_column="KeywordID"
    )

    class Meta:
        managed = False
        db_table = "ProjectRouteofAdmin"
        unique_together = (("projectid", "keywordid"),)


# New Keyword Model for Demographics
class DemographicsKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword",
        max_length=255,
        db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False  # Django will manage this table
        db_table = "DemographicsKeyword"


class ProjectDemographics(models.Model):
    entry_id = models.AutoField(primary_key=True)
    projectid = models.ForeignKey(
        DeltekProjectID,
        models.DO_NOTHING,
        db_column="ProjectID",
        to_field="projectid"
    )
    keywordid = models.ForeignKey(
        DemographicsKeyword, models.DO_NOTHING, db_column="KeywordID"
    )

    class Meta:
        managed = False
        db_table = "ProjectDemographics"
        unique_together = (("projectid", "keywordid"),)


# Questionnaire models
class QuestionnairesKeyword(models.Model):
    """Stores the distinct questionnaire values."""
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword",
        max_length=255,
        # Adjust length as needed
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        unique=True
        # Ensure questionnaire text is unique if desired
    )

    class Meta:
        managed = True
        # Django will manage this table
        db_table = "QuestionnairesKeyword"

    def __str__(self):
        return self.keyword


class ProjectQuestionnaires(models.Model):
    """Links Projects to Questionnaires."""
    entry_id = models.AutoField(primary_key=True)
    projectid = models.ForeignKey(
        DeltekProjectID,
        models.CASCADE,
        # Or models.PROTECT, etc. depending on desired behavior
        db_column="ProjectID",
        to_field="projectid"
    )
    # Storing as free text similar to Ingredients
    questionnaire_text = models.CharField(
        db_column="QuestionnaireText",
        max_length=500,
        # Adjust max length as needed
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )

    class Meta:
        managed = True
        db_table = "ProjectQuestionnaires"
        unique_together = (("projectid", "questionnaire_text"),)
        # Ensure a project doesn't have the same text twice

    def __str__(self):
        return f"{self.projectid.projectid} - {self.questionnaire_text}"
