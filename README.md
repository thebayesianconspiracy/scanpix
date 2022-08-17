# scanpix

scanpix is aimed to be self hosted OR local `Google Photos`. It allows you to search local images and videos(upcoming) using text.  
I love the features of Google Photos, but don't like that I have to send them all my pictures, and that I'm at their mercy for new features.

We also have a hosted mode for demo at [scanpix.co](https://scanpix.co)

## Ultimate goal
- Link your local file storage or Dropbox/Drive 
- Create indexes for images/videos in the background
- App to search for images/videos using text
- Extend to a general `metadata(file)` -> `semantic search` paradigm


## Local Installation
```
# This repo needs pytorch to be installed
# Hopefully you're using pipenv / virtualenv / anaconda
# so that you don't mess up your package versions
pip install -r requirements.txt

# Running
# 1. Running the ML server
cd ml && python server.py --index-loc ../data/

# 2. Running the notebook
cd nbs && jupyter notebook

# 3. Running the indexer
```

Get Involved
--- 
Thanks for taking the time to join our community called [The Bayesian Conspiracy](https://github.com/thebayesianconspiracy) and start contributing!

- __Contributing__ Contributions of all kind are welcome!
  - Read [CONTRIBUTING.md](CONTRIBUTING.md) for information about setting up your environment, the workflow that we expect.
  - Join our discord channel [#scanpix](https://discord.gg/RD5RYvNw) for developer discussion.
  - Submit github issues for any feature enhancements, bugs or documentation problems. 
- __Support__ : Join the `#scanpix` channel in [TheBayesianConspiracy Discord](https://discord.gg/RD5RYvNw) to ask questions or get support from the maintainers and other uses.
- __Discuss__: Tweet using the `#scanpix` hashtag.


Acknowledgements
---
The current version is fully dependent on performance of [clip-vit-large-patch14](https://huggingface.co/openai/clip-vit-large-patch14) and even we are extremely excited by its possibilities.





License
---
[Apache License 2.0](LICENSE)



