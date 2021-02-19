import sys
sys.path.insert(0, "/var/www/flask")

from app import app as application
application.secret_key = os.urandom(42)
application.config["JSON_SORT_KEYS"] = False
application.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
