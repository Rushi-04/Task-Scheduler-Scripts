TASKS = [
    {
        "id": "SAVRX_480",
        "task_folder": r"\EDI Tasks",
        "task_name": "L480 SAVRX 834",
        "parser": "savrx_generic",
        "file_prefix": "IBEW480_",
        "file_extension": ".pgp",

        # NEW 
        "schedule": {
            "days": ["daily"],          # OR ["monday", "thursday"]
            "time": "02:05"             # HH:MM (24-hour)
        }
    },
    {
        "id": "ANTHEM_521",
        "task_folder": r"\EDI Tasks",
        "task_name": "521 ANTHEM 834 WGS",
        "parser": "anthem_521",
        "file_prefix": "521",
        "file_extension": ".834",

        "schedule": {
            "days": ["friday"],
            "time": "06:50"
        }
    },
    {
        "id": "GVS_480",
        "task_folder": r"\EDI Tasks",
        "task_name": "480 GVS 834",
        "parser": "gvs_480",

        # used for filename matching
        "file_prefix": "GVS",
        "file_extension": ".TXT",

        "schedule": {
            "days": ["monday"],
            "time": "05:25"
        }
    },
    {
        "id": "OEW_834_VSP",
        "task_folder": r"\EDI Tasks",
        "task_name": "OEW 834 VSP",
        "parser": "oev_834_vsp",

        # not used but required by interface
        "file_prefix": "",
        "file_extension": "",

        "schedule": {
            "days": ["tuesday"],
            "time": "00:50"
        }
    },
    {
        "id": "HUMANA_FTP",
        "task_folder": r"\EDI Tasks",
        "task_name": "Humana FTP",
        "parser": "humana_ftp",

        # not required for this parser
        "file_prefix": "",
        "file_extension": "",

        "schedule": {
            "days": ["tuesday"],
            "time": "03:00"
        }
    },
    {
        "id": "DELTA_DENTAL_S98",
        "task_folder": r"\EDI Tasks",
        "task_name": "S98 834 to DELTA DENTAL",
        "parser": "delta_dental_s98",

        # not used by this parser
        "file_prefix": "",
        "file_extension": "",

        "schedule": {
            "days": ["tuesday"],
            "time": "03:00"
        }
    },
    {
        "id": "TRI_TRUHEAR_834",
        "task_folder": r"\EDI Tasks",
        "task_name": "TRI TRUHEAR 834",
        "parser": "tri_truhear_834",

        "file_prefix": "TRI",
        "file_extension": ".834",

        "schedule": {
            "days": ["tuesday"],
            "time": "06:45"
        }
    },
    {
        "id": "DELTA_DENTAL_TRI",
        "task_folder": r"\EDI Tasks",
        "task_name": "TRI 834 to DELTA DENTAL",
        "parser": "delta_dental_tri",

        "file_prefix": "TRI",
        "file_extension": ".834",

        "schedule": {
            "days": ["tuesday"],
            "time": "07:00"
        }
    },
    {
        "id": "AMO_CAREFIRST_RET",
        "task_folder": r"\EDI Tasks",
        "task_name": "AMO Carefirst Retiree",
        "parser": "carefirst_amo_retiree",

        # not used by this parser
        "file_prefix": "",
        "file_extension": "",

        "schedule": {
            "days": ["tuesday"],
            "time": "07:15"
        }
    },
    {
        "id": "DELTA_DENTAL_HWL",
        "task_folder": r"\EDI Tasks",
        "task_name": "HWL 834 DELTA DENTAL",
        "parser": "delta_dental_hwl",

        # not used by this parser
        "file_prefix": "",
        "file_extension": "",

        "schedule": {
            "days": ["tuesday"],
            "time": "07:15"
        }
    },
    {
        "id": "TRI_ANTHEM_WGS",
        "task_folder": r"\EDI Tasks",
        "task_name": "TRI 834 ANTHEM WGS",
        "parser": "tri_anthem_wgs",

        "file_prefix": "TRI",
        "file_extension": ".834",

        "schedule": {
            "days": ["tuesday"],
            "time": "08:20"
        }
    },
    {
        "id": "HWL_834_ANTHEM_WGS",
        "task_folder": r"\EDI Tasks",
        "task_name": "HWL 834 ANTHEM WGS",
        "parser": "anthem_wgs_hwl",

        # not required by this parser
        "file_prefix": "",
        "file_extension": "",

        "schedule": {
            "days": ["tuesday"],
            "time": "08:35"
        }
    },
    {
        "id": "TRI_SAVRX_834",
        "task_folder": r"\EDI Tasks",
        "task_name": "TRI SAVRX 834",
        "parser": "tri_savrx_834",

        "file_prefix": "TRICTYBLDM_",
        "file_extension": ".txt",

        "schedule": {
            "days": ["tuesday"],
            "time": "08:45"
        }
    },
    {
        "id": "UHC_TRI",
        "task_folder": r"\EDI Tasks",
        "task_name": "UHC TRI",
        "parser": "uhc_tri",

        # not used by this parser
        "file_prefix": "",
        "file_extension": "",

        "schedule": {
            "days": ["tuesday"],
            "time": "10:00"
        }
    },
    {
        "id": "ANTHEM_WGS_S98",
        "task_folder": r"\EDI Tasks",
        "task_name": "S98 ANTHEM WGS 834",
        "parser": "anthem_wgs_s98",

        # not used by this parser
        "file_prefix": "",
        "file_extension": "",

        "schedule": {
            "days": ["tuesday"],
            "time": "08:10"
        }
    },
    {
        "id": "PEBO_HEALTHCOMB_625",
        "task_folder": r"\EDI Tasks",
        "task_name": "625 PEBO HEALTHCOMB 834",
        "parser": "pebo_healthcomb_625",

        # not used by this parser
        "file_prefix": "",
        "file_extension": "",

        "schedule": {
            "days": ["tuesday", "thursday"],
            "time": "08:15"
        }
    },
    {
        "id": "AMO_CAREFIRST_SAM",
        "task_folder": r"\EDI Tasks",
        "task_name": "AMO CareFirst  Active and Retiree to SAM",  # ← EXACT
        "parser": "carefirst_amo_sam",

        "file_prefix": "AMO_834P_",
        "file_extension": ".txt",

        "schedule": {
            "days": ["tuesday", "wednesday"],
            "time": "09:25"
        }
    },
    {
        "id": "OEW_834_DELTA_DENTAL",
        "task_folder": r"\EDI Tasks",
        "task_name": "OEW 834 to DELTA DENTAL",  # ← EXACT
        "parser": "delta_dental_oew",

        "file_prefix": "4DIBEW",
        "file_extension": ".pgp",

        "schedule": {
            "days": ["wednesday"],
            "time": "00:40"
        }
    },
    {
        "id": "GVS_TRI",
        "task_folder": r"\EDI Tasks",
        "task_name": "GVS TRI",
        "parser": "gvs_tri",

        "file_prefix": "GVS_TRI",
        "file_extension": ".TXT",

        "schedule": {
            "days": ["thursday"],
            "time": "05:15"
        }
    },
    {
        "id": "L480_ANTHEM_WGS_834",
        "task_folder": r"\EDI Tasks",
        "task_name": "L480 ANTHEM WGS 834",
        "parser": "anthem_generic",

        "file_prefix": "480",
        "file_extension": ".834",

        "schedule": {
            "days": ["thursday"],
            "time": "07:00"
        }
    },
    {
        "id": "L82_ANTHEM_WGS_834",
        "task_folder": r"\EDI Tasks",
        "task_name": "L82 ANTHEM WGS 834",
        "parser": "anthem_generic",

        "file_prefix": "L82",
        "file_extension": ".834",

        "schedule": {
            "days": ["thursday"],
            "time": "07:10"
        }
    },
    {
        "id": "MEI_834_DELTA_DENTAL",
        "task_folder": r"\EDI Tasks",
        "task_name": "MEI 834 DELTA DENTAL",
        "parser": "mei_delta_dental",

        "file_prefix": "05589newmaryland_",
        "file_extension": ".txt",

        "schedule": {
            "days": ["thursday"],
            "time": "07:25"
        }
    },
    {
        "id": "MEI_CANCER",
        "task_folder": r"\EDI Tasks",
        "task_name": "MEI CANCER",
        "parser": "mei_cancer",

        "file_prefix": "MEI_CANCER_CLAIMS_",
        "file_extension": ".xls",

        "schedule": {
            "days": ["thursday"],
            "time": "08:05"
        }
    },
    {
        "id": "COSTCO_ELG_P42",
        "task_folder": r"\EDI Tasks",
        "task_name": "COSTCO ELG P42",
        "parser": "costco_p42",

        "file_prefix": "NVPSL_elig-",
        "file_extension": ".txt",

        "schedule": {
            "days": ["thursday"],
            "time": "10:45"
        }
    },
    {
        "id": "OEW_834_SAVRX",
        "task_folder": r"\EDI Tasks",
        "task_name": "OEW 834 SAVRX",
        "parser": "savrx_generic",

        "file_prefix": "OEWEDI_",
        "file_extension": ".pgp",

        "schedule": {
            "days": ["monday", "thursday"],
            "time": "16:20"
        }
    },
    {
        "id": "L82_834_SAVRX",
        "task_folder": r"\EDI Tasks",
        "task_name": "L82 834 SAVRX",
        "parser": "savrx_l82",

        "file_prefix": "SAVRX_L82_", # Prefix from general SAVRX pattern? Wait, let's check prefix.
        "file_extension": ".pgp",

        "schedule": {
            "days": ["monday", "thursday"],
            "time": "21:20"
        }
    },
    {
        "id": "PEBO_HEALTHCOMB_625",
        "task_folder": r"\EDI Tasks",
        "task_name": "625 PEBO HEALTHCOMB 834",
        "parser": "pebo_healthcomb_625",

        "file_prefix": "CP1021_834_",
        "file_extension": ".txt",

        "schedule": {
            "days": ["tuesday", "thursday"],
            "time": "08:15"
        }
    },
    {
        "id": "AMO_AHH_ELIGIBILITY",
        "task_folder": r"\EDI Tasks",
        "task_name": "AMO AHH Eligibility",
        "parser": "amo_ahh",

        "file_prefix": "",
        "file_extension": "",

        # "04:10 AM every Monday, Tuesday, Wednesday, Thursday, Friday, Saturday"
        "schedule": {
            "days": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"],
            "time": "04:10"
        }
    },
    {
        "id": "ANTHEM_WGS_997_RECON",
        "task_folder": r"\EDI Tasks",
        "task_name": "997 Recon Download Anthem_WGS",
        "parser": "anthem_wgs_997",

        "file_prefix": "FA",
        "file_extension": ".835",

        "schedule": {
            "days": ["daily"],
            "time": "05:00"
        }
    },
    {
        "id": "CAPRX_HWL",
        "task_folder": r"\EDI Tasks",
        "task_name": "CAPRX HWL",
        "parser": "caprx_hwl",

        "file_prefix": "IronWorkers_Elig_",
        "file_extension": ".txt",

        "schedule": {
            "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
            "time": "06:30"
        }
    },
    {
        "id": "LAF_WGS_834",
        "task_folder": r"\EDI Tasks",
        "task_name": "LAF WGS 834",
        "parser": "anthem_generic",

        "file_prefix": "LAF",
        "file_extension": ".834",

        "schedule": {
            "days": ["friday"],
            "time": "08:10"
        }
    },
    {
        "id": "VSP_TRICOUNTY",
        "task_folder": r"\EDI Tasks",
        "task_name": "VSP TRICOUNTY",
        "parser": "vsp_tricounty",

        "file_prefix": "",
        "file_extension": "",

        "schedule": {
            "days": ["friday"],
            "time": "08:50"
        }
    },
    {
        "id": "AMO_AHH_TOSAM",
        "task_folder": r"\EDI Tasks",
        "task_name": "AMO AHH ToSAM",
        "parser": "amo_ahh_tosam",

        "file_prefix": "AHH_ABC_Elig_ToAMO_",
        "file_extension": ".TXT",

        "schedule": {
            "days": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"],
            "time": "10:30"
        }
    },
    {
        "id": "OEW_HIGHMARK_834",
        "task_folder": r"\EDI Tasks",
        "task_name": "OEW HIGHMARK 834",
        "parser": "anthem_generic",

        "file_prefix": "OEW",
        "file_extension": ".834",

        "schedule": {
            "days": ["friday"],
            "time": "12:05"
        }
    },
    {
        "id": "OEW_MIR_HIGHMARK",
        "task_folder": r"\EDI Tasks",
        "task_name": "OEW MIR Highmark",
        "parser": "oew_mir_highmark",

        "file_prefix": "MIROUT.D",
        "file_extension": ".txt",

        "schedule": {
            "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
            "time": "15:00"
        }
    },
    {
        "id": "MUS_IWU_ANTHEM_WGS",
        "task_folder": r"\EDI Tasks",
        "task_name": "MUS IWU ANTHEM WGS",
        "parser": "anthem_generic",

        "file_prefix": "IWU",
        "file_extension": ".834",

        "schedule": {
            "days": ["friday"],
            "time": "06:00"
        }
    },
    {
        "id": "MUS_LBU_ANTHEM_WGS",
        "task_folder": r"\EDI Tasks",
        "task_name": "MUS LBU ANTHEM WGS",
        "parser": "anthem_generic",

        "file_prefix": "LBU",
        "file_extension": ".834",

        "schedule": {
            "days": ["friday"],
            "time": "06:15"
        }
    },
    {
        "id": "MNT_BANK_POSPAY",
        "task_folder": "\\",  # Represents single backslash '\'
        "task_name": "MNT BANK POSITIVE PAY",
        "parser": "mnt_bank_pospay",

        "file_prefix": "MEIMTB_",
        "file_extension": ".txt",

        "schedule": {
            "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
            "time": "22:00"
        }
    },
    {
        "id": "OPTIMED_P42",
        "task_folder": "\\",  # Represents single backslash '\'
        "task_name": "OPTIMED P42",
        "parser": "optimed_p42",

        "file_prefix": "P42_ELG_",
        "file_extension": ".csv",

        "schedule": {
            "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
            "time": "10:00"
        }
    },
    {
        "id": "KEYBANK_POSPAY",
        "task_folder": "\\",
        "task_name": "KeyBank Positive Pay - Wex L82",
        "parser": "keybank_pospay",

        "file_prefix": "ARP_L82_",
        "file_extension": ".KBARM.ARMOH",

        "schedule": {
            "days": ["daily"],
            "time": "07:30"
        }
    },
    {
        "id": "AMO_CAREFIRST_ACTIVE",
        "task_folder": r"\EDI Tasks",
        "task_name": "AMO Carefirst Active", # ← Fixed 'f' in Carefirst
        "parser": "amo_carefirst_active",

        "file_prefix": "AMO_834P_",
        "file_extension": ".txt",

        "schedule": {
            "days": ["tuesday", "wednesday"],
            "time": "09:25"
        }
    },
    {
        "id": "LYRA_ELG_OEW",
        "task_folder": r"\EDI Tasks",
        "task_name": "LYRA ELG OEW",
        "parser": "lyra_elg_oew",

        "file_prefix": "4thdistricthealthfund_",
        "file_extension": ".csv",

        "schedule": {
            "days": ["monday"],
            "time": "07:00"
        }
    },
    {
        "id": "L152_ANTHEM_834",
        "task_folder": r"\EDI Tasks",
        "task_name": "L152 ANTHEM 834 TO WGS",
        "parser": "anthem_generic",

        "file_prefix": "152",
        "file_extension": ".834",

        "schedule": {
            "days": ["monday"],
            "time": "08:00"
        }
    },
    {
        "id": "VBA_625_834",
        "task_folder": r"\EDI Tasks",
        "task_name": "625 VBA 834",
        "parser": "vba_625",

        "file_prefix": "vba",
        "file_extension": ".txt",

        "schedule": {
            "days": ["monday"],
            "time": "08:05"
        }
    },
    {
        "id": "SWORD_L82",
        "task_folder": r"\EDI Tasks",
        "task_name": "Sword_L82",
        "parser": "sword_generic",

        "file_prefix": "L82-Eligibility-",
        "file_extension": ".xls",

        "schedule": {
            "days": ["wednesday"],
            "time": "05:00"
        }
    },
    {
        "id": "SWORD_S98",
        "task_folder": r"\EDI Tasks",
        "task_name": "Sword_S98",
        "parser": "sword_generic",

        "file_prefix": "S98-Eligibility-",
        "file_extension": ".xls",

        "schedule": {
            "days": ["wednesday"],
            "time": "05:05"
        }
    }
]



