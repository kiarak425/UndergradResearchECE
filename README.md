# MOSAIC

## Database

The database of the MOSAIC project is meant to get the most accurate and recent data from SpaceTrack.org.

## Geometry Engine

The Geometry Engine is meant to parse through the TLE file in the Database Engine Repository. Furthermore, this iterates throughout the TLE files to get the most recent data and be able to create a list of satellite information.

## Socket

This socket is a command-line tool designed for various satellite tracking operations. It provides the ability to perform tasks such as checking server status, locating satellites, retrieving TLEs (Two-Line Element) data, obtaining long names of satellites, and predicting the next pass of a satellite. This code is paired with a Geometry Engine and a Back-End Database.
