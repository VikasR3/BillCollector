# BillCollector

Collects my bills from different web portals.

## Notes
### get_credentials.sh - prototyping

#!/bin/bash

#curl --json '{"password": "+49307874573"}' http://solg.fritz.box:8087/unlock
curl -X POST -H 'Content-Type: application/json' -d '{"password": "+49307874573"}' http://solg.fritz.box:8087/unlock

#curl --json '{"password": "+49307874573"}' http://solg.fritz.box:8087/sync
curl -X POST -H 'Content-Type: application/json' -d '{"password": "+49307874573"}' http://solg.fritz.box:8087/sync

curl -s http://solg.fritz.box:8087/object/item/KabelDeutschland | jq '.data.login'

## Architecture & Concept - Prototype
Architecture & Concept
===

https://www.duckdns.org/update?domains={YOURVALUE}&token={YOURVALUE}[&ip={YOURVALUE}][&ipv6={YOURVALUE}][&verbose=true][&clear=true]



Flow
- Summary
    - check DNS
    - status:   no password needed
    - sync:     password needed
    - unlock    password needed
    - retrieve  no password needed
    - lock      password needed


- check DNS:  nslookup vault.solg.duckdns.org 
  (5-minutes-renewal scheduliert in OMV: echo url="https://www.duckdns.org/update?domains=solg&token=11eb08e3-8778-43d5-b635-61126a23ef1a&ip=" | curl -k -o ~/duckdns/duck.log -K -)
  OK:
    Server:         10.255.255.254
    Address:        10.255.255.254#53

    Non-authoritative answer:
    Name:   vault.solg.duckdns.org
    Address: 192.168.1.99
- Status: Check curl http://solg.fritz.box:8087/status
  process json - see example response:

  {
    "data": {
        "object": "template",
        "template": {
            "lastSync": "2025-01-26T23:12:19.771Z",
            "serverUrl": "https://vault.solg.duckdns.org",
            "status": "locked",
            "userEmail": "s-c-h-m-i-t-t@web.de",
            "userId": "4f757a23-114f-479b-a40d-51eea8671c0c"
        }
    },
    "success": true
}

  Expect
  - json response       -> else: Check BW API and web service running (http-response code)
  - "success": true     -> else: Check BW API connection to serverURL
  - "status": "locked"  -> else: unlock not needed
  
- Loop for every WebService
  - sync: curl --json '{"password": "+49307874573"}' http://solg.fritz.box:8087/sync
    FAIL:
    {
        "message": "Syncing failed: FetchError: request to https://vault.solg.duckdns.org/identity/connect/token failed, reason: getaddrinfo ENOTFOUND vault.solg.duckdns.org",
        "success": false
    }
    OK:
    {
        "data": {
            "message": null,
            "noColor": false,
            "object": "message",
            "title": "Syncing complete."
        },
        "success": true
    }
        Expect
        - "success": true   -> else: print message

  - unlock: curl --json '{"password": "+49307874573"}' http://solg.fritz.box:8087/unlock
    OK:
    {
        "data": {
            "message": "\nTo unlock your vault, set your session key to the `BW_SESSION` environment variable. ex:\n$ export BW_SESSION=\"uE3lxS8J9nI/oKvN5cpjwyhktxqabtDbtQa71F5yFZGtatC5/2bFTLglCImOlXsAL/qAn9OqGrsoF9Wb5N07cQ==\"\n> $env:BW_SESSION=\"uE3lxS8J9nI/oKvN5cpjwyhktxqabtDbtQa71F5yFZGtatC5/2bFTLglCImOlXsAL/qAn9OqGrsoF9Wb5N07cQ==\"\n\nYou can also pass the session key to any command with the `--session` option. ex:\n$ bw list items --session uE3lxS8J9nI/oKvN5cpjwyhktxqabtDbtQa71F5yFZGtatC5/2bFTLglCImOlXsAL/qAn9OqGrsoF9Wb5N07cQ==",
            "noColor": false,
            "object": "message",
            "raw": "uE3lxS8J9nI/oKvN5cpjwyhktxqabtDbtQa71F5yFZGtatC5/2bFTLglCImOlXsAL/qAn9OqGrsoF9Wb5N07cQ==",
            "title": "Your vault is now unlocked!"
        },
        "success": true
    }
        Expect
        - "success": true   -> else: error message

  - retrieve complete: curl -s http://solg.fritz.box:8087/object/item/KabelDeutschland 
    {
        "data": {
            "collectionIds": [
            ],
            "creationDate": "2025-01-25T20:34:03.724Z",
            "deletedDate": null,
            "favorite": false,
            "fields": [
                {
                    "linkedId": null,
                    "name": "Auto",
                    "type": 0,
                    "value": "1"
                }
            ],
            "folderId": null,
            "id": "7f5fcb78-4635-498d-bf93-3d5989e68559",
            "login": {
                "fido2Credentials": [
                ],
                "password": "xcvcv",
                "passwordRevisionDate": "2025-01-26T23:06:34.629Z",
                "totp": null,
                "uris": [
                    {
                        "match": null,
                        "uri": "https://www.vodafone.de/meinvodafone/account/login"
                    }
                ],
                "username": "sdfsdfs"
            },
            "name": "KabelDeutschland",
            "notes": null,
            "object": "item",
            "organizationId": null,
            "passwordHistory": [
                {
                    "lastUsedDate": "2025-01-26T23:06:34.629Z",
                    "password": "def"
                }
            ],
            "reprompt": 0,
            "revisionDate": "2025-01-27T20:41:22.398Z",
            "type": 1
        },
        "success": true
    }
  - retrieve filtered: curl -s http://solg.fritz.box:8087/object/item/KabelDeutschland | jq '.data.login'
    {
        "fido2Credentials": [],
        "uris": [
            {
            "match": null,
            "uri": "https://www.vodafone.de/meinvodafone/account/login"
            }
        ],
        "username": "dsfsdf",
        "password": "dsfsdf",
        "totp": null,
        "passwordRevisionDate": "2025-01-26T23:06:34.629Z"
    }

  - lock: curl --json '{"password": "+49307874573"}' http://solg.fritz.box:8087/lock
    OK:
    {
        "data": {
            "message": null,
            "noColor": false,
            "object": "message",
            "title": "Your vault is locked."
        },
        "success": true
    }
    
