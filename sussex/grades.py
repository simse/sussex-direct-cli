from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup
import click
from tabulate import tabulate

from sussex import auth

def average_grade():
    html = auth.make_get('https://direct.sussex.ac.uk/page.php?page=course_progress').text
    page = BeautifulSoup(html, 'lxml')
    grade_links = []
    grades = []

    for link in page.find_all('a'):
        try:
            if 'student_module_marks' in link['href'] and link.text != '':
                grade_links.append(link['href'])

        except KeyError:
            pass

    for link in grade_links:
        html = auth.make_get('https://direct.sussex.ac.uk' + link).text
        page = BeautifulSoup(html, 'lxml')
        assessments = []

        module_name = page.select_one('#student_module_marks_subtitle').text

        click.secho(module_name, underline=True)

        for row in page.select("#student_module_marks_border tr.formlet_row_other"):
            offset = 1
            try:
                row.find('td')['rowspan']
            except(KeyError):
                offset = 0

            cells = row.find_all('td')
            assessment = {
                'type': cells[0 + offset].text,
                'weight': float(cells[1 + offset].text.replace('%', '')),
                'due_date': None,
                'submitted_date': cells[3 + offset].text,
                'module_pass_mark': int(cells[4 + offset].text if cells[4 + offset].text else 0),
                'mark_obtained_str': cells[5 + offset].text,
                'mark_percentage': float(cells[6 + offset].text if cells[6 + offset].text else 0),
                'mark_obtained': 0,
                'mark_total': 0
            }

            # Compute mark obtained in seperate parts
            try:
                assessment['mark_obtained'] = int(cells[5 + offset].text.split('/')[0])
                assessment['mark_total'] = int(cells[5 + offset].text.split('/')[1])
            except(ValueError):
                pass

            assessments.append(assessment)

        print(tabulate(assessments, tablefmt='github'))

        # Calculate module grade
        grade = 0

        for a in assessments:
            grade += a['weight'] * (a['mark_percentage'] / 100)

        grades.append(grade)
        print('The weighted grade for this module is: \u001b[1m{}%\u001b[0m'.format(round(grade, 2)))

    click.secho('\n\nYou average grade is: {}%'.format(round(sum(grades) / len(grades), 1)), bold=True)