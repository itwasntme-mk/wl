import requests
import json
from datetime import date
from argparse import ArgumentParser
import wl_tools


URL = "https://wl-api.mf.gov.pl"
#URL = "https://wl-test.mf.gov.pl"
NIP_CHECK_CALL = "/api/check/nip/{nip}/bank-account/{bank_account}"
REGON_CHECK_CALL = "/api/check/regon/{regon}/bank-account/{bank_account}"
QUERY = { "date": date.today().isoformat() }


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
    
  if args.nip:
    nip = args.nip.replace("-", "")
    if not wl_tools.validate_nip(nip):
      exit("Invalid NIP")
    CHECK_CALL = NIP_CHECK_CALL.format(nip = nip, bank_account = bank_account)
  else:
    if not wl_tools.validate_regon(args.regon):
      exit("Invalid REGON")
    CHECK_CALL = REGON_CHECK_CALL.format(regon = args.regon, bank_account = bank_account)

  print(CHECK_CALL)

  response = requests.get(URL + CHECK_CALL, params = QUERY)
  response.encoding = "utf-8"
  
  result = response.json()["result"]
  print("accountAssigned: " + result["accountAssigned"]);
  print("requestId:       " + result["requestId"]);
  
  #print(json.dumps(response.json(), indent = 2, sort_keys = True, ensure_ascii = False))


if __name__ == "__main__":
  main()