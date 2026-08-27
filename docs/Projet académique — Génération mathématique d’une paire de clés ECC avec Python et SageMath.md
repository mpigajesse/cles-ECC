# Projet académique — Génération mathématique d’une paire de clés ECC avec Python et SageMath

## 1. Objectif du projet

L'objectif est de développer un programme pédagogique en **Python/SageMath** permettant de comprendre et d'implémenter mathématiquement la génération d'une paire de clés basée sur la **cryptographie à courbe elliptique (ECC)**.

Le programme devra montrer clairement comment une **clé privée** permet de calculer une **clé publique**.

Le principe fondamental sera :

\[
Q = dG
\]

avec :

- `d` : clé privée ;
- `G` : point générateur de la courbe ;
- `Q` : clé publique ;
- `dG` : multiplication scalaire du point `G` par le nombre entier `d`.

Le projet devra privilégier la compréhension des mathématiques plutôt que l'utilisation directe d'une fonction toute faite de génération de clés.

---

# 2. Références GitHub étudiées

## 2.1 MauriceGit — Elliptic Curve Cryptography Seminar

Repository :

https://github.com/MauriceGit/Elliptic_Curve_Cryptography_Seminar

Fichier particulièrement intéressant :

https://github.com/MauriceGit/Elliptic_Curve_Cryptography_Seminar/blob/master/Code_examples/ecdh.sage.py

Ce projet est particulièrement pertinent pour notre travail car il contient du code **SageMath** consacré à l'ECDH et aux courbes elliptiques.

Le dépôt montre notamment le principe :

```python
privateA = 21
publicA = G * privateA
```

Ce qui correspond directement à :

\[
Q = dG
\]

Source GitHub :  
https://github.com/MauriceGit/Elliptic_Curve_Cryptography_Seminar

---

## 2.2 netesf13d — py-ecc

Repository :

https://github.com/netesf13d/py-ecc

Ce projet est une implémentation Python de primitives de cryptographie sur courbes elliptiques.

Il contient notamment :

- ECC ;
- ECDSA ;
- ECDH ;
- EdDSA ;
- algèbre des courbes elliptiques ;
- exemples sous Jupyter Notebook.

Le projet indique lui-même qu'il est destiné à un usage pédagogique et expérimental, ce qui le rend intéressant comme référence pour notre architecture.

---

## 2.3 AntonKueltz — fastecdsa

Repository :

https://github.com/AntonKueltz/fastecdsa

Ce projet est une bibliothèque Python consacrée à la cryptographie ECC.

Il est particulièrement intéressant pour étudier :

- les paramètres d'une courbe ;
- le point générateur ;
- l'ordre du point ;
- les coordonnées `(x,y)` ;
- les opérations sur les points ;
- les clés privées et publiques.

Le dépôt permet également de construire des courbes de Weierstrass sous la forme :

\[
y^2 = x^3 + ax + b \pmod p
\]

Source GitHub :  
https://github.com/AntonKueltz/fastecdsa

---

## 2.4 ecies/py

Repository :

https://github.com/ecies/py

Ce projet Python implémente ECIES et prend notamment en charge `secp256k1`.

Il est utile pour observer comment une implémentation pratique représente :

```text
Private Key
Public Key
```

et comment la clé publique est obtenue à partir de la clé privée.

Le projet utilise notamment :

```python
PrivateKey(...)
```

puis :

```python
public_key
```

Source GitHub :  
https://github.com/ecies/py

---

## 2.5 scipr-lab — ecfactory

Repository :

https://github.com/scipr-lab/ecfactory

Ce projet est particulièrement intéressant pour la partie **SageMath avancée**.

Il s'agit d'une bibliothèque SageMath permettant notamment de construire différentes familles de courbes elliptiques.

Elle nécessite une installation de SageMath.

Source GitHub :  
https://github.com/scipr-lab/ecfactory

---

# 3. Références secondaires

D'autres projets peuvent être consultés pour comprendre des implémentations plus complètes d'ECIES :

### ecies Python

https://github.com/djanie1/ecies

### ECIESPython

https://github.com/PeteMango/ECIESPython

### ECIES en C/OpenSSL/WolfSSL

https://github.com/insanum/ecies

Ces projets sont davantage orientés vers l'utilisation pratique d'ECC/ECIES que vers la démonstration mathématique élémentaire de `Q = dG`.

---

# 4. Notre objectif spécifique

Nous ne devons pas simplement faire :

```python
private_key = generate_private_key()
public_key = generate_public_key(private_key)
```

car cela cacherait précisément les mathématiques que nous voulons étudier.

Notre programme doit plutôt montrer :

```text
Paramètres de la courbe
        ↓
Point générateur G
        ↓
Génération de d
        ↓
Clé privée d
        ↓
Multiplication scalaire
        ↓
Q = d × G
        ↓
Clé publique Q
```

---

# 5. Modèle mathématique

Nous utiliserons une courbe elliptique de Weierstrass :

\[
E: y^2 = x^3 + ax + b \pmod p
\]

où :

- `p` est un nombre premier ;
- `a` est un paramètre de la courbe ;
- `b` est un paramètre de la courbe ;
- `G` est le point générateur ;
- `n` est l'ordre du générateur.

