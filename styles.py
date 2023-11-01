second_colors = ["&H00FFFFFF","&H00FFFFFF","&H00FFFFFF","&H0000FF00","&H00FF0000","&H0000FF00","&H000000FF"]
rotation = ["0.00","7.00","-7.00","0.00","0.00","0.00","0.00"]
scales = ["100","110","90","100","100","100","100"]

def gen_styles():
    styles = []
    count = 0
    for i in second_colors:
        for j in rotation:
            for k in scales:
                for l in scales:
                    style = "Style: s" + str(count) + ", Arial, 22, " + i + ", &H0000FF00, &H00000000, &H00000000, -1, 0, 0, 0,"+k+","+l+", 0, " + j + ", 1, 3, 4, 3, 0, 0, 10, 0, 2\n" #30, 30, 30
                    styles.append(style)
                    count += 1
    return styles