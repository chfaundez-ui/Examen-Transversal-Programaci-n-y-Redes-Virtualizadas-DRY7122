from ncclient import manager
import time

# Datos de conexión basados en tu topología actual
ROUTER_IP = "192.168.56.101"
USER = "developer"
PASS = "cisco"

# XML Payload con los requerimientos exactos de la Forma A
netconf_payload = """
<config>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname>Faundez-Gomez</hostname>
    <interface>
      <Loopback>
        <name>11</name>
        <ip>
          <address>
            <primary>
              <address>11.11.11.11</address>
              <mask>255.255.255.255</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>
"""

def ejecutar_netconf():
    print(f"[*] Intentando conectar a {ROUTER_IP} por el puerto NETCONF (830)...")
    try:
        # Establecer la sesión SSH para NETCONF
        with manager.connect(
            host=ROUTER_IP,
            port=830,
            username=USER,
            password=PASS,
            hostkey_verify=False
        ) as m:
            print("[+] Conexión NETCONF establecida con éxito.")
            
            # Aplicar la configuración al running-config del dispositivo
            print("[*] Enviando payload XML para cambiar hostname y crear Loopback 11...")
            response = m.edit_config(target='running', config=netconf_payload)
            
            print("\n=== RESPUESTA DEL ROUTER ===")
            print(response)
            print("============================\n")
            print("[+] ¡Procedimiento completado de manera exitosa!")
            
    except Exception as e:
        print(f"[-] Error crítico durante la automatización: {e}")

if __name__ == "__main__":
    ejecutar_netconf()