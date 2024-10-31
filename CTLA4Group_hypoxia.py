import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from differential_equations_hypoxia import radioimmuno_response_model
import new_data_processing_hypoxia as dp
from data_processing import getCellCounts
data = pd.read_csv("../mouseData/White mice - no treatment.csv")
#data = data.drop(columns=['3'])
#print(data.head())
nit_max = 100
nit_T = 100
#param[26] = 10
param = np.array(pd.read_csv("setonix hypoxia constrained growth means control.csv"))
#print(param)

# print(np.array(param))
# param_0 = list(np.transpose(np.array(param))[0])
param = list(np.transpose(param)[0])
param_0 = param.copy()
param_0[39] = 10**82
param_id = [39] #index of parameters to be changed
# param_0[2] = 0.15
# param_0[3] = 0.04
# param_0[4] = 0.4
# param_0[10] = 10**-12
# param_0[32] = 0
# param_0[22] = 0
#param_0 = [500000.0,0.4043764660304215,0.06962669480632436,0.01,0.7,1.0,1.5,1.0000000000000004e-06,0.0,1.82061785504427e-21,1.1637801332682278,0.0492366376540959,0.6416711700693031,0.1617903030935988,0.0416924514099231,0.00416924514099231,2.0,0.0674559557659555,299838.7440652358,0.198909083172271,9.211522519585748e-09,8.284618352937945e-07,0,5.0,100.66660704444035,1062.933185786121,0.1379556739056122,0.4073542114448485,0.0481351408570356,0.0099999999999999,1.1404642118810832e-106,0.2236,0,0.1]
free = [1,1,0]
LQL = 0
activate_vd = 0
use_Markov = 0
T_0 = 1
dT = 0.98
t_f1 = 0
t_f2 = 50
delta_t = 0.05
D = [0]
t_rad = np.array([10])
t_treat_c4 = np.zeros(3)
t_treat_p1 = np.zeros(3)
c4 = 0
p1 = 0
param_best_list = []
c4 = 0.2
p1 = 0
t_f2 = 50
param_id = [39]
data = pd.read_csv("../mouseData/White mice data - PD-1 10 CTLA.csv")
t_treat_c4 = np.array([10])
t_treat_p1 = np.array([10, 12, 14])
for i in range(1,5):
  param_0[37] = 0.2
  param_0[24] = 0.2
  p1 = 0.2
  c4 = 0.2
  row = getCellCounts(data, i)

  #print(row)
  day_length = int(len(row)/3)
  #t_f2 = row[day_length]
  param_best, *_, MSEs, _ = dp.annealing_optimization(row, D, t_rad, c4, p1, t_treat_c4, t_treat_p1, param_0, param_id, T_0, dT, delta_t, free, t_f1, t_f2, nit_max, nit_T, LQL, activate_vd, use_Markov, day_length)
  print(param_best)
  param_best_list.append(param_best)
  times = row[0:day_length]
  #print(times)
  T = row[day_length:2*day_length]
  # print(T)
  # print(fittedVolumes)
  fittedVolumes, radius, radius_H, _, Time, C_tot, C, C_dam, C_tot_N, C_tot_H, C_N, C_H, C_dam_N, C_dam_H, A, Ta_tum, *_ = radioimmuno_response_model(param_best, delta_t, free, t_f1, t_f2, D, t_rad, t_treat_c4, t_treat_p1, LQL, activate_vd, use_Markov)
  #crop fitted volumes so that its same size as array of data volumes
  #print(Time)
  indexes = [index for index, item in enumerate(Time) if item in times]
  fitVolumesCropped = [fittedVolumes[0][index] for index in indexes]
  #print(fitVolumesCropped)
  C_tot = np.array([C_tot[0][index] for index in indexes]) * param_best[7]
  Ta_tum = np.array([Ta_tum[0][index] for index in indexes]) * param_best[21]
  plt.figure(figsize=(8,8))

  # plt.subplot(2, 1, 1)  # 2 rows, 1 column, plot 1
  # plt.plot(np.arange(0,nit_max*nit_T + 1), MSEs, 'o', label='Best MSE')
  # plt.title('Plot 1 with 1 set of data')
  # plt.legend()

