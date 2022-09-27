# Spam Spotting Website #


### To run it on your local machine: ###
```python
# in the root directory
python3 -m venv venv
. venv/bin/activate
export FLASK_APP=webapp
export FLASK_ENV=development
pip install -r requirements.txt
flask run
# The website will then be running on http://127.0.0.1:5000/ 

# SPECIFICALLY FOR WINDOWS
# in the root directory
python3 -m venv venv
. venv/Scripts/activate
$env:FLASK_APP = "webapp"
$env:FLASK_ENV = "development"
pip install -r requirements.txt
flask run
# The website will then be running on http://127.0.0.1:5000/ 
```