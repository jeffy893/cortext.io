# sample api calls
- run them in the following order
- note that if it gets stuck when `Running script 2/4: python3
  CORTEXT_LAYOUT_10K.py 40`; your input may be too short. Add more to it

## Example to test the /write endpoint
curl -X POST \
  http://localhost:5000/write \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a sample text to write to the input file"}'

## You can run the rest of the scripts, then go to Download
curl -X POST http://localhost:5000/run-full-process

## Or run the /run-java endpoint
curl -X POST \
  http://localhost:5000/run-java

## and then the /run-python-scripts endpoint
curl -X POST http://localhost:5000/run-python-scripts

## Download the HTML file to the current directory
curl -o ./000_cortext_io.html http://localhost:5000/download-html
