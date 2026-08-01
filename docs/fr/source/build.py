#!/usr/bin/env python3
"""Reproducible page-composition build for the French ED-POMDP editorial split.

Authoritative inherited source:
  base/ED_POMDP_En_Clair_FR_v1.8.pdf

The build intentionally preserves the inherited guide pages. It adds generated
front matter, patches only the version/introduction block of inherited page 1,
keeps inherited pages 2-30 unchanged, and exports inherited pages 31-37 into an
advanced companion without modifying their scientific content.
"""
from __future__ import annotations

import hashlib
import io
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "base" / "ED_POMDP_En_Clair_FR_v1.8.pdf"
OUT = ROOT / "output"
MAIN_OUT = OUT / "ED_POMDP_En_Clair_FR_v1.9.pdf"
COMP_OUT = OUT / "ED_POMDP_Belief_to_Action_Companion_FR_v1.0.pdf"

EXPECTED_BASE_SHA256 = "7af6e07623b66412362c1a1c4c816b7e950d948fe36db11e4729715761162899"

PAGE_W, PAGE_H = A4

pdfmetrics.registerFont(TTFont("EDSerif", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"))
pdfmetrics.registerFont(TTFont("EDSerifBold", "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"))
BLUE = colors.HexColor("#214D6B")
PALE_GOLD = colors.HexColor("#F7F1DE")
PALE_GREEN = colors.HexColor("#EDF5EA")
PALE_BLUE = colors.HexColor("#EAF2F7")
GREY = colors.HexColor("#6F6F6F")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def draw_header(c: Canvas, text: str) -> None:
    c.setFillColor(GREY)
    c.setFont("EDSerif", 8.5)
    c.drawRightString(PAGE_W - 28 * mm, PAGE_H - 10 * mm, text)


def draw_wrapped(c: Canvas, text: str, x: float, y_top: float, width: float,
                 font: str = "EDSerif", size: float = 10.5,
                 leading: float | None = None, color=colors.black,
                 bold: bool = False) -> float:
    leading = leading or size * 1.15
    style = ParagraphStyle(
        name="body",
        fontName="EDSerifBold" if bold else font,
        fontSize=size,
        leading=leading,
        textColor=color,
        alignment=TA_LEFT,
        spaceAfter=0,
    )
    p = Paragraph(text, style)
    _, h = p.wrap(width, PAGE_H)
    p.drawOn(c, x, y_top - h)
    return h


def rounded_box(c: Canvas, x: float, y: float, w: float, h: float,
                fill, title: str, body: str) -> None:
    c.setFillColor(fill)
    c.roundRect(x, y, w, h, 4 * mm, fill=1, stroke=0)
    c.setFillColor(BLUE)
    c.setFont("EDSerifBold", 9.3)
    c.drawString(x + 5 * mm, y + h - 7 * mm, title)
    draw_wrapped(c, body, x + 5 * mm, y + h - 10.5 * mm, w - 10 * mm,
                 size=6.7, leading=7.4)


def make_main_frontmatter() -> bytes:
    buf = io.BytesIO()
    c = Canvas(buf, pagesize=A4, pageCompression=1)
    draw_header(c, "ED-POMDP en clair - Guide de lecture français")

    c.setFillColor(BLUE)
    c.setFont("EDSerifBold", 18)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 43 * mm,
                 "Mode d’emploi et glossaire de première lecture")

    x = 25 * mm
    w = PAGE_W - 50 * mm
    y = PAGE_H - 93 * mm
    h = 30 * mm
    c.setFillColor(PALE_GOLD)
    c.roundRect(x, y, w, h, 5 * mm, fill=1, stroke=0)
    intro = (
        "Le guide suit une progression en spirale : la première lecture donne le problème, "
        "les paris et les résultats ; les annexes A à F reviennent ensuite sur les formules, "
        "les calculs et leurs limites. Les termes ci-dessous sont des repères, pas un cours "
        "préalable. Le document companion avancé traite séparément l’estimation d’état, la "
        "recherche opérationnelle et l’apprentissage de politiques."
    )
    draw_wrapped(c, intro, x + 5 * mm, y + h - 6 * mm, w - 10 * mm,
                 size=9.6, leading=10.3)

    left = 25 * mm
    gap = 9 * mm
    col_w = (PAGE_W - 50 * mm - gap) / 2
    box_h = 17 * mm
    start_y = 190 * mm
    left_items = [
        ("État latent", "État réel supposé exister mais non observé directement."),
        ("Croyance, prior, posterior", "Distribution de probabilités ; avant observation = prior, après observation = posterior."),
        ("Calibration", "Accord entre les probabilités annoncées et les fréquences réellement observées."),
        ("Score de Brier", "Erreur quadratique d’une prévision probabiliste binaire : (p-y)^2."),
        ("ECE et intervalle (bin)", "Écart moyen de calibration apres regroupement des probabilités proches en intervalles."),
        ("Seed", "Numéro qui permet de reproduire exactement un même scénario aléatoire."),
        ("Cellule et appariement", "Groupe expérimental ; les politiques sont comparées sur le même scénario, paire par paire."),
        ("Baseline", "Méthode de comparaison plus simple ou différente."),
        ("Endpoint", "Mesure finale utilisée pour juger un résultat."),
    ]
    right_items = [
        ("Hypothèse nulle et p-value", "La p-value mesure la rareté du résultat si l’hypothèse d’équivalence était vraie."),
        ("Bootstrap apparie", "Rééchantillonnage avec remise des mêmes paires pour mesurer la variabilité de l'effet."),
        ("Permutation appariee", "Échange aléatoire des étiquettes dans chaque paire pour construire une distribution nulle."),
        ("Holm", "Correction progressive qui protège une famille de nombreux tests contre les faux positifs."),
        ("Identifiabilite", "Possibilité de distinguer les causes cachées à partir des observations disponibles."),
        ("Modèle mal spécifié", "Modèle dont les probabilités supposées ne correspondent pas au monde qui produit les donnees."),
        ("Cote probabiliste (odds)", "Rapport p/(1-p), utile pour exprimer une mise à jour bayésienne."),
        ("Rapport de vraisemblance", "Pouvoir d’une observation à favoriser une hypothèse plutôt qu’une autre."),
        ("VOI / EVI", "Valeur attendue de l’information : gain décisionnel attendu d’une preuve, avant son résultat."),
    ]
    for idx, item in enumerate(left_items):
        yb = start_y - idx * (box_h + 3.5 * mm)
        rounded_box(c, left, yb, col_w, box_h,
                    PALE_GREEN if idx % 3 in (0, 1) else PALE_BLUE,
                    item[0], item[1])
    for idx, item in enumerate(right_items):
        yb = start_y - idx * (box_h + 3.5 * mm)
        rounded_box(c, left + col_w + gap, yb, col_w, box_h,
                    PALE_GREEN if idx % 3 in (0, 1) else PALE_BLUE,
                    item[0], item[1])

    c.setFillColor(GREY)
    c.setFont("EDSerif", 6.8)
    c.drawCentredString(PAGE_W / 2, 21 * mm,
                 "Les noms de fichiers, clés de configuration et identifiants du dépôt restent en anglais")
    c.drawCentredString(PAGE_W / 2, 17.5 * mm,
                 "lorsqu’ils sont des artefacts techniques.")
    c.drawCentredString(PAGE_W / 2, 10.5 * mm,
                       "Page liminaire non numérotée - Guide principal v1.9")
    c.showPage()
    c.save()
    return buf.getvalue()


def make_main_page1_overlay() -> bytes:
    """Patch only the inherited cover's version line and introductory block."""
    buf = io.BytesIO()
    c = Canvas(buf, pagesize=A4, pageCompression=1)

    c.setFillColor(colors.white)
    c.rect(105, 594, PAGE_W - 210, 28, fill=1, stroke=0)
    c.setFillColor(colors.black)
    c.setFont("EDSerif", 8.8)
    c.drawCentredString(PAGE_W / 2, 603,
                       "Guide pédagogique français - Document compagnon - Version 1.9")

    c.setFillColor(colors.white)
    c.setStrokeColor(colors.white)
    c.rect(43, 425, PAGE_W - 86, 165, fill=1, stroke=0)
    c.setFillColor(colors.HexColor("#FBF6E8"))
    c.setStrokeColor(colors.HexColor("#C79A24"))
    c.rect(47, 458, PAGE_W - 94, 132, fill=1, stroke=1)
    c.setFillColor(colors.black)
    c.setFont("EDSerifBold", 9.3)
    c.drawString(54, 570, "À lire avant le papier scientifique")
    body = (
        "Le rapport Step 2 Benchmark Close-Out est une conclusion scientifique et un document d’audit. "
        "Le présent guide explique le problème, la genèse de l’approche, l'intuition, les deux paris "
        "scientifiques, leur tentative de falsification et le sens des résultats. Les annexes A à F "
        "approfondissent la contestation du modèle, sa généalogie, la mesurabilité des variables, les "
        "données synthétiques, le fonctionnement du code et la mécanique statistique utilisée pour juger "
        "un résultat. Certaines notions sont d’abord introduites par leur rôle, puis expliquées et calculées "
        "dans les annexes : une seconde lecture est volontairement utile. L’ancienne Annexe G est publiée "
        "séparément comme document companion avancé. Le guide ne remplace pas les artefacts formels et ne "
        "modifie aucun claim."
    )
    draw_wrapped(c, body, 54, 553, PAGE_W - 108, size=8.35, leading=9.5)

    c.showPage()
    c.save()
    return buf.getvalue()


def make_companion_frontmatter() -> bytes:
    buf = io.BytesIO()
    c = Canvas(buf, pagesize=A4, pageCompression=1)
    draw_header(c, "ED-POMDP - Document companion avancé")
    c.setFillColor(BLUE)
    c.setFont("EDSerifBold", 25)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 70 * mm, "ED-POMDP")
    c.setFont("EDSerifBold", 19)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 87 * mm, "DE LA CROYANCE À L’ACTION")
    c.setFillColor(colors.black)
    c.setFont("EDSerif", 12)
    c.drawCentredString(PAGE_W / 2, PAGE_H - 102 * mm,
                       "Estimation d’état, recherche opérationnelle et apprentissage de politiques")

    c.setFillColor(PALE_GOLD)
    c.roundRect(35 * mm, PAGE_H - 166 * mm, PAGE_W - 70 * mm, 35 * mm,
                5 * mm, fill=1, stroke=0)
    intro = (
        "Document autonome de niveau avancé. Il reproduit sans modification scientifique l’ancienne "
        "Annexe G du guide ED-POMDP en clair v1.8. Les deux pages liminaires ajoutent seulement le contrat "
        "de lecture, les prérequis et des repères terminologiques."
    )
    draw_wrapped(c, intro, 42 * mm, PAGE_H - 140 * mm, PAGE_W - 84 * mm,
                 size=10.5, leading=11.8)

    c.setFillColor(BLUE)
    c.setFont("EDSerifBold", 13)
    c.drawString(35 * mm, PAGE_H - 200 * mm, "Prérequis conseillés")
    prereq = (
        "Probabilités conditionnelles, espérance, mise à jour bayésienne, optimisation, "
        "notions de machine learning et lecture générale d'un MDP/POMDP."
    )
    draw_wrapped(c, prereq, 35 * mm, PAGE_H - 207 * mm, PAGE_W - 70 * mm,
                 size=10.2, leading=11.5)

    c.setFillColor(GREY)
    c.setFont("EDSerif", 9)
    c.drawCentredString(PAGE_W / 2, 18 * mm,
                       "Companion français uniquement - Version 1.0")
    c.showPage()

    draw_header(c, "ED-POMDP - Document companion avancé")
    c.setFillColor(BLUE)
    c.setFont("EDSerifBold", 20)
    c.drawString(25 * mm, PAGE_H - 35 * mm, "Repères terminologiques du companion")
    note = (
        "Les familles d'estimateurs citées sont un panorama de choix possibles, pas un cours complet. "
        "Le texte conserve certains noms anglais lorsqu'ils correspondent aux termes canoniques de la littérature."
    )
    draw_wrapped(c, note, 25 * mm, PAGE_H - 48 * mm, PAGE_W - 50 * mm,
                 size=10.5, leading=11.8)

    terms = [
        ("MAP", "Maximum a posteriori : etat le plus probable après observation."),
        ("Marginalisation", "Sommer ou intégrer les autres variables pour ne garder que la distribution d'intérêt."),
        ("HMM", "Modèle de Markov caché : etat latent évolutif observé indirectement."),
        ("Filtre de Kalman", "Estimateur récursif pour un modèle lineaire gaussien."),
        ("Filtre particulaire / SMC", "Approximation d'une distribution par un ensemble de particules ponderees."),
        ("Inference amortie", "Modele appris qui produit rapidement une approximation de la croyance."),
        ("Ensemble conforme", "Ensemble de prédictions muni d'une garantie de couverture sous hypothèses données."),
        ("Bandit contextuel", "Choix répété d'une action à partir d'un contexte, sans modèle d'etat complet."),
        ("RL model-based", "Apprentissage ou planification avec un modèle explicite des transitions."),
        ("RL model-free", "Apprentissage direct d’une valeur ou politique sans modèle explicite complet."),
        ("Offline RL", "Apprentissage d'une politique à partir de données historiques, sans exploration en ligne."),
        ("Contrainte dure", "Condition qui ne peut pas être compensée par un gain sur un autre objectif."),
    ]
    y = PAGE_H - 95 * mm
    for idx, (term, definition) in enumerate(terms):
        col = idx % 2
        row = idx // 2
        bx = 25 * mm + col * (79 * mm + 8 * mm)
        by = y - row * 31 * mm
        rounded_box(c, bx, by, 79 * mm, 25 * mm,
                    PALE_GREEN if row % 2 == 0 else PALE_BLUE,
                    term, definition)
    c.setFillColor(GREY)
    c.setFont("EDSerif", 8.5)
    c.drawCentredString(PAGE_W / 2, 14 * mm,
                       "Les sept pages suivantes sont reprises à l’identique de l'Annexe G de la v1.8.")
    c.showPage()
    c.save()
    return buf.getvalue()


