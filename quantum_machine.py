def dict_from_list_instances(list_instances):
    """
    Merges a list of classes whose get returns a dictionary into a dictionary

    Param:
        - list_class (List[Class]): List of classes
    Return:
        - output_dict (Dict): Dictionary resulting of the merging of the dictionaries of the classes
    """
    if list_instances is None:
        return {}
    output_dict = {}
    for instance in list_instances:
        output_dict.update(instance.get())
    return output_dict


class Analog_input:
    """
    Define an analog output of a Controller

    Attributes:
        - index (Int): Index of the analog output
        - offset (Float): Value of the offset in V, default to 0 (between -0.5 and 0.5)
        - gain_db (Int): Gain of the pre-ADC amplifier, in dB. Int between -12 and 20
        - shareable (Bool): [Not Implemented] Whether the port is shareable with other QM instances

    Method:
        - get: Returns a Dict with one element with key index and value a dict containing offset and delay
    """
    def __init__(self,
                 index,
                 offset=0.0,
                 gain_db=0,
                 shareable=True):
        self.index = index
        self.offset = offset
        self.gain_db = gain_db
        self.shareable = shareable

    def get(self):
        """
        Returns a dictionary with one element:
        Key : index
        Value : Dict with keys "offset" and "gain_db" and values of offset and gain_db
        """
        return {self.index: {"offset": self.offset,
                             "gain_db": self.gain_db}}


class Digital_input:
    """
    Define an analog output of a Controller

    Attributes:
        - threshold (Float): Index of the analog output
        - polarity (Float): Value of the offset in V, default to 0.
        - window (Int): Value of the delay in ns (only for opx2), default to 0.
        - shareable (Bool): [Not Implemented] Whether the port is shareable with other QM instances

    Method:
        - get: Returns a Dict with one element with key index and value a dict containing offset and delay
    """
    def __init__(self,
                 index,
                 threshold=0.0,
                 polarity="",
                 window=0,
                 shareable=True):
        self.index = index
        self.threshold = threshold
        self.polarity = polarity
        self.window = window
        self.shareable = shareable

    def get(self):
        """
        Returns a dictionary with one element:
        Key : index
        Value : Dict with keys "offset" and "delay" and values of offset and delays
        """
        return {self.index: {"threshold": self.threshold,
                             "polarity": self.polarity,
                             "window": self.window}}


class Analog_output:
    """
    Define an analog output of a Controller

    Attributes:
        - index (Int): Index of the analog output
        - offset (Float): Value of the offset in V, default to 0.
        - delay (Float): Value of the delay in ns (only for opx2), default to 0.
        - shareable (Bool): [Not Implemented] Whether the port is shareable with other QM instances

    Method:
        - get: Returns a Dict with one element with key index and value a dict containing offset and delay
    """
    def __init__(self,
                 index,
                 offset=0.,
                 delay=0.,
                 shareable=True):
        self.index = index
        self.offset = offset
        self.delay = delay
        self.shareable = shareable

    def get(self):
        """
        Returns a dictionary with one element:
        Key : index
        Value : Dict with keys "offset" and "delay" and values of offset and delays
        """
        return {self.index: {"offset": self.offset,
                             "delay": self.delay}}


class Digital_output:
    """
    Define an analog output of a Controller

    Attributes:
        - index (Int): Index of the analog output
        - shareable (Bool): [Not Implemented] Whether the port is shareable with other QM instances
    Method:
        - get: Returns a Dict with one element with key index and value a dict containing offset and delay
    """
    def __init__(self,
                 index,
                 shareable=True):
        self.index = index
        self.shareable = shareable

    def get(self):
        """
        Returns a dictionary with one element:
        Key : index
        Value : Dict with keys "offset" and "delay" and values of offset and delays
        """
        return {self.index: {}}


