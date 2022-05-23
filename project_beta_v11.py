#### LEYENDA ####
#! Cosas a corregir
#? Cosas a aclarar
#TODO PENDIENTE DE HACER

#https://python-para-impacientes.blogspot.com/2016/09/dar-color-las-salidas-en-la-consola.html
#ubicado en C:\Users\Marc\Documents\ADAMO\VENV_PYTHON

import telnetlib
import getpass
import time
import os
import os.path as path
import errno
from numpy.lib.nanfunctions import _remove_nan_1d
from numpy.lib.shape_base import _column_stack_dispatcher
import pandas as pd
import numpy as np



def menu():

    tarea = ''


    print ("*** MENU ***")
    print ("1. Extrae informacion de un nodo")
    print("2. QA NODOS: Realiza comprobaciones y extrae info")

    print ("000. Salir")
    
    tarea = input("Introduce una opcion: ") 
    

    return tarea

def introduce_credenciales():

    user = input ('Introduce el usuario: ')
    password = getpass.getpass()

    return user, password

def introduce_ip():

    #TODO la IP 10.100.1.254 es del laboratorio
    IP = input("Introduce la IP de loopback del equipo del que quieres ejecutrar el script: ")
    
    return IP

def telnet(IP):

    error_auth = 'Error: Authentication fail'

    print ("Realizando acceso telnet a: "+IP)
    print (" ")
    tn = telnetlib.Telnet(IP)
    a = tn.read_until(b'Username:')
    print (a)
    tn.write(user.encode('ascii') + b"\n")
    #! De momento usar esta contrasena  
    b = tn.read_until(b'Password:')
    tn.write(password.encode('ascii') + b"\n")
    c = tn.read_until(b'-cs-20>', 5)
    #? Convertimos a String para validar si se autentica correctamente
    d = str(c)
    if error_auth in d:
        print ("Error de auth")
        print (" ")
        print ("El script no puede continuar ya que hay error de autenticacion")
        tn = 'error_salir'
        return tn
    
    elif error_auth not in d:
        print ("ESTOY DENTRO DEL EQUIPO CON IP: " +IP)
        time.sleep(2)
        print (d)
        print ("Eliminando limitación por buffer de la salida...")
        a = tn.write(b'screen-length 0 temporary'+ b"\n")
        print (a)
        

    return tn

def display_clock(tn):

    print (" ")
    print ("Extracción de la hora...")
    print ("Ejecutando 'display clock'...")
    b = tn.read_until(b'cs-20>', 5)
    tn.write(b'display clock'+ b' \n')
    b = tn.read_until(b'cs-20>', 5)

    return b

def parsing_display_clock(a):

    #! De momento usar esta contrasena  

    print (a)
    a = str(a)
    a = (a.split('\\n'))
    #print (a)
    b = ((a)[1])
    b = (b.split('\\r'))
    # b = fecha larga
    b = ((b)[0])
    print (b)
    c = ((a)[2])
    c = (c.split('\\r'))

    # c = dia de la semana
    c = ((c)[0])
    print (c)

    # hostname
    hostname = ((a)[-1])
    hostname = (hostname.split('>'))
    hostname = ((hostname)[0])
    hostname = (hostname.split('<'))
    hostname = ((hostname)[1])


    return hostname,b,c

def parsing_excel_display_clock(a):

    a=str(a)
    a = a.replace('\\r', '')
    b = a.split('<')
    lineas = b[0].split('\\n')
    filas = []

    for line in lineas:
        if 'display clock' not in line:
            line = line.strip()
            filas.append(line)
    
    col_names = ['display clock']
    df = pd.DataFrame(list(zip(filas)), columns = col_names)

    return df

def valoracion_display_clock(a):
    a=str(a)
    a=a.replace('\\r','')
    lineas=a.split('\\n')
    b = lineas[1]
    linea_hora=b.split('+')
    hora_equipo= linea_hora[0]
    hora_actual=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    return hora_equipo, hora_actual

def display_device_manufacture_info(tn):

    print ("Extracción de serial number...")
    print ("Ejecutando 'display device manufacture-info'...")
    b = tn.read_until(b'cs-20>', 5)
    tn.write(b'display device manufacture-info'+ b' \n') 
    b = tn.read_until(b'cs-20>', 5)
    #print (b)


    return b

def parsing_display_device_manufacture_info(a):

    print ("Realizando parsing del serial number: ")
    print (" ")
    a = str(a)
    #print (a)
    a = (a.split('\\n'))
    a = ((a)[3])
    a = (a.split())
    a = ((a)[2])
    print (a)
    

    return a

def parsing_excel_display_device_manufacture_info(a):

    a = str(a)
    a = a.replace('\\r', '')
    lineas = a.split('\\n')
    valores = lineas[3].split()
    col1=[]
    col2=[]
    col3=[]
    col4=[]
    columnas=[col1, col2, col3, col4]

    for i, j in zip(valores, columnas):
        j.append(i)
    
    col_names = ['Slot','Sub','Serial-number','Manu-date']
    
    df = pd.DataFrame(list(zip(col1,col2,col3,col4)), columns = col_names)
    return df

def display_power(tn):
    print ("Extracción de las fuentes de alimentación...")
    print ("Ejecutando 'display power'...")
    b = tn.read_until(b'>', 5)
    tn.write(b'display power'+ b' \n') 
    b = tn.read_until(b'>', 5)
    return b

