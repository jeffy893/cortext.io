# sample api calls
- run them in the following order
- note that if it gets stuck when `Running script 2/4: python3
  CORTEXT_LAYOUT_10K.py 40`; your input may be too short. Add more to it

## start the api from within the container
- make sure to expose and map the port from your host machine to the container
- `docker run -it -p 5000:5000 --name cortext_api_new cortext:latest`
    - the next time you run this, use `docker start -i cortext_api_new` instead
- then run `python3 /home/ec2-user/cortext_io/api/app.py`
- now run the following commands from another terminal

## Example to test the /write endpoint
curl -X POST \
  http://localhost:5000/write \
  -H "Content-Type: application/json" \
  -d '{"text": "The Legend of Zelda: Majoras Mask[a] is a 2000 action-adventure game developed and published by Nintendo for the Nintendo 64. It was the second The Legend of Zelda game to use 3D graphics, following Ocarina of Time (1998). Designed by a creative team led by Eiji Aonuma, Yoshiaki Koizumi, and Shigeru Miyamoto, Majoras Mask was completed in less than two years. It features enhanced graphics and several gameplay changes, but reuses elements and character models from Ocarina of Time, a creative decision made necessary by time constraints.A few months after Ocarina of Time, the character Link arrives in a parallel world, Termina, and becomes embroiled in a quest to prevent the moon from crashing in three days time. The game introduces gameplay concepts revolving around a perpetually repeating three-day cycle and the use of various masks that transform Link into different forms. As the player progresses, Link learns to play numerous melodies on his ocarina, which allow him to control the flow of time, open hidden passages, or manipulate the environment. As with other Zelda games, players must navigate through several dungeons that contain complex puzzles and enemies. Majoras Mask requires the Expansion Pak add-on for the Nintendo 64, which provides additional memory for more refined graphics and greater capacity in generating on-screen characters.Majoras Mask earned acclaim and is considered one of the best video games ever made. It received praise for its level design, story, and surrealist art direction, and has been noted for its darker tone and themes compared to other Nintendo games.[1] While it only sold about half as many copies as Ocarina of Time, it generated a cult following.[2][3] It was rereleased as part of The Legend of Zelda: Collectors Edition for the GameCube in 2003, via the Virtual Console service for the Wii and Wii U, and the Nintendo Classics service for Nintendo Switch. An enhanced remake for the Nintendo 3DS, The Legend of Zelda: Majoras Mask 3D, was released in 2015. "}'

## You can run the rest of the scripts, then go to Download
curl -X POST http://localhost:5000/run-full-process

## Or run the /run-java endpoint
curl -X POST \
  http://localhost:5000/run-java

## and then the /run-python-scripts endpoint
curl -X POST http://localhost:5000/run-python-scripts

## Download the HTML file to the current directory
curl -o ./000_cortext_io.html http://localhost:5000/download-html
