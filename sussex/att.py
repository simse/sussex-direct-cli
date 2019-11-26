from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup
import click
from tabulate import tabulate

from sussex import auth

def get_attendance(ignore=[], ignore_optionals=True, print_table=True):
    html = auth.make_get('https://direct.sussex.ac.uk/page.php?page=course_progress').text
    page = BeautifulSoup(html, 'lxml')
    attendance_links = []

    # Parse table data from Sussex Direct
    for row in page.find_all('tr'):
        for link in row.find_all('a'):
            try:
                if 'cms_attendance_report' in link['href']:
                    attendance_str = link.text
                    total = int(attendance_str.split('/')[1])
                    attended = int(attendance_str.split('/')[0])
                    query = parse_qs(urlparse(link['href'])[4])
                    module_name = row.find('td').text
                    module_code = row.find_all('td')[1].text

                    backtrack = len(attendance_links) - 1
                    while 'Semester' in module_name:
                        module_name = attendance_links[backtrack]['module_name']
                        backtrack -= 1

                    backtrack = len(attendance_links) - 1
                    while 'G' not in module_code:
                        module_code = attendance_links[backtrack]['module_code']
                        backtrack -= 1

                    attendance_links.append({
                        'module_name': module_name,
                        'module_code': module_code,
                        'module_id': int(query['rul_code'][0]),
                        'group_id': int(query['tgo_code'][0]),
                        'attendance_string': attendance_str,
                        'total_count': total,
                        'attended_count': attended,
                        'percentage': round(attended / total * 100)
                    })
            except KeyError:
                pass

    # Calculate average
    total = 0
    attended = 0

    for a in attendance_links:
        if a['group_id'] not in ignore and a['module_code'] not in ignore:
            # Detect if optional
            if a['percentage'] > 50 and ignore_optionals or not ignore_optionals:
                total += a['total_count']
                attended += a['attended_count']

    average = round(attended / total * 100, 1)

    # Print table
    table = attendance_links
    for t in table:
        del t['total_count']
        del t['attended_count']
        del t['module_id']
        t['percentage'] = str(t['percentage']) + '%'


    click.echo(tabulate(table, headers={
        'module_name': 'Module name',
        'module_code': 'Module code',
        'group_id': 'Group ID',
        'attendance_string': 'Attendance',
        'percentage': 'Percentage',
    }, tablefmt='github'))
    click.secho('\nYour average attendance is: {}%{}'.format(average, ', ignoring optional modules.' if ignore_optionals else '.'))