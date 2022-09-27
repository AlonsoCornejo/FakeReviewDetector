# create virtual environment
python -m venv venv
. venv/Scripts/activate
# set env variables
export FLASK_APP=webapp
export FLASK_ENV=development
# install dependencies
pip install -r requirements.txt
# start up webapp in background
flask run