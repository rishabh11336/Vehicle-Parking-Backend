from app.app import app
from app.models.models import db,User,ParkingLot,ParkingSpot, ReserveParkingSpot

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify



@app.route('/admin/count_users', methods=["GET"])
@jwt_required()
def count_users():
    current_user_email = get_jwt_identity()
    if current_user_email != "admin@gmail.com":
        return jsonify({"msg": "pls login with admin"}), 401
    all_users = User.query.filter_by(role='user').all()
    return jsonify({"count": len(all_users)}), 200


# Define a POST route for user login
@app.route("/admin/create_lots", methods=["POST"])
@jwt_required()
def create_parking_lot():
    current_user_email = get_jwt_identity()
    if current_user_email != "admin@gmail.com":
        return jsonify({"msg": "pls login with admin"}), 401
    data = request.get_json()   
    new_lot = ParkingLot(
        lot_name=data['lot_name'],
        address=data['address'],
        pincode=data['pincode'],
        price_per_hour=data['price_per_hour'],
        total_spots=data['total_spots'],
        image_name = data['image_url']
    )
    db.session.add(new_lot)
    db.session.flush()
    response_data = {
        "msg": "Parking lot created successfully",
    }
    for i in range(1, new_lot.total_spots + 1):
        new_spot = ParkingSpot(
            spot_number=f"A-{i}",
            lot_id=new_lot.id,
            status='available'
        )
        db.session.add(new_spot)
    db.session.commit()
    return jsonify(response_data), 201



@app.route("/admin/update_lots/<int:lot_id>", methods=["PUT"])
@jwt_required()
def update_parking_lot(lot_id):
    update_lot = ParkingLot.query.filter_by(id=lot_id).first()
    if not update_lot:
        return jsonify({"msg": "Parking lot not found!"}), 404
    data = request.get_json()    
    prev_total_spots = update_lot.total_spots
    update_lot.lot_name = data.get('lot_name', update_lot.lot_name)
    update_lot.address = data.get('address', update_lot.address)
    update_lot.pincode = data.get('pincode', update_lot.pincode)
    update_lot.price_per_hour = data.get('price_per_hour', update_lot.price_per_hour)
    update_lot.total_spots = data.get('total_spots', update_lot.total_spots)
    update_lot.image_name = data.get('image_url', update_lot.image_name)
    db.session.flush()
    # if total_spots is changed, then delete old spots
    if ParkingSpot.query.filter_by(lot_id=update_lot.id, status='occupied').count() == 0:
        ParkingSpot.query.filter_by(lot_id=update_lot.id).delete()
        db.session.flush()
        flag = True
    else:
        return jsonify({"msg": "Parking lot has occupied spots!"}), 400
    db.session.flush()

    # then add new spots
    if flag:
        for i in range(1, update_lot.total_spots + 1):
            new_spot = ParkingSpot(
                spot_number=f"A-{i}",
                lot_id=update_lot.id,
                status='available')
            db.session.add(new_spot)
    db.session.commit()

    response_data = {
         "msg": "Parking lot updated successfully"
    }
    return jsonify(response_data)



@app.route("/admin/delete_lots/<int:lot_id>", methods=["DELETE"])
@jwt_required()
def delete_parking_lot(lot_id):
    delete_lot = ParkingLot.query.get(lot_id)
    if not delete_lot:
        return jsonify({"msg": "Parking lot not found!"}), 404
    occupied_spots_count = ParkingSpot.query.filter_by(lot_id=lot_id, status='occupied').count()
    if occupied_spots_count > 0:
        return jsonify({"msg": f"Cannot delete lot {occupied_spots_count} spots are currently occupied."}), 400
    db.session.delete(delete_lot)
    db.session.commit()
    response_data = {
        "msg": "Parking lot deleted successfully!"
    }
    return jsonify(response_data)



@app.route("/admin/users", methods=["GET"])
@jwt_required()
def get_all_users():
    current_user_email = get_jwt_identity()
    if current_user_email != "admin@gmail.com":
        return jsonify({"msg": "pls login with admin"}), 401
    all_users = User.query.filter_by(role='user').all()
    return jsonify([user.serialize() for user in all_users]), 200



@app.route("/admin/all_spot/<int:lot_id>", methods=["GET"])
@jwt_required()
def get_all_spot(lot_id):
    current_user_email = get_jwt_identity()
    if current_user_email != "admin@gmail.com":
        return jsonify({"msg": "pls login with admin"}), 401
    spots_in_lot = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    if not spots_in_lot:
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return jsonify({"msg": "Parking lot not found."}), 404
        else:
            return jsonify({"msg": "This parking lot has no spots."}), 200
    res = []


    for spot in spots_in_lot:
        if spot.status == 'occupied':
            res_spot = ReserveParkingSpot.query.filter_by(spot_id=spot.spot_number).first()
            if not res_spot:
                print(f"Spot {spot.id} is occupied but no reservation found.")
            res.append({
            "id": spot.id,
            "lot_id": spot.lot_id,
            "spot_number": spot.spot_number,
            "status": spot.status,
            "Vehicle": res_spot.vehicle_number,
            "User": res_spot.user_id
        })
        else:
            res.append({
                "id": spot.id,
                "lot_id": spot.lot_id,
                "spot_number": spot.spot_number,
                "status": spot.status,
                "Vehicle": 'N/A',
                "User": 'N/A'
            })

    return jsonify(res), 200
    # return jsonify([spot.serialize() for spot in spots_in_lot]), 200



@app.route("/admin/parking_lots/<int:lot_id>", methods=["GET"])
@jwt_required()
def get_all_parking_lots(lot_id):
    current_user_email = get_jwt_identity()
    if current_user_email != "admin@gmail.com":
        return jsonify({"msg": "pls login with admin"}), 401
    lot = ParkingLot.query.filter_by(id=lot_id).first()
    if not lot:
        return jsonify({"msg": "Parking lot not found."}), 404
    return jsonify(lot.serialize()), 200 




@app.route("/admin/stats", methods=["GET"])
@jwt_required()
def get_admin_stats():
    current_user_email = get_jwt_identity()
    if current_user_email != "admin@gmail.com":
        return jsonify({"msg": "pls login with admin"}), 401
    all_lots = ParkingLot.query.all()
    response_data = []
    for lot in all_lots:
        total_spots = ParkingSpot.query.filter_by(lot_id=lot.id).count()
        occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='occupied').count()
        response_data.append({
            "name": lot.lot_name,
            "totalSpots": total_spots,
            "occupied": occupied_spots
        })
    return jsonify(response_data), 200