"""
This script contains functions used for data cleaning.
"""
import json
from datetime import datetime
from os.path import join
from os import listdir
import pandas as pd
import numpy as np
import maxia_pipedrive.api_handler.organizations
import maxia_pipedrive.api_handler.fields
import maxia_pipedrive.api_handler.users
import maxia_pipedrive.api_handler.stages
import maxia_pipedrive.models
import maxia_pipedrive.relations
import maxia_pipedrive.consts 

# PREPROCESSING MODULES


def preprocess_inep_data():
    in_csv = join(maxia_pipedrive.consts.Consts.microdados_dir, 'microdados_ed_basica_2021.csv')
    out_csv = join(maxia_pipedrive.consts.Consts.microdados_treated_dir,
                   'microdados_ed_basica_2021.csv')
    df = pd.read_csv(in_csv, sep=";", encoding='latin-1', low_memory=False)
    filtered_cols = [
        'NO_ENTIDADE', 'CO_ENTIDADE', 'NU_CNPJ_ESCOLA_PRIVADA',
        'NU_CNPJ_MANTENEDORA', 'CO_ESCOLA_SEDE_VINCULADA',
        'NU_TELEFONE',
        'NO_REGIAO', 'NO_UF', 'SG_UF', 'NO_MUNICIPIO',
        'DS_ENDERECO', 'NU_ENDERECO', 'DS_COMPLEMENTO',
        'NO_BAIRRO', 'CO_CEP',
        'QT_SALAS_UTILIZADAS_DENTRO', 'QT_SALAS_UTILIZA_CLIMATIZADAS',
        'QT_DESKTOP_ALUNO', 'QT_COMP_PORTATIL_ALUNO', 'QT_TABLET_ALUNO',
        'IN_INTERNET', 'IN_INTERNET_ALUNOS', 'IN_BANDA_LARGA',
        'QT_MAT_BAS', 'QT_MAT_INF', 'QT_MAT_FUND_AI',
        'QT_MAT_FUND_AF', 'QT_MAT_MED'  # , 'QT_MAT_PROF', 'QT_MAT_EJA', 'QT_MAT_ESP'
    ]

    # Filter Private Schools (TP_DEPENDENCIA == 4) and only active schools (TP_SITUACAO_FUNCIONAMENTO == 1)
    df_filtered = df[(df['TP_DEPENDENCIA'] == 4) & (
        df['TP_SITUACAO_FUNCIONAMENTO'] == 1)].reset_index(drop=True)
    # Fix number of students only "normal"
    df_filtered['QT_MAT_BAS'] = df_filtered[['QT_MAT_INF',
                                             'QT_MAT_FUND_AI', 'QT_MAT_FUND_AF', 'QT_MAT_MED']].sum(axis=1)

    # drop DDD Columns
    df_filtered['NU_TELEFONE'] = df_filtered.apply(lambda row: f"{int(row['NU_DDD'])} {int(row['NU_TELEFONE'])}" if not any([
                                                   pd.isna(row['NU_DDD']), pd.isna(row['NU_TELEFONE'])]) else '', axis=1)
    df_filtered.drop(columns=['NU_DDD'], inplace=True)

    # Filter columns
    df_filtered = df_filtered[filtered_cols].reset_index(drop=True)

    # Convert column types
    number_cols = [
        'CO_ENTIDADE', 'NU_CNPJ_ESCOLA_PRIVADA', 'NU_CNPJ_MANTENEDORA', 'CO_ESCOLA_SEDE_VINCULADA', 'QT_SALAS_UTILIZA_CLIMATIZADAS',
        'QT_DESKTOP_ALUNO', 'QT_COMP_PORTATIL_ALUNO', 'QT_TABLET_ALUNO', 'QT_MAT_BAS', 'QT_MAT_INF', 'QT_MAT_FUND_AI',
        'QT_MAT_FUND_AF', 'QT_MAT_MED']
    df_filtered[number_cols] = df_filtered[number_cols].astype('Int64')
    df_filtered.loc[df_filtered['NU_CNPJ_ESCOLA_PRIVADA']
                    == 99999999999999, 'NU_CNPJ_ESCOLA_PRIVADA'] = None
    df_filtered.loc[df_filtered['NU_CNPJ_MANTENEDORA']
                    == 99999999999999, 'NU_CNPJ_MANTENEDORA'] = None
    # True/False columns
    bool_cols = ['IN_INTERNET', 'IN_INTERNET_ALUNOS', 'IN_BANDA_LARGA']
    df_filtered[bool_cols] = df_filtered[bool_cols].astype(bool)
    # Create FULL ADDRESS FIELD and drop some columns
    address_cols_sorted = ['DS_ENDERECO', 'NU_ENDERECO',
                           'DS_COMPLEMENTO', 'NO_MUNICIPIO', 'NO_UF', 'CO_CEP']
    df_filtered[maxia_pipedrive.models.Organization.full_address] = df_filtered.fillna(False).apply(
        lambda row: ",".join([str(row[el])
                             for el in address_cols_sorted if row[el]]),
        axis=1
    )
    df_filtered.drop(columns=['DS_ENDERECO', 'NU_ENDERECO',
                     'DS_COMPLEMENTO', 'NO_UF'], inplace=True)

    # Add INEP number on organization name

    df_filtered['NO_ENTIDADE'] = df_filtered.apply(
        lambda row: f"{row['CO_ENTIDADE']} {row['NO_ENTIDADE']}",
        axis=1)

    list_count_seg = [
        'QT_MAT_INF', 'QT_MAT_FUND_AI',
        'QT_MAT_FUND_AF', 'QT_MAT_MED'  # ,
        # 'QT_MAT_PROF', 'QT_MAT_EJA', 'QT_MAT_ESP'
    ]
    list_segs = [
        "Educação Infantil",
        "Ensino Fundamental (Anos Iniciais)", "Ensino Fundamental (Anos Finais)",
        "Ensino Médio"]  # , "Educação Profissional", "EJA", "Educação Especial"]

    # Add Segmentos column
    df_filtered[maxia_pipedrive.models.Organization.segmentos] = df_filtered.fillna(0).apply(
        lambda row: ",".join(
            [seg
             for idx, seg in enumerate(list_segs)
             if row[list_count_seg[idx]] and int(row[list_count_seg[idx]]) > 0]
        ),
        axis=1)

    # Rename columns
    df_filtered.rename(columns={
        'NO_ENTIDADE': maxia_pipedrive.models.Organization.name,
        'CO_ENTIDADE': maxia_pipedrive.models.Organization.inep_number,
        'NU_CNPJ_ESCOLA_PRIVADA': maxia_pipedrive.models.Organization.cnpj,

        'NU_CNPJ_MANTENEDORA': maxia_pipedrive.models.Organization.cnpj_mantenedora,
        'CO_ESCOLA_SEDE_VINCULADA': maxia_pipedrive.models.Organization.inep_number_sede,

        'NU_TELEFONE': maxia_pipedrive.models.Organization.phone_number,

        'NO_REGIAO': maxia_pipedrive.models.Organization.custom_address_region,
        'SG_UF': maxia_pipedrive.models.Organization.custom_address_uf,
        'NO_MUNICIPIO': maxia_pipedrive.models.Organization.custom_address_city,
        'NO_BAIRRO': maxia_pipedrive.models.Organization.custom_address_neigh,
        'CO_CEP': maxia_pipedrive.models.Organization.custom_address_cep,

        'QT_SALAS_UTILIZADAS_DENTRO': maxia_pipedrive.models.Organization.n_rooms,
        'QT_SALAS_UTILIZA_CLIMATIZADAS': maxia_pipedrive.models.Organization.n_rooms_clim,
        'QT_DESKTOP_ALUNO': maxia_pipedrive.models.Organization.n_desktop,
        'QT_COMP_PORTATIL_ALUNO': maxia_pipedrive.models.Organization.n_notebook,
        'QT_TABLET_ALUNO': maxia_pipedrive.models.Organization.n_tablets,
        'IN_INTERNET': maxia_pipedrive.models.Organization.has_internet,
        'IN_BANDA_LARGA': maxia_pipedrive.models.Organization.has_banda_larga,

        'QT_MAT_BAS': maxia_pipedrive.models.Organization.n_students,
        'QT_MAT_INF': maxia_pipedrive.models.Organization.segmentos_n_inf,
        'QT_MAT_FUND_AI': maxia_pipedrive.models.Organization.segmentos_n_fund_1,
        'QT_MAT_FUND_AF': maxia_pipedrive.models.Organization.segmentos_n_fund_2,
        'QT_MAT_MED': maxia_pipedrive.models.Organization.segmentos_n_medio
        # ,
        # 'QT_MAT_PROF': Organization.segmentos_n_prof,
        # 'QT_MAT_EJA': Organization.segmentos_n_eja,
        # 'QT_MAT_ESP': Organization.segmentos_n_esp
    }, inplace=True)

    # Save
    df_filtered.to_csv(out_csv, sep=",", encoding='latin-1')


