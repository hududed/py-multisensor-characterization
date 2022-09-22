import re

SICONVERSIONSTD = {
    'k': 1e3,
    'M': 1e6,
    'c': 1e-2,
    'm': 1e-3,
    'u': 1e-6,
    'n': 1e-9,
    'p': 1e-12,
    'f': 1e-15
}
SICONVERSIONPF = {
    'M': 1e18,
    'k': 1e15,
    'c': 1e10,
    'm': 1e9,
    'u': 1e6,
    'n': 1e3,
    'p': 1e0,
    'f': 1e-3,
}

FIELDNAMES=['Time (s)',
              'Time (min)',
              'Time (hr)',
            'Chamber Temperature SP (°C)', 
            'Chamber Temperature (°C)', 
            'Platform Temperature (°C)',
            'Chamber RH SP (% RH)',
            'Chamber RH (% RH)',
            'Chamber Temperature Output (%)',
            'Platform Output (%)',
            'Chamber Humidity Output (%)',
            'Capacitance (F)',
            'Capacitance (pF)']


def convert_to_pf(unit: str) -> float:
    return SICONVERSIONPF[unit]

def convert_raw_data(data: str) -> float:
    number = re.search('(\d*\.?\d+)',data).group(1)
    Farad_si_unit = re.search('(\wF)',data).group(1)[0]
    print(number, Farad_si_unit)
    return float(number) * convert_to_pf(Farad_si_unit)

def SI_conversion_standard(unit:str):
    """Convert SI Prefix to SI no prefix"""
    
    if 'M' in unit:
        return 10**6
    elif 'k' in unit:
        return 10**3
    elif 'c' in unit:
        return 10**-2
    elif 'm' in unit:
        return 10**-3
    elif 'u' in unit:
        return 10**-6
    elif 'n' in unit:
        return 10**-9
    elif 'p' in unit:
        return 10**-12
    elif 'f' in unit:
        return 10**-15

def SI_conversion_pF(unit:str):
    """Convert SI Prefix to SI no prefix"""
    # print(unit)
    if 'M' in unit:
        return 10**(6+12)
    elif 'k' in unit:
        return 10**(3+12)
    elif 'c' in unit:
        return 10**(-2+12)
    elif 'm' in unit:
        return 10**(-3+12)
    elif 'u' in unit:
        return 10**(-6+12)
    elif 'n' in unit:
        return 10**(-9+12)
    elif 'p' in unit:
        return 10**(-12+12)
    elif 'f' in unit:
        return 10**(-15+12)
    elif 'µ' in unit:
        return 10**(-6+12)
    