from ..config.consts import contract_address


def certificate_address(_type):
    """
    STC    Storage      STCCertificate
    DTC    Data         DATACertificate
    CTC    Computing    CTCCertificate
    MDC    Model        MDCCertificate
    GNC    Gene         GNCCertificate
    INFT1  ImageNFT1    INFT1Certificate
    :param _type: 类型
    :return:
    """
    address = None
    if _type == "STC":
        address = contract_address['STCCertificate']
    elif _type == "DTC":
        address = contract_address['DATACertificate']
    elif _type == "CTC":
        address = contract_address['CTCCertificate']
    elif _type == "MDC":
        address = contract_address['MDCCertificate']
    elif _type == "GNC":
        address = contract_address['GNCCertificate']
    elif _type == "INFT1":
        address = contract_address['INFT1Certificate']
    return address
