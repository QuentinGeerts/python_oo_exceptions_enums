# ============================================================
# Démo 3 — Méthodes, propriétés et classmethod dans un Enum
# ============================================================
# Un Enum est une classe : on peut lui ajouter du comportement.
# Le comportement lié à la valeur vit DANS l'énumération,
# plutôt que dispersé en if/elif partout dans le code.

from enum import Enum, IntEnum


# --- 1. Propriétés et méthodes : un feu tricolore ---
class Feu(Enum):
  VERT = "Vert"
  ORANGE = "Orange"
  ROUGE = "Rouge"

  # Propriété : une information calculée pour chaque membre
  @property
  def duree(self) -> int:
    match self:
      case Feu.VERT:
        return 30
      case Feu.ORANGE:
        return 4
      case Feu.ROUGE:
        return 25

  @property
  def peut_passer(self) -> bool:
    return self is Feu.VERT

  # Méthode : "self" est le membre courant
  def suivant(self) -> "Feu":
    return _SUIVANTS[self]


# Attention : un dict déclaré DANS la classe Enum deviendrait un membre !
# On le place donc à l'extérieur, après la définition.
_SUIVANTS = {
  Feu.VERT: Feu.ORANGE,
  Feu.ORANGE: Feu.ROUGE,
  Feu.ROUGE: Feu.VERT,
}

print("1. Cycle du feu :")
feu = Feu.ROUGE
for _ in range(4):
  print(f"   {feu.value:<7} {feu.duree:>2} s | passer : {feu.peut_passer}")
  feu = feu.suivant()


# --- 2. Méthode qui compare deux membres ---
class Etape(IntEnum):
  PANIER = 1
  PAIEMENT = 2
  LIVRAISON = 3
  TERMINEE = 4

  def peut_aller_a(self, autre: "Etape") -> bool:
    # On ne peut avancer que d'une étape à la fois (IntEnum → calcul possible)
    return autre == self + 1

  @property
  def est_finale(self) -> bool:
    return self is Etape.TERMINEE

print("2. PANIER → PAIEMENT   :", Etape.PANIER.peut_aller_a(Etape.PAIEMENT))
print("2. PANIER → LIVRAISON  :", Etape.PANIER.peut_aller_a(Etape.LIVRAISON))
print("2. TERMINEE finale ?    :", Etape.TERMINEE.est_finale)


# --- 3. classmethod : convertir une saisie utilisateur proprement ---
class NiveauLog(IntEnum):
  DEBUG = 10
  INFO = 20
  WARNING = 30
  ERROR = 40

  @property
  def icone(self) -> str:
    return {10: "🔍", 20: "ℹ️", 30: "⚠️", 40: "❌"}[self.value]

  @classmethod
  def depuis_saisie(cls, saisie: str | int) -> "NiveauLog":
    """Accepte un nom ("info", "ERROR") ou une valeur (20, 40)."""
    if isinstance(saisie, int):
      return cls(saisie)                 # ValueError si valeur inconnue
    try:
      return cls[saisie.strip().upper()]  # KeyError si nom inconnu
    except KeyError:
      # On uniformise : l'appelant n'a qu'une seule exception à gérer
      raise ValueError(f"Niveau inconnu : '{saisie}'") from None


print("3. Conversions :")
for saisie in ["info", " Warning ", 40, "critique", 99]:
  try:
    niveau = NiveauLog.depuis_saisie(saisie)
  except ValueError as e:
    print(f"   {saisie!r:<12} → ERREUR : {e}")
  else:
    print(f"   {saisie!r:<12} → {niveau.icone} {niveau.name}")


# --- 4. Filtrer avec l'ordre d'un IntEnum ---
seuil = NiveauLog.WARNING
messages = [
  (NiveauLog.DEBUG, "Connexion ouverte"),
  (NiveauLog.ERROR, "Disque plein"),
  (NiveauLog.INFO, "Utilisateur connecté"),
  (NiveauLog.WARNING, "Mémoire à 85 %"),
]
print(f"4. Messages >= {seuil.name} :")
for niveau, texte in messages:
  if niveau >= seuil:
    print(f"   {niveau.icone} [{niveau.name}] {texte}")
