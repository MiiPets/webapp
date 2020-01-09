# Tech stack

* Python
* Django (web framework)
* Google cloud (hosting services)
* HTML
* CSS
* JavaScript

While in the developement stage, the DB used is sqlite3. When we move into production this will change though.

# MVP

The code encountered here will be for the MVP product that MiiPets launches. It will cater the following needs:

* Allowing MiiOwners (normal pet owners) to sign up and make a booking for various services.
* Allowing MiiSitter to register as sitters and charge MiiOwners to provide services
* ~~Allowing MiiProviders to register their company and allow MiiOwners to make apointments through MiiPets~~
* Allowing MiiOwners to pay the MiiSitters and ~~MiiProviders~~ while giving compensation to MiiPets (at the moment 20%)

# Deployment

At the moment the plan is as follow:

Deploy the app on Heroku so that we have a PaaS (platform as a service), saving money on hiring someone to oversee it the whole time and allowing us to focus on other things as well. The database will live on heroku in PostgreSQL db, where the data it will be opened via an API for the apps to access it. The file system will be hosten on an AWS bucket system which will integrate very nicely with Heroku as Heroku is also deployed on AWS.

# HTML template is obtained from Envato Market