def parsing_excel_display_power(a):
    a=str(a)
    a=a.replace('\\r','')
    lineas=a.split('\\n')
    col_a=[]
    col_b=[]
    col_c=[]
    col_d=[]
    col_e=[]
    col_f=[]

    b=lineas[4:]
   
    for linea in b:
        if '>' not in linea:
            c=linea.split()
            col_a.append(c[0])
            col_b.append(c[1])
            col_c.append(c[2])
            col_d.append(c[3])
            col_e.append(c[4])
            col_f.append(c[5])
        
    col_names=['Slot', 'PowerID', 'Online', 'Mode','State','Power(W)']
    df = pd.DataFrame(list(zip(col_a,col_b,col_c,col_d, col_e, col_f)), columns = col_names) 
    return df


def valoracion_display_power(a):
    a=str(a)
    a=a.replace('\\r','')
    lineas=a.split('\\n')
    pw1='KO'
    pw2='KO'
    for linea in lineas:
        if 'PWR1' in linea:
            if 'Supply' in linea:
                pw1='OK'
            else:
                pw1='KO'
        if 'PWR2' in linea:
            if 'Supply' in linea:
                pw2='OK'
            else:
                pw2='KO'
    if pw1=='OK' and pw2=='OK':
        QA='OK'
    else:
        QA='KO'

    return QA



def display_interface_description(tn):
    print ("Extracción de las descripciones de las interfaces...")
    print ("Ejecutando 'display interface description'...")
    b = tn.read_until(b'cs-20>', 5)
    tn.write(b'display interface description'+ b' \n') 
    b = tn.read_until(b'cs-20>', 5)
    return b    

def parsing_excel_display_interface_description(a):

    a=str(a)
    a=a.replace('\\r','')
    lineas = a.split('\\n')
    
    try:
        col_a=[]
        col_b=[]
        col_c=[]
        col_d=[]
        count=0
        for linea in lineas:
            if "Interface" in linea:
                break
            else:
                count=count+1
                print("Borro esta linea: ", linea)
        lineas = lineas[count:]
        for linea in lineas:
            print(linea)
            if '>' in linea:
                lineas.remove(linea)
            else:    
                linea=linea.split()
                description=linea[3:]
                col_a.append(linea[0])
                col_b.append(linea[1])
                col_c.append(linea[2])
                col_d.append(' '.join(description))


        col_names=['Interface', 'PHY', 'Protocol', 'Description']
        df = pd.DataFrame(list(zip(col_a,col_b,col_c,col_d)), columns = col_names) 

    except:
        col_names=['display interface description']
        df = pd.DataFrame(list(lineas), columns = col_names)

    return df

def display_ip_routing(tn):

    print ("Extracción de la cantidad de rutas aprendidas...")
    print ("Ejecutando 'display ip routing | i 0.0.0.0/0'...")
    b = tn.read_until(b'cs-20>', 5)
    tn.write(b'display ip routing | i 0.0.0.0/0'+ b' \n') 
    b = tn.read_until(b'cs-20>', 5)
    return b
    
def parsing_display_ip_routing(a):

    print (" ")
    print ("Realizando parsing de las rutas aprendidas...")
    print (" ")
    a = str(a)
    #print (a)
    a = (a.split('\\n'))
    a = ((a)[4])
    #print (a)
    a = (a.split('\\r'))
    #print (a)
    a = ((a)[0])
    print (a)


    return a

def parsing_excel_display_ip_routing(a):

    a=str(a)
    a=a.replace('\\r','')
    lineas=a.split('\\n')
    col_names = ['display ip routing-table | i 0.0.0.0/0']
    for linea in lineas:
        if 'display ip routing' in linea:
            lineas.remove(linea)

    df = pd.DataFrame(list(lineas), columns = col_names) 

    return df

def display_ospf_peer_brief(tn):

    #! De momento usar esta contrasena  

    print ("Extracción de los neighbor de OSPF...")
    print ("Ejecutando 'display ospf peer brief'...")
    b = tn.read_until(b'cs-20>', 5)
    tn.write(b'display ospf peer brief'+ b' \n') 
    b = tn.read_until(b'cs-20>', 5)
    return b

def parsing_display_ospf_peer_brief(a):

    #! De momento usar esta contrasena  
    peering = []
    print ("dentro del parsing dislpay ospf peer brief")
    # print (a)
    a = str(a)
    a = a.split('\\n')
    b = ((a)[-2])
    b = b.split('\\r')
    b = ((b)[0])
    

    print (b)
    print (type(b))

    for peer in a:

        if '0.0.0' in peer: 
            print (peer)
            peering_str = peer+'\n'
            peering.append(peer)

    peering = str(peering)

    return b, peering

def parsing_excel_display_ospf_peer_brief(a):

    a=str(a)
    a=a.replace('\\r','')
    a=a.replace('\\t','')
    lineas=a.split('\\n')
    for linea in lineas:
        if 'display ospf peer brief' in linea:
            lineas.remove(linea)

    col_names = ['display ospf peer brief']
    df = pd.DataFrame(list(lineas), columns = col_names) 

    return df

def valoracion_display_ospf_peer_brief(a):

    a=str(a)
    a=a.replace('\\r','')
    lineas=a.split('\\n')
    peers=0
    for linea in lineas:
        if 'Total Peer' in linea:
            total=linea.strip()
            total=total.split(':')
            peers=int(total[1])
    
    if peers >=1:
        QA='OK'
    else:
        QA='KO'

    return QA


