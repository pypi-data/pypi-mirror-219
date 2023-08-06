'''
Script desenvolvido para a geração do relatório de ensalamento e do acompanhamento de vagas, gerando
análise a respeito das vagas e das capacidades das salas. O script utiliza o XML Unificado do ASC (COA), o re-
latório de capacidade (COA) e o excel de Carga Horária por Turma/Disciplina (Prime). Foi desenvolvido uma tela
para a seleção dos arquivos utilizados. O código é utilizado atualmente pela equipe da CIA


Desenvolvido por Matheus Rosa e Fernando Dias
'''

import time
import Sugestao
import Unificar_XML
import numpy as np
import pandas
import xml.etree.ElementTree as ElementTree
import json
import warnings
import datetime
from unidecode import unidecode
import xlsxwriter
import pytz
import PySimpleGUI as psg

contador = 0


# Função recebe o resultado do cálculo entre vagas - matriculados e gera um análise
def analisar_diferenca(diferenca):
    if diferenca > 0:
        return "Vagas Disponíveis"
    elif diferenca == 0:
        return "Não há vagas"
    elif diferenca < 0:
        return "Vagas excedidas"
    else:
        return ""


# Função recebe matriculados,  diferença entre matriculados - capacidade para gerar uma análise das capacidades
def analisar_capacidade(matriculados, diferenca, capacidade, sala):
    if diferenca > 0:
        return "Capacidade disponível"
    elif sala == "Sem sala":
        return "Sem sala"
    elif matriculados > 0 and diferenca == 0:
        return "Sala lotada"
    elif matriculados == 0 and diferenca == 0:
        return "Indisponível"
    elif capacidade == 0:
        return "Sem Capacidade"
    elif diferenca < 0:
        return "Capacidade excedida"
    else:
        return ""


# Função recebe o XML Unificado e dois dicionários um de escolas e outro de turmas fictícias
def armazenaDadosAscXml(file_name_asc_xml, file_json_turmasfic, contador, file_json_escolas, f):
    tree_xml = ElementTree.parse(file_name_asc_xml)
    root = tree_xml.getroot()
    erro_log_turma = ""
    erro_log_sala = ""

    # converte period
    # retorna starttime/endtime

    # Função para converter o em período (horário) os códigos recebidos do XML
    def convertePeriod(period):
        if period == "1":
            valor = "07:05-07:50"
        elif period == "2":
            valor = "07:50-08:35"
        elif period == "3":
            valor = "08:35-09:20"
        elif period == "4":
            valor = "09:40-10:25"
        elif period == "5":
            valor = "10:25-11:10"
        elif period == "6":
            valor = "11:10-11:55"
        elif period == "7":
            valor = "11:55-12:40"
        elif period == "8":
            valor = "12:40-13:25"
        elif period == "9":
            valor = "13:25-14:10"
        elif period == "10":
            valor = "14:10-14:55"
        elif period == "11":
            valor = "15:15-16:00"
        elif period == "12":
            valor = "16:00-16:45"
        elif period == "13":
            valor = "16:45-17:30"
        elif period == "14":
            valor = "17:30-18:15"
        elif period == "15":
            valor = "18:15-19:00"
        elif period == "16":
            valor = "19:00-19:45"
        elif period == "17":
            valor = "19:45-20:30"
        elif period == "18":
            valor = "20:45-21:30"
        elif period == "19":
            valor = "21:30-22:15"
        elif period == "20":
            valor = "22:15-23:00"
        else:
            valor = ""

        return valor

    # Função para converter em dias da semana os códigos recebidos do XML
    def convertDays(day):
        if day == "1111111" or day == "111111":
            valor = "Cada dia"

        elif day == "1000000" or day == "100000":
            valor = "Segunda-feira"

        elif day == "0100000" or day == "010000":
            valor = "Terça-feira"

        elif day == "0010000" or day == "001000":
            valor = "Quarta-feira"

        elif day == "0001000" or day == "000100":
            valor = "Quinta-feira"

        elif day == "0000100" or day == "000010":
            valor = "Sexta-feira"

        elif day == "0000010" or day == "000001":
            valor = "Sábado"

        elif day == "0000001":
            valor = "Horario Flutuante"
        else:
            valor = ""

        return valor

    # armazenar a id como key e o name como value
    dict_subject = {}
    for subject in root.iter("subject"):
        # parametros
        id = subject.get('id')
        name = subject.get('name')

        dict_subject[id] = name

    # armazenar a id como key e o name,short como value
    dict_classrooms = {}
    for classrooms in root.iter("classroom"):
        # parametros
        id = classrooms.get('id')
        name = classrooms.get('name')
        short = classrooms.get('short')

        dict_classrooms[id] = name, short

    # armazenar a id como key e o name,short como value
    dict_class = {}
    for classes in root.iter("class"):
        # parametros
        id = classes.get('id')
        name = classes.get('name')
        short = classes.get('short')

        turmas_fic = dict(file_json_turmasfic)

        if name.__contains__('Engenharia;') or name.__contains__('Multicom'):
            cr_curso = short.split(";")[5]
            periodo = short.split(";")[2]
            tipo = short.split(";")[3]
            turno = short.split(";")[4]

            chave_turma_fic = f"{cr_curso}|{periodo}"

            if chave_turma_fic in turmas_fic.keys():
                name = turmas_fic[chave_turma_fic]

                new_name = f"{name};{periodo};{tipo};{turno}"
                name = new_name
            else:
                contador += 1
                f.write(f'#{contador} Aviso[Info]: erro ao converter a multicom name ={name} , short={short}''\n')
                continue

        dict_class[id] = name, short

    # armazenar a id como key e o period,days como value
    # para puxar a id da lesson e saber qual o horario e dia daquela aula
    dict_cards = {}
    for cards in root.iter("card"):
        # parametros
        id = str(cards.get('lessonid'))
        period = cards.get('period')
        day = cards.get('days')

        valor = f"({convertePeriod(period)}/{convertDays(day)})"
        try:
            valor_dict = dict_cards[id]

            if valor_dict.__contains__(valor):
                continue
            else:
                dict_cards[id] += valor
        except:

            dict_cards[id] = valor

    dict_retorna_group = {}
    for groups in root.iter("group"):
        id = groups.get('id')
        name = groups.get('name')

        dict_retorna_group[id] = name

    valores = []
    for lessons in root.iter("lesson"):
        id = lessons.get('id')
        subjectid = lessons.get('subjectid')
        groupid = lessons.get('groupids')
        classid = lessons.get('classids')
        classroomsid = lessons.get('classroomids')

        name_subject = dict_subject[subjectid]

        cr_curso = name_subject.split(';')[0]

        quantidade_turma = classid.count(',')

        posicao_turma = 0

        if quantidade_turma == 0:
            quantidade_turma = 1
        else:
            quantidade_turma += 1

        for i in range(0, quantidade_turma):
            try:

                turma = str(dict_class[classid.split(',')[posicao_turma]]).replace(',', '/')
            except:
                contador += 1
                erro_log_turma += f'#{contador} Aviso[Ação]; Turma nao identificada na aula: {id}\n'
                continue

            try:
                periodo = turma.split('/')[0].split(';')[1]
            except:
                contador += 1
                erro_log_turma += f'#{contador} Aviso[Ação]; Erro no formato do nome da turma: aula= {id},  turma= {turma} sala= {classroomsid} \n'
                continue

            quantidade = classroomsid.count(',')
            posicao_sala = 0

            if quantidade == 0:
                quantidade = 1
            else:
                quantidade += 1

            for i in range(0, quantidade):
                try:

                    # if classroomsid == "":
                    #   continue

                    sala = str(dict_classrooms[classroomsid.split(',')[posicao_sala]]).split(',')[0]
                    abrev_sala = str(dict_classrooms[classroomsid.split(',')[posicao_sala]]).split(',')[1]
                except KeyError:
                    sala = "Sem sala"
                    abrev_sala = "-"
                    contador += 1
                    f.write(
                        f'#{contador} Aviso[Info]; XML lessonid = {id} nao teve a classroom encontrada, foi definida como sem sala''\n')

                try:
                    dia_hora = dict_cards[id]

                except KeyError:
                    dia_hora = "-/Flutuante"
                    f.write(
                        f'#{contador} Aviso[Info]; XML lessonid = {id} nao teve o card encontrado, foi definida como Flutuante''\n')

                try:
                    group = dict_retorna_group[groupid.split(',')[0]]
                except:
                    f.write('erro no group da lesson' + id + '\n')
                    group = '---'

                quantidade_dia = dia_hora.count('/')

                if group.replace(' ', '').upper() == 'TURMACOMPLETA' or group.replace(' ', '').upper() == "ENTIRECLASS":
                    group = '  '

                try:
                    quantidade_hora = dia_hora.count('/')
                    for posicao in range(0, quantidade_dia + 1):
                        dia = dia_hora.split(')')[posicao].split('/')[1]

                        for posicao_hora in range(0, quantidade_hora):
                            hora_inicio = dia_hora.split(')')[posicao_hora].split('/')[0].split('-')[0].replace('(', '')
                            # dia = dia_hora.split(')')[posicao].split('/')[1]

                            turma = turma.replace('Manhã e Tarde', 'I')
                            valor = f"{cr_curso}|{periodo}|{turma}|{sala}|{abrev_sala}|{dia_hora}|{name_subject}|{dia}|{group}|{hora_inicio}"
                            valores.append(valor)
                except:
                    posicao_sala += 1
                    continue
                posicao_sala += 1

            posicao_turma += 1

    f.write(erro_log_turma)
    f.write('\n\n')
    return valores


