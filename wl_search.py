#!/usr/bin/python3

import requests
import json
from argparse import ArgumentParser
from datetime import date
import wl_tools


def search(bank_account=None, nip=None, regon=None):
  if not nip and not regon and not bank_account:
    raise ValueError("Missing nip/regon/bank_account.")

  if nip:
    nip = nip.replace("-", "")
    if not wl_tools.validate_nip(nip):
      raise ValueError("Invalid NIP.")
    SEARCH_CALL = wl_tools.NIP_SEARCH_CALL.format(nip = nip)
  elif regon:
    if not wl_tools.validate_regon(regon):
      raise ValueError("Invalid REGON.")
    SEARCH_CALL = wl_tools.REGON_SEARCH_CALL.format(regon = regon)
  else:
    bank_account = bank_account.replace(" ", "")
    if not wl_tools.validate_bank_account(bank_account):
      raise ValueError("Invalid bank account.")
    SEARCH_CALL = wl_tools.BANK_ACCOUNT_SEARCH_CALL.format(bank_account = bank_account)

  print(SEARCH_CALL)

  query = { "date": date.today().isoformat() }
  response = requests.get(wl_tools.URL + SEARCH_CALL, params = query)
  return response.json()


def format_bank_account(bank_account):
  str  = bank_account[0:2] + " "
  str += bank_account[2:6] + " "
  str += bank_account[6:10] + " "
  str += bank_account[10:14] + " "
  str += bank_account[14:18] + " "
  str += bank_account[18:22] + " "
  str += bank_account[22:26]
  
  return str


def print_subject(subject):
  print("NAZWA:              " + subject["name"])
  if subject["residenceAddress"] is not None:
    print("ADRES ZAMIESZKANIA: " + subject["residenceAddress"])
  if subject["workingAddress"] is not None:
    print("ADRES FIRMY:        " + subject["workingAddress"])
  print("NIP:                " + subject["nip"])
  print("REGON:              " + subject["regon"])
  if "krs" in subject and subject["krs"] is not None:
    print("KRS:                " + subject["krs"])
  print("DATA REJESTRACJI:   " + subject["registrationLegalDate"])
  print("STATUS VAT:         " + subject["statusVat"])
  if "accountNumbers" in subject and subject["accountNumbers"] is not None:
    bank_accounts = subject["accountNumbers"]
    if len(bank_accounts) == 1:
      print("KONTO BANKOWE:      " + format_bank_account(bank_accounts[0]))
    else:
      print("KONTA BANKOWE:")
      for bank_account in bank_accounts:
        print("                    " + format_bank_account(bank_account))


def main():
  module_name = __file__[0:-3]

  parser = ArgumentParser(prog = module_name, usage = "%(prog)s [options]")
  
  parser.add_argument("-n", "--nip", action="store", help="Specify NIP")
  parser.add_argument("-r", "--regon", action="store", help="Specify REGON")
  parser.add_argument("-b", "--bank_account", action="store", help="Specify bank account")
  
  args = parser.parse_args()
  response = None
  
  try:
    response = search(args.bank_account, args.nip, args.regon)
  except ValueError as ve:
    exit(ve)
  
  result = response["result"]

  #print(json.dumps(response.json(), indent = 2, sort_keys = True, ensure_ascii = False))

  if "subjects" in result:
    array = result["subjects"]
    for subject in array:
      print_subject(subject)
  else:
    print_subject(result["subject"])

  print()
  print("requestId:          " + result["requestId"]);
    


if __name__ == "__main__":
  main()
