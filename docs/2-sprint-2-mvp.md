# Sprint 2 - A Minimum Viable Product (MVP)


## Sprint Goals

Develop a bare-bones, working web application that provides the key functionality of the system, then test and refine it so that it can serve as the basis for the final phase of development in Sprint 3.


---

## Implemented Database Schema

Added dm contact info

![SCREENSHOT OF DB SCHEMA](screenshots/drawsql.png)



---

## Initial Implementation

The key functionality of the web app was implemented:

![GIF OF FUNCTIONALITY](screenshots\initial_implementation.gif)


---

## In progress feedback 

1. Add discord usernames of DMs to db as most user in dnd club have discord

![SCREENSHOT OF DB SCHEMA CHANGES](screenshots/dm_discord.png)


2. Add more info e.g. lore document attachment, current level
 
![SCREENSHOT OF DB SCHEMA CHANGES](screenshots/currentlevelanddocs.png)

---

## Testing campaign list


1. be able to view a concise list of campaigns easily as a player

![IMAGE OF FUNCTIONALITY](screenshots\testing_list.png)

### Changes / Improvements

I added the DM name to the information displayed in the main page list 

![IMAGE OF CHANGES](screenshots\change_list.png)


---

## Testing campaign details 

2. Able to view useful details about a specific campaign

![GIF OF FUNCTIONALITY](screenshots\testing_details.gif)

### Changes / Improvements

Centred the details and button

![GIF OF FUNCTIONALITY](screenshots\testing_details.gif)


---

## Testing logging in as admin

Testing ability for admin to log in to edit, add or delete campaigns 


![GIF OF FUNCTIONALITY](screenshots\testing_login.gif)

### changes/improvements

Added cancel button to return to homepage

![GIF OF CHANGES](screenshots\change_login.png)

---

## Testing logging out as admin

Testing ability for admin to log out and return to the homepage

![GIF OF FUNCTIONALITY](screenshots\testing_logout.gif)

### changes/improvements

Added cancel button to return to homepage

![GIF OF CHANGES](screenshots\change_logout.gif)



---

## Testing adding campaign

Testing ability to add campaigns I tested it by adding a campaign. The outcome was pretty good but current players could be more than max players

![GIF OF FUNCTIONALITY](screenshots\testing_add.gif)

### Changes / Improvements

Made DB unable to accept current player greater than max players

![GIF OF CHANGES](screenshots\change_add.gif)


---

## Testing editing campaign

Tested editing a campaign by running through editing a campaign

![GIF OF FUNCTIONALITY](screenshots\testing_edit.gif)

### Changes / Improvements

Added cancel button and placeholder for documents

![IMAGE OF CHANGES](screenshots\change_edit.png)


---

## Testing deleting campaign

Testing deletion of a campaign by deleting a campaign

![GIF OF FUNCTIONALITY](screenshots\testing_delete.gif)




---

## Sprint Review

Replace this text with a statement about how the sprint has moved the project forward - key success point, any things that didn't go so well, etc.

This sprint went pretty great it has taken the project even closer to completion and allowed me to work out some kinks after testing 
A key success point was being able to test the interface and see what worked and what didn't and needed tweaking, a limitation was having to use OBS to screen record on my computer at home as i couldn't get a decent gif recorder on linux and trying to do so wasted a lot of time.

---

Addendum: I have now realized that i never used second and third tables in my database which means I'm not using linked tables... Gonna have to fix that

