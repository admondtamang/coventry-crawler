# Install the dependencies

```
pip install -r requirements.txt
```

# Run the application

```
flask run --host=0.0.0.0
```

# Debug

```
flask --app main.py --debug run
```

if error occured : ImportError: cannot import name 'EVENT_TYPE_OPENED' from 'watchdog.events'

```
pip install --upgrade watchdog
```

# Notes

- used mysql for data storage
- default port runs on 50000
