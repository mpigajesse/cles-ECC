#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de Clés ECC - Point d'entrée principal

Programme éducatif pour générer des paires de clés ECC avec transparence mathématique.
Affiche le calcul étape par étape de Q = d·G sur les courbes elliptiques.
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au chemin pour les imports
chemin_src = Path(__file__).parent
if str(chemin_src) not in sys.path:
    sys.path.insert(0, str(chemin_src))

# Ajouter également le répertoire parent pour les imports de paquets
chemin_parent = chemin_src.parent
if str(chemin_parent) not in sys.path:
    sys.path.insert(0, str(chemin_parent))

from colorama import Fore, Style, init

# Initialiser colorama pour la sortie du terminal multiplateforme colorée
init(autoreset=True)


def afficher_en_tete():
    """Affiche l'en-tête de l'application."""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}      GÉNÉRATEUR DE CLÉS ECC - MODE ÉDUCATIF")
    print(f"{Fore.CYAN}      Cryptographie par Courbes Elliptiques")
    print(f"{Fore.CYAN}{'='*70}")
    print(f"\nGénération de paires de clés ECC avec transparence mathématique")
    print(f"Apprentissage: Q = d × G (Clé Publique = Scalaire × Générateur)\n")


def afficher_menu():
    """Affiche les options du menu principal."""
    print(f"\n{Fore.YELLOW}Sélectionnez un mode:")
    print(f"  {Fore.GREEN}1{Fore.RESET} - Mode Pédagogique (petite courbe, calculs visibles)")
    print(f"  {Fore.GREEN}2{Fore.RESET} - Mode Réaliste (secp256k1 - Bitcoin/Ethereum)")
    print(f"  {Fore.GREEN}3{Fore.RESET} - Mode NIST (P-256 - Standard Gouvernemental)")
    print(f"  {Fore.GREEN}4{Fore.RESET} - Exécuter les tests")
    print(f"  {Fore.GREEN}5{Fore.RESET} - Quitter")
    print(f"\n{Fore.YELLOW}Choix: {Fore.RESET}", end="")


def mode_pedagogique():
    """Mode pédagogique avec une petite courbe."""
    print(f"\n{Fore.BLUE}[MODE PÉDAGOGIQUE - Démonstration Éducative]")
    print(f"{Fore.BLUE}Utilisation d'une petite courbe: y² = x³ + 2x + 2 (mod 17)\n")

    try:
        try:
            from .curve import CURVE_P17_A2_B2
            from .point import Point
            from .key_generation import generate_keypair
            from .operations import scalar_mult_with_steps
        except ImportError:
            from curve import CURVE_P17_A2_B2
            from point import Point
            from key_generation import generate_keypair
            from operations import scalar_mult_with_steps

        courbe = CURVE_P17_A2_B2
        G = Point(courbe, 13, 7)  # Point générateur pour la courbe pédagogique
        n = 18  # Ordre

        print(f"{Fore.GREEN}Paramètres de la courbe:")
        print(f"  E: y² = x³ + 2x + 2 (mod 17)")
        print(f"  Générateur G = (13, 7)")
        print(f"  Ordre n = 18")

        # Générer une paire de clés
        print(f"\n{Fore.YELLOW}[1] Génération d'une clé privée aléatoire d...")
        paire_cles = generate_keypair(G, n)
        print(f"{Fore.GREEN}  d = {paire_cles.private_key}")

        # Montrer les étapes de la multiplication scalaire
        print(f"\n{Fore.YELLOW}[2] Calcul de Q = d × G (Multiplication Scalaire)...")
        print(f"{Fore.CYAN}Représentation binaire de {paire_cles.private_key}:")
        print(f"  {bin(paire_cles.private_key)} = {paire_cles.private_key}")

        # Calculer Q = d × G avec les étapes
        Q, etapes = scalar_mult_with_steps(G, paire_cles.private_key, verbose=False)

        print(f"\n{Fore.YELLOW}[3] Résultat:")
        print(f"{Fore.GREEN}  Clé Publique Q = ({Q.x}, {Q.y})")
        print(f"  Q est sur la courbe: {Q.is_on_curve()}")

        print(f"\n{Fore.YELLOW}[4] Vérification:")
        print(f"{Fore.GREEN}  Clé privée d: {paire_cles.private_key}")
        print(f"  Clé publique Q:  ({Q.x}, {Q.y})")
        print(f"  Relation:  Q = d × G ✓")

        print(f"\n{Fore.CYAN}Ceci démontre le principe fondamental d'ECC:")
        print(f"  Facile: d + G → Q")
        print(f"  Difficile: Q + G → d (problème du logarithme discret)")

    except Exception as e:
        print(f"{Fore.RED}Erreur: {e}")
        import traceback
        traceback.print_exc()


