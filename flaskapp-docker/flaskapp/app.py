from flask import Flask, render_template, request, redirect, url_for, json
from flask_mail import Mail, Message
from configparser import ConfigParser

import boto3

config = ConfigParser()
config.read('./config/keys_config.cfg')

AWS_ACCESS_KEYID = config.get('AWS', 'AWS_ACCESS_KEYID')
AWS_SECRET_KEY = config.get('AWS', 'AWS_SECRET_KEY')
AWS_REGION = config.get('AWS', 'AWS_REGION')

dynamodb = boto3.resource('dynamodb',aws_access_key_id=AWS_ACCESS_KEYID,aws_secret_access_key=AWS_SECRET_KEY,region_name=AWS_REGION)

TableName = "Groceries"
table = dynamodb.Table(TableName)



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
    response = table.scan()
    item_list = response['Items']
    return render_template("base.html", item_list=item_list)


@app.route("/add", methods=["POST"])
def add():
    name = request.form.get("name")
    quantity = 0
    new_item = {"Name":name, "Qty":quantity, "Cat":'default'}
    response = table.put_item(Item=new_item)
    return redirect(url_for("home"))

@app.route("/send", methods=["POST"])
def send():
    msg = request.form.get("message")
    response = table.scan()
    item_list = response['Items']
    item_msg = msg + '\r\n'
    for item in item_list:
        item_msg = item_msg + item["Name"] + '--' + str(item["Qty"]) + '--' + item["Cat"] +  '\r\n'
    message = Message('Shopping List', sender = 'meerabibishaik@gmail.com', recipients = ['subhan150687@gmail.com'])
    message.body = item_msg
    mail.send(message)
    return redirect(url_for("home"))

@app.route("/update/<string:item_details>")
def update(item_details):
    updated_item_details = item_details.split('&')
    Qty = updated_item_details[1]
    item_name = updated_item_details[0]
    response = table.update_item(Key={'Name':item_name},
            UpdateExpression='SET Qty= :newQty',
            ExpressionAttributeValues={':newQty':str(int(Qty)+1)},
            ReturnValues="UPDATED_NEW")
    return redirect(url_for("home"))


@app.route("/delete/<string:item_details>")
def delete(item_details):
    deleted_item_details = item_details.split('&')
    item_name = deleted_item_details[0]
    Qty = deleted_item_details[1]    
    response = table.update_item(Key={'Name':item_name},
            UpdateExpression='SET Qty= :newQty',
            ExpressionAttributeValues={':newQty':str(int(Qty)-1)},
            ReturnValues="UPDATED_NEW")
    return redirect(url_for("home"))

