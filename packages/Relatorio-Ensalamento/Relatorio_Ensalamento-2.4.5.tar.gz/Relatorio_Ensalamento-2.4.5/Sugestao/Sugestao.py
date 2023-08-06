import numpy as np
import pandas


class Disciplina:
    def __init__(self, escola, cr_curso, curso, periodo, turma_prime, nome_disciplina, turno, divisao, id_disciplina,
                 nome_professor, alunos_matriculados, vagas, diferenca_vagas, dia,
                 hora_inicio, diferenca_capacidade, analise_capacidade, capacidade_sala):
        self.escola = escola
        self.cr = cr_curso
        self.curso = curso
        self.periodo = periodo
        self.turma_prime = turma_prime
        self.nome_disciplina = nome_disciplina
        self.turno = turno
        self.divisao = divisao
        self.id_disciplina = id_disciplina
        self.nome_professor = nome_professor
        self.alunos_matriculados = alunos_matriculados
        self.vagas = vagas
        self.diferenca_vagas = diferenca_vagas
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.diferenca_capacidade = diferenca_capacidade
        self.analise_capacidade = analise_capacidade
        self.capacidade_sala = capacidade_sala

        if capacidade_sala == 0:
            porcentagem_utilizacao = 0 - alunos_matriculados
        else:
            porcentagem_utilizacao = (alunos_matriculados / capacidade_sala) * 100
            porcentagem_utilizacao = round(porcentagem_utilizacao, 2)

        self.porcentagem_utilizacao = round(porcentagem_utilizacao, 2)

class Subutilizada:
    def __init__(self, sala, disciplina):
        self.sala = sala
        self.disciplina = disciplina
class AmbienteDeAprendizagem:
    def __init__(self, nome_sala, nome_sala_abrev, capacidade_sala, status, disciplina, tipo, tipo_detalhado, escola,curso):
        self.nome_sala = nome_sala
        self.nome_sala_abrev = nome_sala_abrev

        try:
            self.capacidade_sala = int(capacidade_sala)
        except:
            self.capacidade_sala = 0

        self.status = status
        self.Disciplina = disciplina
        self.tipo = tipo
        self.tipo_detalhado = tipo_detalhado
        self.escola = escola
        self.curso = curso

def create_objects(file_name, dict_retorna_status_type, list, dict_retorna_utilizado_graduacao):
    df = pandas.read_excel(file_name, sheet_name='Completo')
    list_sem_status = []
    dict_retorna_escola = {}

    for data in df.iterrows():

        # para nao repetir as salas
        lista_salas = []
        list_objects_disciplinas = []

        # variaveis sala
        nome_sala = data[1]['Sala']
        nome_sala_abrev = data[1]['Sala Abreviação']
        capacidade_sala = data[1]['Capacidade da Sala']
        diferenca_capacidade = data[1]['Diferença Capacidade']
        analise_capacidade = data[1]['Análise Capacidade']
        df_sala = df.loc[df['Sala'] == nome_sala]
        escola = data[1]['Escola']
        curso = data[1]['Curso']
        dia = data[1]['Dia da Semana']

        try:
            utilizado_graduacao = dict_retorna_utilizado_graduacao[nome_sala]
        except:
            utilizado_graduacao = "Sim"

        if utilizado_graduacao == "Não":
            continue

        if nome_sala not in lista_salas:
            for data_disciplinas in df_sala.iterrows():
                # variaveis disciplinas
                escola = data_disciplinas[1]['Escola']
                cr_curso = data_disciplinas[1]['CR Curso']
                curso = data_disciplinas[1]['Curso']
                periodo = data_disciplinas[1]['Período']
                turma_prime = data_disciplinas[1]['Turma Prime']
                nome_disciplina = data_disciplinas[1]['Nome disciplina']
                turno = data_disciplinas[1]['Turno']
                divisao = data_disciplinas[1]['Divisão']
                id_disciplina = data_disciplinas[1]['Id disciplina']
                nome_professor = data_disciplinas[1]['Professor']
                alunos_matriculados = data_disciplinas[1]['Matriculados']
                vagas = data_disciplinas[1]['Vagas Cadastradas']
                dia = data_disciplinas[1]['Dia da Semana']
                hora_inicio = data_disciplinas[1]['Horário de início']
                diferenca_vagas = data_disciplinas[1]['Diferença Vagas']

                disciplina = Disciplina(escola, cr_curso, curso, periodo, turma_prime, nome_disciplina, turno, divisao,
                                        id_disciplina, nome_professor, alunos_matriculados, vagas, diferenca_vagas, dia,
                                        hora_inicio, diferenca_capacidade, analise_capacidade, capacidade_sala)

                list_objects_disciplinas.append(disciplina)
                lista_salas.append(nome_sala)

        try:
            status = dict_retorna_status_type[nome_sala][0]
            tipo = dict_retorna_status_type[nome_sala][1]
            tipo_detalhado = dict_retorna_status_type[nome_sala][2]
        except:
            if nome_sala not in list_sem_status:
                list_sem_status.append(nome_sala)
                # print('Sem status pois, não encontrada na capacidade sala: ',nome_sala)
            status = 'Ativa'
            tipo = " "
            tipo_detalhado = "Sala não esta planilha de infra."

        sala = AmbienteDeAprendizagem(nome_sala, nome_sala_abrev, capacidade_sala, status, list_objects_disciplinas,
                                      tipo, tipo_detalhado, escola,curso)
        dict_retorna_escola[nome_sala] = escola
        list.append(sala)

    return list, dict_retorna_escola


