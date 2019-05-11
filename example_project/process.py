#
# Dans cet example d'application django on va:
# - Lire les données d'un document EXCEL (.xlsx)
# - Insérer les données du document EXCEL dans une base de donnée (SQLite)
# - Faire des opérations dans la base en utilisant l'ORM de Django
# - Modéliser les données de la base de donnée dans un DataFrame (Pandas)
# - Refaire les meme opérations qu'on a fait avec la base de donnée avec Pandas
#

import os
import sys
import pathlib
import django
from django.db import transaction
from django.db.models import Avg, Sum
import openpyxl
import pandas as pd


ABSOLUTE_PATH = str(pathlib.Path(os.getcwd()).parent)
sys.path.append(ABSOLUTE_PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_pandas.settings'

django.setup()

from example_project import models  # noqa: E402


def read_excel_file(file_path='', sheet_name='Sheet1'):
    """On va lire le document EXCEL avec openpyxl
    NB: On peut le lire directement avec Pandas
    Mais je préfère le lire avec openpyxl ...
    Parce que je veux controler ce que je fais :D"""
    wb = openpyxl.load_workbook(file_path)
    ws = wb[sheet_name]
    data = list(zip(*ws.columns))
    column_names = [elm.value for elm in data[0]]
    values = [[k.value for k in elm] for elm in data[1:]]
    return column_names, values


def insert_data(values):
    """Insertion des données dans la database"""
    with transaction.atomic():
        for name, age, job_name, date, manager_name in values:
            manager, _ = models.Manager.objects.get_or_create(
                name=manager_name
            )
            job, _ = models.Job.objects.get_or_create(name=job_name)
            developer, _ = models.Developer.objects.get_or_create(
                manager=manager,
                job=job,
                name=name,
                age=age,
                date=date
            )
            # print(developer)


def read_data():
    """Read data from Database"""
    names = [
        'id',
        'name',
        'age',
        'job__name',
        'manager__name',
        'date'
    ]
    return models.Developer.objects.all().values_list(*names)


def create_df(data):
    """Create DataFrame from database"""
    column_names = [
        field.verbose_name for field in models.Developer._meta.fields
    ]
    return pd.DataFrame(
        data,
        columns=column_names
    )


def pprint(dataframe=None, database=None, field='', header=''):
    """Pretty print data"""
    print('#' * 5, header, '#' * 5)
    if database:
        print("""Database: {field}: {data}""".format(
            field=field,
            data=database.get(field)
        ))
    if dataframe:
        print("""DataFrame: {field}: {data}""".format(
            field=field,
            data=dataframe
        ))
    print()


def operations(df):
    """Faire les memes opérations sur la database et sur le DataFrame"""
    # Average age
    db_avg = models.Developer.objects.all().aggregate(
        average=Avg('age')
    )
    df_avg = df['Age'].mean()
    pprint(
        dataframe=df_avg,
        database=db_avg,
        field='average',
        header='Average Age'
    )
    # Sum age
    db_sum = models.Developer.objects.all().aggregate(
        sum=Sum('age')
    )
    df_sum = df['Age'].sum()
    pprint(
        dataframe=df_sum,
        database=db_sum,
        field='sum',
        header='Sum Age'
    )
    # Average age uniquement pour Manager == Chiheb
    db_avg_chiheb = models.Developer.objects.filter(
        manager__name='Chiheb'
    ).aggregate(
        average=Avg('age')
    )
    df_avg_chiheb = df.loc[df['Manager'].isin(['Chiheb'])]['Age'].mean()
    pprint(
        dataframe=df_avg_chiheb,
        database=db_avg_chiheb,
        field='average',
        header='Average only chiheb'
    )
    # Average age uniquement pour job = Python developer
    db_avg_python = models.Developer.objects.filter(
        job__name='Python developer'
    ).aggregate(
        average=Avg('age')
    )
    df_avg_python = df.loc[df['Job'].isin(['Python developer'])]['Age'].mean()
    pprint(
        dataframe=df_avg_python,
        database=db_avg_python,
        field='average',
        header='Average Age only Python developer'
    )


if __name__ == '__main__':
    file_path, sheet_name = 'dataset.xlsx', 'Sheet1'
    columns, values = read_excel_file(file_path, sheet_name)
    insert_data(values)
    data = read_data()
    df = create_df(data)
    operations(df)
