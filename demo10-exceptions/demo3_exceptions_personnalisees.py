# ============================================================
# Démo 3 — Exceptions personnalisées (exceptions métier)
# ============================================================
# Une exception personnalisée = une classe qui hérite d'Exception.
# Avantages :
#   - un nom qui parle métier (LivreIndisponibleError > ValueError)
#   - des attributs exploitables par l'appelant
#   - une classe de base commune pour tout attraper d'un coup
#
# Hiérarchie de la démo :
#
# BibliothequeError
# ├── LivreIntrouvableError      → isbn
# ├── LivreIndisponibleError     → titre, emprunteur
# └── QuotaDepasseError          → membre, quota, en_cours, excedent (propriété)


# --- 1. La classe de base : vide, elle sert à regrouper ---
class BibliothequeError(Exception):
  """Classe mère de toutes les erreurs de la bibliothèque."""


# --- 2. Exception avec attribut : le message est construit DANS l'exception ---
class LivreIntrouvableError(BibliothequeError):
  def __init__(self, isbn: str) -> None:
    self.isbn = isbn
    super().__init__(f"Aucun livre avec l'ISBN {isbn}")


class LivreIndisponibleError(BibliothequeError):
  def __init__(self, titre: str, emprunteur: str) -> None:
    self.titre = titre
    self.emprunteur = emprunteur
    super().__init__(f"'{titre}' est déjà emprunté par {emprunteur}")


# --- 3. Exception avec une propriété calculée ---
class QuotaDepasseError(BibliothequeError):
  def __init__(self, membre: str, quota: int, en_cours: int) -> None:
    self.membre = membre
    self.quota = quota
    self.en_cours = en_cours
    super().__init__(f"{membre} a atteint son quota ({en_cours}/{quota} livres)")

  @property
  def excedent(self) -> int:
    return self.en_cours - self.quota + 1


# --- Les modèles lèvent, ils n'affichent rien ---
class Livre:
  def __init__(self, isbn: str, titre: str) -> None:
    self.isbn = isbn
    self.titre = titre
    self.emprunteur: str | None = None


class Bibliotheque:
  QUOTA = 2

  def __init__(self) -> None:
    self.__livres: dict[str, Livre] = {}
    self.__emprunts: dict[str, int] = {}

  def ajouter(self, livre: Livre) -> None:
    self.__livres[livre.isbn] = livre

  def emprunter(self, isbn: str, membre: str) -> Livre:
    if isbn not in self.__livres:
      raise LivreIntrouvableError(isbn)

    livre = self.__livres[isbn]
    if livre.emprunteur is not None:
      raise LivreIndisponibleError(livre.titre, livre.emprunteur)

    en_cours = self.__emprunts.get(membre, 0)
    if en_cours >= self.QUOTA:
      raise QuotaDepasseError(membre, self.QUOTA, en_cours)

    livre.emprunteur = membre
    self.__emprunts[membre] = en_cours + 1
    return livre


# --- Programme principal : c'est ICI qu'on décide quoi afficher ---
biblio = Bibliotheque()
biblio.ajouter(Livre("111", "Dune"))
biblio.ajouter(Livre("222", "Fondation"))
biblio.ajouter(Livre("333", "Hypérion"))

demandes = [
  ("111", "Alice"),
  ("111", "Bob"),       # déjà emprunté
  ("222", "Alice"),
  ("333", "Alice"),     # quota atteint
  ("999", "Bob"),       # ISBN inconnu
]

for isbn, membre in demandes:
  try:
    livre = biblio.emprunter(isbn, membre)
  except LivreIndisponibleError as e:
    # On utilise les attributs de l'exception
    print(f"{membre:<6} {isbn} → REFUS : {e} (demandez à {e.emprunteur})")
  except QuotaDepasseError as e:
    print(f"{membre:<6} {isbn} → REFUS : {e} — rendez {e.excedent} livre(s)")
  except BibliothequeError as e:
    # Attrape toutes les AUTRES erreurs métier (ici LivreIntrouvableError)
    print(f"{membre:<6} {isbn} → ERREUR : {e}")
  else:
    print(f"{membre:<6} {isbn} → OK : '{livre.titre}'")


# --- Vérifications sur la hiérarchie ---
erreur = QuotaDepasseError("Alice", 2, 2)
print()
print("isinstance(erreur, QuotaDepasseError) :", isinstance(erreur, QuotaDepasseError))
print("isinstance(erreur, BibliothequeError) :", isinstance(erreur, BibliothequeError))
print("isinstance(erreur, Exception)         :", isinstance(erreur, Exception))
print("str(erreur)                           :", str(erreur))