def insert_matriz(list):
    # matriz[linha][coluna]
    def create_matriz(n_linhas, n_colunas):
        return [["         "] * n_colunas for _ in range(n_linhas)]

    matriz = create_matriz(len(list), 141)

    row = 0
    for object in list:
        matriz[row][0] = object
        if object.Disciplina != None:
            for disciplina in object.Disciplina:
                list_aux = []
                indice = get_indice(disciplina)
                matriz[row][indice] = disciplina
        row += 1

    return matriz


def get_indice(object):
    indice = 0
    dia = object.dia.upper()
    hora_inicio = object.hora_inicio

    if dia == "SEGUNDA-FEIRA":
        indice = 0
    elif dia == "TERÇA-FEIRA":
        indice = 19
    elif dia == "QUARTA-FEIRA":
        indice = 39
    elif dia == "QUINTA-FEIRA":
        indice = 59
    elif dia == "SEXTA-FEIRA":
        indice = 79
    elif dia == "SABADO" or dia == "SÁBADO":
        indice = 99
    elif dia == "FLUTUANTE":
        indice = 119
    else:
        print('erro em encontrar o dia no indice: ', dia)
        exit()

    if hora_inicio == "07:05:00":
        indice += 1
    elif hora_inicio == "07:50:00":
        indice += 2
    elif hora_inicio == "08:35:00":
        indice += 3
    elif hora_inicio == "09:40:00":
        indice += 4
    elif hora_inicio == "10:25:00":
        indice += 5
    elif hora_inicio == "11:10:00":
        indice += 6
    elif hora_inicio == "11:55:00":
        indice += 7
    elif hora_inicio == "12:40:00":
        indice += 8
    elif hora_inicio == "13:25:00":
        indice += 9
    elif hora_inicio == "14:10:00":
        indice += 10
    elif hora_inicio == "15:15:00":
        indice += 11
    elif hora_inicio == "16:00:00":
        indice += 12
    elif hora_inicio == "16:45:00":
        indice += 13
    elif hora_inicio == "17:30:00":
        indice += 14
    elif hora_inicio == "18:15:00":
        indice += 15
    elif hora_inicio == "19:00:00":
        indice += 16
    elif hora_inicio == "19:45:00":
        indice += 17
    elif hora_inicio == "20:45:00":
        indice += 18
    elif hora_inicio == "21:30:00":
        indice += 19
    elif hora_inicio == "22:15:00":
        indice += 20
    elif hora_inicio == "--":
        indice += 21
    else:
        print('erro em encontrar o horário no indice: ', hora_inicio)
        exit()

    return indice


def get_indice_analyze(dia, hora_inicio):
    indice = 0

    dia = dia.upper()

    if dia == "SEGUNDA-FEIRA":
        indice = 0
    elif dia == "TERÇA-FEIRA":
        indice = 19
    elif dia == "QUARTA-FEIRA":
        indice = 39
    elif dia == "QUINTA-FEIRA":
        indice = 59
    elif dia == "SEXTA-FEIRA":
        indice = 79
    elif dia == "SABADO" or dia == "SÁBADO":
        indice = 99
    elif dia == "FLUTUANTE":
        indice = 119
    else:
        print('erro em encontrar o dia no indice: ', dia)
        exit()

    if hora_inicio == "07:50:00":
        indice += 1
    elif hora_inicio == "08:35:00":
        indice += 2
    elif hora_inicio == "09:40:00":
        indice += 3
    elif hora_inicio == "10:25:00":
        indice += 4
    elif hora_inicio == "11:10:00":
        indice += 5
    elif hora_inicio == "11:55:00":
        indice += 6
    elif hora_inicio == "12:40:00":
        indice += 7
    elif hora_inicio == "13:25:00":
        indice += 8
    elif hora_inicio == "14:10:00":
        indice += 9
    elif hora_inicio == "15:15:00":
        indice += 10
    elif hora_inicio == "16:00:00":
        indice += 11
    elif hora_inicio == "16:45:00":
        indice += 12
    elif hora_inicio == "17:30:00":
        indice += 13
    elif hora_inicio == "18:15:00":
        indice += 14
    elif hora_inicio == "19:00:00":
        indice += 15
    elif hora_inicio == "19:45:00":
        indice += 16
    elif hora_inicio == "20:45:00":
        indice += 17
    elif hora_inicio == "21:30:00":
        indice += 18
    elif hora_inicio == "22:15:00":
        indice += 19
    elif hora_inicio == "--":
        indice += 20
    else:
        print('erro em encontrar o horário no indice: ', hora_inicio)
        exit()

    return indice


def create_objects_capacidade(arquivo_capacidade, List_objects, dict_retorna_escola):
    salas_ativas = []
    list = []
    for sala in List_objects:
        salas_ativas.append(sala.nome_sala)

    df = pandas.read_excel(arquivo_capacidade, sheet_name="BASE DE CAPACIDADES CWB", header=2)
    for data in df.iterrows():

        nome_sala = data[1]['NOME ESPAÇO ASC']
        utilizado_graduacao = data[1]['UTILIZADO NA GRADUACAO']

        if utilizado_graduacao == "Não" or nome_sala.__contains__("AULA EXTERNA") is False:
            continue

        if nome_sala not in salas_ativas:
            nome_sala_abrev = data[1]['CÓD. ASC'].replace(' ', '')
            capacidade_sala = data[1]['CAPACIDADE']
            status = data[1]['STATUS']
            tipo = str(data[1]['TIPO DE INSTALAÇÃO'])

            tipo_detalhado = str(data[1]['TIPO DE INSTALAÇÃO DETALHADO'])

            try:
                escola = dict_retorna_escola[nome_sala]
            except:
                escola = ""

            list_objects_disciplinas = None

            sala = AmbienteDeAprendizagem(nome_sala, nome_sala_abrev, capacidade_sala, status, list_objects_disciplinas,
                                          tipo, tipo_detalhado, escola)

            list.append(sala)
    return list


