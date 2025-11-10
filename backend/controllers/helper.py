from collections import defaultdict
from typing import Optional

from flask import current_app, flash, jsonify, redirect, request, url_for
from itsdangerous import URLSafeTimedSerializer as Serializer, BadSignature, SignatureExpired

from models import Reservation

def get_daywise_booking_data(user_id):
    
    reservations = Reservation.query.filter(
        Reservation.user_id == user_id,
        Reservation.leaving_timestamp.isnot(None)
    ).all()

    day_duration = defaultdict(float)

    for res in reservations:
        start = res.parking_timestamp
        end = res.leaving_timestamp
        if start and end:
            hours = (end - start).total_seconds() / 3600.0
            day_key = start.strftime("%Y-%m-%d")
            day_duration[day_key] += hours
    sorted_days = sorted(day_duration.keys())
    labels = sorted_days
    data = [round(day_duration[d], 2) for d in sorted_days]
    return labels, data


def _wants_json_response() -> bool:
    """Determine if the incoming request expects a JSON response."""
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return True
    accept = (request.headers.get('Accept') or '').lower()
    return 'application/json' in accept


def unauthorized_response(message: str = 'Unauthorized', redirect_endpoint: str = 'index'):
    """Return a response suitable for unauthorized access."""
    if _wants_json_response():
        return jsonify({'error': message}), 403
    flash(message)
    return redirect(url_for(redirect_endpoint))


def get_client_role() -> str:
    """Return the client-provided role from request headers or token if available."""
    # First try to get from header
    role = request.headers.get('X-Client-Role')
    if role:
        return role.lower()
    
    # If not in header, try to extract from token
    token = get_token_from_request()
    if token:
        payload = verify_token(token)
        if payload and 'role' in payload:
            return payload['role'].lower()
    
    return ''


def get_client_user_id() -> Optional[int]:
    """Return the client-provided user id from request headers or token if available."""
    # First try to get from header
    raw_user_id = request.headers.get('X-Client-UserId')
    if raw_user_id is not None:
        try:
            return int(raw_user_id)
        except (TypeError, ValueError):
            pass
    
    # If not in header, try to extract from token
    token = get_token_from_request()
    if token:
        payload = verify_token(token)
        if payload and 'user_id' in payload:
            return payload['user_id']
    
    return None


def ensure_role(required_role: str, message: str = 'Unauthorized access!', redirect_endpoint: str = 'index'):
    """Ensure the client supplied role matches the required role."""
    client_role = get_client_role()
    if client_role != required_role:
        return unauthorized_response(message=message, redirect_endpoint=redirect_endpoint)
    return None


def optional_login_required(f):
    """Decorator that allows token-based auth OR Flask-Login session."""
    from functools import wraps
    from flask_login import current_user
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if token-based auth is present
        token = get_token_from_request()
        if token:
            payload = verify_token(token)
            if payload and 'role' in payload:
                # Token is valid, allow request
                return f(*args, **kwargs)
        
        # Fall back to Flask-Login session check
        from flask_login import login_required
        return login_required(f)(*args, **kwargs)
    
    return decorated_function


def verify_token(token: str) -> Optional[dict]:
    """Verify and decode a token. Returns the payload if valid, None otherwise."""
    if not token:
        return None
    try:
        s = Serializer(current_app.config['SECRET_KEY'])
        payload = s.loads(token, salt='auth-token', max_age=86400)  # 24 hours
        return payload
    except (BadSignature, SignatureExpired, ValueError):
        return None


def get_token_from_request() -> Optional[str]:
    """Extract token from Authorization header."""
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        return auth_header[7:]  # Remove 'Bearer ' prefix
    return None