# ============================================================
# Démo 1 — Les bases d'Enum
# ============================================================
# Une énumération = un ensemble FINI de constantes nommées.
# Plutôt que des "chaînes magiques" ("lundi", "LUNDI", "Lundi"...),
# on a un type avec des valeurs connues et vérifiées.

from enum import Enum


# --- 0. Le problème sans Enum ---
def est_weekend_sans_enum(jour: str) -> bool:
  return jour in ("samedi", "dimanche")

print("0. Sans Enum :", est_weekend_sans_enum("Samedi"))  # False → faute de casse invisible


# --- 1. Déclaration ---
class Jour(Enum):
  LUNDI = 1
  MARDI = 2
  MERCREDI = 3
  JEUDI = 4
  VENDREDI = 5
  SAMEDI = 6
  DIMANCHE = 7


# --- 2. Un membre a un nom (name) et une valeur (value) ---
jour = Jour.SAMEDI
print("1.", jour)              # Jour.SAMEDI
print("1.", repr(jour))        # <Jour.SAMEDI: 6>
print("1. name  :", jour.name)   # 'SAMEDI'
print("1. value :", jour.value)  # 6
print("1. type  :", type(jour))  # <enum 'Jour'>


# --- 3. Retrouver un membre ---
print("2. Par valeur :", Jour(3))           # Jour.MERCREDI
print("2. Par nom    :", Jour["VENDREDI"])  # Jour.VENDREDI

# Valeur ou nom inexistant → exceptions différentes !
try:
  Jour(8)
except ValueError as e:
  print("2. Jour(8)        → ValueError :", e)

try:
  Jour["FERIE"]
except KeyError as e:
  print("2. Jour['FERIE']  → KeyError :", e)


# --- 4. Parcourir, compter, tester l'appartenance ---
print("3. Tous les jours :", ", ".join(j.name.capitalize() for j in Jour))
print("3. Nombre :", len(Jour))
print("3. Jour.LUNDI in Jour :", Jour.LUNDI in Jour)
print("3. Liste :", list(Jour)[:3], "...")


# --- 5. Comparaisons ---
# Chaque membre est un singleton : on compare avec "is" ou "=="
print("4. Jour(6) is Jour.SAMEDI :", Jour(6) is Jour.SAMEDI)  # True
print("4. Jour.SAMEDI == 6       :", Jour.SAMEDI == 6)        # False ! un Enum n'est pas un int
print("4. Jour.SAMEDI.value == 6 :", Jour.SAMEDI.value == 6)  # True

# Pas d'ordre avec Enum simple :
try:
  Jour.LUNDI < Jour.MARDI
except TypeError as e:
  print("4. LUNDI < MARDI → TypeError :", e)


# --- 6. Les membres sont des constantes ---
try:
  Jour.LUNDI = 10
except AttributeError as e:
  print("5. Modification interdite :", e)


# --- 7. Utilisation dans une fonction typée ---
def est_weekend(jour: Jour) -> bool:
  return jour in (Jour.SAMEDI, Jour.DIMANCHE)

print("6. Samedi weekend ?", est_weekend(Jour.SAMEDI))
print("6. Mardi weekend ? ", est_weekend(Jour.MARDI))


# --- 8. Les valeurs ne sont pas forcément des entiers ---
class Couleur(Enum):
  ROUGE = "#FF0000"
  VERT = "#00FF00"
  BLEU = "#0000FF"

print("7.", Couleur("#00FF00"), "→", Couleur.VERT.value)


# --- 9. Alias : deux noms pour la même valeur ---
class Reponse(Enum):
  OUI = 1
  YES = 1     # alias de OUI, pas un nouveau membre
  NON = 0

print("8. Reponse.YES is Reponse.OUI :", Reponse.YES is Reponse.OUI)
print("8. Membres parcourus :", [r.name for r in Reponse])  # les alias sont ignorés
