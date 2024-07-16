# models.py
from django.db import models


class Client(models.Model):
    sponsorserial = models.CharField(
        db_column="SponsorSerial",
        primary_key=True,
        max_length=32,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )  # Field name made lowercase.
    sponsorname = models.CharField(
        db_column="SponsorName",
        max_length=100,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "Client"


class DeliverablesKeyword(models.Model):
    keywordid = models.AutoField(
        db_column="KeywordID", primary_key=True
    )  # Field name made lowercase.
    keyword = models.CharField(
        db_column="Keyword", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "DeliverablesKeyword"


class DeltekProjectID(models.Model):
    projectid = models.CharField(
        db_column="ProjectID",
        primary_key=True,
        max_length=20,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )  # Field name made lowercase.
    projectname = models.CharField(
        db_column="ProjectName",
        max_length=40,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    sponsorserial = models.ForeignKey(
        Client, models.DO_NOTHING, db_column="SponsorSerial", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "DeltekProjectID"


class ProjectDeliverables(models.Model):
    projectid = models.ForeignKey(
        DeltekProjectID, models.DO_NOTHING, db_column="ProjectID", primary_key=True
    )  # Field name made lowercase.
    keywordid = models.ForeignKey(
        DeliverablesKeyword, models.DO_NOTHING, db_column="KeywordID"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "ProjectDeliverables"
        unique_together = (("projectid", "keywordid"),)


class IngredientCategoryKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "IngredientCategoryKeyword"


class ProjectIngredientCategory(models.Model):
    projectid = models.OneToOneField(
        DeltekProjectID, models.DO_NOTHING, db_column="ProjectID", primary_key=True
    )
    keywordid = models.ForeignKey(
        IngredientCategoryKeyword, models.DO_NOTHING, db_column="KeywordID"
    )

    class Meta:
        managed = False
        db_table = "ProjectIngredientCategory"
        unique_together = (("projectid", "keywordid"),)


class ProjectIngredients(models.Model):
    projectid = models.OneToOneField(
        DeltekProjectID, models.DO_NOTHING, db_column="ProjectID", primary_key=True
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


class ProjectQuestionnaires(models.Model):
    projectid = models.OneToOneField(
        DeltekProjectID, models.DO_NOTHING, db_column="ProjectID", primary_key=True
    )
    keywordid = models.ForeignKey(
        "QuestionnairesKeywords", models.DO_NOTHING, db_column="KeywordID"
    )

    class Meta:
        managed = False
        db_table = "ProjectQuestionnaires"
        unique_together = (("projectid", "keywordid"),)


class ProjectResponsibleParty(models.Model):
    projectid = models.OneToOneField(
        DeltekProjectID, models.DO_NOTHING, db_column="ProjectID", primary_key=True
    )
    keywordid = models.ForeignKey(
        "ResponsiblePartyKeyword", models.DO_NOTHING, db_column="KeywordID"
    )

    class Meta:
        managed = False
        db_table = "ProjectResponsibleParty"
        unique_together = (("projectid", "keywordid"),)


class ProjectRouteOfAdmin(models.Model):
    projectid = models.OneToOneField(
        DeltekProjectID, models.DO_NOTHING, db_column="ProjectID", primary_key=True
    )
    keywordid = models.ForeignKey(
        "RouteOfAdminKeyword", models.DO_NOTHING, db_column="KeywordID"
    )

    class Meta:
        managed = False
        db_table = "ProjectRouteOfAdmin"
        unique_together = (("projectid", "keywordid"),)


class ProjectStatusKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "ProjectStatusKeyword"


class ProjectStatus(models.Model):
    projectid = models.ForeignKey(
        "DeltekProjectID", models.DO_NOTHING, db_column="ProjectID", primary_key=True
    )
    keywordid = models.ForeignKey(
        ProjectStatusKeyword, models.DO_NOTHING, db_column="KeywordID"
    )

    class Meta:
        managed = False
        db_table = "ProjectStatus"
        unique_together = (("projectid", "keywordid"),)



class QuestionnairesKeywords(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "QuestionnairesKeywords"


class ResponsiblePartyKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "ResponsiblePartyKeyword"


class RouteOfAdminKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "RouteOfAdminKeyword"

class ProjectTherapeuticArea(models.Model):
    projectid = models.ForeignKey(
    DeltekProjectID, models.DO_NOTHING, db_column="ProjectID", primary_key=True
    )  # Field name made lowercase.
    keywordid = models.ForeignKey(
        "TherapeuticAreaKeyword", models.DO_NOTHING, db_column="KeywordID"
    )

    class Meta:
        managed = False
        db_table = "ProjectTherapeuticArea"
        unique_together = (("projectid", "keywordid"),)


class TherapeuticAreaKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "TherapeuticAreaKeyword"


class EFMigrationsHistory(models.Model):
    migrationid = models.CharField(
        db_column="MigrationId",
        primary_key=True,
        max_length=150,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )
    productversion = models.CharField(
        db_column="ProductVersion",
        max_length=32,
        db_collation="SQL_Latin1_General_CP1_CI_AS",
    )

    class Meta:
        managed = False
        db_table = "__EFMigrationsHistory"


class SysDiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation="SQL_Latin1_General_CP1_CI_AS")
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "sysdiagrams"
        unique_together = (("principal_id", "name"),)