La condition de validité de la courbe est :

\[
4a^3 + 27b^2 \not\equiv 0 \pmod p
\]

---

# 6. Génération de la clé privée

La clé privée est un entier secret :

\[
d \in [1,n-1]
\]

Dans notre prototype pédagogique :

```python
d = random.randint(1, n - 1)
```

Dans une véritable implémentation cryptographique, la génération doit utiliser une source d'aléa cryptographiquement sûre.

La valeur `d` ne doit jamais être divulguée dans une utilisation réelle.

---

# 7. Calcul de la clé publique

La clé publique est calculée par :

\[
Q = dG
\]

Il s'agit d'une multiplication scalaire sur la courbe elliptique.

Si :

\[
d=5
\]

alors :

\[
Q=5G
\]

et :

\[
5G = G+G+G+G+G
\]

Le programme devra progressivement montrer comment cette opération est calculée.

---

# 8. Addition de deux points

Pour deux points :

\[
P=(x_1,y_1)
\]

et :

\[
Q=(x_2,y_2)
\]

on calcule :

\[
\lambda =
\frac{y_2-y_1}{x_2-x_1}
\pmod p
\]

puis :

\[
x_3 = \lambda^2-x_1-x_2 \pmod p
\]

et :

\[
y_3 = \lambda(x_1-x_3)-y_1 \pmod p
\]

Le programme devra implémenter cette opération.

---

# 9. Doublement d'un point

Lorsque :

\[
P=Q
\]

on utilise le doublement :

\[
2P=P+P
\]

Le coefficient devient :

\[
\lambda =
\frac{3x_1^2+a}{2y_1}
\pmod p
\]

Puis :

\[
x_3=\lambda^2-2x_1 \pmod p
\]

et :

\[
y_3=\lambda(x_1-x_3)-y_1 \pmod p
\]

---

# 10. Multiplication scalaire

C'est la partie centrale du projet.

Nous devons calculer :

\[
dG
\]

sans simplement appeler une fonction ECC toute faite.

Une première version pédagogique pourra utiliser :

```text
result = O

répéter d fois :
    result = result + G
```

où `O` représente le point à l'infini.

Ensuite, une deuxième version devra utiliser l'algorithme **double-and-add**, beaucoup plus efficace.

Principe :

```text
d = 13

13 en binaire = 1101

13G
 ↓
8G + 4G + G
```

Le programme pourra donc effectuer :

```text
G
2G
4G
8G
13G
```

---

# 11. Architecture souhaitée

Le projet devra être organisé ainsi :

```text
ecc-key-generator/
│
├── README.md
│
├── requirements.txt
│
├── src/
│   ├── curve.py
│   ├── point.py
│   ├── arithmetic.py
│   ├── scalar_multiplication.py
│   ├── key_generation.py
│   └── main.py
│
├── tests/
│   ├── test_curve.py
│   ├── test_point.py
│   ├── test_arithmetic.py
│   └── test_key_generation.py
│
├── sage/
│   ├── ecc_demo.sage
│   └── ecc_verification.sage
│
└── docs/
    ├── mathematics.md
    ├── architecture.md
    └── references.md
```

---

# 12. Fonctionnalités obligatoires

Le programme devra être capable de :

### A. Définir une courbe

```text
p
a
b
```

### B. Définir le générateur

```text
G = (Gx, Gy)
```

### C. Vérifier que G appartient à la courbe

Vérifier :

\[
y_G^2 \equiv x_G^3 + ax_G + b \pmod p
\]

### D. Générer une clé privée

```text
d
```

### E. Calculer la clé publique

```text
Q = dG
```

### F. Afficher les calculs

Le programme devra expliquer les opérations :

```text
1G
2G
4G
8G
...
dG
```

### G. Vérifier la clé publique

Vérifier que :

\[
Q \in E
\]

et éventuellement :

\[
nQ=O
\]

si `n` est l'ordre du générateur.

---

# 13. Mode pédagogique

Le programme devra proposer deux modes.

## Mode 1 — Démonstration

Utiliser de petits nombres afin que l'utilisateur puisse suivre les calculs.

Exemple :

```text
p = 17
a = 2
b = 2
G = (...)
d = 5
```

Le programme affiche chaque opération.

---

## Mode 2 — Courbe réaliste

Utiliser une courbe standard telle que `secp256k1` ou une courbe NIST adaptée.

Le but sera alors de comparer :

```text
Notre implémentation pédagogique
              VS
Bibliothèque cryptographique
```

Attention : notre implémentation pédagogique ne devra pas être présentée comme une bibliothèque de production.

---

# 14. Utilisation de SageMath

SageMath sera utilisé pour :

- vérifier les courbes ;
- vérifier les opérations ;
- effectuer des calculs mathématiques ;
- comparer notre implémentation ;
- visualiser certains résultats ;
- valider les résultats de notre code Python.

Exemple conceptuel :

```python
E = EllipticCurve(GF(p), [a, b])

G = E(Gx, Gy)

Q = d * G
```

Cela nous permettra de comparer :