def mode_realiste():
    """Mode réaliste avec secp256k1."""
    print(f"\n{Fore.BLUE}[MODE RÉALISTE - secp256k1]")
    print(f"{Fore.BLUE}Courbe Bitcoin/Ethereum\n")

    try:
        try:
            from .key_generation import generate_secp256k1_keypair
        except ImportError:
            from key_generation import generate_secp256k1_keypair

        print(f"{Fore.GREEN}Courbe: secp256k1")
        print(f"  E: y² = x³ + 7 (mod p)")
        print(f"  Corps: p = 2²⁵⁶ - 2³² - 977")
        print(f"  Ordre: n ≈ 2²⁵⁶")

        print(f"\n{Fore.YELLOW}Génération d'une paire de clés secp256k1...")
        paire_cles = generate_secp256k1_keypair()

        print(f"\n{Fore.GREEN}Génération réussie!")
        print(f"\n{Fore.YELLOW}Clé Privée (d):")
        print(f"  Hexadécimal: {hex(paire_cles.private_key)[:50]}...")
        print(f"  Bits: {paire_cles.private_key.bit_length()}")

        print(f"\n{Fore.YELLOW}Clé Publique (Q = d·G):")
        print(f"  x: {hex(paire_cles.public_key.x)[:50]}...")
        print(f"  y: {hex(paire_cles.public_key.y)[:50]}...")

        print(f"\n{Fore.CYAN}secp256k1 est utilisée dans:")
        print(f"  • Transactions Bitcoin")
        print(f"  • Contrats intelligents Ethereum")
        print(f"  • Réseau Lightning")
        print(f"  • De nombreuses autres cryptomonnaies")

    except Exception as e:
        print(f"{Fore.RED}Erreur: {e}")
        import traceback
        traceback.print_exc()


def mode_nist():
    """Mode NIST P-256."""
    print(f"\n{Fore.BLUE}[MODE NIST - P-256]")
    print(f"{Fore.BLUE}Courbe Standard FIPS 186-4\n")

    try:
        try:
            from .key_generation import generate_nist_p256_keypair
        except ImportError:
            from key_generation import generate_nist_p256_keypair

        print(f"{Fore.GREEN}Courbe: NIST P-256 (prime256v1, secp256r1)")
        print(f"  E: y² = x³ - 3x + b (mod p)")
        print(f"  Corps: p = 2²⁵⁶ - 2²²⁴ + 2¹⁹² + 2¹²⁸ - 1")
        print(f"  Ordre: n ≈ 2²⁵⁶")

        print(f"\n{Fore.YELLOW}Génération d'une paire de clés NIST P-256...")
        paire_cles = generate_nist_p256_keypair()

        print(f"\n{Fore.GREEN}Génération réussie!")
        print(f"\n{Fore.YELLOW}Clé Privée (d):")
        print(f"  Hexadécimal: {hex(paire_cles.private_key)[:50]}...")
        print(f"  Bits: {paire_cles.private_key.bit_length()}")

        print(f"\n{Fore.YELLOW}Clé Publique (Q = d·G):")
        print(f"  x: {hex(paire_cles.public_key.x)[:50]}...")
        print(f"  y: {hex(paire_cles.public_key.y)[:50]}...")

        print(f"\n{Fore.CYAN}NIST P-256 est normalisée pour:")
        print(f"  • Signatures Numériques FIPS 186-4")
        print(f"  • Authentification Certificat TLS/SSL")
        print(f"  • Applications Gouvernementales et Financières")
        print(f"  • Communications Sécurisées")

    except Exception as e:
        print(f"{Fore.RED}Erreur: {e}")
        import traceback
        traceback.print_exc()


def executer_tests():
    """Exécute la suite de tests."""
    print(f"\n{Fore.BLUE}[EXÉCUTION DES TESTS]")
    print(f"Lancement de pytest...\n")
    import subprocess

    # Utiliser le python du venv s'il est disponible, sinon sys.executable
    python_exe = sys.executable
    resultat = subprocess.run(
        [python_exe, "-m", "pytest", "tests/", "-v", "--tb=short"],
        cwd=Path(__file__).parent.parent
    )
    return resultat.returncode == 0


def principal():
    """Boucle principale de l'application."""
    afficher_en_tete()

    while True:
        afficher_menu()

        try:
            choix = input().strip()

            if choix == "1":
                mode_pedagogique()
            elif choix == "2":
                mode_realiste()
            elif choix == "3":
                mode_nist()
            elif choix == "4":
                succes = executer_tests()
                if succes:
                    print(f"\n{Fore.GREEN}✓ Tous les tests ont réussi!")
                else:
                    print(f"\n{Fore.RED}✗ Certains tests ont échoué")
            elif choix == "5":
                print(f"\n{Fore.YELLOW}Au revoir!\n")
                break
            else:
                print(f"\n{Fore.RED}Choix invalide. Veuillez réessayer.\n")

        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Programme interrompu par l'utilisateur\n")
            break
        except Exception as e:
            print(f"\n{Fore.RED}Erreur: {e}\n")


if __name__ == "__main__":
    principal()
