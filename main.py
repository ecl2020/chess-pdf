import re
# italic, bold, wrapCenter
from latex_commands import *
# parseComments(moves), parseMoves(moves)
from parsePGN import *


def showGame(game):
    newgame = "\\newgame\\mainline{"
    moves = getLine(game, "Moves ")
    movelist = parseMoves(moves)
    variationlist = parseComments(moves)[1]
    for i in range(0, len(movelist)):
        black = False
        if variationlist.get(str(i)):
            newgame += "}\\par\n\\variation[invar]{" + f"{i}."
            if not re.search(" [BKNQRa-h]", variationlist.get(str(i))[0]):
                black = True
            if black:
                newgame += ".."
            for j in range(0, len(variationlist.get(str(i)))):
                if j > 0:
                    newgame += f"{i + j}."
                newgame += variationlist.get(str(i))[j] + " "
            newgame += "}\\par\n \\mainline[outvar]{ "
        newgame += f"{i+1}."
        if i != 0 and i % 8 == 0:
            newgame += movelist[i] + "}" + wrap("\\showboard\n", "center") + \
                       "\\mainline{"
        else:
            newgame += movelist[i] + " "
    newgame += "}"
    return newgame


def setTitle(game):
    players = bold(getLine(game, "White ") +
                   " -- " +
                   getLine(game, "Black "))
    location = italic(getLine(game, "Site "))
    opening = getLine(game, "Opening ") + "\n"
    return players + "\\\\" + location + "\\\\" + opening


def getLine(game, key):
    with open(game, "r") as game:
        if key == "Moves ":
            return game.readlines()[-3]
        for line in game:
            if key in line:
                return line[re.search(' \"', line).end(): -3]
    return "Unknown"


def setDocument(address, game):
    with address as file:
        file.write(
            "\\documentclass[10pt, twocolumn]{article}\n" +
            "\\usepackage[utf8]{inputenc}\n" +
            "\\usepackage{xskak, caption, graphicx, multicol}\n" +
            "\\usepackage[margin=1in]{geometry}\n" +
            "\\setlength{\\parskip}{0.5em}\n" +
            "\\setlength{\\parindent}{0pt}\n" +
            "\\begin{document}\n" +
            wrap(setTitle(game), "center") +
            showGame(game) +
            "\\end{document}\n"
        )


pgn = "./game.txt"
output = open("./chess-game.tex", "w")
setDocument(output, pgn)

output.close()
