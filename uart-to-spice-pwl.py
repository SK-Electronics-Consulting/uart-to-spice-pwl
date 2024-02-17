#!/usr/bin/python
from pathlib import WindowsPath

# Issue with second start char's start bit.
'''
Comms Definitions
'''
baudrate = 1_000_000
num_databits = 8
parity = 'n'
num_stopbits = 1

init_quiet_time = 100.0  # microseconds
inter_byte_quiet_time = 1.0  # microseconds

'''
PHY definitions
'''
lvl_1 = 0.1
lvl_0 = 0.0
idle_state = lvl_1
rise_time = 0.001  # microseconds
fall_time = rise_time  # microseconds

'''
Calculated values
'''
bit_time: float = 1 / baudrate / 1e-6  # microseconds


def create_bit(bit_val: bool) -> str:
    lvl = lvl_1 if bit_val else lvl_0
    time_del = rise_time if bit_val else fall_time
    return f'+{time_del:.4f}u {lvl}\n+{(bit_time - time_del):.4f}u {lvl}\n'


def create_byte_char(char_val: str) -> str:
    pwl_str = ""
    par_val = False

    pwl_str += create_bit(False)  # Start bit

    for bit_num in range(num_databits):
        bit_val = bool((ord(char_val) >> bit_num) & 1)
        par_val = par_val ^ bit_val
        pwl_str += create_bit(bit_val)

    for ii in range(num_stopbits):
        pwl_str += create_bit(True)

    pwl_str += '\n'  # newline for the sake of organizing the file with a blank line
    return pwl_str


def create_byte_int(int_val: int) ->str:
    pwl_str = ""
    par_val = False

    pwl_str += create_bit(False)  # Start bit

    for bit_num in range(num_databits):
        bit_val = bool((int_val >> bit_num) & 1)
        par_val = par_val ^ bit_val
        pwl_str += create_bit(bit_val)

    for ii in range(num_stopbits):
        pwl_str += create_bit(True)

    pwl_str += '\n'  # newline for the sake of organizing the file with a blank line
    return pwl_str


def create_string_pwl(str_val: str) -> str:
    pwl_str = ""
    for chars in str_val:
        pwl_str += create_byte_char(chars)
    return pwl_str


def create_idle_pwl(duration: int) ->str:
    """
    Creates a delay at the idle state of duration length in microseconds.

    :param duration: duration of idle time in microseconds
    :return: pwl string to write
    """
    time_del = rise_time if idle_state else fall_time
    return f'+{time_del:.4f}u {idle_state}\n+{(duration - time_del):.4f}u {idle_state}\n\n'


if __name__ == '__main__':
    output_file_path = WindowsPath('C:/dev_SK/jamystor/New Text Document_.txt')
    with open(output_file_path, "w") as file:
        file.write(create_idle_pwl(100))
        file.write(create_string_pwl("abc"))
        file.write(create_byte_int(85))  # 0x55 in decimal
