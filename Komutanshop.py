from flask import Flask, request, jsonify, render_template_string
import base64
import json

app = Flask(__name__)

# Başlangıç veri tabanı simülasyonu (Örnek veri)
users_db = [
    {
        "id": "1",
        "title": "HappiVPN {Free}",
        "description": "Telegram: @HappiVPN | Satyn almak ucin: @HappiVPN_bot",
        "sub_url": "https://marzban.example.com/sub/admin/123456",
        "encrypted_code": "happ://ZXlKMGFYUnSaVzVmZDJsemRHOXlhVzUwSWpvaVFXNXRpV1p1SWl3aVpYSndhVzVsWkNJNkZDSXNJbU52Ym1ScFptbHNiMk5oZEdsdmJpSTZJQ0lzSW1saVpYSnVZVzFsSWpvaUlpd2laVzVqY25sd2RHRmtYMk52YkdSbGNpSTZJQ0lzSW1sdVpYUnpaV05wYlhCcVpYTWlPaUlpZlgwPQ==",
        "usage": "0.0 / 50.0 GB",
        "status": "0%"
    }
]

def encrypt_happ_data(title, description, sub_url):
    """Formdan gelen 3 veriyi birleştirip 'happ://' protokolüyle Base64 olarak şifreler."""
    config = {
        "title": title,
        "description": description,
        "sub_url": sub_url
    }
    json_str = json.dumps(config, ensure_ascii=False)
    encrypted_bytes = base64.b64encode(json_str.encode('utf-8'))
    return f"happ://{encrypted_bytes.decode('utf-8')}"