def insert_excel(nome_arquivo, dict_retorna_sugestao, dict_retorna_sugestao_list, dict_retorna_sugestao_subutilizada):
    # key = nome da sala, nome da disciplina, dia, hora inicio
    def retorna_sugestao(nome_sala, nome_disciplina, dia, hora_inicio, analise, dict_retorna_sugestao):
        key = f"{nome_sala},{nome_disciplina},{dia},{hora_inicio}"
        key = key.upper()
        sala = ""
        if analise == 'Capacidade excedida' or analise == 'Sem Capacidade' \
                or analise == 'Sala lotada' or analise == 'Sem sala':
            if key in dict_retorna_sugestao.keys():
                sala = dict_retorna_sugestao[key]
                sala = f"{sala.nome_sala} ({sala.capacidade_sala})"
        return sala

    def retorna_sugestao_sugestao_subutilizada(nome_sala, nome_disciplina, dia, hora_inicio, analise,
                                               dict_retorna_sugestao_subutilizada):
        key = f"{nome_sala},{nome_disciplina},{dia},{hora_inicio}"
        key = key.upper()
        sala = ""
        numero = 1
        list_aux = []

        if analise == 'Capacidade excedida' or analise == 'Sem Capacidade' \
                or analise == 'Sala lotada' or analise == 'Sem sala':
            if key in dict_retorna_sugestao_subutilizada.keys():
                list_sala = dict_retorna_sugestao_subutilizada[key]

                num = len(list_sala)
                for sala_aux in list_sala:
                    nome = sala_aux.sala.nome_sala
                    capacidade = sala_aux.sala.capacidade_sala
                    tipo = sala_aux.sala.tipo.lower()
                    alunos_matriculados = sala_aux.disciplina.alunos_matriculados

                    sala += f"{numero}. {nome} ({alunos_matriculados}/{capacidade}) | \n"
                    numero += 1

                while numero <= 5:
                    sala += f'{numero}. Nenhum ambiente do tipo "{tipo}" esta disponivel | \n'
                    numero += 1



        sala = sala[:-1]
        return sala

    def retorna_sugestao_list(nome_sala, nome_disciplina, dia, hora_inicio, analise, dict_retorna_sugestao_list):
        key = f"{nome_sala},{nome_disciplina},{dia},{hora_inicio}"
        key = key.upper()
        sala = ""
        numero = 1
        if analise == 'Capacidade excedida' or analise == 'Sem Capacidade' \
                or analise == 'Sala lotada' or analise == 'Sem sala':
            if key in dict_retorna_sugestao_list.keys():
                list_sala = dict_retorna_sugestao_list[key]
                for sala_aux in list_sala:
                    sala += f"{numero}. {sala_aux.nome_sala} ({sala_aux.capacidade_sala}) | \n"
                    numero += 1

        sala = sala[:-1]
        return sala

    df = pandas.read_excel(nome_arquivo, sheet_name=None)

    df_completo = df['Completo']

    df_completo['Top 5 vazias'] = df_completo.apply(
        lambda x: retorna_sugestao_list(x['Sala'], x['Nome disciplina'], x['Dia da Semana'], x['Horário de início'],
                                        x['Análise Capacidade'], dict_retorna_sugestao_list), axis=1)

    df_completo['Sala Vazia'] = df_completo.apply(
        lambda x: retorna_sugestao(x['Sala'], x['Nome disciplina'], x['Dia da Semana'], x['Horário de início'],
                                   x['Análise Capacidade'], dict_retorna_sugestao), axis=1)

    df_completo['Top 5 Subutilizadas'] = df_completo.apply(
        lambda x: retorna_sugestao_sugestao_subutilizada(x['Sala'], x['Nome disciplina'], x['Dia da Semana'],
                                                         x['Horário de início'],
                                                         x['Análise Capacidade'], dict_retorna_sugestao_subutilizada),
        axis=1)

    writer = pandas.ExcelWriter(nome_arquivo, engine='xlsxwriter')

    df_completo.to_excel(writer, index=False, sheet_name="Completo")
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
    for index, linha in df_completo.iterrows():

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
    worksheet.add_table(0, 0, row - 1, 28, {'style': 'Table Style Light 1', 'columns': [
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
        {'header': 'Analista'},
        {'header': 'Top 5 vazias'},
        {'header': 'Sala Vazia'},
        {'header': 'Top 5 subutilizadas'}
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
    worksheet.set_column('Z:Z', 25)
    worksheet.set_column('AA:AA', 42)
    worksheet.set_column('AB:AB', 42)
    worksheet.set_column('AC:AC', 42)

    df_resumido = df['Resumido']

    df_resumido.to_excel(writer, index=False, sheet_name="Resumido")

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
    for index, linha in df_resumido.iterrows():
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

    def transforma_porcentagem(num):

        valor = num * 100
        valor = f"{valor}%"
        return valor

    df_capacidade = df['Ambientes de Aprendizagem']

    df_capacidade['Overbooking negociado com o coordenador'] = df_capacidade.apply(
        lambda x: transforma_porcentagem(x['Overbooking negociado com o coordenador']), axis=1)

    df_capacidade.to_excel(writer, index=False, sheet_name="Ambientes de Aprendizagem")
    workbook = writer.book
    worksheet = writer.sheets['Ambientes de Aprendizagem']

    # Formatação da Largura da Tabela
    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:B', 25)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 25)
    worksheet.set_column('E:E', 40)
    worksheet.set_column('F:F', 25)
    worksheet.set_column('G:G', 15)
    worksheet.set_column('H:H', 63)
    worksheet.set_column('I:I', 40)
    worksheet.set_column('J:J', 35)
    worksheet.set_column('K:K', 20)
    worksheet.set_column('L:L', 20)
    worksheet.set_column('M:M', 25)
    worksheet.set_column('N:N', 15)
    worksheet.set_column('O:O', 15)
    worksheet.set_column('P:P', 15)
    worksheet.set_column('Q:Q', 20)
    worksheet.set_column('R:R', 30)
    worksheet.set_column('S:S', 30)
    worksheet.set_column('T:T', 40)
    worksheet.set_column('U:U', 40)

    df_horarios = df['Ambientes Horários']
    df_horarios.to_excel(writer, index=False, sheet_name="Ambientes Horários")
    workbook = writer.book
    worksheet = writer.sheets['Ambientes Horários']

    worksheet.add_table(0, 0, row - 1, 2, {'style': 'Table Style Light 1', 'columns': [
        {'header': 'NOME ESPAÇO ASC'},
        {'header': 'Dia da semana'},
        {'header': 'Horário'},

    ]})

    # Formatação da Largura da Tabela
    worksheet.set_column('A:A', 42)
    worksheet.set_column('B:B', 25)
    worksheet.set_column('C:C', 15)

    writer.close()


def create_dict_status_type(arquivo_capacidade, dict_retorna_utilizado_graduacao):
    dict_retona_status = {}

    df = pandas.read_excel(arquivo_capacidade, sheet_name="BASE DE CAPACIDADES CWB", header=2)
    df = df.fillna('')
    for data in df.iterrows():
        nome_sala = str(data[1]['NOME ESPAÇO ASC'])
        status = str(data[1]['STATUS'])
        tipo = str(data[1]['TIPO DE INSTALAÇÃO'])
        tipo_detalhado = str(data[1]['TIPO DE INSTALAÇÃO DETALHADO'])
        utilizado_graduacao = data[1]['UTILIZADO NA GRADUACAO']

        dict_retorna_utilizado_graduacao[nome_sala] = utilizado_graduacao

        if tipo_detalhado == '':
            tipo_detalhado = "Não especificado na planilha de infra."

        dict_retona_status[nome_sala] = status, tipo, tipo_detalhado

    return dict_retona_status, dict_retorna_utilizado_graduacao


def analyze_matriz(matriz, df_capacidade_excedida, dict_retorna_status_type, dict_retorna_prioridade_escola):
    m = np.array(matriz)
    row_number, column_number = m.shape

    # lista para não repetir sugestões
    repeated_classrooms = []

    dict_retorna_sugestao = {}

    for data in df_capacidade_excedida.iterrows():

        # lista de salas vazias
        list_empty_classroom = []

        # pegar o numero da coluna
        day = data[1]["Dia da Semana"]
        start_hour = data[1]["Horário de início"]

        column = get_indice_analyze(day, start_hour)

        # atributos sala atual
        # capacidade esperada
        capacidade_esperada = data[1]["Matriculados"]
        # key
        classroom_name = data[1]["Sala"]
        bloco = classroom_name = classroom_name.split("-")[0]
        subject_name = data[1]["Nome disciplina"]
        try:
            type = dict_retorna_status_type[classroom_name][1]
            detailed_type = dict_retorna_status_type[classroom_name][2]
        except:
            type = " "
            detailed_type = " "

        for row_aux in range(0, row_number):
            if matriz[row_aux][column] == "         ":
                list_empty_classroom.append(matriz[row_aux][0])

        # ordenando em ordem crescente a lista
        list_empty_classroom = sorted(list_empty_classroom, key=lambda x: x.capacidade_sala)

        # aramazenando a lista de prioridades
        try:
            list_blocos = dict_retorna_prioridade_escola[data[1]["Escola"]]
        except:
            list_blocos = []

        # se a lista for maior que 1 o for para
        list_aux = []

        # todo 1 verificação
        # verificando bloco atual e tipo detalhado
        for classroom in list_empty_classroom:

            # atributos da sala sendo analisada
            capacidade_sala_aux = classroom.capacidade_sala
            bloco_aux = classroom.nome_sala.split('-')[0]
            detailed_type_aux = classroom.tipo_detalhado
            status = classroom.status

            # verificando se é um numero valido
            try:
                int(capacidade_sala_aux)
            except:
                continue

            if len(list_aux) >= 1:
                break

            # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
            key = f"{classroom_name},{subject_name},{day},{start_hour}"
            key = key.upper()

            # verifica utilizando o bloco
            if capacidade_sala_aux > capacidade_esperada and key not in dict_retorna_sugestao.keys() \
                    and f"{classroom_name},{column}" not in repeated_classrooms and status == 'Ativa' \
                    and bloco == bloco_aux and detailed_type == detailed_type_aux:
                # não repetir sugestão
                repeated_classrooms.append(f"{classroom_name},{column}")
                list_aux.append(classroom)
                dict_retorna_sugestao[key] = classroom

        # todo 2 verificação
        # verificando bloco prioridade da escola e tipo detalhado
        for numero_bloco in list_blocos:

            if numero_bloco <= 9:
                bloco = f"Bloco 0{numero_bloco} "
            else:
                bloco = f"Bloco {numero_bloco} "

            for classroom in list_empty_classroom:

                # atributos da sala sendo analisada
                capacidade_sala_aux = classroom.capacidade_sala
                bloco_aux = classroom.nome_sala.split('-')[0]
                detailed_type_aux = classroom.tipo_detalhado
                status = classroom.status

                # verificando se é um numero valido
                try:
                    int(capacidade_sala_aux)
                except:
                    continue

                if len(list_aux) >= 1:
                    break

                # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
                key = f"{classroom_name},{subject_name},{day},{start_hour}"
                key = key.upper()

                # verifica utilizando o bloco
                if capacidade_sala_aux > capacidade_esperada and key not in dict_retorna_sugestao.keys() \
                        and f"{classroom_name},{column}" not in repeated_classrooms and status == 'Ativa' \
                        and bloco == bloco_aux and detailed_type == detailed_type_aux:
                    # não repetir sugestão
                    repeated_classrooms.append(f"{classroom_name},{column}")
                    list_aux.append(classroom)
                    dict_retorna_sugestao[key] = classroom

        # todo 3 verificação
        # so verificar o tipo detalhado
        for classroom in list_empty_classroom:

            # atributos da sala sendo analisada
            capacidade_sala_aux = classroom.capacidade_sala
            detailed_type_aux = classroom.tipo_detalhado
            status = classroom.status

            # verificando se é um numero valido
            try:
                int(capacidade_sala_aux)
            except:
                continue

            if len(list_aux) >= 1:
                break

            # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
            key = f"{classroom_name},{subject_name},{day},{start_hour}"
            key = key.upper()

            # verifica utilizando o bloco
            if capacidade_sala_aux > capacidade_esperada and key not in dict_retorna_sugestao.keys() \
                    and f"{classroom_name},{column}" not in repeated_classrooms and status == 'Ativa' \
                    and detailed_type == detailed_type_aux:
                # não repetir sugestão
                repeated_classrooms.append(f"{classroom_name},{column}")
                list_aux.append(classroom)
                dict_retorna_sugestao[key] = classroom

        # todo 4 verificação
        # verificar o bloco atual e o tipo
        for classroom in list_empty_classroom:

            # atributos da sala sendo analisada
            capacidade_sala_aux = classroom.capacidade_sala
            bloco_aux = classroom.nome_sala.split('-')[0]
            type_aux = classroom.tipo
            status = classroom.status

            # verificando se é um numero valido
            try:
                int(capacidade_sala_aux)
            except:
                continue

            if len(list_aux) >= 1:
                break

            # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
            key = f"{classroom_name},{subject_name},{day},{start_hour}"
            key = key.upper()

            # verifica utilizando o bloco
            if capacidade_sala_aux > capacidade_esperada and key not in dict_retorna_sugestao.keys() \
                    and f"{classroom_name},{column}" not in repeated_classrooms and status == 'Ativa' \
                    and bloco == bloco_aux and type == type_aux:
                # não repetir sugestão
                repeated_classrooms.append(f"{classroom_name},{column}")
                list_aux.append(classroom)
                dict_retorna_sugestao[key] = classroom

        # todo 5 verificação
        # verificando bloco prioridade da escola e tipo
        for numero_bloco in list_blocos:

            if numero_bloco <= 9:
                bloco = f"Bloco 0{numero_bloco} "
            else:
                bloco = f"Bloco {numero_bloco} "

            for classroom in list_empty_classroom:

                # atributos da sala sendo analisada
                capacidade_sala_aux = classroom.capacidade_sala
                bloco_aux = classroom.nome_sala.split('-')[0]
                type_aux = classroom.tipo
                status = classroom.status

                # verificando se é um numero valido
                try:
                    int(capacidade_sala_aux)
                except:
                    continue

                if len(list_aux) >= 1:
                    break

                # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
                key = f"{classroom_name},{subject_name},{day},{start_hour}"
                key = key.upper()

                # verifica utilizando o bloco
                if capacidade_sala_aux > capacidade_esperada and key not in dict_retorna_sugestao.keys() \
                        and f"{classroom_name},{column}" not in repeated_classrooms and status == 'Ativa' \
                        and bloco == bloco_aux and type == type_aux:
                    # não repetir sugestão
                    repeated_classrooms.append(f"{classroom_name},{column}")
                    list_aux.append(classroom)
                    dict_retorna_sugestao[key] = classroom

        # todo 6 verificação
        # verificar o tipo
        for classroom in list_empty_classroom:

            # atributos da sala sendo analisada
            capacidade_sala_aux = classroom.capacidade_sala
            type_aux = classroom.tipo
            status = classroom.status

            # verificando se é um numero valido
            try:
                int(capacidade_sala_aux)
            except:
                continue

            if len(list_aux) >= 1:
                break

            # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
            key = f"{classroom_name},{subject_name},{day},{start_hour}"
            key = key.upper()

            # verifica utilizando o bloco
            if capacidade_sala_aux > capacidade_esperada and key not in dict_retorna_sugestao.keys() \
                    and f"{classroom_name},{column}" not in repeated_classrooms and status == 'Ativa' \
                    and type == type_aux:
                # não repetir sugestão
                repeated_classrooms.append(f"{classroom_name},{column}")
                list_aux.append(classroom)
                dict_retorna_sugestao[key] = classroom

        # todo 7 verificação
        # sem verificação verificar
        for classroom in list_empty_classroom:

            # atributos da sala sendo analisada
            capacidade_sala_aux = classroom.capacidade_sala
            status = classroom.status

            # verificando se é um numero valido
            try:
                int(capacidade_sala_aux)
            except:
                continue

            if len(list_aux) >= 1:
                break

            # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
            key = f"{classroom_name},{subject_name},{day},{start_hour}"
            key = key.upper()

            # verifica utilizando o bloco
            if capacidade_sala_aux > capacidade_esperada and key not in dict_retorna_sugestao.keys() \
                    and f"{classroom_name},{column}" not in repeated_classrooms and status == 'Ativa':
                # não repetir sugestão
                repeated_classrooms.append(f"{classroom_name},{column}")
                list_aux.append(classroom)
                dict_retorna_sugestao[key] = classroom

    return dict_retorna_sugestao


def analyze_matriz_list(matriz, df_capacidade_excedida, dict_retorna_status_type, dict_retorna_prioridade_escola):
    m = np.array(matriz)
    row_number, column_number = m.shape

    dict_retorna_sugestao_lista = {}

    for data in df_capacidade_excedida.iterrows():
        # não repetir sugestão na mesma lista de sugestões
        repeated_classrooms = []

        # lista de salas vazias
        list_empty_classroom = []

        # pegar o numero da coluna
        day = data[1]["Dia da Semana"]
        start_hour = data[1]["Horário de início"]

        column = get_indice_analyze(day, start_hour)

        # atributos sala atual
        # capacidade esperada
        capacidade_esperada = data[1]["Matriculados"]
        # key
        classroom_name = data[1]["Sala"]
        bloco = classroom_name.split('-')[0]
        subject_name = data[1]["Nome disciplina"]
        division = data[1]["Divisão"]
        try:
            type = dict_retorna_status_type[classroom_name][1]
            detailed_type = dict_retorna_status_type[classroom_name][2]
        except:
            type = " "
            detailed_type = " "

        for row_aux in range(0, row_number):
            if matriz[row_aux][column] == "         ":
                list_empty_classroom.append(matriz[row_aux][0])

        # ordenando em ordem crescente a lista
        list_empty_classroom = sorted(list_empty_classroom, key=lambda x: x.capacidade_sala)

        # armazenando lista de prioridades da escola
        try:
            list_blocos = dict_retorna_prioridade_escola[data[1]["Escola"]]
        except:
            continue

        # lista que vai ser inserida como sugestão
        list_aux = []

        # todo 1 verificação
        # verificar o bloco atual e o tipo detalhado
        for classroom in list_empty_classroom:

            # atributos da sala sendo analisada
            capacidade_sala_aux = classroom.capacidade_sala
            bloco_aux = classroom.nome_sala.split('-')[0]
            detailed_type_aux = classroom.tipo_detalhado
            status = classroom.status

            # verificando se é um numero valido
            try:
                int(capacidade_sala_aux)
            except:
                continue

            # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
            key = f"{classroom_name},{subject_name},{day},{start_hour}"
            key = key.upper()

            if len(list_aux) >= 5:
                break

            if capacidade_sala_aux > capacidade_esperada and bloco == bloco_aux and \
                    classroom.nome_sala not in repeated_classrooms \
                    and status == 'Ativa' and detailed_type == detailed_type_aux:
                repeated_classrooms.append(classroom.nome_sala)
                list_aux.append(classroom)
                dict_retorna_sugestao_lista[key] = list_aux

        # todo 2 verificação
        # veriricar o bloco prioridade da escola e o tipo detalhado
        for numero_bloco in list_blocos:

            if numero_bloco <= 9:
                bloco = f"Bloco 0{numero_bloco} "
            else:
                bloco = f"Bloco {numero_bloco} "

            for classroom in list_empty_classroom:

                # atributos da sala sendo analisada
                capacidade_sala_aux = classroom.capacidade_sala
                bloco_aux = classroom.nome_sala.split('-')[0]
                detailed_type_aux = classroom.tipo_detalhado
                status = classroom.status

                # verificando se é um numero valido
                try:
                    int(capacidade_sala_aux)
                except:
                    continue

                # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
                key = f"{classroom_name},{subject_name},{day},{start_hour}"
                key = key.upper()

                if len(list_aux) >= 5:
                    break

                if capacidade_sala_aux > capacidade_esperada and bloco == bloco_aux and \
                        classroom.nome_sala not in repeated_classrooms \
                        and status == 'Ativa' and detailed_type == detailed_type_aux:
                    repeated_classrooms.append(classroom.nome_sala)
                    list_aux.append(classroom)
                    dict_retorna_sugestao_lista[key] = list_aux

        # todo 3 verificação
        # verificar o tipo detalhado
        for classroom in list_empty_classroom:

            # atributos da sala sendo analisada
            capacidade_sala_aux = classroom.capacidade_sala
            detailed_type_aux = classroom.tipo_detalhado
            status = classroom.status

            # verificando se é um numero valido
            try:
                int(capacidade_sala_aux)
            except:
                continue

            # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
            key = f"{classroom_name},{subject_name},{day},{start_hour}"
            key = key.upper()

            if len(list_aux) >= 5:
                break

            if capacidade_sala_aux > capacidade_esperada and \
                    classroom.nome_sala not in repeated_classrooms \
                    and status == 'Ativa' and detailed_type == detailed_type_aux:
                repeated_classrooms.append(classroom.nome_sala)
                list_aux.append(classroom)
                dict_retorna_sugestao_lista[key] = list_aux

        # todo 4 verificação
        # verificar o bloco atual e o tipo
        for classroom in list_empty_classroom:

            # atributos da sala sendo analisada
            capacidade_sala_aux = classroom.capacidade_sala
            status = classroom.status
            type_aux = classroom.tipo
            bloco_aux = classroom.nome_sala.split('-')[0]

            # verificando se é um numero valido
            try:
                int(capacidade_sala_aux)
            except:
                continue

            # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
            key = f"{classroom_name},{subject_name},{day},{start_hour}"
            key = key.upper()

            if len(list_aux) >= 5:
                break

            if capacidade_sala_aux > capacidade_esperada and \
                    classroom.nome_sala not in repeated_classrooms \
                    and status == 'Ativa' \
                    and bloco == bloco_aux \
                    and type == type_aux:
                repeated_classrooms.append(classroom.nome_sala)
                list_aux.append(classroom)
                dict_retorna_sugestao_lista[key] = list_aux

        # todo 5 verificação
        # verificar o bloco prioridade da escola e o tipo
        for numero_bloco in list_blocos:

            if numero_bloco <= 9:
                bloco = f"Bloco 0{numero_bloco} "
            else:
                bloco = f"Bloco {numero_bloco} "

            for classroom in list_empty_classroom:

                # atributos da sala sendo analisada
                capacidade_sala_aux = classroom.capacidade_sala
                bloco_aux = classroom.nome_sala.split('-')[0]
                type_aux = classroom.tipo
                status = classroom.status

                # verificando se é um numero valido
                try:
                    int(capacidade_sala_aux)
                except:
                    continue

                # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
                key = f"{classroom_name},{subject_name},{day},{start_hour}"
                key = key.upper()

                if len(list_aux) >= 5:
                    break

                if capacidade_sala_aux > capacidade_esperada and bloco == bloco_aux and \
                        classroom.nome_sala not in repeated_classrooms \
                        and status == 'Ativa' and type == type_aux:
                    repeated_classrooms.append(classroom.nome_sala)
                    list_aux.append(classroom)
                    dict_retorna_sugestao_lista[key] = list_aux

        # todo 6 verificação
        # verificar o tipo
        for classroom in list_empty_classroom:

            # atributos da sala sendo analisada
            capacidade_sala_aux = classroom.capacidade_sala
            status = classroom.status
            type_aux = classroom.tipo

            # verificando se é um numero valido
            try:
                int(capacidade_sala_aux)
            except:
                continue

            # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
            key = f"{classroom_name},{subject_name},{day},{start_hour}"
            key = key.upper()

            if len(list_aux) >= 5:
                break

            if capacidade_sala_aux > capacidade_esperada and \
                    classroom.nome_sala not in repeated_classrooms \
                    and status == 'Ativa' \
                    and type == type_aux:
                repeated_classrooms.append(classroom.nome_sala)
                list_aux.append(classroom)
                dict_retorna_sugestao_lista[key] = list_aux

        # todo 7 verificação
        # sem verificação
        for classroom in list_empty_classroom:

            # atributos da sala sendo analisada
            capacidade_sala_aux = classroom.capacidade_sala
            status = classroom.status

            # verificando se é um numero valido
            try:
                int(capacidade_sala_aux)
            except:
                continue

            # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
            key = f"{classroom_name},{subject_name},{day},{start_hour}"
            key = key.upper()

            if len(list_aux) >= 5:
                break

            if capacidade_sala_aux > capacidade_esperada and \
                    classroom.nome_sala not in repeated_classrooms \
                    and status == 'Ativa':
                repeated_classrooms.append(classroom.nome_sala)
                list_aux.append(classroom)
                dict_retorna_sugestao_lista[key] = list_aux

    return dict_retorna_sugestao_lista


def analyze_matriz_subutilizada(matriz, df_capacidade_excedida, dict_retorna_status_type,
                                dict_retorna_prioridade_escola):
    m = np.array(matriz)
    row_number, column_number = m.shape

    dict_retorna_sugestao_subutilizada = {}

    for data in df_capacidade_excedida.iterrows():

        # não repetir sugestão na mesma lista de sugestões
        repeated_classrooms = []

        # lista de salas vazias
        list_underused_classroom = []

        # pegar o numero da coluna
        day = data[1]["Dia da Semana"]
        start_hour = data[1]["Horário de início"]

        column = get_indice_analyze(day, start_hour)

        # atributos sala atual
        # capacidade esperada
        capacidade_esperada = data[1]["Matriculados"]
        # key
        classroom_name = data[1]["Sala"]
        bloco = classroom_name.split("-")[0]
        subject_name = data[1]["Nome disciplina"]

        try:
            type = dict_retorna_status_type[classroom_name][1]
            detailed_type = dict_retorna_status_type[classroom_name][2]
        except:
            type = " "
            detailed_type = " "

        # buscando as opções na matriz
        #      verificando se esta vazio e se sua capacidade atinge menos de 30%
        disciplina = {}
        for row_aux in range(0, row_number):
            if matriz[row_aux][column] != "         " \
                    and matriz[row_aux][column].porcentagem_utilizacao < 50:
                disciplina[matriz[row_aux][0]] = matriz[row_aux][column]
                list_underused_classroom.append(matriz[row_aux][0])

        # lista que vai ser inserida como sugestão
        list_aux = []

        # ordenando em ordem crescente a lista
        list_underused_classroom = sorted(list_underused_classroom, key=lambda x: x.capacidade_sala)

        # armazenando a prioridade da escola
        try:
            list_blocos = dict_retorna_prioridade_escola[data[1]["Escola"]]
        except:
            list_blocos = []

        # todo 1 verificação
        # veriricando o bloco atual e o tipo detalhado
        for classroom in list_underused_classroom:

            # atributos da sala sendo analisada
            capacidade_sala_aux = classroom.capacidade_sala
            bloco_aux = classroom.nome_sala.split('-')[0]
            detailed_type_aux = classroom.tipo_detalhado
            status = classroom.status

            #ignorando salas sem tipo detalhado definido
            if detailed_type_aux == "Não especificado na planilha de infra." or detailed_type_aux == "Sala não esta planilha de infra.":
                continue

            # verificando se é um numero valido
            try:
                int(capacidade_sala_aux)
            except:
                continue

            # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
            key = f"{classroom_name},{subject_name},{day},{start_hour}"
            key = key.upper()

            if len(list_aux) >= 5:
                break

            if capacidade_sala_aux > capacidade_esperada and bloco == bloco_aux and \
                    classroom.nome_sala not in repeated_classrooms \
                    and status == 'Ativa' and detailed_type == detailed_type_aux:
                repeated_classrooms.append(classroom.nome_sala)

                valor = f"{classroom.nome_sala},{classroom.capacidade_sala},{disciplina[classroom].alunos_matriculados},{type}"

                sala_subutilizada = Subutilizada(classroom,disciplina[classroom])
                list_aux.append(sala_subutilizada)
                dict_retorna_sugestao_subutilizada[key] = list_aux

        # todo 2 verificação
        # verificando o bloco prioridade da escola e o tipo detalhado
        for numero_bloco in list_blocos:

            if numero_bloco <= 9:
                bloco = f"Bloco 0{numero_bloco} "
            else:
                bloco = f"Bloco {numero_bloco} "

            # utilizando o bloco para validar
            for classroom in list_underused_classroom:

                # atributos da sala sendo analisada
                capacidade_sala_aux = classroom.capacidade_sala
                bloco_aux = classroom.nome_sala.split('-')[0]
                detailed_type_aux = classroom.tipo_detalhado
                status = classroom.status

                # ignorando salas sem tipo detalhado definido
                if detailed_type_aux == "Não especificado na planilha de infra." or detailed_type_aux == "Sala não esta planilha de infra.":
                    continue

                # verificando se é um numero valido
                try:
                    int(capacidade_sala_aux)
                except:
                    continue

                # key = nome da sala, nome da disciplina, dia, hora inicio, divisao
                key = f"{classroom_name},{subject_name},{day},{start_hour}"
                key = key.upper()

                if len(list_aux) >= 5:
                    break

                if capacidade_sala_aux > capacidade_esperada and bloco == bloco_aux and \
                        classroom.nome_sala not in repeated_classrooms \
                        and status == 'Ativa' and detailed_type == detailed_type_aux:
                    repeated_classrooms.append(classroom.nome_sala)

                    valor = f"{classroom.nome_sala},{classroom.capacidade_sala},{disciplina[classroom].alunos_matriculados},{type}"
                    sala_subutilizada = Subutilizada(classroom, disciplina[classroom])
                    list_aux.append(sala_subutilizada)
                    dict_retorna_sugestao_subutilizada[key] = list_aux

    return dict_retorna_sugestao_subutilizada


def create_dict_prioridade_escola(caminho_aux):
    df_prioridades = pandas.read_excel(f'{caminho_aux}/Prioridade_escolas.xlsx')
    dict_retorna_prioridade_escola = {}
    for data in df_prioridades.iterrows():
        list_aux = []
        escola = data[1]['Escola']

        for prioridade in range(1, 12):
            prioridade = str(prioridade)
            try:
                bloco = int(data[1][prioridade])
            except:
                break
            list_aux.append(bloco)

        dict_retorna_prioridade_escola[escola] = list_aux
    return dict_retorna_prioridade_escola


def main(nome_arquivo, arquivo_capacidade,caminho_aux):
    # dicts
    dict_retorna_sugestao = {}
    dict_retorna_sugestao_subutilizada = {}
    dict_retorna_sugestao_list = {}
    dict_retorna_escola = {}
    dict_retorna_prioridade_escola = {}
    dict_retorna_utilizado_graduacao = {}

    # lista dos objetos
    list_objects = []

    # dict utioizado para retornar o status da planilha de capacidade
    dict_retorna_status_type, dict_retorna_utilizado_graduacao = create_dict_status_type(arquivo_capacidade,
                                                                                         dict_retorna_utilizado_graduacao)

    # dict para retornar os blocos prioritarios de cada escola
    dict_retorna_prioridade_escola = create_dict_prioridade_escola(caminho_aux)

    list_objects, dict_retorna_escola = create_objects(nome_arquivo, dict_retorna_status_type, list_objects,
                                                       dict_retorna_utilizado_graduacao)

    df_completo = pandas.read_excel(nome_arquivo, sheet_name='Completo')

    df_problemas = df_completo[(df_completo['Análise Capacidade'] == "Capacidade excedida") |
                               (df_completo['Análise Capacidade'] == "Sem Capacidade") |
                               (df_completo['Análise Capacidade'] == "Sala lotada") |
                               (df_completo['Análise Capacidade'] == "Sem sala") &
                               (df_completo['Dia da Semana'] != "Flutuante")]


    df_problemas = df_problemas[df_problemas['Sala'].str.contains('AULA EXTERNA') == False]

    list_objects += create_objects_capacidade(arquivo_capacidade, list_objects, dict_retorna_escola)
    matriz = insert_matriz(list_objects)

    # retorna uma sugestão, sem repetir a sugestão
    print('Criando sugestão...')
    dict_retorna_sugestao = analyze_matriz(matriz, df_problemas, dict_retorna_status_type,
                                           dict_retorna_prioridade_escola)

    # retorna uma sugestão, utilizando salas que so usam 30% ou menos de sua capacidade
    print('Criando lista de subutilizadas...')
    dict_retorna_sugestao_subutilizada = analyze_matriz_subutilizada(matriz, df_problemas,
                                                                     dict_retorna_status_type,
                                                                     dict_retorna_prioridade_escola)

    # retorna um top 5 de sugestões, repetindo sugestão se necessario
    print('Criando lista de sugestões...')
    dict_retorna_sugestao_list = analyze_matriz_list(matriz, df_problemas, dict_retorna_status_type,
                                                     dict_retorna_prioridade_escola)

    print('Inserindo no excel...')
    insert_excel(nome_arquivo, dict_retorna_sugestao, dict_retorna_sugestao_list, dict_retorna_sugestao_subutilizada)
    print("Arquivo gerado com sucesso.")

if __name__ == '__main__':

    main()
