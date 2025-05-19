from datetime import datetime, timezone, timedelta
from app import db

class Trip(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destination = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    itinerary = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationship
    user = db.relationship('User', back_populates='trips')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generate default itinerary if none provided
        if self.itinerary is None and self.start_date and self.end_date:
            self.generate_default_itinerary()

    def get_duration_days(self):
        """Calculate trip duration in days"""
        delta = self.end_date - self.start_date
        return max(1, delta.days + 1)  # Minimum 1 day

    def generate_default_itinerary(self):
        """Generate a default itinerary template based on trip duration"""
        duration = self.get_duration_days()
        itinerary = {}
        
        time_slots = {
            'morning': '9:00 AM - 12:00 PM',
            'afternoon': '1:00 PM - 5:00 PM',
            'evening': '6:00 PM - 10:00 PM'
        }
        
        for day in range(1, duration + 1):
            day_key = f'day{day}'
            itinerary[day_key] = {
                slot: {
                    'time': time_range,
                    'activity': 'Plan your activity',
                    'location': '',
                    'notes': ''
                }
                for slot, time_range in time_slots.items()
            }
        
        self.itinerary = itinerary
        return itinerary

    def __repr__(self):
        return f'<Trip {self.destination}>'
