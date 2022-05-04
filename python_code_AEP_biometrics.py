# -*- coding: utf-8 -*-
"""Change_Emotiv_AEP_Biometrics_28-04-2022.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dloseOmMWoBAabE4gfrwcSvSheYD1L6X

Coded by Jijomon C.M.in Google Colab enviornment, for testing the possibilty of biometric identificaton using Auditory evoked potential collected while 15 subjects listening familiar names. 1D convolutional neural networks and LSTM units are used for creating the deep neural network in Keras
"""

# Download the signals from the google drive
from google.colab import drive
drive.mount('/content/AEP_Emotiv_data')

!pip install -q keras
!pip install -q mne
!pip install -q visualkeras

import keras
import tensorflow as tf
import cv2
import os # for folder changing
import re
import matplotlib.pyplot as plt
import numpy as np
import math
from keras.layers import Dense
from keras.layers import Flatten
import mne
import array
from scipy import signal # for filtering
from sklearn import preprocessing # for  normalising the data
from keras.layers import LSTM
from keras.layers import Dropout
from keras.layers.convolutional import MaxPooling1D
from keras.layers.convolutional import Conv1D

Number_of_electrodes = 1
Sampling_frequency = 256
Feature_diemension = 3*Sampling_frequency # from single electrode
Filter_order = 10
Low_cut_off = 8
Hig_cut_off = 100
filter_sos = signal.butter(Filter_order, [Low_cut_off, Hig_cut_off], 'bp', fs=Sampling_frequency, output='sos')
training_trial_one_AEP = np.zeros([15,Number_of_electrodes,Sampling_frequency*3*60])
training_trial_two_AEP = np.zeros([15,Number_of_electrodes,Sampling_frequency*3*60])
testing_trial_one_AEP  = np.zeros([15,Number_of_electrodes,45824])

training_trial_one_path = '/content/AEP_Emotiv_data/MyDrive/AEP_Emotiv_data/Train_Session_one/trial_one' 
training_trial_two_path = '/content/AEP_Emotiv_data/MyDrive/AEP_Emotiv_data/Train_Session_one/trial_two' 
testing_trial_one_path = '/content/AEP_Emotiv_data/MyDrive/AEP_Emotiv_data/Test_Session_two/trial_one' 
testing_trial_two_path = '/content/AEP_Emotiv_data/MyDrive/AEP_Emotiv_data/Test_Session_two/trial_two'

#For acquiring the trial one training signals
training_trial_one_candidate_count = 0
Label_training_data_trail_one = np.zeros(15)
training_Signal_for_tem_storage_trail_one = np.zeros((15,10))
No_of_vectors_in_one_trial = int(((3*60)/.5)-3)

os.chdir(training_trial_one_path)
for roots, dirs, files in os.walk(training_trial_one_path): # finding all roots directories and files in the folder
  for file in files:
    if file.endswith(".edf"):# if the file is an edf file      
      edf_data_file_name = os.path.join(file) # edf_file_name = name of directory and file
      candidate_name_in_string = re.findall('[0-9]+', edf_data_file_name)
      candidate_Label = int(candidate_name_in_string[0])
      if candidate_Label > 14:
        candidate_Label = candidate_Label-1
      AEP_data_as_List = mne.io.read_raw_edf(edf_data_file_name)
      tem_storage_training = AEP_data_as_List.get_data()
      filtered_signal = signal.sosfilt(filter_sos, tem_storage_training*1000000)              
      training_trial_one_AEP[training_trial_one_candidate_count,:,:] = filtered_signal[4:(4+Number_of_electrodes),256:(256*3*60+256)]
      Label_training_data_trail_one[training_trial_one_candidate_count] = int(candidate_Label-1)
      training_trial_one_candidate_count = training_trial_one_candidate_count+1

training_data_trial_one = [[] for i0 in range(15)]
Label_training_vector_trial_one = np.zeros(15*No_of_vectors_in_one_trial)
for rows in range(15):
  #print(rows)
  training_window_start_index = 0
  training_window_end_index = Feature_diemension
  for vector_index in range (No_of_vectors_in_one_trial):
    training_data_trial_one[rows].append(training_trial_one_AEP[rows,:,training_window_start_index:training_window_end_index])
    Label_training_vector_trial_one[(rows*No_of_vectors_in_one_trial)+vector_index] = Label_training_data_trail_one[rows]
    training_window_start_index = int(training_window_start_index + (0.5*Sampling_frequency))
    training_window_end_index = int(training_window_start_index + Feature_diemension)

training_vector_trial_one = np.ndarray(shape = (15*No_of_vectors_in_one_trial,Number_of_electrodes,Feature_diemension))
for i1 in range(15):
  for i2 in range(No_of_vectors_in_one_trial-8):
    training_vector_trial_one[(i1*(No_of_vectors_in_one_trial-8))+i2,:,:] = training_data_trial_one[i1][i2]#preprocessing.scale(

