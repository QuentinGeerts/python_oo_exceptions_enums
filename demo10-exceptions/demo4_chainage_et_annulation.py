# ============================================================
# Démo 4 — Chaînage (raise ... from) et opération "tout ou rien"
# ============================================================


# --- 1. Traduire une exception technique en exception métier ---
class ConfigError(Exception):
  pass


class CleManquanteError(ConfigError):
  def __init__(self, cle: str) -> None:
    self.cle = cle
    super().__init__(f"Paramètre '{cle}' absent de la configuration")


class Configuration:
  def __init__(self, valeurs: dict[str, str]) -> None:
    self.__valeurs = valeurs

  def lire(self, cle: str) -> str:
    try:
      return self.__valeurs[cle]          # peut lever KeyError (technique)
    except KeyError as e:
      raise CleManquanteError(cle) from e  # → erreur métier, cause conservée


config = Configuration({"hote": "localhost", "port": "5432"})

try:
  config.lire("mot_de_passe")
except CleManquanteError as e:
  print(f"1. {e}")
  print(f"   e.__cause__ = {e.__cause__!r}")
  print(f"   type de la cause : {type(e.__cause__).__name__}")


# --- 2. Sans "from" : Python garde quand même la trace dans __context__ ---
#        "from None" : on coupe volontairement le lien
def sans_from() -> None:
  try:
    {}["x"]
  except KeyError:
    raise ConfigError("Erreur sans from")

def avec_from_none() -> None:
  try:
    {}["x"]
  except KeyError:
    raise ConfigError("Erreur avec from None") from None

for fonction in (sans_from, avec_from_none):
  try:
    fonction()
  except ConfigError as e:
    print(f"2. {e}")
    print(f"   __cause__={e.__cause__!r} | __context__={e.__context__!r} | "
          f"__suppress_context__={e.__suppress_context__}")
# from None ne supprime pas __context__ : il met __suppress_context__ à True,
# ce qui empêche l'affichage de l'ancienne exception dans le traceback.

# Dans le traceback (si non attrapée) :
#   from e    → "The above exception was the direct cause of the following exception"
#   sans from → "During handling of the above exception, another exception occurred"
#   from None → seule la nouvelle exception est affichée


# --- 3. Tout ou rien : annuler l'étape 1 si l'étape 2 échoue, puis relancer ---
class ReservationError(Exception):
  pass


class PlusDePlaceError(ReservationError):
  def __init__(self, element: str) -> None:
    self.element = element
    super().__init__(f"Plus de place disponible : {element}")


class Agence:
  def __init__(self, places_vol: int, chambres: int) -> None:
    self.places_vol = places_vol
    self.chambres = chambres

  def reserver_vol(self) -> None:
    if self.places_vol == 0:
      raise PlusDePlaceError("vol")
    self.places_vol -= 1

  def annuler_vol(self) -> None:
    self.places_vol += 1

  def reserver_hotel(self) -> None:
    if self.chambres == 0:
      raise PlusDePlaceError("hôtel")
    self.chambres -= 1

  def reserver_sejour(self) -> None:
    self.reserver_vol()            # étape 1
    try:
      self.reserver_hotel()        # étape 2
    except ReservationError:
      self.annuler_vol()           # on défait l'étape 1...
      raise                        # ...et on prévient l'appelant


agence = Agence(places_vol=5, chambres=1)

for client in ["Alice", "Bob"]:
  try:
    agence.reserver_sejour()
  except ReservationError as e:
    print(f"3. {client} → ERREUR : {e}")
  else:
    print(f"3. {client} → séjour réservé")
  finally:
    print(f"   état : {agence.places_vol} places vol | {agence.chambres} chambres")

# Bob a échoué sur l'hôtel : sa place de vol a bien été rendue (4 et pas 3).
