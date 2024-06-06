import unisens
import neurokit2 as nk
import pickle

#This needs to be executed once to genereate the bpm database


#Path to Corvolution Data Folder
data_path = "... PATH-TO-DATA ... /Corvolution/"


#Output Path to directory of bpm database 
bpm_db_output = "... PATH-TO-THIS-DIRECTORY ... "

bpm_db_name = "all_bpm.p" 



#number of patient data
n = 150

#List of all user IDs, user data directory is exptected in 'db_path/Person' + id, where id is represented with 5 digits
IDs = range(1, n+1)

#Frequency of ECG samples per second
sample_rate = 1000
#Database with bpm values of every user
all_bpms = dict()

for id in IDs:

    print("Load data of user with id " + str(id))
    #path of user data
    path = data_path + 'Person' + str(id).zfill(5)
    u = unisens.Unisens(path)
    #get ECG Data
    signal = u['ecg.bin']
    data = signal.get_data()
    #Correct Dimensionality
    data = data.ravel()

    #Clean ECG data
    data = nk.ecg_clean(data, sampling_rate=sample_rate)
           

    #Calculate position of R-Spikes, which indicates heart beats
    _, rpeaks = nk.ecg_peaks(data, sampling_rate=sample_rate)
    rpeaks = rpeaks['ECG_R_Peaks']

    #BPM values
    bpm = list()


    minuteMarker = 60 * sample_rate
    beat_counter = 0

    for j in range(len(rpeaks)):
        if rpeaks[j] < minuteMarker: #Heart Beat is within current Minute
            beat_counter +=1
        else:                       #Heart Beats appears in next minute
            minuteMarker += 1000 *60
            bpm.append(beat_counter)
            beat_counter = 0
    
    #Save bpm values of User in database
    all_bpms[str(id)] = bpm

#Trim every sequnce to equal length of 24 hours

print("Trim sequences")
for id in IDs:
    bpm = all_bpms[str(id)]

    #Remove first 30 Minutes of readings since these are error loaded
    bpm = bpm[30:]

    while len(bpm) > 24 * 60: #Remove BPMs while Sequnece is longer than 24 hours
        bpm.pop()
    
    if len(bpm) != 24*60: #Check wheter there is a sequence less than 24 hours long
        raise ValueError('Length is not matching')
    
    #Update sequence length
    all_bpms[str(id)] = bpm

#Save bpm database at output path
f = open(bpm_db_output + bpm_db_name, 'wb')
pickle.dump(all_bpms, f, 4)
f.close()

print("Finished")
print("BPM Database saved at " + bpm_db_output + bpm_db_name)