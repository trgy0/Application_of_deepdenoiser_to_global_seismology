import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df_SNR=pd.read_csv('SNR_P-phase_Z-comp_mag6_oceanic.csv',index_col=0)

df_SNR['SNR Improvement (%)']=(df_SNR['SNR Denoised']/df_SNR['SNR Raw']-1)*100

df_SNR=df_SNR.sort_values(by='SNR Improvement (%)')


fig,ax = plt.subplots(figsize=(12,12))

#ax.plot(df_SNR.index,df_SNR['SNR Raw'], 'r.',label='Raw')
#ax.plot(df_SNR.index,df_SNR['SNR Denoised'],'b.',label='Denoised')
#ax.set_ylabel("SNR values",fontsize=14)

ax.plot(df_SNR['SNR Raw'],df_SNR['SNR Denoised'],'b.',markersize=6)
ax.plot(np.linspace(0,15),np.linspace(0,15),'k')
plt.ylim(0,30)
plt.xlim(0,20)
ax.set_xlabel('SNR Raw')
ax.set_ylabel("SNR Denoised")

print('SUMMARY STATISTICS')
print(df_SNR[['SNR Raw','SNR Denoised','SNR Improvement (%)']].describe())


"""
plt.title("SNR comprasion for raw and denoised signals")
#plt.ylim(0,60)
plt.xlim(0,50)
plt.ylim(0,50)
plt.legend()
plt.show()


# twin object for two different y-axis on the sample plot

# make a plot with different y-axis using second axis object
plt.plot(df_SNR.index, df_SNR['SNR Improvement (%)'],'ko')
plt.ylabel("SNR augementation (%)",fontsize=14)
plt.title("SNR improvement by percetnage")
#plt.ylim(-20,120)
plt.show()


#df_SNR[['SNR Raw','SNR Denoised']].plot.hist(bins=100,alpha=0.5)
#df_SNR[['SNR Raw','SNR Denoised']].plot.bar(stacked=True)

print('SUMMARY STATISTICS')
print(df_SNR.describe())


df_SNR=df_SNR.sort_values(by='Mag')


    

plt.plot(df_SNR['Mag'], df_SNR['SNR Raw'],'ko')
plt.ylabel("SNR",fontsize=14)
plt.xlabel("Magnitude",fontsize=14)
plt.title("SNR Raw vs Magnitude")
plt.show()

plt.plot(df_SNR['Mag'], df_SNR['SNR Denoised'],'ko')
plt.ylabel("SNR",fontsize=14)
plt.xlabel("Magnitude",fontsize=14)
plt.title("SNR Denoised vs Magnitude")
plt.show()

#grouped = df_SNR[['Mag','SNR Denoised']].groupby(['Mag'])
#grouped.boxplot(subplots=False, rot=45, fontsize=12)
"""

