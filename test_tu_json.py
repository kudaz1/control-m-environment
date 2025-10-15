#!/usr/bin/env python3
"""
Test específico con tu JSON completo
"""
import requests
import json

def test_tu_json():
    print("🧪 Probando tu JSON completo...")
    print("=" * 50)
    
    # Tu JSON exacto
    payload = {
        "environment": "Q5",
        "json_data": {
            "GENER_NEXUS-DEMOGRAFICO-CARLOS": {
                "Type": "SimpleFolder",
                "ControlmServer": "COOPEUCH",
                "OrderMethod": "Manual",
                "CC1040P2": {
                    "Type": "Job:OS400:Full:CommandLine",
                    "CommandLine": "CALL PGM(RBIENVFCL)  PARM('CTINTDEM' 'NEXDEM')",
                    "SubApplication": "GENER_NEXUS-DEMOGRAFICO-CARLOS",
                    "Priority": "Very Low",
                    "FileName": "CC1040P2",
                    "Confirm": True,
                    "Host": "ibsqa",
                    "FilePath": "CC1040P2",
                    "CreatedBy": "emuser",
                    "Description": "NEXUS-DEMOGRAFICO",
                    "RunAs": "Q7ABATCH",
                    "Application": "GENER_NEXUS-DEMOGRAFICO-CARLOS",
                    "Variables": [
                        {"tm": "%%TIME"},
                        {"HHt": "%%SUBSTR %%tm  1 2"},
                        {"MMt": "%%SUBSTR %%tm  3 2"},
                        {"SSt": "%%SUBSTR %%tm  5 2"},
                        {"HORA": "%%HHt:%%MMt:%%SSt"},
                        {"OS400-AEV_LEN": "4000"},
                        {"OS400-JOB_NAME": "CC1040P2"},
                        {"OS400-MEM_NAME": "CC1040P2"},
                        {"OS400-MEM_LIB": "CC1040P2"},
                        {"OS400-JOBD": "*USRPRF"},
                        {"OS400-CURLIB": "Q7AHIFILES"},
                        {"OS400-JOB_OWNER": "Q7ABATCH"}
                    ],
                    "RerunLimit": {
                        "Units": "Minutes",
                        "Every": "0"
                    },
                    "When": {
                        "WeekDays": ["MON", "TUE", "WED", "THU", "FRI"],
                        "MonthDays": ["NONE"],
                        "FromTime": "2000",
                        "DaysRelation": "OR",
                        "ConfirmationCalendars": {
                            "Calendar": "Cal_Habil"
                        }
                    },
                    "JobAFT": {
                        "Type": "Resource:Pool",
                        "Quantity": "1"
                    },
                    "IfBase:Folder:Output_12": {
                        "Type": "If:Output",
                        "Code": "código de finalización 20",
                        "Action:SetToNotOK_0": {
                            "Type": "Action:SetToNotOK"
                        },
                        "Mail_1": {
                            "Type": "Action:Mail",
                            "Subject": "%%APPLIC (%%APPLGROUP - %%JOBNAME) ERROR_PROCESO",
                            "To": "controlmerror@coopeuch.cl",
                            "Message": "Estimado, informo a Ud. que el job %%JOBNAME y proceso  detallado en el asunto de este mail, finalizµ incorrectamente. AdemÃs, se registra el promedio del tiempo de ejecuciµn(en segundos)  y hora de termino del proceso: %%AVG_TIME  - %%DAY/%%MONTH/%%$YEAR %%HORA\\n\\nAtte.\\n\\nOperador de Sistema.",
                            "AttachOutput": False
                        }
                    },
                    "IfBase:Folder:Output_13": {
                        "Type": "If:Output",
                        "Code": "(error,ERROR,Permission denied,File Not Found)",
                        "Action:SetToNotOK_0": {
                            "Type": "Action:SetToNotOK"
                        },
                        "Mail_1": {
                            "Type": "Action:Mail",
                            "Subject": "%%APPLIC (%%APPLGROUP - %%JOBNAME) ERROR_PROCESO",
                            "To": "controlmerror@coopeuch.cl",
                            "Message": "Estimado, informo a Ud. que el job %%JOBNAME y proceso  detallado en el asunto de este mail, finalizµ incorrectamente. AdemÃs, se registra el promedio del tiempo de ejecuciµn(en segundos)  y hora de termino del proceso: %%AVG_TIME  - %%DAY/%%MONTH/%%$YEAR %%HORA\\n\\nAtte.\\n\\nOperador de Sistema.\\n",
                            "AttachOutput": False
                        }
                    },
                    "IfBase:Folder:Output_14": {
                        "Type": "If:Output",
                        "Code": "Mensaje . . . . :   C",
                        "Action:SetToNotOK_0": {
                            "Type": "Action:SetToNotOK"
                        },
                        "Mail_1": {
                            "Type": "Action:Mail",
                            "Subject": "%%APPLIC (%%APPLGROUP - %%JOBNAME) ERROR_PROCESO",
                            "To": "controlmerror@coopeuch.cl",
                            "Message": "Estimado, informo a Ud. que el job %%JOBNAME y proceso  detallado en el asunto de este mail, finalizµ incorrectamente. AdemÃs, se registra el promedio del tiempo de ejecuciµn(en segundos)  y hora de termino del proceso: %%AVG_TIME  - %%DAY/%%MONTH/%%$YEAR %%HORA\\n\\nAtte.\\n\\nOperador de Sistema.\\n",
                            "AttachOutput": False
                        }
                    },
                    "IfBase:Folder:Output_15": {
                        "Type": "If:Output",
                        "Code": "código de finalización 0",
                        "Action:SetToOK_0": {
                            "Type": "Action:SetToOK"
                        },
                        "Mail_1": {
                            "Type": "Action:Mail",
                            "Subject": "%%APPLIC (%%APPLGROUP - %%JOBNAME) OK_PROCESO",
                            "To": "controlmok@coopeuch.cl",
                            "Message": "Estimado, informo a Ud. que el job  %%JOBNAME y proceso detallado en el asunto de este mail, finalizµ sin problemas. AdemÃs, se registra el promedio del tiempo de ejecuciµn (en segundos) y hora de termino del proceso: %%AVG_TIME  - %%DAY/%%MONTH/%%$YEAR %%HORA\\nAtte.\\n\\nOperador de Sistema.",
                            "AttachOutput": False
                        }
                    },
                    "IfBase:Folder:Output_16": {
                        "Type": "If:Output",
                        "Code": "Codigo Retorno",
                        "Action:SetToNotOK_0": {
                            "Type": "Action:SetToNotOK"
                        },
                        "Mail_1": {
                            "Type": "Action:Mail",
                            "Subject": "%%APPLIC (%%APPLGROUP - %%JOBNAME) ERROR_PROCESO",
                            "To": "controlmerror@coopeuch.cl",
                            "Message": "Estimado, informo a Ud. que el job %%JOBNAME y proceso  detallado en el asunto de este mail, finalizµ incorrectamente. AdemÃs, se registra el promedio del tiempo de ejecuciµn(en segundos)  y hora de termino del proceso: %%AVG_TIME  - %%DAY/%%MONTH/%%$YEAR %%HORA\\n\\nAtte.\\n\\nOperador de Sistema.\\n",
                            "AttachOutput": False
                        }
                    },
                    "eventsToWaitFor": {
                        "Type": "WaitForEvents",
                        "Events": [
                            {"Event": "PRECIERRE-EODAY-NEXUS-001-IBS-DIA"}
                        ]
                    }
                }
            }
        }
    }
    
    try:
        print("📤 Enviando request...")
        response = requests.post(
            "http://localhost:5000/api/replace-environment",
            json=payload,
            timeout=10
        )
        
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ ÉXITO!")
            print(f"   Ambiente aplicado: {result.get('environment')}")
            
            # Verificar cambios específicos
            modified = result.get('modified_json', {})
            folder = modified.get('GENER_NEXUS-DEMOGRAFICO-CARLOS', {})
            job = folder.get('CC1040P2', {})
            
            print("\n🔍 CAMBIOS VERIFICADOS:")
            print(f"   RunAs: {job.get('RunAs')}")
            
            variables = job.get('Variables', [])
            for var in variables:
                if 'OS400-CURLIB' in var:
                    print(f"   OS400-CURLIB: {var['OS400-CURLIB']}")
                if 'OS400-JOB_OWNER' in var:
                    print(f"   OS400-JOB_OWNER: {var['OS400-JOB_OWNER']}")
            
            # Verificar que los cambios son correctos
            runas = job.get('RunAs')
            if runas == 'Q5ABATCH':
                print("\n✅ CORRECTO: Q7ABATCH → Q5ABATCH")
            else:
                print(f"\n❌ ERROR: RunAs debería ser Q5ABATCH, pero es {runas}")
            
            curlib = None
            jobowner = None
            for var in variables:
                if 'OS400-CURLIB' in var:
                    curlib = var['OS400-CURLIB']
                if 'OS400-JOB_OWNER' in var:
                    jobowner = var['OS400-JOB_OWNER']
            
            if curlib == 'Q5AHIFILES':
                print("✅ CORRECTO: Q7AHIFILES → Q5AHIFILES")
            else:
                print(f"❌ ERROR: OS400-CURLIB debería ser Q5AHIFILES, pero es {curlib}")
                
            if jobowner == 'Q5ABATCH':
                print("✅ CORRECTO: Q7ABATCH → Q5ABATCH")
            else:
                print(f"❌ ERROR: OS400-JOB_OWNER debería ser Q5ABATCH, pero es {jobowner}")
            
            print("\n📄 JSON COMPLETO MODIFICADO:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        else:
            print(f"❌ Error HTTP {response.status_code}")
            print(f"   Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_tu_json()
