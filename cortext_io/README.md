## sample api calls
# Example to test the /write endpoint
curl -X POST \
  http://localhost:5000/write \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a sample text to write to the input file"}'

# Example to test the /run-java endpoint
curl -X POST \
  http://localhost:5000/run-java


# Download the HTML file to the current directory
curl -o ./000_cortext_io.html http://localhost:5000/download-html
