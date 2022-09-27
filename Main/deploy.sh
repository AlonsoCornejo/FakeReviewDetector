# create virtual environment
python -m venv venv
. venv/bin/activate
# set env variables
export FLASK_APP=webapp
export FLASK_ENV=development
# install dependencies
pip install -r requirements.txt
# kill any existing gunicorn instances so we can deploy
pkill gunicorn
# start up webapp in background
gunicorn -b 128.180.108.75 webapp:app --workers=8 --preload --daemon
