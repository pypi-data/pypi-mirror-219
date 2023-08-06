#!/usr/bin/env python3
'''
Stats
'''
import logging
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist, euclidean
import math
import warnings

class Stats():
    """
    utility Class computing basic
    statistics.
    """

    def __init__(self):
        """pass"""

    @staticmethod
    def mean_point(points):
        """
        Compute the mean point

        Parameters
        ----------
            points: list of tuples
                list of points (tuple) with (x,y)

        Returns
        -------

        """

        return points.mean(axis=0)

    @staticmethod
    def centroid(points):

        x = points[0]
        y = points[1]

        N = range(len(points)-1)
        M = np.array([(x[i]-x[i+1])*(y[i]+y[i+1])/2 for i in N]) #Area of each trapezoid
        My = np.array([(x[i]+x[i+1])/2 for i in N])*M #Moment of area (area*distance to centroid) with respect to the Y axis of each trapezoid
        Mx = np.array([(y[i]+y[i+1])/4 for i in N])*M #Moment of area (area*distance to centroid) with respect to the X axis of each trapezoid
        X = sum(My)/sum(M)
        Y = sum(Mx)/sum(M)
        
        centroid = [X , Y]
        return centroid

    @staticmethod
    def weiszfeld(points):
    
        max_error = 0.0000000001
    
        x=np.array([point[0] for point in  points])
        y=np.array([point[1] for point in  points])
    
    
        ext_condition = True
    
        start_x = np.average(x)
        start_y = np.average(y)
    
        while ext_condition:
    
            sod = (((x - start_x)**2) + ((y - start_y)**2))**0.5
    
            new_x = sum(x/sod) / sum(1/sod)
            new_y = sum(y/sod) / sum(1/sod)
    
            ext_condition = (abs(new_x - start_x) > max_error) or \
                (abs(new_y - start_y) > max_error)
    
            start_y = new_y
            start_x = new_x
    
            print(new_x, new_y)
   
        return (start_x, start_y)

    @staticmethod
    def geometric_median(X, eps=1e-5):
        y = np.mean(X, 0)
    
        while True:
            D = cdist(X, [y])
            nonzeros = (D != 0)[:, 0]
    
            Dinv = 1 / D[nonzeros]
            Dinvs = np.sum(Dinv)
            W = Dinv / Dinvs
            T = np.sum(W * X[nonzeros], 0)
    
            num_zeros = len(X) - np.sum(nonzeros)
            if num_zeros == 0:
                y1 = T
            elif num_zeros == len(X):
                print("y {}",y)
                return y
            else:
                R = (T - y) * Dinvs
                r = np.linalg.norm(R)
                rinv = 0 if r == 0 else num_zeros/r
                y1 = max(0, 1-rinv)*T + min(1, rinv)*y
    
            if euclidean(y, y1) < eps:
                print("y1 {}",y1)
                return y1
    
            y = y1
        return y     

    @staticmethod
    def geometric_median2(X, numIter = 200):
        """
        Compute the geometric median of a point sample.
        The geometric median coordinates will be expressed in the Spatial Image reference system (not in real world metrics).
        We use the Weiszfeld's algorithm (http://en.wikipedia.org/wiki/Geometric_median)
    
        :Parameters:
         - `X` (list|np.array) - voxels coordinate (3xN matrix)
         - `numIter` (int) - limit the length of the search for global optimum
    
        :Return:
         - np.array((x,y,z)): geometric median of the coordinates;
        """
        # -- Initialising 'median' to the centroid
        y = np.mean(X,1)

        # -- If the init point is in the set of points, we shift it:
        while (y[0] in X[0]) and (y[1] in X[1]):
            y+=0.1
    
        convergence=False # boolean testing the convergence toward a global optimum
        dist=[] # list recording the distance evolution
    
        # -- Minimizing the sum of the squares of the distances between each points in 'X' and the median.
        i=0
        while ( (not convergence) and (i < numIter) ):
            num_x, num_y = 0.0, 0.0
            denum = 0.0
            m = X.shape[1]
            d = 0
            for j in range(0,m):
                div = math.sqrt( (X[0,j]-y[0])**2 + (X[1,j]-y[1])**2 )
                num_x += X[0,j] / div
                num_y += X[1,j] / div
                denum += 1./div
                d += div**2 # distance (to the median) to miminize
            dist.append(d) # update of the distance evolution
    
            if denum == 0.:
                warnings.warn( "Couldn't compute a geometric median, please check your data!" )
                return [0,0,0]
    
            y = [num_x/denum, num_y/denum] # update to the new value of the median
            if i > 3:
                print(i)
                convergence=(abs(dist[i]-dist[i-2])<0.01) # we test the convergence over three steps for stability
                print("conv", convergence)
            i += 1
        if i == numIter:
            raise ValueError( "The Weiszfeld's algoritm did not converged after"+str(numIter)+"iterations !!!!!!!!!" )
        # -- When convergence or iterations limit is reached we assume that we found the median.
    
        return np.array(y)

    @staticmethod
    def distance(points,center):

        d = 0

        for i,x in enumerate(points[0]):
           d += math.sqrt(pow((points[0][i]-center[0]),2) + pow((points[1][i]-center[1]),2))
           print(pow((points[0][i]-center[0]),2))
           print(points[0][i],center[0])
           #d += u
        return d

    @staticmethod
    def mean_distance(points,center):

        d = [] 

        for i,x in enumerate(points[0]):
           d.append(math.sqrt(pow((points[0][i]-center[0]),2) + pow((points[1][i]-center[1]),2)))
           #print(pow((points[0][i]-center[0]),2))
           #print(points[0][i],center[0])
           #d += u
        return np.mean(d)


    @staticmethod
    def test_meld(a):
        from scipy.optimize import minimize
        x = [point[0] for point in a]
        y = [point[1] for point in a]
        #z = [point[2] for point in a]

       # x0 = np.array([sum(x)/len(x),sum(y)/len(y), sum(z)/len(z)])
        x0 = np.array([sum(x)/len(x),sum(y)/len(y)])
        def dist_func(x0):
            return sum(((np.full(len(x),x0[0])-x)**2+(np.full(len(x),x0[1])-y)**2)**(1/2))

        res = minimize(dist_func, x0, method='nelder-mead')
        return res.x




