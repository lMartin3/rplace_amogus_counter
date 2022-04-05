from PIL import Image
import csv
import matplotlib.pyplot as plt
import numpy as np

patterns = []
totalPixels = 0
totalCount = 0
amongUsColors = dict()

class Pattern:
    def __init__(self, body, visor, delimitator, visorLimit):
        self.body = body
        self.visor = visor
        self.delimitator = delimitator
        self.visorLimit = visorLimit

def isInBound(x, y):
    return x>=0 and x<2000 and y>=0 and y<2000

def checkPattern(arr, x, y, pat : Pattern):
    global totalCount
    global totalPixels
    r, g, b = arr[x, y]
    bodyColor = [r, g, b]
    visorColor = None
    for pix in pat.body:
        if not isInBound(x+pix[0], y+pix[1]): return False
        pr, pg, pb = arr[x+pix[0], y+pix[1]]
        pColor = [pr, pg, pb]
        if pColor != bodyColor:
            return False

    for pix in pat.visor:
        if not isInBound(x+pix[0], y+pix[1]): return False
        pr, pg, pb = arr[x+pix[0], y+pix[1]]
        pColor = [pr, pg, pb]
        if visorColor is None:
            visorColor = pColor
        else:
            if pColor != visorColor:
                return False
            if visorColor == bodyColor:
                return False
            
    for pix in pat.visor:
        if not isInBound(x+pix[0], y+pix[1]): return False
        pr, pg, pb = arr[x+pix[0], y+pix[1]]
        pColor = [pr, pg, pb]
        if pColor == bodyColor:
            return False
    

    for pix in pat.delimitator:
        if not isInBound(x+pix[0], y+pix[1]): return False
        pr, pg, pb = arr[x+pix[0], y+pix[1]]
        pColor = [pr, pg, pb]
        if pColor == bodyColor:
            return False

    for pix in pat.visorLimit:
        if not isInBound(x+pix[0], y+pix[1]): return False
        pr, pg, pb = arr[x+pix[0], y+pix[1]]
        pColor = [pr, pg, pb]
        if pColor == visorColor or pColor == bodyColor:
            return False
    
    key = '#%02x%02x%02x' % (r, g, b)
    currentCount = 0
    if key in amongUsColors.keys():
        currentCount = amongUsColors[key]
    amongUsColors[key] = currentCount+1
    totalCount = totalCount +1
    totalPixels = totalPixels + len(pat.body) + len(pat.visor)
    return True

def checkAmogusPatterns(arr, x, y):
    for i in range (0, len(patterns)):
        pat : Pattern = patterns[i]
        if checkPattern(arr, x, y, pat):
            return True
    return False

def main():
    # Tall among us facing right
    patterns.append(Pattern(
        [[0, 0], [1, 0], [2, 0], [0, 1], [0, 2], [1, 2], [2, 2], [0, 3], [1, 3], [2, 3], [0, 4], [2, 4]],
        [[1, 1], [2, 1]],
        [[-1, 3], [-1, 4], [1, 4]],
        [[3, 1]]))

    # Tall among us facing left
    patterns.append(Pattern(
        [[0, 0], [1, 0], [2, 0], [2, 1], [0, 2], [1, 2], [2, 2], [0, 3], [1, 3], [2, 3], [0, 4], [2, 4]],
        [[0, 1], [1, 1]],
        [[3, 3], [3, 4], [1, 4]],
        [[-1, 1]]))

    # Short among us facing right
    patterns.append(Pattern(
        [[0, 0], [1, 0], [2, 0], [0, 1], [0, 2], [1, 2], [2, 2], [0, 3], [2, 3]],
        [[1, 1], [2, 1]],
        [[-1, 4], [1, 4]],
        [[3, 1]]))

    # Short among us facing left
    patterns.append(Pattern(
        [[0, 0], [1, 0], [2, 0], [2, 1], [0, 2], [1, 2], [2, 2], [0, 3], [2, 3]],
        [[0, 1], [1, 1]],
        [[3, 4], [1, 4]],
        [[-1, 1]]))
    

    img = Image.open("place_2k.png")
    width, height = img.size
    print("{0}x{1}".format(width, height))
    pix = img.convert("RGB").load()
    print(img.mode)
    for y in range(0, height):
        for x in range(0, width):
            r, g, b = pix[x, y]
            color = [r, g, b]
            if(checkAmogusPatterns(pix, x, y)):
                print("FOUND! At {0}, {1}".format(x, y))
            
    print("RESULTS: {0}".format(amongUsColors))
    
    percentages = []
    labels = []
    colors = []

    mappedResults = []
    for key in amongUsColors:
        d = dict()
        d["color"] = key
        d["count"] = amongUsColors[key]
        d["percentage"] = (100 / totalCount) * amongUsColors[key]
        percentages.append(d["percentage"])
        labels.append("{0} ({1})".format(key, d["count"]))
        colors.append(key)
        mappedResults.append(d)


    with open('results.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = ["color", "count", "percentage"])
        writer.writeheader()
        writer.writerows(mappedResults)

    plt.pie(np.array(percentages), labels = labels, colors = colors)
    plt.legend(title = "Colors:",  bbox_to_anchor=(1.5, 1))
    plt.show() 
if __name__=="__main__":
    main()