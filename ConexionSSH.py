import paramiko
from datetime import datetime

# Conexion SSH
class Ssh:
    def __init__(self, ip = None, username = None, password = None):
        # Datos usuario/host
        self.ip = ip
        self.username = username
        self.password = password
        
        # SSH
        self.connection = None

    def get_username(self):
        return self.username

    def get_ip(self):
        return self.ip

    def connect(self):
        self.connection = paramiko.SSHClient()
        self.connection.load_system_host_keys()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            self.connection.connect(self.ip, username = self.username, password = self.password)
        except (paramiko.BadHostKeyException, e):
            PrintMsg.error("El servidor no acepta el tipo de autentificacion")
        except (paramiko.AuthenticationException, e):
            PrintMsg.error("Error al autentificar")
        except (paramiko.SSHException, e):
            PrintMsg.error("Fallo en el protocolo SSH")
        finally:
            if self.connection:
                self.connection.close()


# Conexion SFTP
class Sftp:
    def __init__(self, ip = None, username = None, password = None):
        # Datos usuario/host
        self.ip = ip
        self.username = username
        self.password = password
        
        # SFTP
        self.port = 22

        self.sftp = None
        self.transport = None
    
    def get_username(self):
        return self.username

    def get_ip(self):
        return self.ip

    def get_port(self):
        return self.port
    
    def connect(self):
        try:
            # Create Transport object using supplied method of authentication.
            self.transport = paramiko.Transport((self.ip, self.port))
            self.transport.connect(None, self.username, self.password, None)

            self.sftp = paramiko.SFTPClient.from_transport(self.transport)

        except Exception as e:
            PrintMsg.error('Ha ocurrido un error al conectarse al SFTP: %s: %s' % (e.__class__, e))
            if self.sftp is not None:
                self.sftp.close()
            if self.transport is not None:
                self.transport.close()
    #-------------------------------------------------------------------------------------------------------------------------------------
    #AGREGADO POR ADAM
            pass
    def upload(self,local_path,remote_path):
        try:
            # Create Transport object using supplied method of authentication.
            self.transport = paramiko.Transport((self.ip, self.port))
            self.transport.connect(None, self.username, self.password, None)

            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            self.sftp.put(local_path, remote_path)
            self.sftp.close()

        except Exception as e:
            PrintMsg.error('Ha ocurrido un error al conectarse al SFTP: %s: %s' % (e.__class__, e))
            if self.sftp is not None:
                self.sftp.close()
            if self.transport is not None:
                self.transport.close()
            pass
    #-------------------------------------------------------------------------------------------------------------------------------------

    def command_listfiles(self, directory = None, detailed = False, output = False):
        if not directory:
            directory = '.'
        
        if detailed:
            return self.command_listfiles_detailed(directory, output)
        else:
            return self.sftp.listdir(directory)

    def command_listfiles_detailed(self, directory = None, output = False):
        if not directory:
            directory = '.'
        
        dataFiles = self.sftp.listdir_attr(directory)
        
        listFiles = []
        for dataFile in dataFiles:
            listFiles.append({ 
                'filename': dataFile.filename,
                'date':  str(datetime.fromtimestamp(dataFile.st_mtime))
                })
        
        if output:
            for dataFile in dataFiles:
                print(dataFile)
        
        return listFiles


class PrintMsg:
    @staticmethod
    def get_color(selectColor):
        color = {
            'HEADER': '\033[95m',
            'OKBLUE': '\033[94m',
            'OKGREEN': '\033[92m',
            'WARNING': '\033[93m',
            'FAIL': '\033[91m',
            'ENDC': '\033[0m',
            'BOLD': '\033[1m',
            'UNDERLINE': '\033[4m'
        }

        return color[selectColor]
    
    @staticmethod
    def msg(msg, time = False, sameline = False):
        # Add hora
        addHour = ""
        if time:
            addHour = datetime.now().strftime('%Y-%m-%d %H:%M:%S - ')

        if sameline:
            print ('%s %s' % (addHour, msg))
        else:
            print ('%s %s' % (addHour, msg))

    @staticmethod
    def error(msg, time = False, sameline = False):
        updateMsg = PrintMsg.get_color('FAIL') + msg + PrintMsg.get_color('ENDC') 
        
        PrintMsg.msg(updateMsg, time = time, sameline = sameline)

    @staticmethod
    def ok(msg, time = False, sameline = False):
        updateMsg = PrintMsg.get_color('OKGREEN') + msg + PrintMsg.get_color('ENDC')
        
        PrintMsg.msg(updateMsg, time = time, sameline = sameline)

if __name__ == "__main__":
    user = 'meteoclimp'
    password = 'meteoclimp'
    ip = '217.160.19.164'
    # Conexion SFTP
    sftp = Sftp(
        ip = ip, 
        username = user, 
        password = password
        )

    sftp.connect()

    # Obtenemos ficheros del path
    path = "/home/meteoclimp"
    local_path = 'C:/Users/WDNA/Documents/Archivo_prueba_servidor.txt'
    remote_path = '/home/meteoclimp/Archivo_prueba_servidor.txt'

    # Listamos ficheros del path
    #filesNew = sftp.command_listfiles(path, detailed = True, output = True)
    uload_file = sftp.upload(local_path,remote_path)

    # Anyadimos IP Servidor y NE a los datos de los ficheros
    # lenghtFiles = len(filesNew)
    # filesNewExtend = []
    # for i in filesNew:
    #     i['ip'] = dataServer['IP_OSS']
    #     i['ne'] = ne

    #     filesNewExtend.append(i)

    # # Anyadimos a la array final
    # files += filesNewExtend




    # parsear = argparse.ArgumentParser(
    #     description = 'Script de compresión de archivos/carpetas' 
    #     'filtrados por una fecha límite escrita en el nombre de cada archivo/carpeta',
    #     epilog = '')

    # parsear.add_argument('-c', nargs=4, help='Crear backup de tablas de la base de datos. Si se quiere la maquina local poner en <IP> "localhost": '
    #                                          'script.py -c <NOMBRE.ZIP> <PATH> <FORMATO> <FECHA LIMITE>')

    # args = parsear.parse_args()

    # main(args)


