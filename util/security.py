from itsdangerous import URLSafeTimedSerializer

from settings import app

ts = URLSafeTimedSerializer(app.secret_key)