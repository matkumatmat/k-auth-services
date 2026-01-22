#!/bin/bash

echo "=== Test 1: Health Check ==="
curl -s http://localhost:8000/health | jq .
echo -e "\n"

sleep 1

echo "=== Test 2: Registration with Body (to see request logging) ==="
curl -s -X POST http://localhost:8000/api/v1/register/email \
  -H "Content-Type: application/json" \
  -d '{
    "email": "kayez@gmail.com",
    "password": "SuperSecret123!",
    "full_name": "Kayez Test"
  }' | jq .
echo -e "\n"

sleep 1

echo "=== Test 3: Invalid Request (422 Validation Error) ==="
curl -s -X POST http://localhost:8000/api/v1/validate/quota/consume \
  -H "Content-Type: application/json" \
  -d '{}' | jq .
echo -e "\n"

sleep 1

echo "=== Test 4: Resend OTP (to see domain exception handling) ==="
curl -s -X POST http://localhost:8000/api/v1/otp/resend/email \
  -H "Content-Type: application/json" \
  -d '{"email": "kayez@gmail.com"}' | jq .
echo -e "\n"
