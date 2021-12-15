import numpy as np 
import time
import os
import sys

def locate_zero(array):
    i=0
    j=0
    while (i<3):
        j=0
        if array[i,j] == 0:
            return [i,j]
        while (j<3):
            if array[i,j] == 0 :
                return [i,j]
            j=j+1
        i=i+1

def apply(m,array):
    zero=locate_zero(array)
    if m=='r':
        temp=array[zero[0],zero[1]+1]
        array[zero[0],zero[1]+1]=0
        array[zero[0],zero[1]]=temp
    if m=='l':
        temp=array[zero[0],zero[1]-1]
        array[zero[0],zero[1]-1]=0
        array[zero[0],zero[1]]=temp
    if m=='u':
        temp=array[zero[0]-1,zero[1]]
        array[zero[0]-1,zero[1]]=0
        array[zero[0],zero[1]]=temp
    if m=='d':
        temp=array[zero[0]+1,zero[1]]
        array[zero[0]+1,zero[1]]=0
        array[zero[0],zero[1]]=temp


        