# HTML Arayüzü doğrudan Python kodunun içine gömüldü
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Subscription Panel</title>
    <style>
        :root {
            --bg-color: #0b111e;
            --card-bg: #131c2e;
            --input-bg: #1b263b;
            --accent-blue: #2563eb;
            --accent-glow: #3b82f6;
            --text-main: #ffffff;
            --text-muted: #64748b;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { background-color: var(--bg-color); color: var(--text-main); padding: 20px; display: flex; justify-content: center; }
        
        .container { width: 100%; max-width: 480px; }

        /* Sol Üst Başlık ve Duyuru Alanı */
        .header { margin-bottom: 25px; display: flex; flex-direction: column; text-align: left; }
        .logo-area { display: flex; align-items: center; gap: 10px; margin-bottom: 12px; }
        .logo-icon { width: 32px; height: 32px; background: linear-gradient(135deg, #3b82f6, #1d4ed8); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-weight: bold; }
        .logo-text { font-size: 22px; font-weight: bold; letter-spacing: 0.5px; }
        
        /* İstediğiniz Özel Duyuru Metinleri */
        .owner-notice { font-size: 13px; color: var(--text-muted); margin-bottom: 2px; font-weight: 500; padding-left: 2px; }
        .owner-tg { font-size: 13px; color: var(--accent-glow); font-weight: bold; margin-bottom: 10px; padding-left: 2px; }

        /* İstatistik Kartı */
        .stat-card { background-color: var(--card-bg); padding: 20px; border-radius: 16px; margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between; border-bottom: 3px solid var(--accent-blue); position: relative; width: 100%; }
        .stat-info { display: flex; align-items: center; gap: 15px; }
        .stat-icon-wrapper { width: 45px; height: 45px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 20px; }
        .icon-blue { background-color: rgba(37, 99, 235, 0.2); color: #3b82f6; }
        .stat-label { font-size: 15px; color: #cbd5e1; }
        .stat-value { font-size: 22px; font-weight: bold; }

        /* Kullanıcı Yönetim Alanı */
        .section-header { display: flex; justify-content: space-between; align-items: center; margin: 25px 0 15px 0; width: 100%; }
        .section-title { font-size: 19px; font-weight: 600; }
        .btn-create { background-color: var(--accent-blue); color: white; border: none; padding: 10px 18px; border-radius: 20px; font-size: 14px; font-weight: 600; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3); }
        .btn-create:hover { background-color: var(--accent-glow); transform: translateY(-1px); }

        /* Kullanıcı Listesi Kart Şablonu */
        .user-card { background-color: var(--card-bg); border-radius: 16px; padding: 15px; margin-bottom: 12px; width: 100%; }
        .user-meta { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
        .user-name { display: flex; align-items: center; gap: 8px; font-weight: 600; }
        .badge { background-color: #1e293b; color: #3b82f6; padding: 2px 8px; border-radius: 12px; font-size: 11px; }
        .status-badge { color: #10b981; background: rgba(16, 185, 129, 0.1); padding: 3px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; }
        .user-stats-text { font-size: 12px; color: var(--text-muted); margin-bottom: 12px; text-align: left; }
        
        .action-buttons { display: flex; gap: 8px; }
        .btn-action { flex: 1; padding: 10px; border-radius: 10px; border: none; font-size: 13px; font-weight: 600; cursor: pointer; transition: 0.2s; text-align: center; }
        .btn-kodal { background-color: var(--accent-blue); color: white; }
        .btn-kodal:hover { background-color: var(--accent-glow); }
        .btn-secondary { background-color: #1e293b; color: #94a3b8; }

        /* Pop-up Modal */
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); display: none; align-items: center; justify-content: center; padding: 20px; z-index: 100; }
        .modal-content { background-color: var(--card-bg); width: 100%; max-width: 400px; border-radius: 20px; padding: 25px; border: 1px solid #1e293b; box-shadow: 0 10px 25px rgba(0,0,0,0.5); text-align: left; }
        .modal-content h3 { margin-bottom: 15px; font-size: 18px; color: white; }
        .modal-content input, .modal-content textarea { width: 100%; background-color: var(--input-bg); border: 1px solid #1e293b; border-radius: 10px; padding: 12px; color: white; margin-bottom: 12px; font-size: 14px; outline: none; }
        .modal-content input:focus, .modal-content textarea:focus { border-color: var(--accent-glow); }
        .modal-content textarea { height: 80px; resize: none; }
        .modal-actions { display: flex; gap: 10px; justify-content: flex-end; margin-top: 5px; }
        .btn-submit { background-color: var(--accent-blue); color: white; padding: 10px 20px; border-radius: 10px; border: none; cursor: pointer; font-weight: 600; }
        .btn-cancel { background-color: #334155; color: white; padding: 10px 20px; border-radius: 10px; border: none; cursor: pointer; }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <div class="logo-area">
            <div class="logo-icon">S</div>
            <div class="logo-text">Subscription Panel</div>
        </div>
        <div class="owner-notice">Ähli näsazlyklar uçin ownere yüz tutun</div>
        <div class="owner-tg">TG: @Komutan_Creator</div>
    </div>

    <div class="stat-card">
        <div class="stat-info">
            <div class="stat-icon-wrapper icon-blue">👥</div>
            <div class="stat-label">Aktiw ulanyjylar</div>
        </div>
        <div class="stat-value" id="active-count-display">{{ active_count }} / {{ active_count }}</div>
    </div>

    <div class="section-header">
        <div class="section-title">Ulanyjy kodlary</div>
        <button class="btn-create" onclick="openModal()">+ Ulanyjy döret</button>
    </div>

    <div id="users-list">
        {% for user in users %}
        <div class="user-card">
            <div class="user-meta">
                <div class="user-name">
                    <span>Y</span>
                    <span class="badge">admin</span>
                </div>
                <div class="status-badge">{{ user.status }}</div>
            </div>
            <div class="user-stats-text">{{ user.usage }} • Çäksiz</div>
            
            <div class="action-buttons">
                <button class="btn-action btn-kodal" onclick="copyCode('{{ user.encrypted_code }}')">Kod al</button>
                <button class="btn-action btn-secondary">File</button>
                <button class="btn-action btn-secondary">URL</button>
            </div>
        </div>
        {% endfor %}
    </div>
</div>

<div class="modal-overlay" id="addModal">
    <div class="modal-content">
        <h3>Taze Ulanyjy Döret</h3>
        <input type="text" id="title" placeholder="1. Yazı Yeri (Örn: HappiVPN {Free})">
        <textarea id="description" placeholder="2. Yazı Yeri (77GB altındaki duyuru yazısı)"></textarea>
        <input type="url" id="sub_url" placeholder="3. Yazı Yeri (Marzban Subscription URL)">
        
        <div class="modal-actions">
            <button class="btn-cancel" onclick="closeModal()">Ýatyr</button>
            <button class="btn-submit" onclick="submitUser()">Tamam</button>
        </div>
    </div>
</div>

<script>
    function openModal() {
        document.getElementById('addModal').style.display = 'flex';
    }

    function closeModal() {
        document.getElementById('addModal').style.display = 'none';
        document.getElementById('title').value = '';
        document.getElementById('description').value = '';
        document.getElementById('sub_url').value = '';
    }

    function submitUser() {
        const title = document.getElementById('title').value;
        const description = document.getElementById('description').value;
        const sub_url = document.getElementById('sub_url').value;

        if(!title || !sub_url) {
            alert('Gerekli alanları doldurun!');
            return;
        }

        fetch('/add_user', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title, description, sub_url })
        })
        .then(res => res.json())
        .then(data => {
            if(data.status === 'success') {
                closeModal();
                location.reload();
            } else {
                alert(data.message);
            }
        });
    }

    function copyCode(encryptedCode) {
        navigator.clipboard.writeText(encryptedCode).then(() => {
            alert("Happ şifrelenmiş kod panoya kopyalandı!");
        }).catch(err => {
            alert("Kopyalama başarısız oldu.");
        });
    }
</script>

</body>
</html>
"""

@app.route('/')
def index():
    active_count = len(users_db)
    return render_template_string(HTML_TEMPLATE, users=users_db, active_count=active_count)

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    title = data.get('title')
    description = data.get('description')
    sub_url = data.get('sub_url')
    
    if not title or not sub_url:
        return jsonify({"status": "error", "message": "Gerekli alanları doldurun!"}), 400
        
    encrypted_code = encrypt_happ_data(title, description, sub_url)
    
    new_user = {
        "id": str(len(users_db) + 1),
        "title": title,
        "description": description,
        "sub_url": sub_url,
        "encrypted_code": encrypted_code,
        "usage": "0.0 / 50.0 GB",
        "status": "0%"
    }
    users_db.append(new_user)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
