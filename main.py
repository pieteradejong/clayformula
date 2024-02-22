"""
"Clay Take Home Assignment"
Solution by: Pieter de Jong, February 16, 2023
source:
https://clayrun.notion.site/Clay-Take-Home-Assignment-e39f93736dbb4f709cf033fbe504e44e


At first glance, code structure/reqs seem TypeScript/React centric. My implementation will more aimed at 
an data/API backend rather than driving a UI. 

Core entity: Table as nested dictionary:
{
	1: {col: value, col: value, ...}
	2: {col: value, col: value, ...}
	..
}

Note on time spent: 
- The assignment document is quite lengthy, and esp. the requirements/implementation of step 3 
was hard to follow. Therefore I timeboxed my work and focused on steps 1 and 2. 
Full implementation requires a DAG as noted in notes below.

VERIFICATION:
For verification flow, see notes under main().

Design decisions:
- prod readiness: this would be the beginning of the Table of a backend Data service/API to 
back the front end UI; added some logging as good practice; requires unit testing; limited input validation
- column names hardcoded on instance, could be provided or set on class
- column dependencies: Main columns are handled by updateRow, one dependent column is handled by
	a separate function. Full dependency requires a DAG and traversal, including async API calls.

"""
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Table:

	def __init__(self):
		self.COLUMN_NAMES = {
			'COL_NAME_FIRST_NAME': 'First Name',
			'COL_NAME_LAST_NAME': 'Last Name',
			'COL_NAME_COMPANY_NAME': 'Company Name',
			'COL_NAME_G_SEARCH_INPUT': 'Google Search Input',
			'COL_NAME_PERFORM_SEARCH': 'Perform Search',
			'COL_NAME_LINKEDIN_URL': 'LinkedIn URL',
			'COL_NAME_LINKEDIN_DATA': 'LinkedIn Data'
		}
		self.rows = {}

	def _evaluateFormula(self, formula = None, inputValues: list = []) -> str:
		if formula not in ['CONCAT', 'EXTRACT']:
			raise ValueError('Argument error: no or wrong formula [{formula}] supplied.')
		elif formula == 'CONCAT':
			if len(inputValues) == 3: # DESIGN CHOICE TO NOT ALLOW >3
				return 'linkedin.com ' + ' '.join(inputValues)
			else:
				return 'MISSING INPUT'
		elif formula == 'EXTRACT':
			pass 
	
		
	def appendRow(self, updatedValuesByColumn: dict) -> int:
		new_row_id = len(self.rows) + 1
		self.rows[new_row_id] = { colName: "" for colName in self.COLUMN_NAMES.values()}
		self.updateRow(new_row_id, updatedValuesByColumn)
		return new_row_id

	
	def updateRowForDependentColumn(self, rowId: int) -> None:
		if rowId not in self.rows:
			logging.error(f"Row ID {rowId} does not exist in the table.")
			return
		
		row = self.rows[rowId]
		inputValues = [
			row[self.COLUMN_NAMES['COL_NAME_FIRST_NAME']],
			row[self.COLUMN_NAMES['COL_NAME_LAST_NAME']],
			row[self.COLUMN_NAMES['COL_NAME_COMPANY_NAME']]
		]

		if all(inputValues):
			self.rows[rowId][self.COLUMN_NAMES['COL_NAME_G_SEARCH_INPUT']] = self._evaluateFormula(formula='CONCAT', inputValues=inputValues)
			self.refreshUI(rowId)
	
	def updateRow(self, rowId: int, updatedValuesByColumn: dict) -> list:
		if rowId not in self.rows:
			logging.error(f"Row ID {rowId} does not exist in the table.")
			return

		updated_columns = []
		for col_name in updatedValuesByColumn.keys():
			if col_name not in self.COLUMN_NAMES.values():
				logging.error(f"Column name '{col_name}' does not exist in the table. Proceeding with other columns.")
			else:
				self.rows[rowId][col_name] = updatedValuesByColumn[col_name]
				updated_columns.append(col_name)
				self.refreshUI(rowId, col_name, self.rows[rowId][col_name])
		
		self.updateRowForDependentColumn(rowId)

		return updated_columns

	def refreshUI(self, rowId: int, col_name: str = None, col_updated_value: str = None) -> None:
		if col_name and col_updated_value:
			logging.info(f"UI Refresh: ([{col_name}] updated to: [{col_updated_value}]; row [{rowId}]: [{self.rows[rowId]}] ")
		else:
			logging.info(f"UI Refresh: row [{rowId}]: [{self.rows[rowId]}]")


def main():
	logging.info(f'Starting Clay Take home exercise')
	
	table = Table()

	"""
	VERIFICAITON: Verify correct flow:
	1) Append row 1 First name, verify G_SEARCH dependent column displays 'MISSING INPUT'
	2) Update row 1 Last name, verify two fields populated and G_SEARCH column ditto
	3) Update row 1 Company name, verify dependent field is the concatination
	4) Append full row 2, verify row 1 exists, and row 2 fuly populated including G_SEARCH column
	5) Update row 1 Last name, verify row is updated correctly.
	
	"""

	cellValue = {
		table.COLUMN_NAMES['COL_NAME_FIRST_NAME']: 'Kareem'
	}
	logging.info("\033[95mExpect only first name to be populated:\033[0m")
	id1 = table.appendRow(cellValue)

	cellValue = {
		table.COLUMN_NAMES['COL_NAME_LAST_NAME']: 'Amin',
	}
	logging.info("\033[95mExpect first name and last name to be populated:\033[0m")
	table.updateRow(id1, cellValue)

	cellValue = {
		table.COLUMN_NAMES['COL_NAME_COMPANY_NAME']: 'Clay',
	}
	logging.info("\033[95mExpect first name, last name, company name, and `Google Search Input` to be populated:\033[0m")
	table.updateRow(id1, cellValue)

	secondRow = {
		table.COLUMN_NAMES['COL_NAME_FIRST_NAME']: 'Jane',
		table.COLUMN_NAMES['COL_NAME_LAST_NAME']: 'Doe',
		table.COLUMN_NAMES['COL_NAME_COMPANY_NAME']: 'Hooli',
	}
	logging.info("\033[95mExpect second row to be populated, including 4 cells:\033[0m")
	id2 = table.appendRow(secondRow)

	cellValue = {
		table.COLUMN_NAMES['COL_NAME_LAST_NAME']: 'Smith'
	}
	logging.info("\033[95mExpect first row last name to be updated, including dependent column:\033[0m")
	table.updateRow(id1, cellValue)

	"""old flow:
	initialRowFirst = {
		table.COLUMN_NAMES['COL_NAME_FIRST_NAME']: 'Kareem',
		table.COLUMN_NAMES['COL_NAME_LAST_NAME']: 'Amin',
		table.COLUMN_NAMES['COL_NAME_COMPANY_NAME']: 'Clay',
	}

	initialRowSecond = {
		table.COLUMN_NAMES['COL_NAME_FIRST_NAME']: 'Jane',
		table.COLUMN_NAMES['COL_NAME_COMPANY_NAME']: 'Clay',
	}
	
	id1 = table.appendRow(initialRowFirst)
	id2 = table.appendRow(initialRowSecond)

	table.updateRowForDependentColumn(id1)
	"""

	logging.info(f'Finished running Clay Take home exercise')


if __name__ ==  "__main__":
	main()
	