import client
import os


if __name__ == '__main__':
	print 'Assuming Server is Down'
	print 'Return Code = '+str(client.kv739_init('adg-desktop-07.cs.wisc.edu:8081'))
	print ' PUT Request with key=arko and value=is bored'
        print '(Return Code , Old_Value) = '+ str(client.kv739_put('arko','is bored'))
	print 'Turning Server Back On'
	print 'Return Code = '+str(client.kv739_init('adg-desktop-07.cs.wisc.edu:8080'))
	print ' PUT Request with key=arko and value=is bored'
	print '(Return Code , Old_Value) = '+str(client.kv739_put('arko','is bored'))
	print ' PUT Request with key=arko and value=will be bored'
        print '(Return Code , Old_Value) = '+str(client.kv739_put('arko','will be bored'))
	print ' GET Request with key=arko '
	print '(Return Code , Value) = '+str(client.kv739_get('arko'))
	print ' DELETE Request with key=arko'
	print '(Return Code , Value ) = '+str(client.kv739_delete('arko'))
	print ' GET Request with key=arko '
	print '(Return Code , Value ) = '+str(client.kv739_get('arko'))

	print ' Checking for incorrect string format error cases '
	print ' PUT Request with key=[arko] and value=is bored'
        print '(Return Code , Old_Value) = '+ str(client.kv739_put('[arko]','is bored'))
	print ' PUT Request with key=arko and value=[is bored]'
        print '(Return Code , Old_Value) = '+ str(client.kv739_put('arko','[is bored]'))
	print ' PUT Request with key= and value=is bored'
        print '(Return Code , Old_Value) = '+ str(client.kv739_put('','is bored'))
	print ' PUT Request with key=arko and value='
        print '(Return Code , Old_Value) = '+ str(client.kv739_put('arko',''))



        infile = os.open("/dev/zero", os.O_RDONLY)
	value = os.read(infile,2050)
	os.close(infile)

	print ' PUT Request with key=arko and value greater than 2048 bytes'
        print '(Return Code , Old_Value) = '+ str(client.kv739_put('arko',value))

        infile = os.open("/dev/zero", os.O_RDONLY)
        value = os.read(infile,130)
        os.close(infile)
	
	print ' PUT Request with key greater than 128 bytes'
        print '(Return Code , Old_Value) = '+ str(client.kv739_put('arko',value))



	



	



	

