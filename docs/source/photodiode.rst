3. Measuring with the OPX+
**************************

Configuration
=============

The oscilloscope is replaced by the photo-diode. This time, we don't use an output port but an input port of the OPX+.
We create a measurement pulse that will only acquire data. We connect to this pulse a post-processing tool :class:`integration` with `integration_weights` :math:`\frac{1}{t_{meas}}` with :math:`t_{meas}` the duration of the measurement.
Output port 1 of OPX+ is still connected to the AOM.

Program
=======

The program measures the intensity received by the photo-diode for various amplitudes of the RF pulse sent to the AOM. These amplitudes range from 0V to 0.5V with steps 0.00025V.
For each amplitude, the experiment starts by sending a RF pulse to the AOM. 120ns later, we start measuring the photo-diode. This measure lasts :math`10\mu s`. When it is over, the signal is averaged using :class:`integration`: the amplitudes are summed and divided by the acquisition time. The output is saved in the variable `i`.
