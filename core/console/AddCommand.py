import click
import urllib.request
import requests
from terminaltables import DoubleTable # type: ignore
from core.base.ModuleManager import ModuleManager

@click.group()
def Add():
	"""Add new components to alice"""
	pass


@Add.command()
@click.argument('author_name')
@click.argument('module_name')
def module(author_name: str, module_name: str):
	"""Add module from dedicated repository to Alice"""

	TABLE_DATA = [['Module Installer']]
	table_instance = DoubleTable(TABLE_DATA)
	click.secho('\n{}\n'.format(table_instance.table), fg='yellow')

	try:
		url = '{0}/{1}/{2}/{2}.install'.format(ModuleManager.GITHUB_BARE_BASE_URL, author_name, module_name)
		req = requests.get(url)

		if req.status_code // 100 == 4:
			click.echo(
				f"> Unknown {click.style(f'{author_name}/{module_name}', fg='red')} pair\n"
				f"- You can use {click.style('author:list', fg='yellow')} to list all authors\n"
				f"- You can use {click.style('module:list', fg='yellow')} to list all modules from an author\n\n",
				err=True
			)
			return

		module = req.json()
		click.echo(
			"+ Informations:\n"
			"===============\n"
			f"name: {click.style(str(module['name']), fg='yellow')}\n"
			f"version: {click.style(str(module['version']), fg='yellow')}\n"
			f"author: {click.style(module['author'], fg='yellow')}\n"
			f"maintainers: {click.style(', '.join(module['maintainers']), fg='yellow')}\n"
			f"description: {click.style(module['desc'], fg='yellow')}\n"
			f"aliceMinVersion: {click.style(str(module['aliceMinVersion']), fg='yellow')}\n"
			f"pip requirements: {click.style(', '.join(module['pipRequirements']), fg='yellow')}\n"
			f"system requirements: {click.style(', '.join(module['systemRequirements']), fg='yellow')}\n\n"

			"+ Conditions:\n"
			"=============\n"
			f"lang: {click.style(', '.join(module['conditions']['lang']), fg='yellow')}\n\n"
		)

		urllib.request.urlretrieve(url, 'system/moduleInstallTickets/{}.install'.format(module_name))

	except Exception as e:
		click.secho(f'Failed to add the module: {e}', err=True, fg='red')


