import pygatt
import sys
import time

VALID_HEADERS = (b"\x01\x03", b"\x01\x04")
GET_STATUS = "fe043030002bab15"

message_length = 0
need_to_concat = False
concat_timeout = 1
start_time = 0
data = b""


def data_handler_cb(handle, value):
   global data
   global message_length
   global need_to_concat
   global start_time

   # print(f"Handle: {handle}")
   # value type is bytearray
   value_string = value.hex()
   print(f"Data: {value_string}")

   # PV multi-line data handling
   if value.startswith(VALID_HEADERS) and len(value) > 2:
      data = b""
      message_length = value[2]
      print(f"message_length={message_length}")
      
      if (len(value)-5) < message_length:
         start_time = time.time()
         need_to_concat = True
         print("Data detected. Next data will be concated")
   
#      # print(f"start_time={start_time}")
#      # print(f"stop_time={start_time + concat_timeout}")
#      data = ""
     
   if need_to_concat:
      if time.time() <= (start_time + concat_timeout):
         data = data + value
      else:
         need_to_concat = False
         message_length = 0
         print("Concat timeout occured. Concat aborted.")

   # analyzing data
   if (len(data) -5) == message_length:
      need_to_concat = False
      message_length = 0
      print("Full data fetched. Concat finished.")
         
      print(f"batt SoC ={int.from_bytes(data[46:47], 'big')}")
      print(f"PV V={int.from_bytes(data[63:65], 'big') / 100}")
      print(f"PV A={int.from_bytes(data[65:67], 'big', signed=True) / 100}")
      pv_w = int.from_bytes(data[67:69], 'big') / 100
      print(f"PV W=\t{pv_w}")
      pv_total = int.from_bytes(data[73:75], 'big') / 100
      print(f"PV TOTAL=\t{pv_total}\tkWh")

      print(f"BATT V={int.from_bytes(data[47:49], 'big') / 100}")
      print(f"BATT A={int.from_bytes(data[49:51], 'big', signed=True) / 100}")
      print(f"BATT temp={int.from_bytes(data[17:19], 'big') / 100}")

      print(f"LOAD V={int.from_bytes(data[55:57], 'big') / 100}")
      print(f"LOAD A={int.from_bytes(data[57:59], 'big', signed=True) / 100}")
      load_w = int.from_bytes(data[59:61], 'big') / 100
      print(f"LOAD W=\t{load_w}")
      load_total = int.from_bytes(data[79:81], 'big') / 100
      print(f"LOAD TOTAL=\t{load_total}\tkWh")

   # print(f"time.time()={time.time()}")
   # print(f"need_to_concat={need_to_concat}")
   # print(f"concat_timeout={concat_timeout}")
   # print(f"data={data}")

def main():
   adapter = pygatt.GATTToolBackend(hci_device=sys.argv[1])

   try:
      adapter.start()
      print("adapter started")

      device = adapter.connect(sys.argv[2]) 
      print("connected")
      device.subscribe('0000ff01-0000-1000-8000-00805f9b34fb', callback=data_handler_cb, indication=True)
      print("subscribed")

      # enable notifications
      adapter.sendline('char-write-req 0x0012 0100') 

      # get data
      device.char_write_handle(0x0014, bytes.fromhex(sys.argv[3]))

      time.sleep(1)
      print("Script finished")
      # print(f"data={data}")
      # print(f"len(data)={len(data)}")

   finally:
      adapter.stop()
      print("adapter stopped")

   return 0

if __name__ == '__main__':
   exit(main())
