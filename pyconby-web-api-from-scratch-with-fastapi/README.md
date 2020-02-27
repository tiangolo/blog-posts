# Build a web API from scratch with FastAPI - the workshop

Last weekend I had the chance to go to [PyCon Belarus](https://by.pycon.org/), I had a great time and met a lot of great people.

I gave a talk there:

https://twitter.com/Mariacamilagl30/status/1231202275147812864

And a workshop with about 60 people:

https://twitter.com/pyconby/status/1230797331429306368

When creating the workshop I got a bit excited, and created too much content for the time I had available.

The final app ended up having basic OAuth2 authentication, authorization handling with dependencies, tests with full coverage, etc.

I "gave" a test trial of the full workshop to [Camila](https://twitter.com/Mariacamilagl30) and the total time was about 9 hours, it wasn't really possible to give it all in 3 hours.

But as it was made in incremental steps, completing a full new version of the app at every step (or every 2 steps), we could start it and go through it, step by step, and advance as much as possible. And wherever we ended up by the end would still be a valid version of the app.

The speed of a workshop like this has a constant tradeoff, as there's always people that finish some part faster than others, so, at some points some people will be "bored" while others will be stressed finishing some part before the next comes.

But nevertheless, at the workshop in PyCon Belarus developers were quite fast, and we were able to go up to version 8 of the app, while I was expecting to get only up to about version 5.

But there were 15 versions. So, for those that wanted to see the final version, here it is.

I don't have an easy way to provide it step by step with all the explanations here, but if you are curious you can still check here the last version of the code.

It was all based on the same FastAPI documentation, so, if you want to understand it all you can just follow the full [FastAPI Tutorial - User Guide](https://fastapi.tiangolo.com/tutorial/).

Below are the initial setup instructions and then the link to the full code of the last version.

---

## Create a project directory

Create a directory for the project.

For example `./apiapp/`:

```console
$ mkdir apiapp
$ cd ./apiapp/
```

## Create a Python environment

In the `./apiapp/` directory, create a new Python environment.

You could be using Poetry, Pipenv, or other tools.

To make it simple we are going to use pure Python with the `venv` module.

Make sure you have a Python version > 3.6:

```console
$ python --version

# OR

$ python3.6 --version

# OR

$ python3.7 --version
```

Then use that Python 3.6+ to create a new environment for your project.

```console
python -m venv env
```

That will create a directory `./env/` that will contain a full Python environment, with its own packages, etc.

And in that environment is that we are going to install packages and everything.

### Initialize git

```console
$ git init
```

### Ignore that environment in git

Inside of that `./env/` directory, create a file `.gitignore` with the contents:

```
*
```

(that's a single `*` in the file).

That will tell git that we want to ignore everything inside that directory.

### Activate the environment

Now we need to "activate" the environment.

This will tell your terminal that when you try to run `python` it should use the new Python you just installed in that `./env/` directory and not the global one.

Activate the environment:

```console
$ source ./env/bin/activate
```

To make sure that it worked, check which Python binary is used by your terminal.

```console
$ which python
```

It should show the path of the new Python, something like:

```
/home/user/code/apiapp/env/bin/python
```

#### Activate in Windows

If you are in Windows, in Git Bash, activate with:

```console
$ source ./env/Scripts/activate
```

If you are using PowerShell, activate with:

```console
$ .\env\Scripts\Activate.ps1
```

To confirm which Python you have in PowerShell use:

```console
$ Get-Command python
```

#### Deactivate an environment

We don't need to deactivate the environment because we are going to use it. But if you need to deactivate it later, just run:

```console
$ deactivate
```

## Open your editor

Open your editor and select that environment.

### Visual Studio Code

If you have Visual Studio Code and a shell like Bash, you can just run:

```console
$ code ./
```

In any case, make sure you select the environment you just created for your editor.

If you use Visual Studio Code, make sure you have the [Python Extension](https://code.visualstudio.com/docs/python/python-tutorial#_install-visual-studio-code-and-the-python-extension).

You can then create a dummy file `dummy.py` and open it. That will make VS Code load the extension and show the Python environment used.

In the lower left corner you will see the Python version used, if you click it, you can select a different one.

After this, you can delete the `dummy.py` file.

### PyCharm

If you use PyCharm as your editor, open it.

Select your project directory `./apiapp/` as the workspace.

Then [Configure a Python interpreter](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html) for your project, and select the interpreter inside of the environment you just created.

### Using the correct environment

Using the correct environment in your editor as we described here and opening it exactly in your project directory will make your editor know the installed packages and will let it provide autocompletion, type checks, relative imports, etc.

If you didn't configure the environment correctly or if you didn't open it exactly in your project directory (for example, you open one directory above), your editor won't be able to give you all those features.

## Create files

Now, in your editor, create a directory `app`. It will store all your actual code.

Inside of that `app` directory, create 2 empty files `main.py` and `__init__.py`.

And inside of your project directory, right next to the `app` directory, create an empty `requirements.txt` file.

Your file structure should look like:

```
apiapp
├── app
│   ├── __init__.py
│   └── main.py
├── requirements.txt
└── env
    └── ...

```

## Requirements

Edit your `requirements.txt` to have the following contents:

```
fastapi
uvicorn
sqlalchemy
async-exit-stack
async-generator
passlib[bcrypt]
python-jose[cryptography]
python-multipart
python-dotenv
```

### Install requirements

Now install the requirements from that `requirements.txt` file in the terminal with:

```console
$ pip install -r requirements.txt
```

### Dev requirements

Now, to facilitate development, we'll also add extra packages that will help us during development.

Create a file `dev-requirements.txt` with:

```
black
mypy
flake8
requests
pytest
pytest-cov
isort
autoflake
```

### Install dev requirements

And now install the development requirements in the same way:

```console
$ pip install -r dev-requirements.txt
```

### In VS Code

Enable `Language Server`, `mypy`, `black` in the settings.

### Reload editor

You might need to reload your editor for it to be able to detect the newly installed packages.

### Reload environment

Right after installing new Python packages in your environment, you should activate the environment again:

```console
$ source ./env/bin/activate
```

**Note**: If you are on Windows use the equivalent command.

This will ensure that packages that have a command, like `uvicorn` will be available in your terminal.

Make sure that `uvicorn` is available and is the correct version after installing and re-activating the environment:

```console
$ which uvicorn
```

It should show the `uvicorn` from your environment.

### Note: Other package managers

If you used a different environment and package manager like Poetry or Pipenv, the `requirements.txt` file would be a different file and it would be managed differently, but here we are using the simplest version with the pure/standard Python packages (`venv`, `pip`, etc).

## The app - version 1

Now we are going to create the first version of our app.

### Edit - v1

Edit the file `main.py`...

### Run - v1

Run it:

```console
$ uvicorn app.main:app --reload
```

* Edit `main.py` again, Uvicorn auto-reloads.

## Final Version

The final version of the source code is here: https://github.com/tiangolo/blog-posts/tree/master/pyconby-web-api-from-scratch-with-fastapi/apiapp

## Additional scripts

There's a script to run the **tests** and report coverage in HTML so that you can explore it in your browser:

```console
$ bash test.sh
```

And there is a script to **format** all the code automatically:

```console
$ bash format.sh
```
