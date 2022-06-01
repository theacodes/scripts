"""
Calculates the output resistors required to scale up a voltage to a specific
range.
"""

import itertools

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
R_SERIES.update(x * 10 for x in list(R_SERIES))


def calculate_output_range(min_in, max_in, offset_voltage, rin, roffset, rf):
    c_min = (min_in * -rf / rin) + (offset_voltage * -rf / roffset)
    c_max = (max_in * -rf / rin) + (offset_voltage * -rf / roffset)
    return c_min, c_max


def calculate_component_values(min_in, max_in, min_out, max_out):
    offset_voltage = -10
    input_range = abs(max_in - min_in)
    output_range = abs(max_out - min_out)

    print(f"Input range: {input_range}")
    print(f"Output range: {output_range}")

    target_in_gain = -(output_range / input_range)
    target_offset_gain = -(min_out / offset_voltage)

    print(
        f"Required input gain: {target_in_gain:.3}, offset gain: {target_offset_gain:.3}"
    )

    # Go through *all* of the resistor combinations and calculate their
    # gain results. This isn't very efficient, but it's very fun.
    candidates = []
    for candidate in itertools.product(R_SERIES, repeat=3):
        rin, roffset, rf = candidate
        c_min, c_max = calculate_output_range(
            min_in, max_in, offset_voltage, rin, roffset, rf
        )

        # The output is inverted, so the comparisons here are a little
        # non-intuitive.
        if min_out - 0.2 < c_max < min_out and max_out < c_min < max_out + 0.2:
            candidates.append((rin, roffset, rf, c_min, c_max))

    # Sort by closeness
    candidates.sort(key=lambda x: abs(x[3] - max_out) + abs(x[4] - min_out))

    # Take only the top 5
    # candidates = candidates[: min(len(candidates), 5)]

    for v in candidates:
        print(f"Rin: {v[0]:.3f}, Roffset: {v[1]:.3f}, Rf: {v[2]:.3f}")
        print(f"    Output range: {v[3]:+.3f}v to {v[4]:+.3f}v")


calculate_component_values(0, 3.3, -5, +5)
