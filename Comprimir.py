import zipfile
import os
import os.path
from dateutil.parser import parse
import argparse
import sys
import lib.ConexionSFTP as ConexionSFTP
import lib.PrintMsg as PrintMsg

#Clase que cuya entrada son un directorio "path", un nombre de un archivo zip (si no existe, lo crea), 
#una lista de archivos o carpetas a comprimir y una variable que indica si en el directorio tenemos 
# archivos o carpetas, format = {'archivos','carpetas'}. Esta clase comprime en el archivo zip indicado, 
# la lista de archivos/carpetas de entrada. La compresion se realiza al construir un objeto de esta clase.
#Ejemplo de uso: 
#name = 'archivo.zip'
#path = 'C:\\Users\\WDNA\\repository'
#archivos = ['carpeta1','carpeta2']
#format = 'carpetas'
# ArchivoZip = ArchivoComp(name, path, archivos,format) 
class ArchivoComp:
    
    def __init__(self, name = 'archivo.zip', path = '~', archivos = [],format = 'archivos'):
        self.name = name
        self.archivos = archivos
        self.archivoZip = None 
        
        os.chdir(path) #Seleccionamos 'path' como el directorio en el que vamos a trabajar.
        
        self.archivoZip = zipfile.ZipFile(name,'w',zipfile.ZIP_DEFLATED)
        if(format == 'archivos'):
            PrintMsg.msg("Comprimiendo ficheros...", time = True, sameline = True)
            self.zipArchivos(self.archivos) 
        else:
            PrintMsg.msg("Comprimiendo carpetas...", time = True, sameline = True)
            self.zipDir(self.archivos)
        
        PrintMsg.msg("ok", time = True, sameline = False)

    #Funcion para comprimir una lista de carpetas dada una lista con sus nombres "carpetas" 
    # y un archivo .zip donde pueda guardarlas.
    def zipDir(self, carpetas):
        for carpeta in carpetas:
            for root, dirs, files in os.walk(carpeta):
                for file in files:
                     self.archivoZip.write(os.path.join(root, file))
        
        self.archivoZip.close()

    #Funcion que comprime una lista de archivos dada una lista con sus nombres "archivos" 
    # y un archivo .zip donde pueda guardarlos.
    def zipArchivos(self, archivos):
        for archivo in archivos:
            self.archivoZip.write(archivo) 
        
        self.archivoZip.close() #Anyadimos al .zip los archivos que se encuentran en la lista self_archivos.



#Clase que lee los ficheros/carpetas de un directorio y guarda aquellos cuya fecha 
# #indicada en su nombre sea inferior a limDateStr.
# Ejemplo: 
# path = 'C:\\Users\\WDNA\\repository'
# limdateStr = '20180224'
# FicherosFiltrados = DateArray(path, limdateStr).
# La lista de nombres de ficheros/carpetas la devuelve el comando: FicherosFiltrados.getListaNames()
class DateArray:
    def __init__(self, path = '~',limDateStr = '20180224', format = 'archivos'):
        self.listNames = [] #Lista donde guardaremos los nombres de los ficheros que vamos a comprimir.
        try:
            if(format == 'archivos'):
                PrintMsg.msg("Filtrando ficheros...", time = True, sameline = True)  
            else:
                PrintMsg.msg("Filtrando carpetas...", time = True, sameline = True)

            
            lim_date = parse(limDateStr) #Pasamos el string que contiene la fecha limite a formato fecha.
            strDate = []
            listStr = os.listdir(path)

            #Buscamos los ficheros/carpetas que queremos comprimir:
            for dir in listStr:
                strDate = dir.split('_')[0] #Guardamos la fecha del fichero/carpeta.

                date = parse(strDate) #Pasamos el string que contiene la fecha al formato fecha.    
                if(date <= lim_date):
                    self.listNames.append(dir) #Si la fecha del fichero/carpeta es inferior
                                                #a la fecha limite, guardamos el nombre de dich@ fichero/carpeta.
            PrintMsg.msg("ok", time = True, sameline = False)
        except Exception as e:
            PrintMsg.msg("ok", time = True, sameline = False)
            pass

        
    def getListaNames(self):
        return self.listNames

