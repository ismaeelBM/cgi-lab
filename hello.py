#!/usr/bin/env python3

import os, json
import cgi
import cgitb
cgitb.enable()

# Python 3.7 versus Python 3.8
try:
    from cgi import escape #v3.7
except:
    from html import escape #v3.8

__all__ = ['login_page', 'secret_page', 'after_login_incorrect']


def login_page():
    """
    Returns the HTML for the login page.
    """

    return _wrapper(r"""
    <h1> Welcome! </h1>

    <form method="POST" action="login.py">
        <label> <span>Username:</span> <input autofocus type="text" name="username"></label> <br>
        <label> <span>Password:</span> <input type="password" name="password"></label>

        <button type="submit"> Login! </button>
    </form>
    """)

def _wrapper(page):
    """
    Wraps some text in common HTML.
    """
    return ("""
    <!DOCTYPE HTML>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, sans-serif;
                max-width: 24em;
                margin: auto;
                color: #333;
                background-color: #fdfdfd
            }

            .spoilers {
                color: rgba(0,0,0,0); border-bottom: 1px dashed #ccc
            }
            .spoilers:hover {
                transition: color 250ms;
                color: rgba(36, 36, 36, 1)
            }

            label {
                display: flex;
                flex-direction: row;
            }

            label > span {
                flex: 0;
            }

            label> input {
                flex: 1;
            }

            button {
                font-size: larger;
                float: right;
                margin-top: 6px;
            }
        </style>
    </head>
    <body>
    """ + page + """
    </body>
    </html>
    """)

def secret_page(username=None, password=None):
    """
    Returns the HTML for the page visited after the user has logged-in.
    """
    if username is None or password is None:
        raise ValueError("You need to pass both username and password!")

    return _wrapper("""
    <h1> Welcome, {username}! </h1>

    <p> <small> Pst! I know your password is
        <span class="spoilers"> {password}</span>.
        </small>
    </p>
    """.format(username=escape(username.capitalize()),
               password=escape(password)))

def main():
    print("Content-type:text/html\r\n\r\n")

    var_dict = dict(os.environ)
    print(json.dumps(var_dict))

    if ("QUERY_STRING" in os.environ.keys()):
        print("<b>QUERY_STRING</b>: %s<br>" % (os.environ["QUERY_STRING"]))

    if ("HTTP_USER_AGENT" in os.environ.keys()):
        print("<b>HTTP_USER_AGENT</b>: %s<br>" % (os.environ["HTTP_USER_AGENT"]))

    username = ""
    password = ""
    loggedIn = False

    if ("HTTP_COOKIE" in os.environ.keys()):
        cookies = os.environ["HTTP_COOKIE"].split(',')
        print("<b>HTTP_COOKIE</b>: %s<br>" % (cookies))

        if len(os.environ["HTTP_COOKIE"]) > 0:
            for cookie in cookies:
                (key, value) = cookie.split('=')
                if key == "UserID":
                    username = value
                if key == "Password":
                    password = value
                if key == "LoggedIn":
                    loggedIn = True


    if loggedIn:
        print(secret_page(username, password))

    print(login_page())

main()