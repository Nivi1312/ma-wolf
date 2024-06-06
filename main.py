import pickle
import schemes
import analysis
#Categories size of 15
C = 15
#Average of 1 hour
k = 60
#Mild privacy protection
epsilon = 10

#For local execution use complete path (name inclusive) to all_bpm.p and for containernization just use 'all_bpm.p'
db_path = '.... PATH-TO-BPM-DB .... /all_bpm.p'


f = open(db_path, 'rb')
data = pickle.load(f)
f.close()

#Select an anonymization scheme, if multiple schemes are used the database needs to be deepcopied before initalizing class

# scheme = schemes.SPC(data)
# scheme = schemes.SPAvg(k, data)
# scheme = schemes.SPCat(C, data)
# scheme = schemes.SPAvgCat(k, C, data)
scheme = schemes.SPCatAvg(C, k, data)

#Build anonymized database, chose sensitvity from following keys 'theo', 'emp', 'cor'
a_db = scheme.anonymize_database(epsilon, 'cor')

#Calculate Anonymized Average over every employee
a_avg = schemes.calculate_average(a_db)

#Detect stress times, ideally there shouldn't be found stress since it was not added
stress_times = analysis.detect_stress_times(a_avg)

if len(stress_times) != 0:
    print(stress_times)
else:
    print("No stressful times were found!")