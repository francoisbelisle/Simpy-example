A simple example of discret traffic signal event simulation using Simpy.
The events in this simulation consist of : 
- cars arriving
- traffic signal changing states
- building, interrupting and relieving the traffic queues as they form.

The story goes a little something like this :
Cars send a message to the traffic controler when they arrive
Depending on its state, the traffic controler either:
- let's the car go (it's green for the cars movement)
- Puts the car in a queue (if there already is a queue or if it's red)

In this example, the traffic signal has two states:
- a 15 second WBT
- a 45 second SBT
Both flows for the WBT and SBT movements are randomly generated
about every 10 seconds.
Of course, all values should be changed to more realistic settings

usage : python simpy-example.py

Simulation output is:
time 0 : TRAFFIC STATE CHANGING WBT
time 0 : car 1 SBT has arrived
time 0 : car 1 SBT in queue
time 3 : car 2 SBT has arrived
time 3 : car 2 SBT in queue
time 5 : car 3 SBT has arrived
time 5 : car 3 SBT in queue
time 10 : car 1 WBT has arrived
time 10 : car 1 WBT has left
time 15 : TRAFFIC STATE CHANGING SBT
time 19 : car 1 SBT has left
time 19 : car 4 SBT has arrived
time 19 : car 4 SBT in queue
time 20 : car 2 SBT has left
time 21 : car 2 WBT has arrived
time 21 : car 2 WBT in queue
time 22 : car 3 SBT has left
time 23 : car 3 WBT has arrived
time 23 : car 3 WBT in queue
time 24 : car 4 WBT has arrived
time 24 : car 4 WBT in queue
time 24 : car 5 SBT has arrived
time 24 : car 5 SBT in queue
time 25 : car 4 SBT has left
time 26 : car 5 WBT has arrived
time 26 : car 5 WBT in queue
time 28 : car 5 SBT has left
time 28 : car 6 WBT has arrived
time 28 : car 6 WBT in queue
time 35 : car 6 SBT has arrived
time 35 : car 6 SBT has left
time 37 : car 7 WBT has arrived
time 37 : car 7 WBT in queue
time 37 : car 8 WBT has arrived
time 37 : car 8 WBT in queue
time 51 : car 7 SBT has arrived
time 51 : car 7 SBT has left
time 54 : car 9 WBT has arrived
time 54 : car 9 WBT in queue
time 58 : car 10 WBT has arrived
time 58 : car 10 WBT in queue
time 60 : TRAFFIC STATE CHANGING WBT
time 60 : car 11 WBT has arrived
time 60 : car 11 WBT in queue
time 63 : car 8 SBT has arrived
time 63 : car 8 SBT in queue
time 64 : car 12 WBT has arrived
time 64 : car 12 WBT in queue
time 64 : car 2 WBT has left
time 64 : car 9 SBT has arrived
time 64 : car 9 SBT in queue
time 65 : car 13 WBT has arrived
time 65 : car 13 WBT in queue
time 68 : car 3 WBT has left
time 72 : car 4 WBT has left
time 74 : car 10 SBT has arrived
time 74 : car 10 SBT in queue
time 75 : TRAFFIC STATE CHANGING SBT
time 77 : car 8 SBT has left
time 80 : car 9 SBT has left
time 81 : car 14 WBT has arrived
time 81 : car 14 WBT in queue
time 84 : car 10 SBT has left
time 91 : car 15 WBT has arrived
time 91 : car 15 WBT in queue
time 110 : car 11 SBT has arrived
time 110 : car 11 SBT has left
time 111 : car 16 WBT has arrived
time 111 : car 16 WBT in queue
time 118 : car 12 SBT has arrived
time 118 : car 12 SBT has left
time 119 : car 13 SBT has arrived
time 119 : car 13 SBT has left
