# Clés ECC - Générateur pédagogique de paires de clés

**Un projet académique** pour comprendre la cryptographie par courbes elliptiques en implémentant mathématiquement `Q = dG`

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Status](https://img.shields.io/badge/status-In%20Development-yellow.svg)

---

## 📖 Objectif

Développer un **générateur pédagogique de paires de clés ECC** qui montre **explicitement les calculs mathématiques** au lieu de les masquer derrière une API.

Le projet implémente :
- **Courbes elliptiques** de Weierstrass : `y² = x³ + ax + b (mod p)`
- **Opérations sur points** : addition, doublement, multiplication scalaire
- **Génération de clés** : clé privée `d`, clé publique `Q = dG`
- **Vérification** avec SageMath comme outil indépendant

### Formule fondamentale

```
Q = dG

où :
- d  = clé privée (scalaire secret)
- G  = point générateur (public)
- Q  = clé publique (résultat public)
```

---

## 🚀 Quick Start

### Installation

```bash
# Cloner le repository
git clone git@github.com:mpigajesse/cles-ECC.git
cd cles-ECC

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Exécution

```bash
# Lancer le programme principal
python src/main.py

# Exécuter les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=src
```

---

## 📂 Structure du projet

```
cles-ECC/
│
├── README.md                   # Ce fichier
├── PLAN_IMPLEMENTATION.md      # Roadmap du projet
├── requirements.txt            # Dépendances Python
├── setup.py                    # Configuration setuptools
│
├── src/                        # Code source principal
│   ├── __init__.py
│   ├── main.py                 # Point d'entrée (menus)
│   ├── curve.py                # Classe EllipticCurve
│   ├── point.py                # Classe Point
│   ├── arithmetic.py           # Arithmétique modulaire
│   ├── operations.py           # Opérations sur points
│   ├── scalar_mult.py          # Multiplication scalaire
│   └── key_generation.py       # Génération de clés
│
├── tests/                      # Suite de tests
│   ├── __init__.py
│   ├── test_arithmetic.py
│   ├── test_curve.py
│   ├── test_point.py
│   ├── test_operations.py
│   ├── test_scalar_mult.py
│   └── test_key_generation.py
│
├── sage/                       # Scripts SageMath
│   ├── demo_pedagogique.sage   # Démonstration petite courbe
│   ├── demo_secp256k1.sage     # Démonstration secp256k1
│   └── verification.sage       # Vérification des résultats
│
├── docs/                       # Documentation
│   ├── mathematics.md          # Explications mathématiques
│   ├── architecture.md         # Présentation architecture
│   └── references.md           # Références GitHub
│
├── keys/                       # Stockage des clés (vide, .gitignored)
└── scripts/                    # Scripts utilitaires
```

---

## 🔧 Phases d'implémentation

Voir [PLAN_IMPLEMENTATION.md](PLAN_IMPLEMENTATION.md) pour le détail complet.

| Phase | Description | Statut |
|-------|-------------|--------|
| **Phase 1** | Infrastructure de base | ✅ Complete |
| **Phase 2** | Arithmétique modulaire | ⏳ Todo |
| **Phase 3** | Courbe elliptique | ⏳ Todo |
| **Phase 4** | Points sur courbe | ⏳ Todo |
| **Phase 5** | Opérations sur points | ⏳ Todo |
| **Phase 6** | Multiplication scalaire | ⏳ Todo |
| **Phase 7** | Génération de clés | ⏳ Todo |
| **Phase 8** | Validation SageMath | ⏳ Todo |
| **Phase 9** | Modes d'utilisation | ⏳ Todo |
| **Phase 10** | Documentation & tests | ⏳ Todo |

---

## 📚 Modes disponibles

### Mode pédagogique
- Utilise une **petite courbe** (p=17, p=23, etc.)
- Affiche **toutes les étapes** des calculs
- Idéal pour comprendre les mathématiques

### Mode réaliste
- Utilise **secp256k1** (Bitcoin/Ethereum)
- Calculs efficients
- Montre les différences avec la pédagogie

### Mode NIST
- Utilise **NIST P-256**
- Standard cryptographique
- Comparaison avec les normes

---

## ✅ Fonctionnalités

- ✅ Classe `EllipticCurve` pour définir des courbes de Weierstrass
- ✅ Classe `Point` pour représenter des points sur la courbe
- ✅ Inversion modulaire (algorithme d'Euclide étendu)
- ✅ Addition de points : `P + Q`
- ✅ Doublement de point : `2P = P + P`
- ✅ Multiplication scalaire naïve (pédagogie) : `d × G` en boucle
- ✅ Multiplication scalaire efficace : algorithme double-and-add
- ✅ Génération de clé privée aléatoire
- ✅ Calcul de clé publique : `Q = dG`
- ✅ Affichage des étapes intermédiaires
- ✅ Vérification avec SageMath
- ✅ 80%+ couverture de tests
- ✅ Documentation mathématique

---

## 🧪 Tests

```bash
# Tous les tests
pytest tests/

# Tests avec couverture
pytest tests/ --cov=src --cov-report=html

# Tests d'un module spécifique
pytest tests/test_arithmetic.py -v

# Tests en mode verbose
pytest -vv
```

---

## 📖 Mathématiques

### Courbe elliptique (Weierstrass)
```
E: y² ≡ x³ + ax + b (mod p)
```

où `p` est premier et `4a³ + 27b² ≢ 0 (mod p)`

### Addition de points
```
Pour P ≠ Q :
  λ = (y₂ - y₁) / (x₂ - x₁) mod p
  x₃ = λ² - x₁ - x₂ mod p
  y₃ = λ(x₁ - x₃) - y₁ mod p
```

### Doublement de point
```
Pour P = Q :
  λ = (3x₁² + a) / (2y₁) mod p
  x₃ = λ² - 2x₁ mod p
  y₃ = λ(x₁ - x₃) - y₁ mod p
```

### Multiplication scalaire
```
Double-and-add algorithm :

d = 13 = 1101₂
13G = 8G + 4G + G
```

Voir [docs/mathematics.md](docs/mathematics.md) pour plus de détails.

---

## 🔐 Sécurité

⚠️ **IMPORTANT**

- Ce projet est **strictement pédagogique**
- **NE PAS utiliser en production** pour protéger des secrets
- Les clés privées ne sont **JAMAIS** commises dans git (`.gitignore`)
- Utiliser des `secrets_managers` pour les véritables secrets
- Pas de garanties de sécurité cryptographique

---

## 📚 Références

### Projets étudiés
1. [MauriceGit - ECC Seminar](https://github.com/MauriceGit/Elliptic_Curve_Cryptography_Seminar)
2. [netesf13d - py-ecc](https://github.com/netesf13d/py-ecc)
3. [AntonKueltz - fastecdsa](https://github.com/AntonKueltz/fastecdsa)
4. [ecies - Python](https://github.com/ecies/py)
5. [scipr-lab - ecfactory](https://github.com/scipr-lab/ecfactory)

Voir [docs/references.md](docs/references.md) pour la liste complète.

---

## 👤 Auteur

- **Jesse** ([mpigajesse@gmail.com](mailto:mpigajesse@gmail.com))

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir [LICENSE](LICENSE) pour les détails.

---

## 🎯 Contribution

Les contributions sont bienvenues ! Pour contribuer :

1. Fork le repository
2. Créer une branche feature (`git checkout -b feature/amazing`)
3. Committer les changements (`git commit -m 'Add amazing feature'`)
4. Pousser vers la branche (`git push origin feature/amazing`)
5. Ouvrir une Pull Request

---

## 📞 Support

Pour les questions ou problèmes :
- Ouvrir une [issue GitHub](https://github.com/mpigajesse/cles-ECC/issues)
- Consulter la documentation dans `/docs`
- Voir le plan d'implémentation [PLAN_IMPLEMENTATION.md](PLAN_IMPLEMENTATION.md)