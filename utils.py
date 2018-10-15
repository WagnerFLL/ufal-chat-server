class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class strings:
    help = 'Preencha o segundo campo com $ \
    um desses comandos: $ \
    [chatlist] lista todos os usuários ativos $ \
    [quit] Sai da aplicação $ \
    [broadcast] Envia mensagem para todos $ \
    [file UserName] envia arquivo $ \
    [UserName] para enviar uma mensagem privada '

    finish = 'ACABOU'
    input_path = bcolors.OKBLUE + bcolors.BOLD + 'Digite o caminho para o arquivo: ' + bcolors.ENDC
    input_dest = bcolors.OKBLUE + bcolors.BOLD + 'Destinatário: ' + bcolors.ENDC
    enter_name = bcolors.OKBLUE + bcolors.BOLD + 'Digite seu nome: ' + bcolors.ENDC
    enter_port = bcolors.OKBLUE + bcolors.BOLD + 'Digite o numero da porta: ' + bcolors.ENDC
    enter_ip = bcolors.OKBLUE + bcolors.BOLD + 'Digite o IP do server: ' + bcolors.ENDC
    finish_download = bcolors.OKBLUE + bcolors.BOLD + "Download finalizado." + bcolors.ENDC
    recv_file = bcolors.OKBLUE + bcolors.BOLD + "Recebendo arquivo." + bcolors.ENDC
    server_down = bcolors.OKBLUE + bcolors.BOLD + "Houve um problema no servidor e voce foi desconectado." + bcolors.ENDC
    cmd = 'COMAND'
    recv_msg_cmd = 'Recebendo arquivo...'
    online = 'Usuarios online:$'
    dir_server = 'serverfile'
    invalid_dest = cmd + 'Destinatario invalido'
    exit = cmd + 'Saindo...'
    welcome = cmd + 'Bem-vindo!!!'