def display_mpls_ldp(tn):

    #! De momento usar esta contrasena  

    print ("Extracción de los sesiones ldp...")
    print ("Ejecutando 'display mpls ldp session'...")
    b = tn.read_until(b'cs-20>', 5)
    tn.write(b'display mpls ldp session'+ b' \n') 
    b = tn.read_until(b'cs-20>', 5)
    print ("Extracción de las interfaces con mpls ldp...")
    tn.write(b'display mpls ldp interface'+ b' \n')
    c = tn.read_until(b'cs-20>', 5)
    return b, c

def parsing_display_mpls_ldp(a,b):

     #! De momento usar esta contrasena  

    #print (b)
    b = str(b)
    b = b.split('\\n')
    for line in b:
        if 'Vlanif' in line:
            print (line)
        
        else: 
            pass

    #print (a)
    print (" ")
    a = str(a)
    a = a.split('\\n')
    #print (a)
    #print (len(a))
    total_session = (a[-3])
    print (total_session)
    
    for line in a:
        if '10.' in line:
            print (line)
        else: 
            pass
    

    return


def parsing_excel_display_mpls_ldp(a, b):
    
    # output_display_mpls_ldp_sesion = a
    # output_display_mpls_ldp_interface = b

    a=str(a)
    a=a.replace('\\r','')
    b=str(b)
    b=b.replace('\\r','')
    lineas_a=a.split('\\n')
    lineas_b=b.split('\\n')
    lineas_c=[]
    lineas_a.append(' ')

    for linea in lineas_a:
        
        
        if "display mpls ldp session" in linea:
            lineas_a.remove(linea)
            #lineas_a.insert(0, 'display mpls ldp session')
        elif "<" in linea:
            lineas_a.remove(linea)
        else:
            lineas_c.append('~')
    
    for linea in lineas_b:
        if "display mpls ldp interface" in linea:
            lineas_b.remove(linea)
            #lineas_b.insert(0,'display mpls ldp interface')
        elif "<" in linea:
            lineas_b.remove(linea)
   
    col_names = ['display mpls ldp session','~', 'display mpls ldp interface']
    df = pd.DataFrame(list(zip(lineas_a,lineas_c,lineas_b)), columns = col_names) 

    return df

def valoracion_display_mpls_ldp(a):
    a=str(a)
    a=a.replace('\\r','')
    lineas=a.split('\\n')
    sessions=0

    for linea in lineas:
        if 'TOTAL' in linea:
            total=linea.split()
            sessions=int(total[1])
    
    if sessions >=4:
        QA='OK'
    else:
        QA='KO'

    return QA


def display_vsi(tn):

    #! De momento usar esta contrasena  

    print ("Extracción de las vsi...")
    print ("Ejecutando 'dis vsi peer-info'...")
    a = tn.read_until(b'cs-20>', 5)
    tn.write(b'dis vsi peer-info'+ b' \n') 
    a = tn.read_until(b'>', 5)
    #print (a)

    return a

def parsing_display_vsi(a):

    a = str(a)
    a = a.split('\\n')
    lista_vsi = []
    for linia in a:
        if 'VSI Name: ' in linia:
            b = linia.split(' ')
            lista_vsi.append(b[2])
        

    return lista_vsi

def parsing_excel_display_vsi(a):
    
    a=str(a)
    a=a.replace('\\r','')
    lineas=a.split('\\n')

    for linea in lineas:

        if "display vsi" in linea:
            lineas.remove(linea)

        if "<" in linea:
            lineas.remove(linea)
       
    col_names = ['display vsi']
    df = pd.DataFrame(list(lineas), columns = col_names) 

    return df

def valoracion_display_vsi(a):
    a=str(a)
    a=a.replace('\\r','')
    lineas=a.split('\\n')

    for linea in lineas:
        if 'MGMT' in linea:
            if 'up' in linea:
                mgmt='OK'
            elif 'down' in linea:
                mgmt='KO'
        elif 'ADAMO-RESIDENCIAL' in linea:
            if 'up' in linea:
                residencial='OK'
            elif 'down' in linea:
                residencial='KO'
    
    if mgmt == 'OK' and residencial == 'OK':
        QA='OK'
    else:
        QA='KO'

    return QA

        

def parsing_excel_display_current_config(a):

    a=str(a)
    a=a.replace('\\r','')
    lineas=a.split('\\n')
    col_names=['display current-configuration']
    df=pd.DataFrame(list(lineas), columns=col_names)
    
    return df



def display_vsi_mac_address(tn,a):

    #! De momento usar esta contrasena  
    mac_address_por_vsi = []
    print (a)
    d = ((a)[0])
    print (d)
    print (type(d))
    print ("Extracción de las mac de las vsi...")
    print ("Ejecutando 'display mac-adress vsi ")
    c = tn.read_until(b'cs-20>', 5)
    var_aux = ''

    for elemento in a:
        #print (elemento)
        tn.write(b'display mac-address vsi '+str(elemento).encode('ascii') + b' | i = \n')
        c = tn.read_until(b'cs-20>', 5)
        #print (c)
        c = str(c)
        c = c.split('\\n')
        #print ("AQUI IMPRIMO C")
        print (c)
        for linea in c: 
            if '=' in linea:
                d = linea.split('=')
                macs_totales_x_vsi = d[1]
        
        print (macs_totales_x_vsi,'en vsi ', elemento)

        #command = ((c)[0])
        #cantidad_mac = ((c)[-3])

        #print ("AQUI IMPRIMO MAC ADDRESS X VSI")
        mac_address_por_vsi.append(elemento+'='+macs_totales_x_vsi)
        print (mac_address_por_vsi)

    return mac_address_por_vsi
 
