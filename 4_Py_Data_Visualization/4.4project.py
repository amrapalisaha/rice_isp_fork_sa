"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table

def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    code_dict = read_csv_as_nested_dict(codeinfo['codefile'],
                                              codeinfo['plot_codes'],
                                              codeinfo['separator'],
                                              codeinfo['quote'])
    new_dict = {}
    for key, inner_dict in code_dict.items():
        new_dict[key] = inner_dict[codeinfo['data_codes']]
    return new_dict


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    converted = build_country_code_converter(codeinfo)

    converted_lower = {}
    for key, value in converted.items():
        converted_lower[key.lower()] = value.lower()

    gdp_lower = {}
    for key in gdp_countries:
        gdp_lower[key.lower()] = key

    output = {}
    missing = set()
    for code in plot_countries:
        if (code.lower() in converted_lower and
           converted_lower[code.lower()] in gdp_lower):
            output[code] = gdp_lower[converted_lower[code.lower()]]
        else:
            missing.add(code)

    return output, missing


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    gdp_data_dict = read_csv_as_nested_dict(gdpinfo['gdpfile'],
                                          gdpinfo['country_code'],
                                          gdpinfo['separator'],
                                          gdpinfo['quote'])

    reconciled = reconcile_countries_by_code(codeinfo, plot_countries, gdp_data_dict)

    missing_country_code = reconciled[1]
    missing_gdp_values = set()
    country_code_gdp_year = {}

    for country_code in reconciled[0]:
        if gdp_data_dict[reconciled[0][country_code]][year] == "":
            missing_gdp_values.add(country_code)
        else:
            country_code_gdp_year[country_code] = math.log10(float(
                    gdp_data_dict[reconciled[0][country_code]][year]))

    return country_code_gdp_year, missing_country_code, missing_gdp_values


def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    map_tuple = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)

    map_dict = map_tuple[0]
    missing_country_codes = map_tuple[1]
    missing_gdp_values = map_tuple[2]

    legend_label = 'GDP for ' + year
    plot_title = 'GDP by country for ' + year + ' (log scale), unified by common country CODE'

    worldmap_chart = pygal.maps.world.World()
    worldmap_chart = worldmap_chart.add(legend_label, map_dict)
    worldmap_chart = worldmap_chart.add('Missing from World Bank Data', missing_country_codes)
    worldmap_chart = worldmap_chart.add('No GDP data', missing_gdp_values)
    worldmap_chart.title = plot_title
    worldmap_chart.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()
