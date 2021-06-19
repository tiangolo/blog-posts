# The Future of FastAPI and Pydantic is Bright

This article lives in:

* [Dev.to](https://dev.to/tiangolo/)
* [Medium](https://tiangolo.medium.com/)
* [GitHub](https://github.com/tiangolo/blog-posts/blob/master/the-future-of-fastapi-and-pydantic-is-bright/README.md)

## In very short

The future of [FastAPI](https://fastapi.tiangolo.com/) and [Pydantic](https://pydantic-docs.helpmanual.io/) is bright. ✨

This is because we all, as the Python community, define their future. To help us and to help others. From the Core Developers making Python itself to the new developers that started learning Python this month.

And as long as these tools are helping us all solve problems, help ourselves, help others, and be more efficient and productive,  we all will keep them working and improving.

And that's what we are all doing. 🤓🚀

## Intro

You might have heard not long ago about PEP 563, PEP 649, and some changes that could affect Pydantic and FastAPI in the future.

If you read about it, I wouldn't expect you to understand what all that meant. I didn't fully understand it until I spent hours reading all the related content and doing multiple experiments.

It might have worried you and maybe confuse you a bit.

Now there's nothing to be worried about. But still, here I want to help clarify all that and give you a bit more context.

Brace yourself, you are about to learn a bit more about how Python works, how FastAPI and Pydantic work, how type annotations work, and more. 👇

## Details

### Start with a basic FastAPI app

FastAPI is based on Pydantic. Let's see a simple example using them both.

Imagine that we have a file `./main.py` with the following code:

```python
from typing import Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


app = FastAPI()

@app.post("/items/")
def create_item(item: Item):
    return item


if __name__ == "__main__":
    uvicorn.run(app)
```

You could run this example and start the API application with:

```console
$ python ./main.py

INFO:     Started server process [4418]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Then you could open your browser and interact with the API docs at `http://127.0.0.1:8000/docs`, etc.

But here we want to focus on what happens behind the scenes.

**Note**: Instead of using the last two lines, you could have used the `uvicorn` command, and that's what you would normally do. But for this example it will be useful to see everything from the point of view of the `python` command.

### How Python works

By running that command above, you are asking your system to start the program called `python`. And to give it the file `main.py` as a parameter.

**Note**: In Windows, the program might be called `python.exe` instead of just `python`.

That program called `python` (or `python.exe`) is written in another programming language called "C". Maybe you knew that.

And what that program `python` does is read the file `main.py`, interpret the code that we wrote in it using the **Python** Programming Language, and execute it step by step.

So, we have two things with more or less the same name "python" that represent something slightly different:

* `python`: the program that runs our code (which is actually written in the **C** programming language)
* "Python": the name of the programming language we use to write our code

So, you could say that `python` (the program) can read **Python** (the programming language).

### What is Runtime

Now, when that program `python` is executing our code written in the **Python** programming language, we call that "runtime".

It's just the period of time when it is executing our code.

When our code is not being executed, for example, when we are editing the file `./main.py`, it is not *running*, so we are not at **runtime**.

The way that program works is that, at runtime (when our code is being executed), Pydantic and FastAPI read those **type annotations** (or **type hints**) to extract their data and do things with it.

So, for example, in the `Item` class above, we have:

```python
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
```

At **runtime**, Pydantic and FastAPI will see that `name` is a `str` and `price` is a `float`. And if we send a JSON request with a `price` that is not a `float`, they will be able to validate the data for us.

FastAPI and Pydantic are written in pure **Python**. How can these tools do that? **Python** is so powerful that it has features to allow exactly that, to read type annotations at runtime from the same **Python** code. And Pydantic and FastAPI take advantage of those features.

Another term commonly used to refer to doing things at **runtime** is to do things **dynamically**.

### What is Static Analysis

The counterpart of **runtime**, would be **static**. It just means that the code is not being executed. It's treated just as a text file containing code.

In many cases, "static" is used when saying **Static Analysis**, **Static Checking**, **Static Type Checking**, etc. It refers to tools that understand the rules of the **Python** Programming Language and that can analyze the code, but that don't execute the code itself.

These tools for **static analysis** can check if the code is following the rules correctly, checking that the code is valid, providing autocompletion, and other features. When you are editing code and your editor shows a squiggly red line with an error somewhere, that is **static analysis**.

In some cases, the code could be valid, but it would still be incorrect. For example, if you try to add a `str` and a `float` together:

```python
name = "Rick"
price = 1.99

total = name + price
```

In terms of the rules of the language itself, the code is valid, all the quotes are where they should be, the equal signs are correctly placed, etc. But this code is still incorrect and will not work because you can't add a `str` with a `float`.

Many editors will be able to show you a very valuable squiggly red line with the error message under `name + price` that might save you hours debugging. That is also **static analysis**.

Some tools that do **static analysis** and that you might have heard of are:

* **`mypy`**, the official and main **Static Type Checker**
* **`flake8`**, checks for style and correctness
* **`black`**, autoformats the code in a consistent way that improves efficiency
* **PyCharm**, one of the most popular Python editors, has internal components that do **static analysis** to check for errors, provide autocompletion, etc.
* **VS Code**, the other of the most popular Python editors, using Pylance, also has internal tools to do **static analysis** to check for errors, provide autocompletion, etc.

These tools have saved tons of development hours by detecting many bugs earlier in the development process and in the exact place where those errors happened. I bet that in many cases you might have seen the red line, realize what the error is, think "ah, yeah, right", fix it, and not even consider that *there was a bug in your code*, even for some seconds. If I counted all the times these tools have saved me from these bugs, I would get overwhelmed quickly. 😅

And if you have ever added type annotations to a code base that didn't have them before, you probably would have seen lots of broken sections in the code base and broken corner cases, that were suddenly obvious and you could then fix them. I surely have.

### Type Annotations in Python

The **Type Annotations** (also called **Type Hints**) that we have available in all the supported modern Python versions (Python 3.6 and above) were designed to improve all that **static analysis**.

The original intention was to allow `mypy` and others to help developers while *writing* the code. And that was the main focus for a while.

But then tools like `dataclasses` (from the standard library) and [Samuel Colvin](https://twitter.com/samuel_colvin)'s Pydantic started using these type annotations to do more than only **static analysis**, and to use these same **type annotations** at **runtime**. In the case of Pydantic, to extract that information to do data conversion, validation, and documentation.

### Type Annotations with Forward References

Now, imagine we have a class (it could be a Pydantic model) like this:

```python
from typing import Optional

from pydantic import BaseModel


class Person(BaseModel):
    name: str
    child: Optional[Person] = None
```

Here we have a `Person` that could have a child, that would also be a `Person`. It all looks fine, right?

But now when we run the code (or with the help of some static analysis in editors) we will see that we declared `child: Optional[Person]` inside the body of the class `Person`. So, when that part of the code is run by `python`, the `Person` inside of `name: Optional[Person]` doesn't exist yet (that class is still being created).

This is called a **Forward Reference**. And it would make the code break.

And again, the main purpose of these type annotations was to help with **static analysis**. Using them at runtime was not yet an important use case.

And having the code break just because we are trying to improve static analysis would be very annoying.

To overcome that problem, it's also valid to declare that internal `Person` as a literal string, like this:

```python
from typing import Optional

from pydantic import BaseModel

class Person(BaseModel):
    name: str
    child: Optional["Person"] = None
```

That looked weird to me when I discovered it. It's the name of a class just put there inside a string. But it's valid.

When `python` is running, it will see that as a literal string, so it will not break.

And most static analysis tools know this is valid and will read the literal string and understand that it actually refers to the `Person` class.

By knowing that the `Optional["Person"]` actually refers to the `Person` class, static analysis tools can, for example, detect that this would be an error:

```python
parent = Person(name="Beth")

parent.child = 3
```

A smart editor will use its static analysis tools to detect that `parent.child = 3` is an error because it expects a `Person`.

This solves the problem of the forward reference in the code and allows us to still use static analysis tools.

...we are not talking about using these type annotations at **runtime** yet, but we'll get there later.

### PEPs in Python

PEP stands for **Python Enhancement Proposal**. A PEP is a technical document describing changes to Python, additions to the standard library (for example, adding `dataclasses`), and other types of changes. Or in some cases, they just provide information and establish conventions.

The name says **Proposal**, but when they are finally accepted they become a standard.

### PEP 563 - Postponed Evaluation of Annotations

Knowing what's a PEP, let's go back to the code example above.

If you hadn't seen something like the `Optional["Person"]` part before, you might have cringed a bit. I did the first time I discovered that was valid, but it was understandable as it would solve the problem.

Then [Łukasz Langa](https://twitter.com/llanga) had a smart idea and wrote [PEP 563](https://www.python.org/dev/peps/pep-0563/).

If the way type annotations were interpreted changed, and if they were *implicitly* understood by Python as if they were all just strings, then we would not have to put all those classes inside strings in strange places in our code.

So, we would write our code like:

```python
from typing import Optional

from pydantic import BaseModel

class Person(BaseModel):
    name: str
    child: Optional[Person] = None
```

And then whenever `python` read our file `./main.py` it would see it as if it was written like this:

```python
from typing import Optional

from pydantic import BaseModel

class Person(BaseModel):
    name: "str"
    child: "Optional[Person]" = None
```

So, `python` would run our code happily and without breaking.

And we, the developers would be much happier not having to remember where to put things inside strings and where not.

And we would be able to keep using autocompletion and type checks even in these type annotations with forward references. For example, triggering autocompletion inside a string, with the previous technique, might not always work, but with this change that wouldn't be a problem anymore.

And in the case that some tool ended up using these type annotations at runtime for other reasons, there where still ways to get the information at runtime, with some *small caveats*, but it was still possible.

**Spoiler Alert**: These *small caveats* are what later would become a cumbersome problem for Pydantic, but we'll get there.

**Note**: Have in mind that this was done several years ago, in fact, the same year Pydantic was released for the first time. Using type annotations at runtime for other purposes than static analysis was not a common use case if at all. It's remarkable that it was even accounted for.

Now, as this would change the behavior of Python internally in a more or less drastic way, it would not be enforced by default yet. Instead, it was made available using a special import, `from __future__ import annotations`:

```python
from __future__ import annotations
from typing import Optional

from pydantic import BaseModel

class Person(BaseModel):
    name: str
    child: Optional[Person] = None
```

And as now these type annotations were treated as just strings, it allowed some interesting tricks when using them only for static analysis, like using typing features from future versions of Python in previous versions.

For example, declaring `Person | None` instead of `Optional[Person]`, avoiding the extra `Optional` and the extra import, even in Python 3.7 (that feature is available in Python 3.10 but not in Python 3.7):

```python
from __future__ import annotations

class Person:
    name: str
    child: Person | None = None
```

**Note**: Have in mind that this would only work for static analysis tools, your editor could understand that even in Python 3.7, but Pydantic wouldn't be able to use it and wouldn't work correctly.

This has been there, available since Python 3.7. And that behavior was planned to be the default for Python 3.10 onwards (not now, but keep reading).

### Pydantic and PEP 563

Now, forward to the present, a couple of months ago.

[Pydantic already has *some* support](https://pydantic-docs.helpmanual.io/usage/postponed_annotations/) for using `from __future__ import annotations` in the code as made possible by PEP 563. And in many cases it works fine. For example, this works:

```python
from __future__ import annotations
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


# ✅ Pydantic models outside of functions will always work
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float


app = FastAPI()


@app.post("/items/")
def create_item(item: Item):
    return item
```

But there are *some caveats* that wouldn't work. For example, this doesn't work:

```python
from __future__ import annotations
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


def create_app():
    # 🚨 Pydantic models INSIDE of functions would not work
    class Item(BaseModel):
        name: str
        description: Optional[str] = None
        price: float


    app = FastAPI()


    @app.post("/items/")
    def create_item(item: Item):
        return item
    return app


app = create_app()
```

If you run that code, you would get a disconcerting error:

```
NameError: name 'Item' is not defined
```

To solve it in this case, you could move the `Item` class outside of the function. And there are some other similar corner cases.

These types of disconcerting problems would be especially inconvenient for newcomers to Python (and probably to many experienced Python developers as well), as the problem is not obvious at all for someone that doesn't know the internals (it wasn't obvious to me, and I built FastAPI and Typer 😅).

Python is an example of a very inclusive global tech community, welcoming newcomers from all around the world, from many disciplines. It is being used to solve the most complex problems, including taking pictures of black holes, running drones on Mars, and building the most sophisticated artifical intelligence systems. But at the same time, it's many people's first programing language for its ease of use and its simplicity. And many Python developers don't even consider themselves "developers", even while they use it to solve problems.

So, having an inconvenience like this by default would not be ideal. There are other caveats but I don't want to go deeper into the technical details than I already have. You can read more about them on the [Pydantic issue](https://github.com/samuelcolvin/pydantic/issues/2678), the [mailing list thread](https://mail.python.org/archives/list/python-dev@python.org/thread/QSASX6PZ3LIIFIANHQQFS752BJYFUFPY/#UITB2A657TAINAGWGRD6GCKWFC5PEBIZ), and [Łukasz's detailed explanation](https://mail.python.org/archives/list/python-dev@python.org/thread/ZBJ7MD6CSGM6LZAOTET7GXAVBZB7O77O/).

### PEP 649 - Deferred Evaluation Of Annotations Using Descriptors

Recently, Larry Hastings that had been working on an alternative to PEP 563, [PEP 649](https://www.python.org/dev/peps/pep-0649/), contacted Samuel Colvin (Pydantic's author) and me (author of FastAPI and Typer), as suggested by [Brett Cannon](https://twitter.com/brettsky) (from the Python Steering Council), to see if and how those changes would affect us.

We realized that the changes from PEP 563 (the other one) would be permanently added to Python 3.10 (not requiring the `from __future__ import annotations`), and the caveats and problems still didn't have a solution.

Suddenly it was also clear that these use cases of using type annotations at runtime instead of only for static analysis were not an obvious use case for everyone involved, including the same Larry Hastings who was working on what would be a potential solution for these use cases.

### Asking for Reconsideration

Sadly, we realized all this very late, only weeks before these changes would be set in stone in Python 3.10 (in the end they weren't). Nevertheless, we showed our concerns.

If you read about all this before, that's probably why. It was shared a lot, and it got a bit out of hand.

And sadly, there were some radical comments attacking several of the parts involved (the Python Steering Council, us, etc), as if it was a fight between different groups. 😕

In reality, we are just one big group, the Python Community, and we are all trying to do the best for all of us.

Sadly, all this sudden friction brought a lot of increased stress to all the parties involved. To the Python Steering Council, Core Python Developers, and us, library authors.

Fortunately, everything came out well in the end.

Here's a big shoutout to [Carol Willing](https://twitter.com/willingcarol) that, despite the added stress generated for her and everyone else involved, she helped a lot reconciling different points of view, reducing the friction, and calming down all the situation. That capacity of acknowledging and adopting other's points of view is priceless. We need more Carol Willings in the world. 🤓

### Python Steering Council decision

In case you didn't know, the decision of what goes into Python and what doesn't is done by the **Python Steering Council**.

It is currently formed by:

* Barry Warsaw
* Brett Cannon
* Carol Willing
* Pablo Galindo Salgado
* Thomas Wouters

Now, back to the story, after a couple of days of that previous discussion, during the next Python Steering Council meeting, they [unanimously decided to roll back the decision](https://mail.python.org/archives/list/python-dev@python.org/thread/CLVXXPQ2T2LQ5MP2Y53VVQFCXYWQJHKZ/) of making these type annotations as strings (as described in PEP 563) being the default behavior.

Having those string type annotations by default in Python 3.10 had been decided some time ago, and rolling that change back only weeks before the "feature freeze" (the moment where no more changes are accepted into the next version) was a big decision, involving a lot of extra stress and effort.

Nevertheless, they took the decision in order to support the community of users of FastAPI, Pydantic, and other libraries using these features:

> We can’t risk breaking even a small subset of the FastAPI/pydantic users, not to mention other uses of evaluated type annotations that we’re not aware of yet.

This, again, shows the strong commitment of the Python community, starting from the Steering Council, to be inclusive, and supportive of all users, with different use cases.

Here's another big shoutout to [Pablo Galindo](https://twitter.com/pyblogsal), who [took all the extra work](https://github.com/samuelcolvin/pydantic/issues/2678#issuecomment-823569522) to perform all the last-minute changes, and even voted in favor of them.

### What's Next

The decision was to keep the current behavior, of allowing `from __future__ import annotations` in the code, as defined by PEP 563, but not as the default behavior.

This will provide enough time to find a solution or an alternative that works for all the use cases, including Pydantic, FastAPI, and also the uses cases that are interested exclusively in static analysis.

This is the best possible outcome for everyone. 🎉

It gives enough time to find an alternate solution and it avoids hurried decisions with little time that could have unknown negative effects.

## Who cares about FastAPI and Pydantic

Now, in general, how does the future of FastAPI and Pydantic look like? Who cares about them?

FastAPI, using Pydantic, was included for the first time in the last Python Developer Survey, and despite being the first year in it, it was already [ranked as the third most popular web framework](https://www.jetbrains.com/lp/python-developers-survey-2020/#FrameworksLibraries), after Flask and Django. This shows that it's being useful for many people.

It was also included in the latest [ThoughtWorks Technology Radar](https://www.thoughtworks.com/radar/languages-and-frameworks?blipid=202104087), as one of the technologies that enterprises should start trying out.

FastAPI and Pydantic are currently being used by many products and organizations, from the biggest ones you've heard of, to the smallest teams, including solo developers.

Several popular and widely used cloud providers, SaaS tools, databases, etc. are adding documentation, tutorials, and even improving their offers to better serve the FastAPI users.

The most popular code editors for Python, [PyCharm](https://www.jetbrains.com/pycharm/) and [Visual Studio Code](https://code.visualstudio.com/), have been working on improving their support for FastAPI and Pydantic. I have even talked to both teams directly. 🤓

This is particularly interesting, because FastAPI was designed to have the best support from editors, to provide the best developer experience possible. FastAPI and Pydantic use almost exclusively standard features of the language. When editors improve their support (even more) for these tools, they are actually improving their support for the features of the language itself. And this benefits many other use cases apart from FastAPI and Pydantic.

## Conclusion

Python is a great community.

We are all trying to make it better for all of us, from the Steering Council and Core Developers to library authors and even [those who help others](https://fastapi.tiangolo.com/fastapi-people/) using these libraries.

FastAPI and Pydantic are part of this community that includes and supports everyone, with all their use cases.

And that's the main reason why the future of FastAPI and Pydantic is so bright. Because the future of Python is bright. We all make this future. ✨

## Thanks

Thanks to everyone involved in finding a solution and improving the Python community. 🙇

And special thanks to:

* [Łukasz Langa](https://twitter.com/llanga)
* [Carol Willing](https://twitter.com/willingcarol)
* [Samuel Colvin](https://twitter.com/samuel_colvin)

for their review and feedback on this article before publishing.

## About me

Hey! 👋 I'm Sebastián Ramírez ([tiangolo](https://tiangolo.com)).

You can follow me, contact me, see what I do, or use my open source code:

* [GitHub: tiangolo](https://github.com/tiangolo)
* [Twitter: tiangolo](https://twitter.com/tiangolo)
* [LinkedIn: tiangolo](https://www.linkedin.com/in/tiangolo/)
* [Dev: tiangolo.to](https://dev.to/tiangolo)
* [Medium: tiangolo](https://tiangolo.medium.com/)
* [Web: tiangolo.com](https://tiangolo.com)
