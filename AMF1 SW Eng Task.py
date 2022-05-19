import pandas as pd
import matplotlib.pyplot as plt

#Read data into df
df = pd.read_csv(r'file:///M:\My%20Documents\Python%20Projects\RawData.csv') #Change to match Test Data filepath
pd.set_option('display.max_columns', None)

#Look into test data column data types
#print(df.dtypes)



#Create individual lap df 
Lap1 = df.loc[df['LapNumber']==1]
Lap1 = Lap1.sort_values(by='LapDistance', ascending=True)
Lap2 = df.loc[df['LapNumber']==2]
Lap2 = Lap2.sort_values(by='LapDistance', ascending=True)   #Correct for issue of some distance values in wrong order 
Lap2 = Lap2.reset_index()
Lap3 = df.loc[df['LapNumber']==3]
Lap3 = Lap3.sort_values(by='LapDistance', ascending=True)
Lap3 = Lap3.reset_index()

#Fastest lap comparison
j= Lap1['Speed'].mean()
k = Lap2['Speed'].mean()
l = Lap3['Speed'].mean()

if (j > k) and (j > l):
    print("The fastest lap/setup config is lap 1/ 15 degree flap angle")
elif (k > j) and (k > l):
   print("The fastest lap/setup config is lap 2/ 20 degree flap angle")
else:
   print("The fastest lap/setup config is lap 3/ 25 degree flap angle")
 


#Quick function to plot track layout
def TrackLayout():
    lap_layout = df[['GPSLatCoord','GPSLongCoord']]
    plt.scatter(x=lap_layout['GPSLatCoord'], y=df['GPSLongCoord'])
    plt.title('Bahrain Track Layout')
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

    plt.show()
    plt.savefig('Bahrain_Layout.png')
    return()

TrackLayout()

#Area of interest
chic_L1 = Lap1[(Lap1['LapDistance']>0.611) & (Lap1['LapDistance']<0.798)]
chic_L2 = Lap2[(Lap2['LapDistance']>0.611) & (Lap2['LapDistance']<0.798)]
chic_L3 = Lap3[(Lap3['LapDistance']>0.611) & (Lap3['LapDistance']<0.798)]


#Function to produce telemetry data plots
def Telemetry(Lap1,Lap2,Lap3):
    fig, ax = plt.subplots(6,sharex=True)
    fig.suptitle("Lap/Setup Telemetry Comparison")
    fig.set_size_inches(10,12)
    ax[0].plot(Lap1['LapDistance'], Lap1['Speed'], label='Lap1/15 deg Flap Angle')
    ax[0].plot(Lap2['LapDistance'], Lap2['Speed'], label='Lap2/20 deg Flap Angle')
    ax[0].plot(Lap3['LapDistance'], Lap3['Speed'], label='Lap3/25 deg Flap Angle')
    ax[0].set(ylabel='Speed')
    ax[0].legend(loc="upper right")
    ax[0].grid()
    
    ax[1].plot(Lap1['LapDistance'], Lap1['ThrottlePedal'])
    ax[1].plot(Lap2['LapDistance'], Lap2['ThrottlePedal'])
    ax[1].plot(Lap3['LapDistance'], Lap3['ThrottlePedal'])
    ax[1].set(ylabel='APO')
    ax[1].grid()
    
    ax[2].plot(Lap1['LapDistance'], Lap1['BrakeForce'])
    ax[2].plot(Lap2['LapDistance'], Lap2['BrakeForce'])
    ax[2].plot(Lap3['LapDistance'], Lap3['BrakeForce'])
    ax[2].set(ylabel='Brake Pedal')
    ax[2].grid()

    ax[3].plot(Lap1['LapDistance'], Lap1['CzF'])
    ax[3].plot(Lap2['LapDistance'], Lap2['CzF'])
    ax[3].plot(Lap3['LapDistance'], Lap3['CzF'])
    ax[3].set(ylabel='CzF - Front Dwnfce')
    ax[3].grid()
    
    ax[4].plot(Lap1['LapDistance'], Lap1['CzR'])
    ax[4].plot(Lap2['LapDistance'], Lap2['CzR'])
    ax[4].plot(Lap3['LapDistance'], Lap3['CzR'])
    ax[4].set(ylabel='CzR - Rear Dwnfce')
    ax[4].grid()

    ax[5].plot(Lap1['LapDistance'], Lap1['Cx'])
    ax[5].plot(Lap2['LapDistance'], Lap2['Cx'])
    ax[5].plot(Lap3['LapDistance'], Lap3['Cx'])
    ax[5].set(ylabel='Cx - Drag')
    ax[5].set(xlabel='Lap Distance')
    ax[5].grid()


    plt.rcParams['xtick.major.size'] = 5.0
    plt.rcParams['xtick.minor.size'] = 3.0
    plt.rcParams['ytick.major.size'] = 5.0
    plt.rcParams['ytick.minor.size'] = 3.0
    plt.rcParams['axes.linewidth'] = 0.8
    plt.rcParams['xtick.direction'] = 'out'
    plt.rcParams['ytick.direction'] = 'out'
    x = plt
    #plt.show()
    return(x)

