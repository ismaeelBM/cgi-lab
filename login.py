import cgi, cgitb
import secret
import time

form  = cgi.FieldStorage()

username = form.getvalue('username')
password = form.getvalue('password')
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


def after_login_incorrect():
    """
    Returns the HTML for the page when the login credentials were typed
    incorrectly.
    """
    return _wrapper(r"""
    <h1> Login incorrect :c </h1>

    <p> Incorrect username or password (hint: <span class="spoilers"> Check
        <code>secret.py</code>!</span>)
    <p> <a href="login.py"> Try again. </a>
    """)

if username == secret.username and password == secret.password:
    print("Set-Cookie:UserID=%s,Password=%s,LoggedIn= true;\r\n" % (username,password))
    print("Set-Cookie:Password = %s;\r\n" % (password))
    print("Set-Cookie:LoggedIn = true;\r\n")
    print ("Content-type:text/html\r\n\r\n")
    print ("<html>")
    print ("<head>")
    print ("<title>Hello - Second CGI Program</title>")
    print ("</head>")
    print ("<body>")
    print ("<p><b>Username</b> %s <b>password</b> %s</p>" % (username, password))
    print ("</body>")
    print ("</html>")

else:
    print(after_login_incorrect())
