from django.db import models


# Create your models here.
class ADR_GBA(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    img = models.ImageField(upload_to="")


class Employees(models.Model):
    employee_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, default="nousername")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    cnp = models.CharField(max_length=50)
    email = models.CharField(max_length=500)
    cellphone = models.CharField(max_length=50)
    enrollment_Date = models.DateField(auto_now=True)
    #enrollment_Date = models.DateField(null=True)
    rating = models.FloatField(null=True)
    cache_professional_score = models.FloatField(null=True)
    line_manager = models.ForeignKey(to='Employees', null=True)


class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=50)


class Skills(models.Model):
    skill_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    score = models.FloatField()


class Teams(models.Model):
    team_id = models.AutoField(primary_key=True)
    leader_id = models.ForeignKey(to='Employees')
    name = models.CharField(max_length=50)
    specific = models.CharField(max_length=50)
    base_location = models.CharField(max_length=50)


class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    location = models.CharField(max_length=50)
    parent_id = models.ForeignKey(to='Tasks')


class Employee_Skills(models.Model):
    employee_id = models.ForeignKey(to='Employees')
    skill_id = models.ForeignKey(to='Skills')
    experience = models.FloatField()
    observation = models.CharField(max_length=50)


class Employee_Roles(models.Model):
    employee_id = models.ForeignKey(to='Employees')
    role_id = models.ForeignKey(to='Roles')
    assignment_date = models.DateField(auto_now=True)
    score = models.FloatField(null=True)


class Tasks_Required_Skills(models.Model):
    task_id = models.ForeignKey(to='Tasks')
    skill_id = models.ForeignKey(to='Skills')
    observations = models.CharField(max_length=500)
    min_score = models.FloatField()
    number_of_persons = models.IntegerField()


class Tasks_Team_Assignments(models.Model):
    task_id = models.ForeignKey(to='Tasks')
    team_id = models.ForeignKey(to='Teams')
    observations = models.CharField(max_length=500)
    status = models.IntegerField()


class Team_Skill(models.Model):
    team_id = models.ForeignKey(to='Teams')
    skill_id = models.ForeignKey(to='Skills')
    experience = models.FloatField()
    observations = models.CharField(max_length=500)


class Team_Assignments(models.Model):
    team_id = models.ForeignKey(to='Teams')
    employee_id = models.ForeignKey(to='Employees')
    observation = models.CharField(max_length=500)