#Produce plots of full lap and turn 11 to 13 section
FullLap=Telemetry(Lap1,Lap2,Lap3)
FullLap.savefig('Full_Lap_Telem.png')
FullLap.show
T11_T13=Telemetry(chic_L1,chic_L2,chic_L3)
T11_T13.savefig('Turn_11to13.png')
T11_T13.show






#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#This section was an attempt to categorise the different sections of the track into a corner phase analysis 
#where the user of this tool could select a specific phase and analyse the telemetry for that section.
#I eventually decided against this method due to the limited time available to finish the task, but I have left the code below available for you to look at if interested.


#Create df for each section of track -- ignore blank values in testdata
Straight1 = pd.DataFrame(columns=['Straight No.','LapDistance','Speed','CzF','CzR','Cx','ThottlePedal','BrakeForce'])
Straight2 = pd.DataFrame(columns=['Straight No.','LapDistance','Speed','CzF','CzR','Cx','ThottlePedal','BrakeForce'])
Straight3 = pd.DataFrame(columns=['Straight No.','LapDistance','Speed','CzF','CzR','Cx','ThottlePedal','BrakeForce'])
Brake1 = pd.DataFrame(columns=['Brake Turn No.','LapDistance','Speed','CzF','CzR','Cx','ThottlePedal','BrakeForce'])
Brake2 = pd.DataFrame(columns=['Brake Turn No.','LapDistance','Speed','CzF','CzR','Cx','ThottlePedal','BrakeForce'])
Brake3 = pd.DataFrame(columns=['Brake Turn No.','LapDistance','Speed','CzF','CzR','Cx','ThottlePedal','BrakeForce'])
Entry1 = pd.DataFrame(columns=['Entry Turn No.','LapDistance','Speed','CzF','CzR','Cx','ThottlePedal','BrakeForce'])
Entry2 = pd.DataFrame(columns=['Entry Turn No.','LapDistance','Speed','CzF','CzR','Cx','ThottlePedal','BrakeForce'])
Entry3 = pd.DataFrame(columns=['Entry Turn No.','LapDistance','Speed','CzF','CzR','Cx','ThottlePedal','BrakeForce'])
Apex1 = pd.DataFrame(columns=['Apex Turn No.','LapDistance','Speed','CzF','CzR','Cx','ThottlePedal','BrakeForce'])
Apex2 = pd.DataFrame(columns=['Apex Turn No.','LapDistance','Speed','CzF','CzR','Cx','ThottlePedal','BrakeForce'])
Apex3 = pd.DataFrame(columns=['Apex Turn No.','LapDistance','Speed','CzF','CzR','Cx','ThottlePedal','BrakeForce'])
Exit1 = pd.DataFrame(columns=['Exit Turn No.','LapDistance','Speed','CzF','CzR','Cx','ThottlePedal','BrakeForce'])
Exit2 = pd.DataFrame(columns=['Exit Turn No.','LapDistance','Speed','CzF','CzR','Cx','ThottlePedal','BrakeForce'])
Exit3 = pd.DataFrame(columns=['Exit Turn No.','LapDistance','Speed','CzF','CzR','Cx','ThottlePedal','BrakeForce'])