def merge_overlay(page, overlay_pdf: bytes):
    overlay = PdfReader(io.BytesIO(overlay_pdf)).pages[0]
    page.merge_page(overlay)
    return page


def build() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    actual = sha256(BASE)
    if actual != EXPECTED_BASE_SHA256:
        raise SystemExit(
            f"Base hash mismatch: expected {EXPECTED_BASE_SHA256}, got {actual}"
        )

    base = PdfReader(str(BASE))
    if len(base.pages) != 37:
        raise SystemExit(f"Expected 37 base pages, got {len(base.pages)}")

    main = PdfWriter()
    main.add_page(PdfReader(io.BytesIO(make_main_frontmatter())).pages[0])
    patched_cover = base.pages[0]
    merge_overlay(patched_cover, make_main_page1_overlay())
    main.add_page(patched_cover)
    for idx in range(1, 30):
        main.add_page(base.pages[idx])
    main.add_metadata({
        "/Title": "ED-POMDP en clair - Guide de lecture français v1.9",
        "/Author": "Guillaume Harbonnier",
        "/Subject": "Editorial split preserving the v1.8 scientific content",
    })
    with MAIN_OUT.open("wb") as f:
        main.write(f)

    comp = PdfWriter()
    front = PdfReader(io.BytesIO(make_companion_frontmatter()))
    comp.add_page(front.pages[0])
    comp.add_page(front.pages[1])
    for idx in range(30, 37):
        comp.add_page(base.pages[idx])
    comp.add_metadata({
        "/Title": "ED-POMDP - De la croyance a l'action - Companion FR v1.0",
        "/Author": "Guillaume Harbonnier",
        "/Subject": "Autonomous export of former Annex G",
    })
    with COMP_OUT.open("wb") as f:
        comp.write(f)

    print(f"main={MAIN_OUT} sha256={sha256(MAIN_OUT)}")
    print(f"companion={COMP_OUT} sha256={sha256(COMP_OUT)}")


if __name__ == "__main__":
    build()
