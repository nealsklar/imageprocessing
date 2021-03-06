"""
Joshua Stough
DIP

Utilities for Haar wavelet decomposition.
"""

import numpy as np
from scipy.linalg import orth

#See DIP 6.9.
def makeHaarMatrix(size=4):
    if not np.log2(size).is_integer():
        raise ValueError('makeHaarMatrix: input must be power of 2 (%d).' % size)

    H = np.zeros((size,size))
    H[0,:] = 1.
    # See the print statements for what took a while to debug.
    for u in range(1, size):
        # print('working row ' + str(u))
        mag = 2 ** np.floor(np.log2(u)).astype('int')
        howmany = size//(2*mag)
        # print('\tmag is %d, howmany is %d...' % (mag, howmany))


        row = howmany*[np.sqrt(mag)] + howmany*[-np.sqrt(mag)] + (size-2*howmany)*[0]
        # print('\trow to roll is ' + str(row))
        # print('\twill roll by ' + str(u%mag))

        nrow = np.array(row)

        H[u,:] = np.roll(nrow, 2*howmany*(u%mag))

    H = H/np.sqrt(size)

    return H

#Make random basis until it succeeds.
def makeRandomBasis(size=4):
    BP = np.random.rand(size,size)
    BN = orth(BP)
    if (BN.shape[1] != size):
        return makeRandomBasis(size)
    return BN

"""
Karhunen Loeve Transform version: basically principal components on the
image samples, would give the "best" representation for the provided
image. To be compatible with the wavelet decomposition examples that 
use this module, I'm returning the size x size sort-of transform matrix:
that is, I'm doing PCA on the size x 1 samples in the image and not the 
size x size patches in the image.
Assumes both sides of the provided image are divisible by size.
http://nbviewer.jupyter.org/github/sukhbinder/Notebooks/blob/master/Karhunen%20Loeve%20Transform.ipynb
https://docs.scipy.org/doc/numpy/reference/generated/numpy.linalg.eig.html
https://docs.scipy.org/doc/numpy/reference/generated/numpy.cov.html
"""
def makeKLTBasis(I, size=4):
    Ishape = I.shape
    #Get size x whatever samples.
    colSamples = np.reshape(I, (size, -1), order='F')
    if (len(I.shape) == 3):
        rowSamples = np.reshape(I.transpose((1, 0, 2)), (size,-1), order='F')
    else:
        rowSamples = np.reshape(I.transpose(), (size, -1), order='F')
    allSamples = np.concatenate((colSamples, rowSamples), axis = 1)

    # every column of allSamples represents an observation.
    val, vec = np.linalg.eig(np.cov(allSamples, rowvar=True))

    # Make sure the eigenvectors are sorted in decreasing order of importance.
    vecsorted = vec[:, np.argsort(val)[-1::-1]]

    return vecsorted.T


def makeDCTMatrix(size=4):
    D = np.zeros((size, size))
    x = np.arange(size)
    D[0,:] = np.sqrt(1/size)
    for u in range(1,size):
        D[u,:] = np.sqrt(2/size)*np.cos(((2*x+1)*u*np.pi)/(2*size))
    return D

# For completeness
def makeStandardMatrix(size=4):
    return np.eye(size)