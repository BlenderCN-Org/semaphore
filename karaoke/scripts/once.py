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

'''
Ce script est appelé par main_init.main dans blender
Il ne tourne qu'une seule fois pour initier lss variables
qui seront toutes des attributs du bge.logic (gl)
Seuls les attributs de logic sont stockés en permanence.
'''


from bge import logic as gl

from pymultilame import blendergetobject
from pymultilame import Tempo, MyConfig, MyTools
from pymultilame import UdpClient


def get_conf():
    '''Récupère la configuration depuis le fichier *.ini.'''

    # Le dossier courrant est le dossier dans lequel est le *.blend
    current_dir = gl.expandPath("//")
    print("Dossier courant depuis once.py {}".format(current_dir))
    gl.once = 0

    # TODO: trouver le *.ini en auto
    gl.ma_conf = MyConfig(current_dir + "scripts/bgb.ini")
    gl.conf = gl.ma_conf.conf

    print("\nConfiguration du jeu bgb:")
    print(gl.conf, "\n")

def set_tempo():
    tempo_liste = [ ("toto", 60),
                    ("frame", 999999999999)]

    # Comptage des frames par lettre
    gl.tempoDict = Tempo(tempo_liste)

def set_network():
    gl.data = ""
    gl.clt = UdpClient()

def get_karoke_objet():
    all_obj = blendergetobject.get_all_objects()
    gl.text_obj = all_obj['Text.001']
    gl.text_obj.resolution = 64


def main():
    '''Lancé une seule fois à la 1ère frame au début du jeu par main_once.'''

    print("Initialisation des scripts lancée un seule fois au début du jeu.")

    # Récupération de la configuration
    get_conf()

    set_tempo()
    set_network()
    get_karoke_objet()
    # Pour les mondoshawan
    print("OK des mondoshawan")
