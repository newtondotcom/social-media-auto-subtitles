second_colors = ["&H00FFFFFF","&H00FF0000","&H0000FF00"]
rotation = ["0.00","7.00","-7.00"]

def gen_styles():
    styles = []
    count = 0
    for i in second_colors:
        for j in rotation:
            style = "Style: s" + str(count) + ", Arial, 21, " + i + ", &H000000FF, &H00000000, &H80000000, -1, 0, 0, 0, 100, 100, 0, " + j + ", 1, 3, 4, 3, 30, 30, 30, 0, 2\n"
            styles.append(style)
            count += 1
    return styles