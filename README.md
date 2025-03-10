# Network Device Inventory API
### Objective:
Create a simple REST API using FastAPI to manage a list of network devices(routers, switches,etc).
Requirements:

## Endpoints:
1. GET /devices – List all devices
2. GET /devices/{id} – View a specific device
3. POST /devices – Add a new device
4. PUT /devices/{id} – Update a device
5. DELETE /devices/{id} – Remove a device
Store data in a JSON file or in-memory dictionary
Fields: hostname, IP address, device type (router/switch), vendor (Cisco/Juniper), location
Bonus:

Add basic validation with Pydantic
Swagger UI (FastAPI handles this automatically)
Outcome:
This project sets the base for storing and retrieving network device data through APIs—something you’ll use heavily in automation platforms.
