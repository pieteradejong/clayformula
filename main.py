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




TODO:
? how should rowData be structured?
? what should func sign for def runWorkflowForRow(updatedCell, rowData):


"""

class Table:
	# def __init__(self, title: str = 'DefaultNewTable', colNames: list = [], dataRows: dict = {}):
	def __init__(self, colNames: list = []):
		self.colNames = colNames
		self.dataRows = {}
		# if dataRows:
		# 	self.dataRows = dataRows
		# 	self.colNames = dataRows.keys()
		# else:
		# 	self.colNames = colNames
		# 	self.dataRows = { cn: [] for cn in colNames }


class Column:
	contents: str
	dependencies: list

# FormulaColumn:



def refreshUI(rowData):
	print(f'Start: printing row data')
	print(rowData)
	for row in rowData:
		print(f'row of data: {row}')
	print(f'End of: printing row data')


def evaluateFormula(formula, inputValues):
	pass
# 	 Support two types of formulas
 # 	 - string concatenation of the input values
   # - extracting a field from a value in an array of values

def runWorkflowForRow(updatedCell, rowData):
	refreshUI(rowData)



def main():
	print(f'Starting Clay Take home exercise')
	initialColumns = ['First Name', 'Second Name', 'Company Name']
	initialRowData = {
		1: {
			initialColumns[0]: 'Kareem',
			initialColumns[1]: 'Amin',
			initialColumns[1]: 'Clay'
		},
		2: {
			initialColumns[0]: 'Kareem',
			initialColumns[2]: 'Clay'
		}
	}

	table = Table(initialColumns)

	firstUpdatedCell = {'colName': 'First Name', 'value': 'Luna'}
	rowData = runWorkflowForRow(firstUpdatedCell, initialRowData);

	secondUpdatedCell = {'colName': 'Second Name', 'value': 'Ruan'}
	rowData = runWorkflowForRow(secondUpdatedCell, initialRowData);

	thirdUpdatedCell = {'colName': 'Company Name', 'value': 'Clay'}
	runWorkflowForRow(thirdUpdatedCell, initialRowData)



	print(f'Finished running Clay Take home exercise')



if __name__ ==  "__main__":
	main()
	