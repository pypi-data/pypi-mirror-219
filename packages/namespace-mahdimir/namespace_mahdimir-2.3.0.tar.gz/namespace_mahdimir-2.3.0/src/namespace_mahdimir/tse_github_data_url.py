"""

    """

my_github_username = "imahdimir"
m = my_github_username + "/"

class GitHubDataUrl :
    ind_ins = "Ind-Ins"
    id_2_tic = 'TSETMC_ID-2-Ticker'
    rf = 'Iran-RiskFree-Rate-Monthly'
    mkt_indx = 'TSE-Overall-Index-TEDPIX'
    codal_ltrs = 'all-Codal-letters'
    codal_tics_2_ftics = 'CodalTicker-2-FirmTicker'
    adj_price = 'Adj-Price'
    tse_work_days = 'TSE-Work-Days'
    adj_ret = 'Adj-Ret'
    tedpix = 'TEDPIX'
    nom_price = 'Nominal-Price'
    id_2_ftic = 'TSETMC_ID-2-FirmTicker'

    def __init__(self) :
        for ky , vl in vars(GitHubDataUrl).items() :
            if not ky.startswith('_') :
                setattr(self , ky , m + 'd-' + vl)
