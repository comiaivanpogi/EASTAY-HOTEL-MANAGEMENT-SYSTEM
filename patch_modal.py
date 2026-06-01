import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Flatpickr CDN to head
flatpickr_css = '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">'
if 'flatpickr' not in html:
    html = html.replace('</head>', f'    {flatpickr_css}\n</head>')

flatpickr_js = '<script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>'
if 'flatpickr' not in html.split('</head>')[1]:
    html = html.replace('</body>', f'    {flatpickr_js}\n</body>')

# Replace the old booking modal
old_modal_pattern = re.compile(r'<!-- BOOKING MODAL -->.*?</div>\s*</div>', re.DOTALL)

new_modal = """<!-- BOOKING MODAL -->
    <div class="modal-overlay" id="booking-modal" style="opacity:0; transition: opacity 0.3s ease;">
        <div class="modal-content" style="max-width: 900px; padding: 0; overflow: hidden; transform: scale(0.95); transition: transform 0.3s ease; display:flex; flex-direction:row; flex-wrap: wrap;">
            
            <!-- Left Side: Room Preview -->
            <div style="flex: 1; min-width: 300px; background: #f8f9fa; border-right: 1px solid #eee; display:flex; flex-direction:column;">
                <img id="bm-room-img" src="" style="width: 100%; height: 250px; object-fit: cover;">
                <div style="padding: 25px;">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <h3 id="bm-room-name" style="font-size: 1.4rem; font-weight: 800; margin:0;"></h3>
                        <span id="bm-room-status" class="badge" style="font-size:0.7rem;"></span>
                    </div>
                    <div style="color:var(--primary); font-size:1.2rem; font-weight:700; margin-bottom:20px;">
                        &#8369;<span id="bm-room-price"></span> <span style="font-size:0.8rem; color:#888; font-weight:400;">/ night</span>
                    </div>
                    
                    <div style="font-size:0.9rem; color:#555; margin-bottom:15px;">
                        <i class="fas fa-bed" style="width:20px; color:var(--primary);"></i> <span id="bm-room-bed"></span>
                    </div>
                    <div style="font-size:0.9rem; color:#555; margin-bottom:15px;">
                        <i class="fas fa-user-friends" style="width:20px; color:var(--primary);"></i> Up to <span id="bm-room-cap"></span> guests
                    </div>
                    <div id="bm-room-amenities" style="display:flex; flex-wrap:wrap; gap:10px; margin-top:20px;">
                        <!-- Amenities injected here -->
                    </div>
                </div>
            </div>

            <!-- Right Side: Booking Form -->
            <div style="flex: 1.2; min-width: 350px; padding: 35px; position:relative;">
                <span class="close-modal" onclick="closeModals()" style="position:absolute; right:25px; top:20px;">&times;</span>
                <h3 style="font-size: 1.3rem; margin-bottom: 25px;">Complete Your Booking</h3>
                
                <form id="form-booking" onsubmit="submitBooking(event)">
                    <input type="hidden" id="bm-room-id">
                    
                    <!-- Guest Details -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom:15px;">
                        <div>
                            <label style="font-size: 0.75rem; font-weight: 700; color:#555;">FULL NAME</label>
                            <input type="text" id="bm-guest-name" required placeholder="John Doe">
                        </div>
                        <div>
                            <label style="font-size: 0.75rem; font-weight: 700; color:#555;">EMAIL ADDRESS</label>
                            <input type="email" id="bm-guest-email" required placeholder="john@example.com">
                        </div>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom:15px;">
                        <div>
                            <label style="font-size: 0.75rem; font-weight: 700; color:#555;">PHONE NUMBER</label>
                            <input type="tel" id="bm-guest-phone" required placeholder="+63 900 000 0000">
                        </div>
                        <div>
                            <label style="font-size: 0.75rem; font-weight: 700; color:#555;">GUESTS</label>
                            <div style="display:flex; align-items:center; border:1px solid #e0e0e0; border-radius:10px; overflow:hidden;">
                                <button type="button" onclick="updateGuestCount(-1)" style="flex:1; background:#f8f9fa; border:none; padding:12px; cursor:pointer; font-weight:bold; font-size:1.2rem;">-</button>
                                <input type="number" id="bm-guests" min="1" max="10" value="1" readonly style="flex:2; border:none; text-align:center; padding:12px; border-radius:0; font-weight:bold;">
                                <button type="button" onclick="updateGuestCount(1)" style="flex:1; background:#f8f9fa; border:none; padding:12px; cursor:pointer; font-weight:bold; font-size:1.2rem;">+</button>
                            </div>
                        </div>
                    </div>

                    <!-- Dates -->
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom:15px;">
                        <div>
                            <label style="font-size: 0.75rem; font-weight: 700; color:#555;">CHECK-IN</label>
                            <input type="text" id="bm-check-in" required placeholder="Select Date" style="background:#fff;">
                        </div>
                        <div>
                            <label style="font-size: 0.75rem; font-weight: 700; color:#555;">CHECK-OUT</label>
                            <input type="text" id="bm-check-out" required placeholder="Select Date" style="background:#fff;">
                        </div>
                    </div>
                    
                    <!-- Extras -->
                    <div style="margin-bottom:15px;">
                        <label style="font-size: 0.75rem; font-weight: 700; color:#555;">SPECIAL REQUESTS (OPTIONAL)</label>
                        <textarea id="bm-special" rows="2" placeholder="Any specific needs or preferences?" style="width:100%; padding:12px; border:1px solid #e0e0e0; border-radius:10px; font-family:inherit; resize:none;"></textarea>
                    </div>
                    <div style="margin-bottom:25px;">
                        <label style="font-size: 0.75rem; font-weight: 700; color:#555;">PREFERRED PAYMENT METHOD</label>
                        <select id="bm-payment" required style="width:100%;">
                            <option value="Online Payment">Online Payment (Credit/Debit)</option>
                            <option value="Cashier">Cashier / Front Desk</option>
                        </select>
                    </div>

                    <!-- Price Calculation -->
                    <div style="background:#f8f9fa; padding:15px; border-radius:10px; margin-bottom:25px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:5px; font-size:0.9rem;">
                            <span style="color:#555;">&#8369;<span id="bm-calc-price">0</span> x <span id="bm-calc-nights">0</span> nights</span>
                            <span style="font-weight:600;">&#8369;<span id="bm-calc-subtotal">0</span></span>
                        </div>
                        <hr style="border:none; border-top:1px dashed #ccc; margin:10px 0;">
                        <div style="display:flex; justify-content:space-between; font-weight:800; font-size:1.1rem; color:var(--primary);">
                            <span>Total Due</span>
                            <span>&#8369;<span id="bm-calc-total">0</span></span>
                        </div>
                    </div>

                    <div id="bm-error" style="color:var(--danger); font-size:0.85rem; margin-bottom:15px; font-weight:600;"></div>
                    
                    <div style="display:flex; gap:10px;">
                        <button type="button" class="btn btn-outline" style="flex:1; justify-content:center;" onclick="closeModals()">Cancel</button>
                        <button type="submit" class="btn btn-primary" id="bm-submit-btn" style="flex:2; justify-content:center;">
                            <span id="bm-submit-text">Send Booking Request</span>
                            <i class="fas fa-spinner fa-spin" id="bm-spinner" style="display:none; margin-left:10px;"></i>
                        </button>
                    </div>
                </form>
                
                <!-- Success Message Overlay -->
                <div id="bm-success" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(255,255,255,0.95); flex-direction:column; justify-content:center; align-items:center; padding:40px; text-align:center; z-index:10; border-radius:16px;">
                    <i class="fas fa-check-circle" style="font-size:4rem; color:#27ae60; margin-bottom:20px;"></i>
                    <h3 style="font-size:1.5rem; margin-bottom:10px;">Booking Requested!</h3>
                    <p style="color:#666; margin-bottom:30px;">Your request has been sent successfully. You can track its status in the My Bookings tab.</p>
                    <button type="button" class="btn btn-primary" onclick="closeModals()" style="justify-content:center; width:100%;">Got it</button>
                </div>

            </div>
        </div>
    </div>"""

html = old_modal_pattern.sub(new_modal, html)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
