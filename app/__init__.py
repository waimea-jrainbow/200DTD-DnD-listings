#===========================================================
# DnD listings
# Jaxon Rainbow
#-----------------------------------------------------------
# This site will allow users to view DnD campaigns and
# allow DMs to list their campaigns for players to find.
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

load_dotenv()

# Load environment variables from the .env file
ADMIN_USER = getenv("ADMIN_USER")
ADMIN_PASS = getenv("ADMIN_PASS")


#----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def show_all_things():
    with connect_db() as client:
        # Get all the campaigns from the DB
        sql =  """SELECT 
                campaigns.id, 
                campaigns.name, 
                campaigns.max_players, 
                campaigns.current_players, 
                dms.dm_name
            
            FROM campaigns 
            JOIN dms on campaigns.dm_id = dms.dm_id
            ORDER BY campaigns.name ASC
            """
        params = []
        result = client.execute(sql, params)
        campaigns = result.rows

        

        # Did we get a result?
        if result.rows:
            # yes, so show it on the page
            campaigns = result.rows
            return render_template("pages/user_home.jinja", campaigns=campaigns)
        else:
            # No, so show error
            return not_found_error()


#-----------------------------------------------------------
# campaign page route - Show details of a single campaign
#-----------------------------------------------------------
@app.get("/campaign/<int:id>")
def show_one_campaign(id):
    with connect_db() as client:
        # Get the campaign details from the DB
        sql = """
            SELECT 
                campaigns.id, 
                campaigns.name, 
                campaigns.max_players, 
                campaigns.current_players, 
                campaigns.description, 
                campaigns.current_level, 
                campaigns.docs_link1, 
                campaigns.docs_link2, 
                campaigns.docs_link3, 
                campaigns.docs_link4, 
                campaigns.docs_link5,
                dms.dm_name, 
                dms.dm_phone, 
                dms.dm_email, 
                dms.dm_discord
            
            FROM campaigns 
            JOIN dms on campaigns.dm_id = dms.dm_id
            WHERE id=?
        """
        params = [id]
        result = client.execute(sql, params)

        # Did we get a result?
        if result.rows:
            # yes, so show it on the page
            campaign = result.rows[0]
            return render_template("pages/user_campaign.jinja", campaign=campaign)
        else:
            # No, so show error
            return not_found_error()

#-----------------------------------------------------------
# dm page route - Show details of a single campaign
#-----------------------------------------------------------
@app.get("/dm/<int:id>")
def show_one_dm(id):
    with connect_db() as client:
        # Get the campaign details from the DB
        sql = "SELECT dm_id, dm_name, dm_email, dm_phone, dm_discord FROM dms WHERE dm_id=?"
        params = [id]
        result = client.execute(sql, params)

        # Did we get a result?
        if result.rows:
            # yes, so show it on the page
            dm = result.rows[0]

            # Get the campaign details from the DB
            sql = "SELECT id, name FROM campaigns WHERE dm_id=?"
            params = [id]
            result = client.execute(sql, params)
            campaigns = result.rows

            return render_template("pages/admin_dm.jinja", dm=dm, campaigns=campaigns)
                                   
        else:
            # No, so show error
            return not_found_error()
        


#-----------------------------------------------------------
# Admin view page route - Show all the campaigns with the ability to edit and delete current campaigns and add new ones through a form
#-----------------------------------------------------------
@app.get("/admin_home")
def show_all_admin():
    with connect_db() as client:
        # Get all the campaigns from the DB
        sql = "SELECT id, name FROM campaigns ORDER BY name ASC"
        params = []
        result = client.execute(sql, params)
        campaigns = result.rows

        sql = "SELECT dm_id, dm_name FROM dms"
        params = []
        result = client.execute(sql, params)
        dms = result.rows

        # And show them on the page
        return render_template("pages/admin_home.jinja", campaigns=campaigns, dms=dms)


#-----------------------------------------------------------
# Admin login page route
#-----------------------------------------------------------
@app.get("/admin_login")
def show_login_page():
    return render_template("pages/admin_login.jinja")


#-----------------------------------------------------------
# Route for logging in and out as an admin using data posted from a form
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
        return redirect("/admin_home")
    else:
        flash("Incorrect username or password", "error")
        return redirect("/admin_login")


