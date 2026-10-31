"""Génère les wireframes SVG de la maquette du site essAI (ordinateur, téléphone, plan du site)."""
import os, re, sys
from xml.sax.saxutils import escape

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

INK = "#1B1F1D"; MID = "#8A918D"; LIGHT = "#E4E6E3"; PAPER = "#FFFFFF"; BG = "#F4F5F3"
GREEN = "#12271F"; CREAM = "#FBFAF6"; SAGE = "#8FB3A0"; AMBER = "#E0A84F"; NOTE = "#C2410C"
FONT = "font-family='Helvetica, Arial, sans-serif'"


class Svg:
    def __init__(self, w, h):
        self.w, self.h, self.e = w, h, []

    def add(self, s):
        self.e.append(s)

    def rect(self, x, y, w, h, fill=PAPER, stroke=MID, rx=6, dash=False, sw=1.5):
        d = " stroke-dasharray='6 4'" if dash else ""
        self.add(f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' fill='{fill}' stroke='{stroke}' stroke-width='{sw}'{d}/>")

    def text(self, x, y, s, size=14, weight="normal", fill=INK, anchor="start", italic=False):
        st = " font-style='italic'" if italic else ""
        self.add(f"<text x='{x}' y='{y}' {FONT} font-size='{size}' font-weight='{weight}' fill='{fill}' text-anchor='{anchor}'{st}>{escape(s)}</text>")

    def lines(self, x, y, w, n, gap=14, last=0.6, h=7):
        for i in range(n):
            ww = w * (last if i == n - 1 else 1)
            self.add(f"<rect x='{x}' y='{y + i * gap}' width='{ww:.0f}' height='{h}' rx='3' fill='{LIGHT}'/>")

    def img(self, x, y, w, h, label="image"):
        self.rect(x, y, w, h, fill="#EEF0ED", stroke=MID)
        self.add(f"<line x1='{x}' y1='{y}' x2='{x + w}' y2='{y + h}' stroke='{LIGHT}' stroke-width='2'/>")
        self.add(f"<line x1='{x + w}' y1='{y}' x2='{x}' y2='{y + h}' stroke='{LIGHT}' stroke-width='2'/>")
        self.text(x + w / 2, y + h / 2 + 5, label, 13, fill=MID, anchor="middle", italic=True)

    def button(self, x, y, w, h, label, kind="primary"):
        fill, col, stroke = {"primary": (AMBER, INK, AMBER), "dark": (GREEN, CREAM, GREEN), "ghost": (PAPER, GREEN, GREEN)}[kind]
        self.rect(x, y, w, h, fill=fill, stroke=stroke, rx=h / 2)
        self.text(x + w / 2, y + h / 2 + 5, label, 14, "bold", col, "middle")

    def note(self, n, x, y):
        self.add(f"<circle cx='{x}' cy='{y}' r='13' fill='{NOTE}'/>")
        self.text(x, y + 5, str(n), 13, "bold", "#FFFFFF", "middle")

    def logo(self, x, y, s=40):
        self.rect(x, y, s, s, fill=CREAM, stroke=GREEN, rx=s * 0.28, sw=2)
        self.add(f"<path d='M{x + s * .2} {y + s * .55} Q{x + s * .45} {y + s * .78} {x + s * .72} {y + s * .5}' stroke='{GREEN}' stroke-width='{s * .09:.1f}' fill='none' stroke-linecap='round'/>")
        self.add(f"<path d='M{x + s * .74} {y + s * .32} L{x + s * .78} {y + s * .46} L{x + s * .9} {y + s * .5} L{x + s * .78} {y + s * .54} L{x + s * .74} {y + s * .68} L{x + s * .7} {y + s * .54} L{x + s * .58} {y + s * .5} L{x + s * .7} {y + s * .46} Z' fill='{GREEN}'/>")

    def save(self, name):
        body = "\n".join(self.e)
        svg = f"<svg xmlns='http://www.w3.org/2000/svg' width='{self.w}' height='{self.h}' viewBox='0 0 {self.w} {self.h}'>\n<rect width='100%' height='100%' fill='{BG}'/>\n{body}\n</svg>\n"
        open(os.path.join(OUT, name), "w", encoding="utf-8").write(svg)


# ------------------------------------------------------------------ éléments communs (ordinateur)
PX, PW = 40, 1200            # zone de la page
NX = 1290                    # colonne des notes
NAV = ["Accueil", "Fonctionnalités", "Tarifs", "À propos", "Contact"]


def frame(s, title, subtitle, height):
    s.text(PX, 28, f"essAI — maquette ordinateur — {title}", 18, "bold", GREEN)
    s.text(PX + PW, 28, subtitle, 13, fill=MID, anchor="end")
    s.frame_idx = len(s.e)
    s.rect(PX, 44, PW, height - 84, fill=PAPER, stroke=MID, rx=10)
    s.text(NX, 64, "Notes (interactions prévues)", 16, "bold", GREEN)


def header(s, y, active):
    s.rect(PX, y, PW, 72, fill=CREAM, stroke=LIGHT, rx=0)
    s.logo(PX + 24, y + 16)
    s.text(PX + 76, y + 44, "essAI", 24, "bold", GREEN)
    x = PX + 420
    for item in NAV:
        s.text(x, y + 42, item, 15, "bold" if item == active else "normal", GREEN if item == active else INK)
        if item == active:
            s.add(f"<rect x='{x}' y='{y + 50}' width='{len(item) * 8}' height='3' fill='{AMBER}'/>")
        x += len(item) * 8 + 34
    s.button(PX + PW - 210, y + 18, 186, 38, "Essayer gratuitement")
    return y + 72


def finish(s, yend):
    s.h = max(s.h, yend + 40)
    s.e[s.frame_idx] = re.sub(r"height='[^']*'", f"height='{yend - 44}'", s.e[s.frame_idx], count=1)


def footer(s, y):
    s.rect(PX, y, PW, 180, fill=GREEN, stroke=GREEN, rx=0)
    s.logo(PX + 32, y + 28, 34)
    s.text(PX + 76, y + 52, "essAI", 20, "bold", CREAM)
    s.text(PX + 32, y + 92, "Parle. essAI s'occupe du reste.", 13, fill=SAGE)
    cols = [("Navigation", NAV), ("Le projet", ["À propos", "Dépôt GitHub", "Maquette"]), ("Légal", ["Mentions légales", "Confidentialité"])]
    x = PX + 420
    for t, items in cols:
        s.text(x, y + 36, t, 14, "bold", CREAM)
        for i, it in enumerate(items):
            s.text(x, y + 62 + i * 18, it, 13, fill=CREAM)
        x += 240
    s.text(PX + 32, y + 164, "Projet étudiant TI504N, Efrei 2026-2027 — Tunui TALFER & Lukyan ROBIN", 12, fill=SAGE)
    return y + 180


def notes(s, items, y0=96):
    y = y0
    for n, txt in items:
        s.note(n, NX + 14, y)
        words, line, ly = txt.split(), "", y + 5
        for w in words:
            if len(line) + len(w) > 30:
                s.text(NX + 36, ly, line, 13)
                line, ly = w, ly + 17
            else:
                line = (line + " " + w).strip()
        s.text(NX + 36, ly, line, 13)
        y = ly + 30


def section_title(s, x, y, t, sub=None):
    s.text(x, y, t, 26, "bold", GREEN)
    if sub:
        s.text(x, y + 26, sub, 15, fill=MID)


def phone(s, x, y, w=250, h=470, content=None):
    s.rect(x, y, w, h, fill=INK, stroke=INK, rx=34)
    s.rect(x + 10, y + 12, w - 20, h - 24, fill=CREAM, stroke=CREAM, rx=26)
    s.rect(x + w / 2 - 40, y + 18, 80, 14, fill=INK, stroke=INK, rx=7)
    if content:
        content(x + 10, y + 12, w - 20, h - 24)


def avatar(s, cx, cy, r=18):
    s.add(f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{SAGE}' stroke='{GREEN}' stroke-width='2'/>")
    s.add(f"<circle cx='{cx - r * .35}' cy='{cy - r * .1}' r='{r * .12}' fill='{GREEN}'/>")
    s.add(f"<circle cx='{cx + r * .35}' cy='{cy - r * .1}' r='{r * .12}' fill='{GREEN}'/>")
    s.add(f"<path d='M{cx - r * .35} {cy + r * .3} Q{cx} {cy + r * .55} {cx + r * .35} {cy + r * .3}' stroke='{GREEN}' stroke-width='2' fill='none'/>")


def wave(s, x, y, w, n=22, color=GREEN):
    import math
    step = w / n
    for i in range(n):
        hh = 6 + 22 * abs(math.sin(i * 0.9)) * (0.4 + 0.6 * abs(math.cos(i * 0.37)))
        s.add(f"<rect x='{x + i * step:.1f}' y='{y - hh / 2:.1f}' width='{step * .55:.1f}' height='{hh:.1f}' rx='2' fill='{color}'/>")


def demo_screen(s):
    def draw(x, y, w, h):
        avatar(s, x + 30, y + 52, 15)
        s.text(x + 52, y + 57, "essAI t'écoute…", 13, "bold", GREEN)
        wave(s, x + 18, y + 100, w - 36)
        s.rect(x + 14, y + 132, w - 28, 92, fill=PAPER, stroke=LIGHT, rx=12)
        s.text(x + 24, y + 152, "« Idée pour le mémoire : comparer", 11, fill=INK)
        s.text(x + 24, y + 168, "trois méthodes de révision, trouver", 11, fill=INK)
        s.text(x + 24, y + 184, "des articles avant vendredi… »", 11, fill=INK)
        s.text(x + 24, y + 210, "transcription en direct ▍", 11, fill=MID, italic=True)
        s.rect(x + 14, y + 238, w - 28, 74, fill=SAGE, stroke=SAGE, rx=12)
        s.text(x + 24, y + 260, "✔ Note : Mémoire révision", 12, "bold", GREEN)
        s.text(x + 24, y + 280, "✔ Tâche : trouver 5 articles", 12, "bold", GREEN)
        s.text(x + 24, y + 300, "✔ Rappel : vendredi 9 h", 12, "bold", GREEN)
        for i, lab in enumerate(["Notes", "Agenda", "Notion"]):
            s.rect(x + 14 + i * 72, y + 330, 64, 52, fill=PAPER, stroke=GREEN, rx=12)
            s.text(x + 46 + i * 72, y + 362, lab, 11, "bold", GREEN, "middle")
        s.add(f"<circle cx='{x + w / 2}' cy='{y + h - 34}' r='22' fill='{AMBER}'/>")
        s.text(x + w / 2, y + h - 29, "🎙", 16, anchor="middle")
    return draw


# ------------------------------------------------------------------ 1. ACCUEIL
s = Svg(1640, 2300)
frame(s, "Accueil (index.html)", "niveau 0 — page d'entrée du site", 2300)
y = header(s, 44, "Accueil")
s.note(1, PX + 1190, 80)
# hero
s.rect(PX, y, PW, 560, fill=CREAM, stroke=CREAM, rx=0)
s.text(PX + 70, y + 130, "Parle.", 52, "bold", GREEN)
s.text(PX + 70, y + 190, "essAI s'occupe du reste.", 52, "bold", GREEN)
s.lines(PX + 70, y + 230, 470, 3, gap=18, h=9)
s.button(PX + 70, y + 310, 220, 50, "Essayer gratuitement")
s.button(PX + 310, y + 310, 190, 50, "Voir la démo ▶", "ghost")
s.text(PX + 70, y + 400, "L'essentiel est gratuit. Les abonnements paient les serveurs, pas la pub.", 14, fill=GREEN, italic=True)
phone(s, PX + 820, y + 40, 260, 490, demo_screen(s))
s.note(2, PX + 800, y + 60)
s.note(3, PX + 480, y + 335)
y += 560
# problème
s.text(PX + 600, y + 70, "Une idée te vient… et tu n'as pas le temps de l'écrire ?", 24, "bold", GREEN, "middle")
s.lines(PX + 300, y + 100, 600, 2, gap=18, h=9, last=0.7)
y += 160
# comment ça marche
section_title(s, PX + 70, y + 40, "Comment ça marche")
for i, (t, d) in enumerate([("1. Tu parles", "en vrac, même dans le désordre"), ("2. essAI reformule", "dans le style de tes notes"), ("3. essAI range", "note, tâche, projet, agenda")]):
    x = PX + 70 + i * 370
    s.rect(x, y + 70, 330, 190, fill=PAPER, stroke=LIGHT, rx=16)
    s.img(x + 20, y + 90, 80, 80, "icône")
    s.text(x + 20, y + 200, t, 18, "bold", GREEN)
    s.text(x + 20, y + 224, d, 13, fill=MID)
s.note(4, PX + 1160, y + 90)
y += 300
# carrousel
section_title(s, PX + 70, y + 40, "Ce que tu peux lui dire", "carrousel d'exemples de phrases")
s.rect(PX + 70, y + 90, 1060, 200, fill=BG, stroke=LIGHT, rx=16)
s.text(PX + 100, y + 200, "◀", 30, "bold", GREEN)
for i in range(3):
    x = PX + 160 + i * 320
    s.rect(x, y + 115, 290, 150, fill=PAPER if i != 1 else CREAM, stroke=GREEN if i == 1 else LIGHT, rx=14)
    s.text(x + 20, y + 150, ["« Rappelle-moi d'appeler le", "« Ajoute fractionné mercredi", "« Crée le projet appli de"][i], 14, "bold", GREEN)
    s.text(x + 20, y + 172, ["garagiste lundi matin »", "18 h et décale la réunion »", "colocation avec 3 pistes »"][i], 14, "bold", GREEN)
    s.lines(x + 20, y + 200, 240, 2)
s.text(PX + 1100, y + 200, "▶", 30, "bold", GREEN)
for i in range(5):
    s.add(f"<circle cx='{PX + 560 + i * 20}' cy='{y + 310}' r='5' fill='{GREEN if i == 1 else LIGHT}'/>")
s.note(5, PX + 1160, y + 110)
y += 340
# intégrations
section_title(s, PX + 70, y + 40, "Il range tout là où tu travailles déjà")
for i, lab in enumerate(["Notes Apple", "Calendrier", "Google Agenda", "Notion", "Obsidian"]):
    s.img(PX + 70 + i * 215, y + 70, 190, 70, lab)
y += 180
# tarifs teaser
section_title(s, PX + 70, y + 40, "Trois offres, dont une gratuite")
for i, (n, p) in enumerate([("Gratuit", "0 €"), ("Plus", "4,99 €/mois"), ("Pro", "11,99 €/mois")]):
    x = PX + 70 + i * 370
    s.rect(x, y + 70, 330, 150, fill=CREAM if i == 1 else PAPER, stroke=GREEN if i == 1 else LIGHT, rx=16)
    s.text(x + 24, y + 108, n, 20, "bold", GREEN)
    s.text(x + 24, y + 140, p, 18, "bold", INK)
    s.lines(x + 24, y + 160, 260, 2)
s.button(PX + 490, y + 250, 220, 46, "Voir les tarifs", "dark")
s.note(6, PX + 1160, y + 90)
y += 320
# CTA
s.rect(PX + 70, y, 1060, 150, fill=GREEN, stroke=GREEN, rx=20)
s.text(PX + 600, y + 62, "Ta prochaine idée mérite mieux qu'un oubli.", 24, "bold", CREAM, "middle")
s.button(PX + 490, y + 86, 220, 44, "Essayer gratuitement")
y += 200
finish(s, footer(s, y))
s.note(7, PX + 1190, y + 30)
notes(s, [
    (1, "En-tête commun : logo + titre essAI + navigation. Sur téléphone, menu burger (JS)."),
    (2, "Démo animée en JS : l'onde s'anime, la transcription s'écrit lettre par lettre, puis les cartes partent vers Notes, Agenda et Notion. Se rejoue en boucle."),
    (3, "« Voir la démo » relance l'animation du téléphone."),
    (4, "Apparition des 3 étapes au défilement (IntersectionObserver)."),
    (5, "Carrousel en JS : flèches, points, défilement automatique toutes les 5 s, pause au survol. Exigé par l'énoncé."),
    (6, "Aperçu des offres, lien vers la page Tarifs."),
    (7, "Pied de page commun : navigation + lien « À propos » (exigé)."),
])
s.save("01_accueil_ordinateur.svg")

# ------------------------------------------------------------------ 2. FONCTIONNALITÉS
s = Svg(1640, 2420)
frame(s, "Fonctionnalités (pages/fonctionnalites.html)", "niveau 1 — « En savoir plus »", 2420)
y = header(s, 44, "Fonctionnalités")
s.rect(PX, y, PW, 220, fill=CREAM, stroke=CREAM, rx=0)
s.text(PX + 70, y + 90, "Tout ce qu'essAI fait de ta voix", 40, "bold", GREEN)
s.lines(PX + 70, y + 120, 600, 2, gap=18, h=9)
for i, lab in enumerate(["Dictée", "Reformulation", "Rangement", "Chatbot", "Agents"]):
    s.button(PX + 70 + i * 170, y + 160, 150, 36, lab, "ghost")
s.note(1, PX + 920, y + 178)
y += 220
# dictée
section_title(s, PX + 70, y + 60, "1. Dictée et transcription")
s.lines(PX + 70, y + 90, 420, 4, gap=18, h=9)
s.rect(PX + 600, y + 30, 530, 200, fill=BG, stroke=LIGHT, rx=16)
avatar(s, PX + 640, y + 75)
wave(s, PX + 680, y + 75, 300)
s.text(PX + 1000, y + 80, "→", 26, "bold", GREEN)
s.rect(PX + 630, y + 120, 470, 80, fill=PAPER, stroke=LIGHT, rx=12)
s.lines(PX + 650, y + 140, 420, 3, gap=16)
s.note(2, PX + 1110, y + 40)
y += 270
# reformulation
section_title(s, PX + 70, y + 60, "2. Reformulée dans ton style")
s.rect(PX + 70, y + 90, 500, 200, fill=BG, stroke=LIGHT, rx=16)
s.text(PX + 90, y + 120, "Avant : ce que tu as dit", 14, "bold", MID)
s.lines(PX + 90, y + 140, 460, 6, gap=18)
s.rect(PX + 630, y + 90, 500, 200, fill=CREAM, stroke=GREEN, rx=16)
s.text(PX + 650, y + 120, "Après : la note essAI", 14, "bold", GREEN)
s.lines(PX + 650, y + 140, 460, 6, gap=18)
s.note(3, PX + 1140, y + 100)
y += 330
# rangement
section_title(s, PX + 70, y + 60, "3. Rangée au bon endroit")
s.rect(PX + 470, y + 100, 260, 70, fill=GREEN, stroke=GREEN, rx=14)
s.text(PX + 600, y + 142, "Ta dictée", 18, "bold", CREAM, "middle")
for i, lab in enumerate(["Note", "Tâche", "Projet + pistes", "Agenda"]):
    x = PX + 120 + i * 260
    s.add(f"<line x1='{PX + 600}' y1='{y + 170}' x2='{x + 110}' y2='{y + 240}' stroke='{GREEN}' stroke-width='2' stroke-dasharray='6 4'/>")
    s.rect(x, y + 240, 220, 60, fill=PAPER, stroke=GREEN, rx=12)
    s.text(x + 110, y + 276, lab, 15, "bold", GREEN, "middle")
s.text(PX + 600, y + 340, "Intégrations : Notes Apple · Calendrier · Google Agenda · Notion · Obsidian · recherche web", 14, fill=MID, anchor="middle")
s.note(4, PX + 1140, y + 120)
y += 380
# chatbot
section_title(s, PX + 70, y + 60, "4. Parle avec essAI", "démo : choisis une phrase, l'avatar répond")
s.rect(PX + 70, y + 110, 560, 420, fill=PAPER, stroke=GREEN, rx=18, sw=2)
avatar(s, PX + 110, y + 150)
s.text(PX + 140, y + 156, "essAI", 16, "bold", GREEN)
s.text(PX + 205, y + 156, "● en ligne", 12, fill=SAGE)
s.rect(PX + 90, y + 190, 340, 54, fill=SAGE, stroke=SAGE, rx=14)
s.lines(PX + 105, y + 205, 300, 2, gap=14)
s.rect(PX + 270, y + 260, 340, 54, fill=CREAM, stroke=LIGHT, rx=14)
s.lines(PX + 285, y + 275, 300, 2, gap=14)
s.rect(PX + 90, y + 330, 340, 54, fill=SAGE, stroke=SAGE, rx=14)
s.lines(PX + 105, y + 345, 300, 2, gap=14)
for i, lab in enumerate(["Organise ma semaine", "Idée de projet", "Que peux-tu faire ?"]):
    s.button(PX + 90 + i * 180, y + 410, 170, 32, lab, "ghost")
s.rect(PX + 90, y + 460, 440, 44, fill=BG, stroke=LIGHT, rx=22)
s.text(PX + 110, y + 488, "Écris ou appuie sur le micro…", 13, fill=MID, italic=True)
s.add(f"<circle cx='{PX + 580}' cy='{y + 482}' r='22' fill='{AMBER}'/>")
s.text(PX + 580, y + 487, "🎙", 15, anchor="middle")
s.lines(PX + 690, y + 150, 420, 6, gap=20, h=9)
s.note(5, PX + 640, y + 120)
y += 570
# approfondissement & agents
section_title(s, PX + 70, y + 60, "5. Aller plus loin : approfondissement et agents")
for i, (t, badge) in enumerate([("Approfondissement", "Plus"), ("Agents autonomes (MCP : Claude, ChatGPT)", "Pro")]):
    x = PX + 70 + i * 540
    s.rect(x, y + 90, 500, 200, fill=PAPER, stroke=LIGHT, rx=16)
    s.rect(x + 20, y + 110, 60, 26, fill=AMBER, stroke=AMBER, rx=13)
    s.text(x + 50, y + 128, badge, 13, "bold", INK, "middle")
    s.text(x + 20, y + 170, t, 18, "bold", GREEN)
    s.lines(x + 20, y + 190, 440, 4, gap=18)
s.button(PX + 490, y + 320, 220, 46, "Voir les tarifs", "dark")
s.note(6, PX + 1140, y + 100)
y += 400
finish(s, footer(s, y))
notes(s, [
    (1, "Sommaire : boutons qui font défiler en douceur jusqu'à la section (ancres + scroll-behavior)."),
    (2, "Illustration animée en CSS : l'onde bouge, puis le texte apparaît."),
    (3, "Comparaison avant/après : un curseur JS pour glisser de l'une à l'autre."),
    (4, "Schéma : les flèches se dessinent au défilement (animation CSS)."),
    (5, "Démo du chatbot en JS : réponses préparées (pas d'IA réelle), indicateur « essAI écrit… », avatar qui cligne des yeux."),
    (6, "Badges d'offre, lien vers Tarifs."),
])
s.save("02_fonctionnalites_ordinateur.svg")

# ------------------------------------------------------------------ 3. TARIFS
s = Svg(1640, 2240)
frame(s, "Tarifs (pages/tarifs.html)", "niveau 1 — offres, tableau comparatif, FAQ", 2240)
y = header(s, 44, "Tarifs")
s.rect(PX, y, PW, 200, fill=CREAM, stroke=CREAM, rx=0)
s.text(PX + 600, y + 80, "L'essentiel gratuit. Le reste à prix juste.", 36, "bold", GREEN, "middle")
s.rect(PX + 480, y + 120, 240, 44, fill=PAPER, stroke=GREEN, rx=22)
s.rect(PX + 484, y + 124, 116, 36, fill=GREEN, stroke=GREEN, rx=18)
s.text(PX + 542, y + 148, "Mensuel", 14, "bold", CREAM, "middle")
s.text(PX + 660, y + 148, "Annuel −17 %", 14, "bold", GREEN, "middle")
s.note(1, PX + 750, y + 142)
y += 200
plans = [("Gratuit", None, "0 €", ["Dictée et transcription", "Rangement automatique", "1 intégration", "30 dictées par mois"], False),
         ("Plus", "9,99 €", "4,99 €", ["Tout le Gratuit", "Approfondissement des idées", "Plans de projet détaillés", "500 dictées par mois"], True),
         ("Pro", "24,99 €", "11,99 €", ["Tout le Plus", "Agents autonomes (MCP)", "Claude / ChatGPT connectés", "3 000 dictées par mois"], False)]
for i, (n, old, new, feats, best) in enumerate(plans):
    x = PX + 70 + i * 370
    s.rect(x, y + 50, 330, 440, fill=CREAM if best else PAPER, stroke=GREEN if best else LIGHT, rx=18, sw=2.5 if best else 1.5)
    if best:
        s.rect(x + 95, y + 34, 140, 30, fill=AMBER, stroke=AMBER, rx=15)
        s.text(x + 165, y + 54, "Le plus choisi", 13, "bold", INK, "middle")
    s.text(x + 28, y + 100, n, 24, "bold", GREEN)
    if old:
        s.text(x + 28, y + 140, old, 18, fill=MID)
        s.add(f"<line x1='{x + 26}' y1='{y + 134}' x2='{x + 92}' y2='{y + 134}' stroke='{MID}' stroke-width='2'/>")
        s.rect(x + 110, y + 122, 150, 24, fill=SAGE, stroke=SAGE, rx=12)
        s.text(x + 185, y + 139, "Offre de lancement", 12, "bold", GREEN, "middle")
    s.text(x + 28, y + 186, new, 34, "bold", INK)
    s.text(x + 28 + len(new) * 18, y + 186, "/mois", 14, fill=MID)
    for j, f in enumerate(feats):
        s.text(x + 28, y + 236 + j * 32, "✔  " + f, 14, fill=INK)
    s.button(x + 28, y + 400, 274, 46, "Commencer" if i == 0 else "Choisir " + n, "primary" if best else "ghost")
s.note(2, PX + 1160, y + 60)
y += 540
section_title(s, PX + 70, y + 40, "Comparer les offres", "tableau HTML (exigé par l'énoncé)")
rows = ["Dictées par mois", "Transcription + reformulation", "Intégrations", "Approfondissement", "Agents autonomes", "Assistance"]
tx, tw = PX + 70, 1060
s.rect(tx, y + 80, tw, 52, fill=GREEN, stroke=GREEN, rx=8)
for j, h in enumerate(["Fonctionnalité", "Gratuit", "Plus", "Pro"]):
    s.text(tx + 24 + (0 if j == 0 else 340 + (j - 1) * 240), y + 113, h, 15, "bold", CREAM)
for r, lab in enumerate(rows):
    ry = y + 132 + r * 46
    s.rect(tx, ry, tw, 46, fill=PAPER if r % 2 else BG, stroke=LIGHT, rx=0)
    s.text(tx + 24, ry + 29, lab, 14)
    for j in range(3):
        s.add(f"<rect x='{tx + 364 + j * 240}' y='{ry + 18}' width='60' height='9' rx='4' fill='{LIGHT}'/>")
s.note(3, PX + 1160, y + 100)
y += 470
section_title(s, PX + 70, y + 40, "Où va ton argent ?")
s.lines(PX + 70, y + 70, 420, 3, gap=18, h=9)
for j, (lab, pct, col) in enumerate([("Serveurs et IA", .6, GREEN), ("Développement", .3, SAGE), ("Frais bancaires", .1, AMBER)]):
    s.text(PX + 600, y + 80 + j * 50, lab, 14, "bold")
    s.rect(PX + 760, y + 66 + j * 50, 360, 20, fill=BG, stroke=LIGHT, rx=10)
    s.rect(PX + 760, y + 66 + j * 50, 360 * pct, 20, fill=col, stroke=col, rx=10)
s.note(4, PX + 1160, y + 60)
y += 230
section_title(s, PX + 70, y + 40, "Questions fréquentes")
for j, q in enumerate(["Pourquoi des prix de lancement ?", "Puis-je changer d'offre à tout moment ?", "Que fait essAI de mes données ?", "C'est quoi un agent autonome ?"]):
    ry = y + 70 + j * 62
    s.rect(PX + 70, ry, 1060, 52, fill=PAPER, stroke=LIGHT, rx=12)
    s.text(PX + 94, ry + 32, q, 15, "bold", GREEN)
    s.text(PX + 1100, ry + 33, "+" if j else "−", 20, "bold", GREEN)
s.note(5, PX + 1160, y + 90)
y += 360
finish(s, footer(s, y))
notes(s, [
    (1, "Bascule mensuel/annuel en JS : les prix des cartes et du tableau changent (Plus 49,90 €/an au lieu de 99 €, Pro 119,90 €/an au lieu de 249 €)."),
    (2, "Prix normal barré + prix de lancement (badge « Offre de lancement »)."),
    (3, "Tableau HTML (<table>, <thead>, <tbody>), lignes alternées, défilement horizontal sur téléphone."),
    (4, "Barres qui se remplissent au défilement (animation CSS déclenchée en JS)."),
    (5, "FAQ en accordéon (JS) : un clic ouvre la réponse, ferme les autres."),
])
s.save("03_tarifs_ordinateur.svg")

# ------------------------------------------------------------------ 4. À PROPOS
s = Svg(1640, 1900)
frame(s, "À propos (pages/a-propos.html)", "niveau 1 — exigée par l'énoncé", 1900)
y = header(s, 44, "À propos")
s.rect(PX, y, PW, 220, fill=CREAM, stroke=CREAM, rx=0)
s.text(PX + 70, y + 90, "Pourquoi essAI existe", 40, "bold", GREEN)
s.lines(PX + 70, y + 120, 700, 3, gap=18, h=9)
y += 220
section_title(s, PX + 70, y + 60, "Le problème qu'on veut régler")
s.lines(PX + 70, y + 90, 560, 6, gap=18, h=9)
s.img(PX + 700, y + 40, 430, 220, "illustration : l'idée qui s'envole")
s.note(1, PX + 1140, y + 50)
y += 300
section_title(s, PX + 70, y + 40, "Nos engagements")
for i, t in enumerate(["Gratuit pour l'essentiel", "Tes données t'appartiennent", "Des prix transparents"]):
    x = PX + 70 + i * 370
    s.rect(x, y + 70, 330, 170, fill=PAPER, stroke=LIGHT, rx=16)
    s.img(x + 20, y + 90, 50, 50, "")
    s.text(x + 20, y + 170, t, 17, "bold", GREEN)
    s.lines(x + 20, y + 190, 280, 2)
y += 280
section_title(s, PX + 70, y + 40, "L'équipe", "les membres du projet et le travail de chacun (exigé par l'énoncé)")
for i, (n, r) in enumerate([("Tunui TALFER", "Accueil, Tarifs, CSS commun, démo du téléphone"), ("Lukyan ROBIN", "Maquette, logo, Fonctionnalités, Contact, chatbot")]):
    x = PX + 70 + i * 540
    s.rect(x, y + 90, 500, 250, fill=PAPER, stroke=LIGHT, rx=18)
    s.add(f"<circle cx='{x + 80}' cy='{y + 170}' r='50' fill='{BG}' stroke='{MID}'/>")
    s.text(x + 80, y + 175, "photo", 12, fill=MID, anchor="middle", italic=True)
    s.text(x + 150, y + 150, n, 20, "bold", GREEN)
    s.text(x + 150, y + 175, r, 13, fill=MID)
    s.lines(x + 150, y + 200, 320, 4, gap=18)
s.note(2, PX + 1140, y + 100)
y += 380
section_title(s, PX + 70, y + 40, "Le projet")
s.lines(PX + 70, y + 70, 700, 2, gap=18, h=9)
s.button(PX + 70, y + 120, 230, 44, "Voir le dépôt GitHub", "dark")
y += 200
finish(s, footer(s, y))
notes(s, [
    (1, "Texte de motivation : les idées qui arrivent au mauvais moment et qu'on n'a pas le temps d'écrire."),
    (2, "Cartes de l'équipe qui se retournent au survol (CSS 3D) pour afficher le détail du travail de chacun."),
])
s.save("04_a-propos_ordinateur.svg")

# ------------------------------------------------------------------ 5. CONTACT
s = Svg(1640, 1640)
frame(s, "Contact (pages/contact.html)", "niveau 1 — formulaire (exigé par l'énoncé)", 1640)
y = header(s, 44, "Contact")
s.rect(PX, y, PW, 180, fill=CREAM, stroke=CREAM, rx=0)
s.text(PX + 70, y + 90, "Une question ? Une idée ?", 40, "bold", GREEN)
s.lines(PX + 70, y + 120, 500, 1, h=9)
y += 180
s.rect(PX + 70, y + 50, 660, 700, fill=PAPER, stroke=LIGHT, rx=18)
fy = y + 90
for lab, h in [("Nom *", 46), ("E-mail *", 46), ("Sujet *  (liste : question, partenariat, presse, bug)", 46), ("Message *", 170)]:
    s.text(PX + 100, fy, lab, 14, "bold", GREEN)
    s.rect(PX + 100, fy + 12, 600, h, fill=BG, stroke=MID, rx=10)
    fy += h + 50
s.text(PX + 100, fy - 14, "⚠ Adresse e-mail invalide", 13, fill=NOTE)
s.rect(PX + 100, fy + 6, 20, 20, fill=PAPER, stroke=MID, rx=4)
s.text(PX + 132, fy + 22, "J'accepte que mes données servent à me répondre *", 13)
s.button(PX + 100, fy + 50, 200, 48, "Envoyer")
s.note(1, PX + 740, y + 70)
s.rect(PX + 780, y + 50, 350, 300, fill=GREEN, stroke=GREEN, rx=18)
s.text(PX + 806, y + 100, "Rejoindre la liste d'attente", 18, "bold", CREAM)
s.lines(PX + 806, y + 125, 290, 2, gap=16)
s.rect(PX + 806, y + 180, 298, 44, fill=CREAM, stroke=CREAM, rx=22)
s.button(PX + 806, y + 240, 180, 42, "M'inscrire")
s.note(2, PX + 1140, y + 60)
s.rect(PX + 780, y + 380, 350, 210, fill=PAPER, stroke=LIGHT, rx=18)
s.text(PX + 806, y + 420, "Nous écrire directement", 16, "bold", GREEN)
s.lines(PX + 806, y + 445, 290, 3, gap=20)
s.text(PX + 806, y + 540, "Réponse sous 48 h", 13, fill=MID, italic=True)
y += 800
finish(s, footer(s, y))
notes(s, [
    (1, "Validation du formulaire en JS avant l'envoi : champs obligatoires, format de l'e-mail, message de 20 caractères minimum, messages d'erreur sous les champs, compteur de caractères, message de confirmation."),
    (2, "Liste d'attente : vérification de l'e-mail, puis remerciement animé (aucune donnée envoyée : site statique)."),
])
s.save("05_contact_ordinateur.svg")

# ------------------------------------------------------------------ TÉLÉPHONE (toutes les pages)
MW, MH, GAP = 390, 1800, 60
s = Svg(5 * (MW + GAP) + GAP, MH + 160)
s.text(GAP, 34, "essAI — maquette téléphone (390 px de large) — une colonne, menu burger", 18, "bold", GREEN)
pages = ["Accueil", "Fonctionnalités", "Tarifs", "À propos", "Contact"]
for k, page in enumerate(pages):
    x0, y0 = GAP + k * (MW + GAP), 70
    s.text(x0, y0 - 10, page, 15, "bold", GREEN)
    s.rect(x0, y0, MW, MH, fill=PAPER, stroke=MID, rx=28)
    s.rect(x0, y0, MW, 64, fill=CREAM, stroke=LIGHT, rx=0)
    s.logo(x0 + 16, y0 + 14, 36)
    s.text(x0 + 62, y0 + 40, "essAI", 20, "bold", GREEN)
    for j in range(3):
        s.add(f"<rect x='{x0 + MW - 46}' y='{y0 + 22 + j * 9}' width='26' height='4' rx='2' fill='{GREEN}'/>")
    if k == 0:
        s.note(1, x0 + MW - 70, y0 + 32)
    y = y0 + 64
    if page == "Accueil":
        s.text(x0 + 20, y + 60, "Parle.", 30, "bold", GREEN)
        s.text(x0 + 20, y + 96, "essAI s'occupe", 30, "bold", GREEN)
        s.text(x0 + 20, y + 132, "du reste.", 30, "bold", GREEN)
        s.lines(x0 + 20, y + 152, 340, 2, gap=16)
        s.button(x0 + 20, y + 196, 350, 44, "Essayer gratuitement")
        phone(s, x0 + 70, y + 270, 250, 470, demo_screen(s))
        s.text(x0 + 20, y + 790, "Comment ça marche", 20, "bold", GREEN)
        for j in range(3):
            s.rect(x0 + 20, y + 810 + j * 96, 350, 84, fill=PAPER, stroke=LIGHT, rx=14)
            s.lines(x0 + 100, y + 830 + j * 96, 240, 3, gap=14)
            s.img(x0 + 32, y + 822 + j * 96, 56, 56, "")
        s.text(x0 + 20, y + 1130, "Ce que tu peux lui dire", 20, "bold", GREEN)
        s.rect(x0 + 20, y + 1150, 350, 130, fill=CREAM, stroke=GREEN, rx=14)
        s.lines(x0 + 40, y + 1175, 300, 3, gap=16)
        s.text(x0 + 195, y + 1305, "● ○ ○ ○ ○   (glisser du doigt)", 12, fill=MID, anchor="middle")
        s.note(2, x0 + 20, y + 1150)
    elif page == "Fonctionnalités":
        s.text(x0 + 20, y + 60, "Tout ce qu'essAI", 26, "bold", GREEN)
        s.text(x0 + 20, y + 92, "fait de ta voix", 26, "bold", GREEN)
        s.rect(x0 + 20, y + 120, 350, 40, fill=BG, stroke=LIGHT, rx=20)
        s.text(x0 + 36, y + 146, "Dictée · Reformulation · Rangement · …", 12, fill=MID)
        for j, t in enumerate(["1. Dictée", "2. Ton style", "3. Rangement"]):
            s.text(x0 + 20, y + 200 + j * 180, t, 18, "bold", GREEN)
            s.img(x0 + 20, y + 214 + j * 180, 350, 100, "illustration")
            s.lines(x0 + 20, y + 326 + j * 180, 340, 2, gap=14)
        s.text(x0 + 20, y + 760, "4. Parle avec essAI", 18, "bold", GREEN)
        s.rect(x0 + 20, y + 776, 350, 400, fill=PAPER, stroke=GREEN, rx=16, sw=2)
        avatar(s, x0 + 52, y + 810, 16)
        s.rect(x0 + 34, y + 846, 250, 50, fill=SAGE, stroke=SAGE, rx=12)
        s.rect(x0 + 106, y + 910, 250, 50, fill=CREAM, stroke=LIGHT, rx=12)
        s.rect(x0 + 34, y + 974, 250, 50, fill=SAGE, stroke=SAGE, rx=12)
        s.rect(x0 + 34, y + 1110, 270, 40, fill=BG, stroke=LIGHT, rx=20)
        s.add(f"<circle cx='{x0 + 336}' cy='{y + 1130}' r='18' fill='{AMBER}'/>")
        s.text(x0 + 20, y + 1220, "5. Approfondissement et agents", 18, "bold", GREEN)
        s.rect(x0 + 20, y + 1236, 350, 90, fill=PAPER, stroke=LIGHT, rx=14)
        s.rect(x0 + 20, y + 1336, 350, 90, fill=PAPER, stroke=LIGHT, rx=14)
    elif page == "Tarifs":
        s.text(x0 + 20, y + 60, "L'essentiel gratuit.", 24, "bold", GREEN)
        s.text(x0 + 20, y + 90, "Le reste à prix juste.", 24, "bold", GREEN)
        s.rect(x0 + 75, y + 110, 240, 40, fill=PAPER, stroke=GREEN, rx=20)
        s.rect(x0 + 78, y + 113, 116, 34, fill=GREEN, stroke=GREEN, rx=17)
        s.text(x0 + 136, y + 135, "Mensuel", 13, "bold", CREAM, "middle")
        s.text(x0 + 254, y + 135, "Annuel", 13, "bold", GREEN, "middle")
        for j, (n, old, new) in enumerate([("Gratuit", None, "0 €"), ("Plus", "9,99 €", "4,99 €"), ("Pro", "24,99 €", "11,99 €")]):
            yy = y + 180 + j * 250
            s.rect(x0 + 20, yy, 350, 230, fill=CREAM if j == 1 else PAPER, stroke=GREEN if j == 1 else LIGHT, rx=16)
            s.text(x0 + 40, yy + 36, n, 20, "bold", GREEN)
            if old:
                s.text(x0 + 40, yy + 66, old, 15, fill=MID)
                s.add(f"<line x1='{x0 + 38}' y1='{yy + 61}' x2='{x0 + 96}' y2='{yy + 61}' stroke='{MID}' stroke-width='2'/>")
            s.text(x0 + 40, yy + 104, new + " /mois", 26, "bold")
            s.lines(x0 + 40, yy + 124, 300, 3, gap=16)
            s.button(x0 + 40, yy + 172, 310, 40, "Choisir", "primary" if j == 1 else "ghost")
        s.text(x0 + 20, y + 950, "Comparer", 18, "bold", GREEN)
        s.rect(x0 + 20, y + 966, 350, 220, fill=BG, stroke=LIGHT, rx=10)
        s.text(x0 + 195, y + 1082, "tableau → défilement horizontal", 12, fill=MID, anchor="middle", italic=True)
        s.text(x0 + 20, y + 1230, "Questions fréquentes", 18, "bold", GREEN)
        for j in range(4):
            s.rect(x0 + 20, y + 1246 + j * 54, 350, 46, fill=PAPER, stroke=LIGHT, rx=10)
        s.note(3, x0 + 20, y + 966)
    elif page == "À propos":
        s.text(x0 + 20, y + 60, "Pourquoi essAI", 26, "bold", GREEN)
        s.text(x0 + 20, y + 92, "existe", 26, "bold", GREEN)
        s.lines(x0 + 20, y + 112, 340, 4, gap=16)
        s.img(x0 + 20, y + 190, 350, 180, "illustration")
        s.text(x0 + 20, y + 420, "Nos engagements", 18, "bold", GREEN)
        for j in range(3):
            s.rect(x0 + 20, y + 436 + j * 100, 350, 88, fill=PAPER, stroke=LIGHT, rx=14)
        s.text(x0 + 20, y + 760, "L'équipe", 18, "bold", GREEN)
        for j, n in enumerate(["Tunui TALFER", "Lukyan ROBIN"]):
            yy = y + 776 + j * 210
            s.rect(x0 + 20, yy, 350, 196, fill=PAPER, stroke=LIGHT, rx=16)
            s.add(f"<circle cx='{x0 + 70}' cy='{yy + 54}' r='34' fill='{BG}' stroke='{MID}'/>")
            s.text(x0 + 120, yy + 50, n, 17, "bold", GREEN)
            s.lines(x0 + 40, yy + 104, 310, 4, gap=16)
        s.button(x0 + 20, y + 1210, 350, 44, "Voir le dépôt GitHub", "dark")
    elif page == "Contact":
        s.text(x0 + 20, y + 60, "Une question ?", 26, "bold", GREEN)
        fy = y + 100
        for lab, h in [("Nom *", 44), ("E-mail *", 44), ("Sujet *", 44), ("Message *", 150)]:
            s.text(x0 + 20, fy, lab, 13, "bold", GREEN)
            s.rect(x0 + 20, fy + 10, 350, h, fill=BG, stroke=MID, rx=10)
            fy += h + 42
        s.rect(x0 + 20, fy, 18, 18, fill=PAPER, stroke=MID, rx=4)
        s.text(x0 + 46, fy + 14, "J'accepte…", 12)
        s.button(x0 + 20, fy + 40, 350, 46, "Envoyer")
        s.rect(x0 + 20, fy + 120, 350, 220, fill=GREEN, stroke=GREEN, rx=16)
        s.text(x0 + 40, fy + 160, "Liste d'attente", 18, "bold", CREAM)
        s.rect(x0 + 40, fy + 190, 310, 42, fill=CREAM, stroke=CREAM, rx=21)
        s.button(x0 + 40, fy + 250, 200, 40, "M'inscrire")
    # pied de page compact
    fy = y0 + MH - 170
    s.rect(x0, fy, MW, 170, fill=GREEN, stroke=GREEN, rx=0)
    s.text(x0 + 20, fy + 40, "essAI", 18, "bold", CREAM)
    s.text(x0 + 20, fy + 72, "Accueil · Fonctionnalités · Tarifs", 13, fill=CREAM)
    s.text(x0 + 20, fy + 96, "À propos · Contact · GitHub", 13, fill=CREAM)
    s.text(x0 + 20, fy + 140, "Projet étudiant TI504N — Efrei", 11, fill=SAGE)
for n, t, x in [(1, "Menu burger (JS) : la navigation s'ouvre en plein écran.", GAP),
                (2, "Carrousel au doigt (événements tactiles) sur téléphone.", GAP + 1 * (MW + GAP) + 0),
                (3, "Le tableau défile horizontalement au lieu d'écraser les colonnes.", GAP + 2 * (MW + GAP))]:
    s.note(n, x + 14, MH + 112)
    s.text(x + 36, MH + 117, t, 13)
s.save("06_toutes_les_pages_telephone.svg")

# ------------------------------------------------------------------ PLAN DU SITE
s = Svg(1240, 620)
s.text(40, 40, "essAI — plan du site (arborescence : 2 niveaux maximum, comme l'exige l'énoncé)", 18, "bold", GREEN)
s.rect(470, 80, 300, 90, fill=GREEN, stroke=GREEN, rx=16)
s.text(620, 120, "Accueil", 22, "bold", CREAM, "middle")
s.text(620, 148, "index.html — niveau 0", 13, fill=SAGE, anchor="middle")
kids = [("Fonctionnalités", "pages/fonctionnalites.html"), ("Tarifs", "pages/tarifs.html"), ("À propos", "pages/a-propos.html"), ("Contact", "pages/contact.html")]
for i, (t, f) in enumerate(kids):
    x = 40 + i * 300
    s.add(f"<line x1='620' y1='170' x2='{x + 130}' y2='260' stroke='{GREEN}' stroke-width='2'/>")
    s.rect(x, 260, 260, 90, fill=CREAM, stroke=GREEN, rx=14, sw=2)
    s.text(x + 130, 300, t, 19, "bold", GREEN, "middle")
    s.text(x + 130, 326, f + " — niveau 1", 12, fill=MID, anchor="middle")
secs = {0: ["#dictee", "#reformulation", "#rangement", "#chatbot", "#agents"], 1: ["#offres", "#comparatif", "#argent", "#faq"], 2: ["#probleme", "#engagements", "#equipe"], 3: ["#formulaire", "#liste-attente"]}
for i, ss in secs.items():
    x = 40 + i * 300
    for j, a in enumerate(ss):
        s.rect(x + 30, 380 + j * 40, 200, 30, fill=PAPER, stroke=LIGHT, rx=8, dash=True)
        s.text(x + 130, 400 + j * 40, a, 12, fill=MID, anchor="middle")
s.text(40, 600, "En pointillés : sections de la page (ancres), pas de pages supplémentaires. Chaque page est à 1 clic de l'accueil ; l'en-tête et le pied de page relient toutes les pages entre elles.", 13, fill=INK)
s.save("00_plan_du_site.svg")
print("ok", sorted(os.listdir(OUT)))