# Função recebe o excel de capacidade e retorna apenas a abrev da sala e a sua capacidade
def armazenaDadosCapacidade(file_name_capacidade, contador, f):
    # armazena os valores das colunas importantes
    todos_valores = []

    df = pandas.read_excel(file_name_capacidade, sheet_name="BASE DE CAPACIDADES CWB", header=2)

    posicao = 0
    teste = df.columns
    for dados in df.iterrows():
        abrev_sala = df['CÓD. ASC'][posicao].replace(' ', '')
        capacidade = df['CAPACIDADE'][posicao]

        posicao += 1

        todos_valores.append(f"{abrev_sala}|{capacidade}")

    return todos_valores


def armazenaDadosTurmaDisciplina(file_name_turma_disciplina, file_json_sigla, contador, f):
    siglas = dict(file_json_sigla)

    def converteSigla(turma):
        if turma in siglas.keys():
            return siglas[turma]
        else:
            return turma

    # armazena os valores das colunas importantes
    todos_valores = []

    df = pandas.read_excel(file_name_turma_disciplina)
    posicao = 0
    df['Divisão'] = df['Divisão'].fillna('Teórico')
    for i in df.iterrows():

        cortes = df['Tem Corte'][posicao]
        if cortes == 'Não':
            posicao += 1
            continue

        # valores key
        df['CR Curso'] = df['CR Curso'].fillna(0)
        cr_curso = int(df['CR Curso'][posicao])
        nome_curso = df['Curso'][posicao]
        periodo = df['Período'][posicao]

        nome_turma = df['Turma'][posicao]
        nome_turma = converteSigla(nome_turma)

        quantidade_nome_turma = nome_turma.count('-')
        if quantidade_nome_turma != 3:
            turno = df["Turno"][posicao][0]

            try:
                nome_parte_um = nome_turma.split('-')[0].replace(" ", "")
                nome_parte_dois = nome_turma.split('-')[1].replace(" ", "")
                nome_parte_tres = nome_turma.split('-')[2].replace(" ", "")

                nome_turma = f'{nome_parte_um} - {nome_parte_dois} - {turno} -{nome_parte_tres}'

            except:
                contador += 1
                f.write(f'#{contador} Aviso[Ação]; a turma = {nome_turma} esta no formato incorreto''\n')

        # valores nao utilizados como key
        professor = df['Professor'][posicao]
        nome_disciplina = df['Disciplina'][posicao]
        id_disciplina = df['ID'][posicao]
        divisao = df['Divisão'][posicao]
        dia = df['Data da Semana'][posicao]
        hora_inicio = df['Horário de Início'][posicao]
        hora_final = df['Horário de Término'][posicao]
        agrupamento = df['Agrupamento'][posicao]
        turno = df['Turno'][posicao]
        qtd_alunos = df['Qtde de Alunos Matriculados'][posicao]
        qtd_vagas = df['Nr Vagas Cadastradas'][posicao]
        posicao += 1

        if divisao == ' ' or divisao == '  ' or divisao == '   ' or divisao == 'Teórico':
            divisao = '  '

        valores = f"{cr_curso}|{nome_curso}|{periodo}|{nome_turma}|{nome_disciplina}|{id_disciplina}|{divisao}|{dia}|{hora_inicio}|{hora_final}|" \
                  f"{agrupamento}|{turno}|{qtd_alunos}|{qtd_vagas}|{professor}"

        todos_valores.append(valores)

    return todos_valores


