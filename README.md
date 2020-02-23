# exe_orientation_Q
Exeter Orientation - A campus treasure hunt.

This service is provided as a django web application.

# How to run the code base locally (in IBM cloud style):
1. Install the IBM cloud developer tools:
	https://cloud.ibm.com/docs/cli?topic=cloud-cli-getting-started
2. Run it in a local development container from the app directory. This requires Docker:

```bash
$ ibmcloud dev build
```

```bash
$ ibmcloud dev run
```

Currently when every time someone commits to the develop branch the application gets redeployed:
You can find the web app at: https://eoq1.eu-gb.mybluemix.net/


#### Native Application Development

* Install [Python](https://www.python.org/downloads/)

Running Django applications has been simplified with a `manage.py` file to avoid dealing with configuring environment variables to run your app. From your project root, you can download the project dependencies with:

```bash
pipenv install
```

To run your application locally:

```bash
pipenv shell
python manage.py start
```

Your application will be running at `http://localhost:3000`.  You can access the `/health` endpoint at the host.

##### Debugging locally
To debug a `django` project run `python manage.py runserver` with DEBUG set to True in `settings.py` to start a native django development server. This comes with the Django's stack-trace debugger, which will present runtime failure stack-traces. For more information, see [Django's documentation](https://docs.djangoproject.com/en/2.0/ref/settings/).
