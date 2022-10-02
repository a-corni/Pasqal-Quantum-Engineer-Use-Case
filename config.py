### Configuring the quantum machine
version = 1
center_freq = 100e6  #100 MHz
# Analog output 1
analog_output_1 = {1: {'offset': 0.0,
                       'delay': 0.0,
                       'shareable': True}}
# Use the Analog Output 1 port of an opx2 (has a delay)
ctrl_name = "OPX+"
OPX = {'type': 'opx2',
       'analog_outputs': analog_output_1}
controllers = {ctrl_name: OPX}

# One hardware element : AOM
AOM = {"singleInput": {"port": (ctrl_name, 1)},  # AOM is connected to first port of the controller
       "oscillator": "osc",  # Uses oscillator at frequency 100MHz
       "operations": {"amp_mod": "amp_mod_pulse"}}  # Receives 1 pulse
elements = {"AOM": AOM}

# One pulse of duration 10us
amp_mod_pulse = {"operation": "control",
                 "length": 1e4,
                 "waveforms": {"single": "amp_mod_wf"}}
pulses = {"amp_mod_pulse": amp_mod_pulse}

# Pulse amplitude 0.25V
amp_mod_wf = {"type": "constant", "sample": 0.25}
waveforms = {"amp_mod_wf": amp_mod_wf}

integration_weights = {}
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