# Udacity Capstone Project (final project)
    This is the Udacity fulltack Nanodegree program final project. I was giving the choise to to choose what types of project it will be. I choose a `project management` as my project.
    The project have `two` types of users a `manger` and a `member` each user have different role in this application. There are `four  classes` in this project. `Leader`, `Member`, `Project`, and `Task`. The application is authanticated with `Auth0`.
### The Manger Role
    A manger have the role of performing all tasks.
    - A `Manger` can create an acccount him/her self.
    - Add a `Member` to his/her group.
    - create, update and delete a `Project`.
    - create update, delete and a `Task`  and asign it to a project then a member.

### The Member Role
    A member have a limited access he/she can perform.
    - A `Member` can get `Project` information.
    - get `Task` information.
    - update `Task informations.
    -  delete a `Task`.

### key Dependencies
- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Auth0 Requirement
Go the [Auth0](https://auth0.com/) and create a new account or login if you already have an account.
crete new `Application`  and take note of `Domain` name. Go to the `./src/auth/auth.py` add the domain name to the `AUTH0_DOMAIN` varialbe. Once that is done create an `API` application and get the identifer you have giving your API asign it to the `API_AUDIENCE` variable in the same file.


## Running the server
Before start your application make sure you have `python3`  installed and make sure you have `postgres`. From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```
export FLASK_APP=api.py;
```

To run the server, execute:

```
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

