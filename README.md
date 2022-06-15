# scanpix

scanpix is a `local Google Photos`. It allows you to search local images and videos using text. I love the features of Google Photos, but don't like that I have to send them all my pictures, and that I'm at their mercy for new features.

## Ultimate goal
- Link your local file storage or Dropbox/Drive 
- Create indexes for images/videos in the background
- App to search for images/videos using text
- Extend to a general `metadata(file)` -> `semantic search` paradigm

### Components
- Worker(s) - Service thats always up which takes disk as input, manages state of indexing and runs model on new images and sends to DB
- Databse - DB to store all indexing results
- Search FE - Frontend app to search on - Electron
- Research nbs - Jupyter Notebook(s) to play around on model training and evaluation

## v1.0

### Tasks
- To run using docker compose
- Worker to index images
- Decide and use appropriate similarity search engine


## v1.1

### Features
- Personalised search
- Negative search
- Video search


## Questions to think about
- Do we ever learn from multiple users? How do we get feedback on performance/quality? User generated? Self generated?
- How do we push new models?