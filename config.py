# Configuring the quantum machine
version = 1
center_freq = 100e6  # 100 MHz
# Define Analog outputs
# Analog output 1 used to send a pulse to the AOM
analog_output_1 = {1: {'offset': 0.0,
                       'delay': 0.0}}
# Analog output 2 used to trigger the oscilloscope
analog_output_2 = {2: {'offset': 0.0,
                       'delay': 0.0}}
analog_outputs = {}
analog_outputs.update(analog_output_1)
analog_outputs.update(analog_output_2)

# Use the Analog Output 1 and 2 ports of an opx2 (has a delay)
ctrl_name = "OPX+"
OPX = {'type': 'opx2',
       'analog_outputs': analog_outputs}
controllers = {ctrl_name: OPX}

# Two hardware elements: AOM and oscilloscope
AOM = {"singleInput": {"port": (ctrl_name, 1)},  # AOM is connected to first port of the controller
       "oscillator": "osc",  # Uses oscillator at frequency 100MHz
       "operations": {"amp_mod": "amp_mod_pulse"}}  # Receives 1 pulse
oscillo = {"singleInput": {"port": (ctrl_name, 2)},  # oscilloscope connected to port 2 of the controller
           "oscillator": "osc",  # Uses same oscillator
           "operations": {"trigger": "trigger_pulse"}}  # Receives 1 pulse
elements = {"AOM": AOM,
            "oscillo": oscillo}

# Define the pulses
# AOM RF pulse has length 10us + 120ns
amp_mod_pulse = {"operation": "control",
                 "length": 10120,
                 "waveforms": {"single": "amp_mod_wf"}}
# Trigger pulse for oscillo (duration is below the duration of AOM RF pulse)
trigger_pulse = {"operation": "control",
                 "length": 9000,
                 "waveforms": {"single": "trigger_wf"}}
pulses = {"amp_mod_pulse": amp_mod_pulse,
          "trigger_pulse": trigger_pulse}

# Define the waveforms
# AOM RF Pulse has amplitude 0.25V
# Trigger Pulse has amplitude 0.25V (just interested in a square signal)
amp_mod_wf = {"type": "constant", "sample": 0.25}
trigger_wf = {"type": "constant", "sample": 0.25}
waveforms = {"amp_mod_wf": amp_mod_wf,
             "trigger_wf": trigger_wf}

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
