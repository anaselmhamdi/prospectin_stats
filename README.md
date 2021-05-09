# Storing and querying ProspectIn data

A service made to handle the scraping of the ProspectIn company report sent via email.

I currently use Zapier to trigger the scraping and the data storage into a MongoDB.

To use it as I did in the [article](https://www.anas.link/post/creating-a-custom-dashboard-without-integration-or-api-the-prospectin-use-case):

Clone the repo:

`git clone https://github.com/anaselmhamdi/prospectin_stats.git`

Change the `.env` file with your mongoDB credentials.

Deploy with Serverless (with AWS credentials configured):

`cd prospectin_stats`  
`serverless deploy`

Open an issue or [contact me](mailto:me@anas.link) if you run into trouble
