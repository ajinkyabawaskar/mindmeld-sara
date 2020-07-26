# mindmeld-sara
A virtual travel assistant based on MindMeld capabilities, interfaced by Cisco Webex Teams.

## Getting Started
Requires `mindmeld` which depends on `python3.6`, `virtualenv`, `pip`, and `elasticsearch`.
Find in-depth installation of `mindmeld` here [Install Mindmeld](https://www.mindmeld.com/docs/userguide/getting_started.html)
- Download / clone the repository.
- Enter the virtual environment using `(venv) ~/$ source bin/activate` (on Ubuntu)
- To verify installation of `mindmeld` run: `(venv) ~/$ mindmeld`.
- Run: `(venv) ~/$ mindmeld num-parse` to start numerical parser.
- Verify `elasticsearch` is running in another terminal. 
- Rename the repository folder `mindmeld-sara` to `sara`
- Load data to knowledge base by running:
  - `(venv) ~/$ python3.6 -m sara load-kb sara locations sara/data/locations.json`
  - `(venv) ~/$ python3.6 -m sara load-kb sara india sara/data/india.json`
- Train the model by: `(venv) ~/$ python3.6 -m sara build`
- Open a interactive CLI with chatbot: `(venv) ~/$ python3.6 -m sara converse`

## Files and Directories
This section includes information about directory structure and file naming convention
- The training data for user queries is sorted in the `domains` folder, with a `train.txt` and `test.txt` inside `domains/<domain_name>/<intent_name>` folder.
- The training data for entities in query is sorted in `entities` folder, with a `gazetter.txt` and `mapping.json` inside `entities/<entity_name>` folder.
- The `__init__.py`, `__main__.py`, `root.py` are base files to create application from `mindmeld`
- The `config.py` file contains the configuration for machine learning models.
- Filenames starting with `d_` indicate they contain app handlers for particular domain.`d_` is followed by the domain name, like `d_<domain_name>.py`
- `data` folder is used to store `.sample.json` files which are returned by APIs and `.json` training data for creating Knowledge Base
- In `utilities` folder, filenames starting with `u_` are utility files used to retrieve data from API.
- `extras` folder is used to generate, update or clean training data, and other extra training data, notes, etc.