```text
Notre calcul
     ↓
Q_manual

SageMath
     ↓
Q_sage
```

Puis :

```python
assert Q_manual == Q_sage
```

---

# 15. Consigne principale à donner à l'IA / au développeur

> Développer un programme pédagogique en Python et SageMath permettant de générer une paire de clés ECC en montrant explicitement les calculs mathématiques.
>
> Le programme doit partir des paramètres d'une courbe elliptique de Weierstrass définie sur un corps fini :
>
> \[
> y^2=x^3+ax+b\pmod p
> \]
>
> Il doit générer une clé privée `d`, sélectionner un point générateur `G`, puis calculer la clé publique :
>
> \[
> Q=dG
> \]
>
> L'implémentation doit contenir les opérations mathématiques nécessaires :
>
> - addition de points ;
> - doublement de points ;
> - inversion modulaire ;
> - multiplication scalaire ;
> - double-and-add ;
> - vérification de l'appartenance d'un point à la courbe.
>
> Ne pas masquer les opérations principales derrière une API de génération de clés.
>
> Le programme doit afficher les étapes intermédiaires afin qu'un étudiant puisse comprendre comment la clé publique est mathématiquement obtenue à partir de la clé privée.
>
> SageMath devra être utilisé comme outil de vérification indépendante des résultats.
>
> Le programme devra également contenir des tests permettant de comparer les résultats de notre implémentation avec SageMath.
>
> L'implémentation est strictement pédagogique et ne doit pas être présentée comme une solution cryptographique destinée à protéger de véritables secrets.

---

# 16. Résultat attendu

À la fin, l'utilisateur doit pouvoir exécuter :

```bash
python main.py
```

et obtenir quelque chose ressemblant à :

```text
==================================================
        ECC KEY GENERATOR - MODE PEDAGOGIQUE
==================================================

[1] Courbe elliptique
    y² = x³ + ax + b (mod p)

[2] Paramètres
    p = ...
    a = ...
    b = ...

[3] Point générateur
    G = (...)

[4] Vérification
    G appartient à la courbe : OK

[5] Génération de la clé privée
    d = ...

[6] Multiplication scalaire
    Q = d × G

    Étapes :
    G
    2G
    4G
    8G
    ...

[7] Clé publique
    Q = (...)

[8] Vérification
    Q appartient à la courbe : OK

==================================================
    CLÉ PRIVÉE : d
    CLÉ PUBLIQUE : Q
==================================================
```

---

# 17. Principe fondamental à retenir

Le cœur mathématique du projet est :

```text
                    CLÉ PRIVÉE
                         d
                         │
                         │
                         ▼
                  MULTIPLICATION
                    SCALAIRE
                         │
                         │ d × G
                         ▼
                POINT GÉNÉRATEUR
                         G
                         │
                         ▼
                  CLÉ PUBLIQUE
                         Q
```

Mathématiquement :

\[
\boxed{Q=dG}
\]

La sécurité repose notamment sur le fait qu'il est facile de calculer `Q` à partir de `d` et `G`, alors que retrouver `d` à partir de `Q` et `G` correspond au problème du logarithme discret sur courbe elliptique.

---

# 18. Sources GitHub

1. MauriceGit — Elliptic Curve Cryptography Seminar  
   https://github.com/MauriceGit/Elliptic_Curve_Cryptography_Seminar

2. MauriceGit — Exemple ECDH SageMath  
   https://github.com/MauriceGit/Elliptic_Curve_Cryptography_Seminar/blob/master/Code_examples/ecdh.sage.py

3. netesf13d — py-ecc  
   https://github.com/netesf13d/py-ecc

4. AntonKueltz — fastecdsa  
   https://github.com/AntonKueltz/fastecdsa

5. ecies — Python  
   https://github.com/ecies/py

6. scipr-lab — ecfactory  
   https://github.com/scipr-lab/ecfactory

7. PeteMango — ECIESPython  
   https://github.com/PeteMango/ECIESPython

8. insanum — ECIES  
   https://github.com/insanum/ecies

Ces dépôts servent de **références et sources d'inspiration**. Le code de notre projet devra être développé de manière indépendante et adapté à notre objectif pédagogique.

---

# 19. Étape suivante du projet

La prochaine étape consiste à construire le projet progressivement :

```text
ÉTAPE 1
│
├── Choisir une petite courbe pédagogique
│
ÉTAPE 2
│
├── Implémenter l'arithmétique modulaire
│
ÉTAPE 3
│
├── Implémenter l'inversion modulaire
│
ÉTAPE 4
│
├── Implémenter Point
│
├── addition()
│
└── double()
│
ÉTAPE 5
│
├── Implémenter scalar_multiply()
│
ÉTAPE 6
│
├── Générer d
│
└── Calculer Q = dG
│
ÉTAPE 7
│
├── Vérifier avec SageMath
│
ÉTAPE 8
│
└── Passer à une courbe standard
```

**Ne commençons pas directement par `secp256k1`.** Pour comprendre et valider chaque formule, il est préférable de commencer avec une petite courbe sur un petit corps fini, puis de passer à une courbe réelle une fois que toutes les opérations fonctionnent.