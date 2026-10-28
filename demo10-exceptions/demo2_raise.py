# ============================================================
# Démo 2 — Lever une exception avec raise
# ============================================================
# Dans un modèle, on ne fait pas de print("Erreur") ni de return False :
# on LÈVE une exception. C'est l'appelant qui décide quoi afficher.


class Thermostat:
  MIN = 5
  MAX = 30

  def __init__(self, piece: str) -> None:
    self.piece = piece
    self.__temperature = 20.0

  @property
  def temperature(self) -> float:
    return self.__temperature

  def regler(self, valeur: float) -> None:
    # Mauvais type → TypeError
    if not isinstance(valeur, (int, float)):
      raise TypeError(f"Température attendue en nombre, reçu {type(valeur).__name__}")
    # Bon type mais valeur hors limites → ValueError
    if not self.MIN <= valeur <= self.MAX:
      raise ValueError(f"{valeur} °C hors limites ({self.MIN}–{self.MAX} °C)")
    self.__temperature = float(valeur)


# --- 1. L'appelant gère les erreurs ---
salon = Thermostat("Salon")

for valeur in [22, 45, "chaud"]:
  try:
    salon.regler(valeur)
  except (TypeError, ValueError) as e:
    print(f"1. regler({valeur!r}) → ERREUR : {e}")
  else:
    print(f"1. regler({valeur!r}) → OK, {salon.temperature} °C")


# --- 2. Relancer une exception avec "raise" seul ---
# On attrape pour faire quelque chose (log, nettoyage...),
# puis on laisse l'exception continuer sa route vers l'appelant.
def regler_avec_log(thermostat: Thermostat, valeur: float) -> None:
  try:
    thermostat.regler(valeur)
  except ValueError:
    print(f"2. [LOG] Réglage refusé sur {thermostat.piece}")
    raise  # relance la MÊME exception, traceback intact

try:
  regler_avec_log(salon, 99)
except ValueError as e:
  print(f"2. main a reçu : {e}")


# --- 3. L'exception remonte la pile d'appels ---
# Si une fonction n'attrape pas l'exception, elle remonte à l'appelant,
# puis à l'appelant de l'appelant... jusqu'à un try/except (ou le crash).
def niveau_3() -> None:
  raise RuntimeError("Problème au niveau 3")

def niveau_2() -> None:
  niveau_3()           # pas de try ici

def niveau_1() -> None:
  try:
    niveau_2()
  except RuntimeError as e:
    print(f"3. Attrapée au niveau 1 : {e}")

niveau_1()


# --- 4. finally même avec un return ---
def lire_config(chemin: str) -> str:
  print(f"4. Ouverture de {chemin}")
  try:
    if not chemin.endswith(".ini"):
      raise ValueError("Format non supporté")
    return "config chargée"
  finally:
    print("4. Fermeture (toujours exécutée)")

print("4.", lire_config("app.ini"))
try:
  lire_config("app.txt")
except ValueError as e:
  print(f"4. ERREUR : {e}")
