# - python packages: pywin32, pandas, openpyxl
# pip install pywin32 pandas openpyxl

import re
import sys
from datetime import datetime, date, time
from xml.dom import minidom
import win32com.client
import pandas as pd

# Eka veli ekch folder_to_scan choose kara (separate excel generate karnyasathi)
FOLDERS_TO_SCAN = ["\\"]           # Task Scheduler Library
# FOLDERS_TO_SCAN = ["\\EDI Tasks"]  # EDI Tasks Folder
# FOLDERS_TO_SCAN = ["\\DevTasks"]   # Dev Tasks Folder


OUTPUT_XLSX = "scheduled_tasks_report.xlsx"


def safe_get_text(node_list, default=None):
    if not node_list or node_list.length == 0:
        return default
    node = node_list[0]
    if not node.firstChild:
        return default
    return node.firstChild.nodeValue


def parse_startboundary(start_str):
    if not start_str or not start_str.strip():
        return None

    s = start_str.strip()
    if s.endswith('Z'):
        s = s[:-1] + '+00:00'

    s = re.sub(r"(\.\d{7,})", lambda m: m.group(1)[:7], s)

    try:
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is not None:
            dt = dt.astimezone(tz=None).replace(tzinfo=None)
        return dt
    except Exception:
        pass

    patterns = [
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S%z",
    ]
    for p in patterns:
        try:
            return datetime.strptime(s, p)
        except Exception:
            continue

    m = re.search(r"(\d{4}-\d{2}-\d{2})[T\s]?(\d{2}:\d{2}:\d{2})", s)
    if m:
        try:
            return datetime.strptime(m.group(1) + ' ' + m.group(2), "%Y-%m-%d %H:%M:%S")
        except Exception:
            pass

    return None


def parse_trigger_element(trigger_elem):
    try:
        xml_str = trigger_elem.toxml()
        # StartBoundary
        start_text = safe_get_text(trigger_elem.getElementsByTagName('StartBoundary'))
        start_dt = parse_startboundary(start_text)

        result = {
            'trigger_type': None,
            'start_dt': start_dt,
            'time': start_dt.time() if start_dt else None,
            'days_of_week': [],
            'days_of_month': [],
            'months': [],
            'days_interval': None,
            'readable': None,
            'raw_xml': xml_str,
        }

        parts = []
        if start_dt:
            parts.append(f"Start: {start_dt.strftime('%Y-%m-%d %I:%M %p')}")
        else:
            parts.append("Start: (unparsed)")

        # Weekly
        weeks = trigger_elem.getElementsByTagName('ScheduleByWeek')
        if weeks and weeks.length > 0:
            result['trigger_type'] = 'weekly'
            dow_node = trigger_elem.getElementsByTagName('DaysOfWeek')
            if dow_node and dow_node.length > 0:
                days = [n.nodeName for n in dow_node[0].childNodes if n.nodeType == n.ELEMENT_NODE]
                result['days_of_week'] = days
                parts.append('Weekly on: ' + ', '.join(days))

        # Monthly
        months_nodes = trigger_elem.getElementsByTagName('ScheduleByMonth')
        if months_nodes and months_nodes.length > 0:
            result['trigger_type'] = 'monthly'
            months_node = trigger_elem.getElementsByTagName('Months')
            dom_node = trigger_elem.getElementsByTagName('DaysOfMonth')
            if months_node and months_node.length > 0:
                months = [n.nodeName for n in months_node[0].childNodes if n.nodeType == n.ELEMENT_NODE]
                result['months'] = months
            if dom_node and dom_node.length > 0:
                doms = []
                for n in dom_node[0].childNodes:
                    if n.nodeType == n.ELEMENT_NODE:
                        txt = safe_get_text(n.childNodes)
                    
                        try:
                            doms.append(int(txt))
                        except Exception:
                            try:
                                doms.append(int(n.nodeName))
                            except Exception:
                                pass
                result['days_of_month'] = doms
            parts.append('Monthly on days: ' + (', '.join(map(str, result['days_of_month'])) if result['days_of_month'] else '(none)'))

        # Daily
        day_nodes = trigger_elem.getElementsByTagName('ScheduleByDay')
        if day_nodes and day_nodes.length > 0:
            result['trigger_type'] = 'daily'
            di = trigger_elem.getElementsByTagName('DaysInterval')
            if di and di.length > 0:
                try:
                    result['days_interval'] = int(safe_get_text(di))
                except Exception:
                    result['days_interval'] = None
            parts.append('Daily' + (f' every {result["days_interval"]} day(s)' if result['days_interval'] else ''))

        result['readable'] = '; '.join(parts)
        return result

    except Exception as e:
        return {'trigger_type': None, 'start_dt': None, 'time': None, 'readable': f'(Unparsed Trigger: {e})', 'raw_xml': trigger_elem.toxml()}


