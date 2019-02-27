Remindme is a simply flask app that you can use to remind yourself of anything via an API. 

| HTTP Verb   |      URL Endpoint      |  Action |
|:----------|:-------------|:------|
| POST | /users | register user with params username, password, email. you will receive an API Key you use to create and delete your reminders. |
| POST | /reminders   |  add reminder |
| GET | /reminders |    get reminders |
| GET | /reminders/<ID> |    get reminder with ID |
| PUT | /reminders/<ID> |    update reminder with ID |
| DELETE | /reminders/<ID> |   delete reminder with ID |
