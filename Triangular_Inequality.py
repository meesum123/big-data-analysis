import numpy as np
import operator
import time
import math
import matplotlib.pyplot as plt 
import collections

#dataset
x = np.random.randint(-15000,15000,1500)
y = np.random.randint(-15000,15000,1500)
points = [x,y]
    
class Solution:
    def __init__(self,plane):
        self.plane = plane
        self.rx = plane[0][50]
        self.ry = plane[1][50]
        rxry = self.find_quadrant()
        self.mrx,self.mry = rxry[0],rxry[1]

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
        computes = 0
        for i in range(len(pts)):
            p  = [self.plane[0][pts[i]],self.plane[1][pts[i]]]
            for j in range(i+1,len(pts)):
                pr = [self.plane[0][pts[j]],self.plane[1][pts[j]]]
                dist_right = self.distance([p[0],pr[0]],[p[1],pr[1]])
                theorem_quant = self.distance([self.rx,pr[0]],[self.ry,pr[1]]) - self.distance([self.rx,p[0]],[self.ry,p[1]])
                computes += 1
                if dist_right < min_dist:
                    min_dist = dist_right
                    minx = (p[0],p[1])
                    miny = (pr[0],pr[1])
                
                if theorem_quant > min_dist:
                    break

        point_pair = [minx,miny,min_dist]
        return point_pair,computes

    def get_cluster_midpoint(self):
        return int(np.sum(self.plane[0])/len(self.plane[0])),int(np.sum(self.plane[1])/len(self.plane[0]))

    def get_cluster_corner(self):
        return int(np.max(self.plane[0])),int(np.max(self.plane[1]))

    def midpoint_triangular_inequality(self, dists):
        min_dist = 1000
        dist,pts = zip(*dists) 
        point_pair = 0
        computes = 0

        for i in range(len(pts)):
            p  = [self.plane[0][pts[i]],self.plane[1][pts[i]]]
            for j in range(i+1,len(pts)):
                pr = [self.plane[0][pts[j]],self.plane[1][pts[j]]]
                dist_right = self.distance([p[0],pr[0]],[p[1],pr[1]])
                theorem_quant = self.distance([self.mrx,pr[0]],[self.mry,pr[1]]) - self.distance([self.mrx,p[0]],[self.mry,p[1]])
                computes += 1
                if dist_right < min_dist:
                    min_dist = dist_right
                    minx = (p[0],p[1])
                    miny = (pr[0],pr[1])
                
                if theorem_quant > min_dist:
                    break

        point_pair = [minx,miny,min_dist]
        return point_pair,computes

    def find_quadrant(self):
        q1,q2,q3,q4 = 0,0,0,0
        mids_quad = [[30000/4,30000/4],
                     [3*30000/4,30000/4],
                     [-30000/4,-30000/4],
                     [-3*30000/4,-30000/4]   ]
        for pt in range(len(self.plane[0])):
            if self.plane[0][pt] <= 0 and self.plane[1][pt] > 0:
                q1+=1
            elif self.plane[0][pt] >= 0 and self.plane[1][pt] > 0:
                q2+=1
            elif self.plane[0][pt] <= 0 and self.plane[1][pt] < 0:
                q3+=1
            elif self.plane[0][pt] >= 0 and self.plane[1][pt] < 0:
                q4+=1
        pts_quad = [q1,q2,q3,q4]
        qix = pts_quad.index(max(pts_quad))
        print(qix,pts_quad,mids_quad[qix])
        return mids_quad[qix]



    def ref_pattern_finder(self):
        computes_dict = {}
        for i in range(len(self.plane[0])):
            self.rx = self.plane[0][i]
            self.ry = self.plane[1][i]
            dist_pts = self.compute_distances()
            dists = self.sort_distances(dist_pts)
            point_pair,computes = self.triangular_inequality(dists)
            computes_dict[computes] = [self.rx,self.ry]
            if i%100==0:
                print(int(i/100),'/10')
        computes_dict = collections.OrderedDict(sorted(computes_dict.items()))
        computes_dict_keys = list(iter(computes_dict.items()))
        points_low_comp = [x[1] for x in computes_dict_keys[0:10]]
        comparision = [[computes_dict_keys[0][0],computes_dict_keys[-1][0]], computes_dict_keys[-1][1]]
        return points_low_comp,comparision


    def visualize_plane(self,closest_pts):
        plt.scatter(np.round(self.plane[0]),np.round(self.plane[1]),c='r',s=5)
        plt.scatter(closest_pts[0][0],closest_pts[0][1],s=200,facecolors='none', edgecolors='g')
        plt.scatter(closest_pts[0][0],closest_pts[0][1],c='b',s=10)
        plt.scatter(closest_pts[1][0],closest_pts[1][1],c='b',s=10)
        plt.scatter(self.rx,self.ry,marker='o',c='r',s=20)
        # plt.scatter(self.mrx,self.mry,marker='o',c='y',s=20)
        #plt.scatter([closest_pts[0][0],closest_pts[1][0]],[closest_pts[0][1],closest_pts[1][1]],c='b',marker = 'o', markersize =5)
        plt.show()

    def visualize_plane_low_ref(self,points_ref,max_ref,closest_pts):
        plt.scatter(np.round(self.plane[0]),np.round(self.plane[1]),c='r',s=5)
        plt.scatter(points_ref[0][0],points_ref[0][1],c='b',s=10)
        plt.scatter(points_ref[1][0],points_ref[1][1],c='b',s=10)
        plt.scatter(points_ref[2][0],points_ref[2][1],c='b',s=10)
        plt.scatter(points_ref[3][0],points_ref[3][1],c='b',s=10)
        plt.scatter(points_ref[4][0],points_ref[4][1],c='b',s=10)
        plt.scatter(points_ref[5][0],points_ref[5][1],c='b',s=10)
        plt.scatter(points_ref[6][0],points_ref[6][1],c='b',s=10)
        plt.scatter(points_ref[7][0],points_ref[7][1],c='b',s=10)
        plt.scatter(max_ref[0],max_ref[1],c='y',s=10)
        plt.scatter(closest_pts[0][0],closest_pts[0][1],c='g',s=10)
        plt.scatter(closest_pts[1][0],closest_pts[1][1],c='g',s=10)
        plt.scatter(closest_pts[0][0],closest_pts[0][1],s=200,facecolors='none', edgecolors='y')
        plt.show()

    def run_te(self):
        tte = time.time()
        dist_pts = self.compute_distances()
        dists = self.sort_distances(dist_pts)
        point_pair,computes = self.triangular_inequality(dists)
        ttend = time.time()
        print('\n\n\t-------- Triangular Inequality --------') 
        print('\tTime Taken - ',abs(tte - ttend),' s')
        print('\tNo. of Computations - ',computes)
        print('\tReference Point - ', [self.rx,self.ry])
        print('\tClosest pair points - ', point_pair[0:2])
        print('\tDistance between - ', point_pair[-1], '\n\n')
        # self.visualize_plane(point_pair[0:2])
        return point_pair,self.plane

    def run_mte(self):
        mptte = time.time()
        dist_pts = self.compute_distances()
        dists = self.sort_distances(dist_pts)
        point_pair,computes = self.midpoint_triangular_inequality(dists)
        mpttend = time.time()
        print('\n\n\t-------- Centroid Triangular Inequality --------') 
        print('\tTime Taken - ',abs(mptte - mpttend),' s')
        print('\tNo. of Computations - ',computes)
        print('\tReference Point - ', [self.mrx,self.mry])
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
    sol.run_mte()
    #Bruteforce
    #be = sol.run_bf()
    etbf = time.time()
    points,comparision = sol.ref_pattern_finder()
    sol.visualize_plane_low_ref(points,comparision[1],te[0:2])
    print(comparision)
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