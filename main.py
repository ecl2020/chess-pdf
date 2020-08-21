import re
# italic, bold, wrapCenter
from latex_commands import *


def showGame(game):
    newgame = "\\newgame\\mainline{"
    moves = getLine(game, "Moves ")
    movelist = parseMoves(moves)
    for i in range(0, len(movelist)):
        newgame += f"{i+1}" + "."
        # print("adding move ", i, ": ", movelist[i])
        if i != 0 and i % 8 == 0:
            newgame += movelist[i] + "}" + wrapCenter("\\showboard\n") + \
                       "\\mainline{"
        else:
            newgame += movelist[i] + " "
    newgame += "}"
    return newgame


def parseComments(moves):
    variations = []
    # finding random characters because of the awkward arrows
    comments = re.findall("{[A-z0-9-., %:$#â†’\\(\\)\\+]+}|\\([,A-z0-9$#â†’ .\\+]+\\)", moves)
    skips = re.findall("\\d+\\.\\.\\.", moves)
    for comment in comments:
        if comment[0] == "(":
            variation = comment[1:-1]
            variations.append([variation[0:variation.find(".")],
                               parseMoves(variation)])
        moves = moves.replace(comment, '')
    for skip in reversed(skips):
        moves = moves.replace(skip, '')
    # print(variations)
    return moves


def parseMoves(moves):
    if "{" in moves or "(" in moves:
        moves = parseComments(moves)
    movelist = []
    move_nos = re.finditer("\\d+\\.+ ", moves, flags=0)
    for index in move_nos:
        restofstring = moves[index.end():]
        if re.search("\\d+\\.+ ", restofstring):
            movelist.append(moves[index.end():moves.find(".", index.end())])
        else:
            movelist.append(moves[index.end():])
    for i in range(0, len(movelist)):
        if re.search(" \\d+$", movelist[i]):
            movelist[i] = movelist[i][0:re.search(" \\d+$", movelist[i]).start()]
    return movelist


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
            wrapCenter(setTitle(game)) +
            showGame(game) +
            "\\end{document}\n"
        )


pgn = "./game.txt"
output = open("./chess-game.tex", "w")
setDocument(output, pgn)

output.close()
