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
def home_page():
    data =   """ Welcome to the of Ananse. This is a network inventory api"""
    return data.capitalize()

#get all listed devices
@app.get("/devices")
def get_list_devices():
     """This endpoint allows list all the devices"""
     return {device["hostname"]: device for device in devices}


#get a specific device.
@app.get("/devices/{ip}")
def get_one_device(ip:IPvAnyAddress):
    """This endpoint allows you to search for a device using the IP
    """
    for device in devices:
        if str(device["ip"])==str(ip):
            return device
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Device with IP address {ip} not found.")

#add a new device
@app.post("/devices",status_code=status.HTTP_202_ACCEPTED)
def add_new_device(new_device: Devices):
    """This endpoint allows you to add a new devices
       and also make sure no duplicate exist.
    """
    ip_conflict = any(str(device["ip"]) == str(new_device.ip) for device in devices) 
    host_conflict = any(str(device["hostname"]) == str(new_device.hostname) for device in devices)
    if ip_conflict and host_conflict :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Device with IP {new_device.ip} and hostname {new_device.hostname} alread exist")
    elif ip_conflict:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Device with ip address {new_device.ip} alread exist")
    elif host_conflict:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Device with hostname {new_device.hostname} alread exist")


    devices.append(new_device.model_dump())
    return {"message":f"A new device with IP {new_device.ip} has been addede","device":new_device}

#update device
@app.put("/devices/{ip}")
def update_device(ip:IPvAnyAddress,new_device: Devices):
    """This endpoint allows you to update an existing device."""
    for index,device in  enumerate(devices):
        if str(device["ip"]) == str(ip):
            devices[index] = new_device.model_dump()
            return {"message":f"device with ip {new_device.ip} has been added"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No device with IP {ip} available.")


#delete device
@app.delete("/devices/{ip}")
def delete_devices(ip:IPvAnyAddress):
    """This endpoint allows delete a device which is not in use
    """
    for index,device in enumerate(devices):
        if str(device["ip"]) == str(ip):
            del devices[index]
            return {"message": f"Device with IP {ip} has been deleted."}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No device with IP {ip} found.")
