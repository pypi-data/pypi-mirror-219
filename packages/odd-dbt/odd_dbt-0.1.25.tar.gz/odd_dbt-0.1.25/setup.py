# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['odd_dbt', 'odd_dbt.mapper', 'odd_dbt.models', 'odd_dbt.utils']

package_data = \
{'': ['*']}

install_requires = \
['dbt-core>=1.4.5,<2.0.0',
 'dbt-postgres==1.4.5',
 'dbt-redshift==1.4.0',
 'dbt-snowflake>=1.4.1,<2.0.0',
 'funcy>=1.17,<2.0',
 'loguru>=0.6.0,<0.7.0',
 'odd-models>=2.0.24,<3.0.0',
 'oddrn-generator>=0.1.70,<0.2.0',
 'psycopg2-binary>=2.9.6,<3.0.0',
 'sqlalchemy>=1.4.46,<2.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['odd_dbt_test = odd_dbt.app:app']}

setup_kwargs = {
    'name': 'odd-dbt',
    'version': '0.1.25',
    'description': 'OpenDataDiscovery Action for dbt',
    'long_description': '# OpenDataDiscovery dbt tests metadata collecting\n[![PyPI version](https://badge.fury.io/py/odd-dbt.svg)](https://badge.fury.io/py/odd-dbt)\n\nCLI tool helps automatically parse and ingest DBT test results to OpenDataDiscovery Platform.\nIt can be used as separated CLI tool or within [ODD CLI](https://github.com/opendatadiscovery/odd-cli) package which provides some useful additional features.\n\n## Installation\n```pip install odd-dbt```\n\n## Command options\n```\n╭─ Options ─────────────────────────────────────────────────────────────╮\n│    --project-dir                 PATH  [default: Path().cwd()odd-dbt] │\n│    --target                      TEXT  [default:None]                 │\n│    --profile-name                TEXT  [default:None]                 │\n│ *  --host    -h                  TEXT  [env var: ODD_PLATFORM_HOST]   │\n│ *  --token   -t                  TEXT  [env var: ODD_PLATFORM_TOKEN]  │\n│    --dbt-host                    TEXT  [default: localhost]           │\n│    --help                              Show this message and exit.    │\n╰───────────────────────────────────────────────────────────────────────╯\n```\n\n\n## Command run example\nHow to create [collector token](https://docs.opendatadiscovery.org/configuration-and-deployment/trylocally#create-collector-entity)?\n```bash\nodd_dbt_test --host http://localhost:8080 --token <COLLECTOR_TOKEN>\n```\n\n\n\n## Supported data sources\n| Source    |       |\n| --------- | ----- |\n| Snowflake | 1.4.1 |\n| Redshift  | 1.4.0 |\n| Postgres  | 1.4.5 |\n| MSSQL     |       | \n\n## Requirements\nLibrary to inject Quality Tests entities requires presence of corresponding with them datasets entities in the platform.\nFor example: if you want to inject data quality test of Snowflake table, you need to have entity of that table present in the platform.\n\n## Supported tests\nLibrary supports for basics tests provided by dbt.\n- `unique`: values in the column should be unique\n- `not_null`: values in the column should not contain null values\n- `accepted_values`: column should only contain values from list specified in the test config\n- `relationships`: each value in the select column of the model exists as a specified field in the reference table (also known as referential integrity)\n\n## ODDRN generation for datasets\n`host_settings` of ODDRN generators required for source datasets are loaded from `.dbt/profiles.yml`.\n\nProfiles inside the file looks different for each type of data source.\n\n**Snowflake** host_settings value is created from field `account`. Field value should be `<account_identifier>`\nFor example the URL for an account uses the following format: `<account_identifier>`.snowflakecomputing.com\nExample Snowflake account identifier `hj1234.eu-central-1`.\n\n**Redshift** and **Postgres** host_settings are loaded from field `host` field.\n\nExample Redshift host: `redshift-cluster-example.123456789.eu-central-1.redshift.amazonaws.com`\n',
    'author': 'Mateusz Kulas',
    'author_email': 'mkulas@provectus.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