EMAIL_API_URL = "http://104.153.122.230:8127/send-email"
EMAIL_RECIPIENTS = ["borkarrushi028@gmail.com"]





## TUESDAY :-
# Enabled Tasks Scheduled for Today:

# Task Name	Trigger Time


# \/NVA HWL	At 08:00 AM every Tuesday of every week, starting 05/30/2023
# \/NVA L82	At 08:30 AM every Tuesday of every week, starting 07/05/2023



# Wednesday :- 
# Enabled Tasks Scheduled for Today:

# Task Name	Trigger Time


# \EDI Tasks/Sword_S98	At 05:05 AM every Wednesday of every week, starting 09/11/2025
# \EDI Tasks/CIGNA TRI	At 05:15 AM every Wednesday of every week, starting 12/17/2025
# \EDI Tasks/S98 834 VSP	At 06:30 AM every Wednesday of every week, starting 07/08/2025
# \EDI Tasks/J84 ANTHEM WGS 834	At 06:45 AM every Wednesday of every week, starting 05/12/2025
# \EDI Tasks/AMO Carefirst Active	At 07:15 AM every Wednesday of every week, starting 09/01/2025
# \EDI Tasks/MEI 834 TELEDOC	At 08:00 AM every Wednesday of every week, starting 07/02/2025
# \EDI Tasks/MEI CANCER ELIGIBILITY	At 08:05 AM every Wednesday of every week, starting 07/17/2025
# \EDI Tasks/SAVRX J84	At 08:45 AM every Wednesday of every week, starting 12/22/2025
# \EDI Tasks/TRI SAVRX NON MEDICARE 834	At 08:45 AM every Wednesday of every week, starting 04/30/2025