class Controller:
    """
    Defines a controller such as https://www.quantum-machines.co/opx+/

    Attributes:
        - name (String): Name of the controller
        - type (String): type of controller, initialize to "". ex: "opx1"
        - analog_outputs (List): List of Analog_output objects, default to None
        - digital_outputs (List): List of Digital_output objects, default to None
        - analog_inputs (List): List of Analog_input objects, default to None
        - digital_inputs (List): List of Digital_input objects, default to None
    """
    def __init__(self,
                 name,
                 analog_outputs=None,
                 digital_outputs=None,
                 analog_inputs=None,
                 digital_inputs=None,
                 ctrl_type="opx1"):
        self.name = name
        self.ctrl_type = ctrl_type
        self.analog_outputs = analog_outputs
        self.digital_outputs = digital_outputs
        self.analog_inputs = analog_inputs
        self.digital_inputs = digital_inputs

    def get(self):
        return {self.name: {"type": self.ctrl_type,
                            "analog_outputs": dict_from_list_instances(self.analog_outputs),
                            "digital_outputs": dict_from_list_instances(self.digital_outputs),
                            "analog_inputs": dict_from_list_instances(self.analog_inputs),
                            "digital_inputs": dict_from_list_instances(self.digital_inputs)}}


class Waveform:
    """
    Define the waveforms to be used in the pulses
    Either a constant value waveform or an arbitrary one

    Attributes:
          - name (String): Name of the waveform
          - wvf_type (String): Either "constant" or "arbitrary"
          - sample (Float): Float if type is constant
          - samples (List): List of samples if type is arbitrary
    """
    def __init__(self,
                 name,
                 wvf_type="constant",
                 sample=0.,
                 samples=0.):
        self.name = name
        self.wvf_type = wvf_type
        self.sample = sample
        self.samples = samples

    def get(self):
        if self.wvf_type == "constant":
            return {self.name: {"type": "constant",
                                "sample": self.sample}}
        elif self.wvf_type == "arbitrary":
            return {self.name: {"type": "arbitrary",
                                "samples": self.samples}}
        else:
            raise ValueError("""Waveform type must be "constant" or "arbitrary" """)


class DigitalWaveform:
    """
    Initialize a digital waveform
    """
    def __init__(self,
                 name,
                 digital_waveform):
        self.name = name
        self.digital_waveform = digital_waveform

    def get(self):
        return {self.name: self.digital_waveform}


class IntegrationWeight:
    """
    integration weights are used in the demodulation process as part of the measurement. Defined as a list of tuples
    First element: value of integration weight, Second element is duration (in ns, must be divisible by 4)
    Attributes:
          - name (String): Name of the integration weight being written
          - sin_weight (Double): Integration weight for sine, range [-2048; 2048] in steps of 2**(-15)
          - sin_duration (Int): Integration duration for sine in ns. Must be multiple of 4
          - cos_weight (Double): Integration weight for sine, range [-2048; 2048] in steps of 2**(-15)
          - cos_duration (Int): Integration duration for sine in ns. Must be multiple of 4
    """
    def __init__(self,
                 name,
                 sin_weight=0.,
                 sin_duration=0,
                 cos_weight=0.,
                 cos_duration=0):
        self.name = name
        self.sin_weight = sin_weight
        self.cos_weight = cos_weight
        self.sin_duration = sin_duration
        self.cos_duration = cos_duration

    def get(self):
        return {self.name: {"sine": [(self.sin_weight, self.sin_duration)],
                            "cosine": [(self.cos_weight, self.cos_duration)]}}


class Pulse:
    """
    Defines a Pulse

    Attributes:
          - name (String): Name of the Pulse
          - operation (String): Either "control" or "measurement"
          - length (Int): Pulse duration in ns
          - waveforms (Dict): Map input name (from element) and a waveform (from waveforms)
          - integration_heights (Dict): For a measurement pulse
          - digital_marker (String): [Not Implemented] Name of the digital waveform to be played with the pulse
    """
    def __init__(self,
                 name,
                 waveforms=None,
                 operation="control",
                 length=16,
                 integration_weights=None,
                 digital_marker=""):
        if operation != "control" and operation != "measurement":
            raise ValueError("""Possible values for operation: "control" or "measurement" """)
        if length < 16 or length > 2**31-1:
            raise ValueError("""pulse length must be between 16 and 2^31-1 ns""")
        self.name = name
        self.operation = operation
        self.length = length
        if waveforms is None:
            self.waveforms = {}
        else:
            self.waveforms = waveforms
        self.digital_marker = digital_marker
        self.integration_weights = integration_weights

    def get(self):
        if self.operation != "control" and self.operation != "measurement":
            raise ValueError("""Possible values for operation: "control" or "measurement" """)
        if self.length < 16 or self.length > 2**31-1:
            raise ValueError("""Pulse length must be between 16 and 2^31-1 ns""")
        if self.operation == "control":
            return {self.name: {"operation": self.operation,
                                "length": self.length,
                                "waveforms": self.waveforms}}
        else:
            return {self.name: {"operation": self.operation,
                                "length": self.length,
                                "waveforms": self.waveforms,
                                "integration_weights": self.integration_weights}}


