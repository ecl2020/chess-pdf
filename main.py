import berserk
import re


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
            wrapCenter(setTitle(game)) +
            showGame(game) +
            "\\end{document}\n"
        )


def wrapCenter(content):
    return "\\begin{center}\n" + \
           content + \
           "\\end{center}\n"


def showGame(game):
    newgame = "\\newgame\\mainline{"
    moves = getLine(game, "Moves ")
    movelist = re.split("\\d+\\.", moves)
    for i in range(1, len(movelist)):
        newgame += f"{i}" + "."
        if i % 10 == 0:
            newgame += movelist[i] + "}" + wrapCenter("\\showboard\n") + \
                "\\mainline{"
        else:
            newgame += movelist[i]
    newgame += "}"
    return newgame


def setTitle(game):
    players = "\\textbf{" + \
              getLine(game, "White ") + \
              " -- " + \
              getLine(game, "Black ") + \
              "}\n"
    location = "\\textit{" + \
               getLine(game, "Site ") + \
               "}\n"
    opening = getLine(game, "Opening ") + "\n"
    return players + location + "\\\\" + opening


def getLine(game, key):
    with open(game, "r") as game:
        if key == "Moves ":
            return game.readlines()[-3]
        for line in game:
            if key in line:
                return line[re.search(' \"', line).end(): -3]
    return "Unknown"


pgn = "./game.txt"
output = open("./chess-game.tex", "w")
setDocument(output, pgn)

output.close()
