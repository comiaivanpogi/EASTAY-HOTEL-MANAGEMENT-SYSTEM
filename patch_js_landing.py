import re

with open('static/js/main.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add goToAuth function
js_logic = """
function goToAuth() {
    const landing = document.getElementById('landing-screen');
    landing.style.opacity = '0';
    setTimeout(() => {
        landing.style.visibility = 'hidden';
        document.getElementById('auth-screen').classList.remove('hidden');
    }, 500);
}
"""

js = js.replace('let rooms = [];', 'let rooms = [];' + js_logic)

# Update loadInitialData to handle landing screen visibility
js = js.replace("document.getElementById('auth-screen').classList.add('hidden');", 
                "document.getElementById('landing-screen').style.display = 'none'; document.getElementById('auth-screen').classList.add('hidden');")

with open('static/js/main.js', 'w', encoding='utf-8') as f:
    f.write(js)
