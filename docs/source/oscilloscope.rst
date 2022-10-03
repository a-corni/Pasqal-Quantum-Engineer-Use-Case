2. Writing a QUA program to calibrate your setup
************************************************

Configuration
=============

A new element is introduced in the setup: an oscilloscope. Its channel 2 is connected to the analog output port number 2 of the OPX controler.
A RF signal of frequency 100MHz and duration :math:`9\mu s` is sent to the oscilloscope.
To take into account the raise time for the AOM, the RF pulse has a longer duration of :math`10.12\mu s`.

Not written in the config file, the photo-diode is plugged on the first channel of the oscilloscope.

Program
=======

The experiment is repeated for different values of the amplitude sent to the AOM. The amplitude is ramped from 0 to 0.5V with steps of size 0.00025V (2000 steps).
The RF pulse is sent to the AOM. 120ns later, the trigger pulse is sent to the port `channel 2` of the oscilloscope, launching the acquisition on `channel 1`. We acquire :math:`10\mu s` of signal and make the mean of it. When both operations are over, repeat the experiment.
We measure intensity function of the voltage.

