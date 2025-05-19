from flask import Blueprint, request, jsonify
from models.trip import Trip
from app import db
from utils.auth_middleware import auth_required, get_current_user
from datetime import datetime

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/', methods=['POST'])
@auth_required
def create_trip():
    try:
        # Get and validate request data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        # Check if the payload is nested under 'create_trip'
        if 'create_trip' in data:
            data = data['create_trip']
            
        # Validate required fields
        required_fields = ['destination', 'start_date', 'end_date']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400

        # Create new trip
        trip = Trip(
            user_id=get_current_user().id,
            destination=data['destination'],
            start_date=datetime.fromisoformat(data['start_date'].replace('Z', '+00:00')),
            end_date=datetime.fromisoformat(data['end_date'].replace('Z', '+00:00')),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            itinerary=data.get('itinerary', {})
        )
        
        db.session.add(trip)
        db.session.commit()
        
        return jsonify({
            'message': 'Trip created successfully',
            'trip': {
                'id': trip.id,
                'destination': trip.destination,
                'start_date': trip.start_date.isoformat(),
                'end_date': trip.end_date.isoformat(),
                'latitude': trip.latitude,
                'longitude': trip.longitude,
                'itinerary': trip.itinerary
            }
        }), 201
        
    except Exception as e:
        print(f"Error creating trip: {str(e)}")  # Debug print
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@trips_bp.route('/', methods=['GET'])
@auth_required
def get_trips():
    current_user = get_current_user()
    trips = current_user.trips.all()
    return jsonify([{
        'id': trip.id,
        'destination': trip.destination,
        'start_date': trip.start_date.isoformat(),
        'end_date': trip.end_date.isoformat(),
        'latitude': trip.latitude,
        'longitude': trip.longitude,
        'itinerary': trip.itinerary
    } for trip in trips]), 200

@trips_bp.route('/<int:trip_id>', methods=['GET'])
@auth_required
def get_trip(trip_id):
    current_user = get_current_user()
    trip = current_user.trips.filter_by(id=trip_id).first()
    
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
        
    return jsonify({
        'id': trip.id,
        'destination': trip.destination,
        'start_date': trip.start_date.isoformat(),
        'end_date': trip.end_date.isoformat(),
        'latitude': trip.latitude,
        'longitude': trip.longitude,
        'itinerary': trip.itinerary
    }), 200

@trips_bp.route('/<int:trip_id>', methods=['PUT'])
@auth_required
def update_trip(trip_id):
    current_user = get_current_user()
    trip = current_user.trips.filter_by(id=trip_id).first()
    
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
        
    data = request.get_json()
    
    try:
        if 'destination' in data:
            trip.destination = data['destination']
        if 'start_date' in data:
            trip.start_date = datetime.fromisoformat(data['start_date'])
        if 'end_date' in data:
            trip.end_date = datetime.fromisoformat(data['end_date'])
        if 'latitude' in data:
            trip.latitude = data['latitude']
        if 'longitude' in data:
            trip.longitude = data['longitude']
        if 'itinerary' in data:
            trip.itinerary = data['itinerary']
            
        db.session.commit()
        return jsonify({'message': 'Trip updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@trips_bp.route('/<int:trip_id>', methods=['DELETE'])
@auth_required
def delete_trip(trip_id):
    current_user = get_current_user()
    trip = current_user.trips.filter_by(id=trip_id).first()
    
    if not trip:
        return jsonify({'error': 'Trip not found'}), 404
        
    try:
        db.session.delete(trip)
        db.session.commit()
        return jsonify({'message': 'Trip deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
