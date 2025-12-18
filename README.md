# 🎯 StopDoomScroll

Une application Windows pour arrêter le doomscrolling et rester concentré sur votre travail avec la technique Pomodoro.

## 🌟 Fonctionnalités

- ⏱️ **Timer Pomodoro** personnalisable (travail + pauses)
- 🚫 **Blocage intelligent** des sites distrayants (YouTube, Facebook, Reddit, etc.)
- 🔔 **Système d'alerte multi-niveaux** :
  - 🔊 Sons d'alerte répétés (très audibles)
  - 🔔 Notifications Windows natives
  - 🪟 Fenêtres popup au premier plan
  - ⚙️ Activables/désactivables individuellement
- ☕ **Mode pause** où tous les sites sont autorisés
- ⚙️ **Configuration facile** via une interface graphique
- 🪟 **Fenêtre légère** et discrète qui reste au premier plan

## 📋 Prérequis

- **Windows 10/11**
- **Python 3.8 à 3.12** installé sur votre machine
  - ⚠️ **Recommandé** : Python 3.11 ou 3.12
  - ⚠️ **Python 3.13** peut avoir des problèmes de compatibilité (mais les dépendances sont corrigées)

## 🚀 Installation

### 1. Installer Python

Si vous n'avez pas Python, téléchargez-le depuis [python.org](https://www.python.org/downloads/) et installez-le.

⚠️ **Important** : Cochez "Add Python to PATH" pendant l'installation !

### 2. Installer les dépendances

Ouvrez un terminal (PowerShell ou CMD) dans le dossier du projet et exécutez :

```bash
pip install -r requirements.txt
```

### 3. Lancer l'application

```bash
python main.py
```

## 🎮 Utilisation

### Démarrer une session de travail

1. Cliquez sur **"▶️ Démarrer"**
2. Le timer commence avec la durée de travail configurée (par défaut 25 minutes)
3. L'application surveille vos onglets de navigateur
4. Si vous allez sur un site blacklisté, une alerte s'affiche avec un son

### Pendant la session

- **⏸️ Pause** : Met le timer en pause (le monitoring continue)
- **⏹️ Arrêter** : Arrête complètement la session

### Mode Pause automatique

- À la fin du temps de travail, une pause démarre automatiquement
- Pendant la pause, **aucune alerte** ne s'affichera
- Profitez de votre pause pour vous détendre ! ☕

### Configuration

Cliquez sur **"⚙️ Configuration"** pour :

- Modifier les durées de travail et de pause
- Ajouter/retirer des sites de la blacklist
- **Configurer les types d'alertes** :
  - Sons d'alerte
  - Notifications Windows
  - Fenêtres popup
- Ajuster les paramètres avancés (cooldown, intervalle)

💡 **Astuce** : Vous pouvez désactiver les sons si vous êtes en open space, et garder juste les notifications !

## ⚙️ Configuration avancée

Le fichier `config.json` contient tous les paramètres :

```json
{
  "pomodoro": {
    "work_duration": 25,      // Durée de travail en minutes
    "break_duration": 5,       // Durée de pause en minutes
    "sound_enabled": true      // Activer les sons
  },
  "blacklist": [
    "youtube.com",
    "facebook.com",
    // ... autres sites
  ],
  "check_interval": 2,         // Vérification toutes les X secondes
  "alert_cooldown": 10         // Délai minimum entre 2 alertes (secondes)
}
```

## 🌐 Navigateurs supportés

- ✅ Google Chrome
- ✅ Mozilla Firefox
- ✅ Microsoft Edge

## 💡 Astuces

1. **Personnalisez votre blacklist** : Ajoutez les sites qui vous distraient le plus
2. **Adaptez les durées** : Trouvez le rythme qui vous convient (25/5, 50/10, etc.)
3. **Configurez les alertes** : Choisissez sons + notifications + popup, ou juste ce que vous voulez
4. **Mode discret** : Désactivez les sons en open space, gardez les notifications
5. **Réduisez la fenêtre** : Cliquez sur "➖ Réduire" pour la mettre en icône
6. **Respectez les pauses** : Elles sont essentielles pour rester productif !

📖 **Voir [ALERTES.md](ALERTES.md)** pour tout savoir sur le système d'alertes !

## 🐛 Dépannage

### L'application ne détecte pas mes onglets ⚠️ PROBLÈME COURANT

**Symptôme** : Les tests d'alertes fonctionnent, mais l'app ne réagit pas quand vous êtes sur un site blacklisté.

**Solution rapide** :

1. **Lancez le script de debug** :
   ```bash
   python debug_detection.py
   ```

2. Ouvrez votre navigateur et allez sur le site à bloquer
3. Observez ce qui s'affiche dans la console
4. Si le site n'est pas détecté, ajoutez un mot-clé du titre dans la blacklist

**Mode debug avancé** :

1. Ouvrez `config.json`
2. Changez `"debug_mode": false` en `"debug_mode": true`
3. Lancez `python main.py`
4. Cliquez sur "▶️ Démarrer"
5. Regardez la console pour voir ce qui est détecté

📖 **Consultez [GUIDE_DEBUG.md](GUIDE_DEBUG.md)** pour un guide complet !

### Erreur lors du lancement

```bash
# Réinstallez les dépendances
pip install --upgrade -r requirements.txt
```

### Les alertes ne s'affichent pas

- Vérifiez que vous êtes bien en **mode travail** (bouton "Démarrer" cliqué)
- Vérifiez le **cooldown** des alertes dans la configuration

## 📝 TODO (Fonctionnalités futures)

- [ ] Statistiques détaillées des sessions
- [ ] Graphiques de productivité
- [ ] Export des données en CSV
- [ ] Mode "Focus intense" (blocage complet)
- [ ] Whitelist (autoriser seulement certains sites)
- [ ] Icône dans la barre des tâches (system tray)

## 🤝 Contribution

N'hésitez pas à proposer des améliorations ou à signaler des bugs !

## 📄 Licence

Projet personnel - Libre d'utilisation et de modification

---

**Bonne productivité! 💪🔥**

