# This is simple search

## setup project
git clone git@bitbucket.org:arun6582/simple-search-py.git

`cd simple-search-py`
`sudo pip install virtualenv`
`virtualenv env`
`source env/bin/activate`
`pip install -r requirements.txt`

## Run first instance
`./manage.py runserver 8000 --settings=simple_search.node1`


## Run second instance in second terminal after going into same directory
`source env/bin/activate`
`./manage.py runserver 8001 --settings=simple_search.node2`


...open http://localhost:8000/ in the browser to live.
...open http://localhost:8001/ to see second instance.


...First instance is connected to second node for searches that means data uploaded
...to second node can also be searched through node1.

...You can also configure node2 to search data from node1 by editing file node2.py
just add node1 base url in othernodes array in DB_SETTINGS varialbe just like
node1.py.


...You can have as many node as possible and you can configure any node to search on
any other node.
...Every node is independent of the other in terms of seperation of machines.

## Features
1. multi node search
2. term frequency
3. inverse document frequency
4. granular caching for calculations
5. fields can be specified during search
6. self designed minimal DB
