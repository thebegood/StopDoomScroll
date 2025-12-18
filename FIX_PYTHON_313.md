# 🔧 Fix pour Python 3.13

Vous avez rencontré l'erreur **"Failed to build Pillow"** ou **"KeyError: '__version__'"** ? 

C'est parce que Python 3.13 est très récent et certaines bibliothèques ne sont pas encore totalement compatibles.

## ✅ Solutions (dans l'ordre recommandé)

### Solution 1 : Utiliser les dépendances corrigées (ESSAYEZ D'ABORD)

Les fichiers ont été mis à jour pour fonctionner avec Python 3.13. Essayez :

```bash
# 1. Mettez à jour pip
python -m pip install --upgrade pip setuptools wheel

# 2. Réinstallez les dépendances
pip install -r requirements.txt
```

Si ça fonctionne, lancez l'app :
```bash
python main.py
```

---

### Solution 2 : Installer Python 3.12 (RECOMMANDÉ si Solution 1 échoue)

Python 3.12 est stable et toutes les bibliothèques sont compatibles.

**Étapes** :

1. **Désinstaller Python 3.13** :
   - Panneau de configuration → Programmes → Désinstaller un programme
   - Trouvez "Python 3.13" et désinstallez-le

2. **Télécharger Python 3.12** :
   - Allez sur [https://www.python.org/downloads/release/python-3121/](https://www.python.org/downloads/release/python-3121/)
   - Téléchargez "Windows installer (64-bit)"

3. **Installer Python 3.12** :
   - Lancez l'installateur
   - ⚠️ **COCHEZ "Add Python to PATH"** ← IMPORTANT !
   - Cliquez sur "Install Now"

4. **Vérifier l'installation** :
   ```bash
   python --version
   # Devrait afficher: Python 3.12.x
   ```

5. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

6. **Lancer l'app** :
   ```bash
   python main.py
   ```

---

### Solution 3 : Utiliser un environnement virtuel

Si vous voulez garder Python 3.13 pour d'autres projets :

```bash
# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
venv\Scripts\activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Lancer l'app
python main.py
```

---

## 🎯 Utiliser le script d'installation automatique

Double-cliquez sur **`install.bat`** - il détectera votre version de Python et vous guidera !

---

## 💡 Pourquoi ces erreurs ?

Python 3.13 est sorti récemment (octobre 2024). Les bibliothèques ont besoin de temps pour :
- Compiler des "wheels" (binaires pré-compilés)
- Tester la compatibilité
- Mettre à jour leur code

C'est normal ! Python 3.12 reste la version "stable" recommandée pour le moment.

---

## ✅ Vérification finale

Si tout fonctionne, vous devriez voir :

```bash
python main.py
```

→ Une fenêtre moderne et sombre devrait s'ouvrir avec le timer Pomodoro ! 🎉

---

**Besoin d'aide ?** Lisez `INSTALLATION.md` pour plus de détails.

