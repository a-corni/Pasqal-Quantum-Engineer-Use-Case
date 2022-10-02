from qm.QuantumMachinesManager import QuantumMachinesManager
from config import config as conf
from intensityVoltage import intensityVoltageprog as iVprog

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(conf)  # print configuration
    qmm = QuantumMachinesManager()  # creates a manager instance
    qm = qmm.open_qm(conf)  # opens a quantum machine with the specified configuration
    my_job = qm.execute(iVprog)  # execute program I(V)
    res_handles = my_job.result_handles
    res_handles.wait_for_all_values()
    a = res_handles.get('a').fetch_all()  # obtain V
    i = res_handles.get('i').fetch_all()  # obtain I
