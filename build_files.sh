# build_files.sh

echo "BUILD START"

# create a virtual environment named 'venv' if it doesn't already exist
python 3.11.4 -m venv venv

# activate the virtual environment
source venv/bin/activate


pip install -r requirements.txt
python 3.11.4 manage.py collectstatic --noinput


echo "BUILD END"