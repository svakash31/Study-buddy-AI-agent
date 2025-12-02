"""
Custom CSS for AI Study Buddy
Premium modern design with dark theme, glassmorphism, and smooth animations
"""

def get_custom_css():
    return """
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
    
    /* Root variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        --dark-bg: #0f0f23;
        --card-bg: rgba(255, 255, 255, 0.05);
        --card-border: rgba(255, 255, 255, 0.1);
        --text-primary: #ffffff;
        --text-secondary: #b8b8d1;
        --accent-purple: #9d4edd;
        --accent-blue: #4cc9f0;
        --accent-pink: #f72585;
    }
    
    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0f0f23 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Streamlit header - Transparent and sleek */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    
    /* Toolbar styling */
    [data-testid="stToolbar"] {
        background: transparent;
    }
    
    /* Main block container - Increase padding to ensure content isn't hidden */
    .block-container {
        padding-top: 4rem;
    }
    
    /* Headers */
    h1, h2, h3 {
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    h1 {
        font-size: 3rem !important;
        margin-bottom: 0.5rem !important;
        animation: fadeInDown 0.8s ease-out;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(15, 15, 35, 0.95) 0%, rgba(26, 26, 62, 0.95) 100%);
        border-right: 1px solid var(--card-border);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: var(--text-primary);
    }
    
    /* Cards with glassmorphism */
    .element-container, .stMarkdown, [data-testid="stExpander"] {
        backdrop-filter: blur(10px);
    }
    
    /* Custom metric cards */
    [data-testid="stMetric"] {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: var(--accent-purple);
        box-shadow: 0 8px 32px rgba(157, 78, 221, 0.3);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700;
        background: var(--success-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: var(--card-bg);
        border: 2px dashed var(--card-border);
        border-radius: 16px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--accent-blue);
        background: rgba(76, 201, 240, 0.05);
    }
    
    /* Chat messages */
    [data-testid="stChatMessage"] {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        animation: slideInRight 0.4s ease-out;
    }
    
    [data-testid="stChatMessage"][data-testid-value="user"] {
        border-left: 4px solid var(--accent-purple);
    }
    
    [data-testid="stChatMessage"][data-testid-value="assistant"] {
        border-left: 4px solid var(--accent-blue);
    }
    
    /* Chat input */
    [data-testid="stChatInput"] {
        border: 2px solid var(--card-border);
        border-radius: 24px;
        background: var(--card-bg);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: var(--accent-purple);
        box-shadow: 0 0 20px rgba(157, 78, 221, 0.3);
    }
    
    /* Tabs */
    [data-testid="stTabs"] {
        background: transparent;
    }
    
    button[data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: var(--text-secondary);
        font-weight: 600;
        font-size: 1.1rem;
        padding: 1rem 2rem;
        transition: all 0.3s ease;
    }
    
    button[data-baseweb="tab"]:hover {
        color: var(--accent-purple);
    }
    
    button[data-baseweb="tab"][aria-selected="true"] {
        color: var(--text-primary);
        background: var(--primary-gradient);
        border-radius: 12px 12px 0 0;
    }
    
    /* Expanders */
    [data-testid="stExpander"] {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: var(--success-gradient);
        border-radius: 10px;
    }
    
    /* Text inputs */
    input, textarea, select {
        background: var(--card-bg) !important;
        border: 1px solid var(--card-border) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        padding: 0.75rem !important;
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: var(--accent-purple) !important;
        box-shadow: 0 0 15px rgba(157, 78, 221, 0.2) !important;
    }
    
    /* Info/Success/Warning boxes */
    .stAlert {
        border-radius: 12px;
        border: 1px solid var(--card-border);
        backdrop-filter: blur(10px);
    }
    
    /* Code blocks */
    code {
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid var(--card-border);
        border-radius: 6px;
        padding: 0.2rem 0.4rem;
        font-family: 'JetBrains Mono', monospace;
        color: var(--accent-blue);
    }
    
    pre {
        background: rgba(0, 0, 0, 0.4) !important;
        border: 1px solid var(--card-border);
        border-radius: 12px;
        padding: 1rem;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-gradient);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-gradient);
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.7;
        }
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: var(--accent-purple) !important;
    }
    
    /* Divider */
    hr {
        border-color: var(--card-border);
        margin: 2rem 0;
    }
    
    /* Links */
    a {
        color: var(--accent-blue);
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    a:hover {
        color: var(--accent-purple);
        text-decoration: underline;
    }
    
    /* Custom badge class */
    .badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .badge-success {
        background: var(--success-gradient);
        color: white;
    }
    
    .badge-primary {
        background: var(--primary-gradient);
        color: white;
    }
    
    .badge-secondary {
        background: var(--secondary-gradient);
        color: white;
    }
    
    /* Floating effect for cards */
    .float-card {
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    /* Shimmer effect for loading */
    .shimmer {
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        background-size: 200% 100%;
        animation: shimmer 1.5s infinite;
    }
    
    @keyframes shimmer {
        0% {
            background-position: -200% 0;
        }
        100% {
            background-position: 200% 0;
        }
    }
    </style>
    """
