from app.app import app
from app.models.models import db,User,ParkingLot,ParkingSpot,Booking, ReserveParkingSpot
# from app.cache import cache

import math
from datetime import datetime, date, timedelta
from flask_jwt_extended import  current_user, jwt_required, get_jwt_identity
from flask import request, jsonify


@app.route("/view_lot/<int:lot_id>", methods=["GET"])
@jwt_required()
# @cache.cached(timeout=10, query_string=True)
def veiw_lot(lot_id):
    infos = ParkingSpot.query.filter_by(lot_id=lot_id)
    return jsonify([info.serialize() for info in infos])


@app.route("/user_profile", methods=["GET"])
@jwt_required()
def user_profile():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(user.serialize())


@app.route("/edit_user_profile", methods=["PATCH"])
@jwt_required()
def edit_user_profile():
    # cache.clear()
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    data = request.get_json()
    user.full_name = data.get('full_name', user.full_name)
    user.email = data.get('email', user.email)
    user.phone = data.get('phone', user.phone)
    user.address = data.get('address', user.address)
    user.pin_code = data.get('pin_code', user.pin_code)
    db.session.commit()
    return jsonify({"msg": "User profile updated successfully!"}), 200


@app.route("/user_bookings", methods=["GET"])
@jwt_required()
# @cache.cached(timeout=10, query_string=True)
def user_bookings():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    user_bookings = Booking.query.filter_by(user_id=user.id).all()
    return jsonify([booking.serialize() for booking in user_bookings])


def check_duplicate_booking(vehicle_number,lot_id,start_time,end_time):
    print("Checking booking for vehicle:", vehicle_number, "in lot:", lot_id)
    booking_check = Booking.query.filter_by(vehicle_number=vehicle_number,lot_id=lot_id).all()
    print("Found bookings:", len(booking_check), booking_check)
    for book in booking_check:
        print("Checking booking:", book.start_time, book.end_time)
        if (book.start_time <= start_time) and (book.end_time >= end_time):
            return True
    return False

@app.route("/book_slot/<int:lot_id>",methods=["POST"])
@jwt_required()
def book_slot(lot_id):
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()

    # cache.clear()
    data = request.get_json()
    vehicle_number = data['vehicle_number']
    start_time_str = data["start_time"] if data["start_time"] else "00:00"
    end_time_str = data["end_time"] if data["end_time"] else "23:59"
    start_date_str = data["start_date"] if data["start_date"] else date.today()
    end_date_str = data["end_date"] if data["end_date"] else start_date_str

    booking_date = date.today() 
    
    start_time_obj = datetime.strptime(start_time_str, '%H:%M').time()
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    start_datetime = datetime.combine(start_date, start_time_obj)

    end_time_obj = datetime.strptime(end_time_str, '%H:%M').time()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    end_datetime = datetime.combine(end_date, end_time_obj)

    print("Start DateTime:", start_datetime)
    print("End DateTime:", end_datetime)

    if start_datetime > end_datetime:
        return jsonify({"msg": "Start time must be before end time!"}), 400

    if start_datetime < datetime.now():
        print(start_datetime, datetime.now())
        return jsonify({"msg": "Booking time must be in the future!"}), 400

    ### Check duplicate booking is a function available above
    check = check_duplicate_booking(vehicle_number, lot_id, start_datetime, end_datetime)

    print("Check Booking:", check)

    if check:
        return jsonify({"msg": "Another booking already exists!"}), 404
    park_spot = ParkingSpot.query.filter_by(lot_id = lot_id, status="available")

    if not park_spot:
        return jsonify({"msg" : "Parking spot is fully booked."})
    ###  WE are searching 1st empty spot from spots
    available_spot =  min([spot.spot_number for spot in park_spot])
    spot = ParkingSpot.query.filter_by(lot_id = lot_id, spot_number = available_spot).first()
    spot.status = "available"
    db.session.add(spot)
    db.session.flush()
    booking = Booking(vehicle_number = data["vehicle_number"],
                      booking_type = data["booking_type"],
                      start_time = start_datetime,
                      end_time = end_datetime,
                      check_in_time = None,
                      check_out_time = None,
                      total_cost = ParkingLot.query.filter_by(id=lot_id).first().price_per_hour,
                      status = "Active",
                      user_id = current_user.id,
                      lot_id = lot_id,
                      spot_id = available_spot
                      )
    db.session.add(booking)
    db.session.commit()
    return jsonify({"msg":"Booking Sucessfull"})
    

