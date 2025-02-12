# Backend Technical Specs

## Business Goal:
A language learning school wants to build a prototype of learning portal which will act as three things:
- Inventory of possible vocabulary
- Act as a Learning record store (LRS), providing correct and wrong score on practice vocabulary
- A unified launchpad to launch different learning apps

## Technical Requirements:
- Backend with Python
- Database with SQLite3
- The API will be written with FastAPI
- The API will will always return JSON
- There will be no authentication or authorization
- There will be a single user

## Directory Structure

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── api.py
│   └── models.py
├── requirements.txt
└── README.md
```
## Database Schema
Our database will be a single sqlite database called `words.db` that will be in the root of the project folder of `backend`


We have the following tables:
- words - stored vocabulary words

    | Column  | Type      |
    |---------|-----------|
    | id      | integer   |
    | spanish |  string   |
    | english |  string   |
    | parts   | json      |
- words_groups - join table for words and groups many-to-many

    | Column  | Type      |
    |---------|-----------|
    | id      | integer   |
    | word_id |  integer   |
    | group_id |  integer   |

- groups - thematic group of words

    | Column  | Type      |
    |---------|-----------|
    | id      | integer   |
    | name    |  string   |

- study_sessions - records of study sessions grouping word_review_items

    | Column  | Type      |
    |---------|-----------|
    | id |  integer   | 
    | group_id   | integer      |
    | created_at   | datetime      |
    | study_activity_id | integer |

- word_review_items - a record of word practice, determining if the word was correct or not

    | Column  | Type      |
    |---------|-----------|
    | word_id |  integer   |
    | study_session_id |  integer   |
    | correct   | boolean      |
    | created_at   | datetime      |

- study_activities - records of study activities grouping study sessions

    | Column  | Type      |
    |---------|-----------|
    | id      | integer   |
    | study_session_id |  integer   |
    | group_id   | integer      |
    | created_at   | datetime      |



### API Endpoints

##### GET /api/dashboard/last_study_session
Returns information about the most recent study session.

Response:
```json
{
  "id": 123,
  "activity_name": "Vocabulary Quiz",
  "group_name": "Basic Vocabulary",
  "created_at": "2025-02-11T22:00:00Z",
  "study_activity_id": 456,
  "group_id": 1,
  "correct_count": 8,
  "incorrect_count": 2,
  "total_items": 10
}
```

#### GET /api/dashboard/study_progress
Returns the study progress statistics that will be showed with progress bar in the frontend.

Response:
```json
{
  "total_words_studied": 150,
  "total_available_words": 200,
  "mastery_percentage": 75
}
```

#### GET /api/dashboard/quick_stats
Returns quick statistics about the user's learning progress.

Response:
```json
{
  "success_rate": 80,
  "total_study_sessions": 4,
  "total_active_groups": 3,
  "study_streak_days": 4
}
```

#### GET /api/study-activities
Returns a list of available study activities.

Response:
```json
{
  "study_activities": [
    {
      "id": 456,
      "name": "Vocabulary Quiz",
      "thumbnail_url": "https://example.com/thumbnail.png",
      "description": "Practice vocabulary with flashcards",
      "launch_url": "https://example.com/activities/vocab-quiz"
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 100,
    "items_per_page": 10
  }
}
```

#### GET /api/study-activities/:id
Returns details of a specific study activity.

Response:
```json
{
  "id": 456,
  "name": "Vocabulary Quiz",
  "thumbnail_url": "https://example.com/thumbnail.png",
  "description": "Practice vocabulary with flashcards",
  "launch_url": "https://example.com/activities/vocab-quiz"
}
```

#### GET /api/study-activities/:id/study_sessions
Returns all study sessions for a specific study activity.

Response:
```json
{
  "study_sessions": [
    {
      "id": 789,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Basic Greetings",
      "start_time": "2024-10-19T12:00:00Z",
      "end_time": "2024-10-19T12:30:00Z",
      "review_items_count": 10
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 10,
    "total_items": 100,
    "items_per_page": 10
  }
}
```

#### POST /api/study-activities
Creates a new study activity session.

Request:
```json
{
  "group_id": 1,
  "study_activity_id": 456
}
```

Response:
```json
{
  "id": 789,
  "group_id": 1,
  "study_activity_id": 456,
  "created_at": "2024-10-19T12:00:00Z",
  "launch_url": "https://example.com/activities/vocab-quiz?session=789"
}
```

#### GET /api/words
Returns a paginated list of all words.

Response:
```json
{
  "items": [
    {
      "spanish": "hola", 
      "english": "hello",
      "correct_count": 5,
      "wrong_count": 2
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 500,
    "items_per_page": 100
  }
}
}
```

#### GET /api/words/:id
Returns details of a specific word.

Response:
```json
{
  "spanish": "hola",
  "english": "hello",
  "stats": {
    "correct_count": 5,
    "wrong_count": 2
  },
  "groups": [
    {
      "id": 1,
      "name": "Basic Greetings"
    }
  ]
}
```

#### GET /api/groups
Returns a paginated list of all word groups.

Response:
```json
{
  "items": [
    {
      "id": 1,
      "name": "Basic Greetings",
      "word_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 10,
    "items_per_page": 100
  }
}
```

#### GET /api/groups/:id
Returns details of a specific group.

Response:
```json
{
  "id": 1,
  "name": "Basic Greetings",
  "stats": {
    "total_word_count": 20
  }
}
```

#### GET /api/groups/:id/words
Returns all words in a specific group.

Response:
```json
{
  "items": [
    {
      "spanish": "hola",
      "english": "hello",
      "correct_count": 5,
      "wrong_count": 2
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 20,
    "items_per_page": 100
  }
}
```

#### GET /api/groups/:id/study_sessions
Returns all study sessions for a specific group.

Response:
```json
{
  "items": [
    {
      "id": 789,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Basic Greetings",
      "start_time": "2025-02-08T17:20:23-05:00",
      "end_time": "2025-02-08T17:30:23-05:00",
      "review_items_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 5,
    "items_per_page": 100
  }
}
```

#### GET /api/study-sessions
Returns a paginated list of all study sessions.

Response:
```json
{
  "items": [
    {
      "id": 123,
      "activity_name": "Vocabulary Quiz",
      "group_name": "Basic Greetings",
      "start_time": "2025-02-08T17:20:23-05:00",
      "end_time": "2025-02-08T17:30:23-05:00",
      "review_items_count": 20
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 5,
    "total_items": 100,
    "items_per_page": 100
  }
}
```

#### GET /api/study-sessions/:id
Returns details of a specific study session.

Response:
```json
{
  "id": 123,
  "activity_name": "Vocabulary Quiz",
  "group_name": "Basic Greetings",
  "start_time": "2025-02-08T17:20:23-05:00",
  "end_time": "2025-02-08T17:30:23-05:00",
  "review_items_count": 20
}
```

#### GET /api/study-sessions/:id/words
Returns all words reviewed in a specific study session.

Response:
```json
{
  "items": [
    {
      "spanish": "hola",
      "english": "hello",
      "correct_count": 5,
      "wrong_count": 2
    }
  ],
  "pagination": {
    "current_page": 1,
    "total_pages": 1,
    "total_items": 20,
    "items_per_page": 100
  }
}
```


## Task Runner Tasks

Lets list out possible tasks we need for our lang portal.

### Initialize Database
This task will initialize the sqlite database called `words.db

### Migrate Database
This task will run a series of migrations sql files on the database

Migrations live in the `migrations` folder.
The migration files will be run in order of their file name.
The file names should looks like this:

```text
0001_init.sql
0002_create_words_table.sql
```

### Seed Data
This task will import json files and transform them into target data for our database.

All seed files live in the `seeds` folder.

In our task we should have DSL to specific each seed file and its expected group word name.

```json
[
  {
    "spanish": "viajar",
    "english": "to travel",
  },
  ...
]
```