import hashlib
import random
import sqlite3
import web
from dotenv import load_dotenv

from web import form
# setting urls for classes and methods
urls = ("/", "Hello",
        "/register", "Register",
        "/results", "Logged",
        '/login', "Login_user",
        "/logout", "Logout",
        )

web.config.debug = False  # turning debug mode off for working with sessions

app = web.application(urls, globals())  # defining our app

db_url = os.getenv('SQLITE_db_URL')

db = web.database(dbn='sqlite', db=db_url)  # giving our database url for storing sessions data in database

store = web.session.DBStore(db, 'sessions')  # storing session data into our database AFTER making tables

session = web.session.Session(app, store,
                              initializer={'login': 0, 'privilege': 0, 'username': 'test',
                                           'captha': 0})  # making our session
session_data = session._initializer  # initilazing our session for using as dict in our code

render = web.template.render('templates/')  # locating our html file

vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
vemail = form.regexp(r".*@.*", "must be a valid email address")
register_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Textbox("email", vemail, description="E-Mail"),
    form.Password("password", vpass, description="Password"),
    form.Password("password2", description="Repeat password"),
    form.Button("submit", type="submit", description="Register"),
    form.Number('CapthaCode', web.form.notnull),
    validators=[
        form.Validator("Passwords did't match", lambda i: i.password == i.password2)]

)  # making form for register page


class Hello:  # just for some testing :)

    def GET(self):
        return "project is running"


class Register:  # register module for user registration form

    def GET(self):

        f = register_form()

        # making captha image with captha module--->>>

        image = ImageCaptcha(width=280, height=90)

        randint = random.randint(1000,
                                 9999)  # using random module for getting random numbers between 1000 and 9999 and putting it into randint var

        image.write('{0}'.format(randint), './statics/image/kek.png')  # giving dir for saving our image

        session_data['captha'] = randint  # setting our captha value  (because its in a dict ) to randit

        return render.tem(f)  # rendering our html file

    def POST(self):
        f = register_form()

        if not f.validates():  # if user data isnt validated page will be rendered again
            # making captha image with captha module--->>>
            image = ImageCaptcha(width=280, height=90)

            randint = random.randint(1000,
                                     9999)  # using random module for getting random numbers between 1000 and 9999 and putting it into randint var

            image.write('{0}'.format(randint), './statics/image/kek.png')

            session_data['captha'] = randint  # setting our captha value  (because its in a dict ) to randit

            return render.tem(f)  # rendering our html file

        else:

            user_data = web.input()  # getting user input form and using it as object

            username, password, emails = user_data.username, user_data.password, user_data.email  # setting object as variable "this section is optional"

            authdb = sqlite3.connect('users.db')  # connecting to our db

            c = authdb.cursor()  # using our curson

            pwdhash = hashlib.md5(user_data.password).hexdigest()  # hashing user password with haslib module

            sql = """INSERT INTO userdata (username ,password,email) VALUES (?,?,?)"""  # inserting our user input with sqlite script

            try:

                check = c.execute(sql, (user_data.username, pwdhash, user_data.email))  # executing our sqlite command

                authdb.commit()  # commiting our command
            except:

                return "username is already taken"  # if username is already taken this massage will show

            if check and session_data['captha'] == int(
                    user_data.CapthaCode):  # if data is commited in our db and captha code is same as the image shown user will be loged in

                session_data[
                    'login'] = 1  # after all of these steps we will set login key in our session data dict to 1

                if session_data['login'] == 1:  # if login key is 1 we that means user is logged in
                    session_data[
                        'username'] = username  # setting username key in our session data for using it in Logged module

                    raise web.seeother('/results')  # redirecting user to /result page


class Logged:
    logout_form = web.form.Form(

        web.form.Button('Logout'),

    )  # making a simple button for logout

    def GET(self):

        if session_data['login'] == 1:  # this page will only show if user is logged so we need to see if user is logged
            f = self.logout_form()

            return render.logout(f), "welcome {0}".format(session_data['username'])  # welcoming our user

        raise web.seeother(
            '/login')  # if user is not logged in and wanted to see /result page with typing it in url this line code prevent that act

    def POST(self):

        if not self.logout_form.validates():  # if user input didnt validates page will be rendered again

            return render.logout(self.logout_form)  # rendering html file

        else:

            raise web.seeother('/logout')  # if user uses logout button user will be redirected to /logout page


class Login_user:
    login_form = web.form.Form(web.form.Textbox('username', web.form.notnull),

                               web.form.Password('password', web.form.notnull),

                               web.form.Number('CapthaCode', web.form.notnull),

                               web.form.Button('Login'),
                               )

    # configering user login page

    def GET(self):

        # making captha image with captha module--->>>

        image = ImageCaptcha(width=280, height=90)

        randint = random.randint(1000,
                                 9999)  # using random module for getting random numbers between 1000 and 9999 and putting it into randint

        image.write('{0}'.format(randint), './statics/image/kek.png')  # giving dir for saving our image

        session_data['captha'] = randint  # setting our captha value  (because its in a dict ) to randit

        f = self.login_form()

        return render.logtem(f)  # rendering html file

    def POST(self):

        if not self.login_form.validates():  # if user login inputs didnt validate it will render whole page and captctha image again
            # making captha image with captha module--->>>

            image = ImageCaptcha(width=280,
                                 height=90)  # using random module for getting random numbers between 1000 and 9999 and putting it into randint

            randint = random.randint(1000, 9999)

            image.write('{0}'.format(randint), './statics/image/kek.png')  # giving dir for saving our image

            session_data['captha'] = randint  # setting our captha value  (because its in a dict ) to randit

            return render.logtem(self.login_form)  # rendering our form in html file

        else:

            user_data = web.input()  # getting user input form and using it as object

            pwdhash = hashlib.md5(user_data.password).hexdigest()  # hashing user password with haslib module

            authdb = sqlite3.connect('users.db')  # connecting to our db

            sql = """SELECT * FROM userdata WHERE username=? AND password=?"""  # finding  our user input with sqlite script

            c = authdb.cursor()  # making cursor for sqilte

            drip = c.execute(sql, (user_data.username, pwdhash))  # executing our sqlite command

            if drip:  # if sqlite code has executed succesfully code will continue

                listdata = c.fetchall()  # fething user data from db

                if session_data['captha'] == int(
                        user_data.CapthaCode):  # if user input capctha code is same  as picture code will continue

                    if listdata != []:  # if we get our user data from db user will be logged in

                        session_data['login'] = 1
                        d = 1

                        if d == 1:  # if user is logged in-->

                            for i in listdata:  # becuse we used "fethall" command in our code data we are getting is "list" type so we need to loop through it

                                session_data['username'] = i[
                                    1]  # in our list always second element is username so if username is same as username in our session user will be logged in

                            raise web.seeother('/results')  # redicting user to /result after logged in
                    else:

                        return "invalid username or password"  # if user username or password is wrong this message will be show up

                else:

                    return "invalid capctha code"  # if capctha code is wrong it this message will show up


class Logout:  # module for logging out

    def GET(self):
        d = session_data['login']  # getting our login status in session data

        if d == 1:  # if user is logged in we will set his status to 0 because that means user in logged out
            session_data['login'] = 0

            session_data['username'] = ''  # removing username data from session_data

            raise web.seeother('/login')  # redirecting our user to /login url


if __name__ == "__main__":
    app.run()
