#!/bin/bash
curl https://api.socketxp.com/v1/tunnels \
  -X DELETE \
  -H "Authorization: Bearer <YOUR TOKEN>" 
sudo socketxp connect http://0.0.0.0:7656 -s raspi-nfcapi &> /dev/null &

