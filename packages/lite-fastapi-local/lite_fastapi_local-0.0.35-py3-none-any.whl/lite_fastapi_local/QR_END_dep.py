from pynput.keyboard import Controller


keyboard = Controller()

def on_end():
    
    keyboard.type('QR_END\n')      
      

on_end()