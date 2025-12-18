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
    
    def save_config(self):
        """Sauvegarde la configuration dans config.json"""
        with open('config.json', 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def create_main_window(self):
        """Crée la fenêtre principale (overlay transparent)"""
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("StopDoomScroll")
        self.root.geometry("300x400")
        
        # Toujours au premier plan
        self.root.attributes('-topmost', True)
        
        # Créer l'interface
        self.create_widgets()
        
    def create_widgets(self):
        """Crée les widgets de l'interface"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Titre
        title_label = ctk.CTkLabel(
            main_frame, 
            text="🎯 StopDoomScroll",
            font=("Arial", 20, "bold")
        )
        title_label.pack(pady=10)
        
        # Timer display
        self.timer_label = ctk.CTkLabel(
            main_frame,
            text="00:00",
            font=("Arial", 36, "bold")
        )
        self.timer_label.pack(pady=10)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="⏸️ En attente",
            font=("Arial", 14)
        )
        self.status_label.pack(pady=5)
        
        # Boutons
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(pady=10, fill="x")
        
        self.start_button = ctk.CTkButton(
            button_frame,
            text="▶️ Démarrer",
            command=self.start_work_session,
            fg_color="green",
            hover_color="darkgreen"
        )
        self.start_button.pack(pady=5, fill="x")
        
        self.pause_button = ctk.CTkButton(
            button_frame,
            text="⏸️ Pause",
            command=self.toggle_pause,
            state="disabled"
        )
        self.pause_button.pack(pady=5, fill="x")
        
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="⏹️ Arrêter",
            command=self.stop_session,
            state="disabled",
            fg_color="red",
            hover_color="darkred"
        )
        self.stop_button.pack(pady=5, fill="x")
        
        # Bouton de configuration
        config_button = ctk.CTkButton(
            main_frame,
            text="⚙️ Configuration",
            command=self.open_config_window
        )
        config_button.pack(pady=10, fill="x")
        
        # Bouton pour réduire/afficher
        minimize_button = ctk.CTkButton(
            main_frame,
            text="➖ Réduire",
            command=self.minimize_window,
            fg_color="gray",
            hover_color="darkgray"
        )
        minimize_button.pack(pady=5, fill="x")
        
    def minimize_window(self):
        """Réduit la fenêtre (iconify)"""
        self.root.iconify()
    
    def start_work_session(self):
        """Démarre une session de travail"""
        self.is_work_mode = True
        self.is_break_mode = False
        self.timer_running = True
        self.paused = False
        self.time_remaining = self.config['pomodoro']['work_duration'] * 60
        
        self.start_button.configure(state="disabled")
        self.pause_button.configure(state="normal")
        self.stop_button.configure(state="normal")
        
        self.status_label.configure(text="🔥 Session de travail")
        
        # Démarrer le timer
        self.update_timer()
        
    def start_break_session(self):
        """Démarre une session de pause"""
        self.is_work_mode = False
        self.is_break_mode = True
        self.timer_running = True
        self.paused = False
        self.time_remaining = self.config['pomodoro']['break_duration'] * 60
        
        self.status_label.configure(text="☕ Pause - Détendez-vous!")
        
        # Jouer un son pour indiquer la pause
        if self.config['pomodoro']['sound_enabled']:
            self.play_notification_sound()
        
        # Démarrer le timer
        self.update_timer()
    
    def toggle_pause(self):
        """Met en pause/reprend le timer"""
        self.paused = not self.paused
        if self.paused:
            self.pause_button.configure(text="▶️ Reprendre")
            self.status_label.configure(text="⏸️ En pause")
        else:
            self.pause_button.configure(text="⏸️ Pause")
            if self.is_work_mode:
                self.status_label.configure(text="🔥 Session de travail")
            else:
                self.status_label.configure(text="☕ Pause")
    
    def stop_session(self):
        """Arrête la session en cours"""
        self.is_work_mode = False
        self.is_break_mode = False
        self.timer_running = False
        self.paused = False
        self.time_remaining = 0
        
        self.start_button.configure(state="normal")
        self.pause_button.configure(state="disabled", text="⏸️ Pause")
        self.stop_button.configure(state="disabled")
        
        self.timer_label.configure(text="00:00")
        self.status_label.configure(text="⏸️ En attente")
    
    def update_timer(self):
        """Met à jour le timer chaque seconde"""
        if not self.timer_running:
            return
        
        if not self.paused and self.time_remaining > 0:
            self.time_remaining -= 1
            
            # Mettre à jour l'affichage
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
            
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
                    title="⚠️ StopDoomScroll - ALERTE!",
                    message=f"Vous êtes sur {blocked_site}\nRetournez au travail! 💪",
                    app_name="StopDoomScroll",
                    timeout=10,  # Durée d'affichage en secondes
                )
            except Exception as e:
                print(f"Erreur notification: {e}")
        
        # 3. Afficher la fenêtre d'alerte (popup)
        if self.config['pomodoro'].get('popup_enabled', True):
            self.root.deiconify()  # Restaurer la fenêtre si minimisée
            self.root.lift()  # Mettre au premier plan
            self.root.focus_force()  # Forcer le focus
            
            # Créer une fenêtre popup
            alert_window = ctk.CTkToplevel(self.root)
            alert_window.title("⚠️ Alerte DoomScroll!")
            alert_window.geometry("400x200")
            alert_window.attributes('-topmost', True)
            
            # Centrer la fenêtre
            alert_window.update_idletasks()
            x = (alert_window.winfo_screenwidth() // 2) - (400 // 2)
            y = (alert_window.winfo_screenheight() // 2) - (200 // 2)
            alert_window.geometry(f"+{x}+{y}")
            
            # Contenu
            warning_label = ctk.CTkLabel(
                alert_window,
                text="⚠️ ATTENTION!",
                font=("Arial", 24, "bold"),
                text_color="red"
            )
            warning_label.pack(pady=20)
            
            message_label = ctk.CTkLabel(
                alert_window,
                text=f"Vous êtes sur:\n{blocked_site}\n\nRetournez au travail! 💪",
                font=("Arial", 14)
            )
            message_label.pack(pady=10)
            
            close_button = ctk.CTkButton(
                alert_window,
                text="Je reprends le travail!",
                command=alert_window.destroy,
                fg_color="green",
                hover_color="darkgreen"
            )
            close_button.pack(pady=10)
            
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
        config_window.title("⚙️ Configuration")
        config_window.geometry("500x600")
        
        # Frame scrollable
        scroll_frame = ctk.CTkScrollableFrame(config_window)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Section Pomodoro
        pomodoro_label = ctk.CTkLabel(
            scroll_frame,
            text="⏱️ Timer Pomodoro",
            font=("Arial", 16, "bold")
        )
        pomodoro_label.pack(pady=10, anchor="w")
        
        # Durée de travail
        work_frame = ctk.CTkFrame(scroll_frame)
        work_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(work_frame, text="Durée de travail (minutes):").pack(side="left", padx=5)
        work_entry = ctk.CTkEntry(work_frame, width=60)
        work_entry.insert(0, str(self.config['pomodoro']['work_duration']))
        work_entry.pack(side="right", padx=5)
        
        # Durée de pause
        break_frame = ctk.CTkFrame(scroll_frame)
        break_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(break_frame, text="Durée de pause (minutes):").pack(side="left", padx=5)
        break_entry = ctk.CTkEntry(break_frame, width=60)
        break_entry.insert(0, str(self.config['pomodoro']['break_duration']))
        break_entry.pack(side="right", padx=5)
        
        # Options d'alerte
        alert_options_label = ctk.CTkLabel(
            scroll_frame,
            text="Options d'alerte:",
            font=("Arial", 12, "bold")
        )
        alert_options_label.pack(pady=(10, 5), anchor="w")
        
        # Son activé
        sound_var = tk.BooleanVar(value=self.config['pomodoro'].get('sound_enabled', True))
        sound_check = ctk.CTkCheckBox(
            scroll_frame,
            text="🔊 Activer les sons d'alerte",
            variable=sound_var
        )
        sound_check.pack(pady=2, anchor="w", padx=10)
        
        # Notifications Windows activées
        notification_var = tk.BooleanVar(value=self.config['pomodoro'].get('notification_enabled', True))
        notification_check = ctk.CTkCheckBox(
            scroll_frame,
            text="🔔 Activer les notifications Windows",
            variable=notification_var
        )
        notification_check.pack(pady=2, anchor="w", padx=10)
        
        # Popup activé
        popup_var = tk.BooleanVar(value=self.config['pomodoro'].get('popup_enabled', True))
        popup_check = ctk.CTkCheckBox(
            scroll_frame,
            text="🪟 Activer les fenêtres popup",
            variable=popup_var
        )
        popup_check.pack(pady=2, anchor="w", padx=10)
        
        ctk.CTkLabel(
            scroll_frame,
            text="(Au moins une option doit être activée)",
            font=("Arial", 9),
            text_color="gray"
        ).pack(anchor="w", padx=10)
        
        # Section Blacklist
        blacklist_label = ctk.CTkLabel(
            scroll_frame,
            text="🚫 Sites bloqués",
            font=("Arial", 16, "bold")
        )
        blacklist_label.pack(pady=10, anchor="w")
        
        # Zone de texte pour la blacklist
        blacklist_text = ctk.CTkTextbox(scroll_frame, height=200)
        blacklist_text.pack(fill="x", pady=5)
        blacklist_text.insert("1.0", "\n".join(self.config['blacklist']))
        
        ctk.CTkLabel(
            scroll_frame,
            text="Un site par ligne (ex: youtube.com)",
            font=("Arial", 10),
            text_color="gray"
        ).pack(anchor="w")
        
        # Section Avancé
        advanced_label = ctk.CTkLabel(
            scroll_frame,
            text="🔧 Paramètres avancés",
            font=("Arial", 16, "bold")
        )
        advanced_label.pack(pady=10, anchor="w")
        
        # Intervalle de vérification
        check_frame = ctk.CTkFrame(scroll_frame)
        check_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(check_frame, text="Intervalle de vérification (secondes):").pack(side="left", padx=5)
        check_entry = ctk.CTkEntry(check_frame, width=60)
        check_entry.insert(0, str(self.config['check_interval']))
        check_entry.pack(side="right", padx=5)
        
        # Cooldown des alertes
        cooldown_frame = ctk.CTkFrame(scroll_frame)
        cooldown_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(cooldown_frame, text="Cooldown alertes (secondes):").pack(side="left", padx=5)
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
        
        button_frame = ctk.CTkFrame(scroll_frame)
        button_frame.pack(fill="x", pady=10)
        
        save_button = ctk.CTkButton(
            button_frame,
            text="💾 Sauvegarder",
            command=save_and_close,
            fg_color="green",
            hover_color="darkgreen"
        )
        save_button.pack(side="left", padx=5, expand=True, fill="x")
        
        cancel_button = ctk.CTkButton(
            button_frame,
            text="❌ Annuler",
            command=config_window.destroy,
            fg_color="red",
            hover_color="darkred"
        )
        cancel_button.pack(side="right", padx=5, expand=True, fill="x")
    
    def run(self):
        """Lance l'application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = StopDoomScrollApp()
    app.run()