def preprocess_base():
    import re
    base_fpath = 'data/microdados/BASE_CLIENTES_2022_raw.csv'
    df_base = pd.read_csv(base_fpath, index_col=None)

    df_base[maxia_pipedrive.models.Organization.cnpj] = df_base[maxia_pipedrive.models.Organization.cnpj].apply(
        lambda el: int(re.sub("[^0-9]", "", el))).astype('Int64')  # .to_list()
    df_base.replace({
        55270557000134: 50320803000100,  # DOMINIQUE: 50320803000100
        17143269000120: 9638482000184,  # M2 LAGOA SANTA: 9638482000184
        8291296000159: 9210092000109,  # COLÉGIO DA LUZ: 9210092000109
        6123009000176: 7439904000167,  # COLÉGIO CÔNEGO: 7439904000167
        5833836000190: 14875519000128,  # CESA: 14875519000128
        17217670001562: 17217670000167,  # COLÉGIO BATISTA MINEIRO: 17217670000167
        36583288000111: 30704905000103  # COLÉGIO M2 - VESPASIANO: 30704905000103
    }, inplace=True)
    df_base = df_base[['Escola', 'Razão Social',	'CNPJ', 'Status']].merge(
        load_inep_cleaned(), on='CNPJ')
    # print(df_base[~df_base[Organization.cnpj].isin(inep_cleaned[Organization.cnpj].to_list())])
    df_base = df_base[['Escola', 'Nome', 'Razão Social', 'CNPJ',
                       maxia_pipedrive.models.Organization.inep_number, 'Razão Social',	'Cidade',	'UF',	'Status']]
    df_base.to_excel('data/microdados_treated/BASE_CLIENTES_2022_v1.xlsx')
    return df_base


