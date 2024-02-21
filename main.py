"""
"Clay Take Home Assignment"
Solution by: Pieter de Jong, February 16, 2023
source:
https://clayrun.notion.site/Clay-Take-Home-Assignment-e39f93736dbb4f709cf033fbe504e44e


At first glance, code structure/reqs seem TypeScript/React centric. My implementation will more aimed at 
an data/API backend rather than driving a UI. 

Core abstraction: Table as nested dictionary: 
{
	RowID: RowDataDict(dict),
	RowID: RowDataDict(dict),
	..
}
RowID is in 1,2,3,4,5,.....
RowDataDict is { colName: colValue, colName: colValue, ... }

Function signatures:

def runWorkflowForRow(rowId: int, cellUpdate: dict[str, str]) -> rowData
# if rowId exists, update given column; return row
def refreshUI(rowId: int) -> None:	
# pretty-print values in row


"""
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Table:

	def __init__(self):
		# TODO: constructor should take alternate column names?
		self.COLUMN_NAMES = {
			'COL_NAME_FIRST_NAME': 'First Name',
			'COL_NAME_LAST_NAME': 'Last Name',
			'COL_NAME_COMPANY_NAME': 'Company Name',
			'COL_NAME_PERFORM_SEARCHL': 'Perform Search',
			'COL_NAME_LINKEDIN_URL': 'LinkedIn URL',
			'COL_NAME_LINKEDIN_DATA': 'LinkedIn Data',
			'COL_NAME_G_SEARCH_INPUT': 'Google Search Input',
		}
		self.rows = {}
		
	def appendRow(self, updatedValuesByColumn: dict) -> [int, dict]:
		new_row_id = len(self.rows) + 1
		self.rows[new_row_id] = { colName: "" for colName in self.COLUMN_NAMES.values()}
		self.updateRow(new_row_id, updatedValuesByColumn)
		return [new_row_id, ]

	def updateRow(self, rowId: int, updatedValuesByColumn: dict) -> dict:
		"""
		updates given row with set of new column values. 
		First validates that column names exist, logs error if dont exist
		"""
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
		
		return updated_columns

	def refreshUI(self, rowId: int, col_name: str, col_updated_value: str) -> None:
		logging.info(f'Pringing row data:')
		print(f"Updated: row [{rowId}]: column [{col_name}] was updated to: [{col_updated_value}]")
		logging.info(f'Done printing row data.')


	def evaluateFormula(formula, inputValues):
		pass
	# 	 Support two types of formulas
	# 	 - string concatenation of the input values
	# - extracting a field from a value in an array of values


def main():
	logging.info(f'Starting Clay Take home exercise')
	
	table = Table()

	initialRowFirst = {
		table.COLUMN_NAMES['COL_NAME_FIRST_NAME']: 'Kareem',
		table.COLUMN_NAMES['COL_NAME_LAST_NAME']: 'Amin',
		table.COLUMN_NAMES['COL_NAME_COMPANY_NAME']: 'Clay',
	}

	initialRowSecond = {
		table.COLUMN_NAMES['COL_NAME_FIRST_NAME']: 'Jane',
		table.COLUMN_NAMES['COL_NAME_COMPANY_NAME']: 'Clay',
	}
	
	table.appendRow(initialRowFirst)
	table.appendRow(initialRowSecond)
	# STATUS: added to clas: update and append, now must successful add 2 rows and some new values
	# THEN: add new types of columns



	logging.info(f'Finished running Clay Take home exercise')


if __name__ ==  "__main__":
	main()
	