=========
mPulseApp
=========
``mPulseApp`` is a Python Django application using REST Frameowrk.
It exposes API endpoints for creating instances of a model, one by one using POST or in batch using PUT
and endpoints for list and detail views.


Installation
============
Installation of ``mPulse`` is very easy following these detailed end-to-end steps.

1- download/clone this repo by pressing the green button on the top of the page

2- on your terminal, open a new session and go the the directory you'd like to install in
::

  $ cd <folder_name>/

3- if you don't have virtualenv installed, let's intall it
::

  $ pip install virtualenv

4- we'll need to create a virual environment from which we'll run everything
::

  $ virtualenv <env_name>
  
5- change your directory to ``<env_name>`` and activate the new environment
::

  $ cd <env_name>/
  $ source bin/activate

6- install django for this env
::

  $ pip install django

7- lets create a project
::

  $ django-admin startproject <project_name>
  
8- move the requirements.txt file you downloaded to the newly created ``<project_name>`` directory.

make sure it's in the same directory as manage.py
    
9- change your directory once again to the newly created ``<project_name>`` directory.
::

  $ cd <project_name>/
  
10- in order for everything to run, the app requirements need to be installed.
::

  $ pip install -r requirements.txt


  
Great, now we have all our requirements installed
  
11- We can finally create an app
::

  $ python manage.py startapp <app_name>
  
12- use downloaded files
``admin.py`` ``models.py`` ``maprser.py`` ``viewspy`` ``serializer.py``
to replace the same ones python just created in <app_name> directory

13- use downloaded ``urls.py`` to replace the one in INNER ``<project_name>`` dierctory

14- using a text editor, edit the file ``setting.py`` by adding
::

    'rest_framework',
    'posts',
to ``INSTALLED_APPS``
AND
::

    REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]}
to the end of the ``settings.py`` file, this a requirements from REST documentation

15- IMPORTANT: edit the ``urls.py`` and change the mpulseapp name with your own ``<app_name>``

16- It's migration time
::

    $ python manage.py makemigrations
    $ python manage.py migrate
if that fails for any reason, move the ``0001_initial.py`` to a new 
``migrations`` directory in ``<app_name>`` and run the migrate command only again

17- create a super user, needed for authentication with each request 
::

    $ python manage.py createsuperuser
18- at last, run server
::

    $ python manage.py runserver
ON SUCCESS you should see a link like ``http://127.0.0.1:8000/``
we'll refer to it as <link>




Usage
=====




We now have a running app in a virtual environment, accessable with that

Although we can use a browser to send GET requests natively, we'll use a client
like ``Postman`` so we can send POST And PUT requests easily.


1- Download and install ``Postman``
::

    https://www.postman.com/downloads/

Now we don't have any members to view, so let's send a POST request to create one

2- in ``Postman``, click the + New for a new request, choose POST from the options and this url
::

    <link>/api/members/create/

3- in ``Authorization`` tab choose ``Basic Auth`` and enter you superuser credentials
4- in ``Body`` tab, choose ``form-data`` and enter data fields in ``KEY`` and values in ``VALUE``,
order does not matter as long as you justify Type and Required, and hit ``Send``
You should see a response with the model instance that was just saved

5- in a browser navigate to 
::

    <link>/admin/
and verify our new member

Next up, sending some GET requests.

6- back in ``Postman``, change the request method to GET and the link to
::

    <link>/api/members/
 when you hit ``Send``, you should see a list of the entry you just made

We need more entries in our DB to GET from 
Time for batch uploading

7- change the method PUT and the request link to
::

    <link>/api/members/batch
8- in ``Body`` -> ``from-data table``, change the type of the first key 
from ``Text`` to ``File`` and choose the member_data.csv file and hit Send

You should see messages with progress update

Final step, with our DB populated with. a lof of new Members, let's GET a few by 
Params

9- set the request to GET again, and the request link to
::

    <link>/api/members/?id=<value>
This should return the user with that id value
change id in request link to 
   * ``ph`` for ``phone_numer``
   * ``cmid`` for ``client_member_id``
   * ``aid`` for ``account_id``
and give it a few tries.



Scaling
=======

To make full use of this app, users will need to upload csv files of millions of rows.
That's a file size of 100+ MBs
For obvious reasons, this kind of file shouldn't be uploaded with Http
I reccomend that this app has a front end with an uploader and FormHandler
Storage should not be an issue since uploaded files are deleted as soon as they'reprocessing
As for DB optimization and since a write incurs reads too, I reccomend:
   * using a noSQL KV store (ex ``mongoDB``)
   * Sharding the members table by account_id 
   * implementing a messaging/queue system (ex ``rabbitMQ``)
   
