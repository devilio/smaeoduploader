# Copyright (C) 2010 KenTyde BV
# All rights reserved.
#
# This software is licensed as described in the file LICENSE,
# which you should have received as part of this distribution.

from datetime import datetime, date

import copy

SOH = '\x01'
PROTO = 'FIX.4.2'
CSMASK = 255

ADMIN = set([
    'Logon', 'Logout', 'Resend Request', 'HeartBeat', 'Test Request',
    'Sequence Reset', 'Reject',
])

IGNORE = ADMIN - set(['Reject'])

WENUMS = {
    'EncryptMethod': {
        None: 0,
    },
    'MsgType': {
        'HeartBeat': '0',
        'Test Request': '1',
        'Resend Request': '2',
        'Reject':'3',
        'Sequence Reset': '4',
        'Logout': '5',
        'ExecutionReport': '8',
        'OrderCancelReject': '9',
        'Logon': 'A',
        'NewOrderSingle': 'D',
        'OrderCancelRequest': 'F',
        'OrderCancelReplaceRequest': 'G',
        'OrderStatusRequest': 'H',
        'BusinessMessageReject': 'j',
        'DKTrade': 'Q',
        'QuoteRequest': 'R',
        'Quote': 'S',
        'MarketDataRequest': 'V',
        'MarketDataRequestReject': 'Y',
        'MarketDataSnapshot': 'W',
        'Multi-Leg': 'AB',
        'Multi-Leg Replace': 'AC',
        'QuoteRequestReject': 'AG',
        'MassQuote':'i',
    },
    'Side': {
        'Buy': '1',
        'Sell': '2',
    },
    'LegSide': {
        'Buy': '1',
        'Sell': '2',
    },
    'MDEntryType': {
        'Bid': 0,
        'Offer': 1,
    },
    'OrdType': {
        'Market': '1',
        'Limit': '2',
        'Stop': '3',
        'Stop limit': '4',
        'Market on close': '5',
        'With or without': '6',
        'Limit or better': '7',
        'Limit with or without': '8',
        'Previously Quoted': 'D',
    },
    'OpenClose': {
        'Open': 'O',
        'Close': 'C',
    },
    'PutOrCall': {
        'Put': 0,
        'Call': 1,
    },
    'ExecTransType': {
        'New': '0',
        'Cancel': '1',
        'Correct': '2',
        'Status': '3',
    },
    'OrdStatus': {
        'New': '0',
        'Partially filled': '1',
        'Filled': '2',
        'Done for day': '3',
        'Canceled': '4',
        'Replaced': '5',
        'Pending Cancel': '6',
        'Stopped': '7',
        'Rejected': '8',
        'Suspended': '9',
        'Pending New': 'A',
        'Calculated': 'B',
        'Expired': 'C',
        'Accepted for bidding': 'D',
        'Pending Replace': 'E',
    },
    'ExecType': {
        'New': '0',
        'Partial fill': '1',
        'Fill': '2',
        'Done for day': '3',
        'Canceled': '4',
        'Replace': '5',
        'Pending Cancel': '6',
        'Stopped': '7',
        'Rejected': '8',
        'Suspended': '9',
        'Pending New': 'A',
        'Calculated': 'B',
        'Expired': 'C',
        'Restated': 'D',
        'Pending Replace': 'E',
        'Trade': 'F',
    },
    'SubcriptionRequestType': {
        'Subscribe': 1,
        'Unsubscribe': 2,
    },
    'CxlRejReason': {
        'Too late to cancel': 0,
        'Unknown order': 1,
        'Broker Option': 2,
        'Order already pending': 3,
    },
    'CxlRejResponseTo': {
        'Order Cancel Request': '1',
        'Order Cancel/Replace Request': '2',
    },
    'HandlInst': {
        'auto-private': '1',
        'auto-public': '2',
        'manual': '3',
    },
    'MultiLegReportingType': {
        'Single Security': '1',
        'Individual leg': '2',
        'Multi-leg': '3',
    },
    'ExecInst': {
        'Not held': '1',
        'Work': '2',
        'Go along': '3',
        'Over the day': '4',
        'Held': '5',
        "Participate don't initiate": '6',
    },
    'MiscFeeType': {
        'Regulatory': '1',
        'Tax': '2',
        'Local Commission': '3',
        'Exchange Fees': '4',
        'Stamp': '5',
        'Levy': '6',
        'Other': '7',
        'Markup': '8',
        'Consumption Tax': '9',
    },
    'ExecRestatementReason': {
        'GT Corporate action': 0,
        'GT renewal / restatement': 1,
        'Verbal change': 2,
        'Repricing of order': 3,
        'Broker option': 4,
        'Partial decline of OrderQty': 5,
    },
    'TimeInForce': {
        'Day': '0',
        'GTC': '1',
        'OPG': '2',
        'IOC': '3',
        'FOK': '4',
        'GTX': '5',
        'GTD': '6',
    },
    'TargetStrategy': {
        'Calendar Spread': '1000',
    },
    'OrdRejReason': {
        'Broker option': 0,
        'Unknown symbol': 1,
        'Exchange closed': 2,
        'Order exceeds limit': 3,
        'Too late to enter': 4,
        'Unknown Order': 5,
        'Duplicate Order': 6,
        'Duplicate of a verbally communicated order': 7,
        'Stale Order': 8,
    },
    #FIX.4.3 BARX
    'QuoteCancelType':{
        'Cancel for Symbol(s)':1,
        'Cancel for Security Type(s)':2,
        'Cancel for Underlying Symbol':3,
        'Cancel All Quotes':4,
    },
     #FIX.4.4
    'QuoteType':{
        'Indicative':0,
        'Tradeable':1,
        'RestrictedTradeable':2,
        'Counter':3,
    },
    'QuoteResponseLevel':{
        'NoAck':0,
        'AckNeg':1,
        'AckEach':2,
    },
    
    'LastCapacity':{
        'Agent':1,
        'CrossAgent':2,
        'CrossPrincipal':3,
        'Principal':4,
    },
    'LastLiquidityInd':{
        'AddedLiquidity':1,
        'RemovedLiquidity':2,
        'LiquidityRoutedOut':3,
        'Auction':4,
    },
}

