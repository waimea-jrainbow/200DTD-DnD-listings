#===========================================================
# YOUR PROJECT TITLE HERE
# YOUR NAME HERE
#-----------------------------------------------------------
# BRIEF DESCRIPTION OF YOUR PROJECT HERE
#===========================================================

from flask import Flask, render_template, request, flash, redirect, session
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
@app.route("/")
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
# Thing page route - Show details of a single thing
#-----------------------------------------------------------
@app.get("/campaign/<int:id>")
def show_one_thing(id):
    with connect_db() as client:
        # Get the campaign details from the DB
        sql = "SELECT id, name, max_players, current_players, dm_name, description,dm_email, dm_phone, dm_discord FROM campaigns WHERE id=?"
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
        sql = "SELECT id, name, current_players, max_players, description FROM campaigns ORDER BY name ASC"
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
    # clear out any previous login state
    session["logged_in"] = False

    # Get the data from the form
    user  = request.form.get("username")
    password = request.form.get("password")

    # Sanitize the text inputs
    user = html.escape(user)
    password = html.escape(password)

    if user == ADMIN_USER and password == ADMIN_PASS:  
        session["logged_in"] = True
        flash("You have been logged in", "success")
        return redirect("/admin_view")
    else:
        flash("Incorrect username or password", "error")
        return redirect("/admin_login")

#-----------------------------------------------------------
# Route for logging out as an admin
#----------------------------------------------------------- 
@app.get("/logout")
def admin_logout():
    session["logged_in"] = False
    flash("You have been logged out", "success")
    return redirect("/")
#-----------------------------------------------------------
# Route for adding a thing, using data posted from a form
#-----------------------------------------------------------
@app.post("/add")
def add_a_campaign():
    # Get the data from the form
    name  = request.form.get("name")
    dm_name = request.form.get("dm_name")
    max_players = request.form.get("max_players")
    current_players = request.form.get("current_players")
    description = request.form.get("description")
    dm_email = request.form.get("dm_email")
    dm_phone = request.form.get("dm_phone")
    dm_discord = request.form.get("dm_discord")

    # Sanitize the text inputs
    name = html.escape(name)
    dm_name = html.escape(dm_name)
    description = html.escape(description)
    dm_email = html.escape(dm_email)
    dm_phone = html.escape(dm_phone)
    dm_discord = html.escape(dm_discord)

    with connect_db() as client:
        # Add the thing to the DB
        sql = "INSERT INTO campaigns (name, dm_name, max_players, current_players, description, dm_email, dm_phone, dm_discord) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        params = [name, dm_name, max_players, current_players, description, dm_email, dm_phone, dm_discord]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"Campaign '{name}' added", "success")
        return redirect("/admin_view")


#-----------------------------------------------------------
# Route for showing editing for a campaign, Id given in the route
#-----------------------------------------------------------
@app.get("/show_edit/<int:id>")
def show_edit_campaign(id):
    with connect_db() as client:
        sql = "SELECT * FROM campaigns WHERE id=?"
        result = client.execute(sql, [id])

        if result.rows:
            campaign = result.rows[0]
            return render_template("pages/edit.jinja", campaign=campaign)
        else:
            return not_found_error()


#-----------------------------------------------------------
# Route for editing a campaign, Id given in the route
#-----------------------------------------------------------
@app.post("/edit/<int:id>")
def edit_campaign(id):
    # Get the data from the form
    name  = request.form.get("name")
    dm_name = request.form.get("dm_name")
    max_players = request.form.get("max_players")
    current_players = request.form.get("current_players")
    description = request.form.get("description")
    dm_email = request.form.get("dm_email")
    dm_phone = request.form.get("dm_phone")
    dm_discord = request.form.get("dm_discord")

    # Sanitize the text inputs
    name = html.escape(name)
    dm_name = html.escape(dm_name)
    description = html.escape(description)
    dm_email = html.escape(dm_email)
    dm_phone = html.escape(dm_phone)
    dm_discord = html.escape(dm_discord)

    with connect_db() as client:
        sql = """
            UPDATE campaigns
            SET name=?, dm_name=?, max_players=?, current_players=?, description=?, dm_email=?, dm_phone=?, dm_discord=?
            WHERE id=?
        """
        params = [name, dm_name, max_players, current_players, description, dm_email, dm_phone, dm_discord, id]
        client.execute(sql, params)

    flash(f"Campaign '{name}' updated successfully!", "success")
    return redirect("/admin_view")




#-----------------------------------------------------------
# Route for deleting a campaign, Id given in the route
#-----------------------------------------------------------
@app.get("/delete/<int:id>")
def confirm_delete(id):
    # Show confirmation template
    return render_template("pages/confirm_delete.jinja", id=id)

@app.post("/delete/<int:id>")
def delete_a_thing(id):
    with connect_db() as client:
        sql = "DELETE FROM campaigns WHERE id=?"
        client.execute(sql, [id])

    flash("Campaign deleted", "success")
    return redirect("/admin_view")



