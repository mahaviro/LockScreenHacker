import sys
import random
import math
import os
import datetime
import psutil  # Pastikan menginstal ini via 'pip install psutil' untuk data hardware real
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QFont, QColor, QPen, QPainter, QPolygonF

class HackerLockScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        self.time_counter = 0.0
        self.globe_angle = 0.0  # Sudut rotasi bola dunia
        self.rocket_angle = 0.0 # Sudut orbit roket
        self.is_alarm_active = False  # Status mode siaga merah
        
        # Load password permanen dari direktori file skrip ini berada[cite: 1]
        self.current_password = self.load_password()
        self.pwd_state = "NORMAL"
        self.temp_new_pwd = ""
        
        # Konfigurasi Hujan Biner Vertikal & Horizontal[cite: 1]
        self.v_col_width = 25
        self.h_row_height = 35
        self.v_drops = []
        self.h_drops = []
        
        # Data untuk Panel Hacking Saldo (Sisi Kiri - Nominal Realistis)
        self.hack_balances = []
        self.update_hack_balances()
        
        # Data untuk Streaming Alamat IP (Sisi Kanan)
        self.ip_streams = []
        for _ in range(7):
            self.ip_streams.append({
                'ip': f"{random.randint(10,192)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}",
                'status': random.choice(["[ROOT ACCESS]", "[PACKET SNIFFING]", "[FIREWALL BYPASSED]", "[PORT 443 OPEN]", "[EXPLOITING]"])
            })

        # Data untuk Notifikasi Serangan Global (Pojok Kanan Bawah)
        self.global_attacks = []
        self.update_global_attacks()
        
        # Variabel Hardware Real dari Laptop
        self.cpu_usage = 0.0
        self.ram_used = 0.0
        self.ram_total = 16.0
        self.ram_percent = 0.0
        self.gpu_usage = 65.0  # Simulasi GPU
        self.gpu_temp = 72      # Simulasi GPU Temp
        
        # Pre-komputasi Peta Benua Garis[cite: 1]
        self.map_points = self.generate_world_map()
        
        # Titik satelit statis yang menempel di bumi[cite: 1]
        self.active_nodes = []
        for _ in range(14):
            self.active_nodes.append({
                'lat': math.radians(random.uniform(-60, 70)),
                'lon': math.radians(random.uniform(-180, 180)),
                'blink_speed': random.uniform(0.1, 0.3),
                'phase': random.uniform(0, 2 * math.pi)
            })

        # Grid Peta Dunia Biner di Background[cite: 1]
        self.binary_map_grid = []

        self.initUI()

        # Timer Animasi Utama (30 FPS)[cite: 1]
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update_animation)
        self.anim_timer.start(30) 

        # Timer untuk mengacak data (tiap 500ms)
        self.glitch_timer = QTimer(self)
        self.glitch_timer.timeout.connect(self.update_glitch_data)
        self.glitch_timer.start(500)

    def get_password_file_path(self):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(os.path.abspath(sys.executable))
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, "pwd.txt")

    def load_password(self):
        pwd_path = self.get_password_file_path()
        if os.path.exists(pwd_path):
            try:
                with open(pwd_path, "r") as f:
                    pwd = f.read().strip()
                    if pwd:
                        return pwd
            except:
                pass
        return "123"

    def save_password(self, new_pwd):
        pwd_path = self.get_password_file_path()
        try:
            with open(pwd_path, "w") as f:
                f.write(new_pwd)
        except:
            pass

    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: black;")
        self.setCursor(Qt.BlankCursor) # Sembunyikan mouse[cite: 1]

        # MEMBUAT PANEL TERMINAL DENGAN WIDGET RESMI (ANTI-FREEZE)[cite: 1]
        self.terminal_widget = QWidget(self)
        self.terminal_widget.setStyleSheet("background-color: rgba(0, 0, 0, 235); border: 1px solid #00FF66;")
        
        self.layout_box = QVBoxLayout(self.terminal_widget)
        self.layout_box.setAlignment(Qt.AlignCenter)

        # 1. Judul[cite: 1]
        self.title_label = QLabel("=== DEVICE IS LOCKED ===")
        self.title_label.setStyleSheet("color: #00FF66; border: none; font-weight: bold;")
        self.title_label.setFont(QFont("Courier New", 15))
        self.title_label.setAlignment(Qt.AlignCenter)

        # 2. Status[cite: 1]
        self.status_label = QLabel("DEVICE IS LOCKED, PLEASE ENTER THE ACCESS CODE!")
        self.status_label.setStyleSheet("color: #00FF66; border: none;")
        self.status_label.setFont(QFont("Courier New", 11))
        self.status_label.setAlignment(Qt.AlignCenter)

        # 3. Baris Input Password[cite: 1]
        input_layout = QHBoxLayout()
        input_layout.setAlignment(Qt.AlignCenter)
        
        self.prompt_label = QLabel("ENTER ACCESS CODE:")
        self.prompt_label.setStyleSheet("color: yellow; border: none;")
        self.prompt_label.setFont(QFont("Courier New", 13))
        
        self.password_input = QLineEdit()
        self.password_input.setStyleSheet("color: yellow; background: transparent; border: none;")
        self.password_input.setFont(QFont("Courier New", 13))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMaxLength(15)
        self.password_input.setFixedWidth(200)
        
        self.password_input.returnPressed.connect(self.check_password)

        input_layout.addWidget(self.prompt_label)
        input_layout.addWidget(self.password_input)

        self.layout_box.addWidget(self.title_label)
        self.layout_box.addSpacing(10)
        self.layout_box.addWidget(self.status_label)
        self.layout_box.addSpacing(15)
        self.layout_box.addLayout(input_layout)

        self.password_input.setFocus()
        self.showFullScreen()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        
        num_cols = self.width() // self.v_col_width
        self.v_drops = [{'y': random.randint(-self.height(), 0), 'speed': random.randint(5, 12)} for _ in range(num_cols)]
        
        num_rows = self.height() // self.h_row_height
        self.h_drops = [{'x': random.randint(-self.width(), 0), 'speed': random.randint(3, 8)} for _ in range(num_rows)]

        self.init_binary_map_grid()
        
        if hasattr(self, 'terminal_widget'):
            term_w, term_h = 650, 150
            x_pos = (self.width() - term_w) // 2
            y_pos = (self.height() // 2) + 210
            self.terminal_widget.setGeometry(x_pos, y_pos, term_w, term_h)

    def init_binary_map_grid(self):
        self.binary_map_grid = []
        step_x, step_y = 16, 20
        max_cols = self.width() // step_x
        max_rows = self.height() // step_y
        
        for r in range(max_rows):
            row_chars = []
            for c in range(max_cols):
                lat = (r / max_rows) * 180 - 90
                lon = (c / max_cols) * 360 - 180
                
                is_land = False
                if 15 <= lat <= 75 and -130 <= lon <= -60: is_land = True
                elif -55 <= lat <= 15 and -80 <= lon <= -35: is_land = True
                elif 35 <= lat <= 70 and -10 <= lon <= 45: is_land = True
                elif -35 <= lat <= 35 and -20 <= lon <= 55: is_land = True
                elif 10 <= lat <= 75 and 45 <= lon <= 140: is_land = True
                elif -45 <= lat <= -10 and 110 <= lon <= 155: is_land = True
                
                if is_land:
                    row_chars.append(random.choice(['0', '1']))
                else:
                    row_chars.append(' ' if random.random() > 0.15 else random.choice(['0', '1']))
            self.binary_map_grid.append(row_chars)

    def update_hack_balances(self):
        currencies = [
            ("USD", "$", 1500, 95000),
            ("EUR", "€", 1200, 82000),
            ("IDR", "Rp ", 15000000, 850000000),
            ("BTC", "BTC ", 0.5, 8.5),
            ("ETH", "ETH ", 2.5, 45.0),
            ("JPY", "¥", 200000, 9500000),
            ("GBP", "£", 1000, 65000),
            ("SGD", "$", 2000, 110000),
        ]
        actions = ["[TRANSFER]", "[BREACHED]", "[EXTRACTING]", "[EXFILTRATING]", "[UNLOCKED]", "[BYPASSING]"]
        
        self.hack_balances = []
        for curr, sym, min_v, max_v in random.sample(currencies, len(currencies)):
            if curr in ["BTC", "ETH"]:
                val = random.uniform(min_v, max_v)
                self.hack_balances.append(f"{curr}: {val:.4f} {random.choice(actions)}")
            elif curr == "IDR":
                val = random.randint(int(min_v), int(max_v))
                formatted_val = f"{val:,}".replace(",", ".")
                self.hack_balances.append(f"{curr}: {sym}{formatted_val} {random.choice(actions)}")
            else:
                val = random.randint(int(min_v), int(max_v))
                formatted_val = f"{val:,}"
                self.hack_balances.append(f"{curr}: {sym}{formatted_val} {random.choice(actions)}")

    def update_global_attacks(self):
        cities = ["TOKYO", "NEW YORK", "LONDON", "SINGAPORE", "BERLIN", "MOSCOW", "SYDNEY", "SEOUL", "BEIJING", "PARIS"]
        threats = ["DDoS Layer 7", "Port 443 Breach", "Ransomware Payload", "SQL Injection", "Brute Force Auth", "Zero-Day Exploit"]
        
        self.global_attacks = []
        for _ in range(4):
            c = random.choice(cities)
            t = random.choice(threats)
            self.global_attacks.append(f">> {c}: {t}")

    def update_glitch_data(self):
        if self.binary_map_grid:
            for _ in range(30):
                r = random.randint(0, len(self.binary_map_grid) - 1)
                c = random.randint(0, len(self.binary_map_grid[0]) - 1)
                if self.binary_map_grid[r][c] != ' ':
                    self.binary_map_grid[r][c] = random.choice(['0', '1'])
        
        self.update_hack_balances()
        self.update_global_attacks()

        # Ambil Data Real dari Laptop menggunakan psutil
        try:
            self.cpu_usage = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory()
            self.ram_used = round(mem.used / (1024**3), 1)
            self.ram_total = round(mem.total / (1024**3), 1)
            self.ram_percent = mem.percent
        except:
            self.cpu_usage = 45.0
            self.ram_used = 8.0
            self.ram_total = 16.0
            self.ram_percent = 50.0

        # Simulasi fluktuasi GPU
        self.gpu_usage = round(random.uniform(40.0, 95.0), 1)
        self.gpu_temp = random.randint(65, 84)

        for ip_obj in self.ip_streams:
            ip_obj['ip'] = f"{random.randint(10,192)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"

    def generate_world_map(self):
        points = []
        for lat in range(-90, 90, 6):
            for lon in range(-180, 180, 6):
                is_land = False
                if 15 <= lat <= 75 and -130 <= lon <= -60: is_land = True
                elif -55 <= lat <= 15 and -80 <= lon <= -35: is_land = True
                elif 35 <= lat <= 70 and -10 <= lon <= 45: is_land = True
                elif -35 <= lat <= 35 and -20 <= lon <= 55: is_land = True
                elif 10 <= lat <= 75 and 45 <= lon <= 140: is_land = True
                elif -45 <= lat <= -10 and 110 <= lon <= 155: is_land = True
                
                if is_land and random.random() > 0.25:
                    points.append({
                        'lon': math.radians(lon),
                        'cos_lat': math.cos(math.radians(lat)),
                        'sin_lat': math.sin(math.radians(lat))
                    })
        return points

    def update_animation(self):
        for drop in self.v_drops:
            drop['y'] += drop['speed']
            if drop['y'] > self.height():
                drop['y'] = random.randint(-300, 0)
                drop['speed'] = random.randint(5, 12)

        for drop in self.h_drops:
            drop['x'] += drop['speed']
            if drop['x'] > self.width():
                drop['x'] = random.randint(-400, 0)

        self.globe_angle -= 0.015
        self.rocket_angle += 0.035  
        self.time_counter += 1.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if self.is_alarm_active:
            is_flash_on = int(self.time_counter * 3) % 2 == 0
            if is_flash_on:
                map_color = QColor(150, 0, 0, 180)        
                globe_color = QColor(255, 50, 50, 255)    
            else:
                map_color = QColor(60, 0, 0, 100)
                globe_color = QColor(150, 0, 0, 150)
        else:
            map_color = QColor(0, 100, 30, 120)
            globe_color = QColor(0, 255, 100, 180)

        painter.fillRect(self.rect(), Qt.black)

        font = QFont("Courier New", 11, QFont.Bold)
        painter.setFont(font)

        # 1. RENDER PETA DUNIA BINER DI BACKGROUND
        painter.setPen(map_color)
        step_x, step_y = 16, 20
        for r, row in enumerate(self.binary_map_grid):
            y = r * step_y
            for c, char in enumerate(row):
                if char != ' ':
                    painter.drawText(c * step_x, y, char)

        # 2. RENDER HUJAN BINER VERTIKAL
        v_trail = 8
        for i, drop in enumerate(self.v_drops):
            x = i * self.v_col_width
            base_y = drop['y']
            for j in range(v_trail):
                char_y = base_y - (j * 18)
                if 0 <= char_y <= self.height():
                    alpha = int(180 * (1 - (j / v_trail)))
                    if self.is_alarm_active:
                        painter.setPen(QColor(255, 100, 100, alpha))
                    else:
                        painter.setPen(QColor(180, 255, 180, 255) if j == 0 else QColor(0, 200, 60, alpha))
                    painter.drawText(x, char_y, random.choice(['0', '1']))

        # 3. RENDER HUJAN BINER HORIZONTAL
        h_trail = 8
        for i, drop in enumerate(self.h_drops):
            y = i * self.h_row_height
            base_x = drop['x']
            for j in range(h_trail):
                char_x = base_x - (j * 16)
                if 0 <= char_x <= self.width():
                    alpha = int(140 * (1 - (j / h_trail)))
                    if self.is_alarm_active:
                        painter.setPen(QColor(255, 80, 80, alpha))
                    else:
                        painter.setPen(QColor(150, 255, 150, 200) if j == 0 else QColor(0, 150, 40, alpha))
                    painter.drawText(char_x, y, random.choice(['0', '1']))

        center_x = self.width() // 2
        center_y = self.height() // 2 - 50
        radius = 220

        # --- 4. SISI KIRI ATAS: PANEL PROSES HACKING SALDO (WARNA HIJAU SANGAR) ---
        painter.setFont(QFont("Courier New", 9, QFont.Bold))
        painter.setPen(QColor(0, 255, 120, 230) if not self.is_alarm_active else QColor(255, 50, 50, 220))
        painter.drawText(30, 85, "=== [EXPLOITING FINANCIAL ACCOUNTS] ===")
        
        start_y = 115
        for idx, bal_text in enumerate(self.hack_balances):
            painter.drawText(30, start_y + (idx * 22), bal_text)

        # --- 5. POJOK KIRI BAWAH: MONITORING CPU & GPU REAL LAPTOP ---
        bl_y = self.height() - 170
        painter.setPen(QColor(0, 255, 150, 230) if not self.is_alarm_active else QColor(255, 50, 50, 220))
        painter.drawText(30, bl_y, "=== [HARDWARE TELEMETRY] ===")
        
        cpu_bar = "|" * int(self.cpu_usage / 5)
        gpu_bar = "|" * int(self.gpu_usage / 5)
        ram_bar = "|" * int(self.ram_percent / 5)
        
        painter.drawText(30, bl_y + 25, f"CPU: [{cpu_bar:<20}] {self.cpu_usage}%")
        painter.drawText(30, bl_y + 48, f"GPU: [{gpu_bar:<20}] {self.gpu_usage}% ({self.gpu_temp}°C)")
        painter.drawText(30, bl_y + 71, f"RAM: [{ram_bar:<20}] {self.ram_used}GB / {self.ram_total}GB ({self.ram_percent}%)")

        # --- 6. SISI KANAN ATAS: STREAMING ALAMAT IP TARGET (WARNA HIJAU SANGAR) ---
        right_margin_x = self.width() - 330
        painter.setPen(QColor(0, 255, 100, 220) if not self.is_alarm_active else QColor(255, 50, 50, 220))
        painter.drawText(right_margin_x, 85, "=== [ACTIVE TARGET IP STREAMS] ===")
        
        for idx, ip_obj in enumerate(self.ip_streams):
            ip_row_text = f"{ip_obj['ip']} -> {ip_obj['status']}"
            painter.drawText(right_margin_x, 115 + (idx * 22), ip_row_text)

        # --- 7. POJOK KANAN BAWAH: NOTIFIKASI SERANGAN GLOBAL ---
        br_y = self.height() - 150
        painter.setPen(QColor(0, 255, 150, 220) if not self.is_alarm_active else QColor(255, 50, 50, 220))
        painter.drawText(right_margin_x, br_y, "=== [GLOBAL ATTACK FEED] ===")
        for idx, atk_text in enumerate(self.global_attacks):
            painter.drawText(right_margin_x, br_y + 25 + (idx * 22), atk_text)

        # --- 8. BAGIAN TENGAH ATAS: TANGGAL & JAM STYLE MANDARIN (UKURAN JAM DIPERBESAR) ---
        now = datetime.datetime.now()
        mandarin_date = f"{now.strftime('%Y')}年{now.strftime('%m')}月{now.strftime('%d')}日"
        mandarin_time = now.strftime('%H:%M:%S')
        
        # Render Tanggal (Di atas)
        painter.setFont(QFont("Courier New", 11, QFont.Bold))
        painter.setPen(globe_color)
        painter.drawText(center_x - 150, 42, 300, 20, Qt.AlignCenter, mandarin_date)
        
        # Render Jam (Di bawah tanggal dengan ukuran lebih besar)
        painter.setFont(QFont("Courier New", 21, QFont.Bold))
        painter.drawText(center_x - 150, 68, 300, 30, Qt.AlignCenter, mandarin_time)
        # ----------------------------------------------------------------------------------

        # 9. BOLA DUNIA & GRID GARIS LINTANG/BUJUR
        painter.setPen(QPen(globe_color, 2.5))
        painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)

        painter.setPen(QPen(globe_color, 1, Qt.DashLine))
        painter.drawLine(center_x - radius, center_y, center_x + radius, center_y)

        meridian_offset = math.sin(self.globe_angle) * radius
        painter.drawArc(center_x + int(meridian_offset) - int(radius / 3), center_y - radius, int(radius / 1.5), radius * 2, 0, 360 * 16)

        painter.setPen(QPen(globe_color, 1, Qt.DotLine))
        painter.drawEllipse(center_x - radius - 30, center_y - radius - 30, (radius + 30) * 2, (radius + 30) * 2)

        # 10. PETA BENUA BERPUTAR DI DALAM BOLA DUNIA
        painter.setPen(globe_color)
        for pt in self.map_points:
            current_lon = pt['lon'] + self.globe_angle
            current_lon = (current_lon + math.pi) % (2 * math.pi) - math.pi
            
            if -math.pi/2 <= current_lon <= math.pi/2:
                x = radius * pt['cos_lat'] * math.sin(current_lon)
                y = -radius * pt['sin_lat']
                painter.drawPoint(center_x + int(x), center_y + int(y))

        # --- 11. RENDER "GOD EYE" ALA FREEMASON DI DALAM BOLA DUNIA ---
        eye_cx = center_x
        eye_cy = center_y
        
        glance_x = math.sin(self.time_counter * 0.04) * 15
        glance_y = math.cos(self.time_counter * 0.03) * 7

        tri_size = 95
        p1 = QPointF(eye_cx, eye_cy - tri_size * 0.85 + glance_y)
        p2 = QPointF(eye_cx - tri_size + glance_x, eye_cy + tri_size * 0.6 + glance_y)
        p3 = QPointF(eye_cx + tri_size + glance_x, eye_cy + tri_size * 0.6 + glance_y)
        
        painter.setPen(QPen(globe_color, 1.8))
        painter.setBrush(Qt.NoBrush)
        painter.drawPolygon(QPolygonF([p1, p2, p3]))

        for angle_deg in range(0, 360, 45):
            rad = math.radians(angle_deg + self.time_counter * 0.4)
            rx1 = eye_cx + math.cos(rad) * 45
            ry1 = eye_cy + math.sin(rad) * 45
            rx2 = eye_cx + math.cos(rad) * (tri_size + 15)
            ry2 = eye_cy + math.sin(rad) * (tri_size + 15)
            painter.setPen(QPen(globe_color, 1, Qt.DashLine))
            painter.drawLine(int(rx1), int(ry1), int(rx2), int(ry2))

        eye_rx = 52
        eye_ry = 28
        e_cx = eye_cx + glance_x
        e_cy = eye_cy + 8 + glance_y

        painter.setPen(QPen(globe_color, 2))
        painter.drawEllipse(int(e_cx - eye_rx), int(e_cy - eye_ry), int(eye_rx * 2), int(eye_ry * 2))

        step_ex, step_ey = 10, 10
        font_eye = QFont("Courier New", 9, QFont.Bold)
        painter.setFont(font_eye)

        pupil_x = e_cx + glance_x * 0.5
        pupil_y = e_cy + glance_y * 0.5

        for ey_pos in range(int(e_cy - eye_ry + 2), int(e_cy + eye_ry), step_ey):
            for ex_pos in range(int(e_cx - eye_rx + 6), int(e_cx + eye_rx), step_ex):
                dx_n = (ex_pos - e_cx) / eye_rx
                dy_n = (ey_pos - e_cy) / eye_ry
                if dx_n**2 + dy_n**2 <= 1.0:
                    dist_pupil = math.hypot(ex_pos - pupil_x, ey_pos - pupil_y)
                    if dist_pupil <= 14:
                        painter.setPen(globe_color)
                        char = random.choice(['1', '0'])
                    else:
                        painter.setPen(globe_color)
                        char = random.choice(['0', '1'])
                    painter.drawText(ex_pos, ey_pos, char)

        painter.setFont(font)
        # ----------------------------------------------------------------------------------

        # 12. TITIK SATELIT / NODES DI BUMI
        for node in self.active_nodes:
            current_lon = node['lon'] + self.globe_angle
            current_lon = (current_lon + math.pi) % (2 * math.pi) - math.pi
            
            if -math.pi/2 <= current_lon <= math.pi/2:
                x = radius * math.cos(node['lat']) * math.sin(current_lon)
                y = -radius * math.sin(node['lat'])
                
                alpha = int(150 * (1 + math.sin(node['phase'] + self.time_counter * node['blink_speed'])))
                node_color = QColor(255, 0, 0, alpha) if self.is_alarm_active else QColor(255, 255, 0, alpha)
                
                painter.setBrush(node_color)
                painter.setPen(Qt.NoPen)
                painter.drawEllipse(int(center_x + x) - 4, int(center_y + y) - 4, 8, 8)
                
                painter.setBrush(Qt.NoBrush)
                painter.setPen(QPen(node_color, 1))
                painter.drawEllipse(int(center_x + x) - 8, int(center_y + y) - 8, 16, 16)

        # 13. EFEK ROKET / SATELIT YANG MENGELILINGI BOLA DUNIA
        orbit_rx = radius + 35
        orbit_ry = (radius + 35) // 2.5  
        
        rocket_x = center_x + math.cos(self.rocket_angle) * orbit_rx
        rocket_y = center_y + math.sin(self.rocket_angle) * orbit_ry
        
        for i in range(5):
            trail_angle = self.rocket_angle - (i * 0.08)
            tx = center_x + math.cos(trail_angle) * orbit_rx
            ty = center_y + math.sin(trail_angle) * orbit_ry
            trail_alpha = int(200 * (1 - (i / 5.0)))
            
            painter.setBrush(QColor(0, 255, 255, trail_alpha)) 
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(tx) - int(3 - i/2), int(ty) - int(3 - i/2), int(6 - i), int(6 - i))

        painter.setBrush(QColor(255, 255, 255)) 
        painter.setPen(QPen(QColor(0, 255, 255), 1.5))
        painter.drawEllipse(int(rocket_x) - 5, int(rocket_y) - 5, 10, 10)

    def check_password(self):
        pwd = self.password_input.text()
        
        if self.pwd_state == "NORMAL":
            if pwd.lower() == "chgpass":
                self.pwd_state = "OLD_PWD"
                self.status_label.setText(">> PASSWORD CHANGE PROCESS INITIATED <<")
                self.status_label.setStyleSheet("color: yellow; border: none; font-weight: bold;")
                self.prompt_label.setText("ENTER OLD PASSWORD:")
                self.password_input.clear()
            elif pwd == self.current_password:
                self.is_alarm_active = False
                self.title_label.setStyleSheet("color: #00FF66; border: none; font-weight: bold;")
                self.status_label.setText(">> ACCESS GRANTED, WELCOME BOSS!! <<")
                self.status_label.setStyleSheet("color: #00FF66; border: none; font-weight: bold;")
                self.password_input.clear()
                QTimer.singleShot(1500, sys.exit)
            else:
                self.is_alarm_active = True
                self.title_label.setStyleSheet("color: red; border: none; font-weight: bold;")
                self.status_label.setText(">> ACCESS DENIED! SECURITY ALERT! <<")
                self.status_label.setStyleSheet("color: red; border: none; font-weight: bold;")
                self.terminal_widget.setStyleSheet("background-color: rgba(50, 0, 0, 240); border: 1px solid red;")
                
                self.password_input.clear()
                QTimer.singleShot(1500, self.reset_status)

        elif self.pwd_state == "OLD_PWD":
            if pwd == self.current_password:
                self.pwd_state = "NEW_PWD_1"
                self.status_label.setText(">> OLD PASSWORD CORRECT. ENTER NEW PASSWORD <<")
                self.status_label.setStyleSheet("color: #00FF66; border: none;")
                self.prompt_label.setText("ENTER NEW PASSWORD:")
                self.password_input.clear()
            else:
                self.status_label.setText(">> INCORRECT OLD PASSWORD! RETURNING <<")
                self.status_label.setStyleSheet("color: red; border: none; font-weight: bold;")
                self.password_input.clear()
                QTimer.singleShot(1500, self.reset_to_normal)

        elif self.pwd_state == "NEW_PWD_1":
            if pwd.lower() == "chgpass":
                self.status_label.setText(">> THE WORD 'chgpass' CANNOT BE USED AS A PASSWORD! RETURNING <<")
                self.status_label.setStyleSheet("color: red; border: none; font-weight: bold;")
                self.password_input.clear()
                QTimer.singleShot(1500, self.reset_to_normal)
            elif pwd == "":
                self.status_label.setText(">> PASSWORD CANNOT BE EMPTY! RETURNING <<")
                self.status_label.setStyleSheet("color: red; border: none; font-weight: bold;")
                self.password_input.clear()
                QTimer.singleShot(1500, self.reset_to_normal)
            else:
                self.temp_new_pwd = pwd
                self.pwd_state = "NEW_PWD_2"
                self.status_label.setText(">> RE-ENTER NEW PASSWORD (SECOND TIME) <<")
                self.prompt_label.setText("CONFIRM NEW PASSWORD:")
                self.password_input.clear()

        elif self.pwd_state == "NEW_PWD_2":
            if pwd == self.temp_new_pwd:
                self.pwd_state = "CONFIRM_BEFORE"
                self.status_label.setText(">> CONFIRMATION: ENTER OLD PASSWORD TO CONFIRM CHANGE <<")
                self.status_label.setStyleSheet("color: yellow; border: none; font-weight: bold;")
                self.prompt_label.setText("ENTER OLD PASSWORD:")
                self.password_input.clear()
            else:
                self.status_label.setText(">> NEW PASSWORDS DO NOT MATCH! RETURNING <<")
                self.status_label.setStyleSheet("color: red; border: none; font-weight: bold;")
                self.password_input.clear()
                QTimer.singleShot(1500, self.reset_to_normal)

        elif self.pwd_state == "CONFIRM_BEFORE":
            if pwd == self.current_password:
                self.current_password = self.temp_new_pwd
                self.save_password(self.current_password) 
                self.pwd_state = "CONFIRM_AFTER"
                self.status_label.setText(">> SUCCESS! PASSWORD HAS BEEN CHANGED. (Press Enter) <<")
                self.status_label.setStyleSheet("color: #00FF66; border: none; font-weight: bold;")
                self.prompt_label.setText("COMPLETE (ENTER):")
                self.password_input.clear()
            else:
                self.status_label.setText(">> WRONG OLD PASSWORD! CHANGE CANCELLED <<")
                self.status_label.setStyleSheet("color: red; border: none; font-weight: bold;")
                self.password_input.clear()
                QTimer.singleShot(1500, self.reset_to_normal)

        elif self.pwd_state == "CONFIRM_AFTER":
            self.reset_to_normal()

    def reset_to_normal(self):
        self.pwd_state = "NORMAL"
        self.status_label.setText("DEVICE IS LOCKED, PLEASE ENTER THE ACCESS CODE!")
        self.status_label.setStyleSheet("color: #00FF66; border: none;")
        self.prompt_label.setText("ENTER ACCESS CODE:")
        self.terminal_widget.setStyleSheet("background-color: rgba(0, 0, 0, 235); border: 1px solid #00FF66;")
        self.password_input.clear()

    def reset_status(self):
        if self.pwd_state == "NORMAL":
            self.is_alarm_active = False
            self.title_label.setStyleSheet("color: #00FF66; border: none; font-weight: bold;")
            self.status_label.setText("DEVICE IS LOCKED, PLEASE ENTER THE ACCESS CODE!")
            self.status_label.setStyleSheet("color: #00FF66; border: none;")
            self.terminal_widget.setStyleSheet("background-color: rgba(0, 0, 0, 235); border: 1px solid #00FF66;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    lockscreen = HackerLockScreen()
    sys.exit(app.exec_())