# -*- coding: utf-8 -*-

"""
Utility functions that are commonly used within the package.
"""

from datetime import datetime
import os
import re


def currency_to_num(string, data_type=int):
    """
    Converts a pound sterling currency value into a number.
    >>> currency_to_num("£250,000")
    >>> 250000
    :param string: value of currency as a string
    :param data_type: intended data type of output
    :return: numerical value of currency
    """

    value = string.strip().replace('£', '').replace(',', '').replace('pcm', '')
    try:
        return data_type(value)
    except ValueError:
        return value


def myround(num, base=50):
    """
    Round a number to a nearest number specified by `base`.
    >>> myround(110380, base=50)
    >>> 110400
    :param num: number to round
    :param base: number to which to round to nearest
    :return: rounded number
    """
    return int(base * round(float(num)/base))


def text_or_none(soup, data_type=str):
    """Converts soup text to a data type else return None if soup has no text attribute."""
    try:
        return data_type(soup.text)
    except AttributeError:
        return ''


def to_datetime(date):
    """
    Converts string to a date type.
    >>> to_datetime('21st May 2012')
    >>> datetime(2012, 5, 21, 0, 0)
    """
    date = re.sub(r'\d+(st|nd|rd|th)', lambda m: m.group()[:-2].zfill(2), date)
    return datetime.strptime(date, '%d %b %Y')


def get_station_name(soup, station_num):
    """Extracts station name from string."""
    return soup[station_num].text.strip().split('(')[0].strip()


def dist_to_num(soup):
    """Extracts number from string e.g. '(0.4 miles)' -> 0.4"""
    return float(soup.text.strip().split('(')[-1].replace(')', '').split(' ')[0])


def text_inbetween(text, left, right):
    """Gets string in between two other strings, `left` and `right`."""
    return re.search(r'{}(.*){}'.format(left, right), text).group(1)


def output_data(df, location, output_dir='data'):
    """
    Outputs csv data to disk.  Checks to see if file exists first in which case
    it will append to this file otherwise create new file.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_path = '{}/data_{}.csv'.format(output_dir, location).lower()
    if os.path.isfile(file_path):
        df.to_csv(file_path, mode='a', index=False, header=False)
    else:
        df.to_csv(file_path, index=False)


def insert_into_db(db_conn, cur, data, schema, table):
    """
    Insert dictionary data into a sql database.
    :param db_conn: pymysql database connection
    :param cur: db cursor
    :param data: dictionary values
    :param schema: name of sql schema
    :param table: name of sql table
    """
    placeholder = ', '.join(['%s'] * len(data))
    insert_query = 'insert into {schema}.{table} ({columns}) values ({values});'.format(
        schema=schema, table=table, columns=','.join(data.keys()), values=placeholder)
    cur.execute(insert_query, [str(i) for i in data.values()])
    db_conn.commit()
