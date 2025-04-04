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