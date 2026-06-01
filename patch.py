import re
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add jsPDF to head
html = html.replace('</head>', '    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>\n</head>')

# 2. Add Payment Modals before the closing body
payment_modals = '''
    <!-- PAYMENT MODAL -->
    <div class="modal-overlay" id="payment-modal">
        <div class="modal-content" style="max-width: 500px;">
            <span class="close-modal" onclick="closeModals()">&times;</span>
            <h3 style="font-size: 1.5rem; margin-bottom: 20px;">Process Payment</h3>
            <div id="pay-alert" style="display:none; color:#e74c3c; margin-bottom:15px; font-weight:bold; font-size: 0.9rem;"></div>
            <form id="form-payment" onsubmit="submitPayment(event)">
                <input type="hidden" id="pay-booking-id">
                <label style="font-size: 0.8rem; font-weight: 700;">PAYMENT METHOD</label>
                <select id="pay-method" required>
                    <option value="Online Payment">Online Payment (Credit/Debit)</option>
                    <option value="Cashier">Cashier / Front Desk</option>
                </select>
                <p style="font-size:0.8rem; color:#888; margin-top:10px;">Note: Online payment is simulated for this demo.</p>
                <button type="submit" class="btn btn-primary" style="width: 100%; margin-top: 30px; justify-content: center;">Pay Now</button>
            </form>
        </div>
    </div>

    <!-- RECEIPT MODAL -->
    <div class="modal-overlay" id="receipt-modal">
        <div class="modal-content" style="max-width: 500px; text-align: center;">
            <span class="close-modal" onclick="closeModals()">&times;</span>
            <h3 style="font-size: 1.5rem; margin-bottom: 20px;">Payment Success!</h3>
            <img id="receipt-qr" src="" style="width:200px; height:200px; margin:0 auto 20px; display:block;">
            <p style="color:#636e72; margin-bottom:20px;">Your booking is confirmed.</p>
            <button id="btn-download-pdf" class="btn btn-primary" style="width: 100%; justify-content: center;" onclick="downloadReceipt()">Download PDF Receipt</button>
        </div>
    </div>
'''
html = html.replace('</body>', payment_modals + '\n</body>')

# 3. Add toggle password icon
html = html.replace('<input type="password" id="auth-pass" placeholder="123456789">', 
'<div style="position:relative;"><input type="password" id="auth-pass" placeholder="123456789"><i class="fas fa-eye" id="toggle-pass" style="position:absolute; right:15px; top:22px; cursor:pointer; color:#888;" onclick="togglePassword()"></i></div>')

# 4. Remove inline script and replace with <script src="/js/main.js">
html = re.sub(r'<script>[\s\S]*?</script>', '<script src="/js/main.js"></script>', html)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
