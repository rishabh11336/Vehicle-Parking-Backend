import os
from json import dumps
from httplib2 import Http
from jinja2 import Template
from datetime import datetime



def create_html_report(user, orders, total_expenditure):
    # Load HTML template (assuming you have an HTML template file)
    template = """
<!DOCTYPE html>
<html>
<head>
    <title>Monthly Activity Report</title>
    <style type="text/css">
        body { font-family: Arial, sans-serif; }
        .container { width: 100%; max-width: 600px; margin: auto; }
        .header { background-color: #af9d4c; padding: 10px; text-align: center; color: white; }
        .content { background-color: #ffffff; padding: 20px; }
        .footer { background-color: #535353; padding: 10px; text-align: center; color: white; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #dddddd; text-align: left; padding: 8px; }
        th { background-color: #af9d4c; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            
            <img src="https://github.com/rishabh11336/Mad-2-Backend/blob/main/Emart-logo.jpg?raw=true" alt="E-MArt Logo" style="max-width: 100px;"/>
            <h2>Vehicle Parking App Monthly Activity Report</h2>
        </div>
        <div class="content">
            <p>Dear {{ user.full_name | upper  }},</p>
            <p>Here is your activity report for the month.</p>

            <h3>Order Summary</h3>
            <table>
                <tr>
                    <th>Order ID</th>
                    <th>Date</th>
                    <th>Total</th>
                </tr>
                {% for order in orders %}
                <tr>
                    <td>{{ order.id }}</td>
                    <td>{{ order.dateCreated }}</td>
                    <td>₹{{ order.totalprice }}</td>
                </tr>
                {% endfor %}
            </table>

            <p><strong>Total:</strong> ₹{{ total_expenditure }}</p>
        </div>
        <div class="footer">
            <p>Thank you for vist at Vehicle Parking App.</p>
        </div>
    </div>
</body>
</html>
"""

    # Render the template with the user's data
    html_report = Template(template).render(user=user, orders=orders, total_expenditure=total_expenditure)

    return html_report


def create_html_reminder(user):
    # Load HTML template (assuming you have an HTML template file)
    template = """
<!DOCTYPE html>
<html>
<head>
    <title>Reminder</title>
    <style type="text/css">
        body { font-family: Arial, sans-serif; }
        .container { width: 100%; max-width: 600px; margin: auto; }
        .header { background-color: #af9d4c; padding: 10px; text-align: center; color: white; }
        .content { background-color: #ffffff; padding: 20px; }
        .footer { background-color: #535353; padding: 10px; text-align: center; color: white; }
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #dddddd; text-align: left; padding: 8px; }
        th { background-color: #af9d4c; color: white; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://github.com/rishabh11336/Mad-2-Backend/blob/main/Emart-logo.jpg?raw=true" alt="E-Mart Logo" style="max-width: 100px;"/>
            <h2>Vehicle Parking App Reminder</h2>
        </div>
        <div class="content">
            <p>Dear {{ user.full_name | upper  }},</p>
            <p>You have not visited our Parking today. Please visit us soon.</p>
        </div>
        <div class="footer">
            <p>Thank you for vist at Vehicle Parking App.</p>
        </div>
    </div>
</body>
</html>
"""

    # Render the template with the user's data
    html_reminder = Template(template).render(user=user)

    return html_reminder

def google_chat_webhook(user):
    """Google Chat incoming webhook with a card message resembling an HTML template."""
    # url = "https://chat.googleapis.com/v1/spaces/AAAAPS3VyIw/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=JhhTjjZOXMtvDg8lyv-A-b_mg2Ne9eC4Vd6vonQkit4"
    url = "https://chat.googleapis.com/v1/spaces/AAQAUdy_aaA/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=XzDAiPk_KMvsZfYsGL7kxKO1Raqgdz8GUGo7eGMoU0I"

    username = user

    card_message = {"text": "Hello " + username + ",\nYou have not visited our Parking today. Please visit us soon."}

    message_headers = {"Content-Type": "application/json; charset=UTF-8"}

    try:
        http_obj = Http()
        response = http_obj.request(
            uri=url,
            method="POST",
            headers=message_headers,
            body=dumps(card_message),
        )
        if response[0].status == 200:
            print("Message successfully posted to Google Chat for user: ", username)
        else:
            print(f"Failed to post message to Google Chat. Status: {response[0].status}, Response: {response[1]}")
    except Exception as e:
        print(f"Error posting message to Google Chat for user {username}: {str(e)}")