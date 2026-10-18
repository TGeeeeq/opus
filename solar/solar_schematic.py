import sys

import schemdraw
import schemdraw.elements as elm

schemdraw.use("matplotlib")

FS = 10
SMALL = 8


def wire(d, a, b, **kw):
    return d.add(elm.Line().at(a).to(b).linewidth(1.6), **kw)


def text(d, xy, s, size=SMALL, halign="center", valign="center", color="black"):
    d.add(elm.Label().at(xy).label(s, fontsize=size, halign=halign, valign=valign, color=color))


def box(d, x1, y1, x2, y2):
    for a, b in (((x1, y1), (x2, y1)), ((x2, y1), (x2, y2)), ((x2, y2), (x1, y2)), ((x1, y2), (x1, y1))):
        wire(d, a, b)


def draw(out_base):
    with schemdraw.Drawing(show=False) as d:
        d.config(fontsize=FS, font="DejaVu Sans", lw=1.6, unit=3)

        # FV string G1 + G2 v sérii
        d.add(elm.Solar().at((0, 7)).down().length(3).reverse().label("G1\n100 Wp", loc="bottom", ofst=0.6))
        d.add(elm.Dot().at((0, 4)))
        d.add(elm.Solar().at((0, 4)).down().length(3).reverse().label("G2\n100 Wp", loc="bottom", ofst=0.6))
        text(d, (0.35, 7.35), "+", FS)
        text(d, (0.35, 0.65), "−", FS)
        text(d, (-2.6, 4), "FV string\nVmp ≈ 36 V\nVoc ≈ 45 V\n(mráz ~50 V)\nI ≈ 5,6 A", SMALL)

        d.add(elm.Line().at((-0.9, 2.3)).to((-0.9, -0.6)).linestyle("--").color("#2E7D32").linewidth(1))
        d.add(elm.Ground().at((-0.9, -0.6)).color("#2E7D32"))
        text(d, (-0.9, -1.75), "PE rámů", SMALL, color="#2E7D32")

        # Q1 dvoupólový DC odpínač
        wire(d, (0, 7), (1.5, 7))
        d.add(elm.Switch().at((1.5, 7)).right().length(2))
        wire(d, (3.5, 7), (6, 7))
        wire(d, (0, 1), (1.5, 1))
        d.add(elm.Switch().at((1.5, 1)).right().length(2))
        wire(d, (3.5, 1), (6, 1))
        d.add(elm.Line().at((2.5, 7.25)).to((2.5, 1.25)).linestyle("--").linewidth(1))
        text(d, (2.5, 7.95), "Q1  DC odpínač 2P\n16 A / ≥ 500 V DC", SMALL)
        text(d, (4.7, 7.3), "4 mm²", SMALL)
        text(d, (4.7, 1.3), "4 mm²", SMALL)

        # A1 MPPT regulátor
        box(d, 6, 0, 10, 8)
        text(d, (8, 4.3), "A1\nMPPT\n75/15", FS)
        text(d, (6.15, 7), "PV+", SMALL, halign="left")
        text(d, (6.15, 1), "PV−", SMALL, halign="left")
        text(d, (9.85, 7), "BAT+", SMALL, halign="right")
        text(d, (9.85, 1), "BAT−", SMALL, halign="right")
        text(d, (7, 0.3), "LOAD+", SMALL)
        text(d, (9, 0.3), "LOAD−", SMALL)

        # větev nabíjení: A1 → F2 → + sběrnice
        wire(d, (10, 7), (12, 7))
        d.add(elm.FuseIEC().at((12, 7)).up().length(3).label("F2\n20 A", loc="bottom", ofst=0.3))
        d.add(elm.Dot().at((12, 10)))
        text(d, (11.2, 8.5), "6 mm²", SMALL)
        wire(d, (10, 1), (12, 1))
        wire(d, (12, 1), (12, -2))
        d.add(elm.Dot().at((12, -2)))

        # sběrnice
        wire(d, (12, 10), (20, 10))
        wire(d, (12, -2), (20, -2))
        text(d, (13.4, 10.45), "L+  sběrnice +12,8 V", SMALL, halign="left")
        text(d, (13.4, -2.45), "L−  sběrnice 0 V (−)", SMALL, halign="left")

        # baterie GB1 s hlavním vypínačem Q2 a pojistkou F1
        d.add(elm.Dot().at((16, 10)))
        d.add(elm.Switch().at((16, 10)).down().length(2.2).label("Q2\nhlavní\nvypínač", loc="bottom", ofst=0.3))
        d.add(elm.FuseIEC().at((16, 7.8)).down().length(2.2).label("F1\n80 A\nMEGA/ANL", loc="bottom", ofst=0.3))
        wire(d, (16, 5.6), (16, 5))
        d.add(elm.Battery().at((16, 5)).down().length(3)
              .label("GB1\nLiFePO4\n12,8 V\n100 Ah\n(BMS)", loc="bottom", ofst=0.4))
        text(d, (16.45, 4.75), "+", FS)
        wire(d, (16, 2), (16, -2))
        d.add(elm.Dot().at((16, -2)))
        text(d, (15.25, 0), "25 mm²", SMALL)

        # A2 střídač s pojistkou F3
        d.add(elm.Dot().at((20, 10)))
        d.add(elm.FuseIEC().at((20, 10)).down().length(2.5).label("F3\n60 A", loc="bottom", ofst=0.3))
        wire(d, (20, 7.5), (20, 6.5))
        box(d, 19, 1.5, 23.5, 6.5)
        text(d, (21.4, 4), "A2\nstřídač\n12 V DC /\n230 V AC\n500 W", FS)
        text(d, (20, 6.2), "DC+", SMALL)
        text(d, (20, 1.8), "DC−", SMALL)
        wire(d, (20, 1.5), (20, -2))
        text(d, (19.2, 7), "16 mm²", SMALL)
        for y, name in ((5.5, "L"), (4, "N"), (2.5, "PE")):
            wire(d, (23.5, y), (25.5, y))
            d.add(elm.Dot(open=True).at((25.5, y)))
            text(d, (25.95, y), name, SMALL, halign="left")
        text(d, (24.5, 6.4), "230 V AC", SMALL)

        # 12 V spotřebiče na výstupu LOAD
        d.add(elm.FuseIEC().at((7, 0)).down().length(2).label("F4\n10 A", loc="top", ofst=0.3))
        wire(d, (7, -2), (7, -3.5))
        d.add(elm.Dot().at((7, -3.5)))
        wire(d, (4.5, -3.5), (7, -3.5))
        d.add(elm.Lamp().at((4.5, -3.5)).down().length(3).label("E1\nLED", loc="top", ofst=0.3))
        d.add(elm.Lamp().at((7, -3.5)).down().length(3).label("E2\nLED", loc="bottom", ofst=0.3))
        wire(d, (4.5, -6.5), (9, -6.5))
        d.add(elm.Dot().at((7, -6.5)))
        wire(d, (9, 0), (9, -6.5))
        text(d, (9.5, -4.5), "2,5 mm²", SMALL, halign="left")

        text(d, (11, 12.3), "Ostrovní FV systém 12 V — 2× 100 Wp v sérii, MPPT, LiFePO4 100 Ah, střídač 500 W", 12)
        text(d, (11, 11.6), "orientační schéma pro pochopení principu, ne realizační projekt", SMALL)
        text(d, (17, -4.2),
             "Pořadí zapojení: 1) baterie → A1   2) FV → A1   3) spotřebiče\n"
             "Odpojení v opačném pořadí: nejdřív Q1 (FV), Q2 (baterie) naposled.\n"
             "F1 co nejblíž ke kladnému pólu GB1. Průřezy orientační pro trasy do ~1,5 m.",
             SMALL, halign="left", valign="top")

        d.save(out_base + ".svg")
        d.save(out_base + ".png", dpi=200)


if __name__ == "__main__":
    draw(sys.argv[1] if len(sys.argv) > 1 else "solar-offgrid-12v-schema")
