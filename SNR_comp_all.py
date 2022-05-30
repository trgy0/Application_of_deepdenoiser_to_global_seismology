import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from obspy.core.event.catalog import read_events
from obspy import read
from os import chdir
from obspy import UTCDateTime
from obspy.geodetics import locations2degrees
from obspy.taup import TauPyModel
from obspy.clients.fdsn import Client

sta_name='G.AIS.'

# function to find list of all events where P wave exists
def events_with_P(events): 
    gcarc=np.zeros(len(events))
    k=0
    evts_P=[]   # list to store all the event indexes where P exists

    for evt in events:  
        # EXTRACT ORIGIN
        origin = evt.origins
        # COMPUTE DISTANCE, AZIMUTH AND BACK-AZIMUTH
        gcarc[k]=locations2degrees(origin[0].latitude, origin[0].longitude,sta[0].latitude, sta[0].longitude) 

        if gcarc[k]<90:
            evts_P.append(k)
        k=k+1
    return evts_P

def SNR_calculate(data,t_phase):
    # computing RMS of signal
    t_arr=int(np.floor(t_phase))
    i1_signal= t_arr-10
    i2_signal= t_arr+30  # for the window finishing 15 s after the phase
    RMS_signal = np.sqrt( np.mean(data[i1_signal:i2_signal]**2) )

    #computing RMS of noise
    i1_noise= t_arr-70
    i2_noise= t_arr-30
    RMS_noise = np.sqrt( np.mean(data[i1_noise:i2_noise]**2) )

    return RMS_signal/RMS_noise

def defining_sta():
   # SeismiQuery GIVES ACTIVITY DURING 2010-01-27 AND 2011-01-27
    starttime = UTCDateTime("2010-01-27")
    endtime = UTCDateTime("2011-01-27")
    iris = Client("IRIS")
    net = iris.get_stations(network="G", station="AIS", channel='LHZ', 
                                  starttime=starttime, endtime=endtime, level="response")
    sta=net[0]
    return sta

sta=defining_sta()

chdir("/Users/User/Desktop/DeepDenoiser/seismic_mag6_oceanic")
events=read_events("catalogue", format="QUAKEML")
model = TauPyModel(model="iasp91")

k_list=events_with_P(events)

# creating pandas df to store all the info

df_SNR=pd.DataFrame(columns=['Signal index (k)','Mag','SNR Raw','SNR Denoised'])

for k in k_list:
    output_file_dir='/Users/User/Desktop/DeepDenoiser/seismic_mag6_oceanic_output/results/'+sta_name+str(k)+'.MSEED.npz'
    input_file=read(sta_name+str(k)+'.MSEED')
    event=events[k]
    # calculating arrival times
    Magnitude=event.magnitudes[0].mag

    
    origin=event.origins
    distance_degree=locations2degrees(origin[0].latitude, origin[0].longitude,
                               sta[0].latitude, sta[0].longitude)
    
    arrivals = model.get_travel_times(source_depth_in_km=origin[0].depth*1e-3,
                                      distance_in_degree=distance_degree,phase_list=['P','S','Pdiff'])
    arrivals = model.get_ray_paths(source_depth_in_km=origin[0].depth*1e-3, distance_in_degree=distance_degree, 
                                   phase_list=["P","S"])
    

    # denoised signal vector
    a = np.load(output_file_dir)
    denoised_signal=a["data"][:,-1,-1]
    
    # raw signal vector
    raw_signal=input_file[-1].data[:3000]
    
    #time steps
    time=input_file[2].times()[:3000]
    
    t_phase=arrivals[0].time
    SNR_raw=SNR_calculate(raw_signal,t_phase)
    SNR_denoise=SNR_calculate(denoised_signal,t_phase)
    
    df_SNR = df_SNR.append({'Signal index (k)': k, 'Mag':Magnitude, 'SNR Raw' : SNR_raw, 
                    'SNR Denoised' : SNR_denoise}, ignore_index = True)

chdir("/Users/User/Desktop/DeepDenoiser/SNR values")
df_SNR.to_csv('SNR_P-phase_Z-comp_mag6_oceanic.csv')


    