RENUMS = {}
for tag, vals in WENUMS.iteritems():
    cur = RENUMS.setdefault(tag, {})
    for k, v in vals.iteritems():
        cur[v] = k

RTAGS = {
    1: ('Account', str),
    6: ('AvgPx', float),
    7: ('BeginSeqNo', int),
    8: ('BeginString', str),
    9: ('BodyLength', int),
    10: ('CheckSum', str),
    11: ('ClOrdID', str),
    14: ('CumQty', float),
    15: ('Currency', str),
    16: ('EndSeqNo', int),
    17: ('ExecID', str),
    18: ('ExecInst', list),
    19: ('ExecRefID', str),
    20: ('ExecTransType', str),
    21: ('HandlInst', str),
    22: ('IDSource', str),
    29: ('LastCapacity',int),
    30: ('LastMkt', str),
    31: ('LastPx', float),
    32: ('LastShares', float),
    34: ('MsgSeqNum', int),
    35: ('MsgType', str),
    36: ('NewSeqNo', int),
    37: ('OrderID', str),
    38: ('OrderQty', float),
    39: ('OrdStatus', str),
    40: ('OrdType', str),
    41: ('OrigClOrdID', str),
    43: ('PossDupFlag', bool),
    44: ('Price', float),
    45: ('RefSeqNo', int),
    47: ('Rule80A', str),
    48: ('SecurityID', str),
    49: ('SenderCompID', str),
    50: ('SenderSubID', str),
    52: ('SendingTime', datetime),
    54: ('Side', str),
    55: ('Symbol', str),
    56: ('TargetCompID', str),
    57: ('TargetSubID', str),
    58: ('Text', str),
    59: ('TimeInForce', str),
    60: ('TransactTime', datetime),
    62: ('TransactTime2', datetime),
    63: ('SettlmntTyp', str),
    #64: ('FutSettDate', date),
    64: ('FutSettDate', str),
    75: ('TradeDate', date),
    76: ('ExecBroker', str),
    77: ('OpenClose', str),
    97: ('PossResend', bool),
    98: ('EncryptMethod', int),
    99: ('StopPx', float),
    100: ('ExDestination', str),
    102: ('CxlRejReason', int),
    103: ('OrdRejReason', int),
    108: ('HeartBtInt', int),
    109: ('ClientID', str),
    111: ('MaxFloor', float),
    112: ('TestReqID', str),
    117: ('QuoteID', str),
    122: ('OrigSendingTime', datetime),
    123: ('GapFillFlag', bool),
    126: ('ExpireTime', datetime),
    127: ('DKReason', str),
    131: ('QuoteReqID', str),
    132: ('BidPx', float),
    133: ('OfferPx', float),
    134: ('BidSize', int),
    135: ('OfferSize', int),
    136: ('NoMiscFees', int),
    137: ('MiscFeeAmt', float),
    138: ('MiscFeeCurr', str),
    139: ('MiscFeeType', str),
    141: ('ResetSeqNumFlag', bool),
    146: ('NoRelatedSym', int),
    150: ('ExecType', str),
    151: ('LeavesQty', float),
    167: ('SecurityType', str),
    188: ('BidSpotRate', float),
    189: ('BidForwardPoints', float),    
    190: ('OfferSpotRate', float),
    191: ('OfferForwardPoints', float),
    192: ('OrderQty2', float),
    193: ('FutSettDate2', date),
    194: ('LastSpotRate', float),
    195: ('LastForwardPoints', float),
    198: ('SecondaryOrderID', str),
    200: ('MaturityMonthYear', str),
    201: ('PutOrCall', int),
    202: ('StrikePrice', float),
    205: ('MaturityDay', str),
    206: ('OptAttribute', str),
    207: ('SecurityExchange', str),
    262: ('MDReqID', str),
    263: ('SubcriptionRequestType', int),
    264: ('MarketDepth', int),
    265: ('MDUpdateType', int),
    267: ('NoMDEntryTypes', int),
    268: ('NoMDEntries', int),
    269: ('MDEntryType', int),
    270: ('MDEntryPx', float),
    271: ('MDEntrySize', float),
    272: ('MDEntryDate', date),
    276: ('QuoteCondition', str),
    299: ('QuoteEntryId', str),
    371: ('RefTagID', str),
    372: ('RefMsgType', str),
    373: ('SessionRejectReason', str),
    378: ('ExecRestatementReason', int),
    379: ('BusinessRejectRefID', str),
    380: ('BusinessRejectReason', str),
    424: ('DayOrderQty', float),
    425: ('DayCumQty', float),
    426: ('DayAvgPx', float),
    434: ('CxlRejResponseTo', str),
    439: ('ClearingFirm', str),
    442: ('MultiLegReportingType', str),
    447: ('PartdIDSource', str),
    448: ('PartyID', str),
    452: ('PartyRole', int),
    453: ('NoPartyIDs', int),
    461: ('CFICode', str),
    553: ('Username', str),
    554: ('Password', str),
    555: ('NoLegs', int),
    600: ('LegSymbol', str),
    608: ('LegCFICode', str),
    610: ('LegMaturityMonthYear', str),
    623: ('LegRatioQty', int),
    624: ('LegSide', str),
    654: ('LegRefID', str),
    658: ('QuoteRequestRejectReason', int),
    847: ('TargetStrategy', str),
    1026: ('MDEntrySpotRate', float),
    1027: ('MDEntrySpotPoints', float),
    #FIX.4.2 
    168: ('EffectiveTime',datetime),
    432: ('ExpireDate',str),
    #FIX.4.3
    648: ('MinOfferSize',float),
    647:('MinBidSize',float),
    298:('QuoteCancelType',int),
    ##FIX.4.4
    301: ('QuoteResponseLevel',int),
    537: ('QuoteType',int),
    296: ('NoQuoteSets',str),
    302: ('QuoteSetID',str),
    304: ('TotNoQuoteEntries',int),
    295: ('NoQuoteEntries',str),
    297: ('QuoteStatus',int),
    ## GS price tags
    300: ('QuoteRejectReason',int),
    7890: ('L2BidPx',float),
    7892: ('L2BidSize',int),
    7891: ('L2OfferPx',float),
    7893: ('L2OfferSize',int),
    7894: ('L3BidPx',float),
    7896: ('L3BidSize',int),
    7895: ('L3OfferPx',float),
    7897: ('L3OfferSize',int),
    7898: ('L4BidPx',float),
    7900: ('L4BidSize',int),
    7899: ('L4OfferPx',float),
    7901: ('L4OfferSize',int),
    ## CITI Trade FIX.4.2
    303: ('QuoteRequestType',int),
    335: ('TradSesReqID',str),
    340: ('TradSesStatus',int),
    336: ('TradingSessionID',str),
    ## BARX extension
    6001: ('StrategyName',str),
    6010: ('PriceLimit',str),
    6011: ('LeavesQty',str),
    6012: ('MinTrade',str),
    6013: ('PercentFromLastLimit',str),
    6015: ('StartTime',str),
    6016: ('EndTime',str),
    6018: ('ParticipationRate',str),
    6019: ('ExecutionStyle',str),
    6020: ('MaxOrderSize',str),
    6021: ('AllOrLimitBetterVolume',str),
    6022: ('IncludeCrossingVolume',str),
    6023: ('RelativePriceLimit',str),
    6024: ('IndexType',str),
    6025: ('LimitType',str),
    6026: ('ProfileTilt',str),
    6027: ('PegAdjustment',str),
    6028: ('UseTrailingOrder',str),
    6029: ('StopLossPrice',str),
    6030: ('StopLossMinVolume',str),
    6031: ('StopLossPercentFromLast',str),
    6032: ('UseCustomIndex',str),
    6036: ('MinParticipationRate',str),
    6037: ('MaxParticipationRate',str),
    6038: ('BenchmarkType',str),
    6039: ('BenchmarkPrice',str),
    6040: ('BenchmarkIndex',str),
    6041: ('FavourableChangeRate',str),
    6042: ('AdverseChangeRate',str),
    6043: ('ExecutionView',str),
    6044: ('CrossingEnabled',str),
    6045: ('VolCycleType',str),
    6046: ('VolCycleMultiplierOverride',str),
    6047: ('AveStepVolumeOverride',str),
    6048: ('SmoothVolume',str),
    6050: ('AveStepVolPriceLevels',str),
    6051: ('ImbalanceTriggerRatio',str),
    6052: ('ImbalanceADVPercent',str),
    6053: ('ImbalanceTolerancePercent',str),
    6054: ('BalBookXTriggerPercent',str),
    6055: ('FairVWAPWindowSize',str),
    6056: ('UseThickOrderSizing',str),
    6057: ('OrderSizePercentOverride',str),
    6058: ('AuctionType',str),
    6059: ('VolumeLimit',str),
    6060: ('MarketOrderSize',str),
    6061: ('RelativeLimit',str),
    6062: ('InitialParticipation',str),
    6063: ('PegBenchmark',str),
    6064: ('SORStrategyName',str),
    6065: ('VolumeLimitType',str),
    6066: ('CleanupPrice',str),
    6067: ('MaxTargetOnClosePercent',str),
    6068: ('LimitOTMImpact',str),
    6069: ('MarkerOrderReloadPercent',str),
    6070: ('TrailingVWAPWindow',str),
    6071: ('TrailingVWAPRel%',str),
    6072: ('UseHardEndTime',str),
    6073: ('UseHiLoPriceLimit',str),
    6074: ('TrailingHiLoTimeWindow',str),
    6075: ('TrailingHiLoCountWindow',str),
    6076: ('UseDynMktOrderSize',str),
    6077: ('TrailingDepthBookDecay',str),
    6078: ('TrailingMktOrderSizeDecay',str),
    6079: ('SurplusTriggerPercent',str),
    6102: ('UserID',str),
    6207: ('Execution Venue',str),
    10583: ('ClientOrdLinkID',str),
    ## trader/account
    15000: ('Xref',str),
    
    # PORTA-OA
    851:('LastLiquidityInd',int)
}

