import numpy

a = numpy.zeros(shape=(8, 9))

a[0] = [1,1,0,0,0,0,1,0,0]
a[1] = [1,1,0,0,0,0,1,1,0]
a[2] = [1,1,1,0,0,0,1,1,0]
a[3] = [1,0,1,0,0,0,1,1,1]
a[4] = [1,1,0,1,0,1,0,0,0]
a[5] = [1,1,1,1,0,1,0,0,0]
a[6] = [1,0,1,1,1,0,0,0,0]
a[7] = [1,0,1,1,0,1,0,0,0]

objects=['leech','bream','frog','dog','thorn','reed','bean','corn']
attributes=['needs water', 'lives in water', 'lives on land', 'needs chlorophyll', 'dicotyledon', 'monocytoledon','able to move', 'has limbs','able to suckle']


def intersection(matrix, formal_concept_for_testing):
    #matrix - initial matrix M
    #formal_concept_for_testing - will this boolean vector be formal concept or not?
    matrix_indexes = [] #indexes of M's rows, which contain row formal_concept_for_testing (for computing their closure)
    fcft_indexes = numpy.where(formal_concept_for_testing > 0) #indexes of '1' in formal_concept_for_testing
    intersect = numpy.ones(shape=(1, 9)) #initialize intersection vector with all '1'
    for i in range(0, matrix.shape[0]): #search through M rows to find rows that contain formal_concept_for_testing
        temp = numpy.where(matrix[i] > 0) #temporary vector with indexes of [i]-th M row
        is_subset = numpy.in1d(fcft_indexes, temp) #vector of True/False's that indicates if fcft_indexes is a subset of temp
        #dim(is_subset)=dim(fcft_indexes)
        if numpy.sum(is_subset) == len(fcft_indexes[0]): #if is_subset consists of all True
            matrix_indexes.append(i) #save M's row index
    for i in matrix_indexes: #compute intesection of all rows that contain formal_concept_for_testing
        intersect[0] = intersect[0] * matrix[i]
    return intersect, matrix_indexes

def equality(vec_1, vec_2):
    #function checks if vec_1 and vec_2 are equal element-wise. (that also includes case when vec_1=10100110 and vec_2=10100111)
    i = numpy.amax(numpy.where(vec_1 > 0)) + 1 #index of last '1'
    return numpy.array_equal(vec_1[:,0:i], vec_2[:,0:i])

def save(result, vec):
    #saves vec to result matrix of final formal concepts
    result.append(vec.tolist())

def ganter(matrix):
    last_success = numpy.zeros(shape=(1, 9)) #initialize last_success
    end = numpy.ones(shape=(1, 9))
    result = [] #initialize matrix of formal concepts
    intersection_indexes = [] #matrix of indexes of rows for i-th intersection
    count = 0 #number of steps made to find all formal concepts
    while True:
        formal_concept_for_testing = numpy.copy(last_success) #save last success to formal_concept_for_testing
        for i in reversed(range(9)): #add '1' from the end of formal_concept_for_testing
            count += 1 #step counting

            #generate formal_concept_for_testing:
            if formal_concept_for_testing[:,i]==1: #replace last '1' with '0'
                formal_concept_for_testing[:,i]=0
                continue
            formal_concept_for_testing[:,i]=1 #set last element as '1' if we had '0'

            #calculate intesection for this
            fcft_prime_prime, mat_ind = intersection(matrix, formal_concept_for_testing[0]) #compute intesection for

            #check if A=A'' (and exit loop in that case)
            if equality(formal_concept_for_testing, fcft_prime_prime):
                if numpy.array_equal(formal_concept_for_testing, fcft_prime_prime):
                    save(result, fcft_prime_prime[0])
                    intersection_indexes.append(mat_ind)
                break

            #do we have '0' fot next step? 1011 or 1111?
            zero_count = len(numpy.where(formal_concept_for_testing[0,0:i] == 0)[0])
            if zero_count > 0:
                formal_concept_for_testing[:,i] = 0 #reset [i] element (set as 0)
            else:
                break
        last_success = formal_concept_for_testing #save formas concepst as last success
        if numpy.array_equal(end, formal_concept_for_testing):
            break
    return result,intersection_indexes

def formal_concepts(matrix):
    fc_matrix, objects_ind=ganter(matrix)
    for i in range(0,len(fc_matrix)):
        #save i-th formal concept as boolean vector
        fc_boolean=numpy.array(fc_matrix[i])

        #compute all attributes for i-th formal concept
        fc_attributes=numpy.array(attributes)[fc_boolean.astype(numpy.bool)]

        #compute all objects for i-th formal concept
        fc_objects=[objects[j] for j in objects_ind[i]]

        print str(i+1) + ')\t '+ str(fc_boolean) + ';\n\t Attributes: ' + str(fc_attributes) + '; \n\t Objects: ' + str(fc_objects) + '\n\n'

formal_concepts(a)