# Thursday Tasks


# --------------------------- Friday ------------------------------


# \EDI Tasks/997 Recon Download Anthem_WGS	At 05:00 AM every 1 day(s), starting 09/01/2025 -- partial complete

# \EDI Tasks/CAPRX HWL	At 06:30 AM every Monday, Tuesday, Wednesday, Thursday, Friday of every week, starting 04/27/2023


# \EDI Tasks/ABC Claim INV_ErrorReport_AS400	At 07:30 AM every Tuesday, Wednesday, Thursday, Friday, Saturday of every week, starting 12/22/2022
# \EDI Tasks/MUSGROW Claim IN_ErrorReport_As400	At 07:45 AM every Tuesday, Wednesday, Thursday, Friday, Saturday of every week, starting 06/08/2023

# \EDI Tasks/HealthLink files	At 09:00 AM every Monday, Tuesday, Wednesday, Thursday, Friday of every week, starting 06/10/2025

# \/ITSPlatform Self-heal Utility	At 08:00 AM every 1 day(s), starting 08/28/2025




# -----------------------------------------------------------------

# Task Name	Trigger Time


# MONDAY TASKS


# \EDI Tasks/DELTA P625 834	At 08:45 AM every Monday of every week, starting 10/20/2023
# \EDI Tasks/MEI SAVRX 834	At 08:45 AM every Monday of every week, starting 08/26/2024
# \EDI Tasks/MEI 834	At 09:30 AM every Monday of every week, starting 05/14/2024
# \EDI Tasks/521 834 SAVRX	At 08:30 PM every Monday of every week, starting 07/07/2025
# \EDI Tasks/S98 834 LABONE	At 08:45 PM every Monday of every week, starting 07/08/2025
# \EDI Tasks/OEW 834 LABONE	At 09:40 PM every Monday of every week, starting 07/08/2025

