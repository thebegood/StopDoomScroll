"""
Script de debug pour voir ce que l'application détecte
Utilisez ce script pour comprendre pourquoi un site n'est pas détecté
"""

import time
import win32gui

print("=" * 70)
print("  DEBUG - Détection des onglets de navigateur")
print("=" * 70)
print()
print("📋 Instructions:")
print("1. Lancez ce script")
print("2. Ouvrez votre navigateur (Chrome/Firefox/Edge)")
print("3. Allez sur le site que vous voulez tester (Instagram, YouTube, etc.)")
print("4. Cliquez sur l'onglet du navigateur pour le rendre actif")
print("5. Observez ce qui s'affiche ci-dessous")
print()
print("⚠️  Le script va afficher le titre de votre fenêtre active toutes les 2 secondes")
print("⚠️  Appuyez sur Ctrl+C pour arrêter")
print()
print("=" * 70)
print()

previous_title = ""
detection_count = 0

try:
    while True:
        try:
            # Récupérer la fenêtre active
            hwnd = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(hwnd)
            
            # N'afficher que si le titre change
            if window_title != previous_title:
                print(f"🪟 Fenêtre active: {window_title}")
                print()
                
                # Vérifier si c'est un navigateur
                window_title_lower = window_title.lower()
                is_browser = any(browser in window_title_lower for browser in 
                               ['chrome', 'firefox', 'edge', 'mozilla', 'browser'])
                
                if is_browser:
                    print(f"   ✅ NAVIGATEUR DÉTECTÉ!")
                    print()
                    
                    # Tester avec la blacklist par défaut
                    blacklist = [
                        "youtube.com", "facebook.com", "instagram.com",
                        "twitter.com", "reddit.com", "tiktok.com",
                        "9gag.com", "netflix.com", "twitch.tv"
                    ]
                    
                    detected_sites = []
                    for site in blacklist:
                        clean_site = site.lower().replace('https://', '').replace('http://', '')
                        clean_site = clean_site.replace('www.', '').rstrip('/')
                        
                        if clean_site in window_title_lower:
                            detected_sites.append(site)
                    
                    if detected_sites:
                        print(f"   🚨 SITES BLOQUÉS DÉTECTÉS: {', '.join(detected_sites)}")
                        print(f"   ➡️  L'alerte DEVRAIT se déclencher!")
                        detection_count += 1
                    else:
                        print(f"   ℹ️  Aucun site blacklisté détecté dans ce titre")
                        print(f"   💡 Pour bloquer ce site, ajoutez un mot-clé du titre dans la blacklist")
                    print()
                else:
                    print(f"   ℹ️  Pas un navigateur (pas de détection)")
                    print()
                
                print("-" * 70)
                print()
                
                previous_title = window_title
            
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Erreur: {e}")
            time.sleep(2)

except KeyboardInterrupt:
    print()
    print("=" * 70)
    print(f"✅ Script arrêté. Sites bloqués détectés: {detection_count} fois")
    print("=" * 70)



