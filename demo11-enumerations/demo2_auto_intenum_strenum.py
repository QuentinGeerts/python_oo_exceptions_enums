# ============================================================
# Démo 2 — auto(), @unique, IntEnum, StrEnum
# ============================================================

from enum import Enum, IntEnum, StrEnum, auto, unique


# --- 1. auto() : quand la valeur n'a pas d'importance ---
class Moyen(Enum):
  VOITURE = auto()
  TRAIN = auto()
  VELO = auto()

print("1.", [(m.name, m.value) for m in Moyen])  # 1, 2, 3


# --- 2. @unique : interdit les alias (deux membres avec la même valeur) ---
try:
  @unique
  class Statut(Enum):
    ACTIF = 1
    INACTIF = 2
    ARCHIVE = 2   # erreur de copier-coller

except ValueError as e:
  print("2. @unique →", e)


# --- 3. IntEnum : les membres SONT des entiers ---
# → comparaison, tri, calculs possibles
class Taille(IntEnum):
  S = 1
  M = 2
  L = 3
  XL = 4

print("3. Taille.M == 2      :", Taille.M == 2)        # True (Enum simple : False)
print("3. Taille.S < Taille.L :", Taille.S < Taille.L)  # True
print("3. Taille.XL + 1      :", Taille.XL + 1)        # 5

commande = [Taille.L, Taille.S, Taille.XL, Taille.M]
print("3. Trié               :", [t.name for t in sorted(commande)])
print("3. Plus grande        :", max(commande).name)
print("3. Trié décroissant   :", [t.name for t in sorted(commande, reverse=True)])


# --- 4. StrEnum : les membres SONT des chaînes ---
class Format(StrEnum):
  JSON = auto()   # avec StrEnum, auto() donne le nom en minuscules
  CSV = auto()
  PDF = "pdf"

print("4.", [f.value for f in Format])             # ['json', 'csv', 'pdf']
print("4. Format.JSON == 'json' :", Format.JSON == "json")
print(f"4. rapport.{Format.CSV}")                  # s'utilise directement comme str
print("4. Format('pdf')         :", repr(Format("pdf")))


# --- 5. Quand choisir quoi ? ---
# Enum     → par défaut. Le type est strict, pas de mélange avec int/str.
# IntEnum  → on a besoin d'ordre / de tri (priorités, niveaux, tailles).
# StrEnum  → la valeur sert de texte (JSON, base de données, URL...).
