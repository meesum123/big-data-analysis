import numpy as np
import operator
import time
import math 

#dataset
x = np.random.randint(-10000,10000,1000)
y = np.random.randint(-10000,10000,1000)
points = [x,y]

class Solution:
    def __init__(self,plane):
        self.plane = plane
        self.rx = plane[0][50]
        self.ry = plane[1][50]

    def distance(self,p1,p2):
        return np.sqrt((p1[1] - p1[0])**2 + (p2[1]-p2[0])**2)

    def compute_distances(self):
        dists = []
        pts = []
        for pt in range(len(self.plane[0])):
            x = self.plane[0][pt]
            y = self.plane[1][pt]
            dists.append(self.distance([self.rx,x],[self.ry,y]))
            pts.append(pt)
        dist_pts = zip(dists,pts)
        return dist_pts

    def sort_distances(self,dist_pts):
        dists = sorted(dist_pts, key= operator.itemgetter(0))
        return dists

    def bruteforce(self):
        dists = []
        pts = []
        pts_seen = []
        for pt in range(len(self.plane[0])):
            x = self.plane[0][pt]
            y = self.plane[1][pt]
            for opt in range(len(self.plane[0])):
                ox = self.plane[0][opt]
                oy = self.plane[1][opt]
                if ([ox,oy] not in pts_seen) and (x != ox) and (y != oy):
                    dist_pt = self.distance([x,ox],[y,oy])
                    dists.append(dist_pt)
                    pts.append([(x,y),(ox,oy)])
            pts_seen.append([x,y])
        dist_pts = zip(dists,pts)
        return dist_pts
        
    def triangular_inequality(self, dists):      
        min_dist = 1000
        dist,pts = zip(*dists) 
        point_pair = 0
        for i in range(len(pts)):
            p  = [self.plane[0][pts[i]],self.plane[1][pts[i]]]
            for j in range(i+1,len(pts)):
                pr = [self.plane[0][pts[j]],self.plane[1][pts[j]]]
                dist_right = self.distance([p[0],pr[0]],[p[1],pr[1]])
                theorem_quant = self.distance([self.rx,pr[0]],[self.ry,pr[1]]) - self.distance([self.rx,p[0]],[self.ry,p[1]])
                if dist_right < min_dist:
                    min_dist = dist_right
                    minx = (p[0],p[1])
                    miny = (pr[0],pr[1])
                
                if theorem_quant > min_dist:
                    break

        point_pair = [minx,miny,min_dist]
        return point_pair

    def run_te(self):
        tte = time.time()
        dist_pts = self.compute_distances()
        dists = self.sort_distances(dist_pts)
        point_pair = self.triangular_inequality(dists)
        ttend = time.time()
        print('\n\n\t-------- Triangular Inequality --------') 
        print('\tTime Taken - ',abs(tte - ttend),' s')
        print('\tClosest pair points - ', point_pair[0:2])
        print('\tDistance between - ', point_pair[-1], '\n\n')
        return point_pair,self.plane

    def run_bf(self):
        tbf = time.time()
        dists = self.bruteforce()
        dists = self.sort_distances(dists)
        dist,pts = zip(*dists) 
        point_pair = pts[0]
        tbfend = time.time()
        print('\t------------ Brute Force ------------') 
        print('\tTime Taken - ',abs(tbf - tbfend), ' s')
        print('\tClosest pair points - ', point_pair)
        print('\tDistance between - ', dist[0], '\n\n')

        return point_pair,self.plane 



if __name__ == "__main__":
    sol = Solution(points)
    tte = time.time()
    #Triangular inequality
    te,plane = sol.run_te()
    ette = time.time()
    #Bruteforce
    # be = sol.run_bf()
    etbf = time.time()

    #DAC 
    def brute(ax):
        mi = dist(ax[0], ax[1])
        p1 = ax[0]
        p2 = ax[1]
        ln_ax = len(ax)
        if ln_ax == 2:
            return p1, p2, mi
        for i in range(ln_ax-1):
            for j in range(i + 1, ln_ax):
                if i != 0 and j != 1:
                    d = dist(ax[i], ax[j])
                    if d < mi:  
                        mi = d
                        p1, p2 = ax[i], ax[j]
        return p1, p2, mi
    
    def dist(p1, p2):
        return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
    def closest_pair(ax, ay):
        ln_ax = len(ax)
        if ln_ax <= 3:
            return brute(ax)   
        mid = ln_ax // 2  
        Qx = ax[:mid]  
        Rx = ax[mid:]
        midpoint = ax[mid]  
        Qy = list()
        Ry = list()
        for x in ay:  
            if x <= midpoint:
                Qy.append(x)
            else:
                Ry.append(x)
        (p1, q1, mi1) = closest_pair(Qx, Qy)
        (p2, q2, mi2) = closest_pair(Rx, Ry)
        if mi1 <= mi2:
            d = mi1
            mn = (p1, q1)
        else:
            d = mi2
            mn = (p2, q2)
        (p3, q3, mi3) = closest_split_pair(ax, ay, d, mn)
        if d <= mi3:
            return mn[0], mn[1], d
        else:
            return p3, q3, mi3

    def closest_split_pair(p_x, p_y, delta, best_pair):
        ln_x = len(p_x) 
        mx_x = p_x[ln_x // 2][0] 
        s_y = [x for x in p_y if mx_x - delta <= x[0] <= mx_x + delta]
        best = delta 
        ln_y = len(s_y)  
        for i in range(ln_y - 1):
            for j in range(i+1, min(i + 7, ln_y)):
                p, q = s_y[i], s_y[j]
                dst = dist(p, q)
                if dst < best:
                    best_pair = p, q
                    best = dst
        return best_pair[0], best_pair[1], best

    def solution(x, y):
        a = list(zip(x, y))
        ax = sorted(a, key=lambda x: x[0])  
        ay = sorted(a, key=lambda x: x[1])  
        p1, p2, mi = closest_pair(ax, ay)
        return p1, p2, mi

    metti = time.time()
    p1,p2,mi = solution(plane[0],plane[1])
    metto = time.time()
    
    print('\t------------ Divide & Conquer Approach ------------') 
    print('\tTime Taken - ',abs(metti - metto), ' s')
    print('\tClosest pair points - ', [p1,p2])
    print('\tDistance between - ', mi, '\n\n')

    print('\t Triangular Inequality is ' ,int((ette - etbf)/(tte - ette)) ,'times faster than Bruteforce approch\n\n')
    print('\t Triangular Inequality is ' ,int((metti - metto)/(tte - ette)) ,'times faster than Divide & Conquer approch\n\n')

