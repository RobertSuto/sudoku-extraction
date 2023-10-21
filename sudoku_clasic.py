import cv2 as cv
import numpy as np
from functii import *
import os


def sudoku_clasic(image_path):
    save_path = 'evaluare\\fisiere_solutie\\Suto_Robert_311\\clasic'

    file_name = os.path.join(save_path, image_path[-6:-4] + '_predicted.txt')
    file_name2 = os.path.join(save_path, image_path[-6:-4] + '_bonus_predicted.txt')

    f = open(file_name, 'w+')
    f2 = open(file_name2, 'w+')
    inaltime_tabla = 540
    latime_tabla = 540
    # preparing image
    # dupa cum am vazut in setul de jigsaw, poza 17 era prea in margine asa ca am adaugat o margine gri
    # inainte pentru a evita eroarea
    img = cv.imread(image_path)

    top, bottom, left, right = 5, 5, 5, 5
    margine = (201, 203, 202)
    img = cv.copyMakeBorder(img, top, bottom, left, right, cv.BORDER_CONSTANT, value=margine)
    img_goala = np.zeros((inaltime_tabla, latime_tabla, 3), np.uint8)
    img_treshold = treshold(img)

    #contur
    img_contur, img_contur_mare = img.copy(), img.copy()
    contur, hierarchy = cv.findContours(img_treshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(img_contur, contur, -1, (0,255,0), 3)

    #gasirea tablei
    mare, maxArea = contur_mare(contur)
    if mare.size !=0:
        mare = reorder(mare)
        cv.drawContours(img_contur_mare,mare,-1,(0,255,0), 100)
        pts1 = np.float32(mare)
        pts2 = np.float32([[0,0], [latime_tabla,0], [0,inaltime_tabla],[latime_tabla,inaltime_tabla]])
        matrix = cv.getPerspectiveTransform(pts1,pts2)
        tabla_joc = cv.warpPerspective(img,matrix,(latime_tabla, inaltime_tabla))
        img_deteted_digits = img_goala.copy()
        tabla_joc = cv.flip(tabla_joc, 0)
        tabla_joc = cv.rotate(tabla_joc, cv.ROTATE_90_CLOCKWISE)
        tabla_joc = cv.cvtColor(tabla_joc, cv.COLOR_BGR2GRAY)
        alb_negru = cv.threshold(tabla_joc, 128, 255, cv.THRESH_BINARY)[1]
        tabla_joc = alb_negru.copy()
        tabla_joc = cv.GaussianBlur(tabla_joc, (5, 5), 0)
        tabla_joc = cv.threshold(tabla_joc, 128, 255, cv.THRESH_BINARY)[1]


    tabla_joc = cv.resize(tabla_joc, (latime_tabla, inaltime_tabla))
    patrate = patratele(tabla_joc)
    tabela = []
    for i in range(len(patrate)):
        patrate[i] = patrate[i][10:inaltime_tabla//9-10,10:latime_tabla//9-10]
        if 0 in patrate[i]:
            tabela.append('x')
        else:
            tabela.append('o')

    output_list = [tabela[n:n+9] for n in range(0, len(tabela), 9)]
    for r in range(len(output_list)):

        s = "".join(output_list[r])
        f.write(s)
        f2.write(s)
        if r != len(output_list)-1:
            f.write('\n')
            f2.write('\n')
        s = ""

    f.close()
    f2.close()

dir_path = 'testare\\clasic\\'
def results_sudoku_clasic(dir_path):
    files = os.listdir(dir_path)
    for img_name in files:
        if img_name[-3:] == 'jpg':
            path = dir_path + img_name
        sudoku_clasic(path)
results_sudoku_clasic(dir_path)