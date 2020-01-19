#   This script contains all the mathematical calculations to meausre the similarity / stability of two different clusterings.
#   S = set of N data items.
#   For clustering U and V, (e.g., U = {U_1, U_2, ... , U_R} (distinct partition) where S = Union of U_1 to U_R).
#   where N_00 : the number of pairs that are in different clusters in both U and V
#         N_11 : the number of pairs that are in the same cluster in both U and V
#         N_01 : the number of pairs that are in the same cluster in U but in different clusters in V
#         N_10 : the number of pairs that are in different clusters in U but in same clusters in V
#         n_ij (each element in contigency table) : the number of common elements in two different clusters.

from math import log
import time 

class Cluster_comparator():

    '''
        Cluster comparator constructor.

        params:
            U - collection of all the clusters within clustering
            V - collection of all the clusters within clustering
    '''
    def __init__(self, U, V):
        self.U = U
        self.V = V
        self.U_length = len(U)  # number of clusters in U
        self.V_length = len(V)  # number of clusters in V
        # self.U_set_arr = self.extract_set_array_from_clusters(U)    # list of element set in U
        # self.V_set_arr = self.extract_set_array_from_clusters(V)   # list of element set in V
        # self.contigency_table = self.initialize_contigency_table()   # 2d-array in which each element denoting number of common elements. Last elements denote sum of each row / column

    

    '''
        Extract the elements array from clusters object structures and convert this array to array of sets.

        params:
            clusters - Set_collection object

        return:
            array of sets containing all the elements within clustering
    '''
    def extract_set_array_from_clusters(self, clusters) -> list:
        cluster_array = []

        for i in range(len(clusters)):
            cluster_array.append(set(clusters[i].elements))

        return cluster_array


    '''
        Initialize contigency table in which each element represents the number of common elements in two different clusters.
        Note that last elements denote the sum of each row / column.

        params:

        return: contigency_table, total - 2d array (int)
    '''
    def initialize_contigency_table(self) -> list:
        contigency_table = [[0 for i in range(self.U_length)] for j in range(self.V_length)]
        total = 0

        # update contigency table
        for i in range(self.U_length):
            row_sum = 0
            for j in range(self.V_length):
                for set_element in self.U_set_arr[i]:
                    if set_element in self.V_set_arr[j]:
                        contigency_table[i][j] += 1
                        total += 1
                        row_sum += 1
            
            contigency_table[i].append(row_sum)

        # calculate sum of each column and add it as the last row of the contigency table
        col_sum_arr = [sum([row[i] for row in contigency_table]) for i in range(len(contigency_table[0]))]
        col_sum_arr.append(total)
        contigency_table.append(col_sum_arr)

        return contigency_table


    '''
        Calculate the number of pairs that are in the same cluster in both U and V.

        params:
            U - clustering containing all the clusters
            V - clustering containing all the clusters

        return:
            N_11 - the number of pairs that are in the same cluster in both U and V
    '''
    def calculate_N_11(self) -> int:
        count=0
        for i in self.same_0:
            if i in self.same_1:
                count += 1

        return count  


    '''
        Calculate the number of pairs that are in different clusters in both U and V.

        params:
            U - clustering containing all the clusters
            V - clustering containing all the clusters

        return:
            N_00 - the number of pairs that are in different clusters in both U and V
    '''
    def calculate_N_00(self) -> int:
        count=0
        for i in self.diff_0:
            if i in self.diff_1:
                count+=1 
        
        return count
    

    '''
        Calculate the number of pairs that are in the same cluster in U but in different clusters in V.

        params:
            U - clustering containing all the clusters
            V - clustering containing all the clusters

        return:
            N_01 - the number of pairs that are in the same cluster in U but in different clusters in V
    '''
    def calculate_N_01(self) -> int:
        count=0
        for i in self.same_0:
            if i in self.diff_1:
                count+=1 
        
        return count


    '''
        Calculate the number of pairs that are in different clusters in U but in same clusters in V.

        params:
            U - clustering containing all the clusters
            V - clustering containing all the clusters

        return:
            N_10 - the number of pairs that are in different clusters in U but in same clusters in V
    '''
    def calculate_N_10(self) -> int:
        count=0
        for i in self.diff_0:
            if i in self.same_1:
                count+=1
        
        return count

    '''
        Pair counting based measures.
        Adjusted version of Rand Index (ARI). 

        ARI(U, V) = 2(N_00 * N_11 - N01 * N10) / ((N_00 + N_01) * (N_01 + N_11) + (N_00 + N_10) * (N_10 + N_11)).
        And NC2 item pairs can be classified into one of the 4 types above.

        params:
            U - clustering containing all the clusters
            V - clustering containing all the clusters

        return:
            ARI - Adjusted Rand Index (see above)
    '''
    def adjusted_rand_index(self) -> float:
        
        N_11 = self.calculate_N_11()
        N_00 = self.calculate_N_00()
        N_10 = self.calculate_N_10()
        N_01 = self.calculate_N_01()
        print(N_11, N_00, N_10, N_01)

        divisor = ((N_00 + N_01) * (N_01 + N_11) + (N_00 + N_10) * (N_10 + N_11))
        dividend = 2 * (N_00 * N_11 - N_01 * N_10)
        
        if divisor != 0:
            ari =  dividend / divisor
        else:
            return 0 

        return ari
    
    def initialize_pairs_measure(self, a, b):
        self.same_0 = a
        self.diff_0 = b

        self.U_elem_to_index = self.generate_elem_dict(self.U)                            
        self.V_elem_to_index = self.generate_elem_dict(self.V)                            
        self.generate_pairs_info()

    '''
        Dictionary from element to cluster indexes generator.

        params:
            clusters - Set_collection object            
        
        returns:
            dictionary of element to cluster index dictionary
    '''
    def generate_elem_dict(self, clusters) -> dict:
        elem_to_index = {} 
        for i in range(len(clusters)):
            for j in clusters[i].elements:
                if j != None:
                    # print(clusters[i].index, " : " , j)
                    elem_to_index[j] = clusters[i].index
        
        return elem_to_index
    
    '''
        Generate pairs information to calculate ARI.
        Input pairs from U and V are categorized by falling into same cluster indices or not(different cluster).
        (resets and saves the output lists to class variables)

        params:
        
        returns:

    '''
    def generate_pairs_info(self) -> None:

        if len(self.same_0) == 0 and len(self.diff_0) == 0:
            self.same_0 = set()
            self.diff_0 = set()
        
            for elem_U1, cluster_index_U1 in sorted(self.U_elem_to_index.items()):
                for elem_U2, cluster_index_U2 in sorted(self.U_elem_to_index.items()):
                    if elem_U1 != elem_U2:
                        if elem_U1 < elem_U2:
                            pair = (elem_U1, elem_U2) 
                            if cluster_index_U1 == cluster_index_U2:
                                self.same_0.add(pair)
                            else:
                                self.diff_0.add(pair)          
                                      

        self.same_1 = set()
        self.diff_1 = set()

        for elem_V1, cluster_index_V1 in (self.V_elem_to_index.items()):
            for elem_V2, cluster_index_V2 in (self.V_elem_to_index.items()):
                if elem_V1 != elem_V2:
                    if elem_V1 < elem_V2:
                        pair = (elem_V1, elem_V2)
                        if cluster_index_V1 == cluster_index_V2:
                            self.same_1.add(pair)
                        else:
                            self.diff_1.add(pair)
        
        # return same_0, diff_0, same_1, diff_1


    """ 
        Getter function for same_1 and diff_1 for the next query.

        param:

        return: 
            same_1: list of Pairs that are in the same clusters
            diff_1: list of Pairs that are in different clusters
    """             
    def get_pairs_lists(self):
        return self.same_1, self.diff_1

    
    '''
        Information theoric based measures.
        Mutual Information(MI) - most basic similarity measure of clustering.

        params:

        return:
            mutual_info - mutual information
    '''
    def mutual_information(self):
        mutual_info = 0
        contigency_N = self.contigency_table[self.U_length][self.V_length]  # total sum of number of common elements

        for i in range(len(self.contigency_table)):
            a_i = self.contigency_table[i][self.V_length]
            for j in range(len(self.contigency_table[0])):
                current_n = self.contigency_table[i][j]
                b_j = self.contigency_table[self.U_length][j]
                mutual_info += current_n / contigency_N * log((current_n / contigency_N) / ((a_i * b_j) / contigency_N ** 2))
        
        return mutual_info
    
    