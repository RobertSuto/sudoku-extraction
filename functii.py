import cv2 as cv
import numpy as np




def gray_treshold(img):
    imagine_blur = cv.GaussianBlur(img, (5, 5), 1)
    treshold_image = cv.adaptiveThreshold(imagine_blur, 255, 1, 1, 11, 2)
    return treshold_image

def treshold(img):
    imagine_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    imagine_blur = cv.GaussianBlur(imagine_gray, (5, 5), 1)
    treshold_image = cv.adaptiveThreshold(imagine_blur, 255, 1, 1, 11, 2)
    return treshold_image

def contur_mare(contours):
    mare = np.array([])
    max = 0
    for i in contours:
        area = cv.contourArea(i)
        if area > 50:
            perimetru = cv.arcLength(i, True)
            colturi = cv.approxPolyDP(i, 0.02*perimetru, True)
            if area > max and len(colturi) == 4:
                mare = colturi
                max = area
    return mare, max

def reorder(puncte):
    puncte = puncte.reshape((4,2))
    puncte_noi = np.zeros((4,1,2), dtype = np.int32)
    add = puncte.sum(1)
    puncte_noi[0] = puncte[np.argmin(add)]
    puncte_noi[3] = puncte[np.argmax(add)]
    diff = np.diff(puncte, axis = 1)
    puncte_noi[1] = puncte[np.argmax(diff)]
    puncte_noi[2] = puncte[np.argmin(diff)]
    return puncte_noi

def patratele(img):
    coloane = np.vsplit(img,9) #despartim imaginea in 9 parti egale
    casute = []
    #parcurgem liniile si le splituim in 9 dupa coloane pentru a gasi de la stanga la dreapta
    # si de sus in jos casutele
    # impartirea la 9 ar trebui sa fie buna din moment ce un sudoku este 9/9 iar rezolutiile redimensionarii sunt 540 (multiplu de 9)
    for i in coloane:
        randuri = np.hsplit(i,9)
        for casuta in randuri:
            casute.append(casuta)
    return casute

