Local development
============

We run `pre-commit` to preserve the quality of the code. To set up `pre-commit` run:

```
pip install virtualenvwrapper
mkvirtualenv benfordslaw -p python3.8
echo "cd $(pwd)" >> ~/.virtualenvs/benfordslaw/bin/postactivate
pip install -r requirements/dev.txt
pre-commit install
pre-commit install --hook-type commit-msg
```
