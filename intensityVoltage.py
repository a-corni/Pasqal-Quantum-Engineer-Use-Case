from qm.qua import *
# QUA Program
# Curve of the laser beam intensity function of the amplitude of RF signal (in V)
# Using oscilloscope to measure photodiode signal
# Analog output ports have voltage range +-0.5V : ramp between 0 and 0.5V
# AOM has a rise time of 120ns

with program() as intensityVoltageprog:

    a = declare(fixed)  # multiplicative factor of the RF amplitude, between 0 and 2
    i = declare(fixed)  # intensity measured by the photodiode (actually, a voltage)

    with for_(a, 0.000, a < 2.0 + 0.001/2, a + 0.001):  # 2000 steps
        play('amp_mod_pulse'*amp(a), 'AOM')  # apply a pulse of voltage 0.25*a
        # assign(i, aom(i, a*0.25))  # intensity of the laser beam is changed after 120ns
        wait(120)  # When AOM has risen
        measure('meas_pulse',  # Measure the intensity of the photodiode
                'photodiode',
                None,
                integration.full("integration",  # Compute the average of the intensity over 10us after the 120ns
                                 "out1",  # average intensity is obtained from analog_input_1
                                 i))  # and stored in variable i
        save(a, 'a')
        save(i, "i")
