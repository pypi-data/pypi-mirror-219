# openHySim Package

This is a package contains the OpenSeesPy 3.5.1 and OpenFrescoPy 2.7.2 (x64 bit version) together, and some additional personal subroutines (such as, ritz command for derive stiffness and mass matrix) and some features might happend in OpenSees and OpenFresco during past decade.

In 2023, since the Matlab/Simulink 2021a is the last version surpport xpcTarget, we moved the SpeedGoat realtime machine into newer version of Matlab/Simulink with micro-core system used now in simulink real-time modules for additional features (such as the AI/ML/RL toolbox in simulink real-time machine). However, for hybrid testing, we found the openfrescoPy had not been developed or transitted into newer python environment. This missing made this bundle of toolkits happend.

We colected most recently published api files (in Windows x64 environment), and improved openfrescopy, finally, combined the two (OpenSeesPy and OpenFrescoPy) into one .pyd dynamic library.

For students, who are not quite understand how to configure the hybrid testing environment, this toolkit will lower down the learnning.

contact: neallee@tju.edu.cn
