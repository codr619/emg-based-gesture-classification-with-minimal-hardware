from machine import ADC
import time
adc = ADC(27)
def EMGFilter(input_value):
  """
  This function implements a 4th-order band-pass filter using biquad sections.

  Args:
      input_value: The input signal value (float).

  Returns:
      The filtered output value (float).
  """

  # Filter coefficients (these are specific to the C++ code and might need adjustment)
  a0_1, a1_1, a2_1 = 0.01856301, 0.03712602, 0.01856301
  b1_1, b2_1 = -0.05159732, -0.36347401

  a0_2, a1_2, a2_2 = 1.00000000, -2.00000000, 1.00000000
  b1_2, b2_2 = -0.53945795, -0.39764934

  a0_3, a1_3, a2_3 = 1.00000000, 2.00000000, 1.00000000
  b1_3, b2_3 = -0.47319594, -0.70744137

  a0_4, a1_4, a2_4 = 1.00000000, -2.00000000, 1.00000000
  b1_4, b2_4 = -1.00211112, -0.74520226

  # State variables (initialized to 0 for consistency)
  z1_1, z2_1 = 0.0, 0.0
  z1_2, z2_2 = 0.0, 0.0
  z1_3, z2_3 = 0.0, 0.0
  z1_4, z2_4 = 0.0, 0.0

  # Filter calculation
  x1 = input_value - b1_1 * z1_1 - b2_1 * z2_1
  output = a0_1 * x1 + a1_1 * z1_1 + a2_1 * z2_1
  z2_1 = z1_1
  z1_1 = x1

  x2 = output - b1_2 * z1_2 - b2_2 * z2_2
  output = a0_2 * x2 + a1_2 * z1_2 + a2_2 * z2_2
  z2_2 = z1_2
  z1_2 = x2

  x3 = output - b1_3 * z1_3 - b2_3 * z2_3
  output = a0_3 * x3 + a1_3 * z1_3 + a2_3 * z2_3
  z2_3 = z1_3
  z1_3 = x3

  x4 = output - b1_4 * z1_4 - b2_4 * z2_4
  output = a0_4 * x4 + a1_4 * z1_4 + a2_4 * z2_4
  z2_4 = z1_4
  z1_4 = x4

  return output

samplingFreq=2000
samplingTime=1/samplingFreq
duration = 5  #
start_time = time.time()
while time.time() - start_time < duration:
    digital_value = adc.read_u16()     
    #print("ADC value=",digital_value)
    voltage_value=3.3*(digital_value/65535)
    filtered=EMGFilter(voltage_value)
    print((300*filtered),9.5)
    time.sleep(samplingTime)