def preprocess_roberta_wallet():
    def extract_digits(txt):
        digits = ''.join([s for s in str(txt) if s.isdigit()])
        if len(digits) > 0:
            return int(digits)
    # extract_digits = (lambda txt: int() if len(str(txt))>0 else None)
    roberta_wallet_raw = 'data/wallets/BASE KEY ACCOUNTS.xlsx'
    df_roberta = pd.read_excel(roberta_wallet_raw)
    df_roberta[maxia_pipedrive.models.Organization.cnpj] = df_roberta['CNPJ'].apply(
        extract_digits).astype('Int64', errors='ignore')
    df_roberta[maxia_pipedrive.models.Organization.inep_number] = df_roberta['Organização'].apply(
        lambda el: int(el.split('-')[0].strip()))
    df_roberta[maxia_pipedrive.models.Organization.name] = df_roberta['Organização'].apply(
        lambda el: el.split('-')[1].strip())
    # df_roberta[Organization.n_students] = df_roberta['Total de Alunos']
    df_roberta = df_roberta[[maxia_pipedrive.models.Organization.name, maxia_pipedrive.models.Organization.inep_number, maxia_pipedrive.models.Organization.cnpj,
                             maxia_pipedrive.models.Organization.school_network, maxia_pipedrive.models.Organization.n_students, maxia_pipedrive.models.Organization.average_price]]
    df_roberta.to_excel('data/wallets/Organizacoes_Roberta.xlsx', index=False)

# RELATION CREATION MODULES


def fetch_id_inep_reference(save=True):
    """ This module will fetch the reference id/INEP"""
    data = maxia_pipedrive.api_handler.organizations.get_all_organizations()
    id_inep_dict = {
        org_dict[maxia_pipedrive.models.Organization.get_api_code_dict(
        )[maxia_pipedrive.models.Organization.inep_number]]: org_dict['id']
        for org_dict in data
    }
    if save:
        timestp = datetime.now().strftime(maxia_pipedrive.consts.Consts.date_format)
        save_path = join(maxia_pipedrive.consts.Consts.relations_dir, f'orgid_inep_{timestp}.json')
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(id_inep_dict, f, indent=1)
        return save_path
    return id_inep_dict


def fetch_orgfieldinfo_reference(save=True):
    data = maxia_pipedrive.api_handler.fields.get_all_org_field_info()
    key_id_dict = {
        field_dict['key']: field_dict
        for field_dict in data
    }
    if save:
        timestp = datetime.now().strftime(maxia_pipedrive.consts.Consts.date_format)
        save_path = join(maxia_pipedrive.consts.Consts.relations_dir, f'orgfieldinfo_{timestp}.json')
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(key_id_dict, f, indent=1)
        return save_path
    return key_id_dict


def fetch_useralias_userid_reference(save=True):
    data = maxia_pipedrive.api_handler.users.get_all_users()
    name_email_id_dict = [
        {
            user['name']: user['id'],
            user['email']: user['id']
        }
        for user in data
    ]
    name_email_id_dict = {
        k: v for d in name_email_id_dict for k, v in d.items()}
    if save:
        timestp = datetime.now().strftime(maxia_pipedrive.consts.Consts.date_format)
        save_path = join(maxia_pipedrive.consts.Consts.relations_dir,
                         f'useralias_userid_{timestp}.json')
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(name_email_id_dict, f, indent=1)
        return save_path
    return name_email_id_dict


