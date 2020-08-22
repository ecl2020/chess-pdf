def bold(content):
    return "\\textbf{" + \
           content + \
           "}\n"


def italic(content):
    return "\\textit{" + \
           content + \
           "}\n"


def wrap(content, type):
    return "\\begin{" + type + "}" + \
           content + \
           "\\end{" + type + "}\n"
