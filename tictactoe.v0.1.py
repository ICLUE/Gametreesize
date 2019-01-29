# Tic Tac Toe Importance Sampling Estimator
# Code for "An estimation method for game complexity"
# By Alexander Yong and David Yong @ Urbana, Illinois
# January 28, 2019

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
	y=[["_","_","_"],
           ["_","_","_"],
	   ["_","_","_"]]
	import numpy as np
	z=np.reshape(y,(3,3))
	return z;

def makemove(theposition,rownum, colnum, tomove):
	
	newpos=copy.deepcopy(theposition)
	if(theposition[rownum,colnum]=="_"):
		newpos[rownum,colnum]=tomove
	else:
		return -911
	return newpos;

def randommove(theposition, tomove):

	movelist=[]
	for ii in range (0,3):
		for jj in range (0,3):
			if(theposition[ii,jj]=="_"):
				movelist.append([ii,jj])
	
	randval=random.randint(0,len(movelist)-1)
	themovewemake=movelist[randval]
	anothertemppos=copy.deepcopy(theposition)
	finalanswer=makemove(anothertemppos,themovewemake[0], themovewemake[1],tomove)
	morefinalpos=copy.deepcopy(finalanswer)
	return [morefinalpos, len(movelist)]
		
def checkgameended(thepos, tomove):

	if(thepos[0,0]==str(tomove) and thepos[0,1]==str(tomove) and thepos[0,2]==str(tomove)):
		return tomove
        if(thepos[1,0]==str(tomove) and thepos[1,1]==str(tomove) and thepos[1,2]==str(tomove)):
		return tomove
        if(thepos[2,0]==str(tomove) and thepos[2,1]==str(tomove) and thepos[2,2]==str(tomove)):
		return tomove
        if(thepos[0,0]==str(tomove) and thepos[1,0]==str(tomove) and thepos[2,0]==str(tomove)):
		return tomove
        if(thepos[0,1]==str(tomove) and thepos[1,1]==str(tomove) and thepos[2,1]==str(tomove)):
		return tomove
        if(thepos[0,2]==str(tomove) and thepos[1,2]==str(tomove) and thepos[2,2]==str(tomove)):
		return tomove
        if(thepos[0,0]==str(tomove) and thepos[1,1]==str(tomove) and thepos[2,2]==str(tomove)):
		return tomove
        if(thepos[2,0]==str(tomove) and thepos[1,1]==str(tomove) and thepos[0,2]==str(tomove)):
		return tomove

	blankfound=0
	for ii in range(0,3):
		for jj in range(0,3):
			if(thepos[ii,jj]=="_"):
				blankfound=1

	if(blankfound<>0):
		return -2

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

        print("* Estimated number of games of Tic Tac Toe is", float(averageestimate))

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

	while con == 1:
		randommovepos=copy.deepcopy(thepos)
		tempans=randommove(thepos,tomove)
		thepos=copy.deepcopy(tempans[0])
		estimate=estimate*tempans[1]
		gamelength=gamelength+1
		flag=0

		whowon=checkgameended(thepos, tomove)
		if whowon<>-2:
			con=0

		if tomove==0:
			tomove=1
		else:
			tomove=0

	return(estimate,whowon, gamelength)

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
