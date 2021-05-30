from app import app
from functions import moneylb
print(moneylb())

app.run(host='0.0.0.0', port=8080)