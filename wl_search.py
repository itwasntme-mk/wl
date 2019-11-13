import requests
import json
from datetime import date
from argparse import ArgumentParser
import wl_tools


URL = "https://wl-api.mf.gov.pl"
#URL = "https://wl-test.mf.gov.pl"
BANK_ACCOUNT_SEARCH_CALL = "/api/search/bank-account/{bank_account}"
NIP_SEARCH_CALL = "/api/search/nip/{nip}"
REGON_SEARCH_CALL = "/api/search/regon/{regon}"
QUERY = { "date": date.today().isoformat() }


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
  
  if not args.nip and not args.regon and not args.bank_account:
    exit("Specify NIP, REGON or bank account")
    
  if args.nip:
    nip = args.nip.replace("-", "")
    if not wl_tools.validate_nip(nip):
      exit("Invalid NIP")
    SEARCH_CALL = NIP_SEARCH_CALL.format(nip = nip)
  elif args.regon:
    if not wl_tools.validate_regon(args.regon):
      exit("Invalid REGON")
    SEARCH_CALL = REGON_SEARCH_CALL.format(regon = args.regon)
  else:
    bank_account = args.bank_account.replace(" ", "")
    if not wl_tools.validate_bank_account(bank_account):
      exit("Invalid bank account")
    SEARCH_CALL = BANK_ACCOUNT_SEARCH_CALL.format(bank_account = bank_account)

  print(SEARCH_CALL)

  response = requests.get(URL + SEARCH_CALL, params = QUERY)
  response.encoding = "utf-8"
  result = response.json()["result"]

  #print(json.dumps(response.json(), indent = 2, sort_keys = True, ensure_ascii = False))

  if "subjects" in result:
    array = result["subjects"]
    for subject in array:
      print_subject(subject)
      print()
  else:
    print_subject(result["subject"])

  print("requestId:          " + result["requestId"]);
    


if __name__ == "__main__":
  main()
