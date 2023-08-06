"""

    """

my_github_username = "imahdimir"
m = my_github_username + "/"

class GitHubDataUrl :
    ind_ins = "d-Ind-Ins"
    id_2_tic = 'd-TSETMC_ID-2-Ticker'
    rf = 'd-Iran-RiskFree-Rate-Monthly'
    mkt_indx = 'd-TSE-Overall-Index-TEDPIX'
    codal_ltrs = 'd-all-Codal-letters'
    codal_tics_2_ftics = 'd-CodalTicker-2-FirmTicker'
    adj_price = 'd-Adj-Price'
    tse_work_days = 'd-TSE-Work-Days'
    adj_ret = 'd-Adj-Ret'

    def __init__(self) :
        for ky , vl in vars(GitHubDataUrl).items() :
            if not ky.startswith('_') :
                setattr(self , ky , m + vl)
