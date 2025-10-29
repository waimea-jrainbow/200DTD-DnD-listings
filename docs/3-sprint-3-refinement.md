# Sprint 3 - A Refined and Complete System


## Sprint Goals

Develop the system until it is fully featured, with a refined UI and it satisfies the requirements. The system will be fully tested at this point.


---

## Updated Database Schema 

I have now realized that i never used second and third tables in my database which means I'm not using linked tables... Gonna have to fix that

![SCREENSHOT OF DB SCHEMA](screenshots/final_db.png)

changed from player details to dm details

will now need to add page for adding dm details on admin page

![SCREENSHOT OF DB SCHEMA](screenshots/final_final_schema.png)

---

## Final Implementation

The web app is fully implemented with a refined UI:

![SCREENSHOT OF IMPLEMENTATION](screenshots/final_implementation/1.png)
![SCREENSHOT OF IMPLEMENTATION](screenshots/final_implementation/2.gif)
![SCREENSHOT OF IMPLEMENTATION](screenshots/final_implementation/3.png)
![SCREENSHOT OF IMPLEMENTATION](screenshots/final_implementation/4.png)
![SCREENSHOT OF IMPLEMENTATION](screenshots/final_implementation/5.png)


---

## Testing User campaign listings

I tested the campaign listings when not logged in, I tested this by using the interfaces and getting my stakeholder to use my interface. 

![SCREENSHOT OF TESTING](screenshots/refined_user_campaign_test.png)

### Changes / Improvements

Made the whole entry for each campaign the button to open the view and changed the text "view" to "click to view"

![SCREENSHOT OF CHANGES](screenshots/refined_user_campaign_changes.png)


---

## Testing User campaign details

Testing campaign details, I tested this by using the interfaces and getting my stakeholder to use my interface. 

![SCREENSHOT OF TESTING](screenshots/refined_user_campaign_details_test.png)


---

## Testing logging in as admin

Tested logging in as admin by logging in and getting end-user to log in

![GIF OF TESTING](screenshots/refined_admin_login_test.gif)


---

## Testing logging out from admin

Tested logging out from admin by logging out and getting end-user to log out

![GIF OF TESTING](screenshots/refined_admin_logout_test.gif)


---

## Testing adding campaign

Tested adding a new campaign by adding a campaign using test data and getting my end-user to do the same

![GIF OF TESTING](screenshots/refined_add_campaign_test.gif)

---

## Testing editing campaign

Tested editing a campaign by editing the name of a pre-existing campaign and getting my end-user to do the same

![GIF OF TESTING](screenshots/refined_edit_campaign_test.gif)

---

## Testing deleting campaign

Tested deleting campaign by deleting a pre-existing campaign and getting my end-user to do the same

![GIF OF TESTING](screenshots/refined_delete_campaign_test.gif)

---

## Testing DM view

Tested viewing DM list by going to the DM page and getting my end-user to test how easy it is to get specific information from it

![SCREENSHOT OF TESTING](screenshots/refined_dm_view_test.png)

---

## Testing adding DM

Tested adding a new DM by entering test data and getting end-user to do the same

![GIF OF TESTING](screenshots/refined_add_dm_test.gif)

---

## Testing editing DM

Tested editing a DM by changing the name of a pre-existing DM and getting my end-user to do the same

![GIF OF TESTING](screenshots/refined_edit_dm_test.gif)

### Changes / Improvements

Changed DM discord to not be required as not all DMs will have discord 

![GIF OF CHANGES](screenshots/refined_edit_dm_change.gif)


---

## Testing deleting DM

Tested deleting a DM by deleting a pre-existing DM and getting my end-user to do the same

![GIF OF CHANGES](screenshots/refined_delete_dm_test.gif)


---


## Testing through validating code

I validated all of my HTML by loading up the page and copying the resultant sourcecode into https://validator.w3.org/#validate_by_input

![SCREENSHOT OF VALIDATION](screenshots/validation_1.png)

### Changes / Improvements

Summarized list of changes:

User home:
- Used forward slash instead of backslash when calling images
- added alt text to logo 
- changed ids for repeated DB listings to classes 
User specific campaign view
- Added h2 title for article
Login page:
- removed space between attributes on cancel button
- removed unnecessary article tags
logout confirmation:
- changed cancel button from type="button" to role="button"
Admin home:
- changed ids for repeated DB listings to classes 
- validator advised that role="button" is not necessary on the summary element however I am using this for pico css styling so I did not change it
- Added a non-selectable option to the drop down input for choosing a DM so the highest id DM isn't selected by default
Campaign edit:
- Added a non-selectable option to the drop down input for choosing a DM so the highest id DM isn't selected by default
- validator advised to have a default non-selectable option for the DM dropdown however since this dropdown is already fulfilled by the DM from the DB this is not necessary
- Moved cancel button into the form to allow for flexbox use which stopped the errors caused by unclosed divs from my earlier attempts using a div from inside the form to outside it
Campaign delete confirmation:
- changed cancel button from type="button" to role="button"
Admin DMs view:
- changed ids for repeated DB listings to classes 
- validator advised that role="button" is not necessary on the summary element however I am using this for pico css styling so I did not change it
Specific DM view:
- removed stray paragraph tag
DM delete confirmation:
- changed cancel button from type="button" to role="button"
DM edit:
- moved cancel button into form and added relevant ids


---

I validated all of my CSS by copying styles.css into https://validator.w3.org/#validate_by_input

![SCREENSHOT OF VALIDATION](screenshots/validation_2.png)

However there were no errors but I made sure to go through and clean up my CSS

## Sprint Review


This sprint went well the testing of the refined system let me work out any last kinks in the code and Validating all my work allowed me to follow convention and to reinforce my code further. Something that didn't go very well was me having little to change across sprint 2 to 3 as much of the needed changes were already done 
