### Docker image for reveal js

    guna.n

### Command to create new reveal js presentation

     docker run -it --name revealjs-builder3 -v $(pwd):/app revealjs /bin/bash

- Steps:

  - if you have and .adoc file inside what ever the directory thats not and matter.

  - docker run -it --name (docker container name) -v mapping the volume inside your host machine to dockerized machine.

  - -v (your machine directory) --> where the asciidoc file present's.

  - after the semicolon : operator which means that where you needs to points.

  - user/home/ is the default working directory inside the image.

  - please make sure on /app directory .

  - all the volume inside your local machine will will points into that /app directory only.

  - if you needed to generate the presentation file you explicitly move the file and generate that as of now.

```bash

    Thankyou Happy Coding :)
```
