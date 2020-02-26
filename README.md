# exe_orientation_Q
Exeter Orientation - A campus treasure hunt.

This service is provided as a django web application.

# How to run code base in production
Currently when every time someone commits to the master branch the application gets redeployed:
You can find the web app at: https://exeterorientation.azurewebsites.net/


#### Native Application Development

* Install [Python](https://www.python.org/downloads/)

Running Django applications has been simplified with a `manage.py` file to avoid dealing with configuring environment variables to run your app. From your project root, you can download the project dependencies with:

# How to run the code base locally:
```bash
pipenv install
```

To run your application locally:

```bash
pipenv shell
python manage.py runserver 0:8000 --settings=deploy_django_to_azure.settings.local
```

Your application will be running at `http://localhost:8000`.  

##### Debugging locally
To debug a `django` project run `python manage.py runserver` with DEBUG set to True in `local.py` to start a native django development server. This comes with the Django's stack-trace debugger, which will present runtime failure stack-traces. For more information, see [Django's documentation](https://docs.djangoproject.com/en/2.0/ref/settings/).
