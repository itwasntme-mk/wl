#!/usr/bin/python3

URL = "https://wl-api.mf.gov.pl"
#URL = "https://wl-test.mf.gov.pl"
NIP_CHECK_CALL = "/api/check/nip/{nip}/bank-account/{bank_account}"
REGON_CHECK_CALL = "/api/check/regon/{regon}/bank-account/{bank_account}"
BANK_ACCOUNT_SEARCH_CALL = "/api/search/bank-account/{bank_account}"
NIP_SEARCH_CALL = "/api/search/nip/{nip}"
REGON_SEARCH_CALL = "/api/search/regon/{regon}"


def validate_nip(nip):
  weights = [ 6, 5, 7, 2, 3, 4, 5, 6, 7 ]
  result = 0

  if len(nip) != 10 or not nip.isdigit():
    return False

  for i in range(9):
    j = ord(nip[i]) - 48
    result += j * weights[i]

  j = ord(nip[9]) - 48
  result = result % 11
  return result == j


def validate_regon(regon):
  weights = [ 8, 9, 2, 3, 4, 5, 6, 7 ]
  result = 0

  if len(regon) != 9 or not regon.isdigit():
    return False

  for i in range(8):
    j = ord(regon[i]) - 48
    result += j * weights[i]

  j = ord(regon[9]) - 48
  result = result % 11
  return result == j


def validate_bank_account(bank_account):
  if len(bank_account) != 26 or not bank_account.isdigit():
    return False
    
  result = int(bank_account[2:] + "2521" + bank_account[:2]) # for PL
  return result % 97 == 1
