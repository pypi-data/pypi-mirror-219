# -*- coding: utf-8 -*-
BARRA_INDUSTRY = [
    'Bank', 'RealEstate', 'Health', 'Transportation', 'Mining', 'NonFerMetal',
    'HouseApp', 'LeiService', 'MachiEquip', 'BuildDeco', 'CommeTrade',
    'CONMAT', 'Auto', 'Textile', 'FoodBever', 'Electronics', 'Computer',
    'LightIndus', 'Utilities', 'Telecom', 'AgriForest', 'CHEM', 'Media',
    'IronSteel', 'NonBankFinan', 'ELECEQP', 'AERODEF', 'Conglomerates'
]
BARRA_COUNTRY = ['COUNTRY']
BRAAR_RISKFACTOR = [
    'BETA', 'MOMENTUM', 'SIZE', 'EARNYILD', 'RESVOL', 'GROWTH', 'BTOP',
    'LEVERAGE', 'LIQUIDTY', 'SIZENL'
]
BARRA_ALL = BARRA_INDUSTRY + BARRA_COUNTRY + BRAAR_RISKFACTOR
BARRA_SIZEIND = BARRA_INDUSTRY + BARRA_COUNTRY + ['SIZE', 'SIZENL']