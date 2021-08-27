from flask import Flask, render_template, request, redirect, url_for, json
from flask_mail import Mail, Message

app = Flask(__name__)

# /// = relative path, //// = absolute path
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'meerabibishaik@gmail.com'
app.config['MAIL_PASSWORD'] = 'Janu4gm1'

mail = Mail(app)

@app.route("/")
def home():
    with open('data/items.json') as f:
        item_list=json.load(f)
    #print(todo_list)
    return render_template("base.html", item_list=item_list)


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    quantity = 0
    new_item = {"name":name, "quantity":quantity}
    with open('data/items.json','r') as f:
        item_list=json.load(f)
    item_list.append(new_item)
    with open('data/items.json','w') as f:
        json.dump(item_list,f)
    return redirect(url_for("home"))

@app.route("/send", methods=["POST"])
def send():
    msg = request.form.get("message")
    with open('data/items.json') as f:
        item_list=json.load(f)
    item_msg = msg + '\r\n'
    for item in item_list:
        item_msg = item_msg + item["name"] + '--' + str(item["quantity"]) + '\r\n'
    message = Message('Shopping List', sender = 'meerabibishaik@gmail.com', recipients = ['subhan150687@gmail.com'])
    message.body = item_msg
    mail.send(message)
    return redirect(url_for("home"))

@app.route("/update/<string:item_name>")
def update(item_name):
    with open('data/items.json','r') as f:
        item_list=json.load(f)
    for item in item_list:
        if item["name"]==item_name:
            if item["quantity"]>=0 and item["quantity"]<=9:
                item["quantity"]=item["quantity"]+1
            break
    with open('data/items.json','w') as f:
        json.dump(item_list,f)
    return redirect(url_for("home"))


@app.route("/delete/<string:item_name>")
def delete(item_name):
    with open('data/items.json','r') as f:
        item_list=json.load(f)
    for item in item_list:
        if item["name"]==item_name:
            if item["quantity"]!=0:
                item["quantity"]=item["quantity"]-1
            break
    with open('data/items.json','w') as f:
        json.dump(item_list,f)
    return redirect(url_for("home"))

