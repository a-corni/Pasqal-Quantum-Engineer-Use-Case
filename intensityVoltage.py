from qm.qua import *
# QUA Program
# Curve of the laser beam intensity function of the amplitude of RF signal (in V)
# Using oscilloscope to measure photodiode signal
# Analog output ports have voltage range +-0.5V : ramp between 0 and 0.5V
# AOM has a rise time of 120ns


def aom(i_input, v_rf):
    """
    Models the AOM using page 6 of http://www.aaoptoelectronic.com/wp-content/uploads/documents/AAOPTO-Theory2013-4.pdf
    Efficiency function of input voltage is modeled as a sinus of period 1
    Input:
        - i_input (Float): intensity of the input beam
        - v_rf (Float): voltage of the input RF
    Output:
        - i_output (Float): i_input*Efficiency(v_RF) with Efficiency a sinus.
    """
    # wait(120) # it takes 120ns to reach this value
    return i_input * Math.sin(v_rf)


with program() as intensityVoltageprog:

    a = declare(fixed)  # multiplicative factor of the RF amplitude, between 0 and 2
    i = declare(fixed)  # intensity of laser beam

    with for_(a, 0.000, a < 2.0 + 0.001/2, a + 0.001):  # 2000 steps
        assign(i, 1.)
        play('amp_mod_pulse'*amp(a), 'AOM')  # apply a pulse of voltage 0.25*a
        assign(i, aom(i, a*0.25))  # intensity of the laser beam is changed after 120ns
        wait(120)  # When AOM has risen
        play('trigger_pulse', 'oscillo')  # trigger acquisition at the oscilloscope
        # Port 2 of opx+ is connected on channel 2 of oscilloscope
        # Photo-diode converts intensity into voltage.
        # Voltage is acquired by oscilloscope on channel 1 triggered by channel 2
        # Acquire points during 10us on the oscilloscope. Take the mean.
        save(i, "i")
        save(a, 'a')
