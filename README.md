[![Build Status](https://circleci.com/gh/clouden90/schedulecheck/tree/develop.svg?style=svg)](https://circleci.com/gh/clouden90/schedulecheck/tree/develop)

[schedulecheck](https://github.com/clouden90/schedulecheck.git) is a simple python app to check schedule conflict. The major files are:

- **`example/schedule.txt`** - The example txt file contains meeting times.
- **`reference/*_ref.txt`** - The reference answers based on example/schedule.txt.
- **`./src/schedulecheck/bin/schedulecheck.py`** - Main driver that read input file and find conflicting schedule. 
- **`./src/schedulecheck/meetinglib.py`** - Meetinglib library that contains algorithms of schedule-conflict check. 
- **`./src/schedulecheck/test_meetinglib.py`** - automated tests for the conflicts_check functions in Meetinglib library.

# Algorithms
Two algorithms are implemented: 
- Method1 (conflicts_check1): A simple algorithm is used to check the conflicts. First, the schedules are sorted by end time. Then for loops are used by checking 
  the first meeting and comparing its end time to the start time of the second meeting. If they overlap, the pair will be added in conflict list and keep comparing 
  the first schedule to third, forth ones until no more overlap. Then it continue by comparing the second schedule to the following meetings, and so on.
  This method could run close to O(nlogn) (sorting in python takes O(nlogn)) if there are only a few conflicting meetings and that they are of similar interval
  length. However, worst case for this method would be O(n^2) if there are too many confliciting events.
  
- Method2 (conflicts_check2): A `Interval Tree` algorithm is used to slove the problem. First, a Interval Tree is created and initialized with the first schedule. 
  For the rest of the appointments, it will check if the current appointment conflicts with any of the existing appointments in Interval Tree. If conflicts, the 
  pair will be added in conflict list. Then the current appointment will be inserted in Interval Tree, and move to the next one and so on. The complexity of this 
  method is O(nlogn).

# Installation
Assuming you have python3 already installed, `schedulecheck` can be downloaded and installed by running

```bash
# download source code
git clone https://github.com/clouden90/schedulecheck.git
cd schedulecheck

# install
pip install .

# run the driver with simple test file
schedulecheck -h # provide some useful information about how to use the driver 
schedulecheck -f ./example/schedule.txt -o ./schedule_check.txt -m 1

Then you can check the output `schedule_check.txt`, it should contain soemthing like this with method1:
10:15-10:30 and 10:00-11:00 conflict
11:30-11:45 and 11:00-13:00 conflict
11:00-13:00 and 12:00-13:00 conflict

or lik this with method2:
10:15-10:30 and 10:00-11:00 conflict
12:00-13:00 and 11:00-13:00 conflict
11:30-11:45 and 11:00-13:00 conflict
```

# For developer/contributer
If you would like to contribute/add a new function in `meetinglib.py`, you should also add an automated test associated to that function in `test_meetinglib.py` for ci test.
