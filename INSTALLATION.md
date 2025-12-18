# 📦 Guide d'Installation - StopDoomScroll

## 🎯 Installation rapide (5 minutes)

### Étape 1 : Installer Python

1. Allez sur [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Téléchargez **Python 3.11** ou **Python 3.12** (⚠️ **PAS 3.13** - problèmes de compatibilité)
3. Lancez l'installateur
4. ⚠️ **IMPORTANT** : Cochez **"Add Python to PATH"** en bas de la fenêtre !
5. Cliquez sur "Install Now"
6. Attendez la fin de l'installation

> **Note** : Si vous avez Python 3.13, les nouvelles dépendances corrigées devraient fonctionner, mais Python 3.11/3.12 sont plus stables.

### Étape 2 : Vérifier l'installation de Python

1. Ouvrez **PowerShell** ou **Invite de commandes** :
   - Appuyez sur `Windows + R`
   - Tapez `powershell` ou `cmd`
   - Appuyez sur Entrée

2. Tapez cette commande :
   ```bash
   python --version
   ```

3. Vous devriez voir quelque chose comme : `Python 3.11.x`

### Étape 3 : Installer les dépendances

1. Dans PowerShell/CMD, naviguez vers le dossier du projet :
   ```bash
   cd "C:\1_Startup\Python_StopDoomScroll"
   ```

2. **Option A - Script automatique (recommandé)** :
   ```bash
   install.bat
   ```
   Le script installera tout automatiquement !

3. **Option B - Installation manuelle** :
   ```bash
   pip install -r requirements.txt
   ```

4. Attendez que tout s'installe (1-2 minutes)

**Dépendances installées** :
- `customtkinter` : Interface graphique moderne
- `psutil` : Monitoring système
- `pywin32` : API Windows (détection fenêtres)
- `plyer` : Notifications Windows natives

### Étape 4 : Lancer l'application

**Méthode 1 - Double-clic (facile)** :
- Double-cliquez sur `start.bat`

**Méthode 2 - Ligne de commande** :
```bash
python main.py
```

## ✅ C'est tout !

L'application devrait maintenant s'ouvrir avec une fenêtre moderne et sombre.

## 🐛 Problèmes courants

### ⚠️ Erreur avec Python 3.13 : "Failed to build Pillow" ou "KeyError: '__version__'"

**Cause** : Python 3.13 est très récent et certaines bibliothèques ne sont pas encore compatibles.

**Solution 1 - Essayer les nouvelles dépendances (déjà corrigées)** :
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Solution 2 - Utiliser Python 3.11 ou 3.12 (recommandé)** :
1. Désinstallez Python 3.13
2. Téléchargez Python 3.12 depuis [python.org](https://www.python.org/downloads/)
3. Installez-le (cochez "Add to PATH")
4. Réessayez : `pip install -r requirements.txt`

### Erreur : "python n'est pas reconnu"

**Solution** : Python n'est pas dans le PATH
1. Désinstallez Python
2. Réinstallez en cochant bien **"Add Python to PATH"**

### Erreur : "pip n'est pas reconnu"

**Solution** :
```bash
python -m ensurepip --upgrade
```

### Erreur lors de l'installation de customtkinter

**Solution** : Mettez à jour pip d'abord
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### L'application se lance mais plante immédiatement

**Solution** : Réinstallez les dépendances
```bash
pip uninstall -y customtkinter psutil pygetwindow Pillow
pip install -r requirements.txt
```

### L'application ne détecte pas mes onglets

**Cause possible** : 
- Vous n'êtes pas en mode "travail" (cliquez sur Démarrer)
- Le navigateur n'affiche pas l'URL dans le titre de la fenêtre

**Solution** : 
- Vérifiez que le titre de l'onglet contient bien l'URL du site
- Certains modes de navigation privée peuvent masquer les URLs

## 🎮 Première utilisation

1. **Configurez vos sites** : Cliquez sur "⚙️ Configuration"
2. **Ajoutez des sites à bloquer** : Un par ligne (ex: youtube.com)
3. **Ajustez les durées** : Travail (25 min) / Pause (5 min)
4. **Sauvegardez** : Cliquez sur "💾 Sauvegarder"
5. **Démarrez** : Cliquez sur "▶️ Démarrer"

## 📞 Besoin d'aide ?

Si vous rencontrez un problème :

1. Vérifiez que Python 3.8+ est installé : `python --version`
2. Vérifiez que les dépendances sont installées : `pip list`
3. Lisez les messages d'erreur dans la console
4. Consultez le fichier `README.md` pour plus d'informations

## 🚀 Lancement automatique au démarrage (optionnel)

Pour lancer l'app automatiquement au démarrage de Windows :

1. Appuyez sur `Windows + R`
2. Tapez `shell:startup` et appuyez sur Entrée
3. Créez un raccourci vers `start.bat` dans ce dossier

---

**Bon courage dans votre productivité! 💪🔥**

