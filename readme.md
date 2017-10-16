# My Window Cleaner Web App #

## Background ##

This app is a simple management system for window cleaners and their back office. It is based on a real-world situation with input from a North-London company.

The work flow is based on window cleaners (WCs) needing to access their daily worksheets online (on mobile). These have to have the clients' addresses, job price etc. Jobs are organised by date.

Once a job is done it has to be checked in: it is assigned a status of 'completed', and a payment status of 'paid' or 'owed'. In the backend this then generates a new 'due' job for the customer based on the completed date and the job frequency (usually 4 weeks).

As part of the cycle, office staff have to allocate 'due' jobs to confirm the job date and the WC attached to a job.

WCs need to transfer a commission fee to the office. In reality this would not be done via Stripe or Paypal, as the commission on these services is too high and they would normally do a bank transfer. However for this project I implemented a Stripe payment facility as an example. Here the whole turnover is sent. Once transferred, jobs are marked as 'invoiced' and are removed from the invoice page.

WCs usually go back to collect unpaid jobs at a later date. At this point they can go to their owings and check in jobs as having been paid. 

They also need to keep track of their expenses. This is independent of the back office.

The design brief was to keep the app as **clutter-free** as possible. It is intended to be used rapidly on an hourly basis, by people for whom English may not be a first language, so clarity was the main design constraint, and options need to be limited so there is very little chance for errors. It is a mobile-first site.

## How the app is organised ##


The Django project is divided into several apps:
 
 1. **Accounts**: user and auth management. Relies on Django admin site for managing users. I have used user groups to assign permissions and access to views (via [GroupRequiredMixin](https://django-braces.readthedocs.io/en/latest/access.html#grouprequiredmixin) imported from [django-braces](https://django-braces.readthedocs.io/en/latest/index.html)). The two groups here are **office_admin** and **window_cleaner**. Some of the code makes references to other groups for future development but is not used. 
 2. **Common**: app used for template tags used on base.html 
 3. **Customers**: for customer models, views etc., generally limited to the **office_admin** group. When creating a new customer, addresses are found via a [Google Place Autocomplete API](https://developers.google.com/maps/documentation/javascript/examples/places-autocomplete). This has its limitations for a real-world application but is free. 
 4. **Expenses**:  for expense models, views etc. Only available to **window_cleaner** group. 
 5. **Franchises**: for franchise models. The project is setup so that office staff can only see customers and related data from their own franchise. There is no franchise  management built in beyond the Django admin site.  
 6. **Worksheets**: for models etc. relating to jobs. This is where the bulk of the functionality resides for the project.

## Testing ##


The bulk of testing is testing for access (login required/group required) and succes/failure of POST requests and redirects, as I relied on Django Generic Class-Based Views for most of the design. Except for custom template tags and database errors returned to views, coverage is 100%. The in-browser testing was performed manually with all possible combinations attempted (but no JS-specific testing). For example the Stripe payment method happens partly independently of the Django backend via Javascript.

## Using the app ##


### For office staff: ###
The login 'DAVE' with password 'W1nd0wze' can be used to login as **office_admin**.
**office_admin** will only see the 'customers' link in the nav. This will list all customers (paginated by 10). Users can add or search customers.

There are 3 buttons on the customer list: job list, customer edit and map.

* **Job list** will display the job history for that customer. New jobs can be added **if there is not already a due job** (the add button will be disabled otherwise). The job rows will be formatted differently for due/completed/paid/owed jobs. The display is in decreasing date order. From there jobs can be edited using the edit button. This would be the stage at which jobs are allocated (from a 'due' status) to a WC. This edit form has some custom validation, as not all combination of field values are permitted.
* **customer edit** loads a page to edit the customer details
* **map** loads a location map for the customer address. As the lat/long was not included in the dummy data used to populate the database, only customers that have had the address manually added have that link enabled.
 
### For window cleaners: ###
The login 'KATE' with password 'W1nd0wze' can be used to login as **window_cleaner**.
**window_cleaner** will only see the 'worksheets'/'expenses'/'invoices'/'owings' links in the nav. 

The redirect after login loads '**worksheets**'. These are grouped by date in an accordion. The badges on the accordion headers summarise the number of jobs and total amount.
The accordion section body lists jobs for a day. WCs can check in jobs either as completed/paid or completed/owed (via AJAX). There is a link to load a 'job detail' modal. Once checked in, a job is removed from the list and the totals in the headers are changed (with JQuery). 

'**expenses**' is a simple page to view and edit/add expenses.

'**invoices**' is organised similarly to 'worksheets', however jobs have to be paid in bulk for a date. The Stripe 424242424242 card can be used for testing.

'**owings**' lists all jobs owed to a WC. The search box is a JQuery filter for quick access to the relevant record. The job is logged as paid via an AJAX button.

## Sources ##


The design uses the [Materialize.css](http://materializecss.com/) framework. I have kept the few custom css markups in-line to make the code clearer for the purpose of this exercise. [https://github.com/codedance/jquery.AreYouSure](https://github.com/codedance/jquery.AreYouSure) code is used to prevent users leaving pages with dirty forms. Other sources are referenced in the code comments.