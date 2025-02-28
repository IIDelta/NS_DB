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
        "Client", models.DO_NOTHING, db_column="SponsorSerial", blank=True, null=True
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
        db_column="Keyword", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "DeliverablesKeyword"


class TherapeuticAreaKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "TherapeuticAreaKeyword"


class IngredientCategoryKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "IngredientCategoryKeyword"


class ProjectStatusKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "ProjectStatusKeyword"


class ResponsiblePartyKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
    )

    class Meta:
        managed = False
        db_table = "ResponsiblePartyKeyword"


class RouteofAdminKeyword(models.Model):
    keywordid = models.AutoField(db_column="KeywordID", primary_key=True)
    keyword = models.CharField(
        db_column="Keyword", max_length=255, db_collation="SQL_Latin1_General_CP1_CI_AS"
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
