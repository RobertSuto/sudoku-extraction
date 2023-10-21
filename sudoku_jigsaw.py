import cv2 as cv
import numpy as np
from functii import *
from  functools import cmp_to_key
import os

def sudoku_jigsaw(image_path):
    save_path = 'evaluare\\fisiere_solutie\\Suto_Robert_311\\jigsaw'

    file_name = os.path.join(save_path, image_path[-6:-4] + '_predicted.txt')
    file_name2 = os.path.join(save_path, image_path[-6:-4] + '_bonus_predicted.txt')

    f = open(file_name, 'w+')
    f2 = open(file_name2, 'w+')
    # preparing image
    # dupa cum am vazut in setul de jigsaw, poza 17 era prea in margine asa ca am adaugat o margine gri
    # inainte pentru a evita eroarea
    img = cv.imread(image_path)
    img2 = img.copy()
    inaltime_tabla = 540
    latime_tabla = 540
    # preparing image
    # dupa cum am vazut in setul de jigsaw, poza 17 era prea in margine asa ca am adaugat o margine gri
    # inainte pentru a evita eroarea
    top, bottom, left, right = 5, 5, 5, 5
    margine = (201, 203, 202)
    img = cv.copyMakeBorder(img, top, bottom, left, right, cv.BORDER_CONSTANT, value=margine)

    img = cv.medianBlur(img, 31)
    img = cv.medianBlur(img, 7)
    img = cv.medianBlur(img, 5)

    img_treshold = treshold(img)
    img_goala = np.zeros((inaltime_tabla, latime_tabla, 3), np.uint8)

    # contur
    img_contur, img_contur_mare = img.copy(), img.copy()
    contur = cv.findContours(img_treshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
    cv.drawContours(img_contur, contur, -1, (0, 255, 0), 3)
    # gasirea tablei
    mare, maxArea = contur_mare(contur)
    if mare.size != 0:
        mare = reorder(mare)
        cv.drawContours(img_contur_mare, mare, -1, (0, 255, 0), 100)
        pts1 = np.float32(mare)
        pts2 = np.float32([[0, 0], [latime_tabla, 0], [0, inaltime_tabla], [latime_tabla, inaltime_tabla]])
        matrix = cv.getPerspectiveTransform(pts1, pts2)
        tabla_joc = cv.warpPerspective(img, matrix, (latime_tabla, inaltime_tabla))
        img2 = cv.warpPerspective(img2, matrix, (latime_tabla, inaltime_tabla))
        img2 = cv.flip(img2, 0)
        img2 = cv.rotate(img2, cv.ROTATE_90_CLOCKWISE)

        img_deteted_digits = img_goala.copy()
        tabla_joc = cv.flip(tabla_joc, 0)
        tabla_joc = cv.rotate(tabla_joc, cv.ROTATE_90_CLOCKWISE)

        tabla_joc = cv.cvtColor(tabla_joc, cv.COLOR_BGR2GRAY)
        alb_negru = cv.threshold(tabla_joc, 125, 255, cv.THRESH_BINARY)[1]
        tabla_joc = alb_negru.copy()
        img2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
        alb_negru2 = cv.threshold(img2, 125, 255, cv.THRESH_BINARY)[1]

        img2 = cv.blur(img2, (5, 5))
        alb_negru2 = cv.threshold(img2, 125, 255, cv.THRESH_BINARY)[1]
        img2 = alb_negru2.copy()

    tabla_joc = cv.resize(tabla_joc, (latime_tabla, inaltime_tabla))
    numar_dilatari = np.ones((4, 4), np.uint8)
    tabla_joc = cv.dilate(tabla_joc, numar_dilatari, iterations=1)
    tabla_joc = cv.erode(tabla_joc, numar_dilatari, iterations=1)
    tabla_joc = tabla_joc[10:530, 10:530]
    margine = (0, 0, 0)
    top, bottom, left, right = 10, 10, 10, 10
    tabla_joc = cv.copyMakeBorder(tabla_joc, top, bottom, left, right, cv.BORDER_CONSTANT, value=margine)
    colors = [(255, 0, 0), (102, 0, 0), (153, 0, 0), (0, 255, 0), (0, 153, 0), (0, 102, 0),
              (0, 0, 255), (0, 0, 153), (0, 0, 102)]

    contours = cv.findContours(tabla_joc, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)[0]
    contours = sorted(contours, key=lambda x: cv.boundingRect(x)[1] // 10 * 10 * latime_tabla +
                                              cv.boundingRect(x)[0])

    tabla_joc = cv.cvtColor(tabla_joc, cv.COLOR_GRAY2RGB)
    for i, c in enumerate(contours):
        zona = cv.approxPolyDP(c, 0.0002 * cv.arcLength(c, True), True)
        # 0.002 e epsilon
        cv.drawContours(tabla_joc, [zona], -3, colors[i], cv.FILLED)

    patrate = patratele(tabla_joc)
    for i in range(len(patrate)):
        patrate[i] = patrate[i][29:inaltime_tabla // 9 - 29, 29:latime_tabla // 9 - 29]
    tabela = []
    for i in range(len(patrate)):
        (b, g, r) = patrate[i][0, 0]
        tuplu = (b, g, r)
        if tuplu == colors[0]:
            tabela.append('1')
        elif tuplu == colors[1]:
            tabela.append('2')
        elif tuplu == colors[2]:
            tabela.append('3')
        elif tuplu == colors[3]:
            tabela.append('4')
        elif tuplu == colors[4]:
            tabela.append('5')
        elif tuplu == colors[5]:
            tabela.append('6')
        elif tuplu == colors[6]:
            tabela.append('7')
        elif tuplu == colors[7]:
            tabela.append('8')
        elif tuplu == colors[8]:
            tabela.append('9')

    patrate2 = patratele(img2)
    tabela2 = []
    output_list = []
    for i in range(len(patrate2)):
        patrate2[i] = patrate2[i][15:inaltime_tabla // 9 - 15, 15:latime_tabla // 9 - 15]
        contor = 0
        if 0 in patrate2[i]:
            tabela2.append('x')
        else:
            tabela2.append('o')

    if (len(patrate) == len(patrate2)):
        for i in range(len(patrate)):
            output_list.append(tabela[i])
            output_list.append(tabela2[i])

    output_list = [output_list[n:n + 18] for n in range(0, len(output_list), 18)]
    for r in range(len(output_list)):
        s = "".join(output_list[r])
        f.write(s)
        f2.write(s)
        if r != len(output_list) - 1:
            f.write('\n')
            f2.write('\n')
        s = ""
    f.close()
    f2.close()

dir_path = 'testare\\jigsaw\\'
def results_sudoku_jigsaw(dir_path):
    files = os.listdir(dir_path)
    for img_name in files:
        if img_name[-3:] == 'jpg':
            path = dir_path + img_name
        sudoku_jigsaw(path)
results_sudoku_jigsaw(dir_path)




