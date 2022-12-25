# Real_time_resource_monitor

## Problem Statement -
To build a GUI-based application for real-time monitoring of :-
- CPU & memory utilization
- networking status
- processes and their resource utilization
- hardware sensors related information.

<hr> 

## How to run code in your machine ?
1.First create the virtual environment in your linux OS .
  - Start by opening terminal then use these lines -
    - sudo apt update
  - Install python3 -
    - sudo apt install python3
  - Make sure you have pip installed -
    - sudo apt install python3-pip
  - Check if python3 and pip3 are installed -
    - python3 -V
    - pip3 -V
  - Install virtualenv -
    - pip3 install virtualenv
    - virtualenv os //name of virtual environment is os
  - Start the virtual environment -
    - source os/bin/activate
 
2.Install Important Libraries on the virtual environment -
  - pip install psutil
  - pip install PyQt5
  - pip install pyqtgraph
Other dependencies will be downloaded too with the above libraries .

3. Run the final code
  - There are 3 main files , please make sure that they are at same place , files are -
  - main3.ui, table3.ui and sys3.py
  - Now run the following commands -
    - source os/bin/activate
    - python sys3.py
<hr> 

## Outcomes -
- All the processes in the cpu are listed with their pIds, name, created time, memory,
memory%, threads, status. These information are fetched from the stat/statm files from
the corresponding folder of the process present in the proc file system.
- CPU & RAM utilization, networking speed(Kbps), battery consumption, processor
configuration, graphs corresponding to CPU & RAM are all displayed up to 2 decimal
places.
- An alarm system to indicate if the RAM utilization exceeds 95% to indicate it to the user.
- A GUI for all the output mentioned above providing an easy analysis to the user


<img width="302" alt="ss1" src="https://user-images.githubusercontent.com/103515662/209469215-0a1c06ea-4ec6-4afe-8779-88ab692e2ac0.png">


<hr> 

## For more information -
https://www.youtube.com/watch?v=g5jxJE0LJYA </br>
https://pypi.org/project/psutil/ </br>
https://pypi.org/project/pyqtgraph/ </br>
https://pypi.org/project/PyQt5/ </br>
https://github.com/earthinversion/SystemMonitorApp </br>

<hr>
______________________________________________________________________________