if __name__ == "__main__":

    points = np.array([[1,4,6,8,0,0,9,45],[2,5,7,9,6,6,22,78]])
    #points = np.array([[1,2,5,4],[5,2,2,12]])
    #points = np.array([[1,2,1,5],[1,2,2,8]])
    #points = np.array([[1,3],[1,3]])

    #print(Stats.mean_point(points))
    #mean = np.mean(points, axis=1)
    #print("mean: ",mean)
    #print("mean distance: ", Stats.distance(points,mean))
    #median = np.median(points, axis=1)
    #print("median: ",median)
    #print("median distance: ", Stats.distance(points,median))
    #print("dispersion, distance moyenne: ", Stats.mean_distance(points, median))

    
    #centroid = Stats.centroid(points)
    #print("centroid: ",centroid)
    #centro = Stats.weiszfeld(points)

    geom_median = Stats.geometric_median(points)
    print("ici", geom_median)
    geom_median2 = Stats.geometric_median2(points)
    print("la", geom_median2)
    #print("geom_median2 distance: ", Stats.distance(points,geom_median2))
    print("dispersion, distance moyenne: ", Stats.mean_distance(points, geom_median2))
    geom_test = Stats.test_meld(points)
    print("ra", geom_test)
    print("dispersion, distance moyenne: ", Stats.mean_distance(points, geom_test))


    plt.scatter(points[0], points[1], marker='.')
#    plt.plot(*centroid, 'blue', marker='o',markeredgecolor='black', markersize=7)
#    plt.plot(*mean, 'green', marker='o',markeredgecolor='black', markersize=7)
#    plt.plot(*median, 'orange', marker='o',markeredgecolor='black', markersize=7)
#    plt.plot(*centro, 'purple', marker='o',markeredgecolor='black', markersize=7)
    plt.plot(*geom_median, 'orange', marker='o',markeredgecolor='black', markersize=7)
    plt.plot(*geom_median2, 'yellow', marker='o',markeredgecolor='black', markersize=7)
   #plt.plot(*points_ave, 'green', marker='o',markeredgecolor='black', markersize=7)
    plt.axis('equal')
    #plt.xlim((-0.05, 1.05))
    #plt.legend(['points','Centroid','mean','median','centro','geom_median2'])
    plt.savefig("out.png")

    #centroide = (sum(points[0])/len(points[0]),sum(points[1])/len(points[1]))
    #print(centroide)