WTAGS = dict((v[0], (k, v[1])) for (k, v) in RTAGS.iteritems())

## header tags
RTAGS_HEADER = {
    7: ('BeginSeqNo', int),
    8: ('BeginString', str),
    9: ('BodyLength', int),
    10: ('CheckSum', str),
    16: ('EndSeqNo', int),
    49: ('SenderCompID', str),
    50: ('SenderSubID', str),
    56: ('TargetCompID', str),
    57: ('TargetSubID', str),
}

WTAGS_HEADER = dict((v[0], (k, v[1])) for (k, v) in RTAGS_HEADER.iteritems())

def booldecode(x):
    return {'Y': True, 'N': False}[x]

def boolencode(x):
    return {True: 'Y', False: 'N'}[x]

DATEFMT = '%Y%m%d'

def dencode(d):
    return d.strftime(DATEFMT)

def ddecode(d):
    #print d
    return datetime.strptime(d, DATEFMT).date()

DATETIMEFMT = '%Y%m%d-%H:%M:%S'

def dtencode(dt):
    return dt.strftime(DATETIMEFMT)

def dtdecode(dt):
    if len(dt) == 17:
        return datetime.strptime(dt, DATETIMEFMT)
    base, milli = dt.split('.')
    dt = datetime.strptime(base, DATETIMEFMT)
    dt = dt.replace(microsecond=int(milli) * 1000)
    return dt

