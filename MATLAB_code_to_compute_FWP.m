% Coded by Jijomon C.M. Ph.D. scholar IIT Palakkad
% This is the program to extract the Frequency Weighted Power^ (FWP) features from the selected electrodes the specified frequency band.
%Please place the this script in the folder contains all the data folders namely S001 , S002 . . . S109 downloaded from the PhysioNet database
% Sampling frequency of EEG signal 160 Hz, duration of signal 1 min
% ^FWP is a feature defined in one of our conference paper 
% Jijomon, C. M. and Vinod, A.P., 2020. EEG-based biometric identification using frequency-weighted power feature. IET Biometrics, 9(6), pp.251-258.


clc;
clear;
close all;

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% To read each folder, considering they contain the required EEG signals %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %%

mainFolder = dir(pwd); % pwd for path information, main folder contains all the files inside the current folder
for k = 3:numel(mainFolder) %loop for acessinng all files starting from 3rd one and two are '.' and '..' folders
   
    mainFolder(k).name;      % for testing if you remove ';' all the files & folder names will be displayed
    res1 = isfolder(mainFolder(k).name);
    if(res1==1)             % to check wheather the selected is a file or a folder if yes
        cd(mainFolder(k).name); % to go inside the folder
        subFolder = dir(pwd);   % get the all fils inside the folder
        i = 1;
        str = string()  ;        
        
        for j = 1:numel(subFolder)
            res2 = isfolder(subFolder(j).name);
            if(res2==0)         % Go inside the loop if the considered is not a folder
                subFolder(j).name;
                str(i) = subFolder(j).name; %get all the file names inside the string
                i = i+1;
           
            end               
        end
        

       EO_EEG_sig = str(1);     % first EEG file for Eyes Open Resting state data
       EC_EEG_sig = str(2);     % second eeg file for Eyes Closed Resting State data
        
       [SI,EEG_signal1] = edfread(EO_EEG_sig); % hardcoded assuming there are only two files inside each folder
       [SI,EEG_signal2] = edfread(EC_EEG_sig);
               
%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%    Write code from here    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% %%
 
Chanel_array = [30    25    22    31    41    39     1    29    45     8    24    26    43];% the selected electrode numbers
% the electrode selection is done by another program

for ch = 1:1:13  % loop for each channel 
j=1;
lmt = (7.5*160-1);
% lmt = (5*160-1);
for i = 7.5*160:7.5*160:(60-7.5)*160 % Avoiding the 1st 7.5s EEG signal & windowing the later part into 7.5s windows
   EEG1_W(j,:) = EEG_signal1(Chanel_array(ch),i:i+lmt); 
   EEG2_W(j,:) = EEG_signal2(Chanel_array(ch),i:i+lmt); % Both for Eyes closed and Eyes open
   j = j+1;
end
%% for filtring the EEG signals
n =1;
Wn = [0.5 79]./80; % defining the bandwidth of filter
[z,p] = butter(n,Wn,'bandpass'); % defining Butterworth bandpass filter

for j=1:1:7  %7 because not considering first window

EEG1_W_Filt(j,:) = filtfilt(z,p,EEG1_W(j,:));
EEG2_W_Filt(j,:) = filtfilt(z,p,EEG2_W(j,:));

end
%% To find PSD
for j=1:1:7  %7 because there are 7 windows
    
EEG1_PSD(j,:) = pwelch(EEG1_W_Filt(j,:),160,80,256); % Power in the gamma band for Eyes open
EEG2_PSD(j,:) = pwelch(EEG2_W_Filt(j,:),160,80,256); % power in the gamma band for Eyes closed
end
Late_Gamma_L = floor((30*128)/80);        % to find the gamma band lower limit
Late_Gamma_H = floor((60*128)/80);        %to find the gamma band higher limit

% To find the Power in the 60-80Hz band
temp_sum_1 = 0;
temp_sum_2 = 0;
frequency_sample =0;
for j =1:1:7   %for all the EEG signal windows considered (7 because not considering first window)
    for frequency_sample = 0:1:(Late_Gamma_H-Late_Gamma_L)
        temp_sum_1 = temp_sum_1 + (Late_Gamma_L + frequency_sample)*EEG1_PSD(j,(Late_Gamma_L + frequency_sample));
        Late_Gamma_EO(ch,j,k) = temp_sum_1;
        temp_sum_2 = temp_sum_2 + (Late_Gamma_L + frequency_sample)*EEG2_PSD(j,(Late_Gamma_L+ frequency_sample));
        Late_Gamma_EC(ch,j,k) = temp_sum_2;
    end
end

end     
               
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Main code ends here %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 

                
        cd ..    % Getting out from curent folder
    end
    
    
end