class Mixer:
    """
    Configures the IQ mixer instance used by elements.
    List of Dict for various couples of intermediate and LO frequencies
    Attributes:
          - name (Str): name of the mixer
          - intermediate_frequency (Int): Intermediate Frequency
          - lo_frequency (Int): LO frequency
          - correction (List): 4 elements list specifying the correction matrix. Each element is a double in [-2,2]
    """
    def __init__(self,
                 name,
                 intermediate_frequency,
                 lo_frequency=0,
                 correction=None):
        self.name = name,
        self.intermediate_frequency = intermediate_frequency
        self.lo_frequency = lo_frequency
        if correction is None:
            self.correction = [0., 0., 0., 0.]
        else:
            self.correction = correction[:]

    def get(self):
        return {self.name: [{"intermediate_frequency": self.intermediate_frequency,
                             "lo_frequency": self.lo_frequency,
                             "correction": self.correction}]}


class Oscillator:
    def __init__(self,
                 name,
                 intermediate_frequency,
                 lo_frequency=0,
                 mixer=None):
        self.name = name
        self.lo_frequency = lo_frequency
        self.mixer = mixer
        self.intermediate_frequency = intermediate_frequency

    def get(self):
        output_dict = {self.name: {"intermediate_frequency": self.intermediate_frequency}}
        if self.mixer is None:
            output_dict[self.name]["mixer"] = self.mixer
        if self.lo_frequency==0:
            output_dict[self.name]["lo_frequency"] = self.lo_frequency
        return output_dict

#    def get(self):
#        return {self.name: {"intermediate_frequency": self.intermediate_frequency,
#                            "lo_frequency": self.lo_frequency,
#                            "mixer": self.mixer}}


class Element:
    def __init__(self,
                 name,
                 element):
        self.name = name
        self.element = element

    def get(self):
        return {self.name: self.element}

class Oscillator2:
    def __init__(self,
                 name,
                 intermediate_frequency):
        self.name = name
        self.intermediate_frequency = intermediate_frequency

    def get(self):
        return {self.name: {"intermediate_frequency": self.intermediate_frequency}}


class QuantumMachine:
    """
    Defines a Quantum Machine, the combination of the quantum system and the Operator-X (OPX).
    OPX is the control hardware of the Quantum Orchestration Platform (QOP).

    Attributes:
        - version: Must be set to 1 (documentation from 22/09/2022)
        - controllers: List of Controller objects
        - elements: List of Elements objects
    """
    def __init__(self,
                 controllers=None,
                 elements=None,
                 pulses=None,
                 waveforms=None,
                 digital_waveforms=None,
                 integration_weights=None,
                 mixers=None,
                 oscillators=None,
                 version=1):
        self.version = version
        self.controllers = controllers
        self.elements = elements
        self.pulses = pulses
        self.waveforms = waveforms
        self.digital_waveforms = digital_waveforms
        self.integration_weights = integration_weights
        self.mixers = mixers
        self.oscillators = oscillators

    def config(self):
        return {'version': self.version,
                'controllers': dict_from_list_instances(self.controllers),
                'elements': dict_from_list_instances(self.elements),
                'pulses': dict_from_list_instances(self.pulses),
                'waveforms': dict_from_list_instances(self.waveforms),
                'digital_waveforms': dict_from_list_instances(self.digital_waveforms),
                'integration_weights': dict_from_list_instances(self.integration_weights),
                'mixers': dict_from_list_instances(self.mixers),
                'oscillators': dict_from_list_instances(self.oscillators)}
