# tableau_helpers

A wrapper for the tableau-server-client and hyper-api which abstracts away
boilerplate and in some cases provides a CLI which works without admin privileges.

## tableau_helpers.hyper

Create hyperfiles from one or more csvs by providing a source, destination, 
schema, and optional parameters.

### Code integration

See [test_hyper.py](./tests/test_hyper.py) for some examples in action. 

## tableau_helpers.publish

Upload datasources from your machine to the tableau server by providing a
hyperfile as a source and a project as a destination. 

### Code integration

See [test_publish.py](./tests/test_server.py) for an example. 

## Development

There are a few steps to set up the development environment.
1. Make a copy of [.env.sample](.env.sample) and save it as .env
2. Add your [Personal Access Token](https://help.tableau.com/current/server/en-us/security_personal_access_tokens.html) to .env
3. Set the tableau-server url in .env ex: `https://tableau-test.rki.local`
4. If your SSL cert is self signed, download a copy of your pem and provide the path in .env, otherwise delete the cert entry.
5. Install [pre-commit](https://pre-commit.com/) either in an environment or for your user.
6. Setup pre-commit hooks
   1. `pre-commit install -t pre-commit`
   2. `pre-commit install -t pre-push`
7. Install [tox](https://tox.wiki/en/latest/) either in an environment or for your user.
   1. Test run tox for unit tests `tox` (note: some integration tests require a connection to your tableau server)
   2. Test run tox to reformat files `tox -e lint`
