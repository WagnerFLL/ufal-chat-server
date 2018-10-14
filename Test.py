class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(bcolors.HEADER+ "bcolors.HEADER" + bcolors.ENDC)
print(bcolors.OKBLUE +"bcolors.OKBLUE" + bcolors.ENDC)
print(bcolors.BOLD+"bcolors.BOLD"+ bcolors.ENDC)
print("Normal")
print(bcolors.OKGREEN+ "bcolors.OKGREEN"+ bcolors.ENDC)
print(bcolors.WARNING+ "bcolors.WARNING"+ bcolors.ENDC)
print(bcolors.FAIL+ "bcolors.FAIL"+ bcolors.ENDC)
print(bcolors.UNDERLINE+ "bcolors.UNDERLINE"+ bcolors.ENDC)