def fetch_stagealias_stageinfo_reference(save=True):
    data = maxia_pipedrive.api_handler.stages.get_all_stages()
    stagealias_stagedata = {
        stage['pipeline_name'] + "_" + stage['name']: stage
        for stage in data
    }
    if save:
        timestp = datetime.now().strftime(maxia_pipedrive.consts.Consts.date_format)
        save_path = join(maxia_pipedrive.consts.Consts.relations_dir,
                         f'stagealias_stageinfo_{timestp}.json')
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(stagealias_stagedata, f, indent=1)
        return save_path
    return stagealias_stagedata

# RELATIONS MODULES


def fetch_relation(relation: str):
    available_relations = maxia_pipedrive.consts.Relations.get_available_relations()
    assert relation in available_relations, f'Relation must be one of {available_relations}'

    if relation == maxia_pipedrive.consts.Relations.orgid_inep:
        return fetch_id_inep_reference(save=True)
    if relation == maxia_pipedrive.consts.Relations.orgfieldinfo:
        return fetch_orgfieldinfo_reference(save=True)
    if relation == maxia_pipedrive.consts.Relations.useralias_userid:
        return fetch_useralias_userid_reference(save=True)
    if relation == maxia_pipedrive.consts.Relations.stagealias_stageinfo:
        return fetch_stagealias_stageinfo_reference(save=True)
    if relation == maxia_pipedrive.consts.Relations.dealfieldinfo:
        return maxia_pipedrive.relations.fetch_dealfieldinfo_reference(save=True)
    if relation == maxia_pipedrive.consts.Relations.personfieldinfo:
        return maxia_pipedrive.relations.fetch_personfieldinfo_reference(save=True)

def load_relation(relation: str) -> dict:
    available_relations = maxia_pipedrive.consts.Relations.get_available_relations()
    assert relation in available_relations, f'Relation must be one of {available_relations}'
    list_rel_files = [f for f in listdir(
        maxia_pipedrive.consts.Consts.relations_dir) if relation in f]
    if len(list_rel_files) == 0:
        # generate
        fetch_relation(relation)
        list_rel_files = [
            f for f in listdir(maxia_pipedrive.consts.Consts.relations_dir)
            if relation in f
        ]
    # Get most recent
    relation_file = max(
        list_rel_files,
        key=lambda el: datetime.strptime(
            el.split(relation + "_")[1].split('.')[0],
            maxia_pipedrive.consts.Consts.date_format
        )
    )
    with open(
        join(
            maxia_pipedrive.consts.Consts.relations_dir,
            relation_file),
        'r',
            encoding='utf-8') as f:
        return json.load(f)


def load_inep_cleaned():
    df_ = pd.read_csv('data/microdados_treated/microdados_ed_basica_2021.csv',
                      sep=",", encoding='latin-1', index_col=0)

    # slight fix
    additional_inep_cnpj = {
        25213806: 6977338000184  # Petrônio
    }
    for inep_, cnpj in additional_inep_cnpj.items():
        df_.loc[df_[maxia_pipedrive.models.Organization.inep_number]
                == inep_, maxia_pipedrive.models.Organization.cnpj] = cnpj

    cast_int = [
        maxia_pipedrive.models.Organization.custom_address_cep, maxia_pipedrive.models.Organization.n_students,
        maxia_pipedrive.models.Organization.segmentos_n_inf, maxia_pipedrive.models.Organization.segmentos_n_fund_1,
        maxia_pipedrive.models.Organization.segmentos_n_fund_2, maxia_pipedrive.models.Organization.segmentos_n_medio
    ]
    df_[cast_int] = df_[
        cast_int].fillna(-1).astype('Int64').replace(-1, np.nan)
    # inep_cleaned = inep_cleaned.fillna('')

    cast_int64 = [maxia_pipedrive.models.Organization.cnpj, maxia_pipedrive.models.Organization.cnpj_mantenedora]
    # for c in cast_int64:
    #     inep_cleaned[c] = inep_cleaned[c].fillna(-1).apply(lambda el: int(el) if el is not None else el).astype('Int64').replace(-1, np.nan)
    df_[cast_int64] = df_[
        cast_int64].fillna(-1).astype('Int64').replace(-1, np.nan)

    return df_


if __name__ == '__main__':
    # preprocess_inep_data()
    # preprocess_base()
    # fetch_relation(Relations.orgid_inep)
    # fetch_relation(Relations.useralias_userid)
    # preprocess_roberta_wallet()
    fetch_relation(maxia_pipedrive.consts.Relations.orgid_inep)
