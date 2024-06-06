import pickle
import matplotlib.pyplot as plt
import schemes

#Calculate MACE eror, Set C to the calssification parameter or to None if no Categorization is used
def calc_MACE(rawData, anonData, C = None):
    m = len(rawData)
    if m != len(anonData):
        raise ValueError("Sequences are not of same length")
    
    MACE = 0
    #Add proportional  distance to every point
    for i in range(m):
        MACE += abs(rawData[i] - anonData[i])/m
    
    #Account to maximal categorization error  of C - 1
    if C != None:
        MACE = MACE * (C-1) 

    return MACE
    




#Parameter
C = 15
k = 60
epsilon = 10



#Path to directory of bpm database all_bpm.p
db_path = '... PATH-to-BMP-DB ... /all_bpm.p'


f = open(db_path, 'rb')
data = pickle.load(f)
f.close()


'Choose scheme for visulation and testing'
# scheme = schemes.SPC(data)
# scheme = schemes.SPAvg(60, data)
# scheme = schemes.SPCat(15, data)
# scheme = schemes.SPAvgCat(60, 15, data)
scheme = schemes.SPCatAvg(C, k, data)


#Build anonymized database, chose sensitvity from the following keys 'theo', 'emp', 'cor'
a_db = scheme.anonymize_database(epsilon, 'cor')

#Calculate Anonymized Average over every employee
a_avg = schemes.calculate_average(a_db)

#Raw Data average as reference
raw_avg = schemes.calculate_average(scheme.rawdata)


#Calculate MACE, set C to None if no categorization is used
MACE = calc_MACE(raw_avg, a_avg, C)
MACE = round(MACE, 2)

print('MACE is ' + str(MACE))


'''Configure Simple Pyplot'''
#Raw Average plot
plt.plot(raw_avg, color='blue', zorder=1, label='raw')
#Anonymized Average plot
plt.plot(a_avg, color='orange', zorder=2, label='anonymized')

plt.show()


