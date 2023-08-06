
from scipy.interpolate import interp1d
import numpy as np 
import matplotlib.pyplot as plt 


def my_interpolate(mypoints,method,plot=False,n = 45):

    #p0 = points[0]
    #points = points + [(p0[0],p0[1])]

    points = [(p[0],p[1]) for p in mypoints]
    #print("points", points)

    distance = np.cumsum( np.sqrt(np.sum( np.diff(points, axis=0)**2, axis=1 )) )
    distance = np.insert(distance, 0, 0)

    if len(distance) > 0:
        distance = distance/distance[-1]
    
    # method = "square"
    alpha = np.linspace(0,1,n)
    interpol =  interp1d(distance, points, kind = method , axis=0)
    interpolated_points = interpol(alpha)

    if plot:
        plt.figure()
        plt.scatter([p[0] for p in points], [p[1] for p in points], facecolor="white", color="black")
        plt.scatter([p[0] for p in interpolated_points], [p[1] for p in interpolated_points], color="red")
        plt.show()

    return interpolated_points

if __name__ == "__main__":
    points = [(0,4), (5,5), (1,8)]

    my_interpolate(points,method="quadratic",plot=True)

    points = [(0,4), (0,5), (0,6), (0,7)]
    my_interpolate(points,method="quadratic",plot=False)