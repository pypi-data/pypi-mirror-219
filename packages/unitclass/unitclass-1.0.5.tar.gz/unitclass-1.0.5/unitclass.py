"""
unitclass: Physical unit class suitable for calculations in the sciences.

    Copyright (C) 2023  Blake T. Garretson

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
import math, csv, numbers, re

g = 9.80665  # standard value of accel of gravity


class BadOp(Exception):
    pass


class InconsistentUnitsError(Exception):
    pass


class UnavailableUnit(Exception):
    pass


# Data structure to store unit info
# Keys are unit names, vacd ..lue is a dict in the form:
#     {'factor': <factor>, 'qty': <quantity>, 'aliases': []}
_units = {}

# Keys are aliases, values are primary unit name
_aliases = {}

# https://www.nist.gov/pml/owm/metric-si/si-units
# Quantity construction is a list of two lists containing the units in the
# numerator and the denominator. Multiple units in either list are multiplied.
# The construction does not need to use the MOST simplified units.
# e.g. Pa is defined as force over length squared, but then this could be
# simplified a second time to get base units.
#
# The worst bit of nonsense below is making force a fundamental base unit and
# defining mass in terms of force (m=F/a). This is convenient in order to
# seemlessly convert between newtons, pounds, grams, etc. as "normal" people expect.
_quantities = {
    # Fundamental quantiies
    #   Used to define any other unit that will be converted to/from
    #   or will interact with other units.
    'time': [['time'], []],
    'length': [['length'], []],
    'current': [['current'], []],
    'amount': [['amount'], []],
    'luminous_intensity': [['luminous_intensity'], []],
    'force': [['force'], []],
    'angle': [['angle'], []],
    'unitless': [['unitless'], []],
    # Other special purpose
    'concentration': [['unitless'], []],
    'data': [['data'], []],
    'currency': [['currency'], []],
    # SI
    'mass': [['force', 'time', 'time'], ['length']],  # force/acceleration
    'energy': [['force', 'length'], []],
    'charge': [['current', 'time'], []],
    'catalytic_activity': [['amount'], ['time']],
    'illuminance': [['luminous_intensity', 'angle', 'angle'], ['length'] * 2],
    'power': [['force', 'length'], ['time']],
    'pressure': [['force'], ['length'] * 2],
    'voltage': [['force', 'length'], ['current', 'time']],
    'magnetic_flux': [['force', 'length', 'time'], ['current', 'time']],
    'mag_flux_density': [['force', 'length', 'time'],
                         ['current', 'time', 'length', 'length']],
    'luminous_flux': [['luminous_intensity', 'angle', 'angle'], []],
    'frequency': [[], ['time']],
    'radionuclide_activity': [[], ['time']],
    'absorbed_dose': [['force', 'length', 'length'], ['force', 'time',
                                                      'time']],
    'resistance': [['force', 'length'], ['current', 'current', 'time']],
    'inductance': [['force', 'length', 'time'], ['current', 'current',
                                                 'time']],
    'capacitance': [['current', 'time', 'current', 'time'],
                    ['force', 'length']],
    'solid_angle': [['angle'] * 2, []],
    'dose_equivalent': [['force', 'length', 'length'],
                        ['force', 'time', 'time']],
    'conductance': [['current', 'current', 'time'], ['force', 'length']],
    # other compound units
    'area': [['length'] * 2, []],
    'volume': [['length'] * 3, []],
    'density': [['force'], ['length'] * 3],
    'dyn_viscosity': [['force', 'time'], ['length'] * 2],
    'kin_viscosity': [['energy', 'time'], ['force']],
    'torque': [['force', 'length'], []],
    'speed': [['length'], ['time']],
    'angular speed': [['angle'], ['time']],
    'acceleration': [['length'], ['time', 'time']],
    'fluid_flow': [['length'] * 3, ['time']],
}

# The first unit added in any quantity becomes the default for that unit
_defaults = {}

# key: unique signature of every quantity
# value: quantity name
# This is useful to parse an unknown combination of units and determine if
# it is a known quantity, e.g. N/mm2 is a MPa
_signatures = {}


def _gen_signature(constr):
    """Returns stable identifier/signature for any construction"""
    num, denom = constr
    num = ".".join(sorted(num))
    denom = ".".join(sorted(denom))
    sig = f'{num}|{denom}'
    return sig


def _make_signatures():
    for qty, constr in _quantities.items():
        _signatures[_gen_signature(constr)] = qty


_make_signatures()

# Format: (quantity, unit, aliases, factor, factor unit)
#   factor: conversion factor if a factor unit is given
#     i.e. 1 of the given unit is equal to <factor> <factor units>
#   factor unit: if not given, the factor is ignored. For clarity, the
#     factor is set to 1 below to make it obvious that no scaling is done
# IMPORTANT: Due to pragmatic decisions, all units should be defined in terms
#            of force, not mass. There should not be a mass quantity in
#            the list below!
_unit_list = [
    # SI base units
    ('time', 's', 'second seconds sec secs', 1, ''),
    ('length', 'm', 'meter meters metre metres', 1, ''),
    ('current', 'A', 'ampere amperes amp amps', 1, ''),
    ('temperature', '°K', 'K kelvin Kelvin degK', 1, ''),
    ('amount', 'mol', 'mols mole moles', 1, ''),
    ('luminous_intensity', 'cd', 'candela candelas', 1, ''),
    ('energy', 'J', 'joule joules ', 1, ''),
    ('force', 'N', 'newton newtons', 1, ''),
    ('force', 'g', 'gram grams', g / 1000, 'N'),  # mass kludge
    ('charge', 'C', 'coulomb coulombs', 1, ''),
    ('catalytic_activity', 'kat', 'katal katals', 1, ''),
    ('illuminance', 'lx', 'lux Lux', 1, ''),
    ('power', 'W', 'watt watts', 1, ''),
    ('pressure', 'Pa', 'pascal pascals', 1, ''),
    ('voltage', 'V', 'volt volts', 1, ''),
    ('magnetic_flux', 'Wb', 'weber webers', 1, ''),
    ('mag_flux_density', 'T', 'tesla teslas', 1, ''),
    ('luminous_flux', 'lm', 'lumen lumens', 1, ''),
    ('frequency', 'Hz', 'hertz', 1, ''),
    ('radionuclide_activity', 'Bq', 'becquerel becquerels', 1, ''),
    ('absorbed_dose', 'Gy', 'gray grays', 1, ''),
    ('resistance', 'Ω', 'ohm ohms', 1, ''),
    ('inductance', 'H', 'henry henrys', 1, ''),
    ('capacitance', 'F', 'farad farads', 1, ''),
    ('solid_angle', 'sr', 'steradian', 1, ''),
    ('dose_equivalent', 'Sv', 'sievert sieverts', 1, ''),
    ('conductance', 'S', 'siemens', 1, ''),
    ('angle', 'rad', 'rads radians radian', 1, ''),
    # Other units below
    ('unitless', '', 'unitless _', 1, ''),
    ('time', 'min', 'minute minutes', 60, 's'),
    ('time', 'hr', 'hrs hour hours', 60, 'min'),
    ('time', 'day', 'days', 24, 'hr'),
    ('time', 'week', 'weeks', 7, 'day'),
    ('time', 'fortnight', 'fortnights', 14, 'day'),
    ('time', 'year', 'yr yrs years', 365, 'day'),
    ('length', 'in', 'inch inches "', 25.4, 'mm'),
    ('length', 'ft', "feet ' foot", 12, 'in'),
    ('length', 'yd', 'yard yards', 36, 'in'),
    ('length', 'mi', 'mile miles statutemile statutemiles smi', 5280, 'ft'),
    ('length', 'nmi', 'nauticalmile nauticalmiles', 1852, 'm'),
    ('length', 'league_land', 'leagues_land', 3, 'mi'),
    ('length', 'league_sea', 'leagues_sea nauticalleague nauticalleagues', 3, 'nmi'),
    ('length', 'gmi', 'geographicalmile geographicalmiles', 1855.3247, 'm'),
    ('length', 'mil', '', 0.001, 'in'),
    ('length', 'thou', '', 0.001, 'in'),
    ('length', 'micron', 'microns', 1, 'um'),
    ('length', 'cl', 'caliber', 1, 'in'),
    ('length', 'pt', 'point points pts', 1 / 72, 'in'),
    ('length', 'pica', 'picas', 12, 'pt'),
    ('length', 'angstrom', 'ang', 0.1, 'nm'),
    ('length', 'furlong', 'furlongs', 660, 'ft'),
    ('length', 'intl_cable', 'intl_cables', 185.2, 'm'),
    ('length', 'imp_cable', 'imp_cables', 185.32, 'm'),
    ('length', 'chain', 'chains', 66, 'ft'),
    ('length', 'link', 'links', 100, 'chain'),
    ('length', 'us_cable', 'us_cables', 720, 'ft'),
    ('length', 'fathom', 'fathoms', 6, 'ft'),
    ('length', 'hand', 'hands', 4, 'in'),
    ('length', 'bohrrad', 'bohrradius', 5.29177210903e-11, 'm'),
    ('length', 'smoot', 'smoots', 67, 'in'),
    ('length', 'au', 'astrounit', 149597870.691, 'km'),
    ('acceleration', 'G', 'gravity', g, 'm/s2'),
    ('volume', 'L', 'l liter liters litre litres', 1, 'dm3'),
    # alternate spelling of mL is manually added here for convenience
    ('volume', 'ml', 'milliliter milliliters millilitre millilitres', 1, 'cm3'
     ),
    ('volume', 'cc', 'cubic_cm', 1, 'cm3'),
    ('volume', 'drygal', 'drygallon drygallons us_drygallon drygals', 268.8025,
     'in3'),  # US
    ('volume', 'bsh', 'usbsh bushel us_bushel bushels us_bushels', 2150.42,
     'in3'),  # US
    ('volume', 'gal', 'gallon gallons us_gallon gals', 231, 'in3'),  # US
    ('volume', 'peck', 'pecks uspecks', 0.25, 'bsh'),
    ('volume', 'floz', 'flounce fluidounce us_floz', 1 / 128, 'gal'),  # US
    ('volume', 'quart', 'quarts qt qts us_qt', 32, 'floz'),  # US
    # pint: not using pt or pts because of conflict with typography unit
    ('volume', 'pint', 'pints', 16, 'floz'),  # US,
    ('volume', 'cup', 'cups', 8, 'floz'),  # US
    ('volume', 'gill', 'gills', 4, 'floz'),  # US
    ('volume', 'tbsp', 'Tbsp TBSP tablespoon tablespoons', 0.5, 'floz'),  # US
    ('volume', 'tsp', 'Tsp teaspoon teaspoons', 1 / 6, 'floz'),
    ('volume', 'fldram', 'fldrams us_fldram', 1 / 8, 'floz'),  # US
    ('volume', 'imp_gal', 'imp_gallon imp_gallons imp_gals', 4.54609, 'L'),
    ('volume', 'imp_floz', '', 1 / 160, 'imp_gal'),
    ('volume', 'imp_qt', 'imp_quart', 40, 'imp_floz'),
    ('volume', 'imp_pt', 'imp_pint', 20, 'imp_floz'),
    ('volume', 'imp_cup', '', 10, 'imp_floz'),
    ('volume', 'imp_gill', '', 5, 'imp_floz'),
    ('volume', 'imp_fldram', '', 1 / 8, 'imp_floz'),
    ('area', 'acre', 'acres', 43560, 'ft2'),
    ('area', 'sqft', 'squarefeet squarefoot', 1, 'ft2'),
    ('area', 'sqin', 'squareinches', 1, 'in2'),
    ('force', 'dyn', 'dyne dynes', 1e-5, 'N'),
    ('force', 'lb', 'lbf lb_f lbs pound pounds', 4.4482216,
     'N'),  # pound force
    ('force', 'kip', 'kips kipf klbf', 1000, 'lb'),
    ('force', 'oz', 'ounce ounces ozf ounceforce', 1 / 16, 'lb'),
    ('force', 'troz', 'troyounce troyounces', 31.1034768, 'g'),
    ('force', 'trlb', 'troypound troypounds', 12, 'troz'),
    ('force', 'grain', 'grains', 1 / 480, 'troz'),
    ('force', 'ton', 'tons us_tons shortton', 2000, 'lb'),
    ('force', 'imp_ton', 'imp_tons longton', 2240, 'lb'),
    ('force', 'mton', 'metricton metric_ton', 1000, 'kg'),
    ('force', 'ct', 'carat carats', 200, 'mg'),
    ('force', 'stone', 'stones', 14, 'lb'),
    ('force', 'slug', 'slugs', 32.174, 'lb'),
    ('force', 'dwt', 'pennyweight', 24, 'grains'),
    ('pressure', 'psi', '', 1, 'lb/in2'),
    ('pressure', 'psf', '', 1 / 144, 'lb/in2'),
    ('pressure', 'ksi', '', 1000, 'lb/in2'),
    ('pressure', 'inHg', 'inhg', 3386.388640341, 'Pa'),
    ('pressure', 'inH2O', 'inh2o', 249.082, 'Pa'),
    ('pressure', 'bar', 'bars', 100000, 'Pa'),
    ('pressure', 'mBar', 'mbar mbars millibar', 100, 'Pa'),
    ('pressure', 'atm', 'atmosphere', 101325, 'Pa'),
    ('density', 'pcf', 'PCF', 1, 'lb/ft3'),
    ('power', 'hp', 'horsepower', 550, 'ft*lb/s'),
    ('dyn_viscosity', 'cP', 'centipoise', 1, 'mPa*s'),
    ('dyn_viscosity', 'P', 'poise', 100, 'cP'),
    ('kin_viscosity', 'St', 'stokes stoke', 0.0001, 'm2/s'),
    ('kin_viscosity', 'cSt', 'centistokes centistoke', 1e-6, 'm2/s'),
    ('energy', 'BTU', 'thermochemicalBTU', 4.184 * 453.59237 * 5 / 9, 'J'),
    ('energy', 'cal', 'calorie', 4.184, 'J'),
    ('energy', 'kcal', 'kilocalorie', 1000, 'cal'),
    ('temperature', '°C', 'CC celsius centigrade degC', 1, ''),
    ('temperature', '°F', 'FF fahrenheit degF', 1, ''),
    ('angle', '°', 'deg degree degrees', math.pi / 180, 'rad'),
    ('angle', 'rev', 'revolution revolutions', 360, 'deg'),
    ('angle', 'grad', 'grads gradian gradians grade gon', math.pi / 200,
     'rad'),
    ('angle', 'turn', 'turns', 1, 'rev'),
    ('angle', 'arcmin', 'arcminute minarc minutearc ′', 1 / 360, 'turn'),
    ('angle', 'arcsec', 'arcsecond secarc secondarc ″', 1 / 60, 'arcmin'),
    ('angle', 'mas', 'milliarcsecond marcsec', 1 / 3600000, 'deg'),
    ('angle', 'μas', 'uas microarcsecond uarcsec μarcsec', 0.001, 'mas'),
    ('data', 'B', 'byte bytes', 1, ''),
    ('data', 'KB', 'kilobyte kilobytes', 1024, 'B'),
    ('data', 'MB', 'megabyte megabytes', 1024, 'KB'),
    ('data', 'GB', 'gigabyte gigabytes', 1024, 'MB'),
    ('data', 'TB', 'terabyte terabytes', 1024, 'GB'),
    ('data', 'PB', 'petabyte petabytes', 1024, 'TB'),
    ('data', 'EB', 'exabyte exabytes', 1024, 'PB'),
    ('currency', 'USD', 'dollars dollar usdollar', 1, ''),
    ('currency', 'pennies', 'penny', 0.01, 'USD'),
    ('currency', 'nickels', 'nickel', 0.05, 'USD'),
    ('currency', 'dimes', 'dime', 0.10, 'USD'),
    ('currency', 'quarters', 'quarter', 0.25, 'USD'),
    ('speed', 'mph', 'mileperhour', 1, 'mi/hr'),
    ('speed', 'kph', 'kmperhour', 1, 'km/hr'),
    ('speed', 'c', 'lightspeed', 299792458, 'm/s'),
    ('speed', 'mach', 'Ma mach_sealevel_15C', 340.3, 'm/s'),
    ('angular speed', 'rpm', 'RPM RPMS rpms', 1, 'rev/min'),
    ('concentration', '%', 'pct percent percentage', 0.01, 'unitless'),
    ('concentration', 'ppm', 'partspermillion', 1e-4, 'pct'),
    ('concentration', 'ppb', 'partsperbillion', 1e-7, 'pct'),
    ('fluid_flow', 'gpm', 'galpermin', 1, 'gal/min'),
    ('fluid_flow', 'gph', 'galperhr', 1, 'gal/hr'),
    ('fluid_flow', 'cfm', 'cubicftperminute', 1, 'ft3/min'),
    ('fluid_flow', 'cfs', 'cubicftpersec', 1, 'ft3/sec'),
    ('fluid_flow', 'lpm', 'literspermin', 1, 'L/min'),
    ('torque', 'in*lb', 'inchpound inlb', 1, 'in*lb'),
    ('torque', 'ft*lb', 'footpound ftlb', 1, 'ft*lb'),
]

# SI prefix info
_prefix_units = 'm g s A L J N Pa W Ω V C F H Hz'.split()
_prefix_mult = (1e18, 1e15, 1e12, 1e9, 1e6, 1e3, 1e-1, 1e-2, 1e-3, 1e-6, 1e-9,
                1e-12, 1e-15)
_prefixes = list("EPTGMkdcmμnpf")


def _expand_units(unitlist):
    """Take a list of units and return a list with exponents
    expanded to individual units.  e.g. ["N","m2"] -> ["N", "m", "m"]
    """
    newlist = []
    for u in unitlist:
        if u and u[-1].isdigit():
            newlist.extend([u[:-1]] * int(u[-1]))
        else:
            newlist.append(u)
    return newlist

re_oper = re.compile("(^\(.*?\))|(^(.*?)([*|\/])(.*?)(?=(\(.*?\))|[*\/]|$))"
                     )  # parens group, or next operator
def _parse_unit(text, numerator=None, denominator=None, divflip=False, expand=True):
    """Parse unit str and break down to indvidual components, respecting PEMDAS order 
    of operations and allowing for parentheses.
    e.g.:

    >>> _parse_unit('N*m/(s*in)')
    (['N', 'm'], ['s', 'in'])

    expand: will call _expand_units()
    """    
    if not numerator:
        numerator = []
    if not denominator:
        denominator = []
    text = text.strip()
    if divflip:
        numerator, denominator = denominator, numerator

    while match := re_oper.search(text):
        parens = match.group(1)
        term1 = match.group(3)
        op = match.group(4)
        term2 = match.group(5)
        term2_parens = match.group(6)

        if op in ('*','×','·','•','⋅'):
            end = match.end()
            if term1: numerator.append(term1)
            if term2: numerator.append(term2)
            elif term2_parens:
                numerator, denominator = _parse_unit(
                    term2_parens[1:-1], numerator, denominator, expand=False)
                end += len(term2_parens)
            text = text[end:]
        elif op in ('/','÷'):
            end = match.end()
            if term1: numerator.append(term1)
            if term2: denominator.append(term2)
            elif term2_parens:  # flip num/denom since it's being divided
                numerator, denominator = _parse_unit(term2_parens[1:-1],
                                                          numerator,
                                                          denominator,
                                                          divflip=True, expand=False)
                end += len(term2_parens)
            text = text[end:]
        elif parens:
            text = text[match.end():]
            numerator, denominator = _parse_unit(parens[1:][:-1],
                                                      numerator, denominator, expand=False)
    if text:  # just a single term left
        numerator.append(text)
        text = ''
    if divflip:
        numerator, denominator = denominator, numerator
    if expand:
        numerator = _expand_units(numerator)
        denominator = _expand_units(denominator)
    return numerator, denominator

def _get_unit(unit):
    """Returns unit dict, handling aliases too"""
    if unit in _units:
        return _units[unit]
    elif unit in _aliases:
        return _units[_aliases[unit]]
    else:
        raise UnavailableUnit(f"Unit {unit} is not defined.")


def _get_unit_name(unit_str, ignore_error=False):
    """Returns unit name, handling aliases too"""
    num, denom = _parse_unit(unit_str, expand=True)
    try:
        num_values = [u if u in _units else _aliases[u] for u in num]
        denom_values = [u if u in _units else _aliases[u] for u in denom]
    except KeyError:
        if not ignore_error:
            raise UnavailableUnit(f"Unit {unit_str} is not defined.")
        else:
            return ""
    return _make_name(num_values, denom_values)


def _get_factors(unit_str):
    """Take a unit name and return combination of all factors.
    This is useful for compound units like m/s2"""
    num, denom = _parse_unit(unit_str, expand=True)
    num_values = [_get_unit(u)['factor'] for u in num]
    denom_values = [_get_unit(u)['factor'] for u in denom]
    value = math.prod(num_values) / math.prod(denom_values)
    return value


def add_unit(qty, unit, alias_list, factor, factor_unit):
    """Create unit definition.
    Takes arguments in this format:
    add_unit(<quantity>, <name>, <aliases>, <factor>, <factor unit>)
    e.g. add_unit('length', "in", 'inch inches', 25.4, 'mm')

    >>> add_unit("length", "blake", "blakes bunits", 6, 'ft')

    factor: this is a conversion factor to specify the equivalent
            quantity in a different unit. In the above example
            1 inch is equivalent to 25.4 mm.
    """
    if factor_unit:
        factor *= _get_factors(factor_unit)
    _units[unit] = {
        'factor': factor,
        'qty': qty,
        'aliases': alias_list.split()
    }
    if qty not in _defaults:
        _defaults[qty] = unit
    # add SI prefixes for certain units
    if unit in _prefix_units:
        for mult, prefix in zip(_prefix_mult, _prefixes):
            _units[prefix + unit] = {
                'factor': mult * factor,
                'qty': qty,
                'aliases': []
            }
            if unit == 'Ω':
                _aliases[prefix + 'ohm'] = prefix + unit
                _units[prefix + unit]['aliases'].append(prefix + 'ohm')
            if prefix == 'μ':
                _aliases['u' + unit] = prefix + unit
                _units[prefix + unit]['aliases'].append('u' + unit)
                if unit == 'Ω':
                    _aliases['uohm'] = prefix + unit
                    _units[prefix + unit]['aliases'].append('uohm')
    _aliases.update({alias: unit for alias in alias_list.split()})


for _unitinfo in _unit_list:
    add_unit(*_unitinfo)


def _combine_units(unitlist):
    """Take a list of units and combine them
    e.g. ["N", "m", "m"] -> ["N","m2"]
    """
    newlist = []
    processed = []
    for u in unitlist:
        if u not in processed:
            i = unitlist.count(u)
            if i > 1:
                newlist.append(u + str(i))
            else:
                newlist.append(u)
            processed.append(u)
    return newlist


def _simplify_unit(num, denom):
    """Takes lists of individual units, cancels out dups from num and denom"""
    num = _expand_units(num)
    denom = _expand_units(denom)

    # remove unitless items
    num = [i for i in num if i]
    denom = [i for i in denom if i]

    for u in tuple(num):
        if (u in num) and (u in denom):
            num.remove(u)
            denom.remove(u)
    return num, denom


def _make_name(num, denom, combine=True):
    """Takes list of individual units and combines them

    You would want to set 'combine' to False if you want an expanded unit, useful for
    unit types: force/(length*length)"""
    new_num, new_denom = _simplify_unit(num, denom)
    if combine:
        new_num, new_denom = _combine_units(new_num), _combine_units(new_denom)

    num_str = "*".join(new_num)
    denom_str = "*".join(new_denom)
    if num_str == '' and denom_str == '':
        new_unit = ""
    elif denom_str == '':
        new_unit = num_str
    else:
        if len(new_denom) > 1:
            new_unit = f"{num_str}/({denom_str})" # parens
        else:
            new_unit = f"{num_str}/{denom_str}"
    return new_unit


def _get_construction(fractional_unit, combine=False, listform=False):
    """Reduce the units down to the fundamental quantities (length, force, time, etc.)
    This should be used with the _parse_unit() function to split
    the unit into fractional parts and pass the pair into this function.
    """
    num, denom = fractional_unit
    num_constr = [_get_unit(i)['qty'] for i in num]
    denom_constr = [_get_unit(i)['qty'] for i in denom]
    for u in num_constr:
        if u in _quantities:
            n, d = _quantities[u]
            num_constr.remove(u)
            num_constr.extend(n)
            denom_constr.extend(d)
    for u in denom_constr:
        if u in _quantities:
            n, d = _quantities[u]
            denom_constr.remove(u)
            num_constr.extend(d)
            denom_constr.extend(n)
    num_constr, denom_constr = _simplify_unit(num_constr, denom_constr)
    num_constr.sort()
    denom_constr.sort()
    if num_constr in ([], [''], ['unitless'], ['1']):
        num_constr = ['']
    if listform:
        return [num_constr, denom_constr]
    else:
        construction = _make_name(num_constr, denom_constr, combine=combine)
        return construction


def _check_consistent_units(from_unit, to_unit, silent=False):
    """Return True if units are fundamentally the same OR if one is unitless
    
    arguments are strings, not Unit class"""
    if not all([from_unit, to_unit]):
        return True # one of the units is unitless, so it's essentially a scalar
    to_constr = _get_construction(_parse_unit(to_unit))
    from_constr = _get_construction(_parse_unit(from_unit))
    if to_constr != from_constr:
        errstr = f"Error: Units are not consistent.\n" +\
            f"       {from_unit} is {from_constr}\n" +\
            f"       {to_unit} is {to_constr}"
        if not silent:
            raise InconsistentUnitsError(errstr)
        else:
            return False
    else:
        return True

def _convert_C2F(value):
    return value * 9.0 / 5.0 + 32


def _convert_F2C(value):
    return (value - 32) * 5.0 / 9.0


def _convert_C2K(value):
    return value + 273.15


def _convert_K2C(value):
    return value - 273.15


def convert(value, from_unit, to_unit):
    """Convert value from original unit to new unit
    Example: convert(40, 'pcf', 'kg/m3') returns 640.7
    Special cases include temperature
    """
    # TODO: this doesn't handle compound units with temperature, like J/degC
    
    if (not to_unit) and (from_unit != '%'): # unitless, treat as same unit
        return value
    elif (not from_unit) and (to_unit != '%'): # unitless, treat as same unit
        return value

    both = _get_unit_name(from_unit, ignore_error=True) + \
        _get_unit_name(to_unit, ignore_error=True)
    if both == '°C°F':
        newvalue = _convert_C2F(value)
    elif both == '°F°C':
        newvalue = _convert_F2C(value)
    elif both == '°K°C':
        newvalue = _convert_K2C(value)
    elif both == '°C°K':
        newvalue = _convert_C2K(value)
    elif both == '°F°K':
        newvalue = _convert_C2K(_convert_F2C(value))
    elif both == '°K°F':
        newvalue = _convert_C2F(_convert_K2C(value))
    else:
        _check_consistent_units(from_unit, to_unit)
        newvalue = value * _get_factors(from_unit) / _get_factors(to_unit)
    return newvalue


def list_quantities():
    """List available quantities"""
    [print(x) for x in sorted(list(_quantities.keys()))]


def list_units(qty=[], search=''):
    """List available  units
    By default, all units are printed.

    qty: sequence of quantity names, results
         are limited to this list. Empty sequence
         includes all quantities.
    search: limit results to units and aliases containing
            the search term.
    """
    if not qty:
        qty = _quantities.keys()
    for name, unit in _units.items():
        if unit['qty'] in qty:
            if ((not search) or (search in name) or any(
                (search in x) for x in unit['aliases'])):
                print(
                    f"{name:6}->unit of {unit['qty']:10} aliases: {unit['aliases'] if unit['aliases'] else []}"
                )


# The below lists are the approved functions that are allowed in
# math equations during unit imports.


def _build_import_funcs():
    """
    Create a dictionary of functions that are allowed to be used in equations
    in imported CSV files. Most math fuctions from the math module and some 
    from __builtins__ are allowed, and everything else is forbidden.

    Used in conjunction with _import_units() function which actually reads the 
    CSV and does the eval().
    """
    available_funcs = {}
    mathops = [
        'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'cbrt',
        'ceil', 'comb', 'copysign', 'cos', 'cosh', 'degrees', 'dist', 'e',
        'erf', 'erfc', 'exp', 'exp2', 'expm1', 'fabs', 'factorial', 'floor',
        'fmod', 'frexp', 'fsum', 'gamma', 'gcd', 'hypot', 'inf', 'lcm',
        'ldexp', 'lgamma', 'log', 'log10', 'log1p', 'log2', 'modf', 'perm',
        'pi', 'pow', 'prod', 'radians', 'remainder', 'sin', 'sinh', 'sqrt',
        'tan', 'tanh', 'tau', 'trunc'
    ]

    builtinops = [
        'abs', 'complex', 'divmod', 'float', 'int', 'max', 'min', 'pow',
        'range', 'reversed', 'round', 'sorted', 'sum'
    ]

    for key in builtinops:
        available_funcs[key] = locals().get(key)
    for key in mathops:
        available_funcs[key] = math.__dict__.get(key)
    return available_funcs


_available_funcs = _build_import_funcs()


def _import_units(filename):
    """Loads custom units from a CSV file.
    Example line:
    length, myin, myinch my_inch, 1/8.0, in

    >>> _ = open('doctest_testfile.csv', 'w').write('length, myin, myinch my_inch, 1/8.0, in\\n')
    >>> _import_units('doctest_testfile.csv')
    [['length', 'myin', 'myinch my_inch', 0.125, 'in']]
    >>> import os
    >>> os.remove('doctest_testfile.csv')

    """
    unitdata = []
    with open(filename) as csvfile:
        datareader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for line in datareader:
            line = [x.strip() for x in line]
            # parse factor item in case it's an equation. The eval() is limited to hand selected functions.
            line[3] = eval(line[3], {'__builtins__': {}}, _available_funcs)
            unitdata.append(line)
    return unitdata


def import_units(filename):
    """Loads custom units from a CSV file.
    Example line:
    length, myin, myinch my_inch, 1/8.0, in
    """
    for line in _import_units(filename):
        add_unit(*line)


#######################################################################
#######################################################################
# Unit Class
#######################################################################
#######################################################################
class Unit:
    """
    Unit class

    Usage:
    Create Unit w/
        String: 
            Unit("1 N*m")
            Unit("3.4 mi/hr")
        Int/Float & Str: 
            Unit(1, "N*m")
            Unit(3.4, "mi/hr")
        Create unit and convert:
            Unit(3.4, "mi/hr", "km/hr")
            Unit("3.4 mi/hr km/hr")
        Create & convert w/ method: 
            Unit(3.4, "mi/hr").to("km/hr")
    """

    def __init__(self, *argv):
        self.to_specials = str.maketrans("0123456789*", "⁰¹²³⁴⁵⁶⁷⁸⁹·")
        self.from_specials = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⋅·×", "0123456789***")

        value = None
        unit = ''
        to_unit = ''

        if not argv:
            raise Exception("No arguments given for Unit.")
        elif len(argv) == 1:  # 1, '1', '1 mm', '1 mm in'
            arg =  argv[0]
            if isinstance(arg, Unit): # pass through, if you try to instance a Unit
                unit = arg.unit
                value = arg.value
            elif isinstance(arg, (float,int)): # -> 1
                value = arg
            elif isinstance(arg, str): # -> '1' or 'mm' or '1 mm' or '1 mm in'
                if arg.startswith('$'):
                    items = arg[1:].split()
                    items = [items[0], 'USD']+items[1:]
                else:
                    items = arg.split()
                if len(items) == 1:
                    item = items[0]
                    if all([(i in '0123456789-+.') for i in item]): # is number
                        value = item
                    else: # is a unit with no value given
                        value = 1
                        unit = item
                elif len(items) == 2: # -> 1,'mm'
                    value, unit = items
                elif len(items) == 3: # -> 1, 'mm', 'in' (convert on the fly)
                    value, unit, to_unit = items
                else:
                    raise Exception(f"Too many arguments given: {items}")
        elif len(argv) == 2:
            value, unit = argv
        else:
            value, unit, to_unit, *_ = argv
        self.unit = self._validate_unit(unit)
        self.value = self._input2number(value)
        if to_unit:
            self.to(self._validate_unit(to_unit))

    def _input2number(self, value):
        """
        Convert value to float or int.
        """
        if isinstance(value, str):
            value = float(value) if '.' in value else int(value)
        return value

    def _validate_unit(self, unit_str):
        """Validate unit
        Operations:
        - Verifies unit is in database
        - Checks for aliases (throws exception if it isn't available)
        - Replace superscripts and special characters in case they were passed in
        - if one of the Unit objects was unitless, it removes the empty string from the name
        - Returns primary name (after replacements)
        """
        return _get_unit_name(unit_str.translate(self.from_specials).replace('^','').replace('**',''))

    def _tocopy(self, newunit):
        """Converts and returns a new Unit() copy"""
        newunit = self._validate_unit(newunit)
        value = convert(self.value, self.unit, newunit)
        return Unit(value, newunit)
    
    def to(self, newunit):
        """Converts in-place, and returns self for viewing the result in Jupyter immediately"""
        newunit = self._validate_unit(newunit)
        self.value = convert(self.value, self.unit, newunit)
        self.unit = newunit
        return self

    def _get_construction(self):
        return _get_construction(_parse_unit(self.unit))

    def _new_unit(self, other, op):
        """Get new unit for some math operation.
        Units can be multiplied, divided, powered, abs with
            different units, the new unit will be returned. (op = div, rdiv, mul, pow)
        If other is unitless, it's assumed to be the same as the number with a unit, unless op="pow".
        """
        if (not isinstance(other,
                           Unit)) and (op != "pow"):  # unitless and not pow
            return self.unit
        if op == "pow":
            num, denom = _parse_unit(self.unit)
            num = num * int(other)
            denom = denom * int(other)
        else:
            num1, denom1 = _parse_unit(self.unit)
            num2, denom2 = _parse_unit(other.unit)
            if op == "mul":
                num = num1 + num2
                denom = denom1 + denom2
            elif op == "div":
                num = num1 + denom2
                denom = denom1 + num2
            elif op == "rdiv":
                num = num2 + denom1
                denom = denom2 + num1
            else:
                raise BadOp(
                    "Bad op passed. Must be: addsub, pow, mul, div, rdiv")

        return _make_name(num, denom)

    def expand(self,
               length=_defaults['length'],
               force=_defaults['force'],
               time=_defaults['time'],
               temperature=_defaults['temperature'],
               current=_defaults['current'],
               angle=_defaults['angle'],
               unitless=_defaults['unitless'],
               amount=_defaults['amount'],
               luminous_intensity=_defaults['luminous_intensity']):
        """Expand to fundamental units in terms of given units.
        Default values are used for units, but they can be overridden with the method args.

        This method is not strictly necessary since you can always use to() method to coerce the
        units to anything you want (e.g. "mm*in" to "in2"), but if you have a
        convoluted math operation, it might not be obvious what the final units are
        if they are in different systems.

        Changes object in-place, but also returns it for interactive usability

        Examples:

        >>> a = Unit('1 W')/Unit('1 A')
        >>> a
        1 W/A
        >>> a.expand()
        1 N·m/(A·s)
        >>> a.expand(time='ms', force='lb')
        0.000224809 lb·m/(A·ms)
                        
        """
        constr = _get_construction(_parse_unit(self.unit), combine=True)

        constr = constr.replace("length", length).replace(  # type: ignore
            "force", force).replace("time", time).replace(
                "temperature",
                temperature).replace("current", current).replace(
                    "angle", angle).replace("unitless", unitless).replace(
                        "luminous_intensity",
                        luminous_intensity).replace("amount", amount)
        self.to(constr)
        return self

    def simplify(self):
        """Attempts to find a unit that fits the fundamental quantities of this Unit.
        This does nothing if it can't find a better compound unit to use instead.
        
        >>> a = Unit('1 W')/Unit('1 A')
        >>> a
        1 W/A
        >>> a.simplify()
        1 V

        """
        constr = _get_construction(_parse_unit(self.unit),
                                   combine=False,
                                   listform=True)
        sig = _gen_signature(constr)
        if sig in _signatures:
            qty = _signatures[sig]
            if qty in _defaults:
                new_unit = _defaults[qty]
                self.to(new_unit)
        return self

    def __format__(self, format_spec):
        unit_str = self.unit.translate(self.to_specials)
        prefix = ''
        if 'USD' in unit_str:
            prefix = '$'
            unit_str = unit_str.replace('USD','')
            format_spec = '.2f'
        number = "{r:{f}}".format(r=self.value, f=format_spec)
        return "{}{} {}".format(prefix, number, unit_str).strip()

    def _true_repr(self):
        """
        This is the true __repr__ method that returns a representation that can 
        reconstruct the object. e.g.:

        >>> Unit('2 mm')._true_repr()
        "Unit(2, 'mm')"

        The __repr__ method should really be the __str__ method, but this is library is 
        intended to be used as an interactive calculator from the REPL, so the str() 
        output is desired without using print() from the REPL. If you really want the 
        conventional __repr__ output, this method will do it.

        """
        if isinstance(self.value, numbers.Number):
            return f"Unit({self.value:g}, '{self.unit}')"
        else:
            return ""

    def __repr__(self):
        """
        This outputs an easy to read string representation of the unit class for use with
        a REPL. For pragmatic reasons it doesn't return a representation that can be pasted
        into the REPL to reproduce the object (which is conventional). If you really want that,
        use the self._true_repr() method.

        >>> Unit('1 mm')
        1 mm

        """
        if isinstance(self.value, numbers.Number):
            unit_str = self.unit.translate(self.to_specials)
            prefix = ''
            if 'USD' in unit_str:
                prefix = '$'
                unit_str = unit_str.replace('USD','')
            return "{}{:g} {}".format(prefix,self.value, unit_str).strip()
        else:
            return ""

    def __mul__(self, other):
        other = Unit(other)
        if all([_check_consistent_units(self.unit, other.unit, silent=True),
                    (self.unit != other.unit), all( [self.unit,other.unit]) ]):
            # this ensures we don't have 2in * 3m = 6 in*m
            # If we have the same fundamental quantity (e.g. length), make them the same
            # before the operation
            other = other._tocopy(self.unit)
        newunit = self._new_unit(other, op="mul")
        newvalue = self.value * other.value  # type: ignore
        if (not newunit) and (not isinstance(other, Unit)):
            return Unit(newvalue, '')
        return Unit(newvalue, newunit or other.unit)  # type: ignore

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other, op='div'):
        other = Unit(other)
        if all([_check_consistent_units(self.unit, other.unit, silent=True),
                    (self.unit != other.unit), all( [self.unit,other.unit]) ]):
            # this ensures we don't have 2in * 3m = 6 in*m
            # If we have the same fundamental quantity (e.g. length), make them the same
            # before the operation
            other = other._tocopy(self.unit)
        newunit = self._new_unit(other, op=op)
        newvalue = (self.value / other.value) if op=='div' else (other.value/self.value)
        new_constr = _get_construction(_parse_unit(newunit))
        self_constr = self._get_construction()
        other_constr = other._get_construction()
        u = Unit(newvalue, newunit)
        if new_constr == self_constr:
            u.to(self.unit)
        elif new_constr == other_constr:
            u.to(other.unit)
        return u  # type: ignore

    def __rtruediv__(self, other):
        return self.__truediv__(other, op='rdiv')

    def __add__(self, other):
        if isinstance(other, Unit):
            _check_consistent_units(other.unit, self.unit)
            newunit = self.unit or other.unit
            other = convert(other.value, other.unit, self.unit)
        else:
            newunit = self.unit
        newvalue = self.value + other
        return Unit(newvalue, newunit)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Unit):
            _check_consistent_units(other.unit, self.unit)
            newunit = self.unit or other.unit
            other = convert(other.value, other.unit, self.unit)
        else:
            newunit = self.unit
        newvalue = self.value - other
        return Unit(newvalue, newunit)

    def __rsub__(self, other):
        if isinstance(other, Unit):
            _check_consistent_units(other.unit, self.unit)
            newunit = self.unit or other.unit
            other = convert(other.value, other.unit, self.unit)
        else:
            newunit = self.unit
        newvalue = other - self.value
        return Unit(newvalue, newunit)

    def __pow__(self, other):
        return Unit(self.value**other, self._new_unit(other, op="pow"))

    def __float__(self):
        return float(self.value)  # type: ignore

    def __int__(self):
        return int(self.value)  # type: ignore

    def __abs__(self):
        return Unit(abs(self.value), self.unit)  # type: ignore
    
    def __pos__(self):
        return self
    
    def __neg__(self):
        return Unit(-self.value, self.unit)  # type: ignore
    
    def __lt__(self, other):
        if isinstance(other, Unit):
            _check_consistent_units(other.unit, self.unit)
            other = convert(other.value, other.unit, self.unit)
        return self.value < other

    def __le__(self, other):
        if isinstance(other, Unit):
            _check_consistent_units(other.unit, self.unit)
            other = convert(other.value, other.unit, self.unit)
        return self.value <= other

    def __eq__(self, other):
        if isinstance(other, Unit):
            _check_consistent_units(other.unit, self.unit)
            other = convert(other.value, other.unit, self.unit)
        return self.value == other

    def __ne__(self, other):
        if isinstance(other, Unit):
            _check_consistent_units(other.unit, self.unit)
            other = convert(other.value, other.unit, self.unit)
        return self.value != other

    def __gt__(self, other):
        if isinstance(other, Unit):
            _check_consistent_units(other.unit, self.unit)
            other = convert(other.value, other.unit, self.unit)
        return self.value > other

    def __ge__(self, other):
        if isinstance(other, Unit):
            _check_consistent_units(other.unit, self.unit)
            other = convert(other.value, other.unit, self.unit)
        return self.value >= other


__all__ = [
    'Unit', 'convert', 'add_unit', 'list_units', 'import_units',
    'list_quantities'
]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    doctest.testfile('doctests.txt')
    doctest.testfile('README.md', optionflags=doctest.ELLIPSIS+doctest.NORMALIZE_WHITESPACE)

    # print(Unit(4, 'in2')/Unit(50.8,'mm'))
    # print(Unit(50.8,'mm2')/Unit(4, 'in'))
    # print(4/Unit('2 m'))
    # print(Unit('4 m')/Unit('2 m'))
    print(Unit('1 USD'))
    print(Unit('$1.00'))
    print("{:.10g}".format(Unit('1.00 USD/sqft')))
    # print(Unit('1 USD')/Unit('sqft'))
    # print(Unit('1 USD').to('pennies'))
    # print(Unit('4 m2')/Unit('2 m'))
    # print(Unit(50.8,'mm')*Unit(4, 'in'))
    # print(Unit('1 m')/Unit('1 m'))
    # print(Unit('1 m')/Unit('1 m') + Unit('1 m'))
    # print(Unit('1 m') + Unit('1 m')/Unit('1 m'))
    # a = Unit(1, 'in')
    # b = Unit(1, 'm')/Unit(1, 'm')
    # print(a)
    # print(a.value,'>', a.unit)
    # print(b)
    # print(b.value,'>', b.unit)
    # print(a+b)
    # print(b+a)
