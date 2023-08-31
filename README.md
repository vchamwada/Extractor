# Web Link Extractor


This is a simple web link extractoring tool implemented using a producer consumer design pattern

## Important Note
Includes a `urls.txt` file where you can add the websites you need to extract links from.

Output is too a file named `parsed_links.txt` in the `output` folder

## How to Use

Make sure Docker is installed in your pc

Build the docker image using the command below:
`docker build -t link-extractor .`

Run the Docker container using the command below:
`docker run -it --rm -v $(pwd)/output:/app/output:rw link-extractor`

## Further Information
Further information regarding the production process is contained in `production_process.pdf`