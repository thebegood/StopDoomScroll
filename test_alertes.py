"""
Script de test pour vérifier que les alertes fonctionnent correctement
Exécutez ce script pour tester les sons et notifications AVANT de lancer l'app
"""

import sys

print("=" * 50)
print("  TEST DES ALERTES - StopDoomScroll")
print("=" * 50)
print()

# Test 1 : winsound
print("1️⃣ Test des sons (winsound)...")
try:
    import winsound
    print("   ✅ Module winsound importé")
    
    print("   🔊 Lecture d'un son de test...")
    winsound.Beep(1000, 500)
    print("   ✅ Son joué avec succès!")
    print()
except Exception as e:
    print(f"   ❌ ERREUR: {e}")
    print()

# Test 2 : plyer notifications
print("2️⃣ Test des notifications Windows (plyer)...")
try:
    from plyer import notification
    print("   ✅ Module plyer importé")
    
    print("   🔔 Envoi d'une notification de test...")
    notification.notify(
        title="🧪 Test StopDoomScroll",
        message="Si vous voyez ce message, les notifications fonctionnent! ✅",
        app_name="StopDoomScroll Test",
        timeout=5
    )
    print("   ✅ Notification envoyée!")
    print("   👀 Regardez en bas à droite de votre écran!")
    print()
except Exception as e:
    print(f"   ❌ ERREUR: {e}")
    print()

# Test 3 : win32gui
print("3️⃣ Test de l'API Windows (win32gui)...")
try:
    import win32gui
    print("   ✅ Module win32gui importé")
    
    hwnd = win32gui.GetForegroundWindow()
    window_title = win32gui.GetWindowText(hwnd)
    print(f"   ✅ Fenêtre active détectée: {window_title}")
    print()
except Exception as e:
    print(f"   ❌ ERREUR: {e}")
    print()

# Test 4 : customtkinter
print("4️⃣ Test de l'interface graphique (customtkinter)...")
try:
    import customtkinter as ctk
    print("   ✅ Module customtkinter importé")
    print()
except Exception as e:
    print(f"   ❌ ERREUR: {e}")
    print()

# Test 5 : psutil
print("5️⃣ Test du monitoring système (psutil)...")
try:
    import psutil
    print("   ✅ Module psutil importé")
    cpu_percent = psutil.cpu_percent(interval=0.1)
    print(f"   ✅ CPU: {cpu_percent}%")
    print()
except Exception as e:
    print(f"   ❌ ERREUR: {e}")
    print()

# Résumé
print("=" * 50)
print("  RÉSUMÉ")
print("=" * 50)

errors = []

try:
    import winsound
except:
    errors.append("winsound (sons)")

try:
    from plyer import notification
except:
    errors.append("plyer (notifications)")

try:
    import win32gui
except:
    errors.append("win32gui (API Windows)")

try:
    import customtkinter
except:
    errors.append("customtkinter (interface)")

try:
    import psutil
except:
    errors.append("psutil (monitoring)")

if not errors:
    print("✅ TOUS LES TESTS SONT PASSÉS!")
    print("🚀 Vous pouvez lancer l'application avec: python main.py")
else:
    print("❌ Certains modules manquent:")
    for error in errors:
        print(f"   - {error}")
    print()
    print("💡 Solution: Exécutez 'pip install -r requirements.txt'")

print()
print("=" * 50)
input("Appuyez sur Entrée pour quitter...")

