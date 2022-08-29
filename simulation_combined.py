import subprocess

program_list = ['simulation.py', 'simulation1H0T.py', 'simulation0H1T.py']
for program in program_list:
    print('Started: ' + program)
    subprocess.call(['python3', program])
    print('Finished: ' + program)
