# # from app.app import app
# # from app.models.models import User, Booking
# # from app.utils.templates import google_chat_webhook
# # from datetime import datetime, timedelta, timezone

# # app.app_context().push()

# # utc_now = datetime.now(timezone.utc)

# # # Define the target day's start and end time dynamically using the current date
# # today_start = utc_now.replace(hour=0, minute=0, second=0, microsecond=0)
# # end_of_day = today_start + timedelta(days=1)

# # print(today_start)
# # print(end_of_day)

# # print(f"Checking bookings for {today_start.date()}")

# # # Get all user IDs that have a booking on the target day
# # orders = Booking.query.filter(
# #     Booking.booking_time >= today_start,
# #     Booking.booking_time < end_of_day
# # ).all()

# # orders = Booking.query.all()

# # order_user_ids = {(order.user_id, order.booking_time) for order in orders}

# # print(order_user_ids)

# # print(today_start, end_of_day)

# # # Send a reminder to any user who does not have a booking
# # for user in User.query.filter_by(role='user').all():
# #     if user.id not in order_user_ids:
# #         print(f'Sending reminder to: {user.full_name}')
# #         google_chat_webhook(user.full_name)


# #####################################################################

# # from app.app import app
# # from app.models.models import User, Booking
# # from app.utils.templates import google_chat_webhook
# # from datetime import datetime, timedelta, timezone

# # app.app_context().push()

# # # --- SENIOR DEV FIX ---
# # # Instead of using timezone-naive datetime.now(), we get the current time in UTC.
# # # This prevents bugs where the server's local time differs from the database's time (usually UTC).
# # utc_now = datetime.now(timezone.utc)

# # # Determine the start of the current day in UTC.
# # today_start_utc = utc_now.replace(hour=0, minute=0, second=0, microsecond=0)
# # end_of_day_utc = today_start_utc + timedelta(days=1)

# # print(f"Checking for bookings for the UTC date: {today_start_utc.date()}")

# # # This query now robustly filters for bookings within the current UTC day.
# # # It assumes your database stores timestamps in a timezone-aware format or in UTC.
# # orders = Booking.query.filter(
# #     Booking.booking_time >= today_start_utc,
# #     Booking.booking_time < end_of_day_utc
# # ).all()
# # order_user_ids = {order.user_id for order in orders}

# # print(order_user_ids)

# # # Send a reminder to any user who does not have a booking for the current UTC day.
# # for user in User.query.filter_by(role='user').all():
# #     if user.id not in order_user_ids:
# #         print(f'Sending reminder to: {user.full_name}')
# #         google_chat_webhook(user.full_name)
# #     else:
# #         print(f'User {user.full_name} has a booking today, skipping.')

# #########################################################

# from app.app import app
# from app.models.models import User, Booking
# from app.utils.templates import google_chat_webhook
# from datetime import datetime, timedelta, timezone, date

# app.app_context().push()

# # --- FIX ---
# # To prove the query works, we are temporarily hardcoding the date
# # to match the known booking in your database (2025-07-26).
# # # The previous code was correctly looking for today's date, which is why it found nothing.
# # target_date = datetime.now(timezone.utc)
# # start_of_day = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
# # end_of_day = start_of_day + timedelta(days=1)

# # print(f"Checking for bookings for the specific date: {start_of_day.date()}")
# # print(target_date)
# # print("target-date", target_date.date())


# # # This query will now find the booking on 2025-07-26 because the date range matches the data.
# # orders = Booking.query.all()
# # print({(order.user_id, order.booking_time.date(), order.booking_time.date()==target_date, datetime.date(target_date), order.booking_time.date()==datetime.date(target_date)) for order in orders})
# # order_user_ids = {order.user_id for order in orders if order.booking_time.date()==start_of_day.date()}

# # print({datetime.date(order.booking_time) for order in orders})
# # # print("###############",orders[0].booking_time)
# # print(order_user_ids)

# # # Send a reminder to any user who does not have a booking for the target date.
# # for user in User.query.filter_by(role='user').all():
# #     if user.id not in order_user_ids:
# #         print(f'Sending reminder to: {user.full_name}')
# #         google_chat_webhook(user.full_name)
# #     else:
# #         print(f'User {user.full_name} has a booking on the target date, skipping.')


# utc_now = datetime.now(timezone.utc)

# # Determine the start of the current day in UTC.
# today_start_utc = utc_now.replace(hour=0, minute=0, second=0, microsecond=0)
# end_of_day_utc = today_start_utc + timedelta(days=1)

# # orders = Booking.query.filter(Booking.booking_time > datetime(today_start_utc)).all()

# orders = Booking.query.filter(Booking.booking_time > today_start_utc).all()

# order_user_ids = {order.user_id for order in orders}



# for user in User.query.filter_by(role='user').all():
#     print(user.full_name)
#     if user.id not in order_user_ids:
#         # html_reminder = create_html_reminder(user)
#         # send_email(user.email, 'Reminder', html_reminder)
#         google_chat_webhook(user.full_name)

