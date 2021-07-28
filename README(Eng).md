# Project Website CPC1

## Introduction
Website for managing materials for QA, RD, Procurement and Warehouse Department of Hanoi CPC1 Pharmaceutical JSC.

## Content
* [Packages](#kythuat)
* [Feature](#congnghe)
* [Using](#sudung)
* [Improvement](#phattrien)

<a name="kythuat"/></a>
## Packages
* Back-end Development:
  * python 3.9.5
  * Django 3.2.4
  * mysqlclient 2.0.3
* Front-end Development:
  * HTML/CSS: Using available template at https://www.free-css.com/free-css-templates/page9/the-green-house
  * Bootstrap 4: For adding modal dialog (Incoming)
  * Jquery 3.6: For adding modal dialog (Incoming)
* Libraries:
  * django-autocomplete-light==3.8.2
  * django-import-export==2.5.0
  * xlwt==1.3.0
  * WeasyPrint==52.5
  * django-bootstrap-modal-forms==2.2.0
  * django-widget-tweak==1.4.8
* Deploy Production (Hosted by Heroku):
  * django-heroku==0.3.1
  * gunicorn==20.1.0
  * dj-database-url==0.5.0
  * psycopg2==2.9.1
  * whitenoise==5.2.0
  * Using Amazon S3 Bucket (django-storages và boto3): For storing static and media file (Incoming)


<a name="congnghe"/></a>
## Feature
1. CRUD data (Create/Read/Update/Delete)
2. Export data in file .xls
3. Export file .pdf
4. Send mail

<a name="sudung"/></a>
## Using
1. RD Department:
    *  Create/Read/Update Register Number data
    *  Create/Read Internal Register Number data
    *  Read expired Register Number
    *  Create Marquette Code for new Product
    *  Create Marquette Code for new Material
    *  Create Marquette Code for new Supplier
    *  Create new Supplier
    *  Create Material Change Notification (Export file .pdf and send mail)
2. Procurement Department:
    * Update BFO Code for Product
    * Read Material data of Product
3. Warehouse Department:
    * Create/Read/Update Material Stocks for Weekly Production Plan
4. QA Department:
    * Read Material data of Product
    * Read Material Change Notification data
    * Read Material Stocks data
    * Create/Read/Update Handling Decision for Material Change Notification
    * Create/Read/Update Handling Information for Material Change Notification
    * Define Materials used for Weekly Production Plan and send mail to notify

<a name="phattrien"/></a>
## Improvement
* Incoming functions:
  * Create modal form to improve user experiment
  * Connect production environment to Amazon S3 Bucket
  * Use cronjob to run notification email daily
  * Input authorization for departments
  * Handle user error (Using alert)
