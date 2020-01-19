#   This script contains all the mathematical calculations to meausre the similarity / stability of two different clusterings.
#   S = set of N data items.
#   For clustering U and V, (e.g., U = {U_1, U_2, ... , U_R} (distinct partition) where S = Union of U_1 to U_R).
#   where N_00 : the number of pairs that are in different clusters in both U and V
#         N_11 : the number of pairs that are in the same cluster in both U and V
#         N_01 : the number of pairs that are in the same cluster in U but in different clusters in V
#         N_10 : the number of pairs that are in different clusters in U but in same clusters in V
#         n_ij (each element in contigency table) : the number of common elements in two different clusters.

from math import log

class Cluster_comparator():

    '''
        Cluster comparator constructor.

        params:
            U - collection of all the clusters within clustering
            V - collection of all the clusters within clustering
    '''
    def __init__(self, U, V):
        self.U_length = len(U)  # number of clusters in U
        self.V_length = len(V)  # number of clusters in V
        self.U_set_arr = self.extract_set_array_from_clusters(U)    # list of element set in U
        self.V_set_arr = self.extract_set_array_from_clusters(V)   # list of element set in V
        self.contigency_table = self.initialize_contigency_table()   # 2d-array in which each element denoting number of common elements. Last elements denote sum of each row / column
                                                                                        

    '''
        Extract the elements array from clusters object structures and convert this array to array of sets.

        params:
            clusters - array of Set_ object

        return:
            array of sets containing all the elements within clustering
    '''
    def extract_set_array_from_clusters(self, clusters) -> list:
        cluster_array = []
        for i in range(len(clusters)):
            array_to_set = set(clusters[i].elements)
            array_to_set.discard(None)
            cluster_array.append(array_to_set)

        # print("cluster array: ", cluster_array)

        return cluster_array


    '''
        Initialize contigency table in which each element represents the number of common elements in two different clusters.
        Note that last elements denote the sum of each row / column.

        params:

        return: contigency_table, total - 2d array (int)
    '''
    def initialize_contigency_table(self) -> list:
        contigency_table = [[0 for i in range(self.V_length)] for j in range(self.U_length)]
        # total = 0

        # update contigency table
        for i in range(self.U_length):
            row_sum = 0
            for j in range(self.V_length):
                for set_element in self.U_set_arr[i]:
                    if set_element in self.V_set_arr[j]:
                        contigency_table[i][j] += 1
                        # total += 1
                        row_sum += 1
            
            contigency_table[i].append(row_sum)

        # calculate sum of each column and add it as the last row of the contigency table
        col_sum_arr = [sum([row[i] for row in contigency_table]) for i in range(len(contigency_table[0]))]
        # col_sum_arr.append(total)

        contigency_table.append(col_sum_arr)
        print('contingency table: ')
        for i in contigency_table:
            print(i)


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
        pass


    '''
        Calculate the number of pairs that are in different clusters in both U and V.

        params:
            U - clustering containing all the clusters
            V - clustering containing all the clusters

        return:
            N_00 - the number of pairs that are in different clusters in both U and V
    '''
    def calculate_N_00(self) -> int:
        pass
    

    '''
        Calculate the number of pairs that are in the same cluster in U but in different clusters in V.

        params:
            U - clustering containing all the clusters
            V - clustering containing all the clusters

        return:
            N_01 - the number of pairs that are in the same cluster in U but in different clusters in V
    '''
    def calculate_N_01(self) -> int:
        pass


    '''
        Calculate the number of pairs that are in different clusters in U but in same clusters in V.

        params:
            U - clustering containing all the clusters
            V - clustering containing all the clusters

        return:
            N_10 - the number of pairs that are in different clusters in U but in same clusters in V
    '''
    def calculate_N_10(self) -> int:
        pass


    '''
    '''
    def entropy(self, cluster = "U") -> int:
        entropy = 0
        contigency_N = self.contigency_table[self.U_length][self.V_length]  # total sum of number of common elements

        if cluster == "U":
            for i in range(self.U_length):
                a_i = float(self.contigency_table[i][self.V_length])
                if a_i != 0:
                    entropy += (a_i / contigency_N) * log(a_i / contigency_N)
        
        else:   # cluster = "V"
            for j in range(self.V_length):
                b_j = float(self.contigency_table[self.U_length][j])
                if b_j != 0:
                    entropy += (b_j / contigency_N) * log(b_j / contigency_N)

        return -entropy if entropy !=0 else 0.0000001


    '''
        Calculate the joint entropy of two clusterings via contigency table.

        params:
        
        return:
            joint_entropy - joint entropy of two clusterings
    '''
    def joint_entropy(self) -> float:
        joint_entropy = 0
        contigency_N = self.contigency_table[self.U_length][self.V_length]  # total sum of number of common elements

        for i in range(self.U_length):
            for j in range(self.V_length):
                current_n = float(self.contigency_table[i][j] if self.contigency_table[i][j] !=0 else 0.0000001)
                
                joint_entropy += (current_n / contigency_N) * log(current_n / contigency_N)
        
        return -joint_entropy


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
        N_00 = 0
        N_11 = 0
        N_01 = 0
        N_10 = 0

        ari = 2 * (N_00 * N_11 - N_01 * N_10) / ((N_00 + N_01) * (N_01 + N_11) + (N_00 + N_10) * (N_10 + N_11))

        return ari
    


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

        for i in range(self.U_length):
            a_i = float(self.contigency_table[i][self.V_length])
            for j in range(self.V_length):
                current_n = float(self.contigency_table[i][j])

                if current_n != 0:
                    b_j = float(self.contigency_table[self.U_length][j])
                    mutual_info += (current_n / contigency_N) * log((current_n / contigency_N) / ((a_i * b_j) / contigency_N ** 2))
        
        return mutual_info

    '''
        Information theoric based measures.
        Normalized Mutual Information - joint (NMI) - normalized version of mutual information.

        params:

        return:
            normalized mutual information
    '''
    def joint_normalized_mutual_information(self):
        return self.mutual_information() / self.joint_entropy()
                