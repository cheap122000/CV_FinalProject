import serial
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
import time

# 控制開門
def controlDoor(instruct):
    delaytime = 0.05
    if instruct == 'open':
        ser = serial.Serial('COM3', 9600, timeout=0.5)

        ser.write(bytearray([0x41]))
        time.sleep(delaytime)

        ser.write(bytearray([0x31]))
        time.sleep(delaytime)

        ser.write(bytearray([0x31]))
        time.sleep(delaytime)

    elif instruct == 'close':
        ser = serial.Serial('COM3', 9600, timeout=0.5)

        ser.write(bytearray([0x41]))
        time.sleep(delaytime)

        ser.write(bytearray([0x30]))
        time.sleep(delaytime)

        ser.write(bytearray([0x31]))
        time.sleep(delaytime)


if __name__ == '__main__':
    # 時間標記
    memoryTime = time.time()
    openDoor = False

    # 實體化 Azure Table
    table_service = TableService(account_name='acc_name', account_key='acc_key')
    print(table_service.get_entity('testAPPs', 'ComputerVision', 'instruct', select='action').action)
    
    # 無窮迴圈
    while True:
        # 如果 Table 的 action 欄位是 open
        if table_service.get_entity('testAPPs', 'ComputerVision', 'instruct', select='action').action == 'open':
            # 開門
            if openDoor == False:
                openDoor = True
                memoryTime = time.time()
                controlDoor('open')
            # 三秒後關門，並把 Table 的 action 欄位改為 close
            if time.time() - memoryTime > 3:
                openDoor = False
                controlDoor('close')
                taskU = {'PartitionKey': 'ComputerVision', 'RowKey': 'instruct', 'action': 'close'}
                table_service.merge_entity('testAPPs', taskU)