def gerarRelatorio(file_name_turma_disciplina, file_name_asc_xml, file_json_sigla, file_name_capacidade,
                   file_json_turmasfic, contador, file_json_escolas, file_json_tipos, f, file_name):
    siglas = dict(file_json_sigla)
    escolas = dict(file_json_escolas)
    tipos = dict(file_json_tipos)
    log_sala = {}

    warnings.simplefilter(action='ignore', category=UserWarning)

    def gerarTipo(tipo):
        if tipo in tipos.keys():
            return tipos[tipo]
        else:
            return tipo

    def converteSigla(turma):
        if turma in siglas.keys():
            return siglas[turma]
        else:
            return turma

    def geraEscola(cr_curso):
        if cr_curso in escolas.keys():
            return escolas[cr_curso]
        else:
            return ' '

    # armazenando dados
    array_turmas_disciplinas = armazenaDadosTurmaDisciplina(file_name_turma_disciplina, file_json_sigla, contador, f)

    array_asc_xml = armazenaDadosAscXml(file_name_asc_xml, file_json_turmasfic, contador, file_json_escolas, f)

    array_capacidade = armazenaDadosCapacidade(file_name_capacidade, contador, f)

    dict_capacidade = {}

    for i in array_capacidade:
        abrev_sala = i.split('|')[0]
        capacidade = i.split('|')[1]

        dict_capacidade[abrev_sala] = str(capacidade)

    dict_valores = {}
    dict_retorna_cr_disciplina = {}
    retorna_horario_inicio = {}
    horario_repetido = []
    for i in array_turmas_disciplinas:
        # valores chave
        cr_curso_aluno = i.split('|')[0]
        periodo = i.split('|')[2]
        nome_turma_final = i.split('|')[3].replace('- 2022/1', '').replace('2022/2', '').replace('2023/1', '').replace(
            '2023/2', '')
        nome_turma = i.split('|')[3].replace('- 2022/1', '').replace('-', '').replace('2022/2', '').replace('2023/1',
                                                                                                            '').replace(
            '2023/2', '')
        # valores
        nome_disciplina = unidecode(i.split('|')[4]).upper()
        id_disciplina = i.split('|')[5]
        divisao = i.split('|')[6]
        dia = i.split('|')[7]
        escola = geraEscola(cr_curso_aluno)
        hora_final = i.split('|')[9]
        cr_disciplina = i.split('|')[5]
        nome_curso = i.split('|')[1]
        agrupamento = i.split('|')[10]
        turno = i.split('|')[11]
        qtd_alunos = i.split('|')[12]
        qtd_vagas = i.split('|')[13]
        hora_inicio_old = i.split('|')[8]
        professor = i.split('|')[14]
        hora_inicio = str(hora_inicio_old.split(':')[:-1]).replace(',', ':').replace("'", "").replace("[", "").replace(
            "]", "").replace(' ', '')
        chave_dia = f"{periodo},{nome_turma},{cr_disciplina},{hora_inicio}".replace(' ', '').replace('2022/2',
                                                                                                     '').replace(
            '2023/1', '').upper()
        chave = f"{periodo},{nome_turma},{cr_disciplina},{hora_inicio},{dia},{divisao}".replace(' ', '').upper()
        tipo = gerarTipo(agrupamento)

        dict_valores[chave] = {
            'escola': escola,
            'cr_curso': cr_curso_aluno,
            'nome_disciplina': nome_disciplina,
            'Curso': nome_curso,
            'id_disciplina': id_disciplina,
            'divisao': divisao,
            'Nome_Turma': nome_turma_final,
            'dia': dia,
            'hora_inicio': hora_inicio_old,
            'hora_final': hora_final,
            'cr_disciplina': cr_disciplina,
            'Agrupamento': agrupamento,
            'Turno': turno,
            'qtd_alunos': qtd_alunos,
            'qtd_vagas': qtd_vagas,
            'professor': professor,
            'Tipo': tipo
        }

        chave_horario_repetido = f"{chave}{hora_inicio}"
        try:
            if chave_horario_repetido not in horario_repetido:
                retorna_horario_inicio[chave_dia] += f"|{hora_inicio},{dia},{divisao}"
                horario_repetido.append(chave_horario_repetido)
        except:
            retorna_horario_inicio[chave_dia] = f"{hora_inicio},{dia},{divisao}"

        # retorna id da disciplina
        # - tratamento do nome da disciplina
        nome_disciplina_corrigido = nome_disciplina.split('-')[-1].replace(' ', '')
        chave_disciplina = f"{nome_disciplina_corrigido}{cr_curso_aluno}"
        dict_retorna_cr_disciplina[chave_disciplina] = cr_disciplina

    # usado para utilizar as chaves da planilha e retornar a sala
    dict_retorna_salaxml = {}
    dict_retorna_abrev_salaxml = {}
    key_final = 0
    valores_repetidos = []
    dict_relatorio_final = {}

    # criar dict para retornar a sala
    for dados in array_asc_xml:

        barra = r"'\'"

        periodo = dados.split('|')[1]
        # - tratamento nome turma
        turma = dados.split('|')[2].split('/')[0].replace(barra, '').replace(barra, '').replace(barra, '').replace(
            barra, '').replace("'", '')
        turma = turma[1:]

        turma_nome = converteSigla(turma.split(';')[0])
        abrev_turma = dados.split('|')[2].split('/')[1].replace(barra, '').replace(barra, '').replace(barra,
                                                                                                      '').replace(barra,
                                                                                                                  '').replace(
            "'", '').replace('(', '')
        nome_turma = f"{turma_nome}{periodo}{abrev_turma.split(';')[3]}{turma.split(';')[-1][0]}"
        divisao = dados.split('|')[8]
        dia = dados.split('|')[7]
        hora_inicio = dados.split('|')[9]
        abrev_sala = dados.split('|')[4]
        abrev_sala = abrev_sala.replace(')', '').replace("'", "").replace(' ', '')

        try:
            nome_disciplina = dados.split('|')[6].split(';')[2]
        except:
            f.write(dados.split('|')[6] + 'name esta no formato errado')
            continue
        # valores
        sala = dados.split('|')[3].replace(barra, '').replace(barra, '').replace("'", '').replace('(', '')

        try:
            cr = dados.split('|')[6].split(';')[3]

            cr_curso = dados.split('|')[6].split(';')[0]
            try:
                cr_disciplina = int(cr)
            except:
                nome_disciplina_corrigido = nome_disciplina.split('-')[-1].replace(' ', '').upper()
                nome_disciplina_corrigido = unidecode(nome_disciplina_corrigido)
                chave_disciplina = f"{nome_disciplina_corrigido}{cr_curso}"
                cr_disciplina = dict_retorna_cr_disciplina[chave_disciplina]
                cr_disciplina = str(cr_disciplina)
        except:
            continue

        chave_sala = f"{periodo},{nome_turma},{cr_disciplina},{dia},{divisao},{hora_inicio}".replace(' ', '').upper()

        # retornar sala xml
        try:
            if not dict_retorna_salaxml[chave_sala].__contains__(sala):
                dict_retorna_salaxml[chave_sala] += f",{sala}"
                # dict_retorna_salaxml[chave_sala] = sala
        except:
            dict_retorna_salaxml[chave_sala] = sala

        try:
            if not dict_retorna_abrev_salaxml[sala].__contains__(abrev_sala):
                dict_retorna_abrev_salaxml[sala] += f",{abrev_sala}"
                # dict_retorna_abrev_salaxml[sala] = abrev_sala
        except:
            dict_retorna_abrev_salaxml[sala] = abrev_sala

    log_sem_salas = {}
    log_sala_abrev = {}
    log_sem_turmas_disciplinas = {}
    for dados in array_asc_xml:
        erro_repetido = []
        # barra invertida para poder retirar ela do texto
        barra = r"'\'"
        # valores key
        cr_curso_aluno = dados.split('|')[0].replace(' ', '')
        periodo = dados.split('|')[1]
        hora_inicio_chave_sala = dados.split('|')[9]

        abrev_turma = dados.split('|')[2].split('/')[1].replace(barra, '').replace(barra, '').replace(barra,
                                                                                                      '').replace(barra,
                                                                                                                  '').replace(
            "'", '').replace('(', '')
        dia = dados.split('|')[7]
        try:
            nome_disciplina = dados.split('|')[6].split(';')[2]
        except:
            f.write(dados.split('|')[6] + 'esta no formato errado')
            continue

        # - tratamento nome turma
        turma = dados.split('|')[2].split('/')[0].replace(barra, '').replace(barra, '').replace(barra, '').replace(
            barra, '').replace("'", '')
        turma = turma[1:]
        turma_nome = converteSigla(turma.split(';')[0])
        # turma utilizada para melhor entendimento
        turma_final = f"{turma_nome} - {periodo} - {abrev_turma.split(';')[3]} - {abrev_turma.split(';')[4]}"
        # turma utilizada como key
        nome_turma = f"{turma_nome}{periodo}{abrev_turma.split(';')[3]}{turma.split(';')[-1][0]}"
        try:
            cr = dados.split('|')[6].split(';')[3]

            cr_curso = dados.split('|')[6].split(';')[0]
            try:
                cr_disciplina = int(cr)
            except:
                nome_disciplina_corrigido = nome_disciplina.split('-')[-1].replace(' ', '').upper()
                nome_disciplina_corrigido = unidecode(nome_disciplina_corrigido)
                chave_disciplina = f"{nome_disciplina_corrigido}{cr_curso_aluno}"
                cr_disciplina = dict_retorna_cr_disciplina[chave_disciplina]
                cr_disciplina = int(cr_disciplina)

        except:
            f.write('#' + str(contador) + ' Aviso[Ação]: ' + dados.split('|')[
                6] + ' não foi encontrado o id da disciplina no XML' + '\n')
            contador += 1
            continue

        # valores
        sala = dados.split('|')[3].replace(barra, '').replace(barra, '')

        # chave
        chave = f"{periodo},{nome_turma},{cr_disciplina},{hora_inicio_chave_sala}".replace(' ', '').upper().replace("'",
                                                                                                                    '')

        # armazena a lista de horarios de inicio da turma e disciplina para alocar na chave
        try:
            lista_horario_de_inicio_dia = retorna_horario_inicio[chave]
        except:
            try:
                chave_fic = f"{periodo},{nome_turma[:-1]},{cr_disciplina},{hora_inicio_chave_sala}".replace(' ',
                                                                                                            '').upper().replace(
                    "'", '')
                lista_horario_de_inicio_dia = retorna_horario_inicio[chave_fic]
            except:
                log_sem_turmas_disciplinas[chave] = ''
                continue

        quantidade_horarios = lista_horario_de_inicio_dia.count('|')
        posicao_horario = 0

        for x in range(0, quantidade_horarios + 1):

            hora_inicio = lista_horario_de_inicio_dia.split('|')[posicao_horario].split(',')[0]
            dia = lista_horario_de_inicio_dia.split('|')[posicao_horario].split(',')[1]
            divisao = lista_horario_de_inicio_dia.split('|')[posicao_horario].split(',')[2]

            chave_dia_hora = f"{periodo},{nome_turma},{cr_disciplina},{hora_inicio},{dia},{divisao}".replace(' ',
                                                                                                             '').upper()

            try:
                dia = dict_valores[chave_dia_hora]['dia']
                hora_inicio = dict_valores[chave_dia_hora]['hora_inicio']
                hora_final = dict_valores[chave_dia_hora]['hora_final']
            except:
                try:
                    chave_dia_hora_e = f"{periodo},{nome_turma[:-1]},{cr_disciplina},{hora_inicio},{dia},{divisao}".replace(
                        ' ', '').upper()
                    dia = dict_valores[chave_dia_hora_e]['dia']
                    hora_inicio = dict_valores[chave_dia_hora_e]['hora_inicio']
                    hora_final = dict_valores[chave_dia_hora_e]['hora_final']
                except:
                    posicao_horario += 1
                    f.write(
                        f'#{contador} Aviso[Ação]; Não foi encontrado o dia e hora da turma ' + chave_dia_hora + '\n')
                    continue

            hora_inicio_chave_sala = dados.split('|')[5].split('-')[0].replace('(', '')
            chave_sala = f"{periodo},{nome_turma},{cr_disciplina},{dia},{divisao},{hora_inicio_chave_sala}".replace(' ',
                                                                                                                    '').upper()
            try:
                classroom = dict_retorna_salaxml[chave_sala].replace("'", '').replace('(', '')
            except:
                try:
                    chave_sala_turmafic = f"{periodo},{nome_turma[:-1]},{cr_disciplina},{dia},{divisao}".replace(' ',
                                                                                                                 '').upper()
                    classroom = dict_retorna_salaxml[chave_sala_turmafic].replace("'", '').replace('(', '')
                except:
                    log_sem_salas[chave_sala] = ''
                    # classroom = 'Sem sala'
                    continue

            quantidade = classroom.count(',')
            posicao_sala = 0

            if quantidade == 0:
                quantidade = 1
            else:
                quantidade += 1

            for i in range(0, quantidade):
                sala = classroom.split(',')[posicao_sala]

                # buscando a abreviação da sala
                try:
                    abrev_sala = dict_retorna_abrev_salaxml[sala]

                except:
                    log_sala[sala] = ''

                    continue

                # buscando a capacidade da sala
                try:
                    capacidade = dict_capacidade[abrev_sala]
                except:
                    capacidade = "0"
                    log_sala_abrev[abrev_sala] = ''

                try:
                    valores = dict_valores[chave_dia_hora]
                except:
                    contador += 1
                    f.write(f'#{contador} Aviso[Ação]: dia e hora nao encontrado ' + chave_dia_hora + '\n')
                    continue
                # gerando dict que vai ser inserido no excel

                dict_relatorio_final[key_final] = {
                    'Estabelecimento': 'PUCPR - CURITIBA',
                    'Escola': valores['escola'],
                    'CR Curso': str(valores['cr_curso'].split('.')[0]),
                    'Curso': valores['Curso'],
                    'Periodo': periodo,
                    'Sigla': valores['Agrupamento'],
                    'Tipo': valores['Tipo'],
                    'Turma Prime': f"{valores['Nome_Turma']}2023/1",
                    'Nome disciplina': valores['nome_disciplina'],
                    'Turno': valores['Turno'],
                    'Divisão': valores['divisao'],
                    'Id disciplina': cr_disciplina,
                    'Qtde de Alunos Matri.': verifica_numero(valores['qtd_alunos']),
                    'Nr Vagas Cadastradas': verifica_numero(valores['qtd_vagas']),
                    'Dia': dia,
                    'Hora inicio': hora_inicio,
                    'Hora final': hora_final,
                    'Professor': valores['professor'],
                    'Sala': sala,
                    'Sala Abreviação': abrev_sala,
                    'Capacidade da Sala': capacidade.replace('ECV', '0').replace('nan', '0')
                }

                key_final += 1
                valores_repetidos.append(chave_dia_hora)
                posicao_sala += 1
            posicao_horario += 1

    for chave in log_sala.keys():
        f.write('#' + str(
            contador) + ' Aviso[Ação]; Erro ao buscar a abreviação da sala (periodo,turma,id_disciplina,horario inicio); ' + chave + '\n')
        contador += 1

    for chave in log_sala_abrev.keys():
        f.write('#' + str(contador) + ' Aviso[Info]; Erro ao buscar capacidade da sala (abreviação);' + chave + '\n')
        contador += 1

    # valida para trazer os horarios
    for chave in log_sem_turmas_disciplinas.keys():
        f.write('#' + str(
            contador) + ' Aviso[Ação]; Não foi encontrada no excel prime turmas disciplinas (periodo,turma,id_disciplina,horario inicio); ' + chave + '\n')
        contador += 1

    # valida todas as chaves
    for chave in log_sem_salas.keys():
        f.write('#' + str(
            contador) + ' Aviso[Ação]; Erro na combinação entre XML e Excel Prime (periodo,turma,id_disciplina,dia,divisao,hora inicio); ' + chave + '\n')
        contador += 1

    Relatorio = {}
    valores_repetidos = []
    # tirar repetidos
    for dados in dict_relatorio_final.items():
        if dados[1]['Divisão'] == ' ' or dados[1]['Divisão'] == '  ' or dados[1]['Divisão'] == '   ':
            dados[1]['Divisão'] = '-'
        if dados[1] not in valores_repetidos:
            Relatorio[dados[0]] = dados[1]
            valores_repetidos.append(dados[1])

    df = pandas.DataFrame(data=Relatorio)
    df = (df.T)
    df = df.drop_duplicates()

    df.insert(14, 'Análise Vagas', '')
    df.insert(15, 'Diferença Vagas', '')
    df.insert(23, 'Análise Capacidade', '')
    df.insert(24, 'Diferença Capacidade', '')

    df["Nr Vagas Cadastradas"] = df["Nr Vagas Cadastradas"].replace(" ", 0)
    df["Nr Vagas Cadastradas"] = df["Nr Vagas Cadastradas"].astype(int)
    df["Capacidade da Sala"] = df["Capacidade da Sala"].replace(" ", 0)
    df["Capacidade da Sala"] = df["Capacidade da Sala"].astype(int)
    df["Qtde de Alunos Matri."] = df["Qtde de Alunos Matri."].replace(" ", 0)
    df["Qtde de Alunos Matri."] = df["Qtde de Alunos Matri."].astype(int)
    df["CR Curso"] = df["CR Curso"].astype(str)

    df['Diferença Vagas'] = df.apply(
        lambda row_vagas: row_vagas["Nr Vagas Cadastradas"] - row_vagas["Qtde de Alunos Matri."], axis=1)
    df['Diferença Capacidade'] = df.apply(
        lambda row_vagas: row_vagas["Capacidade da Sala"] - row_vagas["Qtde de Alunos Matri."], axis=1)

    df['Analista'] = df.apply(lambda x: retorna_analista(x['Escola']), axis=1)
    df['Análise Vagas'] = df.apply(lambda row_vagas: analisar_diferenca(row_vagas["Diferença Vagas"]), axis=1)
    df['Análise Capacidade'] = df.apply(lambda row_vagas: analisar_capacidade(row_vagas['Qtde de Alunos Matri.'],
                                                                              row_vagas["Diferença Capacidade"],
                                                                              row_vagas["Capacidade da Sala"],
                                                                              row_vagas["Sala"]), axis=1)

    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    dt_now = utc_now.astimezone(pytz.timezone("America/Sao_Paulo"))
    nome_arquivo = file_name
    writer = pandas.ExcelWriter(nome_arquivo, engine='xlsxwriter')

    df.to_excel(writer, index=False, sheet_name="Completo")

    workbook = writer.book
    worksheet = writer.sheets['Completo']

    formato_verde = workbook.add_format({'font_color': '#006100'})
    formato_verde.set_bg_color('#C6EFCE')
    formato_amarelo = workbook.add_format({'font_color': '#9C5700'})
    formato_amarelo.set_bg_color('#FFEB9C')
    formato_vermelho = workbook.add_format({'font_color': '#9C0031'})
    formato_vermelho.set_bg_color('#FFC7CE')
    formato_cinza_status = workbook.add_format({'font_color': '#1c1c1b'})
    formato_cinza_status.set_bg_color('#9e9891')

    row = 1
    for index, linha in df.iterrows():

        for x in range(0, 25):
            item = str(linha[x])
            if item == "nan":
                item = ''
            if x == 14 or x == 23:
                if item == "Vagas Disponíveis" or item == "Capacidade disponível":
                    worksheet.write(row, x, item, formato_verde)
                elif item == "Não há vagas" or item == "Indisponível" or item == "Sem Capacidade":
                    worksheet.write(row, x, item, formato_amarelo)
                elif item == "Vagas excedidas" or item == "Capacidade excedida" \
                        or item == "Sala lotada":
                    worksheet.write(row, x, item, formato_vermelho)
                elif item == "Sem sala":
                    worksheet.write(row, x, item, formato_cinza_status)
                else:
                    worksheet.write(row, x, item)
            elif x == 15 or x == 24:

                if str(linha[x - 1]) == "Vagas Disponíveis" or str(linha[x - 1]) == "Capacidade disponível":
                    worksheet.write(row, x, item.split('.')[0], formato_verde)
                elif str(linha[x]) == "Sem sala":
                    worksheet.write(row, x, item, formato_cinza_status)
                elif str(linha[x - 1]) == "Não há vagas" or str(linha[x - 1]) == "Indisponível" or \
                        str(linha[x - 1]) == "Sem Capacidade":
                    worksheet.write(row, x, item.split('.')[0], formato_amarelo)
                elif str(linha[x - 1]) == "Vagas excedidas" or str(linha[x - 1]) == "Capacidade excedida" \
                        or str(linha[(x - 1)]) == "Sala lotada":
                    worksheet.write(row, x, item.split('.')[0], formato_vermelho)
                else:
                    worksheet.write(row, x, item.split('.')[0])
            else:
                worksheet.write(row, x, item)

        row += 1
    # Formatação do excel, adicionando estilo
    worksheet.add_table(0, 0, row - 1, 25, {'style': 'Table Style Light 1', 'columns': [
        {'header': 'Estabelecimento'},
        {'header': 'Escola'},
        {'header': 'CR Curso'},
        {'header': 'Curso'},
        {'header': 'Período'},
        {'header': 'Sigla'},
        {'header': 'Tipo'},
        {'header': 'Turma Prime'},
        {'header': 'Nome disciplina'},
        {'header': 'Turno'},
        {'header': 'Divisão'},
        {'header': 'Id disciplina'},
        {'header': 'Matriculados'},
        {'header': 'Vagas Cadastradas'},
        {'header': 'Análise Vagas'},
        {'header': 'Diferença Vagas'},
        {'header': 'Dia da Semana'},
        {'header': 'Horário de início'},
        {'header': 'Horário de término'},
        {'header': 'Professor'},
        {'header': 'Sala'},
        {'header': 'Sala Abreviação'},
        {'header': 'Capacidade da Sala'},
        {'header': 'Análise Capacidade'},
        {'header': 'Diferença Capacidade'},
        {'header': 'Analista'}
    ]})

    # Formatação da Largura da Tabela
    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:B', 25)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 81)
    worksheet.set_column('E:E', 10)
    worksheet.set_column('F:F', 10)
    worksheet.set_column('G:G', 30)
    worksheet.set_column('H:H', 40)
    worksheet.set_column('I:I', 72)
    worksheet.set_column('J:J', 25)
    worksheet.set_column('K:K', 15)
    worksheet.set_column('L:L', 20)
    worksheet.set_column('M:M', 20)
    worksheet.set_column('N:N', 20)
    worksheet.set_column('O:O', 20)
    worksheet.set_column('P:P', 25)
    worksheet.set_column('Q:Q', 26)
    worksheet.set_column('R:R', 20)
    worksheet.set_column('S:S', 20)
    worksheet.set_column('T:T', 45)
    worksheet.set_column('U:U', 42)
    worksheet.set_column('V:V', 25)
    worksheet.set_column('W:W', 25)
    worksheet.set_column('X:X', 25)
    worksheet.set_column('Y:Y', 25)
    worksheet.set_column('Y:Y', 25)

    df_modificado = df

    df_modificado = df_modificado.drop(columns=['Professor'])
    df_modificado = df_modificado.drop(columns=['Hora inicio'])
    df_modificado = df_modificado.drop(columns=['Hora final'])
    df_modificado = df_modificado.drop(columns=['Dia'])
    df_modificado = df_modificado.drop_duplicates()

    df_modificado['Analista'] = df_modificado.apply(lambda x: retorna_analista(x['Escola']), axis=1)
    df_modificado['Status'] = df_modificado.apply(
        lambda x: retorna_status(x['Sala'], x['Diferença Capacidade'], x['Capacidade da Sala']), axis=1)

    df_modificado.to_excel(writer, index=False, sheet_name="Resumido")

    workbook = writer.book
    worksheet = writer.sheets['Resumido']

    formato_verde_status = workbook.add_format({'font_color': '#1c1c1b'})
    formato_verde_status.set_bg_color('#C6EFCE')

    formato_amarelo_status = workbook.add_format({'font_color': '#1c1c1b'})
    formato_amarelo_status.set_bg_color('#FFEB9C')

    formato_laranja_status = workbook.add_format({'font_color': '#1c1c1b'})
    formato_laranja_status.set_bg_color('#b37f30')

    formato_laranja_status = workbook.add_format({'font_color': '#1c1c1b'})
    formato_laranja_status.set_bg_color('#b37f30')

    formato_cinza_status = workbook.add_format({'font_color': '#1c1c1b'})
    formato_cinza_status.set_bg_color('#9e9891')

    formato_vermelho_status = workbook.add_format({'font_color': '#1c1c1b'})
    formato_vermelho_status.set_bg_color('#b33030')

    row = 1
    for index, linha in df_modificado.iterrows():
        for x in range(0, 23):
            item = str(linha[x])
            if item == "nan":
                item = ''
            if x == 14 or x == 19:
                if item == "Vagas Disponíveis" or item == "Capacidade disponível":
                    worksheet.write(row, x, item, formato_verde)
                elif item == "Não há vagas" or item == "Indisponível" or item == "Sem Capacidade":
                    worksheet.write(row, x, item, formato_amarelo)
                elif item == "Vagas excedidas" or item == "Capacidade excedida" \
                        or item == "Sala lotada":
                    worksheet.write(row, x, item, formato_vermelho)
                else:
                    worksheet.write(row, x, item)
            elif x == 15 or x == 20:
                if str(linha[x - 1]) == "Vagas Disponíveis" or str(linha[x - 1]) == "Capacidade disponível":
                    worksheet.write(row, x, item.split('.')[0], formato_verde)
                elif str(linha[x - 1]) == "Não há vagas" or str(linha[x - 1]) == "Indisponível" or \
                        str(linha[x - 1]) == "Sem Capacidade":
                    worksheet.write(row, x, item.split('.')[0], formato_amarelo)
                elif str(linha[x - 1]) == "Vagas excedidas" or str(linha[x - 1]) == "Capacidade excedida" \
                        or str(linha[(x - 1)]) == "Sala lotada":
                    worksheet.write(row, x, item.split('.')[0], formato_vermelho)
                else:
                    worksheet.write(row, x, item.split('.')[0])
            elif x == 22:
                if str(linha[x]) == "Sem sala":
                    worksheet.write(row, x, item, formato_cinza_status)
                elif str(linha[x]) == "Lotada - rever ensalamento":
                    worksheet.write(row, x, item, formato_vermelho_status)
                elif str(linha[x]) == "Ok":
                    worksheet.write(row, x, item, formato_verde_status)
                elif str(linha[x]) == "Próximo da capacidade":
                    worksheet.write(row, x, item, formato_amarelo_status)
                elif str(linha[x]) == "Sem info capacidade":
                    worksheet.write(row, x, item, formato_laranja_status)
            else:
                worksheet.write(row, x, item)

        row += 1
    worksheet.add_table(0, 0, row - 1, 22, {'style': 'Table Style Light 1', 'columns': [
        {'header': 'Estabelecimento'},
        {'header': 'Escola'},
        {'header': 'CR Curso'},
        {'header': 'Curso'},
        {'header': 'Período'},
        {'header': 'Sigla'},
        {'header': 'Tipo'},
        {'header': 'Turma Prime'},
        {'header': 'Nome disciplina'},
        {'header': 'Turno'},
        {'header': 'Divisão'},
        {'header': 'Id disciplina'},
        {'header': 'Matriculados'},
        {'header': 'Vagas Cadastradas'},
        {'header': 'Análise Vagas'},
        {'header': 'Diferença Vagas'},
        {'header': 'Sala'},
        {'header': 'Sala Abreviação'},
        {'header': 'Capacidade da Sala'},
        {'header': 'Análise Capacidade'},
        {'header': 'Diferença Capacidade'},
        {'header': 'Analista'},
        {'header': 'Status'}
    ]})

    # Formatação da Largura da Tabela
    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:B', 25)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 81)
    worksheet.set_column('E:E', 10)
    worksheet.set_column('F:F', 10)
    worksheet.set_column('G:G', 30)
    worksheet.set_column('H:H', 40)
    worksheet.set_column('I:I', 72)
    worksheet.set_column('J:J', 25)
    worksheet.set_column('K:K', 15)
    worksheet.set_column('L:L', 20)
    worksheet.set_column('M:M', 20)
    worksheet.set_column('N:N', 20)
    worksheet.set_column('O:O', 20)
    worksheet.set_column('P:P', 25)
    worksheet.set_column('Q:Q', 26)
    worksheet.set_column('R:R', 20)
    worksheet.set_column('S:S', 20)
    worksheet.set_column('T:T', 45)
    worksheet.set_column('U:U', 42)
    worksheet.set_column('V:V', 20)
    worksheet.set_column('W:W', 42)

    df_capacidade = pandas.read_excel(file_name_capacidade, sheet_name="BASE DE CAPACIDADES CWB", header=2,usecols=range(5, 26))

    df_capacidade.to_excel(writer, index=False, sheet_name="Ambientes de Aprendizagem")

    df_horarios = pandas.DataFrame()

    df_horarios["NOME ESPAÇO ASC"] = df_capacidade["NOME ESPAÇO ASC"]

    dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sabado']

    horarios = ["07:50:00", "08:35:00", "09:40:00", "10:25:00", "11:10:00", "11:55:00", "12:40:00",
                "13:25:00", "14:10:00", "15:15:00", "16:00:00", "16:45:00", "17:30:00", "18:15:00",
                "19:00:00", "19:45:00", "20:45:00", "21:30:00", "22:15:00"]

    dict_horarios = {}
    key = 0
    for dados in df_horarios.iterrows():
        for dia in dias:
            for hora in horarios:
                dict_horarios[key] = {
                    "NOME ESPAÇO ASC": dados[1]["NOME ESPAÇO ASC"],
                    "Dia da semana": dia,
                    "Horário": hora
                }
                key += 1

    df_horarios = pandas.DataFrame(data=dict_horarios)
    df_horarios = (df_horarios.T)
    df_horarios.to_excel(writer, index=False, sheet_name="Ambientes Horários")
    workbook = writer.book
    worksheet = writer.sheets['Ambientes Horários']

    worksheet.add_table(0, 0, row - 1, 2, {'style': 'Table Style Light 1', 'columns': [
        {'header': 'NOME ESPAÇO ASC'},
        {'header': 'Dia da semana'},
        {'header': 'Horário'},

    ]})

    # Formatação da Largura da Tabela
    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:B', 25)
    worksheet.set_column('C:C', 15)

    writer.close()
    return nome_arquivo