# -----------------------------------------------------------------


# TEMPLATE

We have to add a new task now, this is the required info you requested to create a new task.

one line info: \EDI Tasks/Sword_S98	At 05:05 AM every Wednesday of every week, starting 09/11/2025

Task Name: Sword_S98
Log Filename: Log.txt
Log Location: C:\Transfer_Programs\SWORD\S98
Sample : 


C:\Windows\system32>DEL D:\Transfers\Sword\S98\sword* 

C:\Windows\system32>REM load data from BICC 

C:\Windows\system32>"C:\Program Files (x86)\IBM\Client Access\rxferpcb" C:\Transfer_Programs\SWORD\S98\sword.dtf  bicc sailfish 

IBM i Access for Windows
Version 7  Release 1  Level 0
IBM i Access Data Transfer RXFERPCB
(C) Copyright IBM Corporation and Others 1984, 2010.  All rights reserved.
U.S. Government Users Restricted Rights - Use, duplication or disclosure
  restricted by GSA ADP Schedule Contract with IBM Corp.
Licensed Materials - Property of IBM


Transfer request C:\Transfer_Programs\SWORD\S98\sword.dtf SUCCESSFUL.

   Elapsed transfer time: 0 hours 0 minutes 1.15 seconds (1015 ms)
   CompletionTime          = 2026-2-4 5.5.1.0
   Rows Transferred        = 2242
   Data Warnings Occurred  = No
   Data Errors Occurred    = No

