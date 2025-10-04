from pyclbr import Class
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    pin_code = db.Column(db.String(10), nullable=True)
    role = db.Column(db.String(20), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', back_populates='user', lazy=True)

    reserved_spots = db.relationship('ReserveParkingSpot', back_populates='user', lazy=True) 

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "pin_code": self.pin_code,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
    

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)




class ParkingLot(db.Model):
    __tablename__ = 'parking_lot'
    id = db.Column(db.Integer, primary_key=True)
    lot_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
    total_spots = db.Column(db.Integer, nullable=False)
    image_name = db.Column(db.String(500), nullable=True)
    parking_spots = db.relationship('ParkingSpot', backref='parking_lot', lazy=True, cascade="all, delete-orphan")
    bookings = db.relationship('Booking', back_populates='parking_lot', lazy=True)
    def serialize(self):
        available_spots_count = sum(1 for spot in self.parking_spots if spot.status == 'available')
        return {
            "id": self.id,
            "lot_name": self.lot_name,
            "address": self.address,
            "pincode": self.pincode,
            "price_per_hour": self.price_per_hour,
            "total_spots": self.total_spots,
            "available_spots": available_spots_count,
            "image_name": self.image_name
        }



class ParkingSpot(db.Model):
    __tablename__ = 'parking_spot'
    id = db.Column(db.Integer, primary_key=True)
    spot_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='available')
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    booking = db.relationship('Booking', back_populates='parking_spot', uselist=False, lazy=True)

    reserved_spots = db.relationship('ReserveParkingSpot', back_populates='parking_spot', lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "spot_number": self.spot_number,
            "status": self.status,
            "lot_id": self.lot_id
        }



# class Booking(db.Model):
#     __tablename__ = 'booking'
#     id = db.Column(db.Integer, primary_key=True)
#     vehicle_number = db.Column(db.String(20), nullable=False)
#     booking_type = db.Column(db.String(20), nullable=False)
#     booking_time = db.Column(db.DateTime, nullable=False , default=datetime.utcnow)
#     start_time = db.Column(db.DateTime, nullable=False)
#     end_time = db.Column(db.DateTime, nullable=False)
#     check_in_time = db.Column(db.DateTime, nullable=True)
#     check_out_time = db.Column(db.DateTime, nullable=True)
#     total_cost = db.Column(db.Float, nullable=False)
#     status = db.Column(db.String(20), nullable=True, default='Active')
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
#     lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)


#     def serialize(self):
#         def format_datetime(dt):
#             return dt.isoformat() if dt else None

#         return {
#             "id": self.id,
#             "vehicle_number": self.vehicle_number,
#             "booking_type": self.booking_type,
#             "booking_time": format_datetime(self.booking_time),
#             "start_time": format_datetime(self.start_time),
#             "end_time": format_datetime(self.end_time),
#             "check_in_time": format_datetime(self.check_in_time),
#             "check_out_time": format_datetime(self.check_out_time),
#             "total_cost": self.total_cost,
#             "status": self.status,
#             "user_info": {
#                 "id": self.user.id,
#                 "full_name": self.user.full_name,
#                 "email": self.user.email
#             },
#             "spot_info": {
#                 "id": self.parking_spot.id,
#                 "spot_number": self.parking_spot.spot_number,
#                 "lot_id": self.parking_spot.lot_id
#             },
#             "lot_info": {
#                 "id": self.parking_lot.id,
#                 "spot_number": self.parking_lot.lot_name,
#                 "lot_id": self.parking_lot.address,
#                 "pincode": self.parking_lot.pincode,
#                 "price": self.parking_lot.price_per_hour
#             }
#         }




class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(20), nullable=False)
    booking_type = db.Column(db.String(20), nullable=False)
    booking_time = db.Column(db.DateTime, nullable=False , default=datetime.utcnow)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    check_in_time = db.Column(db.DateTime, nullable=True)
    check_out_time = db.Column(db.DateTime, nullable=True)
    total_cost = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=True, default='Active')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)

    user = db.relationship('User', back_populates='bookings')
    parking_spot = db.relationship('ParkingSpot', back_populates='booking')
    parking_lot = db.relationship('ParkingLot', back_populates='bookings')

    def serialize(self):
        def format_datetime(dt):
            return dt.isoformat() if dt else None

        user_info = None
        if self.user:
            user_info = {
                "id": self.user.id,
                "full_name": self.user.full_name,
                "email": self.user.email
            }
        spot_info = None
        if self.parking_spot:
            spot_info = {
                "id": self.parking_spot.id,
                "spot_number": self.parking_spot.spot_number,
                "lot_id": self.parking_spot.lot_id
            }
        lot_info = None
        if self.parking_lot:
            lot_info = {
                "id": self.parking_lot.id,
                "lot_name": self.parking_lot.lot_name,
                "address": self.parking_lot.address,
                "pincode": self.parking_lot.pincode,
                "price_per_hour": self.parking_lot.price_per_hour
            }
        return {
            "id": self.id,
            "vehicle_number": self.vehicle_number,
            "booking_type": self.booking_type,
            "booking_time": format_datetime(self.booking_time),
            "start_time": format_datetime(self.start_time),
            "end_time": format_datetime(self.end_time),
            "check_in_time": format_datetime(self.check_in_time),
            "check_out_time": format_datetime(self.check_out_time),
            "total_cost": self.total_cost,
            "status": self.status,
            "user_info": user_info,
            "spot_info": spot_info,
            "lot_info": lot_info
        }

class ReserveParkingSpot(db.Model):
    __tablename__ = 'reserved_spots'
    id = db.Column(db.Integer, primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    parking_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    parking_cost = db.Column(db.Float, nullable=True)

    user = db.relationship('User', back_populates='reserved_spots')
    parking_spot = db.relationship('ParkingSpot', back_populates='reserved_spots')
