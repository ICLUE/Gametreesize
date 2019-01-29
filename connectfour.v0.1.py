# Connect 4 program: Importance Sampling Estimator v0.1
# Code for "An estimation method for game complexity"
# By Alexander Yong and David Yong @ Urbana, Illinois 
# January 29, 2019

import random
import math
import time
import sys
import copy
import multiprocessing

bigtotal=0
firstwintotal=0
secondwintotal=0
drawtotal=0
totalgamelength=0

def main():
        sampleval=int(input('Sample size : '))
	numberofprocessors=int(input('Number of processor cores to use (0 if you want to use all) : '))
        print("Sample size; cores used", sampleval, numberofprocessors)
        theans=actualestimator(sampleval, numberofprocessors)

def startingposition():
	y=[["_","_","_","_","_","_","_"],
           ["_","_","_","_","_","_","_"],
	   ["_","_","_","_","_","_","_"],
	   ["_","_","_","_","_","_","_"],
           ["_","_","_","_","_","_","_"],
	   ["_","_","_","_","_","_","_"],
	   ["0","1","2","3","4","5","6"]]
	import numpy as np
	z=np.reshape(y,(7,7))
	return z;

def makemove(theposition,columnnum,tomove):
	
	newpos=copy.deepcopy(theposition)
	if(theposition[5,columnnum]=="_"):
		newpos[5,columnnum]=tomove
	elif(theposition[4,columnnum]=="_"):
		newpos[4,columnnum]=tomove
	elif(theposition[3,columnnum]=="_"):
		newpos[3,columnnum]=tomove
	elif(theposition[2,columnnum]=="_"):
                newpos[2,columnnum]=tomove
	elif(theposition[1,columnnum]=="_"):
                newpos[1,columnnum]=tomove
	elif(theposition[0,columnnum]=="_"):
                newpos[0,columnnum]=tomove
	else:
		return -911
	return newpos;

def randommove(theposition, tomove):

	movelist=[]
	for columnnum in range (0,7):
		if(theposition[5,columnnum]=="_"):
			movelist.append(columnnum)
		elif(theposition[4,columnnum]=="_"):
			movelist.append(columnnum)
		elif(theposition[3,columnnum]=="_"):
			movelist.append(columnnum)
		elif(theposition[2,columnnum]=="_"):
			movelist.append(columnnum)
		elif(theposition[1,columnnum]=="_"):
			movelist.append(columnnum)
		elif(theposition[0,columnnum]=="_"):
			movelist.append(columnnum)
	
	randval=random.randint(0,len(movelist)-1)
	themovewemake=movelist[randval]
	anothertemppos=copy.deepcopy(theposition)
	finalanswer=makemove(anothertemppos,themovewemake,tomove)
	morefinalpos=copy.deepcopy(finalanswer)
	return [morefinalpos, len(movelist)]
		
def checkgameended(theposition, tomove):

	rowwin=0
	# check if there are 4 in a row
	for rowval in range(0,6):
		for colval in range(0,4):
			sttm=str(tomove)
			if(theposition[rowval,colval]==sttm and theposition[rowval,colval+1]==sttm and theposition[rowval,colval+2]==sttm and theposition[rowval,colval+3]==sttm):
				return tomove

	# check if there are 4 in a column
	for colval in range(0,7):
		for rowval in range(0,3):
			sttm=str(tomove)
			if(theposition[rowval,colval]==sttm and theposition[rowval+1,colval]==sttm and theposition[rowval+2,colval]==sttm and theposition[rowval+3,colval]==sttm):
				return tomove

	# check if there is a 4 - NW to SE diagonal 
	for rowval in range(0,3):
		for colval in range(0,4):
			sttm=str(tomove)
			if(theposition[rowval,colval]==sttm and theposition[rowval+1,colval+1]==sttm and theposition[rowval+2,colval+2]==sttm and theposition[rowval+3,colval+3]==sttm):
				return tomove

	# check if there is a 4 - SW to NE diagonal
	for rowval in range(3,6):
		for colval in range(0,4):
			sttm=str(tomove)	
			if(theposition[rowval,colval]==sttm and theposition[rowval-1,colval+1]==sttm and theposition[rowval-2,colval+2]==sttm and theposition[rowval-3,colval+3]==sttm):
                                return tomove

	# check if the board is filled (and no win has occurred, hence draw)
	for rowval in range(0,6):
		for colval in range(0,7):
			if(theposition[rowval,colval]=="_"):
				return -99

	return -1;

def actualestimator(samplevalin, numberofprocessors, seed=None):

        global totalgamelength
        global bigtotal
        global firstwintotal
        global secondwintotal
        global drawtotal

        start=time.time()

        if seed is not None:
                random.seed(seed)

	if(numberofprocessors==0):
        	num_workers = multiprocessing.cpu_count()
	else:
		num_workers=numberofprocessors

        sampleval=samplevalin

        while sampleval > 100000:
                pool=multiprocessing.Pool(num_workers)
                for i in range(100000):
                        a = pool.apply_async(run_trial, args=(), callback=process_result)
                pool.close()
                pool.join()
                sampleval -= 100000
        pool = multiprocessing.Pool(num_workers)
        for i in range(sampleval):
                a = pool.apply_async(run_trial, args=(), callback=process_result)
        pool.close()
        pool.join()

        print("--------------------------------------")
        print("            RESULTS                   ")
        print("--------------------------------------")

        averageestimate=bigtotal/float(samplevalin)
        sumofgamelengths=totalgamelength/float(samplevalin)
        drawtotal=drawtotal/float(samplevalin)
        firstwintotal=firstwintotal/float(samplevalin)
        secondwintotal=secondwintotal/float(samplevalin)

        print("* Estimated number of games of Connect Four is", float(averageestimate))

        estgamelength=sumofgamelengths/averageestimate
        print("* Estimated average game length is ", float(estgamelength))

        estfirstwinpercent=firstwintotal/float(averageestimate)
        print("* Estimated percentage of first player wins is ", estfirstwinpercent)

        estsecondwinpercent=secondwintotal/float(averageestimate)
        print("* Estimated percentage of second player wins is ", estsecondwinpercent)

        estdrawpercent=drawtotal/float(averageestimate)
	print("* Estimated percentage of draws is ", estdrawpercent)

        end=time.time()
        print('Executed in seconds: ', end - start)

def run_trial():
        z=startingposition()
        thepos=z
        tomove=0
        con=1
        estimate=1
        gamelength=0
        gameended=0

        while con == 1:
		randommovepos=copy.deepcopy(thepos)
		tempans=randommove(thepos,tomove)
		thepos=copy.deepcopy(tempans[0])
		estimate=estimate*tempans[1]
		gamelength=gamelength+1

		gameended=checkgameended(thepos,tomove)

		if gameended==0:
			con=0
                if gameended==1:
			con=0
                if gameended==-1:
			con=0

                if tomove==0 and con==1:
                        tomove=1
                else:
                        tomove=0

	return(estimate,gameended, gamelength)

def process_result(thepair):

        global totalgamelength
        global bigtotal
        global firstwintotal
        global secondwintotal
        global drawtotal

        estimate=thepair[0]
        thewinner=thepair[1]
        thelength=thepair[2]
        bigtotal=float(bigtotal+estimate)

        totalgamelength = float(totalgamelength+thelength*estimate)

        if(thewinner==0):
                firstwintotal=float(firstwintotal+estimate)

        if(thewinner==1):
                secondwintotal=float(secondwintotal+estimate)

        if(thewinner==-1):
                drawtotal=float(drawtotal+estimate)

if __name__ == '__main__':
	main()