#Function to input lap and phase of interest before returning df
def Segment(Lap,df,phase,phasetitle):
    s=1
    l=0
    l = Lap.index.values
 
    for i in range(0,len(l)):
        
        if i==0:                                                                                #Assume all circuits start on a straight
            df = df.append({phasetitle:s, 'LapDistance':Lap.loc[0,'LapDistance'],'Speed':Lap.loc[0,'Speed'],
                            'CzF':Lap.loc[0,'CzF'],'CzR':Lap.loc[0,'CzR'],
                            'Cx':Lap.loc[0,'Cx'], 'ThrottlePedal':Lap.loc[0,'ThrottlePedal'],
                            'BrakeForce':Lap.loc[0,'BrakeForce']}, ignore_index=True)
            
        elif Lap.loc[i,'CornerPhase'] == phase:
            df = df.append({phasetitle:s, 'LapDistance':Lap.loc[i,'LapDistance'],'Speed':Lap.loc[i,'Speed'],
                            'CzF':Lap.loc[i,'CzF'],'CzR':Lap.loc[i,'CzR'],
                            'Cx':Lap.loc[i,'Cx'], 'ThrottlePedal':Lap.loc[i,'ThrottlePedal'],
                            'BrakeForce':Lap.loc[i,'BrakeForce']}, ignore_index=True)
        
        elif Lap.loc[i-1,'CornerPhase'] == phase and Lap.loc[i,'CornerPhase'] != phase:
            s=s+1 

    return(df)

#Create df for each setup/lap segment -- This process would be included within function to remove need to repeat code given more time
str1 = Segment(Lap1,Straight1,'Straight-line','Straight No.')
str1.to_excel("StraightData.xlsx")  
str2 = Segment(Lap2,Straight2,'Straight-line','Straight No.')  
str3 = Segment(Lap3,Straight3,'Straight-line','Straight No.')  
br1 = Segment(Lap1,Brake1,'Braking','Brake Turn No.')  
br1.to_excel("BrakingData.xlsx")
br2 = Segment(Lap2,Brake2,'Braking','Brake Turn No.') 
br3 = Segment(Lap3,Brake3,'Braking','Brake Turn No.')
en1 = Segment(Lap1,Brake1,'Entry','Entry Turn No.')
en1.to_excel("EntryData.xlsx")
en2 = Segment(Lap2,Brake2,'Entry','Entry Turn No.')
en3 = Segment(Lap3,Brake3,'Entry','Entry Turn No.') 
ap1 = Segment(Lap1,Apex1,'Apex','Apex Turn No.')
ap1.to_excel("ApexData.xlsx")
ap2 = Segment(Lap2,Apex2,'Apex','Apex Turn No.')
ap3 = Segment(Lap3,Apex3,'Apex','Apex Turn No.')
ex1 = Segment(Lap1,Exit1,'Exit','Brake Turn No.')
ex1.to_excel("ExitData.xlsx")
ex2 = Segment(Lap2,Exit2,'Exit','Brake Turn No.')
ex3 = Segment(Lap3,Exit3,'Exit','Brake Turn No.') 

#This function would provide a snapshot of what setup/lap the driver was quicker through 
def SetupComp():
    print("Lap1/Setup1 average straight speed: ",str1['Speed'].mean(),"Lap2/Setup2 =",str2['Speed'].mean(),"Lap3/Setup3 = ",str3['Speed'].mean())
    print("Lap1/Setup1 average braking speed: ",br1['Speed'].mean(),"Lap2/Setup2 =", br2['Speed'].mean(),"Lap3/Setup3 = ", br3['Speed'].mean())
    print("Lap1/Setup1 average entry speed: ",en1['Speed'].mean(),"Lap2/Setup2 =",en2['Speed'].mean(),"Lap3/Setup3 = ",en3['Speed'].mean())
    print("Lap1/Setup1 average apex speed: ",ap1['Speed'].mean(),"Lap2/Setup2 = ",ap2['Speed'].mean(),"Lap3/Setup3 = ",ap3['Speed'].mean())
    print("Lap1/Setup1 average Exit speed: ",ex1['Speed'].mean(),"Lap2/Setup2 = ",ex2['Speed'].mean(),"Lap3/Setup3 = ",ex3['Speed'].mean())
    return()