#For acquiring the trial two training signals
training_trial_two_candidate_count = 0
Label_training_data_trial_two = np.zeros(15)
training_Signal_for_tem_storage_trail_two = np.zeros((15,10))
No_of_vectors_in_one_trial = int(((3*60)/.5)-3)

os.chdir(training_trial_two_path)
for roots, dirs, files in os.walk(training_trial_two_path): # finding all roots directories and files in the folder
  for file in files:
    if file.endswith(".edf"):  # if the file is an edf file
        edf_data_file_name = os.path.join(file) # edf_file_name = name of directory and file
        candidate_name_in_string = re.findall('[0-9]+', edf_data_file_name)
        candidate_Label = int(candidate_name_in_string[0])
        if candidate_Label > 14:
          candidate_Label = candidate_Label-1
        AEP_data_as_List = mne.io.read_raw_edf(edf_data_file_name)
        tem_storage_trial_2 = AEP_data_as_List.get_data()
        filtered_signal_trial_2 = signal.sosfilt(filter_sos, tem_storage_trial_2*1000000)   
        training_trial_two_AEP[training_trial_two_candidate_count,:,:] = filtered_signal_trial_2[4:(4+Number_of_electrodes),256:(256*3*60+256)]
        Label_training_data_trial_two[training_trial_two_candidate_count] = int(candidate_Label-1)
        training_trial_two_candidate_count = training_trial_two_candidate_count+1


training_data_trial_two = [[] for i0 in range(15)]
Label_training_vector_trial_two_initial = np.zeros(15*No_of_vectors_in_one_trial)
for rows in range(15):
  #print(rows)
  training_window_start_index = 0
  training_window_end_index = Feature_diemension
  for vector_index in range (No_of_vectors_in_one_trial):
    training_data_trial_two[rows].append(training_trial_two_AEP[rows,:,training_window_start_index:training_window_end_index])
    Label_training_vector_trial_two_initial[(rows*No_of_vectors_in_one_trial)+vector_index] = int(Label_training_data_trial_two[rows]) #np. vstack((Label_training_vector, rows))
    training_window_start_index = int(training_window_start_index + (0.5*Sampling_frequency))
    training_window_end_index = int(training_window_start_index + Feature_diemension)

training_vector_trial_two = np.ndarray(shape = (15*(No_of_vectors_in_one_trial-175),Number_of_electrodes,Feature_diemension))
Label_training_vector_trial_two = np.zeros(15*(No_of_vectors_in_one_trial-175))

# for acquiring the training data from the trial two of session one
for i1 in range(15):
  for i2 in range(No_of_vectors_in_one_trial-175):
    training_vector_trial_two[(i1*(No_of_vectors_in_one_trial-175))+i2,:,:] = training_data_trial_two[i1][i2]
    Label_training_vector_trial_two[((i1*(No_of_vectors_in_one_trial-175))+i2)] = Label_training_vector_trial_two_initial[((i1*(No_of_vectors_in_one_trial-175))+i2)]

# for acquiring the validation data from the trial two of session one

Validation_vector = np.ndarray(shape = (15*(175-8),Number_of_electrodes,Feature_diemension))
Label_Validation_vector = np.zeros(15*(175-8))
for i1 in range(15):
  for i2 in range(175-8):
    Validation_vector[(i1*(175-8))+i2,:,:] = training_data_trial_two[i1][i2+182]
    Label_Validation_vector[(i1*(175-8))+i2] = Label_training_vector_trial_two_initial[(i1*357)+(i2+182)]

#For acquiring the testing signals from the second session data

testing_trial_one_candidate_count = 0
Label_testing_data_trail_one = np.zeros(15)
testing_Signal_for_tem_storage_trail_one = np.zeros((15,10))
No_of_vectors_in_one_trial = int(((3*60)/.5)-3) ## chance of error

os.chdir(testing_trial_one_path)
for roots, dirs, files in os.walk(testing_trial_one_path): # finding all roots directories and files in the folder
  for file in files:
    if file.endswith(".edf"):# if the file is an edf file      
      edf_data_file_name = os.path.join(file) # edf_file_name = name of directory and file
      candidate_name_in_string = re.findall('[0-9]+', edf_data_file_name)
      candidate_Label = int(candidate_name_in_string[0])
      if candidate_Label > 14:
        candidate_Label = candidate_Label-1
      AEP_data_as_List = mne.io.read_raw_edf(edf_data_file_name)

      tem_storage_testing = AEP_data_as_List.get_data()
      filtered_signal = signal.sosfilt(filter_sos, tem_storage_testing*1000000)              
      testing_trial_one_AEP[testing_trial_one_candidate_count,:,:] = filtered_signal[4:(4+Number_of_electrodes),0:((256*3*60)-256)]
      Label_testing_data_trail_one[testing_trial_one_candidate_count] = int(candidate_Label-1) 
      testing_trial_one_candidate_count = testing_trial_one_candidate_count+1

