# ============================================================
# Démo 4 — Utiliser des Enum dans ses classes
# ============================================================
# Enum comme type d'attribut, tri, comptage et match/case.

from dataclasses import dataclass, field
from enum import Enum, IntEnum, auto


class Transport(Enum):
  STANDARD = auto()
  EXPRESS = auto()
  RELAIS = auto()


class Urgence(IntEnum):
  FAIBLE = 1
  MOYENNE = 2
  FORTE = 3


class EtatColis(Enum):
  PREPARE = "En préparation"
  EXPEDIE = "Expédié"
  LIVRE = "Livré"
  PERDU = "Perdu"


@dataclass
class Colis:
  numero: int
  destination: str
  transport: Transport
  urgence: Urgence = Urgence.MOYENNE
  etat: EtatColis = EtatColis.PREPARE
  historique: list[EtatColis] = field(default_factory=list)

  def __post_init__(self) -> None:
    self.historique.append(self.etat)

  def changer_etat(self, nouvel_etat: EtatColis) -> None:
    if self.etat in (EtatColis.LIVRE, EtatColis.PERDU):
      raise ValueError(f"Colis #{self.numero} déjà clôturé ({self.etat.value})")
    self.etat = nouvel_etat
    self.historique.append(nouvel_etat)

  # --- match/case sur un Enum ---
  def delai_jours(self) -> int:
    match self.transport:
      case Transport.EXPRESS:
        return 1
      case Transport.STANDARD:
        return 3
      case Transport.RELAIS:
        return 4


colis = [
  Colis(1, "Namur", Transport.STANDARD, Urgence.FAIBLE),
  Colis(2, "Liège", Transport.EXPRESS, Urgence.FORTE),
  Colis(3, "Mons", Transport.RELAIS),
  Colis(4, "Gand", Transport.EXPRESS, Urgence.FORTE),
]

colis[0].changer_etat(EtatColis.EXPEDIE)
colis[0].changer_etat(EtatColis.LIVRE)
colis[1].changer_etat(EtatColis.EXPEDIE)

# --- 1. Une exception levée par le modèle ---
try:
  colis[0].changer_etat(EtatColis.EXPEDIE)
except ValueError as e:
  print("1. ERREUR :", e)


# --- 2. Trier par Enum (IntEnum → ordre naturel) ---
print("2. Du plus urgent au moins urgent :")
for c in sorted(colis, key=lambda c: c.urgence, reverse=True):
  print(f"   #{c.numero} {c.urgence.name:<8} {c.transport.name:<8} "
        f"{c.delai_jours()} j — {c.destination} — {c.etat.value}")

# Avec un Enum simple (non ordonné), on trie sur .value :
print("2. Trié par transport :", [f"#{c.numero}" for c in sorted(colis, key=lambda c: c.transport.value)])


# --- 3. Compter par état, y compris les états à 0 ---
# On part de TOUS les membres de l'Enum, pas seulement de ceux rencontrés.
compteur = {etat: 0 for etat in EtatColis}
for c in colis:
  compteur[c.etat] += 1

print("3. Répartition :", " | ".join(f"{etat.value}: {n}" for etat, n in compteur.items()))


# --- 4. Historique : une liste de membres ---
print("4. Historique #1 :", " → ".join(etat.value for etat in colis[0].historique))


# --- 5. Filtrer avec un Enum ---
express = [c.numero for c in colis if c.transport is Transport.EXPRESS]
print("5. Colis express :", express)