def parsing_excel_display_vsi_mac_address(a):

    vsis=[]
    total_macs=[]
    comandos=[]

    for elemento in a:
        
        b=elemento.split('=')
        comando=b[0]
        #comando=comando.replace('b\'','')
        #comandos.append(comando+'=')
        total_macs.append(b[1])
        #c=b[0].split('vsi')
        #d=c[1].split('|')
        vsis.append(comando)

    col_names = ['VSI', 'Nº MACs']
    df = pd.DataFrame(list(zip(vsis,total_macs)), columns = col_names)

    return df
    
def display_transceiver(tn):

    print ("Ejecutando 'display transceiver'...")
    b = tn.read_until(b'cs-20>', 5)
    #print (b)
    tn.write(b'display transceiver'+ b' \n')
    b = tn.read_until(b'cs-20>', 5)
    #print (b)

    return b

def parsing_excel_display_transceiver(a):

    col1 = []
    col2 = []
    col3 = []
    col4 = []
    col5 = []
    col6 = []
    col7 = []
    col8 = []
    col9 = []
    col10 = []
    col11 = []
    col12 = []

    columns = [col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12]
    a = str(a)
    a = a.replace('\\r', '')
    lineas = a.split('\\n')

    for i in lineas:
        if "/" in i:
            z = i.split()
            if "absent" in i:
                interface=z[2].replace(',','')
                for col in columns:
                    if col == col1:
                        col.append(interface)
                    else:
                        col.append('-')                    
            else:
                interface = z[0].replace(',','')
                col1.append(z[0])
        
        elif "Transceiver Type" in i:
            z = i.split(":")
            col2.append(z[1])

        elif "Connector Type" in i:
            z = i.split(":")
            col3.append(z[1])

        elif "Wavelength" in i:
            z = i.split(":")
            col4.append(z[1])

        elif "Transfer Distance" in i:
            z = i.split(":")
            col5.append(z[1])

        elif "Digital Diagnostic Monitoring" in i:
            z = i.split(":")
            col6.append(z[1])

        elif "Vendor Name" in i:
            z = i.split(":")
            if len(col6) > len(col7):
                col7.append(z[1])

        elif "Vendor Part Number" in i:
            z = i.split(":")
            col8.append(z[1])

        elif "Ordering Name" in i:
            z = i.split(":")
            col9.append(z[1])

        elif "Manufacture information" in i:
            z = i.split(":")
            col10.append(z[1])

        elif "Manu. Serial Number" in i:
            z = i.split(":")        
            col11.append(z[1])

        elif "Manufacturing Date" in i:
            z = i.split(":")
            col12.append(z[1])

    col_names = ['Interface', 'Transceiver Type', 'Connector Type', 'Wavelength', 'Transfer Distance', 'Digital Diagnostic Monit', 'Vendor Name', 'Vendor Part Number', 'Ordering Name', 'Manufacture information', 'Manu. SN', 'Manufacturing Date']
    df = pd.DataFrame(list(zip(col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12)), columns = col_names)
    return df


def display_transceiver_verbose(tn, a):
    a=str(a)
    a=a.replace('\\r', '')
    lineas = a.split('\\n')
    interfaces=[]
    for linea in lineas:
        if 'transceiver information:' in linea:
            interfaz=linea.split()
            interfaces.append(interfaz[0])
    
    print ("Ejecutando 'display transceiver interface ***** verbose ")
    c = tn.read_until(b'>', 5)

    transceivers_verbose=[]

    for elemento in interfaces:
        tn.write(b'display transceiver interface '+str(elemento).encode('ascii') +b' verbose \n')
        c = tn.read_until(b'>', 5)
        c = str(c)
        c = c.split('\\n')
        transceivers_verbose.append(c)

    return transceivers_verbose


def parsing_excel_display_transceiver_verbose(a):

    col_a=[]

    for elemento in a:
        for fila in elemento:
            if '>' not in fila:
                b=fila.replace('\\r','')
                b=b.replace('b\'','')
                col_a.append(b)

    col_names = ['display transceiver interface ***** verbose']
    df = pd.DataFrame(list(col_a), columns = col_names)

    return df


def display_license(tn):
    print("Extrayendo información de la licencia")
    print ("Ejecutando 'display license'...")
    b = tn.read_until(b'>', 5)
    #print (b)
    tn.write(b'display license'+ b' \n')
    b = tn.read_until(b'>', 5)
    #print (b)
    return b

def parsing_excel_display_license(a):
    a=str(a)
    a=a.replace('\\r','')
    lineas = a.split('\\n')
    
    for linea in lineas:
        if 'display license' in linea:
            lineas.remove(linea)
        elif '>' in linea:
            lineas.remove(linea)
    
    col_names = ['display license']
    df = pd.DataFrame(list(lineas), columns = col_names)

    return df


def valoracion_display_license(tn, a):
    a=str(a)
    a=a.replace('\\r','')
    license='No license'
    lineas_license=a.split('\\n')

    for linea in lineas_license:
        if '100GEUPG' in linea:
            license = 'L-100GEUPG-S67H'
 
    b = tn.read_until(b'>', 5)
    #print (b)
    tn.write(b'display version | i HUAWEI'+ b' \n')
    b = tn.read_until(b'>', 5)

    c=str(b)
    c=c.replace('\\r','')
    lineas_version=c.split('\\n')
    lineas_version=lineas_version[2:]
    version='S672'
    for linea in lineas_version:
        if 'S673' in linea:
            version='S673'
    
    if version == 'S672':
        QA_display_license = 'NO APLICA'
    elif license == 'No license':
        QA_display_license = 'KO'
    elif license == 'L-100GEUPG-S67H':
        QA_display_license = 'OK'
    else:
        QA_display_license = 'KO'


    return QA_display_license