@app.route("/cancel_booking/<int:booking_id>", methods=["PATCH"])
@jwt_required()
def cancel_booking(booking_id):
    # cache.clear()

    update_booking = Booking.query.filter_by(id=booking_id).first()
    if not update_booking:
        return jsonify({"msg": "Booking not found!"}), 404
    spot = ParkingSpot.query.filter_by(spot_number=update_booking.spot_id, lot_id=update_booking.lot_id).first()
    # data = request.get_json()    
    # update_booking.status = data.get('status', update_booking.status)
    update_booking.status = 'canceled'
    update_booking.total_cost = 0
    db.session.flush()
    if spot:
        spot.status = 'available'
    db.session.commit()
    return jsonify({"msg": "Booking canceled successfully!"})


# @app.route("/check_in/<int:lot_id>/<string:vehicle_number>", methods=["POST"])
# @jwt_required() 
# def user_check_in(lot_id, vehicle_number):
#     cache.clear()
#     user_id = 1 
#     current_time = datetime.now()
#     existing_booking = Booking.query.filter_by(vehicle_number=vehicle_number, status='active').first()
#     if existing_booking:
#         existing_booking.check_in_time = current_time
#         existing_booking.status = 'Parked'
#         spot = ParkingSpot.query.get(existing_booking.spot_id)
#         if spot:
#             spot.status = 'occupied'
#         db.session.commit()
#         return jsonify({
#             "msg": "Pre-booked check-in successful!",
#             "booking_id": existing_booking.id
#         }), 200
#     else:
#         available_spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='available').first()
#         if not available_spot:
#             return jsonify({"msg": "Sorry, this parking lot is full."}), 404            
#         # Create a new booking record on the spot.
#         new_booking = Booking(
#             vehicle_number=vehicle_number,
#             booking_type='direct',
#             booking_time=current_time,
#             check_in_time=current_time,
#             start_time=current_time,
#             end_time=current_time + timedelta(hours=1),
#             total_cost=0, 
#             status='Parked', 
#             user_id=user_id,
#             spot_id=available_spot.id,
#             lot_id=lot_id
#         )     
#         available_spot.status = 'occupied'
#         db.session.add(new_booking)
#         db.session.commit()
        
#         return jsonify({
#             "msg": "Walk-in check-in successful! A new booking has been created.",
#             "booking_id": new_booking.id,
#             "spot_number": available_spot.spot_number
#         }), 201


@app.route("/booking_status/<int:booking_id>", methods=["PATCH"])
@jwt_required()
def booking_status(booking_id):
    # cache.clear()
    booking_status = Booking.query.filter_by(id=booking_id).first()
    if not booking_status:
        return jsonify({"msg": "Booking not found!"}), 404
    booking_status.check_out_time = datetime.now()
    db.session.flush()
    spot_id = booking_status.spot_id
    lot_id = booking_status.lot_id
    Parking_spot = ParkingSpot.query.filter_by(spot_number = spot_id, lot_id = lot_id).first()
    if not Parking_spot:
        return jsonify({"msg": "Parking spot not found!"}), 404
    data = request.get_json()    
    Parking_spot.status = data['status']
    db.session.commit()
    return jsonify({"msg": "Paking Exited successfully"})


@app.route("/parking_lots", methods=["GET"])
@jwt_required()
# @cache.cached(timeout=10, query_string=True)
def get_all_lots():
    all_lots = ParkingLot.query.all()    
    if not all_lots:
        # cache.clear()
        return jsonify({"msg": "Parking lots not found!"}), 404
    results = []    
    for lot in all_lots:
        available_spots_count = ParkingSpot.query.filter_by(lot_id=lot.id, status='available').count()        
        lot_data = {
            "id": lot.id,
            "name": lot.lot_name,
            "address": lot.address,
            "pincode": lot.pincode,
            "price": lot.price_per_hour,
            "total_spots": lot.total_spots,
            "available_spots": available_spots_count,
            "image_url": lot.image_name
        }
        results.append(lot_data)        
    return jsonify(results)