C:\Windows\system32>REM rename file  

C:\Windows\system32>for /F "tokens=2-4 delims=/ " %a in ('date /t') do set filename=S98-Eligibility-%c%a%b.xls 

C:\Windows\system32>set filename=S98-Eligibility-20260204.xls 

C:\Windows\system32>echo S98-Eligibility-20260204.xls 
S98-Eligibility-20260204.xls

C:\Windows\system32>ren D:\Transfers\Sword\S98\sword.xls S98-Eligibility-20260204.xls 

C:\Windows\system32>ftpscrpt -b -p ProductionSites!SWORD_S98 -f C:\Transfer_Programs\SWORD\S98\FTPscript_Put.scp 


Processing Line 1 [TRACE  Screen]



Processing Line 2 [LOG Screen]



Processing Line 3 [Connect]

Finding Host ftp.us.swordhealth.com ...

Connecting to 35.192.106.126:22

Connected to 35.192.106.126:22 in 0.033076 seconds, Waiting for Server Response

Server Welcome: SSH-2.0-SFTPGo_2.5.1

Client Version: SSH-2.0-WS_FTP-12.9.0-0

RSA Signature Verified

Session Keys Created
Ciphers Created

New Client->Server ciphers in place.

New Client->Server ciphers in place.

Completed SSH Key Exchange.  New Keys in place.