@app.get("/confirm_logout")
def confirm_logout():
    # Show confirmation page
    return render_template("pages/admin_confirm_logout.jinja")


@app.post("/logout")
def admin_logout():
    session["logged_in"] = False
    flash("You have been logged out", "success")
    return redirect("/")


#-----------------------------------------------------------
# Route for adding a campaign
#-----------------------------------------------------------
@app.post("/add")
def add_a_campaign():
    # Get the data from the form
    name  = request.form.get("name")
    dm_id = request.form.get("dm_id")
    max_players = int(request.form.get("max_players"))
    current_players = int(request.form.get("current_players"))
    description = request.form.get("description")
    current_level = request.form.get("current_level")
    docs_link1 = request.form.get("docs_link1")
    docs_link2 = request.form.get("docs_link2")
    docs_link3 = request.form.get("docs_link3")
    docs_link4 = request.form.get("docs_link4")
    docs_link5 = request.form.get("docs_link5")

    # Validation: ensure current players ≤ max players
    if current_players > max_players:
        flash("Current players cannot be greater than max players.", "error")
        return redirect("/admin_view")

    # Sanitize the text inputs
    name = html.escape(name)
    description = html.escape(description)
    
    with connect_db() as client:
        # Add the campaign to the DB
        sql = """
            INSERT INTO campaigns 
            (name, dm_id, max_players, current_players, description, docs_link1, docs_link2, docs_link3, docs_link4, docs_link5, current_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = [name, dm_id, max_players, current_players, description,
                  docs_link1, docs_link2, docs_link3, docs_link4, docs_link5, current_level]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"Campaign '{name}' added", "success")
        return redirect("/admin_home")


#-----------------------------------------------------------
# Route for showing the edit page for a campaign
#-----------------------------------------------------------
@app.get("/show_edit/<int:id>")
def show_edit_campaign(id):
    with connect_db() as client:
        sql = "SELECT * FROM campaigns WHERE id=?"
        result = client.execute(sql, [id])
        campaign = result.rows[0]
        sql = "SELECT dm_id, dm_name FROM dms"
        params = []
        result = client.execute(sql, params)
        dms = result.rows

        # And show them on the page
        return render_template("pages/admin_edit_campaign.jinja", campaign=campaign,  dms=dms)

        
#-----------------------------------------------------------
# Route for showing the edit page for a dm
#-----------------------------------------------------------
@app.get("/show_edit_dm/<int:id>")
def show_edit_dm(id):
    with connect_db() as client:
        sql = "SELECT * FROM dms WHERE dm_id=?"
        result = client.execute(sql, [id])

        if result.rows:
            dm = result.rows[0]
            return render_template("pages/admin_edit_dm.jinja", dm=dm)
        else:
            return not_found_error()


#-----------------------------------------------------------
# Route for editing a campaign
#-----------------------------------------------------------
@app.post("/edit/<int:id>")
def edit_campaign(id):
    # Get the data from the form
    name  = request.form.get("name")
    dm_id = request.form.get("dm_id")
    max_players = request.form.get("max_players")
    current_players = request.form.get("current_players")
    description = request.form.get("description")
    current_level = request.form.get("current_level")
    docs_link1 = request.form.get("docs_link1")
    docs_link2 = request.form.get("docs_link2")
    docs_link3 = request.form.get("docs_link3")
    docs_link4 = request.form.get("docs_link4")
    docs_link5 = request.form.get("docs_link5")

    # Sanitize text inputs
    name = html.escape(name)
    dm_id = html.escape(dm_id)
    description = html.escape(description)
    docs_link1 = html.escape(docs_link1)
    docs_link2 = html.escape(docs_link2)
    docs_link3 = html.escape(docs_link3)
    docs_link4 = html.escape(docs_link4)
    docs_link5 = html.escape(docs_link5)

    with connect_db() as client:
        sql = """
            UPDATE campaigns
            SET name=?, dm_id=?, max_players=?, current_players=?, description=?, current_level=?, docs_link1=?, docs_link2=?, docs_link3=?, docs_link4=?, docs_link5=?
            WHERE id=?
        """
        params = [name, dm_id, max_players, current_players, description,
                  current_level, docs_link1, docs_link2, docs_link3, docs_link4, docs_link5, id]
        client.execute(sql, params)
    
    if int(current_players) > int(max_players):
        flash("Current players cannot be greater than max players.", "error")
        return redirect(f"/show_edit/{id}")
    
    flash(f"Campaign '{name}' updated successfully!", "success")
    return redirect("/admin_home")

#-----------------------------------------------------------
# Route for editing a dm
#-----------------------------------------------------------
@app.post("/edit_dm/<int:id>")
def edit_dm(id):
    # Get the data from the form
    dm_name = request.form.get("dm_name")
    dm_email = request.form.get("dm_email")
    dm_phone = request.form.get("dm_phone")
    dm_discord = request.form.get("dm_discord")


    # Sanitize text inputs
    dm_name = html.escape(dm_name)
    dm_email = html.escape(dm_email)
    dm_phone = html.escape(dm_phone)
    dm_discord = html.escape(dm_discord)
    

    with connect_db() as client:
        sql = """
            UPDATE dms
            SET dm_name=?, dm_email=?, dm_phone=?, dm_discord=?
            WHERE dm_id=?
        """
        params = [dm_name, dm_email, dm_phone, dm_discord, id]
        client.execute(sql, params)
    
    
    flash(f"Campaign '{dm_name}' updated successfully!", "success")
    return redirect("/admin_dms")

#-----------------------------------------------------------
# Route for deleting a campaign
#-----------------------------------------------------------
@app.get("/admin_confirm_delete_campaign/<int:id>")
def confirm_delete_campaign(id):
    # Show confirmation template
    return render_template("pages/admin_confirm_delete.jinja", id=id)


@app.post("/delete/<int:id>")
def delete_a_campaign(id):
    with connect_db() as client:
        sql = "DELETE FROM campaigns WHERE id=?"
        client.execute(sql, [id])

    flash("Campaign deleted", "success")
    return redirect("/admin_home")


#-----------------------------------------------------------
# Route for deleting a DM
#-----------------------------------------------------------
@app.get("/admin_confirm_delete_dm/<int:id>")
def confirm_delete_dm(id):
    # Show confirmation template
    return render_template("pages/admin_confirm_delete_dm.jinja", id=id)


@app.post("/delete_dm/<int:id>")
def delete_a_dm(id):
    with connect_db() as client:
        sql = "DELETE FROM dms WHERE dm_id=?"
        client.execute(sql, [id])

    flash("Dungeon Master deleted", "success")
    return redirect("/admin_dms")




#-----------------------------------------------------------
# Route for rendering dm list
#-----------------------------------------------------------
@app.get("/admin_dms")
def show_all_admin_dms():
    with connect_db() as client:
        # Get all the dms from the DB
        sql = "SELECT dm_id, dm_name FROM dms ORDER BY dm_name ASC"
        params = []
        result = client.execute(sql, params)
        DMs = result.rows

        # And show them on the page
        return render_template("pages/admin_dms.jinja", DMs=DMs)


#-----------------------------------------------------------
# Route for adding a DM
#-----------------------------------------------------------
@app.post("/add_dm")
def add_a_dm():
    # Get the data from the form
    dm_name = request.form.get("dm_name")
    dm_email = request.form.get("dm_email")
    dm_phone = request.form.get("dm_phone")
    dm_discord = request.form.get("dm_discord")
    

    # Sanitize the text inputs
    dm_name = html.escape(dm_name)
    dm_email = html.escape(dm_email)
    dm_discord = html.escape(dm_discord)
    
    with connect_db() as client:
        # Add the campaign to the DB
        sql = """
            INSERT INTO dms
            (dm_name, dm_email, dm_phone, dm_discord)
            VALUES (?, ?, ?, ?)
        """
        params = [dm_name, dm_email, dm_phone, dm_discord]
        client.execute(sql, params)

        # Go back to the home page
        flash(f"Dungeon Master '{dm_name}' added", "success")
        return redirect("/admin_dms")


#-----------------------------------------------------------
# Run the Flask app
#-----------------------------------------------------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
