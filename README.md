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
# if you are running PyMailIO within the life time of a long running process, such as
# a web framework of rest API, then set `run_forever=True` as this will yield much
# better performances.
```
Create your email subject & body
```python
r = p.send_email(
    subject="The subject...",
    body="The email body...",
)

```

The response from calling `p.send_email`:
```python
"""

{
    "metadata": { # metadata... },
        "email": {
            "subject": subject,
            "body": body,
            "email_init": # time that PyMailIO sent your email,
    }
}
"""
```

```python

# Get a response from your sent email:
r = p.get_email_response(r)


```


## Built With

* [PyTaskIO](https://github.com/joegasewicz/pytask_io) - Asynchronous Tasks Library using asyncio


## Authors

* **Joe Gasewicz** - *Initial work* - [JoeGasewicz](https://github.com/joegasewicz/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

This library is based on & influenced by [flask-mail](https://github.com/mattupstate/flask-mail).