# Webpy-login-signup-
a simple user registration and login system with session management. with captcha system with python2


## Project configuration:
To run the project and perform testing, you need to have the SQLite database. Place a SQLite file in the project directory itself.

I used NGINX web server to display the CAPTCHA image (make sure to run the web server first) from the "src" tag in the "project/templates/" directory as follows: "http://localhost/image/kek.png" 
(Note: First, you need to configure NGINX, which I'll explain in the text below.)

Once you have created the database file, navigate to "making_table.py" (if it's the first time running this project on your system) to create the required tables using the execute functions.

In the "main.py" file, make sure to set the `db_url` variable correctly.

## NGINX configuration:
After downloading NGINX, go to "nginx-1.22.1\conf\nginx.conf" and in the server section, specify the root directory folder for the project's static files.

Once you have configured NGINX, you can run it, and then run your project.

Please note that there may be some errors or typos in the original text, so it's advisable to double-check the instructions and make necessary corrections if needed.

