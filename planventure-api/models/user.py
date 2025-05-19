from datetime import datetime, timezone, timedelta
from app import db
import bcrypt
from flask_jwt_extended import create_access_token
from flask_jwt_extended import decode_token
from email_validator import validate_email, EmailNotValidError

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationship
    trips = db.relationship('Trip', back_populates='user', lazy='dynamic')

    def set_password(self, password):
        """Hash a password with salt using bcrypt"""
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.password_hash = password_hash.decode('utf-8')

    def check_password(self, password):
        """Check if provided password matches the hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    @property
    def password(self):
        """Prevent password from being accessed"""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """Set password hash"""
        self.set_password(password)

    def generate_auth_token(self, expires_delta=None):
        """Generate JWT token for the user"""
        expires = (
            datetime.now(timezone.utc) + timedelta(seconds=expires_delta)
            if expires_delta
            else None
        )
        return create_access_token(
            identity=str(self.id),  # Convert ID to string
            expires_delta=expires,
            additional_claims={'email': self.email}
        )

    @staticmethod
    def verify_auth_token(token):
        """Verify JWT token and return User instance"""
        try:
            data = decode_token(token)
            return User.query.get(data['sub'])
        except:
            return None

    @staticmethod
    def validate_email(email):
        try:
            valid = validate_email(email)
            return valid.email
        except EmailNotValidError:
            return None

    def __repr__(self):
        return f'<User {self.email}>'
