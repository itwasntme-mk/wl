#!/usr/bin/python3

import requests
import json
from argparse import ArgumentParser
from datetime import date
import wl_tools


def check_nip(subject, nip):
  return subject["nip"] == nip


def check_regon(subject, regon):
  return subject["regon"] == regon


def check(bank_account, nip=None, regon=None):
  if not nip and not regon or not bank_account:
    raise ValueError("Missing nip/regon or bank_account.")

  bank_account = bank_account.replace(" ", "")
    
  if not wl_tools.validate_bank_account(bank_account):
    raise ValueError("Invalid bank account.")
    
  SEARCH_CALL = wl_tools.BANK_ACCOUNT_SEARCH_CALL.format(bank_account = bank_account)

  print(SEARCH_CALL)
  
  query = { "date": date.today().isoformat() }
  response = requests.get(wl_tools.URL + SEARCH_CALL, params = query)
  result = response.json()["result"]
  
  #print(result)
    
  if nip:
    nip = nip.replace("-", "")
    if not wl_tools.validate_nip(nip):
      raise ValueError("Invalid NIP")
    if result["subjects"] is not None:
      for subject in result["subjects"]:
        if check_nip(subject, nip):
          return (True, result["requestId"])
    elif result["subject"] is not None:
      return (check_nip(result["subject"], nip), result["requestId"])
  else:
    if not wl_tools.validate_regon(regon):
      raise ValueError("Invalid REGON")
    if result["subjects"] is not None:
      for subject in result["subjects"]:
        if check_regon(subject, regon):
          return (True, result["requestId"])
    elif result["subject"] is not None:
      return (check_regon(result["subject"], regon), result["requestId"])

  return (False, result["requestId"])


def main():
  module_name = __file__[0:-3]

  parser = ArgumentParser(prog = module_name, usage = "%(prog)s [options]")
  
  parser.add_argument("-n", "--nip", action="store", help="Specify NIP")
  parser.add_argument("-r", "--regon", action="store", help="Specify REGON")
  parser.add_argument("-b", "--bank_account", action="store", help="Specify bank account")
  
  args = parser.parse_args()
  result = None
  requestId = None
  
  try:
    (result, requestId) = check(args.bank_account, args.nip, args.regon)
  except ValueError as ve:
    exit(ve)

  if result:
    print("accountAssigned: TAK");
  else:
    print("accountAssigned: NIE");

  print("requestId:       " + requestId);
  

if __name__ == "__main__":
  main()
