# About This Project

A fashion e-commerce website made with Django web framework and integrated with Firebase Storage and Paypal Smart Payment Buttons **(developed on Windows)**.

You can test it out here https://ruri-commerce.herokuapp.com/. Use sandbox paypal account to checkout.

# Web Page Appearance

**Home Page**
![Home Page](https://user-images.githubusercontent.com/17781413/139363212-fe253209-528f-46a3-9432-3ef4d39d967a.PNG)

**Shop Page**
![Shop Page](https://user-images.githubusercontent.com/17781413/139363217-2ff9051f-7f29-4342-a6d2-eca1e23d2098.PNG)

**Product Page**
![Product Detail Page](https://user-images.githubusercontent.com/17781413/139363224-443392e4-4c44-4233-8573-982a3ff79f34.PNG)

**Cart Page**
![Cart Page](https://user-images.githubusercontent.com/17781413/139363235-b476baf0-de05-4ba5-baac-3d43a1c50eeb.PNG)

**Checkout Page**
![Checkout Page](https://user-images.githubusercontent.com/17781413/139363240-47e0b2cb-491f-4760-b536-360bbb8b34d3.PNG)
 
**Order Status Page**
![Order Status Page](https://user-images.githubusercontent.com/17781413/139363264-cf89350c-2168-487d-ae71-749e0dfef9d3.PNG)

**Order Detail Page**
![Order Details Page](https://user-images.githubusercontent.com/17781413/139363268-403c9665-9732-46db-92bd-e54a390b630a.PNG)

**Login / Signup Page**
![Login-Signup Page](https://user-images.githubusercontent.com/17781413/139363272-15fdd7f7-b60e-4476-9305-e05a40c84c98.PNG)


# How to run this project?

- Download the project using this command.

```
git clone https://github.com/ruriarmandhani/django-ecommerce.git
```

- Go to the project directory and make a virtual environtment.

```
py -m venv venv
```

- Run your virtual environtment.

```
venv\Scripts\activate.bat
```

- Intall the requirements.

```
pip install -r requirements.txt
```

- Go to olshop directory and set the SECRET_KEY variable in settings.py. You can generate django secret key here https://djecrety.ir/.

```
SECRET_KEY = 'your secret key'
```

- Now you need to download the firebase service account key.

![image](https://user-images.githubusercontent.com/17781413/139064434-9484ac02-29b9-46fd-b578-4e866317802a.png)

- And then set up the google cloud storage in the settings.py.

```
GS_BUCKET_NAME = 'your firebase bucket name '
GS_CREDENTIALS = service_account.Credentials.from_service_account_file('your json key path')
```

- Set up SMTP config in settings.py. You can change the config if you don't want to use gmail smtp server.
- See the smtp servers list [here](https://www.arclab.com/en/kb/email/list-of-smtp-and-pop3-servers-mailserver-list.html).

```
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your email'
EMAIL_HOST_PASSWORD = 'your password'
```

- Get the GEODB API key from [here](https://rapidapi.com/wirefreethought/api/geodb-cities/). (GEODB API key is used to get all of the cities in the world to run the autocomplete.js)
- Set up your system variable.

```
set GEODB_API_KEY='your geodb api key'
```

- Or you can add it manually like this.

![GEODB_API_KEY](https://user-images.githubusercontent.com/17781413/139062002-8fe7df92-cd36-4458-8b38-bb11cb6f29fa.PNG)

- Create database scheme.

```
py manage.py makemigrations
py manage.py migrate
```

- Create super user to access django admin.

```
py manage.py createsuperuser
```

- And finally you can run the project.

```
py manage.py runserver
```
