"""Calculates the resistors needed to scale down an input voltage range"""


def calculate_voltage_range(min_in, max_in, rf=47_000, radj=180_000):
    rin = 100_000
    adj_v = -10

    min_out = abs((rf / rin * min_in) + (rf / radj * adj_v))
    max_out = abs((rf / rin * max_in) + (rf / radj * adj_v))

    return min_out, max_out


R_SERIES = set(
    [
        1.00,
        1.05,
        1.10,
        1.15,
        1.21,
        1.27,
        1.33,
        1.40,
        1.47,
        1.54,
        1.62,
        1.69,
        1.78,
        1.87,
        1.96,
        2.05,
        2.15,
        2.26,
        2.37,
        2.49,
        2.61,
        2.74,
        2.87,
        3.01,
        3.16,
        3.32,
        3.48,
        3.65,
        3.83,
        4.02,
        4.22,
        4.42,
        4.64,
        4.87,
        5.11,
        5.36,
        5.62,
        5.90,
        6.19,
        6.49,
        6.81,
        7.15,
        7.50,
        7.87,
        8.25,
        8.66,
        9.09,
        9.53,
    ]
)
R_SERIES.update(
    [
        1.0,
        1.1,
        1.2,
        1.3,
        1.5,
        1.6,
        1.8,
        2.0,
        2.2,
        2.4,
        2.7,
        3.0,
        3.3,
        3.6,
        3.9,
        4.3,
        4.7,
        5.1,
        5.6,
        6.2,
        6.8,
        7.5,
        8.2,
        9.1,
    ]
)


def calculate_component_values(min_in, max_in):
    # inverting op amp
    max_out = 0
    min_out = 3.3

    rin = 100_000
    adj_base = 100_000
    rf_base = 10_000
    adj_v = -10

    for rfmul in R_SERIES:
        for adjmul in R_SERIES:
            rfval = rfmul * rf_base
            adjval = adjmul * adj_base

            min_out_candidate = abs((rfval / rin * min_in) + (rfval / adjval * adj_v))
            max_out_candidate = abs((rfval / rin * max_in) + (rfval / adjval * adj_v))
            zero_v_value = abs((rfval / rin * 0) + (rfval / adjval * adj_v))

            if abs(min_out_candidate - min_out) > 0.1:
                continue

            if abs(max_out_candidate - max_out) > 0.1:
                continue

            print(
                f"Vmin: {min_out_candidate:.2f} Vmax: {max_out_candidate:.2f} Spread {abs(max_out_candidate-min_out_candidate):.2f} V0: {zero_v_value:.2f} Rf: {rfval:.0f} Radj: {adjval:.0f}"
            )


calculate_component_values(-5, +5)
