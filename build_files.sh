# build_files.sh

/opt/vercel/python3/bin/python3 -m pip install -r requirements.txt
/opt/vercel/python3/bin/python3 manage.py collectstatic --noinput