def identifica_parent(tn):
    print("Identificando el switch parent")
    print ("Ejecutando 'display ip routing-table | i 0.0.0.0'...")
    b = tn.read_until(b'>', 5)
    #print (b)
    tn.write(b'display ip routing-table | i 0.0.0.0'+ b' \n')
    b = tn.read_until(b'>', 5)
    #print (b)

    c=str(b)
    c=c.replace('\\r', '')
    lineas=c.split('\\n')
    lineas=lineas[1:]

    for linea in lineas:
        if '0.0.0.0/0' in linea:
            linea_next_hop= linea.split()
            next_hop=linea_next_hop[5]
        elif '>' in linea:
            hostname=linea.replace('<','')
            hostname=hostname.replace('>\'','')


    return next_hop, hostname

def comprueba_vlanif1(tn):
    print("Verificando si la Vlanif1 se ha eliminado")
    print("Ejecutnado 'display current-configuration interface Vlanif 1'")
    b = tn.read_until(b'>', 5)
    #print (b)
    tn.write(b'display current-configuration interface Vlanif 1'+ b' \n')
    b = tn.read_until(b'>', 5)
    #print (b)

    c=str(b)
    c=c.replace('\\r', '')
    lineas=c.split('\\n')
    lineas=lineas[1:]
    vlanif1='KO - Eliminar Vlanif1'
    for linea in lineas:
        if 'Error:' in linea:
            vlanif1='OK'
    return vlanif1




def display_current_configuration(tn):

    print ("Ejecutando display current config...")
    b = tn.read_until(b'cs-20>', 5)
    tn.write(b'dis current-configuration'+ b' \n')
    b = tn.read_until(b'cs-20>', 5)
    return b

def display_cu_interface_sw_parent(tn,output_parent,output_hostname):
    print ("Saliendo del equipo actual...")
    b = tn.read_until(b'>', 5)
    tn.write(b'quit'+ b' \n')

    print ("Accediendo al switch parent")
    print (" ")
    tn2 = telnet(output_parent)
    if tn2 == 'error_salir':
        pass

    else:

        #SOLO A MODO DE PRUEBA CON EL EQUIPO DEL LAB:
        #output_hostname='bcn-oficina-cs-20'
        print ("Extrayendo informacion del equipo...")
        b = tn2.read_until(b'>', 5)
        tn2.write(b'display interface description | i '+str(output_hostname).encode('ascii') +b'\n')
        b = tn2.read_until(b'>', 5)
        b=str(b)
        b=b.replace('\\r','')
        lineas_b=b.split('\\n')
        for linea in lineas_b:
            if 'XGE' in linea:
                c=linea.split()
                interfaz=c[0]
                interfaz=interfaz.replace('XGE','XGi')
            elif '40GE' in linea:
                c=linea.split()
                interfaz=c[0]
            elif '100GE' in linea:
                c=linea.split()
                interfaz=c[0]
            elif 'Eth-Trunk' in linea:
                c=linea.split()
                interfaz=c[0]
                break
        
        d = tn2.read_until(b'>', 5)
        tn2.write(b'display current-configuration interface '+str(interfaz).encode('ascii') +b'\n')
        d = tn2.read_until(b'>', 5) 

        return d

def parsing_excel_display_cu_interface_sw_parent(a):
    a=str(a)
    a=a.replace('\\r','')
    a=a.replace('b\'','')
    lineas = a.split('\\n')
    col_names = ['Configuración puerto en switch parent']
    df = pd.DataFrame(list(lineas), columns = col_names)

    return df

def valoracion_display_cu_interface_sw_parent(a):
    a=str(a)
    lineas = a.split('\\n')
    pvid = 'OK'
    for linea in lineas:
        if 'pvid' in linea:
            pvid='KO - Eliminar port trunk pvid vlan'
    
    return pvid

def data_excel_output_op1(df_transceiver, df_display_clock,df_display_device_manufacture_info,df_display_ip_routing_table,df_display_ospf_peer_brief,df_display_mpls_ldp,df_vsi,df_display_current_config,df_vsi_mac_address,df_display_interface_description):

    print("Abriendo fichero excel para guardar los Dataframes")
    #TODO Anadir mi ruta de W10 y nombre del fichero
    #writer = pd.ExcelWriter ('/home/pedro/scripts/transceivers/prueba2.xlsx')
    if path.exists('C:\\Users\\Marc\\Desktop\\DATA_OUTPUT\\'+hostname+'\\'+'PRE-'+hostname+'.xlsx'):
        writer = pd.ExcelWriter ('C:\\Users\\Marc\\Desktop\\DATA_OUTPUT\\'+hostname+'\\'+'POST-'+hostname+'.xlsx')
    else: 
        writer = pd.ExcelWriter ('C:\\Users\\Marc\\Desktop\\DATA_OUTPUT\\'+hostname+'\\'+'PRE-'+hostname+'.xlsx')

    try:
        df_display_clock.to_excel(writer, sheet_name="Display Clock", index=False)
        df_display_device_manufacture_info.to_excel(writer, sheet_name="dis device man info", index=False)
        df_display_interface_description.to_excel(writer, sheet_name="disp int desc", index=False)
        df_display_ip_routing_table.to_excel(writer, sheet_name="disp ip routing-table", index=False)
        df_display_ospf_peer_brief.to_excel(writer, sheet_name="disp ospf peer brief", index=False)
        df_display_mpls_ldp.to_excel(writer, sheet_name="disp mpls ldp", index=False)
        df_vsi.to_excel(writer, sheet_name="disp vsi", index=False)
        df_vsi_mac_address.to_excel(writer, sheet_name="disp mac-addres vsi", index=False)
        df_transceiver.to_excel(writer, sheet_name="Transceivers", index=False)
        df_display_current_config.to_excel(writer, sheet_name="disp current-conf", index=False)
        writer.save()
        writer.close()
        print("Fichero excel cerrado")

    except:
        print ("ERROR EN data_excel_output_op1")