def scan_folders_and_collect(folders):
    svc = win32com.client.Dispatch('Schedule.Service')
    svc.Connect()

    rows = []

    for folder_path in folders:
        try:
            folder = svc.GetFolder(folder_path)
        except Exception as e:
            print(f"Error: cannot open folder '{folder_path}': {e}")
            continue

        try:
            tasks = folder.GetTasks(0)
        except Exception as e:
            print(f"Error: cannot enumerate tasks in '{folder_path}': {e}")
            continue

        for t in tasks:
            try:
                task_name = t.Name
                task_path = f"{folder_path.rstrip('/')}/{task_name}"
                enabled = bool(t.Enabled)
                xml_text = t.Xml
                dom = minidom.parseString(xml_text)
                triggers_node_list = dom.getElementsByTagName('Triggers')

                if not triggers_node_list or triggers_node_list.length == 0:
                    # No triggers found — still record the task with empty trigger
                    rows.append({
                        'Folder': folder_path,
                        'TaskName': task_name,
                        'TaskPath': task_path,
                        'Enabled': enabled,
                        'TriggerType': None,
                        'TriggerStart': None,
                        'TriggerTime': None,
                        'ReadableTrigger': '(No Triggers)'
                    })
                    continue

                triggers_node = triggers_node_list[0]
                for trig in triggers_node.childNodes:
                    if trig.nodeType != trig.ELEMENT_NODE:
                        continue
                    parsed = parse_trigger_element(trig)

                    rows.append({
                        'Folder': folder_path,
                        'TaskName': task_name,
                        'TaskPath': task_path,
                        'Enabled': enabled,
                        'TriggerType': parsed.get('trigger_type'),
                        'TriggerStart': parsed.get('start_dt'),
                        'TriggerTime': parsed.get('time'),
                        'ReadableTrigger': parsed.get('readable') or parsed.get('raw_xml')
                    })

            except Exception as e:
                print(f"Warning: failed to process task '{getattr(t, 'Name', '<unknown>')}' in folder '{folder_path}': {e}")
                try:
                    rows.append({
                        'Folder': folder_path,
                        'TaskName': getattr(t, 'Name', '<unknown>'),
                        'TaskPath': f"{folder_path.rstrip('/')}/{getattr(t, 'Name', '<unknown>')}",
                        'Enabled': getattr(t, 'Enabled', None),
                        'TriggerType': None,
                        'TriggerStart': None,
                        'TriggerTime': None,
                        'ReadableTrigger': f'(Error parsing task: {e})'
                    })
                except Exception:
                    pass

    return rows


def write_rows_to_excel(rows, outpath):
    if not rows:
        print('No tasks/triggers found. Writing empty sheet.')
        df = pd.DataFrame(columns=['Folder','TaskName','TaskPath','Enabled','TriggerType','TriggerStart','TriggerTime','ReadableTrigger'])
    else:
        df = pd.DataFrame(rows)

    def time_to_str(tval):
        if pd.isna(tval) or tval is None:
            return ''
        if isinstance(tval, time):
            return tval.strftime('%H:%M:%S')
        # if datetime
        if isinstance(tval, datetime):
            return tval.time().strftime('%H:%M:%S')
        try:
            return str(tval)
        except Exception:
            return ''

    df['TriggerTimeStr'] = df['TriggerTime'].apply(time_to_str)


    def start_to_str(d):
        if pd.isna(d) or d is None:
            return ''
        if isinstance(d, datetime):
            try:
                return d.strftime('%Y-%m-%d %H:%M:%S')
            except Exception:
                return str(d)
        try:
            return str(d)
        except Exception:
            return ''

    df['TriggerStartStr'] = df['TriggerStart'].apply(start_to_str)

    # Order columns
    out_df = df[['Folder','TaskName','TaskPath','Enabled','TriggerType','TriggerStartStr','TriggerTimeStr','ReadableTrigger']]
    out_df = out_df.rename(columns={'TriggerStartStr': 'TriggerStart', 'TriggerTimeStr': 'TriggerTime'})


    try:
        out_df.sort_values(by=['Folder','TaskName','TriggerStart'], inplace=True, na_position='last')
    except Exception:
        pass

    # Writingto Excel
    try:
        out_df.to_excel(outpath, index=False)
        print(f'Wrote {len(out_df)} rows to {outpath}')
    except Exception as e:
        print(f'Error: failed to write Excel file {outpath}: {e}')


if __name__ == '__main__':
    print('Scanning folders:', FOLDERS_TO_SCAN)
    rows = scan_folders_and_collect(FOLDERS_TO_SCAN)
    write_rows_to_excel(rows, OUTPUT_XLSX)
    print('Done.')
