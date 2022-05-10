Clark Coding Challenge "Reward System"
===

## Overview

```
.
|-- test
|   |-- __init__.py
|   |-- empty_input.txt
|   |-- input.txt
|   |-- multiple_invitees_input.txt
|   |-- only_first_invite_input.txt
|   |-- out_of_order_input.txt
|   `-- test_main.py
|-- Coding_Challenge_Reward_System.pdf
|-- Makefile
|-- README.md
|-- main.py
|-- requirements.in
`-- requirements.txt
```

## Prerequisites

- `Python 3.10.0`
- `pip 22.0.4`

### Optional

This app was built within a freshly created virtual environment using [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) to ensure that the app and its dependencies are isolated to other projects on the host system. It's encouraged to have separate virtual environment for each project so that installing or uninstalling packages in one project won't have unforeseen negative effects on others. But you could try to run this just without one in your system environment after the prerequisites are satisfied. But there's no guarantee then that the dependencies required by the app to run won't interfere with the underlying system.

## Getting started

The project contains in the root directory a [Makefile](Makefile) that has several commands to setup, run and test the app. In the CLI change to the project root directory to conduct the following steps:

- Run `make list` to show available targets
- If you run this project for the first time, then choose `make setup` to install all dependencies needed for the app to run
- To start the app on `http://0.0.0.0:8000` please select `make run`, afterwards you can send request to the app using e.g. `curl` or `Postman` (_examples further down_)
- To run the test suite please execute `make test_suite`, this will trigger the test framework [pytest](https://docs.pytest.org/en/7.1.x/) to run the test cases in `./test/test_main.py`

### Examples

The framework used to build this app provides interactive API docs out of the box. The two available docs are served at:

- **Swagger UI** `http://0.0.0.0:8000/docs`
- **ReDoc** `http://0.0.0.0:8000//redoc`

They can be used to interact with the API.

Another way to interact with the API is via 

- **Postman**: send the `POST` request to `http://0.0.0.0:8000/confirmed-invitations/scores` and select as *body* `form-data`, the *key* is `file` and the *value* is the path to the required `<prefix>_input.txt` file
- or `curl`
```
curl --location --request POST 'http://0.0.0.0:8000/confirmed-invitations/scores' \
--form 'file=@"/path/to/test/input.txt"'
``` 

## Annotation

The service layer in `./main.py` has two implementations for the calculating the score for confirmed invitations. The first implementation `_calculate_score(..)` is rather straightforward and naive using only Python's hashmaps structure `dict`. It doesn't separate recommendation from acceptance events but process them in the exact order as they come in.

The second implementation `_calculate_score_v2(...)` utilises Python's linked list structure `deque` to build up referrals graphs first before iterate over the input events in reverse order to obtain the latest acceptance events.

Both implementations can handle following cases besides the regular [input.txt](test/input.txt):

- input file is empty: fail with `HTTP Statuscode 400`
- multiple invitations by different user to the same invitee: first-come-first-serve, only the first invite gets recorded
- user invites successfully multiple invitee: in case of multiple confirmed invitations ensure that during sum up no referrals get counted twiced
- events in input file were first assumed to be always in order, later the timestamp was used to sort the events before passing them along to the next steps that were still assuming the events to be in order

One corner case is not covered yet, when the events in the `input.txt` are not separated by new line character but in one long string.