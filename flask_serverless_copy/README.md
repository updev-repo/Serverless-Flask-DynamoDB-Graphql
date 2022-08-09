<h1>Flask project</h1>
<h2>Built with</h2>

Python3\
Flask\
Graphql\
Sqlite\
DynamoDb Local


<h2>Virtualenv</h2>

<code>$ pip3 install virtualenvwrapper</code>\
<code> $ mkvirtualenv flask_env</code>\
<code>$ cd Flask; cd flaskTest</code>
<code>$ workon <yourvirtualenvname></code>


<h2>Install dependencies</h2>

<code>$ pip install -r requirements.txt</code>

<h2>Setting environment variables</h2>

<code>$ export FLASK_APP=main.py</code>\
<code>$ export FLASK_ENV=development</code>


<h2>Setup Database and Dynamodb local</h2>
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html

\
Users and items are created by default when program is run.
\
After installation, Type into terminal to start up dynamodb local.
<code>$ java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb<code>

<h1>Run app</h1>
<code> $ flask run </code>

Run app and visit 127.0.0.1/graphql
copy queries from the file 'query_mutations' and paste into GraphQL interface. 