Trying authentication method: "publickey"

User Authenticated OK!

Completed SSH User Authentication.

Started subsystem "sftp" on channel 0760a2ce

SFTP Protocol Version 3 OK

Server supports SFTP Extension: statvfs@openssh.com

        32

sftp protocol initialized

Changing remote directory to "/outbound/eligibility/files"



Processing Line 4 [lcd D:\Transfers\SWORD\S98]



Processing Line 5 [mput S98*]

No destination folder. The current directory '/outbound/eligibility/files' is used.

Getting Dirlisting

# transferred 4387 bytes in 0.063 seconds, 552.769 kbps ( 69.096 kBps), transfer succeeded.

Starting request
Opening remote file "/outbound/eligibility/files/S98-Eligibility-20260204.xls" for writing

Uploading local file "D:\Transfers\SWORD\S98\S98-Eligibility-20260204.xls"

# transferred 1383936 bytes in 0.585 seconds, 18938.071 kbps ( 2367.259 kBps), transfer succeeded.

Transfer request completed with status: Finished



Processing Line 6 [CLOSE]

Sending channel close message for channel 0760a2ce

SSH Transport closed.

Connection closed.  Ready for next connection.


C:\Windows\system32>move D:\Transfers\Sword\S98\S98-Eligibility-20260204.xls D:\Transfers\Sword\S98\backups\ 
        1 file(s) moved.
