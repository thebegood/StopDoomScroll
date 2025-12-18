# 🔔 Guide des Alertes - StopDoomScroll

## 🎯 Système d'alerte multi-niveaux

L'application dispose de **3 types d'alertes** quand vous êtes sur un site blacklisté :

### 1. 🔊 Sons d'alerte
- **Son répété** : 3 séquences de bips (grave + aigu)
- **Très audible** même si vous portez un casque
- Se joue automatiquement en arrière-plan

### 2. 🔔 Notifications Windows
- **Notification native Windows 10/11**
- Apparaît en bas à droite de votre écran
- Reste affichée pendant 10 secondes
- Message : "Vous êtes sur [site] - Retournez au travail! 💪"

### 3. 🪟 Fenêtre popup
- **Popup au centre de l'écran**
- Toujours au premier plan
- Affiche le site bloqué
- Bouton "Je reprends le travail!"
- Se ferme automatiquement après 8 secondes

## ⚙️ Configuration des alertes

Vous pouvez activer/désactiver chaque type d'alerte :

1. Cliquez sur **"⚙️ Configuration"**
2. Allez dans la section **"Options d'alerte"**
3. Cochez/décochez :
   - 🔊 **Sons d'alerte**
   - 🔔 **Notifications Windows**
   - 🪟 **Fenêtres popup**
4. Cliquez sur **"💾 Sauvegarder"**

> ⚠️ **Important** : Au moins une option doit rester activée !

## 💡 Quelle configuration choisir ?

### Configuration recommandée (par défaut)
✅ Sons + ✅ Notifications + ✅ Popup
- **Maximum d'impact**
- Impossible d'ignorer l'alerte
- Parfait pour les distractions sévères

### Configuration discrète
✅ Notifications + ❌ Sons + ❌ Popup
- **Moins intrusif**
- Bon pour les environnements calmes (bibliothèque, open space)
- Vous pouvez voir l'alerte sans déranger les autres

### Configuration minimaliste
✅ Sons + ❌ Notifications + ❌ Popup
- **Juste un rappel sonore**
- Pas de fenêtre qui s'affiche
- Bon si vous êtes déjà très discipliné

### Configuration visuelle
✅ Popup + ❌ Sons + ❌ Notifications
- **Silencieux**
- Parfait si vous êtes en réunion/appel
- L'alerte visuelle suffit

## 🔧 Paramètres avancés

### Cooldown des alertes
- **Par défaut** : 10 secondes
- Empêche le spam d'alertes si vous restez sur le site
- Modifiable dans **Configuration → Paramètres avancés**

### Intervalle de vérification
- **Par défaut** : 2 secondes
- Fréquence à laquelle l'app vérifie votre onglet actif
- Plus c'est bas, plus c'est réactif (mais plus de ressources CPU)

## 🎵 Personnaliser les sons (avancé)

Les sons sont définis dans le code (`main.py`, fonction `play_alert_sound_repeated`).

Sons actuels :
- **Grave** : 800 Hz, 300ms
- **Aigu** : 1200 Hz, 200ms
- **Répétitions** : 3 fois

Pour modifier :
```python
def play_alert_sound_repeated(self):
    try:
        for i in range(3):  # Nombre de répétitions
            winsound.Beep(800, 300)   # (Fréquence, Durée en ms)
            time.sleep(0.15)
            winsound.Beep(1200, 200)
            time.sleep(0.3)
    except:
        pass
```

## 🧪 Tester les alertes

Pour tester si vos alertes fonctionnent :

1. Lancez l'application
2. Cliquez sur **"▶️ Démarrer"** (lancer une session de travail)
3. Ouvrez votre navigateur (Chrome/Firefox/Edge)
4. Allez sur un site blacklisté (ex: youtube.com)
5. **Les alertes devraient se déclencher !**

Si rien ne se passe :
- Vérifiez que vous êtes en **mode travail** (pas en pause)
- Vérifiez que le site est dans la **blacklist** (Configuration)
- Vérifiez que les alertes sont **activées** dans la configuration
- Regardez la console pour voir les erreurs

## 📝 Notes importantes

### Notifications Windows
- Nécessite la bibliothèque `plyer`
- Fonctionne sur Windows 10/11
- Si les notifications ne s'affichent pas, vérifiez les paramètres Windows :
  - Paramètres → Système → Notifications
  - Assurez-vous que les notifications sont activées

### Sons
- Utilise `winsound` (natif Windows)
- Fonctionne même si votre PC est en mode silencieux
- Le volume dépend de vos paramètres système

### Popup
- Toujours au premier plan
- Peut voler le focus de votre navigateur
- Se ferme automatiquement si vous ne cliquez pas

## 🚀 Prochaines améliorations possibles

- 🎨 Sons personnalisables (MP3, WAV)
- 📊 Compteur d'alertes par session
- ⏰ Alertes programmées ("Pause dans 5 minutes")
- 🎭 Modes de sévérité (doux, moyen, strict)
- 🌙 Mode "Ne pas déranger" avec plages horaires

---

**Bon focus! 💪🔥**

