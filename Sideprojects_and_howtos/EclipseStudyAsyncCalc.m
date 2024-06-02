clc
clear

% sun az/alt
SunAz = deg2rad(121.58);
SunAlt = deg2rad(66.77);

% GOES az/alt
GOESAz = deg2rad(171.4);
GOESAlt = deg2rad(46.5);

rad2deg(acos(sin(GOESAlt)*sin(SunAlt)+cos(GOESAlt)*cos(SunAlt)*cos(SunAz-GOESAz)))