def data_excel_output_op2(df_display_ospf_peer_brief, df_vsi, df_display_mpls_ldp, df_display_device_manufacture_info, df_display_clock, df_display_power, df_display_interface_description, df_display_license, df_transceiver_verbose, df_pvid_parent, QA_display_ospf_peer_brief, QA_display_mpls_ldp, QA_display_vsi, QA_hora_equipo, QA_hora_actual, QA_display_power, QA_vlanif1, QA_display_license, QA_pvid_parent):
    
    print("Abriendo fichero excel para guardar los Dataframes")
    #TODO Anadir mi ruta de W10 y nombre del fichero
    writer = pd.ExcelWriter ('/home/pedro/scripts/transceivers/prueba_opcion2.xlsx')
    #writer = pd.ExcelWriter ('C:\\Users\\Marc\\Desktop\\DATA_OUTPUT\\'+hostname+'\\'+'QA_'+hostname+'.xlsx')

    try:

        col_a=['COMPROBACIONES SWITCH', 'Revisar los SFPs puestos y la potencia', 'OSFP levantado / Verificar router id', 'LDP levantado con vecinos y remote con SPE', 'Verificar doble fuente de alimentación', 'VSI levantadas para GPON y MGMT', 'Date and time en todos los equipos', 'Hora actual', 'Hora del equipo', 'Authentication por Radius/Local', 'Verificar pvid en el nodo de donde cuelga', 'Verificar S/N', 'Verificar licencia de 100G (en el caso de que sea S6730)', '¿Switch 6730 sin licencia?', 'Eliminar vlanif 1 del nuevo switch', '', 'COMPROBACIONES CABECERA', 'Pedir SN de la cabecera para añadir a Inventory', 'Verificar/ activar hardware', 'Comprobar fuentes de alimentación', 'Upgrade de Cabecera']
        col_b=["-", "display transceiver interface ******* verbose", "display ospf peer brief", "display mpls ldp session", "display power", "display vsi", "display clock", "", "", "-", "undo port trunk pvid vlan", "display device manufacturer-info", "display license", "Procedimiento para activar licencias 100G", "-", "", "-", "-", "show/ set card_all_auth", "show", "Upgrade OLT"]
        col_c=["-", "Revisar hoja 'disp transceiver verbose'", QA_display_ospf_peer_brief, QA_display_mpls_ldp, QA_display_power, QA_display_vsi, "-", QA_hora_actual, QA_hora_equipo, "OK", QA_pvid_parent, "OK", QA_display_license, QA_display_license, QA_vlanif1, "", "Pendiente", "Pendiente", "Pendiente", "Pendiente", "Pendiente"]
        #En la primera hoja guardamos el checklist del QA:            
        col_names = ['Task Name','Information','Status']
        df_checklist = pd.DataFrame(list(zip(col_a,col_b,col_c)), columns = col_names)
        df_checklist.to_excel(writer, sheet_name="Checklist QA", index=False)
        #En las siguientes hojas guardamos el resultado de los comandos:
        df_display_ospf_peer_brief.to_excel(writer, sheet_name="disp ospf peer brief", index=False)
        df_vsi.to_excel(writer, sheet_name="display vsi", index=False)
        df_display_mpls_ldp.to_excel(writer, sheet_name="display mpls ldp", index=False)
        df_display_device_manufacture_info.to_excel(writer, sheet_name="disp device man info", index=False)
        df_display_clock.to_excel(writer, sheet_name="display clock", index=False)
        df_display_power.to_excel(writer, sheet_name="display power", index=False)
        df_display_interface_description.to_excel(writer, sheet_name="disp interface desc", index=False)
        df_display_license.to_excel(writer, sheet_name="display license", index=False)
        df_transceiver_verbose.to_excel(writer, sheet_name="disp transceiver verbose", index=False)
        df_pvid_parent.to_excel(writer, sheet_name="dis cu int sw parent", index=False)

        writer.save()
        writer.close()
        print("Fichero excel cerrado")

    except:
        print ("ERROR EN data_excel_output_op2")
    



