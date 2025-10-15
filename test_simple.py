#!/usr/bin/env python3
"""
Script simple para probar la API rápidamente
"""
import requests
import json
import time

def test_api():
    print("🚀 Iniciando pruebas de la API Control-M...")
    print("=" * 50)
    
    # Esperar un momento para que la API se inicie
    time.sleep(1)
    
    # Test 1: Health Check
    print("\n📡 Test 1: Health Check")
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Respuesta: {response.json()}")
        print("   ✅ Health Check OK")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test 2: Reemplazar ambiente Q5
    print("\n🔄 Test 2: Reemplazar ambiente Q5")
    try:
        payload = {
            "environment": "Q5",
            "json_data": {
                "GENER_NEXUS-DEMOGRAFICO-CARLOS": {
                    "CC1040P2": {
                        "RunAs": "Q7ABATCH",
                        "Variables": [
                            {"OS400-CURLIB": "Q7AHIFILES"},
                            {"OS400-JOB_OWNER": "Q7ABATCH"}
                        ]
                    }
                }
            }
        }
        
        response = requests.post(
            "http://localhost:5000/api/replace-environment",
            json=payload,
            timeout=10
        )
        
        print(f"   Status: {response.status_code}")
        result = response.json()
        
        if result.get('success'):
            print("   ✅ Éxito!")
            print(f"   Ambiente aplicado: {result.get('environment')}")
            
            # Verificar cambios
            modified = result.get('modified_json', {})
            folder = modified.get('GENER_NEXUS-DEMOGRAFICO-CARLOS', {})
            job = folder.get('CC1040P2', {})
            
            print("   📋 Campos verificados:")
            print(f"     - RunAs: {job.get('RunAs')}")
            
            variables = job.get('Variables', [])
            for var in variables:
                if 'OS400-CURLIB' in var:
                    print(f"     - OS400-CURLIB: {var['OS400-CURLIB']}")
                if 'OS400-JOB_OWNER' in var:
                    print(f"     - OS400-JOB_OWNER: {var['OS400-JOB_OWNER']}")
            
            # Verificar que los cambios son correctos
            runas = job.get('RunAs')
            if runas == 'Q5ABATCH':
                print("   ✅ Q7ABATCH → Q5ABATCH ✓")
            else:
                print(f"   ❌ Error: RunAs debería ser Q5ABATCH, pero es {runas}")
                
        else:
            print(f"   ❌ Error: {result.get('error')}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ¡API funcionando correctamente!")
    print("\n📝 Ahora puedes usar Postman con:")
    print("   URL: http://localhost:5000/api/replace-environment")
    print("   Method: POST")
    print("   Body: JSON con environment y json_data")
    print("\n💡 La API está corriendo en segundo plano.")
    print("   Para detenerla: Ctrl+C en la terminal donde está corriendo")
    
    return True

if __name__ == "__main__":
    test_api()
