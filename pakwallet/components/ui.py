"""UI Components for PakWallet."""

import streamlit as st

def inject_global_css() -> None:
    """Inject custom CSS for premium Pakistan-themed dark-mode/glassmorphic styling."""
    
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
        
        <style>
        /* Base typography & theme overrides */
        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', 'Outfit', sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            letter-spacing: -0.02em;
        }

        /* Premium Pakistan Green & Gold Accent Palette */
        :root {
            --pak-green-dark: #013217;
            --pak-green: #01411C;
            --pak-green-light: #0d5c2c;
            --pak-gold: #D4AF37;
            --pak-gold-light: #f3d458;
            --glass-bg: rgba(17, 34, 27, 0.7);
            --glass-border: rgba(212, 175, 55, 0.15);
        }

        /* Custom Header block used in login and screens */
        .pak-header {
            background: linear-gradient(135deg, var(--pak-green-dark) 0%, var(--pak-green) 50%, #025928 100%);
            border-left: 5px solid var(--pak-gold);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(8px);
            border: 1px solid var(--glass-border);
        }

        .pak-header h1 {
            color: #ffffff !important;
            margin: 0 !important;
            font-size: 2.8rem !important;
            font-weight: 800 !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }

        .pak-tagline {
            color: var(--pak-gold) !important;
            font-size: 1.1rem;
            font-weight: 600;
            margin-top: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* Cards and Containers styling */
        .metric-card {
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-4px);
            border-color: rgba(212, 175, 55, 0.4);
        }
        
        /* Utility text styles */
        .text-gold {
            color: var(--pak-gold) !important;
        }
        
        .text-green {
            color: #2ecc71 !important;
        }

        .text-red {
            color: #e74c3c !important;
        }
        
        /* Financial health score badge */
        .health-badge {
            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 50px;
            font-weight: bold;
            display: inline-block;
            box-shadow: 0 4px 10px rgba(46, 204, 113, 0.3);
        }
        
        /* Form container */
        div[data-testid="stForm"] {
            background: var(--glass-bg) !important;
            border: 1px solid var(--glass-border) !important;
            border-radius: 12px !important;
            padding: 2rem !important;
            box-shadow: 0 8px 32px 0 rgba(0,0,0,0.25) !important;
        }
        
        /* Streamlit overrides for buttons */
        div.stButton > button {
            background: linear-gradient(135deg, var(--pak-green-light) 0%, var(--pak-green) 100%) !important;
            color: white !important;
            border: 1px solid var(--pak-gold) !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
        }
        
        div.stButton > button:hover {
            background: linear-gradient(135deg, var(--pak-green) 0%, var(--pak-green-dark) 100%) !important;
            box-shadow: 0 0 15px rgba(212, 175, 55, 0.3) !important;
            transform: scale(1.02) !important;
        }
        
        /* Custom card styling for dashboard items */
        .dashboard-container {
            background-color: #121212;
            border-radius: 15px;
            padding: 20px;
            border: 1px solid #222;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
