curl -X 'GET' \
  'http://127.0.0.1:8001/api/reports/formats' \
  -H 'accept: application/json'

curl -X 'GET' \
  'http://127.0.0.1:8001/api/reports/nomenclature/CSV' \
  -H 'accept: application/text'

 curl -X 'POST' \
  'http://127.0.0.1:8001/api/filter/measurement' \
  -H 'accept: application/text' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "г",
  "unique_code": "",
  "type": "like"
}'

curl -X 'POST' \
  'http://127.0.0.1:8001/api/transactions' \
  -H 'accept: text/html' \
  -H 'Content-Type: application/json' \
  -d '{
  "start_period": "1900-01-01",
  "end_period": "2024-12-31",
  "warehouse": {
    "name": "leninsky",
    "unique_code": "",
    "type": "equals"
  },
  "nomenclature": {
    "name": "С",
    "unique_code": "",
    "type": "like"
  }
}'

curl -X 'POST' \
  'http://127.0.0.1:8001/api/turnovers' \
  -H 'accept: text/html' \
  -H 'Content-Type: application/json' \
  -d '{
  "start_period": "1900-01-01",
  "end_period": "2024-12-31",
  "warehouse": {
    "name": "leninsky",
    "unique_code": "",
    "type": "equals"
  },
  "nomenclature": {
    "name": "С",
    "unique_code": "",
    "type": "like"
  }
}'

curl -X 'GET' \
  'http://127.0.0.1:8001/api/block_period' \
  -H 'accept: application/json'

 curl -X 'POST' \
  'http://127.0.0.1:8000/api/new_block_period' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "block_period": "2024-12-31"
}'

curl -X 'GET' \
  'http://127.0.0.1:8001/api/nomenclature/get?unique_code=ed906a1ea99f11efa8fd70a8d3344cb0' \
  -H 'accept: application/text'

curl -X 'PUT' \
  'http://127.0.0.1:8000/api/nomenclature/add' \
  -H 'accept: text/html' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Мясо",
  "full_name": "Мясо сырое",
  "nomenclature_group_unique_code": "ed906a1fa99f11ef9dbc70a8d3344cb0",
  "measurement_unique_code": "ed7d1c94a99f11efb92a70a8d3344cb0"
}'

curl -X 'PATCH' \
  'http://127.0.0.1:8000/api/nomenclature/update' \
  -H 'accept: text/html' \
  -H 'Content-Type: application/json' \
  -d '{
  "unique_code": "ed906a1da99f11ef97ce70a8d3344cb0",
  "name": "Сливочное масло",
  "full_name": "Сливочное масло Крестьянское",
  "nomenclature_group_unique_code": "ed906a1fa99f11ef9dbc70a8d3344cb0",
  "measurement_unique_code": "ed7d1c94a99f11efb92a70a8d3344cb0"
}'

curl -X 'DELETE' \
  'http://127.0.0.1:8000/api/nomenclature/delete' \
  -H 'accept: text/html' \
  -H 'Content-Type: application/json' \
  -d '{
  "unique_code": "ed906a1da99f11ef97ce70a8d3344cb0"
}'

curl -X 'POST' \
  'http://127.0.0.1:8000/api/save_data' \
  -H 'accept: application/json' \
  -d ''

 curl -X 'POST' \
  'http://127.0.0.1:8000/api/load_data' \
  -H 'accept: application/json' \
  -d ''

  curl -X 'GET' \
  'http://127.0.0.1:8001/api/tbs/1900-01-01/2024-12-31/leninsky' \
  -H 'accept: application/json'