TYPES = {
    bool: (boolencode, booldecode),
    str: (str, str),
    int: (str, int),
    float: (str, float),
    long: (str, int),
    date: (dencode, ddecode),
    datetime: (dtencode, dtdecode),
    list: (lambda x: ' '.join(x), lambda x: x.split(' ')),
}

HEADER = [
    'SenderCompID', 'TargetCompID', 'MsgSeqNum', 'SendingTime',
]

REPEAT = {
    'Legs': [
        'LegRefID', 'LegSymbol', 'LegCFICode', 'LegMaturityMonthYear',
        'LegRatioQty', 'LegSide',
    ],
    'MiscFees': [
        'MiscFeeAmt', 'MiscFeeCurr', 'MiscFeeType',
    ],
    'PartyIDs': [
        'PartyID', 'PartdIDSource', 'PartyRole',
    ],
    'RelatedSym': [
        'Symbol', 'CFICode',
    ],
    'MDEntryTypes': [
        'MDEntryType',
    ],
    'MDEntries': [
        'MDEntryType', 'MDEntryPx', 'Currency', 'MDEntrySize', 'MDEntryDate',
        'QuoteCondition', 'QuoteEntryId', 'MDEntrySpotRate',
        'MDEntrySpotPoints',
    ],
    # CITI mass quote
    'QuoteEntries': [
        'QuoteEntryId','Symbol','Currency','TransactTime','FutSettDate','BidSize','OfferSize','BidSpotRate','OfferSpotRate',
        'BidPx','OfferPx'
    ],
}

