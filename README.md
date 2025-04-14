# Setup Flow: 

## Setup Virtual Env:
1. create the venv:

```shell
└─▪ python3 -m venv env 
```

2. activate the venv:

```shell
└─▪ source env/bin/activate 
```
## Install Django and DjangoRestFramework:

1. Install dependencies:

```shell
└─▪ pip install django 
```

2. create a django project before start using the DRF:

```shell
└─▪ django-admin startproject ecommerce_proj_main . # the . is to have the files of the project created in the current directory.
```

3. install DRF:

```shell
└─▪ pip install djangorestframework
```

4. add the drf to your installed_aps setting in the project

5. extract the requierments installed 
```shell
pip freeze > requirements.txt
```

## Management Commands ? 
- In django apps you can define managmenet commands inside each installed_app
- The scripts should be defined inside this folder structure `management/commands`
- To run these commands 
```shell
└─▪ python3 ./manage.py name_of_script_with_.py_at_the_end
```

## Generate a relational-diagram to your data models using python extension:
```shell
└─▪ python3 ./manage.py graph_models name_of_app > `app_models.dot`
```

## Fixing N+1 problem when you query the db
- for 3 orders, and 2 orderItems per order and 1 product per orderItem we used to query the db 19 times
- using `prefetch_related()` instead of `all()` we reduced it to 8 queries.
- using the nested level `prefetch_related()` we optiomized it to 3 queries.

## Creating superuser 
```shell
└─▪ python3 ./manage.py createsuperuser
```