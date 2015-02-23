all:
	export DJANGO_SETTING_MODULE='douhack.settings.local'; python manage.py runserver_plus

prepare_local:
	createuser -d douhack
	createdb -U douhack douhack 
