import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Landing Page CSS
landing_css = """
        /* LANDING PAGE STYLES */
        #landing-screen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100vh;
            z-index: 1000;
            background: #fff;
            overflow-y: auto;
            transition: opacity 0.5s ease, visibility 0.5s ease;
        }

        .hero {
            height: 100vh;
            background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), url('/static/img/hero.png');
            background-size: cover;
            background-position: center;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            color: #fff;
            padding: 0 20px;
        }

        .hero h1 {
            font-size: 4rem;
            font-weight: 800;
            margin-bottom: 20px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.3);
            animation: fadeInUp 1s ease;
        }

        .hero p {
            font-size: 1.2rem;
            max-width: 600px;
            margin-bottom: 40px;
            text-shadow: 0 2px 5px rgba(0,0,0,0.3);
            animation: fadeInUp 1.2s ease;
        }

        .hero .btn-primary {
            padding: 18px 40px;
            font-size: 1.1rem;
            animation: fadeInUp 1.4s ease;
        }

        .features-section {
            padding: 100px 20px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .features-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 40px;
        }

        .feature-card {
            background: #fff;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.05);
            text-align: center;
            transition: transform 0.3s ease;
        }

        .feature-card:hover {
            transform: translateY(-10px);
        }

        .feature-card i {
            font-size: 3rem;
            color: var(--primary);
            margin-bottom: 20px;
        }

        .feature-card h3 {
            font-size: 1.5rem;
            margin-bottom: 15px;
        }

        .feature-card p {
            color: #666;
            line-height: 1.6;
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
"""

html = html.replace('/* Orange accent */', '/* Orange accent */' + landing_css)

# Add Landing Page HTML
landing_html = """
    <!-- LANDING PAGE -->
    <div id="landing-screen">
        <div class="hero">
            <div style="position: absolute; top: 30px; left: 50px; font-weight: 800; font-size: 1.8rem; letter-spacing: -1px;">
                EASTAY<span style="color:var(--primary)">.</span>
            </div>
            <h1>Experience Pure Luxury</h1>
            <p>Discover the perfect blend of comfort and sophistication. Your premium gateway to unforgettable stays starts here.</p>
            <button class="btn btn-primary" onclick="goToAuth()">Get Started <i class="fas fa-arrow-right" style="margin-left:10px"></i></button>
        </div>

        <section class="features-section">
            <div style="text-align: center; margin-bottom: 60px;">
                <h2 style="font-size: 2.5rem; margin-bottom: 10px;">Why Choose Eastay?</h2>
                <p style="color: #888;">We provide world-class amenities and seamless booking experiences.</p>
            </div>
            <div class="features-grid">
                <div class="feature-card">
                    <i class="fas fa-bed"></i>
                    <h3>Luxury Rooms</h3>
                    <p>Elegantly designed spaces with premium furnishings and breathtaking views.</p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-shield-alt"></i>
                    <h3>Secure Booking</h3>
                    <p>State-of-the-art encryption ensures your data and transactions are always protected.</p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-concierge-bell"></i>
                    <h3>Premium Service</h3>
                    <p>Our dedicated team is available 24/7 to ensure your stay is absolutely perfect.</p>
                </div>
            </div>
        </section>

        <footer style="padding: 40px; text-align: center; background: #f8f9fa; color: #888; font-size: 0.9rem;">
            &copy; 2024 Eastay Hotel Management System. All rights reserved.
        </footer>
    </div>
"""

# Insert landing page at the beginning of the body
html = html.replace('<body>', '<body>' + landing_html)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