# Creating the second plot with two sets of data on the same plot
  # plt.subplot(2, 1, 2)  # 2 rows, 1 column, plot 2
  plt.plot(times, T, 'o', color ='red', label ="Tumor Cell data")
  plt.plot(times, fitVolumesCropped, '--', color ='red', label ="optimized Tumor Cell data")
  #plt.plot(times, C_tot*param_best[9], '--', color ='blue', label ="tumour cell count")
  #plt.plot(times, Ta_tum*param_best[23], '--', color ='green', label ="tumour cell count")
  plt.title('Tumour Volume vs Time after anti-PD-1 and anti-CTLA-4 Treatment')
  plt.legend()
  plt.tight_layout()
  figure_name = "setonix hypoxia anti-CTLA-4 10 tumor volume vs time " + str(i) + " .png"
  plt.savefig(figure_name)
  plt.close()


data = pd.read_csv("../mouseData/White mice data - PD1-15 CTLA.csv")
t_treat_c4 = np.array([15])
t_treat_p1 = np.array([15, 17, 19])
for i in range(1,9):
  t_f2 = 60
  param_0[37] = 0.2
  param_0[24] = 0.2
  c4 = 0.2
  p1 = 0.2
  row = getCellCounts(data, i)

  #print(row)
  day_length = int(len(row)/3)
  #t_f2 = row[day_length]
  param_best, *_, MSEs, _ = dp.annealing_optimization(row, D, t_rad, c4, p1, t_treat_c4, t_treat_p1, param_0, param_id, T_0, dT, delta_t, free, t_f1, t_f2, nit_max, nit_T, LQL, activate_vd, use_Markov, day_length)
  print(param_best)
  param_best_list.append(param_best)
  times = row[0:day_length]
  #print(times)
  T = row[day_length:2*day_length]
  # print(T)
  # print(fittedVolumes)
  fittedVolumes, radius, radius_H, _, Time, C_tot, C, C_dam, C_tot_N, C_tot_H, C_N, C_H, C_dam_N, C_dam_H, A, Ta_tum, *_ = radioimmuno_response_model(param_best, delta_t, free, t_f1, t_f2, D, t_rad, t_treat_c4, t_treat_p1, LQL, activate_vd, use_Markov)
  #crop fitted volumes so that its same size as array of data volumes
  #print(Time)
  indexes = [index for index, item in enumerate(Time) if item in times]
  fitVolumesCropped = [fittedVolumes[0][index] for index in indexes]
  #print(fitVolumesCropped)
  C_tot = np.array([C_tot[0][index] for index in indexes]) * param_best[7]
  Ta_tum = np.array([Ta_tum[0][index] for index in indexes]) * param_best[21]
  plt.figure(figsize=(8,8))

  # plt.subplot(2, 1, 1)  # 2 rows, 1 column, plot 1
  # plt.plot(np.arange(0,nit_max*nit_T + 1), MSEs, 'o', label='Best MSE')
  # plt.title('Plot 1 with 1 set of data')
  # plt.legend()

# Creating the second plot with two sets of data on the same plot
  # plt.subplot(2, 1, 2)  # 2 rows, 1 column, plot 2
  plt.plot(times, T, 'o', color ='red', label ="Tumor Cell data")
  plt.plot(times, fitVolumesCropped, '--', color ='red', label ="optimized Tumor Cell data")
  #plt.plot(times, C_tot*param_best[9], '--', color ='blue', label ="tumour cell count")
  #plt.plot(times, Ta_tum*param_best[23], '--', color ='green', label ="tumour cell count")
  plt.title('Tumour Volume vs Time after anti-PD-1 and anti-CTLA-4 Treatment')
  plt.legend()
  plt.tight_layout()
  figure_name = "setonix hypoxia anti-CTLA-4 15 tumor volume vs time " + str(i) + " .png"
  plt.savefig(figure_name)
  plt.close()



dataFrame = pd.DataFrame(param_best_list[0:])
std_devs = dataFrame.std()
means = dataFrame.mean()
dataFrame.to_csv("setonix hypoxia best parameters anti-CTLA-4.csv", index=False)
std_devs.to_csv("setonix hypoxia errors anti-CTLA-4.csv", index=False)
means.to_csv("setonix hypoxia means anti-CTLA-4.csv", index=False)
print(MSEs)
