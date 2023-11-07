rotation = ["0.00","7.00","-7.00","0.00","0.00","0.00","0.00"]
scales = ["100","110","90","100","100","100","100"]

letters_color = [["&H00FFFFFF",1],["&H00FFFFFF",1]]

def gen_styles():
    styles = []
    count = 0
    for i in letters_color:
        for l in range(i[1]):
            for j in rotation:
                for k in scales:
                    for l in scales:
                        style = "Style: s" + str(count) + ", Arial, 22, " + i[0] + ", &H0000FF00, 1 , &H00000000 , -1, 0, 0, 0,"+k+","+l+", 0, " + j + ", 1, 3 , 4, 3, 0, 0, 50, 0, 2\n" #30, 30, 30
                        styles.append(style)
                        count += 1
    return styles


##Alignment values are based on the numeric keypad layout. {\an1} - bottom left, {\an2} - bottom center, {\an3} - bottom right, {\an4} - center left, {\an5} - center center, {\an6} - center right, {\an7} - top left, {\an8} - top center, {\an9} - top right.