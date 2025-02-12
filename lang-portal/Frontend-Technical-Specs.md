# Frontend Technical Spec
## Pages

### Dashboard `/dashboard`

#### Purpose
The purpose of this page is to provide a summary of the user's progress in learning the language.


#### Components
This page contains the following components:
- Last Study Session
  - shows last activity used
  - shows when last activity used
  - summarizes wrog vs correct from last activity
  - has a link to the group
- Study Progress
  - total words study eg. 3/124
    - across all study session show the total words studied out of all possible words in our database
    - display a mastery progress eg. 0%
    
- Quick Stats
  - success rate eg. 80%
  - total study sessions eg. 4
  - total active groups eg. 3
  - study streak eg. 4 days 

- Start Studying Button
  - goes to study activies page

#### Needed API Endpoints
- GET /api/dashboard/last_study_session
- GET /api/dashboard/study_progress
- GET /api/dashboard/quick_stats

### Study Activities `/study-activities`

#### Purpose
The purpose of this page is to show a collections of study activities with a thumbnail and its name, to either launch or view the study activity.

#### Components

- Study Activity Card
  - show a thumbnail of the study activity
  - the name of the study activity
  - a launch button to take us to the launch page
  - the view page to view more information about past study sessions for this study activity

#### Needed API Endpoints

- GET /api/study-activities

### Study Activity Show `/study-activities/:id`

#### Purpose 
The purpose of this page is to show the details of a study activity and its past study sessions.

#### Components
- Name of the study activity
- Thumbnail of study activity
- Description of study activity
- Launch button
- Study Activities Paginated List
  - id
  - activity name
  - group name
  - start time
  - end time (inferred by the last word_review_item submitted)
  - number of review items

#### Needed API Endpoints
- GET /api/study-activities/:id
- GET /api/study-activities/:id/study_sessions

### Study Activity Launch `/study-activities/:id/launch`

#### Purpose
The purpose of this page is to launch a study activity.

#### Components
- Name of the study activity
- Launch form
  - select field for group
  - launch now button

#### Behavior
After the form is submitted, a new tab opens with the study activity based on its URL provided in the database.
Also the after form is submitted the page will redirect to the study session show page.

#### Needed API Endpoints
- POST /api/study-activities

### Words `/words`

#### Purpose
The purpose of this page is to show all the words in our database.

#### Components
- Paginated Word List
  - Fields
    - Spanish
    - English
    - Correct count
    - Wrong count
  - Pagination with 100 ites per page
  - Clicking the Spanish word will take us to the word show page

#### Needed API Endpoints
- GET /api/words


### Word Show `/words/:id`

#### Purpose
The purpose of this page is to show the details of a specific word.

#### Components
- Spanish
- English
- Study Statistics
  - Correct count
  - Wrong count
- Word Groups
  - show a series of pills eg. tags
  - when group name is clicked it will take you to the group show page

#### Needed API Endpoints
- GET /api/words/:id

### Word Groups `/groups`

#### Purpose
The purpose of this page is to show  a list of groups in our database

#### Components
- Paginated Group List
  - Fields
    - Name
    - Word count
  - Clicking the group name will take us to the group show page

#### Needed API Endpoints
- GET /api/groups

### Group Show `/groups/:id`

#### Purpose
The purpose of this page is to show  a specific group

#### Components
- Group Name
- Statistics
  - Total Word count
- Words in Group (Paginated List of Words)
  - Should use the same component as the word index page
- Study Sessions (Paginated List of Study Sessions)
  - Should use the same component as the study index page


#### Needed API Endpoints
- GET /api/groups/:id (The name and group stats)
- GET /api/groups/:id/words 
- GET /api/groups/:id/study_sessions 

### Study Session Index `/study-sessions`

#### Purpose
The purpose of this page is to show  a list of study sessions in our database

#### Components
- Paginated Study Session List
  - Fields
    - Id
    - Activity Name
    - Group Name
    - Start Time
    - End Time
    - Number of Review Items
  - Clicking the study session will take us to the study session show page

#### Needed API Endpoints
- GET /api/study-sessions


### Study Session Show `/study-sessions/:id`


#### Purpose
The purpose of this page is to show  a specific study session


#### Components
- Study Session Details
  - Activity Name
  - Group Name
  - Start Time
  - End Time
  - Number of Review Items
- Word Review Items (Paginated List of Word Review Items)
  - Should use the same component as the word review page

#### Needed API Endpoints
- GET /api/study-sessions/:id
- GET /api/study-sessions/:id/words


### Settings Page `/settings`
#### Components
- Theme Selector 
  - Allows the user to select their preferred theme, either light or dark.
- Reset History Button
  - Delete all the study sessions and word review items.
- Full Reset Button
  - this will drop all data from the database and recreate with initial data.