## Normal Chrome output from WSL2
chrome-linux64$ ./chrome
[221:240:0209/173729.606808:ERROR:bus.cc(407)] Failed to connect to the bus: Failed to connect to socket /var/run/dbus/system_bus_socket: No such file or directory
[221:244:0209/173729.925155:ERROR:bus.cc(407)] Failed to connect to the bus: Failed to connect to socket /var/run/dbus/system_bus_socket: No such file or directory
[221:244:0209/173729.925634:ERROR:bus.cc(407)] Failed to connect to the bus: Failed to connect to socket /var/run/dbus/system_bus_socket: No such file or directory
[221:240:0209/173729.950902:ERROR:bus.cc(407)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix")
[221:240:0209/173729.951133:ERROR:bus.cc(407)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix")
[221:240:0209/173729.951205:ERROR:bus.cc(407)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix")
[221:240:0209/173729.951254:ERROR:bus.cc(407)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix")
[221:240:0209/173729.951710:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.DBus.NameHasOwner: object_path= /org/freedesktop/DBus: unknown error type:
[221:240:0209/173730.051235:ERROR:bus.cc(407)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix")
[221:240:0209/173730.090198:ERROR:bus.cc(407)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix")
[221:240:0209/173730.090250:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.DBus.NameHasOwner: object_path= /org/freedesktop/DBus: unknown error type:
[252:252:0209/173730.121731:ERROR:viz_main_impl.cc(185)] Exiting GPU process due to errors during initialization
[221:240:0209/173730.164442:ERROR:bus.cc(407)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix")
[221:240:0209/173730.164487:ERROR:bus.cc(407)] Failed to connect to the bus: Could not parse server address: Unknown address type (examples of valid types are "tcp" and on UNIX "unix")
[221:221:0209/173730.244940:ERROR:object_proxy.cc(576)] Failed to call method: org.freedesktop.DBus.NameHasOwner: object_path= /org/freedesktop/DBus: unknown error type:
[221:350:0209/173730.265130:ERROR:bus.cc(407)] Failed to connect to the bus: Failed to connect to socket /var/run/dbus/system_bus_socket: No such file or directory
[221:350:0209/173730.265236:ERROR:bus.cc(407)] Failed to connect to the bus: Failed to connect to socket /var/run/dbus/system_bus_socket: No such file or directory
[221:350:0209/173730.265322:ERROR:bus.cc(407)] Failed to connect to the bus: Failed to connect to socket /var/run/dbus/system_bus_socket: No such file or directory
[221:350:0209/173730.265385:ERROR:bus.cc(407)] Failed to connect to the bus: Failed to connect to socket /var/run/dbus/system_bus_socket: No such file or directory
[221:350:0209/173730.265452:ERROR:bus.cc(407)] Failed to connect to the bus: Failed to connect to socket /var/run/dbus/system_bus_socket: No such file or directory
[341:341:0209/173730.427188:ERROR:viz_main_impl.cc(185)] Exiting GPU process due to errors during initialization
[308:7:0209/173730.499359:ERROR:command_buffer_proxy_impl.cc(131)] ContextResult::kTransientFailure: Failed to send GpuControl.CreateCommandBuffer.
[221:221:0209/173733.550034:ERROR:fm_registration_token_uploader.cc(187)] Client is missing for kUser scope
[221:221:0209/173733.550090:ERROR:fm_registration_token_uploader.cc(187)] Client is missing for kUser scope
[221:241:0209/173733.653507:ERROR:registration_request.cc(291)] Registration response error message: DEPRECATED_ENDPOINT