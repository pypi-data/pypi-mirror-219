# BasketCase
Download images and videos from Instagram.

Notable features:
- Stories can be downloaded without triggering the "seen" flag.
- Downloads a high quality version of a profile picture.

## Installation
Install it from [PyPI](https://pypi.org/project/basketcase/).

```sh
pip install --user basketcase
```

> This should put the executable `basketcase` on your PATH.

## Command-line usage
```sh
basketcase -u "https://instagram.com/p/<post_id>"
```

> Downloaded resources will be stored in the current working directory (i.e. `$PWD/basketcase_downloads`).

To download from multiple URLs, create a text file (e.g. `urls.txt`)
and populate it with resource URLs:

```
https://instagram.com/p/<post_id>
https://instagram.com/reel/<reel_id>
https://instagram.com/<username>
```

```sh
basketcase -f ./urls.txt
```

### Supported URLs
| Supported URL                                                  | Description                                                                      |
|----------------------------------------------------------------|----------------------------------------------------------------------------------|
| `https://instagram.com/<username>`                             | User profile. Downloads stories from the past 24 hours, and the profile picture. |
| `https://instagram.com/p/<post_id>`                            | Standard publication.                                                            |
| `https://instagram.com/reel/<reel_id>`                         | Reels movie                                                                      |
| `https://www.instagram.com/stories/highlights/<highlight_id>/` | A collection of stories, or "highlights"                                         |
| `https://www.instagram.com/s/<random_characters>`              | A shorter type of URL                                                            |

### Authentication
1. Add a session cookie

```sh
basketcase --cookie <session_cookie_id> --cookie-name "my session"
# Added session id: 1
```

2. Specify its identifier when downloading

```sh
basketcase -s 1
```

> List all available sessions with `basketcase -l`.
> To disable sessions, use `--no-session`.
> If only one exists, it is treated as the default.

## User data
Cookies and other application data are kept in your home directory (i.e. `~/.basketcase`).

## Development setup
1. `cd` to the project root and create a virtual environment
in a directory named `venv`, which is conveniently ignored in
version control.
2. Install the dependencies.

```sh
pip install -r requirements.txt
```

3. Install this package in editable mode.

```sh
pip install -e .
```

### Package build and upload
1. Update the requirements list.

```sh
pip freeze --exclude-editable > requirements.txt
```

2. Increment the version on `pyproject.toml`.
3. Build the package.

```sh
python -m build
```

4. Commit and push the changes (and a new version tag) to the git repository.
5. Publish it.
```sh
python -m twine upload dist/*
```
