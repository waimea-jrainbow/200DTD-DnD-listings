#===========================================================
# YOUR PROJECT TITLE HERE
# YOUR NAME HERE
#-----------------------------------------------------------
# BRIEF DESCRIPTION OF YOUR PROJECT HERE
#===========================================================

from flask import Flask, render_template, request, flash, redirect
import html

from dotenv import load_dotenv
from os import getenv

from app.helpers.session import init_session
from app.helpers.db      import connect_db
from app.helpers.errors  import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.time    import init_datetime, utc_timestamp, utc_timestamp_now


# Create the app
app = Flask(__name__)

# Configure app
init_session(app)   # Setup a session for messages, etc.
init_logging(app)   # Log requests
init_error(app)     # Handle errors and exceptions
init_datetime(app)  # Handle UTC dates in timestamps

# Load Turso environment variables from the .env file
load_dotenv()
ADMIN_USER = getenv("ADMIN_USER1")
ADMIN_PASS = getenv("ADMIN_PASS1")


#-----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def show_all_things():
    with connect_db() as client:
        # Get all the things from the DB
        sql = "SELECT id, name, max_players, current_players FROM campaigns ORDER BY name ASC"
        params = []
        result = client.execute(sql, params)
        campaigns = result.rows

        # And show them on the page
        return render_template("pages/home.jinja", campaigns=campaigns)



#-----------------------------------------------------------
# About page route
#-----------------------------------------------------------
@app.get("/about/")
def about():
    return render_template("pages/about.jinja")


#-----------------------------------------------------------
# Thing page route - Show details of a single thing
#-----------------------------------------------------------
@app.get("/campaign/<int:id>")
def show_one_thing(id):
    with connect_db() as client:
        # Get the campaign details from the DB
        sql = "SELECT id, name, max_players, current_players FROM campaigns WHERE id=?"
        params = [id]
        result = client.execute(sql, params)

        # Did we get a result?
        if result.rows:
            # yes, so show it on the page
            campaign = result.rows[0]
            return render_template("pages/campaign.jinja", campaign=campaign)

        else:
            # No, so show error
            return not_found_error()


#-----------------------------------------------------------
# Admin view page route - Show all the campaigns with the ability to edit and delete current campaigns and add new ones through a form
#-----------------------------------------------------------
@app.get("/admin_view")
def show_all_admin():
    with connect_db() as client:
        # Get all the campaigns from the DB
        sql = "SELECT id, name, current_players, max_players FROM campaigns ORDER BY name ASC"
        params = []
        result = client.execute(sql, params)
        campaigns = result.rows

        # And show them on the page
        return render_template("pages/admin_view.jinja", campaigns=campaigns)


#-----------------------------------------------------------
# Admin login page route - Show all the campaigns with the ability to edit and delete current campaigns and add new ones through a form
#-----------------------------------------------------------
@app.get("/admin_login")
def show_login_page():

        return render_template("pages/admin_login.jinja")


#-----------------------------------------------------------
# Route for logging in as an admin using data posted from a form
#-----------------------------------------------------------
@app.post("/login")
def admin_login():
    # Get the data from the form
    user  = request.form.get("username")
    password = request.form.get("password")

    # Sanitize the text inputs
    user = html.escape(user)
    password = html.escape(password)

    if user == ADMIN_USER and password == ADMIN_PASS:  
        return redirect("/admin_view")
    else:
        flash("Incorrect username or password", "error")
        return redirect("/admin_login")

#-----------------------------------------------------------
# Route for adding a thing, using data posted from a form
#-----------------------------------------------------------
@app.post("/add")
def add_a_thing():
    # Get the data from the form
    name  = request.form.get("name")
    price = request.form.get("price")

    # Sanitise the text inputs
    name = html.escape(name)

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT INTO things (name, price) VALUES (?, ?)"
        params = [name, price]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"Thing '{name}' added", "success")
        return redirect("/things")


#-----------------------------------------------------------
# Route for deleting a thing, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
def delete_a_thing(id):
    with connect_db() as client:
        # Delete the thing from the DB
        sql = "DELETE FROM things WHERE id=?"
        params = [id]
        client.execute(sql, params)

        # Go back to the home page
        flash("Thing deleted", "success")
        return redirect("/things")


