# Project Title

Hesabe payment gateway application.

## Getting Started

<<<<<<< HEAD
These instructions will help you to integrate hesabe payment gateway on your local machine for development and testing purposes. 
 

=======
These instructions will help you to integrate hesabe payment gateway on your local machine for development and testing purposes.

### Installing and configurations

```
git clone https://github.com/prachi1326/hesabe

```

Install all the dependenices by this command.

```
pip install -r hesabe_app/requirements.txt
```

Step 1) Add installed application to your project.

Step 2) Add installed application to INSTALLED_APPS variable in settings.py

For example
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hesabe_app',-->add this
]
```
Step 3)Do the migrations

```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```
Step 4)Go to admin panel

Step 5)Add  Configuration varaible values in admin panel.
```
Example:
Merchant code:      842217
Success Url:        http://localhost:8000/response
Failure Url:		http://localhost:8000/response
accesscode:			c333729b-d060-4b74-a49d-7686a8353481
Payment Url:		https://sandbox.hesabe.com
Working key:		PkW64zMe5NVdrlPVNnjo2Jy9nOb7v1Xg
IV:					5NVdrlPVNnjo2Jy9
Knet status:		select enable/disable
mpgs status:		select enable/disable
```

### How to use this application.

Create payment function with request parameter and pass amount and other optional parameteres as well as shown below.

This payment function will render the pay.html file which has payment options such as knet/mpgs.
```
def payment(req):
	payment_variables = {

		"variable1" :  variable1 value,
		"variable2" :  variable2 value,
		"variable3" :  variable3 value,
		"variable4" :  variable4 value,
		"variable5" :  variable5 value,
		"amount":amount value,
		"order_id": Order id

	}
	return render(req, 'hesabe_app/pay.html',payment_variables)

```