def data_output_op1(hostname,fecha_larga,dia,serial_number,routes,total_ospf_peer,peering):
    
    #! De momento usar esta contrasena  
    print ("Dentro dataoutput")

    try: 

        #TODO esta variable debe contener el hostname del equipo al que estamos accediendo

        print ("aqui")
        #! OJO. AQUI HAY QUE CAMBIAR LA URL
        os.mkdir('C:\\Users\\Marc\\Desktop\\DATA_OUTPUT\\'+hostname)
        print ("aqui2")
        with open('C:\\Users\\Marc\\Desktop\\DATA_OUTPUT\\'+hostname+'\\'+hostname+'.txt', 'w') as file:
            file.write(dia+' '+fecha_larga+'\n')
            file.write ('       ***       \n')
            file.write(hostname +': '+serial_number+'\n')
            file.write ('       ***       \n')
            file.write('La tabla de rutas contiene:'+routes+' \n')
            file.write('       ***       \n')
            file.write('El OSPF tiene:'+total_ospf_peer+'\n')
            file.write('Los Peer configurados y su estado: '+peering+'\n')
            file.write('       ***       \n')


            


        
    except OSError as error: 
        print ("He fallado al crear el archivo.")
        #TODO esta pendiente de hacer
        print ("Sin embargo, te voy a mostrar toda la configuracion obtenida por pantalla")





#! Main 
tarea = menu()
if tarea == '1':
    print ("Para realizar esta opcion, voy a necesitar un usuario, contrasenya e IP de loopback")
    user, password = introduce_credenciales()
    IP = introduce_ip()
    print ("Accediendo al equipo")
    print (" ")
    tn = telnet(IP)
    if tn == 'error_salir':
        pass

    
    #if tarea != '1':
        pass

    else:

        print ("Extrayendo informacion del equipo...")
        output_display_clock = display_clock(tn)
        print (" ")
        hostname,fecha_larga,dia = parsing_display_clock(output_display_clock)
        print (" ")
        df_display_clock = parsing_excel_display_clock(output_display_clock)
        print (" ")
        output_display_device_manufacture_info = display_device_manufacture_info(tn)
        print (" ")
        df_display_device_manufacture_info = parsing_excel_display_device_manufacture_info(output_display_device_manufacture_info)
        print (" ")
        output_display_interface_description = display_interface_description(tn)
        print(" ")
        df_display_interface_description = parsing_excel_display_interface_description(output_display_interface_description)
        print(" ")
        output_display_transceiver = display_transceiver(tn)
        print (" ")
        df_display_transceiver = parsing_excel_display_transceiver(output_display_transceiver)
        print (" ")
        serial_number = parsing_display_device_manufacture_info(output_display_device_manufacture_info)
        print (" ")
        output_display_ip_routing = display_ip_routing(tn)
        print (" ")
        df_display_ip_routing_table = parsing_excel_display_ip_routing(output_display_ip_routing)
        routes = parsing_display_ip_routing(output_display_ip_routing)
        print (" ")
        output_display_ospf_peer_brief = display_ospf_peer_brief(tn)
        print (" ")
        total_ospf_peer,peering = parsing_display_ospf_peer_brief(output_display_ospf_peer_brief)
        print (" ")
        df_display_ospf_peer_brief = parsing_excel_display_ospf_peer_brief(output_display_ospf_peer_brief)
        print (" ")
        output_display_mpls_ldp_sesion, output_display_mpls_ldp_interface = display_mpls_ldp(tn)
        print (" ")
        parsing_display_mpls_ldp(output_display_mpls_ldp_sesion, output_display_mpls_ldp_interface)
        print (" ")
        df_display_mpls_ldp = parsing_excel_display_mpls_ldp(output_display_mpls_ldp_sesion, output_display_mpls_ldp_interface)
        print (" ")
        output_display_vsi = display_vsi(tn)
        print (" ")
        lista_vsi = parsing_display_vsi(output_display_vsi)
        print(lista_vsi)
        print (" ")
        df_vsi = parsing_excel_display_vsi(output_display_vsi)
        print (" ")
        output_display_vsi_mac_addess=[]
        output_display_vsi_mac_addess=display_vsi_mac_address(tn, lista_vsi)
        print (" ")
        df_vsi_mac_address=parsing_excel_display_vsi_mac_address(output_display_vsi_mac_addess)
        print (" ")
        data_output_op1(hostname,fecha_larga,dia,serial_number,routes,total_ospf_peer,peering)
        print (" ")
        output_display_current_config = display_current_configuration(tn)
        df_display_current_config = parsing_excel_display_current_config(output_display_current_config)

        # PENDIENTE DE CAMBIAR LA FUNCIÓN DE GUARDADO DEL EXCEL
        data_excel_output_op1(df_display_transceiver, df_display_clock,df_display_device_manufacture_info,df_display_ip_routing_table,df_display_ospf_peer_brief,df_display_mpls_ldp,df_vsi,df_display_current_config,df_vsi_mac_address,df_display_interface_description)


        #print ("AQUI VA LA FUNCION PARA EXCEL")
        #print ("AQUI VA LA FUNCION PARA EXCEL")
