# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from custom_user.models import AbstractEmailUser


class Admin(models.Model):
    admin_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'admin'


class AnalysisResult(models.Model):
    fn = models.FloatField(db_column='FN')  # Field name made lowercase.
    fp = models.FloatField(db_column='FP')  # Field name made lowercase.
    tn = models.FloatField(db_column='TN')  # Field name made lowercase.
    tp = models.FloatField(db_column='TP')  # Field name made lowercase.
    analysisresult_path = models.CharField(db_column='analysisResult_path', max_length=255, blank=True,
                                           null=True)  # Field name made lowercase.
    detectionresult_path = models.CharField(db_column='detectionResult_path', max_length=255, blank=True,
                                            null=True)  # Field name made lowercase.
    execution_status = models.CharField(max_length=255)
    targetcode = models.ForeignKey('TagetCode', models.DO_NOTHING,
                                   db_column='targetCode_id')  # Field name made lowercase.
    request = models.ForeignKey('Request', models.DO_NOTHING, primary_key=True)

    class Meta:
        # managed = False
        db_table = 'analysis_result'
        unique_together = (('request', 'targetcode'),)


class DetectionAlgorithm(models.Model):
    algorithm_id = models.AutoField(primary_key=True)
    jar_path = models.CharField(max_length=255, blank=True, null=True)
    main_jarfile = models.CharField(db_column='main_jarFile', max_length=255)  # Field name made lowercase.
    src_path = models.CharField(max_length=255, blank=True, null=True)
    request = models.ForeignKey('Request', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'detection_algorithm'


class FinalResult(models.Model):
    result_id = models.AutoField(primary_key=True)
    fn_avg = models.FloatField(db_column='FN_avg')  # Field name made lowercase.
    fp_avg = models.FloatField(db_column='FP_avg')  # Field name made lowercase.
    tn_avg = models.FloatField(db_column='TN_avg')  # Field name made lowercase.
    tp_avg = models.FloatField(db_column='TP_avg')  # Field name made lowercase.
    execution_times = models.IntegerField()
    rank = models.IntegerField()
    request = models.ForeignKey('Request', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'final_result'


class Request(models.Model):
    request_id = models.AutoField(primary_key=True, max_length=255)
    request_date = models.DateField(blank=True, null=True)
    request_exe_status = models.CharField(max_length=50)
    system_exe_status = models.CharField(max_length=50, blank=True, null=True)
    config = models.ForeignKey('SystemConfig', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'request'


class RequestAttachPattern(models.Model):
    attached_id = models.AutoField(primary_key=True)
    patterns_dir = models.CharField(max_length=255)
    request = models.ForeignKey(Request, models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'request_attach_pattern'


class RequestSelectPattern(models.Model):
    request = models.ForeignKey(Request, models.DO_NOTHING)
    system_pattern = models.ForeignKey('SystemPatterns', models.DO_NOTHING)

    class Meta:
        db_table = 'request_select_pattern'


class SystemConfig(models.Model):
    config_id = models.AutoField(primary_key=True)
    workspace_dir = models.CharField(db_column='workSpace_dir', max_length=255)  # Field name made lowercase.

    class Meta:
        # managed = False
        db_table = 'system_config'


class SystemPatterns(models.Model):
    pattern_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    patterns_dir = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'system_patterns'


class TagetCode(models.Model):
    targetcode_id = models.CharField(db_column='targetCode_id', primary_key=True,
                                     max_length=255)  # Field name made lowercase.
    classdiagram_path = models.CharField(db_column='classDiagram_path', max_length=255, blank=True,
                                         null=True)  # Field name made lowercase.
    patternsinfo_path = models.CharField(db_column='patternsInfo_path', max_length=255, blank=True,
                                         null=True)  # Field name made lowercase.
    targetcode_path = models.CharField(db_column='targetCode_path', max_length=255, blank=True,
                                       null=True)  # Field name made lowercase.
    complexity = models.ForeignKey('TargetCodeConfig', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'taget_code'


class TargetCodeConfig(models.Model):
    complexity_id = models.AutoField(primary_key=True)
    mupi = models.IntegerField(db_column='MUPI')  # Field name made lowercase.
    complexity_level = models.CharField(max_length=255)
    concrete_rate = models.FloatField()
    execution_times = models.IntegerField()
    interface_rate = models.FloatField()
    max_association_rate = models.FloatField()
    max_class_rate = models.IntegerField()
    max_dependency_rate = models.FloatField()
    max_inheritance_rate = models.FloatField()
    max_realization_rete = models.FloatField()
    max_sparcity_rate = models.FloatField()
    max_superclass_rate = models.FloatField(db_column='max_superClass_rate')  # Field name made lowercase.
    status = models.CharField(max_length=255)

    class Meta:
        # managed = False
        db_table = 'target_code_config'


class User(AbstractEmailUser):
    education = models.CharField(max_length=50)
    last_name = models.CharField(db_column="family", max_length=50)
    field = models.CharField(max_length=50)
    first_name = models.CharField(db_column="name", max_length=50)
    email = models.CharField(db_column="official_email", max_length=50, unique=True)
    university_name = models.CharField(max_length=50)

    class Meta:
        db_table = 'user'


class Field(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):  # For Python 2, use __str__ on Python 3
        return self.name

    class Meta:
        db_table = 'field'


class Post(models.Model):
    title = models.CharField(max_length=128, unique=True)
    subtitle = models.CharField(max_length=256)
    content = models.TextField()
    date_created = models.DateTimeField(null=True, auto_now=True)
    date_modified = models.DateTimeField(null=True)
    status = models.SmallIntegerField(default=1, blank=True, null=False)

    def __str__(self):  # For Python 2, use __str__ on Python 3
        return self.title

    class Meta:
        db_table = 'post'


class DashboardPost(models.Model):
    title = models.CharField(max_length=128, unique=True)
    subtitle = models.CharField(max_length=256)
    content = models.TextField()
    date_created = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    status = models.SmallIntegerField(default=1, blank=True, null=False)

    def __str__(self):  # For Python 2, use __str__ on Python 3
        return self.title

    class Meta:
        db_table = 'dashbord_posts'
