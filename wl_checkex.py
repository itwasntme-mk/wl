import requests
import json
from datetime import date
from argparse import ArgumentParser
import wl_tools


URL = "https://wl-api.mf.gov.pl"
#URL = "https://wl-test.mf.gov.pl"
BANK_ACCOUNT_SEARCH_CALL = "/api/search/bank-account/{bank_account}"
QUERY = { "date": date.today().isoformat() }


def check_nip(subject, nip):
  return subject["nip"] == nip


def check_regon(subject, regon):
  return subject["regon"] == regon


def main():
  module_name = __file__[0:-3]

  parser = ArgumentParser(prog = module_name, usage = "%(prog)s [options]")
  
  parser.add_argument("-n", "--nip", action="store", help="Specify NIP")
  parser.add_argument("-r", "--regon", action="store", help="Specify REGON")
  parser.add_argument("-b", "--bank_account", action="store", help="Specify bank account")
  
  args = parser.parse_args()
  
  if not args.nip and not args.regon:
    exit("Specify NIP or REGON + bank account")
    
  if not args.bank_account:
    exit("Specify bank account")
  else:
    bank_account = args.bank_account.replace(" ", "")
    
  if not wl_tools.validate_bank_account(bank_account):
    exit("Invalid bank account")
  else:
    SEARCH_CALL = BANK_ACCOUNT_SEARCH_CALL.format(bank_account = bank_account)

  print(SEARCH_CALL)
  
  response = requests.get(URL + SEARCH_CALL, params = QUERY)
  response.encoding = "utf-8"
  result = response.json()["result"]
    
  if args.nip:
    nip = args.nip.replace("-", "")
    if not wl_tools.validate_nip(nip):
      exit("Invalid NIP")
    if result["subjects"]:
      for subject in result["subjects"]:
        if check_nip(subject, nip):
          print("accountAssigned: TAK");
          break
      else:
        print("accountAssigned: NIE");
    else:
      if check_nip(result["subject"], nip):
        print("accountAssigned: TAK");
      else:
        print("accountAssigned: NIE");
  else:
    if not wl_tools.validate_regon(args.regon):
      exit("Invalid REGON")
    if result["subjects"]:
      for subject in result["subjects"]:
        if check_regon(subject, args.regon):
          print("accountAssigned: TAK");
          break
      else:
        print("accountAssigned: NIE");
    else:
      if check_regon(result["subject"], args.regon):
        print("accountAssigned: TAK");
      else:
        print("accountAssigned: NIE");

  print("requestId:       " + result["requestId"]);
  
  #print(json.dumps(response.json(), indent = 2, sort_keys = True, ensure_ascii = False))


if __name__ == "__main__":
  main()
