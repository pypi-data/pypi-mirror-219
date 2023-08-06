from tkinter import Tk
from tkinter.filedialog import askopenfilename
from datetime import datetime as dt
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


def encontra_periodo(cod_turma):
    if 'LIBRAS' in cod_turma:
        return '8' if 'CSSC' in cod_turma else '10'
    if 'LEA' in cod_turma:
        return '3' if 'LDN' in cod_turma else '2'
    if 'CIDE' in cod_turma:
        return '1'
    if '-' not in cod_turma:
        return ''

    cod_turma = cod_turma.split('-')[1].strip()
    periodo = ''
    for ch in cod_turma:
        if ch in '0123456789':
            periodo += ch
        else:
            break
    return periodo


def encontra_cr(turma, dict_sigla_cr):
    if '-' not in turma:
        return ''
    else:
        if 'LEA' in turma or 'LIBRAS' in turma:
            sigla = turma.split('-')[0].strip()
            validador = sigla
        else:
            turno = turma.split('-')[2].strip()
            sigla = turma.split('-')[0].strip()
            validador = sigla + ' ' + turno
        return dict_sigla_cr.get(validador, '')


def encontra_curso(cod_turma, dict_sigla_curso):
    cod_turma = cod_turma.split('-')[0].strip()
    curso = dict_sigla_curso.get(cod_turma, '')
    return curso


def encontra_escola(cod_turma, dict_sigla_escola):
    cod_turma = cod_turma.split('-')[0].strip()
    escola = dict_sigla_escola.get(cod_turma, '')
    return escola


def trata_turma(arquivo, coluna):
    for i in range(len(arquivo)):
        if 'INTERCAMBIO' in arquivo[i] or 'ISOLADAS' in arquivo[i]:
            turma = arquivo[i].split(' ')
        else:
            turma = arquivo[i].split('-')
        if coluna == 'CR Curso' \
                and 'LEA' not in arquivo[i] \
                and 'LIBRAS' not in arquivo[i] \
                and 'LETTC' not in arquivo[i] \
                and 'INTERCAMBIO' not in arquivo[i] \
                and 'ISOLADAS' not in arquivo[i]:
            sigla = f'{turma[0].strip()} {turma[2].strip()}'
        else:
            sigla = f'{turma[0].strip()}'
        arquivo[i] = sigla
    return arquivo


def valida_eletivas(df, colunas):
    ndf = df
    ndf[colunas[0]] = trata_turma(df[colunas[0]], colunas[1]).astype(dtype='str', errors='ignore')
    ndf = ndf.drop_duplicates().reset_index(drop=True)
    return ndf


def sigla_cr_curso(dados):
    dict_turmas = {}
    colunas = dados.columns.values.tolist()
    info = dados.sort_values(by=[colunas[0], colunas[1]])
    info[colunas[-1]] = info[colunas[-1]].fillna(0).astype(dtype='int', errors='ignore') \
        .astype(dtype='str', errors='ignore')
    info = info.drop_duplicates().reset_index(drop=True)
    eletivas = ['U1', 'U2', 'U3']
    info_eletivas = valida_eletivas(info[info[colunas[0]].str.contains('|'.join(eletivas))]
                                    .reset_index(drop=True), colunas)
    info = info[~info[colunas[0]].str.contains('|'.join(eletivas))].reset_index(drop=True)
    info[colunas[0]] = trata_turma(info[colunas[0]], colunas[1]).astype(dtype='str', errors='ignore')
    info = info.drop_duplicates().reset_index(drop=True)
    for index, row in info_eletivas.iterrows():
        if info_eletivas[colunas[0]][index] not in info[colunas[0]].values:
            valor = info_eletivas[colunas[0]][index]
            info_faltante = info_eletivas[info_eletivas[colunas[0]].str.contains(valor)]
            info = pd.concat([info, info_faltante], ignore_index=True)
    info = info.loc[(info[colunas[-1]] != ' ') & (info[colunas[-1]] != '0')].reset_index(drop=True)
    for index, row in info.iterrows():
        dict_turmas[info[colunas[0]][index]] = info[colunas[1]][index]
        if colunas[1] == 'Curso':
            if info[colunas[1]][index] == 'Multicom' or \
                    info[colunas[1]][index] == 'Humanidades' or \
                    info[colunas[1]][index] == 'Engenharia':
                cr = info[colunas[-1]][index]
                curso = info.loc[(info[colunas[-1]] == cr) & (info[colunas[1]] != info[colunas[1]][index])]
                dict_turmas[info[colunas[0]][index]] = curso[colunas[1]].to_list()[0]
    return dict_turmas


