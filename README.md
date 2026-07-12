# Savannah Woodlands — Event Registration Site

## Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional: for admin panel
python manage.py runserver
```

Then open http://127.0.0.1:8000

## Admin Panel
Access at http://127.0.0.1:8000/admin/ to view all registrations, ticket numbers, and QR codes.

## Pages
- `/`          — Homepage with event info and property showcase
- `/register/` — Registration form (name, email, phone, ticket type)
- `/ticket/<id>/` — Ticket page with QR code (auto-generated on registration)

## Notes
- QR codes are saved to `media/tickets/qr/`
- The ticket page has a Print button for physical tickets
- Each email can only register once
- Ticket numbers: SW-REG-XXXXXXXX (Regular) / SW-VIP-XXXXXXXX (VIP)
