# FastAPI top-level dependencies

This article lives in:

* [Dev.to](https://dev.to/tiangolo/)
* [Medium](https://medium.com/@tiangolo/)
* [GitHub](https://github.com/tiangolo/blog-posts/blob/master/fastapi-top-level-dependencies/README.md)

## Intro

FastAPI version `0.62.0` comes with global dependencies that you can apply to a whole application.

As well as top-level dependencies, tags, and other parameters for `APIRouter`s, that before were available only on `app.include_router()`.

This makes it easier to put configurations and dependencies (e.g. for authentication) related to a group of *path operations* more closely together. 🔒

Let's start by checking `APIRouter`...

## Include a router

Imagine you had a file `users.py` with:

```Python
from fastapi import APIRouter

router = APIRouter()


@router.get("/users/")
def read_users():
    return ["rick", "morty"]
```

And now let's say you want to include it in the `main.py` file with:

```Python
from fastapi import FastAPI, Depends
from . import users
from .dependencies import get_query_token

app = FastAPI()

app.include_router(
    users.router,
    tags=["users"],
    dependencies=[Depends(get_query_token)]
)


@app.get("/")
def main():
    return {"message": "Hello World"}
```

In this example, you are applying the tag `users` to all the *path operations* in `users.py`. And you are also applying the dependency `get_query_token` to all of them.

This works, and it was the only/main way to do it up to version 0.62.0.

But what is not so great about it is that the tag and the dependency are mainly related to `users.py`, not to `main.py`. But that code had to live in `main.py`, instead of being closer to what it is related to.

## `APIRouter` top-level dependencies and tags

Now, with FastAPI version `0.62.0`, you can declare top-level dependencies, tags, and others in the `APIRouter` directly.

So, the new `router.py` can now look like:

```Python
from fastapi import APIRouter, Depends
from .dependencies import get_query_token

router = APIRouter(
    tags=["users"],
    dependencies=[Depends(get_query_token)]
)


@router.get("/users/")
def read_users():
    return ["rick", "morty"]
```

...notice the `tags` and `dependencies` in the `APIRouter`, they can now live closer to their related code! 🎉

And the `main.py` would be simply:

```Python
from fastapi import FastAPI
from . import users

app = FastAPI()

app.include_router(
    users.router,
)


@app.get("/")
def main():
    return {"message": "Hello World"}
```

## Global dependencies

The same way, you can now also declare `dependencies` that apply to **all** the *path operations* in the `FastAPI` application:

```Python
from fastapi import FastAPI, Depends
from .dependencies import get_query_token

app = FastAPI(
    dependencies=[Depends(get_query_token)]
)

@app.get("/")
def main():
    return {"message": "Hello World"}
```

## Tips

Some tips to adopt a convention:

* By default, set all those configs in `APIRouter()`.
* Try to **only** set them in `app.include_router()` when you want to override some defaults that can't (or shouldn't) be set in `APIRouter` directly.
* Set them in `FastAPI()` only when you want them to apply to everything, e.g. some default authentication for a simple app.

## Learn More

You can read more about [global dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/).

And about [`APIRouter` top-level `dependencies`, `tags`, and others](https://fastapi.tiangolo.com/tutorial/bigger-applications/).

If you don't want to miss other news, you can subscribe to the [**FastAPI and friends** official newsletter](https://fastapi.tiangolo.com/newsletter/). 🎉

## About me

Hey! 👋 I'm [tiangolo (Sebastián Ramírez)](https://tiangolo.com).

You can follow me, contact me, see what I do, or use my open source code:

* [GitHub: tiangolo](https://github.com/tiangolo)
* [Twitter: tiangolo](https://twitter.com/tiangolo)
* [LinkedIn: tiangolo](https://www.linkedin.com/in/tiangolo/)
* [Dev: tiangolo.to](https://dev.to/tiangolo)
* [Medium: tiangolo](https://medium.com/@tiangolo)
* [Web: tiangolo.com](https://tiangolo.com)
