# BookApp_Django
Web-app made using Django with 3 type of users

Framework used: Django
languages used: Python3 , html , css , bootstrap

Working:
Homepage without any user logged in takes you to login page where signup
button is available in case want to create new user.
There are three type of users : customer , seller , administrator
at time of registration specify type of user in account type.
After registeration enter username and password to login.
The UI is compatible to be used in mobile and notepad browser also.

If login is made as administrator you will be redirect to dashboard where all
detials of customers and sellers are available and details of all books also.Total
number of orders , pending orders and out for delivery is displayed on
dashboard. The administrator can change status of orders.

If login is made as seller you will be redirected to page for seller only which has
feature to add or delete booksonly belonging to that seller. Total number of
books of seller is displayed there. and seller will see his/her books and can also
see all books.

If login is made as customer then books ordered by him/her is displayed can
also view all books and has feature or create a order for book and the status of
order will be updated by administrator.