# Utiliza: CH-Turma_Prof (Curso) + Pais Exportação (Escola)
def sigla_escola(df_curso, df_escola):
    dict_escola = {}
    escola = df_escola.sort_values(by=['Estabelecimento', 'Escola', 'Turma']) \
        .drop_duplicates().reset_index(drop=True)
    escola['Turma'] = trata_turma(escola['Turma'], '').astype(dtype='str', errors='ignore')
    escola = escola.drop_duplicates().reset_index(drop=True)
    escola['Escola'] = escola['Escola'] \
        .str.replace('Escola de ', '') \
        .str.replace('Escola ', '')
    escola['Estabelecimento'] = escola['Estabelecimento'].str.replace(
        'Pontifícia Universidade Católica do Paraná - ', '')
    curso = df_curso.sort_values(by=['Turma', 'Curso']).drop_duplicates().reset_index(drop=True)
    curso['Turma'] = trata_turma(curso['Turma'], '').astype(dtype='str', errors='ignore')
    curso = curso.drop_duplicates().reset_index(drop=True)
    curso.rename(columns={'Curso': 'Escola'}, inplace=True)
    for index, row in curso.iterrows():
        valida_curso = curso['Escola'][index]
        if valida_curso == 'Identidade':
            dict_escola[curso['Turma'][index]] = 'Administração da Diretoria de Relações Internas'
        elif valida_curso == 'Engenharia':
            dict_escola[curso['Turma'][index]] = 'Politécnica'
        elif valida_curso == 'Multicom':
            dict_escola[curso['Turma'][index]] = 'Belas Artes'
        elif valida_curso == 'Humanidades' or 'LEA' in curso['Turma'][index]:
            dict_escola[curso['Turma'][index]] = 'Educação e Humanidades'
        elif curso['Turma'][index] == 'LDN':
            dict_escola[curso['Turma'][index]] = 'Londrina'
        elif curso['Turma'][index] == 'TLD':
            dict_escola[curso['Turma'][index]] = 'Toledo'
        else:
            info = escola.loc[(escola['Turma'] == curso['Turma'][index])].reset_index(drop=True)
            if info.empty:
                info.loc[0] = ['', '', '']
            if (info['Estabelecimento'][0] == 'Londrina'
                    or info['Estabelecimento'][0] == 'Maringá'
                    or info['Estabelecimento'][0] == 'Toledo'):
                dict_escola[curso['Turma'][index]] = info['Estabelecimento'][0]
            elif (info['Escola'][0] == 'Ciências da Vida'
                  or info['Escola'][0] == 'Medicina'):
                dict_escola[curso['Turma'][index]] = 'Medicina e Ciências da Vida'
            else:
                dict_escola[curso['Turma'][index]] = info['Escola'][0]
    return dict_escola


def trata_relatorio_ch(arquivo):
    # -- CH na Base Ouro --
    # Adiciona ch relogio oficial na base ouro
    # professor — carga horária por disciplina.xlsx
    # validador base ouro = cr disciplina + turma + disciplina
    # validador = cr + turma + disciplina

    df = arquivo[['CR Curso', 'Turma', 'Disciplina', 'C.H. Relógio Oficial']]
    df['CR Curso'] = pd.to_numeric(df['CR Curso'], errors='coerce')

    df['CR Curso'] = df['CR Curso'].fillna(0.0).astype(int)

    df.insert(0, 'Validador', '', True)
    df['Validador'] = df.apply(lambda row: f"{str(row['CR Curso']).strip()}    "
                                           f"{str(row['Turma']).strip()}    "
                                           f"{str(row['Disciplina']).strip()}",
                               axis=1)

    df = df[['Validador', 'C.H. Relógio Oficial']]

    return df


def filtra_alunos(df):
    ndf = df.loc[:, ('Estabelecimento', 'Matrícula', 'Nome Completo', 'Turma Aluno', 'DT_CADASTRO_CONTRATO')] \
        .sort_values(by=['Matrícula', 'Turma Aluno', 'DT_CADASTRO_CONTRATO']).drop_duplicates().reset_index(drop=True)
    c = ndf.loc[:, ('Matrícula', 'Turma Aluno', 'Estabelecimento')].groupby('Matrícula').value_counts()
    incorretos = []
    index = c.index.tolist()
    valores = c.tolist()
    for i in range(len(c.index)):
        if valores[i] >= 2:
            tdf = ndf.loc[ndf['Matrícula'] == index[i][0]].sort_values(by='DT_CADASTRO_CONTRATO').reset_index(drop=True)
            for item in range(len(tdf.index)):
                if tdf['DT_CADASTRO_CONTRATO'][item] != tdf['DT_CADASTRO_CONTRATO'].iat[-1]:
                    incorretos.append(f"{str(tdf['Matrícula'][item]).strip()} "
                                      f"{str(tdf['Turma Aluno'][item].strip())} "
                                      f"{str(tdf['DT_CADASTRO_CONTRATO'][item]).strip()}")
    df.insert(0, 'Validador', '', True)
    df['Validador'] = df.apply(lambda row: f"{str(row['Matrícula']).strip()} "
                                           f"{str(row['Turma Aluno']).strip()} "
                                           f"{str(row['DT_CADASTRO_CONTRATO']).strip()}",
                               axis=1)
    if len(incorretos) > 0:
        df = df[~df['Validador'].str.contains('|'.join(incorretos))].reset_index(drop=True)
    del df['Validador']
    return df


