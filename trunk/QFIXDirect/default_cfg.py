############################################
# quickfix configuration property file name
############################################
QUICKFIXJ_CFG = "QFIXDirect.cfg"


SESS_CFG = {
    # Porta-OA - FUNC
    'OA': 'FIX.4.2:VKNG3->GSAU',
    # Porta-OA - UAT
    #'OA-UAT':'FIX.4.2:VKNG3->GSAU',
    'OA-UAT':'FIX.4.2:VKNG4->GSAU',
    # Flextrade - FUNC
    'FIX':'FIX.4.2:GSPROD4->PORTAF',
    # EDGEAlgo - FUNC
    #'EDGEAlgo':'FIX.4.2:GSVKFARM->EDGE',
    'EDGEAlgo':'FIX.4.2:GSATEST->EDGE',
    # EDGEBBR - FUNC
    'EDGEBlackrock': 'FIX.4.2:BLKEMSAP->GSAU/ADMIN',
    # Plutus - Func
    'Plutus': 'FIX.4.2:VERIFIXTEST->PLUTUSPLUS',
    # EDGEIOS/BBR - Func
    'EDGEIOS': 'FIX.4.2:BBR->JBWF',
}

############################################
# AMQ queue configuration
############################################
#IN_Q = '/queue/fix_in'
#OUT_Q = '/queue/fix_out'
IN_Q = '/queue/SAM_fix_in'
OUT_Q = '/queue/SAM_fix_out'


# webapp configuration 
#
WEBAPP_CFG = {
  'WXS_URL': "jdbc:oracle:thin:@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=mtxodb08-vip)(PORT=1521))(ADDRESS=(PROTOCOL=TCP)(HOST=mtxodb09-vip)(PORT=1521))(LOAD_BALANCE=yes)(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=racst)))",
  'USER': "WXS_DAEMON1",
  'PWD': "test_tiger",
  'JDBC_DRIVER': "oracle.jdbc.driver.OracleDriver",
  'MARKET': 'AUX', # 'AUX' default or 'ASX'
}

# web server port
port = 8008

# logging setting
import logging
#level = logging.DEBUG
level = logging.INFO
logfile = "qfix.log"

showConsole = True