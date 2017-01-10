import os
from subprocess import call

# Script for automatically testing and plotting network performance at various stages 

# Version you are testing with
version = 0

# Location of network models
models  = './training/work/2017-01-04_22-26-08'

errors = []
epochs     = []

# For each timestep
#for epoch in range(50,1050,950):
for epoch in range(50,1050,50):

  # Start in the the top directory
  os.chdir('/root/openface')

  # Remove any caches from previous training or testing
  call('rm /datasets/lfw/v'+str(version)+'/cache.t7',shell=True)
  call('rm /datasets/casia/v'+str(version)+'/cache.t7',shell=True)
  call('rm -rf evaluation/experiment0.reps',shell=True)
import os
from subprocess import call

# Script for automatically testing and plotting network performance at various stages 

# Version you are testing with
version = 0

# Location of network models
models  = './training/work/2017-01-04_22-26-08'

errors = []
epochs     = []

# For each timestep
#for epoch in range(50,1050,950):
for epoch in range(50,1050,50):

  # Start in the the top directory
  os.chdir('/root/openface')

  # Remove any caches from previous training or testing
  call('rm /datasets/lfw/v'+str(version)+'/cache.t7',shell=True)
  call('rm /datasets/casia/v'+str(version)+'/cache.t7',shell=True)
  call('rm -rf evaluation/experiment0.reps',shell=True)

  # Generate representations with the new network
  call('./batch-represent/main.lua '+
       '-outDir evaluation/experiment0.reps '+
       '-model '+models+'/model_'+str(epoch)+'.t7 '+
       '-data /datasets/lfw/v'+str(version)
       ,shell=True)

  # Move to the evaluation directory
  os.chdir('/root/openface/evaluation')

  # Generate the ROC curve and the LFW accuracy
  call('./lfw.py experiment0 experiment0.reps'+
       ' > log_'+str(epoch),shell=True)

  # Parse the ouput
  with open('experiment0.reps/accuracies.txt') as f:
    last = None
    for line in (line for line in f if line.rstrip('\n')):
      last = line

  error = (1 - float(last[5:11]))*100
  errors.append(error)
  epochs.append(epoch)
  print('Error for epoch '+str(epoch)+': ')
  print(error)

# Print the result
print(errors)

  # Generate representations with the new network
  call('./batch-represent/main.lua '+
       '-outDir evaluation/experiment0.reps '+
       '-model '+models+'/model_'+str(epoch)+'.t7 '+
       '-data /datasets/lfw/v'+str(version)
       ,shell=True)

  # Move to the evaluation directory
  os.chdir('/root/openface/evaluation')

  # Generate the ROC curve and the LFW accuracy
  call('./lfw.py experiment0 experiment0.reps'+
       ' > log_'+str(epoch),shell=True)

  # Parse the ouput
  with open('experiment0.reps/accuracies.txt') as f:
    last = None
    for line in (line for line in f if line.rstrip('\n')):
      last = line

  error = (1 - float(last[5:11]))*100
  errors.append(error)
  epochs.append(epoch)
  print('Error for epoch '+str(epoch)+': ')
  print(error)

# Print the result
print(errors)

