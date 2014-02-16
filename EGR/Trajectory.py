#!/usr/bin/pyhthon
#########################################################################
#A simple program to calculate the range of a projectile               #
#and email a file with the projectiles range in it to a specified user #
#Date: 11/22/2013@0152 Author: Joshua Lilly                            #
#########################################################################

import smtplib
import math as math
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import getpass
import copy

class Ryw:
    
    
#########################################################################################################################################################################################################

        #constructor that allows the class to take in the
        # needed information to send the output file in an email
        #by allowing the constructor to do the work at run time
        #security of user is increased since no passwords are held in the src file.
        def __init__(self, email_addr, password, reciv):
            self.email_addr = email_addr
            self.password = password
            self.reciv = reciv
            
#########################################################################################################################################################################################################

        #reads file
        #...really just wanted to use a list as a stack :)
        def read_file(self, name_in): 
            in_stack = []
            con = True
            fh = open(name_in, 'r')
            while(con):
                contents = fh.readline()
                if contents != '':
                    contents = contents.rstrip()
                    in_stack.append(contents)
                else:
                    con = False    
            fh.close()
            return in_stack
        
########################################################################################################################################################################################################        

        #opens a file to erase the contents
        def delete_file(self, file):
            open(file, 'w').close()
            
            
#########################################################################################################################################################################################################

        #prints answers to file
        def print_file(self, name_out, stack, var, target, in_copy):
            i = 0
            self.delete_file(name_out)
            c_stack = copy.copy(stack)
            fh = open(name_out, 'a')
            while(i < var):
                a = str(stack.pop())
                fh.write('Guess ' + str(i + 1) + ': ' + a + 'ft\n')
                i +=1
            win = self.decide_winner(c_stack, target)
            top = in_copy[win - 1]
            top = top.split(',')
            print('For the target distance of ' + str(target) + ' ft guess number ' + str(win) + ' was the closest shot on target.\nInitial velocity was ' + str(top[0]) + ' ft/s and theta was ' + str(top[1]) +  ' degrees. \n')
            fh.write('For the target distance of ' + str(target) + ' ft guess number ' + str(win) + ' was the closest shot on target.\nInitial velocity was '  + str(top[0]) + ' ft/s and theta was ' + str(top[1]) +  ' degrees. \n')
            fh.close()
        
#########################################################################################################################################################################################################

        #decides which guess was the closest to the given target and
        #displays the winner
        def decide_winner(self, c_stack, target):
            win_stack = []
            i = 0
            winner = 0
            sl = len(c_stack)
            while(i < sl):
                a = c_stack.pop()
                diff = abs(float(target) - float(a))
                if len(win_stack) == 0:
                    win_stack.append(diff)
                    winner = i + 1
                elif diff < win_stack[0]:
                    win_stack.pop()
                    win_stack.append(diff)
                    winner = i + 1
                i += 1
            return winner
        
        
#########################################################################################################################################################################################################

        #send answer file in an email
        def send_message(self, smtpserver='smtp.gmail.com:587'):
            msg = MIMEMultipart()
            msg['Subject'] = 'Trajectory Ranges'
            msg['From'] = self.email_addr
            msg['To'] = self.reciv
            msg.attach(MIMEText(open("out.txt").read()))
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(self.email_addr, self.password)
            server.sendmail(self.email_addr, self.reciv, msg.as_string())
            server.close()

        
#########################################################################################################################################################################################################
      
        #Calculates the 't' variable in the kinamatic equation
        def calculate_time(self, guess, a):
            guess = guess.split(',')
            v = guess[0]
            t = guess[1]
            v_naught = float(v)
            theta = float(t)
            rads = math.sin(math.radians(theta))   
            vector_y = v_naught * rads
            a = a/2
            return self.solve_for_time(vector_y, a)
            
#########################################################################################################################################################################################################            
        
        #utilizes the quadratic formula to find time   
        def solve_for_time(self, b, a):
            return (-b+math.sqrt(((b*b)*2)))/(2*a)
        
#########################################################################################################################################################################################################        
       
        #calculartes the horizontal distance
        def calculate(self, guess, a):
            time = self.calculate_time(guess, a)
            guess = guess.split(',')
            v_naught = float(guess[0])
            range_x = time * v_naught
            #print('range' +str(range) + ' time ' + str(time) + 'vo ' + str(v_naught))
            return range_x
 
#########################################################################################################################################################################################################
       
        #if user wishes to enter the target in meters this converts the target into
        #feet since it was required that the initial velocity be taken as feet
        def convert_to_feet(self, target):
            return float(target) * 3.28084
        
#########################################################################################################################################################################################################        
        
        #This is the place in which I will be assembling the simple program
        def Sys_par(self, system, target):
            a = 32.15
            out_stack = []
            in_stack = self.read_file('in.txt')
            if system == 'M':
                target = self.convert_to_feet(target)
            var = len(in_stack)
            i = 1
            in_copy = copy.copy(in_stack)
            while(i <= var):
                guess = in_stack.pop()
                range_x = self.calculate(guess, a)
                out_stack.append(range_x)
                i += 1
            self.print_file('out.txt', out_stack, var, target, in_copy)    
            return 0

########################################################################################################################################################################################################
        
        #checks user input to make sure the range variable gets set as a number
        def is_a_number(self, num):
            try:
                float(num)
                return True
            except ValueError:
                return False
       
#########################################################################################################################################################################################################      

        #checks user input to make sure the user enters m for meters of f for foot
        def is_acceptable_letter(self, let):
            if let == 'M' or let == 'F': return True
            
#########################################################################################################################################################################################################
        
#Application

def main():
    cont = False
    cont2 = False
    email = input('enter the senders email address\n')
    password = getpass.getpass('Enter the senders password\n')
    reciv = input('Enter the recipient\n')
    rd = Ryw(email, password, reciv)
    while(cont == False):
        m_s = input('Would you like to work in meters or feet?\n[m = meters f = feet]\n')
        m_s = m_s.upper()
        if rd.is_acceptable_letter(m_s) == True: cont = True 
    while(cont2 == False):
        target_range = input('Enter the targets range\n')
        if rd.is_a_number(target_range) == True: cont2 = True
    rd.Sys_par(m_s, target_range)
    rd.send_message()
    print('message sent\n')
if __name__ == '__main__': main()
