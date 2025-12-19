import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import json
import time
import threading
import winsound
import psutil
import win32gui
import win32process
from datetime import datetime, timedelta
from plyer import notification
from PIL import Image
import os

class StopDoomScrollApp:
    def __init__(self):
        # Configuration
        self.load_config()
        
        # État de l'application
        self.is_work_mode = False
        self.is_break_mode = False
        self.timer_running = False
        self.time_remaining = 0
        self.last_alert_time = 0
        self.paused = False
        self.mini_mode = False
        self.mini_window = None
        self.mini_timer_label = None
        self.mini_status_label = None
        
        # Charger les icônes
        self.load_icons()
        
        # Créer l'interface principale
        self.create_main_window()
        
        # Démarrer le monitoring en arrière-plan
        self.monitoring_thread = threading.Thread(target=self.monitor_browser, daemon=True)
        self.monitoring_thread.start()
        
    def load_config(self):
        """Charge la configuration depuis config.json"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            messagebox.showerror("Erreur", "Fichier config.json introuvable!")
            exit(1)
    
    def load_icons(self):
        """Charge les icônes PNG et les convertit en blanc"""
        icon_size = (20, 20)  # Taille des icônes principales
        small_icon_size = (16, 16)  # Taille des petites icônes (minimize, mini mode)
        
        def convert_to_white(image):
            """Convertit une icône en blanc tout en préservant l'alpha"""
            # Convertir en RGBA si nécessaire
            if image.mode != 'RGBA':
                image = image.convert('RGBA')
            
            # Créer une nouvelle image
            data = image.getdata()
            new_data = []
            
            for item in data:
                # Si le pixel n'est pas complètement transparent
                if item[3] > 0:  # Alpha > 0
                    # Remplacer par blanc en gardant l'alpha
                    new_data.append((255, 255, 255, item[3]))
                else:
                    # Garder transparent
                    new_data.append(item)
            
            new_image = Image.new('RGBA', image.size)
            new_image.putdata(new_data)
            return new_image
        
        try:
            # Play/Start icon
            play_img = Image.open("icons/play-icon.png")
            play_img_white = convert_to_white(play_img)
            self.play_icon = ctk.CTkImage(light_image=play_img_white, dark_image=play_img_white, size=icon_size)
            
            # Pause icon
            pause_img = Image.open("icons/pause-icon.png")
            pause_img_white = convert_to_white(pause_img)
            self.pause_icon = ctk.CTkImage(light_image=pause_img_white, dark_image=pause_img_white, size=icon_size)
            
            # Stop icon
            stop_img = Image.open("icons/square-icon.png")
            stop_img_white = convert_to_white(stop_img)
            self.stop_icon = ctk.CTkImage(light_image=stop_img_white, dark_image=stop_img_white, size=icon_size)
            
            # Settings icon
            settings_img = Image.open("icons/setting-icon.png")
            settings_img_white = convert_to_white(settings_img)
            self.settings_icon = ctk.CTkImage(light_image=settings_img_white, dark_image=settings_img_white, size=icon_size)
            
            # Minimize icon (smaller)
            minimize_img = Image.open("icons/minus-icon.png")
            minimize_img_white = convert_to_white(minimize_img)
            self.minimize_icon = ctk.CTkImage(light_image=minimize_img_white, dark_image=minimize_img_white, size=small_icon_size)
            
            # Mini Mode icon (smaller)
            mini_mode_img = Image.open("icons/aspect-ratio-icon.png")
            mini_mode_img_white = convert_to_white(mini_mode_img)
            self.mini_mode_icon = ctk.CTkImage(light_image=mini_mode_img_white, dark_image=mini_mode_img_white, size=small_icon_size)
            
        except FileNotFoundError as e:
            print(f"Icône introuvable: {e}")
            # Créer des icônes vides si les fichiers n'existent pas
            self.play_icon = None
            self.pause_icon = None
            self.stop_icon = None
            self.settings_icon = None
            self.minimize_icon = None
            self.mini_mode_icon = None
    
    def save_config(self):
        """Sauvegarde la configuration dans config.json"""
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def create_main_window(self):
        """Crée la fenêtre principale (overlay transparent)"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title("StopDoomScroll")
        self.root.geometry("380x590")
        
        # Fond noir profond comme Figma
        self.root.configure(fg_color="#0f0f0f")
        
        # Toujours au premier plan
        self.root.attributes('-topmost', True)
        
        # Créer l'interface
        self.create_widgets()
        
    def create_widgets(self):
        """Crée les widgets de l'interface"""
        # Frame principal avec fond très sombre
        main_frame = ctk.CTkFrame(self.root, fg_color="#0f0f0f", corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Titre avec lettres espacées
        title_label = ctk.CTkLabel(
            main_frame, 
            text="S T O P D O O M S C R O L L",
            font=("Segoe UI", 16, "bold"),
            text_color="#ffffff"
        )
        title_label.pack(pady=(25, 20))
        
        # Timer display très grand
        self.timer_label = ctk.CTkLabel(
            main_frame,
            text="00:00",
            font=("Segoe UI", 72, "bold"),
            text_color="#ffffff"
        )
        self.timer_label.pack(pady=(10, 5))
        
        # Status label subtil
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Ready to start",
            font=("Segoe UI", 12),
            text_color="#888888"
        )
        self.status_label.pack(pady=(5, 25))
        
        # Boutons avec le style Figma
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=5, fill="x", padx=30)
        
        # Bouton Start Session - Vert émeraude comme Figma (avec icône PNG)
        self.start_button = ctk.CTkButton(
            button_frame,
            text="Start Session" if self.play_icon is None else "  Start Session",
            image=self.play_icon,
            compound="left",
            command=self.start_work_session,
            fg_color="#10B981",
            hover_color="#059669",
            font=("Segoe UI", 14, "bold"),
            height=50,
            corner_radius=15,
            border_width=0,
            text_color="#ffffff"
        )
        self.start_button.pack(pady=8, fill="x")
        
        # Bouton Pause - Gris foncé désactivé (avec icône PNG)
        self.pause_button = ctk.CTkButton(
            button_frame,
            text="Pause" if self.pause_icon is None else "  Pause",
            image=self.pause_icon,
            compound="left",
            command=self.toggle_pause,
            state="disabled",
            fg_color="#252525",
            hover_color="#2f2f2f",
            font=("Segoe UI", 13, "bold"),
            height=48,
            corner_radius=15,
            border_width=0,
            text_color="#666666"
        )
        self.pause_button.pack(pady=8, fill="x")
        
        # Bouton Stop - Gris foncé désactivé (avec icône PNG)
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="Stop" if self.stop_icon is None else "  Stop",
            image=self.stop_icon,
            compound="left",
            command=self.stop_session,
            state="disabled",
            fg_color="#252525",
            hover_color="#2f2f2f",
            font=("Segoe UI", 13, "bold"),
            height=48,
            corner_radius=15,
            border_width=0,
            text_color="#666666"
        )
        self.stop_button.pack(pady=8, fill="x")
        
        # Espace
        ctk.CTkLabel(main_frame, text="", height=10, fg_color="transparent").pack()
        
        # Bouton Settings - Gris moyen (avec icône PNG)
        config_button = ctk.CTkButton(
            button_frame,
            text="Settings" if self.settings_icon is None else "  Settings",
            image=self.settings_icon,
            compound="left",
            command=self.open_config_window,
            fg_color="#3a3a3a",
            hover_color="#454545",
            font=("Segoe UI", 13, "bold"),
            height=48,
            corner_radius=15,
            border_width=0,
            text_color="#cccccc"
        )
        config_button.pack(pady=8, fill="x")
        
        # Boutons en bas
        bottom_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        bottom_frame.pack(pady=(15, 10))
        
        # Bouton Mini Mode (avec icône PNG)
        mini_mode_button = ctk.CTkButton(
            bottom_frame,
            text="Mini Mode" if self.mini_mode_icon is None else " Mini Mode",
            image=self.mini_mode_icon,
            compound="left",
            command=self.toggle_mini_mode,
            fg_color="transparent",
            hover_color="#1a1a1a",
            font=("Segoe UI", 11),
            height=30,
            corner_radius=0,
            border_width=0,
            text_color="#888888"
        )
        mini_mode_button.pack(side="left", padx=5)
        
        # Bouton Minimize (avec icône PNG)
        minimize_button = ctk.CTkButton(
            bottom_frame,
            text="Minimize" if self.minimize_icon is None else " Minimize",
            image=self.minimize_icon,
            compound="left",
            command=self.minimize_window,
            fg_color="transparent",
            hover_color="#1a1a1a",
            font=("Segoe UI", 11),
            height=30,
            corner_radius=0,
            border_width=0,
            text_color="#777777"
        )
        minimize_button.pack(side="left", padx=5)
        
    def minimize_window(self):
        """Réduit la fenêtre (iconify)"""
        self.root.iconify()
    
    def toggle_mini_mode(self):
        """Bascule entre mode normal et mini mode (timer only)"""
        if not self.mini_mode:
            # Activer le mini mode
            self.mini_mode = True
            self.root.withdraw()  # Cacher la fenêtre principale
            self.create_mini_window()
        else:
            # Désactiver le mini mode
            self.mini_mode = False
            if self.mini_window:
                self.mini_window.destroy()
                self.mini_window = None
            self.root.deiconify()  # Montrer la fenêtre principale
    
    def create_mini_window(self):
        """Crée une petite fenêtre avec juste le timer en haut à gauche"""
        self.mini_window = ctk.CTkToplevel(self.root)
        self.mini_window.title("Timer")
        
        # Petite fenêtre compacte (un peu plus grande pour le texte de statut)
        mini_width = 200
        mini_height = 100
        
        # Position en haut à gauche de l'écran
        x_position = 20
        y_position = 20
        
        self.mini_window.geometry(f"{mini_width}x{mini_height}+{x_position}+{y_position}")
        self.mini_window.configure(fg_color="#0f0f0f")
        
        # Toujours au premier plan
        self.mini_window.attributes('-topmost', True)
        
        # Retirer les bordures de fenêtre (optionnel, pour un look plus clean)
        # self.mini_window.overrideredirect(True)  # Décommentez si vous voulez pas de barre de titre
        
        # Permettre de revenir en mode normal en cliquant sur la mini fenêtre
        self.mini_window.protocol("WM_DELETE_WINDOW", self.toggle_mini_mode)
        
        # Frame avec fond semi-transparent
        mini_frame = ctk.CTkFrame(self.mini_window, fg_color="#1a1a1a", corner_radius=10)
        mini_frame.pack(fill="both", expand=True, padx=8, pady=8)
        
        # Timer mini (copie du timer principal)
        self.mini_timer_label = ctk.CTkLabel(
            mini_frame,
            text=self.timer_label.cget("text"),
            font=("Segoe UI", 36, "bold"),
            text_color="#ffffff"
        )
        self.mini_timer_label.pack(expand=True)
        
        # Indicateur de statut avec texte
        status_color = "#888888"
        status_text = "Ready to start"
        if self.is_work_mode and not self.paused:
            status_color = "#10B981"
            status_text = "Work"
        elif self.is_break_mode:
            status_color = "#f59e0b"
            status_text = "Break"
        elif self.paused:
            status_color = "#6366f1"
            status_text = "Paused"
        
        self.mini_status_label = ctk.CTkLabel(
            mini_frame,
            text=f"● {status_text}",
            font=("Segoe UI", 10),
            text_color=status_color
        )
        self.mini_status_label.pack(pady=(0, 5))
        
        # Bouton pour revenir en mode normal (petit, discret)
        expand_button = ctk.CTkButton(
            mini_frame,
            text="⤢",
            command=self.toggle_mini_mode,
            fg_color="transparent",
            hover_color="#2a2a2a",
            font=("Segoe UI", 10),
            width=30,
            height=20,
            corner_radius=5,
            text_color="#666666"
        )
        # Vertically align to the middle right (center y)
        expand_button.place(relx=1.0, rely=0.5, x=-5, anchor="e")
    def start_work_session(self):
        """Démarre une session de travail"""
        self.is_work_mode = True
        self.is_break_mode = False
        self.timer_running = True
        self.paused = False
        self.time_remaining = self.config['pomodoro']['work_duration'] * 60
        
        self.start_button.configure(
            state="disabled",
            fg_color="#1a1a1a",
            image=None  # Cacher l'icône quand désactivé
        )
        self.pause_button.configure(
            state="normal",
            fg_color="#3a3a3a",
            hover_color="#454545",
            text_color="#cccccc"
        )
        self.stop_button.configure(
            state="normal",
            fg_color="#3a3a3a",
            hover_color="#454545",
            text_color="#cccccc"
        )
        
        self.status_label.configure(text="Work session active", text_color="#10B981")
        
        # Démarrer le timer
        self.update_timer()
        
    def start_break_session(self):
        """Démarre une session de pause"""
        self.is_work_mode = False
        self.is_break_mode = True
        self.timer_running = True
        self.paused = False
        self.time_remaining = self.config['pomodoro']['break_duration'] * 60
        
        self.status_label.configure(text="Break time - Relax", text_color="#f59e0b")
        
        # Jouer un son pour indiquer la pause
        if self.config['pomodoro']['sound_enabled']:
            self.play_notification_sound()
        
        # Démarrer le timer
        self.update_timer()
    
    def toggle_pause(self):
        """Met en pause/reprend le timer"""
        self.paused = not self.paused
        if self.paused:
            self.pause_button.configure(text="▶   Resume" if self.pause_icon is None else "  Resume")
            self.status_label.configure(text="Paused", text_color="#6366f1")
        else:
            pause_text = "Pause" if self.pause_icon is None else "  Pause"
            self.pause_button.configure(text=pause_text, image=self.pause_icon)
            if self.is_work_mode:
                self.status_label.configure(text="Work session active", text_color="#10B981")
            else:
                self.status_label.configure(text="Break time", text_color="#f59e0b")
    
    def stop_session(self):
        """Arrête la session en cours"""
        self.is_work_mode = False
        self.is_break_mode = False
        self.timer_running = False
        self.paused = False
        self.time_remaining = 0
        
        self.start_button.configure(
            state="normal",
            fg_color="#10B981",
            hover_color="#059669",
            image=self.play_icon  # Remettre l'icône
        )
        pause_text = "Pause" if self.pause_icon is None else "  Pause"
        self.pause_button.configure(
            state="disabled",
            text=pause_text,
            image=self.pause_icon,
            fg_color="#252525",
            text_color="#666666"
        )
        self.stop_button.configure(
            state="disabled",
            fg_color="#252525",
            text_color="#666666"
        )
        
        self.timer_label.configure(text="00:00")
        self.status_label.configure(text="Ready to start", text_color="#888888")
    
    def update_timer(self):
        """Met à jour le timer chaque seconde"""
        if not self.timer_running:
            return
        
        if not self.paused and self.time_remaining > 0:
            self.time_remaining -= 1
            
            # Mettre à jour l'affichage
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            timer_text = f"{minutes:02d}:{seconds:02d}"
            self.timer_label.configure(text=timer_text)
            
            # Mettre à jour aussi le mini timer si en mini mode
            if self.mini_mode and self.mini_window and self.mini_timer_label:
                self.mini_timer_label.configure(text=timer_text)
                # Mettre à jour le texte et la couleur du statut
                if self.is_work_mode and not self.paused:
                    self.mini_status_label.configure(text="● Work", text_color="#10B981")
                elif self.is_break_mode:
                    self.mini_status_label.configure(text="● Break", text_color="#f59e0b")
                elif self.paused:
                    self.mini_status_label.configure(text="● Paused", text_color="#6366f1")
            
        elif self.time_remaining <= 0:
            # Session terminée
            if self.is_work_mode:
                # Passer en mode pause
                self.start_break_session()
            else:
                # Fin de la pause, retour en attente
                self.stop_session()
                messagebox.showinfo("Pomodoro", "Pause terminée! Prêt pour une nouvelle session?")
        
        # Continuer à mettre à jour
        if self.timer_running:
            self.root.after(1000, self.update_timer)
    
    def get_active_window_title(self):
        """Récupère le titre de la fenêtre active (Windows API)"""
        try:
            hwnd = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(hwnd)
            return window_title
        except:
            return ""
    
    def monitor_browser(self):
        """Surveille les onglets du navigateur en arrière-plan"""
        while True:
            try:
                if self.is_work_mode and not self.paused:
                    window_title = self.get_active_window_title()
                    
                    if window_title:
                        window_title_lower = window_title.lower()
                        
                        # Mode debug : afficher le titre de la fenêtre
                        if self.config.get('debug_mode', False):
                            print(f"[DEBUG] Fenêtre active: {window_title}")
                        
                        # Vérifier si c'est un navigateur
                        is_browser = any(browser in window_title_lower for browser in 
                                       ['chrome', 'firefox', 'edge', 'mozilla', 'browser'])
                        
                        if is_browser:
                            if self.config.get('debug_mode', False):
                                print(f"[DEBUG] Navigateur détecté! Titre: {window_title}")
                            
                            # Vérifier si l'URL/titre contient un site blacklisté
                            for blocked_site in self.config['blacklist']:
                                # Nettoyer le site blacklisté (enlever protocole, www, etc.)
                                clean_site = blocked_site.lower()
                                clean_site = clean_site.replace('https://', '').replace('http://', '')
                                clean_site = clean_site.replace('www.', '')
                                clean_site = clean_site.rstrip('/')
                                
                                # Vérifier si le site est dans le titre
                                if clean_site in window_title_lower:
                                    if self.config.get('debug_mode', False):
                                        print(f"[DEBUG] 🚨 SITE BLOQUÉ DÉTECTÉ: {blocked_site}")
                                    
                                    # Vérifier le cooldown pour ne pas spammer les alertes
                                    current_time = time.time()
                                    if current_time - self.last_alert_time > self.config['alert_cooldown']:
                                        self.trigger_alert(blocked_site)
                                        self.last_alert_time = current_time
                                    break
                
                time.sleep(self.config['check_interval'])
                
            except Exception as e:
                if self.config.get('debug_mode', False):
                    print(f"[DEBUG] Erreur: {e}")
                # Continuer même en cas d'erreur
                time.sleep(self.config['check_interval'])
    
    def trigger_alert(self, blocked_site):
        """Déclenche une alerte visuelle, sonore et notification Windows"""
        # 1. Son d'alerte (répété 3 fois pour être plus audible)
        if self.config['pomodoro'].get('sound_enabled', True):
            threading.Thread(target=self.play_alert_sound_repeated, daemon=True).start()
        
        # 2. Notification Windows native
        if self.config['pomodoro'].get('notification_enabled', True):
            try:
                notification.notify(
                    title="StopDoomScroll - Alert",
                    message=f"Distraction detected: {blocked_site}\nGet back to work!",
                    app_name="StopDoomScroll",
                    timeout=10,
                )
            except Exception as e:
                print(f"Erreur notification: {e}")
        
        # 3. Afficher la fenêtre d'alerte (popup)
        if self.config['pomodoro'].get('popup_enabled', True):
            self.root.deiconify()
            self.root.lift()
            self.root.focus_force()
            
            # Créer une fenêtre popup style Figma
            alert_window = ctk.CTkToplevel(self.root)
            alert_window.title("Alert")
            alert_window.geometry("400x300")
            alert_window.attributes('-topmost', True)
            
            # Fond noir profond comme Figma
            alert_window.configure(fg_color="#0f0f0f")
            
            # Centrer la fenêtre
            alert_window.update_idletasks()
            x = (alert_window.winfo_screenwidth() // 2) - (400 // 2)
            y = (alert_window.winfo_screenheight() // 2) - (300 // 2)
            alert_window.geometry(f"+{x}+{y}")
            
            # Frame principal sans bordure visible
            content_frame = ctk.CTkFrame(alert_window, fg_color="#0f0f0f", corner_radius=0)
            content_frame.pack(fill="both", expand=True, padx=30, pady=30)
            
            # Icône d'alerte
            icon_label = ctk.CTkLabel(
                content_frame,
                text="⚠",
                font=("Segoe UI", 56),
                text_color="#ef4444"
            )
            icon_label.pack(pady=(10, 15))
            
            # Titre
            warning_label = ctk.CTkLabel(
                content_frame,
                text="DISTRACTION DETECTED",
                font=("Segoe UI", 16, "bold"),
                text_color="#ffffff"
            )
            warning_label.pack(pady=(0, 10))
            
            # Message
            message_label = ctk.CTkLabel(
                content_frame,
                text=f"You are on: {blocked_site}\n\nGet back to your work session",
                font=("Segoe UI", 12),
                text_color="#888888"
            )
            message_label.pack(pady=15)
            
            # Bouton de fermeture - Style Figma (vert émeraude)
            close_button = ctk.CTkButton(
                content_frame,
                text="✓   Got it, back to work",
                command=alert_window.destroy,
                fg_color="#10B981",
                hover_color="#059669",
                font=("Segoe UI", 14, "bold"),
                height=50,
                corner_radius=15,
                text_color="#ffffff"
            )
            close_button.pack(pady=(10, 0), fill="x")
            
            # Auto-fermeture après 8 secondes
            alert_window.after(8000, alert_window.destroy)
    
    def play_alert_sound(self):
        """Joue un son d'alerte (un seul beep)"""
        try:
            # Jouer un beep système (Windows) - Son plus grave et long
            winsound.Beep(800, 400)  # Fréquence 800Hz, durée 400ms
        except:
            pass
    
    def play_alert_sound_repeated(self):
        """Joue un son d'alerte répété (plus audible)"""
        try:
            for i in range(3):  # Répéter 3 fois
                winsound.Beep(800, 300)   # Son grave
                time.sleep(0.15)
                winsound.Beep(1200, 200)  # Son aigu
                time.sleep(0.3)
        except:
            pass
    
    def play_notification_sound(self):
        """Joue un son de notification"""
        try:
            winsound.Beep(800, 200)
            time.sleep(0.1)
            winsound.Beep(800, 200)
        except:
            pass
    
    def open_config_window(self):
        """Ouvre la fenêtre de configuration"""
        config_window = ctk.CTkToplevel(self.root)
        config_window.title("Settings")
        config_window.geometry("500x600")
        config_window.configure(fg_color="#0a0a0a")
        
        # Frame scrollable
        scroll_frame = ctk.CTkScrollableFrame(config_window, fg_color="#1a1a1a")
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Section Pomodoro
        pomodoro_label = ctk.CTkLabel(
            scroll_frame,
            text="⏱  Pomodoro Timer",
            font=("Segoe UI", 15, "bold"),
            text_color="#ffffff"
        )
        pomodoro_label.pack(pady=(15, 10), anchor="w")
        
        # Durée de travail
        work_frame = ctk.CTkFrame(scroll_frame)
        work_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(work_frame, text="Work duration (minutes):", text_color="#cccccc").pack(side="left", padx=5)
        work_entry = ctk.CTkEntry(work_frame, width=60)
        work_entry.insert(0, str(self.config['pomodoro']['work_duration']))
        work_entry.pack(side="right", padx=5)
        
        # Durée de pause
        break_frame = ctk.CTkFrame(scroll_frame)
        break_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(break_frame, text="Break duration (minutes):", text_color="#cccccc").pack(side="left", padx=5)
        break_entry = ctk.CTkEntry(break_frame, width=60)
        break_entry.insert(0, str(self.config['pomodoro']['break_duration']))
        break_entry.pack(side="right", padx=5)
        
        # Options d'alerte
        alert_options_label = ctk.CTkLabel(
            scroll_frame,
            text="Alert Options",
            font=("Segoe UI", 13, "bold"),
            text_color="#ffffff"
        )
        alert_options_label.pack(pady=(15, 8), anchor="w")
        
        # Son activé
        sound_var = tk.BooleanVar(value=self.config['pomodoro'].get('sound_enabled', True))
        sound_check = ctk.CTkCheckBox(
            scroll_frame,
            text="Enable alert sounds",
            variable=sound_var,
            text_color="#cccccc"
        )
        sound_check.pack(pady=3, anchor="w", padx=10)
        
        # Notifications Windows activées
        notification_var = tk.BooleanVar(value=self.config['pomodoro'].get('notification_enabled', True))
        notification_check = ctk.CTkCheckBox(
            scroll_frame,
            text="Enable Windows notifications",
            variable=notification_var,
            text_color="#cccccc"
        )
        notification_check.pack(pady=3, anchor="w", padx=10)
        
        # Popup activé
        popup_var = tk.BooleanVar(value=self.config['pomodoro'].get('popup_enabled', True))
        popup_check = ctk.CTkCheckBox(
            scroll_frame,
            text="Enable popup windows",
            variable=popup_var,
            text_color="#cccccc"
        )
        popup_check.pack(pady=3, anchor="w", padx=10)
        
        ctk.CTkLabel(
            scroll_frame,
            text="(At least one option must be enabled)",
            font=("Segoe UI", 9),
            text_color="#666666"
        ).pack(anchor="w", padx=10, pady=(3, 0))
        
        # Section Blacklist
        blacklist_label = ctk.CTkLabel(
            scroll_frame,
            text="⊘  Blocked Sites",
            font=("Segoe UI", 15, "bold"),
            text_color="#ffffff"
        )
        blacklist_label.pack(pady=(15, 10), anchor="w")
        
        # Zone de texte pour la blacklist
        blacklist_text = ctk.CTkTextbox(scroll_frame, height=200)
        blacklist_text.pack(fill="x", pady=5)
        blacklist_text.insert("1.0", "\n".join(self.config['blacklist']))
        
        ctk.CTkLabel(
            scroll_frame,
            text="One site per line (e.g. youtube.com)",
            font=("Segoe UI", 10),
            text_color="#666666"
        ).pack(anchor="w")
        
        # Section Avancé
        advanced_label = ctk.CTkLabel(
            scroll_frame,
            text="⚙  Advanced Settings",
            font=("Segoe UI", 15, "bold"),
            text_color="#ffffff"
        )
        advanced_label.pack(pady=(15, 10), anchor="w")
        
        # Intervalle de vérification
        check_frame = ctk.CTkFrame(scroll_frame)
        check_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(check_frame, text="Check interval (seconds):", text_color="#cccccc").pack(side="left", padx=5)
        check_entry = ctk.CTkEntry(check_frame, width=60)
        check_entry.insert(0, str(self.config['check_interval']))
        check_entry.pack(side="right", padx=5)
        
        # Cooldown des alertes
        cooldown_frame = ctk.CTkFrame(scroll_frame)
        cooldown_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(cooldown_frame, text="Alert cooldown (seconds):", text_color="#cccccc").pack(side="left", padx=5)
        cooldown_entry = ctk.CTkEntry(cooldown_frame, width=60)
        cooldown_entry.insert(0, str(self.config['alert_cooldown']))
        cooldown_entry.pack(side="right", padx=5)
        
        # Boutons de sauvegarde
        def save_and_close():
            try:
                # Sauvegarder les modifications
                self.config['pomodoro']['work_duration'] = int(work_entry.get())
                self.config['pomodoro']['break_duration'] = int(break_entry.get())
                self.config['pomodoro']['sound_enabled'] = sound_var.get()
                self.config['pomodoro']['notification_enabled'] = notification_var.get()
                self.config['pomodoro']['popup_enabled'] = popup_var.get()
                self.config['blacklist'] = [line.strip() for line in blacklist_text.get("1.0", "end").split("\n") if line.strip()]
                self.config['check_interval'] = int(check_entry.get())
                self.config['alert_cooldown'] = int(cooldown_entry.get())
                
                # Vérifier qu'au moins une option d'alerte est activée
                if not (sound_var.get() or notification_var.get() or popup_var.get()):
                    messagebox.showwarning("Attention", "Au moins une option d'alerte doit être activée!\nLe son a été réactivé automatiquement.")
                    self.config['pomodoro']['sound_enabled'] = True
                
                self.save_config()
                messagebox.showinfo("Succès", "Configuration sauvegardée!")
                config_window.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "Veuillez entrer des valeurs numériques valides!")
        
        button_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=15, padx=10)
        
        save_button = ctk.CTkButton(
            button_frame,
            text="✓  Save Changes",
            command=save_and_close,
            fg_color="#10B981",
            hover_color="#0d9488",
            font=("Segoe UI", 13, "bold"),
            height=42,
            corner_radius=12
        )
        save_button.pack(side="left", padx=5, expand=True, fill="x")
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="✕  Cancel",
            command=config_window.destroy,
            fg_color="transparent",
            hover_color="#3a3a3a",
            border_color="#555555",
            border_width=2,
            font=("Segoe UI", 13, "bold"),
            height=42,
            corner_radius=12,
            text_color="#999999"
        )
        cancel_button.pack(side="right", padx=5, expand=True, fill="x")
    
    def run(self):
        """Lance l'application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = StopDoomScrollApp()
    app.run()

