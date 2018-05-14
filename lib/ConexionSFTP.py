import paramiko
from datetime import datetime
from .PrintMsg import PrintMsg

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
        PrintMsg.msg("Conectando a %s:%s..." % (self.ip, self.port), time = True, sameline = True)
        try:
            # Create Transport object using supplied method of authentication.
            self.transport = paramiko.Transport((self.ip, self.port))
            self.transport.connect(None, self.username, self.password, None)

            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            PrintMsg.msg("ok", time = True, sameline = False)
            
        except Exception as e:
            PrintMsg.error('Ha ocurrido un error al conectarse al SFTP: %s: %s' % (e.__class__, e))
            if self.sftp is not None:
                self.sftp.close()
            if self.transport is not None:
                self.transport.close()
            pass
    
    def upload_file(self,local_path,remote_path):
        self.connect()

        # Create Transport object using supplied method of authentication.
        PrintMsg.msg("Subiendo desde %s a %s..." % (local_path, remote_path), time = True, sameline = True)
        self.sftp.put(local_path, remote_path)
        self.sftp.close()
        PrintMsg.msg("ok", time = True, sameline = False)
    
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

    uload_file = sftp.upload(local_path,remote_path)