@app.route("/parking_spot/<int:lot_id>/<int:spot_id>", methods=["GET"])
@jwt_required()
# @cache.cached(timeout=10, query_string=True)
def get_single_lot(lot_id,spot_id):
    spot = ParkingSpot.query.filter_by(lot_id = lot_id,spot_number = spot_id).first()
    if not spot:
        return jsonify({"msg": "Parking lot not found!"}), 404
    spot_data = {
        "lot_id" : spot.lot_id,
        "spot_number" : spot.spot_number,
        "status" : spot.status
    }
    return jsonify(spot_data)        


@app.route("/user_summary", methods=["GET"])
@jwt_required()
def user_summary():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    user_bookings = Booking.query.filter_by(user_id=user.id).all()
    return jsonify([booking.serialize() for booking in user_bookings])


@app.route('/user/booking-details/<int:id>', methods=["GET"])
@jwt_required()
def booking_details(id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email = current_user_email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    _booking = Booking.query.filter_by(user_id=user.id, id=id) #status='occupied'
    return jsonify([booking.serialize() for booking in _booking])


@app.route('/user/check_in/<int:booking_id>', methods=["POST"])
@jwt_required()
def check_in(booking_id):
    # cache.clear()
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    booking = Booking.query.filter_by(id=booking_id, user_id=user.id).first()
    if not booking:
        return jsonify({"msg": "Booking not found"}), 404
    if booking.check_in_time:
        return jsonify({"msg": "Already checked in!"}), 400
    booking.check_in_time = datetime.now()
    booking.status = 'occupied'
    spot = ParkingSpot.query.filter_by(spot_number=booking.spot_id, status='available', lot_id=booking.lot_id).first()
    if spot:
        spot.status = 'occupied'
    else:
        return jsonify({"msg": "Spot not available for check-in!"}), 404
    db.session.flush()
    reserved_spot = ReserveParkingSpot(spot_id=booking.spot_id, lot_id=spot.lot_id, user_id=user.id, vehicle_number=booking.vehicle_number, parking_timestamp=datetime.now())
    db.session.add(reserved_spot)
    db.session.commit()
    return jsonify({"msg": "Check-in successful!"})


@app.route('/user/check_out/<int:booking_id>', methods=["POST"])
@jwt_required()
def check_out(booking_id):
    # cache.clear()
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    booking = Booking.query.filter_by(id=booking_id, user_id=user.id).first()
    if not booking:
        return jsonify({"msg": "Booking not found"}), 404
    if booking.check_out_time:
        return jsonify({"msg": "Already checked out!"}), 400
    
    lot_cost = ParkingLot.query.filter_by(id=booking.lot_id).first().price_per_hour

    booking.check_out_time = datetime.now()
    booking.status = 'completed'
    booking.total_cost = math.ceil(((booking.check_out_time - booking.check_in_time).total_seconds() / 3600)) * lot_cost
    db.session.flush()
    spot = ParkingSpot.query.filter_by(spot_number=booking.spot_id, status='occupied', lot_id=booking.lot_id).first()
    if spot:
        spot.status = 'available'
    db.session.flush()
    # delete entry from ReserveParkingSpot
    reserved_spot = ReserveParkingSpot.query.filter_by(spot_id=booking.spot_id, user_id=user.id, lot_id=spot.lot_id).first()
    if reserved_spot:
        db.session.delete(reserved_spot)
    db.session.commit()
    return jsonify({"msg": "Check-out successful!"})


@app.route('/user/_cost/<int:booking_id>', methods=["GET"])
@jwt_required()
def booking_cost(booking_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"msg": "User not found"}), 404
    booking = Booking.query.filter_by(id=booking_id, user_id=user.id).first()
    if not booking:
        return jsonify({"msg": "Booking not found"}), 404
    return jsonify({"total_cost": booking.total_cost})