#Clase que borra los ficheros/carpetas que se encuentran en el path localPath 
#y cuyo nombre se pasa en el array "archivos".
class Borrar:
    def __init__(self,localPath = '.', archivos = [], format = 'archivos', nameZip = 'archivo.zip'):
        self.localPath = localPath
        self.archivos = archivos
        self.nameZip = nameZip
        self.listNames = [] #Lista donde guardaremos los nombres de los ficheros que vamos a comprimir.

        os.chdir(self.localPath)
        if(format == 'archivos'):
            PrintMsg.msg("Borrando ficheros...", time = True, sameline = True)
            self.Ficheros()  
        else:
            PrintMsg.msg("Borrando carpetas...", time = True, sameline = True)
            self.Carpetas()

        PrintMsg.msg("ok", time = True, sameline = True)
    
    def Ficheros(self):
        for archivo in self.archivos:
            os.remove(archivo)
        os.remove(self.nameZip) #Eliminamos el archivo .zip que hemos creado.

    def Carpetas(self):
        listStr = os.listdir(self.localPath,)
        for carpeta in self.archivos:
            listaArchivosCarpeta = os.listdir(carpeta)
            dirsArchivosCarpeta = []

            for archivo in listaArchivosCarpeta:
                dirsArchivosCarpeta.append(os.path.join(carpeta,archivo))

            for archivo in dirsArchivosCarpeta:
                os.remove(archivo)
            os.removedirs(carpeta)
        os.remove(self.nameZip) #Eliminamos el archivo .zip que hemos creado.

def main(args):
    if args.c or args.d:
        # Parametros
        parameters = { 
            'name': sys.argv[2],
            'localpath': sys.argv[3], 
            'remotepath': sys.argv[4],
            'format': sys.argv[5],
            'lim_date': sys.argv[6],
            'user': sys.argv[7],
            'password': sys.argv[8],
            'ip': sys.argv[9]
            }  

        #Obtenemos los nombres de los ficheros o carpetas a comprimir:
        archivos = DateArray(parameters['localpath'],parameters['lim_date'],parameters['format'])
        names_array = archivos.getListaNames() 
        
        #Comprimimos los ficheros/carpetas indicad@s con un fichero .zip llamado "name":
        ArchivoComp(name = parameters['name'], path = parameters['localpath'], archivos = names_array, format = parameters['format'])


        local_path = os.path.join(parameters['localpath'], parameters['name'])
        remote_path = os.path.join(parameters['remotepath'], parameters['name'])


        # user = 'meteoclimp'
        # password = 'meteoclimp'
        # ip = '217.160.19.164'

        user = parameters['user']
        password = parameters['password']
        ip = parameters['ip']

        # Conexion SFTP
        sftp = ConexionSFTP.Sftp(
            ip = ip, 
            username = user, 
            password = password
            )

        #Subida del archivo comprimido al servidor.
        upload_file = sftp.upload_file(local_path,remote_path)
        
        #Borrar archivos/carpetas locales que se han subido al servidor.
        if args.d:
            Borrar(localPath = parameters['localpath'],archivos = names_array, format = parameters['format'],nameZip = parameters['name'] )


if __name__ == "__main__":  
    parsear = argparse.ArgumentParser(
        description = 'Script de compresion de archivos/carpetas' 
        'filtrados por una fecha limite escrita en el nombre de cada archivo/carpeta',
        epilog = '')

    parsear.add_argument('-c', nargs=8, help='Filtrar archivos/carpetas (segun se indique en la entrada) de un directorio indicado cuyos nombres tengan una \
    fecha inferior a la fecha limite de entrada y despues compimir estos archivos/carpetas en un archivo .zip para enviarlo a un servidor:'
                                             'script.py -c <NOMBRE.ZIP> <PATH LOCAL> <PATH EN EL SERVIDOR> <FORMATO> <FECHA LIMITE> <USER> <PASWWORD> <IP>')
    parsear.add_argument('-d', nargs=8, help='Filtrar archivos/carpetas (segun se indique en la entrada) de un directorio indicado cuyos nombres tengan una \
    fecha inferior a la fecha limite de entrada y despues compimir estos archivos/carpetas en un archivo .zip para enviarlo a un servidor. posteriormente se BORRA EL ARCHIVO .ZIP:'
                                             'script.py -c <NOMBRE.ZIP> <PATH LOCAL> <PATH EN EL SERVIDOR> <FORMATO> <FECHA LIMITE> <USER> <PASWWORD> <IP>')

    args = parsear.parse_args()

    main(args)