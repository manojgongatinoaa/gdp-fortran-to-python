#!/usr/bin/python

# This module defines project-level constants.

# Programer: CG July 2026

# *** for testing purposes ***
BASE_DATA_DIR = "/phodnet/drifter/gonzalez/programs/python/migration_for2py/data/"

# Default data directory
#BASE_DATA_DIR       = "/phodnet/drifter/data/"
DATA_DIR            = BASE_DATA_DIR + "files/"
NEW_DATA_DIR        = BASE_DATA_DIR + "files_new/IDcenter/"
RAW_DIR             = BASE_DATA_DIR + "raw/"
WCK_DIR             = BASE_DATA_DIR + "vck/"
SS_DIR              = BASE_DATA_DIR + "ss/"
BACKUP_DIR          = DATA_DIR + "save/"

# Database
TPB_AB_COEF15_DAT   = DATA_DIR + "tpb_ab_coef15.dat"
WMOGTS15_DAT        = DATA_DIR + "wmogts15.dat"
WMOGTS15_OFF        = DATA_DIR + "wmogts15.off"
IMEI_LUT_DAT        = NEW_DATA_DIR + "IMEI_LUT.dat"
TMPFL30_DAT         = DATA_DIR + "tmpfl30.dat"
DEPLOYED_LOG        = DATA_DIR + "deployed.log"

# Directory file
DIR_FILE            = DATA_DIR + "dirfl50.dat"

data_type_directory = {
    1: RAW_DIR,
    2: WCK_DIR,
    3: WCK_DIR,
    4: SS_DIR
}

data_type_prefix = {
    1: "b",
    2: "p",
    3: "s",
    4: "k"
}

data_type_columns = {
    "b_file": 11,
    "p_file": 4,
    "s_file": 7,
    "k_file": 10,
    "d_file": 22
}
