import os
from subprocess import call

# Script for automatically training and testing OpenFace

# Versions you are testing with
vers_to_run = [ 0, 1]

# For each timestep
for version in vers_to_run:

  model_dir  = 'work/train_'+str(version)

  ############################
  # Train
  ############################

  # Start in the the top directory
  os.chdir('/root/openface')

  # Remove any caches from previous training or testing
  call('rm /datasets/lfw/v'+str(version)+'/cache.t7',shell=True)
  call('rm /datasets/casia/v'+str(version)+'/cache.t7',shell=True)
  call('rm -rf training/work',shell=True)
  call('rm -rf evaluation/experiment0.reps',shell=True)

  # Start in the the top directory
  os.chdir('/root/openface/training')

  # Run training
  call('th main.lua '+
       '-save '+model_dir+' '+
       '-data /datasets/casia/v'+str(version)+' '
       '-nGPU 1 '+
       '-nDonkeys 8 '+
       '-epochSize 200 '+
       '-peoplePerBatch 10 '+
       '-imagesPerPerson 10',
       shell=True)

  ############################
  # Testing
  ############################

  # Test the last epoch
  epoch = 1000

  # Start in the the top directory
  os.chdir('/root/openface')

  # Remove any caches from previous training or testing
  call('rm /datasets/lfw/v'+str(version)+'/cache.t7',shell=True)
  call('rm /datasets/casia/v'+str(version)+'/cache.t7',shell=True)
  call('rm -rf evaluation/experiment0.reps',shell=True)

  # Generate representations with the new network
  call('./batch-represent/main.lua '+
       '-outDir evaluation/experiment0.reps '+
       '-model '+model_dir+'/model_'+str(epoch)+'.t7 '+
       '-data /datasets/lfw/v'+str(version)
       ,shell=True)

  # Move to the evaluation directory
  os.chdir('/root/openface/evaluation')

  # Generate the ROC curve and the LFW accuracy
  call('./lfw.py experiment0 experiment0.reps'+
       ' > log_'+str(epoch),shell=True)

  '''
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
  '''

  # Move back to the top directory
  os.chdir('/root/openface')

  # Copy the output to a separate log file
  call('cp /root/openface/evaluation/experiment0.reps/accuracies.txt '+
       'log_'+str(version)+'.txt',
       shell=True)

                                                                                                                                                                                           90,0-1        Bot

