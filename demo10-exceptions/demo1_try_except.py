# ============================================================
# Démo 1 — try / except / else / finally
# ============================================================
# Une exception est un objet levé quand quelque chose se passe mal.
# Si personne ne l'attrape, le programme s'arrête avec un traceback.

# --- 1. Sans gestion : le programme planterait ---
# print(10 / 0)            # ZeroDivisionError
# int("abc")               # ValueError
# [1, 2, 3][10]            # IndexError
# {"a": 1}["b"]            # KeyError


# --- 2. try / except de base ---
try:
  resultat = 10 / 0
except ZeroDivisionError:
  print("1. Division par zéro impossible")


# --- 3. Récupérer l'objet exception avec "as" ---
try:
  int("abc")
except ValueError as e:
  print(f"2. Type : {type(e).__name__} | Message : {e}")


# --- 4. Plusieurs except : le premier qui correspond gagne ---
def lire_note(saisies: list[str], index: int) -> float:
  try:
    note = float(saisies[index])
    return 20 / note
  except IndexError:
    print(f"   Pas de saisie à l'index {index}")
  except ValueError:
    print(f"   '{saisies[index]}' n'est pas un nombre")
  except ZeroDivisionError:
    print("   La note ne peut pas valoir 0")
  return 0.0

print("3. Plusieurs except :")
saisies = ["10", "abc", "0"]
for i in range(4):
  lire_note(saisies, i)


# --- 5. Un même except pour plusieurs types (tuple) ---
for valeur in ["12", "x", None]:
  try:
    print(f"4. {valeur} → {int(valeur)}")
  except (ValueError, TypeError) as e:
    print(f"4. {valeur!r} → conversion impossible ({type(e).__name__})")


# --- 6. else et finally ---
# else    : exécuté seulement si AUCUNE exception n'a été levée
# finally : exécuté TOUJOURS (succès, erreur, return...) → nettoyage
def diviser(a: float, b: float) -> None:
  try:
    resultat = a / b
  except ZeroDivisionError:
    print(f"5. {a} / {b} → ERREUR")
  else:
    print(f"5. {a} / {b} → {resultat}")
  finally:
    print("   (fin du calcul)")

diviser(10, 2)
diviser(10, 0)


# --- 7. La hiérarchie des exceptions : l'ordre des except compte ---
# BaseException
#  └── Exception
#       ├── ArithmeticError
#       │    └── ZeroDivisionError
#       ├── LookupError
#       │    ├── IndexError
#       │    └── KeyError
#       └── ValueError
print("6. ZeroDivisionError hérite d'ArithmeticError :", issubclass(ZeroDivisionError, ArithmeticError))

try:
  {"a": 1}["b"]
except LookupError as e:          # attrape IndexError ET KeyError
  print(f"6. Attrapée via le parent LookupError : {type(e).__name__}")

# Toujours du plus spécifique au plus général :
try:
  [1][5]
except IndexError:
  print("7. IndexError (spécifique) attrapée en premier")
except Exception:
  print("7. Jamais atteint ici")

# À éviter : "except:" tout seul ou "except Exception: pass"
# → on masque les bugs sans savoir ce qui s'est passé.