def nojson(k):
    return WTAGS[k][1] in (dtdecode, ddecode)

def format(k, v):
    
    if k in WENUMS:
        if isinstance(v, list):
            v = [WENUMS[k].get(i, i) for i in v]
        else:
            v = WENUMS[k][v]
    
    v = TYPES[type(v)][0](v)
    return '%i=%s' % (WTAGS[k][0], v)

def tags(body, k, v):
    
    if k not in REPEAT:
        body.append(format(k, v))
        return
    
    common = set(v[0]).intersection(*[set(grp) for grp in v[1:]])
    if not common:
        raise ValueError('no common value in groups')
    start = sorted(common, key=REPEAT[k].index)[0]
    
    body.append(format('No' + k, len(v)))
    for grp in v:
        tags(body, start, grp[start])
        for key in set(REPEAT[k]) - set([start]):
            if key in grp:
                tags(body, key, grp[key])

def construct(msg):
    
    msg = copy.copy(msg)
    body = []
    body.append(format('MsgType', msg.pop('MsgType')))
    for k in HEADER:
        if k in msg:
            body.append(format(k, msg.pop(k)))
    
    for k, v in msg.iteritems():
        tags(body, k, v)
    
    body = SOH.join(body) + SOH
    header = [format('BeginString', PROTO)]
    header.append(format('BodyLength', len(body)))
    header.append(body)
    
    data = SOH.join(header)
    cs = sum(ord(c) for c in data) & CSMASK
    return data + format('CheckSum', '%03i' % cs) + SOH

def parse(msg):
    tags = msg.split(SOH)
    assert tags[-1] == ''
    tags = tags[:-1]
    
    msgs = [{}]
    parent = [(None, msgs)]
    cur, grp = msgs[0], None
    for tag in tags:
        
        k, v = tag.split('=', 1)
        if int(k) not in RTAGS:
            print "Error: Trying to validate a tag that isn't specified in RTAGS: %s" % k    
            raise ValueError(int(k))
        
        k, type = RTAGS[int(k)]
        v = TYPES[type][1](v)
        if k.startswith('No') and k[2:] in REPEAT and v:
            grp = k[2:]
            parent.append((grp, [{}]))
            cur[k[2:]] = parent[-1][1]
            cur = parent[-1][1][0]
            continue
        
        if k not in RENUMS:
            pass
        elif isinstance(v, tuple) or isinstance(v, list):
            v = v.__class__(RENUMS[k].get(i, i) for i in v)
        elif v in RENUMS[k]:
            v = RENUMS[k][v]
        
        if grp and k not in REPEAT[grp]: # end of current group range
            parent.pop()
            grp = parent[-1][0]
            cur = parent[-1][1][-1]
        if grp and k in cur: # next group
            cur = {}
            parent[-1][1].append(cur)
        
        cur[k] = v
        if k == 'CheckSum':
            cur = {}
            msgs.append(cur)
    
    if not msgs[-1]:
        msgs.pop(-1)
    return msgs
