import numpy as np
import pandas as pd
import math
from sklearn.model_selection import train_test_split
import random
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier

class HFS_CC_PSO:
    def __init__(self, X, y, swarm_size = 25):
        self.X = X
        self.y = y
        self.swarm_size = swarm_size
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X_norm, y, test_size=0.2)
    
    def entropy(self, values):
        probabilities = [float(values.count(value)) / len(values) for value in set(values)]
        return - sum([p * math.log2(p) for p in probabilities])

    def joint_entropy(self, A, B):
        AB = list(zip(A, B))
        return self.entropy(AB)

    def conditional_entropy(self, A, B):
        return self.joint_entropy(A, B) - self.entropy(B)

    def symmetric_uncertainty(self, A, B):
        HA = self.entropy(A)
        HB = self.entropy(B)
        HAB = self.joint_entropy(A, B)
        HA_given_B = self.conditional_entropy(A, B)
        return (2 * HA - HA_given_B) / (HA + HB)
    
    def fitness_function(self, position, clusters):
        selected_features = list()
        for itr, pos in enumerate(position):
            selected_features.append(clusters[itr+1][int(pos)][0])
        #print(len(selected_features))
        X_train_selected = self.X_train[:, selected_features]
        X_test_selected = self.X_test[:, selected_features]
        clf = RandomForestClassifier()
        clf.fit(X_train_selected, self.y_train)
        accuracy = clf.score(X_test_selected, self.y_test)
        return accuracy

    def phase1(self):
        F_strong = list()
        score_list =[]
        for itr, col in enumerate(self.X.columns):
            score = self.symmetric_uncertainty(self.X[col].tolist(), self.y.tolist())
            F_strong.append((col, score))
            score_list.append(score)

        #before = len(F_strong)
        #print(f"Number of features currently = {before}")
        
        Su_max= max(score_list)
        #print(f"Su_max = {Su_max}")

        D = len(self.X.columns)
        SU_D = D / math.log2(D)
        SU_D = round(SU_D)
        #print(f"SU_D = {SU_D}, F_score of SU_D = {F_strong[SU_D][1]}")
        rho= min(0.1* Su_max,F_strong[SU_D][1])

        for t in F_strong:
            if t[1] < rho:
                F_strong.remove(t)

        #after = len(F_strong)
        #print(f"Number of features currently = {after}")
        
        F_strong.sort(key=lambda a: a[1], reverse = True)
        #F_strong
        return F_strong
    
    def phase2(self, F_strong):
        U0 = F_strong.copy()
        clusters = dict()
        k = 1
        dt_max = U0[0][1] - U0[-1][1]
        D_star = len(U0)
        rho1 = (dt_max*math.log2(D_star))/D_star
        #print(f"rho1 = {rho1}")
        
        while True:
            U1 = U0.copy()
            clusters[k] = list()
            clusters[k].append(U0[0])
            # print(clusters)

            #removing clusters having weak correlation with the top feature(f1) in U1
            for i in range(1, len(U1)):
                difference = U0[0][1] - U0[i][1]
                if difference > rho1:
                    U1.remove(U0[i])

            #Finding similar features to f1(to-feature) and storing them to the cluster-K
            for i in range(1, len(U1)):
                if self.symmetric_uncertainty(X_norm_df[U1[0][0]].tolist(), X_norm_df[U1[i][0]].tolist()) >= min(U1[0][1], U1[i][1]):
                    clusters[k].append(U1[i])

            #updating the U0
            for values in clusters[k]:
                U0.remove(values)

            #checking the stopping criteria
            if len(U0) > 1:
                k += 1
            else:
                break
        
        return clusters
    
    def phase3(self, clusters):
        max_list = list()
        for values in clusters.values():
            max_list.append(values[0][1])
        probabilities = list()
        for values in max_list:
            probabilities.append(values/max_list[0])

        M = len(list(clusters.keys()))
        particles = np.zeros((self.swarm_size, M))
        for i in range(self.swarm_size):
            for j in range(M):
                if random.uniform(0, 1) < probabilities[i]:
                    index = random.randint(0, len(clusters[j+1])-1)
                    particles[i][j] = index
                else:
                    particles[i][j] = 0

        #print(particles)
        
        M = len(clusters)
        Pbest = np.zeros((self.swarm_size, M))

        for i in range(self.swarm_size):
            if self.fitness_function(particles[i], clusters) > self.fitness_function(Pbest[i], clusters):
                Pbest[i] = particles[i]
        
        Gbest = np.zeros((1, M))
        for i in range(self.swarm_size):
            if self.fitness_function(Pbest[i], clusters) > self.fitness_function(Gbest[0], clusters):
                Gbest[0] = Pbest[i]
                
        for i in range(self.swarm_size):
            #Calculate pm
            temp_sum = 0
            for j in range(M):
                if Pbest[i][j] == Gbest[0][j]:
                    temp_sum += 1
            pm = 0.1 * (temp_sum/M)

            #Update
            for j in range(M):
                sum1 = Pbest[i][j] + Gbest[0][j]
                first_half = math.ceil(sum1/2)
                abs_diff = abs(Pbest[i][j] - Gbest[0][j])
                gauss = abs(np.random.normal(loc = 0, scale = 1))
                second_half = np.ceil(gauss*abs_diff)
                final = first_half + second_half
                #print(final)
                if random.uniform(0, 1) > pm:
                    if final < len(clusters[j+1]):
                        particles[i][j] = final
                else:
                    particles[i][j] = Pbest[i][j]
                    
        final_features = list()
        for itr, index in enumerate(Gbest[0]):
            if int(index) != 0:
                final_features.append(clusters[itr+1][int(index)][0])
        return final_features

    def fit(self):
        F_strong = self.phase1()
        clusters = self.phase2(F_strong)
        final_features = self.phase3(clusters)
        return final_features





