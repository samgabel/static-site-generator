# Static Site Generator (python)




## Overview

This is a static site generator written completely in Python. It simply takes static assets located in `/static` and markdown notes located in `/content`, and delivers an HTML webpage on `localhost:8888`. The output webpage replicates the directory structure found in `/content`. During the conversion process, it uses the template `template.html` in order to structure the newly converted tags.

![showcase](https://github.com/samgabel/static-site-generator/blob/main/showcase.png?raw=true)



## Usage

1. Clone this repository to your client machine
2. Run `chmod +x main.sh` file in the root of the project
3. Now run the `main.sh` script to convert the sample markdown files (in `/content`) into HTML files in a newly created directory called `/public`
4. Navigate to `localhost:8888` to see the newly created webpage
5. (Optional) Replace the sample files in `/content` and `/static` with your own files!
