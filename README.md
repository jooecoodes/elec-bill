This is our final PIT for the first semester in CS111 Computer Programming 1

### Members:
<ol>
  <li>Villacorta</li>
  <li>Ello</li>
  <li>Bologa</li>
  <li>Recopelacion</li>
  <li>Moneva</li>
  <li>Gomez</li>
  <li>Tangarocan</li>
</ol>

### Initialization
You can run the run.bat file to run the program immediately through the terminal
```bash
.\run
```

### Functionality:
<p>
  This program takes the total bill by taking the current records of your electricity bill
and subtracting it to the previous record to get the base consumption (if you have already set the record otherwise it is set 
to 0 by default) and then calculates the total bill to be payed by multiplying the base consumption with the predetermined rates (generation, transmission, system loss, etc.). If the base consumption goes over the threshold for a residential base consumption (e.g. in this case 1500), the exceeded amount will be taken and calculated with the commercial rate and then added to the residential base consumption calculated with the residential rate to get total amount of the bill. The program stores all data inside 2 .csv files, one is for the general information of the user, and the other one is for their records (which will be named after their IDs). If the first name and the last name matches some data stored during input, it will automatically retrieve the data such as their previous reading to subract with the current reading and get the base consumption.  
</p>

![menu](https://github.com/jooecoodes/elec-bill/blob/master/assets/showcase.png?raw=true)

### Improvements:
There's so much room for improvements in this program including the code itself and make it more efficient and concise. It's not that bad but it's definitely not that well-written resourcefully.