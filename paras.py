# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/9/3
@Author: Haojun Gao
@Description: 
"""


def header_useragent():
    """
    提供完整的headers和可供选择的User-Agent
    :return: headers & userAgent
    """
    headers = {"Accept": "text/html, */*",
               # "accept-encoding": "gzip, deflate, br",
               "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
               "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
               "cookie": "TASSK=enc%3AAN%2FngplBg3A2Lqm19YK7Js4uQiKhMpmHVJ%2BZBIRNFJz%2BE2UwxthDKo37lbWkDVJypvG9ipDTvqkg8CJmr0vJHGPPCR8QQ6rmzoapcY8Dt1VXPcz7E7J2WYeWuDULfsPPKQ%3D%3D; ServerPool=B; VRMCID=%1%V1*id.12019*llp.%2F*e.1568093250581; PMC=V2*MS.52*MD.20190903*LD.20190903; TAUnique=%1%enc%3AMqJCUMuo9JJjg658bFC9NTzONssFd42j1FQvNhEc05N4l51zY1INdA%3D%3D; TART=%1%enc%3AKcBwDxvuYnBeMxBg%2FyqnT61huc6currPwG%2F83HZB25erAyT18o4yl7G%2F2rUkP1er25dZGLjWyRQ%3D; TAAuth3=3%3Ab99d9b8bd72741f534f789ba97363369%3AAHjwbnf8aNmHFcA6%2BRlnl%2FnTQRcyx23RKjvVaxM%2FELNTCPqGL%2FcjO5E1QQrf34%2BzGRWt%2BozcqqIg%2FVyPki4he5Ox3Lrt2dy66QDBKtbtnmajPAjEgR%2FCpC82d5nTzz6TfuFEzh0p%2BHCln%2BwwUIK6O2F7Z9cqC68M2%2BcDZhhvqXYVeb99ZNlZ3DnJPJxoj9hlNA%3D%3D; CM=%1%PremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CRestAds%2FRPers%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C6%2C-1%7CPremiumSURPers%2C%2C-1%7Ctvsess%2C1%2C-1%7CPremiumMCSess%2C%2C-1%7CUVOwnersSess%2C%2C-1%7CRestPremRSess%2C%2C-1%7CCCSess%2C%2C-1%7CCYLSess%2C%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CRestAdsPers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CRestWiFiPers%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CTADORSess%2C%2C-1%7CAdsRetPers%2C%2C-1%7CTARSWBPers%2C%2C-1%7CSPMCSess%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CRestWiFiREXPers%2C%2C-1%7CSPMCWBPers%2C%2C-1%7CRBAPers%2C%2C-1%7CRestAds%2FRSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CWiFiORSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7CRestAdsCCSess%2C%2C-1%7CRestPremRPers%2C%2C-1%7CUVOwnersPers%2C%2C-1%7Csh%2C%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCYLPers%2C%2C-1%7CCCPers%2C%2C-1%7Ctvpers%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CRestWiFiSess%2C%2C-1%7CRestWiFiREXSess%2C%2C-1%7CSPMCPers%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CAdsRetSess%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CRestAdsCCPers%2C%2C-1%7CTADORPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CWiFiORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CTARSWBSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRestAdsSess%2C%2C-1%7CRBASess%2C%2C-1%7CSPORPers%2C%2C-1%7Cperssticker%2C%2C-1%7CSPMCWBSess%2C%2C-1%7C; TATravelInfo=V2*AY.2019*AM.9*AD.15*DY.2019*DM.9*DD.16*A.2*MG.-1*HP.2*FL.3*DSM.1567488745962*RS.1; TAReturnTo=%1%%2FShowUserReviews-g60763-d1687489-r705572515-The_National_9_11_Memorial_Museum-New_York_City_New_York.html; TALanguage=en; TASession=%1%V2ID.E5D393DD845E710CECF66FA66C3BDF0F*SQ.315*PR.40185%7C*LS.DemandLoadAjax*GR.16*TCPAR.14*TBR.70*EXEX.93*ABTR.0*PHTB.24*FS.31*CPU.74*HS.recommended*ES.popularity*DS.5*SAS.popularity*FPS.oldFirst*TS.CB2DAD8F93CC1036E26BB732CE0B4370*LF.en*FA.1*DF.0*FLO.11854338*TRA.false*LD.11854338; PAC=AHgIBKY7cAMyhHRtI3VCtLUhoYaYZW4wZhTun0qFjusIw-jrjJwvdDZp1jFCmsKg1fekkhovvRK8ivhwXzT29hH7q_hG5FHHKP1FzgsSeCr9MvDTq0DbBPQcdb9ZElEKevmQB2xb6KUWUHAqqCtgiww4On9uYGT0f7JdTUOUyXGJ3LF05Q0D6U7mkAFRltke1PcnteacmeJGny_RX7GpfvJuu6JIcClduFeDN-BDckp_ScFAXKmb5vuZyTWGNu4RPP8CCuZppO5FlgOuHyjUp1q6eGUPdsQsO1Fw3DIQoqgAZ4GnCAc2XdXgV5KXPJ8024EQTbMYmSg63TBQi-1M-SM%3D; TAUD=LA-1567488460543-1*RDD-1-2019_09_03*HDD-204508-2019_09_15.2019_09_16*HC-235619*LD-27763869-2019.9.15.2019.9.16*LG-27763871-2.1.F.*ARDD-27763872-2019_09_152019_09_16",
               "Origin": "https://cn.tripadvisor.com",
               "Referer": "https://cn.tripadvisor.com/Attraction_Review-g60763-d1687489-Reviews-The_National_9_11_Memorial_Museum-New_York_City_New_York.html",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
               "x-puid": "XW4YQwoQLi0AAtwfG3AAAACG",
               "X-Requested-With": "XMLHttpRequest"
               }

    userAgent = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"]
    return headers, userAgent
