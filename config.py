# Configuring the quantum machine
version = 1
center_freq = 100e6  # 100 MHz
# Define Analog outputs
# Analog output 1 used to send a pulse to the AOM
analog_output_1 = {1: {'offset': 0.0,
                       'delay': 0.0}}
# Analog input 1 used to acquire data from the photo-diode
analog_input_1 = {1: {'offset': 0.0,
                      'gain_db': 0.0}}

# Use the Analog Output 1 and Analog Input 1 ports of an opx2 (has a delay)
ctrl_name = "OPX+"
OPX = {'type': 'opx2',
       'analog_outputs': analog_output_1,
       "analog_inputs": analog_input_1}
controllers = {ctrl_name: OPX}

# Two hardware elements: AOM and photo-diode
AOM = {"singleInput": {"port": (ctrl_name, 1)},  # AOM is connected to first port of the controller
       "oscillator": "osc",  # Uses oscillator at frequency 100MHz
       "operations": {"amp_mod": "amp_mod_pulse"}}  # Receives 1 pulse
photodiode = {"outputs": {"out1": ("con1", 1)},  # measure on input port 1
              "oscillator": "osc",  # Uses same oscillator
              "operations": {"meas": "meas_pulse"}}  # Performs measurement operation
elements = {"AOM": AOM,
            "photodiode": photodiode}

# Define the pulses
# AOM RF pulse has length 10us + 120ns
amp_mod_pulse = {"operation": "control",
                 "length": 10120,
                 "waveforms": {"single": "amp_mod_wf"}}

# Measurement pulse for the photodiode
# Demodulated with cosine
meas_pulse = {"length": 10000,
              "operation": "measurement",
              "integration_weights": {"integration": "integration"}}
pulses = {"amp_mod_pulse": amp_mod_pulse,
          "meas_pulse": meas_pulse}

# Define the waveforms
# AOM RF Pulse has amplitude 0.25V
amp_mod_wf = {"type": "constant", "sample": 0.25}
waveforms = {"amp_mod_wf": amp_mod_wf}

# Define the integration weights
# Want to avoid overflow: integration weights such that:
# - raw ADC data scaled to between -0.5 and 0.5 multiplied by weights has result between -2 and 2.
# - The sum of the multiplication above is smaller than 2**16
# If we assume constant weights w=1, and a constant signal a[n] = a*cos(\omega_{IF} t_s n)
# then result is d = \frac{a N cos(\phi) 2{-12}}{2}
# The signal is constant and not modulated. We perform the average by integration during 10 \mu s
# Weights used for integration are defined in cosine.
integration_weights = {"integration": {"cosine": [(1/10000, 10000)],
                                       "sine": [(0.0, 10000)]}}
mixers = {}

# Frequency oscillation 100MHz
osc = {"intermediate_frequency": center_freq}
oscillators = {"osc": osc}

config = {"version": version,
          "controllers": controllers,
          "elements": elements,
          "pulses": pulses,
          "waveforms": waveforms,
          "integration_weights": integration_weights,
          "mixers": mixers,
          "oscillators": oscillators}
