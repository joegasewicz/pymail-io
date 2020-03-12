![PyPI](https://img.shields.io/pypi/v/pymail-io)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymail-io)
![Read the Docs (version)](https://img.shields.io/readthedocs/pymail-io/latest)

![PyMailIO](assets/pymail_io.png)

 An Asynchronous mail server that's built on CPython's AsyncIO library.
 
Read the docs: [Documentation](https://pymail-io.readthedocs.io/en/latest/)


```bash
pip install pymail-io
```

#### Quick Start


There are 3 ways to use PyMailIO:


Running PyMailIO as a complete emailing solution:

```python
from pymail_io.pymailio_task import PyMailIOTask

p = PyMailIOTask(
    password="wizard",
    receiver_email="joe@blogs.com", # Or a list of emails receiver_email=["joe@blogs.com", ...],
    sender_email="your_email@gmail.com",
    email_host="smtp.gmail.com",
)
# Create your email subject & body
email_meta = p.send_email(
    subject="The subject...",
    body="The email body...",
)
# Get a response from your sent email:
res = p.get_email_response(email_meta)
```

##### Coming soon:

Running PyMailIO as an asyncio coroutine:

```python
from pymail_io.pymailio_async import PymailIOAsync

p = PymailIOAsync(
    password="wizard",
    receiver_email="joe@blogs.com",
    sender_email="your_email@gmail.com",
    email_host="smtp.gmail.com",
)

# if you are running PyMailIO within the life time of a long running process, such as
# a web framework of rest API, then set `run_for_ever=True` as this will yield much
# better performances.

# Create your email subject & body as a coroutine & await
email_meta = await p.send_email(
    subject="The subject...",
    body="The email body...",
)
# Await a response from your sent email as a coroutine:
res = await p.get_email_response(email_meta)
```
##### Coming soon:

Running PyMailIO as a synchronous function (You will need to handle blocking & response):

```python
from pymail_io.pymailio_sync import PyMailIOSync

p = PyMailIOSync(
    password="wizard",
    receiver_email="joe@blogs.com",
    sender_email="your_email@gmail.com",
    email_host="smtp.gmail.com",
)
# Create your email subject & body
email_meta = p.send_email(
    subject="The subject...",
    body="The email body...",
)
```


## Built With

* [PyTaskIO](https://github.com/joegasewicz/pytask_io) - Asynchronous Tasks Library using asyncio


## Authors

* **Joe Gasewicz** - *Initial work* - [JoeGasewicz](https://github.com/joegasewicz/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

This library is based on & influenced by [flask-mail](https://github.com/mattupstate/flask-mail).