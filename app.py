# c:\Users\Kenneth\OneDrive\Documents\FINAL PROJECT_IVAN\app.py

from app import create_app, db, bcrypt
from app.models import User, Room, Review, Staff, Service
import os
import sys

app = create_app()

def seed_database():
    with app.app_context():
        try:
            print("Checking database...")
            db.create_all()
            
            user_count = User.query.count()
            if user_count == 0:
                print("Database is empty. Initializing and seeding...")
                
                # 1. Seed Admin
                hashed_admin_pw = bcrypt.generate_password_hash('Admin@123').decode('utf-8')
                admin = User(email='admin@eastay.com', password_hash=hashed_admin_pw, name='System Admin', role='admin')
                db.session.add(admin)
                
                # 2. Seed Guest
                hashed_user_pw = bcrypt.generate_password_hash('User@123').decode('utf-8')
                user = User(email='user@eastay.com', password_hash=hashed_user_pw, name='Guest User', role='user')
                db.session.add(user)
                
                db.session.commit()
                
                # 3. Seed Rooms
                rooms_data = [
                    { "name": "Ocean View Deluxe", "type": "Deluxe", "price": 3500, "img": "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=800&q=80", "status": "Available", "capacity": 2, "rating": 5, "amenities": "wifi,ac,tv,breakfast", "bed": "King Bed", "size": 42, "view": "Ocean View", "description": "A luxurious deluxe room featuring breathtaking ocean views from a private balcony. Elegantly furnished with modern decor, the room offers a serene retreat perfect for couples seeking a romantic coastal getaway." },
                    { "name": "Royal Presidential Suite", "type": "Presidential", "price": 12000, "img": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80", "status": "Available", "capacity": 4, "rating": 5, "amenities": "wifi,ac,tv,breakfast,pool,spa", "bed": "King Bed", "size": 120, "view": "Ocean View", "description": "The pinnacle of luxury — our Royal Presidential Suite offers unrivaled grandeur with a full living area, private dining room, butler service, and panoramic ocean views. Experience royalty at its finest." },
                    { "name": "Family Garden View", "type": "Family", "price": 4500, "img": "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?auto=format&fit=crop&w=800&q=80", "status": "Available", "capacity": 6, "rating": 4, "amenities": "wifi,ac,tv,parking", "bed": "Twin Beds", "size": 65, "view": "Garden View", "description": "Spacious and family-friendly, this room overlooks our lush tropical garden. With multiple sleeping arrangements and generous space, it is the ideal choice for families traveling together." },
                    { "name": "Standard Modern Loft", "type": "Standard", "price": 1800, "img": "https://images.unsplash.com/photo-1505691938895-1758d7eaa511?auto=format&fit=crop&w=800&q=80", "status": "Available", "capacity": 1, "rating": 3, "amenities": "wifi,ac", "bed": "Double Bed", "size": 25, "view": "City View", "description": "A smart, efficiently designed loft-style room ideal for solo travelers and business guests. Clean, modern interiors with all the essentials for a comfortable stay at an affordable price." },
                    { "name": "Sunset Executive Suite", "type": "Suite", "price": 7500, "img": "https://images.unsplash.com/photo-1591088398332-8a7791972843?auto=format&fit=crop&w=800&q=80", "status": "Available", "capacity": 2, "rating": 5, "amenities": "wifi,ac,tv,breakfast,gym", "bed": "Queen Bed", "size": 80, "view": "Pool View", "description": "Watch the golden sunset from your private terrace in this executive suite. Featuring a separate lounge area, premium furnishings, and exclusive pool access, this suite blends comfort with sophistication." }
                ]
                for r in rooms_data:
                    db.session.add(Room(**r))
                
                # 4. Seed Staff
                staff_data = [
                    { "name": "Ivan Comia", "email": "ivan@eastay.com", "role": "Hotel Manager", "phone": "09123456789", "salary": 45000 },
                    { "name": "Maria Clara", "email": "maria@eastay.com", "role": "Front Desk", "phone": "09987654321", "salary": 18000 },
                    { "name": "Juan Dela Cruz", "email": "juan@eastay.com", "role": "Housekeeping", "phone": "09112223334", "salary": 15000 }
                ]
                for s in staff_data:
                    db.session.add(Staff(**s))
                    
                # 5. Seed Services
                services_data = [
                    { "name": "Luxury Spa & Massage", "description": "Full body relaxation massage and aromatherapy.", "price": 1500, "icon": "fa-spa" },
                    { "name": "Airport Transfer", "description": "Private car service to and from the airport.", "price": 800, "icon": "fa-car" },
                    { "name": "Guided Island Tour", "description": "Whole day tour of the best scenic spots nearby.", "price": 2500, "icon": "fa-map-marked-alt" }
                ]
                for svc in services_data:
                    db.session.add(Service(**svc))
                
                db.session.commit()
                
                # 6. Seed initial Reviews
                room1 = Room.query.first()
                if room1:
                    db.session.add(Review(user_id=2, room_id=room1.id, rating=5, comment="Amazing stay! The ocean view was stunning."))
                
                db.session.commit()
                print("Database seeded successfully with Rooms, Staff, Services, and Reviews.")
            else:
                print(f"Database already contains {user_count} users. Skipping seeding.")
        except Exception as e:
            print(f"Error during seeding: {str(e)}")
            db.session.rollback()


import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open_new("https://127.0.0.1:5000/")

if __name__ == '__main__':
    seed_database()
    print("\nStarting Flask server on https://127.0.0.1:5000")
    print("NOTE: If you see a 'Network Error' in the browser, make sure you are using HTTPS.")
    
    Timer(1.5, open_browser).start()
    
    try:
        app.run(debug=True, port=5000, ssl_context='adhoc', use_reloader=False)
    except ImportError:
        print("\nERROR: Missing 'pyopenssl'. Run this command: pip install pyopenssl")
    except Exception as e:
        print(f"\nServer error: {str(e)}")
