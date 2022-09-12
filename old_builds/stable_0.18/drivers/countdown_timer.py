def countdown(t):
    import time 
    print("\nWaiting for "+str(t)+" secs before running next iteration\n")   
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
      
    print('Running next iteration..')

  
  

