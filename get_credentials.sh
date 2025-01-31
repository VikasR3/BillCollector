#!/bin/bash

#curl --json '{"password": "+49307874573"}' http://solg.fritz.box:8087/unlock
curl -X POST -H 'Content-Type: application/json' -d '{"password": "+49307874573"}' http://solg.fritz.box:8087/unlock

#curl --json '{"password": "+49307874573"}' http://solg.fritz.box:8087/sync
curl -X POST -H 'Content-Type: application/json' -d '{"password": "+49307874573"}' http://solg.fritz.box:8087/sync

curl -s http://solg.fritz.box:8087/object/item/KabelDeutschland | jq '.data.login'