from flask import Flask, render_template
app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

@app.route('/')
def home():
  return render_template("main.html")

@app.route("/beach")
def beach():
  return render_template("beach.html")

app.run(host='0.0.0.0', port=8080)