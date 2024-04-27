<h1> Legislative Data - Django Project </h1>

## To set up and execute this project, follow the instructions below:

## Prerequisites
Python 3.7 or later
Django 3.2 or later
Other dependencies listed in the requirements.txt file

## Installation
Clone the project repository to your local machine.

- Create a virtual environment for the project.

python3 -m venv venv

- Activate the virtual environment.

source venv/bin/activate

- Install the project dependencies.

pip install -r requirements.txt

## Execution
- Run the migrations to create the necessary database tables.

python manage.py migrate

## Configuration

- Create an admin user to access the Django admin interface.

python manage.py createsuperuser

- Data Import - CSV Upload:
Use the Django admin interface to import data from the provided CSV files (persons.csv, bills.csv, votes.csv, vote_results.csv) into the application. The upload forms are available in the admin pages for Persons, Bills, Vote Results and Votes models.

## Start the Django development server.

python manage.py runserver

## Access the Admin Interface:
- Once the server is running, you can access the admin interface by visiting http://127.0.0.1:8000/admin/ in your web browser. Log in with the admin credentials you created.

## Usage
In the Django admin interface, navigate to the Legislative Data section to view and manage the data.
Use the CSV upload functionality in the models to import data from CSV files.
Check the 'Supported Bills' and 'Opposed Bills' fields on the Person admin page to see how many bills each legislator supported and opposed.
Check the 'Supported Legislators' and 'Opposed Legislators' fields on the Bills admin page to see how many legislator supported and opposed each bill, as well as the 'Primary Sponsor' of the Bill.


## Conclusion
This Django project provides a simple interface for managing and querying legislative data. It allows users to import data from CSV files and view information about legislators' voting history in the admin interface.
