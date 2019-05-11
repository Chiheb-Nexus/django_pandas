#
# Déclaration des modèles de l'application example_project
#


from django.db import models


class Manager(models.Model):
    """Chaque employé a un manager"""
    name = models.CharField(max_length=200, verbose_name='Manager')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'manager'
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'


class Job(models.Model):
    """Chaque développeur a un job"""
    name = models.CharField(max_length=200, verbose_name='Job')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'job'
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'


class Developer(models.Model):
    """Model des développeurs"""
    name = models.CharField(max_length=200, verbose_name='Name')
    age = models.IntegerField(default=0, verbose_name='Age')
    job = models.ForeignKey(
        Job,
        verbose_name='Job',
        related_name='dev_job',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    manager = models.ForeignKey(
        Manager,
        verbose_name='Manager',
        related_name='dev_manager',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    date = models.DateField(verbose_name='Date')

    def __str__(self):
        return '{dev_name} - {job} <{manager}>'.format(
            dev_name=self.name,
            job=self.job,
            manager=self.manager
        )

    class Meta:
        db_table = 'developer'
        verbose_name = 'Developer'
        verbose_name_plural = 'Developers'
