import re


def parseComments(moves):
    variations = {}
    # finding random characters because of the awkward arrows
    comments = re.findall("{[A-z0-9-., %:$#â†’\\(\\)\\+]+}|\\([,A-z0-9$#â†’ .\\+]+\\)", moves)
    skips = re.findall("\\d+\\.\\.\\.", moves)
    for comment in comments:
        if comment[0] == "(":
            variation = comment[1:-1]
            variations.update({variation[0:variation.find(".")]: parseMoves(variation)})
        moves = moves.replace(comment, '')
    for skip in reversed(skips):
        moves = moves.replace(skip, '')
    return [moves, variations]


def parseMoves(moves):
    if "{" in moves or "(" in moves:
        moves = parseComments(moves)[0]
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
