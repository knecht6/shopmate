# Tshirtshop v1.0.0
E-commerce where can search products, with categories, shopping-card and checkout managed by Sripe, have BackOffice Management, where admins are able add new items, users and sell module.

# Tecnologies

# FrontEnd

*	ReactJs v16.7
*	Boostrap v4
*	CSS	3	

# BackEnd

*	Phyton v3.6.7
*	Django v2.2.1
*	Django REST Framework v4.3.0

Web Services
A web service is a technology that uses a set of protocols and standards that serve to exchange data between applications.
Components
•	Rest API (Backend)
•	Frontend Application
Components Description:
•	Rest API: Responsible for the functionality of the application
•	Frontend Application: Application with which users can interact and which, through the consumption of the different microservices, offers users the different functionalities.

Descriptions:
•	Customer: Represents the user of the application, which can interact with the frontend application through different web browsers.
•	React Frontend Application: Frontend application with which users can interact and allow them to access all the functionalities of the system.
o	Cart: React component responsible for the handling of the shopping cart
o	CartItem: React component responsible for displaying the information of each item added to the cart
o	Category: React component responsible for displaying the information of the categories stored in the database
o	CategoryList: React component responsible for containing the list of categories in the database
o	UpdateGeneralData: React component responsible for updating the general data of the Customer
o	Department: React component responsible for displaying the information of the departments stored in the database
o	DepartmentList: React component responsible for containing the list of departments in the database
o	Footer: React component responsible for displaying the footer information of the page
o	Home: React component responsible for displaying the information handled in the Home
o	UpdateData: React component responsible for containing the different customer data update components, such as UpdateGeneralData, UpdateCreditCard and UpdateAddress.
o	Helper: Function in charge of refreshing the access token when necessary
o	ItemDetail: React component responsible for displaying the detailed information of the articles handled in the database
o	Login: React component responsible for managing the login form and all its validations
o	NavBar: React component responsible for displaying the information handled in the navbar of the page
o	SingUp: React component responsible for handling the "Sign Up" form and all its validations
o	Review: React component responsible for displaying the information of the reviews made to the products managed in the database
o	ProductDetail: React component responsible for displaying the products stored in the database
o	ProductReview: React component responsible for managing the list of reviews made to the different products
o	UpdateCreditCard: React component responsible for storing the form for the modification of the customer's credit card
o	ShoppingSuccess: React component that manages the completion of the purchase and the payment of the cart
o	UpdateAddress: React component responsible for storing the form for the modification of the customer's address information

•	Django Rest API
o	Products: Rest application responsible for the management of information related to products, such as the deployment of product information, display of details, prices, among others.
o	Orders: Rest application responsible for the management of orders made in the application, shopping cart, payments, among others.
o	Django Models: Represents all the models made in Django Rest for the connection with the databaseMySQL 
•	Database: Base de datos la cual se estara consultado para realizar cada una de las funcionalidades de la aplicación 

Technologies
React
Open source Javascript library designed to create user interfaces with the aim of facilitating the development of applications on a single page.
Versions:
•	NodeJs: 10.16.0
•	Npm: 6.9.0
Django Rest Framework
Django REST framework is a powerful and flexible toolkit for building Web APIs
Versions
•	Django==2.2.1
•	django-cors-headers==3.0.1
•	django-filter==2.1.0
•	djangorestframework==3.9.4
•	djangorestframework-simplejwt==4.3.0
•	Markdown==3.1
•	mysqlclient==1.4.2.post1
•	Pillow==6.0.0
•	pkg-resources==0.0.0
•	PyJWT==1.7.1
•	pytz==2019.1
•	six==1.12.0
•	sqlparse==0.3.0