# Relatórios: Alunos/Pais Exportação; Alunos Matriculados por Disciplin; Professor - CH Turma Disciplina
def recebe_arquivos(alunos, disciplinas, ch, name):
    print('Gerando a base ouro...')

    # Relatório Alunos Pais Exportação
    df_alunos = pd.read_excel(alunos)

    df_alunos = df_alunos[[
        'Estabelecimento', 'Escola', 'Centro de Resultado', 'Curso', 'Série', 'Matrícula',
        'Nome Completo', 'CPF', 'Data de Nascimento', 'Usuário Internet', 'E-mail', 'Telefone Celular',
        'Situação Acadêmica', 'Tipo de Entrada', 'Tipo de Ingresso', 'Turma', 'Turno', 'Gênero'
    ]]
    df_alunos = df_alunos.loc[df_alunos["Situação Acadêmica"] == 'Matriculado Curso Normal']
    df_alunos = df_alunos.drop_duplicates()

    # Relatóio Disicplinas SQL
    df_disciplinas = pd.read_excel(disciplinas)
    df_disciplinas = df_disciplinas[[
        'CODIGO', 'DT_CADASTRO_CONTRATO', 'TURMA_BASE', 'DISCIPLINA', 'TURMA_DISCIPLINA', 'DIVISAO', 'DIVISAO2'
    ]]
    df_disciplinas = df_disciplinas.drop_duplicates()

    # Relatório CH Turma
    df_ch = pd.read_excel(ch)
    # Dicionário de cr
    dict_sigla_cr = sigla_cr_curso(df_ch.loc[:, ('Turma', 'CR Curso')])
    # Dicionário de curso
    dict_sigla_curso = sigla_cr_curso(df_ch.loc[:, ('Turma', 'Curso', 'CR Curso')])
    # Dicionário de escola
    dict_sigla_escola = sigla_escola(df_ch.loc[:, ('Curso', 'Turma')],
                                     df_alunos.loc[:, ('Turma', 'Escola', 'Estabelecimento')])
    df_ch = trata_relatorio_ch(df_ch)

    print('Juntando dados...')

    df_joined = pd.merge(
        left=df_alunos, right=df_disciplinas, left_on=['Matrícula', 'Turma'], right_on=['CODIGO', 'TURMA_BASE']
    )

    # modificando o dataframe
    df_joined = df_joined[['Estabelecimento', 'Escola', 'Centro de Resultado', 'Curso', 'Série', 'Matrícula',
                           'Nome Completo', 'CPF', 'Data de Nascimento', 'Usuário Internet', 'E-mail',
                           'Telefone Celular', 'Situação Acadêmica', 'Tipo de Entrada', 'Tipo de Ingresso',
                           'Turma', 'Turno', 'Gênero',
                           # dados disciplina
                           'DT_CADASTRO_CONTRATO', 'DISCIPLINA', 'TURMA_DISCIPLINA', 'DIVISAO', 'DIVISAO2']]

    df_joined.rename(columns={
        'Série': 'Período Aluno',
        'Turma': 'Turma Aluno',
        'Centro de Resultado': 'CR Aluno',
        'Curso': 'Curso Aluno',
        'Usuário Internet': 'E-mail Institucional',
        'Disciplina': 'DISCIPLINA',
        'Turma Destino': 'TURMA_DISCIPLINA',
    }, inplace=True)

    print('Calculando...')

    df_joined['E-mail Institucional'] = df_joined.apply(
        lambda row: f"{row['E-mail Institucional']}@pucpr.edu.br",
        axis=1)

    df_joined.insert(18, 'Escola Disciplina', '', True)
    df_joined['Escola Disciplina'] = df_joined.apply(
        lambda row: encontra_escola(row['TURMA_DISCIPLINA'], dict_sigla_escola),
        axis=1)

    df_joined.insert(19, 'Curso_Disciplina', '', True)
    df_joined['Curso_Disciplina'] = df_joined.apply(
        lambda row: encontra_curso(row['TURMA_DISCIPLINA'], dict_sigla_curso),
        axis=1)

    df_joined.insert(20, 'Período_Disciplina', '', True)
    df_joined['Período_Disciplina'] = df_joined.apply(
        lambda row: encontra_periodo(row['TURMA_DISCIPLINA']),
        axis=1)

    df_joined.insert(21, 'CR_Disciplina', '', True)
    df_joined['CR_Disciplina'] = df_joined.apply(
        lambda row: encontra_cr(row['TURMA_DISCIPLINA'], dict_sigla_cr),
        axis=1)

    # Remove o início do nome do estabelecimento
    df_joined['Estabelecimento'] = df_joined['Estabelecimento'].str.replace(
        'Pontifícia Universidade Católica do Paraná - ', '')

    # Remove o início do nome da escola
    df_joined['Escola'] = df_joined['Escola'] \
        .str.replace('Escola de ', '') \
        .str.replace('Escola ', '')

    # Corrige 'Belas Artes' E 'Medicina e Ciências da Vida'
    for escola in df_joined.itertuples():
        if (df_joined['Escola'][escola.Index] == 'Comunicação e Artes'
                or df_joined['Escola'][escola.Index] == 'Arquitetura e Design'):
            df_joined['Escola'][escola.Index] = 'Belas Artes'
        elif (df_joined['Escola'][escola.Index] == 'Ciências da Vida'
              or df_joined['Escola'][escola.Index] == 'Medicina'):
            df_joined['Escola'][escola.Index] = 'Medicina e Ciências da Vida'
        else:
            pass

    # Altera a escola para o nome do campus fora de sede
    df_joined.loc[
        (df_joined['Estabelecimento'] == 'Londrina') |
        (df_joined['Estabelecimento'] == 'Maringá') |
        (df_joined['Estabelecimento'] == 'Toledo'),
        'Escola'] = df_joined['Estabelecimento']

    # No período do aluno deixar só os números
    df_joined['Período Aluno'] = df_joined['Período Aluno'] \
        .str.replace('º Periodo', '') \
        .str.replace('º Período', '')

    # Preenche a coluna Gênero com "Não informado" quando estiver vazia
    df_joined["Gênero"].fillna("Não informado", inplace=True)

    # Remove espaços antes e depois dos nomes
    df_joined['Nome Completo'] = df_joined['Nome Completo'].str.strip()

    # Insere validador para a inclusão da coluna de carga horária
    df_joined.insert(0, 'Validador', '', True)
    df_joined['Validador'] = df_joined.apply(
        lambda row: f"{str(row['CR_Disciplina']).strip()}    "
                    f"{str(row['TURMA_DISCIPLINA']).strip()}    "
                    f"{str(row['DISCIPLINA']).strip()}",
        axis=1)

    df_joined = pd.merge(left=df_joined, right=df_ch, left_on='Validador', right_on='Validador', how='left')
    del df_joined['Validador']

    # Remove linhas duplicadas
    df_joined = df_joined.drop_duplicates()
    df_joined = filtra_alunos(df_joined)

    print('Criando arquivos de saída...')

    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(name, engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df_joined.to_excel(writer, sheet_name='Sheet1', index=False)

    print(f'Salvando arquivos em\n{name}')

    # Close the Pandas Excel writer and output the Excel file.
    writer.close()

    print('Geração de arquivos finalizada!')


if __name__ == '__main__':
    print('Selecione a Relação de Alunos/Pais Exportação')

    Tk().withdraw()
    relacao_alunos = askopenfilename(
        filetypes=[('Arquivo excel', '.xlsx')],
        title='Selecione a Relação de Alunos/Pais Exportação')
    print(f'    {relacao_alunos}')

    print('Selecione o relatório de Alunos Matriculados por Disciplina')

    relatorio_disciplinas = askopenfilename(
        filetypes=[('Arquivo excel', '.xlsx')],
        title='Selecione o relatório de Alunos Matriculados por Disciplina')
    print(f'    {relatorio_disciplinas}')

    print('Selecione o relatório de Professor - Carga Horária por Turma e Disciplina')

    relatorio_ch = askopenfilename(
        filetypes=[('Arquivo excel', '.xlsx')],
        title='Selecione o relatório de Professor - Carga Horária por Turma e Disciplina')
    print(f'    {relatorio_ch}')

    file_name = f'Base_ouro_completa_{dt.now().strftime("%Y%m%d_%Hh%M")}.xlsx'

    recebe_arquivos(relacao_alunos, relatorio_disciplinas, relatorio_ch, file_name)

# Identidade dica sempre no 1º período > Pode ser que mude ao longo dos semestres
