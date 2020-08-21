def bold(content):
    return "\\textbf{" + \
           content + \
           "}\n"


def italic(content):
    return "\\textit{" + \
           content + \
           "}\n"


def wrapCenter(content):
    return "\\begin{center}\n" + \
           content + \
           "\\end{center}\n"
