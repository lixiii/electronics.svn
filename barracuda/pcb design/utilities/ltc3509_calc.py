#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

desired_min_input_voltage = 0
desired_norm_input_voltage = 20
desired_max_input_voltage = 24
desired_output_voltage = 5
desired_switching_freq = 2e6
desired_load_current = 700e-3
desired_inductance = 15e-6
desired_capacitor_type = 'ceramic'
desired_voltage_ripple = 1e-3
desired_input_capacitance = 2e-6
desired_short_protection = 0

# component dependant constants
diode_forward_voltage = 0.40

# temperature dependant constants
min_on_time = 90e-9
min_off_time = 80e-9 # TODO look this up
switch_current_limit = 1.15

# constants
switch_voltage_drop = 0.32


def calc_ptp_ripple(dc, vout, l):
    return (1 - dc) * (vout + diode_forward_voltage) / (l * desired_switching_freq)


if __name__ == '__main__':
    min_input_voltage = desired_min_input_voltage
    norm_input_voltage = desired_norm_input_voltage
    max_input_voltage = desired_max_input_voltage
    output_voltage = desired_output_voltage
    switching_freq = desired_switching_freq
    load_current = desired_load_current
    inductance = desired_inductance
    boost_pin_cap = None
    voltage_ripple = desired_voltage_ripple
    output_capacitance = None
    input_capacitance = None
    short_protection = desired_short_protection

    # calculate absolute maximum duty cycle limits
    min_duty_cycle = switching_freq * min_on_time
    max_duty_cycle = 1 - min_off_time * switching_freq
    normal_duty_cycle = (output_voltage + diode_forward_voltage) / (norm_input_voltage - switch_voltage_drop + diode_forward_voltage)

    # update voltage limits based on duty cycle limits
    min_input_voltage = max((output_voltage + diode_forward_voltage) / (max_duty_cycle) - diode_forward_voltage + switch_voltage_drop, min_input_voltage)
    max_input_voltage = min((output_voltage + diode_forward_voltage) / (min_duty_cycle) - diode_forward_voltage + switch_voltage_drop, max_input_voltage)

    # re-update the min/max duty cycles based on voltage limits
    min_duty_cycle = (output_voltage + diode_forward_voltage)/(max_input_voltage - switch_voltage_drop + diode_forward_voltage)
    max_duty_cycle = (output_voltage + diode_forward_voltage)/(min_input_voltage - switch_voltage_drop + diode_forward_voltage)
    
    print('duty cycle')
    print('    minimum: %.02f' % (min_duty_cycle))
    print('    normal: %.02f' % (normal_duty_cycle))
    print('    maximum: %.02f' % (max_duty_cycle))
    
    print('input voltage')
    print('    minimum: %.02fV' % (min_input_voltage))
    print('    normal: %.02fV' % (norm_input_voltage))
    print('    maximum: %.02fV' % (max_input_voltage))


    # calcualate required boost pin capacitor value

    boost_pin_cap = (1 / (10 * (switching_freq / 1e6))) / 1e6

    print('boost pin capacitor: %.02fuF' % (boost_pin_cap * 1e6))
    if boost_pin_cap <= 0.1e-6:
        print('     0.1uF capacitor works well')

    # inductor selection

    print('inductor')

    # initial guess
    inductor_first_choice = (output_voltage + diode_forward_voltage) * (2.1e6 / switching_freq) / 1e6
    print('    first choice: %.02fuH' % (inductor_first_choice * 1e6))

    # desired choice
    print('    desired choice: %.02fuH' % (desired_inductance * 1e6))

    # static properties
    inductor_rms_current_min = load_current
    inductor_saturation_current_min = load_current * 1.3
    inductor_series_resistance_max = 0.15
    print('    minimum \'maximum load current\': %.02fA' % (inductor_rms_current_min))
    print('    minimum saturation current: %.02fA' % (inductor_saturation_current_min))
    print('    maximum series resistance (DC): %.02fΩ' % (inductor_series_resistance_max))

    # print worst case peak-to-peak ripple current for inductor
    inductor_ptp_ripple_current = calc_ptp_ripple(min_duty_cycle, output_voltage, desired_inductance)
    inductor_peak_current = desired_load_current + inductor_ptp_ripple_current

    print('    peak-to-peak ripple current: %.02fA' % (inductor_ptp_ripple_current))
    print('    peak inductor & switch current: %.02fA' % (inductor_peak_current))

    # check this doesn't exceed the max current for the ltc3509
    if inductor_peak_current > switch_current_limit:
        print('        this exceeds the maximum switch current for the LTC3509')
    else:
        print('        within LTC3509 switch current limit')

    # calculate minimum required inductance
    inductor_theoretical_min = ((1 - min_duty_cycle)/switching_freq)*((output_voltage + diode_forward_voltage)/(switch_current_limit - load_current))
    print('    theoretical minimum inductance: %.02fuH' % (inductor_theoretical_min * 1e6))

    if desired_short_protection == 1:
        # values for short circuit protection
        print('    short protection')
        shorted_current = (max_input_voltage * min_on_time) / inductance + 1.1
        print('        minimum saturation current: %.02fA' % (shorted_current))
        print('        general rule: minimum saturation current: 1.8A')

        inductor_saturation_current_min = max(inductor_saturation_current_min, shorted_current, 1.8)

    # for robust operation
    if max_input_voltage > 30:
        print('    robust operation')
        inductance = max(inductance, 4.2e-6)
        print('        minimum inductance: 4.2uH')
        inductor_saturation_current_min = max(inductor_saturation_current_min, 1.8)
        print('        minimum saturation current: 1.8A')

    # find minimum inductance to satisfy 30% rule
    print('    30% ripple current rule')
    inductance_30_rule = (1 - min_duty_cycle)*((output_voltage + diode_forward_voltage)/(switch_current_limit * 0.3 * switching_freq))
    if inductance_30_rule > inductance:
        inductance = max(inductance, inductance_30_rule)
        print('        new inductance to satisfy 30%% rule: %.02fuH' % (inductance * 1e6))
    else:
        print('        already met')

    # minimum inductance to stop subharmonic oscillations
    print('    subharmonics rule')
    if max_duty_cycle > 0.5:
        inductance_subharmonic = ((output_voltage * diode_forward_voltage)*1.4/(switching_freq / 1e6))/1e6
        if inductance_subharmonic > inductance:
            inductance = max(inductance, inductance_subharmonic)
            print('        new inductance to satisfy subharmonic rule: %.02fuH' % (inductance * 1e6))
        else:
            print('        already met')
    else:
        print('        not required')

    print('output capacitor')
    print('    desired type: %s' % desired_capacitor_type)

    if desired_capacitor_type == 'ceramic':
        output_capacitance = inductor_ptp_ripple_current / (8 * switching_freq * voltage_ripple)
        print('        capacitance to meet voltage ripple requirements: %.2fuF' % (output_capacitance * 1e6))
    else:
        max_esr = voltage_ripple / inductor_ptp_ripple_current
        print('        maximum ESR: %.02fmΩ' % (max_esr * 1e3))

    capacitor_rms_current = inductor_ptp_ripple_current / math.sqrt(12)
    print('    RMS current (not usually a concern): %.02fmA' % (capacitor_rms_current * 1e3))

    capacitance_energy_storage = 10 * inductance * math.pow((switch_current_limit / output_voltage), 2)
    if capacitance_energy_storage < output_capacitance:
        print('    energy storage requirements met')
    else:
        output_capacitance = max(output_capacitance, capacitance_energy_storage)
        print('    capacitance to meet energy storage requirements: %.02fuH' % (output_capacitance * 1e6))
    
    print('diode')

    diode_current = load_current * (max_input_voltage - output_voltage) / max_input_voltage
    print('    worst case average current: %.02fA' % (diode_current))

    if desired_short_protection == 1:
        print('    short protection')
        diode_current = switch_current_limit
        print('        worst case average current: %.02fA' % (diode_current))

    print('final values')
    print('    inductor')
    print('        value: %.02fuH' % (inductance * 1e6))
    print('        minimum \'maximum load current\': %.02fA' % (inductor_rms_current_min))
    print('        minimum saturation current: %.02fA' % (inductor_saturation_current_min))
    print('        maximum series resistance (DC): %.02fΩ' % (inductor_series_resistance_max))
    print('    output capacitor')
    print('        type: %s' % desired_capacitor_type)
    print('        value: %.02fuF' % (output_capacitance * 1e6))
    print('        RMS current (not usually a concern): %.02fmA' % (capacitor_rms_current * 1e3))
    print('    diode')
    print('        average current: %.02fA' % (diode_current))
