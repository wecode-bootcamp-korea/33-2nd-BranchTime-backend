
SECRET_KEY = 'django-insecure-y$7p0l*ltqyk_^w!x117n@sv0#e97awlhc76rrt$#b(38ml%cx'


DATABASES = {
    'default' : {
        'ENGINE'  : 'django.db.backends.mysql',
        'NAME'    : 'branchtime',
        'USER'    : 'root',
        'PASSWORD': '1234',
        'HOST'    : '127.0.0.1',
        'PORT'    : '3306',
        'OPTIONS' : {'charset': 'utf8mb4'}
    }
}


ALGORITHM = 'HS256'