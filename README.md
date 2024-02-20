# UndergradResearchECE-Database

This part of the project is meant to get the most accurate and most recent data from SpaceTrack.org 

This is an edited copy of example code on SpaceTrack.org to work with the SWIFT-UDP project

there is a couple of important elements such as the configuration file with Jackson's SpaceTrack.org login information but any login information should work as long as the configuration file is updated. 

One thing to note is the name of the python script as DatabaseGeneratorV1 even though we are using Github to keep the database up to date, having it named V1 is useful in case Jackson's credentials gets flagged with an API violation. The same code would work but that specific script would not. This information was found after trying to debug the first iteration of the program a day after Jackson recieved an API violation. The main goal is to never get API violations but if they do happen while debugging (what caused the first API violation) there is an easy solution in changing the name of the script to DatabaseGeneratorV2 and so on. 

There is a text file that the python script writes to. The file is temporary and is wiped after every loop of the main program. The file always starts with the date and time the file was generated.
You might notice it has some change notifications this is because if I run the code Github notices a change in the file and exports it along with the changed code.

There are a couple TODOs ranked in order of most important
!!! Add way for the geometry engine to stop the data collection loop (not the pause portion) and close the text file. If the text file isn't closed some data is lost. 

(completed 2/17) Find a new query that only gets the most recent OMM data from space track. Currently the code is getting all historical data which was fine for the source code which only tracked starlink satellites with less historical data but not so much for iridum. 

!! add way for the code to check if a satellite has decayed, this will likely be checking the epoch and if that epoch was more than a year (month?) ago the code will not output its data to the text file.

! Add the ability to get starlink satellites. I don't think this will be super hard but I'm probably going to make another text file for that (awaiting input). 

