from pynput import keyboard

scan_in = str()

def on_press(key):

    global scan_in        
    
    try:
        k = key.char  # single-char keys      
        
    except:
        if key == keyboard.Key.enter: #enter 키가 입력되면 종료
            print(scan_in)        
            return False     
        
    else:
        
        if k is not None:
            scan_in += k
        #print('SCAN is %s' % scan_in)            
        
        
with keyboard.Listener( #thread로 각 Char Listening
    on_press=on_press
    ) as listener:
    
    listener.join()
    
    