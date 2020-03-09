![PyMailIO](assets/pymail_io.png)

 An Asynchronous mail server.



Work in progress... please call back soon! (This is now active)

```bash
pip install pymail-io
```

#### Quick Start



There are 3 ways to use PyMailIO:

    - As a stand alone solution to send your emails & handle the response for you.
    - As a coroutine that will send your email and let you handle the response as an asyncio awaitable.
    - As an email client (you will need to implement your own background task framework & store).

Running PyMailIO as a complete emailing solution:

```python
    from pymail_io.pymailio_task import PyMailIOTask

    p = PyMailIOTask(
        password="wizard",
        receiver_email="joe@blogs.com",
        sender_email="your_email@gmail.com",
        host="smtp.gmail.com",
    )

    res = p.send_email(subject="The subject...", body="The email body...")

```

## Built With

* [PyTaskIO](https://github.com/joegasewicz/pytask_io) - Asynchronous Tasks Library using asyncio


## Authors

* **Joe Gasewicz** - *Initial work* - [JoeGasewicz](https://github.com/joegasewicz/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

This library is based on & influenced by [flask-mail](https://github.com/mattupstate/flask-mail).