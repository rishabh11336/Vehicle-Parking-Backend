from celery import shared_task, Celery
from app.models.models import User, ParkingLot, ParkingSpot, Booking, ReserveParkingSpot
from app.utils.mail_service import send_email
from jinja2 import Template
from datetime import datetime, timedelta, timezone
import csv,os
from app.utils.templates import create_html_reminder, create_html_report, google_chat_webhook


@shared_task(ignore_result=True)
def daily_reminders():
    utc_now = datetime.now(timezone.utc)

    # Determine the start of the current day in UTC.
    today_start_utc = utc_now.replace(hour=0, minute=0, second=0, microsecond=0)

    orders = Booking.query.filter(Booking.booking_time > today_start_utc).all()

    order_user_ids = {order.user_id for order in orders}



    for user in User.query.filter_by(role='user').all():
        print(user.full_name)
        if user.id not in order_user_ids:
            html_reminder = create_html_reminder(user)
            send_email(user.email, 'Reminder', html_reminder)
            google_chat_webhook(user.full_name)
            


# @shared_task(ignore_result=True)
# def monthly_activity_report():
#     print('Sending monthly activity reports')
#     # send sample email
#     html_report = create_html_report(['user'], ['order'], ['total_expenditure'])
#     # send_email('email', 'Monthly Activity Report', html_report)
#     for user in User.query.filter_by(role='user').all():
#         user_orders = [order for order in Order.query.all() if order.user_id == user.id]
#         total_expenditure = sum(order.totalprice for order in user_orders)
#         html_report = create_html_report(user, user_orders, total_expenditure)
#         send_email(user.email, 'Monthly Activity Report', html_report)

# def process_data(products, categories, order_items):
#     processed_products = {}

#     for product in products:
#         category_name = next((c.name for c in categories if c.id == product.category_id), 'Unknown')
#         processed_products[product.id] = {
#             'name': product.name,
#             'price': product.price,
#             'stock': product.quantity,
#             'units_sold': 0,
#             'category_name': category_name
#         }

#     for item in order_items:
#         product_id = item.product_id
#         if product_id not in processed_products:
#             processed_products[product_id] = {
#                 'name': item.product_name,
#                 'price': item.price,
#                 'stock': 0,
#                 'units_sold': 0,
#                 'category_name': 'Unknown'
#             }
#         processed_products[product_id]['units_sold'] += item.quantity

#     return list(processed_products.values())


# @shared_task(ignore_result=True)
# def monthly_activity_report():
#     print('Sending monthly activity reports')
#     for user in User.query.filter_by(role='user').all():
#         user_orders = [order for order in Order.query.all() if order.user_id == user.id]
#         total_expenditure = sum(order.total for order in user_orders)
#         html_report = create_html_report(user, user_orders, total_expenditure)
#         send_email(user.email, 'Monthly Activity Report', html_report)


# def sm_report():
#  # Define the base directory (e.g., your project's root directory)
#     base_dir = os.path.dirname(os.path.abspath(__file__))

#     # Define the directory and filename for the CSV
#     report_dir = os.path.join(base_dir, 'reports')
#     csv_filename = 'data.csv'
#     csv_path = os.path.join(report_dir, csv_filename)

#     # Ensure the directory exists
#     os.makedirs(report_dir, exist_ok=True)

#     # Write the CSV file
#     with open(csv_path, 'w', newline='') as output_file:
#         dict_writer = csv.DictWriter(output_file, ['name', 'price', 'stock', 'units_sold', 'category_name'])
#         dict_writer.writeheader()
#         dict_writer.writerows(process_data(Product.query.all(), Category.query.all(), OrderItem.query.all())) 

#     return csv_path