def retorna_analista(escola):
    if escola == 'Belas Artes':
        analista = 'Diego'

    elif escola == 'Ciências da Vida':
        analista = 'Sheyla'

    elif escola == 'Direito':
        analista = 'Marilise'

    elif escola == 'Educação e Humanidades':
        analista = 'Cristiane'

    elif escola == 'Medicina':
        analista = 'Aline'

    elif escola == 'Negócios':
        analista = 'Elisângela'

    elif escola == 'Politécnica':
        analista = 'Edivane'
    else:
        analista = 'não encontrado'

    return analista


def verifica_numero(valor):
    try:
        numero = int(valor)
    except:
        if valor == "nan":
            numero = 0
        else:
            numero = float(valor)
            numero = int(numero)
    return numero


def retorna_status(sala, diferenca, capacidade):
    if sala == 'Sem sala':
        valor = 'Sem sala'
    elif capacidade == '0' or capacidade == 0:
        valor = 'Sem info capacidade'
    elif diferenca < 0:
        valor = 'Lotada - rever ensalamento'
    elif diferenca < 5:
        valor = 'Próximo da capacidade'
    else:
        valor = 'Ok'
    return valor


def main(arquivo_carga_horaria, arquivo_capacidade, arquivo_xml, file_name):
    # pega somente o nome do arquivo para que o log seja salvo na mesma pasta
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    dt_now = utc_now.astimezone(pytz.timezone("America/Sao_Paulo"))
    f = open(f"./Arquivos_Auxiliares/Log/{str(dt_now.strftime('%y-%m-%d %H-%M'))}.txt", "w+", encoding="utf8")

    file_name_turma_disciplina = arquivo_carga_horaria

    file_name_asc_xml = arquivo_xml

    file_name_capacidade = arquivo_capacidade
    print('Carregando...')

    with open('./Arquivos_Auxiliares/siglas.json', 'r', encoding="utf-8") as j:
        file_json_sigla = json.loads(j.read())

    with open('./Arquivos_Auxiliares/turmasfic.json', 'r', encoding="utf-8") as j:
        file_json_turmasfic = json.loads(j.read())

    with open('./Arquivos_Auxiliares/escolas.json', 'r', encoding="utf-8") as j:
        file_json_escolas = json.loads(j.read())

    with open('./Arquivos_Auxiliares/tipos.json', 'r', encoding="utf-8") as j:
        file_json_tipos = json.loads(j.read())

    nome_arquivo = gerarRelatorio(file_name_turma_disciplina, file_name_asc_xml, file_json_sigla, file_name_capacidade,
                                  file_json_turmasfic, contador, file_json_escolas, file_json_tipos, f, file_name)
    return nome_arquivo


def gerarExcel(file_carga_horaria, file_capacidade, file_xml, file_name):
    # le os valores vindo da tela
    arquivo_carga_horaria = file_carga_horaria
    arquivo_capacidade = file_capacidade

    arquivo_xml = Unificar_XML.main(file_xml)

    nome_arquivo = main(arquivo_carga_horaria, arquivo_capacidade, arquivo_xml, file_name)

    Sugestao.main(nome_arquivo, arquivo_capacidade)

if __name__ == '__main__':

    gerarExcel()
