# 🐛 Guide de Debug - Détection des sites

## Problème : L'application ne détecte pas certains sites

Si l'application ne détecte pas quand vous êtes sur Instagram, YouTube ou d'autres sites, suivez ce guide.

## 🔍 Étape 1 : Activer le mode debug

### Méthode A : Via config.json (Recommandé)

1. Ouvrez `config.json`
2. Changez `"debug_mode": false` en `"debug_mode": true`
3. Sauvegardez le fichier
4. Lancez l'app : `python main.py`
5. Cliquez sur "▶️ Démarrer"
6. Ouvrez votre navigateur et allez sur un site blacklisté
7. Regardez la **console** (la fenêtre noire où vous avez lancé l'app)

Vous verrez des messages comme :
```
[DEBUG] Fenêtre active: Instagram • Photos and videos - Google Chrome
[DEBUG] Navigateur détecté! Titre: Instagram • Photos and videos - Google Chrome
[DEBUG] 🚨 SITE BLOQUÉ DÉTECTÉ: instagram.com
```

### Méthode B : Script de debug standalone

Lancez le script de debug dédié :

```bash
python debug_detection.py
```

Ce script affichera **en temps réel** le titre de toutes vos fenêtres actives et vous dira si elles seraient détectées par l'app.

## 🔍 Étape 2 : Comprendre ce qui est détecté

### Comment fonctionne la détection ?

L'application lit le **titre de la fenêtre** de votre navigateur. Par exemple :

- **YouTube** : `YouTube - Google Chrome` ou `Nom de la vidéo - YouTube`
- **Instagram** : `Instagram • Photos and videos - Google Chrome`
- **Facebook** : `Facebook - Google Chrome`
- **Reddit** : `reddit: the front page of the internet - Mozilla Firefox`

### Pourquoi ça ne marche pas toujours ?

1. **Le titre ne contient pas l'URL** : Certains sites affichent juste leur nom
2. **URL tronquée** : Le navigateur peut couper le titre s'il est trop long
3. **Format différent** : Instagram peut s'afficher comme "Insta" ou "@username • Instagram"
4. **Blacklist incorrecte** : Si vous mettez `https://www.instagram.com/` au lieu de `instagram.com`

## ✅ Étape 3 : Corriger la blacklist

### Format correct

Dans `config.json`, la blacklist doit contenir des mots-clés **simples** :

✅ **BON** :
```json
"blacklist": [
  "youtube.com",
  "youtube",
  "instagram.com",
  "instagram",
  "facebook.com",
  "reddit.com",
  "tiktok.com"
]
```

❌ **MAUVAIS** :
```json
"blacklist": [
  "https://www.youtube.com/",
  "https://www.instagram.com/",
  "http://reddit.com/"
]
```

### Pourquoi ?

Le code nettoie automatiquement les URLs, mais il vaut mieux mettre directement le format simple.

## 🧪 Étape 4 : Tester avec différents formats

Si `instagram.com` ne fonctionne pas, essayez d'ajouter dans la blacklist :

```json
"blacklist": [
  "instagram.com",
  "instagram",
  "insta"
]
```

Lancez `debug_detection.py` pour voir quel mot-clé apparaît dans le titre de votre fenêtre.

## 🔧 Étape 5 : Vérifier que vous êtes en mode travail

L'application ne surveille QUE si :
- ✅ Vous avez cliqué sur **"▶️ Démarrer"**
- ✅ Le timer est actif
- ✅ Vous n'êtes **PAS en pause**

Si le statut affiche "⏸️ En attente" ou "☕ Pause", la détection est désactivée !

## 📊 Cas spécifiques

### Instagram

Titres possibles :
- `Instagram • Photos and videos`
- `Instagram`
- `@username • Instagram`
- `Login • Instagram`

**Solution** : Ajoutez `"instagram"` (sans .com) dans la blacklist

### YouTube

Titres possibles :
- `Titre de la vidéo - YouTube`
- `(123) YouTube - Notifications`
- `YouTube`

**Solution** : `"youtube"` devrait suffire

### TikTok

Titres possibles :
- `TikTok - Make Your Day`
- `@username's video on TikTok`

**Solution** : `"tiktok"` devrait suffire

## 🐛 Problèmes courants

### Problème 1 : "Rien ne s'affiche dans la console"

**Solution** : Vérifiez que :
- Vous avez activé `"debug_mode": true` dans config.json
- Vous avez relancé l'application APRÈS avoir modifié config.json
- Vous regardez bien la console (fenêtre noire) et pas l'interface graphique

### Problème 2 : "Le navigateur n'est pas détecté"

**Cause** : Le titre de la fenêtre ne contient pas "chrome", "firefox", "edge" ou "mozilla"

**Solution** : Lancez `debug_detection.py` et voyez ce qui s'affiche. Si votre navigateur s'appelle différemment (ex: "Brave", "Opera"), modifiez le code :

```python
# Dans main.py, ligne ~245
is_browser = any(browser in window_title_lower for browser in 
               ['chrome', 'firefox', 'edge', 'mozilla', 'browser', 'brave', 'opera'])
```

### Problème 3 : "Le site est détecté mais pas d'alerte"

**Vérifiez** :
1. Le cooldown : Par défaut, une alerte ne peut se déclencher que toutes les 10 secondes
2. Que les alertes sont activées dans Configuration
3. Que le son/notifications/popup sont activés

## 🎯 Exemple complet

**Situation** : Vous voulez bloquer Instagram

1. **Lancez le debug** :
   ```bash
   python debug_detection.py
   ```

2. **Ouvrez Instagram** dans Chrome

3. **Observez la console** :
   ```
   🪟 Fenêtre active: Instagram • Photos and videos - Google Chrome
   ✅ NAVIGATEUR DÉTECTÉ!
   🚨 SITES BLOQUÉS DÉTECTÉS: instagram.com
   ```

4. **Si détecté** ✅ : Votre blacklist est bonne ! Lancez l'app normale
5. **Si pas détecté** ❌ : Notez le titre exact et ajoutez un mot-clé qui apparaît dedans

## 💡 Astuces

1. **Soyez large** : Ajoutez plusieurs variantes
   - `instagram.com`
   - `instagram`
   - `insta` (si pas trop large)

2. **Testez régulièrement** : Les navigateurs peuvent changer le format des titres

3. **Utilisez le debug** : C'est le meilleur moyen de comprendre ce qui se passe

## 📝 Checklist de dépannage

- [ ] Mode debug activé (`"debug_mode": true`)
- [ ] Application lancée avec `python main.py`
- [ ] Session démarrée (bouton ▶️)
- [ ] Pas en mode pause
- [ ] Navigateur ouvert sur le site à bloquer
- [ ] Onglet du navigateur actif (au premier plan)
- [ ] Console visible pour voir les messages debug
- [ ] Blacklist contient le bon mot-clé
- [ ] Cooldown respecté (attendre 10 secondes entre les tests)
- [ ] Au moins une option d'alerte activée (son/notification/popup)

---

**Toujours des problèmes ?** Copiez les logs de la console et vérifiez ce qui est affiché !