elif tarea == '2':
    print("Comprobaciones QA NODOS")
    print ("Para realizar esta opcion, voy a necesitar un usuario, contrasenha e IP de loopback")
    user, password = introduce_credenciales()
    print("Switch")
    IP = introduce_ip()
    print("Cabecera")
    #IP_OLT = introduce_ip()
    print ("Accediendo al equipo")
    print (" ")
    tn = telnet(IP)
    if tn == 'error_salir':
        pass

    
    #if tarea != '1':
        pass

    else:

        '''print ("Extrayendo informacion del equipo...")
        #AQUI EMPIEZO A SACAR LA INFO DEL SWITCH
        #DISPLAY OSPF PEER BRIEF
        output_display_ospf_peer_brief = display_ospf_peer_brief(tn)
        print (" ")
        df_display_ospf_peer_brief = parsing_excel_display_ospf_peer_brief(output_display_ospf_peer_brief)
        print (" ")
        QA_display_ospf_peer_brief = valoracion_display_ospf_peer_brief(output_display_ospf_peer_brief)
        #DISPLAY MPLS LDP SESSION
        output_display_mpls_ldp_sesion, output_display_mpls_ldp_interface = display_mpls_ldp(tn)
        print (" ")
        df_display_mpls_ldp = parsing_excel_display_mpls_ldp(output_display_mpls_ldp_sesion, output_display_mpls_ldp_interface)
        print (" ")
        QA_display_mpls_ldp = valoracion_display_mpls_ldp(output_display_mpls_ldp_sesion)
        #DISPLAY VSI
        output_display_vsi = display_vsi(tn)
        print (" ")
        df_vsi = parsing_excel_display_vsi(output_display_vsi)
        print (" ")
        QA_display_vsi= valoracion_display_vsi(output_display_vsi)
        #DISPLAY DEVICE MANUFACTURE-INFO
        output_display_device_manufacture_info = display_device_manufacture_info(tn)
        print (" ")
        df_display_device_manufacture_info = parsing_excel_display_device_manufacture_info(output_display_device_manufacture_info)
        print (" ")
        #DISPLAY CLOCK
        output_display_clock = display_clock(tn)
        print (" ")
        df_display_clock = parsing_excel_display_clock(output_display_clock)
        print (" ")
        QA_hora_equipo, QA_hora_actual = valoracion_display_clock(output_display_clock)
        #DISPLAY POWER
        output_display_power= display_power(tn)
        print (" ")
        df_display_power= parsing_excel_display_power(output_display_power)
        print(" ")
        QA_display_power= valoracion_display_power(output_display_power)
        print(" ")
        #Verificar que no está configurada la vlanif1
        QA_vlanif1 = comprueba_vlanif1(tn)
        # Display interfaces description
        print (" ")'''
        output_display_interface_description = display_interface_description(tn)
        print(" ")
        df_display_interface_description = parsing_excel_display_interface_description(output_display_interface_description)
        print(df_display_interface_description)
        '''print(" ")    
        #Verificar licencia de 100G (en el caso de que sea S6730)
        output_display_license = display_license(tn)
        print(" ")
        df_display_license = parsing_excel_display_license(output_display_license)
        print(" ")
        QA_display_license = valoracion_display_license(tn, output_display_license)
        # Display transceiver interface ****** verbose
        output_display_transceiver = display_transceiver(tn)
        print (" ")
        output_display_transceiver_verbose = display_transceiver_verbose(tn, output_display_transceiver)
        print (" ")
        #El OUTPUT ESTÁ BIEN, QUEDA HACER EL PARSEO PARA GUARDARLO EN EXCEL
        df_transceiver_verbose = parsing_excel_display_transceiver_verbose(output_display_transceiver_verbose)
        #Verificar pvid en el nodo de donde cuelga
        output_parent, output_hostname = identifica_parent(tn)
        output_pvid_parent = display_cu_interface_sw_parent(tn,output_parent,output_hostname)
        df_pvid_parent= parsing_excel_display_cu_interface_sw_parent(output_pvid_parent)
        QA_pvid_parent = valoracion_display_cu_interface_sw_parent(output_pvid_parent)
        data_excel_output_op2(df_display_ospf_peer_brief, df_vsi, df_display_mpls_ldp, df_display_device_manufacture_info, df_display_clock, df_display_power, df_display_interface_description, df_display_license, df_transceiver_verbose, df_pvid_parent, QA_display_ospf_peer_brief, QA_display_mpls_ldp, QA_display_vsi, QA_hora_equipo, QA_hora_actual, QA_display_power, QA_vlanif1, QA_display_license, QA_pvid_parent)


        #PRINTS DE PRUEBA
        # ESTOS PRINTS HAY QUE METERLOS EN EL EXCEL
        #print(df_display_ospf_peer_brief)
        print('OSFP levantado / Verificar router id: ', QA_display_ospf_peer_brief)
        #print(df_display_mpls_ldp)
        print('LDP levantado con vecinos y remote con SPE: ', QA_display_mpls_ldp)
        #print(df_vsi)
        print('VSI levantadas para GPON y MGMT: ', QA_display_vsi)
        #Display clock
        print('La hora del equipo es: ',QA_hora_equipo)
        print('La hora actual es: ',QA_hora_actual)
        #Sacar el S/N del equipo y marcar OK en el QA
        #print(df_display_power)
        print('Verificar doble fuente de alimentación: ', QA_display_power) 
        print("Interfaz Vlanif 1: ", QA_vlanif1)       
        print("Etiquetado interfaces Switch: revisar descripciones en hoja 'disp int desc'")
        print("Verificar licencia de 100G (en el caso de que sea S6730): ", QA_display_license)
        print("¿Switch 6730 sin licencia?: ",  QA_display_license)
        print("Authentication por Radius/Local: OK (si has podido lanzar el script, el radius funciona correctamente)")
        print("Revisar los SFPs puestos y la potencia: OK (revisar en hoja excel)")
        print("Verificar pvid en el nodo de donde cuelga: ", QA_pvid_parent)'''
        




        ### Una vez guardado el resultado de los comandos en Dataframes y tengamos la valoración de cada comando lo metemos en el excel.





    ################## ESTA PARTE ES PARA COMPROBACIONES EN LA OLT
    '''tn = telnet(IP_OLT)
    if tn == 'error_salir':
        pass

    
    #if tarea != '1':
        pass

    else:

        print ("Extrayendo informacion del equipo...")'''

elif tarea == '000':
    print ("Final de programa")
    print ("Saliendo")