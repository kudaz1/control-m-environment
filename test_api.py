"""
Script para probar la API localmente antes de integrar con Jira
"""
import requests
import json

# URL base de la API (cambiar según dónde esté desplegada)
BASE_URL = "http://localhost:5000"

# JSON de ejemplo (el que proporcionaste)
SAMPLE_JSON = {
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


def test_health():
    """Probar que la API está funcionando"""
    print("\n=== Test 1: Health Check ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")


def test_replace_environment(environment):
    """Probar el reemplazo de ambiente"""
    print(f"\n=== Test 2: Reemplazar ambiente a {environment} ===")
    try:
        payload = {
            "environment": environment,
            "json_data": SAMPLE_JSON
        }
        
        response = requests.post(
            f"{BASE_URL}/api/replace-environment",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        result = response.json()
        
        if result.get('success'):
            print(f"✓ Éxito: Ambiente cambiado a {result.get('environment')}")
            
            # Verificar algunos campos clave
            modified = result.get('modified_json', {})
            folder = modified.get('GENER_NEXUS-DEMOGRAFICO-CARLOS', {})
            job = folder.get('CC1040P2', {})
            
            print(f"\nCampos verificados:")
            print(f"  - RunAs: {job.get('RunAs')}")
            
            variables = job.get('Variables', [])
            for var in variables:
                if 'OS400-CURLIB' in var:
                    print(f"  - OS400-CURLIB: {var['OS400-CURLIB']}")
                if 'OS400-JOB_OWNER' in var:
                    print(f"  - OS400-JOB_OWNER: {var['OS400-JOB_OWNER']}")
        else:
            print(f"✗ Error: {result.get('error')}")
            
    except Exception as e:
        print(f"Error: {e}")


def test_jira_format(environment):
    """Probar el formato que vendría desde Jira"""
    print(f"\n=== Test 3: Formato Jira para ambiente {environment} ===")
    try:
        # Simular lo que Jira enviaría
        payload = {
            "issue": {
                "fields": {
                    "customfield_10001": environment  # Campo personalizado de Jira
                }
            },
            "json_data": SAMPLE_JSON
        }
        
        response = requests.post(
            f"{BASE_URL}/api/replace-environment-from-jira",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        result = response.json()
        
        if result.get('success'):
            print(f"✓ {result.get('message')}")
        else:
            print(f"✗ Error: {result.get('error')}")
            
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("PRUEBAS DE API CONTROL-M")
    print("=" * 60)
    
    # Test 1: Health check
    test_health()
    
    # Test 2: Reemplazar a Q5
    test_replace_environment("Q5")
    
    # Test 3: Reemplazar a Q8
    test_replace_environment("Q8")
    
    # Test 4: Formato Jira
    test_jira_format("Q5")
    
    print("\n" + "=" * 60)
    print("PRUEBAS COMPLETADAS")
    print("=" * 60)