testing_data_trial_one = [[] for i0 in range(15)]
Label_testing_vector_trial_one = np.zeros(15*(No_of_vectors_in_one_trial-10))
for rows in range(15):
  #print(rows)
  testing_window_start_index = 0
  testing_window_end_index = Feature_diemension
  for vector_index in range (No_of_vectors_in_one_trial-10):
    testing_data_trial_one[rows].append(testing_trial_one_AEP[rows,:,testing_window_start_index:testing_window_end_index])
    Label_testing_vector_trial_one[(rows*(No_of_vectors_in_one_trial-10))+vector_index] = Label_testing_data_trail_one[rows]
    testing_window_start_index = int(testing_window_start_index + (0.5*Sampling_frequency))
    testing_window_end_index = int(testing_window_start_index + Feature_diemension)

testing_vector_trial_one = np.ndarray(shape = (15*(No_of_vectors_in_one_trial-10),Number_of_electrodes,Feature_diemension))
for i1 in range(15):
  for i2 in range(No_of_vectors_in_one_trial-10):
    testing_vector_trial_one[(i1*(No_of_vectors_in_one_trial-10))+i2,:,:] = testing_data_trial_one[i1][i2]

# To arrange the signals for training

X_train =  np.ndarray(shape = (8085,Feature_diemension,Number_of_electrodes)) # need to check the size 
X_validation =  np.ndarray(shape = (2505,Feature_diemension,Number_of_electrodes))
X_test =  np.ndarray(shape = (5205,Feature_diemension,Number_of_electrodes))#5205

X_train_pre =  np.ndarray(shape = (8085,Feature_diemension,Number_of_electrodes)) # need to check the size
X_validation_pre =  np.ndarray(shape = (2505,Feature_diemension,Number_of_electrodes))
X_test_pre =  np.ndarray(shape = (5205,Feature_diemension,Number_of_electrodes))#5205

training_vector = np.concatenate((training_vector_trial_one,training_vector_trial_two),axis = 0)
Label_training_vector = np.concatenate((Label_training_vector_trial_one,Label_training_vector_trial_two),axis = 0)

Y_train = Label_training_vector
Y_validation = Label_Validation_vector
Y_test = Label_testing_vector_trial_one

# To reshape the signals
for t0 in range(Number_of_electrodes):
  X_train[:,:,t0] = training_vector[:,t0,:] 
  X_validation[:,:,t0]  = Validation_vector[:,t0,:] 
  X_test[:,:,t0]  = testing_vector_trial_one[:,t0,:] 

# To normalize the training and testing signals
for pre_0 in range(8085):#
  for tt0 in range(Number_of_electrodes):
    X_train_pre[pre_0,:,tt0] = preprocessing.scale(X_train[pre_0,:,tt0])

for pre_1 in range(2505):
  for tt1 in range(Number_of_electrodes):
    X_validation_pre[pre_1,:,tt1] = preprocessing.scale(X_validation[pre_1,:,tt1])

for pre_2 in range(5205):
  for tt2 in range(Number_of_electrodes):   
        X_test_pre[pre_2,:,tt2] = preprocessing.scale(X_test[pre_2,:,tt2])

  ## dimension reduction
X_train_dim_red =  X_train_pre[:,::3]
X_validation_dim_red  =  X_validation_pre[:,::3]
X_test_dim_red  =  X_test_pre[:,::3]

from keras.callbacks import Callback
import visualkeras

model = tf.keras.models.Sequential()
model.add(Conv1D(filters=30, kernel_size=20, activation='relu', input_shape=(256,Number_of_electrodes)))#Feature_diemension
model.add(Conv1D(filters=30, kernel_size=20, activation='relu'))#kernel_size=20
model.add(Dropout(0.2))
model.add(LSTM(50))
model.add(Dropout(0.2))
model.add(Dense(30))
model.add(Dense(15, activation='softmax'))
model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

checkpoint_filepath =  '/content/Own_name_Data/My Drive/Own_name_Data' #'/tmp/checkpoint'
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    save_weights_only=True,
    monitor='val_accuracy',
    mode='max',
    save_best_only=True)

history = model.fit(X_train_dim_red, Y_train, validation_data=(X_validation_dim_red, Y_validation), epochs=50,shuffle=True, callbacks=[model_checkpoint_callback]) # #X_validation, Y_validation
model.load_weights(checkpoint_filepath)

# for testing the trained modelled
test_loss, test_acc = model.evaluate(X_test_dim_red, Y_test)
print(test_loss, test_acc*100)