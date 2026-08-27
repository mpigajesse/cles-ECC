# Plan d'implémentation - Générateur de clés ECC

## 📅 Phases du projet

### **PHASE 1 : Infrastructure de base** ✅
- [ ] Structure des dossiers
- [ ] Fichiers de configuration (`requirements.txt`, `setup.py`)
- [ ] Script principal avec menus

### **PHASE 2 : Arithmétique modulaire** 
- [ ] Inversion modulaire (algorithme d'Euclide étendu)
- [ ] Modulo inverse avec vérification
- [ ] Tests unitaires

### **PHASE 3 : Courbe elliptique**
- [ ] Classe `EllipticCurve` - Weierstrass : y² = x³ + ax + b (mod p)
- [ ] Vérification de validité de courbe
- [ ] Tests unitaires

### **PHASE 4 : Points sur courbe**
- [ ] Classe `Point` avec coordonnées (x, y)
- [ ] Point à l'infini (neutre)
- [ ] Vérification d'appartenance à la courbe
- [ ] Tests unitaires

### **PHASE 5 : Opérations sur points**
- [ ] Addition de deux points différents
- [ ] Doublement d'un point
- [ ] Gestion des cas spéciaux
- [ ] Tests unitaires

### **PHASE 6 : Multiplication scalaire**
- [ ] Approche naïve : boucle (pour la pédagogie)
- [ ] Algorithme double-and-add (efficace)
- [ ] Affichage des étapes intermédiaires
- [ ] Tests unitaires

### **PHASE 7 : Génération de clés**
- [ ] Génération de clé privée `d` aléatoire
- [ ] Calcul de clé publique `Q = dG`
- [ ] Formatage et affichage
- [ ] Tests unitaires

### **PHASE 8 : Validation avec SageMath**
- [ ] Scripts de vérification SageMath
- [ ] Comparaison résultats Python ↔ SageMath
- [ ] Tests de conformité

### **PHASE 9 : Modes d'utilisation**
- [ ] Mode pédagogique (petite courbe p=17, p=23, etc.)
- [ ] Mode réaliste (secp256k1, NIST P-256)
- [ ] Interface utilisateur améliorée
- [ ] Documentation

### **PHASE 10 : Documentation et tests**
- [ ] README complet
- [ ] Documentation mathématique
- [ ] Architecture document
- [ ] Couverture de tests 80%+

---

## 📂 Structure finale attendue

```
cles-ECC/
│
├── README.md                 # Guide principal
├── PLAN_IMPLEMENTATION.md    # Ce fichier
├── requirements.txt          # Dépendances Python
│
├── src/
│   ├── __init__.py
│   ├── curve.py             # Classe EllipticCurve
│   ├── point.py             # Classe Point
│   ├── arithmetic.py        # Opérations modulaires
│   ├── operations.py        # Addition, doublement
│   ├── scalar_mult.py       # Multiplication scalaire
│   ├── key_generation.py    # Génération de clés
│   └── main.py              # Point d'entrée
│
├── tests/
│   ├── __init__.py
│   ├── test_arithmetic.py
│   ├── test_curve.py
│   ├── test_point.py
│   ├── test_operations.py
│   ├── test_scalar_mult.py
│   └── test_key_generation.py
│
├── sage/
│   ├── demo_pedagogique.sage      # Petite courbe
│   ├── demo_secp256k1.sage        # Courbe réelle
│   └── verification.sage          # Vérification
│
└── docs/
    ├── mathematics.md      # Explications mathématiques
    ├── architecture.md     # Architecture du code
    └── references.md       # Références GitHub
```

---

## 🎯 Jalons clés

| Jalon | Description | Entrée | Sortie |
|-------|-------------|--------|--------|
| **M1** | Arithmétique modulaire | Nombres modulo | Inversion modulaire vérifiée |
| **M2** | Points valides | Courbe E | Points ∈ E confirmés |
| **M3** | Opérations basiques | P, Q sur E | P + Q, 2P calculés |
| **M4** | Multiplication scalaire | d, G | dG calculé (demo + fast) |
| **M5** | Génération clés | d aléatoire | Q = dG formé |
| **M6** | Vérification SageMath | Q calculée | Q_sage == Q_python ✓ |
| **M7** | Interfaces | Modes | Mode pédago + réaliste |
| **M8** | Tests complets | Couverture | 80%+ atteint |

---

## 🔧 Technologies

| Composant | Technologie | Utilisation |
|-----------|------------|-------------|
| Implémentation | Python 3.9+ | Code principal |
| Mathématiques avancées | SageMath | Vérification, test |
| Tests | pytest | Test unitaires |
| Validation | ecdsa (externe) | Comparaison |

---

## ⏱️ Estimation

- **Phase 1-3** : ~2-3h (fondations)
- **Phase 4-6** : ~4-5h (cœur mathématique)
- **Phase 7-8** : ~2-3h (génération + validation)
- **Phase 9-10** : ~2h (interfaces + docs)

**Total estimé** : 12-16 heures de développement

---

## 🚀 Prochaines étapes

1. **Créer la structure** (Phase 1)
2. **Implémenter arithmétique** (Phase 2)
3. **Tester chaque brique** (TDD à chaque phase)
4. **Valider avec SageMath** (Phase 8)
5. **Publier et documenter** (Phase 10)

**Commençons ? Vous êtes prêt pour la Phase 1 ?**
