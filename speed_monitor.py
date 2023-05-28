#!/usr/bin/python3
# coding: utf-8

from time import sleep
from os import system
from os.path import exists
from datetime import datetime

import speedtest


def print_header():
    """Exibe o cabeçalho da aplicação"""
    system('clear')
    print('-----------------------------------------------')
    print('  Hello welcome, developed by m0rg4n/b1n/b45h  ')
    print('-----------------------------------------------\n\n')
    print('-----------------------------------------------')
    print('Testando a velocidade da sua internet, aguarde.')
    print('-----------------------------------------------\n\n')

    print('Presione Ctrl+C para parar a aplicação quando desejar finalizar os testes\n\n')

def get_status_connection():
    """Verifica a conexão com a internet
    
    get_status_connection -> bool
    """
    dns_para_pingar = 'www.google.com'

    retorno = system('ping -c 1 ' + dns_para_pingar)

    print_header()

    print('Testando a velocidade...\n')

    if retorno == 0:
        return True
    return False

def get_results():
    """Verifica quais os resultados do teste de velocidade

    get_results() -> dict
    """
    ping = 0
    download = 0
    upload = 0

    if get_status_connection():
        try:
            s = speedtest.Speedtest()
            s.get_best_server()
            s.download()
            s.upload()

            ping = s.results.dict()['ping']
            download = s.results.dict()['download'] / 1000000
            upload = s.results.dict()['upload'] / 1000000
        except:
            ping = 0
            download = 0
            upload = 0
    else:
        ping = 0
        download = 0
        upload = 0

    results = {'ping': ping, 'download': download, 'upload': upload}

    return results

def print_results(results):
    """Exibe os resultados do teste de velocidade"""
    ping = results['ping']
    download = results['download']
    upload = results['upload']

    print_header()

    if results['download']:
        print('---------------Resultados----------------')
        print('|-> Ping: %d' %ping)
        print('|-> Download: %.2f' %download)
        print('|-> Upload: %.2f' %upload)
        print('-----------------------------------------\n\n\n')
    else:
        print('*** Sem conexão com a internet ***\n\n\n')



def write_file(results):
    """Escreve os resultados do teste de velocidade em um arquivo

    Keywords arguments:
    results -- dicionario com os resultados do teste de velocidade
    """
    ping = results['ping']
    download = results['download']
    upload = results['upload']

    name_archive = '/home/testes.txt'
    flag_arquivo = 'a'

    date_time = datetime.now()
    text_date_time = date_time.strftime('%d/%m/%Y %H:%M:%S')

    if not exists(name_archive):
        flag_arquivo = 'w'
        
        with open(name_archive, flag_arquivo) as writer:
            writer.write('Data Hora|Ping|Download|Upload\n')

        flag_arquivo = 'a'

    with open(name_archive, flag_arquivo) as writer:
        writer.write('%s|%d|%.2f|%.2f\n' %(text_date_time , ping, download, upload))

while True:
    try:
        time_sleep = 60

        print_header()

        results = get_results()

        print_results(results)

        write_file(results)

        for timer in range(time_sleep, 0, -1):
            print_results(results)

            print('Próximo teste padrão será realizado em %d segundos!' %timer)

            sleep(1)

    except KeyboardInterrupt:
        print_header()

        print('Ctrl+C presionado... aplicação sendo encerrada')
        print('Obrigado por utilizar a aplicação, até a breve!')
        exit(1)
