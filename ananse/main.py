from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel,IPvAnyAddress

app=FastAPI()


#creating a schema 
class Devices(BaseModel):
    hostname: str
    ip:IPvAnyAddress
    device_type: str
   

# devices = ["Cisco 72100","Cisco Firewire","Mikrotik 951"]
devices =[
  {
    "hostname": "R1",
    "ip": "192.168.1.1",
    "device_type": "cisco_ios"
  },
  {
    "hostname": "R2",
    "ip": "192.168.1.2",
    "device_type": "cisco_ios"
  }
]


@app.get("/")
def test():
    return "Hello world"

#get all listed devices
@app.get("/devices")
def get_list_devices():
   return {device["hostname"]: device for device in devices}


#get a specific device.
@app.get("/devices/{ip}")
def get_one_device(ip:IPvAnyAddress):
    for device in devices:
        if str(device["ip"])==str(ip):
            return device
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Device with IP address {ip} not found.")

#add a new device
@app.post("/devices")
def add_new_device(new_device: Devices):
    for device in devices:
        if str(device["ip"]) == str(new_device.ip):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Device with IP {ip} address alread exist")
        devices.append(new_device.model_dump())
        return {"message":f"A new device with IP {new_device.ip} has been addede"}
print(devices)
#update device
@app.put("/devices/{ip}")
def update_device(ip:IPvAnyAddress):
    pass