"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

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

def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    code_country_dict = {}
    missing_code_set = set()
    for country_code, plot_country_name in plot_countries.items():
        if plot_country_name in gdp_countries:
            code_country_dict[country_code] = plot_country_name
        else:
            missing_code_set.add(country_code)
    return code_country_dict, missing_code_set


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    missing_country_code = set()
    missing_gdp_values = set()
    country_gdp_year = {} 

    gdp_data_dict = read_csv_as_nested_dict(gdpinfo['gdpfile'],
                                          gdpinfo['country_name'],
                                          gdpinfo['separator'],
                                          gdpinfo['quote'])
    print(gdp_data_dict)
    for country_code in plot_countries.keys():

        # find values of plot_countries present as keys in temp_dict
        if plot_countries[country_code] in gdp_data_dict.keys():

            # find keys matching year parameter and suss out empty strings
            if (year in gdp_data_dict[plot_countries[country_code]] and
                gdp_data_dict[plot_countries[country_code]][year] != ''):

                country_gdp_year[country_code] = math.log10(float(
                            gdp_data_dict[plot_countries[country_code]][year]))

            else:
                missing_gdp_values.add(country_code)
        else:
            missing_country_code.add(country_code)

    return country_gdp_year, missing_country_code, missing_gdp_values


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    map_tuple = build_map_dict_by_name(gdpinfo, plot_countries, year)

    map_dict = map_tuple[0]
    missing_country_codes = map_tuple[1]
    missing_gdp_values = map_tuple[2]

    legend_label = 'GDP for ' + year
    plot_title = 'GDP by country for ' + year + ' (log scale), unified by common country NAME'

    worldmap_chart = pygal.maps.world.World()
    worldmap_chart = worldmap_chart.add(legend_label, map_dict)
    worldmap_chart = worldmap_chart.add('Missing from World Bank Data', missing_country_codes)
    worldmap_chart = worldmap_chart.add('No GDP data', missing_gdp_values)
    worldmap_chart.title = plot_title
    worldmap_chart.render_to_file(map_file)


def test_render_world_map():
    """
    Test the project code for several years.
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

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

test_render_world_map()
