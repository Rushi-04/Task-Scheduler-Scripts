import win32com.client
from xml.dom import minidom
from datetime import datetime
import requests

EMAIL_TO = ["borkarananta028@gmail.com", "akumar@abchldg.com"]  # -- Testing
# EMAIL_TO = "akumar@abchldg.com"
EMAIL_API_URL = "http://104.153.122.230:8127/send-email"

def parse_trigger(trigger_xml):
    try:
        trigger = minidom.parseString(trigger_xml).documentElement
        start = trigger.getElementsByTagName("StartBoundary")[0].firstChild.nodeValue
        start_dt = datetime.fromisoformat(start)

        logic = {
            "start_date": start_dt.date(),
            "time": start_dt.time(),
            "type": None,
            "days": [],
            "months": [],
            "interval": None
        }

        readable = f"At {start_dt.strftime('%I:%M %p')}"

        if trigger.getElementsByTagName("ScheduleByWeek"):
            logic["type"] = "weekly"
            days = trigger.getElementsByTagName("DaysOfWeek")[0]
            logic["days"] = [d.nodeName for d in days.childNodes if d.nodeType == d.ELEMENT_NODE]
            readable += f" every {', '.join(logic['days'])} of every week"
        elif trigger.getElementsByTagName("ScheduleByMonth"):  
            logic["type"] = "monthly"
            months = trigger.getElementsByTagName("Months")[0] 
            days = trigger.getElementsByTagName("DaysOfMonth")[0]  
            logic["months"] = [m.nodeName for m in months.childNodes if m.nodeType == m.ELEMENT_NODE]
            logic["days"] = [int(d.firstChild.nodeValue) for d in days.childNodes if d.nodeType == d.ELEMENT_NODE]
            readable += f" on day {', '.join(map(str, logic['days']))} of {', '.join(logic['months'])}"
        elif trigger.getElementsByTagName("ScheduleByDay"):
            logic["type"] = "daily"
            interval = int(trigger.getElementsByTagName("DaysInterval")[0].firstChild.nodeValue)
            logic["interval"] = interval
            readable += f" every {interval} day(s)"

        readable += f", starting {start_dt.strftime('%m/%d/%Y')}"
        return readable, logic

    except Exception:
        return f"(Unparsed Trigger)", {}

def is_scheduled_today(logic):
    today = datetime.today().date()
    weekday = datetime.today().strftime("%A")
    day = datetime.today().day
    month = datetime.today().strftime("%B")

    if today < logic.get("start_date", today):   
        return False   

    trigger_type = logic.get("type")
    if trigger_type == "daily":  
        return (today - logic["start_date"]).days % logic["interval"] == 0
    elif trigger_type == "weekly":
        return weekday in logic["days"]
    elif trigger_type == "monthly":
        return (day in logic["days"]) and (month in logic["months"])

    return False

def list_tasks_with_readable_triggers(subfolder_path):
    svc = win32com.client.Dispatch("Schedule.Service")
    svc.Connect()

    folder = svc.GetFolder("\\")
    for part in subfolder_path.split("\\"):
        folder = folder.GetFolder(part)

    tasks = folder.GetTasks(0)
    results = []

    for t in tasks:
        if not t.Enabled:
            continue

        task_xml = t.Xml
        dom = minidom.parseString(task_xml)
        triggers_node = dom.getElementsByTagName("Triggers")

        if triggers_node:
            for trig in triggers_node[0].childNodes:
                if trig.nodeType == trig.ELEMENT_NODE:
                    xml_str = trig.toxml()
                    readable, logic = parse_trigger(xml_str)
                    if is_scheduled_today(logic):
                        #Prefix folder name to task name
                        results.append((f"{subfolder_path}/{t.Name}", readable))

    return results

def build_html_email(task_data):
    if not task_data:
        return "<p><strong>No tasks are scheduled to run today in any of the folders.</strong></p>"

    html = """
    <html>
    <head>
        <style>
            table {
                font-family: Arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head> 
    <body>  
        <p><strong>0</strong></p>  
        <table>
            <tr><th>Task Name</th><th>Trigger Time</th></tr>
    """    
    for task_name, trigger in task_data:
        html += f"<tr><td>{task_name}</td><td>{trigger}</td></tr>" 

    html += """
        </table>
    </body>
    </html>
    """
    return html

def send_email(html_body):
    for recipient in EMAIL_TO:
        payload = {
            "email": recipient,
            "subject": "Scheduled Tasks for Today",
            "body": html_body
        }

        response = requests.post(EMAIL_API_URL, data=payload)
        if response.status_code == 200:
            print(f"Email sent successfully to {recipient}")
        else:
            print(f"Failed to send email to {recipient}. Status: {response.status_code}, Response: {response.text}")


if __name__ == "__main__":
    folders = ["DevTasks", "EDI Tasks"]  
    # folders = ["Microsoft\\Windows\\Application Experience"]
    all_tasks = []  
  
    for folder in folders:
        try:
            tasks = list_tasks_with_readable_triggers(folder)
            all_tasks.extend(tasks) 
        except Exception as e:
            print(f"Error accessing folder '{folder}': {e}")

    html_body = build_html_email(all_tasks)
    send_email(html_body) 

#Code Last Updated on 18-07-2025 -- rushi -- new code   