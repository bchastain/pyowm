#!/usr/bin/env python
# -*- coding: utf-8 -*-"""

# Temperature conversion constants
KELVIN_OFFSET = 273.15
FAHRENHEIT_OFFSET = 32.0
FAHRENHEIT_DEGREE_SCALE = 1.8

# Wind speed conversion constants
MILES_PER_HOUR_FOR_ONE_METER_PER_SEC = 2.23694
KM_PER_HOUR_FOR_ONE_METER_PER_SEC = 3.6
KNOTS_FOR_ONE_METER_PER_SEC = 1.94384

# Barometric conversion constants
HPA_FOR_ONE_INHG = 33.8639

# Visibility distance conversion constants
MILE_FOR_ONE_METER = 0.000621371
KMS_FOR_ONE_METER = .001

# Decimal precision
ROUNDED_TO = 2


def kelvin_dict_to(d, target_temperature_unit):
    """
    Converts all the values in a dict from Kelvin temperatures to the
    specified temperature format.

    :param d: the dictionary containing Kelvin temperature values
    :type d: dict
    :param target_temperature_unit: the target temperature unit, may be:
        'celsius' or 'fahrenheit'
    :type target_temperature_unit: str
    :returns: a dict with the same keys as the input dict and converted
        temperature values as values
    :raises: *ValueError* when unknown target temperature units are provided

    """
    if target_temperature_unit == 'kelvin':
        return d
    elif target_temperature_unit == 'celsius':
        return {key: kelvin_to_celsius(d[key]) for key in d}
    elif target_temperature_unit == 'fahrenheit':
        return {key: kelvin_to_fahrenheit(d[key]) for key in d}
    else:
        raise ValueError("Invalid value for target temperature conversion \
                         unit")


def kelvin_to_celsius(kelvintemp):
    """
    Converts a numeric temperature from Kelvin degrees to Celsius degrees

    :param kelvintemp: the Kelvin temperature
    :type kelvintemp: int/long/float
    :returns: the float Celsius temperature
    :raises: *TypeError* when bad argument types are provided

    """
    if kelvintemp < 0:
        raise ValueError(__name__ +
                         ": negative temperature values not allowed")
    celsiustemp = kelvintemp - KELVIN_OFFSET
    return float("{0:.2f}".format(celsiustemp))


def kelvin_to_fahrenheit(kelvintemp):
    """
    Converts a numeric temperature from Kelvin degrees to Fahrenheit degrees

    :param kelvintemp: the Kelvin temperature
    :type kelvintemp: int/long/float
    :returns: the float Fahrenheit temperature

    :raises: *TypeError* when bad argument types are provided
    """
    if kelvintemp < 0:
        raise ValueError(__name__ +
                         ": negative temperature values not allowed")
    fahrenheittemp = (kelvintemp - KELVIN_OFFSET) * \
        FAHRENHEIT_DEGREE_SCALE + FAHRENHEIT_OFFSET
    return float("{0:.2f}".format(fahrenheittemp))


def metric_wind_dict_to_imperial(d):
    """
    Converts all the wind values in a dict from meters/sec (metric measurement
    system) to miles/hour (imperial measurement system)
    .

    :param d: the dictionary containing metric values
    :type d: dict
    :returns: a dict with the same keys as the input dict and values converted
        to miles/hour

    """
    result = dict()
    for key, value in d.items():
        if key != 'deg':  # do not convert wind degree
            result[key] = value * MILES_PER_HOUR_FOR_ONE_METER_PER_SEC
        else:
            result[key] = value
    return result


def metric_wind_dict_to_km_h(d):
    """
    Converts all the wind values in a dict from meters/sec
    to km/hour.

    :param d: the dictionary containing metric values
    :type d: dict
    :returns: a dict with the same keys as the input dict and values converted
        to km/hour

    """
    result = dict()
    for key, value in d.items():
        if key != 'deg':  # do not convert wind degree
            result[key] = value * KM_PER_HOUR_FOR_ONE_METER_PER_SEC
        else:
            result[key] = value
    return result


def metric_wind_dict_to_knots(d):
    """
    Converts all the wind values in a dict from meters/sec
    to knots

    :param d: the dictionary containing metric values
    :type d: dict
    :returns: a dict with the same keys as the input dict and values converted
        to km/hour

    """
    result = dict()
    for key, value in d.items():
        if key != 'deg':  # do not convert wind degree
            result[key] = value * KNOTS_FOR_ONE_METER_PER_SEC
        else:
            result[key] = value
    return result


def metric_wind_dict_to_beaufort(d):
    """
    Converts all the wind values in a dict from meters/sec
    to the corresponding Beaufort scale level (which is not an exact number but rather
    represents a range of wind speeds - see: https://en.wikipedia.org/wiki/Beaufort_scale).
    Conversion table: https://www.windfinder.com/wind/windspeed.htm

    :param d: the dictionary containing metric values
    :type d: dict
    :returns: a dict with the same keys as the input dict and values converted
        to Beaufort level

    """
    result = dict()
    for key, value in d.items():
        if key != 'deg':  # do not convert wind degree
            if value <= 0.2:
                bf = 0
            elif 0.2 < value <= 1.5:
                bf = 1
            elif 1.5 < value <= 3.3:
                bf = 2
            elif 3.3 < value <= 5.4:
                bf = 3
            elif 5.4 < value <= 7.9:
                bf = 4
            elif 7.9 < value <= 10.7:
                bf = 5
            elif 10.7 < value <= 13.8:
                bf = 6
            elif 13.8 < value <= 17.1:
                bf = 7
            elif 17.1 < value <= 20.7:
                bf = 8
            elif 20.7 < value <= 24.4:
                bf = 9
            elif 24.4 < value <= 28.4:
                bf = 10
            elif 28.4 < value <= 32.6:
                bf = 11
            else:
                bf = 12
            result[key] = bf
        else:
            result[key] = value
    return result


def metric_pressure_dict_to_inhg(d):
    """
    Converts all barometric pressure values in a dict to "inches of mercury."

    :param d: the dictionary containing metric values
    :type d: dict
    :returns: a dict with the same keys as the input dict and values converted
        to "Hg or inHg (inches of mercury)

    Note what OWM says about pressure: "Atmospheric pressure [is given in hPa]
    (on the sea level, if there is no sea_level or grnd_level data)"
    """
    result = dict()
    for key, value in d.items():
        if value is None:
            continue
        result[key] = round((value / HPA_FOR_ONE_INHG), ROUNDED_TO)
    return result


def visibility_dict_to(d, target_visibility_unit='miles'):
    """
    Converts all meter values in a dict to either miles or kms.

    :param d: the dictionary containing metric values
    :param target_visibility_unit: either miles or kms, ValueError if neither
    :type d: dict
    :type target_visibility_unit: str
    :returns: a dict with converted values for visibility distance
    """
    result = dict()

    if target_visibility_unit == 'miles': const = MILE_FOR_ONE_METER
    elif target_visibility_unit == 'kms': const = KMS_FOR_ONE_METER
    else:
        e = 'Invalid value for target visibility unit'
        raise ValueError(e)

    for key, value in d.items():
        if value is None:
            continue
        result[key] = round(value * const, ROUNDED_TO)
    return result

