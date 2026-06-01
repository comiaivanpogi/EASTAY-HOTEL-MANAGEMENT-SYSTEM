import re

with open('static/js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace BOOKING block
old_booking_block_pattern = re.compile(r'// ============================================================\n//  BOOKING\n// ============================================================.*?// ============================================================\n//  ADMIN FUNCTIONS', re.DOTALL)

new_booking_block = """// ============================================================
//  BOOKING
// ============================================================
let currentBookingRoom = null;
let fpIn = null;
let fpOut = null;

function openBookingModal(id, name) {
    const room = rooms.find(r => r.id === id);
    if (!room) return;
    currentBookingRoom = room;
    
    document.getElementById('bm-room-id').value = id;
    document.getElementById('bm-room-name').innerText = name;
    
    // Fill in room details preview
    document.getElementById('bm-room-img').src = room.img || 'https://via.placeholder.com/400';
    document.getElementById('bm-room-status').innerText = room.status;
    document.getElementById('bm-room-status').className = `badge badge-${room.status.toLowerCase()}`;
    if (room.status === 'Available') {
        document.getElementById('bm-room-status').style.background = '#d4edda';
        document.getElementById('bm-room-status').style.color = '#155724';
    } else {
        document.getElementById('bm-room-status').style.background = '#f8d7da';
        document.getElementById('bm-room-status').style.color = '#721c24';
    }
    
    document.getElementById('bm-room-price').innerText = room.price.toLocaleString();
    document.getElementById('bm-room-bed').innerText = room.bed || 'Standard Bed';
    document.getElementById('bm-room-cap').innerText = room.capacity || 2;
    
    const incl = document.getElementById('bm-room-amenities');
    const amenities = room.amenities || [];
    incl.innerHTML = amenities.map(a => {
        const info = AMENITY_LABELS[a] || { icon: 'fa-check', label: a };
        return `<span style="font-size:0.7rem; background:#eee; padding:4px 8px; border-radius:4px;"><i class="fas ${info.icon}"></i> ${info.label}</span>`;
    }).join('');
    
    // Auto-fill logged in user
    if (currentUser) {
        document.getElementById('bm-guest-name').value = currentUser.name || '';
        document.getElementById('bm-guest-email').value = currentUser.email || '';
    }
    
    // Reset Form
    document.getElementById('form-booking').reset();
    document.getElementById('bm-guests').value = 1;
    document.getElementById('bm-calc-price').innerText = room.price.toLocaleString();
    document.getElementById('bm-calc-nights').innerText = '0';
    document.getElementById('bm-calc-subtotal').innerText = '0';
    document.getElementById('bm-calc-total').innerText = '0';
    document.getElementById('bm-error').innerText = '';
    document.getElementById('bm-success').style.display = 'none';
    
    // Init flatpickr
    if (fpIn) fpIn.destroy();
    if (fpOut) fpOut.destroy();
    
    fpIn = flatpickr("#bm-check-in", {
        minDate: "today",
        onChange: function(selectedDates, dateStr, instance) {
            if (selectedDates.length > 0) {
                fpOut.set("minDate", new Date(selectedDates[0].getTime() + 24 * 60 * 60 * 1000));
                calculatePrice();
            }
        }
    });
    
    fpOut = flatpickr("#bm-check-out", {
        minDate: new Date(new Date().getTime() + 24 * 60 * 60 * 1000),
        onChange: function(selectedDates, dateStr, instance) {
            calculatePrice();
        }
    });

    document.getElementById('booking-modal').style.display = 'flex';
    setTimeout(() => {
        document.getElementById('booking-modal').style.opacity = '1';
        document.querySelector('#booking-modal .modal-content').style.transform = 'scale(1)';
    }, 10);
}

function updateGuestCount(delta) {
    const input = document.getElementById('bm-guests');
    let val = parseInt(input.value) + delta;
    if (val < 1) val = 1;
    if (currentBookingRoom && val > (currentBookingRoom.capacity || 10)) val = currentBookingRoom.capacity || 10;
    input.value = val;
}

function calculatePrice() {
    const dateIn = fpIn.selectedDates[0];
    const dateOut = fpOut.selectedDates[0];
    if (dateIn && dateOut && currentBookingRoom) {
        const diffTime = Math.abs(dateOut - dateIn);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        const total = diffDays * currentBookingRoom.price;
        
        document.getElementById('bm-calc-nights').innerText = diffDays;
        document.getElementById('bm-calc-subtotal').innerText = total.toLocaleString();
        document.getElementById('bm-calc-total').innerText = total.toLocaleString();
    }
}

async function submitBooking(e) {
    e.preventDefault();
    const errEl = document.getElementById('bm-error');
    errEl.innerText = '';
    
    const checkIn = document.getElementById('bm-check-in').value;
    const checkOut = document.getElementById('bm-check-out').value;
    if (!checkIn || !checkOut) { 
        errEl.innerText = 'Please select valid check-in and check-out dates.'; 
        return; 
    }
    
    const newBooking = {
        roomId: parseInt(document.getElementById('bm-room-id').value),
        checkIn,
        checkOut,
        guests: parseInt(document.getElementById('bm-guests').value),
        guestName: document.getElementById('bm-guest-name').value,
        guestEmail: document.getElementById('bm-guest-email').value,
        guestPhone: document.getElementById('bm-guest-phone').value,
        specialRequests: document.getElementById('bm-special').value,
        preferredPayment: document.getElementById('bm-payment').value
    };
    
    const btn = document.getElementById('bm-submit-btn');
    const spinner = document.getElementById('bm-spinner');
    const btnText = document.getElementById('bm-submit-text');
    
    btn.disabled = true;
    spinner.style.display = 'inline-block';
    btnText.innerText = 'Processing...';

    try {
        const res = await fetch('/api/bookings/', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${currentToken}`
            },
            body: JSON.stringify(newBooking)
        });
        const data = await res.json();
        
        if (data.success) {
            document.getElementById('bm-success').style.display = 'flex';
            await loadInitialData();
        } else {
            errEl.innerText = data.message || 'Error submitting booking.';
        }
    } catch (err) {
        errEl.innerText = 'Network Error. Please try again.';
    } finally {
        btn.disabled = false;
        spinner.style.display = 'none';
        btnText.innerText = 'Send Booking Request';
    }
}

// ============================================================
//  ADMIN FUNCTIONS"""

js = old_booking_block_pattern.sub(new_booking_block, js)

# Replace closeModals block
old_close_modal_pattern = re.compile(r'function closeModals\(\) \{.*?\}', re.DOTALL)
new_close_modal = """function closeModals() {
    document.querySelectorAll('.modal-overlay').forEach(m => {
        m.style.opacity = '0';
        const content = m.querySelector('.modal-content');
        if(content) content.style.transform = 'scale(0.95)';
        setTimeout(() => { m.style.display = 'none'; }, 300);
    });
}"""
js = old_close_modal_pattern.sub(new_close_modal, js)

with open('static/js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)

