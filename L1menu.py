import uproot 
import numpy as np
import h5py
import sys
import glob 

good_keys = []
fileIN = open('Prescale_2022_v0_1_1.csv')
for line in fileIN:
    values = line.split(",")
    if values[4] == "1":  
        good_keys.append(values[1])
fileIN.close()   

for fileINname in glob.glob("/eos/cms/store/cmst3/group/l1tr/jngadiub/L1TNtupleRun3/*/L1Menu/L1Menu_v2.root"):
    fileOUTname = "L1bit_" + fileINname.split("/")[9]+".h5"

    fileIN = uproot.open(fileINname)
    tree = fileIN["uGT/mytree"]
    event = np.array(tree["event"])

    L1all_bit = np.zeros(event.shape[0])
    keys = tree.keys()
    for key in keys:
        if key == "event": continue
        if key == "run": continue
        if key in good_keys:
            data = np.array(tree[key])
            L1all_bit = L1all_bit + data

    triggered = L1all_bit > 0
    #triggered = triggered*L1_SingleJet35
    print("%s: %s events passed out of %i (%f)" %(fileINname.split("/")[9], np.sum(triggered), event.shape[0], float(np.sum(triggered)/event.shape[0])))

    fileOUT = h5py.File(fileOUTname, "w")
    fileOUT.create_dataset("event", data=event, compression='gzip')
    fileOUT.create_dataset("L1bit", data = triggered,  compression='gzip')
    fileOUT.close()
