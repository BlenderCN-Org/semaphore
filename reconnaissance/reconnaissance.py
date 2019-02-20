#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

########################################################################
# This file is part of Semaphore.
#
# Semaphore is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Semaphore is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
########################################################################

import os
import numpy as np
import cv2


def sigmoid(x):
    """La fonction sigmoïde est une courbe en S:
    https://fr.wikipedia.org/wiki/Sigmo%C3%AFde_(math%C3%A9matiques)
    """

    return 1 / (1 + np.exp(-x))

def relu(x):
    """Rectifie les négatifs à 0:
    -1 > 0
     1 > 1
     Rectified Linear Unit:

    In the context of artificial neural networks, the rectifier is an
    activation function defined as the positive part of its argument.
    https://bit.ly/2HyT4ZO sur Wikipedia en.
     """

    return np.maximum(0, x)


class Reconnaissance:

    def __init__(self):
        self.weight = np.load('weights.npy')

    def testing(self, img):
        vecteur_ligne = img
        layers = [1600, 100, 100, 27]
        activations = [relu, relu, sigmoid]

        for k in range(len(layers)-1):
            vecteur_ligne = activations[k](np.dot(self.weight[k],
                                                       vecteur_ligne))

            reconnu = np.argmax(vecteur_ligne)
        return reconnu


def webcam(c):
    cap = cv2.VideoCapture(c)
    loop = 1
    reco = Reconnaissance()
    while loop:
        rep, frame = cap.read()

        if rep:
            cv2.imshow('Image', frame)

            # hsv
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower = np.array([122, 90, 90])  # [125,75, 145]

            upper = np.array([255, 255, 255])
            mask = cv2.inRange(hsv, lower, upper)

            # Resize
            img = cv2.resize(mask, (40, 40), interpolation=cv2.INTER_AREA)

            # Flou
            img = cv2.blur(img, (6, 6))

            # Noir et blanc, sans gris
            ret, nb = cv2.threshold(img, 2, 255, cv2.THRESH_BINARY)


            # Resize pour affichage seul
            big = cv2.resize(nb, (600, 600), interpolation=cv2.INTER_AREA)
            cv2.imshow('Final', big)

            # Reshape pour avoir un vecteur ligne
            vect = nb.reshape(40*40)

            k = cv2.waitKey(33)
            # Echap
            if k == 27:
                loop = 0
            # Espace
            elif k == 32:
                reconnu = reco.testing(vect)
                print("Caractère reconnu:", reconnu)

    cv2.destroyAllWindows()

if __name__ == "__main__":
    # 0 = numéro de cam
    webcam(0)
