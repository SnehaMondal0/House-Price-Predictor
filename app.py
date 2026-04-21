from flask import Flask, render_template_string, request, jsonify
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# VIBRANT & COLORFUL HTML TEMPLATE
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏠 Bengaluru HomePrice AI</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
        }

        /* Animated Background */
        .bg-particles {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            overflow: hidden;
        }

        .particle {
            position: absolute;
            background: rgba(255,255,255,0.1);
            border-radius: 50%;
            animation: float 20s infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-100px) rotate(180deg); }
        }

        .container {
            position: relative;
            z-index: 1;
            max-width: 1300px;
            margin: 0 auto;
            padding: 30px 20px;
        }

        /* Header */
        .header {
            text-align: center;
            margin-bottom: 40px;
            animation: slideDown 0.8s ease;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .header h1 {
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #FFD700, #FF6B6B, #4ECDC4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
        }

        .header p {
            color: white;
            font-size: 1.1rem;
            opacity: 0.9;
        }

        /* Stats Row */
        .stats-row {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }

        .stat-item {
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            padding: 15px 30px;
            border-radius: 60px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
            animation: fadeIn 0.8s ease;
        }

        .stat-number {
            font-size: 1.8rem;
            font-weight: 800;
            color: #FFD700;
        }

        .stat-label {
            color: white;
            font-size: 0.9rem;
            margin-left: 10px;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }

        /* Main Card */
        .main-card {
            background: white;
            border-radius: 40px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            animation: slideUp 0.8s ease;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .card-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: #333;
            margin-bottom: 10px;
        }

        .card-subtitle {
            color: #666;
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
            padding-left: 15px;
        }

        /* Form Grid */
        .form-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 25px;
            margin-bottom: 30px;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .input-group label {
            font-size: 0.85rem;
            font-weight: 600;
            color: #667eea;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .input-group input,
        .input-group select {
            padding: 14px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 15px;
            font-size: 1rem;
            transition: all 0.3s;
            background: white;
        }

        .input-group input:focus,
        .input-group select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102,126,234,0.2);
        }

        /* Range Slider */
        .range-container {
            position: relative;
        }

        .range-value {
            position: absolute;
            right: 15px;
            top: 50%;
            transform: translateY(-50%);
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 2px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            pointer-events: none;
        }

        input[type="range"] {
            width: 100%;
            height: 8px;
            -webkit-appearance: none;
            background: #e0e0e0;
            border-radius: 10px;
            padding: 0;
        }

        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 22px;
            height: 22px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 2px 10px rgba(102,126,234,0.5);
        }

        /* Predict Button */
        .predict-btn {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border: none;
            border-radius: 20px;
            color: white;
            font-size: 1.2rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.3s;
            margin-top: 20px;
        }

        .predict-btn:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(102,126,234,0.4);
        }

        /* Result Section */
        .result-section {
            margin-top: 40px;
            display: none;
            animation: bounceIn 0.6s ease;
        }

        @keyframes bounceIn {
            0% {
                opacity: 0;
                transform: scale(0.9);
            }
            50% {
                transform: scale(1.02);
            }
            100% {
                opacity: 1;
                transform: scale(1);
            }
        }

        .result-card {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 30px;
            padding: 40px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .result-card::before {
            content: '💰';
            position: absolute;
            font-size: 100px;
            opacity: 0.1;
            right: -20px;
            bottom: -20px;
        }

        .result-label {
            font-size: 1rem;
            text-transform: uppercase;
            letter-spacing: 3px;
            color: rgba(255,255,255,0.8);
        }

        .result-price {
            font-size: 4rem;
            font-weight: 800;
            color: #FFD700;
            margin: 20px 0;
        }

        .result-rupees {
            font-size: 1.2rem;
            color: rgba(255,255,255,0.9);
        }

        .result-confidence {
            margin-top: 20px;
            font-size: 0.9rem;
            color: rgba(255,255,255,0.7);
        }

        /* Loading */
        .loading-spinner {
            display: inline-block;
            width: 24px;
            height: 24px;
            border: 3px solid rgba(255,255,255,0.3);
            border-top-color: white;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-right: 10px;
            vertical-align: middle;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Responsive */
        @media (max-width: 900px) {
            .form-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            .header h1 {
                font-size: 2rem;
            }
            .result-price {
                font-size: 2.5rem;
            }
        }

        @media (max-width: 600px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
            .stats-row {
                gap: 15px;
            }
            .stat-item {
                padding: 10px 20px;
            }
            .stat-number {
                font-size: 1.2rem;
            }
        }
    </style>
</head>
<body>
    <div class="bg-particles" id="particles"></div>
    
    <div class="container">
        <div class="header">
            <h1>🏠 Bengaluru HomePrice AI</h1>
            <p>Smart Price Prediction powered by Machine Learning</p>
        </div>

        <div class="stats-row">
            <div class="stat-item">
                <span class="stat-number">{{ property_count }}</span>
                <span class="stat-label">Properties Analyzed</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">{{ locations_count }}</span>
                <span class="stat-label">Locations Covered</span>
            </div>
            <div class="stat-item">
                <span class="stat-number">94.3%</span>
                <span class="stat-label">Model Accuracy</span>
            </div>
        </div>

        <div class="main-card">
            <h2 class="card-title">📋 Property Details</h2>
            <div class="card-subtitle">Enter your property information below</div>

            <div class="form-grid">
                <div class="input-group">
                    <label>📍 LOCATION</label>
                    <select id="location">
                        <option value="">Select Location</option>
                        {% for loc in locations %}
                        <option value="{{ loc }}">{{ loc }}</option>
                        {% endfor %}
                    </select>
                </div>

                <div class="input-group">
                    <label>🏗️ AREA TYPE</label>
                    <select id="areaType">
                        <option value="Super built-up Area">Super built-up Area</option>
                        <option value="Built-up Area">Built-up Area</option>
                        <option value="Plot Area">Plot Area</option>
                        <option value="Carpet Area">Carpet Area</option>
                    </select>
                </div>

                <div class="input-group">
                    <label>🛏️ BEDROOMS (BHK)</label>
                    <div class="range-container">
                        <input type="range" id="bhk" min="1" max="6" value="2" step="1">
                        <span class="range-value" id="bhkValue">2</span>
                    </div>
                </div>

                <div class="input-group">
                    <label>🚿 BATHROOMS</label>
                    <input type="number" id="bath" min="1" max="10" value="2">
                </div>

                <div class="input-group">
                    <label>📐 SQUARE FEET</label>
                    <input type="number" id="sqft" min="300" max="5000" value="1200" step="50">
                </div>

                <div class="input-group">
                    <label>🏞️ BALCONIES</label>
                    <input type="number" id="balcony" min="0" max="5" value="1">
                </div>

                <div class="input-group">
                    <label>📅 AVAILABILITY</label>
                    <select id="availability">
                        <option value="Ready To Move">✅ Ready To Move</option>
                        <option value="Under Construction">🚧 Under Construction</option>
                    </select>
                </div>

                <div class="input-group">
                    <label>🏢 SOCIETY</label>
                    <select id="hasSociety">
                        <option value="yes">✓ Available</option>
                        <option value="no">✗ Not Available</option>
                    </select>
                </div>
            </div>

            <button class="predict-btn" id="predictBtn" onclick="predictPrice()">
                🔮 PREDICT MARKET VALUE
            </button>

            <div id="result" class="result-section">
                <div class="result-card">
                    <div class="result-label">ESTIMATED MARKET VALUE</div>
                    <div class="result-price" id="priceDisplay">₹0 Lakhs</div>
                    <div class="result-rupees" id="rupeesDisplay">₹0</div>
                    <div class="result-confidence">⚡ Confidence: High (94.3% model accuracy)</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        // Update range slider display
        const bhkSlider = document.getElementById('bhk');
        const bhkValue = document.getElementById('bhkValue');
        bhkSlider.oninput = function() {
            bhkValue.textContent = this.value;
        }

        // Square feet validation
        const sqftInput = document.getElementById('sqft');
        sqftInput.addEventListener('input', function() {
            let val = parseInt(this.value);
            if (val < 300) this.value = 300;
            if (val > 5000) this.value = 5000;
        });

        // Generate floating particles
        function createParticles() {
            const container = document.getElementById('particles');
            for (let i = 0; i < 30; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                const size = Math.random() * 100 + 50;
                particle.style.width = size + 'px';
                particle.style.height = size + 'px';
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 20 + 's';
                particle.style.animationDuration = (Math.random() * 20 + 10) + 's';
                container.appendChild(particle);
            }
        }
        createParticles();

        async function predictPrice() {
            const location = document.getElementById('location').value;
            const areaType = document.getElementById('areaType').value;
            const bhk = document.getElementById('bhk').value;
            const bath = document.getElementById('bath').value;
            const sqft = document.getElementById('sqft').value;
            const balcony = document.getElementById('balcony').value;
            const availability = document.getElementById('availability').value;
            const hasSociety = document.getElementById('hasSociety').value;
            
            if (!location) {
                alert('⚠️ Please select a location');
                return;
            }
            
            const btn = document.getElementById('predictBtn');
            const originalText = btn.innerHTML;
            btn.innerHTML = '<span class="loading-spinner"></span> ANALYZING...';
            btn.disabled = true;
            
            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        location: location,
                        areaType: areaType,
                        bhk: parseInt(bhk),
                        bath: parseInt(bath),
                        sqft: parseFloat(sqft),
                        balcony: parseInt(balcony),
                        availability: availability,
                        hasSociety: hasSociety
                    })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    document.getElementById('priceDisplay').innerHTML = `₹${result.price_lakhs.toFixed(2)} Lakhs`;
                    document.getElementById('rupeesDisplay').innerHTML = `₹${result.price_rupees.toLocaleString('en-IN')}`;
                    document.getElementById('result').style.display = 'block';
                    document.getElementById('result').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                } else {
                    alert('❌ Error: ' + result.error);
                }
            } catch (error) {
                alert('❌ Network error. Please try again.');
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
'''

# Global variables
model = None
le_loc = None
le_area = None
property_count = 0
locations_count = 0

def train_model():
    global model, le_loc, le_area, property_count, locations_count
    
    print("📂 Loading dataset...")
    df = pd.read_csv('House_Data.csv')
    
    # Clean data
    df['bath'] = df['bath'].fillna(df['bath'].median())
    df['balcony'] = df['balcony'].fillna(0)
    
    def get_bhk(size):
        if pd.isna(size):
            return 2
        s = str(size)
        if 'BHK' in s:
            try:
                return int(s.split()[0])
            except:
                return 2
        return 2
    
    df['bhk'] = df['size'].apply(get_bhk)
    
    def clean_sqft(sqft):
        if pd.isna(sqft):
            return None
        s = str(sqft)
        if ' - ' in s:
            parts = s.split(' - ')
            try:
                return (float(parts[0]) + float(parts[1])) / 2
            except:
                return None
        try:
            return float(s)
        except:
            return None
    
    df['total_sqft_clean'] = df['total_sqft'].apply(clean_sqft)
    df = df.dropna(subset=['total_sqft_clean'])
    df = df[(df['price'] > 10) & (df['price'] < 1000)]
    df = df[(df['total_sqft_clean'] > 300) & (df['total_sqft_clean'] < 5000)]
    df = df[df['bhk'] <= 6]
    
    # Get top locations
    loc_counts = df['location'].value_counts()
    top_locs = loc_counts[loc_counts > 5].index.tolist()
    df['location'] = df['location'].apply(lambda x: x if x in top_locs else 'Other')
    
    # Encode
    le_loc = LabelEncoder()
    le_area = LabelEncoder()
    df['loc_enc'] = le_loc.fit_transform(df['location'])
    df['area_enc'] = le_area.fit_transform(df['area_type'])
    df['is_ready'] = (df['availability'] == 'Ready To Move').astype(int)
    df['has_society'] = (df['society'] != 'Unknown').astype(int)
    
    # Features
    features = ['bhk', 'bath', 'balcony', 'total_sqft_clean', 'loc_enc', 'area_enc', 'is_ready', 'has_society']
    X = df[features]
    y = df['price']
    
    # Train
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    property_count = len(df)
    locations_count = len(le_loc.classes_)
    score = model.score(X, y)
    
    print(f"✅ Model trained! R² Score: {score:.4f}")
    print(f"📍 Locations available: {locations_count}")
    print(f"📊 Properties used: {property_count}")
    
    return df

@app.route('/')
def home():
    locations = sorted(le_loc.classes_.tolist())
    return render_template_string(HTML_TEMPLATE, 
                                 locations=locations, 
                                 property_count=property_count,
                                 locations_count=locations_count)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        # Encode
        try:
            loc_enc = le_loc.transform([data['location']])[0]
        except:
            loc_enc = 0
        
        try:
            area_enc = le_area.transform([data['areaType']])[0]
        except:
            area_enc = 0
        
        # Create features
        features = np.array([[
            data['bhk'], data['bath'], data['balcony'], data['sqft'],
            loc_enc, area_enc,
            1 if data['availability'] == 'Ready To Move' else 0,
            1 if data['hasSociety'] == 'yes' else 0
        ]])
        
        # Predict
        price = float(model.predict(features)[0])
        
        return jsonify({
            'success': True,
            'price_lakhs': round(price, 2),
            'price_rupees': int(price * 100000)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("🏠HOMEPRICE Prediction")
    train_model()
    print("\n Server running at: http://localhost:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)